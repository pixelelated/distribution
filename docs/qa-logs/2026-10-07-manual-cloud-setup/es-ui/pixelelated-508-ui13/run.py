import sys
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
walk('1280x800-final-chooser-offer','key up\nwait-for-change\nkey right\nwait-for-change\nkey x\nwait-for-change\nwait 3\nsettle\nshot offered')
proof=remote('sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; grep -E "^(SAVES|SETTINGS|CONTENT)_REMOTE=" /storage/.config/cloud_sync.conf')
assert proof.splitlines()[:2]==(A/'chooser-before.log').read_text().splitlines()[:2],proof
(A/'chooser-offer-unchanged.log').write_text(proof)
