#!/bin/bash
set -euo pipefail
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15
TASK_OWNER=/workspace/tmp/pixelelated-m7-p4-no-join-negative-02
cd "$TASK_TREE"
export VM_PAIR_DIR="$TASK_OWNER/pair" VM_GL=none
export CLOUD_QA_STATE="$TASK_OWNER/cloud" CLOUD_QA_BACKEND=webdav
export CLOUD_QA_PORT=9040 CLOUD_QA_NAME=pixelelated-m7-p4-no-join-negative-01
export ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
test ! -e "$TASK_OWNER/qa.start"
printf '%s\n' "$TASK_TREE/${RASTERATOPS_BUILD_RUN:?watch-build required}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
cleanup() {
  result=$?
  trap - EXIT
  printf '%s\n' "$result" > "$TASK_OWNER/inner.rc"
  exit "$result"
}
trap cleanup EXIT
sha256sum -c "$TASK_OWNER/harness.sha256"
python3 -I "$TASK_OWNER/run.py"
sha256sum -c "$TASK_OWNER/harness.sha256"
