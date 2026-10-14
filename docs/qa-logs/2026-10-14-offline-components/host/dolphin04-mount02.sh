set -e
for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXDOLPHIN04 && break; sleep 1; done
test -e /dev/disk/by-label/PIXDOLPHIN04
mount -t ext4 -o ro,noload /dev/disk/by-label/PIXDOLPHIN04 /tmp/pix-input
SYSTEMD_PAGER=cat systemctl start essway.service
