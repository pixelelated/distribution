# Punch list — M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

Written by the first reader (Opus 5.5) at stage C, from:
- `02` § The leads (L-01 to L-24, and the floor's 35 with their verdicts);
- `04` § Risk assessment;
- the guest cycle, the stage-C harnesses (`stage-c/runs.txt`) and the floor read (`stage-c/floor.md`);
- the seat's grades (`stage-c/astra-grades.md`).

- **reviewed-at:** `603b358a14` (distribution), **reviewed-at-es:** `16dbac5211` (the pin). **fixed-at:** and **fixed-at-es:** at stage E.
- **Independent depth:** one seat, GPT-6 Astra at `max`: 40 items, all accepted (`stage-c/astra-grades.md`).
- **One item per defect or reusable improvement**, however many leads found it, ordered by severity.
- **Nothing here changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. A fix lands only under a stream brief on the ES branch, proven twice. A row added, moved or renamed updates `docs/es-menu-map.md` in the same commit (D-UI-039).
- **Lines** are the pin's. "Guest" means the M6 image (M7's composition over the pin). "Fixture" means a stage-C harness that fails at the pin and passes its control.
- **The audit issue:** #1257 (a sub-issue of #679), one checkbox per item; `tools/box-check --issue 1257`: 20 open checkboxes, 0 fail.
- **The bugs:** twelve, filed with their code traces after the stage-D ruling (ruled 17:22 UTC, #679 comment 6448695986); each item's **Bug:** line names its issue.

---

## PL-01: a CANCEL as the batch scrape finishes writes through the freed `ThreadedScraper` and marks the completed run cancelled (a `bug` proposed; the fork's CANCEL over upstream's lifetime)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-01, L-02 (EP-6, EP-7), EP-34, EP-37 -- proved: fixture (`stage-c/l02-stop-after-finish.py`); tree (EP-34, EP-37)
- **Owner area:** `es-app/src/scrapers/ThreadedScraper.cpp:323-337` (`stop`), `:228-240` (`run`'s end), `ThreadedScraper.h:77` (`isRunning`)
- **What:**
  - `stop()` reads the static `mInstance` and writes `thread->mExitCode` under no lock, while `run()` sets `finished` under `sProgressMutex`, then does `delete this`.
  - A YES on CANCEL in that window is a heap-use-after-free: the write at `:335` after the self-delete at `:241`. It also sets `cancelled` over `finished`. The page (T31's `GuiScraperRun.cpp:140-141`) then reads SKIPPED - YOU CANCELLED IT over a completed run.
  - The harness widens the window with a hook. The seat shows the interleaving is natural (EP-6): `stop()` copies `mInstance`, the worker finishes and deletes itself, then `stop()` writes. The confirmation's YES calls `stop()` without rechecking `finished` (`GuiScraperRun.cpp:110-116`).
  - Two more ownership paths: the worker can `delete this` before the creator publishes `mHandle` (`:53`; EP-34, unproved). A startup throw leaves `running` set and `finished` unset (`:35-50`, `:308-316`; EP-37).
- **Fix shape (EP-7: a lock on `stop()` alone is not sufficient):**
  - an owned worker that is joined, not self-deleted;
  - every publication and clear of the singleton under one rule (start, the exception path, completion);
  - `mExitCode` and `mPaused` atomic;
  - completion and cancellation decided once, under the mutex;
  - a startup failure finalizes the snapshot.

  `main.cpp`'s exit-time `stop()` needs its teardown order read (outside the slice). The harness's control proves only the first window.
- **Can this be done on the VM?** Yes. The harness against the fixed file (`fix-unit-test`). A guest press in the frame cannot be timed, so the fixture is the proof.
- **Already written:** nothing inherited. The false SKIPPED stamp is a page outcome, not a file; no record carries it.
- **Acceptance:**
  - [ ] `stage-c/l02-stop-after-finish.py` against the fixed `ThreadedScraper.cpp` prints `finished 1, cancelled 0` with no sanitizer report (rc 0), and against the pin reports the use-after-free (`stage-e/` before/after records).
  - [ ] a harness case for EP-34 (the worker done before `mHandle` is assigned) and one for EP-37 (a startup throw), each FAIL at the pin and rc 0 against the fix.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S1 (ownership): an owned, joined worker -- `ThreadedScraper` owns its `std::thread`, `stop()` requests and joins, the destructor joins, no `delete this`; `main.cpp`'s exit teardown read, one `stop()` added there if needed and named under merge debt; a #585 line.
- **Bug:** #1258 (filed 2026-10-27, with its code trace).

## PL-02: a scrape that reached nothing reads as COMPLETED: an IO error, a spent 429 and a long Retry-After end as done; `process()`'s return is dropped, so ScreenScraper's rate limit reads as "no match"; and the page's count is short by the thread count (a `bug` proposed; upstream's request under the fork's page)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.13, 3.5, 3.16, 3.19, L-07 (the media half), L-05 (EP-1 to EP-5, EP-36) -- proved: fixture (`stage-c/l313-request-outcome.py`, `l316-igdb-contract.py`), guest (G-05: ten games offline, COMPLETED, GAMES SCRAPED: 9; it does not prove L-07's media path, EP-4)
- **Owner area:** `es-app/src/scrapers/Scraper.cpp:289-385` (`ScraperHttpRequest::update`, with `:337`, `:350-361`, `:372-376`), `:607-614`, `:631-635` (the media handle); `IGDBScraper.cpp:313-331`; `ThreadedScraper.cpp:248-256` (`updateUI`), `:66`; `ScreenScraper.cpp:383-384` (outside the 42: its `false`)
- **What:**
  - `REQ_IO_ERROR` is an "ignored error" (`:372-376`, a631e8c84). A 429 whose retries are spent is DONE (`:350-352`), and so is a Retry-After over 5 s where `retryOn249()` is false (`:357-361`). So an offline or rate-limited scrape counts no error, and T31's page says COMPLETED.
  - `:337` drops `process()`'s return. The three scrapers document "false = retry, rate limited". ScreenScraper returns `false` for "maximum threads per minute reached", which reads as no match. IGDB returns `false` for no match and on a parse error (3.16), so a fix that honours the return must correct IGDB first.
  - `sProgress.done` is set only as a game is handed out, so a finished run counts total minus threads: ten games read 9 on the guest (3.19). A no-match is counted as scraped, against `ThreadedScraper.h:67`.
  - The media handle's 404, IO error and spent 429 read as done too (L-07; #1191's caller half). So do a failed rename and a failed resize (`:669-688`, EP-5).
  - A dependency request's 404 discards the primary search's results (EP-1).
  - A manual token failure is an empty DONE, and a token transport failure reads INVALID CREDENTIALS (EP-36).
  - Line 4 carries the raw error words only for a fatal error; a nonfatal one has no why (L-05 narrowed, EP-3).
- **Fix shape:**
  - These statuses go through `setError(status, ...)`. The reader stops a run only on its fatal list (`ThreadedScraper.cpp:155-173`), so a batch still survives one game's failure (a631e8c84's intent) and the page counts it.
  - If `:337` is made to honour `false` (one bounded retry, for ScreenScraper's rate limit), IGDB's two `false`s become `true` first. 3.16 is a trap only for that change (EP-2).
  - Transport, response, file creation and media preparation are separate outcomes (EP-5). A token outcome is typed: rejected, unreachable, or absent (EP-36).
  - `run()` sets `done` to `total` minus the queue at its end, and the no-match case is counted apart if the page is to say it.
- **Can this be done on the VM?** Yes. `l313` and `l316` against the fixed files (`fix-unit-test`); G-05 again on the integration image with the link down: COULDN'T SCRAPE: 10 and GAMES SCRAPED: 0 (`fix-walk-pending-image`).
- **Already written:** nothing inherited. A game marked scraped with no data carries a `scrapeDate` (`acceptResult`'s empty-name branch, `ThreadedScraper.cpp:263-266`). Nothing reads that date to skip a game, so it is a stamp, not a gate. Read both: none.
- **Acceptance:**
  - [ ] `l313` against the fixed `Scraper.cpp`: the IO error, the spent 429 and the long Retry-After print `ASYNC_ERROR` with their codes, and 404 still prints `ASYNC_DONE` (rc 0); against the pin, FAIL.
  - [ ] `l316` against the fixed `IGDBScraper.cpp`: `process` returns 1 for `[]`, `{}` and a parse error (rc 0 for its 3.16 half).
  - [ ] a unit on `run()`'s end: ten games on one thread give `done 10`.
  - [ ] on the integration image, SCRAPE NOW with `eth0` down: a frame reading COULDN'T SCRAPE with the game count, not COMPLETED, GAMES SCRAPED: 9 (`fix-walk-pending-image`).
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S2 (outcomes and bounds); `ThreadedScraper::start`'s contract with T31's page unchanged; `GuiScraperRun.cpp` named as T31's collision; a #585 line.
- **Bug:** #1259 (filed 2026-10-27, with its code trace).

## PL-03: a response of the wrong shape is a wild read in the shipped build: TheGamesDB's `"boxart": "x"` and IGDB's or HfsDB's numeric token are SEGVs (a `bug` proposed; upstream's parsers)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.10, 3.8, L-22, floor 3.2 and 3.4 (EP-9 to EP-14, EP-32) -- proved: fixture (`stage-c/l310-boxart-shape.py`, `l316-igdb-contract.py`, both also `--plain`: rc -11; HfsDB's numeric token is the same source defect, not separately measured, EP-10)
- **Owner area:**
  - `GamesDBJSONScraper.cpp:558`, `:590`, `:596-607`, `:415`, `:467-494`; `GamesDBJSONScraperResources.cpp:180-187`;
  - `IGDBScraper.cpp:157`, `:159`;
  - `HfsDBScraper.cpp:202`, `:204`, `:345`, `:410-415`, `:464-473`;
  - `ArcadeDBJSONScraper.cpp:78`, `:87`, `:124`.
- **What:**
  - The recipe builds with NDEBUG (`config/functions:384-388`; ES's `PKG_BUILD_FLAGS` is `-gold`), so rapidjson's `IsObject` and `IsString` assertions are compiled out.
  - `HasMember` on an array or a string walks its elements or bytes as members. `GetString` on a number reads its bits as a pointer.
  - A server, a proxy or a captive portal that answers with the wrong shape crashes ES: `l310` on `"boxart": "x"`, and `l316` on `{"access_token": 5}`.
  - Not every violated precondition is a crash: the array cases violate without one (EP-9).
  - IGDB is built in every image and fetches a token only with both a client id and a secret (`:143-150`). TheGamesDB and HfsDB are built only with their macros.
- **Fix shape:** `IsObject`, `IsArray` or `IsString` before each member access (the controls), one helper per response.
- **Can this be done on the VM?** Yes. Both harnesses against the fixed files (`fix-unit-test`), with the images JSON's case added to `l310`.
- **Already written:** nothing inherited. A crash writes nothing, and a token is held in memory only.
- **Acceptance:**
  - [ ] `l310` and `l316` against the fixed files: every body, `"boxart": "x"` and `{"access_token": 5}` included, prints `preconditions violated 0` and returns (rc 0, and rc 0 with `--plain`); against the pin, FAIL.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S3 (parsers); a #585 line.
- **Bug:** #1260 (filed 2026-10-27, with its code trace).

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
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S2; a #585 line.
- **Bug:** #1261 (filed 2026-10-27, with its code trace).

## PL-05: the token requests and media downloads have no bound but the 10 s connect, and the token fetch at a scrape's start runs on the interface thread (a `bug` proposed; upstream's requests, #299's shape)

- **Severity:** Medium
- **Category:** Performance
- **Question:** Q2
- **Family:** a call with no bound
- **Source Finding:** L-06, L-18, 3.20 (EP-15, EP-16), EP-38 -- proved: tool-run (`t32-bounds.py`: `bounded=0` of 9), tree (the threads, `02` L-18)
- **Owner area:** `Scraper.cpp:267`, `:302`, `:332`, `:564`, `:567`, `:596`; `HfsDBScraper.cpp:195-196`; `IGDBScraper.cpp:150-151`; `GamesDBJSONScraperResources.cpp:153`; `ThreadedScraper.cpp:100`, `:296-320`; `ScraperSearchComponent.cpp:206`, `:220-256`, `:303`, `:321`, `:658`
- **What:**
  - None of the nine constructions sets `timeout` or `stallTimeout`.
  - The two token requests end in `wait()`, a 20 ms sleep loop.
  - A batch run's first searches, and three manual-scrape paths, run on the interface thread. A link that drops after the connect holds the screen until TCP gives up.
  - On the scrape thread, a refetch after 30 minutes can throw with no catch (unproved).
- **Fix shape:**
  - #299's `stallTimeout` on every construction, the media retry at `:596` included (it takes no options, EP-16). A total deadline for the token exchanges. The Retry-After wait capped separately.
  - The manual builder given owned, joined worker state (EP-38).
  - The batch run's first hand-out moved off the interface thread, or the token fetched before the page opens, with the page's own wait.
  - `generateRequests`' throw caught on the scrape thread.
- **Can this be done on the VM?** Yes. `tools/cloud-test-backend`'s dead port, and a stalling listener above 1024 for an https-less scraper URL in a unit (`fix-unit-test`). The interface-thread half is a frame timing on the guest with the link cut after the connect (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `t32-bounds.py` against the fixed tree prints `bounded=9`.
  - [ ] a unit: a request to a listener that accepts and never answers ends within its `stallTimeout` plus 2 s.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S2: the token fetch and the first hand-out move onto the worker, `Progress` reporting a starting state the page already draws; a #585 line.
- **Bug:** #1262 (filed 2026-10-27, with its code trace).

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
- **Fix shape:** the setter bounds only the Content-Length branch (`:2564-2567`; EP-23). The chunked and lengthless reads (`:2559-2562`) need a cumulative limit in the vendored reader. The library's currency is a #585 line. The seat could not verify the other library claims from the packet.
- **Can this be done on the VM?** Yes. From inside the guest, a chunked `POST` past the limit answers 413 and ES's pid is unchanged (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] on the integration image, a chunked POST of 64 MiB to `127.0.0.1:1234` answers 413, and ES's RSS and pid are unchanged (`fix-walk-pending-image`).
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** **recorded, with a #585 line to ROCKNIX** naming the vendored cpp-httplib (the 2020 v0.7 series; its own header `Copyright (c) 2020`; ES's last change to it b4985a427, 2021-11-08). The fix is a bump of the vendored file or a patch inside it, upstream's to take and the integration's to carry. WEB ACCESS is off by default and binds 127.0.0.1 without the player's opt-in.

## PL-07: a picture written from outside ES stays hidden until a restart, and the MANUAL and MAP rows are gated by the same cached reads (a `bug` proposed; upstream's cached reads)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a read of a file another process writes
- **Source Finding:** L-08, L-09 (EP-29) -- proved: guest (G-09, with its control, for a picture), tree (the MANUAL and MAP gates)
- **Owner area:** `DetailedContainer.cpp:903`, `:916` (and `:817-831`, `:863`, `:873`); `Scraper.cpp:88-177`, `:407`, `:440`
- **What:** the rows are decided from `exists()` with the session's cache. ES's own writers drop their entry, so only an outside writer is stale: a cloud content restore, the player over SSH. On the guest a **picture** stayed hidden in the session and appeared after a restart. Its cache owner is not identified (`:806`, `:845-850`; EP-29).
- **Fix shape:** `exists(path, false)` at the reads whose writer is outside ES (`es-native-ui.md` § Core patterns), as the rclone.conf gate did.
- **Can this be done on the VM?** Yes. G-09 again on the integration image, for the picture and for a manual with a theme that draws MANUAL (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] on the integration image, a manual written over serial with the list open shows the MANUAL row on re-entry, without a restart (`fix-walk-pending-image`).
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S4 (views and words); a #585 line.
- **Bug:** #1263 (filed 2026-10-27, with its code trace).

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
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S4; a #585 line.
- **Bug:** #1264 (filed 2026-10-27, with its code trace).

## PL-09: the grid's IMAGE source draws an empty tile for a game with a thumbnail and no image (a question; upstream's view)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.31 (EP-26) -- proved: fixture (`stage-c/l331-grid-image.py`), for the missing fallback; an empty path is not proved a blank tile
- **Owner area:** `views/gamelist/GridGameListView.cpp:131-153`
- **What:** the early return (8f30c244c, 2019) makes the IMAGE fallback added by 4371e3b7d (2021) unreachable. No shipped theme has a grid view (G-02).
- **Fix shape:** drop the early return (the control), if intent is the fallback. The history leaves it ambiguous.
- **Can this be done on the VM?** Yes. The harness (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `l331` against the fixed file: IMAGE with no image returns the thumbnail (rc 0).
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** **recorded, with a #585 line.** No shipped theme draws a grid, so no image shows it, and the history leaves the intent to upstream.

## PL-10: the slice's words: #210's SAVE STATES (HOLD) in French is the game-save word; an English dialog outside `_()`; the help bar refreshed on a cursor move only in collections (a `bug` proposed for the first two; a frame owed for the third)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-10, L-11, 3.34, 3.35 (EP-30, EP-31) -- proved: tree; tool-run (`t32-words.py`); guest (the French bar's five entries, consistent with 3.34, not proved)
- **Owner area:** `locale/lang/fr/LC_MESSAGES/emulationstation2.po` L218; `views/SystemView.cpp:233-234`; `ISimpleGameListView.cpp:681-741`; `BasicGameListView.cpp:31`, `DetailedGameListView.cpp:39`
- **What:**
  - `SAUVEGARDES (MAINTENU)` names game saves where L233 says `SAUVEGARDES D’ÉTAT` (`es-player-text.md` § Conventions).
  - `SystemView.cpp:233-234` shows an English sentence-case dialog outside `_()`, with a bare `"OK"`. Its `UIMode` write has no guaranteed save: `:237-239` saves only if HiddenSystems changes (EP-31).
  - The bar's SAVE STATES (HOLD) is refreshed on a cursor move only in collections.
- **Fix shape:** one catalog line; the dialog through `_()` with its French, and `saveFile()`; `updateHelpPrompts()` on a cursor change in every list.
- **Can this be done on the VM?** Yes. French frames of a list with save states, before and after a cursor move (`fix-walk-pending-image`); `tools/vm-qa`'s `french` suite.
- **Already written:** nothing inherited (a catalog and a dialog).
- **Acceptance:**
  - [ ] the catalog's msgid `SAVE STATES (HOLD)` reads `SAUVEGARDES D’ÉTAT (MAINTENU)` (a grep of the po).
  - [ ] `t32-words.py` over the fixed tree counts the dialog's string, with French.
  - [ ] French frames at 640x480: SAVE STATES (HOLD)'s entry present after a cursor move from a game without save states to one with them (`fix-walk-pending-image`).
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug` for L-10 and L-11, filed; S4 (views and words). **3.34's refresh and the French bar's fifth entry are carried as an observation** (an open item to test, `bugs-are-agent-first.md`): seen once, unexplained; the frame owed is a French 640x480 list with save states before and after a cursor move, on the integration image. If that frame reproduces it, it becomes a bug then.
- **Bug:** #1265 (filed 2026-10-27, with its code trace).

## PL-11: the API's handlers touch `FileData` and quit ES on httplib's pool thread; `/launch` posts a raw pointer per match; `/isIdle` ignores a cloud sync and the proxy (recorded; upstream's services, D-UI-079)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-12, L-13, L-19, L-20, L-21, 3.17, 3.18, 3.22, 3.23, 3.24 (EP-18 to EP-22) -- proved: tree; guest (G-08: `/notify`, `/removegames`, `/caps`, `/isIdle`)
- **Owner area:** `services/HttpServerThread.cpp:241`, `:249`, `:257`, `:299-320`, `:533-543`, `:574`, `:615-630`, `:738`, `:751-755`; `services/HttpApi.cpp:170-193`, `:210-259`; `Scraper.cpp:653-676`, `:784-799`
- **What:** each handler is upstream's.
  - `/notify` toasts from the pool (L-12). `/removegames` and the media writes touch `FileData` there (L-13). `/launch` walks every system and posts a raw `FileData*` per match, with no `break`: launch callbacks, not launches (L-19, #774's sibling, EP-20). `/quit` and its siblings call `quitES` there, and its threading contract is outside the slice (L-21, EP-22). The removal does not free the `FileData` (`:771` commented out, EP-19).
  - `/isIdle` asks the scraper, the installer, the hasher and the updater, but not a cloud sync or the RetroAchievements proxy (L-20). That half is the fork's lane.
  - The media and metadata responses (3.17, 3.18, 3.22-3.24) answer wrong statuses, or overwrite the image under `mix`.
- **Fix shape:** post every handler that touches `FileData` to the interface thread, as `/reloadgames` does. `/isIdle` reads the cloud lock and the proxy's state.
- **Can this be done on the VM?** Yes. G-08's calls with a reload in flight (`fix-walk-pending-image`); a unit on `/isIdle`'s inputs.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the coordinator's ruling recorded here: which of these a stream takes (the `/isIdle` half is in the fork's lanes), and which go to #585 as written.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** **split.** `/isIdle` is a bug in this slice (PL-21), and so is `/launch`'s missing `break` (PL-22), both S6 (the local API). L-12's pool-thread notification, L-21's `quitES`, the rest of L-13, and 3.17, 3.18, 3.22-3.24 are recorded with #585 lines.

## PL-12: the scrapers' smaller parse and media defects: one bad boxart entry drops a whole game, renamed keys yield no media silently, HfsDB's arcade filter drops TEKNOPARROT's id, ArcadeDB's null `system` (recorded; upstream's, partly macro-gated)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.3, 3.7, 3.11, 3.12; `floor.md`'s ArcadeDB `:56` and `:213-218` -- proved: tree (`floor.md`; `:56` re-read)
- **Owner area:** `ArcadeDBJSONScraper.cpp:56`, `:103-127`, `:213-218`; `GamesDBJSONScraper.cpp:293-310`, `:624`; `HfsDBScraper.cpp:29`, `:385-394`, `:410-423`, `:621`
- **What:** in `floor.md`, each as the subagent read it. 3.7's throw-then-drop trace needs a helper the seat did not see (EP-13). Only ArcadeDB is built in every image; TheGamesDB and HfsDB are macro-gated.
- **Fix shape:** per item, contained.
- **Can this be done on the VM?** Yes. Units over each parser (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the coordinator's ruling recorded here: a stream for ArcadeDB's two (built in every image), #585 lines for the rest.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** recorded; #585 lines.

## PL-13: the views' smaller defects: the carousel's fast move leaves an index out of range (hidden by the wrap) and does nothing forward on fewer than ten systems; the letter jump takes a UTF-8 lead byte as a letter and lands wrong under another sort; G-03's cursor stayed on Alpha (recorded; upstream's views; G-03 open)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Family:** a check whose failure reads as success
- **Source Finding:** 3.27, 3.29, 3.30 (EP-24, EP-25) -- proved: fixture (`stage-c/l327-cursor-range.py`); tree (`floor.md`); guest (G-04 clean wrap; G-03 unexplained)
- **Owner area:** `views/SystemView.cpp:272-278`, `:331`; `views/gamelist/ISimpleGameListView.cpp:486-603` (`:511`, `:514`, `:554`, `:603`)
- **What:**
  - `_moveCursorInRange(2, -10, 5)` leaves `-3`, a delta and not a cursor (EP-24). A wrapping carousel hides it: 25 of 312 cases out of range, all congruent.
  - The forward fast move is a no-op on 3 to 9 systems.
  - `toupper(name[0])` files `É` and `Ã` under `"\xC3"`. The `break` at `:514` assumes name order.
  - G-03's cursor stayed on Alpha after a letter jump under a name sort, which neither explains.
- **Fix shape:** a proper modulo, with the guard on `abs(count)`. The first code point, upper-cased. No `break`. G-03 read again with a frame.
- **Can this be done on the VM?** Yes. `l327` (`fix-unit-test`); a list of accented names and a non-name sort on the guest (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the coordinator's ruling recorded here: a stream, or #585 lines (D-UI-079: the views are not a fork lane).
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** recorded; #585 lines. **G-03 is carried as an observation** (an open item to test): the cursor stayed on Alpha after a letter jump under a name sort, seen once and unexplained by 3.29. The frame owed is the same jump on the integration image; if it reproduces, it becomes a bug then.

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
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** S1, with PL-01 (the same lines).

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
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** resolved in the lane at stage E: S5 (the map).

## PL-16: carried, not this slice's to fix: L-16's free-then-read in `reloadCollection` (T33's), L-14's per-tile read (a grid theme), and the #585 lines owed (recorded)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-16, L-14, L-17 (EP-17, EP-28) -- proved: tree
- **Owner area:** `CollectionSystemManager.cpp:1574-1589` (T33's); `GridGameListView.cpp:42-47`; `02` § The #585 lines owed
- **What:** as `02` § The leads gives them, with their lines. L-16 is conditional: the root's ownership and the cursor's identity are T33's to read, and the quick search passes the root's name (EP-28). L-14 is a lead, not a measured cost (EP-17).
- **Fix shape:** none here.
- **Can this be done on the VM?** Yes, for T33: FILTER GAMES BY TEXT on a grouped custom collection on a guest.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `02` § What T33 to T37 inherit names L-16 with its lines.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** Deferred to T33 (#680) for L-16; L-14 recorded; the #585 lines written in `02`.

## PL-17: rebuilding an empty grid reads the placeholder it just deleted (a `bug` proposed; the fork-modified grid and list files)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-26 (EP-35) -- proved: tree (re-read by the first reader)
- **Owner area:** `views/gamelist/ISimpleGameListView.cpp:112-125` (`onFileChanged`), `:929-934` (`createNoEntriesPlaceholder`); `views/gamelist/GridGameListView.cpp:84-87` (`setCursor`), `:214-215`, `:249-253`
- **What:**
  - `onFileChanged` saves the cursor (the placeholder of an empty grid), repopulates, and passes it to `setCursor`.
  - The repopulate creates a new placeholder and `delete`s the previous one.
  - `setCursor` then calls `cursor->isPlaceHolder()` on the freed placeholder: a use-after-free read.
  - Only a theme with a grid view reaches it. The shipped theme has none, but a player may install one.
- **Fix shape:** do not restore a placeholder cursor across a repopulate. Keep it by identity, or skip `setCursor` when the old cursor was a placeholder.
- **Can this be done on the VM?** Yes. A harness over the two functions with an empty root, under ASan (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a stage-E harness: an empty grid's `onFileChanged` under ASan reports a heap-use-after-free at the pin and nothing against the fix.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S4; a #585 line.
- **Bug:** #1266 (filed 2026-10-27, with its code trace).

## PL-18: `hasAnyMedia`'s logo test is inverted (a `bug` proposed; upstream's)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-25 (EP-33) -- proved: tree (re-read)
- **Owner area:** `scrapers/Scraper.cpp:95-97` against `:144-146`
- **What:** a marquee counts as present only when `ScrapperLogoSrc` is **empty**, while the missing-media test uses non-empty. So a game whose only media is its logo can be scraped again, and a disabled logo source can count as present.
- **Fix shape:** `!` on `:96`'s `empty()`, as `:145` has it.
- **Can this be done on the VM?** Yes. A unit over `hasAnyMedia` with the setting toggled (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a unit: an existing marquee and a non-empty `ScrapperLogoSrc` make `hasAnyMedia` true; empty makes it false.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S2; a #585 line.
- **Bug:** #1267 (filed 2026-10-27, with its code trace).

## PL-19: media are named by the game's stem, so two games with one name in different folders share a file (recorded; upstream's naming)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** L-29 (EP-39) -- proved: tree
- **Owner area:** `scrapers/Scraper.cpp:801-811`, `:438-446`
- **What:** `a/game.zip` and `b/game.zip` get the same media path. With overwrite off, the second adopts the first's media.
- **Fix shape:** a collision-resistant name that reads the existing paths. The devices' media folders already hold these names.
- **Can this be done on the VM?** Yes. A unit on `getSaveAsPath` (`fix-unit-test`).
- **Already written:** every scraped device's media folder holds stem-named files and gamelists pointing at them. A fix must read both, or the old paths break.
- **Acceptance:**
  - [ ] the coordinator's ruling recorded here: a stream with a migration, or a #585 line.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** recorded; a #585 line.

## PL-20: TLS peer verification is off in the shared request layer (Deferred: #1154)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Family:** a check whose failure reads as success
- **Source Finding:** EP-40 -- proved: tree (`HttpReq.cpp:191-192`, es-core, outside the 42)
- **Owner area:** `es-core/src/HttpReq.cpp` (#1154's)
- **What:** an untrusted chain is accepted. That widens PL-03: a malformed response need not come from the provider.
- **Fix shape:** #1154's.
- **Can this be done on the VM?** Yes, as #1154 says.
- **Already written:** as #1154 says.
- **Acceptance:**
  - [ ] #1154 names PL-03's parsers as a consumer, in a comment.
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** Deferred to #1154.

## PL-21: `/isIdle` answers idle while a cloud sync, the cloud lock or the proxy's send is running (a `bug`; the fork's lanes, the fork's harness)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q1
- **Family:** a check whose failure reads as success
- **Source Finding:** L-20 (EP-21) -- proved: tree; guest (G-08 read `[ true ]` on an idle guest)
- **Owner area:** `es-app/src/services/HttpServerThread.cpp:299-320`
- **What:**
  - The route asks only about a running game, the scraper, the content installer, the hasher and the updater (`:304-309`).
  - It does not ask about `ThreadedCloudSync::isRunning()` (`ThreadedCloudSync.h:46`), the scripts' `/var/run/cloud_sync.lock` (the predicate `SaveStateBookkeeper.cpp:71` uses), or the proxy's send and top-up (`ProxyCards::sendRunning()`, `topUpRunning()`, `ProxyCards.h:34`, `:44`).
  - The fork's own harness waits on this answer (`tools/es-launch-memory:66`, `tools/ra-ui-test:157`), so a walk can go on while a sync it did not start is still running.
- **Fix shape:** idle also requires no cloud sync, no held cloud lock, and no proxy send or top-up. `/isIdle` is documented as "nothing the fork's harness would race" (EP-21).
- **Can this be done on the VM?** Yes. A harness over the route's predicate with each source doubled (`fix-unit-test`); on the integration image, `flock /var/run/cloud_sync.lock sleep 30 &` and then `curl 127.0.0.1:1234/isIdle` reads `[ false ]` (`fix-walk-pending-image`).
- **Already written:** nothing inherited: the route writes nothing.
- **Acceptance:**
  - [ ] a stage-E harness: with the lock held, a sync running or a send running, the predicate is false at the fix and true at the pin.
  - [ ] on the integration image, `/isIdle` reads `[ false ]` while a shell holds `/var/run/cloud_sync.lock`, and `[ true ]` after (`fix-walk-pending-image`).
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S6 (the local API).
- **Bug:** #1268 (filed 2026-10-27, with its code trace).

## PL-22: `POST /launch` posts one launch per matching file, with no `break`, as a raw `FileData*` read on the pool thread (a `bug`; upstream's route, driven by the fork's harness)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q1
- **Family:** a lifetime or a thread
- **Source Finding:** L-19 (EP-20) -- proved: tree
- **Owner area:** `es-app/src/services/HttpServerThread.cpp:603-630`
- **What:**
  - The handler walks every game system's files on httplib's pool thread while the interface thread may rebuild them.
  - For **every** file whose full path or path equals the body, it posts `ViewController::launch(file)` with the raw pointer captured. There is no `break`, so a game reachable by two paths gets two launch callbacks.
  - A reload between the lookup and the callback leaves the pointer dangling (#774's shape, T2's PL-008).
  - The fork's harness drives this route (`tools/time-to-play:235`, `tools/es-launch-memory:130`).
- **Fix shape:** one launch per request. Post the path, not the pointer, and find the file by path on the interface thread at execution time (D-QA-051 rule 6).
- **Can this be done on the VM?** Yes. A harness with two systems carrying the same path: one launch at the fix, two at the pin (`fix-unit-test`). On the integration image, `tools/time-to-play`'s launch still starts its game (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a stage-E harness: a path matched by two entries posts one launch at the fix and two at the pin, and the posted work carries no `FileData*`.
  - [ ] `tools/time-to-play`'s cell on the integration image reaches its first frame through `/launch` (`fix-walk-pending-image`).
- **Disposition (ruled 17:22 UTC, #679 comment 6448695986):** a `bug`, filed; S6 (the local API).
- **Bug:** #1269 (filed 2026-10-27, with its code trace).

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
| PL-17 | Open | -- |
| PL-18 | Open | -- |
| PL-19 | Open | -- |
| PL-20 | Open | -- |
| PL-21 | Open | -- |
| PL-22 | Open | -- |

```yaml
punch_index:
- id: PL-01
  severity: "High"
  category: Correctness
  question: Q1
  source_finding: "L-01, L-02, EP-34, EP-37"
  outcome: "open"
- id: PL-02
  severity: "High"
  category: Correctness
  question: Q3
  source_finding: "3.13, 3.5, 3.16, 3.19, L-07, L-05, L-27"
  outcome: "open"
- id: PL-03
  severity: "High"
  category: Correctness
  question: Q3
  source_finding: "3.10, 3.8, L-22, 3.2, 3.4"
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
  source_finding: "L-06, L-18, 3.20, L-28"
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
- id: PL-17
  severity: "Medium"
  category: Correctness
  question: Q1
  source_finding: "L-26"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-25"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-29"
  outcome: "open"
- id: PL-20
  severity: "Medium"
  category: Security
  question: Q3
  source_finding: "EP-40"
  outcome: "open"
- id: PL-21
  severity: "Low"
  category: Correctness
  question: Q1
  source_finding: "L-20"
  outcome: "open"
- id: PL-22
  severity: "Low"
  category: Correctness
  question: Q1
  source_finding: "L-19"
  outcome: "open"
```
