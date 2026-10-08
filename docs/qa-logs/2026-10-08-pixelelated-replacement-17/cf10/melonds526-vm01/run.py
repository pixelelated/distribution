from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).parent;B=O.parent;R=Path('/workspace/repos/rocknix.worktrees/conflict-resolution');G=B/'guest03';data=B/'backend/data'
ssh=['ssh','-i',str(G/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
scp=['scp','-q','-i',str(G/'qa-key'),'-P','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
def guest(code,n,expected=0):
 q=subprocess.run(ssh+['bash -s'],input=code,capture_output=True,text=True,timeout=150);(O/(n+'.stdout')).write_text(q.stdout);(O/(n+'.stderr')).write_text(q.stderr);(O/(n+'.rc')).write_text(str(q.returncode)+'\n');assert q.returncode==expected,(n,q.returncode,q.stderr);return q.stdout
def put(src,name):
 p=O/name;p.write_bytes(src.read_bytes());subprocess.run(scp+[str(p),'root@127.0.0.1:/storage/cf526/'+name],check=True);return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():return {str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'directory' for p in sorted(data.rglob('*'))}
def save(n,v):(O/(n+'.json')).write_text(json.dumps(v,indent=2)+'\n')
guest('set -e\nsystemctl stop essway.service\nmkdir -p /storage/cf526\ntest ! -e /usr/config/melonDS\ntest ! -e /storage/.config/melonDS\n','preconditions')
hashes={n:put(src,n) for n,src in [('post-update',R/'projects/ROCKNIX/packages/rocknix/sources/post-update'),('melonds-upgrade-test',R/'tools/melonds-upgrade-test')]}
readback=guest('sha256sum /storage/cf526/post-update /storage/cf526/melonds-upgrade-test','source-readback')
assert [x.split()[0] for x in readback.splitlines()]==list(hashes.values())
witness='set -e\ncat /proc/sys/kernel/random/boot_id\nsha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf /storage/roms/nes/CF10.srm /storage/roms/savestates/nes/CF10.state /usr/bin/cloud_setup /usr/bin/cloud_sync_helper /usr/share/post-update /usr/bin/emulationstation\n. /etc/profile >/dev/null 2>&1\nprintf "startup="; get_setting cloudsync.startup\nprintf "gameexit="; get_setting cloudsync.gameexit\n'
before=guest(witness,'before');cloud=snapshot();save('cloud-before',cloud)
seed='set -e\nmkdir -p /storage/.config/melonDS\nprintf "HKJoy_Custom=99\\nScreenLayout=7\\n" > /storage/.config/melonDS/melonDS.ini\nprintf "keep owner extra\\n" > /storage/.config/melonDS/owner-extra.txt\nchmod 600 /storage/.config/melonDS/melonDS.ini\nsha256sum /storage/.config/melonDS/*\n'
original=guest(seed,'old-control-seed')
guest('timeout 120 /usr/share/post-update','installed-negative',1)
guest('test ! -e /storage/.config/melonDS','negative-deletion')
assert guest(witness,'after-negative')==before and snapshot()==cloud
guest('python3 /storage/cf526/melonds-upgrade-test --post-update /usr/share/post-update --busybox /usr/bin/busybox --output /storage/cf526/old.json','old-focused',1)
old=json.loads(guest('cat /storage/cf526/old.json','old-focused-report'));assert len(old['checks'])==15 and not any(x['pass'] for x in old['checks'])
assert guest(seed,'corrected-seed')==original
guest('timeout 120 bash /storage/cf526/post-update','corrected-full-hook')
assert guest('sha256sum /storage/.config/melonDS/*','owner-after')==original
assert guest(witness,'after-corrected')==before and snapshot()==cloud
guest('python3 /storage/cf526/melonds-upgrade-test --post-update /storage/cf526/post-update --busybox /usr/bin/busybox --output /storage/cf526/new.json','corrected-focused')
new=json.loads(guest('cat /storage/cf526/new.json','corrected-focused-report'));assert len(new['checks'])==15 and all(x['pass'] for x in new['checks'])
guest('timeout 120 bash /storage/cf526/post-update','corrected-full-repeat')
assert guest('sha256sum /storage/.config/melonDS/*','owner-repeat')==original
assert guest(witness,'after-repeat')==before and snapshot()==cloud
save('result',{'passed':True,'installed_old_full_hook_rc':1,'installed_old_deletes_owner_config':True,'corrected_source_full_hook_rc':0,'repeat_preserves_owner_files':True,'actual_vm_old_focused_failures':15,'actual_vm_corrected_focused_passes':15,'source_hashes':hashes,'cloud_local_payload_credentials_auto_choices_and_installed_bytes_unchanged':True,'scope':'corrected source script executed from /storage on replacement17; immutable installed product unchanged; new engineering image inclusion REQUIRED'})
print('PASS #526 actual old deletion/rc1; corrected full hook twice preserves all state; 15 BusyBox controls pass; corrected source still needs image inclusion',flush=True)
