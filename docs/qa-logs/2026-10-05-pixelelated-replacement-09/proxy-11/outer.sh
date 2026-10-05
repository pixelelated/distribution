#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-proxy-11/run.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-proxy-11/outer.rc
exit "$result"
