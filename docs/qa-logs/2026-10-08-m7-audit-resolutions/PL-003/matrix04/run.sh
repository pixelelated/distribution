#!/bin/bash
set -uo pipefail
python3 -u /workspace/tmp/pixelelated-524-path-refusal/matrix04/run.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/matrix04/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/matrix04/outer.rc
exit "$rc"
