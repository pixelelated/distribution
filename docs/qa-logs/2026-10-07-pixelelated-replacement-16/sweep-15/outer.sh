#!/bin/bash
set -uo pipefail
python3 -I -u /workspace/tmp/pixelelated-m7-sweep-15/run.py "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-sweep-15/outer.rc
exit "$result"
