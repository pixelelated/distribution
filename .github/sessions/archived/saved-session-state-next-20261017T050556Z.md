# Saved Session State

> **Saved:** 2026-10-17T04:18:16Z
> **Branch:** `feature/m7-audit-integration-603`
> **Repository:** `pixelelated/distribution`; integration branch `next`
> **Request:** Investigate browser memory/responsiveness; prioritize GTK4 among engine-migration experiments, retain Blink fallback and provider attribution.

## Start here

pixelelated is an immutable Linux distribution for handheld gaming devices, built
by cross-compiling complete OS images. There is no application development server.
The release target is 0.0.1; the current engineering image is private owner testing,
not a designated public RC. The OS name and cloud default are lowercase
`pixelelated` and `/pixelelated`; preserve existing selected paths and credentials.

1. Read current `next:AGENTS.md`, its every-session `.claude/rules/` files, and
   scoped rules before touching their paths. Read the `session-resume` skill.
2. Read this checkpoint, the [live M7 ordered plan](https://github.com/pixelelated/distribution/milestone/7),
   `docs/releases/next-candidate-work.md` and active issues #616/#576/#617/#587/#615. Historical
   queues in archived checkpoints are not the current plan.
3. Read `docs/qa-logs/2026-10-16-browser-headroom-587/README.md`, `analysis.json`,
   `originals/busy-stop.json`, `originals/recovery.json` and run `verify.py`.
   Then read the earlier #615 physical packet for the still-inconclusive loaded-page
   question. Portable #614 is complete; do not repeat its accepted controls.
4. Use `/workspace/repos/rocknix.worktrees/m7-player-setup` on
   `feature/m7-audit-integration-603` for coordinator edits. The primary checkout
   `/workspace/repos/rocknix` stays on `next`. The harness checkout
   `/workspace/repos/rocknix.worktrees/conflict-resolution` is stale and stays
   untouched; do not merge its unrelated history. Verify rules with
   `git diff --quiet next -- .claude CLAUDE.md AGENTS.md`.

GitHub developer identity is `blitterbot`; maintainer is `rasteratops`.
Use configured `gh` authentication and existing SSH configuration; never print
credential values. Private inventories, signed streams and personal captures stay
outside Git. Device read output must exclude `key|pass|token|user|psk` lines.
`docs/device-testing-policy.md` and `tools/device-act` govern named device actions.

## Current focus and completed October17 work

D-WORKFLOW-170 schedules independent GTK4/Blink source work alongside #616.
The latest owner steering identifies GTK4 as the likely smaller migration. #576
and the live M7 body now put **GTK4 first among engine-migration builds**, with
#617 Blink as a prepared fallback. Production adoption is unselected. #616's
actual-provider comparison remains current; #587 safe service-stop and #615
physical loaded-page recovery remain unresolved. No new runtime is active.

Current WebKit is2.54.1 with GTK3/API4.1, already using Skia for page painting.
GTK4's exact-source opportunity is previous-texture/damage-region handling in
WebKit's GTK presentation path. Neither toolkit nor engine alternative has a
measured H700 improvement. Upstream Pi4 compositor benchmarks are not a GTK3/4
comparison. Read docs/qa-logs/2026-10-17-browser-rendering-options/README.md.

Completed source packets (only these commits were cherry-picked from divergent
worker branches; unrelated history stays separate):

- 0d05ce9e60: docs/qa-logs/2026-10-17-gtk4-spike/ contains six dependency/engine
  overlay recipes, preserved product patches, native-input probe and verifier.
  All static checks pass. Graphene/GTK4/WebKit6 compilation and runtime UNRUN.
- 4dd24cd038: docs/qa-logs/2026-10-17-blink-feasibility/ contains a pinned CEF
  Views probe and synthetic fixture. CEF sample cefclient forces X11; use the
  prepared cefsimple direction. SDK ABI and non-root sandbox remain unverified.
  No SDK download, compile or runtime. Blink is a fallback, not a selected port.
- docs/qa-logs/2026-10-17-browser-controls-616/ is the exact-source diagnostic
  helper overlay. Runtime UA and observer controls need no OS-image rebuild.
  Both tiny GENERIC/H700 binaries compile;12 actual target-library parser cases
  pass. See browser-controls-build-616/ for original results. H700 unexecuted.
- docs/qa-logs/2026-10-17-browser-controls-results-616/ retains four VM attempts.
  Attempt1 inherited a1MiB file limit and browser exited SIGXFSZ(-25); the exact
  backing file is unknown. Attempts2/3 rendered the page but DOM report failed
  validation; attempt3 proves matching Origin then schema refusal. Attempt4
  waits for an animation frame/positive geometry and passes all6 cases in31.386s.
  Fixed content viewport640x457/DPR1; actual mobile/default versus desktop UA
  hashes differ, HTTP/DOM match, observer toggles and clean/blocked/hidden controls
  pass. No pressure guard; min408348KiB available; frontend restored.8 reviewed
  frames include the2 earlier failures. Earlier rejected geometry was not recorded:
  do not claim that zero-size geometry was historically proved.

This is direct diagnostic launch, not normal broker/ES handoff or provider,
trusted typing, performance or GPU qualification. The fixture's inherited caption
says no network; the adapted companion sends bounded loopback measurements. This
caption mismatch is documented in frame-review.json and is not product UI.
The full JavaScript sampling profiler is disabled in the current engine recipe.

Herdr w4:p7/p8 failed login refresh before work. Internal active-session agents
completed the three disjoint source packets instead; do not describe those Herdr
workers as running. No authentication settings changed. All workers are done.
The coordinator owns tracker/shared records and runtime admission.

## Previous completed headroom experiment and publication

- D-RA-048 promotes #587 into current M7.P5 beside #615. The owner's verbatim
  request and each VM-first plan are in #587; M7 current/next order is updated.
- Four installed-browser runs pass in active/stopped/stopped/active order on
  unchanged077197/ES16dbac. Available-memory medians233.34/259.07/258.01/231.20MiB;
  difference of condition mean medians26.27MiB. Actual synthetic proxy PSS22–24MiB.
  Observer7.7–7.9MiB measured; PSI unavailable. No guard/OOM; four reviewed loaded
  and four reviewed return frames. Normal queue/cache/account/config preservation
  passes, with service restarts1.035/1.037s.
- Separate slow-response initial-flush control reproduces Result=timeout/status9
  at15.062s even though systemctl stop returns0. Both signed awards and SQLite
  survive this case. Immediate-success synthetic peer recovery is ready1.041s,
  queue empty by3.841s. No real server acknowledgement/idempotency proof.
- Original failed admission125 and first no-NIC loopback8080 collision remain
  fixture failures, not product-memory failures. All successful allocation result
  channels0, guest/observer/matrix exited; admission consumed.2,412,744,704bytes
  of owned disk/OVMF retired. No physical device or cloud operation.
- Exact evidence, original archive, offline analysis/verifier, executed fixtures
  and reviewed frames: `docs/qa-logs/2026-10-16-browser-headroom-587/`.
- Previous publicationffd13eabcd128f8a0410ea6e9f9ab58afa7331cb is verified on both
  ordinary refs with CI passed. This session's evidence/record commit follows it;
  inspect Git and `/tmp/pix-m7-browser-headroom-20261016-01` publication receipts.
  No product source, ES pin or firmware changed.

## Physical #615 results and limits

| Attempt | Observed result | Limitation |
| --- | --- | --- |
| Early Escape at about 18s | Kernel key down/up, natural focus; browser gone by the 2s observation; same ES focus returns, no guard | Page still opening. Controller later fails1 on duplicate timestamp logging; not whole-run PASS. No GTK key-consumption log. |
| Longer attempt, Escape planned 42s | Pressure guard terminates browser at 35.65956s, before Escape; observer1/controller1 | At intervention 190476KiB available, PSI some8.67/full8.21 avg10; minimum184340KiB. No loaded-page screenshot, no OOM/kernel error. |
| Normal close at 25s | Installed close returns0 in 2.211632358s; controller0/observer0, no guard; same ES focus | Provider content still blank. Frame after explicit3s post-close wait is black; later cancel/carousel render. Visual recovery latency unmeasured. |

Later pressure during recovery reached PSI some26.09/full20.81 avg10. Monitor and
controller overhead was not separately measured, so attributing the entire rise
to WebKit, a script, proxy or GPU is unsupported. Round02 also changed observer
lifetime240→600s, input18→42s and fallback assertion55→65s; round03 restored240s
and used normal close25s. Browser90s and pressure guards were unchanged. No fourth
trial. The earlier physical90s `INCOMPLETE_TIME_LIMIT` remains unchanged.

All **163 protected files / 25,549,175 bytes**, selected settings, credentials,
paths, modes, recovery records and hooks were unchanged. Autosync remains off.
Same last-observed boot `067a27f1-143d-4fe8-83cd-937560a5c87b`, ES2696/start5810,
Sway2533/start5399. No game, auth, cloud transfer, reboot or update occurred.
Final physical readback found no browser/WebKit/OAuth/rclone/test keyboard or
failed unit; 570156KiB (556.8MiB) available and rendered carousel. These are the
last test observations, not a fresh device connection at stash time.

All six test services exited. After exact export/hash checks, 33 owned files and
`/tmp/pix-qa615`, `/tmp/pix-qa61502`, `/tmp/pix-qa61503` were removed. The targeted
reset-failed returned1 for absent transient units; independent failed-unit check
passed. Preserve that distinction. Private originals/helper receipts remain at
`/tmp/pix-m7-h700-exit-repro-20261016-01`, including an incidental read-only
achievements screen: do not publish the entire directory or personal inventories.

Upstream review is in `upstream.md`: selected Sway1.11, libinput1.26.2,
WebKitGTK2.54.1; no verified matching fix found in the checked sources. The old
Sway#5423 USB/input report is not a match for the virtual keyboard evidence.

## In progress and next steps

The milestone body is the ordered plan. The following is its current handoff:

1. **#616 with #576 GTK4 first and #617 fallback:** no active producer remains.
   For GTK4, read the new packet and run its static verify.py; prepare a fresh
   dedicated build/* checkout and isolated writable sysroot rooted in current
   product bytes. Preserve accepted GTK3 caches. Inspect actual resolved paths,
   stamps and container mounts before admission; do not clone an entire build
   tree. First allocation: Graphene1CPU/2GiB/2GiB/10min provisional ceiling;
   then GTK4/sandbox dependencies; WebKit6 is a separate heavy compile. These are
   proposals, not allocations. Read README for exact command and caveats.
   In parallel continue #616's source-bound account-free light/Dropbox/Drive/
   OneDrive matrix using the now functional UA/observer helper. A new runtime
   needs fresh admission/owner, actual provider-error exclusions, normal broker
   handoff, observer-off control and input readiness proof. Existing no-NIC
   fixture is not a provider runner. Hold engine/viewport/service state fixed;
   vary RAM then UA separately. Sampling profiling may require an engine build.
   #587 atomic quiescence/bounded cancellation and queue/restart proofs are still
   required before production service suspension. H700 follows portable tests.
2. **#613:** next independent package task. Inspect upstream and exact package
   source, correct the unused `/etc` systems-config fallback link into build
   staging, then prove normal selected-storage precedence and fallback on the VM.
   Active installed mappings are accepted. Keep source/flow/evidence requirements.
3. **#607–610:** Steam registry, recovery identity, failed-RVZ retry, literal shell
   metadata assignments. Fix/qualify affected bytes before affected Nova deployment.
   #611 guidance is backlog. RG SP and Nova still retain the October11 `bc9d`
   baseline; no transfer is in progress. Do not repeat the RG35XX SP update.
4. **#528 public release work:** source/notices dispositions, independent retrieval,
   required backup custody, security/docs and public naming/publication requirements
   remain. Website #511/#605 and infrastructure are independent. D-WORKFLOW-168
   permits private owner testing without declaring this image a public RC.

Do not reopen completed #603/#606/#612 audit/qualification or replay accepted
matrices for cleaner paperwork. #603 reviewed frozen `cdd92`; the two-file ZeroTier
product delta to077197 has a separate focused local review, not a second external
review. Exact receipts: `docs/qa-logs/2026-10-15-post-audit-product-delta/`.

## Runtime state and resumption commands

No build, VM, browser, device diagnostic, external audit or deployment remains
active from this session. VM launcher/wrapper/build/command/monitor/runner/lifecycle
original channels are0; exact host/QEMU identities exited. Admission
9e38f30969c5454097c03354fd79a23e consumed;2,312,990,720 allocated bytes of its owned
VM disk/OVMF retired. Root evidence owner is
/workspace/tmp/pix-browser-controls-vm-20261017-01/export/.
Frozen run: m7-p5-build-20261015-03/.build-runs/20261017T040228Z-0fddbf18.
Compile admission261514b9d3fa44cdaef8b34cbe9f07fd also consumed, all owners exited;
run20261017T035952Z-4429942f. Tiny helpers remain only for queued immediate tests:
/workspace/tmp/pix-browser-controls-compile-20261017-01/out/.
GENERIC SHA530b0d2c7daf739eb061a415da4224a7affcec1b1837a452d182e97a03c16454;
H700 SHA9dad87a65f5415311d663448834aac1ae281212c931f12c3cc2afb8fbbd0f245.
Do not rerun consumed producers or replay old owners/ports.

The prior published base is f511766e17fb. This session integrates two source
packets and then saves evidence/records; inspect actual refs and CI before
claiming this checkpoint's publication. No product source, ES pin or firmware
changed. Private tracker receipts: /tmp/pix-m7-browser-parallel-20261017/.
No off-session notification mechanism is claimed.

Useful read-only checks from the coordinator:

```sh
git status --short --branch
git log -4 --oneline
git ls-remote origin refs/heads/next refs/heads/feature/m7-audit-integration-603
python3 -I docs/qa-logs/2026-10-17-gtk4-spike/verify.py --repo .
(cd docs/qa-logs/2026-10-17-browser-controls-results-616 && sha256sum -c SHA256SUMS)
gh api repos/pixelelated/distribution/milestones/7 --jq .description
gh issue view 576 --repo pixelelated/distribution
gh issue view 616 --repo pixelelated/distribution
```

Use tools/archaeology before declaring another issue new. New runtime uses fresh
admission/owner and tools/watch-build-submit/tools/watch-build; actively observe
at most60s intervals and announce actual completion. Never edit in-flight tools.
Host process checks require actual host context. No broad cleanup or process kill.

## Builds, devices and custody

Product source **077197e6cd3ea31f33b28aaf3882a694b3423b53**, ES
**16dbac5211eea7e70db7394372033be2be7df829** and timestamp **20261015T161744Z**
remain unchanged. Firmware: `0.0.1-dev+20261015T161744Z.g077197e6cd3e`.
GENERIC_X64, H700 and SM8550 builds/readers passed for this source. Build/source
readiness, image qualification, public RC designation and publication are separate.
GENERIC frozen checkout:
`/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-03` on
`build/m7-p5-20261015-03`. H700 and SM8550 native compact originals:
`docs/qa-logs/2026-10-15-zerotier-h700-refresh/` and
`docs/qa-logs/2026-10-15-zerotier-sm8550-refresh/`.

RG35XX SP is the H700 bench, distinct from RG SP. Strict known-host binding:
Hostname100.74.205.40, HostKeyAlias192.168.1.81, StrictHostKeyChecking=yes,
UserKnownHostsFile `/home/max/.ssh/known_hosts`, HostKeyAlgorithms=ssh-ed25519.
Its accepted transfer/reboot authorization is consumed. Saves/cloud/account state
is protected; browser bench authority does not authorize cloud data operations,
gameplay, repeated updates or reboots. Device availability must be checked anew.

Keep required source custody outside Git, not disposable VM retention:

- `/workspace/artifacts/pixelelated-release-sources/m7-delivery-source-20261015-01`:
  1,869 selected objects /12,516,737,444bytes plus metadata; manifest
  `dfbc11140c9f51d1a92572909e5404a7451df1d43a47a223827da1277e1bfb90`.
- `/workspace/artifacts/pixelelated-release-sources/m7-notice-delivery-20261015-01`:
  126 new files /2,059,815bytes plus metadata; manifest
  `aa373739d72621aa5033025644840be8f9456289ed9171194e200f616c7f9e2c`.
- Receipts: `docs/qa-logs/2026-10-15-source-delivery/`,
  `docs/qa-logs/2026-10-15-notice-delivery/`, and
  `docs/qa-logs/2026-10-15-current-source-mapping/`.
  Exact earlier source stores remain held; do not reacquire or rerun accepted
  producers. Local custody/readback is not independent off-host retrieval/backup.

The archived checkpoint below preserves build owners, admissions, original
failures, source maps, all earlier custody hashes and integration-citation history.
Source trees were unchanged by that history correction; no force push occurred.

## Pending requests and deferred observations

- ABL and MAME source-contact requests are **pending and unsent**. Exact drafts:
  `docs/qa-logs/2026-10-15-source-contact-drafts/`; private packet
  `/tmp/pix-m7-abl-mame-contact-options-20261015`. Do not send or duplicate the
  pending question. #585 future upstream contributions need their own scope.
- Root-only stopped-media read remains pending/nonblocking:
  `bash /tmp/pix-m7-stopped-media-root-readback-terminal-20261015/commands.sh`.
  It reads five stopped files, deletes nothing. Do not repeat the question or
  mistake it for cleanup clearance.
- Nova metadata's original writer remains unknown. September29 install retained
  storage; September30 empty restore/0B backup explain activity stamps, and
  pre-install play metadata explains Recent membership. #565 clean/retained
  controls are delivered; no personal reset is needed or authorized by this stash.
- #558 shutdown and #561 LED are watches. #587 and #576 GTK4 are current
  M7 work alongside #616/#617. #568 finalization wording, #562 integrity,
  #586 credentials and #560 fast shutdown remain backlog. Prior proxy target saving was only390KiB and not
  adopted; approximately78MiB ES handoff saving was VM evidence, not a provider cure.

## Key files and related context

| File | Change |
| --- | --- |
| `docs/qa-logs/2026-10-17-gtk4-spike/`, `2026-10-17-blink-feasibility/` | Source-only migration candidates; no engine compile/runtime |
| `docs/qa-logs/2026-10-17-browser-controls-616/`, `browser-controls-build-616/`, `browser-controls-vm-616/`, `browser-controls-results-616/` | Diagnostic source, actual compilation/parser proof, executed VM fixture and original outcomes |
| `docs/qa-logs/2026-10-17-browser-rendering-options/` | Primary-source graphics findings and parallel ownership |
| `docs/decision-register.md` | D-WORKFLOW-170 bounded parallel alternatives |
| `docs/releases/next-candidate-work.md`, `docs/vm-qa-log.md` | GTK4-first migration experiment, provider controls and limits |
| `docs/work-logs/2026_10-work_logs/2026_10_17-work_log.md`, `docs/friction-log.md` | Findings and preserved fixture failures |
| This checkpoint and branch pointer | Archived October16 state; refreshed current queue |

- Current flows: `docs/es-menu-map.md`, `docs/conflict-wizard-ia.md`. No product
  presentation changed; this packet records the exercised existing flow/frames.
- Release preparation: `docs/releases/0.0.1-release-preparation.md` and
  `docs/releases/0.0.1-release-note-draft.md`.
- #585 tracks a conditional upstream proxy cancellation/quiescence contribution;
  no patch or message sent. Fable/council remains optional, not an active audit
  or authorized prepared external transfer.

Ordinary scoped records, commits, pushes and tracker updates remain authorized.
Commit on the coordinator, fast-forward clean `next`, push both ordinary refs;
never force push or merge the stale harness. The required context-free handoff
review is performed on this prepared checkpoint before publication; its receipt
lives in the private preparation directory. No new physical, external transfer,
source-contact message or public release is authorized by this record.

Previous full checkpoint: [saved-session-state-next-20261017T041816Z.md](archived/saved-session-state-next-20261017T041816Z.md).
