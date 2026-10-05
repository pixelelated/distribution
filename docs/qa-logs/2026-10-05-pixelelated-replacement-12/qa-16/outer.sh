#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-qa-16/qualify.sh "${1:?bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-qa-16/outer.rc
exit "$result"
