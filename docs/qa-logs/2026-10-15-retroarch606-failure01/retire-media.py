"""Retire only consumed #606 disposable media after compact evidence custody."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, stat

p = argparse.ArgumentParser()
p.add_argument('--owner', type=Path, required=True)
p.add_argument('--export', dest='export', type=Path, required=True)
p.add_argument('--custody', type=Path, required=True)
a = p.parse_args()
o, e, c = a.owner, a.export, a.custody
assert o.parent == e.parent == Path('/workspace/tmp')
assert re.fullmatch(r'pix-m7-retroarch-exit-proof-20261015-\d\d', o.name)
assert re.fullmatch(r'pix-m7-retroarch-exit-evidence-20261015-\d\d', e.name)
assert o.resolve() == o and e.resolve() == e and c.resolve() == c
assert Path('/proc/self/ns/pid').stat().st_ino == 4026531836
assert os.getuid() == 1000 and not (o / 'retirement.json').exists()
load = lambda f: json.loads(f.read_text())
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
run = Path((o / 'run.path').read_text().strip())
consumed = load(run / 'admission-consumed.json')
assert consumed['state'] == 'consumed' and consumed['run'] == str(run)
assert consumed['evidence_sha256'] == sha(e / 'consumption-draft.json')
receipt = load(e / 'host-exits.json')
vm = load(o / 'vm-result.json')
assert receipt['status'] == 'OWNERS_GONE' and receipt['channels_coherent']
assert receipt['original_channels']['monitor'] == 0
assert vm['rc'] == receipt['original_rc']
assert not vm['cleanup_errors'] and not vm['qemu_still_live']
assert not vm['surviving_host_processes'] and not vm['remaining_host_children']
for pid in set(receipt['pids_exited'] + [v['pid'] for v in receipt['qemu_identities']]):
    assert not Path('/proc', str(pid)).exists(), ('recorded pid remains', pid)
evidence = {}
for f in e.iterdir():
    assert f.is_file() and not f.is_symlink() and f.stat().st_size < 64 * 1024**2
    assert sha(c / f.name) == sha(f), f
    evidence[f.name] = sha(f)
rows = []
for name in ['vm/disk.qcow2', 'vm/OVMF.fd']:
    f = o / name
    s = f.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_uid == os.getuid()
    assert f.resolve() == f and s.st_nlink == 1
    rows.append(dict(path=str(f), device=s.st_dev, inode=s.st_ino,
                     mtime_ns=s.st_mtime_ns, bytes=s.st_size,
                     allocated_bytes=s.st_blocks * 512))
tmp = o / 'host-tmp'
assert tmp.is_dir() and not tmp.is_symlink() and not list(tmp.iterdir())
for row in rows:
    f = Path(row['path'])
    s = f.lstat()
    assert (s.st_dev, s.st_ino, s.st_mtime_ns, s.st_size) == (
        row['device'], row['inode'], row['mtime_ns'], row['bytes'])
    f.unlink()
    assert not f.exists() and not f.is_symlink()
    row['absent_after'] = True
tmp.rmdir()
assert all(sha(e / n) == h == sha(c / n) for n, h in evidence.items())
result = dict(result='RETIRED_EXACT_CONSUMED_MEDIA',
              utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              original_rc=vm['rc'], admission=consumed['id'], targets=rows,
              empty_tmpdir_removed=str(tmp), custody=str(c), evidence=evidence,
              source_image_touched=False, other_records_retained=True)
with (o / 'retirement.json').open('x') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
print(json.dumps(result))
