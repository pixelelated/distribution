"""Installed EN/FR presentation, actual handler and done callback, local fixture.

Requires an isolated candidate-bound guest at the caller's ports. Authentication
is a provider stand-in; no token exchange/account or public-provider claim.
"""
from pathlib import Path
import argparse,base64,datetime,hashlib,http.server,json,shlex,socket,struct,subprocess,threading,time,urllib.request
from persistent_viewer import observe_frames
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--identity',required=True);ap.add_argument('--port',type=int,default=10026)
ap.add_argument('--monitor',required=True);ap.add_argument('--language',choices=['en_US','fr_FR'],required=True)
ap.add_argument('--out',type=Path,required=True);ap.add_argument('--tools',type=Path,required=True)
ap.add_argument('--fixture',type=Path,required=True);ap.add_argument('--build-id',required=True)
a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
ssh=['ssh','-i',a.identity,'-p',str(a.port),'-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1']
resources=[];checks=[];frames=[];sid=None;fixture_pid=None;root='/tmp/m7-signin-presentation'
viewer_stop=threading.Event();viewer_ready=threading.Event();viewer_errors=[];viewer_thread=None
def guest(command,data=None,check=True):
 return subprocess.run(ssh+[command],input=data,text=True,capture_output=True,check=check,timeout=60)
def assertion(ok,name):
 checks.append({'assertion':name,'passed':bool(ok)});(a.out/'assertions.json').write_text(json.dumps(checks,indent=2)+'\n')
 print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:raise AssertionError(name)
def wait(fn,seconds,name):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  value=fn()
  if value:return value
  time.sleep(.3)
 raise TimeoutError(name)
def state():
 r=guest('cat '+root+'/state.json',check=False)
 try:return json.loads(r.stdout) if r.returncode==0 else {}
 except json.JSONDecodeError:return {}
def action(name):guest('touch '+root+'/action-'+name)
def port():
 with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def server(handler):
 s=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);resources.append(s)
 threading.Thread(target=s.serve_forever,daemon=True).start();return s
class Provider(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path=='/start':
   self.send_response(302);self.send_header('Location','/mobile-form');self.send_header('Content-Length','0');self.end_headers();return
  body=b'<!doctype html><meta name=viewport content="width=device-width"><style>body{background:#111;color:#eee;font:20px sans-serif;padding:20px}</style><h1>QA local sign-in</h1><input autofocus aria-label="QA input">'
  self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
class Phone(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path=='/proof-frame':
   body=('<!doctype html><style>body{margin:0}</style><iframe id="phone" style="border:0;width:390px;height:1000px" src="/'+pin+'"></iframe>').encode();content='text/html'
  else:
   with urllib.request.urlopen(tunnel_base+self.path,timeout=20) as r:body=r.read();content=r.headers.get('Content-Type','text/html')
  self.send_response(200);self.send_header('Content-Type',content);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def do_POST(self):
  body=self.rfile.read(int(self.headers['Content-Length']))
  request=urllib.request.Request(tunnel_base+self.path,data=body,headers={'Content-Type':'application/x-www-form-urlencoded'})
  with urllib.request.urlopen(request,timeout=20) as r:result=r.read();code=r.status;content=r.headers.get('Content-Type','text/plain')
  self.send_response(code);self.send_header('Content-Type',content);self.send_header('Content-Length',str(len(result)));self.end_headers();self.wfile.write(result)
def wd(method,path,body=None):
 req=urllib.request.Request(driver_base+path,method=method,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)['value']
def js(script):return wd('POST','/session/'+sid+'/execute/sync',{'script':script,'args':[]})
def frame(path,data,size):
 assertion(struct.unpack('>II',data[16:24])==size,path.name+' dimensions')
 path.write_bytes(data);frames.append({'file':path.name,'sha256':hashlib.sha256(data).hexdigest(),'visual_review':'pending'})
def phone_shot(name):
 wd('POST','/session/'+sid+'/frame',{'id':None})
 key=element['element-6066-11e4-a52e-4f735466cecf']
 frame(a.out/(name+'.png'),base64.b64decode(wd('GET','/session/'+sid+'/element/'+key+'/screenshot')),(390,1000))
 wd('POST','/session/'+sid+'/frame',{'id':element})
def native_shot(name):
 r=subprocess.run([str(a.tools/'vm-visual-qa'),'--monitor',a.monitor,'settle','--timeout','30','--quiet','2'],capture_output=True,text=True,check=True,timeout=45)
 assertion('settle: still after ' in r.stdout,name+' actual native frame stable')
 p=a.out/(name+'.png');subprocess.run([str(a.tools/'vm-visual-qa'),'--monitor',a.monitor,'shot',str(p)],check=True,stdout=subprocess.DEVNULL,timeout=20)
 frame(p,p.read_bytes(),(640,480))
try:
 assertion(guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").stdout.strip().strip('"')==a.build_id,'candidate build identity')
 assertion(guest("pgrep -f '^/usr/bin/retroarch'",check=False).returncode==1,'no game running')
 before=guest('sha256sum /usr/bin/cloud_oauth /usr/bin/cloud-signin-window /usr/bin/emulationstation').stdout
 (a.out/'installed-before.sha256').write_text(before)
 guest('systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting system.language '+a.language+'; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; systemctl start essway')
 def ready():
  r=guest('curl -sS -m 2 http://127.0.0.1:1234/isIdle',check=False)
  try:return r.returncode==0 and json.loads(r.stdout)==[True]
  except json.JSONDecodeError:return False
 wait(ready,90,'installed ES idle after locale change')
 locale_code='''from pathlib import Path
import json
pids=[p for p in Path('/proc').glob('[0-9]*') if (p/'exe').exists() and str((p/'exe').resolve())=='/usr/bin/emulationstation']
assert len(pids)==1
values=dict(x.split(b'=',1) for x in (pids[0]/'environ').read_bytes().split(b'\\0') if b'=' in x)
print(values.get(b'LANGUAGE',b'').decode())
'''
 language=guest('python3 -',data=locale_code).stdout.strip()
 assertion(language.startswith(a.language[:2]),'running ES exports requested language')
 viewer_dir=a.out/'persistent-viewer';viewer_dir.mkdir()
 viewer_thread=threading.Thread(target=observe_frames,args=('127.0.0.1',5912,viewer_dir,viewer_stop,viewer_ready,viewer_errors),daemon=True)
 viewer_thread.start()
 assertion(viewer_ready.wait(10) and not viewer_errors,'persistent read-only VNC viewer ready')
 echo=server(Provider)
 guest('cat > /tmp/m7-signin-fixture.py',data=a.fixture.read_text())
 command='''import os,subprocess
with open('/tmp/m7-signin-fixture.log','w') as f:
 p=subprocess.Popen(['python3','/tmp/m7-signin-fixture.py',URL],env=dict(os.environ,LANGUAGE=LANG),stdin=subprocess.DEVNULL,stdout=f,stderr=f,start_new_session=True)
 print(p.pid)
'''.replace('URL',repr('http://10.0.2.2:'+str(echo.server_port)+'/start')).replace('LANG)',repr(language)+')')
 fixture_pid=int(guest('python3 -',data=command).stdout.strip())
 (a.out/'fixture.pid').write_text(str(fixture_pid)+'\n')
 wait(lambda:state().get('window_alive'),60,'installed local provider window')
 initial=state();assertion(not initial['done_exists'] and not initial['is_finishing_fr'] and not initial['is_finishing_en'],'no finishing page before done callback')
 private=json.loads(guest('cat '+root+'/private-connection.json').stdout);pin=private['pin']
 tunnel_port=port();tunnel_base='http://127.0.0.1:'+str(tunnel_port)
 tunnel=subprocess.Popen(ssh[:-1]+['-N','-o','ExitOnForwardFailure=yes','-L',f'127.0.0.1:{tunnel_port}:127.0.0.1:8080',ssh[-1]],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);resources.append(tunnel)
 def tunnel_ready():
  try:
   with urllib.request.urlopen(tunnel_base+'/'+pin,timeout=2) as r:return r.status==200
  except OSError:return False
 wait(tunnel_ready,15,'owned phone tunnel')
 proxy=server(Phone);driver_port=port();driver_base='http://127.0.0.1:'+str(driver_port)
 log=(a.out/'geckodriver.log').open('w')
 driver=subprocess.Popen(['/snap/firefox/current/usr/lib/firefox/geckodriver','--host','127.0.0.1','--port',str(driver_port)],stdout=log,stderr=subprocess.STDOUT);resources.append(driver)
 def driver_ready():
  try:return wd('GET','/status')['ready']
  except OSError:return False
 wait(driver_ready,15,'owned WebDriver')
 session=wd('POST','/session',{'capabilities':{'alwaysMatch':{'browserName':'firefox','moz:firefoxOptions':{'binary':'/usr/lib/firefox/firefox','args':['-headless']}}}});sid=session['sessionId']
 wd('POST','/session/'+sid+'/window/rect',{'width':600,'height':1200})
 wd('POST','/session/'+sid+'/url',{'url':'http://127.0.0.1:'+str(proxy.server_port)+'/proof-frame'})
 element=wd('POST','/session/'+sid+'/element',{'using':'css selector','value':'#phone'});wd('POST','/session/'+sid+'/frame',{'id':element})
 wait(lambda:js('return document.getElementById("state").textContent')=='Connected.',60,'actual phone handler probe')
 js('document.getElementById("leave-ask").click()')
 expected=['Fermer la page de connexion sur votre console ?','Garder ouverte','Fermer'] if a.language=='fr_FR' else ['Close the sign-in page on your handheld?','Keep','Close']
 text=js('return [document.querySelector("#leave-confirm span").textContent,document.getElementById("leave-keep").textContent,document.getElementById("leave-close").textContent]')
 assertion(text==expected,'actual phone confirmation language')
 phone_shot('phone-confirmation-'+a.language)
 js('document.getElementById("leave-keep").click()')
 assertion(js('return document.getElementById("leave-confirm").hidden') and state()['window_alive'],'Keep retains the installed window')
 js('document.getElementById("leave-ask").click();document.getElementById("leave-close").click()')
 wait(lambda:not state().get('window_alive',True),30,'phone Close ends installed window')
 assertion(not state()['done_exists'],'Close does not mark a successful sign-in')
 action('start-browser');wait(lambda:state().get('window_alive'),30,'new local window')
 action('signed-in')
 flag='is_finishing_fr' if a.language=='fr_FR' else 'is_finishing_en'
 wait(lambda:state().get(flag),60,'actual localized finishing document')
 start=time.monotonic()
 for offset in [0,5,15]:
  time.sleep(max(0,start+offset-time.monotonic()))
  facts=state();assertion(facts.get(flag) and facts.get('done_exists') and facts.get('window_alive'),'finishing retained at '+str(offset)+' seconds')
  if offset in [0,15]:native_shot('native-finishing-'+a.language+'-'+str(offset))
 action('stop-browser');wait(lambda:not state().get('window_alive',True),20,'explicit window dismissal')
 assertion(guest('sha256sum /usr/bin/cloud_oauth /usr/bin/cloud-signin-window /usr/bin/emulationstation').stdout==before,'installed presentation bytes unchanged')
finally:
 errors=[]
 viewer_stop.set()
 if viewer_thread:
  viewer_thread.join(8)
  if viewer_thread.is_alive() or viewer_errors:errors.append('persistent VNC viewer cleanup')
 if sid:
  try:wd('DELETE','/session/'+sid)
  except Exception:errors.append('WebDriver cleanup')
 if fixture_pid is not None:
  try:
   action('quit')
   wait(lambda:guest('test -e '+root+'/fixture.rc',check=False).returncode==0,20,'owned fixture cleanup')
   for name in ['observations.json','source.json','fixture.rc']:(a.out/name).write_text(guest('cat '+root+'/'+name).stdout)
   assertion(guest('cat '+root+'/fixture.rc').stdout.strip()=='0','owned installed window and server cleanup')
   guest('python3 -',data='''from pathlib import Path
import shutil
root=Path('/tmp/m7-signin-presentation')
assert (root/'fixture.rc').read_text().strip()=='0'
shutil.rmtree('/var/run/cloud_oauth')
shutil.rmtree(root)
''')
  except Exception:errors.append('guest fixture cleanup')
 for r in reversed(resources):
  if isinstance(r,subprocess.Popen):
   r.terminate()
   try:r.wait(timeout=10)
   except subprocess.TimeoutExpired:r.kill();r.wait()
  else:r.shutdown();r.server_close()
 (a.out/'result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'frames':frames,'cleanup_errors':errors,'scope':'actual installed presentation with local provider Session stand-in and explicit done callback; no OAuth exchange; direct visual review pending; queued reconnect UI is a separate proof'},indent=2)+'\n')
 assert not errors,errors
print('PASS installed localized presentation; direct frame review required',flush=True)
