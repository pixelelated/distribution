#!/bin/bash
set -euo pipefail
TASK_OWNER=/workspace/tmp/pixelelated-m7-boot-qualification-06
cd /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
python3 "$TASK_OWNER/verify-inputs.py" "$1"
./tools/rasteratops-candidate-store verify "$1"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?watch-build required}" > "$TASK_OWNER/run.path"
date -u +%FT%TZ > "$TASK_OWNER/qa.start"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"; exit "$result"' EXIT
python3 "$TASK_OWNER/qualify-boot.py" "$1"
python3 "$TASK_OWNER/verify-inputs.py" "$1"
./tools/rasteratops-candidate-store verify "$1"
sha256sum -c "$TASK_OWNER/harness.sha256"
