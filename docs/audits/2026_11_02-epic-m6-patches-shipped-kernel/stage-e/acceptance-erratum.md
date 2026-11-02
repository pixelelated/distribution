## Acceptance erratum — 2026-11-02T18:55:24Z (D-WORKFLOW-226)

This prospective amendment supersedes § 10's blanket replay sentence. Stage-A/B
acceptances and their immutable receipts remain valid; the resumed coordinator
reconciles those artifacts without re-executing accepted producers. Stage C's
new formal generator has its own retained five positive and three negative
receipts at `94b5b1c0b983313325dba101217761c6e5c9bca0`. None of this is final
slice acceptance. Missing evidence still produces FAIL, CANNOT or ABSENT.

The final runner's `membership` section directly reconciles the retained block,
99-line outputs, selected immutable modes/blobs, inputs and counts against P1
and the final tip. It does not execute the old block. `runs` reconciles the
accepted 120 complete normal applications and D-WORKFLOW-222 candidate/prefix
receipts, including argv, patch/source/log hashes, digest-chain links, counts,
non-promotion control and the H700-011 dry/normal disagreement. Retained tree
and archive digests are producer observations, not newly measured filesystem
state. It never re-extracts sources or reapplies patches.

`checker-run` and `lint-proof` reconcile the exact historical program/fixture
identities, commands, output/exit receipts and their expected failures and
positive controls. Confirm those program/input identities are unchanged at the
final tip. An unexpected changed accepted input is a concrete coordinator
blocker, not automatic replay or PASS. A known, explicitly scoped new artifact
or failed predicate receives its own check; no blanket replay follows.

The final, previously unsatisfied gates still execute against the candidate:
resolution lint normally and with the audit issue; current rules/register/index/
ceremony and forbidden/secret checks; syntax checks on the final audit-local
generator; live issue/checkbox checks; and the simulated integration with the
exact coordinator tip. They must preserve actual command/output/exit evidence.
Do not substitute old receipts for checks of newly changed final records.
Review the commands first, confine writes to the coordinator's owned scratch,
mask permitted logs, use the existing checkers' interfaces, and keep all
source-only/held-data/runtime limits. The integration simulation changes only
a disposable clone; it does not merge or push a live branch.

The T2 implementation candidate remains separate from shared kit files. Its
receipt predicates and synthetic fixtures are useful, but its executable final
gates must be completed and tested before installation. Authorize implementation
and synthetic-fixture verification only in that candidate; no real final
acceptance run before the lane's completed hand-back. The coordinator alone
installs, runs, reads and accepts the final runner. Its verdict/summary/exit
contract and fail-closed behavior from § 10 remain unchanged.
