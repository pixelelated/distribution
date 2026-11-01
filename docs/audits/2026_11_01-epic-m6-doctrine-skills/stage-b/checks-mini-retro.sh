#!/usr/bin/env bash
# T38 stage B (#685): the checks the auditor's read of mini-retro names (stage-b/notes-mini-retro.md), and two
# for code-auditor's L-02 history. Reads only: git at HEAD and this repository's tracker through gh.
export LC_ALL=C; G=/usr/bin/grep; M=.claude/skills/mini-retro
date -u +%Y-%m-%dT%H:%M:%SZ
echo "== L-02's history: when each floor rule arrived (code-auditor/SKILL.md)"
for s in 'Run it on a device, not on the host' 'An assertion that cannot fail is not evidence'; do
  echo "-- -S'$s':"; git log --format='%h %ad %s' --date=short -S"$s" HEAD -- .claude/skills/code-auditor/SKILL.md | cut -c1-120
done
git show 437ebd09af:.claude/skills/code-auditor/SKILL.md | $G -n -E 'Three hard rules|^[0-9]+\. \*\*' | awk -F: '$1<200' | cut -c1-90
echo "== the scoped audit's checks, per file"
git show HEAD:$M/references/scoped-audit.md | $G -c -E '^### Check [0-9]+ '
git show HEAD:$M/SKILL.md | sed -n '199,252p' | $G -c -E '^[0-9]+\. \*\*'
git show HEAD:$M/SKILL.md | sed -n '353,358p' | $G -c -E '^- \*\*'
git show HEAD:$M/references/template.md | $G -c -E '^- \*\*Check [0-9]+'
echo "== links and paths the read names"
for p in docs/architecture/cornerstone-conformance.md $M/reference/template.md $M/references/template.md docs/retrospective logs/audits docs/planning; do git cat-file -e "HEAD:$p" 2>/dev/null && echo "present $p" || echo "absent  $p"; done
echo "== another estate's issue numbers"
for n in 2510 2674 2302 2289 2387; do gh --repo pixelelated/distribution issue view "$n" --json number,title --jq '"#\(.number) \(.title[0:70])"' 2>&1 | head -n 1 | cut -c1-110; done
echo "== the markers ceremonies.md reads, and how many the record holds"
git ls-tree --name-only HEAD docs/retros/ | $G -c ''; git ls-tree --name-only HEAD docs/futros/ | $G -c ''
echo "== L-10's Already written: the record's mentions of the block's commands"
git grep -n -i -E 'git stash pop|npx vitest' HEAD -- docs/work-logs docs/friction-log.md docs/retros docs/futros docs/audits | cut -c1-160 | head -n 12
git grep -c -i -E 'git stash pop|npx vitest' HEAD -- docs/work-logs docs/friction-log.md docs/retros docs/futros docs/audits | $G -c ''
echo "== the futro/mini-retro continuation sections, byte for byte"
diff <(git show HEAD:.claude/skills/futro/SKILL.md | sed -n '26,35p') <(git show HEAD:$M/SKILL.md | sed -n '26,35p') && echo "futro :26-35 = mini-retro :26-35"
