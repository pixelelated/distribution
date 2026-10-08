from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
O=Path(__file__).resolve().parent;j=json.loads((O/'inputs.json').read_text());T=Path(j['host_worktree'])
assert Path.cwd()==T
(O/'run.path').write_text(str(T/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1;observer=None
try:
 for n,h in json.loads((O/'build-seal.json').read_text()).items():assert hashlib.sha256(Path(n).read_bytes()).hexdigest()==h,n
 assert not subprocess.check_output(['git','status','--porcelain'],text=True).strip()
 assert json.loads((O/'cache-consumption.json').read_text())['result']=='PASS'
 assert json.loads((O/'cache-ready.json').read_text())['result']=='PASS'
 s=os.statvfs('/workspace');free=s.f_bavail*s.f_frsize;assert free>=300*1024**3
 (O/'build-capacity.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'available_bytes':free,'build_reserve_bytes':300*1024**3,'result':'PASS'},indent=2)+'\n')
 subprocess.run(['python3','-I',str(O/'verify-source.py')],check=True)
 subprocess.run(['tools/rc-preflight','--only','proxy-schema'],check=True)
 subprocess.run(['tools/build-preflight'],check=True)
 env=dict(os.environ)
 for n in ['EMULATIONSTATION_SRC','DEVICE_ROOT','PACKAGE','PROJECT','DEVICE','ARCH','CUSTOM_GIT_HASH','CUSTOM_VERSION','CUSTOM_IMAGE_NAME','DIRTY','BASE_ONLY']:env.pop(n,None)
 env.update(DOCKER_WORK_DIR=j['container_worktree'],DOCKER_EXTRA_OPTS='-v /workspace/repos/rocknix/.git:/workspace/repos/rocknix/.git -v '+j['source_cache']+':'+j['container_worktree']+'/sources',CONCURRENCY_MAKE_LEVEL='24',CUSTOM_VERSION='0.0.1')
 for package in ['rclone','emulationstation','duckstation-sa','rocknix']:
  pe=dict(env,PROJECT='ROCKNIX',DEVICE='SM8550',ARCH='aarch64',PACKAGE=package)
  subprocess.run(['make','docker-package-clean'],env=pe,check=True)
 (T/j['build_root']/'.stamps/image/build_target').unlink(missing_ok=True)
 env['DOCKER_EXTRA_OPTS']+=' -v '+str(O)+':'+str(O)+' -v '+j['nix_private_store']+':/nix -v '+j['nix_snapshot']+':'+j['nix_snapshot']+':ro'
 env['DOCKER_EXTRA_OPTS']+=' --name pixelelated-m7-sm8550-refresh02 --label pixelelated.m7.owner=sm8550-refresh02 --cidfile '+str(O/'build.cid')
 observer=subprocess.Popen(['python3','-I','-u',str(O/'observe-container.py')]);(O/'observer.pid').write_text(str(observer.pid)+'\n')
 (O/'artifacts/command.json').write_text(json.dumps({'command':['make','docker-SM8550','COMMAND=bash '+str(O/'inside-build.sh')], 'inside_command':['make','SM8550'],'cwd':str(T),'container_worktree':j['container_worktree'],'device':'SM8550','arches':['arm','aarch64'],'container':j['container'],'global_jobs':24,'webkit_jobs':4,'scope':'canonical target, independent verified warm roots and affected-package clean'},indent=2)+'\n')
 subprocess.run(['make','docker-SM8550','COMMAND=bash '+str(O/'inside-build.sh')],env=env,check=True)
 assert json.loads((O/'artifacts/container-gate.json').read_text())['result']=='PASS'
 assert json.loads((O/'artifacts/fex-package.json').read_text())['result']=='PASS'
 assert observer.wait()==0;observer=None
 subprocess.run(['python3','-I',str(O/'verify-source.py')],check=True)
 subprocess.run(['python3','-I',str(O/'verify-installed.py')],check=True)
 outputs={}
 for p in sorted((T/'target').iterdir()):
  if p.is_file() and p.name.startswith('pixelelated-SM8550.aarch64-'):
   with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
   outputs[p.name]={'path':str(p),'bytes':p.stat().st_size,'sha256':h}
 assert len([n for n in outputs if n.endswith('.img.gz')])==1 and len([n for n in outputs if n.endswith('.tar')])==1
 (O/'artifacts/output-manifest.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'BUILT_REQUIRES_ARTIFACT_ACCEPTANCE','distribution_commit':j['distribution_commit'],'files':outputs,'arm_manifest_sha256':hashlib.sha256(Path(j['arm_manifest']).read_bytes()).hexdigest()},indent=2)+'\n')
 print('BUILT SM8550; installed inclusion passed; independent raw/update acceptance follows',flush=True);rc=0
except subprocess.CalledProcessError as e:
 rc=e.returncode if e.returncode>0 else 128-e.returncode;print('FAILED command rc',rc,flush=True)
finally:
 if observer is not None and observer.poll() is None:observer.terminate();observer.wait()
 (O/'inner.rc').write_text(str(rc)+'\n');(O/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
