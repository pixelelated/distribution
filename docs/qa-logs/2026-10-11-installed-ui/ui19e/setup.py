from ui import *
assert (P/'ready.json').exists()
guest('systemctl stop essway')
conf=subprocess.check_output([str(ROOT/'tools/cloud-test-backend'),'rclone-conf'],env=ENV,text=True)
code="from pathlib import Path\np=Path('/storage/.config/rclone/rclone.conf');p.write_text("+repr(conf)+");p.chmod(0o600)\np=Path('/storage/.config/rclone/active-connection');p.write_text('qa-cloud\\n');p.chmod(0o600)\n"
python(code)
guest(". /etc/profile >/dev/null 2>&1; cloud_setup --set-saves-remote /pixelelated/Saves; cloud_setup --set-settings-remote /pixelelated/Backups; cloud_setup --set-content-remote /pixelelated/Content; mkdir -p /storage/roms/nes; printf 'QA UI PLACEHOLDER NOT A GAME' > /storage/roms/nes/QA-ui.nes")
for folder in ['Saves','Backups','Content/ROMs','Content/BIOS','Content/Media']:(P/'cloud/data/pixelelated'/folder).mkdir(parents=True,exist_ok=True)
mode=restart()
(P/'artifacts/initial-identity.json').write_text(json.dumps({'mode':mode,'image':guest("sed -n 's/^BUILD_ID=//p' /etc/os-release"),'es_sha256':guest('sha256sum /usr/bin/emulationstation').split()[0]},indent=2)+'\n')
walk('en-empty-restore',HUB+'key down\nwait-for-change\nkey x\nwait-for-change\nsettle\nshot options\n')
print('PASS initial setup and empty restore walk; visual review pending',flush=True)
