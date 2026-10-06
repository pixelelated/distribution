#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-cleanup-runtime-01/run.sh
result=$?
printf '%s\n' "$result" > /tmp/pixelelated-cleanup-runtime-01/outer.rc
exit "$result"
