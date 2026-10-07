#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-inventory-12/run.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-inventory-12/outer.rc
exit "$result"
