# T39 Stage-E v1 bounded stranger proof

2026-11-02T18:31:34Z. Codex, harness session `01a19d11-dda5-72e3-86f9-416f36341c24`, lane `m6-p1-survey`, `wN:p3`, to coordinator `wN:p2`. This is the requested handoff proof, not an audit, council verdict, dispatch or planning decision.

Candidate: `/tmp/m6-lane-progress/t39-streams-v1.md`.
SHA256: `b0b063ce0d721017dc736e30019b95964c8f467d4838bf8d7aeab6fe2f6fa0fb` (matched on initial and final content reads).
Accepted T39: `96ef183aae39da587e5dc51d19d7c1fc9e850704`; coordinator base brief/dispositions: `b6332dbc13f5929f05ec5ba23c44285c5ee56b38`. All repository artifact reads used immutable Git objects; no other worktree content was read directly.

Two blocking factual corrections before dispatch:

1. **S6 requires an invalid proof class.** Candidate lines 287–289 require `proved: fix-tree`. The base brief at b6332dbc13 lines 1539/1582 and live #686 line 44 permit only `tree`, `history`, `tool-run`, `fixture`, `design`. Accepted `02-forward-audit.md:639–656` uses that same set, with 12 cells matched to 12 `PROOF:` lines. Correction: use the applicable existing class for each observation, record the fix commit separately, and append its corresponding `PROOF:` line. Preserve the 12 accepted pairs. The resolution linter's outcome checks do not substitute for this explicit acceptance requirement.

2. **S4 depends on a nonexistent accepted per-hit table.** Candidate lines 232–241 instruct the executor to use that table to select/classify the permitted edits. Accepted `02-forward-audit.md:310` is one aggregate L-11 row; Coverage supplies file-level rows. `04-analysis.md:208–211` explicitly describes heuristic counts. Live #1406 PL-11 likewise points to the aggregate and says “a heuristic, not a check.” The base brief at b6332dbc13:1049 supplies the heuristic and ten file counts, and requires a per-hit classification after correction; it does not supply an accepted per-hit table. Correction: reference those actual aggregates and explicitly have S4 enumerate/classify the bounded hits from the nine named immutable source files in its new before/after table, or supply the missing exact table before dispatch. Preserve the tenth file's #585 ownership and rc-accept's ledger boundary. This needs no repeat of Stage B.

Other requested checks established:

- Routing covers PL-01–46 exactly once: 46 entries, no duplicate or missing item. Named inherited owners remain outside T1's edits. The S0 table is routing, not a replacement for the Phase-7 outcomes: inspected resolution lint accepts Resolved/Deferred/Withdrawn and requires the YAML index to agree.
- Accepted population is 254 paths: 223 text, 31 binary; 68 edit-scope plus one edit-under-naming, 18 protected art-byte files, and the recorded ledger/read-only carve. All named S1–S4 editable files belong to edit-scope. Nine L-11 editable files are named; upstream README and rc-accept are explicitly excluded. S1–S5 together name 48 unique editable source paths; no source ownership expansion found.
- S5's exact lower Q5 table is 33 files / 2,770 logical lines: 32 edit-scope plus `plans/conflict-resolution/vita-style-conflict-resolution.md` (unchanged ledger-plan). It is not the older 17-file lens. D-WORKFLOW-223/-224, #686 comment 6584515739 and #1407 agree with keeping the journal in place, retaining dated/status-marked documents, and reserving archive arrangement/individual retirement for #1407.
- Runbook count is correctly **21 matched lines** (22 literal occurrences); headings are exactly 758/806/817. Recipe pin is `16dbac5211eea7e70db7394372033be2be7df829`, available in the named local ES repository. `GuiMenu.cpp:400,412,5612,5615` supplies real backup/restore labels without a fetch or pin change.
- Inspected both checker implementations and accepted receipts. Interface requires `--tree --repo --commit --since --paths --allow --out`, with optional `--withhold findings`; it rejects checkout input, requires 254 paths, retains 13 steps and exit 0/1/2 semantics. Exact line-keyed exceptions must be used; the final withholding run cannot hide findings. Accepted baseline is 13/13, rc 0; withheld findings 10/13, rc 1, with retained mutation/refusal evidence. None was rerun.
- The checker explicitly omits L-11, L-13 and L-18 from automatic lead checks; the brief's focused before/after proofs and per-document table are therefore substantive requirements. Temporary immutable candidate commits satisfy its commit argument. Original-source comparisons hold the 31 binaries and 18 art files. Common contract and S6 preserve accepted A–D receipts; no hidden historical replay, production-tool promotion, archive move, ledger edit or other-owner implementation was found. The base brief/live #686 distinguish lane proof before hand-back merge from coordinator integration checks.

Evidence commands (read-only; run from the launch repository):

```sh
sha256sum /tmp/m6-lane-progress/t39-streams-v1.md
python3 /tmp/m6-t39-stranger-proof.7X5aRR/reproduce.py
T39_TIP=96ef183aae39da587e5dc51d19d7c1fc9e850704
T39_BASE=b6332dbc13f5929f05ec5ba23c44285c5ee56b38
T39_AUDIT=docs/audits/2026_11_01-epic-m6-doctrine-reference
git show "$T39_BASE:docs/reviews/briefs/doctrine-reference.md" | sed -n '1049p;1539p;1582p'
git show "$T39_TIP:$T39_AUDIT/02-forward-audit.md" | sed -n '310p;639,656p'
git show "$T39_TIP:$T39_AUDIT/04-analysis.md" | sed -n '208,211p'
git show "$T39_TIP:$T39_AUDIT/tools/t39-checks.sh"
git show "$T39_TIP:$T39_AUDIT/tools/t39-checks.py"
git show "$T39_TIP:tools/lint-audit-artifacts" | sed -n '350,440p'
git show "$T39_TIP:$T39_AUDIT/stage-c/checks-runs.out"
git show "$T39_BASE:docs/decision-register.md" | rg '^\| D-WORKFLOW-22[34] '
git show "$T39_TIP:projects/ROCKNIX/packages/ui/emulationstation/package.mk" | sed -n '/^PKG_VERSION=/p'
git -C /home/max/Development/emulationstation-next show 16dbac5211eea7e70db7394372033be2be7df829:es-app/src/guis/GuiMenu.cpp | sed -n '400p;412p;5612p;5615p'
gh issue view 686 --repo pixelelated/distribution --json body --jq .body | rg -n 'Every proof|hand-back merge'
gh issue view 1406 --repo pixelelated/distribution --json body --jq .body | rg -n -A16 -B2 PL-11
gh api repos/pixelelated/distribution/issues/comments/6584515739 --jq .body
gh issue view 1407 --repo pixelelated/distribution --json body --jq .body
```

`counts.json` retains the reproducer's arithmetic and class mapping. Only this small private scratch directory was written. No repository/tracker/kit writes, exports, historical test execution, runtime/provider calls or permission answers. Launch worktree remains clean. Bounded assignment complete; coordinator owns corrections, final version and dispatch.
