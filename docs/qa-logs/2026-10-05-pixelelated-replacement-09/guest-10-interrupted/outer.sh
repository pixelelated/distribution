#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-guest-10/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-guest-10/outer.rc
exit "$result"
