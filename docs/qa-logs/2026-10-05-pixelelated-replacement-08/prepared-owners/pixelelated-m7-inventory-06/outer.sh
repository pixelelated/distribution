#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-inventory-06/run.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-inventory-06/outer.rc
exit "$result"
