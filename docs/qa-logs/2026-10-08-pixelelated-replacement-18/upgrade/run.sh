#!/bin/bash
set -euo pipefail
cd /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18
TASK_OWNER=/workspace/tmp/pixelelated-m7-upgrade-18
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"' EXIT
export VM_PAIR_DIR=/workspace/tmp/pixelelated-m7-upgrade-18/pair
export CLOUD_QA_STATE=/workspace/tmp/pixelelated-m7-upgrade-18/cloud
export ROCKNIX_ARTIFACTS=/workspace/tmp/pixelelated-m7-upgrade-18/artifacts
export CLOUD_QA_BACKEND=webdav
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
TASK_BUNDLE=$(realpath "${1:?immutable bundle required}")
mkdir -p "$ROCKNIX_ARTIFACTS"
python3 -I /workspace/tmp/pixelelated-m7-image-18/verify-inputs.py "$TASK_BUNDLE"
python3 -I /workspace/tmp/pixelelated-m7-qa-21/preflight.py
bash /workspace/tmp/pixelelated-m7-upgrade-18/rehearsal.sh /workspace/artifacts/pixelelated-candidates/sha256/7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.tar" 7f58b7b1c592908dcd0ba5987955e59aaa79fe66
tools/cloud-test-backend down
python3 -I /workspace/tmp/pixelelated-m7-image-18/verify-inputs.py "$TASK_BUNDLE"

