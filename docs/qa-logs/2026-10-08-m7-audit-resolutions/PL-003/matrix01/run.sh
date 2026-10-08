#!/bin/bash
set -uo pipefail
python3 -u /workspace/tmp/pixelelated-524-path-refusal/matrix01/run.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/matrix01/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/matrix01/outer.rc
exit "$rc"
