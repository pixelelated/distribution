# Read-only research leads — not independent acceptance verdicts

Phase1.4.5 helpers mapped the following sources. They did not execute checks,
edit files, grade criteria, inspect original PNG pixels or invoke reviewers.
The primary auditor must read every cited artifact before using it as evidence.
Exact issue text and line locations are preserved in `criterion-inventory.json`.
That raw inventory includes historical and later-phase criteria, not only P4 scope.

Abbreviations: Q=`docs/qa-logs/`; R=`projects/ROCKNIX/packages/network/rclone/sources/`;
S=`projects/ROCKNIX/packages/rocknix/sources/scripts/`;
E=`/home/max/Development/emulationstation-next.worktrees/qa-integration/`;
Q09=`Q/2026-10-05-pixelelated-replacement-09/`;
Q10=`Q/2026-10-05-pixelelated-replacement-10/`;
Q12=`Q/2026-10-05-pixelelated-replacement-12/`;
Q14=`Q/2026-10-06-pixelelated-replacement-14/`.

## Cloud/state lane

Helper `/root/m7_p4_cloud_research` enumerated111 live owning-issue criteria
plus8 umbrella criteria (354/383). Count remains a lead until primary scoping.

| Issues | Source anchors | Raw artifact leads |
| --- | --- | --- |
|320|E/es-core/src/SystemConf.cpp:86 recordLastGood,238 LockBusy; E/es-app/tests/unit/SystemConfTests.cpp:465,488|Q/2026-10-03-m7-p1/settings-before.log,settings-after.log,settings-syntax.log; Q09/settings-11|
|349,381|R/rasteratops-settings-archive:8 select_settings_archives; cloud_scan:214; cloud_restore:2046; E/GuiMenu.cpp MINE parsing|Q/2026-10-03-archives-runtime; Q09/runtime-12 and guest-11 C/H/A|
|350,352|R/cloud_scan:153; cloud_content_restore:361,403,504,1308; cloud_setup:497,569; E/es-app/src/guis/GuiMenu.cpp:4060,5294,5440|Q09/guest-11 F/G/H/A/C/D, visual-review.json; docs/es-menu-map.md:132–142|
|351,462|R/cloud_oauth:646,652,1016,1179; cloud-signin-window.c FINISHING_PAGE|Q10/signin-ui-14,15,16; Q/2026-10-06-local-cloud/signin-payload-continuity.json and three protocol reports|
|353,356|R/cloud_migrate_layout:497 relocate,582 merge_into,970 read_marker,997 write_marker,1023 recovery,1216 migration_step_1|Q09/guest-11 A/B/E/H/I/L/T23/T26; optins-11; Q/2026-10-05-p3-reconciliation/cloud-boundaries-01|
|363,364,429,430|R/cloud_scan:153; cloud_backup:810,826,1670; E/GuiMenu.cpp:5495,5585,5602,7455 and main.cpp:683|Q09/guest-11 E/I/J/K/L/T08/T11/T12; runtime-12/artifacts/timing/comparison.json and retained timing-proof.py/installed-samples/all-samples/timestamp-controls|
|365|tools/rasteratops-cloud-layout-test; tools/rasteratops-vm-cloud-epic; docs/rasteratops/cloud-folder-state-table.md:173+|Q/2026-10-03-m7-coverage/actor-case-map.json; Q09/guest-11; focused boundaries; reconciliation/guest-negative|
|366,390|tools/cloud-test-backend:799; tools/last-good-scripts-test:4628,9034,13334|Q/2026-10-03-m7-p1/host-suite-before-fixture-fix.log,host-suite-after.log; current local protocol round-trip.log files|
|376|R/cloud_scan:223; cloud_restore:2093; S/backuptool:113|Q/2026-10-03-archives-runtime; Q09/runtime-12 actual inherited RC2 archive/local+cloud restore|
|377|R/cloud_backup:810,1670; cloud_restore:821,1688,1738|Q/2026-10-03-directory-probe-host; Q/2026-10-03-m7-final-runtime literal superseded S3 branch controls|
|379|R/cloud_migrate_layout:118 backup_pointer_for|Q/2026-10-02-cloud-remediation; archive runtime; focused boundaries T20 follow/settle|
|380,407|R/cloud_migrate_layout:113 content_unset,132 earlier_layout,657 set_pointer; cloud_setup:770|archive root-transitions/transitions.json; focused boundaries T21; Q/2026-10-03-cloud-root-label and cloud-root-replacement02|
|391|R/cloud_migrate_layout:693 resumable,709 derived content,1023 recovery|Q/2026-10-03-m7-coverage/predecessor-before.log,predecessor-after.log,boundary-after.log,legacy-record-after.log; Q09/predecessor-09|
|392|R/cloud_backup:2446 and cloud_restore:2225 remote validation|Q/2026-10-03-m7-coverage/unlinked-before,unlinked-local-paths-before.json,unlinked-after.log; Q09/guest-11 T19|
|401|R/cloud_content_transfer:28,53,65,85 bounded_content_rclone; callers in content backup/restore|Q/2026-10-03-content-network; Q/2026-10-03-replacement-links; Q09/link-10|
|421|projects/ROCKNIX/packages/rocknix/profile.d/001-functions:385 prepare_settings_temp and writers429/447/480/572; S/chksysconfig:69|tools/settings-modes-test; Q09/settings-11; original02163 mode failures|

Research cautions:

- First nonempty archive identity directory is selected before label filtering;
  compare mixed-label/multiple-identity fixtures with intended precedence.
- #353 mentions an actual kill. Operation-boundary fault injection is not
  automatically evidence of a real process kill or arbitrary power cut.
- Focused36-case boundaries used replacement10 and a distinct second guest
  for all nine recovered clouds. Original T23 reset the same guest's config.
- #363/#429 cite runtime07/28ms; later runtime12 reports24ms. Neither is the
  current14 single-sample smoke. Preserve exact clock, byte and stamp controls.
- #351 now uses handset/Mobile-UA and payload continuity; authenticated
  Dropbox remains optional/unverified under D-QA-058/#463.
- Public docs, specific named tools and French/syntax chronology require
  their own evidence even if equivalent-looking VM frames exist.

## Proxy/dependencies lane

Helper `/root/m7_qa05_resume_proof` was reused solely for read-only research.
P=`projects/ROCKNIX/packages/network/raofflineproxy/`. U is the unpacked patched
879b158 Linux source under frozen14's build.pixelelated-GENERIC_X64.x86_64/build/.

| Issues | Source anchors | Raw artifact leads |
| --- | --- | --- |
|361|P/package.mk pin/hash;16 patches; cache-indexed:87/130/164; tools/raofflineproxy-integration-test:77–170|Q/2026-10-03-proxy-refresh; Q/2026-10-06-proxy-879b158/equivalence.json,patched-equivalence.json; proxy-consent/host-b09-01,scripts-b09-01; Q14/preparation; docs/upstream/raofflineproxy|
|362|packages/web/libsoup/package.mk3.8.0 and webkitgtk2.54.1|Q/2026-10-03-dependencies; reconciliation/cold-webkit-libsoup.json; Q10/memory-12,signin-ui-14/15/16,signin-1g-13,signin-provider1g-05|
|384|U/rom_cache.py:362,391,437; U/flusher.py:185,283,505|candidate-preflight/subset-old-source.txt; Q14/subset-11/provider-requests.json,flush-first.json,flush-second.json,assertions.json,guest-proof.log,provenance.json,completion.json|
|386|ROCKNIX overrides glslang16.6.0, SPIR-V Tools ef96ed7 and headers4965431, shaderc2025.3, cbindgen0.29.4,tllist1.1.0; tools/fork-package-freshness:58,147|Q/2026-10-03-dependencies/archives.json,compat-build.log,cbindgen-build.log,glslang-known-good.json,translator-header-compat.json,tllist-live.log; Q14 freshness|
|408|P/patches/018; U/config.py:72,466; P/system.d/raofflineproxy.service:28|Q/2026-10-03-proxy-identity; proxy-runtime; Q14/proxy-14 installed preservation|
|414,452|P/sources/raofflineproxy-ctl:240–258 and SQL568/581/613/680/683/768/1010/1021; U/storage.py:105–150,553; rc-preflight:132|Q/2026-10-04-proxy-schema-note; 2026-10-05-proxy-schema-3036478/schema-review.json,before.log,after.log,frozen11-negative.log; Q14/pre-freeze-schema/default scripts|
|419|Historical aec99c source/patch equality and retained98d0 cache provenance|Q/2026-10-04-proxy-aec99c; 2026-10-04-pixelelated-1e6a-qualification/proxy-04|
|426|7252fc changed consumed Python interfaces; old-native equality insufficient|Q/2026-10-05-proxy-7252fc; Q09/proxy-11,subset-08,boot-04,image-11|
|451|tools/raofflineproxy-integration-test:132–170 streamed/list predecessor APIs and two reopens; actual parent-coupled libchdr607694c|Q/2026-10-05-proxy-3036478/host01-failed,host02; Q14/proxy-14/native-tests.log,native-result.json,assertions.json|
|457|P/patches/019; U/usage_stats.py:86,121,234,236,244; usage_report.py:166; corruption consent in proxy_service.py:1342|Q/2026-10-06-proxy-consent/early-consent-before.json,early-before.log,early-fixed.log,consent01-failed; Q14/consent-02/guest.log,summary.json,collector-events.json,usage-only-counter-observation.json|
|465|tools/ra-ui-test:127–220; ra-offline-test:197–203,289–298,403,464,470–503; E/es-app/src/ProxyCards.cpp:122–186,536|Q/2026-10-06-ra-ui all three owners, qualification/visual manifests; separate Q/2026-10-06-ra-award|
|327|E/es-app/src/guis/GuiRetroAchievementsSettings.cpp:53,95–104,408,431–435|docs/qa-frames/2026-10-03/327; Q10/ui-14; separate website screenshot commit4f6df54|

Research cautions: current source879 Linux/native equivalence to tested b09
is not a fresh879 test execution. Both actual predecessors303/865 are separate
11-case executions. Schema-comment parity is not schema-behavior proof.
Ordinary RA33 and synthetic installed UI109 are separate; the edited ordinary
runner has not been rerun in full. Refusal UI is EN640 only. Early-consent
collector proof does not prove scheduler cadence/UI/provider behavior. The
1GiB example.org and public Dropbox workloads have distinct RSS comparisons.
Use the ROCKNIX SPIR-V override, not the generic recipe. Retained old identity
wording does not require a fielded Rasteratops predecessor after the rename.

## Identity/VM/infrastructure lane

Helper `/root/pixelelated_frozen_resume_proof` was reused for source research;
it did not perform a fresh-context resume proof for this checkpoint.

| Issues | Source/check anchors | Raw artifact leads |
| --- | --- | --- |
|383,344|tools/rasteratops-candidate-store:28; distributions options/version; scripts/image:106,160,166|Q14/build,qa-18/defaults,qa-18/upgrade; image-14; inventory-10; broader Q09/sweep-09 needs continuity|
|337,409|NAMING.md; scripts/image; ES ApiSystem.cpp:172,452; GuiMenu.cpp:1505; inert rocknix-update; BusyBox init predecessor check|Q14 installed identity/payload; RC2 rehearsal; current local cloud; Q/2026-10-04-pixelelated-source,ocean; art proofs|
|359,397|LICENSE.md/TRADEMARK.md; scripts/image:208–214 mode0644|Q14 payload clean/upgrade JSON; Q/2026-10-03-image-policy;14 known P5 licence metadata gaps|
|357|report-stats inert script/masked timer; tools/rasteratops-identity-check:80–99|Q/2026-10-03-m7-final-runtime/artifacts/identity; locate current installed observations|
|310|ES InputConfig/InputManager enumeration release; FileData lifecycle trim; Mesa executable-heap/screen-cache and SDL mode cleanup patches; tools/es-launch-memory|Q/2026-10-03-launch-memory; Q10/memory-12/artifacts/software-10,software-sync-50,virgl-10|
|332|Nova ledcontrol/battery_led_status; ES GuiMenu.cpp:2140–2181,OptionListComponent.h:86; tools/nova-led-test|Q/2026-10-03-led/before.log,after.log,ui-reselection; physical illumination remains later|
|424|quirks/profile.d/999-export:8; identity-check:116–130 actual child|Q/2026-10-04-es-identity-export; Q14 payload/identity frames|
|433|GENERIC_X64 quiet option; BusyBox init:1274–1279 no redraw/debug opt-out|Q10/boot-qualification-05 four clean/upgrade640/1280 matches and negative controls; earlier failed640 kept|
|436|ES GuiMenu.cpp:2321–2350 hasSelection guard; tests/gpu-governor-save.py|replacement07 diagnostic03; replacement08 lifecycle; Q14 clean/upgrade ES lifetime/journals|
|447|GENERIC_X64 sway-generic-x64 virtio/virgl selector and service drop-in|Q/2026-10-05-generic-x64-pixman/selector-04; Q10 software/upgraded/virgl sign-in and1GiB; current14 installed renderer JSON|
|449|Q/2026-10-05-vnc-observer/persistent_viewer.py bounded partial reads and idle; test_observer.py|controls.log; Q09 failed signin-ui-12 and fresh13|
|454|tools/vm-pair:84; vm-stop:13–53 pidfd/identity/timeout; vm-stop-test|Q12 qa-15 failed and continued qa-17 custody/lifetimes|
|455|tools/vm-qa:366,448–462; vm-manager-system-check|Q12/qa-17 manager systems/selected/system-check and parent-review PNGs; inherited FBNeo baseline error|
|393,394|watch-job:175–208; watch-build:71–116; build/install/image/Makefile entrypoints|Q/2026-10-03-watch-job/test-watch-job.py,test-watch-build.py and logs; actual14 owner receipts|
|395|D-WORKFLOW-143; active supervision versus disconnected delivery|Q/2026-10-03-watch-delivery; diagnostic07 terminal17:04→observation17:08 gap; two delivery criteria remain open|
|410|tools/host-maintenance/reclaim-swap idle/headroom/recycle/lock; installer policy/order/rollback; test-swap-reclaim|prior410 evidence/final-*; Q/2026-10-04-host-swap-rollout actual owner grant/busy/recycle/no-op|
|435,441|replacement07 build-attempt-02 cwd guard; Q09 boot-qualification-04 dependency/custody|cwd-controls, original build failure; boot03 failure and boot04+successor-provenance|
|444|tools/watch-build-submit; Q/2026-10-05-watch-submit/test-submit.py|controls.json; interrupted guest10 and durable guest11; submission0 is not job completion|
|459,460|tools/fork-worktree guarded removal and permission scan; D-INFRA-017|Q/2026-10-05-build-storage/approved-cleanup-20261006 exact five roots; Q/2026-10-06-worktree-permissions controls-02|

Research cautions: #337's guest updater network-capture artifact was not located
by the helper; absence is not yet a finding. Future pixelelated update acceptance
is distinct from actual RC2 adoption. #344 contract P2b/P3/P4 are current M7.P5
device/release work, not current execution-phase P2/P3/P4. Historical lowercase
rasteratops/path wording is superseded by D-WORKFLOW-144. Website delivery,
source-bundle licences, notes and physical smoke remain explicit later gates.

## Prior provenance and Tier B leads

Prior375 baseline b2378d9c33/ES e108699ea, cloud354+release344+identity337 scope;
prior410 host-helper-only scope. Prior375 blind/refutation Fable5.1 provenance
and410 refutation provenance are receipt-only sources until Phase2.5; their
review bodies/AC verdicts have not been read. Earlier September29 #313 audit
owns320's inherited disposition; September14 offline-RA/September28 fixes
headers are additional provenance leads. Do not treat any as the current audit.

Tier B inventory: Q09/guest-11 visual manifest32 frames/15 UI cases;
cloud-ui-08 nine frames UI17/UI26; Q10/signin-ui-14/15/16 each15 frames;
Q10/ui-14 bilingual pages; Q10/boot-qualification-05 four boot profiles;
Q12/qa-17 manager-review; Q14/qa-18/review; current UI23-frame manifest.
These counts and file pointers need primary verification. The current UI23
has already been directly reviewed by root during the prerequisite proof.
No new page-scale design review is implied for unchanged surfaces; material
post-retro changes and previously unseen cross-page flows need fresh review.
