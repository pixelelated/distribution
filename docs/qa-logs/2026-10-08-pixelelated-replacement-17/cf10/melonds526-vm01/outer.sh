#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-cf10-17/melonds526-vm01/run.sh
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-cf10-17/melonds526-vm01/outer.rc
exit "$result"
