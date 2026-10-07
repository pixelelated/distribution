"""Capture compatibility outputs before the aarch64 stage; Python 3.10 safe."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

owner = Path(__file__).resolve().parent
tree = Path.cwd()
root = tree / 'build.pixelelated-SM8550.arm'
installed = root / 'image/system'
assert (root / '.stamps/arm/build_target').is_file() and installed.is_dir()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024**2), b''):
            h.update(block)
    return h.hexdigest()


files, links, elf = {}, {}, []
for path in sorted(installed.rglob('*')):
    name = str(path.relative_to(installed))
    if path.is_symlink():
        links[name] = os.readlink(path)
    elif path.is_file():
        files[name] = sha(path)
        with path.open('rb') as stream:
            header = stream.read(20)
        if header[:6] == b'\x7fELF\x01\x01' and header[18:20] == b'\x28\x00':
            elf.append(name)
assert 'usr/bin/retroarch' in elf and 'usr/bin/box86' in elf
assert any('libretro' in p and p.endswith('.so') for p in elf)
stamps = {str(p.relative_to(root)): sha(p) for p in sorted((root / '.stamps').rglob('build_*')) if p.is_file()}
result = dict(utc=datetime.now(timezone.utc).isoformat(), result='PASS',
              scope='SM8550 ARM compatibility outputs before aarch64 handoff',
              files=files, symlinks=links, arm_elf=elf, stamps=stamps)
with (owner / 'artifacts/arm-output-manifest.json').open('x') as out:
    json.dump(result, out, indent=2)
    out.write('\n')
print('PASS SM8550 ARM output manifest: %d files, %d ARM ELF objects' % (len(files), len(elf)), flush=True)
