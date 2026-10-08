#!/bin/bash
set -uo pipefail
export PATH=/tmp/pixelelated-rc-rclone:$PATH
export CLOUD_QA_BACKEND=webdav
export CLOUD_QA_STATE=/workspace/tmp/pixelelated-validator-roundtrip-upkcf1ok/backend
export CLOUD_QA_PORT=19868
export CLOUD_QA_DEAD_PORT=19869
export CLOUD_QA_DEFAULTS=/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults
finish() {
  tools/cloud-test-backend --backend webdav down
}
trap finish EXIT
if ! tools/cloud-test-backend --backend webdav up; then exit 2; fi
tools/cloud-round-trip --host root@127.0.0.1 --port 10210 --identity /workspace/tmp/pixelelated-510-es-ui/guest02/qa-key --backend webdav --dump /workspace/tmp/pixelelated-validator-roundtrip-upkcf1ok/artifacts
qa_rc=$?
printf '%s\n' "$qa_rc" > /workspace/tmp/pixelelated-validator-roundtrip-upkcf1ok/inner.rc
exit "$qa_rc"
