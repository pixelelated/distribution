# Questions for the maintainer — T41 Stage D (#688)

Prepared for the coordinator; recorded 2026-11-02 18:50:01 UTC. Codex / GPT-6-Astra / xhigh, T3 wN:p6, session `01a19d12-29e3-7fe0-9f41-038dac0a5deb`; observed live footer, not provider-attested. The coordinator owns decisions and any stream brief; this lane makes no policy/source change.

## Question 1

Posted and read back exactly: [6585346506](https://github.com/pixelelated/distribution/issues/688#issuecomment-6585346506). Submitted body: `stage-d/issues/question-1.md`; full GitHub API payload: `stage-d/question-1-readback.json`.

**T41 Stage D — question 1 for the coordinator to route (L-03): the three 7.0 copies that equal 7.2's — keep two files, or one file and a symlink, as upstream's 7.2.6 does?**

The accepted evidence records three byte-identical kernel pairs: `0010-msm-resource-cleanup.patch`, `9998-silence-initramfs-unpack-warn.patch`, and `9999-fix-rust-build-error.patch`. A fix made to only one independent copy leaves the other behind; upstream's `9416eec2c2` fixed both 0010 copies by hand. A shared target would make the test-image series follow the shipped-kernel copy, while keeping separate files allows series-specific changes and needs an explicit equality guard while they are intended to match.

[Accepted duplicate receipts](https://github.com/pixelelated/distribution/blob/94b5b1c0b983313325dba101217761c6e5c9bca0/docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/stage-b/corrected/remaining-reads.json), [question and ownership](https://github.com/pixelelated/distribution/blob/94b5b1c0b983313325dba101217761c6e5c9bca0/docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/04-analysis.md#stage-d-questions-drafts-not-posted-early). Stage-D record archaeology found no decided duplicate-storage policy. This is T11's recipe-tree decision after the base merge; T41 has made no source or symlink edit. The actual pointer defect is separately tracked as bug #1408 and audit #1409 PL-001; either storage choice still requires the upstream fix.

Please record the selected disposition and owner in the coordinator's stream disposition, with a decision-register row if required. This is the brief's prepared policy question, not a request for device/runtime permission. The lane stops at the Stage-D checkpoint and does not start a remediation stream.

Codex / GPT-6-Astra / xhigh, session `01a19d12-29e3-7fe0-9f41-038dac0a5deb`, T3 wN:p6; observed footer, not provider-attested.

## Question 2

Posted and read back exactly: [6585347732](https://github.com/pixelelated/distribution/issues/688#issuecomment-6585347732). Submitted body: `stage-d/issues/question-2.md`; full GitHub API payload: `stage-d/question-2-readback.json`.

**T41 Stage D — question 2 for the coordinator to route (L-16): the ramoops patch's contribution layer — ROCKNIX's distribution, or a mainline sun50i-h616.dtsi change?**

The existing answer is constrained by **D-SYS-004**, which says the SoC-level reservation is not something mainline would take and the fork carries it. Record archaeology and the full row were read before this question. The prepared #585 line therefore currently targets **ROCKNIX's distribution layer**, keeping that settled policy; this does not call the policy undecided. Please confirm that queue target in the Stage-D disposition, or explicitly record any requested policy reversal before a different layer is pursued.

The accepted 38-line H700 `0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch` reserves `0x4f000000` / `0x100000`, with `0x80000` console and `0x20000` record size, plus six H700 configuration companions. Pristine pinned 7.2 has no corresponding ramoops node; upstream distribution `651150fc88` has no ramoops-named patch. [Source/context evidence](https://github.com/pixelelated/distribution/blob/94b5b1c0b983313325dba101217761c6e5c9bca0/docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/02-forward-audit.md#the-ramoops-patch), [the never-sent queue line](https://github.com/pixelelated/distribution/blob/94b5b1c0b983313325dba101217761c6e5c9bca0/docs/audits/2026_11_02-epic-m6-patches-shipped-kernel/02-forward-audit.md#the-585-lines-owed). Physical DRAM retention is not re-tested here; #369 remains the parked context read in Stage B.

Nothing has been sent to #585 or upstream. D-WORKFLOW-164/165 remain in force; a contribution-layer disposition is not submission authorization. No DTS/config/source, host, device or cloud action is made by this question. The coordinator owns the answer and any later stream; T41 stops at the Stage-D checkpoint.

Codex / GPT-6-Astra / xhigh, session `01a19d12-29e3-7fe0-9f41-038dac0a5deb`, T3 wN:p6; observed footer, not provider-attested.

## Historical D status

Both prescribed questions are posted. D-SYS-004 remains the existing ramoops policy, D-WORKFLOW-164/165 still prohibit inferring submission authority, and no duplicate-file policy was selected. Awaiting the coordinator's stream disposition; no Stage E action.

## E disposition — 2026-11-02 19:20:06 UTC

Authority: [comment 6585897242](https://github.com/pixelelated/distribution/issues/688#issuecomment-6585897242), D-WORKFLOW-227 at 82cb787674b6132669efa6bd7d38168797e7c1f7.

- PL-001: Deferred to open High bug #1408, owner base integration #563/#559, by https://github.com/pixelelated/distribution/issues/688#issuecomment-6585897242. Upstream 9416eec2c200ad969d9e421e686fc7cbfdaca36a corrects both copies; D-WORKFLOW-209 prohibits a product edit here. The bug is unfixed and not waived; both source-fix criteria remain unchecked. Integration chooses and records its exact intake and evidence under its own scope.
- Question 1 (6585346506): leave the three equal pairs unchanged in T41. The future choice between two files and one file plus symlink remains T11/#658's at the next integration review, with #1408/#563 as the concrete handoff. Prefer the selected upstream layout unless the series require divergent content; any departure needs a carrying reason and equality/divergence guard. This is no global storage-policy selection.
- Question 2 (6585347732): D-SYS-004 confirms ROCKNIX's distribution layer for the ramoops draft. No reversal, mainline submission or new physical-retention claim. Both #585 contribution lines remain drafts, never sent.

All 31 lead owners remain in 02, including firmware T11 and separate T42/T43 populations. No source edit, runtime, external review, permission answer or other-owner change. Continue E–H without another stage relay. D226 preserves accepted executions; only new final records and gates are checked. The coordinator alone performs final simulated integration, acceptance and audit closure.
