#!/bin/bash
# T26 (#673) stage B: the generators of 02's tables, the fixture and the
# three negative controls, each with its exit and wall time. Run from the
# distribution worktree; writes stage-b/*.txt beside this script.
export LC_ALL=C; W=/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673; PIN=16dbac5211eea7e70db7394372033be2be7df829; F=es-app/src/guis/GuiMenu.cpp
A=docs/audits/2026_10_27-epic-m6-es-guimenu; B=$A/stage-b; T=$A/tools; export TMPDIR=/workspace/tmp/m6-t26/tmp; mkdir -p "$TMPDIR"
git -C "$W" show "$PIN:$F" > "$TMPDIR/pin.cpp"; git -C "$W" show "$PIN:es-app/src/guis/GuiMenu.h" > "$TMPDIR/pin.h"
rm -rf "$TMPDIR/tests"; mkdir -p "$TMPDIR/tests"; git -C "$W" archive "$PIN" tests | tar -x -C "$TMPDIR"
run() { # <label> <output file> <command string>
  local t0 t1 rc
  t0=$(date +%s.%N); eval "$3" > "$2" 2>&1; rc=$?; t1=$(date +%s.%N)
  printf '== %s  (rc %s, %.2f s) -> %s\n%s\n\n' "$1" "$rc" "$(echo "$t1 - $t0" | bc)" "${2#$A/}" "$(tail -n 4 "$2" | cut -c1-300)"
}
run "structure: per-line liveness" "$B/lines.txt" 'python3 -I -B $T/t26-structure.py $TMPDIR/pin.cpp $TMPDIR/pin.h $TMPDIR/tests --lines'
run "rows" "$B/rows.txt" 'python3 -I -B $T/t26-rows.py $TMPDIR/pin.cpp . 8ebaf8daad --table --writes --live $B/lines.txt'
run "pages" "$B/pages.txt" 'python3 -I -B $T/t26-pages.py $TMPDIR/pin.cpp --table --dialogs'
run "structure: transitions, reads, duplicates, conditionals" "$B/structure.txt" 'python3 -I -B $T/t26-structure.py $TMPDIR/pin.cpp $TMPDIR/pin.h $TMPDIR/tests --transitions --reads --dups --ifs'
run "merge debt" "$B/merge.txt" 'python3 -I -B $T/t26-merge.py $W bccd715707 rocknix/master $PIN --table'
run "fixture: GetShOutput, verbatim" "$B/positives/getshoutput.out" 'g++ -std=c++17 -O0 -o $TMPDIR/getshoutput $B/positives/getshoutput.cpp && bwrap --clearenv --setenv PATH /usr/bin:/bin --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib --ro-bind-try /lib64 /lib64 --ro-bind $TMPDIR/getshoutput /fixture --proc /proc --dev /dev --unshare-all /fixture'
# The negative controls: each generator must exit 1 on a constructed drift.
sed '9485d' "$TMPDIR/pin.cpp" > "$TMPDIR/neg-rows.cpp"
sed '1134s/new GuiMsgBox(/new GuiMsgBoxGone(/' "$TMPDIR/pin.cpp" > "$TMPDIR/neg-pages.cpp"
sed '7792s/exists(qrPath)/exists(qrPath, false)/' "$TMPDIR/pin.cpp" > "$TMPDIR/neg-structure.cpp"
run "negative: rows without :9485" "$B/neg-rows.txt" 'python3 -I -B $T/t26-rows.py $TMPDIR/neg-rows.cpp . 8ebaf8daad'
run "negative: pages with :1134 renamed" "$B/neg-pages.txt" 'python3 -I -B $T/t26-pages.py $TMPDIR/neg-pages.cpp'
run "negative: structure with :7792 uncached" "$B/neg-structure.txt" 'python3 -I -B $T/t26-structure.py $TMPDIR/neg-structure.cpp $TMPDIR/pin.h $TMPDIR/tests'
run "negative: merge at 23df404f6^" "$B/neg-merge.txt" 'python3 -I -B $T/t26-merge.py $W bccd715707 rocknix/master 23df404f6^'
