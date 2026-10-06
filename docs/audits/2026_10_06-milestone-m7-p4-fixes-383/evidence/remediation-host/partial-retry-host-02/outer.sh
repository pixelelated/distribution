#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-partial-retry-host-02/run.sh
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-p4-partial-retry-host-02/outer.rc
exit "$result"
