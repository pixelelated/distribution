#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-fresh-root-06/run.sh "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-p4-fresh-root-06/outer.rc
exit "$result"
