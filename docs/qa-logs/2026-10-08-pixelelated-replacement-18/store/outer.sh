#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-store-18/run.sh "$@"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-store-18/outer.rc
exit "$result"
