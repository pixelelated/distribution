import sys,json,time
from pathlib import Path
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
remote('systemctl stop essway; cp -a /storage/.config/cloud_sync.conf /storage/qa-manual-ui/before-boot-proof.conf; mkdir -p /storage/qa-manual-ui/provider/ROCKNIX/Saves/savefiles; printf synthetic-preserved-save > /storage/qa-manual-ui/provider/ROCKNIX/Saves/savefiles/keep.srm')
remote("sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"/ROCKNIX/Saves\"|' /storage/.config/cloud_sync.conf; sync")
boot_hashes=remote('sha256sum /storage/.config/rclone/rclone.conf /storage/.config/cloud_sync.conf /storage/qa-manual-ui/provider/ROCKNIX/Saves/savefiles/keep.srm')
(A/'boot-preservation-before.log').write_text(boot_hashes)
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
remote('nohup /usr/bin/rclone serve webdav /storage/qa-manual-ui/provider --addr 127.0.0.1:9867 --dir-cache-time 0s > /storage/qa-manual-ui/provider.log 2>&1 < /dev/null & echo $! > /storage/qa-manual-ui/provider.pid')
pid=int(Path(G['pidfile']).read_text());(A/'qemu-1280x800-owner.json').write_text(json.dumps({'pid':pid,'stat':Path('/proc',str(pid),'stat').read_text(),'argv':Path('/proc',str(pid),'cmdline').read_text().replace('\0',' ')},indent=2)+'\n')
(A/'provider-1280-owner.log').write_text(remote('cat /storage/qa-manual-ui/provider.pid; cat /proc/$(cat /storage/qa-manual-ui/provider.pid)/stat; sha256sum /usr/bin/cloud_setup /usr/bin/cloud_scan /usr/bin/cloud_backup'))
remote('mount --bind /storage/qa-manual-ui/es-final08 /usr/bin/emulationstation; mount --bind /storage/qa-manual-ui/fr-final09.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo')
start('en_US')
walk('1280x800-final-boot-preservation','wake\nwait 20\nsettle\nshot carousel-no-migration')
after=remote('sha256sum /storage/.config/rclone/rclone.conf /storage/.config/cloud_sync.conf /storage/qa-manual-ui/provider/ROCKNIX/Saves/savefiles/keep.srm')
assert boot_hashes==after,'boot modified selected path/config or synthetic data'
proof=after+remote("grep '^SAVES_REMOTE=' /storage/.config/cloud_sync.conf; sha256sum /usr/bin/emulationstation /usr/bin/cloud_setup /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; test ! -e /usr/bin/cloud_migrate_layout && echo MIGRATION_ABSENT; grep -E 'cloud folder|migration|cloud_setup|cloud_remote' /var/log/es_log.txt || true")
(A/'boot-preservation-after.log').write_text(proof)
remote('systemctl stop essway; cp -a /storage/qa-manual-ui/before-boot-proof.conf /storage/.config/cloud_sync.conf; sync')
print('PASS source-overlay startup retains legacy path, connection, and data',flush=True)
sys.argv=['matrix','1280x800'];exec(compile(Path('/tmp/pixelelated-508-matrix-final-v2.py').read_text(),'/tmp/pixelelated-508-matrix-final-v2.py','exec'))
