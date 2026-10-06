#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-approved-cleanup-05-v2/run.sh
result=$?
printf "%s\n" "$result" > /tmp/pixelelated-approved-cleanup-05-v2/outer.rc
exit "$result"
