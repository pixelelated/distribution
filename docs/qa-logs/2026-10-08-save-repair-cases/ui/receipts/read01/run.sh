#!/bin/bash
set -uo pipefail
python3 /workspace/tmp/pixelelated-520-ui-20261008/read01/run.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-520-ui-20261008/read01/inner.rc
exit "$rc"
