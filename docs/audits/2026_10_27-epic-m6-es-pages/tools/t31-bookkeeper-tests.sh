#!/bin/bash
# T31 (#678) S4: tests/app-unit's bookkeeper-tests, built with the host's g++
# because the host has no cmake. The sources, the definition and the include
# order are read from tests/app-unit/CMakeLists.txt's bookkeeper-tests block,
# not typed: SaveStateBookkeeper.cpp is copied into the build tree first, as
# its configure_file does, so its quoted includes find fakes/ before the real
# headers beside it. Prints the binary's own doctest lines; exit 0 when it
# built and passed, 1 when a build or a run failed, 2 when it could not start.
#   bash t31-bookkeeper-tests.sh <es tree> <build dir> [<SaveStateBookkeeper.cpp to test>]
set -uo pipefail
ES=${1:?es tree}; B=${2:?build dir}; UNDER=${3:-$ES/es-app/src/SaveStateBookkeeper.cpp}
CM=$ES/tests/app-unit/CMakeLists.txt
[ -r "$CM" ] || { echo "t31-bookkeeper-tests: $CM unreadable" >&2; exit 2; }
mkdir -p "$B/under-test"
srcs=$(python3 -I - "$CM" "$ES" "$B" <<'PY'
import re, sys
cm, es, b = sys.argv[1:4]
text = re.sub(r"#[^\n]*", "", open(cm).read())
m = re.search(r"add_executable\(\s*bookkeeper-tests\s+([^)]*)\)", text)
if not m: sys.exit("no bookkeeper-tests target")
for s in m.group(1).split():
    print(s.replace("${CMAKE_CURRENT_SOURCE_DIR}", es + "/tests/app-unit").replace("${ES_ROOT}", es).replace("${CMAKE_BINARY_DIR}", b))
PY
) || exit 2
cp "$UNDER" "$B/under-test/SaveStateBookkeeper.cpp" || exit 2
rm -f "$B/cloud_sync.lock"
out=$(g++ -std=c++17 -g -fno-omit-frame-pointer -fsanitize=address,undefined -pthread \
  -DCLOUD_SYNC_LOCK_PATH="\"$B/cloud_sync.lock\"" \
  -I "$ES/tests/app-unit/fakes" -I "$ES/es-app/src" -I "$ES/es-core/src" -I "$ES/external" \
  $srcs -o "$B/bookkeeper-tests" 2>&1); rc=$?
if [ $rc -ne 0 ]; then echo "BUILD FAIL bookkeeper-tests: $(printf '%s\n' "$out" | grep -m3 -E 'error' | sed -E 's#^/[^ ]*/##' | tr '\n' ' ')"; exit 1; fi
(cd "$B" && timeout 300 ./bookkeeper-tests 2>&1) > "$B/run.txt"; rc=$?
grep -E '^\[doctest\] (test cases|assertions)|ERROR|CHECK|REQUIRE' "$B/run.txt" | head -20
echo "RUN bookkeeper-tests: rc $rc"
exit $([ $rc -eq 0 ] && echo 0 || echo 1)
