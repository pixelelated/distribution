#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-16/build.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-replacement-16/outer.rc
exit "$result"
