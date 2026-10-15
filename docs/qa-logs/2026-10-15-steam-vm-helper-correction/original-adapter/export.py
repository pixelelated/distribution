#!/usr/bin/env python3
"""Export original stopped-guest receipts; does not consume or retire owners."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import tarfile

p = argparse.ArgumentParser()
p.add_argument('--owner', type=Path, required=True)
p.add_argument('--checkout', type=Path, required=True)
p.add_argument('--run', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--retain-failed', action='store_true', help='Preserve failed original channels; never qualifies the family')
a = p.parse_args()
runtime = json.loads((a.owner / 'records/runtime.json').read_text())
assert str(a.checkout) == runtime['checkout'] and a.run.parent == a.checkout / '.build-runs'
vm = json.loads((a.owner / 'vm-result.json').read_text())
launcher = json.loads((a.owner / 'lifecycle-owner/launcher-result.json').read_text())
runner = json.loads((a.run / 'runner-result.json').read_text())
originals_pass = (vm['rc'] == launcher['runner_returncode'] == runner['runner_rc'] == runner['command_rc'] == 0 and runner['monitor_rc'] == 0 and (a.owner / 'lifecycle-owner/tool-wrapper.rc').read_text().strip() == '0')
assert originals_pass or a.retain_failed, 'Original family failed; use explicit preservation mode'
pids = [vm['boots'][0]['pid'], launcher['pid']] + [int((a.run / name).read_text()) for name in ('build.pid', 'command.pid', 'watcher.pid')]
assert all(not Path('/proc', str(pid)).exists() for pid in pids)
assert 'down: owned QEMU exited' in (a.owner / 'vm-stop.log').read_text()
unmount = a.owner / ('unmount-' + runtime['panel'] + '.txt')
if originals_pass:
    assert 'PIX_UNMOUNT_RC:0' in unmount.read_text()
a.output.mkdir()
(a.output / 'guest').mkdir()
def sha(f):
    h = hashlib.sha256()
    with f.open('rb') as stream:
        for block in iter(lambda: stream.read(1024**2), b''): h.update(block)
    return h.hexdigest()
def debug(source, target):
    argv = ['debugfs', '-R', 'dump ' + shlex.quote(source) + ' ' + shlex.quote(str(target)), str(a.owner / 'vm/output.ext4')]
    child = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    with (a.output / 'debugfs.log').open('a') as out:
        out.write(json.dumps({'argv': argv, 'original_exit': child.returncode}) + '\n' + child.stdout + child.stderr)
    assert child.returncode == 0 and target.is_file()
debug('/guest-export-manifest.json', a.output / 'guest-export-manifest.json')
rows = json.loads((a.output / 'guest-export-manifest.json').read_text())
assert rows and sum(row['bytes'] for row in rows) <= 1100 * 1024**2
for row in rows:
    name = Path(row['path'])
    assert not name.is_absolute() and '..' not in name.parts and name.parts[0] == 'steam'
    assert 0 <= row['bytes'] <= 75 * 1024**2
    target = a.output / 'guest' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    debug('/' + str(name), target)
    assert target.stat().st_size == row['bytes'] and sha(target) == row['sha256']
stages = []
for index, case in enumerate(runtime['cases'], 1):
    folder = a.output / 'guest/steam' / f'{index:02d}-{case}'
    if not folder.exists():
        assert a.retain_failed
        break
    stage_file = folder / 'stage-result.json'
    observed = json.loads(stage_file.read_text()) if stage_file.exists() else {'status': 'MISSING'}
    archive_path, members_path = folder / 'fixture-records.tar.gz', folder / 'archive-members.json'
    if archive_path.exists() and members_path.exists():
        originals_manifest = json.loads(members_path.read_text())
        with tarfile.open(archive_path, 'r:gz') as archive:
            members = archive.getmembers()
            assert all(m.isfile() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts for m in members)
            assert [m.name for m in members] == [m['path'] for m in originals_manifest]
            for member in originals_manifest:
                digest = hashlib.sha256(); count = 0
                with archive.extractfile(member['path']) as stream:
                    for block in iter(lambda: stream.read(1024**2), b''):
                        count += len(block); assert count <= 2 * 1024**2; digest.update(block)
                assert count == member['bytes'] and digest.hexdigest() == member['sha256']
    else:
        assert a.retain_failed
    stages.append({'case': case, 'status': observed['status'], 'restored': observed.get('restored', False)})
qualified = originals_pass and len(stages) == 14 and all(x['status'] == 'PASS' and x['restored'] for x in stages)
assert qualified or a.retain_failed, 'Original stages did not all qualify'
originals = []
for root, label in ((a.owner, 'owner'), (a.run, 'run')):
    for f in sorted(root.rglob('*')):
        if f.is_file() and not f.is_symlink() and not (root == a.owner and f.is_relative_to(a.owner / 'vm')):
            assert f.stat().st_size < 32 * 1024**2
            originals.append((f, label + '/' + str(f.relative_to(root))))
with tarfile.open(a.output / 'original-records.tar.gz', 'x:gz') as archive:
    for f, name in originals:
        archive.add(f, arcname=name, recursive=False)
with tarfile.open(a.output / 'original-records.tar.gz') as archive:
    assert {x.name for x in archive.getmembers() if x.isfile()} == {name for _, name in originals}
    for f, name in originals:
        data = archive.extractfile(name).read()
        assert len(data) == f.stat().st_size and hashlib.sha256(data).hexdigest() == sha(f)
(a.output / 'original-records.json').write_text(json.dumps([{'path': name, 'bytes': f.stat().st_size, 'sha256': sha(f)} for f, name in originals], indent=2) + '\n')
(a.output / 'host-exits.json').write_text(json.dumps({'pids_absent': pids}, indent=2) + '\n')
(a.output / 'export-result.json').write_text(json.dumps({'original_exit': 0, 'guest_files': len(rows), 'guest_bytes': sum(x['bytes'] for x in rows), 'host_files': len(originals), 'qualification_pass': qualified, 'stages': stages, 'original_family_pass': originals_pass, 'runtime': 'source-chroot preservation only; no installed/native Steam claim; coordinator owns consumption'}, indent=2) + '\n')
print(str(a.output))
