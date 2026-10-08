import datetime,json,os,subprocess,sys
from pathlib import Path
owner=Path(__file__).resolve().parent
manifest=json.loads((owner/'commands.json').read_text())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==manifest['frozen_head']
results=[]
for name,cmd in manifest['commands']:
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 print('START '+name,flush=True)
 with (owner/(name+'.log')).open('wb') as log:
  p=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'TERM':'dumb'})
 row={'name':name,'command':cmd,'rc':p.returncode,'started':started,'ended':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 results.append(row);(owner/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print('END '+name+' rc='+str(p.returncode),flush=True)
result=0 if all(x['rc']==0 for x in results) else 1
(owner/'inner.rc').write_text(str(result)+'\n')
(owner/'outer.rc').write_text(str(result)+'\n')
sys.exit(result)
