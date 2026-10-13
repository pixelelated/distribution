from pathlib import Path
import subprocess,json
r=Path(__file__).parent;results=[]
for lang,variant in [('fr_FR','on'),('fr_FR','off'),('fr_FR','index-off')]:
 p=subprocess.run(['timeout','110','python3',str(r/'notice-frames02.py'),'notice-'+lang+'-640-02-'+variant,lang,variant]);results.append({'language':lang,'variant':variant,'rc':p.returncode});(r/'notice-640-batch02-result.json').write_text(json.dumps(results,indent=2)+'\n')
 if p.returncode:break
raise SystemExit(0 if len(results)==3 and all(x['rc']==0 for x in results) else 1)
