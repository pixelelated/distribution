#!/bin/bash
set -uo pipefail
export TMPDIR=/workspace/tmp
python3 -u "/workspace/tmp/pixelelated-510-coverage02/guest01/create.py"
rc=$?
printf "%s\n" "$rc" > "/workspace/tmp/pixelelated-510-coverage02/guest01/inner.rc"
exit "$rc"
