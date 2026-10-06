from pathlib import Path
import subprocess,json,datetime,sys,hashlib
owner=Path(__file__).parent
repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
es=Path('/home/max/Development/emulationstation-next.worktrees/qa-integration')
assert Path.cwd()==owner
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=es,text=True).strip()=='f6f0c134212bc696f2f6a747c8d390a588f2f0ce'
subprocess.run(['git','diff','--quiet'],cwd=es,check=True)
for name,digest in json.loads((owner/'seal.json').read_text()).items():
 assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
rows=[]
try:
 for name,cmd in json.loads((owner/'checks.json').read_text()):
  print('START',name,flush=True)
  with (owner/'activity'/(name+'.log')).open('w') as log:
   result=subprocess.run(cmd,cwd=repo,stdout=log,stderr=subprocess.STDOUT)
  rows.append({'name':name,'command':cmd,'rc':result.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
  (owner/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
  print('END',name,result.returncode,flush=True)
  if result.returncode:break
 code=0 if len(rows)==3 and all(x['rc']==0 for x in rows) else 1
except BaseException:
 (owner/'inner.rc').write_text('1\n');(owner/'outer.rc').write_text('1\n');raise
(owner/'inner.rc').write_text(str(code)+'\n');(owner/'outer.rc').write_text(str(code)+'\n');sys.exit(code)
