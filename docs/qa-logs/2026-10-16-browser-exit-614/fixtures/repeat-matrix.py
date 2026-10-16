import json,subprocess,time
from pathlib import Path
P=Path('/tmp/pix-m7-browser-exit-20261016-01');R=Path('/workspace/tmp/pix-m7-browser-exit-vm-20261016-01');result={'status':'FAIL','cases':[]};index=100

def req(label,kind,value=''):
 global index
 name=f'{index:03d}-{label}';index+=1
 c=subprocess.run(['python3',str(P/'request.py'),name,kind,value],capture_output=True,text=True,timeout=55)
 assert c.returncode==0,(name,c.stderr)
 v=json.loads((R/'responses'/(name+'.json')).read_text());assert v['status']=='PASS',(name,v)
 return v['output']
def key(k):req('key-'+k,'monitor','sendkey '+k+' 100');time.sleep(.25)
def snapshot(label):
 text=req(label,'python',str(P/'guarded-snapshot.py'));return json.loads(next(x for x in text.splitlines() if x.startswith('{')))
def identity(v):return [(p['pid'],p['start']) for p in v['processes'] if p['exe']=='emulationstation']
try:
 baseline=snapshot('baseline');assert len(identity(baseline))==1
 for number,case in enumerate(['qemu-escape','instant-uinput','normal-close','phone-handler'],1):
  print('START '+case,flush=True)
  for k in ['x','x','down','x']:key(k)
  time.sleep(3);req(case+'-choice','frame');key('x');time.sleep(4)
  before=snapshot(case+'-before');assert identity(before)==identity(baseline)
  assert any(p['exe']=='cloud-signin-window' for p in before['processes'])
  assert any(w['app_id']=='cloud-signin-window' and w['focused'] for w in before['windows'])
  assert sum(json.loads(x)['kind']=='loaded' for x in before['page_events'].splitlines())==number
  req(case+'-browser','frame')
  if case=='qemu-escape':
   key('q');typed=snapshot('qemu-consumption');assert any(json.loads(x).get('kind')=='input' and json.loads(x).get('length')==1 for x in typed['page_events'].splitlines());key('esc');action='QEMU escape'
  else:
   script={'instant-uinput':'instant-escape.py','normal-close':'normal-close.py','phone-handler':'http-escape.py'}[case]
   action=req(case+'-action','python',str(P/script))
  time.sleep(2);after=snapshot(case+'-after');assert identity(after)==identity(baseline) and before['boot']==after['boot']
  assert not any(p['exe']=='cloud-signin-window' or p['exe'].startswith('WebKit') or p['argv'].strip().endswith('cloud_oauth wait') for p in after['processes'])
  assert not any('cloud' in x.lower() for x in after['keyboard_names'])
  req(case+'-return','frame');req(case+'-log','serial',f'cp /var/run/cloud_oauth/window.log /storage/qa614/case{number}-window.log')
  key('z');time.sleep(1);cancelled=snapshot(case+'-cancelled');assert len(cancelled['processes'])==1
  result['cases'].append({'case':case,'status':'PASS','browser':next(p for p in before['processes'] if p['exe']=='cloud-signin-window'),'frontend':identity(after),'action':action});print('PASS '+case,flush=True)
 req('final-ui','frame');result['status']='PASS'
except BaseException as exc:result['error']=repr(exc);raise
finally:(P/'repeat-result.json').write_text(json.dumps(result,indent=2)+'\n')
