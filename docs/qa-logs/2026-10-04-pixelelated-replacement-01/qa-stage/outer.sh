#!/bin/bash
set -uo pipefail
/workspace/tmp/pixelelated-m7-qa-02/qualify.sh "${1:?immutable bundle required}"
result=$?
printf '%s\n' "$result" > /workspace/tmp/pixelelated-m7-qa-02/outer.rc
exit "$result"
