set -e
SYSTEMD_PAGER=cat systemctl stop essway.service
set +e
python3 -I -S -B /tmp/pix567-log-fixture01/run-fixture.py --disposable-guest --case failure --output /tmp/pix567-failure01 --expected-build 1a026648442321609b2288c2c9c06803817f9df2 --expected-es-sha256 8752b5391ea8728c1a088d0a80e3776469692dda665e8f07f062fed3206263d2 --es-source-commit bb9e2785f88c2b9de979022a2a9ded2cbce2f954 --xdg-runtime-dir /run/0-runtime-dir --wayland-display wayland-1 --language en_US --trigger api > /tmp/pix-output/index-failure01.stdout 2> /tmp/pix-output/index-failure01.stderr
rc=$?
printf '%s\n' "$rc" > /tmp/pix-output/index-failure01.rc
if [ -d /tmp/pix567-failure01 ]; then
 test ! -e /tmp/pix567-failure01/key.pem || exit 94
 tar -czf /tmp/pix-output/index-failure01.tar.gz -C /tmp pix567-failure01
 cat /tmp/pix567-failure01/result.json /tmp/pix567-failure01/worker-result.json /tmp/pix567-failure01/worker.stderr 2>/dev/null
fi
cat /tmp/pix-output/index-failure01.stderr
exit "$rc"
