# Forward audit — M6.P2 T33, EmulationStation's system layer (#680)

Composed by `tools/t33-02.py` from this template and the generators under `tools/`. Each generated section ends with its generator's own "generated, asserted" line, and each generator was seen to exit 1 on a constructed drift before it was trusted (`stage-b/generators.txt`). The ES worktree is read at the pin `16dbac5211` by `git -C` only. The distribution was reviewed at `27bd8499f1`. Depth: Independent, one seat (GPT-6 Astra at `max`), at stage C.

Every proof carries `proved:` in #680's vocabulary: `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`. A `fixture` is a stage-C harness that extracts the pin's code as written and is seen to FAIL at the pin and PASS under its `--control` (`stage-c/runs.txt`). The brief is `docs/reviews/briefs/es-app-system.md` at `c48f8b387e`; its § numbers are cited as "brief § N".

## Coverage

The 77 paths, one row each. The read tier is from `git diff` against the fork's base `bccd715707`: added, modified, or neither. The inventory tier is fork-own for the first two and upstream-carried for the third. The fork's numstat is against `bccd715707`, which equals the merge base `cada856d86`'s and `rocknix/master`'s for every row (`stage-a/runs.out`: the three shortstats are equal).

| Path | Lines (`grep -c ''`) | Inventory tier | Read tier | Fork +/- (against `bccd715707`) | Leads naming it |
| --- | ---: | --- | --- | ---: | --- |
| `es-app/CMakeLists.txt` | 363 | fork-own | fork-modified | 44/0 | - |
| `es-app/EmulationStation.h.in` | 27 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/AppWindow.h` | 56 | fork-own | fork-added | 56/0 | L-12, 3.40 |
| `es-app/src/CaptureRotation.cpp` | 188 | fork-own | fork-added | 188/0 | L-02, L-03, 3.33 |
| `es-app/src/CaptureRotation.h` | 39 | fork-own | fork-added | 39/0 | - |
| `es-app/src/CaptureRotationText.cpp` | 164 | fork-own | fork-added | 164/0 | - |
| `es-app/src/CaptureRotationText.h` | 68 | fork-own | fork-added | 68/0 | - |
| `es-app/src/CheevosIndex.cpp` | 30 | fork-own | fork-added | 30/0 | - |
| `es-app/src/CheevosIndex.h` | 47 | fork-own | fork-added | 47/0 | - |
| `es-app/src/CheevosRetry.cpp` | 31 | fork-own | fork-added | 31/0 | - |
| `es-app/src/CheevosRetry.h` | 47 | fork-own | fork-added | 47/0 | - |
| `es-app/src/CloudExit.h` | 30 | fork-own | fork-added | 30/0 | - |
| `es-app/src/CloudFolderValidation.cpp` | 96 | fork-own | fork-added | 96/0 | - |
| `es-app/src/CloudFolderValidation.h` | 33 | fork-own | fork-added | 33/0 | - |
| `es-app/src/CloudOffer.cpp` | 84 | fork-own | fork-added | 84/0 | L-18 |
| `es-app/src/CloudOffer.h` | 33 | fork-own | fork-added | 33/0 | - |
| `es-app/src/CollectionSystemManager.cpp` | 1631 | upstream-carried | upstream-carried | 0/0 | L-06, L-23, 3.16, 3.17, 3.18, 3.19, 3.20 |
| `es-app/src/CollectionSystemManager.h` | 149 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/ContentInstaller.cpp` | 277 | upstream-carried | upstream-carried | 0/0 | L-10 |
| `es-app/src/ContentInstaller.h` | 65 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/CustomFeatures.cpp` | 537 | upstream-carried | upstream-carried | 0/0 | 3.24, 3.25, 3.26 |
| `es-app/src/CustomFeatures.h` | 157 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/DisplayAspect.cpp` | 153 | fork-own | fork-added | 153/0 | L-04 |
| `es-app/src/DisplayAspect.h` | 42 | fork-own | fork-added | 42/0 | - |
| `es-app/src/DisplayAspectText.cpp` | 76 | fork-own | fork-added | 76/0 | - |
| `es-app/src/DisplayAspectText.h` | 26 | fork-own | fork-added | 26/0 | - |
| `es-app/src/EmulationStation.aps` | 78 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/EmulationStation.h` | 31 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/EmulationStation.rc` | 39 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/FileFilterIndex.cpp` | 1412 | upstream-carried | upstream-carried | 0/0 | L-23, L-27, 3.9, 3.10, 3.11 |
| `es-app/src/FileFilterIndex.h` | 197 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/FileSorts.cpp` | 226 | upstream-carried | upstream-carried | 0/0 | 3.27, 3.28 |
| `es-app/src/FileSorts.h` | 87 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/FileTag.cpp` | 46 | upstream-carried | upstream-carried | 0/0 | L-25, 3.29 |
| `es-app/src/FileTag.h` | 20 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/FolderMerge.h` | 74 | fork-own | fork-added | 74/0 | L-15, 3.37 |
| `es-app/src/GameCubeRvzHashRetry.h` | 45 | fork-own | fork-added | 45/0 | 3.39 |
| `es-app/src/Gamelist.cpp` | 848 | upstream-carried | upstream-carried | 0/0 | L-05, 3.12, 3.13, 3.14, 3.15 |
| `es-app/src/Gamelist.h` | 31 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/Genres.cpp` | 372 | upstream-carried | upstream-carried | 0/0 | 3.8 |
| `es-app/src/Genres.h` | 69 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/JourneyTiers.h` | 159 | fork-own | fork-added | 159/0 | L-16, 3.36 |
| `es-app/src/KeyboardMapping.cpp` | 817 | upstream-carried | upstream-carried | 0/0 | L-28, 3.21, 3.22, 3.23 |
| `es-app/src/KeyboardMapping.h` | 80 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/LangParser.cpp` | 242 | upstream-carried | upstream-carried | 0/0 | L-26, 3.31, 3.32 |
| `es-app/src/LangParser.h` | 27 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/LibretroRatio.cpp` | 53 | upstream-carried | upstream-carried | 0/0 | 3.30 |
| `es-app/src/LibretroRatio.h` | 22 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/MetaData.cpp` | 604 | upstream-carried | upstream-carried | 0/0 | 3.2, 3.3, 3.4, 3.5, 3.6, 3.7 |
| `es-app/src/MetaData.h` | 201 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/NetworkThread.cpp` | 274 | fork-own | fork-modified | 105/3 | L-01, L-12, L-13, L-24 |
| `es-app/src/NetworkThread.h` | 108 | fork-own | fork-modified | 29/1 | - |
| `es-app/src/OfflineAchievementsText.cpp` | 283 | fork-own | fork-added | 283/0 | L-17, 3.41 |
| `es-app/src/OfflineAchievementsText.h` | 161 | fork-own | fork-added | 161/0 | - |
| `es-app/src/PlatformId.cpp` | 301 | upstream-carried | upstream-carried | 0/0 | 3.1 |
| `es-app/src/PlatformId.h` | 196 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/RunLock.h` | 74 | fork-own | fork-added | 74/0 | L-14, 3.38 |
| `es-app/src/ScraperCmdLine.cpp` | 290 | upstream-carried | upstream-carried | 0/0 | L-22 |
| `es-app/src/ScraperCmdLine.h` | 7 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/SystemRandomPlaylist.cpp` | 109 | upstream-carried | upstream-carried | 0/0 | 3.34 |
| `es-app/src/SystemRandomPlaylist.h` | 38 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/SystemScreenSaver.cpp` | 1125 | upstream-carried | upstream-carried | 0/0 | L-11 |
| `es-app/src/SystemScreenSaver.h` | 134 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/TextFit.h` | 40 | fork-own | fork-added | 40/0 | L-20, 3.35 |
| `es-app/src/ThreadedBluetooth.cpp` | 123 | upstream-carried | upstream-carried | 0/0 | L-10 |
| `es-app/src/ThreadedBluetooth.h` | 47 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/WifiText.cpp` | 265 | fork-own | fork-added | 265/0 | L-19 |
| `es-app/src/WifiText.h` | 164 | fork-own | fork-added | 164/0 | - |
| `es-app/src/Win32ApiSystem.cpp` | 1269 | fork-own | fork-modified | 3/3 | L-21 |
| `es-app/src/Win32ApiSystem.h` | 70 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/ZaparooSupport.cpp` | 64 | upstream-carried | upstream-carried | 0/0 | L-09 |
| `es-app/src/ZaparooSupport.h` | 21 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/animations/LaunchAnimation.h` | 67 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/animations/MoveCameraAnimation.h` | 28 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/components/ScraperSearchComponent.cpp` | 755 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/components/ScraperSearchComponent.h` | 112 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/es_icon.ico` | 8 | upstream-carried | upstream-carried | 0/0 | - |

generated, asserted: 77 paths; read tiers fork-added 27, fork-modified 4, upstream-carried 46; inventory fork-own 31, upstream-carried 46

## The leads

The brief's L-01 to L-29 (brief § 2), read at their lines. The lines, the shape and Q are the brief's, carried word for word. Family, owner, disposition and proof are this read's. A disposition is proposed for the stage-D pause, and the coordinator rules. "Rule 6" is `bugs-are-agent-first.md` rule 6: an upstream defect whose fix is contained is still ours to close, with a #585 line (D-WORKFLOW-164), never sent (D-WORKFLOW-165).

| Lead | Lines at the pin | Shape | Q | Family | Owner | Disposition proposed | proved: |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L-01 | `es-core/src/watchers/WatchersManager.cpp:181-196` (every `check()` under `mWatchersLock`), `:92-100` (`ResetComponent` takes the same lock); the interface-thread callers `NetworkThread.cpp:21-25` <- `guis/GuiRetroAchievementsSettings.cpp:806`, `:257`, `:191` | a page close that asks for the token check blocks the interface thread until the check in flight ends: `testAccount`'s HTTPS login (`RetroAchievements.cpp:1035-1038`, bounded by `getHttpOptions()`), `canUpdate`'s or `getPadsInfo`'s script; #308 F-RA-19 moved the sign-in off the thread and left this path back onto it | Q2, Q1 | an unbounded wait on the interface thread | es-core's lock (T21's file, upstream-carried); the three callers the fork's (#175, F-RA-19) | rule 6: a contained fix (`nextCheckTime` under a lock of its own, or `check()` outside `mWatchersLock`) put to the pause with T21 named | tree (the read trace: `WatchersManager.cpp:181-196`, `:92-100`, the three callers; G-09 `CANNOT`) |
| L-02 | `CaptureRotation.cpp:146-163` <- `FileData.cpp:1166-1167` | after every RetroArch exit, on the interface thread, the whole `/var/log/exec.log` (`:158`) and `retroarch.cfg` (`:162`) read and scanned; the only size bound is the launcher's truncation (#280) | Q6, Q2 | work on the interface thread | the fork (#280) | recorded; priced by the retro's time-to-play line | tree (G-03 launched no game: the `stat` not shown) |
| L-03 | `CaptureRotation.cpp:175` against `guis/GuiMenu.cpp:5066` | the rotation record, a saves-tier file the cloud syncs, written in place by `writeAllText` where the journey record beside it is atomic; a truncated record reads as untrusted (benign), D-CLOUD-078 asks for temp-and-rename anyway; Backlog #1186's site (§ 1 e) | Q4 | a write with no last good copy | the fork | Backlog #1186's site (§ 1 e): temp-and-rename through `AtomicFile::writeText`, there or in a stream | tool-run (`t33-writes.py`) |
| L-04 | `DisplayAspect.cpp:74-87`, `:116-118`, `:96` + `FileData.cpp:1914-1926`; rebuilt after `SystemData.cpp:503-504` and `views/ViewController.cpp:1470` | the first screenshot look after each library change walks the whole library under `sShotLock` on the interface thread, and every hit walks the tree for the game (T31 PL-26, T32 L-14; § 1 c) | Q6 | work on the interface thread | the fork (T31 PL-26) | recorded with G-03's press-to-frame number | guest (G-03: 0.1 s over 100 captures on a four-game library; not priced) |
| L-05 | `Gamelist.cpp:413` (cached `exists`), `:466-477` (in-place `save_file` `:474`), `:112-117` (the `isRegularFile` gate); writers `SystemData.cpp:1570`, `services/HttpServerThread.cpp:688`; the cache's only reset `es-core/src/utils/FileSystemUtil.cpp:345` | a `gamelist.xml` that arrives after startup (the cloud's game-content restore, D-CLOUD-049) reads as absent through the session cache: the restore's reload may not parse it, and the exit's `updateGamelist` writes the in-memory nodes alone over it; `saveToXml`'s remove-then-save `:307-308` is the same writer's no-last-good shape for the recovery files (D-CLOUD-078) | Q4 | a read of a file another process writes; a write with no last good copy | upstream-carried, inside the lanes (D-CLOUD-049) | a stream (rule 6): `exists(path, false)` at `:413` and `:116`'s gate, `updateGamelist` temp-and-rename; a #585 line | fixture (`stage-c/l313-update-gamelist.py`: FAIL at the pin, control PASS); guest (G-04, with its control) |
| L-06 | `CollectionSystemManager.cpp:1117` (`rootFolder->clear()` via `:1576`) then `:1589` (`reloadGameListView(bundle)`); callers `guis/GuiGamelistOptions.cpp:425`, `views/gamelist/ISimpleGameListView.cpp:462` | the #246 shape (`es-code-traps.md:191`): the custom collection's entries deleted, then the bundle view's cursor read; the fork's `dropGameListView`/`remakeGameListView` pair (`SystemData.cpp:508`) is the contained fix (T32 L-16, handed here; § 1 c) | Q1 | a lifetime: a free, then a read (#246's shape) | upstream-carried | a stream (rule 6): `dropGameListView` before the clear, `remakeGameListView` after (`es-code-traps.md:191`); a #585 line | fixture (`stage-c/l06-reload-collection.py`: heap-use-after-free at the pin, control clean); G-02 drove a plain collection, which `:1573` never repopulates |
| L-07 | `components/ScraperSearchComponent.cpp:197-258` (`:206`, `:230-234`, `:256`, no destructor); dropped at `:358-361` and `:96-100` | a builder destroyed mid-search leaks its running thread, which then writes `:213`, `:217`, `:220` into freed memory; `mFinished` read unsynchronised | Q1 | a lifetime or a thread | upstream-carried (T32 ruling 4 handed it here) | a stream question: the builder owns and joins its thread | fixture (`stage-c/l07-search-builder.py`: heap-use-after-free at the pin, control clean) |
| L-08 | `components/ScraperSearchComponent.cpp:645-658` (`:652`, `:658`) | on `ASYNC_DONE` with no results the second search runs synchronously on the interface thread, the call the builder exists to take off it (`:196`) | Q2, Q6 | work on the interface thread | upstream-carried | with L-07: the second search on the builder's thread | tree |
| L-09 | `ZaparooSupport.cpp:32-39`, `:58-63`; `guis/GuiGameOptions.cpp:59`, `:281`; `main.cpp:839` | a service on `127.0.0.1:7497` that accepts and never answers holds the detached probe forever and, through `mZaparooLock`, the game-options page; `writeZaparooCard` unbounded; outside the lanes, recorded | Q2 | an unbounded wait | upstream-carried, outside the lanes (D-UI-079) | recorded; a #585 line | tool-run (`t33-bounds.py`) |
| L-10 | `ContentInstaller.cpp:61`, `:64-70`, `:247-248`; `ThreadedBluetooth.cpp:19`, `:22-26`, `:46`, `:76`, `:110`; the `AN ERROR OCCURRED: <status>` strings `:144`, `:163`, `:182`, `:200`, `:218`, `:236` | `delete this` on the worker, the thread never joined or deleted, the card closed from the worker; a tool's status text on the screen; outside the lanes (D-UI-079), recorded | Q1, Q5 | a lifetime; a tool's words on a player's toast | upstream-carried, outside the lanes (D-UI-079) | recorded; a #585 line | tree |
| L-11 | `SystemScreenSaver.cpp:156-164`, `:350`, `:1022` | ten retries over a cached miss never see a file appear; a media file deleted since the cache remembered it is handed to the player; the first start walks the library on the interface thread; a post outside `AppWindow` (its target is process-lifetime); outside the lanes, recorded | Q4, Q6 | a read of a file another process writes; work on the interface thread | upstream-carried, outside the lanes (D-UI-079) | recorded | tool-run (`t33-reads.py`); guest (G-06: start and stop, `dim` and `black`) |
| L-12 | `NetworkThread.cpp:206`, `:237`, `:251`, `:257`, `:266` vs `AppWindow.h:38-45`; `main.cpp:1322`, `:1330` | five posts straight to `Window::postToUiThread`, not through the gate the fork wrote for exactly this (F-ES-26); sound by order, but a post between `:1322` and `:1330` lands in `mFunctions` and never runs; `:237`, `:251`, `:257` are the fork's | Q1 | a post that can be dropped at shutdown | the fork (F-ES-26) | a stream question: route the five posts through `AppWindow::post` | fixture (`stage-c/l12-network-posts.py`: five direct posts at the pin; `AppWindowTests.cpp` built, 1 case) |
| L-13 | `NetworkThread.cpp:266-270` | the token written with `SystemConf::set` + `saveSystemConf()` on the interface thread, a `system.cfg` rewrite covered by `es-conf-tests` (D-CLOUD-078's writer is es-core's); nothing new to prove | Q4 | a settings write | the fork | nothing new: `es-conf-tests` covers the writer (D-CLOUD-078) | design (`es-conf-tests`, 10 cases in `stage-c/build-pin.txt`) |
| L-14 | `RunLock.h:44-70` (`:58`, `:66-68`) | `holder()` names a pid whose `/proc/<pid>/cmdline` merely contains `program`; the window is a pid reused between a holder's death and the file's next writer; `OfflineAchievements::stopRun` signals what it returns | Q3, Q7 | a pid reused | the fork | a stream: argv[0] basename equality, contained | tree (`RunLockTests.cpp` built: 3 cases pass; the substring case is a stream's) |
| L-15 | `FolderMerge.h:38-71` <- `SystemData.cpp:486` (`vanished` -> `delete n` `:473`) | every holder of a vanished node (the collections' entries, a group folder, a hasher's queue, the header's own list `:9-13`) must be dropped at the `Tree` `:470-484`; the template's case file exists and has never been built (`tests/app-unit/FolderMergeTests.cpp`) | Q1 | a lifetime: every holder of a vanished node | the fork | recorded with the holders' list | tree (`FolderMergeTests.cpp` built: 3 cases pass) |
| L-16 | `JourneyTiers.h:133-154`; `main.cpp:958-975` | the continuation from fixed literals (sound); a marker with no record runs everything (`--all` + `--yes`, `:142-143`) by design (D-WORKFLOW-050); recorded, not a defect; the case file exists, never built | Q7 | a design, sound | the fork | recorded, not a defect (D-WORKFLOW-050) | design (`JourneyTiersTests.cpp` built: 8 cases pass) |
| L-17 | `OfflineAchievementsText.cpp:18`, `:231` | a 64-bit id or epoch truncated to `int`; harmless today | Q3 | a number truncated | the fork | a stream: `int64_t` through | tree |
| L-18 | `CloudOffer.cpp:37`, `:42-45` | bounded at 90 s on `GuiLoading`'s worker; a `timeout` kill (124) reads COULDN'T CREATE IT; a script exiting 0 having created nothing reads DONE (the no-op-success shape; the script's half is the rclone slice's) | Q3, Q5 | a success read over a no-op | the fork (the dialog); the rclone slice (the script) | a stream question for the dialog's half: what rc 0 proves against what DONE says | tree |
| L-19 | `WifiText.cpp:151-173`, `:67-81`, `:248-252`; `.h:137-146` | with two profiles up on one SSID and neither named, the connected row joins by its name, which `wifictl join` reads as a profile name: a renamed profile fails with `MayBeKey` and the player is asked for a key they have; documented as deliberate | Q5 | a profile joined by name | the fork | recorded: documented as deliberate | design (`WifiTextTests.cpp`, built) |
| L-20 | `TextFit.h:34` | the floor is 4 bytes, not 4 characters: a 4-byte name wider than the box never gets its ellipsis; a two-character CJK name stops at one character | Q5 | a byte floor where a character floor was meant | the fork | a stream: the floor counted in characters | fixture (`stage-c/l335-textfit-floor.py`: FAIL at the pin, control PASS) |
| L-21 | `Win32ApiSystem.cpp:1`, `:1267`, `:316`, `:341`, `:368`; `es-app/CMakeLists.txt:287` | listed unconditionally, guarded in the file: the fork-own tier is provenance | Q7 | provenance | upstream-carried (the fork's three lines `:316`, `:341`, `:368`) | one row each in § The structure (D-WORKFLOW-209) | tool-run (`stage-a/syntax-check.out`) |
| L-22 | `ScraperCmdLine.cpp:27`, `:24`, `:287`; `es-app/CMakeLists.txt` (absent) | 290 lines of console code in no list; Backlog #1235's shape | Q7 | provenance | upstream-carried | recorded as Backlog #1235's shape; never deleted by the lane | tool-run (`stage-a/runs.out`'s CMake grep) |
| L-23 | `FileFilterIndex.cpp:1313`; `CollectionSystemManager.cpp:345-357` | settings-tier files (`.xcc`, `custom-<name>.cfg`, which backuptool's archive carries) written in place; the atomic writer exists (`AtomicFileUtil`) | Q4 | a write with no last good copy | upstream-carried, settings tier (backuptool's archive) | a stream (rule 6): `AtomicFileUtil` for both | tool-run (`t33-writes.py`, `t33-reads.py`) |
| L-24 | `NetworkThread.cpp:19-25`, `main.cpp:898` | `sCheevosToken` points into a `NetworkThread` newed once and never deleted: sound for the process's life, recorded so nobody "fixes" the leak and dangles the static | Q1 | a lifetime, sound | the fork | recorded so nobody frees it and dangles the static | tree |
| L-25 | `FileTag.cpp:6-11` against `:16-18`; the catalog | six of nine tag names reach xgettext through `fake_gettext_*`; `IN PROGRESS`, `DROPPED`, `ON HOLD` do not and have no `msgid` at the pin (six `msgid` lines at po 717, 3576, 3579, 3582, 3585, 3588; none for the three) | Q5 | a player word outside the catalog | upstream-carried | a stream (rule 6): three `_()` and their French (D-UI-051); a #585 line | fixture (`stage-c/l329-filetag-words.py`: FAIL at the pin, control PASS) |
| L-26 | `LangParser.cpp:65` | `{ { "in", "ìndia" }, "in", "in" }`: a non-ASCII token matched lowercase against ASCII ROM names, unreachable; a string literal, so xgettext is unaffected | Q5 | a token unreachable | upstream-carried | a stream (rule 6): one literal; a #585 line | fixture (`stage-c/l331-lang-india.py`: FAIL at the pin, control PASS) |
| L-27 | `FileFilterIndex.cpp:333-340`, `:367` | `"0.05"` rounds to `0 STARS` where `"0"` and `""` read UNKNOWN; a year starting `3`, or three digits, reads `""` | Q3 | a parse that reads a failure as data | upstream-carried | recorded with its case; the fix put to the pause | fixture (`stage-c/l309-rating-year.py`: FAIL at the pin, control PASS) |
| L-28 | `KeyboardMapping.cpp:265`, `:271`, `:282`, `:288` | a trigger or key target `checkTriggerExists`/`checkTargetExists` refuses is dropped silently: a mapping loads as an action with no trigger | Q3 | a parse that drops what it cannot read, silently | upstream-carried, outside the lanes (D-UI-079) | recorded with its case; the fix put to the pause | fixture (`stage-c/l321-keys-parse.py`: FAIL at the pin, control PASS); guest (G-08) |
| L-29 | § 5's two delta commands | merge debt none | Q7 | -- | -- | § The merge debt | tool-run (`stage-a/runs.out`) |

### The floor's pure leads, carried

The brief's 41 rows (brief § 4), word for word, with the proof this read plans. The six that FAIL at the pin are in bold: 3.9, 3.13, 3.21, 3.29, 3.31 and 3.35. Each is seen to FAIL against the unfixed extract before it is trusted, at stage C. Offsets written `+N` are read to absolute lines when a case cites them.

| # | At the pin | Function | What a case would catch | Proof planned |
| --- | --- | --- | --- | --- |
| 3.1 | `PlatformId.cpp:215` (`:220`), `:227` (`:233`), `:237` | `getPlatformId`, `getPlatformName`, the `ArcadeSystems` map | `getPlatformId(nullptr)`; a duplicated table string shadowing an id; an enum value with no row reading `"unknown"`; short names not lowercase | unit case at stage C |
| 3.2 | `MetaData.cpp:28` (`:30-66`), `:42-43`/`:46-47` | `initMetadata`'s `gameDecls` | a key typed twice with two types; `Emulator`/`Core` twice by design, the case pins which wins | unit case at stage C |
| 3.3 | `MetaData.cpp:280` (`+153`, `+158-161`, `+167-169`, `+199-201`) | `appendToXML` | a player-set value equal to its default dropped under `ignoreDefaults`; an `MD_PATH` written absolute when relative was asked | unit case at stage C |
| 3.4 | `MetaData.cpp:357`, `:407`, `:435`, `:451`, `:454`, `:459` | `set`, `get`, `exists`, `getInt`, `getFloat`, `wasChanged` | `getInt` on `""`; a non-numeric `playcount`; `set` of the same value flipping `wasChanged` | unit case at stage C |
| 3.5 | `MetaData.cpp:469` | `importScrappedMetadata` | a scrape wiping a player's favourite flag; an empty scraped field blanking a filled one | unit case at stage C |
| 3.6 | `MetaData.cpp:270` (`+124`) | `migrate` (`FileData*` on the signature: the lane finds the seam) | an old `<hash>` lost on first load (`upgrade-and-install.md:95`: read both) | unit case at stage C |
| 3.7 | `MetaData.cpp:151` (`+20-28`, `+66-70`) | `loadFromXML`'s default-and-lowercase rule and the `<scrap>` reading, lifted | a `"TRUE"` another tool wrote not read as true | unit case at stage C |
| 3.8 | `Genres.cpp:185`, `:234`, `:257`, `:293`, `:323` (`init` `:19`) | the genre lookups, over a seam that takes a document | a game counted twice in the genre filter (parent and child); a trailing comma | unit case at stage C |
| **3.9** | `FileFilterIndex.cpp:247` (**`:322-341`, `:364-369`**), `:362` | the rating, year and played predicates, lifted into string-in/string-out helpers | **`ratingKey("0.05")` reads `0 STARS` where `""` and `"0"` read UNKNOWN (`:333`, `:339`); `yearKey("3000")` and `yearKey("999")` read `""` (`:367`)** (L-27) | **FAIL at the pin**: unit case at stage C |
| 3.10 | `FileFilterIndex.cpp:557` | `jw_distance` (file-static Jaro-Winkler) | identical -> 1.0; empty vs non-empty -> 0; symmetric; a distance above 1 or NaN on an empty string | unit case at stage C |
| 3.11 | `FileFilterIndex.cpp:1107-1321` (`+11`, `+37-39`, `+99-161`) | `CollectionFilter::load`/`save` on a temp `.xcc` (file) | a tag `save` writes that `load` ignores: a filter forgetting one of its rows on restart | file case at stage C |
| 3.12 | `Gamelist.cpp:255`, `:288` (`:261`, `+274`, `+283`) | `addFileDataNode`, `saveToXml` (needs `FileData*`/`SystemData*` doubles, `tests/app-unit/fakes/FileData.h`) | a `<path>` written absolute into a per-system gamelist | unit case at stage C |
| **3.13** | `Gamelist.cpp:374` (**`:413`, `:466-477`**; `:308`, `:622`, `:841`) | `updateGamelist`'s shape | **the in-place `doc.save_file` with no temp-and-rename (D-CLOUD-078) and the cached `exists` before it** (L-05); the shape in a file case, the atomicity `CANNOT` without a fault seam (G-05) | **FAIL at the pin**: file case at stage C; the atomicity `CANNOT` (G-05) |
| 3.14 | `Gamelist.cpp:112` (`+35-38`, `+47`, `+61-63`, `+66`, `+79-83`) | `loadGamelistFile` through its `!fromFile` branch (a string) | a `<path>` with a trailing newline or `\` never matched; the size-mismatch warning | unit case at stage C |
| 3.15 | `Gamelist.cpp:518`, `:631`, `:483` (`+601`, `+705`, `+732-748`) | `packGamelist`, `cleanupGamelist` (file or guest) | `cleanupGamelist` dropping a media reference that exists on disk through the cache | file case at stage C, or G-04 |
| 3.16 | `CollectionSystemManager.cpp:1508`, `:1513`, `:1518`, `:1523`, `:1532` | the collection paths | a name containing `/` or `..` writing outside the collections folder | unit case at stage C |
| 3.17 | `CollectionSystemManager.cpp:598` (`:627`, `:646`, `:651`; `themeFolderExists` `:1492`) | `getValidNewCollectionName` over a seam for `sSystemVector` | an auto-collection name (`"all"`) or a theme folder accepted | unit case at stage C |
| 3.18 | `CollectionSystemManager.cpp:1434` (`+1450`) | `getCollectionsFromConfigFolder` over a handed listing | `custom-.cfg` or `custom-a.cfg.bak` read as a collection | unit case at stage C |
| 3.19 | `CollectionSystemManager.cpp:34` (`:40`) | `getSystemDecls` | names or theme folders not unique; `recent`'s sort | unit case at stage C |
| 3.20 | `CollectionSystemManager.cpp:540` | the `.at()` on a set value (T2 FD-15, #771) | an index outside the 28 sort types | unit case at stage C |
| **3.21** | `KeyboardMapping.cpp:217` (**`:265`, `:271`, `:282`, `:288`**; `checkTriggerExists` `:178`) | `KeyMappingFile::load`'s parse, split out as `parse(json)` | **a trigger naming an unknown key dropped silently: a mapping loads as an action with no trigger** (L-28); a parse error -> what `isValid` `:499` says | **FAIL at the pin**: unit case at stage C |
| 3.22 | `KeyboardMapping.cpp:328`, `:432`, `:512`, `:535`, `:586`, `:726`, `:776`, `:793` | `save`, `fromP2k`, `triggerEquals`, `toTargetString`, `updateMapping`, `removeMapping`, the descriptions | a description with a quote breaking a JSON written by hand (read `:328-431` first); `save -> load` round trip | unit case at stage C |
| 3.23 | `KeyboardMapping.cpp:178`, `:190`, `:199`, `:208` (the tables `:163-176`) | `checkTriggerExists`, `checkTargetExists`, `getTriggerFromP2k`, `getTargetFromP2k` | a key whose name has two `_` taking the wrong tail | unit case at stage C |
| 3.24 | `CustomFeatures.cpp:23` (`:13-21`) | `parseFeatures` | a feature name with a trailing space never enabling its row | unit case at stage C |
| 3.25 | `CustomFeatures.cpp:406`, `:61`, `:93`, `:155` (`:202-207`, `:224-227`, `:242-251`, `:256`, `:292-298`) | `loadCustomFeatures` over an XML string | a feature declared on the core not reaching the menu when the emulator declares none | unit case at stage C |
| 3.26 | `CustomFeatures.cpp:529`, `:534`, `:523` | `hasFeature`, `hasGlobalFeature`, `sort` | a case mismatch between `es_features.cfg` and the launcher | unit case at stage C |
| 3.27 | `FileSorts.cpp:93` (`:96`, `:99`, `:106`; `:83`) | `stripLeadingArticle` | an article matched by prefix; a title that is only an article emptied; `_("A,AN,THE")` translated | unit case at stage C |
| 3.28 | `FileSorts.cpp:32` (`:43-71`) | `getSortType` and the 28-row table | an id twice; a pair not sharing its comparator; `getSortType(-1)` falling to the first row | unit case at stage C |
| **3.29** | `FileTag.cpp:30` (**`:6-11` against `:16-18`**) | `getDisplayIcons` | **three of nine names outside `_()` and absent from the catalog** (L-25); `"finished"` -> 0 (exact case) | **FAIL at the pin**: unit case at stage C |
| 3.30 | `LibretroRatio.cpp:51` (`:12-43`) | `getRatio()` | keys not unique; a value RetroArch does not accept | unit case at stage C |
| **3.31** | `LangParser.cpp:33` (**`:65`**; `:37-64`) | `extractLang` | **`"ìndia"` unreachable: only `"in"` matches** (L-26); `"(USA, Europe)"` -> en + us,eu | **FAIL at the pin**: unit case at stage C |
| 3.32 | `LangParser.cpp:144`, `:203`, `:18` | `parse`, `getFlag`, `getLanguageString` | a region with no flag asset drawing a broken image | unit case at stage C |
| 3.33 | `CaptureRotation.cpp` (§ 2's row) **(fork-own)** | the one cached read beside four uncached | a rotation table written after ES started reading as absent (by design: the lane records the comment `:23-30`) | recorded (`t33-reads.py`: the deliberate cached read) |
| 3.34 | `SystemRandomPlaylist.cpp` (§ 2's row) | `getNextItem` over a seam for the RNG | a path that starts existing mid-session never seen | unit case at stage C over an RNG seam, or recorded with L-11 |
| **3.35** | `TextFit.h` (§ 2's row) **(fork-own)** | `fitOneLine` with a fake measure (1 px per char), `popCharacter` | **a 4-byte name over the width never gets its ellipsis; a two-character CJK name stops at one** (L-20); a label cut inside a UTF-8 sequence | **FAIL at the pin**: unit case at stage C |
| 3.36 | `JourneyTiers.h` (§ 2's row) **(fork-own)** | `record`, `parse`, `replaceRecord`, `command` (`JourneyTiersTests.cpp`'s 8 cases first) | a two-byte record read as empty; a `Write` that fails -> `OldRecordStands`; the literals' exact shape | unit case at stage C |
| 3.37 | `FolderMerge.h` (§ 2's row) **(fork-own)** | `merge(live, fresh, tree)` (`FolderMergeTests.cpp`'s 3 cases first) | a live node dropped when the fresh tree holds it under a different case; a renamed folder | unit case at stage C |
| 3.38 | `RunLock.h` (§ 2's row) **(fork-own)** | `held`, `holder` (`RunLockTests.cpp`'s 3 cases first; file) | a stale lock file read as held; the substring match (L-14) | unit case at stage C |
| 3.39 | `GameCubeRvzHashRetry.h` (§ 2's row) **(fork-own)** | `trim`, `needed` | a valid unknown hash retried; whitespace only | unit case at stage C |
| 3.40 | `AppWindow.h` (§ 2's row) **(fork-own)** | `gate`, `open`, `post`, `closing` (`AppWindowTests.cpp`'s 1 case first) | a task posted after `closing()` running; a task posted before running twice | unit case at stage C |
| 3.41 | `OfflineAchievementsText.cpp` (§ 2's row) **(fork-own)** | `jsonInt`, `parsePendingIds` | the `int` truncation (L-17) | unit case at stage C |

## The library

One row per unit of the game lists, collections, metadata and filters. The facts are read at the cited lines, and the generator checks that each cited caller line holds the call it names. Three things stand out:
- **The first frame waits for the whole library:** every system's `gamelist.xml` parse, the filter index, the collections' load and es_features.cfg, under the splash. None of the slice's own reads is on the network.
- **Two writers are on the player's data:** `gamelist.xml` (game content, synced) and the collections' files (settings, archived). Both write in place (§ The writes).
- **One reader can lose data:** `Gamelist.cpp:413`'s cached read is the one that can drop a restored `gamelist.xml` (L-05).

| Unit | Lines (.cpp / .h) | Includers outside the 77 | Reads | Writes | Thread | The first frame waits for |
| --- | --- | --- | --- | --- | --- | --- |
| `Gamelist` | 848 / 31 | 10 | each system's `gamelist.xml`: `parseGamelist` (`SystemData.cpp:128`), `packGamelist` first when PackGamelists (`:126`) | `updateGamelist` at exit when SaveGamelistsOnExit (`SystemData.cpp:1570`) and from the API (`services/HttpServerThread.cpp:688`); `cleanupGamelist` from the menu (`guis/GuiMenu.cpp:437`, `:1157`); `saveToXml` for the launch (`FileData.cpp:639`) -- § The writes | loadConfig's ThreadPool (`SystemData.cpp:1202-1258`), one work item per system; the writes on the interface thread, at exit, or the API's pool | every system's parse: the pool's `wait` (`SystemData.cpp:1246-1258`) under the splash |
| `MetaData` | 604 / 201 | 4 | each game node, `loadFromXML` inside the parse; with PreloadMedias a cached `exists` per image (`:223`) | through Gamelist's `addFileDataNode`; the editor (`guis/GuiMetaDataEd.cpp`, T31's) | loadConfig's ThreadPool (`SystemData.cpp:1202-1258`), one work item per system | inside the parse; PreloadMedias adds one `exists` per image, thumbnail and marquee |
| `Genres` | 372 / 69 | 9 | `:/genres.xml` (`Genres::init`, `main.cpp:811`) | none | main()'s ThreadPool (`main.cpp:806`) | `waitAllExcept(vlcInit)` (`main.cpp:846`) before the systems load |
| `PlatformId` | 301 / 196 | 11 | no file: the name table, read as each system loads (`SystemData.cpp:1410`) | none | the loader | a table lookup |
| `LangParser` | 242 / 27 | 5 | no file: the region and language table, read when a name is formatted | none | the interface thread | nothing |
| `FileTag` | 46 / 20 | 3 | no file: nine tag names and icons (L-25: three reach no msgid) | none | the interface thread | nothing |
| `CollectionSystemManager` | 1631 / 149 | 17 | the collections folder, `custom-<name>.cfg`, the `.xcc` filters, es_systems.cfg and the theme's collections (§ The reads) | `custom-<name>.cfg` in place (`:345`, `saveCustomCollection`, from `:149` and `guis/GuiCollectionSystemsOptions.cpp:435`) | `loadCollectionSystems` as one pool item (`SystemData.cpp:1214`) or on the main thread without a pool (`:1278`); `updateSystemsList` on the main thread (`:1288`); reloads on the interface thread (L-06) | the collections' load and the systems list before the first view |
| `FileFilterIndex` | 1412 / 197 | 8 | the `.xcc` (`CollectionFilter::load`, `:1144`); each game's metadata as the index is built | the `.xcc` in place (`:1313`, `CollectionFilter::save`, from the filter editor, T31's `guis/GuiGamelistFilter`) | built per system (`SystemData.cpp:657`) on the loader; the filter's change on the interface thread | each system's index while it loads |
| `FileSorts` | 226 / 87 | 7 | no file: the 28 sort types (T2 FD-15: the index against them, `FileData.cpp:1659`) | none | the interface thread | nothing |
| `CustomFeatures` | 537 / 157 | 1 | es_features.cfg, the user's then the image's (`loadEsFeaturesFile`, `SystemData.cpp:1196`) | none (`:151` is dead text) | the main thread, before the pool | the features file's parse |
| `LibretroRatio` | 53 / 22 | 1 | no file: the ratio table (`guis/GuiMenu.cpp:11341`) | none | the interface thread | nothing |

generated, asserted: 11 units

## The helpers

One row per fork-added unit (17 units, 27 files). Its includers outside the 77 are the page or caller in another slice. The case file is matched by name.

Twelve units have a case file:
- Seven are built by `es-unit-tests`, which every lane has run.
- Five are `tests/app-unit`'s, which no lane has built (T18 `02:50-58`). Stage C's first build is theirs, extended in `t33-build-tests.sh`.

Five units have no case file:
- `CaptureRotation` and `DisplayAspect`: their pure halves are their `Text` siblings, which have cases.
- `CloudExit.h`: constants.
- `GameCubeRvzHashRetry.h`: 3.39 plans its case.
- `CloudOffer`: L-18's dialog, read.

The brief's "three without a case" counts `NetworkThread.*`, which is fork-modified, and leaves out the two `Text` pairs. The French is § The words': every msgid the 77 carry has a translation at the pin.

| Unit | Files (lines) | Includers outside the 77 | Case file | Built | `_("` lines |
| --- | --- | --- | --- | --- | --- |
| `AppWindow` | `AppWindow.h` (56) | `FileData.cpp`, `OfflineScanJob.cpp`, `ProxyCards.cpp`, `guis/GuiMenu.cpp`, `main.cpp` | `tests/app-unit/AppWindowTests.cpp` | `app-unit-tests`, never built by a lane (stage C) | 0 |
| `CaptureRotation` | `CaptureRotation.cpp` (188), `CaptureRotation.h` (39) | `FileData.cpp` | **none** | -- | 0 |
| `CaptureRotationText` | `CaptureRotationText.cpp` (164), `CaptureRotationText.h` (68) | none; in the 77: `CaptureRotation.cpp` | `es-app/tests/unit/CaptureRotationTextTests.cpp` | `es-unit-tests`, built by every lane | 0 |
| `CheevosIndex` | `CheevosIndex.cpp` (30), `CheevosIndex.h` (47) | `ThreadedHasher.cpp` | `es-app/tests/unit/CheevosIndexTests.cpp` | `es-unit-tests`, built by every lane | 0 |
| `CheevosRetry` | `CheevosRetry.cpp` (31), `CheevosRetry.h` (47) | `guis/GuiRetroAchievementsSettings.cpp` | `es-app/tests/unit/CheevosRetryTests.cpp` | `es-unit-tests`, built by every lane | 0 |
| `CloudExit` | `CloudExit.h` (30) | `CloudText.cpp`, `CloudTransferJob.cpp`, `ThreadedCloudSync.cpp`, `guis/GuiCloudTransfer.cpp`, `guis/GuiMenu.cpp`, `guis/GuiOfflineScan.cpp`, `main.cpp` | **none** | -- | 0 |
| `CloudFolderValidation` | `CloudFolderValidation.cpp` (96), `CloudFolderValidation.h` (33) | `guis/GuiMenu.cpp` | `es-app/tests/unit/CloudFolderValidationTests.cpp` | `es-unit-tests`, built by every lane | 0 |
| `CloudOffer` | `CloudOffer.cpp` (84), `CloudOffer.h` (33) | `ThreadedCloudSync.cpp`, `guis/GuiCloudTransfer.cpp` | **none** | -- | 12 |
| `DisplayAspect` | `DisplayAspect.cpp` (153), `DisplayAspect.h` (42) | `SystemData.cpp`, `guis/GuiImageViewer.cpp`, `guis/GuiSaveState.cpp`, `views/ViewController.cpp`, `views/gamelist/DetailedContainer.cpp`, `views/gamelist/GridGameListView.cpp`, `views/gamelist/ISimpleGameListView.cpp` | **none** | -- | 0 |
| `DisplayAspectText` | `DisplayAspectText.cpp` (76), `DisplayAspectText.h` (26) | none; in the 77: `DisplayAspect.cpp` | `es-app/tests/unit/DisplayAspectTextTests.cpp` | `es-unit-tests`, built by every lane | 0 |
| `FolderMerge` | `FolderMerge.h` (74) | `SystemData.cpp` | `tests/app-unit/FolderMergeTests.cpp` | `app-unit-tests`, never built by a lane (stage C) | 0 |
| `GameCubeRvzHashRetry` | `GameCubeRvzHashRetry.h` (45) | `ThreadedHasher.cpp` | **none** | -- | 0 |
| `JourneyTiers` | `JourneyTiers.h` (159) | `guis/GuiMenu.cpp`, `main.cpp` | `tests/app-unit/JourneyTiersTests.cpp` | `app-unit-tests`, never built by a lane (stage C) | 0 |
| `OfflineAchievementsText` | `OfflineAchievementsText.cpp` (283), `OfflineAchievementsText.h` (161) | `OfflineAchievements.h`, `RetroAchievements.cpp`, `RetroAchievements.h` | `es-app/tests/unit/OfflineAchievementsTextTests.cpp` | `es-unit-tests`, built by every lane | 0 |
| `RunLock` | `RunLock.h` (74) | `OfflineAchievements.cpp` | `tests/app-unit/RunLockTests.cpp` | `app-unit-tests`, never built by a lane (stage C) | 0 |
| `TextFit` | `TextFit.h` (40) | `guis/GuiCloudTransfer.cpp`, `guis/GuiOfflineScan.cpp`, `guis/GuiScraperRun.cpp` | `tests/app-unit/TextFitTests.cpp` | `app-unit-tests`, never built by a lane (stage C) | 0 |
| `WifiText` | `WifiText.cpp` (265), `WifiText.h` (164) | `ApiSystem.h`, `guis/GuiMenu.cpp`, `guis/GuiWifi.h` | `es-app/tests/unit/WifiTextTests.cpp` | `es-unit-tests`, built by every lane | 0 |

generated, asserted: 17 units in 27 files; 12 with a case file, 7 of them built by `es-unit-tests`

## The writes

§ 5's grep, line for line. Nine lines compile. The brief's "ten live sites" counts `CustomFeatures.cpp:151`, which is text inside a `/* */` block. `Win32ApiSystem.cpp:979` is dead inside `#if WIN32`.

None of the nine is temp-and-rename. `Gamelist.cpp:622` and `:841` keep a `.old` copy that nothing reads back. Every in-place writer is measured against two references:
- JourneyTiers' writer (`guis/GuiMenu.cpp:5066`, `AtomicFile::writeText`);
- es-core's `AtomicFileUtil`, which `es-file-tests` covers.

D-CLOUD-078 asks every writer for temp-and-rename. `Already written:` is answered per row (D-WORKFLOW-050).

| Line | Writes | How | Last good copy | Already written | Disposition proposed |
| --- | --- | --- | --- | --- | --- |
| `CaptureRotation.cpp:175` | a game's `.rotation` record beside its save states (saves tier, synced) | in place (`writeAllText`) | none | a cut record lacks `from=checked-launch` and reads as untrusted (`:124`): the core's table stands in and the next exit rewrites it -- benign | L-03: Backlog #1186's site (§ 1 e); temp-and-rename through `AtomicFile::writeText` |
| `CollectionSystemManager.cpp:345` | a custom collection's `custom-<name>.cfg` (settings tier, in backuptool's archive) | in place (`std::ofstream`, truncate then write, no error check) | none | a cut list reads as a shorter collection: the games past the cut are silently out of it, and the next save writes the shorter list back | L-23: a stream (temp-and-rename through `AtomicFileUtil`, which also drops the cache entry `:1610`/`:1613` remember) |
| `CustomFeatures.cpp:151` | nothing: `c:\temp\test.xml` inside a /* */ block | dead text | -- | nothing inherited: the line never compiled | left: upstream's comment |
| `FileFilterIndex.cpp:1313` | a dynamic collection's filter `.xcc` (settings tier, in backuptool's archive) | in place (`pugi::save_file`) | none | a cut `.xcc` is a parse error: `CollectionFilter::load` returns false and the collection reads as having no filter (every game) | L-23: a stream, as `:345` |
| `Gamelist.cpp:308` | `saveToXml`: the launch's `%GAMEINFOXML%` file (`FileData.cpp:639`) or a gamelist recovery file (`:336`) | remove (`:307`) then `pugi::save_file`: no file between | none | a cut recovery file is a parse error at the next load and the entry is not recovered; the launch's file is rewritten every launch | Backlog #1186's site (§ 1 e) |
| `Gamelist.cpp:474` | `updateGamelist`: the system's `gamelist.xml` (game content tier, D-CLOUD-049, synced) | in place (`pugi::save_file`) | none | a cut `gamelist.xml` is a parse error: the system shows no metadata until the next save, which then starts from an empty `<gameList>` (`:427`) and keeps only the dirty entries | L-05's writer: a stream (temp-and-rename) with the uncached read `:413` |
| `Gamelist.cpp:622` | `packGamelist`: `gamelist.xml` | copy aside to `.old` (`:619-620`), then in place | `gamelist.xml.old` | as `:474`; the `.old` beside it is the previous file, which nothing reads back | Backlog #1186's site (§ 1 e) |
| `Gamelist.cpp:841` | `cleanupGamelist`: `gamelist.xml` | copy aside to `.old` (`:838-839`), then in place | `gamelist.xml.old` | as `:622` | with `:622` |
| `KeyboardMapping.cpp:426` | a `.keys` mapping at its own path (settings tier) | in place (`writeAllText`) | none | a cut `.keys` is a JSON parse error: the mapping loads empty | recorded: outside the lanes (D-UI-079) |
| `KeyboardMapping.cpp:429` | a `.keys` mapping at a named path | in place (`writeAllText`) | none | as `:426` | recorded with `:426` |
| `Win32ApiSystem.cpp:979` | a Windows marker file (`ok`) | dead inside `#if WIN32` | -- | nothing inherited: no image carries it | L-21: recorded |

generated, asserted: 11 lines (9 live, 2 dead) in 7 files

## The reads

One row per `Utils::FileSystem::exists(` line: 83 lines and 86 calls. Four calls are uncached, all in `CaptureRotation.cpp` (`:113`, `:146`, `:161`, `:170`). The 46 upstream-carried files have none.

The cache's rule is T21's file, cited from T32's Q4 and not re-read:
- ES's own writes through `Utils::FileSystem` drop their path from the cache.
- A file written outside the process is not seen until a launch resets the cache (`FileSystemUtil.cpp:345`). Examples are the cloud's game-content restore (D-CLOUD-049) and the player over SSH.
- A third shape this slice adds: ES's own writes that do not go through `Utils::FileSystem`. These are `std::ofstream` (`CollectionSystemManager.cpp:345`) and `pugi::save_file` (`FileFilterIndex.cpp:1313`, `Gamelist.cpp:474`, `:622`, `:841`), and their paths are not dropped either.

The four the brief names, with their dispositions:
- **`Gamelist.cpp:413` (L-05):** the reader that can lose a player's data. The next save starts from an empty `<gameList>` and writes over the restored file.
- **`SystemScreenSaver.cpp:157` and `:164` (L-11):** recorded, outside the lanes.
- **`CaptureRotation.cpp:51`:** left cached on purpose, because it reads the image's read-only tree.

| Line | Reads | Writer while ES runs | Cache | A remembered answer reads as | Disposition proposed |
| --- | --- | --- | --- | --- | --- |
| `CaptureRotation.cpp:51` | fromTable: a core's rotation table under /usr/config/emulationstation/rotation | nobody: the image's read-only tree | cached | nothing can change it while ES runs; sTables memoises the answer anyway (:44-53) | left cached: deliberate, beside the four uncached reads (Q4) |
| `CaptureRotation.cpp:113` | read(): a game's .rotation record beside its save states | ES (write :175) and the cloud's saves tier | uncached | uncached | uncached at the pin: a record restored from the cloud is seen |
| `CaptureRotation.cpp:146` | the launcher's /var/log/exec.log after a RetroArch exit | the launcher (outside ES) | uncached | uncached | uncached at the pin (L-02 is its size, not its cache) |
| `CaptureRotation.cpp:161` | retroarch.cfg after a RetroArch exit | RetroArch (outside ES) | uncached | uncached | uncached at the pin |
| `CaptureRotation.cpp:170` | write(): the record before it is rewritten | ES and the cloud's saves tier | uncached | uncached | uncached at the pin |
| `CollectionSystemManager.cpp:133` | the collections folder under the user's ES path | ES itself (createDirectory :134); the player | cached | a remembered miss calls createDirectory on a folder that exists: harmless | left cached |
| `CollectionSystemManager.cpp:963` | a dynamic collection's filter (.xcc) at startup | ES (FileFilterIndex.cpp:1313, through std::ofstream); a settings restore | cached | a remembered miss loads the collection without its filter until a restart; ES's own writer is not Utils::FileSystem, so its first save is not seen by this read either | recorded with L-23 (the same files) |
| `CollectionSystemManager.cpp:1147` | a custom collection's config before it is populated | ES (std::ofstream :345); a settings restore | cached | a remembered miss shows the custom collection empty until a restart | recorded with L-23 |
| `CollectionSystemManager.cpp:1317` | es_systems.cfg | the image; the player | cached | nothing changes it in a session that matters: a new file needs a restart regardless | left cached |
| `CollectionSystemManager.cpp:1369` | the theme set's folder, its collections.info and each system's theme | a theme installer (ES's own, through Utils::FileSystem) or the player | cached | a remembered miss offers fewer collection themes until a restart | left cached: theme files |
| `CollectionSystemManager.cpp:1372` | the theme set's folder, its collections.info and each system's theme | a theme installer (ES's own, through Utils::FileSystem) or the player | cached | a remembered miss offers fewer collection themes until a restart | left cached: theme files |
| `CollectionSystemManager.cpp:1391` | the theme set's folder, its collections.info and each system's theme | a theme installer (ES's own, through Utils::FileSystem) or the player | cached | a remembered miss offers fewer collection themes until a restart | left cached: theme files |
| `CollectionSystemManager.cpp:1439` | the collections folder under the user's ES path | ES itself (createDirectory :134); the player | cached | a remembered miss calls createDirectory on a folder that exists: harmless | left cached |
| `CollectionSystemManager.cpp:1610` | deleteCustomCollection: the .xcc, then the custom-<name>.cfg | ES (FileFilterIndex.cpp:1313, CollectionSystemManager.cpp:345, both std::ofstream) | cached | a file whose miss was remembered earlier in the session (the .xcc at :963 is the same path, getFilteredCollectionPath) and written since by std::ofstream: the delete reads it absent and returns false | recorded with L-23: the stream that makes the writers atomic routes them through Utils::FileSystem, which drops the entry |
| `CollectionSystemManager.cpp:1613` | deleteCustomCollection: the .xcc, then the custom-<name>.cfg | ES (FileFilterIndex.cpp:1313, CollectionSystemManager.cpp:345, both std::ofstream) | cached | a file whose miss was remembered earlier in the session (the .xcc at :963 is the same path, getFilteredCollectionPath) and written since by std::ofstream: the delete reads it absent and returns false | recorded with L-23: the stream that makes the writers atomic routes them through Utils::FileSystem, which drops the entry |
| `CustomFeatures.cpp:164` | es_features.cfg, the user's then the image's | the image; the player | cached | read once at startup | left cached |
| `CustomFeatures.cpp:167` | es_features.cfg, the user's then the image's | the image; the player | cached | read once at startup | left cached |
| `FileFilterIndex.cpp:867` | showFile: a media path a game's metadata names, for a has-<media> filter | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered answer keeps a game in (or out of) a has-media filter until a launch | recorded: the family of L-05 and L-11, outside the lanes (D-UI-079) |
| `FileFilterIndex.cpp:889` | showFile: a media path a game's metadata names, for a has-<media> filter | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered answer keeps a game in (or out of) a has-media filter until a launch | recorded: the family of L-05 and L-11, outside the lanes (D-UI-079) |
| `FileFilterIndex.cpp:1144` | CollectionFilter::load: the .xcc | ES (std::ofstream :1313) | cached | as :963 | recorded with L-23 |
| `Gamelist.cpp:190` | loadGamelistFile: a game file the gamelist.xml names but the scan did not find | the player, a cloud ROM restore | cached | a remembered miss drops the entry from the list until a restart | recorded: the scan reads the folder, which the cache does not serve |
| `Gamelist.cpp:304` | saveToXml: the system's folder before the write | the player | cached | a remembered hit for a folder removed since lets the write fail; the folder is the system's own | left cached |
| `Gamelist.cpp:352` | removeFromGamelistRecovery: the recovery file | ES itself (removeFile :353, writeAllText) | cached | ES's own writes drop the entry | left cached |
| `Gamelist.cpp:413` | updateGamelist: gamelist.xml before ES merges and writes it | cloud_content_restore (D-CLOUD-049), the player; ES itself (save_file :474, not through Utils::FileSystem) | cached | a gamelist.xml that arrived after startup reads as absent: the next save (a played game, an edit) starts from an empty <gameList> (:427) and writes only the dirty entries over the restored file (:474), losing every other entry's metadata | L-05: a stream (uncached, with :116's gate); G-04's variant the positive, image side |
| `Gamelist.cpp:531` | cleanupGamelist / packGamelist: gamelist.xml | as :413 | cached | a remembered miss skips the cleanup: the safe direction | recorded with L-05 |
| `Gamelist.cpp:601` | packGamelist / cleanupGamelist: each media path the xml names | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss removes the entry for a file restored since; a remembered hit keeps a dangling one | recorded with L-05: the cleanup runs from a menu action, after which a launch has not reset the cache |
| `Gamelist.cpp:644` | cleanupGamelist / packGamelist: gamelist.xml | as :413 | cached | a remembered miss skips the cleanup: the safe direction | recorded with L-05 |
| `Gamelist.cpp:705` | packGamelist / cleanupGamelist: each media path the xml names | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss removes the entry for a file restored since; a remembered hit keeps a dangling one | recorded with L-05: the cleanup runs from a menu action, after which a launch has not reset the cache |
| `Gamelist.cpp:732` | cleanupGamelist: the media file a game's name implies, by suffix and extension | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves media restored since unlinked | recorded with L-05 |
| `Gamelist.cpp:735` | cleanupGamelist: the media file a game's name implies, by suffix and extension | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves media restored since unlinked | recorded with L-05 |
| `Gamelist.cpp:738` | cleanupGamelist: the media file a game's name implies, by suffix and extension | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves media restored since unlinked | recorded with L-05 |
| `Gamelist.cpp:740` | cleanupGamelist: the media file a game's name implies, by suffix and extension | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves media restored since unlinked | recorded with L-05 |
| `Gamelist.cpp:743` | cleanupGamelist: the media file a game's name implies, by suffix and extension | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves media restored since unlinked | recorded with L-05 |
| `Gamelist.cpp:745` | cleanupGamelist: the media file a game's name implies, by suffix and extension | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves media restored since unlinked | recorded with L-05 |
| `Gamelist.cpp:748` | cleanupGamelist: the media file a game's name implies, by suffix and extension | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves media restored since unlinked | recorded with L-05 |
| `Genres.cpp:22` | genres.xml in the resources | nobody: the image's read-only tree | cached | read once | left cached |
| `KeyboardMapping.cpp:222` | a game's or system's .keys file | ES (writes :426, :429); the player; a settings restore | cached | a remembered miss loads no mapping until the next launch resets the cache | left cached: outside the lanes (D-UI-079) |
| `KeyboardMapping.cpp:324` | deleteFile: the .keys file | ES (writes :426, :429, not through Utils::FileSystem) | cached | a mapping saved this session and deleted before a launch: the remembered miss skips removeFile, the file stays | recorded: outside the lanes (D-UI-079) |
| `MetaData.cpp:223` | loadFromXML with PreloadMedias: each image, thumbnail or marquee path | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | the load is at startup or a reload; a file absent then drops its metadata until the next load | recorded: the family of L-05 |
| `SystemRandomPlaylist.cpp:87` | a random game's media path | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit hands a removed file to the player; a remembered miss skips one restored since | recorded with L-11: outside the lanes (D-UI-079) |
| `SystemRandomPlaylist.cpp:97` | a random game's media path | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit hands a removed file to the player; a remembered miss skips one restored since | recorded with L-11: outside the lanes (D-UI-079) |
| `SystemRandomPlaylist.cpp:104` | a random game's media path | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit hands a removed file to the player; a remembered miss skips one restored since | recorded with L-11: outside the lanes (D-UI-079) |
| `SystemScreenSaver.cpp:51` | the screensaver's title folder | ES itself (createDirectory) | cached | harmless | left cached |
| `SystemScreenSaver.cpp:157` | startScreenSaver: ten retries for a random game video | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | ten retries over the same cached answers never see a file appear; a removed video's remembered hit is handed on | L-11: recorded, outside the lanes (D-UI-079) |
| `SystemScreenSaver.cpp:164` | startScreenSaver: the chosen video or image before it plays | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit plays a removed file (the player sees the fallback) | L-11: recorded, outside the lanes (D-UI-079) |
| `SystemScreenSaver.cpp:208` | startScreenSaver: the chosen video or image before it plays | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit plays a removed file (the player sees the fallback) | L-11: recorded, outside the lanes (D-UI-079) |
| `SystemScreenSaver.cpp:375` | the screensaver's title folder | ES itself (createDirectory) | cached | harmless | left cached |
| `SystemScreenSaver.cpp:388` | the screensaver's title folder | ES itself (createDirectory) | cached | harmless | left cached |
| `SystemScreenSaver.cpp:694` | the bezel set's systems folder, its image and .info | a theme installer (ES's own, through Utils::FileSystem) or the player | cached | a remembered miss shows the screensaver without the bezel | left cached: theme files |
| `SystemScreenSaver.cpp:730` | the bezel set's systems folder, its image and .info | a theme installer (ES's own, through Utils::FileSystem) or the player | cached | a remembered miss shows the screensaver without the bezel | left cached: theme files |
| `SystemScreenSaver.cpp:733` | the bezel set's systems folder, its image and .info | a theme installer (ES's own, through Utils::FileSystem) or the player | cached | a remembered miss shows the screensaver without the bezel | left cached: theme files |
| `SystemScreenSaver.cpp:787` | the game's marquee for the screensaver | outside ES only (cloud_content_restore's game content, D-CLOUD-049; the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss hides the marquee | L-11's family: recorded |
| `Win32ApiSystem.cpp:76` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:82` | Windows-only paths (3 calls) | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:85` | Windows-only paths (2 calls) | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:159` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:166` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:324` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:329` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:349` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:354` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:378` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:383` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:484` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:653` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:657` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:661` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:672` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:729` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:739` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:783` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:802` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:831` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:840` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:866` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:871` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:915` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:947` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:968` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:984` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:1210` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:1214` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |
| `Win32ApiSystem.cpp:1217` | Windows-only paths | none: the file is `#if WIN32` (:1-:1267) and compiles to nothing | cached | nothing: no image carries it | L-21: dead on every image; recorded |

generated, asserted: 83 lines, 86 calls, 4 uncached, in 11 files

## The bounds

The table covers every network or script wait reachable from the 77, in three kinds: an HttpReq construction, a process start (§ 5's grep), and a wait the grep cannot see (L-01, L-02, L-09).

The brief's § 5 "HttpReq lines" (`OfflineAchievementsText.h:1`, `ScraperCmdLine.cpp:1`, `Win32ApiSystem.cpp:3`, `ZaparooSupport.cpp:5`) count every line naming HttpReq. The constructions among them are four: two live, both Zaparoo's, and two dead. The one option line is `ZaparooSupport.cpp:38`, a `connectTimeout`.

The slice's own code sets no total or stall bound anywhere. The one bounded process is `CloudOffer.cpp:37`'s `timeout 90` (L-18: the bound is sound). The unbounded live waits are:
- L-01: es-core's lock reached from the interface thread;
- L-09: Zaparoo's probe, its card and its lock, outside the lanes;
- `retroarch.cfg`'s read after every exit (L-02).

| Line | Kind | What waits | Thread | Bound as written | Bounded | Lead |
| --- | --- | --- | --- | --- | --- | --- |
| `Win32ApiSystem.cpp:468` | http | bezels.txt (dead) | -- | dead inside `#if WIN32` | dead | L-21 |
| `Win32ApiSystem.cpp:921` | http | the update version URL (dead) | -- | dead inside `#if WIN32` | dead | L-21 |
| `ZaparooSupport.cpp:39` | http | `isZaparooEnabled`: GET `127.0.0.1:7497/health`, under `mZaparooLock` | a detached thread (`:22-27`, `checkZaparooEnabledAsync`); and the caller's thread for a direct call (`guis/GuiGameOptions.cpp:59`, `:281`) | connect `defaultDelay` (3 s from the async probe, `:38`); no total, no stall | **no** | L-09: a service that accepts and never answers holds the probe and `mZaparooLock` forever |
| `ZaparooSupport.cpp:62` | http | `writeZaparooCard`: POST `127.0.0.1:7497/api/v0.1` | the caller's (the game-options page, the interface thread) | connect 10 s (the default); no total, no stall | **no** | L-09: unbounded after connect; outside the lanes, recorded |
| `CloudOffer.cpp:37` | process | `cloud_setup --seed-folders saves` | `GuiLoading`'s worker; the page waits | `timeout 90` | yes | L-18: the bound is sound; rc 0 alone reads DONE |
| `Win32ApiSystem.cpp:314` | process | `executeScript(command)` defined (dead) | -- | dead inside `#if WIN32` | dead | L-21 |
| `Win32ApiSystem.cpp:340` | process | `executeScript(command, fn)` defined (dead) | -- | dead inside `#if WIN32` | dead | L-21 |
| `Win32ApiSystem.cpp:1264` | process | `batocera-bluetooth forgetBT` (dead) | -- | dead inside `#if WIN32` | dead | L-21 |
| `Win32ApiSystem.h:55` | process | `executeScript` declared (dead with its file) | -- | a declaration | dead | L-21 |
| `Win32ApiSystem.h:56` | process | `executeScript` declared (dead with its file) | -- | a declaration | dead | L-21 |
| `NetworkThread.cpp:24` | wait | `checkCheevosTokenSoon` -> es-core's `ResetComponent`, which takes `mWatchersLock` (`WatchersManager.cpp:92-100`) | the interface thread (`guis/GuiRetroAchievementsSettings.cpp:806`, `:257`, `:191`) | as long as the watcher thread holds `mWatchersLock` across every `check()` (`WatchersManager.cpp:181-196`), each of which may be a network call | **no** | L-01: rule 6, es-core's lock (T21's file) put to the pause |
| `CaptureRotation.cpp:158` | wait | the whole `/var/log/exec.log`, read and scanned | the interface thread, after every RetroArch exit (`FileData.cpp:1166-1167`) | the launcher's truncation (#280): the log is this session's only | yes | L-02: priced by the retro's time-to-play line (G-03's `stat`) |
| `CaptureRotation.cpp:162` | wait | `retroarch.cfg`, read and scanned | the interface thread, after every RetroArch exit | none: the file's size, which nothing bounds (L-02: the launcher's truncation covers only the log) | **no** | L-02 |
| `ZaparooSupport.cpp:32` | wait | `mZaparooLock` taken by `isZaparooEnabled` | whichever thread asks second, the game-options page among them | as long as the first holder's request (no total bound above) | **no** | L-09 |

generated, asserted: 4 http, 6 process lines, 4 waits; 7 live, 2 bounded, 7 dead (Win32)

## The words

The 176 `_("` lines, 223 calls and 196 distinct msgids, each against the French catalog at the pin (`locale/lang/fr/LC_MESSAGES/emulationstation2.po`, continuation lines joined). Beyond the table, five more items:
- **L-25:** `FileTag.cpp:6-11` passes six of nine tag names through `fake_gettext_*`. `IN PROGRESS`, `DROPPED` and `ON HOLD` are not there and have no msgid; they reach T31's filter and editor pages in English under French. The catalog's six are at po 717, 3576, 3579, 3582, 3585 and 3588. proved: (stage C) 3.29's case; tool-run (`stage-a/runs.out`'s msgid grep).
- **L-26:** `LangParser.cpp:65`'s `"ìndia"` is a string literal, so xgettext is unaffected, but the token is unreachable. proved: (stage C) 3.31's case.
- **The dialog words** (7 `GuiMsgBox`, 1 `GuiLoading`, 2 text-edit popups; `stage-a/runs.out`):
  - `CloudOffer.cpp:51` has CHANGE FOLDER / CREATE ANYWAY / NOT NOW, and `:59` has CREATE IT / NOT NOW. Back falls through to the last button, NOT NOW, the safe one (`es-ui-style-guide.md` § Confirmations).
  - `:42`'s outcome box is DONE... / COULDN'T CREATE IT. CHECK YOUR CONNECTION AND TRY AGAIN FROM MANAGE CLOUD STORAGE. on rc alone (L-18).
  - `components/ScraperSearchComponent.cpp:386` is an English sentence-case message upper-cased by `toUpper`, outside `_()`, with a bare `"FINISH"`: no French reaches it.
  - `:468` reads AN ERROR OCCURRED: <the tool's error, upper-cased> with RETRY / SKIP.
  - `ThreadedBluetooth.cpp:54` and `:118` are single-OK boxes.
  - These four, the two scraper boxes and the two Bluetooth boxes, are upstream-carried and outside the lanes (D-UI-079), recorded.
- **L-10's toasts:** `ContentInstaller.cpp:144`, `:163`, `:182`, `:200`, `:218` and `:236` read `AN ERROR OCCURRED: <status>`, a tool's text on a player's toast. Recorded, outside the lanes.
- **The one help bar:** `ScraperSearchComponent::getHelpPrompts` (`:738-744`) adds ACCEPT RESULT to the grid's only while a row is selected. It offers a direction only where the grid moves (`es-code-traps.md` § The help bar).

| msgid | Sites | French (po line) |
| --- | --- | --- |
| `2 players` | `CollectionSystemManager.cpp:42` | 2 joueurs (L3509) |
| `4 players` | `CollectionSystemManager.cpp:43` | 4 joueurs (L3512) |
| `A DRIVE IS ALREADY BEING FORMATTED.` | `ThreadedBluetooth.cpp:118` | UN DISQUE EST DÉJÀ EN COURS DE FORMATAGE. (L3633) |
| `A REBOOT IS REQUIRED TO COMPLETE THE OPERATION` | `ThreadedBluetooth.cpp:108` | UN REDÉMARRAGE EST NÉCESSAIRE POUR FINALISER L’OPÉRATION (L3630) |
| `A,AN,THE` | `FileSorts.cpp:83` | LE,LA,LES,L’,UN,UNE,DE,DES,D’,AU,A,AUX (L3233) |
| `ACCEPT RESULT` | `ScraperSearchComponent.cpp:742` | ACCEPTER LE RÉSULTAT (L58) |
| `ALREADY PLAYED` | `FileFilterIndex.cpp:41` | DÉJÀ JOUÉ (L3663) |
| `AN ERROR OCCURRED` | `ContentInstaller.cpp:144`, `ContentInstaller.cpp:163`, `ContentInstaller.cpp:182`, `ContentInstaller.cpp:200`, `ContentInstaller.cpp:218`, `ContentInstaller.cpp:236`, `ScraperSearchComponent.cpp:468` | UNE ERREUR EST SURVENUE (L40) |
| `Added '%s' to '%s'` | `CollectionSystemManager.cpp:758` | '%s' ajouté à '%s' (L3543) |
| `Alt BoxArt` | `MetaData.cpp:63` | Boîte (Alt) (L3365) |
| `Arcade system` | `MetaData.cpp:78` | Système arcade (L3416) |
| `BEZELS INSTALLED SUCCESSFULLY` | `ContentInstaller.cpp:178` | DÉCORATIONS INSTALLÉES AVEC SUCCÈS (L3257) |
| `BEZELS UNINSTALLED SUCCESSFULLY` | `ContentInstaller.cpp:196` | DÉCORATIONS DÉSINSTALLÉES AVEC SUCCÈS (L1649) |
| `BLUETOOTH SCAN IS ALREADY RUNNING.` | `ThreadedBluetooth.cpp:54` | DÉCOUVERTE BLUETOOTH DÉJÀ EN COURS. (L1138) |
| `BUGGY` | `FileTag.cpp:9` | BOGUÉ (L3582) |
| `Box` | `MetaData.cpp:53` | Boite (L3317) |
| `Box backside` | `MetaData.cpp:64` | Dos de la boîte (L3371) |
| `CANCEL` | `ScraperSearchComponent.cpp:471` | ANNULER (L49) |
| `CHANGE FOLDER` | `CloudOffer.cpp:54` | CHANGER DE DOSSIER (L4638) |
| `COULDN'T CREATE IT. CHECK YOUR CONNECTION AND TRY AGAIN FROM MANAGE CLOUD STORAGE.` | `CloudOffer.cpp:44` | IMPOSSIBLE DE LE CRÉER. VÉRIFIEZ VOTRE CONNEXION ET RÉESSAYEZ DEPUIS GÉRER LE STOCKAGE CLOUD. (L4632) |
| `CREATE ANYWAY` | `CloudOffer.cpp:55` | CRÉER QUAND MÊME (L4641) |
| `CREATE IT` | `CloudOffer.cpp:63` | LE CRÉER (L4650) |
| `Cartridge` | `MetaData.cpp:62` | Cartouche (L3359) |
| `Cheevos Game ID` | `MetaData.cpp:96`, `MetaData.cpp:96` | Game ID Cheevos (L3482) |
| `Cheevos Hash` | `MetaData.cpp:95` | Hash Cheevos (L3476) |
| `Cheevos checksum` | `MetaData.cpp:95` | Checksum Cheevos (L3479) |
| `Core` | `MetaData.cpp:43`, `MetaData.cpp:47` | Cœur (L2731) |
| `Crc32` | `MetaData.cpp:87` | Crc32 (L3449) |
| `Crc32 checksum` | `MetaData.cpp:87` | Checksum CRC32 (L3452) |
| `DEVELOPER, ASCENDING` | `FileSorts.cpp:57` | DEVELOPPEUR, CROISSANT (L3191) |
| `DEVELOPER, DESCENDING` | `FileSorts.cpp:58` | DEVELOPPEUR, DÉCROISSANT (L3194) |
| `DISLIKED` | `FileTag.cpp:11` | J’AIME PAS (L3588) |
| `DONE. YOUR SAVES WILL GO THERE THE NEXT TIME YOU BACK THEM UP.` | `CloudOffer.cpp:43` | TERMINÉ. VOS SAUVEGARDES IRONT LÀ À LA PROCHAINE SAUVEGARDE. (L4629) |
| `DOWNLOADING` | `ContentInstaller.cpp:78` | TÉLÉCHARGEMENT (L3251) |
| `Description` | `MetaData.cpp:34` | Description (L3272) |
| `Developer` | `MetaData.cpp:70`, `ScraperSearchComponent.cpp:65` | Développeur (L22) |
| `Downloading` | `ScraperSearchComponent.cpp:597`, `ScraperSearchComponent.cpp:616` | Téléchargement (L52) |
| `Emulator` | `MetaData.cpp:42`, `MetaData.cpp:46` | Émulateur (L2728) |
| `Extracting` | `Win32ApiSystem.cpp:517` | Extraction (L3143) |
| `FAMILY` | `FileFilterIndex.cpp:33` | FAMILLE (L3642) |
| `FAVORITES` | `FileFilterIndex.cpp:30` | FAVORIS (L944) |
| `FILE CREATION DATE, ASCENDING` | `FileSorts.cpp:63` | DATE D’AJOUT, CROISSANT (L3209) |
| `FILE CREATION DATE, DESCENDING` | `FileSorts.cpp:64` | DATE D’AJOUT, DÉCROISSANT (L3212) |
| `FILENAME, ASCENDING` | `FileSorts.cpp:43` | NOM DU JEU, CROISSANT (L3149) |
| `FILENAME, DESCENDING` | `FileSorts.cpp:44` | NOM DU JEU, DÉCROISSANT (L3152) |
| `FINISHED` | `FileTag.cpp:6` | TERMINÉ (L717) |
| `FORMATTING DEVICE` | `ThreadedBluetooth.cpp:73` | FORMATAGE DU PÉRIPHÉRIQUE (L3624) |
| `Fan art` | `MetaData.cpp:55` | Fanart (L3323) |
| `Favorite` | `MetaData.cpp:81` | Favori (L194) |
| `Formatting` | `ThreadedBluetooth.cpp:74` | Formatage (L3627) |
| `GAME TIME, ASCENDING` | `FileSorts.cpp:65` | TEMPS DE JEU, CROISSANT (L3215) |
| `GAME TIME, DESCENDING` | `FileSorts.cpp:66` | TEMPS DE JEU, DÉCROISSANT (L3218) |
| `GENRE` | `FileFilterIndex.cpp:31` | GENRE (L3636) |
| `GENRE, ASCENDING` | `FileSorts.cpp:55` | GENRE, CROISSANT (L3185) |
| `GENRE, DESCENDING` | `FileSorts.cpp:56` | GENRE, DÉCROISSANT (L3188) |
| `Game family` | `MetaData.cpp:73` | Famille de jeu (L3404) |
| `Game time` | `MetaData.cpp:90` | Temps de jeu (L191) |
| `Genre` | `MetaData.cpp:36`, `ScraperSearchComponent.cpp:66` | Genre (L25) |
| `Genres` | `MetaData.cpp:76` | Genres (L3410) |
| `HAS ACHIEVEMENTS` | `FileFilterIndex.cpp:42` | AVEC DES SUCCÈS (L3666) |
| `HAVING MEDIAS` | `FileFilterIndex.cpp:48` | AYANT DES MÉDIAS (L3684) |
| `Hidden` | `MetaData.cpp:82` | Caché (L3428) |
| `Image` | `MetaData.cpp:50` | Image (L3299) |
| `Interlaced` | `Win32ApiSystem.cpp:1064` | Entrelacé (L3146) |
| `KIDGAME` | `FileFilterIndex.cpp:40` | JEU ENFANT (L3660) |
| `Kidgame` | `MetaData.cpp:83` | Jeu enfant (L3434) |
| `LANGUAGE` | `FileFilterIndex.cpp:38` | LANGUE (L2325) |
| `LAST PLAYED, ASCENDING` | `FileSorts.cpp:49` | DERNIÈRES PARTIES, CROISSANT (L3167) |
| `LAST PLAYED, DESCENDING` | `FileSorts.cpp:50` | DERNIÈRES PARTIES, DÉCROISSANT (L3170) |
| `LIGHTGUN` | `FileFilterIndex.cpp:44` | PISTOLET OPTIQUE (L3672) |
| `LIKED` | `FileTag.cpp:10` | J’AIME (L3585) |
| `Languages` | `MetaData.cpp:92` | Langues (L3464) |
| `Last played` | `MetaData.cpp:85` | Dernier jeu (L185) |
| `Logo` | `MetaData.cpp:52` | Logo (L3311) |
| `MISSING MEDIAS` | `FileFilterIndex.cpp:49` | MEDIAS MANQUANTS (L3687) |
| `Magazine` | `MetaData.cpp:58` | Magazine (L3341) |
| `Manual` | `MetaData.cpp:57` | Manuel (L3335) |
| `Map` | `MetaData.cpp:59` | Carte (L3347) |
| `Md5` | `MetaData.cpp:88` | Md5 (L3455) |
| `Md5 checksum` | `MetaData.cpp:88` | Checksum MD5 (L3458) |
| `Mix` | `MetaData.cpp:66` | Mix d’images (L3383) |
| `MultiDisk` | `MetaData.cpp:100`, `MetaData.cpp:100` | MultiDisque (L3488) |
| `NO GAMES FOUND - SKIP` | `ScraperSearchComponent.cpp:392` | AUCUN JEU NE CORRESPOND - PASSER (L37) |
| `NOT NOW` | `CloudOffer.cpp:56`, `CloudOffer.cpp:64` | PAS MAINTENANT (L4313) |
| `NOT WORKING` | `FileTag.cpp:8` | NE FONCTIONNE PAS (L3579) |
| `NOTHING TO RESTORE: YOUR CLOUD HAS %s, NOT %s.\n\nIS THE NAME RIGHT?` | `CloudOffer.cpp:52` | RIEN À RESTAURER : VOTRE CLOUD CONTIENT %s, PAS %s.

LE NOM EST-IL LE BON ? (L4635) |
| `NUMBER PLAYERS, ASCENDING` | `FileSorts.cpp:51` | NOMBRE DE JOUEURS, CROISSANT (L3173) |
| `NUMBER PLAYERS, DESCENDING` | `FileSorts.cpp:52` | NOMBRE DE JOUEURS, DÉCROISSANT (L3176) |
| `Name` | `MetaData.cpp:33` | Nom (L3266) |
| `None` | `CollectionSystemManager.cpp:801`, `CollectionSystemManager.cpp:802`, `CollectionSystemManager.cpp:833`, `CollectionSystemManager.cpp:834` | Aucun (L3554) |
| `OK` | `CloudOffer.cpp:45` | OK (L119) |
| `PACKAGE INSTALLED SUCCESSFULLY` | `ContentInstaller.cpp:214` | PAQUET INSTALLÉ AVEC SUCCÈS (L3260) |
| `PACKAGE REMOVED SUCCESSFULLY` | `ContentInstaller.cpp:232` | PAQUET SUPPRIMÉ AVEC SUCCÈS (L3263) |
| `PLAYERS` | `FileFilterIndex.cpp:34` | JOUEURS (L3645) |
| `PUBLISHER, ASCENDING` | `FileSorts.cpp:59` | EDITEUR, CROISSANT (L3197) |
| `PUBLISHER, DESCENDING` | `FileSorts.cpp:60` | EDITEUR, DÉCROISSANT (L3200) |
| `PUBLISHER/DEVELOPER` | `FileFilterIndex.cpp:35` | ÉDITEUR/DÉVELOPPEUR (L3648) |
| `Play count` | `MetaData.cpp:84` | Nombre de parties (L3440) |
| `Players` | `MetaData.cpp:80`, `ScraperSearchComponent.cpp:67` | Joueurs (L28) |
| `Publisher` | `MetaData.cpp:71`, `ScraperSearchComponent.cpp:64` | Éditeur (L19) |
| `RATING` | `FileFilterIndex.cpp:36` | NOTATION (L3651) |
| `RATING, ASCENDING` | `FileSorts.cpp:45` | NOTATION, CROISSANTE (L3155) |
| `RATING, DESCENDING` | `FileSorts.cpp:46` | NOTATION, DÉCROISSANTE (L3158) |
| `REGION` | `FileFilterIndex.cpp:39` | RÉGION (L3657) |
| `RELEASE DATE, ASCENDING` | `FileSorts.cpp:53` | DATE DE SORTIE, CROISSANT (L3179) |
| `RELEASE DATE, DESCENDING` | `FileSorts.cpp:54` | DATE DE SORTIE, DÉCROISSANT (L3182) |
| `RELEASE YEAR, SYSTEM, ASCENDING` | `FileSorts.cpp:70` | ANNÉE DE SORTIE, SYSTÈME, CROISSANT (L3227) |
| `RELEASE YEAR, SYSTEM, DESCENDING` | `FileSorts.cpp:71` | ANNÉE DE SORTIE, SYSTÈME, DÉCROISSANT (L3230) |
| `RETRY` | `ScraperSearchComponent.cpp:469` | RECOMMENCER (L43) |
| `Rating` | `MetaData.cpp:68`, `ScraperSearchComponent.cpp:69` | Notation (L34) |
| `Region` | `MetaData.cpp:93` | Région (L3470) |
| `Release date` | `MetaData.cpp:69` | Date de sortie (L3392) |
| `Released` | `ScraperSearchComponent.cpp:68` | Date de sortie (L31) |
| `Removed '%s' from '%s'` | `CollectionSystemManager.cpp:760` | '%s' supprimé de '%s' (L3547) |
| `RetroAchievements` | `CollectionSystemManager.cpp:45` | RetroAchievements (L3518) |
| `SCANNING BLUETOOTH` | `ThreadedBluetooth.cpp:16` | DÉCOUVERTE BLUETOOTH (L711) |
| `SEARCH` | `FileFilterIndex.cpp:1372` | RECHERCHER (L173) |
| `SEARCH FOR` | `ScraperSearchComponent.cpp:724`, `ScraperSearchComponent.cpp:731` | CHERCHER (L55) |
| `SETTING UP YOUR CLOUD FOLDERS` | `CloudOffer.cpp:34` | CRÉATION DE VOS DOSSIERS CLOUD (L4626) |
| `SKIP` | `ScraperSearchComponent.cpp:470` | PASSER (L46) |
| `SLOW` | `FileTag.cpp:7` | LENT (L3576) |
| `SPINNER` | `FileFilterIndex.cpp:47` | SPINNER (L3681) |
| `STEERING WHEEL` | `FileFilterIndex.cpp:45` | VOLANT (L3675) |
| `SYSTEM, ASCENDING` | `FileSorts.cpp:61` | SYSTÈME, CROISSANT (L3203) |
| `SYSTEM, DESCENDING` | `FileSorts.cpp:62` | SYSTÈME, DÉCROISSANT (L3206) |
| `SYSTEM, RELEASE YEAR, ASCENDING` | `FileSorts.cpp:68` | SYSTÈME, ANNÉE DE SORTIE, CROISSANT (L3221) |
| `SYSTEM, RELEASE YEAR, DESCENDING` | `FileSorts.cpp:69` | SYSTÈME, ANNÉE DE SORTIE, DÉCROISSANT (L3224) |
| `Screenscraper Game ID` | `MetaData.cpp:98`, `MetaData.cpp:98` | Game ID Screenscraper (L3485) |
| `Searching` | `ScraperSearchComponent.cpp:31`, `ScraperSearchComponent.cpp:355`, `ScraperSearchComponent.cpp:623` | Recherche (L16) |
| `Searching for devices...` | `ThreadedBluetooth.cpp:17` | Recherche de manettes… (L3621) |
| `Sort name` | `MetaData.cpp:39` | Nom du tri (L3287) |
| `TAG` | `FileFilterIndex.cpp:32` | BALISE (L3639) |
| `THEME INSTALLED SUCCESSFULLY` | `ContentInstaller.cpp:140` | THÈME INSTALLÉ AVEC SUCCÈS (L3254) |
| `THEME UNINSTALLED SUCCESSFULLY` | `ContentInstaller.cpp:159` | THÈME DÉSINSTALLÉ AVEC SUCCÈS (L819) |
| `TIMES PLAYED, ASCENDING` | `FileSorts.cpp:47` | PARTIES JOUÉES, CROISSANT (L3161) |
| `TIMES PLAYED, DESCENDING` | `FileSorts.cpp:48` | PARTIES JOUÉES, DÉCROISSANT (L3164) |
| `TRACKBALL` | `FileFilterIndex.cpp:46` | TRACKBALL (L3678) |
| `Tags` | `MetaData.cpp:38` | Balises (L3281) |
| `This collection is empty.` | `CollectionSystemManager.cpp:797` | Cette collection est vide. (L3550) |
| `Title shot` | `MetaData.cpp:56` | Image avec titre (L3329) |
| `UPDATE AVAILABLE` | `NetworkThread.cpp:198` | MISE À JOUR DISPONIBLE (L3591) |
| `VERTICAL` | `FileFilterIndex.cpp:43` | VERTICAL (L3669) |
| `Various` | `CollectionSystemManager.cpp:833`, `CollectionSystemManager.cpp:834` | Divers (L3557) |
| `Video` | `MetaData.cpp:51` | Vidéo (L3305) |
| `Wheel` | `MetaData.cpp:65` | Logo (L3377) |
| `YEAR` | `FileFilterIndex.cpp:37` | ANNÉE (L3654) |
| `YOUR CLOUD HAS NO %s FOLDER YET.\n\nCREATE IT NOW?` | `CloudOffer.cpp:62` | VOTRE CLOUD N’A PAS ENCORE DE DOSSIER %s.

LE CRÉER MAINTENANT ? (L4647) |
| `YOUR CLOUD HAS NO SAVES FOLDER YET.\n\nCREATE IT NOW?` | `CloudOffer.cpp:61` | VOTRE CLOUD N’A PAS ENCORE DE DOSSIER DE SAUVEGARDES.

LE CRÉER MAINTENANT ? (L4644) |
| `all games` | `CollectionSystemManager.cpp:39` | tous les jeux (L3500) |
| `arcade` | `CollectionSystemManager.cpp:48` | arcade (L3521) |
| `collections` | `CollectionSystemManager.cpp:56` | collections (L3539) |
| `core` | `MetaData.cpp:43`, `MetaData.cpp:47` | cœur (L3296) |
| `emulator` | `MetaData.cpp:42`, `MetaData.cpp:46` | émulateur (L3293) |
| `enter favorite` | `MetaData.cpp:81` | entrer le favori (L3425) |
| `enter game genre` | `MetaData.cpp:36` | entrer le genre du jeu (L3278) |
| `enter game genres` | `MetaData.cpp:76` | entrer le(s) genre(s) du jeu (L3413) |
| `enter game sort name` | `MetaData.cpp:39` | entrer le nom du tri (L3290) |
| `enter hidden` | `MetaData.cpp:82` | entrer le jeu caché (L3431) |
| `enter kidgame` | `MetaData.cpp:83` | entrer le jeu enfant (L3437) |
| `enter last played date` | `MetaData.cpp:85` | entrer la date de la dernière partie (L3446) |
| `enter number of times played` | `MetaData.cpp:84` | entrer le nombre de parties (L3443) |
| `enter path to alt boxart` | `MetaData.cpp:63` | entrer le chemin vers la boîte (Alt) (L3368) |
| `enter path to box` | `MetaData.cpp:53` | entrer le chemin vers la boîte (L3320) |
| `enter path to box background` | `MetaData.cpp:64` | entrer le chemin vers le dos de la boîte (L3374) |
| `enter path to cartridge` | `MetaData.cpp:62` | entrer le chemin vers la cartouche (L3362) |
| `enter path to fan art` | `MetaData.cpp:55` | entrer le chemin vers le fanart (L3326) |
| `enter path to image` | `MetaData.cpp:50` | entrer le chemin vers l’image (L3302) |
| `enter path to logo` | `MetaData.cpp:52` | entrer le chemin vers le logo (L3314) |
| `enter path to magazine` | `MetaData.cpp:58` | entrer le chemin vers le magazine (L3344) |
| `enter path to manual` | `MetaData.cpp:57` | entrer le chemin vers le manuel (L3338) |
| `enter path to map` | `MetaData.cpp:59` | entrer le chemin vers la carte (L3350) |
| `enter path to mix` | `MetaData.cpp:66` | entrer le chemin vers le mix d’images (L3386) |
| `enter path to title shot` | `MetaData.cpp:56` | entrer le chemin vers l’image titre (L3332) |
| `enter path to video` | `MetaData.cpp:51` | entrer le chemin vers la vidéo (L3308) |
| `enter path to wheel` | `MetaData.cpp:65` | entrer le chemin vers le logo (L3380) |
| `enter rating` | `MetaData.cpp:68` | entrer la notation (L3389) |
| `enter release date` | `MetaData.cpp:69` | entrer la date de sortie (L3395) |
| `favorites` | `CollectionSystemManager.cpp:41` | favoris (L3506) |
| `how long the game has been played in total (seconds)` | `MetaData.cpp:90` | entrer le temps de jeu (L3461) |
| `last played` | `CollectionSystemManager.cpp:40` | dernier joué (L3503) |
| `lightgun games` | `CollectionSystemManager.cpp:50` | jeux au pistolet (L3527) |
| `never played` | `CollectionSystemManager.cpp:44` | jamais joué (L3515) |
| `spinner games` | `CollectionSystemManager.cpp:53` | jeux au spinner (L3536) |
| `tags` | `MetaData.cpp:38` | balises (L3284) |
| `this game's arcade system` | `MetaData.cpp:78` | système arcade du jeu (L3419) |
| `this game's description` | `MetaData.cpp:34` | description du jeu (L3275) |
| `this game's developer` | `MetaData.cpp:70` | développeur du jeu (L3398) |
| `this game's game family` | `MetaData.cpp:73` | famille du jeu (L3407) |
| `this game's languages` | `MetaData.cpp:92` | langues du jeu (L3467) |
| `this game's name` | `MetaData.cpp:33` | nom du jeu (L3269) |
| `this game's number of players` | `MetaData.cpp:80` | nombre de joueurs du jeu (L3422) |
| `this game's publisher` | `MetaData.cpp:71` | éditeur du jeu (L3401) |
| `this game's region` | `MetaData.cpp:93` | région du jeu (L3473) |
| `trackball games` | `CollectionSystemManager.cpp:52` | jeux au trackball (L3533) |
| `vertical arcade` | `CollectionSystemManager.cpp:49` | arcade vertical (L3524) |
| `wheel games` | `CollectionSystemManager.cpp:51` | jeux au volant (L3530) |

generated, asserted: 176 lines, 223 calls, 196 distinct msgids in 11 files; 0 with an empty French msgstr, 0 with no msgid

## The structure

**`es-app/CMakeLists.txt`** (brief § 2's row, read at the pin):
- **The four conditionals:**
  - `if(WIN32)` `:3-29`, with `if(INJECT_VERSION)` nested `:7-28`;
  - three `if(MSVC)`: `:292-296`, `:299-311` and `:320-329`.
- No `BATOCERA` or `ROCKNIX` condition, no `add_definitions` and no test target.
- 30 of the slice's 31 `.cpp` are in `ES_SOURCES`; `ScraperCmdLine.cpp` is absent (L-22).
- 34 of the 41 headers are in `ES_HEADERS`. The seven not listed are `AppWindow.h`, `FolderMerge.h`, `GameCubeRvzHashRetry.h`, `JourneyTiers.h`, `RunLock.h`, `ScraperCmdLine.h` and `TextFit.h`. This is a listing omission, not a build one: headers compile through their includers.
- T21's branch adds ten lines to this file (`origin/feature/m6-es-state-and-bridge-668`, `stage-a/runs.out`), named as a collision for any stream that edits it.

**The Windows residue** (L-21, one row each, D-WORKFLOW-209):

| Path | What it is | Disposition proposed |
| --- | --- | --- |
| `Win32ApiSystem.cpp` | `#if WIN32` `:1` to `:1267`, listed unconditionally (`CMakeLists.txt:287`); preprocesses to nothing on every image (`stage-a/syntax-check.out`); the fork's three lines `:316`, `:341`, `:368` | recorded: provenance, not a defect |
| `Win32ApiSystem.h` | the class's header, 70 lines, `executeScript` declared `:55-56` | recorded with it |
| `EmulationStation.h.in`, `EmulationStation.rc`, `EmulationStation.aps`, `es_icon.ico` | the Windows version resource and icon (`if(WIN32)` `:3-29`) | recorded: never built on an image |
| `ScraperCmdLine.cpp` / `.h` | 290 lines of console scraping in no list; its `platform.h` does not exist (class (f)) | recorded as Backlog #1235's shape; never deleted by the lane (`engineering-practices.md` § Before deleting a duplicate) |

**The credential macros** are not in this slice. Brief § 1's sentence is the one statement of where they live.

**The map** (D-UI-039). `tools/es-menu-map-check` prints `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`, rc 0 (`stage-a/runs.out`). It still cannot see the two filter pages. Their titles are passed in a member initializer, `mMenu(window, _("FILTER GAMELIST BY"))` (`guis/GuiGamelistFilter.cpp:11`) and `mMenu(window, _("EDIT DYNAMIC COLLECTION FILTERS"))` (`:17`), and none of the check's three patterns (`tools/es-menu-map-check:48-55`: `new GuiSettings(`, `GuiSettings(` constructed directly, `MenuComponent(`) reads that form. UPDATE GAMELISTS is an action row, not a screen, so the check never reads it.

The proposed text follows. A stage-E stream the coordinator writes adds it to `docs/es-menu-map.md`, in the same commit as any row that stream touches. The lane does not edit the map.

- Under **`## What lives where`**, the GAME SETTINGS row's TOOLS group gains its first row. GAME COLLECTION's OPTIONS gains the same row:
  > `UPDATE GAMELISTS` -- GAME SETTINGS > TOOLS (`guis/GuiMenu.cpp:5756`) and GAME COLLECTION SETTINGS > OPTIONS (`guis/GuiCollectionSystemsOptions.cpp:368`): one action in two places, the same call (`GuiMenu::updateGameLists`). It refuses while a scrape or the hasher runs (`GuiMenu.cpp:8501-8511`) and otherwise reloads the game lists. With INDEX NEW GAMES on, it ends in the hasher's toast INDEXING COMPLETED. UPDATE GAMELISTS TO APPLY CHANGES. (`ThreadedHasher.cpp:146`).
- A new short section, **`## Game list filters`**, after `## What lives where`:
  > **FILTER GAMELIST BY** -- a page of its own (`guis/GuiGamelistFilter.cpp:11`), opened from a game list's VIEW OPTIONS > NAVIGATION > OTHER FILTERS (`guis/GuiGamelistOptions.cpp:77-79`, `:435`). Each row is a facet of the system's `FileFilterIndex`; BACK applies the choice (`applyFilters`, `:39`, `:226-263`). Where a system's choice is kept across a restart is read at stage C before this text is final.
  >
  > **EDIT DYNAMIC COLLECTION FILTERS** -- the same page over a dynamic collection's index (`guis/GuiGamelistFilter.cpp:17`). It is opened from that collection's VIEW OPTIONS > DYNAMIC COLLECTION (`guis/GuiGamelistOptions.cpp:174-176`, `:603`) and from GAME COLLECTION SETTINGS when a dynamic collection is made (`guis/GuiCollectionSystemsOptions.cpp:495`). Its choices are written to the collection's `.xcc` in place (`FileFilterIndex.cpp:1313`, L-23).
- The check's half is named for the coordinator: a fourth pattern, `\bmMenu\s*\(\s*\w+\s*,\s*_\("([^"]+)"\)`, would let `tools/es-menu-map-check` see both titles. That is a change under `tools/`, which this lane does not make.

## The merge debt

**None.** The merge base with `rocknix/master` (`f6c542872e`) is `cada856d86`. Its parent `bccd715707` is the base the stale `upstream/master` ref still names, and `bccd715707..cada856d86` touches none of the 77. **0 of the 14 upstream commits since `cada856d86` touch the 77** (`upstream commits rc=1`, `upstream numstat rc=1`); upstream's whole delta is `GuiMenu.cpp` and `.h`. All 46 upstream-carried files are byte-identical to `rocknix/master` and to `cada856d86`. **The fork's four modified files:** `CMakeLists.txt` 44/0, `NetworkThread.cpp` 105/3, `NetworkThread.h` 29/1, `Win32ApiSystem.cpp` 3/3. **Batocera's six commits since `1750dded8c`** (`a79c12052`, `5f106acce`, `308221458`, `52710803c`, `7988b09d9`, `b69fb143c`) are context only: they are not ROCKNIX's, so they are never a debt figure and were never fetched. **Inherited from the other lanes:**
- T21's `es-app/CMakeLists.txt` +10/-0, `WifiText.cpp` +11/-0 and `WifiText.h` +13/-0 (`44d3c7e25 e38dcdefd eeee95265 31b49999e 00669ccd9 ba0e82c1f`);
- T20's `OfflineAchievementsText.cpp` +99/-0 and `.h` +52/-0 (`274a71add f85061f14`).

proved: tool-run (`stage-a/runs.out`; L-29).

## The runs

Stage A's runs are in `stage-a/runs.out` (brief § 5's block, each expectation met; the two errata accepted on #680 at 18:43 UTC) and `stage-a/syntax-check.out`.

| Run | Figure | A FAIL would mean | Where |
| --- | --- | --- | --- |
| the scope | 77; 31 `.cpp`, 41 `.h`, 5 other | a path dropped or added since the brief | `stage-a/runs.out` |
| the delta, three ways | `31 files changed, 2689 insertions(+), 7 deletions(-)` three times; 27 added; 4 modified; 72 commits, 68 non-merge | the bases disagree: the tiers would need two tables | `stage-a/runs.out` |
| upstream's delta | 0 rc=1, 0 rc=1; 46 identical twice | merge debt this slice would owe | `stage-a/runs.out` |
| the other lanes' deltas | T21 10/11/13 lines, T20 99/52; the rest empty | an unnamed collision at stage E | `stage-a/runs.out` |
| the strings | 176 lines in 11 files, 223 calls; 196 msgids, 0 empty, 0 missing | an untranslated or missing msgid | `stage-a/runs.out`; `tools/t33-words.py` |
| the French, both bases | `es-untranslated` 706/706 and 703/703, rc 0 | a fork string without French | `stage-a/runs.out` |
| the reads | 83 lines, 86 calls, 4 uncached | a read the table does not name | `tools/t33-reads.py` |
| the writes | 11 lines (9 compiled, 2 dead) | a writer the table does not name | `tools/t33-writes.py` |
| the bounds | 4 http, 6 process, 4 waits; 2 bounded, 7 dead | a wait the table does not name | `tools/t33-bounds.py` |
| the library | 11 units, each cited caller line holding its call | a fact read off a moved line | `tools/t33-library.py` |
| the helpers | 17 units in 27 files; 12 with a case, 7 built | a unit with a case nobody runs, unnamed | `tools/t33-helpers.py` |
| the map | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 | an undeclared screen | `stage-a/runs.out` |
| the compile | `es-syntax-check` rc 2 (no build root); plain `g++` rc 1 at `pugixml/src/pugixml.hpp`; the stand-in check 29/29 rc 0 | a class (a)-(d) file the host's g++ refuses | `stage-a/runs.out`, `stage-a/syntax-check.out` |
| the include graph | (stage C) `t33-includes.py` | -- | stage C |
| the unit build | (stage C) `t33-build-tests.sh`'s `TOTAL:` line, with `app-unit-tests` | -- | stage C |
| the generators' drifts | each exits 1 on a wrong count and on a paths list with its file dropped | a generator that cannot fail | `stage-b/generators.txt` |

## The guest cycle

One window, planned in `stage-b/window-plan.md` (brief § 5 item 2): 25 minutes plus 5 of grace, for a plan of 1,260 s.

Granted on #680 at 19:00 UTC (comment 6450973084). START 19:01:31 UTC (comment 6451000093). The guest was stopped by `tools/vm-stop` on its pidfile at 19:14:06 UTC (rc 0), 13 minutes into the 25. The image is M7's composition, so every frame below is `image`. Records and frames are under `guest-cycle/`.

| G | Result | proved: |
| --- | --- | --- |
| G-01 | `BUILD_ID=069fc270442134fe771258418adf4e666e0473fb`, `VERSION=0.0.1-dev+20261022T235948Z.g069fc2704421`, `640 480`; the slice's literals present in the installed binary (`SETTING UP YOUR CLOUD FOLDERS`, `from=checked-launch`, the two filter titles, `IN PROGRESS`, ...) | guest (`g01-identity.txt`) |
| G-02 | seeded `custom-t33.cfg` (Alpha) with the collection selected; it opens in the COLLECTIONS bundle (`g02-1-left3`, `g02-3-t33-list`); REMOVE FROM T33 on Alpha inside the bundle: the view rebuilt onto the bundle's `t33` folder, ES's pid unchanged (2308), no backtrace in the journal. **L-06 did not fault on one removal**: the heap's choice, as #246's was; the proof stays the ASan extract at stage C. The removal is written only later (the file kept its line until UPDATE GAMELISTS wrote it empty) | guest (`g02-l06.txt`, frames `g02-*`) |
| G-03 | UPDATE GAMELISTS is TOOLS's first row of GAME SETTINGS (`g03-1`), behind REALLY UPDATE GAMELISTS? YES / NO (`g03-2`); `/isIdle` `[ true ]` 8 s after YES; the three stubs listed (`g03-6-gb-list`); **no index toast**: INDEX NEW GAMES is not on in this fixture, so that half is not shown. SCREENSHOTS over 100 zero-byte captures of one stem: the first change 0.1 s after the press, settled 1.3 s later, on a four-game library: L-04's walk is not priced by this library. `/var/log/exec.log` absent (no RetroArch launch in the window): L-02's `stat` is not shown | guest (`g03-update.txt`, `g03-screenshots.txt`) |
| G-04 | **L-05 reproduced.** gb's `gamelist.xml` written from outside ES while it ran (an entry for Bravo with a description, md5 `055b53a8…`); Alpha starred (recorded at once in `recovery/gb/Alpha.xml`, `saveToXml`); QUIT > RESTART EMULATIONSTATION > YES (pid 3303 -> 4215): gb's `gamelist.xml` now holds Alpha's entry alone (md5 `d4307578…`), **Bravo's entry and its description gone**. The control, gbc's file written the same way with no dirty game, byte-identical. The recovery folder emptied by the clean exit; the path relative, only non-default fields. **Mine:** a first read at 19:07:52 was taken with REALLY RESTART EMULATIONSTATION? still open (`g04-5`) and is void as G-04's read, kept as the before-state; its "2308 before" was wrong too (2308 preceded my 19:06 systemctl restart; ES was 3303) | guest (`g04-gamelists-after.txt`, `g04-gamelists.txt`, `g04-where.txt`) |
| G-05 | `CANNOT` (no fault seam); 3.13 at stage C | -- |
| G-06 | `ScreenSaverTime` 60000 with `dim`: dimmed at 70 s (`g06-1`), the same screen awake after `shift` (`g06-2`); with `black`: a black frame (`g06-3`); 0 crash lines in essway over the boot | guest (`g06-dim.txt`, `g06b-g08-seed.txt`) |
| G-07 | `CANNOT` (no NIC) | -- |
| G-08 | the editor reached by the list's VIEW OPTIONS > OPTIONS > VIEW PAD TO KEYBOARD INFORMATION (`GuiGamelistOptions.cpp:257`; GAME OPTIONS offers no PADTOKEY row for this game); a seeded `Alpha.gb.keys` with one mapping on `up` and one on `t33unknown`: **the editor shows `T33 KNOWN` alone, and nothing says a mapping was dropped (L-28's positive)**. Seeded over serial rather than set in the editor, inside the bound; the file's shape is `load`'s at `:236-292` | guest (`g06b-g08-seed.txt`, `g08-4-editor`) |
| G-09 | `CANNOT` (no account) | -- |
| G-10 | journal: 0 crash lines; the disk `t33.qcow2` 2,309,619,712 bytes, sha256 `1409b81a…6ca9ca4`, removed; qemu 0, compilers 0 | guest (`retired.txt`, `g10-journal.txt`) |

**Also seen on the way:** VIEW OPTIONS > NAVIGATION > OTHER FILTERS on the gb list (`g08-2`), the path the proposed map text for FILTER GAMELIST BY names.

## The streams

Written by the coordinator after stage D, as for T21, T26 and T32. The lane leaves this heading and the pause's dispositions.

## Positives

- **The fork's helpers are pure where it matters.** Seven units with built cases (CloudFolderValidation 4, CheevosRetry 7, OfflineAchievementsText 15, CheevosIndex 6, WifiText 19, CaptureRotationText 8, DisplayAspectText 3; brief § 5's counts; the total is stage C's `TOTAL:` line) are string-in/string-out and fail closed (`CloudFolderValidation`'s `document()` refuses empty, oversized, NUL and an unknown schema).
- **CaptureRotation reads its four mutable inputs uncached and trusts its record only with `from=checked-launch`** (`:124`): a cut or foreign record reads as untrusted, the benign direction.
- **`AppWindow::post`'s two locks are taken in one order everywhere** (brief § 2, confirmed): the gate, then `Window::mNotificationMessagesLock`.
- **CloudOffer's dialogs put the safe choice last**, where back lands (NOT NOW), and its script carries its own bound (`timeout 90`).
- **Every msgid the 77 carry has French at the pin** (196 of 196). The three that FileTag never passes through `_()` are L-25, the exception that check cannot see.
- **No merge debt:** the 46 upstream-carried files are `rocknix/master`'s bytes.

## The #585 lines owed

Per D-WORKFLOW-164, each upstream-side lead is weighed for upstream. None is sent (D-WORKFLOW-165), and each is rechecked against upstream's head when it is ready. At stage D these are the candidates, by lead; the punch items are numbered in `05`, and stage F fills the commit. "Present at" `rocknix/master` means the 46 upstream-carried files are byte-identical to it at the pin (§ The merge debt). `batocera/master` was not read.

| Upstream | File | The change (proposed) | Evidence | Present at |
| --- | --- | --- | --- | --- |
| batocera-emulationstation, then ROCKNIX | `Gamelist.cpp` `updateGamelist`, `packGamelist`, `cleanupGamelist`; `SystemData.cpp` `getGamelistPath` | L-05: the read of `gamelist.xml` uncached; the write temp-and-rename | `stage-c/l313-update-gamelist.py`; G-04 | `rocknix/master` |
| batocera-emulationstation, then ROCKNIX | `CollectionSystemManager.cpp` `reloadCollection` | L-06: the bundle view's cursor read before the collection is cleared, the view remade from the path | `stage-c/l06-reload-collection.py` | `rocknix/master` |
| batocera-emulationstation, then ROCKNIX | `components/ScraperSearchComponent.cpp` `ScraperAsyncRequestsBuilder` | L-07: a destructor that joins and deletes the thread; `mFinished` atomic | `stage-c/l07-search-builder.py` | `rocknix/master` |
| batocera-emulationstation, then ROCKNIX | `CollectionSystemManager.cpp:345`, `FileFilterIndex.cpp:1313` | L-23: the collections' files written temp-and-rename | `t33-writes.py` | `rocknix/master` |
| batocera-emulationstation, then ROCKNIX | `FileTag.cpp` | L-25: three tag names through `_()` | `stage-c/l329-filetag-words.py` | `rocknix/master` |
| batocera-emulationstation, then ROCKNIX | `LangParser.cpp:65` | L-26: the token `india` | `stage-c/l331-lang-india.py` | `rocknix/master` |
| batocera-emulationstation, then ROCKNIX (if the pause takes them) | `FileFilterIndex.cpp` rating and year; `KeyboardMapping.cpp` `load` | L-27, L-28: the rule as the cases state it; a log line for a dropped mapping; shape before `GetString` | `stage-c/l309-rating-year.py`, `stage-c/l321-keys-parse.py`; G-08 | `rocknix/master` |
| ROCKNIX's es-core, then batocera (if the pause takes it) | `es-core/src/watchers/WatchersManager.cpp` | L-01: `check()` outside `mWatchersLock` | the read trace | `rocknix/master` (T21's file) |
| recorded only, outside the lanes | `ZaparooSupport.cpp`, `ContentInstaller.cpp`, `ThreadedBluetooth.cpp`, `SystemScreenSaver.cpp` | L-09, L-10, L-11: bounds, thread ownership, uncached reads | `t33-bounds.py`, `t33-reads.py` | `rocknix/master` |

Q7's six candidates, for the coordinator to weigh. These are what the slice carries that upstream lacks:
1. **`maskSecrets` on the logged command line** (`80f52e500`). It needs `StringUtil`'s `maskSecrets`, which is in 0 files at `rocknix/master`.
2. **The bounded token-check retry at link-up** (`d9d6083de`, `461e14305`, `42f9e8851`). It needs `testAccount(..., bool* refused)` at `RetroAchievements.h:282`.
3. **The startup index re-run at link-up** (`cce9ab12a`). It needs `ThreadedHasher::cheevosLibraryCameThisSession` and `SystemData::startIndexesAtStart`, both absent at master.
4. **`FolderMerge.h`.** Its consumer is in an earlier slice (`SystemData.cpp:486`).
5. **`CheevosIndex.*`.** Its consumer is `ThreadedHasher.cpp`.
6. **`GameCubeRvzHashRetry.h`.** Its consumer is `ThreadedHasher.cpp:44`; #609 is open against it.

## What T34 to T37 inherit

Brief § 5 item 3's eight items, written here and not tested here:
1. **The provenance table:** § Coverage, 27 / 4 / 46 against `bccd715707` and `cada856d86`, which agree.
2. **The cached-read table with its writers:** § The reads, 83 rows, and its third shape (ES's own non-`Utils::FileSystem` writers).
3. **The write table:** § The writes, nine compiled lines in place, one dead text and one dead Win32.
4. **The thread-and-lifetime table:** § The library's thread column, § The bounds, and L-06, L-07, L-10, L-12, L-15 and L-24 (stage C adds the harnesses).
5. **The bounds table:** § The bounds.
6. **The `app-unit-tests` build recipe:** the five case files, their nine fakes under `tests/app-unit/fakes/`, and the pugixml root `/workspace/cache/rocknix-sources/emulationstation/emulationstation-<PIN>/external`, in `tools/t33-build-tests.sh` at stage C.
7. **The map's two filter rows and UPDATE GAMELISTS as proposed text:** § The structure.
8. **The Windows residue's dispositions:** § The structure.
