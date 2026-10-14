from pathlib import Path
import subprocess,json,time,traceback
from ui import out
r=Path(__file__).parent;case=r/'capability-system-fr1280';repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');result={'rc':1,'started':time.time()}
def walk(keys,label):
 p=case/(label+'.steps');p.write_text('\n'.join(['wake','settle']+sum((['key '+k,'wait-for-change','settle'] for k in keys),[])+['shot '+label])+'\n')
 q=subprocess.run([str(repo/'tools/vm-visual-qa'),'--monitor',str(r/'vm/monitor.sock'),'run',str(p),'--outdir',str(case/label)],timeout=100);assert q.returncode==0
try:
 result['before']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe')
 settings=out('cat /storage/.config/system/configs/system.cfg');(case/'before-synthetic-system.cfg').write_text(settings)
 walk(['down','x'],'support-dialog');walk(['x','up','left'],'retroarch-selection');walk(['right'],'auto-restored');walk(['z','z','z','z'],'returned')
 observed=out('cat /storage/.config/system/configs/system.cfg');(case/'after-synthetic-system.cfg').write_text(observed)
 keys=['global.autosave','gamecube.autosave','dreamcast.autosave','gamecube.emulator','gamecube.core','dreamcast.emulator','dreamcast.core']
 def read(raw):return {k:[line.split('=',1)[1] for line in raw.splitlines() if line.startswith(k+'=')] for k in keys}
 result['settings_before']=read(settings);result['settings_after']=read(observed);assert result['settings_before']==result['settings_after']
 result['after']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe');assert result['before']==result['after']
 assert out('cat /storage/qa575/launch-events')==''
 result['rc']=0
except BaseException as e:result['error']=str(e);traceback.print_exc()
finally:
 result['ended']=time.time();(case/'finish-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
