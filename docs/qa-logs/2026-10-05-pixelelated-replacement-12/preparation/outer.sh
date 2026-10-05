#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-12/build.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-replacement-12/outer.rc
exit "$result"
