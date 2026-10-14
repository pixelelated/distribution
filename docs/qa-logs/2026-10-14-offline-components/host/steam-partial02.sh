set -e
export TMPDIR=/tmp/pix-steam-small
set +e
python3 -I -S -B /tmp/pix-extra/steam/docs/qa-logs/2026-10-14-steam-client-crc-source/fixture.py --disposable-vm --case partial-extraction-retry --output /tmp/pix-steam-small/partial02 > /tmp/pix-output/steam-partial02.stdout 2> /tmp/pix-output/steam-partial02.stderr
rc=$?
printf '%s\n' "$rc" > /tmp/pix-output/steam-partial02.rc
if [ -f /tmp/pix-steam-small/partial02/result.json ]; then cp /tmp/pix-steam-small/partial02/result.json /tmp/pix-output/steam-partial02-result.json; cat /tmp/pix-output/steam-partial02-result.json; fi
if [ -f /tmp/pix-steam-small/partial02/qa/client-observation.json ]; then cat /tmp/pix-steam-small/partial02/qa/client-observation.json; fi
tar -czf /tmp/pix-output/steam-partial02.tar.gz -C /tmp/pix-steam-small partial02
cat /tmp/pix-output/steam-partial02.stderr
exit "$rc"
