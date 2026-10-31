#!/bin/bash
# Each generator: run clean (expect rc 0), then three constructed drifts, each expected rc 1 with a FAIL line:
#   (a) a wrong expectation; (b) the paths list with a cited file dropped; (c) the pin's paths read at the base
#   bccd715707, where the cited lines' texts have moved. Run from the distribution worktree.
A=docs/audits/2026_10_31-epic-m6-es-core-window-input
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682
P=16dbac5211; PL=.qa-scratch/t35/paths.txt; T=/workspace/tmp/m6-t35/tmp
one() {  # name expect-args wrong-key dropped-file
  g=$1; ok=$2; bad=$3; drop=$4
  /usr/bin/grep -v -x -F "$drop" "$PL" > "$T/paths-minus.txt"
  echo "== $g"
  python3 -I "$A/tools/$g" "$W" "$P" "$PL" $ok > "$T/g.out" 2>&1; rc=$?
  echo "clean rc=$rc"; tail -n 1 "$T/g.out"
  python3 -I "$A/tools/$g" "$W" "$P" "$PL" $bad > "$T/g.out" 2>&1; rc=$?
  echo "(a) $bad rc=$rc"; /usr/bin/grep -m 2 '^FAIL' "$T/g.out"
  python3 -I "$A/tools/$g" "$W" "$P" "$T/paths-minus.txt" $ok > "$T/g.out" 2>&1; rc=$?
  echo "(b) without $drop rc=$rc"; /usr/bin/grep -m 2 '^FAIL' "$T/g.out"
  python3 -I "$A/tools/$g" "$W" bccd715707 "$PL" $ok > "$T/g.out" 2>&1; rc=$?
  echo "(c) at bccd715707 rc=$rc"; /usr/bin/grep -m 2 '^FAIL' "$T/g.out"; /usr/bin/grep -c '^FAIL' "$T/g.out"
}
date -u +%FT%TZ
one t35-coverage.py "rows=96 added=1 modified=12 upstream=83 inv_fork=13 inv_up=83 lines=22575" "rows=95" es-core/src/Window.cpp
one t35-leads.py "leads=29 cases=27" "cases=26" es-core/src/Window.cpp
one t35-surfaces.py "rows=22 containers=5 sites=15" "sites=14" es-core/src/Window.cpp
one t35-input.py "writes=9 real_writes=5 reads_counted=2 exists=5 rows=12" "real_writes=7" es-core/src/InputManager.cpp
one t35-locks.py "lines=67 files=11 locks=10 weak=2 includes=4" "lines=66" es-core/src/Window.cpp
one t35-lifetimes.py "threads=18 detach=4 delete_this=17 posts=6 raw=8 rows=52" "detach=5" es-core/src/Window.cpp
one t35-scripts.py "sites=4 shell_direct=0" "shell_direct=1" es-core/src/Scripting.cpp
one t35-words.py "lines=86 files=10 occurrences=97 msgids=61 fr_missing=0 tiered=0 plural_calls=28 plural_fr_missing=0 glyph_lines=27" "msgids=62" es-core/src/Window.cpp
one t35-includes.py "headers=51 cpp_named_once=44 unregistered=2 batocera=9 batocera_96=7 cmake_ifs=2 rocknix=3 map_titles=0" "rocknix=4" es-core/src/Window.cpp
date -u +%FT%TZ
