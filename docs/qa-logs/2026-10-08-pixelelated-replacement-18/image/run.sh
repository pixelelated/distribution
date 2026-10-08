#!/bin/bash
set -euo pipefail
cd /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18
TASK_OWNER=/workspace/tmp/pixelelated-m7-image-18
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"' EXIT
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
TASK_BUNDLE=$(realpath "${1:?immutable bundle required}")
mkdir -p /workspace/tmp/pixelelated-m7-image-18/artifacts
python3 -I /workspace/tmp/pixelelated-m7-image-18/verify-inputs.py "$TASK_BUNDLE"
python3 -I /workspace/tmp/pixelelated-m7-image-18/extract.py "$TASK_BUNDLE"
tools/rasteratops-candidate-store verify "$TASK_BUNDLE"

