# Build directory retirement lifecycle

The build account runs one ordinary-account retention engine for (1) a targeted
sweep after authoritative admission consumption and (2) scheduled checkout
reconciliation. This is the D-INFRA-025 and D-INFRA-030 generated-tree route. The existing
narrow, explicitly requested PCH retirement remains compatible. The engine
decides eligibility and reports exact holds, journal recovery and measured
space. This integration provides no delete authority, invents no manifest and
never converts an unconsumed or interrupted run to a qualified result.

The normal `watch-build` runner writes its original terminal channels as before.
After `build-admission consume` or the supported
`consume-reporting-failure` succeeds, and after the reservation lock is
released, the consumer starts one bounded independent targeted sweep. Its
output goes to a new `build-tree-retention-after-consume.log` in the original
run directory, outside the original command, runner and consumption outputs.
The trigger log marks the attempt only. An empty log is an incomplete attempt.
See the engine JSON and final sweep exit line for the outcome. Maintenance
failure, timeout and unavailable installation leave the original build and
consume statuses alone. A repeat consume does not overwrite a prior trigger
log. Periodic reconciliation handles a missed trigger, an interrupted build
or an interrupted sweep through the same engine.

The installed checkout is a stable canonical software location. Individual
builds continue using their selected frozen watcher, admission and evidence.
The engine always runs from its canonical home with its canonical sibling
guards, and the checkout passed to a targeted sweep is the original run's
checkout. An older frozen consumer may lack the immediate hook. Its existing
registry records still enter the scheduled checkout sweep, with no checkout
rewrite or per-run setup. Discovery snapshots both the canonical Git-common
and matching per-account filesystem registries under their own locks and
releases those locks before invoking the engine. It deduplicates job and queue
checkout paths, requires the configured checkout's volume, and visits up to
four registered checkouts per cycle. A private cursor advances durably before
each attempt so a repeatedly interrupted checkout does not starve other
producers. The cursor is scheduling state only. Each invocation independently
revalidates all deletion guards against current state.

Registry locks and old receipt formats remain independent. An unverified
mixed-registry protocol, incomplete queue or
dependency visibility, unknown host use or missing independent custody leaves
the affected files held. Use an exact verified fixed-path legacy custody record
when appropriate, through the engine's own contract. There is no age-only
deletion.

## Eligible checkout and working directories

A normal account-owned checkout with mode `0755` is supported. Its
`.build-runs` and generated `build.*` paths can be private (for example,
`0700`). Every directory traversed from the checkout into a selected
working path must belong to the build account, match the volume, and
exclude group and other write access. A `0775` checkout cannot safely
host this sweep even when its build directory and run records are
private. Another writer could replace the paths that lead to them.
The engine reports the hold before discovery. It also holds a shared,
foreign, redirected or replaced parent inside an otherwise usable
checkout. A preparation made before this layout is established confers
no authority over a different checkout or generated inode.

Use an ordinary non-shared project checkout with the existing admission,
run and result procedure. A future admission may point to a fresh
owner-controlled project checkout and its own generated outputs. Retain
original checkout provenance and independent results when selecting
that route. Existing shared checkouts stay held for the coordinating
owner. Nested selection narrows the set of positively owned generated
files through the existing custody and enrollment inputs. It still
requires trusted parents. Establish that layout when preparing an owned
checkout for normal admission.

Both expanded and compact custody are limited to owned working files
under the admitted profile's `build.*/build/` directory. They preserve
stamps, staged products, toolchains and result receipts outside that
working directory. A nested repository marker in the removal ancestry
also holds the affected scope. The engine binds the live ancestor
identities before host-use observation and rechecks each selected path's
ancestry at the unlink or empty-directory removal boundary. Unknown
siblings are left in place.

These layout checks are one part of the normal sweep. Accepted terminal
custody, all applicable registry locks and queue visibility, preserved
source/results, and the trusted current host-use report are still
required. The one-file private transfer cleanup example uses its own
exact retirement and recovery evidence for the individually named
transfer. Qualify a build-tree sweep through its own terminal custody and
host-use checks.

## Private update-tar QA readbacks

The host checkout's `tools/pixelelated-state-check --payload` can opt in to
retirement for one reconstructed `SYSTEM` file. Plan this as an ordinary
admitted QA run. Put the exact absolute keeper tar in the admission plan's
`inputs` and add `"private_readback": {"archive": "/absolute/keeper.tar",
"sha256": "<original packaging digest>"}` to that plan. Keep the ordinary
output declarations and their owners and release conditions. The normal
watcher assigns the private run directory, so no shared scratch root is
enrolled. Start the reader directly under the watcher from that checkout.

```sh
tools/watch-build --admission "$admission_receipt" -- \
  "$checkout/tools/pixelelated-state-check" --payload "$keeper_tar" \
  --private-readback "$keeper_sha256"
```

The reader exclusively creates `$run/private-readback/SYSTEM` and passes
the opened copy only to its own bounded SquashFS listing and cat commands
via an inherited descriptor. It publishes `$run/private-readback.json`
after reconstructing and reading back the copy. Keep this receipt and the
original QA channels. Add the receipt's exact absolute path and SHA-256 to
the normal acceptance's `evidence` array before running the usual
`build-admission consume` command. An investigated QA error can be consumed
without changing its original result. Use this route only for a
non-exporting readback whose copy will never be a VM disk, bind source,
queued input or independent deliverable.

The existing after-consume hook and 15-minute sweep both use the canonical
engine. The engine binds the original terminal result, producer admission,
and exact accepted receipt, then checks protected and queued references
under the existing registry locks. It acquires an exclusive kernel lease
on the copy and a read lease on the independent archive. It verifies the
archive and exact member again, compares the copy, writes a durable
intent, rechecks identity, and unlinks only that inode. It retains the
archive, original channels, source, siblings and run directory. An
interrupted intent with a missing copy and no receipt stays unconfirmed
and gets zero byte credit. A present copy with no complete producer receipt
stays held. Ordinary kernel lease refusal or file contention, changed
custody, and overlapping registered references also hold the file.
Verified unlinks and measured available-space changes remain separate.

This tier uses the existing 200-second engine bound. It accepts one plain
GNU or POSIX release archive up to 5 GiB and one regular `SYSTEM` up to
4 GiB per producer run, with at most 4,096 tar headers. It requires an owned
non-shared checkout, the original account and PID namespace, and supported
Linux file leases. Path or custody inspection outside the exact producer
and already registered scopes is outside this tier. Historical
extractions, exported media, install image scratch, manually created
copies and mixed retirement declarations need their applicable independent
custody route. Whole-tree and legacy safeguards and the timer configuration
are unchanged.

## Deploy as the ordinary build account

From the reviewed canonical checkout after the engine, its sibling guards and
this integration are present, use the same account and XDG state location as
the build producers. These commands stage and enable the standard Serval unit.

```sh
/usr/bin/python3 -I -B /workspace/repos/rocknix/tools/host-maintenance/build-retention-cycle \
  install --checkout /workspace/repos/rocknix
systemctl --user daemon-reload
systemctl --user enable --now pixelelated-build-tree-retention.timer
systemctl --user list-timers pixelelated-build-tree-retention.timer
```

The installer stages the owned settings and unit files exclusively, prints
their exact paths and does not call systemd. Repeating it with identical owned
settings and units leaves those files in place and fills only missing files.
It refuses different content, incorrect modes, aliases or foreign files. A custom
`XDG_CONFIG_HOME` must be the configuration root of the same user manager.
The service uses the recorded `XDG_STATE_HOME` or the ordinary account's
`~/.local/state` default. Keep the integrated checkout path and reviewed
software available across restarts. No privilege or linger change is required.
With the user manager stopped, catch-up occurs when the manager next starts,
subject to the ordinary persistent calendar timer behavior.

The oneshot runs every 15 minutes. Discovery has a 15-second subprocess bound
inside the 225-second cycle budget. A periodic checkout starts only when its
full 205-second engine timeout fits. A targeted sweep has the same 205-second
engine timeout. The engine's own finite bounds still apply. systemd starts
termination after 235 seconds and allows at most 10 seconds for that stop. The default
settings location gives the following unattended invocation.

```sh
/usr/bin/python3 -I -B /workspace/repos/rocknix/tools/host-maintenance/build-retention-cycle \
  sweep --settings /home/max/.config/pixelelated/build-retention.json
```

Each selected checkout gets the absolute canonical
`build-tree-retention sweep --checkout ABS` command. The targeted path supplies
the same engine with `--run ABS`. The cycle emits the engine's original JSON
for each invocation followed by a summary of attempted paths, holds, and
deferred count. The engine checks unregistered generated directories within
visited checkouts. Unregistered checkout roots, unrelated Git-common
registries and other parts of the volume remain outside inventory coverage,
as stated in each cycle summary.

Status 0 means settled or no eligible work. Status 1 means a named hold,
bounded deferral or partial recovery and remains visible in JSON and the
service's journal. Status 2 means integration or input failure. Only the
service treats 1 as a healthy timer invocation. The maintenance result is
independent of the build result. Read the first natural cycle in the journal.

```sh
journalctl --user -u pixelelated-build-tree-retention.service -n 40 --no-pager
```

Root rollout verification also needs one actual terminal/accepted job and one
abandoned job reconciled against real registry and host-use evidence, including
the engine-reported held and measured available bytes. The isolated lifecycle
tests exercise the actual admission/watcher/installed cycle with a fake engine,
so those tests fit a VM and carry no production host-use or reclamation claim.

## Run cleanup on demand

The build account can run `tools/host-maintenance/build-retention-cycle full`
from the installed checkout. It selects the project image from the existing
admission ledgers, then ranks the known directories on this volume using
verified inventory entries. It joins nested output paths to their declaring
checkout and checks known Git worktrees with ranked build profiles. Each
eligible checkout uses the same retirement engine as completion and the
scheduled service. The report identifies held paths and the inputs they overlap. A competing sweep holds the existing cycle lock. Each engine call
retains its normal deadline and use checks. The full pass leaves the timer
cursor intact. Unknown owners and incomplete discovery remain visible.

Use `full --target-bytes N` for a measured capacity goal. Include the proposed
stage's peak, reserve and other reservations in N. Exit 0 means measured
ordinary availability reached N. An already satisfied target returns before
discovery and reports the backlog as unassessed. A later successful capacity
result can still leave the backlog open. Verified unlinks, measured reclaimed
space and actual availability are separate fields. Admission still rechecks
current capacity and protections.

Use `full` without a target for the discovered superseded-build backlog. Exit 0
requires complete scoped coverage and terminal dispositions. A known empty
scope can settle with zero unlinks. Missing or incomplete inventory, an
unvisited checkout, an unresolved ranked path, or an unresolved guard keeps the
backlog open. A ranked path needs a matching verified retirement or coverage
by an exact retained image keeper path. A visit, a checkout-level no-op and
a build budget cannot settle a ranked path. Scope outside the inventory
continues to be disclosed by the report.

On a miss or incomplete backlog, stdout's `outcome` identifies the goal,
shortfall, backlog state and progress. The short stderr follow-through gives
the next owner and evidence-backed action. The JSON keeps the largest
reported hold, the highest-ranked ordinary action and up to three distinct
alternative remedies. These counts describe overlapping scope and action
records. Ranking never credits potential free bytes. The full pass already
tries independent ranked checkouts. If its leading ordinary action is an
operation or observation limit on an exact registered run, it can issue one
bounded targeted continuation through the same engine. A zero-result or
partially productive pass still exits 1 if its stated goal is open.

Treat shared-checkout diagnostics, legacy routing and incomplete inventory
as OS work. Examine the selected generated path's writer, alias and retained
input facts before choosing the next guarded scope. Escalate only a recorded
missing privileged operation with its exact operand and owner. For example,
an observed missing reviewed host-use reporter for an exact enrolled root
identifies the fixed reporter path and the storage administrator. A generic
ownership, permission or producer availability reason stays an OS diagnosis.
The ordinary preparation hook, periodic cycle and after-consume routes keep
their existing budgets and guards.

## Before copying or launching a build

Call the existing cycle module from the normal admission or private-copy
preflight with the selected checkout and volume, the complete peak byte
requirement (including the operating reserve), the current registered
reservations, and all inputs and destinations of the next operation.

```python
from pathlib import Path
from runpy import run_path

review = run_path(str(Path(canonical_checkout) /
                      "tools/host-maintenance/build-retention-cycle"))["prebuild_review"]
result = review(checkout, volume, required_bytes, reserved_bytes, protected_paths)
```

The sufficient-capacity path reads live filesystem availability and up to
twelve retained size hints without loading the engine, acquiring registry
locks or walking directories. Missing or stale hints do not block a build.
On a shortage, the preview reads
the requesting and canonical supplier Git-common registries and the matching
filesystem registry. It discovers producers from their project rows and
looks one level beneath `.build-runs` in the known checkout roots. A legacy
run with an admitted record or a nested checkout can appear even when the
caller's input list does not name it. A missing registry or unreadable data
has an explicit hold or omission. Unknown and unrelated project checkouts,
uninventoried directories, and files beyond the metadata bounds remain
outside the review. It does not recursively walk build caches.

The result includes `available_bytes`, `initial_available_bytes`,
`required_bytes`, `reserved_bytes`, `shortfall_bytes`, `candidates`,
`attempts`, `omissions`, and `measured_reclaimed_bytes`. The first capacity
snapshot preserves the caller's reservation operand. On shortage,
`observed_reserved_bytes` separately counts visible running reservations
across the found routes once. If that count exceeds the caller's snapshot,
retirement is held. The admission caller owns current, locked capacity
revalidation before publishing a receipt or starting the work.

Candidates report exact accepted leaves only when their identity, ownership
and final hard link still match. Native immutable catalogs and identity-bound
compiled custody snapshots are reusable. A compact keeper without a snapshot
is unmeasured until the guarded engine acts. Nonzero original outcomes with
accepted failed-investigated custody can qualify. An expired lease or
unregistered abandoned run can be reported but supplies no retirement
authority. `unique_observed_bytes` counts each device/inode once across the
report; it is an inventory figure and cannot satisfy admission.

A shortage reader can also consume a small, optional retained size inventory
from the ordinary account's canonical XDG state directory. Under
`pixelelated/build-retention-inventory/<device-hex>-<fsid-hex>/`, an owned
`index.json` contains `{"schema":1,"sha256":"..."}` for the exact bytes of
the sibling `inventory.json`. Both files must be singly linked with mode
`0600`. The inventory object contains `schema:1`, `volume:[device,fsid]`
(decimal integers), `observed_epoch` in Unix seconds, and up to 512
`entries`. Each entry has the already-discovered `path`,
`allocated_bytes`, a short custody `reason`, full `identity` containing
`device,inode,uid,mode` as integers, and the observed `mtime_ns` and
`ctime_ns`. Populate this from retained project measurements and their
matched directory identities. Stale, replaced, or out-of-scope entries are
omitted. A matching directory timestamp cannot establish that its descendants
are unchanged, so hints only affect the presentation order. Hints can
overlap other hints and must never be added into projected capacity.

Call `prebuild_last_sizes(volume, registered_paths)` if the admission caller
already matched paths using its locked ledgers. The result contains only
`candidates` and `omissions`. Candidates have `path`, `allocated_bytes`,
`reason`, and `inventory_sha256`. The helper checks up to 4,096 supplied
names lexically, reads at most 4 MiB of fixed inventory metadata within a
two-second metadata budget, and returns up to twelve matching hints. It
never acquires an admission lock. Ordinary stat calls inspect only matching
recorded names and the selected volume.

Use `retire=True` only from the normal shortage path after the workload's
complete pending protection has been durably published in the existing
admission registry. The review releases its advisory registry locks before
calling the guarded engine on a single exact terminal run. The engine must
see the pending workload scope in its own lock set. Among eligible runs,
measured final-link bytes govern ordering, with unmeasured compact custody
as fallback. The engine retains its own use, ownership, dependency and
recovery checks. A refusal on one run can advance to another; at most three
exact attempts are made, each with the existing 205-second subprocess bound.
See the named hold for remaining limitations, including a filesystem-keyed
legacy preparation interval the engine cannot observe.

Every attempt and final decision resamples free space. The measured reclaimed
field is bounded by the engine's newly verified unlinks, their observed
per-attempt gain and the final net gain. An observed increase without that
binding may improve actual capacity while reporting zero verified reclaim.
No ranked estimate, pending delete, or recorded allocation is credited as
free space. The ordinary admission locks, original one-use behavior, and
periodic reconciliation stay in effect.

### Single local OS image generation

The image keeper uses the actual image stage of a watched release, mkimage or
noobs invocation. Its admitted build, target and source locations are joined to
the original watcher and artifact identity. The same selector ranks all supplied
project registries across targets and volumes. One actual active generation
takes precedence. When idle, the newest successful completed generation wins.
Two active generations, an unclassified newer legacy firmware producer, or
changed original evidence hold retirement. Package runs and QA copies do not
supply image-stage records.

The ordinary, periodic, completion and prebuild guarded routes consult this
policy under their existing effect locks. Queue inputs, other owners and
original source/result custody remain independently protected. The selector
adds no release or deletion authority.

For a read-only report use:

    tools/host-maintenance/build-tree-retention keeper --checkout /absolute/project/checkout

An owner-reviewed legacy migration can be checked with the keeper command's
--migration argument. For ongoing use the selected authority stores the
validated immutable document as os-image-history.json in its admission
registry, owned by the ordinary build account with mode 0600. The two legacy
roles are a successful full producer and independently joined same-image media.
The media does not supply a separate generation or change completion rank.
Read-only reporting accepts unsealed legacy rows. Effect routes still require
the existing registry and custody admission. Full-pass callers can use
select_os_keeper(ledgers, effect_volume_device) in build-tree-retention and
apply the reported keeper.protected_paths to their own locked operands.

## Release compiler-cache space from a held checkout

A checkout trust refusal applies to the attempted tree operation. The build
account can still maintain a separately qualified local ccache with its native
tool. First check the actual owner and parent, the fs/device and inode, the
retained image and queued inputs, host copy jobs and relevant container mounts.
Identify the exact cache root and hold it by directory descriptor. Check the
shard entries, including their ccache format, version, namespace and link
counts. An unknown file, foreign writer, competing raw copy or unresolved
alias holds that store. Move to the next qualified store. The project keeps
the compiler, configuration, stamps, source and retained images.

On the tested 4.13.6 stores, the build account used the matching host binary
and libraries. Under the admission locks it bound the cache and library
directories by open descriptor, selected the empty namespace and evicted
entries older than 21 days. The native tool takes its shard locks. In a
qualified wrapper, the native invocation takes this form.

```sh
"$ccache_bin" --evict-namespace '' --evict-older-than 21d
```

Bind `CCACHE_DIR` to that selected store and use a controlled config and
private temporary directory. Validate the affected entry types first.
An age-only cleanup can also remove unexpected files under the shards.
Keep the native exit status and the cache metadata before and after. Compare
the remaining entries, account for shared inodes, and take free-space
measurements directly around the eviction. Record any partial effect before
considering another action. Attribute at most the independently verified
released allocation to a positive free-space delta. This route retires cache
entries. The surrounding generated profile needs its own disposition.

## Verify coverage before using whole-profile retirement

Check that the ordinary producer declared the disposable generation and that
the collector can consume that same declaration after completion. Retain the
actual source, user edits, accepted deliverables and original result outside
the selected scope. A cold rebuild may replace obsolete compiler output.
Preserving a second complete profile, starting a replacement build or
constructing a catalog by hand for a test is unnecessary for that purpose.

Use recorded counts and link information from the real profile before asking
for host observation. Check all three bounds: custody compilation, the
retirement engine and the enrolled host reader. A successful small
opted-in fixture proves only that layout, its entry count and its link types.
Count literal symlinks without following them. Identify hardlinks with names
outside the selected generation and account for blocks only once.

For the October SM8550 run, the prior counts were 870,240 names for ARM and
3,617,361 descendants in the AArch64 comparison. The deployed compact compiler
allows at most 8,192 items, the effect inventory 65,536, and the host reader
200,000 entries per pass. The host index also refuses a hardlink with an
unaccounted-for name outside the root. The two original producer receipts
lack an ordinary accepted whole-profile declaration. Selecting the newer
image or freeing sufficient space does not satisfy any of those requirements.
Keep these generations open under their exact scoped retirement operation.
