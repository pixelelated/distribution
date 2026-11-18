# Coordination continuity

The operational coordinator owns worker dispatch and retained result consumption.
Keep human questions and meaningful outcomes separate from internal receipts.

## Recovery and complete lifecycle

D-WORKFLOW-197 extends standing host authority and parallel continuation through the existing build preflight and result
writer; see `docs/build-authority.md`. After login or UI recovery, reconcile
actual process/session identities, retained failures/retirement and pending
returns before selecting successors. Verify the existing observer rather than
resetting reminder budgets. Record all lanes with observed start or item-specific
dependency; do not equate old completed assignments with an empty backlog.
Current recovery evidence: `docs/qa-logs/2026-11-18-workspace-recovery/RESULT.json`.
