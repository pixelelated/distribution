#!/usr/bin/env bash
# T39 (#686): each table of t39-tables.py seen to exit 0 on the export and 1 on a constructed drift, each drift on
# its own scratch copy of the export (never a checkout), before its table is trusted (brief § 6, the Tools row).
#   bash t39-tables-drift.sh <export> <repo> <commit> <probes> <allow> <issues> <scratch>
E=${1:?export}; R=${2:?repo}; C=${3:?commit}; P=${4:?probes}; A=${5:?allow}; I=${6:?issues}; S=${7:?scratch}
G=/usr/bin/grep
case "$S" in /workspace/tmp/m6-t39/*) ;; *) echo "refused: scratch must be under /workspace/tmp/m6-t39/"; exit 2 ;; esac
T=$(cd "$(dirname "$0")" && pwd)/t39-tables.py
rm -rf "${S:?}"
mkdir -p "$S"
mk() { cp -a "$E" "$S/$1"; }
check() {  # check <label> <want> <table> <export>
  local label=$1 want=$2 table=$3 ex=$4 rc
  python3 -I "$T" "$table" --export "$ex" --repo "$R" --commit "$C" --probes "$P" --allow "$A" --issues "$I" > /dev/null 2> "$S/last.err"
  rc=$?
  printf '%-40s rc=%s (want %s) %s\n' "$label" "$rc" "$want" "$($G -m1 '^FAIL' "$S/last.err" | cut -c1-120)"
}
check "coverage, the export" 0 coverage "$E"
mk cov; rm "$S/cov/docs/council-limits.md"
check "coverage, one document removed" 1 coverage "$S/cov"
check "binaries, the export" 0 binaries "$E"
mk bin; printf 'x' >> "$S/bin/docs/pixelelated/art/raster/2x/neon.png"
check "binaries, one byte on a PNG" 1 binaries "$S/bin"
check "art, the export" 0 art "$E"
mk art; printf ' ' >> "$S/art/docs/pixelelated/art/wordmark/neon.svg"
check "art, one byte on an SVG" 1 art "$S/art"
check "q4, the export" 0 q4 "$E"
mk q4; printf '\nAs decided in D-CLOUD-9999.\n' >> "$S/q4/docs/releases/versioning.md"
check "q4, a planted unresolved ID" 1 q4 "$S/q4"
check "q5, the export" 0 q5 "$E"
mk q5; rm "$S/q5/docs/savestate-compat-test.md"
check "q5, one reference document removed" 1 q5 "$S/q5"
check "q6, the export" 0 q6 "$E"
mk q6; sed -i '21d' "$S/q6/docs/pixelelated/art/README.md"
check "q6, a dead path's line moved" 1 q6 "$S/q6"
