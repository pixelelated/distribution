#!/bin/bash
set -euo pipefail
O=/tmp/pixelelated-508-ui01
trap 'rc=$?; printf "%s\n" "$rc" > "$O/inner.rc"' EXIT
python3 "$O/control.py" stage
