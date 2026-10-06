# Independent blind code review — pixelelated M7 P4, Milestone tier

You are the external Anthropic reviewer in a two-model code audit, not a five-seat council. You cannot open files or run tools: all source and observations you may cite are in this packet. Primary verdicts, hypotheses, prior-audit answers and proposed findings are withheld. Find defects, unsafe interactions, scope/evidence gaps and contradictions independently. For each item give a stable ID B-01 etc., severity Critical/High/Medium/Low, precise packet file:line, concrete trigger, actual versus required behavior, and a falsifying observation. Distinguish an observed code defect from an unexecuted exact criterion. State what you cannot judge. Do not assume a missing excerpt proves missing code. Do not treat future P5 device/publication work as newly discovered implementation failure.

Frozen distribution7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2, ESf6f0c134212bc696f2f6a747c8d390a588f2f0ce, proxy879b158995d412af434301ebdae581f66b8b6d57; immutable bundleb77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1. Current scope is P1–P3 product fixes and qualified VM behavior; P5 physical/device/source/publication is subsequent. New identity is lowercase pixelelated; only ROCKNIX→pixelelated adoption is required. Stored interfaces and upstream credits remain compatible. Dropbox authenticated trust-page observation is owner-waived as a gate; WebDAV/SFTP/S3 local runtime and dedicated RA real award have run. No product edits occurred during the audit.

Evidence domain: actual14 is current;09→10 changed rendering,10→14 changed proxy/native/consent only. Older target evidence is reused only for byte-identical relevant installed payloads, never asserted as a fresh current14 run. Host controls are not target execution. A synthetic local HTTP flusher test is not a real provider run. No physical-board observation is inferred from a VM.

## Exact forward criteria and primary observations (verdict columns removed)


### I320-L32 — inputs/issues/320.md:32

Requirement: `recordLastGood` is taken under the same lock as the read it records, or compares the live file's identity (size and mtime, or a hash) before publishing and skips when it changed: the `es-conf-tests` case `a script's newer good state published between the read and the record is not overwritten` seen to FAIL on the code before the fix and PASS after.

Artifact observations: E/es-core/src/SystemConf.cpp:86–108 reacquires PidLock and compares the complete current choice before atomic publication; E/es-app/tests/unit/SystemConfTests.cpp:465–486 constructs the intervening newer script publication. Fresh evidence/es-checks-02/activity/es-conf.log:10 cases/119 assertions pass, rc0; checks.json retains compile/run argv and sealed exact ES source. Original settings-before.log at docs/qa-logs/2026-10-03-m7-p1 fails this assertion.


### I320-L33 — inputs/issues/320.md:33

Requirement: The `LockBusy` path does not publish a recovery record from a read it could not lock: a second `es-conf-tests` case, seen to FAIL first.

Artifact observations: E/es-core/src/SystemConf.cpp:250–266 skips record publication on RecoveryWrite::LockBusy for both temporary and backup recovery. SystemConfTests.cpp:488–505 holds the real lock and supplies divergent complete temporary/recovery states. Fresh10-case/119-assertion execution rc0; prior settings-before.log records its specific failed recovery-record comparison.


### I320-L34 — inputs/issues/320.md:34

Requirement: On a guest, a script write of `system.cfg` raced against the interface's recovery (a damaged live file restored at start-up while `set_setting` writes) leaves the last-good record at the script's newer state: the record's bytes compared after the race, in `tools/vm-qa`'s `last-good` suite or a proof script under `docs/qa-frames/`.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/settings-11/artifacts/result.json and guest.log retain20 installed checks: same ES PID1989 pauses after lock release, actual shell writers publish newer state, resumed ES preserves identical live/record SHA256c185423fc387f230447eec8c54c9beaaadd538af08d82fc99fcc14729ea416d3. Fresh current14 staged hashes match all three recorded installed ES/profile/chksysconfig bytes exactly.


### I320-L35 — inputs/issues/320.md:35

Requirement: `docs/audits/2026_09_29-milestone-audit-of-the-313-fixes/05-punch-list.md` § Deferred cites this issue, and its Phase 7 row records the commit.

Artifact observations: docs/audits/2026_09_29-milestone-audit-of-the-313-fixes/05-punch-list.md:83 retains the #320 deferral;113–123 add the Phase7 follow-up naming full ES39f8883545537d5274708ea85c4683612078a957 and guest-proof boundary.


### I349-L29 — inputs/issues/349.md:29

Requirement: On the transfer page, the SETTINGS restore row's line under the label names the device the archive to be restored came from, read from the label in its file name (`backuptool` prints it; the interface reads it): a 640x480 frame from a `tools/vm-walks` walk shows `<DEVICE>, <DATE>` (D-CLOUD-164).

Artifact observations: E/es-app/src/guis/GuiMenu.cpp:4878–4894 parses MINE and displays the archive label/date. Directly reviewed evidence/archive-frames/04-A-options-after-move.png shows GENERIC X64,09/30/2026 at640x480, from guest11 on replacement09.


### I349-L33 — inputs/issues/349.md:33

Requirement: `docs/es-menu-map.md` carries the SETTINGS row's two states, offered with the device and date or dimmed with `NO SETTINGS BACKUP FROM THIS DEVICE YET` (D-UI-039, D-CLOUD-162), and `tools/es-menu-map-check` passes in `tools/vm-qa`'s `menumap` suite. *(Rewritten 2026-10-01: the choice page it named is superseded.)*

Artifact observations: docs/es-menu-map.md:139 includes both SETTINGS states. Fresh tools/es-menu-map-check --es-src E exited0 (host-checks-01/activity/menu-map.log).


### I349-L34 — inputs/issues/349.md:34

Requirement: The public page for cloud sync says the SETTINGS row restores this device's own newest backup and is dimmed when the cloud has none from it (docs follow-up with #42, `documentation-accuracy.md`). *(Rewritten 2026-10-01: a restore from another device is not offered.)*

Artifact observations: #344 contract publication stages and docs/rasteratops/release-readiness.md retain public-site delivery as a later gate; the website follow-up remains tracked with#42.


### I349-L42 — inputs/issues/349.md:42

Requirement: After the scan page (#350), the SETTINGS restore row is offered only when the cloud's Backups folder holds an archive whose label equals this device's `cloud_device_id --label`; with the QA cloud seeded with a foreign label only, guest d's 640x480 frame shows the row dimmed with its reason, and with its own label seeded the row is offered with `<DEVICE>, <DATE>` (D-CLOUD-164) under it.

Artifact observations: cloud_scan:214–239 writes label-filtered MINE; GuiMenu.cpp:4878–4894 disables absent/invalid MINE. Guest11 C/logs/run.log records completed foreign-only scan with empty MINE; evidence/archive-frames/04-C-after-scan.png and04-A-options-after-move.png directly show the two required row states.


### I349-L43 — inputs/issues/349.md:43

Requirement: A restore never takes another device's archive by default: the cloud restore selects this device model's newest compatible archive and passes it to `backuptool`, and its journal line names the label it chose; the foreign-label case on guest d leaves `system.hostname` unchanged.

Artifact observations: cloud_restore:2046–2140 shares the directory selector and chooses the own-label newest archive before its explicitly permitted console fallback. Runtime12 archive/writer-selection.json and022/023/026/027.log prove the selected archive is restored and sentinel bytes agree. Guest11 C shows the UI row disabled.


### I349-L44 — inputs/issues/349.md:44

Requirement: The scan page's line reads, while it runs, the words approved for #350 (proposed: `CHECKING WHAT SETTINGS AND CONTENT YOUR CLOUD HAS FOR THIS DEVICE...`), and the outcome vocabulary when it ends (`es-player-text.md`); frames from the walk show both.

Artifact observations: E/es-app/src/guis/GuiCloudTransfer.cpp:1003–1011 selects the approved full sentence or whole-clause640px fallback. Directly reviewed H scan frames in evidence/archive-frames show CHECKING WHAT YOUR CLOUD HAS FOR THIS DEVICE..., with phases1 and3; A completed options are the successful auto-continued outcome.


### I392-L18 — inputs/issues/392.md:18

Requirement: Empty/failed remote discovery produces a nonzero setup refusal for both transfer scripts, with unchanged pointers/payloads and no create-folder offer; before/after production-script receipts retained.

Artifact observations: cloud_backup:2446–2460 and cloud_restore:2225–2238 require a nonempty remote prefix ending in colon before path operations. Original docs/qa-logs/2026-10-03-m7-coverage/unlinked-before.log has four failures; unlinked-after.log has13 passes. Fresh evidence/host-checks-01/activity/cloud-layout.log passes each empty/failed-discovery T19 case.


### I392-L19 — inputs/issues/392.md:19

Requirement: A writable local path supplied as the cloud path is not read or written when no remote is linked; configured-cloud controls continue to pass.

Artifact observations: Fresh T19-local-path-cloud_backup/cloud_restore cases in evidence/host-checks-01/activity/cloud-layout.log exercise actual writable local-path fixtures; the original unlinked-before.log records allfour failures. Configured-cloud actors in the same316-case run pass.


### I392-L20 — inputs/issues/392.md:20

Requirement: Candidate guest evidence records the refusal/outcome and unchanged bytes for direct and automatic calls.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest-11/artifacts/cloud-epic/T19/logs/run.log:12 actual installed assertions, covering direct/automatic backup/restore setup refusal and unchanged cloud bytes/pointers. Source continuity09→14 is in evidence/candidate-product-continuity.json.


### I421-L23 — inputs/issues/421.md:23

Requirement: All four settings writers preserve restrictive input modes, including a private recovery record and permissive pre-existing temporary, with byte-correct set/delete/sort/pair operations; old-source controls fail and corrected controls pass.

Artifact observations: 001-functions:385 prepare_settings_temp intersects source modes and caller umask before bytes are written; four callers at429/460/494/598 gate publication on it. docs/qa-logs/2026-10-04-settings-race-and-modes/modes-old.json records22 failing controls; modes-new.json passes29. Fresh host-checks01 scripts.log repeats the29 cases using current14 image tools.


### I421-L24 — inputs/issues/421.md:24

Requirement: chksysconfig backup/restore retains the privacy of its source/destination; failures leave original published bytes and report failure.

Artifact observations: chksysconfig:69–78 put prepares restrictive destination temporary, streams with cat, then atomically renames. modes-new.json and installed replacement09 settings11/artifacts/modes.json cover backup/restore in allfour mode states plus five refusal cases; fresh scripts.log passes them again.


### I421-L25 — inputs/issues/421.md:25

Requirement: Corrected image clean/actual-RC2 qualification plus installed settings-race/mode proof pass; exact hashes bind the new candidate and original02163 results remain retained.

Artifact observations: replacement09 settings11 result.json has20 installed race/identity checks and modes.json29 cases. Fresh evidence/settings-payload14.json matches ES,profile,chksysconfig and BusyBox hashes exactly. Current14 qa18/defaults/report.md has all15 suites and qa18/upgrade/rehearsal.log records actual RC2→7afa9efcfc state preservation. Original02163 receipts remain under2026-10-04-pixelelated-02163-qualification.


### I376-L22 — inputs/issues/376.md:22

Requirement: A regression case runs the production reader with RASTERATOPS OS identity and selects the same-device legacy ROCKNIX archive; its negative control at the old commit fails. The suite's PASS lines and fixture bytes are retained.

Artifact observations: Production rasteratops-settings-archive:1-43 and cloud_scan:190-249 retain ROCKNIX/RASTERATOPS names. docs/qa-logs/2026-10-02-cloud-remediation/baseline-results.json records the actual T24 writer-directory/legacy failures; focused-fixed-results.json records their corrected selection. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.


### I376-L23 — inputs/issues/376.md:23

Requirement: New/legacy same-device and foreign-device fixtures prove selection prefers this device model's newest compatible archive, the transfer-page SETTINGS row is gated on MINE (D-CLOUD-156/162), and the console retains its deliberate NEWEST fallback when only a foreign archive exists (D-CLOUD-067); selected names and restored sentinel hashes are retained.

Artifact observations: docs/qa-logs/2026-10-03-archives-runtime/extended/selection-matrix.json retains current, legacy, healed-ID, flat and foreign-only selected filenames plus sentinel hashes; GuiMenu.cpp:4878-4894 gates the row on MINE. cloud_restore:2030-2170 keeps the documented console fallback. docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest-11/artifacts/cloud-epic/C/logs/run.log and evidence/archive-frames/ retain disabled foreign-only UI. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.


### I376-L24 — inputs/issues/376.md:24

Requirement: Local backup, pre-restore snapshot, revert and retention cases prove the documented legacy/new-name contract without dropping recoverable files; retained names and restored sentinel hashes are in the log.

Artifact observations: docs/qa-logs/2026-10-03-archives-runtime/local-recovery/assertions.json and recovery-cases.json contain actual ROCKNIX and RASTERATOPS archive paths/hashes, original sentinel hashes, live PRE_RESTORE snapshots, protected history and final history. local-recovery.py:15-70 injects failure after real extraction; backuptool:1349-1380 excludes the active snapshot before date-name trimming; :1455 onward snapshots before extraction. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.


### I376-L25 — inputs/issues/376.md:25

Requirement: The final branded image's RC2 upgrade rehearsal preserves existing settings archives and restores them through the cloud and local recovery entry points; logs identify image hashes and the selected archives.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/archive/assertions.json (14 assertions), writer-selection.json and provenance.json identify the inherited actual RC2 archive and production cloud/local restores. Raw logs010,011,016,017,022,023,026,027 retain selected archive, writer execution and restored sentinel SHA85704db48b3889a61f0cc9d70a0df1bea530c9e153f995f6cf68752bc7a343d3. Replacement14 qa18 upgrade rehearsal separately preserves actual RC2 state (26 assertions); evidence/candidate-product-continuity.json binds unchanged archive code09→14.


### I381-L24 — inputs/issues/381.md:24

Requirement: A candidate guest creates a settings archive through production cloud_backup, then opens RESTORE FROM CLOUD; the scan selects the actual archive and a640x480 frame shows SETTINGS enabled with the approved device/date text. Archive path, scan facts and frame are retained.

Artifact observations: docs/qa-logs/2026-10-03-archives-runtime/extended/ui-writer-selection.json identifies actual production archive2026_10_03-182015-GENERIC-X64-ROCKNIX_SETTINGS.tar.gz, MINE/NEWEST equality and count1. Directly viewed extended/restore-page.png at640x480: SETTINGS enabled, GENERIC X64,10/03/2026. docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/archive/writer-selection.json independently identifies the later actual production writer archive2026_10_05-043142-GENERIC-X64-ROCKNIX_SETTINGS.tar.gz and SHA0b9f0b2e0259f2a5c06dbc0750f6b5d1ad0ad6c7c7d74b80277f16481f7cacc5.


### I381-L25 — inputs/issues/381.md:25

Requirement: Production restore consumes exactly the archive the scan selected; sentinel hash and journal verify it. Current device, legacy device name, healed previous IDs, foreign-only and flat-root fixtures preserve the documented selection behavior.

Artifact observations: docs/qa-logs/2026-10-03-archives-runtime/extended/selection-matrix.json identifies archive/sentinel per current, legacy, healed-ID, flat and foreign-only fixture. docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/archive/assertions.json includes exact journal-selected archive and restored sentinel assertions; raw022/023/026/027 corroborate actual restore and bytes. Shared selector rasteratops-settings-archive:1-43 supplies both cloud_scan and cloud_restore. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.


### I381-L26 — inputs/issues/381.md:26

Requirement: The old scan fails a regression using writer-shaped per-device directories; the corrected scan passes. Existing flat-root cases remain compatibility controls, not the only fixtures.

Artifact observations: docs/qa-logs/2026-10-02-cloud-remediation/baseline-results.json: writer-directory T24 controls fail on original code while the legacy flat-root control passes. focused-fixed-results.json and fresh evidence/host-checks-01/cloud-layout-results.json retain fixed current/legacy/healed/flat/foreign cases. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.


### I381-L27 — inputs/issues/381.md:27

Requirement: The final RASTERATOPS image also discovers legacy ROCKNIX-suffixed archives under those folders (#376), and main WebDAV/S3 plus pair migration suites remain green.

Artifact observations: Replacement09 runtime12 archive assertions and selected production ROCKNIX-suffixed archive plus source continuity09→14. docs/qa-logs/2026-10-06-local-cloud/{webdav,sftp,s3}/report.md and completion.json bind actual image c7df6a6f428086f79a377ca1b049f20694f34a868987cf12c493c78eab7b2254 and three106PASS/0FAIL/0SKIP executions. Focused cloud-boundaries01 identities.json identifies two distinct VM boot/device IDs; pair-copy-Backups-{interrupted,final,follower}.json retains preserved hashes, new pointers and follower journal. results.json covers all nine fault/retry/follower cases.


### I356-L75 — inputs/issues/356.md:75

Requirement: `cloud_migrate_layout` runs numbered steps from the marker's version to the build's, each with the move dialog, each copy-verify-delete, each a journal line naming the step; a `tools/pixelelated-vm-cloud-boundaries` case (paired with the retained MOVE UI proof) seeds layout 1 and ends at layout 2 with the marker written and nothing lost (hash list before and after).

Artifact observations: cloud_migrate_layout:1216-1525 dispatches step1 and records begin/backups/saves/discarded/content/complete. docs/qa-logs/2026-10-05-p3-reconciliation/cloud-boundaries-01/proof.py:150-184 seeds literal layout=1, verifies all four tiers, layout=2 bytes, old-file absence and six journal stages; artifacts/results.json records PASS. Existing guest09 MOVE frame sequence is retained under guest-11 A. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.


### I356-L77 — inputs/issues/356.md:77

Requirement: Fault injection after each completed tier and at marker publication followed by retry preserves both sides, completes without duplicate/lost state, and lets a second guest follow; logs identify the numbered step and hashes.

Artifact observations: docs/qa-logs/2026-10-05-p3-reconciliation/cloud-boundaries-01/proof.py:150-184 and artifacts/results.json cover four copy, four deletion and one marker fault followed by recovery/repeat. identities.json and all nine follower.json files identify guest b; inspected copy-Backups intermediate/final/follower hashes and journal. cloud_migrate_layout:970-1215 binds retry record to paths/config and :1428-1518 records each tier. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.


### I356-L78 — inputs/issues/356.md:78

Requirement: The step for `/GAMES` and `/ROCKNIX` is step 1 and is the one #353 ships; the design note lives in `docs/rasteratops/cloud-layout.md`.

Artifact observations: docs/rasteratops/cloud-layout.md:1-115 specifies strict markers, numbered step1, JSON recovery record, copy/verify/delete and actual predecessor boundary. cloud_migrate_layout migration_step_1 is the only registered transition; fresh host and retained VM evidence cover GAMES and ROCKNIX.


### I380-L22 — inputs/issues/380.md:22

Requirement: Regression fixtures distinguish missing CONTENT_REMOTE, explicit empty cloud root, a derived old Content folder and a named custom folder for join, follow, settle and apply; log records before/after values.

Artifact observations: cloud_migrate_layout:100-150 distinguishes key presence; :657-795 and :1450-1510 preserve explicit root/custom choices. docs/qa-logs/2026-10-05-p3-reconciliation/cloud-boundaries-01/proof.py:200-214 and artifacts/results.json exercise all16 join/follow/settle/apply × omitted/root/derived/custom cases with before/after pointers and bytes. October2 baseline-results.json fails the four root-overwrite cases; focused-fixed-results.json passes. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.


### I380-L23 — inputs/issues/380.md:23

Requirement: On GENERIC_X64, an explicit root holding ROMs/BIOS remains the selected location after a layout transition and the scan lists/restores the original sentinel; missing-key fixtures get the documented default.

Artifact observations: docs/qa-logs/2026-10-03-cloud-root-replacement02/attempt-02/artifacts/{transitions,assertions}.json retain actual pointer changes, root ROM/BIOS scan output and two restored sentinel checks per mode. docs/qa-logs/2026-10-05-p3-reconciliation/cloud-boundaries-01/T21 current-name matrix independently preserves root bytes and assigns defaults only to missing keys. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.


### I380-L24 — inputs/issues/380.md:24

Requirement: The contradictory seeding/migration fixtures and state table agree on one representation without silently replacing a player-selected folder; existing content-root tests remain green.

Artifact observations: docs/rasteratops/cloud-folder-state-table.md:173-289 maps each actor and specifies missing/root/custom distinctions; executable T21 matrix and older contradictory fixture now omit the key where unset was intended. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.


### I391-L22 — inputs/issues/391.md:22

Requirement: Historical RC2/run101 controls reproduce all four failures before the fix, then recover every owned payload and complete marker publication; retained logs identify predecessor script hashes and before/after pointers/hashes.

Artifact observations: docs/qa-logs/2026-10-03-m7-coverage/predecessor-before.log:6PASS/4FAIL includes RC2-content, run101-discarded/content/marker failures; predecessor-after.log:15PASS/0FAIL, plus fresh316 suite. docs/qa-logs/2026-10-05-pixelelated-replacement-09/predecessor-09/artifacts/predecessor/RC2-content-inherited.json retains exact predecessor SHA76f003f52d98056bda9685d44cb224d4c4034089e6ce70509ffaa294da275f27 and installed SHAfe184dc2a20f991d35402065c36373f915aa821c96f15b8dbfdd09ba8e533555, split pointers and payload hashes.


### I391-L23 — inputs/issues/391.md:23

Requirement: Recovery remains interruptible and repeatable; controls retain custom content/root choices, refuse unmarked foreign destination conflicts, and preserve both versions when an allowed merge is required.

Artifact observations: cloud_migrate_layout:693-795 and recovery/relocate sections only recover known old tiers, bind the record and refuse foreign collisions. predecessor-after.log includes reinterrupted, boundary-root/custom/foreign/fleet PASS; legacy-record-after.log covers old schema1 compatibility; docs/qa-logs/2026-10-05-pixelelated-replacement-09/predecessor-09/RC2-content-reinterrupted-{new-fault,recovered}.json preserve identical payload hashes across failed marker and successful retry. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.


### I391-L24 — inputs/issues/391.md:24

Requirement: Candidate VM/upgrade proof verifies the inherited partial state and its recovery, naming the image and showing payload hashes and the supported retry/move path.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/predecessor-09/predecessor-proof.py:1-108 checks exact upgraded buildcf511ce79b83cba7fea8b14cfa3d04fb13e4b4fb and unmodified installed script, executes transferred RC2 script, retains five inherited states, then installed recovery. artifacts/predecessor/assertions.json has65 passing assertions; reinterrupted scan reports migration-pending, needs-step returns0, retry publishes exact layout2.


### I407-L18 — inputs/issues/407.md:18

Requirement: A focused old-code control observes the empty destination; corrected output clearly names the cloud root while retaining named-folder output.

Artifact observations: docs/qa-logs/2026-10-03-cloud-root-label/check.py and check.log directly execute production set_pointer. Old empty-root output has a blank destination; corrected output says the root of your cloud. Named /Mine/ROMs output and exact stored values are controls. Fresh host suite includes cloud migration regressions.


### I407-L19 — inputs/issues/407.md:19

Requirement: Explicit CONTENT_REMOTE remains empty after the actual transition and root ROM/BIOS restores remain byte-identical on the resulting image.

Artifact observations: docs/qa-logs/2026-10-03-cloud-root-replacement02/attempt-02/artifacts/transitions.json and assertions.json:22 actual guest assertions, four real pointer transitions, root preserved, root ROMs/BIOS scanned and both sentinels restored each time. cloud_migrate_layout set_pointer uses a display-only phrase for empty content while persisting the original value.


### I350-L24 — inputs/issues/350.md:24

Requirement: Opening BACK UP TO THE CLOUD or RESTORE FROM THE CLOUD opens CHECKING YOUR CLOUD before any options (D-CLOUD-167), with the live line and CANCEL as the one way out while it runs (D-UI-078); the options page follows when the listing is in. A `tools/vm-walks` frame sequence shows menu, scan page, options, and no frame with a card drawn over a dialog.

Artifact observations: GuiMenu.cpp:5440-5475 opens cloud_scan in GuiCloudTransfer before creating options; cloud_scan:153-255 persists facts then done. Directly viewed original guest11 H scan0/1 and A options, plus G scan0 and backup options; CANCEL is the running control, no options dialog under either scan. guest11/{H,A,G}/logs/run.log retains walk order.


### I350-L25 — inputs/issues/350.md:25

Requirement: When the comparison fails (the cloud unreachable: the dead port of `tools/cloud-test-backend`), the page says why in the outcome vocabulary (`COULDN'T FINISH - …`, `es-player-text.md`) and offers TRY AGAIN beside CLOSE; a frame shows it.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest-11/artifacts/cloud-epic/F/logs/run.log: dead port produces no success stamp,3PASS/0FAIL. Directly viewed01-F-outcome.png: CHECKING YOUR CLOUD, COULDN’T FINISH, CLOUD FOLDER — YOUR CLOUD STOPPED ANSWERING, CLOSE and TRY AGAIN.


### I350-L26 — inputs/issues/350.md:26

Requirement: `docs/es-menu-map.md` carries the page (D-UI-039); `tools/es-menu-map-check` passes.

Artifact observations: docs/es-menu-map.md:130-147 includes opening scan, failed outcome, folder dialogs and content scan. Fresh evidence/host-checks-01/results.json records es-menu-map check rc0 against exact ES checkout.


### I350-L27 — inputs/issues/350.md:27

Requirement: The interface edit passes `tools/es-syntax-check` before the pin moves, and `docs/cloud-sync-changelog.md` carries the change the day it lands.

Artifact observations: docs/qa-logs/2026-10-03-m7-p1/es-syntax.log records GuiMenu.cpp OK/PASS for the remediation before candidate package qualification. docs/cloud-sync-changelog.md:2933-2990 records the October1 scan-first behavior and unchanged semantics; exact ESf6f0 source is compiled into current14 image.


### I350-L35 — inputs/issues/350.md:35

Requirement: The opening scan checks folder state, settings archives by label and content location before options; CONTINUE with content selected runs the second content scan in the selected classes (D-CLOUD-167); the options page on guest d lists only rows the scan found (a frame per seeded case: settings for this label, settings for a foreign label only, content under `/ROCKNIX/Content`, content nowhere).

Artifact observations: cloud_scan:153-255 reads folder→archives→content-location before done; --content executes only selected classes. GuiMenu.cpp:5294-5314 schedules the second scan; guest11 H/A/C/D logs and original frames cover own-label enabled, foreign-only disabled, content found and absent; D progresses through second scan to NES-only picker.


### I350-L36 — inputs/issues/350.md:36

Requirement: Its live line says what it is checking in the words approved for it (D-CLOUD-164: `CHECKING WHAT SETTINGS AND CONTENT YOUR CLOUD HAS FOR THIS DEVICE...`); the string and its French land in the same commit (D-UI-051).

Artifact observations: GuiCloudTransfer.cpp:1008-1010 uses the approved full sentence plus whole-clause640px fallback; exact French strings in locale/lang/fr/LC_MESSAGES/emulationstation2.po:6515+. git log -S identifies both source and French introduction in dc819f432483acad722a14234d7bbe6b999a705c at2026-10-01 14:38:17UTC. Actual H/G frames show the complete shorter line at640px.


### I352-L34 — inputs/issues/352.md:34

Requirement: A CHOOSE CLOUD FOLDER page (the `GuiFileBrowser` pattern fed by `rclone lsf`, `es-native-ui.md` § Reusable precedents) sets `CONTENT_REMOTE` through `cloud_setup`, and the transfer page re-reads it; the walk's frames show the chosen folder and the journal shows the `Content path` line.

Artifact observations: GuiMenu.cpp:5210-5314 routes a selected folder through cloud_setup --set-content-remote, checks status, then rereads for the scan. cloud_setup:569-605 validates/persists the pointer and logs Content path. Guest11 D frame shows the chooser and later automatic fallback is proven.


### I352-L35 — inputs/issues/352.md:35

Requirement: With `CONTENT_REMOTE` back at `/ROCKNIX/Content` and the QA cloud seeded with `Photos/` and `Documents/` at its root, CONTENT TO RESTORE on guest d lists only ROM systems and BIOS: the walk's 640x480 frame and the scan's output lines. (The Nova's own listing is re-read on its next staging, as a read, and noted here in a comment.)

Artifact observations: cloud_content_restore:1308-1323 filters pre-tier root rows by local or supported systems. Directly viewed guest11 D/03-D-systems.png: NES is shown; Photos/Documents appear only in04-D-chooser.png as cloud folders, not systems. Host scripts fresh1719 suite includes A0 Photos/Documents negative controls and genuine gb positive control.


### I352-L36 — inputs/issues/352.md:36

Requirement: `docs/es-menu-map.md` carries the chooser (D-UI-039); `tools/es-menu-map-check` and `tools/vocabulary-check` pass; the cloud-sync page on the site says where the content folder is chosen (`documentation-accuracy.md`).

Artifact observations: docs/es-menu-map.md:140-146 includes chooser; fresh host es-menu-map check rc0 and ES-checks02 vocabulary164strings/0wrong. The public cloud-sync site delivery remains the separate P5 docs gate.


### I352-L45 — inputs/issues/352.md:45

Requirement: Only then, with nothing found under either, the chooser opens; a frame shows it with the QA cloud's root folders listed as folders to pick from, never as systems.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 D log and directly reviewed03-D-question.png/04-D-chooser.png show absent configured/fallback content leads to the chooser; Documents/Photos are presented as folder paths. GuiMenu.cpp:5228-5282 makes that route explicit.


### I352-L32 — inputs/issues/352.md:32

Requirement: `cloud_content_restore --scan` lists a pre-tier folder only when this device has a folder of that name under `/storage/roms` or the name is a supported system (`legacy_dirs` / `supported_systems`), the same rule `resolve_src` applies; a `tools/cloud-round-trip` case seeds `Photos/` and `Documents/` at the root and the scan's output carries neither line.

Artifact observations: cloud_content_restore:1308-1323 filters pre-tier rows by local directory or supported system. Fresh host1719-suite A0 case includes real gb and unrelated Photos/Documents; guest11 D seeded both unrelated folders and retained a NES-only picker.


### I352-L33 — inputs/issues/352.md:33

Requirement: When the content root holds no `ROMs/` and no known system folder, the page says so instead of listing: `YOUR CLOUD HAS NO ROMS OR BIOS AT <folder>.` / `CHOOSE THE FOLDER WHERE YOUR GAMES ARE?` (approved D-CLOUD-164), with a row that opens the folder chooser; a 640x480 frame shows it.

Artifact observations: cloud_setup --content-location production source and seven actual candidate14 case outputs are included below (content-probe01 and repeatedrefutation03). Cloud/pointer before/after hashes are in the raw result records.


### I352-L44 — inputs/issues/352.md:44

Requirement: When the configured content root holds no `ROMs/` and no known system folder, the scan looks under the cloud root's `/ROCKNIX/Content` (the saves root's parent, `cloud_setup:629-631`) and, finding `ROMs/` or `BIOS/` there, uses that folder automatically and writes `CONTENT_REMOTE` (D-CLOUD-167, no USE IT confirmation); on guest d with `CONTENT_REMOTE=""` and content seeded under `/ROCKNIX/Content`, the frame sequence advances to the options and the journal shows the `Content path` line.

Artifact observations: Same production setup path and raw seven-case outputs below; ES consumer is included with source line numbers.


### I356-L76 — inputs/issues/356.md:76

Requirement: A second guest on the same cloud takes the new marker at its next check with no dialog (its journal line), and the version-aware candidate offered a newer or malformed marker refuses unsupported writes/marker overwrite, showing a supported outcome (frame plus byte/pointer assertions). The separate RC2→candidate and mixed-installation receipts name the actual old binary and prove preservation; they do not claim RC2 implements this future protocol.

Artifact observations: cloud_migrate_layout read_marker and cloud_scan read_folder/why_for_rc source included. UI26 future-script output and refusal text are in the retained excerpt. Before/after target hashes establish write refusal.


### I363-L73 — inputs/issues/363.md:73

Requirement: No sync runs networked layout join/state/follow/migration preparation before transfer. The local `cloud_migrate_layout --superseded` string-list call and per-run legacy saves-folder existence probe required by D-CLOUD-172 remain permitted. `tools/last-good-scripts-test` reports both no-folder-check PASS lines; missing/unknown-root controls preserve D-CLOUD-172. This corrects the obsolete literal no-call wording against D-CLOUD-170/172/173, rather than removing the required absent-folder guard.

Artifact observations: cloud_backup:826-840 performs only local --superseded lookup; :1670-1698 retains the one legacy-parent existence probe and unknown fallback. cloud_restore has no networked migration preparation. Fresh scripts.log:1461-1462 records both no-folder-check PASS lines; T18 missing/unknown controls pass.


### I363-L74 — inputs/issues/363.md:74

Requirement: An exit sync on an existing earlier `/ROCKNIX` folder and the current folder meets the unchanged five-alternating-sample median difference limit of30ms. Current candidate runtime07:272/244ms medians,28ms difference, real transferred bytes and zero migration preparation. #429 preserves the original36ms failed attempt and justifies the new fixture-bound qualification.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/timing/installed-samples.json contains two separate warmups and10 alternating measured transfers, all rc0 with local/remote hashes equal; comparison.json reports269/245ms medians,24ms absolute difference,30ms limit and0migration journal delta. timing-proof.py measures exact installed cloud_backup SHA12a231698b70a8b83eb9d1fd1bc593f4507313030635a6750392f5fd19130a03.


### I363-L75 — inputs/issues/363.md:75

Requirement: `cloud_migrate_layout --needs-step` answers with no network: 0 for an earlier default, not kept, with a remote set up; 1 for the current folder, a folder of the player's own, a kept one, or no remote; 2 for a conf it cannot read; rclone never starts (`tools/last-good-scripts-test` section aa, its `--needs-step` lines).

Artifact observations: cloud_migrate_layout:1520-1560 implements --needs-step before network/locking. Fresh scripts.log:1453-1460 checks earlier defaults0, current/custom/kept/no-remote1, unreadable2, exact case matching and no rclone execution. Fresh evidence/host-checks-01/activity/scripts.log and cloud-layout-results.json:1719/316 PASS, expected injected rc1.


### I363-L76 — inputs/issues/363.md:76

Requirement: `cloud_scan --folder` is the folder item alone -- the join, the state, the quiet follow -- with no archive or root listing, the opening scan's files left as they were, and a refused join ending with its why and no state (section ab, its `--folder` lines).

Artifact observations: cloud_scan --folder source and actual UI26 transcript below; opening scan/state scope and output semantics are separately inspectable.


### I363-L77 — inputs/issues/363.md:77

Requirement: The transfer pages' scan still checks on every open (`tools/last-good-scripts-test` section ab).

Artifact observations: GuiMenu.cpp:5440-5475 constructs a fresh scan on every cloud transfer open. cloud_scan removes prior done/state/facts and reruns prepare/folder/archives/content before publishing done. Fresh host sectionab passes; guest11 A/H/G/F/C demonstrate repeated independent opens including failed/no-stamp path.


### I379-L22 — inputs/issues/379.md:22

Requirement: A synthetic cloud with no save files and one same-device settings archive in each old layout keeps that archive discoverable after follow, settle, setup and transfer-page scan; VM log records pointer values, selected filename and restored sentinel hash.

Artifact observations: Actual archives-runtime/archive-proof.py:82-95 independently resets ROCKNIX/GAMES settings-only clouds, runs follow/settle, calls full scan and restores the writer sentinel; assertions.json records those four cycles. Focused boundary36 adds current-name follow/settle/custom payload preservation. Fresh T20 actor wizard/transfer/boot rows pass.


### I379-L23 — inputs/issues/379.md:23

Requirement: Controls with save files, no archives, a kept layout and an explicit custom Backups folder preserve the documented behavior; each case has a reset and negative control on the old commit.

Artifact observations: cloud_migrate_layout:118 backup_pointer_for keeps custom/populated tiers; independently reset T20 actor and follow/settle/default/custom/apply-other-source cases all pass in fresh316results. Baseline October2 T20 failures and fixed results retain before/after negative controls; focused boundaries six settings-only controls run on a genuine installed guest.


### I379-L24 — inputs/issues/379.md:24

Requirement: The state/actor table includes saves-empty / Backups-nonempty independently of OS-name compatibility #376; main and pair migration suites remain green.

Artifact observations: docs/rasteratops/cloud-folder-state-table.md T20 and executable actor map explicitly separate settings presence from saves and suffix compatibility. Main replacement14 three local backends each106PASS; focused36-case paired migration has distinct devices and per-case byte/pointer assertions. Fresh evidence/host-checks-01/activity/scripts.log and cloud-layout-results.json:1719/316 PASS, expected injected rc1.


### I430-L28 — inputs/issues/430.md:28

Requirement: A fresh fixture waits outside measurement until the actual guest clock exceeds this layout's previous remote upload timestamp plus the comparison window; it asserts and retains the actual newly written mtime and preceding remote mtime before measuring the unchanged production command.

Artifact observations: runtime12/timing-proof.py:25-55 waits on actual guest time until previous remote mtime+2s, writes real fresh bytes, retains actual mtime, and requires >previous+1s before measured command. docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/timing/installed-samples.json records every boundary.


### I430-L29 — inputs/issues/430.md:29

Requirement: Every sample retains timing, return code, local/remote hashes and timestamp facts before a possible assertion; failed output is captured privately/sanitized before teardown.

Artifact observations: timing-proof.py appends before-command row before timing, after-command row containing rc/hash/mtime before transfer assertions, and sanitized failed output before throwing. All10 measured rows plus warmups retained in installed-samples.json.


### I430-L30 — inputs/issues/430.md:30

Requirement: A deliberately invalid timestamp boundary is rejected by the fixture predicate; fixed predeclared diagnostic batches transfer every changed save without forcing future mtimes, changing clocks or bypassing production comparison.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/timing/timestamp-controls.json records same-time/within-window/exact-boundary refusals and later acceptance. Read timestamp_valid and asserts; all10 installed measured transfers have real matching bytes with no utime/clock modification.


### I363-L78 — inputs/issues/363.md:78

Requirement: At the end of cloud setup, for a fresh install whose cloud holds its saves under an earlier folder, the step reads the move before the seeding (`tools/cloud-pair-migration` step 2's lines), and the frames show CHECKING YOUR CLOUD, the MOVE question, then CLOUD SETUP COMPLETE after the answer (`tools/vm-visual-qa` frames at 640x480).

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/optins-11/artifacts/pair-console.log step2 on actual RC269e6039f8f/newcf511ce79b shows folder scan superseded/move, NOT NOW then seeding at the joined ROCKNIX tier, no pixelelated duplicate and byte-identical restore. guest11 L7checks retain setup ordering; directly viewed L setup-complete640px frame preserves ROCKNIX paths. GuiMenu.cpp:5495-5525 sets setup rescan/abandon to finish before seeding.


### I363-L79 — inputs/issues/363.md:79

Requirement: At boot, for a guest whose conf names an earlier folder it has not kept, with a remote set up, the step comes up after the startup sync's card: CHECKING YOUR CLOUD, then the question; NOT NOW brings it back at the next boot; after MOVE the next boot raises nothing and the journal reads `nothing to settle` (frames at 640x480 and the journal, guest d).

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 I/logs/run.log verifies first boot offer, NOT NOW keeps pointer, second boot repeats, MOVE transfers and repoints, third boot --needs-step1. E frame shows startup card alone then creation dialog without card. GuiMenu.cpp:5585-5609 waits for hasAsyncNotifications as well as worker and GUI/game state.


### I363-L80 — inputs/issues/363.md:80

Requirement: Offline at boot (the guest's link cut on the QEMU monitor), the step asks `FINISH CLOUD SETUP` / `YOU'RE NOT ONLINE. CONNECT TO FINISH SETTING UP YOUR CLOUD FOLDER.` with CONNECT TO WI-FI and NOT NOW (a frame at 640x480).

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 J/logs/run.log4checks and directly reviewed01-J-offline.png at640x480 show FINISH CLOUD SETUP, exact offline explanation, CONNECT TO WI-FI/NOT NOW. GuiMenu.cpp:5550-5568 uses default-route test and offers Wi-Fi callback.


### I363-L81 — inputs/issues/363.md:81

Requirement: With a settings restore's marker and an earlier folder both set at boot (written on guest d, a named stand-in for a restore followed by an update), FINISH RESTORE PROCESS comes first with nothing over it; its FINISH brings the step once the screen is free; its LATER brings neither until the next boot (frames at 640x480).

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 K7checks retain restore marker, LATER suppresses cloud step, FINISH consumes marker and brings it. Directly reviewed01-K-restore-page.png and03-K-after-finish.png show restore first and move later, with no overlay.


### I363-L82 — inputs/issues/363.md:82

Requirement: `tools/cloud-pair-migration` covers both later cases: the other guest's step follows after the move (step 5), and a guest that missed its step and backed up into the earlier folder has those saves merged by MOVE with nothing left behind (step 5n; 5m checks absent-root refusal/follow) -- its PASS lines.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/optins-11/artifacts/pair-console.log step5 follows with journal/quiet state, step5m stages old pointers and proves absent-root backup refusal then follow, step5n stages older cloud bytes and proves protected merge with all final bytes/no old files; final42PASS/0FAIL.


### I353-L31 — inputs/issues/353.md:31

Requirement: A carried upstream `/GAMES` (a value no player typed) counts as no folder (D-CLOUD-161). At the end of cloud setup the seeding points it at `/pixelelated` and makes the three folders without asking (D-CLOUD-169: `tools/last-good-scripts-test`'s `--settle` lines); at boot the cloud folder step offers CREATE IT / CHOOSE A FOLDER / NOT NOW (D-CLOUD-170: guest d's epic proof, case E's frame), and so does a transfer page's scan, where CREATE IT writes the three `/pixelelated` paths (case B: the conf's three lines and `tools/cloud-test-backend ls`); with a `/GAMES` that holds files the dialog is the move naming `/GAMES` (case B0's frame).

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 B7checks and E6checks show populatedGAMES prompts move; absentGAMES CREATE IT settles saves/backups; boot offers CREATE/CHOOSE/NOT NOW after78no-folder. Fresh scripts1719 includes settle and current/legacy creation controls.


### I353-L33 — inputs/issues/353.md:33

Requirement: The folder is settled by the cloud folder step, at the end of cloud setup and at boot (D-CLOUD-170, #363), never by a sync: with the folder absent the startup and exit syncs end in the card's `SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET` pointing at MANAGE CLOUD STORAGE (the startup stamp's `78 no-folder`, D-CLOUD-166), and 640x480 frames show the step at the end of setup (guest d's epic proof, case L) and at boot (cases E and I).

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 E/L/I logs and directly viewed E card/offer plus L setup-complete demonstrate setup/boot settlement and78no-folder refusal. cloud_backup:1670-1698 suppresses absent earlier defaults; fresh sectionad four controls pass.


### I353-L34 — inputs/issues/353.md:34

Requirement: The offer carries a third choice to pick a different folder (the folder chooser of #352), and its text has no icon or glyph drawn between its two sentences: a 640x480 frame from guest d and, when it is next staged, one from the device.

Artifact observations: Directly viewed E/01-E-step-offer.png640x480: CREATE IT, CHOOSE A FOLDER, NOT NOW; no icon/glyph between explanatory sentences. GuiMenu.cpp:5410-5440 routes CHOOSE A FOLDER through the existing sync path editor.


### I353-L35 — inputs/issues/353.md:35

Requirement: The words the offer uses are approved by the maintainer before the build (`player-language.md`): proposed `YOUR CLOUD HAS NO /ROCKNIX/Saves FOLDER YET.` / `CREATE IT`, `CHOOSE A FOLDER`, `NOT NOW`; their French lands in the same commit (D-UI-051).

Artifact observations: D-CLOUD-164 records owner approval of all13cloud-epic strings. ESdc819f432483acad722a14234d7bbe6b999a705c introduces source and French together; fr.po includes creation/move/chooser lines. Current E/K images show the revised dynamic pixelelated destination.


### I353-L36 — inputs/issues/353.md:36

Requirement: The default folder's name (`/ROCKNIX` today, D-WORKFLOW-101; `/pixelelated` proposed) is a register row on the maintainer's word, with D-WORKFLOW-101's mixed-installation test run before any default changes.

Artifact observations: D-CLOUD-158 explicitly reverses D-WORKFLOW-101 and keeps mixed-installation gate; D-WORKFLOW-144 changes destination to lowercasepixelelated. docs/qa-logs/2026-10-05-pixelelated-replacement-09/optins-11/artifacts/pair-console.log names real old69e6039f8f and currentcf511ce79b, updates the old guest in place and verifies byte-preserving convergence;42PASS.


### I364-L33 — inputs/issues/364.md:33

Requirement: A backup on a carried `/GAMES` the cloud does not hold makes no `/GAMES`, sends nothing, prints `>>> offer create-saves-folder|/GAMES` and ends 0, on a deliberate run and on the exit sync's `--automatic --recent` run. A `/GAMES` the cloud holds is backed up as before, and an absent current folder is still made (`tools/last-good-scripts-test` section ad, its four PASS lines; against the previous commit the first two FAIL).

Artifact observations: cloud_backup:1670-1698 returns the create-saves-folder offer without mkdir/copy when a successful parent probe proves absence. Fresh scripts.log:1492-1495 passes deliberate and recent-automatic absentGAMES, existingGAMES and absent-current controls.


### I364-L34 — inputs/issues/364.md:34

Requirement: At a boot on a stock-shaped conf with nothing in the cloud, the startup card reads SKIPPED with `78 no-folder`, the QA cloud holds no `/GAMES` afterwards, and the cloud folder step offers CREATE IT (guest d's epic proof, case E: its PASS lines and `tools/cloud-test-backend ls`).

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 E log records1791186987 78 no-folder, noGAMES payload, unchanged configuredGAMES afterNOT NOW and creation offer; direct640px startup/offer frames match.


### I364-L35 — inputs/issues/364.md:35

Requirement: The cost the listing adds to an exit sync on an earlier folder (59 ms on run 101's follow benchmark, against 16 ms on run 100) is kept with its reason or removed, decided against #365's folder table (D-WORKFLOW-134).

Artifact observations: cloud_backup:810-823 uses one trailing-slash parent-directory listing, with unknown fallback at1670-1698; D-CLOUD-173 retains absence safety. runtime12 actual-byte timing gives269/245ms medians,24ms≤30,0migration prep; original historical costs remain recorded.


### I353-L32 — inputs/issues/353.md:32

Requirement: An earlier `/ROCKNIX` folder gets one dialog, MOVE first (D-CLOUD-160): MOVE copies, verifies and deletes (the move page's frames on guest d; `tools/cloud-test-backend ls` shows `/pixelelated` whole and no `/ROCKNIX`; a kill during the copy leaves `/ROCKNIX` intact and a second MOVE completes it); another device on `/ROCKNIX` is re-pointed at its next cloud folder step or transfer-page scan with no dialog (`tools/cloud-pair-migration` step 5's journal line, D-CLOUD-170), one that wrote there first is merged by its MOVE (step 5m, D-CLOUD-168); KEEP USING leaves a device on `/ROCKNIX` for good; NOT NOW asks again at the next boot and the next transfer page.

Artifact observations: docs/qa-logs/2026-10-05-pixelelated-replacement-09/optins-11/artifacts/pair-console.log establishes move/follow/staged late-write merge; guest11 I proves NOT NOW/retry/settled boot; fresh A57 host check kills process group before the third copy and recovers. Focused boundaries adds four copy/deletion fault classes on real guests.


### I353-L52 — inputs/issues/353.md:52

Requirement: The move carries `Saves-replaced` (the set-aside of conflict losers beside the saves folder) to `/pixelelated/Saves-replaced` by the same copy, verify, delete, and nothing of ours remains under the old name afterwards: a `tools/last-good-scripts-test` case seeds a set-aside copy under the old layout and reads it back under the new one with the old folder gone; the round trip on the VM shows the sync's next set-aside landing under `/pixelelated`.

Artifact observations: guest11 A verifies all four folders including Saves-replaced moved, old source removed. Focused boundaries preserves distinct discarded-save SHA through faults/retries; fresh host tests retain shelf cases.


### I365-L101 — inputs/issues/365.md:101

Requirement: `docs/` carries the cloud folder's state table: each combination of conf state and cloud state, with what each actor does and the code line that does it. A walk of the table against the scripts lists no cell where two actors disagree, or names each disagreement as a decision.

Artifact observations: docs/rasteratops/cloud-folder-state-table.md:18–121 records dimensions, eight concrete call paths for seven actors, T01–T25 decisions and named disagreement dispositions; :173 onward adds T26 and executable current-source coverage. R/cloud_migrate_layout shared transition, cloud_setup settlement guard, cloud_backup/restore probes and E/main.cpp startup gate were read against this map.


### I365-L103 — inputs/issues/365.md:103

Requirement: The guest-d proof runs from `tools/` with a per-case state reset. Its exit code is non-zero when any check fails, seen once on a constructed failure.

Artifact observations: tools/rasteratops-vm-cloud-epic:4–40 runs each selected case in a separate process and returns accumulated failure; fresh evidence/guest-negative-02/result.json records actual expected rc1, console 0 PASS/1 FAIL at15:43:45UTC. Q09/guest-11 retains installed per-case resets and runtime assertions.


### I365-L104 — inputs/issues/365.md:104

Requirement: The retro file over runs 95 to 101 names each pattern with its guard, in `tools/`, `.githooks/` or `.claude/rules/`, as `ceremonies.md` asks of a blindspot.

Artifact observations: docs/retros/2026-10-02-cloud-runs-95-101.md names five patterns and links implemented guards: actor-state runner, source-derived stale-path checks, separate-process/reset/negative controls, actual UI/byte assertions, and issue-tracking reconciliation. Current tools/rasteratops-cloud-layout-test, rasteratops-vm-cloud-epic and last-good-scripts-test implement those guards.


### I365-L117 — inputs/issues/365.md:117

Requirement: T17 fault-and-recovery VM case proves no misleading old-root seeding after failed settlement while the wizard can finish and the boot step can retry; retained log shows initial/final pointers, README locations and sentinel hashes.

Artifact observations: Q09/cloud-ui-08/artifacts/cloud-ui/UI17/logs/run.log has19PASS/0FAIL; UI17-before-cloud.json equals the failed cloud snapshot, with Setup.srm SHA d7c0956d2b153e4c48ac6e75125255c465555cbc0a65793c3e4e459b108afa5d. Recovery retains that byte stream under pixelelated/Saves and markerSHA be68d69fa1fe3ddbcaa9295b8e3e732fd0113d909e38cf643d95aab41c9b1a22; recovery-step/journal logs show next-boot MOVE and completion.


### I365-L118 — inputs/issues/365.md:118

Requirement: The new independent settings/content/archive dimensions and residual cases are represented in the table and promoted guest proof with reset, failing negative control and byte/pointer assertions; source-only hypotheses remain explicitly distinguished from executed failures.

Artifact observations: State table T20–T26 plus tools/pixelelated-vm-cloud-boundaries and BND/proof.py map independent backup/content pointers, root/omitted/custom transitions, configured-first residual, collision, restricted parent and distinct-follower recovery. Retained BND36 installed assertions include reset and exact bytes/pointers; Q09 predecessor65/UI17/guest cases separately exercise startup and archive behavior. Fresh guest negative rc1 is retained.


### I390-L18 — inputs/issues/390.md:18

Requirement: The fixture returns absence for a missing marker, returns stored marker bytes, and retains rcat bytes; targeted setup cases exercise both path and bucket modes.

Artifact observations: tools/last-good-scripts-test:4620–4685 C2 fixture now makes cat return3 for absence or stored marker bytes and rcat persist stdin. C2 path/bucket setup cases and the fresh1719-script suite pass; the focused316-layout suite also passes.


### I390-L19 — inputs/issues/390.md:19

Requirement: The complete host script suite has no regressions from the fixture correction; output and source revision retained.

Artifact observations: docs/qa-logs/2026-10-03-m7-p1/host-suite-after.log ends PASSED (focused93/0 then full suite result). Fresh evidence/host-checks-01/activity/scripts.log has1719PASS/0FAIL; results.json records command rc0 with frozen14 system and exact E.


### I390-L20 — inputs/issues/390.md:20

Requirement: The marker failure is recorded as fixture evidence, distinct from the reproduced production failures on #356.

Artifact observations: docs/qa-logs/2026-10-03-m7-p1/host-suite-before-fixture-fix.log marker failures occur in the C2 test shim; production malformed/future-marker and retry-before artifacts are separate. Source correction is in last-good-scripts-test cat/rcat fixture, while R/cloud_migrate_layout owns the product marker validation.


### I365-L102 — inputs/issues/365.md:102

Requirement: An actor × state coverage map names an executable assertion for every applicable T01–T26 cell (and a reason for each inapplicable one); `tools/last-good-scripts-test` runs those cases and passes. The previous commit fails the cases for the cells this work changed.

Artifact observations: docs/rasteratops/cloud-folder-state-table.md:173–end and actor-case-map.json name208 actor cells across26 states. Fresh evidence/actor-map-pass-coverage.json mechanically matches all210 unique executable case names to PASS lines in our current host suite (0 missing). Earlier baseline.log has36PASS/22FAIL, including T17/18/20/21/24 changed behavior; boundary/predecessor old/fixed controls cover later extensions.


### I377-L22 — inputs/issues/377.md:22

Requirement: Production-path cases distinguish present, absent and failed parent listings; the failed listing cannot produce a create-folder offer. The old commit fails the regression case and the fixed commit's PASS lines are retained.

Artifact observations: R/cloud_backup:810–840/1670 and cloud_restore:1688–1760 distinguish present/absent/unknown; failed discovery suppresses creation. Oct2 baseline.log contains both T18-bucket-backup-unknown and restore FAIL; fresh316 focused run passes the exact whole-script cases and parent error3/4/5/7 controls. Installed S3 attempt03 demonstrates actual parent403 with child200.


### I377-L23 — inputs/issues/377.md:23

Requirement: The corresponding backup/restore bucket predicates are audited together; each failed-read fixture either passes a regression test or has a documented source-based reason it cannot reach the bad branch.

Artifact observations: Both production helper/caller pairs and tools/rasteratops-cloud-layout-test:335–347 were read together. Synthetic bucket sets the literal /ROCKNIX/Saves so the superseded backup guard is reachable. Actual bucket-prefixed S3 restore has no corresponding literal gate; its HTTP proxy-events.json records403 at Rasteratops/ after200 at child.


### I377-L24 — inputs/issues/377.md:24

Requirement: A whole-script synthetic bucket case with a reachable superseded literal tests the backup guard; an S3 QA fault case tests the ungated restore sibling. Each injects the failed parent listing, preserves sentinel hashes, reports the truthful outcome and succeeds after the fault is removed. The normal bucket-prefixed S3 backup fixture does not reach superseded_saves_setting and cannot count as that branch’s test.

Artifact observations: Current provider_failure fixture reaches the literal backup guard, asserts fault-fired/no create offer/unchanged cloud sentinel; baseline fails and fresh host run passes. Actual S3 attempt03 assertions/proxy-events/refused-output/sentinels prove nonzero restore, truthful refusal, local/cloud preservation, removal of403 fault and exact retry restore.


### I377-L25 — inputs/issues/377.md:25

Requirement: Existing absent-legacy-root refusal, current/custom-root creation and corrected pair-migration cases remain green. No extra recurring network probe is introduced without #364's timing acceptance being reverified.

Artifact observations: Fresh316/1719 suites cover absent legacy refusal/current/custom creation; Q09/optins-11 actual42PASS mixed predecessor pair preserves/follows/merges, and runtime12 five-sample installed comparison is269vs245ms (24ms, limit30) with identical2000-byte payload and no migration journal.


### I366-L34 — inputs/issues/366.md:34

Requirement: The stale-name check reads the list from `cloud_migrate_layout --superseded` and matches each entry as a whole path component; run against today's `tools/cloud-test-backend` (the bare `/GAMES` at line 806) it FAILs, and that failing run is recorded in the day's work log with its command (`engineering-practices.md` § Guards must fail closed).

Artifact observations: last-good-scripts-test:9005–9060 derives whole-component patterns from production --superseded. 2026-10-04-qa-fixture-guard/guard-extracted.py and old.log identify actual b2378d9 source line806 and reject its backend prefix/default mismatch; result.json binds old-backendSHA90f5df2d and guardSHA c53df68f. Current full suite passes this exact guard.


### I366-L35 — inputs/issues/366.md:35

Requirement: `tools/cloud-test-backend saves-remote` names, on every backend `tools/cloud-test-backend backends` lists, a folder that `cloud_migrate_layout --superseded` does not list: a check in `tools/last-good-scripts-test` that loops over the backends and PASSes.

Artifact observations: Current full1719 suite runs advertised-backend loop. Guard result.json lists webdav/ftp /pixelelated/Saves, S3 /rocknix-qa/pixelelated/Saves, SMB /qashare/pixelelated/Saves and the SFTP QA data prefix. Source derives prefix plus shipped default and rejects each superseded path.


### I366-L36 — inputs/issues/366.md:36

Requirement: `tools/vm-qa`'s round-trip suite reads PASS in `report.md` on the first image built after the fix, and its `round-trip.log` names the new folder on the `SAVES_REMOTE` line.

Artifact observations: 2026-10-03-archive-harness/rerun/report.md exact503e24e10d first post-fix image has round-trip PASS81s; round-trip.log says /Rasteratops/Saves and all9 uploaded and restored byte-identical.


### I366-L37 — inputs/issues/366.md:37

Requirement: The S3 backend still gets a legal bucket name: `tools/cloud-round-trip --backend s3` against a QA guest logs `only 9/9` or no shortfall line for its saves upload.

Artifact observations: 2026-10-03-m7-qa-01/s3/report.md actual503e24e10d PASS107s; round-trip.log selects /rocknix-qa/Rasteratops/Saves and verifies all9 original, all9 replaced, all9 restored bytes. Current full guard validates legal S3 bucket names.


### I401-L33 — inputs/issues/401.md:33

Requirement: Retain both original failures and code/history trace with actual guest evidence.

Artifact observations: 2026-10-03-content-network/s3-before-link.log:51–81 retains actual LINK3/4 success-after-outage failures at70.3/59.0s and wrongly successful stamps; s3-before-guest.log retains actual command output. Shared helper and caller diff show the formerly direct rclone commands now use progress-sensitive bounded_content_rclone.


### I401-L34 — inputs/issues/401.md:34

Requirement: Content network operations stop after bounded inactivity across provider SDK retries; progressing large transfers and cancellation remain functional. Actual-source stalled/progressing/failure controls prove the distinction.

Artifact observations: R/cloud_content_transfer:28–164 parses five monotonic high-water counters, bounds inactivity and preserves progressing operations; SIGINT/TERM/EXIT clean tracked child/tee. test-content-guard.py executes source-extracted old/new copy calls; guard-controls and BusyBox summaries each12PASS/6FAIL before,18PASS/0FAIL after. Current1719 suite reexecutes permanent whole-script6 controls.


### I401-L35 — inputs/issues/401.md:35

Requirement: WebDAV and S3 content backup/restore and affected scan cases pass real link-loss/retry/whole-byte/stamp checks under unchanged bounds on the replacement image.

Artifact observations: Q09/link-10 actual two installed seven-case matrices:75 WebDAV/76 S3 assertions, four result channels0 and actual cleanup07:13:44. S3 LINK3/4 stop35.1/35.2s after cut withrc69; WebDAV30.1/30.0s. Both prove no partial litter, matching whole receiving files, failure stamps and plain-retry exact bytes; scans preserve unrelated stamps and recover24systems+BIOS.


### I401-L36 — inputs/issues/401.md:36

Requirement: Full affected host/package gates and image upgrade/clean qualification pass; source, artifact and remaining priorities are recorded.

Artifact observations: Fresh host-checks01 full1719 and focused316 pass with exact14 tools; frozen14 qa18 clean/default and actual26-check RC2 upgrade receipts bind unchanged helper and both callers. Q09/link-10 completion and frozen source/bundle custody retain exact runtime inputs.


### I429-L28 — inputs/issues/429.md:28

Requirement: Retained original failure, all result channels and actual cleanup receipt; diagnosis names measured operations/conditions and distinguishes product cost from measurement noise.

Artifact observations: 2026-10-04-pixelelated-57cbc-qualification/runtime-06/comparison.json retains286/250ms=36ms>30, same cloud_backupSHA12a23169; completion has actual/four rc1 and all5ownedPIDs absent00:43:50. timing-diagnosis.md and diagnostic02 separate24ms listing cost, actual timestamp evidence and three predeclared batches.


### I429-L29 — inputs/issues/429.md:29

Requirement: Any correction preserves missing/unknown-folder behavior with meaningful negative controls; no original frozen owner or source tree is edited.

Artifact observations: Product cloud_backup retains parent-directory predicate and missing/unknown branch distinction; fresh T14/T18 and all parent-error controls pass. Diagnostic change is only the clock-safe helper; timing-proof.py waits beyond remote timestamp outside measurement without modifying product, clock or mtime.


### I429-L30 — inputs/issues/429.md:30

Requirement: Exact candidate installed qualification meets the unchanged five-sample alternating median30ms limit, with every transfer byte verified and no migration preparation; retain all attempts and justify any repeat from the diagnosis.

Artifact observations: runtime07 completion actual29491/fourrc0; installed-samples/comparison gives272/244ms=28≤30, twelve actual transferred-byte/timestamp records and zero migration journal. Later Q09/runtime12 same script five alternating medians269/245=24ms with all12 byte comparisons.


### I430-L31 — inputs/issues/430.md:31

Requirement: Original failures and limited readonly-inspection evidence are retained, and fresh acceptance ownership remains distinct from diagnostics under #429.

Artifact observations: Original diagnostic01 actual/fourrc1 remains retained; inspection01 failed-save-facts.json shows persisted c8629db9 bytes on both sides and guest mtime1135.277ms older, not the original live4ff90268 write. Diagnostic02 actual/fourrc1, trace01 actual/fourrc0, runtime07 actual/fourrc0 have separate owners and actual cleanup receipts.


### I429-L31 — inputs/issues/429.md:31

Requirement: Installed identity/Tools consumer proof completes, and M7/checkpoint identify the accepted artifact and next dependency-gated owner.

Artifact observations: runtime07 identity-proof.py executes installed13 checks; assertions.json confirms actual upgraded Tools XML/hash, identity, retired reporting/updater, policy bytes. Exact actual/fourrc0 and owner cleanup independently read. Current M7 body and checkpoint retain accepted frozen14 custody and P4→capacity→H700 order.


### I351-L58 — inputs/issues/351.md:58

Requirement: 1: the Close control sits at the bottom of the page, below the note, with at least 2rem of space above it, and a tap asks a confirmation (the safe answer first) before Escape is sent; a 390 px headless-Firefox render shows the placement, and the page's load test (the harness from #330) passes.

Artifact observations: R/cloud_oauth:646–657/1000–1023 places .leave after the note with2rem margin; :1179 confirmation uses Keep before Close and sends Escape only on confirmed click. Fresh full-script log:650–653 executes the node page interaction/load controls. Directly reviewed Q10/signin-ui14 04/05 phone frames; signin-proof.py:308–331 uses actual headless Firefox157 and390px iframe.


### I351-L59 — inputs/issues/351.md:59

Requirement: 2: the state line has at least `.75rem` above and below it in both states (`Checking…`, `Connected.`); the two 390 px renders show it.

Artifact observations: Q10/signin-ui14 phone-metrics.json records actual390px width/root font16px and12px top/bottom margins in Checking… and Connected. Both original frames directly viewed. R/cloud_oauth #state margin is .75rem 0.


### I351-L60 — inputs/issues/351.md:60

Requirement: 3: the image ships `CHASSIS=handset` and the installed sign-in window sends Mobile Safari in both actual HTTP requests and `navigator.userAgent`. Replacement10 signin-ui14/15/16 each retain 40 passing checks and 15 reviewed frames; `signin-ui-14/build.log` lines41–47 and `artifacts/signin/all-local-navigator.json` prove this. Replacement14 readback under #462 confirms handset chassis and identical installed `cloud-signin-window`/`cloud_oauth` hashes (`signin-payload-continuity.json`). This reuses explicitly identified prior runtime evidence on unchanged bytes; it is not a new authenticated Dropbox execution. The provider-owned trust-page observation is #463, outside M7.

Artifact observations: Q10/signin-ui14 build.log and all-local-requests.json show actual HTTP/start/302/mobile-form Mobile Safari user agent; all-local-navigator.json independently records navigator.userAgent. Frozen14 signin-payload-continuity.json verifies CHASSIS handset and exact windowSHAfc9a3473/OAuthSHAc9982e28.


### I351-L61 — inputs/issues/351.md:61

Requirement: 4: the finishing page carries the shared `STYLE` (the card, the `h1`, the note), reads as a success, and says what happens next; a frame from guest d's window shows it.

Artifact observations: cloud-signin-window.c:415–450 FINISHING_PAGE uses shared visual styling, green Connected heading and Finishing up on your handheld… note. Directly viewed installed02-finishing-marker-stand-in.png; finishing-transition.json changes actual pageSHA36043094→890973b0 after done marker while window stays open.


### I351-L62 — inputs/issues/351.md:62

Requirement: Every string added has its French in the same commit where it is an interface string (D-UI-051), and `tools/vocabulary-check` passes on the scripts.

Artifact observations: D-CLOUD-164 text and actual cloud_oauth phone confirmation plus cloud-signin-window FINISHING_PAGE source are included. Exact installed payload equality was verified; no new French-mode runtime run is supplied.


### I362-L68 — inputs/issues/362.md:68

Requirement: Owner disposition recorded in D-WORKFLOW-138: refresh with existing functionality preserved.

Artifact observations: D-WORKFLOW-138 in docs/decision-register.md:592 explicitly withdraws libsoup3.6.6/proxy old-pin exceptions, requires functionality preservation and refresh. Current libsoup recipe3.8.0 and selected WebKit2.54.1 follow that disposition.


### I362-L69 — inputs/issues/362.md:69

Requirement: Recipe uses verified 3.8.0 archive and explicit optional dependency settings; pkgcheck passes.

Artifact observations: packages/web/libsoup/package.mk names3.8.0 SHA bbf08fa3e03a88c31a3d27a0d87cb422e9490f2d08e149211103df6d638a2238; cold consumed inventory retains matching1609676-byte archive. Explicit optional settings include disabledzstd/brotli/ntlm/gssapi/sysprof/introspection. Fresh evidence/local-pkgcheck01 validates actual matched recipe rc0/0FAIL.


### I362-L70 — inputs/issues/362.md:70

Requirement: Cold-build WebKitGTK 2.54.1 against libsoup 3.8.0; tools/fork-package-freshness exits 0 and the cut record names both inputs.

Artifact observations: P3 cold-webkit-libsoup.json binds consumed archive/build stamps and unchanged recipe hashes. Directly read original cold build.log lines310232/310242 and1179166/1179405: targetlibsoup3.8.0 built, targetWebKit found linkedSoup3.8.0. Frozen14 preparation/package-freshness.log and freshness-completion.json actual/fourrc0 at00:42 bind1608 recipes/tools and both CURRENT inputs.


### I362-L71 — inputs/issues/362.md:71

Requirement: VM sign-in frames show the sign-in page in touch layout and finishing page; report the30-second combined RSS against D-WORKFLOW-048's approved loaded-page profile (about284MiB on the ordinary guest), explain any material growth, and prove the page loads in an actual1GiB guest without a kernel OOM or lost responsiveness; HTTP/TLS/redirect behavior works on the resulting image. This replaces the undefined “within its bound”: the existing tool has no numerical ceiling assertion.

Artifact observations: Installed signin-ui14 actualHTTP302/Mobile-UA/JS-UA and inspected phone/finishing frames establish touch/redirect behavior; public HTTPS pages load. Ordinary8GiB public-login30s peak701264KiB is a heavier workload than D-WORKFLOW-048 simple-page≈284MiB. Actual1GiB signin-1g13 example.org271416KiB and signin-provider1g05 publiclogin395676KiB,30s, responsive/no kernelOOM; actualQEMU1024MiB/firmware1048576KiB, Linux810372KiB recorded. Both loaded640x480frames directly viewed.


### I462-L28 — inputs/issues/462.md:28

Requirement: Append a decision refining D-QA-017/D-QA-041 and update active rules, release readiness, tracker priorities, and resume handoff to make hosted accounts optional; source/readback evidence identifies the changed gate.

Artifact observations: D-QA-058 is appended with exact owner direction; vm-first/release-candidates localWebDAV/SFTP/MinIO rules, readiness active heading, saved handoff and tracker-readback.json reconcile hosted-optional gate.


### I462-L29 — inputs/issues/462.md:29

Requirement: Frozen replacement14 has separate WebDAV, SFTP, and MinIO/S3 round-trip PASS reports; report exact cases, failures/skips and scope, with immutable image/source identity.

Artifact observations: 2026-10-06-local-cloud three actual7afa9efcfc reports name bundleb77e47e5/imagec7df6a6f and PASS86/73/110s; each round-trip106PASS/0FAIL/0SKIP. Logs verify9upload/replacement/restorebytes, excludes, refusal/stamps and serialization; completion totals318.


### I462-L30 — inputs/issues/462.md:30

Requirement: Retain fresh-owner harness seals, all four watcher result channels, final process/VM/backend cleanup readback, and sanitized evidence. Submission is not completion.

Artifact observations: Local-cloud harness seals/source manifest70cb0448 and completion05:59:18 retain four rc0, actual6PIDs absent, noQEMU/MinIO/backendpidfiles and ports9010/9011/9012/9013/10022/10023unbound. Raw sanitized protocol logs and SHA256SUMS are retained.


### I462-L31 — inputs/issues/462.md:31

Requirement: Preserve unverified Dropbox trust-page behavior in a milestone-less follow-up; reconcile #351's local browser criteria against existing artifacts without claiming an authenticated Dropbox test.

Artifact observations: Installed phone/window payload continuity and EN target frame receipts retained; assess required languages against source and approved contract.


### I462-L32 — inputs/issues/462.md:32

Requirement: Publish the explicit RA reset target and retain account-backed proof status separately; M7 continues P3 → approved P4 review → H700 arm then aarch64.

Artifact observations: Saved checkpoint and RA-award completion identify Tobu15738/Potato-tanSecret100359 softcore:33PASS, initialunearned→queue1→pending0→provider-earned, relaunch28→27, actual/fourrc0 and06:10cleanup/accountclear. Milestone evidence/p4-milestone-after.json orders P4 before capacity461/H700arm→aarch64.


### I361-L119 — inputs/issues/361.md:119

Requirement: Owner disposition recorded in D-WORKFLOW-138: refresh current upstream, preserve functionality; prior pin proposal withdrawn.

Artifact observations: D-WORKFLOW-138 owner direction explicitly withdraws the old proxy/libsoup exception; P/package.mk pins879b158 and parent-coupled libchdr607694c/rcheevos1433173. Current scope preserves whole-library offline behavior and prepares upstream fixes.


### I361-L121 — inputs/issues/361.md:121

Requirement: Indexed and unindexed whole-library scans retain truthful readiness, no total-library cap, interruption/retry, polite request pacing, and safe handling of server 429s; a synthetic library over 100 games proves the boundary.

Artifact observations: P/raofflineproxy-cache-indexed:87–112 uses background pacing and persists pauses; unindexed call explicitly opts out of100-game budget and rejects queued readiness. tools/raofflineproxy-integration-test tests125indexed/unindexed,124+retry, persistedpause,429stop/restart and upstream100default. Original whole-library-before reports125OKbut100actual; after125actual. b09host11 tests pass with consumed-source equality to879.


### I361-L124 — inputs/issues/361.md:124

Requirement: tools/fork-package-freshness exits0 on frozen replacement14; freshness05/allfour0 and exact recipe/tool verification retained. Earlier failed13 and completed12 results remain their own evidence.

Artifact observations: Frozen14 preparation/package-freshness.log starts/ends exact1608recipe/tool verification and CURRENT879b158/libchdr607694c/libsoup3.8.0/WebKit2.54.1; freshness-completion.json actual/allfour0 at00:42 and fourabsentPIDs. Frozen13 freshness04 failed on newer879 remains separate.


### I408-L18 — inputs/issues/408.md:18

Requirement: Exact branded image reproduces missing automatic account discovery while an explicit-path control succeeds; no credential values enter evidence.

Artifact observations: 2026-10-03-proxy-identity/packaged-identity.json identifies installed config.pyc/OS_NAME RASTERATOPS, automatic=false but explicit=true; assertions.json exactbuild/syntheticaccount pass and automaticdiscovery fails.


### I408-L19 — inputs/issues/408.md:19

Requirement: A focused upstream-compatible patch recognizes both identities, preserves unrelated-platform behavior and configured overrides, and passes old-code negative controls.

Artifact observations: P/patches/018-pixelelated-platform-identity.patch matches complete OS_NAME records for ROCKNIX/pixelelated; focused tests cover custom override, commented/previous-field/lookalike rejection. Original7control before/after and b09 upstream Linux818 tests retain negative/fixed evidence.


### I408-L20 — inputs/issues/408.md:20

Requirement: The next image's packaged resolver automatically reads the canonical synthetic account, and existing cache/sign-in/base/subset queue state survives reopen.

Artifact observations: Frozen14 proxy14/assertions.json22PASS: actual packaged modules, lowercase detector/canonical syntheticaccount, all predecessor cache/pending rows and base/subset mapping through2reopens, legacy image bytes, actual service HTTP/cache paths, pending awards remain while offline. Native18/0skip separate.


### I384-L14 — inputs/issues/384.md:14

Requirement: The original mapping fails and the patched mapping passes, with the upstream award-parity tests passing against the patched source.

Artifact observations: 2026-10-02-candidate-preflight/subset-old-source.txt actual1→100,2→100 contradicts expectedsubset200; subset-backport-tests.log23passed. Current U/rom_cache.py:362–458 iterates each achievement set’s GameId and lookupwantedIDs. Current b09 Linux818 includes award parity; consumed runtime/test trees equality independently recomputed.


### I384-L15 — inputs/issues/384.md:15

Requirement: The candidate guest preserves each subset game ID and retains the queued award in the offline/proxy regression suite.

Artifact observations: Frozen14 subset11/assertions.json35PASS, actualHTTP provider-requests.json fetches game100 andgame200; first flush acceptsbase1/refusessubset2with503 retainingpending1, second sends onlysubset2 and pending0. Empty repeat has no requests; subsetunlock andflushstamp assertions pass.


### I384-L16 — inputs/issues/384.md:16

Requirement: The candidate records the refreshed exact upstream pin, retired duplicate patch disposition and corresponding source containing the preservation fix.

Artifact observations: P/package.mk879b158 SHA98495732; full-series disposition retires017; exact U/rom_cache.py has set-aware mapping. Frozen14 preparation inventory and installedsubset/proxy custodysource7afa9efcfc bind selected implementation.


### I451-L28 — inputs/issues/451.md:28

Requirement: The original current-predecessor AttributeError and actual nonzero outcomes are retained.

Artifact observations: 2026-10-05-proxy-3036478/host01-failed/predecessor-diagnostic-stderr.log retains AttributeError get_all_cache_by_prefix; completion actual/allfour1 and all4PIDs absent22:08:07.


### I451-L29 — inputs/issues/451.md:29

Requirement: Fresh execution passes all11 fork integration checks with both current7252fc and historical865e21 predecessor sources, preserving exact cache rows, queued base/subset awards, sign-in and legacy images across two reopens.

Artifact observations: host02/run.sh separately executes actual7252fc and historical865predecessor integrations; bothlogs11testsOK, fourrc0/cleanup22:10:32. tools/raofflineproxy-integration-test:132–170 dispatches old list versusnewiterator API and compares fullrows/signin/images/base-subset through2reopens. Fresh evidence/proxy-local-integration01 separately passes11each against selected879 with303and865predecessors.


### I451-L30 — inputs/issues/451.md:30

Requirement: The815 upstream Linux checks pass with the newly compiled libchdr607694c library and no native skips; exact source/helper hashes and actual terminal/cleanup receipts are retained.

Artifact observations: host02/patched.log actual815Linux tests/12.751s/OK, no skip line; run.sh compiles coupledlibchdr607694c native helper before setting explicit RAOFFLINEPROXY_RCHASH_LIB; input/native-library hashes and completion bind actual source/build/result. Frozen14 native-result18/0skip plus4legacyCHD/canary/malformed controls exercise installedlibSHA6c484a29.


### I457-L16 — inputs/issues/457.md:16

Requirement: A regression fails on unchanged upstream at uptime0/5 and passes with the correction, including immediate consent changes and declined/unanswered controls; source/output hashes retained.

Artifact observations: Original early-consent-before.json uptime0/5grantedcounter0versusexpected1,31scontrol1. early-before.log has3assertionfailures/8methods; fixed8pass. Patch019 sentinelNone forcesinitial/invalidated read while retaining30s post-observation cache. Fresh evidence/proxy-local-integration01/consent.log executes exact selected879ConsentTests8/0fail.


### I457-L17 — inputs/issues/457.md:17

Requirement: All selected upstream Linux tests and relevant fork integration tests pass with the narrow patch; package lint and schema guard pass.

Artifact observations: b09host818/no skip plus11each303/865 integration passed; independent evidence/proxy-source-equality.json compares219nonbackup/nonbytecode Linux files and53native files to frozen879 with0added/removed/changed. Fresh879integration11each andConsentTests8pass. Fresh12actualrecipe lints and hostchecks01schema pass.


### I457-L18 — inputs/issues/457.md:18

Requirement: A fresh candidate contains the correction and the installed positive/negative/restart HTTP proof passes; loaded module hashes and actual completion/cleanup receipts retained.

Artifact observations: Frozen14 consent02summary30cases across15consentvalues/restarts, actualloopbackcollector, actualfirstgrantcounter7→8at16.705s; loaded8moduleSHA preserved. Invalid/nonbool/unanswered/declined/oldgrant produce0requests; positive usage1/logs2/both3 thenreplay0. Completion actual/four0and5PIDs absent01:01:30.


### I457-L19 — inputs/issues/457.md:19

Requirement: A focused upstream patch plus reproduction/test instructions is prepared under #168; no upstream submission is implied by preparation.

Artifact observations: docs/upstream/raofflineproxy/early-consent/{README.md,fix.patch} namesbaseb09, exactapply/testinstructions and8test before/fixedresults. Fresh bytecomparison showsdraft==packaged019. Contributionmaprow019ownedby168 and explicitunsubmittedstatus.


### I361-L122 — inputs/issues/361.md:122

Requirement: Existing cached sign-in, cache rows, ROM/image paths, pending base/subset awards and restart/reconnection survive an upgrade fixture; declined/unanswered telemetry never sends.

Artifact observations: Frozen14 proxy14actual22preservation andsubset11actual35HTTPassertions preservecachedsign-in,fullrows,ROMpaths,legacyimagebytes andpendingbase/subsetthrough2reopens/reconnection/refusedretry. Consent02actual30cases andloadedmodulehashes enforce unanswered/declinednoHTTP.


### I414-L20 — inputs/issues/414.md:20

Requirement: Correct the compatibility note after verifying the exact pinned storage schema and caller assumptions; retain the equality and current-Storage test evidence.

Artifact observations: 2026-10-04-proxy-schema-note/source-proof.json retains identical old/new storage SHA15e17157 and cache_keys19c79b3c, noncomment-script equality and the original1688PASS/1schemaFAIL. Every direct SQL query was checked: ctl 581,613,680–683,768,1010/1021,1478/1493 consumes existing api_cache/pending_awards columns; current Storage DDL105–167 and cache-key builders preserve them. Streaming whole_games fallback uses current iter_cache_by_prefix. Source/schema equality is retained in docs/qa-logs/2026-10-05-proxy-schema-3036478/schema-review.json. Fresh host-checks01 full script suite1719/0 includes actual-current-Storage writer/ctl reader test; frozen14 installed suite supplies target execution.


### I414-L21 — inputs/issues/414.md:21

Requirement: An early package/preflight check fails for stale, missing or malformed recorded pins, passes the corrected package, and does not bypass the existing runtime/schema assertion.

Artifact observations: tools/rc-preflight132–165 validates exactly one full recipe/header pin before /etc/profile. Fresh evidence/proxy-schema-controls-01:15PASS/0FAIL rc0; missing/short/duplicate/stale/below-header controls reject, absent files return2, matching succeeds, ordinary dispatcher stale returns1.


### I414-L22 — inputs/issues/414.md:22

Requirement: A replacement artifact includes the corrected script and passes the affected script suite; preserve the original failed candidate and its evidence.

Artifact observations: Original b137d8c373 scripts1688/1 retained with SHA802533b8 in source-proof.json; replacement14 frozen installed script suite1719/0 and custody-verified ctl contains879-reviewed note. Historical corrected recipe changes no executable lines.


### I452-L28 — inputs/issues/452.md:28

Requirement: Retain the actual old-note rc1 and source/schema byte comparison; review every direct SQL query against the selected schema.

Artifact observations: docs/qa-logs/2026-10-05-proxy-schema-3036478/before.log and frozen11-negative.log retain old725 note/current303 rc1; schema-review.json records actual725/303 storage62a545a1 and cachekeys19c79b3c equality. Every direct SQL query was checked: ctl 581,613,680–683,768,1010/1021,1478/1493 consumes existing api_cache/pending_awards columns; current Storage DDL105–167 and cache-key builders preserve them. Streaming whole_games fallback uses current iter_cache_by_prefix. Source/schema equality is retained in docs/qa-logs/2026-10-05-proxy-schema-3036478/schema-review.json. Fresh host-checks01 full script suite1719/0 includes actual-current-Storage writer/ctl reader test; frozen14 installed suite supplies target execution.


### I452-L29 — inputs/issues/452.md:29

Requirement: Only the reviewed pin comment changes; package lint and existing offline schema preflight pass, while the original frozen input still fails.

Artifact observations: git show fc689bdfc2709a2855424460fb70681622b959ce changes only two comment lines725→303 and review citation426→452. docs/qa-logs/2026-10-05-proxy-schema-3036478/after.log and frozen11-negative.log retain positive/negative guard; fresh local-pkgcheck-01 raofflineproxy matched actual recipe rc0, fresh15-control guard passes.


### I452-L30 — inputs/issues/452.md:30

Requirement: The corrected source is published and a new sealed candidate input set passes the guard before any build or cache adoption.

Artifact observations: replacement12/preparation/pre-freeze-schema.log names primary next55d8ee8f75 and PASS303 review before build; freeze-receipt.json seals6549product/180symlinks/202QA with SHA bfdcf9b2655157b7e4d3a59f1c6fa803f68989b2cfb8b460eb0f2a666ee98192. Historical12 build/adoption receipts retain source55d8, custody and terminal all-zero channels; source publication is ancestor of frozen14.


### I386-L26 — inputs/issues/386.md:26

Requirement: Each listed package has a verified current source and consumer-compatibility result; the recipes are refreshed, or an actual parent-coupled/version constraint is documented with evidence and a recorded disposition. No unexplained old-pin exception.

Artifact observations: 2026-10-03-dependencies archives.json binds five exact archives; glslang-known-good.json selects ef96ed7/4965431 and both current recipes repeat that parent coupling. Actual compat-build.log links native SPIRV/glslang/shaderc and compiles752-byte Vulkan vertex shader; cbindgen-build.log builds/reports0.29.4 on project Rust1.94.1. translator-header-compat.json shows candidate13ahead/0behind declared translator revision; tllist real tags resolve1.1.0. Frozen14 package-freshness lists glslang16.6/current,cbindgen0.29.4/current,tllist1.1/current and explicit coupledheaders exception.


### I386-L27 — inputs/issues/386.md:27

Requirement: tllist's upstream version is resolved; any freshness resolver fix has a retained failing/passing control. UNKNOWN is not CURRENT.

Artifact observations: tools/fork-package-freshness58–64/147 adds Codeberg tags resolver. Retained codeberg-before.log fails stable/new-stable controls, after passesall6. Fresh evidence/dependency-controls-01 rc0: six controls pass incl prerelease exclusion,newstableBEHIND,empty/malformed/requesterror UNKNOWN even withvalidbody. tllist-live.log actual1.1.0CURRENT and frozen14 freshness repeatsit.


### I386-L28 — inputs/issues/386.md:28

Requirement: tools/pkgcheck passes for changed recipes; relevant consumers build and their VM acceptance receipts identify the exact candidate inputs.

Artifact observations: Fresh local-pkgcheck01 matched glslang,spirv-tools,spirv-headers,shaderc,cbindgen,tllist rc0. Original cold bundle22533e35 build.log99343/170387/704632/801533 explicitly builds hostglslang,targettllist,SPIRV-Tools,targetglslang. Frozen14 inventory10 source-inventory.json binds exact archives and actual target/host stamps plus Mesa/Vulkan/WebKit consumers; accepted642-taskimage/default15suite/virgl-Pixman installed qualification binds source7afa9 and manifest70cb0448.


### I386-L29 — inputs/issues/386.md:29

Requirement: tools/fork-package-freshness exits 0 on the frozen candidate inputs and the source manifest names the verified archives/hashes. #361/#362 qualification remains separately required.

Artifact observations: Q14/preparation/freshness-completion.json real00:42:18 UTC records allfour0 and fourPIDabsence for frozen14run004114; package-freshness.log has explained PINNED and no BEHIND/UNKNOWN. Q14 inventory10 errors0/568roots records exact checked archives and stamps; input manifest70cb0448 binds1608recipes.


### I361-L120 — inputs/issues/361.md:120

Requirement: Every patch has a source-backed retained/rebased/superseded disposition and the final series applies cleanly.

Artifact observations: docs/rasteratops/raofflineproxy-refresh.md enumerates001–019 with16 retained and006/014/017retired. Currentstorage64–70/815–855 protects permanent prefixes in bothSQLite/JSON; image_cache246–315 reuses thread/host connections withdrop/retry/redirectfallback; subsetmapping source independently verifiedI384. Selected879 patch-application.log retains all16 zero-fuzzapplications, fresh proxy-source-equality219Linux/53native zerochanged confirms qualifiedb09consumedbytes.


### I361-L125 — inputs/issues/361.md:125

Requirement: Remaining general-purpose fixes are reconciled with #168 for focused upstream contributions and regression tests. Ten tested drafts and interface-dependent dispositions are published in the linked contribution map; submission/acceptance remain separate.

Artifact observations: docs/upstream/raofflineproxy/contribution-map.md reconciles all16 retained patches,3retired and older168ideas; ten standalone drafts have explicit unsubmittedstatus. 2026-10-06-upstream-drafts raw before/fixed logs independently show7drafts:40targeted/169related executions,zero skips; originals fail real400/404/429 response,wrongaccount,warningfilter,refreshstops,consent,PNG/DNS assertions. Earlier image-publication/identity recheckreceipt and before/fixedlogs bindb09;019consent8-test evidence reviewedseparately.


### I332-L22 — inputs/issues/332.md:22

Requirement: A run of the Nova's `ledcontrol` on the host with `LED_PATH` pointed at a fixture: `brightness max|mid|min` writes three distinct `brightness` values to all eight LEDs (today it writes nothing); `battery`, `rgb` and `off` each leave the fixture in a stated state; the transcript filed here.

Artifact observations: Fresh evidence/ui-lifecycle-controls-01/nova-led.stdout: actualscripts14PASS0FAIL, each8brightnessmax255/mid128/min32;RGBwhite,explicitcustom,off,7batterycolors and10blinksteps. Original2026-10-03-led/before.log6PASS8batteryFAIL retained; correctedafter14PASS.


### I332-L23 — inputs/issues/332.md:23

Requirement: Choosing the value already selected in LED COLOR or LED BRIGHTNESS applies it (the row's callback runs on a press, not only on a change), shown by the fixture's files changing on a walk of the page on a guest with the quirk's script and a fake `LED_PATH`, or by a frame of the row plus the device's sysfs read after the press.

Artifact observations: ActualOct3isolatedVM ui-reselection brightness-before0×8→after128×8, allwhiteRGBunchanged, actualcalls rgb then brightnessmid, savedsettingsstillrgb/mid. Viewed01-mid-already-selected and02-mid-reselected frames; result.json9observedchecks and ui-source-match.json bind exact menu/popup code. E GuiMenu2140–2181 callback reapplies selectedvalue.


### I424-L18 — inputs/issues/424.md:18

Requirement: Retain exact installed negative evidence and identify the source/environment boundary.

Artifact observations: 2026-10-04-es-identity-export/installed-negative.txt hasos-releasepixelelated butprocessPID2470noOS_NAME andoldexportSHA6fbbd886. Directlyviewedactualmain-menuROCKNIX andwrongupdateNOUPDATEAVAILABLE. ProfileomitsOS_NAME; ApiSystem applicationnamefallbackROCKNIX explainsboth.


### I424-L19 — inputs/issues/424.md:19

Requirement: Add a focused regression that fails against the old launch/profile and proves OS_NAME reaches the actual child without unrelated identity/config changes.

Artifact observations: tools/rasteratops-identity-check116–130 sourcesactualexportprofile undercleanenvironment thenexecs/bin/shchild; freshui-lifecycle-controls01 oldexportunset/0.0.1/community, newexportpixelelated/0.0.1/community. Allotherprofilevaluesidentical. Historicalwholeidentitybefore1failure/after0retained.


### I424-L20 — inputs/issues/424.md:20

Requirement: A replacement candidate's clean and retained-storage ES process receives pixelelated; actual menu and manual-update frames show the intended behavior.

Artifact observations: Q14qa18 installedpayload-initial-clean PID1639 andpayload-upgrade PID1484 actual/usr/bin/emulationstation environmentOS_NAMEpixelelated withexportSHA3708af2b andbuild7afa9. Directlyviewedboth01mainmenus displaypixelelated0.0.1 andboth05manualdialogs pointtopixelelated/distribution/releases.


### I424-L21 — inputs/issues/424.md:21

Requirement: Reconcile the sweep/identity checks so a correct os-release file alone cannot close this consumer criterion; retain the superseded artifact's results honestly.

Artifact observations: Currentidentity-checkchildassertionfailsoldprofile andpassesnew; Q14check-payload reads/proc/<ES>/environ andinstalledprofilehash. Before/afterlogs,negativeoldframes andnewconsumerframesremain distinctartifacts.


### I436-L50 — inputs/issues/436.md:50

Requirement: Retained actual old-image reproduction binds the exception, process restart, missing capability and affected save callback.

Artifact observations: Replacement07 identity-diagnostic03: before/information PID1405 restart0; back-two journal line99 throws vector::_M_range_check from empty selection; delayed/reopen PID2925 restart1. GPU controls old.log reproduces absent selection exception. GuiMenu2321–2350 formerly saved getSelected even when capability list empty.


### I436-L51 — inputs/issues/436.md:51

Requirement: The corrected UI safely handles absent GPU governor capability while preserving selection/save behavior when capability exists; old failing and new passing controls are retained.

Artifact observations: Current GuiMenu GPU save callback checks hasSelection before any config write/command. Fresh source-extracted C++ control in ui-lifecycle-controls01 passes six cases: absent, retained absent, unselected, unchanged, changed, fallback. Original old.log fails absent case.


### I436-L52 — inputs/issues/436.md:52

Requirement: Fresh and retained-state upgraded candidate guests return from System Settings without an ES process restart or exception, with actual menu frames and journal proof.

Artifact observations: Copied exact QA18 owner lifecycle files into evidence/ui-lifecycle-controls01/installed-{initial-clean,upgrade,upgrade-software}. Actual PID/start ticks stay1639/509,1484/354,1489/353 across System Settings walks; each result passes and retained journals contain no range exception/termination. Exact14 identity frames reviewed separately. Original08 clean/upgrade lifecycle passes are also retained.


### I436-L53 — inputs/issues/436.md:53

Requirement: Relevant syntax/package checks, candidate qualification, milestone order and checkpoint reflect the repair; #422 retains its separate navigation scope.

Artifact observations: Replacement07 gpu-governor-controls syntax.log explicitly checks GuiMenu.cpp PASS with corresponding rc0; source pin is inherited by current frozen ESf6f0c134. Current package lint, actual14 build/defaults/upgrade and independent lifecycle checks pass. Retained tracker-readback and published checkpoint preserve P4 before device work, with #422 separately named.


### I454-L12 — inputs/issues/454.md:12

Requirement: Shared stop verifies the QEMU/owned-disk identity, waits for the same process to exit, fails boundedly on timeout, and retains the pidfile on failure. Deterministic tests retain delayed exit, wrong-process refusal and timeout controls.

Artifact observations: tools/vm-stop13–58 validates QEMU executable and exact -drive argument, captures start ticks, opens pidfd, rechecks identity, signals same handle and polls boundedly; timeout retains pidfile. Q12 harness-controls/stop-final/controls.log has seven actual-host controls including self-removed pidfile and immediate port reuse.


### I454-L13 — inputs/issues/454.md:13

Requirement: Actual upgraded QA15 disk is preserved and continued in a fresh owner; virgl and automatic software/Pixman checks and identity frames pass, with immediate stop/restart and actual terminal cleanup evidence.

Artifact observations: Q12 QA17 upgraded-disk-custody.json names actual QA15 diskSHA3c2d5dc1, independent inode, guest-byte equality and standalone16GiB converted copy. Renderer software/virgl and ten installed identity frames retained; completion23:40:46 records four0 and all observed process absence, supplement closes5909/10022/9010 and backend.


### I454-L14 — inputs/issues/454.md:14

Requirement: QA15's original failure,15default/26upgrade results, source/input identities and follow-up scope are retained; downstream unstarted owners bind the completed evidence chain explicitly.

Artifact observations: Q12 QA15 completion allfour1 with15 reported defaults/26 actual RC2 assertions retained; QA16 allfour1 self-removed-pidfile failure also retained. QA17 seals exact12 source/input and scoped continuation, and current14 full QA18 reruns the corrected shared harness. Historical downstream proxy13/subset10 retain their plan/candidate bindings.


### I455-L12 — inputs/issues/455.md:12

Requirement: Root cause and first available historical evidence are recorded from actual fixture/system state; inherited coverage is not represented as a new branding regression.

Artifact observations: #455 source snapshot and Q12 QA17 fixture/readback record match-dialog removes GB ROMs, causing requested GB to fall back to FBNeo in QA15/QA14 and earlier accepted baseline. vm-qa ensure_manager_fixture now precedes each manager; scoped walk log records reseeding. Actual selected-system receipt and frame establish corrected outcome.


### I455-L13 — inputs/issues/455.md:13

Requirement: Harness fails for a wrong/missing requested system before accepting the walkthrough, with a retained negative control.

Artifact observations: tools/vm-qa449–462 records real ES system-selected event, queries visible systems and invokes vm-manager-system-check before walk acceptance. Fresh manager-controls.json has six expected results: valid passes; wrong,missing,duplicate,hidden,empty refuse. Q12 original five controls and three CLI refusals retained.


### I455-L14 — inputs/issues/455.md:14

Requirement: Game Boy, NES and FBNeo each reach the intended manager on the exact candidate; actual frames and relevant aspect/orientation evidence retained without silently accepting a new baseline.

Artifact observations: Exact14 QA18 defaults/walks manager-{gb,nes,fbn}-system-check logs pass actual gb/nes/fbn. Directly viewed all three04-manager frames: GB/Ninoid landscape160×144 ratio; NES/Bobl and FBNeo/Ms.Pac-Man portrait with round rings and top green orientation mark; consistent start arrow. QA17 comparison-reviewed retains19screens/14claims/0unclaimed/0missing with unchanged baseline/masks.


### I310-L21 — inputs/issues/310.md:21

Requirement: The mapping is named: a diff of the interface's `/proc/<pid>/maps` across one launch/exit cycle on the VM shows the 10 MiB region and the code that makes it (the region's flags and backing in the issue).

Artifact observations: Oct3 software-3/003.maps→004.maps adds10MiB total anonymous rwxp; adjacent mappings merge so the newly printed20MiB region replaces an existing10MiB mapping. Fresh evidence/memory-recalculation.json retains both totals. jit-trace.log mmap length10485760/protection7/flags34 and matching jit-symbols.txt resolve rtasm_exec_malloc→SSE vertex translation; unload-trace records driver unloading.


### I310-L22 — inputs/issues/310.md:22

Requirement: With the fix, `E1-pl069-control.sh`'s 10 cycles on the VM leave VmSize within one cycle's noise (under 1 MB of growth over 10) and VmRSS within 2 MB; equivalent launch/exit CSV and identity receipts filed under `docs/qa-logs/2026-10-03-launch-memory/`.

Artifact observations: Fresh independent CSV recomputation of Q10 memory12: five warmups then10 software cycles, onePID2010, VmSize-448KiB/RSS+684KiB; virgl onePID2137,0/+224KiB. Both within original1024/2048 limits. Installed identities and renderer receipts bind frozen10; unchanged ES/Mesa/SDL bytes carry to14.


### I310-L23 — inputs/issues/310.md:23

Requirement: `E1-pl069.sh`'s 50 cycles with the exit sync on show the same flat VmSize, so PL-069's fix and this one are shown apart (the csv filed).

Artifact observations: Q10 software-sync50 cycles.csv has56rows including initial state, five warmups and50 measured cycles, samePID7226; fresh computation0KiB virtual/+444KiB resident. All55 exit-sync files have distinct timestamps and status0 completed. Original failed intermediate RSS endurance runs remain retained.


### I310-L24 — inputs/issues/310.md:24

Requirement: Already written: nothing -- the growth lives in the running process and a restart clears it.

Artifact observations: Defect consists of anonymous process mappings, lost DSO pointers, udev/SDL allocations and retained freed heap. Source fixes only process lifecycle resources; actual restart/newprocess measurements reset these. No storage/cloud migration is added by Mesa/SDL patches or ES trims.


### I433-L73 — inputs/issues/433.md:73

Requirement: Retain original failed640/passed1280 matcher outputs, selected actual frames, capture hashes, all runner results and verified cleanup without conflating runner success with visual acceptance.

Artifact observations: Original57cbc UI07 splash640 result0.9610208817<0.995 and1280 result0.996047282 retain frames/hashes and allzero command completion. Directly viewed failed640 actual-best: console overlay removes glyph pixels. Separate visual result remains failed despite successful runner and verified cleanup.


### I433-L74 — inputs/issues/433.md:74

Requirement: A bounded diagnostic distinguishes the failure cause using captured framebuffer/console facts and controls; no blind repeat-until-pass or threshold change.

Artifact observations: Boot diagnostic01 actual original0.85159249; exact splash drawn in text mode1.0 then line erasure0.981691626; graphics mode console write stays1.0. Diagnostic03 actual quiet640/1280 both1.0 after asserting Syslinux/GRUB consumption; failed01/02 setup attempts retained. Fresh renderer-controls01 executes16 real init-predicate observations including original policy failure and debug/other-device controls.


### I433-L75 — inputs/issues/433.md:75

Requirement: Any necessary product/harness fix has source-level evidence plus exact-candidate clean/retained-state boot proof at both sizes with unchanged matcher/negative controls. If product inputs change, freeze a new candidate and reconcile required qualification.

Artifact observations: GENERIC_X64 options74–76 adds quiet while retaining serial/tty0. BusyBox init1274–1279 applies same suppression to old no-quiet configs unless debugging. Q10 boot05 allfour clean/actualRC2-upgraded640/1280 result1.0 at0.995 with12 rejected controls; directly viewed allfour exact best frames. Earlier08/09 same boot proof and newer14 unchanged boot inputs retained.


### I433-L76 — inputs/issues/433.md:76

Requirement: Published evidence and the M7/#409/#422/#431 bodies identify the accepted replacement and safe downstream dependency binding before any successor predecessor proof advances.

Artifact observations: Retained #433 source snapshot identifies published cf511ce replacement09, source/manifest and predecessor06 dependence on boot03/UI10; #441 subsequent failed binding retained then boot04 verifies actual QA13 upgraded disk with full build/kernel/backing checks. Boot05 provenance names prior04 and actualQA14 upgraded backing for new10. Current milestone/checkpoint retains ordered P4 before device builds.


### I447-L70 — inputs/issues/447.md:70

Requirement: Original command success, failed local frame, five other reviewed frames, hashes and actual cleanup retained without relabelling.

Artifact observations: Q09 signin-ui08-unaccepted retains command17checks/allzero and original local frameSHAa977f54c; directly viewed partial old loading page/jagged blocks below redirect. Five other original frames and all hashes retained;09:47:31 cleanup identifies absent owner/guest and noQEMU.


### I447-L71 — inputs/issues/447.md:71

Requirement: New sealed capture path requires the existing visual tool's stable-screen result with a bound; unsteady/no-result cases cannot count as accepted captures.

Artifact observations: stable_panel.py requires rc0 plus exact settle:still output after2quiet seconds within30seconds. Actual zero-timeout receipt returns0 but moving-at-bound and passedfalse; source assertion requires rejection. Four stable page receipts retained in accepted14.


### I447-L72 — inputs/issues/447.md:72

Requirement: Fresh full sign-in proof passes actual redirect/UA/phone checks; six intended frames are semantically reviewed with stability receipts and actual result/cleanup agreement. Authenticated Dropbox trust remains separate.

Artifact observations: Q10 signin14/15/16 each40checks/fifteenframes with actual HTTP+navigator Mobile UA, redirect,390CSS-pixel phone metrics and installed hashes. Six intended14frames directly viewed across this review: complete local form, finishing message, public login, Checking/Connected phone and public OAuth login. Each owner four0 with actual process absence20:18/20:20/20:23.


### I447-L73 — inputs/issues/447.md:73

Requirement: M7 and checkpoint identify accepted successor and the remaining1GiB/account/audit gates.

Artifact observations: #447 retained issue records accepted source8708d8e, runtime13 scope and ordered freshfreeze10/clean-upgrade/1GiB/account/audit beforeH700. Current checkpoint identifies accepted frozen14 and later realRA33/localcloud318, with optionalDropbox#463 and independent audit still incomplete.


### I447-L74 — inputs/issues/447.md:74

Requirement: Resolve the reproducible software-host stale/partial scanout on the declared software VM profile: fresh bounded native/host comparison and full sign-in semantic frames agree without forced resize/input, with actual old/partial/unsettled rejection, matching terminal results and cleanup. Canonical virgl success alone does not satisfy this criterion.

Artifact observations: Q10 signin14 actual0/5/15 render observations bind correct finishing documentSHA890973b0, QEMU/VNC identicalSHA68a39b52 and native raw-pixel comparison PASS at each offset. Fresh exact-pixel controls accept correct image and reject real old09 and partial08 frames. Earlier matched Pixman/GLES2 and actualROCKNIX RC2 controls retained.


### I447-L152 — inputs/issues/447.md:152

Requirement: Rebuilt GENERIC_X64 clean/RC2-upgraded guests select Pixman without virgl and retain accelerated virgl; actual GPU features, compositor environment/logs and installed file hashes prove selection.

Artifact observations: Current14 QA18 installed renderer records: clean/upgradevirgl negotiatedbit0=1, WLR_RENDERER unset and GLES2virgl; upgrade softwarebit0=0, WLR_RENDERERpixman. WrapperSHA15b13fa9/dropinSHAca1e6aaf/sharedswaySHA1b42a41b agree. Q10 cleansoftware boot05 and signin14, upgradedsoftware15 provide installed clean/retained selection with actual kernelfeatures/logs.


### I447-L153 — inputs/issues/447.md:153

Requirement: Selector boundary controls preserve explicit/unknown/non-virtio/multi-GPU cases; shared handheld startup bytes remain unchanged.

Artifact observations: GENERIC_X64 wrapper validates exact single card and one virtio child, actual driver and binary>=64bit feature string; explicit renderer/render-device returns unchanged. Selector04 executes22 cases on each image BusyBox actual software/virgl guest; all boundaries pass, including multiple/unknown/nonvirtio/malformed and multidigit card. Shared sway hash1b42a41b unchanged.


### I447-L154 — inputs/issues/447.md:154

Requirement: Relevant ES, emulator launch/exit, visual and time-to-play checks pass on the rebuilt software and accelerated profiles; original failures remain preserved.

Artifact observations: Q10 memory12 both installed profiles pass10-cycle launch/exit and strict growth, plus software50sync. Exit/time-to-play logs retain firstpixels0.570/0.636s, backup1.324/1.673s, relaunch1.012/1.011s; exact boot/sign-in/identity visuals and QA14 defaults/actualRC2 upgrade retained. Later14 QA18 repeats full defaults and installedrenderer checks.


### I327-L20 — inputs/issues/327.md:20

Requirement: A frame of the page at 640x480 from `tools/vm-walks/docs/retro-achievements.steps` on the first-release candidate image shows the explanation as short lines under the rows they explain (or one short block in the description size), each row visibly separated, the approved two paragraphs wrap within the panel without clipping (D-UI-119), and the frame filed under `docs/qa-frames/` beside the before frame.

Artifact observations: GuiRetroAchievementsSettings.cpp:53–68 uses description-font measured wrapping; :95–105 supplies the two paragraphs; :431–435 separates them. Directly inspected docs/qa-frames/2026-10-03/327/{before,en-640x480,fr-640x480}.png: the old all-caps block becomes two separated, readable paragraphs entirely inside the panel. Actual replacement10 ui-14 retains this unchanged surface.


### I327-L21 — inputs/issues/327.md:21

Requirement: `tools/es-menu-map-check` PASS, the French strings for every changed sentence in the same commit (D-UI-051), `tools/vocabulary-check` PASS.

Artifact observations: Fresh audit host-checks01 menu-map and vocabulary commands passed; ES-checks02 vocabulary reports 164 strings / 0 wrong. ES commit c0cb9925eb41c313d011634c79adc6fd45acb099 changes both the page and locale/lang/fr/LC_MESSAGES/emulationstation2.po; direct diff contains all four replacement prose sentences plus scan outcome strings.


### I327-L22 — inputs/issues/327.md:22

Requirement: The site's `retro-achievements/offline-achievements.png` retaken from the walk after the change.

Artifact observations: Local website commit 4f6df54ca16121ff2cd0620407aea6434ee59147 changes docs/_inc/images/retro-achievements/offline-achievements.png. Fresh sha256sum of that file and the directly reviewed en-640x480.png both equal a40331aa212c7e9d4e3901b990bfac0bfe1013803a66346e763c92f72d943976.


### I357-L16 — inputs/issues/357.md:16

Requirement: No device on the candidate posts to `stats.rocknix.org`: the timer is not enabled in the image (`systemctl list-timers` on guest d after a boot shows no `rocknix-report-stats`), and the script, if kept, has no ROCKNIX endpoint (`grep -c rocknix.org` on the shipped script prints 0).

Artifact observations: Source rocknix-report-stats is an unconditional exit 0 with no endpoint. system.d/rocknix-report-stats.timer is masked to /dev/null. Read actual upgraded guest docs/qa-logs/2026-10-03-m7-final-runtime/artifacts/identity/{003,004,005,006}.log and pixelelated-1e6a runtime-05 timers.txt: only evidence/tmpfiles timers, masked statistics unit, endpoint count 0. Replacement09 installed artifact sweep retains the same b03adb70 shim hash and /dev/null target; unchanged source continuity through frozen14 was verified.


### I337-L28 — inputs/issues/337.md:28

Requirement: A GENERIC_X64 image boots under the new name with its own splash and logo, `OS_NAME` read from `/etc/os-release`, the manual-update row visible, and no automatic upstream update request in the captured guest network evidence (frame/readback/capture filed here).

Artifact observations: Actual14 qa-18 installed payload and identity frames prove inherited OS_NAME=pixelelated, its wordmark and MANUAL UPDATES. Actual boot-qualification05 provides unchanged boot renderer proof. ES ApiSystem refuses automatic/forced update checks for pixelelated; rocknix-update is inert, and older installed identity logs show query rc1 without output.


### I337-L27 — inputs/issues/337.md:27

Requirement: The register row that calls the direction (D-WORKFLOW-081's answer) names the fork's name and the licence terms it keeps (GPL-2 and MIT kept whole; the CC BY-SA attribution line; no ROCKNIX images).

Artifact observations: D-WORKFLOW-084 settles the fork direction and GPL-2/MIT preservation; D-WORKFLOW-144 makes pixelelated the current name. LICENSE.md retains upstream attribution and original code terms, distinguishes ROCKNIX branding CC BY-NC-SA 4.0 from new project artwork, and TRADEMARK.md governs project marks. Actual14 uses the new LCD wordmark.


### I359-L29 — inputs/issues/359.md:29

Requirement: A register row records the artwork licence and whether a trademark policy exists; `LICENSE.md`'s branding section names the fork's terms and `TRADEMARK.md` exists or the row says why not (`tools/vocabulary-check` and the licence text in the image's `/usr/share/licenses` agree: a `grep` on the image's SYSTEM).

Artifact observations: D-WORKFLOW-131 sets artwork and trademark policy; D-WORKFLOW-136/144 update bot/project names. LICENSE.md branding section and TRADEMARK.md implement those terms. Fresh local hashes agree with actual14 qa-18 installed payload records: LICENSE 1a277de267611abc4242e6a1e08ac2abac54316e7abcbf8ae7afd0a1dc98ec6c, TRADEMARK d46db25cb845b021cd7f1c13dabcd98d04e77d89a45968527e58abc9e3788761, both mode644. Fresh audit vocabulary passed.


### I409-L266 — inputs/issues/409.md:266

Requirement: Saved specification and editable master explicitly name Tiny5 Duo LCD; recorded font hash matches the existing approved face.

Artifact observations: docs/pixelelated/art/wordmark-system.md and source/pixelelated-live-text.svg explicitly use Tiny5 Duo LCD. source/font.json pins version2.007, upstream f740beb653d6839fac1f8c794668ffcf22037342 and SHA256 b0cada86874b192d304716536e84e735ec9b22719a3b9c2ba390ab0881a3a916. Fresh generator --check with the actual pinned splash font reproduced all ten SVG/CSS products; evidence/wordmark-controls-01/reproduce.log.


### I409-L267 — inputs/issues/409.md:267

Requirement: Six outlined SVGs and two monochrome variants reproduce from the pinned font/palettes; exact RGB555 colors, alpha gaps, orientation and hard boundaries pass artifact checks.

Artifact observations: Fresh wordmark-controls-01 results: ten vector/CSS files exactly reproduced from150 original LCD contours; all24 PNGs use exactly their RGB555-derived colors and only alpha0/255. Standard alpha masks are identical and Scanline strictly removes rows. Direct source read shows five exact rectangles, vertical zones only for Dual, horizontal bands otherwise, and no background/image/font embedding in production SVG.


### I409-L268 — inputs/issues/409.md:268

Requirement: Retained light/dark/midtone/saturated and small-size proofs demonstrate the portable assets; runtime integration remains separately tracked before the image freeze.

Artifact observations: Directly reviewed art/proofs/backgrounds.png: all eight treatments on white, near-black, mid-gray and saturated magenta, including expected low-contrast monochrome examples. small-sizes.png compares Ocean and light monochrome at16/24/32/64px. Boot-qualification05 and actual14 installed f5fa9839 assets separately establish integration.


### I337-L29 — inputs/issues/337.md:29

Requirement: The approved placeholder site under the fork domain carries lineage/attribution and release/adoption links; its build/retrieval receipt is filed here. A full site is later scope (D-WORKFLOW-098).

Artifact observations: D-WORKFLOW-098 explicitly chooses a name-only placeholder, superseding the criterion’s lineage/adoption link requirement. D-WORKFLOW-099 selects GitHub Pages and leaves deployment separately tracked; input issue337 itself calls this the approved placeholder rather than a full-site gate.


### I337-L53 — inputs/issues/337.md:53

Requirement: The release notes and the site's ssh page say the ssh password is unchanged in 0.0.1 (D-WORKFLOW-129, #358): the notes file's line and the docs PR.

Artifact observations: D-WORKFLOW-129 records the unchanged rocknix password and later #358. NAMING.md retains the password contract. Searches of current docs/releases, docs/rasteratops and the local website do not locate the required0.0.1 release note and SSH-page change; current website FAQs instead describes upstream generated passwords.


### I359-L30 — inputs/issues/359.md:30

Requirement: The release notes' lineage and non-endorsement paragraph (#344 P4) points at the same terms.

Artifact observations: LICENSE.md and TRADEMARK.md implement the approved terms and actual14 carries their identical bytes. No0.0.1 release-note lineage/non-endorsement paragraph is present under docs/releases; #344’s release-note criterion remains explicitly P5 in the current milestone.


### I465-L20 — inputs/issues/465.md:20

Requirement: A reusable harness loads settings before ES starts, verifies the unchanged installed ES/proxy/ctl identities, and records a real interface address disconnect/reconnect.

Artifact observations: Read tools/ra-ui-test:139–169 and :126–135: hash installed ES/ctl/all proxy bytecode, stop ES, write settings, clear owned fixture, then restart and verify a different PID; actual NetworkManager disconnect removes the address for two watcher observations. qualified-03 contains all four corresponding assertion sets. Fresh local readback confirms all46 installed hashes invariant across profiles and unchanged ES lifetime within each.


### I465-L21 — inputs/issues/465.md:21

Requirement: English/French sending and sent outcome frames at640x480 and1280x960 show readable correctly bounded cards, matched to pending counts, actual installed-flusher loopback receipts and `last-sync-link` records.

Artifact observations: Directly reviewed all four profiles’ sending and sent frames at640x480 and1280x960. Cards remain within panel bounds; English/French text fits. qualified-03 actual installed flusher.pyc receipts show patch/award/unlocks HTTP200, flushed1/pending0; installed ctl pending assertions and last-sync-link status0 sent agree. Fresh local reconciliation totals109 passing assertions.


### I465-L22 — inputs/issues/465.md:22

Requirement: A controlled refused send retains pending state and produces the bounded failure/retry outcome; empty/repeated link transitions do not invent another successful send.

Artifact observations: EN640 refuse-flush.json records HTTP503, flushed0/pending1; refuse-stamp.txt is status5 not-sent IT STOPPED ANSWERING. Directly viewed refusal sending/outcome/dismissal: bounded failure and retry sentence, then no card. All four empty-repeat frames have no notification and assertions require unchanged last-sync-link.


### I465-L23 — inputs/issues/465.md:23

Requirement: Every frame claim is directly reviewed; original failures are retained. The standard watcher, four terminal result channels and actual owned guest/provider cleanup are verified.

Artifact observations: All23 qualified originals directly viewed during this independent audit, plus the superseded French baseline showing its erroneous startup send. Owner01/02 evidence remains present. Qualified completion.json records all four rc0 and actual five-process absence, no QEMU, unbound10026/5912 at07:01:20; fixture checks every local provider/flusher exited.


### I465-L24 — inputs/issues/465.md:24

Requirement: The ordinary award harness starts ES with its updated settings and captures reconnect as well as exit events, without weakening its unearned/API checks. Changed harness behavior has VM evidence; the completed RA33 account proof remains immutable.

Artifact observations: Direct git diff629603d6 for tools/ra-offline-test adds settings reload before launch, actual address removal, reconnect capture/wait and current sent stamp; existing unearned/account/API checks remain. Fresh bash -n exits0. UI owner03 separately executes the changed settings/address/card mechanics on frozen14. RA33 evidence remains separate and immutable.


### I465-L25 — inputs/issues/465.md:25

Requirement: Publish exact evidence and reconcile #361/M7 coverage. Begin the approved #383 P4 fixes audit only after the remaining software qualification is satisfied.

Artifact observations: Actual qualification07:01:40 precedes audit setup07:04:22. inputs/ui-publication.json records remote feature629603d6 and next63675be4 readback07:04:47; inputs/ui-tracker-completion.json and retained issue bodies reconcile361/383/465 and M7 at07:05:49. Published commit contains the exact qualified receipts and harness change.


### I337-L40 — inputs/issues/337.md:40

Requirement: A fresh guest on the candidate, signed in to the QA cloud, creates and uses `/pixelelated/{Saves,Backups,Content}`: `tools/cloud-test-backend ls` after a backup and a saves sync shows the three folders and nothing under `/ROCKNIX`; `grep -rn ROCKNIX projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf*` prints nothing; `tools/vocabulary-check` passes.

Artifact observations: Both current cloud_sync.conf files define /pixelelated/Saves, /pixelelated/Backups and /pixelelated/Content. Actual mixed pair optins-11 starts a fresh guest on all three and verifies final remote bytes/config convergence; guest-11 creation cases and actual14 cloud318/default round-trip verify installed consumers. Fresh vocabulary passed.


### I337-L41 — inputs/issues/337.md:41

Requirement: Every `/ROCKNIX` cloud path in the interface and the scripts is listed by the sweep (`docs/rasteratops/p0-sweep-hits.txt`, rule `cloud-path`, 56 lines) and each is changed or marked history in the same commit; the sweep re-run on the candidate's tree lists none as current.

Artifact observations: Historical p0-sweep-hits.txt records the56 cloud-path hits; p0-sweep.md explicitly dates its immutable baseline51f78ac5b4. Current NAMING.md and rename-plan.md classify legacy roots as migration/kept-choice/archive inputs, while current defaults use /pixelelated. Actual replacement09 artifact classification reports zero FIX/UNKNOWN contexts, with retained-context allowlist.


### I337-L50 — inputs/issues/337.md:50

Requirement: `DISTRONAME="pixelelated"`: `os-release` reads `OS_NAME="pixelelated"`, the images are `pixelelated-<board>.<arch>-0.0.1.*`, the info page reads `OPERATING SYSTEM: pixelelated` (a 640x480 frame from guest d; `/etc/os-release` from the image's SYSTEM); repositories, packages and hosts stay lowercase `rasteratops`; the cloud folder is `/pixelelated` (D-CLOUD-158).

Artifact observations: distributions/ROCKNIX/options sets DISTRONAME=pixelelated; scripts/image uses it for OS_NAME and artifact names. Actual14 installed payloads and directly reviewed identity frames show pixelelated; the frozen image/update names begin pixelelated and conf defaults use /pixelelated.


### I337-L51 — inputs/issues/337.md:51

Requirement: The migration tar carries the suffix `-from-ROCKNIX` (`IMAGE_SUFFIX`), so its name passes the RC2 init's check (`init:882`): the built name is `pixelelated-H700.aarch64-0.0.1-from-ROCKNIX.tar` and `tools/vm-upgrade-rehearsal` from RC2's image applies it; the suffix is dropped in the build after 0.0.1 (D-WORKFLOW-128).

Artifact observations: IMAGE_SUFFIX=from-ROCKNIX and scripts/image:116–117 append it. Actual14 qa-18 upgrade/rehearsal.log boots retained September29 RC2 69e6039f8f, stages pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.tar, returns7afa9efcfc and passes26 preservation assertions.


### I337-L52 — inputs/issues/337.md:52

Requirement: The splash and the theme's logo carry the word mark alone until the icon arrives (D-WORKFLOW-130): the splash frame at boot and the theme's logo frame on guest d show the name in the chosen face and no pictorial mark.

Artifact observations: Source splash pin8c71126c and ES/theme assets use the canonical f5fa9839 lowercase LCD wordmark with no icon. Actual14 payload hashes match; boot-qualification05 clean/upgraded640/1280 frames directly reviewed in I433 and exact template match1.0 with12 rejected negative controls. Fresh portable asset proofs contain only lettering.


### I354-L67 — inputs/issues/354.md:67

Requirement: The rehearsal (`tools/vm-upgrade-rehearsal`) from RC2's x64 image keeps every piece of state across the update (its PASS), and a stock-shaped conf carried across (`/GAMES`, nothing in the cloud) meets the cloud folder step at the boot after rather than a dialog from the startup sync: the startup stamp's `78 no-folder` and the step's CREATE IT offer in 640x480 frames (guest d's epic proof, case E; D-CLOUD-166, D-CLOUD-170).

Artifact observations: Actual14 qa-18 upgrade/rehearsal.log independently shows retained RC2 identity, four save/state hashes, marker, setting, remote, cloud pointers and backup unchanged after the update. guest-11 E installed logs and previously directly reviewed640 offer show startup78 no-folder followed by CREATE IT / CHOOSE A FOLDER / NOT NOW for empty stock-shaped GAMES.


### I354-L68 — inputs/issues/354.md:68

Requirement: `tools/vm-qa` on the candidate passes every suite, `frame-diff` against the accepted baseline explains every changed frame by one of the children, `tools/vocabulary-check` and `tools/es-menu-map-check` pass.

Artifact observations: Actual14 qa-18 default suite results: all15 suites pass,1719 script assertions and16 walks/78 frames; frame-diff has34 claimed regions and no unclaimed/missing changes. Fresh audit host menu-map/vocabulary and ES vocabulary checks pass.


### I354-L69 — inputs/issues/354.md:69

Requirement: Every string the five children add is approved by the maintainer before the build and lands with its French (D-UI-051); `docs/cloud-sync-changelog.md` carries the changes the day they land (`change-log.md`); the site's cloud-sync page names `/pixelelated` (`documentation-accuracy.md`, with #42).

Artifact observations: D-CLOUD-164 approves thirteen strings with French; current ES catalog and standalone phone/window sources are in the packet. Public website work is ordered P5.


### I354-L66 — inputs/issues/354.md:66

Requirement: The mixed-installation test (`tools/cloud-pair-migration` on `tools/vm-pair`): guest a updated in place from RC2's image with a `/ROCKNIX` cloud, guest b a fresh install on the same QA cloud; for the default-derived fixture both confs end at `/pixelelated/{Saves,Backups,Content}`; separate populated/custom backup and explicit-root content fixtures retain their independent pointers and byte access, a save written on each arrives on the other, nothing was removed from `/ROCKNIX` before its verified copy, a guest that missed its step and wrote into the earlier folder is merged by MOVE (D-CLOUD-168), and the log names each step: its PASS lines, and its negative control on a build without the join (D-CLOUD-169) failing.

Artifact observations: Directly read actual optins-11 pair-console.log: retained69e6039f8f upgraded in place, freshcf511 guest,42 passing assertions, save bytes in both directions, per-tier copy/verify before removal, marker follow and staged late-write MOVE merge. Separate guest-11 B explicit-root fixture and prior independently audited custom backup controls preserve independent pointers.


### I361-L123 — inputs/issues/361.md:123

Requirement: Upstream Linux suites and fork proxy regression sections pass on the exact selected source; cold image build, tools/ra-offline-test and UI/progress/flush proof pass on the VM.

Artifact observations: The upstream Linux818-test execution uses b09 source whose219 Linux and53 native files compare byte-for-byte with selected879, excluding generated .orig files; equality evidence retained. Fresh selected879 focused proxy controls and actual14 proxy22/native18/legacyCHD4/subset35 all pass. Cold build provenance, later frozen14 build642/642, RA33 real unearned/offline/provider/relaunch and UI465109 assertions/23 frames establish the composed VM gate.


### I383-L284 — inputs/issues/383.md:284

Requirement: #365's T01–T26 table maps each relevant actor/state cell to executable assertions or a justified inapplicable cell; #356 adds strict supported-version, numbered-step, marker-failure and interrupted retry/fleet controls; #320 has deterministic recovery-race controls; writer-shaped archive discovery is the first negative control. The promoted guest proof resets every case and exits nonzero on an injected assertion failure.

Artifact observations: Independent actor-map-pass-coverage.json connects208 actor/state cells to210 exact assertion names; fresh full1719/focused316 host tests pass with expected injected rc1. Actual guest-11 and focused cloud-boundaries01 cover strict markers, numbered steps, nine copy/delete/marker fault/follower cases. Fresh deterministic ES320 tests119 assertions and old failures verify lock recovery. Writer-shaped archive negative is first in retained remediation baseline. Guest-negative02 records actual0PASS/1FAIL rc1.


### I383-L285 — inputs/issues/383.md:285

Requirement: #376/#377/#379/#380/#381 and #365 settlement, #363 card ordering, #364 timing, #366 fixture defects have source fixes and retained passing/failing controls. Each owning issue carries its own evidence.

Artifact observations: Independent child entries verify source/installed controls for376/377/379/380/381/365/363/364/366, including fixed timing and archive restoration. This review also confirms #467 content classification and #468 future-marker reason loss; narrow settlement/manual chooser/hostname/S3 retry evidence gaps remain in the ledger.


### I383-L286 — inputs/issues/383.md:286

Requirement: #361/#362/#386 input refresh and preservation checks pass; #310/#327/#332 carry-forward software criteria and host gates are resolved. #337's approved OS identity is integrated on the frozen upstream baseline. One recorded input set produces the candidate; clean install, RC2 upgrade, full VM QA, pair migration, visual and timing evidence identify that build.

Artifact observations: Current input refresh and preserved state/native/proxy tests are verified under361/362/386. Carry-forward310/327/332 software proofs pass. Frozen14 manifest6550/207/180, immutable bundle19 files, actual clean/RC2 upgrade/default QA and unchanged-source pair/boot/visual/endurance evidence are tied to their proper builds.


### I383-L287 — inputs/issues/383.md:287

Requirement: The code-auditor review of the fixes includes the approved independent other-lab model through the Facilitator; findings are resolved and any resulting product changes rebuilt and requalified before an RC claim.

Artifact observations: This milestone-tier code-auditor run selected independent depth: Codex primary plus Fable5.1/xhigh through the verified Facilitator. Phase2 is active; external blind/refutation calls correctly await2.5/3/4/4.5. Frozen product has not been mutated mid-audit.


### I409-L236 — inputs/issues/409.md:236

Requirement: Record the new identity hierarchy and lowercase default in the append-only decision register; reconcile active naming policy, instructions, milestone order and open issue criteria. Retain historical attribution and closed titles.

Artifact observations: D-WORKFLOW-144/145/146 and D-CLOUD-174 record lowercase identity, characters/LCD and new root. NAMING.md, active rules and rename-plan.md agree; M7 keeps its ordered current phases and frozen historical artifacts.


### I409-L237 — inputs/issues/409.md:237

Requirement: Classify old-name references across active source, tools, sibling repos and infrastructure; retain an explicit compatibility/history/owner/character allowlist. Canonical org URLs and relevant Git remotes resolve to pixelelated; the personal account is verified as rasteratops and the bot identity is unchanged. Historical maxengel-owned forks retain their verified locations; rasteratops/rocknix.org returned 404 and no transfer is assumed.

Artifact observations: NAMING v2 and rename-plan classify compatibility/history/owner/character references. Fresh local remotes show distribution and ES origins under pixelelated, while upstream and verified historical maxengel forks remain. Actual published source refs and consumed ghcr.io/pixelelated/build digest support new namespace use. User confirmation and the dated Oct4 work log record owner rasteratops and unchanged Blitterbot; rocknix.org403/404 is explicitly unresolved.


### I409-L238 — inputs/issues/409.md:238

Requirement: Distribution/ES/splash/theme and licence/trademark source use the agreed lowercase identity and Tiny5 Duo LCD wordmark alone. Exact source pins and existing lint/syntax/identity guards pass; obsolete brand references are classified rather than globally replaced.

Artifact observations: Current distro options, ES f6f0c134, splash8c71126c, theme canonical f5fa9839 wordmark and LICENSE/TRADEMARK use lowercase pixelelated. Fresh package checks, ES unit/vocabulary guards, source export controls and exact font reproduction pass; retained native/C++ syntax checks and actual14 installed identity support runtime.


### I409-L239 — inputs/issues/409.md:239

Requirement: New setup defaults to /pixelelated; configured /ROCKNIX and /GAMES selections and archive discovery remain usable. Isolated controls and candidate clean/upgrade receipts demonstrate no silent cloud relocation or archive loss.

Artifact observations: Current defaults use /pixelelated; actual mixed RC2/fresh pair42 checks, guest-11 keep/not-now/explicit-root cases, focused boundaries and actual14 upgrade26 retain source bytes and configured pointers. Fresh316 layout plus1719 full host checks exercise legacy archive readers and interrupted recovery.


### I409-L240 — inputs/issues/409.md:240

Requirement: The update asset naming/procedure satisfies the ROCKNIX RC2 predecessor init check, and the new image accepts future pixelelated updates. Retain actual upgrade evidence for ROCKNIX RC2.

Artifact observations: Actual14 rehearsal boots69e6039f8f and applies the named from-ROCKNIX tar, returns7afa9efcfc with26 preservation assertions. Current init:883 substitutes @DISTRONAME@ from scripts/image, and options supplies pixelelated; future pixelelated filenames satisfy that predicate.


### I409-L241 — inputs/issues/409.md:241

Requirement: Verify the build-container namespace/digest and source fetches. A monitored build with tested delivery produces a newly frozen pixelelated artifact; retain the image identity/manual-update/brand/licence/source/localisation checks and affected default/upgrade/visual/performance evidence. Do not rename or relabel replacement02.

Artifact observations: Consumed-container.json for the cold build records ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39 as configured and consumed. Exact source inventory568 roots and archive hashes bind frozen14’s new bundleb77e47e57a; watched build642/642 and four terminal rc0 are retained. Actual14 identity/licence/manual-update/default/upgrade plus unchanged-source classified/localized/visual/performance evidence are separately identified.


### I409-L242 — inputs/issues/409.md:242

Requirement: Expand the approved P4 primary plus Fable5.1 Facilitator fixes review to this transition; resolve findings and renew affected artifact proofs before calling the image an RC.

Artifact observations: The current383 audit explicitly includes rename/identity, renderer, cloud and proxy changes on frozen14 and records the authorized Fable5.1 Facilitator plan. It has found product issues and is still in the primary stages.


### I344-L196 — inputs/issues/344.md:196

Requirement: `docs/rasteratops/p0-read.md` exists with one decision per row of the base plan's §2, each citing `path:line`, and its first line answers three questions: does `DISTRO=rasteratops` imply a new directory; do image and asset file names derive from `DISTRO`, `DISTRONAME` or something else; what does `rocknix-update` match on. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md`

Artifact observations: p0-read.md starts with the three answers and a decision/evidence row for each base-plan section2 topic. Fresh historical source read confirms config/options sources a DISTRO directory and scripts/image derives display/artifact identity from DISTRONAME.


### I344-L197 — inputs/issues/344.md:197

Requirement: The sweep report from the base plan's §1.15 command lists every hit in exactly one of four classes (display text; machine identity; persisted paths and network names; boot and storage contracts); every class 2 to 4 hit is marked KEEP, and any non-KEEP carries `path:line`, a reason and a reference to a recorded yes. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-sweep.md and p0-sweep-hits.txt`

Artifact observations: Fresh parser verifies2415 rows and2415 unique path/line keys: classes1323/561/393/138. The sole class2–4 non-KEEP is rocknix-update endpoint with path:line, reason and D-WORKFLOW-093.


### I344-L198 — inputs/issues/344.md:198

Requirement: The updater note records the mechanism, the asset pattern, redirect handling, any distro-name check, draft and pre-release handling, the manual route, and the comparison function's result on `0.0.1` against RC2's version string as a table, and names Branch A (unaided over-the-air) or Branch B (manual adoption). -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-updater.md`

Artifact observations: p0-updater.md provides mechanism, filename/board gate, curl redirect behavior, draft handling, manual route and both ordering tables; it selects Branch B with the reason that RC2 asks ROCKNIX’s service.


### I344-L199 — inputs/issues/344.md:199

Requirement: `BUILD_ID`'s derivation is quoted with `path:line`, with its timestamp and host dependence stated. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § BUILD_ID`

Artifact observations: p0-read.md BUILD_ID section quotes image source and actual RC2 metadata: checkout commit or CUSTOM_GIT_HASH, separate BUILD_DATE and branch, no embedded timestamp. Current14 manifest/source confirm the same derivation.


### I344-L200 — inputs/issues/344.md:200

Requirement: `docs/rasteratops/support-matrix.md` exists with the columns target/arch, physical boards, QA guest, clean install, upgrade, boot medium and boot-chain deltas, recovery method, attachment status; the mandatory migration device is marked. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/support-matrix.md`

Artifact observations: support-matrix.md has all requested target/arch, board, guest, clean/upgrade, boot/recovery and attachment columns; RG35XX SP is the mandatory migration device. D-WORKFLOW-114 explicitly defers RK3566 and preserves two panel sizes.


### I344-L201 — inputs/issues/344.md:201

Requirement: `df -B1` of the build volume and `du -sb` per existing root are recorded, with the forecast as line items (old roots, new roots, source archives, VM overlays, retained candidates). -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Disk`

Artifact observations: p0-read.md records Sep30 df volume bytes, seven root du values, shared archives, four QA disks and retained candidates; forecast separates old/new roots, cache growth, overlays and retained images.


### I344-L202 — inputs/issues/344.md:202

Requirement: The per-asset size limit is recorded with its source and date; the ES licence is quoted from the ES tree; the splash repository's owner is recorded; the digest behind the build container's `:latest` is recorded; `DISTRO_SRC` or its equivalent is recorded. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts`

Artifact observations: p0-read.md Platform facts records dated GitHub asset limit/source, quotes ES MIT terms, names upstream splash owner/pin, consumed container digest and DISTRO_SRC/mirror. Current ES recipe says MIT, correcting the earlier discrepancy.


### I344-L203 — inputs/issues/344.md:203

Requirement: D-WORKFLOW-088 (present in the register; absent from the run's packet) is cited, and Choice 2 of #338 is labelled or struck. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts`

Artifact observations: p0-read.md Platform facts explicitly identifies D-WORKFLOW-088’s absence from the old packet and strikes Choice2 via D-WORKFLOW-096, which records the second Lenovo64GB choice.


### I344-L204 — inputs/issues/344.md:204

Requirement: `git log -- distributions/` shows no identity commit and `git tag` shows no `0.0.1`. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts`

Artifact observations: Fresh git log at historical51f78ac5b4 confirms last distributions commit ff8058e311, upstream GRUB selection. P0 document retains the47-tag/no0.0.1 observation; current git tag --list0.0.1 is still empty.


### I344-L212 — inputs/issues/344.md:212

Requirement: The three repositories are transferred and `rocknix-splash` forked; the ES and splash commits are pinned; every recipe URL and `git remote -v` in every worktree shows fork addresses.

Artifact observations: Current distro/ES origins are pixelelated; pinned ES/splash source archives and published refs are retained. Fresh remotes also retain ROCKNIX/upstream and maxengel historical forks deliberately.


### I344-L213 — inputs/issues/344.md:213

Requirement: The bot token's scope inventory (repositories × permissions × expiry) is recorded and an expiry reminder is configured on the mail channel.

Artifact observations: The bot migration preserves Blitterbot and standing fork push identity; current git origins use the blitterbot SSH alias. No sanitized repositories×permissions×expiry inventory plus tested mail-reminder receipt was located in the project audit inputs.


### I344-L214 — inputs/issues/344.md:214

Requirement: A workflow grep finds no `pull_request`, `pull_request_target` or `workflow_run` job with `runs-on: self-hosted`; a trigger dry-run from a throwaway fork schedules no self-hosted job.

Artifact observations: Fresh grep of all workflow files shows every runs-on is GitHub-hosted ubuntu; validate-pull-request and its reusable freeze check are ubuntu-24.04. No self-hosted label exists.


### I344-L215 — inputs/issues/344.md:215

Requirement: Isolation: `sudo -u runner test -r <path>; echo $?` prints `1` for each secret path; a canary read alerts; `sudo -u runner id` shows no `docker`; `sudo -u runner sudo -l` is empty; `sudo -u runner test -r /var/run/docker.sock` fails; the setuid audit is recorded. If any check fails, the runner is shown disabled.

Artifact observations: D-WORKFLOW-119 conditions the trust boundary on self-hosted runner introduction; all current workflow jobs target hosted ubuntu. Infrastructure topology is later under D-WORKFLOW-113.


### I344-L216 — inputs/issues/344.md:216

Requirement: The build container is mirrored under fork control; the build invocation references it by `@sha256:`; `docker inspect` or a build-log line shows that digest consumed.

Artifact observations: Cold consumed-container.json records configured ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39 and identical consumed image digest, running as1000:1000. Frozen14 inputs bind that same digest.


### I344-L217 — inputs/issues/344.md:217

Requirement: A source-tarball archive index lists every fetched tarball with its hash, in fork-owned storage inside the backup scope.

Artifact observations: Actual14 source-inventory10 records568 roots,583 components and525 install stamps with zero inventory errors; exact source archives are hashed and retained in the shared cache and immutable input records.


### I344-L219 — inputs/issues/344.md:219

Requirement: The candidate store path and its `flock` wrapper are in place; the upstream base commit is recorded as frozen.

Artifact observations: tools/rasteratops-candidate-store uses fcntl.flock LOCK_EX, temporary staging, source/destination digest comparison, read-only files and atomic rename to sha256/<manifest>. Fresh initial audit verify accepted all19 current bundle files. Retained preflight controls reuse same input, preserve changed-input bundle and reject corrupted image bytes. D-WORKFLOW-111 records upstream freeze.


### I344-L220 — inputs/issues/344.md:220

Requirement: The freeze is in force with the emergency exception written. -- D-WORKFLOW-111, 2026-10-01: `upstream/next` at `9fd38fa870` (fetched 2026-09-29 11:02 UTC); the exception is a security fix for a matrix target, cherry-picked by a register row.

Artifact observations: D-WORKFLOW-111 states exact9fd38fa87094d4f0e956d03ac6c660fe4fd5e9d6 freeze and the named security-fix exception. Fresh merge-base of frozen14 and upstream/next returns that exact base.


### I344-L228 — inputs/issues/344.md:228

Requirement: A cold `GENERIC_X64` build exits `0` with `DISTRONAME` set and `DISTRO=ROCKNIX` retained (or the split's completed build-and-boot log, if P0 supplied a reason); the build log is archived with the manifest; the concurrency setting is recorded.

Artifact observations: Actual cold-01 sourceb137d8c3, global24 workers, pinned container and manifestc83828fa are retained with642/642 jobs and build/inner/watcher rc0. Full216844873-byte build log lives in immutable bundle22533e35. Later independently copied/requalified14 has its own642/642 four-channel rc0 record.


### I344-L229 — inputs/issues/344.md:229

Requirement: The brand sweep reports zero unclassified hits against `NAMING.md` allowlist vN (N recorded); an injected old-logo frame fails the template match (threshold and bounding box recorded).

Artifact observations: Replacement09 sweep-09 reads57293 files and8603 classified contexts against NAMING v2 with zero FIX/UNKNOWN; ten scanner and60 context mutation controls pass. Current boot05 template matches1.0 and rejects12 old-logo/blank/wrong-size controls.


### I344-L230 — inputs/issues/344.md:230

Requirement: The localisation reconciliation lists every touched `.po` and `.xml` entry, with no orphan.

Artifact observations: Sweep09 localisation.json pins ESf6f0c134 (same as frozen14), reconciles851 catalogue/95 XML entries,57 retired/two removed entries, zero unclassified and zero active orphans. Installed Tools XML parses and matches source; actual14 unchanged ES/theme/Tools hashes corroborate continuity.


### I344-L231 — inputs/issues/344.md:231

Requirement: The secret sweep reports counts only, all zero.

Artifact observations: Sweep09 reports zero unclassified credential-pattern matches;70 matches in20 files are reviewed public constants bound to exact source/hash proofs. Actual frozen14 input custody and public QA sanitation are retained.


### I344-L232 — inputs/issues/344.md:232

Requirement: `tools/vm-qa` reads PASS bound to a candidate-store hash equal to the manifest hash, before and after the run.

Artifact observations: Actual14 qa-18/defaults/report.md identifies bundleb77e47e57a, source7afa9efcfc and all15 passing suites. qa-18/build.log:12–13 and243–244 verifies frozen inputs and candidate-store hashes before and after; initial independent audit reverified all19 bundle files.


### I344-L233 — inputs/issues/344.md:233

Requirement: The upstream base commit is unchanged since P1.

Artifact observations: Fresh git merge-base frozen7afa9efcfc and upstream/next returns exact9fd38fa87094d4f0e956d03ac6c660fe4fd5e9d6, matching D-WORKFLOW-111 and recorded manifest ancestry.


### I344-L234 — inputs/issues/344.md:234

Requirement: The RC2 guest's early signal is recorded (offered or not offered; the comparison result).

Artifact observations: p0-updater.md explicitly derives no fork offering on RC2: it contacts ROCKNIX’s endpoint, has no semantic comparison and only accepts dates for forced selection. Actual retained RC2 upgrade proves the manual adoption route.


### I344-L235 — inputs/issues/344.md:235

Requirement: A draft release exists with only the X64 asset.

Artifact observations: Current M7 milestone explicitly maps #344 contract P2 draft/asset selection into current P5 under #265/#344 after P4 and device gates. Current bytes remain in immutable engineering candidate storage.


### I344-L241 — inputs/issues/344.md:241

Requirement: The device image is built; the manifest's input block (distribution, ES and splash commits, container digest, source index) is diff-empty against P2's; the per-image `BUILD_ID` and hash are in the manifest and the candidate store.

Artifact observations: inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.


### I344-L248 — inputs/issues/344.md:248

Requirement: Branch B: `docs/releases/device-facts.md` carries the migration device's row showing the seven-step procedure completed; the fork-aware updater prints "manual update required"; a network capture shows no request to the upstream host; post-upgrade hashes equal the pre-upgrade ones; the fork-to-fork proof is written as the `0.0.2` gate.

Artifact observations: inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.


### I344-L254 — inputs/issues/344.md:254

Requirement: Every matrix target is built from P2's input set; the requalification check is diff-empty, or the X64 re-run is recorded.

Artifact observations: inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.


### I344-L255 — inputs/issues/344.md:255

Requirement: Each asset's hash equals its manifest entry; each attached asset is under the recorded per-asset limit.

Artifact observations: Current immutable bundle manifests record x64 image2073512198 bytes and tar2074368000 bytes, both below the recorded2147483648-byte limit. Initial audit verifies their hashes against manifestb77e47e57a.


### I344-L256 — inputs/issues/344.md:256

Requirement: The brand, secret, leak and localisation sweeps are re-run on every image with P2's PASS conditions.

Artifact observations: Existing sweep09 provides full brand/credential/localisation controls; current14 has exact payload/identity custody and unchanged locale source. Current P2 audit entries229/231 identify the missing renewed full scan on14 changed artifacts.


### I344-L257 — inputs/issues/344.md:257

Requirement: The per-SoC boot-artifact matrix is filled (upgrade against clean flash; downgrade safety); any target with a boot-chain delta has its device-facts smoke-test row before attachment.

Artifact observations: inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.


### I344-L258 — inputs/issues/344.md:258

Requirement: The component inventory file has a disposition per item; the corresponding-source bundle is retrievable and hash-verified.

Artifact observations: Actual inventory10 contains583 mapped shipped components and568 source roots with zero source-inventory errors. The recorded qualification explicitly retains14 component licence-metadata gaps and says publication corresponding-source bundle is incomplete.


### I344-L259 — inputs/issues/344.md:259

Requirement: The channel-separation demonstration is recorded: a draft, pre-release or CI candidate is not offered on the stable channel.

Artifact observations: Current updater shim returns1 for check and ES blocks automatic/forced update checks for pixelelated. P0 derives Branch B and shows RC2 does not query GitHub Releases; current candidate remains in immutable local storage.


### I344-L260 — inputs/issues/344.md:260

Requirement: Each device asset has its smoke-test evidence recorded before attachment; untested assets remain held (D-WORKFLOW-120, supersedes the earlier Branch B disclosure alternative).

Artifact observations: inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.


### I344-L261 — inputs/issues/344.md:261

Requirement: The release notes carry the support matrix with per-device verification status, adoption instructions, the trust assumption, recovery, source links, lineage and non-endorsement (not "marks retained"), the cloud compatibility exception, and the redirect dependency.

Artifact observations: inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.


### I344-L262 — inputs/issues/344.md:262

Requirement: The publication yes is recorded in the action log; otherwise the state reads "stopped at immutable candidate".

Artifact observations: Current readiness, milestone and all14 qualification records explicitly stop short of RC/device-ready/publication claims and identify immutable bundleb77e47e57a. Current git tag0.0.1 is absent. Standing fork-push permission is not recorded as release publication approval.


### I344-L266 — inputs/issues/344.md:266

Requirement: Each #341 relaxation the release needs lands with a bidirectional test: the newly permitted pattern passes and the secret and PII fixtures are still blocked.

Artifact observations: The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.


### I344-L267 — inputs/issues/344.md:267

Requirement: The first merge-cadence run records divergence, patch-refresh and ES conflict numbers.

Artifact observations: The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.


### I344-L268 — inputs/issues/344.md:268

Requirement: The hosted-QA experiment log records N=10 boot and flow runs, the failure count and the transfer cost, with no timing claims.

Artifact observations: The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.


### I344-L269 — inputs/issues/344.md:269

Requirement: Redirect-sunset tracking records the fielded devices that have completed one fork-to-fork update.

Artifact observations: The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.


### I344-L270 — inputs/issues/344.md:270

Requirement: A QA-frame retention policy is written, and a one-sided regression limit for any timing gate.

Artifact observations: The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.


### I344-L276 — inputs/issues/344.md:276

Requirement: The feasibility proof on `GENERIC_X64` covers display ownership, compositing, focus, controller ownership and lifecycle when either process exits; any command interface is bound to localhost with the address recorded.

Artifact observations: The source checkbox is explicitly #344 contract P6 — Post-0.0.1 Step0 under D-WORKFLOW-102, separately owned by #336/#339/#346. Current M7 plan keeps the existing ES/RetroArch launch stack.


### I344-L277 — inputs/issues/344.md:277

Requirement: A background Tier 1 report covers the files Step 0 did not touch; the launch-slice review follows the spike.

Artifact observations: The source checkbox is explicitly #344 contract P6 — Post-0.0.1 Step0 under D-WORKFLOW-102, separately owned by #336/#339/#346. Current M7 plan keeps the existing ES/RetroArch launch stack.


### I344-L278 — inputs/issues/344.md:278

Requirement: The bidirectional RetroArch → runner → RetroArch interchange test (saves, states, auto-slot, pending achievements, queue location) passes before #336 Step 1.

Artifact observations: The source checkbox is explicitly #344 contract P6 — Post-0.0.1 Step0 under D-WORKFLOW-102, separately owned by #336/#339/#346. Current M7 plan keeps the existing ES/RetroArch launch stack.


### I344-L299 — inputs/issues/344.md:299

Requirement: Each row above the owner approves is in `docs/decision-register.md` with its ID, and `tools/register-check` passes.

Artifact observations: The source issue maps approved fourteen-row decisions to D-WORKFLOW-115–126 and explicitly names superseded102/CLOUD158/P0 rows. Direct register reads match the approved changes; fresh tools/register-check exits0 with599 IDs, each once, and all live citations resolved.


## SOURCE docs/audits/2026_10_06-milestone-m7-p4-fixes-383/inputs/distribution-product-diff.patch

```text
1: diff --git a/distributions/ROCKNIX/options b/distributions/ROCKNIX/options
2: index 5ce69d6e26..79c92f1cdb 100644
3: --- a/distributions/ROCKNIX/options
4: +++ b/distributions/ROCKNIX/options
5: @@ -8,13 +8,13 @@
6:    HARDENING_SUPPORT="no"
7:  
8:  # The name of the parent organization for updates
9: -  GIT_ORGANIZATION="ROCKNIX"
10: +  GIT_ORGANIZATION="pixelelated"
11:  
12:  # The name of the github project for updates
13:    GIT_REPO="distribution"
14:  
15:  # Name of the Distro to build (full name, without special characters)
16: -  DISTRONAME="ROCKNIX"
17: +  DISTRONAME="pixelelated"
18:  
19:  # Name of the OS to build (full name, lower case, without special characters)
20:    OSNAME="rocknix"
21: @@ -23,13 +23,13 @@
22:    DESCRIPTION="An Open Source firmware."
23:  
24:  # Distribution Home URL
25: -  HOME_URL="https://rocknix.org"
26: +  HOME_URL="https://pixelelated.com"
27:  
28:  # Documentation URL
29: -  WIKI_URL="https://rocknix.org"
30: +  WIKI_URL="https://github.com/pixelelated/distribution/tree/next/docs"
31:  
32:  # Where to report bugs
33: -  BUG_REPORT_URL="https://rocknix.org"
34: +  BUG_REPORT_URL="https://github.com/pixelelated/distribution/issues"
35:  
36:  # Root password to integrate in the target system
37:    ROOT_PASSWORD="rocknix"
38: diff --git a/distributions/ROCKNIX/version b/distributions/ROCKNIX/version
39: index 9cfcbda200..4b27f51fa0 100644
40: --- a/distributions/ROCKNIX/version
41: +++ b/distributions/ROCKNIX/version
42: @@ -2,4 +2,7 @@
43:    DISTRO_VERSION="devel"
44:  
45:  # OS_VERSION: OS Version
46: -  OS_VERSION="$(date +%Y%m%d)"
47: +  OS_VERSION="0.0.1"
48: +
49: +# RC2 accepts an adoption tar whose name still contains ROCKNIX (D-WORKFLOW-128).
50: +  IMAGE_SUFFIX="from-ROCKNIX"
51: diff --git a/packages/linux/package.mk b/packages/linux/package.mk
52: index 7f022fbc75..9177177894 100644
53: --- a/packages/linux/package.mk
54: +++ b/packages/linux/package.mk
55: @@ -128,8 +128,8 @@ pre_make_target() {
56:    # set initramfs source
57:    ${PKG_BUILD}/scripts/config --set-str CONFIG_INITRAMFS_SOURCE "$(kernel_initramfs_confs) ${BUILD}/initramfs"
58:  
59: -  # set default hostname based on ${DISTRONAME}
60: -  ${PKG_BUILD}/scripts/config --set-str CONFIG_DEFAULT_HOSTNAME "${DISTRONAME}"
61: +  # Keep the RC2 network identity across the display rename (D-WORKFLOW-123).
62: +  ${PKG_BUILD}/scripts/config --set-str CONFIG_DEFAULT_HOSTNAME "ROCKNIX"
63:  
64:    # disable swap support if not enabled
65:    if [ ! "${SWAP_SUPPORT}" = yes ]; then
66: diff --git a/packages/web/libsoup/package.mk b/packages/web/libsoup/package.mk
67: index 78aa198fc2..3ac0f4593d 100644
68: --- a/packages/web/libsoup/package.mk
69: +++ b/packages/web/libsoup/package.mk
70: @@ -2,9 +2,8 @@
71:  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
72:  
73:  PKG_NAME="libsoup"
74: -# freshness: pinned -- 3.8.0 is a new series (GNOME's 3.8, 2026-09) under the WebKitGTK the sign-in window is built on; the 3.6 series stays for 0.0.1 and moves with the next WebKitGTK bump (fork #362)
75: -PKG_VERSION="3.6.6"
76: -PKG_SHA256="51ed0ae06f9d5a40f401ff459e2e5f652f9a510b7730e1359ee66d14d4872740"
77: +PKG_VERSION="3.8.0"
78: +PKG_SHA256="bbf08fa3e03a88c31a3d27a0d87cb422e9490f2d08e149211103df6d638a2238"
79:  PKG_LICENSE="LGPL-2.1-or-later"
80:  PKG_SITE="https://libsoup.gnome.org/"
81:  PKG_URL="https://download.gnome.org/sources/${PKG_NAME}/${PKG_VERSION:0:3}/${PKG_NAME}-${PKG_VERSION}.tar.xz"
82: @@ -14,6 +13,8 @@ PKG_LONGDESC="HTTP client/server library for GNOME; WebKit's network backend."
83:  pre_configure_target() {
84:    # No introspection, docs or tests in an image build; brotli, ntlm and
85:    # sysprof are all optional and unused by the WebKit network process.
86: +  # Keep 3.8's new optional zstd decoder explicit, independent of which
87: +  # other packages happen to have populated the shared sysroot (#362).
88:    PKG_MESON_OPTS_TARGET="-Dintrospection=disabled \
89:                           -Dvapi=disabled \
90:                           -Ddocs=disabled \
91: @@ -21,6 +22,7 @@ pre_configure_target() {
92:                           -Dsysprof=disabled \
93:                           -Dntlm=disabled \
94:                           -Dbrotli=disabled \
95: +                         -Dzstd=disabled \
96:                           -Dgssapi=disabled \
97:                           -Dtls_check=false"
98:  }
99: diff --git a/packages/web/webkitgtk/package.mk b/packages/web/webkitgtk/package.mk
100: index d2d51100cf..eb94b26e14 100644
101: --- a/packages/web/webkitgtk/package.mk
102: +++ b/packages/web/webkitgtk/package.mk
103: @@ -2,8 +2,8 @@
104:  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
105:  
106:  PKG_NAME="webkitgtk"
107: -PKG_VERSION="2.54.0"
108: -PKG_SHA256="846fd19ccedbae1dbfe904f26dbf2d68a800a33a50caf2ad5222c8dcb3f25682"
109: +PKG_VERSION="2.54.1"
110: +PKG_SHA256="ea0bbb02dbdbc596874a4e7ad35b66645b3e0a232bd0e4081de5ed92eb0a397d"
111:  PKG_LICENSE="LGPL-2.1-or-later AND BSD-2-Clause"
112:  PKG_SITE="https://webkitgtk.org/"
113:  PKG_URL="https://webkitgtk.org/releases/${PKG_NAME}-${PKG_VERSION}.tar.xz"
114: diff --git a/projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/sway/sway-generic-x64 b/projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/sway/sway-generic-x64
115: new file mode 100755
116: index 0000000000..a46bc88c1a
117: --- /dev/null
118: +++ b/projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/sway/sway-generic-x64
119: @@ -0,0 +1,40 @@
120: +#!/bin/sh
121: +# SPDX-License-Identifier: GPL-2.0-or-later
122: +# Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
123: +
124: +# Non-virgl virtio scanout can keep stale host frames with GLES2/llvmpipe.
125: +# Use Pixman only on that device, not on accelerated or unidentified GPUs.
126: +# This wrapper is installed only on GENERIC_X64 and makes no storage changes.
127: +select_software_renderer() {
128: +  [ -z "${WLR_RENDERER:-}" ] || return
129: +  [ -z "${WLR_RENDER_DRM_DEVICE:-}" ] || return
130: +  case "${WLR_DRM_DEVICES:-}" in
131: +    /dev/dri/card*) card_number=${WLR_DRM_DEVICES#/dev/dri/card} ;;
132: +    *) return ;;
133: +  esac
134: +  case "$card_number" in
135: +    ''|*[!0-9]*) return ;; # Unknown paths or multiple GPUs: retain selection.
136: +  esac
137: +
138: +  # Linux virtio_gpu registers DRM against the transport parent. Negotiated
139: +  # features belong to its virtio child, not the DRM card's device symlink.
140: +  set -- /sys/class/drm/card${card_number}/device/virtio[0-9]*
141: +  [ "$#" -eq 1 ] && [ -d "$1" ] || return
142: +  driver=$(readlink "$1/driver")
143: +  [ "${driver##*/}" = virtio_gpu ] || return
144: +
145: +  # Virtio sysfs emits negotiated bits lowest-first; VIRTIO_GPU_F_VIRGL is0.
146: +  # A render node is not proof of virgl: DRIVER_RENDER is set in both modes.
147: +  features=$(cat "$1/features" 2>/dev/null) || return
148: +  case "$features" in
149: +    ''|*[!01]*) return ;;
150: +    0*)
151: +      [ "${#features}" -ge 64 ] || return
152: +      export WLR_RENDERER=pixman
153: +      logger -t Sway 'GENERIC_X64: Pixman for virtio GPU without virgl'
154: +      ;;
155: +  esac
156: +}
157: +
158: +select_software_renderer
159: +exec /usr/bin/sway.sh "$@"
160: diff --git a/projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf b/projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf
161: new file mode 100644
162: index 0000000000..6f2883b860
163: --- /dev/null
164: +++ b/projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf
165: @@ -0,0 +1,3 @@
166: +[Service]
167: +ExecStart=
168: +ExecStart=/usr/lib/sway/sway-generic-x64
169: diff --git a/projects/ROCKNIX/devices/GENERIC_X64/options b/projects/ROCKNIX/devices/GENERIC_X64/options
170: index 5f94718161..9038263b95 100644
171: --- a/projects/ROCKNIX/devices/GENERIC_X64/options
172: +++ b/projects/ROCKNIX/devices/GENERIC_X64/options
173: @@ -71,8 +71,9 @@
174:      SYSTEM_SIZE="4096"
175:      SYSTEM_PART_START="8192"
176:  
177: -  # Extra command line for x86_64
178: -    EXTRA_CMDLINE="console=ttyS0,115200 console=tty0"
179: +  # Keep kernel console redraws from erasing the framebuffer splash (#433).
180: +  # Serial QA access stays enabled; remove quiet and add debugging for verbosity.
181: +    EXTRA_CMDLINE="quiet console=ttyS0,115200 console=tty0"
182:  
183:    # Disable joypad driver for x86_64
184:      ROCKNIX_JOYPAD="no"
185: diff --git a/projects/ROCKNIX/devices/GENERIC_X64/vm/README.md b/projects/ROCKNIX/devices/GENERIC_X64/vm/README.md
186: index fc64f44944..c835d50eae 100644
187: --- a/projects/ROCKNIX/devices/GENERIC_X64/vm/README.md
188: +++ b/projects/ROCKNIX/devices/GENERIC_X64/vm/README.md
189: @@ -44,6 +44,25 @@ projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm \
190:    run --headless --res 640x480 target/ROCKNIX-GENERIC_X64.x86_64-<date>.qcow2
191:  ```
192:  
193: +Normal boots suppress kernel console messages so console redraws cannot erase
194: +the framebuffer splash. The serial QA shell and kernel journal remain available.
195: +The initramfs applies this default on upgraded GENERIC_X64 guests whose existing
196: +boot configuration lacks `quiet`. For verbose boot diagnosis, remove `quiet` and
197: +add `debugging` to the active boot entry (Syslinux on BIOS, GRUB on UEFI).
198: +
199: +On a virtio GPU without negotiated virgl support (`--gl none`), the
200: +GENERIC_X64 Sway service selects Pixman for composition. This avoids stale
201: +host-visible frames observed with GLES2/llvmpipe. Applications retain their
202: +own graphics drivers; accelerated virgl guests retain wlroots' normal
203: +renderer selection. The choice is recomputed at startup without changing
204: +saved settings. Explicit `WLR_RENDERER` or `WLR_RENDER_DRM_DEVICE` overrides,
205: +unidentified devices and multiple-card selections are left alone.
206: +
207: +The selector checks the chosen card's `virtio_gpu` driver and negotiated
208: +feature bit 0, not the presence of a render node: the kernel exposes render
209: +nodes in both modes. A journal entry tagged `Sway` records when Pixman is
210: +selected. This service override exists only in the GENERIC_X64 filesystem.
211: +
212:  Generate the UTM bundle (a qcow2 that needs another file -- a backing image,
213:  an external data file -- is refused: the bundle carries the one file; flatten
214:  it with `qemu-img convert -O qcow2` first):
215: diff --git a/projects/ROCKNIX/packages/graphics/SDL2/patches/0010-release-display-modes-on-display-removal.patch b/projects/ROCKNIX/packages/graphics/SDL2/patches/0010-release-display-modes-on-display-removal.patch
216: new file mode 100644
217: index 0000000000..26bccfd511
218: --- /dev/null
219: +++ b/projects/ROCKNIX/packages/graphics/SDL2/patches/0010-release-display-modes-on-display-removal.patch
220: @@ -0,0 +1,25 @@
221: +Subject: [PATCH] video: free mode storage when removing a display
222: +
223: +Wayland removes its displays during VideoQuit, before the generic cleanup
224: +loop. SDL_DelVideoDisplay drops the display count but does not release its
225: +mode array, so every video reinitialization leaks that allocation. Use the
226: +same mode/desktop cleanup as the normal quit path before removing the display.
227: +
228: +Downstream: rasteratops/distribution#310. Actual Wayland launch cycles under
229: +LeakSanitizer retain 768 bytes per cycle at SDL_AddDisplayMode before this fix.
230: +SDL 2.32.10 is the latest SDL2 release checked for this build; the SDL2 branch
231: +still has the same missing cleanup.
232: +
233: +--- a/src/video/SDL_video.c
234: ++++ b/src/video/SDL_video.c
235: +@@ -693,6 +693,10 @@
236: +     }
237: + 
238: +     SDL_SendDisplayEvent(&_this->displays[index], SDL_DISPLAYEVENT_DISCONNECTED, 0);
239: ++
240: ++    SDL_ResetDisplayModes(index);
241: ++    SDL_free(_this->displays[index].desktop_mode.driverdata);
242: ++    _this->displays[index].desktop_mode.driverdata = NULL;
243: + 
244: +     SDL_free(_this->displays[index].driverdata);
245: +     _this->displays[index].driverdata = NULL;
246: diff --git a/projects/ROCKNIX/packages/graphics/glslang/package.mk b/projects/ROCKNIX/packages/graphics/glslang/package.mk
247: index 1ef4a14dce..9f434a8af9 100644
248: --- a/projects/ROCKNIX/packages/graphics/glslang/package.mk
249: +++ b/projects/ROCKNIX/packages/graphics/glslang/package.mk
250: @@ -1,14 +1,15 @@
251:  # SPDX-License-Identifier: GPL-2.0
252:  # Copyright (C) 2021-present Frank Hartung (supervisedthinking (@) gmail.com)
253:  # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
254: +# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
255:  
256:  PKG_NAME="glslang"
257:  # The SPIRV-Tools & SPIRV-Headers pkg_version/s need to match the compatible (known_good) glslang pkg_version.
258:  # https://raw.githubusercontent.com/KhronosGroup/glslang/${PKG_VERSION}/known_good.json
259:  # When updating glslang pkg_version please update to the known_good spirv-tools & spirv-headers pkg_version/s.
260: -PKG_VERSION="15.1.0"
261: -PKG_SHA256="4bdcd8cdb330313f0d4deed7be527b0ac1c115ff272e492853a6e98add61b4bc"
262: -PKG_LICENSE="Apache-2.0"
263: +PKG_VERSION="16.6.0"
264: +PKG_SHA256="9c09b901149c729df745057dafa815278aaa101b84d2b6e14f16a42de52f97f2"
265: +PKG_LICENSE="BSD-3-Clause AND BSD-2-Clause AND MIT AND Apache-2.0"
266:  PKG_SITE="https://github.com/KhronosGroup/glslang"
267:  PKG_URL="https://github.com/KhronosGroup/glslang/archive/${PKG_VERSION}.tar.gz"
268:  PKG_DEPENDS_HOST="toolchain:host Python3:host"
269: @@ -17,7 +18,6 @@ PKG_LONGDESC="Khronos-reference front end for GLSL/ESSL, partial front end for H
270:  PKG_DEPENDS_UNPACK="spirv-headers spirv-tools"
271:  
272:  PKG_CMAKE_OPTS_COMMON="-DBUILD_EXTERNAL=ON \
273: -                       -DENABLE_SPVREMAPPER=OFF \
274:                         -DENABLE_GLSLANG_JS=OFF \
275:                         -DENABLE_RTTI=OFF \
276:                         -DENABLE_EXCEPTIONS=OFF \
277: diff --git a/projects/ROCKNIX/packages/graphics/mesa/patches/001-rtasm-release-executable-heap-on-unload.patch b/projects/ROCKNIX/packages/graphics/mesa/patches/001-rtasm-release-executable-heap-on-unload.patch
278: new file mode 100644
279: index 0000000000..51176f6c4f
280: --- /dev/null
281: +++ b/projects/ROCKNIX/packages/graphics/mesa/patches/001-rtasm-release-executable-heap-on-unload.patch
282: @@ -0,0 +1,69 @@
283: +Subject: [PATCH] rtasm: release the executable heap when the driver unloads
284: +
285: +The POSIX executable allocator retains a 10 MiB mmap after its suballocations
286: +are freed. When an application closes and reloads the DRI driver (for example,
287: +EmulationStation around each game), the static pointers are lost and a new
288: +heap is mapped each time. Register cleanup with atexit, as other Mesa global
289: +resources do; on our glibc target it also runs when the owning DSO unloads.
290: +
291: +Publish the heap only after both allocations succeed, and unwind allocation
292: +or callback-registration failure so a later call can retry. The arena stays
293: +shared and locked during normal operation; no per-shader mmap is introduced.
294: +
295: +Downstream: rasteratops/distribution#310. Mesa 26.2.2; current upstream still
296: +has the same unpaired mmap. See docs/qa-logs/2026-10-03-launch-memory/.
297: +
298: +--- a/src/gallium/auxiliary/rtasm/rtasm_execmem.c
299: ++++ b/src/gallium/auxiliary/rtasm/rtasm_execmem.c
300: +@@ -67,18 +67,44 @@
301: + static unsigned char *exec_mem = NULL;
302: + 
303: + 
304: ++static void
305: ++destroy_heap(void)
306: ++{
307: ++   u_mmDestroy(exec_heap);
308: ++   exec_heap = NULL;
309: ++   munmap(exec_mem, EXEC_HEAP_SIZE);
310: ++   exec_mem = NULL;
311: ++}
312: ++
313: ++
314: + static int
315: + init_heap(void)
316: + {
317: +-   if (!exec_heap)
318: +-      exec_heap = u_mmInit( 0, EXEC_HEAP_SIZE );
319: ++   if (exec_heap)
320: ++      return 1;
321: + 
322: +-   if (!exec_mem)
323: +-      exec_mem = (unsigned char *) mmap(NULL, EXEC_HEAP_SIZE,
324: +-         PROT_EXEC | PROT_READ | PROT_WRITE,
325: +-         MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
326: ++   exec_mem = (unsigned char *) mmap(NULL, EXEC_HEAP_SIZE,
327: ++      PROT_EXEC | PROT_READ | PROT_WRITE,
328: ++      MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
329: ++   if (exec_mem == MAP_FAILED)
330: ++      return 0;
331: + 
332: +-   return (exec_mem != MAP_FAILED);
333: ++   exec_heap = u_mmInit(0, EXEC_HEAP_SIZE);
334: ++   if (!exec_heap) {
335: ++      munmap(exec_mem, EXEC_HEAP_SIZE);
336: ++      exec_mem = NULL;
337: ++      return 0;
338: ++   }
339: ++
340: ++   /* The DRI driver can be unloaded before the process exits. Return the
341: ++    * executable arena as well as its bookkeeping when that happens.
342: ++    */
343: ++   if (atexit(destroy_heap) != 0) {
344: ++      destroy_heap();
345: ++      return 0;
346: ++   }
347: ++
348: ++   return 1;
349: + }
350: + 
351: + 
352: diff --git a/projects/ROCKNIX/packages/graphics/mesa/patches/002-virgl-release-empty-screen-cache.patch b/projects/ROCKNIX/packages/graphics/mesa/patches/002-virgl-release-empty-screen-cache.patch
353: new file mode 100644
354: index 0000000000..9c729f3824
355: --- /dev/null
356: +++ b/projects/ROCKNIX/packages/graphics/mesa/patches/002-virgl-release-empty-screen-cache.patch
357: @@ -0,0 +1,46 @@
358: +Subject: [PATCH] virgl: release an empty screen cache after probe or teardown
359: +
360: +The process-global fd table survives a failed virgl probe and the last screen
361: +release. If the driver is unloaded, its pointer is lost. A software-rendered
362: +application that repeatedly reloads Mesa then leaks the empty table each time.
363: +Destroy an empty table under the existing screen mutex, on both paths. Live
364: +screen entries and their sharing/refcounts are unchanged.
365: +
366: +Downstream: rasteratops/distribution#310. LeakSanitizer names 592 bytes per
367: +failed software-profile probe at virgl_drm_screen_create in Mesa 26.2.2.
368: +
369: +--- a/src/gallium/winsys/virgl/drm/virgl_drm_winsys.c
370: ++++ b/src/gallium/winsys/virgl/drm/virgl_drm_winsys.c
371: +@@ -1305,6 +1305,16 @@
372: + static struct hash_table *fd_tab = NULL;
373: + static simple_mtx_t virgl_screen_mutex = SIMPLE_MTX_INITIALIZER;
374: + 
375: ++/* Called with virgl_screen_mutex held. No screen owns an empty cache. */
376: ++static void
377: ++virgl_drm_release_empty_screen_cache(void)
378: ++{
379: ++   if (fd_tab && fd_tab->entries == 0) {
380: ++      _mesa_hash_table_destroy(fd_tab, NULL);
381: ++      fd_tab = NULL;
382: ++   }
383: ++}
384: ++
385: + static void
386: + virgl_drm_screen_destroy(struct pipe_screen *pscreen)
387: + {
388: +@@ -1317,6 +1327,7 @@
389: +    if (destroy) {
390: +       fd = virgl_drm_winsys(screen->vws)->fd;
391: +       _mesa_hash_table_remove_key(fd_tab, intptr_to_pointer(fd));
392: ++      virgl_drm_release_empty_screen_cache();
393: +    }
394: +    simple_mtx_unlock(&virgl_screen_mutex);
395: + 
396: +@@ -1405,6 +1416,7 @@
397: +    }
398: + 
399: + unlock:
400: ++   virgl_drm_release_empty_screen_cache();
401: +    simple_mtx_unlock(&virgl_screen_mutex);
402: +    return pscreen;
403: + }
404: diff --git a/projects/ROCKNIX/packages/graphics/shaderc/patches/001-fix-overwriting-dependencies.patch b/projects/ROCKNIX/packages/graphics/shaderc/patches/001-fix-overwriting-dependencies.patch
405: index 443d514aec..87cc8cbc54 100644
406: --- a/projects/ROCKNIX/packages/graphics/shaderc/patches/001-fix-overwriting-dependencies.patch
407: +++ b/projects/ROCKNIX/packages/graphics/shaderc/patches/001-fix-overwriting-dependencies.patch
408: @@ -23,4 +23,4 @@ index 1277d87e73..058a1e8121 100644
409:  +  #add_dependencies(glslc_exe build-version)
410:   endif(SHADERC_ENABLE_EXECUTABLES)
411:   
412: - shaderc_add_tests(
413: \ No newline at end of file
414: + shaderc_add_tests(
415: diff --git a/projects/ROCKNIX/packages/graphics/spirv-headers/package.mk b/projects/ROCKNIX/packages/graphics/spirv-headers/package.mk
416: index 687ebd3320..3023b85a54 100644
417: --- a/projects/ROCKNIX/packages/graphics/spirv-headers/package.mk
418: +++ b/projects/ROCKNIX/packages/graphics/spirv-headers/package.mk
419: @@ -1,14 +1,16 @@
420:  # SPDX-License-Identifier: GPL-2.0
421:  # Copyright (C) 2021-present Frank Hartung (supervisedthinking (@) gmail.com)
422:  # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
423: +# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
424:  
425:  PKG_NAME="spirv-headers"
426:  # The SPIRV-Headers pkg_version needs to match the compatible (known_good) glslang pkg_version.
427:  # https://raw.githubusercontent.com/KhronosGroup/glslang/${PKG_VERSION}/known_good.json
428:  # When updating glslang pkg_version please update to the known_good spirv-headers pkg_version.
429: -PKG_VERSION="3f17b2af6784bfa2c5aa5dbb8e0e74a607dd8b3b"
430: -PKG_SHA256="2301e11e5c77213258d6863bf4e6c607a8c6431fa8336e98ac6a2131bd6284f8"
431: -PKG_LICENSE="Apache-2.0"
432: +# freshness: pinned -- follows glslang16.6.0 known_good.json; SPIRV-Tools DEPS names the same headers (#386)
433: +PKG_VERSION="496543121ce6419f23d6fa5d7194ba66c36212d2"
434: +PKG_SHA256="a9bb9c48713245eacf97cc539b6f1d45405a92d8813f8b82e635f0a085ee9898"
435: +PKG_LICENSE="MIT"
436:  PKG_SITE="https://github.com/KhronosGroup/SPIRV-headers"
437:  PKG_URL="https://github.com/KhronosGroup/SPIRV-headers/archive/${PKG_VERSION}.tar.gz"
438:  PKG_DEPENDS_HOST=""
439: diff --git a/projects/ROCKNIX/packages/graphics/spirv-tools/package.mk b/projects/ROCKNIX/packages/graphics/spirv-tools/package.mk
440: index 134653d525..a95b993862 100644
441: --- a/projects/ROCKNIX/packages/graphics/spirv-tools/package.mk
442: +++ b/projects/ROCKNIX/packages/graphics/spirv-tools/package.mk
443: @@ -1,13 +1,15 @@
444:  # SPDX-License-Identifier: GPL-2.0
445:  # Copyright (C) 2021-present Frank Hartung (supervisedthinking (@) gmail.com)
446:  # Copyright (C) 2021-present Team LibreELEC (https://libreelec.tv)
447: +# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
448:  
449:  PKG_NAME="spirv-tools"
450:  # The SPIRV-Tools pkg_version needs to match the compatible (known_good) glslang pkg_version.
451:  # https://raw.githubusercontent.com/KhronosGroup/glslang/${PKG_VERSION}/known_good.json
452:  # When updating glslang pkg_version please update to the known_good spirv-tools pkg_version.
453: -PKG_VERSION="4d2f0b40bfe290dea6c6904dafdf7fd8328ba346"
454: -PKG_SHA256="41481a45441d92b2404aa06bdecbb0302f22636335be4e19023632c83fa89aa1"
455: +# freshness: pinned -- follows glslang16.6.0 known_good.json; SPIRV-Tools DEPS names the same headers (#386)
456: +PKG_VERSION="ef96ed763b43b59b33b31b362f09a02b729fa1c9"
457: +PKG_SHA256="82c62146083fd558735a3171cf97cfc47903ca7d368482e87f94bd44883c0f00"
458:  PKG_LICENSE="Apache-2.0"
459:  PKG_SITE="https://github.com/KhronosGroup/SPIRV-Tools"
460:  PKG_URL="https://github.com/KhronosGroup/SPIRV-Tools/archive/${PKG_VERSION}.tar.gz"
461: diff --git a/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/analog_sticks_ledcontrol b/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/analog_sticks_ledcontrol
462: index b3a90018f8..2c17623df8 100644
463: --- a/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/analog_sticks_ledcontrol	
464: +++ b/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/analog_sticks_ledcontrol	
465: @@ -6,7 +6,7 @@
466:  # Simple script to set led brightness and rgb color based on
467:  # brightness and rgb values from emulation station
468:  
469: -LED_PATH="/sys/devices/platform/"
470: +LED_PATH="${LED_PATH:-/sys/devices/platform/}"
471:  
472:  function led_brightness() {
473:    n=1
474: diff --git a/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/battery_led_status b/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/battery_led_status
475: index c98fcc4480..acf8f6bb0a 100644
476: --- a/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/battery_led_status	
477: +++ b/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/battery_led_status	
478: @@ -8,7 +8,8 @@
479:  
480:  . /etc/profile
481:  
482: -LED_PATH="/sys/devices/platform/"
483: +LED_PATH="${LED_PATH:-/sys/devices/platform/}"
484: +BATTERY_PATH="${BATTERY_PATH:-/sys/class/power_supply/battery}"
485:  
486:  function bat_led_off() {
487:    n=1
488: @@ -24,8 +25,8 @@ function bat_led_off() {
489:  function bat_led_red() {
490:    n=1
491:    while [ "$n" -lt 5 ]; do
492: -    echo 255 >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/brightness
493: -    echo 255 >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/brightness
494: +    echo "${LED_BRIGHTNESS}" >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/brightness
495: +    echo "${LED_BRIGHTNESS}" >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/brightness
496:      echo 0 0 255 >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/multi_intensity
497:      echo 0 0 255 >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/multi_intensity
498:      n=$(( n + 1 ))
499: @@ -35,8 +36,8 @@ function bat_led_red() {
500:  function bat_led_green() {
501:    n=1
502:    while [ "$n" -lt 5 ]; do
503: -    echo 255 >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/brightness
504: -    echo 255 >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/brightness
505: +    echo "${LED_BRIGHTNESS}" >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/brightness
506: +    echo "${LED_BRIGHTNESS}" >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/brightness
507:      echo 0 255 0 >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/multi_intensity
508:      echo 0 255 0 >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/multi_intensity
509:      n=$(( n + 1 ))
510: @@ -46,8 +47,8 @@ function bat_led_green() {
511:  function bat_led_orange() {
512:    n=1
513:    while [ "$n" -lt 5 ]; do
514: -    echo 255 >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/brightness
515: -    echo 255 >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/brightness
516: +    echo "${LED_BRIGHTNESS}" >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/brightness
517: +    echo "${LED_BRIGHTNESS}" >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/brightness
518:      echo 0 20 255 >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/multi_intensity
519:      echo 0 20 255 >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/multi_intensity
520:      n=$(( n + 1 ))
521: @@ -57,8 +58,8 @@ function bat_led_orange() {
522:  function bat_led_yellow() {
523:    n=1
524:    while [ "$n" -lt 5 ]; do
525: -    echo 255 >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/brightness
526: -    echo 255 >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/brightness
527: +    echo "${LED_BRIGHTNESS}" >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/brightness
528: +    echo "${LED_BRIGHTNESS}" >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/brightness
529:      echo 0 125 255 >  ${LED_PATH}/multi-ledl${n}/leds/rgb:l${n}/multi_intensity
530:      echo 0 125 255 >  ${LED_PATH}/multi-ledr${n}/leds/rgb:r${n}/multi_intensity
531:      n=$(( n + 1 ))
532: @@ -72,8 +73,14 @@ while true
533:    if [ ! ${BAT_LED_STATE} == "battery" ]; then
534:      break
535:    else
536: -    CAP=$(cat /sys/class/power_supply/battery/capacity)
537: -    STAT=$(cat /sys/class/power_supply/battery/status)
538: +    # Keep the selected level across color changes and low-battery blinks.
539: +    case "$(get_setting led.brightness)" in
540: +      min) LED_BRIGHTNESS=32 ;;
541: +      mid) LED_BRIGHTNESS=128 ;;
542: +      *) LED_BRIGHTNESS=255 ;;
543: +    esac
544: +    CAP=$(cat "${BATTERY_PATH}/capacity")
545: +    STAT=$(cat "${BATTERY_PATH}/status")
546:        if [ ${STAT} == "Discharging" ]; then
547:          if (( ${CAP} <= 10 ))
548:            then
549: diff --git a/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/ledcontrol b/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/ledcontrol
550: index 72f5cb92fb..2b8bdb0a8d 100644
551: --- a/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/ledcontrol	
552: +++ b/projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/ledcontrol	
553: @@ -8,7 +8,7 @@
554:  # (fork #332's first criterion); on the device it is the platform's.
555:  LED_PATH="${LED_PATH:-/sys/devices/platform/}"
556:  
557: -# The six LEDs' brightness, 0-255 (the colour stays in multi_intensity).
558: +# The eight LEDs' brightness, 0-255 (the colour stays in multi_intensity).
559:  function led_brightness_all() {
560:    n=1
561:    while [ "$n" -lt 5 ]; do
562: @@ -60,7 +60,7 @@ case ${1} in
563:    ;;
564:    brightness)
565:      # LED BRIGHTNESS (max|mid|min): the case the row called and nothing
566: -    # answered (fork #332). Written to the six LEDs whatever the colour
567: +    # answered (fork #332). Written to the eight LEDs whatever the colour
568:      # case, and remembered for the next rgb with no colour set.
569:      led_brightness_all "$(brightness_value "${2}")"
570:      set_setting led.brightness ${2}
571: diff --git a/projects/ROCKNIX/packages/hardware/quirks/profile.d/999-export b/projects/ROCKNIX/packages/hardware/quirks/profile.d/999-export
572: index dc44ba28bb..8514a6f5df 100755
573: --- a/projects/ROCKNIX/packages/hardware/quirks/profile.d/999-export
574: +++ b/projects/ROCKNIX/packages/hardware/quirks/profile.d/999-export
575: @@ -5,7 +5,8 @@
576:  ### If you add a variable that should persist across processes,
577:  ### remember to export it here.
578:  
579: -export  OS_VERSION \
580: +export  OS_NAME \
581: +	OS_VERSION \
582:  	OS_BUILD \
583:  	SLOW_CORES \
584:  	FAST_CORES \
585: diff --git a/projects/ROCKNIX/packages/linux/package.mk b/projects/ROCKNIX/packages/linux/package.mk
586: index cbe7df55fe..36d6cde809 100644
587: --- a/projects/ROCKNIX/packages/linux/package.mk
588: +++ b/projects/ROCKNIX/packages/linux/package.mk
589: @@ -156,8 +156,8 @@ pre_make_target() {
590:    # set initramfs source
591:    ${PKG_BUILD}/scripts/config --set-str CONFIG_INITRAMFS_SOURCE "$(kernel_initramfs_confs) ${BUILD}/initramfs"
592:  
593: -  # set default hostname based on ${DISTRONAME}
594: -  ${PKG_BUILD}/scripts/config --set-str CONFIG_DEFAULT_HOSTNAME "${DISTRONAME}"
595: +  # Keep the RC2 network identity across the display rename (D-WORKFLOW-123).
596: +  ${PKG_BUILD}/scripts/config --set-str CONFIG_DEFAULT_HOSTNAME "ROCKNIX"
597:  
598:    # disable swap support if not enabled
599:    if [ ! "${SWAP_SUPPORT}" = yes ]; then
600: diff --git a/projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml b/projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml
601: index 206ddce8ca..e14b1f34ea 100644
602: --- a/projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml
603: +++ b/projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml
604: @@ -3,7 +3,7 @@
605:      <game>
606:          <path>./commander.sh</path>
607:          <name>File Manager</name>
608: -        <desc>Enables you to browse the ROCKNIX filesystem and manage files directly on your device. You can also use this tool to copy files from external drives to your ROCKNIX filesystem.</desc>
609: +        <desc>Browse files on your device and copy files to or from external drives.</desc>
610:          <developer>Tardigrade and ROCKNIX</developer>
611:          <publisher>ROCKNIX</publisher>
612:          <rating>5.0</rating>
613: @@ -38,8 +38,8 @@
614:      </game>
615:      <game>
616:          <path>./Install ROCKNIX.sh</path>
617: -        <name>Install ROCKNIX</name>
618: -        <desc>Use this utility to install ROCKNIX to the local storage on your device. Note: This process will wipe the drive that you choose to install ROCKNIX on.</desc>
619: +        <name>Install pixelelated</name>
620: +        <desc>Install pixelelated to your device's local storage. This erases all data on the drive you select.</desc>
621:          <developer>ROCKNIX</developer>
622:          <publisher>ROCKNIX</publisher>
623:          <rating>5.0</rating>
624: @@ -51,7 +51,7 @@
625:      <game>
626:          <path>./Start PortMaster.sh</path>
627:          <name>PortMaster</name>
628: -        <desc>PortMaster is a simple tool that allows you to download various game ports that are available for ROCKNIX and other ARM based devices. You can find details at portmaster.games</desc>
629: +        <desc>Download game ports for pixelelated and other supported devices. Learn more at portmaster.games.</desc>
630:          <developer>Portmaster</developer>
631:          <publisher>Portmaster</publisher>
632:          <rating>5.0</rating>
633: @@ -63,7 +63,7 @@
634:      <game>
635:          <path>./cloud_backup.sh</path>
636:          <name>RCLONE Backup</name>
637: -        <desc>Backup your saves to a cloud drive using RCLONE. Please make sure you have followed the steps at rocknix.org to set up RCLONE first.</desc>
638: +        <desc>Back up saves to your cloud storage. Set up your cloud account in Game Settings &gt; Cloud Settings first.</desc>
639:          <developer>ROCKNIX</developer>
640:          <publisher>ROCKNIX</publisher>
641:          <rating>5.0</rating>
642: @@ -75,7 +75,7 @@
643:      <game>
644:          <path>./cloud_restore.sh</path>
645:          <name>RCLONE Restore</name>
646: -        <desc>Restores your saves from a cloud drive using RCLONE. Please make sure you have followed the steps at rocknix.org to set up RCLONE first.</desc>
647: +        <desc>Restore saves from your cloud storage. Set up your cloud account in Game Settings &gt; Cloud Settings first.</desc>
648:          <developer>ROCKNIX</developer>
649:          <publisher>ROCKNIX</publisher>
650:          <rating>5.0</rating>
651: @@ -389,7 +389,7 @@ it's recommended to have a mouse and keyboard to modify settings.</desc>
652:      <game>
653:          <path>./Start touchHLE.sh</path>
654:          <name>Start touchHLE</name>
655: -        <desc>Opens the touchHLE GUI (iOS) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings. A free and open-source application that emulates iOS games compatible with iOS 2 & 3, enabling people to play their iOS games on Windows, macOS, and Linux systems.</desc>
656: +        <desc>Opens the touchHLE GUI (iOS) to enable global configuration changes to be made directly to the emulator. It's recommended to have a mouse and keyboard available to modify settings. A free and open-source application that emulates iOS games compatible with iOS 2 &amp; 3, enabling people to play their iOS games on Windows, macOS, and Linux systems.</desc>
657:          <developer>ROCKNIX</developer>
658:          <publisher>ROCKNIX</publisher>
659:          <rating>5.0</rating>
660: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy-libchdr/package.mk b/projects/ROCKNIX/packages/network/raofflineproxy-libchdr/package.mk
661: index fa0fd0d95c..8fa68df8a4 100644
662: --- a/projects/ROCKNIX/packages/network/raofflineproxy-libchdr/package.mk
663: +++ b/projects/ROCKNIX/packages/network/raofflineproxy-libchdr/package.mk
664: @@ -3,16 +3,19 @@
665:  
666:  PKG_NAME="raofflineproxy-libchdr"
667:  # The commit RAOfflineProxy pins as its third_party/libchdr submodule at the
668: -# proxy's own pinned commit (248ce5a since 2026-09-28, the same submodule commit as at c1bd3724; unchanged since 4e9bab48, fork #165), read the same way as
669: -# raofflineproxy-rcheevos. The proxy's tarball carries the submodule as an
670: +# proxy's own pinned commit3036478f2b2d22db451396a48f44feee94e8462f,
671: +# verified 2026-10-05 from its third_party gitlinks (#361). This advances
672: +# 8e7b8bd through the parent's ANSI C compatibility update. Full pins and
673: +# native regression receipts are retained in the proxy3036478 QA record.
674: +# The proxy's tarball carries the submodule as an
675:  # empty directory; these sources (libchdr and the miniz, lzma and zstd
676:  # decoders it vendors under deps/) are compiled by raofflineproxy's recipe
677:  # into libraproxy_rchash.so so a CHD disc image hashes the way RetroArch
678:  # hashes it (fork #179). Source only: nothing here is built or installed on
679:  # its own.
680:  # freshness: pinned -- follows the third_party/libchdr submodule commit RAOfflineProxy names (fork #179)
681: -PKG_VERSION="8e7b8bd32bc676b7e5c6b42fe7d2daca986c4a0d"
682: -PKG_SHA256="04d6c61946c95addb78f4554740283b93249b81d8437e3d8a58ca1899c824dcc"
683: +PKG_VERSION="607694ca0812edfc9cc2030c64634fc2393668de"
684: +PKG_SHA256="02e772a74c4e5ec110bb646e729e1910268d2dae2c76df2a1b35525cc3826a9c"
685:  PKG_LICENSE="BSD-3-Clause"
686:  PKG_SITE="https://github.com/rtissera/libchdr"
687:  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
688: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy-rcheevos/package.mk b/projects/ROCKNIX/packages/network/raofflineproxy-rcheevos/package.mk
689: index 1e1743c574..712138e42f 100644
690: --- a/projects/ROCKNIX/packages/network/raofflineproxy-rcheevos/package.mk
691: +++ b/projects/ROCKNIX/packages/network/raofflineproxy-rcheevos/package.mk
692: @@ -3,9 +3,10 @@
693:  
694:  PKG_NAME="raofflineproxy-rcheevos"
695:  # The commit RAOfflineProxy pins as its third_party/rcheevos submodule at the
696: -# proxy's own pinned commit (248ce5a since 2026-09-28, the same submodule commit as at c1bd3724 and 0711f0b9, fork #259; upstream moved it from
697: -# 2ad0b86 in 095867d): read from the repository's
698: -# tree with `gh api repos/misantronic/RAOfflineProxy/contents/third_party`.
699: +# proxy's own pinned commit5866cd9ba784c13771a99c52dd6b6f2acc546842,
700: +# verified 2026-10-03 from its third_party gitlinks (#361). The submodule
701: +# commit is unchanged from248ce5a; full pins are retained in
702: +# docs/qa-logs/2026-10-03-proxy-refresh/coupled-pins.tsv.
703:  # GitHub's tarball of the proxy carries the submodule as an empty directory,
704:  # so the sources that rc_hash is built from come in through this package and
705:  # are compiled by raofflineproxy's own recipe into libraproxy_rchash.so, the
706: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/package.mk b/projects/ROCKNIX/packages/network/raofflineproxy/package.mk
707: index 9243fcae1e..b2b92f0056 100644
708: --- a/projects/ROCKNIX/packages/network/raofflineproxy/package.mk
709: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/package.mk
710: @@ -2,23 +2,22 @@
711:  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
712:  
713:  PKG_NAME="raofflineproxy"
714: -# Pinned by full commit (packages/README.md): main at 2026-09-28 (248ce5a,
715: -# step 0 of the release candidate; c1bd3724 of 2026-09-26 before, fork #293).
716: -# The 23 commits since c1bd3724 are the Android app (the stale login token's
717: -# 401 on award sync, #182; NetherSX2's host-override broadcast, #190; the
718: -# caching budget, #174), dependabot, and nightly CI. On the Linux side the
719: -# updater learned a nightly channel (update.py, #176/#179) -- reached only
720: -# from the CLI's update commands, which nothing on this image runs -- and
721: -# config.py stops taking the dArkOS path on spruce (#178), neither of which
722: -# is this image. The store, the proxy service and the cache keys are
723: -# unchanged; the login key was already lower-cased on Linux, which is the
724: -# half of #182 the Android app lacked. Both submodules are unchanged
725: -# (rcheevos 1433173, libchdr 8e7b8bd; D-RA-029, D-RA-037). Every patch
726: -# applies as it did; 008's config.py hunk header is moved eight lines to
727: -# where #178 left load_config. APP_VERSION still reads 1.13.0-alpha1.
728: -# freshness: pinned -- upstream's next four commits (93f98382bc, 2026-09-30) rewrite the Linux caching model into a 100-per-30-minutes budget with a queue, and nine of the fork's sixteen patches no longer apply to them; pinned for 0.0.1 pending the maintainer's disposition on fork #361
729: -PKG_VERSION="248ce5acae75113d09500cd7c6661a12fee4b93c"
730: -PKG_SHA256="5a430a6bc75d4d101ef983ea1c67897613387148f991daafac5a035637ec7cf5"
731: +# Current upstream main at2026-10-06; D-WORKFLOW-138/#361 selects the
732: +# refresh while retaining whole-library preparation and offline state.
733: +# The16 patches preserve the fork's service, recovery and image
734: +# behavior. Upstream now owns connection reuse and subset award mapping;
735: +# duplicate patches014/017 are retired. The explicit OS scanner opts out
736: +# of the100-game budget window but retains locks, request pacing and429
737: +# pauses, and never counts queued work as ready. See docs/rasteratops/
738: +# raofflineproxy-refresh.md for dispositions and exact host/VM boundaries.
739: +# Patch018 recognizes pixelelated without moving ROCKNIX account/cache paths (#408).
740: +# Coupled rcheevos/libchdr pins remain those in this parent (D-RA-029/037).
741: +# 879b158 retains b09d604's entire Linux/native trees and both gitlinks;
742: +# its delta is Android update notifications. Patch019 reads granted consent even
743: +# during early boot and invalidates the cache immediately (#457).
744: +# Source tests and installed-image proof remain separately recorded.
745: +PKG_VERSION="879b158995d412af434301ebdae581f66b8b6d57"
746: +PKG_SHA256="984957322337d1325f1b0fc11502336a80241ec511fd041c969bb0103c231664"
747:  # GPLv3 text with no "or any later version" grant in the sources.
748:  PKG_LICENSE="GPL-3.0-only"
749:  PKG_SITE="https://github.com/misantronic/RAOfflineProxy"
750: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/001-dorequest-4xx-passthrough.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/001-dorequest-4xx-passthrough.patch
751: index 42c6039bb9..dd3bae18a5 100644
752: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/001-dorequest-4xx-passthrough.patch
753: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/001-dorequest-4xx-passthrough.patch
754: @@ -25,11 +25,13 @@ Seen on ROCKNIX (fork issue maxengel/rocknix#166) with the proxy at
755:  for, and "Load failed (-29): Unknown game" without it. Offered upstream
756:  as-is (ROCKNIX D-RA-002: whatever the fork changes in the proxy goes back).
757:  
758: +diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
759: +index eb14239..cf8fab2 100644
760:  --- a/linux/raofflineproxy/proxy_service.py
761:  +++ b/linux/raofflineproxy/proxy_service.py
762: -@@ -81,6 +81,20 @@ REFRESH_PLAYED_WINDOW_DAYS = 7
763: - ONLINE_REFRESH_IDLE_DELAY_SECONDS = 5 * 60
764: +@@ -83,6 +83,20 @@ ONLINE_REFRESH_IDLE_DELAY_SECONDS = 5 * 60
765:   REFRESH_PLAYED_WINDOW_MS = REFRESH_PLAYED_WINDOW_DAYS * 24 * 60 * 60 * 1000
766: + CACHE_QUEUE_POLL_SECONDS = 60
767:   ALWAYS_TRY_UPSTREAM_ACTIONS = {"login", "login2"}
768:  +# A 4xx RetroAchievements sends for a dorequest.php call it understood but
769:  +# cannot satisfy -- 404 "Unknown game" for a hash with no set, 400 for a bad
770: @@ -48,7 +50,7 @@ as-is (ROCKNIX D-RA-002: whatever the fork changes in the proxy goes back).
771:   
772:   
773:   def is_static_asset_request(path: str) -> bool:
774: -@@ -527,6 +541,12 @@ class ProxyRuntimeServer(ThreadingTCPServer):
775: +@@ -529,6 +543,12 @@ class ProxyRuntimeServer(ThreadingTCPServer):
776:               return self.handle_offline_request(path, raw_body, action)
777:   
778:           if upstream[0] != "success":
779: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/002-no-synthetic-casual-only-achievement.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/002-no-synthetic-casual-only-achievement.patch
780: index 1a3dde30f7..63e2359ed9 100644
781: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/002-no-synthetic-casual-only-achievement.patch
782: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/002-no-synthetic-casual-only-achievement.patch
783: @@ -34,6 +34,8 @@ five seconds into every proxied session. The Android filter
784:  the same gap. Offered upstream as-is (ROCKNIX D-RA-002, D-RA-003: whatever
785:  the fork changes in the proxy goes back).
786:  
787: +diff --git a/linux/raofflineproxy/rom_cache.py b/linux/raofflineproxy/rom_cache.py
788: +index e904d78..9cad97a 100644
789:  --- a/linux/raofflineproxy/rom_cache.py
790:  +++ b/linux/raofflineproxy/rom_cache.py
791:  @@ -37,6 +37,12 @@ def filter_warning_achievement_ids(ids: list[int]) -> list[int]:
792: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/003-flush-stamp.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/003-flush-stamp.patch
793: index bcc47036d5..21d5893b5c 100644
794: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/003-flush-stamp.patch
795: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/003-flush-stamp.patch
796: @@ -21,6 +21,8 @@ ACHIEVEMENTS HAVE BEEN SENT TO RETROACHIEVEMENTS." Offered upstream as-is
797:  same file would serve the KNULLI integration, which already reads
798:  cached_game_ids.txt.
799:  
800: +diff --git a/linux/raofflineproxy/flusher.py b/linux/raofflineproxy/flusher.py
801: +index 2cb8b9d..d777bec 100644
802:  --- a/linux/raofflineproxy/flusher.py
803:  +++ b/linux/raofflineproxy/flusher.py
804:  @@ -2,13 +2,14 @@ from __future__ import annotations
805: @@ -31,7 +33,7 @@ cached_game_ids.txt.
806:   import time
807:   from dataclasses import dataclass
808:   
809: - from . import cache_keys
810: + from . import usage_stats
811:   from .auth import resolve_credentials
812:   from .award_signing import public_key_base64, sign_award, verify_award
813:  -from .config import FALLBACK_USER_AGENT, MAX_PROXY_PORT, upstream_host
814: @@ -39,28 +41,25 @@ cached_game_ids.txt.
815:   from .network import build_api_url, http_post
816:   from .rom_cache import (
817:       CacheGameAuthError,
818: -@@ -39,6 +40,11 @@ from .utils import (
819: +@@ -39,6 +40,7 @@ from .utils import (
820:   MAX_RETRIES = 5
821:   GENESIS_HASH = "genesis"
822:   MAX_AWARD_OFFSET_SECONDS = 14 * 24 * 60 * 60
823: -+# "<epoch> <flushed>", written after a flush that sent at least one award, for
824: -+# an OS integration to read (and remove, once it has told the player) -- the
825: -+# same kind of file as es_export's cached_game_ids.txt. The log says the same
826: -+# thing, but a log is not a signal anyone else can consume.
827:  +FLUSH_STAMP_FILE = CONFIG_DIR / "last-flush"
828:   LOGGER = logging.getLogger("raofflineproxy")
829:   
830:   
831: -@@ -486,6 +492,8 @@ def flush_pending_awards(storage: Storage, config_data: dict) -> FlushOutcome:
832: -         skipped_stale,
833: +@@ -488,6 +490,9 @@ def flush_pending_awards(storage: Storage, config_data: dict) -> FlushOutcome:
834:           pending_remaining,
835:       )
836: + 
837:  +    if flushed:
838:  +        write_flush_stamp(flushed)
839: - 
840: ++
841:       return FlushOutcome(
842:           flushed=flushed,
843: -@@ -496,6 +504,18 @@ def flush_pending_awards(storage: Storage, config_data: dict) -> FlushOutcome:
844: +         total=len(pending),
845: +@@ -497,6 +502,18 @@ def flush_pending_awards(storage: Storage, config_data: dict) -> FlushOutcome:
846:       )
847:   
848:   
849: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch
850: index 1a7471ea63..d679e4855b 100644
851: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch
852: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/004-no-cap-on-cached-games.patch
853: @@ -1,27 +1,77 @@
854: -The client caps manual caching at 100 games ("to keep bulk caching from
855: -generating too many RetroAchievements requests at once", docs/caching-games.md)
856: -and derives the smart-cache limit from the same constant. On ROCKNIX the scan
857: -is the way every game on the console comes to earn offline (fork #179,
858: -D-RA-010), and the maintainer's call is that every game does (fork #184 note 6,
859: -D-RA-014): "Why would there be a limit on how many games I can have stored for
860: -offline play? I would want every game available for offline play to be able to
861: -be played offline with the ability to unlock the achievements." The cap goes;
862: -the request throttle (network.py: 0.3 s between requests, a cooldown per batch,
863: -backoff on 429) stays, so a full-library scan is as polite as the capped one,
864: -only longer.
865: +rom_browser: allow an OS-managed deliberate whole-library scan
866:  
867: +Rasteratops' explicit preparation scans must retain more than100 games in
868: +one run (D-RA-014, #361). Add an opt-in budgeted=False argument to the
869: +single-ROM/drain entrypoints. Existing upstream callers keep the100-game
870: +window and batch bound. Deliberate calls retain the queue locks, pacing,
871: +429 stop and persisted pause; each cached game is still charged. They do
872: +not treat queued success as readiness: the integrating helper checks queued.
873:  
874: +The original patch004 raised a removed total-library cap. This replacement
875: +preserves that workflow through current upstream's queue API instead.
876: +
877: +diff --git a/linux/raofflineproxy/rom_browser.py b/linux/raofflineproxy/rom_browser.py
878: +index 97ab179..5fd43cc 100644
879:  --- a/linux/raofflineproxy/rom_browser.py
880:  +++ b/linux/raofflineproxy/rom_browser.py
881: -@@ -46,7 +46,10 @@ SUPPORTED_ARCHIVE_EXTENSIONS = {".zip", ".7z"}
882: - # which bundles a 7z reader (third_party/lzma-sdk), so it never reaches zipfile.
883: - ZIP_READABLE_ARCHIVE_EXTENSIONS = {".zip"}
884: - EXCLUDED_BROWSER_DIR_NAMES = {"Imgs"}
885: --MAX_CACHED_GAMES = 100
886: -+# ROCKNIX: no cap on how many games the scan may cache (fork #184, D-RA-014);
887: -+# upstream's 100 was a courtesy to the server, which the request throttle in
888: -+# network.py keeps. Large enough that no library reaches it.
889: -+MAX_CACHED_GAMES = 1000000
890: - MAX_SCAN_ENTRIES = 5000
891: - MAX_SCAN_DEPTH = 12
892: - # RetroAchievements adds hashes over time, so a "no match" is only cached long enough to
893: +@@ -513,9 +513,12 @@ def fetch_game_id(
894: +     return int(game_id)
895: + 
896: + 
897: +-def add_rom_to_cache(path: Path, storage: Storage, config_data: dict) -> AddRomResult:
898: ++def add_rom_to_cache(
899: ++    path: Path, storage: Storage, config_data: dict, *, budgeted: bool = True
900: ++) -> AddRomResult:
901: +     """Caches one ROM right away if the caching budget allows it, otherwise queues it for the
902: +-    proxy service."""
903: ++    proxy service. An OS-managed deliberate scan may set budgeted=False to
904: ++    prepare its whole library; locking, request pacing and server pauses remain."""
905: +     user_agent = self_user_agent()
906: +     credentials = resolve_credentials(storage, config_data, user_agent)
907: +     if credentials is None:
908: +@@ -550,6 +553,7 @@ def add_rom_to_cache(path: Path, storage: Storage, config_data: dict) -> AddRomR
909: +             credentials,
910: +             user_agent,
911: +             wait_for_lock=True,
912: ++            budgeted=budgeted,
913: +             keys=[rom.key],
914: +             on_outcome=lambda queued, outcome, game_id, message: outcomes.__setitem__(
915: +                 queued.key, (outcome, game_id, message)
916: +@@ -670,6 +674,7 @@ def drain_cache_queue(
917: +     keys: list[str] | None = None,
918: +     on_item=None,
919: +     on_outcome=None,
920: ++    budgeted: bool = True,
921: + ) -> DrainResult:
922: +     """The single place that sends RA requests for bulk caching: works through the queue oldest
923: +     first (or through keys, in order) within the caching budget. A window allows
924: +@@ -693,6 +698,7 @@ def drain_cache_queue(
925: +                 None if keys is None else list(dict.fromkeys(keys)),
926: +                 on_item,
927: +                 on_outcome,
928: ++                budgeted,
929: +             )
930: + 
931: + 
932: +@@ -705,6 +711,7 @@ def _drain_locked(
933: +     pending_keys: list[str] | None,
934: +     on_item,
935: +     on_outcome,
936: ++    budgeted: bool = True,
937: + ) -> DrainResult:
938: +     cached = 0
939: +     no_match = 0
940: +@@ -771,7 +778,12 @@ def _drain_locked(
941: +             report(rom, QueuedRomOutcome.ALREADY_CACHED, local.game_id, "")
942: +             continue
943: + 
944: +-        games_left = cache_budget.remaining(storage)
945: ++        # A deliberate OS scan can prepare more than one budget window,
946: ++        # but a persisted pause (including a 429 from another process) still
947: ++        # stops it. Every successful game is charged for the background worker.
948: ++        if not budgeted and cache_budget.load(storage).paused_until > current_millis():
949: ++            return result(DrainStop.BUDGET_EXHAUSTED, cache_budget.next_available_at(storage))
950: ++        games_left = cache_budget.remaining(storage) if budgeted else 1
951: +         if games_left == 0:
952: +             return result(DrainStop.BUDGET_EXHAUSTED, cache_budget.next_available_at(storage))
953: +         apply_scan_batch_cooldown(requested)
954: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/005-keep-the-refresh-thread-alive.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/005-keep-the-refresh-thread-alive.patch
955: index 801af115d2..6f36137e89 100644
956: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/005-keep-the-refresh-thread-alive.patch
957: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/005-keep-the-refresh-thread-alive.patch
958: @@ -22,36 +22,30 @@ Written for ROCKNIX (fork issue maxengel/rocknix#186, PL-25). Offered
959:  upstream as-is (ROCKNIX D-RA-016: whatever the fork changes in the proxy
960:  goes back).
961:  
962: +diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
963:  --- a/linux/raofflineproxy/proxy_service.py
964:  +++ b/linux/raofflineproxy/proxy_service.py
965: -@@ -46,6 +46,7 @@ from .network import (
966: +@@ -46,6 +46,7 @@
967:       response_content_type,
968:   )
969:   from .rom_cache import (
970:  +    CacheGameAuthError,
971: -     build_achievement_game_ids,
972:       build_unlocks_array,
973:       cache_session,
974: -@@ -80,6 +81,9 @@ FAKE_OFFLINE_SUCCESS_ACTIONS = {"ping", "postactivity"}
975: +     cache_unlocks,
976: +@@ -81,6 +82,7 @@
977:   REFRESH_PLAYED_WINDOW_DAYS = 7
978:   ONLINE_REFRESH_IDLE_DELAY_SECONDS = 5 * 60
979:   REFRESH_PLAYED_WINDOW_MS = REFRESH_PLAYED_WINDOW_DAYS * 24 * 60 * 60 * 1000
980: -+# Fetches that fail in a row before a refresh pass gives up (the link, the
981: -+# server); a refused sign-in ends a pass at once, without a request per game.
982:  +REFRESH_MAX_FAILURES_IN_A_ROW = 3
983: + CACHE_QUEUE_POLL_SECONDS = 60
984:   ALWAYS_TRY_UPSTREAM_ACTIONS = {"login", "login2"}
985:   # A 4xx RetroAchievements sends for a dorequest.php call it understood but
986: - # cannot satisfy -- 404 "Unknown game" for a hash with no set, 400 for a bad
987: -@@ -1054,35 +1058,50 @@ class PeriodicRefresh(threading.Thread):
988: +@@ -1054,37 +1056,47 @@
989:           self.stop_event.set()
990:   
991:       def run(self) -> None:
992: -+        # A pass that fails -- a request that raised, the store unreadable
993: -+        # for a moment -- costs that pass and nothing more: the thread lives
994: -+        # for the service's lifetime, and with it the eviction it carries.
995: -+        # Without this it dies on the first exception, silently, with
996: -+        # Restart=on-failure none the wiser, and the service runs on with no
997: -+        # refresh and no eviction until its next start.
998: ++        # A failed pass must not silently end the service's refresh thread.
999:           while not self.stop_event.wait(self.interval_seconds):
1000:  -            if not self.server.is_online():
1001:  -                continue
1002: @@ -63,22 +57,24 @@ goes back).
1003:  -            )
1004:  -            if credentials is None:
1005:  -                continue
1006: +-            if rate_limit.paused_until() is not None:
1007: +-                LOGGER.info("Periodic refresh skipped; RetroAchievements asked to slow down")
1008: +-                continue
1009:  -            if not self.wait_until_idle():
1010:  -                continue
1011: --            patch_entries = self.server.storage.get_all_cache_by_prefix(
1012: --                cache_keys.PREFIX_PATCH
1013: --            )
1014: +-            patch_keys = self.server.storage.cache_keys_by_prefix(cache_keys.PREFIX_PATCH)
1015:  -            recently_played = load_recently_played_game_ids(
1016:  -                self.server.storage, current_millis() - REFRESH_PLAYED_WINDOW_MS
1017:  -            )
1018: --            due_game_ids = due_refresh_game_ids(patch_entries, recently_played)
1019: +-            due_game_ids = due_refresh_game_ids(patch_keys, recently_played)
1020:  -            LOGGER.info(
1021:  -                "Periodic refresh: %d of %d cached game(s) played in the last %d day(s)",
1022:  -                len(due_game_ids),
1023: --                len(patch_entries),
1024: +-                len(patch_keys),
1025:  -                REFRESH_PLAYED_WINDOW_DAYS,
1026:  -            )
1027: --            self.refresh_games(due_game_ids, credentials, user_agent)
1028: +-            with rate_limit.background():
1029: +-                self.refresh_games(due_game_ids, credentials, user_agent)
1030:  -            before = current_millis() - (self.cache_ttl_seconds * 1000)
1031:  -            self.server.storage.evict_cache_older_than(before)
1032:  +            try:
1033: @@ -100,28 +96,30 @@ goes back).
1034:  +        )
1035:  +        if credentials is None:
1036:  +            return
1037: ++        if rate_limit.paused_until() is not None:
1038: ++            LOGGER.info("Periodic refresh skipped; RetroAchievements asked to slow down")
1039: ++            return
1040:  +        if not self.wait_until_idle():
1041:  +            return
1042: -+        patch_entries = self.server.storage.get_all_cache_by_prefix(
1043: -+            cache_keys.PREFIX_PATCH
1044: -+        )
1045: ++        patch_keys = self.server.storage.cache_keys_by_prefix(cache_keys.PREFIX_PATCH)
1046:  +        recently_played = load_recently_played_game_ids(
1047:  +            self.server.storage, current_millis() - REFRESH_PLAYED_WINDOW_MS
1048:  +        )
1049: -+        due_game_ids = due_refresh_game_ids(patch_entries, recently_played)
1050: ++        due_game_ids = due_refresh_game_ids(patch_keys, recently_played)
1051:  +        LOGGER.info(
1052:  +            "Periodic refresh: %d of %d cached game(s) played in the last %d day(s)",
1053:  +            len(due_game_ids),
1054: -+            len(patch_entries),
1055: ++            len(patch_keys),
1056:  +            REFRESH_PLAYED_WINDOW_DAYS,
1057:  +        )
1058: -+        self.refresh_games(due_game_ids, credentials, user_agent)
1059: ++        with rate_limit.background():
1060: ++            self.refresh_games(due_game_ids, credentials, user_agent)
1061:  +        before = current_millis() - (self.cache_ttl_seconds * 1000)
1062:  +        self.server.storage.evict_cache_older_than(before)
1063:   
1064:       def wait_until_idle(self) -> bool:
1065:           idle_delay = self.server.activity.idle_delay_seconds()
1066: -@@ -1095,26 +1114,42 @@ class PeriodicRefresh(threading.Thread):
1067: +@@ -1097,6 +1109,7 @@
1068:   
1069:       def refresh_games(self, game_ids: list[int], credentials: dict, user_agent: str) -> int:
1070:           refreshed = 0
1071: @@ -129,44 +127,16 @@ goes back).
1072:           for game_id in game_ids:
1073:               if self.server.activity.idle_delay_seconds() > 0:
1074:                   LOGGER.info("Periodic refresh paused; proxy became active")
1075: -                 break
1076: --            refresh_game_patch(
1077: --                game_id,
1078: --                credentials,
1079: --                user_agent,
1080: --                self.server.storage,
1081: --                self.server.config_data,
1082: --                cache_images=image_caching_enabled(self.server.config_data),
1083: --            )
1084: --            cache_unlocks(
1085: --                game_id,
1086: --                credentials,
1087: --                user_agent,
1088: --                self.server.config_data,
1089: --                self.server.storage,
1090: --            )
1091: --            cache_session(game_id, credentials, self.server.storage)
1092: -+            try:
1093: -+                refresh_game_patch(
1094: -+                    game_id,
1095: -+                    credentials,
1096: -+                    user_agent,
1097: -+                    self.server.storage,
1098: -+                    self.server.config_data,
1099: -+                    cache_images=image_caching_enabled(self.server.config_data),
1100: -+                )
1101: -+                cache_unlocks(
1102: -+                    game_id,
1103: -+                    credentials,
1104: -+                    user_agent,
1105: -+                    self.server.config_data,
1106: -+                    self.server.storage,
1107: -+                )
1108: -+                cache_session(game_id, credentials, self.server.storage)
1109: +@@ -1118,9 +1131,24 @@
1110: +                     self.server.storage,
1111: +                 )
1112: +                 cache_session(game_id, credentials, self.server.storage)
1113: +-                refreshed += 1
1114:  +            except CacheGameAuthError as exc:
1115:  +                LOGGER.warning("Periodic refresh: sign-in refused (%s); ending the pass", exc)
1116:  +                break
1117: -+            except Exception as exc:
1118: +             except Exception as exc:
1119: +-                LOGGER.warning("Periodic refresh failed for game %s: %s", game_id, exc)
1120:  +                failures_in_a_row += 1
1121:  +                LOGGER.warning("Periodic refresh: game %s not refreshed: %s", game_id, exc)
1122:  +                if failures_in_a_row >= REFRESH_MAX_FAILURES_IN_A_ROW:
1123: @@ -175,8 +145,12 @@ goes back).
1124:  +                        failures_in_a_row,
1125:  +                    )
1126:  +                    break
1127: ++                if rate_limit.paused_until() is not None:
1128: ++                    LOGGER.warning("Periodic refresh stopped; RetroAchievements answered 429")
1129: ++                    break
1130:  +                continue
1131:  +            failures_in_a_row = 0
1132: -             refreshed += 1
1133: -         return refreshed
1134: - 
1135: ++            refreshed += 1
1136: +             if rate_limit.paused_until() is not None:
1137: +                 LOGGER.warning("Periodic refresh stopped; RetroAchievements answered 429")
1138: +                 break
1139: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/007-cached-sign-in-of-the-configured-account.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/007-cached-sign-in-of-the-configured-account.patch
1140: index 96f240c01f..614fc5f61a 100644
1141: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/007-cached-sign-in-of-the-configured-account.patch
1142: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/007-cached-sign-in-of-the-configured-account.patch
1143: @@ -18,6 +18,8 @@ unchanged: a token wins, then the cache, then a fresh login2.
1144:  Written for ROCKNIX (fork issue maxengel/rocknix#186, PL-23). Offered
1145:  upstream as-is (ROCKNIX D-RA-016).
1146:  
1147: +diff --git a/linux/raofflineproxy/auth.py b/linux/raofflineproxy/auth.py
1148: +index 2f1de88..aaa78d7 100644
1149:  --- a/linux/raofflineproxy/auth.py
1150:  +++ b/linux/raofflineproxy/auth.py
1151:  @@ -47,10 +47,6 @@ def resolve_credentials(
1152: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/008-log-upload-opt-in.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/008-log-upload-opt-in.patch
1153: index c4c2790df2..05595f44c2 100644
1154: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/008-log-upload-opt-in.patch
1155: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/008-log-upload-opt-in.patch
1156: @@ -25,22 +25,24 @@ Written for ROCKNIX (fork issue maxengel/rocknix#186, PL-12). Offered
1157:  upstream as-is (ROCKNIX D-RA-016), the default being the project's to
1158:  decide.
1159:  
1160: +diff --git a/linux/raofflineproxy/config.py b/linux/raofflineproxy/config.py
1161: +index 12d2dfb..5cba299 100644
1162:  --- a/linux/raofflineproxy/config.py
1163:  +++ b/linux/raofflineproxy/config.py
1164: -@@ -332,6 +332,13 @@ def load_config() -> dict:
1165: +@@ -332,6 +332,11 @@ def load_config() -> dict:
1166:       return data
1167:   
1168:   
1169:  +def log_upload_enabled(config_data: dict | None = None) -> bool:
1170: -+    """Whether the service may upload a log bundle on its own. Off unless
1171: -+    config.json says "upload_logs": true -- the JSON true, nothing else; the
1172: -+    menu's manual upload, a choice made on screen, is not gated by this."""
1173: ++    """Automatic log upload requires an explicit JSON true, never truthiness."""
1174:  +    return (config_data or {}).get("upload_logs") is True
1175:  +
1176:  +
1177:   def image_caching_enabled(config_data: dict | None = None) -> bool:
1178:       config_data = config_data or {}
1179:       configured = config_data.get("cache_images")
1180: +diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
1181: +index a0199ad..9c0908d 100644
1182:  --- a/linux/raofflineproxy/proxy_service.py
1183:  +++ b/linux/raofflineproxy/proxy_service.py
1184:  @@ -22,6 +22,7 @@ from .config import (
1185: @@ -51,7 +53,7 @@ decide.
1186:       proxy_host,
1187:       proxy_port,
1188:       upstream_host,
1189: -@@ -1163,7 +1164,7 @@ def due_refresh_game_ids(patch_entries: list[dict], recently_played: set[int]) -
1190: +@@ -1271,7 +1272,7 @@ def due_refresh_game_ids(patch_entries: list[dict], recently_played: set[int]) -
1191:       return due
1192:   
1193:   
1194: @@ -60,22 +62,17 @@ decide.
1195:       # The menu only ever attempts this once (on first open after the incident) and shows
1196:       # the user the outcome regardless of success, so it doesn't nag them again — if that
1197:       # one attempt happened while offline, the report would otherwise never reach us. The
1198: -@@ -1171,6 +1172,14 @@ def retry_storage_corruption_report() -> None:
1199: +@@ -1279,6 +1280,9 @@ def retry_storage_corruption_report() -> None:
1200:       incident = storage_corruption.load_incident()
1201:       if incident is None or incident.get("reported"):
1202:           return
1203: -+    # Only where the configuration opts in. The report is a log bundle sent
1204: -+    # to a third-party endpoint, from a service, without anyone's yes, at a
1205: -+    # moment nobody is watching -- after a data file was found corrupt, on a
1206: -+    # handheld a power cut is an ordinary evening for. An OS that wants the
1207: -+    # reports sets "upload_logs": true in config.json.
1208:  +    if not log_upload_enabled(config_data):
1209:  +        LOGGER.info("Storage corruption report not sent: upload_logs is off")
1210:  +        return
1211:       try:
1212:           upload_id = log_uploader.report_storage_corruption(incident)
1213:       except Exception as exc:
1214: -@@ -1210,7 +1219,7 @@ def run_proxy_service(
1215: +@@ -1321,7 +1325,7 @@ def run_proxy_service(
1216:           save_online_state(initial_online)
1217:           if initial_online:
1218:               server.flush_pending_awards()
1219: @@ -83,4 +80,65 @@ decide.
1220:  +            retry_storage_corruption_report(config_data)
1221:           connectivity_monitor.start()
1222:           periodic_refresh.start()
1223: +         cache_queue_worker.start()
1224: +
1225: +diff --git a/linux/tests/test_linux_storage_corruption_retry.py b/linux/tests/test_linux_storage_corruption_retry.py
1226: +--- a/linux/tests/test_linux_storage_corruption_retry.py
1227: ++++ b/linux/tests/test_linux_storage_corruption_retry.py
1228: +@@ -5,12 +5,28 @@
1229: + 
1230: + 
1231: + class RetryStorageCorruptionReportTests(unittest.TestCase):
1232: ++    def test_automatic_upload_requires_explicit_true(self) -> None:
1233: ++        incident = {"reported": False, "upload_id": None}
1234: ++        for config in ({}, {"upload_logs": None}, {"upload_logs": False},
1235: ++                       {"upload_logs": 0}, {"upload_logs": 1},
1236: ++                       {"upload_logs": "false"}, {"upload_logs": "true"},
1237: ++                       {"upload_logs": "yes"}, None):
1238: ++            with (
1239: ++                self.subTest(config=config),
1240: ++                mock.patch.object(proxy_service.storage_corruption, "load_incident", return_value=incident),
1241: ++                mock.patch.object(proxy_service.log_uploader, "report_storage_corruption") as report,
1242: ++                mock.patch.object(proxy_service.storage_corruption, "mark_reported") as mark,
1243: ++            ):
1244: ++                proxy_service.retry_storage_corruption_report(config)
1245: ++                report.assert_not_called()
1246: ++                mark.assert_not_called()
1247: ++
1248: +     def test_noop_when_no_incident(self) -> None:
1249: +         with (
1250: +             mock.patch.object(proxy_service.storage_corruption, "load_incident", return_value=None),
1251: +             mock.patch.object(proxy_service.log_uploader, "report_storage_corruption") as report,
1252: +         ):
1253: +-            proxy_service.retry_storage_corruption_report()
1254: ++            proxy_service.retry_storage_corruption_report({"upload_logs": True})
1255: + 
1256: +         report.assert_not_called()
1257: + 
1258: +@@ -20,7 +36,7 @@
1259: +             mock.patch.object(proxy_service.storage_corruption, "load_incident", return_value=incident),
1260: +             mock.patch.object(proxy_service.log_uploader, "report_storage_corruption") as report,
1261: +         ):
1262: +-            proxy_service.retry_storage_corruption_report()
1263: ++            proxy_service.retry_storage_corruption_report({"upload_logs": True})
1264: + 
1265: +         report.assert_not_called()
1266: + 
1267: +@@ -33,7 +49,7 @@
1268: +             ),
1269: +             mock.patch.object(proxy_service.storage_corruption, "mark_reported") as mark_reported,
1270: +         ):
1271: +-            proxy_service.retry_storage_corruption_report()
1272: ++            proxy_service.retry_storage_corruption_report({"upload_logs": True})
1273: + 
1274: +         mark_reported.assert_called_once_with("abc123")
1275: + 
1276: +@@ -48,7 +64,7 @@
1277: +             ),
1278: +             mock.patch.object(proxy_service.storage_corruption, "mark_reported") as mark_reported,
1279: +         ):
1280: +-            proxy_service.retry_storage_corruption_report()
1281: ++            proxy_service.retry_storage_corruption_report({"upload_logs": True})
1282: + 
1283: +         mark_reported.assert_not_called()
1284:   
1285: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/009-unique-image-temp-names.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/009-unique-image-temp-names.patch
1286: index d0eb0b0482..861dc3e65a 100644
1287: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/009-unique-image-temp-names.patch
1288: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/009-unique-image-temp-names.patch
1289: @@ -17,36 +17,18 @@ is left to the project.
1290:  Written for ROCKNIX (fork issue maxengel/rocknix#186, PL-33). Offered
1291:  upstream as-is (ROCKNIX D-RA-016).
1292:  
1293: +diff --git a/linux/raofflineproxy/image_cache.py b/linux/raofflineproxy/image_cache.py
1294: +index baef764..64384c9 100644
1295:  --- a/linux/raofflineproxy/image_cache.py
1296:  +++ b/linux/raofflineproxy/image_cache.py
1297: -@@ -2,7 +2,9 @@ from __future__ import annotations
1298: - 
1299: - import json
1300: - import logging
1301: -+import os
1302: - import shutil
1303: -+import threading
1304: - import urllib.request
1305: - from concurrent.futures import ThreadPoolExecutor
1306: - from pathlib import Path
1307: -@@ -165,11 +167,20 @@ def download_static_image(
1308: -                 headers={"User-Agent": user_agent, "Accept-Encoding": "identity"},
1309: -                 method="GET",
1310: -             )
1311: +@@ -206,10 +206,10 @@ def download_static_image(
1312: +         target = resolve_cached_static_asset(clean_path) or sharded_static_path(clean_path)
1313: +         if not target.exists():
1314: +             target.parent.mkdir(parents=True, exist_ok=True)
1315:  -            tmp = target.with_suffix(target.suffix + ".tmp")
1316: -+            # A name of this process's and this thread's: two workers
1317: -+            # fetching one asset -- the pool's four threads, or the service's
1318: -+            # pool and a bulk cache's in another process -- used to share
1319: -+            # <target>.tmp, so one's rename moved the other's half-written
1320: -+            # bytes into place and one's cleanup unlinked the other's file.
1321: -+            # os.replace, so the second to finish overwrites the first's
1322: -+            # identical bytes rather than failing on an existing target.
1323: -+            tmp = target.with_name(
1324: -+                f"{target.name}.{os.getpid()}.{threading.get_ident()}.tmp"
1325: -+            )
1326: ++            tmp = target.with_name(f"{target.name}.{os.getpid()}.{threading.get_ident()}.tmp")
1327:               try:
1328: -                 with urllib.request.urlopen(request, timeout=10) as response:
1329: -                     tmp.write_bytes(response.read())
1330: +                 tmp.write_bytes(_fetch_image(url, user_agent))
1331:  -                tmp.rename(target)
1332:  +                os.replace(tmp, target)
1333:                   tmp = None
1334: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/010-store-only-header.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/010-store-only-header.patch
1335: index 8ae6f48b51..fd8a6e9a88 100644
1336: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/010-store-only-header.patch
1337: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/010-store-only-header.patch
1338: @@ -14,6 +14,9 @@ A request carrying `X-RA-Store-Only: 1` is now served by handle_offline_request
1339:  whatever is_online() says: the store's copy, or the store's "not cached", at
1340:  once. Nothing else changes; a client that does not send the header is
1341:  served as before. Awards never take this path (they are handled first).
1342: +
1343: +diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
1344: +index 9c0908d..259f21e 100644
1345:  --- a/linux/raofflineproxy/proxy_service.py
1346:  +++ b/linux/raofflineproxy/proxy_service.py
1347:  @@ -412,6 +412,17 @@ class ProxyRuntimeServer(ThreadingTCPServer):
1348: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/011-offline-login-header.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/011-offline-login-header.patch
1349: index 4d95654dfe..1b3210d086 100644
1350: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/011-offline-login-header.patch
1351: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/011-offline-login-header.patch
1352: @@ -24,6 +24,8 @@ Written for ROCKNIX (fork issue maxengel/rocknix#194). Offered upstream
1353:  as-is (ROCKNIX D-RA-002, D-RA-016: whatever the fork changes in the proxy
1354:  goes back); the headers are additive and cost a client nothing.
1355:  
1356: +diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
1357: +index 259f21e..f19d977 100644
1358:  --- a/linux/raofflineproxy/proxy_service.py
1359:  +++ b/linux/raofflineproxy/proxy_service.py
1360:  @@ -92,6 +92,14 @@ ALWAYS_TRY_UPSTREAM_ACTIONS = {"login", "login2"}
1361: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/012-offline-image-miss.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/012-offline-image-miss.patch
1362: index 5751cd15ee..e8a660958d 100644
1363: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/012-offline-image-miss.patch
1364: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/012-offline-image-miss.patch
1365: @@ -47,6 +47,8 @@ Written for ROCKNIX (fork issue maxengel/rocknix#199). Offered upstream
1366:  as-is (ROCKNIX D-RA-002, D-RA-016: whatever the fork changes in the proxy
1367:  goes back).
1368:  
1369: +diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
1370: +index f19d977..c8e9724 100644
1371:  --- a/linux/raofflineproxy/proxy_service.py
1372:  +++ b/linux/raofflineproxy/proxy_service.py
1373:  @@ -100,6 +100,11 @@ AUTH_FAILURE_STATUSES = {401, 403}
1374: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch
1375: index 7b36ae8884..b19a1a0b21 100644
1376: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch
1377: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/013-validate-a-cached-image-before-publishing-it.patch
1378: @@ -33,41 +33,17 @@ second pass fetches the asset whole.
1379:  Written for ROCKNIX (fork issue maxengel/rocknix#213). Offered upstream
1380:  as-is.
1381:  
1382: +diff --git a/linux/raofflineproxy/image_cache.py b/linux/raofflineproxy/image_cache.py
1383: +index 64384c9..6378a23 100644
1384:  --- a/linux/raofflineproxy/image_cache.py
1385:  +++ b/linux/raofflineproxy/image_cache.py
1386: -@@ -6,6 +6,7 @@ import os
1387: - import shutil
1388: - import threading
1389: - import urllib.request
1390: -+import zlib
1391: - from concurrent.futures import ThreadPoolExecutor
1392: - from pathlib import Path
1393: - 
1394: -@@ -179,7 +180,30 @@ def download_static_image(
1395: -             )
1396: +@@ -208,7 +208,12 @@ def download_static_image(
1397: +             target.parent.mkdir(parents=True, exist_ok=True)
1398: +             tmp = target.with_name(f"{target.name}.{os.getpid()}.{threading.get_ident()}.tmp")
1399:               try:
1400: -                 with urllib.request.urlopen(request, timeout=10) as response:
1401: --                    tmp.write_bytes(response.read())
1402: -+                    declared = response.headers.get("Content-Length")
1403: -+                    payload = response.read()
1404: -+                # An image is published only when it is whole and is an
1405: -+                # image. response.read() returns what arrived, so a
1406: -+                # connection that drops mid-body used to be written under
1407: -+                # the asset's real name and every later existence check --
1408: -+                # this function's own target.exists(), the proxy's
1409: -+                # resolve_cached_static_asset, ROCKNIX's image pass -- called
1410: -+                # it cached for good. Two tests, before the rename that makes
1411: -+                # it the cache's answer: the length the server declared if it
1412: -+                # declared one, and for a .png the whole-PNG test below
1413: -+                # (png_problem). A body that fails either is dropped and the
1414: -+                # asset stays missing, which is a state the callers already
1415: -+                # handle (a miss is re-requested, or answered 404 at once
1416: -+                # offline). Written for ROCKNIX (fork maxengel/rocknix#213).
1417: -+                if declared is not None and declared.isdigit() and len(payload) != int(declared):
1418: -+                    raise ValueError(
1419: -+                        f"short read: {len(payload)} of {declared} bytes"
1420: -+                    )
1421: -+                if image_path.lower().endswith(".png"):
1422: +-                tmp.write_bytes(_fetch_image(url, user_agent))
1423: ++                payload = _fetch_image(url, user_agent)
1424: ++                if clean_path.lower().endswith(".png"):
1425:  +                    problem = png_problem(payload)
1426:  +                    if problem is not None:
1427:  +                        raise ValueError(problem)
1428: @@ -75,7 +51,36 @@ as-is.
1429:                   os.replace(tmp, target)
1430:                   tmp = None
1431:               finally:
1432: -@@ -250,3 +274,42 @@ def delete_cached_images_for_game(game_i
1433: +@@ -252,7 +257,11 @@ def _fetch_image(url: str, user_agent: str) -> bytes:
1434: +             _drop_thread_connection(parts.netloc)
1435: +         if response.status != _HTTP_OK:
1436: +             return _fetch_with_urllib(url, user_agent)
1437: +-        return body
1438: ++        try:
1439: ++            return _checked_image_body(response, body)
1440: ++        except ValueError:
1441: ++            _drop_thread_connection(parts.netloc)
1442: ++            raise
1443: +     raise OSError(f"could not fetch {url}")
1444: + 
1445: + 
1446: +@@ -263,7 +272,14 @@ def _fetch_with_urllib(url: str, user_agent: str) -> bytes:
1447: +         method="GET",
1448: +     )
1449: +     with urllib.request.urlopen(request, timeout=10, context=configured_ssl_context()) as response:
1450: +-        return response.read()
1451: ++        return _checked_image_body(response, response.read())
1452: ++
1453: ++
1454: ++def _checked_image_body(response, payload: bytes) -> bytes:
1455: ++    declared = response.getheader("Content-Length")
1456: ++    if declared is not None and declared.isdigit() and len(payload) != int(declared):
1457: ++        raise ValueError(f"short read: {len(payload)} of {declared} bytes")
1458: ++    return payload
1459: + 
1460: + 
1461: + def _thread_connection(host: str) -> http.client.HTTPSConnection:
1462: +@@ -380,3 +396,43 @@ def delete_cached_images_for_game(game_id: int) -> None:
1463:   def clear_all_cached_images() -> None:
1464:       if IMAGE_CACHE_DIR.exists():
1465:           shutil.rmtree(IMAGE_CACHE_DIR, ignore_errors=True)
1466: @@ -118,3 +123,29 @@ as-is.
1467:  +    except zlib.error as exc:
1468:  +        return f"PNG image data does not inflate: {exc}"
1469:  +    return None
1470: ++
1471: +diff --git a/linux/tests/test_linux_image_cache_shutdown.py b/linux/tests/test_linux_image_cache_shutdown.py
1472: +index ecd5dfe..91171e4 100644
1473: +--- a/linux/tests/test_linux_image_cache_shutdown.py
1474: ++++ b/linux/tests/test_linux_image_cache_shutdown.py
1475: +@@ -64,6 +64,9 @@ class ImageConnectionReuseTests(unittest.TestCase):
1476: +                 self.status = status
1477: +                 self.will_close = False
1478: + 
1479: ++            def getheader(self, _name):
1480: ++                return "3"
1481: ++
1482: +             def read(self) -> bytes:
1483: +                 return b"png"
1484: + 
1485: +@@ -173,7 +176,9 @@ class ShardedStaticImagesTests(unittest.TestCase):
1486: +     def test_a_download_lands_in_its_shard_folder(self) -> None:
1487: +         from unittest import mock
1488: + 
1489: +-        with mock.patch.object(self.image_cache, "_fetch_image", return_value=b"png"):
1490: ++        # This test isolates sharded placement; publication validity has its own controls.
1491: ++        with mock.patch.object(self.image_cache, "png_problem", return_value=None), \
1492: ++                mock.patch.object(self.image_cache, "_fetch_image", return_value=b"png"):
1493: +             self.image_cache.download_static_image("https://media/Badge/123456.png", "/Badge/123456.png", "ua")
1494: + 
1495: +         expected = self.image_cache.sharded_static_path("Badge/123456.png")
1496: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/014-reuse-one-connection-per-thread-for-images.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/014-reuse-one-connection-per-thread-for-images.patch
1497: deleted file mode 100644
1498: index 0bc605d97d..0000000000
1499: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/014-reuse-one-connection-per-thread-for-images.patch
1500: +++ /dev/null
1501: @@ -1,169 +0,0 @@
1502: -image_cache: reuse one connection per thread instead of one per image
1503: -
1504: -Every static asset was fetched with its own urllib.request.urlopen, so a
1505: -badge whose median size is 5.6 KB paid a TCP connect and a TLS handshake of
1506: -its own. Measured on a ROCKNIX guest against media.retroachievements.org:
1507: -161 ms per image on a fresh connection against 28 ms over one already open,
1508: -and 14.9 images/s through the real caching pass against 83.6/s with a
1509: -connection per worker. For a first-time fill of a 494-game library -- 30,546
1510: -images -- that is the difference between about half an hour of fetching and
1511: -about six minutes, nearly all of it handshake.
1512: -
1513: -It is also the politer shape, which is why it is worth doing rather than
1514: -raising concurrency: the same request count and the same bytes, a fraction
1515: -of the connection setup. The pool stays at the size it was.
1516: -
1517: -A pooled connection can be closed by the server between uses and nothing
1518: -says so until the next write fails, so every fetch retries once on a fresh
1519: -connection. Response bodies are always read in full -- an unread body
1520: -poisons the connection for the next caller -- and a non-2xx raises
1521: -urllib.error.HTTPError exactly as urlopen did, so callers that treat any
1522: -failure as "not cached" are unchanged. Redirects are followed up to three
1523: -deep, cross-host included.
1524: -
1525: -The length and PNG checks added by 013 are untouched: the declared length
1526: -now comes from the pooled response's headers, and nothing is published until
1527: -it has passed both.
1528: -
1529: -Written for ROCKNIX (fork maxengel/rocknix#217).
1530: -
1531: ---- a/linux/raofflineproxy/image_cache.py
1532: -+++ b/linux/raofflineproxy/image_cache.py
1533: -@@ -1,10 +1,13 @@
1534: - from __future__ import annotations
1535: - 
1536: -+import http.client
1537: - import json
1538: - import logging
1539: - import os
1540: - import shutil
1541: - import threading
1542: -+import urllib.error
1543: -+import urllib.parse
1544: - import urllib.request
1545: - import zlib
1546: - from concurrent.futures import ThreadPoolExecutor
1547: -@@ -144,6 +147,95 @@ def rewrite_image_urls(
1548: -     return json.dumps(data, separators=(",", ":")), downloads
1549: - 
1550: - 
1551: -+# One connection per thread per host, reused across images.
1552: -+#
1553: -+# Every badge was fetched with its own urllib.request.urlopen, which means a
1554: -+# TCP connect and a TLS handshake for a file whose median size is 5.6 KB. On a
1555: -+# guest that measured 161 ms per image against 28 ms over a connection already
1556: -+# open -- so a first-time fill of a 494-game library spent over half an hour
1557: -+# almost entirely in handshakes (ROCKNIX fork maxengel/rocknix#217).
1558: -+#
1559: -+# Reuse is also the politer shape: the same bytes and the same request count,
1560: -+# a fraction of the setup, so it is not a licence to raise concurrency and the
1561: -+# pool size is deliberately unchanged.
1562: -+#
1563: -+# A pooled connection can be closed by the server between uses and there is no
1564: -+# way to tell until the write fails, so every fetch retries once on a fresh
1565: -+# connection before giving up. Bodies are always read in full, because a
1566: -+# response left unread poisons the connection for the next caller.
1567: -+_pool = threading.local()
1568: -+
1569: -+
1570: -+def _pooled_connection(scheme: str, host: str, timeout: float, fresh: bool = False):
1571: -+    connections = getattr(_pool, "connections", None)
1572: -+    if connections is None:
1573: -+        connections = _pool.connections = {}
1574: -+    key = (scheme, host)
1575: -+    existing = connections.get(key)
1576: -+    if fresh and existing is not None:
1577: -+        try:
1578: -+            existing.close()
1579: -+        except Exception:
1580: -+            pass
1581: -+        existing = None
1582: -+        connections.pop(key, None)
1583: -+    if existing is None:
1584: -+        if scheme == "https":
1585: -+            existing = http.client.HTTPSConnection(host, timeout=timeout)
1586: -+        else:
1587: -+            existing = http.client.HTTPConnection(host, timeout=timeout)
1588: -+        connections[key] = existing
1589: -+    return existing
1590: -+
1591: -+
1592: -+def _drop_connection(scheme: str, host: str) -> None:
1593: -+    connections = getattr(_pool, "connections", None) or {}
1594: -+    connection = connections.pop((scheme, host), None)
1595: -+    if connection is not None:
1596: -+        try:
1597: -+            connection.close()
1598: -+        except Exception:
1599: -+            pass
1600: -+
1601: -+
1602: -+def fetch_static_asset(url: str, headers: dict, timeout: float = 10.0, _redirects: int = 3):
1603: -+    """GET url over a reused connection. Returns (response headers, body).
1604: -+
1605: -+    Raises on a non-2xx status, as urlopen did, so callers that already treat
1606: -+    any failure as "not cached" keep their behaviour.
1607: -+    """
1608: -+    parsed = urllib.parse.urlsplit(url)
1609: -+    scheme = parsed.scheme or "https"
1610: -+    host = parsed.netloc
1611: -+    target = parsed.path or "/"
1612: -+    if parsed.query:
1613: -+        target = f"{target}?{parsed.query}"
1614: -+
1615: -+    last_error: Exception | None = None
1616: -+    for attempt in (False, True):
1617: -+        connection = _pooled_connection(scheme, host, timeout, fresh=attempt)
1618: -+        try:
1619: -+            connection.request("GET", target, headers=headers)
1620: -+            response = connection.getresponse()
1621: -+            body = response.read()  # always, or the connection cannot be reused
1622: -+            status = response.status
1623: -+            if status in (301, 302, 303, 307, 308) and _redirects > 0:
1624: -+                location = response.headers.get("Location")
1625: -+                if location:
1626: -+                    return fetch_static_asset(
1627: -+                        urllib.parse.urljoin(url, location), headers, timeout, _redirects - 1
1628: -+                    )
1629: -+            if status < 200 or status >= 300:
1630: -+                raise urllib.error.HTTPError(url, status, response.reason, response.headers, None)
1631: -+            return response.headers, body
1632: -+        except urllib.error.HTTPError:
1633: -+            raise
1634: -+        except Exception as exc:  # a closed or broken connection: retry once
1635: -+            last_error = exc
1636: -+            _drop_connection(scheme, host)
1637: -+    raise last_error if last_error else RuntimeError("fetch failed")
1638: -+
1639: -+
1640: - def download_static_image(
1641: -     url: str,
1642: -     image_path: str,
1643: -@@ -163,11 +255,6 @@ def download_static_image(
1644: -         target = STATIC_DIR / clean_path
1645: -         if not target.exists():
1646: -             target.parent.mkdir(parents=True, exist_ok=True)
1647: --            request = urllib.request.Request(
1648: --                url,
1649: --                headers={"User-Agent": user_agent, "Accept-Encoding": "identity"},
1650: --                method="GET",
1651: --            )
1652: -             # A name of this process's and this thread's: two workers
1653: -             # fetching one asset -- the pool's four threads, or the service's
1654: -             # pool and a bulk cache's in another process -- used to share
1655: -@@ -179,9 +266,12 @@ def download_static_image(
1656: -                 f"{target.name}.{os.getpid()}.{threading.get_ident()}.tmp"
1657: -             )
1658: -             try:
1659: --                with urllib.request.urlopen(request, timeout=10) as response:
1660: --                    declared = response.headers.get("Content-Length")
1661: --                    payload = response.read()
1662: -+                headers, payload = fetch_static_asset(
1663: -+                    url,
1664: -+                    {"User-Agent": user_agent, "Accept-Encoding": "identity"},
1665: -+                    timeout=10,
1666: -+                )
1667: -+                declared = headers.get("Content-Length")
1668: -                 # An image is published only when it is whole and is an
1669: -                 # image. response.read() returns what arrived, so a
1670: -                 # connection that drops mid-body used to be written under
1671: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/015-bounded-name-lookup.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/015-bounded-name-lookup.patch
1672: index 93c2194bbb..c8a19cfcb3 100644
1673: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/015-bounded-name-lookup.patch
1674: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/015-bounded-name-lookup.patch
1675: @@ -37,7 +37,9 @@ seconds.
1676:  Written for ROCKNIX (fork issue maxengel/rocknix#242). Offered upstream
1677:  as-is (ROCKNIX D-RA-002, D-RA-016).
1678:  
1679: -diff -ruN a/linux/raofflineproxy/network.py b/linux/raofflineproxy/network.py
1680: +
1681: +diff --git a/linux/raofflineproxy/network.py b/linux/raofflineproxy/network.py
1682: +index e4681a5..cecdb1f 100644
1683:  --- a/linux/raofflineproxy/network.py
1684:  +++ b/linux/raofflineproxy/network.py
1685:  @@ -3,6 +3,7 @@ from __future__ import annotations
1686: @@ -48,7 +50,7 @@ diff -ruN a/linux/raofflineproxy/network.py b/linux/raofflineproxy/network.py
1687:   import ssl
1688:   import threading
1689:   import time
1690: -@@ -20,6 +21,16 @@ REDACTED_QUERY_KEYS = {"p", "t", "token", "password"}
1691: +@@ -21,6 +22,16 @@ REDACTED_QUERY_KEYS = {"p", "t", "token", "password"}
1692:   REACHABILITY_INTERVAL_SECONDS = 30.0
1693:   PROBE_ATTEMPTS = 3
1694:   PROBE_RETRY_DELAY_SECONDS = 1.0
1695: @@ -65,7 +67,7 @@ diff -ruN a/linux/raofflineproxy/network.py b/linux/raofflineproxy/network.py
1696:   HTTP_TOO_MANY_REQUESTS = 429
1697:   HTTP_GET_MAX_429_RETRIES = 4
1698:   HTTP_GET_INITIAL_429_BACKOFF_SECONDS = 2.0
1699: -@@ -251,7 +262,94 @@ def probe_retroachievements(
1700: +@@ -252,7 +263,94 @@ def probe_retroachievements(
1701:       return False
1702:   
1703:   
1704: @@ -160,6 +162,8 @@ diff -ruN a/linux/raofflineproxy/network.py b/linux/raofflineproxy/network.py
1705:       request = urllib.request.Request(
1706:           url,
1707:           headers={
1708: +diff --git a/linux/raofflineproxy/proxy_service.py b/linux/raofflineproxy/proxy_service.py
1709: +index c8e9724..c5b4a95 100644
1710:  --- a/linux/raofflineproxy/proxy_service.py
1711:  +++ b/linux/raofflineproxy/proxy_service.py
1712:  @@ -44,6 +44,7 @@ from .network import (
1713: @@ -216,12 +220,14 @@ diff -ruN a/linux/raofflineproxy/network.py b/linux/raofflineproxy/network.py
1714:  +                "application/json",
1715:  +                body_text,
1716:  +            )
1717: +         counted = path.startswith("/dorequest.php")
1718:           try:
1719:               if method == "POST":
1720: -                 status, reason, response_body = http_post(
1721: +diff --git a/linux/tests/test_linux_network.py b/linux/tests/test_linux_network.py
1722: +index 279f241..b5c610b 100644
1723:  --- a/linux/tests/test_linux_network.py
1724:  +++ b/linux/tests/test_linux_network.py
1725: -@@ -16,6 +16,55 @@ class LinuxNetworkTests(unittest.TestCase):
1726: +@@ -18,6 +18,55 @@ class LinuxNetworkTests(unittest.TestCase):
1727:           os.environ.pop("RAOFFLINEPROXY_CA_FILE", None)
1728:           os.environ.pop("SSL_CERT_FILE", None)
1729:   
1730: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/016-say-what-became-of-a-download.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/016-say-what-became-of-a-download.patch
1731: index 6b7f0dd180..55ecad6edc 100644
1732: --- a/projects/ROCKNIX/packages/network/raofflineproxy/patches/016-say-what-became-of-a-download.patch
1733: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/016-say-what-became-of-a-download.patch
1734: @@ -17,22 +17,17 @@ ignore the return value -- the service's own pool -- are unchanged.
1735:  Written for ROCKNIX (fork issue maxengel/rocknix#307, PL-060's
1736:  follow-up). Offered upstream as-is.
1737:  
1738: +diff --git a/linux/raofflineproxy/image_cache.py b/linux/raofflineproxy/image_cache.py
1739: +index 6378a23..d69e139 100644
1740:  --- a/linux/raofflineproxy/image_cache.py
1741:  +++ b/linux/raofflineproxy/image_cache.py
1742: -@@ -236,19 +236,35 @@ def fetch_static_asset(url: str, headers
1743: -     raise last_error if last_error else RuntimeError("fetch failed")
1744: +@@ -187,19 +187,25 @@ def rewrite_image_urls(
1745: +     return json.dumps(data, separators=(",", ":")), downloads
1746:   
1747:   
1748: -+# What became of a download (ROCKNIX, audit #307 PL-060's follow-up). A
1749: -+# server that does not have an image says so, and saying so is permanent in
1750: -+# a way a timeout is not: a caller that fetches a whole store's images needs
1751: -+# to tell the two apart, or one badge the server never had fails its every
1752: -+# pass. So download_static_image returns one of these, and logs the class,
1753: -+# the URL and the HTTP status of any image it did not cache.
1754: -+IMAGE_CACHED = "cached"        # there already, or fetched whole
1755: -+IMAGE_ABSENT = "absent"        # the server answered 404 or 410: it does not have it
1756: -+IMAGE_TRANSIENT = "transient"  # anything else: a timeout, a 5xx, a refused
1757: -+                               # connection, a short or damaged body -- try again
1758: ++IMAGE_CACHED = "cached"
1759: ++IMAGE_ABSENT = "absent"
1760: ++IMAGE_TRANSIENT = "transient"
1761:  +ABSENT_HTTP_STATUSES = (404, 410)
1762:  +
1763:  +
1764: @@ -48,17 +43,13 @@ follow-up). Offered upstream as-is.
1765:       (e.g. "/Badge/496014.png"). No-ops if already cached.
1766:   
1767:       If game_id is provided and image_path starts with /Images/, also copies the
1768: --    downloaded file to the per-game directory for UI display. All failures are
1769: +     downloaded file to the per-game directory for UI display. All failures are
1770:  -    silently swallowed — images are best-effort.
1771: -+    downloaded file to the per-game directory for UI display. Failures are not
1772: -+    raised -- images are best-effort -- but they are no longer silent: the
1773: -+    return value is IMAGE_CACHED, IMAGE_ABSENT (404 or 410) or IMAGE_TRANSIENT
1774: -+    (anything else), and an image not cached is logged with its class, URL and
1775: -+    HTTP status. Callers that ignore the return value are unchanged.
1776: ++    returned as cached, absent (404/410), or transient; no failure is raised.
1777:       """
1778:       try:
1779:           clean_path = image_path.lstrip("/").split("?", 1)[0]
1780: -@@ -308,8 +324,18 @@ def download_static_image(
1781: +@@ -228,8 +234,13 @@ def download_static_image(
1782:               if not icon_file.exists():
1783:                   icon_file.parent.mkdir(parents=True, exist_ok=True)
1784:                   icon_file.write_bytes(target.read_bytes())
1785: @@ -67,14 +58,9 @@ follow-up). Offered upstream as-is.
1786:  -        LOGGER.debug("Failed to cache image path=%s: %s", image_path, exc)
1787:  +        status = getattr(exc, "code", None)
1788:  +        outcome = IMAGE_ABSENT if status in ABSENT_HTTP_STATUSES else IMAGE_TRANSIENT
1789: -+        LOGGER.info(
1790: -+            "Image not cached (%s): %s%s -- %s",
1791: -+            outcome,
1792: -+            url,
1793: -+            f" HTTP {status}" if status is not None else "",
1794: -+            exc,
1795: -+        )
1796: ++        LOGGER.info("Image not cached (%s): %s%s -- %s", outcome, url,
1797: ++                    f" HTTP {status}" if status is not None else "", exc)
1798:  +        return outcome
1799:   
1800:   
1801: - def schedule_image_download(
1802: + def _fetch_image(url: str, user_agent: str) -> bytes:
1803: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/018-pixelelated-platform-identity.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/018-pixelelated-platform-identity.patch
1804: new file mode 100644
1805: index 0000000000..31d597f553
1806: --- /dev/null
1807: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/018-pixelelated-platform-identity.patch
1808: @@ -0,0 +1,58 @@
1809: +config: recognize pixelelated as the ROCKNIX settings layout
1810: +
1811: +pixelelated changes OS_NAME while retaining /storage and the canonical
1812: +system.cfg account. Without recognition, automatic credential discovery
1813: +misses that file after the rename. Match complete OS_NAME records so an
1814: +unrelated field or commented example is not treated as platform identity.
1815: +No stored paths, accounts, cache schema, or upstream queue behavior change.
1816: +Fork #408; intended for upstream contribution with #168.
1817: +
1818: +--- a/linux/raofflineproxy/config.py
1819: ++++ b/linux/raofflineproxy/config.py
1820: +@@ -74,7 +74,11 @@
1821: +         content = OS_RELEASE_PATH.read_text(encoding="utf-8", errors="replace")
1822: +     except OSError:
1823: +         return False
1824: +-    return 'OS_NAME="ROCKNIX"' in content
1825: ++    # pixelelated retains ROCKNIX's settings and emulator layout.
1826: ++    return any(
1827: ++        line in {'OS_NAME="ROCKNIX"', 'OS_NAME="pixelelated"'}
1828: ++        for line in content.splitlines()
1829: ++    )
1830: + 
1831: + 
1832: + def running_on_spruce() -> bool:
1833: +--- a/linux/tests/test_linux_rocknix.py
1834: ++++ b/linux/tests/test_linux_rocknix.py
1835: +@@ -18,6 +18,31 @@
1836: +                 self.assertTrue(config.running_on_rocknix())
1837: +             finally:
1838: +                 config.OS_RELEASE_PATH = original
1839: ++
1840: ++    def test_pixelelated_discovers_rocknix_account_settings(self) -> None:
1841: ++        with tempfile.TemporaryDirectory() as temp_dir:
1842: ++            os_release = Path(temp_dir) / "os-release"
1843: ++            system_cfg = Path(temp_dir) / "system.cfg"
1844: ++            os_release.write_text('OS_NAME="pixelelated"\n', encoding="utf-8")
1845: ++            system_cfg.touch()
1846: ++            with patch.object(config, "OS_RELEASE_PATH", os_release), patch.object(
1847: ++                config, "DEFAULT_ROCKNIX_SYSTEM_CFG", system_cfg
1848: ++            ):
1849: ++                self.assertTrue(config.running_on_rocknix())
1850: ++                self.assertEqual(config.detect_rocknix_system_cfg(), str(system_cfg))
1851: ++                self.assertEqual(
1852: ++                    config.detect_rocknix_system_cfg({"rocknix_system_cfg": "/custom/system.cfg"}),
1853: ++                    "/custom/system.cfg",
1854: ++                )
1855: ++
1856: ++    def test_platform_name_must_be_the_complete_os_name_record(self) -> None:
1857: ++        with tempfile.TemporaryDirectory() as temp_dir:
1858: ++            os_release = Path(temp_dir) / "os-release"
1859: ++            for text in ('# OS_NAME="ROCKNIX"', 'PREVIOUS_OS_NAME="ROCKNIX"', 'OS_NAME="ROCKNIX_REMIX"'):
1860: ++                with self.subTest(text=text):
1861: ++                    os_release.write_text(text + "\n", encoding="utf-8")
1862: ++                    with patch.object(config, "OS_RELEASE_PATH", os_release):
1863: ++                        self.assertFalse(config.running_on_rocknix())
1864: + 
1865: +     def test_running_on_rocknix_false_when_os_release_differs(self) -> None:
1866: +         with tempfile.TemporaryDirectory() as temp_dir:
1867: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/patches/019-consent-cache-initial-observation.patch b/projects/ROCKNIX/packages/network/raofflineproxy/patches/019-consent-cache-initial-observation.patch
1868: new file mode 100644
1869: index 0000000000..8f2fabf04a
1870: --- /dev/null
1871: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/patches/019-consent-cache-initial-observation.patch
1872: @@ -0,0 +1,81 @@
1873: +usage_stats: distinguish an unchecked consent cache from uptime zero
1874: +
1875: +A fresh process stores 0.0 as the last consent check. During the first
1876: +30 seconds after boot, monotonic() is below the cache interval, so a
1877: +configured grant is never read and opted-in requests are not counted.
1878: +The same sentinel cannot reliably invalidate consent during early boot.
1879: +
1880: +Use None for an unobserved/invalidated cache and read consent on its first
1881: +use. Preserve the existing interval after a real observation, explicit
1882: +decline clearing, version checks and report gating. No stored format changes.
1883: +Regression tests cover uptime zero/five, decline/regrant and unanswered
1884: +consent. Original failures remain under fork #457; contribution tracked #168.
1885: +
1886: +--- a/linux/raofflineproxy/usage_stats.py
1887: ++++ b/linux/raofflineproxy/usage_stats.py
1888: +@@ -231,17 +231,17 @@
1889: +         self._pending = PendingCounters()
1890: +         self._last_flush = time.monotonic()
1891: +         self._consent: Optional[bool] = None
1892: +-        self._consent_checked_at = 0.0
1893: ++        self._consent_checked_at: Optional[float] = None
1894: + 
1895: +     def forget_consent(self) -> None:
1896: +         with self._mutex:
1897: +-            self._consent_checked_at = 0.0
1898: ++            self._consent_checked_at = None
1899: +             if load_consent() is not True:
1900: +                 self._pending = PendingCounters()
1901: + 
1902: +     def _consented(self) -> bool:
1903: +         now = time.monotonic()
1904: +-        if now - self._consent_checked_at >= CONSENT_CACHE_SECONDS:
1905: ++        if self._consent_checked_at is None or now - self._consent_checked_at >= CONSENT_CACHE_SECONDS:
1906: +             self._consent = load_consent()
1907: +             self._consent_checked_at = now
1908: +         return self._consent is True
1909: +--- a/linux/tests/test_linux_usage_stats.py
1910: ++++ b/linux/tests/test_linux_usage_stats.py
1911: +@@ -39,6 +39,42 @@
1912: + 
1913: + 
1914: + class ConsentTests(UsageIsolation):
1915: ++    def test_granted_consent_counts_during_early_uptime(self) -> None:
1916: ++        for uptime in (0.0, 5.0):
1917: ++            with self.subTest(uptime=uptime), mock.patch.object(
1918: ++                usage_stats.time, "monotonic", return_value=uptime
1919: ++            ), mock.patch.object(usage_stats, "_recorder", usage_stats._Recorder()):
1920: ++                usage_stats.clear()
1921: ++                self.config.update({"usage_stats_consent": True, "usage_stats_consent_version": 1})
1922: ++                usage_stats.record_request(usage_stats.SOURCE_EMULATOR, 200)
1923: ++                usage_stats.flush()
1924: ++                self.assertEqual(usage_stats.snapshot().get("requests_emulator"), 1)
1925: ++
1926: ++    def test_consent_changes_apply_immediately_during_early_uptime(self) -> None:
1927: ++        with mock.patch.object(usage_stats.time, "monotonic", return_value=5.0), mock.patch.object(
1928: ++            usage_stats, "_recorder", usage_stats._Recorder()
1929: ++        ):
1930: ++            usage_stats.save_consent(True)
1931: ++            usage_stats.record_request(usage_stats.SOURCE_EMULATOR, 200)
1932: ++            usage_stats.flush()
1933: ++            self.assertEqual(usage_stats.snapshot().get("requests_emulator"), 1)
1934: ++            usage_stats.save_consent(False)
1935: ++            usage_stats.record_request(usage_stats.SOURCE_EMULATOR, 200)
1936: ++            usage_stats.flush()
1937: ++            self.assertEqual(usage_stats.snapshot(), {})
1938: ++            usage_stats.save_consent(True)
1939: ++            usage_stats.record_request(usage_stats.SOURCE_EMULATOR, 200)
1940: ++            usage_stats.flush()
1941: ++            self.assertEqual(usage_stats.snapshot().get("requests_emulator"), 1)
1942: ++
1943: ++    def test_unanswered_is_not_counted_during_early_uptime(self) -> None:
1944: ++        with mock.patch.object(usage_stats.time, "monotonic", return_value=0.0), mock.patch.object(
1945: ++            usage_stats, "_recorder", usage_stats._Recorder()
1946: ++        ):
1947: ++            usage_stats.record_request(usage_stats.SOURCE_EMULATOR, 200)
1948: ++            usage_stats.flush()
1949: ++            self.assertEqual(usage_stats.snapshot(), {})
1950: ++
1951: +     def test_unanswered_is_none(self) -> None:
1952: +         self.assertIsNone(usage_stats.load_consent())
1953: + 
1954: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images b/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images
1955: index 62fa455139..589b74c92d 100755
1956: --- a/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images
1957: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-images
1958: @@ -246,7 +246,7 @@ def all_paths(storage: Storage) -> set[str]:
1959:      """Every image path the cached rows refer to, whether its file is there."""
1960:      seen: set[str] = set()
1961:      for prefix in ROW_PREFIXES:
1962: -        for row in storage.get_all_cache_by_prefix(prefix):
1963: +        for row in storage.iter_cache_by_prefix(prefix):
1964:              body = row.get("responseBody")
1965:              if body:
1966:                  seen |= image_paths(body)
1967: @@ -258,7 +258,7 @@ def missing_paths(storage: Storage) -> tuple[list[str], int, int]:
1968:      seen: set[str] = set()
1969:      rows = 0
1970:      for prefix in ROW_PREFIXES:
1971: -        for row in storage.get_all_cache_by_prefix(prefix):
1972: +        for row in storage.iter_cache_by_prefix(prefix):
1973:              body = row.get("responseBody")
1974:              if not body:
1975:                  continue
1976: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed b/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed
1977: index 34263b7d49..3d295cb43c 100755
1978: --- a/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed
1979: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed
1980: @@ -39,13 +39,13 @@ import sys
1981:  import threading
1982:  from pathlib import Path
1983:  
1984: -from raofflineproxy import cache_keys, image_cache, network, rom_browser, rom_cache
1985: +from raofflineproxy import cache_budget, cache_keys, image_cache, network, rate_limit, rom_browser, rom_cache
1986:  from raofflineproxy.auth import resolve_credentials
1987:  from raofflineproxy.config import configure_logging, image_caching_enabled, load_config
1988:  from raofflineproxy.network import apply_scan_batch_cooldown
1989:  from raofflineproxy.rom_browser import add_rom_to_cache, normalize_cached_rom_path
1990:  from raofflineproxy.rom_cache import cache_game
1991: -from raofflineproxy.storage import Storage
1992: +from raofflineproxy.storage import Storage, current_millis
1993:  from raofflineproxy.utils import proxy_user_agent, self_user_agent
1994:  
1995:  # Every RetroAchievements action a game cost, in order. http_get is bound by
1996: @@ -89,15 +89,24 @@ def cache_indexed(game_id: int, hash_value: str, path: Path, credentials: dict,
1997:      """Cache one game from its id and hash. Returns the title cached."""
1998:      hash_value = cache_keys.normalize_hash(hash_value)
1999:      user_agent = proxy_user_agent(self_user_agent())
2000: -    cache_game(
2001: -        game_id,
2002: -        hash_value,
2003: -        credentials,
2004: -        user_agent,
2005: -        storage,
2006: -        config_data,
2007: -        cache_images=image_caching_enabled(config_data),
2008: -    )
2009: +    paused = max(rate_limit.paused_until() or 0, cache_budget.load(storage).paused_until)
2010: +    if paused > current_millis():
2011: +        raise rate_limit.RateLimitedError("RetroAchievements asked to slow down; try again later")
2012: +    try:
2013: +        with rate_limit.background():
2014: +            cache_game(
2015: +                game_id,
2016: +                hash_value,
2017: +                credentials,
2018: +                user_agent,
2019: +                storage,
2020: +                config_data,
2021: +                cache_images=image_caching_enabled(config_data),
2022: +            )
2023: +    finally:
2024: +        paused = rate_limit.paused_until()
2025: +        if paused is not None:
2026: +            cache_budget.pause_until(storage, paused)
2027:      storage.upsert_cache(
2028:          cache_keys.game_id(hash_value),
2029:          json.dumps({"GameID": game_id}, separators=(",", ":")),
2030: @@ -178,12 +187,12 @@ def main() -> int:
2031:                  print(f"FAIL {index}/{total} {label}: not found", flush=True)
2032:                  continue
2033:              try:
2034: -                result = add_rom_to_cache(path, storage, config_data)
2035: +                result = add_rom_to_cache(path, storage, config_data, budgeted=False)
2036:              except Exception as error:
2037:                  failed += 1
2038:                  print(f"FAIL {index}/{total} {label}: {error}", flush=True)
2039:                  continue
2040: -            if result.success:
2041: +            if result.success and not result.queued:
2042:                  cached += 1
2043:                  print(f"OK {index}/{total} {label}", flush=True)
2044:              else:
2045: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl b/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl
2046: index f9e2dc1453..435853c2e8 100755
2047: --- a/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl
2048: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl
2049: @@ -239,10 +239,12 @@
2050:  #
2051:  # The store this reads -- read-only, through the service's own sqlite3
2052:  # module, never written here -- is the client's schema at the commit
2053: -# package.mk pins (248ce5acae75113d09500cd7c6661a12fee4b93c, storage.py
2054: -# _initialize_sqlite, read 2026-09-28 for audit #308 F-RA-07 at c1bd3724
2055: -# and unchanged since, as are cache_keys.py and proxy_service.py; the
2056: -# header named 4e9bab48, three pins back, until then): pending_awards(id,
2057: +# package.mk pins (879b158995d412af434301ebdae581f66b8b6d57, storage.py
2058: +# _initialize_sqlite, reviewed 2026-10-06 for #457). Consumed columns and
2059: +# cache-key spellings remain compatible. The additive cached_game_meta table
2060: +# and delete/rename triggers index existing rows without changing award data. The suite reads a store the current client wrote,
2061: +# and the integration fixture reopens the predecessor's store with current
2062: +# Storage twice, preserving cache/login/base/subset award bytes: pending_awards(id,
2063:  # achievementId, queryString, requestBody, queuedAt, status) for pending,
2064:  # pending-ids and summary; api_cache(cacheKey, responseBody, sourceRomPath,
2065:  # cachedAt) for account, summary, the ready set behind added= and the
2066: @@ -1476,7 +1478,7 @@ def whole_games():
2067:          rows = db.execute("SELECT cacheKey, substr(responseBody, 1, 512) FROM api_cache WHERE cacheKey LIKE ? OR cacheKey LIKE ?", ("unlocks:%", "achievementsets:%")).fetchall()
2068:      except Exception:
2069:          db = None
2070: -        rows = [(e.get("cacheKey") or "", e.get("responseBody") or "") for prefix in (cache_keys.PREFIX_UNLOCKS, cache_keys.PREFIX_ACHIEVEMENTSETS) for e in storage.get_all_cache_by_prefix(prefix)]
2071: +        rows = ((e.get("cacheKey") or "", e.get("responseBody") or "") for prefix in (cache_keys.PREFIX_UNLOCKS, cache_keys.PREFIX_ACHIEVEMENTSETS) for e in storage.iter_cache_by_prefix(prefix))
2072:      for key, head in rows:
2073:          parts = str(key).split(":")
2074:          if parts[0] == "unlocks":
2075: @@ -1502,7 +1504,7 @@ def whole_games():
2076:  whole = whole_games()
2077:  cached_paths = {
2078:      normalize_cached_rom_path(entry["sourceRomPath"])
2079: -    for entry in storage.get_all_cache_by_prefix(cache_keys.PREFIX_PATCH)
2080: +    for entry in storage.cache_summaries_by_prefix(cache_keys.PREFIX_PATCH)
2081:      if isinstance(entry.get("sourceRomPath"), str) and entry["sourceRomPath"].strip()
2082:      and entry["cacheKey"].endswith(":" + user)
2083:      and cache_keys.parse_game_id_from_patch_key(entry["cacheKey"]) in whole
2084: diff --git a/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-refresh b/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-refresh
2085: index b5f63b3243..cab14d3805 100755
2086: --- a/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-refresh
2087: +++ b/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-refresh
2088: @@ -51,23 +51,14 @@ def note(text: str) -> None:
2089:      print(text, flush=True)
2090:  
2091:  
2092: -def cached_games(storage: Storage) -> list[dict]:
2093: -    """Every patch row, as due_refresh_game_ids wants them."""
2094: -    rows = []
2095: -    for row in storage.get_all_cache_by_prefix(cache_keys.PREFIX_PATCH):
2096: -        if row.get("responseBody"):
2097: -            rows.append(row)
2098: -    return rows
2099: +def cached_games(storage: Storage) -> list[str]:
2100: +    """Patch keys only, matching upstream's refresh scope without loading bodies."""
2101: +    return storage.cache_keys_by_prefix(cache_keys.PREFIX_PATCH)
2102:  
2103:  
2104: -def game_ids(rows: list[dict]) -> list[int]:
2105: -    ids = []
2106: -    for row in rows:
2107: -        key = str(row.get("cacheKey") or "")
2108: -        parts = key.split(":")
2109: -        if len(parts) > 1 and parts[1].isdigit():
2110: -            ids.append(int(parts[1]))
2111: -    return ids
2112: +def game_ids(keys: list[str]) -> list[int]:
2113: +    return sorted({gid for key in keys
2114: +                   if (gid := cache_keys.parse_game_id_from_patch_key(key)) is not None})
2115:  
2116:  
2117:  def drop_startsession(storage: Storage, game_id: int) -> int:
2118: @@ -81,8 +72,7 @@ def drop_startsession(storage: Storage, game_id: int) -> int:
2119:      removed = 0
2120:      prefix = f"{cache_keys.PREFIX_STARTSESSION}{game_id}:"
2121:      try:
2122: -        for row in storage.get_all_cache_by_prefix(cache_keys.PREFIX_STARTSESSION):
2123: -            key = str(row.get("cacheKey") or "")
2124: +        for key in storage.cache_keys_by_prefix(prefix):
2125:              if key.startswith(prefix):
2126:                  storage.delete_cache(key)
2127:                  removed += 1
2128: @@ -101,7 +91,7 @@ def row_ages(storage: Storage, game_id: int) -> str:
2129:      for prefix in (cache_keys.PREFIX_PATCH,
2130:                     cache_keys.PREFIX_UNLOCKS, cache_keys.PREFIX_STARTSESSION):
2131:          try:
2132: -            rows = [r for r in storage.get_all_cache_by_prefix(prefix)
2133: +            rows = [r for r in storage.cache_summaries_by_prefix(prefix)
2134:                      if f":{game_id}:" in f":{str(r.get('cacheKey') or '')}:"
2135:                      or str(r.get("cacheKey") or "").startswith(f"{prefix}{game_id}:")]
2136:          except Exception:
2137: @@ -110,7 +100,7 @@ def row_ages(storage: Storage, game_id: int) -> str:
2138:              ages.append(f"{prefix.rstrip(':')}=none")
2139:              continue
2140:          try:
2141: -            stamp = int(rows[0].get("cachedAt") or 0)
2142: +            stamp = max(int(row.get("cachedAt") or 0) for row in rows)
2143:              stamp = stamp // 1000 if stamp > 1e11 else stamp
2144:              ages.append(f"{prefix.rstrip(':')}={max(0, now_ms // 1000 - stamp)}s")
2145:          except Exception:
2146: diff --git a/projects/ROCKNIX/packages/network/rclone/package.mk b/projects/ROCKNIX/packages/network/rclone/package.mk
2147: index 5186c7da3a..c2ae281d74 100644
2148: --- a/projects/ROCKNIX/packages/network/rclone/package.mk
2149: +++ b/projects/ROCKNIX/packages/network/rclone/package.mk
2150: @@ -69,6 +69,7 @@ makeinstall_target() {
2151:    cp cloud_oauth ${INSTALL}/usr/bin/
2152:    cp cloud_content_restore ${INSTALL}/usr/bin/
2153:    cp cloud_content_backup ${INSTALL}/usr/bin/
2154: +  cp cloud_content_transfer ${INSTALL}/usr/bin/
2155:    cp cloud_sync_cleanup_duplicates.sh ${INSTALL}/usr/bin/
2156:    cp cloud_saves_root ${INSTALL}/usr/bin/
2157:    cp cloud_capture ${INSTALL}/usr/bin/
2158: @@ -82,6 +83,7 @@ makeinstall_target() {
2159:    # cloud_scan: the restore flow's scan page runs it first and offers only
2160:    # what it found (D-CLOUD-156, fork #350); reads only, no lock.
2161:    cp cloud_scan ${INSTALL}/usr/bin/
2162: +  cp rasteratops-settings-archive ${INSTALL}/usr/bin/
2163:    # No game-end event hook. EmulationStation runs the save sync itself now
2164:    # (FileData::launchGame), so it can show the result on the progress card
2165:    # instead of backgrounding the work into /dev/null where nobody could tell
2166: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup b/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup
2167: index c7da6b6af1..47dd405085 100755
2168: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup
2169: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup
2170: @@ -805,23 +805,19 @@ say_why() {
2171:  # on a bucket whether a folder exists: its parent lists it. cloud_restore's
2172:  # two helpers, the same rule here so the two scripts never disagree about
2173:  # whether a saves folder is there (#141).
2174: -BUCKET_BASED=""
2175: -bucket_based() {
2176: -    if [ -z "${BUCKET_BASED}" ]; then
2177: -        if rclone backend features "${REMOTENAME}" 2>/dev/null | grep -q '"BucketBased": *true'; then
2178: -            BUCKET_BASED=1
2179: -        else
2180: -            BUCKET_BASED=0
2181: -        fi
2182: -    fi
2183: -    [ "${BUCKET_BASED}" = "1" ]
2184: -}
2185: +# Return 0 present, 1 absent, 2 unknown. The caller must never turn 2
2186: +# into a create-folder offer. Preserve the provider's error for reporting.
2187:  bucket_dir_listed() {
2188: -    local path="${1%/}" parent name
2189: +    local path="${1%/}" parent name listing
2190:      name="${path##*/}"
2191:      [ -n "${name}" ] || return 0
2192:      parent="${path%/*}"
2193: -    rclone lsf --dirs-only "${REMOTENAME}${parent}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -qx "${name}/"
2194: +    # This is a directory query. The trailing slash avoids WebDAV's extra
2195: +    # file-type probe before listing, while retaining the same three-way
2196: +    # presence result (#364); no absence result is cached between runs.
2197: +    listing=$(rclone lsf --dirs-only "${REMOTENAME}${parent%/}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); BUCKET_READ_RC=$?
2198: +    [ "${BUCKET_READ_RC}" -eq 0 ] || return 2
2199: +    printf '%s\n' "${listing}" | grep -qxF -- "${name}/"
2200:  }
2201:  
2202:  # Whether the saves setting is a default this project once shipped
2203: @@ -1673,10 +1669,24 @@ backup_game_saves() {
2204:      # a guess would leave the saves only on the device.
2205:      if superseded_saves_setting; then
2206:          local saves_folder="${SAVES_REMOTE%/}" list_rc
2207: -        rclone lsd "${REMOTENAME}${saves_folder}" "${RCLONE_PROBE_OPTS[@]}" >/dev/null 2>&1; list_rc=$?
2208: -        if [ ${list_rc} -eq 0 ] && bucket_based && ! bucket_dir_listed "${saves_folder}"; then
2209: -            list_rc=3
2210: -        fi
2211: +        # The parent's directory listing proves presence on both path and
2212: +        # bucket backends. One call replaces lsd + backend features (and on
2213: +        # buckets a third call); exit sync keeps the absence guard without
2214: +        # paying for backend classification on every game (#364, #377).
2215: +        bucket_dir_listed "${saves_folder}"; list_rc=$?
2216: +        case "${list_rc}" in
2217: +            0) ;;
2218: +            1) list_rc=3 ;; # A successful parent listing omitted this folder.
2219: +            2)
2220: +                list_rc=5  # Unknown: retain the existing backup fallback.
2221: +                # A missing parent on a path backend means the child is
2222: +                # absent too. Confirm with the child's own missing status;
2223: +                # a bucket's successful empty lsd proves nothing here.
2224: +                if [ "${BUCKET_READ_RC}" -eq 3 ]; then
2225: +                    rclone lsd "${REMOTENAME}${saves_folder}" "${RCLONE_PROBE_OPTS[@]}" >/dev/null 2>&1
2226: +                    [ "$?" -eq 3 ] && list_rc=3
2227: +                fi ;;
2228: +        esac
2229:          if [ ${list_rc} -eq 3 ]; then
2230:              log_message "saves folder ${SAVES_REMOTE} is a default an earlier version shipped, and the cloud has none; a backup does not make it (D-CLOUD-172)" "false"
2231:              log_message "Nothing backed up: your cloud has no ${saves_folder} folder yet." "true"
2232: @@ -2384,7 +2394,7 @@ MANIFEST
2233:                  osn=$(os_name)
2234:                  listing=$(rclone lsf --files-only --include "*.{zip,tar.gz}" "${device_dest}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null)
2235:                  mine=$(printf '%s\n' "${listing}" \
2236: -                       | grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-${osn}_SETTINGS\.tar\.gz$" | sort -r)
2237: +                       | grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-(${osn}|ROCKNIX|RASTERATOPS)_SETTINGS\.tar\.gz$" | sort -r)
2238:                  total_n=$(printf '%s\n' "${listing}" | grep -c .)
2239:                  mine_n=$(printf '%s\n' "${mine}" | grep -c .)
2240:                  if [ "${total_n}" -gt "${mine_n}" ]; then
2241: @@ -2432,11 +2442,18 @@ main() {
2242:      # anyway; only the system-only path has no such step of its own. After
2243:      # load_config, which sets an automatic run's deadline: the probe ran
2244:      # before it, outside the ceiling (#308 gpt F-CS-34).
2245: -    [ "${SYSTEM_ONLY}" -eq 1 ] && check_internet
2246:      
2247: -    # Use the first configured remote in rclone
2248: -    # Note: This assumes at least one remote is configured and the first one should be used
2249: +    # An existing config file can contain no remote (#392). Without the
2250: +    # prefix, rclone interprets SAVES_REMOTE as a local path. Refuse before
2251: +    # any path operation instead of offering to create a "cloud" locally.
2252:      REMOTENAME=$(first_remote)
2253: +    case "${REMOTENAME}" in
2254: +        ?*:) ;;
2255: +        *) log_message "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first." "true" "ERROR"
2256: +           say_why "YOUR CLOUD STORAGE ISN'T SET UP YET"
2257: +           clean_exit 1 ;;
2258: +    esac
2259: +    [ "${SYSTEM_ONLY}" -eq 1 ] && check_internet
2260:      
2261:      # Begin main script operations with user-friendly header
2262:      log_message "=> ${OS_NAME} CLOUD BACKUP\n"
2263: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup
2264: index 617075d27f..dbb2a75cd7 100755
2265: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup
2266: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup
2267: @@ -217,6 +217,8 @@ RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10
2268:  _net_opts=$(echo "${RCLONE_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
2269:  [ -n "${_net_opts}" ] || _net_opts="${RCLONE_NET_OPTS_FALLBACK}"
2270:  read -r -a RCLONE_NET_OPTS_ARRAY <<< "${_net_opts}"
2271: +# Installed beside this script, also when the host fixtures copy it.
2272: +. "$(dirname "${BASH_SOURCE[0]}")/cloud_content_transfer" || exit 1
2273:  # A probe is a single listing that exists to answer quickly: one attempt,
2274:  # tighter than the transfers (the same values the saves scripts probe with).
2275:  readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
2276: @@ -260,7 +262,7 @@ say_why() {
2277:  why_for() {
2278:      case "$1" in
2279:          3|4) echo "COULDN'T FIND YOUR CLOUD FOLDER" ;;
2280: -        5)   echo "YOUR CLOUD STOPPED ANSWERING" ;;
2281: +        5|124) echo "YOUR CLOUD STOPPED ANSWERING" ;;
2282:          6)   echo "SOME FILES DIDN'T FINISH" ;;
2283:          7|8) echo "YOUR CLOUD WOULDN'T TAKE THE FILES" ;;
2284:          130) echo "IT WAS STOPPED" ;;
2285: @@ -703,7 +705,7 @@ for DIR in "${DIRS[@]}"; do
2286:      # --seed-folders) is not content, and neither side counts it (#308 gpt
2287:      # F-CS-30): it came down into /storage/roms/bios and read ever after as a
2288:      # file this device has and the cloud does not.
2289: -    rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2290: +    bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2291:          "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${MEDIA_EXCLUDES[@]}" \
2292:          --exclude "gamelist.xml" --exclude "**/gamelist.xml" --exclude "/README.txt" \
2293:          --progress --stats 1s \
2294: @@ -715,8 +717,8 @@ for DIR in "${DIRS[@]}"; do
2295:      # result is the unit's, by the same 0|9 rule (audit #307 PL-066): it
2296:      # was discarded with `|| true`, so a game list that did not move left a
2297:      # unit, a stamp and a page that said the unit had.
2298: -    if [ "${MEDIA_MODE}" != roms ]; then
2299: -        rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2300: +    if [ "${MEDIA_MODE}" != roms ] && { [ "${RC}" -eq 0 ] || [ "${RC}" -eq 9 ]; }; then
2301: +        bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2302:              "${GAMELIST_ONLY[@]}" --update \
2303:              --stats 0 \
2304:              --log-file "${LOG_FILE}" --log-level INFO
2305: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore
2306: index a4d7ea5857..4f9a62f367 100755
2307: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore
2308: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore
2309: @@ -223,6 +223,8 @@ RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10
2310:  _net_opts=$(echo "${RCLONE_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
2311:  [ -n "${_net_opts}" ] || _net_opts="${RCLONE_NET_OPTS_FALLBACK}"
2312:  read -r -a RCLONE_NET_OPTS_ARRAY <<< "${_net_opts}"
2313: +# Installed beside this script, also when the host fixtures copy it.
2314: +. "$(dirname "${BASH_SOURCE[0]}")/cloud_content_transfer" || exit 1
2315:  # A probe is a single listing that exists to answer quickly: one attempt,
2316:  # tighter than the transfers (the same values the saves scripts probe with).
2317:  readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
2318: @@ -266,7 +268,7 @@ say_why() {
2319:  why_for() {
2320:      case "$1" in
2321:          3|4) echo "COULDN'T FIND YOUR CLOUD FOLDER" ;;
2322: -        5)   echo "YOUR CLOUD STOPPED ANSWERING" ;;
2323: +        5|124) echo "YOUR CLOUD STOPPED ANSWERING" ;;
2324:          6)   echo "SOME FILES DIDN'T FINISH" ;;
2325:          7|8) echo "YOUR CLOUD WOULDN'T TAKE THE FILES" ;;
2326:          130) echo "IT WAS STOPPED" ;;
2327: @@ -731,7 +733,7 @@ match_plan_one() {
2328:  
2329:      if [ "${lrc}" -eq 0 ] && [ -n "${listing}" ]; then
2330:          # Present in the cloud: sync reconciles both directions of difference.
2331: -        out=$(rclone sync "${src}" "${local_dir}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2332: +        out=$(bounded_content_rclone sync "${src}" "${local_dir}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2333:                  "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
2334:                  --dry-run --stats 0 2>&1)
2335:          lrc=$?
2336: @@ -1021,7 +1023,7 @@ match_run() {
2337:                      # the removals are final (D-CLOUD-023), which is why a
2338:                      # count above the preview's is refused before this runs.
2339:                      match_before "${sys}"
2340: -                    rclone sync "$(remote_for "${sys}")" "${DEST}/${sys}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2341: +                    bounded_content_rclone sync "$(remote_for "${sys}")" "${DEST}/${sys}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2342:                          "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
2343:                          --max-delete "${files}" \
2344:                          --progress --stats 1s \
2345: @@ -1293,7 +1295,7 @@ case "${1}" in
2346:          # unchanged: the sentinels are 75 and 69, which rclone never returns.
2347:          if [ "${scan_rc}" -ne 0 ] && [ "${scan_rc}" -ne 3 ]; then
2348:              log_message "scan: the cloud could not be read (rclone exit ${scan_rc})"
2349: -            echo "Your cloud couldn't be read. Try again." >&2
2350: +            echo "Couldn't finish reading your cloud. Try again." >&2
2351:              exit "${scan_rc}"
2352:          fi
2353:          # The pre-tier rows (a system straight under the content root) are
2354: @@ -1542,7 +1544,7 @@ for DIR in "${DIRS[@]}"; do
2355:      # F-CS-30): it came down into /storage/roms/bios and read ever after as a
2356:      # file this device has and the cloud does not.
2357:      UNIT_LOG0=$(log_offset)
2358: -    rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2359: +    bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2360:          "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${MEDIA_EXCLUDES[@]}" \
2361:          --exclude "gamelist.xml" --exclude "**/gamelist.xml" --exclude "/README.txt" \
2362:          --progress --stats 1s \
2363: @@ -1554,8 +1556,8 @@ for DIR in "${DIRS[@]}"; do
2364:      # result is the unit's, by the same 0|9 rule (audit #307 PL-066): it
2365:      # was discarded with `|| true`, so a game list that did not move left a
2366:      # unit, a stamp and a page that said the unit had.
2367: -    if [ "${MEDIA_MODE}" != roms ]; then
2368: -        rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2369: +    if [ "${MEDIA_MODE}" != roms ] && { [ "${RC}" -eq 0 ] || [ "${RC}" -eq 9 ]; }; then
2370: +        bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2371:              "${GAMELIST_ONLY[@]}" --update \
2372:              --stats 0 \
2373:              --log-file "${LOG_FILE}" --log-level INFO
2374: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_transfer b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_transfer
2375: new file mode 100644
2376: index 0000000000..6efaf26e4f
2377: --- /dev/null
2378: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_transfer
2379: @@ -0,0 +1,158 @@
2380: +#!/bin/bash
2381: +# SPDX-License-Identifier: GPL-2.0
2382: +# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
2383: +
2384: +# Shared by the two content scripts. D-CLOUD-127 applies to content too:
2385: +# SDK retries must not outlive inactivity, but a progressing ROM library
2386: +# has no total-duration limit (#401). Keep the five-counter interpretation
2387: +# aligned with cloud_backup/cloud_restore; a retry's rising total is not
2388: +# progress. These helpers are sourced, never run as a separate command.
2389: +
2390: +child_running() {
2391: +    local _pid _comm state
2392: +    { read -r _pid _comm state _ < "/proc/$1/stat"; } 2>/dev/null || return 1
2393: +    [ "${state}" != "Z" ]
2394: +}
2395: +
2396: +# The furthest rclone's stats block in the tail of a trace has got: bytes
2397: +# transferred, checks done, files transferred, files deleted, entries
2398: +# listed -- five integers on one line. The listed count is the Checks line's
2399: +# "Listed N" (#308, the seats' claude F-CS-13): a first backup against a
2400: +# folder of tens of thousands of files lists for longer than the ceiling
2401: +# before its first check completes, and a count that only read checks
2402: +# ended that run as a stall. The bytes line is the Transferred: with a unit in
2403: +# it; the one without is the file count. A block's last line is glued to
2404: +# the next block's Transferred: (the rule's "Progress output" section),
2405: +# which the sed unglues. Rates, ETAs, percentages and the elapsed time are
2406: +# not progress and are not read.
2407: +progress_mark() {
2408: +    tail -c 8192 "$1" 2>/dev/null | tr '\r' '\n' | sed 's/Transferred:/\nTransferred:/g' | awk '
2409: +        function unit(u) {
2410: +            if (u ~ /^K/) return 1024
2411: +            if (u ~ /^M/) return 1048576
2412: +            if (u ~ /^G/) return 1073741824
2413: +            if (u ~ /^T/) return 1099511627776
2414: +            return 1
2415: +        }
2416: +        /^Transferred:/ {
2417: +            s = $0; sub(/^Transferred:[ \t]*/, "", s); sub(/ \/.*$/, "", s)
2418: +            n = split(s, w, " ")
2419: +            if (n >= 2) { b = w[1] * unit(w[2]); if (b > bytes) bytes = b }
2420: +            else if (n == 1 && w[1] ~ /^[0-9]+$/ && w[1] + 0 > files) files = w[1] + 0
2421: +        }
2422: +        /^Checks:/  { s = $0; sub(/^Checks:[ \t]*/, "", s);  sub(/[^0-9].*$/, "", s); if (s + 0 > checks)  checks  = s + 0
2423: +                      if ($0 ~ /Listed [0-9]/) { l = $0; sub(/^.*Listed /, "", l); sub(/[^0-9].*$/, "", l); if (l + 0 > listed) listed = l + 0 } }
2424: +        /^Deleted:/ { s = $0; sub(/^Deleted:[ \t]*/, "", s); sub(/[^0-9].*$/, "", s); if (s + 0 > deleted) deleted = s + 0 }
2425: +        END { printf "%.0f %.0f %.0f %.0f %.0f\n", bytes, checks, files, deleted, listed }'
2426: +}
2427: +
2428: +# Did any count in <mark> exceed <high water>? Prints the new high water --
2429: +# each field the larger of the two, so a count that falls back (a phase
2430: +# that starts over) never lets an old level read as new progress -- and
2431: +# returns 0 when something grew.
2432: +advance_mark() {
2433: +    local a=($1) b=(${2:-0 0 0 0 0}) i grew=1
2434: +    for i in 0 1 2 3 4; do
2435: +        if [ "${a[$i]:-0}" -gt "${b[$i]:-0}" ] 2>/dev/null; then
2436: +            b[$i]="${a[$i]}"
2437: +            grew=0
2438: +        fi
2439: +    done
2440: +    echo "${b[*]}"
2441: +    return "${grew}"
2442: +}
2443: +
2444: +idle_timeout_seconds() {
2445: +    local v="" prev="" a
2446: +    for a in "$@"; do
2447: +        case "${a}" in
2448: +            --timeout=*) v="${a#--timeout=}" ;;
2449: +            *) [ "${prev}" = "--timeout" ] && v="${a}" ;;
2450: +        esac
2451: +        prev="${a}"
2452: +    done
2453: +    case "${v}" in
2454: +        *h) [[ "${v%h}" =~ ^[0-9]+$ ]] && echo $(( ${v%h} * 3600 )) ;;
2455: +        *m) [[ "${v%m}" =~ ^[0-9]+$ ]] && echo $(( ${v%m} * 60 )) ;;
2456: +        *s) [[ "${v%s}" =~ ^[0-9]+$ ]] && echo "${v%s}" ;;
2457: +        *)  [[ "${v}" =~ ^[0-9]+$ ]] && echo "${v}" ;;
2458: +    esac
2459: +}
2460: +
2461: +# A subshell keeps cleanup traps local: cloud_content_restore also owns
2462: +# the scan's temporary directory. stdout remains the original stats stream;
2463: +# stderr still reaches the caller, including dry-run deletion notices.
2464: +bounded_content_rclone() (
2465: +    local dir="" pid="" tee_pid="" rc=1 ended=0
2466: +    local high="0 0 0 0 0" mark new since now idle ceiling=36 n
2467: +    local -a args=("$@")
2468: +    local has_progress=0 a
2469: +    for a in "$@"; do
2470: +        case "${a}" in --progress|-P) has_progress=1 ;; esac
2471: +    done
2472: +    [ "${has_progress}" -eq 1 ] || args+=(--progress)
2473: +    idle=$(idle_timeout_seconds "$@")
2474: +    [[ "${idle}" =~ ^[0-9]+$ ]] && [ "${idle}" -gt 0 ] && ceiling=$((idle + 6))
2475: +
2476: +    stop_child() {
2477: +        [ -n "$1" ] || return 0
2478: +        if child_running "$1"; then
2479: +            kill -TERM "$1" 2>/dev/null
2480: +            local n=0
2481: +            while [ "${n}" -lt 30 ] && child_running "$1"; do sleep 0.1; n=$((n + 1)); done
2482: +            child_running "$1" && kill -KILL "$1" 2>/dev/null
2483: +        fi
2484: +        wait "$1" 2>/dev/null || true
2485: +    }
2486: +    cleanup() {
2487: +        stop_child "${pid}"
2488: +        stop_child "${tee_pid}"
2489: +        [ -z "${dir}" ] || rm -rf -- "${dir}"
2490: +    }
2491: +    trap cleanup EXIT
2492: +    trap 'exit 130' INT
2493: +    trap 'exit 143' TERM
2494: +    # Failure to create the guard is a failure of this call, never an
2495: +    # unbounded transfer silently accepted as guarded.
2496: +    if ! dir=$(mktemp -d "${CEILING_DIR_ROOT:-/var/run}/cloud-content.XXXXXX")         || ! mkfifo "${dir}/fifo"; then
2497: +        log_message "cannot create content transfer inactivity guard"
2498: +        exit 1
2499: +    fi
2500: +    : > "${dir}/trace" || exit 1
2501: +    tee "${dir}/trace" < "${dir}/fifo" &
2502: +    tee_pid=$!
2503: +    command rclone "${args[@]}" > "${dir}/fifo" &
2504: +    pid=$!
2505: +    since=${SECONDS}
2506: +    while child_running "${pid}"; do
2507: +        sleep 0.25
2508: +        now=${SECONDS}
2509: +        [ "${now}" -gt "${since}" ] || continue
2510: +        mark=$(progress_mark "${dir}/trace")
2511: +        if new=$(advance_mark "${mark}" "${high}"); then
2512: +            high="${new}"
2513: +            since=${SECONDS}
2514: +        elif [ $((now - since)) -ge "${ceiling}" ]; then
2515: +            ended=1
2516: +            stop_child "${pid}"
2517: +            break
2518: +        fi
2519: +    done
2520: +    if [ "${ended}" -eq 1 ]; then
2521: +        rc=124
2522: +        log_message "rclone $1 made no progress for ${ceiling}s; reporting 124"
2523: +    else
2524: +        wait "${pid}"; rc=$?
2525: +    fi
2526: +    pid=""
2527: +    # Drain the final stats before the caller prints the outcome. A
2528: +    # terminated test shim can leave a writer behind; do not wait forever.
2529: +    n=0
2530: +    while [ "${n}" -lt 30 ] && child_running "${tee_pid}"; do sleep 0.1; n=$((n + 1)); done
2531: +    stop_child "${tee_pid}"
2532: +    tee_pid=""
2533: +    if [ -s "${dir}/trace" ] && [ -n "$(tail -c1 "${dir}/trace")" ]; then
2534: +        printf '\n'
2535: +    fi
2536: +    exit "${rc}"
2537: +)
2538: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout b/projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout
2539: index 5949be7cea..1a1dc4bfe6 100755
2540: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout
2541: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout
2542: @@ -54,9 +54,9 @@
2543:  . /etc/profile 2>/dev/null
2544:  
2545:  SYNC_CONF="/storage/.config/cloud_sync.conf"
2546: -NEW_SAVES="/Rasteratops/Saves"
2547: -NEW_BACKUPS="/Rasteratops/Backups"
2548: -NEW_CONTENT="/Rasteratops/Content"
2549: +NEW_SAVES="/pixelelated/Saves"
2550: +NEW_BACKUPS="/pixelelated/Backups"
2551: +NEW_CONTENT="/pixelelated/Content"
2552:  NEW_ROOT="${NEW_SAVES%/*}"   # the folder the tiers move into; named by the plan line below
2553:  # Every saves folder this project ever shipped as its default. A device whose
2554:  # saves folder is one of these is on a layout it never chose, so the move is
2555: @@ -69,6 +69,9 @@ SUPERSEDED_DEFAULT_SAVES=("/GAMES" "/ROCKNIX/Saves")
2556:  # is offered; written after a move or a seeding.
2557:  LAYOUT_VERSION=2
2558:  LAYOUT_MARKER=".layout"
2559: +REMOTE_LAYOUT=0
2560: +MIGRATION_RECORD="/storage/.config/cloud-layout-migration.json"
2561: +MIGRATION_ACTIVE=0
2562:  
2563:  # Which superseded default's saves folder holds files in this cloud, the
2564:  # configured one first, then the others newest first: into SOURCE_FOUND,
2565: @@ -106,12 +109,32 @@ earlier_source() { # <remote> [except]
2566:  # the first layout. Content goes with it only where this device's own was
2567:  # unset or the current default; a folder the player chose for ROMs stays
2568:  # theirs.
2569: +# An explicit empty CONTENT_REMOTE is the cloud root, not an unset option.
2570: +content_unset() { ! grep -q '^CONTENT_REMOTE=' "${SYNC_CONF}" 2>/dev/null; }
2571: +
2572: +# A pointer-only transition may follow an empty default backup tier, never
2573: +# abandon its archives or replace a custom folder. Called directly: failed
2574: +# listings terminate the caller through list_or_stop, not a subshell.
2575: +backup_pointer_for() { # <remote> <configured backups> <destination default>
2576: +    local remote="$1" backups="$2" target="$3" known=0
2577: +    NEXT_BACKUPS="${backups}"
2578: +    case "${backups%/}" in
2579: +        ""|/GAMES/backup|/ROCKNIX/Backups|/pixelelated/Backups) known=1 ;;
2580: +    esac
2581: +    [ "${known}" -eq 1 ] || return 0
2582: +    if [ -n "${backups}" ]; then
2583: +        list_or_stop "${remote}${backups%/}/" --files-only -R --include '*.{zip,tar.gz}'
2584: +        [ -n "${LISTING}" ] && return 0
2585: +    fi
2586: +    NEXT_BACKUPS="${target}"
2587: +}
2588: +
2589:  earlier_layout() { # <saves folder> <this device's content pointer>
2590:      local src="$1" content="$2" parent
2591:      parent="${src%/*}"; [ -n "${parent}" ] || parent="${src}"
2592:      E_SAVES="${src}"
2593:      if [ "${src}" = "/GAMES" ]; then E_BACKUPS="/GAMES/backup"; else E_BACKUPS="${parent}/Backups"; fi
2594: -    if [ -z "${content}" ] || same_folder "${content}" "${NEW_CONTENT}"; then
2595: +    if content_unset || same_folder "${content}" "${NEW_CONTENT}"; then
2596:          E_CONTENT="${parent}/Content"
2597:      else
2598:          E_CONTENT="${content}"
2599: @@ -372,7 +395,8 @@ SAVES_EXCLUDES=(--exclude '/backup/**' --exclude '/Backups/**')
2600:  has_files() { # <path> [more lsf arguments...]
2601:      local path="$1"
2602:      shift
2603: -    list_or_stop "${path}" --files-only -R "${SAVES_EXCLUDES[@]}" "$@"
2604: +    # The setup note is not a save and must not outrank another root's data.
2605: +    list_or_stop "${path}" --files-only -R "${SAVES_EXCLUDES[@]}" --exclude '/README.txt' "$@"
2606:      [ -n "${LISTING}" ]
2607:  }
2608:  
2609: @@ -543,9 +567,12 @@ relocate() { # <src> <dst> <what> <pointer key> [filter arguments...]
2610:      fi
2611:      say "Removing the old ${what} folder..."
2612:      [ "${MODE}" = "--apply" ] && echo ">>> doing remove"
2613: -    { rclone delete "${src}" --files-from-raw "${list}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2614: -        && rclone rmdirs "${src}" "${RCLONE_NET_OPTS_ARRAY[@]}"; } >/dev/null 2>&1 \
2615: -        || say "(could not remove the old folder; the copy is complete and verified)"
2616: +    if ! rclone delete "${src}" --files-from-raw "${list}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1; then
2617: +        say "The verified copy is in the new folder, but the old files couldn't be removed. Try again to finish."
2618: +        rm -f "${list}"
2619: +        return 1
2620: +    fi
2621: +    rclone rmdirs "${src}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1 || :
2622:      rm -f "${list}"
2623:      return 0
2624:  }
2625: @@ -609,9 +636,12 @@ merge_into() { # <src> <dst> <what> <pointer key> <list>
2626:      fi
2627:      say "Removing the old ${what} folder..."
2628:      [ "${MODE}" = "--apply" ] && echo ">>> doing remove"
2629: -    { rclone delete "${src}" --files-from-raw "${list}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
2630: -        && rclone rmdirs "${src}" "${RCLONE_NET_OPTS_ARRAY[@]}"; } >/dev/null 2>&1 \
2631: -        || say "(could not remove the old folder; the merge is complete and verified)"
2632: +    if ! rclone delete "${src}" --files-from-raw "${list}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1; then
2633: +        say "The merged files are in the new folder, but the old files couldn't be removed. Try again to finish."
2634: +        rm -f "${list}" "${differ}" "${missing}"
2635: +        return 1
2636: +    fi
2637: +    rclone rmdirs "${src}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1 || :
2638:      rm -f "${list}" "${differ}" "${missing}"
2639:      return 0
2640:  }
2641: @@ -636,7 +666,7 @@ set_pointer() { # <key> <remote path>
2642:          logger -t cloud_migrate_layout "could not write $1 to ${SYNC_CONF}; stopped before removing anything" 2>/dev/null
2643:          return 1
2644:      fi
2645: -    say "Now using ${2} for your $(tier_words "$1")."
2646: +    say "Now using ${2:-the root of your cloud} for your $(tier_words "$1")."
2647:  }
2648:  
2649:  # A tier as the player knows it (es-player-text.md: the four tiers), for
2650: @@ -683,6 +713,20 @@ derived_content() {
2651:      echo "${parent%/}/Content"
2652:  }
2653:  
2654: +# RC2 could finish its saves/backups moves before /GAMES/Content; run101
2655: +# could finish both pointers before its discarded/content tiers (#391).
2656: +# Only these exact earlier defaults are inherited derived content. A custom
2657: +# path ending in /Content is still the player's independent choice.
2658: +historical_content() {
2659: +    same_folder "$1" /GAMES/Content || same_folder "$1" /ROCKNIX/Content
2660: +}
2661: +
2662: +moving_content() { # <saves source> <content pointer>
2663: +    [ -n "$2" ] && ! same_folder "$2" "${NEW_CONTENT}" || return 1
2664: +    same_folder "$2" "$(derived_content "$(folder_abs "$1")")" && return 0
2665: +    { superseded_default "$1" || same_folder "$1" "${NEW_SAVES}"; } && historical_content "$2"
2666: +}
2667: +
2668:  # Move content to the current namespace if it is safe to, and repoint the
2669:  # config. Never merges into an existing destination -- that is the same
2670:  # interruptible half-migrated state the saves move refuses.
2671: @@ -747,7 +791,12 @@ migrate_content() {
2672:  #   CURRENT_EXISTS=0|1          whether the current default's saves folder lists
2673:  #   MARKER=layout=<n> | -       the cloud's marker, when one is there
2674:  layout_state() { # <remote> <saves> <backups> <content>
2675: -    local remote="$1" saves="$2" backups="$3" content="$4" state keep cur=0 marker
2676: +    local remote="$1" saves="$2" backups="$3" content="$4" state keep cur=0 marker old_replaced=""
2677: +    if [ -e "${MIGRATION_RECORD}" ]; then
2678: +        migration_record_load "${remote}" || return $?
2679: +        printf 'STATE=migration-pending\nSOURCE=%s\nCURRENT=%s\n' "${saves}" "${NEW_SAVES}"
2680: +        return 0
2681: +    fi
2682:      keep=$(conf_value LAYOUT_KEEP) || return 2
2683:      echo "SAVES=${saves}"
2684:      echo "BACKUPS=${backups}"
2685: @@ -758,12 +807,25 @@ layout_state() { # <remote> <saves> <backups> <content>
2686:      # while its saves sit in /ROCKNIX/Saves, made by its sibling on the
2687:      # fork's earlier build (the Retroid Pocket Nova, 2026-10-01): read from
2688:      # the conf alone it is "superseded, empty" and would be offered a fresh
2689: -    # /Rasteratops beside its real saves. So every default this project
2690: +    # /pixelelated beside its real saves. So every default this project
2691:      # once shipped is looked at, and the one holding files is the source
2692:      # the move is offered from (SOURCE=), the configured one or not.
2693:      local source=""
2694:      if same_folder "${saves}" "${NEW_SAVES}"; then
2695:          state=current
2696: +        # Older builds wrote no recovery record. Their current primary
2697: +        # pointers do not prove the derived content or discarded shelf moved.
2698: +        # This is a folder-page read, never an extra probe on a direct sync.
2699: +        if same_folder "${backups}" "${NEW_BACKUPS}"; then
2700: +            local earlier
2701: +            if historical_content "${content}"; then
2702: +                state=migration-pending
2703: +            else
2704: +                for earlier in "${SUPERSEDED_DEFAULT_SAVES[@]}"; do
2705: +                    if has_entries "${remote}${earlier}-replaced/"; then state=migration-pending; break; fi
2706: +                done
2707: +            fi
2708: +        fi
2709:      elif [ -n "${keep}" ] && same_folder "${saves}" "${keep}"; then
2710:          state=kept
2711:      elif superseded_default "${saves}"; then
2712: @@ -812,11 +874,12 @@ layout_follow() { # <remote> <saves> <backups> <content>
2713:      # (the futro's pre-mortem, 2026-10-01). The move is offered instead,
2714:      # which copies, verifies and only then removes.
2715:      has_files "${remote}${saves}/" && return 3
2716: +    backup_pointer_for "${remote}" "${backups}" "${NEW_BACKUPS}"
2717:      set_pointer SAVES_REMOTE "${NEW_SAVES}" || return 1
2718: -    set_pointer SETTINGS_REMOTE "${NEW_BACKUPS}" || return 1
2719: +    set_pointer SETTINGS_REMOTE "${NEXT_BACKUPS}" || return 1
2720:      # Content follows only where it was derived from the old folder or
2721:      # never set; a folder the player chose for ROMs stays theirs.
2722: -    if [ -z "${content}" ] || same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")" \
2723: +    if content_unset || same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")" \
2724:         || same_folder "${content}" "${saves%/}/Content"; then
2725:          set_pointer CONTENT_REMOTE "${NEW_CONTENT}" || return 1
2726:      fi
2727: @@ -853,8 +916,11 @@ layout_join() { # <remote> <saves> <content>
2728:      fi
2729:      earlier_source "${remote}" "${saves}" || return 3
2730:      earlier_layout "${SOURCE_FOUND}" "${content}"
2731: +    local backups
2732: +    backups=$(conf_value SETTINGS_REMOTE) || return 2
2733: +    backup_pointer_for "${remote}" "${backups}" "${E_BACKUPS}"
2734:      set_pointer SAVES_REMOTE "${E_SAVES}" || return 1
2735: -    set_pointer SETTINGS_REMOTE "${E_BACKUPS}" || return 1
2736: +    set_pointer SETTINGS_REMOTE "${NEXT_BACKUPS}" || return 1
2737:      set_pointer CONTENT_REMOTE "${E_CONTENT}" || return 1
2738:      say "Joined: this device now uses ${remote}${E_SAVES}, where your saves already are."
2739:      logger -t cloud_migrate_layout "joined the fleet at ${E_SAVES}: no saves in ${NEW_SAVES}" 2>/dev/null
2740: @@ -878,9 +944,10 @@ layout_settle() { # <remote> <saves> <backups> <content>
2741:      keep=$(conf_value LAYOUT_KEEP) || return 2
2742:      [ -n "${keep}" ] && same_folder "${saves}" "${keep}" && return 3
2743:      has_files "${remote}${saves}/" && return 3
2744: +    backup_pointer_for "${remote}" "${backups}" "${NEW_BACKUPS}"
2745:      set_pointer SAVES_REMOTE "${NEW_SAVES}" || return 1
2746: -    set_pointer SETTINGS_REMOTE "${NEW_BACKUPS}" || return 1
2747: -    if [ -z "${content}" ] || same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")" \
2748: +    set_pointer SETTINGS_REMOTE "${NEXT_BACKUPS}" || return 1
2749: +    if content_unset || same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")" \
2750:         || same_folder "${content}" "${saves%/}/Content"; then
2751:          set_pointer CONTENT_REMOTE "${NEW_CONTENT}" || return 1
2752:      fi
2753: @@ -894,15 +961,137 @@ layout_settle() { # <remote> <saves> <backups> <content>
2754:  # current folder with no marker is somebody's own folder of the same name,
2755:  # which the refusals below still protect.
2756:  fleet_made() { # <remote>
2757: -    rclone cat "${1}${NEW_SAVES%/*}/${LAYOUT_MARKER}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | head -1 | grep -q '^layout='
2758: +    [ "${REMOTE_LAYOUT}" = "${LAYOUT_VERSION}" ]
2759: +}
2760: +
2761: +# A marker is a version, not merely a prefix. Validate its complete bytes;
2762: +# shell substitution would silently discard NULs and trailing newlines. A
2763: +# failed read is not absence if the parent still lists the marker.
2764: +read_marker() { # <remote>
2765: +    local tmp rc version
2766: +    REMOTE_LAYOUT=0
2767: +    tmp=$(mktemp /tmp/cloud_layout_marker.XXXXXX) || return 5
2768: +    rclone cat "${1}${NEW_ROOT}/${LAYOUT_MARKER}" "${RCLONE_LIST_OPTS[@]}" > "${tmp}" 2>/dev/null; rc=$?
2769: +    if [ "${rc}" -ne 0 ]; then
2770: +        rm -f "${tmp}"
2771: +        list_or_stop "${1}${NEW_ROOT}/" --files-only
2772: +        if printf '%s\n' "${LISTING}" | grep -qFx -- "${LAYOUT_MARKER}"; then
2773: +            unreadable "${1}${NEW_ROOT}/${LAYOUT_MARKER}" "${rc}"
2774: +        fi
2775: +        return 0
2776: +    fi
2777: +    for version in 1 2; do
2778: +        if printf 'layout=%s\n' "${version}" | cmp -s - "${tmp}"; then
2779: +            REMOTE_LAYOUT="${version}"
2780: +            rm -f "${tmp}"
2781: +            return 0
2782: +        fi
2783: +    done
2784: +    rm -f "${tmp}"
2785: +    say "This cloud folder uses a layout this version can't read. No further changes were made. Check for a newer system version before trying again."
2786: +    [ "${MODE}" = "--apply" ] && echo ">>> why YOUR CLOUD FOLDER COULDN'T BE READ"
2787: +    logger -t cloud_migrate_layout "unsupported or malformed layout marker; refused" 2>/dev/null
2788: +    return 4
2789:  }
2790:  
2791:  write_marker() { # <remote>
2792: +    # Another device may have changed the marker while the tiers moved.
2793: +    read_marker "$1" || return $?
2794:      if printf 'layout=%s\n' "${LAYOUT_VERSION}" | rclone rcat "${1}${NEW_SAVES%/*}/${LAYOUT_MARKER}" "${RCLONE_NET_OPTS_ARRAY[@]}" 2>/dev/null; then
2795: +        read_marker "$1" || return $?
2796: +        [ "${REMOTE_LAYOUT}" = "${LAYOUT_VERSION}" ] || return 5
2797:          return 0
2798:      fi
2799: -    say "The layout marker could not be written; the folders moved all the same."
2800: +    say "Your files moved, but the cloud folder setup didn't finish. Try the move again to finish it."
2801: +    [ "${MODE}" = "--apply" ] && echo ">>> why SOME FILES DIDN'T FINISH"
2802:      logger -t cloud_migrate_layout "could not write ${LAYOUT_MARKER} at ${1}${NEW_SAVES%/*}" 2>/dev/null
2803: +    return 5
2804: +}
2805: +
2806: +# Local recovery state keeps the sources after their live pointers advance.
2807: +# It is never sourced as shell and never grants permission to merge a foreign
2808: +# destination. Each retry still verifies the actual cloud bytes. A record is
2809: +# bound to the remote configuration and the original/current pointer choices.
2810: +remote_fingerprint() {
2811: +    # rclone refreshes OAuth tokens during ordinary transfers. Bind the
2812: +    # configured provider/root, not that routinely changing credential.
2813: +    local config
2814: +    config=$(sed '/^[[:space:]]*token[[:space:]]*=/d' /storage/.config/rclone/rclone.conf) || return 1
2815: +    printf '%s\n' "${config}" | sha256sum
2816: +}
2817: +
2818: +migration_record_save() {
2819: +    migration_record_write "$@" && return 0
2820: +    say "Couldn't save the cloud move's progress on this device. Try again when storage is available."
2821: +    [ "${MODE}" = "--apply" ] && echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED"
2822: +    return 5
2823: +}
2824: +
2825: +migration_record_write() { # <stage>; consumes the calling step's local paths
2826: +    local stage="$1" tmp fingerprint
2827: +    fingerprint=$(remote_fingerprint) || return 5
2828: +    fingerprint="${fingerprint%% *}"
2829: +    tmp=$(mktemp "${MIGRATION_RECORD}.XXXXXX" 2>/dev/null) || return 5
2830: +    if [ "${MIGRATION_ACTIVE}" = 1 ]; then
2831: +        jq --arg stage "${stage}" '.stage=$stage' "${MIGRATION_RECORD}" > "${tmp}"
2832: +    else
2833: +        jq -n --arg remote "${remote}" --arg fingerprint "${fingerprint}" \
2834: +            --arg saves "${saves}" --arg backups "${backups}" --arg content "${content}" \
2835: +            --arg discarded "${old_replaced}" \
2836: +            --arg cs "$(conf_value SAVES_REMOTE)" --arg cb "$(conf_value SETTINGS_REMOTE)" \
2837: +            --arg cc "$(conf_value CONTENT_REMOTE)" --arg stage "${stage}" \
2838: +            '{schema:1,step:1,from:1,to:2,remote:$remote,fingerprint:$fingerprint,
2839: +              source:{saves:$saves,backups:$backups,content:$content,discarded:$discarded},
2840: +              configured:{saves:$cs,backups:$cb,content:$cc},stage:$stage}' > "${tmp}"
2841: +    fi
2842: +    if [ "$?" -ne 0 ] || ! sync || ! mv -f "${tmp}" "${MIGRATION_RECORD}" || ! sync; then
2843: +        rm -f "${tmp}"
2844: +        return 5
2845: +    fi
2846: +    MIGRATION_ACTIVE=1
2847: +    logger -t cloud_migrate_layout "migration step=1 from=1 to=2 stage=${stage}" 2>/dev/null
2848: +    return 0
2849: +}
2850: +
2851: +migration_record_load() { # <remote>; restores the calling step's source paths
2852: +    [ -e "${MIGRATION_RECORD}" ] || return 0
2853: +    local fingerprint key live initial target value
2854: +    fingerprint=$(remote_fingerprint) || return 5
2855: +    fingerprint="${fingerprint%% *}"
2856: +    if ! jq -e --arg remote "$1" --arg fingerprint "${fingerprint}" '
2857: +        .schema==1 and .step==1 and .from==1 and .to==2 and
2858: +        .remote==$remote and .fingerprint==$fingerprint and
2859: +        ([.source.saves,.source.backups,.source.content,
2860: +          .configured.saves,.configured.backups,.configured.content] |
2861: +          all(.[]; type=="string" and (explode | all(.[]; .>=32)))) and
2862: +        ((.source | has("discarded") | not) or
2863: +          (.source.discarded | type=="string" and (explode | all(.[]; .>=32))))
2864: +        ' "${MIGRATION_RECORD}" >/dev/null 2>&1; then
2865: +        say "The previous cloud move couldn't be read safely. Nothing more was changed."
2866: +        return 5
2867: +    fi
2868: +    for key in saves backups content; do
2869: +        case "${key}" in
2870: +            saves) live=$(conf_value SAVES_REMOTE); target="${NEW_SAVES}" ;;
2871: +            backups) live=$(conf_value SETTINGS_REMOTE); target="${NEW_BACKUPS}" ;;
2872: +            content) live=$(conf_value CONTENT_REMOTE); target="${NEW_CONTENT}" ;;
2873: +        esac
2874: +        initial=$(jq -r --arg k "${key}" '.configured[$k]' "${MIGRATION_RECORD}") || return 5
2875: +        if ! same_folder "${live}" "${initial}" && ! same_folder "${live}" "${target}"; then
2876: +            say "Your cloud folder choices changed during the move. Nothing more was changed."
2877: +            return 5
2878: +        fi
2879: +        value=$(jq -r --arg k "${key}" '.source[$k]' "${MIGRATION_RECORD}") || return 5
2880: +        value=$(clean_path "${value}") || return 5
2881: +        printf -v "${key}" '%s' "${value}"
2882: +    done
2883: +    # Optional in schema1: records written before #391 derive this shelf
2884: +    # from their retained saves source. New records keep it independently,
2885: +    # so recovering an old shelf never reselects a live saves folder.
2886: +    value=$(jq -r '.source.discarded // (.source.saves | rtrimstr("/") + "-replaced")' "${MIGRATION_RECORD}") || return 5
2887: +    old_replaced=$(clean_path "${value}") || return 5
2888: +    MIGRATION_ACTIVE=1
2889: +    logger -t cloud_migrate_layout "migration step=1 from=1 to=2 resume" 2>/dev/null
2890:      return 0
2891:  }
2892:  
2893: @@ -979,6 +1168,12 @@ main() {
2894:          printf -v "${ptr}" '%s' "${cleaned}"
2895:      done
2896:  
2897: +    # All default-layout transitions share the version boundary, including
2898: +    # seeding through --settle. A custom layout elsewhere is independent.
2899: +    if superseded_default "${saves}" || same_folder "${saves}" "${NEW_SAVES}"; then
2900: +        read_marker "${remote}" || return $?
2901: +    fi
2902: +
2903:      # A layout the owner chose is current too. CHANGE CLOUD FOLDER writes the
2904:      # settings and content folders as SIBLINGS of the saves folder -- the
2905:      # parent's Backups and Content, or the folder's own when it sits at the
2906: @@ -987,14 +1182,41 @@ main() {
2907:      # as current, so this check offered to move a deliberately chosen layout
2908:      # back to the default one (#74). The nested first layout, backups INSIDE
2909:      # the saves folder, is the only shape this tool exists to move.
2910: +    if [ -e "${MIGRATION_RECORD}" ]; then
2911: +        case "${mode}" in
2912: +            --join|--follow) return 3 ;; # The explicit retry owns the remaining move.
2913: +            --settle|--keep|--write-marker)
2914: +                say "The cloud folder move hasn't finished. Try the move again to finish it."
2915: +                return 5 ;;
2916: +        esac
2917: +    fi
2918:      case "${mode}" in
2919:          --state)  layout_state "${remote}" "${saves}" "${backups}" "${content}"; return $? ;;
2920:          --keep)   layout_keep "${saves}"; return $? ;;
2921:          --follow) layout_follow "${remote}" "${saves}" "${backups}" "${content}"; return $? ;;
2922:          --join)   layout_join "${remote}" "${saves}" "${content}"; return $? ;;
2923:          --settle) layout_settle "${remote}" "${saves}" "${backups}" "${content}"; return $? ;;
2924: +        --write-marker)
2925: +            # Seeding must not declare an unfinished local move complete.
2926: +            [ ! -e "${MIGRATION_RECORD}" ] || return 5
2927: +            same_folder "${saves}" "${NEW_SAVES}" || return 3
2928: +            write_marker "${remote}"; return $? ;;
2929:      esac
2930:  
2931: +    # Step 1 is the supported predecessor (unmarked/layout 1) to layout 2.
2932: +    # A layout-2 fleet may still have an older device's files to move, so
2933: +    # marker 2 does not skip that device's step. Later versions must add an
2934: +    # explicit dispatcher entry; read_marker refuses them in this build.
2935: +    case "${REMOTE_LAYOUT}" in
2936: +        0|1|2) migration_step_1 "${remote}" "${saves}" "${backups}" "${content}" "${mode}" ;;
2937: +        *) return 4 ;;
2938: +    esac
2939: +}
2940: +
2941: +migration_step_1() {
2942: +    local remote="$1" saves="$2" backups="$3" content="$4" mode="$5" old_replaced=""
2943: +    migration_record_load "${remote}" || return $?
2944: +
2945:      local sabs sib_parent
2946:      sabs=$(folder_abs "${saves}")
2947:      sib_parent="${sabs%/*}"; [ -n "${sib_parent}" ] || sib_parent="${sabs}"
2948: @@ -1003,32 +1225,33 @@ main() {
2949:      # earlier default and is offered the move (D-CLOUD-160).
2950:      if ! superseded_default "${saves}" \
2951:         && ! same_folder "${saves}" "${NEW_SAVES}" && same_folder "${backups}" "${sib_parent}/Backups"; then
2952: -        if [ -z "${content}" ] || same_folder "${content}" "${sib_parent}/Content"; then
2953: +        if content_unset || same_folder "${content}" "${sib_parent}/Content"; then
2954:              say "Already on a sibling layout of your own (${saves}, ${backups}); nothing to move."
2955:              return 3
2956:          fi
2957:      fi
2958:  
2959: -    if same_folder "${saves}" "${NEW_SAVES}" && same_folder "${backups}" "${NEW_BACKUPS}"; then
2960: -        # Saves and backups are current, but a device migrated before
2961: -        # CONTENT_REMOTE was carried along is still pointing its ROMs at the old
2962: -        # namespace. Repair that here rather than making it a separate flow --
2963: -        # this is the state every early migration left behind.
2964: -        # The old SAVES_REMOTE is gone by now, so the derived value cannot be
2965: -        # recomputed. The signature is enough: the helper always appends
2966: -        # "/Content", so a path shaped that way and not already the current
2967: -        # one is one of ours, left behind.
2968: -        if [ -n "${content}" ] && ! same_folder "${content}" "${NEW_CONTENT}"; then
2969: -            case "${content}" in
2970: -                */Content)
2971: -                    say "Saves and backups are current, but content still points at ${remote}${content}."
2972: -                    migrate_content "${remote}" "${content}"  "${mode}"
2973: -                    return $?
2974: -                ;;
2975: -            esac
2976: +    if [ "${MIGRATION_ACTIVE}" = 0 ] && same_folder "${saves}" "${NEW_SAVES}" \
2977: +       && same_folder "${backups}" "${NEW_BACKUPS}"; then
2978: +        # The live primary pointers are authoritative. Another device may
2979: +        # still write old saves/backups: only the retained content pointer
2980: +        # and an owned discarded shelf are eligible for this recovery.
2981: +        local earlier
2982: +        for earlier in "${SUPERSEDED_DEFAULT_SAVES[@]}"; do
2983: +            if has_entries "${remote}${earlier}-replaced/"; then
2984: +                old_replaced="${earlier}-replaced"; break
2985: +            fi
2986: +        done
2987: +        if [ -z "${old_replaced}" ] && ! moving_content "${saves}" "${content}"; then
2988: +            # An older build may have stopped just before publication. An
2989: +            # explicit apply finishes that marker without inventing a move
2990: +            # or rewriting equivalent pointer spellings (PL-001).
2991: +            if [ "${mode}" = "--apply" ] && [ "${REMOTE_LAYOUT}" != "${LAYOUT_VERSION}" ]; then
2992: +                write_marker "${remote}" || return $?
2993: +            fi
2994: +            say "Already on the current layout (${NEW_SAVES}, ${NEW_BACKUPS})."
2995: +            return 3
2996:          fi
2997: -        say "Already on the current layout (${NEW_SAVES}, ${NEW_BACKUPS})."
2998: -        return 3
2999:      fi
3000:  
3001:      # The move starts from the folder that holds the saves. A device whose
3002: @@ -1038,25 +1261,25 @@ main() {
3003:      # folder -- a setting, nothing copied -- and then moved from it like
3004:      # any other. Backups and content are taken as that layout's siblings
3005:      # (or the nested /GAMES/backup for the first layout).
3006: -    if superseded_default "${saves}" && ! has_files "${remote}${saves}/"; then
3007: +    if [ "${MIGRATION_ACTIVE}" = 0 ] && superseded_default "${saves}" && ! has_files "${remote}${saves}/"; then
3008:          local src
3009:          superseded_source "${remote}" "${saves}"; src="${SOURCE_FOUND}"
3010:          if [ -n "${src}" ] && ! same_folder "${src}" "${saves}"; then
3011:              say "Your saves are in ${remote}${src}, not in ${remote}${saves} as this device was set; moving from there."
3012:              local src_parent="${src%/*}"; [ -n "${src_parent}" ] || src_parent="${src}"
3013: -            if [ "${mode}" = "--apply" ]; then
3014: -                set_pointer SAVES_REMOTE "${src}" || return 5
3015: -                if [ "${src}" = "/GAMES" ]; then set_pointer SETTINGS_REMOTE "/GAMES/backup" || return 5
3016: -                else set_pointer SETTINGS_REMOTE "${src_parent}/Backups" || return 5; fi
3017: -                [ -z "${content}" ] && { set_pointer CONTENT_REMOTE "${src_parent}/Content" || return 5; content="${src_parent}/Content"; }
3018: -            fi
3019: +            local src_backups="${src_parent}/Backups"
3020: +            [ "${src}" = "/GAMES" ] && src_backups="/GAMES/backup"
3021: +            backup_pointer_for "${remote}" "${backups}" "${src_backups}"
3022: +            # Select sources here; publish pointers only after verified
3023: +            # copies, with the recovery record already retained below.
3024:              saves="${src}"
3025: -            if [ "${src}" = "/GAMES" ]; then backups="/GAMES/backup"; else backups="${src_parent}/Backups"; fi
3026: -            [ -z "${content}" ] && content="${src_parent}/Content"
3027: +            backups="${NEXT_BACKUPS}"
3028: +            content_unset && content="${src_parent}/Content"
3029:              sabs=$(folder_abs "${saves}")
3030:              sib_parent="${sabs%/*}"; [ -n "${sib_parent}" ] || sib_parent="${sabs}"
3031:          fi
3032:      fi
3033: +    [ -n "${old_replaced}" ] || old_replaced="${sabs%/}-replaced"
3034:  
3035:      say "This device stores:"
3036:      say "  saves    ${remote}${saves}"
3037: @@ -1129,6 +1352,14 @@ main() {
3038:              blocked=1
3039:          fi
3040:      fi
3041: +    if ! same_folder "${old_replaced}" "${NEW_SAVES}-replaced" && has_entries "${remote}${old_replaced}/" \
3042: +       && exists "${remote}${NEW_SAVES}-replaced" \
3043: +       && ! resumable "${remote}${old_replaced}" "${remote}${NEW_SAVES}-replaced"; then
3044: +        if fleet_made "${remote}"; then merging=1; else
3045: +            say "REFUSING: ${remote}${NEW_SAVES}-replaced already exists."
3046: +            blocked=1
3047: +        fi
3048: +    fi
3049:      if [ "${blocked}" = "1" ]; then
3050:          [ "${mode}" = "--apply" ] && echo ">>> why THE NEW FOLDER ALREADY HAS FILES IN IT"
3051:          return 4
3052: @@ -1150,16 +1381,13 @@ main() {
3053:      # (<saves>-replaced, cloud_backup's) is ours and travels with the saves
3054:      # (D-CLOUD-165): to a player the change is a renamed shelf, not a new
3055:      # one, and nothing of ours stays under the old name.
3056: -    local old_replaced="${saves%/}-replaced"
3057: -    if ! same_folder "${saves}" "${NEW_SAVES}" && has_entries "${remote}${old_replaced}/"; then
3058: +    if ! same_folder "${old_replaced}" "${NEW_SAVES}-replaced" && has_entries "${remote}${old_replaced}/"; then
3059:          say "  ${remote}${old_replaced}  ->  ${remote}${NEW_SAVES}-replaced"; plan="${plan:+${plan},}discarded"
3060:      fi
3061:      # The content folder derived beside the saves moves too (the same test
3062:      # the items count makes below). It was moved and never listed here, so
3063:      # the hub's preview said less than --apply did (2026-10-01).
3064: -    if [ -n "${content}" ] && ! same_folder "${content}" "${NEW_CONTENT}" \
3065: -       && same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")" \
3066: -       && has_entries "${remote}${content}/"; then
3067: +    if moving_content "${saves}" "${content}" && has_entries "${remote}${content}/"; then
3068:          say "  ${remote}${content}  ->  ${remote}${NEW_CONTENT}"; plan="${plan:+${plan},}content"
3069:      fi
3070:  
3071: @@ -1168,7 +1396,7 @@ main() {
3072:          # what moves and where): the tiers holding files, in move order --
3073:          # backups, saves, discarded, content -- or none when only a setting
3074:          # would change. The row named /ROCKNIX on a build whose folder is
3075: -        # /Rasteratops until this line existed (2026-10-01).
3076: +        # /pixelelated until this line existed (2026-10-01).
3077:          echo ">>> plan ${plan:-none} ${NEW_ROOT}"
3078:          say ""
3079:          say "Nothing has been changed. Run with --apply to do it."
3080: @@ -1176,6 +1404,7 @@ main() {
3081:      fi
3082:  
3083:      say ""
3084: +    migration_record_save begin || return $?
3085:      # What moves, counted before anything does, so the page reads ITEM 1 OF n
3086:      # from the first announcement (D-UI-026); each tier announces itself in
3087:      # the page's own words as its move begins. A tier with nothing stored
3088: @@ -1183,10 +1412,8 @@ main() {
3089:      local items=0 item=0
3090:      ! same_folder "${backups}" "${NEW_BACKUPS}" && has_entries "${remote}${backups}/" && items=$((items + 1))
3091:      ! same_folder "${saves}" "${NEW_SAVES}" && has_files "${remote}${saves_src}/" && items=$((items + 1))
3092: -    ! same_folder "${saves}" "${NEW_SAVES}" && has_entries "${remote}${old_replaced}/" && items=$((items + 1))
3093: -    [ -n "${content}" ] && ! same_folder "${content}" "${NEW_CONTENT}" \
3094: -       && same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")" \
3095: -       && has_entries "${remote}${content}/" && items=$((items + 1))
3096: +    ! same_folder "${old_replaced}" "${NEW_SAVES}-replaced" && has_entries "${remote}${old_replaced}/" && items=$((items + 1))
3097: +    moving_content "${saves}" "${content}" && has_entries "${remote}${content}/" && items=$((items + 1))
3098:      announce() { item=$((item + 1)); echo ">>> unit $1|${item}|${items}"; }
3099:      # The backups first (PL-025). In the original layout they sit inside the
3100:      # saves folder; moved first, they are out of it before the saves move
3101: @@ -1207,6 +1434,7 @@ main() {
3102:          fi
3103:      fi
3104:  
3105: +    migration_record_save backups || return $?
3106:      local moved_saves=0
3107:      if ! same_folder "${saves}" "${NEW_SAVES}"; then
3108:          if has_files "${remote}${saves_src}/"; then
3109: @@ -1216,17 +1444,15 @@ main() {
3110:          else
3111:              set_pointer SAVES_REMOTE "${NEW_SAVES}" || return 5
3112:          fi
3113: -        # A content pointer at the cloud's root (empty, the shape a stock
3114: -        # conf carries up: the Nova's, 2026-09-30) is a value nobody chose,
3115: -        # and left alone it put the seeded ROMs and BIOS folders at the root
3116: -        # of the cloud beside /Rasteratops (guest d, 2026-10-01, case B). It
3117: -        # follows the saves to the current layout, as --follow's does.
3118: -        if [ -z "${content}" ]; then
3119: +        # Only a missing content choice follows automatically. An explicit
3120: +        # empty value selects the cloud root and must survive the move (#380).
3121: +        if content_unset; then
3122:              set_pointer CONTENT_REMOTE "${NEW_CONTENT}" || return 5
3123:              content="${NEW_CONTENT}"
3124:          fi
3125:      fi
3126: -    if ! same_folder "${saves}" "${NEW_SAVES}" && has_entries "${remote}${old_replaced}/"; then
3127: +    migration_record_save saves || return $?
3128: +    if ! same_folder "${old_replaced}" "${NEW_SAVES}-replaced" && has_entries "${remote}${old_replaced}/"; then
3129:          announce "DISCARDED SAVES"
3130:          if ! relocate "${remote}${old_replaced}" "${remote}${NEW_SAVES}-replaced" "discarded saves" ""; then
3131:              say "Your discarded saves didn't finish moving; they are still at ${remote}${old_replaced}. Try again."
3132: @@ -1234,6 +1460,7 @@ main() {
3133:          fi
3134:      fi
3135:  
3136: +    migration_record_save discarded || return $?
3137:      # ROMs move with the saves they belong to, when the pointer is one we
3138:      # derived. A CONTENT_REMOTE the owner set themselves is theirs, and stays.
3139:      # Its result is the run's (audit #307 PL-071): a content move that was
3140: @@ -1243,8 +1470,7 @@ main() {
3141:      # Compared as folders, and never onto itself (PL-001): a saves folder at
3142:      # /ROCKNIX derives /ROCKNIX/Content, the new folder itself, which the
3143:      # string compare sent through the move and so onto itself.
3144: -    if [ -n "${content}" ] && ! same_folder "${content}" "${NEW_CONTENT}" \
3145: -       && same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")"; then
3146: +    if moving_content "${saves}" "${content}"; then
3147:          has_entries "${remote}${content}/" && announce "ROMS, BIOS, AND GAME CONTENT"
3148:          migrate_content "${remote}" "${content}" "${mode}" || content_rc=$?
3149:      elif [ -n "${content}" ] && ! same_folder "${content}" "${NEW_CONTENT}"; then
3150: @@ -1256,7 +1482,11 @@ main() {
3151:          say "Saves are at ${remote}${NEW_SAVES} and backups at ${remote}${NEW_BACKUPS}, but your ROMs and BIOS files didn't move. Try again."
3152:          return "${content_rc}"
3153:      fi
3154: -    write_marker "${remote}"
3155: +    migration_record_save content || return $?
3156: +    write_marker "${remote}" || return $?
3157: +    migration_record_save complete || return $?
3158: +    rm -f "${MIGRATION_RECORD}" || return 5
3159: +    sync || return 5
3160:      say "Done. Saves are at ${remote}${NEW_SAVES}, backups at ${remote}${NEW_BACKUPS}."
3161:      [ "${moved_saves}" = "1" ] && say "Old folders were left in place if anything else was in them."
3162:      return 0
3163: @@ -1276,8 +1506,20 @@ if [ "${1:-}" = "--superseded" ]; then printf '%s\n' "${SUPERSEDED_DEFAULT_SAVES
3164:  # every boot for nothing. The scripts write the defaults in their own case.
3165:  if [ "${1:-}" = "--needs-step" ]; then
3166:      CASE_INSENSITIVE=0
3167: +    if [ -e "${MIGRATION_RECORD}" ]; then
3168: +        grep -q '^\[' /storage/.config/rclone/rclone.conf 2>/dev/null || exit 1
3169: +        exit 0
3170: +    fi
3171:      _saves=$(conf_value SAVES_REMOTE) || exit 2
3172:      _keep=$(conf_value LAYOUT_KEEP) || exit 2
3173: +    if same_folder "${_saves}" "${NEW_SAVES}"; then
3174: +        _backups=$(conf_value SETTINGS_REMOTE) || exit 2
3175: +        _content=$(conf_value CONTENT_REMOTE) || exit 2
3176: +        if same_folder "${_backups}" "${NEW_BACKUPS}" && historical_content "${_content}"; then
3177: +            grep -q '^\[' /storage/.config/rclone/rclone.conf 2>/dev/null || exit 1
3178: +            exit 0
3179: +        fi
3180: +    fi
3181:      superseded_default "${_saves}" || exit 1
3182:      [ -n "${_keep}" ] && same_folder "${_saves}" "${_keep}" && exit 1
3183:      grep -q '^\[' /storage/.config/rclone/rclone.conf 2>/dev/null || exit 1
3184: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth b/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth
3185: index 71e5822f5a..f1031e9308 100755
3186: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth
3187: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth
3188: @@ -730,7 +730,7 @@ document.querySelector("input[name=code]").addEventListener("paste", function ()
3189:  # rather than carried in the address. Scanning the QR skips this page, because
3190:  # the QR encodes the PIN.
3191:  PIN_PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
3192: -<title>ROCKNIX cloud sign-in</title>
3193: +<title>pixelelated cloud sign-in</title>
3194:  <style>%(style)s</style>
3195:  <div class=card>
3196:  <h1>Almost there</h1>
3197: @@ -1026,7 +1026,7 @@ window.onerror = function (message) {
3198:    var state = document.getElementById("state");
3199:    if (!state) return;
3200:    state.className = "err";
3201: -  state.textContent = "This page stopped working. Reload it; if it happens again, tell the ROCKNIX team: " + message;
3202: +  state.textContent = "This page stopped working. Reload it; if it happens again, report it to the pixelelated project: " + message;
3203:  };
3204:  (function () {
3205:    var pin = "%(pin)s";
3206: @@ -1508,7 +1508,7 @@ class RemoteKeyboard:
3207:                  fcntl.ioctl(fd, UI_SET_KEYBIT, code)
3208:              # struct uinput_user_dev: name[80], id{bustype,vendor,product,
3209:              # version}, ff_effects_max, then the absmin/max/fuzz/flat arrays.
3210: -            name = b"ROCKNIX cloud sign-in".ljust(80, b"\0")
3211: +            name = b"pixelelated cloud sign-in".ljust(80, b"\0")
3212:              os.write(fd, name + struct.pack("HHHHi", 0x03, 0x1209, 0x0001, 1, 0)
3213:                       + b"\0" * (4 * 64 * 4))
3214:              fcntl.ioctl(fd, UI_DEV_CREATE)
3215: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore b/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore
3216: index 8d69566c5d..67ce8b2a25 100755
3217: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore
3218: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore
3219: @@ -793,12 +793,20 @@ outcome_word() {
3220:  # Whether the cloud is bucket-based (S3 and compatibles, GCS, Swift, B2):
3221:  # rclone's own word, asked once, locally.
3222:  BUCKET_BASED=""
3223: +# Return 0 for bucket, 1 for path, 2 when the provider could not answer.
3224: +# Only a successful features read is cached; a failed read stays retriable.
3225:  bucket_based() {
3226: +    local features
3227:      if [ -z "${BUCKET_BASED}" ]; then
3228: -        if rclone backend features "${REMOTENAME}" 2>/dev/null | grep -q '"BucketBased": *true'; then
3229: +        features=$(rclone backend features "${REMOTENAME}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); BUCKET_READ_RC=$?
3230: +        [ "${BUCKET_READ_RC}" -eq 0 ] || return 2
3231: +        if printf '%s\n' "${features}" | grep -q '"BucketBased": *true'; then
3232:              BUCKET_BASED=1
3233: -        else
3234: +        elif printf '%s\n' "${features}" | grep -q '"BucketBased": *false'; then
3235:              BUCKET_BASED=0
3236: +        else
3237: +            BUCKET_READ_RC=1
3238: +            return 2
3239:          fi
3240:      fi
3241:      [ "${BUCKET_BASED}" = "1" ]
3242: @@ -808,12 +816,19 @@ bucket_based() {
3243:  # marker or by objects under it. The remote's root always exists; a bucket
3244:  # is listed at the root. Listing the folder itself proves nothing there
3245:  # (#141), so this never does.
3246: +# Return 0 present, 1 absent, 2 unknown. The caller must never turn 2
3247: +# into a create-folder offer. Preserve the provider's error for reporting.
3248:  bucket_dir_listed() {
3249: -    local path="${1%/}" parent name
3250: +    local path="${1%/}" parent name listing
3251:      name="${path##*/}"
3252:      [ -n "${name}" ] || return 0
3253:      parent="${path%/*}"
3254: -    rclone lsf --dirs-only "${REMOTENAME}${parent}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -qx "${name}/"
3255: +    # This is a directory query. The trailing slash avoids WebDAV's extra
3256: +    # file-type probe before listing, while retaining the same three-way
3257: +    # presence result (#364); no absence result is cached between runs.
3258: +    listing=$(rclone lsf --dirs-only "${REMOTENAME}${parent%/}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); BUCKET_READ_RC=$?
3259: +    [ "${BUCKET_READ_RC}" -eq 0 ] || return 2
3260: +    printf '%s\n' "${listing}" | grep -qxF -- "${name}/"
3261:  }
3262:  
3263:  why_for() {
3264: @@ -1488,14 +1503,6 @@ device_label() {
3265:      [ -n "${tool}" ] && "${tool}" --label 2>/dev/null | tr -cd 'A-Za-z0-9_-'
3266:  }
3267:  
3268: -# Does a cloud folder hold a settings archive at its top level? The same
3269: -# match the transfer below uses, so a folder this says yes to is one the
3270: -# restore can take from. Anything else -- unreachable, absent, only
3271: -# subfolders -- is no.
3272: -folder_has_archives() {
3273: -    rclone lsf "${1}/" --include "/*.{zip,tar.gz}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -q .
3274: -}
3275: -
3276:  # The OS name the archive's name ends with. backuptool has OS_NAME from
3277:  # /etc/profile; this script is started by systemd and by EmulationStation,
3278:  # where no profile has run, so it is read from the file the profile reads it
3279: @@ -1673,9 +1680,19 @@ restore_game_saves() {
3280:      # and the same rule judges the parent below, which is how a mistyped
3281:      # root fails on a bucket exactly as on a path-based cloud (2026-09-12,
3282:      # the maintainer's marker question). The features call is local.
3283: -    if [ ${remote_check_status} -eq 0 ] && bucket_based && ! bucket_dir_listed "${SAVES_REMOTE}"; then
3284: -        log_message "bucket-based cloud: ${SAVES_REMOTE} is not listed by its parent (no marker, no objects), which on a bucket is the folder not existing" "false"
3285: -        remote_check_status=3
3286: +    local remote_presence_unknown=0
3287: +    if [ "${remote_check_status}" -eq 0 ]; then
3288: +        local bucket_rc
3289: +        bucket_based; bucket_rc=$?
3290: +        if [ "${bucket_rc}" -eq 0 ]; then
3291: +            bucket_dir_listed "${SAVES_REMOTE}"; bucket_rc=$?
3292: +            case "${bucket_rc}" in
3293: +                1) remote_check_status=3 ;;
3294: +                2) remote_check_status="${BUCKET_READ_RC}"; remote_presence_unknown=1 ;;
3295: +            esac
3296: +        elif [ "${bucket_rc}" -eq 2 ]; then
3297: +            remote_check_status="${BUCKET_READ_RC}"; remote_presence_unknown=1
3298: +        fi
3299:      fi
3300:      if [ $remote_check_status -ne 0 ]; then
3301:          network_lost_during_run "$remote_check_status" "the saves restore"
3302: @@ -1709,8 +1726,19 @@ restore_game_saves() {
3303:          local saves_parent="${saves_path%/*}"
3304:          [ "${saves_parent}" = "${saves_path}" ] && saves_parent=""
3305:          local missing_name="${saves_path##*/}"
3306: -        if rclone lsd "${REMOTENAME}${saves_parent}" "${RCLONE_LIST_OPTS[@]}" >/dev/null 2>&1 \
3307: -           && { ! bucket_based || bucket_dir_listed "${saves_parent}"; }; then
3308: +        # Only a proved missing folder can lead to a creation offer. A
3309: +        # timeout/permission failure on the child remains a failure even if
3310: +        # its parent happens to answer the next request.
3311: +        local parent_present=0 parent_kind
3312: +        if [ "${remote_presence_unknown}" -eq 0 ] && { [ "${remote_check_status}" -eq 3 ] || [ "${remote_check_status}" -eq 4 ]; } \
3313: +           && rclone lsd "${REMOTENAME}${saves_parent}" "${RCLONE_LIST_OPTS[@]}" >/dev/null 2>&1; then
3314: +            bucket_based; parent_kind=$?
3315: +            case "${parent_kind}" in
3316: +                1) parent_present=1 ;;
3317: +                0) bucket_dir_listed "${saves_parent}" && parent_present=1 ;;
3318: +            esac
3319: +        fi
3320: +        if [ "${parent_present}" -eq 1 ]; then
3321:              local near
3322:              near=$(rclone lsf --dirs-only "${REMOTENAME}${saves_parent}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null \
3323:                     | sed 's|/$||' | near_names "${missing_name}" | head -1)
3324: @@ -2015,77 +2043,32 @@ restore_system_files() {
3325:          # SETTINGS_REMOTE, and they are still someone's only backup -- a device
3326:          # that upgrades must keep finding them. Nothing is moved or deleted:
3327:          # the root copy may belong to another device that has not updated yet.
3328: -        local own_name device_src legacy_src restore_src=""
3329: -        own_name=$(device_folder)
3330: -        device_src="${REMOTENAME}${SETTINGS_REMOTE}/${own_name}"
3331: -        legacy_src="${REMOTENAME}${SETTINGS_REMOTE}"
3332: -
3333: -        # The folder this device would have used before the name became
3334: -        # readable. An existing device keeps its stored identity and never
3335: -        # moves, but a reflashed one regenerates -- which is the point of
3336: -        # seeding from the hardware address -- and under the new rule it
3337: -        # generates a different name. Without this it would find nothing and
3338: -        # report that it has no backup, while its backups sat one folder away.
3339: -        local prior_name="" id_tool
3340: +        local restore_src="" legacy_src="${REMOTENAME}${SETTINGS_REMOTE}" id_tool archive_tool archive_rc
3341:          id_tool=$(device_id_tool)
3342: -        [ -n "${id_tool}" ] && prior_name=$("${id_tool}" --legacy 2>/dev/null \
3343: -                                            | tr -cd 'A-Za-z0-9_.-')
3344: -        local prior_src="${REMOTENAME}${SETTINGS_REMOTE}/${prior_name}"
3345: -
3346: -        # The folders this device may have written under while its id ended
3347: -        # in the shared constant (#86): until 2026-09-08 every device whose
3348: -        # kernel builds in the sit tunnel hashed the same string, so the RG SP
3349: -        # backed up to Anbernic-RG-SP-ee5013fc56 and the RG35XX SP to
3350: -        # ROCKNIX-ee5013fc56. cloud_device_id heals such an id on the first
3351: -        # run that sees a real hardware address and lists the old names under
3352: -        # --previous; the archives are still there, and still someone's only
3353: -        # backup. Nothing is moved: the same name was produced by every device
3354: -        # of that model or hostname, so a folder here may hold another
3355: -        # device's archives too, and the log says so when one is taken.
3356: -        local previous_names=""
3357: -        [ -n "${id_tool}" ] && previous_names=$("${id_tool}" --previous 2>/dev/null \
3358: -                                                | tr -cd 'A-Za-z0-9_.\n-')
3359: -
3360: -        # In order: this device's own folder, its pre-label name, the folders
3361: -        # it was healed away from, and the root where archives sat before
3362: -        # folders existed. The first that holds an archive wins.
3363: -        if folder_has_archives "${device_src}"; then
3364: -            restore_src="${device_src}"
3365: -            log_message "Restoring from this device's own cloud folder (${own_name})" "false"
3366: -        fi
3367: -        if [ -z "${restore_src}" ] && [ -n "${prior_name}" ] && folder_has_archives "${prior_src}"; then
3368: -            restore_src="${prior_src}"
3369: -            log_message "Using the backups saved under this device's old name (${prior_name})." "true"
3370: -        fi
3371: -        if [ -z "${restore_src}" ] && [ -n "${previous_names}" ]; then
3372: -            local previous_name
3373: -            while IFS= read -r previous_name; do
3374: -                [ -n "${previous_name}" ] || continue
3375: -                # Already tried above. A cloud_device_id from before --previous
3376: -                # existed answers it with the current id, so this also keeps
3377: -                # an older helper from sending the restore round the same
3378: -                # folder twice.
3379: -                [ "${previous_name}" = "${own_name}" ] && continue
3380: -                [ "${previous_name}" = "${prior_name}" ] && continue
3381: -                if folder_has_archives "${REMOTENAME}${SETTINGS_REMOTE}/${previous_name}"; then
3382: -                    restore_src="${REMOTENAME}${SETTINGS_REMOTE}/${previous_name}"
3383: -                    log_message "using backups saved under ${previous_name}, a folder this device may have written to while its id was the shared constant (#86); another device of the same model or hostname may have written there too" "false" "WARN"
3384: -                    log_message "Using backups from a folder this device may have shared with another of the same model, so they may not all be from this device." "true" "WARN"
3385: -                    break
3386: -                fi
3387: -            done <<< "${previous_names}"
3388: +        archive_tool="$(dirname "$(readlink -f "$0")")/rasteratops-settings-archive"
3389: +        [ -r "${archive_tool}" ] || archive_tool=/usr/bin/rasteratops-settings-archive
3390: +        if [ ! -r "${archive_tool}" ]; then
3391: +            report_rclone_error 1 "Reading settings backups"
3392: +            return 1
3393:          fi
3394: -        if [ -z "${restore_src}" ] && folder_has_archives "${legacy_src}"; then
3395: -            restore_src="${legacy_src}"
3396: -            log_message "Using a backup saved before this device had its own cloud folder" "false"
3397: +        . "${archive_tool}"
3398: +        select_settings_archives "${legacy_src}" "${id_tool}"; archive_rc=$?
3399: +        if [ "${archive_rc}" -ne 0 ]; then
3400: +            report_rclone_error "${archive_rc}" "Reading settings backups"
3401: +            return "${archive_rc}"
3402:          fi
3403: +        restore_src="${SETTINGS_ARCHIVE_SOURCE}"
3404:          if [ -z "${restore_src}" ]; then
3405: -            # Say what is actually there. Other devices' folders are not this
3406: -            # device's to restore silently, but "no backup found" when the
3407: -            # cloud plainly holds several is the kind of dead end that sends
3408: -            # someone looking in the wrong place.
3409: -            local others
3410: -            others=$(rclone lsf "${legacy_src}/" --dirs-only "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | tr -d '/' | tr '\n' ' ')
3411: +            # Other devices' folders are useful context, never candidates for
3412: +            # a silent restore. Keep the existing explanation without turning
3413: +            # a failed directory listing into a claim that the cloud is empty.
3414: +            local others others_rc
3415: +            others=$(rclone lsf "${legacy_src}/" --dirs-only "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); others_rc=$?
3416: +            case "${others_rc}" in
3417: +                0|3|4) ;;
3418: +                *) report_rclone_error "${others_rc}" "Reading settings backups"; return "${others_rc}" ;;
3419: +            esac
3420: +            others=$(printf '%s' "${others}" | tr -d '/' | tr '\n' ' ')
3421:              if [ -n "${others}" ]; then
3422:                  log_message "There's no settings backup for this device yet. The cloud has backups from: ${others}" "true" "WARN"
3423:              else
3424: @@ -2094,6 +2077,10 @@ restore_system_files() {
3425:              RESTORE_SYSTEM_STATUS=0
3426:              return 0
3427:          fi
3428: +        log_message "Restoring settings from ${restore_src} (${SETTINGS_ARCHIVE_KIND} device folder)" "false"
3429: +        if [ "${SETTINGS_ARCHIVE_KIND}" = previous ]; then
3430: +            log_message "Using backups from a folder this device may have shared with another of the same model, so they may not all be from this device." "true" "WARN"
3431: +        fi
3432:  
3433:          # The newest one, not all of them. The cloud keeps a dated history now
3434:          # -- 2026_09_02-143000-ROCKNIX_BACKUP.zip -- so a folder transfer would
3435: @@ -2117,12 +2104,12 @@ restore_system_files() {
3436:          # taken for this device's own; the label cannot tell them apart.
3437:          local osn listing label mine newest
3438:          osn=$(os_name)
3439: -        listing=$(rclone lsf --files-only --include "*.{zip,tar.gz}" "${restore_src}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null)
3440: +        listing="${SETTINGS_ARCHIVE_LISTING}"
3441:          label=$(device_label)
3442:          mine=""
3443:          if [ -n "${label}" ]; then
3444:              mine=$(printf '%s\n' "${listing}" \
3445: -                   | grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-${osn}_SETTINGS\.tar\.gz$" | sort | tail -1)
3446: +                   | grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-(${osn}|ROCKNIX|RASTERATOPS)_SETTINGS\.tar\.gz$" | sort | tail -1)
3447:          fi
3448:          if [ -n "${mine}" ]; then
3449:              newest="${mine}"
3450: @@ -2140,7 +2127,7 @@ restore_system_files() {
3451:                  # The label is what sits between the stamp and -ROCKNIX_; an
3452:                  # archive from before the label has nothing there.
3453:                  made_by=$(printf '%s\n' "${newest}" \
3454: -                          | sed -nE "s/^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-(.*)-${osn}_(SETTINGS|BACKUP)\.(tar\.gz|zip)\$/\1/p")
3455: +                          | sed -nE "s/^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-(.*)-(${osn}|ROCKNIX|RASTERATOPS)_(SETTINGS|BACKUP)\.(tar\.gz|zip)\$/\1/p")
3456:                  case "${made_by}" in
3457:                      '') made_by="made before backups were named after the device" ;;
3458:                      *)  made_by="made on ${made_by}" ;;
3459: @@ -2235,11 +2222,17 @@ main() {
3460:      # the settings-only path has no such step of its own -- cloud_backup's
3461:      # shape (#308 claude F-CS-04), one remote round trip fewer per run. After
3462:      # load_config, which sets an automatic run's deadline (#308 gpt F-CS-34).
3463: -    [ "${SYSTEM_ONLY}" -eq 1 ] && check_internet
3464: -    
3465: -    # Define locations for source and remote
3466: -    # Note: This assumes at least one remote is configured and the first one should be used
3467: +    # An existing config file can contain no remote (#392). Without the
3468: +    # prefix, rclone interprets SAVES_REMOTE as a local path. Refuse before
3469: +    # any path operation instead of treating local files as cloud storage.
3470:      REMOTENAME=$(first_remote)
3471: +    case "${REMOTENAME}" in
3472: +        ?*:) ;;
3473: +        *) log_message "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first." "true" "ERROR"
3474: +           say_why "YOUR CLOUD STORAGE ISN'T SET UP YET"
3475: +           clean_exit 1 ;;
3476: +    esac
3477: +    [ "${SYSTEM_ONLY}" -eq 1 ] && check_internet
3478:      
3479:      # Begin main script operations with user-friendly header
3480:      log_message "=> ${OS_NAME} CLOUD RESTORE\n"
3481: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan b/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan
3482: index b455b4c872..dfc11ef10a 100755
3483: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan
3484: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan
3485: @@ -174,10 +174,13 @@ read_folder() {
3486:      # elsewhere.
3487:      if [ "$(sed -n 's/^STATE=//p' "${OUT}/state")" = superseded-empty ] \
3488:         && [ "$(sed -n 's/^CURRENT_EXISTS=//p' "${OUT}/state")" = 1 ]; then
3489: -        if timeout 20 "${layout}" --follow >/dev/null 2>&1; then
3490: -            log "scan: followed the fleet to the current layout"
3491: -            "${layout}" --state > "${OUT}/state" 2>/dev/null; stop_on $? "--state"
3492: -        fi
3493: +        timeout 20 "${layout}" --follow >/dev/null 2>&1; rc=$?
3494: +        case "${rc}" in
3495: +            0) log "scan: followed the fleet to the current layout" ;;
3496: +            3) ;; # The remote may have changed since the state read; read it again.
3497: +            *) stop_on "${rc}" "--follow" ;;
3498: +        esac
3499: +        "${layout}" --state > "${OUT}/state" 2>/dev/null; stop_on $? "--state"
3500:      fi
3501:  }
3502:  
3503: @@ -207,19 +210,21 @@ echo ">>> unit SETTINGS BACKUPS||"
3504:  echo ">>> doing scan"
3505:  settings_remote=$(conf_get SETTINGS_REMOTE) || { why "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"; exit 1; }
3506:  settings_remote="${settings_remote%/}"
3507: -listing=$(rclone lsf --files-only --include "*.{zip,tar.gz}" "${REMOTE}${settings_remote:+${settings_remote#/}}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); rc=$?
3508: -case "${rc}" in
3509: -    0) ;;
3510: -    3|4) listing="" ;;   # no Backups folder yet: nothing to restore, not a failure
3511: -    *) stop_on "${rc}" "archives listing" ;;
3512: -esac
3513: +# Use the restore reader's directory priority, including inherited device IDs.
3514: +archive_tool=$(sibling rasteratops-settings-archive)
3515: +[ -r "${archive_tool}" ] || { why "SOMETHING WENT WRONG"; exit 1; }
3516: +. "${archive_tool}"
3517: +select_settings_archives "${REMOTE}${settings_remote}" "$(sibling cloud_device_id)"; rc=$?
3518: +stop_on "${rc}" "archives listing"
3519: +listing="${SETTINGS_ARCHIVE_LISTING}"
3520:  printf '%s\n' "${listing}" | sed '/^$/d' > "${OUT}/archives"
3521:  label=$(device_label); osn=$(os_name); mine=""; newest=""
3522:  if [ -n "${label}" ]; then
3523: -    mine=$(grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-${osn}_SETTINGS\.tar\.gz$" "${OUT}/archives" | sort | tail -1)
3524: +    mine=$(grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-(${osn}|ROCKNIX|RASTERATOPS)_SETTINGS\.tar\.gz$" "${OUT}/archives" | sort | tail -1)
3525:  fi
3526:  newest=$(grep -E '^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-' "${OUT}/archives" | sort | tail -1)
3527:  {
3528: +    echo "SOURCE=${SETTINGS_ARCHIVE_SOURCE}"
3529:      echo "LABEL=${label}"
3530:      echo "MINE=${mine}"
3531:      echo "NEWEST=${newest}"
3532: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup b/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup
3533: index 49204c368d..f7ed69f8d1 100755
3534: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup
3535: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup
3536: @@ -446,7 +446,7 @@ syncpath_problem() {
3537:          echo
3538:          echo "  ${probe}"
3539:          echo
3540: -        echo "Try something like /rocknix-saves-yourname/Saves instead."
3541: +        echo "Try something like /pixelelated-saves-yourname/Saves instead."
3542:      else
3543:          echo "Your provider wouldn't accept this folder:"
3544:          echo
3545: @@ -531,7 +531,7 @@ case "$1" in
3546:  
3547:          # Where the games actually are, when the configured root holds nothing
3548:          # of ours (fork #352, D-CLOUD-156): the cloud root's Content folder --
3549: -        # the saves folder's parent, /Rasteratops/Content by default -- is
3550: +        # the saves folder's parent, /pixelelated/Content by default -- is
3551:          # looked at for a ROMs or BIOS folder, and named, so the interface can
3552:          # offer it before it asks the player to choose.
3553:          FOUND=""
3554: @@ -727,17 +727,28 @@ case "$1" in
3555:          # The folder is settled before anything is made
3556:          # (cloud_migrate_layout --settle, D-CLOUD-169). A fresh install, or
3557:          # a carried /GAMES, beside a fleet still on the earlier folder joins
3558: -        # it: seeding an empty /Rasteratops beside the player's saves left a
3559: +        # it: seeding an empty /pixelelated beside the player's saves left a
3560:          # new device reading a folder with none of them in it (the
3561:          # mixed-installation test, D-CLOUD-158), and seeding the carried
3562:          # /GAMES put a README there that every later check read as saves. A
3563:          # carried default with nothing anywhere is pointed at the current
3564:          # folders, which the seeding makes, as for any new cloud. A settle
3565: -        # that could not answer changes nothing and the seeding goes on.
3566: +        # that could not answer makes nothing. The wizard may still finish;
3567: +        # its boot step retries, without a misleading README at the old root.
3568:          layout_tool="$(dirname "$(readlink -f "$0")")/cloud_migrate_layout"
3569:          [ -x "${layout_tool}" ] || layout_tool=/usr/bin/cloud_migrate_layout
3570: -        [ -x "${layout_tool}" ] && timeout 30 "${layout_tool}" --settle >/dev/null 2>&1 \
3571: -            && log_message "Seeding: this device's cloud folder was settled first (cloud_migrate_layout --settle)"
3572: +        if [ ! -x "${layout_tool}" ]; then
3573: +            log_message "Seeding: cloud folder settlement is unavailable; nothing was made"
3574: +            exit 1
3575: +        fi
3576: +        timeout 30 "${layout_tool}" --settle >/dev/null 2>&1; settle_rc=$?
3577: +        case "${settle_rc}" in
3578: +            0) log_message "Seeding: this device's cloud folder was settled first (cloud_migrate_layout --settle)" ;;
3579: +            3) ;; # A current, populated, custom or kept folder needs no transition.
3580: +            *) log_message "Seeding: cloud folder settlement exited ${settle_rc}; nothing was made"
3581: +               echo "Your cloud folder couldn't be checked, so no folders were made. Try again."
3582: +               exit "${settle_rc}" ;;
3583: +        esac
3584:          # Read as text, never eval'd: the config is shell, and a value an
3585:          # earlier build wrote could carry a command (PL-051). A folder in a
3586:          # form the scripts cannot read makes nothing: read as empty, it
3587: @@ -750,8 +761,8 @@ case "$1" in
3588:              log_message "Seeding: a folder in ${SYNC_CONF} is not in a form the sync reads; nothing was made"
3589:              exit 1
3590:          fi
3591: -        SAVES="${SAVES_REMOTE:-/Rasteratops/Saves}"
3592: -        BACKUPS="${SETTINGS_REMOTE:-/Rasteratops/Backups}"
3593: +        SAVES="${SAVES_REMOTE:-/pixelelated/Saves}"
3594: +        BACKUPS="${SETTINGS_REMOTE:-/pixelelated/Backups}"
3595:          # An empty CONTENT_REMOTE is not a missing one: it is
3596:          # --use-content-root's "the cloud's root", which is where the
3597:          # content scripts put ROMs/ and BIOS/ (ROOT="<remote>:"). Only a
3598: @@ -759,7 +770,7 @@ case "$1" in
3599:          if grep -q '^CONTENT_REMOTE=' "${SYNC_CONF}" 2>/dev/null; then
3600:              CONTENT="${CONTENT_REMOTE%/}"
3601:          else
3602: -            CONTENT="/Rasteratops/Content"
3603: +            CONTENT="/pixelelated/Content"
3604:          fi
3605:  
3606:          for d in "${SAVES}" "${SAVES}/savefiles" "${SAVES}/savestates" \
3607: @@ -781,11 +792,14 @@ case "$1" in
3608:          # Not beside a folder this project once shipped as its default: a
3609:          # device that joined one marks nothing, and a layout=2 marker at
3610:          # /ROCKNIX would say a thing about that cloud that is not so.
3611: -        if [ -x "${layout_tool}" ] && "${layout_tool}" --superseded 2>/dev/null | grep -qFx -- "${SAVES%/}"; then
3612: -            :
3613: -        elif ! printf 'layout=2\n' | rclone rcat "${REMOTE}${SAVES%/*}/.layout" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null; then
3614: -            log_message "Seeding: the layout marker could not be written at ${SAVES%/*}/.layout"
3615: -        fi
3616: +        # The same version-aware writer owns publication for migration and
3617: +        # seeding. Custom and earlier layouts publish no current marker.
3618: +        "${layout_tool}" --write-marker; marker_rc=$?
3619: +        case "${marker_rc}" in
3620: +            0|3) ;;
3621: +            *) log_message "Seeding: layout marker publication failed (${marker_rc})"
3622: +               exit "${marker_rc}" ;;
3623: +        esac
3624:  
3625:          seed_note() {
3626:              local dir="$1" listing tmp; shift
3627: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf b/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf
3628: index f83a2b4b89..5ae1113dc5 100644
3629: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf
3630: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf
3631: @@ -27,11 +27,11 @@ SAVESPATH="/storage/roms"
3632:  SETTINGS_BACKUPS="/storage/roms/backup"
3633:  
3634:  # Saves on the cloud remote
3635: -SAVES_REMOTE="/Rasteratops/Saves"
3636: +SAVES_REMOTE="/pixelelated/Saves"
3637:  
3638:  # Settings backups on the cloud remote. Must be a sibling of SAVES_REMOTE,
3639:  # never inside it -- a mirror of the saves folder would delete the archives.
3640: -SETTINGS_REMOTE="/Rasteratops/Backups"
3641: +SETTINGS_REMOTE="/pixelelated/Backups"
3642:  
3643:  # ROMs and BIOS files on the cloud remote, one folder per system plus "bios".
3644:  # Previously unset, which put them at the remote root and scattered system
3645: @@ -43,7 +43,7 @@ SETTINGS_REMOTE="/Rasteratops/Backups"
3646:  # has no parent to put them beside: that config gets "" (the remote root,
3647:  # where its ROMs already were) for its owner to set. Clear it back to "" to
3648:  # use the remote root.
3649: -CONTENT_REMOTE="/Rasteratops/Content"
3650: +CONTENT_REMOTE="/pixelelated/Content"
3651:  
3652:  # A superseded cloud folder this device chose to keep when the move to the
3653:  # current layout was offered (KEEP USING, D-CLOUD-160): the folder kept, so the
3654: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults b/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults
3655: index a581ea6f7a..356929b872 100644
3656: --- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults
3657: +++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults
3658: @@ -27,11 +27,11 @@ DEFAULT_SAVESPATH="/storage/roms"
3659:  DEFAULT_SETTINGS_BACKUPS="/storage/roms/backup"
3660:  
3661:  # Saves on the cloud remote
3662: -DEFAULT_SAVES_REMOTE="/Rasteratops/Saves"
3663: +DEFAULT_SAVES_REMOTE="/pixelelated/Saves"
3664:  
3665:  # Settings backups on the cloud remote. Must be a sibling of SAVES_REMOTE,
3666:  # never inside it -- a mirror of the saves folder would delete the archives.
3667: -DEFAULT_SETTINGS_REMOTE="/Rasteratops/Backups"
3668: +DEFAULT_SETTINGS_REMOTE="/pixelelated/Backups"
3669:  
3670:  # ROMs and BIOS files on the cloud remote, one folder per system plus "bios".
3671:  # Previously unset, which put them at the remote root and scattered system
3672: @@ -43,7 +43,7 @@ DEFAULT_SETTINGS_REMOTE="/Rasteratops/Backups"
3673:  # has no parent to put them beside: that config gets "" (the remote root,
3674:  # where its ROMs already were) for its owner to set. Clear it back to "" to
3675:  # use the remote root.
3676: -DEFAULT_CONTENT_REMOTE="/Rasteratops/Content"
3677: +DEFAULT_CONTENT_REMOTE="/pixelelated/Content"
3678:  
3679:  # A superseded cloud folder this device chose to keep when the move to the
3680:  # current layout was offered (KEEP USING, D-CLOUD-160): the folder kept, so the
3681: diff --git a/projects/ROCKNIX/packages/network/rclone/sources/rasteratops-settings-archive b/projects/ROCKNIX/packages/network/rclone/sources/rasteratops-settings-archive
3682: new file mode 100755
3683: index 0000000000..3daea42081
3684: --- /dev/null
3685: +++ b/projects/ROCKNIX/packages/network/rclone/sources/rasteratops-settings-archive
3686: @@ -0,0 +1,43 @@
3687: +#!/bin/bash
3688: +# SPDX-License-Identifier: GPL-2.0
3689: +# Copyright (C) 2026-present rasteratops (https://github.com/rasteratops)
3690: +# Shared archive discovery for cloud_scan and cloud_restore. Sourced, no I/O
3691: +# until select_settings_archives is called. Directory priority is part of the
3692: +# persisted device identity: current, pre-label, healed IDs, then flat legacy.
3693: +# Never search other devices recursively. A failed read is not an empty folder.
3694: +select_settings_archives() { # <remote Backups path> <device-id helper>
3695: +    local root="${1%/}" tool="$2" own="" prior="" previous="" name path rc
3696: +    local -a names=()
3697: +    SETTINGS_ARCHIVE_SOURCE=""; SETTINGS_ARCHIVE_LISTING=""; SETTINGS_ARCHIVE_KIND=""
3698: +    if [ -x "${tool}" ]; then
3699: +        own=$("${tool}" 2>/dev/null | tr -cd 'A-Za-z0-9_.-')
3700: +        prior=$("${tool}" --legacy 2>/dev/null | tr -cd 'A-Za-z0-9_.-')
3701: +        previous=$("${tool}" --previous 2>/dev/null | tr -cd 'A-Za-z0-9_.\n-')
3702: +    fi
3703: +    [ -n "${own}" ] && names+=("${own}")
3704: +    [ -n "${prior}" ] && [ "${prior}" != "${own}" ] && names+=("${prior}")
3705: +    while IFS= read -r name; do
3706: +        [ -n "${name}" ] && [ "${name}" != "${own}" ] && [ "${name}" != "${prior}" ] && names+=("${name}")
3707: +    done <<< "${previous}"
3708: +    names+=("")
3709: +    for name in "${names[@]}"; do
3710: +        case "${name}" in .|..) continue ;; esac
3711: +        path="${root}${name:+/${name}}"
3712: +        SETTINGS_ARCHIVE_LISTING=$(rclone lsf --files-only --include '/*.{zip,tar.gz}' "${path}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); rc=$?
3713: +        case "${rc}" in
3714: +            0) ;;
3715: +            3|4) SETTINGS_ARCHIVE_LISTING=""; continue ;;
3716: +            *) SETTINGS_ARCHIVE_LISTING=""; return "${rc}" ;;
3717: +        esac
3718: +        [ -n "${SETTINGS_ARCHIVE_LISTING}" ] || continue
3719: +        SETTINGS_ARCHIVE_SOURCE="${path}"
3720: +        case "${name}" in
3721: +            "") SETTINGS_ARCHIVE_KIND=flat ;;
3722: +            "${own}") SETTINGS_ARCHIVE_KIND=current ;;
3723: +            "${prior}") SETTINGS_ARCHIVE_KIND=legacy ;;
3724: +            *) SETTINGS_ARCHIVE_KIND=previous ;;
3725: +        esac
3726: +        return 0
3727: +    done
3728: +    return 0
3729: +}
3730: diff --git a/projects/ROCKNIX/packages/rocknix/package.mk b/projects/ROCKNIX/packages/rocknix/package.mk
3731: index aaf53af86c..7174ed1182 100644
3732: --- a/projects/ROCKNIX/packages/rocknix/package.mk
3733: +++ b/projects/ROCKNIX/packages/rocknix/package.mk
3734: @@ -1,5 +1,6 @@
3735:  # SPDX-License-Identifier: GPL-2.0
3736:  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
3737: +# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
3738:  
3739:  PKG_NAME="rocknix"
3740:  PKG_VERSION=""
3741: @@ -10,7 +11,8 @@ PKG_URL=""
3742:  # at build time when upstream dropped the package (a3d0ad0430) -- the image
3743:  # simply shipped without it and "backuptool backup" could not run. Declaring
3744:  # it here turns an invisible runtime dependency into one the build enforces.
3745: -PKG_DEPENDS_TARGET="toolchain autostart zip"
3746: +# The private-settings writer uses BusyBox stat/chmod before publication (#421).
3747: +PKG_DEPENDS_TARGET="toolchain autostart zip busybox"
3748:  PKG_LONGDESC="ROCKNIX Meta Package"
3749:  PKG_TOOLCHAIN="make"
3750:  
3751: diff --git a/projects/ROCKNIX/packages/rocknix/profile.d/001-functions b/projects/ROCKNIX/packages/rocknix/profile.d/001-functions
3752: index 71d57c2088..0ec8ef874d 100644
3753: --- a/projects/ROCKNIX/packages/rocknix/profile.d/001-functions
3754: +++ b/projects/ROCKNIX/packages/rocknix/profile.d/001-functions
3755: @@ -382,6 +382,28 @@ function settings_base() {
3756:    return 0
3757:  }
3758:  
3759: +function prepare_settings_temp() {
3760: +  # The rename must not widen a private live file or recovery record (#421).
3761: +  # Set the temporary's mode while it is empty, including an old temporary
3762: +  # left by an interrupted writer. Callers hold the settings lock where used.
3763: +  local tmp="${1}" source bits mode=0777 found=0
3764: +  shift
3765: +  [ ! -L "${tmp}" ] && { [ ! -e "${tmp}" ] || [ -f "${tmp}" ]; } || return 1
3766: +  for source in "$@"; do
3767: +    [ "${source}" != "${tmp}" ] || return 1
3768: +    [ -e "${source}" ] || continue
3769: +    bits=$(stat -L -c %a "${source}") || return 1
3770: +    [[ "${bits}" =~ ^[0-7]{1,4}$ ]] || return 1
3771: +    mode=$((mode & 8#${bits}))
3772: +    found=1
3773: +  done
3774: +  [ "${found}" = 1 ] || mode=0600
3775: +  # Never relax the caller's umask either.
3776: +  bits=$(umask); [[ "${bits}" =~ ^[0-7]{1,4}$ ]] || return 1
3777: +  printf -v bits '%o' "$((mode & ~8#${bits} & 0777))"
3778: +  ( umask 077; : > "${tmp}" ) && chmod "${bits}" "${tmp}"
3779: +}
3780: +
3781:  # One key, one write, one rename, under a lock the caller holds: awk prints
3782:  # every line but the key's, then the key's new line, into a temporary
3783:  # beside the file, and the temporary is renamed over it -- so the file goes
3784: @@ -405,7 +427,8 @@ function settings_base() {
3785:  #
3786:  # It writes onto settings_base's lines, not the file's bytes: see there.
3787:  function write_setting_line() {
3788: -  if ( set -o pipefail
3789: +  if prepare_settings_temp "${J_CONF}.tmp" "${J_CONF}" "${J_CONF}.backup" \
3790: +     && ( set -o pipefail
3791:         settings_base | K="${1}" V="${2}" awk 'BEGIN { k = ENVIRON["K"]; v = ENVIRON["V"] }
3792:                                                index($0, k "=") != 1 { print }
3793:                                                END { print k "=" v }' ) > "${J_CONF}.tmp" 2>/dev/null \
3794: @@ -439,7 +462,8 @@ function del_setting() {
3795:        # itself is not loosened.
3796:        write_setting_line "${1}" "" || rc=1
3797:      else
3798: -      if ( set -o pipefail; settings_base | K="${1}" awk 'index($0, ENVIRON["K"] "=") != 1' ) > "${J_CONF}.tmp" 2>/dev/null \
3799: +      if prepare_settings_temp "${J_CONF}.tmp" "${J_CONF}" "${J_CONF}.backup" \
3800: +         && ( set -o pipefail; settings_base | K="${1}" awk 'index($0, ENVIRON["K"] "=") != 1' ) > "${J_CONF}.tmp" 2>/dev/null \
3801:           && mv -f "${J_CONF}.tmp" "${J_CONF}"
3802:        then
3803:          :
3804: @@ -454,6 +478,7 @@ function del_setting() {
3805:  }
3806:  
3807:  function sort_settings() {
3808: +  local rc=0
3809:    wait_lock || return 1
3810:    # The sorted copy replaces the live file only when it is plainly a config:
3811:    # non-empty and still carrying the hostname line every image writes. An
3812: @@ -466,15 +491,18 @@ function sort_settings() {
3813:    # gpt G3-D-04): a producer that fails after the hostname line left a
3814:    # nonempty, plausible, truncated copy that the test below would install.
3815:    # pipefail in a subshell, as the neighbouring writers have it.
3816: -  if ( set -o pipefail; settings_base | grep '^[a-z0-9]' | sort >"${J_CONF}.tmp" ) \
3817: +  if prepare_settings_temp "${J_CONF}.tmp" "${J_CONF}" "${J_CONF}.backup" \
3818: +     && ( set -o pipefail; settings_base | grep '^[a-z0-9]' | sort >"${J_CONF}.tmp" ) \
3819:       && [ -s "${J_CONF}.tmp" ] && grep -q '^system\.hostname=' "${J_CONF}.tmp"
3820:    then
3821: -    mv -f "${J_CONF}.tmp" "${J_CONF}"
3822: +    mv -f "${J_CONF}.tmp" "${J_CONF}" || rc=1
3823:    else
3824:      rm -f "${J_CONF}.tmp"
3825:      logger -t sort_settings "left system.cfg alone: the sorted copy was empty or had no hostname line" 2>/dev/null
3826: +    rc=1
3827:    fi
3828:    rm -f "${J_CONF_LOCK}"
3829: +  return ${rc}
3830:  }
3831:  
3832:  function set_kill() {
3833: @@ -567,7 +595,8 @@ function set_settings() {
3834:      cp -f /usr/config/system/configs/system.cfg /storage/.config/system/configs/system.cfg
3835:    fi
3836:    wait_lock || return 1
3837: -  if ( set -o pipefail
3838: +  if prepare_settings_temp "${J_CONF}.tmp" "${J_CONF}" "${J_CONF}.backup" \
3839: +     && ( set -o pipefail
3840:         settings_base | env "${pairs[@]}" SN="${n}" awk 'BEGIN { n = ENVIRON["SN"]; for (j = 1; j <= n; j++) { k[j] = ENVIRON["SK" j]; v[j] = ENVIRON["SV" j]; d[j] = ENVIRON["SD" j] } }
3841:                                                       { for (j = 1; j <= n; j++) if (index($0, k[j] "=") == 1) next; print }
3842:                                                       END { for (j = 1; j <= n; j++) if (d[j] != 1) print k[j] "=" v[j] }' ) > "${J_CONF}.tmp" 2>/dev/null \
3843: diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool b/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
3844: index abeb76de36..fd19f0e018 100755
3845: --- a/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
3846: +++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
3847: @@ -95,7 +95,7 @@ stamp_at() {
3848:  }
3849:  STAMP_EPOCH="$(date +%s)"
3850:  BACKUP_STAMP="$(stamp_at "${STAMP_EPOCH}")"
3851: -# The device's name sits between the stamp and -${OS_NAME}_SETTINGS.
3852: +# The device's name sits between the stamp and -${ARCHIVE_OS_NAME}_SETTINGS.
3853:  #
3854:  # Every device used to write <stamp>-ROCKNIX_SETTINGS.tar.gz, so two
3855:  # handhelds' archives were told apart by nothing. Maintainer, 2026-09-08: a
3856: @@ -140,8 +140,10 @@ DEVICE_LABEL="$(device_label)"
3857:  # extracts cleanly over an existing one. Verified on-device, because Info-ZIP
3858:  # on a desktop and busybox on a handheld disagree, which is how the original
3859:  # bug stayed invisible.
3860: -BACKUPFILE="${SETTINGS_BACKUPS}/${BACKUP_STAMP}-${DEVICE_LABEL:+${DEVICE_LABEL}-}${OS_NAME}_SETTINGS.tar.gz"
3861: -LEGACY_BACKUPFILE="${SETTINGS_BACKUPS}/${OS_NAME}_BACKUP.zip"
3862: +# Archive names are a persisted compatibility contract, not OS display text.
3863: +ARCHIVE_OS_NAME=ROCKNIX
3864: +BACKUPFILE="${SETTINGS_BACKUPS}/${BACKUP_STAMP}-${DEVICE_LABEL:+${DEVICE_LABEL}-}${ARCHIVE_OS_NAME}_SETTINGS.tar.gz"
3865: +LEGACY_BACKUPFILE="${SETTINGS_BACKUPS}/${ARCHIVE_OS_NAME}_BACKUP.zip"
3866:  
3867:  # The newest archive present, whatever it is called and whichever device wrote
3868:  # it. Names lead with the date, so sorting them orders them by age.
3869: @@ -156,13 +158,15 @@ LEGACY_BACKUPFILE="${SETTINGS_BACKUPS}/${OS_NAME}_BACKUP.zip"
3870:  # from before the label finds a new archive with the very same code.
3871:  newest_backup() {
3872:      local found
3873: -    found=$(ls -1 "${SETTINGS_BACKUPS}"/*-"${OS_NAME}"_SETTINGS.tar.gz \
3874: -                  "${SETTINGS_BACKUPS}"/*-"${OS_NAME}"_BACKUP.tar.gz \
3875: -                  "${SETTINGS_BACKUPS}"/*-"${OS_NAME}"_BACKUP.zip 2>/dev/null | sort | tail -1)
3876: +    found=$(ls -1 "${SETTINGS_BACKUPS}"/*-{ROCKNIX,RASTERATOPS,pixelelated}_SETTINGS.tar.gz \
3877: +                  "${SETTINGS_BACKUPS}"/*-{ROCKNIX,RASTERATOPS,pixelelated}_BACKUP.tar.gz \
3878: +                  "${SETTINGS_BACKUPS}"/*-{ROCKNIX,RASTERATOPS,pixelelated}_BACKUP.zip 2>/dev/null | sort | tail -1)
3879:      if [ -n "${found}" ]; then
3880:          echo "${found}"
3881:      elif [ -f "${LEGACY_BACKUPFILE}" ]; then
3882:          echo "${LEGACY_BACKUPFILE}"
3883: +    elif [ -f "${SETTINGS_BACKUPS}/RASTERATOPS_BACKUP.zip" ]; then
3884: +        echo "${SETTINGS_BACKUPS}/RASTERATOPS_BACKUP.zip"
3885:      fi
3886:  }
3887:  ARCHIVE_KEEP=3
3888: @@ -1456,11 +1460,11 @@ case "${VERB}" in
3889:          # player made; it is trimmed with the rest of archive/ so the folder
3890:          # stays bounded.
3891:          mkdir -p "${ARCHIVEFOLDER}"
3892: -        SNAPSHOT="${ARCHIVEFOLDER}/${BACKUP_STAMP}-PRE_RESTORE-${DEVICE_LABEL:+${DEVICE_LABEL}-}${OS_NAME}_SETTINGS.tar.gz"
3893: +        SNAPSHOT="${ARCHIVEFOLDER}/${BACKUP_STAMP}-PRE_RESTORE-${DEVICE_LABEL:+${DEVICE_LABEL}-}${ARCHIVE_OS_NAME}_SETTINGS.tar.gz"
3894:          while [ -e "${SNAPSHOT}" ]
3895:          do
3896:              STAMP_EPOCH=$((STAMP_EPOCH + 1)); BACKUP_STAMP="$(stamp_at "${STAMP_EPOCH}")"
3897: -            SNAPSHOT="${ARCHIVEFOLDER}/${BACKUP_STAMP}-PRE_RESTORE-${DEVICE_LABEL:+${DEVICE_LABEL}-}${OS_NAME}_SETTINGS.tar.gz"
3898: +            SNAPSHOT="${ARCHIVEFOLDER}/${BACKUP_STAMP}-PRE_RESTORE-${DEVICE_LABEL:+${DEVICE_LABEL}-}${ARCHIVE_OS_NAME}_SETTINGS.tar.gz"
3899:          done
3900:          # The restore's own lists, each checked (#307, the audit of the fix
3901:          # round, PL-006): with none, the copy cannot be built, so nothing is
3902: @@ -1824,7 +1828,7 @@ case "${VERB}" in
3903:          while [ -e "${BACKUPFILE}" ]
3904:          do
3905:              STAMP_EPOCH=$((STAMP_EPOCH + 1)); BACKUP_STAMP="$(stamp_at "${STAMP_EPOCH}")"
3906: -            BACKUPFILE="${SETTINGS_BACKUPS}/${BACKUP_STAMP}-${DEVICE_LABEL:+${DEVICE_LABEL}-}${OS_NAME}_SETTINGS.tar.gz"
3907: +            BACKUPFILE="${SETTINGS_BACKUPS}/${BACKUP_STAMP}-${DEVICE_LABEL:+${DEVICE_LABEL}-}${ARCHIVE_OS_NAME}_SETTINGS.tar.gz"
3908:          done
3909:  
3910:          # The archive at the root right now, named before the new one exists
3911: diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig b/projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig
3912: index 006a86f9b1..da37772504 100755
3913: --- a/projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig
3914: +++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig
3915: @@ -66,7 +66,8 @@ valid() {
3916:  # the same directory, then rename over the target.
3917:  put() {
3918:    local src="$1" dst="$2"
3919: -  if cp "${src}" "${dst}.tmp" && mv -f "${dst}.tmp" "${dst}"; then
3920: +  if prepare_settings_temp "${dst}.tmp" "${src}" "${dst}" \
3921: +     && cat "${src}" > "${dst}.tmp" && mv -f "${dst}.tmp" "${dst}"; then
3922:      return 0
3923:    fi
3924:    rm -f "${dst}.tmp"
3925: diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/installtointernal b/projects/ROCKNIX/packages/rocknix/sources/scripts/installtointernal
3926: index cd8c1d33d7..75ac1e6ee9 100755
3927: --- a/projects/ROCKNIX/packages/rocknix/sources/scripts/installtointernal
3928: +++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/installtointernal
3929: @@ -252,4 +252,4 @@ echo "  Android userdata: ${UD_PART_DEV} (${ud_sz} GB)"
3930:  echo "  ROCKNIX : ${RK_PART_DEV} (${rk_sz} GB)"
3931:  echo "  STORAGE : ${ST_PART_DEV} (${st_sz} GB)"
3932:  echo
3933: -echo "ROCKNIX Installation to internal UFS was successful. You can now reboot and remove your SD card."
3934: +echo "pixelelated installation to internal UFS was successful. You can now reboot and remove your SD card."
3935: diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-es-thebezelproject b/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-es-thebezelproject
3936: index 13dc463695..0b1e5c0149 100755
3937: --- a/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-es-thebezelproject
3938: +++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-es-thebezelproject
3939: @@ -21,7 +21,7 @@
3940:  #
3941:  
3942:  readonly VERSION="20220606"
3943: -readonly TITLE="the BezelProject for ROCKNIX"
3944: +readonly TITLE="the BezelProject for pixelelated"
3945:  readonly LOGS_DIR="/var/log"
3946:  readonly DECORATION_DIR="/storage/roms/bezels"
3947:  readonly ROMS_DIR="/storage/roms"
3948: diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-memory-manager b/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-memory-manager
3949: index 60ea3a036f..bb2af52c20 100755
3950: --- a/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-memory-manager
3951: +++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-memory-manager
3952: @@ -148,7 +148,7 @@ show_status_json() {
3953:  }
3954:  
3955:  show_status() {
3956: -    echo "--- ROCKNIX Memory Manager Status ---"
3957: +    echo "--- pixelelated Memory Manager Status ---"
3958:      printf "System RAM:  %s MB\n" "$TOTAL_MEM_MB"
3959:      printf "RAM Tier:    %s\n" "$([ "$IS_LOW_RAM" = true ] && echo "Low" || ([ "$IS_MID_RAM" = true ] && echo "Mid" || echo "High"))"
3960:      printf "SoC Tier:    %s\n" "$([ "$IS_HIGH_PERF_SOC" = true ] && echo "High Performance" || echo "Standard")"
3961: diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-report-stats b/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-report-stats
3962: index fe7bdc907c..57830db92a 100755
3963: --- a/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-report-stats
3964: +++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-report-stats
3965: @@ -1,48 +1,7 @@
3966:  #!/bin/sh
3967: -# This script reports non personally identifiable information to ROCKNIX so that we can
3968: -# see active user statistics.
3969: -
3970: -. /etc/profile
3971: -
3972: -MACHINEIDFILE=/storage/.cache/systemd-machine-id
3973: -USERID=$(cat ${MACHINEIDFILE})
3974: -
3975: -ENDPOINT_URL="https://stats.rocknix.org"
3976: -MAX_RETRIES=5
3977: -RETRY_DELAY=60
3978: -
3979: -send_stats() {
3980: -    curl -s -S -X POST \
3981: -        -F "ROCKNIX_UID=${USERID:(-12)}" \
3982: -        -F "ROCKNIX_VERSION=${OS_VERSION}" \
3983: -        -F "ROCKNIX_BUILD=${OS_BUILD}" \
3984: -        -F "ROCKNIX_SOC=${HW_DEVICE}" \
3985: -        -F "ROCKNIX_DEV=${QUIRK_DEVICE}" \
3986: -        $ENDPOINT_URL
3987: -    return $?
3988: -}
3989: -
3990: -# Try to send stats with retries
3991: -retry_count=0
3992: -while [ $retry_count -lt $MAX_RETRIES ]; do
3993: -    # Check network connectivity first (ping DNS server)
3994: -    if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
3995: -        send_stats
3996: -        exit_code=$?
3997: -
3998: -        if [ $exit_code -eq 0 ]; then
3999: -            echo "Statistics reported successfully."
4000: -            exit 0
4001: -        else
4002: -            echo "Failed to send statistics (HTTP error). Retrying in $RETRY_DELAY seconds..."
4003: -        fi
4004: -    else
4005: -        echo "Network connection unavailable. Retrying in $RETRY_DELAY seconds..."
4006: -    fi
4007: -
4008: -    sleep $RETRY_DELAY
4009: -    retry_count=$((retry_count + 1))
4010: -done
4011: -
4012: -echo "Maximum retry attempts reached. Failed to report statistics."
4013: -exit 1
4014: +# SPDX-License-Identifier: GPL-2.0
4015: +# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
4016: +# Copyright (C) 2026-present Rasteratops (https://github.com/rasteratops)
4017: +# D-WORKFLOW-110: retain the old entry point for upgraded installations,
4018: +# with no collection and no network request. The timer is masked too.
4019: +exit 0
4020: diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-update b/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-update
4021: index 9a36377caa..d8f1f1b21d 100755
4022: --- a/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-update
4023: +++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-update
4024: @@ -1,205 +1,15 @@
4025:  #!/bin/sh
4026:  # SPDX-License-Identifier: GPL-2.0
4027:  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
4028: -
4029: -. /etc/profile
4030: -
4031: -BRANCH="$(get_setting updates.branch)"
4032: -FORCE="$(get_setting updates.force)"
4033: -
4034: -ENDPOINT_URL="https://update.rocknix.org"
4035: -
4036: -MACHINEIDFILE=/storage/.cache/systemd-machine-id
4037: -USERID=$(cat ${MACHINEIDFILE})
4038: -
4039: -# Function to check for an update. It returns a URL if an update is available.
4040: -check_update() {
4041: -    custom_force="${1:-$FORCE}"
4042: -
4043: -    update_url=$(curl -s -S -X POST \
4044: -        -F "OS=${OS_NAME}" \
4045: -        -F "ARCH=${HW_ARCH}" \
4046: -        -F "SOC=${HW_DEVICE}" \
4047: -        -F "VERSION=${OS_VERSION}" \
4048: -        -F "UID=${USERID:(-12)}" \
4049: -        -F "BUILD=${OS_BUILD}" \
4050: -        -F "DEV=${QUIRK_DEVICE}" \
4051: -        -F "FORCE=${custom_force}" \
4052: -        -F "BRANCH=${BRANCH}" \
4053: -        "$ENDPOINT_URL")
4054: -    echo "$update_url"
4055: -    return $?
4056: -}
4057: -
4058: -# Function to get list of releases
4059: -get_releases() {
4060: -    releases=$(curl -s -S -X POST \
4061: -        -F "OS=${OS_NAME}" \
4062: -        -F "ARCH=${HW_ARCH}" \
4063: -        -F "SOC=${HW_DEVICE}" \
4064: -        -F "BRANCH=${BRANCH}" \
4065: -        -F "LIST=1" \
4066: -        "$ENDPOINT_URL")
4067: -    echo "$releases"
4068: -    return $?
4069: -}
4070: -
4071: -# Returns 0 if there is enough available free space at target_path in megabytes.
4072: -check_disk_space() {
4073: -    target_path=$1
4074: -    required_mB=$2
4075: -    available_mB=$(df -m "$target_path" | awk 'NR==2 {print $4}')
4076: -    if [ "$available_mB" -ge "$required_mB" ]; then
4077: -        return 0
4078: -    else
4079: -        return 1
4080: -    fi
4081: -}
4082: -
4083: -# Download a file from url to destination and show progress.
4084: -download_file() {
4085: -    url=$1
4086: -    destination=$2
4087: -    curl --progress-bar -S -L "$url" -o "$destination"
4088: -    return $?
4089: -}
4090: -
4091: -# Main update logic.
4092: -main_update() {
4093: -    custom_force="${1:-$FORCE}"
4094: -    update_url=$(check_update "$custom_force")
4095: -
4096: -    # Check if the returned update_url looks like a URL (e.g., starts with http)
4097: -    case "$update_url" in
4098: -        http://*|https://*)
4099: -            echo "Update available at: $update_url" ;;
4100: -        *)
4101: -            echo "No update available or invalid update URL."
4102: -            exit 1
4103: -            ;;
4104: -    esac
4105: -
4106: -    # Check that there is at least 2GB of available free space on /storage.
4107: -    if ! check_disk_space "/storage" "2048"; then
4108: -        echo "Not enough free space on /storage (need at least 2GB)."
4109: -        exit 1
4110: -    fi
4111: -
4112: -    # Ensure that the /storage/.update folder exists.
4113: -    if [ ! -d "/storage/.update" ]; then
4114: -        mkdir -p /storage/.update || { echo "Failed to create /storage/.update directory."; exit 1; }
4115: -    fi
4116: -
4117: -    # Extract the file name from the update URL.
4118: -    filename=$(basename "$update_url")
4119: -
4120: -    # Define download destinations inside /storage/.update folder using the original file names.
4121: -    update_file="/storage/.update/${filename}"
4122: -    checksum_file="/storage/.update/${filename}.sha256"
4123: -
4124: -    # Downloaded under a .part name and renamed only after the checksum
4125: -    # matches. The updater at the next boot looks for *.tar, so a download
4126: -    # this script never finished -- a dropped link, a power cut -- used to
4127: -    # be picked up as an update, fail to unpack, and cost a boot; a .part
4128: -    # is never looked at (D-CLOUD-078, fork #105). A .part left by an
4129: -    # earlier run is not an update either, and is cleared first.
4130: -    part_file="${update_file}.part"
4131: -    part_checksum="${checksum_file}.part"
4132: -    rm -f /storage/.update/*.part 2>/dev/null
4133: -
4134: -    # Download the update file.
4135: -    echo "Downloading update file..."
4136: -    download_file "$update_url" "$part_file"
4137: -    if [ $? -ne 0 ]; then
4138: -        echo "Failed to download update file."
4139: -        rm -f "$part_file"
4140: -        exit 1
4141: -    fi
4142: -
4143: -    # Download the checksum file (append .sha256 to the update URL).
4144: -    checksum_url="${update_url}.sha256"
4145: -    echo "Downloading checksum file..."
4146: -    download_file "$checksum_url" "$part_checksum"
4147: -    if [ $? -ne 0 ]; then
4148: -        echo "Failed to download checksum file."
4149: -        rm -f "$part_file" "$part_checksum"
4150: -        exit 1
4151: -    fi
4152: -
4153: -    # Verify checksum, then give the files the names the updater looks for.
4154: -    echo "Verifying the downloaded update..."
4155: -    expected_checksum=$(awk '{print $1}' "$part_checksum")
4156: -    actual_checksum=$(sha256sum "$part_file" | awk '{print $1}')
4157: -    if [ -n "$expected_checksum" ] && [ "$expected_checksum" = "$actual_checksum" ]; then
4158: -        if mv -f "$part_file" "$update_file" && mv -f "$part_checksum" "$checksum_file"; then
4159: -            echo "Checksum verified successfully. Reboot to apply the update."
4160: -            set_setting updates.force 0
4161: -            sync
4162: -        else
4163: -            echo "The verified update could not be put in place. Removing downloaded files."
4164: -            rm -f "$part_file" "$part_checksum" "$update_file" "$checksum_file"
4165: -            exit 1
4166: -        fi
4167: -    else
4168: -        echo "Checksum verification failed. Removing downloaded files."
4169: -        rm -f "$part_file" "$part_checksum"
4170: -        exit 1
4171: -    fi
4172: -}
4173: -
4174: -# Check network connectivity (ping DNS server)
4175: -if ! ping -c 1 8.8.8.8 >/dev/null 2>&1; then
4176: -    echo "Network connection unavailable."
4177: -    exit 1
4178: -fi
4179: -
4180: -# Read the first argument to determine the mode.
4181: -mode=$1
4182: -
4183: -# Check if the mode is a number (e.g., 20250101), which indicates forcing a specific version
4184: -if echo "$mode" | grep -q '^[0-9]\{8\}$'; then
4185: -    # If mode is a date (8 digits), treat it as a forced version
4186: -    echo "Forcing update to version $mode..."
4187: -    main_update "$mode"
4188: -    exit 0
4189: -fi
4190: -
4191: -case "$mode" in
4192: -    check)
4193: -        update_url=$(check_update)
4194: -        case "$update_url" in
4195: -            http://*|https://*)
4196: -                # Extract the filename from the URL.
4197: -                filename=$(basename "$update_url")
4198: -                # Use shell parameter expansion to remove everything up to the last dash, then remove the .tar suffix.
4199: -                version=${filename##*-}
4200: -                version=${version%.tar}
4201: -                echo "$version"
4202: -                exit 0
4203: -                ;;
4204: -            *)
4205: -                echo "No update available."
4206: -                exit 1
4207: -                ;;
4208: -        esac
4209: -        ;;
4210: -    releases)
4211: -        # Get the list of available releases
4212: -        echo "Checking available releases..."
4213: -        releases=$(get_releases)
4214: -        echo "$releases"
4215: -        exit 0
4216: -        ;;
4217: -    update|"")
4218: -        # If mode is "update" or no argument is provided, proceed with the update.
4219: -        main_update
4220: -        ;;
4221: -    *)
4222: -        echo "Usage: $0 [check|update|releases|<version>]"
4223: -        echo "  check     - Check for available updates and print version"
4224: -        echo "  update    - Update to the latest version"
4225: -        echo "  releases  - Show available releases"
4226: -        echo "  <version> - Force update to specific version (e.g., 20250101)"
4227: -        exit 1
4228: -        ;;
4229: +# Copyright (C) 2026-present Rasteratops (https://github.com/rasteratops)
4230: +# Manual adoption for0.0.1 (D-WORKFLOW-093). Retain the command name for
4231: +# installed callers, but never contact the previous distribution's updater.
4232: +case "${1:-}" in
4233: +    check) exit 1 ;;
4234: +    --help|-h) result=0 ;;
4235: +    *) result=1 ;;
4236:  esac
4237: +printf '%s\n' 'This version uses manual updates.' \
4238: +    'Get the update for your device and its instructions from:' \
4239: +    'https://github.com/pixelelated/distribution/releases'
4240: +exit "${result}"
4241: diff --git a/projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.timer b/projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.timer
4242: deleted file mode 100644
4243: index 94acc4be30..0000000000
4244: --- a/projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.timer
4245: +++ /dev/null
4246: @@ -1,8 +0,0 @@
4247: -[Unit]
4248: -Description=Timer to report anonymous ROCKNIX install statistics
4249: -
4250: -[Timer]
4251: -OnBootSec=5min
4252: -
4253: -[Install]
4254: -WantedBy=timers.target
4255: diff --git a/projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.timer b/projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.timer
4256: new file mode 120000
4257: index 0000000000..dc1dc0cde0
4258: --- /dev/null
4259: +++ b/projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.timer
4260: @@ -0,0 +1 @@
4261: +/dev/null
4262: \ No newline at end of file
4263: diff --git a/projects/ROCKNIX/packages/rust/cbindgen/package.mk b/projects/ROCKNIX/packages/rust/cbindgen/package.mk
4264: index 1a8a664656..2e9722a78e 100644
4265: --- a/projects/ROCKNIX/packages/rust/cbindgen/package.mk
4266: +++ b/projects/ROCKNIX/packages/rust/cbindgen/package.mk
4267: @@ -1,11 +1,12 @@
4268:  # SPDX-License-Identifier: GPL-2.0-or-later
4269:  # Copyright (C) 2025-present Team LibreELEC (https://libreelec.tv)
4270: +# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4271:  
4272:  PKG_NAME="cbindgen"
4273: -PKG_VERSION="0.29.2"
4274: -PKG_SHA256="c7d4d610482390c70e471a5682de714967e187ed2f92f2237c317a484a8c7e3a"
4275: +PKG_VERSION="0.29.4"
4276: +PKG_SHA256="9b5757e915cf8be523d3aca282b9b5651bafa112e14bf1ba488562ba282807d6"
4277:  PKG_LICENSE="MPL-2.0"
4278: -PKG_SITE="https://github.com/mozilla/bindgen"
4279: +PKG_SITE="https://github.com/mozilla/cbindgen"
4280:  PKG_URL="https://github.com/mozilla/cbindgen/archive/v${PKG_VERSION}.tar.gz"
4281:  PKG_DEPENDS_HOST="cargo:host"
4282:  PKG_LONGDESC="A project for generating C bindings from Rust code"
4283: diff --git a/projects/ROCKNIX/packages/sysutils/busybox/scripts/init b/projects/ROCKNIX/packages/sysutils/busybox/scripts/init
4284: index 43a90e5025..0abc963be0 100755
4285: --- a/projects/ROCKNIX/packages/sysutils/busybox/scripts/init
4286: +++ b/projects/ROCKNIX/packages/sysutils/busybox/scripts/init
4287: @@ -7,6 +7,7 @@
4288:  # Copyright (C) 2016-2018 Team LibreELEC (https://libreelec.tv)
4289:  # Copyright (C) 2018-present Team CoreELEC (https://coreelec.org)
4290:  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
4291: +# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4292:  
4293:  # create directories
4294:  /usr/bin/busybox mkdir -p /dev
4295: @@ -1270,8 +1271,10 @@ for arg in $(cat /proc/cmdline); do
4296:    esac
4297:  done
4298:  
4299: -# hide kernel log messages on console
4300: -if [ "${QUIET}" = "yes" ]; then
4301: +# Existing GENERIC_X64 installs retain a boot config without quiet. Keep kernel
4302: +# console redraws off the splash there too; debugging without quiet opts out.
4303: +# This only changes console output, not the kernel log retained by journald.
4304: +if [ "${QUIET}" = "yes" ] || { [ "@DEVICENAME@" = "GENERIC_X64" ] && [ "${DEBUG}" != "yes" ]; }; then
4305:    echo '1 4 1 7' > /proc/sys/kernel/printk
4306:  fi
4307:  
4308: diff --git a/projects/ROCKNIX/packages/tools/installer/scripts/installer b/projects/ROCKNIX/packages/tools/installer/scripts/installer
4309: index 4ac2bb4c41..3ce67fca62 100644
4310: --- a/projects/ROCKNIX/packages/tools/installer/scripts/installer
4311: +++ b/projects/ROCKNIX/packages/tools/installer/scripts/installer
4312: @@ -371,7 +371,7 @@ EOF
4313:    } | whiptail --backtitle "$BACKTITLE" --gauge "Please wait while your system is being setup ..." 6 73 0
4314:  
4315:    # install complete
4316: -  MSG_TITLE="ROCKNIX Install Complete"
4317: +  MSG_TITLE="pixelelated Install Complete"
4318:    MSG_DETAIL="You may now remove the install media and shutdown.\n"
4319:    whiptail --backtitle "$BACKTITLE" --title "$MSG_TITLE" --msgbox "$MSG_DETAIL" 7 73
4320:  }
4321: @@ -447,9 +447,9 @@ prompt_backup_unpack() {
4322:  menu_main() {
4323:    # show the mainmenu
4324:    MSG_TITLE="MAIN MENU"
4325: -  MSG_MENU="\nWelcome to ROCKNIX installation tool! \
4326: +  MSG_MENU="\nWelcome to pixelelated installation tool! \
4327:  \n
4328: -This tool is used to copy ROCKNIX from the installation media \
4329: +This tool is used to copy pixelelated from the installation media \
4330:  to your disk or other device. You'll be up and running in no time! \
4331:  Please note that the contents of the disk you choose will be wiped \
4332:  out during the installation. \
4333: @@ -458,7 +458,7 @@ out during the installation. \
4334:  
4335:    whiptail --backtitle "$BACKTITLE" --cancel-button "$MSG_CANCEL" \
4336:      --title "$MSG_TITLE" --menu "$MSG_MENU" 18 73 4 \
4337: -      1 "Install ROCKNIX" \
4338: +      1 "Install pixelelated" \
4339:        2 "View installation log" \
4340:        3 "Save installation log" \
4341:        4 "Shutdown" 2> $TMPDIR/mainmenu
4342: @@ -492,7 +492,7 @@ logfile_save() {
4343:  
4344:    mount -o remount,ro /flash
4345:  
4346: -  MSG_TITLE="ROCKNIX Log Saved"
4347: +  MSG_TITLE="pixelelated Log Saved"
4348:    MSG_DETAIL="Log location: ${LOGBACKUP}\n"
4349:    whiptail --backtitle "$BACKTITLE" --title "$MSG_TITLE" --msgbox "$MSG_DETAIL" 7 52
4350:  }
4351: @@ -506,7 +506,7 @@ do_poweroff() {
4352:  
4353:  # setup needed variables
4354:  OS_VERSION=$(lsb_release)
4355: -BACKTITLE="ROCKNIX Installer - ${OS_VERSION}"
4356: +BACKTITLE="pixelelated Installer - ${OS_VERSION}"
4357:  
4358:  TMPDIR="/tmp/installer"
4359:  LOGFILE="$TMPDIR/install.log"
4360: @@ -535,7 +535,7 @@ rm -rf $TMPDIR
4361:  mkdir -p $TMPDIR
4362:  
4363:  #create log file
4364: -echo "ROCKNIX Installer - ${OS_VERSION} started at:" > $LOGFILE
4365: +echo "pixelelated Installer - ${OS_VERSION} started at:" > $LOGFILE
4366:  date >> $LOGFILE
4367:  
4368:  dbglg "System status"
4369: diff --git a/projects/ROCKNIX/packages/tools/rocknix-splash/package.mk b/projects/ROCKNIX/packages/tools/rocknix-splash/package.mk
4370: index 5fbf76a99d..05c052c4c0 100644
4371: --- a/projects/ROCKNIX/packages/tools/rocknix-splash/package.mk
4372: +++ b/projects/ROCKNIX/packages/tools/rocknix-splash/package.mk
4373: @@ -2,10 +2,10 @@
4374:  # Copyright (C) 2025 ROCKNIX (https://github.com/ROCKNIX)
4375:  
4376:  PKG_NAME="rocknix-splash"
4377: -PKG_VERSION="9d295bcb74be2282e32c6b614efbea6036974ba8"
4378: -PKG_SHA256="ffa718a9bbcbf69857b91acf854abaf4cc00a7802f61d531341517546c26e635"
4379: +PKG_VERSION="8c71126ceef702528c87a4c49625e64988609f26"
4380: +PKG_SHA256="6a24b287920ad553cbe1e2ecf66fac7a4fb2e3756ba1b98473ca201f3abebcba"
4381:  PKG_LICENSE="GPL"
4382: -PKG_SITE="https://rocknix.org"
4383: -PKG_URL="https://github.com/ROCKNIX/${PKG_NAME}/archive/${PKG_VERSION}.tar.gz"
4384: +PKG_SITE="https://github.com/pixelelated/splash"
4385: +PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
4386:  PKG_DEPENDS_INIT="toolchain"
4387: -PKG_LONGDESC="ROCKNIX splash screen application"
4388: +PKG_LONGDESC="pixelelated splash screen application"
4389: diff --git a/projects/ROCKNIX/packages/ui/emulationstation/package.mk b/projects/ROCKNIX/packages/ui/emulationstation/package.mk
4390: index 13cd0251d9..fafb09aae8 100644
4391: --- a/projects/ROCKNIX/packages/ui/emulationstation/package.mk
4392: +++ b/projects/ROCKNIX/packages/ui/emulationstation/package.mk
4393: @@ -2,10 +2,10 @@
4394:  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
4395:  
4396:  PKG_NAME="emulationstation"
4397: -PKG_VERSION="e108699ea313ecd5ec64b4310a4ea665e05ca19f"
4398: +PKG_VERSION="f6f0c134212bc696f2f6a747c8d390a588f2f0ce"
4399:  PKG_GIT_CLONE_BRANCH="test/qa-integration"
4400: -PKG_LICENSE="GPL"
4401: -PKG_SITE="https://github.com/rasteratops/emulationstation"
4402: +PKG_LICENSE="MIT"
4403: +PKG_SITE="https://github.com/pixelelated/emulationstation"
4404:  PKG_URL="${PKG_SITE}.git"
4405:  # noto-sans-cjk came from upstream 2026-09, and poppler with the PDF support
4406:  # upstream's EmulationStation gained (e0e8b7ac33); the fork builds its own ES
4407: diff --git a/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/package.mk b/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/package.mk
4408: index 3bd55b348d..f649b076a4 100644
4409: --- a/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/package.mk
4410: +++ b/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/package.mk
4411: @@ -14,6 +14,8 @@ PKG_TOOLCHAIN="manual"
4412:  makeinstall_target() {
4413:    mkdir -p ${INSTALL}/usr/share/themes/${PKG_NAME}
4414:      cp -rf * ${INSTALL}/usr/share/themes/${PKG_NAME}
4415: +    cp ${PKG_DIR}/sources/pixelelated-wordmark.svg ${INSTALL}/usr/share/themes/${PKG_NAME}/
4416: +    cp ${PKG_DIR}/sources/Tiny5-OFL.txt ${INSTALL}/usr/share/themes/${PKG_NAME}/
4417:      rm -rf ${INSTALL}/usr/share/themes/${PKG_NAME}/_inc/systems/{artwork-circuit,artwork-classic,artwork-nintendont,artwork-noir,artwork-outline}
4418:      sed -i '/<include name="\(noir\|nintendont\|circuit\|outline\)"/d' ${INSTALL}/usr/share/themes/${PKG_NAME}/theme.xml
4419:      sed -i '/<\/theme>/i\
4420: diff --git a/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch b/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch
4421: new file mode 100644
4422: index 0000000000..f0689a5e31
4423: --- /dev/null
4424: +++ b/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/patches/001-pixelelated-splash.patch
4425: @@ -0,0 +1,31 @@
4426: +pixelelated: replace the default splash and its display name (#337).
4427: +
4428: +Keep the distribution:rocknix setting and custom splash path compatible.
4429: +
4430: +--- a/theme.xml
4431: ++++ b/theme.xml
4432: +@@ -23,7 +23,7 @@
4433: +    -->
4434: +    <subset name="distribution" displayName="Distribution">
4435: +       <include name="batocera" displayName="Batocera/Knulli" />
4436: +-      <include name="rocknix" displayName="RockNIX" />
4437: ++      <include name="rocknix" displayName="pixelelated" />
4438: +       <include name="retrobat" displayName="Retrobat" />
4439: +    </subset>
4440: + 
4441: +--- a/splash.xml
4442: ++++ b/splash.xml
4443: +@@ -27,8 +27,11 @@
4444: +          <path>${themeCustomizationsPath}splash.jpg</path>
4445: +       </image>
4446: +       <image ifSubset="splash-screen:default" name="background">
4447: +-         <origin>0 0</origin>
4448: +-         <pos>1 1</pos>
4449: ++         <origin>0.5 0.5</origin>
4450: ++         <pos>0.5 0.36</pos>
4451: ++         <maxSize>0.8 0.6</maxSize>
4452: ++         <path>./pixelelated-wordmark.svg</path>
4453: ++         <linearSmooth>false</linearSmooth>
4454: +       </image>
4455: +       <image name="progressbar">
4456: +          <origin>0.5 0.5</origin>
4457: diff --git a/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/sources/Tiny5-OFL.txt b/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/sources/Tiny5-OFL.txt
4458: new file mode 100644
4459: index 0000000000..df38291f41
4460: --- /dev/null
4461: +++ b/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/sources/Tiny5-OFL.txt
4462: @@ -0,0 +1,93 @@
4463: +Copyright 2026 The Tiny5 Project Authors (https://github.com/Gissio/font_Tiny5)
4464: +
4465: +This Font Software is licensed under the SIL Open Font License, Version 1.1.
4466: +This license is copied below, and is also available with a FAQ at:
4467: +https://scripts.sil.org/OFL
4468: +
4469: +
4470: +-----------------------------------------------------------
4471: +SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
4472: +-----------------------------------------------------------
4473: +
4474: +PREAMBLE
4475: +The goals of the Open Font License (OFL) are to stimulate worldwide
4476: +development of collaborative font projects, to support the font creation
4477: +efforts of academic and linguistic communities, and to provide a free and
4478: +open framework in which fonts may be shared and improved in partnership
4479: +with others.
4480: +
4481: +The OFL allows the licensed fonts to be used, studied, modified and
4482: +redistributed freely as long as they are not sold by themselves. The
4483: +fonts, including any derivative works, can be bundled, embedded, 
4484: +redistributed and/or sold with any software provided that any reserved
4485: +names are not used by derivative works. The fonts and derivatives,
4486: +however, cannot be released under any other type of license. The
4487: +requirement for fonts to remain under this license does not apply
4488: +to any document created using the fonts or their derivatives.
4489: +
4490: +DEFINITIONS
4491: +"Font Software" refers to the set of files released by the Copyright
4492: +Holder(s) under this license and clearly marked as such. This may
4493: +include source files, build scripts and documentation.
4494: +
4495: +"Reserved Font Name" refers to any names specified as such after the
4496: +copyright statement(s).
4497: +
4498: +"Original Version" refers to the collection of Font Software components as
4499: +distributed by the Copyright Holder(s).
4500: +
4501: +"Modified Version" refers to any derivative made by adding to, deleting,
4502: +or substituting -- in part or in whole -- any of the components of the
4503: +Original Version, by changing formats or by porting the Font Software to a
4504: +new environment.
4505: +
4506: +"Author" refers to any designer, engineer, programmer, technical
4507: +writer or other person who contributed to the Font Software.
4508: +
4509: +PERMISSION & CONDITIONS
4510: +Permission is hereby granted, free of charge, to any person obtaining
4511: +a copy of the Font Software, to use, study, copy, merge, embed, modify,
4512: +redistribute, and sell modified and unmodified copies of the Font
4513: +Software, subject to the following conditions:
4514: +
4515: +1) Neither the Font Software nor any of its individual components,
4516: +in Original or Modified Versions, may be sold by itself.
4517: +
4518: +2) Original or Modified Versions of the Font Software may be bundled,
4519: +redistributed and/or sold with any software, provided that each copy
4520: +contains the above copyright notice and this license. These can be
4521: +included either as stand-alone text files, human-readable headers or
4522: +in the appropriate machine-readable metadata fields within text or
4523: +binary files as long as those fields can be easily viewed by the user.
4524: +
4525: +3) No Modified Version of the Font Software may use the Reserved Font
4526: +Name(s) unless explicit written permission is granted by the corresponding
4527: +Copyright Holder. This restriction only applies to the primary font name as
4528: +presented to the users.
4529: +
4530: +4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
4531: +Software shall not be used to promote, endorse or advertise any
4532: +Modified Version, except to acknowledge the contribution(s) of the
4533: +Copyright Holder(s) and the Author(s) or with their explicit written
4534: +permission.
4535: +
4536: +5) The Font Software, modified or unmodified, in part or in whole,
4537: +must be distributed entirely under this license, and must not be
4538: +distributed under any other license. The requirement for fonts to
4539: +remain under this license does not apply to any document created
4540: +using the Font Software.
4541: +
4542: +TERMINATION
4543: +This license becomes null and void if any of the above conditions are
4544: +not met.
4545: +
4546: +DISCLAIMER
4547: +THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
4548: +EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
4549: +MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
4550: +OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
4551: +COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
4552: +INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
4553: +DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
4554: +FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
4555: +OTHER DEALINGS IN THE FONT SOFTWARE.
4556: diff --git a/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg b/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg
4557: new file mode 100644
4558: index 0000000000..213585ef45
4559: --- /dev/null
4560: +++ b/projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg
4561: @@ -0,0 +1,263 @@
4562: +<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 32" width="480" height="256" shape-rendering="crispEdges" role="img" aria-labelledby="title">
4563: +<title id="title">pixelelated</title>
4564: +<g id="wordmark">
4565: +<path fill="#10E6FF" d="M6.9375 14.5625 L6.0625 14.5625 L6.0625 15.3125 L6.9375 15.3125 Z"/>
4566: +<path fill="#10A5FF" d="M6.9375 15.3125 L6.0625 15.3125 L6.0625 15.4375 L6.9375 15.4375 Z"/>
4567: +<path fill="#10E6FF" d="M5.9375 14.5625 L5.0625 14.5625 L5.0625 15.3125 L5.9375 15.3125 Z"/>
4568: +<path fill="#10A5FF" d="M5.9375 15.3125 L5.0625 15.3125 L5.0625 15.4375 L5.9375 15.4375 Z"/>
4569: +<path fill="#10E6FF" d="M4.9375 14.5625 L4.0625 14.5625 L4.0625 15.3125 L4.9375 15.3125 Z"/>
4570: +<path fill="#10A5FF" d="M4.9375 15.3125 L4.0625 15.3125 L4.0625 15.4375 L4.9375 15.4375 Z"/>
4571: +<path fill="#10E6FF" d="M3.9375 14.5625 L3.0625 14.5625 L3.0625 15.3125 L3.9375 15.3125 Z"/>
4572: +<path fill="#10A5FF" d="M3.9375 15.3125 L3.0625 15.3125 L3.0625 15.4375 L3.9375 15.4375 Z"/>
4573: +<path fill="#10A5FF" d="M7.9375 15.5625 L7.0625 15.5625 L7.0625 16.4375 L7.9375 16.4375 Z"/>
4574: +<path fill="#10A5FF" d="M6.9375 15.5625 L6.0625 15.5625 L6.0625 16.4375 L6.9375 16.4375 Z"/>
4575: +<path fill="#10A5FF" d="M4.9375 15.5625 L4.0625 15.5625 L4.0625 16.4375 L4.9375 16.4375 Z"/>
4576: +<path fill="#10A5FF" d="M3.9375 15.5625 L3.0625 15.5625 L3.0625 16.4375 L3.9375 16.4375 Z"/>
4577: +<path fill="#10A5FF" d="M7.9375 16.5625 L7.0625 16.5625 L7.0625 16.6875 L7.9375 16.6875 Z"/>
4578: +<path fill="#1963FF" d="M7.9375 16.6875 L7.0625 16.6875 L7.0625 17.4375 L7.9375 17.4375 Z"/>
4579: +<path fill="#10A5FF" d="M6.9375 16.5625 L6.0625 16.5625 L6.0625 16.6875 L6.9375 16.6875 Z"/>
4580: +<path fill="#1963FF" d="M6.9375 16.6875 L6.0625 16.6875 L6.0625 17.4375 L6.9375 17.4375 Z"/>
4581: +<path fill="#10A5FF" d="M4.9375 16.5625 L4.0625 16.5625 L4.0625 16.6875 L4.9375 16.6875 Z"/>
4582: +<path fill="#1963FF" d="M4.9375 16.6875 L4.0625 16.6875 L4.0625 17.4375 L4.9375 17.4375 Z"/>
4583: +<path fill="#10A5FF" d="M3.9375 16.5625 L3.0625 16.5625 L3.0625 16.6875 L3.9375 16.6875 Z"/>
4584: +<path fill="#1963FF" d="M3.9375 16.6875 L3.0625 16.6875 L3.0625 17.4375 L3.9375 17.4375 Z"/>
4585: +<path fill="#1963FF" d="M6.9375 17.5625 L6.0625 17.5625 L6.0625 18.0625 L6.9375 18.0625 Z"/>
4586: +<path fill="#1921B5" d="M6.9375 18.0625 L6.0625 18.0625 L6.0625 18.4375 L6.9375 18.4375 Z"/>
4587: +<path fill="#1963FF" d="M5.9375 17.5625 L5.0625 17.5625 L5.0625 18.0625 L5.9375 18.0625 Z"/>
4588: +<path fill="#1921B5" d="M5.9375 18.0625 L5.0625 18.0625 L5.0625 18.4375 L5.9375 18.4375 Z"/>
4589: +<path fill="#1963FF" d="M4.9375 17.5625 L4.0625 17.5625 L4.0625 18.0625 L4.9375 18.0625 Z"/>
4590: +<path fill="#1921B5" d="M4.9375 18.0625 L4.0625 18.0625 L4.0625 18.4375 L4.9375 18.4375 Z"/>
4591: +<path fill="#1963FF" d="M3.9375 17.5625 L3.0625 17.5625 L3.0625 18.0625 L3.9375 18.0625 Z"/>
4592: +<path fill="#1921B5" d="M3.9375 18.0625 L3.0625 18.0625 L3.0625 18.4375 L3.9375 18.4375 Z"/>
4593: +<path fill="#1921B5" d="M3.9375 18.5625 L3.0625 18.5625 L3.0625 19.4375 L3.9375 19.4375 Z"/>
4594: +<path fill="#1921B5" d="M4.9375 18.5625 L4.0625 18.5625 L4.0625 19.4375 L4.9375 19.4375 Z"/>
4595: +<path fill="#A5FFFF" d="M9.9375 12.5625 L9.0625 12.5625 L9.0625 13.4375 L9.9375 13.4375 Z"/>
4596: +<path fill="#A5FFFF" d="M10.9375 12.5625 L10.0625 12.5625 L10.0625 13.4375 L10.9375 13.4375 Z"/>
4597: +<path fill="#10E6FF" d="M9.9375 14.5625 L9.0625 14.5625 L9.0625 15.3125 L9.9375 15.3125 Z"/>
4598: +<path fill="#10A5FF" d="M9.9375 15.3125 L9.0625 15.3125 L9.0625 15.4375 L9.9375 15.4375 Z"/>
4599: +<path fill="#10E6FF" d="M10.9375 14.5625 L10.0625 14.5625 L10.0625 15.3125 L10.9375 15.3125 Z"/>
4600: +<path fill="#10A5FF" d="M10.9375 15.3125 L10.0625 15.3125 L10.0625 15.4375 L10.9375 15.4375 Z"/>
4601: +<path fill="#10A5FF" d="M9.9375 15.5625 L9.0625 15.5625 L9.0625 16.4375 L9.9375 16.4375 Z"/>
4602: +<path fill="#10A5FF" d="M10.9375 15.5625 L10.0625 15.5625 L10.0625 16.4375 L10.9375 16.4375 Z"/>
4603: +<path fill="#10A5FF" d="M9.9375 16.5625 L9.0625 16.5625 L9.0625 16.6875 L9.9375 16.6875 Z"/>
4604: +<path fill="#1963FF" d="M9.9375 16.6875 L9.0625 16.6875 L9.0625 17.4375 L9.9375 17.4375 Z"/>
4605: +<path fill="#10A5FF" d="M10.9375 16.5625 L10.0625 16.5625 L10.0625 16.6875 L10.9375 16.6875 Z"/>
4606: +<path fill="#1963FF" d="M10.9375 16.6875 L10.0625 16.6875 L10.0625 17.4375 L10.9375 17.4375 Z"/>
4607: +<path fill="#1963FF" d="M9.9375 17.5625 L9.0625 17.5625 L9.0625 18.0625 L9.9375 18.0625 Z"/>
4608: +<path fill="#1921B5" d="M9.9375 18.0625 L9.0625 18.0625 L9.0625 18.4375 L9.9375 18.4375 Z"/>
4609: +<path fill="#1963FF" d="M10.9375 17.5625 L10.0625 17.5625 L10.0625 18.0625 L10.9375 18.0625 Z"/>
4610: +<path fill="#1921B5" d="M10.9375 18.0625 L10.0625 18.0625 L10.0625 18.4375 L10.9375 18.4375 Z"/>
4611: +<path fill="#10E6FF" d="M12.9375 14.5625 L12.0625 14.5625 L12.0625 15.3125 L12.9375 15.3125 Z"/>
4612: +<path fill="#10A5FF" d="M12.9375 15.3125 L12.0625 15.3125 L12.0625 15.4375 L12.9375 15.4375 Z"/>
4613: +<path fill="#10E6FF" d="M13.9375 14.5625 L13.0625 14.5625 L13.0625 15.3125 L13.9375 15.3125 Z"/>
4614: +<path fill="#10A5FF" d="M13.9375 15.3125 L13.0625 15.3125 L13.0625 15.4375 L13.9375 15.4375 Z"/>
4615: +<path fill="#10E6FF" d="M15.9375 14.5625 L15.0625 14.5625 L15.0625 15.3125 L15.9375 15.3125 Z"/>
4616: +<path fill="#10A5FF" d="M15.9375 15.3125 L15.0625 15.3125 L15.0625 15.4375 L15.9375 15.4375 Z"/>
4617: +<path fill="#10E6FF" d="M16.9375 14.5625 L16.0625 14.5625 L16.0625 15.3125 L16.9375 15.3125 Z"/>
4618: +<path fill="#10A5FF" d="M16.9375 15.3125 L16.0625 15.3125 L16.0625 15.4375 L16.9375 15.4375 Z"/>
4619: +<path fill="#10A5FF" d="M13.9375 15.5625 L13.0625 15.5625 L13.0625 16.4375 L13.9375 16.4375 Z"/>
4620: +<path fill="#10A5FF" d="M14.9375 15.5625 L14.0625 15.5625 L14.0625 16.4375 L14.9375 16.4375 Z"/>
4621: +<path fill="#10A5FF" d="M15.9375 15.5625 L15.0625 15.5625 L15.0625 16.4375 L15.9375 16.4375 Z"/>
4622: +<path fill="#10A5FF" d="M12.9375 16.5625 L12.0625 16.5625 L12.0625 16.6875 L12.9375 16.6875 Z"/>
4623: +<path fill="#1963FF" d="M12.9375 16.6875 L12.0625 16.6875 L12.0625 17.4375 L12.9375 17.4375 Z"/>
4624: +<path fill="#10A5FF" d="M13.9375 16.5625 L13.0625 16.5625 L13.0625 16.6875 L13.9375 16.6875 Z"/>
4625: +<path fill="#1963FF" d="M13.9375 16.6875 L13.0625 16.6875 L13.0625 17.4375 L13.9375 17.4375 Z"/>
4626: +<path fill="#10A5FF" d="M15.9375 16.5625 L15.0625 16.5625 L15.0625 16.6875 L15.9375 16.6875 Z"/>
4627: +<path fill="#1963FF" d="M15.9375 16.6875 L15.0625 16.6875 L15.0625 17.4375 L15.9375 17.4375 Z"/>
4628: +<path fill="#10A5FF" d="M16.9375 16.5625 L16.0625 16.5625 L16.0625 16.6875 L16.9375 16.6875 Z"/>
4629: +<path fill="#1963FF" d="M16.9375 16.6875 L16.0625 16.6875 L16.0625 17.4375 L16.9375 17.4375 Z"/>
4630: +<path fill="#1963FF" d="M12.9375 17.5625 L12.0625 17.5625 L12.0625 18.0625 L12.9375 18.0625 Z"/>
4631: +<path fill="#1921B5" d="M12.9375 18.0625 L12.0625 18.0625 L12.0625 18.4375 L12.9375 18.4375 Z"/>
4632: +<path fill="#1963FF" d="M13.9375 17.5625 L13.0625 17.5625 L13.0625 18.0625 L13.9375 18.0625 Z"/>
4633: +<path fill="#1921B5" d="M13.9375 18.0625 L13.0625 18.0625 L13.0625 18.4375 L13.9375 18.4375 Z"/>
4634: +<path fill="#1963FF" d="M15.9375 17.5625 L15.0625 17.5625 L15.0625 18.0625 L15.9375 18.0625 Z"/>
4635: +<path fill="#1921B5" d="M15.9375 18.0625 L15.0625 18.0625 L15.0625 18.4375 L15.9375 18.4375 Z"/>
4636: +<path fill="#1963FF" d="M16.9375 17.5625 L16.0625 17.5625 L16.0625 18.0625 L16.9375 18.0625 Z"/>
4637: +<path fill="#1921B5" d="M16.9375 18.0625 L16.0625 18.0625 L16.0625 18.4375 L16.9375 18.4375 Z"/>
4638: +<path fill="#10E6FF" d="M19.9375 14.5625 L19.0625 14.5625 L19.0625 15.3125 L19.9375 15.3125 Z"/>
4639: +<path fill="#10A5FF" d="M19.9375 15.3125 L19.0625 15.3125 L19.0625 15.4375 L19.9375 15.4375 Z"/>
4640: +<path fill="#10E6FF" d="M20.9375 14.5625 L20.0625 14.5625 L20.0625 15.3125 L20.9375 15.3125 Z"/>
4641: +<path fill="#10A5FF" d="M20.9375 15.3125 L20.0625 15.3125 L20.0625 15.4375 L20.9375 15.4375 Z"/>
4642: +<path fill="#10E6FF" d="M21.9375 14.5625 L21.0625 14.5625 L21.0625 15.3125 L21.9375 15.3125 Z"/>
4643: +<path fill="#10A5FF" d="M21.9375 15.3125 L21.0625 15.3125 L21.0625 15.4375 L21.9375 15.4375 Z"/>
4644: +<path fill="#10A5FF" d="M18.9375 15.5625 L18.0625 15.5625 L18.0625 16.4375 L18.9375 16.4375 Z"/>
4645: +<path fill="#10A5FF" d="M19.9375 15.5625 L19.0625 15.5625 L19.0625 16.4375 L19.9375 16.4375 Z"/>
4646: +<path fill="#10A5FF" d="M20.9375 15.5625 L20.0625 15.5625 L20.0625 16.4375 L20.9375 16.4375 Z"/>
4647: +<path fill="#10A5FF" d="M21.9375 15.5625 L21.0625 15.5625 L21.0625 16.4375 L21.9375 16.4375 Z"/>
4648: +<path fill="#10A5FF" d="M22.9375 15.5625 L22.0625 15.5625 L22.0625 16.4375 L22.9375 16.4375 Z"/>
4649: +<path fill="#10A5FF" d="M18.9375 16.5625 L18.0625 16.5625 L18.0625 16.6875 L18.9375 16.6875 Z"/>
4650: +<path fill="#1963FF" d="M18.9375 16.6875 L18.0625 16.6875 L18.0625 17.4375 L18.9375 17.4375 Z"/>
4651: +<path fill="#10A5FF" d="M19.9375 16.5625 L19.0625 16.5625 L19.0625 16.6875 L19.9375 16.6875 Z"/>
4652: +<path fill="#1963FF" d="M19.9375 16.6875 L19.0625 16.6875 L19.0625 17.4375 L19.9375 17.4375 Z"/>
4653: +<path fill="#1963FF" d="M19.9375 17.5625 L19.0625 17.5625 L19.0625 18.0625 L19.9375 18.0625 Z"/>
4654: +<path fill="#1921B5" d="M19.9375 18.0625 L19.0625 18.0625 L19.0625 18.4375 L19.9375 18.4375 Z"/>
4655: +<path fill="#1963FF" d="M20.9375 17.5625 L20.0625 17.5625 L20.0625 18.0625 L20.9375 18.0625 Z"/>
4656: +<path fill="#1921B5" d="M20.9375 18.0625 L20.0625 18.0625 L20.0625 18.4375 L20.9375 18.4375 Z"/>
4657: +<path fill="#1963FF" d="M21.9375 17.5625 L21.0625 17.5625 L21.0625 18.0625 L21.9375 18.0625 Z"/>
4658: +<path fill="#1921B5" d="M21.9375 18.0625 L21.0625 18.0625 L21.0625 18.4375 L21.9375 18.4375 Z"/>
4659: +<path fill="#1963FF" d="M22.9375 17.5625 L22.0625 17.5625 L22.0625 18.0625 L22.9375 18.0625 Z"/>
4660: +<path fill="#1921B5" d="M22.9375 18.0625 L22.0625 18.0625 L22.0625 18.4375 L22.9375 18.4375 Z"/>
4661: +<path fill="#A5FFFF" d="M24.9375 13.5625 L24.0625 13.5625 L24.0625 13.9375 L24.9375 13.9375 Z"/>
4662: +<path fill="#10E6FF" d="M24.9375 13.9375 L24.0625 13.9375 L24.0625 14.4375 L24.9375 14.4375 Z"/>
4663: +<path fill="#A5FFFF" d="M25.9375 13.5625 L25.0625 13.5625 L25.0625 13.9375 L25.9375 13.9375 Z"/>
4664: +<path fill="#10E6FF" d="M25.9375 13.9375 L25.0625 13.9375 L25.0625 14.4375 L25.9375 14.4375 Z"/>
4665: +<path fill="#10E6FF" d="M24.9375 14.5625 L24.0625 14.5625 L24.0625 15.3125 L24.9375 15.3125 Z"/>
4666: +<path fill="#10A5FF" d="M24.9375 15.3125 L24.0625 15.3125 L24.0625 15.4375 L24.9375 15.4375 Z"/>
4667: +<path fill="#10E6FF" d="M25.9375 14.5625 L25.0625 14.5625 L25.0625 15.3125 L25.9375 15.3125 Z"/>
4668: +<path fill="#10A5FF" d="M25.9375 15.3125 L25.0625 15.3125 L25.0625 15.4375 L25.9375 15.4375 Z"/>
4669: +<path fill="#10A5FF" d="M24.9375 15.5625 L24.0625 15.5625 L24.0625 16.4375 L24.9375 16.4375 Z"/>
4670: +<path fill="#10A5FF" d="M25.9375 15.5625 L25.0625 15.5625 L25.0625 16.4375 L25.9375 16.4375 Z"/>
4671: +<path fill="#10A5FF" d="M24.9375 16.5625 L24.0625 16.5625 L24.0625 16.6875 L24.9375 16.6875 Z"/>
4672: +<path fill="#1963FF" d="M24.9375 16.6875 L24.0625 16.6875 L24.0625 17.4375 L24.9375 17.4375 Z"/>
4673: +<path fill="#10A5FF" d="M25.9375 16.5625 L25.0625 16.5625 L25.0625 16.6875 L25.9375 16.6875 Z"/>
4674: +<path fill="#1963FF" d="M25.9375 16.6875 L25.0625 16.6875 L25.0625 17.4375 L25.9375 17.4375 Z"/>
4675: +<path fill="#1963FF" d="M24.9375 17.5625 L24.0625 17.5625 L24.0625 18.0625 L24.9375 18.0625 Z"/>
4676: +<path fill="#1921B5" d="M24.9375 18.0625 L24.0625 18.0625 L24.0625 18.4375 L24.9375 18.4375 Z"/>
4677: +<path fill="#1963FF" d="M25.9375 17.5625 L25.0625 17.5625 L25.0625 18.0625 L25.9375 18.0625 Z"/>
4678: +<path fill="#1921B5" d="M25.9375 18.0625 L25.0625 18.0625 L25.0625 18.4375 L25.9375 18.4375 Z"/>
4679: +<path fill="#10E6FF" d="M28.9375 14.5625 L28.0625 14.5625 L28.0625 15.3125 L28.9375 15.3125 Z"/>
4680: +<path fill="#10A5FF" d="M28.9375 15.3125 L28.0625 15.3125 L28.0625 15.4375 L28.9375 15.4375 Z"/>
4681: +<path fill="#10E6FF" d="M29.9375 14.5625 L29.0625 14.5625 L29.0625 15.3125 L29.9375 15.3125 Z"/>
4682: +<path fill="#10A5FF" d="M29.9375 15.3125 L29.0625 15.3125 L29.0625 15.4375 L29.9375 15.4375 Z"/>
4683: +<path fill="#10E6FF" d="M30.9375 14.5625 L30.0625 14.5625 L30.0625 15.3125 L30.9375 15.3125 Z"/>
4684: +<path fill="#10A5FF" d="M30.9375 15.3125 L30.0625 15.3125 L30.0625 15.4375 L30.9375 15.4375 Z"/>
4685: +<path fill="#10A5FF" d="M27.9375 15.5625 L27.0625 15.5625 L27.0625 16.4375 L27.9375 16.4375 Z"/>
4686: +<path fill="#10A5FF" d="M28.9375 15.5625 L28.0625 15.5625 L28.0625 16.4375 L28.9375 16.4375 Z"/>
4687: +<path fill="#10A5FF" d="M29.9375 15.5625 L29.0625 15.5625 L29.0625 16.4375 L29.9375 16.4375 Z"/>
4688: +<path fill="#10A5FF" d="M30.9375 15.5625 L30.0625 15.5625 L30.0625 16.4375 L30.9375 16.4375 Z"/>
4689: +<path fill="#10A5FF" d="M31.9375 15.5625 L31.0625 15.5625 L31.0625 16.4375 L31.9375 16.4375 Z"/>
4690: +<path fill="#10A5FF" d="M27.9375 16.5625 L27.0625 16.5625 L27.0625 16.6875 L27.9375 16.6875 Z"/>
4691: +<path fill="#1963FF" d="M27.9375 16.6875 L27.0625 16.6875 L27.0625 17.4375 L27.9375 17.4375 Z"/>
4692: +<path fill="#10A5FF" d="M28.9375 16.5625 L28.0625 16.5625 L28.0625 16.6875 L28.9375 16.6875 Z"/>
4693: +<path fill="#1963FF" d="M28.9375 16.6875 L28.0625 16.6875 L28.0625 17.4375 L28.9375 17.4375 Z"/>
4694: +<path fill="#1963FF" d="M28.9375 17.5625 L28.0625 17.5625 L28.0625 18.0625 L28.9375 18.0625 Z"/>
4695: +<path fill="#1921B5" d="M28.9375 18.0625 L28.0625 18.0625 L28.0625 18.4375 L28.9375 18.4375 Z"/>
4696: +<path fill="#1963FF" d="M29.9375 17.5625 L29.0625 17.5625 L29.0625 18.0625 L29.9375 18.0625 Z"/>
4697: +<path fill="#1921B5" d="M29.9375 18.0625 L29.0625 18.0625 L29.0625 18.4375 L29.9375 18.4375 Z"/>
4698: +<path fill="#1963FF" d="M30.9375 17.5625 L30.0625 17.5625 L30.0625 18.0625 L30.9375 18.0625 Z"/>
4699: +<path fill="#1921B5" d="M30.9375 18.0625 L30.0625 18.0625 L30.0625 18.4375 L30.9375 18.4375 Z"/>
4700: +<path fill="#1963FF" d="M31.9375 17.5625 L31.0625 17.5625 L31.0625 18.0625 L31.9375 18.0625 Z"/>
4701: +<path fill="#1921B5" d="M31.9375 18.0625 L31.0625 18.0625 L31.0625 18.4375 L31.9375 18.4375 Z"/>
4702: +<path fill="#A5FFFF" d="M33.9375 13.5625 L33.0625 13.5625 L33.0625 13.9375 L33.9375 13.9375 Z"/>
4703: +<path fill="#10E6FF" d="M33.9375 13.9375 L33.0625 13.9375 L33.0625 14.4375 L33.9375 14.4375 Z"/>
4704: +<path fill="#A5FFFF" d="M34.9375 13.5625 L34.0625 13.5625 L34.0625 13.9375 L34.9375 13.9375 Z"/>
4705: +<path fill="#10E6FF" d="M34.9375 13.9375 L34.0625 13.9375 L34.0625 14.4375 L34.9375 14.4375 Z"/>
4706: +<path fill="#10E6FF" d="M33.9375 14.5625 L33.0625 14.5625 L33.0625 15.3125 L33.9375 15.3125 Z"/>
4707: +<path fill="#10A5FF" d="M33.9375 15.3125 L33.0625 15.3125 L33.0625 15.4375 L33.9375 15.4375 Z"/>
4708: +<path fill="#10E6FF" d="M34.9375 14.5625 L34.0625 14.5625 L34.0625 15.3125 L34.9375 15.3125 Z"/>
4709: +<path fill="#10A5FF" d="M34.9375 15.3125 L34.0625 15.3125 L34.0625 15.4375 L34.9375 15.4375 Z"/>
4710: +<path fill="#10A5FF" d="M33.9375 15.5625 L33.0625 15.5625 L33.0625 16.4375 L33.9375 16.4375 Z"/>
4711: +<path fill="#10A5FF" d="M34.9375 15.5625 L34.0625 15.5625 L34.0625 16.4375 L34.9375 16.4375 Z"/>
4712: +<path fill="#10A5FF" d="M33.9375 16.5625 L33.0625 16.5625 L33.0625 16.6875 L33.9375 16.6875 Z"/>
4713: +<path fill="#1963FF" d="M33.9375 16.6875 L33.0625 16.6875 L33.0625 17.4375 L33.9375 17.4375 Z"/>
4714: +<path fill="#10A5FF" d="M34.9375 16.5625 L34.0625 16.5625 L34.0625 16.6875 L34.9375 16.6875 Z"/>
4715: +<path fill="#1963FF" d="M34.9375 16.6875 L34.0625 16.6875 L34.0625 17.4375 L34.9375 17.4375 Z"/>
4716: +<path fill="#1963FF" d="M33.9375 17.5625 L33.0625 17.5625 L33.0625 18.0625 L33.9375 18.0625 Z"/>
4717: +<path fill="#1921B5" d="M33.9375 18.0625 L33.0625 18.0625 L33.0625 18.4375 L33.9375 18.4375 Z"/>
4718: +<path fill="#1963FF" d="M34.9375 17.5625 L34.0625 17.5625 L34.0625 18.0625 L34.9375 18.0625 Z"/>
4719: +<path fill="#1921B5" d="M34.9375 18.0625 L34.0625 18.0625 L34.0625 18.4375 L34.9375 18.4375 Z"/>
4720: +<path fill="#10E6FF" d="M37.9375 14.5625 L37.0625 14.5625 L37.0625 15.3125 L37.9375 15.3125 Z"/>
4721: +<path fill="#10A5FF" d="M37.9375 15.3125 L37.0625 15.3125 L37.0625 15.4375 L37.9375 15.4375 Z"/>
4722: +<path fill="#10E6FF" d="M38.9375 14.5625 L38.0625 14.5625 L38.0625 15.3125 L38.9375 15.3125 Z"/>
4723: +<path fill="#10A5FF" d="M38.9375 15.3125 L38.0625 15.3125 L38.0625 15.4375 L38.9375 15.4375 Z"/>
4724: +<path fill="#10E6FF" d="M39.9375 14.5625 L39.0625 14.5625 L39.0625 15.3125 L39.9375 15.3125 Z"/>
4725: +<path fill="#10A5FF" d="M39.9375 15.3125 L39.0625 15.3125 L39.0625 15.4375 L39.9375 15.4375 Z"/>
4726: +<path fill="#10E6FF" d="M40.9375 14.5625 L40.0625 14.5625 L40.0625 15.3125 L40.9375 15.3125 Z"/>
4727: +<path fill="#10A5FF" d="M40.9375 15.3125 L40.0625 15.3125 L40.0625 15.4375 L40.9375 15.4375 Z"/>
4728: +<path fill="#10A5FF" d="M36.9375 15.5625 L36.0625 15.5625 L36.0625 16.4375 L36.9375 16.4375 Z"/>
4729: +<path fill="#10A5FF" d="M37.9375 15.5625 L37.0625 15.5625 L37.0625 16.4375 L37.9375 16.4375 Z"/>
4730: +<path fill="#10A5FF" d="M39.9375 15.5625 L39.0625 15.5625 L39.0625 16.4375 L39.9375 16.4375 Z"/>
4731: +<path fill="#10A5FF" d="M40.9375 15.5625 L40.0625 15.5625 L40.0625 16.4375 L40.9375 16.4375 Z"/>
4732: +<path fill="#10A5FF" d="M36.9375 16.5625 L36.0625 16.5625 L36.0625 16.6875 L36.9375 16.6875 Z"/>
4733: +<path fill="#1963FF" d="M36.9375 16.6875 L36.0625 16.6875 L36.0625 17.4375 L36.9375 17.4375 Z"/>
4734: +<path fill="#10A5FF" d="M37.9375 16.5625 L37.0625 16.5625 L37.0625 16.6875 L37.9375 16.6875 Z"/>
4735: +<path fill="#1963FF" d="M37.9375 16.6875 L37.0625 16.6875 L37.0625 17.4375 L37.9375 17.4375 Z"/>
4736: +<path fill="#10A5FF" d="M39.9375 16.5625 L39.0625 16.5625 L39.0625 16.6875 L39.9375 16.6875 Z"/>
4737: +<path fill="#1963FF" d="M39.9375 16.6875 L39.0625 16.6875 L39.0625 17.4375 L39.9375 17.4375 Z"/>
4738: +<path fill="#10A5FF" d="M40.9375 16.5625 L40.0625 16.5625 L40.0625 16.6875 L40.9375 16.6875 Z"/>
4739: +<path fill="#1963FF" d="M40.9375 16.6875 L40.0625 16.6875 L40.0625 17.4375 L40.9375 17.4375 Z"/>
4740: +<path fill="#1963FF" d="M37.9375 17.5625 L37.0625 17.5625 L37.0625 18.0625 L37.9375 18.0625 Z"/>
4741: +<path fill="#1921B5" d="M37.9375 18.0625 L37.0625 18.0625 L37.0625 18.4375 L37.9375 18.4375 Z"/>
4742: +<path fill="#1963FF" d="M38.9375 17.5625 L38.0625 17.5625 L38.0625 18.0625 L38.9375 18.0625 Z"/>
4743: +<path fill="#1921B5" d="M38.9375 18.0625 L38.0625 18.0625 L38.0625 18.4375 L38.9375 18.4375 Z"/>
4744: +<path fill="#1963FF" d="M39.9375 17.5625 L39.0625 17.5625 L39.0625 18.0625 L39.9375 18.0625 Z"/>
4745: +<path fill="#1921B5" d="M39.9375 18.0625 L39.0625 18.0625 L39.0625 18.4375 L39.9375 18.4375 Z"/>
4746: +<path fill="#1963FF" d="M40.9375 17.5625 L40.0625 17.5625 L40.0625 18.0625 L40.9375 18.0625 Z"/>
4747: +<path fill="#1921B5" d="M40.9375 18.0625 L40.0625 18.0625 L40.0625 18.4375 L40.9375 18.4375 Z"/>
4748: +<path fill="#A5FFFF" d="M42.9375 13.5625 L42.0625 13.5625 L42.0625 13.9375 L42.9375 13.9375 Z"/>
4749: +<path fill="#10E6FF" d="M42.9375 13.9375 L42.0625 13.9375 L42.0625 14.4375 L42.9375 14.4375 Z"/>
4750: +<path fill="#A5FFFF" d="M43.9375 13.5625 L43.0625 13.5625 L43.0625 13.9375 L43.9375 13.9375 Z"/>
4751: +<path fill="#10E6FF" d="M43.9375 13.9375 L43.0625 13.9375 L43.0625 14.4375 L43.9375 14.4375 Z"/>
4752: +<path fill="#10E6FF" d="M42.9375 14.5625 L42.0625 14.5625 L42.0625 15.3125 L42.9375 15.3125 Z"/>
4753: +<path fill="#10A5FF" d="M42.9375 15.3125 L42.0625 15.3125 L42.0625 15.4375 L42.9375 15.4375 Z"/>
4754: +<path fill="#10E6FF" d="M43.9375 14.5625 L43.0625 14.5625 L43.0625 15.3125 L43.9375 15.3125 Z"/>
4755: +<path fill="#10A5FF" d="M43.9375 15.3125 L43.0625 15.3125 L43.0625 15.4375 L43.9375 15.4375 Z"/>
4756: +<path fill="#10E6FF" d="M44.9375 14.5625 L44.0625 14.5625 L44.0625 15.3125 L44.9375 15.3125 Z"/>
4757: +<path fill="#10A5FF" d="M44.9375 15.3125 L44.0625 15.3125 L44.0625 15.4375 L44.9375 15.4375 Z"/>
4758: +<path fill="#10A5FF" d="M42.9375 15.5625 L42.0625 15.5625 L42.0625 16.4375 L42.9375 16.4375 Z"/>
4759: +<path fill="#10A5FF" d="M43.9375 15.5625 L43.0625 15.5625 L43.0625 16.4375 L43.9375 16.4375 Z"/>
4760: +<path fill="#10A5FF" d="M42.9375 16.5625 L42.0625 16.5625 L42.0625 16.6875 L42.9375 16.6875 Z"/>
4761: +<path fill="#1963FF" d="M42.9375 16.6875 L42.0625 16.6875 L42.0625 17.4375 L42.9375 17.4375 Z"/>
4762: +<path fill="#10A5FF" d="M43.9375 16.5625 L43.0625 16.5625 L43.0625 16.6875 L43.9375 16.6875 Z"/>
4763: +<path fill="#1963FF" d="M43.9375 16.6875 L43.0625 16.6875 L43.0625 17.4375 L43.9375 17.4375 Z"/>
4764: +<path fill="#1963FF" d="M43.9375 17.5625 L43.0625 17.5625 L43.0625 18.0625 L43.9375 18.0625 Z"/>
4765: +<path fill="#1921B5" d="M43.9375 18.0625 L43.0625 18.0625 L43.0625 18.4375 L43.9375 18.4375 Z"/>
4766: +<path fill="#1963FF" d="M44.9375 17.5625 L44.0625 17.5625 L44.0625 18.0625 L44.9375 18.0625 Z"/>
4767: +<path fill="#1921B5" d="M44.9375 18.0625 L44.0625 18.0625 L44.0625 18.4375 L44.9375 18.4375 Z"/>
4768: +<path fill="#10E6FF" d="M47.9375 14.5625 L47.0625 14.5625 L47.0625 15.3125 L47.9375 15.3125 Z"/>
4769: +<path fill="#10A5FF" d="M47.9375 15.3125 L47.0625 15.3125 L47.0625 15.4375 L47.9375 15.4375 Z"/>
4770: +<path fill="#10E6FF" d="M48.9375 14.5625 L48.0625 14.5625 L48.0625 15.3125 L48.9375 15.3125 Z"/>
4771: +<path fill="#10A5FF" d="M48.9375 15.3125 L48.0625 15.3125 L48.0625 15.4375 L48.9375 15.4375 Z"/>
4772: +<path fill="#10E6FF" d="M49.9375 14.5625 L49.0625 14.5625 L49.0625 15.3125 L49.9375 15.3125 Z"/>
4773: +<path fill="#10A5FF" d="M49.9375 15.3125 L49.0625 15.3125 L49.0625 15.4375 L49.9375 15.4375 Z"/>
4774: +<path fill="#10A5FF" d="M46.9375 15.5625 L46.0625 15.5625 L46.0625 16.4375 L46.9375 16.4375 Z"/>
4775: +<path fill="#10A5FF" d="M47.9375 15.5625 L47.0625 15.5625 L47.0625 16.4375 L47.9375 16.4375 Z"/>
4776: +<path fill="#10A5FF" d="M48.9375 15.5625 L48.0625 15.5625 L48.0625 16.4375 L48.9375 16.4375 Z"/>
4777: +<path fill="#10A5FF" d="M49.9375 15.5625 L49.0625 15.5625 L49.0625 16.4375 L49.9375 16.4375 Z"/>
4778: +<path fill="#10A5FF" d="M50.9375 15.5625 L50.0625 15.5625 L50.0625 16.4375 L50.9375 16.4375 Z"/>
4779: +<path fill="#10A5FF" d="M46.9375 16.5625 L46.0625 16.5625 L46.0625 16.6875 L46.9375 16.6875 Z"/>
4780: +<path fill="#1963FF" d="M46.9375 16.6875 L46.0625 16.6875 L46.0625 17.4375 L46.9375 17.4375 Z"/>
4781: +<path fill="#10A5FF" d="M47.9375 16.5625 L47.0625 16.5625 L47.0625 16.6875 L47.9375 16.6875 Z"/>
4782: +<path fill="#1963FF" d="M47.9375 16.6875 L47.0625 16.6875 L47.0625 17.4375 L47.9375 17.4375 Z"/>
4783: +<path fill="#1963FF" d="M47.9375 17.5625 L47.0625 17.5625 L47.0625 18.0625 L47.9375 18.0625 Z"/>
4784: +<path fill="#1921B5" d="M47.9375 18.0625 L47.0625 18.0625 L47.0625 18.4375 L47.9375 18.4375 Z"/>
4785: +<path fill="#1963FF" d="M48.9375 17.5625 L48.0625 17.5625 L48.0625 18.0625 L48.9375 18.0625 Z"/>
4786: +<path fill="#1921B5" d="M48.9375 18.0625 L48.0625 18.0625 L48.0625 18.4375 L48.9375 18.4375 Z"/>
4787: +<path fill="#1963FF" d="M49.9375 17.5625 L49.0625 17.5625 L49.0625 18.0625 L49.9375 18.0625 Z"/>
4788: +<path fill="#1921B5" d="M49.9375 18.0625 L49.0625 18.0625 L49.0625 18.4375 L49.9375 18.4375 Z"/>
4789: +<path fill="#1963FF" d="M50.9375 17.5625 L50.0625 17.5625 L50.0625 18.0625 L50.9375 18.0625 Z"/>
4790: +<path fill="#1921B5" d="M50.9375 18.0625 L50.0625 18.0625 L50.0625 18.4375 L50.9375 18.4375 Z"/>
4791: +<path fill="#A5FFFF" d="M56.9375 13.5625 L56.0625 13.5625 L56.0625 13.9375 L56.9375 13.9375 Z"/>
4792: +<path fill="#10E6FF" d="M56.9375 13.9375 L56.0625 13.9375 L56.0625 14.4375 L56.9375 14.4375 Z"/>
4793: +<path fill="#A5FFFF" d="M55.9375 13.5625 L55.0625 13.5625 L55.0625 13.9375 L55.9375 13.9375 Z"/>
4794: +<path fill="#10E6FF" d="M55.9375 13.9375 L55.0625 13.9375 L55.0625 14.4375 L55.9375 14.4375 Z"/>
4795: +<path fill="#10E6FF" d="M56.9375 14.5625 L56.0625 14.5625 L56.0625 15.3125 L56.9375 15.3125 Z"/>
4796: +<path fill="#10A5FF" d="M56.9375 15.3125 L56.0625 15.3125 L56.0625 15.4375 L56.9375 15.4375 Z"/>
4797: +<path fill="#10E6FF" d="M55.9375 14.5625 L55.0625 14.5625 L55.0625 15.3125 L55.9375 15.3125 Z"/>
4798: +<path fill="#10A5FF" d="M55.9375 15.3125 L55.0625 15.3125 L55.0625 15.4375 L55.9375 15.4375 Z"/>
4799: +<path fill="#10E6FF" d="M54.9375 14.5625 L54.0625 14.5625 L54.0625 15.3125 L54.9375 15.3125 Z"/>
4800: +<path fill="#10A5FF" d="M54.9375 15.3125 L54.0625 15.3125 L54.0625 15.4375 L54.9375 15.4375 Z"/>
4801: +<path fill="#10E6FF" d="M53.9375 14.5625 L53.0625 14.5625 L53.0625 15.3125 L53.9375 15.3125 Z"/>
4802: +<path fill="#10A5FF" d="M53.9375 15.3125 L53.0625 15.3125 L53.0625 15.4375 L53.9375 15.4375 Z"/>
4803: +<path fill="#10A5FF" d="M53.9375 15.5625 L53.0625 15.5625 L53.0625 16.4375 L53.9375 16.4375 Z"/>
4804: +<path fill="#10A5FF" d="M56.9375 15.5625 L56.0625 15.5625 L56.0625 16.4375 L56.9375 16.4375 Z"/>
4805: +<path fill="#10A5FF" d="M55.9375 15.5625 L55.0625 15.5625 L55.0625 16.4375 L55.9375 16.4375 Z"/>
4806: +<path fill="#10A5FF" d="M52.9375 15.5625 L52.0625 15.5625 L52.0625 16.4375 L52.9375 16.4375 Z"/>
4807: +<path fill="#10A5FF" d="M56.9375 16.5625 L56.0625 16.5625 L56.0625 16.6875 L56.9375 16.6875 Z"/>
4808: +<path fill="#1963FF" d="M56.9375 16.6875 L56.0625 16.6875 L56.0625 17.4375 L56.9375 17.4375 Z"/>
4809: +<path fill="#10A5FF" d="M55.9375 16.5625 L55.0625 16.5625 L55.0625 16.6875 L55.9375 16.6875 Z"/>
4810: +<path fill="#1963FF" d="M55.9375 16.6875 L55.0625 16.6875 L55.0625 17.4375 L55.9375 17.4375 Z"/>
4811: +<path fill="#10A5FF" d="M53.9375 16.5625 L53.0625 16.5625 L53.0625 16.6875 L53.9375 16.6875 Z"/>
4812: +<path fill="#1963FF" d="M53.9375 16.6875 L53.0625 16.6875 L53.0625 17.4375 L53.9375 17.4375 Z"/>
4813: +<path fill="#10A5FF" d="M52.9375 16.5625 L52.0625 16.5625 L52.0625 16.6875 L52.9375 16.6875 Z"/>
4814: +<path fill="#1963FF" d="M52.9375 16.6875 L52.0625 16.6875 L52.0625 17.4375 L52.9375 17.4375 Z"/>
4815: +<path fill="#1963FF" d="M53.9375 17.5625 L53.0625 17.5625 L53.0625 18.0625 L53.9375 18.0625 Z"/>
4816: +<path fill="#1921B5" d="M53.9375 18.0625 L53.0625 18.0625 L53.0625 18.4375 L53.9375 18.4375 Z"/>
4817: +<path fill="#1963FF" d="M56.9375 17.5625 L56.0625 17.5625 L56.0625 18.0625 L56.9375 18.0625 Z"/>
4818: +<path fill="#1921B5" d="M56.9375 18.0625 L56.0625 18.0625 L56.0625 18.4375 L56.9375 18.4375 Z"/>
4819: +<path fill="#1963FF" d="M55.9375 17.5625 L55.0625 17.5625 L55.0625 18.0625 L55.9375 18.0625 Z"/>
4820: +<path fill="#1921B5" d="M55.9375 18.0625 L55.0625 18.0625 L55.0625 18.4375 L55.9375 18.4375 Z"/>
4821: +<path fill="#1963FF" d="M54.9375 17.5625 L54.0625 17.5625 L54.0625 18.0625 L54.9375 18.0625 Z"/>
4822: +<path fill="#1921B5" d="M54.9375 18.0625 L54.0625 18.0625 L54.0625 18.4375 L54.9375 18.4375 Z"/>
4823: +</g>
4824: +</svg>
4825: diff --git a/scripts/build b/scripts/build
4826: index e746446125..574516d541 100755
4827: --- a/scripts/build
4828: +++ b/scripts/build
4829: @@ -4,6 +4,12 @@
4830:  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
4831:  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
4832:  
4833: +# Fork build monitoring: nested calls reuse the outer run (#394).
4834: +if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
4835: +  exec ./tools/watch-build --entry -- "$0" "$@"
4836: +fi
4837: +unset RASTERATOPS_WATCH_EXEC
4838: +
4839:  . config/options "${1}"
4840:  
4841:  record_timestamp BUILD_BEGIN
4842: diff --git a/scripts/build_compat b/scripts/build_compat
4843: index 5af9525eed..048734ad10 100755
4844: --- a/scripts/build_compat
4845: +++ b/scripts/build_compat
4846: @@ -2,6 +2,12 @@
4847:  # SPDX-License-Identifier: GPL-2.0
4848:  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
4849:  
4850: +# Fork build monitoring: nested calls reuse the outer run (#394).
4851: +if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
4852: +  exec ./tools/watch-build --entry -- "$0" "$@"
4853: +fi
4854: +unset RASTERATOPS_WATCH_EXEC
4855: +
4856:  unset _CACHE_PACKAGE_LOCAL _CACHE_PACKAGE_GLOBAL _DEBUG_DEPENDS_LIST _DEBUG_PACKAGE_LIST
4857:  
4858:  . config/options ""
4859: diff --git a/scripts/build_distro b/scripts/build_distro
4860: index 21fad95f0d..f2e6df5eba 100755
4861: --- a/scripts/build_distro
4862: +++ b/scripts/build_distro
4863: @@ -6,6 +6,12 @@
4864:  ### Simple script to build ROCKNX
4865:  ###
4866:  
4867: +# Fork build monitoring: nested calls reuse the outer run (#394).
4868: +if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
4869: +  exec ./tools/watch-build --entry -- "$0" "$@"
4870: +fi
4871: +unset RASTERATOPS_WATCH_EXEC
4872: +
4873:  set -e
4874:  
4875:  scripts/checkdeps
4876: diff --git a/scripts/image b/scripts/image
4877: index 2ff53ffa98..752b2c57aa 100755
4878: --- a/scripts/image
4879: +++ b/scripts/image
4880: @@ -4,6 +4,12 @@
4881:  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
4882:  # Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
4883:  
4884: +# Fork build monitoring: nested calls reuse the outer run (#394).
4885: +if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
4886: +  exec ./tools/watch-build --entry -- "$0" "$@"
4887: +fi
4888: +unset RASTERATOPS_WATCH_EXEC
4889: +
4890:  unset _CACHE_PACKAGE_LOCAL _CACHE_PACKAGE_GLOBAL _DEBUG_DEPENDS_LIST _DEBUG_PACKAGE_LIST
4891:  
4892:  . config/options ""
4893: @@ -196,6 +202,17 @@ if [ -n "${DEVICE}" ] && [ -d "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/files
4894:    done
4895:  fi
4896:  
4897: +# Keep the fork's approved identity terms with its artwork in SYSTEM (#397).
4898: +# Install the authoritative files at image assembly time so a text change
4899: +# cannot be hidden by an unchanged package build stamp.
4900: +if [ "${DISTRONAME}" = "pixelelated" ]; then
4901: +  for policy in LICENSE.md TRADEMARK.md; do
4902: +    install -D -m 0644 "${ROOT}/${policy}" \
4903: +      "${INSTALL}/usr/share/licenses/pixelelated/${policy}" \
4904: +      || die "Unable to install pixelelated identity policy: ${policy}"
4905: +  done
4906: +fi
4907: +
4908:  # Replace placeholders with values in install script to eMMC
4909:  if [ -f ${INSTALL}/usr/bin/install2emmc ]; then
4910:    sed -e "s%@SYSTEM_SIZE@%${SYSTEM_SIZE}%g" \
4911: diff --git a/scripts/install b/scripts/install
4912: index 7069dba659..daeb62a87d 100755
4913: --- a/scripts/install
4914: +++ b/scripts/install
4915: @@ -5,6 +5,12 @@
4916:  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
4917:  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
4918:  
4919: +# Fork build monitoring: nested calls reuse the outer run (#394).
4920: +if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
4921: +  exec ./tools/watch-build --entry -- "$0" "$@"
4922: +fi
4923: +unset RASTERATOPS_WATCH_EXEC
4924: +
4925:  . config/options "${1}"
4926:  
4927:  if [ -z "${1}" ]; then
```


## SOURCE docs/audits/2026_10_06-milestone-m7-p4-fixes-383/inputs/es-diff.patch

```text
1: diff --git a/es-app/src/ApiSystem.cpp b/es-app/src/ApiSystem.cpp
2: index 4bc0989d1..323267a82 100644
3: --- a/es-app/src/ApiSystem.cpp
4: +++ b/es-app/src/ApiSystem.cpp
5: @@ -171,7 +171,8 @@ std::string ApiSystem::getVersion(bool extra)
6:  
7:  std::string ApiSystem::getApplicationName()
8:  {
9: -	return "ROCKNIX";
10: +    const std::string name = Utils::Platform::GetEnv("OS_NAME");
11: +    return name.empty() ? "ROCKNIX" : name;
12:  }
13:  
14:  bool ApiSystem::setOverscan(bool enable) 
15: @@ -447,6 +448,9 @@ bool ApiSystem::canArchitectureUpdate(std::string& architecture) {
16:  bool ApiSystem::canUpdate(std::vector<std::string>& output) 
17:  {
18:  	LOG(LogDebug) << "ApiSystem::canUpdate";
19: +    // Manual adoption in pixelelated0.0.1, including inherited force settings.
20: +    if (getApplicationName() == "pixelelated")
21: +        return false;
22:  
23:  	FILE *pipe = popen("rocknix-update check", "r");
24:  	if (pipe == NULL)
25: diff --git a/es-app/src/FileData.cpp b/es-app/src/FileData.cpp
26: index e463b20d7..15d9a1bed 100644
27: --- a/es-app/src/FileData.cpp
28: +++ b/es-app/src/FileData.cpp
29: @@ -40,6 +40,9 @@
30:  #include "guis/GuiLoading.h"
31:  #include "views/ViewController.h"
32:  #include <chrono>
33: +#if defined(__GLIBC__)
34: +#include <malloc.h>
35: +#endif
36:  #include <thread>
37:  #include <atomic>
38:  #include "OfflineAchievements.h"
39: @@ -1070,6 +1073,12 @@ bool FileData::launchGame(Window* window, LaunchGameOptions options)
40:  
41:  	bool hideWindow = Settings::getInstance()->getBool("HideWindow");
42:  	window->deinit(hideWindow);
43: +
44: +#if defined(__GLIBC__)
45: +	// Renderer teardown frees large heaps which glibc may keep mapped.
46: +	// Return those pages before the emulator needs memory (distro #310).
47: +	malloc_trim(0);
48: +#endif
49:  	
50:  	const std::string rom = Utils::FileSystem::getEscapedPath(getPath());
51:  	const std::string basename = Utils::FileSystem::getStem(getPath());
52: @@ -1201,6 +1210,12 @@ bool FileData::launchGame(Window* window, LaunchGameOptions options)
53:  
54:  	window->reactivateGui();
55:  
56: +#if defined(__GLIBC__)
57: +	// Resource reload also leaves temporary heap pages behind. Release
58: +	// them once the interface is ready, rather than accumulating them.
59: +	malloc_trim(0);
60: +#endif
61: +
62:  	// A screenshot taken in this session is in a folder the viewer scanned
63:  	// at boot. Re-read the folders that changed, once the launch has fully
64:  	// unwound (#82; the rescan may delete this very FileData when the game
65: diff --git a/es-app/src/guis/GuiMenu.cpp b/es-app/src/guis/GuiMenu.cpp
66: index 1295575ae..2d399196e 100644
67: --- a/es-app/src/guis/GuiMenu.cpp
68: +++ b/es-app/src/guis/GuiMenu.cpp
69: @@ -559,8 +559,8 @@ void GuiMenu::addVersionInfo()
70:  
71:  	if (!ApiSystem::getInstance()->getVersion().empty())
72:  	{
73: -		if (ApiSystem::getInstance()->getApplicationName() == "ROCKNIX")
74: -			label = "ROCKNIX " + ApiSystem::getInstance()->getVersion() + " (" + ApiSystem::getInstance()->getVersion(true) + ")";
75: +		if (ApiSystem::getInstance()->getApplicationName() == "ROCKNIX" || ApiSystem::getInstance()->getApplicationName() == "pixelelated")
76: +			label = ApiSystem::getInstance()->getApplicationName() + " " + ApiSystem::getInstance()->getVersion() + " (" + ApiSystem::getInstance()->getVersion(true) + ")";
77:  		else
78:  		{
79:  			std::string aboutInfo = ApiSystem::getInstance()->getApplicationName() + " V" + ApiSystem::getInstance()->getVersion();
80: @@ -1502,9 +1502,18 @@ void GuiMenu::openUpdatesSettings(bool selectTorrentService)
81:  		});
82:  	}
83:  
84: -	if (ApiSystem::getInstance()->isScriptingSupported(ApiSystem::UPGRADE))
85: -	{
86: -		updateGui->addGroup(_("SOFTWARE UPDATES"));
87: +    if (ApiSystem::getInstance()->getApplicationName() == "pixelelated")
88: +    {
89: +        updateGui->addGroup(_("SOFTWARE UPDATES"));
90: +        updateGui->addEntry(_("MANUAL UPDATES"), true, [this]
91: +        {
92: +            mWindow->pushGui(new GuiMsgBox(mWindow,
93: +                _("This version uses manual updates. Open github.com/pixelelated/distribution/releases on a computer, choose the update for your device, and follow the instructions."), _("OK")));
94: +        });
95: +    }
96: +    else if (ApiSystem::getInstance()->isScriptingSupported(ApiSystem::UPGRADE))
97: +    {
98: +        updateGui->addGroup(_("SOFTWARE UPDATES"));
99:  
100:  		// Enable updates
101:  		updateGui->addSwitch(_("CHECK FOR UPDATES"), "updates.enabled", false);
102: @@ -1975,7 +1984,16 @@ void GuiMenu::openSystemSettings()
103:        auto rocknix_screenshot_enabled = std::make_shared<SwitchComponent>(mWindow);
104:        bool rocknixscreenshotenabled = SystemConf::getInstance()->get("rocknix.screenshot.enabled") == "1";
105:        rocknix_screenshot_enabled->setState(SystemConf::getInstance()->getBool("rocknix.screenshot.enabled"));
106: -      s->addWithLabel(_("ENABLE ROCKNIX SCREENSHOT"), rocknix_screenshot_enabled);
107: +      // This brand stays lowercase; addWithLabel uppercases the entire label.
108: +      ComponentListRow screenshotRow;
109: +      auto screenshotTheme = ThemeData::getMenuTheme();
110: +      auto screenshotLabel = std::make_shared<TextComponent>(mWindow,
111: +          _("ENABLE pixelelated SCREENSHOT"), screenshotTheme->Text.font, screenshotTheme->Text.color);
112: +      if (EsLocale::isRTL())
113: +          screenshotLabel->setHorizontalAlignment(Alignment::ALIGN_RIGHT);
114: +      screenshotRow.addElement(screenshotLabel, true);
115: +      screenshotRow.addElement(rocknix_screenshot_enabled, false);
116: +      s->addRow(screenshotRow);
117:        rocknix_screenshot_enabled->setOnChangedCallback([rocknix_screenshot_enabled] {
118:                bool rocknixscreenshotenabled = rocknix_screenshot_enabled->getState();
119:                       SystemConf::getInstance()->set("rocknix.screenshot.enabled", rocknixscreenshotenabled ? "1" : "0");
120: @@ -2321,6 +2339,10 @@ void GuiMenu::openSystemSettings()
121:  	s->addWithLabel(_("DEFAULT GPU SCALING GOVERNOR"), optionsGpuGovernors);
122:  	s->addSaveFunc([selectedGpuGovernor, optionsGpuGovernors]
123:  	{
124: +		// A device without GPU governor support has no option to apply.
125: +		if (!optionsGpuGovernors->hasSelection())
126: +			return;
127: +
128:  		if (optionsGpuGovernors->changed()) {
129:  			SystemConf::getInstance()->set("system.gpuperf", optionsGpuGovernors->getSelected());
130:  		}
131: @@ -5318,8 +5340,26 @@ static void cloudOfferFolder(Window* window, const CloudFolderAsk& ask)
132:  	const std::function<void()> abandon = ask.abandon;
133:  	const auto st = cloudScanFacts("state");
134:  	const std::string state = cloudScanFact(st, "STATE");
135: -	const std::string current = cloudScanFact(st, "CURRENT").empty() ? "/Rasteratops/Saves" : cloudScanFact(st, "CURRENT");
136: +	const std::string current = cloudScanFact(st, "CURRENT").empty() ? "/pixelelated/Saves" : cloudScanFact(st, "CURRENT");
137:  	const std::string newRoot = cloudRootOf(current);
138: +	if (state == "migration-pending")
139: +	{
140: +		LOG(LogInfo) << "cloud folder: interrupted move; offering retry";
141: +		window->pushGui(new GuiMsgBox(window,
142: +			_("YOUR CLOUD FOLDER MOVE DIDN'T FINISH.\n\nTRY AGAIN? FILES ALREADY MOVED WILL BE KEPT."),
143: +			_("TRY AGAIN"), [window, newRoot, rescan, abandon]
144: +			{
145: +				auto page = new GuiCloudTransfer(window, "/usr/bin/cloud_migrate_layout --apply", _("MOVING YOUR CLOUD FOLDER"));
146: +				page->setFailedNote(_("WHAT MOVED IS IN THE NEW FOLDER. TRY AGAIN TO FINISH."));
147: +				page->setCompletedAction(rescan, _("CONTINUE"), _("PRESS ANY BUTTON TO CONTINUE"),
148: +					Utils::String::format(_("YOUR CLOUD FOLDER IS NOW %s.").c_str(), newRoot.c_str()), true);
149: +				if (abandon)
150: +					page->setDismissedAction(abandon);
151: +				window->pushGui(page);
152: +			},
153: +			_("NOT NOW"), then));
154: +		return;
155: +	}
156:  	if (state == "superseded-with-files")
157:  	{
158:  		const std::string source = cloudScanFact(st, "SOURCE") == "-" || cloudScanFact(st, "SOURCE").empty()
159: @@ -5333,7 +5373,7 @@ static void cloudOfferFolder(Window* window, const CloudFolderAsk& ask)
160:  			{
161:  				LOG(LogInfo) << "cloud folder: moving " << oldRoot << " to " << newRoot;
162:  				auto page = new GuiCloudTransfer(window, "/usr/bin/cloud_migrate_layout --apply", _("MOVING YOUR CLOUD FOLDER"));
163: -				page->setFailedNote(Utils::String::format(_("YOUR CLOUD STILL HAS %s. NOTHING WAS REMOVED.").c_str(), oldRoot.c_str()));
164: +				page->setFailedNote(_("WHAT MOVED IS IN THE NEW FOLDER. TRY AGAIN TO FINISH."));
165:  				// One short sentence: the longer one, naming the three tiers,
166:  				// was cut at 640 px (guest d, 2026-10-01).
167:  				page->setCompletedAction(rescan, _("CONTINUE"), _("PRESS ANY BUTTON TO CONTINUE"),
168: @@ -5547,8 +5587,13 @@ static bool cloudFolderStepIfQuiet(Window* window)
169:  	if (sCloudFolderStepOffered)
170:  		return true;
171:  	if (window->peekGui() != ViewController::get() || FileData::GetRunningGame() != nullptr
172: -		|| ThreadedCloudSync::isRunning() || CloudTransferJob::running())
173: +		|| ThreadedCloudSync::isRunning() || CloudTransferJob::running()
174: +		|| window->hasAsyncNotifications())
175:  		return false;
176: +
177: +	// Worker completion releases the sync lock before its outcome card's
178: +	// linger and fade finish. Let the actual window relinquish that surface
179: +	// before the setup step takes it (#363), including any queued card.
180:  	sCloudFolderStepOffered = true;
181:  	cloudFolderStepAtBoot(window);
182:  	return true;
183: @@ -5782,7 +5827,7 @@ static void cloudPreviewTidyFolders(Window* window)
184:  // The row's line, from what the check would move: one whole sentence per
185:  // shape, each with its French, the tiers in the vocabulary's words. The
186:  // line used to name /ROCKNIX, the folder of an earlier build, on a build
187: -// whose folder is /Rasteratops, and SAVES AND SETTINGS BACKUPS when the
188: +// whose folder is /pixelelated, and SAVES AND SETTINGS BACKUPS when the
189:  // check planned the content folder alone (2026-10-01, fork #353).
190:  static std::string cloudTidyLine(const CloudText::TidyPlan& plan)
191:  {
192: diff --git a/es-app/src/main.cpp b/es-app/src/main.cpp
193: index ad2b5717d..a11963bb1 100644
194: --- a/es-app/src/main.cpp
195: +++ b/es-app/src/main.cpp
196: @@ -675,6 +675,16 @@ static void startStartupSavesSync(Window* window)
197:  		" done;"
198:  		" [ \"$_up\" = 1 ] || exit " + noNetwork + ";"
199:  		" fi;"
200: +		// Boot-only preparation uses the same join/follow classifier as the
201: +		// folder page. It must precede writes: a startup backup into an empty
202: +		// old folder could otherwise make it win over the fleet's real saves
203: +		// (#365, T08/T11/T12). This does not show or apply the move; its page
204: +		// still waits for this worker and its outcome card to finish.
205: +		" if [ -x /usr/bin/cloud_migrate_layout ] && [ -x /usr/bin/cloud_scan ]; then"
206: +		" /usr/bin/cloud_migrate_layout --needs-step >/dev/null 2>&1; _s=$?;"
207: +		" if [ \"$_s\" = 0 ]; then"
208: +		" timeout 30 /usr/bin/cloud_scan --folder; _s=$?; [ \"$_s\" = 0 ] || exit \"$_s\";"
209: +		" elif [ \"$_s\" != 1 ]; then exit \"$_s\"; fi; fi;"
210:  		" echo \">>> doing receive\";"
211:  		" /usr/bin/cloud_restore --yes --method=copy --update --saves-only --automatic; _r=$?;"
212:  		" echo \">>> tier RESTORING SAVES|$_r\";"
213: @@ -924,7 +934,7 @@ int main(int argc, char* argv[])
214:  		f.close();
215:  
216:  		if (val == "1")
217: -		window.pushGui(new GuiMsgBox(&window, "ROCKNIX IS FREE SOFTWARE.\n\n IF YOU PAID FOR ROCKNIX YOU HAVE BEEN SCAMMED.\n\n PLEASE REQUEST A REFUND FROM THE SELLER!", _("AGREE")));
218: +		window.pushGui(new GuiMsgBox(&window, "pixelelated IS FREE SOFTWARE.\n\n IF YOU PAID FOR pixelelated YOU HAVE BEEN SCAMMED.\n\n PLEASE REQUEST A REFUND FROM THE SELLER!", _("AGREE")));
219:  
220:  		std::remove(markerFile.c_str());
221:  	}
222: diff --git a/es-app/tests/unit/SystemConfTests.cpp b/es-app/tests/unit/SystemConfTests.cpp
223: index 81e89960e..90d991e41 100644
224: --- a/es-app/tests/unit/SystemConfTests.cpp
225: +++ b/es-app/tests/unit/SystemConfTests.cpp
226: @@ -94,6 +94,12 @@ struct SystemConfTestAccess
227:  		return SystemConf::getInstance();
228:  	}
229:  
230: +	// Resume at the actual publication boundary with a captured earlier read.
231: +	static void record(SystemConf* conf, const std::string& snapshot)
232: +	{
233: +		conf->recordLastGood(snapshot);
234: +	}
235: +
236:  	static bool recovered() { return SystemConf::sRecovered; }
237:  };
238:  
239: @@ -455,3 +461,46 @@ TEST_CASE("a record cut short is neither loaded nor recorded, and the defaults a
240:  		CHECK(get(path + ".backup") == whole);
241:  	}
242:  }
243: +
244: +TEST_CASE("a script's newer good state published between the read and the record is not overwritten")
245: +{
246: +	ScratchDir dir;
247: +	const std::string path = dir / "system.cfg";
248: +	const std::string lockPath = dir / ".system.cfg.lock";
249: +	const std::string earlier = "system.hostname=A\naudio.volume=70\n";
250: +	const std::string newer = "system.hostname=A\naudio.volume=40\n";
251: +	put(path, earlier);
252: +	SystemConf* conf = SystemConfTestAccess::fresh(path, lockPath, 20);
253: +	// The loader/save retains this snapshot while a script gets its turn.
254: +	const std::string snapshot = get(path);
255: +	{
256: +		PidLock script(lockPath);
257: +		REQUIRE(script.acquire(1000));
258: +		REQUIRE(Utils::AtomicFile::writeText(path, newer, 0600));
259: +		REQUIRE(Utils::AtomicFile::writeText(path + ".backup", newer, 0600));
260: +	}
261: +	SystemConfTestAccess::record(conf, snapshot);
262: +	CHECK(get(path) == newer);
263: +	CHECK(get(path + ".backup") == newer);
264: +	CHECK(modeOf(path + ".backup") == 0600);
265: +}
266: +
267: +TEST_CASE("LockBusy recovery reads its temporary without publishing over the holder's record")
268: +{
269: +	ScratchDir dir;
270: +	const std::string path = dir / "system.cfg";
271: +	const std::string lockPath = dir / ".system.cfg.lock";
272: +	const std::string unfinished = "system.hostname=A\naudio.volume=70\n";
273: +	const std::string recorded = "system.hostname=A\naudio.volume=40\n";
274: +	put(path, "system.hostname=A\naudio.vol");
275: +	put(path + ".tmp", unfinished);
276: +	put(path + ".backup", recorded);
277: +	PidLock script(lockPath);
278: +	REQUIRE(script.acquire(1000));
279: +	SystemConf* conf = SystemConfTestAccess::fresh(path, lockPath, 20);
280: +	CHECK(conf->get("audio.volume") == "70");
281: +	CHECK(SystemConfTestAccess::recovered());
282: +	CHECK(get(path) == "system.hostname=A\naudio.vol");
283: +	CHECK(get(path + ".backup") == recorded);
284: +	CHECK(get(path + ".tmp") == unfinished);
285: +}
286: diff --git a/es-core/src/GunManager.cpp b/es-core/src/GunManager.cpp
287: index 11bd02430..c6ba2270a 100644
288: --- a/es-core/src/GunManager.cpp
289: +++ b/es-core/src/GunManager.cpp
290: @@ -938,6 +938,7 @@ void GunManager::udev_initial_gunsList()
291:  	bool bGunborder;
292:  
293:  	struct udev_enumerate *enumerate = udev_enumerate_new(udev);
294: +	if (enumerate == NULL) return;
295:  	udev_enumerate_add_match_property(enumerate, "ID_INPUT_GUN", "1");
296:  	udev_enumerate_add_match_subsystem(enumerate, "input");
297:  	udev_enumerate_scan_devices(enumerate);
298: @@ -956,6 +957,7 @@ void GunManager::udev_initial_gunsList()
299:  
300:  		if (udev_addGun(dev, NULL, bGunborder) == false) udev_device_unref(dev); // unhandled device
301:  	}
302: +	udev_enumerate_unref(enumerate);
303:  }
304:  
305:  bool GunManager::udev_addGun(struct udev_device *dev, Window* window, bool needGunBorder)
306: diff --git a/es-core/src/InputConfig.cpp b/es-core/src/InputConfig.cpp
307: index eac76c64d..f149f45f4 100644
308: --- a/es-core/src/InputConfig.cpp
309: +++ b/es-core/src/InputConfig.cpp
310: @@ -69,6 +69,7 @@ std::string getDeviceParentSyspath(const std::string& path) {
311:    if (udev != NULL)
312:      {
313:        struct udev_enumerate *enumerate = udev_enumerate_new(udev);
314: +      if (enumerate == NULL) { udev_unref(udev); return res; }
315:        udev_enumerate_add_match_subsystem(enumerate, "input");
316:        udev_enumerate_scan_devices(enumerate);
317:        devs = udev_enumerate_get_list_entry(enumerate);
318: @@ -85,6 +86,7 @@ std::string getDeviceParentSyspath(const std::string& path) {
319:  		const char *bt_parent_sysname = udev_device_get_syspath(bt_parent);
320:  		res = bt_parent_sysname;
321:  		udev_device_unref(ud);
322: +		udev_enumerate_unref(enumerate);
323:  		udev_unref(udev);
324:  		return res;
325:  	      }
326: @@ -95,6 +97,7 @@ std::string getDeviceParentSyspath(const std::string& path) {
327:  		const char *usb_parent_sysname = udev_device_get_syspath(usb_parent);
328:  		res = usb_parent_sysname;
329:  		udev_device_unref(ud);
330: +		udev_enumerate_unref(enumerate);
331:  		udev_unref(udev);
332:  		return res;
333:  	      }
334: @@ -103,10 +106,12 @@ std::string getDeviceParentSyspath(const std::string& path) {
335:  
336:  	    // fallback (should not happen) ; return the device path
337:  	    res = name;
338: +	    udev_enumerate_unref(enumerate);
339:  	    udev_unref(udev);
340: -	    return name;
341: +	    return res;
342:  	  }
343:  	}
344: +      udev_enumerate_unref(enumerate);
345:        udev_unref(udev);
346:      }
347:    return "";
348: @@ -140,6 +145,7 @@ bool InputConfig::isWheel(const std::string path) {
349:  	if (udev != NULL)
350:  	  {
351:  	    struct udev_enumerate *enumerate = udev_enumerate_new(udev);
352: +	    if (enumerate == NULL) { udev_unref(udev); return false; }
353:  	    udev_enumerate_add_match_property(enumerate, "ID_INPUT_WHEEL", "1");
354:  	    udev_enumerate_add_match_subsystem(enumerate, "input");
355:  	    udev_enumerate_scan_devices(enumerate);
356: @@ -160,6 +166,7 @@ bool InputConfig::isWheel(const std::string path) {
357:  	    	}
358:  	    	udev_device_unref(dev);
359:  	      }
360: +	    udev_enumerate_unref(enumerate);
361:  	    udev_unref(udev);
362:  	  }
363:  	return res;
364: diff --git a/es-core/src/InputManager.cpp b/es-core/src/InputManager.cpp
365: index b8da3ee39..2da307f66 100644
366: --- a/es-core/src/InputManager.cpp
367: +++ b/es-core/src/InputManager.cpp
368: @@ -117,6 +117,7 @@ std::vector<std::string> InputManager::getMice() {
369:    if (udev != NULL)
370:      {
371:        struct udev_enumerate *enumerate = udev_enumerate_new(udev);
372: +      if (enumerate == NULL) { udev_unref(udev); return mice; }
373:        udev_enumerate_add_match_property(enumerate, "ID_INPUT_MOUSE", "1");
374:        udev_enumerate_add_match_subsystem(enumerate, "input");
375:        udev_enumerate_scan_devices(enumerate);
376: @@ -141,6 +142,7 @@ std::vector<std::string> InputManager::getMice() {
377:  	  udev_device_unref(dev);
378:  	}
379:  
380: +      udev_enumerate_unref(enumerate);
381:        udev_unref(udev);
382:      }
383:    #endif
384: diff --git a/es-core/src/Splash.h b/es-core/src/Splash.h
385: index 2daf55e36..8705ab81a 100644
386: --- a/es-core/src/Splash.h
387: +++ b/es-core/src/Splash.h
388: @@ -7,7 +7,10 @@
389:  class Window;
390:  class TextureResource;
391:  
392: -#if WIN32
393: +#if defined(ROCKNIX)
394: +#define DEFAULT_SPLASH_IMAGE ":/pixelelated-wordmark.svg"
395: +#define OLD_SPLASH_LAYOUT true
396: +#elif WIN32
397:  #define DEFAULT_SPLASH_IMAGE ":/splash.svg"
398:  #define OLD_SPLASH_LAYOUT true
399:  #else
400: diff --git a/es-core/src/SystemConf.cpp b/es-core/src/SystemConf.cpp
401: index 8d6ccf2a0..1869f3f9d 100644
402: --- a/es-core/src/SystemConf.cpp
403: +++ b/es-core/src/SystemConf.cpp
404: @@ -85,6 +85,17 @@ void SystemConf::parseSystemConf(const std::string& text)
405:  // every start and after every save, and most of those change nothing.
406:  void SystemConf::recordLastGood(const std::string& text, int recoveredMode)
407:  {
408: +	// The load/save released its lock before reaching this publication.
409: +	// Reacquire and compare the complete current choice under the lock: a
410: +	// script's newer state must win over this call's older snapshot (#320).
411: +	Utils::AtomicFile::PidLock lock(sLockPath);
412: +	if (!lock.acquire(sLockBudgetMs))
413: +		return;
414: +	const auto current = Utils::AtomicFile::chooseConfig(mSystemConfFile);
415: +	if (current.text != text ||
416: +		(!current.record && current.source != Utils::AtomicFile::LoadedConfig::Source::Backup))
417: +		return;
418: +
419:  	// No less private than the live file it copies (#308 F-ES-08): a record
420:  	// an earlier build made 0644 beside a 0600 file is rewritten for its mode
421:  	// even when its text is the same. A recovery passes the mode every copy
422: @@ -93,7 +104,7 @@ void SystemConf::recordLastGood(const std::string& text, int recoveredMode)
423:  	// is no file -- made a 0600 temporary's text a 0644 record (audit of the
424:  	// fix round, gpt G2-E-core-05).
425:  	const std::string backup = mSystemConfFile + ".backup";
426: -	const int mode = recoveredMode >= 0 ? recoveredMode : Utils::AtomicFile::modeOf(mSystemConfFile, 0644);
427: +	const int mode = current.mode & (recoveredMode >= 0 ? recoveredMode : 07777);
428:  	if (Utils::AtomicFile::readText(backup) == text && Utils::AtomicFile::modeOf(backup, mode) == mode)
429:  		return;
430:  	if (!Utils::AtomicFile::writeText(backup, text, mode))
431: @@ -234,7 +245,8 @@ bool SystemConf::loadFromDisk()
432:  			<< ".tmp that an interrupted save left -- loading that and writing it back";
433:  		parseSystemConf(chosen.text);
434:  		reportWriteBack("its .tmp");
435: -		recordLastGood(chosen.text, mode);
436: +		if (wrote != Utils::AtomicFile::RecoveryWrite::LockBusy)
437: +			recordLastGood(chosen.text, mode);
438:  		sRecovered = true;
439:  		return true;
440:  
441: @@ -247,7 +259,8 @@ bool SystemConf::loadFromDisk()
442:  		// copy shares, which the live file is written with (claude
443:  		// G2-E-core-04 b: a record an earlier build made 0644 stayed so beside
444:  		// the 0600 file until the next save).
445: -		recordLastGood(chosen.text, mode);
446: +		if (wrote != Utils::AtomicFile::RecoveryWrite::LockBusy)
447: +			recordLastGood(chosen.text, mode);
448:  		sRecovered = true;
449:  		return true;
450:  
451: @@ -316,7 +329,8 @@ bool SystemConf::saveSystemConf()
452:  
453:  	// What was just written is, by construction, the newest good state, so
454:  	// it becomes the record (D-CLOUD-078: a success becomes the last known
455: -	// good). Outside the lock: the shell never takes it for the record.
456: +	// good). recordLastGood reacquires the lock and revalidates that snapshot;
457: +	// a script may have published a newer state since this save released it.
458:  	// Unless it was merged onto a file cut short: the record then keeps the
459:  	// keys the cut lost (audit of the fixes G-E1-04).
460:  	if (baseWhole)
461: diff --git a/es-core/src/Window.cpp b/es-core/src/Window.cpp
462: index 223659821..78da39809 100644
463: --- a/es-core/src/Window.cpp
464: +++ b/es-core/src/Window.cpp
465: @@ -1143,6 +1143,12 @@ void Window::renderScreenSaver()
466:  		mScreenSaver->renderScreenSaver();
467:  }
468:  
469: +bool Window::hasAsyncNotifications()
470: +{
471: +	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
472: +	return !mAsyncNotificationComponent.empty();
473: +}
474: +
475:  AsyncNotificationComponent* Window::createAsyncNotificationComponent(bool actionLine)
476:  {
477:  	std::unique_lock<std::mutex> lock(mNotificationMessagesLock);
478: diff --git a/es-core/src/Window.h b/es-core/src/Window.h
479: index 8b8f65b2f..1f1fd7e1c 100644
480: --- a/es-core/src/Window.h
481: +++ b/es-core/src/Window.h
482: @@ -97,6 +97,8 @@ public:
483:  	std::shared_ptr<BatteryIndicatorComponent>	getBatteryIndicator() { return mBatteryIndicator; }
484:  
485:  	AsyncNotificationComponent* createAsyncNotificationComponent(bool actionLine = false);
486: +	// Includes queued, lingering and fading cards until the window removes them.
487: +	bool hasAsyncNotifications();
488:  
489:  	bool isCalibratingGun() { return mCalibrationText != nullptr; }
490:  	void setGunCalibrationState(bool isCalibrating);
491: diff --git a/locale/lang/fr/LC_MESSAGES/emulationstation2.po b/locale/lang/fr/LC_MESSAGES/emulationstation2.po
492: index 1d92db348..f6f9b733f 100644
493: --- a/locale/lang/fr/LC_MESSAGES/emulationstation2.po
494: +++ b/locale/lang/fr/LC_MESSAGES/emulationstation2.po
495: @@ -5113,8 +5113,8 @@ msgstr "ACTIVER LA SURCOUCHE MANGOHUD"
496:  msgid "ENABLE TOUCHSCREEN KEYBOARD"
497:  msgstr "ACTIVER LE CLAVIER TACTILE"
498:  
499: -msgid "ENABLE ROCKNIX SCREENSHOT"
500: -msgstr "ACTIVER LA CAPTURE D’ÉCRAN ROCKNIX"
501: +msgid "ENABLE pixelelated SCREENSHOT"
502: +msgstr "ACTIVER LA CAPTURE D’ÉCRAN pixelelated"
503:  
504:  msgid "SCREEN BRIGHTNESS"
505:  msgstr "LUMINOSITÉ DE L’ÉCRAN"
506: @@ -6613,3 +6613,18 @@ msgstr "VOUS N’ÊTES PAS EN LIGNE. CONNECTEZ-VOUS POUR TERMINER LA CONFIGURATI
507:  
508:  msgid "CONNECT TO WI-FI"
509:  msgstr "SE CONNECTER AU WI-FI"
510: +
511: +msgid "MANUAL UPDATES"
512: +msgstr "MISES À JOUR MANUELLES"
513: +
514: +msgid "This version uses manual updates. Open github.com/pixelelated/distribution/releases on a computer, choose the update for your device, and follow the instructions."
515: +msgstr "Cette version utilise des mises à jour manuelles. Sur un ordinateur, ouvrez github.com/pixelelated/distribution/releases, choisissez la mise à jour pour votre appareil, puis suivez les instructions."
516: +
517: +msgid "YOUR CLOUD FOLDER MOVE DIDN'T FINISH.\n\nTRY AGAIN? FILES ALREADY MOVED WILL BE KEPT."
518: +msgstr "LE DÉPLACEMENT DU DOSSIER CLOUD N'A PAS ABOUTI.\n\nRÉESSAYER ? LES FICHIERS DÉJÀ DÉPLACÉS SERONT CONSERVÉS."
519: +
520: +msgid "WHAT MOVED IS IN THE NEW FOLDER. TRY AGAIN TO FINISH."
521: +msgstr "LES FICHIERS DÉPLACÉS SONT DANS LE NOUVEAU DOSSIER. RÉESSAYEZ POUR TERMINER."
522: +
523: +msgid "YOUR CLOUD FOLDER COULDN'T BE READ"
524: +msgstr "IMPOSSIBLE DE LIRE VOTRE DOSSIER CLOUD"
525: diff --git a/resources/Tiny5-OFL.txt b/resources/Tiny5-OFL.txt
526: new file mode 100644
527: index 000000000..df38291f4
528: --- /dev/null
529: +++ b/resources/Tiny5-OFL.txt
530: @@ -0,0 +1,93 @@
531: +Copyright 2026 The Tiny5 Project Authors (https://github.com/Gissio/font_Tiny5)
532: +
533: +This Font Software is licensed under the SIL Open Font License, Version 1.1.
534: +This license is copied below, and is also available with a FAQ at:
535: +https://scripts.sil.org/OFL
536: +
537: +
538: +-----------------------------------------------------------
539: +SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
540: +-----------------------------------------------------------
541: +
542: +PREAMBLE
543: +The goals of the Open Font License (OFL) are to stimulate worldwide
544: +development of collaborative font projects, to support the font creation
545: +efforts of academic and linguistic communities, and to provide a free and
546: +open framework in which fonts may be shared and improved in partnership
547: +with others.
548: +
549: +The OFL allows the licensed fonts to be used, studied, modified and
550: +redistributed freely as long as they are not sold by themselves. The
551: +fonts, including any derivative works, can be bundled, embedded, 
552: +redistributed and/or sold with any software provided that any reserved
553: +names are not used by derivative works. The fonts and derivatives,
554: +however, cannot be released under any other type of license. The
555: +requirement for fonts to remain under this license does not apply
556: +to any document created using the fonts or their derivatives.
557: +
558: +DEFINITIONS
559: +"Font Software" refers to the set of files released by the Copyright
560: +Holder(s) under this license and clearly marked as such. This may
561: +include source files, build scripts and documentation.
562: +
563: +"Reserved Font Name" refers to any names specified as such after the
564: +copyright statement(s).
565: +
566: +"Original Version" refers to the collection of Font Software components as
567: +distributed by the Copyright Holder(s).
568: +
569: +"Modified Version" refers to any derivative made by adding to, deleting,
570: +or substituting -- in part or in whole -- any of the components of the
571: +Original Version, by changing formats or by porting the Font Software to a
572: +new environment.
573: +
574: +"Author" refers to any designer, engineer, programmer, technical
575: +writer or other person who contributed to the Font Software.
576: +
577: +PERMISSION & CONDITIONS
578: +Permission is hereby granted, free of charge, to any person obtaining
579: +a copy of the Font Software, to use, study, copy, merge, embed, modify,
580: +redistribute, and sell modified and unmodified copies of the Font
581: +Software, subject to the following conditions:
582: +
583: +1) Neither the Font Software nor any of its individual components,
584: +in Original or Modified Versions, may be sold by itself.
585: +
586: +2) Original or Modified Versions of the Font Software may be bundled,
587: +redistributed and/or sold with any software, provided that each copy
588: +contains the above copyright notice and this license. These can be
589: +included either as stand-alone text files, human-readable headers or
590: +in the appropriate machine-readable metadata fields within text or
591: +binary files as long as those fields can be easily viewed by the user.
592: +
593: +3) No Modified Version of the Font Software may use the Reserved Font
594: +Name(s) unless explicit written permission is granted by the corresponding
595: +Copyright Holder. This restriction only applies to the primary font name as
596: +presented to the users.
597: +
598: +4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font
599: +Software shall not be used to promote, endorse or advertise any
600: +Modified Version, except to acknowledge the contribution(s) of the
601: +Copyright Holder(s) and the Author(s) or with their explicit written
602: +permission.
603: +
604: +5) The Font Software, modified or unmodified, in part or in whole,
605: +must be distributed entirely under this license, and must not be
606: +distributed under any other license. The requirement for fonts to
607: +remain under this license does not apply to any document created
608: +using the Font Software.
609: +
610: +TERMINATION
611: +This license becomes null and void if any of the above conditions are
612: +not met.
613: +
614: +DISCLAIMER
615: +THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
616: +EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
617: +MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
618: +OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE
619: +COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
620: +INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
621: +DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
622: +FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
623: +OTHER DEALINGS IN THE FONT SOFTWARE.
624: diff --git a/resources/pixelelated-wordmark.svg b/resources/pixelelated-wordmark.svg
625: new file mode 100644
626: index 000000000..213585ef4
627: --- /dev/null
628: +++ b/resources/pixelelated-wordmark.svg
629: @@ -0,0 +1,263 @@
630: +<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 32" width="480" height="256" shape-rendering="crispEdges" role="img" aria-labelledby="title">
631: +<title id="title">pixelelated</title>
632: +<g id="wordmark">
633: +<path fill="#10E6FF" d="M6.9375 14.5625 L6.0625 14.5625 L6.0625 15.3125 L6.9375 15.3125 Z"/>
634: +<path fill="#10A5FF" d="M6.9375 15.3125 L6.0625 15.3125 L6.0625 15.4375 L6.9375 15.4375 Z"/>
635: +<path fill="#10E6FF" d="M5.9375 14.5625 L5.0625 14.5625 L5.0625 15.3125 L5.9375 15.3125 Z"/>
636: +<path fill="#10A5FF" d="M5.9375 15.3125 L5.0625 15.3125 L5.0625 15.4375 L5.9375 15.4375 Z"/>
637: +<path fill="#10E6FF" d="M4.9375 14.5625 L4.0625 14.5625 L4.0625 15.3125 L4.9375 15.3125 Z"/>
638: +<path fill="#10A5FF" d="M4.9375 15.3125 L4.0625 15.3125 L4.0625 15.4375 L4.9375 15.4375 Z"/>
639: +<path fill="#10E6FF" d="M3.9375 14.5625 L3.0625 14.5625 L3.0625 15.3125 L3.9375 15.3125 Z"/>
640: +<path fill="#10A5FF" d="M3.9375 15.3125 L3.0625 15.3125 L3.0625 15.4375 L3.9375 15.4375 Z"/>
641: +<path fill="#10A5FF" d="M7.9375 15.5625 L7.0625 15.5625 L7.0625 16.4375 L7.9375 16.4375 Z"/>
642: +<path fill="#10A5FF" d="M6.9375 15.5625 L6.0625 15.5625 L6.0625 16.4375 L6.9375 16.4375 Z"/>
643: +<path fill="#10A5FF" d="M4.9375 15.5625 L4.0625 15.5625 L4.0625 16.4375 L4.9375 16.4375 Z"/>
644: +<path fill="#10A5FF" d="M3.9375 15.5625 L3.0625 15.5625 L3.0625 16.4375 L3.9375 16.4375 Z"/>
645: +<path fill="#10A5FF" d="M7.9375 16.5625 L7.0625 16.5625 L7.0625 16.6875 L7.9375 16.6875 Z"/>
646: +<path fill="#1963FF" d="M7.9375 16.6875 L7.0625 16.6875 L7.0625 17.4375 L7.9375 17.4375 Z"/>
647: +<path fill="#10A5FF" d="M6.9375 16.5625 L6.0625 16.5625 L6.0625 16.6875 L6.9375 16.6875 Z"/>
648: +<path fill="#1963FF" d="M6.9375 16.6875 L6.0625 16.6875 L6.0625 17.4375 L6.9375 17.4375 Z"/>
649: +<path fill="#10A5FF" d="M4.9375 16.5625 L4.0625 16.5625 L4.0625 16.6875 L4.9375 16.6875 Z"/>
650: +<path fill="#1963FF" d="M4.9375 16.6875 L4.0625 16.6875 L4.0625 17.4375 L4.9375 17.4375 Z"/>
651: +<path fill="#10A5FF" d="M3.9375 16.5625 L3.0625 16.5625 L3.0625 16.6875 L3.9375 16.6875 Z"/>
652: +<path fill="#1963FF" d="M3.9375 16.6875 L3.0625 16.6875 L3.0625 17.4375 L3.9375 17.4375 Z"/>
653: +<path fill="#1963FF" d="M6.9375 17.5625 L6.0625 17.5625 L6.0625 18.0625 L6.9375 18.0625 Z"/>
654: +<path fill="#1921B5" d="M6.9375 18.0625 L6.0625 18.0625 L6.0625 18.4375 L6.9375 18.4375 Z"/>
655: +<path fill="#1963FF" d="M5.9375 17.5625 L5.0625 17.5625 L5.0625 18.0625 L5.9375 18.0625 Z"/>
656: +<path fill="#1921B5" d="M5.9375 18.0625 L5.0625 18.0625 L5.0625 18.4375 L5.9375 18.4375 Z"/>
657: +<path fill="#1963FF" d="M4.9375 17.5625 L4.0625 17.5625 L4.0625 18.0625 L4.9375 18.0625 Z"/>
658: +<path fill="#1921B5" d="M4.9375 18.0625 L4.0625 18.0625 L4.0625 18.4375 L4.9375 18.4375 Z"/>
659: +<path fill="#1963FF" d="M3.9375 17.5625 L3.0625 17.5625 L3.0625 18.0625 L3.9375 18.0625 Z"/>
660: +<path fill="#1921B5" d="M3.9375 18.0625 L3.0625 18.0625 L3.0625 18.4375 L3.9375 18.4375 Z"/>
661: +<path fill="#1921B5" d="M3.9375 18.5625 L3.0625 18.5625 L3.0625 19.4375 L3.9375 19.4375 Z"/>
662: +<path fill="#1921B5" d="M4.9375 18.5625 L4.0625 18.5625 L4.0625 19.4375 L4.9375 19.4375 Z"/>
663: +<path fill="#A5FFFF" d="M9.9375 12.5625 L9.0625 12.5625 L9.0625 13.4375 L9.9375 13.4375 Z"/>
664: +<path fill="#A5FFFF" d="M10.9375 12.5625 L10.0625 12.5625 L10.0625 13.4375 L10.9375 13.4375 Z"/>
665: +<path fill="#10E6FF" d="M9.9375 14.5625 L9.0625 14.5625 L9.0625 15.3125 L9.9375 15.3125 Z"/>
666: +<path fill="#10A5FF" d="M9.9375 15.3125 L9.0625 15.3125 L9.0625 15.4375 L9.9375 15.4375 Z"/>
667: +<path fill="#10E6FF" d="M10.9375 14.5625 L10.0625 14.5625 L10.0625 15.3125 L10.9375 15.3125 Z"/>
668: +<path fill="#10A5FF" d="M10.9375 15.3125 L10.0625 15.3125 L10.0625 15.4375 L10.9375 15.4375 Z"/>
669: +<path fill="#10A5FF" d="M9.9375 15.5625 L9.0625 15.5625 L9.0625 16.4375 L9.9375 16.4375 Z"/>
670: +<path fill="#10A5FF" d="M10.9375 15.5625 L10.0625 15.5625 L10.0625 16.4375 L10.9375 16.4375 Z"/>
671: +<path fill="#10A5FF" d="M9.9375 16.5625 L9.0625 16.5625 L9.0625 16.6875 L9.9375 16.6875 Z"/>
672: +<path fill="#1963FF" d="M9.9375 16.6875 L9.0625 16.6875 L9.0625 17.4375 L9.9375 17.4375 Z"/>
673: +<path fill="#10A5FF" d="M10.9375 16.5625 L10.0625 16.5625 L10.0625 16.6875 L10.9375 16.6875 Z"/>
674: +<path fill="#1963FF" d="M10.9375 16.6875 L10.0625 16.6875 L10.0625 17.4375 L10.9375 17.4375 Z"/>
675: +<path fill="#1963FF" d="M9.9375 17.5625 L9.0625 17.5625 L9.0625 18.0625 L9.9375 18.0625 Z"/>
676: +<path fill="#1921B5" d="M9.9375 18.0625 L9.0625 18.0625 L9.0625 18.4375 L9.9375 18.4375 Z"/>
677: +<path fill="#1963FF" d="M10.9375 17.5625 L10.0625 17.5625 L10.0625 18.0625 L10.9375 18.0625 Z"/>
678: +<path fill="#1921B5" d="M10.9375 18.0625 L10.0625 18.0625 L10.0625 18.4375 L10.9375 18.4375 Z"/>
679: +<path fill="#10E6FF" d="M12.9375 14.5625 L12.0625 14.5625 L12.0625 15.3125 L12.9375 15.3125 Z"/>
680: +<path fill="#10A5FF" d="M12.9375 15.3125 L12.0625 15.3125 L12.0625 15.4375 L12.9375 15.4375 Z"/>
681: +<path fill="#10E6FF" d="M13.9375 14.5625 L13.0625 14.5625 L13.0625 15.3125 L13.9375 15.3125 Z"/>
682: +<path fill="#10A5FF" d="M13.9375 15.3125 L13.0625 15.3125 L13.0625 15.4375 L13.9375 15.4375 Z"/>
683: +<path fill="#10E6FF" d="M15.9375 14.5625 L15.0625 14.5625 L15.0625 15.3125 L15.9375 15.3125 Z"/>
684: +<path fill="#10A5FF" d="M15.9375 15.3125 L15.0625 15.3125 L15.0625 15.4375 L15.9375 15.4375 Z"/>
685: +<path fill="#10E6FF" d="M16.9375 14.5625 L16.0625 14.5625 L16.0625 15.3125 L16.9375 15.3125 Z"/>
686: +<path fill="#10A5FF" d="M16.9375 15.3125 L16.0625 15.3125 L16.0625 15.4375 L16.9375 15.4375 Z"/>
687: +<path fill="#10A5FF" d="M13.9375 15.5625 L13.0625 15.5625 L13.0625 16.4375 L13.9375 16.4375 Z"/>
688: +<path fill="#10A5FF" d="M14.9375 15.5625 L14.0625 15.5625 L14.0625 16.4375 L14.9375 16.4375 Z"/>
689: +<path fill="#10A5FF" d="M15.9375 15.5625 L15.0625 15.5625 L15.0625 16.4375 L15.9375 16.4375 Z"/>
690: +<path fill="#10A5FF" d="M12.9375 16.5625 L12.0625 16.5625 L12.0625 16.6875 L12.9375 16.6875 Z"/>
691: +<path fill="#1963FF" d="M12.9375 16.6875 L12.0625 16.6875 L12.0625 17.4375 L12.9375 17.4375 Z"/>
692: +<path fill="#10A5FF" d="M13.9375 16.5625 L13.0625 16.5625 L13.0625 16.6875 L13.9375 16.6875 Z"/>
693: +<path fill="#1963FF" d="M13.9375 16.6875 L13.0625 16.6875 L13.0625 17.4375 L13.9375 17.4375 Z"/>
694: +<path fill="#10A5FF" d="M15.9375 16.5625 L15.0625 16.5625 L15.0625 16.6875 L15.9375 16.6875 Z"/>
695: +<path fill="#1963FF" d="M15.9375 16.6875 L15.0625 16.6875 L15.0625 17.4375 L15.9375 17.4375 Z"/>
696: +<path fill="#10A5FF" d="M16.9375 16.5625 L16.0625 16.5625 L16.0625 16.6875 L16.9375 16.6875 Z"/>
697: +<path fill="#1963FF" d="M16.9375 16.6875 L16.0625 16.6875 L16.0625 17.4375 L16.9375 17.4375 Z"/>
698: +<path fill="#1963FF" d="M12.9375 17.5625 L12.0625 17.5625 L12.0625 18.0625 L12.9375 18.0625 Z"/>
699: +<path fill="#1921B5" d="M12.9375 18.0625 L12.0625 18.0625 L12.0625 18.4375 L12.9375 18.4375 Z"/>
700: +<path fill="#1963FF" d="M13.9375 17.5625 L13.0625 17.5625 L13.0625 18.0625 L13.9375 18.0625 Z"/>
701: +<path fill="#1921B5" d="M13.9375 18.0625 L13.0625 18.0625 L13.0625 18.4375 L13.9375 18.4375 Z"/>
702: +<path fill="#1963FF" d="M15.9375 17.5625 L15.0625 17.5625 L15.0625 18.0625 L15.9375 18.0625 Z"/>
703: +<path fill="#1921B5" d="M15.9375 18.0625 L15.0625 18.0625 L15.0625 18.4375 L15.9375 18.4375 Z"/>
704: +<path fill="#1963FF" d="M16.9375 17.5625 L16.0625 17.5625 L16.0625 18.0625 L16.9375 18.0625 Z"/>
705: +<path fill="#1921B5" d="M16.9375 18.0625 L16.0625 18.0625 L16.0625 18.4375 L16.9375 18.4375 Z"/>
706: +<path fill="#10E6FF" d="M19.9375 14.5625 L19.0625 14.5625 L19.0625 15.3125 L19.9375 15.3125 Z"/>
707: +<path fill="#10A5FF" d="M19.9375 15.3125 L19.0625 15.3125 L19.0625 15.4375 L19.9375 15.4375 Z"/>
708: +<path fill="#10E6FF" d="M20.9375 14.5625 L20.0625 14.5625 L20.0625 15.3125 L20.9375 15.3125 Z"/>
709: +<path fill="#10A5FF" d="M20.9375 15.3125 L20.0625 15.3125 L20.0625 15.4375 L20.9375 15.4375 Z"/>
710: +<path fill="#10E6FF" d="M21.9375 14.5625 L21.0625 14.5625 L21.0625 15.3125 L21.9375 15.3125 Z"/>
711: +<path fill="#10A5FF" d="M21.9375 15.3125 L21.0625 15.3125 L21.0625 15.4375 L21.9375 15.4375 Z"/>
712: +<path fill="#10A5FF" d="M18.9375 15.5625 L18.0625 15.5625 L18.0625 16.4375 L18.9375 16.4375 Z"/>
713: +<path fill="#10A5FF" d="M19.9375 15.5625 L19.0625 15.5625 L19.0625 16.4375 L19.9375 16.4375 Z"/>
714: +<path fill="#10A5FF" d="M20.9375 15.5625 L20.0625 15.5625 L20.0625 16.4375 L20.9375 16.4375 Z"/>
715: +<path fill="#10A5FF" d="M21.9375 15.5625 L21.0625 15.5625 L21.0625 16.4375 L21.9375 16.4375 Z"/>
716: +<path fill="#10A5FF" d="M22.9375 15.5625 L22.0625 15.5625 L22.0625 16.4375 L22.9375 16.4375 Z"/>
717: +<path fill="#10A5FF" d="M18.9375 16.5625 L18.0625 16.5625 L18.0625 16.6875 L18.9375 16.6875 Z"/>
718: +<path fill="#1963FF" d="M18.9375 16.6875 L18.0625 16.6875 L18.0625 17.4375 L18.9375 17.4375 Z"/>
719: +<path fill="#10A5FF" d="M19.9375 16.5625 L19.0625 16.5625 L19.0625 16.6875 L19.9375 16.6875 Z"/>
720: +<path fill="#1963FF" d="M19.9375 16.6875 L19.0625 16.6875 L19.0625 17.4375 L19.9375 17.4375 Z"/>
721: +<path fill="#1963FF" d="M19.9375 17.5625 L19.0625 17.5625 L19.0625 18.0625 L19.9375 18.0625 Z"/>
722: +<path fill="#1921B5" d="M19.9375 18.0625 L19.0625 18.0625 L19.0625 18.4375 L19.9375 18.4375 Z"/>
723: +<path fill="#1963FF" d="M20.9375 17.5625 L20.0625 17.5625 L20.0625 18.0625 L20.9375 18.0625 Z"/>
724: +<path fill="#1921B5" d="M20.9375 18.0625 L20.0625 18.0625 L20.0625 18.4375 L20.9375 18.4375 Z"/>
725: +<path fill="#1963FF" d="M21.9375 17.5625 L21.0625 17.5625 L21.0625 18.0625 L21.9375 18.0625 Z"/>
726: +<path fill="#1921B5" d="M21.9375 18.0625 L21.0625 18.0625 L21.0625 18.4375 L21.9375 18.4375 Z"/>
727: +<path fill="#1963FF" d="M22.9375 17.5625 L22.0625 17.5625 L22.0625 18.0625 L22.9375 18.0625 Z"/>
728: +<path fill="#1921B5" d="M22.9375 18.0625 L22.0625 18.0625 L22.0625 18.4375 L22.9375 18.4375 Z"/>
729: +<path fill="#A5FFFF" d="M24.9375 13.5625 L24.0625 13.5625 L24.0625 13.9375 L24.9375 13.9375 Z"/>
730: +<path fill="#10E6FF" d="M24.9375 13.9375 L24.0625 13.9375 L24.0625 14.4375 L24.9375 14.4375 Z"/>
731: +<path fill="#A5FFFF" d="M25.9375 13.5625 L25.0625 13.5625 L25.0625 13.9375 L25.9375 13.9375 Z"/>
732: +<path fill="#10E6FF" d="M25.9375 13.9375 L25.0625 13.9375 L25.0625 14.4375 L25.9375 14.4375 Z"/>
733: +<path fill="#10E6FF" d="M24.9375 14.5625 L24.0625 14.5625 L24.0625 15.3125 L24.9375 15.3125 Z"/>
734: +<path fill="#10A5FF" d="M24.9375 15.3125 L24.0625 15.3125 L24.0625 15.4375 L24.9375 15.4375 Z"/>
735: +<path fill="#10E6FF" d="M25.9375 14.5625 L25.0625 14.5625 L25.0625 15.3125 L25.9375 15.3125 Z"/>
736: +<path fill="#10A5FF" d="M25.9375 15.3125 L25.0625 15.3125 L25.0625 15.4375 L25.9375 15.4375 Z"/>
737: +<path fill="#10A5FF" d="M24.9375 15.5625 L24.0625 15.5625 L24.0625 16.4375 L24.9375 16.4375 Z"/>
738: +<path fill="#10A5FF" d="M25.9375 15.5625 L25.0625 15.5625 L25.0625 16.4375 L25.9375 16.4375 Z"/>
739: +<path fill="#10A5FF" d="M24.9375 16.5625 L24.0625 16.5625 L24.0625 16.6875 L24.9375 16.6875 Z"/>
740: +<path fill="#1963FF" d="M24.9375 16.6875 L24.0625 16.6875 L24.0625 17.4375 L24.9375 17.4375 Z"/>
741: +<path fill="#10A5FF" d="M25.9375 16.5625 L25.0625 16.5625 L25.0625 16.6875 L25.9375 16.6875 Z"/>
742: +<path fill="#1963FF" d="M25.9375 16.6875 L25.0625 16.6875 L25.0625 17.4375 L25.9375 17.4375 Z"/>
743: +<path fill="#1963FF" d="M24.9375 17.5625 L24.0625 17.5625 L24.0625 18.0625 L24.9375 18.0625 Z"/>
744: +<path fill="#1921B5" d="M24.9375 18.0625 L24.0625 18.0625 L24.0625 18.4375 L24.9375 18.4375 Z"/>
745: +<path fill="#1963FF" d="M25.9375 17.5625 L25.0625 17.5625 L25.0625 18.0625 L25.9375 18.0625 Z"/>
746: +<path fill="#1921B5" d="M25.9375 18.0625 L25.0625 18.0625 L25.0625 18.4375 L25.9375 18.4375 Z"/>
747: +<path fill="#10E6FF" d="M28.9375 14.5625 L28.0625 14.5625 L28.0625 15.3125 L28.9375 15.3125 Z"/>
748: +<path fill="#10A5FF" d="M28.9375 15.3125 L28.0625 15.3125 L28.0625 15.4375 L28.9375 15.4375 Z"/>
749: +<path fill="#10E6FF" d="M29.9375 14.5625 L29.0625 14.5625 L29.0625 15.3125 L29.9375 15.3125 Z"/>
750: +<path fill="#10A5FF" d="M29.9375 15.3125 L29.0625 15.3125 L29.0625 15.4375 L29.9375 15.4375 Z"/>
751: +<path fill="#10E6FF" d="M30.9375 14.5625 L30.0625 14.5625 L30.0625 15.3125 L30.9375 15.3125 Z"/>
752: +<path fill="#10A5FF" d="M30.9375 15.3125 L30.0625 15.3125 L30.0625 15.4375 L30.9375 15.4375 Z"/>
753: +<path fill="#10A5FF" d="M27.9375 15.5625 L27.0625 15.5625 L27.0625 16.4375 L27.9375 16.4375 Z"/>
754: +<path fill="#10A5FF" d="M28.9375 15.5625 L28.0625 15.5625 L28.0625 16.4375 L28.9375 16.4375 Z"/>
755: +<path fill="#10A5FF" d="M29.9375 15.5625 L29.0625 15.5625 L29.0625 16.4375 L29.9375 16.4375 Z"/>
756: +<path fill="#10A5FF" d="M30.9375 15.5625 L30.0625 15.5625 L30.0625 16.4375 L30.9375 16.4375 Z"/>
757: +<path fill="#10A5FF" d="M31.9375 15.5625 L31.0625 15.5625 L31.0625 16.4375 L31.9375 16.4375 Z"/>
758: +<path fill="#10A5FF" d="M27.9375 16.5625 L27.0625 16.5625 L27.0625 16.6875 L27.9375 16.6875 Z"/>
759: +<path fill="#1963FF" d="M27.9375 16.6875 L27.0625 16.6875 L27.0625 17.4375 L27.9375 17.4375 Z"/>
760: +<path fill="#10A5FF" d="M28.9375 16.5625 L28.0625 16.5625 L28.0625 16.6875 L28.9375 16.6875 Z"/>
761: +<path fill="#1963FF" d="M28.9375 16.6875 L28.0625 16.6875 L28.0625 17.4375 L28.9375 17.4375 Z"/>
762: +<path fill="#1963FF" d="M28.9375 17.5625 L28.0625 17.5625 L28.0625 18.0625 L28.9375 18.0625 Z"/>
763: +<path fill="#1921B5" d="M28.9375 18.0625 L28.0625 18.0625 L28.0625 18.4375 L28.9375 18.4375 Z"/>
764: +<path fill="#1963FF" d="M29.9375 17.5625 L29.0625 17.5625 L29.0625 18.0625 L29.9375 18.0625 Z"/>
765: +<path fill="#1921B5" d="M29.9375 18.0625 L29.0625 18.0625 L29.0625 18.4375 L29.9375 18.4375 Z"/>
766: +<path fill="#1963FF" d="M30.9375 17.5625 L30.0625 17.5625 L30.0625 18.0625 L30.9375 18.0625 Z"/>
767: +<path fill="#1921B5" d="M30.9375 18.0625 L30.0625 18.0625 L30.0625 18.4375 L30.9375 18.4375 Z"/>
768: +<path fill="#1963FF" d="M31.9375 17.5625 L31.0625 17.5625 L31.0625 18.0625 L31.9375 18.0625 Z"/>
769: +<path fill="#1921B5" d="M31.9375 18.0625 L31.0625 18.0625 L31.0625 18.4375 L31.9375 18.4375 Z"/>
770: +<path fill="#A5FFFF" d="M33.9375 13.5625 L33.0625 13.5625 L33.0625 13.9375 L33.9375 13.9375 Z"/>
771: +<path fill="#10E6FF" d="M33.9375 13.9375 L33.0625 13.9375 L33.0625 14.4375 L33.9375 14.4375 Z"/>
772: +<path fill="#A5FFFF" d="M34.9375 13.5625 L34.0625 13.5625 L34.0625 13.9375 L34.9375 13.9375 Z"/>
773: +<path fill="#10E6FF" d="M34.9375 13.9375 L34.0625 13.9375 L34.0625 14.4375 L34.9375 14.4375 Z"/>
774: +<path fill="#10E6FF" d="M33.9375 14.5625 L33.0625 14.5625 L33.0625 15.3125 L33.9375 15.3125 Z"/>
775: +<path fill="#10A5FF" d="M33.9375 15.3125 L33.0625 15.3125 L33.0625 15.4375 L33.9375 15.4375 Z"/>
776: +<path fill="#10E6FF" d="M34.9375 14.5625 L34.0625 14.5625 L34.0625 15.3125 L34.9375 15.3125 Z"/>
777: +<path fill="#10A5FF" d="M34.9375 15.3125 L34.0625 15.3125 L34.0625 15.4375 L34.9375 15.4375 Z"/>
778: +<path fill="#10A5FF" d="M33.9375 15.5625 L33.0625 15.5625 L33.0625 16.4375 L33.9375 16.4375 Z"/>
779: +<path fill="#10A5FF" d="M34.9375 15.5625 L34.0625 15.5625 L34.0625 16.4375 L34.9375 16.4375 Z"/>
780: +<path fill="#10A5FF" d="M33.9375 16.5625 L33.0625 16.5625 L33.0625 16.6875 L33.9375 16.6875 Z"/>
781: +<path fill="#1963FF" d="M33.9375 16.6875 L33.0625 16.6875 L33.0625 17.4375 L33.9375 17.4375 Z"/>
782: +<path fill="#10A5FF" d="M34.9375 16.5625 L34.0625 16.5625 L34.0625 16.6875 L34.9375 16.6875 Z"/>
783: +<path fill="#1963FF" d="M34.9375 16.6875 L34.0625 16.6875 L34.0625 17.4375 L34.9375 17.4375 Z"/>
784: +<path fill="#1963FF" d="M33.9375 17.5625 L33.0625 17.5625 L33.0625 18.0625 L33.9375 18.0625 Z"/>
785: +<path fill="#1921B5" d="M33.9375 18.0625 L33.0625 18.0625 L33.0625 18.4375 L33.9375 18.4375 Z"/>
786: +<path fill="#1963FF" d="M34.9375 17.5625 L34.0625 17.5625 L34.0625 18.0625 L34.9375 18.0625 Z"/>
787: +<path fill="#1921B5" d="M34.9375 18.0625 L34.0625 18.0625 L34.0625 18.4375 L34.9375 18.4375 Z"/>
788: +<path fill="#10E6FF" d="M37.9375 14.5625 L37.0625 14.5625 L37.0625 15.3125 L37.9375 15.3125 Z"/>
789: +<path fill="#10A5FF" d="M37.9375 15.3125 L37.0625 15.3125 L37.0625 15.4375 L37.9375 15.4375 Z"/>
790: +<path fill="#10E6FF" d="M38.9375 14.5625 L38.0625 14.5625 L38.0625 15.3125 L38.9375 15.3125 Z"/>
791: +<path fill="#10A5FF" d="M38.9375 15.3125 L38.0625 15.3125 L38.0625 15.4375 L38.9375 15.4375 Z"/>
792: +<path fill="#10E6FF" d="M39.9375 14.5625 L39.0625 14.5625 L39.0625 15.3125 L39.9375 15.3125 Z"/>
793: +<path fill="#10A5FF" d="M39.9375 15.3125 L39.0625 15.3125 L39.0625 15.4375 L39.9375 15.4375 Z"/>
794: +<path fill="#10E6FF" d="M40.9375 14.5625 L40.0625 14.5625 L40.0625 15.3125 L40.9375 15.3125 Z"/>
795: +<path fill="#10A5FF" d="M40.9375 15.3125 L40.0625 15.3125 L40.0625 15.4375 L40.9375 15.4375 Z"/>
796: +<path fill="#10A5FF" d="M36.9375 15.5625 L36.0625 15.5625 L36.0625 16.4375 L36.9375 16.4375 Z"/>
797: +<path fill="#10A5FF" d="M37.9375 15.5625 L37.0625 15.5625 L37.0625 16.4375 L37.9375 16.4375 Z"/>
798: +<path fill="#10A5FF" d="M39.9375 15.5625 L39.0625 15.5625 L39.0625 16.4375 L39.9375 16.4375 Z"/>
799: +<path fill="#10A5FF" d="M40.9375 15.5625 L40.0625 15.5625 L40.0625 16.4375 L40.9375 16.4375 Z"/>
800: +<path fill="#10A5FF" d="M36.9375 16.5625 L36.0625 16.5625 L36.0625 16.6875 L36.9375 16.6875 Z"/>
801: +<path fill="#1963FF" d="M36.9375 16.6875 L36.0625 16.6875 L36.0625 17.4375 L36.9375 17.4375 Z"/>
802: +<path fill="#10A5FF" d="M37.9375 16.5625 L37.0625 16.5625 L37.0625 16.6875 L37.9375 16.6875 Z"/>
803: +<path fill="#1963FF" d="M37.9375 16.6875 L37.0625 16.6875 L37.0625 17.4375 L37.9375 17.4375 Z"/>
804: +<path fill="#10A5FF" d="M39.9375 16.5625 L39.0625 16.5625 L39.0625 16.6875 L39.9375 16.6875 Z"/>
805: +<path fill="#1963FF" d="M39.9375 16.6875 L39.0625 16.6875 L39.0625 17.4375 L39.9375 17.4375 Z"/>
806: +<path fill="#10A5FF" d="M40.9375 16.5625 L40.0625 16.5625 L40.0625 16.6875 L40.9375 16.6875 Z"/>
807: +<path fill="#1963FF" d="M40.9375 16.6875 L40.0625 16.6875 L40.0625 17.4375 L40.9375 17.4375 Z"/>
808: +<path fill="#1963FF" d="M37.9375 17.5625 L37.0625 17.5625 L37.0625 18.0625 L37.9375 18.0625 Z"/>
809: +<path fill="#1921B5" d="M37.9375 18.0625 L37.0625 18.0625 L37.0625 18.4375 L37.9375 18.4375 Z"/>
810: +<path fill="#1963FF" d="M38.9375 17.5625 L38.0625 17.5625 L38.0625 18.0625 L38.9375 18.0625 Z"/>
811: +<path fill="#1921B5" d="M38.9375 18.0625 L38.0625 18.0625 L38.0625 18.4375 L38.9375 18.4375 Z"/>
812: +<path fill="#1963FF" d="M39.9375 17.5625 L39.0625 17.5625 L39.0625 18.0625 L39.9375 18.0625 Z"/>
813: +<path fill="#1921B5" d="M39.9375 18.0625 L39.0625 18.0625 L39.0625 18.4375 L39.9375 18.4375 Z"/>
814: +<path fill="#1963FF" d="M40.9375 17.5625 L40.0625 17.5625 L40.0625 18.0625 L40.9375 18.0625 Z"/>
815: +<path fill="#1921B5" d="M40.9375 18.0625 L40.0625 18.0625 L40.0625 18.4375 L40.9375 18.4375 Z"/>
816: +<path fill="#A5FFFF" d="M42.9375 13.5625 L42.0625 13.5625 L42.0625 13.9375 L42.9375 13.9375 Z"/>
817: +<path fill="#10E6FF" d="M42.9375 13.9375 L42.0625 13.9375 L42.0625 14.4375 L42.9375 14.4375 Z"/>
818: +<path fill="#A5FFFF" d="M43.9375 13.5625 L43.0625 13.5625 L43.0625 13.9375 L43.9375 13.9375 Z"/>
819: +<path fill="#10E6FF" d="M43.9375 13.9375 L43.0625 13.9375 L43.0625 14.4375 L43.9375 14.4375 Z"/>
820: +<path fill="#10E6FF" d="M42.9375 14.5625 L42.0625 14.5625 L42.0625 15.3125 L42.9375 15.3125 Z"/>
821: +<path fill="#10A5FF" d="M42.9375 15.3125 L42.0625 15.3125 L42.0625 15.4375 L42.9375 15.4375 Z"/>
822: +<path fill="#10E6FF" d="M43.9375 14.5625 L43.0625 14.5625 L43.0625 15.3125 L43.9375 15.3125 Z"/>
823: +<path fill="#10A5FF" d="M43.9375 15.3125 L43.0625 15.3125 L43.0625 15.4375 L43.9375 15.4375 Z"/>
824: +<path fill="#10E6FF" d="M44.9375 14.5625 L44.0625 14.5625 L44.0625 15.3125 L44.9375 15.3125 Z"/>
825: +<path fill="#10A5FF" d="M44.9375 15.3125 L44.0625 15.3125 L44.0625 15.4375 L44.9375 15.4375 Z"/>
826: +<path fill="#10A5FF" d="M42.9375 15.5625 L42.0625 15.5625 L42.0625 16.4375 L42.9375 16.4375 Z"/>
827: +<path fill="#10A5FF" d="M43.9375 15.5625 L43.0625 15.5625 L43.0625 16.4375 L43.9375 16.4375 Z"/>
828: +<path fill="#10A5FF" d="M42.9375 16.5625 L42.0625 16.5625 L42.0625 16.6875 L42.9375 16.6875 Z"/>
829: +<path fill="#1963FF" d="M42.9375 16.6875 L42.0625 16.6875 L42.0625 17.4375 L42.9375 17.4375 Z"/>
830: +<path fill="#10A5FF" d="M43.9375 16.5625 L43.0625 16.5625 L43.0625 16.6875 L43.9375 16.6875 Z"/>
831: +<path fill="#1963FF" d="M43.9375 16.6875 L43.0625 16.6875 L43.0625 17.4375 L43.9375 17.4375 Z"/>
832: +<path fill="#1963FF" d="M43.9375 17.5625 L43.0625 17.5625 L43.0625 18.0625 L43.9375 18.0625 Z"/>
833: +<path fill="#1921B5" d="M43.9375 18.0625 L43.0625 18.0625 L43.0625 18.4375 L43.9375 18.4375 Z"/>
834: +<path fill="#1963FF" d="M44.9375 17.5625 L44.0625 17.5625 L44.0625 18.0625 L44.9375 18.0625 Z"/>
835: +<path fill="#1921B5" d="M44.9375 18.0625 L44.0625 18.0625 L44.0625 18.4375 L44.9375 18.4375 Z"/>
836: +<path fill="#10E6FF" d="M47.9375 14.5625 L47.0625 14.5625 L47.0625 15.3125 L47.9375 15.3125 Z"/>
837: +<path fill="#10A5FF" d="M47.9375 15.3125 L47.0625 15.3125 L47.0625 15.4375 L47.9375 15.4375 Z"/>
838: +<path fill="#10E6FF" d="M48.9375 14.5625 L48.0625 14.5625 L48.0625 15.3125 L48.9375 15.3125 Z"/>
839: +<path fill="#10A5FF" d="M48.9375 15.3125 L48.0625 15.3125 L48.0625 15.4375 L48.9375 15.4375 Z"/>
840: +<path fill="#10E6FF" d="M49.9375 14.5625 L49.0625 14.5625 L49.0625 15.3125 L49.9375 15.3125 Z"/>
841: +<path fill="#10A5FF" d="M49.9375 15.3125 L49.0625 15.3125 L49.0625 15.4375 L49.9375 15.4375 Z"/>
842: +<path fill="#10A5FF" d="M46.9375 15.5625 L46.0625 15.5625 L46.0625 16.4375 L46.9375 16.4375 Z"/>
843: +<path fill="#10A5FF" d="M47.9375 15.5625 L47.0625 15.5625 L47.0625 16.4375 L47.9375 16.4375 Z"/>
844: +<path fill="#10A5FF" d="M48.9375 15.5625 L48.0625 15.5625 L48.0625 16.4375 L48.9375 16.4375 Z"/>
845: +<path fill="#10A5FF" d="M49.9375 15.5625 L49.0625 15.5625 L49.0625 16.4375 L49.9375 16.4375 Z"/>
846: +<path fill="#10A5FF" d="M50.9375 15.5625 L50.0625 15.5625 L50.0625 16.4375 L50.9375 16.4375 Z"/>
847: +<path fill="#10A5FF" d="M46.9375 16.5625 L46.0625 16.5625 L46.0625 16.6875 L46.9375 16.6875 Z"/>
848: +<path fill="#1963FF" d="M46.9375 16.6875 L46.0625 16.6875 L46.0625 17.4375 L46.9375 17.4375 Z"/>
849: +<path fill="#10A5FF" d="M47.9375 16.5625 L47.0625 16.5625 L47.0625 16.6875 L47.9375 16.6875 Z"/>
850: +<path fill="#1963FF" d="M47.9375 16.6875 L47.0625 16.6875 L47.0625 17.4375 L47.9375 17.4375 Z"/>
851: +<path fill="#1963FF" d="M47.9375 17.5625 L47.0625 17.5625 L47.0625 18.0625 L47.9375 18.0625 Z"/>
852: +<path fill="#1921B5" d="M47.9375 18.0625 L47.0625 18.0625 L47.0625 18.4375 L47.9375 18.4375 Z"/>
853: +<path fill="#1963FF" d="M48.9375 17.5625 L48.0625 17.5625 L48.0625 18.0625 L48.9375 18.0625 Z"/>
854: +<path fill="#1921B5" d="M48.9375 18.0625 L48.0625 18.0625 L48.0625 18.4375 L48.9375 18.4375 Z"/>
855: +<path fill="#1963FF" d="M49.9375 17.5625 L49.0625 17.5625 L49.0625 18.0625 L49.9375 18.0625 Z"/>
856: +<path fill="#1921B5" d="M49.9375 18.0625 L49.0625 18.0625 L49.0625 18.4375 L49.9375 18.4375 Z"/>
857: +<path fill="#1963FF" d="M50.9375 17.5625 L50.0625 17.5625 L50.0625 18.0625 L50.9375 18.0625 Z"/>
858: +<path fill="#1921B5" d="M50.9375 18.0625 L50.0625 18.0625 L50.0625 18.4375 L50.9375 18.4375 Z"/>
859: +<path fill="#A5FFFF" d="M56.9375 13.5625 L56.0625 13.5625 L56.0625 13.9375 L56.9375 13.9375 Z"/>
860: +<path fill="#10E6FF" d="M56.9375 13.9375 L56.0625 13.9375 L56.0625 14.4375 L56.9375 14.4375 Z"/>
861: +<path fill="#A5FFFF" d="M55.9375 13.5625 L55.0625 13.5625 L55.0625 13.9375 L55.9375 13.9375 Z"/>
862: +<path fill="#10E6FF" d="M55.9375 13.9375 L55.0625 13.9375 L55.0625 14.4375 L55.9375 14.4375 Z"/>
863: +<path fill="#10E6FF" d="M56.9375 14.5625 L56.0625 14.5625 L56.0625 15.3125 L56.9375 15.3125 Z"/>
864: +<path fill="#10A5FF" d="M56.9375 15.3125 L56.0625 15.3125 L56.0625 15.4375 L56.9375 15.4375 Z"/>
865: +<path fill="#10E6FF" d="M55.9375 14.5625 L55.0625 14.5625 L55.0625 15.3125 L55.9375 15.3125 Z"/>
866: +<path fill="#10A5FF" d="M55.9375 15.3125 L55.0625 15.3125 L55.0625 15.4375 L55.9375 15.4375 Z"/>
867: +<path fill="#10E6FF" d="M54.9375 14.5625 L54.0625 14.5625 L54.0625 15.3125 L54.9375 15.3125 Z"/>
868: +<path fill="#10A5FF" d="M54.9375 15.3125 L54.0625 15.3125 L54.0625 15.4375 L54.9375 15.4375 Z"/>
869: +<path fill="#10E6FF" d="M53.9375 14.5625 L53.0625 14.5625 L53.0625 15.3125 L53.9375 15.3125 Z"/>
870: +<path fill="#10A5FF" d="M53.9375 15.3125 L53.0625 15.3125 L53.0625 15.4375 L53.9375 15.4375 Z"/>
871: +<path fill="#10A5FF" d="M53.9375 15.5625 L53.0625 15.5625 L53.0625 16.4375 L53.9375 16.4375 Z"/>
872: +<path fill="#10A5FF" d="M56.9375 15.5625 L56.0625 15.5625 L56.0625 16.4375 L56.9375 16.4375 Z"/>
873: +<path fill="#10A5FF" d="M55.9375 15.5625 L55.0625 15.5625 L55.0625 16.4375 L55.9375 16.4375 Z"/>
874: +<path fill="#10A5FF" d="M52.9375 15.5625 L52.0625 15.5625 L52.0625 16.4375 L52.9375 16.4375 Z"/>
875: +<path fill="#10A5FF" d="M56.9375 16.5625 L56.0625 16.5625 L56.0625 16.6875 L56.9375 16.6875 Z"/>
876: +<path fill="#1963FF" d="M56.9375 16.6875 L56.0625 16.6875 L56.0625 17.4375 L56.9375 17.4375 Z"/>
877: +<path fill="#10A5FF" d="M55.9375 16.5625 L55.0625 16.5625 L55.0625 16.6875 L55.9375 16.6875 Z"/>
878: +<path fill="#1963FF" d="M55.9375 16.6875 L55.0625 16.6875 L55.0625 17.4375 L55.9375 17.4375 Z"/>
879: +<path fill="#10A5FF" d="M53.9375 16.5625 L53.0625 16.5625 L53.0625 16.6875 L53.9375 16.6875 Z"/>
880: +<path fill="#1963FF" d="M53.9375 16.6875 L53.0625 16.6875 L53.0625 17.4375 L53.9375 17.4375 Z"/>
881: +<path fill="#10A5FF" d="M52.9375 16.5625 L52.0625 16.5625 L52.0625 16.6875 L52.9375 16.6875 Z"/>
882: +<path fill="#1963FF" d="M52.9375 16.6875 L52.0625 16.6875 L52.0625 17.4375 L52.9375 17.4375 Z"/>
883: +<path fill="#1963FF" d="M53.9375 17.5625 L53.0625 17.5625 L53.0625 18.0625 L53.9375 18.0625 Z"/>
884: +<path fill="#1921B5" d="M53.9375 18.0625 L53.0625 18.0625 L53.0625 18.4375 L53.9375 18.4375 Z"/>
885: +<path fill="#1963FF" d="M56.9375 17.5625 L56.0625 17.5625 L56.0625 18.0625 L56.9375 18.0625 Z"/>
886: +<path fill="#1921B5" d="M56.9375 18.0625 L56.0625 18.0625 L56.0625 18.4375 L56.9375 18.4375 Z"/>
887: +<path fill="#1963FF" d="M55.9375 17.5625 L55.0625 17.5625 L55.0625 18.0625 L55.9375 18.0625 Z"/>
888: +<path fill="#1921B5" d="M55.9375 18.0625 L55.0625 18.0625 L55.0625 18.4375 L55.9375 18.4375 Z"/>
889: +<path fill="#1963FF" d="M54.9375 17.5625 L54.0625 17.5625 L54.0625 18.0625 L54.9375 18.0625 Z"/>
890: +<path fill="#1921B5" d="M54.9375 18.0625 L54.0625 18.0625 L54.0625 18.4375 L54.9375 18.4375 Z"/>
891: +</g>
892: +</svg>
```


## SOURCE projects/ROCKNIX/packages/network/rclone/sources/cloud_setup

```text
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_setup - configure the rclone cloud remote.
6: #
7: # Walks the player through rclone's own interactive configuration over SSH:
8: # it is the only flow that handles every provider completely (OAuth sign-in,
9: # folder choices, provider-specific questions). This screen supplies the
10: # connection details in big text, waits, then verifies the remote actually
11: # works before declaring success.
12: #
13: # The native UI wizard drives the same flow through three flags:
14: #   --info       key=value connection facts (IP, SSH command, override
15: #                state, password, sshd state, OAuth-port state,
16: #                configured remotes)
17: #   --free-auth-port  clear a stale sign-in webserver holding rclone's
18: #                OAuth port 53682
19: #   --set-content-remote <path>  change the content root alone (CONTENT_REMOTE;
20: #                the chooser's, fork #352); nothing moves
21: #   --set-saves-remote <path>  change the cloud folder (SAVES_REMOTE) the sync
22: #                (--set-syncpath is accepted as the older spelling)
23: #                tools use, keeping SETTINGS_REMOTE alongside it; refuses a
24: #                path the remote cannot use
25: #   --accept-saves-root  the saves folder is on a different card than the last
26: #                sync and that is intended (cloud_saves_root)
27: #   --check-syncpath [path]  validate a cloud folder against the remote's
28: #                shape without changing anything (default: the current one)
29: #   --content-location  report where this device's ROMs/BIOS actually are in
30: #                the cloud (key=value; STATE=ok|stranded-at-root|empty;
31: #                unreadable, exit 1, when its value is not in a form the
32: #                sync reads)
33: #   --use-content-root  point content back at the remote root, moving nothing
34: #   --connected  exit 0 when an inbound SSH session is established, so the
35: #                connect step can be verified rather than taken on faith
36: #   --check [remote]  verify a remote (default: first); exit 0 working,
37: #                1 missing, 2 configured but unreachable
38: 
39: . /etc/profile
40: 
41: SCRIPT_NAME=$(basename "$0")
42: LOG_FILE="/var/log/cloud_sync.log"
43: SYNC_CONF="/storage/.config/cloud_sync.conf"
44: 
45: log_message() {
46:     local message="$1"
47:     local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
48:     echo "[${timestamp}] [INFO] [${SCRIPT_NAME}] ${message}" >> ${LOG_FILE}
49: }
50: 
51: # The config is shell: every cloud script sources it. So a value is written
52: # as text between double quotes, never through a sed replacement -- where &
53: # is the matched line and | ends the expression, so "/R&D/Saves" became
54: # garbage and "/a|b" failed the write while OK was printed (audit #307
55: # PL-051) -- and a value that would mean something to a shell between double
56: # quotes (" $ ` \) is refused where it is typed (syncpath_problem).
57: #
58: # conf_set KEY VALUE [KEY VALUE ...] writes every pair in one pass, each
59: # KEY= line replaced (every one, as the sed was) or appended, to a file
60: # beside the config that is renamed over it: all the keys or none, and the
61: # previous config intact when the write fails. The values reach awk through
62: # the environment, so nothing in them is interpreted. Returns non-zero when
63: # the config could not be written.
64: conf_set() {
65:     local tmp="${SYNC_CONF}.tmp.$$" src="${SYNC_CONF}" n=0 i
66:     local -a pairs=() want=()
67:     # Something at the config's path that is not a file is not a config this
68:     # can write: read as "absent", `mv -f` then put the new file INSIDE a
69:     # directory there and succeeded (audit of stream C, G-C-04).
70:     if [ -e "${SYNC_CONF}" ] && [ ! -f "${SYNC_CONF}" ]; then
71:         return 1
72:     fi
73:     [ -f "${src}" ] || src=/dev/null
74:     while [ $# -ge 2 ]; do
75:         n=$((n + 1)); pairs+=("CONF_K${n}=$1" "CONF_V${n}=$2")
76:         want+=("$1=\"$2\""); shift 2
77:     done
78:     # Braced, and silenced as a whole: a redirection that fails opening the
79:     # temp file happens before a `2>/dev/null` written after it, and the
80:     # shell printed its own diagnostic -- a line number and the temp file's
81:     # path -- ahead of the caller's sentence (G-C-07).
82:     if { env "${pairs[@]}" CONF_N="${n}" awk '
83:         BEGIN {
84:             n = ENVIRON["CONF_N"] + 0
85:             for (i = 1; i <= n; i++) {
86:                 k[i] = ENVIRON["CONF_K" i]
87:                 line[i] = k[i] "=\"" ENVIRON["CONF_V" i] "\""
88:             }
89:         }
90:         {
91:             for (i = 1; i <= n; i++)
92:                 if (index($0, k[i] "=") == 1) { print line[i]; seen[i] = 1; next }
93:             print
94:         }
95:         END { for (i = 1; i <= n; i++) if (!seen[i]) print line[i] }
96:     ' "${src}" > "${tmp}" && mv -f "${tmp}" "${SYNC_CONF}"; } 2>/dev/null; then
97:         # Written is what the file says, not what mv returned: a regular
98:         # file at the path, holding every line asked for.
99:         [ -f "${SYNC_CONF}" ] || return 1
100:         for i in "${want[@]}"; do
101:             grep -qFx -- "${i}" "${SYNC_CONF}" 2>/dev/null || return 1
102:         done
103:         return 0
104:     fi
105:     rm -f "${tmp}" 2>/dev/null
106:     return 1
107: }
108: 
109: # One value from the config, read as text -- never by sourcing or eval, since
110: # a value an earlier build wrote with $( ) in it would run (PL-051) -- and as
111: # the scripts that run with it read it, so this and they never disagree
112: # about a player's folder:
113: #   - Of two assignments of a key, the FIRST: every saves run the interface
114: #     starts is --yes, which runs cloud_sync_cleanup_duplicates.sh, which
115: #     keeps the first and is what the file becomes; the content scripts'
116: #     conf_get reads the first too. This read the last, as `source` alone
117: #     would, so with a key written twice the hub's line and
118: #     --content-location named a folder the scripts stopped using at their
119: #     next run (the audit of the fix round, PL-021; the first cut's G-C-03
120: #     gpt and G-C-06 claude had moved it from first to last).
121: #   - The value double quoted, single quoted or a bare word, then nothing,
122: #     or blanks and a # comment: the forms conf_valid lets a file through
123: #     with. Anything else is exit 2 and nothing printed -- /Mine/'My Saves',
124: #     text after a closing quote, a double-quoted value with $, ` or \ in it
125: #     (what a shell would expand there) -- as the content scripts' conf_get
126: #     answers it and as conf_valid refuses the whole file. The first cut
127: #     read /Mine/'My as the folder, one no script would ever use (the audit
128: #     of the fix round, gpt G2-C-01).
129: # Nothing when the key is absent. The same awk as cloud_content_backup's and
130: # cloud_content_restore's conf_get, on the file SYNC_CONF names.
131: conf_get() { # <KEY> (the content scripts' reader, mirrored so every reader agrees, D-CLOUD-149): its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
132:     [ -f ${SYNC_CONF} ] || return 0
133:     awk -v k="$1" '
134:         { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
135:         index($0, k "=") != 1 && !other \
136:             && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
137:         index($0, k "=") == 1 {
138:             s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
139:             c = substr(s, 1, 1)
140:             if (c == "\"") {
141:                 # Inside double quotes bash reads \" \\ \$ and \` as the one
142:                 # character each (PL-015), and so does this; an unescaped $
143:                 # or backtick is an expansion this reader does not make, and
144:                 # any other backslash is refused as conf_valid refuses it.
145:                 n = length(s); i = 2; closed = 0
146:                 while (i <= n) {
147:                     d = substr(s, i, 1)
148:                     if (d == "\"") { closed = 1; break }
149:                     if (d == "\\") {
150:                         e = substr(s, i + 1, 1)
151:                         if (e == "\"" || e == "\\" || e == "$" || e == "`") { v = v e; i += 2; continue }
152:                         ok = 0
153:                         why = (e == "") ? "a value continued onto the next line, which this reader does not follow" \
154:                                         : "a backslash inside double quotes that is not one of the escapes bash reads there"
155:                         break
156:                     }
157:                     if (d == "$" || d == "`") { ok = 0; why = "a $ or a backtick inside double quotes"; break }
158:                     v = v d; i++
159:                 }
160:                 if (ok && !closed) { ok = 0; why = "a double-quoted value that does not close on its line" }
161:                 if (ok) r = substr(s, i + 1)
162:             } else if (c == "'"'"'") {
163:                 j = index(substr(s, 2), c)
164:                 if (j) { v = substr(s, 2, j - 1); r = substr(s, j + 2) } else { ok = 0; why = "a single-quoted value that does not close on its line" }
165:             } else {
166:                 match(s, /^[A-Za-z0-9_.\/:@%+,=-]*/); v = substr(s, 1, RLENGTH); r = substr(s, RLENGTH + 1)
167:             }
168:             if (ok && r !~ /^([ \t]+(#.*)?)?$/) { ok = 0; why = "something after the value that is not a # comment" }
169:             if (!found) { found = 1; first = v; firstok = ok; firstwhy = "line " NR ": " why }
170:         }
171:         END {
172:             if (cntrl) { print "line " cntrl ": a control character other than a tab"; exit 2 }
173:             if (other) { print "line " other ": " k " set in a form this reader does not read"; exit 2 }
174:             if (found && !firstok) { print firstwhy; exit 2 }
175:             if (found) print first
176:         }
177:     ' ${SYNC_CONF}
178: }
179: 
180: # Wait for any confirm/cancel input: controller (evtest) or keyboard.
181: wait_for_button() {
182:     local input_device=""
183:     for dev in /dev/input/event*; do
184:         if [ -c "$dev" ]; then
185:             local supports=$(udevadm info "$dev" 2>/dev/null | awk '/ID_INPUT_JOYSTICK=1/ {print "joystick"}')
186:             if [ "$supports" = "joystick" ]; then
187:                 input_device="$dev"
188:                 break
189:             fi
190:         fi
191:     done
192:     if [ -n "$input_device" ]; then
193:         evtest "$input_device" 2>/dev/null | grep -m 1 -E "BTN_(SOUTH|EAST|A|B|START).*value 1" >/dev/null
194:     else
195:         read -sn1 2>/dev/null
196:     fi
197: }
198: 
199: # Connection facts, shared by the console flow and the native UI.
200: # resolve_connection sets SSH_CMD, SHOW_QR, OVERRIDE_ACTIVE and IP_ADDR
201: # (empty when offline).
202: resolve_connection() {
203:     OVERRIDE_ACTIVE=0
204:     IP_ADDR=$(ip route get 1 2>/dev/null | awk '{for (i=1;i<=NF;i++) if ($i=="src") {print $(i+1); exit}}')
205:     # The -L tunnel lets the provider sign-in page (which rclone serves on
206:     # the handheld at localhost:53682) open in the computer's own browser,
207:     # so the full 'auto config' flow works over SSH - see
208:     # rclone.org/remote_setup.
209:     SSH_CMD="ssh -L 53682:localhost:53682 root@${IP_ADDR}"
210:     SHOW_QR=1
211:     # Optional connection override: when the device is reached through a
212:     # gateway that remaps its address (development setups, tunnels,
213:     # proxies), the command in this file is shown instead of the direct one.
214:     OVERRIDE_FILE="/storage/.config/cloud_setup_ssh"
215:     if [ -s "${OVERRIDE_FILE}" ]; then
216:         SSH_CMD=$(head -n1 "${OVERRIDE_FILE}")
217:         SHOW_QR=0
218:         OVERRIDE_ACTIVE=1
219:         log_message "Using connection override: ${SSH_CMD}"
220:     fi
221: }
222: 
223: # True when at least one inbound SSH session is established (a peer is
224: # connected to local port 22). Reads /proc/net/tcp* directly so it works
225: # without ss/netstat; port 22 is 0016 hex, state 01 is ESTABLISHED.
226: ssh_session_established() {
227:     local f
228:     for f in /proc/net/tcp /proc/net/tcp6; do
229:         [ -r "$f" ] || continue
230:         if awk 'NR>1 { n=split($2,a,":"); if (a[n]=="0016" && $4=="01") found=1 } END { exit found?0:1 }' "$f"; then
231:             return 0
232:         fi
233:     done
234:     return 1
235: }
236: 
237: # True when something on the device already listens on rclone's OAuth
238: # port 53682 (hex D1B2, state 0A is LISTEN) - a stale sign-in webserver
239: # from an interrupted `rclone config` would make the next auto-config
240: # attempt fail with "bind: address already in use".
241: auth_port_busy() {
242:     local f
243:     for f in /proc/net/tcp /proc/net/tcp6; do
244:         [ -r "$f" ] || continue
245:         if awk 'NR>1 { n=split($2,a,":"); if (a[n]=="D1B2" && $4=="0A") found=1 } END { exit found?0:1 }' "$f"; then
246:             return 0
247:         fi
248:     done
249:     return 1
250: }
251: 
252: # Does this cloud folder work on this remote?
253: #
254: # Dropbox, Google Drive and OneDrive are path-based: "/GAMES" is a folder and
255: # any name will do. S3, B2 and friends are bucket-based - the first path
256: # component IS the bucket, and bucket names have rules the shipped default
257: # breaks (uppercase is illegal), so a sync fails with InvalidBucketName and
258: # nothing in that message points back at this setting.
259: #
260: # rclone reports the distinction itself, so no provider list is hardcoded.
261: # Returns 0 when the path will work; prints a reason and returns 1 when not.
262: # Listings that decide something get a bound (as the sync scripts' do) -- the
263: # folder probe below and the parent walk alike; `backend features` asks
264: # rclone about itself and makes no round trip: a cloud that never answers is
265: # a refusal in 30 s, not a wizard that hangs. Until #151 PL-15 the probe was
266: # the one unbounded listing here, and this comment covered only the walk.
267: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
268: # Is this remote path missing, rather than unreadable? rclone answers "not
269: # found" (exit 3) when the server's reply is the one it maps to that, and a
270: # plain error (exit 1) when the words differ: an FTP server that answers a
271: # missing folder with 501 "No such directory." where the standard reply is
272: # 550 makes every "is it there yet?" branch read as "the cloud is broken"
273: # (#142, from the #133 matrix). The parent settles it, whatever the words:
274: # walk up until a level lists. A level that lists and lacks the next name is
275: # a path not created yet (0); one that lists and holds it means the failure
276: # was something else (1); a remote whose root will not list is broken (1).
277: # On a bucket an absent prefix lists as empty, which is the same answer
278: # (D-CLOUD-120). Called only after a listing has already failed with a code
279: # other than 3, so the everyday path costs nothing extra.
280: absent_not_broken() {
281:     local path="${1%/}" remote rel name parent listing
282:     remote="${path%%:*}:"; rel="${path#*:}"; rel="${rel#/}"
283:     while [ -n "${rel}" ]; do
284:         name="${rel##*/}"; parent="${rel%/*}"
285:         [ "${parent}" = "${rel}" ] && parent=""
286:         if listing=$(rclone lsf --dirs-only "${remote}/${parent:+${parent}/}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); then
287:             printf '%s\n' "${listing}" | grep -qFx -- "${name}/" && return 1
288:             return 0
289:         fi
290:         [ -n "${parent}" ] || return 1
291:         rel="${parent}"
292:     done
293:     return 1
294: }
295: 
296: # Callers pass the first remote; an empty one stops after the string checks,
297: # which hold with no remote configured at all.
298: syncpath_problem() {
299:     local path="$1" remote="$2" bucket probe
300:     path="/$(echo "${path}" | sed 's:^/*::; s:/*$::')"
301: 
302:     if [ "${path}" = "/" ]; then
303:         echo "Your cloud folder can't be empty."
304:         return 1
305:     fi
306:     # The config is shell, sourced by every cloud script: the characters a
307:     # shell reads inside double quotes, and control characters, are refused
308:     # where the folder is typed (audit #307 PL-051, conf_set).
309:     case "${path}" in
310:         *[\"\$\`\\]*|*[[:cntrl:]]*)
311:             echo "Your cloud folder's name can't contain \", \$, \`, or \\."
312:             return 1
313:             ;;
314:     esac
315:     # Every part of the path is a folder's name, and the checks below read
316:     # the text. A part that is empty (//), . or .. names no folder of its
317:     # own: /Mine/Backups/. is /Mine/Backups on a cloud that resolves it,
318:     # while its siblings -- <parent>/Backups and <parent>/Content, made from
319:     # the text by dirname -- came out as /Mine/Backups/Backups and
320:     # /Mine/Backups/Content, inside it: the nesting the sibling check below
321:     # exists to stop, walked past (the audit of the fix round, PL-009; gpt
322:     # G2-C-04). Refused where it is typed, before any other check reads the
323:     # text, with the folder the path would have meant.
324:     case "${path}/" in
325:         *//*|*/./*|*/../*)
326:             local part canon="" try
327:             local -a parts=()
328:             IFS=/ read -r -a parts <<< "${path#/}"
329:             for part in "${parts[@]}"; do
330:                 case "${part}" in
331:                     ""|.) ;;
332:                     ..) canon="${canon%/*}" ;;
333:                     *) canon="${canon}/${part}" ;;
334:                 esac
335:             done
336:             if [ -z "${canon}" ]; then
337:                 echo "Your cloud folder can't be empty."
338:                 return 1
339:             fi
340:             # Offered only as a folder the checks below take: two levels
341:             # at least, and not named like its own siblings.
342:             try="${canon}"
343:             case "${canon#/}" in */*) ;; *) try="${canon}/Saves" ;; esac
344:             case "$(printf '%s' "${try##*/}" | tr 'A-Z' 'a-z')" in
345:                 backups|content) try="${try%/*}/Saves" ;;
346:             esac
347:             echo "Your cloud folder can't have an empty part, or a part called . or .., in its path."
348:             echo "Try ${try}."
349:             return 1
350:             ;;
351:     esac
352:     # Player-facing, these call it the cloud folder, which is what the
353:     # interface's row and its refusal dialog call it (G-C-03 claude).
354:     #
355:     # The saves folder has to sit inside another folder. Its settings
356:     # backups and games are kept beside it -- <parent>/Backups and
357:     # <parent>/Content -- and a saves folder at the top of the cloud has no
358:     # parent to keep them in. The setter used to put them INSIDE it instead
359:     # (/GAMES/Backups, /GAMES/Content): the nesting a mirror of the saves
360:     # folder deletes, because to the saves allowlist every file in them is
361:     # excluded (audit #307 PL-015, rclone-cloud-sync.md). So it is refused
362:     # where it is typed, with the folder to use instead -- on a bucket remote
363:     # that is the bucket and a folder in it, the shape the bucket message
364:     # below asks for anyway.
365:     case "${path#/}" in
366:         */*) ;;
367:         *)
368:             echo "Your cloud folder needs to sit inside another folder, so your settings backups and games can go beside it."
369:             echo "Try ${path}/Saves."
370:             return 1
371:             ;;
372:     esac
373:     # And the three have to be three folders. The settings and content
374:     # folders are <parent>/Backups and <parent>/Content, so a saves folder
375:     # called Backups or Content is its own sibling: two tiers in one folder,
376:     # and the saves sync walking the other tier's files (audit #307, G-C-01).
377:     # Compared case-folded, because Dropbox and OneDrive fold case.
378:     local parent="${path%/*}" folded
379:     folded="$(printf '%s' "${path}" | tr 'A-Z' 'a-z')"
380:     local sibling=""
381:     [ "${folded}" = "$(printf '%s' "${parent}/Backups" | tr 'A-Z' 'a-z')" ] && sibling="your settings backups"
382:     [ "${folded}" = "$(printf '%s' "${parent}/Content" | tr 'A-Z' 'a-z')" ] && sibling="your ROMs and BIOS"
383:     if [ -n "${sibling}" ]; then
384:         echo "Your cloud folder can't be called ${path##*/}: ${sibling} go in a folder of that name beside it."
385:         echo "Try ${parent}/Saves."
386:         return 1
387:     fi
388:     [ -n "${remote}" ] || return 0
389: 
390:     # No provider rules are encoded here on purpose. rclone does not validate
391:     # bucket names itself - it hands them to the provider and relays the
392:     # rejection - so the rules live with the provider, differ between them,
393:     # and would go stale in this script. The problem was never missing
394:     # validation; it was validation arriving at sync time, in a log, as
395:     # "InvalidBucketName" with nothing tying it to the folder that caused it.
396:     #
397:     # So: ask the provider now, and attach the answer to the setting.
398:     #
399:     # Only what rclone says went wrong, never its listing. This used to read
400:     # stdout as well, so a folder that already existed and held anything --
401:     # a saves folder with savestates/ in it, which is every folder somebody
402:     # would type on a second device -- was refused as "your provider would
403:     # not accept this folder", with the folder's own contents quoted as the
404:     # reason (found by the A3 fixture on the VM pair, 2026-09-06).
405:     probe=$(rclone lsd "${remote}${path#/}" "${RCLONE_LIST_OPTS[@]}" --log-level ERROR 2>&1 >/dev/null | head -2)
406:     case "${probe}" in
407:         # A folder that does not exist yet is fine - it gets created on use.
408:         *"not found"*|*NoSuchBucket*|"") return 0 ;;
409:     esac
410:     # The same folder, on a server whose "missing" rclone relays as a plain
411:     # error rather than "not found" (#142). On a path-based cloud a folder
412:     # its parent lacks is a folder not created yet, whatever the words. On
413:     # a bucket the first component is a bucket name the provider judges,
414:     # and the provider's own answer stands -- the parent rule would read
415:     # InvalidBucketName as "not there yet" and store the name it rejected.
416:     #
417:     # Which kind this remote is, rclone says in JSON, and the answer has to
418:     # be one of the two before anything rests on it. A `backend features`
419:     # that fails or prints neither is "unknown", and unknown takes the
420:     # provider's refusal at face value: the parent walk runs only on a
421:     # remote known to be path-based. Until #151 PL-14 a failed call read as
422:     # "not bucket-based" -- a grep over empty output -- and the walk ran,
423:     # so the one guard against storing a rejected bucket name fell open
424:     # exactly when rclone could not be asked.
425:     local features bucket_based=unknown
426:     if features=$(rclone backend features "${remote}" 2>/dev/null); then
427:         case "${features}" in
428:             *'"BucketBased": true'*)  bucket_based=yes ;;
429:             *'"BucketBased": false'*) bucket_based=no ;;
430:         esac
431:     fi
432:     if [ "${bucket_based}" = no ] && absent_not_broken "${remote}${path#/}"; then
433:         return 0
434:     fi
435: 
436:     # Something is wrong. If the remote is bucket-based, name the reason the
437:     # message will not: the first path component is a bucket, not a folder.
438:     if [ "${bucket_based}" = yes ]; then
439:         bucket="${path#/}"; bucket="${bucket%%/*}"
440:         echo "Your provider wouldn't accept \"${bucket}\"."
441:         echo
442:         echo "This provider keeps things in buckets, so the first part of the"
443:         echo "folder is a bucket name, not a folder - and bucket names have"
444:         echo "rules that folders do not. They are also shared with everyone"
445:         echo "else using the provider, not private to your account."
446:         echo
447:         echo "  ${probe}"
448:         echo
449:         echo "Try something like /pixelelated-saves-yourname/Saves instead."
450:     else
451:         echo "Your provider wouldn't accept this folder:"
452:         echo
453:         echo "  ${probe}"
454:     fi
455:     return 1
456: }
457: 
458: case "$1" in
459:     --info)
460:         # Machine-readable connection facts for the native UI.
461:         resolve_connection
462:         echo "IP=${IP_ADDR}"
463:         echo "SSH_CMD=${SSH_CMD}"
464:         echo "OVERRIDE=${OVERRIDE_ACTIVE}"
465:         # Whether a root password is set, never the password: this output is
466:         # parsed by EmulationStation through a pipeline, and a credential that
467:         # crosses a script boundary is one careless echo from a log (#116,
468:         # D-INFRA-008). The page that must show or pre-fill it reads
469:         # root.password in-process from its own settings.
470:         echo "PASSWORD_SET=$([ -n "$(get_setting root.password)" ] && echo 1 || echo 0)"
471:         echo "SSH_UP=$(systemctl is-active sshd 2>/dev/null)"
472:         echo "AUTH_PORT=$(auth_port_busy && echo busy || echo free)"
473:         # Both names for one value: EmulationStation reads SYNCPATH= until its
474:         # side of the vocabulary sweep (#73) lands; SAVES_REMOTE= is the name.
475:         # A folder in a form the scripts cannot read is named as none: the
476:         # sync refuses that config too, and the folder editor the interface
477:         # opens from this line is the way to set one it can (gpt G2-C-01).
478:         if ! saves_remote="$(conf_get SAVES_REMOTE)"; then
479:             log_message "SAVES_REMOTE in ${SYNC_CONF} is not in a form the sync reads (${saves_remote}); no folder named"
480:             saves_remote=""
481:         fi
482:         echo "SAVES_REMOTE=${saves_remote}"
483:         echo "SYNCPATH=${saves_remote}"
484:         echo "REMOTES=$(rclone listremotes 2>/dev/null | tr '\n' ' ')"
485:         # Which provider this device is actually connected to. The name is the
486:         # player's own label for the remote; the type is rclone's word for the
487:         # service (dropbox, drive, webdav...), which EmulationStation turns
488:         # into the name the player picked it by. Until this, nothing on any
489:         # screen said who the cloud was -- the setup page offered to connect
490:         # one and never mentioned the one already there (fork #110).
491:         remote_name="$(rclone listremotes 2>/dev/null | head -1)"
492:         remote_name="${remote_name%:}"
493:         echo "REMOTE_NAME=${remote_name}"
494:         echo "REMOTE_TYPE=$(rclone config show "${remote_name}" 2>/dev/null | sed -n 's/^[[:space:]]*type[[:space:]]*=[[:space:]]*//p' | head -1)"
495:         exit 0
496:     ;;
497:     --content-location)
498:         # Where is this device's content actually stored in the cloud?
499:         #
500:         # CONTENT_REMOTE is new, so an upgrading device gains one it never had.
501:         # Anyone who had put ROMs at the remote root by hand - the only way
502:         # content reached the cloud before f60ea2b8f8 - would find the content
503:         # list empty and nothing explaining why. Report the situation as
504:         # key=value so a UI can offer the choice rather than leaving the owner
505:         # to guess.
506:         #
507:         # Reported, never acted on: moving somebody's cloud files is not a
508:         # thing to do behind their back.
509:         REMOTE=$(rclone listremotes 2>/dev/null | head -1)
510:         [ -z "${REMOTE}" ] && { echo "STATE=no-remote"; exit 2; }
511:         if ! CP="$(conf_get CONTENT_REMOTE)"; then
512:             echo "STATE=unreadable"
513:             exit 1
514:         fi
515: 
516:         # Only directories this device could actually have put there count as
517:         # ours. Anything else at the root is the owner's own business.
518:         LOCAL=$(cloud_content_backup --list 2>/dev/null | tr '\n' ' ')
519:         AT_PATH=0; AT_ROOT=0; ROOT_DIRS=""
520:         # Both listings carry the bound every listing here does (#308 claude
521:         # F-RS-13): rclone's own defaults are three runs of ten retries,
522:         # under a page waiting on the answer.
523:         if [ -n "${CP}" ]; then
524:             AT_PATH=$(rclone lsf --dirs-only "${REMOTE}${CP#/}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | wc -l)
525:         fi
526:         for d in $(rclone lsf --dirs-only "${REMOTE}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | sed 's:/$::'); do
527:             case " ${LOCAL} " in
528:                 *" ${d} "*) AT_ROOT=$((AT_ROOT + 1)); ROOT_DIRS="${ROOT_DIRS}${d} " ;;
529:             esac
530:         done
531: 
532:         # Where the games actually are, when the configured root holds nothing
533:         # of ours (fork #352, D-CLOUD-156): the cloud root's Content folder --
534:         # the saves folder's parent, /pixelelated/Content by default -- is
535:         # looked at for a ROMs or BIOS folder, and named, so the interface can
536:         # offer it before it asks the player to choose.
537:         FOUND=""
538:         if [ "${AT_PATH}" -eq 0 ] && [ "${AT_ROOT}" -eq 0 ]; then
539:             SV="$(conf_get SAVES_REMOTE)" || SV=""
540:             SV="${SV%/}"; SP="${SV%/*}"; [ "${SP}" = "${SV}" ] && SP=""
541:             CAND="${SP}/Content"
542:             if [ "${CAND}" != "${CP%/}" ] \
543:                && rclone lsf --dirs-only "${REMOTE}${CAND#/}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -qE '^(ROMs|BIOS)/$'; then
544:                 FOUND="${CAND}"
545:             fi
546:         fi
547:         echo "CONTENT_REMOTE=${CP}"
548:         echo "AT_PATH=${AT_PATH}"
549:         echo "AT_ROOT=${AT_ROOT}"
550:         echo "ROOT_DIRS=${ROOT_DIRS% }"
551:         echo "FOUND=${FOUND}"
552:         # An empty CONTENT_REMOTE means the root IS the content path, so content
553:         # sitting there is correct rather than stranded - otherwise a UI would
554:         # keep offering to fix something already resolved.
555:         if [ -z "${CP}" ] && [ "${AT_ROOT}" -gt 0 ]; then
556:             echo "STATE=ok"
557:         elif [ "${AT_PATH}" -gt 0 ]; then
558:             echo "STATE=ok"
559:         elif [ "${AT_ROOT}" -gt 0 ]; then
560:             echo "STATE=stranded-at-root"
561:         elif [ -n "${FOUND}" ]; then
562:             echo "STATE=found-elsewhere"
563:         else
564:             echo "STATE=empty"
565:         fi
566:         exit 0
567:     ;;
568: 
569:     --set-content-remote)
570:         # Point this device's content root at a folder the player chose or
571:         # the scan found (the chooser, fork #352; CONTENT_REMOTE alone --
572:         # the saves and settings folders stay where they are). Moves
573:         # nothing, reversible, instant. The string checks are the saves
574:         # folder's: one leading slash, no shell characters, no "..", which
575:         # the sync's reader would refuse (conf_get) or rclone would
576:         # resolve to a folder nobody named. A folder at the top of the
577:         # cloud is fine here, unlike a saves folder (it has no siblings).
578:         NEWPATH="$2"
579:         [ -z "${NEWPATH}" ] && { echo "ERROR empty path"; exit 1; }
580:         NEWPATH="/$(echo "${NEWPATH}" | sed 's:^/*::; s:/*$::')"
581:         case "${NEWPATH}" in
582:             "/") echo "ERROR root path not allowed"; exit 1 ;;
583:             *..*) echo "That folder name can't be used."; exit 1 ;;
584:             *[\$\`\\\"\']*|*[[:space:]]*) echo "That folder name has characters your cloud sync settings can't hold."; exit 1 ;;
585:         esac
586:         if ! conf_set CONTENT_REMOTE "${NEWPATH}"; then
587:             echo "Your cloud sync settings couldn't be saved."
588:             log_message "Content path NOT changed to ${NEWPATH}: ${SYNC_CONF} could not be written"
589:             exit 1
590:         fi
591:         log_message "Content path set to ${NEWPATH} by request"
592:         echo "OK ${NEWPATH}"
593:         exit 0
594:     ;;
595:     --use-content-root)
596:         # The safe resolution: point this device back at the root where its
597:         # content already is. Moves nothing, reversible, instant.
598:         if ! conf_set CONTENT_REMOTE ""; then
599:             echo "ERROR the cloud sync settings could not be saved"
600:             log_message "Content path NOT changed: ${SYNC_CONF} could not be written"
601:             exit 1
602:         fi
603:         log_message "Content path set to the remote root by request"
604:         echo "OK content stays at the remote root"
605:         exit 0
606:     ;;
607: 
608:     --accept-saves-root)
609:         # The owner says the card the saves folder is on now is the right
610:         # one (#83): remember it, so saves transfers stop refusing.
611:         tool="$(dirname "$(readlink -f "$0")")/cloud_saves_root"
612:         [ -x "${tool}" ] || tool=/usr/bin/cloud_saves_root
613:         exec "${tool}" accept
614:     ;;
615:     --check-syncpath)
616:         # Validate a candidate cloud folder without changing anything, so the
617:         # UI can refuse a bad one where it is typed rather than letting it
618:         # fail later inside a sync.
619:         if [ -n "${2:-}" ]; then
620:             CAND="$2"
621:         elif ! CAND="$(conf_get SAVES_REMOTE)"; then
622:             echo "Your cloud sync settings couldn't be read."
623:             exit 1
624:         else
625:             # The conf's own value is judged as the migration judges it
626:             # (the audit of the fixes, claude G3-D-07): one trailing slash
627:             # is a spelling, not an empty part.
628:             CAND="${CAND%/}"
629:         fi
630:         REMOTE=$(rclone listremotes 2>/dev/null | head -1)
631:         if [ -z "${REMOTE}" ]; then
632:             echo "No cloud remote configured."
633:             exit 2
634:         fi
635:         if syncpath_problem "${CAND}" "${REMOTE}"; then
636:             echo "OK ${CAND}"
637:             exit 0
638:         fi
639:         exit 1
640:     ;;
641: 
642:     --set-saves-remote|--set-syncpath)
643:         # Change the cloud folder the saves live in, and move the settings
644:         # backups and the ROMs with it -- as SIBLINGS, never inside it.
645:         # This used to write SETTINGS_REMOTE="<saves>/backup", which is the
646:         # first-layout nesting cloud_migrate_layout exists to undo and the
647:         # trap cloud_backup warns about: a mirror of the saves folder can
648:         # delete the archives kept beneath it. The siblings are the saves
649:         # folder's parent's: <parent>/Backups and <parent>/Content. A saves
650:         # folder at the top of the cloud has no parent and is refused
651:         # (syncpath_problem) -- it used to adopt the folder itself as the
652:         # parent, which nested both inside it (audit #307 PL-015).
653:         NEWPATH="$2"
654:         if [ -z "${NEWPATH}" ]; then
655:             echo "ERROR empty path"
656:             exit 1
657:         fi
658:         # Normalize: exactly one leading slash, no trailing slash.
659:         NEWPATH="/$(echo "${NEWPATH}" | sed 's:^/*::; s:/*$::')"
660:         if [ "${NEWPATH}" = "/" ]; then
661:             echo "ERROR root path not allowed"
662:             exit 1
663:         fi
664:         # Refuse a path this remote cannot use, rather than storing it and
665:         # letting the next sync fail with a provider error naming nothing the
666:         # player recognises. The string checks -- a parent for the siblings
667:         # (PL-015), no shell characters (PL-051) -- hold with no remote.
668:         SP_REMOTE=$(rclone listremotes 2>/dev/null | head -1)
669:         if ! syncpath_problem "${NEWPATH}" "${SP_REMOTE}"; then
670:             exit 1
671:         fi
672:         SP_PARENT="$(dirname "${NEWPATH}")"
673:         # All three or none (conf_set): a folder half-changed is a saves
674:         # folder whose settings still go to the old place.
675:         if ! conf_set SAVES_REMOTE "${NEWPATH}" \
676:                       SETTINGS_REMOTE "${SP_PARENT}/Backups" \
677:                       CONTENT_REMOTE "${SP_PARENT}/Content"; then
678:             # Under the interface's "THE CLOUD FOLDER WAS NOT CHANGED": this line
679:             # says why, and nothing the title already said (G-C-03 claude).
680:             echo "Your cloud sync settings couldn't be saved."
681:             log_message "Sync path NOT changed to ${NEWPATH}: ${SYNC_CONF} could not be written"
682:             exit 1
683:         fi
684:         log_message "Sync path changed to ${NEWPATH}"
685:         echo "OK ${NEWPATH}"
686:         exit 0
687:     ;;
688:     --free-auth-port)
689:         # Clear a stale sign-in webserver left by an interrupted
690:         # `rclone config`, so the next auto-config attempt can bind.
691:         pkill -f "rclone config" 2>/dev/null
692:         pkill -f "rclone authorize" 2>/dev/null
693:         log_message "Cleared stale processes holding the OAuth port"
694:         echo "OK"
695:         exit 0
696:     ;;
697:     --connected)
698:         # The native UI gates its connect step on this, so the player
699:         # cannot advance without an SSH session actually being open.
700:         if ssh_session_established; then
701:             echo "CONNECTED"
702:             exit 0
703:         fi
704:         echo "NONE"
705:         exit 1
706:     ;;
707:     --seed-folders)
708:         # Give a new remote a shape, so somebody with a fresh handheld can see
709:         # where their files go.
710:         #
711:         # Until the first upload these folders do not exist, so a player who
712:         # wants to seed their library from a computer first has to guess three
713:         # names and a per-system convention. The folders answer that; the
714:         # README in each answers what belongs there.
715:         #
716:         # The READMEs are also what makes this work at all on bucket-based
717:         # remotes (S3, B2): there the first path component is a bucket and the
718:         # rest is a key prefix, so an empty directory does not persist and
719:         # `rclone mkdir` on a subpath succeeds while creating nothing. A file
720:         # in the folder is what materialises it.
721:         #
722:         # Nothing is ever overwritten and nothing is deleted. Paths come from
723:         # the config, so a player who moved their cloud folder gets their own
724:         # layout seeded rather than ours.
725:         REMOTE=$(rclone listremotes 2>/dev/null | head -1)
726:         [ -z "${REMOTE}" ] && { echo "ERROR no remote"; exit 2; }
727:         # The folder is settled before anything is made
728:         # (cloud_migrate_layout --settle, D-CLOUD-169). A fresh install, or
729:         # a carried /GAMES, beside a fleet still on the earlier folder joins
730:         # it: seeding an empty /pixelelated beside the player's saves left a
731:         # new device reading a folder with none of them in it (the
732:         # mixed-installation test, D-CLOUD-158), and seeding the carried
733:         # /GAMES put a README there that every later check read as saves. A
734:         # carried default with nothing anywhere is pointed at the current
735:         # folders, which the seeding makes, as for any new cloud. A settle
736:         # that could not answer makes nothing. The wizard may still finish;
737:         # its boot step retries, without a misleading README at the old root.
738:         layout_tool="$(dirname "$(readlink -f "$0")")/cloud_migrate_layout"
739:         [ -x "${layout_tool}" ] || layout_tool=/usr/bin/cloud_migrate_layout
740:         if [ ! -x "${layout_tool}" ]; then
741:             log_message "Seeding: cloud folder settlement is unavailable; nothing was made"
742:             exit 1
743:         fi
744:         timeout 30 "${layout_tool}" --settle >/dev/null 2>&1; settle_rc=$?
745:         case "${settle_rc}" in
746:             0) log_message "Seeding: this device's cloud folder was settled first (cloud_migrate_layout --settle)" ;;
747:             3) ;; # A current, populated, custom or kept folder needs no transition.
748:             *) log_message "Seeding: cloud folder settlement exited ${settle_rc}; nothing was made"
749:                echo "Your cloud folder couldn't be checked, so no folders were made. Try again."
750:                exit "${settle_rc}" ;;
751:         esac
752:         # Read as text, never eval'd: the config is shell, and a value an
753:         # earlier build wrote could carry a command (PL-051). A folder in a
754:         # form the scripts cannot read makes nothing: read as empty, it
755:         # became the default folder here and was seeded in the player's
756:         # cloud (gpt G2-C-01).
757:         if ! SAVES_REMOTE="$(conf_get SAVES_REMOTE)" \
758:            || ! SETTINGS_REMOTE="$(conf_get SETTINGS_REMOTE)" \
759:            || ! CONTENT_REMOTE="$(conf_get CONTENT_REMOTE)"; then
760:             echo "Your cloud sync settings couldn't be read, so no folders were made."
761:             log_message "Seeding: a folder in ${SYNC_CONF} is not in a form the sync reads; nothing was made"
762:             exit 1
763:         fi
764:         SAVES="${SAVES_REMOTE:-/pixelelated/Saves}"
765:         BACKUPS="${SETTINGS_REMOTE:-/pixelelated/Backups}"
766:         # An empty CONTENT_REMOTE is not a missing one: it is
767:         # --use-content-root's "the cloud's root", which is where the
768:         # content scripts put ROMs/ and BIOS/ (ROOT="<remote>:"). Only a
769:         # config with no such line gets the default (#308 gpt F-RS-20).
770:         if grep -q '^CONTENT_REMOTE=' "${SYNC_CONF}" 2>/dev/null; then
771:             CONTENT="${CONTENT_REMOTE%/}"
772:         else
773:             CONTENT="/pixelelated/Content"
774:         fi
775: 
776:         for d in "${SAVES}" "${SAVES}/savefiles" "${SAVES}/savestates" \
777:                  "${SAVES}/screenshots" "${BACKUPS}" \
778:                  ${CONTENT:+"${CONTENT}"} "${CONTENT}/ROMs" "${CONTENT}/BIOS"; do
779:             # --s3-directory-markers writes a zero-byte object ending in "/",
780:             # which is how S3 itself represents a folder -- without it a
781:             # bucket remote silently keeps nothing, and mkdir still exits 0.
782:             # Ignored by path-based backends, so it costs nothing there.
783:             # Bounded like the listings (#308 claude F-RS-13, gpt F-RS-19):
784:             # up to two dozen calls under one 90 s box in the interface.
785:             rclone mkdir --s3-directory-markers "${REMOTE}${d}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null
786:         done
787:         # The layout marker (fork #356): one line at the parent of the saves
788:         # folder saying which shape of folders this cloud carries, read by
789:         # every device before it offers a move or a creation
790:         # (cloud_migrate_layout --state). Written here because seeding is
791:         # where a cloud first takes the current shape.
792:         # Not beside a folder this project once shipped as its default: a
793:         # device that joined one marks nothing, and a layout=2 marker at
794:         # /ROCKNIX would say a thing about that cloud that is not so.
795:         # The same version-aware writer owns publication for migration and
796:         # seeding. Custom and earlier layouts publish no current marker.
797:         "${layout_tool}" --write-marker; marker_rc=$?
798:         case "${marker_rc}" in
799:             0|3) ;;
800:             *) log_message "Seeding: layout marker publication failed (${marker_rc})"
801:                exit "${marker_rc}" ;;
802:         esac
803: 
804:         seed_note() {
805:             local dir="$1" listing tmp; shift
806:             # Never clobber a note the owner may have written themselves, and
807:             # never write on a guess. The folder's own listing says whether a
808:             # README.txt is in it. Asking for the file by name could not: a
809:             # listing that failed for any reason read as "absent" and the
810:             # owner's note was replaced (audit #307 PL-047), and on a bucket
811:             # a key that is not there lists as nothing with exit 0, which read
812:             # as "present" -- so no README was ever written there (#308
813:             # claude F-RS-09). A listing that fails writes nothing.
814:             if ! listing=$(rclone lsf --files-only "${REMOTE}${dir}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); then
815:                 log_message "Seeding: ${dir} could not be listed, so its README was not written"
816:                 return 1
817:             fi
818:             printf '%s\n' "${listing}" | grep -qFx -- 'README.txt' && return 0
819:             tmp=$(mktemp) || return 1
820:             printf '%s\n' "$@" > "${tmp}"
821:             # --ignore-existing: another device may have written one since
822:             # the listing.
823:             rclone copyto --ignore-existing "${tmp}" "${REMOTE}${dir}/README.txt" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null
824:             rm -f "${tmp}"
825:         }
826: 
827:         seed_note "${SAVES}" \
828:             "Game saves, save states, and screenshots." \
829:             "" \
830:             "  savefiles/    battery saves" \
831:             "  savestates/   save state snapshots" \
832:             "  screenshots/" \
833:             "" \
834:             "The handheld writes these itself. Nothing to put here by hand."
835: 
836:         seed_note "${BACKUPS}" \
837:             "Settings backups, one folder per handheld." \
838:             "" \
839:             "Written by the device. Nothing to put here by hand."
840: 
841:         # Not at the top of somebody's cloud: with content at the root, the
842:         # ROMs and BIOS folders carry their own notes and the root keeps
843:         # whatever the owner has there.
844:         [ -n "${CONTENT}" ] && seed_note "${CONTENT}" \
845:             "Put your games and BIOS files here." \
846:             "" \
847:             "  ROMs/       one folder per system - snes, psx, n64, gba, ..." \
848:             "  BIOS/       BIOS and firmware files" \
849:             "" \
850:             "The handheld reads these when you choose" \
851:             "\"Restore from the cloud\" on it."
852: 
853:         seed_note "${CONTENT}/ROMs" \
854:             "Your games, one folder per system." \
855:             "" \
856:             "Use the same folder names the handheld uses - snes, psx, n64," \
857:             "gba, megadrive, and so on. The game list on the device shows them."
858: 
859:         seed_note "${CONTENT}/BIOS" \
860:             "BIOS and firmware files." \
861:             "" \
862:             "These land in /storage/roms/bios on the handheld, keeping" \
863:             "whatever subfolder structure you use here."
864: 
865:         # Report what is actually there, not what we asked for: on a bucket
866:         # remote a mkdir can succeed and leave nothing behind.
867:         for d in "${SAVES}" "${BACKUPS}" "${CONTENT}/ROMs" "${CONTENT}/BIOS"; do
868:             # A listing, never lsjson --stat: on a bucket remote stat reports
869:             # success for any path at all, so the MISSING branch could never
870:             # be reached -- the report would have been unconditionally OK,
871:             # which is the shape of an assertion that cannot fail.
872:             if [ -n "$(rclone lsf "${REMOTE}${d}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | head -1)" ] \
873:                || rclone lsf --dirs-only "${REMOTE}${d%/*}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -qFx -- "${d##*/}/"; then
874:                 echo "OK ${d}"
875:             else
876:                 echo "MISSING ${d}"
877:             fi
878:         done
879:         exit 0
880:     ;;
881: 
882:     --check)
883:         # Verify a remote ($2 if given, else the first configured one);
884:         # plain-text verdict on stdout, exit 0 = working, 1 = missing,
885:         # 2 = configured but unreachable.
886:         REMOTE="$2"
887:         [ -z "${REMOTE}" ] && REMOTE=$(rclone listremotes 2>/dev/null | head -1)
888:         if [ -z "${REMOTE}" ]; then
889:             echo "NONE"
890:             log_message "Cloud setup check: no remotes configured"
891:             exit 1
892:         fi
893:         # The probe is bounded like every other listing here (RCLONE_LIST_OPTS:
894:         # one run, three low-level retries). It carried only the two timeouts,
895:         # so rclone's own defaults applied -- three runs of ten retries each --
896:         # under a blocking spinner on three interface pages; the shape #113
897:         # bounded for the syncs (traced 2026-09-25, #273).
898:         if rclone lsd "${REMOTE}" "${RCLONE_LIST_OPTS[@]}" >/dev/null 2>&1; then
899:             echo "OK ${REMOTE}"
900:             log_message "Cloud setup verified working remote: ${REMOTE}"
901:             exit 0
902:         fi
903:         echo "FAIL ${REMOTE}"
904:         log_message "Cloud setup: remote ${REMOTE} failed verification"
905:         exit 2
906:     ;;
907: esac
908: 
909: clear
910: 
911: # Need a network address to be reachable over SSH
912: resolve_connection
913: if [ -z "${IP_ADDR}" ]; then
914:     echo -e "\e[31mNo network connection detected.\e[0m"
915:     echo "Connect to a network first, then try again."
916:     echo
917:     echo "Press any button to exit."
918:     wait_for_button
919:     exit 1
920: fi
921: 
922: ROOTPASS=$(get_setting root.password)
923: 
924: log_message "Cloud setup instructions shown (${SSH_CMD})"
925: 
926: echo -e "\e[32m=> ${OS_NAME:-ROCKNIX} CLOUD SETUP\e[0m"
927: echo
928: echo "Connect from a computer on your network and follow rclone's"
929: echo "step-by-step setup. It signs in to your cloud provider and picks"
930: echo "the account/folder to use."
931: echo
932: echo -e "  1. On your computer, connect:  \e[1;36m${SSH_CMD}\e[0m"
933: echo -e "     Password:                   \e[1;36m${ROOTPASS:-<not set>}\e[0m"
934: echo -e "  2. Run:                        \e[1;36mrclone config\e[0m"
935: echo "     Choose 'n' for a new remote, pick your provider, and follow"
936: echo "     the prompts. Defaults are fine if you are unsure."
937: echo "     When asked 'Use auto config?', answer Y, then open the"
938: echo "     sign-in link it prints in your computer's browser."
939: echo "  3. Quit with 'q' when the remote is listed, then come back here."
940: echo
941: if [ "${SHOW_QR}" = "1" ]; then
942:     echo "Phone with an SSH app instead? Scan to connect:"
943:     qrencode -t ANSIUTF8 -m 2 "ssh://root@${IP_ADDR}"
944:     echo
945: fi
946: echo "Press any button here when you are done (or to cancel)."
947: 
948: wait_for_button
949: 
950: echo
951: REMOTE=$(rclone listremotes 2>/dev/null | head -1)
952: if [ -z "${REMOTE}" ]; then
953:     echo -e "\e[33mNo cloud remote configured yet.\e[0m"
954:     echo "Run this again once you have completed 'rclone config'."
955:     log_message "Cloud setup finished with no remotes configured"
956:     sleep 5
957:     exit 0
958: fi
959: 
960: echo "Checking ${REMOTE} ..."
961: if rclone lsd "${REMOTE}" "${RCLONE_LIST_OPTS[@]}" >/dev/null 2>&1; then
962:     echo -e "\e[32mCloud remote configured and working: ${REMOTE}\e[0m"
963:     echo "You can now use the cloud backup and restore tools."
964:     log_message "Cloud setup verified working remote: ${REMOTE}"
965: else
966:     echo -e "\e[31mThe remote ${REMOTE} exists but is not responding.\e[0m"
967:     echo "Its sign-in may be incomplete or expired. Connect again and"
968:     echo "run 'rclone config reconnect ${REMOTE}' to repair it."
969:     log_message "Cloud setup: remote ${REMOTE} failed verification"
970: fi
971: sleep 5
972: exit 0
```


## SOURCE projects/ROCKNIX/packages/network/rclone/sources/cloud_scan

```text
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present rasteratops (https://github.com/rasteratops)
4: 
5: # cloud_scan - what the cloud holds for this device, before anything is offered.
6: #
7: # The transfer pages scan first and offer only what the scan found
8: # (D-CLOUD-156, fork #350): the folder's state, the settings archives by
9: # device label, where the content is, and -- once the player has ticked
10: # what to move -- the content listing in those classes. This runs those
11: # reads and talks to the scan page in the protocol every cloud page reads
12: # (">>> unit", ">>> doing", ">>> why"), writing each result to a file the
13: # options page builds from.
14: #
15: #   cloud_scan                   the opening scan: the folder, the settings
16: #                                archives, where the content is (three items)
17: #   cloud_scan --content [--with-media|--media-only]
18: #                                the content listing for the systems page,
19: #                                in the classes ticked (one item)
20: #   cloud_scan --folder          the folder alone, for the cloud folder step
21: #                                at the end of cloud setup and at boot
22: #                                (D-CLOUD-170, fork #363; one item)
23: #
24: # Reads, with two exceptions, both settings: a fresh install beside a fleet
25: # still on an earlier folder joins it (cloud_migrate_layout --join), and a
26: # device on a superseded folder whose current folder another device has
27: # already made is re-pointed to it (cloud_migrate_layout --follow;
28: # D-CLOUD-160's "your other devices will follow"). Nothing in the cloud
29: # changes, so no lock is taken and a sync may run beside it.
30: #
31: # Results, under /storage/.cache/cloud_sync/scan/:
32: #   state             cloud_migrate_layout --state, one fact per line
33: #   archives          every settings archive in the Backups folder, one per line
34: #   settings          LABEL= (this device's), MINE= (its newest), NEWEST= (overall), COUNT=
35: #   content-location  cloud_setup --content-location, key=value
36: #   root-dirs         the folders at the cloud's root, one per line (the chooser's)
37: #   done              the epoch the opening scan completed; absent while it runs or failed
38: #   scan              cloud_content_restore --scan's rows        (--content)
39: #   systems           the systems this device syncs (--systems)  (--content)
40: #   content-done      the epoch the content scan completed       (--content)
41: #
42: # Exit: 0 all read; 69 no network (the page says SKIPPED - YOU'RE NOT
43: # ONLINE); 1 no cloud storage set up; otherwise the failing read's code,
44: # with a ">>> why" in the player's words before it (D-UI-028).
45: 
46: . /etc/profile 2>/dev/null
47: 
48: OUT=/storage/.cache/cloud_sync/scan
49: SYNC_CONF=/storage/.config/cloud_sync.conf
50: readonly EXIT_NO_NETWORK=69
51: # Every listing here is bounded as the other readers' are (#308 claude F-RS-13).
52: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
53: 
54: say() { echo "$@"; }
55: log() { logger -t cloud_scan "$*" 2>/dev/null; }
56: why() { echo ">>> why $*"; }
57: 
58: # The shared reader (cloud_setup's, the content scripts', D-CLOUD-149): a
59: # value in a form the sync does not read is nothing here, never a folder.
60: conf_get() { # <KEY>
61:     [ -f "${SYNC_CONF}" ] || return 0
62:     awk -v k="$1" '
63:         index($0, k "=") == 1 {
64:             s = substr($0, length(k) + 2); v = ""
65:             if (s ~ /^"/) { s = substr(s, 2); i = index(s, "\""); if (i == 0) exit 2; v = substr(s, 1, i - 1) }
66:             else if (s ~ /^\047/) { s = substr(s, 2); i = index(s, "\047"); if (i == 0) exit 2; v = substr(s, 1, i - 1) }
67:             else { i = index(s, "#"); v = (i == 0) ? s : substr(s, 1, i - 1); sub(/[ \t]+$/, "", v) }
68:             if (v ~ /[$`\\]/) exit 2
69:             print v; exit 0
70:         }
71:     ' "${SYNC_CONF}"
72: }
73: 
74: sibling() { # <name>: the script beside this one, else the installed one
75:     local t; t="$(dirname "$(readlink -f "$0")")/$1"
76:     [ -x "${t}" ] || t="/usr/bin/$1"
77:     echo "${t}"
78: }
79: device_label() {
80:     local tool; tool=$(sibling cloud_device_id)
81:     [ -x "${tool}" ] && "${tool}" --label 2>/dev/null | tr -cd 'A-Za-z0-9_-'
82: }
83: os_name() {
84:     local name="${OS_NAME}"
85:     [ -z "${name}" ] && name=$(sed -n 's/^OS_NAME="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' /etc/os-release 2>/dev/null | head -1)
86:     [ -z "${name}" ] && name="ROCKNIX"
87:     printf '%s\n' "${name}" | tr -cd 'A-Za-z0-9_-'
88: }
89: 
90: # What an rclone exit means to a player: the sentences the card and the
91: # rows already carry for these codes (ThreadedCloudSync::whyForCode), so
92: # one code is never called two things and the French reaches them.
93: why_for_rc() {
94:     case "$1" in
95:         3|4) why "COULDN'T FIND YOUR CLOUD FOLDER" ;;
96:         5|124) why "YOUR CLOUD STOPPED ANSWERING" ;;   # 124: a bounded step's timeout (the join)
97:         7|8) why "YOUR CLOUD WOULDN'T TAKE THE FILES" ;;
98:         *)   why "SOMETHING WENT WRONG" ;;
99:     esac
100: }
101: 
102: # Before any read: a place to write, a route, a remote.
103: prepare() {
104:     mkdir -p "${OUT}" || { log "scan: cannot make ${OUT}"; why "SOMETHING WENT WRONG"; exit 1; }
105:     # No route, nothing tried: the page says SKIPPED - YOU'RE NOT ONLINE from
106:     # the code alone (D-CLOUD-072, D-CLOUD-112).
107:     if ! ip route show default 2>/dev/null | grep -q .; then
108:         log "scan: no default route; skipped"
109:         exit "${EXIT_NO_NETWORK}"
110:     fi
111:     REMOTE=$(rclone listremotes 2>/dev/null | head -1)
112:     if [ -z "${REMOTE}" ]; then
113:         why "YOUR CLOUD STORAGE ISN'T SET UP YET"
114:         exit 1
115:     fi
116: }
117: 
118: # A read that failed ends the run with its why; 69 is the page's own sentinel.
119: stop_on() { # <rc> <what>
120:     [ "$1" -eq 0 ] && return 0
121:     log "scan: $2 exited $1"
122:     [ "$1" -eq "${EXIT_NO_NETWORK}" ] && exit "$1"
123:     why_for_rc "$1"
124:     exit "$1"
125: }
126: 
127: # --content: the listing the systems page is built from, in the classes
128: # the player ticked (cloud_content_restore --scan's own flags), and the
129: # systems this device syncs. One item; the page's row 3 says it is
130: # comparing.
131: scan_content() {
132:     local label="ROMS AND BIOS" rc
133:     case " $* " in
134:         *" --with-media "*) label="ROMS, BIOS, AND GAME CONTENT" ;;
135:         *" --media-only "*) label="GAME CONTENT" ;;
136:     esac
137:     rm -f "${OUT}"/scan "${OUT}"/scan.err "${OUT}"/systems "${OUT}"/content-done
138:     prepare
139:     echo ">>> unit ${label}||"
140:     echo ">>> doing compare"
141:     "$(sibling cloud_content_restore)" --scan "$@" > "${OUT}/scan" 2> "${OUT}/scan.err"; rc=$?
142:     [ "${rc}" -eq 0 ] || log "scan: --scan $* exited ${rc}: $(head -1 "${OUT}/scan.err" 2>/dev/null)"
143:     stop_on "${rc}" "--scan"
144:     "$(sibling cloud_content_restore)" --systems > "${OUT}/systems" 2>/dev/null || : > "${OUT}/systems"
145:     date +%s > "${OUT}/content-done"
146:     log "scan: content done ($(grep -c . "${OUT}/scan") rows, ${label})"
147:     exit 0
148: }
149: 
150: # 1. The folder: current, kept, superseded or the player's own; the current
151: #    folder's presence; the marker (cloud_migrate_layout --state, fork #353).
152: #    The opening scan's first item, and the whole of --folder.
153: read_folder() {
154:     local layout rc
155:     echo ">>> unit CLOUD FOLDER||"
156:     echo ">>> doing scan"
157:     layout=$(sibling cloud_migrate_layout)
158:     # A fresh install beside a fleet still on the earlier folder joins it first
159:     # (cloud_migrate_layout --join, a setting): the state below then reads the
160:     # folder the player's saves are in, and the move is offered from there
161:     # rather than CREATE IT beside them. 3 is "nothing to join"; anything else
162:     # that is not 0 is the cloud not answering, and stops the scan with its why.
163:     timeout 20 "${layout}" --join >/dev/null 2>&1; rc=$?
164:     case "${rc}" in
165:         0) log "scan: joined the fleet's earlier folder" ;;
166:         3) ;;
167:         *) stop_on "${rc}" "--join" ;;
168:     esac
169:     "${layout}" --state > "${OUT}/state" 2>/dev/null; stop_on $? "--state"
170:     # A device left on a superseded folder with nothing in it, whose current
171:     # folder another device has already made, follows the fleet here -- the
172:     # one place it does since no sync asks any more (D-CLOUD-170): the dialogs
173:     # then never ask about a folder the player has already answered for
174:     # elsewhere.
175:     if [ "$(sed -n 's/^STATE=//p' "${OUT}/state")" = superseded-empty ] \
176:        && [ "$(sed -n 's/^CURRENT_EXISTS=//p' "${OUT}/state")" = 1 ]; then
177:         timeout 20 "${layout}" --follow >/dev/null 2>&1; rc=$?
178:         case "${rc}" in
179:             0) log "scan: followed the fleet to the current layout" ;;
180:             3) ;; # The remote may have changed since the state read; read it again.
181:             *) stop_on "${rc}" "--follow" ;;
182:         esac
183:         "${layout}" --state > "${OUT}/state" 2>/dev/null; stop_on $? "--state"
184:     fi
185: }
186: 
187: case "$1" in
188:     --content) shift; scan_content "$@" ;;
189:     --folder)
190:         # The step reads state alone; the opening scan's other files are
191:         # left as they were, and are rewritten by the next opening scan.
192:         rm -f "${OUT}"/state
193:         prepare
194:         read_folder
195:         log "scan: folder done ($(sed -n 's/^STATE=//p' "${OUT}/state"))"
196:         exit 0 ;;
197:     "") ;;
198:     *) echo "usage: cloud_scan [--content [--with-media|--media-only] | --folder]" >&2; exit 2 ;;
199: esac
200: 
201: rm -f "${OUT}"/state "${OUT}"/archives "${OUT}"/settings "${OUT}"/content-location "${OUT}"/root-dirs "${OUT}"/done
202: prepare
203: date +%s > "${OUT}/started"
204: read_folder
205: 
206: # 2. The settings archives, by the device that wrote each (the label in the
207: #    name, cloud_restore's rule): this device's newest first, else the newest
208: #    overall, else none -- the row is offered or dimmed from this (D-CLOUD-162).
209: echo ">>> unit SETTINGS BACKUPS||"
210: echo ">>> doing scan"
211: settings_remote=$(conf_get SETTINGS_REMOTE) || { why "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"; exit 1; }
212: settings_remote="${settings_remote%/}"
213: # Use the restore reader's directory priority, including inherited device IDs.
214: archive_tool=$(sibling rasteratops-settings-archive)
215: [ -r "${archive_tool}" ] || { why "SOMETHING WENT WRONG"; exit 1; }
216: . "${archive_tool}"
217: select_settings_archives "${REMOTE}${settings_remote}" "$(sibling cloud_device_id)"; rc=$?
218: stop_on "${rc}" "archives listing"
219: listing="${SETTINGS_ARCHIVE_LISTING}"
220: printf '%s\n' "${listing}" | sed '/^$/d' > "${OUT}/archives"
221: label=$(device_label); osn=$(os_name); mine=""; newest=""
222: if [ -n "${label}" ]; then
223:     mine=$(grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-(${osn}|ROCKNIX|RASTERATOPS)_SETTINGS\.tar\.gz$" "${OUT}/archives" | sort | tail -1)
224: fi
225: newest=$(grep -E '^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-' "${OUT}/archives" | sort | tail -1)
226: {
227:     echo "SOURCE=${SETTINGS_ARCHIVE_SOURCE}"
228:     echo "LABEL=${label}"
229:     echo "MINE=${mine}"
230:     echo "NEWEST=${newest}"
231:     echo "COUNT=$(grep -c . "${OUT}/archives")"
232: } > "${OUT}/settings"
233: 
234: # 3. Where the content is: the configured root, the cloud root's
235: #    /Rasteratops/Content, or nowhere yet (cloud_setup --content-location,
236: #    fork #352) -- and the folders at the cloud's root, for the chooser the
237: #    page offers when nothing of ours is found. The listing itself waits for
238: #    --content, once the player has said which classes to compare.
239: echo ">>> unit GAME CONTENT||"
240: echo ">>> doing scan"
241: "$(sibling cloud_setup)" --content-location > "${OUT}/content-location" 2>/dev/null; rc=$?
242: [ "${rc}" -eq 0 ] || log "scan: --content-location exited ${rc} (reported, not fatal)"
243: rclone lsf --dirs-only "${REMOTE}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | sed 's:/$::; /^$/d' > "${OUT}/root-dirs"; rc=${PIPESTATUS[0]}
244: stop_on "${rc}" "root listing"
245: 
246: date +%s > "${OUT}/done"
247: log "scan: done ($(grep -c . "${OUT}/archives") archives, $(sed -n 's/^STATE=//p' "${OUT}/state"), content $(sed -n 's/^STATE=//p' "${OUT}/content-location"))"
248: exit 0
```


## SOURCE projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout

```text
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_migrate_layout - move a device off the original cloud folder layout.
6: #
7: # The first layout put everything under /GAMES, with the settings backups nested
8: # inside the saves folder at /GAMES/backup. Both are wrong in ways that bite:
9: #
10: #   - /GAMES is a name somebody may well have used for something else, and we
11: #     write into it as though it were ours.
12: #   - a backup folder inside the saves folder is inside the path that a `sync`
13: #     backup mirrors, so the archive is deletable by the operation meant to
14: #     protect it.
15: #
16: # The default has been /ROCKNIX/Saves and /ROCKNIX/Backups since b35c5832b1,
17: # but cloud_sync_helper only ever adds keys that are missing -- it never
18: # rewrites one already in the file -- so every device configured before that
19: # is still on the old layout and will stay there for ever unless asked.
20: #
21: # This is an offer, never automatic. Where somebody's saves live is theirs to
22: # decide, and the safe answer is always to leave it alone.
23: #
24: #   cloud_migrate_layout --check     what would move, and whether it is safe
25: #   cloud_migrate_layout --apply     do it
26: #   cloud_migrate_layout --state     one line per fact, for the interface to decide
27: #                                    what to offer (STATE=current|kept|superseded-with-files|
28: #                                    superseded-empty|own|no-remote; fork #353)
29: #   cloud_migrate_layout --keep      record that this device keeps its superseded
30: #                                    folder (LAYOUT_KEEP in the conf; asked once, D-CLOUD-160)
31: #   cloud_migrate_layout --superseded  the superseded defaults, one per line (no network)
32: #   cloud_migrate_layout --needs-step  0 when the cloud folder step has something to settle:
33: #                                    an earlier default, not kept, a remote set up (no
34: #                                    network; asked at every boot, D-CLOUD-170)
35: #   cloud_migrate_layout --follow    re-point a device on a superseded default at the
36: #                                    current layout when another device has already
37: #                                    made it (no question; D-CLOUD-160's "the other
38: #                                    devices follow"); 0 when it did, 3 when there was
39: #                                    nothing to follow
40: #   cloud_migrate_layout --join      point a device whose own folder holds no saves --
41: #                                    the current default, or a default this project once
42: #                                    shipped -- at the earlier folder that does hold them
43: #                                    (no question; a fresh install, or a carried /GAMES,
44: #                                    beside a fleet still on the earlier folder); 0 when
45: #                                    it did, 3 when there was nothing to join
46: #   cloud_migrate_layout --settle    the seeding's step (cloud_setup --seed-folders):
47: #                                    --join, else a carried default with nothing in it
48: #                                    anywhere is pointed at the current folders, which
49: #                                    the seeding then makes, as for any new cloud
50: #
51: # Only the two folders we wrote are moved. Anything else under the old folder
52: # is left exactly where it is, because it is not ours.
53: 
54: . /etc/profile 2>/dev/null
55: 
56: SYNC_CONF="/storage/.config/cloud_sync.conf"
57: NEW_SAVES="/pixelelated/Saves"
58: NEW_BACKUPS="/pixelelated/Backups"
59: NEW_CONTENT="/pixelelated/Content"
60: NEW_ROOT="${NEW_SAVES%/*}"   # the folder the tiers move into; named by the plan line below
61: # Every saves folder this project ever shipped as its default. A device whose
62: # saves folder is one of these is on a layout it never chose, so the move is
63: # offered (D-CLOUD-160); any other folder is the player's own and stays
64: # (the sibling-layout branch below). Oldest first; the current default is
65: # NEW_SAVES and is not listed.
66: SUPERSEDED_DEFAULT_SAVES=("/GAMES" "/ROCKNIX/Saves")
67: # The marker a cloud carries once it is on the current layout (#356): one
68: # line, layout=<n>, at the parent of the saves folder. Read before anything
69: # is offered; written after a move or a seeding.
70: LAYOUT_VERSION=2
71: LAYOUT_MARKER=".layout"
72: REMOTE_LAYOUT=0
73: MIGRATION_RECORD="/storage/.config/cloud-layout-migration.json"
74: MIGRATION_ACTIVE=0
75: 
76: # Which superseded default's saves folder holds files in this cloud, the
77: # configured one first, then the others newest first: into SOURCE_FOUND,
78: # empty when none does. Called directly, never inside $(...): its listings
79: # stop the run when the cloud cannot be read (list_or_stop), and inside a
80: # substitution that stop ended only the subshell -- a listing that failed
81: # read as "no folder holds the saves", a provider error taken for absence,
82: # and --state then said superseded-empty and the interface offered CREATE
83: # IT (found 2026-10-01 reading for the mixed-installation test).
84: SOURCE_FOUND=""
85: superseded_source() { # <remote> <configured saves folder>
86:     local remote="$1" saves="$2"
87:     SOURCE_FOUND=""
88:     if has_files "${remote}${saves}/"; then SOURCE_FOUND="${saves}"; return 0; fi
89:     earlier_source "${remote}" "${saves}"
90: }
91: 
92: # The newest superseded default, other than <except>, whose saves folder
93: # holds files: into SOURCE_FOUND. Newest first, because where both an
94: # upstream /GAMES and the fork's /ROCKNIX/Saves hold saves, the fork's is
95: # the one its other devices write.
96: earlier_source() { # <remote> [except]
97:     local remote="$1" except="${2:-}" i s
98:     SOURCE_FOUND=""
99:     for (( i = ${#SUPERSEDED_DEFAULT_SAVES[@]} - 1; i >= 0; i-- )); do
100:         s="${SUPERSEDED_DEFAULT_SAVES[i]}"
101:         [ -n "${except}" ] && same_folder "${s}" "${except}" && continue
102:         if has_files "${remote}${s}/"; then SOURCE_FOUND="${s}"; return 0; fi
103:     done
104:     return 1
105: }
106: 
107: # The pointers of the layout an earlier saves folder belongs to, into
108: # E_SAVES E_BACKUPS E_CONTENT: its siblings, or the nested /GAMES/backup of
109: # the first layout. Content goes with it only where this device's own was
110: # unset or the current default; a folder the player chose for ROMs stays
111: # theirs.
112: # An explicit empty CONTENT_REMOTE is the cloud root, not an unset option.
113: content_unset() { ! grep -q '^CONTENT_REMOTE=' "${SYNC_CONF}" 2>/dev/null; }
114: 
115: # A pointer-only transition may follow an empty default backup tier, never
116: # abandon its archives or replace a custom folder. Called directly: failed
117: # listings terminate the caller through list_or_stop, not a subshell.
118: backup_pointer_for() { # <remote> <configured backups> <destination default>
119:     local remote="$1" backups="$2" target="$3" known=0
120:     NEXT_BACKUPS="${backups}"
121:     case "${backups%/}" in
122:         ""|/GAMES/backup|/ROCKNIX/Backups|/pixelelated/Backups) known=1 ;;
123:     esac
124:     [ "${known}" -eq 1 ] || return 0
125:     if [ -n "${backups}" ]; then
126:         list_or_stop "${remote}${backups%/}/" --files-only -R --include '*.{zip,tar.gz}'
127:         [ -n "${LISTING}" ] && return 0
128:     fi
129:     NEXT_BACKUPS="${target}"
130: }
131: 
132: earlier_layout() { # <saves folder> <this device's content pointer>
133:     local src="$1" content="$2" parent
134:     parent="${src%/*}"; [ -n "${parent}" ] || parent="${src}"
135:     E_SAVES="${src}"
136:     if [ "${src}" = "/GAMES" ]; then E_BACKUPS="/GAMES/backup"; else E_BACKUPS="${parent}/Backups"; fi
137:     if content_unset || same_folder "${content}" "${NEW_CONTENT}"; then
138:         E_CONTENT="${parent}/Content"
139:     else
140:         E_CONTENT="${content}"
141:     fi
142: }
143: 
144: superseded_default() { # <saves folder>: 0 when it is a default this project once shipped
145:     local s
146:     for s in "${SUPERSEDED_DEFAULT_SAVES[@]}"; do same_folder "$1" "${s}" && return 0; done
147:     return 1
148: }
149: 
150: say() { echo "$@"; }
151: 
152: remote_name() {
153:     rclone listremotes 2>/dev/null | head -1
154: }
155: 
156: # The shared reader (cloud_setup's, the content scripts', D-CLOUD-149): a
157: # single-quoted or bare pointer used to come back as the whole line from
158: # `cut -d'"' -f2`, and the new folder logic then moved the pointer off the
159: # player's saves (the audit of the fixes, claude G3-D-05).
160: conf_get() { # <KEY> (the content scripts' reader, mirrored so every reader agrees, D-CLOUD-149): its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
161:     [ -f ${SYNC_CONF} ] || return 0
162:     awk -v k="$1" '
163:         { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
164:         index($0, k "=") != 1 && !other \
165:             && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
166:         index($0, k "=") == 1 {
167:             s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
168:             c = substr(s, 1, 1)
169:             if (c == "\"") {
170:                 # Inside double quotes bash reads \" \\ \$ and \` as the one
171:                 # character each (PL-015), and so does this; an unescaped $
172:                 # or backtick is an expansion this reader does not make, and
173:                 # any other backslash is refused as conf_valid refuses it.
174:                 n = length(s); i = 2; closed = 0
175:                 while (i <= n) {
176:                     d = substr(s, i, 1)
177:                     if (d == "\"") { closed = 1; break }
178:                     if (d == "\\") {
179:                         e = substr(s, i + 1, 1)
180:                         if (e == "\"" || e == "\\" || e == "$" || e == "`") { v = v e; i += 2; continue }
181:                         ok = 0
182:                         why = (e == "") ? "a value continued onto the next line, which this reader does not follow" \
183:                                         : "a backslash inside double quotes that is not one of the escapes bash reads there"
184:                         break
185:                     }
186:                     if (d == "$" || d == "`") { ok = 0; why = "a $ or a backtick inside double quotes"; break }
187:                     v = v d; i++
188:                 }
189:                 if (ok && !closed) { ok = 0; why = "a double-quoted value that does not close on its line" }
190:                 if (ok) r = substr(s, i + 1)
191:             } else if (c == "'"'"'") {
192:                 j = index(substr(s, 2), c)
193:                 if (j) { v = substr(s, 2, j - 1); r = substr(s, j + 2) } else { ok = 0; why = "a single-quoted value that does not close on its line" }
194:             } else {
195:                 match(s, /^[A-Za-z0-9_.\/:@%+,=-]*/); v = substr(s, 1, RLENGTH); r = substr(s, RLENGTH + 1)
196:             }
197:             if (ok && r !~ /^([ \t]+(#.*)?)?$/) { ok = 0; why = "something after the value that is not a # comment" }
198:             if (!found) { found = 1; first = v; firstok = ok; firstwhy = "line " NR ": " why }
199:         }
200:         END {
201:             if (cntrl) { print "line " cntrl ": a control character other than a tab"; exit 2 }
202:             if (other) { print "line " other ": " k " set in a form this reader does not read"; exit 2 }
203:             if (found && !firstok) { print firstwhy; exit 2 }
204:             if (found) print first
205:         }
206:     ' ${SYNC_CONF}
207: }
208: conf_value() {
209:     local v
210:     v=$(conf_get "$1"); case $? in 2) echo "cloud_migrate_layout: ${SYNC_CONF}: ${v}" >&2; return 2 ;; esac
211:     printf '%s\n' "${v}"
212: }
213: 
214: # One folder, one spelling (the audit of the fix round, PL-001). The guards
215: # in main that decide whether a tier has already landed compared the conf's
216: # raw string with /ROCKNIX/Saves, so SAVES_REMOTE="/ROCKNIX/Saves/" -- a
217: # trailing slash, from a hand edit or an older setup -- read as the old
218: # layout: --check offered the move, and --apply copied the saves onto
219: # themselves (rclone's copy of a folder onto itself exits 0 and changes
220: # nothing), checked them clean against themselves, and deleted every file
221: # it had listed; the content folder went the same way. So a pointer is read
222: # as the folder it names:
223: #
224: #   clean_path     runs of / as one, no "." component, no trailing /; a
225: #                  leading / kept only if it had one, so the path handed to
226: #                  rclone is the one the other scripts use; it fails on a
227: #                  ".." component, which rclone resolves by rules of its
228: #                  own, so main leaves such a layout alone;
229: #   folder_key     that from the root, in one case when the cloud folds case
230: #                  (Dropbox, OneDrive) or cannot say whether it does;
231: #   same_folder    two keys equal;
232: #   inside_folder  the first strictly under the second, and rel_inside the
233: #                  part below, in the first one's own spelling.
234: CASE_INSENSITIVE=1
235: clean_path() { # <path>
236:     local p="$1" lead="" out="" part
237:     local -a parts=()
238:     case "${p}" in /*) lead="/" ;; esac
239:     IFS=/ read -r -a parts <<< "${p}"
240:     for part in "${parts[@]}"; do
241:         case "${part}" in
242:             ""|.) ;;
243:             ..) return 1 ;;
244:             *) out="${out:+${out}/}${part}" ;;
245:         esac
246:     done
247:     printf '%s%s' "${lead}" "${out}"
248: }
249: folder_abs() { # <cleaned path>: the same folder from the root, in its own spelling
250:     printf '/%s' "${1#/}"
251: }
252: folder_key() { # <path>
253:     local p
254:     p=$(clean_path "$1") || p="$1"
255:     p="/${p#/}"
256:     [ "${CASE_INSENSITIVE}" = 1 ] && p="${p,,}"
257:     printf '%s' "${p}"
258: }
259: same_folder() { # <path> <path>
260:     [ "$(folder_key "$1")" = "$(folder_key "$2")" ]
261: }
262: inside_folder() { # <path> <path>: the first strictly under the second
263:     local ka kb
264:     ka=$(folder_key "$1"); kb=$(folder_key "$2")
265:     [ "${ka}" != "${kb}" ] || return 1
266:     [ "${kb}" = "/" ] && return 0
267:     case "${ka}" in "${kb}"/*) return 0 ;; esac
268:     return 1
269: }
270: rel_inside() { # <path> <path>: the part of the first below the second (inside_folder holds)
271:     local a b
272:     a=$(clean_path "$1") || a="$1"; b=$(clean_path "$2") || b="$2"
273:     a=$(folder_abs "${a}"); b=$(folder_abs "${b}")
274:     if [ "${b}" = "/" ]; then printf '%s' "${a#/}"; else printf '%s' "${a:$(( ${#b} + 1 ))}"; fi
275: }
276: 
277: # A listing's bound (#143): three low-level retries, the value every other
278: # cloud script lists with.
279: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
280: # Every other call's (#308 claude F-CS-23): RCLONE_NET_OPTS from the conf,
281: # or the shipped value when the conf has none -- the bound the transfers
282: # carry everywhere else, where this script ran on rclone's own defaults
283: # (a 60 s connect, a 5 min idle, ten low-level retries, three runs: the
284: # behaviour #101 removed from every other script). Set in main.
285: RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
286: RCLONE_NET_OPTS_ARRAY=()
287: # What a verification compares by: size and hash where the remote keeps
288: # hashes, the bytes themselves where it keeps none (WebDAV, SFTP, SMB,
289: # FTP), where `rclone check` would otherwise compare sizes alone. Set in
290: # main from `rclone backend features`; a remote whose features cannot be
291: # read is checked by content too.
292: CHECK_OPTS=()
293: 
294: # One cloud transfer at a time (F-CS-23): the lock every other cloud script
295: # takes, for --apply only -- the check reads and writes nothing, as the
296: # match preview does. Without it a startup or game-exit sync could write
297: # into the folder this was moving. The same descriptor discipline as the
298: # others: the body runs with fd 9 closed, so nothing it starts holds the
299: # lock. Exit 75 is the skip EmulationStation names.
300: CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
301: take_cloud_lock() {
302:     local tries=0
303:     exec 9>"${CLOUD_SYNC_LOCK}"
304:     while ! flock -n 9; do
305:         if [ "${tries}" -ge 4 ]; then
306:             echo "Skipped: another cloud sync is already running. Try again when it's done."
307:             exit 75
308:         fi
309:         tries=$((tries + 1))
310:         sleep 0.25
311:     done
312: }
313: 
314: # A cloud that did not answer is not an empty cloud (audit #307 PL-027).
315: # Every presence test here used to be `[ -n "$(rclone lsf ... 2>/dev/null |
316: # head -1)" ]`, which discards rclone's exit: a listing that failed read as
317: # a folder with nothing in it, and --apply went on to rewrite the pointers
318: # with nothing copied. A listing now ends one of three ways: it listed
319: # (LISTING holds what it said, perhaps nothing), the folder is not there
320: # (rclone's 3/4, or the nearest listable parent lacks it -- #142's walk,
321: # for a server whose "missing" rclone does not map to 3), or the cloud
322: # could not be read -- and then the run stops where it is, saying so, with
323: # every pointer that has not already landed left where it was.
324: unreadable() { # <path> <rclone exit>
325:     local rc="$2"
326:     [ "${rc}" -gt 0 ] 2>/dev/null || rc=1
327:     say "Couldn't read your cloud, so nothing more was changed. Try again when you're online."
328:     [ "${MODE}" = "--apply" ] && echo ">>> why YOUR CLOUD STOPPED ANSWERING"
329:     logger -t cloud_migrate_layout "could not list $1 (rclone exit $2); stopped" 2>/dev/null
330:     exit "${rc}"
331: }
332: 
333: # Is this remote path missing, rather than unreadable? cloud_content_restore's
334: # walk, verbatim: up to the nearest level that lists; a level that lists and
335: # lacks the next name is a path not created yet (0), one that holds it means
336: # the failure was something else (1), and a root that will not list is
337: # broken (1).
338: absent_not_broken() {
339:     local path="${1%/}" remote rel name parent listing
340:     remote="${path%%:*}:"; rel="${path#*:}"; rel="${rel#/}"
341:     while [ -n "${rel}" ]; do
342:         name="${rel##*/}"; parent="${rel%/*}"
343:         [ "${parent}" = "${rel}" ] && parent=""
344:         if listing=$(rclone lsf --dirs-only "${remote}/${parent:+${parent}/}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); then
345:             printf '%s\n' "${listing}" | grep -qFx -- "${name}/" && return 1
346:             return 0
347:         fi
348:         [ -n "${parent}" ] || return 1
349:         rel="${parent}"
350:     done
351:     return 1
352: }
353: 
354: # LISTING=what rclone lsf [args] <path> lists; nothing for a folder that is
355: # not there; the run stops for one that cannot be read. Never called inside
356: # $(...), so the stop is the script's.
357: LISTING=""
358: list_or_stop() { # <path> [lsf args...]
359:     local path="$1" rc
360:     shift
361:     LISTING=$(rclone lsf "$@" "${path}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); rc=$?
362:     case "${rc}" in
363:         0) return 0 ;;
364:         3|4) LISTING=""; return 0 ;;
365:     esac
366:     if absent_not_broken "${path}"; then
367:         LISTING=""
368:         return 0
369:     fi
370:     unreadable "${path}" "${rc}"
371: }
372: 
373: # Does a remote path exist and hold anything?
374: has_entries() {
375:     list_or_stop "$1"
376:     [ -n "${LISTING}" ]
377: }
378: 
379: # Does it hold actual files, ignoring the backup folder underneath it?
380: #
381: # Not the same question as "is it empty". The original layout has the backups
382: # nested inside the saves folder, so a saves folder with nothing in it but
383: # that subdirectory still lists an entry -- and reading that as "the saves are
384: # here" would move the backups into the middle of the saves.
385: #
386: # The same exclusions are what the saves relocation carries (audit #307
387: # PL-025): a test that looks past backup/ and Backups/ and a copy that then
388: # moves them is how the original layout's settings archives landed in
389: # Saves/backup/. Anchored at the folder's root, where the nested layout put
390: # them; the caller adds the tiers nested deeper. Every argument is passed
391: # as it is given -- the exclusion used to travel as one unquoted word
392: # (${extra}), which the shell split and glob-expanded against the working
393: # directory (#308 claude F-CS-23).
394: SAVES_EXCLUDES=(--exclude '/backup/**' --exclude '/Backups/**')
395: has_files() { # <path> [more lsf arguments...]
396:     local path="$1"
397:     shift
398:     # The setup note is not a save and must not outrank another root's data.
399:     list_or_stop "${path}" --files-only -R "${SAVES_EXCLUDES[@]}" --exclude '/README.txt' "$@"
400:     [ -n "${LISTING}" ]
401: }
402: 
403: # Does a remote path exist?
404: #
405: # NOT `rclone lsjson --stat`, which is what this used to be. On bucket-based
406: # remotes (S3, B2, Minio) stat synthesises a directory entry for *any* path --
407: # verified against Minio on rclone 1.60 and 1.74, where
408: # "utterly-bogus-never-created" reports success with IsDir true. So it can
409: # never report absence there, and every caller that branched on it took the
410: # "exists" path unconditionally.
411: #
412: # A listing can report absence. Two questions, because a directory can be real
413: # without holding files: does it contain anything, or does its parent list it
414: # (which is what an --s3-directory-markers marker object produces)?
415: exists() {
416:     list_or_stop "$1"
417:     [ -n "${LISTING}" ] && return 0
418:     local parent name
419:     parent="${1%/}"; name="${parent##*/}"; parent="${parent%/*}"
420:     [ -n "${name}" ] || return 1
421:     list_or_stop "${parent}/" --dirs-only
422:     printf '%s\n' "${LISTING}" | grep -qxF -- "${name}/"
423: }
424: 
425: # Did a `rclone check` find the two sides the same? Only when it says so
426: # both ways: its exit status is 0, and its count of differences is exactly
427: # zero. The count alone was the test here, as a substring -- and "10
428: # differences found" contains "0 differences found", so a check that found
429: # ten changed files let the pointer move and the old folder go, and a new
430: # folder holding ten other versions of the same names read as a partial
431: # copy to resume into (the audit of the fixes to #307, G-A-01).
432: check_clean() { # <rclone check's exit status> <its output>
433:     [ "$1" -eq 0 ] 2>/dev/null || return 1
434:     printf '%s\n' "$2" | grep -qE '(^|[^0-9])0 differences found'
435: }
436: 
437: # Relocate a folder by copy, verify, delete -- never `rclone move`.
438: #
439: # move deletes as it goes, so an interruption -- a handheld dropping off wifi is
440: # the normal case, not the exception -- leaves the library split across two
441: # paths with no record of which files went where (#57, upgrade-and-install.md).
442: # Copy first: a second run finds the copied files already present and skips
443: # them. Verify by content with `rclone check`, reading its whole output rather
444: # than one line of it (engineering-practices.md: rclone prints "N matching
445: # files" last, and a check against the last line matched nothing). Only a
446: # verified pass removes the source; a failed one leaves both sides intact and
447: # says so.
448: #
449: # Pipelines are avoided on purpose: `rclone ... | tail` reports tail's status,
450: # which is how a short backup once announced itself a success.
451: #
452: # The tier's pointer is written the moment its copy is verified, before its
453: # source is removed (audit #307 PL-026). Both pointers used to be written
454: # after both moves, so a run that moved the saves and was cut before the
455: # end left SAVES_REMOTE at the emptied folder -- a device syncing to a
456: # folder with nothing in it -- and the next run, finding the new folder
457: # already there, refused it. Now a cut run leaves each tier either where it
458: # was (not yet verified) or where it went (pointer written), and the next
459: # run moves only what has not landed.
460: #
461: # Any filter arguments after the fourth are the tier's own (PL-025): they
462: # decide which files are the tier's, so a folder nested in the source that
463: # belongs to another tier -- the original layout's backup/ and Content/
464: # inside the saves folder -- is neither moved with it nor deleted with it.
465: #
466: # And the source loses only what was copied and verified (audit #307
467: # PL-053). The files are listed once, by those filters, and the list is the
468: # whole job: the copy, the check and the deletion each take exactly it
469: # (--files-from-raw, which keeps a name's spaces), and the empty folders go
470: # after. The old folder used to be purged after a point-in-time check, so a
471: # save another device wrote into it between the check and the purge was
472: # lost; now it is not on the list, stays where it was written, and is
473: # still there for that device's own migration.
474: #
475: # 0 when the tier moved; 1 when its copy or check failed, the old folder
476: # whole; 2 when its pointer could not be written, which set_pointer has
477: # said, the old folder whole too.
478: # The second device's move, onto a current folder the fleet already made
479: # (RELOCATE_MERGE=1, D-CLOUD-168): the first device's move made the folder
480: # and removed the old one, and a device still on the old build then wrote
481: # its saves back under the old name (the mixed-installation test, step 3),
482: # so when it upgrades its old folder holds files and the new one exists.
483: # Refusing would strand it on NOT NOW for ever; merging is the sync's own
484: # rule -- the newer copy of each file wins -- made non-destructive: every
485: # version that differs between the two folders is set aside first, under
486: # the same <saves>-replaced/<stamp> shelf the backup keeps its conflict
487: # losers on, then the copy runs with --update and the new folder's own
488: # overwritten copies go to that shelf too (--backup-dir), and the old
489: # folder is removed only once every name it held is present in the new
490: # one. Nothing in the new folder is deleted, and nothing is lost: each
491: # byte that was in the cloud is in the new folder or on the shelf.
492: RELOCATE_MERGE=0
493: merge_shelf() { # <dst>: the set-aside beside the destination, one folder per run
494:     echo "${1%/}-replaced/$(date +%Y_%m_%d-%H%M%S)-move"
495: }
496: 
497: relocate() { # <src> <dst> <what> <pointer key> [filter arguments...]
498:     local src="$1" dst="$2" what="$3" key="$4" out list
499:     shift 4
500:     local -a filt=("$@")
501:     # One folder under two spellings is not a move (PL-001): copied onto
502:     # itself it checks clean, and the delete after it removes every file
503:     # it listed. Refused here whatever the caller compared.
504:     if same_folder "${src#*:}" "${dst#*:}"; then
505:         say "REFUSING: ${src} and ${dst} are the same folder, so nothing was copied or removed."
506:         logger -t cloud_migrate_layout "relocate: ${src} and ${dst} are one folder; refused" 2>/dev/null
507:         return 1
508:     fi
509:     # A destination inside the source -- a saves folder at /ROCKNIX moving
510:     # to /ROCKNIX/Saves -- is never listed as the source's own: a run cut
511:     # after its copy left part of it there, and the resume moved that copy
512:     # into /ROCKNIX/Saves/Saves (PL-001, found with the spelling cases).
513:     if inside_folder "${dst#*:}" "${src#*:}"; then
514:         filt+=(--exclude "/$(rel_inside "${dst#*:}" "${src#*:}")/**")
515:     fi
516:     list_or_stop "${src}" -R --files-only "${filt[@]}"
517:     if [ -z "${LISTING}" ]; then
518:         [ -z "${key}" ] || set_pointer "${key}" "${dst#*:}" || return 2
519:         return 0
520:     fi
521:     list=$(mktemp /tmp/cloud_migrate_layout.XXXXXX) || { say "Couldn't make a working file on this device; nothing was moved."; return 1; }
522:     printf '%s\n' "${LISTING}" > "${list}"
523:     if [ "${RELOCATE_MERGE}" = 1 ]; then
524:         merge_into "${src}" "${dst}" "${what}" "${key}" "${list}"
525:         return $?
526:     fi
527:     say "Copying ${what}..."
528:     # Under --apply the move runs on a page (GuiCloudTransfer, fork #353):
529:     # ">>> doing" names the step for its row 3, and the copy's own progress
530:     # goes to stdout for the page's counters (COPYING n OF m), as every
531:     # transfer's does; the check and the delete print nothing it reads.
532:     local copy_rc
533:     if [ "${MODE}" = "--apply" ]; then
534:         echo ">>> doing copy"
535:         rclone copy "${src}" "${dst}" --files-from-raw "${list}" --create-empty-src-dirs=false --progress --stats 2s \
536:             "${RCLONE_NET_OPTS_ARRAY[@]}" 2>&1 | tee "${list}.out"; copy_rc=${PIPESTATUS[0]}
537:         out=$(cat "${list}.out" 2>/dev/null); rm -f "${list}.out"
538:     else
539:         out=$(rclone copy "${src}" "${dst}" --files-from-raw "${list}" --create-empty-src-dirs=false "${RCLONE_NET_OPTS_ARRAY[@]}" 2>&1); copy_rc=$?
540:     fi
541:     if [ "${copy_rc}" -ne 0 ]; then
542:         printf '%s\n' "${out}" | tail -3
543:         # A copy that stopped part-way has put some files in the new
544:         # folder; only the old one is as it was (G-A-12).
545:         say "Couldn't finish copying ${what}. Nothing was removed from the old folder; some files may already be in the new one."
546:         rm -f "${list}"
547:         return 1
548:     fi
549:     say "Verifying ${what}..."
550:     [ "${MODE}" = "--apply" ] && echo ">>> doing verify"
551:     out=$(rclone check "${src}" "${dst}" --files-from-raw "${list}" --one-way "${CHECK_OPTS[@]}" "${RCLONE_NET_OPTS_ARRAY[@]}" 2>&1)
552:     if ! check_clean $? "${out}"; then
553:         printf '%s\n' "${out}" | grep -iE "differ|missing|error" | head -3
554:         say "The copy of ${what} didn't match, so nothing was removed from the old folder."
555:         rm -f "${list}"
556:         return 1
557:     fi
558:     # The source goes only once the pointer has landed (G-A-02): a pointer
559:     # that could not be written leaves the device on the old folder, so the
560:     # old folder must still hold everything -- the next run finds the copy
561:     # already there and resumes.
562:     # A folder with no pointer of its own (the set-aside beside the saves,
563:     # named from SAVES_REMOTE by the scripts) has nothing to record here.
564:     if [ -n "${key}" ] && ! set_pointer "${key}" "${dst#*:}"; then
565:         rm -f "${list}"
566:         return 2
567:     fi
568:     say "Removing the old ${what} folder..."
569:     [ "${MODE}" = "--apply" ] && echo ">>> doing remove"
570:     if ! rclone delete "${src}" --files-from-raw "${list}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1; then
571:         say "The verified copy is in the new folder, but the old files couldn't be removed. Try again to finish."
572:         rm -f "${list}"
573:         return 1
574:     fi
575:     rclone rmdirs "${src}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1 || :
576:     rm -f "${list}"
577:     return 0
578: }
579: 
580: # relocate's merge half (RELOCATE_MERGE, above): shelf, copy --update, verify
581: # by presence, remove. <list> is the source's own file listing.
582: merge_into() { # <src> <dst> <what> <pointer key> <list>
583:     local src="$1" dst="$2" what="$3" key="$4" list="$5" shelf differ missing out rc
584:     shelf="${dst%%:*}:$(merge_shelf "${dst#*:}")"
585:     differ=$(mktemp /tmp/cloud_migrate_layout.XXXXXX) || { rm -f "${list}"; return 1; }
586:     missing="${differ}.missing"
587:     say "Merging ${what} into ${dst}: the newer copy of each file is kept, the other set aside under ${shelf#*:}."
588:     # 1. What differs between the two folders is shelved from the source
589:     #    first; the destination's own copies the update replaces follow
590:     #    through --backup-dir. A check that cannot run shelves nothing and
591:     #    stops here (guards fail closed).
592:     rclone check "${src}" "${dst}" --one-way --files-from-raw "${list}" --differ "${differ}" "${CHECK_OPTS[@]}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1; rc=$?
593:     case "${rc}" in 0|1) ;; *)
594:         say "Couldn't compare ${what} with the new folder, so nothing was merged."
595:         rm -f "${list}" "${differ}" "${missing}"; return 1 ;;
596:     esac
597:     if [ -s "${differ}" ]; then
598:         [ "${MODE}" = "--apply" ] && echo ">>> doing copy"
599:         if ! out=$(rclone copy "${src}" "${shelf}" --files-from-raw "${differ}" "${RCLONE_NET_OPTS_ARRAY[@]}" 2>&1); then
600:             printf '%s\n' "${out}" | tail -3
601:             say "Couldn't set aside the ${what} that differ, so nothing was merged."
602:             rm -f "${list}" "${differ}" "${missing}"; return 1
603:         fi
604:         say "$(grep -c . "${differ}") ${what} file(s) differ between the folders; the old folder's copies are on the shelf."
605:     fi
606:     # 2. The copy, newer wins; a file the new folder had a newer copy of is
607:     #    left as it is, and one it replaces goes to the shelf.
608:     say "Copying ${what}..."
609:     local copy_rc
610:     if [ "${MODE}" = "--apply" ]; then
611:         echo ">>> doing copy"
612:         rclone copy "${src}" "${dst}" --files-from-raw "${list}" --update --backup-dir "${shelf}" --create-empty-src-dirs=false --progress --stats 2s \
613:             "${RCLONE_NET_OPTS_ARRAY[@]}" 2>&1 | tee "${list}.out"; copy_rc=${PIPESTATUS[0]}
614:         out=$(cat "${list}.out" 2>/dev/null); rm -f "${list}.out"
615:     else
616:         out=$(rclone copy "${src}" "${dst}" --files-from-raw "${list}" --update --backup-dir "${shelf}" --create-empty-src-dirs=false "${RCLONE_NET_OPTS_ARRAY[@]}" 2>&1); copy_rc=$?
617:     fi
618:     if [ "${copy_rc}" -ne 0 ]; then
619:         printf '%s\n' "${out}" | tail -3
620:         say "Couldn't finish merging ${what}. Nothing was removed from the old folder."
621:         rm -f "${list}" "${differ}" "${missing}"; return 1
622:     fi
623:     # 3. Verified by presence: every name the old folder held is in the new
624:     #    one. Content may differ where the new folder's copy was newer, and
625:     #    that copy is the one kept, so a content check is not the test here.
626:     say "Verifying ${what}..."
627:     [ "${MODE}" = "--apply" ] && echo ">>> doing verify"
628:     : > "${missing}"
629:     rclone check "${src}" "${dst}" --one-way --files-from-raw "${list}" --missing-on-dst "${missing}" "${CHECK_OPTS[@]}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1; rc=$?
630:     if [ "${rc}" -gt 1 ] || [ -s "${missing}" ]; then
631:         say "Not every ${what} file reached the new folder ($(grep -c . "${missing}" 2>/dev/null) missing), so nothing was removed from the old folder."
632:         rm -f "${list}" "${differ}" "${missing}"; return 1
633:     fi
634:     if [ -n "${key}" ] && ! set_pointer "${key}" "${dst#*:}"; then
635:         rm -f "${list}" "${differ}" "${missing}"; return 2
636:     fi
637:     say "Removing the old ${what} folder..."
638:     [ "${MODE}" = "--apply" ] && echo ">>> doing remove"
639:     if ! rclone delete "${src}" --files-from-raw "${list}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1; then
640:         say "The merged files are in the new folder, but the old files couldn't be removed. Try again to finish."
641:         rm -f "${list}" "${differ}" "${missing}"
642:         return 1
643:     fi
644:     rclone rmdirs "${src}" "${RCLONE_NET_OPTS_ARRAY[@]}" >/dev/null 2>&1 || :
645:     rm -f "${list}" "${differ}" "${missing}"
646:     return 0
647: }
648: 
649: # Point a key of the conf at a tier's new folder: the line rewritten in
650: # place, or added when the conf has none -- and then read back. A write
651: # that did not land (a full or read-only /storage, a path sed's
652: # replacement would mangle) is a failure the caller must stop on, before
653: # anything is removed (the audit of the fixes to #307, G-A-02): its result
654: # used to go unread, and relocate deleted the old folder after it either
655: # way, leaving the device pointed at a folder the run had just emptied.
656: # 0 when the conf now says <remote path>, 1 when it does not.
657: set_pointer() { # <key> <remote path>
658:     if grep -q "^$1=" "${SYNC_CONF}" 2>/dev/null; then
659:         sed -i "s|^$1=.*|$1=\"$2\"|" "${SYNC_CONF}" 2>/dev/null
660:     else
661:         printf '%s="%s"\n' "$1" "$2" >> "${SYNC_CONF}" 2>/dev/null
662:     fi
663:     if [ "$(conf_value "$1")" != "$2" ]; then
664:         say "Couldn't save the new folder in this device's settings. It still uses the old one, and nothing was removed from it."
665:         [ "${MODE}" = "--apply" ] && echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED"
666:         logger -t cloud_migrate_layout "could not write $1 to ${SYNC_CONF}; stopped before removing anything" 2>/dev/null
667:         return 1
668:     fi
669:     say "Now using ${2:-the root of your cloud} for your $(tier_words "$1")."
670: }
671: 
672: # A tier as the player knows it (es-player-text.md: the four tiers), for
673: # the tidy page's lines -- which named the config key (audit of the fixes,
674: # claude G-A-11).
675: tier_words() { # <pointer key>
676:     case "$1" in
677:         SAVES_REMOTE) echo "saves" ;;
678:         SETTINGS_REMOTE) echo "settings backups" ;;
679:         CONTENT_REMOTE) echo "ROMs, BIOS, and game content" ;;
680:         *) echo "files" ;;
681:     esac
682: }
683: 
684: # Is an existing destination a partial copy of this source, and nothing else?
685: #
686: # The refusals below exist so two devices' libraries are never merged. But a
687: # copy interrupted half-way also leaves a destination that exists, and the same
688: # refusal would then block the resume forever. The two cases differ in one
689: # checkable way: a partial copy holds nothing that did not come from the
690: # source. The reverse one-way check asks exactly that -- every file in dst is
691: # present and identical in src -- so a foreign file in dst fails it and the
692: # refusal stands.
693: resumable() {
694:     local src="$1" dst="$2" out
695:     out=$(rclone check "${dst}" "${src}" --one-way "${CHECK_OPTS[@]}" "${RCLONE_NET_OPTS_ARRAY[@]}" 2>&1)
696:     check_clean $? "${out}"
697: }
698: 
699: # What cloud_sync_helper would have derived CONTENT_REMOTE to be for a given
700: # SAVES_REMOTE. The helper deliberately derives it rather than taking the shipped
701: # default, so that ROMs and saves stay in one namespace -- its own comment
702: # calls a split "worse than either layout alone".
703: #
704: # That is exactly what this script used to produce: it moved saves and backups
705: # to /ROCKNIX and left CONTENT_REMOTE behind, so a migrated device looked for its
706: # ROMs under a /GAMES that no longer had anything in it. Matching against the
707: # derived value is how we tell our own pointer from one the owner chose --
708: # theirs is left alone.
709: derived_content() {
710:     local sync="$1" parent
711:     parent=$(dirname "${sync}")
712:     [ "${parent}" = "/" ] && parent="${sync}"
713:     echo "${parent%/}/Content"
714: }
715: 
716: # RC2 could finish its saves/backups moves before /GAMES/Content; run101
717: # could finish both pointers before its discarded/content tiers (#391).
718: # Only these exact earlier defaults are inherited derived content. A custom
719: # path ending in /Content is still the player's independent choice.
720: historical_content() {
721:     same_folder "$1" /GAMES/Content || same_folder "$1" /ROCKNIX/Content
722: }
723: 
724: moving_content() { # <saves source> <content pointer>
725:     [ -n "$2" ] && ! same_folder "$2" "${NEW_CONTENT}" || return 1
726:     same_folder "$2" "$(derived_content "$(folder_abs "$1")")" && return 0
727:     { superseded_default "$1" || same_folder "$1" "${NEW_SAVES}"; } && historical_content "$2"
728: }
729: 
730: # Move content to the current namespace if it is safe to, and repoint the
731: # config. Never merges into an existing destination -- that is the same
732: # interruptible half-migrated state the saves move refuses.
733: migrate_content() {
734:     local remote="$1" content="$2" mode="$3"
735: 
736:     if has_entries "${remote}${content}/"; then
737:         if exists "${remote}${NEW_CONTENT}" && ! resumable "${remote}${content}" "${remote}${NEW_CONTENT}"; then
738:             if fleet_made "${remote}"; then
739:                 RELOCATE_MERGE=1   # the fleet's folder: the second device's content merges (D-CLOUD-168)
740:             else
741:                 say "REFUSING: ${remote}${NEW_CONTENT} already exists, and ${remote}${content}"
742:                 say "holds files. Nothing moved and the config is unchanged -- merging two"
743:                 say "content folders is not something to do without being asked."
744:                 [ "${mode}" = "--apply" ] && echo ">>> why THE NEW FOLDER ALREADY HAS FILES IN IT"
745:                 return 4
746:             fi
747:         fi
748:         say "Would copy, verify, then remove  ${remote}${content}  ->  ${remote}${NEW_CONTENT}"
749:         if [ "${mode}" != "--apply" ]; then
750:             echo ">>> plan content ${NEW_ROOT}"
751:             say "Nothing has been changed. Run with --apply to do it."
752:             return 0
753:         fi
754:         local rrc=0
755:         relocate "${remote}${content}" "${remote}${NEW_CONTENT}" "content" CONTENT_REMOTE || rrc=$?
756:         if [ "${rrc}" -ne 0 ]; then
757:             # 2 is a pointer that could not be written, which has said so.
758:             if [ "${rrc}" -ne 2 ]; then
759:                 say "The config is unchanged."
760:                 echo ">>> why SOME FILES DIDN'T FINISH"
761:             fi
762:             return 5
763:         fi
764:         say "Content is now at ${remote}${NEW_CONTENT}."
765:         return 0
766:     else
767:         say "Nothing is stored at ${remote}${content}, so only the setting changes."
768:         if [ "${mode}" != "--apply" ]; then
769:             echo ">>> plan none ${NEW_ROOT}"
770:             say "Nothing has been changed. Run with --apply to do it."
771:             return 0
772:         fi
773:     fi
774: 
775:     set_pointer CONTENT_REMOTE "${NEW_CONTENT}" || return 5
776:     say "Content is now at ${remote}${NEW_CONTENT}."
777:     return 0
778: }
779: 
780: # --- the layout as facts (#353, #356) -----------------------------------
781: #
782: # One line per fact and nothing the interface has to parse out of prose:
783: #
784: #   STATE=current               the saves folder is the current default
785: #   STATE=kept                  a superseded default this device chose to keep (--keep)
786: #   STATE=superseded-with-files a default this project once shipped, holding saves:
787: #                               the move is offered (D-CLOUD-160)
788: #   STATE=superseded-empty      such a default with nothing in it, or absent:
789: #                               the creation of the current layout is offered (D-CLOUD-161)
790: #   STATE=own                   a folder the player chose; nothing is offered
791: #   CURRENT_EXISTS=0|1          whether the current default's saves folder lists
792: #   MARKER=layout=<n> | -       the cloud's marker, when one is there
793: layout_state() { # <remote> <saves> <backups> <content>
794:     local remote="$1" saves="$2" backups="$3" content="$4" state keep cur=0 marker old_replaced=""
795:     if [ -e "${MIGRATION_RECORD}" ]; then
796:         migration_record_load "${remote}" || return $?
797:         printf 'STATE=migration-pending\nSOURCE=%s\nCURRENT=%s\n' "${saves}" "${NEW_SAVES}"
798:         return 0
799:     fi
800:     keep=$(conf_value LAYOUT_KEEP) || return 2
801:     echo "SAVES=${saves}"
802:     echo "BACKUPS=${backups}"
803:     echo "CONTENT=${content}"
804:     echo "CURRENT=${NEW_SAVES}"
805:     # The folder this device is configured for is one witness; the cloud is
806:     # the other. A device upgraded from stock carries /GAMES in its conf
807:     # while its saves sit in /ROCKNIX/Saves, made by its sibling on the
808:     # fork's earlier build (the Retroid Pocket Nova, 2026-10-01): read from
809:     # the conf alone it is "superseded, empty" and would be offered a fresh
810:     # /pixelelated beside its real saves. So every default this project
811:     # once shipped is looked at, and the one holding files is the source
812:     # the move is offered from (SOURCE=), the configured one or not.
813:     local source=""
814:     if same_folder "${saves}" "${NEW_SAVES}"; then
815:         state=current
816:         # Older builds wrote no recovery record. Their current primary
817:         # pointers do not prove the derived content or discarded shelf moved.
818:         # This is a folder-page read, never an extra probe on a direct sync.
819:         if same_folder "${backups}" "${NEW_BACKUPS}"; then
820:             local earlier
821:             if historical_content "${content}"; then
822:                 state=migration-pending
823:             else
824:                 for earlier in "${SUPERSEDED_DEFAULT_SAVES[@]}"; do
825:                     if has_entries "${remote}${earlier}-replaced/"; then state=migration-pending; break; fi
826:                 done
827:             fi
828:         fi
829:     elif [ -n "${keep}" ] && same_folder "${saves}" "${keep}"; then
830:         state=kept
831:     elif superseded_default "${saves}"; then
832:         superseded_source "${remote}" "${saves}"; source="${SOURCE_FOUND}"
833:         if [ -n "${source}" ]; then state=superseded-with-files; else state=superseded-empty; fi
834:     else
835:         state=own
836:     fi
837:     echo "SOURCE=${source:--}"
838:     exists "${remote}${NEW_SAVES}" && cur=1
839:     echo "CURRENT_EXISTS=${cur}"
840:     marker=$(rclone cat "${remote}${NEW_SAVES%/*}/${LAYOUT_MARKER}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | head -1 | tr -cd 'a-z0-9=')
841:     echo "MARKER=${marker:--}"
842:     echo "STATE=${state}"
843:     return 0
844: }
845: 
846: # KEEP USING <folder>: asked once (D-CLOUD-160). The conf remembers the
847: # folder kept, so --state reads "kept" until the folder changes.
848: layout_keep() { # <saves>
849:     set_pointer LAYOUT_KEEP "$1" || return 1
850:     say "Keeping ${1}; the move will not be offered again for this folder."
851:     logger -t cloud_migrate_layout "layout kept at $1 by request" 2>/dev/null
852:     return 0
853: }
854: 
855: # "Your other devices will follow": a device on a superseded default whose
856: # current-default folder already exists in the cloud -- another device made
857: # the move -- is re-pointed with no question and one line in the journal.
858: # Nothing is copied or removed here; the folders are already where they
859: # belong. 0 when the device now points at the current layout, 3 when there
860: # was nothing to follow, 1 when the conf could not be written.
861: layout_follow() { # <remote> <saves> <backups> <content>
862:     local remote="$1" saves="$2" backups="$3" content="$4" keep
863:     same_folder "${saves}" "${NEW_SAVES}" && return 3
864:     superseded_default "${saves}" || return 3
865:     keep=$(conf_value LAYOUT_KEEP) || return 2
866:     [ -n "${keep}" ] && same_folder "${saves}" "${keep}" && return 3
867:     # One listing for the usual answer, "no device has moved yet": the
868:     # current folder's parent, which names Saves/ once it exists (exists()
869:     # would list the folder and then its parent, two rclone starts).
870:     list_or_stop "${remote}${NEW_SAVES%/*}/" --dirs-only
871:     printf '%s\n' "${LISTING}" | grep -qxF -- "${NEW_SAVES##*/}/" || return 3
872:     # A device whose old folder still holds files is not followed: they
873:     # would be stranded in a folder nothing reads once the pointer moves
874:     # (the futro's pre-mortem, 2026-10-01). The move is offered instead,
875:     # which copies, verifies and only then removes.
876:     has_files "${remote}${saves}/" && return 3
877:     backup_pointer_for "${remote}" "${backups}" "${NEW_BACKUPS}"
878:     set_pointer SAVES_REMOTE "${NEW_SAVES}" || return 1
879:     set_pointer SETTINGS_REMOTE "${NEXT_BACKUPS}" || return 1
880:     # Content follows only where it was derived from the old folder or
881:     # never set; a folder the player chose for ROMs stays theirs.
882:     if content_unset || same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")" \
883:        || same_folder "${content}" "${saves%/}/Content"; then
884:         set_pointer CONTENT_REMOTE "${NEW_CONTENT}" || return 1
885:     fi
886:     say "Followed: this device now uses ${remote}${NEW_SAVES}, which another device already made."
887:     logger -t cloud_migrate_layout "followed the fleet from ${saves} to ${NEW_SAVES}" 2>/dev/null
888:     return 0
889: }
890: 
891: # A fresh install beside a fleet still on the earlier folder: this device
892: # is on the current default, the current saves folder holds no saves (it
893: # is not there, or only the seeding's folders and README are), and a
894: # folder this project once shipped as its default does hold them. Without
895: # this the device was offered CREATE IT beside the player's saves, and saw
896: # none of them on its first restore -- the mixed-installation test's fresh
897: # device (D-CLOUD-158). It is pointed at the earlier folder's layout -- a
898: # setting, nothing copied -- so it reads and writes where the saves are,
899: # and is then offered the move as every device on that folder is
900: # (D-CLOUD-160). 0 when it joined, 3 when there was nothing to join, 1
901: # when the conf could not be written.
902: layout_join() { # <remote> <saves> <content>
903:     local remote="$1" saves="$2" content="$3" keep
904:     if same_folder "${saves}" "${NEW_SAVES}"; then
905:         has_files "${remote}${NEW_SAVES}/" --exclude '/README.txt' && return 3
906:     elif superseded_default "${saves}"; then
907:         # The Nova's shape (2026-09-30): a carried /GAMES with nothing in it,
908:         # the saves in /ROCKNIX/Saves beside it. Joined, the move is offered
909:         # from the folder that holds them and KEEP USING keeps that folder;
910:         # left on /GAMES, KEEP USING /ROCKNIX recorded /GAMES.
911:         keep=$(conf_value LAYOUT_KEEP) || return 2
912:         [ -n "${keep}" ] && same_folder "${saves}" "${keep}" && return 3
913:         has_files "${remote}${saves}/" && return 3
914:     else
915:         return 3
916:     fi
917:     earlier_source "${remote}" "${saves}" || return 3
918:     earlier_layout "${SOURCE_FOUND}" "${content}"
919:     local backups
920:     backups=$(conf_value SETTINGS_REMOTE) || return 2
921:     backup_pointer_for "${remote}" "${backups}" "${E_BACKUPS}"
922:     set_pointer SAVES_REMOTE "${E_SAVES}" || return 1
923:     set_pointer SETTINGS_REMOTE "${NEXT_BACKUPS}" || return 1
924:     set_pointer CONTENT_REMOTE "${E_CONTENT}" || return 1
925:     say "Joined: this device now uses ${remote}${E_SAVES}, where your saves already are."
926:     logger -t cloud_migrate_layout "joined the fleet at ${E_SAVES}: no saves in ${NEW_SAVES}" 2>/dev/null
927:     return 0
928: }
929: 
930: # The wizard's seeding step (cloud_setup --seed-folders): join the earlier
931: # folder that holds the saves; else a device still on a default this
932: # project once shipped, with nothing in it and nothing anywhere, is on no
933: # folder at all (D-CLOUD-161) and is pointed at the current folders, which
934: # the seeding then makes and lists, as it does for any new cloud. Seeding
935: # the carried /GAMES itself put a README there, which every later check
936: # read as saves: the move was offered from /GAMES and left the player's
937: # saves in /ROCKNIX (2026-10-01). 0 when the device was pointed somewhere,
938: # 3 when its folder stands.
939: layout_settle() { # <remote> <saves> <backups> <content>
940:     local remote="$1" saves="$2" backups="$3" content="$4" rc keep
941:     layout_join "${remote}" "${saves}" "${content}"; rc=$?
942:     [ "${rc}" -ne 3 ] && return "${rc}"
943:     superseded_default "${saves}" || return 3
944:     keep=$(conf_value LAYOUT_KEEP) || return 2
945:     [ -n "${keep}" ] && same_folder "${saves}" "${keep}" && return 3
946:     has_files "${remote}${saves}/" && return 3
947:     backup_pointer_for "${remote}" "${backups}" "${NEW_BACKUPS}"
948:     set_pointer SAVES_REMOTE "${NEW_SAVES}" || return 1
949:     set_pointer SETTINGS_REMOTE "${NEXT_BACKUPS}" || return 1
950:     if content_unset || same_folder "${content}" "$(derived_content "$(folder_abs "${saves}")")" \
951:        || same_folder "${content}" "${saves%/}/Content"; then
952:         set_pointer CONTENT_REMOTE "${NEW_CONTENT}" || return 1
953:     fi
954:     say "Your cloud had nothing in ${remote}${saves}; this device now uses ${remote}${NEW_SAVES}."
955:     logger -t cloud_migrate_layout "settled a carried ${saves} with nothing in it on ${NEW_SAVES}" 2>/dev/null
956:     return 0
957: }
958: 
959: # Did another device of ours make the current layout? The marker at the
960: # folder's parent says so (write_marker, after a move or a seeding). A
961: # current folder with no marker is somebody's own folder of the same name,
962: # which the refusals below still protect.
963: fleet_made() { # <remote>
964:     [ "${REMOTE_LAYOUT}" = "${LAYOUT_VERSION}" ]
965: }
966: 
967: # A marker is a version, not merely a prefix. Validate its complete bytes;
968: # shell substitution would silently discard NULs and trailing newlines. A
969: # failed read is not absence if the parent still lists the marker.
970: read_marker() { # <remote>
971:     local tmp rc version
972:     REMOTE_LAYOUT=0
973:     tmp=$(mktemp /tmp/cloud_layout_marker.XXXXXX) || return 5
974:     rclone cat "${1}${NEW_ROOT}/${LAYOUT_MARKER}" "${RCLONE_LIST_OPTS[@]}" > "${tmp}" 2>/dev/null; rc=$?
975:     if [ "${rc}" -ne 0 ]; then
976:         rm -f "${tmp}"
977:         list_or_stop "${1}${NEW_ROOT}/" --files-only
978:         if printf '%s\n' "${LISTING}" | grep -qFx -- "${LAYOUT_MARKER}"; then
979:             unreadable "${1}${NEW_ROOT}/${LAYOUT_MARKER}" "${rc}"
980:         fi
981:         return 0
982:     fi
983:     for version in 1 2; do
984:         if printf 'layout=%s\n' "${version}" | cmp -s - "${tmp}"; then
985:             REMOTE_LAYOUT="${version}"
986:             rm -f "${tmp}"
987:             return 0
988:         fi
989:     done
990:     rm -f "${tmp}"
991:     say "This cloud folder uses a layout this version can't read. No further changes were made. Check for a newer system version before trying again."
992:     [ "${MODE}" = "--apply" ] && echo ">>> why YOUR CLOUD FOLDER COULDN'T BE READ"
993:     logger -t cloud_migrate_layout "unsupported or malformed layout marker; refused" 2>/dev/null
994:     return 4
995: }
996: 
997: write_marker() { # <remote>
998:     # Another device may have changed the marker while the tiers moved.
999:     read_marker "$1" || return $?
1000:     if printf 'layout=%s\n' "${LAYOUT_VERSION}" | rclone rcat "${1}${NEW_SAVES%/*}/${LAYOUT_MARKER}" "${RCLONE_NET_OPTS_ARRAY[@]}" 2>/dev/null; then
1001:         read_marker "$1" || return $?
1002:         [ "${REMOTE_LAYOUT}" = "${LAYOUT_VERSION}" ] || return 5
1003:         return 0
1004:     fi
1005:     say "Your files moved, but the cloud folder setup didn't finish. Try the move again to finish it."
1006:     [ "${MODE}" = "--apply" ] && echo ">>> why SOME FILES DIDN'T FINISH"
1007:     logger -t cloud_migrate_layout "could not write ${LAYOUT_MARKER} at ${1}${NEW_SAVES%/*}" 2>/dev/null
1008:     return 5
1009: }
1010: 
1011: # Local recovery state keeps the sources after their live pointers advance.
1012: # It is never sourced as shell and never grants permission to merge a foreign
1013: # destination. Each retry still verifies the actual cloud bytes. A record is
1014: # bound to the remote configuration and the original/current pointer choices.
1015: remote_fingerprint() {
1016:     # rclone refreshes OAuth tokens during ordinary transfers. Bind the
1017:     # configured provider/root, not that routinely changing credential.
1018:     local config
1019:     config=$(sed '/^[[:space:]]*token[[:space:]]*=/d' /storage/.config/rclone/rclone.conf) || return 1
1020:     printf '%s\n' "${config}" | sha256sum
1021: }
1022: 
1023: migration_record_save() {
1024:     migration_record_write "$@" && return 0
1025:     say "Couldn't save the cloud move's progress on this device. Try again when storage is available."
1026:     [ "${MODE}" = "--apply" ] && echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED"
1027:     return 5
1028: }
1029: 
1030: migration_record_write() { # <stage>; consumes the calling step's local paths
1031:     local stage="$1" tmp fingerprint
1032:     fingerprint=$(remote_fingerprint) || return 5
1033:     fingerprint="${fingerprint%% *}"
1034:     tmp=$(mktemp "${MIGRATION_RECORD}.XXXXXX" 2>/dev/null) || return 5
1035:     if [ "${MIGRATION_ACTIVE}" = 1 ]; then
1036:         jq --arg stage "${stage}" '.stage=$stage' "${MIGRATION_RECORD}" > "${tmp}"
1037:     else
1038:         jq -n --arg remote "${remote}" --arg fingerprint "${fingerprint}" \
1039:             --arg saves "${saves}" --arg backups "${backups}" --arg content "${content}" \
1040:             --arg discarded "${old_replaced}" \
1041:             --arg cs "$(conf_value SAVES_REMOTE)" --arg cb "$(conf_value SETTINGS_REMOTE)" \
1042:             --arg cc "$(conf_value CONTENT_REMOTE)" --arg stage "${stage}" \
1043:             '{schema:1,step:1,from:1,to:2,remote:$remote,fingerprint:$fingerprint,
1044:               source:{saves:$saves,backups:$backups,content:$content,discarded:$discarded},
1045:               configured:{saves:$cs,backups:$cb,content:$cc},stage:$stage}' > "${tmp}"
1046:     fi
1047:     if [ "$?" -ne 0 ] || ! sync || ! mv -f "${tmp}" "${MIGRATION_RECORD}" || ! sync; then
1048:         rm -f "${tmp}"
1049:         return 5
1050:     fi
1051:     MIGRATION_ACTIVE=1
1052:     logger -t cloud_migrate_layout "migration step=1 from=1 to=2 stage=${stage}" 2>/dev/null
1053:     return 0
1054: }
1055: 
1056: migration_record_load() { # <remote>; restores the calling step's source paths
1057:     [ -e "${MIGRATION_RECORD}" ] || return 0
1058:     local fingerprint key live initial target value
1059:     fingerprint=$(remote_fingerprint) || return 5
1060:     fingerprint="${fingerprint%% *}"
1061:     if ! jq -e --arg remote "$1" --arg fingerprint "${fingerprint}" '
1062:         .schema==1 and .step==1 and .from==1 and .to==2 and
1063:         .remote==$remote and .fingerprint==$fingerprint and
1064:         ([.source.saves,.source.backups,.source.content,
1065:           .configured.saves,.configured.backups,.configured.content] |
1066:           all(.[]; type=="string" and (explode | all(.[]; .>=32)))) and
1067:         ((.source | has("discarded") | not) or
1068:           (.source.discarded | type=="string" and (explode | all(.[]; .>=32))))
1069:         ' "${MIGRATION_RECORD}" >/dev/null 2>&1; then
1070:         say "The previous cloud move couldn't be read safely. Nothing more was changed."
1071:         return 5
1072:     fi
1073:     for key in saves backups content; do
1074:         case "${key}" in
1075:             saves) live=$(conf_value SAVES_REMOTE); target="${NEW_SAVES}" ;;
1076:             backups) live=$(conf_value SETTINGS_REMOTE); target="${NEW_BACKUPS}" ;;
1077:             content) live=$(conf_value CONTENT_REMOTE); target="${NEW_CONTENT}" ;;
1078:         esac
1079:         initial=$(jq -r --arg k "${key}" '.configured[$k]' "${MIGRATION_RECORD}") || return 5
1080:         if ! same_folder "${live}" "${initial}" && ! same_folder "${live}" "${target}"; then
1081:             say "Your cloud folder choices changed during the move. Nothing more was changed."
1082:             return 5
1083:         fi
1084:         value=$(jq -r --arg k "${key}" '.source[$k]' "${MIGRATION_RECORD}") || return 5
1085:         value=$(clean_path "${value}") || return 5
1086:         printf -v "${key}" '%s' "${value}"
1087:     done
1088:     # Optional in schema1: records written before #391 derive this shelf
1089:     # from their retained saves source. New records keep it independently,
1090:     # so recovering an old shelf never reselects a live saves folder.
1091:     value=$(jq -r '.source.discarded // (.source.saves | rtrimstr("/") + "-replaced")' "${MIGRATION_RECORD}") || return 5
1092:     old_replaced=$(clean_path "${value}") || return 5
1093:     MIGRATION_ACTIVE=1
1094:     logger -t cloud_migrate_layout "migration step=1 from=1 to=2 resume" 2>/dev/null
1095:     return 0
1096: }
1097: 
1098: MODE="--check"
1099: main() {
1100:     # Every pointer this tool reads must be readable by the shared grammar
1101:     # before anything is compared or moved (the audit of the fixes, claude
1102:     # G3-D-05): a value the reader cannot read ends the run with its why,
1103:     # as cloud_setup ends, never as an empty pointer that reads as a folder.
1104:     local _k _v
1105:     for _k in SAVESPATH SETTINGS_BACKUPS SAVES_REMOTE SETTINGS_REMOTE CONTENT_REMOTE RCLONE_NET_OPTS; do
1106:         _v=$(conf_get "${_k}"); case $? in 2) echo "Your cloud sync settings couldn't be read (${SYNC_CONF}: ${_v})." >&2; exit 2 ;; esac
1107:     done
1108:     local mode="${1:---check}"
1109:     local remote saves backups content old_root
1110:     MODE="${mode}"
1111: 
1112:     remote=$(remote_name)
1113:     if [ -z "${remote}" ]; then
1114:         say "No cloud remote is configured; nothing to migrate."
1115:         return 1
1116:     fi
1117: 
1118:     # The cloud answers before anything is asked of it (PL-027): a remote
1119:     # that does not list at its root is unreadable, and nothing below --
1120:     # a presence test, a pointer -- is reached.
1121:     # Not for --follow, which an exit sync on a device still on an earlier
1122:     # folder runs before every write: its own first listing stops the run on
1123:     # a cloud that cannot be read, and the probe and the features query were
1124:     # two of the four rclone starts it cost each time (time to play,
1125:     # 2026-10-01). Nothing it writes depends on either.
1126:     local probe_rc
1127:     if [ "${mode}" != "--follow" ]; then
1128:         rclone lsd "${remote}" "${RCLONE_LIST_OPTS[@]}" >/dev/null 2>&1; probe_rc=$?
1129:         [ "${probe_rc}" -eq 0 ] || unreadable "${remote}" "${probe_rc}"
1130:     fi
1131: 
1132:     local net_opts
1133:     net_opts=$(conf_value RCLONE_NET_OPTS | tr -s ' ' | sed 's/^ //; s/ $//')
1134:     [ -n "${net_opts}" ] || net_opts="${RCLONE_NET_OPTS_FALLBACK}"
1135:     read -r -a RCLONE_NET_OPTS_ARRAY <<< "${net_opts}"
1136:     # The query creates the remote, a round trip on most backends, so it
1137:     # carries the listing bound like every other call here (audit of the
1138:     # fixes, G-A-11/G-A-10); one that fails or times out reads as "no
1139:     # hashes", the safe side.
1140:     local features=""
1141:     [ "${mode}" != "--follow" ] && features=$(rclone backend features "${remote}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | tr -d ' \t\n')
1142:     case "${features}" in *'"Hashes":["'*) ;; *) CHECK_OPTS=(--download) ;; esac
1143:     # And whether it keeps case apart (PL-001): only a cloud that says so
1144:     # holds /rocknix/saves and /ROCKNIX/Saves as two folders. One that folds
1145:     # case, or whose features cannot be read, holds them as one, and a
1146:     # pointer spelled either way is the new folder, so nothing moves -- the
1147:     # safe side, since the other side deletes a folder copied onto itself.
1148:     case "${features}" in *'"CaseInsensitive":false'*) CASE_INSENSITIVE=0 ;; *) CASE_INSENSITIVE=1 ;; esac
1149: 
1150:     saves=$(conf_value SAVES_REMOTE)
1151:     backups=$(conf_value SETTINGS_REMOTE)
1152: 
1153:     content=$(conf_value CONTENT_REMOTE)
1154: 
1155:     # Each pointer as the folder it names (PL-001): cleaned for the paths
1156:     # below and compared by folder_key, never as a string. A ".." cannot be
1157:     # read as one folder without the cloud's own rules -- rclone resolves
1158:     # /ROCKNIX/Old/../Saves to /ROCKNIX/Saves -- so a layout holding one is
1159:     # left exactly as it is.
1160:     local ptr cleaned
1161:     for ptr in saves backups content; do
1162:         if ! cleaned=$(clean_path "${!ptr}"); then
1163:             say "REFUSING: a folder in this device's cloud settings has .. in it, so it can't be told which folder it means. Nothing was changed."
1164:             [ "${mode}" = "--apply" ] && echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
1165:             logger -t cloud_migrate_layout "a pointer has a .. component; nothing done" 2>/dev/null
1166:             return 4
1167:         fi
1168:         printf -v "${ptr}" '%s' "${cleaned}"
1169:     done
1170: 
1171:     # All default-layout transitions share the version boundary, including
1172:     # seeding through --settle. A custom layout elsewhere is independent.
1173:     if superseded_default "${saves}" || same_folder "${saves}" "${NEW_SAVES}"; then
1174:         read_marker "${remote}" || return $?
1175:     fi
1176: 
1177:     # A layout the owner chose is current too. CHANGE CLOUD FOLDER writes the
1178:     # settings and content folders as SIBLINGS of the saves folder -- the
1179:     # parent's Backups and Content, or the folder's own when it sits at the
1180:     # root -- and a device on /Custom/Saves, /Custom/Backups, /Custom/Content
1181:     # has nothing to migrate. Until 2026-09-11 only the /ROCKNIX names counted
1182:     # as current, so this check offered to move a deliberately chosen layout
1183:     # back to the default one (#74). The nested first layout, backups INSIDE
1184:     # the saves folder, is the only shape this tool exists to move.
1185:     if [ -e "${MIGRATION_RECORD}" ]; then
1186:         case "${mode}" in
1187:             --join|--follow) return 3 ;; # The explicit retry owns the remaining move.
1188:             --settle|--keep|--write-marker)
1189:                 say "The cloud folder move hasn't finished. Try the move again to finish it."
1190:                 return 5 ;;
1191:         esac
1192:     fi
1193:     case "${mode}" in
1194:         --state)  layout_state "${remote}" "${saves}" "${backups}" "${content}"; return $? ;;
1195:         --keep)   layout_keep "${saves}"; return $? ;;
1196:         --follow) layout_follow "${remote}" "${saves}" "${backups}" "${content}"; return $? ;;
1197:         --join)   layout_join "${remote}" "${saves}" "${content}"; return $? ;;
1198:         --settle) layout_settle "${remote}" "${saves}" "${backups}" "${content}"; return $? ;;
1199:         --write-marker)
1200:             # Seeding must not declare an unfinished local move complete.
1201:             [ ! -e "${MIGRATION_RECORD}" ] || return 5
1202:             same_folder "${saves}" "${NEW_SAVES}" || return 3
1203:             write_marker "${remote}"; return $? ;;
1204:     esac
1205: 
1206:     # Step 1 is the supported predecessor (unmarked/layout 1) to layout 2.
1207:     # A layout-2 fleet may still have an older device's files to move, so
1208:     # marker 2 does not skip that device's step. Later versions must add an
1209:     # explicit dispatcher entry; read_marker refuses them in this build.
1210:     case "${REMOTE_LAYOUT}" in
1211:         0|1|2) migration_step_1 "${remote}" "${saves}" "${backups}" "${content}" "${mode}" ;;
1212:         *) return 4 ;;
1213:     esac
1214: }
1215: 
1216: migration_step_1() {
1217:     local remote="$1" saves="$2" backups="$3" content="$4" mode="$5" old_replaced=""
1218:     migration_record_load "${remote}" || return $?
1219: 
1220:     local sabs sib_parent
1221:     sabs=$(folder_abs "${saves}")
1222:     sib_parent="${sabs%/*}"; [ -n "${sib_parent}" ] || sib_parent="${sabs}"
1223:     # A superseded default is not a layout of the player's own, however
1224:     # sibling-shaped: /ROCKNIX/Saves beside /ROCKNIX/Backups is the fork's
1225:     # earlier default and is offered the move (D-CLOUD-160).
1226:     if ! superseded_default "${saves}" \
1227:        && ! same_folder "${saves}" "${NEW_SAVES}" && same_folder "${backups}" "${sib_parent}/Backups"; then
1228:         if content_unset || same_folder "${content}" "${sib_parent}/Content"; then
1229:             say "Already on a sibling layout of your own (${saves}, ${backups}); nothing to move."
1230:             return 3
1231:         fi
1232:     fi
1233: 
1234:     if [ "${MIGRATION_ACTIVE}" = 0 ] && same_folder "${saves}" "${NEW_SAVES}" \
1235:        && same_folder "${backups}" "${NEW_BACKUPS}"; then
1236:         # The live primary pointers are authoritative. Another device may
1237:         # still write old saves/backups: only the retained content pointer
1238:         # and an owned discarded shelf are eligible for this recovery.
1239:         local earlier
1240:         for earlier in "${SUPERSEDED_DEFAULT_SAVES[@]}"; do
1241:             if has_entries "${remote}${earlier}-replaced/"; then
1242:                 old_replaced="${earlier}-replaced"; break
1243:             fi
1244:         done
1245:         if [ -z "${old_replaced}" ] && ! moving_content "${saves}" "${content}"; then
1246:             # An older build may have stopped just before publication. An
1247:             # explicit apply finishes that marker without inventing a move
1248:             # or rewriting equivalent pointer spellings (PL-001).
1249:             if [ "${mode}" = "--apply" ] && [ "${REMOTE_LAYOUT}" != "${LAYOUT_VERSION}" ]; then
1250:                 write_marker "${remote}" || return $?
1251:             fi
1252:             say "Already on the current layout (${NEW_SAVES}, ${NEW_BACKUPS})."
1253:             return 3
1254:         fi
1255:     fi
1256: 
1257:     # The move starts from the folder that holds the saves. A device whose
1258:     # configured folder is a superseded default with nothing in it, while
1259:     # another superseded default's folder holds files (the Nova: /GAMES in
1260:     # the conf, /ROCKNIX/Saves in the cloud), is first pointed at that
1261:     # folder -- a setting, nothing copied -- and then moved from it like
1262:     # any other. Backups and content are taken as that layout's siblings
1263:     # (or the nested /GAMES/backup for the first layout).
1264:     if [ "${MIGRATION_ACTIVE}" = 0 ] && superseded_default "${saves}" && ! has_files "${remote}${saves}/"; then
1265:         local src
1266:         superseded_source "${remote}" "${saves}"; src="${SOURCE_FOUND}"
1267:         if [ -n "${src}" ] && ! same_folder "${src}" "${saves}"; then
1268:             say "Your saves are in ${remote}${src}, not in ${remote}${saves} as this device was set; moving from there."
1269:             local src_parent="${src%/*}"; [ -n "${src_parent}" ] || src_parent="${src}"
1270:             local src_backups="${src_parent}/Backups"
1271:             [ "${src}" = "/GAMES" ] && src_backups="/GAMES/backup"
1272:             backup_pointer_for "${remote}" "${backups}" "${src_backups}"
1273:             # Select sources here; publish pointers only after verified
1274:             # copies, with the recovery record already retained below.
1275:             saves="${src}"
1276:             backups="${NEXT_BACKUPS}"
1277:             content_unset && content="${src_parent}/Content"
1278:             sabs=$(folder_abs "${saves}")
1279:             sib_parent="${sabs%/*}"; [ -n "${sib_parent}" ] || sib_parent="${sabs}"
1280:         fi
1281:     fi
1282:     [ -n "${old_replaced}" ] || old_replaced="${sabs%/}-replaced"
1283: 
1284:     say "This device stores:"
1285:     say "  saves    ${remote}${saves}"
1286:     say "  backups  ${remote}${backups}"
1287:     say ""
1288:     say "The current layout is:"
1289:     say "  saves    ${remote}${NEW_SAVES}"
1290:     say "  backups  ${remote}${NEW_BACKUPS}"
1291:     say ""
1292: 
1293:     # Where the saves actually are. Under the original layout SAVES_REMOTE was the
1294:     # folder itself; a device whose owner has already tidied them into a
1295:     # subfolder is the more useful case to handle, since that is what somebody
1296:     # does after losing files to a mirror.
1297:     local saves_src="${saves}" nested
1298:     # "at the root" must not count the saves subfolder, or a recursive listing
1299:     # finds the files inside it and concludes they were at the root all along
1300:     # -- which would move the whole folder, backups included, into Saves. Nor
1301:     # the other tiers nested in it: the content folder derived beside the
1302:     # saves (/GAMES/Content) holds files, and read as "saves at the root" it
1303:     # sent a tidied saves/ subfolder into Saves/saves/ (found by F-CS-23's
1304:     # case, a gap in the PL-025 commit).
1305:     local -a root_nested=()
1306:     for nested in "${backups}" "${content}"; do
1307:         [ -n "${nested}" ] && inside_folder "${nested}" "${saves}" \
1308:             && root_nested+=(--exclude "/$(rel_inside "${nested}" "${saves}")/**")
1309:     done
1310:     if ! has_files "${remote}${saves}/" --exclude '/saves/**' "${root_nested[@]}" \
1311:        && has_files "${remote}${saves}/saves/"; then
1312:         saves_src="${saves%/}/saves"
1313:         say "Saves are in ${remote}${saves_src}, not at the root."
1314:     fi
1315:     # The other tiers nested inside the saves source ride with neither its
1316:     # presence test nor its move (PL-025): the settings folder of the
1317:     # original layout (/GAMES/backup) and the content folder derived beside
1318:     # the saves (/GAMES/Content) each move to a place of their own.
1319:     for nested in "${backups}" "${content}"; do
1320:         [ -n "${nested}" ] && inside_folder "${nested}" "${saves_src}" \
1321:             && SAVES_EXCLUDES+=(--exclude "/$(rel_inside "${nested}" "${saves_src}")/**")
1322:     done
1323: 
1324:     # Refuse to move onto something already there. A move into an existing
1325:     # directory is done file by file, which is exactly the interruptible,
1326:     # half-migrated state worth avoiding -- and it could merge two devices'
1327:     # libraries without anyone asking for that.
1328:     #
1329:     # Each tier is judged against its own source (PL-026): the backups
1330:     # destination used to be compared with the saves source, so a copy of
1331:     # the backups cut half-way could never be resumed. A tier whose pointer
1332:     # already names the new folder has landed, and is left alone; one whose
1333:     # source holds nothing has nothing to merge, and only its pointer moves --
1334:     # the state an earlier build left when it was cut after its moves and
1335:     # before its pointers.
1336:     # Unless the fleet made the new folder (its marker, D-CLOUD-168): then
1337:     # this is the second device's move and the tiers merge (merge_into).
1338:     local blocked=0 merging=0
1339:     if ! same_folder "${backups}" "${NEW_BACKUPS}" && has_entries "${remote}${backups}/" \
1340:        && exists "${remote}${NEW_BACKUPS}" \
1341:        && ! resumable "${remote}${backups}" "${remote}${NEW_BACKUPS}"; then
1342:         if fleet_made "${remote}"; then merging=1; else
1343:             say "REFUSING: ${remote}${NEW_BACKUPS} already exists."
1344:             blocked=1
1345:         fi
1346:     fi
1347:     if ! same_folder "${saves}" "${NEW_SAVES}" && has_files "${remote}${saves_src}/" \
1348:        && exists "${remote}${NEW_SAVES}" \
1349:        && ! resumable "${remote}${saves_src}" "${remote}${NEW_SAVES}"; then
1350:         if fleet_made "${remote}"; then merging=1; else
1351:             say "REFUSING: ${remote}${NEW_SAVES} already exists."
1352:             blocked=1
1353:         fi
1354:     fi
1355:     if ! same_folder "${old_replaced}" "${NEW_SAVES}-replaced" && has_entries "${remote}${old_replaced}/" \
1356:        && exists "${remote}${NEW_SAVES}-replaced" \
1357:        && ! resumable "${remote}${old_replaced}" "${remote}${NEW_SAVES}-replaced"; then
1358:         if fleet_made "${remote}"; then merging=1; else
1359:             say "REFUSING: ${remote}${NEW_SAVES}-replaced already exists."
1360:             blocked=1
1361:         fi
1362:     fi
1363:     if [ "${blocked}" = "1" ]; then
1364:         [ "${mode}" = "--apply" ] && echo ">>> why THE NEW FOLDER ALREADY HAS FILES IN IT"
1365:         return 4
1366:     fi
1367:     if [ "${merging}" = 1 ]; then
1368:         say "Another device has already moved to ${remote}${NEW_SAVES%/*}: this one's folders merge into it, the newer copy of each file kept and the other set aside."
1369:         RELOCATE_MERGE=1
1370:     fi
1371: 
1372:     say "Would move, server-side, leaving anything else where it is:"
1373:     local plan=""
1374:     if ! same_folder "${backups}" "${NEW_BACKUPS}" && has_entries "${remote}${backups}/"; then
1375:         say "  ${remote}${backups}  ->  ${remote}${NEW_BACKUPS}"; plan="${plan:+${plan},}backups"
1376:     fi
1377:     if ! same_folder "${saves}" "${NEW_SAVES}" && has_files "${remote}${saves_src}/"; then
1378:         say "  ${remote}${saves_src}  ->  ${remote}${NEW_SAVES}"; plan="${plan:+${plan},}saves"
1379:     fi
1380:     # The set-aside of conflict losers beside the saves folder
1381:     # (<saves>-replaced, cloud_backup's) is ours and travels with the saves
1382:     # (D-CLOUD-165): to a player the change is a renamed shelf, not a new
1383:     # one, and nothing of ours stays under the old name.
1384:     if ! same_folder "${old_replaced}" "${NEW_SAVES}-replaced" && has_entries "${remote}${old_replaced}/"; then
1385:         say "  ${remote}${old_replaced}  ->  ${remote}${NEW_SAVES}-replaced"; plan="${plan:+${plan},}discarded"
1386:     fi
1387:     # The content folder derived beside the saves moves too (the same test
1388:     # the items count makes below). It was moved and never listed here, so
1389:     # the hub's preview said less than --apply did (2026-10-01).
1390:     if moving_content "${saves}" "${content}" && has_entries "${remote}${content}/"; then
1391:         say "  ${remote}${content}  ->  ${remote}${NEW_CONTENT}"; plan="${plan:+${plan},}content"
1392:     fi
1393: 
1394:     if [ "${mode}" != "--apply" ]; then
1395:         # One line the interface reads (the TIDY UP row's description says
1396:         # what moves and where): the tiers holding files, in move order --
1397:         # backups, saves, discarded, content -- or none when only a setting
1398:         # would change. The row named /ROCKNIX on a build whose folder is
1399:         # /pixelelated until this line existed (2026-10-01).
1400:         echo ">>> plan ${plan:-none} ${NEW_ROOT}"
1401:         say ""
1402:         say "Nothing has been changed. Run with --apply to do it."
1403:         return 0
1404:     fi
1405: 
1406:     say ""
1407:     migration_record_save begin || return $?
1408:     # What moves, counted before anything does, so the page reads ITEM 1 OF n
1409:     # from the first announcement (D-UI-026); each tier announces itself in
1410:     # the page's own words as its move begins. A tier with nothing stored
1411:     # moves only its pointer and is not an item.
1412:     local items=0 item=0
1413:     ! same_folder "${backups}" "${NEW_BACKUPS}" && has_entries "${remote}${backups}/" && items=$((items + 1))
1414:     ! same_folder "${saves}" "${NEW_SAVES}" && has_files "${remote}${saves_src}/" && items=$((items + 1))
1415:     ! same_folder "${old_replaced}" "${NEW_SAVES}-replaced" && has_entries "${remote}${old_replaced}/" && items=$((items + 1))
1416:     moving_content "${saves}" "${content}" && has_entries "${remote}${content}/" && items=$((items + 1))
1417:     announce() { item=$((item + 1)); echo ">>> unit $1|${item}|${items}"; }
1418:     # The backups first (PL-025). In the original layout they sit inside the
1419:     # saves folder; moved first, they are out of it before the saves move
1420:     # looks, as well as excluded from it. Each pointer is written as its
1421:     # tier lands (PL-026), only once the data is where it will point: a
1422:     # config updated first, then a move that failed, is a device looking at
1423:     # an empty folder and reporting that it has no saves. A tier with
1424:     # nothing stored only has its pointer moved.
1425:     if ! same_folder "${backups}" "${NEW_BACKUPS}"; then
1426:         if has_entries "${remote}${backups}/"; then
1427:             announce "SETTINGS BACKUPS"
1428:             if ! relocate "${remote}${backups}" "${remote}${NEW_BACKUPS}" "backups" SETTINGS_REMOTE; then
1429:                 say "Nothing else attempted."
1430:                 return 5
1431:             fi
1432:         else
1433:             set_pointer SETTINGS_REMOTE "${NEW_BACKUPS}" || return 5
1434:         fi
1435:     fi
1436: 
1437:     migration_record_save backups || return $?
1438:     local moved_saves=0
1439:     if ! same_folder "${saves}" "${NEW_SAVES}"; then
1440:         if has_files "${remote}${saves_src}/"; then
1441:             announce "SAVES"
1442:             relocate "${remote}${saves_src}" "${remote}${NEW_SAVES}" "saves" SAVES_REMOTE "${SAVES_EXCLUDES[@]}" || return 5
1443:             moved_saves=1
1444:         else
1445:             set_pointer SAVES_REMOTE "${NEW_SAVES}" || return 5
1446:         fi
1447:         # Only a missing content choice follows automatically. An explicit
1448:         # empty value selects the cloud root and must survive the move (#380).
1449:         if content_unset; then
1450:             set_pointer CONTENT_REMOTE "${NEW_CONTENT}" || return 5
1451:             content="${NEW_CONTENT}"
1452:         fi
1453:     fi
1454:     migration_record_save saves || return $?
1455:     if ! same_folder "${old_replaced}" "${NEW_SAVES}-replaced" && has_entries "${remote}${old_replaced}/"; then
1456:         announce "DISCARDED SAVES"
1457:         if ! relocate "${remote}${old_replaced}" "${remote}${NEW_SAVES}-replaced" "discarded saves" ""; then
1458:             say "Your discarded saves didn't finish moving; they are still at ${remote}${old_replaced}. Try again."
1459:             return 5
1460:         fi
1461:     fi
1462: 
1463:     migration_record_save discarded || return $?
1464:     # ROMs move with the saves they belong to, when the pointer is one we
1465:     # derived. A CONTENT_REMOTE the owner set themselves is theirs, and stays.
1466:     # Its result is the run's (audit #307 PL-071): a content move that was
1467:     # refused or failed used to be followed by "Done." and exit 0, so the
1468:     # card said the tidy had completed while the ROMs stayed behind.
1469:     local content_rc=0
1470:     # Compared as folders, and never onto itself (PL-001): a saves folder at
1471:     # /ROCKNIX derives /ROCKNIX/Content, the new folder itself, which the
1472:     # string compare sent through the move and so onto itself.
1473:     if moving_content "${saves}" "${content}"; then
1474:         has_entries "${remote}${content}/" && announce "ROMS, BIOS, AND GAME CONTENT"
1475:         migrate_content "${remote}" "${content}" "${mode}" || content_rc=$?
1476:     elif [ -n "${content}" ] && ! same_folder "${content}" "${NEW_CONTENT}"; then
1477:         say "Leaving CONTENT_REMOTE at ${content} -- it is not a path this migration set."
1478:     fi
1479: 
1480:     say ""
1481:     if [ "${content_rc}" -ne 0 ]; then
1482:         say "Saves are at ${remote}${NEW_SAVES} and backups at ${remote}${NEW_BACKUPS}, but your ROMs and BIOS files didn't move. Try again."
1483:         return "${content_rc}"
1484:     fi
1485:     migration_record_save content || return $?
1486:     write_marker "${remote}" || return $?
1487:     migration_record_save complete || return $?
1488:     rm -f "${MIGRATION_RECORD}" || return 5
1489:     sync || return 5
1490:     say "Done. Saves are at ${remote}${NEW_SAVES}, backups at ${remote}${NEW_BACKUPS}."
1491:     [ "${moved_saves}" = "1" ] && say "Old folders were left in place if anything else was in them."
1492:     return 0
1493: }
1494: 
1495: # --superseded: the list, one per line, for the sync scripts' string test
1496: # before they pay for a network call (no conf, no network, no lock).
1497: if [ "${1:-}" = "--superseded" ]; then printf '%s\n' "${SUPERSEDED_DEFAULT_SAVES[@]}"; exit 0; fi
1498: # --needs-step: whether the cloud folder step has something to settle
1499: # (D-CLOUD-170), asked at every boot, so no network and no rclone start: the
1500: # saves folder is a default this project once shipped, the player has not
1501: # kept it, and a remote is set up. 0 when it has, 1 when not, 2 when the
1502: # conf cannot be read -- which settles nothing, so the step stays away.
1503: # Names compared as written, case included: with no network there is no
1504: # asking the cloud whether it folds case, and a hand-typed /games that a
1505: # case-sensitive cloud calls the player's own would put the scan up at
1506: # every boot for nothing. The scripts write the defaults in their own case.
1507: if [ "${1:-}" = "--needs-step" ]; then
1508:     CASE_INSENSITIVE=0
1509:     if [ -e "${MIGRATION_RECORD}" ]; then
1510:         grep -q '^\[' /storage/.config/rclone/rclone.conf 2>/dev/null || exit 1
1511:         exit 0
1512:     fi
1513:     _saves=$(conf_value SAVES_REMOTE) || exit 2
1514:     _keep=$(conf_value LAYOUT_KEEP) || exit 2
1515:     if same_folder "${_saves}" "${NEW_SAVES}"; then
1516:         _backups=$(conf_value SETTINGS_REMOTE) || exit 2
1517:         _content=$(conf_value CONTENT_REMOTE) || exit 2
1518:         if same_folder "${_backups}" "${NEW_BACKUPS}" && historical_content "${_content}"; then
1519:             grep -q '^\[' /storage/.config/rclone/rclone.conf 2>/dev/null || exit 1
1520:             exit 0
1521:         fi
1522:     fi
1523:     superseded_default "${_saves}" || exit 1
1524:     [ -n "${_keep}" ] && same_folder "${_saves}" "${_keep}" && exit 1
1525:     grep -q '^\[' /storage/.config/rclone/rclone.conf 2>/dev/null || exit 1
1526:     exit 0
1527: fi
1528: [ "${1:-}" = "--apply" ] && take_cloud_lock
1529: main "$@" 9>&-
```


## SOURCE projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup

```text
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_content_backup - push game content (ROMs, BIOS, ...) to the cloud.
6: #
7: # Mirror of cloud_content_restore: an explicit, user-initiated copy of chosen
8: # local directories from /storage/roms to the cloud content root. Copy-only -
9: # it never deletes anything on the remote. Save/state/screenshot directories
10: # are excluded here; they travel via the saves sync.
11: #
12: # Usage:
13: #   cloud_content_backup --list           print local content directories
14: #   cloud_content_backup --list-sizes     print them as name|bytes
15: #   cloud_content_backup <dir> [<dir>..]  copy local dirs to the cloud
16: #   cloud_content_backup --all            copy all local content directories
17: #
18: # The remote content root defaults to the remote's root; set CONTENT_REMOTE in
19: # /storage/.config/cloud_sync.conf to point somewhere else (e.g. "GAMES").
20: 
21: . /etc/profile
22: 
23: LOG_FILE="/var/log/cloud_sync.log"
24: SCRIPT_NAME=$(basename "$0")
25: DEST="/storage/roms"
26: 
27: # The exit that means "nothing ran: another cloud sync holds the lock", which
28: # EmulationStation names (SKIPPED - ANOTHER CLOUD SYNC IS RUNNING). It was 3
29: # until 2026-09-09, which is also rclone's "directory not found", so a failed
30: # unit carrying rclone's code to the final exit read as a sync that was never
31: # running (#99, blindspot 33). sysexits.h's EX_TEMPFAIL sits above everything
32: # rclone returns (0-9) and below the 128+signal range, so nothing this script
33: # forwards can produce it. The same two numbers (75, and 69 for no network --
34: # raised here when the link goes away under a running unit, see
35: # stop_no_network) are what EmulationStation reads; scripts and ES ship
36: # together.
37: readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69
38: 
39: log_message() {
40:     echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO] [${SCRIPT_NAME}] ${1}" >> ${LOG_FILE}
41: }
42: 
43: # One cloud transfer at a time, whoever asked for it.
44: #
45: # Three callers can start one: EmulationStation at boot (the startup sync,
46: # which ran headless from autostart/102-cloud-saves until #94), EmulationStation
47: # after a game exits, and a person in the menu. Until
48: # 2026-09-04 the game-exit path was an OS hook with a pgrep guard; moving it
49: # into ES kept the visible progress and dropped the guard, so exiting a game
50: # during the boot sync started a second rclone against the same remote. Two
51: # writers on one folder is how a mirror deleted another handheld's saves
52: # (D-CLOUD-014); two copies racing is milder, and still nothing anybody asked
53: # for.
54: #
55: # The lock lives here, in the script, so no caller has to know about the
56: # others. /var/run is tmpfs, so a lock cannot survive a reboot and go stale.
57: # Non-blocking, because a request that queues silently behind a twenty-minute
58: # transfer looks exactly like one that hung. Exit EXIT_LOCK_HELD (75) means
59: # "skipped: another sync is running" -- the UI names it, and no last-run stamp
60: # is written for work that did not happen.
61: #
62: # The descriptor is this shell's and nothing else's. A shell redirection
63: # carries no close-on-exec, so `exec 9>` hands fd 9 to every child the
64: # script starts, and rclone then holds the lock for the whole of a transfer
65: # (watched in /proc on the VM, #124). While the script outlives its
66: # children that is invisible, because bash waits for each of them before it
67: # exits. The moment it does not -- killed or orphaned while rclone is still
68: # copying, a child left in the background -- the lock outlives the run that
69: # took it and every sync afterwards is refused with "another cloud sync is
70: # running" when nothing is running at all. So the body runs with fd 9
71: # closed ("9>&-"): bash keeps the lock on a descriptor of its own, which it
72: # does mark close-on-exec, and nothing this script starts can see it.
73: #
74: # The refusal also waits a moment before saying no, as belt and braces for
75: # a holder this script does not own: a descriptor leaked by an older build,
76: # or a process in the act of exiting, frees itself in milliseconds, while a
77: # real concurrent transfer does not. One second of patience turns a raced
78: # skip into a run that works and costs a genuinely blocked run one second.
79: CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
80: take_cloud_lock() {
81:     local tries=0
82:     exec 9>"${CLOUD_SYNC_LOCK}"
83:     while ! flock -n 9; do
84:         if [ "${tries}" -ge 4 ]; then
85:             echo "Skipped: another cloud sync is already running. Try again when it's done."
86:             log_message "skipped: another cloud sync holds ${CLOUD_SYNC_LOCK}"
87:             exit "${EXIT_LOCK_HELD}"
88:         fi
89:         tries=$((tries + 1))
90:         sleep 0.25
91:     done
92: }
93: 
94: if [ ! -e "/storage/.config/rclone/rclone.conf" ]; then
95:     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
96:     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
97:     exit 1
98: fi
99: 
100: # The two values this script needs from cloud_sync.conf, read as text and
101: # never sourced (audit #307 PL-051's script half): a folder value an earlier
102: # build wrote with "$(...)" in it ran on every `source`. A CONTENT_REMOTE
103: # that carries a $, a backtick, a backslash or a control character is not a
104: # folder name, and the run refuses it rather than use it as a path.
105: #
106: # Read in the forms `source` reads (the audit of the fixes, G-A-06/G-A-02):
107: # the value double quoted, single quoted or bare; after it nothing, or
108: # blanks and a # comment. The first cut took only KEY=value or KEY="value"
109: # whole: a trailing comment or single quotes gave an empty CONTENT_REMOTE --
110: # the cloud's root -- where the folder had been, and the backup went there.
111: # A line it cannot read as plain text exits 2, and CONTENT_REMOTE's refuses
112: # the run; nothing is read as the root that did not say the root. Of two
113: # lines for one key, the first: every saves run EmulationStation starts is
114: # --yes, which runs cloud_sync_cleanup_duplicates.sh, which keeps the first,
115: # so that is the value the saves scripts run with and the file is left with.
116: #
117: # And a file with a control character but a tab anywhere in it is
118: # unreadable here as it is to the saves scripts' conf_valid (the audit of
119: # the fix round, PL-002): this reader never sources the file, but a blank
120: # is a space or a tab to both, so the tiers run with one reading of one
121: # file -- a carriage return after a value used to pass here as a blank.
122: #
123: # The key set in a form `source` reads and this does not -- indented,
124: # exported, declared, appended to, or with a blank before the = -- is
125: # unreadable, never absent (the audit of the fix round, lead G2-A-03):
126: # read as absent it was the cloud's root, and a content backup went there.
127: # The saves scripts' conf_valid refuses such a file whole.
128: conf_get() { # <KEY>: its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
129:     [ -f /storage/.config/cloud_sync.conf ] || return 0
130:     awk -v k="$1" '
131:         { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
132:         index($0, k "=") != 1 && !other \
133:             && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
134:         index($0, k "=") == 1 {
135:             s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
136:             c = substr(s, 1, 1)
137:             if (c == "\"") {
138:                 # Inside double quotes bash reads \" \\ \$ and \` as the one
139:                 # character each (PL-015), and so does this; an unescaped $
140:                 # or backtick is an expansion this reader does not make, and
141:                 # any other backslash is refused as conf_valid refuses it.
142:                 n = length(s); i = 2; closed = 0
143:                 while (i <= n) {
144:                     d = substr(s, i, 1)
145:                     if (d == "\"") { closed = 1; break }
146:                     if (d == "\\") {
147:                         e = substr(s, i + 1, 1)
148:                         if (e == "\"" || e == "\\" || e == "$" || e == "`") { v = v e; i += 2; continue }
149:                         ok = 0
150:                         why = (e == "") ? "a value continued onto the next line, which this reader does not follow" \
151:                                         : "a backslash inside double quotes that is not one of the escapes bash reads there"
152:                         break
153:                     }
154:                     if (d == "$" || d == "`") { ok = 0; why = "a $ or a backtick inside double quotes"; break }
155:                     v = v d; i++
156:                 }
157:                 if (ok && !closed) { ok = 0; why = "a double-quoted value that does not close on its line" }
158:                 if (ok) r = substr(s, i + 1)
159:             } else if (c == "'"'"'") {
160:                 j = index(substr(s, 2), c)
161:                 if (j) { v = substr(s, 2, j - 1); r = substr(s, j + 2) } else { ok = 0; why = "a single-quoted value that does not close on its line" }
162:             } else {
163:                 match(s, /^[A-Za-z0-9_.\/:@%+,=-]*/); v = substr(s, 1, RLENGTH); r = substr(s, RLENGTH + 1)
164:             }
165:             if (ok && r !~ /^([ \t]+(#.*)?)?$/) { ok = 0; why = "something after the value that is not a # comment" }
166:             if (!found) { found = 1; first = v; firstok = ok; firstwhy = "line " NR ": " why }
167:         }
168:         END {
169:             if (cntrl) { print "line " cntrl ": a control character other than a tab"; exit 2 }
170:             if (other) { print "line " other ": " k " set in a form this reader does not read"; exit 2 }
171:             if (found && !firstok) { print firstwhy; exit 2 }
172:             if (found) print first
173:         }
174:     ' /storage/.config/cloud_sync.conf
175: }
176: if ! CONTENT_REMOTE=$(conf_get CONTENT_REMOTE); then
177:     # On a refusal conf_get says why, for the log: the line and its shape,
178:     # never the value (PL-015).
179:     log_message "cloud_sync.conf was not read: ${CONTENT_REMOTE}"
180:     echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
181:     echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
182:     exit 1
183: fi
184: # The bound falls back to the shipped value below when this is empty; a
185: # line it cannot read is that too, and the log says so.
186: if ! RCLONE_NET_OPTS=$(conf_get RCLONE_NET_OPTS); then
187:     log_message "RCLONE_NET_OPTS was not read (${RCLONE_NET_OPTS}); the shipped bound stands in"
188:     RCLONE_NET_OPTS=""
189: fi
190: case "${CONTENT_REMOTE}" in
191:     *[\$\`\\]*|*[[:cntrl:]]*)
192:         echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
193:         echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
194:         exit 1 ;;
195: esac
196: 
197: REMOTENAME=$(rclone listremotes | head -1)
198: if [ -z "${REMOTENAME}" ]; then
199:     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
200:     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
201:     exit 1
202: fi
203: 
204: ROOT="${REMOTENAME}${CONTENT_REMOTE:+${CONTENT_REMOTE}/}"
205: 
206: # The bound on every rclone command below that opens a socket: RCLONE_NET_OPTS
207: # from cloud_sync.conf, or the same shipped values when the config has no
208: # such line yet -- this script reads the config without running
209: # cloud_sync_helper, so on the first run after an update it may not, and the
210: # bound is a guard that a missing line must not switch off. The reasoning
211: # for the numbers is beside the option in cloud_sync.conf.defaults; the
212: # short version is that rclone's own defaults (60 s connect, 5 min idle, 10
213: # low-level retries, 3 whole-run retries) hold a run for over ten minutes
214: # on a link that drops mid-run (#101, #102, #103). Keep the fallback in step
215: # with the default.
216: RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
217: _net_opts=$(echo "${RCLONE_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
218: [ -n "${_net_opts}" ] || _net_opts="${RCLONE_NET_OPTS_FALLBACK}"
219: read -r -a RCLONE_NET_OPTS_ARRAY <<< "${_net_opts}"
220: # Installed beside this script, also when the host fixtures copy it.
221: . "$(dirname "${BASH_SOURCE[0]}")/cloud_content_transfer" || exit 1
222: # A probe is a single listing that exists to answer quickly: one attempt,
223: # tighter than the transfers (the same values the saves scripts probe with).
224: readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
225: # A listing's bound (#143): three low-level retries, not a transfer's ten --
226: # rclone's S3 backend hands the count to the AWS SDK as attempts with
227: # exponential backoff (see cloud_backup for the measurement).
228: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
229: 
230: # Whole or not at all: to a temporary name beside the stamp, then renamed
231: # over it, as ThreadedCloudSync::recordOutcome does. A kill mid-write leaves
232: # the previous stamp; it used to leave an empty file (D-CLOUD-078, #105).
233: # LAST_WHY, when a `>>> why` line was printed, becomes the stamp's third
234: # field as a token (spaces to underscores) for the row to read (D-UI-028).
235: LAST_WHY=""
236: write_stamp() {
237:     local file="$1" line="$2" tmp
238:     mkdir -p "$(dirname "${file}")" 2>/dev/null
239:     tmp="${file}.tmp.$$"
240:     { printf '%s\n' "${line}" > "${tmp}"; } 2>/dev/null \
241:         && mv -f "${tmp}" "${file}" 2>/dev/null \
242:         || rm -f "${tmp}" 2>/dev/null
243: }
244: record_outcome() { # <stamp-name> <rc>
245:     local why=""
246:     case "$2" in
247:         0|9|"${EXIT_NO_NETWORK}"|"${EXIT_LOCK_HELD}") ;;
248:         *) [ -n "${LAST_WHY}" ] && why=" $(printf '%s' "${LAST_WHY}" | tr ' ' '_')" ;;
249:     esac
250:     write_stamp "/storage/.cache/cloud_sync/last-$1" "$(date +%s) $2${why}"
251: }
252: 
253: # Why a unit did not finish, in the player's words (D-UI-028, D-CLOUD-077):
254: # one `>>> why <SENTENCE>` protocol line per failing unit, which the page
255: # and the card read; rclone's code stays in the log. The sentences are the
256: # vocabulary table's in es-native-ui.md.
257: say_why() {
258:     LAST_WHY="$1"
259:     echo ">>> why $1"
260:     log_message "why: $1"
261: }
262: why_for() {
263:     case "$1" in
264:         3|4) echo "COULDN'T FIND YOUR CLOUD FOLDER" ;;
265:         5|124) echo "YOUR CLOUD STOPPED ANSWERING" ;;
266:         6)   echo "SOME FILES DIDN'T FINISH" ;;
267:         7|8) echo "YOUR CLOUD WOULDN'T TAKE THE FILES" ;;
268:         130) echo "IT WAS STOPPED" ;;
269:         *)   echo "SOMETHING WENT WRONG" ;;
270:     esac
271: }
272: 
273: has_default_route() {
274:     ip -4 route show default 2>/dev/null | grep -q . \
275:         || ip -6 route show default 2>/dev/null | grep -q .
276: }
277: 
278: # Is the network gone? Asked after rclone failed, so the run can say why it
279: # ended rather than hand up a code that reads as FAILED and sends somebody
280: # to a log. Gone: no default route, or a route through which neither the
281: # remote nor anything else answers a bounded probe. Not gone: the remote
282: # answers again (a blip rclone did not survive), or the internet answers
283: # while the remote does not (the provider, or the sign-in) -- that is
284: # rclone's failure to report, and the caller passes rclone's code through
285: # as before. The same three questions cloud_backup asks (#101, #103).
286: network_gone() {
287:     has_default_route || return 0
288:     rclone lsd "${REMOTENAME}" "${RCLONE_PROBE_OPTS[@]}" >/dev/null 2>&1 && return 1
289:     ping -q -c1 -W 3 1.1.1.1 >/dev/null 2>&1 && return 1
290:     ping -q -c1 -W 3 8.8.8.8 >/dev/null 2>&1 && return 1
291:     return 0
292: }
293: 
294: # The network went away under a running unit. Says so, records that the run
295: # did not complete -- never a 0, which would read as a backup that happened
296: # -- and exits EXIT_NO_NETWORK, which EmulationStation names (SKIPPED - NO
297: # NETWORK CONNECTION on the card, SKIPPED, NO NETWORK on the row). No
298: # further unit is attempted: each would stall for another minute against
299: # the same dead link. rclone copy writes each file under a temporary name
300: # and renames it when complete, so nothing partial is left in the cloud.
301: #
302: # SKIPPED means nothing was touched (#308 claude F-CS-24): once a unit has
303: # completed, a run the network then ends stamps "69 gaps <why>", which the
304: # rows read as COULDN'T FINISH; the exit stays 69.
305: # Did this run's rclone move a file since <offset> into the log? Progress,
306: # for the stamp stop_no_network writes, is what rclone logged moving --
307: # "<path>: Copied (...)", "Moved (...)", "Deleted" -- not a unit that
308: # completed (the audit of the fixes, G-A-08/G-A-13): files a unit moved
309: # before its own failure did not count, and a unit that moved nothing did.
310: # Every transfer here logs at INFO to LOG_FILE, and the transfer lock
311: # keeps any other cloud script from writing it meanwhile.
312: log_offset() { stat -c %s "${LOG_FILE}" 2>/dev/null || echo 0; }
313: moved_since() { # <byte offset into LOG_FILE>
314:     local now
315:     now=$(stat -c %s "${LOG_FILE}" 2>/dev/null) || return 1
316:     [ "${now}" -gt "$1" ] 2>/dev/null || return 1
317:     tail -c +$(( $1 + 1 )) "${LOG_FILE}" 2>/dev/null | grep -qE ': (Copied|Moved) \(|: Deleted$'
318: }
319: PROGRESS_MADE=0
320: stop_no_network() {
321:     local rc="$1" unit="$2"
322:     echo "Couldn't finish: lost the network while backing up ${unit}. Try again when you're online."
323:     log_message "stopped: the network went away while backing up ${unit} (rclone exit ${rc}); exit ${EXIT_NO_NETWORK}"
324:     if [ "${PROGRESS_MADE}" = 1 ]; then
325:         write_stamp "/storage/.cache/cloud_sync/last-content-backup" "$(date +%s) ${EXIT_NO_NETWORK} gaps YOU WENT OFFLINE PART-WAY THROUGH"
326:     else
327:         record_outcome content-backup "${EXIT_NO_NETWORK}"
328:     fi
329:     exit "${EXIT_NO_NETWORK}"
330: }
331: 
332: # What this device calls a game system.
333: #
334: # EmulationStation declares one <path> per system, and on a handheld those are
335: # the /storage/roms subdirectories that hold games. Deriving the list from the
336: # device's own config means it is right per device -- an H700 has 122, a
337: # Snapdragon target has more -- and it never drifts, because the image that
338: # adds a system also adds it here.
339: #
340: # Match on <path>, not <name>: they differ for a dozen systems (ES calls the
341: # folder "coleco" and the system "colecovision", "fbneo"/"fbn", "pc88"/"pc-88"),
342: # and matching names silently drops those folders from the backup.
343: ES_SYSTEMS=""
344: for c in /storage/.config/emulationstation/es_systems.cfg \
345:          /usr/config/emulationstation/es_systems.cfg; do
346:     [ -r "${c}" ] && { ES_SYSTEMS="${c}"; break; }
347: done
348: 
349: system_folders() {
350:     [ -n "${ES_SYSTEMS}" ] || return 0
351:     sed -n 's:.*<path>/storage/roms/\([^</]*\).*:\1:p' "${ES_SYSTEMS}" | sort -u
352: }
353: 
354: # Local content directories, by allowlist.
355: #
356: # This used to be a denylist -- everything under /storage/roms except four
357: # names -- so any directory that appeared there was uploaded as though it were
358: # a game system. That is the same shape of mistake as a denylist sync filter:
359: # what gets included is decided by what happens to be on the disk rather than
360: # by anything anyone chose. bezels, themes, music and a stray scummvm folder
361: # were all being swept up that way, none of them systems (ES keeps scummvm's
362: # games in /storage/.config/scummvm/games and music's playlists in
363: # /storage/.config/gmu/playlists -- the /storage/roms folders of those names
364: # are leftovers).
365: #
366: # In scope: the systems ES declares, and bios. Everything else is out, and
367: # stays out until somebody decides otherwise.
368: # The content-tier files under a directory, as one find(1) definition.
369: #
370: # Extra find arguments are appended, so a caller can list them, count them or
371: # total their sizes without restating the exclusions. "Does this hold
372: # anything?" and "how much does it hold?" answering about different file sets
373: # is exactly how a badge ends up contradicting the size printed next to it.
374: #
375: # Kept in step with SAVE_EXCLUDES and CONFLICT_EXCLUDES below by hand -- there
376: # is no shared parser, and a pattern added there must be added here. The
377: # conflict patterns matter as much as the save ones: without them --list-sizes
378: # counts another sync client's duplicate as content this device holds, and the
379: # picker's badge reports a size the cloud will never agree with.
380: content_files() {
381:     local dir="$1"; shift
382:     # One rule for both sides (D-CLOUD-048), set by MEDIA_MODE (D-CLOUD-050):
383:     #   roms  -- ROMs and BIOS only: the scraper's folders and the game list
384:     #            are neither listed nor moved
385:     #   with  -- ROMs and game content together
386:     #   only  -- game content alone: the scraper's folders and gamelist.xml
387:     # The game list is game content (D-CLOUD-049): the scraper writes it
388:     # beside the artwork, and a restored-then-scraped device must read as
389:     # matching its cloud under ROMs alone. At any depth, as the transfers
390:     # move it (the ROMs pass excludes "**/gamelist.xml", the game-list pass
391:     # includes it): a list below a system's own folder was counted as a ROM
392:     # (the audit of the fixes, G-A-10).
393:     local -a media=()
394:     local d
395:     case "${MEDIA_MODE:-roms}" in
396:         roms) for d in ${MEDIA_DIRS:-images videos manuals screenshots fanart boxart wheel mix maps media}; do media+=( ! -path "${dir%/}/${d}/*" ); done
397:               media+=( ! -name gamelist.xml ) ;;
398:         only) media+=( "(" -name gamelist.xml )
399:               for d in ${MEDIA_DIRS:-images videos manuals screenshots fanart boxart wheel mix maps media}; do media+=( -o -path "${dir%/}/${d}/*" ); done
400:               media+=( ")" ) ;;
401:     esac
402:     find "${dir}" -type f \
403:         ! -name '*.srm' ! -name '*.sav' ! -name '*.fs' ! -name '*.state*' \
404:         ! -name '*.auto' ! -name '*.dsv*' ! -name '*.eep' ! -name '*.mpk' \
405:         ! -name '*.sra' ! -name '*.fla' ! -name '*.mcd' ! -name '*.mcr' \
406:         ! -path '*/save/*' ! -path '*/memcards/*' \
407:         ! -path '*/shared/savefiles/*' ! -path '*/PPSSPP/*' \
408:         ! -path '*conflicted copy*' ! -name '*.sync-conflict-*' \
409:         ! -name '*.????????.partial' \
410:         ! -path "${dir%/}/README.txt" \
411:         "${media[@]}" "$@" 2>/dev/null
412: }
413: 
414: # Does this directory hold anything the content tier would actually transfer?
415: has_content() {
416:     content_files "$1" | head -1 | grep -q .
417: }
418: 
419: # How many bytes of it. Compared against the cloud's own total to answer
420: # whether a system on this device matches what is stored -- an equal total is
421: # not proof of identical files (see #53), so the caller must not phrase it as
422: # one, but a different total is proof they differ, which is the case worth
423: # flagging.
424: content_bytes() {
425:     content_files "$1" -exec stat -c '%s' {} + \
426:         | awk '{ t += $1 } END { print t+0 }'
427: }
428: 
429: list_local_dirs() {
430:     local allow
431:     allow=$(system_folders)
432:     for d in "${DEST}"/*/; do
433:         [ -d "${d}" ] || continue
434:         base=$(basename "${d}")
435:         # The saves sync owns these, and ES declares screenshots and
436:         # savestates as systems of its own -- so the allowlist alone lets them
437:         # through, and content sync would upload the same files the saves sync
438:         # is already keeping, into a second place, under different rules.
439:         # Membership of the content tier is the intersection: a system ES
440:         # declares, and not something another tier already owns.
441:         case "${base}" in
442:             savefiles|savestates|screenshots|backup) continue ;;
443:         esac
444:         if [ "${base}" != "bios" ]; then
445:             printf '%s\n' "${allow}" | grep -qxF "${base}" || continue
446:         fi
447:         # Skip a directory with nothing this tier would carry.
448:         #
449:         # "Not empty" is the wrong test: RetroArch writes .srm and .state next
450:         # to the ROM, so a system whose only contents are saves looks populated
451:         # while a content transfer would send nothing from it. That made --list
452:         # claim the device "has" GBA when what it had was GBA saves, and the
453:         # picker's badge repeated the claim.
454:         #
455:         has_content "${d}" || continue
456:         echo "${base}"
457:     done
458: }
459: 
460: # Where a local directory belongs in the cloud.
461: #
462: # The cloud layout is for a person looking at it on a computer, not a mirror of
463: # the device's storage. There, "bios" is just another folder beside the game
464: # systems, which is an accident of how the handheld stores things and tells a
465: # reader nothing. Two named folders do: ROMs and BIOS.
466: remote_for() {
467:     case "$1" in
468:         bios) echo "${ROOT}BIOS" ;;
469:         *)    echo "${ROOT}ROMs/$1" ;;
470:     esac
471: }
472: 
473: # The systems this device syncs, chosen once and changeable. See
474: # cloud_content_restore for why this lives in /storage/.cache rather than in
475: # anything the settings backup captures. A device that does not want PS2 coming
476: # down does not want it going up either, so both directions read the same file.
477: SELECTION="/storage/.cache/cloud_sync/content-systems"
478: 
479: # Only a system folder's name is ever acted on (audit #307 PL-030):
480: # --set-systems refuses any other since that change, and a selection an
481: # earlier build wrote without the check is read past a line that is not
482: # one, never with it.
483: selected_systems() {
484:     [ -r "${SELECTION}" ] || return 0
485:     grep -E '^[A-Za-z0-9_][A-Za-z0-9._-]*$' "${SELECTION}" 2>/dev/null
486: }
487: 
488: # --with-media: include scraped game content (D-CLOUD-048). Off by default:
489: # the scraper's folders under a system are neither moved nor counted unless
490: # the switch is on, so a restored-then-scraped device does not read as
491: # "different" from its cloud copy. Taken from anywhere on the command line.
492: MEDIA_MODE=roms
493: _ARGS=()
494: for _a in "$@"; do
495:     case "${_a}" in
496:         --with-media) MEDIA_MODE=with ;;
497:         --media-only) MEDIA_MODE=only ;;
498:         *) _ARGS+=("${_a}") ;;
499:     esac
500: done
501: set -- "${_ARGS[@]}"
502: MEDIA_DIRS="images videos manuals screenshots fanart boxart wheel mix maps media"
503: # What the main rclone pass carries, per mode. The game list never rides the
504: # main pass: it has its own --update pass below (newest wins), which runs
505: # only when game content is in scope.
506: MEDIA_EXCLUDES=()
507: case "${MEDIA_MODE}" in
508:     roms) for _d in ${MEDIA_DIRS}; do MEDIA_EXCLUDES+=(--exclude "/${_d}/**"); done ;;
509:     only) for _d in ${MEDIA_DIRS}; do MEDIA_EXCLUDES+=(--include "/${_d}/**"); done ;;
510: esac
511: 
512: case "${1}" in
513:     --selected)
514:         # Only the selected systems that this device actually has content for.
515:         mapfile -t ALLDIRS < <(list_local_dirs)
516:         DIRS=()
517:         for d in "${ALLDIRS[@]}"; do
518:             selected_systems | grep -qxF "${d}" && DIRS+=("${d}")
519:         done
520:         # BIOS is not a system and not a pick (D-CLOUD-043): it comes with
521:         # the ROMs tier whenever this device holds any, exactly as restore
522:         # brings it whenever the cloud does. Found in the VM on 2026-09-06:
523:         # a device's BIOS folder never went up once the picker stopped
524:         # listing it. Not with game content alone -- BIOS is not that.
525:         if [ "${MEDIA_MODE}" != only ] && printf '%s\n' "${ALLDIRS[@]}" | grep -qx bios \
526:             && ! printf '%s\n' "${DIRS[@]}" | grep -qx bios; then
527:             DIRS+=("bios")
528:         fi
529:         # Nothing here to send is nothing to do -- a run that completed, not
530:         # one that failed (#308 claude F-CS-15): it exited 1, and the page
531:         # read COULDN'T FINISH - SOMETHING WENT WRONG. Exit 0, the sentence,
532:         # and the stamp saying the last press completed.
533:         if [ ${#DIRS[@]} -eq 0 ]; then
534:             echo "Nothing to back up: none of the systems you picked have anything on this device."
535:             record_outcome content-backup 0
536:             exit 0
537:         fi
538:     ;;
539:     --list)
540:         list_local_dirs
541:         exit $?
542:     ;;
543:     --list-sizes)
544:         # name|bytes for what this device holds, the mirror of
545:         # cloud_content_restore --scan. The picker needs both sides to say
546:         # whether a system here matches the copy in the cloud.
547:         while IFS= read -r base; do
548:             [ -n "${base}" ] || continue
549:             printf '%s|%s\n' "${base}" "$(content_bytes "${DEST}/${base}")"
550:         done < <(list_local_dirs)
551:         exit 0
552:     ;;
553:     --all)
554:         mapfile -t DIRS < <(list_local_dirs)
555:         if [ ${#DIRS[@]} -eq 0 ]; then
556:             echo "Nothing to back up: there are no ROMs or BIOS files on this device."
557:             record_outcome content-backup 0
558:             exit 0
559:         fi
560:     ;;
561:     "")
562:         echo "Usage: ${SCRIPT_NAME} --list | --list-sizes | --all | <dir> [<dir>...]" >&2
563:         exit 1
564:     ;;
565:     *)
566:         DIRS=("$@")
567:     ;;
568: esac
569: 
570: # Another sync client's unresolved dispute is not our content.
571: #
572: # Dropbox and Nextcloud rename the losing side of a concurrent write to
573: # "X (Someone's conflicted copy 2026-09-03)"; Syncthing appends
574: # ".sync-conflict-<date>". Carrying those onto a handheld doubles the storage
575: # for no benefit -- the player cannot resolve a conflict from a games menu --
576: # and it makes the artifacts immortal: a device that downloaded them uploads
577: # them again on the next backup, so deleting them in the cloud looks like the
578: # provider putting them back. That happened here, to 271 directories of BIOS
579: # (2026-09-04).
580: #
581: # Resolution belongs on the computer where both sides can be seen. We decline
582: # to move them in either direction, which is also the only way a cleanup on
583: # one side stays done.
584: CONFLICT_EXCLUDES=(
585:     --exclude "**conflicted copy**"
586:     --exclude "**.sync-conflict-**"
587:     --exclude "*.????????.partial"
588: )
589: 
590: # gamelist.xml travels on its own terms.
591: #
592: # It is the scraping payload -- names, descriptions, genres, ratings, media
593: # paths and the cheevos hashes that cost a hash of every ROM -- and all of that
594: # is device-independent, so sharing it means scraping once rather than once per
595: # handheld. Paths inside it are relative ("./Mega Man 3 (USA).zip"), so it
596: # carries across devices unchanged.
597: #
598: # It degrades well in both directions, which is why this is safe at all:
599: #
600: #   * Reading, EmulationStation builds its list from the filesystem first and
601: #     skips any entry whose ROM is absent ("does not exist ... Ignoring"), so a
602: #     52-entry list on a handheld holding 10 of those games shows 10 games and
603: #     no phantoms. That holds while ParseGamelistOnly is false, which is the
604: #     default.
605: #   * Writing, updateGamelist re-reads the file and rewrites only the entries
606: #     whose metadata changed, preserving entries for ROMs this device does not
607: #     have -- deliberately, per its own comment.
608: #
609: # What neither of those protects against is rclone, which replaces a file
610: # wholesale. A device that scans its own ROMs and uploads before it has ever
611: # restored would push a thin list over a rich one. That is an ordering problem,
612: # not a merge problem, and --update solves it: skip when the destination is
613: # newer, so the freshest list wins rather than the last writer.
614: #
615: # Hence a separate pass. --update on the whole content transfer would also
616: # apply to ROMs, where "destination is newer" is not a reason to skip a file
617: # somebody deliberately re-uploaded.
618: #
619: # Three fields remain genuinely per-device -- playcount, lastplayed and
620: # gametime, which EmulationStation itself marks isStatistic and refuses to let
621: # a scrape overwrite. A file-level sync cannot make that distinction, so those
622: # are last-writer-wins across devices. Everything else in the file is authored
623: # or scraped, and favorite is explicitly not a statistic in ES's model.
624: GAMELIST_ONLY=( --include "gamelist.xml" --include "**/gamelist.xml" )
625: 
626: # What the saves tier owns, and content must never carry.
627: #
628: # A system directory holds more than games: RetroArch writes .srm and .state
629: # next to the ROM, and several systems keep memory cards in a subfolder. The
630: # saves allowlist claims all of it ("+ /**/*.srm" and friends in
631: # cloud_sync-rules.txt), so uploading a system folder wholesale puts saves
632: # in a second cloud location under different rules -- two writers and no
633: # reconciliation, which is exactly how 70 files were deleted on 2026-09-01.
634: #
635: # Worse in the other direction: a content restore would then copy stale saves
636: # back over live ones.
637: #
638: # The earlier allowlist fix (d77d4ea44d) covered directories another tier
639: # owns. This is the same rule one level down, for files. Kept in step with
640: # cloud_sync-rules.txt by hand -- there is no shared parser, and a pattern
641: # added there must be added here. .fla was added there (#89, N64's flash
642: # saves beside the ROM) and not here, so a content backup uploaded it and
643: # a match removed it as content (the audit's gpt F-CS-02).
644: SAVE_EXCLUDES=(
645:     --exclude "*.srm" --exclude "*.sav" --exclude "*.fs"
646:     --exclude "*.state*" --exclude "*.auto" --exclude "*.dsv*"
647:     --exclude "*.eep" --exclude "*.mpk" --exclude "*.sra" --exclude "*.fla"
648:     --exclude "*.mcd" --exclude "*.mcr"
649:     --exclude "save/**" --exclude "memcards/**"
650:     --exclude "shared/savefiles/**" --exclude "PPSSPP/**"
651: )
652: 
653: STATUS=0
654: take_cloud_lock
655: # Everything from here to the end of the script runs with the lock
656: # descriptor closed, so no child of this run can hold the lock once this
657: # shell is gone -- see take_cloud_lock. The brace group is the whole of
658: # the change: it adds no subshell, so exits, traps and variables behave
659: # exactly as they did.
660: {
661: UNIT_N=${#DIRS[@]}; UNIT_I=0
662: for DIR in "${DIRS[@]}"; do
663:     # Local -> remote. This script uploads; cloud_content_restore is the one
664:     # that brings content back down.
665:     SRC="${DEST}/${DIR}"
666:     TARGET="$(remote_for "${DIR}")"
667:     UNIT_I=$((UNIT_I + 1))
668:     log_message "Content backup: ${SRC} -> ${TARGET}"
669:     # The marker the transfer page reads: what is being copied, and which of
670:     # how many. Restore has emitted it since D-UI-024; backup never did, so
671:     # the page kept the previous script's last label -- SETTINGS BACKUP --
672:     # through every system it uploaded (maintainer, 2026-09-06).
673:     echo ">>> unit ${DIR:-everything}|${UNIT_I}|${UNIT_N}"
674:     echo "Backing up ${DIR:-everything} to the cloud..."
675:     # --progress is what puts the stats on stdout. With only --log-file they
676:     # go to the log and the caller sees nothing -- which is why the progress
677:     # card sat at "0 B / 0 B, -, 0 B/s" through a restore that was in fact
678:     # copying Mega Drive ROMs the whole time. The saves path has always passed
679:     # it; these two never did.
680:     #
681:     # And NOT --stats-one-line: that collapses the display to a totals line,
682:     # losing the per-file block. A transfer of a thousand small BIOS files
683:     # spends minutes between percentage changes, and the only thing that says
684:     # it is alive rather than stuck is the name of the file it is on right
685:     # now. --stats 1s keeps that moving.
686:     #
687:     # No --progress-terminal-width: the flag does not exist on every rclone we
688:     # ship against (the saves scripts test for it with "rclone help | grep"
689:     # before using it), and an unknown flag is a usage error that transfers
690:     # nothing. rclone pads the file name out to a guessed width; the reader
691:     # trims it, so the flag bought nothing worth a version check.
692:     #
693:     # The folder first, on its own. rclone creates a missing destination as
694:     # part of a copy, but only after listing it, and a server that answers a
695:     # missing folder with an error rather than "not found" (an FTP server's
696:     # 501 where the standard reply is 550) fails that listing. Under
697:     # --retries 1 that one attempt is the whole run: reported as failed,
698:     # with files that may or may not have landed (#142, from the #133
699:     # matrix: 2 of 3). mkdir is one round trip, idempotent, and on a bucket
700:     # under directory markers it writes the marker the folder's parent then
701:     # lists (D-CLOUD-120). Its own failure is left to the copy to report.
702:     rclone mkdir "${TARGET}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null
703:     UNIT_LOG0=$(log_offset)
704:     # The setup's note at a unit's root (BIOS/README.txt, cloud_setup
705:     # --seed-folders) is not content, and neither side counts it (#308 gpt
706:     # F-CS-30): it came down into /storage/roms/bios and read ever after as a
707:     # file this device has and the cloud does not.
708:     bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
709:         "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${MEDIA_EXCLUDES[@]}" \
710:         --exclude "gamelist.xml" --exclude "**/gamelist.xml" --exclude "/README.txt" \
711:         --progress --stats 1s \
712:         --log-file "${LOG_FILE}" --log-level INFO
713:     RC=$?
714: 
715:     # The game list: newest wins, rather than whoever ran last. Game content
716:     # only (D-CLOUD-049) -- under ROMs alone the file stays where it is. Its
717:     # result is the unit's, by the same 0|9 rule (audit #307 PL-066): it
718:     # was discarded with `|| true`, so a game list that did not move left a
719:     # unit, a stamp and a page that said the unit had.
720:     if [ "${MEDIA_MODE}" != roms ] && { [ "${RC}" -eq 0 ] || [ "${RC}" -eq 9 ]; }; then
721:         bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
722:             "${GAMELIST_ONLY[@]}" --update \
723:             --stats 0 \
724:             --log-file "${LOG_FILE}" --log-level INFO
725:         GL_RC=$?
726:         case "${RC}" in
727:             0|9) case "${GL_RC}" in 0|9) ;; *) RC=${GL_RC} ;; esac ;;
728:         esac
729:     fi
730: 
731:     # What moved in this unit, whatever its result (G-A-08/G-A-13).
732:     moved_since "${UNIT_LOG0}" && PROGRESS_MADE=1
733:     if [ ${RC} -ne 0 ] && [ ${RC} -ne 9 ]; then
734:         # A failed unit says why: the network gone ends the run as 69 here,
735:         # anything else carries rclone's own code up as before.
736:         network_gone && stop_no_network "${RC}" "${DIR:-everything}"
737:         log_message "backup of ${DIR:-everything}: rclone exit ${RC}"
738:         echo "Couldn't finish backing up ${DIR:-everything}: $(why_for "${RC}" | tr 'A-Z' 'a-z')."
739:         say_why "$(why_for "${RC}")"
740:         STATUS=${RC}
741:     else
742:         echo "Backed up ${DIR:-everything}."
743:     fi
744: done
745: 
746: # The progress card is gone by the time somebody who walked away comes back, so
747: # leave the outcome where the menu can read it later. Device-local state, so it
748: # lives under /storage/.cache and not in the settings backup.
749: record_outcome content-backup "${STATUS}"
750: 
751: # A failed unit leaves with rclone's own code, unremapped: nothing rclone
752: # returns can read as the lock sentinel now that it is 75 (#99).
753: exit ${STATUS}
754: } 9>&-
```


## SOURCE projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore

```text
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_content_restore - pull game content (ROMs, BIOS, ...) from the cloud.
6: #
7: # Unlike the saves sync (allowlist-filtered, never touches ROMs/BIOS), this is
8: # an explicit, user-initiated copy of a chosen remote directory into
9: # /storage/roms. It never deletes anything locally (rclone copy) and skips
10: # files that already exist unless they differ.
11: #
12: # Usage:
13: #   cloud_content_restore --list           print top-level remote directories
14: #   cloud_content_restore <dir> [<dir>..]  copy remote dirs into /storage/roms
15: #   cloud_content_restore --all            copy the whole remote content root
16: #   cloud_content_restore --match          preview making this device match;
17: #                                          writes the plan --apply is held to
18: #   cloud_content_restore --match --apply  do what the preview planned, no
19: #                                          more (the only mode that deletes)
20: #
21: # The remote content root defaults to the remote's root; set CONTENT_REMOTE in
22: # /storage/.config/cloud_sync.conf to point somewhere else (e.g. "GAMES").
23: 
24: . /etc/profile
25: 
26: LOG_FILE="/var/log/cloud_sync.log"
27: SCRIPT_NAME=$(basename "$0")
28: DEST="/storage/roms"
29: 
30: # The exit that means "nothing ran: another cloud sync holds the lock", which
31: # EmulationStation names (SKIPPED - ANOTHER CLOUD SYNC IS RUNNING). It was 3
32: # until 2026-09-09, which is also rclone's "directory not found", so a failed
33: # unit carrying rclone's code to the final exit read as a sync that was never
34: # running (#99, blindspot 33). sysexits.h's EX_TEMPFAIL sits above everything
35: # rclone returns (0-9) and below the 128+signal range, so nothing this script
36: # forwards can produce it. The same two numbers (75, and 69 for no network --
37: # raised here when the link goes away under a running unit, see
38: # stop_no_network) are what EmulationStation reads; scripts and ES ship
39: # together.
40: readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69
41: 
42: log_message() {
43:     echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO] [${SCRIPT_NAME}] ${1}" >> ${LOG_FILE}
44: }
45: 
46: # One cloud transfer at a time, whoever asked for it.
47: #
48: # Three callers can start one: EmulationStation at boot (the startup sync,
49: # which ran headless from autostart/102-cloud-saves until #94), EmulationStation
50: # after a game exits, and a person in the menu. Until
51: # 2026-09-04 the game-exit path was an OS hook with a pgrep guard; moving it
52: # into ES kept the visible progress and dropped the guard, so exiting a game
53: # during the boot sync started a second rclone against the same remote. Two
54: # writers on one folder is how a mirror deleted another handheld's saves
55: # (D-CLOUD-014); two copies racing is milder, and still nothing anybody asked
56: # for.
57: #
58: # The lock lives here, in the script, so no caller has to know about the
59: # others. /var/run is tmpfs, so a lock cannot survive a reboot and go stale.
60: # Non-blocking, because a request that queues silently behind a twenty-minute
61: # transfer looks exactly like one that hung. Exit EXIT_LOCK_HELD (75) means
62: # "skipped: another sync is running" -- the UI names it, and no last-run stamp
63: # is written for work that did not happen.
64: #
65: # The descriptor is this shell's and nothing else's. A shell redirection
66: # carries no close-on-exec, so `exec 9>` hands fd 9 to every child the
67: # script starts, and rclone then holds the lock for the whole of a transfer
68: # (watched in /proc on the VM, #124). While the script outlives its
69: # children that is invisible, because bash waits for each of them before it
70: # exits. The moment it does not -- killed or orphaned while rclone is still
71: # copying, a child left in the background -- the lock outlives the run that
72: # took it and every sync afterwards is refused with "another cloud sync is
73: # running" when nothing is running at all. So the body runs with fd 9
74: # closed ("9>&-"): bash keeps the lock on a descriptor of its own, which it
75: # does mark close-on-exec, and nothing this script starts can see it.
76: #
77: # The refusal also waits a moment before saying no, as belt and braces for
78: # a holder this script does not own: a descriptor leaked by an older build,
79: # or a process in the act of exiting, frees itself in milliseconds, while a
80: # real concurrent transfer does not. One second of patience turns a raced
81: # skip into a run that works and costs a genuinely blocked run one second.
82: CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
83: take_cloud_lock() {
84:     local tries=0
85:     exec 9>"${CLOUD_SYNC_LOCK}"
86:     while ! flock -n 9; do
87:         if [ "${tries}" -ge 4 ]; then
88:             echo "Skipped: another cloud sync is already running. Try again when it's done."
89:             log_message "skipped: another cloud sync holds ${CLOUD_SYNC_LOCK}"
90:             exit "${EXIT_LOCK_HELD}"
91:         fi
92:         tries=$((tries + 1))
93:         sleep 0.25
94:     done
95: }
96: 
97: if [ ! -e "/storage/.config/rclone/rclone.conf" ]; then
98:     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
99:     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
100:     exit 1
101: fi
102: 
103: # The two values this script needs from cloud_sync.conf, read as text and
104: # never sourced (audit #307 PL-051's script half): a folder value an earlier
105: # build wrote with "$(...)" in it ran on every `source`. A CONTENT_REMOTE
106: # that carries a $, a backtick, a backslash or a control character is not a
107: # folder name, and the run refuses it rather than use it as a path.
108: #
109: # Read in the forms `source` reads (the audit of the fixes, G-A-06/G-A-02):
110: # the value double quoted, single quoted or bare; after it nothing, or
111: # blanks and a # comment. The first cut took only KEY=value or KEY="value"
112: # whole: a trailing comment or single quotes gave an empty CONTENT_REMOTE --
113: # the cloud's root -- where the folder had been, and the backup went there.
114: # A line it cannot read as plain text exits 2, and CONTENT_REMOTE's refuses
115: # the run; nothing is read as the root that did not say the root. Of two
116: # lines for one key, the first: every saves run EmulationStation starts is
117: # --yes, which runs cloud_sync_cleanup_duplicates.sh, which keeps the first,
118: # so that is the value the saves scripts run with and the file is left with.
119: #
120: # And a file with a control character but a tab anywhere in it is
121: # unreadable here as it is to the saves scripts' conf_valid (the audit of
122: # the fix round, PL-002): this reader never sources the file, but a blank
123: # is a space or a tab to both, so the tiers run with one reading of one
124: # file -- a carriage return after a value used to pass here as a blank.
125: #
126: # The key set in a form `source` reads and this does not -- indented,
127: # exported, declared, appended to, or with a blank before the = -- is
128: # unreadable, never absent (the audit of the fix round, lead G2-A-03):
129: # read as absent it was the cloud's root, and a content backup went there.
130: # The saves scripts' conf_valid refuses such a file whole.
131: conf_get() { # <KEY>: its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
132:     [ -f /storage/.config/cloud_sync.conf ] || return 0
133:     awk -v k="$1" '
134:         { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
135:         index($0, k "=") != 1 && !other \
136:             && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
137:         index($0, k "=") == 1 {
138:             s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
139:             c = substr(s, 1, 1)
140:             if (c == "\"") {
141:                 # Inside double quotes bash reads \" \\ \$ and \` as the one
142:                 # character each (PL-015), and so does this; an unescaped $
143:                 # or backtick is an expansion this reader does not make, and
144:                 # any other backslash is refused as conf_valid refuses it.
145:                 n = length(s); i = 2; closed = 0
146:                 while (i <= n) {
147:                     d = substr(s, i, 1)
148:                     if (d == "\"") { closed = 1; break }
149:                     if (d == "\\") {
150:                         e = substr(s, i + 1, 1)
151:                         if (e == "\"" || e == "\\" || e == "$" || e == "`") { v = v e; i += 2; continue }
152:                         ok = 0
153:                         why = (e == "") ? "a value continued onto the next line, which this reader does not follow" \
154:                                         : "a backslash inside double quotes that is not one of the escapes bash reads there"
155:                         break
156:                     }
157:                     if (d == "$" || d == "`") { ok = 0; why = "a $ or a backtick inside double quotes"; break }
158:                     v = v d; i++
159:                 }
160:                 if (ok && !closed) { ok = 0; why = "a double-quoted value that does not close on its line" }
161:                 if (ok) r = substr(s, i + 1)
162:             } else if (c == "'"'"'") {
163:                 j = index(substr(s, 2), c)
164:                 if (j) { v = substr(s, 2, j - 1); r = substr(s, j + 2) } else { ok = 0; why = "a single-quoted value that does not close on its line" }
165:             } else {
166:                 match(s, /^[A-Za-z0-9_.\/:@%+,=-]*/); v = substr(s, 1, RLENGTH); r = substr(s, RLENGTH + 1)
167:             }
168:             if (ok && r !~ /^([ \t]+(#.*)?)?$/) { ok = 0; why = "something after the value that is not a # comment" }
169:             if (!found) { found = 1; first = v; firstok = ok; firstwhy = "line " NR ": " why }
170:         }
171:         END {
172:             if (cntrl) { print "line " cntrl ": a control character other than a tab"; exit 2 }
173:             if (other) { print "line " other ": " k " set in a form this reader does not read"; exit 2 }
174:             if (found && !firstok) { print firstwhy; exit 2 }
175:             if (found) print first
176:         }
177:     ' /storage/.config/cloud_sync.conf
178: }
179: if ! CONTENT_REMOTE=$(conf_get CONTENT_REMOTE); then
180:     # On a refusal conf_get says why, for the log: the line and its shape,
181:     # never the value (PL-015).
182:     log_message "cloud_sync.conf was not read: ${CONTENT_REMOTE}"
183:     echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
184:     echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
185:     exit 1
186: fi
187: # The bound falls back to the shipped value below when this is empty; a
188: # line it cannot read is that too, and the log says so.
189: if ! RCLONE_NET_OPTS=$(conf_get RCLONE_NET_OPTS); then
190:     log_message "RCLONE_NET_OPTS was not read (${RCLONE_NET_OPTS}); the shipped bound stands in"
191:     RCLONE_NET_OPTS=""
192: fi
193: case "${CONTENT_REMOTE}" in
194:     *[\$\`\\]*|*[[:cntrl:]]*)
195:         echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
196:         echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
197:         exit 1 ;;
198: esac
199: 
200: REMOTENAME=$(rclone listremotes | head -1)
201: if [ -z "${REMOTENAME}" ]; then
202:     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
203:     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
204:     exit 1
205: fi
206: 
207: ROOT="${REMOTENAME}${CONTENT_REMOTE:+${CONTENT_REMOTE}/}"
208: LEGACY_ROOT="${REMOTENAME}"
209: 
210: # The bound on every rclone command below that opens a socket: RCLONE_NET_OPTS
211: # from cloud_sync.conf, or the same shipped values when the config has no
212: # such line yet -- this script reads the config without running
213: # cloud_sync_helper, so on the first run after an update it may not, and the
214: # bound is a guard that a missing line must not switch off. The reasoning
215: # for the numbers is beside the option in cloud_sync.conf.defaults; the
216: # short version is that rclone's own defaults (60 s connect, 5 min idle, 10
217: # low-level retries, 3 whole-run retries) hold a run for over ten minutes
218: # on a link that drops mid-run (#101, #102, #103). Keep the fallback in step
219: # with the default. The two rclone calls that touch only this device --
220: # `rclone size` and `rclone delete` on a local folder in the match flow --
221: # open no socket and carry none of this.
222: RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
223: _net_opts=$(echo "${RCLONE_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
224: [ -n "${_net_opts}" ] || _net_opts="${RCLONE_NET_OPTS_FALLBACK}"
225: read -r -a RCLONE_NET_OPTS_ARRAY <<< "${_net_opts}"
226: # Installed beside this script, also when the host fixtures copy it.
227: . "$(dirname "${BASH_SOURCE[0]}")/cloud_content_transfer" || exit 1
228: # A probe is a single listing that exists to answer quickly: one attempt,
229: # tighter than the transfers (the same values the saves scripts probe with).
230: readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
231: # A listing's bound (#143): three low-level retries, not a transfer's ten --
232: # rclone's S3 backend hands the count to the AWS SDK as attempts with
233: # exponential backoff (see cloud_backup for the measurement).
234: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
235: 
236: # Whole or not at all: to a temporary name beside the stamp, then renamed
237: # over it, as ThreadedCloudSync::recordOutcome does. A kill mid-write leaves
238: # the previous stamp; it used to leave an empty file (D-CLOUD-078, #105).
239: # LAST_WHY, when a `>>> why` line was printed, becomes the stamp's third
240: # field as a token (spaces to underscores) for the row to read (D-UI-028).
241: LAST_WHY=""
242: write_stamp() {
243:     local file="$1" line="$2" tmp
244:     mkdir -p "$(dirname "${file}")" 2>/dev/null
245:     tmp="${file}.tmp.$$"
246:     { printf '%s\n' "${line}" > "${tmp}"; } 2>/dev/null \
247:         && mv -f "${tmp}" "${file}" 2>/dev/null \
248:         || rm -f "${tmp}" 2>/dev/null
249: }
250: record_outcome() { # <stamp-name> <rc>
251:     local why=""
252:     case "$2" in
253:         0|9|"${EXIT_NO_NETWORK}"|"${EXIT_LOCK_HELD}") ;;
254:         *) [ -n "${LAST_WHY}" ] && why=" $(printf '%s' "${LAST_WHY}" | tr ' ' '_')" ;;
255:     esac
256:     write_stamp "/storage/.cache/cloud_sync/last-$1" "$(date +%s) $2${why}"
257: }
258: 
259: # Why a unit did not finish, in the player's words (D-UI-028, D-CLOUD-077):
260: # one `>>> why <SENTENCE>` protocol line per failing unit, which the page
261: # and the card read; rclone's code stays in the log. The sentences are the
262: # vocabulary table's in es-native-ui.md.
263: say_why() {
264:     LAST_WHY="$1"
265:     echo ">>> why $1"
266:     log_message "why: $1"
267: }
268: why_for() {
269:     case "$1" in
270:         3|4) echo "COULDN'T FIND YOUR CLOUD FOLDER" ;;
271:         5|124) echo "YOUR CLOUD STOPPED ANSWERING" ;;
272:         6)   echo "SOME FILES DIDN'T FINISH" ;;
273:         7|8) echo "YOUR CLOUD WOULDN'T TAKE THE FILES" ;;
274:         130) echo "IT WAS STOPPED" ;;
275:         *)   echo "SOMETHING WENT WRONG" ;;
276:     esac
277: }
278: 
279: has_default_route() {
280:     ip -4 route show default 2>/dev/null | grep -q . \
281:         || ip -6 route show default 2>/dev/null | grep -q .
282: }
283: 
284: # Is the network gone? Asked after rclone failed, so the run can say why it
285: # ended rather than hand up a code that reads as FAILED and sends somebody
286: # to a log. Gone: no default route, or a route through which neither the
287: # remote nor anything else answers a bounded probe. Not gone: the remote
288: # answers again (a blip rclone did not survive), or the internet answers
289: # while the remote does not (the provider, or the sign-in) -- that is
290: # rclone's failure to report, and the caller passes rclone's code through
291: # as before. The same three questions cloud_backup asks (#101, #103).
292: network_gone() {
293:     has_default_route || return 0
294:     rclone lsd "${REMOTENAME}" "${RCLONE_PROBE_OPTS[@]}" >/dev/null 2>&1 && return 1
295:     ping -q -c1 -W 3 1.1.1.1 >/dev/null 2>&1 && return 1
296:     ping -q -c1 -W 3 8.8.8.8 >/dev/null 2>&1 && return 1
297:     return 0
298: }
299: 
300: # The network went away under a running unit. Says so, records that the run
301: # did not complete -- never a 0, which would read as a restore that happened
302: # -- under the stamp the action keeps (last-content-restore, or
303: # last-content-match for --match --apply), and exits EXIT_NO_NETWORK, which
304: # EmulationStation names (SKIPPED - NO NETWORK CONNECTION on the card,
305: # SKIPPED, NO NETWORK on the row). No further unit is attempted: each would
306: # stall for another minute against the same dead link. rclone copy and sync
307: # write each file under a temporary name and rename it when complete, so
308: # nothing partial is left on the card; a match's deletions had already
309: # happened when the sync ran, and they are final -- a match removes only
310: # what the cloud does not have (D-CLOUD-023; #308 gpt F-CS-26: this said
311: # the cloud still held them).
312: #
313: # SKIPPED means nothing was touched (#308 claude F-CS-24): when something had
314: # already moved -- a unit completed, a match removed files -- before the
315: # network went, the stamp still carries 69 and adds the gaps token and a why,
316: # "<epoch> 69 gaps YOU WENT OFFLINE PART-WAY THROUGH", which the rows read as
317: # COULDN'T FINISH (CloudText::parseLastRun takes the token before the code).
318: # The exit stays 69; the page reads a 69 after progress the same way.
319: # Did this run's rclone move a file since <offset> into the log? Progress,
320: # for the stamp stop_no_network writes, is what rclone logged moving --
321: # "<path>: Copied (...)", "Moved (...)", "Deleted" -- not a unit that
322: # completed (the audit of the fixes, G-A-08/G-A-13): files a unit moved
323: # before its own failure did not count, and a unit that moved nothing did.
324: # Every transfer here logs at INFO to LOG_FILE, and the transfer lock
325: # keeps any other cloud script from writing it meanwhile.
326: log_offset() { stat -c %s "${LOG_FILE}" 2>/dev/null || echo 0; }
327: moved_since() { # <byte offset into LOG_FILE>
328:     local now
329:     now=$(stat -c %s "${LOG_FILE}" 2>/dev/null) || return 1
330:     [ "${now}" -gt "$1" ] 2>/dev/null || return 1
331:     tail -c +$(( $1 + 1 )) "${LOG_FILE}" 2>/dev/null | grep -qE ': (Copied|Moved) \(|: Deleted$'
332: }
333: PROGRESS_MADE=0
334: stop_no_network() {
335:     local stamp="$1" rc="$2" doing="$3"
336:     echo "Couldn't finish: lost the network while ${doing}. Try again when you're online."
337:     log_message "stopped: the network went away while ${doing} (rclone exit ${rc}); exit ${EXIT_NO_NETWORK}"
338:     if [ "${PROGRESS_MADE}" = 1 ]; then
339:         write_stamp "/storage/.cache/cloud_sync/last-content-${stamp}" "$(date +%s) ${EXIT_NO_NETWORK} gaps YOU WENT OFFLINE PART-WAY THROUGH"
340:     else
341:         record_outcome "content-${stamp}" "${EXIT_NO_NETWORK}"
342:     fi
343:     exit "${EXIT_NO_NETWORK}"
344: }
345: 
346: # Read the old shape, write the new one.
347: #
348: # CONTENT_REMOTE is newer than content sync itself. Before it existed, content
349: # sat at the remote root, and an upgraded device would look in the new place,
350: # find nothing, and simply show an empty list - the player never chose a
351: # layout, so there is nothing for them to reason about, and nobody reads
352: # release notes on a handheld.
353: #
354: # So restore looks in the configured location and falls back to the old one.
355: # Backups always write to the configured location, so a library migrates by
356: # itself the next time it is backed up, with no prompt and no migration step.
357: # The legacy root on a path-based remote is the whole account, which holds the
358: # owner's own folders too. Only directories this device actually has locally
359: # are offered from there - listing somebody's holiday photos as restorable ROMs
360: # would be worse than the empty list this fixes.
361: legacy_dirs() {
362:     local d base
363:     for d in "${DEST}"/*/; do
364:         [ -d "${d}" ] || continue
365:         base=$(basename "${d}")
366:         case "${base}" in savefiles|savestates|screenshots|backup) continue ;; esac
367:         echo "${base}"
368:     done
369: }
370: 
371: # Where a local directory lives in the current cloud layout.
372: #
373: # ROMs and BIOS are named folders rather than a mirror of /storage/roms,
374: # because the person filling them in is looking at a file manager on a
375: # computer, where "bios sitting beside snes" is an accident of how a handheld
376: # stores things. The local name is what everything else here uses, so the
377: # mapping stays in one place: bios lives under BIOS, everything else under
378: # ROMs.
379: remote_for() {
380:     case "$1" in
381:         bios) echo "${ROOT}BIOS" ;;
382:         *)    echo "${ROOT}ROMs/$1" ;;
383:     esac
384: }
385: 
386: # Returns the full remote path that actually holds this directory.
387: #
388: # Three shapes are in the field and all of them have to keep working:
389: #
390: #   1. ROMs/<system> and BIOS      -- current
391: #   2. <system> and bios, flat under CONTENT_REMOTE  -- what shipped before this
392: #   3. <system> at the remote root -- before CONTENT_REMOTE existed at all
393: #
394: # Read all three, write only the first (cloud_content_backup). A library then
395: # migrates itself the next time it is backed up: nothing to prompt about,
396: # nothing to explain, and a device that has not updated yet still finds its
397: # content where it left it.
398: #
399: # The legacy root on a path-based remote is the whole account, which holds the
400: # owner's own folders too. Only directories this device actually has locally
401: # are offered from there - listing somebody's holiday photos as restorable ROMs
402: # would be worse than the empty list this fixes.
403: resolve_src() {
404:     local dir="$1" new
405:     new="$(remote_for "${dir}")"
406:     if exists_remote "${new}"; then
407:         echo "${new}"
408:     elif rclone lsf --dirs-only "${ROOT}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | sed 's:/$::' | grep -qx "${dir}"; then
409:         log_message "Content \"${dir}\" found in the flat pre-ROMs layout"
410:         echo "${ROOT}${dir}"
411:     elif [ -n "${CONTENT_REMOTE}" ] && legacy_dirs | grep -qx "${dir}" \
412:          && rclone lsf --dirs-only "${LEGACY_ROOT}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | sed 's:/$::' | grep -qx "${dir}"; then
413:         log_message "Content \"${dir}\" found at the pre-CONTENT_REMOTE location"
414:         echo "${LEGACY_ROOT}${dir}"
415:     else
416:         echo "${new}"
417:     fi
418: }
419: 
420: # Does a remote path exist?
421: #
422: # NOT `rclone lsjson --stat`, which is what this used to be. On bucket-based
423: # remotes (S3, B2, Minio) stat synthesises a directory entry for *any* path --
424: # verified against Minio on rclone 1.60 and 1.74, where
425: # "utterly-bogus-never-created" reports success with IsDir true. So it can
426: # never report absence there, and every caller that branched on it took the
427: # "exists" path unconditionally.
428: #
429: # A listing can report absence. Two questions, because a directory can be real
430: # without holding files: does it contain anything, or does its parent list it
431: # (which is what an --s3-directory-markers marker object produces)?
432: exists_remote() {
433:     [ -n "$(rclone lsf "$1" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | head -1)" ] && return 0
434:     local parent name
435:     parent="${1%/}"; name="${parent##*/}"; parent="${parent%/*}"
436:     [ -n "${name}" ] || return 1
437:     rclone lsf --dirs-only "${parent}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -qx "${name}/"
438: }
439: 
440: # Is this remote path missing, rather than unreadable? rclone answers "not
441: # found" (exit 3) when the server's reply is the one it maps to that, and a
442: # plain error (exit 1) when the words differ: an FTP server that answers a
443: # missing folder with 501 "No such directory." where the standard reply is
444: # 550 makes every "is it there yet?" branch read as "the cloud is broken"
445: # (#142, from the #133 matrix). The parent settles it, whatever the words:
446: # walk up until a level lists. A level that lists and lacks the next name is
447: # a path not created yet (0); one that lists and holds it means the failure
448: # was something else (1); a remote whose root will not list is broken (1).
449: # On a bucket an absent prefix lists as empty, which is the same answer
450: # (D-CLOUD-120). Called only after a listing has already failed with a code
451: # other than 3, so the everyday path costs nothing extra.
452: absent_not_broken() {
453:     local path="${1%/}" remote rel name parent listing
454:     remote="${path%%:*}:"; rel="${path#*:}"; rel="${rel#/}"
455:     while [ -n "${rel}" ]; do
456:         name="${rel##*/}"; parent="${rel%/*}"
457:         [ "${parent}" = "${rel}" ] && parent=""
458:         if listing=$(rclone lsf --dirs-only "${remote}/${parent:+${parent}/}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); then
459:             printf '%s\n' "${listing}" | grep -qFx -- "${name}/" && return 1
460:             return 0
461:         fi
462:         [ -n "${parent}" ] || return 1
463:         rel="${parent}"
464:     done
465:     return 1
466: }
467: 
468: # Which systems this device syncs.
469: #
470: # One cloud library, many handhelds, and they are not interchangeable: an H700
471: # cannot run GameCube, and a 3:2 panel makes a device a Game Boy Advance
472: # machine by preference rather than by limit. So the set is a per-device
473: # choice.
474: #
475: # Kept in /storage/.cache, deliberately. The obvious homes -- cloud_sync.conf,
476: # or ES's system.cfg -- are both captured by the settings backup, and restoring
477: # one device's selection onto another would silently change what that device
478: # syncs. That is the same defect shape as the CONTENT_REMOTE split (6717e0b348),
479: # and once was enough.
480: #
481: # No file means no selection means everything, so a device that has never
482: # opened the picker behaves exactly as it did before.
483: SELECTION="/storage/.cache/cloud_sync/content-systems"
484: 
485: # Only a system folder's name is ever acted on (audit #307 PL-030):
486: # --set-systems refuses any other since that change, and a selection an
487: # earlier build wrote without the check is read past a line that is not
488: # one, never with it.
489: selected_systems() {
490:     [ -r "${SELECTION}" ] || return 0
491:     grep -E '^[A-Za-z0-9_][A-Za-z0-9._-]*$' "${SELECTION}" 2>/dev/null
492: }
493: 
494: # The systems this image can actually run, from its own EmulationStation
495: # config. Matched on <path>, not <name>: they differ for a dozen systems and
496: # matching names silently mislabels those as unsupported.
497: es_systems_file() {
498:     for c in /storage/.config/emulationstation/es_systems.cfg \
499:              /usr/config/emulationstation/es_systems.cfg; do
500:         [ -r "${c}" ] && { echo "${c}"; return 0; }
501:     done
502: }
503: 
504: supported_systems() {
505:     local c; c=$(es_systems_file)
506:     [ -n "${c}" ] || return 0
507:     sed -n 's:.*<path>/storage/roms/\([^</]*\).*:\1:p' "${c}" | sort -u
508: }
509: 
510: # Total bytes per top-level directory, from ONE recursive listing.
511: #
512: # rclone size per system would be one API round trip each, which on a library
513: # of thirty systems is thirty waits before the player sees anything. lsf
514: # --format sp returns size and path for every file in a single call; summing
515: # them here costs nothing.
516: sizes_under() {
517:     rclone lsf -R --files-only --format "sp" --separator "|" "$1" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null \
518:         | grep -v '|README\.txt$' \
519:         | awk -F'|' '{ i = index($2, "/"); if (i == 0) next;
520:                        d = substr($2, 1, i - 1); sz[d] += $1 }
521:                      END { for (d in sz) print d "|" sz[d] }'
522: }
523: 
524: 
525: # --- make this device match the cloud ------------------------------------
526: #
527: # Backup and restore are both copy-only, deliberately, so a system removed
528: # from the cloud stays on the device forever and a card can never be made to
529: # match the library. This is the third action, and the only one here that
530: # deletes.
531: #
532: # Five rules, each of which has already cost something in this subsystem:
533: #
534: #  1. --delete-excluded NEVER appears. Save files live inside system
535: #     directories; with the excludes in place rclone leaves excluded
536: #     destination files alone, and that one flag inverts it into a save wipe.
537: #  2. Only ROMs/<selected system> and BIOS. /storage/roms also holds
538: #     savefiles, savestates, screenshots, backup, bezels, themes and music --
539: #     other tiers' or nobody's.
540: #  3. An empty or failed listing must never mean "delete everything". A wifi
541: #     drop, a lapsed token and a renamed cloud folder all look exactly like an
542: #     empty cloud, so the content root is positively confirmed to hold
543: #     something before any deletion is considered.
544: #  4. Cloud -> device only. The mirror direction is what deleted another
545: #     handheld's whole save library on 2026-09-01 (D-CLOUD-014).
546: #  5. Saves survive a removed system. Its content goes; the .srm and .state
547: #     files stay, leaving the directory holding only those -- which
548: #     has_content() correctly reports as no content.
549: #
550: # Deletions are final on the device: no local backup-dir. The space reclaimed
551: # is the entire point of syncing ROMs selectively, and the cloud is the backup
552: # by definition, since this only ever removes what the cloud does not have
553: # (D-CLOUD-023). Preview first, then apply.
554: 
555: # Defined here, above every consumer.
556: #
557: # They used to sit below the case statement, which was fine while the only
558: # consumer was the transfer loop at the end of the file -- and silently
559: # catastrophic the moment --match started calling them from inside the case.
560: # Bash expands an unset array to nothing, so rclone ran with no save
561: # excludes at all and a match would have deleted .srm and .state files. It
562: # was invisible in the output: fewer exclusions simply means more deletions,
563: # and the preview reported them as ordinary work.
564: 
565: # What the saves tier owns, and content must never carry.
566: #
567: # A system directory holds more than games: RetroArch writes .srm and .state
568: # next to the ROM, and several systems keep memory cards in a subfolder. The
569: # saves allowlist claims all of it ("+ /**/*.srm" and friends in
570: # cloud_sync-rules.txt), so uploading a system folder wholesale puts saves
571: # in a second cloud location under different rules -- two writers and no
572: # reconciliation, which is exactly how 70 files were deleted on 2026-09-01.
573: #
574: # Worse in the other direction: a content restore would then copy stale saves
575: # back over live ones.
576: #
577: # The earlier allowlist fix (d77d4ea44d) covered directories another tier
578: # owns. This is the same rule one level down, for files. Kept in step with
579: # cloud_sync-rules.txt by hand -- there is no shared parser, and a pattern
580: # added there must be added here. .fla was added there (#89, N64's flash
581: # saves beside the ROM) and not here, so a content backup uploaded it and
582: # a match removed it as content (the audit's gpt F-CS-02).
583: SAVE_EXCLUDES=(
584:     --exclude "*.srm" --exclude "*.sav" --exclude "*.fs"
585:     --exclude "*.state*" --exclude "*.auto" --exclude "*.dsv*"
586:     --exclude "*.eep" --exclude "*.mpk" --exclude "*.sra" --exclude "*.fla"
587:     --exclude "*.mcd" --exclude "*.mcr"
588:     --exclude "save/**" --exclude "memcards/**"
589:     --exclude "shared/savefiles/**" --exclude "PPSSPP/**"
590: )
591: 
592: # Another sync client's unresolved dispute is not our content.
593: #
594: # Dropbox and Nextcloud rename the losing side of a concurrent write to
595: # "X (Someone's conflicted copy 2026-09-03)"; Syncthing appends
596: # ".sync-conflict-<date>". Carrying those onto a handheld doubles the storage
597: # for no benefit -- the player cannot resolve a conflict from a games menu --
598: # and it makes the artifacts immortal: a device that downloaded them uploads
599: # them again on the next backup, so deleting them in the cloud looks like the
600: # provider putting them back. That happened here, to 271 directories of BIOS
601: # (2026-09-04).
602: #
603: # Resolution belongs on the computer where both sides can be seen. We decline
604: # to move them in either direction, which is also the only way a cleanup on
605: # one side stays done.
606: CONFLICT_EXCLUDES=(
607:     --exclude "**conflicted copy**"
608:     --exclude "**.sync-conflict-**"
609:     --exclude "*.????????.partial"
610: )
611: 
612: # gamelist.xml travels on its own terms.
613: #
614: # It is the scraping payload -- names, descriptions, genres, ratings, media
615: # paths and the cheevos hashes that cost a hash of every ROM -- and all of that
616: # is device-independent, so sharing it means scraping once rather than once per
617: # handheld. Paths inside it are relative ("./Mega Man 3 (USA).zip"), so it
618: # carries across devices unchanged.
619: #
620: # It degrades well in both directions, which is why this is safe at all:
621: #
622: #   * Reading, EmulationStation builds its list from the filesystem first and
623: #     skips any entry whose ROM is absent ("does not exist ... Ignoring"), so a
624: #     52-entry list on a handheld holding 10 of those games shows 10 games and
625: #     no phantoms. That holds while ParseGamelistOnly is false, which is the
626: #     default.
627: #   * Writing, updateGamelist re-reads the file and rewrites only the entries
628: #     whose metadata changed, preserving entries for ROMs this device does not
629: #     have -- deliberately, per its own comment.
630: #
631: # What neither of those protects against is rclone, which replaces a file
632: # wholesale. A device that scans its own ROMs and uploads before it has ever
633: # restored would push a thin list over a rich one. That is an ordering problem,
634: # not a merge problem, and --update solves it: skip when the destination is
635: # newer, so the freshest list wins rather than the last writer.
636: #
637: # Hence a separate pass. --update on the whole content transfer would also
638: # apply to ROMs, where "destination is newer" is not a reason to skip a file
639: # somebody deliberately re-uploaded.
640: #
641: # Three fields remain genuinely per-device -- playcount, lastplayed and
642: # gametime, which EmulationStation itself marks isStatistic and refuses to let
643: # a scrape overwrite. A file-level sync cannot make that distinction, so those
644: # are last-writer-wins across devices. Everything else in the file is authored
645: # or scraped, and favorite is explicitly not a statistic in ES's model.
646: GAMELIST_ONLY=( --include "gamelist.xml" --include "**/gamelist.xml" )
647: 
648: # What EmulationStation owns, which a content match must never delete.
649: #
650: # gamelist.xml carries <playcount>, <lastplayed> and <favorite> -- per-device
651: # facts that exist nowhere else -- and images/, videos/ and manuals/ hold
652: # scraped artwork that can represent hours of scraping. None of it is content
653: # the cloud is authoritative about, so "the cloud does not have it" is not a
654: # reason to remove it.
655: #
656: # Found the only way these things are ever found: reading a real dry run,
657: # which listed "gamelist.xml: Skipped delete" for every system on the device.
658: #
659: # Deliberately scoped to the match path. Whether backup should *upload* a
660: # gamelist is a separate and open question (#61) -- but deleting one locally
661: # is wrong under every answer to it.
662: METADATA_EXCLUDES=(
663:     --exclude "gamelist.xml"
664:     --exclude "**/gamelist.xml"
665:     --exclude "images/**"
666:     --exclude "videos/**"
667:     --exclude "manuals/**"
668:     --exclude "magazines/**"
669:     --exclude "media/**"
670: )
671: 
672: # rclone reports sizes in a NOTICE line using human units ("6.090Ki", "64Ki")
673: # when the destination is local, and bare bytes for a small local-to-local
674: # copy. Parsing only digits silently produced zero for every real transfer.
675: to_bytes() {
676:     awk '{ n = $0 + 0; u = $0; gsub(/[0-9.]/, "", u)
677:            if (u == "Ki") n *= 1024
678:            else if (u == "Mi") n *= 1048576
679:            else if (u == "Gi") n *= 1073741824
680:            else if (u == "Ti") n *= 1099511627776
681:            printf "%d\n", n }'
682: }
683: 
684: # Does the content root actually hold anything? Rule 3.
685: cloud_root_populated() {
686:     local n
687:     n=$(rclone lsf --dirs-only "${ROOT}ROMs/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -c . )
688:     [ "${n}" -gt 0 ] && return 0
689:     rclone lsf --files-only "${ROOT}BIOS/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -q . && return 0
690:     return 1
691: }
692: 
693: # What one system would gain and lose. Prints "<sys>|<verb>|<files>|<bytes>",
694: # or "<sys>|fail|<rclone exit>|0" when it cannot be told.
695: #
696: # The counting uses rclone against the local path with the very same exclude
697: # arrays the transfer uses, rather than a second hand-written find predicate:
698: # a deletion predicate that can drift from the transfer predicate is how saves
699: # get deleted by a tool that believes it is only touching ROMs.
700: #
701: # Absent is something the cloud says, never something a failure implies
702: # (rule 3, audit #307 PL-001). The system's listing is read apart from its
703: # emptiness: exit 0 with nothing listed, or rclone's 3/4 ("not found"), is a
704: # system the cloud does not have. Any other exit -- a 429 after rclone's own
705: # retries, the link dropping between two calls -- is asked of the parent
706: # (absent_not_broken, #142's walk, for a server whose "missing" rclone does
707: # not map to 3); a parent that lists the system, or will not list at all,
708: # makes the answer "could not tell", and a system that cannot be told is
709: # neither planned nor touched. The listing used to be `lsf | grep -q .`,
710: # which read a failed call as an empty folder and planned `remove`; apply
711: # then deleted the whole system on a transient error. The dry run and the
712: # local count are read the same way: a count that failed is not a zero.
713: match_plan_one() {
714:     local sys="$1" src local_dir n b out listing lrc
715:     src="$(remote_for "${sys}")"
716:     local_dir="${DEST}/${sys}"
717: 
718:     [ -d "${local_dir}" ] || { printf '%s|none|0|0\n' "${sys}"; return 0; }
719: 
720:     listing=$(rclone lsf "${src}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); lrc=$?
721:     case "${lrc}" in
722:         0|3|4) ;;
723:         *)
724:             if absent_not_broken "${src}"; then
725:                 log_message "match: ${sys} listing failed (rclone exit ${lrc}); its parent lists and lacks it, so it is absent"
726:                 lrc=3
727:             else
728:                 log_message "match: ${sys} could not be listed (rclone exit ${lrc}); not planned"
729:                 printf '%s|fail|%s|0\n' "${sys}" "${lrc}"
730:                 return 0
731:             fi ;;
732:     esac
733: 
734:     if [ "${lrc}" -eq 0 ] && [ -n "${listing}" ]; then
735:         # Present in the cloud: sync reconciles both directions of difference.
736:         out=$(bounded_content_rclone sync "${src}" "${local_dir}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
737:                 "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
738:                 --dry-run --stats 0 2>&1)
739:         lrc=$?
740:         if [ "${lrc}" -ne 0 ]; then
741:             log_message "match: ${sys} dry run failed (rclone exit ${lrc}); not planned"
742:             printf '%s|fail|%s|0\n' "${sys}" "${lrc}"
743:             return 0
744:         fi
745:         # "NOTICE: Game3.zip: Skipped delete as --dry-run is set (size 5)" --
746:         # the exact wording on rclone 1.75.0, read off the real output rather
747:         # than taken from the documentation. The size in the tail is what lets
748:         # the confirmation say how much space comes back.
749:         n=$(printf '%s\n' "${out}" | grep -c "Skipped delete")
750:         b=$(printf '%s\n' "${out}" | sed -n 's/.*Skipped delete.*(size \([0-9.KMGTi]*\)).*/\1/p' \
751:               | to_bytes | awk '{ t += $1 } END { print t+0 }')
752:         printf '%s|sync|%s|%s\n' "${sys}" "${n}" "${b}"
753:     else
754:         # Absent from the cloud entirely: its content goes, its saves stay.
755:         out=$(rclone size "${local_dir}" \
756:                 "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" 2>/dev/null)
757:         lrc=$?
758:         n=$(printf '%s\n' "${out}" | sed -n 's/^Total objects: *\([0-9]*\).*/\1/p' | head -1)
759:         b=$(printf '%s\n' "${out}" | sed -n 's/^Total size: .*(\([0-9]*\) Byte).*/\1/p' | head -1)
760:         if [ "${lrc}" -ne 0 ] || [ -z "${n}" ]; then
761:             log_message "match: ${sys} could not be counted on this device (rclone exit ${lrc}); not planned"
762:             printf '%s|fail|%s|0\n' "${sys}" "${lrc}"
763:             return 0
764:         fi
765:         [ -n "${b}" ] || b=0
766:         [ "${n}" -eq 0 ] && { printf '%s|none|0|0\n' "${sys}"; return 0; }
767:         printf '%s|remove|%s|%s\n' "${sys}" "${n}" "${b}"
768:     fi
769: }
770: 
771: # The saves restore's record that the tree under it holds no leftover of a
772: # cut transfer (cloud_restore's PARTIALS_CLEAN, #308 claude F-CS-08): this
773: # script writes into the same tree, so it takes the record down while it
774: # writes and puts it back only when it ended by itself with nothing of its
775: # own left over -- a failed unit's folder is swept for rclone's
776: # <name>.<8>.partial before that. A run of this cut part-way leaves the
777: # record down, and the next saves restore walks the tree (the audit of the
778: # fixes, claude G-A-07: the record said clean across a content restore
779: # that was cut, and the next content backup sent the leftover as a ROM).
780: TREE_CLEAN=/storage/.cache/cloud_sync/restore-tree-clean
781: TREE_CLEAN_AT_START=0
782: tree_record_take() { [ -e "${TREE_CLEAN}" ] && TREE_CLEAN_AT_START=1; rm -f "${TREE_CLEAN}" 2>/dev/null; }
783: tree_record_give() { [ "${TREE_CLEAN_AT_START}" = 1 ] && : > "${TREE_CLEAN}" 2>/dev/null; return 0; }
784: sweep_partials() { [ -d "$1" ] || return 0; find "$1" -type f -name '*.????????.partial' -exec rm -f {} + 2>/dev/null; }
785: 
786: # The plan the player agreed to (audit #307 PL-001, F-CS-03). The preview
787: # writes one line per system it checked -- "<sys>|<verb>|<files>|<bytes>",
788: # none included -- under a header naming the moment, whole or not at all,
789: # and only when every system could be told; apply reads it and holds each
790: # system to it: the same verb, no more to remove than the preview counted,
791: # and that count, not its own, is --max-delete. A system the plan does not
792: # name, or whose verb changed since, is refused rather than recomputed and
793: # run. The plan is spent by the apply that reads it, so each apply stands on
794: # the preview that immediately led to it. Device-local, under /storage/.cache
795: # like the stamps: a plan restored onto another device would describe
796: # another card.
797: MATCH_PLAN="/storage/.cache/cloud_sync/content-match-plan"
798: match_plan_write() { # <plan lines>
799:     mkdir -p "$(dirname "${MATCH_PLAN}")" 2>/dev/null
800:     { printf 'plan %s\n' "$(date +%s)"; printf '%s\n' "$1" | grep '|'; } > "${MATCH_PLAN}.tmp.$$" 2>/dev/null \
801:         && mv -f "${MATCH_PLAN}.tmp.$$" "${MATCH_PLAN}" 2>/dev/null \
802:         || { rm -f "${MATCH_PLAN}.tmp.$$" 2>/dev/null; return 1; }
803: }
804: match_plan_of() { # <sys>: its line from the plan, or nothing
805:     [ -n "${MATCH_PLAN_TEXT}" ] || return 1
806:     printf '%s\n' "${MATCH_PLAN_TEXT}" | awk -F'|' -v s="$1" '$1 == s { print; exit }'
807: }
808: 
809: # What a match removed, as rclone reports it (#308 gpt F-CS-26). Before a
810: # system runs, its content files are listed with their sizes by the same
811: # excludes the run uses; its rclone writes a log of its own, whose
812: # "<path>: Deleted" lines name what went; the count and the bytes are
813: # those names looked up in the list, added to the run's totals. The log is
814: # then appended to the script's own.
815: MATCH_LOG=""
816: MATCH_BEFORE=""
817: match_before() { # <sys>
818:     MATCH_LOG=$(mktemp /tmp/cloud-match-log.XXXXXX 2>/dev/null) || MATCH_LOG="/tmp/cloud-match-log.$$"
819:     MATCH_BEFORE=$(mktemp /tmp/cloud-match-before.XXXXXX 2>/dev/null) || MATCH_BEFORE="/tmp/cloud-match-before.$$"
820:     : > "${MATCH_LOG}"
821:     rclone lsf -R --files-only --format "sp" --separator "|" "${DEST}/$1" \
822:         "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" > "${MATCH_BEFORE}" 2>/dev/null
823: }
824: match_count() { # <sys>: adds what the log says went to the totals
825:     local counted cfiles cbytes
826:     counted=$(awk -F'|' -v L="${MATCH_BEFORE}" '
827:         BEGIN { while ((getline x < L) > 0) { i = index(x, "|"); sz[substr(x, i + 1)] = substr(x, 1, i - 1) } }
828:         / : .*: Deleted$/ { p = $0; sub(/^.* : /, "", p); sub(/: Deleted$/, "", p); n++; b += sz[p] }
829:         END { print n + 0 "|" b + 0 }' "${MATCH_LOG}" 2>/dev/null)
830:     IFS='|' read -r cfiles cbytes <<< "${counted:-0|0}"
831:     [ "${cfiles}" -gt 0 ] 2>/dev/null && PROGRESS_MADE=1
832:     # A sync's copies down are progress too (G-A-08).
833:     grep -qE ': (Copied|Moved) \(' "${MATCH_LOG}" 2>/dev/null && PROGRESS_MADE=1
834:     total_removed=$((total_removed + cfiles))
835:     total_bytes=$((total_bytes + cbytes))
836:     removed_detail="${removed_detail}${removed_detail:+,}$1:${cfiles}:${cbytes}"
837:     cat "${MATCH_LOG}" >> "${LOG_FILE}" 2>/dev/null
838:     rm -f "${MATCH_LOG}" "${MATCH_BEFORE}"
839: }
840: 
841: match_run() {
842:     local apply="$1" sys line verb files bytes rc=0 sync_rc=0 del_rc=0 total_removed=0
843: 
844:     # The exclusions are the only thing standing between this and somebody's
845:     # saves, so assert they exist rather than trusting the file's layout. An
846:     # unset array expands to nothing and rclone would happily proceed.
847:     if [ ${#SAVE_EXCLUDES[@]} -eq 0 ] || [ ${#METADATA_EXCLUDES[@]} -eq 0 ]; then
848:         echo "Refusing: the rules that keep your saves safe aren't loaded."
849:         log_message "match: refused, exclusion arrays empty"
850:         return 1
851:     fi
852: 
853:     # The preview is read-only and may run beside a transfer; applying is one.
854:     [ "${apply}" = "1" ] && take_cloud_lock
855:     # As at the foot of the script: the rest of the run cannot leak the
856:     # lock into rclone. Closing a descriptor that was never opened (the
857:     # preview, which takes no lock) is a no-op.
858:     {
859: 
860:     if ! cloud_root_populated; then
861:         echo "Refusing to change anything: your cloud's ROMs and BIOS folder looks empty."
862:         echo "That looks the same whether it really is empty, you're offline, or the"
863:         echo "folder was renamed - so nothing is removed."
864:         log_message "match: refused, content root lists nothing"
865:         # One of the three it can tell apart: with the network gone the
866:         # refusal is the no-network skip, and says so with the code
867:         # EmulationStation names. Nothing ran, so no stamp.
868:         if network_gone; then
869:             echo "Skipped: there's no network connection. Try again when you're online."
870:             log_message "match: skipped, no network"
871:             exit "${EXIT_NO_NETWORK}"
872:         fi
873:         return 1
874:     fi
875: 
876:     mapfile -t SYS < <(selected_systems)
877:     if [ ${#SYS[@]} -eq 0 ]; then
878:         echo "You haven't picked any systems for this device yet."
879:         return 1
880:     fi
881: 
882:     # The plan (PL-001): a preview starts from none and writes its own at the
883:     # end; an apply reads the one the preview left and spends it before
884:     # anything runs, so a second apply cannot stand on the same agreement.
885:     MATCH_PLAN_TEXT=""
886:     local plan_lines="" pverb pfiles pbytes
887:     if [ "${apply}" = "1" ]; then
888:         if [ -s "${MATCH_PLAN}" ] && head -1 "${MATCH_PLAN}" | grep -q '^plan [0-9][0-9]*$'; then
889:             MATCH_PLAN_TEXT=$(tail -n +2 "${MATCH_PLAN}")
890:         fi
891:         rm -f "${MATCH_PLAN}" 2>/dev/null
892:         # Spent means gone (the audit of the fix round, lead G2-A-04): a
893:         # plan the cache would not let go stayed for the next apply, which
894:         # then stood on a preview it did not follow. One that cannot be
895:         # removed is not used.
896:         if [ -e "${MATCH_PLAN}" ]; then
897:             echo "Nothing was removed: something went wrong on this device. Try again."
898:             log_message "match: refused, the preview plan ${MATCH_PLAN} could not be removed, so it could not be spent"
899:             say_why "SOMETHING WENT WRONG"
900:             record_outcome content-match 1
901:             return 1
902:         fi
903:         if [ -z "${MATCH_PLAN_TEXT}" ]; then
904:             # No check behind this apply at all -- run on its own, or run
905:             # again after the apply that spent the plan -- is not a change
906:             # since a check; the why names what is missing (vm-qa run 68:
907:             # the round-trip ran --apply alone and was told SOMETHING
908:             # CHANGED SINCE YOU CHECKED).
909:             echo "Nothing was removed: check what would change first, then try again."
910:             log_message "match: refused, no preview plan to apply"
911:             say_why "CHECK WHAT WOULD CHANGE FIRST"
912:             record_outcome content-match 1
913:             return 1
914:         fi
915:         # It writes into the saves restore's tree (G-A-07).
916:         tree_record_take
917:     else
918:         rm -f "${MATCH_PLAN}" 2>/dev/null
919:     fi
920: 
921:     # What the page that runs this shows when it is done. A match is mostly
922:     # deletion, and rclone's own totals for a deletion read "0 B / 0 B" --
923:     # true and useless (maintainer, 2026-09-07). So each system is announced
924:     # as a unit while it runs, and the summary at the end names what went:
925:     # the numbers the confirmation showed, per system, so the last screen
926:     # answers the first one.
927:     local total_bytes=0 removed_detail="" unit_i=0 unit_n=${#SYS[@]} planned
928:     for sys in "${SYS[@]}"; do
929:         unit_i=$((unit_i + 1))
930:         # Every chosen system is an item on the page, announced before its
931:         # own dry run -- so the page names what is being checked while the
932:         # check runs -- and announced whether or not it turns out to need
933:         # anything. The page shows ITEM i OF n with this script's n, so n has
934:         # to be the number of announcements the run makes and i their running
935:         # count; until 2026-09-09 a system with nothing to do was skipped
936:         # without one, and a run over three systems ended on ITEM 2 OF 3
937:         # (#95). "Already matches the cloud" is that item's outcome, not a
938:         # reason to hide it, and counting the work first would have held the
939:         # page on WORKING with no item through one dry run per system. The
940:         # preview (apply=0) prints plan lines for the confirmation and no
941:         # markers, as before.
942:         [ "${apply}" = "1" ] && echo ">>> unit ${sys}|${unit_i}|${unit_n}"
943:         planned=$(match_plan_one "${sys}")
944:         IFS='|' read -r _ verb files bytes <<< "${planned}"
945:         if [ "${apply}" = "1" ] && [ "${verb}" != "fail" ] && [ "${verb}" != "none" ]; then
946:             # Held to the preview: the same verb, and no more to remove than
947:             # it counted -- a ROM added since, or a system gone from the
948:             # cloud since, is not what the player agreed to. The preview's
949:             # count, not this one, is what --max-delete is given.
950:             pverb=""; pfiles=""; pbytes=""
951:             IFS='|' read -r _ pverb pfiles pbytes <<< "$(match_plan_of "${sys}")"
952:             if [ -z "${pverb}" ] || [ "${verb}" != "${pverb}" ] \
953:                || ! [ "${files}" -le "${pfiles:-0}" ] 2>/dev/null; then
954:                 echo "Nothing was removed from ${sys}: it changed since you checked. Check again to see what would change."
955:                 log_message "match: ${sys} refused: previewed ${pverb:-nothing}|${pfiles:--}, now ${verb}|${files}"
956:                 say_why "SOMETHING CHANGED SINCE YOU CHECKED"
957:                 rc=1
958:                 continue
959:             fi
960:             files="${pfiles}"; bytes="${pbytes}"
961:         fi
962:         [ "${apply}" = "1" ] || plan_lines="${plan_lines}${planned}"$'\n'
963:         case "${verb}" in
964:             fail)
965:                 # A system that could not be told is neither planned nor
966:                 # touched (PL-001). With the network gone the run is the
967:                 # no-network skip, as everywhere else here; otherwise the
968:                 # preview says so and plans nothing, and an apply says why.
969:                 if [ "${apply}" = "1" ]; then
970:                     echo "Couldn't check ${sys} against your cloud, so nothing was removed from it."
971:                 else
972:                     echo "Couldn't check ${sys} against your cloud. Try again."
973:                 fi
974:                 if network_gone; then
975:                     if [ "${apply}" = "1" ]; then
976:                         echo ">>> removed ${total_removed}|${total_bytes}|${removed_detail}"
977:                         stop_no_network match "${files}" "checking ${sys} against the cloud"
978:                     fi
979:                     echo "Skipped: there's no network connection. Try again when you're online."
980:                     exit "${EXIT_NO_NETWORK}"
981:                 fi
982:                 [ "${apply}" = "1" ] && say_why "$(why_for "${files}")"
983:                 rc=${files}
984:                 [ "${rc}" -ne 0 ] 2>/dev/null || rc=1
985:                 continue
986:             ;;
987:             none)
988:                 [ "${apply}" = "1" ] && echo "Nothing to remove from ${sys}: it already matches the cloud."
989:                 continue
990:             ;;
991:             remove)
992:                 if [ "${apply}" = "1" ]; then
993:                     echo "Removing ${files} files from ${sys} that aren't in your cloud..."
994:                     match_before "${sys}"
995:                     rclone delete "${DEST}/${sys}" \
996:                         "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
997:                         --max-delete "${files}" \
998:                         --log-file "${MATCH_LOG}" --log-level INFO
999:                     del_rc=$?
1000:                     match_count "${sys}"
1001:                     if [ ${del_rc} -ne 0 ]; then
1002:                         rc=${del_rc}
1003:                         log_message "match: removing ${sys}: rclone exit ${del_rc}"
1004:                         echo "Couldn't finish removing files from ${sys}: $(why_for "${del_rc}" | tr 'A-Z' 'a-z')."
1005:                         say_why "$(why_for "${del_rc}")"
1006:                     fi
1007:                     rmdir "${DEST}/${sys}" 2>/dev/null
1008:                 else
1009:                     echo "${sys}|remove|${files}|${bytes}"
1010:                 fi
1011:             ;;
1012:             sync)
1013:                 if [ "${apply}" = "1" ]; then
1014:                     echo "Matching ${sys} to the cloud..."
1015:                     # --max-delete is the fail-closed half: if reality has
1016:                     # drifted from the preview the player agreed to, this
1017:                     # aborts rather than deleting more than they saw.
1018:                     #
1019:                     # It is a cap, not a transaction. Measured on rclone
1020:                     # 1.75.0: given three deletions and --max-delete 2, it
1021:                     # exits 7 having already removed two. So it bounds the
1022:                     # damage to what was previewed and does not undo it --
1023:                     # the removals are final (D-CLOUD-023), which is why a
1024:                     # count above the preview's is refused before this runs.
1025:                     match_before "${sys}"
1026:                     bounded_content_rclone sync "$(remote_for "${sys}")" "${DEST}/${sys}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
1027:                         "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
1028:                         --max-delete "${files}" \
1029:                         --progress --stats 1s \
1030:                         --log-file "${MATCH_LOG}" --log-level INFO
1031:                     sync_rc=$?
1032:                     match_count "${sys}"
1033:                     if [ ${sync_rc} -ne 0 ]; then
1034:                         rc=${sync_rc}
1035:                         sweep_partials "${DEST}/${sys}"
1036:                         # A failed unit says why: the network gone ends the
1037:                         # run as 69 here, anything else carries rclone's own
1038:                         # code up as before. Before the 69 exit, the running
1039:                         # totals go out on the same `>>> removed` line the
1040:                         # completed run prints, so the page can report the
1041:                         # deletions that did happen -- a match is mostly
1042:                         # deletion, and it had already run for every system
1043:                         # before this one (D-UI-028; #105). The totals are
1044:                         # what rclone reports removed (match_count), within
1045:                         # what the player agreed to; what was removed is what
1046:                         # the cloud does not have, so it is gone (D-CLOUD-023).
1047:                         if network_gone; then
1048:                             echo ">>> removed ${total_removed}|${total_bytes}|${removed_detail}"
1049:                             stop_no_network match "${sync_rc}" "matching ${sys} to the cloud"
1050:                         fi
1051:                         log_message "match: matching ${sys}: rclone exit ${sync_rc}"
1052:                         echo "Couldn't finish matching ${sys} to the cloud: $(why_for "${sync_rc}" | tr 'A-Z' 'a-z')."
1053:                         say_why "$(why_for "${sync_rc}")"
1054:                     fi
1055:                 else
1056:                     # The bytes the dry run counted, so the confirmation and
1057:                     # the done page agree (the preview said 78 KB where the
1058:                     # page then said 224 KB, 2026-09-07).
1059:                     echo "${sys}|sync|${files}|${bytes}"
1060:                 fi
1061:             ;;
1062:             *)
1063:                 # match_plan_one prints none, remove or sync; anything else
1064:                 # is a failure to plan, and an announced item must not end
1065:                 # in silence.
1066:                 [ "${apply}" = "1" ] && echo "Couldn't check ${sys} against the cloud."
1067:                 log_message "match: no plan for ${sys} (${planned})"
1068:                 rc=1
1069:             ;;
1070:         esac
1071:     done
1072: 
1073:     # The preview's plan, only when every system could be told: a preview
1074:     # that could not see one system offers nothing to apply.
1075:     if [ "${apply}" != "1" ] && [ "${rc}" -eq 0 ]; then
1076:         if ! match_plan_write "${plan_lines}"; then
1077:             echo "Couldn't keep track of what would change, so nothing can be removed yet. Try again."
1078:             log_message "match: the plan could not be written to ${MATCH_PLAN}"
1079:             rc=1
1080:         fi
1081:     fi
1082: 
1083:     if [ "${apply}" = "1" ]; then
1084:         # ">>> removed 14|314572800|snes:12:300000000,gb:2:14572800" -- the
1085:         # page renders it on its last screen. The counts are the files rclone
1086:         # reports it removed, with the sizes listed before it ran (#308 gpt
1087:         # F-CS-26); they were the preview's, and a system one of whose
1088:         # deletions failed was reported as though all of them had happened.
1089:         # --max-delete holds each system to the preview's count.
1090:         echo ">>> removed ${total_removed}|${total_bytes}|${removed_detail}"
1091:         log_message "match: applied, removed ${total_removed} files, rc=${rc}"
1092:         tree_record_give
1093:         # The page that ran it fades; the row in the menu has to be able to
1094:         # answer "did that work?" afterwards, like every other cloud action.
1095:         record_outcome content-match "${rc}"
1096:     fi
1097:     return ${rc}
1098:     } 9>&-
1099: }
1100: 
1101: content_files() {
1102:     local dir="$1"; shift
1103:     # One rule for both sides (D-CLOUD-048), set by MEDIA_MODE (D-CLOUD-050):
1104:     #   roms  -- ROMs and BIOS only: the scraper's folders and the game list
1105:     #            are neither listed nor moved
1106:     #   with  -- ROMs and game content together
1107:     #   only  -- game content alone: the scraper's folders and gamelist.xml
1108:     # The game list is game content (D-CLOUD-049): the scraper writes it
1109:     # beside the artwork, and a restored-then-scraped device must read as
1110:     # matching its cloud under ROMs alone. At any depth, as the transfers
1111:     # move it (the ROMs pass excludes "**/gamelist.xml", the game-list pass
1112:     # includes it): a list below a system's own folder was counted as a ROM
1113:     # (the audit of the fixes, G-A-10).
1114:     local -a media=()
1115:     local d
1116:     case "${MEDIA_MODE:-roms}" in
1117:         roms) for d in ${MEDIA_DIRS:-images videos manuals screenshots fanart boxart wheel mix maps media}; do media+=( ! -path "${dir%/}/${d}/*" ); done
1118:               media+=( ! -name gamelist.xml ) ;;
1119:         only) media+=( "(" -name gamelist.xml )
1120:               for d in ${MEDIA_DIRS:-images videos manuals screenshots fanart boxart wheel mix maps media}; do media+=( -o -path "${dir%/}/${d}/*" ); done
1121:               media+=( ")" ) ;;
1122:     esac
1123:     find "${dir}" -type f \
1124:         ! -name '*.srm' ! -name '*.sav' ! -name '*.fs' ! -name '*.state*' \
1125:         ! -name '*.auto' ! -name '*.dsv*' ! -name '*.eep' ! -name '*.mpk' \
1126:         ! -name '*.sra' ! -name '*.fla' ! -name '*.mcd' ! -name '*.mcr' \
1127:         ! -path '*/save/*' ! -path '*/memcards/*' \
1128:         ! -path '*/shared/savefiles/*' ! -path '*/PPSSPP/*' \
1129:         ! -path '*conflicted copy*' ! -name '*.sync-conflict-*' \
1130:         ! -name '*.????????.partial' \
1131:         ! -path "${dir%/}/README.txt" \
1132:         "${media[@]}" "$@" 2>/dev/null
1133: }
1134: # Local systems that hold content, for the union scan.
1135: local_content_dirs() {
1136:     local d base
1137:     for d in "${DEST}"/*/; do
1138:         [ -d "${d}" ] || continue
1139:         base=$(basename "${d}")
1140:         case "${base}" in savefiles|savestates|screenshots|backup) continue ;; esac
1141:         content_files "${d}" | head -1 | grep -q . && printf '%s\n' "${base}"
1142:     done
1143: }
1144: # What a copy from side $1 to side $2 would move, as "count|bytes". Both
1145: # files are "size|relpath" listings, and a line matches only when the far
1146: # side has the same name at the same size -- so a file absent over there
1147: # counts, and so does one present at a different size, which is what
1148: # `rclone copy` compares (size, then modtime where the backend keeps one).
1149: # A same-size file is NOT counted whatever changed inside it: these listings
1150: # carry name and size only, so a file rewritten to the same length -- a
1151: # patched ROM, a re-saved config -- reads as present, though a copy would
1152: # move it on modtime or hash. The figure here can therefore run under what
1153: # a copy moves, never over. The caller also strips the game list from both
1154: # listings first (see --scan): its direction is decided by a modtime these
1155: # listings do not carry, so a differing size is not a direction. The count
1156: # and the bytes describe one set, so a page can put them on one line without
1157: # contradicting itself; until 2026-09-08 the count compared names alone and
1158: # would have read "0 FILES" beside a non-zero size for a ROM re-uploaded at
1159: # a new size.
1160: # Not comm(1): the image's busybox has no comm, and `comm ... | wc -l` then
1161: # reads 0 -- "nothing differs" -- which is the wrong way for a count to fail
1162: # (found in the VM, 2026-09-06). awk is what this script already runs on;
1163: # the getline form is safe when either file is empty, where the NR==FNR
1164: # idiom is not.
1165: delta_of() {
1166:     awk -F'|' -v L="$2" 'BEGIN { while ((getline x < L) > 0) a[x] = 1 }
1167:         !($0 in a) { n++; b += $1 } END { print n+0 "|" b+0 }' "$1"
1168: }
1169: # Drop from a cloud "size|path" listing what content_files drops locally, so
1170: # the two sides are counted by one rule.
1171: #
1172: # The same set content_files and the transfers describe (#308 gpt F-CS-30):
1173: # a save folder at any depth -- save/, memcards/, PPSSPP/ and dc's
1174: # shared/savefiles/, as the local find and the unanchored rclone excludes
1175: # have them -- and the setup's note at a unit's root (a README.txt directly
1176: # in a system's folder), which neither side carries. A README deeper in a
1177: # game's folder is that game's, and is content on both sides. This used to
1178: # look for save folders one level down only, missed shared/savefiles, and
1179: # dropped every README at any depth, so a restored system read as differing
1180: # from its own cloud copy.
1181: cloud_content_filter() {
1182:     local dirs; dirs="^($(echo ${MEDIA_DIRS} | tr ' ' '|'))$"
1183:     awk -F'|' -v dirs="${dirs}" -v mode="${MEDIA_MODE}" '
1184:         { n = split($2, seg, "/"); if (n < 2) next
1185:           f = seg[n]
1186:           game = (n > 2 && seg[2] ~ dirs) || f == "gamelist.xml"
1187:           if (mode == "roms" && game) next
1188:           if (mode == "only" && !game) next
1189:           if (f ~ /\.(srm|sav|fs|auto|eep|mpk|sra|fla|mcd|mcr)$/ || f ~ /\.state/ || f ~ /\.dsv/) next
1190:           if ($2 ~ /conflicted copy/ || f ~ /\.sync-conflict-/) next
1191:           if (f ~ /\.[^.\/][^.\/][^.\/][^.\/][^.\/][^.\/][^.\/][^.\/]\.partial$/) next
1192:           if (n == 2 && f == "README.txt") next
1193:           for (i = 2; i < n; i++) {
1194:               if (seg[i] == "save" || seg[i] == "memcards" || seg[i] == "PPSSPP") next
1195:               if (seg[i] == "shared" && i + 1 < n && seg[i + 1] == "savefiles") next
1196:           }
1197:           print }'
1198: }
1199: # --with-media: include scraped game content (D-CLOUD-048). Off by default:
1200: # the scraper's folders under a system are neither moved nor counted unless
1201: # the switch is on, so a restored-then-scraped device does not read as
1202: # "different" from its cloud copy. Taken from anywhere on the command line.
1203: MEDIA_MODE=roms
1204: _ARGS=()
1205: for _a in "$@"; do
1206:     case "${_a}" in
1207:         --with-media) MEDIA_MODE=with ;;
1208:         --media-only) MEDIA_MODE=only ;;
1209:         *) _ARGS+=("${_a}") ;;
1210:     esac
1211: done
1212: set -- "${_ARGS[@]}"
1213: MEDIA_DIRS="images videos manuals screenshots fanart boxart wheel mix maps media"
1214: # What the main rclone pass carries, per mode. The game list never rides the
1215: # main pass: it has its own --update pass below (newest wins), which runs
1216: # only when game content is in scope.
1217: MEDIA_EXCLUDES=()
1218: case "${MEDIA_MODE}" in
1219:     roms) for _d in ${MEDIA_DIRS}; do MEDIA_EXCLUDES+=(--exclude "/${_d}/**"); done ;;
1220:     only) for _d in ${MEDIA_DIRS}; do MEDIA_EXCLUDES+=(--include "/${_d}/**"); done ;;
1221: esac
1222: 
1223: case "${1}" in
1224:     --match)
1225:         # Preview by default; --apply is what deletes.
1226:         if [ "${2}" = "--apply" ]; then
1227:             match_run 1
1228:         else
1229:             match_run 0
1230:         fi
1231:         exit $?
1232:     ;;
1233:     --scan)
1234:         # One line per system in the union of cloud and device:
1235:         #   name|cloud_bytes|supported|device_bytes|files_in_cloud_not_here|files_here_not_in_cloud|bytes_in_cloud_not_here|bytes_here_not_in_cloud
1236:         # Both sides listed by the same rule (D-CLOUD-048) as "size|relpath"
1237:         # and compared by name and size (delta_of), because totals cannot say
1238:         # whether one side has what the other has. Fields 7 and 8 are what a
1239:         # copy in that direction would send; fields 5 and 6 count the same
1240:         # set. The game list is in the totals and never in the comparison
1241:         # (below). They arrived 2026-09-08; the first six keep their position
1242:         # and type, so a page built against six still reads this line.
1243:         SUP=$(supported_systems)
1244:         TMP=$(mktemp -d /tmp/cloud-scan.XXXXXX); trap 'rm -rf "${TMP}"' EXIT
1245:         rclone lsf -R --files-only --format "sp" --separator "|" "${ROOT}ROMs/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null \
1246:             | cloud_content_filter > "${TMP}/cloud"
1247:         scan_rc=${PIPESTATUS[0]}
1248:         # A code other than 3 from a folder that is simply not there yet
1249:         # (a server whose "missing" rclone does not map to "not found",
1250:         # #142) is an empty cloud, not one that could not be read.
1251:         if [ "${scan_rc}" -ne 0 ] && [ "${scan_rc}" -ne 3 ] && absent_not_broken "${ROOT}ROMs/"; then
1252:             log_message "scan: ROMs is not there yet (rclone exit ${scan_rc}; its nearest listable parent lacks it)"
1253:             scan_rc=3
1254:         fi
1255:         # BIOS is the ROMs tier's, never game content's: under --media-only it
1256:         # is not listed, so the union does not carry a line the page would
1257:         # skip and the log would puzzle over (3608 cloud BIOS files "not on
1258:         # this device" under game content alone, RG35XX SP, 2026-09-06).
1259:         if [ "${MEDIA_MODE}" != only ]; then
1260:             rclone lsf -R --files-only --format "sp" --separator "|" "${ROOT}BIOS/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null \
1261:                 | grep -v '^[0-9]*|README\.txt$' | sed 's/|/|bios\//' >> "${TMP}/cloud"
1262:             bios_rc=${PIPESTATUS[0]}
1263:             if [ "${bios_rc}" -ne 0 ] && [ "${bios_rc}" -ne 3 ] && absent_not_broken "${ROOT}BIOS/"; then
1264:                 log_message "scan: BIOS is not there yet (rclone exit ${bios_rc}; its nearest listable parent lacks it)"
1265:                 bios_rc=3
1266:             fi
1267:             # Keep the code that says the most. A missing folder is rclone's
1268:             # 3 and the one code an empty cloud gives, so a ROMs listing the
1269:             # cloud refused (5, 7) must not be overwritten by a BIOS folder
1270:             # that merely is not there yet.
1271:             if [ "${bios_rc}" -ne 0 ] && { [ "${scan_rc}" -eq 0 ] || [ "${scan_rc}" -eq 3 ]; }; then
1272:                 scan_rc=${bios_rc}
1273:             fi
1274:         fi
1275:         # A listing that failed with the network gone is not an empty cloud,
1276:         # and the page must not be handed one: every system on the device
1277:         # would read as "not in your cloud yet". Say why, print no lines,
1278:         # and exit the code EmulationStation names. A listing that failed
1279:         # with the network up -- no ROMs folder yet, rclone's 3 -- is an
1280:         # empty cloud, and goes on as before.
1281:         if [ "${scan_rc}" -ne 0 ] && network_gone; then
1282:             log_message "scan: skipped, no network (rclone exit ${scan_rc})"
1283:             echo "Skipped: there's no network connection. Try again when you're online." >&2
1284:             exit "${EXIT_NO_NETWORK}"
1285:         fi
1286:         # A listing that failed with the network up is not an empty cloud
1287:         # either, unless the failure is that the folder is not there: rclone's
1288:         # 3, "directory not found", is what a cloud nothing has been backed up
1289:         # to yet answers, and goes on as before. Anything else -- the cloud
1290:         # refused the connection, rejected the sign-in, or answered with an
1291:         # error -- is a cloud that could not be read, and the page must say
1292:         # so rather than list every system on the device as "not yet in your
1293:         # cloud" (a refused port exited 5 and the picker offered the whole
1294:         # device for upload, 2026-09-10; D-CLOUD-077). rclone's code goes up
1295:         # unchanged: the sentinels are 75 and 69, which rclone never returns.
1296:         if [ "${scan_rc}" -ne 0 ] && [ "${scan_rc}" -ne 3 ]; then
1297:             log_message "scan: the cloud could not be read (rclone exit ${scan_rc})"
1298:             echo "Couldn't finish reading your cloud. Try again." >&2
1299:             exit "${scan_rc}"
1300:         fi
1301:         # The pre-tier rows (a system straight under the content root) are
1302:         # offered only for a folder this device has or a system it supports
1303:         # -- the rule resolve_src applies, which this listing never did (fork
1304:         # #352: on a device whose content root was the Dropbox root, every
1305:         # folder in the account -- "my Hello sign directory, documents,
1306:         # videos" -- was listed as a system to restore).
1307:         sizes_under "${ROOT}" | grep -vE '^(ROMs|BIOS)\|' \
1308:             | awk -F'|' -v loc=" $(legacy_dirs | tr '\n' ' ') " -v sup="$(printf '\n%s\n' "${SUP}")" \
1309:                   '{ if (index(loc, " " $1 " ") || index(sup, "\n" $1 "\n")) print }' > "${TMP}/legacy"
1310:         {
1311:             cut -d'|' -f2 "${TMP}/cloud" | cut -d/ -f1
1312:             local_content_dirs
1313:         } | sort -u | while IFS= read -r name; do
1314:             [ -n "${name}" ] || continue
1315:             # This system's cloud side, "size|relpath" under the system.
1316:             awk -F'|' -v n="${name}" '{ split($2, seg, "/"); if (seg[1] == n) print $1 "|" substr($2, length(n) + 2) }' "${TMP}/cloud" > "${TMP}/c"
1317:             # The device side by the same rule. One find per system: stat
1318:             # supplies the sizes, so the total needs no second pass. The
1319:             # prefix is cut by length, not by pattern, so a system name
1320:             # holding a regex character cannot mis-strip.
1321:             if [ -d "${DEST}/${name}" ]; then
1322:                 content_files "${DEST}/${name}" -exec stat -c '%s|%n' {} + \
1323:                     | awk -v p="${DEST}/${name}/" '{ i = index($0, "|"); print substr($0, 1, i) substr($0, i + 1 + length(p)) }' > "${TMP}/l"
1324:             else
1325:                 : > "${TMP}/l"
1326:             fi
1327:             cbytes=$(awk -F'|' '{ t += $1 } END { print t+0 }' "${TMP}/c")
1328:             lbytes=$(awk -F'|' '{ t += $1 } END { print t+0 }' "${TMP}/l")
1329:             # The game list is in those totals and out of the comparison.
1330:             # Under game content it travels in its own pass, --update, newest
1331:             # wins (the transfer below); these listings carry no modtime to
1332:             # say which side that is, so a size that differs is not a
1333:             # direction, and a page that counted it read "1 FILE TO RESTORE"
1334:             # on whichever side's list was older -- and kept reading it,
1335:             # since a run moves nothing that way (found in review,
1336:             # 2026-09-08). Any depth, as the transfer's "**/gamelist.xml".
1337:             # Under ROMs alone a system's own list is on neither side, so
1338:             # there the strip touches only a list nested in a subfolder.
1339:             grep -vE '[|/]gamelist\.xml$' "${TMP}/c" > "${TMP}/cd"
1340:             grep -vE '[|/]gamelist\.xml$' "${TMP}/l" > "${TMP}/ld"
1341:             IFS='|' read -r cnl cnl_bytes <<< "$(delta_of "${TMP}/cd" "${TMP}/ld")"
1342:             IFS='|' read -r lnc lnc_bytes <<< "$(delta_of "${TMP}/ld" "${TMP}/cd")"
1343:             if [ "${name}" = "bios" ] || printf '%s\n' "${SUP}" | grep -qxF "${name}"; then sup=1; else sup=0; fi
1344:             echo "${name}|${cbytes}|${sup}|${lbytes}|${cnl}|${lnc}|${cnl_bytes}|${lnc_bytes}"
1345:         done
1346:         # The pre-tier layout (a system straight under the content root) is
1347:         # listed for size alone and never compared: device_bytes and every
1348:         # comparison field are 0 without looking. The page reads an empty
1349:         # far side as "all of it moves", which is the only true reading of
1350:         # a line like this.
1351:         while IFS='|' read -r name bytes; do
1352:             [ -n "${name}" ] || continue
1353:             echo "${name}|${bytes}|0|0|0|0|0|0"
1354:         done < "${TMP}/legacy"
1355:         exit 0
1356:     ;;
1357:     --systems)
1358:         selected_systems
1359:         exit 0
1360:     ;;
1361:     --set-systems)
1362:         shift
1363:         # System folder names, and nothing else (audit #307 PL-030). The
1364:         # picker passes the names it read from the cloud, joined by spaces,
1365:         # and every one of them goes on to name a folder under /storage/roms
1366:         # and in the cloud; one that is not a folder's name -- a character
1367:         # the shell would act on, a glob, "..", a leading dash a later grep
1368:         # would take as an option -- is refused, and the whole selection
1369:         # with it, so nothing is half-written. The names are split with
1370:         # globbing off: `printf $*` expanded "*" against the working folder.
1371:         local_names=()
1372:         set -f
1373:         read -r -a local_names <<< "$*"
1374:         set +f
1375:         for _n in "${local_names[@]}"; do
1376:             if ! [[ "${_n}" =~ ^[A-Za-z0-9_][A-Za-z0-9._-]*$ ]]; then
1377:                 echo "Nothing was changed: \"${_n}\" isn't the name of a system folder."
1378:                 log_message "set-systems: refused, not a system folder name: ${_n}"
1379:                 exit 1
1380:             fi
1381:         done
1382:         mkdir -p "$(dirname "${SELECTION}")" 2>/dev/null
1383:         # An empty selection is a real answer ("none"), distinct from never
1384:         # having chosen; the file exists either way. Which is exactly why it
1385:         # is written whole or not at all: a kill mid-write left an empty
1386:         # file, and an empty file is a different valid choice -- every later
1387:         # --selected then said no systems were selected (D-CLOUD-078, #105).
1388:         { [ ${#local_names[@]} -eq 0 ] || printf '%s\n' "${local_names[@]}"; } > "${SELECTION}.tmp.$$" 2>/dev/null
1389:         mv -f "${SELECTION}.tmp.$$" "${SELECTION}" 2>/dev/null || rm -f "${SELECTION}.tmp.$$"
1390:         echo "OK $(selected_systems | wc -l) selected"
1391:         exit 0
1392:     ;;
1393:     --selected)
1394:         mapfile -t DIRS < <(selected_systems)
1395:         # BIOS is not a system and is no longer a pick (maintainer, 2026-09-06):
1396:         # it comes with the tier whenever the cloud has it. The tier's own
1397:         # switch already says ROMS AND BIOS; nothing runs without them. A
1398:         # "bios" line in the selection -- the placeholder the interface wrote
1399:         # so that BIOS alone was not refused -- is the same thing: remote_for
1400:         # sends it to BIOS/, one unit, never to a system folder under ROMs/.
1401:         if [ "${MEDIA_MODE}" != only ] && exists_remote "${ROOT}BIOS" && ! printf '%s\n' "${DIRS[@]}" | grep -qx bios; then
1402:             DIRS+=("bios")
1403:         fi
1404:         # Refused only when there is nothing at all -- after BIOS is added,
1405:         # not before: "BIOS and no system" is a selection, and was refused
1406:         # as none (coordinator's row under audit #307 PL-012).
1407:         if [ ${#DIRS[@]} -eq 0 ]; then
1408:             echo "You haven't picked any systems for this device."
1409:             exit 1
1410:         fi
1411:     ;;
1412:     --list)
1413:         # Top-level directories only; one per line, no trailing slash.
1414:         # Lists both locations so an upgraded device still sees content that
1415:         # predates CONTENT_REMOTE, rather than presenting an unexplained empty
1416:         # list to somebody who changed nothing.
1417:         {
1418:             # current layout, reported under the local names the rest of the
1419:             # script uses -- BIOS in the cloud is /storage/roms/bios here
1420:             rclone lsf --dirs-only "${ROOT}ROMs/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | sed 's:/$::'
1421:             # the flat layout that shipped before it, minus its own containers
1422:             rclone lsf --dirs-only "${ROOT}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | sed 's:/$::' \
1423:                 | grep -vxE 'ROMs|BIOS'
1424:             if [ -n "${CONTENT_REMOTE}" ]; then
1425:                 rclone lsf --dirs-only "${LEGACY_ROOT}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | sed 's:/$::' \
1426:                     | grep -Fxf <(legacy_dirs) 2>/dev/null
1427:             fi
1428:         } | sort -u | sed '/^$/d'
1429:         exit 0
1430:     ;;
1431:     --all)
1432:         # Every system the cloud holds, and BIOS, each a unit of its own --
1433:         # the journey's first restore (main.cpp, the first-device prompt).
1434:         # It used to be one unit, DIRS=(""), which remote_for resolved to
1435:         # the ROMs container: BIOS never came down though the page said
1436:         # everything had, and the scraper-folder excludes, anchored at a
1437:         # system's root ("/images/**"), matched nothing under ROMs/ (audit
1438:         # #307 PL-012). Now the systems are enumerated as the picker lists
1439:         # them and each resolves as --selected resolves it (resolve_src:
1440:         # ROMs/<system>, then the flat layout, then the remote root), so
1441:         # every anchor sits where it does for --selected.
1442:         #
1443:         # Every listing this stands on is read fail-closed: a listing that
1444:         # failed is not an empty cloud. The ROMs listing was; the two older
1445:         # layouts' and BIOS's were not, so a cloud still on an older layout
1446:         # whose one listing failed restored nothing and said "Nothing to
1447:         # restore" (the audit of the fixes, G-A-07/G-A-03). The two older
1448:         # layouts are consulted only for names this device knows as
1449:         # systems -- ES declares them, or it holds the folder -- because an
1450:         # older layout's root is somebody's account, and a folder there is
1451:         # not a system because it is a folder.
1452:         all_listing() { # <path>: LISTED=its folders; the run stops when it cannot be read
1453:             local path="$1" lrc
1454:             LISTED=$(rclone lsf --dirs-only "${path}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); lrc=$?
1455:             [ "${lrc}" -eq 0 ] && return 0
1456:             LISTED=""
1457:             { [ "${lrc}" -eq 3 ] || [ "${lrc}" -eq 4 ] || absent_not_broken "${path}"; } && return 0
1458:             log_message "restore --all: ${path} could not be listed (rclone exit ${lrc})"
1459:             if network_gone; then
1460:                 echo "Skipped: there's no network connection. Try again when you're online."
1461:                 exit "${EXIT_NO_NETWORK}"
1462:             fi
1463:             echo "Couldn't finish: your cloud couldn't be read, so nothing was restored. Try again."
1464:             say_why "$(why_for "${lrc}")"
1465:             record_outcome content-restore "${lrc}"
1466:             exit "${lrc}"
1467:         }
1468:         all_listing "${ROOT}ROMs/"
1469:         ALL_ROMS=$(printf '%s\n' "${LISTED}" | sed 's:/$::')
1470:         ALL_KNOWN=$( { supported_systems; legacy_dirs; echo bios; } | sort -u )
1471:         all_listing "${ROOT}"
1472:         # BIOS is there when the content root lists it (a folder with files,
1473:         # or a directory marker) -- what exists_remote asked, from the same
1474:         # listing, read fail-closed.
1475:         ALL_BIOS=0; printf '%s\n' "${LISTED}" | grep -qx 'BIOS/' && ALL_BIOS=1
1476:         ALL_FLAT=$(printf '%s\n' "${LISTED}" | sed 's:/$::' | grep -vxE 'ROMs|BIOS' | grep -Fxf <(printf '%s\n' "${ALL_KNOWN}"))
1477:         ALL_LEGACY=""
1478:         if [ -n "${CONTENT_REMOTE}" ]; then
1479:             all_listing "${LEGACY_ROOT}"
1480:             ALL_LEGACY=$(printf '%s\n' "${LISTED}" | sed 's:/$::' | grep -Fxf <(legacy_dirs))
1481:         fi
1482:         mapfile -t DIRS < <(printf '%s\n' "${ALL_ROMS}" "${ALL_FLAT}" "${ALL_LEGACY}" | grep -v '^$' | sort -u)
1483:         # BIOS as --selected brings it: whenever the cloud has it, and not
1484:         # with game content alone.
1485:         if [ "${MEDIA_MODE}" != only ] && [ "${ALL_BIOS}" -eq 1 ] && ! printf '%s\n' "${DIRS[@]}" | grep -qx bios; then
1486:             DIRS+=("bios")
1487:         fi
1488:         if [ ${#DIRS[@]} -eq 0 ]; then
1489:             echo "Nothing to restore: your cloud has no ROMs or BIOS files yet."
1490:             log_message "restore --all: nothing in the cloud's ROMs or BIOS folders"
1491:             record_outcome content-restore 0
1492:             exit 0
1493:         fi
1494:     ;;
1495:     "")
1496:         echo "Usage: ${SCRIPT_NAME} --list | --all | <dir> [<dir>...]" >&2
1497:         exit 1
1498:     ;;
1499:     *)
1500:         DIRS=("$@")
1501:     ;;
1502: esac
1503: 
1504: 
1505: 
1506: STATUS=0
1507: take_cloud_lock
1508: # Everything from here to the end of the script runs with the lock
1509: # descriptor closed, so no child of this run can hold the lock once this
1510: # shell is gone -- see take_cloud_lock. The brace group is the whole of
1511: # the change: it adds no subshell, so exits, traps and variables behave
1512: # exactly as they did.
1513: {
1514: UNIT_N=${#DIRS[@]}; UNIT_I=0
1515: tree_record_take
1516: for DIR in "${DIRS[@]}"; do
1517:     SRC="$(resolve_src "${DIR}")"
1518:     TARGET="${DEST}/${DIR}"
1519:     UNIT_I=$((UNIT_I + 1))
1520:     log_message "Content restore: ${SRC} -> ${TARGET}"
1521:     # The marker the transfer page reads: what is being copied, and which of
1522:     # how many. rclone's own block totals that follow are this system's.
1523:     echo ">>> unit ${DIR:-everything}|${UNIT_I}|${UNIT_N}"
1524:     echo "Restoring ${DIR:-everything} from the cloud..."
1525:     # --progress is what puts the stats on stdout. With only --log-file they
1526:     # go to the log and the caller sees nothing -- which is why the progress
1527:     # card sat at "0 B / 0 B, -, 0 B/s" through a restore that was in fact
1528:     # copying Mega Drive ROMs the whole time. The saves path has always passed
1529:     # it; these two never did.
1530:     #
1531:     # And NOT --stats-one-line: that collapses the display to a totals line,
1532:     # losing the per-file block. A transfer of a thousand small BIOS files
1533:     # spends minutes between percentage changes, and the only thing that says
1534:     # it is alive rather than stuck is the name of the file it is on right
1535:     # now. --stats 1s keeps that moving.
1536:     #
1537:     # No --progress-terminal-width: the flag does not exist on every rclone we
1538:     # ship against (the saves scripts test for it with "rclone help | grep"
1539:     # before using it), and an unknown flag is a usage error that transfers
1540:     # nothing. rclone pads the file name out to a guessed width; the reader
1541:     # trims it, so the flag bought nothing worth a version check.
1542:     # The setup's note at a unit's root (BIOS/README.txt, cloud_setup
1543:     # --seed-folders) is not content, and neither side counts it (#308 gpt
1544:     # F-CS-30): it came down into /storage/roms/bios and read ever after as a
1545:     # file this device has and the cloud does not.
1546:     UNIT_LOG0=$(log_offset)
1547:     bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
1548:         "${SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${MEDIA_EXCLUDES[@]}" \
1549:         --exclude "gamelist.xml" --exclude "**/gamelist.xml" --exclude "/README.txt" \
1550:         --progress --stats 1s \
1551:         --log-file "${LOG_FILE}" --log-level INFO
1552:     RC=$?
1553: 
1554:     # The game list: newest wins, rather than whoever ran last. Game content
1555:     # only (D-CLOUD-049) -- under ROMs alone the file stays where it is. Its
1556:     # result is the unit's, by the same 0|9 rule (audit #307 PL-066): it
1557:     # was discarded with `|| true`, so a game list that did not move left a
1558:     # unit, a stamp and a page that said the unit had.
1559:     if [ "${MEDIA_MODE}" != roms ] && { [ "${RC}" -eq 0 ] || [ "${RC}" -eq 9 ]; }; then
1560:         bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
1561:             "${GAMELIST_ONLY[@]}" --update \
1562:             --stats 0 \
1563:             --log-file "${LOG_FILE}" --log-level INFO
1564:         GL_RC=$?
1565:         case "${RC}" in
1566:             0|9) case "${GL_RC}" in 0|9) ;; *) RC=${GL_RC} ;; esac ;;
1567:         esac
1568:     fi
1569: 
1570:     # What moved in this unit, whatever its result (G-A-08/G-A-13).
1571:     moved_since "${UNIT_LOG0}" && PROGRESS_MADE=1
1572:     if [ ${RC} -ne 0 ] && [ ${RC} -ne 9 ]; then
1573:         # What a failed transfer may have left in this unit's folder goes
1574:         # now (G-A-07).
1575:         sweep_partials "${TARGET}"
1576:         # A failed unit says why: the network gone ends the run as 69 here,
1577:         # anything else carries rclone's own code up as before.
1578:         network_gone && stop_no_network restore "${RC}" "restoring ${DIR:-everything}"
1579:         log_message "restore of ${DIR:-everything}: rclone exit ${RC}"
1580:         echo "Couldn't finish restoring ${DIR:-everything}: $(why_for "${RC}" | tr 'A-Z' 'a-z')."
1581:         say_why "$(why_for "${RC}")"
1582:         STATUS=${RC}
1583:     else
1584:         echo "Restored ${DIR:-everything}."
1585:     fi
1586: done
1587: 
1588: tree_record_give
1589: 
1590: # The progress card is gone by the time somebody who walked away comes back, so
1591: # leave the outcome where the menu can read it later. Device-local state, so it
1592: # lives under /storage/.cache and not in the settings backup.
1593: record_outcome content-restore "${STATUS}"
1594: 
1595: # A failed unit leaves with rclone's own code, unremapped: nothing rclone
1596: # returns can read as the lock sentinel now that it is 75 (#99).
1597: exit ${STATUS}
1598: } 9>&-
```


## SOURCE docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/refutation-03/probe.py

```text
1: #!/usr/bin/env python3
2: """Read the unchanged installed content classifier in isolated synthetic clouds."""
3: import argparse
4: import importlib.machinery
5: import importlib.util
6: import json
7: from pathlib import Path
8: import socket
9: import subprocess
10: import sys
11: 
12: owner = Path(__file__).resolve().parent
13: loader = importlib.machinery.SourceFileLoader('boundaries', str(owner / 'boundaries.py'))
14: spec = importlib.util.spec_from_loader(loader.name, loader)
15: mod = importlib.util.module_from_spec(spec)
16: loader.exec_module(mod)
17: 
18: 
19: class Probe(mod.Proof):
20:     def run_cases(self):
21:         cases = [
22:             ('empty-configured', '/Mine', {}, 'empty', ''),
23:             ('unrelated-configured', '/Mine', {'Mine/Photos/x.jpg': b'private photo fixture'}, 'empty', ''),
24:             ('unrelated-configured-fallback', '/Mine', {'Mine/Photos/x.jpg': b'private photo fixture', 'pixelelated/Content/ROMs/gb/A.gb': b'game fixture'}, 'found-elsewhere', '/pixelelated/Content'),
25:             ('tiered-configured', '/Mine', {'Mine/ROMs/gb/A.gb': b'game fixture', 'Mine/BIOS/qa.bin': b'bios fixture'}, 'ok', ''),
26:             ('tiered-explicit-root', '', {'ROMs/gb/A.gb': b'game fixture', 'BIOS/qa.bin': b'bios fixture'}, 'ok', ''),
27:             ('legacy-explicit-root', '', {'gb/A.gb': b'game fixture'}, 'ok', ''),
28:             ('unrelated-explicit-root', '', {'Photos/x.jpg': b'private photo fixture'}, 'empty', ''),
29:         ]
30:         for name, content, files, expected, found in cases:
31:             self.case = name
32:             print('START ' + name, flush=True)
33:             self.reset()
34:             self.conf('/pixelelated/Saves', '/pixelelated/Backups', content)
35:             self.on('a', 'mkdir -p /storage/roms/gb')
36:             for path, data in files.items():
37:                 self.put(path, data)
38:             before = {'cloud': self.hashes(), 'pointers': self.pointers()}
39:             result = self.on('a', '/usr/bin/cloud_setup --content-location')
40:             facts = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
41:             after = {'cloud': self.hashes(), 'pointers': self.pointers()}
42:             mod.require(before == after, 'read-only classification mutated fixture')
43:             passed = facts.get('STATE') == expected and facts.get('FOUND') == found
44:             row = {'case': name, 'expected_state': expected, 'expected_found': found,
45:                    'facts': facts, 'before': before, 'after': after, 'rc': result.returncode,
46:                    'status': 'PASS' if passed else 'FAIL'}
47:             self.results.append(row)
48:             mod.save(self.logs / 'results.json', self.results)
49:             print(row['status'] + ' ' + name + ' expected=' + expected + ' actual=' + facts.get('STATE', '<missing>'), flush=True)
50:         for key, value in self.original_scripts.items():
51:             guest, script = key.split('/')
52:             mod.require(self.on(guest, 'sha256sum /usr/bin/' + script).stdout.split()[0] == value,
53:                         'installed bytes changed: ' + key)
54:         mod.save(self.logs / 'installed-unchanged.json', self.original_scripts)
55:         return 0 if all(x['status'] == 'PASS' for x in self.results) else 1
56: 
57:     def cleanup(self):
58:         # Current vm-pair down verifies exact owned disks with pidfds and waits.
59:         self.local('vm-pair', 'down')
60:         if self.backend_started:
61:             self.local('cloud-test-backend', 'down')
62:         for port in (9040, 10022, 10023, 5909, 5910):
63:             with socket.socket() as sock:
64:                 mod.require(sock.connect_ex(('127.0.0.1', port)) != 0, 'owned port still open')
65:         mod.save(self.owner / 'cleanup.json', {'owned_guests_stopped': True, 'backend_stopped': True,
66:                                               'ports_unbound': [9040, 10022, 10023, 5909, 5910]})
67: 
68: 
69: if __name__ == '__main__':
70:     p = argparse.ArgumentParser()
71:     p.add_argument('--tree', type=Path, required=True)
72:     p.add_argument('--image', type=Path, required=True)
73:     p.add_argument('--build-id', required=True)
74:     p.add_argument('--output', type=Path, required=True)
75:     proof = Probe(p.parse_args())
76:     try:
77:         proof.start()
78:         code = proof.run_cases()
79:     finally:
80:         proof.cleanup()
81:     sys.exit(code)
```


## SOURCE docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/refutation-03/artifacts/results.json

```text
1: [
2:   {
3:     "after": {
4:       "cloud": {},
5:       "pointers": {
6:         "CONTENT_REMOTE": "/Mine",
7:         "LAYOUT_KEEP": "",
8:         "SAVES_REMOTE": "/pixelelated/Saves",
9:         "SETTINGS_REMOTE": "/pixelelated/Backups"
10:       }
11:     },
12:     "before": {
13:       "cloud": {},
14:       "pointers": {
15:         "CONTENT_REMOTE": "/Mine",
16:         "LAYOUT_KEEP": "",
17:         "SAVES_REMOTE": "/pixelelated/Saves",
18:         "SETTINGS_REMOTE": "/pixelelated/Backups"
19:       }
20:     },
21:     "case": "empty-configured",
22:     "expected_found": "",
23:     "expected_state": "empty",
24:     "facts": {
25:       "AT_PATH": "0",
26:       "AT_ROOT": "0",
27:       "CONTENT_REMOTE": "/Mine",
28:       "FOUND": "",
29:       "ROOT_DIRS": "",
30:       "STATE": "empty"
31:     },
32:     "rc": 0,
33:     "status": "PASS"
34:   },
35:   {
36:     "after": {
37:       "cloud": {
38:         "Mine/Photos/x.jpg": "ab10bb7bc26c1ec27f9a3696ed3ff66f9caad8de197ebe9a4f3332f1577670b9"
39:       },
40:       "pointers": {
41:         "CONTENT_REMOTE": "/Mine",
42:         "LAYOUT_KEEP": "",
43:         "SAVES_REMOTE": "/pixelelated/Saves",
44:         "SETTINGS_REMOTE": "/pixelelated/Backups"
45:       }
46:     },
47:     "before": {
48:       "cloud": {
49:         "Mine/Photos/x.jpg": "ab10bb7bc26c1ec27f9a3696ed3ff66f9caad8de197ebe9a4f3332f1577670b9"
50:       },
51:       "pointers": {
52:         "CONTENT_REMOTE": "/Mine",
53:         "LAYOUT_KEEP": "",
54:         "SAVES_REMOTE": "/pixelelated/Saves",
55:         "SETTINGS_REMOTE": "/pixelelated/Backups"
56:       }
57:     },
58:     "case": "unrelated-configured",
59:     "expected_found": "",
60:     "expected_state": "empty",
61:     "facts": {
62:       "AT_PATH": "1",
63:       "AT_ROOT": "0",
64:       "CONTENT_REMOTE": "/Mine",
65:       "FOUND": "",
66:       "ROOT_DIRS": "",
67:       "STATE": "ok"
68:     },
69:     "rc": 0,
70:     "status": "FAIL"
71:   },
72:   {
73:     "after": {
74:       "cloud": {
75:         "Mine/Photos/x.jpg": "ab10bb7bc26c1ec27f9a3696ed3ff66f9caad8de197ebe9a4f3332f1577670b9",
76:         "pixelelated/Content/ROMs/gb/A.gb": "fa50d02b39b239f20fa5810196dfbce4960c77fc7a2a2e893473da4e95382136"
77:       },
78:       "pointers": {
79:         "CONTENT_REMOTE": "/Mine",
80:         "LAYOUT_KEEP": "",
81:         "SAVES_REMOTE": "/pixelelated/Saves",
82:         "SETTINGS_REMOTE": "/pixelelated/Backups"
83:       }
84:     },
85:     "before": {
86:       "cloud": {
87:         "Mine/Photos/x.jpg": "ab10bb7bc26c1ec27f9a3696ed3ff66f9caad8de197ebe9a4f3332f1577670b9",
88:         "pixelelated/Content/ROMs/gb/A.gb": "fa50d02b39b239f20fa5810196dfbce4960c77fc7a2a2e893473da4e95382136"
89:       },
90:       "pointers": {
91:         "CONTENT_REMOTE": "/Mine",
92:         "LAYOUT_KEEP": "",
93:         "SAVES_REMOTE": "/pixelelated/Saves",
94:         "SETTINGS_REMOTE": "/pixelelated/Backups"
95:       }
96:     },
97:     "case": "unrelated-configured-fallback",
98:     "expected_found": "/pixelelated/Content",
99:     "expected_state": "found-elsewhere",
100:     "facts": {
101:       "AT_PATH": "1",
102:       "AT_ROOT": "0",
103:       "CONTENT_REMOTE": "/Mine",
104:       "FOUND": "",
105:       "ROOT_DIRS": "",
106:       "STATE": "ok"
107:     },
108:     "rc": 0,
109:     "status": "FAIL"
110:   },
111:   {
112:     "after": {
113:       "cloud": {
114:         "Mine/BIOS/qa.bin": "54bdd075d07d3bb149baf7f7684a7a56a3be6ae66bc2a18a221ac33544d17e19",
115:         "Mine/ROMs/gb/A.gb": "fa50d02b39b239f20fa5810196dfbce4960c77fc7a2a2e893473da4e95382136"
116:       },
117:       "pointers": {
118:         "CONTENT_REMOTE": "/Mine",
119:         "LAYOUT_KEEP": "",
120:         "SAVES_REMOTE": "/pixelelated/Saves",
121:         "SETTINGS_REMOTE": "/pixelelated/Backups"
122:       }
123:     },
124:     "before": {
125:       "cloud": {
126:         "Mine/BIOS/qa.bin": "54bdd075d07d3bb149baf7f7684a7a56a3be6ae66bc2a18a221ac33544d17e19",
127:         "Mine/ROMs/gb/A.gb": "fa50d02b39b239f20fa5810196dfbce4960c77fc7a2a2e893473da4e95382136"
128:       },
129:       "pointers": {
130:         "CONTENT_REMOTE": "/Mine",
131:         "LAYOUT_KEEP": "",
132:         "SAVES_REMOTE": "/pixelelated/Saves",
133:         "SETTINGS_REMOTE": "/pixelelated/Backups"
134:       }
135:     },
136:     "case": "tiered-configured",
137:     "expected_found": "",
138:     "expected_state": "ok",
139:     "facts": {
140:       "AT_PATH": "2",
141:       "AT_ROOT": "0",
142:       "CONTENT_REMOTE": "/Mine",
143:       "FOUND": "",
144:       "ROOT_DIRS": "",
145:       "STATE": "ok"
146:     },
147:     "rc": 0,
148:     "status": "PASS"
149:   },
150:   {
151:     "after": {
152:       "cloud": {
153:         "BIOS/qa.bin": "54bdd075d07d3bb149baf7f7684a7a56a3be6ae66bc2a18a221ac33544d17e19",
154:         "ROMs/gb/A.gb": "fa50d02b39b239f20fa5810196dfbce4960c77fc7a2a2e893473da4e95382136"
155:       },
156:       "pointers": {
157:         "CONTENT_REMOTE": "",
158:         "LAYOUT_KEEP": "",
159:         "SAVES_REMOTE": "/pixelelated/Saves",
160:         "SETTINGS_REMOTE": "/pixelelated/Backups"
161:       }
162:     },
163:     "before": {
164:       "cloud": {
165:         "BIOS/qa.bin": "54bdd075d07d3bb149baf7f7684a7a56a3be6ae66bc2a18a221ac33544d17e19",
166:         "ROMs/gb/A.gb": "fa50d02b39b239f20fa5810196dfbce4960c77fc7a2a2e893473da4e95382136"
167:       },
168:       "pointers": {
169:         "CONTENT_REMOTE": "",
170:         "LAYOUT_KEEP": "",
171:         "SAVES_REMOTE": "/pixelelated/Saves",
172:         "SETTINGS_REMOTE": "/pixelelated/Backups"
173:       }
174:     },
175:     "case": "tiered-explicit-root",
176:     "expected_found": "",
177:     "expected_state": "ok",
178:     "facts": {
179:       "AT_PATH": "0",
180:       "AT_ROOT": "0",
181:       "CONTENT_REMOTE": "",
182:       "FOUND": "",
183:       "ROOT_DIRS": "",
184:       "STATE": "empty"
185:     },
186:     "rc": 0,
187:     "status": "FAIL"
188:   },
189:   {
190:     "after": {
191:       "cloud": {
192:         "gb/A.gb": "fa50d02b39b239f20fa5810196dfbce4960c77fc7a2a2e893473da4e95382136"
193:       },
194:       "pointers": {
195:         "CONTENT_REMOTE": "",
196:         "LAYOUT_KEEP": "",
197:         "SAVES_REMOTE": "/pixelelated/Saves",
198:         "SETTINGS_REMOTE": "/pixelelated/Backups"
199:       }
200:     },
201:     "before": {
202:       "cloud": {
203:         "gb/A.gb": "fa50d02b39b239f20fa5810196dfbce4960c77fc7a2a2e893473da4e95382136"
204:       },
205:       "pointers": {
206:         "CONTENT_REMOTE": "",
207:         "LAYOUT_KEEP": "",
208:         "SAVES_REMOTE": "/pixelelated/Saves",
209:         "SETTINGS_REMOTE": "/pixelelated/Backups"
210:       }
211:     },
212:     "case": "legacy-explicit-root",
213:     "expected_found": "",
214:     "expected_state": "ok",
215:     "facts": {
216:       "AT_PATH": "0",
217:       "AT_ROOT": "0",
218:       "CONTENT_REMOTE": "",
219:       "FOUND": "",
220:       "ROOT_DIRS": "",
221:       "STATE": "empty"
222:     },
223:     "rc": 0,
224:     "status": "FAIL"
225:   },
226:   {
227:     "after": {
228:       "cloud": {
229:         "Photos/x.jpg": "ab10bb7bc26c1ec27f9a3696ed3ff66f9caad8de197ebe9a4f3332f1577670b9"
230:       },
231:       "pointers": {
232:         "CONTENT_REMOTE": "",
233:         "LAYOUT_KEEP": "",
234:         "SAVES_REMOTE": "/pixelelated/Saves",
235:         "SETTINGS_REMOTE": "/pixelelated/Backups"
236:       }
237:     },
238:     "before": {
239:       "cloud": {
240:         "Photos/x.jpg": "ab10bb7bc26c1ec27f9a3696ed3ff66f9caad8de197ebe9a4f3332f1577670b9"
241:       },
242:       "pointers": {
243:         "CONTENT_REMOTE": "",
244:         "LAYOUT_KEEP": "",
245:         "SAVES_REMOTE": "/pixelelated/Saves",
246:         "SETTINGS_REMOTE": "/pixelelated/Backups"
247:       }
248:     },
249:     "case": "unrelated-explicit-root",
250:     "expected_found": "",
251:     "expected_state": "empty",
252:     "facts": {
253:       "AT_PATH": "0",
254:       "AT_ROOT": "0",
255:       "CONTENT_REMOTE": "",
256:       "FOUND": "",
257:       "ROOT_DIRS": "",
258:       "STATE": "empty"
259:     },
260:     "rc": 0,
261:     "status": "PASS"
262:   }
263: ]
```


## SOURCE docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/refutation-03/console.log

```text
1: watch-build: recording in /workspace/repos/rocknix.worktrees/conflict-resolution/.build-runs/20261006T170444Z-6cd2ca39
2: PASS candidate bundle /workspace/artifacts/pixelelated-candidates/sha256/b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1
3: up: a (pid 2572302, ssh :10022, serial /tmp/rocknix-qemu-serial.sock, mac 52:54:00:52:4E:58)
4: up: b (pid 2572324, ssh :10023, serial /tmp/rocknix-qemu-serial-b.sock, mac 52:54:00:52:4E:59)
5: ready: a on 7afa9efcfc over ssh :10022 (answered after 0s)
6: ready: b on 7afa9efcfc over ssh :10023 (answered after 0s)
7: up: webdav serving /workspace/tmp/pixelelated-m7-p4-refutation-03/proof/cloud/data at http://127.0.0.1:9040 (guest: http://10.0.2.2:9040)
8: START empty-configured
9: PASS empty-configured expected=empty actual=empty
10: START unrelated-configured
11: FAIL unrelated-configured expected=empty actual=ok
12: START unrelated-configured-fallback
13: FAIL unrelated-configured-fallback expected=found-elsewhere actual=ok
14: START tiered-configured
15: PASS tiered-configured expected=ok actual=ok
16: START tiered-explicit-root
17: FAIL tiered-explicit-root expected=ok actual=empty
18: START legacy-explicit-root
19: FAIL legacy-explicit-root expected=ok actual=empty
20: START unrelated-explicit-root
21: PASS unrelated-explicit-root expected=empty actual=empty
22: down: owned QEMU exited (pid 2572302)
23: down: owned QEMU exited (pid 2572324)
24: down
```


## SOURCE docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/proxy-source-equality.json

```text
1: {
2:   "linux": {
3:     "before_files": 219,
4:     "after_files": 219,
5:     "added": [],
6:     "removed": [],
7:     "changed": []
8:   },
9:   "third_party": {
10:     "before_files": 53,
11:     "after_files": 53,
12:     "added": [],
13:     "removed": [],
14:     "changed": []
15:   }
16: }
```


## SOURCE docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/memory-recalculation.json

```text
1: {
2:   "csv_results": [
3:     {
4:       "profile": "software-10",
5:       "rows": 16,
6:       "pid_count": 1,
7:       "measured_cycles": 10,
8:       "virtual_growth_kib": -448,
9:       "resident_growth_kib": 684,
10:       "stamp_files": 0
11:     },
12:     {
13:       "profile": "software-sync-50",
14:       "rows": 56,
15:       "pid_count": 1,
16:       "measured_cycles": 50,
17:       "virtual_growth_kib": 0,
18:       "resident_growth_kib": 444,
19:       "stamp_files": 55,
20:       "unique_stamps": 55,
21:       "stamp_example": "1791232317 0 completed"
22:     },
23:     {
24:       "profile": "virgl-10",
25:       "rows": 16,
26:       "pid_count": 1,
27:       "measured_cycles": 10,
28:       "virtual_growth_kib": 0,
29:       "resident_growth_kib": 224,
30:       "stamp_files": 0
31:     }
32:   ],
33:   "new_rwxp_maps": [
34:     "7f27bec00000-7f27c0000000 rwxp 00000000 00:00 0 "
35:   ],
36:   "maps": {
37:     "003.maps": {
38:       "rwxp": [
39:         "7f27bf600000-7f27c0000000 rwxp 00000000 00:00 0 ",
40:         "7f27e0400000-7f27e0e00000 rwxp 00000000 00:00 0 ",
41:         "7f27e2400000-7f27e2e00000 rwxp 00000000 00:00 0 ",
42:         "7f27fc800000-7f27fd200000 rwxp 00000000 00:00 0 "
43:       ],
44:       "bytes": 41943040
45:     },
46:     "004.maps": {
47:       "rwxp": [
48:         "7f27bec00000-7f27c0000000 rwxp 00000000 00:00 0 ",
49:         "7f27e0400000-7f27e0e00000 rwxp 00000000 00:00 0 ",
50:         "7f27e2400000-7f27e2e00000 rwxp 00000000 00:00 0 ",
51:         "7f27fc800000-7f27fd200000 rwxp 00000000 00:00 0 "
52:       ],
53:       "bytes": 52428800
54:     }
55:   },
56:   "rwxp_growth_bytes": 10485760,
57:   "map_note": "Adjacent anonymous mappings merge: newly printed20MiB region replaces an existing10MiB region; total growth is10MiB, not20MiB.",
58:   "all55_sync_stamps_successful": true
59: }
```


## SOURCE docs/qa-logs/2026-10-06-ra-ui/qualification.json

```text
1: {
2:   "qualified_utc": "2026-10-06T07:01:40.373352+00:00",
3:   "source": "7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2",
4:   "candidate_bundle": "b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1",
5:   "assertions": 109,
6:   "failures": 0,
7:   "skips": 0,
8:   "frames_directly_reviewed": 23,
9:   "profiles": [
10:     {
11:       "profile": "en_US-1280x960",
12:       "assertions": 25,
13:       "frames": 5,
14:       "passed": true
15:     },
16:     {
17:       "profile": "en_US-640x480",
18:       "assertions": 34,
19:       "frames": 8,
20:       "passed": true
21:     },
22:     {
23:       "profile": "fr_FR-1280x960",
24:       "assertions": 25,
25:       "frames": 5,
26:       "passed": true
27:     },
28:     {
29:       "profile": "fr_FR-640x480",
30:       "assertions": 25,
31:       "frames": 5,
32:       "passed": true
33:     }
34:   ],
35:   "installed_file_hashes_per_profile": 46,
36:   "same_installed_hashes_all_profiles": true,
37:   "all_four_results_zero": true,
38:   "actual_cleanup_verified_utc": "2026-10-06T07:01:20.488225+00:00",
39:   "boundary": "Synthetic local award/HTTP provider; installed ES/ctl/Storage/flusher. Real provider award remains separate RA33. No whole changed ordinary-runner rerun."
40: }
```


## SOURCE projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth:570–780

```text
570:                     "replaces it" % gone.returncode)
571:             return False, CLOSED_EARLY
572:         log("remote %s created for %s" % (name, self.backend))
573:         return True, name
574: 
575: 
576: # What a closed or replaced attempt's own late ending says, on the phone and
577: # in the log, when it has one to say.
578: CLOSED_EARLY = "That sign-in was closed before it finished."
579: 
580: # One remote created at a time in this process (Session._create_remote).
581: _CREATE_LOCK = threading.Lock()
582: 
583: 
584: # rclone's backend names are lowercase identifiers ("dropbox", "onedrive").
585: # They are not what the provider calls itself, and a page headed "Connect
586: # dropbox" reads like a typo on the one screen where the player is deciding
587: # whether to trust us with their storage. The handheld passes the curated name
588: # it already shows in its own menu; this map is the fallback for a backend
589: # reached some other way, and title-casing is the fallback for that.
590: DISPLAY_NAMES = {
591:     "acd": "Amazon Drive", "box": "Box", "drive": "Google Drive",
592:     "dropbox": "Dropbox", "gcs": "Google Cloud Storage",
593:     "gphotos": "Google Photos", "hidrive": "HiDrive", "jottacloud": "Jottacloud",
594:     "mailru": "Mail.ru Cloud", "onedrive": "Microsoft OneDrive",
595:     "opendrive": "OpenDrive", "pcloud": "pCloud",
596:     "premiumizeme": "premiumize.me", "putio": "put.io",
597:     "sharefile": "Citrix ShareFile", "sugarsync": "SugarSync",
598:     "yandex": "Yandex Disk", "zoho": "Zoho WorkDrive",
599:     "filefabric": "Enterprise File Fabric",
600: }
601: 
602: 
603: def display_name(backend, label=None):
604:     # Our curated name wins where we have one: rclone's descriptions are
605:     # written for its documentation ("Google Cloud Storage (this is not Google
606:     # Drive)"), which is accurate and wrong as a page heading. The passed
607:     # label -- rclone's description, by way of the handheld's menu -- covers
608:     # everything else, and title-casing covers a backend reached from a shell.
609:     if backend in DISPLAY_NAMES:
610:         return DISPLAY_NAMES[backend]
611:     if label:
612:         return label
613:     return backend.replace("_", " ").title()
614: 
615: 
616: # Single %, not %%: this is substituted into the templates as a *value*
617: # (%(style)s), so its percent signs are never seen by the formatter. Escaping
618: # them the way the templates do shipped "width:100%%" as literal CSS, which
619: # every browser discards -- which is how a four-character PIN box ended up
620: # rendering at its default twenty-character width with wide letter spacing,
621: # overflowing the card on a phone.
622: STYLE = """
623: body{font:16px/1.5 system-ui,sans-serif;margin:0;padding:20px;background:#111;color:#eee}
624: .card{max-width:34rem;margin:0 auto}
625: h1{font-size:1.3rem;margin:0 0 .25rem}
626: h2{font-size:1rem;margin:1.5rem 0 .5rem;color:#9cf;text-transform:uppercase;
627:    letter-spacing:.05em}
628: ol{padding-left:1.3rem;margin:.5rem 0}li{margin:.4rem 0}
629: a.go{display:block;background:#2d7;color:#000;padding:14px;border-radius:8px;
630:      text-align:center;font-weight:600;text-decoration:none;margin:.5rem 0}
631: input{width:100%;padding:12px;font-size:16px;border-radius:8px;border:1px solid #555;
632:       background:#1c1c1c;color:#eee;box-sizing:border-box}
633: /* Four characters do not need the width of a phone. Sized in ch so it tracks
634:    the font rather than assuming one, and capped against the card so it still
635:    shrinks rather than overflowing on a narrow screen. */
636: input.pin{font-size:24px;letter-spacing:.5em;text-align:center;
637:           width:7ch;max-width:100%;padding-left:.6em}
638: form.narrow{text-align:center}
639: form.narrow button{width:auto;min-width:9rem}
640: button{margin-top:10px;padding:12px 20px;font-size:16px;border-radius:8px;
641:        border:0;background:#4af;color:#000;font-weight:600;width:100%}
642: button.minor{background:#333;color:#ddd;font-weight:500}
643: .note{color:#aaa;font-size:.9rem}
644: /* The connection line sits between the heading and the field; without
645:    margins of its own it read as part of both (fork #351). */
646: #state{margin:.75rem 0}
647: /* The way off the handheld's page lives at the very bottom, under the note,
648:    with room above it, so a drag on the pad that runs off its edge lands
649:    on text and not on Close (fork #351, D-CLOUD-163). Its two-step
650:    confirmation replaces the row in place. */
651: [hidden]{display:none!important}
652: .leave{margin-top:2rem}
653: .leave .ask{display:flex;gap:8px;align-items:center}
654: .leave .ask span{flex:1 1 auto;color:#aaa;font-size:.9rem}
655: .leave .ask button{flex:0 0 auto;width:auto;padding:12px 18px;margin-top:0}
656: .err{background:#722;padding:12px;border-radius:8px;margin:1rem 0}
657: .ok{background:#272;padding:12px;border-radius:8px;margin:1rem 0}
658: .box{border:1px solid #444;border-radius:10px;padding:14px;margin:1rem 0}
659: .big{font-size:1.6rem;text-align:center;margin:1rem 0}
660: /* Five buttons on a phone's 350 px share the row from a basis of nothing
661:    (flex:1 1 0) and may shrink below their words (min-width:0, which flex
662:    items refuse by default); width:auto undoes the block rule's 100%, which
663:    as a basis put every button on a row of its own. Show sat off the right
664:    edge of an iPhone's screen (fork #330). */
665: .keys{display:flex;gap:8px;margin-top:10px}
666: .keys button{flex:1 1 0;min-width:0;width:auto;padding:12px 6px;margin-top:0}
667: /* The trackpad. Tall enough to drag across a four-inch screen's worth of
668:    page without lifting a finger, and touch-action:none so the browser does
669:    not steal the gesture to scroll its own page. */
670: .pad{height:11rem;margin-top:12px;border:1px dashed #555;border-radius:10px;
671:      background:#181818;touch-action:none;display:flex;align-items:center;
672:      justify-content:center;color:#666;font-size:.85rem;user-select:none}
673: .pad.live{border-color:#4af;color:#4af}
674: """
675: 
676: # The paste field sits ABOVE the sign-in button on purpose. Somebody arriving
677: # here for the first time reads the numbered steps and goes down to the button;
678: # somebody arriving the *second* time -- back from the provider, holding an
679: # address that expires in about two minutes -- needs the box to be the first
680: # thing on the screen, not something below a large green button that looks like
681: # the action. Getting that wrong cost a real sign-in: the tester approved
682: # access, could not see where the address went, and by the time they found it
683: # the code had expired (fork #51).
684: PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
685: <title>Connect %(name)s</title>
686: <style>%(style)s</style>
687: <div class=card>
688: <h1>Connect %(name)s</h1>
689: <p class=note>Keep this page open. You will come back to it.</p>
690: %(message)s
691: 
692: %(here)s
693: <h2>1. Sign in and approve access</h2>
694: <a class=go href="%(provider)s" target="_blank" rel="noopener">Sign in to %(name)s</a>
695: <p class=note>Opens in a new tab, so <strong>this page stays where it
696: is</strong>. Approve access, then come straight back here — what you bring
697: back is only good for a couple of minutes.</p>
698: 
699: <h2>2. Paste the address it lands on</h2>
700: <p class=note>Approving sends the browser to an address it cannot open, so it
701: shows an error — <em>"Safari cannot open the page"</em>, <em>"This site can't
702: be reached"</em>, or similar. <strong>That error page is the point: its
703: address is what we need.</strong> Tap its address bar, copy the whole thing,
704: come back to this tab and paste it below.</p>
705: <form method=post id=f>
706: <input name=code placeholder="Paste here" autofocus
707:        autocapitalize=off autocorrect=off spellcheck=false inputmode=url>
708: <input type=hidden name=pin value="%(pin)s">
709: <button type=submit>Confirm</button>
710: </form>
711: <script>
712: // Paste and it goes -- what was pasted expires in about two minutes, and the
713: // tester who lost one spent them looking for the button.
714: document.querySelector("input[name=code]").addEventListener("paste", function () {
715:   var f = document.getElementById("f");
716:   setTimeout(function () { if (this.value.indexOf("code=") >= 0) f.submit(); }.bind(this), 50);
717: });
718: </script>
719: 
720: <form method=post>
721: <input type=hidden name=pin value="%(pin)s">
722: <input type=hidden name=restart value="1">
723: <button class=minor type=submit>Lost the address? Start over</button>
724: </form>
725: </div>
726: """
727: 
728: # Typing an address into a phone is the fallback for a phone that cannot scan,
729: # and it has to stay short enough to type -- so the PIN is asked for here
730: # rather than carried in the address. Scanning the QR skips this page, because
731: # the QR encodes the PIN.
732: PIN_PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
733: <title>pixelelated cloud sign-in</title>
734: <style>%(style)s</style>
735: <div class=card>
736: <h1>Almost there</h1>
737: %(message)s
738: <p>The address on the handheld ends in four digits. Type them here.</p>
739: <form method=get action="/" class=narrow>
740: <input class=pin name=pin inputmode=numeric pattern="[0-9]*" maxlength=4 autofocus
741:        autocomplete=off placeholder="0000" value="%(pin)s">
742: <button type=submit>Continue</button>
743: </form>
744: <p class=note>They are a PIN. This page is open to everyone on your network
745: while setup is running, and the PIN is what stops somebody else finishing the
746: sign-in with their own account. Scanning the code on the handheld fills it in
747: for you.</p>
748: </div>
749: """
750: 
751: DONE_PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
752: <title>Connected</title>
753: <style>%(style)s</style>
754: <div class=card>
755: <h1>Connected</h1>
756: <div class=ok>%(name)s is set up on your handheld as <strong>%(remote)s</strong>.</div>
757: <div class=big>Go back to the handheld<br>and choose CONTINUE</div>
758: <p class=note>You can close this page.</p>
759: </div>
760: """
761: 
762: 
763: SIGNIN_WINDOW = "/usr/bin/cloud-signin-window"
764: UINPUT = "/dev/uinput"
765: 
766: 
767: def sway_env():
768:     """Enough environment to talk to the running sway over its IPC socket."""
769:     session = running_session()
770:     if not session:
771:         return {}
772:     runtime, display = session
773:     env = {"XDG_RUNTIME_DIR": runtime, "WAYLAND_DISPLAY": display}
774:     for name in sorted(os.listdir(runtime)):
775:         if name.startswith("sway-ipc.") and name.endswith(".sock"):
776:             env["SWAYSOCK"] = os.path.join(runtime, name)
777:             break
778:     return env
779: 
780: 
```


## SOURCE projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth:975–1190

```text
975: <h1>Keyboard for %(name)s</h1>
976: 
977: <div id=state class=note>Checking&hellip;</div>
978: 
979: <input id=kb type=password placeholder="Type here" autocapitalize=off
980:        autocorrect=off spellcheck=false autofocus>
981: <div id=warn class=err hidden></div>
982: <div class=keys>
983: <button type=button class=minor data-key=backspace>Back</button>
984: <button type=button class=minor data-key=tab>Tab</button>
985: <button type=button class=minor data-key=enter>Enter</button>
986: <button type=button class=minor id=clear>Clear</button>
987: <button type=button class=minor id=show>Show</button>
988: </div>
989: 
990: 
991: <div class=keys>
992: <button type=button class=minor data-key=left>&larr;</button>
993: <button type=button class=minor data-key=up>&uarr;</button>
994: <button type=button class=minor data-key=down>&darr;</button>
995: <button type=button class=minor data-key=right>&rarr;</button>
996: </div>
997: <div class=keys>
998: <button type=button class=minor data-key=f2>Page up</button>
999: <button type=button class=minor data-key=f3>Page down</button>
1000: </div>
1001: <h2>Pointer</h2>
1002: <div class=pad id=pad>drag to move &middot; tap to click</div>
1003: 
1004: <p class=note>The sign-in page is on your handheld&rsquo;s screen, not here.
1005: This types for it, so you can more easily retrieve and type your login
1006: info. What you type crosses your network unencrypted, so use this on a
1007: network you trust.</p>
1008: 
1009: <!-- A way off the handheld's page that does not depend on its gamepad: a
1010:      pad the bridge cannot read (#308 gpt F-RS-16) leaves this, and the
1011:      window quits on Escape. At the bottom, under the note, because it sat
1012:      right above the drag pad and a thumb found it by accident (fork #351);
1013:      and asked once, in place, before Escape is sent (D-CLOUD-163). -->
1014: <div class=leave id=leave>
1015: <button type=button class=minor id=leave-ask>Close page</button>
1016: <div class=ask id=leave-confirm hidden><span>Close the sign-in page on your handheld?</span>
1017: <button type=button class=minor id=leave-keep>Keep</button><button type=button id=leave-close>Close</button></div>
1018: </div>
1019: </div>
1020: 
1021: <script>
1022: // A script that dies before it starts leaves the page saying Checking... for
1023: // as long as it is open, its taps dead (fork #330). Said on the page, with
1024: // the browser's words for the ROCKNIX team, instead of nothing.
1025: window.onerror = function (message) {
1026:   var state = document.getElementById("state");
1027:   if (!state) return;
1028:   state.className = "err";
1029:   state.textContent = "This page stopped working. Reload it; if it happens again, report it to the pixelelated project: " + message;
1030: };
1031: (function () {
1032:   var pin = "%(pin)s";
1033:   var box = document.getElementById("kb");
1034:   var warn = document.getElementById("warn");
1035:   var state = document.getElementById("state");
1036:   var pad = document.getElementById("pad");
1037: 
1038:   // One request at a time, in order. Backspaces and characters that overtake
1039:   // each other arrive as scrambled text in the field on the handheld.
1040:   //
1041:   // Two states from the probe: winUp, the window is on the handheld's
1042:   // screen (the named keys drive it -- Tab is how a field the page did not
1043:   // focus is reached); ready, a field on its page has had the caret, so
1044:   // text has somewhere to go. It was `up` until fork #330 -- the same name
1045:   // as the pad's up(e) below, and a var assigned false over a hoisted
1046:   // function makes addEventListener("touchend", up) throw before poll()
1047:   // ever runs: the page sat on Checking... with its taps dead on every
1048:   // browser, while drags moved the pointer (their handler was bound first).
1049:   var winUp = false;
1050:   var ready = false;
1051:   var page = null;
1052:   var queue = Promise.resolve();
1053:   function send(body) {
1054:     queue = queue.then(function () {
1055:       return fetch("/" + pin, {
1056:         method: "POST",
1057:         headers: {"Content-Type": "application/x-www-form-urlencoded"},
1058:         body: body + "&pin=" + encodeURIComponent(pin)
1059:       }).catch(function () {});
1060:     });
1061:     return queue;
1062:   }
1063: 
1064:   // Two different strings, which is the distinction the first cut missed.
1065:   // `shown` is what is in the box; `sent` is what has actually reached the
1066:   // handheld. They differ whenever somebody types before the page is open --
1067:   // the order this flow asks for, since the QR is on the screen the sign-in
1068:   // page replaces.
1069:   var sent = "";
1070: 
1071:   function deliver(v) {
1072:     if (v === sent) return;
1073:     if (v.length > sent.length && v.indexOf(sent) === 0) {
1074:       send("type=" + encodeURIComponent(v.slice(sent.length)));
1075:     } else if (v.length < sent.length && sent.indexOf(v) === 0) {
1076:       for (var i = 0; i < sent.length - v.length; i++) send("key=backspace");
1077:     } else {
1078:       for (var j = 0; j < sent.length; j++) send("key=backspace");
1079:       if (v) send("type=" + encodeURIComponent(v));
1080:     }
1081:     sent = v;
1082:   }
1083: 
1084:   // Every named key -- from the buttons below and from the phone's own
1085:   // keyboard alike -- goes through here, so the box and the handheld's field
1086:   // never part. The buttons used to post their key and nothing else: Back
1087:   // deleted on the handheld and left the box as it was, and every later
1088:   // keystroke was reckoned against a box one character off, so a password
1089:   // typed with one correction went across altered (audit #307 PL-017).
1090:   //
1091:   // The box holds what has been typed into the handheld's field since the
1092:   // focus last moved there. Back trims it, and with it empty still deletes
1093:   // on the handheld -- text that was there already. Enter submits the field,
1094:   // and Tab, the arrows and Close move away from it: what the box holds was
1095:   // for the field left behind, so it starts again. Page up and down only
1096:   // scroll.
1097:   function act(named) {
1098:     if (named === "backspace") {
1099:       if (box.value) {
1100:         box.value = box.value.slice(0, -1);
1101:         if (ready) deliver(box.value);
1102:       } else if (winUp) {
1103:         send("key=backspace");
1104:       }
1105:       return;
1106:     }
1107:     if (!winUp) return;
1108:     send("key=" + named);
1109:     if (named !== "f2" && named !== "f3") { box.value = ""; sent = ""; dropped = []; warnSay(); }
1110:   }
1111: 
1112:   // Only what the handheld can type goes in the box: printable ASCII,
1113:   // [ -~], the US layout cloud_oauth types with. Anything else used to be
1114:   // sent, dropped at the other end without a word, and left showing here
1115:   // -- a credential altered in silence (#308 claude F-RS-16, gpt F-RS-13).
1116:   // It is taken out of the box instead, and the page says which.
1117:   //
1118:   // The line names the characters only while Show is on. With the box
1119:   // masked it counts them: a password's characters written out under a
1120:   // box that hides them is the box's masking undone (G-C-05, the audit of
1121:   // stream C).
1122:   var dropped = [];
1123:   function warnSay() {
1124:     if (!dropped.length) { warn.hidden = true; return; }
1125:     var many = dropped.length > 1;
1126:     warn.textContent = box.type === "password"
1127:       ? "The handheld can't type " + (many ? dropped.length + " of the characters you entered"
1128:           : "one of the characters you entered") + ", so " + (many ? "they were" : "it was") + " left out."
1129:       : "The handheld can't type " + dropped.join(" ") + ", so "
1130:           + (many ? "they were" : "it was") + " left out.";
1131:     warn.hidden = false;
1132:   }
1133:   function typable() {
1134:     var v = box.value, kept = v.replace(/[^ -~]/g, "");
1135:     if (kept === v) return;
1136:     dropped = v.replace(/[ -~]/g, "").split("");
1137:     box.value = kept;
1138:     warnSay();
1139:   }
1140: 
1141:   // What you typed stays visible. Clearing the box after every keystroke made
1142:   // a keyboard that looked broken -- you type and nothing appears anywhere
1143:   // you can see.
1144:   box.addEventListener("input", function () {
1145:     typable();
1146:     if (ready) deliver(box.value);
1147:   });
1148:   box.addEventListener("keydown", function (e) {
1149:     var named = {Enter: "enter", Backspace: "backspace", Tab: "tab"}[e.key];
1150:     if (!named) return;
1151:     e.preventDefault();
1152:     act(named);
1153:   });
1154: 
1155:   // Masked, because what goes through this box is mostly a password, and
1156:   // it stayed readable on the phone's screen after it was sent (#308 gpt
1157:   // F-RS-14). Show reveals it for checking; it hides again on a second
1158:   // press.
1159:   var show = document.getElementById("show");
1160:   show.addEventListener("click", function () {
1161:     var hidden = box.type === "password";
1162:     box.type = hidden ? "text" : "password";
1163:     show.textContent = hidden ? "Hide" : "Show";
1164:     warnSay();
1165:   });
1166: 
1167:   // Local only: the handheld has moved to another field and this box still
1168:   // holds what went into the last one.
1169:   document.getElementById("clear").addEventListener("click", function () {
1170:     box.value = ""; sent = ""; dropped = []; warnSay(); box.focus();
1171:   });
1172: 
1173:   // Close page asks once, in place, in the words approved for it (D-CLOUD-164
1174:   // string 12): the button gives way to the question with Keep and Close;
1175:   // Keep puts the button back, Close sends Escape as the old button did.
1176:   // Static markup toggled by hidden, nothing built at run time: the page's
1177:   // load test under node has no createElement, and a browser's confirm()
1178:   // cannot carry these words.
1179:   var leaveAsk = document.getElementById("leave-ask"), leaveConfirm = document.getElementById("leave-confirm");
1180:   function leaveShow(asking) { leaveAsk.hidden = asking; leaveConfirm.hidden = !asking; }
1181:   leaveAsk.addEventListener("click", function () { leaveShow(true); });
1182:   document.getElementById("leave-keep").addEventListener("click", function () { leaveShow(false); });
1183:   document.getElementById("leave-close").addEventListener("click", function () { act("escape"); leaveShow(false); });
1184:   Array.prototype.forEach.call(document.querySelectorAll("[data-key]"), function (b) {
1185:     b.addEventListener("click", function () { act(b.dataset.key); });
1186:   });
1187: 
1188:   // Drag to move, tap to click. Deltas rather than absolute positions,
1189:   // because the pointer belongs to the handheld's screen and this pad has no
1190:   // idea how big that is.
```


## SOURCE projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c:420–480

```text
420:  * released -- and closing first left the player looking at a black screen
421:  * immediately after a sign-in that had just succeeded, which reads as a
422:  * crash rather than as progress.
423:  *
424:  * In the phone page's own style (cloud_oauth's STYLE: the dark card, the
425:  * heading, the note), reading as a success and saying what happens next
426:  * (fork #351 section 4; the approved words, D-CLOUD-164 string 13). It was
427:  * one unstyled line, which the maintainer read as "a 404 page or something
428:  * incredibly basic" (2026-09-30). A data: URL, so # is %23 and the page
429:  * needs no file the window would have to find. */
430: static const char *FINISHING_PAGE =
431:     "data:text/html,<meta name=viewport content='width=device-width'>"
432:     "<style>body{font:16px/1.5 system-ui,sans-serif;margin:0;padding:20px;"
433:     "background:%23111;color:%23eee;min-height:100vh;box-sizing:border-box;"
434:     "display:flex;align-items:center;justify-content:center}"
435:     ".card{max-width:34rem;text-align:center}"
436:     "h1{font-size:1.6rem;margin:0 0 .5rem;color:%232d7}"
437:     ".note{color:%23aaa;font-size:1rem}</style>"
438:     "<body><div class=card><h1>Connected</h1>"
439:     "<p class=note>Finishing up on your handheld&hellip;</p></div></body>";
440: 
441: static gboolean probe_tick(gpointer data)
442: {
443:     Osk *osk = data;
444: 
445:     /* cloud_oauth says the sign-in landed. Nothing on the provider's page
446:      * matters from here, and this window is the only thing on the screen
447:      * until EmulationStation is back. */
448:     const char *done_file = g_getenv("CLOUD_SIGNIN_DONE_FILE");
449:     if (done_file && g_file_test(done_file, G_FILE_TEST_EXISTS)) {
450:         webkit_web_view_load_uri(osk->view, FINISHING_PAGE);
451:         if (osk->hints)
452:             gtk_widget_hide(osk->hints);
453:         gtk_revealer_set_reveal_child(GTK_REVEALER(osk->revealer), FALSE);
454:         return G_SOURCE_REMOVE;
455:     }
456:     static const char *script =
457:         "(function () {"
458:         "  var a = document.activeElement;"
459:         /* A provider moves from email to password without loading a page, and
460:          * leaves focus on the body. Nothing then has the caret, so the
461:          * on-screen keyboard has nowhere to type and spatial navigation has
462:          * no anchor to move from -- the password box cannot be selected at
463:          * all, which is where a real sign-in stopped. Adopt a field when the
464:          * page has abandoned focus, never when something else holds it. */
465:         "  if (!a || a === document.body || a.tagName === 'BODY') {"
466:         "    var boxes = document.querySelectorAll("
467:         "      'input[type=text],input[type=email],input[type=password],"
468:         "       input[type=tel],input[type=url],input:not([type]),textarea');"
469:         "    for (var i = 0; i < boxes.length; i++) {"
470:         "      var b = boxes[i], r = b.getBoundingClientRect();"
471:         "      if (!r.width || !r.height || b.disabled || b.readOnly) continue;"
472:         "      if (r.bottom < 0 || r.top > innerHeight) continue;"
473:         "      b.focus();"
474:         "      a = document.activeElement;"
475:         "      break;"
476:         "    }"
477:         "  }"
478:         "  if (!a) return 'none';"
479:         "  var t = (a.tagName || '').toUpperCase();"
480:         "  var ty = (a.type || 'text').toLowerCase();"
```


## SOURCE /home/max/Development/emulationstation-next.worktrees/qa-integration/es-app/src/guis/GuiMenu.cpp:4860–4910

```text
4860: 	auto media = std::make_shared<SwitchComponent>(window);
4861: 	media->setState(hasContent && remembered("media", false));
4862: 	if (hasContent)
4863: 		s->addWithDescription(_("GAME CONTENT"),
4864: 			_("SCRAPED ARTWORK, VIDEOS, MANUALS, AND GAME LISTS"), media);
4865: 
4866: 	auto settings = std::make_shared<SwitchComponent>(window);
4867: 	settings->setState(remembered("settings", false));
4868: 	// On a restore the row is offered only when the cloud holds a settings
4869: 	// backup from this device model (D-CLOUD-162, #349): the scan page before
4870: 	// this one listed the archives by the label in their names (cloud_scan's
4871: 	// settings file, MINE= this device's newest). With none the row stays,
4872: 	// dimmed, with its reason -- es-ui-style-guide.md dims rather than hides
4873: 	// -- and nothing is ticked; offered, its line says which device and when,
4874: 	// the approved "<DEVICE>, <DATE>" (D-CLOUD-164). A backup always has
4875: 	// settings to send, and a page with no scan behind it (older scripts)
4876: 	// reads as it always did.
4877: 	const std::map<std::string, std::string> archives = backup ? std::map<std::string, std::string>() : cloudScanFacts("settings");
4878: 	const bool scanned = !backup && archives.count("MINE") > 0;
4879: 	const CloudText::SettingsArchive mine = scanned ? CloudText::parseSettingsArchive(cloudScanFact(archives, "MINE")) : CloudText::SettingsArchive();
4880: 	if (scanned && !mine.ok)
4881: 	{
4882: 		settings->setState(false);
4883: 		cloudAddDimmedRow(s, window, _("SETTINGS"), _("NO SETTINGS BACKUP FROM THIS DEVICE YET"));
4884: 	}
4885: 	else
4886: 		s->addWithDescription(_("SETTINGS"),
4887: 			// The date in the system's own shape, as every LAST line is
4888: 			// (cloudLastLabel): the formatter knows no month names, and
4889: 			// "%b" printed nothing (guest d, 2026-10-01).
4890: 			scanned ? CloudText::deviceNameFromLabel(mine.label) + ", " + Utils::Time::timeToString(mine.when, Utils::Time::getSystemDateFormat())
4891: 			        : std::string(_("CONFIGURATION, CONTROLS, AND THEMES")), settings);
4892: 
4893: 	// Written on the way out, by whichever exit -- BACK included, because a
4894: 	// tick somebody set and then thought better of running is still their
4895: 	// answer to "what moves". GuiSettings::save() also returns early when a
4896: 	// page registers no save function, so this is what flushes SystemConf.
4897: 	s->addSaveFunc([key, saves, content, media, settings]
4898: 	{
4899: 		auto conf = SystemConf::getInstance();
4900: 		conf->set(key + "saves",    saves->getState()    ? "1" : "0");
4901: 		conf->set(key + "content",  content->getState()  ? "1" : "0");
4902: 		conf->set(key + "media",    media->getState()    ? "1" : "0");
4903: 		conf->set(key + "settings", settings->getState() ? "1" : "0");
4904: 	});
4905: 
4906: 	// The two lines the content page opens with. The first names the
4907: 	// per-system classes -- what the choice of systems on that page applies
4908: 	// to -- separated by middle dots, not joined by AND (one class is called
4909: 	// ROMS AND BIOS). The second names what rides along for the whole device:
4910: 	// settings always; saves too, today, because the saves sync is one pass
```


## SOURCE /home/max/Development/emulationstation-next.worktrees/qa-integration/es-app/src/guis/GuiMenu.cpp:5185–5270

```text
5185: 	}
5186: 
5187: 	window->pushGui(s);
5188: }
5189: 
5190: // The content folder, settled before the content scan on a restore (#352,
5191: // D-CLOUD-156): the scan page found where the games are (cloud_setup
5192: // --content-location). Found under the cloud root's Content folder while
5193: // the configured root holds nothing of ours, the device is pointed there
5194: // with no question -- it is ours, by name. Found nowhere, the approved
5195: // question offers the chooser; NOT NOW goes on to a listing that will say
5196: // no system holds what was ticked. Anything else is as configured.
5197: static void cloudOpenContentFolderChooser(Window* window, const std::function<void()>& then);
5198: static void cloudSetContentFolder(Window* window, const std::string& folder, const std::function<void()>& then)
5199: {
5200: 	window->pushGui(new GuiLoading<std::pair<std::string, std::string>>(window, _("WORKING..."),
5201: 		[folder](IGuiLoadingHandler*)
5202: 		{
5203: 			std::string why, rc;
5204: 			for (auto& line : Utils::Platform::GetShOutputLines(
5205: 				"timeout 30 /usr/bin/cloud_setup --set-content-remote " + Utils::String::shellQuote(folder) + " 2>&1; echo \"RC=$?\""))
5206: 			{
5207: 				const std::string l = Utils::String::trim(line);
5208: 				if (Utils::String::startsWith(l, "RC="))
5209: 					rc = l.substr(3);
5210: 				else if (!l.empty())
5211: 					why += (why.empty() ? "" : "\n") + l;
5212: 			}
5213: 			return std::make_pair(rc, why);
5214: 		},
5215: 		[window, folder, then](std::pair<std::string, std::string> result)
5216: 		{
5217: 			if (result.first != "0")
5218: 			{
5219: 				LOG(LogWarning) << "cloud content folder: " << folder << " was refused: " << result.second;
5220: 				window->pushGui(new GuiMsgBox(window,
5221: 					_("THE CLOUD FOLDER WAS NOT CHANGED") + (result.second.empty() ? "" : "\n\n" + result.second), _("OK"), nullptr));
5222: 				return;
5223: 			}
5224: 			LOG(LogInfo) << "cloud content folder: now " << folder;
5225: 			then();
5226: 		}));
5227: }
5228: static void cloudOfferContentFolder(Window* window, const std::function<void()>& then)
5229: {
5230: 	const auto facts = cloudScanFacts("content-location");
5231: 	const std::string state = cloudScanFact(facts, "STATE");
5232: 	const std::string found = cloudScanFact(facts, "FOUND");
5233: 	if (state == "found-elsewhere" && !found.empty())
5234: 	{
5235: 		LOG(LogInfo) << "cloud content folder: nothing of ours at the configured root; using " << found;
5236: 		cloudSetContentFolder(window, found, then);
5237: 		return;
5238: 	}
5239: 	if (state != "empty")
5240: 	{
5241: 		then();
5242: 		return;
5243: 	}
5244: 	std::string folder = cloudScanFact(facts, "CONTENT_REMOTE");
5245: 	if (folder.empty())
5246: 		folder = "/";
5247: 	window->pushGui(new GuiMsgBox(window,
5248: 		Utils::String::format(_("YOUR CLOUD HAS NO ROMS OR BIOS AT %s.\n\nCHOOSE THE FOLDER WHERE YOUR GAMES ARE?").c_str(), folder.c_str()),
5249: 		_("CHOOSE A FOLDER"), [window, then] { cloudOpenContentFolderChooser(window, then); },
5250: 		_("NOT NOW"), then));
5251: }
5252: // CHOOSE A CLOUD FOLDER (#352, the approved title): the folders at the
5253: // cloud's root, as the scan listed them (root-dirs), the one the scan
5254: // found first when it found one. A press points the device's content root
5255: // there and goes on to the content scan.
5256: static void cloudOpenContentFolderChooser(Window* window, const std::function<void()>& then)
5257: {
5258: 	auto s = new GuiSettings(window, _("CHOOSE A CLOUD FOLDER"));
5259: 	std::vector<std::string> dirs;
5260: 	const std::string found = cloudScanFact(cloudScanFacts("content-location"), "FOUND");
5261: 	if (!found.empty())
5262: 		dirs.push_back(found);
5263: 	std::vector<std::string> roots;
5264: 	cloudScanLines("root-dirs", roots);
5265: 	for (auto& d : roots)
5266: 		if (!d.empty() && "/" + d != found)
5267: 			dirs.push_back("/" + d);
5268: 	if (dirs.empty())
5269: 		cloudSetupAddInfoRow(s, window, _("NONE"), false);
5270: 	for (auto& d : dirs)
```


## docs/decision-register.md:549

| D-CLOUD-164 | 2026-10-01 | **The cloud epic's thirteen player-facing strings are approved as the baseline** (the scan page's title and live line; the dimmed and offered settings-row lines; the folder offer with CREATE IT / CHOOSE A FOLDER / NOT NOW; the move dialog with MOVE / KEEP USING /ROCKNIX / NOT NOW and the move page's running and ended lines; the empty-content-root question; the chooser's title; the sync card's `SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET` with its action line; the phone page's close confirmation; the finishing page's two lines -- the list on #354, 2026-10-01), to be fine-tuned under the rolling release cycle (D-WORKFLOW-094) rather than argued now; each lands with its French (D-UI-051). Maintainer: *"This sounds right to me, and certainly a good starting place. Since we're going to move to a more of a rolling release cycle, we can always fine-tune this later."* | #354 and its children; D-UI-045, D-UI-028/030 (the outcome words) |


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-07-failed/artifacts/cloud-ui/UI26/logs/UI26-future-after-pointers.txt

```text
1: SAVES_REMOTE="/ROCKNIX/Saves"
2: SETTINGS_REMOTE="/ROCKNIX/Backups"
3: CONTENT_REMOTE="/ROCKNIX/Content"
4: LAYOUT_KEEP="/ROCKNIX/Saves"
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-07-failed/artifacts/cloud-ui/UI26/logs/UI26-future-before-pointers.txt

```text
1: SAVES_REMOTE="/ROCKNIX/Saves"
2: SETTINGS_REMOTE="/ROCKNIX/Backups"
3: CONTENT_REMOTE="/ROCKNIX/Content"
4: LAYOUT_KEEP="/ROCKNIX/Saves"
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-07-failed/artifacts/cloud-ui/UI26/logs/UI26-future-interface.log

```text
1: 2026-10-05 05:31:47	[2139]	INFO	CloudTransferJob: CHECKING YOUR CLOUD exited 4 (0 files, 0 bytes, 0 tiers reported)
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-07-failed/artifacts/cloud-ui/UI26/logs/UI26-future-script.log

```text
1: >>> unit CLOUD FOLDER||
2: >>> doing scan
3: >>> why COULDN'T FIND YOUR CLOUD FOLDER
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-07-failed/artifacts/cloud-ui/UI26/logs/UI26-malformed-after-pointers.txt

```text
1: SAVES_REMOTE="/ROCKNIX/Saves"
2: SETTINGS_REMOTE="/ROCKNIX/Backups"
3: CONTENT_REMOTE="/ROCKNIX/Content"
4: LAYOUT_KEEP="/ROCKNIX/Saves"
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-07-failed/artifacts/cloud-ui/UI26/logs/UI26-malformed-before-pointers.txt

```text
1: SAVES_REMOTE="/ROCKNIX/Saves"
2: SETTINGS_REMOTE="/ROCKNIX/Backups"
3: CONTENT_REMOTE="/ROCKNIX/Content"
4: LAYOUT_KEEP="/ROCKNIX/Saves"
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-07-failed/artifacts/cloud-ui/UI26/logs/UI26-malformed-interface.log

```text
1: 2026-10-05 05:30:22	[2148]	INFO	CloudTransferJob: CHECKING YOUR CLOUD exited 4 (0 files, 0 bytes, 0 tiers reported)
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-07-failed/artifacts/cloud-ui/UI26/logs/UI26-malformed-script.log

```text
1: >>> unit CLOUD FOLDER||
2: >>> doing scan
3: >>> why COULDN'T FIND YOUR CLOUD FOLDER
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-08/artifacts/cloud-ui/UI26/logs/UI26-future-after-pointers.txt

```text
1: SAVES_REMOTE="/ROCKNIX/Saves"
2: SETTINGS_REMOTE="/ROCKNIX/Backups"
3: CONTENT_REMOTE="/ROCKNIX/Content"
4: LAYOUT_KEEP="/ROCKNIX/Saves"
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-08/artifacts/cloud-ui/UI26/logs/UI26-future-before-pointers.txt

```text
1: SAVES_REMOTE="/ROCKNIX/Saves"
2: SETTINGS_REMOTE="/ROCKNIX/Backups"
3: CONTENT_REMOTE="/ROCKNIX/Content"
4: LAYOUT_KEEP="/ROCKNIX/Saves"
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-08/artifacts/cloud-ui/UI26/logs/UI26-future-interface.log

```text
1: 2026-10-05 05:43:38	[2143]	INFO	CloudTransferJob: CHECKING YOUR CLOUD exited 4 (0 files, 0 bytes, 0 tiers reported)
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-08/artifacts/cloud-ui/UI26/logs/UI26-future-script.log

```text
1: >>> unit CLOUD FOLDER||
2: >>> doing scan
3: >>> why COULDN'T FIND YOUR CLOUD FOLDER
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-08/artifacts/cloud-ui/UI26/logs/UI26-malformed-after-pointers.txt

```text
1: SAVES_REMOTE="/ROCKNIX/Saves"
2: SETTINGS_REMOTE="/ROCKNIX/Backups"
3: CONTENT_REMOTE="/ROCKNIX/Content"
4: LAYOUT_KEEP="/ROCKNIX/Saves"
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-08/artifacts/cloud-ui/UI26/logs/UI26-malformed-before-pointers.txt

```text
1: SAVES_REMOTE="/ROCKNIX/Saves"
2: SETTINGS_REMOTE="/ROCKNIX/Backups"
3: CONTENT_REMOTE="/ROCKNIX/Content"
4: LAYOUT_KEEP="/ROCKNIX/Saves"
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-08/artifacts/cloud-ui/UI26/logs/UI26-malformed-interface.log

```text
1: 2026-10-05 05:42:12	[2140]	INFO	CloudTransferJob: CHECKING YOUR CLOUD exited 4 (0 files, 0 bytes, 0 tiers reported)
```


## SOURCE docs/qa-logs/2026-10-05-pixelelated-replacement-09/cloud-ui-08/artifacts/cloud-ui/UI26/logs/UI26-malformed-script.log

```text
1: >>> unit CLOUD FOLDER||
2: >>> doing scan
3: >>> why COULDN'T FIND YOUR CLOUD FOLDER
```
