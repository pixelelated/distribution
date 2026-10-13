from pathlib import Path
import json,subprocess,time
from ui import out,remote
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');p=repo/'docs/qa-logs/2026-10-13-wifi-backend-source';case=r/'backend-controls';case.mkdir();result={'rc':1,'started':time.time(),'cases':[]};dest='/storage/qa-wifi-577-backend'
try:
 remote('mkdir -p '+dest+'/scratch',capture_output=True)
 for file,name in [(p/'fixture.py','fixture.py'),(p/'source-review.json','source-review.json'),(repo/'projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl','current')]:
  with file.open('rb') as f:remote('cat > '+dest+'/'+name,stdin=f)
 old=subprocess.check_output(['git','show','6cf8405bcc398af71ba081b6eb377da41b44ef0d:projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl'],cwd=repo)
 remote('cat > '+dest+'/original',input=old,capture_output=True)
 for version in ['original','current']:
  args=json.loads((r/'ssh-command.json').read_text())+[f'python3 {dest}/fixture.py --version {version} --source {dest}/{version} --tmp-root {dest}/scratch']
  with (case/(version+'.jsonl')).open('wb') as stdout,(case/(version+'.stderr')).open('wb') as stderr:q=subprocess.run(args,stdout=stdout,stderr=stderr,timeout=210)
  rows=[json.loads(x) for x in (case/(version+'.jsonl')).read_text().splitlines()];result['cases'].append({'version':version,'original_rc':q.returncode,'count':len(rows),'all_pass':all(x['result']=='PASS' for x in rows)});assert q.returncode==0 and len(rows)==37 and all(x['result']=='PASS' for x in rows),version
 result['rc']=0
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
