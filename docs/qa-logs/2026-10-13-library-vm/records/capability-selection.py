from pathlib import Path
import json,time,subprocess
from ui import out
r=Path(__file__).parent;case=r/'capability-selection-fr640';case.mkdir();repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');result={'rc':1,'started':time.time()}
def walk(keys,label):
 p=case/(label+'.steps');p.write_text('\n'.join(['wake','settle']+sum((['key '+k,'wait-for-change','settle'] for k in keys),[])+['shot '+label])+'\n')
 subprocess.run([str(repo/'tools/vm-visual-qa'),'--monitor',str(r/'vm/monitor.sock'),'run',str(p),'--outdir',str(case/label)],check=True,timeout=90)
def selected():
 keys=['global.autosave','dreamcast.autosave','dreamcast.emulator','dreamcast.core','dreamcast["pixelelated-capability.cdi"].emulator','dreamcast["pixelelated-capability.cdi"].core']
 raw=out('cat /storage/.config/system/configs/system.cfg').splitlines()
 return {k:[l.split('=',1)[1] for l in raw if l.startswith(k+'=')] for k in keys}
try:
 assert json.loads((r/'capability-small03-result.json').read_text())['rc']==0
 result['before']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();result['settings_before']=selected()
 assert result['settings_before']['dreamcast["pixelelated-capability.cdi"].emulator']==['retroarch']
 walk(['s','s'],'retroarch-before');walk(['left'],'auto-standalone');walk(['down','x'],'auto-help');walk(['x','up','right'],'retroarch-after');walk(['z'],'returned')
 result['after']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();assert result['before']==result['after']
 result['settings_after']=selected();assert result['settings_before']==result['settings_after']
 assert out('cat /storage/qa575/launch-events')==''
 result['rc']=0
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
