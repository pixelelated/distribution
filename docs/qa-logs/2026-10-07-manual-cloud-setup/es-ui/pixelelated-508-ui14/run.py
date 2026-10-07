import sys
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
remote("mkdir -p /storage/qa-manual-ui/provider/pixelelated/Content/ROMs/gb; printf 'synthetic library marker, never launched\\n' > /storage/qa-manual-ui/provider/pixelelated/Content/ROMs/gb/QA.gb; sync")
(A/'chooser-payload-before.log').write_text(remote('find /storage/qa-manual-ui/provider -type f -exec sha256sum {} \\; | sort'))
walk('1280x800-final-chooser-decline','key right\nwait-for-change\nkey x\nwait-for-change 30 0\nwait 8\nsettle\nshot after-not-now')
proof=remote('sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; grep -E "^(SAVES|SETTINGS|CONTENT)_REMOTE=" /storage/.config/cloud_sync.conf')
assert proof.splitlines()[:2]==(A/'chooser-before.log').read_text().splitlines()[:2],proof
(A/'chooser-decline-unchanged.log').write_text(proof)
print('PASS NOT NOW preserves selected paths and credentials',flush=True)
