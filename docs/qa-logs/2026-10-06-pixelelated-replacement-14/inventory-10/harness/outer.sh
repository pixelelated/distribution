#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-inventory-10/run.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-inventory-10/outer.rc
exit "$result"
