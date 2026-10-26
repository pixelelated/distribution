#!/bin/bash
# T18 (#665): tests/app-unit's jobs-tests -- the only test of the transfer
# job's stop races -- built with the host's g++ by commands generated from
# tests/app-unit/CMakeLists.txt, because the host has no cmake. Allowed by
# the coordinator on #665 at 10:02 UTC (F-19).
#
#   bash docs/audits/2026_10_26-epic-m6-es-cloud-pages/tools/t18-build-jobs-tests.sh <es tree> <build dir>
#
# Read from the CMakeLists itself: the file's compile and link options
# (AddressSanitizer and UBSan), its configure_file copies into under-test/
# (so a copied source's quoted includes find the doubles, as configure does),
# and jobs-tests' sources, with ${ES_ROOT}, ${CMAKE_CURRENT_SOURCE_DIR} and
# ${CMAKE_BINARY_DIR} expanded; the include roots are the target's own, the
# fakes BEFORE the rest. The copies are the test's, never an edit of the
# shipped file. Writes only under <build dir>. Exit 0 when it built and
# passed; 1 when the build or the run failed; 2 when it could not start.
set -uo pipefail
ES=${1:?es tree}; B=${2:?build dir}
CM="${ES}/tests/app-unit/CMakeLists.txt"
[ -r "${CM}" ] || { echo "t18-build-jobs-tests: ${CM} unreadable" >&2; exit 2; }
command -v g++ >/dev/null || { echo "t18-build-jobs-tests: no g++" >&2; exit 2; }
mkdir -p "${B}/under-test"
python3 -I - "${CM}" "${ES}" "${B}" > "${B}/plan.txt" <<'PY' || exit 2
import re, sys
cm, es, b = sys.argv[1:4]
unit = cm.rsplit("/", 1)[0]
text = re.sub(r"#[^\n]*", "", open(cm).read())
def expand(s):
    return s.replace("${ES_ROOT}", es).replace("${CMAKE_CURRENT_SOURCE_DIR}", unit).replace("${CMAKE_BINARY_DIR}", b)
for flags in re.findall(r"add_compile_options\(([^)]*)\)", text):
    print("cflags", flags.strip())
for flags in re.findall(r"add_link_options\(([^)]*)\)", text):
    print("lflags", flags.strip())
for src, dst in re.findall(r"configure_file\(\s*(\S+)\s+(\S+)\s+COPYONLY\)", text):
    print("copy", expand(src), expand(dst))
m = re.search(r"add_executable\(\s*jobs-tests\s+([^)]*)\)", text)
for s in m.group(1).split():
    print("src", expand(s))
for kind, body in re.findall(r"target_include_directories\(\s*jobs-tests\s+(BEFORE\s+PRIVATE|PRIVATE)\s+([^)]*)\)", text):
    for d in body.split():
        print("inc", expand(d))
PY
CFLAGS=$(awk '$1=="cflags"{$1=""; print}' "${B}/plan.txt")
LFLAGS=$(awk '$1=="lflags"{$1=""; print}' "${B}/plan.txt")
while read -r kind src dst; do
  [ "${kind}" = copy ] || continue
  case "${dst}" in */under-test/*) cp "${src}" "${dst}" || exit 2 ;; esac
done < "${B}/plan.txt"
mapfile -t SRCS < <(awk '$1=="src"{print $2}' "${B}/plan.txt")
mapfile -t INCS < <(awk '$1=="inc"{print "-I"; print $2}' "${B}/plan.txt")
echo "g++: $(g++ --version | head -1)"
echo "\$ g++ -std=c++17 -pthread ${CFLAGS} ${LFLAGS} ${INCS[*]} <${#SRCS[@]} sources> -o jobs-tests"
printf '    %s\n' "${SRCS[@]}"
# shellcheck disable=SC2086
if ! g++ -std=c++17 -pthread ${CFLAGS} ${LFLAGS} "${INCS[@]}" "${SRCS[@]}" -o "${B}/jobs-tests" > "${B}/build.log" 2>&1; then
  echo "BUILD FAIL jobs-tests:"; tail -n 20 "${B}/build.log"; exit 1
fi
echo "built jobs-tests"
( cd "${B}" && ./jobs-tests ) > "${B}/run.log" 2>&1; rc=$?
echo "RUN jobs-tests: rc ${rc}; $(grep -E '^\[doctest\] (test cases|assertions):' "${B}/run.log" | tr -s ' ' | tr '\n' ' ')"
[ "${rc}" -eq 0 ] || { grep -E 'ERROR|FAILED|runtime error|AddressSanitizer' "${B}/run.log" | head -n 15; exit 1; }
exit 0
