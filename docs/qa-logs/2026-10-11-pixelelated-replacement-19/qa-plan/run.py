from pathlib import Path
import json,os,subprocess,hashlib,socket
p=Path(__file__).resolve().parent;r=Path.cwd();accept=Path('/workspace/tmp/pixelelated-m7-image19')
assert json.loads((accept/'launcher-result.json').read_text())['runner_returncode']==0
bundle=Path((accept/'bundle.path').read_text().strip());image=next(bundle.glob('*.img.gz'))
(p/'run.path').write_text(str(r/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
env={**os.environ,'TMPDIR':str(p/'tmp'),'VM_PAIR_DIR':str(p/'pair'),'CLOUD_QA_STATE':str(p/'cloud'),'ROCKNIX_ARTIFACTS':str(p/'artifacts'),'CLOUD_QA_BACKEND':'webdav','CLOUD_QA_NAME':'pixelelated-m7-qa19-s3','ES_SRC':'/home/max/Development/emulationstation-next.worktrees/qa-integration','RETROARCH_SRC':str(r/'build.pixelelated-GENERIC_X64.x86_64'),'QA_SYSTEM_ROOT':str(accept/'root'),'WALK_BASELINE':'/workspace/artifacts/rocknix-images/walk-baseline','PYTHONDONTWRITEBYTECODE':'1','PATH':str(p/'bin')+':'+os.environ['PATH']}
subprocess.run(['python3',str(p/'preflight.py')],env=env,check=True)
subprocess.run(['tools/rasteratops-candidate-store','verify',str(bundle)],env=env,check=True)
rows=[]
def step(name,cmd):
 print('START',name,flush=True)
 with (p/(name+'.log')).open('w') as f:rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 rows.append({'step':name,'returncode':rc});(p/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print('END',name,rc,flush=True)
 return rc
try:
 assert step('pair-up',['tools/vm-pair','up',str(image)])==0
 assert step('clean-payload',['python3',str(p/'check-payload.py'),'clean'])==0
 step('standard',['tools/vm-qa','--skip-up',str(image)])
 step('after-defaults',['python3',str(p/'check-payload.py'),'after-defaults'])
 for backend in ['sftp','s3']:step(backend,['tools/vm-qa','--skip-up','--only','round-trip','--backend',backend,str(image)])
finally:
 step('pair-down',['tools/vm-pair','down'])
 for backend in ['webdav','sftp','s3']:step(backend+'-down',['tools/cloud-test-backend','--backend',backend,'down'])
step('bundle-after',['tools/rasteratops-candidate-store','verify',str(bundle)])
raise SystemExit(0 if all(x['returncode']==0 for x in rows) else 1)
