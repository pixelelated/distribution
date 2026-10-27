# Punch list — M6.P2 T33, EmulationStation's system layer (#680)

Written by the first reader (Opus 5.5) at stage C, and rendered by `tools/t33-05.py` from `stage-c/punch-items.py`. Its sources:
- `02` § The leads (L-01 to L-29, and the floor's 41 with their verdicts);
- `04` § Risk assessment;
- the guest cycle, the stage-C fixtures (`stage-c/runs.txt`) and the floor read (`stage-c/floor.md`, a subagent's, labelled);
- the seat's grades (`stage-c/astra-grades.md`).

- **reviewed-at:** `27bd8499f1` (distribution); **reviewed-at-es:** `16dbac5211` (the pin). **fixed-at** and **fixed-at-es** come at stage E.
- **Independent depth:** one seat, GPT-6 Astra at `max` (`second-opinions/review-plan.json`).
- **One item per defect or reusable improvement**, however many leads found it, ordered by severity within the bugs proposed, then the recorded.
- **Nothing here changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. A fix lands only under a stream brief on the ES branch, proven twice. A row added, moved or renamed updates `docs/es-menu-map.md` in the same commit (D-UI-039).
- **Lines** are the pin's. "Guest" means the M6 image (M7's composition over the pin). "Fixture" means a stage-C harness that fails at the pin and passes its control.
- **Every disposition is a question** for the stage-D pause (`question:`). The coordinator rules; the bugs are filed after the ruling, each with its code trace and its `Already written:` line.

---

## PL-01: a `gamelist.xml` restored from the cloud while ES runs is overwritten by the next save with the changed entries alone (a `bug` proposed; upstream's reader and writer, the fork's lanes, D-CLOUD-049)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q4
- **Family:** a read of a file another process writes; a write with no last good copy
- **Source Finding:** L-05, 3.13, 3.15 -- proved: fixture (`stage-c/l313-update-gamelist.py`); guest (G-04, with its control)
- **Owner area:** `es-app/src/Gamelist.cpp:412-413`, `:466-477` (`:474`), `:518-631` (`:601`, `:622`, `:705`, `:732-748`, `:841`); `SystemData.cpp:1653` (`getGamelistPath`, outside the slice)
- **What:**
  - `SystemData::getGamelistPath` caches the system's `gamelist.xml` as absent when the systems load (`SystemData.cpp:1653`), and `updateGamelist` reads that cached answer at `:413`.
  - A file the cloud's game-content restore writes afterwards is not seen: the save starts from an empty `<gameList>` (`:427`) and writes only the dirty entries over the restored file in place (`:474`). Every restored description and picture reference is lost.
  - `cleanupGamelist` and `packGamelist` decide media references by the same cache (`:601`, `:705`, `:732-748`; the floor's 3.15) and write in place after a `.old` copy nothing reads (`:619-622`, `:838-841`).
- **Fix shape:**
  - the read of `gamelist.xml` and of each media path in the three functions uncached (`exists(path, false)`), and `getGamelistPath`'s own check the same;
  - the three writes temp-and-rename through `AtomicFileUtil`, which also drops the cache entry.
- **Can this be done on the VM?** Yes. The fixture against the fixed file (`fix-unit-test` shape), then G-04 again on the integration image (`fix-walk-pending-image`).
- **Already written:** a `gamelist.xml` already overwritten on a device is lost metadata the device cannot recover; the cloud copy is the player's, and a restore after the fix is read. A `gamelist.xml.old` left by `:619-620` or `:838-839` is read by nothing, before or after: nothing inherited.
- **Acceptance:**
  - [ ] `stage-c/l313-update-gamelist.py` against the fixed `Gamelist.cpp` prints `Bravo present` and `inode new (replaced)` with rc 0, and against the pin reports both FAIL lines (`stage-e/` before/after records).
  - [ ] On the integration image, G-04's steps leave `/storage/roms/gb/gamelist.xml` holding both the outside entry and the favourite (a `vm-serial` read in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6 (upstream-carried, contained, inside the lanes), one stream with a #585 line?

## PL-02: editing a dynamic collection's filters from the collections bundle frees the games the bundle's view points at, then reads the cursor (a `bug` proposed; upstream's reload, #246's shape)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-06, T32 L-16 -- proved: fixture (`stage-c/l06-reload-collection.py`, a heap-use-after-free under ASan); the guest's G-02 drove a plain collection, which `:1573` never repopulates
- **Owner area:** `es-app/src/CollectionSystemManager.cpp:1558-1600` (`reloadCollection`), `:1115-1117` (`populateCustomCollection`'s clear), `:1302` (the bundle's child); callers `guis/GuiGamelistOptions.cpp:425`, `views/gamelist/ISimpleGameListView.cpp:462`
- **What:**
  - A dynamic collection's root folder is the custom collections bundle's child, by identity (`:1302`).
  - `reloadCollection(name, true)` repopulates it, and `populateCustomCollection` clears the root (`:1117`), deleting every game in it. `ViewController::reloadGameListView(bundle)` then reads the old view's cursor (`ViewController.cpp:1140-1142`), a freed `FileData` when the cursor was on one of those games.
- **Fix shape:**
  - read the bundle view's cursor path before the repopulate and remake the view from it (`es-code-traps.md:191`'s two halves, `dropGameListView` / `remakeGameListView`).
- **Can this be done on the VM?** Yes. The fixture against the fixed file; on the integration image, a dynamic collection's filter edited from the bundle with the cursor on one of its games, the journal read for a backtrace.
- **Already written:** nothing inherited: a crash leaves no record but the journal's backtrace.
- **Acceptance:**
  - [ ] `stage-c/l06-reload-collection.py` against the fixed `CollectionSystemManager.cpp` prints `no freed entry was read` with no sanitizer report (rc 0), and against the pin reports the heap-use-after-free (`stage-e/` records).
  - [ ] On the integration image, the walk above ends with the same ES pid and no `crash backtrace` line in `journalctl -u essway` (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6, a #585 line?

## PL-03: backing out of a single-game scrape while its search is being built leaves the builder's thread writing into freed memory (a `bug` proposed; upstream's search component, outside the lanes)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-07, L-08 -- proved: fixture (`stage-c/l07-search-builder.py`, a heap-use-after-free under ASan)
- **Owner area:** `es-app/src/components/ScraperSearchComponent.cpp:196-258` (`ScraperAsyncRequestsBuilder`), `:206`, `:231`; drop sites `:358-361`, `:96-100`; `:645-658` (L-08's synchronous second search)
- **What:**
  - The builder runs `Scraper::search` on a thread it news (`:206`) and never joins or deletes; `update()` drops the pointer after a join (`:231`), leaking the object. The class has no destructor.
  - `stop()` and the component's destructor drop the builder while its thread runs: the thread then writes `mSearchHandle`, `mError` and `mFinished` into freed memory. `mFinished` is read across threads unsynchronised.
  - L-08: with no results, the second search runs synchronously on the interface thread (`:652`, `:658`).
- **Fix shape:**
  - a destructor that joins and deletes the thread; the thread deleted after `update()`'s join; `mFinished` atomic; L-08's second search through the same builder.
- **Can this be done on the VM?** Yes. The fixture against the fixed file; a guest walk cannot time the window.
- **Already written:** nothing inherited: no file is written by the window.
- **Acceptance:**
  - [ ] `stage-c/l07-search-builder.py` against the fixed file prints `nothing wrote into the freed builder` with no sanitizer report (rc 0), and against the pin reports the heap-use-after-free (`stage-e/` records).
- **Disposition (proposed for the stage-D pause):** question: a `bug` under rule 6 though outside the lanes (a crash, contained), or recorded with a #585 line?

## PL-04: a genre name found by its part after `/` returns through the end iterator (a `bug` proposed; upstream's genre table)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** the floor's 3.8 [re-read], 3.11 -- proved: tree (`stage-c/floor.md`, the first reader's re-read at `Genres.cpp:304`)
- **Owner area:** `es-app/src/Genres.cpp:293-306` (`fromGenreName`), `:299`; reached from `FileFilterIndex.cpp:1251-1253`, `:1184` (a dynamic collection's genre filter) and the scrapers
- **What:**
  - `fromGenreName` looks a name up whole (`:295`); on a miss it tries each part after `/` and, on a hit, returns `mGenres[g->second]` (`:304`), where `g` is the whole name's end iterator, not the part's `sg`. That is undefined behaviour: a wrong genre or a crash.
  - `:299`'s `name.find("/") >= 0` is always true (`size_t`).
  - The floor's 3.8 also finds a parent genre counted twice for a game with two of its children (`Genres.cpp:244-248`, `FileFilterIndex.cpp:1015-1016`).
- **Fix shape:**
  - `mGenres[sg->second]` at `:304`; `!= std::string::npos` at `:299`; a unit case over a document seam (3.8's).
- **Can this be done on the VM?** Yes. A unit case in `es-unit-tests` over a genre table; it FAILs at the pin under ASan.
- **Already written:** nothing inherited: a filter's `.xcc` stores the genre by name and is read the same way after the fix.
- **Acceptance:**
  - [ ] A unit case `fromGenreName("Foo / <a known subgenre>")` returns that subgenre's entry; at the pin, under ASan, it reports the end-iterator read (`stage-e/` records).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6 (one token), with the double count recorded?

## PL-05: a custom collection's list and a dynamic collection's filter are written in place, and ES's own writes leave the file cache stale (a `bug` proposed; upstream's writers, settings tier)

- **Severity:** Medium
- **Category:** Reliability
- **Question:** Q4
- **Family:** a write with no last good copy; a read of a file another process writes
- **Source Finding:** L-23, the third cache shape -- proved: tool-run (`t33-writes.py`, `t33-reads.py`)
- **Owner area:** `es-app/src/CollectionSystemManager.cpp:340-358` (`std::ofstream`, `:345`), `:1610`, `:1613`, `:963`; `FileFilterIndex.cpp:1313` (`pugi::save_file`), `:1144`
- **What:**
  - Both files are in the settings tier backuptool archives, written in place with no error check (`:345`) or a logged one (`:1313`). A cut `custom-<name>.cfg` reads as a shorter collection, which the next save writes back; a cut `.xcc` is a parse error and the collection loses its filter.
  - Neither writer goes through `Utils::FileSystem`, so a path whose miss the cache remembered (`:963` reads the `.xcc` at startup) stays absent: `deleteCustomCollection` (`:1610`, `:1613`) can return false for a file written this session.
- **Fix shape:**
  - both writes through `AtomicFileUtil` (temp-and-rename), which drops the cache entry; the delete's checks uncached.
- **Can this be done on the VM?** Yes. A file case over a temp folder for each writer (the floor's 3.11 shape), and the delete after a create in one session on the guest.
- **Already written:** a `custom-<name>.cfg` or `.xcc` already cut on a device reads as it does today, a shorter list or no filter; the fix changes the write, not the read: nothing to migrate.
- **Acceptance:**
  - [ ] A file case kills the write half-way (a writer double) and the previous file is what remains; at the pin the cut file remains (`stage-e/`).
  - [ ] On the integration image, a custom collection created and deleted in one session leaves no `custom-<name>.cfg` (a `vm-serial` listing in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6, one stream with PL-01's helper?

## PL-06: NetworkThread posts straight to the window, past the closing gate the fork wrote for exactly this (a `bug` proposed; the fork's file)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-12 -- proved: fixture (`stage-c/l12-network-posts.py`)
- **Owner area:** `es-app/src/NetworkThread.cpp:206`, `:237`, `:251`, `:257`, `:266`; `AppWindow.h:38-45`; `main.cpp:1322`, `:1330`
- **What:**
  - `AppWindow::post` drops a worker's post once `main()` calls `AppWindow::closing()` (`main.cpp:1322`, F-ES-26). NetworkThread's watchers run until `WatchersManager::stop()` (`:1330`), and its five posts call `mWindow->postToUiThread` directly: a check that ends between the two lines queues a task no loop runs, `:266`'s token write among them.
- **Fix shape:**
  - the five posts through `AppWindow::post(mWindow, ...)`.
- **Can this be done on the VM?** Yes. The fixture's count and run against the fixed file.
- **Already written:** nothing inherited: a lost task writes nothing.
- **Acceptance:**
  - [ ] `stage-c/l12-network-posts.py` against the fixed `NetworkThread.cpp` prints `0 direct post(s)` (rc 0), and against the pin `5 direct post(s) at :206, :237, :251, :257, :266` (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug` (the fork's own rule), noting T20's hasher-start lines `:248`, `:251`?

## PL-07: three tag names a player reads, IN PROGRESS, DROPPED and ON HOLD, never reach the French catalog (a `bug` proposed; upstream's words, D-UI-051)

- **Severity:** Medium
- **Category:** Words
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-25, 3.29 -- proved: fixture (`stage-c/l329-filetag-words.py`)
- **Owner area:** `es-app/src/FileTag.cpp:6-11` against `:16-18`; `locale/lang/fr/LC_MESSAGES/emulationstation2.po`
- **What:**
  - Six of nine names pass through `fake_gettext_*` defines so xgettext extracts them; IN PROGRESS, DROPPED and ON HOLD do not, and the catalog has no msgid for them. T31's filter and metadata pages show them in English under French.
- **Fix shape:**
  - three `fake_gettext_*` defines and their French, proposed and built as proposed (D-UI-112): EN COURS, ABANDONNÉ, EN PAUSE.
- **Can this be done on the VM?** Yes. The fixture against the fixed file and catalog; a frame of the filter page in FR on the integration image.
- **Already written:** nothing inherited: a tag is stored by its English name in `gamelist.xml` and is unchanged; only the label is translated.
- **Acceptance:**
  - [ ] `stage-c/l329-filetag-words.py` against the fixed `FileTag.cpp` and catalog prints `9 tag names, 0 without` (rc 0), and against the pin `3 without` (`stage-e/`).
  - [ ] `tools/es-untranslated` reports 0 without French on the stream's tree.
- **Disposition (proposed for the stage-D pause):** question: a `bug` with the three French words as proposed (the maintainer's to change)?

## PL-08: the long-job pages' text fit keeps four characters of an ASCII name and one of a Japanese one (a `bug` proposed; the fork's helper)

- **Severity:** Low
- **Category:** Words
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-20, 3.35, T20 S9 -- proved: fixture (`stage-c/l335-textfit-floor.py`); `TextFitTests.cpp`'s 3 cases pass
- **Owner area:** `es-app/src/TextFit.h:34`; callers `guis/GuiCloudTransfer.cpp:585`, `GuiOfflineScan`, `GuiScraperRun`
- **What:**
  - `fitOneLine`'s floor `text.size() > 4` counts bytes, so the minimum kept is four ASCII characters but one CJK character.
- **Fix shape:**
  - the floor counted in characters (the helper's own `popCharacter` rule).
- **Can this be done on the VM?** Yes. The fixture and a fourth `TextFitTests.cpp` case.
- **Already written:** nothing inherited: a label is drawn, not stored.
- **Acceptance:**
  - [ ] `stage-c/l335-textfit-floor.py` against the fixed header keeps 4 characters for both scripts (rc 0); a new `TextFitTests.cpp` case passes in `app-unit-tests`.
- **Disposition (proposed for the stage-D pause):** question: a `bug`?

## PL-09: a ROM tagged `(India)` reads no language or region: the table's token is `ìndia` (a `bug` proposed; upstream's)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q5
- **Family:** a check whose failure reads as success
- **Source Finding:** L-26, 3.31 -- proved: fixture (`stage-c/l331-lang-india.py`)
- **Owner area:** `es-app/src/LangParser.cpp:65`
- **What:**
  - Tags are lowercased before `extractLang` (`:148`); `india` never equals `ìndia` (U+00EC), so only `in` matches.
- **Fix shape:**
  - the token `india`.
- **Can this be done on the VM?** Yes. The fixture against the fixed file.
- **Already written:** nothing inherited: the language is derived at load, not stored.
- **Acceptance:**
  - [ ] `stage-c/l331-lang-india.py` against the fixed file reads `india -> lang [in] region [in]` (rc 0).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6, a #585 line?

## PL-10: `RunLock::holder` names any process whose command line merely contains the program's name (a `bug` proposed; the fork's helper)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-14, the floor's 3.38 -- proved: tree (`RunLock.h:66-68`; `stage-c/floor.md`); `RunLockTests.cpp`'s 3 cases pass
- **Owner area:** `es-app/src/RunLock.h:44-70`; caller `OfflineAchievements::stopRun`
- **What:**
  - With the lock held and its pid reused by, say, `tail -f /var/log/raofflineproxy-ctl.log`, `holder()` returns that pid, and `stopRun` signals it.
- **Fix shape:**
  - argv[0]'s basename compared for equality; a fourth `RunLockTests.cpp` case.
- **Can this be done on the VM?** Yes. A `RunLockTests.cpp` case with a fixture cmdline file.
- **Already written:** nothing inherited: the lock file holds a pid, read the same way.
- **Acceptance:**
  - [ ] A new `RunLockTests.cpp` case (a holder whose cmdline contains the name as a substring) FAILs at the pin and passes on the fix in `app-unit-tests` (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`?

## PL-11: a 64-bit id or epoch in the proxy's list is truncated to `int` (a `bug` proposed; the fork's helper)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-17, the floor's 3.41 -- proved: tree (`stage-c/floor.md`)
- **Owner area:** `es-app/src/OfflineAchievementsText.cpp:17-20` (`jsonInt`), `:229`
- **What:**
  - `"4294967297 1700000000"` reads id 1 and is accepted; `(int)v.GetInt64()` truncates the same way. Harmless with today's ids.
- **Fix shape:**
  - `int64_t` through, with an `OfflineAchievementsTextTests.cpp` case above 2^31 (T20's delta on the same file named as a collision).
- **Can this be done on the VM?** Yes. A case in `es-unit-tests`.
- **Already written:** nothing inherited: the ids are read from the proxy each time.
- **Acceptance:**
  - [ ] A new `OfflineAchievementsTextTests.cpp` case with an id above 2^31 FAILs at the pin and passes on the fix (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, or deferred to T20's file?

## PL-12: a key map's refused trigger drops the whole mapping with no word, and the loader reads strings unchecked (upstream's loader, outside the lanes)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-28, 3.21 -- proved: fixture (`stage-c/l321-keys-parse.py`); guest (G-08)
- **Owner area:** `es-app/src/KeyboardMapping.cpp:217-300` (`:262-272`, `:292`; `GetString` with no `IsString` at `:247-288`)
- **What:**
  - A trigger `checkTriggerExists` refuses is skipped, and a mapping with no trigger is dropped (`:292`): the editor shows the rest and says nothing.
  - Under NDEBUG, `GetString` on a `type`, `mode`, `description` or `trigger` that is not a string is a wild read on a hand-edited file.
- **Fix shape:**
  - a log line naming the dropped trigger (the fixture's control), and shape before every `GetString`.
- **Can this be done on the VM?** Yes. The fixture against the fixed file; G-08 on the integration image.
- **Already written:** nothing inherited: `.keys` files are read the same way; the fix adds a line, not a format.
- **Acceptance:**
  - [ ] `stage-c/l321-keys-parse.py` against the fixed file prints the log line naming `t33unknown` (rc 0).
- **Disposition (proposed for the stage-D pause):** question: recorded with a #585 line (outside the lanes, D-UI-079), or a `bug` under rule 6?

## PL-13: the filter's rating and year keys: a positive rating reads 0 STARS, a year outside 1000-2999 reads nothing, and `1 STARS` (upstream's filter, outside the lanes)

- **Severity:** Low
- **Category:** Words
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-27, 3.9 -- proved: fixture (`stage-c/l309-rating-year.py`)
- **Owner area:** `es-app/src/FileFilterIndex.cpp:321-340`, `:364-369`
- **What:**
  - `0.05` rounds to `0 STARS` where `""` and `"0"` read UNKNOWN; `3000…` and `0999…` read `""`; the label for one star is `1 STARS`.
- **Fix shape:**
  - a floor of one star for a positive rating; four digits for a year; the label's singular.
- **Can this be done on the VM?** Yes. The fixture against the fixed file.
- **Already written:** nothing inherited: the keys are derived at load.
- **Acceptance:**
  - [ ] `stage-c/l309-rating-year.py` against the fixed file prints no `(want ...)` line (rc 0).
- **Disposition (proposed for the stage-D pause):** question: recorded with a #585 line (outside the lanes), or a `bug`?

## PL-14: closing a RetroAchievements page waits on the watcher lock while a network check holds it (es-core's lock, the fork's callers)

- **Severity:** Medium
- **Category:** Performance
- **Question:** Q2
- **Family:** a call with no bound
- **Source Finding:** L-01 -- proved: tree (the read trace; G-09 `CANNOT`)
- **Owner area:** `es-core/src/watchers/WatchersManager.cpp:181-196`, `:92-100` (T21's file); `NetworkThread.cpp:21-25` <- `guis/GuiRetroAchievementsSettings.cpp:806`, `:257`, `:191`
- **What:**
  - The interface thread's `ResetComponent` takes `mWatchersLock`, which the watcher thread holds across every `check()`, a network login among them: a page close waits out the check.
- **Fix shape:**
  - `check()` run outside `mWatchersLock`, or `nextCheckTime` under a lock of its own (rule 6, T21's file named).
- **Can this be done on the VM?** No case without SDL; the bound's arithmetic and the trace are the proof.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] The stream's record shows `check()` called with `mWatchersLock` released (a line-cited read of the fixed `WatchersManager.cpp` in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug` under rule 6 in es-core (T21's file), or routed to the es-core slice?

## PL-15: CloudOffer says DONE on a script's exit 0 alone (the fork's dialog; the script's half is the rclone slice's)

- **Severity:** Low
- **Category:** Words
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-18 -- proved: tree
- **Owner area:** `es-app/src/CloudOffer.cpp:37`, `:42-45`
- **What:**
  - `timeout 90 cloud_setup --seed-folders saves` (the bound is sound); its rc alone chooses DONE or COULDN'T CREATE IT, so a script that exits 0 having created nothing says DONE, and a `timeout` kill (124) reads as the connection.
- **Fix shape:**
  - the outcome read from the folder's presence after the run, or the script's `>>> why` line; the script's half to the rclone slice.
- **Can this be done on the VM?** Yes, with a stub script on the guest.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] A guest run with a stub that exits 0 without creating the folder shows the not-done outcome (a frame in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a stream here, or the whole item to the rclone slice?

## PL-16: the other in-place writers: the rotation record, the key maps, and `saveToXml`'s remove-then-save (Backlog #1186's sites)

- **Severity:** Medium
- **Category:** Reliability
- **Question:** Q4
- **Family:** a write with no last good copy
- **Source Finding:** L-03, T21 PL-20 -- proved: tool-run (`t33-writes.py`)
- **Owner area:** `es-app/src/CaptureRotation.cpp:175`, `KeyboardMapping.cpp:426`, `:429`, `Gamelist.cpp:307-308`
- **What:**
  - `writeAllText` in place (`CaptureRotation.cpp:175`, `KeyboardMapping.cpp:426`, `:429`) and remove-then-save with no file between (`Gamelist.cpp:307-308`).
- **Fix shape:**
  - #1186's helper, when it lands, at these four lines.
- **Can this be done on the VM?** Yes, as #1186 states.
- **Already written:** a cut `.rotation` reads as untrusted (`:124`), a cut `.keys` as an empty map, a cut recovery file as no recovery: each falls to the safe reading.
- **Acceptance:**
  - [ ] #1186's acceptance names these four lines.
- **Disposition (proposed for the stage-D pause):** question: deferred to #1186, these lines added to it?

## PL-17: the map describes neither filter page nor UPDATE GAMELISTS, and the map check cannot see member-initialized titles (required: D-UI-039)

- **Severity:** Medium
- **Category:** Documentation
- **Question:** Q7
- **Family:** a page the map does not describe
- **Source Finding:** Q7, the brief's § 7 -- proved: tool-run (`es-menu-map-check`'s line; the grep's 0 hits)
- **Owner area:** `docs/es-menu-map.md`; `tools/es-menu-map-check:48-55`; `guis/GuiGamelistFilter.cpp:11`, `:17`; `guis/GuiMenu.cpp:5756`; `guis/GuiCollectionSystemsOptions.cpp:368`
- **What:**
  - The proposed text is in `02` § The structure. The check reads three title shapes and misses `mMenu(window, _("..."))` in a member initializer (#951/#965's class).
- **Fix shape:**
  - the rows added by the coordinator's stage-E stream, in the same commit as any row it touches; the fourth pattern for the coordinator.
- **Can this be done on the VM?** Yes: the check and the grep on the tree.
- **Already written:** nothing inherited: documentation.
- **Acceptance:**
  - [ ] `grep -c -E 'FILTER GAMELIST BY|EDIT DYNAMIC COLLECTION FILTERS|UPDATE GAMELISTS' docs/es-menu-map.md` prints 3 or more, and `tools/es-menu-map-check` prints `0 missing`.
- **Disposition (proposed for the stage-D pause):** question: the stream at stage E as the brief says; the check's pattern to #951/#965?

## PL-18: the floor's smaller upstream defects (recorded; upstream's)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** the floor's 3.1, 3.3, 3.4, 3.5, 3.10's aside, 3.14, 3.16, 3.17, 3.26, 3.28, 3.32, 3.34, 3.37; 3.20's sibling -- proved: tree (`stage-c/floor.md`)
- **Owner area:** `PlatformId.cpp:28`, `:171`; `MetaData.cpp:303`, `:313`, `:392-404`, `:568`; `FileFilterIndex.cpp:579-580`; `Gamelist.cpp:177`; `CollectionSystemManager.cpp:627-651`, `:1510`; `CustomFeatures.cpp:531`, `:536`; `FileSorts.cpp:38`; `LangParser.cpp:225-226`; `SystemRandomPlaylist.cpp:28-30`; `FolderMerge.h:50-52`; `FileData.cpp:1659` (outside the slice)
- **What:**
  - Each in `stage-c/floor.md` with its input. The two with a player cost: a scrape blanks a filled field it did not return (3.5, `MetaData.cpp:568`), and `<sys>.sort=28` throws at `FileData.cpp:1659` (T2 FD-15's sibling, #771).
- **Fix shape:**
  - each recorded with a #585 line; 3.20's sibling to #771.
- **Can this be done on the VM?** Yes, each as a unit case.
- **Already written:** nothing inherited by recording.
- **Acceptance:**
  - [ ] `02` § The #585 lines owed carries a line for each of 3.5 and 3.8's double count, and #771 carries `FileData.cpp:1659` (a comment link in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: recorded, 3.5 raised to a `bug`, and `FileData.cpp:1659` to #771?

## PL-19: the surfaces outside the lanes: Zaparoo's unbounded probe, the installer's and Bluetooth's self-deleting workers and tool-text toasts, the screensaver's cached reads and launch, the scraper search's words (recorded; D-UI-079)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a call with no bound
- **Source Finding:** L-09, L-10, L-11, L-02, L-04, the take-up row T2 `:293-294`, `02` § The words -- proved: tool-run, tree, guest (G-06)
- **Owner area:** `ZaparooSupport.cpp:32-39`, `:58-63`; `ContentInstaller.cpp:61`, `:144-236`; `ThreadedBluetooth.cpp:19-110`; `SystemScreenSaver.cpp:156-164`, `:546`; `components/ScraperSearchComponent.cpp:386`, `:468`; `CaptureRotation.cpp:162`; `DisplayAspect.cpp:74-87`
- **What:**
  - Each in `02` with its lines: no bound past the connect; `delete this` on a worker; `AN ERROR OCCURRED: <status>`; ten retries over a cached miss; the screensaver's launch skipping the format and BIOS checks (keeping the cloud gate); an English dialog outside `_()`; `retroarch.cfg` read on every exit; the screenshot walk.
- **Fix shape:**
  - recorded, with #585 lines; L-02 and L-04 priced by the integration image's time-to-play.
- **Can this be done on the VM?** Partly: G-06 ran; the rest are reads.
- **Already written:** nothing inherited by recording.
- **Acceptance:**
  - [ ] `02` § The #585 lines owed carries the recorded row naming these files.
- **Disposition (proposed for the stage-D pause):** question: recorded as listed?

## PL-20: the Windows and console residue (recorded; L-21, L-22)

- **Severity:** Low
- **Category:** Structure
- **Question:** Q7
- **Family:** a page the map does not describe
- **Source Finding:** L-21, L-22 -- proved: tool-run (`stage-a/syntax-check.out`, the CMake grep)
- **Owner area:** `Win32ApiSystem.cpp`/`.h`, `EmulationStation.h.in`, `EmulationStation.rc`, `EmulationStation.aps`, `es_icon.ico`, `ScraperCmdLine.cpp`/`.h`; `es-app/CMakeLists.txt:287`
- **What:**
  - One row each in `02` § The structure.
- **Fix shape:**
  - none by the lane; `ScraperCmdLine` to #1235.
- **Can this be done on the VM?** n/a.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] #1235 names `ScraperCmdLine.*` (a comment link in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: recorded, `ScraperCmdLine` to #1235?

## Phase 7 resolution gate

Stage F rewrites this table and the index together. Until then every item is `Open`.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | -- |
| PL-02 | Open | -- |
| PL-03 | Open | -- |
| PL-04 | Open | -- |
| PL-05 | Open | -- |
| PL-06 | Open | -- |
| PL-07 | Open | -- |
| PL-08 | Open | -- |
| PL-09 | Open | -- |
| PL-10 | Open | -- |
| PL-11 | Open | -- |
| PL-12 | Open | -- |
| PL-13 | Open | -- |
| PL-14 | Open | -- |
| PL-15 | Open | -- |
| PL-16 | Open | -- |
| PL-17 | Open | -- |
| PL-18 | Open | -- |
| PL-19 | Open | -- |
| PL-20 | Open | -- |

```yaml
punch_index:
- id: PL-01
  severity: "High"
  category: Correctness
  question: Q4
  source_finding: "L-05, 3.13, 3.15"
  outcome: "open"
- id: PL-02
  severity: "High"
  category: Correctness
  question: Q1
  source_finding: "L-06, T32 L-16"
  outcome: "open"
- id: PL-03
  severity: "Medium"
  category: Correctness
  question: Q1
  source_finding: "L-07, L-08"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Correctness
  question: Q3
  source_finding: "the floor's 3.8 [re-read], 3.11"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: Reliability
  question: Q4
  source_finding: "L-23, the third cache shape"
  outcome: "open"
- id: PL-06
  severity: "Medium"
  category: Correctness
  question: Q1
  source_finding: "L-12"
  outcome: "open"
- id: PL-07
  severity: "Medium"
  category: Words
  question: Q5
  source_finding: "L-25, 3.29"
  outcome: "open"
- id: PL-08
  severity: "Low"
  category: Words
  question: Q5
  source_finding: "L-20, 3.35, T20 S9"
  outcome: "open"
- id: PL-09
  severity: "Low"
  category: Correctness
  question: Q5
  source_finding: "L-26, 3.31"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-14, the floor's 3.38"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-17, the floor's 3.41"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-28, 3.21"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Words
  question: Q3
  source_finding: "L-27, 3.9"
  outcome: "open"
- id: PL-14
  severity: "Medium"
  category: Performance
  question: Q2
  source_finding: "L-01"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Words
  question: Q3
  source_finding: "L-18"
  outcome: "open"
- id: PL-16
  severity: "Medium"
  category: Reliability
  question: Q4
  source_finding: "L-03, T21 PL-20"
  outcome: "open"
- id: PL-17
  severity: "Medium"
  category: Documentation
  question: Q7
  source_finding: "Q7, the brief's § 7"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "the floor's 3.1, 3.3, 3.4, 3.5, 3.10's aside, 3.14, 3.16, 3.17, 3.26, 3.28, 3.32, 3.34, 3.37; 3.20's sibling"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-09, L-10, L-11, L-02, L-04, the take-up row T2 `:293-294`, `02` § The words"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-21, L-22"
  outcome: "open"
```
