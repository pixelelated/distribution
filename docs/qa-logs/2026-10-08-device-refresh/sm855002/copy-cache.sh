#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-sm8550-refresh-02
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-sm8550-02
[ "$(pwd -P)" = "$TASK_TREE" ]
[ "$(id -u)" = 1000 ]
[ ! -e "$TASK_OWNER/copy.start" ]
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/copy.run"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/copy.start"
trap 'rc=$?; printf "%s\n" "$rc" > "$TASK_OWNER/copy.rc"; printf "%s\n" "$rc" > "$TASK_OWNER/copy.outer.rc"' EXIT
python3 -I "$TASK_OWNER/verify-source.py"
python3 -I "$TASK_OWNER/copy-cache.py"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/copy.finish"
