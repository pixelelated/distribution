#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-qa-14/qualify.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-qa-14/outer.rc
exit "$result"
