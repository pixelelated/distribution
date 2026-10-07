"""Execute the exact reviewed #493/#494 batch; verify-only unless --apply."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import time

BASE = Path('/workspace/tmp')
REPO = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
PLAN = BASE / 'pixelelated-m7-broad-retirement-plan-01/plan.json'
EXTRACTIONS = BASE / 'pixelelated-m7-extraction-retention-02/artifacts/result.json'
ROOT_CHECK = BASE / 'pixelelated-m7-broad-root-readback-01/root-process-readback.json'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def identity(path):
    s = Path(path).lstat()
    return dict(device=s.st_dev, inode=s.st_ino, size=s.st_size,
                allocated_bytes=s.st_blocks * 512, mtime_ns=s.st_mtime_ns,
                uid=s.st_uid, mode=s.st_mode, links=s.st_nlink)


def same(row, hashed=False):
    p = Path(row['path'])
    require(str(p.resolve()) == str(p) and not p.is_symlink(), 'redirected file: ' + str(p))
    require(identity(p) == row['identity'], 'identity changed: ' + str(p))
    if hashed:
        require(sha(p) == row['sha256'], 'content changed: ' + str(p))
        require(identity(p) == row['identity'], 'file changed while hashing: ' + str(p))


def available():
    s = os.statvfs('/workspace')
    return s.f_bavail * s.f_frsize


def write(path, data):
    with Path(path).open('x') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')


def within(path, root):
    return path == root or path.startswith(root.rstrip('/') + '/')


def check_root_coverage(targets, roots):
    missing = [target for target in targets if not any(within(target, root) for root in roots)]
    require(not missing, 'administrator check omitted cleanup targets: ' + repr(missing))


def live_check(targets, owner, label):
    receipt = read(ROOT_CHECK)
    require(receipt['effective_uid'] == 0 and receipt['readonly'] and not receipt['unreadable'], 'incomplete administrator check')
    require(receipt['roots'] == read(ROOT_CHECK.parent / 'roots.json'), 'administrator scope changed')
    check_root_coverage(targets, receipt['roots'])
    stamp = datetime.fromisoformat(receipt['utc']).timestamp()
    age = time.time() - stamp
    require(0 <= age < 7200, 'administrator check outside this cleanup session')
    for hit in receipt['matches']:
        require(all(not any(within(r['tree'], t) or within(t, r['tree']) for t in targets)
                    for r in hit['references']), 'administrator snapshot names a cleanup target')
    btime = int(next(line.split()[1] for line in Path('/proc/stat').read_text().splitlines() if line.startswith('btime ')))
    hz = os.sysconf('SC_CLK_TCK')
    pattern = re.compile('(?:' + '|'.join(re.escape(t) for t in sorted(targets, key=len, reverse=True)) + r')(?=/|$|[\s\x00])')
    protected, hits, errors = [], [], []
    for process in Path('/proc').glob('[0-9]*'):
        if int(process.name) == os.getpid():
            continue
        try:
            status = dict(line.split(':', 1) for line in (process / 'status').read_text().splitlines() if ':' in line)
            if status.get('Kthread', '').strip() == '1':
                continue
            started = btime + int((process / 'stat').read_text().rsplit(')', 1)[1].split()[19]) / hz
            refs, denied = [], []
            for kind in ['cwd', 'exe', 'root']:
                try:
                    refs.append((kind, os.readlink(process / kind)))
                except PermissionError:
                    denied.append(kind)
                except FileNotFoundError:
                    pass
            refs.extend(('argument', os.fsdecode(x)) for x in (process / 'cmdline').read_bytes().split(b'\0') if x)
            try:
                for fd in (process / 'fd').iterdir():
                    try:
                        refs.append(('fd', os.readlink(fd)))
                    except FileNotFoundError:
                        pass
            except PermissionError:
                denied.append('fd')
            try:
                for line in (process / 'maps').read_text().splitlines():
                    parts = line.split(None, 5)
                    if len(parts) == 6:
                        refs.append(('mapping', parts[5]))
            except PermissionError:
                denied.append('maps')
            if denied:
                require(started < stamp, 'new protected process after administrator snapshot: ' + process.name)
                protected.append(dict(pid=int(process.name), started_epoch=started, fields=denied))
            for kind, value in refs:
                for match in pattern.finditer(value):
                    hits.append(dict(pid=int(process.name), kind=kind, target=match.group()))
        except FileNotFoundError:
            continue
        except (OSError, RuntimeError) as error:
            errors.append(dict(pid=int(process.name), error=str(error)))
    mounts = []
    for cid in subprocess.check_output(['docker', 'ps', '-aq'], text=True).split():
        data = json.loads(subprocess.check_output(['docker', 'inspect', cid], text=True))[0]
        for mount in data['Mounts']:
            if any(within(mount['Source'], t) or within(t, mount['Source']) for t in targets):
                mounts.append(dict(container=cid, source=mount['Source'], running=data['State']['Running']))
    # Actual mountpoints must never be recursively removed or unlinked as files.
    mounted = []
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        path = line.split()[4].replace('\\040', ' ').replace('\\134', '\\')
        if any(within(path, t) for t in targets):
            mounted.append(path)
    report = dict(utc=datetime.now(timezone.utc).isoformat(), administrator_receipt=str(ROOT_CHECK),
                  administrator_sha256=sha(ROOT_CHECK), administrator_age_seconds=age,
                  protected_existing_processes=protected, matches=hits, errors=errors,
                  container_mounts=mounts, host_mounts=mounted,
                  scope='Administrator snapshot plus current visible references and process birth times; protected fields are not claimed freshly reread. No new protected process is accepted.')
    write(owner / 'artifacts' / (label + '-live.json'), report)
    require(not hits and not errors and not mounts and not mounted, 'active-use check failed: ' + label)


def check_tree(root, entries):
    """Match every entry without following directory links; reject new files."""
    root = Path(root)
    require(str(root.resolve()) == str(root), 'redirected extraction root')
    expected = {r['path']: r for r in entries}
    require(len(expected) == len(entries) and str(root) in expected, 'invalid tree manifest')
    device = expected[str(root)]['identity']['device']
    pending, seen = [root], set()
    while pending:
        p = pending.pop()
        require(str(p) in expected, 'unreviewed extraction entry: ' + str(p))
        row = expected[str(p)]
        require(identity(p) == row['identity'], 'extraction entry changed: ' + str(p))
        s = p.lstat()
        require(s.st_dev == device, 'cross-device extraction')
        seen.add(str(p))
        if stat.S_ISLNK(s.st_mode):
            require(os.readlink(p) == row['target'], 'extraction symlink changed')
        elif stat.S_ISDIR(s.st_mode):
            require(s.st_uid == os.getuid(), 'unowned extraction directory')
            with os.scandir(p) as iterator:
                pending.extend(Path(e.path) for e in iterator)
        else:
            require(stat.S_ISREG(s.st_mode), 'special extraction entry')
    require(seen == set(expected), 'missing extraction entries')


def remove_tree(root, entries):
    check_tree(root, entries)
    root = Path(root)
    # Change only reviewed, owned directory modes. Never follow a link target.
    for row in entries:
        p = Path(row['path'])
        if stat.S_ISDIR(row['identity']['mode']):
            os.chmod(p, stat.S_IMODE(row['identity']['mode']) | 0o700, follow_symlinks=False)
    require(os.supports_dir_fd and os.fwalk, 'descriptor-relative removal unavailable')
    rootfd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        expected = {str(Path(r['path']).relative_to(root)): r for r in entries}
        for path, dirs, files, fd in os.fwalk('.', topdown=False, dir_fd=rootfd, follow_symlinks=False):
            for name in files + dirs:
                relative = str(Path(path) / name)
                row = expected[relative]
                s = os.stat(name, dir_fd=fd, follow_symlinks=False)
                require((s.st_dev, s.st_ino) == (row['identity']['device'], row['identity']['inode']), 'entry replaced during removal')
                if stat.S_ISDIR(s.st_mode):
                    os.rmdir(name, dir_fd=fd)
                else:
                    os.unlink(name, dir_fd=fd)
    finally:
        os.close(rootfd)
    root.rmdir()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    owner = args.owner.resolve(strict=True)
    require(os.getuid() != 0 and owner.parent == BASE, 'must run unprivileged under exact owner')
    require(not (owner / 'execution.json').exists(), 'owner already used')
    for name, digest in read(owner / 'seal.json').items():
        require(sha(name) == digest, 'sealed input changed: ' + name)
    plan, extracts = read(PLAN), read(EXTRACTIONS)
    require(len(plan['payloads']) == 850 and len(plan['worktrees']) == 4 and len(extracts['extractions']) == 10, 'scope mismatch')
    require(read(PLAN.parent / 'owner-verification.json')['result'] == 'PASS', 'plan not accepted')
    require(read(EXTRACTIONS.parent.parent / 'owner-verification.json')['result'] == 'PASS', 'extractions not accepted')
    approval = read(owner / 'authorization.json')
    require(approval['plan_sha256'] == sha(PLAN) and approval['extractions_sha256'] == sha(EXTRACTIONS), 'authorization scope mismatch')
    targets = [r['path'] for r in plan['payloads']] + [r['tree'] for r in plan['worktrees']]
    for row in extracts['extractions']:
        targets += [r['path'] for r in row['files']] + [row['extracted_root']]
    require(len(set(targets)) == 884, 'duplicate or unexpected targets')
    live_check(targets, owner, 'initial')
    fresh = read(BASE / 'pixelelated-m7-broad-dependencies-02/artifacts/result.json')
    old = read(BASE / 'pixelelated-m7-broad-dependencies-01/artifacts/result.json')
    require(read(BASE / 'pixelelated-m7-broad-dependencies-02/owner-verification.json')['result'] == 'PASS', 'fresh reference scan not accepted')
    for key in ['external_symlinks', 'artifact_path_references', 'container_mounts', 'errors']:
        require(fresh[key] == old[key], 'external references changed: ' + key)
    for row in plan['payloads']:
        same(row)
    require(sha(plan['retained_records']) == plan['retained_records_sha256'], 'record manifest changed')
    records = read(plan['retained_records'])
    for row in extracts['extractions']:
        require(sha(row['tree_manifest']) == row['tree_manifest_sha256'], 'extraction manifest changed')
        check_tree(row['extracted_root'], read(row['tree_manifest']))
        for entry in row['files']:
            same(entry, hashed=True)
        records.extend(row['records_retained'])
    records = list({r['path']: r for r in records}.values())
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda r: same(r, hashed=True), records))
    for row in plan['protected_test_firmware']:
        same(row, hashed=True)
    objects = read(Path(plan['custody_store']) / 'objects.json')
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda item: sha(item[1]['object']) == item[0], objects.items()))
    require(all(results), 'preserved source object changed')
    for row in plan['worktrees']:
        tree = row['tree']
        require(identity(tree) == row['root_identity'], 'worktree root changed')
        require(subprocess.check_output(['git', '-C', tree, 'rev-parse', 'HEAD'], text=True).strip() == row['head'], 'worktree head changed')
        diff = subprocess.check_output(['git', '-C', tree, 'diff', '--binary', 'HEAD'])
        require(hashlib.sha256(diff).hexdigest() == row['tracked_diff_sha256'], 'worktree edits changed')
    # Header readbacks verify the recorded backing graph immediately before removal.
    for row in plan['payloads']:
        if 'chain' in row:
            data = json.loads(subprocess.check_output(['qemu-img', 'info', '--force-share', '--backing-chain', '--output=json', row['path']], text=True))
            require(data == row['chain'], 'backing chain changed: ' + row['path'])
    live_check(targets, owner, 'before-removal')
    before = available()
    write(owner / 'verification.json', dict(utc=datetime.now(timezone.utc).isoformat(), result='PASS',
          payloads=850, worktrees=4, extractions=10, retained_records=len(records), custody_objects=len(objects),
          available_bytes=before, apply=args.apply, plan_sha256=sha(PLAN), extractions_sha256=sha(EXTRACTIONS)))
    print('PASS exact scope, source custody, records, backing graph and active-use checks', flush=True)
    if not args.apply:
        return
    removed = []
    try:
        with (owner / 'retired.ndjson').open('x') as journal:
            def record(row):
                removed.append(row)
                journal.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(), **row)) + '\n')
                journal.flush()
                os.fsync(journal.fileno())
            for row in plan['payloads']:
                same(row)
                Path(row['path']).unlink()
                record(dict(path=row['path'], identity=row['identity'], sha256=row['sha256'], kind='payload'))
            print('REMOVED 850 reviewed disk and firmware payloads', flush=True)
            for row in extracts['extractions']:
                for entry in row['files']:
                    same(entry)
                    Path(entry['path']).unlink()
                    record(dict(path=entry['path'], identity=entry['identity'], sha256=entry['sha256'], kind='extracted-file'))
                remove_tree(row['extracted_root'], read(row['tree_manifest']))
                record(dict(path=row['extracted_root'], tree_manifest=row['tree_manifest'], tree_manifest_sha256=row['tree_manifest_sha256'], kind='extracted-tree'))
                print('REMOVED extracted copy ' + Path(row['owner']).name, flush=True)
            for row in plan['worktrees']:
                tree = row['tree']
                live_check([tree], owner, Path(tree).name)
                with (owner / 'artifacts' / (Path(tree).name + '-remove.log')).open('x') as out:
                    subprocess.run([str(REPO / 'tools/fork-worktree'), 'remove', tree, '--force'], cwd=REPO, stdout=out, stderr=subprocess.STDOUT, check=True)
                require(not Path(tree).exists(), 'worktree remains after helper')
                record(dict(path=tree, head=row['head'], custody_store=plan['custody_store'], kind='worktree'))
                print('REMOVED worktree ' + Path(tree).name, flush=True)
    finally:
        write(owner / 'execution.json', dict(utc=datetime.now(timezone.utc).isoformat(), removed=removed,
              expected_targets=len(targets), before_available_bytes=before, after_available_bytes=available(),
              observed_recovery_bytes=available() - before, all_targets_absent=all(not os.path.lexists(p) for p in targets)))
    require(all(not os.path.lexists(p) for p in targets) and len(removed) == len(targets), 'incomplete cleanup')
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda r: same(r, hashed=True), records))
    for row in plan['protected_test_firmware']:
        same(row, hashed=True)
    require(all(sha(value['object']) == key for key, value in objects.items()), 'source custody changed after deletion')
    registered = subprocess.check_output(['git', 'worktree', 'list', '--porcelain'], cwd=REPO, text=True)
    require(all('worktree ' + r['tree'] + '\n' not in registered for r in plan['worktrees']), 'worktree still registered')
    write(owner / 'acceptance.json', dict(utc=datetime.now(timezone.utc).isoformat(), result='PASS',
          removed_targets=len(targets), retained_records_verified=len(records), custody_objects_verified=len(objects),
          test_firmware_verified=len(plan['protected_test_firmware']), available_bytes=available(),
          scope='Exact authorized scope retired; compact records and required inputs verified. Historical input links are preserved as provenance and may now dangle.'))
    print('PASS cleanup and retained-input verification; free bytes ' + str(available()), flush=True)


if __name__ == '__main__':
    main()
