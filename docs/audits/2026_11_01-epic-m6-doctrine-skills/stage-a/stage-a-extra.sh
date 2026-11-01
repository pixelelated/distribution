#!/usr/bin/env bash
# T38 stage A (#685): the reads the brief leaves to the lane, run from the lane's worktree after
# the runs block. The removal check with the lane's-tip placeholder filled (87c2ab0fed, the dispatch tip); each ID
# the 52 cite looked up in the decided and the open table of the register at the coordinator's tip (3a9b0aec81);
# the highest decided row per area there (the pointer's Register: line); the register's row count
# at the proof's hash, the coordinator's tip and HEAD; and the rules this session loaded at its
# start (the T5 worktree's HEAD 52e6794ba7) against the coordinator's tip.
#   bash stage-a-extra.sh > stage-a-extra.out 2>&1
export LC_ALL=C; G=/usr/bin/grep; X=':(exclude).claude/rules/'
H=$(cd "$(dirname "$0")" && pwd); T=/workspace/tmp/m6-t38; mkdir -p "$T/tmp"
CO=3a9b0aec81
date -u +%H:%M:%S
bash "$H/removal.sh"
echo "removal check: the lines above are its output (none expected); its rc is tail's"
git show "$CO:docs/decision-register.md" > "$T/tmp/register-co.md"
o=$($G -n '^## Open decisions' "$T/tmp/register-co.md" | cut -d: -f1)
echo "open decisions heading at :$o"
for id in $(git grep -h -o -E 'D-[A-Z]+-[0-9]+' HEAD -- .claude/ "$X" | sort -u); do
  printf '%s dec:%s open:%s\n' "$id" "$(head -n $((o-1)) "$T/tmp/register-co.md" | $G -c -F "| $id |")" "$(tail -n +"$o" "$T/tmp/register-co.md" | $G -c -F "| $id |")"
done
echo "-- highest decided per area above :$o at $CO:"
head -n $((o-1)) "$T/tmp/register-co.md" | $G -o -E '^\| D-[A-Z]+-[0-9]+ \|' | sed -E 's/^\| (D-[A-Z]+)-([0-9]+) \|/\1 \2/' | sort -k1,1 -k2,2n | awk '{m[$1]=$2} END {for (a in m) print a"-"m[a]}' | sort | tr '\n' ' '; echo
for h in 2f42ff5ddf "$CO" HEAD; do printf 'register rows at %s: %s\n' "$h" "$(git show "$h:docs/decision-register.md" | $G -c -E '^\| D-[A-Z]+-[0-9]+ \|')"; done
git diff "$CO" HEAD -- docs/decision-register.md | $G -E '^[+-]\| D-' | cut -c1-40
echo "-- the three moved files, lines at the P1 tip, at next and at HEAD (grep -c ''):"
for p in .claude/skills/code-auditor/references/templates.md .claude/skills/council/IMPORTED-FROM.md .claude/skills/mini-retro/references/scoped-audit.md; do
  printf '%s %s %s %s\n' "$p" "$(git show "2174265e9c:$p" | $G -c '')" "$(git show "8ebaf8daad:$p" | $G -c '')" "$(git show "HEAD:$p" | $G -c '')"
done
echo "-- the rules this session loaded (52e6794ba7) against the coordinator's tip:"
git diff --stat 52e6794ba7 "$CO" -- .claude/rules CLAUDE.md AGENTS.md
echo "-- this lane's ref:"
git for-each-ref --format='%(refname:short) %(objectname:short=10)' 'refs/heads/feature/m6-doctrine-skills-685' 'refs/remotes/origin/feature/m6-doctrine-skills-685'
