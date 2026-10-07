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
