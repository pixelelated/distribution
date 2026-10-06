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
### AC-I363-L73

> No sync runs networked layout join/state/follow/migration preparation before transfer. The local `cloud_migrate_layout --superseded` string-list call and per-run legacy saves-folder existence probe required by D-CLOUD-172 remain permitted. `tools/last-good-scripts-test` reports both no-folder-check PASS lines; missing/unknown-root controls preserve D-CLOUD-172. This corrects the obsolete literal no-call wording against D-CLOUD-170/172/173, rather than removing the required absent-folder guard.

**Source:** #363, inputs/issues/363.md:73
**Checked:** 2026-10-06T15:37:16.047296+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_backup:826-840 performs only local --superseded lookup; :1670-1698 retains the one legacy-parent existence probe and unknown fallback. cloud_restore has no networked migration preparation. Fresh scripts.log:1461-1462 records both no-folder-check PASS lines; T18 missing/unknown controls pass.

**Refutation attempted:** Inspected main.cpp:683 separately: startup orchestration deliberately prepares the folder before transfer under D-CLOUD-173. The no-per-sync preparation rule applies to transfer scripts, not removal of this approved boot-only ordering.

**Notes:** No extra recurring join/state/follow/move has been added; the absent-folder guard is not waived.

### AC-I363-L74

> An exit sync on an existing earlier `/ROCKNIX` folder and the current folder meets the unchanged five-alternating-sample median difference limit of30ms. Current candidate runtime07:272/244ms medians,28ms difference, real transferred bytes and zero migration preparation. #429 preserves the original36ms failed attempt and justifies the new fixture-bound qualification.

**Source:** #363, inputs/issues/363.md:74
**Checked:** 2026-10-06T15:37:16.047370+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/timing/installed-samples.json contains two separate warmups and10 alternating measured transfers, all rc0 with local/remote hashes equal; comparison.json reports269/245ms medians,24ms absolute difference,30ms limit and0migration journal delta. timing-proof.py measures exact installed cloud_backup SHA12a231698b70a8b83eb9d1fd1bc593f4507313030635a6750392f5fd19130a03.

**Refutation attempted:** Read every sample and the predeclared ordering, not only the aggregate; waiting for valid upload timestamps occurs outside measurement. Source continuity09→14 preserves this script.

**Notes:** Earlier runtime07 result28ms and the original36ms failure are distinct retained attempts; this is runtime12 evidence, not a new14 performance execution.

### AC-I363-L75

> `cloud_migrate_layout --needs-step` answers with no network: 0 for an earlier default, not kept, with a remote set up; 1 for the current folder, a folder of the player's own, a kept one, or no remote; 2 for a conf it cannot read; rclone never starts (`tools/last-good-scripts-test` section aa, its `--needs-step` lines).

**Source:** #363, inputs/issues/363.md:75
**Checked:** 2026-10-06T15:37:16.047408+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_migrate_layout:1520-1560 implements --needs-step before network/locking. Fresh scripts.log:1453-1460 checks earlier defaults0, current/custom/kept/no-remote1, unreadable2, exact case matching and no rclone execution. Fresh evidence/host-checks-01/activity/scripts.log and cloud-layout-results.json:1719/316 PASS, expected injected rc1.

**Refutation attempted:** Confirmed pending-record exception intentionally returns0; local eligibility cannot silently claim a remote marker check.

**Notes:** The predicate is exercised through host exact-source controls and whole-guest boot cases, not inferred solely from a comment.

### AC-I363-L76

> `cloud_scan --folder` is the folder item alone -- the join, the state, the quiet follow -- with no archive or root listing, the opening scan's files left as they were, and a refused join ending with its why and no state (section ab, its `--folder` lines).

**Source:** #363, inputs/issues/363.md:76
**Checked:** 2026-10-06T15:37:16.047433+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** cloud_scan:read_folder and --folder branch remove only state, preserve opening scan files and omit archive/root listing. Fresh scripts.log:1479 verifies this; refused join stops without state. Actual UI26 proves refusal but reason is mislabeled for an unsupported layout.

**Refutation attempted:** Cross-layer rc4 means unsupported layout to migration and missing folder to the rclone-only mapper; suppression of stdout loses the truthful reason.

**Notes:** Folder-only scope passes; truthful refused-join explanation is affected by #468.

**Gaps:** Resolve #468 reason propagation and requalify join/state/follow failure outcomes without changing folder-only listing scope.

### AC-I363-L77

> The transfer pages' scan still checks on every open (`tools/last-good-scripts-test` section ab).

**Source:** #363, inputs/issues/363.md:77
**Checked:** 2026-10-06T15:37:16.047454+00:00
**Verdict:** PASS ✓

**Evidence:** GuiMenu.cpp:5440-5475 constructs a fresh scan on every cloud transfer open. cloud_scan removes prior done/state/facts and reruns prepare/folder/archives/content before publishing done. Fresh host sectionab passes; guest11 A/H/G/F/C demonstrate repeated independent opens including failed/no-stamp path.

**Refutation attempted:** Checked that cached facts do not bypass the next scan, and the filesystem exists check for rclone.conf explicitly bypasses cached misses.

**Notes:** No restored old done stamp is accepted as the next opening scan.

### AC-I379-L22

> A synthetic cloud with no save files and one same-device settings archive in each old layout keeps that archive discoverable after follow, settle, setup and transfer-page scan; VM log records pointer values, selected filename and restored sentinel hash.

**Source:** #379, inputs/issues/379.md:22
**Checked:** 2026-10-06T15:37:16.047471+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Actual archives-runtime/archive-proof.py:82-95 independently resets ROCKNIX/GAMES settings-only clouds, runs follow/settle, calls full scan and restores the writer sentinel; assertions.json records those four cycles. Focused boundary36 adds current-name follow/settle/custom payload preservation. Fresh T20 actor wizard/transfer/boot rows pass.

**Refutation attempted:** The retained archive VM cycles directly prove follow/settle/full scan/restore. They do not execute cloud_setup completion for that same settings-only fixture; host wizard coverage is not a substitute for the explicitly required VM path.

**Notes:** No observed archive loss; this is an incomplete setup-route receipt.

**Gaps:** Locate a settings-only installed setup→scan→restore receipt or add it to the next bounded VM qualification, retaining old/new pointer and selected archive/sentinel evidence.

### AC-I379-L23

> Controls with save files, no archives, a kept layout and an explicit custom Backups folder preserve the documented behavior; each case has a reset and negative control on the old commit.

**Source:** #379, inputs/issues/379.md:23
**Checked:** 2026-10-06T15:37:16.047491+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_migrate_layout:118 backup_pointer_for keeps custom/populated tiers; independently reset T20 actor and follow/settle/default/custom/apply-other-source cases all pass in fresh316results. Baseline October2 T20 failures and fixed results retain before/after negative controls; focused boundaries six settings-only controls run on a genuine installed guest.

**Refutation attempted:** Checked custom tier and empty old saves are independent; a populated save root is not needed to keep old backup content.

**Notes:** Existing no-archive/kept/classification controls preserve intentional policy; no OS-name assumption substitutes for archive discovery.

### AC-I379-L24

> The state/actor table includes saves-empty / Backups-nonempty independently of OS-name compatibility #376; main and pair migration suites remain green.

**Source:** #379, inputs/issues/379.md:24
**Checked:** 2026-10-06T15:37:16.047507+00:00
**Verdict:** PASS ✓

**Evidence:** docs/rasteratops/cloud-folder-state-table.md T20 and executable actor map explicitly separate settings presence from saves and suffix compatibility. Main replacement14 three local backends each106PASS; focused36-case paired migration has distinct devices and per-case byte/pointer assertions. Fresh evidence/host-checks-01/activity/scripts.log and cloud-layout-results.json:1719/316 PASS, expected injected rc1.

**Refutation attempted:** Read the current remediation/coverage section as distinct from preserved historical baseline defects.

**Notes:** Protocol matrix and specific settings-only fixtures are both retained; current14 local runs do not relabel older pair execution.

### AC-I430-L28

> A fresh fixture waits outside measurement until the actual guest clock exceeds this layout's previous remote upload timestamp plus the comparison window; it asserts and retains the actual newly written mtime and preceding remote mtime before measuring the unchanged production command.

**Source:** #430, inputs/issues/430.md:28
**Checked:** 2026-10-06T15:37:16.047522+00:00
**Verdict:** PASS ✓

**Evidence:** runtime12/timing-proof.py:25-55 waits on actual guest time until previous remote mtime+2s, writes real fresh bytes, retains actual mtime, and requires >previous+1s before measured command. docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/timing/installed-samples.json records every boundary.

**Refutation attempted:** The wait uses monotonic only for its30s timeout; neither guest clock nor file mtime is forced forward. Measurement starts after the wait/fixture write.

**Notes:** Remote upload mtime, not an assumed host/guest clock relation, determines readiness.

### AC-I430-L29

> Every sample retains timing, return code, local/remote hashes and timestamp facts before a possible assertion; failed output is captured privately/sanitized before teardown.

**Source:** #430, inputs/issues/430.md:29
**Checked:** 2026-10-06T15:37:16.047538+00:00
**Verdict:** PASS ✓

**Evidence:** timing-proof.py appends before-command row before timing, after-command row containing rc/hash/mtime before transfer assertions, and sanitized failed output before throwing. All10 measured rows plus warmups retained in installed-samples.json.

**Refutation attempted:** Read order of writes relative to asserts to check that a failing byte predicate cannot erase the measured failed sample.

**Notes:** Raw synthetic fixture evidence is retained; credentials are not logged.

### AC-I430-L30

> A deliberately invalid timestamp boundary is rejected by the fixture predicate; fixed predeclared diagnostic batches transfer every changed save without forcing future mtimes, changing clocks or bypassing production comparison.

**Source:** #430, inputs/issues/430.md:30
**Checked:** 2026-10-06T15:37:16.047555+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/runtime-12/artifacts/timing/timestamp-controls.json records same-time/within-window/exact-boundary refusals and later acceptance. Read timestamp_valid and asserts; all10 installed measured transfers have real matching bytes with no utime/clock modification.

**Refutation attempted:** A no-op transfer cannot count: each sample writes random2000-byte save content and compares local/remote SHA before accepting timing.

**Notes:** The threshold is unchanged; success is not achieved by future-dating the file.

### AC-I363-L78

> At the end of cloud setup, for a fresh install whose cloud holds its saves under an earlier folder, the step reads the move before the seeding (`tools/cloud-pair-migration` step 2's lines), and the frames show CHECKING YOUR CLOUD, the MOVE question, then CLOUD SETUP COMPLETE after the answer (`tools/vm-visual-qa` frames at 640x480).

**Source:** #363, inputs/issues/363.md:78
**Checked:** 2026-10-06T15:38:46.236869+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/optins-11/artifacts/pair-console.log step2 on actual RC269e6039f8f/newcf511ce79b shows folder scan superseded/move, NOT NOW then seeding at the joined ROCKNIX tier, no pixelelated duplicate and byte-identical restore. guest11 L7checks retain setup ordering; directly viewed L setup-complete640px frame preserves ROCKNIX paths. GuiMenu.cpp:5495-5525 sets setup rescan/abandon to finish before seeding.

**Refutation attempted:** A mixed-image pair is named by both builds; the setup route is not inferred from a same-image clean install.

**Notes:** Automatic default migration is not confused with copying game files during pointer preparation.

### AC-I363-L79

> At boot, for a guest whose conf names an earlier folder it has not kept, with a remote set up, the step comes up after the startup sync's card: CHECKING YOUR CLOUD, then the question; NOT NOW brings it back at the next boot; after MOVE the next boot raises nothing and the journal reads `nothing to settle` (frames at 640x480 and the journal, guest d).

**Source:** #363, inputs/issues/363.md:79
**Checked:** 2026-10-06T15:38:46.236946+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 I/logs/run.log verifies first boot offer, NOT NOW keeps pointer, second boot repeats, MOVE transfers and repoints, third boot --needs-step1. E frame shows startup card alone then creation dialog without card. GuiMenu.cpp:5585-5609 waits for hasAsyncNotifications as well as worker and GUI/game state.

**Refutation attempted:** Checked actual notification lifetime gate; worker termination alone would allow the previously observed overlap.

**Notes:** Continuous captures and prior primary visual manifest remain retained; fresh review sampled original E frames and read all I assertions.

### AC-I363-L80

> Offline at boot (the guest's link cut on the QEMU monitor), the step asks `FINISH CLOUD SETUP` / `YOU'RE NOT ONLINE. CONNECT TO FINISH SETTING UP YOUR CLOUD FOLDER.` with CONNECT TO WI-FI and NOT NOW (a frame at 640x480).

**Source:** #363, inputs/issues/363.md:80
**Checked:** 2026-10-06T15:38:46.236978+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 J/logs/run.log4checks and directly reviewed01-J-offline.png at640x480 show FINISH CLOUD SETUP, exact offline explanation, CONNECT TO WI-FI/NOT NOW. GuiMenu.cpp:5550-5568 uses default-route test and offers Wi-Fi callback.

**Refutation attempted:** The fixture cuts the guest link, not a refused application endpoint; NOT NOW is separately asserted.

**Notes:** No physical radio claim is made by a VM network-link proof.

### AC-I363-L81

> With a settings restore's marker and an earlier folder both set at boot (written on guest d, a named stand-in for a restore followed by an update), FINISH RESTORE PROCESS comes first with nothing over it; its FINISH brings the step once the screen is free; its LATER brings neither until the next boot (frames at 640x480).

**Source:** #363, inputs/issues/363.md:81
**Checked:** 2026-10-06T15:38:46.237010+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 K7checks retain restore marker, LATER suppresses cloud step, FINISH consumes marker and brings it. Directly reviewed01-K-restore-page.png and03-K-after-finish.png show restore first and move later, with no overlay.

**Refutation attempted:** The marker is explicitly injected as a named stand-in; this does not pretend the walk independently performed a real cloud settings restore.

**Notes:** Actual archive restoration is proved separately; this fixture isolates boot ordering.

### AC-I363-L82

> `tools/cloud-pair-migration` covers both later cases: the other guest's step follows after the move (step 5), and a guest that missed its step and backed up into the earlier folder has those saves merged by MOVE with nothing left behind (step 5n; 5m checks absent-root refusal/follow) -- its PASS lines.

**Source:** #363, inputs/issues/363.md:82
**Checked:** 2026-10-06T15:38:46.237028+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/optins-11/artifacts/pair-console.log step5 follows with journal/quiet state, step5m stages old pointers and proves absent-root backup refusal then follow, step5n stages older cloud bytes and proves protected merge with all final bytes/no old files; final42PASS/0FAIL.

**Refutation attempted:** Read the staged-input labels:5m resets candidate pointers and5n plants older-build bytes; neither is relabeled as an old binary understanding the new marker.

**Notes:** Initial mixed-image/actual update phases1–4 and staged later-state phases5m/5n are distinct.

### AC-I353-L31

> A carried upstream `/GAMES` (a value no player typed) counts as no folder (D-CLOUD-161). At the end of cloud setup the seeding points it at `/pixelelated` and makes the three folders without asking (D-CLOUD-169: `tools/last-good-scripts-test`'s `--settle` lines); at boot the cloud folder step offers CREATE IT / CHOOSE A FOLDER / NOT NOW (D-CLOUD-170: guest d's epic proof, case E's frame), and so does a transfer page's scan, where CREATE IT writes the three `/pixelelated` paths (case B: the conf's three lines and `tools/cloud-test-backend ls`); with a `/GAMES` that holds files the dialog is the move naming `/GAMES` (case B0's frame).

**Source:** #353, inputs/issues/353.md:31
**Checked:** 2026-10-06T15:38:46.237045+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 B7checks and E6checks show populatedGAMES prompts move; absentGAMES CREATE IT settles saves/backups; boot offers CREATE/CHOOSE/NOT NOW after78no-folder. Fresh scripts1719 includes settle and current/legacy creation controls.

**Refutation attempted:** B’s explicit empty CONTENT_REMOTE intentionally preserves the cloud root under #380; the literal historical three-path phrasing does not authorize overwriting that deliberate content choice.

**Notes:** Defaults follow D-WORKFLOW-144, and independent content choices follow #380.

### AC-I353-L33

> The folder is settled by the cloud folder step, at the end of cloud setup and at boot (D-CLOUD-170, #363), never by a sync: with the folder absent the startup and exit syncs end in the card's `SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET` pointing at MANAGE CLOUD STORAGE (the startup stamp's `78 no-folder`, D-CLOUD-166), and 640x480 frames show the step at the end of setup (guest d's epic proof, case L) and at boot (cases E and I).

**Source:** #353, inputs/issues/353.md:33
**Checked:** 2026-10-06T15:38:46.237063+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 E/L/I logs and directly viewed E card/offer plus L setup-complete demonstrate setup/boot settlement and78no-folder refusal. cloud_backup:1670-1698 suppresses absent earlier defaults; fresh sectionad four controls pass.

**Refutation attempted:** No sync silently creates oldGAMES; boot-only pointer preparation is explicitly approved D-CLOUD-173 and not a recurring migration before each transfer.

**Notes:** The card and later dialog are separate observed surfaces.

### AC-I353-L34

> The offer carries a third choice to pick a different folder (the folder chooser of #352), and its text has no icon or glyph drawn between its two sentences: a 640x480 frame from guest d and, when it is next staged, one from the device.

**Source:** #353, inputs/issues/353.md:34
**Checked:** 2026-10-06T15:38:46.237081+00:00
**Verdict:** PASS ✓

**Evidence:** Directly viewed E/01-E-step-offer.png640x480: CREATE IT, CHOOSE A FOLDER, NOT NOW; no icon/glyph between explanatory sentences. GuiMenu.cpp:5410-5440 routes CHOOSE A FOLDER through the existing sync path editor.

**Refutation attempted:** Distinguished the cloud-root choice from the content-only chooser; both have their own source paths.

**Notes:** Physical-device repeat is later staging evidence; the named UI behavior is VM-verifiable.

### AC-I353-L35

> The words the offer uses are approved by the maintainer before the build (`player-language.md`): proposed `YOUR CLOUD HAS NO /ROCKNIX/Saves FOLDER YET.` / `CREATE IT`, `CHOOSE A FOLDER`, `NOT NOW`; their French lands in the same commit (D-UI-051).

**Source:** #353, inputs/issues/353.md:35
**Checked:** 2026-10-06T15:38:46.237098+00:00
**Verdict:** PASS ✓

**Evidence:** D-CLOUD-164 records owner approval of all13cloud-epic strings. ESdc819f432483acad722a14234d7bbe6b999a705c introduces source and French together; fr.po includes creation/move/chooser lines. Current E/K images show the revised dynamic pixelelated destination.

**Refutation attempted:** Verified the decision’s explicit approval instead of asking again or treating a proposal as approval.

**Notes:** D-WORKFLOW-144 changes project spelling without reopening settled cloud behavior.

### AC-I353-L36

> The default folder's name (`/ROCKNIX` today, D-WORKFLOW-101; `/pixelelated` proposed) is a register row on the maintainer's word, with D-WORKFLOW-101's mixed-installation test run before any default changes.

**Source:** #353, inputs/issues/353.md:36
**Checked:** 2026-10-06T15:38:46.237114+00:00
**Verdict:** PASS ✓

**Evidence:** D-CLOUD-158 explicitly reverses D-WORKFLOW-101 and keeps mixed-installation gate; D-WORKFLOW-144 changes destination to lowercasepixelelated. docs/qa-logs/2026-10-05-pixelelated-replacement-09/optins-11/artifacts/pair-console.log names real old69e6039f8f and currentcf511ce79b, updates the old guest in place and verifies byte-preserving convergence;42PASS.

**Refutation attempted:** Checked the oldbinary identity rather than a simulated branded predecessor; no unfielded /Rasteratops adoption test is required.

**Notes:** The required supported adoption is ROCKNIX→pixelelated.

### AC-I364-L33

> A backup on a carried `/GAMES` the cloud does not hold makes no `/GAMES`, sends nothing, prints `>>> offer create-saves-folder|/GAMES` and ends 0, on a deliberate run and on the exit sync's `--automatic --recent` run. A `/GAMES` the cloud holds is backed up as before, and an absent current folder is still made (`tools/last-good-scripts-test` section ad, its four PASS lines; against the previous commit the first two FAIL).

**Source:** #364, inputs/issues/364.md:33
**Checked:** 2026-10-06T15:38:46.237130+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_backup:1670-1698 returns the create-saves-folder offer without mkdir/copy when a successful parent probe proves absence. Fresh scripts.log:1492-1495 passes deliberate and recent-automatic absentGAMES, existingGAMES and absent-current controls.

**Refutation attempted:** Positive existing and current cases prevent a trivial fix that refuses every backup; unknown provider controls are separately preserved.

**Notes:** No extra layout preparation replaces the bounded existence check.

### AC-I364-L34

> At a boot on a stock-shaped conf with nothing in the cloud, the startup card reads SKIPPED with `78 no-folder`, the QA cloud holds no `/GAMES` afterwards, and the cloud folder step offers CREATE IT (guest d's epic proof, case E: its PASS lines and `tools/cloud-test-backend ls`).

**Source:** #364, inputs/issues/364.md:34
**Checked:** 2026-10-06T15:38:46.237147+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/guest11 E log records1791186987 78 no-folder, noGAMES payload, unchanged configuredGAMES afterNOT NOW and creation offer; direct640px startup/offer frames match.

**Refutation attempted:** Read cloud absence assertion and kept pointer, not only the reassuring card text.

**Notes:** This is a stock-shaped configuration fixture, explicitly distinct from the separate actualRC2 update.

### AC-I364-L35

> The cost the listing adds to an exit sync on an earlier folder (59 ms on run 101's follow benchmark, against 16 ms on run 100) is kept with its reason or removed, decided against #365's folder table (D-WORKFLOW-134).

**Source:** #364, inputs/issues/364.md:35
**Checked:** 2026-10-06T15:38:46.237162+00:00
**Verdict:** PASS ✓

**Evidence:** cloud_backup:810-823 uses one trailing-slash parent-directory listing, with unknown fallback at1670-1698; D-CLOUD-173 retains absence safety. runtime12 actual-byte timing gives269/245ms medians,24ms≤30,0migration prep; original historical costs remain recorded.

**Refutation attempted:** The overhead decision preserves the missing-folder guard rather than caching away a required check or relaxing the30ms limit.

**Notes:** Current evidence is identified runtime12; no new performance measurement is inferred from unrelated14 smoke.

### AC-I353-L32

> An earlier `/ROCKNIX` folder gets one dialog, MOVE first (D-CLOUD-160): MOVE copies, verifies and deletes (the move page's frames on guest d; `tools/cloud-test-backend ls` shows `/pixelelated` whole and no `/ROCKNIX`; a kill during the copy leaves `/ROCKNIX` intact and a second MOVE completes it); another device on `/ROCKNIX` is re-pointed at its next cloud folder step or transfer-page scan with no dialog (`tools/cloud-pair-migration` step 5's journal line, D-CLOUD-170), one that wrote there first is merged by its MOVE (step 5m, D-CLOUD-168); KEEP USING leaves a device on `/ROCKNIX` for good; NOT NOW asks again at the next boot and the next transfer page.

**Source:** #353, inputs/issues/353.md:32
**Checked:** 2026-10-06T15:38:46.237178+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** docs/qa-logs/2026-10-05-pixelelated-replacement-09/optins-11/artifacts/pair-console.log establishes move/follow/staged late-write merge; guest11 I proves NOT NOW/retry/settled boot; fresh A57 host check kills process group before the third copy and recovers. Focused boundaries adds four copy/deletion fault classes on real guests.

**Refutation attempted:** Read tools/last-good-scripts-test:8622-8660: the SIGKILL hook is before rclone copy starts. Neither that nor an injected provider error proves an actual installed transfer killed while copying.

**Notes:** Safe copy/verify/delete and boundary retry are established, but the explicit during-copy kill requirement remains narrower than available evidence.

**Gaps:** Locate an actual installed mid-copy kill receipt or add one on the owned VM/backend before closing this criterion; preserve source bytes and complete a secondMOVE.

### AC-I353-L52

> The move carries `Saves-replaced` (the set-aside of conflict losers beside the saves folder) to `/pixelelated/Saves-replaced` by the same copy, verify, delete, and nothing of ours remains under the old name afterwards: a `tools/last-good-scripts-test` case seeds a set-aside copy under the old layout and reads it back under the new one with the old folder gone; the round trip on the VM shows the sync's next set-aside landing under `/pixelelated`.

**Source:** #353, inputs/issues/353.md:52
**Checked:** 2026-10-06T15:38:46.237195+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** guest11 A verifies all four folders including Saves-replaced moved, old source removed. Focused boundaries preserves distinct discarded-save SHA through faults/retries; fresh host tests retain shelf cases.

**Refutation attempted:** Pair5n merges distinct names; that alone does not establish a new conflicting save’s next set-aside under pixelelated.

**Notes:** Existing shelf migration passes. The explicit next-sync set-aside receipt has not yet been located in the read evidence.

**Gaps:** Read a subsequent installed sync conflict/shelf path assertion, or retain that check during the next affected qualification.

### AC-I365-L101

> `docs/` carries the cloud folder's state table: each combination of conf state and cloud state, with what each actor does and the code line that does it. A walk of the table against the scripts lists no cell where two actors disagree, or names each disagreement as a decision.

**Source:** #365, inputs/issues/365.md:101
**Checked:** 2026-10-06T15:44:25.291764+00:00
**Verdict:** PASS ✓

**Evidence:** docs/rasteratops/cloud-folder-state-table.md:18–121 records dimensions, eight concrete call paths for seven actors, T01–T25 decisions and named disagreement dispositions; :173 onward adds T26 and executable current-source coverage. R/cloud_migrate_layout shared transition, cloud_setup settlement guard, cloud_backup/restore probes and E/main.cpp startup gate were read against this map.

**Refutation attempted:** Did not treat the deliberately preserved run101 table as current behavior: remediation/current-source sections and source anchors distinguish historical failures. Direct-save bypass is an explicit D-CLOUD-169 boundary.

**Notes:** The table is a classified behavioral model. Newly found content recognition and refusal wording defects #467/#468 remain audit findings; this document criterion does not waive them.

### AC-I365-L103

> The guest-d proof runs from `tools/` with a per-case state reset. Its exit code is non-zero when any check fails, seen once on a constructed failure.

**Source:** #365, inputs/issues/365.md:103
**Checked:** 2026-10-06T15:44:25.291830+00:00
**Verdict:** PASS ✓

**Evidence:** tools/rasteratops-vm-cloud-epic:4–40 runs each selected case in a separate process and returns accumulated failure; fresh evidence/guest-negative-02/result.json records actual expected rc1, console 0 PASS/1 FAIL at15:43:45UTC. Q09/guest-11 retains installed per-case resets and runtime assertions.

**Refutation attempted:** Ran --inject-failure ourselves without a guest: failure propagates through the actual check/done/exit path. Inspected normal prerequisite and per-case dispatch rather than counting a printed PASS.

**Notes:** The injected negative tests process reporting; it does not simulate a VM failure. Normal installed runtime evidence is separate.

### AC-I365-L104

> The retro file over runs 95 to 101 names each pattern with its guard, in `tools/`, `.githooks/` or `.claude/rules/`, as `ceremonies.md` asks of a blindspot.

**Source:** #365, inputs/issues/365.md:104
**Checked:** 2026-10-06T15:44:25.291857+00:00
**Verdict:** PASS ✓

**Evidence:** docs/retros/2026-10-02-cloud-runs-95-101.md names five patterns and links implemented guards: actor-state runner, source-derived stale-path checks, separate-process/reset/negative controls, actual UI/byte assertions, and issue-tracking reconciliation. Current tools/rasteratops-cloud-layout-test, rasteratops-vm-cloud-epic and last-good-scripts-test implement those guards.

**Refutation attempted:** Compared claimed guard mechanisms to executable sources and fresh316/1719 outputs, rather than accepting the older322/1367 count as current.

**Notes:** Historical run counts remain labeled as historical.

### AC-I365-L117

> T17 fault-and-recovery VM case proves no misleading old-root seeding after failed settlement while the wizard can finish and the boot step can retry; retained log shows initial/final pointers, README locations and sentinel hashes.

**Source:** #365, inputs/issues/365.md:117
**Checked:** 2026-10-06T15:44:25.291883+00:00
**Verdict:** PASS ✓

**Evidence:** Q09/cloud-ui-08/artifacts/cloud-ui/UI17/logs/run.log has19PASS/0FAIL; UI17-before-cloud.json equals the failed cloud snapshot, with Setup.srm SHA d7c0956d2b153e4c48ac6e75125255c465555cbc0a65793c3e4e459b108afa5d. Recovery retains that byte stream under pixelelated/Saves and markerSHA be68d69fa1fe3ddbcaa9295b8e3e732fd0113d909e38cf643d95aab41c9b1a22; recovery-step/journal logs show next-boot MOVE and completion.

**Refutation attempted:** Read real fault activation, wizard completion, absence of README/marker/new roots while faulted, initial/final pointers and payload hashes. Fault dismissal alone would not satisfy the case.

**Notes:** Replacement09 execution; cloud scripts are byte-continuous through frozen14. No new14 UI execution is claimed.

### AC-I365-L118

> The new independent settings/content/archive dimensions and residual cases are represented in the table and promoted guest proof with reset, failing negative control and byte/pointer assertions; source-only hypotheses remain explicitly distinguished from executed failures.

**Source:** #365, inputs/issues/365.md:118
**Checked:** 2026-10-06T15:44:25.291902+00:00
**Verdict:** PASS ✓

**Evidence:** State table T20–T26 plus tools/pixelelated-vm-cloud-boundaries and BND/proof.py map independent backup/content pointers, root/omitted/custom transitions, configured-first residual, collision, restricted parent and distinct-follower recovery. Retained BND36 installed assertions include reset and exact bytes/pointers; Q09 predecessor65/UI17/guest cases separately exercise startup and archive behavior. Fresh guest negative rc1 is retained.

**Refutation attempted:** Inspected setup/reset and fault boundaries in the actual proof, including distinct second-guest identity; source hypotheses are not treated as executed failures. No actual mid-copy kill is inferred.

**Notes:** I353-L32 separately records the missing mid-transfer kill proof; this does not invalidate the executed operation-boundary/dimension coverage.

### AC-I390-L18

> The fixture returns absence for a missing marker, returns stored marker bytes, and retains rcat bytes; targeted setup cases exercise both path and bucket modes.

**Source:** #390, inputs/issues/390.md:18
**Checked:** 2026-10-06T15:44:25.291920+00:00
**Verdict:** PASS ✓

**Evidence:** tools/last-good-scripts-test:4620–4685 C2 fixture now makes cat return3 for absence or stored marker bytes and rcat persist stdin. C2 path/bucket setup cases and the fresh1719-script suite pass; the focused316-layout suite also passes.

**Refutation attempted:** Read marker read/write fixture branches and separate backend path handling; absent marker is not represented as empty successful content. The old host-suite-before-fixture-fix.log exposes44 harness failures.

**Notes:** Host fixture contract, not a production runtime claim.

### AC-I390-L19

> The complete host script suite has no regressions from the fixture correction; output and source revision retained.

**Source:** #390, inputs/issues/390.md:19
**Checked:** 2026-10-06T15:44:25.291936+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-m7-p1/host-suite-after.log ends PASSED (focused93/0 then full suite result). Fresh evidence/host-checks-01/activity/scripts.log has1719PASS/0FAIL; results.json records command rc0 with frozen14 system and exact E.

**Refutation attempted:** Compared original44 failures with corrected run, then independently ran current complete suite; retained command/source custody prevents silently substituting another checkout.

**Notes:** Current count is1719, not the older historical count.

### AC-I390-L20

> The marker failure is recorded as fixture evidence, distinct from the reproduced production failures on #356.

**Source:** #390, inputs/issues/390.md:20
**Checked:** 2026-10-06T15:44:25.291952+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-03-m7-p1/host-suite-before-fixture-fix.log marker failures occur in the C2 test shim; production malformed/future-marker and retry-before artifacts are separate. Source correction is in last-good-scripts-test cat/rcat fixture, while R/cloud_migrate_layout owns the product marker validation.

**Refutation attempted:** Followed the failing setup path into the fixture and compared its supplied marker bytes; did not attribute44 test-environment failures to the product.

**Notes:** Independent #468 remains a real installed UI reason defect, distinct from this repaired fixture.

### AC-I365-L102

> An actor × state coverage map names an executable assertion for every applicable T01–T26 cell (and a reason for each inapplicable one); `tools/last-good-scripts-test` runs those cases and passes. The previous commit fails the cases for the cells this work changed.

**Source:** #365, inputs/issues/365.md:102
**Checked:** 2026-10-06T15:45:09.677511+00:00
**Verdict:** PASS ✓

**Evidence:** docs/rasteratops/cloud-folder-state-table.md:173–end and actor-case-map.json name208 actor cells across26 states. Fresh evidence/actor-map-pass-coverage.json mechanically matches all210 unique executable case names to PASS lines in our current host suite (0 missing). Earlier baseline.log has36PASS/22FAIL, including T17/18/20/21/24 changed behavior; boundary/predecessor old/fixed controls cover later extensions.

**Refutation attempted:** Checked actual map cardinality and all named PASS lines, plus original failure text and the fixture implementation. T23 reuse and T26 direct/preflight distinctions are explicitly documented rather than pretending208 wholly independent functions.

**Notes:** Fresh316 focused/1719 total checks pass; installed VM coverage is separately required and assessed.

### AC-I377-L22

> Production-path cases distinguish present, absent and failed parent listings; the failed listing cannot produce a create-folder offer. The old commit fails the regression case and the fixed commit's PASS lines are retained.

**Source:** #377, inputs/issues/377.md:22
**Checked:** 2026-10-06T15:45:09.677581+00:00
**Verdict:** PASS ✓

**Evidence:** R/cloud_backup:810–840/1670 and cloud_restore:1688–1760 distinguish present/absent/unknown; failed discovery suppresses creation. Oct2 baseline.log contains both T18-bucket-backup-unknown and restore FAIL; fresh316 focused run passes the exact whole-script cases and parent error3/4/5/7 controls. Installed S3 attempt03 demonstrates actual parent403 with child200.

**Refutation attempted:** Read the exact whole-script injected predicate and proof that fault-fired exists; failed features read is an additional restore case. Confirmed original absence-offer failure rather than a generic unavailable endpoint.

**Notes:** Unknown backup retains the existing fallback policy; the criterion forbids a false create-folder offer, not all backup attempts.

### AC-I377-L23

> The corresponding backup/restore bucket predicates are audited together; each failed-read fixture either passes a regression test or has a documented source-based reason it cannot reach the bad branch.

**Source:** #377, inputs/issues/377.md:23
**Checked:** 2026-10-06T15:45:09.677608+00:00
**Verdict:** PASS ✓

**Evidence:** Both production helper/caller pairs and tools/rasteratops-cloud-layout-test:335–347 were read together. Synthetic bucket sets the literal /ROCKNIX/Saves so the superseded backup guard is reachable. Actual bucket-prefixed S3 restore has no corresponding literal gate; its HTTP proxy-events.json records403 at Rasteratops/ after200 at child.

**Refutation attempted:** Confirmed ordinary rocknix-qa/Rasteratops/Saves cannot satisfy the exact old-root backup predicate; did not count the normal S3 backup round trip as that branch proof.

**Notes:** Separate host synthetic backup and installed S3 restore evidence preserve branch reachability distinctions.

### AC-I377-L24

> A whole-script synthetic bucket case with a reachable superseded literal tests the backup guard; an S3 QA fault case tests the ungated restore sibling. Each injects the failed parent listing, preserves sentinel hashes, reports the truthful outcome and succeeds after the fault is removed. The normal bucket-prefixed S3 backup fixture does not reach superseded_saves_setting and cannot count as that branch’s test.

**Source:** #377, inputs/issues/377.md:24
**Checked:** 2026-10-06T15:45:09.677636+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Current provider_failure fixture reaches the literal backup guard, asserts fault-fired/no create offer/unchanged cloud sentinel; baseline fails and fresh host run passes. Actual S3 attempt03 assertions/proxy-events/refused-output/sentinels prove nonzero restore, truthful refusal, local/cloud preservation, removal of403 fault and exact retry restore.

**Refutation attempted:** Read the entire synthetic provider_failure function: it does not remove the fault and run a successful backup retry, nor assert backup terminal status/truthful outcome. No such additional literal-backup receipt is established by the normal bucket-prefixed S3 result.

**Notes:** This is a missing part of the literal-backup test contract, not an observed product data-loss defect.

**Gaps:** Add a reachable literal synthetic bucket backup failure→retry proof with distinct local/cloud hashes and truthful terminal outcome; retain actual S3 restore evidence.

### AC-I377-L25

> Existing absent-legacy-root refusal, current/custom-root creation and corrected pair-migration cases remain green. No extra recurring network probe is introduced without #364's timing acceptance being reverified.

**Source:** #377, inputs/issues/377.md:25
**Checked:** 2026-10-06T15:45:09.677656+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh316/1719 suites cover absent legacy refusal/current/custom creation; Q09/optins-11 actual42PASS mixed predecessor pair preserves/follows/merges, and runtime12 five-sample installed comparison is269vs245ms (24ms, limit30) with identical2000-byte payload and no migration journal.

**Refutation attempted:** Inspected single-parent listing implementation and actual paired timing rows. Current14 single-sample protocol smoke is not substituted for the five-sample performance evidence.

**Notes:** Runtime09 source continuity to14 established separately; no new recurring network probe is introduced by the reviewed change.

### AC-I366-L34

> The stale-name check reads the list from `cloud_migrate_layout --superseded` and matches each entry as a whole path component; run against today's `tools/cloud-test-backend` (the bare `/GAMES` at line 806) it FAILs, and that failing run is recorded in the day's work log with its command (`engineering-practices.md` § Guards must fail closed).

**Source:** #366, inputs/issues/366.md:34
**Checked:** 2026-10-06T15:45:56.647276+00:00
**Verdict:** PASS ✓

**Evidence:** last-good-scripts-test:9005–9060 derives whole-component patterns from production --superseded. 2026-10-04-qa-fixture-guard/guard-extracted.py and old.log identify actual b2378d9 source line806 and reject its backend prefix/default mismatch; result.json binds old-backendSHA90f5df2d and guardSHA c53df68f. Current full suite passes this exact guard.

**Refutation attempted:** Read the actual old failure output and source-derived regex, including inline-comment control. Bare /GAMES is matched without maintaining another hand-coded old-name list.

**Notes:** Historical command and work-log21:58 retained; fresh full-suite run independently validates current guard.

### AC-I366-L35

> `tools/cloud-test-backend saves-remote` names, on every backend `tools/cloud-test-backend backends` lists, a folder that `cloud_migrate_layout --superseded` does not list: a check in `tools/last-good-scripts-test` that loops over the backends and PASSes.

**Source:** #366, inputs/issues/366.md:35
**Checked:** 2026-10-06T15:45:56.647339+00:00
**Verdict:** PASS ✓

**Evidence:** Current full1719 suite runs advertised-backend loop. Guard result.json lists webdav/ftp /pixelelated/Saves, S3 /rocknix-qa/pixelelated/Saves, SMB /qashare/pixelelated/Saves and the SFTP QA data prefix. Source derives prefix plus shipped default and rejects each superseded path.

**Refutation attempted:** Checked nonempty unique backend enumeration and S3 name regex/no-IP/no-double-dot controls, not merely one WebDAV result.

**Notes:** No backend listener is started by these path-query controls.

### AC-I366-L36

> `tools/vm-qa`'s round-trip suite reads PASS in `report.md` on the first image built after the fix, and its `round-trip.log` names the new folder on the `SAVES_REMOTE` line.

**Source:** #366, inputs/issues/366.md:36
**Checked:** 2026-10-06T15:45:56.647373+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-03-archive-harness/rerun/report.md exact503e24e10d first post-fix image has round-trip PASS81s; round-trip.log says /Rasteratops/Saves and all9 uploaded and restored byte-identical.

**Refutation attempted:** Read original historical build identity and then-current default; do not rewrite the old run as /pixelelated. Original unrelated harness failures remain retained.

**Notes:** Current14 separate three-protocol318 proof uses the renamed default; it is not substituted for the first-post-fix criterion.

### AC-I366-L37

> The S3 backend still gets a legal bucket name: `tools/cloud-round-trip --backend s3` against a QA guest logs `only 9/9` or no shortfall line for its saves upload.

**Source:** #366, inputs/issues/366.md:37
**Checked:** 2026-10-06T15:45:56.647394+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-03-m7-qa-01/s3/report.md actual503e24e10d PASS107s; round-trip.log selects /rocknix-qa/Rasteratops/Saves and verifies all9 original, all9 replaced, all9 restored bytes. Current full guard validates legal S3 bucket names.

**Refutation attempted:** A bucket prefix remains distinct from an ordinary path, and successful transfer assertions defeat a trivially empty-upload pass.

**Notes:** No live provider account or personal data involved.

### AC-I401-L33

> Retain both original failures and code/history trace with actual guest evidence.

**Source:** #401, inputs/issues/401.md:33
**Checked:** 2026-10-06T15:46:44.920230+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-03-content-network/s3-before-link.log:51–81 retains actual LINK3/4 success-after-outage failures at70.3/59.0s and wrongly successful stamps; s3-before-guest.log retains actual command output. Shared helper and caller diff show the formerly direct rclone commands now use progress-sensitive bounded_content_rclone.

**Refutation attempted:** Separated LINK7 pre-cut fixture failure (#402) from the two genuine interrupted-transfer product failures; byte-valid retries do not excuse waiting out the outage.

**Notes:** Original failures preserved without relabeling.

### AC-I401-L34

> Content network operations stop after bounded inactivity across provider SDK retries; progressing large transfers and cancellation remain functional. Actual-source stalled/progressing/failure controls prove the distinction.

**Source:** #401, inputs/issues/401.md:34
**Checked:** 2026-10-06T15:46:44.920287+00:00
**Verdict:** PASS ✓

**Evidence:** R/cloud_content_transfer:28–164 parses five monotonic high-water counters, bounds inactivity and preserves progressing operations; SIGINT/TERM/EXIT clean tracked child/tee. test-content-guard.py executes source-extracted old/new copy calls; guard-controls and BusyBox summaries each12PASS/6FAIL before,18PASS/0FAIL after. Current1719 suite reexecutes permanent whole-script6 controls.

**Refutation attempted:** Read cancellation waiting for a live child, stale retry totals versus growing bytes/listed counts, >3GiB arithmetic, failed guard storage and unchanged6s grace. Progress tests last beyond the stall bound; no overall transfer timeout is imposed.

**Notes:** Installed link-loss results below establish target behavior; host controls alone are not image qualification.

### AC-I401-L35

> WebDAV and S3 content backup/restore and affected scan cases pass real link-loss/retry/whole-byte/stamp checks under unchanged bounds on the replacement image.

**Source:** #401, inputs/issues/401.md:35
**Checked:** 2026-10-06T15:46:44.920314+00:00
**Verdict:** PASS ✓

**Evidence:** Q09/link-10 actual two installed seven-case matrices:75 WebDAV/76 S3 assertions, four result channels0 and actual cleanup07:13:44. S3 LINK3/4 stop35.1/35.2s after cut withrc69; WebDAV30.1/30.0s. Both prove no partial litter, matching whole receiving files, failure stamps and plain-retry exact bytes; scans preserve unrelated stamps and recover24systems+BIOS.

**Refutation attempted:** Read logs with observed unavailable route/address during40.7s outage, not merely an endpoint URL refusal. S3 scan is plainrc1 after41.4s with truthful reason; did not misreport it asrc69.

**Notes:** Replacement09 execution is byte-continuous for these scripts through14; no repeated14 cut run claimed.

### AC-I401-L36

> Full affected host/package gates and image upgrade/clean qualification pass; source, artifact and remaining priorities are recorded.

**Source:** #401, inputs/issues/401.md:36
**Checked:** 2026-10-06T15:46:44.920340+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh host-checks01 full1719 and focused316 pass with exact14 tools; frozen14 qa18 clean/default and actual26-check RC2 upgrade receipts bind unchanged helper and both callers. Q09/link-10 completion and frozen source/bundle custody retain exact runtime inputs.

**Refutation attempted:** Retained prior1373/322 and outer143 discrepancy as historical; acceptance uses current complete result channels and actual cleanup, never outer-only success.

**Notes:** Image/source/gate receipts are independently audited; candidate still blocked by new unrelated findings #467/#468.

### AC-I429-L28

> Retained original failure, all result channels and actual cleanup receipt; diagnosis names measured operations/conditions and distinguishes product cost from measurement noise.

**Source:** #429, inputs/issues/429.md:28
**Checked:** 2026-10-06T15:46:44.920358+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-04-pixelelated-57cbc-qualification/runtime-06/comparison.json retains286/250ms=36ms>30, same cloud_backupSHA12a23169; completion has actual/four rc1 and all5ownedPIDs absent00:43:50. timing-diagnosis.md and diagnostic02 separate24ms listing cost, actual timestamp evidence and three predeclared batches.

**Refutation attempted:** No unsupported causal claim that swap or VM noise caused the36ms difference; diagnostic01 missing-byte failure and diagnostic02 parser error remain failures.

**Notes:** Acceptance is distinct fresh runtime07 and later runtime12, not a renamed failed run.

### AC-I429-L29

> Any correction preserves missing/unknown-folder behavior with meaningful negative controls; no original frozen owner or source tree is edited.

**Source:** #429, inputs/issues/429.md:29
**Checked:** 2026-10-06T15:46:44.920375+00:00
**Verdict:** PASS ✓

**Evidence:** Product cloud_backup retains parent-directory predicate and missing/unknown branch distinction; fresh T14/T18 and all parent-error controls pass. Diagnostic change is only the clock-safe helper; timing-proof.py waits beyond remote timestamp outside measurement without modifying product, clock or mtime.

**Refutation attempted:** Compared source hashes before/after and inspected meaningful absent/unknown negative controls. No presence cache or retry-until-lucky change was introduced.

**Notes:** Fresh owners preserve original failed backing/receipts.

### AC-I429-L30

> Exact candidate installed qualification meets the unchanged five-sample alternating median30ms limit, with every transfer byte verified and no migration preparation; retain all attempts and justify any repeat from the diagnosis.

**Source:** #429, inputs/issues/429.md:30
**Checked:** 2026-10-06T15:46:44.920390+00:00
**Verdict:** PASS ✓

**Evidence:** runtime07 completion actual29491/fourrc0; installed-samples/comparison gives272/244ms=28≤30, twelve actual transferred-byte/timestamp records and zero migration journal. Later Q09/runtime12 same script five alternating medians269/245=24ms with all12 byte comparisons.

**Refutation attempted:** Original runtime06 36ms remainsfailed; fresh repeat justified by actual fixture flaw, three declared diagnostic batches and separate trace collection. Single-sample14 smoke not used as acceptance timing.

**Notes:** Neither instrumented trace timings nor successful diagnostic substeps qualify the acceptance owner.

### AC-I430-L31

> Original failures and limited readonly-inspection evidence are retained, and fresh acceptance ownership remains distinct from diagnostics under #429.

**Source:** #430, inputs/issues/430.md:31
**Checked:** 2026-10-06T15:46:44.920409+00:00
**Verdict:** PASS ✓

**Evidence:** Original diagnostic01 actual/fourrc1 remains retained; inspection01 failed-save-facts.json shows persisted c8629db9 bytes on both sides and guest mtime1135.277ms older, not the original live4ff90268 write. Diagnostic02 actual/fourrc1, trace01 actual/fourrc0, runtime07 actual/fourrc0 have separate owners and actual cleanup receipts.

**Refutation attempted:** Read persisted byte hashes and receipt chronology; inspection after abrupt guest stop cannot reconstruct the lost live timestamp. Instrumented trace and diagnostic batches never substituted for uninstrumented acceptance.

**Notes:** The evidence explicitly limits what the read-only inspection proves.

### AC-I429-L31

> Installed identity/Tools consumer proof completes, and M7/checkpoint identify the accepted artifact and next dependency-gated owner.

**Source:** #429, inputs/issues/429.md:31
**Checked:** 2026-10-06T15:49:19.887883+00:00
**Verdict:** PASS ✓

**Evidence:** runtime07 identity-proof.py executes installed13 checks; assertions.json confirms actual upgraded Tools XML/hash, identity, retired reporting/updater, policy bytes. Exact actual/fourrc0 and owner cleanup independently read. Current M7 body and checkpoint retain accepted frozen14 custody and P4→capacity→H700 order.

**Refutation attempted:** Read the executed consumer commands: /storage/.config/modules/gamelist.xml is hashed and parsed, not only the package template. Silent update decline is rc1/zero bytes, not generic help success.

**Notes:** This closes the original identity stage; later product defects still block overall readiness.

### AC-I351-L58

> 1: the Close control sits at the bottom of the page, below the note, with at least 2rem of space above it, and a tap asks a confirmation (the safe answer first) before Escape is sent; a 390 px headless-Firefox render shows the placement, and the page's load test (the harness from #330) passes.

**Source:** #351, inputs/issues/351.md:58
**Checked:** 2026-10-06T15:49:19.887952+00:00
**Verdict:** PASS ✓

**Evidence:** R/cloud_oauth:646–657/1000–1023 places .leave after the note with2rem margin; :1179 confirmation uses Keep before Close and sends Escape only on confirmed click. Fresh full-script log:650–653 executes the node page interaction/load controls. Directly reviewed Q10/signin-ui14 04/05 phone frames; signin-proof.py:308–331 uses actual headless Firefox157 and390px iframe.

**Refutation attempted:** Keep sends nothing; hidden CSS rule prevents both controls showing together. Actual390px frames place Close below the complete note and separated from the pointer pad.

**Notes:** Frame review performed before this verdict; no mocked DOM screenshot claim.

### AC-I351-L59

> 2: the state line has at least `.75rem` above and below it in both states (`Checking…`, `Connected.`); the two 390 px renders show it.

**Source:** #351, inputs/issues/351.md:59
**Checked:** 2026-10-06T15:49:19.887985+00:00
**Verdict:** PASS ✓

**Evidence:** Q10/signin-ui14 phone-metrics.json records actual390px width/root font16px and12px top/bottom margins in Checking… and Connected. Both original frames directly viewed. R/cloud_oauth #state margin is .75rem 0.

**Refutation attempted:** Actual installed probe transition supplies Connected; delayed first probe preserves Checking, not a manually replaced text node.

**Notes:** Two measured states, not inferred CSS alone.

### AC-I351-L60

> 3: the image ships `CHASSIS=handset` and the installed sign-in window sends Mobile Safari in both actual HTTP requests and `navigator.userAgent`. Replacement10 signin-ui14/15/16 each retain 40 passing checks and 15 reviewed frames; `signin-ui-14/build.log` lines41–47 and `artifacts/signin/all-local-navigator.json` prove this. Replacement14 readback under #462 confirms handset chassis and identical installed `cloud-signin-window`/`cloud_oauth` hashes (`signin-payload-continuity.json`). This reuses explicitly identified prior runtime evidence on unchanged bytes; it is not a new authenticated Dropbox execution. The provider-owned trust-page observation is #463, outside M7.

**Source:** #351, inputs/issues/351.md:60
**Checked:** 2026-10-06T15:49:19.888016+00:00
**Verdict:** PASS ✓

**Evidence:** Q10/signin-ui14 build.log and all-local-requests.json show actual HTTP/start/302/mobile-form Mobile Safari user agent; all-local-navigator.json independently records navigator.userAgent. Frozen14 signin-payload-continuity.json verifies CHASSIS handset and exact windowSHAfc9a3473/OAuthSHAc9982e28.

**Refutation attempted:** Distinguished rclone Go-http-client probe from browser requests; did not count public Dropbox page as authenticated trust-page proof.

**Notes:** Identified prior runtime on unchanged installed bytes, as this reconciled criterion explicitly permits.

### AC-I351-L61

> 4: the finishing page carries the shared `STYLE` (the card, the `h1`, the note), reads as a success, and says what happens next; a frame from guest d's window shows it.

**Source:** #351, inputs/issues/351.md:61
**Checked:** 2026-10-06T15:49:19.888036+00:00
**Verdict:** PASS ✓

**Evidence:** cloud-signin-window.c:415–450 FINISHING_PAGE uses shared visual styling, green Connected heading and Finishing up on your handheld… note. Directly viewed installed02-finishing-marker-stand-in.png; finishing-transition.json changes actual pageSHA36043094→890973b0 after done marker while window stays open.

**Refutation attempted:** Prior local form is rejected by transition/pixel guard; finishing is stable at0/5/10/20s and not merely a screenshot taken from the wrong prior page.

**Notes:** English presentation passes; French completeness fails the separate criterion below.

### AC-I351-L62

> Every string added has its French in the same commit where it is an interface string (D-UI-051), and `tools/vocabulary-check` passes on the scripts.

**Source:** #351, inputs/issues/351.md:62
**Checked:** 2026-10-06T15:49:19.888053+00:00
**Verdict:** FAIL ✗

**Evidence:** D-CLOUD-164 expressly includes phone close confirmation and finishing two lines, each with French. R/cloud_oauth:1016/1179 serves literal English Close/Keep/question; cloud-signin-window.c:430–450 loads one static English FINISHING_PAGE. Source search finds no gettext/system.language/setlocale route in either implementation. Installed payload hashes match these sources; actual EN frames show their shipped wording. Fresh vocabulary164/0 and full script checks pass their narrower scope.

**Refutation attempted:** tools/archaeology --no-gh --since2026-10-01 finishing finds the binding bilingual decision and no exemption. ES catalog mechanism does not translate a static HTML/data URL produced by independent Python/C programs.

**Notes:** This is a failed source/localization contract. No French-mode VM sign-in execution is claimed; add it to repair qualification. External tracker publication is temporarily blocked by approval-review sign-in failure.

**Gaps:** Translate the newly required phone confirmation and finishing text through the selected system language, with EN/FR390px phone and actual installed finishing frames plus unchanged action/escape controls.

### AC-I362-L68

> Owner disposition recorded in D-WORKFLOW-138: refresh with existing functionality preserved.

**Source:** #362, inputs/issues/362.md:68
**Checked:** 2026-10-06T15:51:57.281490+00:00
**Verdict:** PASS ✓

**Evidence:** D-WORKFLOW-138 in docs/decision-register.md:592 explicitly withdraws libsoup3.6.6/proxy old-pin exceptions, requires functionality preservation and refresh. Current libsoup recipe3.8.0 and selected WebKit2.54.1 follow that disposition.

**Refutation attempted:** Read recorded maintainer language and exact current recipes, not issue status.

**Notes:** Decision compliance is separate from complete runtime proof.

### AC-I362-L69

> Recipe uses verified 3.8.0 archive and explicit optional dependency settings; pkgcheck passes.

**Source:** #362, inputs/issues/362.md:69
**Checked:** 2026-10-06T15:51:57.281569+00:00
**Verdict:** PASS ✓

**Evidence:** packages/web/libsoup/package.mk names3.8.0 SHA bbf08fa3e03a88c31a3d27a0d87cb422e9490f2d08e149211103df6d638a2238; cold consumed inventory retains matching1609676-byte archive. Explicit optional settings include disabledzstd/brotli/ntlm/gssapi/sysprof/introspection. Fresh evidence/local-pkgcheck01 validates actual matched recipe rc0/0FAIL.

**Refutation attempted:** Checked late-binding options inside pre_configure_target and actual recipe match; rc0 without a matched file is not counted (the separate libchdr shorthand mistake was corrected).

**Notes:** No product recipe changed during audit.

### AC-I362-L70

> Cold-build WebKitGTK 2.54.1 against libsoup 3.8.0; tools/fork-package-freshness exits 0 and the cut record names both inputs.

**Source:** #362, inputs/issues/362.md:70
**Checked:** 2026-10-06T15:51:57.281596+00:00
**Verdict:** PASS ✓

**Evidence:** P3 cold-webkit-libsoup.json binds consumed archive/build stamps and unchanged recipe hashes. Directly read original cold build.log lines310232/310242 and1179166/1179405: targetlibsoup3.8.0 built, targetWebKit found linkedSoup3.8.0. Frozen14 preparation/package-freshness.log and freshness-completion.json actual/fourrc0 at00:42 bind1608 recipes/tools and both CURRENT inputs.

**Refutation attempted:** Did not count a cached install stamp as cold compilation; original cold log/source inventory is named, replacement10→14 recipe continuity separately verified.

**Notes:** A new optional audit-time network check is pending approval-service authentication; this PASS is the criterion’s retained cold/cut proof, not a later latest-version claim.

### AC-I362-L71

> VM sign-in frames show the sign-in page in touch layout and finishing page; report the30-second combined RSS against D-WORKFLOW-048's approved loaded-page profile (about284MiB on the ordinary guest), explain any material growth, and prove the page loads in an actual1GiB guest without a kernel OOM or lost responsiveness; HTTP/TLS/redirect behavior works on the resulting image. This replaces the undefined “within its bound”: the existing tool has no numerical ceiling assertion.

**Source:** #362, inputs/issues/362.md:71
**Checked:** 2026-10-06T15:51:57.281617+00:00
**Verdict:** PASS ✓

**Evidence:** Installed signin-ui14 actualHTTP302/Mobile-UA/JS-UA and inspected phone/finishing frames establish touch/redirect behavior; public HTTPS pages load. Ordinary8GiB public-login30s peak701264KiB is a heavier workload than D-WORKFLOW-048 simple-page≈284MiB. Actual1GiB signin-1g13 example.org271416KiB and signin-provider1g05 publiclogin395676KiB,30s, responsive/no kernelOOM; actualQEMU1024MiB/firmware1048576KiB, Linux810372KiB recorded. Both loaded640x480frames directly viewed.

**Refutation attempted:** Compared workload and allocation explicitly rather than claiming like-for-like growth from different pages; checked real low-memory allocation, no numerical RSS ceiling invented, no authenticated Dropbox claim.

**Notes:** Source/script payload continuity to14 established. Localization defect I351-L62 remains separate.

### AC-I462-L28

> Append a decision refining D-QA-017/D-QA-041 and update active rules, release readiness, tracker priorities, and resume handoff to make hosted accounts optional; source/readback evidence identifies the changed gate.

**Source:** #462, inputs/issues/462.md:28
**Checked:** 2026-10-06T15:51:57.281636+00:00
**Verdict:** PASS ✓

**Evidence:** D-QA-058 is appended with exact owner direction; vm-first/release-candidates localWebDAV/SFTP/MinIO rules, readiness active heading, saved handoff and tracker-readback.json reconcile hosted-optional gate.

**Refutation attempted:** Read current rule text and exact readback body hashes; historical old Dropbox prerequisites are marked superseded, not counted as active blockers.

**Notes:** No relaxation of separate RA award proof.

### AC-I462-L29

> Frozen replacement14 has separate WebDAV, SFTP, and MinIO/S3 round-trip PASS reports; report exact cases, failures/skips and scope, with immutable image/source identity.

**Source:** #462, inputs/issues/462.md:29
**Checked:** 2026-10-06T15:51:57.281654+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-06-local-cloud three actual7afa9efcfc reports name bundleb77e47e5/imagec7df6a6f and PASS86/73/110s; each round-trip106PASS/0FAIL/0SKIP. Logs verify9upload/replacement/restorebytes, excludes, refusal/stamps and serialization; completion totals318.

**Refutation attempted:** Read installed reports and meaningful negative lines, not only completion summary. Provenance UNSTARTED is the original launch input; later terminal receipts establish actual execution.

**Notes:** Three owned local protocols, no hosted-authentication inference.

### AC-I462-L30

> Retain fresh-owner harness seals, all four watcher result channels, final process/VM/backend cleanup readback, and sanitized evidence. Submission is not completion.

**Source:** #462, inputs/issues/462.md:30
**Checked:** 2026-10-06T15:51:57.281670+00:00
**Verdict:** PASS ✓

**Evidence:** Local-cloud harness seals/source manifest70cb0448 and completion05:59:18 retain four rc0, actual6PIDs absent, noQEMU/MinIO/backendpidfiles and ports9010/9011/9012/9013/10022/10023unbound. Raw sanitized protocol logs and SHA256SUMS are retained.

**Refutation attempted:** Matched source/image and terminal ownership to original fresh owner; submission receipt alone is not qualification.

**Notes:** No original failed owner was overwritten.

### AC-I462-L31

> Preserve unverified Dropbox trust-page behavior in a milestone-less follow-up; reconcile #351's local browser criteria against existing artifacts without claiming an authenticated Dropbox test.

**Source:** #462, inputs/issues/462.md:31
**Checked:** 2026-10-06T15:51:57.281685+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** tracker-readback.json records463OPEN/milestone null and named hosted-optional gate; signin-payload-continuity explicitly reuses prior installed browser evidence without authenticatedDropbox. I351-L58–61 pass against actual artifacts.

**Refutation attempted:** Independent review found that #351 bilingual criterion is not satisfied: static phone/finishing English has no translation route despite D-CLOUD-164. Prior closure is not sufficient reconciliation.

**Notes:** Dropbox deferral is valid and remains unchanged; this gap is local interface localization.

**Gaps:** Reconcile #351’s translation criterion and qualify its French repair; no hosted account is needed.

### AC-I462-L32

> Publish the explicit RA reset target and retain account-backed proof status separately; M7 continues P3 → approved P4 review → H700 arm then aarch64.

**Source:** #462, inputs/issues/462.md:32
**Checked:** 2026-10-06T15:51:57.281701+00:00
**Verdict:** PASS ✓

**Evidence:** Saved checkpoint and RA-award completion identify Tobu15738/Potato-tanSecret100359 softcore:33PASS, initialunearned→queue1→pending0→provider-earned, relaunch28→27, actual/fourrc0 and06:10cleanup/accountclear. Milestone evidence/p4-milestone-after.json orders P4 before capacity461/H700arm→aarch64.

**Refutation attempted:** Kept account-backed proof separate from synthetic UI109 and local cloud318. No renewed reset required merely to restate this proof.

**Notes:** No device action or upstream/publication permission inferred.

### AC-I361-L119

> Owner disposition recorded in D-WORKFLOW-138: refresh current upstream, preserve functionality; prior pin proposal withdrawn.

**Source:** #361, inputs/issues/361.md:119
**Checked:** 2026-10-06T15:53:38.800827+00:00
**Verdict:** PASS ✓

**Evidence:** D-WORKFLOW-138 owner direction explicitly withdraws the old proxy/libsoup exception; P/package.mk pins879b158 and parent-coupled libchdr607694c/rcheevos1433173. Current scope preserves whole-library offline behavior and prepares upstream fixes.

**Refutation attempted:** Read exact pinned recipe and disposition, not a branch name or closed tracker.

**Notes:** Freshness is timed evidence, not a timeless statement.

### AC-I361-L121

> Indexed and unindexed whole-library scans retain truthful readiness, no total-library cap, interruption/retry, polite request pacing, and safe handling of server 429s; a synthetic library over 100 games proves the boundary.

**Source:** #361, inputs/issues/361.md:121
**Checked:** 2026-10-06T15:53:38.800914+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** P/raofflineproxy-cache-indexed:87–112 uses background pacing and persists pauses; unindexed call explicitly opts out of100-game budget and rejects queued readiness. tools/raofflineproxy-integration-test tests125indexed/unindexed,124+retry, persistedpause,429stop/restart and upstream100default. Original whole-library-before reports125OKbut100actual; after125actual. b09host11 tests pass with consumed-source equality to879.

**Refutation attempted:** Reviewed actual cached-row assertions and pause persistence, not reported OK counts. These125-game executions use host Python and mocked provider behavior; current installed proxy14 proves preservation/service/native formats but not this125-game scanner boundary.

**Notes:** No product failure inferred from the missing target-runtime boundary.

**Gaps:** Execute the125-game indexed/unindexed and queued/429/retry controls against installed candidate modules/helper in an isolated VM, preserving pacing semantics and failure controls.

### AC-I361-L124

> tools/fork-package-freshness exits0 on frozen replacement14; freshness05/allfour0 and exact recipe/tool verification retained. Earlier failed13 and completed12 results remain their own evidence.

**Source:** #361, inputs/issues/361.md:124
**Checked:** 2026-10-06T15:53:38.800942+00:00
**Verdict:** PASS ✓

**Evidence:** Frozen14 preparation/package-freshness.log starts/ends exact1608recipe/tool verification and CURRENT879b158/libchdr607694c/libsoup3.8.0/WebKit2.54.1; freshness-completion.json actual/allfour0 at00:42 and fourabsentPIDs. Frozen13 freshness04 failed on newer879 remains separate.

**Refutation attempted:** Read actual exit channels and package rows; not relabeling prior12 or failed13. Purposeful parent-coupled pins are explicitly marked PINNED.

**Notes:** This criterion names frozen14 freshness05. New audit-time recheck is unstarted because approval-service authentication is still failing.

### AC-I408-L18

> Exact branded image reproduces missing automatic account discovery while an explicit-path control succeeds; no credential values enter evidence.

**Source:** #408, inputs/issues/408.md:18
**Checked:** 2026-10-06T15:53:38.800962+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-03-proxy-identity/packaged-identity.json identifies installed config.pyc/OS_NAME RASTERATOPS, automatic=false but explicit=true; assertions.json exactbuild/syntheticaccount pass and automaticdiscovery fails.

**Refutation attempted:** Both routes use the same synthetic account and canonical parser; no credential value appears in the result. Original failure is distinguished from later lowercase identity.

**Notes:** Historical intermediate brand was never fielded; current required transition remains ROCKNIX→pixelelated.

### AC-I408-L19

> A focused upstream-compatible patch recognizes both identities, preserves unrelated-platform behavior and configured overrides, and passes old-code negative controls.

**Source:** #408, inputs/issues/408.md:19
**Checked:** 2026-10-06T15:53:38.800983+00:00
**Verdict:** PASS ✓

**Evidence:** P/patches/018-pixelelated-platform-identity.patch matches complete OS_NAME records for ROCKNIX/pixelelated; focused tests cover custom override, commented/previous-field/lookalike rejection. Original7control before/after and b09 upstream Linux818 tests retain negative/fixed evidence.

**Refutation attempted:** Read full patch and original automatic-versus-explicit controls; no account/cache path relocation. Current lowercase patch supersedes historical Rasteratops spelling.

**Notes:** Generic detector policy only, no behavior change on unrelated OS identities.

### AC-I408-L20

> The next image's packaged resolver automatically reads the canonical synthetic account, and existing cache/sign-in/base/subset queue state survives reopen.

**Source:** #408, inputs/issues/408.md:20
**Checked:** 2026-10-06T15:53:38.801004+00:00
**Verdict:** PASS ✓

**Evidence:** Frozen14 proxy14/assertions.json22PASS: actual packaged modules, lowercase detector/canonical syntheticaccount, all predecessor cache/pending rows and base/subset mapping through2reopens, legacy image bytes, actual service HTTP/cache paths, pending awards remain while offline. Native18/0skip separate.

**Refutation attempted:** Read explicit no-source-override claim together with actual installed custody and real-service assertions; exactrow preservation is stronger than only a count.

**Notes:** Synthetic account/owned VM; separate RA33 proves actual provider award path.

### AC-I384-L14

> The original mapping fails and the patched mapping passes, with the upstream award-parity tests passing against the patched source.

**Source:** #384, inputs/issues/384.md:14
**Checked:** 2026-10-06T15:55:48.391596+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-02-candidate-preflight/subset-old-source.txt actual1→100,2→100 contradicts expectedsubset200; subset-backport-tests.log23passed. Current U/rom_cache.py:362–458 iterates each achievement set’s GameId and lookupwantedIDs. Current b09 Linux818 includes award parity; consumed runtime/test trees equality independently recomputed.

**Refutation attempted:** Read nested set ownership rather than base GameId alone; old ambiguity is reproduced, not merely inferred.

**Notes:** Patch017 is retired because upstream implements the preservation; no duplicate backport remains.

### AC-I384-L15

> The candidate guest preserves each subset game ID and retains the queued award in the offline/proxy regression suite.

**Source:** #384, inputs/issues/384.md:15
**Checked:** 2026-10-06T15:55:48.391658+00:00
**Verdict:** PASS ✓

**Evidence:** Frozen14 subset11/assertions.json35PASS, actualHTTP provider-requests.json fetches game100 andgame200; first flush acceptsbase1/refusessubset2with503 retainingpending1, second sends onlysubset2 and pending0. Empty repeat has no requests; subsetunlock andflushstamp assertions pass.

**Refutation attempted:** Queued subset is neither remapped tobase nor discarded asstale/deleted; failure and retry are actualloopbackHTTP with installed modules.

**Notes:** Syntheticprovider fixture, separate from genuine providerRA33.

### AC-I384-L16

> The candidate records the refreshed exact upstream pin, retired duplicate patch disposition and corresponding source containing the preservation fix.

**Source:** #384, inputs/issues/384.md:16
**Checked:** 2026-10-06T15:55:48.391686+00:00
**Verdict:** PASS ✓

**Evidence:** P/package.mk879b158 SHA98495732; full-series disposition retires017; exact U/rom_cache.py has set-aware mapping. Frozen14 preparation inventory and installedsubset/proxy custodysource7afa9efcfc bind selected implementation.

**Refutation attempted:** Compared actual current mapping and no017patch in16-file series; recipecomment alone would not prove it.

**Notes:** Historical backport23tests remain dated original evidence.

### AC-I451-L28

> The original current-predecessor AttributeError and actual nonzero outcomes are retained.

**Source:** #451, inputs/issues/451.md:28
**Checked:** 2026-10-06T15:55:48.391707+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-05-proxy-3036478/host01-failed/predecessor-diagnostic-stderr.log retains AttributeError get_all_cache_by_prefix; completion actual/allfour1 and all4PIDs absent22:08:07.

**Refutation attempted:** Read actual exception from actual725 predecessor API, not a fake expected failure; old emptybuild.log has its own SHA and does not carry the missingtrace.

**Notes:** This was a harness API failure, not data migration failure.

### AC-I451-L29

> Fresh execution passes all11 fork integration checks with both current7252fc and historical865e21 predecessor sources, preserving exact cache rows, queued base/subset awards, sign-in and legacy images across two reopens.

**Source:** #451, inputs/issues/451.md:29
**Checked:** 2026-10-06T15:55:48.391731+00:00
**Verdict:** PASS ✓

**Evidence:** host02/run.sh separately executes actual7252fc and historical865predecessor integrations; bothlogs11testsOK, fourrc0/cleanup22:10:32. tools/raofflineproxy-integration-test:132–170 dispatches old list versusnewiterator API and compares fullrows/signin/images/base-subset through2reopens. Fresh evidence/proxy-local-integration01 separately passes11each against selected879 with303and865predecessors.

**Refutation attempted:** No monkeypatch of old schema; oldsource constructs its ownrealStorage. Current fresh303 execution is not relabeled725.

**Notes:** Hostupgrade fixtures separately backed by installed14 preservation22.

### AC-I451-L30

> The815 upstream Linux checks pass with the newly compiled libchdr607694c library and no native skips; exact source/helper hashes and actual terminal/cleanup receipts are retained.

**Source:** #451, inputs/issues/451.md:30
**Checked:** 2026-10-06T15:55:48.391748+00:00
**Verdict:** PASS ✓

**Evidence:** host02/patched.log actual815Linux tests/12.751s/OK, no skip line; run.sh compiles coupledlibchdr607694c native helper before setting explicit RAOFFLINEPROXY_RCHASH_LIB; input/native-library hashes and completion bind actual source/build/result. Frozen14 native-result18/0skip plus4legacyCHD/canary/malformed controls exercise installedlibSHA6c484a29.

**Refutation attempted:** Distinguished host815original andlater818afterconsenttests; native capability cannot pass by skipping. Parentcoupled input is verified independently of recipe text.

**Notes:** Exact original host02andcurrentinstalled14 receipts remain separate.

### AC-I457-L16

> A regression fails on unchanged upstream at uptime0/5 and passes with the correction, including immediate consent changes and declined/unanswered controls; source/output hashes retained.

**Source:** #457, inputs/issues/457.md:16
**Checked:** 2026-10-06T15:55:48.391763+00:00
**Verdict:** PASS ✓

**Evidence:** Original early-consent-before.json uptime0/5grantedcounter0versusexpected1,31scontrol1. early-before.log has3assertionfailures/8methods; fixed8pass. Patch019 sentinelNone forcesinitial/invalidated read while retaining30s post-observation cache. Fresh evidence/proxy-local-integration01/consent.log executes exact selected879ConsentTests8/0fail.

**Refutation attempted:** Grant/decline/regrant and unanswered controls tested; no change to storedformat or oldmissedcounter recovery claimed.

**Notes:** SourceSHA recorded for fresh unprivileged run; installedproof below.

### AC-I457-L17

> All selected upstream Linux tests and relevant fork integration tests pass with the narrow patch; package lint and schema guard pass.

**Source:** #457, inputs/issues/457.md:17
**Checked:** 2026-10-06T15:55:48.391779+00:00
**Verdict:** PASS ✓

**Evidence:** b09host818/no skip plus11each303/865 integration passed; independent evidence/proxy-source-equality.json compares219nonbackup/nonbytecode Linux files and53native files to frozen879 with0added/removed/changed. Fresh879integration11each andConsentTests8pass. Fresh12actualrecipe lints and hostchecks01schema pass.

**Refutation attempted:** Original222Linux equality count included generated .orig backups; current explicitscope excludes .orig/.rej/.pyc and verifiesall219consumed/testfiles. No claim that full818 were freshly reexecuted under879.

**Notes:** Exact consumed source equivalence supports the retained full suite, with fresh currentintegration/consent checks.

### AC-I457-L18

> A fresh candidate contains the correction and the installed positive/negative/restart HTTP proof passes; loaded module hashes and actual completion/cleanup receipts retained.

**Source:** #457, inputs/issues/457.md:18
**Checked:** 2026-10-06T15:55:48.391793+00:00
**Verdict:** PASS ✓

**Evidence:** Frozen14 consent02summary30cases across15consentvalues/restarts, actualloopbackcollector, actualfirstgrantcounter7→8at16.705s; loaded8moduleSHA preserved. Invalid/nonbool/unanswered/declined/oldgrant produce0requests; positive usage1/logs2/both3 thenreplay0. Completion actual/four0and5PIDs absent01:01:30.

**Refutation attempted:** Positivecounter catches earlycachebug; negative-only silentcollector would be vacuous. Current installed pyc identities checked; earlier consent01failedreceipt retained.

**Notes:** No scheduler/UI/externalcollector claim; this is the specified installed reporting-function HTTPproof.

### AC-I457-L19

> A focused upstream patch plus reproduction/test instructions is prepared under #168; no upstream submission is implied by preparation.

**Source:** #457, inputs/issues/457.md:19
**Checked:** 2026-10-06T15:55:48.391810+00:00
**Verdict:** PASS ✓

**Evidence:** docs/upstream/raofflineproxy/early-consent/{README.md,fix.patch} namesbaseb09, exactapply/testinstructions and8test before/fixedresults. Fresh bytecomparison showsdraft==packaged019. Contributionmaprow019ownedby168 and explicitunsubmittedstatus.

**Refutation attempted:** Patchincludesits3regressionmethods and format-preservation rationale; combinedforkPASSis not the only suppliedreproduction.

**Notes:** Preparation does not imply submission/acceptance or outboundpermission.

### AC-I361-L122

> Existing cached sign-in, cache rows, ROM/image paths, pending base/subset awards and restart/reconnection survive an upgrade fixture; declined/unanswered telemetry never sends.

**Source:** #361, inputs/issues/361.md:122
**Checked:** 2026-10-06T15:55:48.391825+00:00
**Verdict:** PASS ✓

**Evidence:** Frozen14 proxy14actual22preservation andsubset11actual35HTTPassertions preservecachedsign-in,fullrows,ROMpaths,legacyimagebytes andpendingbase/subsetthrough2reopens/reconnection/refusedretry. Consent02actual30cases andloadedmodulehashes enforce unanswered/declinednoHTTP.

**Refutation attempted:** Failure503retains onlysubsetpending, acceptedbaseisnotresent; positiveconsentcontrolproducesrequests while negativecontrolsdo not.

**Notes:** Owned syntheticfixtures; actualaccountRA33separatelyprovidesproviderconfirmation.

### AC-I414-L20

> Correct the compatibility note after verifying the exact pinned storage schema and caller assumptions; retain the equality and current-Storage test evidence.

**Source:** #414, inputs/issues/414.md:20
**Checked:** 2026-10-06T16:01:19.176941+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-04-proxy-schema-note/source-proof.json retains identical old/new storage SHA15e17157 and cache_keys19c79b3c, noncomment-script equality and the original1688PASS/1schemaFAIL. Every direct SQL query was checked: ctl 581,613,680–683,768,1010/1021,1478/1493 consumes existing api_cache/pending_awards columns; current Storage DDL105–167 and cache-key builders preserve them. Streaming whole_games fallback uses current iter_cache_by_prefix. Source/schema equality is retained in docs/qa-logs/2026-10-05-proxy-schema-3036478/schema-review.json. Fresh host-checks01 full script suite1719/0 includes actual-current-Storage writer/ctl reader test; frozen14 installed suite supplies target execution.

**Refutation attempted:** Compared both schema and callers, not merely matching the comment hash; additive cached_game_meta does not replace consumed fields.

**Notes:** Original414 fix and later452/879 comment refresh remain distinct historical events.

### AC-I414-L21

> An early package/preflight check fails for stale, missing or malformed recorded pins, passes the corrected package, and does not bypass the existing runtime/schema assertion.

**Source:** #414, inputs/issues/414.md:21
**Checked:** 2026-10-06T16:01:19.177003+00:00
**Verdict:** PASS ✓

**Evidence:** tools/rc-preflight132–165 validates exactly one full recipe/header pin before /etc/profile. Fresh evidence/proxy-schema-controls-01:15PASS/0FAIL rc0; missing/short/duplicate/stale/below-header controls reject, absent files return2, matching succeeds, ordinary dispatcher stale returns1.

**Refutation attempted:** Historical control used ec60 literally; adapted only its current-pin variable/root so negatives actually corrupt today’s879 note. Runtime Storage writer/reader assertion remains independently present/executed.

**Notes:** The guard proves review-note agreement, not schema compatibility by itself.

### AC-I414-L22

> A replacement artifact includes the corrected script and passes the affected script suite; preserve the original failed candidate and its evidence.

**Source:** #414, inputs/issues/414.md:22
**Checked:** 2026-10-06T16:01:19.177038+00:00
**Verdict:** PASS ✓

**Evidence:** Original b137d8c373 scripts1688/1 retained with SHA802533b8 in source-proof.json; replacement14 frozen installed script suite1719/0 and custody-verified ctl contains879-reviewed note. Historical corrected recipe changes no executable lines.

**Refutation attempted:** Did not erase original failure or call a host-only guard a rebuilt image. Exact14 source/payload and installed suite are separately retained.

**Notes:** Later proxy advances supersede the original pin with reviewed notes.

### AC-I452-L28

> Retain the actual old-note rc1 and source/schema byte comparison; review every direct SQL query against the selected schema.

**Source:** #452, inputs/issues/452.md:28
**Checked:** 2026-10-06T16:01:19.177059+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-05-proxy-schema-3036478/before.log and frozen11-negative.log retain old725 note/current303 rc1; schema-review.json records actual725/303 storage62a545a1 and cachekeys19c79b3c equality. Every direct SQL query was checked: ctl 581,613,680–683,768,1010/1021,1478/1493 consumes existing api_cache/pending_awards columns; current Storage DDL105–167 and cache-key builders preserve them. Streaming whole_games fallback uses current iter_cache_by_prefix. Source/schema equality is retained in docs/qa-logs/2026-10-05-proxy-schema-3036478/schema-review.json. Fresh host-checks01 full script suite1719/0 includes actual-current-Storage writer/ctl reader test; frozen14 installed suite supplies target execution.

**Refutation attempted:** Searched all execute/SELECT occurrences, including duplicated head parser and streaming fallback; read fields/key owner scoping, not only declaration list.

**Notes:** Native/API interface refresh elsewhere is independently audited.

### AC-I452-L29

> Only the reviewed pin comment changes; package lint and existing offline schema preflight pass, while the original frozen input still fails.

**Source:** #452, inputs/issues/452.md:29
**Checked:** 2026-10-06T16:01:19.177079+00:00
**Verdict:** PASS ✓

**Evidence:** git show fc689bdfc2709a2855424460fb70681622b959ce changes only two comment lines725→303 and review citation426→452. docs/qa-logs/2026-10-05-proxy-schema-3036478/after.log and frozen11-negative.log retain positive/negative guard; fresh local-pkgcheck-01 raofflineproxy matched actual recipe rc0, fresh15-control guard passes.

**Refutation attempted:** Compared actual commit diff; matching comment is not used as runtime compatibility evidence. Frozen11 negative retained.

**Notes:** No runtime source modified in this correction.

### AC-I452-L30

> The corrected source is published and a new sealed candidate input set passes the guard before any build or cache adoption.

**Source:** #452, inputs/issues/452.md:30
**Checked:** 2026-10-06T16:01:19.177095+00:00
**Verdict:** PASS ✓

**Evidence:** replacement12/preparation/pre-freeze-schema.log names primary next55d8ee8f75 and PASS303 review before build; freeze-receipt.json seals6549product/180symlinks/202QA with SHA bfdcf9b2655157b7e4d3a59f1c6fa803f68989b2cfb8b460eb0f2a666ee98192. Historical12 build/adoption receipts retain source55d8, custody and terminal all-zero channels; source publication is ancestor of frozen14.

**Refutation attempted:** Unbuilt11 copy/adoption is distinct from compilation; no build claimed on the failed11 freeze. Actual pre-freeze command output names corrected source, not only README.

**Notes:** Current package inputs are subsequently frozen879; this criterion concerns the original452 sequence.

### AC-I386-L26

> Each listed package has a verified current source and consumer-compatibility result; the recipes are refreshed, or an actual parent-coupled/version constraint is documented with evidence and a recorded disposition. No unexplained old-pin exception.

**Source:** #386, inputs/issues/386.md:26
**Checked:** 2026-10-06T16:03:18.967184+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-03-dependencies archives.json binds five exact archives; glslang-known-good.json selects ef96ed7/4965431 and both current recipes repeat that parent coupling. Actual compat-build.log links native SPIRV/glslang/shaderc and compiles752-byte Vulkan vertex shader; cbindgen-build.log builds/reports0.29.4 on project Rust1.94.1. translator-header-compat.json shows candidate13ahead/0behind declared translator revision; tllist real tags resolve1.1.0. Frozen14 package-freshness lists glslang16.6/current,cbindgen0.29.4/current,tllist1.1/current and explicit coupledheaders exception.

**Refutation attempted:** Did not treat shaderc’s older tested DEPS baseline as an upper-version constraint; tested its actual compile/link. Headers remain parent-coupled, not falsely advertised newest standalone.

**Notes:** Source-current evidence is timestamped Oct3/cut Oct6 00:42. Native host probes do not claim hardware acceptance; actual target consumers/build receipts below.

### AC-I386-L27

> tllist's upstream version is resolved; any freshness resolver fix has a retained failing/passing control. UNKNOWN is not CURRENT.

**Source:** #386, inputs/issues/386.md:27
**Checked:** 2026-10-06T16:03:18.967249+00:00
**Verdict:** PASS ✓

**Evidence:** tools/fork-package-freshness58–64/147 adds Codeberg tags resolver. Retained codeberg-before.log fails stable/new-stable controls, after passesall6. Fresh evidence/dependency-controls-01 rc0: six controls pass incl prerelease exclusion,newstableBEHIND,empty/malformed/requesterror UNKNOWN even withvalidbody. tllist-live.log actual1.1.0CURRENT and frozen14 freshness repeatsit.

**Refutation attempted:** Fixture curl is a local executable asserting exact URL; fresh test proves classification without claiming a live lookup. Transport failure cannot become CURRENT.

**Notes:** Fresh live network check remains approval-service blocked; does not invalidate retained cut-time lookup.

### AC-I386-L28

> tools/pkgcheck passes for changed recipes; relevant consumers build and their VM acceptance receipts identify the exact candidate inputs.

**Source:** #386, inputs/issues/386.md:28
**Checked:** 2026-10-06T16:03:18.967277+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh local-pkgcheck01 matched glslang,spirv-tools,spirv-headers,shaderc,cbindgen,tllist rc0. Original cold bundle22533e35 build.log99343/170387/704632/801533 explicitly builds hostglslang,targettllist,SPIRV-Tools,targetglslang. Frozen14 inventory10 source-inventory.json binds exact archives and actual target/host stamps plus Mesa/Vulkan/WebKit consumers; accepted642-taskimage/default15suite/virgl-Pixman installed qualification binds source7afa9 and manifest70cb0448.

**Refutation attempted:** Shaderc/cbindgen host compatibility is retained separately; not invented as installed GENERIC_X64 components. Actual cold compile lines supplement later cached stamps. No hardware acceptance inferred.

**Notes:** #361/#362 runtime gates are independently graded; unchanged graphics dependency inputs carry their original cold compilation lineage.

### AC-I386-L29

> tools/fork-package-freshness exits 0 on the frozen candidate inputs and the source manifest names the verified archives/hashes. #361/#362 qualification remains separately required.

**Source:** #386, inputs/issues/386.md:29
**Checked:** 2026-10-06T16:03:18.967298+00:00
**Verdict:** PASS ✓

**Evidence:** Q14/preparation/freshness-completion.json real00:42:18 UTC records allfour0 and fourPIDabsence for frozen14run004114; package-freshness.log has explained PINNED and no BEHIND/UNKNOWN. Q14 inventory10 errors0/568roots records exact checked archives and stamps; input manifest70cb0448 binds1608recipes.

**Refutation attempted:** Earlier freshness04 is retained failed on new879; no success borrowed from outdated13freeze. Fullinventorysuccess is distinct from separate proxy/browseracceptance.

**Notes:** This is the frozen-cut freshness criterion, not a claim no upstream commit has arrived since.

### AC-I361-L120

> Every patch has a source-backed retained/rebased/superseded disposition and the final series applies cleanly.

**Source:** #361, inputs/issues/361.md:120
**Checked:** 2026-10-06T16:03:18.967323+00:00
**Verdict:** PASS ✓

**Evidence:** docs/rasteratops/raofflineproxy-refresh.md enumerates001–019 with16 retained and006/014/017retired. Currentstorage64–70/815–855 protects permanent prefixes in bothSQLite/JSON; image_cache246–315 reuses thread/host connections withdrop/retry/redirectfallback; subsetmapping source independently verifiedI384. Selected879 patch-application.log retains all16 zero-fuzzapplications, fresh proxy-source-equality219Linux/53native zerochanged confirms qualifiedb09consumedbytes.

**Refutation attempted:** Connection reuse does not substitute for009atomicpublication; retired017 was checked against nested set IDs, not top-levelonly. Distinct019initialconsentfix has independent old/new regression.

**Notes:** Offsets are not fuzz; application and behavior evidence remain distinct.

### AC-I361-L125

> Remaining general-purpose fixes are reconciled with #168 for focused upstream contributions and regression tests. Ten tested drafts and interface-dependent dispositions are published in the linked contribution map; submission/acceptance remain separate.

**Source:** #361, inputs/issues/361.md:125
**Checked:** 2026-10-06T16:03:18.967340+00:00
**Verdict:** PASS ✓

**Evidence:** docs/upstream/raofflineproxy/contribution-map.md reconciles all16 retained patches,3retired and older168ideas; ten standalone drafts have explicit unsubmittedstatus. 2026-10-06-upstream-drafts raw before/fixed logs independently show7drafts:40targeted/169related executions,zero skips; originals fail real400/404/429 response,wrongaccount,warningfilter,refreshstops,consent,PNG/DNS assertions. Earlier image-publication/identity recheckreceipt and before/fixedlogs bindb09;019consent8-test evidence reviewedseparately.

**Refutation attempted:** Pristine production hash controls distinguish signature-only or sandbox failures; six interface-dependent contributions remain expressly API/policy discussions. No combinedseries test was silently sold as eachstandalonedraft.

**Notes:** No PR submitted/accepted; owner approval remains required for outward168contribution.

### AC-I332-L22

> A run of the Nova's `ledcontrol` on the host with `LED_PATH` pointed at a fixture: `brightness max|mid|min` writes three distinct `brightness` values to all eight LEDs (today it writes nothing); `battery`, `rgb` and `off` each leave the fixture in a stated state; the transcript filed here.

**Source:** #332, inputs/issues/332.md:22
**Checked:** 2026-10-06T16:04:49.889329+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh evidence/ui-lifecycle-controls-01/nova-led.stdout: actualscripts14PASS0FAIL, each8brightnessmax255/mid128/min32;RGBwhite,explicitcustom,off,7batterycolors and10blinksteps. Original2026-10-03-led/before.log6PASS8batteryFAIL retained; correctedafter14PASS.

**Refutation attempted:** Tool adaptation changes only profile/path/service/sleep boundaries; all branch/brightness/RGB code executes. Fixed fixture starts all8values0 and asserts exact perLED outputs.

**Notes:** Hostfixture is explicitly requested by this criterion; no physical perceivedbrightness claimed.

### AC-I332-L23

> Choosing the value already selected in LED COLOR or LED BRIGHTNESS applies it (the row's callback runs on a press, not only on a change), shown by the fixture's files changing on a walk of the page on a guest with the quirk's script and a fake `LED_PATH`, or by a frame of the row plus the device's sysfs read after the press.

**Source:** #332, inputs/issues/332.md:23
**Checked:** 2026-10-06T16:04:49.889404+00:00
**Verdict:** PASS ✓

**Evidence:** ActualOct3isolatedVM ui-reselection brightness-before0×8→after128×8, allwhiteRGBunchanged, actualcalls rgb then brightnessmid, savedsettingsstillrgb/mid. Viewed01-mid-already-selected and02-mid-reselected frames; result.json9observedchecks and ui-source-match.json bind exact menu/popup code. E GuiMenu2140–2181 callback reapplies selectedvalue.

**Refutation attempted:** Zeroedfixture supplies negative state even thoughMIDalreadyselected; aftervalues distinguishcallbackfromunchangedsavedpreference. HistoricalfullscreenROCKNIXframe is not mislabeled branded14.

**Notes:** ExactunchangedLEDblock proof travels with sourcecontinuity; physical Nova illumination remains laterfact.

### AC-I424-L18

> Retain exact installed negative evidence and identify the source/environment boundary.

**Source:** #424, inputs/issues/424.md:18
**Checked:** 2026-10-06T16:04:49.889443+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-04-es-identity-export/installed-negative.txt hasos-releasepixelelated butprocessPID2470noOS_NAME andoldexportSHA6fbbd886. Directlyviewedactualmain-menuROCKNIX andwrongupdateNOUPDATEAVAILABLE. ProfileomitsOS_NAME; ApiSystem applicationnamefallbackROCKNIX explainsboth.

**Refutation attempted:** Correctfilealone was insufficient; readactualchildenvironment andtwoactualconsumerframes.

**Notes:** Oldfailed1e6a preserved, nohotpatchofthatimage.

### AC-I424-L19

> Add a focused regression that fails against the old launch/profile and proves OS_NAME reaches the actual child without unrelated identity/config changes.

**Source:** #424, inputs/issues/424.md:19
**Checked:** 2026-10-06T16:04:49.889466+00:00
**Verdict:** PASS ✓

**Evidence:** tools/rasteratops-identity-check116–130 sourcesactualexportprofile undercleanenvironment thenexecs/bin/shchild; freshui-lifecycle-controls01 oldexportunset/0.0.1/community, newexportpixelelated/0.0.1/community. Allotherprofilevaluesidentical. Historicalwholeidentitybefore1failure/after0retained.

**Refutation attempted:** Newchildreceivesexportedvalue ratherthanparent-onlyshellvariable; oldprofilenegativeactually executedfresh.

**Notes:** Focusedcurrentchildcontrol succeeds; nofullhostnamespace identityrunclaimed.

### AC-I424-L20

> A replacement candidate's clean and retained-storage ES process receives pixelelated; actual menu and manual-update frames show the intended behavior.

**Source:** #424, inputs/issues/424.md:20
**Checked:** 2026-10-06T16:04:49.889484+00:00
**Verdict:** PASS ✓

**Evidence:** Q14qa18 installedpayload-initial-clean PID1639 andpayload-upgrade PID1484 actual/usr/bin/emulationstation environmentOS_NAMEpixelelated withexportSHA3708af2b andbuild7afa9. Directlyviewedboth01mainmenus displaypixelelated0.0.1 andboth05manualdialogs pointtopixelelated/distribution/releases.

**Refutation attempted:** Verifiedrunningconsumerplusactualframes onclean/retainedstorage; notos-releasealone norhostsourceguard.

**Notes:** ActualRC2upgradequalification chain separatelyretained; noautomaticupdatesrequested.

### AC-I424-L21

> Reconcile the sweep/identity checks so a correct os-release file alone cannot close this consumer criterion; retain the superseded artifact's results honestly.

**Source:** #424, inputs/issues/424.md:21
**Checked:** 2026-10-06T16:04:49.889501+00:00
**Verdict:** PASS ✓

**Evidence:** Currentidentity-checkchildassertionfailsoldprofile andpassesnew; Q14check-payload reads/proc/<ES>/environ andinstalledprofilehash. Before/afterlogs,negativeoldframes andnewconsumerframesremain distinctartifacts.

**Refutation attempted:** Sourcecheckdoesnotreplaceinstalledpayload/frames; earlierpost-buildsuccessneverrewritesoldnegative.

**Notes:** Consumeridentitycontract is nowexplicitlytested atbothboundaries.

### AC-I436-L50

> Retained actual old-image reproduction binds the exception, process restart, missing capability and affected save callback.

**Source:** #436, inputs/issues/436.md:50
**Checked:** 2026-10-06T16:06:29.597518+00:00
**Verdict:** PASS ✓

**Evidence:** Replacement07 identity-diagnostic03: before/information PID1405 restart0; back-two journal line99 throws vector::_M_range_check from empty selection; delayed/reopen PID2925 restart1. GPU controls old.log reproduces absent selection exception. GuiMenu2321–2350 formerly saved getSelected even when capability list empty.

**Refutation attempted:** This is the actual old-image process transition and exception, not a navigation screenshot interpreted as a crash.

**Notes:** #422 navigation timing remains a different scope.

### AC-I436-L51

> The corrected UI safely handles absent GPU governor capability while preserving selection/save behavior when capability exists; old failing and new passing controls are retained.

**Source:** #436, inputs/issues/436.md:51
**Checked:** 2026-10-06T16:06:29.597584+00:00
**Verdict:** PASS ✓

**Evidence:** Current GuiMenu GPU save callback checks hasSelection before any config write/command. Fresh source-extracted C++ control in ui-lifecycle-controls01 passes six cases: absent, retained absent, unselected, unchanged, changed, fallback. Original old.log fails absent case.

**Refutation attempted:** Test compiles release NDEBUG semantics but contract assertions remain active; present/unchanged selection still invokes its command, changed selection saves only selected value.

**Notes:** Source controls complement installed evidence below.

### AC-I436-L52

> Fresh and retained-state upgraded candidate guests return from System Settings without an ES process restart or exception, with actual menu frames and journal proof.

**Source:** #436, inputs/issues/436.md:52
**Checked:** 2026-10-06T16:06:29.597613+00:00
**Verdict:** PASS ✓

**Evidence:** Copied exact QA18 owner lifecycle files into evidence/ui-lifecycle-controls01/installed-{initial-clean,upgrade,upgrade-software}. Actual PID/start ticks stay1639/509,1484/354,1489/353 across System Settings walks; each result passes and retained journals contain no range exception/termination. Exact14 identity frames reviewed separately. Original08 clean/upgrade lifecycle passes are also retained.

**Refutation attempted:** Compared start ticks as well as PID, and actual logs/frames; no restarted process with a reused name is accepted.

**Notes:** These are completed Oct6 QA18 observations, not a newly launched VM.

### AC-I436-L53

> Relevant syntax/package checks, candidate qualification, milestone order and checkpoint reflect the repair; #422 retains its separate navigation scope.

**Source:** #436, inputs/issues/436.md:53
**Checked:** 2026-10-06T16:06:29.597635+00:00
**Verdict:** PASS ✓

**Evidence:** Replacement07 gpu-governor-controls syntax.log explicitly checks GuiMenu.cpp PASS with corresponding rc0; source pin is inherited by current frozen ESf6f0c134. Current package lint, actual14 build/defaults/upgrade and independent lifecycle checks pass. Retained tracker-readback and published checkpoint preserve P4 before device work, with #422 separately named.

**Refutation attempted:** Source syntax alone was not used to close runtime criterion; exact clean/retained evidence above is required.

**Notes:** No RC assertion; later independent audit remains underway.

### AC-I454-L12

> Shared stop verifies the QEMU/owned-disk identity, waits for the same process to exit, fails boundedly on timeout, and retains the pidfile on failure. Deterministic tests retain delayed exit, wrong-process refusal and timeout controls.

**Source:** #454, inputs/issues/454.md:12
**Checked:** 2026-10-06T16:06:29.597653+00:00
**Verdict:** PASS ✓

**Evidence:** tools/vm-stop13–58 validates QEMU executable and exact -drive argument, captures start ticks, opens pidfd, rechecks identity, signals same handle and polls boundedly; timeout retains pidfile. Q12 harness-controls/stop-final/controls.log has seven actual-host controls including self-removed pidfile and immediate port reuse.

**Refutation attempted:** Fresh local rerun retained in ui-lifecycle-controls01 failed before controls because sandbox denied socket creation; not counted as PASS or product failure. Original real-host seven-control receipt plus QA17 immediate restart is the executable evidence.

**Notes:** A new host rerun remains approval-auth blocked; no bypass attempted.

### AC-I454-L13

> Actual upgraded QA15 disk is preserved and continued in a fresh owner; virgl and automatic software/Pixman checks and identity frames pass, with immediate stop/restart and actual terminal cleanup evidence.

**Source:** #454, inputs/issues/454.md:13
**Checked:** 2026-10-06T16:06:29.597672+00:00
**Verdict:** PASS ✓

**Evidence:** Q12 QA17 upgraded-disk-custody.json names actual QA15 diskSHA3c2d5dc1, independent inode, guest-byte equality and standalone16GiB converted copy. Renderer software/virgl and ten installed identity frames retained; completion23:40:46 records four0 and all observed process absence, supplement closes5909/10022/9010 and backend.

**Refutation attempted:** Different qcow container hashes do not mean different guest bytes; qemu-img comparison and no backing dependency establish independent copy. No arbitrary sleep substitutes for vm-stop.

**Notes:** QA15 original disk remains unchanged; follow-up scope is explicit.

### AC-I454-L14

> QA15's original failure,15default/26upgrade results, source/input identities and follow-up scope are retained; downstream unstarted owners bind the completed evidence chain explicitly.

**Source:** #454, inputs/issues/454.md:14
**Checked:** 2026-10-06T16:06:29.597689+00:00
**Verdict:** PASS ✓

**Evidence:** Q12 QA15 completion allfour1 with15 reported defaults/26 actual RC2 assertions retained; QA16 allfour1 self-removed-pidfile failure also retained. QA17 seals exact12 source/input and scoped continuation, and current14 full QA18 reruns the corrected shared harness. Historical downstream proxy13/subset10 retain their plan/candidate bindings.

**Refutation attempted:** Neither failed aggregate is rewritten green; scoped follow-up is not described as fresh full15 defaults.

**Notes:** Later14 full qualification is distinct from12 continuation.

### AC-I455-L12

> Root cause and first available historical evidence are recorded from actual fixture/system state; inherited coverage is not represented as a new branding regression.

**Source:** #455, inputs/issues/455.md:12
**Checked:** 2026-10-06T16:06:29.597706+00:00
**Verdict:** PASS ✓

**Evidence:** #455 source snapshot and Q12 QA17 fixture/readback record match-dialog removes GB ROMs, causing requested GB to fall back to FBNeo in QA15/QA14 and earlier accepted baseline. vm-qa ensure_manager_fixture now precedes each manager; scoped walk log records reseeding. Actual selected-system receipt and frame establish corrected outcome.

**Refutation attempted:** An identical wrong baseline could pass image comparison; system/game evidence is separately required. This is inherited harness coverage, not proof of a pixelelated regression.

**Notes:** Prior wrong frames and first comparison remain retained.

### AC-I455-L13

> Harness fails for a wrong/missing requested system before accepting the walkthrough, with a retained negative control.

**Source:** #455, inputs/issues/455.md:13
**Checked:** 2026-10-06T16:06:29.597722+00:00
**Verdict:** PASS ✓

**Evidence:** tools/vm-qa449–462 records real ES system-selected event, queries visible systems and invokes vm-manager-system-check before walk acceptance. Fresh manager-controls.json has six expected results: valid passes; wrong,missing,duplicate,hidden,empty refuse. Q12 original five controls and three CLI refusals retained.

**Refutation attempted:** Checks actual selection, not StartupSystem preference or screenshot filename. Missing games cannot silently fall back and still pass.

**Notes:** Host parser fixture is supplemented by actual installed-system output below.

### AC-I455-L14

> Game Boy, NES and FBNeo each reach the intended manager on the exact candidate; actual frames and relevant aspect/orientation evidence retained without silently accepting a new baseline.

**Source:** #455, inputs/issues/455.md:14
**Checked:** 2026-10-06T16:06:29.597738+00:00
**Verdict:** PASS ✓

**Evidence:** Exact14 QA18 defaults/walks manager-{gb,nes,fbn}-system-check logs pass actual gb/nes/fbn. Directly viewed all three04-manager frames: GB/Ninoid landscape160×144 ratio; NES/Bobl and FBNeo/Ms.Pac-Man portrait with round rings and top green orientation mark; consistent start arrow. QA17 comparison-reviewed retains19screens/14claims/0unclaimed/0missing with unchanged baseline/masks.

**Refutation attempted:** Game labels and geometry were read from actual pixels, not per-walk names; two initial unclaimed carousel regions remain preserved with bounded fixture-composition explanations.

**Notes:** No silent new baseline or masked content error accepted.

### AC-I310-L21

> The mapping is named: a diff of the interface's `/proc/<pid>/maps` across one launch/exit cycle on the VM shows the 10 MiB region and the code that makes it (the region's flags and backing in the issue).

**Source:** #310, inputs/issues/310.md:21
**Checked:** 2026-10-06T16:07:51.468273+00:00
**Verdict:** PASS ✓

**Evidence:** Oct3 software-3/003.maps→004.maps adds10MiB total anonymous rwxp; adjacent mappings merge so the newly printed20MiB region replaces an existing10MiB mapping. Fresh evidence/memory-recalculation.json retains both totals. jit-trace.log mmap length10485760/protection7/flags34 and matching jit-symbols.txt resolve rtasm_exec_malloc→SSE vertex translation; unload-trace records driver unloading.

**Refutation attempted:** Did not mistake merged20MiB map size for per-cycle growth. Virgl control remains flat; allocator reload before/after50 cycles retains512000KiB versus0.

**Notes:** Mesa001 pairs executable arena/bookkeeping teardown and unwinds mmap/calloc/atexit failures.

### AC-I310-L22

> With the fix, `E1-pl069-control.sh`'s 10 cycles on the VM leave VmSize within one cycle's noise (under 1 MB of growth over 10) and VmRSS within 2 MB; equivalent launch/exit CSV and identity receipts filed under `docs/qa-logs/2026-10-03-launch-memory/`.

**Source:** #310, inputs/issues/310.md:22
**Checked:** 2026-10-06T16:07:51.468337+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh independent CSV recomputation of Q10 memory12: five warmups then10 software cycles, onePID2010, VmSize-448KiB/RSS+684KiB; virgl onePID2137,0/+224KiB. Both within original1024/2048 limits. Installed identities and renderer receipts bind frozen10; unchanged ES/Mesa/SDL bytes carry to14.

**Refutation attempted:** No threshold changed; earlier Mesa-only and one-trim failures remain retained. Read source glibc-only trims, udev enumeration release/copy-before-free and packaged SDL/Mesa cleanup.

**Notes:** This is retained completed VM qualification with fresh arithmetic, not a new14 endurance execution.

### AC-I310-L23

> `E1-pl069.sh`'s 50 cycles with the exit sync on show the same flat VmSize, so PL-069's fix and this one are shown apart (the csv filed).

**Source:** #310, inputs/issues/310.md:23
**Checked:** 2026-10-06T16:07:51.468364+00:00
**Verdict:** PASS ✓

**Evidence:** Q10 software-sync50 cycles.csv has56rows including initial state, five warmups and50 measured cycles, samePID7226; fresh computation0KiB virtual/+444KiB resident. All55 exit-sync files have distinct timestamps and status0 completed. Original failed intermediate RSS endurance runs remain retained.

**Refutation attempted:** Counted and parsed every stamp rather than accepting file existence; stable memory and completed sync are simultaneous in same run.

**Notes:** Even the stricter2048KiB RSS endurance condition passes; criterion originally required flat VmSize.

### AC-I310-L24

> Already written: nothing -- the growth lives in the running process and a restart clears it.

**Source:** #310, inputs/issues/310.md:24
**Checked:** 2026-10-06T16:07:51.468385+00:00
**Verdict:** PASS ✓

**Evidence:** Defect consists of anonymous process mappings, lost DSO pointers, udev/SDL allocations and retained freed heap. Source fixes only process lifecycle resources; actual restart/newprocess measurements reset these. No storage/cloud migration is added by Mesa/SDL patches or ES trims.

**Refutation attempted:** Inspected all three packaged patches and relevant ES ownership/trim sites; no serialization or persistent format changes.

**Notes:** Historical already-written statement accurately limits impact to running-process memory.

### AC-I433-L73

> Retain original failed640/passed1280 matcher outputs, selected actual frames, capture hashes, all runner results and verified cleanup without conflating runner success with visual acceptance.

**Source:** #433, inputs/issues/433.md:73
**Checked:** 2026-10-06T16:10:48.114182+00:00
**Verdict:** PASS ✓

**Evidence:** Original57cbc UI07 splash640 result0.9610208817<0.995 and1280 result0.996047282 retain frames/hashes and allzero command completion. Directly viewed failed640 actual-best: console overlay removes glyph pixels. Separate visual result remains failed despite successful runner and verified cleanup.

**Refutation attempted:** No threshold reduction or retitling original success; all924 differing pixels and original negative controls remain recorded.

**Notes:** Command completion and visual acceptance explicitly differ.

### AC-I433-L74

> A bounded diagnostic distinguishes the failure cause using captured framebuffer/console facts and controls; no blind repeat-until-pass or threshold change.

**Source:** #433, inputs/issues/433.md:74
**Checked:** 2026-10-06T16:10:48.114244+00:00
**Verdict:** PASS ✓

**Evidence:** Boot diagnostic01 actual original0.85159249; exact splash drawn in text mode1.0 then line erasure0.981691626; graphics mode console write stays1.0. Diagnostic03 actual quiet640/1280 both1.0 after asserting Syslinux/GRUB consumption; failed01/02 setup attempts retained. Fresh renderer-controls01 executes16 real init-predicate observations including original policy failure and debug/other-device controls.

**Refutation attempted:** The first quiet attempt edited inactive GRUB and is retained failed; corrected active boot-path assertion precedes quiet comparison. No attribution to one particular kernel message is invented.

**Notes:** Controlled console redraw explains mechanism; diagnostic COW is not candidate qualification.

### AC-I433-L75

> Any necessary product/harness fix has source-level evidence plus exact-candidate clean/retained-state boot proof at both sizes with unchanged matcher/negative controls. If product inputs change, freeze a new candidate and reconcile required qualification.

**Source:** #433, inputs/issues/433.md:75
**Checked:** 2026-10-06T16:10:48.114272+00:00
**Verdict:** PASS ✓

**Evidence:** GENERIC_X64 options74–76 adds quiet while retaining serial/tty0. BusyBox init1274–1279 applies same suppression to old no-quiet configs unless debugging. Q10 boot05 allfour clean/actualRC2-upgraded640/1280 result1.0 at0.995 with12 rejected controls; directly viewed allfour exact best frames. Earlier08/09 same boot proof and newer14 unchanged boot inputs retained.

**Refutation attempted:** Upgraded cmdlines retain old no-quiet state, so test exercises fallback rather than silently rewriting owner config. Serial/journal access preserved; new product freeze followed source change.

**Notes:** Separate renderer/sign-in qualification is not inferred from splash alone.

### AC-I433-L76

> Published evidence and the M7/#409/#422/#431 bodies identify the accepted replacement and safe downstream dependency binding before any successor predecessor proof advances.

**Source:** #433, inputs/issues/433.md:76
**Checked:** 2026-10-06T16:10:48.114292+00:00
**Verdict:** PASS ✓

**Evidence:** Retained #433 source snapshot identifies published cf511ce replacement09, source/manifest and predecessor06 dependence on boot03/UI10; #441 subsequent failed binding retained then boot04 verifies actual QA13 upgraded disk with full build/kernel/backing checks. Boot05 provenance names prior04 and actualQA14 upgraded backing for new10. Current milestone/checkpoint retains ordered P4 before device builds.

**Refutation attempted:** Replacement08 remaining owners remain unstarted; passes not transferred across changed images. Source custody and accepted successor paths corroborate tracker ordering.

**Notes:** Historical dependency corrections remain explicit; no successor is replayed.

### AC-I447-L70

> Original command success, failed local frame, five other reviewed frames, hashes and actual cleanup retained without relabelling.

**Source:** #447, inputs/issues/447.md:70
**Checked:** 2026-10-06T16:10:48.114318+00:00
**Verdict:** PASS ✓

**Evidence:** Q09 signin-ui08-unaccepted retains command17checks/allzero and original local frameSHAa977f54c; directly viewed partial old loading page/jagged blocks below redirect. Five other original frames and all hashes retained;09:47:31 cleanup identifies absent owner/guest and noQEMU.

**Refutation attempted:** A loaded page and rc0 do not establish painted correctness; original remains visually unaccepted.

**Notes:** Later09/10 stale-frame and12 observer failures also remain separate.

### AC-I447-L71

> New sealed capture path requires the existing visual tool's stable-screen result with a bound; unsteady/no-result cases cannot count as accepted captures.

**Source:** #447, inputs/issues/447.md:71
**Checked:** 2026-10-06T16:10:48.114335+00:00
**Verdict:** PASS ✓

**Evidence:** stable_panel.py requires rc0 plus exact settle:still output after2quiet seconds within30seconds. Actual zero-timeout receipt returns0 but moving-at-bound and passedfalse; source assertion requires rejection. Four stable page receipts retained in accepted14.

**Refutation attempted:** Stable-but-wrong page remains possible and is separately rejected by finishing pixel reference; stable flag alone cannot qualify intent.

**Notes:** Capture bound is fixed; no repeat-until-pass or forced resize.

### AC-I447-L72

> Fresh full sign-in proof passes actual redirect/UA/phone checks; six intended frames are semantically reviewed with stability receipts and actual result/cleanup agreement. Authenticated Dropbox trust remains separate.

**Source:** #447, inputs/issues/447.md:72
**Checked:** 2026-10-06T16:10:48.114350+00:00
**Verdict:** PASS ✓

**Evidence:** Q10 signin14/15/16 each40checks/fifteenframes with actual HTTP+navigator Mobile UA, redirect,390CSS-pixel phone metrics and installed hashes. Six intended14frames directly viewed across this review: complete local form, finishing message, public login, Checking/Connected phone and public OAuth login. Each owner four0 with actual process absence20:18/20:20/20:23.

**Refutation attempted:** No authenticated trust/Dropbox account claim; finished markup, actual painted page and process cleanup are separate predicates.

**Notes:** English presentation verified; French source omission separately failsI351-L62.

### AC-I447-L73

> M7 and checkpoint identify accepted successor and the remaining1GiB/account/audit gates.

**Source:** #447, inputs/issues/447.md:73
**Checked:** 2026-10-06T16:10:48.114366+00:00
**Verdict:** PASS ✓

**Evidence:** #447 retained issue records accepted source8708d8e, runtime13 scope and ordered freshfreeze10/clean-upgrade/1GiB/account/audit beforeH700. Current checkpoint identifies accepted frozen14 and later realRA33/localcloud318, with optionalDropbox#463 and independent audit still incomplete.

**Refutation attempted:** Account-backed proof never inferred from public sign-in or synthetic UI; optional Dropbox disposition is D-QA-058.

**Notes:** Tracker phase names and remaining gates remain explicit.

### AC-I447-L74

> Resolve the reproducible software-host stale/partial scanout on the declared software VM profile: fresh bounded native/host comparison and full sign-in semantic frames agree without forced resize/input, with actual old/partial/unsettled rejection, matching terminal results and cleanup. Canonical virgl success alone does not satisfy this criterion.

**Source:** #447, inputs/issues/447.md:74
**Checked:** 2026-10-06T16:10:48.114383+00:00
**Verdict:** PASS ✓

**Evidence:** Q10 signin14 actual0/5/15 render observations bind correct finishing documentSHA890973b0, QEMU/VNC identicalSHA68a39b52 and native raw-pixel comparison PASS at each offset. Fresh exact-pixel controls accept correct image and reject real old09 and partial08 frames. Earlier matched Pixman/GLES2 and actualROCKNIX RC2 controls retained.

**Refutation attempted:** No forced resize/input; GLES2 stale0/5 and recovered15 is retained, while Pixman has allnine correct samples. Claim is renderer/allocation-path isolation, not blame assigned to an unproved individual component.

**Notes:** Software profile receives direct proof, not substitution with successful virgl.

### AC-I447-L152

> Rebuilt GENERIC_X64 clean/RC2-upgraded guests select Pixman without virgl and retain accelerated virgl; actual GPU features, compositor environment/logs and installed file hashes prove selection.

**Source:** #447, inputs/issues/447.md:152
**Checked:** 2026-10-06T16:10:48.114400+00:00
**Verdict:** PASS ✓

**Evidence:** Current14 QA18 installed renderer records: clean/upgradevirgl negotiatedbit0=1, WLR_RENDERER unset and GLES2virgl; upgrade softwarebit0=0, WLR_RENDERERpixman. WrapperSHA15b13fa9/dropinSHAca1e6aaf/sharedswaySHA1b42a41b agree. Q10 cleansoftware boot05 and signin14, upgradedsoftware15 provide installed clean/retained selection with actual kernelfeatures/logs.

**Refutation attempted:** Render-node presence is not used as capability; actual selected virtio child negotiated features decide. No runtime override supplies the PASS.

**Notes:** Unchanged10→14 renderer bytes explicitly carry earlier clean software tests.

### AC-I447-L153

> Selector boundary controls preserve explicit/unknown/non-virtio/multi-GPU cases; shared handheld startup bytes remain unchanged.

**Source:** #447, inputs/issues/447.md:153
**Checked:** 2026-10-06T16:10:48.114415+00:00
**Verdict:** PASS ✓

**Evidence:** GENERIC_X64 wrapper validates exact single card and one virtio child, actual driver and binary>=64bit feature string; explicit renderer/render-device returns unchanged. Selector04 executes22 cases on each image BusyBox actual software/virgl guest; all boundaries pass, including multiple/unknown/nonvirtio/malformed and multidigit card. Shared sway hash1b42a41b unchanged.

**Refutation attempted:** Unknown capability fails to existing behavior; no broadened software override on handhelds. Wrapper is device overlay/service drop-in only.

**Notes:** Selection fixtures do not by themselves prove compositor output; installed rendered proof above does.

### AC-I447-L154

> Relevant ES, emulator launch/exit, visual and time-to-play checks pass on the rebuilt software and accelerated profiles; original failures remain preserved.

**Source:** #447, inputs/issues/447.md:154
**Checked:** 2026-10-06T16:10:48.114430+00:00
**Verdict:** PASS ✓

**Evidence:** Q10 memory12 both installed profiles pass10-cycle launch/exit and strict growth, plus software50sync. Exit/time-to-play logs retain firstpixels0.570/0.636s, backup1.324/1.673s, relaunch1.012/1.011s; exact boot/sign-in/identity visuals and QA14 defaults/actualRC2 upgrade retained. Later14 QA18 repeats full defaults and installedrenderer checks.

**Refutation attempted:** One-repeat timing smoke is not a distribution or proof of active-sync interruption; original failed owners remain failed. Current review independently recalculates CSV and all55 stamps.

**Notes:** Physical hardware performance remains a later named fact.

### AC-I327-L20

> A frame of the page at 640x480 from `tools/vm-walks/docs/retro-achievements.steps` on the first-release candidate image shows the explanation as short lines under the rows they explain (or one short block in the description size), each row visibly separated, the approved two paragraphs wrap within the panel without clipping (D-UI-119), and the frame filed under `docs/qa-frames/` beside the before frame.

**Source:** #327, inputs/issues/327.md:20
**Checked:** 2026-10-06T16:15:31.698370+00:00
**Verdict:** PASS ✓

**Evidence:** GuiRetroAchievementsSettings.cpp:53–68 uses description-font measured wrapping; :95–105 supplies the two paragraphs; :431–435 separates them. Directly inspected docs/qa-frames/2026-10-03/327/{before,en-640x480,fr-640x480}.png: the old all-caps block becomes two separated, readable paragraphs entirely inside the panel. Actual replacement10 ui-14 retains this unchanged surface.

**Refutation attempted:** Compared the old frame with both languages at the smallest panel; the longer French second paragraph still fits. Checked that conditional indexing text is measured using the longest version, preventing height underallocation.

**Notes:** This is explanation-page evidence, not offline award or reconnect evidence.

### AC-I327-L21

> `tools/es-menu-map-check` PASS, the French strings for every changed sentence in the same commit (D-UI-051), `tools/vocabulary-check` PASS.

**Source:** #327, inputs/issues/327.md:21
**Checked:** 2026-10-06T16:15:31.698467+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh audit host-checks01 menu-map and vocabulary commands passed; ES-checks02 vocabulary reports 164 strings / 0 wrong. ES commit c0cb9925eb41c313d011634c79adc6fd45acb099 changes both the page and locale/lang/fr/LC_MESSAGES/emulationstation2.po; direct diff contains all four replacement prose sentences plus scan outcome strings.

**Refutation attempted:** Read the actual French commit diff, rather than the commit message alone; each conditional and unconditional sentence has a translated msgstr. French 640 frame confirms runtime translation.

**Notes:** Current source retains the same prose. Exact executed check receipts are in evidence/host-checks-01 and evidence/es-checks-02.

### AC-I327-L22

> The site's `retro-achievements/offline-achievements.png` retaken from the walk after the change.

**Source:** #327, inputs/issues/327.md:22
**Checked:** 2026-10-06T16:15:31.698494+00:00
**Verdict:** PASS ✓

**Evidence:** Local website commit 4f6df54ca16121ff2cd0620407aea6434ee59147 changes docs/_inc/images/retro-achievements/offline-achievements.png. Fresh sha256sum of that file and the directly reviewed en-640x480.png both equal a40331aa212c7e9d4e3901b990bfac0bfe1013803a66346e763c92f72d943976.

**Refutation attempted:** Verified exact screenshot bytes instead of trusting the docs commit title; it is the new two-paragraph capture, not the retained before image.

**Notes:** Criterion asks for a retaken site asset. Public website publication remains a separate P5 gate with prior 403/404, not claimed here.

### AC-I357-L16

> No device on the candidate posts to `stats.rocknix.org`: the timer is not enabled in the image (`systemctl list-timers` on guest d after a boot shows no `rocknix-report-stats`), and the script, if kept, has no ROCKNIX endpoint (`grep -c rocknix.org` on the shipped script prints 0).

**Source:** #357, inputs/issues/357.md:16
**Checked:** 2026-10-06T16:16:51.958004+00:00
**Verdict:** PASS ✓

**Evidence:** Source rocknix-report-stats is an unconditional exit 0 with no endpoint. system.d/rocknix-report-stats.timer is masked to /dev/null. Read actual upgraded guest docs/qa-logs/2026-10-03-m7-final-runtime/artifacts/identity/{003,004,005,006}.log and pixelelated-1e6a runtime-05 timers.txt: only evidence/tmpfiles timers, masked statistics unit, endpoint count 0. Replacement09 installed artifact sweep retains the same b03adb70 shim hash and /dev/null target; unchanged source continuity through frozen14 was verified.

**Refutation attempted:** Found a retained timers.target.wants symlink and checked its ultimate target. It points at the masked /dev/null unit, so its presence cannot schedule collection. The retained service invokes only the inert shim.

**Notes:** Earlier guest runtime evidence is attributed to its actual image; not reported as a new14 timer execution.

### AC-I337-L28

> A GENERIC_X64 image boots under the new name with its own splash and logo, `OS_NAME` read from `/etc/os-release`, the manual-update row visible, and no automatic upstream update request in the captured guest network evidence (frame/readback/capture filed here).

**Source:** #337, inputs/issues/337.md:28
**Checked:** 2026-10-06T16:16:51.958069+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Actual14 qa-18 installed payload and identity frames prove inherited OS_NAME=pixelelated, its wordmark and MANUAL UPDATES. Actual boot-qualification05 provides unchanged boot renderer proof. ES ApiSystem refuses automatic/forced update checks for pixelelated; rocknix-update is inert, and older installed identity logs show query rc1 without output.

**Refutation attempted:** Searched retained QA logs for packet captures/network capture evidence and read the shipped updater; located source/installed-shim checks but no captured guest network trace establishing the literal final clause. tools/rasteratops-identity-check itself explicitly says it does not replace guest network proof.

**Notes:** No automatic upstream request is indicated by source. This is a missing specified measurement, not an observed unwanted request.

**Gaps:** Retain a bounded guest network observation covering automatic startup/update query paths, with a positive capture control, or explicitly reconcile the criterion to the stronger scoped evidence accepted by the owner.

### AC-I337-L27

> The register row that calls the direction (D-WORKFLOW-081's answer) names the fork's name and the licence terms it keeps (GPL-2 and MIT kept whole; the CC BY-SA attribution line; no ROCKNIX images).

**Source:** #337, inputs/issues/337.md:27
**Checked:** 2026-10-06T16:16:51.958104+00:00
**Verdict:** PASS ✓

**Evidence:** D-WORKFLOW-084 settles the fork direction and GPL-2/MIT preservation; D-WORKFLOW-144 makes pixelelated the current name. LICENSE.md retains upstream attribution and original code terms, distinguishes ROCKNIX branding CC BY-NC-SA 4.0 from new project artwork, and TRADEMARK.md governs project marks. Actual14 uses the new LCD wordmark.

**Refutation attempted:** Checked that old branding terms were not silently applied to new artwork and that upstream credits were not erased by a blanket rename. The criterion shorthand CC BY-SA omits NC; the actual retained licence is correctly BY-NC-SA.

**Notes:** No legal interpretation beyond verifying the project’s recorded policy and source text.

### AC-I359-L29

> A register row records the artwork licence and whether a trademark policy exists; `LICENSE.md`'s branding section names the fork's terms and `TRADEMARK.md` exists or the row says why not (`tools/vocabulary-check` and the licence text in the image's `/usr/share/licenses` agree: a `grep` on the image's SYSTEM).

**Source:** #359, inputs/issues/359.md:29
**Checked:** 2026-10-06T16:16:51.958126+00:00
**Verdict:** PASS ✓

**Evidence:** D-WORKFLOW-131 sets artwork and trademark policy; D-WORKFLOW-136/144 update bot/project names. LICENSE.md branding section and TRADEMARK.md implement those terms. Fresh local hashes agree with actual14 qa-18 installed payload records: LICENSE 1a277de267611abc4242e6a1e08ac2abac54316e7abcbf8ae7afd0a1dc98ec6c, TRADEMARK d46db25cb845b021cd7f1c13dabcd98d04e77d89a45968527e58abc9e3788761, both mode644. Fresh audit vocabulary passed.

**Refutation attempted:** Checked whole installed-file hashes on clean and upgrade, rather than only matching the displayed name; verified the font’s separate OFL terms are retained and not overwritten by project artwork terms.

**Notes:** Registration is deferred #360; current trademark policy exists without claiming registered status.

### AC-I409-L266

> Saved specification and editable master explicitly name Tiny5 Duo LCD; recorded font hash matches the existing approved face.

**Source:** #409, inputs/issues/409.md:266
**Checked:** 2026-10-06T16:18:15.161844+00:00
**Verdict:** PASS ✓

**Evidence:** docs/pixelelated/art/wordmark-system.md and source/pixelelated-live-text.svg explicitly use Tiny5 Duo LCD. source/font.json pins version2.007, upstream f740beb653d6839fac1f8c794668ffcf22037342 and SHA256 b0cada86874b192d304716536e84e735ec9b22719a3b9c2ba390ab0881a3a916. Fresh generator --check with the actual pinned splash font reproduced all ten SVG/CSS products; evidence/wordmark-controls-01/reproduce.log.

**Refutation attempted:** Used the installed build source’s font bytes and generator family/hash check, not an approximate font name. A deliberately wrong font hash is rejected.

**Notes:** Default python lacks fontTools; the existing /tmp/pixelelated-fontenv interpreter supplies the documented4.66.1 dependency. No download or font substitution.

### AC-I409-L267

> Six outlined SVGs and two monochrome variants reproduce from the pinned font/palettes; exact RGB555 colors, alpha gaps, orientation and hard boundaries pass artifact checks.

**Source:** #409, inputs/issues/409.md:267
**Checked:** 2026-10-06T16:18:15.161912+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh wordmark-controls-01 results: ten vector/CSS files exactly reproduced from150 original LCD contours; all24 PNGs use exactly their RGB555-derived colors and only alpha0/255. Standard alpha masks are identical and Scanline strictly removes rows. Direct source read shows five exact rectangles, vertical zones only for Dual, horizontal bands otherwise, and no background/image/font embedding in production SVG.

**Refutation attempted:** Four invalid RGB555 inputs and wrong font hash were rejected. Compared complete transparency masks across every treatment; verified Scanline removes pixels rather than adding a background. Source color conversion resolves inconsistent draft hex examples using canonical triplets.

**Notes:** Six multicolor and two monochrome products are preserved. Runtime’s NanoSVG-compatible flattened path asset is separately verified, not confused with the portable clipped master.

### AC-I409-L268

> Retained light/dark/midtone/saturated and small-size proofs demonstrate the portable assets; runtime integration remains separately tracked before the image freeze.

**Source:** #409, inputs/issues/409.md:268
**Checked:** 2026-10-06T16:18:15.161941+00:00
**Verdict:** PASS ✓

**Evidence:** Directly reviewed art/proofs/backgrounds.png: all eight treatments on white, near-black, mid-gray and saturated magenta, including expected low-contrast monochrome examples. small-sizes.png compares Ocean and light monochrome at16/24/32/64px. Boot-qualification05 and actual14 installed f5fa9839 assets separately establish integration.

**Refutation attempted:** The small proof exposes weak24px LCD sampling; it is not represented as universally readable. The specification permits monochrome/dedicated small marks, while current boot uses the larger approved form. Checked that background examples do not become standard asset backgrounds via fresh alpha checks.

**Notes:** Portable design proofs are not asserted as device rendering tests.

### AC-I337-L29

> The approved placeholder site under the fork domain carries lineage/attribution and release/adoption links; its build/retrieval receipt is filed here. A full site is later scope (D-WORKFLOW-098).

**Source:** #337, inputs/issues/337.md:29
**Checked:** 2026-10-06T16:18:15.161961+00:00
**Verdict:** SKIP ○

**Evidence:** D-WORKFLOW-098 explicitly chooses a name-only placeholder, superseding the criterion’s lineage/adoption link requirement. D-WORKFLOW-099 selects GitHub Pages and leaves deployment separately tracked; input issue337 itself calls this the approved placeholder rather than a full-site gate.

**Refutation attempted:** Read the actual decision text against the checkbox: the checkbox still asks for content expressly removed by the owner. No site build/retrieval proof was located in current P4 evidence.

**Notes:** Stale contract and P5 deployment follow-up; do not claim a deployed site or add unapproved content. Reconcile the issue body during punch-list disposition.

### AC-I337-L53

> The release notes and the site's ssh page say the ssh password is unchanged in 0.0.1 (D-WORKFLOW-129, #358): the notes file's line and the docs PR.

**Source:** #337, inputs/issues/337.md:53
**Checked:** 2026-10-06T16:18:15.161984+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** D-WORKFLOW-129 records the unchanged rocknix password and later #358. NAMING.md retains the password contract. Searches of current docs/releases, docs/rasteratops and the local website do not locate the required0.0.1 release note and SSH-page change; current website FAQs instead describes upstream generated passwords.

**Refutation attempted:** Checked the actual local website content rather than assuming the policy row was already published. The #327 screenshot commit does not change SSH documentation.

**Notes:** Known P5 documentation/release work, not a new device-runtime regression.

**Gaps:** Write and publish the accurate fork release/adoption and SSH documentation before distribution to players; keep site access403/404 disposition explicit.

### AC-I359-L30

> The release notes' lineage and non-endorsement paragraph (#344 P4) points at the same terms.

**Source:** #359, inputs/issues/359.md:30
**Checked:** 2026-10-06T16:18:15.162004+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** LICENSE.md and TRADEMARK.md implement the approved terms and actual14 carries their identical bytes. No0.0.1 release-note lineage/non-endorsement paragraph is present under docs/releases; #344’s release-note criterion remains explicitly P5 in the current milestone.

**Refutation attempted:** Searched the release and identity documentation for the actual promised paragraph and terms links; policy files alone do not satisfy a release-note claim.

**Notes:** Existing later publication gate, not completed by this P4 audit.

**Gaps:** P5 release notes must state lineage/non-endorsement and link the same installed project terms.

### AC-I465-L20

> A reusable harness loads settings before ES starts, verifies the unchanged installed ES/proxy/ctl identities, and records a real interface address disconnect/reconnect.

**Source:** #465, inputs/issues/465.md:20
**Checked:** 2026-10-06T16:19:25.158403+00:00
**Verdict:** PASS ✓

**Evidence:** Read tools/ra-ui-test:139–169 and :126–135: hash installed ES/ctl/all proxy bytecode, stop ES, write settings, clear owned fixture, then restart and verify a different PID; actual NetworkManager disconnect removes the address for two watcher observations. qualified-03 contains all four corresponding assertion sets. Fresh local readback confirms all46 installed hashes invariant across profiles and unchanged ES lifetime within each.

**Refutation attempted:** Earlier owner01 omitted compiled modules; owner03 explicitly requires flusher.pyc and hashes all44 proxy files. Earlier owner02 carried pending state into French; owner03 clears its owned fixture before restart and asserts no startup outcome.

**Notes:** Dedicated synthetic QA fixture; no real account or physical network operation.

### AC-I465-L21

> English/French sending and sent outcome frames at640x480 and1280x960 show readable correctly bounded cards, matched to pending counts, actual installed-flusher loopback receipts and `last-sync-link` records.

**Source:** #465, inputs/issues/465.md:21
**Checked:** 2026-10-06T16:19:25.158465+00:00
**Verdict:** PASS ✓

**Evidence:** Directly reviewed all four profiles’ sending and sent frames at640x480 and1280x960. Cards remain within panel bounds; English/French text fits. qualified-03 actual installed flusher.pyc receipts show patch/award/unlocks HTTP200, flushed1/pending0; installed ctl pending assertions and last-sync-link status0 sent agree. Fresh local reconciliation totals109 passing assertions.

**Refutation attempted:** Compared images with raw provider and stamp evidence, rather than treating a sending card or an exit frame as proof of upload. Checked both languages and both panel sizes.

**Notes:** Local HTTP provider verifies actual installed flusher/UI composition. Real RetroAchievements acceptance is separately established by RA33, not by these synthetic cases.

### AC-I465-L22

> A controlled refused send retains pending state and produces the bounded failure/retry outcome; empty/repeated link transitions do not invent another successful send.

**Source:** #465, inputs/issues/465.md:22
**Checked:** 2026-10-06T16:19:25.158492+00:00
**Verdict:** PASS ✓

**Evidence:** EN640 refuse-flush.json records HTTP503, flushed0/pending1; refuse-stamp.txt is status5 not-sent IT STOPPED ANSWERING. Directly viewed refusal sending/outcome/dismissal: bounded failure and retry sentence, then no card. All four empty-repeat frames have no notification and assertions require unchanged last-sync-link.

**Refutation attempted:** The rejected request does not yield a success stamp or drop the award. Read the bounded polling rather than assuming the card ended from a screenshot alone; the positive send and refused request provide contrasting outcomes.

**Notes:** Failure case is English640 only as specified; full four-profile failure localization is not claimed.

### AC-I465-L23

> Every frame claim is directly reviewed; original failures are retained. The standard watcher, four terminal result channels and actual owned guest/provider cleanup are verified.

**Source:** #465, inputs/issues/465.md:23
**Checked:** 2026-10-06T16:19:25.158520+00:00
**Verdict:** PASS ✓

**Evidence:** All23 qualified originals directly viewed during this independent audit, plus the superseded French baseline showing its erroneous startup send. Owner01/02 evidence remains present. Qualified completion.json records all four rc0 and actual five-process absence, no QEMU, unbound10026/5912 at07:01:20; fixture checks every local provider/flusher exited.

**Refutation attempted:** Successful wrapper codes did not rescue earlier invalid owners. Per-profile visual_review=pending is intentionally immutable; separate visual-review.json and actual pixel inspection complete that later gate. Read both terminal and cleanup evidence.

**Notes:** Connected standard watcher was consumed; no off-session notification claim.

### AC-I465-L24

> The ordinary award harness starts ES with its updated settings and captures reconnect as well as exit events, without weakening its unearned/API checks. Changed harness behavior has VM evidence; the completed RA33 account proof remains immutable.

**Source:** #465, inputs/issues/465.md:24
**Checked:** 2026-10-06T16:19:25.158539+00:00
**Verdict:** PASS ✓

**Evidence:** Direct git diff629603d6 for tools/ra-offline-test adds settings reload before launch, actual address removal, reconnect capture/wait and current sent stamp; existing unearned/account/API checks remain. Fresh bash -n exits0. UI owner03 separately executes the changed settings/address/card mechanics on frozen14. RA33 evidence remains separate and immutable.

**Refutation attempted:** No changed ordinary-runner full execution is claimed. Reviewed the complete diff for weakened assertions: screenshot failure now propagates, and outcome timestamp must follow T_UP. Existing account checks were not deleted or relaxed.

**Notes:** Future ordinary award run still needs an unearned achievement; no new reset consumed for this audit.

### AC-I465-L25

> Publish exact evidence and reconcile #361/M7 coverage. Begin the approved #383 P4 fixes audit only after the remaining software qualification is satisfied.

**Source:** #465, inputs/issues/465.md:25
**Checked:** 2026-10-06T16:19:25.158556+00:00
**Verdict:** PASS ✓

**Evidence:** Actual qualification07:01:40 precedes audit setup07:04:22. inputs/ui-publication.json records remote feature629603d6 and next63675be4 readback07:04:47; inputs/ui-tracker-completion.json and retained issue bodies reconcile361/383/465 and M7 at07:05:49. Published commit contains the exact qualified receipts and harness change.

**Refutation attempted:** Distinguished UI qualification, publication and audit phase timestamps. Review started only after UI passed; neither this ordering nor #465 closure is used as evidence that P4 itself has passed.

**Notes:** This audit later found separate content/sign-in issues. They do not falsify the narrow reconnect-card qualification.

### AC-I337-L40

> A fresh guest on the candidate, signed in to the QA cloud, creates and uses `/pixelelated/{Saves,Backups,Content}`: `tools/cloud-test-backend ls` after a backup and a saves sync shows the three folders and nothing under `/ROCKNIX`; `grep -rn ROCKNIX projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf*` prints nothing; `tools/vocabulary-check` passes.

**Source:** #337, inputs/issues/337.md:40
**Checked:** 2026-10-06T16:21:18.341104+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Both current cloud_sync.conf files define /pixelelated/Saves, /pixelelated/Backups and /pixelelated/Content. Actual mixed pair optins-11 starts a fresh guest on all three and verifies final remote bytes/config convergence; guest-11 creation cases and actual14 cloud318/default round-trip verify installed consumers. Fresh vocabulary passed.

**Refutation attempted:** Ran the requested ROCKNIX source search: it returns two archive-format comments, one per conf, describing the retained ROCKNIX_SETTINGS suffix. These are valid compatibility documentation, not stale default paths.

**Notes:** The functional destination requirement is supported; the literal grep-empty clause contradicts retained archive compatibility and needs reconciliation.

**Gaps:** Amend the source predicate to check active path values while explicitly allowing the two archive-format comments; retain a named fresh-guest three-tier listing as the criterion’s exact artifact.

### AC-I337-L41

> Every `/ROCKNIX` cloud path in the interface and the scripts is listed by the sweep (`docs/rasteratops/p0-sweep-hits.txt`, rule `cloud-path`, 56 lines) and each is changed or marked history in the same commit; the sweep re-run on the candidate's tree lists none as current.

**Source:** #337, inputs/issues/337.md:41
**Checked:** 2026-10-06T16:21:18.341177+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Historical p0-sweep-hits.txt records the56 cloud-path hits; p0-sweep.md explicitly dates its immutable baseline51f78ac5b4. Current NAMING.md and rename-plan.md classify legacy roots as migration/kept-choice/archive inputs, while current defaults use /pixelelated. Actual replacement09 artifact classification reports zero FIX/UNKNOWN contexts, with retained-context allowlist.

**Refutation attempted:** The old56-line list is a historical snapshot, not a refreshed one-to-one mapping to today’s source. Its broad cloud-path rule also included a mirror URL. A zero unclassified installed sweep does not establish every old line’s exact same-commit disposition.

**Notes:** No new incorrect default path is demonstrated by this bookkeeping gap. Existing #467 concerns content discovery separately.

**Gaps:** Reconcile the old per-hit criterion to the current context-based source/artifact classification, or supply the explicit56-entry disposition map. Do not erase valid legacy readers to satisfy a blanket grep.

### AC-I337-L50

> `DISTRONAME="pixelelated"`: `os-release` reads `OS_NAME="pixelelated"`, the images are `pixelelated-<board>.<arch>-0.0.1.*`, the info page reads `OPERATING SYSTEM: pixelelated` (a 640x480 frame from guest d; `/etc/os-release` from the image's SYSTEM); repositories, packages and hosts stay lowercase `rasteratops`; the cloud folder is `/pixelelated` (D-CLOUD-158).

**Source:** #337, inputs/issues/337.md:50
**Checked:** 2026-10-06T16:21:18.341206+00:00
**Verdict:** PASS ✓

**Evidence:** distributions/ROCKNIX/options sets DISTRONAME=pixelelated; scripts/image uses it for OS_NAME and artifact names. Actual14 installed payloads and directly reviewed identity frames show pixelelated; the frozen image/update names begin pixelelated and conf defaults use /pixelelated.

**Refutation attempted:** Actual OS_NAME propagation was separately verified at the child-process boundary (#424), not inferred only from os-release. The criterion’s repositories/hosts stay rasteratops clause is superseded by D-WORKFLOW-144; retained internal ROCKNIX contracts follow D-WORKFLOW-123.

**Notes:** Functional current identity passes. Reconcile stale criterion wording; no backward rename of organization or machine contracts.

### AC-I337-L51

> The migration tar carries the suffix `-from-ROCKNIX` (`IMAGE_SUFFIX`), so its name passes the RC2 init's check (`init:882`): the built name is `pixelelated-H700.aarch64-0.0.1-from-ROCKNIX.tar` and `tools/vm-upgrade-rehearsal` from RC2's image applies it; the suffix is dropped in the build after 0.0.1 (D-WORKFLOW-128).

**Source:** #337, inputs/issues/337.md:51
**Checked:** 2026-10-06T16:21:18.341227+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** IMAGE_SUFFIX=from-ROCKNIX and scripts/image:116–117 append it. Actual14 qa-18 upgrade/rehearsal.log boots retained September29 RC2 69e6039f8f, stages pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.tar, returns7afa9efcfc and passes26 preservation assertions.

**Refutation attempted:** Checked real old-build identity, update queue and preserved bytes; this is not a newly created old-shaped guest. No current H700 image is present, so the literal H700 filename/build clause is not inferred from x64.

**Notes:** VM adoption is qualified; H700 and later suffix removal remain planned release work.

**Gaps:** Build the frozen H700 arm/aarch64 chain after P4/capacity gates, retain its actual named artifact and perform the separately authorized physical adoption check.

### AC-I337-L52

> The splash and the theme's logo carry the word mark alone until the icon arrives (D-WORKFLOW-130): the splash frame at boot and the theme's logo frame on guest d show the name in the chosen face and no pictorial mark.

**Source:** #337, inputs/issues/337.md:52
**Checked:** 2026-10-06T16:21:18.341248+00:00
**Verdict:** PASS ✓

**Evidence:** Source splash pin8c71126c and ES/theme assets use the canonical f5fa9839 lowercase LCD wordmark with no icon. Actual14 payload hashes match; boot-qualification05 clean/upgraded640/1280 frames directly reviewed in I433 and exact template match1.0 with12 rejected negative controls. Fresh portable asset proofs contain only lettering.

**Refutation attempted:** Checked old-logo negative rejection and that neither theme selection nor runtime asset introduces character art. The old Rasteratops icon was not merely recolored.

**Notes:** Separate boot status text is outside the wordmark; transparency is preserved in the canonical source.

### AC-I354-L67

> The rehearsal (`tools/vm-upgrade-rehearsal`) from RC2's x64 image keeps every piece of state across the update (its PASS), and a stock-shaped conf carried across (`/GAMES`, nothing in the cloud) meets the cloud folder step at the boot after rather than a dialog from the startup sync: the startup stamp's `78 no-folder` and the step's CREATE IT offer in 640x480 frames (guest d's epic proof, case E; D-CLOUD-166, D-CLOUD-170).

**Source:** #354, inputs/issues/354.md:67
**Checked:** 2026-10-06T16:21:18.341265+00:00
**Verdict:** PASS ✓

**Evidence:** Actual14 qa-18 upgrade/rehearsal.log independently shows retained RC2 identity, four save/state hashes, marker, setting, remote, cloud pointers and backup unchanged after the update. guest-11 E installed logs and previously directly reviewed640 offer show startup78 no-folder followed by CREATE IT / CHOOSE A FOLDER / NOT NOW for empty stock-shaped GAMES.

**Refutation attempted:** The startup path does not issue the interactive dialog itself; boot setup owns the offer. Existing populated and keep fixtures take different paths, so this is not an unconditional CREATE IT screenshot.

**Notes:** Uses unchanged cloud source from replacement09 and current14 upgrade evidence, with their actual image identities.

### AC-I354-L68

> `tools/vm-qa` on the candidate passes every suite, `frame-diff` against the accepted baseline explains every changed frame by one of the children, `tools/vocabulary-check` and `tools/es-menu-map-check` pass.

**Source:** #354, inputs/issues/354.md:68
**Checked:** 2026-10-06T16:21:18.341281+00:00
**Verdict:** PASS ✓

**Evidence:** Actual14 qa-18 default suite results: all15 suites pass,1719 script assertions and16 walks/78 frames; frame-diff has34 claimed regions and no unclaimed/missing changes. Fresh audit host menu-map/vocabulary and ES vocabulary checks pass.

**Refutation attempted:** Earlier QA15/16 manager failures and wrong-fixture frames are preserved and not accepted. Actual14 manager source/lifetimes and exact GB/NES/FBNeo frames were rechecked independently under I455.

**Notes:** A green existing suite is limited to its predicates; separately discovered #467/#468 remain valid audit findings.

### AC-I354-L69

> Every string the five children add is approved by the maintainer before the build and lands with its French (D-UI-051); `docs/cloud-sync-changelog.md` carries the changes the day they land (`change-log.md`); the site's cloud-sync page names `/pixelelated` (`documentation-accuracy.md`, with #42).

**Source:** #354, inputs/issues/354.md:69
**Checked:** 2026-10-06T16:21:18.341298+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** D-CLOUD-164 approves13 strings and ESdc819f43 includes cloud page strings and French together; dated changelog records Oct1 cloud features and Oct4 /pixelelated transition. docs/pixelelated/cloud-folders.md prepares current wording. Actual local website cloud-sync.md:108 still says /ROCKNIX.

**Refutation attempted:** Read the site file instead of assuming the prepared fork document updated it. Independent I351-L62 also finds the approved French phone/finishing strings absent, despite broader page translations.

**Notes:** Combines a current localization defect with separate P5 website work.

**Gaps:** Fix French phone/finishing surfaces under the recorded draft finding and verify both languages; reconcile/publish the cloud-sync site with the current default once the website destination/access is resolved.

### AC-I354-L66

> The mixed-installation test (`tools/cloud-pair-migration` on `tools/vm-pair`): guest a updated in place from RC2's image with a `/ROCKNIX` cloud, guest b a fresh install on the same QA cloud; for the default-derived fixture both confs end at `/pixelelated/{Saves,Backups,Content}`; separate populated/custom backup and explicit-root content fixtures retain their independent pointers and byte access, a save written on each arrives on the other, nothing was removed from `/ROCKNIX` before its verified copy, a guest that missed its step and wrote into the earlier folder is merged by MOVE (D-CLOUD-168), and the log names each step: its PASS lines, and its negative control on a build without the join (D-CLOUD-169) failing.

**Source:** #354, inputs/issues/354.md:66
**Checked:** 2026-10-06T16:23:14.264428+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Directly read actual optins-11 pair-console.log: retained69e6039f8f upgraded in place, freshcf511 guest,42 passing assertions, save bytes in both directions, per-tier copy/verify before removal, marker follow and staged late-write MOVE merge. Separate guest-11 B explicit-root fixture and prior independently audited custom backup controls preserve independent pointers.

**Refutation attempted:** The old-code host baseline has22 real failures and constructed runner negatives exist, but searches did not locate the literal mixed-pair run on a build without the join. Staged late writes are explicitly distinguished from an old live guest writing concurrently.

**Notes:** Positive mixed-installation behavior is qualified; the requested exact negative remains an evidence gap.

**Gaps:** Locate or retain the installed no-join mixed-pair negative, or reconcile the criterion to the named old-code and guest controls without relabeling them.

### AC-I361-L123

> Upstream Linux suites and fork proxy regression sections pass on the exact selected source; cold image build, tools/ra-offline-test and UI/progress/flush proof pass on the VM.

**Source:** #361, inputs/issues/361.md:123
**Checked:** 2026-10-06T16:23:14.264498+00:00
**Verdict:** PASS ✓

**Evidence:** The upstream Linux818-test execution uses b09 source whose219 Linux and53 native files compare byte-for-byte with selected879, excluding generated .orig files; equality evidence retained. Fresh selected879 focused proxy controls and actual14 proxy22/native18/legacyCHD4/subset35 all pass. Cold build provenance, later frozen14 build642/642, RA33 real unearned/offline/provider/relaunch and UI465109 assertions/23 frames establish the composed VM gate.

**Refutation attempted:** Did not pretend that818 upstream tests were newly executed on an879 checkout; source equality is explicit. UI exit-only frames were insufficient until separate real-address reconnect proof. Original runtime/header/schema/consent failures remain retained.

**Notes:** Indexed125-game performance proof is separately partial under I361-L121; this clause’s ordinary offline award/UI/flush proof is complete.

### AC-I383-L284

> #365's T01–T26 table maps each relevant actor/state cell to executable assertions or a justified inapplicable cell; #356 adds strict supported-version, numbered-step, marker-failure and interrupted retry/fleet controls; #320 has deterministic recovery-race controls; writer-shaped archive discovery is the first negative control. The promoted guest proof resets every case and exits nonzero on an injected assertion failure.

**Source:** #383, inputs/issues/383.md:284
**Checked:** 2026-10-06T16:23:14.264533+00:00
**Verdict:** PASS ✓

**Evidence:** Independent actor-map-pass-coverage.json connects208 actor/state cells to210 exact assertion names; fresh full1719/focused316 host tests pass with expected injected rc1. Actual guest-11 and focused cloud-boundaries01 cover strict markers, numbered steps, nine copy/delete/marker fault/follower cases. Fresh deterministic ES320 tests119 assertions and old failures verify lock recovery. Writer-shaped archive negative is first in retained remediation baseline. Guest-negative02 records actual0PASS/1FAIL rc1.

**Refutation attempted:** Read case-reset mechanism and actual installed negative rather than accepting a check that exited before a guest. Source/error controls distinguish unknown markers from absence, and unsupported marker UI wording remains separately defective #468.

**Notes:** Coverage-map completeness does not erase behavior defects discovered outside its predicates.

### AC-I383-L285

> #376/#377/#379/#380/#381 and #365 settlement, #363 card ordering, #364 timing, #366 fixture defects have source fixes and retained passing/failing controls. Each owning issue carries its own evidence.

**Source:** #383, inputs/issues/383.md:285
**Checked:** 2026-10-06T16:23:14.264555+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Independent child entries verify source/installed controls for376/377/379/380/381/365/363/364/366, including fixed timing and archive restoration. This review also confirms #467 content classification and #468 future-marker reason loss; narrow settlement/manual chooser/hostname/S3 retry evidence gaps remain in the ledger.

**Refutation attempted:** Re-derived child criteria instead of treating closed tracker states or broad suite success as sufficient. Some compound clauses do not have their exact requested runtime observation.

**Notes:** This is the ongoing P4 fixes audit’s aggregate punch list, not a new claim that all remediation failed.

**Gaps:** Resolve confirmed product findings and exact child evidence gaps; update owning issue criteria/evidence and requalify affected frozen inputs before an RC.

### AC-I383-L286

> #361/#362/#386 input refresh and preservation checks pass; #310/#327/#332 carry-forward software criteria and host gates are resolved. #337's approved OS identity is integrated on the frozen upstream baseline. One recorded input set produces the candidate; clean install, RC2 upgrade, full VM QA, pair migration, visual and timing evidence identify that build.

**Source:** #383, inputs/issues/383.md:286
**Checked:** 2026-10-06T16:23:14.264574+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Current input refresh and preserved state/native/proxy tests are verified under361/362/386. Carry-forward310/327/332 software proofs pass. Frozen14 manifest6550/207/180, immutable bundle19 files, actual clean/RC2 upgrade/default QA and unchanged-source pair/boot/visual/endurance evidence are tied to their proper builds.

**Refutation attempted:** Prior-image evidence is carried only with consumed-byte continuity, not renamed as14 execution. Literal125-game installed scan is still missing; identity criteria include stale contract text and a missing guest network capture.

**Notes:** Image is an engineering candidate with known audit findings, not yet a release candidate.

**Gaps:** Close current product/evidence punch list, preserve exact input custody through any fixes, and rerun affected VM gates.

### AC-I383-L287

> The code-auditor review of the fixes includes the approved independent other-lab model through the Facilitator; findings are resolved and any resulting product changes rebuilt and requalified before an RC claim.

**Source:** #383, inputs/issues/383.md:287
**Checked:** 2026-10-06T16:23:14.264593+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** This milestone-tier code-auditor run selected independent depth: Codex primary plus Fable5.1/xhigh through the verified Facilitator. Phase2 is active; external blind/refutation calls correctly await2.5/3/4/4.5. Frozen product has not been mutated mid-audit.

**Refutation attempted:** No live detached reviewer or completed external opinion exists. The approval service currently cannot refresh its login token; no provider command executed and no substituted local seat counts.

**Notes:** Existing authorized next gate, not a request for new permission.

**Gaps:** Complete the serial primary stages, restore tool approval authentication, run verified other-lab review, disposition/refute findings, then fix/rebuild/requalify before any RC claim.

### AC-I409-L236

> Record the new identity hierarchy and lowercase default in the append-only decision register; reconcile active naming policy, instructions, milestone order and open issue criteria. Retain historical attribution and closed titles.

**Source:** #409, inputs/issues/409.md:236
**Checked:** 2026-10-06T16:23:14.264612+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** D-WORKFLOW-144/145/146 and D-CLOUD-174 record lowercase identity, characters/LCD and new root. NAMING.md, active rules and rename-plan.md agree; M7 keeps its ordered current phases and frozen historical artifacts.

**Refutation attempted:** Exact input issues still contain stale requirements:337L50 says repositories/hosts remain rasteratops,337L29 asks for links removed by D-WORKFLOW-098, and blanket grep predicates conflict with retained compatibility comments. NAMING’s seven FIX contexts paragraph is historical but not labeled as such after416 resolved it.

**Notes:** Core naming implementation is correct; full active-contract reconciliation is incomplete.

**Gaps:** Reconcile affected open acceptance text and clearly label the first-sweep status as historical; preserve closed titles and original evidence.

### AC-I409-L237

> Classify old-name references across active source, tools, sibling repos and infrastructure; retain an explicit compatibility/history/owner/character allowlist. Canonical org URLs and relevant Git remotes resolve to pixelelated; the personal account is verified as rasteratops and the bot identity is unchanged. Historical maxengel-owned forks retain their verified locations; rasteratops/rocknix.org returned 404 and no transfer is assumed.

**Source:** #409, inputs/issues/409.md:237
**Checked:** 2026-10-06T16:23:14.264628+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** NAMING v2 and rename-plan classify compatibility/history/owner/character references. Fresh local remotes show distribution and ES origins under pixelelated, while upstream and verified historical maxengel forks remain. Actual published source refs and consumed ghcr.io/pixelelated/build digest support new namespace use. User confirmation and the dated Oct4 work log record owner rasteratops and unchanged Blitterbot; rocknix.org403/404 is explicitly unresolved.

**Refutation attempted:** Did not globally rewrite maxengel forks or assume the website transferred. A fresh external readback was attempted but rejected before execution by approval-service login refresh failure; no new account/API verification can be claimed.

**Notes:** Source/remote classification is supported; the original detailed repo/account readback receipt was not located in retained primary artifacts during this audit.

**Gaps:** Retain a sanitized repo/account ID and canonical URL readback once approval authentication works; keep website destination/access unresolved rather than silently selecting another repository.

### AC-I409-L238

> Distribution/ES/splash/theme and licence/trademark source use the agreed lowercase identity and Tiny5 Duo LCD wordmark alone. Exact source pins and existing lint/syntax/identity guards pass; obsolete brand references are classified rather than globally replaced.

**Source:** #409, inputs/issues/409.md:238
**Checked:** 2026-10-06T16:23:14.264646+00:00
**Verdict:** PASS ✓

**Evidence:** Current distro options, ES f6f0c134, splash8c71126c, theme canonical f5fa9839 wordmark and LICENSE/TRADEMARK use lowercase pixelelated. Fresh package checks, ES unit/vocabulary guards, source export controls and exact font reproduction pass; retained native/C++ syntax checks and actual14 installed identity support runtime.

**Refutation attempted:** Checked compiled OS_NAME propagation, real XML parser, OFL font provenance and preserved upstream credits rather than a global string replacement. The previously retained old wording/XML failures remain as controls.

**Notes:** No icon or alternate font is introduced; current input and source hash continuity are retained.

### AC-I409-L239

> New setup defaults to /pixelelated; configured /ROCKNIX and /GAMES selections and archive discovery remain usable. Isolated controls and candidate clean/upgrade receipts demonstrate no silent cloud relocation or archive loss.

**Source:** #409, inputs/issues/409.md:239
**Checked:** 2026-10-06T16:23:14.264661+00:00
**Verdict:** PASS ✓

**Evidence:** Current defaults use /pixelelated; actual mixed RC2/fresh pair42 checks, guest-11 keep/not-now/explicit-root cases, focused boundaries and actual14 upgrade26 retain source bytes and configured pointers. Fresh316 layout plus1719 full host checks exercise legacy archive readers and interrupted recovery.

**Refutation attempted:** Migration is explicit copy/verify/remove, not a blind remote rename. Custom backup/content pointers are kept independent. Existing legacy archive suffixes/readers remain; configured/kept ROCKNIX/GAMES do not become empty new folders.

**Notes:** The separate #467 content-presence classifier defect does not demonstrate relocation or archive loss; it remains a blocker under its own criteria.

### AC-I409-L240

> The update asset naming/procedure satisfies the ROCKNIX RC2 predecessor init check, and the new image accepts future pixelelated updates. Retain actual upgrade evidence for ROCKNIX RC2.

**Source:** #409, inputs/issues/409.md:240
**Checked:** 2026-10-06T16:23:14.264676+00:00
**Verdict:** PASS ✓

**Evidence:** Actual14 rehearsal boots69e6039f8f and applies the named from-ROCKNIX tar, returns7afa9efcfc with26 preservation assertions. Current init:883 substitutes @DISTRONAME@ from scripts/image, and options supplies pixelelated; future pixelelated filenames satisfy that predicate.

**Refutation attempted:** Read the original predecessor’s filename match and actual staged filename. This does not assert OTA offering, version ordering, wrong-architecture protection, or an executed future0.0.2 update.

**Notes:** D-WORKFLOW-128 makes suffix removal/fork-to-fork runtime proof a later release gate; actual RC2 adoption is qualified now.

### AC-I409-L241

> Verify the build-container namespace/digest and source fetches. A monitored build with tested delivery produces a newly frozen pixelelated artifact; retain the image identity/manual-update/brand/licence/source/localisation checks and affected default/upgrade/visual/performance evidence. Do not rename or relabel replacement02.

**Source:** #409, inputs/issues/409.md:241
**Checked:** 2026-10-06T16:23:14.264691+00:00
**Verdict:** PASS ✓

**Evidence:** Consumed-container.json for the cold build records ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39 as configured and consumed. Exact source inventory568 roots and archive hashes bind frozen14’s new bundleb77e47e57a; watched build642/642 and four terminal rc0 are retained. Actual14 identity/licence/manual-update/default/upgrade plus unchanged-source classified/localized/visual/performance evidence are separately identified.

**Refutation attempted:** Replacement02 remains historical and is not renamed. New manifests and hashes identify actual new bytes; source/QA files and raw symlink targets were independently reverified. Public component licence metadata gaps and off-session notification are not claimed complete.

**Notes:** This passes engineering build qualification scope, not P5 publication readiness.

### AC-I409-L242

> Expand the approved P4 primary plus Fable5.1 Facilitator fixes review to this transition; resolve findings and renew affected artifact proofs before calling the image an RC.

**Source:** #409, inputs/issues/409.md:242
**Checked:** 2026-10-06T16:23:14.264707+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** The current383 audit explicitly includes rename/identity, renderer, cloud and proxy changes on frozen14 and records the authorized Fable5.1 Facilitator plan. It has found product issues and is still in the primary stages.

**Refutation attempted:** No external review has run in this audit and no finding has been silently waived or fixed while scope was under review.

**Notes:** Current authorized work; no RC designation.

**Gaps:** Finish serial review, obtain verified independent opinion, resolve all blocker findings and renew affected installed proofs after changes.

### AC-I344-L196

> `docs/rasteratops/p0-read.md` exists with one decision per row of the base plan's §2, each citing `path:line`, and its first line answers three questions: does `DISTRO=rasteratops` imply a new directory; do image and asset file names derive from `DISTRO`, `DISTRONAME` or something else; what does `rocknix-update` match on. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md`

**Source:** #344, inputs/issues/344.md:196
**Checked:** 2026-10-06T16:24:27.284871+00:00
**Verdict:** PASS ✓

**Evidence:** p0-read.md starts with the three answers and a decision/evidence row for each base-plan section2 topic. Fresh historical source read confirms config/options sources a DISTRO directory and scripts/image derives display/artifact identity from DISTRONAME.

**Refutation attempted:** Checked mechanism references against historical51f78ac5b4, not just today’s renamed tree.

**Notes:** Historical P0 read, not current runtime qualification; current lowercase scope is D-WORKFLOW-144.

### AC-I344-L197

> The sweep report from the base plan's §1.15 command lists every hit in exactly one of four classes (display text; machine identity; persisted paths and network names; boot and storage contracts); every class 2 to 4 hit is marked KEEP, and any non-KEEP carries `path:line`, a reason and a reference to a recorded yes. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-sweep.md and p0-sweep-hits.txt`

**Source:** #344, inputs/issues/344.md:197
**Checked:** 2026-10-06T16:24:27.284932+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh parser verifies2415 rows and2415 unique path/line keys: classes1323/561/393/138. The sole class2–4 non-KEEP is rocknix-update endpoint with path:line, reason and D-WORKFLOW-093.

**Refutation attempted:** Rejected malformed rows and duplicate file/line classifications; examined the explicit exception.

**Notes:** Historical snapshot51f78ac5b4; later approved cloud-default changes supersede its KEEP choices and need current criterion reconciliation separately.

### AC-I344-L198

> The updater note records the mechanism, the asset pattern, redirect handling, any distro-name check, draft and pre-release handling, the manual route, and the comparison function's result on `0.0.1` against RC2's version string as a table, and names Branch A (unaided over-the-air) or Branch B (manual adoption). -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-updater.md`

**Source:** #344, inputs/issues/344.md:198
**Checked:** 2026-10-06T16:24:27.284959+00:00
**Verdict:** PASS ✓

**Evidence:** p0-updater.md provides mechanism, filename/board gate, curl redirect behavior, draft handling, manual route and both ordering tables; it selects Branch B with the reason that RC2 asks ROCKNIX’s service.

**Refutation attempted:** Read comparison rows: there is no client semantic-version ordering, and forced mode only accepts dates. A one-line new-image endpoint edit cannot change fielded RC2. Actual RC2→14 rehearsal corroborates the filename/manual path.

**Notes:** Later D-WORKFLOW-128 chooses suffix placement; historical updater note is not a current OTA implementation claim.

### AC-I344-L199

> `BUILD_ID`'s derivation is quoted with `path:line`, with its timestamp and host dependence stated. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § BUILD_ID`

**Source:** #344, inputs/issues/344.md:199
**Checked:** 2026-10-06T16:24:27.284990+00:00
**Verdict:** PASS ✓

**Evidence:** p0-read.md BUILD_ID section quotes image source and actual RC2 metadata: checkout commit or CUSTOM_GIT_HASH, separate BUILD_DATE and branch, no embedded timestamp. Current14 manifest/source confirm the same derivation.

**Refutation attempted:** Checked branch/host/time distinctions; two worktrees of one commit do not imply distinct BUILD_ID values.

**Notes:** Manifest binds more than BUILD_ID, which alone does not identify all consumed inputs.

### AC-I344-L200

> `docs/rasteratops/support-matrix.md` exists with the columns target/arch, physical boards, QA guest, clean install, upgrade, boot medium and boot-chain deltas, recovery method, attachment status; the mandatory migration device is marked. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/support-matrix.md`

**Source:** #344, inputs/issues/344.md:200
**Checked:** 2026-10-06T16:24:27.285011+00:00
**Verdict:** PASS ✓

**Evidence:** support-matrix.md has all requested target/arch, board, guest, clean/upgrade, boot/recovery and attachment columns; RG35XX SP is the mandatory migration device. D-WORKFLOW-114 explicitly defers RK3566 and preserves two panel sizes.

**Refutation attempted:** Read physical board and target distinctions, including DDR3/DDR4 and Nova ABL facts; old observations are dated and not represented as pixelelated tests.

**Notes:** Creation/content of the matrix passes; current device qualification is still later work.

### AC-I344-L201

> `df -B1` of the build volume and `du -sb` per existing root are recorded, with the forecast as line items (old roots, new roots, source archives, VM overlays, retained candidates). -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Disk`

**Source:** #344, inputs/issues/344.md:201
**Checked:** 2026-10-06T16:24:27.285028+00:00
**Verdict:** PASS ✓

**Evidence:** p0-read.md records Sep30 df volume bytes, seven root du values, shared archives, four QA disks and retained candidates; forecast separates old/new roots, cache growth, overlays and retained images.

**Refutation attempted:** Verified line items and units are present, rather than a claim that a4TB nominal disk has that much free space.

**Notes:** Historical capacity only. Current measured cleanup/retention and #461 capacity gate supersede this forecast before device builds.

### AC-I344-L202

> The per-asset size limit is recorded with its source and date; the ES licence is quoted from the ES tree; the splash repository's owner is recorded; the digest behind the build container's `:latest` is recorded; `DISTRO_SRC` or its equivalent is recorded. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts`

**Source:** #344, inputs/issues/344.md:202
**Checked:** 2026-10-06T16:24:27.285044+00:00
**Verdict:** PASS ✓

**Evidence:** p0-read.md Platform facts records dated GitHub asset limit/source, quotes ES MIT terms, names upstream splash owner/pin, consumed container digest and DISTRO_SRC/mirror. Current ES recipe says MIT, correcting the earlier discrepancy.

**Refutation attempted:** Checked each required fact is attributed and dated; font terms remain distinct.

**Notes:** The criterion is the P0 record. Publication must revalidate platform limits and actual asset sizes; no current internet lookup was possible here.

### AC-I344-L203

> D-WORKFLOW-088 (present in the register; absent from the run's packet) is cited, and Choice 2 of #338 is labelled or struck. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts`

**Source:** #344, inputs/issues/344.md:203
**Checked:** 2026-10-06T16:24:27.285060+00:00
**Verdict:** PASS ✓

**Evidence:** p0-read.md Platform facts explicitly identifies D-WORKFLOW-088’s absence from the old packet and strikes Choice2 via D-WORKFLOW-096, which records the second Lenovo64GB choice.

**Refutation attempted:** Read the actual decision row to ensure the missing choice was settled, not silently discarded.

**Notes:** No new infrastructure is created by this audit.

### AC-I344-L204

> `git log -- distributions/` shows no identity commit and `git tag` shows no `0.0.1`. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts`

**Source:** #344, inputs/issues/344.md:204
**Checked:** 2026-10-06T16:24:27.285077+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh git log at historical51f78ac5b4 confirms last distributions commit ff8058e311, upstream GRUB selection. P0 document retains the47-tag/no0.0.1 observation; current git tag --list0.0.1 is still empty.

**Refutation attempted:** Evaluated this pre-change criterion at its dated baseline, not today when identity commits appropriately exist.

**Notes:** Historical sequencing gate passes; current identity commits are intended.

### AC-I344-L212

> The three repositories are transferred and `rocknix-splash` forked; the ES and splash commits are pinned; every recipe URL and `git remote -v` in every worktree shows fork addresses.

**Source:** #344, inputs/issues/344.md:212
**Checked:** 2026-10-06T16:25:48.911566+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Current distro/ES origins are pixelelated; pinned ES/splash source archives and published refs are retained. Fresh remotes also retain ROCKNIX/upstream and maxengel historical forks deliberately.

**Refutation attempted:** A blanket every-recipe/every-remote fork-only requirement would incorrectly rewrite upstream dependencies and historical forks; input409 has the approved classified policy. Detailed account/repo transfer readback is currently blocked/unlocated.

**Notes:** Reconcile the literal old contract with D-WORKFLOW-144; do not destroy upstream remotes.

**Gaps:** Retain sanitized canonical repository/account readbacks and update the criterion to distinguish project origins from upstream source URLs and intentional remotes.

### AC-I344-L213

> The bot token's scope inventory (repositories × permissions × expiry) is recorded and an expiry reminder is configured on the mail channel.

**Source:** #344, inputs/issues/344.md:213
**Checked:** 2026-10-06T16:25:48.911632+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** The bot migration preserves Blitterbot and standing fork push identity; current git origins use the blitterbot SSH alias. No sanitized repositories×permissions×expiry inventory plus tested mail-reminder receipt was located in the project audit inputs.

**Refutation attempted:** A successful prior push proves usable Git authentication, not API permission scope or expiry notification. No secret token was read or printed.

**Notes:** Credential operations metadata remains a release-process item; the API-switch problem is separate.

**Gaps:** Locate or record non-secret permission/expiry metadata and the configured reminder evidence. Do not send mail or change tokens without the applicable named authorization.

### AC-I344-L214

> A workflow grep finds no `pull_request`, `pull_request_target` or `workflow_run` job with `runs-on: self-hosted`; a trigger dry-run from a throwaway fork schedules no self-hosted job.

**Source:** #344, inputs/issues/344.md:214
**Checked:** 2026-10-06T16:25:48.911661+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Fresh grep of all workflow files shows every runs-on is GitHub-hosted ubuntu; validate-pull-request and its reusable freeze check are ubuntu-24.04. No self-hosted label exists.

**Refutation attempted:** Read reusable workflow routing as well as direct PR jobs; disabled ai-usage is not an active workflow. A throwaway-fork scheduling experiment receipt was not located.

**Notes:** Source-level unsafe routing is absent; historical end-to-end dry-run clause remains unproved.

**Gaps:** Retain the trigger dry-run or explicitly reconcile it to current fully hosted routing; repeat full isolation/scheduling proof before any self-hosted runner is introduced.

### AC-I344-L215

> Isolation: `sudo -u runner test -r <path>; echo $?` prints `1` for each secret path; a canary read alerts; `sudo -u runner id` shows no `docker`; `sudo -u runner sudo -l` is empty; `sudo -u runner test -r /var/run/docker.sock` fails; the setuid audit is recorded. If any check fails, the runner is shown disabled.

**Source:** #344, inputs/issues/344.md:215
**Checked:** 2026-10-06T16:25:48.911689+00:00
**Verdict:** SKIP ○

**Evidence:** D-WORKFLOW-119 conditions the trust boundary on self-hosted runner introduction; all current workflow jobs target hosted ubuntu. Infrastructure topology is later under D-WORKFLOW-113.

**Refutation attempted:** No local runner-user sudo/secret access test was run, and source routing alone is not a claim about organization runner registration.

**Notes:** Not applicable to the present local-build/hosted-CI execution path. Keep the checks mandatory before enabling a self-hosted runner; no runner-is-disabled assertion is invented.

### AC-I344-L216

> The build container is mirrored under fork control; the build invocation references it by `@sha256:`; `docker inspect` or a build-log line shows that digest consumed.

**Source:** #344, inputs/issues/344.md:216
**Checked:** 2026-10-06T16:25:48.911708+00:00
**Verdict:** PASS ✓

**Evidence:** Cold consumed-container.json records configured ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39 and identical consumed image digest, running as1000:1000. Frozen14 inputs bind that same digest.

**Refutation attempted:** Checked consumed image ID as well as a tag/name string; namespace migration did not silently select a different container.

**Notes:** No current registry probe is claimed; retained executed build is the evidence.

### AC-I344-L217

> A source-tarball archive index lists every fetched tarball with its hash, in fork-owned storage inside the backup scope.

**Source:** #344, inputs/issues/344.md:217
**Checked:** 2026-10-06T16:25:48.911724+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Actual14 source-inventory10 records568 roots,583 components and525 install stamps with zero inventory errors; exact source archives are hashed and retained in the shared cache and immutable input records.

**Refutation attempted:** An inventory is not a complete publicly retrievable corresponding-source bundle. Fourteen component licence metadata gaps remain, and off-host backup/restore infrastructure is explicitly deferred.

**Notes:** Source input custody for engineering QA passes; publication/backup-scope completion is distinct.

**Gaps:** Finish component dispositions and the retrievable corresponding-source package before release; preserve the deferred Infrastructure topology boundary rather than claiming an off-host backup exists.

### AC-I344-L219

> The candidate store path and its `flock` wrapper are in place; the upstream base commit is recorded as frozen.

**Source:** #344, inputs/issues/344.md:219
**Checked:** 2026-10-06T16:25:48.911741+00:00
**Verdict:** PASS ✓

**Evidence:** tools/rasteratops-candidate-store uses fcntl.flock LOCK_EX, temporary staging, source/destination digest comparison, read-only files and atomic rename to sha256/<manifest>. Fresh initial audit verify accepted all19 current bundle files. Retained preflight controls reuse same input, preserve changed-input bundle and reject corrupted image bytes. D-WORKFLOW-111 records upstream freeze.

**Refutation attempted:** Read verifier’s manifest digest, unexpected file, symlink, size and hash checks; confirmed corruption returnedFAIL rather than trusting directory naming.

**Notes:** Read-only ownership is an accidental-write guard; explicit local owner chmod is not claimed cryptographically impossible.

### AC-I344-L220

> The freeze is in force with the emergency exception written. -- D-WORKFLOW-111, 2026-10-01: `upstream/next` at `9fd38fa870` (fetched 2026-09-29 11:02 UTC); the exception is a security fix for a matrix target, cherry-picked by a register row.

**Source:** #344, inputs/issues/344.md:220
**Checked:** 2026-10-06T16:25:48.911758+00:00
**Verdict:** PASS ✓

**Evidence:** D-WORKFLOW-111 states exact9fd38fa87094d4f0e956d03ac6c660fe4fd5e9d6 freeze and the named security-fix exception. Fresh merge-base of frozen14 and upstream/next returns that exact base.

**Refutation attempted:** Older merge commits in ancestry predate the freeze and are not mistaken for new post-freeze merges.

**Notes:** Current package refreshes do not imply an upstream distribution merge.

### AC-I344-L228

> A cold `GENERIC_X64` build exits `0` with `DISTRONAME` set and `DISTRO=ROCKNIX` retained (or the split's completed build-and-boot log, if P0 supplied a reason); the build log is archived with the manifest; the concurrency setting is recorded.

**Source:** #344, inputs/issues/344.md:228
**Checked:** 2026-10-06T16:26:58.914568+00:00
**Verdict:** PASS ✓

**Evidence:** Actual cold-01 sourceb137d8c3, global24 workers, pinned container and manifestc83828fa are retained with642/642 jobs and build/inner/watcher rc0. Full216844873-byte build log lives in immutable bundle22533e35. Later independently copied/requalified14 has its own642/642 four-channel rc0 record.

**Refutation attempted:** The original outer tool session returned143 with no outer.rc; retained outer-session.json does not conceal it. Actual command completion, checksummed outputs and exited owner/container independently establish the build criterion.

**Notes:** Cold provenance belongs to cold01, not a falsely described cold14. Final14 has its own source manifest and qualification.

### AC-I344-L229

> The brand sweep reports zero unclassified hits against `NAMING.md` allowlist vN (N recorded); an injected old-logo frame fails the template match (threshold and bounding box recorded).

**Source:** #344, inputs/issues/344.md:229
**Checked:** 2026-10-06T16:26:58.914636+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Replacement09 sweep-09 reads57293 files and8603 classified contexts against NAMING v2 with zero FIX/UNKNOWN; ten scanner and60 context mutation controls pass. Current boot05 template matches1.0 and rejects12 old-logo/blank/wrong-size controls.

**Refutation attempted:** The broad installed sweep is bound to cf511 replacement09. Frozen14 changes proxy/native artifacts; exact current14 full-image classification receipt was not located. Unchanged artwork/source continuity alone is not a new whole-image sweep.

**Notes:** Current branding frames and changed-source review are supported; the literal complete-candidate sweep needs final refresh.

**Gaps:** Run/bind the complete artifact classification to the final repaired candidate before RC, retaining fixed allowlist/context provenance and all negative controls.

### AC-I344-L230

> The localisation reconciliation lists every touched `.po` and `.xml` entry, with no orphan.

**Source:** #344, inputs/issues/344.md:230
**Checked:** 2026-10-06T16:26:58.914666+00:00
**Verdict:** PASS ✓

**Evidence:** Sweep09 localisation.json pins ESf6f0c134 (same as frozen14), reconciles851 catalogue/95 XML entries,57 retired/two removed entries, zero unclassified and zero active orphans. Installed Tools XML parses and matches source; actual14 unchanged ES/theme/Tools hashes corroborate continuity.

**Refutation attempted:** Checked the actual report’s commit identities and orphan counts rather than only README. No later locale/XML source changes were found in09→14 product delta.

**Notes:** This verifies touched catalogue/XML reconciliation, not universal translation coverage; missing plain phone/finishing French strings remain a separate confirmed finding.

### AC-I344-L231

> The secret sweep reports counts only, all zero.

**Source:** #344, inputs/issues/344.md:231
**Checked:** 2026-10-06T16:26:58.914687+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Sweep09 reports zero unclassified credential-pattern matches;70 matches in20 files are reviewed public constants bound to exact source/hash proofs. Actual frozen14 input custody and public QA sanitation are retained.

**Refutation attempted:** The wording all counts zero is inaccurate for deliberate public-key/constant matches, and the full secret sweep is from09 rather than current14’s changed proxy artifacts. No secret exposure is demonstrated.

**Notes:** Counts-only reporting is preserved; no raw credential values were exposed during this review.

**Gaps:** Refresh the full scanner on final candidate bytes and state zero unclassified/private matches with explicit reviewed public false positives; reconcile the literal zero-all-counts checkbox.

### AC-I344-L232

> `tools/vm-qa` reads PASS bound to a candidate-store hash equal to the manifest hash, before and after the run.

**Source:** #344, inputs/issues/344.md:232
**Checked:** 2026-10-06T16:26:58.914713+00:00
**Verdict:** PASS ✓

**Evidence:** Actual14 qa-18/defaults/report.md identifies bundleb77e47e57a, source7afa9efcfc and all15 passing suites. qa-18/build.log:12–13 and243–244 verifies frozen inputs and candidate-store hashes before and after; initial independent audit reverified all19 bundle files.

**Refutation attempted:** Verified the reports name the immutable candidate, not mutable target outputs. Earlier failed QA owners and incorrect fixture baselines remain excluded.

**Notes:** Scoped suites passed; audit-discovered behavior gaps are not invalidated by a general PASS banner.

### AC-I344-L233

> The upstream base commit is unchanged since P1.

**Source:** #344, inputs/issues/344.md:233
**Checked:** 2026-10-06T16:26:58.914732+00:00
**Verdict:** PASS ✓

**Evidence:** Fresh git merge-base frozen7afa9efcfc and upstream/next returns exact9fd38fa87094d4f0e956d03ac6c660fe4fd5e9d6, matching D-WORKFLOW-111 and recorded manifest ancestry.

**Refutation attempted:** Distinguished older pre-freeze upstream merges in history from a new integration during qualification.

**Notes:** Package refreshes and the local overlay advanced without moving the upstream baseline.

### AC-I344-L234

> The RC2 guest's early signal is recorded (offered or not offered; the comparison result).

**Source:** #344, inputs/issues/344.md:234
**Checked:** 2026-10-06T16:26:58.914748+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** p0-updater.md explicitly derives no fork offering on RC2: it contacts ROCKNIX’s endpoint, has no semantic comparison and only accepts dates for forced selection. Actual retained RC2 upgrade proves the manual adoption route.

**Refutation attempted:** No retained live RC2 offered/not-offered network observation was located. Source analysis and manual staging do not establish a captured server response.

**Notes:** Branch B is already approved; do not contact a real update service merely to chase stale Branch A wording.

**Gaps:** Reconcile the early-signal clause to approved manual adoption or retain a bounded isolated old-client observation without altering a personal device.

### AC-I344-L235

> A draft release exists with only the X64 asset.

**Source:** #344, inputs/issues/344.md:235
**Checked:** 2026-10-06T16:26:58.914764+00:00
**Verdict:** SKIP ○

**Evidence:** Current M7 milestone explicitly maps #344 contract P2 draft/asset selection into current P5 under #265/#344 after P4 and device gates. Current bytes remain in immutable engineering candidate storage.

**Refutation attempted:** No draft-release API result is available or claimed. Successful fork code pushes are not release creation.

**Notes:** Expected later work, not a newly discovered P4 product defect; create only the concrete qualified draft at its ordered stage.

### AC-I344-L241

> The device image is built; the manifest's input block (distribution, ES and splash commits, container digest, source index) is diff-empty against P2's; the per-image `BUILD_ID` and hash are in the manifest and the candidate store.

**Source:** #344, inputs/issues/344.md:241
**Checked:** 2026-10-06T16:28:00.024923+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.

**Refutation attempted:** No current H700/Nova build or physical measurement is inferred from the successful GENERIC_X64 image. No device action or publication occurred during this audit.

**Notes:** Frozen-input H700 arm/aarch64 build and per-image manifest remains an existing ordered later gate, not a newly discovered P4 product failure.

### AC-I344-L248

> Branch B: `docs/releases/device-facts.md` carries the migration device's row showing the seven-step procedure completed; the fork-aware updater prints "manual update required"; a network capture shows no request to the upstream host; post-upgrade hashes equal the pre-upgrade ones; the fork-to-fork proof is written as the `0.0.2` gate.

**Source:** #344, inputs/issues/344.md:248
**Checked:** 2026-10-06T16:28:00.024998+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.

**Refutation attempted:** No current H700/Nova build or physical measurement is inferred from the successful GENERIC_X64 image. No device action or publication occurred during this audit.

**Notes:** Mandatory RG35XX SP manual migration, network and state-preservation proof; future fork-to-fork gate remains an existing ordered later gate, not a newly discovered P4 product failure.

### AC-I344-L254

> Every matrix target is built from P2's input set; the requalification check is diff-empty, or the X64 re-run is recorded.

**Source:** #344, inputs/issues/344.md:254
**Checked:** 2026-10-06T16:28:00.025028+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.

**Refutation attempted:** No current H700/Nova build or physical measurement is inferred from the successful GENERIC_X64 image. No device action or publication occurred during this audit.

**Notes:** Remaining supported matrix builds and source-set comparison remains an existing ordered later gate, not a newly discovered P4 product failure.

### AC-I344-L255

> Each asset's hash equals its manifest entry; each attached asset is under the recorded per-asset limit.

**Source:** #344, inputs/issues/344.md:255
**Checked:** 2026-10-06T16:28:00.025049+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Current immutable bundle manifests record x64 image2073512198 bytes and tar2074368000 bytes, both below the recorded2147483648-byte limit. Initial audit verifies their hashes against manifestb77e47e57a.

**Refutation attempted:** No H700 or Nova asset is attached or represented by these x64 hashes; per-asset checks must follow each later build.

**Notes:** Known P5 matrix completion, with current x64 integrity already verified.

**Gaps:** Verify every future device asset against its manifest and the publication-time host limit before attachment.

### AC-I344-L256

> The brand, secret, leak and localisation sweeps are re-run on every image with P2's PASS conditions.

**Source:** #344, inputs/issues/344.md:256
**Checked:** 2026-10-06T16:28:00.025068+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Existing sweep09 provides full brand/credential/localisation controls; current14 has exact payload/identity custody and unchanged locale source. Current P2 audit entries229/231 identify the missing renewed full scan on14 changed artifacts.

**Refutation attempted:** Old-image zero-unclassified results cannot simply be renamed as results for all later device images.

**Notes:** Current final-image refresh and later per-device execution are separately owed.

**Gaps:** Run all required sweeps on the repaired final x64 image and every device image before their attachment; retain original results and no broad allowlist exemptions.

### AC-I344-L257

> The per-SoC boot-artifact matrix is filled (upgrade against clean flash; downgrade safety); any target with a boot-chain delta has its device-facts smoke-test row before attachment.

**Source:** #344, inputs/issues/344.md:257
**Checked:** 2026-10-06T16:28:00.025087+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.

**Refutation attempted:** No current H700/Nova build or physical measurement is inferred from the successful GENERIC_X64 image. No device action or publication occurred during this audit.

**Notes:** Per-SoC clean/update/downgrade boot-chain comparison and smoke evidence remains an existing ordered later gate, not a newly discovered P4 product failure.

### AC-I344-L258

> The component inventory file has a disposition per item; the corresponding-source bundle is retrievable and hash-verified.

**Source:** #344, inputs/issues/344.md:258
**Checked:** 2026-10-06T16:28:00.025104+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Actual inventory10 contains583 mapped shipped components and568 source roots with zero source-inventory errors. The recorded qualification explicitly retains14 component licence-metadata gaps and says publication corresponding-source bundle is incomplete.

**Refutation attempted:** An upstream URL, shared source cache or successful package fetch alone does not demonstrate a retrievable complete corresponding-source release.

**Notes:** Existing P5 publication gate under D-WORKFLOW-121.

**Gaps:** Resolve all14 dispositions and produce/retrieve/hash-verify the corresponding-source bundle, including exact patches/build scripts, before release publication.

### AC-I344-L259

> The channel-separation demonstration is recorded: a draft, pre-release or CI candidate is not offered on the stable channel.

**Source:** #344, inputs/issues/344.md:259
**Checked:** 2026-10-06T16:28:00.025120+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Current updater shim returns1 for check and ES blocks automatic/forced update checks for pixelelated. P0 derives Branch B and shows RC2 does not query GitHub Releases; current candidate remains in immutable local storage.

**Refutation attempted:** No retained controlled end-to-end draft/pre-release/CI versus stable offering demonstration or guest network capture was found; source gating alone is not that requested experiment.

**Notes:** No new automated channel exists; keep this contract aligned with manual adoption rather than inventing an OTA service.

**Gaps:** Reconcile the demonstration to manual-update semantics or retain a bounded isolated test proving current query behavior before P5 closure.

### AC-I344-L260

> Each device asset has its smoke-test evidence recorded before attachment; untested assets remain held (D-WORKFLOW-120, supersedes the earlier Branch B disclosure alternative).

**Source:** #344, inputs/issues/344.md:260
**Checked:** 2026-10-06T16:28:00.025136+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.

**Refutation attempted:** No current H700/Nova build or physical measurement is inferred from the successful GENERIC_X64 image. No device action or publication occurred during this audit.

**Notes:** Per-device smoke proof before attachment; untested assets remain held remains an existing ordered later gate, not a newly discovered P4 product failure.

### AC-I344-L261

> The release notes carry the support matrix with per-device verification status, adoption instructions, the trust assumption, recovery, source links, lineage and non-endorsement (not "marks retained"), the cloud compatibility exception, and the redirect dependency.

**Source:** #344, inputs/issues/344.md:261
**Checked:** 2026-10-06T16:28:00.025151+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/milestone.md explicitly maps #344 contract P2b/P3/P4 to current M7.P5 after the fixes audit and capacity review. support-matrix.md and device-facts.md distinguish historic ROCKNIX observations from the unbuilt pixelelated device artifacts.

**Refutation attempted:** No current H700/Nova build or physical measurement is inferred from the successful GENERIC_X64 image. No device action or publication occurred during this audit.

**Notes:** Release/adoption/recovery/source/lineage/non-endorsement documentation remains an existing ordered later gate, not a newly discovered P4 product failure.

### AC-I344-L262

> The publication yes is recorded in the action log; otherwise the state reads "stopped at immutable candidate".

**Source:** #344, inputs/issues/344.md:262
**Checked:** 2026-10-06T16:28:00.025168+00:00
**Verdict:** PASS ✓

**Evidence:** Current readiness, milestone and all14 qualification records explicitly stop short of RC/device-ready/publication claims and identify immutable bundleb77e47e57a. Current git tag0.0.1 is absent. Standing fork-push permission is not recorded as release publication approval.

**Refutation attempted:** Checked that completed cleanup/build/QA and user permission to proceed are not being relabeled as approval to publish the release.

**Notes:** Audit continues actively. Stopped at immutable candidate describes publication state, not an owner request to pause audit work.

### AC-I344-L266

> Each #341 relaxation the release needs lands with a bidirectional test: the newly permitted pattern passes and the secret and PII fixtures are still blocked.

**Source:** #344, inputs/issues/344.md:266
**Checked:** 2026-10-06T16:28:00.025183+00:00
**Verdict:** SKIP ○

**Evidence:** The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.

**Refutation attempted:** No background experiment, new guard relaxation, fielded update or completed general retention policy is asserted. Current #461 capacity/retention review and measured #364 timing controls keep their own narrower scope.

**Notes:** Deferred any needed #341 secret/PII guard relaxation and bidirectional controls; no extra first-RC gate is inferred from its inclusion in the historical parent issue.

### AC-I344-L267

> The first merge-cadence run records divergence, patch-refresh and ES conflict numbers.

**Source:** #344, inputs/issues/344.md:267
**Checked:** 2026-10-06T16:28:00.025199+00:00
**Verdict:** SKIP ○

**Evidence:** The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.

**Refutation attempted:** No background experiment, new guard relaxation, fielded update or completed general retention policy is asserted. Current #461 capacity/retention review and measured #364 timing controls keep their own narrower scope.

**Notes:** Deferred first post-freeze merge-cadence cost report; no extra first-RC gate is inferred from its inclusion in the historical parent issue.

### AC-I344-L268

> The hosted-QA experiment log records N=10 boot and flow runs, the failure count and the transfer cost, with no timing claims.

**Source:** #344, inputs/issues/344.md:268
**Checked:** 2026-10-06T16:28:00.025213+00:00
**Verdict:** SKIP ○

**Evidence:** The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.

**Refutation attempted:** No background experiment, new guard relaxation, fielded update or completed general retention policy is asserted. Current #461 capacity/retention review and measured #364 timing controls keep their own narrower scope.

**Notes:** Deferred hosted QA ten-run feasibility and transfer-cost experiment; no extra first-RC gate is inferred from its inclusion in the historical parent issue.

### AC-I344-L269

> Redirect-sunset tracking records the fielded devices that have completed one fork-to-fork update.

**Source:** #344, inputs/issues/344.md:269
**Checked:** 2026-10-06T16:28:00.025231+00:00
**Verdict:** SKIP ○

**Evidence:** The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.

**Refutation attempted:** No background experiment, new guard relaxation, fielded update or completed general retention policy is asserted. Current #461 capacity/retention review and measured #364 timing controls keep their own narrower scope.

**Notes:** Deferred fielded-device redirect sunset after a fork-to-fork update; no extra first-RC gate is inferred from its inclusion in the historical parent issue.

### AC-I344-L270

> A QA-frame retention policy is written, and a one-sided regression limit for any timing gate.

**Source:** #344, inputs/issues/344.md:270
**Checked:** 2026-10-06T16:28:00.025247+00:00
**Verdict:** SKIP ○

**Evidence:** The exact source checkbox is under #344 contract P5 — Post-0.0.1 background; the current milestone explicitly preserves that as later work. D-WORKFLOW-111/116/117/122 retain the release freeze and future cadence/redirect conditions.

**Refutation attempted:** No background experiment, new guard relaxation, fielded update or completed general retention policy is asserted. Current #461 capacity/retention review and measured #364 timing controls keep their own narrower scope.

**Notes:** Deferred general QA-frame retention and one-sided timing policy; no extra first-RC gate is inferred from its inclusion in the historical parent issue.

### AC-I344-L276

> The feasibility proof on `GENERIC_X64` covers display ownership, compositing, focus, controller ownership and lifecycle when either process exits; any command interface is bound to localhost with the address recorded.

**Source:** #344, inputs/issues/344.md:276
**Checked:** 2026-10-06T16:28:00.025263+00:00
**Verdict:** SKIP ○

**Evidence:** The source checkbox is explicitly #344 contract P6 — Post-0.0.1 Step0 under D-WORKFLOW-102, separately owned by #336/#339/#346. Current M7 plan keeps the existing ES/RetroArch launch stack.

**Refutation attempted:** No experimental runner implementation or its test result is inferred from current emulator-exit or proxy preservation tests.

**Notes:** Deferred runner feasibility and ownership/lifecycle spike; outside the current fixes audit implementation surface.

### AC-I344-L277

> A background Tier 1 report covers the files Step 0 did not touch; the launch-slice review follows the spike.

**Source:** #344, inputs/issues/344.md:277
**Checked:** 2026-10-06T16:28:00.025277+00:00
**Verdict:** SKIP ○

**Evidence:** The source checkbox is explicitly #344 contract P6 — Post-0.0.1 Step0 under D-WORKFLOW-102, separately owned by #336/#339/#346. Current M7 plan keeps the existing ES/RetroArch launch stack.

**Refutation attempted:** No experimental runner implementation or its test result is inferred from current emulator-exit or proxy preservation tests.

**Notes:** Deferred background Tier1/launch-slice review; outside the current fixes audit implementation surface.

### AC-I344-L278

> The bidirectional RetroArch → runner → RetroArch interchange test (saves, states, auto-slot, pending achievements, queue location) passes before #336 Step 1.

**Source:** #344, inputs/issues/344.md:278
**Checked:** 2026-10-06T16:28:00.025292+00:00
**Verdict:** SKIP ○

**Evidence:** The source checkbox is explicitly #344 contract P6 — Post-0.0.1 Step0 under D-WORKFLOW-102, separately owned by #336/#339/#346. Current M7 plan keeps the existing ES/RetroArch launch stack.

**Refutation attempted:** No experimental runner implementation or its test result is inferred from current emulator-exit or proxy preservation tests.

**Notes:** Deferred RetroArch/runner bidirectional state interchange; outside the current fixes audit implementation surface.

### AC-I344-L299

> Each row above the owner approves is in `docs/decision-register.md` with its ID, and `tools/register-check` passes.

**Source:** #344, inputs/issues/344.md:299
**Checked:** 2026-10-06T16:28:00.025309+00:00
**Verdict:** PASS ✓

**Evidence:** The source issue maps approved fourteen-row decisions to D-WORKFLOW-115–126 and explicitly names superseded102/CLOUD158/P0 rows. Direct register reads match the approved changes; fresh tools/register-check exits0 with599 IDs, each once, and all live citations resolved.

**Refutation attempted:** Verified row10 was not adopted as drafted and did not reintroduce a second-human-owner requirement; later identity and namespace decisions refine earlier terms.

**Notes:** The mechanical check proves identifier/citation consistency; row content was separately read.


## Forward Audit Summary

Completed independently at 2026-10-06T16:28:47.044075+00:00. Prior per-criterion answer keys remain unopened at this boundary.

| Verdict | Count | Criteria |
| --- | ---: | --- |
| PASS | 204 | I320-L32, I320-L33, I320-L34, I320-L35, I349-L29, I349-L33, I349-L42, I349-L44, I392-L18, I392-L19, I392-L20, I421-L23, I421-L24, I421-L25, I376-L22, I376-L23, I376-L24, I376-L25, I381-L24, I381-L25, I381-L26, I381-L27, I356-L75, I356-L77, I356-L78, I380-L22, I380-L23, I380-L24, I391-L22, I391-L23, I391-L24, I407-L18, I407-L19, I350-L24, I350-L25, I350-L26, I350-L27, I350-L35, I350-L36, I352-L35, I352-L45, I352-L32, I363-L73, I363-L74, I363-L75, I363-L77, I379-L23, I379-L24, I430-L28, I430-L29, I430-L30, I363-L78, I363-L79, I363-L80, I363-L81, I363-L82, I353-L31, I353-L33, I353-L34, I353-L35, I353-L36, I364-L33, I364-L34, I364-L35, I365-L101, I365-L103, I365-L104, I365-L117, I365-L118, I390-L18, I390-L19, I390-L20, I365-L102, I377-L22, I377-L23, I377-L25, I366-L34, I366-L35, I366-L36, I366-L37, I401-L33, I401-L34, I401-L35, I401-L36, I429-L28, I429-L29, I429-L30, I430-L31, I429-L31, I351-L58, I351-L59, I351-L60, I351-L61, I362-L68, I362-L69, I362-L70, I362-L71, I462-L28, I462-L29, I462-L30, I462-L32, I361-L119, I361-L124, I408-L18, I408-L19, I408-L20, I384-L14, I384-L15, I384-L16, I451-L28, I451-L29, I451-L30, I457-L16, I457-L17, I457-L18, I457-L19, I361-L122, I414-L20, I414-L21, I414-L22, I452-L28, I452-L29, I452-L30, I386-L26, I386-L27, I386-L28, I386-L29, I361-L120, I361-L125, I332-L22, I332-L23, I424-L18, I424-L19, I424-L20, I424-L21, I436-L50, I436-L51, I436-L52, I436-L53, I454-L12, I454-L13, I454-L14, I455-L12, I455-L13, I455-L14, I310-L21, I310-L22, I310-L23, I310-L24, I433-L73, I433-L74, I433-L75, I433-L76, I447-L70, I447-L71, I447-L72, I447-L73, I447-L74, I447-L152, I447-L153, I447-L154, I327-L20, I327-L21, I327-L22, I357-L16, I337-L27, I359-L29, I409-L266, I409-L267, I409-L268, I465-L20, I465-L21, I465-L22, I465-L23, I465-L24, I465-L25, I337-L50, I337-L52, I354-L67, I354-L68, I361-L123, I383-L284, I409-L238, I409-L239, I409-L240, I409-L241, I344-L196, I344-L197, I344-L198, I344-L199, I344-L200, I344-L201, I344-L202, I344-L203, I344-L204, I344-L216, I344-L219, I344-L220, I344-L228, I344-L230, I344-L232, I344-L233, I344-L262, I344-L299 |
| PARTIAL | 36 | I349-L43, I352-L34, I352-L36, I356-L76, I363-L76, I379-L22, I353-L32, I353-L52, I377-L24, I462-L31, I361-L121, I337-L28, I337-L53, I359-L30, I337-L40, I337-L41, I337-L51, I354-L69, I354-L66, I383-L285, I383-L286, I383-L287, I409-L236, I409-L237, I409-L242, I344-L212, I344-L213, I344-L214, I344-L217, I344-L229, I344-L231, I344-L234, I344-L255, I344-L256, I344-L258, I344-L259 |
| FAIL | 3 | I352-L33, I352-L44, I351-L62 |
| SKIP | 18 | I349-L34, I337-L29, I344-L215, I344-L235, I344-L241, I344-L248, I344-L254, I344-L257, I344-L260, I344-L261, I344-L266, I344-L267, I344-L268, I344-L269, I344-L270, I344-L276, I344-L277, I344-L278 |
| UNTESTABLE | 0 | none |

**Overall assessment: FAIL — not RC-ready.** All261 forward criteria are independently graded; counts are criterion counts, not unique bugs. Two content-classification failures share #467; the French sign-in failure has an unpublished draft. The future-marker error-message defect #468 is PARTIAL because safe refusal works. Other PARTIAL entries include narrow measurement gaps, stale contracts, aggregate ongoing audit gates and already scheduled P5 work; they must not be counted as36 new product defects. Eighteen SKIP entries retain explicit later/superseded/inapplicable reasons.

## Coverage Boundary

**Examined:** frozen distro/ES/proxy and relevant package, identity, rendering, cloud and QA source; exact issue text; primary command logs and before/after controls; current source/bundle custody; selected installed VM behavior and direct full-panel images. Fresh executable checks include1719 script assertions,316 focused layout assertions,119 ES assertions, package checks, schema/proxy/dependency/UI guards, asset reproduction and invalid controls. Earlier executed evidence is accepted only with its actual input identity and named unchanged-source boundary.

**Deliberately not examined yet:** prior375/382/411 per-AC answers (Phase2.5 next); Phase3 supporting-history/doctrine synthesis; external reviewer opinion (Phase4.6 later). No new physical-device/personal-cloud action, token retrieval, unrelated cleanup or product mutation occurred. Post-0.0.1 runner/hosted-QA/cadence work and current P5 device/publication requirements remain explicitly separate.

**Dimensions not exercised:** actual installed125-game scan, a literal installed mid-copy kill, specific narrow manual chooser/hostname/settlement/shelf/retry predicates named in the ledger, the promised guest update-network capture and a renewed full final-image sweep. The API switch did not restore automatic approval authentication; host/network/provider commands failed before execution, with no bypass. No background audit worker exists. Continue serially into Phase2.5 under standing authorization.

## Prior-verdict cross-check

Completed 2026-10-06T16:34:36.604187+00:00. Independent261 verdicts were sealed at16:28:47UTC; prior answers first opened16:29:42UTC. No prior answer was used to derive Phase2. Full exact old/current criteria, evidence and reasons: `evidence/prior-verdict-comparison.json`.

The123 prior entries are compared individually below. Changed verdicts reflect new implementation/evidence or a stated scope revision; they are not silently rewritten historical outcomes. Two superseded clauses have no current checkbox. Prior numbering is not the current inventory: old353 comment criteria are explicitly mapped across their owning issues.

| Prior AC | Prior | Current AC and verdict | Relationship / explanation |
| --- | --- | --- | --- |
| 344-01 | PASS | I344-L196 PASS | Agreement |
| 344-02 | PASS | I344-L197 PASS | Agreement |
| 344-03 | PASS | I344-L198 PASS | Agreement |
| 344-04 | PASS | I344-L199 PASS | Agreement |
| 344-05 | PASS | I344-L200 PASS | Agreement |
| 344-06 | PASS | I344-L201 PASS | Agreement |
| 344-07 | PASS | I344-L202 PASS | Agreement |
| 344-08 | PASS | I344-L203 PASS | Agreement |
| 344-09 | PASS | I344-L204 PASS | Agreement |
| 344-10 | PARTIAL | I344-L212 PARTIAL | Agreement |
| 344-11 | PARTIAL | I344-L213 PARTIAL | Agreement |
| 344-12 | FAIL | I344-L214 PARTIAL | Changed; Source-level unsafe routing is absent; historical end-to-end dry-run clause remains unproved. |
| 344-13 | PARTIAL | I344-L215 SKIP | Changed; Not applicable to the present local-build/hosted-CI execution path. Keep the checks mandatory before enabling a self-hosted runner; no runner-is-disabled assertion is invented. |
| 344-14 | PARTIAL | I344-L216 PASS | Changed; No current registry probe is claimed; retained executed build is the evidence. |
| 344-15 | PARTIAL | I344-L217 PARTIAL | Agreement |
| 344-16 | SKIP | No current checkbox | Removed from current checkbox scope by D-WORKFLOW-113; #355 owns post-0.0.1 snapshot/restore drill. Prior SKIP stands; no current runtime claim. |
| 344-17 | PARTIAL | I344-L219 PASS | Changed; Read-only ownership is an accidental-write guard; explicit local owner chmod is not claimed cryptographically impossible. |
| 344-18 | PASS | I344-L220 PASS | Agreement |
| 344-19 | FAIL | I344-L228 PASS | Changed; Cold provenance belongs to cold01, not a falsely described cold14. Final14 has its own source manifest and qualification. |
| 344-20 | FAIL | I344-L229 PARTIAL | Changed; Current branding frames and changed-source review are supported; the literal complete-candidate sweep needs final refresh. |
| 344-21 | UNTESTABLE | I344-L230 PASS | Changed; This verifies touched catalogue/XML reconciliation, not universal translation coverage; missing plain phone/finishing French strings remain a separate confirmed finding. |
| 344-22 | UNTESTABLE | I344-L231 PARTIAL | Changed; Counts-only reporting is preserved; no raw credential values were exposed during this review. |
| 344-23 | UNTESTABLE | I344-L232 PASS | Changed; Scoped suites passed; audit-discovered behavior gaps are not invalidated by a general PASS banner. |
| 344-24 | PARTIAL | I344-L233 PASS | Changed; Package refreshes and the local overlay advanced without moving the upstream baseline. |
| 344-25 | PARTIAL | I344-L234 PARTIAL | Agreement |
| 344-26 | PARTIAL | I344-L235 SKIP | Changed; Expected later work, not a newly discovered P4 product defect; create only the concrete qualified draft at its ordered stage. |
| 344-27 | UNTESTABLE | I344-L241 SKIP | Changed; Frozen-input H700 arm/aarch64 build and per-image manifest remains an existing ordered later gate, not a newly discovered P4 product failure. |
| 344-28 | SKIP | No current checkbox | Branch A rejected by D-WORKFLOW-093; current contract retains Branch B. Prior SKIP stands; do not map an automatic adoption experiment to manual adoption. |
| 344-29 | UNTESTABLE | I344-L248 SKIP | Changed; Mandatory RG35XX SP manual migration, network and state-preservation proof; future fork-to-fork gate remains an existing ordered later gate, not a newly discovered P4 product failure. |
| 344-30 | UNTESTABLE | I344-L254 SKIP | Changed; Remaining supported matrix builds and source-set comparison remains an existing ordered later gate, not a newly discovered P4 product failure. |
| 344-31 | UNTESTABLE | I344-L255 PARTIAL | Changed; Known P5 matrix completion, with current x64 integrity already verified. |
| 344-32 | UNTESTABLE | I344-L256 PARTIAL | Changed; Current final-image refresh and later per-device execution are separately owed. |
| 344-33 | UNTESTABLE | I344-L257 SKIP | Changed; Per-SoC clean/update/downgrade boot-chain comparison and smoke evidence remains an existing ordered later gate, not a newly discovered P4 product failure. |
| 344-34 | UNTESTABLE | I344-L258 PARTIAL | Changed; Existing P5 publication gate under D-WORKFLOW-121. |
| 344-35 | UNTESTABLE | I344-L259 PARTIAL | Changed; No new automated channel exists; keep this contract aligned with manual adoption rather than inventing an OTA service. |
| 344-36 | UNTESTABLE | I344-L260 SKIP | Current device attachment contract supersedes the old disclosure alternative under D-WORKFLOW-120; P5 remains unexecuted, explicitly SKIP in this P4 audit. |
| 344-37 | UNTESTABLE | I344-L261 SKIP | Changed; Release/adoption/recovery/source/lineage/non-endorsement documentation remains an existing ordered later gate, not a newly discovered P4 product failure. |
| 344-38 | PARTIAL | I344-L262 PASS | Changed; Audit continues actively. Stopped at immutable candidate describes publication state, not an owner request to pause audit work. |
| 344-39 | SKIP | I344-L266 SKIP | Agreement |
| 344-40 | SKIP | I344-L267 SKIP | Agreement |
| 344-41 | SKIP | I344-L268 SKIP | Agreement |
| 344-42 | SKIP | I344-L269 SKIP | Agreement |
| 344-43 | SKIP | I344-L270 SKIP | Agreement |
| 344-44 | SKIP | I344-L276 SKIP | Agreement |
| 344-45 | SKIP | I344-L277 SKIP | Agreement |
| 344-46 | SKIP | I344-L278 SKIP | Agreement |
| 344-47 | PASS | I344-L299 PASS | Agreement |
| 337-01 | PASS | I337-L27 PASS | Agreement |
| 337-02 | FAIL | I337-L28 PARTIAL | Identity, splash and manual-update row now execute on the candidate. Contract now expressly asks for guest network capture; that narrow measurement remains absent. |
| 337-03 | SKIP | I337-L29 SKIP | Both skip the new public site under D-WORKFLOW-098; active documentation accuracy remains owed. |
| 337-04 | PARTIAL | I337-L40 PARTIAL | Agreement |
| 337-05 | PARTIAL | I337-L41 PARTIAL | Agreement |
| 337-06 | FAIL | I337-L50 PASS | Changed; Functional current identity passes. Reconcile stale criterion wording; no backward rename of organization or machine contracts. |
| 337-07 | FAIL | I337-L51 PARTIAL | Changed; VM adoption is qualified; H700 and later suffix removal remain planned release work. |
| 337-08 | FAIL | I337-L52 PASS | Changed; Separate boot status text is outside the wordmark; transparency is preserved in the canonical source. |
| 337-09 | PARTIAL | I337-L53 PARTIAL | Agreement |
| 354-01 | PARTIAL | I354-L66 PARTIAL | Agreement |
| 354-02 | PARTIAL | I354-L67 PASS | Changed; Uses unchanged cloud source from replacement09 and current14 upgrade evidence, with their actual image identities. |
| 354-03 | FAIL | I354-L68 PASS | Changed; A green existing suite is limited to its predicates; separately discovered #467/#468 remain valid audit findings. |
| 354-04 | PARTIAL | I354-L69 PARTIAL | Agreement |
| 349-01 | PARTIAL | I349-L29 PASS | Changed; Retained09 execution; ES and cloud-source continuity to14 is recorded separately. |
| 349-02 | PASS | I349-L33 PASS | Agreement |
| 349-03 | PARTIAL | I349-L34 SKIP | Changed; Explicitly outside this P4 product-fixes gate. Public documentation is still owed before the applicable publication gate; no site-completion claim. |
| 349-04 | FAIL | I349-L42 PASS | Changed; Foreign archive availability alone does not enable the UI row; the deliberately broader console fallback is a separate D-CLOUD-067 contract. |
| 349-05 | PARTIAL | I349-L43 PARTIAL | Both retain the exact foreign-only hostname measurement gap. Writer selection and compatibility are separately improved; console NEWEST fallback is deliberate, not a failed UI gate. |
| 349-06 | PARTIAL | I349-L44 PASS | Changed; The full proposed long string is not claimed to fit640px; documented size-aware wording preserves the meaning. |
| 350-01 | PARTIAL | I350-L24 PASS | D-CLOUD-167 reconciled the entry sequence; retained target frames now show opening scan, cancellation and options without overlap. |
| 350-02 | PARTIAL | I350-L25 PASS | Changed; Current wording includes the concrete reason and safe unchanged-state sentence. |
| 350-03 | PASS | I350-L26 PASS | Agreement |
| 350-04 | PARTIAL | I350-L27 PASS | Changed; The documented old brand name is historical; current rename is covered separately. |
| 350-05 | FAIL | I350-L35 PASS | Prior nested-writer defect #381 is fixed and installed seeded frames/readbacks cover both own and foreign archives; after-class content comparison is the approved contract. |
| 350-06 | PARTIAL | I350-L36 PASS | Changed; Clarity and fitting behavior follow the existing player-text policy. |
| 351-01 | PARTIAL | I351-L58 PASS | Changed; Frame review performed before this verdict; no mocked DOM screenshot claim. |
| 351-02 | PARTIAL | I351-L59 PASS | Changed; Two measured states, not inferred CSS alone. |
| 351-03 | PARTIAL | I351-L60 PASS | Actual target HTTP and navigator user-agent plus handset/640 frames now exist. Dropbox trust page specifically moved to optional #463 by owner D-QA-058; no provider claim inferred. |
| 351-04 | PARTIAL | I351-L61 PASS | Changed; English presentation passes; French completeness fails the separate criterion below. |
| 351-05 | PARTIAL | I351-L62 FAIL | Changed; This is a failed source/localization contract. No French-mode VM sign-in execution is claimed; add it to repair qualification. External tracker publication is temporarily blocked by approval-review sign-in failure. |
| 352-01 | PARTIAL | I352-L32 PASS | Changed; Content listing filtering itself is distinct from the broken location classification recorded at I352-L33/L44. |
| 352-02 | PARTIAL | I352-L33 FAIL | Changed; Existing D empty-folder frame is valid but insufficient for the broader no-known-content clause. Probe also exposes explicit-root recognition asymmetry. |
| 352-03 | PARTIAL | I352-L34 PARTIAL | Agreement |
| 352-04 | PARTIAL | I352-L35 PASS | Changed; Historical /ROCKNIX content fixture now uses canonical /pixelelated after migration. Physical Nova readback remains staging context, not a prerequisite for this VM-verifiable behavior. |
| 352-05 | PARTIAL | I352-L36 PARTIAL | Agreement |
| 352-06 | PARTIAL | I352-L44 FAIL | Approved automatic fallback replaces obsolete confirmation. Independent installed challenge proves unrelated configured folders prevent real fallback and explicit root content is missed: #467, rather than only missing UI evidence. |
| 352-07 | PARTIAL | I352-L45 PASS | Changed; This covers the empty configured folder fixture. The unrelated-subdirectory case is a separate in-flight executable check. |
| 353-01 | PARTIAL | I353-L31 PASS | Changed; Defaults follow D-WORKFLOW-144, and independent content choices follow #380. |
| 353-02 | PARTIAL | I353-L32 PARTIAL | Agreement |
| 353-03 | PARTIAL | I353-L33 PASS | Changed; The card and later dialog are separate observed surfaces. |
| 353-04 | PARTIAL | I353-L34 PASS | Changed; Physical-device repeat is later staging evidence; the named UI behavior is VM-verifiable. |
| 353-05 | PARTIAL | I353-L35 PASS | Changed; D-WORKFLOW-144 changes project spelling without reopening settled cloud behavior. |
| 353-06 | PARTIAL | I353-L36 PASS | Changed; The required supported adoption is ROCKNIX→pixelelated. |
| 353-07 | PARTIAL | I353-L52 PARTIAL | Agreement |
| 356-01 | FAIL | I356-L75 PASS | Changed; Only the implemented predecessor→2 transition is claimed, not arbitrary future version support. |
| 356-02 | PARTIAL | I356-L76 PARTIAL | Both PARTIAL but narrowed differently: numbered marker/fault/quiet-follow tests now exist; RC2 is not retroactively marker-aware. Actual future-marker refusal remains safe but reports missing folder (#468). |
| 356-03 | FAIL | I356-L78 PASS | Changed; Current canonical destination is pixelelated; historical Rasteratops paths occur only in old evidence. |
| 363-01 | FAIL | I363-L73 PASS | Original no-call wording contradicted D-CLOUD-170/172/173. Reconciled criterion prohibits networked layout preparation while retaining local list and legacy presence guard; fresh source-backed checks pass. |
| 363-02 | FAIL | I363-L74 PASS | Five-alternating-sample 30ms limit unchanged. Original59ms and later36ms failures retained; isolated actual candidate runtime07 measures272/244ms medians,28ms, with transferred bytes. |
| 363-03 | PASS | I363-L75 PASS | Agreement |
| 363-04 | PASS | I363-L76 PARTIAL | Changed; Folder-only scope passes; truthful refused-join explanation is affected by #468. |
| 363-05 | PASS | I363-L77 PASS | Agreement |
| 363-06 | PARTIAL | I363-L78 PASS | Changed; Automatic default migration is not confused with copying game files during pointer preparation. |
| 363-07 | FAIL | I363-L79 PASS | Changed; Continuous captures and prior primary visual manifest remain retained; fresh review sampled original E frames and read all I assertions. |
| 363-08 | PARTIAL | I363-L80 PASS | Changed; No physical radio claim is made by a VM network-link proof. |
| 363-09 | PARTIAL | I363-L81 PASS | Changed; Actual archive restoration is proved separately; this fixture isolates boot ordering. |
| 363-10 | PASS | I363-L82 PASS | Agreement |
| 364-01 | PASS | I364-L33 PASS | Agreement |
| 364-02 | PARTIAL | I364-L34 PASS | Changed; This is a stock-shaped configuration fixture, explicitly distinct from the separate actualRC2 update. |
| 364-03 | PARTIAL | I364-L35 PASS | Changed; Current evidence is identified runtime12; no new performance measurement is inferred from unrelated14 smoke. |
| 365-01 | PARTIAL | I365-L101 PASS | Changed; The table is a classified behavioral model. Newly found content recognition and refusal wording defects #467/#468 remain audit findings; this document criterion does not waive them. |
| 365-02 | FAIL | I365-L102 PASS | New actor×state map supplies208cells/210named assertions; fresh matching finds every name in the PASS log, with original old-code failures retained. |
| 365-03 | FAIL | I365-L103 PASS | Changed; The injected negative tests process reporting; it does not simulate a VM failure. Normal installed runtime evidence is separate. |
| 365-04 | PASS | I365-L104 PASS | Agreement |
| 366-01 | FAIL | I366-L34 PASS | Changed; Historical command and work-log21:58 retained; fresh full-suite run independently validates current guard. |
| 366-02 | FAIL | I366-L35 PASS | Changed; No backend listener is started by these path-query controls. |
| 366-03 | FAIL | I366-L36 PASS | Changed; Current14 separate three-protocol318 proof uses the renamed default; it is not substituted for the first-post-fix criterion. |
| 366-04 | UNTESTABLE | I366-L37 PASS | Changed; No live provider account or personal data involved. |
| 361-01 | PARTIAL | I361-L119 PASS; I361-L124 PASS | Owner explicitly chose current upstream D-WORKFLOW-138; frozen-source freshness proof now exists. No inference of latest beyond recorded00:42 query. |
| 361-02 | SKIP | I361-L120 PASS; I361-L121 PARTIAL; I361-L122 PASS; I361-L123 PASS | Refresh taken, so former conditional SKIP now applies. Patch/Linux/preservation/award/UI proofs pass; exact installed125-game whole-library proof remains PARTIAL. |
| 362-01 | PARTIAL | I362-L68 PASS; I362-L69 PASS; I362-L70 PASS | Refresh chosen and3.8.0 built/linked with WebKit2.54.1; exact source and recorded freshness now satisfy disposition/build contract. |
| 362-02 | SKIP | I362-L70 PASS; I362-L71 PASS | Refresh conditional now applies. Cold compilation, actual loaded-page30s RSS and1GiB responsiveness replace vague bound; local HTTP/TLS/redirect proven, provider-owned Dropbox page optional. |
| 353-C01 | PARTIAL | I409-L236 PARTIAL; I337-L41 PARTIAL | Comment-era reversal sweep now falls under rename reconciliation. PARTIAL persists for stale active contract and exact old56-path disposition map; protected upstream/compatibility/history must remain. |
| 353-C02 | PARTIAL | I365-L101 PASS; I365-L102 PASS; I353-L33 PASS | Current actor map and installed stock-shaped boot proof now distinguish absent GAMES/populated old root and delay offer until card clears; no silent old-root creation. |
| 353-C03 | PARTIAL | I363-L82 PASS; I379-L22 PARTIAL | Actual pair5n proves late saves survive refusal/follow/move; settings-only sibling now tested through restore/follow/settle. Exact setup-completion receipt still narrower PARTIAL. |
| 353-C04 | PARTIAL | I353-L52 PARTIAL | Shelf move proven in guest and fault/retry hashes; next installed conflicting-sync shelf placement remains unlocated, so PARTIAL persists. |

### Prior punch-list continuity

| Prior item | Current independent disposition |
| --- | --- |
| #382 PL001 / #376 legacy archive suffix | I376-L22–L25 PASS: production writer/reader, target restores and inherited RC2 archive. Current compatibility remains deliberate. |
| #382 PL002 / #381 nested writer directories | I381 criteria PASS; target selected names/frames and fresh regression controls. Distinct foreign hostname gap remains I349-L43. |
| #382 PL003 / #377 bucket failed-read false absence | Production predicates and target S3 restore fault/retry now pass. I377-L24 keeps exact host backup successful-retry/outcome receipt PARTIAL. |
| #382 PL004 / #379 settings-only settlement | Source/follow/settle/whole restore pass; I379-L22 keeps literal cloud_setup completion proof PARTIAL. No silent closure. |
| #382 PL005 / #380 explicit empty content root | Pointer-preservation fix passes. #467 finds a different downstream classifier defect; it does not invalidate preservation bytes. |
| #382 PL006 audit-document evidence specificity | Prior notes repaired. Current261 entries independently give artifact, attempted refutation and limits; no new product item. |
| #411 guarded host helper PL001–005 | Prior resolutions retained for Phase3 supporting-source/receipt review. No privileged operation is repeated or inferred from closed state. |

The historical#382/#411 disposition documents were read directly; fresh GitHub tracker readback is blocked before execution by approval-service authentication. Their earlier publication is not a fresh current-state assertion. No Phase7 outcome is inferred from memory.

### Disagreements carried forward

- Prior352 content checks were PARTIAL for missing candidate proof. Actual independent challenge now FAILs I352-L33/L44 (#467). This is newly established behavior, not a demonstrated regression date.
- Prior351 French was PARTIAL; source-backed approved-string comparison now FAILs I351-L62. Missing French was not newly introduced by the rename on the evidence read.
- Prior363-04 PASS becomes I363-L76 PARTIAL: safe join refusal is intact, but application rc4 is presented as a missing cloud folder (#468). The old host checks did not establish truth of the actual refusal frame.
- Historical no-call and unsupported old-build marker promises were reconciled to recorded decisions and actual capabilities. Scope changes remain explicit.
- Other changes principally close former missing-build/runtime evidence or preserve ordered P5 work as SKIP. No P5 device/publication work is declared complete.
