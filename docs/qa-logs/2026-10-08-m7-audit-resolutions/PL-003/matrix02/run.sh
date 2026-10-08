#!/bin/bash
set -uo pipefail
python3 -u /workspace/tmp/pixelelated-524-path-refusal/matrix02/run.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/matrix02/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/matrix02/outer.rc
exit "$rc"
