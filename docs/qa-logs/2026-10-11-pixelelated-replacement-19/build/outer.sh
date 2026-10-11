#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-build19/build.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-build19/outer.rc
exit "$result"
