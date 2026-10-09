#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-readiness-control-01
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'rc=$?; printf "%s\n" "$rc" > "$TASK_OWNER/inner.rc"' EXIT
ssh -i /workspace/tmp/pixelelated-m7-readiness-01/qa-key -p 10291 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes root@127.0.0.1 'python3 -' < "$TASK_OWNER/guest.py"
scp -q -r -i /workspace/tmp/pixelelated-m7-readiness-01/qa-key -P 10291 -o LogLevel=ERROR -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.1:/tmp/pix529-baseline "$TASK_OWNER/evidence"
