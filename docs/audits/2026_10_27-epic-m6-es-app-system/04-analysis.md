# Analysis — M6.P2 T33, EmulationStation's system layer (#680)

## Executive summary

- **What was read:** 77 paths of `es-app` at the pin `16dbac5211`: the game lists, collections, metadata and filters (46 upstream-carried, byte-identical to ROCKNIX's master); the fork's 17 helper units (27 files); and NetworkThread and the CMake list (4 fork-modified).
- **Proofs:**
  - Nine host fixtures, each extracting the pin's code as written, FAIL at the pin and PASS under the proposed fix (`stage-c/runs.txt`).
  - The unit build ran every target, `tests/app-unit`'s five case files for the first time (`TOTAL: 239 test cases in 5 binaries`, 0 failed).
  - One guest window reproduced L-05 and L-28 on the image (`02` § The guest cycle).
- **The highest finding is L-05,** in the lanes (D-CLOUD-049). A `gamelist.xml` restored from the cloud while ES runs is overwritten at the next save by the changed entries alone, because the read before the write is a cached miss (`SystemData.cpp:1653`, then `Gamelist.cpp:413`) and the write is in place (`:474`). Proved on the host (3.13) and on the image (G-04, with a control).
- **Two use-after-frees, proved under ASan:**
  - L-06: a dynamic collection's reload frees what the bundle view's cursor points at.
  - L-07: the scrape search's builder thread outlives its builder.
- **Fork rules the fork's own code misses:**
  - NetworkThread bypasses `AppWindow`'s closing gate (L-12).
  - TextFit's floor counts bytes (L-20).
  - None of the nine compiled writers is temp-and-rename (D-CLOUD-078).
- **Words:** three FileTag names a player reads have no French (L-25). One token is unreachable (L-26).
- **No merge debt.**

## Acceptance-criteria scorecard

#680's body, at the end of stage C (before the seat's grades are applied):

| # | Checkbox (short) | State | Evidence |
| --- | --- | --- | --- |
| 1 | folder layout | partial | `00` to `04` and `stage-a`/`b`/`c`/`guest-cycle`/`tools` present; `05`, `second-opinions/` and `stage-d`/`e` come at stage D and E |
| 2 | lint PASS | open | pre-issue lint at stage C's end; resolution at close |
| 3 | review plan and provenance | open | the two keyed calls at stage C's end |
| 4 | Phase 7 outcomes | open | stage F |
| 5 | header commits | open | `reviewed-at` set; `fixed-at` at stage E |
| 6 | `01` § Scope | met | `01-research-notes.md` § Scope |
| 7 | coverage table | met | `02` § Coverage, 77 rows, asserted |
| 8 | the runs' counts | met | `02` § The runs, `stage-a/runs.out` |
| 9 | generated tables | met | six generators and the composer, drift-tested (`stage-b/generators.txt`) |
| 10 | the reads, 83 rows | met | `02` § The reads; the four named rows carry dispositions |
| 11 | the writes, 11 rows | met | `02` § The writes, with `Already written:` per row |
| 12 | the merge debt line | met | `02` § The merge debt |
| 13 | every § 5 command recorded | partial | `stage-a/runs.out` holds every command; wall time per command is not recorded (the block captured none, as brief § 5 says), so the table in `02` § The runs cites the files |
| 14 | the guest cycle | partial | G-01 to G-10 recorded; **not done:** frames in FR (the window ran EN only); G-03's index toast (INDEX NEW GAMES off) |
| 15 | no build, no fetch, no handheld, no owner account | met | `00` |
| 16 | `04` § Q1-Q7; bugs' traces | partial | this file; the bugs' traces at stage D |
| 17 | every proof's `proved:`, every item's `question:` | partial | `02`'s leads carry the vocabulary; `question:` in `05` |
| 18 | the retro | open | stage F |
| 19 | the map's proposed text | met | `02` § The structure (and the check's blindness, #951/#965's class) |
| 20 | the five gates on the branch | open | at hand-back |
| 21 | the `TOTAL:` line, 0 failed after the fixes | partial | at the pin: `TOTAL: 239 test cases in 5 binaries`; after the fixes at stage E |

## Risk assessment

| Risk | Where | Who meets it | Severity |
| --- | --- | --- | --- |
| A restored `gamelist.xml` loses its entries | L-05 | every player who restores game content from the cloud while ES runs, then plays or edits a game | **high** (data loss, in the lanes) |
| A dynamic collection's filter edit crashes ES | L-06 | a player who edits a dynamic collection's filters from the bundle with the cursor on one of its games | **high** (a crash; #246's shape) |
| A stopped scrape search writes into freed memory | L-07 | a player who backs out of a single-game scrape while its token or hash is being built | medium (a crash or heap corruption; scraping, outside the lanes) |
| Collections' files cut by a power loss | L-23 | settings tier, archived by the backup tool | medium |
| A refused trigger dropped silently; wild reads on a malformed `.keys` | L-28 | a player who edits a key map by hand | low (outside the lanes) |
| Tag names in English under French | L-25 | French players filtering by tag | low |
| A post lost at shutdown | L-12 | a token write racing the exit | low |
| An interface-thread wait on the watcher lock | L-01 | a page close during a network check | medium (a freeze bounded by the check) |

## Coverage boundary

- **Read whole:** the 27 fork-added files and NetworkThread. The upstream-carried files are read at the lines the leads, the floor and the generators cite. The floor's 35 non-harness rows were read by a read-only subagent (`stage-c/floor.md`, labelled), whose PRESENT verdicts the first reader re-read before carrying any into `05`.
- **Run:** the unit build (all targets), nine fixtures, and the guest window (EN).
- **Not run:** FR frames; the index toast; a launch, so L-02's `stat`; the content installer and NetworkThread's checks (no NIC, no account); the screensaver's video and slideshow modes; a TSan run (L-07's `mFinished`, L-12).
- **Outside the slice, cited:** `SystemData.cpp`, `ViewController.cpp`, `FileData.cpp`, `main.cpp`, es-core's `FileSystemUtil.cpp` and `WatchersManager.cpp` (T21's), and the pages (T31's).

## The questions

### Q1 Lifetimes and threads
- **L-06** (`CollectionSystemManager.cpp:1573-1600`, `:1302`, `:1115-1117`; `ViewController.cpp:1140-1142`): proved, a heap-use-after-free. The fix is es-code-traps.md:191's two halves: read the cursor path before the clear, and remake from it. Upstream-carried, contained (rule 6), with a #585 line.
- **L-07** (`components/ScraperSearchComponent.cpp:196-258`, `:206`, `:231`, `:358-361`): proved. The fix is a destructor that joins and deletes the thread, with `mFinished` atomic.
- **L-12** (`NetworkThread.cpp:206`, `:237`, `:251`, `:257`, `:266`; `main.cpp:1322`, `:1330`): proved by count and by the gate's behaviour. The fix routes the five posts through `AppWindow::post`.
- **L-15** (`FolderMerge.h:38-71` <- `SystemData.cpp:486`): its three cases pass. The holders' list is recorded for the rescan's owner.
- **L-24** (`NetworkThread.cpp:19-25`, `main.cpp:898`): sound for the process's life. Recorded so nobody frees the static.
- **L-10** (`ContentInstaller.cpp`, `ThreadedBluetooth.cpp`): `delete this` on the worker, the thread never joined. Outside the lanes, recorded, with a #585 line.

### Q2 Bounded calls
- **L-01:** the interface thread's `ResetComponent` (`NetworkThread.cpp:24`) takes `mWatchersLock`, which the watcher thread holds across every `check()` (`WatchersManager.cpp:181-196`). A page close waits out a network check. It is es-core's lock (T21's file): rule 6, put to the pause.
- **L-09:** Zaparoo's probe and card set no total or stall bound (`ZaparooSupport.cpp:39`, `:62`), and the lock (`:32`) inherits it. Outside the lanes, recorded.
- **L-18:** `timeout 90` is the bound, and it is sound (`02` § The bounds: 2 bounded of 7 live).
- **L-02:** `retroarch.cfg` (`CaptureRotation.cpp:162`) has no bound but its size, on the interface thread after every exit. The time-to-play line prices it.

### Q3 Reads that read as success
- **L-27** (3.9): `0.05` reads 0 STARS, and `3000…`/`0999…` read "" (`FileFilterIndex.cpp:331-339`, `:367`). Proved. Also, `1 STARS` has no singular.
- **L-28** (3.21): a refused trigger drops the whole mapping with no word (`KeyboardMapping.cpp:262-272`, `:292`). Proved on the host and the image. The loader's other reads (`:247-288`) call `GetString` with no `IsString`, which are wild reads under NDEBUG on a malformed file.
- **L-14:** `holder()`'s substring match (`RunLock.h:66-68`) would name an unrelated process whose argv contains `program`. Its three cases pass, but none covers the substring. A stream's case.
- **L-17:** `(int)v.GetInt64()` (`OfflineAchievementsText.cpp:18`). Harmless today.
- **L-18:** `CloudOffer.cpp:42-45` reads DONE on rc 0 alone. The script's half is the rclone slice's.
- **`MetaData::getInt`** (`:451`, `atoi`): reads 0 unchecked. Recorded.

### Q4 Uncached reads and in-place writes
- **L-05:**
  - **The read:** the first cached miss is `SystemData::getGamelistPath` (`SystemData.cpp:1653`), at the systems' load and again at `Gamelist.cpp:412`. Then `:413` reads the remembered miss.
  - **The write:** in place (`:474`).
  - **Fix:** an uncached read at `:413` and in `getGamelistPath` for the read path, and temp-and-rename at `:474`, `:622` and `:841`.
  - **`Already written:`** a `gamelist.xml` already cut by a past power loss is a parse error, and `:416-424` falls to an empty root. The fix reads both, so nothing is inherited beyond what a reread repairs.
- **L-23 and the third cache shape:** `std::ofstream` (`CollectionSystemManager.cpp:345`) and `pugi::save_file` (`FileFilterIndex.cpp:1313`) bypass the cache's invalidation. `deleteCustomCollection` (`:1610`, `:1613`) can refuse a file written this session.
- **L-03:** Backlog #1186's site.
- **L-13:** covered by `es-conf-tests`.

### Q5 The words, the French and the help bars
- **L-25** (3.29): IN PROGRESS, DROPPED and ON HOLD have no `_()` and no msgid (`FileTag.cpp:6-11` against `:16-18`). Proved. Proposed French, built as proposed (D-UI-112): EN COURS, ABANDONNÉ, EN PAUSE.
- **L-26** (3.31): `ìndia` (`LangParser.cpp:65`). Proved.
- **The upstream boxes:** `ScraperSearchComponent.cpp:386` (English, `toUpper`, a bare `"FINISH"`) and `:468`, and the installer's toasts (L-10). Outside the lanes, recorded.
- **The one help bar** (`ScraperSearchComponent.cpp:738-744`): sound.

### Q6 The views and their cost
- **L-04:** the first SCREENSHOTS look after a library change walks the library under `sShotLock`. On the guest it opened 0.1 s after the press over 100 captures and four games, which is not a price.
- **L-11 and `SystemRandomPlaylist`:** cached reads; outside the lanes, recorded.
- **The screensaver's launch** (`SystemScreenSaver.cpp:546`): it skips `ViewController::launch`'s format warning (`:497`) and BIOS check (`:507`), and keeps the cloud gate (`FileData.cpp:993`). Recorded (take-up row T2 `:293-294`).

### Q7 The structure, the map and the merge debt
- **The map:** the proposed text for FILTER GAMELIST BY, EDIT DYNAMIC COLLECTION FILTERS and UPDATE GAMELISTS is in `02` § The structure. The check's blindness to member-initializer titles is named with its fourth pattern. UPDATE GAMELISTS has two homes (GAME SETTINGS > TOOLS; GAME COLLECTION SETTINGS > OPTIONS), both seen on the guest for the first.
- **The residue:** L-21 and L-22, one row each.
- **The merge debt:** none.
- **Collisions:** T21's ten `CMakeLists.txt` lines and its `WifiText` delta, and T20's `OfflineAchievementsText` delta. A stream that edits these files names them.

## The take-up table (brief § 2), each row disposed

| Row | Disposition |
| --- | --- |
| T2 FD-9/FD-19 `Scripting.cpp` | inherited, the es-core slice's (§ 1 a) |
| T2 FD-15 / #771 `CollectionSystemManager.cpp:540` | the floor's 3.20; verdict in `stage-c/floor.md`, carried to `05` |
| T2 SD-1 / #781 | T2's file; `FolderMerge.h`'s cases pass (L-15) |
| T2 PC-1 detached card workers | a T35/T18 lead, inherited (§ 1 d) |
| T2 exit callees `FileData.cpp:1166-1167`, `:1207`, `:1208` | L-02; the retro's time-to-play line |
| T2's brief `:293-294` screensaver launch | graded: skips `:497`, `:507`; keeps `FileData.cpp:993` (Q6) |
| T31 PL-26 / T32 L-14 `DisplayAspect.cpp:74-87` | L-04 (Q6) |
| T32 L-16 `CollectionSystemManager.cpp:1558-1600` | L-06, proved (Q1) |
| T21 PL-20 / #1186 | L-03, `KeyboardMapping.cpp:426`, `:429`: deferred to #1186 |
| T31 PL-25 / #1235 | L-22: the Backlog's |
| T32 errata 23 | recorded, not re-grepped |
| T20 PL-01 / #1170, PL-07 / #301 | the callers' side: `NetworkThread.cpp:248`, `:251` post the hasher's start to the interface thread (L-12's sites); the hasher's side is T20's |
| T20 PL-06 / #1175 | `CheevosRetry.*` unchanged, 7 cases pass |
| T20 PL-04, PL-05 | read at both refs, inherited, no second fix |
| T20 `02:167` `GameCubeRvzHashRetry.h` vs #609 | the floor's 3.39; the ruling at the pause |
| T20 S9 TextFit | L-20, proved |
| T21 PL-06 / #1194, PL-16 / #1204 `WifiText` | read at both refs, inherited |
| T21 `Win32ApiSystem.cpp` (D-WORKFLOW-209) | L-21 |
| T21 PL-15 / #1203 CMake list | the collision named (Q7) |
| T18 `02:24-27`... the seven test files | the subjects audited here; their cases pass |
| T18 `02:50-58` `app-unit-tests` | built: 18 cases pass |
| T18 #1150 CloudOffer linger | T18's fix, cited |
| T26 `JourneyTiers::PATH` uncached | a positive |
| T31 `GuiKeyMappingEditor` strips (#63) | the pages are T31's; the load is L-28 |
| T32 3.32 `FileSorts.h:22-23` | the enum is T33's; the bug is T32's |
| Backlog #560 FAST SHUTDOWN | `Gamelist.cpp:374-481` is the writer's half: recorded with L-05 |
| #69 Tools icons | cited, outside the 77 |
| #585 | the lines in `02` § The #585 lines owed |
| #1140, #1143, #1144 | T18's |
| the map's three declarations | Q7 |

## Renovation face

### Q1 Modernize
The writers want one atomic helper (`AtomicFileUtil`) where they now use `std::ofstream` and `pugi::save_file`. The collection reload wants the drop and remake halves #246 introduced.

### Q2 Standards
D-CLOUD-078 is met by none of the nine compiled writers. D-UI-051 is met but for three tag names. The fork's own `AppWindow` rule is not met by NetworkThread.

### Q3 Bugs
L-05, L-06, L-07, L-12, L-20, L-23, L-25, L-26, and L-14's substring. The proposed set and its owners are in `05`.

### Q4 Package currency
pugixml is a gitlink at the pin (`61c944895e…`). rapidjson is the recipe's 1.1.0. Neither is behind the tree's.

### Q5 Efficiency
L-02 (`retroarch.cfg` on every exit), L-04 (the screenshot walk) and L-01 (the lock wait). None was measured as dominating on the guest.

### Q6 Dead ends
`Win32ApiSystem.*`, the four Windows resource files, `ScraperCmdLine.*` (L-21, L-22), and `CustomFeatures.cpp:151`'s commented write.

### Q7 Clarity and structure
Seven headers absent from `ES_HEADERS`. `KeyboardMapping`'s loader, which never reports what it drops. The menu map check's three title patterns.

## Instruction File Recommendations

### Coverage gaps (would have prevented)
- `es-code-traps.md` § Pure text and § A rescan: nothing says that ES's own writes outside `Utils::FileSystem` leave the cache stale. The cached-read rule (`es-native-ui.md` § "A file another process writes is read uncached") covers other processes only, and L-23's third shape is the same process.

### Codification gaps (proposals for the coordinator)
- **`tools/es-menu-map-check` reads only three title shapes.** A fourth, `mMenu(window, _("..."))` in a member initializer, would see the two filter pages (#951/#965's class).
- **A writer rule a grep can audit:** `save_file(`, `std::ofstream` or `writeAllText(` on a player-data path, outside `AtomicFileUtil`.

## Second opinion

Filled after the two keyed calls (stage C's last step).

## Quality self-check

- **Every figure in `02` is a tool's line,** and every generator has a constructed negative.
- **Every proved lead names its artifact:** a guest step's file and frame, or a fixture's FAIL-then-PASS pair.
- **Void passes are recorded as void:** G-04's first read.
- **Corrections to the brief are listed** (`03` § 3.3).
- **What a subagent read is labelled** (`stage-c/floor.md`).
- **Not done:** FR frames; the index toast; L-02's `stat`; L-14's substring case; a TSan run.
