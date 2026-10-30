# Punch list — M6.P2 T33, EmulationStation's system layer (#680)

Written by the first reader (Opus 5.5) at stage C, and rendered by `tools/t33-05.py` from `stage-c/punch-items.py`. Its sources:
- `02` § The leads (L-01 to L-29, and the floor's 41 with their verdicts);
- `04` § Risk assessment;
- the guest cycle, the stage-C fixtures (`stage-c/runs.txt`) and the floor read (`stage-c/floor.md`, a subagent's, labelled);
- the seat's grades (`stage-c/astra-grades.md`).

- **reviewed-at:** `27bd8499f1` (distribution); **reviewed-at-es:** `16dbac5211` (the pin). **fixed-at:** the distribution's hand-back tip on `feature/m6-es-app-system-680` (named in #680's header and the hand-back post); **fixed-at-es:** `f802c55c6` (`feature/m6-es-app-system-680`, pixelelated/emulationstation; S1a `d0d92dda6` to S6 over the pin).
- **Independent depth:** one seat, GPT-6 Astra at `max` (`second-opinions/review-plan.json`).
- **One item per defect or reusable improvement**, however many leads found it. PL-01 to PL-20 are the first read's, ordered by severity within the bugs proposed, then the recorded; PL-21 to PL-26 are the seat's new items (EP-39 to EP-46), appended.
- **Nothing here changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. A fix lands only under a stream brief on the ES branch, proven twice. A row added, moved or renamed updates `docs/es-menu-map.md` in the same commit (D-UI-039).
- **Lines** are the pin's. "Guest" means the M6 image (M7's composition over the pin). "Fixture" means a stage-C harness that fails at the pin and passes its control.
- **Every disposition is a question** for the stage-D pause (`question:`). **Ruled 20:10 UTC** (#680 comment 6452429909): twenty bugs, #1271 to #1290, filed with their code traces by `tools/t33-file-bugs.py`; **ruled 20:15 UTC** (#680 comment 6452522368): PL-13 and PL-18's 3.5, #1291 and #1292 (`--second`). Each item's **Bug:** line names its issue.
- **The audit issue:** #1270 (a sub-issue of #680), one checkbox per item, ticked at stage E's hand-back from the Phase 7 table below; `tools/box-check --issue 1270`'s line is in the hand-back post.
- **Lines corrected at Phase 7** (the stream brief's § Lines): PL-04's `:304` is `:305`; PL-09's `:148` is `:150`; PL-12's `:292` is `:293-294`; PL-22's `resetIndex` is `:148-162`; PL-13's `:321` is `:322`; PL-11's `:229` is `:230`; the checker's patterns are `:49-56`.

---

## PL-01: a `gamelist.xml` restored from the cloud while ES runs is overwritten by the next save with the changed entries alone (a `bug` proposed; upstream's reader and writer, the fork's lanes, D-CLOUD-049)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q4
- **Family:** a read of a file another process writes; a write with no last good copy
- **Source Finding:** L-05, 3.13, 3.15, EP-1, EP-2, EP-36 -- proved: fixture (`stage-c/l313-update-gamelist.py`); guest (G-04, with its control)
- **Owner area:** `es-app/src/Gamelist.cpp:412-413`, `:466-477` (`:474`), `:518-631` (`:601`, `:622`, `:705`, `:732-748`, `:841`); `SystemData.cpp:1653` (`getGamelistPath`, outside the slice)
- **What:**
  - `SystemData::getGamelistPath` caches the system's `gamelist.xml` as absent when the systems load (`SystemData.cpp:1653`), and `updateGamelist` reads that cached answer at `:413`.
  - A file the cloud's game-content restore writes afterwards is not seen: the save starts from an empty `<gameList>` (`:427`) and writes only the dirty entries over the restored file in place (`:474`). Every restored description and picture reference is lost.
  - `cleanupGamelist` and `packGamelist` decide media references by the same cache (`:601`, `:705`, `:732-748`; the floor's 3.15) and write in place after a `.old` copy nothing reads (`:619-622`, `:838-841`).
  - **EP-36:** even with a fresh read, a dirty game's whole node is removed and rebuilt from memory (`:449-459`), so the restored description and art of *that* game are lost; and a writer between the read (`:416`) and the write (`:474`) is a lost update.
  - **EP-1:** an unreadable `gamelist.xml` is logged and then overwritten (`:416-424`).
- **Fix shape:**
  - the reads uncached: `:413`, `getGamelistPath` (`SystemData.cpp:1652-1663`), and `packGamelist`'s and `cleanupGamelist`'s media probes (`:595-605`, `:702-752`; EP-2);
  - a field-level merge of a dirty game's node with the file's (EP-36), and no overwrite of a file that did not parse (EP-1);
  - the three writes temp-and-rename, with the cache entry dropped explicitly (EP-19);
  - the startup order checked: `packGamelist` clears recovery before `parseGamelist` reads it (EP-2).
- **Can this be done on the VM?** Yes. The fixture against the fixed file (`fix-unit-test` shape), then G-04 again on the integration image (`fix-walk-pending-image`).
- **Already written:** a `gamelist.xml` already overwritten on a device is lost metadata the device cannot recover; the cloud copy is the player's, and a restore after the fix is read. A `gamelist.xml.old` left by `:619-620` or `:838-839` is read by nothing, before or after: nothing inherited.
- **Acceptance:**
  - [ ] `stage-c/l313-update-gamelist.py` against the fixed `Gamelist.cpp` prints `Bravo present` and `inode new (replaced)` with rc 0, and against the pin reports both FAIL lines (`stage-e/` before/after records).
  - [ ] The fixture gains a same-game case (a restored description on the dirty game) that FAILs at the pin and passes on the fix (EP-36).
  - [ ] On the integration image, G-04's steps leave `/storage/roms/gb/gamelist.xml` holding both the outside entry and the favourite (a `vm-serial` read in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6 (upstream-carried, contained, inside the lanes), one stream with a #585 line?
- **Bug:** #1271 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-02: a dynamic collection's reload frees the games a view's cursor may hold, then reads the bundle view's cursor; the route from the bundle is not established (a `bug` proposed, conditional; upstream's reload, #246's shape)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-06, T32 L-16, EP-5, EP-37, EP-38 -- proved: fixture (`stage-c/l06-reload-collection.py`, the mechanism); the caller route open (EP-5)
- **Owner area:** `es-app/src/CollectionSystemManager.cpp:1558-1600` (`reloadCollection`), `:1115-1117` (`populateCustomCollection`'s clear), `:1302` (the bundle's child); callers `guis/GuiGamelistOptions.cpp:425`, `views/gamelist/ISimpleGameListView.cpp:462`
- **What:**
  - A dynamic collection's root folder is the custom collections bundle's child, by identity (`:1302`).
  - `reloadCollection(name, true)` repopulates it, and `populateCustomCollection` clears the root (`:1117`), deleting every game in it. `ViewController::reloadGameListView(bundle)` then reads the old view's cursor (`ViewController.cpp:1140-1142`), a freed `FileData` when the cursor was on one of those games.
  - **EP-5:** `GuiGamelistOptions.cpp:424` reloads the collection only when the system is not the bundle, and `ISimpleGameListView.cpp:461-462` reloads by the root's system. A route from the bundle is not established. A **non-bundled** dynamic collection's own view is cleared by `:1117` and not remade by `reloadCollection`: a further lead.
  - **EP-37:** `moveToFolder` is called on the retained old view, not the remade one (`:1586-1593`).
  - **EP-38:** the screensaver keeps `FileData*` (`SystemScreenSaver.cpp:350-358`) that no retirement shown clears.
- **Fix shape:**
  - every view holding the collection's games dropped before the clear and remade after from the cursor's path (`es-code-traps.md:191`); the remade view moved (EP-37); the caller route established before the stream (a read of `ISimpleGameListView.cpp:445-464`'s callers).
- **Can this be done on the VM?** Yes. The fixture against the fixed file; on the integration image, a dynamic collection's filter edited from the bundle with the cursor on one of its games, the journal read for a backtrace.
- **Already written:** nothing inherited: a crash leaves no record but the journal's backtrace.
- **Acceptance:**
  - [ ] `stage-c/l06-reload-collection.py` against the fixed `CollectionSystemManager.cpp` prints `no freed entry was read` with no sanitizer report (rc 0), and against the pin reports the heap-use-after-free (`stage-e/` records).
  - [ ] On the integration image, the walk above ends with the same ES pid and no `crash backtrace` line in `journalctl -u essway` (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug` under rule 6 once the route is read (the mechanism is proved), or recorded with the lead?
- **Bug:** #1272 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-03: backing out of a single-game scrape while its search is being built leaves the builder's thread writing into freed memory (a `bug` proposed; upstream's search component, outside the lanes)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-07, L-08 -- proved: fixture (`stage-c/l07-search-builder.py`, a heap-use-after-free under ASan)
- **Owner area:** `es-app/src/components/ScraperSearchComponent.cpp:196-258` (`ScraperAsyncRequestsBuilder`), `:206`, `:231`; drop sites `:358-361`, `:96-100`; `:645-658` (L-08's synchronous second search)
- **What:**
  - The builder runs `Scraper::search` on a thread it news (`:206`). `update()` joins it after a completed search and then drops the pointer without deleting it (`:230-233`; EP-6: the first reader's "never joined" was wrong). The class has no destructor.
  - `stop()` and the component's destructor drop the builder while its thread runs: the thread then writes `mSearchHandle`, `mError` and `mFinished` into freed memory. `mFinished` is read across threads unsynchronised.
  - L-08: with no results, the second search runs synchronously on the interface thread (`:652`, `:658`).
- **Fix shape:**
  - one ownership scheme: the builder owns its thread, joins only when `joinable()`, deletes it; `mFinished` atomic; `stop()` does not join on the interface thread (EP-6); L-08's second search through the same builder.
- **Can this be done on the VM?** Yes. The fixture against the fixed file; a guest walk cannot time the window.
- **Already written:** nothing inherited: no file is written by the window.
- **Acceptance:**
  - [ ] `stage-c/l07-search-builder.py` against the fixed file prints `nothing wrote into the freed builder` with no sanitizer report (rc 0), and against the pin reports the heap-use-after-free (`stage-e/` records).
- **Disposition (proposed for the stage-D pause):** question: a `bug` under rule 6 though outside the lanes (a crash, contained), or recorded with a #585 line?
- **Bug:** #1273 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-04: a genre name found by its part after `/` returns through the end iterator (a `bug` proposed; upstream's genre table)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** the floor's 3.8 [re-read], 3.11 -- proved: tree (`stage-c/floor.md`, the first reader's re-read at `Genres.cpp:304`; the line returned through is `:305`, stage E's § Lines)
- **Owner area:** `es-app/src/Genres.cpp:293-306` (`fromGenreName`), `:299`; reached from `FileFilterIndex.cpp:1251-1253`, `:1184` (a dynamic collection's genre filter) and the scrapers
- **What:**
  - `fromGenreName` looks a name up whole (`:295`); on a miss it tries each part after `/` and, on a hit, returns `mGenres[g->second]` (`:305`), where `g` is the whole name's end iterator, not the part's `sg`. That is undefined behaviour: a wrong genre or a crash.
  - `:299`'s `name.find("/") >= 0` is always true (`size_t`).
  - The floor's 3.8 also finds a parent genre counted twice for a game with two of its children (`Genres.cpp:244-248`, `FileFilterIndex.cpp:1015-1016`).
- **Fix shape:**
  - `mGenres[sg->second]` at `:305`; `!= std::string::npos` at `:299`; a unit case over a document seam (3.8's).
- **Can this be done on the VM?** Yes. A unit case in `es-unit-tests` over a genre table; it FAILs at the pin under ASan.
- **Already written:** nothing inherited: a filter's `.xcc` stores the genre by name and is read the same way after the fix.
- **Acceptance:**
  - [ ] A unit case `fromGenreName("Foo / <a known subgenre>")` returns that subgenre's entry; at the pin, under ASan, it reports the end-iterator read (`stage-e/` records).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6 (one token), with the double count recorded?
- **Bug:** #1274 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-05: a custom collection's list and a dynamic collection's filter are written in place, and ES's own writes leave the file cache stale (a `bug` proposed; upstream's writers, settings tier)

- **Severity:** Medium
- **Category:** Reliability
- **Question:** Q4
- **Family:** a write with no last good copy; a read of a file another process writes
- **Source Finding:** L-23, the third cache shape, EP-19, EP-43 -- proved: tool-run (`t33-writes.py`, `t33-reads.py`)
- **Owner area:** `es-app/src/CollectionSystemManager.cpp:340-358` (`std::ofstream`, `:345`), `:1610`, `:1613`, `:963`; `FileFilterIndex.cpp:1313` (`pugi::save_file`), `:1144`
- **What:**
  - Both files are in the settings tier backuptool archives, written in place: `custom-<name>.cfg` by `std::ofstream` with no error check (`:345`), the `.xcc` by pugixml (`:1313`). A cut `.cfg` reads as a shorter collection, which the next save writes back; a cut `.xcc` is a parse error, and the collection is left **empty** (`:1114-1124`; EP-19).
  - Neither writer goes through `Utils::FileSystem`, so a path whose miss the cache remembered (`:963`) stays absent: `deleteCustomCollection` (`:1609-1614`) falls to the `.cfg`, or returns false.
  - **EP-43:** the filter page discards `save()`'s result and closes as saved (`GuiGamelistFilter.cpp:262-270`).
- **Fix shape:**
  - both writes temp-and-rename with the cache entry dropped explicitly (`FileSystemUtil.cpp:348-350`'s reset, EP-19); the delete's checks uncached; the page keeps its choices and says so when `save()` fails (EP-43).
- **Can this be done on the VM?** Yes. A file case over a temp folder for each writer (the floor's 3.11 shape), and the delete after a create in one session on the guest.
- **Already written:** a `custom-<name>.cfg` or `.xcc` already cut on a device reads as it does today, a shorter list or no filter; the fix changes the write, not the read: nothing to migrate.
- **Acceptance:**
  - [ ] A file case kills the write half-way (a writer double) and the previous file is what remains; at the pin the cut file remains (`stage-e/`).
  - [ ] On the integration image, a custom collection created and deleted in one session leaves no `custom-<name>.cfg` (a `vm-serial` listing in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6, one stream with PL-01's helper?
- **Bug:** #1275 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-06: NetworkThread posts straight to the window, past the closing gate the fork wrote for exactly this (a `bug` proposed; the fork's file)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-12 -- proved: fixture (`stage-c/l12-network-posts.py`)
- **Owner area:** `es-app/src/NetworkThread.cpp:206`, `:237`, `:251`, `:257`, `:266`; `AppWindow.h:38-45`; `main.cpp:1322`, `:1330`
- **What:**
  - `AppWindow::post` drops a worker's post once `main()` calls `AppWindow::closing()` (`main.cpp:1322`, F-ES-26). NetworkThread's watchers run until `WatchersManager::stop()` (`:1330`), and its five posts call `mWindow->postToUiThread` directly: a check that ends between the two lines queues a task no loop runs, `:266`'s token write among them.
  - **EP-7:** this is a closing-protocol violation, not a dangling write; routing the posts through the gate drops a completed token write rather than saving it, so the stream states the drain policy.
- **Fix shape:**
  - the five posts through `AppWindow::post(mWindow, ...)`.
- **Can this be done on the VM?** Yes. The fixture's count and run against the fixed file.
- **Already written:** nothing inherited: a lost task writes nothing.
- **Acceptance:**
  - [ ] `stage-c/l12-network-posts.py` against the fixed `NetworkThread.cpp` prints `0 direct post(s)` (rc 0), and against the pin `5 direct post(s) at :206, :237, :251, :257, :266` (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug` (the fork's own rule), noting T20's hasher-start lines `:248`, `:251`?
- **Bug:** #1276 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

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
- **Bug:** #1277 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

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
- **Bug:** #1278 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-09: a ROM tagged `(India)` reads no language or region: the table's token is `ìndia` (a `bug` proposed; upstream's)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q5
- **Family:** a check whose failure reads as success
- **Source Finding:** L-26, 3.31 -- proved: fixture (`stage-c/l331-lang-india.py`)
- **Owner area:** `es-app/src/LangParser.cpp:65`
- **What:**
  - Tags are lowercased before `extractLang` (`:150`); `india` never equals `ìndia` (U+00EC), so only `in` matches.
- **Fix shape:**
  - the token `india`.
- **Can this be done on the VM?** Yes. The fixture against the fixed file.
- **Already written:** nothing inherited: the language is derived at load, not stored.
- **Acceptance:**
  - [ ] `stage-c/l331-lang-india.py` against the fixed file reads `india -> lang [in] region [in]` (rc 0).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, rule 6, a #585 line?
- **Bug:** #1279 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

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
- **Bug:** #1280 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-11: a 64-bit id or epoch in the proxy's list is truncated to `int` (a `bug` proposed; the fork's helper)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-17, the floor's 3.41 -- proved: tree (`stage-c/floor.md`)
- **Owner area:** `es-app/src/OfflineAchievementsText.cpp:17-20` (`jsonInt`), `:230`
- **What:**
  - `jsonInt`'s `(int)v.GetInt64()` narrows an id (`:17-20`), and the id fields are `int`. The epoch is `time_t` via `strtoll` (`:229-231`; EP-12: the first reader had it as `int`). Out-of-range input needs a defined outcome.
- **Fix shape:**
  - `int64_t` through, with an `OfflineAchievementsTextTests.cpp` case above 2^31 (T20's delta on the same file named as a collision).
- **Can this be done on the VM?** Yes. A case in `es-unit-tests`.
- **Already written:** nothing inherited: the ids are read from the proxy each time.
- **Acceptance:**
  - [ ] A new `OfflineAchievementsTextTests.cpp` case with an id above 2^31 FAILs at the pin and passes on the fix (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, or deferred to T20's file?
- **Bug:** #1281 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-12: a key map's refused trigger drops the whole mapping with no word, and the loader reads strings unchecked (upstream's loader, outside the lanes)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-28, 3.21, EP-10 -- proved: fixture (`stage-c/l321-keys-parse.py`); guest (G-08)
- **Owner area:** `es-app/src/KeyboardMapping.cpp:217-300` (`:262-272`, `:293-294`; `GetString` with no `IsString` at `:247-288`)
- **What:**
  - A trigger `checkTriggerExists` refuses is skipped, and a mapping with no trigger is dropped (`:293-294`): the editor shows the rest and says nothing.
  - **EP-10:** under NDEBUG, `GetString` with no `IsString` at `:251`, `:254`, `:257` (type, mode, description), `:265-266`, `:271-272` (triggers) and `:282-283`, `:288-289` (targets), and no `IsObject` before `HasMember` (`:246-250`), are undefined behaviour on a hand-edited file. The `GetArray` calls are guarded. A chord with one unknown trigger loses it and changes meaning.
- **Fix shape:**
  - a log line naming the dropped trigger (the fixture's control), and shape before every `GetString`.
- **Can this be done on the VM?** Yes. The fixture against the fixed file; G-08 on the integration image.
- **Already written:** nothing inherited: `.keys` files are read the same way; the fix adds a line, not a format.
- **Acceptance:**
  - [ ] `stage-c/l321-keys-parse.py` against the fixed file prints the log line naming `t33unknown` (rc 0).
- **Disposition (proposed for the stage-D pause):** question: a `bug` under rule 6 (memory safety on a player file, EP-10), or recorded with a #585 line (outside the lanes)?
- **Bug:** #1282 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-13: the filter's rating and year keys: a positive rating reads 0 STARS, a year outside 1000-2999 reads nothing, and `1 STARS` (upstream's filter, outside the lanes)

- **Severity:** Low
- **Category:** Words
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-27, 3.9 -- proved: fixture (`stage-c/l309-rating-year.py`)
- **Owner area:** `es-app/src/FileFilterIndex.cpp:322-340`, `:364-369`
- **What:**
  - `0.05` rounds to `0 STARS` where `""` and `"0"` read UNKNOWN; `3000…` and `0999…` read `""`; the label for one star is `1 STARS`.
  - **EP-11:** the cases' rule (one star for any positive rating; any four digits a year) is a proposed policy, and `1 STARS` is an index key whose display is not yet read.
- **Fix shape:**
  - a floor of one star for a positive rating; four digits for a year; the label's singular.
- **Can this be done on the VM?** Yes. The fixture against the fixed file.
- **Already written:** nothing inherited: the keys are derived at load.
- **Acceptance:**
  - [ ] `stage-c/l309-rating-year.py` against the fixed file prints no `(want ...)` line (rc 0).
- **Disposition (proposed for the stage-D pause):** question: recorded with a #585 line (outside the lanes), or a `bug`?
- **Bug:** #1291 (filed 2026-10-27, with its code trace; ruled 20:15 UTC)

## PL-14: closing a RetroAchievements page waits on the watcher lock while a network check holds it (es-core's lock, the fork's callers)

- **Severity:** Medium
- **Category:** Performance
- **Question:** Q2
- **Family:** a call with no bound
- **Source Finding:** L-01 -- proved: tree (the read trace; G-09 `CANNOT`)
- **Owner area:** `es-core/src/watchers/WatchersManager.cpp:80-100`, `:181-199` (T21's file); `NetworkThread.cpp:21-25` <- `guis/GuiRetroAchievementsSettings.cpp:805-806` and `NetworkThread.cpp:257` (EP-13: the brief's `:191` is a comment and `:257` a weak-pointer test)
- **What:**
  - The interface thread's `ResetComponent` takes `mWatchersLock`, which the watcher thread holds across every `check()`, a network login among them: a page close waits out the check.
- **Fix shape:**
  - `check()` run outside `mWatchersLock` with the registry's lifetime kept (unregistering deletes the `WatcherInfo`, `:80-86`; EP-13), or `nextCheckTime` under a lock of its own (rule 6, T21's file named).
- **Can this be done on the VM?** No case without SDL; the bound's arithmetic and the trace are the proof.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] The stream's record shows `check()` called with `mWatchersLock` released (a line-cited read of the fixed `WatchersManager.cpp` in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug` under rule 6 in es-core (T21's file), or routed to the es-core slice?
- **Bug:** #1283 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

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
- **Bug:** #1284 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-16: the other in-place writers: the rotation record, the key maps, and `saveToXml`'s remove-then-save (Backlog #1186's sites)

- **Severity:** Medium
- **Category:** Reliability
- **Question:** Q4
- **Family:** a write with no last good copy
- **Source Finding:** L-03, T21 PL-20 -- proved: tool-run (`t33-writes.py`)
- **Owner area:** `es-app/src/CaptureRotation.cpp:175`, `KeyboardMapping.cpp:426`, `:429`, `Gamelist.cpp:307-308`
- **What:**
  - `writeAllText` in place, its result unread (`CaptureRotation.cpp:175`, `KeyboardMapping.cpp:426`, `:429`), and remove-then-save with no file between (`Gamelist.cpp:307-308`; EP-3: a failed save destroys the previous recovery record).
- **Fix shape:**
  - #1186's helper, when it lands, at these four lines.
- **Can this be done on the VM?** Yes, as #1186 states.
- **Already written:** a cut `.rotation` reads as untrusted (`:124`), a cut `.keys` as an empty map, a cut recovery file as no recovery: each falls to the safe reading.
- **Acceptance:**
  - [ ] #1186's acceptance names these four lines.
- **Disposition (proposed for the stage-D pause):** question: deferred to #1186, these lines added to it?
- **Bug:** #1285 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-17: the map describes neither filter page nor UPDATE GAMELISTS, and the map check cannot see member-initialized titles (required: D-UI-039)

- **Severity:** Medium
- **Category:** Documentation
- **Question:** Q7
- **Family:** a page the map does not describe
- **Source Finding:** Q7, the brief's § 7 -- proved: tool-run (`es-menu-map-check`'s line; the grep's 0 hits)
- **Owner area:** `docs/es-menu-map.md`; `tools/es-menu-map-check:49-56`; `guis/GuiGamelistFilter.cpp:11`, `:17`; `guis/GuiMenu.cpp:5756`; `guis/GuiCollectionSystemsOptions.cpp:368`
- **What:**
  - The proposed text is in `02` § The structure: UPDATE GAMELISTS has **one** handheld home, GAME SETTINGS > TOOLS; the collection-settings entry is Windows-only (`GuiCollectionSystemsOptions.cpp:366-369`; EP-25). The check reads three title shapes and misses `mMenu(window, _("..."))` in a member initializer (#951/#965's class); the fourth pattern's census is rerun (EP-26).
- **Fix shape:**
  - the rows added by the coordinator's stage-E stream, in the same commit as any row it touches; the fourth pattern for the coordinator.
- **Can this be done on the VM?** Yes: the check and the grep on the tree.
- **Already written:** nothing inherited: documentation.
- **Acceptance:**
  - [ ] `grep -c -E 'FILTER GAMELIST BY|EDIT DYNAMIC COLLECTION FILTERS|UPDATE GAMELISTS' docs/es-menu-map.md` prints 3 or more, the UPDATE GAMELISTS row names GAME SETTINGS > TOOLS alone, and `tools/es-menu-map-check` prints `0 missing`.
- **Disposition (proposed for the stage-D pause):** question: the stream at stage E as the brief says; the check's pattern to #951/#965?

## PL-18: the floor's smaller upstream defects (recorded; upstream's)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** the floor's 3.1, 3.3 (the prefix case), 3.4, 3.5, 3.10's aside, 3.14, 3.32, 3.34; 3.20's sibling; EP-27 to EP-35 -- proved: tree (`stage-c/floor.md`)
- **Owner area:** `PlatformId.cpp:28`, `:171`; `MetaData.cpp:303`, `:313`, `:392-404`, `:568`; `FileFilterIndex.cpp:579-580`; `Gamelist.cpp:177`; `CollectionSystemManager.cpp:627-651`, `:1510`; `CustomFeatures.cpp:531`, `:536`; `FileSorts.cpp:38`; `LangParser.cpp:225-226`; `SystemRandomPlaylist.cpp:28-30`; `FolderMerge.h:50-52`; `FileData.cpp:1659` (outside the slice)
- **What:**
  - Each in `stage-c/floor.md` with its input. The two with a player cost: a scrape blanks a filled field it did not return (3.5, `MetaData.cpp:568`), and `<sys>.sort=28` throws at `FileData.cpp:1659` (T2 FD-15's sibling, #771).
  - **Removed by the seat as not defects:** 3.26 (EP-30), 3.28 (EP-31), 3.37 (EP-32); 3.16 and 3.17 narrowed to preconditions (EP-28, EP-29); 3.3's default omission is a contract (EP-27); 3.10's empty/empty is 0 (EP-33).
- **Fix shape:**
  - each recorded with a #585 line; 3.20's sibling to #771.
- **Can this be done on the VM?** Yes, each as a unit case.
- **Already written:** nothing inherited by recording.
- **Acceptance:**
  - [ ] `02` § The #585 lines owed carries a line for each of 3.5 and 3.8's double count, and #771 carries `FileData.cpp:1659` (a comment link in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: recorded, 3.5 raised to a `bug`, and `FileData.cpp:1659` to #771?
- **Bug:** #1292 for 3.5 alone (filed 2026-10-27, with its code trace; ruled 20:15 UTC); the rest recorded as listed

## PL-19: the surfaces outside the lanes: Zaparoo's unbounded probe, the installer's and Bluetooth's self-deleting workers and tool-text toasts, the screensaver's cached reads and launch, the scraper search's words (recorded; D-UI-079)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a call with no bound
- **Source Finding:** L-09, L-10, L-11, L-02, L-04, the take-up row T2 `:293-294`, `02` § The words, EP-14 to EP-17, EP-45, EP-47 -- proved: tool-run, tree, guest (G-06)
- **Owner area:** `ZaparooSupport.cpp:32-39`, `:58-63`; `ContentInstaller.cpp:61`, `:144-236`; `ThreadedBluetooth.cpp:19-110`; `SystemScreenSaver.cpp:156-164`, `:546`; `components/ScraperSearchComponent.cpp:386`, `:468`; `CaptureRotation.cpp:162`; `DisplayAspect.cpp:74-87`
- **What:**
  - Each in `02` with its lines: no bound past the connect; `delete this` on a worker; `AN ERROR OCCURRED: <status>`; ten retries over a cached miss; the screensaver's launch skipping the format and BIOS checks (keeping the cloud gate); an English dialog outside `_()`; `retroarch.cfg` read on every exit; the screenshot walk.
  - **EP-45:** Zaparoo's card write is `req.wait()` alone, and the name is inserted raw into JSON (`ZaparooSupport.cpp:58-63`). **EP-47:** Bluetooth's worker, started in the constructor, can delete itself (`ThreadedBluetooth.cpp:39-47`) before `start()` publishes it (`:58`). **EP-14:** L-02's log read has no size bound.
- **Fix shape:**
  - recorded, with #585 lines; L-02 and L-04 priced by the integration image's time-to-play.
- **Can this be done on the VM?** Partly: G-06 ran; the rest are reads.
- **Already written:** nothing inherited by recording.
- **Acceptance:**
  - [ ] `02` § The #585 lines owed carries the recorded row naming these files.
- **Disposition (proposed for the stage-D pause):** question: recorded as listed, or EP-47's publication race (a use-after-free) raised to a `bug` under rule 6?
- **Bug:** #1290 for EP-47 alone (filed 2026-10-27, with its code trace; ruled 20:10 UTC); the rest recorded as listed

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

## PL-21: a malformed unlocks reply reads as known, empty progress (a `bug` proposed; the fork's helper, the offline achievements lane)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** EP-42 -- proved: tree (`OfflineAchievementsText.cpp:183-200`, the first reader's read)
- **Owner area:** `es-app/src/OfflineAchievementsText.cpp:183-200` (`parseUnlocks`), `:99-112`, `:120-148`; `OfflineAchievementsText.h:84-90`
- **What:**
  - `parseUnlocks` rejects only a boolean-false `Success` (`:187`); a missing or non-bool one passes, every invalid list entry is skipped, and `ok = true` (`:199`): `{"Success":"false","UserUnlocks":[{}]}` reads as known with no unlocks, against the header's own contract (`.h:84-90`). The patch and set readers set `ok` without the `Success` check (`:99-112`, `:120-148`).
- **Fix shape:**
  - `Success` required true and boolean; a list whose entries are all invalid is not `ok`; the documented all-unofficial set kept (`.h:75-76`); cases in `OfflineAchievementsTextTests.cpp` (T20's delta named as a collision).
- **Can this be done on the VM?** Yes. Cases in `es-unit-tests`.
- **Already written:** nothing inherited: a reply is parsed when it arrives; a wrongly empty reading is replaced by the next good reply.
- **Acceptance:**
  - [ ] New `OfflineAchievementsTextTests.cpp` cases (a missing `Success`, a string `Success`, a list of only invalid entries) FAIL at the pin and pass on the fix (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug` (the fork's lane), or T20's file?
- **Bug:** #1286 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-22: `FileFilterIndex::resetIndex` clears copies of its indexes, so a reset keeps every old key (a `bug` proposed; upstream's filter)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** EP-44 -- proved: tree (`FileFilterIndex.cpp:148-162`, `:1102-1105`)
- **Owner area:** `es-app/src/FileFilterIndex.cpp:1102-1105` (`clearIndex`), `:154-162` (`resetIndex`, nine facets); caller `CollectionSystemManager.cpp:1114`
- **What:**
  - `clearIndex(std::map<std::string, int> indexMap)` takes the map by value and clears the copy. `resetIndex` calls it for every facet, so a dynamic collection's repopulate (`:1114`) and every other reset keep the old keys and counts: the filter pages offer values no game has.
- **Fix shape:**
  - `clearIndex(std::map<std::string, int>& indexMap)`; a unit case over a populated index.
- **Can this be done on the VM?** Yes. A unit case; a frame of FILTER GAMELIST BY after a reset on the integration image.
- **Already written:** nothing inherited: the index is built in memory.
- **Acceptance:**
  - [ ] A unit case populates an index, calls `resetIndex`, and asserts the facet maps are empty; it FAILs at the pin (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug` under rule 6 (one character), a #585 line?
- **Bug:** #1287 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-23: a token check in flight writes the token back after the player turned achievements off (a `bug` proposed; the fork's NetworkThread, the achievements lane)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** EP-39 -- proved: tree (`NetworkThread.cpp:260-272`, `GuiRetroAchievementsSettings.cpp:793-799`)
- **Owner area:** `es-app/src/NetworkThread.cpp:130-138`, `:260-272`; `guis/GuiRetroAchievementsSettings.cpp:795-796`
- **What:**
  - The check snapshots the credentials, signs in, and posts only the returned token; the interface writes it (`:266-270`) with no account or generation check. Turning achievements off clears the token (`GuiRetroAchievementsSettings.cpp:795-796`); a check already running writes it back.
- **Fix shape:**
  - the result carries the account and a settings generation, and is dropped when either changed; with PL-06's gate.
- **Can this be done on the VM?** Yes, with a blocked sign-in double in a harness over the two functions (`fixture`).
- **Already written:** a token written back on a device after a disable stays in `system.cfg` until the next disable or sign-in; the fix's next check overwrites it.
- **Acceptance:**
  - [ ] A fixture blocks the sign-in, clears the token, releases the old result, and asserts the token stays empty; it FAILs at the pin (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug` (the fork's lane), with PL-06 in one stream?
- **Bug:** #1288 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-24: the rotation record is cached as written though the write is unchecked, and the cache is keyed by mtime alone (a `bug` proposed; the fork's helper)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a read of a file another process writes
- **Source Finding:** EP-40, EP-41, L-03 -- proved: tree (`CaptureRotation.cpp:100-110`, `:174-181`)
- **Owner area:** `es-app/src/CaptureRotation.cpp:100-110` (`read`'s `sKnownAt`), `:174-181` (`write`)
- **What:**
  - **EP-40:** `writeAllText`'s result is not read; the new turns are cached with the destination's mtime (`:179-180`), so a failed write reads as the new rotation until restart.
  - **EP-41:** `sKnownAt` answers by mtime alone (`:103-108`), before the uncached probe: a record replaced (by the cloud's saves tier) with the same mtime returns the old turns.
- **Fix shape:**
  - cache only after a checked write; key the cache by mtime and size (or reread the few bytes); with PL-16's helper for the write.
- **Can this be done on the VM?** Yes. A fixture over `read` and `write` with a failing write double and a same-mtime replacement.
- **Already written:** nothing inherited: the cache is in memory; a record on disk is read the same way.
- **Acceptance:**
  - [ ] A fixture with a failing write and one with a same-mtime replacement each FAIL at the pin and pass on the fix (`stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: a `bug`, or with PL-16 under #1186?
- **Bug:** #1289 (filed 2026-10-27, with its code trace; ruled 20:10 UTC)

## PL-25: the screensaver keeps `FileData` pointers the rescan does not retire (a lead; upstream's screensaver, outside the lanes)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** EP-38, EP-8 -- proved: tree (a lead; the retirement paths outside the packet)
- **Owner area:** `es-app/src/SystemScreenSaver.cpp:342-358`, `:378-380`, `:538-548`; `SystemData.cpp:459-473` (outside the slice)
- **What:**
  - The media list and `mCurrentGame` hold raw `FileData*`; the rescan's retirement shown removes collection and group holders, not the screensaver's. Not reproduced.
- **Fix shape:**
  - the screensaver's holders on L-15's retirement checklist; or the screensaver stores paths, as `DisplayAspect` does.
- **Can this be done on the VM?** Yes: prime the screensaver, remove a ROM, rescan, select its media under an ASan build (an image with ASan is not available; a fixture first).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] A read of the rescan's invalidation paths names whether the screensaver's list is cleared (`stage-e/`), and a fixture follows if it is not.
- **Disposition (proposed for the stage-D pause):** question: recorded as a lead for the rescan's owner?
- **Bug:** #1305 (filed 2026-10-30 at acceptance, with its code trace; the coordinator's ruling, #680 comment 6525495300)

## PL-26: a mouse-only key map loads and saves but is called invalid (recorded; upstream's, outside the lanes)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** EP-46 -- proved: tree (`KeyboardMapping.cpp:499-509`)
- **Owner area:** `es-app/src/KeyboardMapping.cpp:178-181`, `:293-294`, `:499-509`; `guis/GuiGamelistOptions.cpp:262-267`
- **What:**
  - A mouse mapping needs no targets and is accepted by the loader and writer, but `isValid()` requires targets on some mapping, so a file of mouse mappings alone is invalid and its information row is hidden.
- **Fix shape:**
  - `isValid()` accepts a mouse mapping with a trigger.
- **Can this be done on the VM?** Yes. A unit case.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `02` § The #585 lines owed carries this item's line (a grep in `stage-e/`).
- **Disposition (proposed for the stage-D pause):** question: recorded with a #585 line?

## Phase 7 resolution gate

Stage E's hand-back, 2026-10-30: every item at its outcome, the table and the index rewritten together from `stage-c/punch-items.py`'s `RES`. The ES commits are on `feature/m6-es-app-system-680` (pixelelated/emulationstation), fixed-at-es `f802c55c6`; each stream's before, after and checks are under `stage-e/`, the tip's are `stage-e/handback-checks.txt`, and `02` § The streams carries one row per stream.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Resolved | Resolved in `d0d92dda6` (ES, S1a: read uncached, parse before write, temp-and-rename, the recovery kept) and `dd86d7ce2` (S1b: the changed fields laid over the file's entry, D-CLOUD-187) under #1271; `getGamelistPath`'s two tokens are `stage-e/patches/s1a-SystemData-getGamelistPath.patch` for T2's file (ruling 1); EP-36's lost update recorded; a #585 line |
| PL-02 | Resolved | Resolved in `4e9a7d166` (ES, S2) under #1272: the holders' views dropped before the clear and remade after (#246's pair); Medium stands, the non-bundled route does not fault (ruling 10); a #585 line |
| PL-03 | Resolved | Resolved in `d370ac62e` (ES, S5) under #1273: the builder owns and joins its thread, copies its params, takes the second search; the join's bound named in `stage-e/s5-checks.txt`; a #585 line |
| PL-04 | Resolved | Resolved in `0b369b44b` (ES, S3) under #1274: `npos` at `:299` and the part's entry at `:305` (the line corrected); 3.8's double count recorded; a #585 line |
| PL-05 | Resolved | Resolved in `4e9a7d166` (ES, S2) under #1275: the custom list and the dynamic filter written temp-and-rename, the delete's reads uncached; EP-43's page half is `stage-e/patches/s2-GuiGamelistFilter-save-result.patch` for T31's file (ruling 4); a #585 line |
| PL-06 | Resolved | Resolved in `b902cc8ba` (ES, S4a) under #1276: the five posts through `AppWindow::post`, the drain policy in the file's comment |
| PL-07 | Resolved | Resolved in `f802c55c6` (ES, S6) under #1277: three anchors, EN COURS, ABANDONNÉ, EN PAUSE; the French frames are an open item to test at the integration window; a #585 line |
| PL-08 | Resolved | Resolved in `0b369b44b` (ES, S3) under #1278: the floor counts characters, a fourth `TextFitTests` case |
| PL-09 | Resolved | Resolved in `0b369b44b` (ES, S3) under #1279: the token `india` (the lowercasing is `:150`, corrected); a #585 line |
| PL-10 | Resolved | Resolved in `a5273390e` (ES, S4b) under #1280: argv[0]'s base name, or the script after sh or bash (the ctl is #!/bin/bash); two `RunLockTests` cases |
| PL-11 | Resolved | Resolved in `a5273390e` (ES, S4b) under #1281: the ids 64-bit, an out-of-range pending id dropped (the id is `:230`, corrected); T20's collision named, no shared line |
| PL-12 | Resolved | Resolved in `0b369b44b` (ES, S3) under #1282: shapes checked before `GetString`, a refused trigger logged and named (the drop is `:293-294`, corrected); the toast's call is `stage-e/patches/s3-GuiKeyMappingEditor-refused-keys.patch` for T31's file (ruling 2); a #585 line |
| PL-13 | Resolved | Resolved in `0b369b44b` (ES, S3) under #1291: one star at least, four digits, a stored `0 STARS` read as `1 STARS` (ruling 3, #1291's line edited; `:322`, corrected); a #585 line |
| PL-14 | Resolved | Resolved in `b902cc8ba` (ES, S4a) under #1283, the fork's half: the sign-in on a worker the component owns, `check()` quick under the lock; the update check and the lock's own shape recorded for the es-core slice (ruling 7), #1283 keeps that checkbox open; a #585 line for es-core |
| PL-15 | Resolved | Resolved in `a5273390e` (ES, S4b) under #1284: DONE only on rc 0 with an OK line and no why (ruling 9); the why through CloudText, 124 STOPPED ANSWERING; the script's half needs no line |
| PL-16 | Resolved | Resolved in `d0d92dda6` (ES, S1a: `saveToXml`) and `a5273390e` (S4b: the rotation record and the key maps) under #1285: temp-and-rename, a killed write leaves the previous file whole |
| PL-17 | Resolved | Resolved in `75f696b22d` (distribution, S7) for #1270's checkbox 17: UPDATE GAMELISTS and `## Game list filters`; `es-menu-map-check` 0 missing, the grep 5; the checker's blind spot is the coordinator's note on #965 |
| PL-18 | Resolved | Resolved in `0b369b44b` (ES, S3) under #1292 for 3.5 (the scrape leaves a field it did not return); the rest are #585 lines in `02`; 3.20's sibling to #771 (`stage-e/comment-links.md`) |
| PL-19 | Resolved | Resolved in `d370ac62e` (ES, S5) under #1290 for EP-47 (the scan published under a lock, the formatter too); the remainder are #585 lines in `02`, recorded (D-UI-079) |
| PL-20 | Deferred | Deferred: #1235 -- `ScraperCmdLine.{cpp,h}` named there (`stage-e/comment-links.md`); the Windows residue one row each in `02` § The structure (D-WORKFLOW-209) |
| PL-21 | Resolved | Resolved in `a5273390e` (ES, S4b) under #1286: Success present, boolean and true; a list of only invalid ids not ok |
| PL-22 | Resolved | Resolved in `4e9a7d166` (ES, S2) under #1287: `clearIndex` by reference (`resetIndex` `:148-162`, corrected); a #585 line |
| PL-23 | Resolved | Resolved in `b902cc8ba` (ES, S4a) under #1288: the answer applied only to the credentials it was asked with and only while the switch is on; the save tests the switch and the account; no generation (ruling 5: sameacct passes) |
| PL-24 | Resolved | Resolved in `a5273390e` (ES, S4b) under #1289: the turns cached only after a checked write; the record known by mtime to the nanosecond, size and inode |
| PL-25 | Deferred | Deferred: #1305 -- filed at acceptance on the coordinator's ruling (#680 comment 6525495300), Medium proposed: the list is not cleared on the transfer's rescan, `stage-c/pl25-screensaver.py` FAILs at the pin and the tip (`stage-e/pl25-read.txt`); the fix is the integration's (`SystemData.cpp`, a `stage-e/` patch for T2's file) and T35's (`Window.cpp`); #585 line 21 |
| PL-26 | Deferred | Deferred: #585 -- recorded, line 18 of `02`'s stage-E table |

```yaml
punch_index:
- id: PL-01
  severity: "High"
  category: Correctness
  question: Q4
  source_finding: "L-05, 3.13, 3.15, EP-1, EP-2, EP-36"
  outcome: "resolved"
- id: PL-02
  severity: "Medium"
  category: Correctness
  question: Q1
  source_finding: "L-06, T32 L-16, EP-5, EP-37, EP-38"
  outcome: "resolved"
- id: PL-03
  severity: "Medium"
  category: Correctness
  question: Q1
  source_finding: "L-07, L-08"
  outcome: "resolved"
- id: PL-04
  severity: "Medium"
  category: Correctness
  question: Q3
  source_finding: "the floor's 3.8 [re-read], 3.11"
  outcome: "resolved"
- id: PL-05
  severity: "Medium"
  category: Reliability
  question: Q4
  source_finding: "L-23, the third cache shape, EP-19, EP-43"
  outcome: "resolved"
- id: PL-06
  severity: "Medium"
  category: Correctness
  question: Q1
  source_finding: "L-12"
  outcome: "resolved"
- id: PL-07
  severity: "Medium"
  category: Words
  question: Q5
  source_finding: "L-25, 3.29"
  outcome: "resolved"
- id: PL-08
  severity: "Low"
  category: Words
  question: Q5
  source_finding: "L-20, 3.35, T20 S9"
  outcome: "resolved"
- id: PL-09
  severity: "Low"
  category: Correctness
  question: Q5
  source_finding: "L-26, 3.31"
  outcome: "resolved"
- id: PL-10
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-14, the floor's 3.38"
  outcome: "resolved"
- id: PL-11
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-17, the floor's 3.41"
  outcome: "resolved"
- id: PL-12
  severity: "Medium"
  category: Correctness
  question: Q3
  source_finding: "L-28, 3.21, EP-10"
  outcome: "resolved"
- id: PL-13
  severity: "Low"
  category: Words
  question: Q3
  source_finding: "L-27, 3.9"
  outcome: "resolved"
- id: PL-14
  severity: "Medium"
  category: Performance
  question: Q2
  source_finding: "L-01"
  outcome: "resolved"
- id: PL-15
  severity: "Low"
  category: Words
  question: Q3
  source_finding: "L-18"
  outcome: "resolved"
- id: PL-16
  severity: "Medium"
  category: Reliability
  question: Q4
  source_finding: "L-03, T21 PL-20"
  outcome: "resolved"
- id: PL-17
  severity: "Medium"
  category: Documentation
  question: Q7
  source_finding: "Q7, the brief's § 7"
  outcome: "resolved"
- id: PL-18
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "the floor's 3.1, 3.3 (the prefix case), 3.4, 3.5, 3.10's aside, 3.14, 3.32, 3.34; 3.20's sibling; EP-27 to EP-35"
  outcome: "resolved"
- id: PL-19
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-09, L-10, L-11, L-02, L-04, the take-up row T2 `:293-294`, `02` § The words, EP-14 to EP-17, EP-45, EP-47"
  outcome: "resolved"
- id: PL-20
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-21, L-22"
  outcome: "deferred"
- id: PL-21
  severity: "Medium"
  category: Correctness
  question: Q3
  source_finding: "EP-42"
  outcome: "resolved"
- id: PL-22
  severity: "Medium"
  category: Correctness
  question: Q3
  source_finding: "EP-44"
  outcome: "resolved"
- id: PL-23
  severity: "Medium"
  category: Correctness
  question: Q1
  source_finding: "EP-39"
  outcome: "resolved"
- id: PL-24
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "EP-40, EP-41, L-03"
  outcome: "resolved"
- id: PL-25
  severity: "Medium"
  category: Correctness
  question: Q1
  source_finding: "EP-38, EP-8"
  outcome: "deferred"
- id: PL-26
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "EP-46"
  outcome: "deferred"
```
