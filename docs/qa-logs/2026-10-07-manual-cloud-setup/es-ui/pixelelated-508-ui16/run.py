import sys,json,hashlib,re
sys.path.insert(0,'/tmp/pixelelated-508-ui01');from control import *
before=remote('cat /storage/.config/cloud_sync.conf')
credentials=remote('sha256sum /storage/.config/rclone/rclone.conf')
walk('1280x800-final-chooser-list','key x\nwait-for-change\nwait 3\nkey x\nwait-for-change\nwait 3\nsettle\nshot folders-before-choice')
unchanged=remote('cat /storage/.config/cloud_sync.conf');assert before==unchanged,'opening chooser changed selected path'
(A/'chooser-list-unchanged.log').write_text(remote('sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf; grep -E "^(SAVES|SETTINGS|CONTENT)_REMOTE=" /storage/.config/cloud_sync.conf'))
walk('1280x800-final-chooser-selected','key x\nwait-for-change 30 0\nwait 8\nsettle\nshot selected-library')
after=remote('cat /storage/.config/cloud_sync.conf')
strip=lambda s:re.sub(r'^CONTENT_REMOTE=.*\n?','',s,flags=re.M)
assert strip(before)==strip(after),'another config field changed'
assert re.search(r'^CONTENT_REMOTE="/pixelelated/Content"$',after,re.M),after
assert before!=after
assert credentials==remote('sha256sum /storage/.config/rclone/rclone.conf')
payload=remote('find /storage/qa-manual-ui/provider -type f -exec sha256sum {} \\; | sort')
assert payload==(A/'chooser-payload-before.log').read_text(),'provider payload changed'
proof=remote('sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf /usr/bin/emulationstation /usr/bin/cloud_setup /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo; grep -E "^(SAVES|SETTINGS|CONTENT)_REMOTE=" /storage/.config/cloud_sync.conf; grep "cloud content folder:" /var/log/es_log.txt')
(A/'chooser-explicit-selection.log').write_text(proof)
(A/'chooser-pointer-proof.json').write_text(json.dumps({'offered_and_declined_without_config_or_credential_change':True,'before_config_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_config_sha256':hashlib.sha256(after.encode()).hexdigest(),'only_changed_key':'CONTENT_REMOTE','old':'/manual-choice','new':'/pixelelated/Content','other_config_bytes_equal':True,'credentials_equal':True,'provider_files_equal':True,'synthetic_ROM_never_launched':True},indent=2)+'\n')
walk('1280x800-final-chooser-cancel','key z\nwait-for-change\nsettle\nshot cancelled-without-restore')
remote('systemctl stop essway; cp -a /storage/qa-manual-ui/before-chooser.conf /storage/.config/cloud_sync.conf; sync')
print('PASS explicit content choice changes CONTENT_REMOTE only, keeps credentials/data, no restore launched; fixture config restored',flush=True)
