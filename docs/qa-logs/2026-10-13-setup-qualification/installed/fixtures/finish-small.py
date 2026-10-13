from pathlib import Path
import subprocess,json
r=Path(__file__).parent
prior=json.loads((r/'notice-640-batch02-owner/launcher-result.json').read_text());assert prior['runner_returncode']==0
results=[]
for command in [['wifi-profile.py','fr640','fr_FR'],['recent-frames.py','en640','en_US'],['recent-frames.py','fr640','fr_FR']]:
 p=subprocess.run(['timeout','330','python3',str(r/command[0]),*command[1:]])
 results.append({'command':command,'rc':p.returncode});(r/'finish-small-result.json').write_text(json.dumps(results,indent=2)+'\n')
 if p.returncode:break
raise SystemExit(0 if len(results)==3 and all(x['rc']==0 for x in results) else 1)
