#!/bin/bash
set -euo pipefail
cd /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18
TASK_OWNER=/workspace/tmp/pixelelated-m7-cf10-18/public-adoption01
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"' EXIT
python3 -I -u /workspace/tmp/pixelelated-m7-cf10-18/public-adoption01/run.py
