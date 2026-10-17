# Saved Session State

> **Saved:** 2026-10-17T05:53:18Z
> **Branch:** `feature/m7-audit-integration-603`
> **Repository:** `pixelelated/distribution`; integration branch `next`
> **Request:** Continue M7 browser investigation and try another rclone provider login; Google Drive and Dropbox forms now observed, GTK4 engine/fixture compiled.

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

## Current focus and October17 completed experiments

D-WORKFLOW-170: #576 GTK4 is first among engine-migration experiments; #617 Blink
is fallback. #616 provider attribution remains parallel. No production engine,
UA, script filter or service-suspension policy is selected. WebKit2.54.1 GTK3/API4.1
already paints with Skia; GTK4 is not yet a measured H700 memory/speed improvement.
#587/#615 remain unresolved. **No build, VM, browser or audit job is active.**

**The requested second provider was exercised.** A fresh2GiB GENERIC VM used the
normal installed ES/rclone flow to open Google Drive and then Dropbox. Both
returned HTTP200 and painted sign-in forms, two reviewed frames each, with empty
fields. No credentials or consent were submitted. Local fixture also loaded.
Event probes were on, periodic observer off, default UA,640x457 content/DPR1.
This is functional launch/cancel/recovery proof, not a completed account link,
trusted-input proof or fair performance/memory ranking. The engine compilation
overlapped and durations differed. Whole-guest MemAvailable is not browser PSS.
Public exact-source evidence:
`docs/qa-logs/2026-10-17-provider-functional-616/` and
`docs/qa-logs/2026-10-17-provider-instrumentation-616/`.

All three browser cases closed normally with no guard interventions or survivors;
same ES PID1645/start1146, idle200, original browser and missing-rclone-directory
state restored. Original VM/watcher/runner/launcher0; admission41d3a0c1 consumed.
Owned disk/OVMF2,322,104,320allocated bytes retired after evidence export. Private
raw logs/full argv/request/PIN/QR frames stay in the owner, outside Git:
`/workspace/tmp/pix-provider616-vm-20261017-01`.
Do not publish that whole directory. The expired calibration service stop returned5;
its original natural240s expiry remains separate, not a rewritten zero.

The local native-input fixture refused before POST because the product excludes
loopback URLs from its page marker. **Input remains UNPROVEN.** Source-only v2
uses exact listener/helper/guard ownership and a fresh server-owner receipt;
it is in the functional packet under sources/v2-unrun and has not executed.
Normal phone-instruction navigation initially kept list focus: UP then RIGHT,
review filled CONTINUE, then X. Initial false starts had no callback or browser;
they are not handoff defects. Both saved Google frames contain the form.

The diagnostic request/DOM/input helper compiled for GENERIC and H700 and passed
14 actual pre-GTK controls. Compile owner2.580s, all original channels0,
admissionf94742 consumed. Tiny helpers remain for immediate tests at
`/workspace/tmp/pix-provider616-compile-20261017-01/out/`.
GENERIC SHA8c3a9ba06dc78efffee68bb510b5f273f2fafc8d2ecbc8ee17227a3e4c1e3f0a;
H700 SHA8da94f0cf89b4788c8e3186eb272e9a9d7d67163a5b3d120d99a4c85aff353be.
Product source, ES pin and firmware remain unchanged.

**GTK4/API6 engine and native-input fixture compile.** Frozen diagnostic checkout:
`/workspace/repos/rocknix.worktrees/m7-gtk4-build-20261017-01`, branch
`build/m7-gtk4-20261017-01`, commit969354955741d6c0ca8ce816e1c59ad338b1605b.
It starts from4c3eda48 and stages only six reviewed overlay recipes/two preserved
patches. Never merge it as production adoption. Accepted GTK3 roots are unchanged.
Only independent toolchain/stamps/config were seeded, not a whole old build tree.
Graphene1.10.8, GTK4.24.1, libseccomp2.6.1, bubblewrap0.11.2 and xdg-dbus-proxy0.1.7
all compiled; original Python compatibility failure remains retained.

WebKit2.54.1 completed in2155.316882s, all original channels0, no OOM;
14,397,218,816B cgroup peak is compiler use, not target browser memory. Host
swap-out92131pages is recorded. Owner/container exited, admissionae36c146 consumed.
Engine owner `/workspace/tmp/pix-webkit6-build-20261017-01`, run
`.build-runs/20261017T050229Z-20b8d63a` in the diagnostic checkout.
Actual configuration selects GTK4/Wayland/Skia/GBM/sandbox. Leave
WEBKIT_SAMPLE_MEMORY unset: even value0 enables it; samplerON differs from profilerOFF.
Evidence: `docs/qa-logs/2026-10-17-gtk4-engine-576/` and earlier gtk4-build-576.

All11 critical package/sysroot loaded-byte identities match. Runtime-layer
readback resolves378edges over94ELFs; adding the compiled fixture resolves396
over95. **Strict checker remains FAIL:** four absolute build paths and two relative
`lib` search paths are inherited from accepted-image dependencies; none belongs
to the new overlay. No loader failure or memory cause is established. Preserve
all earlier checker failures and versioned repairs in gtk4-closure-576. Root's
explicit qualification allowed compile only, runtime_authorized:false.

The tiny GTK4 input fixture then compiled in1.846s, all original channels0;
peak118,661,120B, no OOM or host swap-out. Owner/container exited and admission
9af04cef consumed. Binary27056B, SHA
27908eb5badf203de53332c4e35ee96d8c7fbbb6afefd5d72d11c9d8068359f8 at
`/workspace/tmp/pix-gtk4-input-compile-20261017-01/out/input/input-spike`.
Run `.build-runs/20261017T055050Z-ebd5bf9d`, packet gtk4-input-compile-576.
Retain the new build root only for immediate overlay/runtime tests. Runtime
input/popup/close, actual sandbox UID/caps/namespaces/seccomp, dlopen/module/schema
closure, ABI compatibility and H700 performance are still unproved. Root launch
does not itself prove sandbox isolation.

Earlier #616 direct-launch six no-NIC controls and12 parser cases stay accepted;
do not replay for paperwork. Blink source packet remains uncompiled. Herdr w4:p7/p8
login refresh failed before work; do not call those workers active. Internal agents
prepared/reviewed disjoint packets; they hold no runtime allocation.

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

1. **#616 controlled input/provider comparison and #576 portable runtime proof.**
   First fix the local fixture precondition using the prepared v2 (fresh server
   owner receipt, actual trusted-input and untrusted-event negative controls).
   Then use matched uncontended cases for light/Google Drive/Dropbox, fixed UA,
   geometry, observer and lifetime; compare actual process PSS/reclaim/page
   readiness before separate UA or script experiments. Initial2GiB functional
   pass is not1GiB/H700 performance. No account or consent needed. For GTK4,
   disposition the six inherited search paths and assemble exact new-package
   payloads over accepted runtime in a fresh guest, including schemas/modules,
   certificates/fonts/processes/injected bundle. Use compiled input fixture for
   synthetic typing/popup/close/cleanup, actual sandbox identity and reviewed
   presentation before provider/performance or physical work. Each new runtime
   needs fresh admission, owner, guard and active result supervision. Do not
   rerun completed engine/compiler owners. #587 busy-stop safety remains required
   before any service suspension policy; Blink is fallback.
2. **#613 next independent package task, source-only patch ready.**
   `/tmp/pix-m7-613-source-20261017` has a one-line fallback symlink target fix,
   patch SHAc22a60e12d87fdb0ca2fa05696267c1df351d2c473400bd37e3d64df87ec2b97;
   pkgcheck/bash-n/apply checks pass. Current checked upstream still has the bug;
   conditional contribution belongs #585 after proof. No product edit applied.
   Fresh VM must isolate hardcoded /storage/.config/emulationstation paths;
   ES --home alone is insufficient. Prove storage precedence and fallback with
   fresh ES processes and flow/evidence references before promotion.
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

All current build/VM/browser owners are complete; admissions consumed and exact
host/container exits checked. Source workers are packaging/reviewing evidence only.
The requested additional-provider functional test is complete in its stated scope.
No physical action or pending user approval is needed for the next portable tests.
Do not reuse old run owners, consumed admissions, retired disks or expired listeners.
Original compile/VM receipts are in the owners/packets above. New runtime requires
fresh measured admission and watched submission; no off-session notifier exists.

Prior #616 VM allocation9e38f30969c5454097c03354fd79a23e consumed;2,312,990,720
allocated bytes of its owned VM disk/OVMF retired. Export owner
/workspace/tmp/pix-browser-controls-vm-20261017-01/export/. Frozen run
m7-p5-build-20261015-03/.build-runs/20261017T040228Z-0fddbf18.
Compile admission261514b9d3fa44cdaef8b34cbe9f07fd consumed. Tiny helpers remain
only for queued immediate tests at /workspace/tmp/pix-browser-controls-compile-20261017-01/out/.
GENERIC SHA530b0d2c7daf739eb061a415da4224a7affcec1b1837a452d182e97a03c16454;
H700 SHA9dad87a65f5415311d663448834aac1ae281212c931f12c3cc2afb8fbbd0f245.
Do not rerun consumed producers or replay old owners/ports.

The prior verified published ordinary refs are4594975b5c0e4bcc4a7f24a38ab76f097ffa009f,
with three hosted checks passed at /tmp/pix-gtk4-publication-20261017-01.
This checkpoint and new experiment packets follow it. Publication receipts for
this record batch will be in /tmp/pix-provider-gtk4-publication-20261017-01;
inspect actual refs and CI before claiming the newest record published.
No production source, ES pin or firmware changed.

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
| `docs/qa-logs/2026-10-17-gtk4-spike/`, `2026-10-17-blink-feasibility/` | Original source-only packets; subsequent GTK4 builds are in gtk4-build-576, Blink remains uncompiled |
| `docs/qa-logs/2026-10-17-browser-controls-616/`, `browser-controls-build-616/`, `browser-controls-vm-616/`, `browser-controls-results-616/` | Diagnostic source, actual compilation/parser proof, executed VM fixture and original outcomes |
| `docs/qa-logs/2026-10-17-gtk4-build-576/`, `2026-10-17-provider-handoff-616/` | Completed dependency originals and prepared provider wrapper; engine/provider results are in the newer companion packets |
| `docs/qa-logs/2026-10-17-browser-rendering-options/` | Primary-source graphics findings and parallel ownership |
| `docs/decision-register.md` | D-WORKFLOW-170 bounded parallel alternatives |
| `docs/releases/next-candidate-work.md`, `docs/vm-qa-log.md` | GTK4-first migration experiment, provider controls and limits |
| `docs/work-logs/2026_10-work_logs/2026_10_17-work_log.md`, `docs/friction-log.md` | Findings and preserved fixture failures |
| This checkpoint and branch pointer | Archived preceding October17 state; terminal owners and executable next queue |

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

Previous full checkpoint: [saved-session-state-next-20261017T055318Z.md](archived/saved-session-state-next-20261017T055318Z.md).
