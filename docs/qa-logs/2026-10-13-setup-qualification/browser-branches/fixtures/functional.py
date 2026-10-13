from pathlib import Path
import subprocess,json,time
r=Path(__file__).parent;result={'rc':1,'cases':[],'started':time.time()}
try:
 for mode in ['cancel','provider-failure','success']:
  name='en640-'+mode
  p=subprocess.run(['python3','-u',str(r/'case04.py'),name,mode,'en_US'],timeout=240)
  result['cases'].append({'name':name,'original_rc':p.returncode});print('CASE COMPLETE',name,p.returncode,flush=True)
  if p.returncode:raise RuntimeError(name+' failed')
 result['rc']=0
finally:
 result['ended']=time.time();(r/'functional-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
