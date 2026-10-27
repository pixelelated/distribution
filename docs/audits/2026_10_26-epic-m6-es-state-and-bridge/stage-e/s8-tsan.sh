#!/bin/bash
# T21 (#668) S8: es-settings-tests' sources built with ThreadSanitizer, and
# the case that saves on one thread while another reads and writes run alone.
# Prints the case's rc and ThreadSanitizer's summary lines (paths cut).
#   PUGIXML_INCLUDE_DIR=<dir holding pugixml/> bash s8-tsan.sh <es tree> <scratch>
set -uo pipefail
ES=${1:?es tree}; S=${2:?scratch}
PX=${PUGIXML_INCLUDE_DIR:?pugixml}
mkdir -p "$S"
g++ -std=c++17 -O1 -g -fsanitize=thread -pthread -I "$ES/es-core/src" -I "$ES/external" -I "$PX" \
  "$ES/es-app/tests/unit/SettingsTests.cpp" "$ES/es-core/src/Settings.cpp" "$ES/es-core/src/utils/AtomicFileUtil.cpp" \
  "$ES/es-core/src/utils/FileSystemUtil.cpp" "$ES/es-core/src/utils/StringUtil.cpp" "$ES/es-core/src/utils/md5.cpp" \
  "$PX/pugixml/src/pugixml.cpp" -o "$S/es-settings-tests-tsan" > "$S/build.log" 2>&1 \
  || { echo "BUILD FAIL"; tail -n 15 "$S/build.log"; exit 2; }
echo "== built from $(git -C "$ES" rev-parse --short=10 HEAD)$(git -C "$ES" diff --quiet HEAD -- es-core || echo ' + the working tree')"
TSAN_OPTIONS="halt_on_error=0 report_signal_unsafe=0" "$S/es-settings-tests-tsan" -tc='*ThreadSanitizer*' > "$S/run.log" 2>&1; rc=$?
echo "rc $rc"
grep -c '^WARNING: ThreadSanitizer' "$S/run.log" | sed 's/^/ThreadSanitizer warnings: /'
grep -E '^SUMMARY: ThreadSanitizer' "$S/run.log" | sed -E 's#/[^ :]*/##g' | sort | uniq -c | head -n 5
grep -E 'test cases:' "$S/run.log"
