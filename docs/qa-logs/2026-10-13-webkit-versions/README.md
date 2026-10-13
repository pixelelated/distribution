# WebKit versions, memory pressure and GStreamer package closure — 2026-10-13

Owning issues: #570 browser pressure, #572 packaging, #573 upstream troubleshooting rule.
Can this be done on the VM? Yes. All work here used disposable GENERIC_X64 guests,
public unauthenticated pages and package-only builds. No owner device or cloud data action.

## Findings

The installed WebKitGTK2.54.1 remains the latest published stable release. Related
upstream reports were checked against our actual source, without a confirmed match:
[dated upstream review](upstream-check.md), [fix-presence hashes](font-fix-presence.json).
D-WORKFLOW-162 now requires this check early in every investigation.

The 2.54.0 microversion does not provide an observed memory improvement. An initial
loaded 1024MiB-guest trial reaches390.14MiB browser PSS versus380.98MiB for installed
2.54.1. The original old-engine matrix nevertheless FAILED its post-run bundle-path
assertion; this is a retained measurement, not a passed matrix. The corrected repeated
matrix then stalls with both engines and the VM resets during its fourth trial.
These unloaded pages are excluded from memory comparisons.

With a planned restart at2048MiB, both engines load successfully and direct-reclaim
counters remain unchanged. This is a headroom control, not proof of handheld performance
or resolution. Three90-second runs, all loaded with two reviewed native frames:

| Engine/package | Peak browser PSS MiB | Minimum MemAvailable MiB |
| --- | ---: | ---: |
| 2.54.0/original | 580.81 | 907.67 |
| 2.54.1/original | 560.60 | 965.64 |
| 2.54.1/corrected GStreamer | 568.21 | 961.38 |

Each run exits cleanly, leaves no browser processes, preserves boot identity, and
restores temporary mounts. Greater PSS with more RAM is not directly comparable to
pressure-constrained PSS. One ordered sample per case is not a statistical regression
finding. See [trials](trials.json), [samples](samples.json) and [headroom result](headroom-result.json).

## Failed low-memory matrix and reset

At1024MiB assigned (810368KiB visible), repeat02 trials1–3 never reach a loaded page;
trial4 on2.54.0 resets the guest at01:11:15UTC, before the host timeout at01:12:45.
Trials5–6 never run. The original result remains1. Native loading frames and exact
result files are retained. A duration stop and rc0 from the older sampler were
insufficient acceptance: measure02 now requires the page URL, load-finished record,
two captured frames, unchanged boot ID and clean teardown; it streams samples to
storage so a reset does not erase all measurement output.

A3.03-second snapshot during a stalled2.54.1 trial shows428136 direct-scanned pages,
310215 direct-reclaimed pages,310001 file refaults and7306 allocation stalls.
Host RAM remained available. This is severe guest reclaim activity, but not proof of
a memory leak or the physical H700 incident's precise cause. Previous-boot evidence
contains no established OOM/panic/reset cause or pstore dump. A15-second watchdog was
configured; its involvement is unproved. Zone snapshots are explicitly POSTRESET.
The optional schedstat read dropped process rows in resource-snapshot.py; its empty
process list is invalid evidence of absence. The principal smaps sampler is unaffected.

[Reset summary](reset-summary.json), [raw counter pair](resource-snapshots.jsonl),
[previous boot journal](journal-previous-boot.txt), [kernel](kernel-previous-boot.txt),
[boot readback](boot-review.txt), [original failure](version-matrix-result02.json).

## Actual GStreamer package repair

The scoped ROCKNIX override enables tools (which builds the external scanner) and
keeps libgstcontroller in its post-install cleanup. The generic upstream recipe is
unchanged. The isolated build sources the actual feature recipe and build helpers,
uses a read-only accepted toolchain, compiles and installs the package, then applies
the old/new cleanup controls. Original cleanup removes the controller; the corrected
hook preserves it and /usr/lib/gstreamer-1.0/gst-plugin-scanner.

A fresh-registry VM control fails255 on original installed libraries with missing
controller/scanner warnings, then passes0 with the actual installed-new payload
and no plugin-loader warning. No LD_LIBRARY_PATH or GST_PLUGIN_SCANNER override is
used for that control. The scanner is too brief for the10ms process poll to observe;
we do not claim that poll caught it. Installed hashes and successful fresh discovery
are recorded. The subsequent current-engine browser run has no GStreamer warnings,
but memory is similar. This fixes a verified dependency failure, not #570.

[Inputs](gstreamer-inputs.json), [install controls](gstreamer-result.json),
[plugin controls](gstreamer-vm-proof.json), [result](gstreamer-plugin-result04.json).
Package lint and shell syntax pass. No ES source, copy, navigation or layout changed;
public sign-in frames exercise the unchanged presentation. #572 stays open until
next assembled-image clean/retained qualification verifies dependency closure.

## Exact conditions and retained failures

VM20 source1a026648442321609b2288c2c9c06803817f9df2, installed accepted app,
4Haswell CPUs,640x480 software graphics, ES resident, no guest swap. Normal ES renderer
suspension, phone input, navigation chains and authenticated usability were not tested.
The low-memory VM exposes791MiB, unlike the H700's974MiB; its kernel config reserves
256MiB CMA and lacks PSI. H700 config differs. Do not equate assigned RAM or this
reset with handheld behavior. Memory sampler instrumentation is kept separate;
Linux fastMallocStatistics returns peak RSS, so those labels cannot partition current
allocation. Kernel smaps PSS is the comparison measure.

2.54.0 was rebuilt from verified patched release source:36417 source files checked,
1623changed/4removed,2534Ninja steps,4jobs in a24GiB pinned builder, networking off.
The old package directory retains the cache's2.54.1 name only to satisfy absolute
build paths; runtime API reports2.54.0 and mapped libraries/helper hashes bind it.
Source archives, commands and immutable-cache sentinels are retained. 2.52.6 has
only been inspected as source; it has NOT been built or run. No product pin changed.

Public text log copies normalize terminal line endings, ANSI colors and trailing
whitespace; [normalization hashes](text-normalization.json) bind the unchanged
originals retained in the task owner.

[All original channels and actual exits](channels.json) retain the unsupported--qa
submission, initial GStreamer fixture error, bundle guard failure, aborted dependency
wait and subsequent failed prerequisite owners. No failed owner was rewritten or
replayed. All test owners are terminal. [Retirement](retirement.json) verifies no
browser/mount remains, QEMU exit, and removal of the disk, UEFI and temporary keys
(about2.5GB allocated). Small package runtimes/build inputs remain for the next
immediate engine-boundary test. No background build/test is running.

Next: test the earlier2.52.6 compositor boundary with explicit configuration controls;
exercise normal ES handoff/navigation/input/recovery at measured guest-visible limits;
then qualify #572 in the next image. #570 remains unresolved and no RC is ready.
