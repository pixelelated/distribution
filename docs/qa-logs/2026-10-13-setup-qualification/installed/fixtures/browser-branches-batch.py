from pathlib import Path
import subprocess,json
r=Path(__file__).parent;results=[]
for route,scenario in [('native','recovered'),('phone','recovered'),('native','completed'),('phone','expired'),('native','provider-failed'),('phone','back')]:
 p=subprocess.run(['timeout','180','python3',str(r/'browser-branches.py'),'browser-'+route+'-'+scenario+'-en640',route,'en_US',scenario])
 results.append({'route':route,'scenario':scenario,'rc':p.returncode});(r/'browser-branches-batch-result.json').write_text(json.dumps(results,indent=2)+'\n')
 if p.returncode:break
raise SystemExit(0 if len(results)==6 and all(x['rc']==0 for x in results) else 1)
