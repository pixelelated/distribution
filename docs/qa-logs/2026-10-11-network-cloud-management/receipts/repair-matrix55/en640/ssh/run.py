from pathlib import Path
import importlib.util,subprocess,time,json
s=importlib.util.spec_from_file_location('v','/tmp/pix537-vm.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
D=Path('/workspace/repos/rocknix.worktrees/m7-cloud-connections');O=Path('/workspace/tmp/pix540-ui55/en640/ssh')
subprocess.run(['python3','/tmp/pix537-reset-ui.py','en_US'],check=True)
v.remote("systemctl stop essway; printf '[spare]\\ntype = alias\\nremote = /storage/qa537/provider\\n' > /storage/.config/rclone/rclone.conf; printf '\\n' > /storage/.config/rclone/active-connection; . /etc/profile >/dev/null 2>&1; set_setting root.password QA-EXAMPLE-ONLY; rm -f /tmp/emulationstation.ready; systemctl start essway")
for _ in range(100):
 if 'ready' in v.remote('test -f /tmp/emulationstation.ready && echo ready || true'):break
 time.sleep(.2)
else:raise RuntimeError('ES not ready')
steps=Path('/tmp/pix537-full-lifecycle.steps').read_text().split('shot connections')[0]+'shot unselected\nkey up x2\nkey x\nwait-for-change\nsettle\nshot ssh-chooser\nkey up x3\nkey x\nwait-for-change\nsettle\nshot ssh-step1\nkey up\nkey right\nkey x\nwait-for-change\nsettle\nkey up\nkey right\nkey x\nwait-for-change\nsettle\nshot ssh-final\n'
p=O/'ssh.steps';p.write_text(steps)
child=subprocess.Popen(['ssh',*v.opts,'-p',str(v.G['ssh_port']),'root@127.0.0.1','sleep 90'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:subprocess.run([str(D/'tools/vm-visual-qa'),'--monitor',str(v.O/'monitor.sock'),'run',str(p),'--outdir',str(O/'ssh')],check=True)
finally:child.terminate();child.wait()
print('DONE real SSH wizard walk',flush=True)
