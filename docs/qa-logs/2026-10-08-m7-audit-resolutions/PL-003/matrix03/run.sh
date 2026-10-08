#!/bin/bash
set -uo pipefail
python3 -u /workspace/tmp/pixelelated-524-path-refusal/matrix03/run.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/matrix03/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/matrix03/outer.rc
exit "$rc"
