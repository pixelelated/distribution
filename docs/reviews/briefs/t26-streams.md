# Stream brief: M6.P2 T26, stage E (#673)

**The coordinator's, 2026-10-27, at T26's stage-D pause** (the lane's post of 09:12 UTC; #1213 the audit, 29 items). Thirteen streams, serial, on the EmulationStation branch `feature/m6-es-guimenu-673` in `/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673`, which leaves the pin `16dbac5211` for the first time here; the distribution worktree takes only the audit folder's records, the day's log and, in S2, `docs/es-menu-map.md`. The dispositions that are not streams are in the ruling on #673; this file is only what changes code.

## The rules every stream keeps

The rules of T21's stream brief (`t21-streams.md` § The rules every stream keeps) apply here unchanged: test first with the FAIL recorded against the pin's code (`stage-e/sN-before.txt`, `sN-after.txt`, `sN-checks.txt`); D-WORKFLOW-210 and D-WORKFLOW-211; the host build by the lane's generated script (`tools/t26-build-tests.sh` or the lane's name) with the recipe's patched rapidjson, `es-syntax-check`'s `CANNOT` form, and the stand-in syntax check T21 left (`stage-e/syntax-check.sh` on `feature/m6-es-state-and-bridge-668`, read by `git show`, copied under this slice's audit folder) for `GuiMenu.cpp`; every new player sentence with its French in the same commit (D-UI-051, D-UI-112); the non-ASCII check over the added lines only; one commit per stream, `Refs #673, #<bug>`, no closing keyword, the ES `pre-push-test` before each push; `Already written:` answered in the bug and in `02` § The streams; nothing under the distribution's `packages/`, `projects/` or `tools/`; no guest, build, fetch or keyed call; `rm -rf` only as `"${VAR:?}"/...` in its own short command; a question for the coordinator on #673, never only on the screen (Backlog #1183); a stream the harness refuses is posted by number and stopped (D-WORKFLOW-212). **One more, this slice's own: a row added, moved or renamed updates `docs/es-menu-map.md` in the same commit and `tools/es-menu-map-check` passes before it (D-UI-039).** T21's ES branch at `3ae9610b0` is read by `git show` for what it already fixed in these files' neighbours (its S1 for `buildInputTextConfigRow`, its S6 `WifiText::connectOutcome`); nothing of it is merged here (the integration merges both).

## S1 -- PL-01: the repair picker's lifetime (High)

Files: `es-app/src/guis/GuiMenu.cpp` `openCloudSetup` (`:8219-8239`), `cloudSetupShowSshStep` (`:6660-6713`).

1. **Positive, before:** a harness case in `tests/cloud-oauth-lifetime.py`'s shape under ASan: the setup page closed by the picker, the network gone before the press, the picker's next press -- a use-after-free on the pin's lines.
2. **The fix:** the picker never calls `close()` on a page it already closed: the page it replaces is handed to the next transition and the transition is the one that closes, as `cloudSetupPresent(window, current, prev)` already does for the wizard (`es-native-ui.md` § Code conventions: callbacks on the new page hand that page to the next transition, never a deleted predecessor); when the network has dropped the picker shows its refusal on the page it still owns.
3. **Positive, after:** the case clean under ASan; `cloud-oauth-lifetime.py` still PASS.
4. **`Already written:`** nothing inherited (a lifetime).
5. **Commit:** `es-app: the repair picker never closes a page it already closed when the network drops (Refs #673, #<PL-01's bug>)`.

## S2 -- PL-02 and PL-15: the relink sentence and the map (Medium)

Files: `GuiMenu.cpp` `openRestoreRelink` (`:8460`), the French catalog, `docs/es-menu-map.md:405` (the distribution worktree, the same commit pair).

1. **Positive, before:** a unit over the sentence's row name against the row the hub builds at the pin (CLOUD CONNECTIONS, `c8dc72cf9`): the pin's sentence names a row that does not exist.
2. **The fix:** the sentence names the row as the pin builds it and the map holds it -- CLOUD CONNECTIONS, under its hub path -- in English and French; the map's relink heading reads what D-UI-046 settled, in the same change; `tools/es-menu-map-check --es-src <W> --ref <commit>` passes before the commit.
3. **Positive, after:** the unit PASS; the check's line.
4. **`Already written:`** nothing inherited (a sentence).
5. **Commit:** `es-app: the relink page's check-connection sentence names the CLOUD CONNECTIONS row (Refs #673, #<PL-02's bug>)`, and on the distribution branch `docs: the menu map's relink heading reads as D-UI-046 settled (Refs #673, #<the same bug>)`.

## S3 -- PL-03 and PL-04: two rows that write where no reader reads (Medium)

Files: `GuiMenu.cpp` `openGamesSettings` (`:5928`, `:5946-5947`), `openUISettings` (`:9485`).

1. **Positives, before:** units over each row's key and store against its reader: VIDEO FILTER writes `global.videofilters` where `setsettings.sh:793` reads `videofilter`; GAME MEDIAS DURING FAST SCROLLING writes `system.cfg` where `IList.h:110` reads `Settings`. FAIL on the pin.
2. **The fix:** each row writes the key and the store its reader reads (`global.videofilter`; `ScrollLoadMedias` in `es_settings.cfg`) and **reads both at load** -- the old key or store when the new one is absent -- writing only the new one (`upgrade-and-install.md` § An upgrade should be invisible, step 1).
3. **Positives, after:** the units PASS; a device-state fixture holding the old key alone loads the value and the next save writes the new key.
4. **`Already written:`** `global.videofilters=` in `system.cfg` and `ScrollLoadMedias` in `system.cfg` on every device that touched the rows -- read both, write the new one; nothing removed.
5. **Commit:** `es-app: VIDEO FILTER and GAME MEDIAS DURING FAST SCROLLING write where their readers read, and read the old place too (Refs #673, #<PL-03's bug>, #<PL-04's bug>)`; two #585 lines (upstream's rows).

## S4 -- PL-05: one guarded apply of the device password (Medium)

Files: `GuiMenu.cpp` the SSH wizard's password page (`:6523-6542`), the relink's DEVICE PASSWORD (`:8412-8425`); the SECURITY page (`:3261-3275`) is under `BATOCERA` and not built on ROCKNIX (recorded, not changed).

1. **Positive, before:** a harness case over the save hooks: an unchanged close runs `setrootpass`; an empty entry is persisted while the device keeps its password. FAIL on the pin.
2. **The fix:** one guarded apply shared by the pages: non-empty and changed (`es-ui-style-guide.md` § Saving), else the stored value is restored before the save and nothing runs; the display stays as the wizard designed it.
3. **Positive, after:** the case PASS; a journal read on the integration guest shows no `setrootpass` after an unchanged close (`fix-walk-pending-image`).
4. **`Already written:`** a device whose `root.password` reads empty while its password stands -- read both: an empty stored value is treated as unset and the row shows nothing until set.
5. **Commit:** `es-app: the device password is applied once, when non-empty and changed (Refs #673, #<PL-05's bug>)`.

## S5 -- PL-06: the cloud pages' calls off the frame (Medium)

Files: `GuiMenu.cpp` the sites `05` PL-06 lists (`:5579`, `:5589`, `:7233`, `:7321`, `:7450`, `:7930`, `:8027`, `:8091`, `:6749`, the `cloud_remote active` and `cloud_oauth cancel` calls).

1. **Positive, before:** a harness case with a stub script that sleeps 3 s: the pin's call holds the interface thread for it with no bound.
2. **The fix:** each listed call runs through the argv executor with a deadline (`WifiScanProcess::read(command, timeout, cancelled)`'s model, 5 s by D-CLOUD-109's spirit) under a `GuiLoading` spinner when it may exceed a frame, its timeout read as a failure with the page's existing sentence; `cloud_oauth cancel`'s own sleep stays the script's (T17's) but no longer blocks a frame. The other process starts in this file are recorded for the interface slices by site, not changed here.
3. **Positive, after:** the stub's 3 s no longer blocks the interface thread; a 6 s stub reads as a failure at the deadline.
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app: the cloud pages' script calls run bounded, under a spinner, off the frame (Refs #673, #<PL-06's bug>)`.

## S6 -- PL-07 and PL-08: the reads of files other processes write (Low)

Files: `GuiMenu.cpp` `cloudOAuthShowSignIn` (`:7767-7796`), `cloudOAuthPresentChoice` (`:7644-7646`), `cloudSelectionRead` (`:4133-4150`), `openNetworkSettings` (`:10303`).

1. **Positives, before:** units over the reads: the QR path asked cached (one failed attempt leaves the session text-only -- the window's G10 with its control); `isRegularFile` cached under a comment that says uncached; `wg0.conf` cached.
2. **The fix:** `exists(path, false)` and the uncached `isRegularFile` form for every file another process writes (`es-native-ui.md` § Core patterns); the QR texture re-requested by a path the texture cache does not alias (or the cache entry dropped) when the page is rebuilt.
3. **Positives, after:** the units PASS; G10's shape on the integration guest draws the QR after a failed attempt without an ES restart (`fix-walk-pending-image`).
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app: the sign-in's QR, the scan and selection files and wg0.conf are read uncached (Refs #673, #<PL-07's bug>, #<PL-08's bug>)`.

## S7 -- PL-09 and PL-10: the French (Low)

Files: `GuiMenu.cpp` `cloudOpenMatch` (`:5313-5326`), `runMaintenanceCommand` (`:360-389`), `openCloudAddRemote` (`:8116`), the provider labels (`:5679-5682`, `:8012`, `:8078`, `:7323-7328`, `:7452-7455`); `CloudText.cpp:18-46`.

1. **Positives, before:** `tools/es-untranslated` and the window's G11: the match's refusal and a failed maintenance run's why reach the screen as the script's English; the runtime msgid at `:8116` has no French; `providerLabel()` bypasses gettext.
2. **The fix:** the script's why sentences map through `CloudText::whySentences` with their French (the T18/T21 shape; a sentence the table lacks is added with its French); the provider labels through `_()` with extractable literals; the form's script-supplied labels through a table with French.
3. **Positives, after:** `es-untranslated --upstream cada856d86` names none of them; the French frames at the integration window.
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app: the match's refusal, the maintenance why and the provider labels reach the French (Refs #673, #<PL-09's bug>, #<PL-10's bug>)`.

## S8 -- PL-11 and PL-21: the command readers and one quoting (Low)

Files: `GuiMenu.cpp` `:7407-7422`, `:7995-8001`, `:8445-8453`, `:5579`, `:5589`, `cloudShellQuote` (`:7183-7194`); `es-core/src/platform/Platform.cpp:891-905` (`GetShOutput`, es-core's: a contained fix, `bugs-are-agent-first.md` rule 6, a #585 line).

1. **Positives, before:** units: `GetShOutput` drops a byte per read and never tests `popen`'s result; the two parses of one `OK=` line; a lost status line read as YOUR CLOUD IS ANSWERING; `cloudShellQuote` and `Utils::String::shellQuote` produce the same output over a corpus of names (the refactor's guard).
2. **The fix:** `GetShOutput` reads whole and fails closed; one parse; an empty status is a failure with its sentence; `cloudShellQuote` replaced by `Utils::String::shellQuote` (`credential-quoting.py`'s count unchanged).
3. **Positives, after:** the units PASS; `tests/credential-quoting.py` PASS.
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app, es-core: the cloud pages read a command's whole output, parse a status once, and quote through one function (Refs #673, #<PL-11's bug>)`.

## S9 -- PL-12 and PL-18: writes only when something changed (Low)

Files: `GuiMenu.cpp` `openRestoreRelink` (`:8307-8318`), `openSoundSettings` (`:9609-9613`, `:9653-9661`), `openSystemSettings` (`:1857-1870`).

1. **Positives, before:** the stores and the journal after a no-change close: the relink WI-FI PASSWORD page reconnects; SOUND SETTINGS writes two defaults at open; the timezone is written by every close.
2. **The fix:** the reconnect only when the password changed; the defaults read without being written; the timezone written when it changed. Rule 6 for the upstream and ROCKNIX rows; #585 lines.
3. **Positives, after:** a no-change visit leaves both stores' mtimes and the journal unchanged (the harness with doubled stores; the integration guest's mtimes).
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app: the relink's Wi-Fi password, SOUND SETTINGS' defaults and the timezone are written only when changed (Refs #673, #<PL-12's bug>, #<PL-18's bug>)`.

## S10 -- PL-13: a stored value to the shell, quoted (Low)

Files: `GuiMenu.cpp` `openSystemSettings` (`:2150-2167`), ROCKNIX-built behind `DEVICE_LED_CONTROL`.

1. **Positive, before:** `tests/credential-quoting.py`'s shape: a `led.color` value with a quote reaches `sh -lc` unquoted.
2. **The fix:** `Utils::String::shellQuote` on the argument; the count gains the site. Rule 6 (ROCKNIX's code in this file); a #585 line for ROCKNIX.
3. **Positive, after:** the case PASS.
4. **`Already written:`** a `led.color` already stored is read as before.
5. **Commit:** `es-app: the LED colour reaches the shell quoted (Refs #673, #<PL-13's bug>)`.

## S11 -- PL-14, PL-16 and PL-28: the words (Low)

Files: `GuiMenu.cpp` `openUpdatesSettings` (`:1513-1521`), the Wi-Fi verdicts (`:8320-8332`, `:10084-10090`, `:10124-10129`, `:10172`), `openRestoreRelink` (`:8486-8493`); the French catalog.

1. **Positives, before:** the units over the three strings (the MANUAL UPDATES dialog in sentence case; the three Wi-Fi verdicts; FINISH silent on a failed marker removal), FAIL on the pin.
2. **The fix, the words as ruled (D-UI-112, built as proposed):** MANUAL UPDATES in the house's upper case; **one Wi-Fi composer:** the switch's toggle shows one toast, `WI-FI IS ON.` / `WI-FI IS OFF.` (French `LE WI-FI EST ACTIVÉ.` / `LE WI-FI EST DÉSACTIVÉ.`), the relink page's success says what T21's S6 composes (`WifiText::connectOutcome`, read by `git show` at `3ae9610b0`, the same words), and the page close adds nothing (D-UI-107: no word twice); FINISH on a failed marker removal: `COULDN'T FINISH - THIS DEVICE COULDN'T SAVE THAT SETUP IS DONE. TRY AGAIN.` (French `IMPOSSIBLE DE TERMINER - CET APPAREIL N’A PAS PU ENREGISTRER LA FIN DE LA CONFIGURATION. RÉESSAYEZ.`), the marker left in place (the safe direction).
3. **Positives, after:** the units PASS; `es-untranslated` names none; frames at the integration window.
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app: MANUAL UPDATES in the house's case, one Wi-Fi verdict, and FINISH says when the marker stays (Refs #673, #<PL-14's bug>, #<PL-16's bug>, #<PL-28's bug>)`.

## S12 -- PL-25: the theme-set file onto the atomic writer (Low)

Files: `GuiMenu.cpp` `saveSubsetSettings` (`:11587`); Backlog #1186's row for this file.

1. **Positive, before:** the kill sweep's shape over the writer: a kill mid-write leaves a cut file.
2. **The fix:** `Utils::AtomicFile::writeText` with its result read (T18's S2 shape).
3. **Positive, after:** 0 kill points leave a cut file; `tools/t21-writers.py --expect-writeall` down by one on T21's branch at integration (recorded, not run here).
4. **`Already written:`** an empty or cut theme-set file on a card is read as today and replaced whole at the next save.
5. **Commit:** `es-app: the theme-set file is written atomically (Refs #673, #<PL-25's bug>, #1186)`.

## S13 -- PL-29: the dead fallback (Low)

Files: `GuiMenu.cpp` `cloudOpenTransfer` (`:5253-5256`), `cloudOpenTransferOptions` (`:4838-4841`).

1. **Positive, before:** a harness case with `cloud_scan` absent: the fallback cannot reach the transfer options.
2. **The fix:** the fallback removed (every image ships `cloud_scan`; D-CLOUD-175's scripts are current); with the script absent the page says its existing sentence for a missing tool and stops.
3. **Positive, after:** the case shows the sentence and no dead path; the transfer options reachable with the script present.
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app: the transfer page's fallback for images without cloud_scan is removed (Refs #673, #<PL-29's bug>)`.

## The record

As T21's: `02` § The streams with one row per stream (the positive before, the commit, the positive after, the `Already written:` answer, `proved:`); `05`'s gate table and `punch_index` moved together at Phase 7; `00`'s stage-E entry; the hand-back after stage E's record naming both tips, with `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in #673's body and each bug's `fixed-at-es`.

## What never runs here

A build, a compiler beyond the host's `g++` for the test targets and the stand-in syntax check, a guest, a fetch, a keyed council call, anything on a unit, a change outside the ES branch, the audit folder and `docs/es-menu-map.md` (S2), a change to T1's files or to upstream copies of a line beyond the contained fixes named.
