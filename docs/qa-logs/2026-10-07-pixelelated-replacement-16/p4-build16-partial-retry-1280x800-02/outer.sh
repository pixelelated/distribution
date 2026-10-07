#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-p4-build16-partial-retry-1280x800-02/run.sh "${1:?bundle required}"
result=$?
printf "%s\n" "$result" > /workspace/tmp/pixelelated-m7-p4-build16-partial-retry-1280x800-02/outer.rc
exit "$result"
