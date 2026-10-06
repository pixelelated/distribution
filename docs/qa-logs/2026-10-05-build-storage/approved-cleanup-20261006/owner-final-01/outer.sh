#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-approved-cleanup-final-01/run.sh
result=$?
printf "%s\n" "$result" > /tmp/pixelelated-approved-cleanup-final-01/outer.rc
exit "$result"
