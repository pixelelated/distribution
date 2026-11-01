#!/usr/bin/env bash
# T38 (#685): each table generator seen to exit 1 on a constructed drift, on its own scratch copy of the export
# (never a checkout), and 0 on the export itself, before its table is trusted (brief § 6, the Tools row).
#   bash t38-tables-drift.sh <export> <repo> <tools-dir> <scratch>
E=${1:?export}; R=${2:?repo}; T=${3:?tools}; S=${4:?scratch}; G=/usr/bin/grep
case "$S" in /workspace/tmp/m6-t38/*) ;; *) echo "refused: scratch must be under /workspace/tmp/m6-t38/"; exit 2;; esac
mkdir -p "$S"
run() { python3 -I "$T/t38-tables.py" "$@" > /dev/null 2> "$S/last.err"; }
mk() { rm -rf "${S:?}/$1"; mkdir -p "$S/$1"; cp -a "$E/.claude" "$S/$1/"; }
check() { local name=$1 want=$2; shift 2; run "$@"; local rc=$?
  printf '%-36s rc=%s (want %s) %s\n' "$name" "$rc" "$want" "$($G -m1 '^FAIL' "$S/last.err" | cut -c1-110)"; }
check "coverage, the export" 0 coverage "$E" "$T/coverage-answers.tsv"
mk cov; rm "$S/cov/.claude/skills/futro/references/template.md"
check "coverage, one file removed" 1 coverage "$S/cov" "$T/coverage-answers.tsv"
check "q4, the export" 0 q4 "$E" "$R"
mk q4; printf ' ' >> "$S/q4/.claude/agents/council-member-gpt.agent.md"
check "q4, one byte on an agent" 1 q4 "$S/q4" "$R"
check "q5, the export" 0 q5 "$E" "$R"
mk q5; sed -i '/^description:/d' "$S/q5/.claude/skills/session-resume/SKILL.md"
check "q5, a description removed" 1 q5 "$S/q5" "$R"
check "q6, the export" 0 q6 "$E" "$R"
mk q6; mv "$S/q6/.claude/skills/release-notes" "$S/q6/.claude/skills/release-notes-x"
check "q6, a skill renamed" 1 q6 "$S/q6" "$R"
check "q7, the export" 0 q7 "$E"
mk q7; sed -i 's/^## pixelelated continuation$/## pixelelated, continued/' "$S/q7/.claude/skills/futro/SKILL.md"
check "q7, a shared section renamed" 1 q7 "$S/q7"
