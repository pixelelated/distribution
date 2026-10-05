#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-replacement-07/build-attempt-02/build.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-replacement-07/build-attempt-02/outer.rc
exit "$result"
