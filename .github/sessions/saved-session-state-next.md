# Saved Session State

> **Saved**: 2026-10-13T03:25:05.105383+00:00
> **Branch**: feature/m7-player-setup
> **Repo**: pixelelated/distribution

## Start here

pixelelated is an immutable Linux gaming distribution. Read next's AGENTS.md,
every-session rules, docs/device-testing-policy.md, and M7's live milestone body.
Harness conflict-resolution is stale; leave it alone. Main /workspace/repos/rocknix
stays on next; active /workspace/repos/rocknix.worktrees/m7-player-setup is
feature/m7-player-setup. Starting published source is d29d0781ecb416ed8d51323b1fa2c3237755b8ff.
Prior browser-stack delivery01 is COMPLETE: result/launcher/wrapper/build0, owners
exited, clean checkouts and successful exact-head hosted checks. Do not replay it.
This historical-performance record has its separate delivery01 below; check actual
result channels before retrying or describing it as published.

## Current Focus

#570 browser pressure remains unresolved. The owner asks whether earlier speed
optimizations were lost, phone control adds overhead, or indirect stack changes
explain the slowdown. Historical review and a small synchronous host JavaScript
control are COMPLETE. No product/ES/device change, VM, firmware build or audit ran.
No diagnostic process remains active. The next runtime test is normal ES handoff
with separate no-phone, idle-phone and active-phone controls, not an owner login.

## Completed This Session

- NEW docs/qa-logs/2026-10-13-browser-history/ binds the timeline, source hashes,
  actual old/current phone-page JS and deferred-fetch controls. Both controls
  and a fresh-path replay pass. These are stub transport/DOM semantics, NOT
  measured browser/device latency. Old nesting/mirroring is gone; ES teardown,
  flat pointer/fractional carry and movement coalescing remain. October11 common
  input queue delays movement behind typing responses, while preserving the
  move-before-click fix; do not revert it blindly. The2s phone poll reads state
  files; the500ms in-page focus evaluation runs with either keyboard choice.
- August30 commit reports150s→2s after removing nesting, but it is historical
  timing without a reproducible current-content baseline. Native proxy arrives
  September13, after that early browser work. Current76–105MiB footprint is a
  changed stack cost, not dated proof against the owner's unknown last-fast build.
- #570 request quoted at issuecomment-6137434751. Full issue and M7 order remain;
  runtime usability/repair stays open. Independent zero-context reviewer spawn
  again hit the thread limit. Existing m7_owner_feedback_handoff completed a repository-led independent review: hashes and fresh replay pass; corrected the handset-change date to October1. See delivery01/handoff-review.md. This is reused context, not fresh zero-context.

Prior completed browser-stack work (not rerun this turn):

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

1. Deliver this record through the fresh owner
   /workspace/tmp/pixelelated-browser-history-20261013/delivery01/. publish.py
   requires a clean committed feature, fast-forwards clean next, guarded-pushes
   and waits for exact-head record/wordlist checks. Read result.json,
   launcher-result.json, tool-wrapper.rc, build.rc, consumption.json and remote
   HEAD before retrying. Prior /workspace/tmp/pixelelated-browser-stack-20261013/
   delivery01 is finished and must NOT run again. No test is pending in background.
2. #570 next controls are in browser-history/README.md: same fixed synthetic page,
   same viewport/keyboard policy through normal ES launch; no phone client, idle
   phone polling, then scripted typing/drag/navigation. Record issued/acknowledged/
   visibly-applied input, heartbeat, CPU/PSS/kernel/refaults, ES startup overlap and
   return/recovery. Repeat reordered with settled baselines and bind frames/source.
   Actual phone presence differs from --phone, which suppresses automatic OSK.
   No owner credentials, cloud or proxy restart needed. VM question is recorded in
   #570; add exact fixture criteria before the next runtime job. No VM retained.
   Then isolate focus-probe pacing and proxy/service load with synthetic data.
   Current eval timer has no outstanding-request guard, but runtime backlog is not
   proved. Preserve focus readiness, input ordering and completion. Proxy startup/
   reconnect can flush awards; use synthetic queue/DB data and listener readiness.
   Existing emulators only check8080/fall back direct, not on-demand service start.
   Read browser-stack/proxy-lifecycle.md before any lifecycle proposal. No selected
   optimization or proxy suspension; SIGSTOP does not reclaim resident memory.
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

- docs/qa-logs/2026-10-13-browser-history/: timeline, source manifest, original
  host control results and reproducible small fixtures. No product source change.
- Dated October13 work log, index, friction log and this archived checkpoint.

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

Previous checkpoint: archived/saved-session-state-next-20261013T032505Z.md
