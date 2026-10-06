#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-boot-qualification-07/run.sh "${1:?bundle}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-boot-qualification-07/outer.rc
exit "$result"
