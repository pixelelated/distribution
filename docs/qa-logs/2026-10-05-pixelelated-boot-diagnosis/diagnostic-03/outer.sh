#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-boot-diagnostic-03/run.sh "$1"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-boot-diagnostic-03/outer.rc
exit "$result"
