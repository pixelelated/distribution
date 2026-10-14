set -e
export TMPDIR=/tmp/pix-steam-full
set +e
python3 -I -S -B /tmp/pix-input/steam/docs/qa-logs/2026-10-14-steam-client-alias-source/fixture.py --disposable-vm --case existing-internal-alias --output /tmp/pix-steam-full/alias01 > /tmp/pix-output/steam-alias.stdout 2> /tmp/pix-output/steam-alias.stderr
rc=$?
printf '%s\n' "$rc" > /tmp/pix-output/steam-alias.rc
if [ -f /tmp/pix-steam-full/alias01/result.json ]; then cp /tmp/pix-steam-full/alias01/result.json /tmp/pix-output/steam-alias-result.json; cat /tmp/pix-output/steam-alias-result.json; fi
if [ -f /tmp/pix-steam-full/alias01/caller-observation.json ]; then cat /tmp/pix-steam-full/alias01/caller-observation.json; fi
tar -czf /tmp/pix-output/steam-alias.tar.gz -C /tmp/pix-steam-full alias01
cat /tmp/pix-output/steam-alias.stderr
exit "$rc"
