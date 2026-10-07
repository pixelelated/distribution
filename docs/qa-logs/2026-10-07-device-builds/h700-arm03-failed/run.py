from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
owner=Path(__file__).resolve().parent
j=json.loads((owner/'inputs.json').read_text());tree=Path(j['host_worktree'])
assert Path.cwd()==tree
(owner/'run.path').write_text(str(tree/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for name,sha in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==sha
 assert not subprocess.check_output(['git','status','--porcelain'],text=True).strip()
 assert (tree/j['build_root']).is_dir()
 subprocess.run(['python3','-I',str(owner/'verify-source.py')],check=True)
 subprocess.run(['tools/rc-preflight','--only','proxy-schema'],check=True)
 subprocess.run(['tools/build-preflight'],check=True)
 env=dict(os.environ)
 for name in ['EMULATIONSTATION_SRC','DEVICE_ROOT','PACKAGE','PROJECT','DEVICE','ARCH','CUSTOM_GIT_HASH','CUSTOM_VERSION','CUSTOM_IMAGE_NAME','DIRTY','BASE_ONLY']:
  env.pop(name,None)
 env.update(DOCKER_WORK_DIR=str(tree),DOCKER_EXTRA_OPTS='-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v '+j['source_cache']+':'+str(tree)+'/sources -v '+str(owner)+':'+str(owner),CONCURRENCY_MAKE_LEVEL=str(j['global_jobs']))
 command=['make','docker-H700','COMMAND=env -u DEVICE_ROOT PROJECT=ROCKNIX DEVICE=H700 ARCH=arm bash /workspace/tmp/pixelelated-m7-h700-arm-03/inside-build.sh']
 (owner/'artifacts/command.json').write_text(json.dumps({'command':command,'cwd':str(tree),'device':'H700','arch':'arm','container':j['container'],'global_jobs':j['global_jobs']},indent=2)+'\n')
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
   if header[:5]==b'\x7fELF\x01' and header[18:20]==b'\x28\x00':arm_elf.append(name)
 assert arm_elf and files
 stamps={str(p.relative_to(build)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((build/'.stamps').rglob('build_*')) if p.is_file()}
 payload={'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS','scope':'H700 arm compatibility output only; no firmware image or physical boot claim','files':files,'symlinks':links,'arm_elf':arm_elf,'stamps':stamps}
 (owner/'artifacts/output-manifest.json').write_text(json.dumps(payload,indent=2)+'\n')
 print('PASS H700 arm compatibility output: '+str(len(files))+' files, '+str(len(arm_elf))+' ARM ELF objects, '+str(len(stamps))+' build stamps',flush=True)
 rc=0
except subprocess.CalledProcessError as e:
 rc=e.returncode if e.returncode>0 else 128-e.returncode
 print('FAILED command with exit '+str(rc),flush=True)
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
