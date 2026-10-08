#!/bin/bash
set -uo pipefail
python3 -u /workspace/tmp/pixelelated-524-path-refusal/guest01/create.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/guest01/inner.rc
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-524-path-refusal/guest01/outer.rc
exit "$rc"
