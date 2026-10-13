# Next executable preparation and serialized experiment — UNRUN

**VM-first answer:** this policy, its memory/CPU consequences, and synthetic
sign-in preservation can be tested on GENERIC_X64. No physical fact requires a
device. The coordinator must record the exact plan and resource owner in #570
before runtime. No runtime lease or compiler authorization is granted to this
worker. #493 still gates any full build/cache copy; neither is needed to author
or statically validate this packet. Delivery03 and prior test owners are retired.

## 1. Source preparation, independently executable now

From the assigned checkout, the following is read-only static validation:

```sh
export TMPDIR=/workspace/tmp/pix-m7-investigation-20261013/tmp
packet=docs/qa-logs/2026-10-13-browser-memory-policy
webkit=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/build/webkitgtk-2.54.1
python3 "$packet/prepare.py" --repo . --webkit-root "$webkit"
```

For the later coordinator-owned stage, emit the ~50 KiB C file using the same
command with `--emit-candidate > "$stage/cloud-signin-window.c"`, where `stage`
is a newly allocated private directory, not the immutable cache. Check its
SHA256 against `candidate.json`. This performs the exact transformation without
GNU patch. Alternatively, after verifying both compressed and uncompressed
hashes, GNU patch can consume decompressed bytes via stdin in a tiny fresh tree.
Do not assume GNU patch is installed in the guest. Stage verified small source
or binary files from the host; do not prepare or modify the accepted cache.

The candidate deliberately has no page observer. The coordinator owns that
instrumentation and must bind the combined source/observer hashes and prove the
policy helper is its only A/B delta. Do not invoke archived UA/breakpoint
`prepare.py`, `provision.py`, or `matrix.py`: they contain retired private-owner
paths and allocations. Reuse reviewed source content only, through the new owner.

## 2. Small diagnostic compile and synthetic gate, after allocation

Compile only this application translation unit against the already installed
GTK3/WebKit2GTK4.1 sysroot, using the recipe's compiler/flags/libs and `-latomic`.
Do not build WebKit or copy its cache. The prior compiler harness assumes an old
container mount path; verify the actual compiler/sysroot mapping rather than
blindly replaying it. Record compiler, pkg-config GTK/WebKit versions, source,
flags, sysroot/library hashes, binary hash, and actual exit. If unavailable, stop
with that blocker; this packet does not authorize provisioning.

Before actual-page work, one new synthetic preservation gate per mode must use
the coordinator's fail-closed loopback fixture and no provider/account data:

1. `CLOUD_SIGNIN_MEMORY_POLICY=default` and `strict35` both report WebKit2.54.1,
   ephemeral=1, conservative=.33, poll=30, kill_fraction=0; strict=.50/.35.
   Verify installed library identity as well as the reported version.
2. Exercise enabled JS with a retained object checksum and a bounded temporary
   allocation whose references are dropped. Wait through two 30-second periods,
   keep a visible page, and retain the checksums/form state. Do not increase
   allocation until OOM just to force a policy crossing.
3. Use dummy email/password text, native keyboard focus/typing, an allowed
   related popup, origin-checked postMessage/opener return, and local callback
   receipt. Assert exact fixture state, popup close, and successful return.
   Assert a disallowed-host navigation/popup remains refused. Do not use real
   credentials or a real IdP to fill this gate.
4. Set fixture cookie/localStorage/sessionStorage sentinels, preserve them within
   the session where appropriate, then close all browser children. In a fresh
   ephemeral launch assert no persisted cookie/localStorage; sessionStorage
   must not migrate to the new top-level session. Preserve offline proxy state:
   no proxy service/account is needed or touched by this browser experiment.

These are candidate-specific tests, not a claim that they ran here. Source
equivalence cannot prove cookie/popup/input behavior under GC or memory pressure.

## 3. Conditional actual-page A/B, serialized under coordinator ownership

First consume the coordinator's page/CPU/reclaim attribution. This candidate is
worth running only if the WebProcess spends time in the 0.35–0.50 physical-RAM
RSS band through a periodic deadline, and reclaimable memory is plausible. If
all relevant samples are below 0.35, or above 0.50 before both deadlines, return
**control not exercised** rather than changing several knobs. If page execution
dominates without reclaim/GC evidence, defer this control under D-WORKFLOW-163.

Proposed bounded matrix after that gate: **default, strict35, strict35, default**,
one browser at a time, a fresh ephemeral context each, 65 seconds per trial,
same 1280 MiB-assigned guest profile (~1042.6 MiB historical visible RAM), four
vCPUs, software renderer, original DMABuf override, same desktop UA and 640 CSS
width in every cell. Use the normal ES handoff/return, no proxy or phone client,
same untouched cookie-banner state and no credentials/login. The coordinator
must separately authorize any actual-provider page access; this source packet
does not do so. Do not silently change guest memory or renderer to make the
policy pass. Allocation includes synthetic gates plus a single four-cell matrix;
no automatic extensions/retries.

Launch-environment delta, within the coordinator's reviewed runner only:

```text
arm A: CLOUD_SIGNIN_MEMORY_POLICY=default
arm B: CLOUD_SIGNIN_MEMORY_POLICY=strict35
both:  JSC_logGC=1   (if included in the recorded observation plan)
```

Do not set other JSC/allocator/cache knobs or
`WEBKIT_DISABLE_MEMORY_PRESSURE_MONITOR`. Preserve every environment value that
affects graphics or auth. Record relevant scalar overrides without dumping the
entire environment or an OAuth URL.

Start monotonic-clock sampling before child creation. At 1 Hz capture PID plus
starttime, RSS/PSS/anonymous, per-process user/system CPU and major faults,
MemAvailable, memory PSI totals, reclaim/refault/allocstall counters, cgroup
membership and effective limit context. Retain timestamped bounded stderr for
relief totals and JSC GC events; policy startup lines must match the requested
arm. Keep the coordinator's same heartbeat/input/load/frame observer in both
arms; it is not a script profiler. Retain at least the two periodic opportunities
near 30/60 seconds, and delayed samples after any asynchronous cleanup.

Keep the existing 100 MiB MemAvailable abort threshold and a 65-second deadline
with verified owner/watchdog. Stop a trial on either guard, unexpected child
termination, stalled runner, unsafe log growth (proposed 8 MiB per trial), or
lost callback/input state. Record the abort as a failure, restore the original
browser, and return the result; never extend the run to force success. Match
all log limits and observation settings across arms. The coordinator allocates
exact VM/PID/ports/disk limits; none of the retired values is reusable authority.

## Interpretation and retirement

Require independent evidence that the control operated. A lower PSS sample or
the startup line alone is insufficient: relate per-child RSS/deadlines to
relief/GC activity. The Release build may not identify exact policy transitions;
if system pressure notifications or asynchronous event timing prevent attribution,
report **activation ambiguous**, not policy accepted. Do not infer 30-second
timer execution when the child's main loop may have been stalled.

Compare paired peak AND end-of-window browser PSS/anonymous, minimum available,
kernel reclaim/refault deltas, total browser CPU-seconds, GC pause/cycle totals,
load/heartbeat/input-to-paint and ES return time. Reduced immediate RSS with
higher CPU, repeated recompilation, worse input, extra resource requests, or
callback/popup failure is not an improvement. Four cells screen the hypothesis;
they do not establish a production threshold or statistically reliable benefit.
Preservation failures reject the candidate. A promising result needs later
same-observer qualification and clean/upgrade paths before promotion.

Return exact source/binary/library hashes, actual process exits and guards,
numeric/page/frame evidence, and restored browser/no remaining children/retired
owner receipts. Reverting the one environment mode to `default` restores policy
for a newly constructed context; removing the diagnostic binary restores the
original application. No account, provider, proxy, or stored-data cleanup should
be necessary because this experiment must not create such state.
