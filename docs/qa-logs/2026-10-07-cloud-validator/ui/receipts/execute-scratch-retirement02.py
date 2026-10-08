#!/usr/bin/env python3
"""Execute the one reviewed UI scratch plan; refuse scope or input drift."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

PACKET = Path(__file__).resolve().parent.parent
ROOT = Path('/workspace/tmp/pixelelated-510-es-ui')
PLAN = PACKET / 'receipts/retirement-plan.json'
RECEIPT = PACKET / 'receipts/scratch-retirement-executed02.json'
EXPECTED = {
    'build08/emulationstation': '4926f10e128807d480dc080ea58488bb618aa75e866f99cae33ee55ce6d14e00',
    'build08/artifacts/fr.mo': '48a183b04ad3be28dc97d6a335eee61730bb36a195d1246f1bdf5c2178b81125',
}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def run(*argv):
    return subprocess.run(argv, check=True, capture_output=True, text=True, timeout=20).stdout


def identity(path):
    s = path.lstat()
    return {'device': s.st_dev, 'inode': s.st_ino, 'mode': s.st_mode}


def checkpoint():
    RECEIPT.write_text(json.dumps(receipt, indent=2) + '\n')


assert not RECEIPT.exists(), 'Never overwrite a prior execution receipt'
plan = json.loads(PLAN.read_text())
assert plan['root'] == str(ROOT) and ROOT.resolve() == ROOT
assert plan['bytes_excluding_preserved'] == 449796406
scopes = [Path(c['scope']) for c in plan['candidates']]
allowed = {f'build{i:02d}' for i in range(1, 9)} | {'guest01', 'host01'} | {f'ui{i:02d}' for i in range(1, 11)}
assert {s.name for s in scopes} == allowed and len(scopes) == 20
preserve = {Path(p) for p in plan['preserve']}
assert preserve == {ROOT / 'guest02', *(ROOT / p for p in EXPECTED)}
subprocess.run(['sha256sum', '--quiet', '-c', 'SHA256SUMS'], cwd=PACKET, check=True)
receipt = {
    'schema_version': 1, 'started_utc': utc(), 'state': 'preflight',
    'authorization': 'Root delegated exact prepared plan execution under user retention policy; no guest actions.',
    'plan_sha256': digest(PLAN), 'packet_seal_before_sha256': digest(PACKET / 'SHA256SUMS'),
    'packet_files_verified_before': len((PACKET / 'SHA256SUMS').read_text().splitlines()),
    'pid_namespace': os.readlink('/proc/self/ns/pid'), 'removed': [],
}
checkpoint()
try:
    expected_hashes = {str(ROOT / p): digest(ROOT / p) for p in EXPECTED}
    assert expected_hashes == {str(ROOT / p): h for p, h in EXPECTED.items()}
    guest_paths = [ROOT / 'guest02', ROOT / 'guest02/vm.qcow2', ROOT / 'guest02/qa-key']
    guest_before = {str(p): identity(p) for p in guest_paths} if (ROOT / 'guest02').exists() else {}
    receipt['protected_before'] = {'artifact_hashes': expected_hashes, 'guest_identities': guest_before}
    if guest_before:
        qemu_pid = int((ROOT / 'guest02/vm.pid').read_text().strip())
        assert (Path('/proc') / str(qemu_pid)).exists(), 'Root-owned guest must remain alive'
    else:
        retired = PACKET.parent / 'roundtrip/guest-retirement.json'
        retired_data = json.loads(retired.read_text())
        assert retired_data['retired_guest_tree'] == str(ROOT / 'guest02')
        assert retired_data['no_immediately_queued_guest_test'] is True
        assert not Path('/proc', str(retired_data['guest_pid'])).exists()
        qemu_pid = None
        receipt['root_guest_retirement'] = {'receipt': str(retired), 'sha256': digest(retired),
                                            'note': 'Root completed both ordinary suites and retired guest before this cleanup began.'}

    manifests = []
    for item, scope in zip(plan['candidates'], scopes):
        assert scope.parent == ROOT and scope.resolve() == scope and scope.is_dir()
        assert not (scope / '.git').exists(), 'No source checkout may be retired'
        files, dirs = [], []
        for folder, subdirs, names in os.walk(scope, followlinks=False):
            folder = Path(folder)
            for name in subdirs + names:
                p = folder / name
                s = p.lstat()
                assert not stat.S_ISLNK(s.st_mode), f'Symlink refused: {p}'
                assert s.st_dev == ROOT.stat().st_dev, f'Cross-filesystem path refused: {p}'
                if p in preserve:
                    continue
                if stat.S_ISDIR(s.st_mode):
                    assert not os.path.ismount(p), f'Mountpoint refused: {p}'
                elif stat.S_ISREG(s.st_mode):
                    files.append((p, (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns), s.st_blocks * 512, digest(p)))
                else:
                    raise RuntimeError(f'Special file refused: {p}')
            dirs.append(folder)
        assert len(files) == item['files'] and sum(f[1][2] for f in files) == item['bytes'], f'Plan drift: {scope}'
        manifests.append((item, files, dirs))

    # Inspect actual host process arguments, cwd, and accessible file descriptors.
    # Only matching scope names are recorded; unrelated command lines remain private.
    matches, unreadable_same_uid, examined = [], [], 0
    scope_strings = [str(s) for s in scopes]
    def scoped(value):
        return [s for s in scope_strings if value == s or value.startswith(s + '/')]
    for proc in Path('/proc').iterdir():
        if not proc.name.isdigit() or int(proc.name) == os.getpid():
            continue
        try:
            uid = proc.stat().st_uid
            argv = (proc / 'cmdline').read_bytes().split(b'\0')
            hits = {s for s in scope_strings if any(s.encode() in a for a in argv)}
            examined += 1
            if uid == os.getuid():
                try:
                    hits.update(scoped(os.readlink(proc / 'cwd')))
                    for fd in (proc / 'fd').iterdir():
                        try:
                            hits.update(scoped(os.readlink(fd)))
                        except FileNotFoundError:
                            pass
                except PermissionError:
                    unreadable_same_uid.append(int(proc.name))
            if hits:
                matches.append({'pid': int(proc.name), 'scopes': sorted(hits)})
        except (FileNotFoundError, ProcessLookupError):
            pass
    receipt['process_check'] = {'utc': utc(), 'processes_examined': examined, 'matching_processes': matches,
                                'same_uid_unreadable_dependencies': unreadable_same_uid, 'guest_pid_preserved': qemu_pid}
    # These exact privileged session services were identified independently.
    # Their worker children and every readable process were checked above.
    service_roles = {
        2325: ('systemd', '/usr/lib/systemd/systemd --user'),
        2342: ('(sd-pam)', '(sd-pam)'),
        564119: ('ssh-agent', '/usr/bin/ssh-agent -D -a /run/user/1000/gcr/.ssh'),
        2880345: ('sshd-session', 'sshd-session: max@notty'),
    }
    classified = []
    unclassified = []
    for pid in unreadable_same_uid:
        proc = Path('/proc') / str(pid)
        role = ((proc / 'comm').read_text().strip(),
                (proc / 'cmdline').read_bytes().decode().replace('\0', ' ').strip())
        if service_roles.get(pid) == role:
            classified.append({'pid': pid, 'role': role[0],
                               'reason': 'Privileged user/session service; no command scope match. All readable descendants checked.'})
        else:
            unclassified.append(pid)
    receipt['process_check']['classified_unreadable_session_services'] = classified
    receipt['process_check']['unclassified_unreadable_dependencies'] = unclassified
    assert not matches and not unclassified, 'Active or unclassified dependency refuses removal'
    ids = run('docker', 'ps', '--quiet').split()
    mounted = []
    if ids:
        for line in run('docker', 'inspect', '--format', '{{json .Mounts}}', *ids).splitlines():
            for mount in json.loads(line):
                source = mount.get('Source', '').rstrip('/') or '/'
                for scope in scope_strings:
                    if source == scope or scope.startswith(source + '/') or source.startswith(scope + '/') or source == '/':
                        mounted.append({'source': source, 'scope': scope})
    receipt['container_mount_check'] = {'running_containers': len(ids), 'matching_mounts': mounted}
    assert not mounted, 'Container mount dependency refuses removal'
    before = os.statvfs(ROOT)
    receipt['filesystem_available_bytes_before'] = before.f_bavail * before.f_frsize
    receipt['state'] = 'deleting exact reviewed files'
    checkpoint()
    for item, files, dirs in manifests:
        aggregate = hashlib.sha256()
        for path, expected_stat, blocks, sha in files:
            s = path.lstat()
            assert (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns) == expected_stat, f'File changed: {path}'
            assert path not in preserve and ROOT / 'guest02' not in path.parents
            aggregate.update((str(path.relative_to(ROOT)) + '\0' + sha + '\n').encode())
            path.unlink()
        removed_dirs = 0
        for directory in sorted(dirs, key=lambda p: len(p.parts), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
                removed_dirs += 1
        receipt['removed'].append({'scope': item['scope'], 'files': len(files), 'logical_bytes': item['bytes'],
                                   'allocated_bytes': sum(f[2] for f in files), 'directories': removed_dirs,
                                   'ordered_path_and_content_sha256_digest': aggregate.hexdigest()})
        checkpoint()
    final_hashes = {str(ROOT / p): digest(ROOT / p) for p in EXPECTED}
    assert final_hashes == expected_hashes
    if guest_before:
        assert {str(p): identity(p) for p in guest_paths} == guest_before
        assert (Path('/proc') / str(qemu_pid)).exists()
    else:
        assert not (ROOT / 'guest02').exists()
    assert set(ROOT.iterdir()) == ({ROOT / 'guest02', ROOT / 'build08'} if guest_before else {ROOT / 'build08'})
    assert {p for p in (ROOT / 'build08').rglob('*') if p.is_file()} == {ROOT / p for p in EXPECTED}
    subprocess.run(['sha256sum', '--quiet', '-c', 'SHA256SUMS'], cwd=PACKET, check=True)
    after = os.statvfs(ROOT)
    receipt.update({'state': 'complete', 'finished_utc': utc(), 'protected_after': {'artifact_hashes': final_hashes,
                    'guest_identities': guest_before, 'guest_pid_alive': qemu_pid},
                    'removed_files': sum(r['files'] for r in receipt['removed']),
                    'removed_directories': sum(r['directories'] for r in receipt['removed']),
                    'retired_logical_bytes': sum(r['logical_bytes'] for r in receipt['removed']),
                    'retired_allocated_bytes': sum(r['allocated_bytes'] for r in receipt['removed']),
                    'filesystem_available_bytes_after': after.f_bavail * after.f_frsize,
                    'filesystem_available_delta_bytes': after.f_bavail * after.f_frsize - receipt['filesystem_available_bytes_before'],
                    'free_space_caveat': 'Concurrent ordinary QA is active; filesystem delta is observational, not a solely attributed cleanup measure.',
                    'original_packet_verified_after': True,
                    'untouched': ['guest input, guest disk contents, guest key, guest processes',
                                  'source checkouts', 'accepted build roots', 'shared rclone', 'original failure logs in canonical packet']})
    checkpoint()
    print(json.dumps({k: receipt[k] for k in ('state', 'removed_files', 'removed_directories', 'retired_logical_bytes', 'retired_allocated_bytes', 'filesystem_available_delta_bytes')}))
except BaseException as exc:
    receipt.update({'state': 'failed; inspect before retry', 'failed_utc': utc(), 'error': str(exc)})
    checkpoint()
    raise
