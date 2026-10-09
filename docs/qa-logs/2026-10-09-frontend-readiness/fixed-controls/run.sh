#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-readiness-fixed-01
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'rc=$?; printf "%s\n" "$rc" > "$TASK_OWNER/inner.rc"' EXIT
opts=(-i /workspace/tmp/pixelelated-m7-readiness-01/qa-key -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes)
scp -q "${opts[@]}" -P 10291 "$TASK_OWNER/sway-ready" root@127.0.0.1:/tmp/pix529-sway-ready
scp -q "${opts[@]}" -P 10291 "$TASK_OWNER/essway.service" root@127.0.0.1:/run/systemd/system/essway.service
ssh "${opts[@]}" -p 10291 root@127.0.0.1 'chmod 755 /tmp/pix529-sway-ready; systemctl daemon-reload; sha256sum /tmp/pix529-sway-ready /run/systemd/system/essway.service'
set +e
ssh "${opts[@]}" -p 10291 root@127.0.0.1 'python3 -u -' < "$TASK_OWNER/guest.py"
rc=$?
scp -q -r "${opts[@]}" -P 10291 root@127.0.0.1:/tmp/pix529-fixed "$TASK_OWNER/evidence"
copyrc=$?
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
exit "$copyrc"
