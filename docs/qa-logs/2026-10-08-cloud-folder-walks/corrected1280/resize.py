from pathlib import Path
import json,subprocess
O=Path(__file__).parent;P=Path('/workspace/tmp/pixelelated-m7-walk527-03')
R=Path('/workspace/repos/rocknix.worktrees/m7-p5-cloud-folder-walks')
g=json.loads((P/'guest.json').read_text())
subprocess.run([str(R/'tools/vm-stop'),'/tmp/rocknix-qemu-d.pid',str(P/'vm.qcow2')],check=True)
cmd=g['command'];cmd[cmd.index('--res')+1]='1280x800'
subprocess.run(cmd,check=True)
subprocess.run([str(R/'tools/vm-serial'),'--socket','/tmp/rocknix-qemu-serial-d.sock','wait','--up-to','180'],check=True)
g.update(command=cmd,resolution='1280x800',qemu_pid=int(Path('/tmp/rocknix-qemu-d.pid').read_text()))
(O/'guest.json').write_text(json.dumps(g,indent=2)+'\n')
