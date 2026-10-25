#!/bin/bash
# T28 stage E (#675): every stream's cases, both sides, one summary line.
#   run-all.sh <unfixed update.sh> <fixed update.sh>
# Rows: S1's four cases on each side (8), and the success path's console
# output compared between the two files (1). Exits 0 only when every row
# meets its side's expectation.
set -u
U=${1:?unfixed update.sh}; X=${2:?fixed update.sh}
H=$(cd "$(dirname "$0")" && pwd)
rows=0; bad=0; cannot=0
for c in updateabl-fail updateabl-slow-fail copy-fail success; do
  for side in unfixed fixed; do
    f=$U; [ $side = fixed ] && f=$X
    line=$("$H/s1/update-case.sh" "$f" $side $c | tail -1); rc=$?
    rows=$((rows+1)); echo "$line"
    case "$line" in *UNEXPECTED*) bad=$((bad+1)) ;; *CANNOT*) cannot=$((cannot+1)) ;; esac
  done
done
a=$("$H/s1/update-case.sh" "$U" unfixed success | grep -E '^  \| (out|err): '); b=$("$H/s1/update-case.sh" "$X" fixed success | grep -E '^  \| (out|err): ')
rows=$((rows+1))
if [ -n "$a" ] && [ "$a" = "$b" ]; then echo "success-console: identical on both sides ($(printf '%s\n' "$a" | wc -l) lines)"; else echo "success-console: UNEXPECTED, the outputs differ"; bad=$((bad+1)); fi
echo "run-all: $rows rows, $bad unexpected, $cannot could not run"
[ $bad -eq 0 ] && [ $cannot -eq 0 ]
