from pathlib import Path
import sys,json,time,subprocess,urllib.parse,traceback
from ui import out
from playwright.sync_api import sync_playwright,expect
r=Path(__file__).parent;target=Path(sys.argv[1]);target.mkdir();result={'rc':1,'started':time.time()};tunnel=None
try:
 info=dict(line.split('=',1) for line in out('cloud_oauth info').splitlines() if '=' in line)
 ssh=json.loads((r/'ssh-command.json').read_text());tunnel=subprocess.Popen(ssh[:-1]+['-N','-o','ExitOnForwardFailure=yes','-L','127.0.0.1:18080:127.0.0.1:8080',ssh[-1]],stdout=(target/'tunnel.stdout').open('w'),stderr=(target/'tunnel.stderr').open('w'))
 (target/'tunnel-pid.json').write_text(json.dumps({'pid':tunnel.pid})+'\n');time.sleep(.5);assert tunnel.poll() is None
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/home/max/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome')
  try:
   ctx=browser.new_context(viewport={'width':320,'height':800},service_workers='block');unexpected=[]
   def route(req):
    if urllib.parse.urlsplit(req.request.url).netloc=='127.0.0.1:18080':req.continue_()
    else:unexpected.append(req.request.url);req.abort()
   ctx.route('**/*',route);page=ctx.new_page();page.set_default_timeout(12000);page.goto('http://127.0.0.1:18080/'+info['PIN']);expect(page.locator('#state')).to_have_attribute('data-kind','connected')
   baseline=page.locator('#kb').bounding_box();page.screenshot(path=str(target/'01-connected.png'),full_page=True)
   page.evaluate("window.seenKinds=[];new MutationObserver(()=>seenKinds.push(document.querySelector('#state').dataset.kind)).observe(document.querySelector('#state'),{attributes:true,attributeFilter:['data-kind']});")
   page.locator('#kb').fill('first571');expect(page.locator('#kb')).to_have_value('',timeout=15000);expect(page.locator('#state')).to_have_attribute('data-kind','connected')
   assert page.locator('#kb').bounding_box()==baseline;page.screenshot(path=str(target/'02-next-page.png'),full_page=True)
   page.locator('#kb').fill('second571')
   end=time.monotonic()+10
   while time.monotonic()<end:
    rows=[json.loads(x) for x in out('cat /storage/qa570flows/typed.jsonl').splitlines()]
    if any(x=={'phase':'2','value':'second571'} for x in rows):break
    time.sleep(.2)
   else:raise RuntimeError('second-page input not delivered')
   assert {'phase':'1','value':'first571'} in rows
   result['seen_kinds']=page.evaluate('seenKinds');assert all(x=='connected' for x in result['seen_kinds'])
   result['delivered']=rows;page.screenshot(path=str(target/'03-second-delivered.png'),full_page=True);assert not unexpected;result['source_sha256']=out('sha256sum /usr/bin/cloud_oauth').split()[0];result['rc']=0
  finally:browser.close()
except BaseException as e:result['error']=str(e);traceback.print_exc()
finally:
 if tunnel:
  tunnel.terminate()
  try:tunnel.wait(5)
  except subprocess.TimeoutExpired:tunnel.kill();tunnel.wait(3)
  result['tunnel_exit']=tunnel.returncode
 result['ended']=time.time();(target/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
