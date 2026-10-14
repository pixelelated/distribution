from pathlib import Path
import json,subprocess,time
r=Path(__file__).parent;result={'rc':1,'started':time.time(),'stages':[]}
try:
 for name,args,limit in [('provision',['provision1280.py'],150),('capability-rebind',['capability-rebind1280.py'],45),('capability-large',['capability-large03.py'],720),('global-en',['capability-global.py','capability-global-en1280','en_US'],150),('global-fr',['capability-global.py','capability-global-fr1280','fr_FR'],150),('wifi-fr',['wifi-profile.py','fr1280-bb9e','fr_FR'],320)]:
  p=subprocess.run(['python3',str(r/args[0]),*args[1:]],timeout=limit);result['stages'].append({'name':name,'rc':p.returncode});(r/'large-progress.json').write_text(json.dumps(result,indent=2)+'\n');assert p.returncode==0,name
 result['rc']=0
finally:
 result['ended']=time.time();(r/'large-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
