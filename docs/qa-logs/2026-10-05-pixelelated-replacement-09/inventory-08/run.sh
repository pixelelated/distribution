#!/bin/bash
set -euo pipefail
TASK_COORDINATION=/workspace/repos/rocknix.worktrees/conflict-resolution
[ "$(pwd -P)" = "$TASK_COORDINATION" ] || { echo "Refusing inventory: use its separate coordination worktree" >&2; exit 2; }
TASK_OWNER=/workspace/tmp/pixelelated-m7-inventory-08
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09
TASK_INPUTS=/workspace/tmp/pixelelated-m7-replacement-09/inputs.json
test ! -e "$TASK_OWNER/start"
test "$(cat /workspace/tmp/pixelelated-m7-replacement-09/outer.rc)" = 0
sha256sum -c "$TASK_OWNER/harness.sha256"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/start"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?}" > "$TASK_OWNER/run.path"
finish() { result=$?; trap - EXIT; printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"; exit "$result"; }
trap finish EXIT
python3 "$TASK_OWNER/source-inventory.py" "$TASK_TREE" "$TASK_INPUTS" "$TASK_OWNER/artifacts/source-inventory.json"
python3 "$TASK_OWNER/qualify-inventory.py"
python3 "$TASK_OWNER/component-map.py" --tree "$TASK_TREE" --inputs "$TASK_INPUTS" --inventory "$TASK_OWNER/artifacts/source-inventory-qualified.json" --output "$TASK_OWNER/artifacts/components.json"
