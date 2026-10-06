#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-fresh-root-07/run.sh "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-p4-fresh-root-07/outer.rc
exit "$result"
