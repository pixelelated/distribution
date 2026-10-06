# Audit analysis — M7 P4 fixes (#383)

**Audit tracker:** [M7.P4 #471](https://github.com/pixelelated/distribution/issues/471) — open; remediation required.

**Date:** 2026-10-06
**Spec:** inputs/scoped-criteria.json; M7/#383 current P4 gate
**Commits:** distribution7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2;
ESf6f0c134212bc696f2f6a747c8d390a588f2f0ce;
proxy879b158995d412af434301ebdae581f66b8b6d57.
**Bundle:** b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1.
**Status:** primary synthesis; independent external opinion pending. No Phase5
punch list, audit completion, product fix or RC approval is implied.

## Executive Summary

The prior structural failures have substantial direct remediation evidence:
writer-shaped legacy archives restore correctly, numbered layout migration
survives tier/marker faults, settings recovery preserves a concurrent writer,
clean and actual RC2-upgraded VM paths pass, and current upstream proxy/native
changes retain cache/pending awards. Real award/flush and separate reconnect UI
proofs are qualified. The old ROCKNIX build history does not establish that all
these paths were previously sound; the audit distinguishes prior evidence,
changed code, changed fixtures and new observations.

The frozen candidate is **not RC-ready**. Eight verified product findings now remain (three primary and five from
independent review). The original three are: content-folder classification prevents discovery of valid content,
unsupported-layout refusal uses a false missing-folder explanation, and the
required phone/finishing French strings are not implemented. Precise missing
measurements and stale active contract text also remain; they are not36 distinct
product defects. Existing P5 device/source/publication work stays ordered after
P4 closure and capacity review. No product bytes changed during this audit.

Phase2 independently recorded261 criteria before opening prior answers. Phase2.5
compared all123 previous criteria; Phase3 covers30 canonical rules,74 distinct
blindspot entries and190 supporting-history criteria across55 issues. The
independent Anthropic Fable5.1/xhigh reviewer completed both sequential calls
through the Facilitator; their verified outputs and all primary grades follow below. This primary synthesis was settled before reviewer invocation. The token repair restored actual-host access at16:58UTC; the refutation repeat then completed on the build volume. Current external-review execution is recorded in the Phase4.6 section below.

## Acceptance-criteria scorecard

The exact criterion text/evidence/refutation is in02 and the machine ledger;
IDs below map one-to-one to those independently recorded entries. Counts include
historical and explicitly later clauses, so the percentage is a coverage metric,
not a release confidence score.

| Verdict | Count |
| --- | ---: |
| PASS | 204 |
| PARTIAL | 36 |
| FAIL | 3 |
| SKIP | 18 |
| UNTESTABLE | 0 |
| Total | 261 |

**Pass rate:** 204/261 (78.2%).

| ID | Criterion | Verdict | Notes |
| --- | --- | --- | --- |
| I320-L32 | `recordLastGood` is taken under the same lock as the read it records, or compares the live file's identity (size and mtime, or a hash) before publishing and skips when it changed: the `es-conf-tests` case `a script's newer good state published between the read and the record is not overwritten` seen to FAIL on the code before the fix and PASS after. | PASS | Host compiled test proves the synchronization branch, separately from the installed target evidence below. |
| I320-L33 | The `LockBusy` path does not publish a recovery record from a read it could not lock: a second `es-conf-tests` case, seen to FAIL first. | PASS | The guarded publication handles both recovery source cases; reading an unlocked snapshot is not treated as permission to write it. |
| I320-L34 | On a guest, a script write of `system.cfg` raced against the interface's recovery (a damaged live file restored at start-up while `set_setting` writes) leaves the last-good record at the script's newer state: the record's bytes compared after the race, in `tools/vm-qa`'s `last-good` suite or a proof script under `docs/qa-frames/`. | PASS | This is explicitly the replacement09 installed execution on byte-identical relevant current14 payloads, not a claimed new14 race run. Current14 default/RC2 qualification is evaluated separately. |
| I320-L35 | `docs/audits/2026_09_29-milestone-audit-of-the-313-fixes/05-punch-list.md` § Deferred cites this issue, and its Phase 7 row records the commit. | PASS | This criterion requires the old resolution row itself; no prior375/382/411 acceptance answer key has been opened. |
| I349-L29 | On the transfer page, the SETTINGS restore row's line under the label names the device the archive to be restored came from, read from the label in its file name (`backuptool` prints it; the interface reads it): a 640x480 frame from a `tools/vm-walks` walk shows `<DEVICE>, <DATE>` (D-CLOUD-164). | PASS | Retained09 execution; ES and cloud-source continuity to14 is recorded separately. |
| I349-L33 | `docs/es-menu-map.md` carries the SETTINGS row's two states, offered with the device and date or dimmed with `NO SETTINGS BACKUP FROM THIS DEVICE YET` (D-UI-039, D-CLOUD-162), and `tools/es-menu-map-check` passes in `tools/vm-qa`'s `menumap` suite. *(Rewritten 2026-10-01: the choice page it named is superseded.)* | PASS | The earlier choice-page wording is explicitly superseded in the criterion. |
| I349-L34 | The public page for cloud sync says the SETTINGS row restores this device's own newest backup and is dimmed when the cloud has none from it (docs follow-up with #42, `documentation-accuracy.md`). *(Rewritten 2026-10-01: a restore from another device is not offered.)* | SKIP | Explicitly outside this P4 product-fixes gate. Public documentation is still owed before the applicable publication gate; no site-completion claim. |
| I349-L42 | After the scan page (#350), the SETTINGS restore row is offered only when the cloud's Backups folder holds an archive whose label equals this device's `cloud_device_id --label`; with the QA cloud seeded with a foreign label only, guest d's 640x480 frame shows the row dimmed with its reason, and with its own label seeded the row is offered with `<DEVICE>, <DATE>` (D-CLOUD-164) under it. | PASS | Foreign archive availability alone does not enable the UI row; the deliberately broader console fallback is a separate D-CLOUD-067 contract. |
| I349-L43 | A restore never takes another device's archive by default: the cloud restore selects this device model's newest compatible archive and passes it to `backuptool`, and its journal line names the label it chose; the foreign-label case on guest d leaves `system.hostname` unchanged. | PARTIAL | Locate a separate retained foreign-only UI hostname comparison or execute that bounded assertion on an owned candidate guest. Carry the proof gap until resolved. |
| I349-L44 | The scan page's line reads, while it runs, the words approved for #350 (proposed: `CHECKING WHAT SETTINGS AND CONTENT YOUR CLOUD HAS FOR THIS DEVICE...`), and the outcome vocabulary when it ends (`es-player-text.md`); frames from the walk show both. | PASS | The full proposed long string is not claimed to fit640px; documented size-aware wording preserves the meaning. |
| I392-L18 | Empty/failed remote discovery produces a nonzero setup refusal for both transfer scripts, with unchanged pointers/payloads and no create-folder offer; before/after production-script receipts retained. | PASS | No empty prefix can make the later rclone path silently local. |
| I392-L19 | A writable local path supplied as the cloud path is not read or written when no remote is linked; configured-cloud controls continue to pass. | PASS | The fixture tests both empty config and failed discovery before path use. |
| I392-L20 | Candidate guest evidence records the refusal/outcome and unchanged bytes for direct and automatic calls. | PASS | Retained09 target execution plus fresh host regressions; no new14 target execution claimed. |
| I421-L23 | All four settings writers preserve restrictive input modes, including a private recovery record and permissive pre-existing temporary, with byte-correct set/delete/sort/pair operations; old-source controls fail and corrected controls pass. | PASS | The helper rejects a symlink temporary and invalid stat/chmod results; all four literal call sites were read. |
| I421-L24 | chksysconfig backup/restore retains the privacy of its source/destination; failures leave original published bytes and report failure. | PASS | The fixture invokes production functions and image BusyBox; installed runtime evidence separately confirms the target. |
| I421-L25 | Corrected image clean/actual-RC2 qualification plus installed settings-race/mode proof pass; exact hashes bind the new candidate and original02163 results remain retained. | PASS | Targeted09 execution is reused only for identical relevant installed bytes, with current14 clean/RC2 qualification named separately. |
| I376-L22 | A regression case runs the production reader with RASTERATOPS OS identity and selects the same-device legacy ROCKNIX archive; its negative control at the old commit fails. The suite's PASS lines and fixture bytes are retained. | PASS | The legacy suffix is a compatibility contract; ARCHIVE_OS_NAME remains ROCKNIX in backuptool. |
| I376-L23 | New/legacy same-device and foreign-device fixtures prove selection prefers this device model's newest compatible archive, the transfer-page SETTINGS row is gated on MINE (D-CLOUD-156/162), and the console retains its deliberate NEWEST fallback when only a foreign archive exists (D-CLOUD-067); selected names and restored sentinel hashes are retained. | PASS | Selection is newest matching label within the first nonempty directory, not globally newest across all directories (D-CLOUD-068). |
| I376-L24 | Local backup, pre-restore snapshot, revert and retention cases prove the documented legacy/new-name contract without dropping recoverable files; retained names and restored sentinel hashes are in the log. | PASS | Both suffixes retain three historical files plus the active recovery snapshot; normal backup subsequently retains the three histories. Actual target execution is retained; fresh host tests corroborate it. |
| I376-L25 | The final branded image's RC2 upgrade rehearsal preserves existing settings archives and restores them through the cloud and local recovery entry points; logs identify image hashes and the selected archives. | PASS | Runtime archive selection was executed on the explicitly named replacement09 image, not newly on14; unchanged archive payload and14 upgrade evidence are distinguished. |
| I381-L24 | A candidate guest creates a settings archive through production cloud_backup, then opens RESTORE FROM CLOUD; the scan selects the actual archive and a640x480 frame shows SETTINGS enabled with the approved device/date text. Archive path, scan facts and frame are retained. | PASS | The directly reviewed writer UI frame belongs to the recorded October3 candidate; subsequent writer-shaped execution is separate evidence. |
| I381-L25 | Production restore consumes exactly the archive the scan selected; sentinel hash and journal verify it. Current device, legacy device name, healed previous IDs, foreign-only and flat-root fixtures preserve the documented selection behavior. | PASS | The foreign fallback is console-only intentional behavior; empty MINE disables the UI. |
| I381-L26 | The old scan fails a regression using writer-shaped per-device directories; the corrected scan passes. Existing flat-root cases remain compatibility controls, not the only fixtures. | PASS | Writer-shaped directories are first-class fixtures. Flat-root cases remain compatibility controls. |
| I381-L27 | The final RASTERATOPS image also discovers legacy ROCKNIX-suffixed archives under those folders (#376), and main WebDAV/S3 plus pair migration suites remain green. | PASS | Historical RASTERATOPS identity wording is superseded by lowercase pixelelated D-WORKFLOW-144. Authenticated Dropbox remains explicitly outside this local protocol baseline. |
| I356-L75 | `cloud_migrate_layout` runs numbered steps from the marker's version to the build's, each with the move dialog, each copy-verify-delete, each a journal line naming the step; a `tools/pixelelated-vm-cloud-boundaries` case (paired with the retained MOVE UI proof) seeds layout 1 and ends at layout 2 with the marker written and nothing lost (hash list before and after). | PASS | Only the implemented predecessor→2 transition is claimed, not arbitrary future version support. |
| I356-L77 | Fault injection after each completed tier and at marker publication followed by retry preserves both sides, completes without duplicate/lost state, and lets a second guest follow; logs identify the numbered step and hashes. | PASS | This satisfies named operation-boundary faults. It does not prove SIGKILL during a copy or arbitrary power loss; #353 is graded separately. |
| I356-L78 | The step for `/GAMES` and `/ROCKNIX` is step 1 and is the one #353 ships; the design note lives in `docs/rasteratops/cloud-layout.md`. | PASS | Current canonical destination is pixelelated; historical Rasteratops paths occur only in old evidence. |
| I380-L22 | Regression fixtures distinguish missing CONTENT_REMOTE, explicit empty cloud root, a derived old Content folder and a named custom folder for join, follow, settle and apply; log records before/after values. | PASS | All16 matrix cases were executed on replacement10; source continuity to14 is retained. |
| I380-L23 | On GENERIC_X64, an explicit root holding ROMs/BIOS remains the selected location after a layout transition and the scan lists/restores the original sentinel; missing-key fixtures get the documented default. | PASS | Older actual root restore execution is distinguished from current-name16-case transition coverage and source continuity. |
| I380-L24 | The contradictory seeding/migration fixtures and state table agree on one representation without silently replacing a player-selected folder; existing content-root tests remain green. | PASS | No player-selected cloud root is silently replaced by a migration-derived Content path. |
| I391-L22 | Historical RC2/run101 controls reproduce all four failures before the fix, then recover every owned payload and complete marker publication; retained logs identify predecessor script hashes and before/after pointers/hashes. | PASS | run101 is historical host compatibility coverage; real candidate VM execution uses actual RC2-created states. |
| I391-L23 | Recovery remains interruptible and repeatable; controls retain custom content/root choices, refuse unmarked foreign destination conflicts, and preserve both versions when an allowed merge is required. | PASS | This is controlled operation interruption, not an arbitrary process/power-cut guarantee. |
| I391-L24 | Candidate VM/upgrade proof verifies the inherited partial state and its recovery, naming the image and showing payload hashes and the supported retry/move path. | PASS | Replacement09 runtime evidence remains valid for unchanged migration bytes through14; current14 actual RC2 upgrade is a separate26-assertion qualification. |
| I407-L18 | A focused old-code control observes the empty destination; corrected output clearly names the cloud root while retaining named-folder output. | PASS | The historical control extracts only the actual pointer writer; actual installed label proof is separately retained in replacement02 transitions. |
| I407-L19 | Explicit CONTENT_REMOTE remains empty after the actual transition and root ROM/BIOS restores remain byte-identical on the resulting image. | PASS | Follow/settle/apply are tested for value preservation even when they emit no content-pointer sentence. |
| I350-L24 | Opening BACK UP TO THE CLOUD or RESTORE FROM THE CLOUD opens CHECKING YOUR CLOUD before any options (D-CLOUD-167), with the live line and CANCEL as the one way out while it runs (D-UI-078); the options page follows when the listing is in. A `tools/vm-walks` frame sequence shows menu, scan page, options, and no frame with a card drawn over a dialog. | PASS | This is retained installed unchanged-ES evidence, with source continuity to14. |
| I350-L25 | When the comparison fails (the cloud unreachable: the dead port of `tools/cloud-test-backend`), the page says why in the outcome vocabulary (`COULDN'T FINISH - …`, `es-player-text.md`) and offers TRY AGAIN beside CLOSE; a frame shows it. | PASS | Current wording includes the concrete reason and safe unchanged-state sentence. |
| I350-L26 | `docs/es-menu-map.md` carries the page (D-UI-039); `tools/es-menu-map-check` passes. | PASS | No menu row changed during this audit. |
| I350-L27 | The interface edit passes `tools/es-syntax-check` before the pin moves, and `docs/cloud-sync-changelog.md` carries the change the day it lands. | PASS | The documented old brand name is historical; current rename is covered separately. |
| I350-L35 | The opening scan checks folder state, settings archives by label and content location before options; CONTINUE with content selected runs the second content scan in the selected classes (D-CLOUD-167); the options page on guest d lists only rows the scan found (a frame per seeded case: settings for this label, settings for a foreign label only, content under `/ROCKNIX/Content`, content nowhere). | PASS | Acceptance is established for the named seeded cases, not all possible cloud folder contents. |
| I350-L36 | Its live line says what it is checking in the words approved for it (D-CLOUD-164: `CHECKING WHAT SETTINGS AND CONTENT YOUR CLOUD HAS FOR THIS DEVICE...`); the string and its French land in the same commit (D-UI-051). | PASS | Clarity and fitting behavior follow the existing player-text policy. |
| I352-L34 | A CHOOSE CLOUD FOLDER page (the `GuiFileBrowser` pattern fed by `rclone lsf`, `es-native-ui.md` § Reusable precedents) sets `CONTENT_REMOTE` through `cloud_setup`, and the transfer page re-reads it; the walk's frames show the chosen folder and the journal shows the `Content path` line. | PARTIAL | Locate another executed manual chooser selection with selected-folder frame/journal, or add a focused installed UI assertion before closing this criterion. |
| I352-L35 | With `CONTENT_REMOTE` back at `/ROCKNIX/Content` and the QA cloud seeded with `Photos/` and `Documents/` at its root, CONTENT TO RESTORE on guest d lists only ROM systems and BIOS: the walk's 640x480 frame and the scan's output lines. (The Nova's own listing is re-read on its next staging, as a read, and noted here in a comment.) | PASS | Historical /ROCKNIX content fixture now uses canonical /pixelelated after migration. Physical Nova readback remains staging context, not a prerequisite for this VM-verifiable behavior. |
| I352-L36 | `docs/es-menu-map.md` carries the chooser (D-UI-039); `tools/es-menu-map-check` and `tools/vocabulary-check` pass; the cloud-sync page on the site says where the content folder is chosen (`documentation-accuracy.md`). | PARTIAL | Public cloud-sync page must describe folder selection before P5 publication (#42); do not claim it published from local map evidence. |
| I352-L45 | Only then, with nothing found under either, the chooser opens; a frame shows it with the QA cloud's root folders listed as folders to pick from, never as systems. | PASS | This covers the empty configured folder fixture. The unrelated-subdirectory case is a separate in-flight executable check. |
| I352-L32 | `cloud_content_restore --scan` lists a pre-tier folder only when this device has a folder of that name under `/storage/roms` or the name is a supported system (`legacy_dirs` / `supported_systems`), the same rule `resolve_src` applies; a `tools/cloud-round-trip` case seeds `Photos/` and `Documents/` at the root and the scan's output carries neither line. | PASS | Content listing filtering itself is distinct from the broken location classification recorded at I352-L33/L44. |
| I352-L33 | When the content root holds no `ROMs/` and no known system folder, the page says so instead of listing: `YOUR CLOUD HAS NO ROMS OR BIOS AT <folder>.` / `CHOOSE THE FOLDER WHERE YOUR GAMES ARE?` (approved D-CLOUD-164), with a row that opens the folder chooser; a 640x480 frame shows it. | FAIL | Fix content-location classification to recognize actual supported content rather than any directory, then requalify the question/chooser and genuine-content controls on a rebuilt image. |
| I352-L44 | When the configured content root holds no `ROMs/` and no known system folder, the scan looks under the cloud root's `/ROCKNIX/Content` (the saves root's parent, `cloud_setup:629-631`) and, finding `ROMs/` or `BIOS/` there, uses that folder automatically and writes `CONTENT_REMOTE` (D-CLOUD-167, no USE IT confirmation); on guest d with `CONTENT_REMOTE=""` and content seeded under `/ROCKNIX/Content`, the frame sequence advances to the options and the journal shows the `Content path` line. | FAIL | Use a consistent game-content predicate for configured path, explicit root and fallback; retain unrelated-folder and valid-content controls. Recheck automatic choice with actual VM UI after the fix. |
| I356-L76 | A second guest on the same cloud takes the new marker at its next check with no dialog (its journal line), and the version-aware candidate offered a newer or malformed marker refuses unsupported writes/marker overwrite, showing a supported outcome (frame plus byte/pointer assertions). The separate RC2→candidate and mixed-installation receipts name the actual old binary and prove preservation; they do not claim RC2 implements this future protocol. | PARTIAL | The actual future-marker refusal frame misleadingly says COULDN’T FIND YOUR CLOUD FOLDER. cloud_scan discards the layout explanation, then maps application rc4 to the rclone missing-folder meaning. Preserve refusal safety but propagate a truthful reason before considering the full outcome accepted. |
| I363-L73 | No sync runs networked layout join/state/follow/migration preparation before transfer. The local `cloud_migrate_layout --superseded` string-list call and per-run legacy saves-folder existence probe required by D-CLOUD-172 remain permitted. `tools/last-good-scripts-test` reports both no-folder-check PASS lines; missing/unknown-root controls preserve D-CLOUD-172. This corrects the obsolete literal no-call wording against D-CLOUD-170/172/173, rather than removing the required absent-folder guard. | PASS | No extra recurring join/state/follow/move has been added; the absent-folder guard is not waived. |
| I363-L74 | An exit sync on an existing earlier `/ROCKNIX` folder and the current folder meets the unchanged five-alternating-sample median difference limit of30ms. Current candidate runtime07:272/244ms medians,28ms difference, real transferred bytes and zero migration preparation. #429 preserves the original36ms failed attempt and justifies the new fixture-bound qualification. | PASS | Earlier runtime07 result28ms and the original36ms failure are distinct retained attempts; this is runtime12 evidence, not a new14 performance execution. |
| I363-L75 | `cloud_migrate_layout --needs-step` answers with no network: 0 for an earlier default, not kept, with a remote set up; 1 for the current folder, a folder of the player's own, a kept one, or no remote; 2 for a conf it cannot read; rclone never starts (`tools/last-good-scripts-test` section aa, its `--needs-step` lines). | PASS | The predicate is exercised through host exact-source controls and whole-guest boot cases, not inferred solely from a comment. |
| I363-L76 | `cloud_scan --folder` is the folder item alone -- the join, the state, the quiet follow -- with no archive or root listing, the opening scan's files left as they were, and a refused join ending with its why and no state (section ab, its `--folder` lines). | PARTIAL | Resolve #468 reason propagation and requalify join/state/follow failure outcomes without changing folder-only listing scope. |
| I363-L77 | The transfer pages' scan still checks on every open (`tools/last-good-scripts-test` section ab). | PASS | No restored old done stamp is accepted as the next opening scan. |
| I379-L22 | A synthetic cloud with no save files and one same-device settings archive in each old layout keeps that archive discoverable after follow, settle, setup and transfer-page scan; VM log records pointer values, selected filename and restored sentinel hash. | PARTIAL | Locate a settings-only installed setup→scan→restore receipt or add it to the next bounded VM qualification, retaining old/new pointer and selected archive/sentinel evidence. |
| I379-L23 | Controls with save files, no archives, a kept layout and an explicit custom Backups folder preserve the documented behavior; each case has a reset and negative control on the old commit. | PASS | Existing no-archive/kept/classification controls preserve intentional policy; no OS-name assumption substitutes for archive discovery. |
| I379-L24 | The state/actor table includes saves-empty / Backups-nonempty independently of OS-name compatibility #376; main and pair migration suites remain green. | PASS | Protocol matrix and specific settings-only fixtures are both retained; current14 local runs do not relabel older pair execution. |
| I430-L28 | A fresh fixture waits outside measurement until the actual guest clock exceeds this layout's previous remote upload timestamp plus the comparison window; it asserts and retains the actual newly written mtime and preceding remote mtime before measuring the unchanged production command. | PASS | Remote upload mtime, not an assumed host/guest clock relation, determines readiness. |
| I430-L29 | Every sample retains timing, return code, local/remote hashes and timestamp facts before a possible assertion; failed output is captured privately/sanitized before teardown. | PASS | Raw synthetic fixture evidence is retained; credentials are not logged. |
| I430-L30 | A deliberately invalid timestamp boundary is rejected by the fixture predicate; fixed predeclared diagnostic batches transfer every changed save without forcing future mtimes, changing clocks or bypassing production comparison. | PASS | The threshold is unchanged; success is not achieved by future-dating the file. |
| I363-L78 | At the end of cloud setup, for a fresh install whose cloud holds its saves under an earlier folder, the step reads the move before the seeding (`tools/cloud-pair-migration` step 2's lines), and the frames show CHECKING YOUR CLOUD, the MOVE question, then CLOUD SETUP COMPLETE after the answer (`tools/vm-visual-qa` frames at 640x480). | PASS | Automatic default migration is not confused with copying game files during pointer preparation. |
| I363-L79 | At boot, for a guest whose conf names an earlier folder it has not kept, with a remote set up, the step comes up after the startup sync's card: CHECKING YOUR CLOUD, then the question; NOT NOW brings it back at the next boot; after MOVE the next boot raises nothing and the journal reads `nothing to settle` (frames at 640x480 and the journal, guest d). | PASS | Continuous captures and prior primary visual manifest remain retained; fresh review sampled original E frames and read all I assertions. |
| I363-L80 | Offline at boot (the guest's link cut on the QEMU monitor), the step asks `FINISH CLOUD SETUP` / `YOU'RE NOT ONLINE. CONNECT TO FINISH SETTING UP YOUR CLOUD FOLDER.` with CONNECT TO WI-FI and NOT NOW (a frame at 640x480). | PASS | No physical radio claim is made by a VM network-link proof. |
| I363-L81 | With a settings restore's marker and an earlier folder both set at boot (written on guest d, a named stand-in for a restore followed by an update), FINISH RESTORE PROCESS comes first with nothing over it; its FINISH brings the step once the screen is free; its LATER brings neither until the next boot (frames at 640x480). | PASS | Actual archive restoration is proved separately; this fixture isolates boot ordering. |
| I363-L82 | `tools/cloud-pair-migration` covers both later cases: the other guest's step follows after the move (step 5), and a guest that missed its step and backed up into the earlier folder has those saves merged by MOVE with nothing left behind (step 5n; 5m checks absent-root refusal/follow) -- its PASS lines. | PASS | Initial mixed-image/actual update phases1–4 and staged later-state phases5m/5n are distinct. |
| I353-L31 | A carried upstream `/GAMES` (a value no player typed) counts as no folder (D-CLOUD-161). At the end of cloud setup the seeding points it at `/pixelelated` and makes the three folders without asking (D-CLOUD-169: `tools/last-good-scripts-test`'s `--settle` lines); at boot the cloud folder step offers CREATE IT / CHOOSE A FOLDER / NOT NOW (D-CLOUD-170: guest d's epic proof, case E's frame), and so does a transfer page's scan, where CREATE IT writes the three `/pixelelated` paths (case B: the conf's three lines and `tools/cloud-test-backend ls`); with a `/GAMES` that holds files the dialog is the move naming `/GAMES` (case B0's frame). | PASS | Defaults follow D-WORKFLOW-144, and independent content choices follow #380. |
| I353-L33 | The folder is settled by the cloud folder step, at the end of cloud setup and at boot (D-CLOUD-170, #363), never by a sync: with the folder absent the startup and exit syncs end in the card's `SKIPPED - YOUR CLOUD FOLDER ISN'T SET UP YET` pointing at MANAGE CLOUD STORAGE (the startup stamp's `78 no-folder`, D-CLOUD-166), and 640x480 frames show the step at the end of setup (guest d's epic proof, case L) and at boot (cases E and I). | PASS | The card and later dialog are separate observed surfaces. |
| I353-L34 | The offer carries a third choice to pick a different folder (the folder chooser of #352), and its text has no icon or glyph drawn between its two sentences: a 640x480 frame from guest d and, when it is next staged, one from the device. | PASS | Physical-device repeat is later staging evidence; the named UI behavior is VM-verifiable. |
| I353-L35 | The words the offer uses are approved by the maintainer before the build (`player-language.md`): proposed `YOUR CLOUD HAS NO /ROCKNIX/Saves FOLDER YET.` / `CREATE IT`, `CHOOSE A FOLDER`, `NOT NOW`; their French lands in the same commit (D-UI-051). | PASS | D-WORKFLOW-144 changes project spelling without reopening settled cloud behavior. |
| I353-L36 | The default folder's name (`/ROCKNIX` today, D-WORKFLOW-101; `/pixelelated` proposed) is a register row on the maintainer's word, with D-WORKFLOW-101's mixed-installation test run before any default changes. | PASS | The required supported adoption is ROCKNIX→pixelelated. |
| I364-L33 | A backup on a carried `/GAMES` the cloud does not hold makes no `/GAMES`, sends nothing, prints `>>> offer create-saves-folder\|/GAMES` and ends 0, on a deliberate run and on the exit sync's `--automatic --recent` run. A `/GAMES` the cloud holds is backed up as before, and an absent current folder is still made (`tools/last-good-scripts-test` section ad, its four PASS lines; against the previous commit the first two FAIL). | PASS | No extra layout preparation replaces the bounded existence check. |
| I364-L34 | At a boot on a stock-shaped conf with nothing in the cloud, the startup card reads SKIPPED with `78 no-folder`, the QA cloud holds no `/GAMES` afterwards, and the cloud folder step offers CREATE IT (guest d's epic proof, case E: its PASS lines and `tools/cloud-test-backend ls`). | PASS | This is a stock-shaped configuration fixture, explicitly distinct from the separate actualRC2 update. |
| I364-L35 | The cost the listing adds to an exit sync on an earlier folder (59 ms on run 101's follow benchmark, against 16 ms on run 100) is kept with its reason or removed, decided against #365's folder table (D-WORKFLOW-134). | PASS | Current evidence is identified runtime12; no new performance measurement is inferred from unrelated14 smoke. |
| I353-L32 | An earlier `/ROCKNIX` folder gets one dialog, MOVE first (D-CLOUD-160): MOVE copies, verifies and deletes (the move page's frames on guest d; `tools/cloud-test-backend ls` shows `/pixelelated` whole and no `/ROCKNIX`; a kill during the copy leaves `/ROCKNIX` intact and a second MOVE completes it); another device on `/ROCKNIX` is re-pointed at its next cloud folder step or transfer-page scan with no dialog (`tools/cloud-pair-migration` step 5's journal line, D-CLOUD-170), one that wrote there first is merged by its MOVE (step 5m, D-CLOUD-168); KEEP USING leaves a device on `/ROCKNIX` for good; NOT NOW asks again at the next boot and the next transfer page. | PARTIAL | Locate an actual installed mid-copy kill receipt or add one on the owned VM/backend before closing this criterion; preserve source bytes and complete a secondMOVE. |
| I353-L52 | The move carries `Saves-replaced` (the set-aside of conflict losers beside the saves folder) to `/pixelelated/Saves-replaced` by the same copy, verify, delete, and nothing of ours remains under the old name afterwards: a `tools/last-good-scripts-test` case seeds a set-aside copy under the old layout and reads it back under the new one with the old folder gone; the round trip on the VM shows the sync's next set-aside landing under `/pixelelated`. | PARTIAL | Read a subsequent installed sync conflict/shelf path assertion, or retain that check during the next affected qualification. |
| I365-L101 | `docs/` carries the cloud folder's state table: each combination of conf state and cloud state, with what each actor does and the code line that does it. A walk of the table against the scripts lists no cell where two actors disagree, or names each disagreement as a decision. | PASS | The table is a classified behavioral model. Newly found content recognition and refusal wording defects #467/#468 remain audit findings; this document criterion does not waive them. |
| I365-L103 | The guest-d proof runs from `tools/` with a per-case state reset. Its exit code is non-zero when any check fails, seen once on a constructed failure. | PASS | The injected negative tests process reporting; it does not simulate a VM failure. Normal installed runtime evidence is separate. |
| I365-L104 | The retro file over runs 95 to 101 names each pattern with its guard, in `tools/`, `.githooks/` or `.claude/rules/`, as `ceremonies.md` asks of a blindspot. | PASS | Historical run counts remain labeled as historical. |
| I365-L117 | T17 fault-and-recovery VM case proves no misleading old-root seeding after failed settlement while the wizard can finish and the boot step can retry; retained log shows initial/final pointers, README locations and sentinel hashes. | PASS | Replacement09 execution; cloud scripts are byte-continuous through frozen14. No new14 UI execution is claimed. |
| I365-L118 | The new independent settings/content/archive dimensions and residual cases are represented in the table and promoted guest proof with reset, failing negative control and byte/pointer assertions; source-only hypotheses remain explicitly distinguished from executed failures. | PASS | I353-L32 separately records the missing mid-transfer kill proof; this does not invalidate the executed operation-boundary/dimension coverage. |
| I390-L18 | The fixture returns absence for a missing marker, returns stored marker bytes, and retains rcat bytes; targeted setup cases exercise both path and bucket modes. | PASS | Host fixture contract, not a production runtime claim. |
| I390-L19 | The complete host script suite has no regressions from the fixture correction; output and source revision retained. | PASS | Current count is1719, not the older historical count. |
| I390-L20 | The marker failure is recorded as fixture evidence, distinct from the reproduced production failures on #356. | PASS | Independent #468 remains a real installed UI reason defect, distinct from this repaired fixture. |
| I365-L102 | An actor × state coverage map names an executable assertion for every applicable T01–T26 cell (and a reason for each inapplicable one); `tools/last-good-scripts-test` runs those cases and passes. The previous commit fails the cases for the cells this work changed. | PASS | Fresh316 focused/1719 total checks pass; installed VM coverage is separately required and assessed. |
| I377-L22 | Production-path cases distinguish present, absent and failed parent listings; the failed listing cannot produce a create-folder offer. The old commit fails the regression case and the fixed commit's PASS lines are retained. | PASS | Unknown backup retains the existing fallback policy; the criterion forbids a false create-folder offer, not all backup attempts. |
| I377-L23 | The corresponding backup/restore bucket predicates are audited together; each failed-read fixture either passes a regression test or has a documented source-based reason it cannot reach the bad branch. | PASS | Separate host synthetic backup and installed S3 restore evidence preserve branch reachability distinctions. |
| I377-L24 | A whole-script synthetic bucket case with a reachable superseded literal tests the backup guard; an S3 QA fault case tests the ungated restore sibling. Each injects the failed parent listing, preserves sentinel hashes, reports the truthful outcome and succeeds after the fault is removed. The normal bucket-prefixed S3 backup fixture does not reach superseded_saves_setting and cannot count as that branch’s test. | PARTIAL | Add a reachable literal synthetic bucket backup failure→retry proof with distinct local/cloud hashes and truthful terminal outcome; retain actual S3 restore evidence. |
| I377-L25 | Existing absent-legacy-root refusal, current/custom-root creation and corrected pair-migration cases remain green. No extra recurring network probe is introduced without #364's timing acceptance being reverified. | PASS | Runtime09 source continuity to14 established separately; no new recurring network probe is introduced by the reviewed change. |
| I366-L34 | The stale-name check reads the list from `cloud_migrate_layout --superseded` and matches each entry as a whole path component; run against today's `tools/cloud-test-backend` (the bare `/GAMES` at line 806) it FAILs, and that failing run is recorded in the day's work log with its command (`engineering-practices.md` § Guards must fail closed). | PASS | Historical command and work-log21:58 retained; fresh full-suite run independently validates current guard. |
| I366-L35 | `tools/cloud-test-backend saves-remote` names, on every backend `tools/cloud-test-backend backends` lists, a folder that `cloud_migrate_layout --superseded` does not list: a check in `tools/last-good-scripts-test` that loops over the backends and PASSes. | PASS | No backend listener is started by these path-query controls. |
| I366-L36 | `tools/vm-qa`'s round-trip suite reads PASS in `report.md` on the first image built after the fix, and its `round-trip.log` names the new folder on the `SAVES_REMOTE` line. | PASS | Current14 separate three-protocol318 proof uses the renamed default; it is not substituted for the first-post-fix criterion. |
| I366-L37 | The S3 backend still gets a legal bucket name: `tools/cloud-round-trip --backend s3` against a QA guest logs `only 9/9` or no shortfall line for its saves upload. | PASS | No live provider account or personal data involved. |
| I401-L33 | Retain both original failures and code/history trace with actual guest evidence. | PASS | Original failures preserved without relabeling. |
| I401-L34 | Content network operations stop after bounded inactivity across provider SDK retries; progressing large transfers and cancellation remain functional. Actual-source stalled/progressing/failure controls prove the distinction. | PASS | Installed link-loss results below establish target behavior; host controls alone are not image qualification. |
| I401-L35 | WebDAV and S3 content backup/restore and affected scan cases pass real link-loss/retry/whole-byte/stamp checks under unchanged bounds on the replacement image. | PASS | Replacement09 execution is byte-continuous for these scripts through14; no repeated14 cut run claimed. |
| I401-L36 | Full affected host/package gates and image upgrade/clean qualification pass; source, artifact and remaining priorities are recorded. | PASS | Image/source/gate receipts are independently audited; candidate still blocked by new unrelated findings #467/#468. |
| I429-L28 | Retained original failure, all result channels and actual cleanup receipt; diagnosis names measured operations/conditions and distinguishes product cost from measurement noise. | PASS | Acceptance is distinct fresh runtime07 and later runtime12, not a renamed failed run. |
| I429-L29 | Any correction preserves missing/unknown-folder behavior with meaningful negative controls; no original frozen owner or source tree is edited. | PASS | Fresh owners preserve original failed backing/receipts. |
| I429-L30 | Exact candidate installed qualification meets the unchanged five-sample alternating median30ms limit, with every transfer byte verified and no migration preparation; retain all attempts and justify any repeat from the diagnosis. | PASS | Neither instrumented trace timings nor successful diagnostic substeps qualify the acceptance owner. |
| I430-L31 | Original failures and limited readonly-inspection evidence are retained, and fresh acceptance ownership remains distinct from diagnostics under #429. | PASS | The evidence explicitly limits what the read-only inspection proves. |
| I429-L31 | Installed identity/Tools consumer proof completes, and M7/checkpoint identify the accepted artifact and next dependency-gated owner. | PASS | This closes the original identity stage; later product defects still block overall readiness. |
| I351-L58 | 1: the Close control sits at the bottom of the page, below the note, with at least 2rem of space above it, and a tap asks a confirmation (the safe answer first) before Escape is sent; a 390 px headless-Firefox render shows the placement, and the page's load test (the harness from #330) passes. | PASS | Frame review performed before this verdict; no mocked DOM screenshot claim. |
| I351-L59 | 2: the state line has at least `.75rem` above and below it in both states (`Checking…`, `Connected.`); the two 390 px renders show it. | PASS | Two measured states, not inferred CSS alone. |
| I351-L60 | 3: the image ships `CHASSIS=handset` and the installed sign-in window sends Mobile Safari in both actual HTTP requests and `navigator.userAgent`. Replacement10 signin-ui14/15/16 each retain 40 passing checks and 15 reviewed frames; `signin-ui-14/build.log` lines41–47 and `artifacts/signin/all-local-navigator.json` prove this. Replacement14 readback under #462 confirms handset chassis and identical installed `cloud-signin-window`/`cloud_oauth` hashes (`signin-payload-continuity.json`). This reuses explicitly identified prior runtime evidence on unchanged bytes; it is not a new authenticated Dropbox execution. The provider-owned trust-page observation is #463, outside M7. | PASS | Identified prior runtime on unchanged installed bytes, as this reconciled criterion explicitly permits. |
| I351-L61 | 4: the finishing page carries the shared `STYLE` (the card, the `h1`, the note), reads as a success, and says what happens next; a frame from guest d's window shows it. | PASS | English presentation passes; French completeness fails the separate criterion below. |
| I351-L62 | Every string added has its French in the same commit where it is an interface string (D-UI-051), and `tools/vocabulary-check` passes on the scripts. | FAIL | Translate the newly required phone confirmation and finishing text through the selected system language, with EN/FR390px phone and actual installed finishing frames plus unchanged action/escape controls. |
| I362-L68 | Owner disposition recorded in D-WORKFLOW-138: refresh with existing functionality preserved. | PASS | Decision compliance is separate from complete runtime proof. |
| I362-L69 | Recipe uses verified 3.8.0 archive and explicit optional dependency settings; pkgcheck passes. | PASS | No product recipe changed during audit. |
| I362-L70 | Cold-build WebKitGTK 2.54.1 against libsoup 3.8.0; tools/fork-package-freshness exits 0 and the cut record names both inputs. | PASS | A new optional audit-time network check is pending approval-service authentication; this PASS is the criterion’s retained cold/cut proof, not a later latest-version claim. |
| I362-L71 | VM sign-in frames show the sign-in page in touch layout and finishing page; report the30-second combined RSS against D-WORKFLOW-048's approved loaded-page profile (about284MiB on the ordinary guest), explain any material growth, and prove the page loads in an actual1GiB guest without a kernel OOM or lost responsiveness; HTTP/TLS/redirect behavior works on the resulting image. This replaces the undefined “within its bound”: the existing tool has no numerical ceiling assertion. | PASS | Source/script payload continuity to14 established. Localization defect I351-L62 remains separate. |
| I462-L28 | Append a decision refining D-QA-017/D-QA-041 and update active rules, release readiness, tracker priorities, and resume handoff to make hosted accounts optional; source/readback evidence identifies the changed gate. | PASS | No relaxation of separate RA award proof. |
| I462-L29 | Frozen replacement14 has separate WebDAV, SFTP, and MinIO/S3 round-trip PASS reports; report exact cases, failures/skips and scope, with immutable image/source identity. | PASS | Three owned local protocols, no hosted-authentication inference. |
| I462-L30 | Retain fresh-owner harness seals, all four watcher result channels, final process/VM/backend cleanup readback, and sanitized evidence. Submission is not completion. | PASS | No original failed owner was overwritten. |
| I462-L31 | Preserve unverified Dropbox trust-page behavior in a milestone-less follow-up; reconcile #351's local browser criteria against existing artifacts without claiming an authenticated Dropbox test. | PARTIAL | Reconcile #351’s translation criterion and qualify its French repair; no hosted account is needed. |
| I462-L32 | Publish the explicit RA reset target and retain account-backed proof status separately; M7 continues P3 → approved P4 review → H700 arm then aarch64. | PASS | No device action or upstream/publication permission inferred. |
| I361-L119 | Owner disposition recorded in D-WORKFLOW-138: refresh current upstream, preserve functionality; prior pin proposal withdrawn. | PASS | Freshness is timed evidence, not a timeless statement. |
| I361-L121 | Indexed and unindexed whole-library scans retain truthful readiness, no total-library cap, interruption/retry, polite request pacing, and safe handling of server 429s; a synthetic library over 100 games proves the boundary. | PARTIAL | Execute the125-game indexed/unindexed and queued/429/retry controls against installed candidate modules/helper in an isolated VM, preserving pacing semantics and failure controls. |
| I361-L124 | tools/fork-package-freshness exits0 on frozen replacement14; freshness05/allfour0 and exact recipe/tool verification retained. Earlier failed13 and completed12 results remain their own evidence. | PASS | This criterion names frozen14 freshness05. New audit-time recheck is unstarted because approval-service authentication is still failing. |
| I408-L18 | Exact branded image reproduces missing automatic account discovery while an explicit-path control succeeds; no credential values enter evidence. | PASS | Historical intermediate brand was never fielded; current required transition remains ROCKNIX→pixelelated. |
| I408-L19 | A focused upstream-compatible patch recognizes both identities, preserves unrelated-platform behavior and configured overrides, and passes old-code negative controls. | PASS | Generic detector policy only, no behavior change on unrelated OS identities. |
| I408-L20 | The next image's packaged resolver automatically reads the canonical synthetic account, and existing cache/sign-in/base/subset queue state survives reopen. | PASS | Synthetic account/owned VM; separate RA33 proves actual provider award path. |
| I384-L14 | The original mapping fails and the patched mapping passes, with the upstream award-parity tests passing against the patched source. | PASS | Patch017 is retired because upstream implements the preservation; no duplicate backport remains. |
| I384-L15 | The candidate guest preserves each subset game ID and retains the queued award in the offline/proxy regression suite. | PASS | Syntheticprovider fixture, separate from genuine providerRA33. |
| I384-L16 | The candidate records the refreshed exact upstream pin, retired duplicate patch disposition and corresponding source containing the preservation fix. | PASS | Historical backport23tests remain dated original evidence. |
| I451-L28 | The original current-predecessor AttributeError and actual nonzero outcomes are retained. | PASS | This was a harness API failure, not data migration failure. |
| I451-L29 | Fresh execution passes all11 fork integration checks with both current7252fc and historical865e21 predecessor sources, preserving exact cache rows, queued base/subset awards, sign-in and legacy images across two reopens. | PASS | Hostupgrade fixtures separately backed by installed14 preservation22. |
| I451-L30 | The815 upstream Linux checks pass with the newly compiled libchdr607694c library and no native skips; exact source/helper hashes and actual terminal/cleanup receipts are retained. | PASS | Exact original host02andcurrentinstalled14 receipts remain separate. |
| I457-L16 | A regression fails on unchanged upstream at uptime0/5 and passes with the correction, including immediate consent changes and declined/unanswered controls; source/output hashes retained. | PASS | SourceSHA recorded for fresh unprivileged run; installedproof below. |
| I457-L17 | All selected upstream Linux tests and relevant fork integration tests pass with the narrow patch; package lint and schema guard pass. | PASS | Exact consumed source equivalence supports the retained full suite, with fresh currentintegration/consent checks. |
| I457-L18 | A fresh candidate contains the correction and the installed positive/negative/restart HTTP proof passes; loaded module hashes and actual completion/cleanup receipts retained. | PASS | No scheduler/UI/externalcollector claim; this is the specified installed reporting-function HTTPproof. |
| I457-L19 | A focused upstream patch plus reproduction/test instructions is prepared under #168; no upstream submission is implied by preparation. | PASS | Preparation does not imply submission/acceptance or outboundpermission. |
| I361-L122 | Existing cached sign-in, cache rows, ROM/image paths, pending base/subset awards and restart/reconnection survive an upgrade fixture; declined/unanswered telemetry never sends. | PASS | Owned syntheticfixtures; actualaccountRA33separatelyprovidesproviderconfirmation. |
| I414-L20 | Correct the compatibility note after verifying the exact pinned storage schema and caller assumptions; retain the equality and current-Storage test evidence. | PASS | Original414 fix and later452/879 comment refresh remain distinct historical events. |
| I414-L21 | An early package/preflight check fails for stale, missing or malformed recorded pins, passes the corrected package, and does not bypass the existing runtime/schema assertion. | PASS | The guard proves review-note agreement, not schema compatibility by itself. |
| I414-L22 | A replacement artifact includes the corrected script and passes the affected script suite; preserve the original failed candidate and its evidence. | PASS | Later proxy advances supersede the original pin with reviewed notes. |
| I452-L28 | Retain the actual old-note rc1 and source/schema byte comparison; review every direct SQL query against the selected schema. | PASS | Native/API interface refresh elsewhere is independently audited. |
| I452-L29 | Only the reviewed pin comment changes; package lint and existing offline schema preflight pass, while the original frozen input still fails. | PASS | No runtime source modified in this correction. |
| I452-L30 | The corrected source is published and a new sealed candidate input set passes the guard before any build or cache adoption. | PASS | Current package inputs are subsequently frozen879; this criterion concerns the original452 sequence. |
| I386-L26 | Each listed package has a verified current source and consumer-compatibility result; the recipes are refreshed, or an actual parent-coupled/version constraint is documented with evidence and a recorded disposition. No unexplained old-pin exception. | PASS | Source-current evidence is timestamped Oct3/cut Oct6 00:42. Native host probes do not claim hardware acceptance; actual target consumers/build receipts below. |
| I386-L27 | tllist's upstream version is resolved; any freshness resolver fix has a retained failing/passing control. UNKNOWN is not CURRENT. | PASS | Fresh live network check remains approval-service blocked; does not invalidate retained cut-time lookup. |
| I386-L28 | tools/pkgcheck passes for changed recipes; relevant consumers build and their VM acceptance receipts identify the exact candidate inputs. | PASS | #361/#362 runtime gates are independently graded; unchanged graphics dependency inputs carry their original cold compilation lineage. |
| I386-L29 | tools/fork-package-freshness exits 0 on the frozen candidate inputs and the source manifest names the verified archives/hashes. #361/#362 qualification remains separately required. | PASS | This is the frozen-cut freshness criterion, not a claim no upstream commit has arrived since. |
| I361-L120 | Every patch has a source-backed retained/rebased/superseded disposition and the final series applies cleanly. | PASS | Offsets are not fuzz; application and behavior evidence remain distinct. |
| I361-L125 | Remaining general-purpose fixes are reconciled with #168 for focused upstream contributions and regression tests. Ten tested drafts and interface-dependent dispositions are published in the linked contribution map; submission/acceptance remain separate. | PASS | No PR submitted/accepted; owner approval remains required for outward168contribution. |
| I332-L22 | A run of the Nova's `ledcontrol` on the host with `LED_PATH` pointed at a fixture: `brightness max\|mid\|min` writes three distinct `brightness` values to all eight LEDs (today it writes nothing); `battery`, `rgb` and `off` each leave the fixture in a stated state; the transcript filed here. | PASS | Hostfixture is explicitly requested by this criterion; no physical perceivedbrightness claimed. |
| I332-L23 | Choosing the value already selected in LED COLOR or LED BRIGHTNESS applies it (the row's callback runs on a press, not only on a change), shown by the fixture's files changing on a walk of the page on a guest with the quirk's script and a fake `LED_PATH`, or by a frame of the row plus the device's sysfs read after the press. | PASS | ExactunchangedLEDblock proof travels with sourcecontinuity; physical Nova illumination remains laterfact. |
| I424-L18 | Retain exact installed negative evidence and identify the source/environment boundary. | PASS | Oldfailed1e6a preserved, nohotpatchofthatimage. |
| I424-L19 | Add a focused regression that fails against the old launch/profile and proves OS_NAME reaches the actual child without unrelated identity/config changes. | PASS | Focusedcurrentchildcontrol succeeds; nofullhostnamespace identityrunclaimed. |
| I424-L20 | A replacement candidate's clean and retained-storage ES process receives pixelelated; actual menu and manual-update frames show the intended behavior. | PASS | ActualRC2upgradequalification chain separatelyretained; noautomaticupdatesrequested. |
| I424-L21 | Reconcile the sweep/identity checks so a correct os-release file alone cannot close this consumer criterion; retain the superseded artifact's results honestly. | PASS | Consumeridentitycontract is nowexplicitlytested atbothboundaries. |
| I436-L50 | Retained actual old-image reproduction binds the exception, process restart, missing capability and affected save callback. | PASS | #422 navigation timing remains a different scope. |
| I436-L51 | The corrected UI safely handles absent GPU governor capability while preserving selection/save behavior when capability exists; old failing and new passing controls are retained. | PASS | Source controls complement installed evidence below. |
| I436-L52 | Fresh and retained-state upgraded candidate guests return from System Settings without an ES process restart or exception, with actual menu frames and journal proof. | PASS | These are completed Oct6 QA18 observations, not a newly launched VM. |
| I436-L53 | Relevant syntax/package checks, candidate qualification, milestone order and checkpoint reflect the repair; #422 retains its separate navigation scope. | PASS | No RC assertion; later independent audit remains underway. |
| I454-L12 | Shared stop verifies the QEMU/owned-disk identity, waits for the same process to exit, fails boundedly on timeout, and retains the pidfile on failure. Deterministic tests retain delayed exit, wrong-process refusal and timeout controls. | PASS | A new host rerun remains approval-auth blocked; no bypass attempted. |
| I454-L13 | Actual upgraded QA15 disk is preserved and continued in a fresh owner; virgl and automatic software/Pixman checks and identity frames pass, with immediate stop/restart and actual terminal cleanup evidence. | PASS | QA15 original disk remains unchanged; follow-up scope is explicit. |
| I454-L14 | QA15's original failure,15default/26upgrade results, source/input identities and follow-up scope are retained; downstream unstarted owners bind the completed evidence chain explicitly. | PASS | Later14 full qualification is distinct from12 continuation. |
| I455-L12 | Root cause and first available historical evidence are recorded from actual fixture/system state; inherited coverage is not represented as a new branding regression. | PASS | Prior wrong frames and first comparison remain retained. |
| I455-L13 | Harness fails for a wrong/missing requested system before accepting the walkthrough, with a retained negative control. | PASS | Host parser fixture is supplemented by actual installed-system output below. |
| I455-L14 | Game Boy, NES and FBNeo each reach the intended manager on the exact candidate; actual frames and relevant aspect/orientation evidence retained without silently accepting a new baseline. | PASS | No silent new baseline or masked content error accepted. |
| I310-L21 | The mapping is named: a diff of the interface's `/proc/<pid>/maps` across one launch/exit cycle on the VM shows the 10 MiB region and the code that makes it (the region's flags and backing in the issue). | PASS | Mesa001 pairs executable arena/bookkeeping teardown and unwinds mmap/calloc/atexit failures. |
| I310-L22 | With the fix, `E1-pl069-control.sh`'s 10 cycles on the VM leave VmSize within one cycle's noise (under 1 MB of growth over 10) and VmRSS within 2 MB; equivalent launch/exit CSV and identity receipts filed under `docs/qa-logs/2026-10-03-launch-memory/`. | PASS | This is retained completed VM qualification with fresh arithmetic, not a new14 endurance execution. |
| I310-L23 | `E1-pl069.sh`'s 50 cycles with the exit sync on show the same flat VmSize, so PL-069's fix and this one are shown apart (the csv filed). | PASS | Even the stricter2048KiB RSS endurance condition passes; criterion originally required flat VmSize. |
| I310-L24 | Already written: nothing -- the growth lives in the running process and a restart clears it. | PASS | Historical already-written statement accurately limits impact to running-process memory. |
| I433-L73 | Retain original failed640/passed1280 matcher outputs, selected actual frames, capture hashes, all runner results and verified cleanup without conflating runner success with visual acceptance. | PASS | Command completion and visual acceptance explicitly differ. |
| I433-L74 | A bounded diagnostic distinguishes the failure cause using captured framebuffer/console facts and controls; no blind repeat-until-pass or threshold change. | PASS | Controlled console redraw explains mechanism; diagnostic COW is not candidate qualification. |
| I433-L75 | Any necessary product/harness fix has source-level evidence plus exact-candidate clean/retained-state boot proof at both sizes with unchanged matcher/negative controls. If product inputs change, freeze a new candidate and reconcile required qualification. | PASS | Separate renderer/sign-in qualification is not inferred from splash alone. |
| I433-L76 | Published evidence and the M7/#409/#422/#431 bodies identify the accepted replacement and safe downstream dependency binding before any successor predecessor proof advances. | PASS | Historical dependency corrections remain explicit; no successor is replayed. |
| I447-L70 | Original command success, failed local frame, five other reviewed frames, hashes and actual cleanup retained without relabelling. | PASS | Later09/10 stale-frame and12 observer failures also remain separate. |
| I447-L71 | New sealed capture path requires the existing visual tool's stable-screen result with a bound; unsteady/no-result cases cannot count as accepted captures. | PASS | Capture bound is fixed; no repeat-until-pass or forced resize. |
| I447-L72 | Fresh full sign-in proof passes actual redirect/UA/phone checks; six intended frames are semantically reviewed with stability receipts and actual result/cleanup agreement. Authenticated Dropbox trust remains separate. | PASS | English presentation verified; French source omission separately failsI351-L62. |
| I447-L73 | M7 and checkpoint identify accepted successor and the remaining1GiB/account/audit gates. | PASS | Tracker phase names and remaining gates remain explicit. |
| I447-L74 | Resolve the reproducible software-host stale/partial scanout on the declared software VM profile: fresh bounded native/host comparison and full sign-in semantic frames agree without forced resize/input, with actual old/partial/unsettled rejection, matching terminal results and cleanup. Canonical virgl success alone does not satisfy this criterion. | PASS | Software profile receives direct proof, not substitution with successful virgl. |
| I447-L152 | Rebuilt GENERIC_X64 clean/RC2-upgraded guests select Pixman without virgl and retain accelerated virgl; actual GPU features, compositor environment/logs and installed file hashes prove selection. | PASS | Unchanged10→14 renderer bytes explicitly carry earlier clean software tests. |
| I447-L153 | Selector boundary controls preserve explicit/unknown/non-virtio/multi-GPU cases; shared handheld startup bytes remain unchanged. | PASS | Selection fixtures do not by themselves prove compositor output; installed rendered proof above does. |
| I447-L154 | Relevant ES, emulator launch/exit, visual and time-to-play checks pass on the rebuilt software and accelerated profiles; original failures remain preserved. | PASS | Physical hardware performance remains a later named fact. |
| I327-L20 | A frame of the page at 640x480 from `tools/vm-walks/docs/retro-achievements.steps` on the first-release candidate image shows the explanation as short lines under the rows they explain (or one short block in the description size), each row visibly separated, the approved two paragraphs wrap within the panel without clipping (D-UI-119), and the frame filed under `docs/qa-frames/` beside the before frame. | PASS | This is explanation-page evidence, not offline award or reconnect evidence. |
| I327-L21 | `tools/es-menu-map-check` PASS, the French strings for every changed sentence in the same commit (D-UI-051), `tools/vocabulary-check` PASS. | PASS | Current source retains the same prose. Exact executed check receipts are in evidence/host-checks-01 and evidence/es-checks-02. |
| I327-L22 | The site's `retro-achievements/offline-achievements.png` retaken from the walk after the change. | PASS | Criterion asks for a retaken site asset. Public website publication remains a separate P5 gate with prior 403/404, not claimed here. |
| I357-L16 | No device on the candidate posts to `stats.rocknix.org`: the timer is not enabled in the image (`systemctl list-timers` on guest d after a boot shows no `rocknix-report-stats`), and the script, if kept, has no ROCKNIX endpoint (`grep -c rocknix.org` on the shipped script prints 0). | PASS | Earlier guest runtime evidence is attributed to its actual image; not reported as a new14 timer execution. |
| I337-L28 | A GENERIC_X64 image boots under the new name with its own splash and logo, `OS_NAME` read from `/etc/os-release`, the manual-update row visible, and no automatic upstream update request in the captured guest network evidence (frame/readback/capture filed here). | PARTIAL | Retain a bounded guest network observation covering automatic startup/update query paths, with a positive capture control, or explicitly reconcile the criterion to the stronger scoped evidence accepted by the owner. |
| I337-L27 | The register row that calls the direction (D-WORKFLOW-081's answer) names the fork's name and the licence terms it keeps (GPL-2 and MIT kept whole; the CC BY-SA attribution line; no ROCKNIX images). | PASS | No legal interpretation beyond verifying the project’s recorded policy and source text. |
| I359-L29 | A register row records the artwork licence and whether a trademark policy exists; `LICENSE.md`'s branding section names the fork's terms and `TRADEMARK.md` exists or the row says why not (`tools/vocabulary-check` and the licence text in the image's `/usr/share/licenses` agree: a `grep` on the image's SYSTEM). | PASS | Registration is deferred #360; current trademark policy exists without claiming registered status. |
| I409-L266 | Saved specification and editable master explicitly name Tiny5 Duo LCD; recorded font hash matches the existing approved face. | PASS | Default python lacks fontTools; the existing /tmp/pixelelated-fontenv interpreter supplies the documented4.66.1 dependency. No download or font substitution. |
| I409-L267 | Six outlined SVGs and two monochrome variants reproduce from the pinned font/palettes; exact RGB555 colors, alpha gaps, orientation and hard boundaries pass artifact checks. | PASS | Six multicolor and two monochrome products are preserved. Runtime’s NanoSVG-compatible flattened path asset is separately verified, not confused with the portable clipped master. |
| I409-L268 | Retained light/dark/midtone/saturated and small-size proofs demonstrate the portable assets; runtime integration remains separately tracked before the image freeze. | PASS | Portable design proofs are not asserted as device rendering tests. |
| I337-L29 | The approved placeholder site under the fork domain carries lineage/attribution and release/adoption links; its build/retrieval receipt is filed here. A full site is later scope (D-WORKFLOW-098). | SKIP | Stale contract and P5 deployment follow-up; do not claim a deployed site or add unapproved content. Reconcile the issue body during punch-list disposition. |
| I337-L53 | The release notes and the site's ssh page say the ssh password is unchanged in 0.0.1 (D-WORKFLOW-129, #358): the notes file's line and the docs PR. | PARTIAL | Write and publish the accurate fork release/adoption and SSH documentation before distribution to players; keep site access403/404 disposition explicit. |
| I359-L30 | The release notes' lineage and non-endorsement paragraph (#344 P4) points at the same terms. | PARTIAL | P5 release notes must state lineage/non-endorsement and link the same installed project terms. |
| I465-L20 | A reusable harness loads settings before ES starts, verifies the unchanged installed ES/proxy/ctl identities, and records a real interface address disconnect/reconnect. | PASS | Dedicated synthetic QA fixture; no real account or physical network operation. |
| I465-L21 | English/French sending and sent outcome frames at640x480 and1280x960 show readable correctly bounded cards, matched to pending counts, actual installed-flusher loopback receipts and `last-sync-link` records. | PASS | Local HTTP provider verifies actual installed flusher/UI composition. Real RetroAchievements acceptance is separately established by RA33, not by these synthetic cases. |
| I465-L22 | A controlled refused send retains pending state and produces the bounded failure/retry outcome; empty/repeated link transitions do not invent another successful send. | PASS | Failure case is English640 only as specified; full four-profile failure localization is not claimed. |
| I465-L23 | Every frame claim is directly reviewed; original failures are retained. The standard watcher, four terminal result channels and actual owned guest/provider cleanup are verified. | PASS | Connected standard watcher was consumed; no off-session notification claim. |
| I465-L24 | The ordinary award harness starts ES with its updated settings and captures reconnect as well as exit events, without weakening its unearned/API checks. Changed harness behavior has VM evidence; the completed RA33 account proof remains immutable. | PASS | Future ordinary award run still needs an unearned achievement; no new reset consumed for this audit. |
| I465-L25 | Publish exact evidence and reconcile #361/M7 coverage. Begin the approved #383 P4 fixes audit only after the remaining software qualification is satisfied. | PASS | This audit later found separate content/sign-in issues. They do not falsify the narrow reconnect-card qualification. |
| I337-L40 | A fresh guest on the candidate, signed in to the QA cloud, creates and uses `/pixelelated/{Saves,Backups,Content}`: `tools/cloud-test-backend ls` after a backup and a saves sync shows the three folders and nothing under `/ROCKNIX`; `grep -rn ROCKNIX projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf*` prints nothing; `tools/vocabulary-check` passes. | PARTIAL | Amend the source predicate to check active path values while explicitly allowing the two archive-format comments; retain a named fresh-guest three-tier listing as the criterion’s exact artifact. |
| I337-L41 | Every `/ROCKNIX` cloud path in the interface and the scripts is listed by the sweep (`docs/rasteratops/p0-sweep-hits.txt`, rule `cloud-path`, 56 lines) and each is changed or marked history in the same commit; the sweep re-run on the candidate's tree lists none as current. | PARTIAL | Reconcile the old per-hit criterion to the current context-based source/artifact classification, or supply the explicit56-entry disposition map. Do not erase valid legacy readers to satisfy a blanket grep. |
| I337-L50 | `DISTRONAME="pixelelated"`: `os-release` reads `OS_NAME="pixelelated"`, the images are `pixelelated-<board>.<arch>-0.0.1.*`, the info page reads `OPERATING SYSTEM: pixelelated` (a 640x480 frame from guest d; `/etc/os-release` from the image's SYSTEM); repositories, packages and hosts stay lowercase `rasteratops`; the cloud folder is `/pixelelated` (D-CLOUD-158). | PASS | Functional current identity passes. Reconcile stale criterion wording; no backward rename of organization or machine contracts. |
| I337-L51 | The migration tar carries the suffix `-from-ROCKNIX` (`IMAGE_SUFFIX`), so its name passes the RC2 init's check (`init:882`): the built name is `pixelelated-H700.aarch64-0.0.1-from-ROCKNIX.tar` and `tools/vm-upgrade-rehearsal` from RC2's image applies it; the suffix is dropped in the build after 0.0.1 (D-WORKFLOW-128). | PARTIAL | Build the frozen H700 arm/aarch64 chain after P4/capacity gates, retain its actual named artifact and perform the separately authorized physical adoption check. |
| I337-L52 | The splash and the theme's logo carry the word mark alone until the icon arrives (D-WORKFLOW-130): the splash frame at boot and the theme's logo frame on guest d show the name in the chosen face and no pictorial mark. | PASS | Separate boot status text is outside the wordmark; transparency is preserved in the canonical source. |
| I354-L67 | The rehearsal (`tools/vm-upgrade-rehearsal`) from RC2's x64 image keeps every piece of state across the update (its PASS), and a stock-shaped conf carried across (`/GAMES`, nothing in the cloud) meets the cloud folder step at the boot after rather than a dialog from the startup sync: the startup stamp's `78 no-folder` and the step's CREATE IT offer in 640x480 frames (guest d's epic proof, case E; D-CLOUD-166, D-CLOUD-170). | PASS | Uses unchanged cloud source from replacement09 and current14 upgrade evidence, with their actual image identities. |
| I354-L68 | `tools/vm-qa` on the candidate passes every suite, `frame-diff` against the accepted baseline explains every changed frame by one of the children, `tools/vocabulary-check` and `tools/es-menu-map-check` pass. | PASS | A green existing suite is limited to its predicates; separately discovered #467/#468 remain valid audit findings. |
| I354-L69 | Every string the five children add is approved by the maintainer before the build and lands with its French (D-UI-051); `docs/cloud-sync-changelog.md` carries the changes the day they land (`change-log.md`); the site's cloud-sync page names `/pixelelated` (`documentation-accuracy.md`, with #42). | PARTIAL | Fix French phone/finishing surfaces under the recorded draft finding and verify both languages; reconcile/publish the cloud-sync site with the current default once the website destination/access is resolved. |
| I354-L66 | The mixed-installation test (`tools/cloud-pair-migration` on `tools/vm-pair`): guest a updated in place from RC2's image with a `/ROCKNIX` cloud, guest b a fresh install on the same QA cloud; for the default-derived fixture both confs end at `/pixelelated/{Saves,Backups,Content}`; separate populated/custom backup and explicit-root content fixtures retain their independent pointers and byte access, a save written on each arrives on the other, nothing was removed from `/ROCKNIX` before its verified copy, a guest that missed its step and wrote into the earlier folder is merged by MOVE (D-CLOUD-168), and the log names each step: its PASS lines, and its negative control on a build without the join (D-CLOUD-169) failing. | PARTIAL | Locate or retain the installed no-join mixed-pair negative, or reconcile the criterion to the named old-code and guest controls without relabeling them. |
| I361-L123 | Upstream Linux suites and fork proxy regression sections pass on the exact selected source; cold image build, tools/ra-offline-test and UI/progress/flush proof pass on the VM. | PASS | Indexed125-game performance proof is separately partial under I361-L121; this clause’s ordinary offline award/UI/flush proof is complete. |
| I383-L284 | #365's T01–T26 table maps each relevant actor/state cell to executable assertions or a justified inapplicable cell; #356 adds strict supported-version, numbered-step, marker-failure and interrupted retry/fleet controls; #320 has deterministic recovery-race controls; writer-shaped archive discovery is the first negative control. The promoted guest proof resets every case and exits nonzero on an injected assertion failure. | PASS | Coverage-map completeness does not erase behavior defects discovered outside its predicates. |
| I383-L285 | #376/#377/#379/#380/#381 and #365 settlement, #363 card ordering, #364 timing, #366 fixture defects have source fixes and retained passing/failing controls. Each owning issue carries its own evidence. | PARTIAL | Resolve confirmed product findings and exact child evidence gaps; update owning issue criteria/evidence and requalify affected frozen inputs before an RC. |
| I383-L286 | #361/#362/#386 input refresh and preservation checks pass; #310/#327/#332 carry-forward software criteria and host gates are resolved. #337's approved OS identity is integrated on the frozen upstream baseline. One recorded input set produces the candidate; clean install, RC2 upgrade, full VM QA, pair migration, visual and timing evidence identify that build. | PARTIAL | Close current product/evidence punch list, preserve exact input custody through any fixes, and rerun affected VM gates. |
| I383-L287 | The code-auditor review of the fixes includes the approved independent other-lab model through the Facilitator; findings are resolved and any resulting product changes rebuilt and requalified before an RC claim. | PARTIAL | Complete the serial primary stages, restore tool approval authentication, run verified other-lab review, disposition/refute findings, then fix/rebuild/requalify before any RC claim. |
| I409-L236 | Record the new identity hierarchy and lowercase default in the append-only decision register; reconcile active naming policy, instructions, milestone order and open issue criteria. Retain historical attribution and closed titles. | PARTIAL | Reconcile affected open acceptance text and clearly label the first-sweep status as historical; preserve closed titles and original evidence. |
| I409-L237 | Classify old-name references across active source, tools, sibling repos and infrastructure; retain an explicit compatibility/history/owner/character allowlist. Canonical org URLs and relevant Git remotes resolve to pixelelated; the personal account is verified as rasteratops and the bot identity is unchanged. Historical maxengel-owned forks retain their verified locations; rasteratops/rocknix.org returned 404 and no transfer is assumed. | PARTIAL | Retain a sanitized repo/account ID and canonical URL readback once approval authentication works; keep website destination/access unresolved rather than silently selecting another repository. |
| I409-L238 | Distribution/ES/splash/theme and licence/trademark source use the agreed lowercase identity and Tiny5 Duo LCD wordmark alone. Exact source pins and existing lint/syntax/identity guards pass; obsolete brand references are classified rather than globally replaced. | PASS | No icon or alternate font is introduced; current input and source hash continuity are retained. |
| I409-L239 | New setup defaults to /pixelelated; configured /ROCKNIX and /GAMES selections and archive discovery remain usable. Isolated controls and candidate clean/upgrade receipts demonstrate no silent cloud relocation or archive loss. | PASS | The separate #467 content-presence classifier defect does not demonstrate relocation or archive loss; it remains a blocker under its own criteria. |
| I409-L240 | The update asset naming/procedure satisfies the ROCKNIX RC2 predecessor init check, and the new image accepts future pixelelated updates. Retain actual upgrade evidence for ROCKNIX RC2. | PASS | D-WORKFLOW-128 makes suffix removal/fork-to-fork runtime proof a later release gate; actual RC2 adoption is qualified now. |
| I409-L241 | Verify the build-container namespace/digest and source fetches. A monitored build with tested delivery produces a newly frozen pixelelated artifact; retain the image identity/manual-update/brand/licence/source/localisation checks and affected default/upgrade/visual/performance evidence. Do not rename or relabel replacement02. | PASS | This passes engineering build qualification scope, not P5 publication readiness. |
| I409-L242 | Expand the approved P4 primary plus Fable5.1 Facilitator fixes review to this transition; resolve findings and renew affected artifact proofs before calling the image an RC. | PARTIAL | Finish serial review, obtain verified independent opinion, resolve all blocker findings and renew affected installed proofs after changes. |
| I344-L196 | `docs/rasteratops/p0-read.md` exists with one decision per row of the base plan's §2, each citing `path:line`, and its first line answers three questions: does `DISTRO=rasteratops` imply a new directory; do image and asset file names derive from `DISTRO`, `DISTRONAME` or something else; what does `rocknix-update` match on. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md` | PASS | Historical P0 read, not current runtime qualification; current lowercase scope is D-WORKFLOW-144. |
| I344-L197 | The sweep report from the base plan's §1.15 command lists every hit in exactly one of four classes (display text; machine identity; persisted paths and network names; boot and storage contracts); every class 2 to 4 hit is marked KEEP, and any non-KEEP carries `path:line`, a reason and a reference to a recorded yes. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-sweep.md and p0-sweep-hits.txt` | PASS | Historical snapshot51f78ac5b4; later approved cloud-default changes supersede its KEEP choices and need current criterion reconciliation separately. |
| I344-L198 | The updater note records the mechanism, the asset pattern, redirect handling, any distro-name check, draft and pre-release handling, the manual route, and the comparison function's result on `0.0.1` against RC2's version string as a table, and names Branch A (unaided over-the-air) or Branch B (manual adoption). -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-updater.md` | PASS | Later D-WORKFLOW-128 chooses suffix placement; historical updater note is not a current OTA implementation claim. |
| I344-L199 | `BUILD_ID`'s derivation is quoted with `path:line`, with its timestamp and host dependence stated. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § BUILD_ID` | PASS | Manifest binds more than BUILD_ID, which alone does not identify all consumed inputs. |
| I344-L200 | `docs/rasteratops/support-matrix.md` exists with the columns target/arch, physical boards, QA guest, clean install, upgrade, boot medium and boot-chain deltas, recovery method, attachment status; the mandatory migration device is marked. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/support-matrix.md` | PASS | Creation/content of the matrix passes; current device qualification is still later work. |
| I344-L201 | `df -B1` of the build volume and `du -sb` per existing root are recorded, with the forecast as line items (old roots, new roots, source archives, VM overlays, retained candidates). -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Disk` | PASS | Historical capacity only. Current measured cleanup/retention and #461 capacity gate supersede this forecast before device builds. |
| I344-L202 | The per-asset size limit is recorded with its source and date; the ES licence is quoted from the ES tree; the splash repository's owner is recorded; the digest behind the build container's `:latest` is recorded; `DISTRO_SRC` or its equivalent is recorded. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts` | PASS | The criterion is the P0 record. Publication must revalidate platform limits and actual asset sizes; no current internet lookup was possible here. |
| I344-L203 | D-WORKFLOW-088 (present in the register; absent from the run's packet) is cited, and Choice 2 of #338 is labelled or struck. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts` | PASS | No new infrastructure is created by this audit. |
| I344-L204 | `git log -- distributions/` shows no identity commit and `git tag` shows no `0.0.1`. -- done 2026-09-30, `224b73ea54`: `docs/rasteratops/p0-read.md § Platform facts` | PASS | Historical sequencing gate passes; current identity commits are intended. |
| I344-L212 | The three repositories are transferred and `rocknix-splash` forked; the ES and splash commits are pinned; every recipe URL and `git remote -v` in every worktree shows fork addresses. | PARTIAL | Retain sanitized canonical repository/account readbacks and update the criterion to distinguish project origins from upstream source URLs and intentional remotes. |
| I344-L213 | The bot token's scope inventory (repositories × permissions × expiry) is recorded and an expiry reminder is configured on the mail channel. | PARTIAL | Locate or record non-secret permission/expiry metadata and the configured reminder evidence. Do not send mail or change tokens without the applicable named authorization. |
| I344-L214 | A workflow grep finds no `pull_request`, `pull_request_target` or `workflow_run` job with `runs-on: self-hosted`; a trigger dry-run from a throwaway fork schedules no self-hosted job. | PARTIAL | Retain the trigger dry-run or explicitly reconcile it to current fully hosted routing; repeat full isolation/scheduling proof before any self-hosted runner is introduced. |
| I344-L215 | Isolation: `sudo -u runner test -r <path>; echo $?` prints `1` for each secret path; a canary read alerts; `sudo -u runner id` shows no `docker`; `sudo -u runner sudo -l` is empty; `sudo -u runner test -r /var/run/docker.sock` fails; the setuid audit is recorded. If any check fails, the runner is shown disabled. | SKIP | Not applicable to the present local-build/hosted-CI execution path. Keep the checks mandatory before enabling a self-hosted runner; no runner-is-disabled assertion is invented. |
| I344-L216 | The build container is mirrored under fork control; the build invocation references it by `@sha256:`; `docker inspect` or a build-log line shows that digest consumed. | PASS | No current registry probe is claimed; retained executed build is the evidence. |
| I344-L217 | A source-tarball archive index lists every fetched tarball with its hash, in fork-owned storage inside the backup scope. | PARTIAL | Finish component dispositions and the retrievable corresponding-source package before release; preserve the deferred Infrastructure topology boundary rather than claiming an off-host backup exists. |
| I344-L219 | The candidate store path and its `flock` wrapper are in place; the upstream base commit is recorded as frozen. | PASS | Read-only ownership is an accidental-write guard; explicit local owner chmod is not claimed cryptographically impossible. |
| I344-L220 | The freeze is in force with the emergency exception written. -- D-WORKFLOW-111, 2026-10-01: `upstream/next` at `9fd38fa870` (fetched 2026-09-29 11:02 UTC); the exception is a security fix for a matrix target, cherry-picked by a register row. | PASS | Current package refreshes do not imply an upstream distribution merge. |
| I344-L228 | A cold `GENERIC_X64` build exits `0` with `DISTRONAME` set and `DISTRO=ROCKNIX` retained (or the split's completed build-and-boot log, if P0 supplied a reason); the build log is archived with the manifest; the concurrency setting is recorded. | PASS | Cold provenance belongs to cold01, not a falsely described cold14. Final14 has its own source manifest and qualification. |
| I344-L229 | The brand sweep reports zero unclassified hits against `NAMING.md` allowlist vN (N recorded); an injected old-logo frame fails the template match (threshold and bounding box recorded). | PARTIAL | Run/bind the complete artifact classification to the final repaired candidate before RC, retaining fixed allowlist/context provenance and all negative controls. |
| I344-L230 | The localisation reconciliation lists every touched `.po` and `.xml` entry, with no orphan. | PASS | This verifies touched catalogue/XML reconciliation, not universal translation coverage; missing plain phone/finishing French strings remain a separate confirmed finding. |
| I344-L231 | The secret sweep reports counts only, all zero. | PARTIAL | Refresh the full scanner on final candidate bytes and state zero unclassified/private matches with explicit reviewed public false positives; reconcile the literal zero-all-counts checkbox. |
| I344-L232 | `tools/vm-qa` reads PASS bound to a candidate-store hash equal to the manifest hash, before and after the run. | PASS | Scoped suites passed; audit-discovered behavior gaps are not invalidated by a general PASS banner. |
| I344-L233 | The upstream base commit is unchanged since P1. | PASS | Package refreshes and the local overlay advanced without moving the upstream baseline. |
| I344-L234 | The RC2 guest's early signal is recorded (offered or not offered; the comparison result). | PARTIAL | Reconcile the early-signal clause to approved manual adoption or retain a bounded isolated old-client observation without altering a personal device. |
| I344-L235 | A draft release exists with only the X64 asset. | SKIP | Expected later work, not a newly discovered P4 product defect; create only the concrete qualified draft at its ordered stage. |
| I344-L241 | The device image is built; the manifest's input block (distribution, ES and splash commits, container digest, source index) is diff-empty against P2's; the per-image `BUILD_ID` and hash are in the manifest and the candidate store. | SKIP | Frozen-input H700 arm/aarch64 build and per-image manifest remains an existing ordered later gate, not a newly discovered P4 product failure. |
| I344-L248 | Branch B: `docs/releases/device-facts.md` carries the migration device's row showing the seven-step procedure completed; the fork-aware updater prints "manual update required"; a network capture shows no request to the upstream host; post-upgrade hashes equal the pre-upgrade ones; the fork-to-fork proof is written as the `0.0.2` gate. | SKIP | Mandatory RG35XX SP manual migration, network and state-preservation proof; future fork-to-fork gate remains an existing ordered later gate, not a newly discovered P4 product failure. |
| I344-L254 | Every matrix target is built from P2's input set; the requalification check is diff-empty, or the X64 re-run is recorded. | SKIP | Remaining supported matrix builds and source-set comparison remains an existing ordered later gate, not a newly discovered P4 product failure. |
| I344-L255 | Each asset's hash equals its manifest entry; each attached asset is under the recorded per-asset limit. | PARTIAL | Verify every future device asset against its manifest and the publication-time host limit before attachment. |
| I344-L256 | The brand, secret, leak and localisation sweeps are re-run on every image with P2's PASS conditions. | PARTIAL | Run all required sweeps on the repaired final x64 image and every device image before their attachment; retain original results and no broad allowlist exemptions. |
| I344-L257 | The per-SoC boot-artifact matrix is filled (upgrade against clean flash; downgrade safety); any target with a boot-chain delta has its device-facts smoke-test row before attachment. | SKIP | Per-SoC clean/update/downgrade boot-chain comparison and smoke evidence remains an existing ordered later gate, not a newly discovered P4 product failure. |
| I344-L258 | The component inventory file has a disposition per item; the corresponding-source bundle is retrievable and hash-verified. | PARTIAL | Resolve all14 dispositions and produce/retrieve/hash-verify the corresponding-source bundle, including exact patches/build scripts, before release publication. |
| I344-L259 | The channel-separation demonstration is recorded: a draft, pre-release or CI candidate is not offered on the stable channel. | PARTIAL | Reconcile the demonstration to manual-update semantics or retain a bounded isolated test proving current query behavior before P5 closure. |
| I344-L260 | Each device asset has its smoke-test evidence recorded before attachment; untested assets remain held (D-WORKFLOW-120, supersedes the earlier Branch B disclosure alternative). | SKIP | Per-device smoke proof before attachment; untested assets remain held remains an existing ordered later gate, not a newly discovered P4 product failure. |
| I344-L261 | The release notes carry the support matrix with per-device verification status, adoption instructions, the trust assumption, recovery, source links, lineage and non-endorsement (not "marks retained"), the cloud compatibility exception, and the redirect dependency. | SKIP | Release/adoption/recovery/source/lineage/non-endorsement documentation remains an existing ordered later gate, not a newly discovered P4 product failure. |
| I344-L262 | The publication yes is recorded in the action log; otherwise the state reads "stopped at immutable candidate". | PASS | Audit continues actively. Stopped at immutable candidate describes publication state, not an owner request to pause audit work. |
| I344-L266 | Each #341 relaxation the release needs lands with a bidirectional test: the newly permitted pattern passes and the secret and PII fixtures are still blocked. | SKIP | Deferred any needed #341 secret/PII guard relaxation and bidirectional controls; no extra first-RC gate is inferred from its inclusion in the historical parent issue. |
| I344-L267 | The first merge-cadence run records divergence, patch-refresh and ES conflict numbers. | SKIP | Deferred first post-freeze merge-cadence cost report; no extra first-RC gate is inferred from its inclusion in the historical parent issue. |
| I344-L268 | The hosted-QA experiment log records N=10 boot and flow runs, the failure count and the transfer cost, with no timing claims. | SKIP | Deferred hosted QA ten-run feasibility and transfer-cost experiment; no extra first-RC gate is inferred from its inclusion in the historical parent issue. |
| I344-L269 | Redirect-sunset tracking records the fielded devices that have completed one fork-to-fork update. | SKIP | Deferred fielded-device redirect sunset after a fork-to-fork update; no extra first-RC gate is inferred from its inclusion in the historical parent issue. |
| I344-L270 | A QA-frame retention policy is written, and a one-sided regression limit for any timing gate. | SKIP | Deferred general QA-frame retention and one-sided timing policy; no extra first-RC gate is inferred from its inclusion in the historical parent issue. |
| I344-L276 | The feasibility proof on `GENERIC_X64` covers display ownership, compositing, focus, controller ownership and lifecycle when either process exits; any command interface is bound to localhost with the address recorded. | SKIP | Deferred runner feasibility and ownership/lifecycle spike; outside the current fixes audit implementation surface. |
| I344-L277 | A background Tier 1 report covers the files Step 0 did not touch; the launch-slice review follows the spike. | SKIP | Deferred background Tier1/launch-slice review; outside the current fixes audit implementation surface. |
| I344-L278 | The bidirectional RetroArch → runner → RetroArch interchange test (saves, states, auto-slot, pending achievements, queue location) passes before #336 Step 1. | SKIP | Deferred RetroArch/runner bidirectional state interchange; outside the current fixes audit implementation surface. |
| I344-L299 | Each row above the owner approves is in `docs/decision-register.md` with its ID, and `tools/register-check` passes. | PASS | The mechanical check proves identifier/citation consistency; row content was separately read. |

## Provisional findings

### F-01 — content discovery and restore disagree about what counts as content

**Severity: High. Category: Interaction Defect. Owner: cloud setup/restore.**
Issue#467; I352-L33 and I352-L44 FAIL. `cloud_setup:518–545` counts any directory
under nonempty CONTENT_REMOTE, but tests explicit account-root content against
`cloud_content_backup --list`, which requires local files. Unrelated Photos can
therefore count as content and suppress valid derived fallback; a fresh/empty
local library can miss actual ROMs/BIOS or a supported legacy game directory.

Actual unchanged candidate14 was probed with seven isolated synthetic WebDAV
clouds by `evidence/content-probe-01/probe.py` through its sealed monitored
`run.py`. The executed command is retained in `run.py` and owner receipts; do not
replay the completed owner. Three controls pass; four challenges fail:
`unrelated-configured` expects empty but gets ok;
`unrelated-configured-fallback` expects found-elsewhere but gets ok;
`tiered-explicit-root` and `legacy-explicit-root` expect ok but get empty.
`artifacts/results.json` records actual outputs and before/after pointers/cloud
hashes. All four terminal result channels are1 and actual cleanup is retained.

ES `GuiMenu.cpp:5225–5250` consumes that STATE: only found-elsewhere changes the
content path and only empty offers the chooser. Consequently this is a player
flow defect, not an unused helper discrepancy. No fixture data was lost or
modified; severity reflects blocked/misdirected restoration, not a data-loss
claim. Repair should share a content-recognition contract with restore, preserve
unrelated folders and explicit-empty root, handle unreadable listings distinctly,
and add installed empty-device/root/fallback and manual chooser success proof.

### F-02 — layout refusal is safe but says the folder is missing

**Severity: Medium. Category: Interaction Defect. Owner: layout/scan/UI.**
Issue#468; I356-L76 and I363-L76 PARTIAL. `cloud_migrate_layout:970–994` accepts
only complete supported marker bytes and returns4 on future/malformed content,
after a truthful application explanation. `cloud_scan:163–184` suppresses layout
output and sends its status through `why_for_rc:93–100`, where4 means rclone
folder absence. Actual UI26 future-refusal frame says COULDN’T FIND YOUR CLOUD
FOLDER despite the present unsupported marker. Preserved hashes and pointers
prove safe refusal, not truthful diagnosis.

Keep marker/write refusal. Give join/state/follow failures a producer-aware
reason rather than redefining every transport4. The sibling survey in03 covers
all current mapper callers and the separate apply path. Verify future/malformed,
real missing-folder and unavailable-provider states with target output/frame
and no-mutation controls. Initial inferred PASS was explicitly amended in02
after pixel inspection; that correction remains visible.

### F-03 — standalone sign-in pages omit the required French text

**Severity: Medium. Category: Acceptance Criteria Gap. Owner: sign-in UI.**
I351-L62 FAIL; I462-L31 and I354-L69 depend on it. Issue#469 now tracks the prepared finding; `signin-french-issue-draft.md` retains its source and acceptance criteria. D-CLOUD-164 explicitly includes phone Close confirmation and
the finishing page's two lines and requires French. `cloud_oauth:1015–1017`
and `network/cloud-signin-window/sources/cloud-signin-window.c:430–450` are
literal English outside the ES gettext catalog; they do not select a system
language. Current installed payload equality binds the source conclusion.

This is a source-contract defect; existing English frames do not constitute a
new French-mode runtime observation. Repair both surfaces, retain safe-answer-
first confirmation/Escape behavior and actual done-marker transition. Verify
English/French390px phone and640px native finishing frames using local owned
fixtures; no Dropbox credential or additional provider reset is needed.

## Code Quality Assessment

Strengths: explicit compatibility suffixes, atomic publication and shared locks,
numbered migrations with byte verification, source manifests and immutable
artifact custody, bounded provider work, precise before/after controls and
preserved original failures. Current source adoption avoids reviving the old
proxy merely to match a stale fixture.

Complexity hotspots remain cloud_migrate_layout/cloud_setup/cloud_scan,
cloud_content_restore and ES GuiMenu's asynchronous flows. The same concept is
encoded differently in setup, backup and restore; integer exit codes lose their
producer context; standalone HTML bypasses the otherwise correct ES translation
pipeline. These are concrete causes of F01–03. Broad refactoring during this
frozen review would invalidate its scope; fixes must be bounded and requalified.

## Cornerstone Conformance

**Overall: MEDIUM.** The complete per-rule/per-blindspot tables are in03.
Progress preservation, VM-first and exact-input custody have direct support.
Least-surprise/content discovery and player-language conformance fail for F01–03.
Watchers preserve evidence but disconnected delivery is still an explicit#395
limit. Continuous audit execution is now codified under D-WORKFLOW-149/#466;
a save checkpoint is not a pause or a running worker.

## Spec Fidelity

Approved changes are maintained: lowercase pixelelated, Tiny5 Duo LCD hard
RGB555/Ocean Bands assets, current upstream dependencies, only ROCKNIX adoption,
manual updates, no upstream statistics, optional Dropbox trust-page observation.
Numbered-marker compatibility is not retroactively attributed to RC2. The
current VM/preservation qualification remains distinct from future H700 builds.

Active-text reconciliation is incomplete (I409-L236, I337-L40/L41/L50): historical
first-sweep wording and literal old-name grep clauses need context. Two archive
compatibility comments legitimately contain ROCKNIX. D-WORKFLOW-144 does not
justify removing format compatibility or upstream attribution to satisfy grep.
This is existing rename/contract work, not a fourth observed runtime defect.

## Missing Artifacts and Pre-existing Tracked Scope

The exact PARTIAL criteria below remain open requirements. They are carried
from owning work, not inflated into duplicate punch items. Missing means not
located in the recorded search scope; it does not establish that the behavior
fails. Resolve by the named proof or an explicit, recorded contract revision,
never by silently ticking a parent.

| Owning criterion | Remaining artifact / next verification |
| --- | --- |
| I349-L43 | Foreign-only UI restore leaves system.hostname unchanged: retain before/after plus selected/no-selected archive. |
| I352-L34 | Successful manual chooser selection, persisted path and completed restore scan; existing D walk cancels. |
| I379-L22 | Settings-only installed cloud_setup completion→scan→selected archive/sentinel, not merely follow/settle/full restore. |
| I353-L32 | Actual installed mid-copy process kill followed by safe retry; host kill before third copy and guest returned errors do not prove that clause. |
| I353-L52 | Subsequent actual conflicting sync places new discarded-save copy under pixelelated after the shelf move. |
| I377-L24 | Literal synthetic bucket-backup failed parent read→successful retry and truthful terminal status. Real S3 restore403/retry is separate. |
| I361-L121 | Installed125-game indexed/unindexed whole-library pacing/429/interruption/retry proof; host controls are not this target run. |
| I354-L66 | Exact installed mixed-pair no-join negative; old host22FAIL baseline is not that experiment. |
| I337-L28, I344-L234/L259 | Bounded guest updater query/network observation with positive capture control, or reconciled manual-update measurement contract. |
| I344-L229/L231/L256 | Full brand/secret/leak sweep on final repaired candidate and future device images;09 sweep is not an unchanged-whole-image14 result. |
| I344-L212/L213/L214, I409-L237 | Sanitized canonical repo/account metadata, token scope/expiry/reminder receipt, current hosted-trigger proof; no credential contents required. |
| I337-L40/L41, I409-L236 | Active criteria/naming-history reconciliation and exact path/context sweep disposition. |
| I344-L217/L258 |14component-license dispositions and retrievable/hash-verified corresponding-source package before publication. |
| I337-L53, I349-L34, I352-L36, I359-L30 | Public cloud/adoption/SSH/attribution documentation; destination/access403/404 remains unresolved P5. |
| I337-L51, I344-L241/L248/L254/L255/L257/L260/L261 | Capacity#461, H700 DDR4 arm thenaarch64, actual device/adoption/boot proof and release assets/notes; no premature device readiness. |
| #395 | Configured/tested disconnected delivery destination is absent; current supervision is active-session only. |

Search/proximate-work record: Phase2 entries and01 name the current retained
QA chains, source transitions and searched frame/runtime outputs. For the
updater claim the primary search is recorded in the packet supplement; no new
network trace was found in those project QA directories. Prior375 comparison
explains why old missing-measurement rows remain narrower gaps after substantial
new proof. The recorded fresh remote/account probe failed before execution during the
earlier authentication outage. Later access recovery does not supply the
unexecuted account-metadata proof; this remains an evidence gap, not a
negative search result for the remote account.

## Tier B visual-QA consolidation

Existing accepted proofs remain tied to their own images and payload equality:
replacement09 guest11 cloud cases and UI17/UI26; replacement10 software/virgl
sign-in14/15/16, menu/Tools and four clean/upgrade640/1280 boot frames; current14
QA18 actual78 walk frames/34claims and clean/upgrade lifetime checks; qualified
RA UI03's23 original EN/FR640/1280 reconnect frames/109assertions. The primary
auditor directly inspected the relevant frames recorded per AC; no image count
alone is a visual PASS.

Fresh audit visual attention covered the future-marker message (F02), all23
reconnect frames and Tiny5 LCD background/small-size proofs. The previously
failed RA UI01/02 remain excluded. Wordmark24 raster exports contain only
approved palette colors and binary alpha;24px can sample LCD lettering poorly,
so no universal small-size readability claim is made. F01 needs repaired path
flow frames; F03 needs French phone/native frames. No wholesale page-scale
redesign is substituted for existing qualified layouts.

## Risk Assessment

| Risk | Severity | Impact | Mitigation |
| --- | --- | --- | --- |
| F01 | High | Valid cloud games not discovered; false configured success hides fallback | Unify recognition and exercise empty-local/root/configured/fallback target matrix. |
| F02 | Medium | Player receives wrong corrective direction when an update/layout is unsupported | Typed application versus transport reason; preserve refusal and verify actual frame. |
| F03 | Medium | Approved French sign-in flow remains English | Locale-aware standalone texts, both languages and actual transition proof. |
| Narrow measurement gaps | Medium, coverage uncertainty | Existing successful evidence is broader-sounding than its exact exercised cases | Keep PARTIAL and complete/reconcile each literal predicate. No invented runtime defect. |
| Premature device/public release | High if gate bypassed | Unqualified hardware or incomplete source/licensing published | Preserve ordered P4→capacity→H700→physical/P5 gates and publication authorization boundary. |

## Coverage Boundary

**Examined:**6550product files/207QA inputs/180raw symlinks manifest binding;
86changed product/build files and18ES files; source, commits, current/retained
installed artifacts and frames; fresh1719script/316focused checks,119ES assertions,
12recipe lints and additional dependency/proxy/schema/asset controls. Exact
execution versus source-equality reuse is stated per AC; raw commands/results
are retained. The supporting190rows are historical trust review, not190 new runs.

**Deliberately not examined:** physical H700/Nova panel/radio/battery behavior,
new device builds and public release; personal cloud mutation; optionalDropbox
trust/account proof; offsite backup topology and automation backlog. No audit
finding is a waiver of already ordered publication requirements.

**Dimensions not exercised:** the exact missing measurements above, fresh
publication-time metadata, destructive host fault injection, disconnected alerts,
and independent provider review. Primary exact model variant is unknown; lab is
OpenAI. Sandbox/auth limitations are harness failures, not product regressions.

## Instruction File Recommendations

| Finding / pattern | Existing rule that would prevent it | Recommendation |
| --- | --- | --- |
| F01 | engineering-practices: verify artifact and full blast radius; rclone-cloud-sync ownership/filter rules; blindspots8/22/31/36/44 | Extend production classifier regression matrix across configured/root/derived paths and empty local library. Existing doctrine suffices; a test/tool is more useful than another slogan. |
| F02 | es-player-text truthful outcomes; engineering-practices names are not behavior; blindspot33 typed status collision | Add producer-aware status tests and actual frame checks, preserving real rclone error controls. No global rc4 remapping. |
| F03 | player-language / es-player-text D-UI-051 and D-CLOUD-164 | Add standalone HTML strings to the existing language check's explicit surface scope; keep native and phone locale plumbing covered. |
| Repeated proof-substitution limits | engineering-practices artifact rule, vm-first and blindspots8/34/44/61 | Name execution domain, verb, input identity and failing control in retained qualification records; tools should reject absent required measurements where feasible. |
| Audit paused after save | code-auditor continuity and engineering-practices D-WORKFLOW-149 | Already changed under#466; record live owner/result delivery and continue until an actual blocker. No duplicate new rule needed. |

There are no three demonstrated uncovered instances requiring a new rule file.
The recurring weaknesses already have canonical homes; enforce them with
specific executable controls. This review recommends changes but does not edit
instruction files during the frozen audit. Phase7 may implement the bounded
checks alongside fixes; any broader language-tool change must preserve scope.

## Finding Verification (Phase 4.5)

| Finding | Severity | Refutation result | What was checked |
| --- | --- | --- | --- |
| F01 | High | Survives fresh actual-target repeat | Re-read classifier, backup eligibility, restore scan and ES consumer end-to-end. All retained probe files rehashed, seven before/after states equal,3PASS/4FAIL unchanged. A supported restore scanner cannot repair the earlier wrong STATE consumed by the UI. Fresh refutation03 repeats all seven cases:3PASS/4FAIL, identical outputs, allfourrc1 and actual cleanup verified. Failed01/02 are retained separately. |
| F02 | Medium | Survives | Marker guard protects bytes, but does not fix the caller's rc4 reason. UI26 actual pixels match the false sentence; generic transport mapping cannot express the application refusal truthfully. |
| F03 | Medium | Survives source contract check; repair runtime proof still required | Re-read D-CLOUD-164, phone literals and native FINISHING_PAGE/done-marker consumer. Existing ES translations cannot translate independently served literal HTML. No French-mode target observation invented. |

`evidence/finding-verification.json` and `evidence/refutation-03/` record the
completed17:06UTC actual rerun: all four terminal results1,3PASS/4FAIL, exact
original case outputs and no mutation. Actual host cleanup was verified17:08:41.
Refutation01 failed before VM setup on a missing directory;02 failed during
/tmp expansion and could not write outer results. Its incomplete image was
hash-preserved on/workspace before removing only that new temporary copy.
Neither failed owner is accepted as a reproduction. The watcher remained live,
but final observation was later than the60-second supervision policy; record
that limitation rather than claiming perfect delivery cadence. Phase4.5 is now
complete; no product code was changed.

## Second opinion (Phase 4.6)

**Complete:** both external calls verified, full answers read, every lead graded
against primary source/installed evidence. Primary: Codex/OpenAI, exact variant
unknown. Independent depth: **two model perspectives, one external reviewer,
two sequential calls**; no five-seat council and no substitute reviewer.
The owner explicitly approved both transfers (`transfer-approval.json`).

Both calls used `tools/council/run invoke --member claude --provider openrouter
--prompt-file <packet> --output <answer>` through sealed, actively supervised
`watch-build-submit` owners. Facilitator1.14.0 attested actual served
`anthropic/claude-fable-5.1`, effort`xhigh`, success, provider-response identity
PASS and output hashes. Provider reported Anthropic; the approved recipe is
not provider-pinned (`NOT_PINNED`). No retries occurred.

| Call | Packet / answer and provenance | Terminal / verified UTC | Reasoning tokens |
| --- | --- | --- | ---: |
| Blind | `second-opinions/claude-blind-brief.md` → `claude-blind.md`; `claude-blind.md.provenance.json`; `blind-verification.json` |18:36:42 /18:36:55|54082|
| Refutation | `second-opinions/claude-brief.md` → `claude-audit.md`; `claude-audit.md.provenance.json`; `refutation-verification.json` |18:49:11 /18:49:33|36704|

Each had five successful status channels, all sealed inputs unchanged at
verification (43/29), and actual owner processes absent. First terminal
observations were18:36:43 and18:49:16. Raw responses, packets and receipts are
retained unchanged. `evidence/fable-blind-01` and `fable-refutation-01` retain
owner/watcher records. Active-session supervision delivered these results;
#395 off-session alerts remain unconfigured. The observation gap over the
18:42–18:44 context transition is visible in the raw log; no uninterrupted
60-second coverage claim.

Primary verification then ran fourteen installed experiments on frozen14:
`evidence/reviewer-leads-03` (ten) and `reviewer-coverage-01` (four), all four
status channels0 per run, unchanged installed hashes, six actual PIDs absent
per run and five owned ports unbound. These zero statuses mean the experiments
completed, **not that every challenged product behavior passed**. The first
lead dispatch failed before execution on an absent activity directory;02
failed after an invalid-assignment fixture survived reset. Both are retained;
03 restored the entire synthetic config between cases and repeated all ten.
All runtime cloud data were synthetic/local. No personal cloud was contacted.

### Blind-pass grading

Source paths below are the installed rclone sources under
`projects/ROCKNIX/packages/network/rclone/sources/`, or the separately pinned
ES tree. Runtime filenames are under the named evidence run's `artifacts/`.

| Item | Primary grade | Evidence and disposition |
| --- | --- | --- |
| B-01 | confirmed; folded F-01 High | Original/refutation03 unrelated-folder failures repeat exactly; GuiMenu5239 bypasses chooser on false ok. Listing-error/absence branch stays in #467 repair scope. |
| B-02 | confirmed; folded F-01 | Explicit tiered/legacy root cases wrongly empty on14; both controls and unchanged pointers retained. |
| B-03 | confirmed; folded F-02 Medium | UI26 false missing-folder reason; marker before/after equality re-read in `second-opinions/ui26-marker-readback.json`. |
| B-04 | disagree with runtime prohibition; agree, narrowed to existing contract reconciliation | D-CLOUD-173 expressly permits boot preparation; main683–687 implements the30-second ceiling and stop-before-transfer. B-04 was withdrawn as a defect in refutation. Old no-per-sync wording needs its boot exception, not a code reversal. |
| B-05 | confirmed, G-01 Medium | `reviewer-leads-03/B05-kept-sibling-observation.json`: current marker/layout plus guest b KEEP yields migration-pending and moves b's live discarded shelf. Live saves and b pointers remain unchanged; bytes survive at the new shelf. |
| B-06 | agree, narrowed; G-02 Medium | `B06-record-fingerprint-observation.json`: comment-only config change after actual interruption makes state/apply/seed exit5; token exclusion succeeds, original binding resumes. Safe refusal is intentional; overbroad invalidation and absent supported recovery are the gap. No claim ordinary OAuth refresh breaks it. |
| B-07 | agree, re-graded Medium; G-03 | `B07-{join,follow,settle}-observation.json`: second pointer fault returns1; unfaulted retry returns3 with the partial pointers still present. Follow/settle report current. Persistent missed recovery warrants Medium rather than source-only Low. |
| B-08 | agree, narrowed to existing bookkeeping | D-UI-112 and player-language48–58 permit proposed words built for owner review; size-aware shortening is established. No per-string historic approval invented. Reviewer citation D-WORKFLOW-094 is unrelated rolling-release policy and is not used. Record proposed repair wording in the owning issues; do not create a permission blocker from this lead. |
| B-09 | agree, narrowed to reproduced G-04 Low | Strict join reader safely rejects the exported-assignment control before scan. A valid escaped-dollar folder is accepted by state but scan exits1 at SETTINGS BACKUPS (`B09-escaped`). Shared grammar is inconsistent; no wrong-root listing claim survives. |
| B-10 | agree, narrowed to existing contract reconciliation | Current plus pending record/historical content intentionally returns0; source1507–1526, #391 target recovery and host migration_retry cover it. Clarify stale I363-L75, no runtime defect. |
| B-11 | disagree with an unbounded-listing finding | Per-operation listing bounds plus actual S3 scan refusal41.4s in I401-L35 answer it. Refutation withdrew it. No new global worst-case guarantee inferred. |
| B-12 | agree, narrowed to explicitly scoped evidence reuse | Relevant09 ES/script bytes match14; actual frames were directly inspected. Refutation withdrew invalidation. Actual09 renderer identity was not located, so no virgl assertion is invented. Fresh final repaired-image frames remain owed. |
| B-13 | confirmed, folded F-03 and existing publication gaps | D-CLOUD-164 explicitly requires French for the phone confirmation/native finish. Token metadata and final sweep gaps already appear above and are not duplicate findings. |
| B-14 | agree, re-graded Medium; G-05 | `B14-{control,space,dots}`: actual root listing offers all three; MyGames selects, My Games/Games..old are refused with unchanged pointers. Ordinary valid library names cannot be selected; stronger than an unexecuted style concern. |

### Refutation-pass grading

| Item | Primary grade | Evidence and disposition |
| --- | --- | --- |
| R-01 | confirmed; folded F-01 | `reviewer-coverage-01/R01-stranded-root-observation.json`: STATE=stranded-at-root, but actual content scan reports gb cloud_bytes0 with a real root game present. Full ES source search has no stranded/root-action consumer. Include legacy root discovery/selection in #467; do not add a duplicate PL. |
| R-02 | disagree with stated ordinary-upgrade trigger | `post-update:108–111` invokes helper; `cloud_sync_helper:466–492` intentionally derives root for /GAMES. Installed `R02-stock-helper` writes explicit empty CONTENT_REMOTE and preserves cloud hashes. Forced missing-key readers differ, but the proposed normal NOT NOW window omits update initialization. I380's established transition contract is not downgraded on that premise. |
| R-03 | confirmed; folded F-02 | Installed `R03-outer-timeout`: second marker read stalled, outer ceiling returns124 in30.229s with no why and unchanged cloud/pointers. ThreadedCloudSync80–96 has no124-specific fallback, so generic reason follows. No card pixels for this new timeout are claimed; repair requires them. |
| R-04 | confirmed as pre-existing tracked boundary | T25 already proves configured prefix usable while full chooser scan refuses root denial. This is in #365's residual scope, not a new audit PL or an accepted all-provider guarantee. |
| R-05 | disagree for the stated wizard ceiling | GuiMenu7462 wraps seed-folders in timeout90. The direct script/create-page path has per-operation limits and is a distinct coverage boundary, not proof the wizard lacks its bound. |
| F-01 refutation | confirmed, High retained | Primary seven-case kill pass, full consumer and new R01 target case; no mitigating supported scan path repairs the earlier wrong branch. Automatic found-folder behavior follows D-CLOUD-167; reviewer suggestion to restrict it is a design lead, not a new owner decision. |
| F-02 refutation | confirmed, Medium retained | Marker bytes and pointers safe; message wrong. Extend sibling coverage to application rc2/5 and outer124 without treating all failures as transport errors. |
| F-03 refutation | confirmed, Medium retained | Independent HTML is English; D-CLOUD-164 specifies the exact phone/finish strings. Repair must state its locale source and prove EN/FR on both surfaces. |

### Packet coverage questions

| Question | Primary disposition |
| --- | --- |
|1 root consumer completeness| Full ES search and installed R01 settle the missing consumer/scanner effect; folded F01. |
|2 missing-key initialization| Installed helper plus post-update call settle the ordinary stock-shaped upgrade premise; no blanket claim arbitrary malformed state is healed. |
|3 timeout descendants| `C03-timeout-child` used installed /usr/bin/timeout, exit124; its owned sleep child was absent after the deadline. This exact control passes; no arbitrary daemon escape guarantee. |
|4 marker bytes| Both UI26 original before/after cloud manifests include the exact .layout hash and compare equal; readback JSON retained. |
|5 boundaries base| Retained exact `evidence/refutation-03/boundaries.py` and current target base read directly; Proof verifies BUILD_ID, installed hashes, fixture reset, cloud hashes and cleanup. It was omitted from the review excerpt, not absent from primary evidence. |
|6 B05/B06 execution| Both executed on unchanged14 with before/after proof in reviewer-leads03, including binding/token controls. |
|7 string approvals| No uncited owner approval claimed. Existing proposed-wording practice applies; exact original criteria/proposed strings remain bookkeeping scope. |
|8 preparation card text| Directly re-read E-boot0025 (SYNCING SAVES AT STARTUP / CHECKING THE CONNECTION) and0030 (SKIPPED / cloud folder not set up). Exact preparation-subphase timestamp is not identified; no new wrong-card claim or full transient-state proof. |
|9 outer124 reachability| Actual stalled second marker read reaches124 in30.229s; folded F02. |
|10 non-TTY progress| New B05/B06 installed output captured over SSH without a TTY includes Transferred/Elapsed progress; retained #401 stalled-transfer proof supplies the guard's stop-time evidence. |

Net effect: **five new findings G-01–G-05**, two Low→Medium re-grades after
runtime proof, original F-01–F-03 retained; R01/R03 folded into their repair
scope. B04/B11 are not runtime defects; B08/B10 are existing contract work;
B12 remains accurately bounded evidence reuse. R02's upgrade premise and R05's
wizard premise are refuted. Eight product findings total:1High,6Medium,1Low;
zero Critical. No known defect is waived and no product source changed.
The261-entry independent scorecard is preserved as the pre-review record;
these additional cross-cutting findings extend the final punch list rather
than silently rewriting that historical independence boundary.

## Quality Self-Check

| Item | Status |
| --- | --- |
| Scorecard IDs match02/machine ledger |261exact/unique; generated counts204/36/3/18/0. |
| Conformance tables |30rules and74distinct blindspots in03;190supporting IDs mapped separately. |
| Coverage boundary | Present in02 and04; runtime/source/host reuse distinguished. |
| Finding verification | Complete; fresh repeat and exact failed attempts recorded. |
| Second opinion | Complete: two verified calls,14blind/fiveR/threeF items and10coverage questions graded against primary artifacts. |
| Instruction recommendations | Present; existing-rule enforcement, no ungrounded new doctrine. |
| Tier B consolidation | Present with original image/run/frame identities and remaining repairs. |
| Verdict vocabulary | PASS/PARTIAL/FAIL/SKIP/UNTESTABLE only in forward ledger. |
| Traceability/evidence/reproducibility/actionability/completeness | Primary scope covered; audit incomplete until independent review, final artifacts and resolution. |
