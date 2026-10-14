from pathlib import Path
import json,subprocess,time
r=Path(__file__).parent;result={'rc':1,'started':time.time(),'stages':[]}
try:
 for name,args,limit in [('selection',['capability-selection.py'],120),('steam-fex',['steam-corrected.py'],120),('dolphin',['dolphin-controls.py'],410),('global-en',['capability-global.py','capability-global-en640','en_US'],150),('global-fr',['capability-global.py','capability-global-fr640','fr_FR'],150),('wifi-fr',['wifi-profile.py','fr640-bb9e','fr_FR'],320)]:
  p=subprocess.run(['python3',str(r/args[0]),*args[1:]],timeout=limit);result['stages'].append({'name':name,'rc':p.returncode});(r/'small-followup-progress.json').write_text(json.dumps(result,indent=2)+'\n');assert p.returncode==0,name
 result['rc']=0
finally:
 result['ended']=time.time();(r/'small-followup-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
