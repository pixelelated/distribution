set -eu
mkdir -p /storage/qa521/extract
cd /storage/qa521/extract
timeout 60 /usr/bin/duckstation-sa --appimage-extract > /storage/qa521/extract.log 2>&1
ls -l squashfs-root/AppRun squashfs-root/AppRun.wrapped squashfs-root/usr/bin/*
printf '\nBUNDLED_LIBRARY_PATHS\n'
find squashfs-root -name '*.so*' -type f | sort
printf '\nDIRECT_APPLICATION_CLOSURE\n'
LD_LIBRARY_PATH=/storage/qa521/extract/squashfs-root/usr/lib /usr/bin/ldd /storage/qa521/extract/squashfs-root/usr/bin/duckstation-qt
