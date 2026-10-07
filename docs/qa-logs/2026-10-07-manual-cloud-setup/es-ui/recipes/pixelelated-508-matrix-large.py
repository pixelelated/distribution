import sys,json,time
from pathlib import Path
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
remote('systemctl stop essway; sync')
run([R/'tools/vm-stop',G['pidfile'],G['disk']])
with open(A/'qemu-1280x800.log','w') as f:
 run([R/'projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm','run','--headless','--daemonize','--monitor',MON,'--serial',G['serial'],'--pidfile',G['pidfile'],'--vnc','58','--ssh-port',PORT,'--mac','52:54:00:50:50:58','--res','1280x800',G['disk']],stdout=f,stderr=subprocess.STDOUT)
run([R/'tools/vm-serial','--socket',G['serial'],'wait','--up-to','300'])
for i in range(60):
 try:
  remote('systemctl stop essway');break
 except Exception:time.sleep(2)
else:raise RuntimeError('SSH did not return after resize boot')
remote('mkdir -p /storage/qa-508/upper /storage/qa-508/work; mount -t overlay overlay -o lowerdir=/usr/bin,upperdir=/storage/qa-508/upper,workdir=/storage/qa-508/work /usr/bin; mount --bind /storage/qa-508/cloud_sync.conf /usr/config/cloud_sync.conf; mount --bind /storage/qa-508/cloud_sync.conf.defaults /usr/config/cloud_sync.conf.defaults; mount --bind /storage/qa-manual-ui/cloud_setup-final /usr/bin/cloud_setup; test ! -e /usr/bin/cloud_migrate_layout')
remote('nohup /usr/bin/rclone serve webdav /storage/qa-manual-ui/provider --addr 127.0.0.1:9867 > /storage/qa-manual-ui/provider.log 2>&1 < /dev/null & echo $! > /storage/qa-manual-ui/provider.pid')
pid=int(Path(G['pidfile']).read_text());(A/'qemu-1280x800-owner.json').write_text(json.dumps({'pid':pid,'stat':Path('/proc',str(pid),'stat').read_text(),'argv':Path('/proc',str(pid),'cmdline').read_text().replace('\0',' ')},indent=2)+'\n')
(A/'provider-1280-owner.log').write_text(remote('cat /storage/qa-manual-ui/provider.pid; cat /proc/$(cat /storage/qa-manual-ui/provider.pid)/stat; sha256sum /usr/bin/cloud_setup /usr/bin/cloud_scan /usr/bin/cloud_backup'))
sys.argv=['matrix','1280x800'];exec(compile(Path('/tmp/pixelelated-508-matrix.py').read_text(),'/tmp/pixelelated-508-matrix.py','exec'))
