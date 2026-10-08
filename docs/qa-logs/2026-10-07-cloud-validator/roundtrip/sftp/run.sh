#!/bin/bash
set -uo pipefail
export PATH=/tmp/pixelelated-rc-rclone:$PATH
export CLOUD_QA_BACKEND=sftp
export CLOUD_QA_STATE=/workspace/tmp/pixelelated-validator-sftp-si7gx7nn/backend
export CLOUD_QA_PORT=19870
export CLOUD_QA_DEAD_PORT=19871
export CLOUD_QA_DEFAULTS=/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults
finish() {
  /workspace/repos/rocknix.worktrees/conflict-resolution/tools/cloud-test-backend --backend sftp down
}
trap finish EXIT
if ! /workspace/repos/rocknix.worktrees/conflict-resolution/tools/cloud-test-backend --backend sftp up; then exit 2; fi
/workspace/repos/rocknix.worktrees/conflict-resolution/tools/cloud-round-trip --host root@127.0.0.1 --port 10210 --identity /workspace/tmp/pixelelated-510-es-ui/guest02/qa-key --backend sftp --dump /workspace/tmp/pixelelated-validator-sftp-si7gx7nn/artifacts
qa_rc=$?
printf '%s\n' "$qa_rc" > /workspace/tmp/pixelelated-validator-sftp-si7gx7nn/inner.rc
exit "$qa_rc"
