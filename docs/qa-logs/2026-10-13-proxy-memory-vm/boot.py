import subprocess,gzip,shutil,json,datetime
from pathlib import Path
r=Path(__file__).parent
src=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261011T194522Z.g1a0266484423-from-ROCKNIX.img.gz')
raw=r/'disk.img'; disk=r/'disk.qcow2'
if disk.exists() or raw.exists(): raise SystemExit('Refusing existing disk')
import hashlib
expected=src.with_name(src.name+'.sha256').read_text().split()[0]
assert hashlib.file_digest(src.open('rb'),'sha256').hexdigest()==expected
print('Verified accepted image; expanding',flush=True)
with gzip.open(src,'rb') as s,raw.open('xb') as d:shutil.copyfileobj(s,d,8*1280*1280)
subprocess.run(['qemu-img','convert','-f','raw','-O','qcow2',str(raw),str(disk)],check=True)
subprocess.run(['qemu-img','resize',str(disk),'16G'],check=True)
raw.unlink()
args=['python3',str(r/'profile-vm.py'),'run',str(disk),'--headless','--daemonize','--gl','none','--res','640x480','--ssh-port','10575','--vnc','60','--pidfile',str(r/'vm.pid'),'--serial',str(r/'serial.sock'),'--monitor',str(r/'monitor.sock'),'--ovmf-vars',str(r/'OVMF.fd')]
print('Starting 2048 MiB diagnostic guest',flush=True)
subprocess.run(args,check=True)
subprocess.run(['tools/vm-serial','--socket',str(r/'serial.sock'),'wait','--up-to','240'],check=True)
print('Guest frontend ready; diagnostic guest remains owned by vm.pid',flush=True)
(r/'boot-result.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ready':True,'memory_mib':2048,'disk':str(disk),'source':str(src),'pidfile':str(r/'vm.pid')},indent=2)+'\n')
