from pathlib import Path
import subprocess,json
from ui import out
r=Path(__file__).parent;case=r/'capability-system-fr1280';repo=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
steps=case/'gamecube.steps';steps.write_text('wake\nkey down\nkey x\nwait-for-change\nsettle\nshot gamecube\n')
p=subprocess.run([str(repo/'tools/vm-visual-qa'),'--monitor',str(r/'vm/monitor.sock'),'run',str(steps),'--outdir',str(case/'gamecube')],timeout=45)
(case/'gamecube-result.json').write_text(json.dumps({'rc':p.returncode,'review':'PENDING','identity':out('cat /proc/sys/kernel/random/boot_id; pidof emulationstation; sha256sum /proc/$(pidof emulationstation)/exe')},indent=2)+'\n')
raise SystemExit(p.returncode)
