# Compiler timeout source correction — 2026-10-13

Refs #576, #570. Source review found that the original
`subprocess.run(timeout=60)` kills and waits for the compiler driver alone.
Compiler children can survive that timeout. No compiler was invoked in the
original recorded checks, so those checks did not exercise this defect.

`compile-api-smoke.py` now uses a single `run_bounded` helper for the compiler
and all pkg-config queries. `Popen(start_new_session=True)` puts each command
in its own POSIX session and process group. On a communication timeout or
another exception after launch, including a checked nonzero compiler exit,
the helper sends SIGKILL to the entire original group, even if the leader has
already exited. It then waits for and reaps the direct child with a separate
five-second timeout. It closes captured pipes instead of draining them without
a deadline. A group that has already disappeared is tolerated; other signal
errors and reap timeouts become explicit cleanup failures. The original error
is re-raised after successful cleanup. A failed compiler attempt still removes
its exclusively created output path.

The compiler communication deadline remains 60 seconds, and each pkg-config
query retains 15 seconds. Cleanup may take another five seconds. These are
subprocess deadlines, not a hard deadline for the entire script or an OS
process stuck in an uninterruptible kernel operation.

This implements process-group cleanup, not a subreaper or a cgroup supervisor.
The script reaps its direct child; other killed group members are reaped by
their parents or the environment's init/reaper. A descendant that deliberately
leaves the group, or termination of this script by an unhandled signal
(including SIGTERM/SIGKILL), remains the coordinator external runner's
containment responsibility. Any cleanup failure requires teardown of the
allocated job/guest and verification that its processes are gone before the
resource lease is released. No new runner or runtime lease is allocated here.

## Evidence and historical binding

This correction is **static source review only**: AST parsing, source/diff
inspection, and byte/hash checks. Neither the corrected helper nor a synthetic
child, pkg-config, compiler, binary, or VM was executed for this correction.
No process-group termination or reaping PASS is claimed.

`checks.json`, `checks-initial.json`, `compile-api-smoke.log`, and all other
pre-existing evidence receipts remain byte-for-byte unchanged. The recorded
compiler exit2 belongs to the original source at
`da0ecd80473037708dab38e82ea458708cc8c1b6`, whose SHA256 is
`b3301d16fca9a09bd8a93c81ca15caad4a9571d23112e3187d6238d0e3349aff`.
Its hash is deliberately not replaced in the historical receipt. The new
[static-review receipt](timeout-cleanup-source-review.json) hashes only changed
or newly added current source/documentation, excluding itself, and records the
unchanged historical bindings separately by original commit.

## Next coordinator-owned experiment

Before a compiler allocation, use an exclusively allocated disposable Linux
job/VM with a working init/reaper and an outer teardown mechanism. Exercise the
helper with synthetic commands that fork a child and grandchild in the same
group, ignore SIGTERM, and exceed the deadline. Include a captured-pipe case
whose driver exits while descendants keep stdout/stderr open, and a checked
nonzero driver exit with a live child. Use short test-only deadlines when
calling the helper; do not change its production 15/60-second call sites.

Retain command/source hashes, process IDs and group IDs, timeout/error logs,
elapsed time, the direct child's return/reap status, and evidence that recorded
descendants are absent after the environment's reaper has run. Also exercise
successful output and compiler failure/output removal. A forced outer-runner
termination must demonstrate job-wide teardown independently. None of these
checks ran in this source-only correction, and a pre-compiler readiness exit2
would still not prove the timeout path.
