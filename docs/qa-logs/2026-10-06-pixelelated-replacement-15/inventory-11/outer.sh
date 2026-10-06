#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-inventory-11/run.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-inventory-11/outer.rc
exit "$result"
