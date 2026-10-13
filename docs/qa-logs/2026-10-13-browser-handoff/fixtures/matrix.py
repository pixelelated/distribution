from pathlib import Path
import subprocess,json,time,os,signal,socket,threading,hashlib,statistics,sys
from playwright.sync_api import sync_playwright
r=Path(__file__).parent;ssh=json.loads((r/'ssh-command.json').read_text());results=[];server=None;tunnel=None
# Launch observer/server before a trial; all sampling and phone work stays scoped.
def remote(cmd,**kw):return subprocess.run(ssh+[cmd],check=True,timeout=kw.pop('timeout',30),**kw)
def output(cmd):return remote(cmd,capture_output=True,text=True).stdout

def key(k):
 with socket.socket(socket.AF_UNIX) as s:
  s.settimeout(3);s.connect(str(r/'monitor.sock'));s.recv(4096);s.sendall(('sendkey '+k+' 100\n').encode());time.sleep(.2);s.recv(4096)

def shot(path):
 data=output("python3 - <<'P'\nimport os,subprocess\nfrom pathlib import Path\np=next(x for x in Path('/run').glob('**/wayland-*') if x.is_socket());e=dict(os.environ,XDG_RUNTIME_DIR=str(p.parent),WAYLAND_DISPLAY=p.name)\nr=subprocess.run(['grim','/storage/qa570/frame.png'],env=e);raise SystemExit(r.returncode)\nP")
 with path.open('wb') as f:remote('cat /storage/qa570/frame.png',stdout=f)

def read_events(name):
 if not (r/'events.jsonl').exists():return []
 rows=[]
 for line in (r/'events.jsonl').read_text().splitlines():
  try:x=json.loads(line)
  except json.JSONDecodeError:continue
  if x.get('run')==name:rows.append(x)
 return rows

def waitfor(fn,limit,label):
 end=time.monotonic()+limit
 while time.monotonic()<end:
  x=fn()
  if x:return x
  time.sleep(.3)
 raise RuntimeError('Timed out: '+label)

def trial(name,mode,browser):
 out=r/name;out.mkdir();(r/'case.json').write_text(json.dumps({'name':name}))
 before=json.loads(output("python3 - <<'P'\nfrom pathlib import Path\nimport json\nes=[int(p.name) for p in Path('/proc').glob('[0-9]*') if (p/'exe').resolve().name=='emulationstation'];print(json.dumps({'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'es':es}))\nP"))
 # Full PSS baseline recorded for five seconds before opening.
 guest='/storage/qa570/'+name;sample_log=(out/'sampler-ssh.log').open('wb');sampler=subprocess.Popen(ssh+['python3 /storage/qa570/sampler.py '+guest],stdout=sample_log,stderr=sample_log)
 context=None;phone=None;error=None;closed=False
 try:
  if mode!='none':
   context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
   phone=context.new_page()
   phone.add_init_script('''window.qaRequests=[];const originalFetch=window.fetch;window.fetch=function(u,o){const row={issued:Date.now(),url:String(u),body:o?.body||null};window.qaRequests.push(row);return originalFetch.apply(this,arguments).then(v=>{row.ack=Date.now();row.status=v.status;return v},e=>{row.error=String(e);row.ack=Date.now();throw e})};''')
   pin=output("python3 -c \"import json;print(json.load(open('/var/run/cloud_oauth/session.json'))['pin'])\"").strip()
   phone.goto('http://127.0.0.1:10581/'+pin,wait_until='domcontentloaded',timeout=15000)
  time.sleep(5);shot(out/'before.png');start=time.monotonic();key('x')
  waitfor(lambda:[e for e in read_events(name) if e.get('kind')=='loaded' and e['n']==0],35,'initial loaded page')
  loaded=time.monotonic();acted=set();frames=set();last_guard=-5
  while time.monotonic()-loaded<75:
   events=read_events(name);latest={e['n']:e for e in events if e.get('kind')=='loaded'}
   for n,e in latest.items():
    if mode=='active' and n not in acted and time.time()*1000-e['received_wall_ms']>3500:
     assert phone.locator('#state').inner_text()=='Connected.','phone field not ready'
     phone.locator('#clear').click();phone.locator('#kb').fill('a'*64)
     pad=phone.locator('#pad').bounding_box();x=pad['x']+pad['width']/2;y=pad['y']+pad['height']/2
     phone.mouse.move(x,y);phone.mouse.down()
     phone.mouse.move(x+20,y+10,steps=30);phone.mouse.up();acted.add(n)
   t=time.monotonic()-loaded
   for threshold in [10,70]:
    if t>=threshold and threshold not in frames:shot(out/('page-'+str(threshold)+'.png'));frames.add(threshold)
   # A guard is an incomplete control, never a low-memory PASS.
   if t-last_guard>=5:
    last_guard=t
    guard=output('test ! -f '+guest+'/guard.json && echo clear || echo guarded').strip();assert guard=='clear','memory guard fired'
   if phone:phone.wait_for_timeout(100)
   else:time.sleep(.1)
  key('esc');closed=True
  waitfor(lambda:output("test -n \"$(pidof cloud-signin-window)\" && echo running || echo gone").strip()=='gone',20,'browser exit')
  time.sleep(6);shot(out/'returned.png')
  if phone:
   phone.screenshot(path=str(out/'phone.png'),full_page=True);(out/'phone-requests.json').write_text(json.dumps(phone.evaluate('window.qaRequests'),indent=2)+'\n')
  # The normal cancellation return is STILL WAITING / OK. Dismiss it to QR.
  key('x');time.sleep(2);shot(out/'ready-next.png')
  after=json.loads(output("python3 - <<'P'\nfrom pathlib import Path\nimport json\nes=[int(p.name) for p in Path('/proc').glob('[0-9]*') if (p/'exe').resolve().name=='emulationstation'];print(json.dumps({'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'es':es}))\nP"))
  assert before==after and before['es'],'frontend/boot changed'
  events=read_events(name);pages=sorted({e['n'] for e in events if e.get('kind')=='loaded'});assert pages==[0,1,2,3],pages
  if mode=='active':
   assert acted=={0,1,2,3},acted
   for n in range(4):assert any(e.get('kind')=='input' and e['n']==n and e['length']==64 and e['valid'] for e in events),'input not applied '+str(n)
  result={'name':name,'mode':mode,'rc':0,'before':before,'after':after,'loaded_seconds':loaded-start,'pages':pages,'acted':sorted(acted)}
 except BaseException as e:
  error=repr(e);result={'name':name,'mode':mode,'rc':1,'error':error};raise
 finally:
  if not closed:
   try:remote('/usr/bin/cloud_oauth close',capture_output=True,timeout=25)
   except Exception:pass
  if context:context.close()
  remote('touch '+guest+'/stop',capture_output=True)
  try:sampler.wait(timeout=10)
  except subprocess.TimeoutExpired:sampler.terminate();sampler.wait(timeout=5)
  sample_log.close();remote('tar -czf '+guest+'.tgz -C '+guest+' .',capture_output=True)
  with (out/'guest.tgz').open('wb') as f:remote('cat '+guest+'.tgz',stdout=f)
  remote('cat /var/run/cloud_oauth/window.log',stdout=(out/'window.log').open('wb'))
  (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');results.append(result);(r/'progress.json').write_text(json.dumps(results,indent=2)+'\n')
 print('DONE '+name,flush=True)

result={'started':time.time()}
try:
 server=subprocess.Popen(['python3',str(r/'server02.py')],stdout=(r/'server02.log').open('wb'),stderr=subprocess.STDOUT)
 tunnel=subprocess.Popen(ssh[:-1]+['-N','-L','127.0.0.1:10581:10.0.2.15:8080',ssh[-1]],stdout=(r/'tunnel.log').open('wb'),stderr=subprocess.STDOUT)
 time.sleep(1)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/home/max/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome',args=['--disable-dev-shm-usage'])
  for name,mode in [('none1','none'),('idle1','idle'),('active1','active'),('active2','active'),('idle2','idle'),('none2','none')]:
   print('START '+name,flush=True);trial(name,mode,browser)
  browser.close()
 result.update(rc=0,cases=results)
except BaseException as e:result.update(rc=1,error=repr(e),cases=results);raise
finally:
 for p in [tunnel,server]:
  if p and p.poll() is None:
   p.terminate()
   try:p.wait(timeout=8)
   except subprocess.TimeoutExpired:p.kill();p.wait()
 result['ended']=time.time();(r/'matrix-result.json').write_text(json.dumps(result,indent=2)+'\n')
