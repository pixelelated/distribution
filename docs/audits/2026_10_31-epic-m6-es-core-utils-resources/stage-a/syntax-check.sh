#!/bin/bash
# T36 (#683) S0: the stand-in syntax check (brief s5 item 1; T35's shape, T36's fakes + macro).
# g++ -fsyntax-only over the slice's .cpp with stage-a/fakes/ (T35's 15 + T36's 4: ft2build.h
# with FreeType records, GLES3/gl3.h, vlc/vlc.h, t36-sdl-gl.h), -DUSE_OPENGLES_30 (the macro
# the image's -DGLES3=1 sets), the pugixml root and rapidjson. Checks a file's own C++.
#   PUGIXML_INCLUDE_DIR=<dir> RAPIDJSON_INCLUDE_DIR=<dir> stage-a/syntax-check.sh <es tree> <paths file>
set -uo pipefail
ES=${1:?es tree}; PF=${2:?paths file}
F="$(cd "$(dirname "$0")/fakes" && pwd)" || exit 2
[ -r "${PUGIXML_INCLUDE_DIR:?}/pugixml/src/pugixml.hpp" ] || { echo "t36-syntax-check: no pugixml under ${PUGIXML_INCLUDE_DIR}" >&2; exit 2; }
[ -r "${RAPIDJSON_INCLUDE_DIR:?}/rapidjson/document.h" ] || { echo "t36-syntax-check: no rapidjson under ${RAPIDJSON_INCLUDE_DIR}" >&2; exit 2; }
echo "g++: $(g++ --version | head -1); fakes: $(find "$F" -type f | wc -l) files; -DUSE_OPENGLES_30"
n=0; bad=0
for p in $(grep -E '\.cpp$' "${PF}"); do
  n=$((n + 1))
  out=$(g++ -std=c++17 -fsyntax-only -DHAVE_INTL -DROCKNIX -DUSE_OPENGLES_30 -I "$F" -I "$ES/es-app/src" -I "$ES/es-core/src" -I "$ES/external" -I "${PUGIXML_INCLUDE_DIR}" -I "${RAPIDJSON_INCLUDE_DIR}" "$ES/$p" 2>&1)
  rc=$?
  echo "rc=${rc} ${p#es-core/src/}"
  [ "$rc" -eq 0 ] || { bad=$((bad + 1)); printf '%s\n' "$out" | grep -m3 -E 'error' | sed 's/^/    /'; }
done
echo "t36-syntax-check: ${n} file(s) checked, $((n - bad)) rc 0, ${bad} not"
[ "$n" -eq 25 ] || { echo "t36-syntax-check: expected 25 files, checked ${n}"; exit 1; }
[ "$bad" -eq 0 ]
