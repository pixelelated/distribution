# Saved Session State

> **Saved**: 2026-10-13T02:25:23.841583+00:00
> **Branch**: feature/m7-player-setup
> **Repo**: pixelelated/distribution

## Start here

pixelelated is an immutable Linux gaming distribution. Read next's AGENTS.md,
every-session rules, docs/device-testing-policy.md, and M7's live milestone body.
Harness conflict-resolution is stale; leave it alone. Main /workspace/repos/rocknix
stays on next; active /workspace/repos/rocknix.worktrees/m7-player-setup is
feature/m7-player-setup. Starting published source2292e9a2983227a62aaf7846a5b739c41b0841a7
and its delivery01 are COMPLETE with successful exact-head checks; #573 is closed.
Do not replay the older delivery. This new packet/authorization checkpoint is being
prepared for the separate browser-stack delivery01 below; read actual channels.

## Current Focus

#570 browser pressure remains unresolved. The owner asked about ES/background
services and actual GPU usage, then designated the separate RG35XX SP as the
browser bench (D-QA-060), protecting saves and other owner data. We completed
source review, full idle census and eight bounded physical rendering controls.
No product code/pin/permanent setting or firmware changed. No browser test is
running; all three owners and their device units exited, temporary state retired.

## Completed This Session

- docs/qa-logs/2026-10-13-browser-stack/ binds source review, sanitized numeric
  samples, exact fixtures, eight outcomes, five reviewed native640x480 frames,
  original owner channels and hash-verified retirement. Read README + trials first;
  samples is a large compact JSON array, do not dump it into context.
- D-QA-060 and device policy retain explicit browser bench authorization. The
  RG35XX SP is100.74.205.40, model Anbernic RG35XX SP, H700/DDR4; the separate
  RG SP100.75.221.73 is OFF. Old SSHalias rg35xxsp defaults to LAN; use explicit
  Hostname for the intended device. Nova100.84.232.105 is unrelated to this test.
- Normal ES sign-in keeps the process/database, unloads renderer/input/audio
  after cloud_oauth open and restores them after wait. open confirms process
  existence, not a ready frame. Direct diagnostic launches bypass this handoff.
- Actual WebKit2.54.1 source gates browser hardware acceleration off when
  WEBKIT_DISABLE_DMABUF_RENDERER=1, our deliberate #228/D-WORKFLOW-048 default.
  Previous virgl VM kept that flag, so it was not a browser-acceleration comparison.
- Bench idle:974.7MiB visible,32MiB CMA,no swap,556.1MiB available. RAOfflineProxy
  ~105MiB PSS, ES102, Tailscale43, Sway26; service cgroups identify the Python proxy.
  This is resident overhead, not a diagnosed leak. Proxy/ES fall to~76MiB under
  pressure as file-backed pages are reclaimed. Panfrost is bound.
- Simple-page off/on both load, peak133.65/163.70MiB PSS. Accelerated WebKit page
  process acquires real Panfrost DRM buffers; disabled page process has no DRM
  client (GTK parent may still use one). Do not double-count DRM buffers and PSS.
- Public controls: first off loads then guard-stops; first on and both owner02
  repeats end BEFORE load. PSI-only guard can fire with429–520MiB available.
  Original failures/incompletes are retained. Final owner03 requires settled
  baselines, pairs PSI>5 with available<256MiB and keeps the160MiB sampled cutoff,
  adds vmstat/faults and a loaded-page capture. Both public paths now load but
  still hit guards, on25.5s/off46.7s. Peaks373.46/483.27MiB are CENSORED and not a
  renderer efficiency ranking. Cookie banner/content timing also differs.
- Final on/off file refault deltas13283/33415, direct scans3020/666, allocation
  stalls42/1. Reclaim occurred; root cause remains unknown. No crash/reset; same
  boot/frontend/proxy/compositor PIDs. Final546.7MiB available after cleanup.
  No game, save-writing operation, owner config/credential edit, authenticated
  sign-in/cloud action, firmware transfer or reboot. Save bytes were not inventoried
  in this experiment; do not claim a full save-hash proof.

## In Progress and Next Steps

1. Deliver the reviewed record through
   /workspace/tmp/pixelelated-browser-stack-20261013/delivery01/. publish.py requires
   a clean feature commit, fast-forwards clean next, guarded-pushes and checks
   both exact-head record/wordlist runs. It does not create the commit. Read
   result.json, launcher-result.json, tool-wrapper.rc, recorded build.rc and
   consumption.json/remote/checkouts before retrying; prepared is not published.
   No test is left running while preparing this delivery. A new zero-context reviewer could not be spawned
   because the session thread limit was reached; an existing reviewer without
   this browser-session briefing is performing a repository-led independent
   handoff review. Read delivery01/handoff-review.md; do not call it a newly
   spawned zero-context review. All issues570/572 remain open.
2. #570 next: VM normal ES→browser handoff, startup overlap, navigation/input,
   return/repeated lifecycle with complete process/kernel/GPU accounting and
   loaded-frame/latency/recovery criteria. Existing direct-launch figures do not
   quantify normal resource teardown. Extend the fixture with VM provisioning;
   no VM is retained from prior runs. Count observer overhead. Use settled
   baselines and retain truncated/incomplete pages, not a low-PSS success label.
   Include the owner's proxy-lifecycle question: proxy-lifecycle.md traces boot
   always-on,15s reconnect/startup award flush,60s optional cache/folder workers,
   hour refresh and proxy-traffic-only idle. Browser has no dependency. Emulator
   launchers check listener/fall back direct, not on-demand start. No owner proxy
   stop/restart authorized by implication where it would send awards or mutate
   owner progress. VM-only synthetic queue/no-account tests should assess idle
   footprint or orderly browser-owned unload/restoration and readiness. SIGSTOP
   does not free memory. No optimization selected. Upstream head3958abce has four
   newer commits; no memory fix established; check fixed8080 assumptions on intake.
3. Then the isolated2.52.6 engine boundary with documented configuration changes.
   #572 corrected GStreamer recipe is already package/install/fresh-registry
   qualified in2292e9a298; final assembled-image closure remains open. The physical
   accepted browser still shows the known scanner/controller warnings. Do not
   reintroduce missing runtime pieces or claim they explain pressure: the earlier
   fixed-runtime VM control removed warnings without a memory reduction.
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


## Key Files Modified

- docs/device-testing-policy.md and docs/decision-register.md: D-QA-060 scope.
- docs/qa-logs/2026-10-13-browser-stack/: review, fixtures, numeric data, frames,
  original result/exit/retirement receipts and explicit comparison limitations.
- docs/work-logs/2026_10-work_logs/2026_10_13-work_log.md, INDEX and friction log.
- This canonical checkpoint and archived predecessor. No ES or product code change.

## Related Context and Notes for Next Session

Live M7 order: #570/#572 → #565 → #566 → #567 → #571 → #564 stable20261001 repair →
#493 lifecycle gate before a full cache/build → new-source VM/audit → H700 then
SM8550 → #528/#344 publication. No public RC allocated. #558/#561 are watch items;
#562/#568 future. No audit running. No provider/account operation is authorized
by the browser bench permission. Use tools/device-act for every device mutation.
Browser diagnostics/custom builds on the named RG35XX SP are authorized within
#570 without another approval question; protect saves/account configuration and
apply artifact/preservation qualification before any diagnostic firmware update.

Accepted device sourcebc9dfe8141d9561dc1d8502313d00a84c4566ee8, ES
c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78, rclone1.75.2. VM20 source
1a026648442321609b2288c2c9c06803817f9df2. Frozen current cache
/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20; container path
/workspace/repos/rocknix.worktrees/m7-pixelelated remains required for absolute
build files. Never mutate the accepted cache or hardlink a mutable copy.
Pinned builder ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39.

Older-engine WT /workspace/repos/rocknix.worktrees/m7-webkit-versions-570 is clean
build/m7-webkit-versions-570 atd4f0ed2824. Package2.54.0/source/runtime and corrected
GStreamer fixtures remain in /workspace/tmp/pixelelated-webkit-versions-20261013
for the immediate next engine control.2.52.6 source inspected, NOT BUILT OR RUN.
1024MiB VM exposed810368KiB,256MiB CMA;2048 exposed1840256KiB. Prior low-memory
repeat reset during2.54.0 is unproved, original matrix rc1 retained. Headroom
trials loaded both2.54.0/2.54.1. No downgrade rationale. All15 old owners exited,
VM disks/keys retired; don't replay boot.py on an existing artifact.

Current private measurements: /workspace/tmp/pixelelated-browser-stack-20261013/.
bench-owner01/02/03 all launcher/wrapper/build rc0 and exited; consumption.json
records actual exits, not merely terminal watcher heartbeat. Device units have
ended. Three temporary device roots retired by hash-checked retire-bench.py;
retirement-result0 and final-census show same boot/frontend. Nothing needs stopping.
Raw logs/config/account data are not in the public packet; retain safe readers.
Shell needs require_escalated because the stale harness sandbox fails its /tmp
mount and active paths are outside its writable root. Set
TMPDIR=/workspace/tmp/pixelelated-webkit-versions-20261013/tmp for tools/hooks.
watch-build-submit needs an existing fresh owner and -- --activity-dir OWNER --
COMMAND. No off-session alert exists; actively consume all owners and announce
completion. Do not leave a long job between turns without its verified supervisor.

ES /home/max/Development/emulationstation-next is an old checkout; inspect accepted
c8dc72cf9e with git show and make an isolated feature worktree before editing.
#564 isolated feature/m7-rocknix-20261001 has the Steam defect; repair before merge.
Chosen upstream stablec445081a59518f37d9776e5412dd7b14910696f7 (D-WORKFLOW-161).
#493 prior cleanup completed; don't replay. Required custody6.855GB at
/workspace/artifacts/pixelelated-build-custody/issue-493-oldtrees-20261012-03 stays.
Prior identity/copy/menu/audit decisions and provider-baseline requirements remain.

Previous checkpoint: archived/saved-session-state-next-20261013T022523Z.md
