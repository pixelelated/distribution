#!/usr/bin/env bash
# T38 stage B (#685): the checks the auditor's read of code-auditor names (stage-b/notes-code-auditor.md).
# Reads only: git at HEAD (the dispatch tip's bytes for the 52), this repository's tracker through gh.
# Never runs tools/council/run (ruling (k)): its options are read from its source.
export LC_ALL=C; G=/usr/bin/grep; C=.claude/skills/code-auditor
date -u +%Y-%m-%dT%H:%M:%SZ
echo "== intent, by git log -S (oldest last)"
for s in 'Three hard rules' 'Subagent output is a LEAD, never EVIDENCE' 'Twelve recorded' 'randomly-chosen' 'Trust them; do not re-derive' 'scaffold has none today' 'tier_exception' 'subagents do not inherit terminal access' 'agent-terminal-safety'; do
  echo "-- -S'$s':"; git log --format='%h %ad %s' --date=short -S"$s" HEAD -- "$C" | cut -c1-140
done
echo "== where each string sits now"
git grep -n -E 'Evidence floor rule 3|rule 3\)' HEAD -- "$C" | cut -c1-120
git grep -c -E 'pre-issue|--phase' HEAD -- "$C"; echo "pre-issue/--phase in code-auditor: grep rc=$? (1 = none)"
git grep -n -i -E 'local' HEAD -- "$C/SKILL.md" "$C/references/phases.md" "$C/references/review-levels.md" | cut -c1-150
echo "== agent-terminal-safety anywhere in the tree"
git ls-tree -r --name-only HEAD | $G -i -c 'agent-terminal-safety'; git grep -l -i 'agent-terminal-safety' HEAD | cut -c1-100
echo "== the duration the widened pattern misses"
git grep -n -E '<[0-9]+ ?min' HEAD -- .claude/skills | cut -c1-120
echo "== the blindspot register's numbered entries at HEAD"
git show HEAD:docs/blindspot-register.md | $G -c -E '^## [0-9]+\.'; git show HEAD:docs/blindspot-register.md | $G -o -E '^## [0-9]+\.' | tail -n 1
echo "== another estate's issue numbers, on this tracker"
for n in 2299 2634 2382 2952 3059; do gh --repo pixelelated/distribution issue view "$n" --json number,title,state --jq '"#\(.number) \(.state) \(.title[0:80])"' 2>&1 | head -n 1; done
gh --repo pixelelated/distribution issue list --state all --limit 1 --json number --jq '"highest issue number: \(.[0].number)"'
echo "== #810 and #375"
gh --repo pixelelated/distribution issue view 810 --json state,body --jq '.state, (.body | split("\n")[] | select(test("SKILL|phases|review-levels|templates|skill")))' | cut -c1-220
gh --repo pixelelated/distribution issue view 375 --json number,state,title --jq '"#\(.number) \(.state) \(.title[0:90])"'
echo "== tools/council/run: present, and its invoke options read from its source (never run)"
git cat-file -e HEAD:tools/council/run && echo "tools/council/run present"
git show HEAD:tools/council/run | $G -n -E -e '--member|--provider|--prompt-file|--output|invoke' | head -n 12 | cut -c1-140
