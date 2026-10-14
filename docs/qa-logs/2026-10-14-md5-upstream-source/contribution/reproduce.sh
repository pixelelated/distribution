#!/bin/bash
# SPDX-License-Identifier: MIT
# PREPARED, UNRUN: fresh x86_64 Linux output, explicit compiler, no network.
set -euo pipefail
if [ "$#" -ne 2 ]; then
    echo 'usage: reproduce.sh NEW_ABSOLUTE_OUTPUT ABSOLUTE_GCC_OR_CLANG' >&2
    exit 2
fi
case "$(uname -s):$(uname -m)" in Linux:x86_64) ;; *) exit 2 ;; esac
case "$1:$2" in /*:/*) ;; *) exit 2 ;; esac
BUNDLE=$(cd -- "$(dirname -- "$0")" && pwd -P)
OUT=$1
COMPILER=$2
[ -x "$COMPILER" ]
(cd -- "$BUNDLE" && sha256sum --check SHA256SUMS)
# mkdir refuses every existing owner; no reuse, replacement, or cleanup.
mkdir -m 700 -- "$OUT"
ulimit -c 0
ulimit -f 8192
python3 -I -S -B - "$BUNDLE" "$OUT" <<'PY'
import hashlib, json, sys
from pathlib import Path
bundle, out = map(Path, sys.argv[1:])
assert out.resolve() == out
source = json.loads((bundle/'source.json').read_text())
for name, digest in source['source_files'].items():
    assert hashlib.sha256((bundle/'upstream'/name).read_bytes()).hexdigest() == digest
original = (bundle/'upstream/utils/md5.c').read_bytes()
for name in ('before.c','after.c'):
    with (out/name).open('xb') as stream: stream.write(original)
PY
run() {
    local label=$1 seconds=$2 code
    shift 2
    set +e
    timeout --signal=TERM --kill-after=5s "${seconds}s" "$@" >"$OUT/$label.stdout" 2>"$OUT/$label.stderr"
    code=$?
    set -e
    printf '%s\n' "$code" >"$OUT/$label.rc"
}
run patch 10 patch --batch --forward "$OUT/after.c" "$BUNDLE/md5-alignment.patch"
[ "$(cat "$OUT/patch.rc")" = 0 ]
python3 -I -S -B - "$BUNDLE" "$OUT" <<'PY'
import hashlib, json, sys
from pathlib import Path
bundle, out = map(Path, sys.argv[1:])
assert hashlib.sha256((out/'after.c').read_bytes()).hexdigest() == json.loads((bundle/'source.json').read_text())['patched_md5_sha256']
PY
for mode in before after; do
    run "$mode-build" 60 "$COMPILER" -std=c99 -O1 -g -fstrict-aliasing \
        -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer \
        -DMD5_u32plus=uint32_t -I"$BUNDLE/upstream/include" \
        "$BUNDLE/md5-alignment.c" "$OUT/$mode.c" -o "$OUT/$mode"
    [ "$(cat "$OUT/$mode-build.rc")" = 0 ]
done
for mode in before after; do
    run "$mode" 15 env ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 \
        UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 "$OUT/$mode"
done
python3 -I -S -B "$BUNDLE/compare-digests.py" "$OUT"
# Keep every binary/log/original exit for the caller; no automatic deletion.
