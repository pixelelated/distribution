#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-approved-cleanup-03/run.sh
result=$?
printf '%s\n' "$result" > /tmp/pixelelated-approved-cleanup-03/outer.rc
exit "$result"
