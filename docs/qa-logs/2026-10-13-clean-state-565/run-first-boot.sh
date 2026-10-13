#!/bin/sh
# Prepared coordinator-only experiment; not run in the source lane (#565).
set -eu
owner=${1:?fresh allocated owner directory}
serial=${2:?allocated guest serial socket}
test -d "$owner"
test -S "$serial"
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
cd "$repo"
test ! -e "$owner/first-boot.sh"
test ! -e "$owner/first-boot.serial"
tools/pixelelated-state-check-test --prepare-guest-script "$owner/first-boot.sh"
tools/vm-serial --socket "$serial" --timeout 180 script "$owner/first-boot.sh" > "$owner/first-boot.serial"
python3 - "$owner/first-boot.serial" <<'PY'
import json
from pathlib import Path
import sys
try:
    text = Path(sys.argv[1]).read_text()
    start = text.index('{\n')
    report, _ = json.JSONDecoder().raw_decode(text[start:])
    ok = (report.get('schema') == 1 and
          report.get('policy') == 'pixelelated-selected-state-v1' and
          report.get('mode') == 'first-boot' and report.get('status') == 'pass' and
          report.get('blocked_count') == 0 and report.get('error_count') == 0 and
          any(row.get('category') == 'boot-ready' and row.get('status') == 'clear'
              and row.get('present') is True for row in report.get('checks', [])) and
          text.count('PIX_STATE_565_RC=') == 1 and 'PIX_STATE_565_RC=0' in text)
except Exception:
    ok = False
print(json.dumps({'status': 'pass' if ok else 'error', 'category': 'first-boot-selected-state'}))
sys.exit(0 if ok else 2)
PY
