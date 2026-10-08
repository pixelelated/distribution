#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-walk527-03/run.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-walk527-03/outer.rc
exit "$result"
