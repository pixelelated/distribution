#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-sweep-08/run.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-sweep-08/outer.rc
exit "$result"
