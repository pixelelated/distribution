from pathlib import Path
import sys,json,time,subprocess,xml.etree.ElementTree as ET,re,traceback,importlib.util,importlib.machinery,shlex
from ui import out,remote,shot
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');name,lang,variant=sys.argv[1:];case=r/name;case.mkdir();result={'rc':1,'started':time.time(),'language':lang,'variant':variant};dest='/storage/qa-notice-567'
loader=importlib.machinery.SourceFileLoader('vq',str(repo/'tools/vm-visual-qa'));spec=importlib.util.spec_from_loader(loader.name,loader);vq=importlib.util.module_from_spec(spec);loader.exec_module(vq);mon=vq.Monitor(str(r/'vm/monitor.sock'))
def wait_idle():
 end=time.monotonic()+45
 while time.monotonic()<end:
  if out('curl -fsS http://127.0.0.1:1234/isIdle 2>/dev/null || true').replace(' ','').strip()=='[true]':return
  time.sleep(.3)
 raise RuntimeError('frontend readiness')
def walk(keys):
 lines=[]
 for k in keys:lines+=['key '+k,'wait-for-change','settle']
 vq.run_steps(mon,lines,str(case/'walk'))
def frame(label):
 stable,_=vq.settle(mon.frame,timeout=12,quiet=1);assert stable;shot(case/(label+'.png'))
routes={}
try:
 assert out('cloud_oauth status').strip()=='idle'
 remote('systemctl stop essway.service; mkdir -p '+dest,capture_output=True)
 result['original_routes']={}
 for family in ['4','6']:
  result['original_routes'][family]=out('ip -'+family+' route show default').splitlines()
  remote('ip -'+family+' route add unreachable default metric 1',capture_output=True)
  routes[family]=True
 for family,address in [('4','198.51.100.1'),('6','2001:db8::1')]:
  p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+['ip -'+family+' route get '+address],capture_output=True,text=True,timeout=10)
  assert p.returncode!=0,(family,p.stdout)
 # This fixture owns the sole GB game, proven in the previous isolated matrix.
 assert all(Path(p).name in ['pixelelated-library-setup.gb','gamelist.xml','gamelist.xml.bak','gamelist.xml.tmp'] for p in out('find /storage/roms/gb -type f').splitlines())
 with (repo/'docs/qa-logs/2026-10-13-library-setup-source/fixtures/indexed.gamelist.xml').open('rb') as f:remote('cat > /storage/roms/gb/gamelist.xml',stdin=f)
 raw=out('cat /storage/qa-library-578/original-settings.cfg');raw=re.sub(r'^\s*<\?xml[^?]*\?>','',raw,count=1);wrap=ET.fromstring('<fixture>'+raw+'</fixture>');root=list(wrap)[0] if len(wrap)==1 and list(wrap)[0].tag=='config' else wrap;root.tag='config'
 for node in list(root):
  if node.get('name') in ['CheevosCheckIndexesAtStart','NetPlayCheckIndexesAtStart','StartupSystem','StartupOnGameList']:root.remove(node)
 ET.SubElement(root,'bool',name='CheevosCheckIndexesAtStart',value='false' if variant=='index-off' else 'true');ET.SubElement(root,'bool',name='NetPlayCheckIndexesAtStart',value='false')
 ET.SubElement(root,'string',name='StartupSystem',value='gb');ET.SubElement(root,'bool',name='StartupOnGameList',value='false')
 remote('cat > /storage/.config/emulationstation/es_settings.cfg',input=ET.tostring(root),capture_output=True)
 remote('mkdir -p /storage/.config/emulationstation/scripts/update-gamelists',capture_output=True)
 hook='#!/bin/sh\nprintf "%s\\n" event >> '+dest+'/events\n'
 remote('cat > /storage/.config/emulationstation/scripts/update-gamelists/qa567.sh',input=hook,text=True,capture_output=True)
 remote('chmod 755 /storage/.config/emulationstation/scripts/update-gamelists/qa567.sh; : > '+dest+'/events',capture_output=True)
 remote('. /etc/profile >/dev/null 2>&1; set_setting global.retroachievements.offlineproxy '+('0' if variant=='off' else '1')+'; set_setting system.language '+lang+'; systemctl start essway.service',capture_output=True);wait_idle()
 result['before']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();assert 'f6fd61b7bea859467f1a3b0e1f890c975bfef9aaafd1866e727752727de013b3' in result['before']
 vq.run_steps(mon,['wake','settle'],str(case/'initial'));walk(['ret','x']);frame('game-settings');walk(['x']);frame('confirmation')
 assert out('cat '+dest+'/events')==''
 walk(['right','x']);frame('no-returned');assert out('cat '+dest+'/events')==''
 walk(['x','z']);frame('back-returned');assert out('cat '+dest+'/events')==''
 walk(['x']);mon.sendkey('x');wait_idle();time.sleep(1);frame('yes-returned')
 events=out('cat '+dest+'/events');(case/'events.txt').write_text(events);assert events.count('event')==1,repr(events)
 result['after']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();assert result['before']==result['after']
 for family,address in [('4','198.51.100.1'),('6','2001:db8::1')]:
  p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+['ip -'+family+' route get '+address],capture_output=True,text=True,timeout=10)
  assert p.returncode!=0,(family,p.stdout)
 result['event_count']=1;result['rc']=0
except BaseException as e:result['error']=str(e);traceback.print_exc()
finally:
 result['route_cleanup']=[]
 for family in routes:
  p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+['ip -'+family+' route del unreachable default metric 1'],capture_output=True,text=True,timeout=10)
  result['route_cleanup'].append({'family':family,'rc':p.returncode,'stderr':p.stderr})
  if p.returncode:result['rc']=1
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
