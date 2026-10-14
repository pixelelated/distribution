set -e
umount /tmp/pix-input
mount -t ext4 -o ro,noload /dev/disk/by-label/PIXDOLPHIN04 /tmp/pix-input
SYSTEMD_PAGER=cat systemctl start essway.service
