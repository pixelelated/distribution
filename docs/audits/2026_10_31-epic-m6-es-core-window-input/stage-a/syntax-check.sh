#!/bin/bash
# T35 (#682): the brief's stand-in syntax check (§ 5 item 1; T21's
# stage-e/syntax-check.sh:12-16 shape, T34's stage-a/syntax-check.sh copied by
# git show from feature/m6-es-core-components-681 at 3e285d86b3 and adapted)
# over the 44 `.cpp` of the 96: g++ -fsyntax-only with T34's 14 fakes (T31's 13
# and T34's SDL_power.h) copied under stage-a/fakes/, plus any fake the first
# errors forced (each named in the record), the pin's pugixml root and
# rapidjson. The udev (HAVE_UDEV), pulse (_ENABLE_PULSE_), TTS (_ENABLE_TTS_),
# CEC (HAVE_LIBCEC) and WIN32 branches are not defined, so not parsed. It checks
# a file's own C++ and proves nothing about SDL, ALSA or curl. rc per file;
# exit 0 when every one of the 44 is rc 0, 1 otherwise, 2 when it cannot start.
#   PUGIXML_INCLUDE_DIR=<dir> RAPIDJSON_INCLUDE_DIR=<dir> stage-a/syntax-check.sh <es tree> <paths file>
set -uo pipefail
ES=${1:?es tree}; PF=${2:?paths file}
F="$(cd "$(dirname "$0")/fakes" && pwd)" || exit 2
[ -r "${PUGIXML_INCLUDE_DIR:?}/pugixml/src/pugixml.hpp" ] || { echo "t35-syntax-check: no pugixml under ${PUGIXML_INCLUDE_DIR}" >&2; exit 2; }
[ -r "${RAPIDJSON_INCLUDE_DIR:?}/rapidjson/document.h" ] || { echo "t35-syntax-check: no rapidjson under ${RAPIDJSON_INCLUDE_DIR}" >&2; exit 2; }
echo "g++: $(g++ --version | head -1); fakes: $(find "$F" -type f | wc -l) files"
n=0; bad=0
for p in $(grep -E '\.cpp$' "${PF}"); do
  n=$((n + 1))
  out=$(g++ -std=c++17 -fsyntax-only -DHAVE_INTL -DROCKNIX -I "$F" -I "$ES/es-app/src" -I "$ES/es-core/src" -I "$ES/external" -I "${PUGIXML_INCLUDE_DIR}" -I "${RAPIDJSON_INCLUDE_DIR}" "$ES/$p" 2>&1)
  rc=$?
  echo "rc=${rc} ${p#es-core/src/}"
  [ "$rc" -eq 0 ] || { bad=$((bad + 1)); printf '%s\n' "$out" | grep -m3 -E 'error' | sed 's/^/    /'; }
done
echo "t35-syntax-check: ${n} file(s) checked, $((n - bad)) rc 0, ${bad} not"
[ "$n" -eq 44 ] || { echo "t35-syntax-check: expected 44 files, checked ${n}"; exit 1; }
[ "$bad" -eq 0 ]
