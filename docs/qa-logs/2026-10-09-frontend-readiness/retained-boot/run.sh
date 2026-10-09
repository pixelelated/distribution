#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-readiness-boot-01
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'rc=$?; printf "%s\n" "$rc" > "$TASK_OWNER/inner.rc"' EXIT
python3 -I -u "$TASK_OWNER/run.py"
