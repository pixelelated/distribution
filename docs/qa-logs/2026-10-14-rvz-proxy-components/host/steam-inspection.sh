set -eu
mkdir /tmp/pix-output/steam-inspection01
cd /tmp/pix-input/packets/2026-10-14-steam-client-download-recovery-source
sha256sum -c SHA256SUMS > /tmp/pix-output/steam-inspection01/source-hashes.log
unshare -m --propagation private /bin/sh -s <<'PIXSTEAM'
set -eu
mkdir /run/pix582-verify01
mount -t tmpfs -o size=768m,noexec,nosuid,nodev,mode=700 tmpfs /run/pix582-verify01
cp -a /tmp/pix-input/steam/download01 /run/pix582-verify01/download01
cp -a /tmp/pix-input/steam/recovery01 /run/pix582-verify01/recovery01
cat > /run/pix582-verify01/admission.json <<'PIXJSON'
{"coordinator": "w4:p2", "packet_manifest_sha256": "0f885f19b56e12d334a3109e58ad345528cf0ba8c82f2bef28aee2cb09f742ef", "scratch_mount": "/run/pix582-verify01", "scratch_max_bytes": 805306368, "expires_utc": "2026-10-14T03:35:23.923990+00:00"}
PIXJSON
set +e
/usr/bin/python3 -I -S -B vm_verify.py --scratch-root /run/pix582-verify01 --output /run/pix582-verify01/rejected01 --archive /run/pix582-verify01/download01/archive.zip --admission /run/pix582-verify01/admission.json > /tmp/pix-output/steam-inspection01/rejected.stdout 2> /tmp/pix-output/steam-inspection01/rejected.stderr
pxrc=$?
printf '%s\n' "$pxrc" > /tmp/pix-output/steam-inspection01/rejected.rc
set -e
test "$pxrc" = 1
test ! -e /run/pix582-verify01/verify-attempt.json
/usr/bin/python3 -I -S -B -c 'import json;d=json.load(open("/tmp/pix-output/steam-inspection01/rejected.stdout"));assert d["status"]=="FAIL" and not d["children"] and "Need original successful revised-host receipt" in d["error"];print("Original failed acquisition alone correctly refused before decoder")'
set +e
/usr/bin/python3 -I -S -B vm_verify.py --scratch-root /run/pix582-verify01 --output /run/pix582-verify01/verify01 --archive /run/pix582-verify01/download01/archive.zip --recovery /run/pix582-verify01/recovery01/result.json --admission /run/pix582-verify01/admission.json > /tmp/pix-output/steam-inspection01/stdout 2> /tmp/pix-output/steam-inspection01/stderr
pxrc=$?
printf '%s\n' "$pxrc" > /tmp/pix-output/steam-inspection01/original.rc
if test -d /run/pix582-verify01/verify01; then cp -a /run/pix582-verify01/verify01 /tmp/pix-output/steam-inspection01/receipts || exit 125; fi
cp /run/pix582-verify01/admission.json /tmp/pix-output/steam-inspection01/admission.json || exit 125
cat /tmp/pix-output/steam-inspection01/stdout
cat /tmp/pix-output/steam-inspection01/stderr
exit "$pxrc"
PIXSTEAM
