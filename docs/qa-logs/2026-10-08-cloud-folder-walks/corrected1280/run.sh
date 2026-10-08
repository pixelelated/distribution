#!/bin/bash
set -euo pipefail
cd /workspace/repos/rocknix.worktrees/m7-p5-cloud-folder-walks
TASK_OWNER=/workspace/tmp/pixelelated-m7-walk527-04
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
test "$(git rev-parse HEAD)" = 2e484871bd80aae668ee1a22b25978a30d12f29c
test -z "$(git status --porcelain)"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"' EXIT
python3 -I "$TASK_OWNER/resize.py"
export VM_PAIR_DIR=/workspace/tmp/pixelelated-m7-walk527-03 CLOUD_QA_STATE=/workspace/tmp/pixelelated-m7-walk527-03/cloud ROCKNIX_ARTIFACTS="$TASK_OWNER/artifacts"
export CLOUD_QA_BACKEND=webdav CLOUD_QA_PORT=19087 CLOUD_QA_DEAD_PORT=19088
export PATH="/workspace/tmp/pixelelated-m7-walk527-03/bin:$PATH"
export QA_SYSTEM_ROOT=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64/image/system
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
set +e
tools/vm-qa --skip-up --guest d --only walks --walk to-change-cloud-folder --walk confirm-cloud-folder /workspace/artifacts/pixelelated-candidates/sha256/f557176651026f59bb5931993b12491a6019c0383321fb89fa1a05a596514fe6/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz
TASK_RC=$?
set -e
printf '%s\n' "$TASK_RC" > "$TASK_OWNER/walks.rc"
# Leave the predecessor-owned guest for immediate branch/frame readback.
# The outer result is the walk result, not an assertion that teardown ran.
exit "$TASK_RC"
