#!/usr/bin/env bash
# T38 (#685) stage D: the reads behind the five bugs' Already written lines. Read-only; run from the worktree root.
G=/usr/bin/grep; export LC_ALL=C
echo "== L-52: does the lint write anything? (open for write, write_text, os.replace, mkdir)"
$G -n -E "open\([^)]*['\"][wa]['\"]|write_text|write_bytes|os\.replace|\.mkdir\(" tools/lint-audit-artifacts; echo "grep rc=$? (1 = none)"
echo "== L-52: the lint's phases"
$G -n -E 'add_argument\("--(phase|issue)"' tools/lint-audit-artifacts
echo "== L-52: audit folders whose running log records a pre-issue run, and folders with a completion marker"
n=0; for d in docs/audits/*/; do [ -f "$d/00-running-log.md" ] && $G -q -- '--phase pre-issue' "$d/00-running-log.md" && n=$((n+1)); done; echo "pre-issue recorded: $n"
ls docs/audits/*/audit-completion.json 2>/dev/null | $G -c .
echo "== L-13: gh's default here"
gh repo set-default --view 2>&1 | head -n 1
echo "== L-13: futros and work logs citing another repository's issue comments"
$G -rln -E 'github\.com/ROCKNIX/distribution/issues|repos/ROCKNIX/distribution/issues' docs/futros docs/retros docs/work-logs 2>/dev/null | $G -c .
echo "== L-13: the gh calls in the six imported skills that name no repository"
$G -rn -F '{owner}/{repo}' .claude/skills | cut -c1-120
echo "== L-11: the releases on the fork (newest five)"
gh release list --repo pixelelated/distribution --limit 5 2>&1 | cut -c1-100
echo "== L-11: the tool's own words"
$G -n -i -E 'no upload|never publishes|--prepare' tools/fork-publish-release | head -n 5
echo "== L-56: review plans with tier_exception, in this tree"
for f in docs/audits/*/second-opinions/review-plan.json; do $G -l '"tier_exception"' "$f"; done 2>/dev/null
echo "== L-56: 4.6 recorded not applicable in those folders' 04"
for f in docs/audits/*/second-opinions/review-plan.json; do $G -q '"tier_exception"' "$f" || continue; d=${f%/second-opinions/review-plan.json}; printf '%s %s\n' "$d" "$($G -c -i -E '4\.6.*not applicable|not applicable at local' "$d/04-analysis.md" 2>/dev/null)"; done
echo "== L-10: records naming the block run (work logs, friction log, retros, futros, audits other than T38's)"
$G -rln -E 'git stash pop|npx vitest' docs/work-logs docs/friction-log.md docs/retros docs/futros docs/audits 2>/dev/null | $G -v 2026_11_01-epic-m6-doctrine-skills | $G -c .
echo "== L-56: Local epic-tier plans on this repository's local refs (no fetch), each folder's 04 on 4.6"
for r in $(git for-each-ref --format='%(refname:short)' refs/heads refs/remotes/origin | $G -E 'm6-|next$'); do
  git grep -l '"tier_exception"' "$r" -- 'docs/audits/*/second-opinions/review-plan.json' 2>/dev/null
done | sort -t: -k2 -u | while IFS=: read -r ref f; do
  d=${f%/second-opinions/review-plan.json}
  printf '%s @%s 4.6-not-applicable-lines=%s pending-lines=%s\n' "$d" "$ref" \
    "$(git show "$ref:$d/04-analysis.md" 2>/dev/null | $G -c -i -E '4\.6.*(not applicable|n/a)|not applicable at local|(local|no) .*second opinion')" \
    "$(git show "$ref:$d/04-analysis.md" 2>/dev/null | $G -c -i -E '4\.6.*pending|phase 4\.6 .*blocked')"
done
