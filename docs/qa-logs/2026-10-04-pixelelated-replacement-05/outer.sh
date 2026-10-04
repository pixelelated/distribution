#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-05/build.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-replacement-05/outer.rc
exit "$result"
