from pathlib import Path
from datetime import datetime, timezone
import collections, hashlib, json, os, stat, subprocess, sys, time

owner = Path(__file__).resolve().parent
out = owner / 'artifacts'
(owner / 'run.path').write_text(str(Path.cwd() / os.environ['RASTERATOPS_BUILD_RUN']) + '\n')

def now():
    return datetime.now(timezone.utc).isoformat()

def ident(s):
    return dict(device=s.st_dev, inode=s.st_ino, size=s.st_size,
                allocated_bytes=s.st_blocks * 512, mtime_ns=s.st_mtime_ns,
                uid=s.st_uid, mode=s.st_mode, links=s.st_nlink)

def capacity():
    s = os.statvfs('/workspace')
    return dict(utc=now(), total_bytes=s.f_blocks*s.f_frsize,
                available_bytes=s.f_bavail*s.f_frsize,
                used_bytes=(s.f_blocks-s.f_bfree)*s.f_frsize,
                reserved_free_bytes=(s.f_bfree-s.f_bavail)*s.f_frsize)

rc = 1
try:
    for name, digest in json.loads((owner / 'seal.json').read_text()).items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    started = now()
    (out / 'before.json').write_text(json.dumps(capacity(), indent=2) + '\n')
    roots = [Path('/workspace/tmp'), Path('/workspace/artifacts/rocknix-images')]
    rows, large, symlinks, errors, disks, metadata = [], [], [], [], [], []
    seen_links, hardlinks = set(), collections.defaultdict(list)
    directories = files = 0
    tick = time.monotonic()
    for root in roots:
        device = root.stat().st_dev
        entries = list(root.iterdir())
        for group in sorted(entries):
            if group == owner or group.name == 'pixelelated-m7-broad-root-readback-01':
                continue
            totals = dict(path=str(group), allocated_bytes=0, apparent_bytes=0,
                          files=0, directories=0, symlinks=0, special=0)
            pending = [group]
            while pending:
                p = pending.pop()
                try:
                    s = p.lstat()
                    if s.st_dev != device:
                        errors.append(dict(path=str(p), error='cross-filesystem entry'))
                        continue
                    if stat.S_ISLNK(s.st_mode):
                        symlinks.append(dict(source=str(p), target=os.path.realpath(p), link=os.readlink(p)))
                        totals['symlinks'] += 1
                    elif stat.S_ISDIR(s.st_mode):
                        totals['allocated_bytes'] += s.st_blocks * 512
                        totals['directories'] += 1
                        directories += 1
                        with os.scandir(p) as children:
                            pending.extend(Path(x.path) for x in children)
                    elif stat.S_ISREG(s.st_mode):
                        files += 1
                        totals['files'] += 1
                        totals['apparent_bytes'] += s.st_size
                        key = (s.st_dev, s.st_ino)
                        if s.st_nlink > 1:
                            hardlinks[str(key)].append(str(p))
                        if s.st_nlink == 1 or key not in seen_links:
                            totals['allocated_bytes'] += s.st_blocks * 512
                        if s.st_nlink > 1:
                            seen_links.add(key)
                        if s.st_blocks * 512 >= 8 * 1024**2:
                            large.append(dict(path=str(p), group=str(group), identity=ident(s)))
                        if p.name.endswith(('.qcow2', '.qcow', '.vmdk', '.vdi', '.vhd', '.vhdx')):
                            disks.append(dict(path=str(p), group=str(group), identity=ident(s)))
                        elif p.name.endswith(('.img', '.raw')):
                            with p.open('rb') as stream:
                                if stream.read(4) == b'QFI\xfb':
                                    disks.append(dict(path=str(p), group=str(group), identity=ident(s)))
                        if p.name in ['RECORD.txt', 'result.json', 'manifest.json', 'owner-verification.json',
                                      'build.rc', 'inner.rc', 'outer.rc', 'tool-wrapper.rc', 'launcher-result.json'] or p.suffix == '.sha256':
                            metadata.append(dict(path=str(p), identity=ident(s)))
                    else:
                        totals['special'] += 1
                except OSError as error:
                    errors.append(dict(path=str(p), error=str(error)))
                if time.monotonic() - tick >= 10:
                    print(f'Scanned {directories} directories, {files} files, {len(large)} large payloads; {len(errors)} errors', flush=True)
                    tick = time.monotonic()
            rows.append(totals)
    for number, row in enumerate(disks):
        p = Path(row['path'])
        try:
            call = subprocess.run(['qemu-img', 'info', '--force-share', '--backing-chain', '--output=json', str(p)],
                                  capture_output=True, text=True, timeout=30)
            row['qemu_returncode'] = call.returncode
            row['unchanged'] = row['identity'] == ident(p.lstat())
            if call.returncode == 0:
                row['chain'] = json.loads(call.stdout)
            else:
                row['inspection_error'] = call.stderr
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            row['inspection_error'] = str(error)
        if number % 25 == 0:
            print(f'Inspected {number+1}/{len(disks)} disk chains', flush=True)
    report = dict(started_utc=started, finished_utc=now(), roots=[str(r) for r in roots],
                  directories=directories, files=files, groups=rows, large_files=large,
                  disks=disks, symlinks=symlinks, metadata=metadata,
                  hardlinks=dict(hardlinks), errors=errors, capacity=capacity(),
                  scope='Read-only classification input; no removal eligibility or content preservation claimed.')
    file = out / 'inventory.json'
    file.write_text(json.dumps(report, indent=2) + '\n')
    summary = dict(started_utc=started, finished_utc=report['finished_utc'],
                   directories=directories, files=files, groups=len(rows), large_files=len(large),
                   disks=len(disks), errors=len(errors),
                   disk_inspection_errors=sum('inspection_error' in x for x in disks),
                   allocated_bytes=sum(r['allocated_bytes'] for r in rows),
                   report_sha256=hashlib.sha256(file.read_bytes()).hexdigest(), deletion_performed=False)
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary), flush=True)
    assert not errors, errors[:5]
    rc = 0
finally:
    (owner / 'inner.rc').write_text(str(rc) + '\n')
    (owner / 'outer.rc').write_text(str(rc) + '\n')
sys.exit(rc)
