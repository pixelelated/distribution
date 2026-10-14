set -eu
mkdir /tmp/pix-extra
for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXEXTRA01 && break; sleep 1; done
mount -t ext4 -o ro,noload /dev/disk/by-label/PIXEXTRA01 /tmp/pix-extra
