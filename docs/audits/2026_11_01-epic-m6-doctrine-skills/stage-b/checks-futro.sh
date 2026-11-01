#!/usr/bin/env bash
# T38 stage B (#685): the checks the auditor's read of futro names (stage-b/notes-futro.md).
# Reads only: git at HEAD, gh's local configuration, and this repository's tracker. No fetch.
export LC_ALL=C; G=/usr/bin/grep; F=.claude/skills/futro
date -u +%Y-%m-%dT%H:%M:%SZ
echo "== L-13: which repository gh fills {owner}/{repo} with here"
gh repo set-default --view 2>&1 | head -n 2; echo "set-default --view rc=$?"
git remote -v | awk '{print $1, $2}' | sort -u | sed -E 's#(https?://)[^@/]*@#\1#'
echo "== the base-divergence MUST: is there a main to compare with?"
git rev-parse --verify --quiet origin/main >/dev/null; echo "origin/main rc=$?"; git rev-parse --verify --quiet refs/heads/main >/dev/null; echo "main rc=$?"
git symbolic-ref --quiet refs/remotes/origin/HEAD 2>&1 | head -n 1
echo "== 'Apply four techniques' and its fifth bullet, by git log -S"
for s in 'Apply four techniques' 'Replaced-mechanism archetype' 'Honesty check on the simulation'; do echo "-- -S'$s':"; git log --format='%h %ad %s' --date=short -S"$s" HEAD -- "$F/SKILL.md" | cut -c1-120; done
echo "== the register sections SKILL.md cites, in the project's register and the starter"
for t in 'required\[\]`?-enumeration' 'Substrate-precondition assumption'; do printf '%s: register %s, starter %s\n' "$t" "$(git show HEAD:docs/blindspot-register.md | $G -c -E "$t")" "$(git show HEAD:$F/references/blindspot-register.md | $G -c -E "$t")"; done
echo "== the low issue numbers techniques.md and template.md cite, on this tracker"
for n in 1556 1558 2373 2545 2647 2648 203; do gh --repo pixelelated/distribution issue view "$n" --json number,title,state --jq '"#\(.number) \(.state) \(.title[0:80])"' 2>&1 | head -n 1 | cut -c1-120; done
echo "== how the 17 futros' headings run (question 1's level)"
for f in $(git ls-tree --name-only HEAD docs/futros/ | head -n 17); do printf '%s %s\n' "$(git show HEAD:$f | $G -m1 -o -E '^#+ (1\.|Q1|1 )' )" "${f##*/}"; done | sort | uniq -c | sort -rn | head -n 6
