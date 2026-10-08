#!/bin/bash
set -uo pipefail
export TMPDIR=/workspace/tmp
python3 -u /workspace/tmp/pixelelated-524-path-refusal/build01/build.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/build01/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/build01/outer.rc
exit "$rc"
