from pathlib import Path
import json,subprocess,time,hashlib,shlex,traceback
from ui import out,remote,shot
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');packet=repo/'docs/qa-logs/2026-10-13-library-setup-source/fixtures';case=r/'recent-en640';case.mkdir();result={'rc':1,'started':time.time(),'cases':[]};dest='/storage/qa-library-578';binary='f6fd61b7bea859467f1a3b0e1f890c975bfef9aaafd1866e727752727de013b3'
def wait_idle():
 end=time.monotonic()+45
 while time.monotonic()<end:
  if out('curl -fsS http://127.0.0.1:1234/isIdle 2>/dev/null || true').replace(' ','').strip()=='[true]':return
  time.sleep(.5)
 raise RuntimeError('frontend readiness')
try:
 assert out('cloud_oauth status').strip()=='idle'
 assert not out('find /storage/roms/gb -type f').strip(),'GB fixture root not empty'
 remote('mkdir -p '+dest,capture_output=True)
 for f in packet.iterdir():
  if f.is_file():
   with f.open('rb') as h:remote('cat > '+dest+'/'+shlex.quote(f.name),stdin=h)
 remote('systemctl stop essway.service; cp /storage/.config/emulationstation/es_settings.cfg '+dest+'/original-settings.cfg',capture_output=True)
 spec=json.loads((packet/'collections.json').read_text())
 boot=out('cat /proc/sys/kernel/random/boot_id').strip()
 for spec_case in spec['cases']:
  name=spec_case['id'];g=dest+'/'+name
  remote('systemctl stop essway.service',capture_output=True)
  # Only this owner has created files under this initially empty GB directory.
  names=out('find /storage/roms/gb -type f').splitlines()
  assert all(Path(n).name in ['pixelelated-library-setup.gb','gamelist.xml','gamelist.xml.bak','gamelist.xml.tmp'] for n in names),names
  remote('rm -f /storage/roms/gb/pixelelated-library-setup.gb /storage/roms/gb/gamelist.xml /storage/roms/gb/gamelist.xml.bak /storage/roms/gb/gamelist.xml.tmp',capture_output=True)
  remote('python3 '+dest+'/prepare-collection-inputs.py --case '+name+' --settings '+dest+'/original-settings.cfg --out '+g,capture_output=True)
  remote('cp '+g+'/es_settings.cfg /storage/.config/emulationstation/es_settings.cfg; cp '+g+'/pixelelated-library-setup.gb /storage/roms/gb/',capture_output=True)
  if spec_case['history']:remote('cp '+g+'/gamelist.xml /storage/roms/gb/',capture_output=True)
  remote('. /etc/profile >/dev/null 2>&1; set_setting system.language en_US; systemctl start essway.service',capture_output=True);wait_idle()
  pid=out('pidof emulationstation').strip()
  p=subprocess.run(json.loads((r/'ssh-command.json').read_text())+['python3 '+dest+'/probe-collections.py --case '+name+' --pid '+pid+' --boot-id '+boot+' --binary-sha256 '+binary+' --out '+g+'/result.json'],capture_output=True,text=True,timeout=25)
  (case/(name+'.stdout')).write_text(p.stdout);(case/(name+'.stderr')).write_text(p.stderr)
  data=out('cat '+g+'/result.json');(case/(name+'.json')).write_text(data);entry=json.loads(data);entry['actual_exit']=p.returncode;result['cases'].append(entry)
  print(name,p.returncode,flush=True)
  assert p.returncode==0,entry
  if name in ['default-rom-only','default-history','retained-favorites']:
   shot(case/(name+'.png'))
  time.sleep(1)
 result['rc']=0
except BaseException as e:result['error']=str(e);traceback.print_exc()
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
