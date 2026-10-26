#!/bin/bash
# T18 (#665): EmulationStation's unit tests, built with the host's g++ by
# commands generated from es-app/tests/unit/CMakeLists.txt, because the host
# has no cmake (the brief's section 5, version 2). Then each binary is run and
# its own summary line kept.
#
#   RAPIDJSON_INCLUDE_DIR=<dir holding rapidjson/> \
#     bash docs/audits/2026_10_26-epic-m6-es-cloud-pages/tools/t18-build-tests.sh <es tree> <build dir>
#
# The four binaries and their sources are read from CMakeLists.txt's
# add_executable() / add_library() lists, with ${CMAKE_CURRENT_SOURCE_DIR}
# and ${ES_ROOT} expanded, so a source added there is built here; nothing is
# typed. The include roots are the file's own: es-app/src, es-core/src,
# external (doctest), rapidjson for es-unit-tests, fakes/ before es-core for
# es-conf-tests. -std=c++17 as CXX_STANDARD 17; -pthread for Threads::Threads;
# ES_ROOT_DIR for es-file-tests; _WIN32 for the one object of
# es-file-tests-win32. A missing rapidjson stops here, as the CMakeLists'
# FATAL_ERROR does: a binary that silently tests less is the failure it
# forbids. Writes only under <build dir>. Exit 0 when every binary built and
# passed; 1 when a build or a run failed; 2 when it could not start.
set -uo pipefail
ES=${1:?es tree}; B=${2:?build dir}
CM="${ES}/es-app/tests/unit/CMakeLists.txt"
[ -r "${CM}" ] || { echo "t18-build-tests: ${CM} unreadable" >&2; exit 2; }
[ -n "${RAPIDJSON_INCLUDE_DIR:-}" ] && [ -r "${RAPIDJSON_INCLUDE_DIR}/rapidjson/document.h" ] \
  || { echo "t18-build-tests: rapidjson/document.h not under RAPIDJSON_INCLUDE_DIR='${RAPIDJSON_INCLUDE_DIR:-}'; nothing built" >&2; exit 2; }
command -v g++ >/dev/null || { echo "t18-build-tests: no g++" >&2; exit 2; }
mkdir -p "${B}"
# target -> its source list, from CMakeLists.txt itself.
python3 -I - "${CM}" "${ES}" > "${B}/sources.txt" <<'PY' || exit 2
import re, sys
cm, es = sys.argv[1], sys.argv[2]
text = re.sub(r"#[^\n]*", "", open(cm).read())
unit = cm.rsplit("/", 1)[0]
for kind, name, body in re.findall(r"add_(executable|library)\(\s*([A-Za-z0-9_-]+)\s+(?:OBJECT\s+)?([^)]*)\)", text):
    for s in body.split():
        s = s.replace("${CMAKE_CURRENT_SOURCE_DIR}", unit).replace("${ES_ROOT}", es)
        print(name, s)
PY
echo "g++: $(g++ --version | head -1)"
echo "rapidjson: ${RAPIDJSON_INCLUDE_DIR} (document.h $(sha256sum < "${RAPIDJSON_INCLUDE_DIR}/rapidjson/document.h" | cut -c1-16))"
srcs() { awk -v t="$1" '$1 == t && $2 !~ /^\$</ {print $2}' "${B}/sources.txt"; }
CXX=(g++ -std=c++17 -O0 -g0 -pthread)
UNIT="${ES}/es-app/tests/unit"
FAIL=0
build() { # <name> <flags...> -- <sources...>
  local name=$1; shift; local flags=() ; while [ "$1" != -- ]; do flags+=("$1"); shift; done; shift
  echo "\$ ${CXX[*]} ${flags[*]} <$# sources> -o ${name}"
  printf '    %s\n' "$@"
  if ! "${CXX[@]}" "${flags[@]}" "$@" -o "${B}/${name}" > "${B}/${name}.build.log" 2>&1; then
    echo "BUILD FAIL ${name}:"; tail -n 15 "${B}/${name}.build.log"; FAIL=1; return 1
  fi
  echo "built ${name}"
}
mapfile -t S1 < <(srcs es-unit-tests)
build es-unit-tests -I "${ES}/es-app/src" -I "${ES}/es-core/src" -I "${ES}/external" -I "${RAPIDJSON_INCLUDE_DIR}" -- "${S1[@]}"
mapfile -t S2 < <(srcs es-file-tests)
build es-file-tests -I "${ES}/es-core/src" -I "${ES}/external" "-DES_ROOT_DIR=\"${ES}\"" -- "${S2[@]}"
mapfile -t S3 < <(srcs es-conf-tests)
build es-conf-tests -I "${UNIT}/fakes" -I "${ES}/es-core/src" -I "${ES}/external" -- "${S3[@]}"
mapfile -t S4o < <(srcs atomicfile-win32-branch)
mapfile -t S4 < <(srcs es-file-tests-win32)
echo "\$ ${CXX[*]} -D_WIN32 -c ${S4o[*]} -o atomicfile-win32-branch.o"
if "${CXX[@]}" -D_WIN32 -I "${ES}/es-core/src" -c "${S4o[@]}" -o "${B}/atomicfile-win32-branch.o" > "${B}/win32obj.build.log" 2>&1; then
  build es-file-tests-win32 -I "${ES}/es-core/src" -I "${ES}/external" -- "${S4[@]}" "${B}/atomicfile-win32-branch.o"
else
  echo "BUILD FAIL atomicfile-win32-branch:"; tail -n 15 "${B}/win32obj.build.log"; FAIL=1
fi
for t in es-unit-tests es-file-tests es-conf-tests es-file-tests-win32; do
  [ -x "${B}/${t}" ] || { echo "RUN ${t}: not built"; FAIL=1; continue; }
  "${B}/${t}" > "${B}/${t}.run.log" 2>&1; rc=$?
  echo "RUN ${t}: rc ${rc}; $(grep -E '^\[doctest\] (test cases|assertions):' "${B}/${t}.run.log" | tr -s ' ' | tr '\n' ' ')"
  [ "${rc}" -eq 0 ] || { FAIL=1; grep -E 'ERROR|FAILED' "${B}/${t}.run.log" | head -n 10; }
done
exit "${FAIL}"
