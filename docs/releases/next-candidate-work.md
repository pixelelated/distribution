# Next pixelelated candidate — working list

Reconciled October14 under #585 against live issues, their latest comments and
source-bound component evidence. The baseline is the last tested device build,
`0.0.1-dev+20261011T222153Z.gbc9dfe8141d9` (#555–#557). This does not relabel it as
a publicly designated RC. The [M7 milestone body](https://github.com/pixelelated/distribution/milestone/7)
owns execution order; this table is a dated readiness reference.

Open does not mean untouched: several fixes have compiled/installed component
proof and remain open for the final composition. An engineering image must exist
before its clean-install/upgrade checks can run; those checks hold RC designation,
not the build needed to perform them. The initial reconciliation launched no tests; the dated evidence below includes subsequent component runs.

## Testing findings still in the current candidate

| Work | Verified so far | Still required |
| --- | --- | --- |
| Browser slowdown and memory pressure — #570/#572 | Actual compiled ES handoff change reclaims78.01MiB in a bounded VM comparison; repeated handoff and recovery pass. GStreamer controller/scanner recipe/install and fresh-registry controls pass. | Final combined image/dependency closure and relevant UI/clean/retained checks; H700 corroboration remains a separate physical observation. No claim of a universal WebKit or speed cure. |
| Phone keyboard status — #571 | Compact stable status, translated component checks and actual installed bridge navigation/input pass; keyboard geometry remains fixed. | Final-source integration and affected assembled-image regression. This is no longer an unimplemented ribbon proposal. |
| Wi-Fi picker — #577 | Stable initial/refresh/empty/error/scroll UI, existing connection routes and separate backend failure controls pass. Subsequent compiled French hint frames are retained. | Combined corrected backend through UI, final image and retained settings. Synthetic enumeration is not a physical radio measurement. |
| GameCube RVZ and offline achievements — #574/#583/#584 | Frontend reader/retry, MD5 sanitizer subset, proxy padding/scanner and Dolphin routing configuration have passing component evidence. Actual Dolphin decoding/encoding/whole-data roundtrips, native proxy ISO/RVZ/cache/account/award/reconnect integration,234 CHD-bearing hashes and actual main/systemd/real worker lifecycle now pass within scope. | Current native library is now source-bound by a successful pinned build. #588 startup race is causally reproduced, repaired and passes actual-service plus ten component cases. Packaged repairs reproduce the tested Python source exactly. Still required: current-library hash/codec integration, installed/default-boot composition and Dolphin gameplay, plus final frontend/image integration. The original synthetic header failure and its additive correction remain recorded; protocol proof is not full-service qualification. |
| Standalone save-state expectations and Dolphin data preservation — #575/#581 | Capability/help and EN/FR frames, retained-data refusal and save-path controls pass within scope; shorter French descriptions and corrected English640 long-card refusal/return verified. | Native emulator/save behavior and clean/retained installed paths. Ordinary game saves and automatic save states remain different capabilities. |
| Notice before offline-achievement preparation — #567 | Conditional confirmation UI and four native ES indexing API branches pass; actual preparation was represented by a controlled ctl substitute. | Actual proxy/top-up integration on the composed source and final image; do not equate the substitute with offline-service qualification. |
| Nova account/history isolation — #565 | Provenance investigation completed to available evidence; library-copy test separates ROM-only from gamelist history. Selected clean-state and payload guards have positive/negative controls. Original account entry remains unknown. | Inspect the actual next firmware payload; clean install must lack personal accounts/fabricated history, while retained-storage upgrade preserves legitimate settings/history. |
| Recent default — #578 | One-literal compiled default fix and nine default/explicit-choice controls pass; imported gamelist history can populate Recent, a ROM alone cannot. | Final-source/image proof while preserving explicit player choices. Historical Nova Recent entries are not evidence that this new default fix fabricated history. |
| ScreenScraper developer provisioning — #566 | Runtime versus compiled behavior and separate player accounts are traced. The owner selected the existing shared JELOS developer identity (D-WORKFLOW-166); recipe/gate candidate19221 passes127 root-policy and4 environment-selection VM controls. | Qualify the actual rebuilt binary, UI/frames, backup and clean/upgrade images. Replacement credentials are backlog #586, not a candidate dependency. Preserve unrelated private-credential protections. |
| Steam installation recovery — #564/#579/#580/#582 | Runtime/FEX/Proton preservation and complete synthetic caller controls pass within scope. Partial-client retry defect reproduced; real55-member client archive CRC/layout inspection passes. | Client transaction03e130 addresses both independent review findings in source; corrected full caller and fresh profile-symlink VM cases pass. Existing-profile, detached-child, census-failure, real transport-timeout, interrupted-publish, committed-self-update and CRC-retry cases now pass. The CRC fixture logging failure and correction remain recorded. Broader recovery and native/installed qualification remain; original a057 fixture failure is retained. This was found during the20261001 intake, not reported from gameplay. |

Evidence: [installed setup](../qa-logs/2026-10-13-setup-qualification/installed/README.md),
[library/preservation components](../qa-logs/2026-10-13-library-vm/README.md),
[October14 frame completion](../qa-logs/2026-10-14-offline-components/README.md),
[RVZ/proxy/MD5 and archive results](../qa-logs/2026-10-14-rvz-proxy-components/README.md),
[Dolphin preparation](../qa-logs/2026-10-14-dolphin-tool-preparation/README.md),
[independent formats](../qa-logs/2026-10-14-independent-format-runtime/README.md),
[native proxy integration](../qa-logs/2026-10-14-proxy-native-runtime/README.md),
[actual proxy lifecycle](../qa-logs/2026-10-14-proxy-service-runtime/README.md),
[startup reconnect repair](../qa-logs/2026-10-14-proxy-startup-runtime/README.md),
[current native build](../qa-logs/2026-10-14-proxy-current-native-runtime/README.md),
[CHD parity](../qa-logs/2026-10-14-chd-native-runtime/README.md),
[Steam first caller and review](../qa-logs/2026-10-14-steam-client-first-caller/README.md).
Earlier packet UNRUN labels describe their preparation time; later exact-source
receipts supply scoped completion. No failed original result is rewritten.

## Observations to monitor and work intentionally deferred

- **Nova shutdown restarting (#558):** normal power-off requests and later boot
  are recorded; no retained crash dump or confirmed cause. Read-only triage is
  complete. At the owner's October14 direction, await a reliable reproducer or
  useful recurrence evidence before repair work. This watch item does not block
  the candidate and is not fixed.
- **RG SP red LED (#561):** a saved Red preference explained the observed color;
  Default is restored by the owner. The low-battery warning uses a persistent
  setter; interruption before restoring the prior choice is a plausible lead,
  not a proved test-script write. Original writer remains unknown. Monitor subsequent
  use/upgrades; the deferred interruption matrix is not an active build gate.
- **Last-game/finishing progress (#568), ROM/cloud integrity comparison (#562),
  fast-shutdown value (#560), reusable upstream intake procedure (#559),
  replacement ScreenScraper credentials (#586):** backlog. #568 asks whether the
  last game is active or post-game work is continuing; no owner copy choice is
  pending. A finishing label must follow actual game-processing completion.
- **Temporary proxy shutdown during browsing (#587):** future measured lifecycle experiment, conditional on preserving queued awards, cache work and next-game readiness (D-RA-047). No production behavior change or extra RC gate.
- **GTK4 and lazy proxy imports (#576/#570):** diagnostic alternatives under
  D-WORKFLOW-163, not mandatory migrations for this RC. Target lazy-import savings
  were only390KiB; no GTK4 memory benefit has been measured.
- **Automatic retirement (#493), off-session alerts (#395), FOSS observability
  (#432), reset automation (#464/#240):** infrastructure follow-up. Current build
  admission, owned cleanup and active result supervision remain required.

#569's retained cloud-configuration diagnosis is closed; its history feeds #565.
Previously completed USB/startup/version/cloud-management fixes and prior audits
are not reopened simply by this inventory. Remaining restore regression is #349.

## Build completion and upstream follow-up

Finish the outstanding source/component work, compose #563's ROCKNIX20261001
foundation, produce and qualify the combined GENERIC_X64 image/real retained
upgrade, complete the applicable audit, then H700 and SM8550 under #555.
#528/#344 and related source/licence/custody/identity/notes requirements still
govern publication; they are distinct from creating an engineering image.

[Running upstream queue #585](https://github.com/pixelelated/distribution/issues/585)
holds submissions until the initial current build and relevant qualification are
complete (D-WORKFLOW-165). Keep #168's existing ten proxy drafts, new RVZ/MD5
fixes and smaller ROCKNIX candidates visible. Submission-only standalone proof
and PR preparation are follow-up work, not additions to the critical path.

## Historical October11 working list — superseded by the review above


Recorded 2026-10-11 under #533, following the maintainer's request to document
the list and begin #531. The [M7 milestone body](https://github.com/pixelelated/distribution/milestone/7)
is the authoritative current order; this is a dated working reference, not a
second release queue. No new candidate is built or designated by this list.

| Order | Work | Evidence needed before advancing |
| --- | --- | --- |
| 1 | #531: USB revision independent of the OS version | Actual networking/MTP preparation controls on host and guest, old-source failure, preserved descriptor identities; then installed bytes on the combined image. Source controls pass: 72/72 on host and guest, old-source failure retained. The combined-image check remains. |
| 2 | #532: thin rolling RC/release naming | D-WORKFLOW-159 selected: rc.N then release, explicit never-reused counter per frozen set, internal dev default, new qualified assembly for release. Host57 controls pass; shared #530 installed-image proof remains. |
| 3 | #533: reconcile remaining issue criteria | Reconciled in [the scope table](next-candidate-scope.md): 18 M7 issues, four bugs. Retire migration; preserve #349/#350 exact-frame gaps and publication requirements. #528 firmware dispositions precede final freeze. |
| 4 | #535–#540 source/audit complete; #528 engineering input disposition | Eleven source-backed licence declarations, inherited HarfBuzz ICU resolution and checksum-pinned unchanged Doom bytes pass pinned-builder proof. Retain all existing components for engineering QA; shader/ABL/vendor/prebuilt terms and source custody still hold publication. See the [disposition packet](../qa-logs/2026-10-11-component-inputs/README.md). #537 needs combined-image qualification. |
| 5 | #344/#529/#530/#531: combined engineering image | Recheck #493 build/QA headroom, freeze one input set, actively supervised build, installed fixes/identity, clean/public ROCKNIX and retained-storage tests, affected flow frames and applicable delta review. |
| 6 | #528/#265/#344/#359: release completion | Independent retrieval/hash verification and off-host custody, adoption/recovery/support/source/branding notes, applicable hardware/attachment gates and named publication authority. |

#529's startup fix and #530's build identity are integrated; their next-image
criteria are open. Earlier accepted VM/cloud/audit/device evidence is retained
with its source scope and is not replayed merely to resume. No automatic cloud
move/follow returns. Names do not confer qualification, and an image needed for
QA may be built before its installed-image criteria can pass.

Website #511, broad observability #432, disconnected notifications #395,
active-name cleanup #509 and personal cleanup/redundancy #516/#518 remain
separate. Active supervision and prompt delivery of long-job results remain
required now. Previously approved device transfers/reboots have completed;
owner devices are in use. #536 consumed one later explicit screenshot approval;
its frame/aggregate navigation-log observation is recorded separately. No input,
sign-in submission or configuration change was performed. #535 open Wi-Fi is now part of M7.P5 under the latest implementation approval.

## 2026-10-11 audit delta

The approved Fable 5.1/xhigh refutation completed and its identity/provenance
verified. #540 owns seven findings: three High, one Medium, three Low. All seven
repairs pass focused guest controls, 1,373 full-regression PASS controls,
108 WebDAV + 108 SFTP checks, 26 connection transactions and 15 whole-script
refusals. Final54 builds; matrix55 supplies 16 reviewed affected EN/FR small/large
frames. Earlier rejected fixtures/layouts remain recorded with their own source.
Distribution `bc2dceb406` is integrated on next and pins published ES
`c8dc72cf9e`. All seven #540 findings are resolved. #528 and the combined-image
clean/retained qualification gates remain next. No new RC designation or
owner-device action follows from source-overlay qualification.
