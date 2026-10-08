#!/bin/bash
set -uo pipefail
ssh -i /workspace/tmp/pixelelated-520-ui-20261008/guest01/qa-key -p 10220 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1 'set -eu
mkdir -p /storage/qa521/extract
cd /storage/qa521/extract
timeout 60 /usr/bin/duckstation-sa --appimage-extract > /storage/qa521/extract.log 2>&1
ls -l squashfs-root/AppRun squashfs-root/AppRun.wrapped squashfs-root/usr/bin/*
printf '"'"'\nBUNDLED_LIBRARY_PATHS\n'"'"'
find squashfs-root -name '"'"'*.so*'"'"' -type f | sort
printf '"'"'\nDIRECT_APPLICATION_CLOSURE\n'"'"'
LD_LIBRARY_PATH=/storage/qa521/extract/squashfs-root/usr/lib /usr/bin/ldd /storage/qa521/extract/squashfs-root/usr/bin/duckstation-qt
' > /workspace/tmp/pixelelated-520-ui-20261008/duck-extract01/extract-readback.log 2>&1
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/duck-extract01/inner.rc
exit "$rc"
