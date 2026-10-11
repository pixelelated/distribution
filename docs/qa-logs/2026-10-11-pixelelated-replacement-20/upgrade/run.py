from pathlib import Path
import subprocess,json,os,hashlib
p=Path(__file__).resolve().parent;r=Path.cwd();j=json.loads(Path('/workspace/tmp/pixelelated-m7-build20b/inputs.json').read_text())
for name,want in json.loads((p/'prepared-manifest.json').read_text()).items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==want,name
assert json.loads(Path('/workspace/tmp/pixelelated-m7-qa20/launcher-result.json').read_text())['runner_returncode']==1
assert json.loads(Path('/workspace/tmp/pixelelated-m7-qa20-accept02/launcher-result.json').read_text())['runner_returncode']==0
qualification=json.loads((p/'clean-qualification.json').read_text())
assert qualification['result']=='PASS' and qualification['source']==j['distribution_commit']
assert qualification['original_launcher_returncode']==1 and qualification['resolved_original_scripts_failures']==7
assert qualification['corrected_regression']['failures']==qualification['corrected_regression']['skips']==0
old=Path('/workspace/artifacts/pixelelated-candidates/sha256/ee8e263c2e63b7fc79a458e9e89b0f4a3c393487377a6a820c7f7166dada1662')
new=Path(Path('/workspace/tmp/pixelelated-m7-image20/bundle.path').read_text().strip())
env={**os.environ,'TMPDIR':str(p/'tmp'),'VM_QEMU_RUNTIME_DIR':str(p/'runtime'),'VM_PAIR_DIR':str(p/'pair'),'CLOUD_QA_STATE':str(p/'cloud'),'ROCKNIX_ARTIFACTS':str(p/'artifacts'),'CLOUD_QA_BACKEND':'webdav','PYTHONDONTWRITEBYTECODE':'1','PATH':str(p/'bin')+':'+os.environ['PATH']}
subprocess.run(['python3','/workspace/tmp/pixelelated-m7-build20b/verify-source.py'],check=True)
subprocess.run(['python3',str(p/'preflight.py')],env=env,check=True)
rows=[]
def step(name,cmd):
 print('START',name,flush=True)
 with (p/(name+'.log')).open('w') as f:rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 rows.append({'step':name,'returncode':rc});(p/'result.json').write_text(json.dumps(rows,indent=2)+'\n');print('END',name,rc,flush=True);return rc
try:
 for label,b in [('old',old),('new',new)]:assert step('verify-'+label,['tools/rasteratops-candidate-store','verify',str(b)])==0
 assert step('rehearsal',['bash',str(p/'rehearsal.sh'),str(next(old.glob('*.img.gz'))),str(next(new.glob('*.tar'))),j['distribution_commit']])==0
 assert step('payload',['python3',str(p/'check-payload.py'),'upgraded'])==0
 assert step('information',['python3',str(p/'information.py'),str(p/'artifacts/information')])==0
 assert step('retained-suites',['tools/vm-qa','--skip-up','--only','fresh,round-trip,exit,time-to-play',str(next(new.glob('*.img.gz')))])==0
finally:
 step('pair-down',['tools/vm-pair','down']);step('webdav-down',['tools/cloud-test-backend','down'])
step('bundle-after',['tools/rasteratops-candidate-store','verify',str(new)])
raise SystemExit(0 if all(x['returncode']==0 for x in rows) else 1)
