from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
j=json.loads((owner/'inputs.json').read_text());tree=Path(j['host_worktree'])
assert Path.cwd()==tree
(owner/'run.path').write_text(str(tree/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for name,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==sha,name
 assert not subprocess.check_output(['git','status','--porcelain'],text=True).strip()
 assert (tree/j['build_root']).is_dir()
 assert json.loads(Path(j['recovery_receipt']).read_text())['result']=='PASS'
 subprocess.run(['python3','-I',str(owner/'verify-arm.py')],check=True)
 assert json.loads(Path('/workspace/tmp/pixelelated-m7-h700-firmware-acceptance-01/artifacts/acceptance.json').read_text())['result']=='PASS'
 assert json.loads(Path('/workspace/tmp/pixelelated-m7-broad-cleanup-01/owner-verification.json').read_text())['result']=='PASS'
 assert hashlib.sha256(Path(j['arm_manifest']).read_bytes()).hexdigest()==j['arm_manifest_sha256']
 s=os.statvfs('/workspace');free=s.f_bavail*s.f_frsize;assert free>=347688935424,free
 (owner/'capacity.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'available_bytes':free,'stage_required_bytes':347688935424,'result':'PASS'},indent=2)+'\n')
 subprocess.run(['python3','-I',str(owner/'verify-source.py')],check=True)
 subprocess.run(['tools/rc-preflight','--only','proxy-schema'],check=True)
 subprocess.run(['tools/build-preflight'],check=True)
 env=dict(os.environ)
 for name in ['EMULATIONSTATION_SRC','DEVICE_ROOT','PACKAGE','PROJECT','DEVICE','ARCH','CUSTOM_GIT_HASH','CUSTOM_VERSION','CUSTOM_IMAGE_NAME','DIRTY','BASE_ONLY']:
  env.pop(name,None)
 env.update(DOCKER_WORK_DIR=str(tree),DOCKER_EXTRA_OPTS='-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v '+j['source_cache']+':'+str(tree)+'/sources -v '+str(owner)+':'+str(owner)+' -v '+j['nix_private_store']+':/nix -v '+j['nix_snapshot']+':'+j['nix_snapshot']+':ro',CONCURRENCY_MAKE_LEVEL=str(j['global_jobs']))
 command=['make','docker-SM8550','COMMAND=env -u DEVICE_ROOT PROJECT=ROCKNIX DEVICE=SM8550 ARCH=aarch64 CUSTOM_VERSION=0.0.1 bash '+str(owner/'inside-build.sh')]
 (owner/'artifacts/command.json').write_text(json.dumps({'command':command,'cwd':str(tree),'device':'SM8550','arch':'aarch64; accepted ARM carried forward','container':j['container'],'global_jobs':j['global_jobs']},indent=2)+'\n')
 subprocess.run(command,env=env,check=True)
 subprocess.run(['python3','-I',str(owner/'verify-source.py')],check=True)
 outputs={}
 for p in sorted((tree/'target').iterdir()):
  if p.is_file() and p.name.startswith('pixelelated-SM8550.aarch64-'):
   with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
   outputs[p.name]={'path':str(p),'bytes':p.stat().st_size,'sha256':h}
 assert len([n for n in outputs if n.endswith('.img.gz')])==1,list(outputs)
 assert any(n.endswith('.tar') for n in outputs),list(outputs)
 subprocess.run(['python3','-I',str(owner/'verify-arm.py')],check=True)
 assert json.loads((owner/'artifacts/fex-package.json').read_text())['result']=='PASS'
 assert json.loads((owner/'artifacts/proof-controls.json').read_text())['result']=='PASS'
 assert json.loads((owner/'artifacts/container-gate.json').read_text())['result']=='PASS'
 assert Path(j['arm_manifest']).is_file()
 receipt={'arm_manifest_sha256':hashlib.sha256(Path(j['arm_manifest']).read_bytes()).hexdigest(),'utc':datetime.now(timezone.utc).isoformat(),'result':'BUILT_REQUIRES_ARTIFACT_ACCEPTANCE','distribution_commit':j['distribution_commit'],'files':outputs,'scope':'Compiler/output completion only; raw-update payload, architecture/identity, independent custody and physical testing remain separate.'}
 (owner/'artifacts/output-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print('BUILT SM8550 outputs; independent artifact acceptance follows',flush=True)
 rc=0
except subprocess.CalledProcessError as e:
 rc=e.returncode if e.returncode>0 else 128-e.returncode
 print('FAILED command with exit '+str(rc),flush=True)
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
