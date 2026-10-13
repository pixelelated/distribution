# Saved Session State

> **Saved**: 2026-10-13T01:35:34.485496+00:00
> **Branch**: feature/m7-player-setup
> **Repo**: pixelelated/distribution

## Start here

pixelelated is an immutable handheld Linux distribution. Read next's AGENTS.md,
every-session rules and device-testing-policy, then M7's live milestone body.
Harness conflict-resolution is stale; leave it alone. Main /workspace/repos/rocknix
stays on next; active /workspace/repos/rocknix.worktrees/m7-player-setup is
feature/m7-player-setup. Starting published source was d4f0ed282411e113995789b8eae5d6a0de2c693c.
New rule commit5edc91060c54d805df214326b404e4bff40385ae is integrated locally.
This checkpoint and package/evidence commit are being prepared for guarded delivery.
Read delivery01 actual results before any retry; prepared does not mean published.

This session implemented the owner's required upstream troubleshooting check
(#573, D-WORKFLOW-162), rebuilt WebKit2.54.0 for comparison, repaired #572's scoped
GStreamer recipe and tested the actual install. #570 memory pressure is NOT FIXED.
No full firmware, physical-device/cloud action, external audit or production WebKit
pin change. All build/test owners ended; QEMU, disk, UEFI and temporary keys retired.
No test is left running. Package runtimes/build inputs remain for the immediate
next version-boundary test; do not retain obsolete VM disks.

## Current focus and findings

1. Latest published WebKit stable remains2.54.1 on October13. Inspected upstream
   bugs319590/305401/306430/268477. Font-variation fix is already in both2.54.0 and
   2.54.1; X11/DMA-BUF follow-up is not established for our Wayland/disabled-DMA-BUF
   app. Dated links/source hashes are in the new packet. New engineering rule
   requires early upstream issue/release/fix checks, pin/patch identification,
   fix-presence verification and explicit applicability limits. AGENTS/CLAUDE
   parity, rules/register/package checks pass. #573 closes after verified push.
2. 2.54.0 package build completed00:58:25UTC,2534Ninja edges, source verified and
   original cache mounted read-only. Initial loaded120s public page reaches390MiB
   PSS versus381MiB on2.54.1. Original matrix FAILED its bundle-path assertion after
   measurement; preserve its rc1. Fixed repeated1024MiB matrix then stalled before
   load on both engines. Lower PSS on those uncompleted pages is NOT improvement.
   Guest unexpectedly reset01:11:15UTC during fourth2.54.0 trial; host timeout later.
   Direct reclaim/file refaults/allocation stalls surged. No OOM/panic/pstore cause
   established; a15s watchdog was configured, involvement unproved. Host had37GiB
   available. Do not assert this is exactly the owner's physical crash.
3. Planned restart with2048MiB permits both engines and corrected-GStreamer browser
   runs to load. Three90s trials pass load/two frames/boot/teardown and show zero
   direct reclaim. Peak browser PSS581/561/568MiB; these are one ordered sample each,
   not statistical comparisons or handheld-capacity proof. New measure02 streams
   samples and rejects unloaded pages. Original sampler's duration-only guard was
   insufficient. Optional schedstat read invalidated resource-snapshot process
   rows; empty rows are not process absence. Principal smaps samples remain valid.
4. #572 recipe enables tools (scanner) and preserves libgstcontroller. Actual
   package build/install old/new cleanup controls pass; fresh-registry original255
   versus corrected0, no scanner-path override. Corrected browser has no GStreamer
   warnings but similar memory. Final assembled-image dependency/clean/retained
   qualification remains open. No ES source/copy/navigation/layout change.

## Evidence and lifecycle

Public compact packet: docs/qa-logs/2026-10-13-webkit-versions/README.md,
manifest, source/runtime hashes, trials/samples, reviewed native640x480 frames,
previous boot logs, failure results, original channels and retirement receipt.
Private owner: /workspace/tmp/pixelelated-webkit-versions-20261013/.

Build WT /workspace/repos/rocknix.worktrees/m7-webkit-versions-570 remains clean
on build/m7-webkit-versions-570 atd4f0ed2824. It owns package build watcher only,
not product source. ROOT/package-2.54.0 and source-2.54.0, runtime-2.54.0 tar/manifest,
gst02/installed-new and actual recipe/build fixtures remain. Cached directory
still sayswebkitgtk-2.54.1 for absolute build paths; verified source/runtime is2.54.0.
Source2.52.6 archive was inspected but NOT BUILT OR RUN. Compare configuration
before using it: older recipe had GTK3/GStreamerGL off; current requires GL/video.
2.54.0 was isolated with current dependencies/options; no production downgrade.

All15 original launcher channels/build/wrapper/actual process exits are recorded,
including failures. headroom-owner ended0 at01:29:58UTC; retirement-owner ended0
at01:30:34UTC, guest mount/browser readback clean and2,497,298,432allocated bytes
retired. No VM pid/disk/key remains; recreate in a fresh owner for further tests.
Do not rerun boot.py on an existing artifact. Failed gst vm-owner waits never
injected payload; plugin-owner04 and headroom-owner supply real package proof.

1024MiB assigned guest exposes810368KiB;2048MiB exposes1840256KiB. FourHaswell CPUs,
softwaregraphics640x480, ES resident, no swap/PSI. VM kernel CMA256MiB differs from
H700 config/physical memory. Direct launch with --no-auto-keyboard does not exercise
normal ES renderer suspension, navigation, phone input or authenticated sign-in.
Do not infer input responsiveness from a loaded frame or use memory-sampler peak
RSS labels as allocator partitioning; use kernel PSS.

## Record delivery

Owner /workspace/tmp/pixelelated-webkit-versions-20261013/delivery01/ is prepared.
Read result.json, launcher-result.json, tool-wrapper.rc, recorded build.rc,
head.txt and hosted-checks.json plus remote/git readback before any retry.
The intended operation is an authorized commit, fast-forward next and guarded
push, followed by both exact-head record/wordlist hosted checks. No success is
implied here. The fresh-context session-stash reviewer receipt lives there.
Previous October12 browser-isolation delivery02 completed atd4f0ed2824; don't replay.

## Next commands and ordered work

1. If delivery01 is still prepared, commit the reviewed feature source/evidence
   with Refs #570, #572, #573 first; publish.py requires a clean feature tree and
   does not create the commit. Submit the prepared delivery through watch-build-submit.
   If already submitted, consume its original channels and do not replay.
   Close #573 only after published head/checks verification.
   #570 stays unresolved; #572 stays open for final assembled-image closure.
2. #570: next discrimination is a2.52.6 boundary control with documented options,
   plus normal ES handoff/navigation/input/recovery at measured guest-visible
   limits. Assess VM CMA/headroom differences before assigning a platform cause.
   Preserve all uncompleted-page/reset evidence. No physical facts are needed to
   begin these; existing WebKit device authority stays limited to its named scope.
3. #572 source is package-qualified; next full build must verify installed scanner
   and controller plus fresh-registry/browser/clean/retained closure. Do not call
   injected standalone package proof an accepted new SYSTEM image. Keep fixed
   recipe before freezing the next candidate. No new full cache before #493 gate.
4. Continue #565: implement and prove an executable artifact credential gate;
   tools/fork-publish-release currently only prepares a release plan and lists
   credential inspection as still owed. Old rule prose describing its retired
   uploader is not executable proof. Preserve no-values reporting and synthetic
   negative controls; inspect final payload bytes. Add a disposable retained-
   account upgrade proof, without real account requests. Original Nova RA
   authorship remains unknown; existing private preservation receipts suffice
   to show unchanged owner state, not clean defaults.
5. #566: provider-supported dedicated pixelelated ScreenScraper identity.
   Official webapi2 page says developers request access through its forum.
   Public/shared JELOS credentials are not evidence of redistribution rights.
   Prepare a concrete request before seeking permission to contact anyone.
   Compiled-pair precedence already hides runtime developer rows; keep player
   accounts separate, backup exclusion and release gating. No provider outreach
   or credential embedding is authorized by merely filing the issue.
6. #567: conditional advance notice on UPDATE GAMELISTS that offline achievement
   preparation follows, only when the actual enabled/account/index gates apply.
   GuiMenu.cpp around8440 currently has only REALLY UPDATE GAMELISTS?. Inspect
   SystemData/ViewController actual gating. Update EN/FR canonical flow and
   source-bound640x480/1280x800 frames before promotion. #568 final-game versus
   finishing phase remains future work.
7. #571 follows those owner-ordered items before a new candidate: compact
   header in cloud_oauth REMOTE_PAGE (around958), phone_page translations near106,
   probe/poll around1257. Keep reachable/loading separate from field readiness;
   queued typing must not be sent into an unfocused page. Verify navigation,
   genuine failure/reconnect/session end, long headings, EN/FR narrow/wide
   actual browser frames and unchanged pointer/input. Existing Node controls
   are in tools/last-good-scripts-test C4 near6126; preserve their meaningful
   assertions when DOM markup changes. /home/max/.cache/ms-playwright has
   chromium1223; Playwright is in the uv cache, not global Python.
8. Repair #564 on isolated feature/m7-rocknix-20261001 before its source merge.
   #493 mandatory retention/capacity enforcement precedes ANY new full cache
   copy/build. Then freeze repaired source, clean/retained GENERIC_X64, full
   protocols/time-to-play/independent review, H700 then SM8550, and #528/#344
   publication/source/custody gates. No public RC has been allocated.

## Exact source, tooling and retained project context

Accepted devices bc9dfe8141d9561dc1d8502313d00a84c4566ee8, ES
c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78, rclone1.75.2. VM20 source
1a026648442321609b2288c2c9c06803817f9df2. Accepted artifacts/toolchain at
/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20; frozen cache mounts
read-only at /workspace/repos/rocknix.worktrees/m7-pixelelated inside Docker.
Pinned builder ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39.
No accepted cache mutation or full copy. Host2.8TiB available at01:30UTC.

Shell needs require_escalated because stale sandbox's /tmp quota fails and active
paths are outside its writable root. Set TMPDIR=/workspace/tmp/pixelelated-webkit-versions-20261013/tmp
for tools/hooks. tools/watch-build-submit requires an EXISTING fresh owner dir.
Use --owner OWNER -- --activity-dir OWNER -- COMMAND; no --qa or --mode flag.
One watched job per worktree, frozen scripts, original channels and actual exits.
No off-session notifications; actively supervise every submitted long job.

ES /home/max/Development/emulationstation-next remains old67f92692c3; create a
feature worktree from acceptedc8dc72cf9e before editing. ApiSystem.cpp launchCloudSignIn
opens browser then suspends renderer; Window::deinit unloads resources/renderer,
not the full database. Normal handoff is still unmeasured in this incident.

M7 live order remains #570/#572 → #565 → #566 → #567 → #571 → #564 stable20261001
repair → #493 lifecycle enforcement → new-source VM/audit → H700 then SM8550 →
#528/#344 publication gates. Isolated feature/m7-rocknix-20261001 at62e9929fdce5d44ceb7f68150770475c568d1ac2
containsf370dc8787 and #564 Steam defect; do not merge it before repair. Chosen stable
basec445081a59518f37d9776e5412dd7b14910696f7, D-WORKFLOW-161. No public RC allocated.

#493 cleanup batches are complete; don't replay. Required6.855GB custody at
/workspace/artifacts/pixelelated-build-custody/issue-493-oldtrees-20261012-03 stays.
Automatic retention/capacity enforcement still required before full builds.
Prior owner-device/account evidence stays private in October12 task roots;
#569 diagnosis published/closed, original Nova sign-in authorship unknown.
RG SP Tailnet100.75.221.73 (SSHalias needs override); Nova100.84.232.105. Any physical
mutations use device-act with applicable named authority. This session made none.
#558/#561 watch items, #562/#568 future; no external audit running.

Previous checkpoint: archived/saved-session-state-next-20261013T013534Z.md
