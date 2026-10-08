#!/usr/bin/env python3
"""Rebuild the frozen final UI for newly identified visual branches only."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

OWNER = Path('/workspace/tmp/pixelelated-510-coverage02/build02')
SOURCE = Path('/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup')
COMMIT = 'baeea2a8c9bf508949104abcf04583a2338e054f'
commands = json.loads((OWNER / 'commands.json').read_text())
cwd = Path(commands['cwd'])
started = time.monotonic()


def run(argv, **kwargs):
    print('RUN', argv[0], argv[-2:], flush=True)
    subprocess.run(argv, check=True, cwd=cwd, **kwargs)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


assert subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip() == COMMIT
assert not subprocess.check_output(['git', '-C', str(SOURCE), 'status', '--porcelain'], text=True).strip()
old = json.loads((OWNER / 'reference-inputs.json').read_text())
inputs = {Path(e['path']) for e in old if not e['path'].startswith('/workspace/tmp/')}
core = cwd.parent / 'libes-core.a'
inputs.add(core)
inputs.add(SOURCE / 'locale/lang/fr/LC_MESSAGES/emulationstation2.po')
for e in old:
    if e['path'].startswith('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/'):
        assert sha(Path(e['path'])) == e['sha256'], 'Reused input differs from reviewed final build: ' + e['path']


def snapshot():
    return [{'path': str(p), 'sha256': sha(p), 'size': p.stat().st_size} for p in sorted(inputs)]


before = snapshot()
(OWNER / 'inputs-before.json').write_text(json.dumps(before, indent=2) + '\n')
for source, command in commands['commands'].items():
    print('COMPILING', source, flush=True)
    run(command)
copied_core = OWNER / 'libes-core.a'
shutil.copyfile(core, copied_core)
members = OWNER / 'members'
members.mkdir()
member = members / 'AsyncNotificationComponent.cpp.o'
shutil.copyfile(OWNER / 'es-core_src_components_AsyncNotificationComponent.cpp.o', member)
compiler = Path(next(iter(commands['commands'].values()))[0])
ar = compiler.with_name(compiler.name.replace('g++', 'ar'))
assert 'AsyncNotificationComponent.cpp.o' in subprocess.check_output([str(ar), 't', str(core)], text=True).splitlines()
run([str(ar), 'rcs', str(copied_core), str(member)])
with (OWNER / 'artifacts/link.log').open('w') as log:
    run(commands['link'], stdout=log, stderr=subprocess.STDOUT)
run(['msgfmt', '--check', '-o', str(OWNER / 'artifacts/fr.mo'), str(SOURCE / 'locale/lang/fr/LC_MESSAGES/emulationstation2.po')])
after = snapshot()
(OWNER / 'inputs-after.json').write_text(json.dumps(after, indent=2) + '\n')
assert after == before, 'Read-only source/build inputs changed'
assert subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip() == COMMIT
assert not subprocess.check_output(['git', '-C', str(SOURCE), 'status', '--porcelain'], text=True).strip()
outputs = [{'path': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in [OWNER / 'emulationstation', OWNER / 'artifacts/fr.mo']]
receipt = {'es_commit': COMMIT, 'kind': 'reconstructed unchanged-source overlay binary, not firmware',
           'elapsed_seconds': round(time.monotonic() - started, 3), 'compile_units': len(commands['commands']),
           'parallelism': 1, 'inputs_unchanged': len(before), 'outputs': outputs,
           'logical_footprint_bytes': sum(p.stat().st_size for p in OWNER.rglob('*') if p.is_file())}
(OWNER / 'artifacts/outputs.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS', json.dumps(receipt), flush=True)
