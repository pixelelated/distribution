from pathlib import Path
import subprocess,json,time
r=Path(__file__).parent;result={'rc':1,'started':time.time(),'cases':[]}
try:
 for lang in ['en_US','fr_FR']:
  for mode in ['gc-auto','gc-retro-override','dc-auto','dc-standalone-override','dc-retro-override']:
   name='capability-'+mode+'-'+lang+'-640-03'
   c=subprocess.run(['python3',str(r/'capability-case03.py'),name,lang,mode],timeout=180)
   result['cases'].append({'name':name,'rc':c.returncode})
   assert c.returncode==0,name
 result['rc']=0
finally:
 result['ended']=time.time();(r/'capability-small03-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
