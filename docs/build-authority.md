# Standing host build and test authority

Authority ID: **D-WORKFLOW-196**, granted by Max on 2026-11-17.
Canonical operating rule: [.claude/rules/device-builds.md](../.claude/rules/device-builds.md#standing-host-build-and-test-authority).
This repository record is available to every harness; private memory, an installed
skill, or access to the originating chat is not required.

## Verbatim authority

> Yes, go ahead and prepare the reviewed code for the M7 build.

> Also, how do we prevent me from needing to do this type of approval again? This seems pretty important and like something we will need to continually do, so we should have a permission that enables us to run this in an ongoing manner, as opposed to requiring one-off approval.
>
> Being able to create, generate, and test builds is something we frequently need to do and have done in the past, so we need a way to make sure we can do it in the future. I'm not sure what's changed, but what's important is that we have a good solution in place.

> Need to make sure this isn't just stored in memory, but stored in a durable fashion, so it is portable and can be invoked by any harness. It needs to be an instruction file, agent file, etc.

The first approval accepts the presented M7 private source-assembly proposal:
3660 bytes, SHA256 `c04df1b893ab5ded8c6b44b41622b637c671ce94aaf0b825e419bed4f565ed37`.
That individual run has CPU quota 200%, memory 2 GiB, no swap, 128 tasks,
540 seconds service runtime and 900 seconds for the whole episode, with private
outputs and network isolation. These are that run's limits, not limits for all
future OS builds. The subsequent instruction grants ongoing routine host source
preparation/assembly, builds and isolated testing under the project rules.

## Invocation reference

This includes executing ordinary internal activation/START and launching the
authorized host assembly/build/test workload, subject to actual platform review
and per-run readiness. It is execution authority, not merely permission to edit
preparation files. Describe those effects accurately at the review boundary.

For each run, cite **D-WORKFLOW-196**, this document and the canonical rule.
Record the concrete operation, selected source and output/worktree, owner,
operation-specific resource/time/disk limits, current admission evidence,
monitor/result location and remaining separately governed actions. Include the
relevant authority and effects directly in platform-review justifications;
merely pointing to a nested selection file can lose the scope at that boundary.
Admission and START records implement this authorization; they are not another
request for Max's permission. No record may claim a process started before it did.

Preserve original attempts, refusals and one-use budgets. An actual enforcement
refusal is not overridden by this document. Inspect its stated reason and exact
submitted authority, retain the originals, and use only the review system's
supported evidence/review route. Never disguise activation as a metadata-only
operation or route around a refusal. Escalate the actual unresolved boundary in
ordinary language rather than asking Max to approve technical file counts.

This standing authority does not itself authorize physical-device actions,
personal/cloud data changes, publication, destructive cleanup, changing shared
platform settings, foreign supplier commitments or automatic retention renewal.
Those retain their own governing instructions and approvals.
