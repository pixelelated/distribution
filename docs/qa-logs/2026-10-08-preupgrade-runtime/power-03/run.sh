#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-alignment-power-03
printf "%s\n" "$PWD/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'rc=$?; printf "%s\n" "$rc" > "$TASK_OWNER/inner.rc"' EXIT
sha256sum -c "$TASK_OWNER/harness.sha256"
python3 -I -u "$TASK_OWNER/run.py"
