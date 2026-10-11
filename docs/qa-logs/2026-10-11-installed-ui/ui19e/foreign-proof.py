from ui import *
art=P/'artifacts'
cmd='sha256sum /storage/.config/system/configs/system.cfg /storage/.config/cloud_sync.conf /storage/.config/rclone/active-connection /storage/.config/rclone/rclone.conf'
before=guest(cmd)
walk('en-foreign-restore',HUB+'key down\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot options\n')
facts=guest('cat /storage/.cache/cloud_sync/scan/settings');assert 'MINE=\n' in facts and 'Foreign-QA' in facts,facts
assert guest(cmd)==before
(art/'foreign-only-scan.txt').write_text(facts+'\n')
(art/'foreign-preserved.txt').write_text(before+'\n')
print('PASS foreign-only archive UI scan preserves settings/configuration',flush=True)
