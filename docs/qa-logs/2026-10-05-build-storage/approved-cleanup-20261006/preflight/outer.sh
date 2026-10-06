#!/bin/bash
set -uo pipefail
bash /tmp/pixelelated-cleanup-preflight-01/run.sh
result=$?
printf '%s\n' "$result" > /tmp/pixelelated-cleanup-preflight-01/outer.rc
exit "$result"
