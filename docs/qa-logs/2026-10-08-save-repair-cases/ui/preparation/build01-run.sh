#!/bin/bash
set -uo pipefail
export TMPDIR=/workspace/tmp
python3 -u /workspace/tmp/pixelelated-520-ui-20261008/build01/build.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/build01/inner.rc
exit "$rc"
