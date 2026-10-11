from ui import *
import shutil
assert (P/'ready.json').exists()
art=P/'artifacts'
# Use the actual installed archive writer and uploader on this disposable VM.
print('START installed writer and cloud backup',flush=True)
log=guest('. /etc/profile >/dev/null 2>&1; backuptool backup && cloud_backup --yes --system-only',180)
(art/'settings-backup.log').write_text(log+'\n')
base=P/'cloud/data/pixelelated/Backups'
files=list(base.rglob('*_SETTINGS.tar.gz'));assert len(files)==1,[str(x) for x in files]
written=files[0];orig=written.read_bytes();label=guest('/usr/bin/cloud_device_id --label')
assert label in written.name
same=written.with_name('2026_10_11-190000-'+label+'-pixelelated_SETTINGS.tar.gz');same.write_bytes(orig)
foreign=written.with_name('2026_10_12-190000-Foreign-QA-ROCKNIX_SETTINGS.tar.gz');foreign.write_bytes(orig)
def inventory():return {str(x.relative_to(base)):hashlib.sha256(x.read_bytes()).hexdigest() for x in base.rglob('*') if x.is_file()}
(art/'same-model-inventory.json').write_text(json.dumps(inventory(),indent=2)+'\n')
restart();walk('en-offered-restore',HUB+'key down\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot options\n')
facts=guest('cat /storage/.cache/cloud_sync/scan/settings');assert 'MINE='+same.name in facts,facts
(art/'same-model-scan.txt').write_text(facts+'\n')
result=guest('. /etc/profile >/dev/null 2>&1; cloud_restore --yes --system-only',180)
(art/'same-model-restore.log').write_text(result+'\n')
(art/'same-model-journal.txt').write_text(guest('tail -100 /var/log/cloud_sync.log')+'\n')
download=guest('sha256sum /storage/roms/backup/'+same.name).split()[0];assert download==hashlib.sha256(orig).hexdigest()
(art/'selected-archive.json').write_text(json.dumps({'selected':same.name,'sha256':download,'label':label},indent=2)+'\n')
# Retain only a newer foreign-labelled archive in the same writer-owned directory.
written.unlink();same.unlink()
(art/'foreign-only-inventory.json').write_text(json.dumps(inventory(),indent=2)+'\n')
restart()
cmd='sha256sum /storage/.config/system.cfg /storage/.config/cloud_sync.conf /storage/.config/rclone/active-connection /storage/.config/rclone/rclone.conf'
before=guest(cmd)
walk('en-foreign-restore',HUB+'key down\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot options\n')
facts=guest('cat /storage/.cache/cloud_sync/scan/settings');assert 'MINE=\n' in facts and foreign.name in facts,facts
assert guest(cmd)==before
(art/'foreign-only-scan.txt').write_text(facts+'\n')
(art/'foreign-preserved.txt').write_text(before+'\n')
print('PASS archive selection/download/hash and foreign-only scan preservation; frames require review',flush=True)
