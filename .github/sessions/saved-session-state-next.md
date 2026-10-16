# Saved Session State

> **Saved:** 2026-10-16T17:18:28Z
> **Branch:** `feature/m7-audit-integration-603`
> **Repository:** `pixelelated/distribution`; integration branch `next`
> **Request:** Continue VM browser headroom tests, preserving browser functionality and safe service recovery.

## Start here

pixelelated is an immutable Linux distribution for handheld gaming devices, built
by cross-compiling complete OS images. There is no application development server.
The release target is 0.0.1; the current engineering image is private owner testing,
not a designated public RC. The OS name and cloud default are lowercase
`pixelelated` and `/pixelelated`; preserve existing selected paths and credentials.

1. Read current `next:AGENTS.md`, its every-session `.claude/rules/` files, and
   scoped rules before touching their paths. Read the `session-resume` skill.
2. Read this checkpoint, the [live M7 ordered plan](https://github.com/pixelelated/distribution/milestone/7),
   `docs/releases/next-candidate-work.md` and active issues #587/#615. Historical
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

## Current focus

Preserve the browser on1GiB devices by investigating safe temporary service
shutdown. The new #587 VM evidence finds26.27MiB more available memory in a small
synthetic workload and successful normal restarts, but also a **busy-stop timeout
and SIGKILL at15seconds**. A production pause/stop policy is not selected. The
next work is a safe quiescence/cancellation and restoration contract, followed by
fresh VM interruption tests, then a separately scoped H700 loaded-page trial.

## Completed this session and publication

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

1. **#587 / #615:** inspect `proxy_service.py:run_proxy_service`'s synchronous
   initial flush before the stop_event loop, service.py's signal/event propagation,
   flusher.py/network.py blocking I/O and the actual15s unit timeout. Design an
   atomic quiescence or bounded cancellation contract with no busy-check/stop race;
   preserve queue/cache/account routing and restore only a previously active
   service that this session stopped. Prove busy worker/slow response, failed
   launch, browser exit/crash, stale owner, disabled service, restart failure and
   duplicate acknowledgement behavior on a fresh VM allocation. Do not adopt
   SIGSTOP (it retains memory), unconditional stop, or only a larger timeout.
   Source preparation/candidate review comes before a new runtime. Then prepare
   a bounded real-page H700 test; #615 loaded-page Escape remains inconclusive.
   The completed fixtures are historical absolute paths, not replay commands.
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

No build, VM, device diagnostic, provider audit or deployment remains active
from this experiment. Original launcher/wrapper/command/monitor/runner/build/VM
channels are0 and exact host/QEMU identities exited. Admission
5c8eeab34ebb4b30ae07af99fc0c7aa6 was consumed and its two owned VM files retired.
Private preparation: `/tmp/pix-m7-browser-headroom-20261016-01`.
Retired guest owner: `/workspace/tmp/pix-m7-headroom-vm-20261016-02`.
Compact export: `/workspace/tmp/pix-m7-headroom-evidence-20261016-01`.
Frozen run: `/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-03/.build-runs/20261016T165313Z-96219fda`.
Matrix run: coordinator `.build-runs/20261016T170036Z-509ef5cb`.
Publication CI, if launched after this checkpoint, has its own owner/receipts
inside the private preparation directory; inspect actual results. No off-session
notifier is claimed. The first refused allocation01 has no VM.

Useful read-only checks from the coordinator:

```sh
git status --short --branch
git log -3 --oneline
git ls-remote origin refs/heads/next refs/heads/feature/m7-audit-integration-603
python3 -I docs/qa-logs/2026-10-16-browser-headroom-587/verify.py
gh api repos/pixelelated/distribution/milestones/7 --jq .description
gh issue view 587 --repo pixelelated/distribution
```

Use `tools/archaeology` before declaring another issue new. A new runtime gets
fresh admission/owner and `tools/watch-build-submit`/`tools/watch-build`; actively
check results at intervals of at most60s and announce actual completion. Never
edit a tool in flight. Host process checks require actual host context; sandbox
PID views can conceal host processes. No broad process kill or blanket cleanup.

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
- #558 shutdown and #561 LED are watches. #587 is current M7 work; #576 GTK4,
  #568 finalization wording, #562 integrity, #586 credentials and #560 fast
  shutdown remain backlog. Prior proxy target saving was only390KiB and not
  adopted; approximately78MiB ES handoff saving was VM evidence, not a provider cure.

## Key files and related context

| File | Change |
| --- | --- |
| `docs/qa-logs/2026-10-16-browser-headroom-587/` | New original evidence, analysis, verifier, fixtures and reviewed frames |
| `docs/decision-register.md` | D-RA-048 promotion/safety constraints |
| `docs/releases/next-candidate-work.md`, `docs/vm-qa-log.md` | Current result and scope |
| `docs/work-logs/2026_10-work_logs/2026_10_16-work_log.md`, `docs/friction-log.md` | Findings, fixture failures and durable next step |
| This checkpoint and branch pointer | Archived prior bytes; refreshed current queue |

- Previous checkpoint intact: [saved-session-state-next-20261016T171828Z.md](archived/saved-session-state-next-20261016T171828Z.md).
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
