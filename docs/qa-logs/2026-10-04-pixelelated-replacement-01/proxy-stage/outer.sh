#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-proxy-01/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-proxy-01/outer.rc
exit "$result"
