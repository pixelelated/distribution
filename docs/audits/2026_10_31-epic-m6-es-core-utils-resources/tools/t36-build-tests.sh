#!/bin/bash
# T36 (#683): the slice's host tests (T35's t36-build-tests shape, trimmed to this slice).
# Two binaries:
#   es-unit-tests        -- the existing target, which links the slice's StringUtil.cpp,
#                           TimeText.cpp and OfflineProxyUrl.cpp (sources parsed from
#                           es-app/tests/unit/CMakeLists.txt, never typed); its TOTAL is real.
#   utils-resources-tests -- this slice's floor cases, with FileSystemUtil.cpp, StringUtil.cpp
#                           and md5.cpp linked whole and the parse-only seams lifted by
#                           t36-extract.py into <build>/x (a refused extract is not built).
# Each binary is run and its own [doctest] summary kept; the TOTAL is the tools' lines, never
# a hand sum. Writes only under <build dir>. rc 0 when every binary built and passed; 1 on a
# build/run failure; 2 when it cannot start.
set -uo pipefail
ES=${1:?es tree}; B=${2:?build dir}
CM="${ES}/es-app/tests/unit/CMakeLists.txt"
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -r "${CM}" ] || { echo "t36-build-tests: ${CM} unreadable" >&2; exit 2; }
# rapidjson is not needed by utils-resources-tests; a note only.
[ -r "${RAPIDJSON_INCLUDE_DIR:-/nonexistent}/rapidjson/document.h" ] && echo "rapidjson: present (unused here)" || echo "rapidjson: absent (unused here)"
command -v g++ >/dev/null || { echo "t36-build-tests: no g++" >&2; exit 2; }
mkdir -p "${B}"
echo "g++: $(g++ --version | head -1)"
echo "rapidjson: ${RAPIDJSON_INCLUDE_DIR} (document.h $(sha256sum < "${RAPIDJSON_INCLUDE_DIR}/rapidjson/document.h" | cut -c1-16))"
CXX=(g++ -std=c++17 -O0 -g0 -pthread)
FAIL=0
build() { # <name> <flags...> -- <sources...>
  local name=$1; shift; local flags=(); while [ "$1" != -- ]; do flags+=("$1"); shift; done; shift
  rm -f -- "${B:?}/${name:?}" "${B:?}/${name:?}.run.log"
  echo "\$ ${CXX[*]} ${flags[*]} <$# sources> -o ${name}"
  if ! "${CXX[@]}" "${flags[@]}" "$@" -o "${B}/${name}" > "${B}/${name}.build.log" 2>&1; then
    echo "BUILD FAIL ${name}:"; tail -n 20 "${B}/${name}.build.log"; FAIL=1; return 1
  fi
  echo "built ${name}"
}
# es-unit-tests is NOT built here: rapidjson 1.1.0 fails to compile under this host's
# g++ 15 (-Wtemplate-body on GenericStringRef::operator=). The slice's three files it
# links (StringUtil.cpp, TimeText.cpp, OfflineProxyUrl.cpp) are proven by T34's and
# T35's es-unit-tests runs (185 cases, their records). utils-resources-tests needs no
# rapidjson. The rapidjson gate below is kept for when a working copy is supplied.

# utils-resources-tests: the floor cases, over the lifted seams and the linked-whole sources.
X="${B}/x"; rm -rf -- "${B:?}/x"
python3 -B -I "${HERE}/t36-extract.py" "${ES}" "$(git -C "${ES}" rev-parse HEAD)" "${X}" \
  || { echo "t36-build-tests: the extracts were refused; utils-resources-tests not built"; FAIL=1; }
UR=""
if [ -d "${X}" ]; then
  UR=utils-resources-tests
  build utils-resources-tests "-DT36_X=\"${X}\"" -I "${X}" -I "${ES}/es-core/src" -I "${ES}/external" -- \
    "${HERE}/t36-utils-resources-tests.cpp" \
    "${ES}/es-core/src/utils/FileSystemUtil.cpp" \
    "${ES}/es-core/src/utils/StringUtil.cpp" \
    "${ES}/es-core/src/utils/md5.cpp"
fi
for t in ${UR}; do
  [ -x "${B}/${t}" ] || { echo "RUN ${t}: not built"; FAIL=1; continue; }
  "${B}/${t}" > "${B}/${t}.run.log" 2>&1; rc=$?
  echo "RUN ${t}: rc ${rc}; $(grep -E '^\[doctest\] (test cases|assertions):' "${B}/${t}.run.log" | tr -s ' ' | tr '\n' ' ')"
  if [ "${rc}" -ne 0 ]; then
    FAIL=1
    awk '/^TEST CASE:/{tc=$0} /ERROR|FAILED|CHECK\(/{if(tc){print "    "tc; tc=""}}' "${B}/${t}.run.log" | head -n 40
    grep -E 'ERROR|CHECK' "${B}/${t}.run.log" | head -n 30 | sed 's/^/      /'
  fi
done
TOTAL=0; BINS=0
for t in ${UR}; do
  [ -r "${B}/${t}.run.log" ] || continue
  n=$(grep -m1 -E '^\[doctest\] test cases:' "${B}/${t}.run.log" | grep -o -E '[0-9]+' | head -n 1)
  [ -n "${n}" ] && { TOTAL=$((TOTAL + n)); BINS=$((BINS + 1)); }
done
echo "TOTAL: ${TOTAL} test cases in ${BINS} binaries"
exit "${FAIL}"
