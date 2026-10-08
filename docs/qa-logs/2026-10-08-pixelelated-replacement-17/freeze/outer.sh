#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-17/build.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-replacement-17/outer.rc
exit "$result"
