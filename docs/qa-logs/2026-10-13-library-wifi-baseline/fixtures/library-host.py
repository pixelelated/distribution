from pathlib import Path
import subprocess,json,datetime
r=Path(__file__).parent;s=json.loads((r/'ssh-command.json').read_text());result={'started':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 p=subprocess.run(s+['python3 /storage/qa-m7-baseline/library-fixture.py'],timeout=240);result['rc']=p.returncode
finally:
 for n in ['library-result.json','rom-only.json','rom-plus-gamelist.json']:
  p=subprocess.run(s+['cat /storage/qa-m7-baseline/'+n],capture_output=True,timeout=15)
  if p.returncode==0:(r/n).write_bytes(p.stdout)
 result['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(r/'library-host-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result.get('rc',1))
