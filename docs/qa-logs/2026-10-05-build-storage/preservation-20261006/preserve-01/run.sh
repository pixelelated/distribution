#!/bin/bash
set -euo pipefail
TASK_OWNER=/tmp/pixelelated-cleanup-preserve-01
TASK_TREE=/workspace/repos/rocknix.worktrees/conflict-resolution
cd "$TASK_OWNER"
sha256sum -c harness.sha256
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"; exit "$result"' EXIT
nice -n 10 ionice -c 3 python3 -I "$TASK_OWNER/preserve.py"
