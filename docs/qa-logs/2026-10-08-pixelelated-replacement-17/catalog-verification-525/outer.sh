#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement17-verification01/run.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-replacement17-verification01/outer.rc
exit "$result"
