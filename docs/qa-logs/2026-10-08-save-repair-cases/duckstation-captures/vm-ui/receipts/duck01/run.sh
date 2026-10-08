#!/bin/bash
set -uo pipefail
python3 /workspace/tmp/pixelelated-520-ui-20261008/duck01/run.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/duck01/inner.rc
exit "$rc"
