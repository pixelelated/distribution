#!/bin/bash
set -uo pipefail
python3 -I -u /workspace/tmp/pixelelated-m7-sweep-10/run.py "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-sweep-10/outer.rc
exit "$result"
