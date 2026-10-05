"""Run on an owned QA guest only; installed ES + actual shell writers, #320."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

base = Path('/tmp/pixelelated-settings-race')
config = Path('/storage/.config/system/configs/system.cfg')
backup = Path(str(config) + '.backup')
dropin = Path('/run/systemd/system/essway.service.d/90-settings-race.conf')
rows = []
def check(name, okay, **detail):
    rows.append({'name': name, 'pass': bool(okay), **detail})
    print(('PASS ' if okay else 'FAIL ') + name, flush=True)
    if not okay:
        raise RuntimeError(name)
def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True)
def sha(data):
    return hashlib.sha256(data).hexdigest()
def wait_marker(step):
    mark = base / f'ready-{step}'
    for _ in range(400):
        if mark.exists():
            pid, observed = map(int, mark.read_text().split())
            check(f'pause {step} is the installed ES', observed == step and
                  os.readlink(f'/proc/{pid}/exe') == '/usr/bin/emulationstation', pid=pid)
            return pid
        time.sleep(.1)
    diagnostics = {'processes': [], 'service': subprocess.run(
        ['systemctl', 'show', 'essway', '-p', 'ActiveState', '-p', 'SubState', '-p', 'MainPID', '-p', 'ExecMainCode', '-p', 'ExecMainStatus'],
        capture_output=True, text=True).stdout}
    for proc in Path('/proc').glob('[0-9]*'):
        try:
            name = (proc/'comm').read_text().strip()
            if name not in ['emulationstation', 'emulationstatio', 'start_es.sh', 'bash']: continue
            env = (proc/'environ').read_bytes().split(b'\0')
            diagnostics['processes'].append({'pid': int(proc.name), 'comm': name,
                'exe': os.readlink(proc/'exe'),
                'probe_env': b'PIXELELATED_SETTINGS_RACE=owned-qa-320' in env,
                'preload_env': b'LD_PRELOAD=/tmp/pixelelated-settings-race/pause-unlock.so' in env,
                'probe_mapped': 'pause-unlock.so' in (proc/'maps').read_text()})
        except (FileNotFoundError, ProcessLookupError): pass
    journal = subprocess.run(['journalctl', '-u', 'essway', '-n', '80', '--no-pager'], capture_output=True, text=True).stdout
    diagnostics['probe_trace'] = (base/'probe-trace').read_text() if (base/'probe-trace').exists() else 'missing'
    diagnostics['loader_errors'] = [line for line in journal.splitlines()
                                    if 'ld.so:' in line or 'cannot be preloaded' in line]
    (base/'diagnostics.json').write_text(json.dumps(diagnostics, indent=2)+'\n')
    raise RuntimeError(f'ES pause {step} did not arrive; diagnostics retained')

def main():
    check('candidate BUILD_ID', 'cf511ce79b83cba7fea8b14cfa3d04fb13e4b4fb' in Path('/etc/os-release').read_text())
    expected = json.loads((base / 'expected.json').read_text())
    for path, digest in expected.items():
        actual = sha(Path(path).read_bytes())
        check('installed bytes ' + path, actual == digest, actual_sha256=actual, expected_sha256=digest)
    check('owned new drop-in', not dropin.exists())
    run('systemctl', 'stop', 'essway')
    originals = {p: (p.read_bytes(), p.stat().st_mode & 0o777) if p.exists() else None
                 for p in [config, backup, Path(str(config) + '.tmp'), Path(str(backup) + '.tmp')]}
    try:
        check('no settings writer lock', not Path('/tmp/.system.cfg.lock').exists())
        old = b'\n'.join(line for line in originals[config][0].splitlines()
                         if not line.startswith(b'qa.settings.race=')) + b'\nqa.settings.race=older\n'
        check('whole starting recovery record', b'system.hostname=' in old and old.endswith(b'\n'))
        # chooseConfig deliberately preserves a non-prefix partial hand edit.
        # Model an actual interrupted write: a strict prefix of the newer record.
        damaged = old[:-4]
        check('damage is a strict cut prefix, not a different hand edit',
              old.startswith(damaged) and len(damaged) < len(old) and not damaged.endswith(b'\n'))
        config.write_bytes(damaged); config.chmod(0o600)
        backup.write_bytes(old); backup.chmod(0o600)
        for p in [Path(str(config)+'.tmp'), Path(str(backup)+'.tmp')]:
            p.unlink(missing_ok=True)
        dropin.parent.mkdir(parents=True, exist_ok=True)
        dropin.write_text('[Service]\nEnvironment=LD_PRELOAD=/tmp/pixelelated-settings-race/pause-unlock.so\nEnvironment=PIXELELATED_SETTINGS_RACE=owned-qa-320\nRestart=no\n')
        run('systemctl', 'daemon-reload'); run('systemctl', 'start', 'essway')
        pid1 = wait_marker(1)
        check('ES recovered damaged live file before script', config.read_bytes() == old and backup.read_bytes() == old,
              damaged_sha256=sha(damaged), recovered_sha256=sha(config.read_bytes()))
        check('ES released shared settings lock', not Path('/tmp/.system.cfg.lock').exists())
        run('/bin/bash', '-c', '. /etc/profile; set_setting qa.settings.race newer || exit; wait_lock || exit; /usr/bin/chksysconfig backup; task_rc=$?; rm -f "$J_CONF_LOCK"; exit "$task_rc"')
        newer = config.read_bytes()
        check('actual shell writers published newer live and record', b'qa.settings.race=newer\n' in newer and
              newer != old and backup.read_bytes() == newer, newer_sha256=sha(newer))
        (base/'release-1').touch()
        pid2 = wait_marker(2)
        check('same ES resumed record publication', pid1 == pid2)
        check('newer live and last-good bytes survive stale ES snapshot', config.read_bytes() == newer and backup.read_bytes() == newer,
              live_sha256=sha(config.read_bytes()), record_sha256=sha(backup.read_bytes()))
        check('live and record remain private', config.stat().st_mode & 0o777 == 0o600 and backup.stat().st_mode & 0o777 == 0o600)
        (base/'release-2').touch()
    finally:
        (base/'release-1').touch(); (base/'release-2').touch()
        run('systemctl', 'stop', 'essway')
        dropin.unlink(missing_ok=True)
        for path, value in originals.items():
            if value is None: path.unlink(missing_ok=True)
            else: path.write_bytes(value[0]); path.chmod(value[1])
        check('owned settings restored exactly', all((not path.exists()) if value is None else
              (path.read_bytes() == value[0] and path.stat().st_mode & 0o777 == value[1])
              for path, value in originals.items()))
        run('systemctl', 'daemon-reload'); run('systemctl', 'start', 'essway')
        for path, digest in expected.items():
            actual = sha(Path(path).read_bytes())
            check('unchanged installed bytes ' + path, actual == digest, actual_sha256=actual, expected_sha256=digest)

try:
    main()
except BaseException as exc:
    rows.append({'name': 'exception', 'pass': False, 'type': type(exc).__name__, 'message': str(exc)})
    raise
finally:
    (base/'result.json').write_text(json.dumps({'pass': all(r['pass'] for r in rows), 'checks': rows}, indent=2)+'\n')
