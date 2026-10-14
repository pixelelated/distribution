from pathlib import Path
import json,time
from ui import out
r=Path(__file__).parent;case=r/'capability-system-fr1280';original=json.loads((case/'finish-result.json').read_text());result={'rc':1,'utc':time.time(),'original_result_rc':original['rc'],'original_failure_preserved':True}
try:
 result['identity']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe');assert result['identity']==original['before']
 result['launch_events']=out('cat /storage/qa575/launch-events');assert result['launch_events']==''
 result['installed_defaults']=out("for p in /usr/config/system/configs/system.cfg /usr/config/system/configs/system.cfg.defaults /storage/.config/system/configs/system.cfg.defaults; do test ! -f \"$p\" || { echo \"$p\"; sed -n '/^gamecube\.emulator=/p; /^gamecube\.core=/p' \"$p\"; }; done")
 for k,before in original['settings_before'].items():
  after=original['settings_after'][k]
  if k in ('gamecube.emulator','gamecube.core'):assert before==[''] and after==[]
  else:assert before==after
 result['interpretation']='UI returned to AUTO after explicit selection changes. Empty emulator/core entries were removed by normal SystemConf persistence. Other five preferences unchanged. This is not byte-identical settings preservation; original exact-file assertion remains failed.'
 result['rc']=0
finally:(case/'readback-result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
