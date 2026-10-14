set -eu
mkdir /tmp/pix-md5-input /tmp/pix-output/md5-target01
for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXMD5 && break; sleep 1; done
mount -t ext4 -o ro,noload /dev/disk/by-label/PIXMD5 /tmp/pix-md5-input
unshare -m --propagation private /bin/sh -s <<'PIXMD5'
set -eu
mkdir /tmp/pix574-md5-01
mount -t tmpfs -o size=512m,nosuid,nodev,mode=700 tmpfs /tmp/pix574-md5-01
set +e
TMPDIR=/tmp/pix574-md5-01 timeout --signal=TERM --kill-after=5s 30s /usr/bin/python3 -I -S -B /tmp/pix-md5-input/recovery/controls.py --input /tmp/pix-md5-input > /tmp/pix-output/md5-target01/recovery-controls.stdout 2> /tmp/pix-output/md5-target01/recovery-controls.stderr
pxrc=$?
printf '%s\n' "$pxrc" > /tmp/pix-output/md5-target01/recovery-controls.rc
cat /tmp/pix-output/md5-target01/recovery-controls.stdout
cat /tmp/pix-output/md5-target01/recovery-controls.stderr
if test "$pxrc" != 0; then exit "$pxrc"; fi
timeout --signal=TERM --kill-after=5s 310s /usr/bin/python3 -I -S -B /tmp/pix-md5-input/recovery/run-guest.py --disposable-vm --input /tmp/pix-md5-input --scratch /tmp/pix574-md5-01 > /tmp/pix-output/md5-target01/stdout 2> /tmp/pix-output/md5-target01/stderr
pxrc=$?
printf '%s\n' "$pxrc" > /tmp/pix-output/md5-target01/original.rc
if test -d /tmp/pix574-md5-01/receipts; then cp -a /tmp/pix574-md5-01/receipts /tmp/pix-output/md5-target01/receipts || exit 125; fi
cat /tmp/pix-output/md5-target01/stdout
cat /tmp/pix-output/md5-target01/stderr
exit "$pxrc"
PIXMD5
