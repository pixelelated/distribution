#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-qa-21/run.sh "$@"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-qa-21/outer.rc
exit "$result"
