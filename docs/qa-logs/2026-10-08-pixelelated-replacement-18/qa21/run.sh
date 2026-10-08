#!/bin/bash
set -euo pipefail
cd /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18
TASK_OWNER=/workspace/tmp/pixelelated-m7-qa-21
test ! -e "$TASK_OWNER/qa.start"
sha256sum -c "$TASK_OWNER/harness.sha256"
printf '%s\n' "$PWD/${RASTERATOPS_BUILD_RUN:?use watch-build}" > "$TASK_OWNER/run.path"
date -u +%Y-%m-%dT%H:%M:%SZ > "$TASK_OWNER/qa.start"
trap 'result=$?; printf "%s\n" "$result" > "$TASK_OWNER/inner.rc"' EXIT
export VM_PAIR_DIR=/workspace/tmp/pixelelated-m7-qa-21/pair
export CLOUD_QA_STATE=/workspace/tmp/pixelelated-m7-qa-21/cloud
export ROCKNIX_ARTIFACTS=/workspace/tmp/pixelelated-m7-qa-21/artifacts
export CLOUD_QA_BACKEND=webdav
export ES_SRC=/home/max/Development/emulationstation-next.worktrees/qa-integration
export RETROARCH_SRC=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement18/build.pixelelated-GENERIC_X64.x86_64
export QA_SYSTEM_ROOT="$RETROARCH_SRC/image/system"
export WALK_BASELINE=/workspace/artifacts/rocknix-images/walk-baseline
TASK_BUNDLE=$(realpath "${1:?immutable bundle required}")
mkdir -p "$ROCKNIX_ARTIFACTS"
python3 -I /workspace/tmp/pixelelated-m7-image-18/verify-inputs.py "$TASK_BUNDLE"
python3 -I /workspace/tmp/pixelelated-m7-qa-21/preflight.py
tools/vm-pair up "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz"
python3 -I /workspace/tmp/pixelelated-m7-qa-21/check-payload.py clean
set +e
tools/vm-qa --skip-up "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz"
TASK_QA_RC=$?
set -e
printf '%s\n' "$TASK_QA_RC" > /workspace/tmp/pixelelated-m7-qa-21/default-suite.rc
python3 -I /workspace/tmp/pixelelated-m7-qa-21/check-payload.py after-defaults
# No device or offsite provider is involved in any case.
for TASK_BACKEND in sftp s3; do
 set +e
 tools/vm-qa --skip-up --only round-trip --backend "$TASK_BACKEND" "$TASK_BUNDLE/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz"
 TASK_PROTOCOL_RC=$?
 set -e
 printf '%s\n' "$TASK_PROTOCOL_RC" > /workspace/tmp/pixelelated-m7-qa-21/"$TASK_BACKEND".rc
 [ "$TASK_PROTOCOL_RC" = 0 ] || TASK_QA_RC=1
done
tools/vm-pair down
for TASK_BACKEND in webdav sftp s3; do tools/cloud-test-backend --backend "$TASK_BACKEND" down; done
python3 -I /workspace/tmp/pixelelated-m7-image-18/verify-inputs.py "$TASK_BUNDLE"
exit "$TASK_QA_RC"

