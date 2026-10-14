#!/usr/bin/python3
"""UNRUN: serial-coordinated #581 remaining callers, disposable no-NIC VM only.

This wrapper executes the sealed v4 fixture as a subprocess, never imports it.
It does not generate inputs, inject keys, capture frames, or change product code.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tarfile
import time

HERE = Path(__file__).resolve().parent
INPUT = Path('/tmp/pix-input/dolphin')
OUTPUT = Path('/tmp/pix-output')
V4 = INPUT / 'v4'
CALLER = INPUT / 'caller'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    pending = path.with_name(path.name + '.pending')
    pending.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    pending.replace(path)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def identity(pid):
    try:
        fields = Path('/proc', str(pid), 'stat').read_text().rsplit(')', 1)[1].split()
        return {'pid':int(pid), 'start_ticks':fields[19], 'state':fields[0]}
    except FileNotFoundError:
        return None


def alive(record):
    current = identity(record['pid']) if record else None
    return bool(current and current['start_ticks'] == record['start_ticks'] and current['state'] != 'Z')


def selected_cases(value):
    baseline = read(HERE / 'resume-baseline.json')
    require(value['run_id'] not in baseline['consumed_run_ids'], 'consumed run ID; allocate a fresh owner')
    require('matrix' not in value, 'matrix fallback is retired here; provide explicit case_ids')
    ids = value.get('case_ids')
    require(isinstance(ids, list) and 1 <= len(ids) <= 2 and all(isinstance(i, str) for i in ids),
            'case_ids must be an explicit nonempty list of at most two IDs')
    require(len(set(ids)) == len(ids), 'duplicate case IDs are not allowed')
    require(not set(ids) & set(baseline['completed_case_ids']), 'selection includes an already completed caller')
    require(set(ids) <= set(baseline['selection_scope']), 'selection includes an unknown/out-of-scope case')
    catalog = read(HERE / 'cases.json') + read(HERE / 'missing-fr640.json')
    by_id = {case['id']: case for case in catalog}
    require(len(by_id) == len(catalog), 'ambiguous source catalog')
    require(set(baseline['selection_scope']) | set(baseline['completed_case_ids']) == set(by_id),
            'resume baseline does not cover the source catalog')
    return [by_id[case_id] for case_id in ids]


def reject_completed_outputs(value, output_root=OUTPUT):
    # Conservative refusal of known completed receipts; never silently skip a
    # requested case or treat a failed whole batch as permission to replay it.
    require(output_root.resolve() == output_root and output_root.is_dir(), 'missing/unsafe receipt root')
    for previous in sorted(output_root.glob('dolphin-remaining-*')):
        require(previous.is_dir() and not previous.is_symlink(), 'unsafe prior output root')
        require(re.fullmatch(r'dolphin-remaining-[A-Za-z0-9_-]{1,32}', previous.name), 'malformed prior output root')
        if previous.name == 'dolphin-remaining-' + value['run_id']:
            continue  # this fresh batch's status/advance calls remain usable
        for case in selected_cases(value):
            directory = previous / case['id']
            require(not directory.is_symlink() and (not directory.exists() or directory.is_dir()), 'unsafe prior case directory')
            result = directory / 'result.json'
            require(not result.is_symlink(), 'unsafe prior completion receipt')
            if result.exists():
                require(result.is_file(), 'unreadable prior completion receipt')
                receipt = read(result)
                require(isinstance(receipt, dict) and receipt.get('status') == 'PASS',
                        'unsupported/malformed prior completion receipt; review originals')
                raise RuntimeError('case has a completed receipt; exclude it explicitly: ' + case['id'] + ' at ' + str(result))


def config(path=INPUT / 'allocation.json'):
    value = read(path)
    require(re.fullmatch('[A-Za-z0-9_-]{1,32}', value['run_id']), 'invalid run_id')
    require(re.fullmatch('[0-9a-f]{64}', value['es_sha256']), 'exact ES SHA256 required')
    require(re.fullmatch('[0-9a-f]{40}', value['es_source']), 'exact ES source required')
    require(value['renderer'] in ('Vulkan', 'OGL'), 'unsupported recipe renderer')
    require(value['panel'] == [640, 480], 'this remaining-frame batch requires 640x480')
    selected_cases(value)
    return value


def root_for(value):
    return OUTPUT / ('dolphin-remaining-' + value['run_id'])


def preflight(value):
    require(os.geteuid() == 0, 'disposable guest root required')
    require(sorted(name for _, name in socket.if_nameindex()) == ['lo'], 'guest must have only lo')
    require(HERE == INPUT / 'batch', 'stage this packet at /tmp/pix-input/dolphin/batch')
    for path in (INPUT, HERE, V4, CALLER, INPUT / 'source', INPUT / 'product',
                 INPUT / 'defaults/dolphin-emu', INPUT / 'defaults/receipt.json', INPUT / 'allocation.json'):
        require(path.resolve() == path and path.exists(), 'missing or symlinked staging input: ' + str(path))
        require(os.statvfs(path).f_flag & os.ST_RDONLY, 'staging input is not read-only: ' + str(path))
    require(OUTPUT.resolve() == OUTPUT and OUTPUT.is_dir(), 'missing real /tmp/pix-output')
    require(not os.statvfs(OUTPUT).f_flag & os.ST_RDONLY, 'output is read-only')
    binding = read(HERE / 'binding.json')
    for name, expected in binding['v4_files'].items():
        require(sha(V4 / name) == expected, 'sealed v4 mismatch: ' + name)
    for name, expected in binding['caller_files'].items():
        require(sha(CALLER / name) == expected, 'candidate caller composition mismatch: ' + name)
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(Path(name).name == name and sha(HERE / name) == digest, 'batch packet mismatch: ' + name)
    for name, expected in binding['distribution_files'].items():
        require(sha(INPUT / 'source' / name) == expected, 'source mismatch: ' + name)
    require(sha(INPUT / 'defaults/receipt.json') == binding['defaults_receipt_sha256'], 'defaults receipt mismatch')
    require(sha('/usr/bin/emulationstation') == value['es_sha256'], 'ES binary mismatch')
    # v4 performs complete defaults/recipe/resource/utility/socket checks before
    # stopping essway for each case. Never resolve an applet's invocation path.
    for name in ('bash', 'python3', 'systemctl', 'mv'):
        require(os.access('/usr/bin/' + name, os.X_OK), 'missing guest utility: ' + name)
    require(stat.S_ISSOCK(Path(value['wayland_socket']).stat().st_mode), 'missing Wayland socket')
    reject_completed_outputs(value)


def signal_stage(root, case, phase, serial, **details):
    event = dict(case=case, phase=phase, token=f'{serial:02d}-{phase}', **details)
    write(root / 'events' / (event['token'] + '.json'), event)
    write(root / 'serial-ready.json', event)
    return event


def wait_until(root, predicate, process=None, timeout=90):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        require(not (root / 'abort.json').exists(), 'host requested abort')
        if process is not None:
            require(process.poll() is None, 'session exited before host stage completed')
        if predicate():
            return
        time.sleep(0.2)
    raise RuntimeError('bounded stage timeout')


def gate(root, event, process=None, timeout=90):
    path = root / 'advances' / (event['token'] + '.json')
    wait_until(root, path.is_file, process, timeout)
    value = read(path)
    require(value['token'] == event['token'], 'advance token mismatch')


def archive(owner, destination):
    # No synthetic storage or symlink dereference. Original receipts are copied
    # byte-for-byte; the live owner is retained until coordinator retirement.
    with tarfile.open(destination, 'w', dereference=False) as output:
        for path in sorted(owner.rglob('*')):
            relative = path.relative_to(owner)
            if relative.parts[:2] == ('active', 'storage'):
                continue
            if path.is_file() and not path.is_symlink():
                output.add(path, arcname=str(relative), recursive=False)


def cleanup(process, owner):
    actions = []
    if process.poll() is None:
        # Normal stop first; immutable wrapper owns service restoration.
        if (owner / 'active').is_dir():
            (owner / 'active/stop').touch(exist_ok=True)
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            process.send_signal(signal.SIGTERM)
            actions.append('TERM session wrapper; immutable trap retires namespace and restores frontend')
            try:
                process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                # Only this owner, validated PID/start, own process group.
                recorded = owner / 'active/runner-pid.json'
                if recorded.is_file() and alive(read(recorded)):
                    os.killpg(read(recorded)['pid'], signal.SIGKILL)
                    actions.append('KILL recorded unshare group')
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=5)
                actions.append('KILL session group; frontend recovery requires coordinator')
    return actions


def entry_evidence(active, destination):
    # Exact bounded snapshots from this newly generated synthetic owner only.
    # Marker presence is not a claim that the library has rendered.
    destination.mkdir()
    rows = {}
    names = ('ready.json', 'case.json', 'es-pid.json', 'es.stdout', 'es.stderr',
             'logs/es_log.txt', 'storage/.config/emulationstation/es_settings.cfg',
             'storage/.config/emulationstation/es_systems.cfg')
    for index, name in enumerate(names):
        path = active / name
        require(not path.is_symlink(), 'symlinked entry evidence path')
        if not path.exists():
            rows[name] = {'present': False}
            continue
        require(path.resolve() == path and path.is_file(), 'unsafe entry evidence path')
        with path.open('rb') as stream:
            data = stream.read(65537)
        truncated = len(data) > 65536
        data = data[:65536]
        snapshot = str(index) + '-' + path.name
        (destination / snapshot).write_bytes(data)
        rows[name] = {'present': True, 'snapshot': snapshot, 'bytes': len(data),
                      'truncated': truncated, 'sha256': hashlib.sha256(data).hexdigest()}
    value = {'ready_marker': read(active / 'ready.json'), 'files': rows,
             'meaning': 'ES startup marker only. Review actual header, selected synthetic game and footer before explicit launch. No automatic key or deadline extension.',
             'source': 'bound main.cpp sets ready after goToStart and before its main render loop',
             'logs': 'unchanged native ES logging level; startup warnings alone do not prove a missing view'}
    write(destination / 'evidence.json', value)
    return value


def run_case(root, value, case, index):
    owner = Path('/tmp/pix581-installed-' + value['run_id'] + '-' + case['id'])
    require(not os.path.lexists(owner), 'case owner already exists; no replay')
    case_output = root / case['id']
    case_output.mkdir()
    command = ['/usr/bin/bash', str(CALLER / 'guest-session.sh'), str(INPUT / 'source'), str(owner),
               case['system'], case['scenario'], case['language'], value['es_sha256'], value['es_source'],
               value['wayland_socket'], value['renderer'], str(INPUT / 'product'),
               str(INPUT / 'defaults/dolphin-emu'), str(INPUT / 'defaults/receipt.json')]
    write(case_output / 'command.json', command)
    with (case_output / 'session.stdout').open('wb') as stdout, (case_output / 'session.stderr').open('wb') as stderr:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, start_new_session=True)
        write(case_output / 'session-pid.json', identity(process.pid))
        error = None
        actions = []
        try:
            active = owner / 'active'
            wait_until(root, (active / 'ready.json').is_file, process, 110)
            mounted = read(active / 'mounted.json')
            require(mounted['interfaces'] == ['lo'], 'fixture namespace has a NIC')
            shutil.copyfile(active / 'mounted.json', case_output / 'mounted.json')
            startup = entry_evidence(active, case_output / 'entry-evidence')
            event = signal_stage(root, case, 'entry', index * 4, owner=str(owner),
                                 mounted_receipt=str(case_output / 'mounted.json'), startup_evidence=startup)
            gate(root, event, process, 45)  # host captures/reviews entry and presses x ONCE
            wait_until(root, (active / 'caller.json').is_file, process, 50)
            caller = read(active / 'caller.json')
            shutil.copyfile(active / 'caller.json', case_output / 'caller.json')
            require(caller['status'] == 'PASS', 'sealed v4 caller assertions failed')
            if case['scenario'] not in ('fresh', 'known-link'):
                wait_until(root, (active / 'native-consumed.json').is_file, process, 10)
                shutil.copyfile(active / 'visible-error.txt', case_output / 'visible-error.txt')
                event = signal_stage(root, case, 'error', index * 4 + 1, caller=caller)
                gate(root, event, process, 45)  # actual native frame; x ONCE dismisses
            event = signal_stage(root, case, 'returned', index * 4 + 2, caller=caller)
            gate(root, event, process, 30)  # host reviews return before normal stop
            (active / 'stop').touch(exist_ok=False)
            require(process.wait(timeout=40) == 0, 'original guest-session exit nonzero')
            originals = {'session_process':process.returncode,
                         'session':int((owner / 'session.exit').read_text()),
                         'frontend_restore':int((owner / 'frontend-restore.exit').read_text()),
                         'unshare':read(active / 'runner-exit.json')['original_unshare_exit'],
                         'es':read(active / 'es-exit.json')['original_exit'],
                         'runemu':read(active / 'runemu-exit.json')['original_exit']}
            require(all(originals[key] == 0 for key in ('session_process','session','frontend_restore','unshare','es')),
                    'original supervisor/frontend exit nonzero')
            require(originals['runemu'] == (0 if case['scenario'] in ('fresh', 'known-link') else 250), 'runemu exit mismatch')
            require(read(active / 'boundary.json')['status'] == 'PASS', 'native boundary failed')
            require(not alive(read(active / 'runner-pid.json')), 'owned unshare still alive')
            ns = mounted['namespaces']['pid']
            remaining = []
            for path in Path('/proc').glob('[0-9]*/ns/pid'):
                try:
                    if os.readlink(path) == ns:
                        remaining.append(int(path.parts[2]))
                except FileNotFoundError:
                    pass
            require(not remaining, 'owned namespace processes remain')
            frontend = subprocess.run(['/usr/bin/systemctl', 'is-active', '--quiet', 'essway.service'], timeout=10, check=False)
            require(frontend.returncode == 0, 'frontend not active after restoration')
            write(case_output / 'result.json', dict(status='PASS', originals=originals,
                  frontend_active_exit=frontend.returncode, namespace_processes_remaining=remaining,
                  frames='see host advance records; source-staged proof, not shipped-image qualification'))
        except BaseException as exc:
            error = str(exc) or type(exc).__name__
            raise
        finally:
            actions = cleanup(process, owner)
            originals = {}
            for name, relative, key in (
                    ('session', 'session.exit', None), ('frontend_restore', 'frontend-restore.exit', None),
                    ('interrupted_session', 'session-interrupted.exit', None),
                    ('unshare', 'active/runner-exit.json', 'original_unshare_exit'),
                    ('es', 'active/es-exit.json', 'original_exit'),
                    ('runemu', 'active/runemu-exit.json', 'original_exit')):
                path = owner / relative
                try:
                    originals[name] = (read(path)[key] if key else int(path.read_text())) if path.is_file() else None
                except (ValueError, KeyError):
                    originals[name] = 'MALFORMED; original file retained in archive'
            write(case_output / 'session-original-exit.json', {'original_exit':process.returncode,
                  'observed_original_exits':originals, 'cleanup_actions':actions, 'error':error})
            if owner.is_dir():
                archive(owner, case_output / 'owner-receipts.tar')
    event = signal_stage(root, case, 'complete', index * 4 + 3, result=read(case_output / 'result.json'))
    gate(root, event, timeout=120)  # no next case until coordinator consumes originals


def run(root):
    value = config()
    require(root == root_for(value), 'output/config mismatch')
    def terminate(_signum, _frame):
        raise KeyboardInterrupt('batch interrupted')
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    try:
        with os.fdopen(os.open('/tmp/pix581-remaining-batch.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600), 'w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            preflight(value)
            cases = selected_cases(value)
            for index, case in enumerate(cases, 1):
                run_case(root, value, case, index)
        write(root / 'batch-result.json', {'status':'PASS', 'cases':len(cases), 'runtime':'original exits retained; frames require host review'})
        signal_stage(root, None, 'done', 99, result=read(root / 'batch-result.json'))
        return 0
    except BaseException as exc:
        write(root / 'batch-result.json', {'status':'FAIL', 'error':str(exc) or type(exc).__name__})
        signal_stage(root, None, 'failed', 99, result=read(root / 'batch-result.json'))
        return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('start', 'run', 'status', 'advance', 'abort', 'plan'))
    parser.add_argument('--disposable-vm', action='store_true')
    parser.add_argument('--token')
    parser.add_argument('--review')
    parser.add_argument('--allocation', type=Path, help='plan only: read an explicit host allocation JSON')
    parser.add_argument('--receipts-root', type=Path, help='plan only: optional owned public output receipt directory')
    args = parser.parse_args()
    require(args.operation == 'plan' or (args.allocation is None and args.receipts_root is None),
            '--allocation/--receipts-root are supported only for plan')
    if args.operation == 'plan':
        require(args.allocation is not None, 'plan requires --allocation')
        value = config(args.allocation)
        if args.receipts_root is not None:
            require(not os.path.lexists(args.receipts_root / ('dolphin-remaining-' + value['run_id'])), 'run ID already has receipts')
            reject_completed_outputs(value, args.receipts_root)
        print('PIX581_JSON=' + json.dumps({'run_id':value['run_id'], 'case_ids':[c['id'] for c in selected_cases(value)],
              'excluded_completed_ids':read(HERE / 'resume-baseline.json')['completed_case_ids'],
              'prior_output_receipts_checked':args.receipts_root is not None, 'runtime':'UNRUN; selection planning only'}, separators=(',', ':')))
        return 0
    value = config()
    root = root_for(value)
    if args.operation == 'run':
        return run(root)
    if args.operation == 'start':
        require(args.disposable_vm, 'explicit disposable-VM acknowledgement required')
        preflight(value)
        root.mkdir(mode=0o700)  # refuses an existing allocation; never resumes/replays
        (root / 'events').mkdir(); (root / 'advances').mkdir()
        write(root / 'allocation.json', value)
        write(root / 'selection.json', {'case_ids':[c['id'] for c in selected_cases(value)],
              'resume_baseline_sha256':sha(HERE / 'resume-baseline.json'),
              'excluded_completed_ids':read(HERE / 'resume-baseline.json')['completed_case_ids']})
        write(root / 'guest-before.json', {'interfaces':socket.if_nameindex(), 'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()})
        with (root / 'batch.stdout').open('wb') as stdout, (root / 'batch.stderr').open('wb') as stderr:
            process = subprocess.Popen(['/usr/bin/bash', str(HERE / 'batch-session.sh'), str(root)],
                stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, start_new_session=True)
        write(root / 'batch-session-pid.json', identity(process.pid))
        response = {'started':True, 'output':str(root), 'session_pid':process.pid}
    elif args.operation == 'status':
        response = read(root / 'serial-ready.json') if (root / 'serial-ready.json').is_file() else {'phase':'starting'}
        response['batch_session_exit'] = int((root / 'batch-session.exit').read_text()) if (root / 'batch-session.exit').is_file() else None
        record = root / 'batch-session-pid.json'
        response['batch_session_alive'] = alive(read(record)) if record.is_file() else None
    elif args.operation == 'advance':
        event = read(root / 'serial-ready.json')
        require(args.token == event['token'] and event['phase'] in ('entry','error','returned','complete'), 'stale/invalid advance')
        require(args.review and 1 <= len(args.review) <= 1000, 'frame/original-exit review required')
        path = root / 'advances' / (args.token + '.json')
        require(not path.exists(), 'stage already advanced; no replay')
        write(path, {'token':args.token, 'review':args.review})
        response = {'advanced':args.token}
    else:
        write(root / 'abort.json', {'requested':True})
        response = {'abort_requested':True, 'consume_failed_result_and_original_exits':True}
    print('PIX581_JSON=' + json.dumps(response, separators=(',', ':')))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        sys.exit(2)
