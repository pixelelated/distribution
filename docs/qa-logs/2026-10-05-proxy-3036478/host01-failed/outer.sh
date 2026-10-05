#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-proxy-3036478/host01/run.sh
TASK_RESULT=$?
printf '%s\n' "$TASK_RESULT" > /tmp/pixelelated-proxy-3036478/host01/outer.rc
exit "$TASK_RESULT"
