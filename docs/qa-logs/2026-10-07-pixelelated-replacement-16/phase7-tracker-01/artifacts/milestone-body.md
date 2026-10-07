## Current priority — qualified software to H700 device builds

P3 GENERIC_X64 qualification and P4 fixes audit are complete on candidate 16.
All eight findings are resolved with published commits, installed evidence and exact
tracker readbacks. #471/#467/#468/#478/#479 and the compound software gates
#361/#386/#327/#409/#383 are completed. Original failed runs remain retained.

1. **#461: read-only capacity/retention review.** Remeasure free space, next
   build/copy/artifact/QA footprint and protected transitive dependencies.
   The previous exact two-disk retirement is complete; no wider deletion is
   authorized. An unreadable or referenced dependency cannot be proposed away.
2. **H700 DDR4 RG35XX SP arm**, from qualified product inputs, under the
   standard build watcher with active result delivery; verify the exact asset.
3. **H700 aarch64**, with its own measured capacity and artifact verification.
4. **Named physical/P5 gates:** device adoption/smoke facts, corresponding
   source and 14 known licence metadata gaps, public docs and manifest-bound
   release assets. Physical actions and publication require their named scope.

Candidate16: ee014909137e03706e0b3020b8396be589aaa705; ES 72494bc72e3d64d4dcfeb4e6478052bbdf166c5b;
bundle 7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a.
All 15 default suites, 78 comparison frames with zero unclaimed differences,
26 actual ROCKNIX RC2 upgrade checks, and 318 local WebDAV/SFTP/S3 assertions pass. No new RA reset or Dropbox
credential is needed. Unchanged proxy/library proof has explicit byte/source
custody; no new live upstream-freshness query is claimed.

This is software qualification, not RC designation or release publication.
Watchers record status; the primary consumes results. Off-session alerts #395,
FOSS observability #432 and automated RA reset #464 retain their later scope.
Can this be done on the VM? Software qualification is complete on the VM.
Storage capacity and device compilation are host facts; physical smoke gates
retain their named hardware facts and separate action scope.

[Final audit resolutions](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md), [criterion reconciliation](https://github.com/pixelelated/distribution/blob/7f293a22d97317d1632952a5cf2e9d4a45bd2cb2/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/10-closure-reconciliation.md).

## Ordered critical path

| Phase | Priority / state | Exit gate |
| --- | --- | --- |
| **M7.P0 — Tracking conventions** | **COMPLETE** — tracking reconciliation #388; continuation/reference cleanup #389, with local checks and live readback. | This ordered body, open titles and canonical rules agree. No product readiness implied. |
| **M7.P1 — Safe migration and recovery** | **SOURCE GATE COMPLETE** — #365/#356/#320 plus #391/#392 source controls and guest promotion verified; all image-only acceptance stays assigned to P3. | Supported marker versions, repeatable numbered transitions, interruption/marker-failure recovery and settings-lock safety have passing/failing controls; applicable actor/state coverage is explicit. |
| **M7.P2 — Qualified release inputs** | **COMPLETE** — #361/#362/#386 input and unchanged-source preservation criteria reconciled; #310/#327/#332 software gates accepted. | Source manifests, actual consumers/runtime proof and explicit cut-time freshness evidence retained. |
| **M7.P3 — Build and qualify the image** | **COMPLETE FOR GENERIC_X64 CANDIDATE16** — all 15 default suites, 78 screens, 26 actual RC2 upgrade checks, and 318 protocol assertions; affected installed recovery/UI and exact unchanged-input carry-forward accepted. | Frozen product/input identity, preserved original state and independent completion/cleanup receipts. Device artifacts retain their own build/smoke gates. |
| **M7.P4 — Independent fixes audit** | **COMPLETE** — approved primary plus both Fable passes; all eight findings resolved in #471; repaired candidate 16 rebuilt and requalified. | Published audit 05/08/10 and exact checked/closed issue readbacks. No further external audit call required. |
| **M7.P5 — Device builds and release staging** | **NEXT: capacity review #461 → H700 DDR4 RG35XX SP arm → aarch64**. Then named physical and publication gates. | Each device artifact verified before its authorized smoke/migration actions; source/licence/public docs and manifest-bound assets before release publication. |

### M7.P1 — Work in order

1. **Migration controls and shared state model** — #365 with #356 and fixture correction #390: map applicable actors to T01–T26 assertions, preserve independent settings/content choices, and retain failing controls for the missed transitions. #391 owns inherited partial states; #392 owns missing-remote refusal.
2. **Versioned, repeatable migration** — #356: strict malformed/future-marker handling, numbered steps/journal, failure at tier or marker publication, safe retry and second-device follow. Name the actual older-build compatibility boundary; do not claim RC2 understands a future protocol.
3. **Settings recovery locking** — #320: deterministic concurrent-write and lock-busy controls, then fix stale recovery-record publication.

P1's source exit permits later candidate VM evidence to remain open. It does not close an issue from host tests alone.

### M7.P2 — Work in order

1. **Current proxy with no functionality loss** — #361 and #384: reconcile local patches with current upstream, prove >100-game preparation, never count queued work as ready offline, preserve cached sign-in/data and queued base/subset awards through upgrade/reconnect.
2. **Compatible current dependencies** — #362 and #386: libsoup/WebKit build inputs plus glslang, SPIR-V headers, cbindgen and tllist; verified sources, compatibility and package checks. Coupled dependencies retain evidenced parent pins. Distribution ancestry remains frozen by D-WORKFLOW-111.
3. **Remaining software and execution gates** — #310 launch-memory cause/fix, #332 LED script/reselection, #371 push-hook fix, #367 process guard/help, #368 remaining handoff armatures. Diagnostic VM builds are allowed when required to investigate these.

#327's implemented explanation-page change is now a P3 frame/docs verification item. Upstream contribution #168 can proceed with qualified local fixes; upstream acceptance does not hold the candidate.

### M7.P3 — Work in order

0. **Lowercase pixelelated transition** — #409 identity source, sibling pins, cloud default, active addresses/policies and source controls are complete above. The RGB555 LCD asset system, Ocean splash/ES/theme integration and fresh input freeze are complete above; build and installed behavior proof remain. No RASTERATOPS predecessor gate. Repeat applicable qualification on new bytes; #409 is completed after final candidate 16 qualification and the P4 audit; old candidate evidence stays historical.

1. **Freeze, cold-build and retain the exact artifact** — #383/#344: distro/ES/splash commits, container digest actually consumed, source inventory, concurrency, fresh lowercase pixelelated root, logs, candidate manifest and digest verification before/after QA. #393/#394 provide corrected activity detection and automatic monitoring for future builds; the completed image keeps its frozen source. #395 retains disconnected delivery as an explicit outstanding infrastructure item; active-session supervision accompanies the durable watcher. A detached status file is not an alert.
2. **Clean install and RC2 upgrade; actual cloud paths** — #354 and #349/#350/#351/#352/#353/#363/#364/#365/#366/#376/#377/#379/#380/#381. Run full VM QA plus required opt-ins, local WebDAV/SFTP/MinIO-S3, independently reset promoted cases, pair migration, interrupted retries/future markers, writer-shaped archives, and injected failing controls.
3. **Preservation, performance and identity** — #361/#362/#384 runtime proofs; #310 memory/launch loops; #364 timing; #327 explanation frame/docs; #332 software fixture/UI evidence; #337 identity/manual update; #357 no upstream reporting; #359 licences. English/French at 640x480 and Nova1280x960, time-to-play and image brand/secret/localisation/source checks.

**Engineering-build gate is not the RC gate.** Image-only acceptance criteria must remain open until the image exists and supplies proof. They do not prohibit that engineering build. An RC claim requires the known software bugs resolved and P4 completed; no RC2 bug waiver carries automatically.

### M7.P4 — Work in order

The fixes review belongs to #383. #375/#382 are the completed initial review and dispositions; do not restart them. Use the approved cross-lab depth and verified receipts. Resolve findings, renew affected artifact evidence, then make the RC readiness call. The general automatic version/depth policy is later #378, not a missing authorization for this review.

### M7.P5 — Work in order

#265 and #344 own manifest-bound release selection/draft tooling, corresponding-source publication, adoption/recovery/release notes and public docs. Preserve the approved support matrix. The first handheld route is: complete P3 and the P4 fixes review, build the H700 DDR4 image for the RG35XX SP from the qualified inputs, verify that device artifact, then perform its approved migration and smoke checks. The GENERIC_X64 artifact cannot be flashed to this handheld. RG35XX SP migration precedes remaining device attachments; each asset needs its own smoke evidence (D-WORKFLOW-100/120). Physical actions, personal-cloud writes and publication retain their named-action gates. Keep unqualified assets held.

## Placement and historical references

M7-wide umbrellas: #383 delivery, #344 release contract, #354 cloud scope. Their titles omit P because they span phases. Other open titles use their owning M7.P phase. An input issue assigned P2 can retain image-only acceptance for P3; title placement does not waive that criterion.

The older #344 headings remain **contract sections**, not this execution queue: contract P0 is historical investigation; contract P1 spans current P2/P3 custody; contract P2 maps to current P3; contract P2b/P3/P4 map to current P5; contract P5/P6 are later work. Cite `#344 contract P2` explicitly rather than renumbering that evidence.

## Explicitly outside this release

Infrastructure topology/off-host restore drill (#347/#348/#355), replacement runner and progressive inherited-code review planning (#336/#339/#346), own telemetry design (#387), full site beyond the approved placeholder, trademark registration and general automatic review-depth policy (#378). Existing decisions D-WORKFLOW-102/113 and the release contract remain binding.


Build/VM QA OpenTelemetry evaluation is separately recorded in #432 following the maintainer's question. Existing device-telemetry design #387 is different. No collector/backend deployment or new RC gate inferred; current priority stays qualification above.

#432 remains backlog: D-INFRA-016 prefers fully FOSS observability, comparing SkyWalking and the clarified ClickHouse option with complete license/resource evidence and local-site/self-hosted online deployment, likely after separate build and agent/observer hosts are available. It is not an added M7 RC gate.

Hosted Dropbox/offsite observations are explicitly optional under D-QA-058/#462; #463 is milestone-less. No personal-cloud credential is a release dependency.

#464/D-QA-059 reopens automated dedicated RA fixture resets (Browserbase/Kitesurf/local browser comparison) as backlog; it does not delay this RC. #240 retains softcore route expansion and reset guidance.
