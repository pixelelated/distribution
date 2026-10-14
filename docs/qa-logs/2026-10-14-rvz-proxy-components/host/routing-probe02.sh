set -eu
mkdir /tmp/pix-route02
for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXROUTE02 && break; sleep 1; done
mount -t ext4 -o ro,noload /dev/disk/by-label/PIXROUTE02 /tmp/pix-route02
set -eu
mkdir /tmp/pix-output/routing02
cd /tmp/pix-route02/2026-10-14-dolphin-proxy-routing-census-source
sha256sum -c SHA256SUMS > /tmp/pix-output/routing02/source-hashes.log
unshare -m --propagation private /bin/sh -s <<'PIXROUTE'
set -eu
mount -t tmpfs -o size=64m,nosuid,nodev,mode=755 tmpfs /run
set +e
timeout --signal=TERM --kill-after=5s 75s /usr/bin/python3 -I -S -B fixtures/probe.py --output /run/pix584-route02 > /tmp/pix-output/routing02/stdout 2> /tmp/pix-output/routing02/stderr
pxrc=$?
printf '%s\n' "$pxrc" > /tmp/pix-output/routing02/original.rc
if test -d /run/pix584-route02; then
 /usr/bin/python3 -I -S -B -c 'from pathlib import Path;import shutil;s=Path("/run/pix584-route02");d=Path("/tmp/pix-output/routing02/receipts");d.mkdir();[(shutil.copytree(p,d/p.name) if p.is_dir() else shutil.copy2(p,d/p.name)) for p in s.iterdir() if p.name!="root"]' || exit 125
fi
cat /tmp/pix-output/routing02/stdout
cat /tmp/pix-output/routing02/stderr
exit "$pxrc"
PIXROUTE
