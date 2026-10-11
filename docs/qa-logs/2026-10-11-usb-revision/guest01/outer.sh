#!/bin/bash
set -uo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-usb-531-01
bash "$TASK_OWNER/run.sh"
rc=$?
printf '%s\n' "$rc" > "$TASK_OWNER/outer.rc"
exit "$rc"
