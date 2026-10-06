#!/bin/bash
set -euo pipefail
TASK_OWNER=/tmp/pixelelated-cleanup-runtime-02
TASK_TREE=/workspace/repos/rocknix.worktrees/conflict-resolution
cd "$TASK_OWNER"
sha256sum -c harness.sha256
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"; exit "$result"' EXIT
nice -n 10 ionice -c 3 python3 -I "$TASK_OWNER/preserve.py"
for n in 03 05 06 07 08; do
  nice -n 10 ionice -c 3 python3 -I "$TASK_OWNER/source-inventory.py" \
    "/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement$n" \
    "/workspace/tmp/pixelelated-m7-replacement-$n/inputs.json" \
    "$TASK_OWNER/source-inventory-$n.json"
done
