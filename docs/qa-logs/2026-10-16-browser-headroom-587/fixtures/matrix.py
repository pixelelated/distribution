import json,sys,time,signal
from pathlib import Path
from drive import req,key,P,R
result={'status':'FAIL','cases':[],'source':'077197e6cd3ea31f33b28aaf3882a694b3423b53','order':['active','stopped','stopped','active']};i=100
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('matrix 300s deadline')));signal.alarm(300)
def command(label,kind,value=''):
 global i
 name=f'{i:03d}-{label}';i+=1;return req(name,kind,value)
def press(k):
 global i
 key(f'{i:03d}-key-{k}',k);i+=1

def snap(label):
 text=command(label,'python',str(P/'snapshot.py'));return json.loads(next(x for x in text.splitlines() if x.startswith('{')))
def proxy(action):
 command('action-'+action,'serial',f"printf '{action}' > /storage/qa587/proxy-action")
 return command('proxy-'+action,'python',str(P/'proxy-control.py'))
def phase(name):command('phase','serial',f"printf '{name}' > /storage/qa587/phase")
try:
 baseline=snap('baseline');frontend=[x for x in baseline['processes'] if x['exe']=='emulationstation'];assert len(frontend)==1
 proxy('verify')
 for n,state in enumerate(result['order'],1):
  print('START',n,state,flush=True);row={'number':n,'state':state,'status':'FAIL'};result['cases'].append(row)
  if state=='stopped':row['stop']=proxy('stop')
  else:proxy('start')
  phase(f'{n}-{state}-pre');time.sleep(6)
  for k in ['x','x','down','x']:press(k)
  time.sleep(3);command('choice','frame');phase(f'{n}-{state}-browser');launched=time.monotonic();press('x')
  for _ in range(10):
   time.sleep(1);before=snap('loading')
   if before['paint_ready']>=n:break
  assert before['paint_ready']==n and before['loaded']==n,before
  assert [x for x in before['processes'] if x['exe']=='emulationstation']==frontend
  assert any(x['app_id']=='cloud-signin-window' and x['focused'] for x in before['windows'])
  row['readiness_observed_seconds']=time.monotonic()-launched;row['browser']=next(x for x in before['processes'] if x['exe']=='cloud-signin-window')
  command('loaded','frame');phase(f'{n}-{state}-steady');time.sleep(10)
  press('q');typed=snap('input');assert typed['input']==n
  action=command('normal-close','python',str(P/'normal-close.py'));row['close']=action
  phase(f'{n}-{state}-return');time.sleep(3);after=snap('returned')
  assert [x for x in after['processes'] if x['exe']=='emulationstation']==frontend
  assert not any(x['exe']=='cloud-signin-window' or 'WebKit' in x['comm'] for x in after['processes'])
  command('returned-frame','frame');press('z');time.sleep(1)
  if state=='stopped':row['restart']=proxy('start')
  row['preservation']=proxy('verify');row['status']='PASS';print('PASS',n,state,flush=True)
 result['status']='PASS'
except BaseException as e:
 result['error']=repr(e);print('FAIL',repr(e),flush=True)
 try:result['failure_close']=command('failure-close','serial','/usr/bin/cloud_oauth close')
 except BaseException as cleanup:result['cleanup_error']=repr(cleanup)
 try:result['failure_restart']=proxy('start')
 except BaseException as cleanup:result['restart_error']=repr(cleanup)
finally:
 signal.alarm(0);(P/'matrix-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['status']=='PASS' else 1)
