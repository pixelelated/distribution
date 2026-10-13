from pathlib import Path
import subprocess,json,datetime
r=Path(__file__).parent;s=json.loads((r/'ssh-command.json').read_text());result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rc':1}
try:
 for name in ['collection-fixture.py','library-fixture02.py']:
  p=subprocess.run(s+['python3 /storage/qa-m7-baseline/'+name],timeout=280);result[name]=p.returncode
  if p.returncode:raise RuntimeError(name+' failed')
 result['rc']=0
finally:
 for src,dst in [('collection-result.json','collection-result.json'),('collection-progress.json','collection-progress.json'),('library02/library-result.json','library02-result.json'),('library02/rom-only.json','library02-rom-only.json'),('library02/rom-plus-gamelist.json','library02-rom-plus-gamelist.json')]:
  p=subprocess.run(s+['cat /storage/qa-m7-baseline/'+src],capture_output=True,timeout=15)
  if p.returncode==0:(r/dst).write_bytes(p.stdout)
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'collection-library02-host-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
