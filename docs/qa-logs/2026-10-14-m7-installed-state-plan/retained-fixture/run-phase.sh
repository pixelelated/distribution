#!/bin/bash
# Coordinator-only; run under a fresh watched owner, never directly on a device.
set -eu
repo=${1:?frozen checkout}
prepared=${2:?prepared script directory}
owner=${3:?fresh watched phase owner}
serial=${4:?owned disposable VM serial socket}
phase=${5:?seed before after or backup}
packet=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
case "$phase" in seed) ceiling=340;; before|after) ceiling=220;; backup) ceiling=460;; *) exit 2;; esac
test -S "$serial"
test -d "$owner"
test ! -e "$owner/$phase.serial"
test ! -e "$owner/$phase.transport.rc"
test ! -e "$owner/$phase.result.json"
python3 -I - "$prepared" "$phase" "$repo" <<'PY'
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]); phase=sys.argv[2]; repo=Path(sys.argv[3])
bind=json.loads((root/'bindings.json').read_text())
assert hashlib.sha256((root/(phase+'.sh')).read_bytes()).hexdigest()==bind['scripts'][phase+'.sh']
assert hashlib.sha256((repo/'tools/vm-serial').read_bytes()).hexdigest()==bind['vm_serial_sha256']
PY
set +e
timeout --signal=TERM --kill-after=10s "${ceiling}s" "$repo/tools/vm-serial" --socket "$serial" --timeout "$((ceiling - 10))" script "$prepared/$phase.sh" > "$owner/$phase.serial" 2> "$owner/$phase.transport.stderr"
transport=$?
set -e
printf '%s\n' "$transport" > "$owner/$phase.transport.rc"
python3 -I "$packet/collect.py" --phase "$phase" --serial "$owner/$phase.serial" --transport-rc "$owner/$phase.transport.rc" --output "$owner/$phase.result.json"
