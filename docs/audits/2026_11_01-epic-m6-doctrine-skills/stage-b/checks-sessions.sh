#!/usr/bin/env bash
# T38 stage B (#685): the checks the auditor's read of session-resume and session-stash names
# (stage-b/notes-sessions.md). Reads only: git at HEAD and next, and this repository's tracker.
export LC_ALL=C; G=/usr/bin/grep
date -u +%Y-%m-%dT%H:%M:%SZ
echo "== tracked session files"
git ls-tree --name-only HEAD .github/sessions/ | $G -c -E 'saved-session-state-'; git ls-tree --name-only HEAD .github/sessions/ | $G -c 'saved-session-state-main'
git ls-tree --name-only HEAD .github/sessions/archived/ | $G -c ''
echo "== does any tool or hook refuse an overwrite without the archive (L-18)"
git grep -l -E 'saved-session-state|sessions/archived' HEAD -- tools .githooks | $G -c ''
echo "== the canonical stash on next: its first headings"
git show next:.github/sessions/saved-session-state-next.md | $G -n -E '^#{1,2} ' | head -n 6 | cut -c1-90
echo "== the stranger's proof sentence, and when it came"
git show HEAD:.claude/skills/session-stash/SKILL.md | $G -n -o 'prove it by giving an agent with no context[^;.]*'
git log --format='%h %ad %s' --date=short -S'prove it by giving an agent with no context' HEAD -- .claude/skills/session-stash/SKILL.md | cut -c1-120
echo "== how the lane pointers are framed: #1014 and the register"
gh --repo pixelelated/distribution issue view 1014 --json number,state,title --jq '"#\(.number) \(.state) \(.title[0:100])"'
git grep -n -E 'D-WORKFLOW-[0-9]+ \|' HEAD -- docs/decision-register.md | $G -i -E 'pointer' | cut -c1-200 | head -n 4
git show HEAD:.github/sessions/saved-session-state-feature-m6-doctrine-skills-685.md | $G -n -o 'updates this file \*\*at every checkpoint\*\* (#1014)'
