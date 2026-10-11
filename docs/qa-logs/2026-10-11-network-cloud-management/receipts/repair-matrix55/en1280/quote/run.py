from pathlib import Path
import importlib.util,subprocess,time,json
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');O=Path('/workspace/tmp/pix540-ui55/en1280/quote')
subprocess.run(['python3','/tmp/pix537-reset-ui.py','en_US'],check=True)
v.remote("systemctl stop essway; cp /storage/qa537/rclone-real /usr/bin/rclone; printf '[two words]\\ntype = alias\\nremote = /storage/qa537/provider\\n' > /storage/.config/rclone/rclone.conf; printf 'two words\\n' > /storage/.config/rclone/active-connection; chmod 600 /storage/.config/rclone/rclone.conf /storage/.config/rclone/active-connection; rm -f /tmp/emulationstation.ready; systemctl start essway")
for _ in range(100):
 if 'ready' in v.remote('test -f /tmp/emulationstation.ready && echo ready || true'):break
 time.sleep(.2)
else:raise RuntimeError('ES not ready')
v.remote("swaymsg -s /run/0-runtime-dir/sway-ipc.0.sock 'output Virtual-1 mode --custom 1280x800@60Hz'")
steps=Path('/tmp/pix537-full-lifecycle.steps').read_text().split('shot details')[0]+'shot details\nkey down x2\nkey x\nwait-for-change\nsettle\nshot check-result\n'
p=O/'quoted.steps';p.write_text(steps)
subprocess.run([str(D/'tools/vm-visual-qa'),'--monitor',str(v.O/'monitor.sock'),'run',str(p),'--outdir',str(O/'quoted')],check=True)
(O/'source.json').write_text(json.dumps({'binary_sha256':v.remote('sha256sum /usr/bin/emulationstation').split()[0],'state':v.remote('cloud_remote list')},indent=2)+'\n')
print('DONE first exact-source quoted-name walk',flush=True)
