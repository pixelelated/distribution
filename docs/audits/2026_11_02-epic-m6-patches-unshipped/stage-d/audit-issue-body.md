Stage-D audit of T43 #690 under area #1054 / M6, explicitly dispatched in comment6589165585. Actual primary: Codex / GPT-6-Astra / xhigh (OpenAI), T1 wN:p4, session01a19d12-0c07-7ba3-88b8-ab9d609f4d67; Local reviewers[]. Source afdec2bf8b88135befcb7ec56efb3a7ea327bd73, seed601e4694f9726b2228d3571efdb5cfc061c6d442. Audit root: docs/audits/2026_11_02-epic-m6-patches-unshipped/.

## Executive summary

432 native paths /328,516 logical lines;31 recipe contexts and114 source plans.779 complete normal source applications including context returned0,600 native calls over333 paths. Native results:330 clean,199 offset,71 fuzz;40 native paths include fuzz.75 plans qualify,38 remain open,one is configuration-only.93 native paths have at least one open input (87 wholly open,6 mixed).12 config rows are source inputs only. Fixed upstream:334 identical,39 changed,59 absent; all432 match fork base.

Both432-key tables and all four exact-input negative controls pass. The actual partial-failure runner preserves the prefix and blocks successors. Pre-issue lint prints `PASS pre-issue artifacts (does not certify resolution)`. There is one Low source-evidence gap, zero new reactive bugs. Existing High #1408 and Medium #1410 retain their own fix boundaries; normal application is not correctness. Both time-to-play quantities remain unmeasured and untouched.

## Acceptance-criteria scorecard

At the D boundary:15 PASS,3 PARTIAL,2 SKIP of the20 slice criteria. Partial:AC13 final Phase7 resolution;AC17 projection retirement/closing census;AC18 final post-disposition checks. Skipped until dispatch:AC19 G/H retro/final handback;AC20 final root acceptance/integration. The precise per-criterion evidence is in04-analysis.md. No final completion or acceptance is claimed.

## Acceptance criteria

- [ ] PL-001: an outcome matrix contains exactly the93 native open-input keys, retains each missing plan input, existing source owner, next mechanism and receipt, and preserves positive/open results for the six mixed rows; the coordinator-dispatched outcome agrees between this issue, the YAML index and Phase7 table, with named evidence or follow-up.

# Punch list — T43 patches-unshipped

Generated from the actual source/receipt census. **1 finding:0 Critical,0 High,0 Medium,1 Low.** Zero new reactive bugs. Stage D only; Phase7 remains open until coordinator disposition. Source audit:04-analysis.md. Tracker is added after pre-issue lint.

## PL-001 — Give the93 native source-input gaps explicit outcome custody

- **Question:** Q3, with Q4/Q6 context.
- **Severity:** Low.
- **Category:** Test Gap (source-evidence qualification, not a product-failure verdict).
- **Source finding:** stage-b/open-inputs.json and table-summary.json; AC-09's explicit qualifications.
- **Owner area:** T43 record custody #690; actual source owners remain T25 #672, T8 #655, T30 #677, T23 #670 and T11 #658 as each row names.
- **Where:**93 exact native keys in stage-b/open-inputs.json;38 package/consumer plans in application receipts;87 wholly open paths and6 mixed shared paths.
- **What:** After coordinator disposition, carry every missing archive/checksum/custom-hook preimage into a named outcome and next mechanism. Keep positive evidence attached to its own consumer; do not turn a mixed row into blanket success. The disposition may retain an explicitly deferred qualified row with its existing owner; this item requests no fetch, source fix or runtime action.
- **Why:** A provenance table can otherwise lose the source-input limit when summarized as “patches apply.”
- **Evidence:** stage-b/plans.json supplies exact recipe pin/URL/SHA and selector; each group receipt supplies inspected candidate hashes and concrete absent/preimage limits.20 initially held overlay plans were resolved by new bounded input qualification; remaining gaps are specific. Table negatives protect native keys and identity.
- **Ladder:** source table → exact recipe/consumer → missing archive or transformation preimage → permitted future owner qualification → normal source application only after inputs bind. Runtime correctness remains a separate later proof.
- **Next mechanism:** coordinator Stage-E stream disposition and a machine-readable owner/outcome matrix reusing these immutable receipts; no A–D replay.
- **Already written:** immutable patches/configs/recipes and cached source inputs pre-exist. This audit changes no installed state, source, cache or cloud data. A later source uptake remains a separate owner's change.
- **Can this be done on the VM?** This gap concerns immutable source inputs, not runtime behavior; a guest cannot supply missing archive provenance. No guest or runtime allocation is requested.
- **Acceptance:** An outcome matrix has exactly the93 open native keys and retains each plan-specific missing input, existing source owner, next mechanism and receipt; mixed6 rows retain both positive and open results. The audit issue and YAML/Phase7 table agree on the coordinator-dispatched outcome, with named evidence or follow-up. No product fix or applicability claim is invented.

## Pre-existing tracked scope — exempt from this Phase7 gate

- #1408: High MSM cleanup uninitialized-pointer defect; existing #563/#559 integration. The source copies match T41; successful application is not correctness.
- #1410: T42 PPSSPP nested-patch defect; standalone owner #677. T43 does not duplicate it.
- #1101: inventory unpack edges; #1048/#346: class-removal decision; #585: contribution queue remains unsent.
- T25/T11/T27/T41/T42 accepted source/pin/configuration contexts remain attributed to their immutable records. Fixed-upstream uptake stays #563/#559.

## Machine-readable index

```yaml
punch_index:
- id: PL-001
  severity: Low
  category: Test Gap
  source_finding: T43-source-inputs
  question: Q3
  owner_area: T43 record custody with existing source owners
  where: stage-b/open-inputs.json
  acceptance: "Exactly93 native keys retain per-plan evidence limits, owners and next mechanisms; mixed6 rows preserve both results; tracker/index/table agree."
  outcome: open
```

## Phase 7 resolution gate

| Item | Outcome | Evidence / next action |
| --- | --- | --- |
| PL-001 | Open | Await coordinator Stage-E stream disposition; stage-b/open-inputs.json and exact group receipts retained |

## Delivery boundary

A–D only. Pause at clean published D for coordinator stream disposition. No source, recipe, config, rule, register or ledger changes; no runtime/build/provider/physical/cloud action or other-agent permission answer. Audit closure and completion marker require explicit root acceptance. The source projections are retained under receipt-bound T43 scratch roots for later authorized H retirement; shared caches remain read only.
