#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-build16-recovery-1280x800-01/run.sh "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-p4-build16-recovery-1280x800-01/outer.rc
exit "$result"
