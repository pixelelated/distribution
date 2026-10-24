#!/usr/bin/env python3
"""Actual subprocess controls for #444; no VM or network required."""
from pathlib import Path
import atexit
import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

root = Path(__file__).resolve().parents[3]
launcher = root / 'tools/watch-build-submit'
base = Path(tempfile.mkdtemp(prefix='pixelelated-watch-submit-'))
# The fixture root is removed however the control ends (#913).
atexit.register(shutil.rmtree, base, True)
(base / 'tools').mkdir()
for name in ['watch-build', 'watch-job']:
    shutil.copy2(root / 'tools' / name, base / 'tools' / name)
# The runner refuses an unadmitted run (#493): the fixture is an admitted
# checkout, as test-build-monitor's is, and each launch takes a receipt
# prepared just before it, since an admission binds the registry generation.
(base / 'scripts').mkdir()
(base / 'scripts/README').write_text('fixture\n')
(base / 'Makefile').write_text('')
helper_spec = importlib.util.spec_from_file_location(
    'admission_test_fixture', root / 'tools/host-maintenance/admission-test-fixture.py')
helper = importlib.util.module_from_spec(helper_spec)
helper_spec.loader.exec_module(helper)
admission, admission_plan, _ = helper.prepare_fixture(base, root)


def admitted_environment(name):
    receipt = base / ('admission-' + name + '.json')
    admission.prepare(admission_plan, receipt)
    return dict(os.environ, PIXELELATED_BUILD_ADMISSION=str(receipt), XDG_STATE_HOME=str(helper.state_dir(base)))


rows = []


def wait_file(path):
    deadline = time.monotonic() + 15
    while not path.exists():
        assert time.monotonic() < deadline, str(path)
        time.sleep(.05)
    return path.read_text()


def submit(owner, code):
    owner.mkdir()
    args = [sys.executable, str(launcher), '--owner', str(owner), '--',
            '--interval', '1', '--stall-min', '1', '--',
            sys.executable, '-c', 'import time;time.sleep(2);raise SystemExit(' + str(code) + ')']
    env = admitted_environment(owner.name)
    result = subprocess.run(args, cwd=base, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['state'] == 'submitted'
    assert not (owner / 'tool-wrapper.rc').exists()
    duplicate = subprocess.run(args, cwd=base, env=env, capture_output=True, text=True)
    assert duplicate.returncode == 2
    got = int(wait_file(owner / 'tool-wrapper.rc'))
    assert got == code
    result = json.loads(wait_file(owner / 'launcher-result.json'))
    assert result['runner_returncode'] == code
    rows.append({'case': 'success' if code == 0 else 'nonzero',
                 'submission_rc': 0, 'completion_rc': got, 'duplicate_rc': 2})


submit(base / 'success', 0)
submit(base / 'nonzero', 7)
owner = base / 'lost-submitter'; owner.mkdir()
command = [sys.executable, str(launcher), '--owner', str(owner), '--',
           '--interval', '1', '--stall-min', '1', '--',
           sys.executable, '-c', 'import time;time.sleep(3);raise SystemExit(0)']
controller = subprocess.Popen([sys.executable, '-c',
    'import subprocess,sys,time;subprocess.run(sys.argv[1:],check=True);time.sleep(30)',
    *command], cwd=base, env=admitted_environment(owner.name),
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
wait_file(owner / 'launcher-start.json')
os.killpg(controller.pid, signal.SIGTERM)
assert controller.wait(timeout=5) == -signal.SIGTERM
assert int(wait_file(owner / 'tool-wrapper.rc')) == 0
result = json.loads(wait_file(owner / 'launcher-result.json'))
assert result['runner_returncode'] == 0
rows.append({'case': 'submitting_process_group_terminated', 'controller_signal': 15,
             'detached_completion_rc': 0})
for case in ['success', 'nonzero', 'lost-submitter']:
    owner = base / case
    console = (owner / 'console.log').read_text()
    run = Path(console.split('watch-build: recording in ', 1)[1].splitlines()[0])
    assert int((run / 'build.rc').read_text()) == (7 if case == 'nonzero' else 0)
    assert (run / 'build.status').read_text().startswith('state:       finished\n')
    for name in ['command.pid', 'watcher.pid']:
        proc = Path('/proc') / (run / name).read_text().strip()
        if proc.exists():
            assert (proc / 'stat').read_text().rsplit(')', 1)[1].split()[0] == 'Z'
rows.append({'case': 'all_standard_terminal_receipts_and_process_cleanup', 'pass': True})
print(json.dumps({'passed': True, 'fixture': str(base), 'controls': rows}, indent=2))
