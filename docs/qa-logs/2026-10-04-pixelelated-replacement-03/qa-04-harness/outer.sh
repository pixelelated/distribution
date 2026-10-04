#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-qa-04/qualify.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-qa-04/outer.rc
exit "$result"
