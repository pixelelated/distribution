from pathlib import Path
import subprocess,json,hashlib
O=Path(__file__).parent;B=O.parent;R=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18');G=B/'guest01';data=B/'backend/data'
ssh=['ssh','-i',str(G/'qa-key'),'-p','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5','root@127.0.0.1']
scp=['scp','-q','-i',str(G/'qa-key'),'-P','10230','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null']
def guest(code,n):
 q=subprocess.run(ssh+['bash -s'],input=code,capture_output=True,text=True,timeout=150);(O/(n+'.stdout')).write_text(q.stdout);(O/(n+'.stderr')).write_text(q.stderr);(O/(n+'.rc')).write_text(str(q.returncode)+'\n');q.check_returncode();return q.stdout

def snapshot():return {str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'directory' for p in sorted(data.rglob('*'))}
guest('set -e\nsystemctl stop essway.service\nmkdir -p /storage/cf526\ntest ! -e /usr/config/melonDS\ntest ! -e /storage/.config/melonDS\n','preconditions')
installed=guest('sha256sum /usr/share/post-update','installed-hash').split()[0]
assert installed==hashlib.sha256((R/'projects/ROCKNIX/packages/rocknix/sources/post-update').read_bytes()).hexdigest()
script=R/'tools/melonds-upgrade-test';subprocess.run(scp+[str(script),'root@127.0.0.1:/storage/cf526/melonds-upgrade-test'],check=True)
assert guest('sha256sum /storage/cf526/melonds-upgrade-test','test-hash').split()[0]==hashlib.sha256(script.read_bytes()).hexdigest()
witness='set -e\ncat /proc/sys/kernel/random/boot_id\nsha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf /storage/roms/nes/CF10.srm /storage/roms/savestates/nes/CF10.state /usr/bin/cloud_setup /usr/bin/cloud_sync_helper /usr/share/post-update /usr/bin/emulationstation\n. /etc/profile >/dev/null 2>&1\nprintf "startup="; get_setting cloudsync.startup\nprintf "gameexit="; get_setting cloudsync.gameexit\n'
before=guest(witness,'before');cloud=snapshot();(O/'cloud-before.json').write_text(json.dumps(cloud,indent=2)+'\n')
seed='set -e\nmkdir -p /storage/.config/melonDS\nprintf "HKJoy_Custom=99\\nScreenLayout=7\\n" > /storage/.config/melonDS/melonDS.ini\nprintf "keep owner extra\\n" > /storage/.config/melonDS/owner-extra.txt\nchmod 600 /storage/.config/melonDS/melonDS.ini\nsha256sum /storage/.config/melonDS/*\n'
original=guest(seed,'owner-seed')
for phase in ['full-hook','full-repeat']:
 guest('timeout 120 /usr/share/post-update',phase)
 assert guest('sha256sum /storage/.config/melonDS/*','owner-'+phase)==original
 assert guest('stat -c %a /storage/.config/melonDS/melonDS.ini','mode-'+phase).strip()=='600'
 assert guest(witness,'witness-'+phase)==before and snapshot()==cloud
 guest('python3 /storage/cf526/melonds-upgrade-test --post-update /usr/share/post-update --busybox /usr/bin/busybox --output /storage/cf526/result.json','focused-'+phase)
 result=json.loads(guest('cat /storage/cf526/result.json','focused-report-'+phase))
 assert result['pass'] and len(result['checks'])==15 and all(x['pass'] for x in result['checks'])
 assert result['post_update_sha256']==installed
(O/'result.json').write_text(json.dumps({'passed':True,'installed_post_update_sha256':installed,'full_hook_twice':True,'actual_busybox_cases':15,'source_overlay':False,'local_files_modes_cloud_credentials_choices_unchanged':True},indent=2)+'\n')
print('PASS installed whole hook twice; owner INI and extra file retained;15 actual VM controls pass',flush=True)
