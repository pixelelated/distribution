#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-link-09/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-link-09/outer.rc
exit "$result"
