#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-p3-20261006/host-b09-01/run.sh
TASK_RESULT=$?
printf '%s\n' "$TASK_RESULT" > /tmp/pixelelated-p3-20261006/host-b09-01/outer.rc
exit "$TASK_RESULT"
