"""Freeze and prepare the authorized SM8550 build after H700 acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import subprocess

primary = Path('/workspace/repos/rocknix')
tree = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-01')
owner = Path('/workspace/tmp/pixelelated-m7-sm8550-build-01')
previous = Path('/workspace/tmp/pixelelated-m7-h700-firmware-01')
accepted = Path('/workspace/tmp/pixelelated-m7-h700-firmware-acceptance-01')
branch = 'build/m7-pixelelated-sm8550-01'


def git(*args):
    return subprocess.check_output(['git', '-C', str(primary), *args], text=True).strip()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


assert json.loads((accepted / 'owner-verification.json').read_text())['result'] == 'PASS'
assert json.loads((accepted / 'artifacts/acceptance.json').read_text())['result'] == 'PASS'
assert not tree.exists() and not owner.exists(), 'Fresh SM8550 checkout and owner required'
assert git('branch', '--show-current') == 'next'
assert not git('status', '--porcelain')
head = git('rev-parse', 'HEAD')
assert git('ls-remote', 'origin', 'refs/heads/next').split()[0] == head
j = json.loads((previous / 'inputs.json').read_text())
product = ['config', 'distributions', 'packages', 'projects', 'scripts', 'Makefile', 'LICENSE.md', 'TRADEMARK.md']
assert not git('diff', '--name-only', j['distribution_commit'], head, '--', *product)
assert sha(j['host_options_path']) == j['host_options_sha256']
s = os.statvfs('/workspace')
available = s.f_bavail * s.f_frsize
assert available >= 347688935424, available
subprocess.run(['git', '-C', str(primary), 'worktree', 'add', '-b', branch, str(tree), head], check=True)
owner.mkdir(mode=0o700)
(owner / 'artifacts').mkdir()
stamp = datetime.now(timezone.utc).isoformat()
j.update(device='SM8550', arch='aarch64', compatibility_arch='arm', distribution_commit=head,
         distribution_branch=branch, host_worktree=str(tree), container_worktree=str(tree),
         build_root='build.pixelelated-SM8550.aarch64', frozen_at=stamp,
         build_mode='cold ARM compatibility followed by cold aarch64 firmware',
         purpose='M7.P5 #492: SM8550 after accepted H700 firmware',
         arm_manifest=str(owner / 'artifacts/arm-output-manifest.json'))
j.pop('arm_manifest_sha256')
for key in ['source_files', 'qa_source_files']:
    j[key] = {name: sha(tree / name) for name in j[key]}
j['source_symlinks'] = {name: os.readlink(tree / name) for name in j['source_symlinks']}
(owner / 'inputs.json').write_text(json.dumps(j, sort_keys=True, indent=2) + '\n')

s = (previous / 'run.py').read_text().replace('H700', 'SM8550')
s = s.replace(" assert json.loads(Path('/workspace/tmp/pixelelated-m7-broad-cleanup-01/acceptance.json').read_text())['result']=='PASS'", " assert json.loads(Path('/workspace/tmp/pixelelated-m7-h700-firmware-acceptance-01/artifacts/acceptance.json').read_text())['result']=='PASS'")
s = s.replace(" assert hashlib.sha256(Path(j['arm_manifest']).read_bytes()).hexdigest()==j['arm_manifest_sha256']", " assert not (tree/'build.pixelelated-SM8550.arm').exists(), 'ARM stage must also be cold'")
s = s.replace('287480930304', '347688935424')
s = s.replace("ARCH=aarch64 CUSTOM_VERSION=0.0.1", "CUSTOM_VERSION=0.0.1")
s = s.replace("'arch':'aarch64'", "'arch':'arm+aarch64'")
s = s.replace(" assert any(n.endswith('-DDR3.img.gz') for n in outputs),list(outputs)\n assert any(n.endswith('-DDR4.img.gz') for n in outputs),list(outputs)", " assert len([n for n in outputs if n.endswith('.img.gz')])==1,list(outputs)")
s = s.replace(" receipt={'utc':", " assert Path(j['arm_manifest']).is_file()\n receipt={'arm_manifest_sha256':hashlib.sha256(Path(j['arm_manifest']).read_bytes()).hexdigest(),'utc':")
ast.parse(s)
(owner / 'run.py').write_text(s)
(owner / 'verify-source.py').write_text((previous / 'verify-source.py').read_text().replace(str(previous), str(owner)))
(owner / 'inside-build.sh').write_text('#!/bin/bash\nset -euo pipefail\nexport ARCH=arm\n./scripts/build_distro\npython3 -I ' + str(owner / 'record-arm.py') + '\nexport ARCH=aarch64\n./scripts/build_distro\n')
(owner / 'record-arm.py').write_bytes(Path(__file__).with_name('record-arm.py').read_bytes())
subprocess.run(['bash', '-n', str(owner / 'inside-build.sh')], check=True)
subprocess.run(['python3', '-I', str(owner / 'verify-source.py')], cwd=tree, check=True)
receipt = dict(utc=stamp, distribution_commit=head, branch=branch,
               inputs_sha256=sha(owner / 'inputs.json'),
               h700_product_equivalent=True, h700_accepted=True,
               available_bytes=available, stage_required_bytes=347688935424,
               container=j['container'], global_jobs=24, webkit_jobs=4,
               scope='Prepared only; guarded host preflight precedes watched submission')
(owner / 'freeze-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
names = ['inputs.json', 'run.py', 'verify-source.py', 'inside-build.sh', 'record-arm.py', 'freeze-receipt.json']
(owner / 'seal.json').write_text(json.dumps({str(owner / n): sha(owner / n) for n in names}, indent=2) + '\n')
print(json.dumps(receipt), flush=True)
