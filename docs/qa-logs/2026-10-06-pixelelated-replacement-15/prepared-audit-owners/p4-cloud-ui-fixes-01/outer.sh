#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-cloud-ui-fixes-01/run.sh "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-p4-cloud-ui-fixes-01/outer.rc
exit "$result"
