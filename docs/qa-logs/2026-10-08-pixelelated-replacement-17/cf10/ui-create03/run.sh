#!/bin/bash
set -euo pipefail
cd /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement17
TASK_OWNER=/workspace/tmp/pixelelated-m7-cf10-17/ui-create03
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"' EXIT
python3 -I -u "$TASK_OWNER/run.py"
