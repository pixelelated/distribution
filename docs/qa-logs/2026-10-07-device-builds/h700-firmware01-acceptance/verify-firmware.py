"""Read-only H700 firmware acceptance; scratch disks are removed after proof."""
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
build_owner = Path('/workspace/tmp/pixelelated-m7-h700-firmware-01')
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
assert len(images) == 2 and len(archives) == 1
assert {re.search(r'-(DDR[34])\.img\.gz$', p.name).group(1) for p in images} == {'DDR3', 'DDR4'}
assert len({digest(p) for p in images}) == 2
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
    bootloaders = {}
    for variant in ['DDR3', 'DDR4']:
        name = next(n for n in members if n.endswith('/3rdparty/bootloader/H700_' + variant + '_u-boot-sunxi-with-spl.bin'))
        bootloaders[variant] = tf.extractfile(name).read()
assert bootloaders['DDR3'] != bootloaders['DDR4']
system_hash = digest(system)
release = cat(system, 'etc/os-release').decode()
(owner / 'artifacts/os-release').write_text(release)
values = dict(line.split('=', 1) for line in release.splitlines() if '=' in line)
values = {k: v.strip('"') for k, v in values.items()}
for k, v in dict(OS_NAME='pixelelated', OS_VERSION='0.0.1', BUILD_ID=inputs['distribution_commit'],
                 BUILD_BRANCH=inputs['distribution_branch'], HW_DEVICE='H700', HW_ARCH='aarch64',
                 BUILDER_VERSION=inputs['container'].split('@')[1]).items():
    assert values[k] == v, (k, values.get(k), v)
architecture = []
for name in ['usr/bin/emulationstation', 'usr/bin/retroarch']:
    content = cat(system, name)
    assert content[:6] == b'\x7fELF\x02\x01' and content[18:20] == b'\xb7\x00', name
    architecture.append(dict(path=name, arch='aarch64', sha256=hashlib.sha256(content).hexdigest()))
arm = json.loads(Path(inputs['arm_manifest']).read_text())
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
    variant = re.search(r'-(DDR[34])\.img\.gz$', image.name).group(1)
    raw = scratch / (variant + '.img')
    with gzip.open(image, 'rb') as src, raw.open('xb') as dst:
        while block := src.read(4 * 1024**2):
            if block.count(0) == len(block):
                dst.seek(len(block), 1)
            else:
                dst.write(block)
        dst.truncate()
    with raw.open('rb') as stream:
        mbr = stream.read(512)
        assert mbr[-2:] == b'\x55\xaa'
        first, sectors = struct.unpack_from('<II', mbr, 446 + 8)
        assert mbr[446 + 4] in [0x0b, 0x0c] and first >= 2048 and sectors > 0
        stream.seek(8192)
        assert stream.read(len(bootloaders[variant])) == bootloaders[variant]
    extracted = scratch / (variant + '-SYSTEM')
    subprocess.run([str(mcopy), '-i', str(raw) + '@@' + str(first * 512), '::/SYSTEM', str(extracted)], check=True)
    assert digest(extracted) == system_hash
    # config/options defaults KERNEL_NAME to KERNEL; H700 only sets KERNEL_TARGET=Image.
    kernel_file = scratch / (variant + '-KERNEL')
    subprocess.run([str(mcopy), '-i', str(raw) + '@@' + str(first * 512), '::/KERNEL', str(kernel_file)], check=True)
    assert digest(kernel_file) == kernel_hash
    row = dict(image=image.name, variant=variant, system_sha256=system_hash, kernel_sha256=kernel_hash,
               bootloader_sha256=hashlib.sha256(bootloaders[variant]).hexdigest(), first_sector=first,
               raw_sha256=digest(raw), raw_bytes=raw.stat().st_size)
    equality.append(row)
    for path in [raw, extracted, kernel_file]:
        path.unlink()
    print('PASS H700 ' + variant + ' raw/update SYSTEM, kernel and exact bootloader; scratch removed', flush=True)
(owner / 'artifacts/payload-equality.json').write_text(json.dumps(equality, indent=2) + '\n')
system.unlink()
assert not list(scratch.iterdir())
scratch.rmdir()
subprocess.run([str(tree / 'tools/rasteratops-candidate-store'), 'verify', str(bundle)], check=True)
receipt = dict(utc=datetime.now(timezone.utc).isoformat(), result='PASS', scope='H700 firmware artifacts; no physical boot/smoke or RC/publication claim',
               bundle=str(bundle), bundle_manifest_sha256=digest(bundle / 'manifest.json'),
               distribution_commit=inputs['distribution_commit'], architecture=architecture,
               arm_handoff_files=len(handoff), variants=equality, scratch_removed=True,
               source_unchanged=True, independent_bundle_inodes=True)
(owner / 'artifacts/acceptance.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS H700 firmware artifact acceptance', flush=True)
