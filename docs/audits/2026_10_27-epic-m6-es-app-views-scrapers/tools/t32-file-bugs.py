#!/usr/bin/env python3
"""T32 (#679): the titles and bodies of the twelve bugs the stage-D ruling names, from 05-punch-list.md
(T31's t31-file-bugs.py, adapted: filed before the stream brief, so each carries its own code trace).

    python3 -I t32-file-bugs.py <05-punch-list.md> <out dir>

Writes <out dir>/PL-NN.title and PL-NN.md. A body is: an introduction, the
item's section of 05 copied (its family, owner area, fix shape, VM line,
Already written line, acceptance and the ruling), then a code trace in four
parts -- how it was found, the defect at its source at the pin, the siblings
hunted, and what reading cannot prove -- then the acceptance every T32 bug
shares. Asserts twelve bugs, each with a trace.
"""
import os, re, sys

PLS = ["PL-01", "PL-02", "PL-03", "PL-04", "PL-05", "PL-07", "PL-08", "PL-10", "PL-17", "PL-18", "PL-21", "PL-22"]
TRACE = {
 "PL-01": ("L-01 at stage B (the unlocked static); `stage-c/l02-stop-after-finish.py` at stage C (a heap-use-after-free at the pin; `--plain` prints cancelled 1 over finished 1); the seat's EP-6 (the interleaving is natural), EP-7 (the lock is not enough), EP-34 and EP-37.",
           "`ThreadedScraper.cpp:323-337`: `stop()` copies `mInstance` (`:325`), marks `cancelled` under `sProgressMutex`, then writes `thread->mExitCode` (`:335`) with no check that the run is alive. `run()` publishes `finished` (`:232-238`), then `delete this` (`:241`). `Process()` publishes `running` before its first searches (`:35-50`), and `start()`'s catch deletes the instance without finalizing it (`:308-316`). `mHandle = new std::thread(...)` (`:53`) is assigned after the worker may already have run.",
           "`isRunning()` (`ThreadedScraper.h:77`) and its API caller (`HttpServerThread.cpp:306`); `mPaused` (`:181`); the CANCEL dialog's YES (`GuiScraperRun.cpp:110-116`, T31's) calls `stop()` without rechecking `finished`; `main.cpp:1332` calls `stop()` at exit (teardown order to read, outside the slice).",
           "The device timing of a press in the frame the last game ends; the harness widens the window with a named hook, and EP-6 shows the order needs none. EP-34's publication race is read, not run."),
 "PL-02": ("3.13 at stage B; G-05 on the guest (ten games, link down: COMPLETED, GAMES SCRAPED: 9); `stage-c/l313-request-outcome.py` and `l316-igdb-contract.py` FAIL at the pin; the floor's 3.19 (re-read) explains the 9; the seat's EP-1 to EP-5 and EP-36.",
           "`Scraper.cpp:372-376` makes `REQ_IO_ERROR` an ignored error (a631e8c84); `:343-347` and `:351-360` make a spent or long 429 `ASYNC_DONE`; `:337` drops `process()`'s return. `ThreadedScraper.cpp:248-256` sets `done` only at hand-out. The media handle (`:607-614`, `:631-635`, `:669-688`) treats 404, IO, a spent 429, a failed rename and a failed resize as DONE. `IGDBScraper.cpp:169-175` and `HfsDBScraper.cpp:214-220` return an empty queue on a manual token failure.",
           "ScreenScraper's \"maximum threads per minute reached\" `false` (`ScreenScraper.cpp:383-384`, outside the 42) is dropped at `:337`. A dependency request's 404 discards the primary results (EP-1). #1205 (T21 PL-17) owns the HTTP-date `Retry-After`. The reader's fatal list (`ThreadedScraper.cpp:157-159`) does not include codes 3 or 429, so `setError` keeps a batch running.",
           "Whether a failed transfer leaves partial bytes (`HttpReq`'s cleanup, es-core, EP-4); the media path on a guest (G-05 had no results, so no media was resolved)."),
 "PL-03": ("3.10 at stage B; `stage-c/l310-boxart-shape.py` (`\"boxart\": \"x\"`: SEGV, rc -11 with `--plain`) and `l316-igdb-contract.py` (`{\"access_token\": 5}`: SEGV) at stage C; the recipe's NDEBUG read at `config/functions:384-388`; the seat's EP-9 to EP-14 and EP-32 for the inventory.",
           "rapidjson 1.1.0's `HasMember`, `operator[]` and `GetString` assert their containing type, and the assertion is compiled out. `GamesDBJSONScraper.cpp:590`, `:598`, `:605-607` (HasMember before IsObject), `:467-494`; `IGDBScraper.cpp:157`, `:159`; `HfsDBScraper.cpp:202`, `:204`, `:345`, `:410-415`, `:464-473`; `ArcadeDBJSONScraper.cpp:78`, `:87`, `:124`; `GamesDBJSONScraperResources.cpp:180-187`.",
           "`HttpApi.cpp:179-201`'s JSON import (outside the seat's packet), the IGDB game parser's helpers; EP-40 (#1154): with TLS verification off, the body need not come from the provider.",
           "Which shapes crash and which only misread (the array cases violate without a crash); HfsDB's numeric token is the same source defect, not separately run."),
 "PL-04": ("The floor's 3.15 (a subagent's read, re-read by the first reader at its lines).",
           "`Scraper.cpp:67-78`: `getScraper` returns `nullptr` for a name absent from the registry, which `:24-39` builds from the build's macros. `ThreadedScraper.cpp:296` calls `Scraper::getScraper()->getThreadCount(error)` unchecked; `:100` the same for `search`. `GuiScraperStart.cpp:74-78` shows the first entry when the saved name is absent and writes `Scraper` only from the change callback (`:215`).",
           "`ScraperSearchComponent.cpp:321` dereferences `getScraper(ss->name)` unchecked; `isValidConfiguredScraper` (`:80-83`) is called only at `ScraperSearchComponent.cpp:384`. Settings' default is `ScreenScraper` (`Settings.cpp:259`), registered in the fork's builds (#64).",
           "Which ROCKNIX builds carry which macros (their CI's secrets); the guest proof writes the setting directly."),
 "PL-05": ("L-06 at stage B (`t32-bounds.py`: 9 constructions, `bounded=0`); L-18's threads read at stage C; the seat's EP-15, EP-16 and EP-38.",
           "`HttpReqOptions`' defaults are a 10 s connect and no total or stall bound (`HttpReq.h:48-65`); `wait()` is a 20 ms sleep loop (`HttpReq.cpp:638-644`). `ThreadedScraper::start` -> `Process()` -> `ProcessNextGame` -> `ScraperThread::run` -> `search` -> `generateRequests` -> `ensureToken` (`IGDBScraper.cpp:150-151`, `HfsDBScraper.cpp:195-196`) runs before the worker exists (`ThreadedScraper.cpp:53`), on the interface thread. `Scraper.cpp:596`'s media retry takes no options.",
           "The manual paths on the interface thread (`ScraperSearchComponent.cpp:303`, `:658`; `:652` not live, EP-15); the manual builder's plain flag, leaked thread and missing join (`:206`, `:220-256`, EP-38); `GamesDBJSONScraperResources.cpp:153`; the uncaught throw on the scrape thread after a 30-minute gap between searches.",
           "The freeze's length on a device; it is bounded only by TCP's retries once the connect has completed."),
 "PL-07": ("L-08 at stage B; G-09 on the guest (a picture written over serial with the list open: absent in the session, present after a restart); the seat's EP-29 narrowed it.",
           "`DetailedContainer.cpp:899-916` decides MANUAL and MAP from `Utils::FileSystem::exists` with the session cache (`es-native-ui.md` § Core patterns); the image paths at `:806`, `:845-850`. ES's own writers drop their cache entry (`FileSystemUtil.cpp:1051`, `:1067`, `:1097`, `:1445`, `:1457-1458`, `:1506-1507`), so the stale case is a writer outside ES.",
           "`:817-831`, `:863-873` (the alternative images and the marquee); `Scraper.cpp:88-177`, `:407`, `:440` (L-09: what to fetch and overwrite decided from the same cache).",
           "Which cache held G-09's picture (EP-29: the image component's own, or the filesystem's); the stream proves each gate it changes."),
 "PL-08": ("3.32 at stage B; `stage-c/l332-year-and-time.py` FAILs at the pin; `DetailedContainer.cpp:1049` read and found not to wrap.",
           "`GameNameFormatter.cpp:84-85`: `mSortId == FileSorts::RELEASEDATE_ASCENDING` twice (5cb43906b); `FileSorts.h:23` has `RELEASEDATE_DESCENDING = 11`. `:175`: `h = (seconds / 3600) % 24` (2e4b5a9dc) with no day field.",
           "`TimeUtil.cpp:514-583` (`secondsToString`, the detailed row: folds the day back, \"25 h\"); the `SYSTEM_` and `_SYSTEM` variants are both listed.",
           "Nothing: the harness runs the statements as written."),
 "PL-10": ("L-10 and L-11 at stage B; the catalog read by `t32-words.py`; the seat's EP-30 and EP-31.",
           "`emulationstation2.po` L218: `SAVE STATES (HOLD)` -> `SAUVEGARDES (MAINTENU)`, the game-save word, beside L233's `SAVE STATES` -> `SAUVEGARDES D’ÉTAT`. `SystemView.cpp:233-234`: a sentence-case English message and a bare `\"OK\"` outside `_()`, after `UIMode` is set with no guaranteed `saveFile()` (`:237-239` saves only if HiddenSystems changed).",
           "The other `_()` calls in the 42 (`t32-words.py`: 69 calls, 50 msgids, 0 empty, 0 missing); `SystemView.cpp:243`'s all-hidden dialog (its French at L117). 3.34's refresh is carried as an observation, not this bug.",
           "How the French reads at 640x480 until a frame is taken."),
 "PL-17": ("The seat's EP-35, re-read by the first reader at its lines.",
           "`ISimpleGameListView.cpp:112-125`: `onFileChanged` saves `getCursor()` and passes it to `setCursor` after `populateList`. For an empty grid, `populateList` -> `addPlaceholder` -> `createNoEntriesPlaceholder` deletes the previous placeholder (`:929-934`), which was that cursor. `GridGameListView.cpp:84`: `cursor && !mGrid.setCursor(cursor) && !cursor->isPlaceHolder()` reads it.",
           "The other views' `setCursor` (Basic, Detailed, Video, Carousel) and their placeholder paths; `mLastParentFolderData` is the one owner.",
           "Which file-change notifications reach an empty grid on a device; only a theme with a grid view draws one."),
 "PL-18": ("The seat's EP-33, re-read by the first reader at its lines.",
           "`Scraper.cpp:95-97`: `if (Settings::getInstance()->getString(\"ScrapperLogoSrc\").empty() && !file->getMetadata(MetaDataId::Marquee).empty() && exists(...)) return true;` -- the logo counts only when its source is off. `:144-146`, the missing-media test, uses `!...empty()`.",
           "The other media in `hasAnyMedia` (`:86-110`) test their source as non-empty.",
           "Nothing: the predicate is read as written."),
 "PL-21": ("L-20 at stage B; G-08 (`[ true ]` on an idle guest); the seat's EP-21; the ruling names the fork's harness.",
           "`HttpServerThread.cpp:304-309`: idle is no running game, scraper, installer, hasher or updater. `ThreadedCloudSync::isRunning()` (`ThreadedCloudSync.h:46`), the cloud lock (`/var/run/cloud_sync.lock`, the predicate at `SaveStateBookkeeper.cpp:71`) and `ProxyCards::sendRunning()` / `topUpRunning()` (`ProxyCards.h:34`, `:44`) are not asked.",
           "The callers: `tools/es-launch-memory:66`, `tools/ra-ui-test:157`; `/reloadgames` (`:533-542`) posts with no idle check (recorded, EP-21).",
           "Nothing beyond the route: the predicate is read as written."),
 "PL-22": ("L-19 at stage B; the seat's EP-20; the ruling names the fork's harness.",
           "`HttpServerThread.cpp:613-629`: for each game system, `getFilesRecursive(GAME)` on the pool thread, and for each match `postToUiThread([w, file] { ... ViewController::get()->launch(file); })`, with no `break` and the raw `FileData*` captured.",
           "#774 (T2 PL-008, a launch held behind a question keeps raw pointers); `/removegames` (`:738-770`) mutates on the pool thread (recorded, L-13); the callers `tools/time-to-play:235`, `tools/es-launch-memory:130`.",
           "Whether `ViewController::launch` rejects a second callback (outside the slice; EP-20: \"launch callbacks\")."),
}
# A heading too long for a GitHub title (256) is shortened here, in the heading's words.
SHORT = {"PL-02": "a scrape that reached nothing reads as COMPLETED: IO errors, spent 429s and failed media read as done, and the count is short by the thread count"}
assert sorted(TRACE) == sorted(PLS), set(PLS) ^ set(TRACE)
text = open(sys.argv[1], encoding="utf-8").read()
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
INTRO = ("Found by T32 (#679), the audit of EmulationStation's game list views, scrapers and services "
         "(`docs/audits/2026_10_27-epic-m6-es-app-views-scrapers/` on `feature/m6-es-app-views-scrapers-679`; the audit issue #1257), "
         "read at the ES pin `16dbac5211`. The section below is the item's in `05-punch-list.md`, copied with the stage-D ruling "
         "(#679, comment 6448695986); its leads and proofs are in `02-forward-audit.md`, the guest's records under `guest-cycle/`, "
         "the host harnesses under `stage-c/`.")
for pl in PLS:
    m = re.search(r"^## (%s): (.*?)\n(.*?)(?=^## PL-|^---\n\n## Phase 7)" % pl, text, re.S | re.M)
    assert m, pl
    title = re.sub(r"\s*\((a `bug`[^)]*|recorded[^)]*)\)\s*$", "", m.group(2)).strip()
    title = SHORT.get(pl, title)
    found, source, siblings, cannot = TRACE[pl]
    sect = m.group(3).rstrip().replace("- [ ] ", "- ")
    for need in ("**Already written:**", "**Can this be done on the VM?**"):
        assert need in sect, (pl, need)
    body = "\n".join([INTRO, "", "## " + pl, sect, "",
                      "## Code trace", "",
                      "- **How it was found:** " + found,
                      "- **The defect at its source (the pin):** " + source,
                      "- **Siblings hunted:** " + siblings,
                      "- **What reading cannot prove:** " + cannot, "",
                      "## Acceptance criteria", "",
                      "- [ ] The item's positive FAILs on the pin and PASSes on the stream's commit: `stage-e/<stream>-before.txt` and `-after.txt` in the audit folder, as the item's **Acceptance** lines above describe.",
                      "- [ ] `02` § The streams carries the stream's row with this bug's `Already written:` answer, and `05`'s Phase 7 row names the commit.", ""])
    full = "Bug: EmulationStation: %s (T32 %s)" % (title, pl)
    assert len(full) <= 256, (pl, len(full))
    open(os.path.join(out, pl + ".title"), "w").write(full + "\n")
    open(os.path.join(out, pl + ".md"), "w").write(body)
    print(pl, len(full), len(body))
