#!/bin/bash
# T35 (#682): T34's t34-build-tests.sh (#681, copied by git show from feature/m6-es-core-components-681 at 3e285d86b3 and renamed), itself T33's t33-build-tests.sh (#680, copied by git show from its branch and renamed), itself T32's t32-build-tests.sh (#679, copied and renamed), itself T31's t31-build-tests.sh, itself T26's t26-build-tests.sh (#673, copied by git show from feature/m6-es-guimenu-673 and renamed), itself T21's t21-build-tests.sh (#668, copied by git show at c500e6bd53), itself T20's t20-build-tests.sh (#667, from T18's t18-build-tests.sh, #665) renamed: EmulationStation's unit tests, built with the host's g++ by
# commands generated from es-app/tests/unit/CMakeLists.txt, because the host
# has no cmake (the brief's section 5, version 2). Then each binary is run and
# its own summary line kept.
#
#   RAPIDJSON_INCLUDE_DIR=<dir holding rapidjson/> \
#     bash docs/audits/2026_10_31-epic-m6-es-core-window-input/tools/t35-build-tests.sh <es tree> <build dir>
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
[ -r "${CM}" ] || { echo "t35-build-tests: ${CM} unreadable" >&2; exit 2; }
[ -n "${RAPIDJSON_INCLUDE_DIR:-}" ] && [ -r "${RAPIDJSON_INCLUDE_DIR}/rapidjson/document.h" ] \
  || { echo "t35-build-tests: rapidjson/document.h not under RAPIDJSON_INCLUDE_DIR='${RAPIDJSON_INCLUDE_DIR:-}'; nothing built" >&2; exit 2; }
command -v g++ >/dev/null || { echo "t35-build-tests: no g++" >&2; exit 2; }
mkdir -p "${B}"
# target -> its source list, from CMakeLists.txt itself.
python3 -I - "${CM}" "${ES}" "${PUGIXML_INCLUDE_DIR:-${ES}/external}" > "${B}/sources.txt" <<'PY' || exit 2
import re, sys
cm, es = sys.argv[1], sys.argv[2]
pugi = sys.argv[3] if len(sys.argv) > 3 else ""
text = re.sub(r"#[^\n]*", "", open(cm).read())
unit = cm.rsplit("/", 1)[0]
for kind, name, body in re.findall(r"add_(executable|library)\(\s*([A-Za-z0-9_-]+)\s+(?:OBJECT\s+)?([^)]*)\)", text):
    for s in body.split():
        s = s.replace("${CMAKE_CURRENT_SOURCE_DIR}", unit).replace("${ES_ROOT}", es).replace("${PUGIXML_INCLUDE_DIR}", pugi)
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
  # A failed compile must leave no binary behind for the run below (T34 S3).
  rm -f -- "${B:?}/${name:?}" "${B:?}/${name:?}.run.log"
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
# es-fs-tests (T21 S4, #1191), when the tree's CMakeLists has it.
mapfile -t S5 < <(srcs es-fs-tests)
FS=""
if [ "${#S5[@]}" -gt 0 ]; then
  FS=es-fs-tests
  build es-fs-tests -I "${ES}/es-core/src" -I "${ES}/external" -- "${S5[@]}"
fi
# es-settings-tests (T21 S8, #1200), when the tree names it: pugixml from
# PUGIXML_INCLUDE_DIR (default <es tree>/external), as the CMakeLists has it.
mapfile -t S6 < <(srcs es-settings-tests)
ST=""
if [ "${#S6[@]}" -gt 0 ]; then
  PX="${PUGIXML_INCLUDE_DIR:-${ES}/external}"
  [ -r "${PX}/pugixml/src/pugixml.hpp" ] || { echo "t35-build-tests: pugixml/src/pugixml.hpp not under PUGIXML_INCLUDE_DIR='${PX}'"; exit 2; }
  echo "pugixml: ${PX} (pugixml.hpp $(sha256sum < "${PX}/pugixml/src/pugixml.hpp" | cut -c1-16))"
  ST=es-settings-tests
  build es-settings-tests -I "${ES}/es-core/src" -I "${ES}/external" -I "${PX}" -- "${S6[@]}"
fi
# Any other test the tree's CMakeLists names (T21 S13 on): built with the
# include roots every target here uses, pugixml and rapidjson among them.
MORE=""
for extra in $(awk '{print $1}' "${B}/sources.txt" | sort -u); do
  case " es-unit-tests es-file-tests es-conf-tests es-file-tests-win32 atomicfile-win32-branch es-fs-tests es-settings-tests " in *" ${extra} "*) continue;; esac
  mapfile -t SX < <(srcs "${extra}")
  MORE="${MORE} ${extra}"
  build "${extra}" -I "${ES}/es-app/src" -I "${ES}/es-core/src" -I "${ES}/external" -I "${PUGIXML_INCLUDE_DIR:-${ES}/external}" -I "${RAPIDJSON_INCLUDE_DIR}" -- "${SX[@]}"
done
# T33 (#680): tests/app-unit's app-unit-tests, which no lane had built (T18
# 02:50-58). Its sources and flags are its own CMakeLists' (`:35-46`):
# main.cpp and the five case files, include roots es-app/src, es-core/src and
# external (no fakes/ for this target: the file puts fakes/ BEFORE only for
# proxycards-tests, jobs-tests and bookkeeper-tests), -g with
# -fsanitize=address,undefined. Parsed, never typed.
APPCM="${ES}/tests/app-unit/CMakeLists.txt"
APP=""
if [ -r "${APPCM}" ]; then
  mapfile -t SA < <(python3 -I - "${APPCM}" <<'PYA'
import re, sys
cm = sys.argv[1]
text = re.sub(r"#[^\n]*", "", open(cm).read())
m = re.search(r"add_executable\(\s*app-unit-tests\s+([^)]*)\)", text)
d = cm.rsplit("/", 1)[0]
for s in (m.group(1).split() if m else []):
    print(s.replace("${CMAKE_CURRENT_SOURCE_DIR}", d))
PYA
)
  if [ "${#SA[@]}" -gt 0 ]; then
    APP=app-unit-tests
    build app-unit-tests -g -fno-omit-frame-pointer -fsanitize=address,undefined -I "${ES}/es-app/src" -I "${ES}/es-core/src" -I "${ES}/external" -- "${SA[@]}"
  fi
fi
mapfile -t S4o < <(srcs atomicfile-win32-branch)
mapfile -t S4 < <(srcs es-file-tests-win32)
echo "\$ ${CXX[*]} -D_WIN32 -c ${S4o[*]} -o atomicfile-win32-branch.o"
if "${CXX[@]}" -D_WIN32 -I "${ES}/es-core/src" -c "${S4o[@]}" -o "${B}/atomicfile-win32-branch.o" > "${B}/win32obj.build.log" 2>&1; then
  build es-file-tests-win32 -I "${ES}/es-core/src" -I "${ES}/external" -- "${S4[@]}" "${B}/atomicfile-win32-branch.o"
else
  echo "BUILD FAIL atomicfile-win32-branch:"; tail -n 15 "${B}/win32obj.build.log"; FAIL=1
fi
for t in es-unit-tests es-file-tests es-conf-tests es-file-tests-win32 ${FS} ${ST} ${MORE} ${APP}; do
  [ -x "${B}/${t}" ] || { echo "RUN ${t}: not built"; FAIL=1; continue; }
  "${B}/${t}" > "${B}/${t}.run.log" 2>&1; rc=$?
  echo "RUN ${t}: rc ${rc}; $(grep -E '^\[doctest\] (test cases|assertions):' "${B}/${t}.run.log" | tr -s ' ' | tr '\n' ' ')"
  [ "${rc}" -eq 0 ] || { FAIL=1; grep -E 'ERROR|FAILED' "${B}/${t}.run.log" | head -n 10; }
done
# T35 (#682): window-input-tests, the candidates' cases over the pin's lines
# lifted verbatim by t35-extract.py (refused unless each range holds its
# code), with the pin's watchers/WatchersManager.cpp linked behind
# tests/app-unit/fakes/Log.h (fakes/ first, as the app-unit targets put it)
# and pugixml header-only from PUGIXML_INCLUDE_DIR.
HERE="$(cd "$(dirname "$0")" && pwd)"
X="${B}/x"
# A refused extraction must leave nothing to build against: the directory is
# cleared first, so an earlier run's extracts are never compiled (stage E S2:
# a refused run built window-input-tests from the previous run's x/).
rm -rf -- "${B:?}/x"
python3 -B -I "${HERE}/t35-extract.py" "${ES}" "$(git -C "${ES}" rev-parse HEAD)" "${X}" || { echo "t35-build-tests: the extracts were refused; window-input-tests not built"; FAIL=1; }
WT=""
if [ -d "${X}" ]; then
  WT=window-input-tests
  PX="${PUGIXML_INCLUDE_DIR:-${ES}/external}"
  [ -r "${PX}/pugixml/src/pugixml.hpp" ] || { echo "t35-build-tests: pugixml/src/pugixml.hpp not under PUGIXML_INCLUDE_DIR='${PX}'"; exit 2; }
  echo "pugixml (window-input-tests, floor-tests): ${PX} (pugixml.hpp $(sha256sum < "${PX}/pugixml/src/pugixml.hpp" | cut -c1-16))"
  build window-input-tests "-DT35_X=\"${X}\"" -I "${X}" -I "${ES}/external" -I "${ES}/tests/app-unit/fakes" -I "${ES}/es-core/src" -I "${PX}" -- "${HERE}/t35-window-input-tests.cpp" "${ES}/es-core/src/watchers/WatchersManager.cpp" || true
  # T35 (#682) stage E S0 (ruling 21): floor-tests, the floor cases no stream holds,
  # over their own lifts; the pin's InputConfig.h with SDL from stage-a/fakes.
  WT="${WT} floor-tests"
  build floor-tests "-DT35_X=\"${X}\"" -I "${X}" -I "${ES}/external" -I "${ES}/tests/app-unit/fakes" -I "$(dirname "${HERE}")/stage-a/fakes" -I "${ES}/es-core/src" -I "${PX}" -- "${HERE}/t35-floor-tests.cpp" || true
fi
for t in ${WT}; do
  [ -x "${B}/${t}" ] || { echo "RUN ${t}: not built"; FAIL=1; continue; }
  "${B}/${t}" > "${B}/${t}.run.log" 2>&1; rc=$?
  echo "RUN ${t}: rc ${rc}; $(grep -E '^\[doctest\] (test cases|assertions):' "${B}/${t}.run.log" | tr -s ' ' | tr '\n' ' ')"
  grep -E '^TEST CASE:|ERROR: CHECK|MESSAGE:|  values: CHECK|ResetComponent returned' "${B}/${t}.run.log" | sed 's/^/    /' | head -n 40
  # every failing case by name, untruncated (stage E S1 on: the 40-line excerpt above can cut one)
  grep -E '^TEST CASE:' "${B}/${t}.run.log" | sed 's/^TEST CASE: */    failing: /' | sort -u
  [ "${rc}" -eq 0 ] || FAIL=1
done
# T35 (#682): the two sanitizer programs (their sources under ../stage-c/), each run
# and its first report line kept: 3.17 over the posted functions, 3.3 over the watchers.
san() { # <name> <sanitizer> <source> [extra sources...]
  local n=$1 f=$2 src=$3; shift 3
  rm -f -- "${B:?}/${n:?}" "${B:?}/${n:?}.run.log"
  if g++ -std=c++17 -O1 -g -fno-omit-frame-pointer -fsanitize="$f" -pthread -I "${X}" -I "${ES}/tests/app-unit/fakes" -I "${ES}/es-core/src" "${src}" "$@" -o "${B}/${n}" > "${B}/${n}.build.log" 2>&1; then
    "${B}/${n}" > "${B}/${n}.run.log" 2>&1; local rc=$?
    echo "SAN ${n} (-fsanitize=${f}): rc ${rc}; $(grep -m1 -E 'ERROR: AddressSanitizer|WARNING: ThreadSanitizer|SUMMARY:' "${B}/${n}.run.log" || echo 'no sanitizer report')"
  else
    echo "SAN ${n}: BUILD FAIL"; tail -n 8 "${B}/${n}.build.log"
  fi
}
AUD="$(dirname "${HERE}")"
san tsan-posts thread "${AUD}/stage-c/tsan-posts.cpp"
san tsan-watchers thread "${AUD}/stage-c/tsan-watchers.cpp" "${ES}/es-core/src/watchers/WatchersManager.cpp"
san asan-watchers address "${AUD}/stage-c/asan-watchers.cpp" "${ES}/es-core/src/watchers/WatchersManager.cpp"
# The total, from the binaries' own summary lines: a record quotes this line
# rather than a sum written by hand (T21 stage E: totals written without
# adding were found 2 to 53 cases high, S2 to S13).
TOTAL=0; BINS=0
for t in es-unit-tests es-file-tests es-conf-tests es-file-tests-win32 ${FS} ${ST} ${MORE} ${APP} ${WT}; do
  [ -r "${B}/${t}.run.log" ] || continue
  n=$(grep -m1 -E '^\[doctest\] test cases:' "${B}/${t}.run.log" | grep -o -E '[0-9]+' | head -n 1)
  [ -n "${n}" ] && { TOTAL=$((TOTAL + n)); BINS=$((BINS + 1)); }
done
echo "TOTAL: ${TOTAL} test cases in ${BINS} binaries"
exit "${FAIL}"
