#!/bin/bash
# T18 (#665) stage A: the brief's section 5 runs, each with its exit and wall
# time. Read-only but for one compile: the unit tests, built with the host's
# g++ by tools/t18-build-tests.sh into /workspace/tmp/m6-t18/build (the brief
# allows the host compiler for es-app/tests/unit). No fetch, no other build,
# no plan, no guest, nothing on a handheld, no M7 build root or m7-* ES
# worktree, no tools/council/run call. Every line that prints source passes
# the read filter (D-QA-021) where it could carry a credential word.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-cloud-pages-665
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t18/tmp
A=docs/audits/2026_10_26-epic-m6-es-cloud-pages
OUT=${OUT:-/workspace/tmp/m6-t18/runner/out}
W=/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665
PIN=16dbac5211eea7e70db7394372033be2be7df829
BASE=bccd71570
DISPATCH=cbf6d7ef83
EIGHT="es-app/src/CloudText.cpp es-app/src/CloudText.h es-app/src/CloudTransferJob.cpp es-app/src/CloudTransferJob.h es-app/src/guis/GuiCloudTransfer.cpp es-app/src/guis/GuiCloudTransfer.h es-app/src/ThreadedCloudSync.cpp es-app/src/ThreadedCloudSync.h"
SCRIPTS="projects/ROCKNIX/packages/network/rclone/sources projects/ROCKNIX/packages/rocknix/sources/scripts projects/ROCKNIX/packages/network/raofflineproxy/sources"
mkdir -p "$TMPDIR" "$OUT" .qa-scratch/t18
printf 'id\trc\tseconds\tstarted_utc\n' > "$OUT/runs.tsv"
F() { grep -v -i -E 'key|pass|token|user|psk'; }
run() {
  local id=$1; shift
  local t0 t1 rc started
  started=$(date -u +%H:%M:%S); t0=$(date +%s.%N)
  ( "$@" ) > "$OUT/$id.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.2f\t%s\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)" "$started" >> "$OUT/runs.tsv"
}
pshow() { git -C "$W" show "$PIN:$1"; }
r01_block() { python3 -I "$D/$A/stage-a/scope.py"; wc -l < .qa-scratch/t18/paths.txt; }
r02_lines() { while IFS= read -r p; do printf '%6d %s\n' "$(pshow "$p" | wc -l)" "$p"; done < .qa-scratch/t18/paths.txt | awk '{s+=$1; print} END {print "wc -l lines", s}'; }
r03_in_merge_base() { while IFS= read -r p; do git -C "$W" cat-file -e "$BASE:$p" 2>/dev/null && echo "IN MERGE BASE: $p"; done < .qa-scratch/t18/paths.txt | wc -l; }
r04_pin_and_base() { git -C "$W" merge-base upstream/master "$PIN"; echo "ahead $(git -C "$W" rev-list --count upstream/master.."$PIN") behind $(git -C "$W" rev-list --count "$PIN"..upstream/master)"; git -C "$W" rev-parse upstream/master; }
r05_sources() { grep -c '^es-app/src/' .qa-scratch/t18/paths.txt; grep '^es-app/src/' .qa-scratch/t18/paths.txt | while IFS= read -r p; do pshow "$p" | wc -l; done | awk '{s+=$1} END {print "source lines", s}'; grep -c '^es-app/tests/' .qa-scratch/t18/paths.txt; grep '^es-app/tests/' .qa-scratch/t18/paths.txt | while IFS= read -r p; do pshow "$p" | wc -l; done | awk '{s+=$1} END {print "test lines", s}'; }
r06_test_cases() { grep '^es-app/tests/' .qa-scratch/t18/paths.txt | grep '\.cpp$' | while IFS= read -r p; do printf '%s %s %s\n' "$(pshow "$p" | grep -c 'TEST_CASE(')" "$(pshow "$p" | grep -c -E 'CHECK[A-Z_]*\(')" "$p"; done | tee /dev/stderr | awk '{c+=$1; k+=$2; n++} END {print "TEST_CASE", c, "checks", k, "files", n}'; printf 'CloudTextTests TEST_CASE %s\n' "$(pshow es-app/tests/unit/CloudTextTests.cpp | grep -c 'TEST_CASE(')"; }
# The brief's regex under GNU grep -E reads \s inside [...] as a backslash and
# an s, so a return type with a space in it (std::pair<std::string, std::string>)
# is missed: 44. Under grep -P, or the interactive shell's ugrep-backed grep
# function the brief's 47 came from, \s in a class is whitespace: 47.
r07_declarations() { printf 'grep -E (GNU) %s\n' "$(pshow es-app/src/CloudText.h | grep -c -E '^\s+[A-Za-z_:<>,\s]+ [A-Za-z_]+\(.*\);')"; printf 'grep -P (GNU) %s\n' "$(pshow es-app/src/CloudText.h | grep -c -P '^\s+[A-Za-z_:<>,\s]+ [A-Za-z_]+\(.*\);')"; echo '--- the three -E misses'; diff <(pshow es-app/src/CloudText.h | grep -n -E '^\s+[A-Za-z_:<>,\s]+ [A-Za-z_]+\(.*\);') <(pshow es-app/src/CloudText.h | grep -n -P '^\s+[A-Za-z_:<>,\s]+ [A-Za-z_]+\(.*\);') | grep '^>'; }
r08_markers_exits() { pshow es-app/src/CloudText.cpp | grep -n -E 'rfind\(">>> [a-z]+ ", 0\)' | cut -c1-80; pshow es-app/src/CloudText.cpp | grep -n 'exitCode == 75'; echo '--- whyForCode'; pshow es-app/src/ThreadedCloudSync.cpp | sed -n '80,98p'; echo '--- 0 and 9'; pshow es-app/src/CloudTransferJob.cpp | sed -n '302p'; pshow es-app/src/guis/GuiCloudTransfer.cpp | sed -n '289p;440p'; }
r09_wrappers() { git -C "$W" grep -n -E 'setsid sh -c|trap .. PIPE|popen\(' "$PIN" -- es-app/src/CloudTransferJob.cpp es-app/src/ThreadedCloudSync.cpp | sed "s/^$PIN://" | cut -c1-140; }
r10_stamps() { pshow es-app/src/ThreadedCloudSync.cpp | grep -n -E 'STAMP_DIR|readStamps|std::rename|writeAllText' | cut -c1-110; echo '--- CloudText.cpp:180-192'; pshow es-app/src/CloudText.cpp | sed -n '180,192p'; }
r11_exists() { git -C "$W" grep -c -E 'FileSystem::exists\(' "$PIN" -- $EIGHT | sed "s/^$PIN://"; echo "(no line above = 0 in the eight)"; git -C "$W" grep -c -E 'FileSystem::exists\(' "$PIN" -- es-app/src | sed "s/^$PIN://" | sort -t: -k2 -n -r | head -n 3; }
r12_lifetimes() { git -C "$W" grep -n -E 'delete this|postToUiThread|\.detach\(\)|sleep_for|SIGKILL|SIGTERM|kill\(' "$PIN" -- es-app/src/guis/GuiCloudTransfer.cpp es-app/src/ThreadedCloudSync.cpp es-app/src/CloudTransferJob.cpp | sed "s/^$PIN://" | cut -c1-130; }
r13_why_table() {
  export LC_ALL=C
  pshow es-app/src/CloudText.cpp | sed -n '414,467p' | grep -c '{ "'
  pshow es-app/src/CloudText.cpp | sed -n '414,467p' | grep -o -E '\{ "[A-Z][^"]+"' | sed 's/^{ "//; s/"$//' | sort -u | tee "$TMPDIR/why-es.txt" | wc -l
  git grep -h -o -E '>>> why [A-Z][A-Z0-9 ,.'"'"'?!-]+|say_why "[A-Z][^"]+"|\bwhy "[A-Z][^"]+"' 8ebaf8daad -- $SCRIPTS | sed -E 's/^(>>> why |say_why "|why ")//; s/"$//' | sort -u | tee "$TMPDIR/why-scripts.txt" | wc -l
  echo "shared $(comm -12 "$TMPDIR/why-es.txt" "$TMPDIR/why-scripts.txt" | wc -l)"; echo '--- scripts only'; comm -13 "$TMPDIR/why-es.txt" "$TMPDIR/why-scripts.txt"; echo "--- ES only $(comm -23 "$TMPDIR/why-es.txt" "$TMPDIR/why-scripts.txt" | wc -l)"; comm -23 "$TMPDIR/why-es.txt" "$TMPDIR/why-scripts.txt"
  git grep -n -E 'say_why "\$|why "\$' 8ebaf8daad -- projects/ROCKNIX/packages/network/rclone/sources projects/ROCKNIX/packages/rocknix/sources/scripts | sed 's/^8ebaf8daad://' | tee "$TMPDIR/why-vars.txt" | wc -l; cut -d: -f1 "$TMPDIR/why-vars.txt" | sort | uniq -c
}
r14_strings() { git -C "$W" grep -o -h -E '_\("[^"]*"\)' "$PIN" -- $EIGHT | wc -l; for f in es-app/src/ThreadedCloudSync.cpp es-app/src/guis/GuiCloudTransfer.cpp; do printf '%s occurrences %s unique %s\n' "$f" "$(pshow "$f" | grep -o -E '_\("[^"]*"\)' | wc -l)" "$(pshow "$f" | grep -o -E '_\("[^"]*"\)' | sort -u | wc -l)"; done; echo "WIFI: $(git -C "$W" grep -o -h -E '_\("[^"]*WIFI[^"]*"\)' "$PIN" -- $EIGHT | wc -l)"; echo "BACK UP / BACKUP:"; git -C "$W" grep -o -h -E '_\("[^"]*BACK ?UP[^"]*"\)' "$PIN" -- $EIGHT | sort -u; }
r15_xgettext() { while IFS= read -r p; do n=$(pshow "$p" | grep -c -P '^\s*//.*[^\x00-\x7F]'); [ "$n" -gt 0 ] && echo "$n $p"; done < .qa-scratch/t18/paths.txt; echo "(no line = 0 comment lines)"; for f in es-app/src/guis/GuiCloudTransfer.cpp es-app/src/CloudTransferJob.cpp es-app/src/CloudTransferJob.h; do printf '%s %s\n' "$(pshow "$f" | grep -c -P '[^\x00-\x7F]')" "$f"; pshow "$f" | grep -n -P '[^\x00-\x7F]' | cut -c1-150; done; }
r16_history() { tr '\n' '\0' < .qa-scratch/t18/paths.txt | xargs -0 git -C "$W" log --no-merges --format='%h %an' $BASE.."$PIN" -- | tee "$TMPDIR/hist.txt" | wc -l; cut -d' ' -f2- "$TMPDIR/hist.txt" | sort | uniq -c | sort -rn; tr '\n' '\0' < .qa-scratch/t18/paths.txt | xargs -0 git -C "$W" log --no-merges --format=%ad --date=short $BASE.."$PIN" -- | sort | sed -n '1p;$p'; tr '\n' '\0' < .qa-scratch/t18/paths.txt | xargs -0 git -C "$W" log --no-merges --format=%ad --date=format:%Y-%m $BASE.."$PIN" -- | sort | uniq -c; echo '--- the newest ten'; tr '\n' '\0' < .qa-scratch/t18/paths.txt | xargs -0 git -C "$W" log --no-merges --format='%h %ad %s' --date=short -n 10 $BASE.."$PIN" -- | cut -c1-120; echo '--- per file (top 6)'; while IFS= read -r p; do printf '%s %s\n' "$(git -C "$W" log --no-merges --format=%h $BASE.."$PIN" -- "$p" | wc -l)" "$p"; done < .qa-scratch/t18/paths.txt | sort -rn | head -6; }
r17_callers() { git -C "$W" grep -n -E 'new GuiCloudTransfer|ThreadedCloudSync::start|CloudTransferJob::' "$PIN" -- es-app/src | sed "s/^$PIN://" | grep -v -E '^es-app/src/(guis/GuiCloudTransfer|ThreadedCloudSync|CloudTransferJob|CloudText)\.' | cut -c1-120; echo "GuiMenu.cpp lines naming /usr/bin/cloud_: $(pshow es-app/src/guis/GuiMenu.cpp | grep -c '/usr/bin/cloud_')"; }
r18_toolchain() { command -v cmake ninja g++ | sed 's/^/present: /'; for b in /workspace/repos/pixelelated/distribution.worktrees/*/build.pixelelated-GENERIC_X64.x86_64; do [ -d "$b" ] || continue; printf '%s: es-build %s rapidjson %s ninja %s\n' "$(basename "$(dirname "$b")")" "$(ls -d "$b"/build/emulationstation-* 2>/dev/null | wc -l)" "$(ls -d "$b"/build/rapidjson-*/include 2>/dev/null | wc -l)" "$(ls "$b"/toolchain/bin/ninja 2>/dev/null | wc -l)"; done; }
r19_cmake_list() { pshow es-app/tests/unit/CMakeLists.txt | grep -n -E 'add_executable|add_library|target_include_directories|RAPIDJSON|doctest' | cut -c1-120; }
r20_unit_tests() { RAPIDJSON_INCLUDE_DIR=/workspace/tmp/m6-t18/rapidjson bash "$D/$A/tools/t18-build-tests.sh" "$W" /workspace/tmp/m6-t18/build-stage-a; cat /workspace/tmp/m6-t18/rapidjson-check.txt; }
r21_syntax_check() { ES_BUILD_ROOT=/nonexistent tools/es-syntax-check --tree "$W" es-app/src/CloudText.cpp 2>&1 | tail -n 2; echo "rc=${PIPESTATUS[0]}"; }
r22_host_syntax() { g++ -std=c++17 -fsyntax-only -I "$W/es-app/src" -I "$W/es-core/src" "$W/es-app/src/CloudText.cpp" 2>&1 | tail -n 2; echo "host syntax rc=${PIPESTATUS[0]}"; }
r23_untranslated() { tools/es-untranslated --help 2>&1 | head -n 3; echo "(the brief's line passes the tree positionally; the tool takes --es-src)"; tools/es-untranslated --es-src "$W" > "$TMPDIR/untranslated.txt" 2>&1; echo "rc $?"; tail -n 3 "$TMPDIR/untranslated.txt"; grep -E 'CloudText|CloudTransferJob|GuiCloudTransfer|ThreadedCloudSync' "$TMPDIR/untranslated.txt" | head -n 20; echo "lines naming the eight: $(grep -c -E 'CloudText|CloudTransferJob|GuiCloudTransfer|ThreadedCloudSync' "$TMPDIR/untranslated.txt")"; }
r24_menu_map() { grep -n -E '^## (Cloud|Visual evidence)' docs/es-menu-map.md; echo "cloud walks: $(ls tools/vm-walks | grep -c -i -E 'cloud|sync|transfer|backup|restore')"; ls tools/vm-walks | grep -i -E 'cloud|sync|transfer|backup|restore'; tools/es-menu-map-check --es-src "$W" 2>&1 | tail -n 2; echo "rc ${PIPESTATUS[0]}"; }
r25_removal_rule() { git diff --stat $DISPATCH HEAD -- packages projects tools | tail -1; echo "(empty line above = nothing under packages/projects/tools since the dispatch tip)"; git -C "$W" diff --stat "$PIN" HEAD | tail -1; echo "es HEAD $(git -C "$W" rev-parse HEAD)"; }
r26_identity_literal() { # a _( ) literal of the 30 the merge base lacks, for the window's strings check
  git -C "$W" grep -o -h -E '_\("[A-Z][A-Z ,.'"'"'-]{30,}"\)' "$PIN" -- es-app/src/guis/GuiCloudTransfer.cpp es-app/src/ThreadedCloudSync.cpp | sed -E 's/^_\("//; s/"\)$//' | sort -u | while IFS= read -r s; do
    n=$(git -C "$W" grep -c -F -- "$s" "$BASE" -- es-app es-core 2>/dev/null | wc -l); [ "$n" -eq 0 ] && echo "absent from $BASE: $s"; done | head -n 5; }
run r01_block r01_block
run r02_lines r02_lines
run r03_in_merge_base r03_in_merge_base
run r04_pin_and_base r04_pin_and_base
run r05_sources r05_sources
run r06_test_cases r06_test_cases
run r07_declarations r07_declarations
run r08_markers_exits r08_markers_exits
run r09_wrappers r09_wrappers
run r10_stamps r10_stamps
run r11_exists r11_exists
run r12_lifetimes r12_lifetimes
run r13_why_table r13_why_table
run r14_strings r14_strings
run r15_xgettext r15_xgettext
run r16_history r16_history
run r17_callers r17_callers
run r18_toolchain r18_toolchain
run r19_cmake_list r19_cmake_list
run r20_unit_tests r20_unit_tests
run r21_syntax_check r21_syntax_check
run r22_host_syntax r22_host_syntax
run r23_untranslated r23_untranslated
run r24_menu_map r24_menu_map
run r25_removal_rule r25_removal_rule
run r26_identity_literal r26_identity_literal
cat "$OUT/runs.tsv"
