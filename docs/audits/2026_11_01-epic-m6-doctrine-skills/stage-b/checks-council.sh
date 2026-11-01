#!/usr/bin/env bash
# T38 stage B (#685): the checks the auditor's read of the council family names (stage-b/notes-council-family.md).
# Reads only: git at HEAD (the Facilitator's and the wrapper's sources are read, never run) and this
# repository's tracker. No council call of any kind (ruling (k)).
export LC_ALL=C; G=/usr/bin/grep; C=.claude/skills/council; R=.claude/skills/council-research
date -u +%Y-%m-%dT%H:%M:%SZ
echo "== paths the family names, present or absent at HEAD"
for p in .github/agents/trio-council.agent.md research/trio-runs research/council-runs research/council-research docs/architecture/bedrock \
  research/council-research/2026-05-24-researcher-federation-substrate .github/instructions $C/references/step-prompts/step2-peer-review.md \
  $C/references/prompt-templates/step2-template.md $R/references/phase-4-council-deliberation.md $C/references/phase-4-council-deliberation.md; do
  git cat-file -e "HEAD:$p" 2>/dev/null && echo "present $p" || echo "absent  $p"; done
git ls-tree --name-only HEAD research/council-runs/ | $G -c ''
echo "== the hooks council-research says enforce its gate"
git ls-tree --name-only HEAD .githooks/ | $G -c -E 'council'; git grep -l -E 'council-research-(provenance|digests)|summarize-council-research' HEAD -- .githooks | $G -c ''
echo "== a register row for #636 or #638 (L-37)"
git show HEAD:docs/decision-register.md | $G -c -E '#636|#638'
echo "== #1045: what it says is missing (L-48)"
gh --repo pixelelated/distribution issue view 1045 --json body --jq .body | $G -n -i -E 'procedure|refresh|pristine|missing|none' | head -n 6 | cut -c1-220
echo "== the wrapper's subcommands (tools/council/run, read from its source)"
git show HEAD:tools/council/run | $G -n -E '^\s+[a-z-]+\)' | cut -c1-90
echo "== the Facilitator's options the blocks use (scripts/council-invoke.ts, T45's file, read only)"
for o in --member --provider --prompt-file --prompt --output --max-tokens --max-retries --source-manifest --council-research-run-id --phase --invoker-agent-name; do printf '%s %s\n' "$o" "$(git show HEAD:scripts/council-invoke.ts | $G -c -F -e "\"$o\"")"; done
git show HEAD:scripts/lint-council-run.ts | $G -c -F -e '--at-step'
echo "== the references' reduced-roster sentences (reader item 1)"
git grep -n -i -E 'fall back to \(N-1\)|5, 4, or 3|3, 4, or 5|four or three' HEAD -- $R $C | cut -c1-160
echo "== council's pipeline on one-at-a-time and the vote shapes (reader items 2, 7)"
git show HEAD:$C/references/pipeline.md | $G -n -i -E 'one at a time|retired|2-1-1|5-0' | head -n 8 | cut -c1-170
git show HEAD:$C/references/voting-rules.md | $G -n -i -E '5-0|impossible' | head -n 4 | cut -c1-170
echo "== L-36: the shadow profiles and the Mistral override (scripts/lib/council-roster.ts, T45's file, read only)"
git show HEAD:scripts/lib/council-roster.ts | $G -n -i -E 'shadow|mistral|decisionAuthority|non-binding' | head -n 12 | cut -c1-170
echo "== L-33, L-42, L-43 at their lines"
git show HEAD:$R/references/provenance-schema.md | sed -n '594p' | cut -c1-200
git grep -n 'research/trio-runs' HEAD -- $C $R | cut -c1-140
git grep -n -E 'docs/architecture/bedrock' HEAD -- $C $R | cut -c1-140
echo "== L-47: the work logs' lines naming council-research"
git grep -h -c 'council-research' HEAD -- 'docs/work-logs/*/*.md' | awk '{s+=$1} END {print "work-log lines naming council-research:", s}'
git grep -l 'council-research' HEAD -- 'docs/work-logs/*/*.md' | $G -c ''
