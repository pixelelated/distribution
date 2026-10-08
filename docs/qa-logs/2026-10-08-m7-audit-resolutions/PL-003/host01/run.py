import datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
o=Path(__file__).resolve().parent
m=json.loads((o/'commands.json').read_text())
def snapshot():return {p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in m['files']}
before=snapshot();(o/'inputs-before.json').write_text(json.dumps(before,indent=2)+'\n');rows=[];rc=1
try:
 for name,cmd in m['commands']:
  print('START',name,flush=True)
  start=datetime.datetime.now(datetime.timezone.utc).isoformat()
  with (o/(name+'.log')).open('wb') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,cwd=m['source'],env={**os.environ,'TERM':'dumb'})
  rows.append({'name':name,'argv':cmd,'returncode':r.returncode,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});(o/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
  print('END',name,r.returncode,flush=True)
  if r.returncode:break
 after=snapshot();(o/'inputs-after.json').write_text(json.dumps(after,indent=2)+'\n');assert after==before,'source changed during checks'
 rc=0 if len(rows)==len(m['commands']) and all(r['returncode']==0 for r in rows) else 1
finally:
 (o/'inner.rc').write_text(str(rc)+'\n');(o/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
