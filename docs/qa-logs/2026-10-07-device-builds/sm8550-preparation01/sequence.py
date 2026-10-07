"""Supervise watched stages; never advance without artifact and exit acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
import time

owner = Path(__file__).resolve().parent
primary = Path('/workspace/repos/rocknix')
tree = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01')
build = Path('/workspace/tmp/pixelelated-m7-sm8550-build-01')
accept = Path('/workspace/tmp/pixelelated-m7-sm8550-acceptance-01')
waiter = Path('/workspace/tmp/pixelelated-m7-sm8550-wait-h700-01')
tracker_errors = []


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, data):
    with path.open('x') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')


def read(path):
    return json.loads(path.read_text())


def state(phase, **details):
    data = dict(utc=now(), pid=os.getpid(), phase=phase, **details)
    temporary = owner / 'state.new'
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(owner / 'state.json')
    print(json.dumps(data), flush=True)


def seal(folder, names):
    write(folder / 'seal.json', {str(folder / n): hashlib.sha256((folder / n).read_bytes()).hexdigest() for n in names})


def submit(folder, cwd):
    subprocess.run(['python3', '-I', str(owner / 'watch-build-submit.py'), '--owner', str(folder),
                    '--', '--', 'python3', '-I', str(folder / 'run.py')], cwd=cwd, check=True)


def exited(folder):
    if not (folder / 'launcher-result.json').is_file():
        return False
    run = Path((folder / 'run.path').read_text().strip())
    pids = [read(folder / 'launcher-pid.json')['pid']]
    pids += [int((run / n).read_text()) for n in ['build.pid', 'watcher.pid', 'command.pid']]
    return all(not Path('/proc', str(pid)).exists() for pid in pids)


def consume(folder, phase):
    while not exited(folder):
        state(phase, active_owner=str(folder))
        time.sleep(30)
    if not (folder / 'owner-verification.json').exists():
        subprocess.run(['python3', '-I', str(owner / 'verify-owner.py'), str(folder)], check=True)
    receipt = read(folder / 'owner-verification.json')
    assert receipt['result'] == 'PASS', (folder, receipt['channels'])


def actual_container():
    ids = subprocess.check_output(['docker', 'ps', '-q', '--no-trunc'], text=True).split()
    containers = json.loads(subprocess.check_output(['docker', 'inspect', *ids], text=True)) if ids else []
    matches = [c for c in containers if any(m['Source'] == str(tree) for m in c['Mounts'])]
    if not matches:
        return False
    assert len(matches) == 1
    c = matches[0]
    inputs = read(build / 'inputs.json')
    assert c['Image'] == inputs['container_image_id'] and c['State']['Running']
    mounts = {m['Source']: m['Destination'] for m in c['Mounts']}
    for source, destination in [(str(tree), str(tree)), (str(build), str(build)),
                                ('/workspace/repos/rocknix/.git', '/workspace/repos/rocknix/.git'),
                                (inputs['source_cache'], str(tree / 'sources'))]:
        assert mounts.get(source) == destination
    write(build / 'runtime-start.json', dict(utc=now(), state='running',
          containers=[dict(id=c['Id'], image=c['Image'], state=c['State']['Status'],
                           host_pid=c['State']['Pid'], mounts=[dict(source=m['Source'], destination=m['Destination'], rw=m['RW']) for m in c['Mounts']])]))
    return True


def update_tracker(complete):
    # Preserve the standing ordered plan and replace only its current device row.
    try:
        inputs = read(build / 'inputs.json')
        status = 'accepted' if complete else 'building'
        text = ('H700 firmware artifact acceptance passed, including both DDR variants, '
                'raw/update equality and actual ARM handoff. SM8550 is ' + status +
                ' from frozen `' + inputs['distribution_commit'] + '` after capacity and guarded host preflight. '
                'Owners: `/workspace/tmp/pixelelated-m7-sm8550-build-01` and '
                '`/workspace/tmp/pixelelated-m7-sm8550-acceptance-01`. '
                'The sequential controller uses standard watchers and verified exits. '
                'Physical actions, source/licence staging and release publication remain separate; no RC claim.')
        base = 'repos/pixelelated/distribution/'
        for endpoint, field in [('issues/492', 'body'), ('milestones/7', 'description')]:
            current = json.loads(subprocess.check_output(['gh', 'api', base + endpoint], text=True))
            body = current[field]
            if field == 'body':
                marker = '## Earlier device build record'
                assert marker in body
                body = '## Current firmware work — ' + now() + '\n\n' + text + '\n\n' + marker + body.split(marker, 1)[1]
            else:
                assert current['title'].startswith('M7:')
                lines = body.splitlines()
                replacement = '4. **#492 CURRENT: SM8550 ' + status + '.** ' + text
                found = [i for i, line in enumerate(lines) if line.startswith('4. **#492')]
                assert len(found) == 1
                lines[found[0]] = replacement
                found = [i for i, line in enumerate(lines) if line.startswith('3. **#492 CURRENT: H700') or line.startswith('3. **#492 H700 firmware artifact acceptance COMPLETE.')]
                assert len(found) == 1
                lines[found[0]] = '3. **#492 H700 firmware artifact acceptance COMPLETE.** Both DDR variants, raw/update payloads, installed identity, ARM handoff and independent custody verified; physical boot remains separate. Cleanup #493/#494 and its #498 limitation remain recorded.'
                for i, line in enumerate(lines):
                    if line.startswith('2. **#492 H700 arm'):
                        lines[i] = '2. **#492 H700 arm and #497 actual handoff proof COMPLETE.** Accepted compatibility output is present byte-for-byte in the verified firmware. The source repair and failed owners remain preserved; issue reconciliation follows the retained artifacts.'
                    if line.startswith('| **M7.P5 —'):
                        lines[i] = '| **M7.P5 — Device builds and release staging** | **CURRENT: H700 firmware accepted; SM8550 ' + status + '**. Then named physical and publication gates. | Each device artifact verified before its authorized smoke/migration actions; source/licence/public docs and manifest-bound assets before release publication. |'
                lines[0] = '## Current priority — SM8550 ' + status + ', then named device and release gates'
                body = '\n'.join(lines) + '\n'
            label = endpoint.replace('/', '-') + ('-complete' if complete else '-started')
            request = owner / (label + '.json')
            write(request, {field: body})
            subprocess.run(['gh', 'api', '--method', 'PATCH', base + endpoint, '--input', str(request)], check=True, stdout=subprocess.DEVNULL)
            after = json.loads(subprocess.check_output(['gh', 'api', base + endpoint], text=True))
            assert after[field] == body
            write(owner / (label + '-readback.json'), after)
    except Exception as error:
        tracker_errors.append(repr(error))
        state('tracker-update-needs-review', error=repr(error))


result = dict(result='FAILED')
try:
    for name, expected in read(owner / 'seal.json').items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, name
    write(owner / 'controller-start.json', dict(utc=now(), pid=os.getpid(), start_ticks=Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19]))
    submit(waiter, primary)
    consume(waiter, 'waiting-for-H700-artifact-acceptance')
    state('preparing-SM8550')
    subprocess.run(['python3', '-I', str(owner / 'prepare.py')], check=True)
    # No watched stage is alive here. The installed helper independently refuses
    # any other active compiler, watcher or guest before touching fixed /swap.img.
    with (owner / 'host-preflight.log').open('x') as out:
        preflight = subprocess.run([str(tree / 'tools/build-preflight'), '--reclaim-swap'], cwd=tree, stdout=out, stderr=subprocess.STDOUT)
    write(owner / 'host-preflight-result.json', dict(utc=now(), returncode=preflight.returncode))
    assert preflight.returncode == 0, 'Host preflight refused; prepared build has not started'
    accept.mkdir(mode=0o700)
    (accept / 'artifacts').mkdir()
    for src, dst in [('accept-run.py', 'run.py'), ('verify-firmware.py', 'verify-firmware.py'), ('verify-owner.py', 'verify-owner.py')]:
        (accept / dst).write_bytes((owner / src).read_bytes())
    seal(accept, ['run.py', 'verify-firmware.py', 'verify-owner.py'])
    submit(build, tree)
    state('SM8550-builder-starting', active_owner=str(build))
    for attempt in range(60):
        if actual_container():
            break
        assert not (build / 'launcher-result.json').exists(), 'Builder exited before container startup; inspect retained build owner'
        time.sleep(2)
    else:
        raise RuntimeError('Container startup not verified within two minutes; build owner retained')
    submit(accept, primary)
    update_tracker(False)
    consume(accept, 'SM8550-build-and-artifact-verification')
    assert read(accept / 'artifacts/acceptance.json')['result'] == 'PASS'
    update_tracker(True)
    result = dict(result='PASS' if not tracker_errors else 'ARTIFACTS_PASS_TRACKER_PENDING',
                  acceptance=str(accept / 'artifacts/acceptance.json'),
                  scope='H700 then SM8550 build artifacts accepted; physical testing and release remain separate')
except Exception as error:
    result['error'] = repr(error)
    raise
finally:
    result.update(utc=now(), tracker_errors=tracker_errors)
    write(owner / 'controller-result.json', result)
    state('complete' if result['result'] == 'PASS' else 'needs-review', result=result)
