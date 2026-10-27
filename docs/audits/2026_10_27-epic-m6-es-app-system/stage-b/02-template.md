# Forward audit — M6.P2 T33, EmulationStation's system layer (#680)

Composed by `tools/t33-02.py` from this template and the generators under `tools/`. Each generated section ends with its generator's own "generated, asserted" line, and each generator was seen to exit 1 on a constructed drift before it was trusted (`stage-b/generators.txt`). The ES worktree is read at the pin `16dbac5211` by `git -C` only. The distribution was reviewed at `27bd8499f1`. Depth: Independent, one seat (GPT-6 Astra at `max`), at stage C.

Every proof carries `proved:` in #680's vocabulary: `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`. A `fixture` is a stage-C harness that extracts the pin's code as written and is seen to FAIL at the pin and PASS under its `--control` (`stage-c/runs.txt`). The brief is `docs/reviews/briefs/es-app-system.md` at `c48f8b387e`; its § numbers are cited as "brief § N".

## Coverage

The 77 paths, one row each. The read tier is from `git diff` against the fork's base `bccd715707`: added, modified, or neither. The inventory tier is fork-own for the first two and upstream-carried for the third. The fork's numstat is against `bccd715707`, which equals the merge base `cada856d86`'s and `rocknix/master`'s for every row (`stage-a/runs.out`: the three shortstats are equal).

{{COVERAGE}}

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

The brief's 41 rows (brief § 4), word for word, with their proof. The 35 non-fixture rows were read by a read-only subagent and five re-read by the first reader (`stage-c/floor.md`, labelled). The six that FAIL at the pin are in bold: 3.9, 3.13, 3.21, 3.29, 3.31 and 3.35. Each is seen to FAIL against the unfixed extract before it is trusted, at stage C. Offsets written `+N` are read to absolute lines when a case cites them.

| # | At the pin | Function | What a case would catch | proved: |
| --- | --- | --- | --- | --- |
| 3.1 | `PlatformId.cpp:215` (`:220`), `:227` (`:233`), `:237` | `getPlatformId`, `getPlatformName`, the `ArcadeSystems` map | `getPlatformId(nullptr)`; a duplicated table string shadowing an id; an enum value with no row reading `"unknown"`; short names not lowercase | tree (`stage-c/floor.md`: PRESENT [re-read]) |
| 3.2 | `MetaData.cpp:28` (`:30-66`), `:42-43`/`:46-47` | `initMetadata`'s `gameDecls` | a key typed twice with two types; `Emulator`/`Core` twice by design, the case pins which wins | tree (`stage-c/floor.md`: ABSENT) |
| 3.3 | `MetaData.cpp:280` (`+153`, `+158-161`, `+167-169`, `+199-201`) | `appendToXML` | a player-set value equal to its default dropped under `ignoreDefaults`; an `MD_PATH` written absolute when relative was asked | tree (`stage-c/floor.md`: PRESENT) |
| 3.4 | `MetaData.cpp:357`, `:407`, `:435`, `:451`, `:454`, `:459` | `set`, `get`, `exists`, `getInt`, `getFloat`, `wasChanged` | `getInt` on `""`; a non-numeric `playcount`; `set` of the same value flipping `wasChanged` | tree (`stage-c/floor.md`: PRESENT) |
| 3.5 | `MetaData.cpp:469` | `importScrappedMetadata` | a scrape wiping a player's favourite flag; an empty scraped field blanking a filled one | tree (`stage-c/floor.md`: PRESENT [re-read]) |
| 3.6 | `MetaData.cpp:270` (`+124`) | `migrate` (`FileData*` on the signature: the lane finds the seam) | an old `<hash>` lost on first load (`upgrade-and-install.md:95`: read both) | tree (`stage-c/floor.md`: ABSENT) |
| 3.7 | `MetaData.cpp:151` (`+20-28`, `+66-70`) | `loadFromXML`'s default-and-lowercase rule and the `<scrap>` reading, lifted | a `"TRUE"` another tool wrote not read as true | tree (`stage-c/floor.md`: ABSENT) |
| 3.8 | `Genres.cpp:185`, `:234`, `:257`, `:293`, `:323` (`init` `:19`) | the genre lookups, over a seam that takes a document | a game counted twice in the genre filter (parent and child); a trailing comma | tree (`stage-c/floor.md`: PRESENT [re-read]) |
| **3.9** | `FileFilterIndex.cpp:247` (**`:322-341`, `:364-369`**), `:362` | the rating, year and played predicates, lifted into string-in/string-out helpers | **`ratingKey("0.05")` reads `0 STARS` where `""` and `"0"` read UNKNOWN (`:333`, `:339`); `yearKey("3000")` and `yearKey("999")` read `""` (`:367`)** (L-27) | **fixture** (`stage-c/l309-rating-year.py`: FAIL at the pin, control PASS) |
| 3.10 | `FileFilterIndex.cpp:557` | `jw_distance` (file-static Jaro-Winkler) | identical -> 1.0; empty vs non-empty -> 0; symmetric; a distance above 1 or NaN on an empty string | tree (`stage-c/floor.md`: ABSENT (aside PRESENT [re-read])) |
| 3.11 | `FileFilterIndex.cpp:1107-1321` (`+11`, `+37-39`, `+99-161`) | `CollectionFilter::load`/`save` on a temp `.xcc` (file) | a tag `save` writes that `load` ignores: a filter forgetting one of its rows on restart | tree (`stage-c/floor.md`: ABSENT) |
| 3.12 | `Gamelist.cpp:255`, `:288` (`:261`, `+274`, `+283`) | `addFileDataNode`, `saveToXml` (needs `FileData*`/`SystemData*` doubles, `tests/app-unit/fakes/FileData.h`) | a `<path>` written absolute into a per-system gamelist | tree (`stage-c/floor.md`: ABSENT) |
| **3.13** | `Gamelist.cpp:374` (**`:413`, `:466-477`**; `:308`, `:622`, `:841`) | `updateGamelist`'s shape | **the in-place `doc.save_file` with no temp-and-rename (D-CLOUD-078) and the cached `exists` before it** (L-05); the shape in a file case, the atomicity `CANNOT` without a fault seam (G-05) | **fixture** (`stage-c/l313-update-gamelist.py`: FAIL at the pin, control PASS) |
| 3.14 | `Gamelist.cpp:112` (`+35-38`, `+47`, `+61-63`, `+66`, `+79-83`) | `loadGamelistFile` through its `!fromFile` branch (a string) | a `<path>` with a trailing newline or `\` never matched; the size-mismatch warning | tree (`stage-c/floor.md`: PRESENT) |
| 3.15 | `Gamelist.cpp:518`, `:631`, `:483` (`+601`, `+705`, `+732-748`) | `packGamelist`, `cleanupGamelist` (file or guest) | `cleanupGamelist` dropping a media reference that exists on disk through the cache | tree (`stage-c/floor.md`: PRESENT) |
| 3.16 | `CollectionSystemManager.cpp:1508`, `:1513`, `:1518`, `:1523`, `:1532` | the collection paths | a name containing `/` or `..` writing outside the collections folder | tree (`stage-c/floor.md`: PRESENT) |
| 3.17 | `CollectionSystemManager.cpp:598` (`:627`, `:646`, `:651`; `themeFolderExists` `:1492`) | `getValidNewCollectionName` over a seam for `sSystemVector` | an auto-collection name (`"all"`) or a theme folder accepted | tree (`stage-c/floor.md`: PRESENT) |
| 3.18 | `CollectionSystemManager.cpp:1434` (`+1450`) | `getCollectionsFromConfigFolder` over a handed listing | `custom-.cfg` or `custom-a.cfg.bak` read as a collection | tree (`stage-c/floor.md`: ABSENT) |
| 3.19 | `CollectionSystemManager.cpp:34` (`:40`) | `getSystemDecls` | names or theme folders not unique; `recent`'s sort | tree (`stage-c/floor.md`: ABSENT) |
| 3.20 | `CollectionSystemManager.cpp:540` | the `.at()` on a set value (T2 FD-15, #771) | an index outside the 28 sort types | tree (`stage-c/floor.md`: ABSENT (sibling PRESENT [re-read], outside the slice)) |
| **3.21** | `KeyboardMapping.cpp:217` (**`:265`, `:271`, `:282`, `:288`**; `checkTriggerExists` `:178`) | `KeyMappingFile::load`'s parse, split out as `parse(json)` | **a trigger naming an unknown key dropped silently: a mapping loads as an action with no trigger** (L-28); a parse error -> what `isValid` `:499` says | **fixture** (`stage-c/l321-keys-parse.py`: FAIL at the pin, control PASS) |
| 3.22 | `KeyboardMapping.cpp:328`, `:432`, `:512`, `:535`, `:586`, `:726`, `:776`, `:793` | `save`, `fromP2k`, `triggerEquals`, `toTargetString`, `updateMapping`, `removeMapping`, the descriptions | a description with a quote breaking a JSON written by hand (read `:328-431` first); `save -> load` round trip | tree (`stage-c/floor.md`: ABSENT) |
| 3.23 | `KeyboardMapping.cpp:178`, `:190`, `:199`, `:208` (the tables `:163-176`) | `checkTriggerExists`, `checkTargetExists`, `getTriggerFromP2k`, `getTargetFromP2k` | a key whose name has two `_` taking the wrong tail | tree (`stage-c/floor.md`: ABSENT) |
| 3.24 | `CustomFeatures.cpp:23` (`:13-21`) | `parseFeatures` | a feature name with a trailing space never enabling its row | tree (`stage-c/floor.md`: ABSENT) |
| 3.25 | `CustomFeatures.cpp:406`, `:61`, `:93`, `:155` (`:202-207`, `:224-227`, `:242-251`, `:256`, `:292-298`) | `loadCustomFeatures` over an XML string | a feature declared on the core not reaching the menu when the emulator declares none | tree (`stage-c/floor.md`: ABSENT) |
| 3.26 | `CustomFeatures.cpp:529`, `:534`, `:523` | `hasFeature`, `hasGlobalFeature`, `sort` | a case mismatch between `es_features.cfg` and the launcher | tree (`stage-c/floor.md`: PRESENT) |
| 3.27 | `FileSorts.cpp:93` (`:96`, `:99`, `:106`; `:83`) | `stripLeadingArticle` | an article matched by prefix; a title that is only an article emptied; `_("A,AN,THE")` translated | tree (`stage-c/floor.md`: ABSENT) |
| 3.28 | `FileSorts.cpp:32` (`:43-71`) | `getSortType` and the 28-row table | an id twice; a pair not sharing its comparator; `getSortType(-1)` falling to the first row | tree (`stage-c/floor.md`: PRESENT) |
| **3.29** | `FileTag.cpp:30` (**`:6-11` against `:16-18`**) | `getDisplayIcons` | **three of nine names outside `_()` and absent from the catalog** (L-25); `"finished"` -> 0 (exact case) | **fixture** (`stage-c/l329-filetag-words.py`: FAIL at the pin, control PASS) |
| 3.30 | `LibretroRatio.cpp:51` (`:12-43`) | `getRatio()` | keys not unique; a value RetroArch does not accept | tree (`stage-c/floor.md`: ABSENT) |
| **3.31** | `LangParser.cpp:33` (**`:65`**; `:37-64`) | `extractLang` | **`"ìndia"` unreachable: only `"in"` matches** (L-26); `"(USA, Europe)"` -> en + us,eu | **fixture** (`stage-c/l331-lang-india.py`: FAIL at the pin, control PASS) |
| 3.32 | `LangParser.cpp:144`, `:203`, `:18` | `parse`, `getFlag`, `getLanguageString` | a region with no flag asset drawing a broken image | tree (`stage-c/floor.md`: PRESENT) |
| 3.33 | `CaptureRotation.cpp` (§ 2's row) **(fork-own)** | the one cached read beside four uncached | a rotation table written after ES started reading as absent (by design: the lane records the comment `:23-30`) | tree (`stage-c/floor.md`: NO-DEFECT-CLAIM) |
| 3.34 | `SystemRandomPlaylist.cpp` (§ 2's row) | `getNextItem` over a seam for the RNG | a path that starts existing mid-session never seen | tree (`stage-c/floor.md`: PRESENT) |
| **3.35** | `TextFit.h` (§ 2's row) **(fork-own)** | `fitOneLine` with a fake measure (1 px per char), `popCharacter` | **a 4-byte name over the width never gets its ellipsis; a two-character CJK name stops at one** (L-20); a label cut inside a UTF-8 sequence | **fixture** (`stage-c/l335-textfit-floor.py`: FAIL at the pin, control PASS) |
| 3.36 | `JourneyTiers.h` (§ 2's row) **(fork-own)** | `record`, `parse`, `replaceRecord`, `command` (`JourneyTiersTests.cpp`'s 8 cases first) | a two-byte record read as empty; a `Write` that fails -> `OldRecordStands`; the literals' exact shape | tree (`stage-c/floor.md`: ABSENT) |
| 3.37 | `FolderMerge.h` (§ 2's row) **(fork-own)** | `merge(live, fresh, tree)` (`FolderMergeTests.cpp`'s 3 cases first) | a live node dropped when the fresh tree holds it under a different case; a renamed folder | tree (`stage-c/floor.md`: PRESENT) |
| 3.38 | `RunLock.h` (§ 2's row) **(fork-own)** | `held`, `holder` (`RunLockTests.cpp`'s 3 cases first; file) | a stale lock file read as held; the substring match (L-14) | tree (`stage-c/floor.md`: PRESENT) |
| 3.39 | `GameCubeRvzHashRetry.h` (§ 2's row) **(fork-own)** | `trim`, `needed` | a valid unknown hash retried; whitespace only | tree (`stage-c/floor.md`: ABSENT) |
| 3.40 | `AppWindow.h` (§ 2's row) **(fork-own)** | `gate`, `open`, `post`, `closing` (`AppWindowTests.cpp`'s 1 case first) | a task posted after `closing()` running; a task posted before running twice | tree (`stage-c/floor.md`: ABSENT) |
| 3.41 | `OfflineAchievementsText.cpp` (§ 2's row) **(fork-own)** | `jsonInt`, `parsePendingIds` | the `int` truncation (L-17) | tree (`stage-c/floor.md`: PRESENT) |

## The library

One row per unit of the game lists, collections, metadata and filters. The facts are read at the cited lines, and the generator checks that each cited caller line holds the call it names. Three things stand out:
- **The first frame waits for the whole library:** every system's `gamelist.xml` parse, the filter index, the collections' load and es_features.cfg, under the splash. None of the slice's own reads is on the network.
- **Two writers are on the player's data:** `gamelist.xml` (game content, synced) and the collections' files (settings, archived). Both write in place (§ The writes).
- **One reader can lose data:** `Gamelist.cpp:413`'s cached read is the one that can drop a restored `gamelist.xml` (L-05).

{{LIBRARY}}

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

{{HELPERS}}

## The writes

§ 5's grep, line for line. Nine lines compile. The brief's "ten live sites" counts `CustomFeatures.cpp:151`, which is text inside a `/* */` block. `Win32ApiSystem.cpp:979` is dead inside `#if WIN32`.

None of the nine is temp-and-rename. `Gamelist.cpp:622` and `:841` keep a `.old` copy that nothing reads back. Every in-place writer is measured against two references:
- JourneyTiers' writer (`guis/GuiMenu.cpp:5066`, `AtomicFile::writeText`);
- es-core's `AtomicFileUtil`, which `es-file-tests` covers.

D-CLOUD-078 asks every writer for temp-and-rename. `Already written:` is answered per row (D-WORKFLOW-050).

{{WRITES}}

## The reads

One row per `Utils::FileSystem::exists(` line: 83 lines and 86 calls. Four calls are uncached, all in `CaptureRotation.cpp` (`:113`, `:146`, `:161`, `:170`). The 46 upstream-carried files have none.

The cache's rule is T21's file, cited from T32's Q4 and not re-read:
- ES's own writes through `Utils::FileSystem` drop their path from the cache.
- A file written outside the process is not seen until a launch resets the cache (`FileSystemUtil.cpp:345`). Examples are the cloud's game-content restore (D-CLOUD-049) and the player over SSH.
- A third shape this slice adds: ES's own writes that do not go through `Utils::FileSystem`. These are `std::ofstream` (`CollectionSystemManager.cpp:345`) and `pugi::save_file` (`FileFilterIndex.cpp:1313`, `Gamelist.cpp:474`, `:622`, `:841`), and their paths are not dropped either. The key maps are not among them: they write through `writeAllText` (EP-21).

The four the brief names, with their dispositions:
- **`Gamelist.cpp:413` (L-05):** the reader that can lose a player's data. The next save starts from an empty `<gameList>` and writes over the restored file.
- **`SystemScreenSaver.cpp:157` and `:164` (L-11):** recorded, outside the lanes. Each retry picks a new candidate, but a candidate whose miss is cached never becomes visible (EP-17).
- **`CaptureRotation.cpp:51`:** left cached on purpose, because it reads the image's read-only tree. The four uncached reads are not full freshness: `sKnownAt`, keyed by mtime alone, answers first (`:103-108`, EP-41).

{{READS}}

## The bounds

The table covers every network or script wait reachable from the 77, in three kinds: an HttpReq construction, a process start (§ 5's grep), and a wait the grep cannot see (L-01, L-02, L-09).

The brief's § 5 "HttpReq lines" (`OfflineAchievementsText.h:1`, `ScraperCmdLine.cpp:1`, `Win32ApiSystem.cpp:3`, `ZaparooSupport.cpp:5`) count every line naming HttpReq. The constructions among them are four: two live, both Zaparoo's, and two dead. The one option line is `ZaparooSupport.cpp:38`, a `connectTimeout`.

The table is not exhaustive (EP-18). It rows direct constructions, process starts and named waits. The transitive calls through `ApiSystem` (`ContentInstaller.cpp:132-135`, `:206-209`; `ThreadedBluetooth.cpp:41-44`, `:102-105`) and the search component's fallback searches (`ScraperSearchComponent.cpp:652`, `:658`) are named here and not bounded by this read. The slice's own code sets no total or stall bound anywhere. The one bounded process is `CloudOffer.cpp:37`'s `timeout 90` (L-18: the bound is sound). The launcher's truncation of `exec.log` is not a size bound (EP-14). The unbounded live waits are:
- L-01: es-core's lock reached from the interface thread;
- L-09: Zaparoo's probe, its card and its lock, outside the lanes;
- `retroarch.cfg`'s read after every exit (L-02).

{{BOUNDS}}

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

{{WORDS}}

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

- Under **`## What lives where`**, the GAME SETTINGS row's TOOLS group gains its first row:
  > `UPDATE GAMELISTS` -- GAME SETTINGS > TOOLS (`guis/GuiMenu.cpp:5756`; seen on the guest, G-03). It asks REALLY UPDATE GAMELISTS?, then reloads the game lists. While a scrape or the hasher runs, it asks to stop that instead and returns (`GuiMenu.cpp:8501-8517`). The second entry, in GAME COLLECTION SETTINGS > OPTIONS (`guis/GuiCollectionSystemsOptions.cpp:366-369`), is inside `#if defined(WIN32) && !defined(_DEBUG)` and never on a handheld (EP-25; the stage-B draft gave it two homes). The index toast (`ThreadedHasher.cpp:146`) is not promised: the guest did not show it.
- A new short section, **`## Game list filters`**, after `## What lives where`:
  > **FILTER GAMELIST BY** -- a page of its own (`guis/GuiGamelistFilter.cpp:11`), opened from a game list's VIEW OPTIONS > NAVIGATION > OTHER FILTERS (`guis/GuiGamelistOptions.cpp:77-79`, `:435`). Each row is a facet of the system's `FileFilterIndex`; BACK applies the choice to the in-memory index (`applyFilters`, `:39`, `:226-263`). The page saves nothing for an ordinary filter (EP-26); whether another component persists it is not established.
  >
  > **EDIT DYNAMIC COLLECTION FILTERS** -- the same page over a dynamic collection's index (`guis/GuiGamelistFilter.cpp:17`). It is opened from that collection's VIEW OPTIONS > DYNAMIC COLLECTION (`guis/GuiGamelistOptions.cpp:174-176`, `:603`) and from GAME COLLECTION SETTINGS when a dynamic collection is made (`guis/GuiCollectionSystemsOptions.cpp:495`). Its choices are written to the collection's `.xcc` in place (`FileFilterIndex.cpp:1313`, L-23), and the page closes as saved whatever `save()` returned (`GuiGamelistFilter.cpp:262-270`, EP-43); creating one reloads the collection on finalize (`GuiCollectionSystemsOptions.cpp:495-504`).
- The check's half is named for the coordinator: a fourth pattern, `\bmMenu\s*\(\s*\w+\s*,\s*_\("([^"]+)"\)`, would let `tools/es-menu-map-check` see both titles. It may find other pages too, so its census is rerun with it (EP-26). That is a change under `tools/`, which this lane does not make.

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
| the bounds | 4 http, 6 process, 4 waits; 1 bounded, 7 dead (EP-14: the log read is not bounded) | a wait the table does not name | `tools/t33-bounds.py` |
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

- **The fork's helpers are mostly pure.** Seven units with built cases (CloudFolderValidation 4, CheevosRetry 7, OfflineAchievementsText 15, CheevosIndex 6, WifiText 19, CaptureRotationText 8, DisplayAspectText 3; brief § 5's counts; the total is stage C's `TOTAL:` line) are string-in/string-out, and `CloudFolderValidation`'s `document()` fails closed (it refuses empty, oversized, NUL and an unknown schema). `OfflineAchievementsText`'s `parseUnlocks` does not: a missing `Success` or a list of invalid entries reads `ok` (EP-42).
- **CaptureRotation trusts its record only with `from=checked-launch`** (`:124`): a cut or foreign record reads as untrusted, the benign direction. (Narrowed by EP-40 and EP-41: the running process caches by mtime after an unchecked write.)
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
