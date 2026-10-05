#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-10-build02/build.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-replacement-10-build02/outer.rc
exit "$result"
