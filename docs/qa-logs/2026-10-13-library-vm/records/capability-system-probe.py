from pathlib import Path
import subprocess,json,time
from ui import out
r=Path(__file__).parent;case=r/'capability-system-fr1280';case.mkdir();repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
steps=case/'open.steps';steps.write_text('wake\nkey ret\nwait-for-change\nsettle\nkey x\nwait-for-change\nsettle\nkey up x2\nsettle\nshot system-row\n')
p=subprocess.run([str(repo/'tools/vm-visual-qa'),'--monitor',str(r/'vm/monitor.sock'),'run',str(steps),'--outdir',str(case/'open')],timeout=80)
(case/'probe.json').write_text(json.dumps({'rc':p.returncode,'review':'PENDING','identity':out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe')},indent=2)+'\n')
raise SystemExit(p.returncode)
