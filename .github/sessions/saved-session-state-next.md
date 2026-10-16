# Saved Session State

> **Saved:** 2026-10-16T16:22:04Z
> **Branch:** `feature/m7-audit-integration-603`
> **Repository:** `pixelelated/distribution`; integration branch `next`
> **Request:** “Let's stash our work.” Investigation is stopped for this handoff.

## Start here

pixelelated is an immutable Linux distribution for handheld gaming devices, built
by cross-compiling complete OS images. There is no application development server.
The release target is 0.0.1; the current engineering image is private owner testing,
not a designated public RC. The OS name and cloud default are lowercase
`pixelelated` and `/pixelelated`; preserve existing selected paths and credentials.

1. Read current `next:AGENTS.md`, its every-session `.claude/rules/` files, and
   scoped rules before touching their paths. Read the `session-resume` skill.
2. Read this checkpoint, the [live M7 ordered plan](https://github.com/pixelelated/distribution/milestone/7),
   `docs/releases/next-candidate-work.md` and the active issue #615. Historical
   queues in archived checkpoints are not the current plan.
3. Read `docs/qa-logs/2026-10-16-h700-browser-exit-615/README.md`, `summary.json`,
   `frame-index.json`, preservation/cleanup receipts and `verify.py` for the
   unresolved physical browser question. Portable #614 is already complete.
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

We are determining why a Dropbox browser attempt on the H700 RG35XX SP became
unresponsive and did not visibly respond to synthetic Escape. Portable installed
exit/input controls pass; three physical follow-ups establish early exit, normal
close, and a pressure-guard event, but **loaded-page Escape remains inconclusive**.
No product fix is selected. Do not call it a one-time glitch or a reproduced
WebKit/input bug. The next experiment must attribute instrumentation overhead and
process memory and establish actual page readiness before drawing that conclusion.

## Completed this session and publication

- Investigation/evidence commit **060dbde84144af11f99a70453e9d537c7f724490** is
  published on `origin/next` and `origin/feature/m7-audit-integration-603`.
  Both remote heads and clean local checkouts were read back at this stash.
  The stash commit follows it; inspect Git for that commit's publication status.
- All three hosted checks for 060dbde passed: wordlist jobs 116841197323 and
  116841196476, record job 116841196709. CI result receipt:
  `/tmp/pix-m7-h700-exit-repro-20261016-01/ci-result.json`.
  [Publication readback](https://github.com/pixelelated/distribution/issues/615#issuecomment-6209489875).
- #615's 34 compact originals and six reviewed 640×480 frames are retained with
  SHA256SUMS, an offline verifier, preservation and cleanup receipts. The original
  failed outcomes remain failures. Context-free evidence review corrected the
  timing description and stale branch pointers before publication.
- #614 is closed: four guarded installed-browser VM controls pass on the same
  source (QEMU Escape, immediate-destroy uinput, installed normal close in
  0.27249s, installed phone HTTP handler over guest loopback). First observer's
  absent-PSI failure is retained and excluded; the corrected repeat passed.
  Evidence: `docs/qa-logs/2026-10-16-browser-exit-614/`. This 8GiB no-NIC x86 proof
  does not establish H700 memory capacity, provider authentication or physical
  phone/controller behavior. Its VM was stopped and 2.48GB disposable disks retired.

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

1. **#615:** design the lean follow-up first. Account for observer/controller
   overhead, collect per-process PSS and explicit loading/loaded-page evidence.
   Record the VM-first split in the issue; use #614's accepted controls where
   applicable. Retain independent pressure/deadline guards. Previous three-trial
   allocation is complete and its fixtures are historical, not commands to replay.
   Bind any further device experiment to a fresh owner and named authorized scope;
   do not silently extend the completed allocation or relax its safety thresholds.
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

No build, VM, device diagnostic, provider audit or deployment is active from this
work. All workers are idle. Prior CI watcher is finished, with launcher/wrapper/
command/monitor/runner/build results0. Host PIDs3673029/3673059/3673031/3673030
were rechecked absent during stash. Owner:
`/tmp/pix-m7-h700-exit-ci-20261016-02`; run:
`/workspace/repos/rocknix.worktrees/m7-player-setup/.build-runs/20261016T061824Z-2bd1dc52`.
An initial submission to missing owner01 failed2 before launch; owner02 corrected
it. No off-session notifier is claimed. Stash publication checks, if launched,
have their separate owner `/tmp/pix-m7-session-stash-20261016-01/ci-owner` and
receipts in its parent; inspect their actual results before calling them complete.

Useful read-only checks from the coordinator:

```sh
git status --short --branch
git log -3 --oneline
git ls-remote origin refs/heads/next refs/heads/feature/m7-audit-integration-603
python3 -I docs/qa-logs/2026-10-16-h700-browser-exit-615/verify.py
gh api repos/pixelelated/distribution/milestones/7 --jq .description
gh issue view 615 --repo pixelelated/distribution
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
- #558 shutdown and #561 LED are watches. #587 proxy pause, #576 GTK4,
  #568 finalization wording, #562 integrity, #586 credentials and #560 fast
  shutdown remain backlog. Prior proxy target saving was only390KiB and not
  adopted; approximately78MiB ES handoff saving was VM evidence, not a provider cure.

## Key files and related context

This stash archives the previous full checkpoint, refreshes this canonical file
and its two branch pointers, and appends the dated work log/index. No product file,
firmware, personal device state or prior QA original changes.

- Previous checkpoint, intact: [saved-session-state-next-20261016T162204Z.md](archived/saved-session-state-next-20261016T162204Z.md).
- Current flows: `docs/es-menu-map.md`, `docs/conflict-wizard-ia.md` and exact-source
  frame indices. ES behavior/copy changes require references and reviewed frames.
- Release preparation: `docs/releases/0.0.1-release-preparation.md` and
  `docs/releases/0.0.1-release-note-draft.md`.
- Work log: `docs/work-logs/2026_10-work_logs/2026_10_16-work_log.md`.
- Stash readbacks/review/CI receipts: `/tmp/pix-m7-session-stash-20261016-01`.

Ordinary scoped records, commits, pushes and tracker updates remain authorized.
Commit on the coordinator, fast-forward clean `next`, push both ordinary refs;
never force push or merge the stale harness. A context-free handoff review is
required by D-WORKFLOW-133 and passed on the prepared handoff: the reviewer
reconstructed the current queue, verified archives and ran the offline evidence
check without device/network access. This handoff does not authorize new external model
transfers, source-contact messages or publication of a release.
