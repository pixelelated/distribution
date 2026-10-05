#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-inventory-09/run.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-inventory-09/outer.rc
exit "$result"
