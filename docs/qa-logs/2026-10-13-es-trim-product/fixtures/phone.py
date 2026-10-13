from ui import *
from playwright.sync_api import sync_playwright
import shlex
case=r/'phone';case.mkdir();(r/'page-server/case.json').write_text(json.dumps({'name':'phone-product'}))
def identity():return out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation').strip()
def events():
 p=r/'page-server/events.jsonl'
 return [json.loads(l) for l in p.read_text().splitlines() if json.loads(l).get('run')=='phone-product'] if p.exists() else []
def waitfor(fn,seconds,label,page=None):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  if fn():return
  if page:page.wait_for_timeout(150)
  else:time.sleep(.15)
 raise RuntimeError(label)
result={'rc':1,'before':identity()};tunnel=None;opened=False
try:
 with socket.socket() as s:s.bind(('127.0.0.1',10603))
 tunnel=subprocess.Popen(ssh[:-1]+['-N','-L','127.0.0.1:10603:10.0.2.15:8080',ssh[-1]],stdout=(case/'tunnel.log').open('wb'),stderr=subprocess.STDOUT)
 code='import json; print(json.load(open("/var/run/cloud_oauth/session.json"))["pin"])';pin=out('python3 -c '+shlex.quote(code)).strip();assert pin.isdecimal()
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/home/max/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome',args=['--disable-dev-shm-usage'])
  context=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);phone=context.new_page();phone.goto('http://127.0.0.1:10603/'+pin,wait_until='domcontentloaded',timeout=15000)
  key('x');opened=True
  for n in [0,1]:
   waitfor(lambda:any(e.get('kind')=='loaded' and e['n']==n for e in events()),35,'page not loaded '+str(n),phone)
   waitfor(lambda:phone.locator('#state').inner_text()=='Connected.',15,'phone not connected',phone)
   phone.locator('#clear').click();phone.locator('#kb').fill('a'*16)
   waitfor(lambda:any(e.get('kind')=='input' and e['n']==n and e['length']==16 and e['valid'] for e in events()),15,'phone input not applied',phone)
   shot(case/('page-'+str(n)+'.png'));phone.screenshot(path=str(case/('phone-'+str(n)+'.png')),full_page=True)
  key('esc');waitfor(lambda:out('pidof cloud-signin-window || true').strip()=='',20,'browser did not exit');opened=False
  time.sleep(2);shot(case/'returned.png');result['after']=identity();assert result['before']==result['after'];result.update(rc=0,events=events(),input_scope='actual remote phone page in host Chromium;16 characters applied on each of two page loads')
  context.close();browser.close()
finally:
 if opened:
  try:remote('/usr/bin/cloud_oauth close',capture_output=True)
  except Exception:pass
 if tunnel and tunnel.poll() is None:tunnel.terminate();tunnel.wait(timeout=10)
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
