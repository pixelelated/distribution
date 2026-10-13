#!/usr/bin/env python3
import json,re,subprocess,time,urllib.request,urllib.error,platform
from pathlib import Path
assert platform.machine()=='x86_64' and Path('/storage/qa-m7-baseline/library-fixture.py').exists(), 'Disposable QA guest required'
out=Path('/storage/qa-m7-baseline');cfg=Path('/storage/.config/emulationstation/es_settings.cfg')
results=[]
def fetch(path):
 try:
  with urllib.request.urlopen('http://127.0.0.1:1234'+path,timeout=3) as f:return f.status,json.load(f)
 except urllib.error.HTTPError as e:return e.code,None
def idle():
 end=time.monotonic()+60
 while time.monotonic()<end:
  try:
   if fetch('/isIdle')==(200,[True]):return
  except OSError:pass
  time.sleep(.5)
 raise RuntimeError('ES readiness timeout')
def setting(value):
 text=cfg.read_text();text=re.sub(r'<string\s+name="CollectionSystemsAuto"\s+value="[^"]*"\s*/>','',text)
 if value is not None:
  node='<string name="CollectionSystemsAuto" value="'+value+'" />\n'
  text=text.replace('</config>',node+'</config>') if '</config>' in text else text+'\n'+node
 cfg.write_text(text)
try:
 for label,value,expected in [('absent-default',None,404),('spaced','favorites, recent',404),('canonical','favorites,recent',200),('explicit-favorites-only','favorites',404)]:
  subprocess.run(['systemctl','stop','essway.service'],check=True,timeout=40);setting(value)
  subprocess.run(['systemctl','start','essway.service'],check=True,timeout=40);idle()
  status,recent=fetch('/systems/recent/games');code,systems=fetch('/systems');assert code==200 and status==expected
  if status==200:assert any(x.get('playcount')=='5' and x['path'].endswith('pixelelated-fixture.gb') for x in recent)
  row={'case':label,'recent_http_status':status,'system_names':[x['name'] for x in systems],'recent_games':recent,'pid':subprocess.check_output(['pidof','emulationstation'],text=True).strip(),'rc':0};results.append(row)
  (out/'collection-progress.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS '+label+' HTTP'+str(status),flush=True)
 (out/'collection-result.json').write_text(json.dumps({'rc':0,'cases':results},indent=2)+'\n')
finally:
 # Set a valid collection precondition for the separate history-copy test.
 subprocess.run(['systemctl','stop','essway.service'],check=True,timeout=40);setting('favorites,recent')
 for p in [Path('/storage/roms/gb/pixelelated-fixture.gb'),Path('/storage/roms/gb/gamelist.xml')]:
  b=p.read_bytes();assert b'pixelelated-fixture' in b or b'PIXELELATED SYNTHETIC METADATA FIXTURE' in b;p.unlink()
 subprocess.run(['systemctl','start','essway.service'],check=True,timeout=40);idle()
