#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-cf10-18/melonds-installed01/run.sh "$@"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-cf10-18/melonds-installed01/outer.rc
exit "$result"
