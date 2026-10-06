#!/bin/bash
set -uo pipefail
python3 -I -u /workspace/tmp/pixelelated-m7-sweep-11/run.py "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-sweep-11/outer.rc
exit "$result"
