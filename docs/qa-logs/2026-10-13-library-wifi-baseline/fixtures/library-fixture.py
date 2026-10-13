#!/usr/bin/env python3
# Synthetic QA guest only. Never launch the stub ROM or use on an owner device.
import datetime,hashlib,json,subprocess,time,urllib.request,urllib.error
from pathlib import Path
out=Path('/storage/qa-m7-baseline');out.mkdir(exist_ok=True)
root=Path('/storage/roms/gb');rom=root/'pixelelated-fixture.gb';xml=root/'gamelist.xml'
report={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'cases':[],'scope':'synthetic ROM stub; no emulator or cloud operation'}
def run(*args):return subprocess.run(args,check=True,capture_output=True,text=True,timeout=40).stdout
def request(path):
 try:
  with urllib.request.urlopen('http://127.0.0.1:1234'+path,timeout=3) as f:return json.load(f)
 except urllib.error.HTTPError as e:
  if e.code==404:return []
  raise
def idle():
 end=time.monotonic()+70
 while time.monotonic()<end:
  try:
   if request('/isIdle')==[True]:return
  except (OSError,ValueError):pass
  time.sleep(.5)
 raise RuntimeError('ES readiness deadline')
def state():
 # Keep values in memory only; emit equality/presence, never values or hashes.
 configs={}
 for rel in ['system/configs/system.cfg','retroarch/retroarch.cfg','emulationstation/es_settings.cfg']:
  p=Path('/storage/.config')/rel
  configs[rel]=sorted(x for x in p.read_text().splitlines() if any(v in x.lower() for v in ['retroachievement','cheevos_','screenscraper','rclone'])) if p.exists() else None
 files={}
 for p in [Path('/storage/.config/rclone/rclone.conf'),Path('/storage/.config/rclone/active-connection')]:files[str(p)]=p.read_bytes() if p.exists() else None
 p=Path('/storage/.cache/cloud_sync')
 for f in p.rglob('*') if p.exists() else []:
  if f.is_file():files[str(f)]=f.read_bytes()
 return configs,files
try:
 idle();assert not rom.exists() and not xml.exists(),'Requires untouched synthetic GB fixture paths'
 before=state();initial=request('/systems/recent/games');assert initial==[], 'Fresh fixture requires empty Recent'
 report['initial_recent_count']=len(initial)
 for name,history in [('rom-only',False),('rom-plus-gamelist',True)]:
  run('systemctl','stop','essway.service')
  root.mkdir(exist_ok=True);rom.write_bytes(b'PIXELELATED SYNTHETIC METADATA FIXTURE\n')
  if history:xml.write_text('<?xml version="1.0"?><gameList><game><path>./pixelelated-fixture.gb</path><name>Metadata fixture</name><playcount>5</playcount><lastplayed>20260908T031024</lastplayed><favorite>true</favorite></game></gameList>\n')
  else:assert not xml.exists()
  run('systemctl','start','essway.service');idle()
  games=request('/systems/gb/games');recent=request('/systems/recent/games')
  row=next(x for x in games if x['path'].endswith('/pixelelated-fixture.gb'))
  found=[x for x in recent if x['path'].endswith('/pixelelated-fixture.gb')]
  assert bool(found)==history,(name,'Recent membership mismatch')
  assert int(row.get('playcount','0'))==(5 if history else 0)
  if history:assert row['lastplayed']=='20260908T031024'
  after=state();assert before==after, 'Account or cloud activity state changed'
  case={'case':name,'rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'playcount':int(row.get('playcount','0')),'lastplayed':row.get('lastplayed',''),'recent_member':bool(found),'selected_account_and_cloud_activity_unchanged':True,'frontend_pid':run('pidof','emulationstation').strip(),'rc':0}
  report['cases'].append(case);(out/(name+'.json')).write_text(json.dumps({'case':case,'gb':games,'recent':recent},indent=2)+'\n')
  print('PASS '+name+' Recent='+str(bool(found)),flush=True)
 assert report['cases'][0]['rom_sha256']==report['cases'][1]['rom_sha256']
 report['rc']=0
except BaseException as e:
 report.update(rc=1,error=str(e));raise
finally:
 report['ended']=datetime.datetime.now(datetime.timezone.utc).isoformat();(out/'library-result.json').write_text(json.dumps(report,indent=2)+'\n')
