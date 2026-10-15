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
assert (rows or a.retain_failed) and sum(row['bytes'] for row in rows) <= 1100 * 1024**2
for row in rows:
    name = Path(row['path'])
    assert not name.is_absolute() and '..' not in name.parts and name.parts[0] == 'steam'
    assert 0 <= row['bytes'] <= 75 * 1024**2
    target = a.output / 'guest' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    debug('/' + str(name), target)
    assert target.stat().st_size == row['bytes'] and sha(target) == row['sha256']
metadata = {'status': 'MISSING', 'restored': False, 'original_helper_exit': None,
            'archive_complete': False, 'qualification_pass': False}
metadata_rows = []
try:
    debug('/metadata-export-manifest.json', a.output / 'metadata-export-manifest.json')
    metadata_rows = json.loads((a.output / 'metadata-export-manifest.json').read_text())
    assert metadata_rows and len(metadata_rows) <= 32
    assert sum(row['bytes'] for row in metadata_rows) <= 16 * 1024**2
    assert sum(row['bytes'] for row in rows + metadata_rows) <= 1100 * 1024**2
    assert len({row['path'] for row in metadata_rows}) == len(metadata_rows)
    for row in metadata_rows:
        name = Path(row['path'])
        assert not name.is_absolute() and '..' not in name.parts and len(name.parts) == 2 and name.parts[0] == 'metadata'
        assert 0 <= row['bytes'] <= 16 * 1024**2
        target = a.output / 'guest' / name; target.parent.mkdir(parents=True, exist_ok=True)
        debug('/' + str(name), target)
        assert target.stat().st_size == row['bytes'] and sha(target) == row['sha256']
    folder = a.output / 'guest/metadata'
    stage = json.loads((folder / 'stage-result.json').read_text())
    metadata.update({key: stage[key] for key in ('status', 'restored', 'original_helper_exit')})
    members = json.loads((folder / 'control-members.json').read_text())
    helper = None
    with tarfile.open(folder / 'control-records.tar.gz', 'r:gz') as archive:
        actual = archive.getmembers()
        assert len(actual) == len(members) and [m.name for m in actual] == [m['path'] for m in members]
        for member, row in zip(actual, members):
            assert not Path(member.name).is_absolute() and '..' not in Path(member.name).parts
            assert member.mode == row['mode']
            if row['kind'] == 'symlink':
                assert member.issym() and member.linkname == row['target']
                assert not Path(member.linkname).is_absolute() and '..' not in Path(member.linkname).parts
            else:
                assert row['kind'] == 'file' and member.isfile() and member.size <= 2 * 1024**2
                data = archive.extractfile(member).read()
                assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256']
                if member.name == 'result.json':
                    helper = json.loads(data)
    metadata['archive_complete'] = True
    assert helper is not None, 'Original metadata helper result missing'
    metadata['helper_result'] = helper
    binding = json.loads((a.owner / 'records/family.json').read_text())['metadata']
    metadata['qualification_pass'] = (
        metadata['status'] == 'PASS' and metadata['restored'] is True and metadata['original_helper_exit'] == 0
        and helper['status'] == 'PASS' and helper['passed'] is True
        and helper['source_sha256'] == binding['candidate_source_sha256']
        and helper['baseline']['source_sha256'] == binding['frozen_installer_sha256']
        and helper['baseline']['executed'] is False and helper['scope'] == 'installed-vm-curl'
        and helper['curl_sha256'] == binding['installed_dependencies']['/usr/bin/curl']['sha256']
        and [row['path'] for row in helper['requests']] == ['/normal-cachyos', '/normal-ge', '/oversize', '/stall']
        and not helper['cleanup'] and not helper['signals'] and helper['old_families_equal'])
except (AssertionError, OSError, ValueError, KeyError, tarfile.TarError) as error:
    metadata.update(qualification_pass=False, preservation_error=repr(error))
    assert a.retain_failed, 'Original metadata evidence incomplete: ' + repr(error)
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
qualified = originals_pass and metadata['qualification_pass'] and len(stages) == 14 and all(x['status'] == 'PASS' and x['restored'] for x in stages)
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
(a.output / 'export-result.json').write_text(json.dumps({'original_exit': 0, 'guest_files': len(rows) + len(metadata_rows), 'guest_bytes': sum(x['bytes'] for x in rows + metadata_rows), 'host_files': len(originals), 'qualification_pass': qualified, 'metadata': metadata, 'stages': stages, 'original_family_pass': originals_pass, 'runtime': 'Installed dependency metadata function plus unchanged14 source-chroot cases; no installed/native Steam claim; coordinator owns consumption'}, indent=2) + '\n')
print(str(a.output))
