# Reviews: the codebase renovation program (M6)

The whole codebase, reviewed and brought up to date in slices, progressively,
beside feature work (D-WORKFLOW-083, D-WORKFLOW-102, D-WORKFLOW-181). The
milestone is M6; the epic is #339; the plan for the plan is #346.

| File | What it is | Written by |
| --- | --- | --- |
| `plan-for-the-plan.md` | how the program is planned: the survey, the slicing, the ordering lenses, the per-slice procedure, the brief an executor receives, the drift rules, the ledgers | P0 (#346) |
| `order.md` | the slices in order, each with its lens, paths, line count, the release it gates, its depth and the evidence that closes it (#346's first criterion) | P1 |
| `inventory.json`, `inventory.md` | every path's root, provenance tier, language, lines, patches, last fork and upstream commits, reachability; the per-area totals | `tools/renovation-inventory` (P1), re-run at every slice close |
| `status.md` | one row per slice: area, lines, depth, state, reviewed-at, drift since | `tools/renovation-status` (P1) |
| `briefs/<slice>.md` | the brief an executing session runs a slice from, ten sections, committed before dispatch | the planner |

The audits themselves live under `docs/audits/<date>-epic-m6-<slice>/`, the
retros under `docs/retros/`, and the decisions in `docs/decision-register.md`.
