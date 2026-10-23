# Audit Analysis — M6.P2 T2, EmulationStation's launch path

**Auditor:** Code Auditor skill, with the renovation face (plan § 4)
**Date:** 2026-10-23
**Subject:** #649, the twenty EmulationStation paths at the pin `16dbac5211` (distribution `reviewed-at` `f4e0f0a196`)
**Spec:** `docs/reviews/briefs/es-launch-path.md` version 2

---

## Executive Summary

All twenty paths were read line by line: 11,287 lines, 17 fork-own and 3 upstream-carried. The fork's part of the three big files is the launch: about a fifth of `FileData.cpp`, 280 lines of `SystemData.cpp` and 498 of `main.cpp`. The rest is batocera's, byte for byte.

After the guest (stage A trials and eight proofs, `02-forward-audit.md` § Guest proofs), there is no Critical and no High. **Two Medium, both reproduced on the pin's binary:**

- **SS-1:** the shipped save-state path double-quotes the state file into the command. A ROM named `Test $HOME.gb` launched from its auto save handed the launcher `--state_file=/storage/roms/savestates/gb/Test /storage.state.auto` (G-6).
- **SD-2:** a sub-folder of any system is skipped when its path contains `ports` or `windows`. `gb/Sports/` was not listed and `gb/Puzzle/` was (G-4).

Two findings first graded Medium were **corrected by the guest**:

- **FD-14:** DELETE GAME follows no path outside the folder. Instead it never deletes a playlist's discs at all, because it removes the list before reading it (G-7). The containment gap stays as a latent condition on its fix.
- **VC-1:** the gated question appears 0.11 to 0.24 s after the press, over a black handover screen. The transition is `instant` by default and there is no splash on ROCKNIX (G-8).

Both are now Low. The rest are Low and Renovation rows. Q4: `rocknix/master` has 0 commits on the twenty since `cada856d8`; batocera has seven, none merged yet, three applying cleanly. Q6: 370 entry points, five unreached functions (one fork-retired, `renumberSlots`) and the expected unshipped `#if` arms. Q5 is measured (0.65 s and 1.01 s, no growth in memory).

## Acceptance-criteria scorecard

| AC | Verdict (end of Phase 2) | Note |
| --- | --- | --- |
| AC-01 | PARTIAL | `00` to `04` now; `05` is stage D |
| AC-02 | UNTESTABLE | the lint runs after 4.6 |
| AC-03 | UNTESTABLE | 4.6 waits for the host |
| AC-04 | UNTESTABLE | stage F |
| AC-05 | PARTIAL | `reviewed-at` recorded; the body is written at the hand-back |
| AC-06 | PASS | the BUILD_ID read from the guest (`069fc2704421...`) |
| AC-07 | PASS | 20 rows |
| AC-08 | PASS so far | every named check ran with its line; the syntax compile is owed per edited `.cpp` (none yet) |
| AC-09 | PASS | the two numbers beside #336's baseline, the loglevel, the memory table |
| AC-10 | PASS | 370 rows, below |
| AC-11 | PASS | below |
| AC-12 | PASS | 10 guest proofs, 10 `proved:` cells |
| AC-13 to AC-16 | UNTESTABLE | stages E to H |

## Code Quality Assessment

### Strengths
- The fork's launch code states its reasons beside the code: each gate, the capture generation, and the bookkeeper's lock order. It is quoted consistently (`shellQuote` on every capture, retire and adopt argument; `FileData.cpp:1147-1153`, `SaveStateBookkeeper.cpp:182-228`, `main.cpp:555-561`).
- `rescanIfFolderChanged` merges rather than rebuilds, dropping views and collection entries before deleting (SD-1).
- The fault handler is async-signal-careful and re-raises (MN-7).
- The pure parts have homes and tests: `LaunchCommand.h` (LaunchCommandTests), `SaveStateJobQueue` (SaveStateJobQueueTests).

### Concerns
- Command lines are built by string concatenation in several dialects: `shellQuote`, `getEscapedPath`, quote-on-space, and raw double quotes (SS-1, FD-2, FD-3).
- Upstream's list-driven deletes have no containment (FD-14).
- Plain statics are read across threads (FD-18).

### Complexity Hotspots
- `FileData::launchGame` (`:928-1328`, 400 lines, five responsibilities).
- `FileData.cpp` overall, which mixes the node model, the art lookup, the command, the gates and the return.
- `SystemData.cpp` (`loadConfig`'s two loading modes; `populateFolder`'s hard-coded exclusions).
- `main.cpp`'s `main` (`:697-1367`).

## Cornerstone Conformance

### Findings
See `03-retrospective.md` § 3.2. The ES rules are met except FD-10, FD-12, MN-5 and MN-6 (words), FD-8 (latent) and MN-4 (comments). One doctrine paragraph is stale (`time-to-play.md` on D-CLOUD-076/109, where the code ships D-CLOUD-130).

## Spec Fidelity

### Aligned
D-CLOUD-130 (every sync a launch interrupts asks), D-UI-096 (the question's shape), D-UI-093/095 (one surface at a time; automatic network work shown), D-UI-101/109 (saves first, then the batch), D-RA-035, D-CLOUD-062 (the frozen pair read from the finished command), D-LAUNCH-001 (play time on exit 0), D-UI-069 in `onGameEnded`, D-CLOUD-133 (SIGTERM kept immediate), D-UI-073 (the bookkeeper's rules).

### Diverged
FD-13 (a comment says renumbering), MN-4 (three comments), and `time-to-play.md` (the rule, not the code).

## Missing Artifacts

Unit cases for `formatCommandLineArgument` (FD-2) and `getContentFiles`/`deleteGameFiles` (FD-14). Search: `git -C $W grep -n -E 'formatCommandLineArgument|getContentFiles|deleteGameFiles' $PIN -- es-app/tests` → none.

## Risk Assessment

| Risk | Likelihood | Impact | Finding |
| --- | --- | --- | --- |
| DELETE GAME leaves a multi-file game's discs, and they return as games (and, once the order is fixed, files outside the folder would go) | medium (every multi-disc delete) | low now; high if the order is fixed without containment | FD-14 (G-7) |
| A state launch's command broken or expanded by a ROM name | low-medium (`$` in names) | medium (wrong file, or a command) | SS-1 (reproduced, G-6) |
| Games in a folder named `...ports`/`...windows` invisible | medium (genre folders) | medium (games missing) | SD-2 (reproduced, G-4) |
| A refused launch asks over the black handover screen | high (every gated launch) | low (surprise; 0.1-0.24 s) | VC-1 (G-8) |
| A freed `FileData` used by a deferred launch | very low (API reload during a wait) | high (crash) | FD-8 |
| A stored sort id crashes a list after a cross-build update | low | medium (crash on open) | SD-4 / FD-15 (reproduced, G-9) |

## Coverage Boundary

**Examined:** the twenty paths by reading, and the context reads named in `02-forward-audit.md` § Coverage Boundary.
**Exercised on the guest:** the ten proofs G-1 to G-10 (the pin's binary). **Compiled:** the unit tests, `tests/app-unit` under ASan/UBSan, the three harnesses. **Second reading's limits:** both seats saw only the excerpts (`second-opinions/*-brief.md`); the rest stands on this lane's reading. **Not exercised:** a netplay join, a real sync under a gate (a named substitute was used), thread interleavings (no ThreadSanitizer), a DELETE after the order is fixed.

## Finding Verification (Phase 4.5)

Each graded finding's primary lines were re-read at 17:5x from `git show $PIN:<path>`, not from the notes. **Confirmed:**
- **FD-14:** `FileData.cpp:1446-1451` (`isAbsolute` → insert; the `trim[0] == '/'` arm unreachable because `FileSystemUtil.cpp`'s `isAbsolute` is `path[0] == '/'` off WIN32), `:1503-1506` (the removes). The confirmation is `GuiGameOptions.cpp:253` `THIS WILL DELETE THE ACTUAL GAME FILE(S)!`, which names no path.
- **SS-1:** `SaveState.cpp:77`, `:97`, `:111`.
- **SD-2:** `SystemData.cpp:626-632`.
- **SD-3:** `SystemData.cpp:1039-1043`, `:1046-1050`.
- **VC-1:** `ViewController.cpp:584-587` (the splash before the animation), `:615-618` (`doLaunchGame` at its end).
- **FD-15:** `FileData.cpp:1658-1662`.
- **MN-3:** `main.cpp:533-540`.

**Withdrawn or graded down while writing** (recorded where they changed):
- **FD-1** Medium → Low and Q6: `netplayClientPassword` is never assigned.
- **FD-8** Medium → Low and latent: the rescan's two posts cannot land in a wait.
- **FD-14** Medium → Low (G-7): the delete never reads its list, so nothing outside the folder went; the discs stay instead.
- **VC-1** Medium → Low (G-8): `instant` by default, no splash on ROCKNIX; the question appears in 0.11 to 0.24 s.
- **SD-3** confirmed (G-5), **SS-1** confirmed (G-6) and **SD-2** confirmed (G-4) on the pin's binary.
- **VC-2**: netplay off short-circuits the IP check.
- **FD-18**'s HTTP-thread reader: none exists.

**Prior audits (provenance only, read now that Phase 2 is written):** the eight punch lists of § 1.5 were grepped for this phase's finding shapes (`.m3u`, `state_file`, `rfind("ports")`, `UKNOWN`, `formatCommandLineArgument`, `renumberSlots`). The command and its result are in the running log. A prior item that already names a finding is cited at Phase 5, and nothing is transcribed.

## Renovation face

### Q1 Modernize
- **FD-18:** `FileData::mRunningGame` → `std::atomic<FileData*>` behind `GetRunningGame()`. The tree's form is `sGamesStarted` (`FileData.cpp:90`).
- **One quoting dialect for command lines:** SS-1, FD-2 and FD-3 should use `Utils::String::shellQuote`, which the fork already uses in the same file (`:678`, `:1148-1153`).
- **Recorded, not proposed (upstream lines; merge cost against batocera, D-WORKFLOW-185's shape):** raw owning pointers (`mDisplayName`, `SystemData`'s members, `new SystemDataPtr[]`), C-style casts, and `ifstream` with manual `close()`.
- **The duplicated readers of one argument line** (`launchToken` here, `${ARGUMENTS##*-P}` in `runemu.sh`, and the `-P` fixtures in two test files) are the seam of § 3.5. The coordinator sequences the two lanes' fixes.
- The `racommands` save-state arms (SS-2) and the `--core=`/`--emulator=` tokens are #336's line: Q1 items there are `deferred:#336`.

### Q2 Standards and best practices
- **FD-10:** `UKNOWN ERROR` (`FileData.cpp:760`; the msgid in the French catalogue, and batocera's).
- **FD-11:** a log file's text shown to the player, unbounded.
- **FD-12:** two spaces before a toast's glyph (`es-ui-style-guide.md` § Glyphs).
- **MN-5:** three boxes outside `_()` (`main.cpp:929`, `:328-339`), so no French (D-UI-051). `es-untranslated` cannot see them.
- **MN-6:** `DOWNLOAD YOUR GAMES, ...` (`main.cpp:980`; D-UI-022's verbs and tiers).
- **SS-1:** the `shellQuote` rule (brief § 4 Q2).
- Checks run at the pin: credential quoting 9/9/0, menu map 0 missing, French 703/703/0, vocabulary 163 judged, 0 wrong (`02-forward-audit.md` § Mechanical checks).

### Q3 Bugs
Defects, each a `bug` issue at stage D with its VM criterion:
- **Medium:** SS-1 (reproduced, G-6), SD-2 (reproduced, G-4).
- **Low, corrected by the guest:** FD-14 (G-7) and VC-1 (G-8), both from Medium.
- **Low:** SD-3 (reproduced, G-5), SD-4/FD-15 (reproduced, G-9), FD-8 (latent), MN-2, MN-3, SB-2, FD-1 (spectator), FD-2/FD-3 (reachable under a custom template), FD-18.

Seam leads posted for other slices: FD-7 (T36), FD-9/FD-19 (T33/T21), PC-1/SB-3 (T35/T16/T18), PC-2 (T21), the 7z hash quoting (`ApiSystem.cpp:1527`, `:1659`; T21), `GuiGamelistOptions.cpp:148` (FD-15's sibling), and `GuiMenu.cpp:11714-11738` (MN-5's sibling).

### Q4 Package currency: both upstreams
- **`rocknix/master`** (`f6c542872`, fetched 2026-10-23): `git -C $W rev-list --count cada856d8..rocknix/master -- <the 20 paths>` = **0**. Nothing to take.
- **`batocera/master`** (`b2ceb55a7`): `git -C $W log --oneline 1750dded8..batocera/master -- <the 20 paths>` = **7**. Each was tested with `git show <c> -- <20> | git apply --check` (forward) and `--reverse`, which writes nothing:

| Commit | Date | Subject | Files | Forward / reverse at the pin | Disposition |
| --- | --- | --- | --- | --- | --- |
| `13e21d420` | 2026-09-12 | Fix for quicksearch/random system | `SystemData.cpp` (`getRandomSystem`) | applies / no | **to merge**: a fix (random picks only visible systems), upstream lines, no fork overlap |
| `195a517ef` | 2026-10-01 | Merge pull request #2213 from Tartifless/master | (the merge carrying `13e21d420`) | no diff of its own | **merged with `13e21d420`**: the same change |
| `b69fb143c` | 2026-09-30 | Add a "max depth" to limit the number of rom subfolders to parse | `SystemData.cpp`, `.h` | conflicts (`SystemData.cpp:100`, `.h:119`, the fork's `mFolderScannedAt` hunk) / no | **to merge, by hand**: `populateFolder`'s new depth must also reach the fork's `rescanIfFolderChanged` (`:434`), or a rescan reads deeper than startup did and its merge reports files as new |
| `d17cf003e` | 2026-10-05 | [Pico8] Only show .p8 carts as images when they are PNG files | `FileData.cpp` (`getImagePath`) | applies / no | **to merge**: a fix on upstream lines (`:442`) |
| `308221458` | 2026-10-16 | fix zoom into the game art at launch; fix bios check threading | `ViewController.cpp`, `.h` | applies / no | **to merge**: the BIOS check leaves the interface thread and runs during the transition (`CheckBiosesAtLaunch`, default false, `Settings.cpp:207`). It changes `launch`'s signature for every caller in other slices, and it touches VC-1's ground (where the gates sit) |
| `5f106acce` | 2026-10-19 | fix game launch zoom timings | `ViewController.cpp` | stacks on `308221458` | **to merge after `308221458`** |
| `0806a0c5c` | 2026-10-20 | launch zoom centres on the selected game art from every launch path, fade to the game splash when there is no art | `ViewController.cpp` | stacks on `308221458` | **to merge after `308221458`** |

None is merged, none is not applicable, and six are to merge, one by hand. Upstream merges are the coordinator's to schedule (D-WORKFLOW-189). The three `ViewController` commits are best taken before VC-1's fix, so the fix is written once against the new `launch`. The inventory's `overlap` column is false for all twenty, measured against `rocknix/master` only, so these seven come from the log, as the brief says.

### Q5 Efficiency

Measured on the lane's guest: BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`, 4 vCPUs, 8 GiB, GL through virgl (the headless default, `generic-x64-vm-testing.md` § The guests render in hardware), `video_driver = "gl"` as shipped, **`system.loglevel = verbose`** (the engineering image's `DEVELOPMENT_DEFAULTS`), and no cloud remote.

| Number | This slice's guest, at the pin (median / mean / max, n=3) | #336's baseline (VM) | T1's measurement on this image |
| --- | --- | --- | --- |
| interface → a game's first frame | **0.65 / 0.67 / 0.81 s** | 1.05 s | 0.64 s |
| a game's exit → the next game's first frame | **1.01 / 1.01 / 1.01 s** | 2.03 s | 1.01 s |
| (press → RetroArch existing) | 0.48 / 0.51 / 0.56 s | 0.58 s | — |
| (press → RetroArch drawing, 200 CPU ticks) | 4.53 / 4.56 / 4.62 s | 4.58 s | — |

The report ends `Not a pass: the exit sync had no cloud to reach`. The exit sync skips at once, so the second number is not like for like with a configured device (T1's caveat, and the brief's). The improvement against #336's baseline predates this slice: #336's numbers were taken before the M7 work this image carries. This slice has changed nothing yet.

**`es-launch-memory`'s per-cycle table** (`$R/launch-memory-1/cycles.csv`; columns cycle, pid, epoch, VmSize KiB, VmRSS KiB, threads):

| cycle | pid | VmSize KiB | VmRSS KiB | threads |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1567 | 1,557,112 | 157,308 | 13 |
| 1 | 1567 | 1,552,088 | 129,156 | 14 |
| 2 | 1567 | 1,552,128 | 130,836 | 14 |
| 3 | 1567 | 1,552,128 | 130,980 | 14 |
| 4 | 1567 | 1,552,132 | 130,640 | 14 |
| 5 | 1567 | 1,552,120 | 131,008 | 14 |

So a launch and an exit leave nothing behind in the process: VmSize stays flat to 44 KiB after the first exit's trim (`malloc_trim`, `FileData.cpp:1080`, `:1216`), and #310's 10 MiB per cycle does not recur. The first exit releases about 26 MiB RSS.

**The gated launch (G-8):** the question shows 0.11 to 0.24 s after the press, with the default `instant` transition and no splash. A non-instant `GameTransitionStyle` adds its 0.4 to 1.5 s before the question and again in the return.

**Items still to itemise:**
- **Press → command:** `captureGate`'s ≤ 300 ms (`FileData.cpp:888`) is waited only when a capture is still recording. `configureEmulators` (FD-6), `window->deinit`, `malloc_trim` and `fireEvent("game-start")`'s three directory scans are inside the 0.48 s to RetroArch existing.
- **Exit → next frame:** the state repository's `refresh` (SR-2) at 500 states costs nothing measurable (G-10: 1.01 s, as without). `recordAfterSession`, `fireEvent("game-end")`, `window->init`, `refreshCollectionSystems` and `saveToGamelistRecovery` are inside the 1.01 s.
- **Startup:** the boot game, `serial_number_check`, `preload`, and `loadSystem(name)`'s re-parse per group (SD-3) are not timed here, because `startup` reboots and the brief's cells exclude it.

### Q6 Dead ends: one reachability row per entry point of the twenty files, and per preprocessor conditional

**The commands and their counts** (at the pin):
- brief § 4's header regex → **154** declarations;
- `grep -n '^static '` over the ten `.cpp` → **32** lines (13 functions, 19 data);
- `git grep -n -E '^#(if|else|elif)'` → **60** (the brief recorded 36; the pattern also matches `#ifdef`/`#ifndef`).

A regex misses multi-line, inline and indented forms, so the list was rebuilt by `q6-reachability.py` (this folder; `python3 -I q6-reachability.py $W $PIN`) to **295** declarations, **13** static functions and **62** conditionals: **370 rows**, read by eye against the headers. The hand corrections: `recordCopy`, whose call spans two lines and is reached (`GuiSaveState.cpp:524`), and the 19 static data lines, which are not entry points.

**Unreached:** five functions, each confirmed with `git grep -n -w <name> $PIN -- es-app/src es-core/src es-app/tests`: `renumberSlots` (SR-1, fork-retired by D-UI-069), `isVirtualFolderDisplayEnabled`, `hasGamelist`, `setIndex` and `isDefaultConfig` (upstream API). Of the conditionals, every WIN32, `_RPI_`, `BATOCERA`, `_ENABLE_KODI_`, `FREEIMAGE_LIB` and `DEBUG` arm and the `#else` of each `#if ROCKNIX` are unshipped. Each is a row, not a removal (D-WORKFLOW-185's shape). Beyond functions:
- the template placeholders `%BASENAME%`, `%ROM_RAW%`, `%GAMENAME%`, `%SYSTEMNAME%`, `%GAMEINFOXML%`, `%HOME%` and `%NETPLAY%` are not in the shipped command (FD-5; `distributions/ROCKNIX/config/functions:128`);
- `-monitor` needs ` -system `, which the command lacks;
- the `racommands` save-state arms run only without `es_savestates.cfg` (SS-2);
- `LaunchGameOptions::isSaveStateInfoTemporary` and `netplayClientPassword` (FD-21);
- the commented-out SIGTERM handler (`main.cpp:730`, decided by D-CLOUD-133);
- `--log-path` is passed by `start_es.sh` and read by nobody (MN-1).

Final count: **370 rows** (295 + 13 + 62), command counts 154/32/60, and **5 unreached functions** carrying `Already written:`.

| # | Kind | Where | Entry point | Reachability (`use_lines` = lines elsewhere in es-app/src and es-core/src naming it) |
| ---: | --- | --- | --- | --- |
| 1 | decl | `FileData.h:53` | `LaunchGameOptions` | reached (26 use lines) |
| 2 | decl | `FileData.h:94` | `FileData` | reached (647 use lines) |
| 3 | decl | `FileData.h:95` | `~FileData` | reached by `delete`/scope end (destructor) |
| 4 | decl | `FileData.h:97` | `GetRunningGame` | reached (11 use lines) |
| 5 | decl | `FileData.h:103` | `getName` | reached (324 use lines) |
| 6 | decl | `FileData.h:105` | `getType` | reached (111 use lines) |
| 7 | decl | `FileData.h:113` | `getBreadCrumbPath` | reached (2 use lines) |
| 8 | decl | `FileData.h:115` | `getSystemEnvData` | reached (25 use lines) |
| 9 | decl | `FileData.h:117` | `getThumbnailPath` | reached (20 use lines) |
| 10 | decl | `FileData.h:118` | `getVideoPath` | reached (10 use lines) |
| 11 | decl | `FileData.h:119` | `getMarqueePath` | reached (14 use lines) |
| 12 | decl | `FileData.h:120` | `getImagePath` | reached (31 use lines) |
| 13 | decl | `FileData.h:122` | `getCore` | reached (17 use lines) |
| 14 | decl | `FileData.h:123` | `getEmulator` | reached (23 use lines) |
| 15 | decl | `FileData.h:125` | `isNetplaySupported` | reached (13 use lines) |
| 16 | decl | `FileData.h:127` | `setCore` | reached (1 use lines) |
| 17 | decl | `FileData.h:128` | `setEmulator` | reached (1 use lines) |
| 18 | decl | `FileData.h:130` | `getHidden` | reached (8 use lines) |
| 19 | decl | `FileData.h:131` | `getFavorite` | reached (12 use lines) |
| 20 | decl | `FileData.h:132` | `getKidGame` | reached (6 use lines) |
| 21 | decl | `FileData.h:133` | `hasCheevos` | reached (12 use lines) |
| 22 | decl | `FileData.h:135` | `hasAnyMedia` | reached (4 use lines) |
| 23 | decl | `FileData.h:136` | `getFileMedias` | reached (3 use lines) |
| 24 | decl | `FileData.h:138` | `getConfigurationName` | reached (6 use lines) |
| 25 | decl | `FileData.h:140` | `isPlaceHolder` | reached (9 use lines) |
| 26 | decl | `FileData.h:142` | `getKey` | reached (4 use lines) |
| 27 | decl | `FileData.h:143` | `isArcadeAsset` | reached (3 use lines) |
| 28 | decl | `FileData.h:144` | `isVerticalArcadeGame` | reached (2 use lines) |
| 29 | decl | `FileData.h:145` | `isLightGunGame` | reached (7 use lines) |
| 30 | decl | `FileData.h:146` | `isWheelGame` | reached (7 use lines) |
| 31 | decl | `FileData.h:147` | `isTrackballGame` | reached (7 use lines) |
| 32 | decl | `FileData.h:148` | `isSpinnerGame` | reached (7 use lines) |
| 33 | decl | `FileData.h:149` | `getFullPath` | reached (17 use lines) |
| 34 | decl | `FileData.h:150` | `getFileName` | reached (72 use lines) |
| 35 | decl | `FileData.h:151` | `getSourceFileData` | reached (118 use lines) |
| 36 | decl | `FileData.h:152` | `getSystemName` | reached (20 use lines) |
| 37 | decl | `FileData.h:155` | `getDisplayName` | reached (25 use lines) |
| 38 | decl | `FileData.h:158` | `getCleanName` | reached (3 use lines) |
| 39 | decl | `FileData.h:160` | `getlaunchCommand` | reached (3 use lines) |
| 40 | decl | `FileData.h:161` | `getlaunchCommand` | reached (3 use lines) |
| 41 | decl | `FileData.h:163` | `launchGame` | reached (8 use lines) |
| 42 | decl | `FileData.h:165` | `resetSettings` | reached (8 use lines) |
| 43 | decl | `FileData.h:167` | `getMetadata` | reached (254 use lines) |
| 44 | decl | `FileData.h:177` | `deleteGameFiles` | reached (2 use lines) |
| 45 | decl | `FileData.h:179` | `checkCrc32` | reached (4 use lines) |
| 46 | decl | `FileData.h:180` | `checkMd5` | reached (1 use lines) |
| 47 | decl | `FileData.h:181` | `checkCheevosHash` | reached (2 use lines) |
| 48 | decl | `FileData.h:183` | `importP2k` | reached (3 use lines) |
| 49 | decl | `FileData.h:184` | `convertP2kFile` | reached (2 use lines) |
| 50 | decl | `FileData.h:185` | `hasP2kFile` | reached (2 use lines) |
| 51 | decl | `FileData.h:187` | `hasKeyboardMapping` | reached (8 use lines) |
| 52 | decl | `FileData.h:188` | `getKeyboardMapping` | reached (5 use lines) |
| 53 | decl | `FileData.h:189` | `isFeatureSupported` | reached (22 use lines) |
| 54 | decl | `FileData.h:190` | `isExtensionCompatible` | reached (2 use lines) |
| 55 | decl | `FileData.h:192` | `getCurrentGameSetting` | reached (3 use lines) |
| 56 | decl | `FileData.h:194` | `hasContentFiles` | reached (3 use lines) |
| 57 | decl | `FileData.h:195` | `getContentFiles` | reached (3 use lines) |
| 58 | decl | `FileData.h:197` | `setSelectedGame` | reached (4 use lines) |
| 59 | decl | `FileData.h:199` | `parsePlayersRange` | reached (3 use lines) |
| 60 | decl | `FileData.h:202` | `getProperty` | reached (44 use lines) |
| 61 | decl | `FileData.h:203` | `getBindableTypeName` | reached (8 use lines) |
| 62 | decl | `FileData.h:206` | `getGenre` | reached (3 use lines) |
| 63 | decl | `FileData.h:207` | `getSortName` | reached (2 use lines) |
| 64 | decl | `FileData.h:210` | `getKeyboardMappingFilePath` | reached (9 use lines) |
| 65 | decl | `FileData.h:211` | `getMessageFromExitCode` | reached (1 use lines) |
| 66 | decl | `FileData.h:215` | `findLocalArt` | reached (7 use lines) |
| 67 | decl | `FileData.h:229` | `CollectionFileData` | reached (15 use lines) |
| 68 | decl | `FileData.h:230` | `~CollectionFileData` | reached by `delete`/scope end (destructor) |
| 69 | decl | `FileData.h:231` | `getName` | reached (324 use lines) |
| 70 | decl | `FileData.h:232` | `getSourceFileData` | reached (118 use lines) |
| 71 | decl | `FileData.h:233` | `getKey` | reached (4 use lines) |
| 72 | decl | `FileData.h:234` | `getPath` | reached (135 use lines) |
| 73 | decl | `FileData.h:236` | `getSystemName` | reached (20 use lines) |
| 74 | decl | `FileData.h:237` | `getSystemEnvData` | reached (25 use lines) |
| 75 | decl | `FileData.h:239` | `getMetadata` | reached (254 use lines) |
| 76 | decl | `FileData.h:254` | `FolderData` | reached (144 use lines) |
| 77 | decl | `FileData.h:255` | `~FolderData` | reached by `delete`/scope end (destructor) |
| 78 | decl | `FileData.h:257` | `isVirtualStorage` | reached (6 use lines) |
| 79 | decl | `FileData.h:261` | `isVirtualFolderDisplayEnabled` | **unreached** (upstream-carried inline getter; no caller in es-app/es-core). Already written: nothing (a read of a member). Exposed: nothing |
| 80 | decl | `FileData.h:263` | `FindByPath` | reached (11 use lines) |
| 81 | decl | `FileData.h:265` | `getChildren` | reached (37 use lines) |
| 82 | decl | `FileData.h:267` | `findChildrenListToDisplayAtCursor` | reached (4 use lines) |
| 83 | decl | `FileData.h:269` | `getFilesRecursive` | reached (33 use lines) |
| 84 | decl | `FileData.h:270` | `getFlatGameList` | reached (1 use lines) |
| 85 | decl | `FileData.h:272` | `addChild` | reached (131 use lines) |
| 86 | decl | `FileData.h:273` | `removeChild` | reached (27 use lines) |
| 87 | decl | `FileData.h:274` | `bulkRemoveChildren` | reached (1 use lines) |
| 88 | decl | `FileData.h:276` | `createChildrenByFilenameMap` | reached (3 use lines) |
| 89 | decl | `FileData.h:278` | `findUniqueGameForFolder` | reached (3 use lines) |
| 90 | decl | `FileData.h:280` | `clear` | reached (247 use lines) |
| 91 | decl | `FileData.h:281` | `removeVirtualFolders` | reached (1 use lines) |
| 92 | decl | `FileData.h:282` | `removeFromVirtualFolders` | reached (8 use lines) |
| 93 | decl | `FileData.h:285` | `getFilesRecursiveWithContext` | reached (2 use lines) |
| 94 | decl | `SystemData.h:53` | `SystemEnvironmentData` | reached (15 use lines) |
| 95 | decl | `SystemData.h:62` | `isValidExtension` | reached (5 use lines) |
| 96 | decl | `SystemData.h:73` | `BindableRandom` | reached (4 use lines) |
| 97 | decl | `SystemData.h:75` | `getProperty` | reached (44 use lines) |
| 98 | decl | `SystemData.h:77` | `getBindableTypeName` | reached (8 use lines) |
| 99 | decl | `SystemData.h:88` | `SystemData` | reached (588 use lines) |
| 100 | decl | `SystemData.h:89` | `~SystemData` | reached by `delete`/scope end (destructor) |
| 101 | decl | `SystemData.h:91` | `getSystem` | reached (216 use lines) |
| 102 | decl | `SystemData.h:92` | `getFirstVisibleSystem` | reached (3 use lines) |
| 103 | decl | `SystemData.h:94` | `getRootFolder` | reached (103 use lines) |
| 104 | decl | `SystemData.h:99` | `rescanIfFolderChanged` | reached (5 use lines) |
| 105 | decl | `SystemData.h:100` | `rescanChangedFolders` | reached (2 use lines) |
| 106 | decl | `SystemData.h:101` | `getName` | reached (324 use lines) |
| 107 | decl | `SystemData.h:114` | `hasGamelist` | **unreached** (upstream; `rescanIfFolderChanged` tests `exists(getGamelistPath(false))` itself, `SystemData.cpp:382`). Already written: nothing (a read). Exposed: nothing |
| 108 | decl | `SystemData.h:115` | `getThemePath` | reached (4 use lines) |
| 109 | decl | `SystemData.h:117` | `getGameCount` | reached (2 use lines) |
| 110 | decl | `SystemData.h:119` | `getGameCountInfo` | reached (6 use lines) |
| 111 | decl | `SystemData.h:120` | `updateDisplayedGameCount` | reached (5 use lines) |
| 112 | decl | `SystemData.h:123` | `hasDirtySystems` | reached (1 use lines) |
| 113 | decl | `SystemData.h:124` | `deleteSystems` | reached (3 use lines) |
| 114 | decl | `SystemData.h:125` | `loadConfig` | reached (4 use lines) |
| 115 | decl | `SystemData.h:132` | `startIndexesAtStart` | reached (4 use lines) |
| 116 | decl | `SystemData.h:133` | `getConfigPath` | reached (10 use lines) |
| 117 | decl | `SystemData.h:135` | `loadFeatures` | reached (1 use lines) |
| 118 | decl | `SystemData.h:139` | `getIterator` | reached (1 use lines) |
| 119 | decl | `SystemData.h:140` | `getRevIterator` | reached (1 use lines) |
| 120 | decl | `SystemData.h:141` | `isCollection` | reached (77 use lines) |
| 121 | decl | `SystemData.h:142` | `isGameSystem` | reached (39 use lines) |
| 122 | decl | `SystemData.h:144` | `isGroupSystem` | reached (17 use lines) |
| 123 | decl | `SystemData.h:145` | `isGroupChildSystem` | reached (29 use lines) |
| 124 | decl | `SystemData.h:147` | `isVisible` | reached (54 use lines) |
| 125 | decl | `SystemData.h:148` | `isHidden` | reached (7 use lines) |
| 126 | decl | `SystemData.h:151` | `getPrev` | reached (1 use lines) |
| 127 | decl | `SystemData.h:152` | `getRandomSystem` | reached (3 use lines) |
| 128 | decl | `SystemData.h:153` | `getRandomGame` | reached (1 use lines) |
| 129 | decl | `SystemData.h:156` | `loadTheme` | reached (6 use lines) |
| 130 | decl | `SystemData.h:158` | `getIndex` | reached (21 use lines) |
| 131 | decl | `SystemData.h:159` | `setIndex` | **unreached** (upstream inline setter). Already written: nothing. Exposed: replacing the filter index without deleting the old one (a leak if called) |
| 132 | decl | `SystemData.h:163` | `removeFromIndex` | reached (8 use lines) |
| 133 | decl | `SystemData.h:167` | `addToIndex` | reached (14 use lines) |
| 134 | decl | `SystemData.h:171` | `resetFilters` | reached (9 use lines) |
| 135 | decl | `SystemData.h:175` | `resetIndex` | reached (7 use lines) |
| 136 | decl | `SystemData.h:179` | `setUIModeFilters` | reached (7 use lines) |
| 137 | decl | `SystemData.h:183` | `getEmulators` | reached (17 use lines) |
| 138 | decl | `SystemData.h:186` | `setSortId` | reached (3 use lines) |
| 139 | decl | `SystemData.h:188` | `getSystemViewMode` | reached (7 use lines) |
| 140 | decl | `SystemData.h:189` | `setSystemViewMode` | reached (7 use lines) |
| 141 | decl | `SystemData.h:191` | `getGridSizeOverride` | reached (4 use lines) |
| 142 | decl | `SystemData.h:193` | `setGamelistHash` | reached (1 use lines) |
| 143 | decl | `SystemData.h:197` | `isCheevosSupported` | reached (9 use lines) |
| 144 | decl | `SystemData.h:199` | `isNetplayActivated` | reached (7 use lines) |
| 145 | decl | `SystemData.h:201` | `getParentGroupSystem` | reached (19 use lines) |
| 146 | decl | `SystemData.h:203` | `getAllGroupNames` | reached (1 use lines) |
| 147 | decl | `SystemData.h:204` | `getGroupChildSystemNames` | reached (4 use lines) |
| 148 | decl | `SystemData.h:206` | `getEmulator` | reached (23 use lines) |
| 149 | decl | `SystemData.h:207` | `getCore` | reached (17 use lines) |
| 150 | decl | `SystemData.h:209` | `getDefaultEmulator` | reached (7 use lines) |
| 151 | decl | `SystemData.h:210` | `getDefaultCore` | reached (7 use lines) |
| 152 | decl | `SystemData.h:212` | `getLaunchCommand` | reached (2 use lines) |
| 153 | decl | `SystemData.h:213` | `getCoreNames` | reached (1 use lines) |
| 154 | decl | `SystemData.h:215` | `isCurrentFeatureSupported` | reached (2 use lines) |
| 155 | decl | `SystemData.h:216` | `isFeatureSupported` | reached (22 use lines) |
| 156 | decl | `SystemData.h:217` | `getCustomFeatures` | reached (1 use lines) |
| 157 | decl | `SystemData.h:218` | `getCompatibleCoreNames` | reached (2 use lines) |
| 158 | decl | `SystemData.h:220` | `hasFeatures` | reached (3 use lines) |
| 159 | decl | `SystemData.h:221` | `hasEmulatorSelection` | reached (4 use lines) |
| 160 | decl | `SystemData.h:223` | `getFilterIndex` | reached (1 use lines) |
| 161 | decl | `SystemData.h:226` | `getKnownSystemNames` | reached (2 use lines) |
| 162 | decl | `SystemData.h:228` | `hasKeyboardMapping` | reached (8 use lines) |
| 163 | decl | `SystemData.h:229` | `getKeyboardMapping` | reached (5 use lines) |
| 164 | decl | `SystemData.h:231` | `shouldExtractHashesFromArchives` | reached (5 use lines) |
| 165 | decl | `SystemData.h:233` | `getShowFilenames` | reached (1 use lines) |
| 166 | decl | `SystemData.h:234` | `getShowParentFolder` | reached (4 use lines) |
| 167 | decl | `SystemData.h:235` | `getShowFavoritesFirst` | reached (1 use lines) |
| 168 | decl | `SystemData.h:236` | `getShowFavoritesIcon` | reached (4 use lines) |
| 169 | decl | `SystemData.h:237` | `getShowCheevosIcon` | reached (2 use lines) |
| 170 | decl | `SystemData.h:238` | `getShowFlags` | reached (2 use lines) |
| 171 | decl | `SystemData.h:239` | `getShowTags` | reached (1 use lines) |
| 172 | decl | `SystemData.h:240` | `getFolderViewMode` | reached (6 use lines) |
| 173 | decl | `SystemData.h:241` | `getBoolSetting` | reached (16 use lines) |
| 174 | decl | `SystemData.h:243` | `resetSettings` | reached (8 use lines) |
| 175 | decl | `SystemData.h:245` | `getSaveStateRepository` | reached (13 use lines) |
| 176 | decl | `SystemData.h:248` | `getProperty` | reached (44 use lines) |
| 177 | decl | `SystemData.h:249` | `getBindableTypeName` | reached (8 use lines) |
| 178 | decl | `SystemData.h:253` | `createGroupedSystems` | reached (1 use lines) |
| 179 | decl | `SystemData.h:268` | `populateFolder` | reached (3 use lines) |
| 180 | decl | `SystemData.h:269` | `indexAllGameFilters` | reached (2 use lines) |
| 181 | decl | `SystemData.h:270` | `setIsGameSystemStatus` | reached (1 use lines) |
| 182 | decl | `SystemData.h:271` | `removeMultiDiskContent` | reached (3 use lines) |
| 183 | decl | `SystemData.h:273` | `loadSystem` | reached (6 use lines) |
| 184 | decl | `SystemData.h:274` | `loadAdditionnalConfig` | reached (3 use lines) |
| 185 | decl | `SystemData.h:279` | `populate` | reached (5 use lines) |
| 186 | decl | `LaunchCommand.h:28` | `launchToken` | reached (2 use lines) |
| 187 | decl | `LaunchCommand.h:39` | `wordEnd` | reached (4 use lines) |
| 188 | decl | `LaunchCommand.h:51` | `launchArgument` | reached (4 use lines) |
| 189 | decl | `LaunchCommand.h:53` | `launchToken` | reached (2 use lines) |
| 190 | decl | `ProxyCards.h:27` | `linkReturned` | reached (2 use lines) |
| 191 | decl | `ProxyCards.h:32` | `afterSync` | reached (2 use lines) |
| 192 | decl | `ProxyCards.h:34` | `sendRunning` | reached (2 use lines) |
| 193 | decl | `ProxyCards.h:41` | `topUp` | reached (3 use lines) |
| 194 | decl | `ProxyCards.h:44` | `topUpRunning` | reached (3 use lines) |
| 195 | decl | `ProxyCards.h:47` | `stopTopUp` | reached (2 use lines) |
| 196 | decl | `ProxyCards.h:55` | `indexRanOffline` | reached (3 use lines) |
| 197 | decl | `SaveState.h:13` | `isSlotValid` | reached (3 use lines) |
| 198 | decl | `SaveState.h:22` | `getScreenShot` | reached (11 use lines) |
| 199 | decl | `SaveState.h:25` | `remove` | reached (120 use lines) |
| 200 | decl | `SaveState.h:26` | `copyToSlot` | reached (2 use lines) |
| 201 | decl | `SaveState.h:33` | `makeStateFilename` | reached (5 use lines) |
| 202 | decl | `SaveState.h:35` | `setupSaveState` | reached (1 use lines) |
| 203 | decl | `SaveState.h:36` | `onGameEnded` | reached (1 use lines) |
| 204 | decl | `SaveState.h:39` | `SaveState` | reached (53 use lines) |
| 205 | decl | `SaveState.h:47` | `SaveState` | reached (53 use lines) |
| 206 | decl | `SaveStateRepository.h:16` | `SaveStateRepository` | reached (49 use lines) |
| 207 | decl | `SaveStateRepository.h:17` | `~SaveStateRepository` | reached by `delete`/scope end (destructor) |
| 208 | decl | `SaveStateRepository.h:19` | `isEnabled` | reached (42 use lines) |
| 209 | decl | `SaveStateRepository.h:20` | `getNextFreeSlot` | reached (1 use lines) |
| 210 | decl | `SaveStateRepository.h:21` | `renumberSlots` | **unreached** since D-UI-069 removed batocera's call (SR-1). Already written: nothing; it renames slots only when called, and no device holds anything it left that this code reads. Exposed: a rename of every slot above a gap, which the save sync reads as a delete plus a new file |
| 211 | decl | `SaveStateRepository.h:23` | `supportsAutoSave` | reached (1 use lines) |
| 212 | decl | `SaveStateRepository.h:24` | `supportsIncrementalSaveStates` | reached (6 use lines) |
| 213 | decl | `SaveStateRepository.h:25` | `hasSaveStates` | reached (4 use lines) |
| 214 | decl | `SaveStateRepository.h:27` | `getSaveStates` | reached (6 use lines) |
| 215 | decl | `SaveStateRepository.h:29` | `clear` | reached (247 use lines) |
| 216 | decl | `SaveStateRepository.h:30` | `refresh` | reached (12 use lines) |
| 217 | decl | `SaveStateRepository.h:32` | `getGameAutoSave` | reached (1 use lines) |
| 218 | decl | `SaveStateRepository.h:33` | `getDefaultAutoSaveSaveState` | reached (3 use lines) |
| 219 | decl | `SaveStateRepository.h:34` | `getDefaultNewGameSaveState` | reached (2 use lines) |
| 220 | decl | `SaveStateRepository.h:36` | `getEmptySaveState` | reached (2 use lines) |
| 221 | decl | `SaveStateRepository.h:44` | `onDisk` | reached (6 use lines) |
| 222 | decl | `SaveStateRepository.h:45` | `anyOnDisk` | reached (2 use lines) |
| 223 | decl | `SaveStateConfigFile.h:13` | `SaveStateCoreConfig` | reached (5 use lines) |
| 224 | decl | `SaveStateConfigFile.h:24` | `SaveStateConfig` | reached (34 use lines) |
| 225 | decl | `SaveStateConfigFile.h:26` | `Default` | reached (8 use lines) |
| 226 | decl | `SaveStateConfigFile.h:30` | `matchSlotFile` | reached (1 use lines) |
| 227 | decl | `SaveStateConfigFile.h:31` | `matchAutoFile` | reached (1 use lines) |
| 228 | decl | `SaveStateConfigFile.h:32` | `getDirectory` | reached (2 use lines) |
| 229 | decl | `SaveStateConfigFile.h:51` | `equals` | reached (3 use lines) |
| 230 | decl | `SaveStateConfigFile.h:56` | `isDefaultConfig` | **unreached** (upstream-carried; `isActiveConfig` is the one used, `SaveState.cpp:60`). Already written: nothing (a read). Exposed: nothing |
| 231 | decl | `SaveStateConfigFile.h:57` | `isActiveConfig` | reached (3 use lines) |
| 232 | decl | `SaveStateConfigFile.h:68` | `SetupRegEx` | reached (2 use lines) |
| 233 | decl | `SaveStateConfigFile.h:74` | `isEnabled` | reached (42 use lines) |
| 234 | decl | `SaveStateConfigFile.h:75` | `getSaveStateConfigs` | reached (8 use lines) |
| 235 | decl | `SaveStateConfigFile.h:78` | `SaveStateConfigFile` | reached (21 use lines) |
| 236 | decl | `SaveStateConfigFile.h:79` | `getSaveStateConfig` | reached (1 use lines) |
| 237 | decl | `SaveStateConfigFile.h:81` | `Instance` | reached (53 use lines) |
| 238 | decl | `SaveStateJobQueue.h:42` | `enqueueDelete` | reached (1 use lines) |
| 239 | decl | `SaveStateJobQueue.h:45` | `enqueueCopy` | reached (1 use lines) |
| 240 | decl | `SaveStateJobQueue.h:50` | `take` | reached (24 use lines) |
| 241 | decl | `SaveStateJobQueue.h:54` | `finish` | reached (15 use lines) |
| 242 | decl | `SaveStateJobQueue.h:57` | `isPending` | reached (4 use lines) |
| 243 | decl | `SaveStateJobQueue.h:60` | `completed` | reached (55 use lines) |
| 244 | decl | `SaveStateBookkeeper.h:49` | `deleteLater` | reached (1 use lines) |
| 245 | decl | `SaveStateBookkeeper.h:53` | `recordCopy` | reached: `GuiSaveState.cpp:524` (a call split across two lines, read by hand) |
| 246 | decl | `SaveStateBookkeeper.h:58` | `isPending` | reached (4 use lines) |
| 247 | decl | `SaveStateBookkeeper.h:61` | `completed` | reached (55 use lines) |
| 248 | decl | `SaveStateBookkeeper.h:66` | `holdsTransferLock` | reached (1 use lines) |
| 249 | decl | `SaveStateBookkeeper.h:70` | `shutdown` | reached (18 use lines) |
| 250 | decl | `views/ViewController.h:29` | `init` | reached (88 use lines) |
| 251 | decl | `views/ViewController.h:30` | `deinit` | reached (56 use lines) |
| 252 | decl | `views/ViewController.h:32` | `hasInstance` | reached (4 use lines) |
| 253 | decl | `views/ViewController.h:39` | `configurationReplaced` | reached (2 use lines) |
| 254 | decl | `views/ViewController.h:41` | `get` | reached (1321 use lines) |
| 255 | decl | `views/ViewController.h:43` | `~ViewController` | reached by `delete`/scope end (destructor) |
| 256 | decl | `views/ViewController.h:47` | `preload` | reached (1 use lines) |
| 257 | decl | `views/ViewController.h:51` | `reloadGameListView` | reached (13 use lines) |
| 258 | decl | `views/ViewController.h:52` | `reloadGameListView` | reached (13 use lines) |
| 259 | decl | `views/ViewController.h:65` | `remakeGameListView` | reached (2 use lines) |
| 260 | decl | `views/ViewController.h:66` | `reloadSystemListViewTheme` | reached (2 use lines) |
| 261 | decl | `views/ViewController.h:68` | `reloadAll` | reached (78 use lines) |
| 262 | decl | `views/ViewController.h:71` | `goToNextGameList` | reached (1 use lines) |
| 263 | decl | `views/ViewController.h:72` | `goToPrevGameList` | reached (1 use lines) |
| 264 | decl | `views/ViewController.h:73` | `goToGameList` | reached (16 use lines) |
| 265 | decl | `views/ViewController.h:74` | `goToGameList` | reached (16 use lines) |
| 266 | decl | `views/ViewController.h:75` | `goToSystemView` | reached (10 use lines) |
| 267 | decl | `views/ViewController.h:76` | `goToSystemView` | reached (10 use lines) |
| 268 | decl | `views/ViewController.h:77` | `goToStart` | reached (9 use lines) |
| 269 | decl | `views/ViewController.h:78` | `ReloadAndGoToStart` | reached (1 use lines) |
| 270 | decl | `views/ViewController.h:80` | `onFileChanged` | reached (27 use lines) |
| 271 | decl | `views/ViewController.h:84` | `launch` | reached (63 use lines) |
| 272 | decl | `views/ViewController.h:85` | `launch` | reached (63 use lines) |
| 273 | decl | `views/ViewController.h:88` | `update` | reached (267 use lines) |
| 274 | decl | `views/ViewController.h:89` | `render` | reached (191 use lines) |
| 275 | decl | `views/ViewController.h:105` | `getSystem` | reached (216 use lines) |
| 276 | decl | `views/ViewController.h:112` | `getState` | reached (181 use lines) |
| 277 | decl | `views/ViewController.h:115` | `getHelpStyle` | reached (12 use lines) |
| 278 | decl | `views/ViewController.h:117` | `getGameListView` | reached (28 use lines) |
| 279 | decl | `views/ViewController.h:118` | `getSystemListView` | reached (5 use lines) |
| 280 | decl | `views/ViewController.h:119` | `removeGameListView` | reached (1 use lines) |
| 281 | decl | `views/ViewController.h:121` | `onThemeChanged` | reached (30 use lines) |
| 282 | decl | `views/ViewController.h:123` | `onShow` | reached (68 use lines) |
| 283 | decl | `views/ViewController.h:124` | `onScreenSaverActivate` | reached (18 use lines) |
| 284 | decl | `views/ViewController.h:125` | `onScreenSaverDeactivate` | reached (18 use lines) |
| 285 | decl | `views/ViewController.h:127` | `getSelectedSystem` | reached (2 use lines) |
| 286 | decl | `views/ViewController.h:128` | `getViewMode` | reached (1 use lines) |
| 287 | decl | `views/ViewController.h:130` | `reloadAllGames` | reached (13 use lines) |
| 288 | decl | `views/ViewController.h:132` | `setActiveView` | reached (1 use lines) |
| 289 | decl | `views/ViewController.h:134` | `hitTest` | reached (48 use lines) |
| 290 | decl | `views/ViewController.h:137` | `ViewController` | reached (268 use lines) |
| 291 | decl | `views/ViewController.h:140` | `playViewTransition` | reached (3 use lines) |
| 292 | decl | `views/ViewController.h:141` | `doLaunchGame` | reached (3 use lines) |
| 293 | decl | `views/ViewController.h:142` | `checkLaunchOptions` | reached (1 use lines) |
| 294 | decl | `views/ViewController.h:143` | `getSystemId` | reached (3 use lines) |
| 295 | decl | `views/ViewController.h:144` | `changeVolume` | reached (2 use lines) |
| 296 | static | `FileData.cpp:117` | `steadyMs` | reached (5 use lines) |
| 297 | static | `FileData.cpp:122` | `captureAgeSeconds` | reached (2 use lines) |
| 298 | static | `FileData.cpp:528` | `formatCommandLineArgument` | reached (2 use lines) |
| 299 | static | `FileData.cpp:774` | `launchNow` | reached (4 use lines) |
| 300 | static | `FileData.cpp:800` | `rememberSaveState` | reached (1 use lines) |
| 301 | static | `FileData.cpp:818` | `launchWhenGone` | reached (3 use lines) |
| 302 | static | `FileData.cpp:876` | `captureGate` | reached (1 use lines) |
| 303 | static | `FileData.cpp:1343` | `getTokens` | reached (2 use lines) |
| 304 | static | `SystemData.cpp:312` | `dropCollectionEntries` | reached (1 use lines) |
| 305 | static | `SaveState.cpp:47` | `_changeCommandlineArgument` | reached (2 use lines) |
| 306 | static | `SaveStateConfigFile.cpp:171` | `readXmlValue` | reached (18 use lines) |
| 307 | static | `main.cpp:380` | `crashWrite` | reached (4 use lines) |
| 308 | static | `main.cpp:622` | `startStartupSavesSync` | reached (1 use lines) |
| 309 | pp | `FileData.h:2` | `#ifndef ES_APP_FILE_DATA_H` | include guard: shipped |
| 310 | pp | `SystemData.h:2` | `#ifndef ES_APP_SYSTEM_DATA_H` | include guard: shipped |
| 311 | pp | `LaunchCommand.h:2` | `#ifndef ES_APP_LAUNCH_COMMAND_H` | include guard: shipped |
| 312 | pp | `ProxyCards.h:2` | `#ifndef ES_APP_PROXY_CARDS_H` | include guard: shipped |
| 313 | pp | `views/ViewController.h:2` | `#ifndef ES_APP_VIEWS_VIEW_CONTROLLER_H` | include guard: shipped |
| 314 | pp | `FileData.cpp:43` | `#if defined(__GLIBC__)` | shipped (glibc) |
| 315 | pp | `FileData.cpp:633` | `#ifdef WIN32` | unreached on the image (no WIN32) |
| 316 | pp | `FileData.cpp:635` | `#else` | shipped (the opposite of a WIN32 `#if`) |
| 317 | pp | `FileData.cpp:672` | `#if WIN32` | unreached on the image (no WIN32) |
| 318 | pp | `FileData.cpp:677` | `#if ROCKNIX` | shipped (`-DROCKNIX=1`, package.mk:19) |
| 319 | pp | `FileData.cpp:679` | `#else` | unreached on the image (the `#else` of `#if ROCKNIX`: upstream's form) |
| 320 | pp | `FileData.cpp:685` | `#if WIN32` | unreached on the image (no WIN32) |
| 321 | pp | `FileData.cpp:690` | `#if ROCKNIX` | shipped (`-DROCKNIX=1`, package.mk:19) |
| 322 | pp | `FileData.cpp:692` | `#else` | unreached on the image (the `#else` of `#if ROCKNIX`: upstream's form) |
| 323 | pp | `FileData.cpp:744` | `#if WIN32` | unreached on the image (no WIN32) |
| 324 | pp | `FileData.cpp:746` | `#else` | shipped (the opposite of a WIN32 `#if`) |
| 325 | pp | `FileData.cpp:1077` | `#if defined(__GLIBC__)` | shipped (glibc) |
| 326 | pp | `FileData.cpp:1213` | `#if defined(__GLIBC__)` | shipped (glibc) |
| 327 | pp | `FileData.cpp:1863` | `#if DEBUG` | unreached (not a DEBUG build) |
| 328 | pp | `FileData.cpp:1875` | `#if DEBUG` | unreached (not a DEBUG build) |
| 329 | pp | `FileData.cpp:1889` | `#if DEBUG` | unreached (not a DEBUG build) |
| 330 | pp | `FileData.cpp:1956` | `#if WIN32 && !_DEBUG` | unreached on the image (no WIN32): the `#else` beside it ships |
| 331 | pp | `FileData.cpp:1958` | `#else` | shipped (the opposite of `WIN32 && !_DEBUG`) |
| 332 | pp | `FileData.cpp:2006` | `#if WIN32 && !_DEBUG` | unreached on the image (no WIN32): the `#else` beside it ships |
| 333 | pp | `FileData.cpp:2008` | `#else` | shipped (the opposite of `WIN32 && !_DEBUG`) |
| 334 | pp | `FileData.cpp:2035` | `#if WIN32 && !_DEBUG` | unreached on the image (no WIN32): the `#else` beside it ships |
| 335 | pp | `FileData.cpp:2037` | `#else` | shipped (the opposite of `WIN32 && !_DEBUG`) |
| 336 | pp | `FileData.cpp:2044` | `#if WIN32 && !_DEBUG` | unreached on the image (no WIN32): the `#else` beside it ships |
| 337 | pp | `FileData.cpp:2046` | `#else` | shipped (the opposite of `WIN32 && !_DEBUG`) |
| 338 | pp | `SystemData.cpp:35` | `#if WIN32` | unreached on the image (no WIN32) |
| 339 | pp | `SystemData.cpp:2134` | `#if WIN32 && !_DEBUG` | unreached on the image (no WIN32): the `#else` beside it ships |
| 340 | pp | `SystemData.cpp:2136` | `#else` | shipped (the opposite of `WIN32 && !_DEBUG`) |
| 341 | pp | `SystemData.cpp:2152` | `#if WIN32 && !_DEBUG` | unreached on the image (no WIN32): the `#else` beside it ships |
| 342 | pp | `SystemData.cpp:2154` | `#else` | shipped (the opposite of `WIN32 && !_DEBUG`) |
| 343 | pp | `SaveStateRepository.cpp:15` | `#if WIN32` | unreached on the image (no WIN32) |
| 344 | pp | `SaveStateRepository.cpp:121` | `#if WIN32` | unreached on the image (no WIN32) |
| 345 | pp | `SaveStateRepository.cpp:123` | `#else` | shipped (the opposite of a WIN32 `#if`) |
| 346 | pp | `SaveStateBookkeeper.cpp:12` | `#if !defined(_WIN32)` | shipped |
| 347 | pp | `SaveStateBookkeeper.cpp:23` | `#ifndef CLOUD_SYNC_LOCK_PATH` | shipped (the device's lock path; a test defines its own) |
| 348 | pp | `SaveStateBookkeeper.cpp:121` | `#if defined(_WIN32)` | unreached on the image (no WIN32) |
| 349 | pp | `SaveStateBookkeeper.cpp:123` | `#else` | shipped (the opposite of a WIN32 `#if`) |
| 350 | pp | `SaveStateBookkeeper.cpp:143` | `#if !defined(_WIN32)` | shipped |
| 351 | pp | `views/ViewController.cpp:492` | `#ifdef _RPI_` | unreached (no BCMHOST/RPI) |
| 352 | pp | `views/ViewController.cpp:869` | `#if !WIN32` | shipped |
| 353 | pp | `views/ViewController.cpp:895` | `#if WIN32` | unreached on the image (no WIN32) |
| 354 | pp | `main.cpp:42` | `#ifdef __GLIBC__` | shipped (glibc) |
| 355 | pp | `main.cpp:65` | `#ifdef WIN32` | unreached on the image (no WIN32) |
| 356 | pp | `main.cpp:262` | `#ifdef WIN32` | unreached on the image (no WIN32) |
| 357 | pp | `main.cpp:356` | `#ifdef WIN32` | unreached on the image (no WIN32) |
| 358 | pp | `main.cpp:363` | `#if WIN32` | unreached on the image (no WIN32) |
| 359 | pp | `main.cpp:365` | `#else` | shipped (the opposite of a WIN32 `#if`) |
| 360 | pp | `main.cpp:417` | `#ifdef __GLIBC__` | shipped (glibc) |
| 361 | pp | `main.cpp:701` | `#ifdef WIN32` | unreached on the image (no WIN32) |
| 362 | pp | `main.cpp:721` | `#ifdef __GLIBC__` | shipped (glibc) |
| 363 | pp | `main.cpp:740` | `#ifdef WIN32` | unreached on the image (no WIN32) |
| 364 | pp | `main.cpp:773` | `#ifdef FREEIMAGE_LIB` | unreached (no CMakeLists defines FREEIMAGE_LIB) |
| 365 | pp | `main.cpp:798` | `#if !WIN32` | shipped |
| 366 | pp | `main.cpp:874` | `#ifdef _ENABLE_KODI_` | unreached (`-DDISABLE_KODI=1`) |
| 367 | pp | `main.cpp:1129` | `#ifdef WIN32` | unreached on the image (no WIN32) |
| 368 | pp | `main.cpp:1154` | `#ifdef BATOCERA` | unreached (no -DBATOCERA) |
| 369 | pp | `main.cpp:1198` | `#ifdef BATOCERA` | unreached (no -DBATOCERA) |
| 370 | pp | `main.cpp:1350` | `#ifdef FREEIMAGE_LIB` | unreached (no CMakeLists defines FREEIMAGE_LIB) |

### Q7 Clarity and structure
- `FileData.cpp` holds five responsibilities in 2,680 lines, and `launchGame` alone is 400 lines (§ 3.1).
- Nothing in the three big files says which lines are batocera's and which the fork's (the hunk maps above). A header line naming the provenance would save a reader the `git diff`.
- **FD-4:** `getlaunchCommand` writes `system.cfg`.
  - **The row for PL-031 (S1, deferred to #678).** The builder seeds `global.netplay.nickname` with the application's name plus `Player` and saves `system.cfg` when the key is empty (`FileData.cpp:653-657`, pin numbering). Three readers rely on that seeding without saying so: the NICKNAME row of `GuiNetPlaySettings.cpp:26`, the NETPLAY NICKNAME row of `GuiGameOptions.cpp:203` (both `addInputTextConfigRow` over the stored key), and `SystemData.cpp:1854`'s export. On a fresh device, any launch fills the key, so those rows show the default. Removing only the write would leave them empty.
  - **The proposed move:** the default is supplied where netplay is enabled or where those two pages load, either by seeding once or by a read that falls back. The builder then reads the key and falls back to the same default without saving. That reaches two files of T31's (#678) and one of T2's, so it is a lead for T31 on #649, and S1 does not change the builder alone.
  - **Already written:** devices hold the seeded or chosen nickname, which is read as it is.
- **FD-13:** the renumbering comment.
- **MN-4:** three stale comments.
- **SS-3:** duplicated arms.
- **VC-3:** three copies of the end callback.
- **ProxyCards:** the comments carry audit identifiers as much as rules.
- **SD-6:** dead commented code.
- The three readers of one argument line (Q1).

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)
- `tools/es-untranslated` counts only `_()` strings, so a player string outside `_()` has no French and no checker sees it (MN-5). This is a tool change for the tooling slice, not a rule.
- `tools/vocabulary-check` judges three word pairs. A verb outside the two (MN-6, `DOWNLOAD`) passes. Same owner.

### Codification Gaps (needs-new-rule)
- `time-to-play.md`'s paragraph on what ships (D-CLOUD-076/109) is stale against D-CLOUD-130. That is a doctrine edit for the doctrine slice, found here and not this lane's to make (D-WORKFLOW-189).

### Recommended Action Sequence
At stage D, the punch list and the bug issues. Then the coordinator's stream briefs (stage E). The leads are posted on #649 for their slices.

### Handoff to Phase Z.6
None; the retro is at stage G.

## Second opinion (Phase 4.6)

**Primary:** Claude Code, `anthropic/claude-opus-5-5`, Anthropic; identity source: the dispatch on #649 (2026-10-23T17:21:03Z) and the session's model metadata.
**Depth:** extended. **Perspectives:** 3 including the primary. **External reviewers:** 2, each from a different lab (OpenAI, Google). **Calls:** one refutation pass each (epic tier), each preceded by a probe.

**Run:** `tools/watch-build --record-only -- tools/council/run invoke --member <m> --provider openrouter --prompt-file <abs>/second-opinions/<m>-brief.md --output <abs>/second-opinions/<m>-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`. The key comes from `~/.config/council/env`, sourced by the runner. The two calls ran one after the other (one watched run per worktree; Argon's first start was refused before any provider call, 19:07:05).

**Identity** (each Facilitator receipt, `council-facilitator@1.14.1-pixelelated.2`):

| Seat | Probe | Refutation pass | Observed model / provider | Effort | Output sha256 |
| --- | --- | --- | --- | --- | --- |
| `gpt` | 19:06:24, rc 0, `provider_response` PASS | 19:07:00-19:26:32, rc 0, 1,171,305 ms, 0 retries, 37,984 reasoning tokens, brief sha256 `d1224767ab90...` | `openai/gpt-6-astra` / OpenAI (PASS) | max, PASS | `4929f876acc19700ae4b3bb9158744b87640004452b31470868c05af43d3bad5` |
| `gemini-argon` | 19:06:37, rc 0, `provider_response` PASS | 19:26:4x-19:40:3x, rc 0, 825,007 ms, 1 retry, 38,024 reasoning tokens, brief sha256 `f74ef056b128...` | `google/gemini-4-argon` / Google (PASS) | high, PASS | `9c89f7c6ea305b25669c27f0d0474481a318ff259133e516225cac109ef0d812` |

Every seat item is a lead. Each grade below rests on the orchestrator's own read of the pin (`git show $PIN:<path>`) or on a guest artifact, never on the packet.

### Astra's items, graded against the artifacts

| Seat item | Orchestrator's grade | Evidence |
| --- | --- | --- |
| SS-1 should be High: `$(...)`/backtick in a state file name executes a command | **agree, re-graded Medium → High** (Argon's dissent below) | `SaveState.cpp:77,97,111` double quotes; G-6 shows the shell expanding inside them on the shipped path; ES runs commands through `/bin/sh` (`FileData.cpp:1100-1103`) as root on the image |
| SD-2 Medium; `rfind("windows")` is case-sensitive | **agree, narrowed** (lowercase only; `Windows 95 era` is not matched) | `SystemData.cpp:631` |
| FD-14: the containment seam is still live through the metadata loop and a failed unlink; `.ccd` builds names without opening | **agree, re-graded Low → Medium** | `FileData.cpp:1487-1494` removes every existing `MD_PATH` file wherever it points; `:1503` is unchecked; `:1424-1430` builds `.ccd` siblings without reading the file |
| VC-1 Low; keep the timing to `POST /launch`; return 800/600/10 ms | **agree, narrowed** | `ViewController.cpp:626,647,666`; G-8 used the API |
| FD-8 should be Medium | **disagree, kept Low**: reachable only through the loopback API's reload during a wait; the fix is in the item | `main.cpp:818`; G-search of the rescan posts (`FileData.cpp:1223`, `GuiCloudTransfer.cpp:335`) |
| SD-3 should be Medium | **agree, re-graded Low → Medium** (Argon concurs with G-04 folded in) | G-5; `SystemData.cpp:1039-1050` |
| SD-4/FD-15 should be Medium | **agree, re-graded Low → Medium** | G-9 (status 134), control 27 |
| MN-3 Medium, limited to the stale replay | **agree, re-graded Low → Medium** (Argon concurs) | `main.cpp:529-540`; `FileData.cpp:703-714` bakes the state arguments |
| SB-2: the exact spin is unproved; the unbounded retry stands | **agree, narrowed** | `SaveStateBookkeeper.cpp:159-173` |
| FD-18 Low, a real race | **confirmed** | `FileData.cpp:83,1094,1111`; `ProxyCards.cpp:269,410,416` |
| LC-1 reachable with a quoted custom template | **agree, narrowed** | `LaunchCommand.h:39-41` copies the word's bytes |
| FD-2/FD-3 Medium as conditional command execution | **agree, re-graded Low → Medium** (a benign custom template plus a scraped name is enough) | `FileData.cpp:528-534,624-630` |
| FD-9/FD-19 Medium on their optional path | **agree** for T33's lead (not this slice's fix) | `Scripting.cpp:88-113` |
| G-01 save-state pointer protected too late (dialogs before `rememberSaveState`) | **confirmed, Low, folded into FD-8's item** (Argon G-06 the same) | `ViewController.cpp:500,520`; `FileData.cpp:939` |
| G-02 a completed capture loses its exit sync when the retried launch is refused | **confirmed, Low** (the saves stay local and go up at the next game's exit sync) | `FileData.cpp:921-923`, `:1295`, `:1303`; Argon G-01 the same |
| G-03 the rescan misses changes inside subfolders | **confirmed, Low** (documented limitation at `SystemData.cpp:356-357`; Argon G-03 adds the missing multi-disk filter) | `SystemData.cpp:385-387,434` |
| G-04 deletion proceeds without the retirement record | **disagree, withdrawn**: decided by D-CLOUD-133 (the worker unlinks what the script left; the player asked) | `SaveStateBookkeeper.h:13-21`; `docs/decision-register.md` D-CLOUD-133 |
| G-05 fallback NEW GAME strands the auto save in `.bak` | **confirmed, Low** (the `racommands` fallback only, SS-2's path) | `SaveState.cpp:81-83,114-133,166-169` |
| G-06 a later placeholder rewrites inserted data | **confirmed, Low, folded into FD-2's item** (Argon G-02 the same) | `FileData.cpp:622-648` |
| G-07 forced-option detection by substring | **confirmed, Low, folded into FD-2's item** (FD-5 had it as inert on the shipped command) | `FileData.cpp:611-615` |
| G-08 an explicitly empty option reads as absent | **confirmed, Low, folded into LC-1** | `LaunchCommand.h:53-54` |
| G-09 PLAY NOW permission is global | **confirmed, Low** | `FileData.cpp:938`, `:1038` |
| G-10 the top-up card's screen check expires before the post runs | **confirmed, Low** | `ProxyCards.cpp:253-262` |
| G-11 the 3-second card wait is not a bound | **agree, narrowed into G-10's item**: unbounded only if the interface thread stalls after claiming, when everything stalls | `ProxyCards.cpp:263-264` |
| G-12 `executeScript`'s quote test | **confirmed, a lead for T33** (Argon G-10 the same) | `Scripting.cpp:104-105` |
| G-13 play time includes the return processing | **confirmed, Low** | `FileData.cpp:1088`, `:1199-1203` |

### Argon's items, graded against the artifacts

| Seat item | Orchestrator's grade | Evidence |
| --- | --- | --- |
| SS-1 Medium, not High (a single-user handheld) | **disagree, kept at High** (Astra's grade): a ROM name from a downloaded set runs as a root command, and that is a security defect whoever owns the device | as above; G-6 |
| SD-2: the intent is to skip subfolders of the `ports`/`windows` systems | **agree, narrowed**: the fix compares the system name for those two | `SystemData.cpp:619-632` |
| FD-14 back to Medium (the metadata loop; broken multi-disc delete) | **agree, re-graded Low → Medium** | as Astra's row |
| VC-1 Low | **agree** | G-8 |
| FD-8 Low | **agree** | |
| SD-3 Medium with G-04 | **agree, re-graded** | G-5 |
| SD-4 Medium (a possible boot loop when it is the start system with the list) | **agree, re-graded** | G-9 |
| MN-3 Medium (baked `-state_slot -1`, stale core; p2k and rotation skipped) | **agree, re-graded**; G-08 folded in | `main.cpp:527-572`; `SaveState.cpp:74-75` |
| SB-2 Low | **agree** | |
| FD-18 Low | **confirmed** | |
| FD-1 narrow: the MITM session is dropped too | **agree** (it was in FD-1) | `FileData.cpp:667-678` |
| G-01 the capture's exit sync lost on a refused retry | **confirmed, Low** (same as Astra's G-02) | `FileData.cpp:897-924`, `:1295-1307` |
| G-02 a later placeholder rewrites the ROM path | **confirmed, Low, folded into FD-2's item** | `FileData.cpp:622-648` |
| G-03 the rescan: same-second changes missed; no multi-disk filter | **confirmed, Low, folded with Astra's G-03** | `SystemData.cpp:385-387,434` (no `removeMultiDiskContent` in the rescan) |
| G-04 overlay order and child-element tags deleted | **confirmed, Low, folded into SD-3's item** | `SystemData.cpp:1026-1029`, `:1081-1084` |
| G-05 `onShow` not called after a refusal; `windows_installers` leaves input locked | **agree, narrowed**: the refusal arm lacks `onShow`. The `windows_installers` arm reloads the whole `ViewController` (`:622`), so its lock goes with it. Low, folded into VC-1's item | `ViewController.cpp:478`, `:615-668` |
| G-06 `saveStateInfo` dangling in the dialogs; `mCurrentView` dereferenced unchecked | **confirmed, Low, folded into FD-8's item** | `ViewController.cpp:577-579` |
| G-07 `.cue` `FILE` lines not trimmed; `\` not normalised | **agree, narrowed**: `FILE` is top-level in a standard cue sheet, but a UTF-8 BOM or leading space on its line defeats `startsWith`. Low, folded into FD-14's item (the same function) | `FileData.cpp:1411-1419` |
| G-08 the boot game skips `convertP2kFile` and the rotation record | **confirmed, folded into MN-3** | `main.cpp:527-572` |
| G-09 `attach` blocks 3 s while a game holds the screen | **disagree, withdrawn**: by design and bounded (`ProxyCards.cpp:240-243`: the run goes on without a card) | `:263` |
| G-10 `executeScript` quote test; `break` drops `arg3` | **confirmed, a lead for T33** | `Scripting.cpp:100-106` |
| G-11 `populateFolder` leaks a folder already in the map | **confirmed, Low** (upstream lines) | `SystemData.cpp:642-647` |
| G-12 the lock flag cleared before the lock | **confirmed, Low**: the window is in the safe direction (a DELETE refused for a moment) | `SaveStateBookkeeper.cpp:146-147` |
| G-13 `/tmp/game.xml` removed on every build; the host's `--port ''` when unset | **agree, narrowed**: the removal is harmless. The port has a shipped default (`system.cfg:74`, `55435`), so it needs a cleared setting. Low, folded into FD-1's item | `FileData.cpp:644`, `:691` |

**Net effect:**
- **Re-graded:** SS-1 to High; FD-14, SD-3, SD-4, MN-3 and FD-2/FD-3 to Medium; LC-1, SB-2, SD-2 and VC-1 narrowed.
- **New items:** five, from the seats' findings. The capture's exit sync on a refused retry, the rescan's limits, the fallback NEW GAME `.bak`, the global PLAY NOW, and the play-time measure come from Astra; the `populateFolder` leak from Argon. The top-up card's re-check is folded with its sibling.
- **Folded into existing items:** ten seat items.
- **Withdrawn, with their artifact:** two (Astra G-04 by D-CLOUD-133; Argon G-09 by design).
- **Disagreements recorded:** two (FD-8 kept Low against Astra; SS-1 kept High against Argon).
- **Leads for other slices:** the `Scripting` quoting (T33/T21).
- **What both said they could not judge from the packet:** the unexcerpted ranges, the launcher's reading, the notification teardown, the `FolderMerge` ownership, and the startup sync against a boot game's saves. This is carried into § Coverage Boundary: those claims rest on this lane's own reading and guest proofs, not on the second reading.

## Quality Self-Check

- Every finding cites `file:line` at the pin, read this session. Phase 4.5 re-read the graded ones.
- No verdict rests on tracker state.
- Every runtime claim is a lead, held for the guest.
- Two findings were corrected by caller searches (FD-1, FD-8), and the corrections are recorded where they happened.
- The counts that differ from the brief are written as deltas (`rocknix/master`'s hash, #120's state, the conditional count, the reader on the HTTP thread, Scripting's slice).
