#!/usr/bin/env python3
import pathlib,hashlib,json,subprocess,socket,time,gzip,shutil,os
O=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008/guest01')
R=pathlib.Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
IMG=pathlib.Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/target/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz')
started=time.monotonic()
for port in [10220,5940]:
 with socket.socket() as sock:sock.bind(('127.0.0.1',port))
for name in ['/tmp/pix520-mon.sock','/tmp/pix520-ser.sock']:assert not pathlib.Path(name).exists(),name
with IMG.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
assert digest=='74e57ad8957b1c719c18db098d5713577a952af8802524658d0ada7dee1b6b12'
subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(O/'qa-key'),'-C','pixelelated-520-qa'],check=True)
with gzip.open(IMG,'rb') as src, (O/'image.img').open('wb') as dst:shutil.copyfileobj(src,dst,2**20)
subprocess.run(['qemu-img','convert','-f','raw','-O','qcow2',str(O/'image.img'),str(O/'vm.qcow2')],check=True)
subprocess.run(['qemu-img','resize',str(O/'vm.qcow2'),'16G'],check=True);(O/'image.img').unlink()
command=[str(R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm'),'run','--headless','--daemonize','--res','640x480','--ssh-port','10220','--vnc','40','--monitor','/tmp/pix520-mon.sock','--serial','/tmp/pix520-ser.sock','--pidfile',str(O/'vm.pid'),'--mac','52:54:00:52:52:20',str(O/'vm.qcow2')]
subprocess.run(command,check=True)
subprocess.run([str(R/'tools/vm-serial'),'--socket','/tmp/pix520-ser.sock','wait','--up-to','180'],check=True)
pub=(O/'qa-key.pub').read_text().strip()
subprocess.run([str(R/'tools/vm-serial'),'--socket','/tmp/pix520-ser.sock','sh',"mkdir -p /storage/.ssh; chmod 700 /storage/.ssh; printf '%s\\n' '"+pub+"' > /storage/.ssh/authorized_keys; chmod 600 /storage/.ssh/authorized_keys"],check=True,stdout=subprocess.DEVNULL)
ssh=['ssh','-i',str(O/'qa-key'),'-p','10220','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
for i in range(30):
 ready=subprocess.run(ssh+['grep ^BUILD_ID= /etc/os-release'],capture_output=True,text=True)
 if ready.returncode==0:break
 time.sleep(2)
else:raise RuntimeError('QA SSH did not become ready')
subprocess.run(ssh+['ip route del default 2>/dev/null || true; ip -6 route del default 2>/dev/null || true; ip route; ip -6 route'],check=True,stdout=(O/'network-boundary.txt').open('w'))
record={'image':str(IMG),'image_sha256':digest,'qemu_pid':int((O/'vm.pid').read_text()),'ssh_port':10220,'vnc_display':40,'monitor':'/tmp/pix520-mon.sock','serial':'/tmp/pix520-ser.sock','resolution':'640x480','command':command,'elapsed_seconds':round(time.monotonic()-started,3),'disk_logical_bytes':(O/'vm.qcow2').stat().st_size,'disk_allocated_bytes':(O/'vm.qcow2').stat().st_blocks*512,'owner':'rc_cloud_ui exclusive','purpose':'#520 changed-backend affected UI proof only','build_readback':ready.stdout.strip(),'qa_key':'guest01/qa-key; private key never archived'}
(O/'guest.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS',json.dumps(record),flush=True)
