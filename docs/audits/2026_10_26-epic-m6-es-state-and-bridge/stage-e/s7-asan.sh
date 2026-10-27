#!/bin/bash
# T21 (#668) S7: build s7-asan.cpp against an ES tree's HttpText.cpp and run
# its cases, one per process. Prints each case's rc and the sanitizer's
# summary line (paths cut to the file name).
#   bash s7-asan.sh <es tree> <scratch> <case...>
set -uo pipefail
ES=${1:?es tree}; S=${2:?scratch}; shift 2
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$S"
g++ -std=c++17 -O0 -g -fsanitize=address,undefined -fno-omit-frame-pointer -I "$ES/es-core/src" \
  "$D/s7-asan.cpp" "$ES/es-core/src/HttpText.cpp" "$ES/es-core/src/utils/StringUtil.cpp" -o "$S/s7-asan" > "$S/build.log" 2>&1 \
  || { echo "BUILD FAIL"; tail -n 15 "$S/build.log"; exit 2; }
echo "== s7-asan built from $(git -C "$ES" rev-parse --short=10 HEAD)$(git -C "$ES" diff --quiet HEAD -- es-core || echo ' + the working tree')"
for c in "$@"; do
  echo "-- $c"
  ASAN_OPTIONS=detect_leaks=1 "$S/s7-asan" "$c" > "$S/$c.log" 2>&1; rc=$?
  echo "rc $rc"
  grep -E '^(header parsed|status read|headers sent)' "$S/$c.log"
  grep -E 'ERROR: AddressSanitizer|SUMMARY: (AddressSanitizer|UndefinedBehaviorSanitizer)|runtime error' "$S/$c.log" | sed -E 's#/[^ :]*/##g; s/0x[0-9a-f]+/0x.../g' | head -n 3
done
