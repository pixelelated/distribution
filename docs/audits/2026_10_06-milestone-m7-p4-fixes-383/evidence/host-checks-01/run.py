from pathlib import Path
import subprocess,os,json,datetime,sys,hashlib
owner=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
assert Path.cwd()==repo
# The product source stays frozen even while process documentation is updated.
subprocess.run(['git','diff','--quiet','7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','--','projects','packages','distributions','config'],check=True)
seal=json.loads((owner/'seal.json').read_text())
for path,h in seal.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h,path
env=os.environ.copy();env['QA_SYSTEM_ROOT']='/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement14/build.pixelelated-GENERIC_X64.x86_64/image/system';env['ES_SRC']='/home/max/Development/emulationstation-next.worktrees/qa-integration'
rows=[]
try:
 for name,cmd,want in json.loads((owner/'checks.json').read_text()):
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();print('START',name,start,flush=True)
  with (owner/'activity'/(name+'.log')).open('w') as log:
   r=subprocess.run(cmd,cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT)
  rows.append({'name':name,'command':cmd,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rc':r.returncode,'expected_rc':want,'passed':r.returncode==want})
  (owner/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print('END',name,r.returncode,'expected',want,flush=True)
  if r.returncode!=want:break
 code=0 if len(rows)==5 and all(x['passed'] for x in rows) else 1
except BaseException:
 (owner/'inner.rc').write_text('1\n');(owner/'outer.rc').write_text('1\n');raise
(owner/'inner.rc').write_text(str(code)+'\n');(owner/'outer.rc').write_text(str(code)+'\n');sys.exit(code)
