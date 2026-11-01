#!/usr/bin/env bash
# t38-fix.sh: T38 (#685) stage E, one item: checked at its parent and at its fix, then committed
# (docs/reviews/briefs/t38-streams.md at 95052eaf78, § The rules every stream keeps). Run from the worktree root,
# with the item's edit in the working tree and nothing staged:
#
#   bash <audit>/tools/t38-fix.sh --pl PL-NN --stream SN --leads 'L-xx[, L-yy]' --subject '<subject>' \
#     --files '<path> ...' --check '<bash, run in <export>/.claude/skills>' \
#     --expect-before '<ERE>' --expect-after '<ERE>' --already '<the Already written answer>' \
#     --sentence '<words the fix changes>' --sentence-file <path> [--desc <skill>]... [--keep-allow] [--note '<line>']
#
# What it does, in order (each step's output goes into stage-e/<SN>-<PL>.txt):
#   1. exports the parent (HEAD) with `git archive`, never a checkout, unless that export exists;
#   2. restores the three allowlists to HEAD's bytes (unless --keep-allow) and re-keys their exact-line entries
#      in the files the edit changed (tools/t38-rekey.py);
#   3. stages --files and the allowlists, refuses any staged path outside the fork-adapted skills and the audit
#      folder's allowlists and checker, and exports the staged tree (`git write-tree`) the same way;
#   4. runs --check on both exports; the parent's output must match --expect-before, the fix's --expect-after
#      (each output's lines joined with ` ; `);
#   5. runs tools/t38-checks.sh on the staged tree (--commit is that tree), tools/rules-check --quiet, and the
#      wordlist over the added lines; each must exit 0;
#   6. only then commits, with the FAIL and PASS lines, the checker's TOTAL:, the rcs, the description lengths,
#      the Already written answer and the import-unchanged line in the body; checks the commit's tree is the
#      tree that was checked; writes the record; retires the parent's export.
# Exit 0 committed, 1 an expectation or a check failed (nothing committed; the index is reset), 2 cannot run.
set -u
REPO=$(git rev-parse --show-toplevel) || exit 2
AUD=docs/audits/2026_11_01-epic-m6-doctrine-skills
E=/workspace/tmp/m6-t38/e
G=/usr/bin/grep
PL= SID= LEADS= SUBJ= FILES= CHECK= EB= EA= ALREADY= SENT= SFILE= KEEP= NOTE=
DESCS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --pl) PL=$2; shift 2 ;; --stream) SID=$2; shift 2 ;; --leads) LEADS=$2; shift 2 ;;
    --subject) SUBJ=$2; shift 2 ;; --files) FILES=$2; shift 2 ;; --check) CHECK=$2; shift 2 ;;
    --expect-before) EB=$2; shift 2 ;; --expect-after) EA=$2; shift 2 ;; --already) ALREADY=$2; shift 2 ;;
    --sentence) SENT=$2; shift 2 ;; --sentence-file) SFILE=$2; shift 2 ;; --desc) DESCS+=("$2"); shift 2 ;;
    --keep-allow) KEEP=1; shift ;; --note) NOTE=$2; shift 2 ;;
    *) echo "t38-fix: refused: unknown argument $1"; exit 2 ;;
  esac
done
for v in PL SID LEADS SUBJ FILES CHECK EB EA ALREADY SENT SFILE; do
  [ -n "${!v}" ] || { echo "t38-fix: refused: --${v,,} is required"; exit 2; }
done
cd "$REPO" || exit 2
[ -z "$(git diff --cached --name-only)" ] || { echo "t38-fix: refused: something is already staged"; exit 2; }
P=$(git rev-parse --short=10 HEAD) || exit 2
REC="$AUD/stage-e/$SID-$PL.txt"
mkdir -p "$AUD/stage-e" "$E" || exit 2
ALLOWS="$AUD/tools/allow-legit.txt $AUD/tools/allow-inherited.txt $AUD/tools/allow-findings.txt"
now() { date -u +%H:%M:%S; }
xport() { # <tree-ish> <dir>
  local d=$2
  rm -rf "${d:?}"; mkdir -p "$d"
  ( set -o pipefail; git archive "$1" .claude/agents .claude/skills | tar -x -C "$d" )
}
if [ ! -d "$E/$P/.claude" ]; then
  xport HEAD "$E/$P"; rc=$?
  [ $rc -eq 0 ] || { echo "t38-fix: refused: the parent's export failed rc=$rc"; exit 2; }
  echo "$(now) made $E/$P (the parent of $PL)" >> "$AUD/stage-e/exports.log"
fi
abort() { git reset -q; echo "t38-fix: $1; nothing committed"; exit "${2:-1}"; }
# 2. the allowlists
if [ -z "$KEEP" ]; then
  for a in $ALLOWS; do git show "HEAD:$a" > "$a" || abort "cannot restore $a" 2; done
fi
REKEY=$(python3 -I "$AUD/tools/t38-rekey.py" "$E/$P" "$REPO" $ALLOWS); rc=$?
[ $rc -eq 0 ] || { echo "$REKEY"; abort "the re-key refused rc=$rc" 2; }
# 3. stage and export the staged tree
# shellcheck disable=SC2086
git add -- $FILES $ALLOWS || abort "git add failed" 2
BAD=$(git diff --cached --name-only | $G -v -E '^(\.claude/skills/(code-auditor|mini-retro|futro|begin-delivery|session-stash|session-resume|release-notes|developer-relations)/|docs/audits/2026_11_01-epic-m6-doctrine-skills/tools/(allow-(legit|inherited|findings)\.txt|t38-checks\.py)$)')
[ -z "$BAD" ] || abort "a staged path outside the lane's files: $BAD" 2
[ -n "$(git diff --cached --name-only -- .claude/skills)" ] || abort "no skill file is staged" 2
T=$(git write-tree) || abort "git write-tree failed" 2
TS=${T:0:10}
xport "$T" "$E/t-$TS" || abort "the fix's export failed" 2
# 4. the check, both sides
runcheck() { ( cd "$1/.claude/skills" && X=$1 REPO=$REPO AUD=$REPO/$AUD bash -c "$CHECK" 2>&1 ); }
B=$(runcheck "$E/$P"); BRC=$?
A=$(runcheck "$E/t-$TS"); ARC=$?
BJ=$(printf '%s' "$B" | sed ':a;N;$!ba;s/\n/ ; /g')
AJ=$(printf '%s' "$A" | sed ':a;N;$!ba;s/\n/ ; /g')
echo "before (rc=$BRC): $BJ"; echo "after (rc=$ARC): $AJ"
[[ "$BJ" =~ $EB ]] || abort "the parent's output does not match --expect-before /$EB/"
[[ "$AJ" =~ $EA ]] || abort "the fix's output does not match --expect-after /$EA/"
# 5. the checker, rules-check, the wordlist
CO=$(bash "$AUD/tools/t38-checks.sh" --tree "$E/t-$TS" --repo "$REPO" --commit "$T" --allow "$AUD/tools" --out "$E/t-$TS/out" 2>&1); CRC=$?
CSTEPS=$(printf '%s\n' "$CO" | $G -E '^(ok|FAIL|info|allowlists read|TOTAL)|^      FAIL')
CTOTAL=$(printf '%s\n' "$CO" | $G '^TOTAL:')
echo "$CSTEPS"
[ $CRC -eq 0 ] || abort "tools/t38-checks.sh exited $CRC"
tools/rules-check --quiet > /dev/null 2>&1; RRC=$?
[ $RRC -eq 0 ] || abort "tools/rules-check --quiet exited $RRC"
git diff --cached -U0 | $G -E '^\+' | $G -v -E '^\+\+\+ ' | sed 's/^+//' | tools/forbidden-terms-check --stdin > /dev/null 2>&1; WRC=$?
[ $WRC -eq 0 ] || abort "the wordlist over the added lines exited $WRC"
# the description lengths
DL=""
for d in "${DESCS[@]}"; do
  q() { python3 -I "$AUD/tools/t38-tables.py" q5 "$1" "$REPO" 2>/dev/null | awk -F'|' -v k="\`$d\`" '{gsub(/ /,"",$2)} $2==k {gsub(/ /,"",$5); print $5}'; }
  w() { sed -n '3p' "$1/.claude/skills/$d/SKILL.md" | wc -c; }
  DL="${DL}Description, $d/SKILL.md:3: $(q "$E/$P") -> $(q "$E/t-$TS") characters of the scalar (tools/t38-tables.py q5); $(w "$E/$P") -> $(w "$E/t-$TS") bytes of the line (sed -n 3p | wc -c)
"
done
# import-unchanged, read at the parent
IL=$(git log --format=%h -S"$SENT" HEAD -- "$SFILE" | paste -sd' ')
if [ "$IL" = "437ebd09af" ]; then IU="yes"; else IU="no"; fi
IMPORT="import-unchanged: $IU (git log -S over $SFILE at $P prints: ${IL:-nothing})"
# 6. commit
MSG=$(mktemp -p "$E" msg.XXXXXX)
{
  printf '%s\n\n' "$SUBJ"
  printf '%s (%s), stream %s of docs/reviews/briefs/t38-streams.md at 95052eaf78.\n\n' "$PL" "$LEADS" "$SID"
  printf 'Check (run in each export'"'"'s .claude/skills): %s\n' "$CHECK"
  printf 'FAIL at the parent %s: %s\n' "$P" "$BJ"
  printf 'PASS at the fix: %s\n' "$AJ"
  printf 'tools/t38-checks.sh exit 0: %s\n' "$CTOTAL"
  printf 'tools/rules-check --quiet rc=0\n'
  [ -n "$DL" ] && printf '%s' "$DL"
  [ -n "$NOTE" ] && printf '%s\n' "$NOTE"
  printf 'Already written: %s\n' "$ALREADY"
  printf '%s\n' "$IMPORT"
  printf '\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
} > "$MSG"
git commit -q -F "$MSG"; rc=$?
rm -f "$MSG"
[ $rc -eq 0 ] || abort "git commit exited $rc"
C=$(git rev-parse --short=10 HEAD)
[ "$(git rev-parse HEAD^{tree})" = "$T" ] || { echo "t38-fix: STOP: the commit's tree is not the tree that was checked"; exit 1; }
mv "$E/t-$TS" "$E/$C" && echo "$(now) made $E/$C (the fix of $PL, from tree $TS)" >> "$AUD/stage-e/exports.log"
{
  echo "# $PL ($LEADS), $SID: $SUBJ"
  echo "parent: $P (export $E/$P); fix: $C (tree $TS, export $E/$C)"
  echo "check, run in each export's .claude/skills: $CHECK"
  echo "FAIL at the parent (rc=$BRC): $BJ"
  echo "PASS at the fix (rc=$ARC): $AJ"
  echo "allowlists re-keyed: $(printf '%s' "$REKEY" | paste -sd';')"
  echo "tools/t38-checks.sh exit $CRC at the fix (--commit $TS):"
  printf '%s\n' "$CSTEPS"
  echo "tools/rules-check --quiet rc=$RRC"
  echo "the wordlist over the added lines rc=$WRC"
  [ -n "$DL" ] && printf '%s' "$DL"
  [ -n "$NOTE" ] && echo "$NOTE"
  echo "Already written: $ALREADY"
  echo "$IMPORT"
  echo "time to play: untouched -- the 52 load in an agent's session, never on an image"
  echo "git show --stat --format= $C:"
  git show --stat --format= "$C"
} > "$REC"
rm -rf "${E:?}/$P" && echo "$(now) retired $E/$P" >> "$AUD/stage-e/exports.log"
echo "t38-fix: $PL committed as $C; $CTOTAL; record $REC"
