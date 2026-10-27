#!/bin/bash
# T21 (#668) stage E: g++ -fsyntax-only over EmulationStation sources the host
# cannot build, with the stand-in curl and SDL headers in stage-e/fakes/,
# pugixml at the submodule's commit and the recipe's rapidjson, and the
# build's own HAVE_INTL (CMakeLists.txt:575). It checks the file's own C++;
# it proves nothing about curl or SDL. One line per file: rc and the first
# error.
#   PUGIXML_INCLUDE_DIR=<dir> RAPIDJSON_INCLUDE_DIR=<dir> bash syntax-check.sh <es tree> <file...>
set -uo pipefail
ES=${1:?es tree}; shift
F=$(cd "$(dirname "$0")" && pwd)/fakes
fail=0
for f in "$@"; do
  out=$(g++ -std=c++17 -fsyntax-only -DHAVE_INTL -I "$F" -I "$ES/es-app/src" -I "$ES/es-core/src" -I "$ES/external" \
    -I "${PUGIXML_INCLUDE_DIR:?}" -I "${RAPIDJSON_INCLUDE_DIR:?}" "$ES/$f" 2>&1); rc=$?
  echo "$f: rc $rc$( [ $rc -ne 0 ] && printf '; %s' "$(printf '%s\n' "$out" | grep -m1 -E 'error' | sed -E 's#^/[^ ]*/##')")"
  [ $rc -eq 0 ] || fail=1
done
exit $fail
