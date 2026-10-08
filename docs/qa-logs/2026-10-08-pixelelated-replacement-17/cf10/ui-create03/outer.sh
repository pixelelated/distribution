#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-cf10-17/ui-create03/run.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-cf10-17/ui-create03/outer.rc
exit "$result"
