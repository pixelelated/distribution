#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-approved-cleanup-08-v3/run.sh
result=$?
printf "%s\n" "$result" > /tmp/pixelelated-approved-cleanup-08-v3/outer.rc
exit "$result"
