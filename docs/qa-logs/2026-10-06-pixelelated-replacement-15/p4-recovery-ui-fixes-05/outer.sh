#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-recovery-ui-fixes-05/run.sh "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-p4-recovery-ui-fixes-05/outer.rc
exit "$result"
