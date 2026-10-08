#!/bin/bash
set -uo pipefail
python3 -u /workspace/tmp/pixelelated-510-coverage02/build03/finalize.py
rc=$?
printf "%s\n" "$rc" > /workspace/tmp/pixelelated-510-coverage02/build03/inner.rc
exit "$rc"
