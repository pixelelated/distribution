#!/bin/bash
# Record the qualification wrapper result inside the watched command boundary.
set -u
/workspace/tmp/pixelelated-m7-qa-01/qualify.sh /workspace/artifacts/pixelelated-candidates/sha256/22533e35b95a122ebd0d7dc2b60f6e816982594af62454f5209a04be8da3512d
TASK_RESULT=$?
printf '%s\n' "$TASK_RESULT" > /workspace/tmp/pixelelated-m7-qa-01/outer.rc
exit "$TASK_RESULT"
