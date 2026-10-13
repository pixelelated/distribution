from pathlib import Path
import json,subprocess,time,hashlib
from ui import out,remote,shot
r=Path(__file__).parent;repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');packet=repo/'docs/qa-logs/2026-10-13-wifi-picker-source/fixtures';case=r/'wifi-en640-initial';case.mkdir();result={'rc':1,'started':time.time()}
try:
 result['identity_before']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip()
 remote('mkdir -p /storage/qa-wifi-577-setup; printf "577\\n" > /storage/qa-wifi-577-setup/ALLOW-SYNTHETIC-WIFI; cp /usr/bin/wifictl /storage/qa-wifi-577-setup/wifictl-original',capture_output=True)
 for source,name in [('wifictl-fixture.py','fixture.py'),('layout-plan.json','plan.json'),('state-empty.json','state.json')]:
  with (packet/source).open('rb') as f:remote('cat > /storage/qa-wifi-577-setup/'+name,stdin=f)
 wrapper='#!/bin/sh\nexport PIXELELATED_WIFI_577_DIR=/storage/qa-wifi-577-setup\nexec python3 /storage/qa-wifi-577-setup/fixture.py "$@"\n'
 remote('cat > /storage/qa-wifi-577-setup/wifictl',input=wrapper,text=True,capture_output=True)
 remote('chmod 755 /storage/qa-wifi-577-setup/wifictl; mount --bind /storage/qa-wifi-577-setup/wifictl /usr/bin/wifictl; mount --make-private /usr/bin/wifictl',capture_output=True)
 steps=case/'walk.steps';steps.write_text('wake\nkey ret\nwait-for-change\nsettle\nkey up x6\nkey x\nwait-for-change\nsettle\nshot network-settings\nkey down x5\nkey x\nwait 1\nshot initial-search\nwait 9\nsettle\nshot initial-results\n')
 p=subprocess.run([str(repo/'tools/vm-visual-qa'),'--monitor',str(r/'vm/monitor.sock'),'run',str(steps),'--outdir',str(case/'frames')],timeout=70);assert p.returncode==0
 events=out('cat /storage/qa-wifi-577-setup/calls.jsonl');(case/'calls.jsonl').write_text(events);rows=[json.loads(x) for x in events.splitlines()];assert sum(x['phase']=='start' and x['command'] in ['list','scanlist'] for x in rows)==1
 result['identity_after']=out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe').strip();assert result['identity_before']==result['identity_after'];result['rc']=0
finally:
 result['ended']=time.time();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(result['rc'])
