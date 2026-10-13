from ui import *
r=Path(__file__).parent
remote('/usr/bin/cloud_oauth cancel',capture_output=True)
remote('umount /usr/bin/cloud-signin-window; mkdir -p /storage/qa570bp',capture_output=True)
with (r/'cloud-signin-window').open('rb') as f:remote('cat > /storage/qa570bp/cloud-signin-window',stdin=f)
remote('chmod 755 /storage/qa570bp/cloud-signin-window; mount --bind /storage/qa570bp/cloud-signin-window /usr/bin/cloud-signin-window; sha256sum /usr/bin/rclone /usr/bin/cloud-signin-window',stdout=(r/'installed.txt').open('w'))
remote('systemd-run --unit=qa570bp-broker --property=RuntimeMaxSec=1050 /usr/bin/cloud_oauth serve dropbox --name qa570bp --timeout 1000',capture_output=True)
time.sleep(4);shot(r/'setup.png')
print('PROVISIONED')
