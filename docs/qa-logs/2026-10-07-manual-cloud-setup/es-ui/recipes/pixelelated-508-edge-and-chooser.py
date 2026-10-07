import sys,json,time,hashlib
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
remote('systemctl stop essway')
before=remote('sha256sum /storage/.config/rclone/rclone.conf /storage/.config/cloud_sync.conf; find /storage/qa-manual-ui/provider -type f -exec sha256sum {} \; | sort')
scp('/tmp/pixelelated-508-edge-fix/cloud_setup-sealed','/storage/qa-manual-ui/cloud_setup-edge')
scp('/tmp/pixelelated-508-edge-fix/guest-check.sh','/storage/qa-manual-ui/edge-check.sh')
remote('chmod 755 /storage/qa-manual-ui/cloud_setup-edge; mount --bind /storage/qa-manual-ui/cloud_setup-edge /usr/bin/cloud_setup')
log=remote('bash /storage/qa-manual-ui/edge-check.sh')
assert log.count('VERIFIED')==11,log
(A/'final-edge-guards.log').write_text(log)
after=remote('sha256sum /storage/.config/rclone/rclone.conf /storage/.config/cloud_sync.conf; find /storage/qa-manual-ui/provider -type f -exec sha256sum {} \; | sort')
assert before==after,'edge fixture changed original data/config'
assert remote('test ! -e /storage/.config/profile.d/zz-508-edge-readback.sh && test ! -e /storage/qa-508-edge-readback/bin && echo RESTORED').strip()=='RESTORED'
(A/'edge-provider-unchanged.log').write_text(after)
log=remote('/usr/bin/cloud_setup --seed-folders; rc=$?; echo SEED_RC=$rc; sha256sum /usr/bin/cloud_setup')
assert 'SEED_RC=0' in log and log.count('OK ')==4,log
(A/'final-edge-ordinary-seed.log').write_text(log)
print('PASS 10 focused shell controls plus credentials/config/provider preservation and ordinary seed',flush=True)
import sys,json,time
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
remote('systemctl stop essway; cp -a /storage/.config/cloud_sync.conf /storage/qa-manual-ui/before-chooser.conf')
remote("sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE=\"/manual-choice\"|' /storage/.config/cloud_sync.conf; . /etc/profile >/dev/null 2>&1; set_setting cloudsync.pick.restore.saves 0; set_setting cloudsync.pick.restore.content 1; set_setting cloudsync.pick.restore.media 0; set_setting cloudsync.pick.restore.settings 0; sync")
before=remote('sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; grep -E "^(SAVES|SYSTEM|CONTENT)_REMOTE=" /storage/.config/cloud_sync.conf; find /storage/qa-manual-ui/provider -type f -exec sha256sum {} \\; | sort; /usr/bin/cloud_setup --content-location')
assert 'STATE=found-elsewhere' in before and 'FOUND=/pixelelated/Content' in before,before
(A/'chooser-before.log').write_text(before)
start('en_US')
walk('1280x800-final-chooser-hub',(R/'tools/vm-walks/to-manage-cloud-storage.steps').read_text())
walk('1280x800-final-chooser-options','key down\nwait-for-change\nkey x\nwait-for-change 30 0\nwait 10\nsettle\nshot options')
