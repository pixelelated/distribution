from pathlib import Path
import json,time,subprocess,sys,shlex
from ui import out,remote
r=Path(__file__).parent;name,lang=sys.argv[1:];case=r/name;case.mkdir();repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');result={'rc':1,'started':time.time(),'language':lang}
def walk(keys,label):
 p=case/(label+'.steps');p.write_text('\n'.join(['wake','settle']+sum((['key '+k,'wait-for-change','settle'] for k in keys),[])+['shot '+label])+'\n')
 subprocess.run([str(repo/'tools/vm-visual-qa'),'--monitor',str(r/'vm/monitor.sock'),'run',str(p),'--outdir',str(case/label)],check=True,timeout=120)
def values():
 raw=out('cat /storage/.config/system/configs/system.cfg');keys=['global.autosave','gamecube.autosave','dreamcast.autosave']
 return {k:[l.split('=',1)[1] for l in raw.splitlines() if l.startswith(k+'=')] for k in keys}
try:
 remote('systemctl stop essway.service',capture_output=True)
 remote('. /etc/profile >/dev/null 2>&1; set_setting system.language '+shlex.quote(lang)+'; systemctl start essway.service',capture_output=True)
 end=time.monotonic()+45
 while time.monotonic()<end:
  if out('curl -fsS http://127.0.0.1:1234/isIdle 2>/dev/null || true').replace(' ','').strip()=='[true]':break
  time.sleep(.4)
 else:raise RuntimeError('frontend readiness')
 result['before']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip()
 result['settings_before']=values()
 walk(['ret','x'],'global-top');walk(['down']*6,'global-autosave');walk(['down']*2,'global-manager');walk(['z','z'],'returned')
 result['settings_after']=values();assert result['settings_after']==result['settings_before']
 assert out('cat /storage/qa575/launch-events')==''
 result['after']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();assert result['before']==result['after']
 result['rc']=0
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
