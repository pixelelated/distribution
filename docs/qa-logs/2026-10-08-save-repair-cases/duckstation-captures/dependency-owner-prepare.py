#!/usr/bin/env python3
"""Seed only the named isolated #523 owner; never write accepted inputs."""
from pathlib import Path
import hashlib
import json
import subprocess

owner = Path('/workspace/repos/rocknix.worktrees/m7-duckstation-deps01')
accepted = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16')
build_name = 'build.pixelelated-GENERIC_X64.x86_64'
assert Path.cwd() == owner
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == 'dda2a04aaf411b8bc13aedf5ce44ff33ce4b3d3a'
assert subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip() == 'build/m7-duckstation-deps01'
build = owner / build_name
build.mkdir()
commands = []
for name in ['toolchain', '.stamps']:
    cmd = ['cp', '-a', '--reflink=auto', str(accepted / build_name / name), str(build / name)]
    commands.append(cmd)
    subprocess.run(cmd, check=True)
    print('Seeded isolated ' + name, flush=True)
source = Path('/workspace/cache/rocknix-sources/libcom-err/libcom-err-1.47.4.tar.xz')
digest = hashlib.sha256(source.read_bytes()).hexdigest()
assert digest == 'fd5bf388cbdbe006a3d3b318d983b2948382440acc85a87f1e7d108653e8db0b'
target = owner / 'sources/libcom-err'
target.mkdir(parents=True)
for path in sorted(source.parent.glob(source.name + '*')):
    cmd = ['cp', '-a', '--reflink=auto', str(path), str(target / path.name)]
    commands.append(cmd)
    subprocess.run(cmd, check=True)
(owner / 'dependency-owner.json').write_text(json.dumps({
    'owner': str(owner), 'accepted_readonly_inputs': str(accepted),
    'source_sha256': digest, 'commands': commands,
    'scope': 'Copied toolchain/stamps and checked source only; no compilation or accepted-root mutation.'
}, indent=2) + '\n')
print('Isolated source/toolchain preparation complete.', flush=True)
