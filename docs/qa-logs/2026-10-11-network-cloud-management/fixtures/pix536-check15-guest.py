from pathlib import Path
import urllib.request,urllib.parse,time,json,os
O=Path('/storage/qa537/browser15');P=O/'events.jsonl'
def post(**fields):
 fields['pin']='1234'
 with urllib.request.urlopen('http://127.0.0.1:9978/1234',urllib.parse.urlencode(fields).encode(),timeout=10) as r:assert r.status==204
def tap(x,y):
 post(move='-2000,-2000');post(move=f'{x},{y}');post(click='1');time.sleep(.6)
def paths():return [json.loads(x)['path'] for x in P.read_text().splitlines()]
def waitpath(want):
 for _ in range(40):
  if any(want in p for p in paths()):return True
  time.sleep(.1)
 return False
result={}
tap(120,90)
for event in ['mouseover','mousedown','mouseup','click']:
 result[event]=waitpath('/event?'+event+'=button')
result['button']=waitpath('/event?button=clicked')
tap(120,150);post(type='fixture');post(key='backspace')
result['typing_and_backspace']=waitpath('/event?input=fixtur')
post(key='tab');post(wheel='-5');time.sleep(1)
result['wheel_scroll']=any('/event?scroll=' in p and not p.endswith('=0') for p in paths())
post(wheel='100');time.sleep(1)
tap(120,210)
result['auth_link']=waitpath('/event?ready=%2Fnext')
post(key='backspace');time.sleep(1)
result['provider_handled_back_preserved']=waitpath('/event?prevented=1') and '/next' in Path('/var/run/cloud_oauth/page').read_text()
post(key='home');assert waitpath('/event?prevented=off')
import importlib.util,importlib.machinery,sys
sys.path.insert(0,'/usr/bin');loader=importlib.machinery.SourceFileLoader('fixture_oauth','/usr/bin/cloud_oauth');spec=importlib.util.spec_from_loader(loader.name,loader);c=importlib.util.module_from_spec(spec);loader.exec_module(c)
k=c.RemoteKeyboard();assert k.open();time.sleep(.4);k._tap(14,True);time.sleep(.4);k.close()
result['modified_back_preserved']='/next' in Path('/var/run/cloud_oauth/page').read_text()
post(key='backspace');time.sleep(1)
result['browser_back']=Path('/var/run/cloud_oauth/page').read_text().strip()=='http://dropbox.com:9977/'

# Keep the actual related popup's opener; close returns to an interactive parent.
tap(120,270);result['popup_loaded']=waitpath('/popup')
post(key='tab');post(key='enter');result['popup_return']=waitpath('/event?popup=returned')
tap(120,90);result['parent_usable']=Path('/var/run/cloud_oauth/page').read_text().strip()=='http://dropbox.com:9977/'
tap(120,330);time.sleep(.6)
result['unrelated_blocked']=not any(json.loads(x)['host'].startswith('unrelated.example') for x in P.read_text().splitlines())
(O/'partial.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));assert all(result.values())
