#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-inventory-04/run.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-inventory-04/outer.rc
exit "$result"
