# T39 final acceptance contract — 2026-11-02

D-WORKFLOW-229, coordinator disposition before final acceptance. This refines
D-WORKFLOW-220 and the base brief § 5/§ 7/§ 10 against the exact Stage-H
integration already required by the stream brief. No source ownership expands.

Pins: reviewed B=`86ebb6dffce7bec2dda6296bd84dd225a28b1347`;
authorized coordinator K=`329011b9eae20922b4d0727e13bf1626b2e1c04f`;
integration M=`24a5e0e294607bc6fc99025873cb063d26c9a4da`;
hand-back T=`4eb5dfab8e745914a55e7de3e5a43c5b91ebc608`.

The original predicates remain recorded as false: criterion 5's unfiltered
history has 46 commits (16 lane, 30 imported); its protected diff has six
coordinator briefs and 3,056 inserted lines. Criterion 12 prints ten imported
coordinator commits. Criterion 24's unqualified mention count is two, although
both retained census entries identify the coordinator as author. No old
command is relabelled PASS. The bounded support report and raw results are
retained in `t39-final-support/` beside this document.

The replacement predicates for live #686 and base-brief criteria 5/12/24 are:

1. **5 — exact integration provenance.** Header pins remain B/T, no ES pair.
   M has exactly the lane's G tip and K as parents; K is an ancestor of T.
   `git log --no-merges B..T --not K` contains only the 16 lane commits, whose
   changed paths remain within the dispatched source/audit/record scope.
   Every non-owned final mode/blob equals K; the 48 changed owned sources
   equal the final S5 source commit through M and T. Registers lose zero
   lines. The audit-local exact-K check rejects a wrong/unmerged tip,
   post-merge protected edit and merge-resolution protected edit. Excluding
   history alone is insufficient. The original unfiltered counts remain in
   the evidence.
2. **12 — lane ledger ownership.** The original ledger-path history command,
   with `--not K` before `--`, prints no line; the final ledger mode/blobs
   equal K. The ledger classifications and inherited owner routes remain
   required. Criterion 13's read-only history predicate remains unchanged.
3. **24 — no lane host action.** The committed census retains its observed
   time, baseline/current counts (712/1,061), both coordinator-authored
   mentions at lines 802/1003 and zero T39-authored entries. The closing
   census records no T39 START, RETURN, compile, runtime allocation or host
   write. Coordinator narrative is not a lane action. This is a retained
   producer observation, not a fresh host inspection; no host action or
   unqualified zero-match claim is authorized.

**Final verification method.** The stream brief's S6 no-replay instruction
supersedes § 10's blanket replay of accepted membership, stage runs,
generators and four harness runs. Reconcile their immutable inputs,
programs, outputs, counts and identities, including all 124 A–D receipts,
49 binary/art identities, 28 proof pairs and all 46 Phase-7 outcomes.
The 64 final ordinary producer receipts are retained separately under
`t39-final-producer-receipts/`, bound to T; committed H receipts at M remain
historical. `t39-exact-receipt-storage.json` maps four raw files to reversible
JSON envelopes, preserving exact bytes and hashes.

Execute new coordinator integration gates in a disposable clone: exact
coordinator/lane pins, full-entry log preservation, regenerated index,
rules/register/index/ceremony/forbidden/hooks, resolution lint normally and
with the audit issue, and diff hygiene. Retain commands, exits and hashes.
Read current issue bodies and verify every criterion against named evidence.
The old blanket-replay `kit/t39-accept.sh` is not run or claimed passing;
the retained reconciliation plus these new integration gates is the final
acceptance procedure. A missing or changed artifact blocks its predicate;
new behavior execution requires a separately scoped concrete correction.

This document records the method, not acceptance. Acceptance requires the
completed evidence mapping and all final integration gates, then coordinator
closure of audit #1406. Deferred owner work and bug integration obligations
stay open. The lane's completion marker follows explicit acceptance only.

The simulated merge’s full diff-hygiene command returned 2 solely for three
byte-identical accepted raw receipts (`stage-a/issue-states.txt`,
`stage-a/order.out`, `stage-c/tables/drift.out`). Their exact accepted hashes
and the all-other-paths rc0 are retained in
`t39-simulated-integration/diff-reconciliation.json`; historical bytes are
not normalized. All eight required new record/integration gates returned 0.
