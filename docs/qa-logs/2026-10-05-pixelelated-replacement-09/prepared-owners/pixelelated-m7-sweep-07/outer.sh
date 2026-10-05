#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-sweep-07/run.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-sweep-07/outer.rc
exit "$result"
