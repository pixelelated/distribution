> **Current execution — November18:** source assembly14 is actually running
> under D196, with CPU2/2GiB/swap0 and successful incremental checkpoints.
> Attempt11/12/13 failures are preserved. The corrected terminal route passed
> root's actual default-executor checkpoint and621442-byte raw-stdin save.
> Independent #610 guest proof completed27cases and retired; its exact fix regions
> are already in the selected candidate, so no patch/replay is needed. Two issue
> criteria are proved; affected-image packaging remains open. All seven worker
> dispositions are in the compact result. Root supervises assembly/report/retirement,
> then candidate build readiness; near-full host swap must be handled through
> the existing guarded helper after active work retires. No new user decision.
> Read `docs/qa-logs/2026-11-18-workspace-recovery/RESULT.json` for current evidence.
> Earlier activity/approval waits below are historical where superseded; M6
> remains independently owned and is not an M7 dependency.

> **Execution observation, November17 (D-WORKFLOW-195):** source-assembly START
> remains rejected. Independent #610 fixture preparation completed20 host checks;
> target-image qualification remains open. M6 continuation193 completed useful G283 metadata, done14711;
> wholeG283 remains open and next relation assessment stays with its original owner.
> Earlier settled-state observations are history, not current execution status.
> Evidence: `docs/qa-logs/2026-11-17-proactive-continuation/blocked-path-parallel-progress/RESULT.json`.

# Current project priorities

Maintainer correction, 2026-11-16: **M7 stabilizes the current candidate. M6 assesses
the codebase in parallel and produces a punchlist for the following major build.**
M6 recommendation integration is not an M7 prerequisite. D-WORKFLOW-185,
[#1435](https://github.com/pixelelated/distribution/issues/1435).

The machine-readable current queue is [current-priorities.json](current-priorities.json).
This page explains its governance; do not append daily chronology to either file.

| Order | Priority | Owner | Outcome / boundary |
| --- | --- | --- | --- |
| Now | M7-SCOPE | M7 root / P9 | Identify and exclude the mistakenly selected M6 overlay from the M7 candidate plan, preserving independent M7 fixes and all historical evidence. No blind rollback. |
| Now | M7-STABILIZE | M7 root | Finish current candidate stabilization and required qualification. |
| Parallel | M6-ASSESS | M6 root | Maintain assessment coverage, findings and punchlist; do not integrate recommendations into M7. |
| After M7 | M6-GAP | M6 root | Freeze the latest completed M7 build and its exact source, pause development, and complete the final gap-analysis review. |
| Later | NEXT-MAJOR | Coordinator | Use the final M6 recommendations to plan and implement the subsequent major build. |

## Where each kind of information belongs

- **Goals and order:** this current queue and the live [M7](https://github.com/pixelelated/distribution/milestone/7)
  and [M6](https://github.com/pixelelated/distribution/milestone/6) milestone bodies.
  The milestone bodies remain the tracker execution plans; they link the same
  priority IDs and revision. A disagreement is reconciled before dispatch.
- **Phase and task:** linked milestone issues name the outcome, owner, dependencies
  and exit artifacts. Each assignment cites its parent priority ID and revision.
- **Current activity:** the existing coordination ledger tracks selected, working,
  returned, consumed, blocked and intentionally idle states, with next checks.
- **History and learning:** dated work logs link task -> phase/issue -> priority;
  decisions explain changes, and retros/futros test whether the process improved.
  Child-lane logs link back to their owning issue and priority; the coordinator's
  day log links child results instead of copying their transcripts. Existing
  logs stay intact. Historical entries are not the current queue.

## Rules for updating and using the queue

1. On resume, read this page and the JSON before worker returns or old task plans.
   Read live milestone bodies when changing phase, scope or order.
2. Before dispatch, choose the priority ID, work kind, input milestone and output
   milestone. Run `tools/priority-check` with those values. Retain its result and
   priority digest in the existing selection record, alongside the concrete task.
   This checks declared scope only; the coordinator must also inspect the actual
   deliverable. It grants no execution or device authority.
3. A source handoff is evidence, not a priority decision. Cross-milestone findings
   go to the originating punchlist unless explicitly selected for the target.
   A separately required M7 defect may still be fixed under its M7 issue; record
   that rationale rather than importing the whole M6 recommendation queue.
4. A maintainer scope/order change updates the queue, live milestone bodies,
   decision register, coordination ledger and affected owners in the same turn.
   Preserve previous snapshots and link the work-log change record. No silent
   priority changes through a new source map, archive or technical handoff.
5. At each return, check its outcome against the selected priority before marking
   it complete or scheduling a successor. At each phase transition, reconcile
   active assignments, dependencies and exclusions. Weekly retros inspect scope
   drift as well as idle time, and remove redundant administrative work.
6. M6-GAP and NEXT-MAJOR stay unavailable until their stated prerequisites are
   actually met and the queue is explicitly revised. The final review pause is
   scheduled after M7, not imposed now.

## Current correction and verification

The November 14 M6 composition selection was a scope error. It and its derivatives
remain historical evidence; they are no longer a direction to integrate M6 into
M7. P9 owns the finite provenance/separation plan. Existing private archives and
failed assembly outputs are retained, not deleted or represented as M7-qualified.
Completed generic tooling corrections remain available; their necessity for the
M7-only route must be established before more dependent work is scheduled.

The next actual handoff must demonstrate that the declared priority and delivered
scope agree. Passing the guard or saving this document is not proof of sustained
coordination improvement. See the [November 16 work log](work-logs/2026_11-work_logs/2026_11_16-work_log.md).

The M7-only source boundary is selected: 228 actions, 21 directories, 83 equalities,
221 unique inputs and the original ES archive/recipe. M7I-1/2/3 are closed in
source. Placement, observation, control publication and enablement results are
consumed; their timing and custody qualifications remain in the work log.

Materialization05 failed and is spent. The paired typed-index correction8f299c33
is accepted in source after independent review13307. P9 batching successor13311
is returned as proposed source (55506 bytes/0bc2a543): extraction-only parent
flush batching, directory identity checks and complete pre-success flush coverage.
Interrupted batches remain unqualified; other callers retain eager durability.

Both production fixes and the context06 composition are accepted within their
reviewed source scopes. P8 review13368 found no composition blocker and confirmed
all22 harness slices remain identical. The later qualification binding needs two
whole-source hash updates and their dependent SLICES/argv/request references.

P8 closure13416 accepts the grouped corrected harness/context06 source within
its reviewed scope. Supplier13430 is now also accepted: exact20 module slots,
selected grouped templates and unchanged27-child/360/450 limits. Root verified
the47-member seal and minimal source/template changes directly, reusing the
accepted parent review. No new grouped-source audit is selected.

P7 negative witness13437 confirms that its named retained image-route records
provide no Python module/loader associations. The finite lookup is closed;
no whole-build absence is claimed, and no further index scan is selected.
The existing baseline17 collector remains the missing image listing/tool
producer; its output will not by itself qualify Python kinds/version/loading.

P-D13455 is consumed: all74 selected static bindings matched;48 regular targets
and31,523,257 total episode bytes were read, with original0 and no drift/errors.
The concrete request remains refusing. Root prepared a nonexecuting proposal:
existing user-service boundary,512MiB service MemoryMax and256MiB outside
observer/publisher planning allowance. These are proposals, not admission or
reserved resources. Static equality does not establish behavior applicability.

### Current continuation — November17

The input-retention/never-started stoppage is cleared. Root prepared private owned
source/helper copies and executed the existing short runner check once. All four
cases produced expected results and exact service retirement was verified. The
original evidence publisher failed a0664 carrier-mode guard; that failure remains
explicit. A narrow source correction passes focused tests, without runtime replay.
Read the [actual outcome](qa-logs/2026-11-17-proactive-continuation/owned-run-outcome.json).

The corrected image collector and two incremental Python collections have now
executed under normal platform review. They completed16,27 and25 reads. Original
missing-utility and permission-mode failures remain spent; the mode fix preserves
intentional BusyBox4755 rather than changing image permissions. Ten focused
checks passed. The baseline final cut retains a receipt-envelope error, with
separate verification of unchanged original outputs; both Python batch cuts pass.
All image hashes/identities matched before and after, with children and services
retired. No guest or new build has run.

Root joined12 tools,20 declared Python modules and4 loader files and verified the
target's static builtin/frozen tables and version without executing it. Prepared
worker/prior input contracts pass source checks. The next disposable-VM source
preflight has begun; capacity observation is not admission. Root owns the exact
firmware/readback/safe-name and current execution selection joins. See
[static-input result](qa-logs/2026-11-17-proactive-continuation/python-static-input-preparation/RESULT.json)
and [VM source preflight](qa-logs/2026-11-17-proactive-continuation/python-static-input-preparation/vm-successor-preflight.json).
There is no active Max decision. Prior approval remains resolved/spent; no owner
commitment was renewed. D-WORKFLOW-191 requires actual continuation, not another
scheduled status checkpoint. Independent M6 assessment remains separate.
