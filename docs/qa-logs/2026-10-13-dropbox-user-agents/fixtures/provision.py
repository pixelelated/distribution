from pathlib import Path
import subprocess,json,time,hashlib
r=Path(__file__).parent;old=Path('/workspace/tmp/pix570-handoff-20261013');ssh=json.loads((old/'ssh-command.json').read_text())
def run(c,**kw):return subprocess.run(ssh+[c],check=True,timeout=30,**kw)
run('/usr/bin/cloud_oauth cancel',capture_output=True)
run('umount /usr/bin/rclone; mkdir -p /storage/qa570ua; cp /usr/bin/cloud-signin-window /storage/qa570ua/installed-browser',capture_output=True)
with (r/'cloud-signin-window').open('rb') as f:run('cat > /storage/qa570ua/cloud-signin-window',stdin=f)
run('chmod 755 /storage/qa570ua/cloud-signin-window; mount --bind /storage/qa570ua/cloud-signin-window /usr/bin/cloud-signin-window; sha256sum /usr/bin/rclone /usr/bin/cloud-signin-window /storage/qa570ua/installed-browser',stdout=(r/'installed.txt').open('w'))
# Start real account-free authorization. GUI will use its normal launch/wait handoff;
# its old synthetic QR is setup-only, not proof of the new session PIN.
run("systemd-run --unit=qa570ua-broker --property=RuntimeMaxSec=900 /usr/bin/cloud_oauth serve dropbox --name qa570ua --timeout 850",capture_output=True)
time.sleep(4)
run("python3 - <<'P'\nimport os,subprocess,json\nfrom pathlib import Path\np=next(x for x in Path('/run').glob('**/wayland-*') if x.is_socket());e=dict(os.environ,XDG_RUNTIME_DIR=str(p.parent),WAYLAND_DISPLAY=p.name);s=next(p.parent.glob('sway-ipc*'));e['SWAYSOCK']=str(s);subprocess.run(['swaymsg','[app_id=\"emulationstation\"] focus'],env=e,check=True);subprocess.run(['grim','/storage/qa570ua/setup.png'],env=e,check=True)\nP",capture_output=True)
with (r/'setup.png').open('wb') as f:run('cat /storage/qa570ua/setup.png',stdout=f)
(r/'ssh-command.json').write_text(json.dumps(ssh))
print('PROVISIONED')
