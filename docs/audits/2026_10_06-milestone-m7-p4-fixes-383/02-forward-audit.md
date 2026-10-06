# Forward audit — M7 P4 fixes (#383)

**Auditor:** code-auditor skill, Codex/OpenAI primary
**Date:** 2026-10-06
**Subject:** independent review of the frozen candidate and owning fixes
**Spec:** inputs/scoped-criteria.json; exact primary issue snapshots.

E denotes the pinned ES checkout at /home/max/Development/emulationstation-next.worktrees/qa-integration, HEADf6f0c134. All paths beginning docs/ are repository-relative.

## Running notes

### AC-I320-L32

> `recordLastGood` is taken under the same lock as the read it records, or compares the live file's identity (size and mtime, or a hash) before publishing and skips when it changed: the `es-conf-tests` case `a script's newer good state published between the read and the record is not overwritten` seen to FAIL on the code before the fix and PASS after.

**Source:** #320, inputs/issues/320.md:32
**Checked:** 2026-10-06T15:09:08.109811+00:00
**Verdict:** PASS ✓

**Evidence:** E/es-core/src/SystemConf.cpp:86–108 reacquires PidLock and compares the complete current choice before atomic publication; E/es-app/tests/unit/SystemConfTests.cpp:465–486 constructs the intervening newer script publication. Fresh evidence/es-checks-02/activity/es-conf.log:10 cases/119 assertions pass, rc0; checks.json retains compile/run argv and sealed exact ES source. Original settings-before.log at docs/qa-logs/2026-10-03-m7-p1 fails this assertion.

**Refutation attempted:** Attempted stale-snapshot overwrite after another lock owner publishes both live and recovery bytes; old production source fails, current source leaves the newer text and0600 mode. Current source comparison also rejects an incomplete non-record choice.

**Notes:** Host compiled test proves the synchronization branch, separately from the installed target evidence below.

### AC-I320-L33

> The `LockBusy` path does not publish a recovery record from a read it could not lock: a second `es-conf-tests` case, seen to FAIL first.

**Source:** #320, inputs/issues/320.md:33
**Checked:** 2026-10-06T15:09:08.109811+00:00
**Verdict:** PASS ✓

**Evidence:** E/es-core/src/SystemConf.cpp:250–266 skips record publication on RecoveryWrite::LockBusy for both temporary and backup recovery. SystemConfTests.cpp:488–505 holds the real lock and supplies divergent complete temporary/recovery states. Fresh10-case/119-assertion execution rc0; prior settings-before.log records its specific failed recovery-record comparison.

**Refutation attempted:** The held-lock test would fail if either recovery path published the chosen temporary over the holder record; current source blocks that publication. The live-file branch also must acquire the lock inside recordLastGood.

**Notes:** The guarded publication handles both recovery source cases; reading an unlocked snapshot is not treated as permission to write it.

### AC-I320-L34

> On a guest, a script write of `system.cfg` raced against the interface's recovery (a damaged live file restored at start-up while `set_setting` writes) leaves the last-good record at the script's newer state: the record's bytes compared after the race, in `tools/vm-qa`'s `last-good` suite or a proof script under `docs/qa-frames/`.

**Source:** #320, inputs/issues/320.md:34
**Checked:** 2026-10-06T15:09:08.109811+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/settings-11/artifacts/result.json and guest.log retain20 installed checks: same ES PID1989 pauses after lock release, actual shell writers publish newer state, resumed ES preserves identical live/record SHA256c185423fc387f230447eec8c54c9beaaadd538af08d82fc99fcc14729ea416d3. Fresh current14 staged hashes match all three recorded installed ES/profile/chksysconfig bytes exactly.

**Refutation attempted:** Checked that the fixture actually pauses the installed process, releases the lock and writes newer bytes before resumption; it rejects missing interleaving. Initial damaged hash differs from recovered/newer hashes, preventing a no-op pass. Installed files and owned original settings are restored/unchanged.

**Notes:** This is explicitly the replacement09 installed execution on byte-identical relevant current14 payloads, not a claimed new14 race run. Current14 default/RC2 qualification is evaluated separately.

### AC-I320-L35

> `docs/audits/2026_09_29-milestone-audit-of-the-313-fixes/05-punch-list.md` § Deferred cites this issue, and its Phase 7 row records the commit.

**Source:** #320, inputs/issues/320.md:35
**Checked:** 2026-10-06T15:09:08.109811+00:00
**Verdict:** PASS ✓

**Evidence:** docs/audits/2026_09_29-milestone-audit-of-the-313-fixes/05-punch-list.md:83 retains the #320 deferral;113–123 add the Phase7 follow-up naming full ES39f8883545537d5274708ea85c4683612078a957 and guest-proof boundary.

**Refutation attempted:** Read only the required historical #320 resolution metadata after independently deriving the current three behavior criteria. It explicitly retains the historical deferral and does not claim the source fix alone qualified a guest.

**Notes:** This criterion requires the old resolution row itself; no prior375/382/411 acceptance answer key has been opened.

### AC-I349-L29

> On the transfer page, the SETTINGS restore row's line under the label names the device the archive to be restored came from, read from the label in its file name (`backuptool` prints it; the interface reads it): a 640x480 frame from a `tools/vm-walks` walk shows `<DEVICE>, <DATE>` (D-CLOUD-164).

**Source:** #349, inputs/issues/349.md:29
**Checked:** 2026-10-06T15:13:02.584638+00:00
**Verdict:** PASS ✓

**Evidence:** E/es-app/src/guis/GuiMenu.cpp:4878–4894 parses MINE and displays the archive label/date. Directly reviewed evidence/archive-frames/04-A-options-after-move.png shows GENERIC X64,09/30/2026 at640x480, from guest11 on replacement09.

**Refutation attempted:** Compared foreign-only frame04-C-after-scan.png: the row is dimmed with a reason instead of presenting a foreign device/date. The label/date uses the selected archive filename, not merely the current hostname.

**Notes:** Retained09 execution; ES and cloud-source continuity to14 is recorded separately.

### AC-I349-L33

> `docs/es-menu-map.md` carries the SETTINGS row's two states, offered with the device and date or dimmed with `NO SETTINGS BACKUP FROM THIS DEVICE YET` (D-UI-039, D-CLOUD-162), and `tools/es-menu-map-check` passes in `tools/vm-qa`'s `menumap` suite. *(Rewritten 2026-10-01: the choice page it named is superseded.)*

**Source:** #349, inputs/issues/349.md:33
**Checked:** 2026-10-06T15:13:02.584698+00:00
**Verdict:** PASS ✓

**Evidence:** docs/es-menu-map.md:139 includes both SETTINGS states. Fresh tools/es-menu-map-check --es-src E exited0 (host-checks-01/activity/menu-map.log).

**Refutation attempted:** Read the actual map row rather than relying on the guard alone; offered device/date and the exact dimmed reason are both present.

**Notes:** The earlier choice-page wording is explicitly superseded in the criterion.

### AC-I349-L34

> The public page for cloud sync says the SETTINGS row restores this device's own newest backup and is dimmed when the cloud has none from it (docs follow-up with #42, `documentation-accuracy.md`). *(Rewritten 2026-10-01: a restore from another device is not offered.)*

**Source:** #349, inputs/issues/349.md:34
**Checked:** 2026-10-06T15:13:02.584725+00:00
**Verdict:** SKIP ○

**Evidence:** #344 contract publication stages and docs/rasteratops/release-readiness.md retain public-site delivery as a later gate; the website follow-up remains tracked with#42.

**Refutation attempted:** Did not infer website publication from changed source docs or local screenshots. Existing website403/404 access failure remains disclosed.

**Notes:** Explicitly outside this P4 product-fixes gate. Public documentation is still owed before the applicable publication gate; no site-completion claim.

### AC-I349-L42

> After the scan page (#350), the SETTINGS restore row is offered only when the cloud's Backups folder holds an archive whose label equals this device's `cloud_device_id --label`; with the QA cloud seeded with a foreign label only, guest d's 640x480 frame shows the row dimmed with its reason, and with its own label seeded the row is offered with `<DEVICE>, <DATE>` (D-CLOUD-164) under it.

**Source:** #349, inputs/issues/349.md:42
**Checked:** 2026-10-06T15:13:02.584746+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_scan:214–239 writes label-filtered MINE; GuiMenu.cpp:4878–4894 disables absent/invalid MINE. Guest11 C/logs/run.log records completed foreign-only scan with empty MINE; evidence/archive-frames/04-C-after-scan.png and04-A-options-after-move.png directly show the two required row states.

**Refutation attempted:** Checked completed-scan sentinel, empty MINE, and visible dimming against the positive own-label case; not merely an empty or unfinished page.

**Notes:** Foreign archive availability alone does not enable the UI row; the deliberately broader console fallback is a separate D-CLOUD-067 contract.

### AC-I349-L43

> A restore never takes another device's archive by default: the cloud restore selects this device model's newest compatible archive and passes it to `backuptool`, and its journal line names the label it chose; the foreign-label case on guest d leaves `system.hostname` unchanged.

**Source:** #349, inputs/issues/349.md:43
**Checked:** 2026-10-06T15:13:02.584772+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** cloud_restore:2046–2140 shares the directory selector and chooses the own-label newest archive before its explicitly permitted console fallback. Runtime12 archive/writer-selection.json and022/023/026/027.log prove the selected archive is restored and sentinel bytes agree. Guest11 C shows the UI row disabled.

**Refutation attempted:** Read tools/rasteratops-vm-cloud-epic:213–219: caseC asserts empty MINE/completed scan and dismisses the page, but does not compare system.hostname before/after. Therefore its PASS line cannot independently prove the exact unchanged-hostname clause.

**Notes:** This is a narrow missing assertion in retained evidence, not a reproduced foreign-restore product defect. The console fallback is intentional and not grounds for removing it.

**Gaps:** Locate a separate retained foreign-only UI hostname comparison or execute that bounded assertion on an owned candidate guest. Carry the proof gap until resolved.

### AC-I349-L44

> The scan page's line reads, while it runs, the words approved for #350 (proposed: `CHECKING WHAT SETTINGS AND CONTENT YOUR CLOUD HAS FOR THIS DEVICE...`), and the outcome vocabulary when it ends (`es-player-text.md`); frames from the walk show both.

**Source:** #349, inputs/issues/349.md:44
**Checked:** 2026-10-06T15:13:02.584791+00:00
**Verdict:** PASS ✓

**Evidence:** E/es-app/src/guis/GuiCloudTransfer.cpp:1003–1011 selects the approved full sentence or whole-clause640px fallback. Directly reviewed H scan frames in evidence/archive-frames show CHECKING WHAT YOUR CLOUD HAS FOR THIS DEVICE..., with phases1 and3; A completed options are the successful auto-continued outcome.

**Refutation attempted:** Original PNGs were opened from the retained owner, rather than inferred from the copied selected-frame subset. The shorter wording is implemented deliberately under D-UI-035 and fits the640px line.

**Notes:** The full proposed long string is not claimed to fit640px; documented size-aware wording preserves the meaning.

### AC-I392-L18

> Empty/failed remote discovery produces a nonzero setup refusal for both transfer scripts, with unchanged pointers/payloads and no create-folder offer; before/after production-script receipts retained.

**Source:** #392, inputs/issues/392.md:18
**Checked:** 2026-10-06T15:15:25.965233+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_backup:2446–2460 and cloud_restore:2225–2238 require a nonempty remote prefix ending in colon before path operations. Original docs/qa-logs/2026-10-03-m7-coverage/unlinked-before.log has four failures; unlinked-after.log has13 passes. Fresh evidence/host-checks-01/activity/cloud-layout.log passes each empty/failed-discovery T19 case.

**Refutation attempted:** Both missing remote and failed remote enumeration are supplied independently to both whole production transfer scripts; their setup refusal is nonzero and no create-folder offer is accepted.

**Notes:** No empty prefix can make the later rclone path silently local.

### AC-I392-L19

> A writable local path supplied as the cloud path is not read or written when no remote is linked; configured-cloud controls continue to pass.

**Source:** #392, inputs/issues/392.md:19
**Checked:** 2026-10-06T15:15:25.965313+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh T19-local-path-cloud_backup/cloud_restore cases in evidence/host-checks-01/activity/cloud-layout.log exercise actual writable local-path fixtures; the original unlinked-before.log records allfour failures. Configured-cloud actors in the same316-case run pass.

**Refutation attempted:** The adversarial cloud path names a writable local fixture, so unchanged bytes is meaningful; it is not a permission-error substitute for missing-remote validation.

**Notes:** The fixture tests both empty config and failed discovery before path use.

### AC-I392-L20

> Candidate guest evidence records the refusal/outcome and unchanged bytes for direct and automatic calls.

**Source:** #392, inputs/issues/392.md:20
**Checked:** 2026-10-06T15:15:25.965339+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest-11/artifacts/cloud-epic/T19/logs/run.log:12 actual installed assertions, covering direct/automatic backup/restore setup refusal and unchanged cloud bytes/pointers. Source continuity09→14 is in evidence/candidate-product-continuity.json.

**Refutation attempted:** Each of four invocation shapes verifies refusal, no local-path treatment and no cloud/pointer changes; a no-op before script execution cannot satisfy the required setup outcome.

**Notes:** Retained09 target execution plus fresh host regressions; no new14 target execution claimed.

### AC-I421-L23

> All four settings writers preserve restrictive input modes, including a private recovery record and permissive pre-existing temporary, with byte-correct set/delete/sort/pair operations; old-source controls fail and corrected controls pass.

**Source:** #421, inputs/issues/421.md:23
**Checked:** 2026-10-06T15:15:25.965359+00:00
**Verdict:** PASS ✓

**Evidence:** 001-functions:385 prepare_settings_temp intersects source modes and caller umask before bytes are written; four callers at429/460/494/598 gate publication on it. docs/qa-logs/2026-10-04-settings-race-and-modes/modes-old.json records22 failing controls; modes-new.json passes29. Fresh host-checks01 scripts.log repeats the29 cases using current14 image tools.

**Refutation attempted:** Private live/record, permissive preexisting temp and restricted group inputs are separate cases for each writer; the old source actually widens modes to0644/0666, whereas the corrected target-mode matrix preserves0600/0640 and exact content.

**Notes:** The helper rejects a symlink temporary and invalid stat/chmod results; all four literal call sites were read.

### AC-I421-L24

> chksysconfig backup/restore retains the privacy of its source/destination; failures leave original published bytes and report failure.

**Source:** #421, inputs/issues/421.md:24
**Checked:** 2026-10-06T15:15:25.965377+00:00
**Verdict:** PASS ✓

**Evidence:** chksysconfig:69–78 put prepares restrictive destination temporary, streams with cat, then atomically renames. modes-new.json and installed replacement09 settings11/artifacts/modes.json cover backup/restore in allfour mode states plus five refusal cases; fresh scripts.log passes them again.

**Refutation attempted:** A copy command that resets prepared permissions is avoided; symlink/chmod/stat/producer/rename faults return1 and do not publish replacement bytes.

**Notes:** The fixture invokes production functions and image BusyBox; installed runtime evidence separately confirms the target.

### AC-I421-L25

> Corrected image clean/actual-RC2 qualification plus installed settings-race/mode proof pass; exact hashes bind the new candidate and original02163 results remain retained.

**Source:** #421, inputs/issues/421.md:25
**Checked:** 2026-10-06T15:15:25.965393+00:00
**Verdict:** PASS ✓

**Evidence:** replacement09 settings11 result.json has20 installed race/identity checks and modes.json29 cases. Fresh evidence/settings-payload14.json matches ES,profile,chksysconfig and BusyBox hashes exactly. Current14 qa18/defaults/report.md has all15 suites and qa18/upgrade/rehearsal.log records actual RC2→7afa9efcfc state preservation. Original02163 receipts remain under2026-10-04-pixelelated-02163-qualification.

**Refutation attempted:** Compared actual executable hashes rather than package names or build IDs alone; the retained race names same ES PID and newer record hash. Current upgrade log explicitly stages the from-ROCKNIX tar and confirms new build after reboot.

**Notes:** Targeted09 execution is reused only for identical relevant installed bytes, with current14 clean/RC2 qualification named separately.

### AC-I376-L22

> A regression case runs the production reader with RASTERATOPS OS identity and selects the same-device legacy ROCKNIX archive; its negative control at the old commit fails. The suite's PASS lines and fixture bytes are retained.

**Source:** #376, inputs/issues/376.md:22
**Checked:** 2026-10-06T15:20:17.437222+00:00
**Verdict:** PASS ✓

**Evidence:** Production rasteratops-settings-archive:1-43 and cloud_scan:190-249 retain ROCKNIX/RASTERATOPS names. docs/qa-logs/2026-10-02-cloud-remediation/baseline-results.json records the actual T24 writer-directory/legacy failures; focused-fixed-results.json records their corrected selection. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.

**Refutation attempted:** Compared the writer-shaped per-device negative controls against flat-root controls; flat-root success alone previously concealed this bug.

**Notes:** The legacy suffix is a compatibility contract; ARCHIVE_OS_NAME remains ROCKNIX in backuptool.

### AC-I376-L23

> New/legacy same-device and foreign-device fixtures prove selection prefers this device model's newest compatible archive, the transfer-page SETTINGS row is gated on MINE (D-CLOUD-156/162), and the console retains its deliberate NEWEST fallback when only a foreign archive exists (D-CLOUD-067); selected names and restored sentinel hashes are retained.

**Source:** #376, inputs/issues/376.md:23
**Checked:** 2026-10-06T15:20:17.437279+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-archives-runtime/extended/selection-matrix.json retains current, legacy, healed-ID, flat and foreign-only selected filenames plus sentinel hashes; GuiMenu.cpp:4878-4894 gates the row on MINE. cloud_restore:2030-2170 keeps the documented console fallback. docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest-11/artifacts/cloud-epic/C/logs/run.log and evidence/archive-frames/ retain disabled foreign-only UI. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.

**Refutation attempted:** The foreign-only console restoration is deliberate D-CLOUD-067; it does not contradict the stricter UI gate. The separate hostname assertion gap stays PARTIAL at I349-L43.

**Notes:** Selection is newest matching label within the first nonempty directory, not globally newest across all directories (D-CLOUD-068).

### AC-I376-L24

> Local backup, pre-restore snapshot, revert and retention cases prove the documented legacy/new-name contract without dropping recoverable files; retained names and restored sentinel hashes are in the log.

**Source:** #376, inputs/issues/376.md:24
**Checked:** 2026-10-06T15:20:17.437308+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-archives-runtime/local-recovery/assertions.json and recovery-cases.json contain actual ROCKNIX and RASTERATOPS archive paths/hashes, original sentinel hashes, live PRE_RESTORE snapshots, protected history and final history. local-recovery.py:15-70 injects failure after real extraction; backuptool:1349-1380 excludes the active snapshot before date-name trimming; :1455 onward snapshots before extraction. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.

**Refutation attempted:** Inspected the wrapper to exclude a fake no-op extraction, and the 2030-dated mixed histories to test clock skew rather than only normal chronological retention.

**Notes:** Both suffixes retain three historical files plus the active recovery snapshot; normal backup subsequently retains the three histories. Actual target execution is retained; fresh host tests corroborate it.

### AC-I376-L25

> The final branded image's RC2 upgrade rehearsal preserves existing settings archives and restores them through the cloud and local recovery entry points; logs identify image hashes and the selected archives.

**Source:** #376, inputs/issues/376.md:25
**Checked:** 2026-10-06T15:20:17.437334+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/archive/assertions.json (14 assertions), writer-selection.json and provenance.json identify the inherited actual RC2 archive and production cloud/local restores. Raw logs010,011,016,017,022,023,026,027 retain selected archive, writer execution and restored sentinel SHA85704db48b3889a61f0cc9d70a0df1bea530c9e153f995f6cf68752bc7a343d3. Replacement14 qa18 upgrade rehearsal separately preserves actual RC2 state (26 assertions); evidence/candidate-product-continuity.json binds unchanged archive code09→14.

**Refutation attempted:** Checked actual inherited archive and sentinel bytes instead of inferring compatibility from the version label or a clean install.

**Notes:** Runtime archive selection was executed on the explicitly named replacement09 image, not newly on14; unchanged archive payload and14 upgrade evidence are distinguished.

### AC-I381-L24

> A candidate guest creates a settings archive through production cloud_backup, then opens RESTORE FROM CLOUD; the scan selects the actual archive and a640x480 frame shows SETTINGS enabled with the approved device/date text. Archive path, scan facts and frame are retained.

**Source:** #381, inputs/issues/381.md:24
**Checked:** 2026-10-06T15:20:17.437353+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-archives-runtime/extended/ui-writer-selection.json identifies actual production archive2026_10_03-182015-GENERIC-X64-ROCKNIX_SETTINGS.tar.gz, MINE/NEWEST equality and count1. Directly viewed extended/restore-page.png at640x480: SETTINGS enabled, GENERIC X64,10/03/2026. docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/archive/writer-selection.json independently identifies the later actual production writer archive2026_10_05-043142-GENERIC-X64-ROCKNIX_SETTINGS.tar.gz and SHA0b9f0b2e0259f2a5c06dbc0750f6b5d1ad0ad6c7c7d74b80277f16481f7cacc5.

**Refutation attempted:** Confirmed production-generated filenames and scan facts, not only synthetic flat fixtures or a reviewer caption. Existing later UI own-label/foreign controls remain separately recorded.

**Notes:** The directly reviewed writer UI frame belongs to the recorded October3 candidate; subsequent writer-shaped execution is separate evidence.

### AC-I381-L25

> Production restore consumes exactly the archive the scan selected; sentinel hash and journal verify it. Current device, legacy device name, healed previous IDs, foreign-only and flat-root fixtures preserve the documented selection behavior.

**Source:** #381, inputs/issues/381.md:25
**Checked:** 2026-10-06T15:20:17.437370+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-archives-runtime/extended/selection-matrix.json identifies archive/sentinel per current, legacy, healed-ID, flat and foreign-only fixture. docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/archive/assertions.json includes exact journal-selected archive and restored sentinel assertions; raw022/023/026/027 corroborate actual restore and bytes. Shared selector rasteratops-settings-archive:1-43 supplies both cloud_scan and cloud_restore. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.

**Refutation attempted:** Compared the exact selected name to the real restored content, checked foreign NEWEST can differ from own MINE, and preserved directory-priority semantics.

**Notes:** The foreign fallback is console-only intentional behavior; empty MINE disables the UI.

### AC-I381-L26

> The old scan fails a regression using writer-shaped per-device directories; the corrected scan passes. Existing flat-root cases remain compatibility controls, not the only fixtures.

**Source:** #381, inputs/issues/381.md:26
**Checked:** 2026-10-06T15:20:17.437388+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-02-cloud-remediation/baseline-results.json: writer-directory T24 controls fail on original code while the legacy flat-root control passes. focused-fixed-results.json and fresh evidence/host-checks-01/cloud-layout-results.json retain fixed current/legacy/healed/flat/foreign cases. Fresh evidence/host-checks-01: cloud-layout 316 PASS/0 FAIL, full suite 1719 PASS/0 FAIL, deliberately injected failure rc1.

**Refutation attempted:** Read both baseline and corrected primary results; an all-flat suite would not detect the defect.

**Notes:** Writer-shaped directories are first-class fixtures. Flat-root cases remain compatibility controls.

### AC-I381-L27

> The final RASTERATOPS image also discovers legacy ROCKNIX-suffixed archives under those folders (#376), and main WebDAV/S3 plus pair migration suites remain green.

**Source:** #381, inputs/issues/381.md:27
**Checked:** 2026-10-06T15:20:48.315336+00:00
**Verdict:** PASS ✓

**Evidence:** Replacement09 runtime12 archive assertions and selected production ROCKNIX-suffixed archive plus source continuity09→14. docs/qa-logs/2026-10-06-local-cloud/{webdav,sftp,s3}/report.md and completion.json bind actual image c7df6a6f428086f79a377ca1b049f20694f34a868987cf12c493c78eab7b2254 and three106PASS/0FAIL/0SKIP executions. Focused cloud-boundaries01 identities.json identifies two distinct VM boot/device IDs; pair-copy-Backups-{interrupted,final,follower}.json retains preserved hashes, new pointers and follower journal. results.json covers all nine fault/retry/follower cases.

**Refutation attempted:** Distinguished actual replacement14 local-protocol execution from unchanged replacement10 pair proof, and checked the follower is a different guest rather than the same VM with reset configuration. Read before/after cloud hashes, not only a suite summary.

**Notes:** Historical RASTERATOPS identity wording is superseded by lowercase pixelelated D-WORKFLOW-144. Authenticated Dropbox remains explicitly outside this local protocol baseline.

### AC-I356-L75

> `cloud_migrate_layout` runs numbered steps from the marker's version to the build's, each with the move dialog, each copy-verify-delete, each a journal line naming the step; a `tools/pixelelated-vm-cloud-boundaries` case (paired with the retained MOVE UI proof) seeds layout 1 and ends at layout 2 with the marker written and nothing lost (hash list before and after).

**Source:** #356, inputs/issues/356.md:75
**Checked:** 2026-10-06T15:21:59.977022+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_migrate_layout:1216-1525 dispatches step1 and records begin/backups/saves/discarded/content/complete. docs/qa-logs/2026-10-05-p3-reconciliation/cloud-boundaries-01/proof.py:150-184 seeds literal layout=1, verifies all four tiers, layout=2 bytes, old-file absence and six journal stages; artifacts/results.json records PASS. Existing guest09 MOVE frame sequence is retained under guest-11 A. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.

**Refutation attempted:** Confirmed the layout1 fixture is actually seeded and the result compares exact bytes; this is not a marker-free transition relabeled as version-aware.

**Notes:** Only the implemented predecessor→2 transition is claimed, not arbitrary future version support.

### AC-I356-L77

> Fault injection after each completed tier and at marker publication followed by retry preserves both sides, completes without duplicate/lost state, and lets a second guest follow; logs identify the numbered step and hashes.

**Source:** #356, inputs/issues/356.md:77
**Checked:** 2026-10-06T15:21:59.977101+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-p3-reconciliation/cloud-boundaries-01/proof.py:150-184 and artifacts/results.json cover four copy, four deletion and one marker fault followed by recovery/repeat. identities.json and all nine follower.json files identify guest b; inspected copy-Backups intermediate/final/follower hashes and journal. cloud_migrate_layout:970-1215 binds retry record to paths/config and :1428-1518 records each tier. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.

**Refutation attempted:** Operation-specific fired sentinel, nonzero result and absent success marker are required; second guest must have no mover record and must preserve cloud hashes.

**Notes:** This satisfies named operation-boundary faults. It does not prove SIGKILL during a copy or arbitrary power loss; #353 is graded separately.

### AC-I356-L78

> The step for `/GAMES` and `/ROCKNIX` is step 1 and is the one #353 ships; the design note lives in `docs/rasteratops/cloud-layout.md`.

**Source:** #356, inputs/issues/356.md:78
**Checked:** 2026-10-06T15:21:59.977130+00:00
**Verdict:** PASS ✓

**Evidence:** docs/rasteratops/cloud-layout.md:1-115 specifies strict markers, numbered step1, JSON recovery record, copy/verify/delete and actual predecessor boundary. cloud_migrate_layout migration_step_1 is the only registered transition; fresh host and retained VM evidence cover GAMES and ROCKNIX.

**Refutation attempted:** Checked documentation admits RC2 lacks the future protocol and that the marker is not a distributed lock.

**Notes:** Current canonical destination is pixelelated; historical Rasteratops paths occur only in old evidence.

### AC-I380-L22

> Regression fixtures distinguish missing CONTENT_REMOTE, explicit empty cloud root, a derived old Content folder and a named custom folder for join, follow, settle and apply; log records before/after values.

**Source:** #380, inputs/issues/380.md:22
**Checked:** 2026-10-06T15:21:59.977150+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_migrate_layout:100-150 distinguishes key presence; :657-795 and :1450-1510 preserve explicit root/custom choices. docs/qa-logs/2026-10-05-p3-reconciliation/cloud-boundaries-01/proof.py:200-214 and artifacts/results.json exercise all16 join/follow/settle/apply × omitted/root/derived/custom cases with before/after pointers and bytes. October2 baseline-results.json fails the four root-overwrite cases; focused-fixed-results.json passes. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.

**Refutation attempted:** An empty value is not treated as a missing key. The missing-key fixture explicitly removes the assignment; named custom and derived paths are separate inputs.

**Notes:** All16 matrix cases were executed on replacement10; source continuity to14 is retained.

### AC-I380-L23

> On GENERIC_X64, an explicit root holding ROMs/BIOS remains the selected location after a layout transition and the scan lists/restores the original sentinel; missing-key fixtures get the documented default.

**Source:** #380, inputs/issues/380.md:23
**Checked:** 2026-10-06T15:21:59.977167+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-cloud-root-replacement02/attempt-02/artifacts/{transitions,assertions}.json retain actual pointer changes, root ROM/BIOS scan output and two restored sentinel checks per mode. docs/qa-logs/2026-10-05-p3-reconciliation/cloud-boundaries-01/T21 current-name matrix independently preserves root bytes and assigns defaults only to missing keys. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.

**Refutation attempted:** Read transition output to exclude previous no-op follow/settle fixtures: old/new SAVES_REMOTE differ while CONTENT_REMOTE remains exactly empty.

**Notes:** Older actual root restore execution is distinguished from current-name16-case transition coverage and source continuity.

### AC-I380-L24

> The contradictory seeding/migration fixtures and state table agree on one representation without silently replacing a player-selected folder; existing content-root tests remain green.

**Source:** #380, inputs/issues/380.md:24
**Checked:** 2026-10-06T15:21:59.977185+00:00
**Verdict:** PASS ✓

**Evidence:** docs/rasteratops/cloud-folder-state-table.md:173-289 maps each actor and specifies missing/root/custom distinctions; executable T21 matrix and older contradictory fixture now omit the key where unset was intended. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.

**Refutation attempted:** Read the historical section as historical; it explicitly retains the original root-overwrite finding, while the remediation and executable map document the fixed representation.

**Notes:** No player-selected cloud root is silently replaced by a migration-derived Content path.

### AC-I391-L22

> Historical RC2/run101 controls reproduce all four failures before the fix, then recover every owned payload and complete marker publication; retained logs identify predecessor script hashes and before/after pointers/hashes.

**Source:** #391, inputs/issues/391.md:22
**Checked:** 2026-10-06T15:21:59.977202+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-m7-coverage/predecessor-before.log:6PASS/4FAIL includes RC2-content, run101-discarded/content/marker failures; predecessor-after.log:15PASS/0FAIL, plus fresh316 suite. docs/qa-logs/2026-10-05-pixelelated-replacement-09/predecessor-09/artifacts/predecessor/RC2-content-inherited.json retains exact predecessor SHA76f003f52d98056bda9685d44cb224d4c4034089e6ce70509ffaa294da275f27 and installed SHAfe184dc2a20f991d35402065c36373f915aa821c96f15b8dbfdd09ba8e533555, split pointers and payload hashes.

**Refutation attempted:** Read the failed baseline entries and actual inherited state; the fixture executes historical scripts rather than inventing only candidate-shaped recovery records.

**Notes:** run101 is historical host compatibility coverage; real candidate VM execution uses actual RC2-created states.

### AC-I391-L23

> Recovery remains interruptible and repeatable; controls retain custom content/root choices, refuse unmarked foreign destination conflicts, and preserve both versions when an allowed merge is required.

**Source:** #391, inputs/issues/391.md:23
**Checked:** 2026-10-06T15:21:59.977218+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_migrate_layout:693-795 and recovery/relocate sections only recover known old tiers, bind the record and refuse foreign collisions. predecessor-after.log includes reinterrupted, boundary-root/custom/foreign/fleet PASS; legacy-record-after.log covers old schema1 compatibility; docs/qa-logs/2026-10-05-pixelelated-replacement-09/predecessor-09/RC2-content-reinterrupted-{new-fault,recovered}.json preserve identical payload hashes across failed marker and successful retry. Fresh host-checks01:316 layout assertions PASS, deliberate failure rc1; full1719 suite PASS.

**Refutation attempted:** Read exact hash sets before and after repeated failure; foreign content is separately refused in focused boundaries proof.py:225-235, leaving old and destination bytes distinct.

**Notes:** This is controlled operation interruption, not an arbitrary process/power-cut guarantee.

### AC-I391-L24

> Candidate VM/upgrade proof verifies the inherited partial state and its recovery, naming the image and showing payload hashes and the supported retry/move path.

**Source:** #391, inputs/issues/391.md:24
**Checked:** 2026-10-06T15:21:59.977233+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/predecessor-09/predecessor-proof.py:1-108 checks exact upgraded buildcf511ce79b83cba7fea8b14cfa3d04fb13e4b4fb and unmodified installed script, executes transferred RC2 script, retains five inherited states, then installed recovery. artifacts/predecessor/assertions.json has65 passing assertions; reinterrupted scan reports migration-pending, needs-step returns0, retry publishes exact layout2.

**Refutation attempted:** Verified SHA of the historical script and installed source, actual partial pointers/content hashes, repeat stability and final installed-byte invariance. The script is run on an actual-upgrade candidate, not merely host Bash.

**Notes:** Replacement09 runtime evidence remains valid for unchanged migration bytes through14; current14 actual RC2 upgrade is a separate26-assertion qualification.

### AC-I407-L18

> A focused old-code control observes the empty destination; corrected output clearly names the cloud root while retaining named-folder output.

**Source:** #407, inputs/issues/407.md:18
**Checked:** 2026-10-06T15:21:59.977250+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-cloud-root-label/check.py and check.log directly execute production set_pointer. Old empty-root output has a blank destination; corrected output says the root of your cloud. Named /Mine/ROMs output and exact stored values are controls. Fresh host suite includes cloud migration regressions.

**Refutation attempted:** The label check verifies the saved empty value stays empty, avoiding a cosmetic fix that changes the selected location.

**Notes:** The historical control extracts only the actual pointer writer; actual installed label proof is separately retained in replacement02 transitions.

### AC-I407-L19

> Explicit CONTENT_REMOTE remains empty after the actual transition and root ROM/BIOS restores remain byte-identical on the resulting image.

**Source:** #407, inputs/issues/407.md:19
**Checked:** 2026-10-06T15:21:59.977266+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-cloud-root-replacement02/attempt-02/artifacts/transitions.json and assertions.json:22 actual guest assertions, four real pointer transitions, root preserved, root ROMs/BIOS scanned and both sentinels restored each time. cloud_migrate_layout set_pointer uses a display-only phrase for empty content while persisting the original value.

**Refutation attempted:** Checked that join really changes the saves pointer and displays the phrase, rather than passing on no-op output.

**Notes:** Follow/settle/apply are tested for value preservation even when they emit no content-pointer sentence.

### AC-I350-L24

> Opening BACK UP TO THE CLOUD or RESTORE FROM THE CLOUD opens CHECKING YOUR CLOUD before any options (D-CLOUD-167), with the live line and CANCEL as the one way out while it runs (D-UI-078); the options page follows when the listing is in. A `tools/vm-walks` frame sequence shows menu, scan page, options, and no frame with a card drawn over a dialog.

**Source:** #350, inputs/issues/350.md:24
**Checked:** 2026-10-06T15:26:34.379313+00:00
**Verdict:** PASS ✓

**Evidence:** GuiMenu.cpp:5440-5475 opens cloud_scan in GuiCloudTransfer before creating options; cloud_scan:153-255 persists facts then done. Directly viewed original guest11 H scan0/1 and A options, plus G scan0 and backup options; CANCEL is the running control, no options dialog under either scan. guest11/{H,A,G}/logs/run.log retains walk order.

**Refutation attempted:** Compared actual running frames to post-scan options in both directions, not just the final screenshot.

**Notes:** This is retained installed unchanged-ES evidence, with source continuity to14.

### AC-I350-L25

> When the comparison fails (the cloud unreachable: the dead port of `tools/cloud-test-backend`), the page says why in the outcome vocabulary (`COULDN'T FINISH - …`, `es-player-text.md`) and offers TRY AGAIN beside CLOSE; a frame shows it.

**Source:** #350, inputs/issues/350.md:25
**Checked:** 2026-10-06T15:26:34.379384+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest-11/artifacts/cloud-epic/F/logs/run.log: dead port produces no success stamp,3PASS/0FAIL. Directly viewed01-F-outcome.png: CHECKING YOUR CLOUD, COULDN’T FINISH, CLOUD FOLDER — YOUR CLOUD STOPPED ANSWERING, CLOSE and TRY AGAIN.

**Refutation attempted:** Checked that failure cannot advance through a stale done stamp; runner removes prior scan artifacts before retry.

**Notes:** Current wording includes the concrete reason and safe unchanged-state sentence.

### AC-I350-L26

> `docs/es-menu-map.md` carries the page (D-UI-039); `tools/es-menu-map-check` passes.

**Source:** #350, inputs/issues/350.md:26
**Checked:** 2026-10-06T15:26:34.379420+00:00
**Verdict:** PASS ✓

**Evidence:** docs/es-menu-map.md:130-147 includes opening scan, failed outcome, folder dialogs and content scan. Fresh evidence/host-checks-01/results.json records es-menu-map check rc0 against exact ES checkout.

**Refutation attempted:** Read the flow map, then executed the checker rather than assuming the diagram matches source.

**Notes:** No menu row changed during this audit.

### AC-I350-L27

> The interface edit passes `tools/es-syntax-check` before the pin moves, and `docs/cloud-sync-changelog.md` carries the change the day it lands.

**Source:** #350, inputs/issues/350.md:27
**Checked:** 2026-10-06T15:26:34.379442+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-m7-p1/es-syntax.log records GuiMenu.cpp OK/PASS for the remediation before candidate package qualification. docs/cloud-sync-changelog.md:2933-2990 records the October1 scan-first behavior and unchanged semantics; exact ESf6f0 source is compiled into current14 image.

**Refutation attempted:** Distinguished the original dated changelog from later requalification and verified the compilation artifact instead of treating a pinned hash as compilation evidence.

**Notes:** The documented old brand name is historical; current rename is covered separately.

### AC-I350-L35

> The opening scan checks folder state, settings archives by label and content location before options; CONTINUE with content selected runs the second content scan in the selected classes (D-CLOUD-167); the options page on guest d lists only rows the scan found (a frame per seeded case: settings for this label, settings for a foreign label only, content under `/ROCKNIX/Content`, content nowhere).

**Source:** #350, inputs/issues/350.md:35
**Checked:** 2026-10-06T15:26:34.379459+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_scan:153-255 reads folder→archives→content-location before done; --content executes only selected classes. GuiMenu.cpp:5294-5314 schedules the second scan; guest11 H/A/C/D logs and original frames cover own-label enabled, foreign-only disabled, content found and absent; D progresses through second scan to NES-only picker.

**Refutation attempted:** Read actual first/second scan entrypoints to distinguish discovery from class-specific comparisons. New unrelated-directory classifier lead affects #352 and is separately probed, not hidden by these fixture passes.

**Notes:** Acceptance is established for the named seeded cases, not all possible cloud folder contents.

### AC-I350-L36

> Its live line says what it is checking in the words approved for it (D-CLOUD-164: `CHECKING WHAT SETTINGS AND CONTENT YOUR CLOUD HAS FOR THIS DEVICE...`); the string and its French land in the same commit (D-UI-051).

**Source:** #350, inputs/issues/350.md:36
**Checked:** 2026-10-06T15:26:34.379476+00:00
**Verdict:** PASS ✓

**Evidence:** GuiCloudTransfer.cpp:1008-1010 uses the approved full sentence plus whole-clause640px fallback; exact French strings in locale/lang/fr/LC_MESSAGES/emulationstation2.po:6515+. git log -S identifies both source and French introduction in dc819f432483acad722a14234d7bbe6b999a705c at2026-10-01 14:38:17UTC. Actual H/G frames show the complete shorter line at640px.

**Refutation attempted:** Verified both commits are identical, rather than only checking translations exist now; fallback selects an approved complete clause rather than chopping letters.

**Notes:** Clarity and fitting behavior follow the existing player-text policy.

### AC-I352-L34

> A CHOOSE CLOUD FOLDER page (the `GuiFileBrowser` pattern fed by `rclone lsf`, `es-native-ui.md` § Reusable precedents) sets `CONTENT_REMOTE` through `cloud_setup`, and the transfer page re-reads it; the walk's frames show the chosen folder and the journal shows the `Content path` line.

**Source:** #352, inputs/issues/352.md:34
**Checked:** 2026-10-06T15:26:34.379494+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** GuiMenu.cpp:5210-5314 routes a selected folder through cloud_setup --set-content-remote, checks status, then rereads for the scan. cloud_setup:569-605 validates/persists the pointer and logs Content path. Guest11 D frame shows the chooser and later automatic fallback is proven.

**Refutation attempted:** Read the actual walk: D2 cancels the chooser with key z; D4 uses automatic fallback. Those do not establish a successful manual folder selection.

**Notes:** Source supports the desired path but the cited current walk is narrower than the checkbox.

**Gaps:** Locate another executed manual chooser selection with selected-folder frame/journal, or add a focused installed UI assertion before closing this criterion.

### AC-I352-L35

> With `CONTENT_REMOTE` back at `/ROCKNIX/Content` and the QA cloud seeded with `Photos/` and `Documents/` at its root, CONTENT TO RESTORE on guest d lists only ROM systems and BIOS: the walk's 640x480 frame and the scan's output lines. (The Nova's own listing is re-read on its next staging, as a read, and noted here in a comment.)

**Source:** #352, inputs/issues/352.md:35
**Checked:** 2026-10-06T15:26:34.379513+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_content_restore:1308-1323 filters pre-tier root rows by local or supported systems. Directly viewed guest11 D/03-D-systems.png: NES is shown; Photos/Documents appear only in04-D-chooser.png as cloud folders, not systems. Host scripts fresh1719 suite includes A0 Photos/Documents negative controls and genuine gb positive control.

**Refutation attempted:** An empty list could trivially hide private folders; the actual NES row and gb host positive fixture ensure content remains discoverable.

**Notes:** Historical /ROCKNIX content fixture now uses canonical /pixelelated after migration. Physical Nova readback remains staging context, not a prerequisite for this VM-verifiable behavior.

### AC-I352-L36

> `docs/es-menu-map.md` carries the chooser (D-UI-039); `tools/es-menu-map-check` and `tools/vocabulary-check` pass; the cloud-sync page on the site says where the content folder is chosen (`documentation-accuracy.md`).

**Source:** #352, inputs/issues/352.md:36
**Checked:** 2026-10-06T15:26:34.379530+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** docs/es-menu-map.md:140-146 includes chooser; fresh host es-menu-map check rc0 and ES-checks02 vocabulary164strings/0wrong. The public cloud-sync site delivery remains the separate P5 docs gate.

**Refutation attempted:** Passing local instruction/map checks cannot establish the separately hosted documentation page.

**Notes:** Same public-site gate as I349-L34, but this combined criterion includes both passed local work and outstanding publication.

**Gaps:** Public cloud-sync page must describe folder selection before P5 publication (#42); do not claim it published from local map evidence.

### AC-I352-L45

> Only then, with nothing found under either, the chooser opens; a frame shows it with the QA cloud's root folders listed as folders to pick from, never as systems.

**Source:** #352, inputs/issues/352.md:45
**Checked:** 2026-10-06T15:26:34.379546+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 D log and directly reviewed03-D-question.png/04-D-chooser.png show absent configured/fallback content leads to the chooser; Documents/Photos are presented as folder paths. GuiMenu.cpp:5228-5282 makes that route explicit.

**Refutation attempted:** The screenshot was checked as actual640x480 pixels, including full text and separate folder paths, rather than a manifest caption.

**Notes:** This covers the empty configured folder fixture. The unrelated-subdirectory case is a separate in-flight executable check.

### AC-I352-L32

> `cloud_content_restore --scan` lists a pre-tier folder only when this device has a folder of that name under `/storage/roms` or the name is a supported system (`legacy_dirs` / `supported_systems`), the same rule `resolve_src` applies; a `tools/cloud-round-trip` case seeds `Photos/` and `Documents/` at the root and the scan's output carries neither line.

**Source:** #352, inputs/issues/352.md:32
**Checked:** 2026-10-06T15:27:44.992645+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_content_restore:1308-1323 filters pre-tier rows by local directory or supported system. Fresh host1719-suite A0 case includes real gb and unrelated Photos/Documents; guest11 D seeded both unrelated folders and retained a NES-only picker.

**Refutation attempted:** Verified a genuine supported content row remains visible while unrelated folders remain selectable only in the cloud-folder chooser.

**Notes:** Content listing filtering itself is distinct from the broken location classification recorded at I352-L33/L44.

### AC-I352-L33

> When the content root holds no `ROMs/` and no known system folder, the page says so instead of listing: `YOUR CLOUD HAS NO ROMS OR BIOS AT <folder>.` / `CHOOSE THE FOLDER WHERE YOUR GAMES ARE?` (approved D-CLOUD-164), with a row that opens the folder chooser; a 640x480 frame shows it.

**Source:** #352, inputs/issues/352.md:33
**Checked:** 2026-10-06T15:27:44.992707+00:00
**Verdict:** FAIL ✗

**Evidence:** Fresh evidence/content-probe-01/artifacts/results.json on exact installed7afa9efcfc: unrelated-configured seeds /Mine/Photos/x.jpg, CONTENT_REMOTE=/Mine, no ROMs/BIOS/known systems; STATE=ok, AT_PATH=1, expected empty. Empty-folder control returns empty and real-tiered configured control returns ok. GuiMenu.cpp:5237 skips chooser whenever state != empty.

**Refutation attempted:** Executed the criterion’s omitted boundary using the unchanged binary and real local WebDAV. All cloud bytes and pointers stayed identical; all four result channels rc1 and cleanup independently verified.

**Notes:** Existing D empty-folder frame is valid but insufficient for the broader no-known-content clause. Probe also exposes explicit-root recognition asymmetry.

**Gaps:** Fix content-location classification to recognize actual supported content rather than any directory, then requalify the question/chooser and genuine-content controls on a rebuilt image.

### AC-I352-L44

> When the configured content root holds no `ROMs/` and no known system folder, the scan looks under the cloud root's `/ROCKNIX/Content` (the saves root's parent, `cloud_setup:629-631`) and, finding `ROMs/` or `BIOS/` there, uses that folder automatically and writes `CONTENT_REMOTE` (D-CLOUD-167, no USE IT confirmation); on guest d with `CONTENT_REMOTE=""` and content seeded under `/ROCKNIX/Content`, the frame sequence advances to the options and the journal shows the `Content path` line.

**Source:** #352, inputs/issues/352.md:44
**Checked:** 2026-10-06T15:27:44.992736+00:00
**Verdict:** FAIL ✗

**Evidence:** Fresh content-probe01 unrelated-configured-fallback case seeds unrelated /Mine/Photos plus real /pixelelated/Content/ROMs/gb/A.gb. cloud_setup reports STATE=ok, FOUND empty rather than found-elsewhere; AT_PATH=1 prevents fallback. GuiMenu.cpp:5228 only auto-selects when found-elsewhere.

**Refutation attempted:** Real installed classifier and backend reproduce the suppression; normal configured game folder remains the positive control.

**Notes:** The original legacy /ROCKNIX destination is superseded by pixelelated. The defect concerns the same discovery rule, not naming.

**Gaps:** Use a consistent game-content predicate for configured path, explicit root and fallback; retain unrelated-folder and valid-content controls. Recheck automatic choice with actual VM UI after the fix.

### AC-I356-L76

> A second guest on the same cloud takes the new marker at its next check with no dialog (its journal line), and the version-aware candidate offered a newer or malformed marker refuses unsupported writes/marker overwrite, showing a supported outcome (frame plus byte/pointer assertions). The separate RC2→candidate and mixed-installation receipts name the actual old binary and prove preservation; they do not claim RC2 implements this future protocol.

**Source:** #356, inputs/issues/356.md:76
**Checked:** 2026-10-06T15:30:21.103072+00:00
**Verdict:** PASS ✓

**Evidence:** Focused cloud-boundaries01 identities and nine follower.json files: distinct guest b has no mover record, follows via folder scan and records journal while cloud hashes remain identical. Replacement09 guest11 T26 logs30 actual installed refusal/preservation assertions; cloud-ui08 UI26 logs13 checks and directly reviewed future-refusal640px frame saying COULDN’T FIND YOUR CLOUD FOLDER with CLOSE/TRY AGAIN. Actual RC2 upgrade and predecessor09 preserve prior data. Fresh316 host checks corroborate strict markers.

**Refutation attempted:** Separated candidate marker-awareness from actual historical RC2 binary behavior; a renamed fixture or a reset same-guest configuration does not satisfy the pair proof.

**Notes:** Future/malformed refusal preserves marker, pointers and cloud payloads; no distributed-lock guarantee is inferred.


#### Amendment to AC-I356-L76 — PARTIAL

The primary pixel read shows COULDN’T FIND YOUR CLOUD FOLDER for a present but future marker. `cloud_migrate_layout:995` returns4 after the accurate unsupported-version explanation. `cloud_scan:160–173` discards that output and `why_for_rc:97–104` interprets4 as rclone directory absence. `UI26-future-script.log` and the original frame agree. Safety/refusal and second-guest following remain proven; the outcome reason is not truthful. The earlier PASS is superseded by PARTIAL, with a reason-propagation repair/qualification gap. No additional invocation is needed to establish this retained installed behavior on unchanged scripts.
