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
