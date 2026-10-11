from pathlib import Path
import importlib.util,subprocess,json
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');O=Path('/workspace/tmp/pix540-ui55/fr1280/missing')
def walk(label,steps):
 p=O/(label+'.steps');p.write_text(steps)
 subprocess.run([str(D/'tools/vm-visual-qa'),'--monitor',str(v.O/'monitor.sock'),'run',str(p),'--outdir',str(O/label)],check=True)
before=v.remote('sha256sum /storage/.config/rclone/rclone.conf /storage/qa537/provider/save.srm')
walk('missing-open','key x\nkey down x2\nkey x\nwait-for-change\nsettle\nshot edit\nkey up x2\nkey x\nwait-for-change\nsettle\nshot confirm\n')
v.remote("printf 'missing\\n' > /storage/.config/rclone/active-connection")
walk('missing-error','key x\nwait-for-change\nsettle\nshot missing-selection\n')
assert before==v.remote('sha256sum /storage/.config/rclone/rclone.conf /storage/qa537/provider/save.srm')
(O/'result.json').write_text(json.dumps({'config_payload_unchanged':True,'binary':v.remote('sha256sum /usr/bin/emulationstation').split()[0]},indent=2)+'\n')
