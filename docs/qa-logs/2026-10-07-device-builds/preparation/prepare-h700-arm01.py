"""Freeze the authorized #492 H700 arm build after accepted #491 cleanup."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, subprocess

repo = Path('/workspace/repos/rocknix')
coord = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
tree = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01')
owner = Path('/workspace/tmp/pixelelated-m7-h700-arm-01')
cleanup = Path('/workspace/tmp/pixelelated-m7-h700-qa-retirement-01')
sizing = Path('/workspace/tmp/pixelelated-m7-storage-sizing-02')
proposal = coord / 'docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-retirement-proposal/proposal.json'

def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()

assert git('branch', '--show-current') == 'next' and not git('status', '--porcelain')
assert not tree.exists() and not owner.exists()
for p in [cleanup, sizing]:
    assert json.loads((p / 'owner-verification.json').read_text())['result'] == 'PASS'
assert json.loads((cleanup / 'acceptance.json').read_text())['result'] == 'PASS'
assert len(json.loads((cleanup / 'execution.json').read_text())['removed']) == 22
assert (coord / '.build-runs/h700-host-preflight.rc').read_text().strip() == '0'
base = json.loads(Path('/workspace/tmp/pixelelated-m7-replacement-16/inputs.json').read_text())
head = git('rev-parse', 'HEAD')
paths = ['config', 'distributions', 'packages', 'projects', 'scripts', 'Makefile']
assert not git('diff', '--name-only', base['distribution_commit'], head, '--', *paths)
required = json.loads(proposal.read_text())['builds'][0]['required_bytes']
fs = os.statvfs('/workspace'); available = fs.f_bavail * fs.f_frsize
assert available >= required + 1024**3, (available, required)
assert hashlib.sha256(Path(base['host_options_path']).read_bytes()).hexdigest() == base['host_options_sha256']
assert subprocess.check_output(['docker', 'image', 'inspect', base['container'], '--format', '{{.Id}}'], text=True).strip() == base['container_image_id']
branch = 'build/m7-pixelelated-h700-01'
subprocess.run(['git', '-C', str(repo), 'worktree', 'add', str(tree), '-b', branch, head], check=True)
fs = os.statvfs('/workspace'); available_after_checkout = fs.f_bavail * fs.f_frsize
assert available_after_checkout >= required, (available_after_checkout, required)
owner.mkdir(mode=0o700)
(owner / 'artifacts').mkdir()
j = {k: v for k, v in base.items() if not k.startswith('cache_parent_')}
j.update(distribution_commit=head, distribution_branch=branch, host_worktree=str(tree),
         container_worktree=str(tree), device='H700', arch='arm',
         build_root='build.pixelelated-H700.arm',
         build_mode='cold independent H700 arm compatibility root; shared downloads only',
         frozen_at=datetime.now(timezone.utc).isoformat(),
         qualified_product_commit=base['distribution_commit'],
         purpose='M7.P5 #492: H700 compatibility first, firmware after capacity review; SM8550 next')
for key in ['source_files', 'qa_source_files']:
    j[key] = {p: hashlib.sha256((tree / p).read_bytes()).hexdigest() for p in base[key]}
j['source_symlinks'] = {p: os.readlink(tree / p) for p in base['source_symlinks']}
(owner / 'inputs.json').write_text(json.dumps(j, sort_keys=True, indent=2) + '\n')
(owner / 'capacity.json').write_text(json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
    'available_before_checkout_bytes': available, 'required_arm_bytes': required,
    'available_after_checkout_bytes': available_after_checkout,
    'checkout_allowance_bytes': 1024**3, 'proposal': str(proposal),
    'cleanup_acceptance_sha256': hashlib.sha256((cleanup / 'acceptance.json').read_bytes()).hexdigest(),
    'scope': 'H700 arm only; does not establish aarch64 or SM8550 fit'}, indent=2) + '\n')
verify = Path('/workspace/tmp/pixelelated-m7-replacement-16/verify-source.py').read_text()
verify = verify.replace('pixelelated-m7-replacement-16', 'pixelelated-m7-h700-arm-01')
(owner / 'verify-source.py').write_text(verify)
run = '''from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
j=json.loads((owner/'inputs.json').read_text());tree=Path(j['host_worktree'])
assert Path.cwd()==tree
(owner/'run.path').write_text(str(tree/os.environ['RASTERATOPS_BUILD_RUN'])+'\\n')
rc=1
try:
 for name,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==sha
 assert not subprocess.check_output(['git','status','--porcelain'],text=True).strip()
 assert not (tree/j['build_root']).exists()
 subprocess.run(['python3','-I',str(owner/'verify-source.py')],check=True)
 subprocess.run(['tools/rc-preflight','--only','proxy-schema'],check=True)
 subprocess.run(['tools/build-preflight'],check=True)
 env=dict(os.environ)
 for name in ['EMULATIONSTATION_SRC','DEVICE_ROOT','PACKAGE','PROJECT','DEVICE','ARCH','CUSTOM_GIT_HASH','CUSTOM_VERSION','CUSTOM_IMAGE_NAME','DIRTY','BASE_ONLY']:
  env.pop(name,None)
 env.update(DOCKER_WORK_DIR=str(tree),DOCKER_EXTRA_OPTS='-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v '+j['source_cache']+':'+str(tree)+'/sources',CONCURRENCY_MAKE_LEVEL=str(j['global_jobs']))
 command=['make','docker-H700','COMMAND=env -u DEVICE_ROOT PROJECT=ROCKNIX DEVICE=H700 ARCH=arm ./scripts/build_distro']
 (owner/'artifacts/command.json').write_text(json.dumps({'command':command,'cwd':str(tree),'device':'H700','arch':'arm','container':j['container'],'global_jobs':j['global_jobs']},indent=2)+'\\n')
 subprocess.run(command,env=env,check=True)
 subprocess.run(['python3','-I',str(owner/'verify-source.py')],check=True)
 build=tree/j['build_root'];assert (build/'.stamps/arm/build_target').is_file()
 installed=build/'image/system';assert installed.is_dir()
 files={};links={};arm_elf=[]
 for p in sorted(installed.rglob('*')):
  name=str(p.relative_to(installed))
  if p.is_symlink():links[name]=os.readlink(p)
  elif p.is_file():
   files[name]=hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
   with p.open('rb') as f:header=f.read(20)
   if header[:5]==b'\\x7fELF\\x01' and header[18:20]==b'\\x28\\x00':arm_elf.append(name)
 assert arm_elf and files
 stamps={str(p.relative_to(build)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((build/'.stamps').rglob('build_*')) if p.is_file()}
 payload={'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','scope':'H700 arm compatibility output only; no firmware image or physical boot claim','files':files,'symlinks':links,'arm_elf':arm_elf,'stamps':stamps}
 (owner/'artifacts/output-manifest.json').write_text(json.dumps(payload,indent=2)+'\\n')
 print('PASS H700 arm compatibility output: '+str(len(files))+' files, '+str(len(arm_elf))+' ARM ELF objects, '+str(len(stamps))+' build stamps',flush=True)
 rc=0
except subprocess.CalledProcessError as e:
 rc=e.returncode if e.returncode>0 else 128-e.returncode
 print('FAILED command with exit '+str(rc),flush=True)
finally:
 (owner/'inner.rc').write_text(str(rc)+'\\n');(owner/'outer.rc').write_text(str(rc)+'\\n')
sys.exit(rc)
'''
ast.parse(run)
(owner / 'run.py').write_text(run)
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'commit': head, 'branch': branch,
           'qualified_product': base['distribution_commit'], 'product_paths_equal': paths,
           'inputs_sha256': hashlib.sha256((owner / 'inputs.json').read_bytes()).hexdigest(),
           'source_files': len(j['source_files']), 'qa_source_files': len(j['qa_source_files']),
           'source_symlinks': len(j['source_symlinks']), 'container': j['container'],
           'container_image_id': j['container_image_id'], 'global_jobs': j['global_jobs'],
           'webkit_jobs': j['webkit_jobs'], 'scope': 'prepared, not submitted'}
(owner / 'freeze-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
subprocess.run(['python3', '-I', str(owner / 'verify-source.py')], cwd=tree, check=True)
names = ['inputs.json', 'capacity.json', 'verify-source.py', 'run.py', 'freeze-receipt.json']
(owner / 'seal.json').write_text(json.dumps({str(owner / n): hashlib.sha256((owner / n).read_bytes()).hexdigest() for n in names}, indent=2) + '\n')
print(json.dumps(receipt))
