#!/bin/bash
set -uo pipefail
export CLOUD_QA_STATE=/workspace/tmp/pixelelated-524-path-refusal/s3-state
export CLOUD_QA_NAME=pixelelated-524-path-refusal
export CLOUD_QA_PORT=9039
export CLOUD_QA_BUCKET=pixelelated-qa524
export CLOUD_QA_IMAGE=14cea493d9a3
/workspace/repos/rocknix/tools/cloud-test-backend --backend s3 up
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/s3-start01/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/s3-start01/outer.rc
exit "$rc"
