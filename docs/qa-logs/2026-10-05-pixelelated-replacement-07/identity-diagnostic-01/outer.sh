#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-identity-diagnostic-01/run.sh "${1:?bundle}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-identity-diagnostic-01/outer.rc
exit "$result"
