from pathlib import Path
import subprocess,json,time
r=Path(__file__).parent;results=[]
for route in ['native','phone']:
 p=subprocess.run(['timeout','180','python3',str(r/'browser-recovery02.py'),'browser-'+route+'-fr640',route,'fr_FR'])
 results.append({'route':route,'rc':p.returncode})
 if p.returncode:break
(r/'browser-fr640-batch-result.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(0 if len(results)==2 and all(x['rc']==0 for x in results) else 1)
