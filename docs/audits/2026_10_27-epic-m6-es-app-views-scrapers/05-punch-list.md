# Punch list — M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

Written by the first reader (Opus 5.5) at stage C, from:
- `02` § The leads (L-01 to L-24, and the floor's 35 with their verdicts);
- `04` § Risk assessment;
- the guest cycle, the stage-C harnesses (`stage-c/runs.txt`) and the floor read (`stage-c/floor.md`);
- the seat's grades (`stage-c/astra-grades.md`).

- **reviewed-at:** `603b358a14` (distribution), **reviewed-at-es:** `16dbac5211` (the pin). **fixed-at:** and **fixed-at-es:** at stage E.
- **Independent depth:** one seat, GPT-6 Astra at `max` (`04` § Second opinion).
- **One item per defect or reusable improvement**, however many leads found it, ordered by severity.
- **Nothing here changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. A fix lands only under a stream brief on the ES branch, proven twice. A row added, moved or renamed updates `docs/es-menu-map.md` in the same commit (D-UI-039).
- **Lines** are the pin's. "Guest" means the M6 image (M7's composition over the pin). "Fixture" means a stage-C harness that fails at the pin and passes its control.
- **The bugs are proposed, not filed.** As on #678, each is filed with its code trace once the coordinator rules at the stage-D pause.

---

## PL-01: a CANCEL as the batch scrape finishes writes through the freed `ThreadedScraper` and marks the completed run cancelled (a `bug` proposed; the fork's CANCEL over upstream's lifetime)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-01, L-02 -- proved: fixture (`stage-c/l02-stop-after-finish.py`)
- **Owner area:** `es-app/src/scrapers/ThreadedScraper.cpp:323-337` (`stop`), `:228-240` (`run`'s end), `ThreadedScraper.h:77` (`isRunning`)
- **What:**
  - `stop()` reads the static `mInstance` and writes `thread->mExitCode` under no lock, while `run()` sets `finished` under `sProgressMutex`, then does `delete this`.
  - A YES on CANCEL in that window is a heap-use-after-free at `:333`, and it sets `cancelled` over `finished`. The page (T31's `GuiScraperRun.cpp:140-141`) then reads SKIPPED - YOU CANCELLED IT over a completed run.
  - The harness widens the window with a hook, as it says. On a device the order needs a press in the frame the last game ends.
- **Fix shape:** the control. `stop()` takes `sProgressMutex`, returns when `finished` is set, and reads `mInstance` under it. `run()` clears `mInstance` under the same lock before `delete this`. `isRunning()` and `main.cpp:1332`'s exit-time `stop()` read the same static under the same lock.
- **Can this be done on the VM?** Yes. The harness against the fixed file (`fix-unit-test`). A guest press in the frame cannot be timed, so the fixture is the proof.
- **Already written:** nothing inherited. The false SKIPPED stamp is a page outcome, not a file; no record carries it.
- **Acceptance:**
  - [ ] `stage-c/l02-stop-after-finish.py` against the fixed `ThreadedScraper.cpp` prints `finished 1, cancelled 0` with no sanitizer report (rc 0), and against the pin reports the use-after-free (`stage-e/` before/after records).
- **Disposition (proposed):** a `bug`, filed after the ruling; a stream on the ES branch; a #585 line (the unlocked lifetime is upstream's).

## PL-02: a scrape that reached nothing reads as COMPLETED: an IO error, a spent 429 and a long Retry-After end as done; `process()`'s return is dropped, so ScreenScraper's rate limit reads as "no match"; and the page's count is short by the thread count (a `bug` proposed; upstream's request under the fork's page)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.13, 3.5, 3.16, 3.19, L-07 (the media half), L-05 -- proved: fixture (`stage-c/l313-request-outcome.py`, `l316-igdb-contract.py`), guest (G-05: ten games offline, COMPLETED, GAMES SCRAPED: 9)
- **Owner area:** `es-app/src/scrapers/Scraper.cpp:289-385` (`ScraperHttpRequest::update`, with `:337`, `:350-361`, `:372-376`), `:607-614`, `:631-635` (the media handle); `IGDBScraper.cpp:313-331`; `ThreadedScraper.cpp:248-256` (`updateUI`), `:66`; `ScreenScraper.cpp:383-384` (outside the 42: its `false`)
- **What:**
  - `REQ_IO_ERROR` is an "ignored error" (`:372-376`, a631e8c84). A 429 whose retries are spent is DONE (`:350-352`), and so is a Retry-After over 5 s where `retryOn249()` is false (`:357-361`). So an offline or rate-limited scrape counts no error, and T31's page says COMPLETED.
  - `:337` drops `process()`'s return. The three scrapers document "false = retry, rate limited". ScreenScraper returns `false` for "maximum threads per minute reached", which reads as no match. IGDB returns `false` for no match and on a parse error (3.16), so a fix that honours the return must correct IGDB first.
  - `sProgress.done` is set only as a game is handed out, so a finished run counts total minus threads: ten games read 9 on the guest (3.19). A no-match is counted as scraped, against `ThreadedScraper.h:67`.
  - The media handle's 404, IO error and spent 429 read as done too (L-07; #1191's caller half).
- **Fix shape:**
  - These statuses go through `setError(status, ...)`. The reader stops a run only on its fatal list (`ThreadedScraper.cpp:155-173`), so a batch still survives one game's failure (a631e8c84's intent) and the page counts it.
  - `:337` honours `false` with one bounded retry after `mOverQuotaRetryDelay`. IGDB's two `false`s become `true` (the control).
  - `run()` sets `done` to `total` minus the queue at its end, and the no-match case is counted apart if the page is to say it.
- **Can this be done on the VM?** Yes. `l313` and `l316` against the fixed files (`fix-unit-test`); G-05 again on the integration image with the link down: COULDN'T SCRAPE: 10 and GAMES SCRAPED: 0 (`fix-walk-pending-image`).
- **Already written:** nothing inherited. A game marked scraped with no data carries a `scrapeDate` (`acceptResult`'s empty-name branch, `ThreadedScraper.cpp:263-266`). Nothing reads that date to skip a game, so it is a stamp, not a gate. Read both: none.
- **Acceptance:**
  - [ ] `l313` against the fixed `Scraper.cpp`: the IO error, the spent 429 and the long Retry-After print `ASYNC_ERROR` with their codes, and 404 still prints `ASYNC_DONE` (rc 0); against the pin, FAIL.
  - [ ] `l316` against the fixed `IGDBScraper.cpp`: `process` returns 1 for `[]`, `{}` and a parse error (rc 0 for its 3.16 half).
  - [ ] a unit on `run()`'s end: ten games on one thread give `done 10`.
  - [ ] on the integration image, SCRAPE NOW with `eth0` down: a frame reading COULDN'T SCRAPE with the game count, not COMPLETED, GAMES SCRAPED: 9 (`fix-walk-pending-image`).
- **Disposition (proposed):** a `bug`, filed after the ruling; one stream (the request, the reader's count, IGDB's return); #1205 keeps the HTTP-date half; a #585 line.

## PL-03: a response of the wrong shape is a wild read in the shipped build: TheGamesDB's `"boxart": "x"` and IGDB's or HfsDB's numeric token are SEGVs (a `bug` proposed; upstream's parsers)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.10, 3.8, L-22 -- proved: fixture (`stage-c/l310-boxart-shape.py`, `l316-igdb-contract.py`, both also `--plain`: rc -11)
- **Owner area:**
  - `GamesDBJSONScraper.cpp:590`, `:598`, `:605-607`, `:415`, `:462-491`; `GamesDBJSONScraperResources.cpp:180`;
  - `IGDBScraper.cpp:155-157`;
  - `HfsDBScraper.cpp:202-204`.
- **What:**
  - The recipe builds with NDEBUG (`config/functions:384-388`; ES's `PKG_BUILD_FLAGS` is `-gold`), so rapidjson's `IsObject` and `IsString` assertions are compiled out.
  - `HasMember` on an array or a string walks its elements or bytes as members. `GetString` on a number reads its bits as a pointer.
  - A server, a proxy or a captive portal that answers with the wrong shape crashes ES: `l310` on `"boxart": "x"`, and `l316` on `{"access_token": 5}`.
  - IGDB is built in every image. TheGamesDB and HfsDB only with their macros.
- **Fix shape:** `IsObject`, `IsArray` or `IsString` before each member access (the controls), one helper per response.
- **Can this be done on the VM?** Yes. Both harnesses against the fixed files (`fix-unit-test`), with the images JSON's case added to `l310`.
- **Already written:** nothing inherited. A crash writes nothing, and a token is held in memory only.
- **Acceptance:**
  - [ ] `l310` and `l316` against the fixed files: every body, `"boxart": "x"` and `{"access_token": 5}` included, prints `preconditions violated 0` and returns (rc 0, and rc 0 with `--plain`); against the pin, FAIL.
- **Disposition (proposed):** a `bug`, filed after the ruling; a stream; a #585 line.

## PL-04: a saved scraper the build does not register crashes SCRAPE NOW (a `bug` proposed; upstream's registry, an upgrade path)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q7
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.15 -- proved: tree (`floor.md`; re-read by the first reader)
- **Owner area:** `Scraper.cpp:67-78` (`getScraper`), `:80-83`; `ThreadedScraper.cpp:296`, `:100`; `components/ScraperSearchComponent.cpp:321`; `guis/GuiScraperStart.cpp:74-78`, `:215` (T31's file)
- **What:**
  - The registry depends on the build's macros (`Scraper.cpp:24-39`), while `es_settings.cfg`'s `Scraper` survives an upgrade.
  - SCRAPER shows the first entry when the saved name is absent, but writes the setting only on a change (`:215`).
  - SCRAPE NOW then dereferences `getScraper()`'s `nullptr` at `ThreadedScraper.cpp:296`.
  - Reached from a device that last scraped with a scraper this build lacks: a ROCKNIX build with another key set, or a fork build without a macro.
- **Fix shape:** `getScraper()` falls back to the first registered scraper. SCRAPER saves its shown selection on open.
- **Can this be done on the VM?** Yes. Write `Scraper` = an unregistered name into the guest's `es_settings.cfg`, open SCRAPER and press SCRAPE NOW (`fix-walk-pending-image`). A unit on `getScraper` with an injected registry (`fix-unit-test`).
- **Already written:** devices may carry a `Scraper` name their build does not register. The fix reads it, falls back, and writes the shown one on SCRAPER's open: read both.
- **Acceptance:**
  - [ ] a unit: `getScraper("Absent")` returns the first registered scraper.
  - [ ] on the integration image with `Scraper` set to an unregistered name: SCRAPE NOW runs, ES's pid is unchanged, and the journal has no backtrace (`fix-walk-pending-image`).
- **Disposition (proposed):** a `bug`, filed after the ruling; a stream; a #585 line.

## PL-05: the token requests and media downloads have no bound but the 10 s connect, and the token fetch at a scrape's start runs on the interface thread (a `bug` proposed; upstream's requests, #299's shape)

- **Severity:** Medium
- **Category:** Performance
- **Question:** Q2
- **Family:** a call with no bound
- **Source Finding:** L-06, L-18, 3.20 -- proved: tool-run (`t32-bounds.py`: `bounded=0` of 9), tree (the threads, `02` L-18)
- **Owner area:** `Scraper.cpp:267`, `:302`, `:332`, `:564`, `:567`, `:596`; `HfsDBScraper.cpp:195-196`; `IGDBScraper.cpp:150-151`; `GamesDBJSONScraperResources.cpp:153`; `ThreadedScraper.cpp:100`, `:296-320`; `ScraperSearchComponent.cpp:303`, `:321`, `:652`, `:658`
- **What:**
  - None of the nine constructions sets `timeout` or `stallTimeout`.
  - The two token requests end in `wait()`, a 20 ms sleep loop.
  - A batch run's first searches, and three manual-scrape paths, run on the interface thread. A link that drops after the connect holds the screen until TCP gives up.
  - On the scrape thread, a refetch after 30 minutes can throw with no catch (unproved).
- **Fix shape:**
  - #299's: `stallTimeout` on the scrapers' options, the media handle's and the two token requests'.
  - The batch run's first hand-out moved off the interface thread, or the token fetched before the page opens, with the page's own wait.
  - `generateRequests`' throw caught on the scrape thread.
- **Can this be done on the VM?** Yes. `tools/cloud-test-backend`'s dead port, and a stalling listener above 1024 for an https-less scraper URL in a unit (`fix-unit-test`). The interface-thread half is a frame timing on the guest with the link cut after the connect (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `t32-bounds.py` against the fixed tree prints `bounded=9`.
  - [ ] a unit: a request to a listener that accepts and never answers ends within its `stallTimeout` plus 2 s.
- **Disposition (proposed):** a `bug`, filed after the ruling; one stream with PL-02 (the same files); a #585 line.

## PL-06: the vendored cpp-httplib (2020) bounds no request body; with WEB ACCESS on, a LAN host can grow one until ES dies (a `bug` proposed; upstream's server)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q7
- **Family:** a call with no bound
- **Source Finding:** L-24 -- proved: tree (`httplib.h:72`, `:2475`, `:2558-2559`); upstream check dated 2026-10-27 in `02` § The structure
- **Owner area:** `es-app/src/services/httplib.h`; `HttpServerThread.cpp:821-828`
- **What:**
  - `CPPHTTPLIB_PAYLOAD_MAX_LENGTH` is `SIZE_MAX`, and chunked reads take no limit: CVE-2025-46728's class, fixed upstream in 0.20.1.
  - The server listens on loopback, or on every interface with WEB ACCESS (a player's switch).
  - CVE-2026-45372's mechanism (decoded header values) is absent at this version.
- **Fix shape:** `mHttpServer->set_payload_max_length(<the largest media upload>)` where the server is built, plus a chunked limit in the vendored reader. The library's currency is a #585 line.
- **Can this be done on the VM?** Yes. From inside the guest, a chunked `POST` past the limit answers 413 and ES's pid is unchanged (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] on the integration image, a chunked POST of 64 MiB to `127.0.0.1:1234` answers 413, and ES's RSS and pid are unchanged (`fix-walk-pending-image`).
- **Disposition (proposed):** a `bug`, filed after the ruling, or recorded for the coordinator under D-UI-079 (WEB ACCESS is upstream's lane); a #585 line either way.

## PL-07: a manual or map written from outside ES is hidden until a launch or a restart (a `bug` proposed; upstream's cached reads)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a read of a file another process writes
- **Source Finding:** L-08, L-09 -- proved: guest (G-09, with its control)
- **Owner area:** `DetailedContainer.cpp:903`, `:916` (and `:817-831`, `:863`, `:873`); `Scraper.cpp:88-177`, `:407`, `:440`
- **What:** the rows are decided from `exists()` with the session's cache. ES's own writers drop their entry, so only an outside writer is stale: a cloud content restore, the player over SSH. On the guest, the manual stayed hidden in the session and appeared after a restart.
- **Fix shape:** `exists(path, false)` at the reads whose writer is outside ES (`es-native-ui.md` § Core patterns), as the rclone.conf gate did.
- **Can this be done on the VM?** Yes. G-09 again on the integration image: the MANUAL row appears without a restart (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] on the integration image, a manual written over serial with the list open shows the MANUAL row on re-entry, without a restart (`fix-walk-pending-image`).
- **Disposition (proposed):** a `bug`, filed after the ruling, or a stream question (the cloud restore is the fork's lane).

## PL-08: the game name shows no year under a descending date sort, and 25 hours of play read `[01:00:00]` (a `bug` proposed; upstream's formatter)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** 3.32 -- proved: fixture (`stage-c/l332-year-and-time.py`)
- **Owner area:** `views/gamelist/GameNameFormatter.cpp:84-85`, `:171-185`
- **What:** the initialiser tests `RELEASEDATE_ASCENDING` twice (5cb43906b), and `(seconds / 3600) % 24` drops the days (2e4b5a9dc). The detailed row does not wrap (`secondsToString`).
- **Fix shape:** the control: DESCENDING in the second line, and the hours without `% 24`.
- **Can this be done on the VM?** Yes. The harness (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `l332` against the fixed file: `RELEASEDATE_DESCENDING 1` and `GAME [25:00:00]` (rc 0); against the pin, FAIL.
- **Disposition (proposed):** a `bug`, filed after the ruling; a stream; a #585 line.

## PL-09: the grid's IMAGE source draws an empty tile for a game with a thumbnail and no image (a question; upstream's view)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.31 -- proved: fixture (`stage-c/l331-grid-image.py`)
- **Owner area:** `views/gamelist/GridGameListView.cpp:131-153`
- **What:** the early return (8f30c244c, 2019) makes the IMAGE fallback added by 4371e3b7d (2021) unreachable. No shipped theme has a grid view (G-02).
- **Fix shape:** drop the early return (the control), if intent is the fallback. The history leaves it ambiguous.
- **Can this be done on the VM?** Yes. The harness (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `l331` against the fixed file: IMAGE with no image returns the thumbnail (rc 0).
- **Disposition (proposed):** put to the coordinator: a `bug` with the fix, or recorded (no shipped theme reaches it; D-UI-079).

## PL-10: the slice's words: #210's SAVE STATES (HOLD) in French is the game-save word; an English dialog outside `_()`; the help bar refreshed on a cursor move only in collections (a `bug` proposed for the first two; a frame owed for the third)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-10, L-11, 3.34, 3.35 -- proved: tree; tool-run (`t32-words.py`); guest (the French bar's five entries, consistent with 3.34, not proved)
- **Owner area:** `locale/lang/fr/LC_MESSAGES/emulationstation2.po` L218; `views/SystemView.cpp:233-234`; `ISimpleGameListView.cpp:681-741`; `BasicGameListView.cpp:31`, `DetailedGameListView.cpp:39`
- **What:**
  - `SAUVEGARDES (MAINTENU)` names game saves where L233 says `SAUVEGARDES D’ÉTAT` (`es-player-text.md` § Conventions).
  - `SystemView.cpp:233-234` writes `UIMode` with no `saveFile()` and shows an English sentence-case dialog outside `_()`, with a bare `"OK"`.
  - The bar's SAVE STATES (HOLD) is refreshed on a cursor move only in collections.
- **Fix shape:** one catalog line; the dialog through `_()` with its French, and `saveFile()`; `updateHelpPrompts()` on a cursor change in every list.
- **Can this be done on the VM?** Yes. French frames of a list with save states, before and after a cursor move (`fix-walk-pending-image`); `tools/vm-qa`'s `french` suite.
- **Already written:** nothing inherited (a catalog and a dialog).
- **Acceptance:**
  - [ ] the catalog's msgid `SAVE STATES (HOLD)` reads `SAUVEGARDES D’ÉTAT (MAINTENU)` (a grep of the po).
  - [ ] `t32-words.py` over the fixed tree counts the dialog's string, with French.
  - [ ] French frames at 640x480: SAVE STATES (HOLD)'s entry present after a cursor move from a game without save states to one with them (`fix-walk-pending-image`).
- **Disposition (proposed):** a `bug` for L-10 and L-11, filed after the ruling (#210's string is the fork's); 3.34's refresh as a frame first.

## PL-11: the API's handlers touch `FileData` and quit ES on httplib's pool thread; `/launch` posts a raw pointer per match; `/isIdle` ignores a cloud sync and the proxy (recorded; upstream's services, D-UI-079)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-12, L-13, L-19, L-20, L-21, 3.17, 3.18, 3.22, 3.23, 3.24 -- proved: tree; guest (G-08: `/notify`, `/removegames`, `/caps`, `/isIdle`)
- **Owner area:** `services/HttpServerThread.cpp:241`, `:249`, `:257`, `:299-320`, `:533-543`, `:574`, `:615-630`, `:738`, `:751-755`; `services/HttpApi.cpp:170-193`, `:210-259`; `Scraper.cpp:653-676`, `:784-799`
- **What:** each handler is upstream's.
  - `/notify` toasts from the pool (L-12). `/removegames` and the media writes touch `FileData` there (L-13). `/launch` walks every system and posts a raw `FileData*` per match, with no `break` (L-19, #774's sibling). `/quit` and its siblings call `quitES` there (L-21).
  - `/isIdle` asks the scraper, the installer, the hasher and the updater, but not a cloud sync or the RetroAchievements proxy (L-20). That half is the fork's lane.
  - The media and metadata responses (3.17, 3.18, 3.22-3.24) answer wrong statuses, or overwrite the image under `mix`.
- **Fix shape:** post every handler that touches `FileData` to the interface thread, as `/reloadgames` does. `/isIdle` reads the cloud lock and the proxy's state.
- **Can this be done on the VM?** Yes. G-08's calls with a reload in flight (`fix-walk-pending-image`); a unit on `/isIdle`'s inputs.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the coordinator's ruling recorded here: which of these a stream takes (the `/isIdle` half is in the fork's lanes), and which go to #585 as written.
- **Disposition (proposed):** recorded, with `/isIdle`'s cloud half put to the coordinator as a `bug` in the fork's lane; the rest #585 lines.

## PL-12: the scrapers' smaller parse and media defects: one bad boxart entry drops a whole game, renamed keys yield no media silently, HfsDB's arcade filter drops TEKNOPARROT's id, ArcadeDB's null `system` (recorded; upstream's, partly macro-gated)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.3, 3.7, 3.11, 3.12; `floor.md`'s ArcadeDB `:56` and `:213-218` -- proved: tree (`floor.md`; `:56` re-read)
- **Owner area:** `ArcadeDBJSONScraper.cpp:56`, `:103-127`, `:213-218`; `GamesDBJSONScraper.cpp:293-310`, `:624`; `HfsDBScraper.cpp:29`, `:385-394`, `:410-423`, `:621`
- **What:** in `floor.md`, each as the subagent read it. Only ArcadeDB is built in every image; TheGamesDB and HfsDB are macro-gated.
- **Fix shape:** per item, contained.
- **Can this be done on the VM?** Yes. Units over each parser (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the coordinator's ruling recorded here: a stream for ArcadeDB's two (built in every image), #585 lines for the rest.
- **Disposition (proposed):** recorded; ArcadeDB's `:56` and `:213-218` in PL-02's stream if the coordinator takes them.

## PL-13: the views' smaller defects: the carousel's fast move leaves an index out of range (hidden by the wrap) and does nothing forward on fewer than ten systems; the letter jump takes a UTF-8 lead byte as a letter and lands wrong under another sort; G-03's cursor stayed on Alpha (recorded; upstream's views; G-03 open)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.27, 3.29, 3.30 -- proved: fixture (`stage-c/l327-cursor-range.py`); tree (`floor.md`); guest (G-04 clean wrap; G-03 unexplained)
- **Owner area:** `views/SystemView.cpp:272-278`, `:331`; `views/gamelist/ISimpleGameListView.cpp:486-603` (`:511`, `:514`, `:554`, `:603`)
- **What:**
  - `_moveCursorInRange(2, -10, 5)` leaves `-3`. The caller uses only the delta, so a wrapping carousel hides it (25 of 312 cases out of range, all congruent).
  - The forward fast move is a no-op on 3 to 9 systems.
  - `toupper(name[0])` files `É` and `Ã` under `"\xC3"`. The `break` at `:514` assumes name order.
  - G-03's cursor stayed on Alpha after a letter jump under a name sort, which neither explains.
- **Fix shape:** a proper modulo, with the guard on `abs(count)`. The first code point, upper-cased. No `break`. G-03 read again with a frame.
- **Can this be done on the VM?** Yes. `l327` (`fix-unit-test`); a list of accented names and a non-name sort on the guest (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the coordinator's ruling recorded here: a stream, or #585 lines (D-UI-079: the views are not a fork lane).
- **Disposition (proposed):** recorded as #585 lines; G-03 carried as a frame for whichever stream next touches the list.

## PL-14: `run()` leaks every `ScraperThread` and its own `std::thread` (recorded, or with PL-01's stream)

- **Severity:** Low
- **Category:** Performance
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-23 -- proved: tree (`ThreadedScraper.cpp:218`, `:53`, `:71-72`)
- **Owner area:** `es-app/src/scrapers/ThreadedScraper.cpp`
- **What:** each finished `ScraperThread` is erased without a `delete` (717e7d8c3), and `mHandle` is never joined or freed.
- **Fix shape:** delete on erase; detach or join `mHandle` before `delete this`.
- **Can this be done on the VM?** Yes. `l02`'s fixture with a heap thread and LeakSanitizer (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `l02` with a heap-allocated thread double reports no leak against the fixed file.
- **Disposition (proposed):** in PL-01's stream (the same lines).

## PL-15: the map has no section for the five view styles, the rows that pick them, or the SCREENSHOTS list (required: checkbox 18, D-UI-039)

- **Severity:** Low
- **Category:** Documentation
- **Question:** Q7
- **Family:** a page the map does not describe
- **Source Finding:** L-15 -- proved: tree (`docs/es-menu-map.md:135`)
- **Owner area:** `docs/es-menu-map.md`
- **What:** the views carry no screen title, so `es-menu-map-check` cannot see them. `SystemView.cpp:552`'s computed title is #965's.
- **Fix shape:** a section naming the five styles, GAMELIST VIEW STYLE (T26's), VIEW OPTIONS (T31's) and the SCREENSHOTS list, in the distribution branch.
- **Can this be done on the VM?** Yes. `tools/es-menu-map-check --es-src <W> --ref <reviewed-at-es>` (`tool-run`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `tools/es-menu-map-check --es-src <W> --ref <fixed-at-es>` prints `0 missing` with the section in place.
- **Disposition (proposed):** resolved in the lane at stage E (a docs commit).

## PL-16: carried, not this slice's to fix: L-16's free-then-read in `reloadCollection` (T33's), L-14's per-tile read (a grid theme), and the #585 lines owed (recorded)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-16, L-14, L-17 -- proved: tree
- **Owner area:** `CollectionSystemManager.cpp:1574-1589` (T33's); `GridGameListView.cpp:42-47`; `02` § The #585 lines owed
- **What:** as `02` § The leads gives them, with their lines.
- **Fix shape:** none here.
- **Can this be done on the VM?** Yes, for T33: FILTER GAMES BY TEXT on a grouped custom collection on a guest.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `02` § What T33 to T37 inherit names L-16 with its lines.
- **Disposition (proposed):** Deferred to T33 (#680) for L-16; L-14 recorded; the #585 lines written in `02`.

---

## Phase 7

At stage D every item is open, awaiting the coordinator's dispositions. Stage F rewrites this table and the index together.

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

```yaml
punch_index:
- id: PL-01
  severity: "High"
  category: Correctness
  question: Q1
  source_finding: "L-01, L-02"
  outcome: "open"
- id: PL-02
  severity: "High"
  category: Correctness
  question: Q3
  source_finding: "3.13, 3.5, 3.16, 3.19, L-07, L-05"
  outcome: "open"
- id: PL-03
  severity: "High"
  category: Correctness
  question: Q3
  source_finding: "3.10, 3.8, L-22"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Correctness
  question: Q7
  source_finding: "3.15"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: Performance
  question: Q2
  source_finding: "L-06, L-18, 3.20"
  outcome: "open"
- id: PL-06
  severity: "Medium"
  category: Security
  question: Q7
  source_finding: "L-24"
  outcome: "open"
- id: PL-07
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-08, L-09"
  outcome: "open"
- id: PL-08
  severity: "Low"
  category: Correctness
  question: Q6
  source_finding: "3.32"
  outcome: "open"
- id: PL-09
  severity: "Low"
  category: Correctness
  question: Q6
  source_finding: "3.31"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: Correctness
  question: Q5
  source_finding: "L-10, L-11, 3.34, 3.35"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: Correctness
  question: Q1
  source_finding: "L-12, L-13, L-19, L-20, L-21, 3.17, 3.18, 3.22, 3.23, 3.24"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "3.3, 3.7, 3.11, 3.12"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Correctness
  question: Q6
  source_finding: "3.27, 3.29, 3.30"
  outcome: "open"
- id: PL-14
  severity: "Low"
  category: Performance
  question: Q1
  source_finding: "L-23"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Documentation
  question: Q7
  source_finding: "L-15"
  outcome: "open"
- id: PL-16
  severity: "Low"
  category: Correctness
  question: Q1
  source_finding: "L-16, L-14, L-17"
  outcome: "open"
```
