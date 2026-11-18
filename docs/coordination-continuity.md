# Coordination continuity

The operational coordinator owns worker dispatch and retained result consumption.
Keep human questions and meaningful outcomes separate from internal receipts.

## Keep communication scoped to its subject

D-WORKFLOW-194 clarification (November 18): Keep each update scoped to its subject. Group facts only when their relationship is established and relevant, and explain that relationship explicitly. In a requested broad overview, separate workstreams. Never use unrelated progress to imply that the current objective advanced or to soften its blocker. Check the implication of the complete response, not only the literal accuracy of each sentence. For example, M6 activity is not M7 progress and does not make M6 an M7 input or gate. State actual dependencies explicitly.

Keep operational ACKs/receipts out of the human conversation; preserve meaningful outcome and actual blocker reporting.

## Recovery and complete lifecycle

D-WORKFLOW-197 extends standing host authority and parallel continuation through the existing build preflight and result
writer; see `docs/build-authority.md`. After login or UI recovery, reconcile
actual process/session identities, retained failures/retirement and pending
returns before selecting successors. Verify the existing observer rather than
resetting reminder budgets. Record all lanes with observed start or item-specific
dependency; do not equate old completed assignments with an empty backlog.
Current recovery evidence: `docs/qa-logs/2026-11-18-workspace-recovery/RESULT.json`.
