#!/bin/bash
# #810: two synthetic epic-tier audit folders for tools/lint-audit-artifacts.
#   a  depth local, reviewers [], no tier_exception  -> the control: must FAIL
#   b  the same with tier_exception D-WORKFLOW-184 and a reason -> the case
# Each folder carries the minimum the lint reads: the five artifact files
# (04 with its five sections and a Second opinion heading, 05 with one item
# Withdrawn at its Phase 7 gate) and second-opinions/review-plan.json.
# Usage, from the repository root:
#   docs/qa-logs/2026-10-24-lint-local-epic/synthetic-810.sh   # builds .qa-scratch/810/, runs both
set -u
OUT=.qa-scratch/810
rm -rf "${OUT}"
make_folder() {
  local d="${OUT}/$1" extra="$2"
  mkdir -p "${d}/second-opinions"
  for f in 01-research-notes 02-forward-audit 03-retrospective; do
    printf '# %s\n\nSynthetic folder for #810.\n' "${f}" > "${d}/${f}.md"
  done
  printf '# 04 Analysis\n\n## Executive summary\n\n## Acceptance-criteria scorecard\n\n## Risk assessment\n\n## Coverage boundary\n\n## Quality self-check\n\n## Second opinion\n\nLocal depth: the executor alone.\n' > "${d}/04-analysis.md"
  printf '# 05 Punch list\n\n## PL-01 synthetic item\n\n## Phase 7 resolution gate\n\n| Item | Outcome |\n| --- | --- |\n| PL-01 | Withdrawn |\n' > "${d}/05-punch-list.md"
  cat > "${d}/second-opinions/review-plan.json" <<JSON
{
  "schema_version": 1,
  "depth": "local",
  "primary": {
    "harness": "Claude Code",
    "model": "anthropic/claude-opus-5.5",
    "lab": "anthropic",
    "identity_source": "session metadata"
  },
  "reviewers": []${extra}
}
JSON
}
make_folder 2026_10_24-epic-m6-synthetic-a ''
make_folder 2026_10_24-epic-m6-synthetic-b ',
  "tier_exception": "D-WORKFLOW-184",
  "reason": "plan § 6c: a doctrine read is Local"'
for x in a b; do
  tools/lint-audit-artifacts "${OUT}/2026_10_24-epic-m6-synthetic-${x}"; echo "rc=$?"
done
