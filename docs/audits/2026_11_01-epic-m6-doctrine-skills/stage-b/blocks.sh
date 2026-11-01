#!/usr/bin/env bash
# T38 stage B (#685), 02 § Command blocks: the 28 shell-tagged fenced blocks of the 52 (bash, sh, shell,
# console). The two that are reads run here with their placeholders filled; every other block's scripts are
# checked for existence at HEAD and never run (ruling (k): a provider call, a run directory, a write or a fetch).
export LC_ALL=C; G=/usr/bin/grep
date -u +%Y-%m-%dT%H:%M:%SZ
echo "== code-auditor/SKILL.md:278, run with <main-checkout> as this repository (the same objects)"
diff -q .claude/skills/code-auditor/SKILL.md <(git show next:.claude/skills/code-auditor/SKILL.md); echo "diff -q SKILL.md rc=$?"
diff -q .claude/skills/code-auditor/references/templates.md <(git show next:.claude/skills/code-auditor/references/templates.md) >/dev/null; echo "the same diff over templates.md, which the block does not read: rc=$?"
echo "== mini-retro/SKILL.md:129, run with <base-branch> and <base> as the P1 tip 2174265e9c"
git log --oneline 2174265e9c..HEAD | $G -c ''; echo "git log rc=${PIPESTATUS[0]}"
for sha in $(git log --reverse --format=%h 2174265e9c..HEAD | head -n 2); do echo "=== $sha"; git show --stat $sha | head -20 | tail -12 | $G -c ''; done
echo "== scoped-audit.md:333's layout: a <service>/src/ tree"
git ls-tree -d --name-only HEAD services 2>/dev/null | $G -c ''
echo "== the scripts the other 26 blocks call, at HEAD"
for s in scripts/verify-pins.ts scripts/council-run-start.ts scripts/council-invoke.ts scripts/write-step-seal.ts scripts/build-council-prompt.ts scripts/council-run-summary.ts scripts/lint-council-research-provenance.ts scripts/summarize-council-research-lints.ts tools/council/run; do git cat-file -e "HEAD:$s" 2>/dev/null && echo "present $s" || echo "absent  $s"; done
git show HEAD:.claude/skills/council/references/review-formats.md | sed -n '70,74p' | $G -o -E "from ['\"][^'\"]+['\"]" | head -n 2
for m in $(git show HEAD:.claude/skills/council/references/review-formats.md | sed -n '70,74p' | $G -o -E "from ['\"][^'\"]+['\"]" | sed -E "s/from ['\"]\.?\/?//; s/['\"]$//"); do git cat-file -e "HEAD:$m" 2>/dev/null && echo "present $m" || echo "absent  $m"; done
echo "== the consumer re-hash blocks (council-research/SKILL.md:302, provenance-schema.md:259): a run to hash"
git ls-tree --name-only HEAD research/council-research/ 2>/dev/null | $G -c ''
