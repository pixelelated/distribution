# Standing host build and test authority

Authority ID: **D-WORKFLOW-196**, granted by Max on 2026-11-17.
Canonical operating rule: [.claude/rules/device-builds.md](../.claude/rules/device-builds.md#standing-host-build-and-test-authority).
This repository record is available to every harness; private memory, an installed
skill, or access to the originating chat is not required.

For cache staging and build admission, follow the [build-volume headroom
check](../.claude/rules/worktrees.md#check-build-volume-headroom-before-copying-or-launching).

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

### Launching a two-ABI device build under admission (#1442)

A handheld build runs two passes, `arm` and `aarch64`, so its admission
declares two profiles (for example `ROCKNIX/H700/arm` and
`ROCKNIX/H700/aarch64`). Export one of them for the outer launch:

```bash
PROJECT=ROCKNIX DEVICE=H700 ARCH=aarch64 make docker-H700
```

The device's make target sets each pass's own profile inside the container,
so both passes still match an admitted profile. A Docker launch with none
exported is refused by `build-admission` at once, with the profiles to export
named; until 2026-11-25 it got through admission and the host-side Docker
entry refused it later ("nested profile is outside admission"). A native
`make H700` needs nothing exported, because each pass sets its own profile
before its nested check. A single-profile build, such as GENERIC_X64, needs
nothing exported either: admission fills its one profile in.

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

## Complete execution and evidence lifecycle (D-WORKFLOW-197)

Max instructed: “We need to make all five of these changes.” The five accepted
changes are narrow writable destinations, actual lifecycle preflight, compact
result references, measured prospective budgets, and observed continuation.
The exact request and recovery instruction are retained in
`docs/qa-logs/2026-11-18-workspace-recovery/REQUEST.md` (#1437).

Before selecting a run, reconcile the **effective live** executor profile with
its owned source, output and report paths. A config edit does not change an
already-running session. Codex0.169.1 supports `--add-dir <exact-owned-directory>`
with workspace-write and review retained; Herdr's supported agent-start interface
passes native arguments after `--`. A managed app-server launcher exposes the
workspaceWrite `writableRoots` through its supported sandbox policy; require its
actual settings readback rather than assuming the CLI option was honored.
Do not restart a busy lane or alter protected/shared permissions to apply this.
Use an already-writable private location when it satisfies the operation, or
request review for the exact otherwise-authorized effect. No broad full access.

The November18 live OS session grants its worktree and `/tmp`, not
`/workspace/artifacts`. `auto_review` does not establish that every editing route
has access to another directory. The prior large apply_patch publication reached
a manual edit UI; the pathname/profile mismatch is verified, but the internal
reason that particular route did not auto-approve is not established. Do not
claim that changing repository prose or a config file repaired the live profile.
Select the actual supported writer and test that route, including its permissions.

Preflight the selected executor's prepare, input resolution, bounded execution,
**same report writer**, readback and retirement with owned disposable probe
outputs before the expensive run. Use one exclusive, fsynced immutable original
and bounded path/byte/digest references thereafter. Test payload sizes and
argument limits representative of the real evidence; a shell touch does not
prove a later edit-tool publication works. Keep probe success distinct from
real workload success. `tools/build-preflight` remains the existing entrypoint.

Use `tools/watch-build-submit --record-result` to retain compact immutable result
references and optionally update a compact current pointer; it does not infer
success from submission or copy the full ledger. Keep full originals available.
Derive new work/reporting budgets from actual extraction, checkpoint and writer
costs plus explicit shutdown/report reserve and current host admission. Separate
user/platform hard limits from coordinator estimates. Never extend a spent run;
a prospective D196 selection must explain its limits and preserve the original.

A useful result proceeds into actual next authorized work, or a specific external
constraint with its owner. Report deadlines do not postpone root preparation.
Inspect current priority/issue criteria for useful independent work, record
actual starts and returns through existing lanes, and leave capacity ready when
its named dependency is unmet. Do not invent reviews or a competing scheduler.
