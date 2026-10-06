#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-p3-20261006/scripts-b09-01/run.sh
TASK_RC=$?
printf '%s\n' "$TASK_RC" > /tmp/pixelelated-p3-20261006/scripts-b09-01/outer.rc
exit "$TASK_RC"
