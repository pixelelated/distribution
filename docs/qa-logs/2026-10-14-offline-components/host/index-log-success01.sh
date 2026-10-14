set -e
for i in 1 2 3 4 5; do test -e /dev/disk/by-label/PIXINDEXLOG && break; sleep 1; done
mkdir /tmp/pix-indexlog
mount -t ext4 -o ro,noload /dev/disk/by-label/PIXINDEXLOG /tmp/pix-indexlog
python3 -I -S -B /tmp/pix-indexlog/docs/qa-logs/2026-10-14-library-index-log-correction/prepare-correction.py --sealed-fixture /tmp/pix-input/distribution/docs/qa-logs/2026-10-13-library-index-fixture --sealed-guard /tmp/pix-indexlog/docs/qa-logs/2026-10-14-library-index-fsize-correction --output /tmp/pix567-log-fixture01
set -e
SYSTEMD_PAGER=cat systemctl stop essway.service
set +e
python3 -I -S -B /tmp/pix567-log-fixture01/run-fixture.py --disposable-guest --case success --output /tmp/pix567-log-success01 --expected-build 1a026648442321609b2288c2c9c06803817f9df2 --expected-es-sha256 8752b5391ea8728c1a088d0a80e3776469692dda665e8f07f062fed3206263d2 --es-source-commit bb9e2785f88c2b9de979022a2a9ded2cbce2f954 --xdg-runtime-dir /run/0-runtime-dir --wayland-display wayland-1 --language en_US --trigger api > /tmp/pix-output/index-log-success01.stdout 2> /tmp/pix-output/index-log-success01.stderr
rc=$?
printf '%s\n' "$rc" > /tmp/pix-output/index-log-success01.rc
if [ -d /tmp/pix567-log-success01 ]; then
 test ! -e /tmp/pix567-log-success01/key.pem || exit 94
 tar -czf /tmp/pix-output/index-log-success01.tar.gz -C /tmp pix567-log-success01
 cat /tmp/pix567-log-success01/result.json /tmp/pix567-log-success01/worker-result.json /tmp/pix567-log-success01/worker.stderr 2>/dev/null
fi
cat /tmp/pix-output/index-log-success01.stderr
exit "$rc"
