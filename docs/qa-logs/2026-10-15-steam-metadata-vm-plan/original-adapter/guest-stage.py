#!/usr/bin/env python3
"""One existing source-chroot case, original result export and guest restoration."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import signal
import stat
import subprocess
import tarfile
import time

INPUT = Path('/tmp/pix-input')
OUTPUT = Path('/tmp/pix-output')
PACKET = INPUT / 'docs/qa-logs/2026-10-14-steam-remaining-source'
SEAL = '79dc1d57d8741b644e99cd8348c4c362fbef3a1c815c48f6fa23b84a6e201c34'
CASES = ('fresh-profile-dot', 'fresh-profile-dot-absent', 'valid-existing-alias',
         'existing-profile-dot', 'self-updated-client', 'partial-before-profile',
         'marker-missing-core', 'metadata-conflict-after-profile', 'unknown-stage-before-profile',
         'download-failure-retry', 'validation-failure-retry', 'publication-failure-retry',
         'metadata-failure-retry', 'interrupt-prepared-retry')
NEGATIVE = set(CASES[5:9])
RETRIES = set(CASES[9:])
SELECTED = ('/storage/.local/share/Steam', '/storage/.steam',
            '/storage/.local/share/fex-emu', '/storage/.config/fex-emu',
            '/storage/.local/share/applications/steam.desktop', '/tmp/.process-kill-data')
MAX_STAGE = 75 * 1024**2
MAX_FAMILY = 1100 * 1024**2


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')


def expired(signum, frame):
    raise TimeoutError('Stage deadline or termination')


def children():
    rows = {}
    for p in Path('/proc').iterdir():
        if not p.name.isdecimal():
            continue
        try:
            fields = (p / 'stat').read_text().rsplit(')', 1)[1].split()
            rows[int(p.name)] = {'pid': int(p.name), 'ppid': int(fields[1]),
                                 'state': fields[0], 'start_ticks': int(fields[19])}
        except (FileNotFoundError, ProcessLookupError):
            continue
    owned = {os.getpid()}
    while True:
        added = {pid for pid, row in rows.items() if row['ppid'] in owned} - owned
        if not added:
            break
        owned |= added
    return [rows[pid] for pid in sorted(owned) if pid != os.getpid()]


def selected_state():
    rows, count, total = {}, 0, 0
    for name in SELECTED:
        root = Path(name)
        paths = [root]
        if root.is_dir() and not root.is_symlink():
            paths += sorted(root.rglob('*'))
        for path in paths:
            count += 1
            assert count <= 4096, 'Unexpected selected real-storage size'
            try:
                s = path.lstat()
            except FileNotFoundError:
                rows[str(path)] = {'absent': True}; continue
            row = {'mode': s.st_mode, 'device': s.st_dev, 'inode': s.st_ino,
                   'uid': s.st_uid, 'gid': s.st_gid, 'size': s.st_size}
            if stat.S_ISLNK(s.st_mode):
                row['link'] = os.readlink(path)
            elif stat.S_ISREG(s.st_mode):
                total += s.st_size
                assert s.st_size <= 8 * 1024**2 and total <= 64 * 1024**2
                row['sha256'] = sha(path)
            else:
                assert stat.S_ISDIR(s.st_mode), 'Unexpected selected real-storage object'
            rows[str(path)] = row
    return rows


def mount_rows():
    def unescape(value):
        return re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1], 8)), value)
    rows = []
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        fields = line.split(); rows.append((unescape(fields[4]), line))
    return rows


def parent_state():
    names = ('mnt', 'pid', 'net', 'ipc', 'uts')
    rows = mount_rows()
    targets = ('/', '/storage', '/usr', '/proc/sys/fs/binfmt_misc', str(INPUT), str(OUTPUT))
    selected = {}
    for target in targets:
        choices = [(p, row) for p, row in rows if target == p or target.startswith(p.rstrip('/') + '/')]
        selected[target] = max(choices, key=lambda x: len(x[0]))[1]
    fields = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
    return {'pid': os.getpid(), 'start_ticks': int(fields[19]),
            'namespaces': {n: os.readlink('/proc/self/ns/' + n) for n in names},
            'selected_mounts': selected, 'selected_storage': selected_state()}


def assert_namespaces_gone(identities):
    for process in Path('/proc').iterdir():
        if not process.name.isdecimal():
            continue
        for name, value in identities.items():
            try:
                observed = os.readlink(process / 'ns' / name)
            except (FileNotFoundError, ProcessLookupError):
                continue
            assert observed != value, 'Private case namespace still used by PID ' + process.name


def exported_files():
    rows = []
    for path in sorted((OUTPUT / 'steam').rglob('*')):
        assert not path.is_symlink(), 'Aliased exported result'
        if path.is_file():
            rows.append({'path': str(path.relative_to(OUTPUT)), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    assert sum(row['bytes'] for row in rows) <= MAX_FAMILY
    return rows


def seal_output():
    rows = exported_files()
    manifest = OUTPUT / 'guest-export-manifest.json'
    pending = OUTPUT / ('guest-export-manifest.pending.' + str(os.getpid()))
    save(pending, rows); os.replace(pending, manifest)
    subprocess.run(['sync'], check=True, timeout=5)
    return rows


def export_case(source, stage):
    excluded = ('rootfs', 'storage', 'tmp', 'qa/payloads')
    rows = []
    total = 0
    for path in sorted(source.rglob('*')):
        name = str(path.relative_to(source))
        if any(name == x or name.startswith(x + '/') for x in excluded):
            continue
        assert not path.is_symlink(), 'Unexpected evidence symlink'
        if path.is_file():
            s = path.stat(); total += s.st_size
            assert s.st_size <= 2 * 1024**2 and total <= 64 * 1024**2
            rows.append({'path': name, 'bytes': s.st_size, 'sha256': sha(path)})
    save(stage / 'archive-members.json', rows)
    archive_path = stage / 'fixture-records.tar.gz'
    with tarfile.open(archive_path, 'x:gz') as archive:
        for row in rows:
            archive.add(source / row['path'], arcname=row['path'], recursive=False)
            assert archive_path.stat().st_size <= MAX_STAGE
    with tarfile.open(archive_path, 'r:gz') as archive:
        assert [m.name for m in archive.getmembers()] == [row['path'] for row in rows]
        for row in rows:
            stream = archive.extractfile(row['path']); digest = hashlib.sha256(); count = 0
            for block in iter(lambda: stream.read(1024**2), b''):
                count += len(block); digest.update(block)
            assert count == row['bytes'] and digest.hexdigest() == row['sha256']
            assert sha(source / row['path']) == row['sha256']
    return {'original_files': len(rows), 'original_bytes': total,
            'archive_sha256': sha(archive_path), 'archive_bytes': archive_path.stat().st_size}


def main():
    p = argparse.ArgumentParser(); group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--case', choices=CASES); group.add_argument('--seal-output', action='store_true')
    a = p.parse_args()
    assert os.geteuid() == 0 and platform.machine() == 'x86_64'
    assert Path('/sys/class/dmi/id/sys_vendor').read_text().strip() == 'QEMU'
    assert sys_flags_safe(), 'Python assertions must remain enabled'
    binding = json.loads((INPUT / 'family.json').read_text())
    assert binding['cases'] == list(CASES) and sha(PACKET / 'SHA256SUMS') == SEAL
    fields = dict(line.split('=', 1) for line in Path('/etc/os-release').read_text().splitlines() if '=' in line)
    assert fields['BUILD_ID'].strip('"') == binding['source_commit']
    assert fields['HW_DEVICE'].strip('"') == 'GENERIC_X64'
    installer = INPUT / binding['installer_path']
    assert sha(installer) == binding['installer_sha256']
    if a.seal_output:
        signal.signal(signal.SIGALRM, expired); signal.alarm(15)
        seal_output(); print('PIX582_EXPORT_SEALED', flush=True); return 0
    index = CASES.index(a.case)
    root = OUTPUT / 'steam'; root.mkdir(exist_ok=True)
    assert sorted(p.name for p in root.iterdir()) == [f'{n + 1:02d}-{c}' for n, c in enumerate(CASES[:index])]
    for n, c in enumerate(CASES[:index]):
        old = json.loads((root / f'{n + 1:02d}-{c}' / 'stage-result.json').read_text())
        assert old['status'] == 'PASS' and old['restored'] is True
    assert os.statvfs(OUTPUT).f_bavail * os.statvfs(OUTPUT).f_frsize >= MAX_STAGE
    stage = root / f'{index + 1:02d}-{a.case}'; stage.mkdir()
    scratch = Path('/run') / f'pix582-stage-{index + 1:02d}'
    assert not scratch.exists() and not scratch.is_symlink() and not children()
    assert ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0
    result = {'status': 'FAIL', 'case': a.case, 'original_wrapper_exit': None,
              'restored': False, 'started_monotonic': time.monotonic(), 'scope': 'source chroot; no installed/native Steam claim'}
    proc = None; mounted = False; output = scratch / a.case
    before = parent_state(); save(stage / 'parent-before.json', before)
    signal.signal(signal.SIGALRM, expired); signal.signal(signal.SIGTERM, expired); signal.alarm(160)
    try:
        scratch.mkdir(mode=0o700)
        mount = subprocess.run(['mount', '-n', '-t', 'tmpfs', '-o', 'size=3G,mode=700,nosuid,nodev', 'tmpfs', str(scratch)], capture_output=True, timeout=5)
        save(stage / 'scratch-mount.json', {'original_exit': mount.returncode, 'stderr': mount.stderr.decode(errors='replace')})
        assert mount.returncode == 0; mounted = True
        output = scratch / a.case
        argv = ['timeout', '--signal=TERM', '--kill-after=10s', '120s', 'python3', '-I', '-S', '-B',
                str(PACKET / 'fixture.py'), '--disposable-vm', '--case', a.case,
                '--installer', str(installer), '--output', str(output)]
        env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LC_ALL': 'C', 'LANG': 'C', 'TMPDIR': str(scratch)}
        save(stage / 'command.json', {'argv': argv, 'environment': env})
        with (stage / 'stdout').open('xb') as stdout, (stage / 'stderr').open('xb') as stderr:
            proc = subprocess.Popen(argv, env=env, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, start_new_session=True)
            result['command_pid'] = proc.pid
            deadline = time.monotonic() + 132
            while proc.poll() is None:
                assert time.monotonic() < deadline, 'Original timeout wrapper did not finish'
                assert stdout.tell() <= 2 * 1024**2 and stderr.tell() <= 2 * 1024**2, 'Wrapper output cap'
                time.sleep(0.1)
            result['original_wrapper_exit'] = proc.returncode
        save(stage / 'original-result.json', {'wrapper_exit': proc.returncode})
        assert not children(), 'Stage descendants remain after fixture exit'
        result['export'] = export_case(output, stage)
        fixture = json.loads((output / 'result.json').read_text())
        namespace = json.loads((output / 'namespace-result.json').read_text())
        result['fixture_status'] = fixture['status']
        result['original_caller_exits'] = namespace['attempts'] and [x['installer_exit'] for x in namespace['attempts']]
        expected = [1, 0] if a.case in RETRIES else [1] if a.case in NEGATIVE else [0]
        result['expected_original_caller_exits'] = expected
        assert_namespaces_gone(namespace['namespaces'])
        assert proc.returncode == 0 and fixture['status'] == 'PASS' and namespace['status'] == 'RETURNED'
        assert result['original_caller_exits'] == expected
        assert fixture['guard'] is None and fixture['remaining_descendants'] == []
        assert fixture['supervision']['quiescent'] and not fixture['supervision']['intervention']
        assert namespace['remaining_descendants'] == [] and all(x['trace_driver_exit'] == x['installer_exit'] for x in namespace['attempts'])
        assert parent_state() == before, 'Selected real guest state changed'
        subprocess.run(['sync'], check=True, timeout=5)
        unmount = subprocess.run(['umount', str(scratch)], capture_output=True, timeout=5)
        save(stage / 'scratch-unmount.json', {'original_exit': unmount.returncode, 'stderr': unmount.stderr.decode(errors='replace')})
        assert unmount.returncode == 0; mounted = False
        scratch.rmdir()
        assert not any(p == str(scratch) or p.startswith(str(scratch) + '/') for p, _ in mount_rows())
        assert not children() and parent_state() == before
        save(stage / 'parent-after.json', parent_state())
        result['restored'] = True; result['status'] = 'PASS'
    except BaseException as error:
        result['error'] = repr(error)
    finally:
        signal.alarm(0)
        if proc is not None and proc.poll() is None:
            result['failure_intervention'] = True
            os.killpg(proc.pid, signal.SIGTERM)
            try: proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL); proc.wait(timeout=3)
            result['original_wrapper_exit'] = proc.returncode
        if output.is_dir() and not (stage / 'fixture-records.tar.gz').exists() and not children():
            try:
                signal.alarm(10)
                result['failure_export'] = export_case(output, stage)
            except BaseException as error:
                result['failure_export_error'] = repr(error)
            finally:
                signal.alarm(0)
        result['scratch_still_mounted'] = mounted
        result['elapsed_seconds'] = time.monotonic() - result['started_monotonic']
        result['remaining_descendants'] = children()
        if result['remaining_descendants']:
            result['status'] = 'FAIL'
        # Failure scratch stays in this disposable guest until bounded family teardown.
        # It is never erased or reused to manufacture restoration.
        save(stage / 'stage-result.json', result)
        rows = seal_output()
        assert sum(x['bytes'] for x in rows if x['path'].startswith('steam/' + stage.name + '/')) <= MAX_STAGE
        print('PIX582_STAGE_RESULT:' + json.dumps({'case': a.case, 'status': result['status'],
              'restored': result['restored'], 'original_wrapper_exit': result['original_wrapper_exit']}), flush=True)
    return 0 if result['status'] == 'PASS' else 1


def sys_flags_safe():
    import sys
    return sys.flags.optimize == 0


if __name__ == '__main__':
    raise SystemExit(main())
