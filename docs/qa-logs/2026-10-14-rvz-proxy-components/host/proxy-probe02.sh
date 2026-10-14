set -eu
mkdir /tmp/pix-output/proxy-revision02
cd /tmp/pix-input/packets/2026-10-14-proxy-rvz-source
sha256sum -c SHA256SUMS > /tmp/pix-output/proxy-revision02/source-hashes.log
cd /tmp/pix-extra/packets/2026-10-14-proxy-rvz-fixture-correction
sha256sum -c SHA256SUMS > /tmp/pix-output/proxy-revision02/revision-hashes.log
unshare -m --propagation private /bin/sh -s <<'PIXPROBE'
set -eu
mount -t tmpfs -o size=32m,nosuid,nodev,mode=755 tmpfs /run
set +e
timeout --signal=TERM --kill-after=5s 45s /usr/bin/python3 -I -S -B fixtures/probe.py --output /run/pix583-revision02 > /tmp/pix-output/proxy-revision02/stdout 2> /tmp/pix-output/proxy-revision02/stderr
pxrc=$?
printf '%s\n' "$pxrc" > /tmp/pix-output/proxy-revision02/original.rc
if test -f /run/pix583-revision02/result.json; then
 cp /run/pix583-revision02/result.json /tmp/pix-output/proxy-revision02/result.json || exit 125
fi
cat /tmp/pix-output/proxy-revision02/stdout
cat /tmp/pix-output/proxy-revision02/stderr
exit "$pxrc"
PIXPROBE
