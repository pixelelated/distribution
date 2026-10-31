#!/bin/bash
# T34 (#681): the brief's stand-in syntax check (§ 5 item 1; T21's
# stage-e/syntax-check.sh:12-16 shape) over the 37 component sources of
# classes (c), (c+) and (e): g++ -fsyntax-only with T31's 13 fakes and the
# lane's tenth (stage-a/fakes/SDL_power.h), the pin's pugixml root and the
# recipe's rapidjson. VideoVlcComponent.cpp, class (d), needs <vlc/vlc.h> and
# <vlc/libvlc_version.h>, which no fake supplies: CANNOT, named. It checks a
# file's own C++ and proves nothing about SDL, VLC or curl. rc per file;
# exit 0 when every one of the 37 is rc 0, 1 otherwise, 2 when it cannot start.
#   PUGIXML_INCLUDE_DIR=<dir> RAPIDJSON_INCLUDE_DIR=<dir> stage-a/syntax-check.sh <es tree> <paths file>
set -uo pipefail
ES=${1:?es tree}; PF=${2:?paths file}
F="$(cd "$(dirname "$0")/../stage-a/fakes" && pwd)" || exit 2
[ -r "${PUGIXML_INCLUDE_DIR:?}/pugixml/src/pugixml.hpp" ] || { echo "t34-syntax-check: no pugixml under ${PUGIXML_INCLUDE_DIR}" >&2; exit 2; }
[ -r "${RAPIDJSON_INCLUDE_DIR:?}/rapidjson/document.h" ] || { echo "t34-syntax-check: no rapidjson under ${RAPIDJSON_INCLUDE_DIR}" >&2; exit 2; }
echo "g++: $(g++ --version | head -1); fakes: $(find "$F" -type f | wc -l) files"
n=0; bad=0
for p in $(grep -E '\.cpp$' "${PF}"); do
  case "$p" in *VideoVlcComponent.cpp) echo "CANNOT ${p#es-core/src/components/}: <vlc/vlc.h> and <vlc/libvlc_version.h> (:8-9) have no fake"; continue;; esac
  n=$((n + 1))
  out=$(g++ -std=c++17 -fsyntax-only -DHAVE_INTL -I "$F" -I "$ES/es-app/src" -I "$ES/es-core/src" -I "$ES/external" -I "${PUGIXML_INCLUDE_DIR}" -I "${RAPIDJSON_INCLUDE_DIR}" "$ES/$p" 2>&1)
  rc=$?
  echo "rc=${rc} ${p#es-core/src/components/}"
  [ "$rc" -eq 0 ] || { bad=$((bad + 1)); printf '%s\n' "$out" | grep -m3 -E 'error' | sed 's/^/    /'; }
done
echo "t34-syntax-check: ${n} file(s) checked, $((n - bad)) rc 0, ${bad} not"
[ "$n" -eq 37 ] || { echo "t34-syntax-check: expected 37 files, checked ${n}"; exit 1; }
[ "$bad" -eq 0 ]
