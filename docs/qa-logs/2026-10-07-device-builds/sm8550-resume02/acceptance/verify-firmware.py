"""Read-only SM8550 firmware acceptance; scratch disks are removed after proof."""
from pathlib import Path
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import tarfile

owner = Path(__file__).resolve().parent
build_owner = Path('/workspace/tmp/pixelelated-m7-sm8550-build-02')
inputs = json.loads((build_owner / 'inputs.json').read_text())
tree = Path(inputs['host_worktree'])
root = tree / inputs['build_root']
outputs = json.loads((build_owner / 'artifacts/output-manifest.json').read_text())


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def cat(system, name):
    return subprocess.check_output(['unsquashfs', '-cat', str(system), name])


files = [Path(r['path']) for r in outputs['files'].values() if r['path'].endswith(('.img.gz', '.tar', '.sha256'))]
for path in files:
    assert digest(path) == outputs['files'][path.name]['sha256'], path
    if path.name.endswith('.sha256'):
        parts = path.read_text().split()
        assert len(parts) == 2 and Path(parts[1]).name == path.name.removesuffix('.sha256')
        assert digest(path.with_name(parts[1])) == parts[0]
images = [p for p in files if p.name.endswith('.img.gz')]
archives = [p for p in files if p.name.endswith('.tar')]
assert len(images) == 1 and len(archives) == 1
subprocess.run(['python3', '-I', str(build_owner / 'verify-source.py')], cwd=tree, check=True)

store = Path('/workspace/artifacts/pixelelated-candidates')
command = [str(tree / 'tools/rasteratops-candidate-store'), 'put', '--store', str(store), '--inputs', str(build_owner / 'inputs.json'), *map(str, files)]
log = subprocess.check_output(command, cwd=tree, text=True)
(owner / 'artifacts/candidate-store.log').write_text(log)
bundle = Path([line.removeprefix('PASS candidate bundle ') for line in log.splitlines() if line.startswith('PASS candidate bundle ')][-1])
assert bundle.parent == store / 'sha256'
manifest = json.loads((bundle / 'manifest.json').read_text())
for path in files:
    copied = bundle / path.name
    assert digest(copied) == digest(path)
    assert (copied.stat().st_dev, copied.stat().st_ino) != (path.stat().st_dev, path.stat().st_ino)
(owner / 'candidate-bundle.path').write_text(str(bundle) + '\n')

scratch = owner / 'scratch'
scratch.mkdir()
system = scratch / 'SYSTEM'
archive = bundle / archives[0].name
with tarfile.open(archive) as tf:
    members = tf.getnames()
    names = [n for n in members if n.endswith('/target/SYSTEM')]
    assert len(names) == 1
    with tf.extractfile(names[0]) as src, system.open('xb') as dst:
        shutil.copyfileobj(src, dst, 4 * 1024**2)
    kernel = [n for n in members if n.endswith('/target/KERNEL')]
    assert len(kernel) == 1
    with tf.extractfile(kernel[0]) as src:
        kernel_hash = hashlib.file_digest(src, 'sha256').hexdigest()
    boot_files = {}
    prefix = '/3rdparty/bootloader/'
    for member in tf.getmembers():
        if member.isfile() and prefix in member.name:
            relative = member.name.split(prefix, 1)[1]
            if relative.startswith('rocknix_abl/'):
                assert '..' not in Path(relative).parts
                with tf.extractfile(member) as src:
                    boot_files[relative] = hashlib.file_digest(src, 'sha256').hexdigest()
    assert any(n.endswith('/abl_signed-SM8550.elf') for n in boot_files)
system_hash = digest(system)
release = cat(system, 'etc/os-release').decode()
(owner / 'artifacts/os-release').write_text(release)
values = dict(line.split('=', 1) for line in release.splitlines() if '=' in line)
values = {k: v.strip('"') for k, v in values.items()}
for k, v in dict(OS_NAME='pixelelated', OS_VERSION='0.0.1', BUILD_ID=inputs['distribution_commit'],
                 BUILD_BRANCH=inputs['distribution_branch'], HW_DEVICE='SM8550', HW_ARCH='aarch64',
                 BUILDER_VERSION=inputs['container'].split('@')[1]).items():
    assert values[k] == v, (k, values.get(k), v)
architecture = []
for name in ['usr/bin/emulationstation', 'usr/bin/retroarch']:
    content = cat(system, name)
    assert content[:6] == b'\x7fELF\x02\x01' and content[18:20] == b'\xb7\x00', name
    architecture.append(dict(path=name, arch='aarch64', sha256=hashlib.sha256(content).hexdigest()))
assert digest(inputs['arm_manifest']) == outputs['arm_manifest_sha256']
arm = json.loads(Path(inputs['arm_manifest']).read_text())
assert arm['result'] == 'PASS'
handoff = []
mapping = {'usr/bin/retroarch': 'usr/bin/retroarch32', 'usr/bin/box86': 'usr/bin/box86',
           'usr/lib/libretro/gpsp_libretro.so': 'usr/lib/libretro/gpsp_libretro.so',
           'usr/lib/libretro/desmume_libretro.so': 'usr/lib/libretro/desmume_libretro.so'}
for src, target in mapping.items():
    content = cat(system, target)
    sha = hashlib.sha256(content).hexdigest()
    assert content[:6] == b'\x7fELF\x01\x01' and content[18:20] == b'\x28\x00', target
    assert sha == arm['files'][src], (target, 'ARM handoff byte mismatch')
    handoff.append(dict(source=src, installed=target, sha256=sha, arch='arm'))
lib32 = [n for n in arm['files'] if n.startswith('usr/lib/') and '/' not in n.removeprefix('usr/lib/') and '.so' in n]
assert lib32
for src in lib32:
    target = src.replace('usr/lib/', 'usr/lib32/', 1)
    content = cat(system, target)
    assert hashlib.sha256(content).hexdigest() == arm['files'][src], target
    handoff.append(dict(source=src, installed=target, sha256=arm['files'][src], arch='arm-library'))
(owner / 'artifacts/arm-handoff.json').write_text(json.dumps(handoff, indent=2) + '\n')
equality = []
mcopy = root / 'toolchain/bin/mcopy'
for image in images:
    image = bundle / image.name
    variant = 'SM8550'
    raw = scratch / (variant + '.img')
    with gzip.open(image, 'rb') as src, raw.open('xb') as dst:
        while block := src.read(4 * 1024**2):
            if block.count(0) == len(block):
                dst.seek(len(block), 1)
            else:
                dst.write(block)
        dst.truncate()
    partition_json = json.loads(subprocess.check_output(['/usr/sbin/sfdisk', '--json', str(raw)], text=True))
    table = partition_json['partitiontable']
    assert table['label'] == 'gpt' and table['unit'] == 'sectors' and table['sectorsize'] == 512
    assert len(table['partitions']) == 2
    first_partition = table['partitions'][0]
    first, sectors = first_partition['start'], first_partition['size']
    assert first >= 2048 and sectors > 0 and first_partition['name'] == 'system'
    assert table['partitions'][1]['name'] == 'storage'
    (owner / 'artifacts/partition-table.json').write_text(json.dumps(partition_json, indent=2) + '\n')
    for name, expected in boot_files.items():
        copy = scratch / 'boot-file'
        subprocess.run([str(mcopy), '-i', str(raw) + '@@' + str(first * 512), '::/' + name, str(copy)], check=True)
        assert digest(copy) == expected, name
        copy.unlink()
    extracted = scratch / (variant + '-SYSTEM')
    subprocess.run([str(mcopy), '-i', str(raw) + '@@' + str(first * 512), '::/SYSTEM', str(extracted)], check=True)
    assert digest(extracted) == system_hash
    # config/options defaults KERNEL_NAME to KERNEL; SM8550 sets KERNEL_TARGET=Image.
    kernel_file = scratch / (variant + '-KERNEL')
    subprocess.run([str(mcopy), '-i', str(raw) + '@@' + str(first * 512), '::/KERNEL', str(kernel_file)], check=True)
    assert digest(kernel_file) == kernel_hash
    row = dict(image=image.name, variant=variant, system_sha256=system_hash, kernel_sha256=kernel_hash,
               bootloader_files=boot_files, first_sector=first,
               raw_sha256=digest(raw), raw_bytes=raw.stat().st_size)
    equality.append(row)
    for path in [raw, extracted, kernel_file]:
        path.unlink()
    print('PASS SM8550 ' + variant + ' raw/update SYSTEM, kernel and exact ABL files; scratch removed', flush=True)
(owner / 'artifacts/payload-equality.json').write_text(json.dumps(equality, indent=2) + '\n')

fex_proof=json.loads((build_owner/'artifacts/fex-package.json').read_text())
assert fex_proof['result']=='PASS'
fex_installed=[]
for entry in fex_proof['files']:
    content=cat(system,entry['path'])
    assert hashlib.sha256(content).hexdigest()==entry['sha256'],entry['path']
    assert int.from_bytes(content[18:20],'little')==entry['machine'],entry['path']
    fex_installed.append(entry)
(owner/'artifacts/fex-installed.json').write_text(json.dumps({'result':'PASS','files':fex_installed,'package_proof_sha256':digest(build_owner/'artifacts/fex-package.json')},indent=2)+'\n')
subprocess.run(['python3','-I',str(build_owner/'verify-arm.py')],check=True)

system.unlink()
assert not list(scratch.iterdir())
scratch.rmdir()
subprocess.run([str(tree / 'tools/rasteratops-candidate-store'), 'verify', str(bundle)], check=True)
receipt = dict(utc=datetime.now(timezone.utc).isoformat(), result='PASS', scope='SM8550 firmware artifacts; no physical boot/smoke or RC/publication claim',
               bundle=str(bundle), bundle_manifest_sha256=digest(bundle / 'manifest.json'),
               distribution_commit=inputs['distribution_commit'], architecture=architecture,
               arm_handoff_files=len(handoff), variants=equality, scratch_removed=True,
               source_unchanged=True, independent_bundle_inodes=True)
(owner / 'artifacts/acceptance.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS SM8550 firmware artifact acceptance', flush=True)
