#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-cf10-17/ui-create02/run.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-cf10-17/ui-create02/outer.rc
exit "$result"
