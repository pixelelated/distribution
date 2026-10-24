#!/bin/bash
# fixture-cases.sh -- T14 S12's control for PL-23: does each lint fail fixture
# prove one guard? tools/lint-audit-artifacts over the pass fixture, the
# coupled fail fixture and the two split ones; then over each split fixture
# with a scratch copy of the lint whose guard for that fixture's violation is
# disabled (its `bad(...)` line replaced by `pass`): the fixture must then pass,
# while the other split fixture still fails. Nothing outside the scratch.
#   fixture-cases.sh <tree> <scratch>
set -u
T="$(cd "$1" && pwd)"; S="$2"; rm -rf "${S:?}"; mkdir -p "$S"
F="$T/tools/test-fixtures/lint-audit-artifacts"; L="$T/tools/lint-audit-artifacts"
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
run() { python3 -I -B "$1" "$F/fixture-epic-m6-renovation-$2" > "$S/$3.txt" 2>&1; echo $?; }
fails() { grep -cE '^\s+FAIL ' "$S/$1.txt"; }
FACE="04-analysis.md has no '## Renovation face' section"; QUESTION="carries no 'question: Q1..Q7'"
disable() {  # <copy> <message fragment>: the bad(...) line carrying it becomes pass
  python3 -I -B - "$L" "$1" "$2" <<'PY'
import sys
src, dst, frag = sys.argv[1:]
lines = open(src).read().split("\n")
hits = [i for i, l in enumerate(lines) if frag in l and "bad(" in l]
assert len(hits) == 1, hits
l = lines[hits[0]]; lines[hits[0]] = l[:len(l) - len(l.lstrip())] + "pass"
open(dst, "w").write("\n".join(lines))
PY
}
p=$(run "$L" pass pass); c=$(run "$L" fail coupled); fa=$(run "$L" fail-face face); fq=$(run "$L" fail-question question)
echo "  pass rc $p | coupled rc $c, $(fails coupled) failures | fail-face rc $fa, $(fails face) | fail-question rc $fq, $(fails question)"
check "the pass fixture passes" "$([ "$p" = 0 ] && echo 0 || echo 1)"
check "the coupled fixture's one run names both failures, so neither guard is proved alone (the positive)" "$([ "$c" = 1 ] && [ "$(fails coupled)" = 2 ] && grep -qF "$FACE" "$S/coupled.txt" && grep -qF "$QUESTION" "$S/coupled.txt" && echo 0 || echo 1)"
check "fail-face fails with exactly the face failure" "$([ "$fa" = 1 ] && [ "$(fails face)" = 1 ] && grep -qF "$FACE" "$S/face.txt" && echo 0 || echo 1)"
check "fail-question fails with exactly the question failure" "$([ "$fq" = 1 ] && [ "$(fails question)" = 1 ] && grep -qF "$QUESTION" "$S/question.txt" && echo 0 || echo 1)"
disable "$S/lint-no-face" "$FACE"; disable "$S/lint-no-question" "$QUESTION"
a=$(run "$S/lint-no-face" fail-face nf-face); b=$(run "$S/lint-no-face" fail-question nf-question)
x=$(run "$S/lint-no-question" fail-question nq-question); y=$(run "$S/lint-no-question" fail-face nq-face)
echo "  face guard off: fail-face rc $a, fail-question rc $b | question guard off: fail-question rc $x, fail-face rc $y"
check "with the face guard off, fail-face passes and fail-question still fails: fail-face depends on that guard alone" "$([ "$a" = 0 ] && [ "$b" = 1 ] && echo 0 || echo 1)"
check "with the question guard off, fail-question passes and fail-face still fails: fail-question depends on that guard alone" "$([ "$x" = 0 ] && [ "$y" = 1 ] && echo 0 || echo 1)"
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
