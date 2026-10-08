#!/usr/bin/env python3
"""Finite synthetic host proof of pinned old cloud helper guard/lock behavior.

Not a device alignment tool, ES runtime proof, or systemd simulation. Paths
derive from public product constants; all payloads and credentials are invented.
"""
import argparse
import fcntl
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import types

REF = '43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa'
SOURCES = 'projects/ROCKNIX/packages/network/rclone/sources/'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(path):
    return {str(p.relative_to(path)): digest(p) for p in sorted(path.rglob('*')) if p.is_file()}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--fixture-tool', type=Path, required=True)
    parser.add_argument('--rclone', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cases', help='Comma-separated exact cases for a focused retry')
    args = parser.parse_args()
    args.source_root = args.source_root.resolve(strict=True)
    args.fixture_tool = args.fixture_tool.resolve(strict=True)
    args.rclone = str(args.rclone.resolve(strict=True))
    args.output = args.output.resolve()
    args.ref = REF
    args.output.mkdir(parents=True, exist_ok=False)
    loader = importlib.machinery.SourceFileLoader('old_layout_fixture', str(args.fixture_tool))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    fixture = importlib.util.module_from_spec(spec)
    loader.exec_module(fixture)
    fixture.ROOT = args.source_root
    require = fixture.require
    # A local alias needs no network. Enforce that at the sandbox boundary.
    def isolated_run(cmd, *pos, **kw):
        if isinstance(cmd, list) and cmd[0] == 'bwrap':
            cmd = [cmd[0], '--unshare-net', *cmd[1:]]
        return subprocess.run(cmd, *pos, **kw)
    fixture.subprocess = types.SimpleNamespace(run=isolated_run, PIPE=subprocess.PIPE,
                                               STDOUT=subprocess.STDOUT)
    source = subprocess.check_output(['git', '-C', str(args.source_root), 'show',
                                      REF + ':' + SOURCES + 'cloud_migrate_layout'], text=True)
    current = re.search(r'^NEW_SAVES="([^"]+)"$', source, re.M).group(1)
    historical = re.findall(r'"([^"]+)"', re.search(
        r'^SUPERSEDED_DEFAULT_SAVES=\(([^\n]+)\)$', source, re.M).group(1))
    legacy, previous = historical
    current_root, previous_root = current.rsplit('/', 1)[0], previous.rsplit('/', 1)[0]
    results = []
    source_hashes = {}

    def call(f, script, *argv, rc=0):
        r = f.run(script, *argv)
        require(r.returncode == rc, f'{script} {argv}: rc={r.returncode}, expected {rc}: {r.stdout[-700:]}')
        return r.stdout

    def seed(f):
        fixture.put(f.path/'storage/roms/gb/QA_LOCAL.srm', 'invented local progress\n')
        fixture.put(f.path/'storage/.cache/cloud_sync/replaced/QA/QA_RECOVERY.srm', 'invented recovery\n')
        fixture.put(f.path/'storage/.config/system/configs/system.cfg',
                    'system.hostname=QA\ncloudsaves.startup=0\ncloudsaves.gameexit=0\n')
        f.file('/QA_SENTINEL/remote.bin', 'invented remote sentinel\n')

    def protected(f):
        return {'local': snapshot(f.path/'storage/roms'),
                'recovery': snapshot(f.path/'storage/.cache/cloud_sync/replaced'),
                'credential': digest(f.path/'storage/.config/rclone/rclone.conf'),
                'system_config': digest(f.path/'storage/.config/system/configs/system.cfg'),
                'remote': snapshot(f.path/'cloud')}

    def lease_probe(f, held=True):
        call(f, 'lease-probe', 'held' if held else 'free')

    def needs_step(f, expected):
        before = (f.path/'ctl/argv').read_text()
        call(f, 'cloud_migrate_layout', '--needs-step', rc=expected)
        require((f.path/'ctl/argv').read_text() == before, '--needs-step started rclone')

    def case(name, setup, work):
        if args.cases and name not in args.cases.split(','):
            return
        f = fixture.Fixture(args.output/name, args)
        seed(f)
        setup(f)
        for script, body in {
            'startup-witness': 'printf "%s\\n" isolated-fixture-ready\nrclone version\nrclone cat qa:/QA_SENTINEL/remote.bin\n',
            'lease-probe': ('stat -c "lock-inode=%d:%i" /var/run/cloud_sync.lock\n'
                            'if flock -n /var/run/cloud_sync.lock -c true; then\n'
                            ' [ "$1" = free ] || exit 41; echo lease-free\n'
                            'else\n [ "$1" = held ] || exit 42; echo lease-held\nfi\n'),
        }.items():
            fixture.put(f.path/'repo'/script, body)
        inputs = snapshot(f.path/'repo')
        source_hashes.update({k: v for k, v in inputs.items() if k.startswith('cloud_')})
        before = protected(f)
        fd = None
        try:
            started = call(f, 'startup-witness')
            require(started.startswith('isolated-fixture-ready\nrclone v1.75.1\n')
                    and 'invented remote sentinel\n' in started, 'real-rclone startup witness missing')
            lock = f.path/'run/cloud_sync.lock'
            fd = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            st = os.fstat(fd)
            write_json(f.path/'lease.json', {'holder_pid': os.getpid(),
                       'host_inode': f'{st.st_dev}:{st.st_ino}', 'mechanism': 'fcntl.flock LOCK_EX|LOCK_NB',
                       'sandbox_path': '/var/run/cloud_sync.lock', 'note': 'same bind-mounted inode; independently probed before and after helper'})
            lease_probe(f)
            work(f)
            lease_probe(f)
            require(protected(f) == before, 'helper changed synthetic payload, recovery, credentials, or auto0')
            require(snapshot(f.path/'repo') == inputs, 'pinned executable inputs changed')
            # Exact allowed reads, including real alias-backend feature query.
            calls = (f.path/'ctl/argv').read_text().splitlines()
            for cmd in calls:
                require(cmd.startswith(('version', 'cat ', 'lsd ', 'lsf ', 'listremotes',
                                        'backend features ', 'config file', 'config dump')),
                        'unexpected rclone operation: ' + cmd)
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
            fd = None
            lease_probe(f, False)
            results.append({'case': name, 'result': 'PASS'})
            print('PASS', name, flush=True)
        except Exception as error:
            results.append({'case': name, 'result': 'FAIL', 'error': str(error)})
            print('FAIL', name, str(error), flush=True)
        finally:
            if fd is not None:
                os.close(fd)
            write_json(f.path/'final-state.json', {'protected_before': before,
                       'protected_after': protected(f), 'pointers': f.pointers(),
                       'source_sha256': inputs})
            write_json(f.path/'fixture-shims.json', {p.name: p.read_text() for p in (f.path/'shim').iterdir()})
            retired = []
            for part in ('repo', 'shim', 'storage', 'cloud', 'run', 'log'):
                path = f.path/part
                retired.append({'directory': part, 'files': sum(p.is_file() for p in path.rglob('*'))})
                shutil.rmtree(path)
            write_json(f.path/'retired-fixtures.json', retired)

    def setup_join(f, guard=''):
        f.conf(legacy, legacy+'/backup', legacy+'/Content', guard)
        f.file(previous+'/gb/QA_REMOTE.srm', 'invented previous-default save\n')

    def setup_follow(f, guard=''):
        f.conf(previous, previous_root+'/Backups', previous_root+'/Content', guard)
        f.directory(previous)
        f.file(current+'/gb/QA_REMOTE.srm', 'invented current-default save\n')
        f.file(current_root+'/.layout', 'layout=2\n')

    def pointer_action(f, mode, target, guarded=False):
        initial = f.pointers()
        needs_step(f, 1 if guarded else 0)
        call(f, 'cloud_migrate_layout', mode, rc=3 if guarded else 0)
        if guarded:
            require(f.pointers() == initial, 'matching guard did not preserve pointer configuration')
            needs_step(f, 1)
        else:
            require(f.pointers()['SAVES_REMOTE'] == target and target != initial['SAVES_REMOTE'],
                    'unguarded helper did not exercise pointer mutation')
        write_json(f.path/'pointer-diff.json', {k: {'before': initial.get(k), 'after': v}
                    for k, v in f.pointers().items() if initial.get(k) != v})

    case('unguarded-join-under-lease', setup_join,
         lambda f: pointer_action(f, '--join', previous))
    case('unguarded-follow-under-lease', setup_follow,
         lambda f: pointer_action(f, '--follow', current))
    case('matching-guard-join', lambda f: setup_join(f, legacy),
         lambda f: pointer_action(f, '--join', legacy, True))
    case('matching-guard-follow', lambda f: setup_follow(f, previous),
         lambda f: pointer_action(f, '--follow', previous, True))
    case('mismatched-guard-does-not-stop-follow', lambda f: setup_follow(f, '/QA_DIFFERENT/Saves'),
         lambda f: pointer_action(f, '--follow', current))

    def setup_settle(f):
        f.conf(previous, previous_root+'/Backups', previous_root+'/Content', previous)

    case('matching-guard-settle', setup_settle,
         lambda f: pointer_action(f, '--settle', previous, True))

    def guarded_scan(f):
        initial = f.pointers()
        needs_step(f, 1)
        call(f, 'cloud_scan', '--folder')
        require(f.pointers() == initial, 'folder scan changed guarded pointers')
        state = (f.path/'storage/.cache/cloud_sync/scan/state').read_text()
        require('STATE=kept\n' in state, 'guarded folder scan did not classify kept')
        (f.path/'scan-state.txt').write_text(state)
        needs_step(f, 1)
    case('matching-guard-folder-scan', lambda f: setup_follow(f, previous), guarded_scan)

    def current_guard_setup(f):
        f.conf(current, current_root+'/Backups', current_root+'/Content', current)
        f.file(previous+'/gb/QA_REMOTE.srm', 'invented previous-default save\n')

    def current_guard_limit(f):
        before = f.pointers()
        needs_step(f, 1)
        call(f, 'cloud_migrate_layout', '--join')
        require(f.pointers()['SAVES_REMOTE'] == previous, 'current-default join boundary not exercised')
        write_json(f.path/'pointer-diff.json', {k: {'before': before.get(k), 'after': v}
                    for k, v in f.pointers().items() if before.get(k) != v})
    case('current-default-keep-is-not-universal', current_guard_setup, current_guard_limit)

    def setup_transfer(f):
        setup_follow(f, previous)
        f.file(previous+'/gb/QA_SOURCE.srm', 'invented source save\n')
        f.file(previous_root+'/Content/ROMs/gb/QA_GAME.gb', 'invented ROM\n')
        fixture.put(f.path/'storage/roms/gb/QA_GAME.gb', 'invented local ROM\n')
        fixture.put(f.path/'storage/.config/emulationstation/es_systems.cfg', '<path>/storage/roms/gb</path>\n')

    def transfer_refusal(f, script, argv):
        initial = f.pointers()
        before_calls = (f.path/'ctl/argv').read_text()
        started = time.monotonic()
        output = call(f, script, *argv, rc=75)
        elapsed = time.monotonic()-started
        require(elapsed < 6, 'lock refusal was not bounded')
        require('another cloud sync' in output.lower(), 'rc75 lacked lock refusal witness')
        require(f.pointers() == initial, 'blocked writer changed pointer configuration')
        after_calls = (f.path/'ctl/argv').read_text()
        require(after_calls.startswith(before_calls), 'rclone operation log changed underneath control')
        discovery = after_calls[len(before_calls):].splitlines()
        # The old content scripts discover the selected library before taking
        # the transfer lock. This lock prevents transfers, not those reads.
        if script.startswith('cloud_content_'):
            require(all(c == 'listremotes' or c.startswith('lsf --dirs-only ') for c in discovery),
                    'blocked content writer reached an operation beyond discovery: '+str(discovery))
        else:
            require(not discovery, 'blocked saves/apply writer reached rclone')
        write_json(f.path/'lock-refusal.json', {'rc': 75, 'elapsed_seconds': elapsed,
                    'discovery_before_lock_refusal': discovery, 'transfer_operations': 0})

    for script, argv in [
        ('cloud_backup', ('--yes', '--saves-only', '--automatic')),
        ('cloud_restore', ('--yes', '--saves-only', '--automatic')),
        ('cloud_content_backup', ('--all',)),
        ('cloud_content_restore', ('--all',)),
        ('cloud_migrate_layout', ('--apply',)),
    ]:
        case('lease-refuses-'+script, setup_transfer,
             lambda f, script=script, argv=argv: transfer_refusal(f, script, argv))
    if args.cases:
        require(set(args.cases.split(',')) == {r['case'] for r in results}, 'unknown selected case')
    summary = {'source_ref': REF, 'source_root': str(args.source_root),
               'public_default_paths': {'current': current, 'historical': historical},
               'results': results, 'passed': sum(r['result'] == 'PASS' for r in results),
               'failed': sum(r['result'] == 'FAIL' for r in results),
               'fixture_source_sha256': source_hashes, 'fixture_override': ['cloud_device_id'],
               'rclone_sha256': digest(Path(args.rclone)),
               'harness_sha256': digest(Path(__file__)),
               'fixture_tool_sha256': digest(args.fixture_tool),
               'scope': 'Synthetic host old-helper behavior only. ES and systemd runtime, transaction, restart, rollback and device acceptance are not proved.'}
    write_json(args.output/'summary.json', summary)
    print(f"old-helper-proof: {summary['passed']} PASS, {summary['failed']} FAIL", flush=True)
    return bool(summary['failed'])


if __name__ == '__main__':
    sys.exit(main())
