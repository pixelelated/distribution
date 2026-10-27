# Retrospective audit — M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

This was written by the first reader (Opus 5.5) after stages A and B, the guest window and the stage-C host proofs, and before any seat saw the packet. Line numbers are the pin's (`16dbac5211`). The leads are `02`'s: L-01 to L-21 from stages A and B, and L-22 to L-24 from stage C. The floor's 35 are `02` § The leads' second table.

## 3.1 Architectural coherence

- **Three subsystems share one directory tree and one thread, the interface thread.**
  - The views (`views/`, `views/gamelist/`) draw the carousel and the six list styles.
  - The scrapers (`scrapers/`) fetch metadata and media.
  - The services (`services/`) are the local HTTP API on port 1234.

  Each reaches the others through `ViewController` (T2's) and `FileData` (T21's and T26's). The include graph is 410 include lines in the 42, 143 of them into es-core, and 47 lines in from 23 files outside (`stage-c/includes.out`). Each `.cpp` under `views/` and `services/` includes `ViewController.h`, and `ViewController.cpp` includes the slice's headers back: the cycle the brief takes as given.
- **The scrapers have one request type and one reader.**
  - `ScraperHttpRequest::update` (`Scraper.cpp:289-385`) turns an `HttpReq` status into an `AsyncHandle` status.
  - `ThreadedScraper` (`:103-173`) reads it: a fatal list stops the run, any other error is counted, and DONE is a game with or without a match.

  The contract between them is a comment written in three scrapers (`IGDBScraper.cpp:313`, the GamesDB and ArcadeDB equivalents): "return false only when we reached a maximum scrap by minute, to retry". **No caller reads the return** (`Scraper.cpp:337`). IGDB returns false for "no match" (3.16). ScreenScraper, which ships in the fork's images, returns false for "maximum threads per minute reached" (`ScreenScraper.cpp:383-384`), so a rate-limited search reads as no match. An IO error and a spent 429 end as DONE (3.13). So the one place that turns a network failure into something the page can count drops it, and the page reads COMPLETED, GAMES SCRAPED: 9 offline (G-05). The page's count is itself short by the thread count, since `done` is set only at hand-out (3.19): G-05's guest had ten games.
- **The scrapers parse with rapidjson and check the shape after reading it.** Several sites call `HasMember` before `IsObject`, or `GetString` before `IsString`: 3.10 and 3.8 in GamesDB (its process, its images JSON and its resources), and L-22 in IGDB's and HfsDB's token reads. The recipe builds with NDEBUG, so rapidjson's assertion is compiled out, and a wrong shape is a wild read: two SEGVs at stage C.
- **The batch scrape is a fourth-tier page over a thread whose lifetime is its own.** `ThreadedScraper::run` ends with `delete this`, while `stop()` and `isRunning()` read the static `mInstance` under no lock. L-01 is the read; L-02's harness turns it into a use-after-free, and the same window marks a finished run cancelled. Each run also leaks its `ScraperThread`s and its `std::thread` (L-23).
- **The services run their handlers on httplib's pool.** Some post to the interface thread and some do not: `/notify` (L-12), `/removegames` and the media writes (L-13), `/launch`'s walk (L-19), and `/quit`, `/shutdown` and `/restart` (L-21). The vendored httplib is the 2020 v0.7 series with no body limit (L-24).
- **The views are upstream's, with the fork's additions in three files:**
  - `ISimpleGameListView.cpp`: #210's SAVE STATES (HOLD) help, the letter jump and the filter.
  - `GridGameListView.cpp`: #243's display aspect on the tiles.
  - `DetailedContainer.cpp`: the extras' aspect and the play-time row.

  `GameNameFormatter` is upstream's: its doubled ASCENDING and its `% 24` (3.32).

## 3.2 Project conformance

- **`engineering-practices.md` § Guards must fail closed, and blindspot 22.** `Scraper.cpp:372-376` turns an unreachable server into "no results" (3.13, G-05). The success path is reached by more than success: an IO error, a spent 429 and a long Retry-After all read as done.
- **`es-player-text.md` § Outcome vocabulary.**
  - The scrape page (T31's) can only say COMPLETED for a run that reached nothing, because the run hands it no error (3.13).
  - SKIPPED - YOU CANCELLED IT can be shown over a completed run (L-02).
  - Line 4 carries `removeHtmlTags(getErrorMsg())`, curl's or a server's words, for every scraper but ScreenScraper (L-05).
- **`es-code-traps.md` § A pooled connection with the link gone is silent for a quarter of an hour (#299).**
  - None of the nine `HttpReq` constructions in the slice sets `stallTimeout` or `timeout` (L-06, `t32-bounds.py`).
  - Two are on the stack and end in `wait()`, a 20 ms sleep loop (L-18).
  - L-18's read at stage C: the token fetch runs on the **interface thread** at a batch run's start and in three manual-scrape paths, so the bound on that freeze is the connect timeout plus nothing.
- **`es-native-ui.md` § Core patterns ("a file another process writes is read uncached").** All 49 `exists`-family reads in the 42 are cached (`t32-reads.py`). ES's own writers drop their entry, so the stale case is a writer outside the process. G-09 showed a **picture** written from outside ES absent until a restart. Which cache held it is not identified (EP-29), so it is L-08's shape, not proof of the MANUAL row's gate.
- **`es-code-traps.md` § A rescan that deletes FileData drops the view first (#246).** The same free-then-read shape sits in `CollectionSystemManager::reloadCollection` behind the slice's filter (L-16, carried to T33). `POST /launch` posts raw `FileData*` from the pool thread (L-19, #774's sibling).
- **`es-player-text.md` § Every fork string ships in English and French.**
  - All 50 msgids in the slice have French (`t32-words.py`: 0 empty, 0 missing).
  - #210's SAVE STATES (HOLD) is translated with the game-save word (L-10).
  - `SystemView.cpp:233-234` shows an English dialog outside `_()` (L-11).
- **D-UI-039.** The view styles and the row that picks them are not in the menu map, and the views carry no screen title the checker can see (L-15).
- **D-UI-079 (change stays inside the lanes).** Of the stage-C proofs:
  - L-02 is in the fork's lane (the scrape page, D-UI-078).
  - 3.13 is upstream code under the fork's page.
  - 3.10, L-22, L-24, 3.27, 3.31 and 3.32 are upstream's.

  Each of these is a contained fix, so `bugs-are-agent-first.md` rule 6 applies. 3.27, 3.31 and 3.32 are views the fork does not work in: they are proposed as `bug`s only where the player sees them (3.31, 3.32), and recorded otherwise (3.27; G-04 shows no player-visible effect).

## 3.3 Spec fidelity

The brief's figures held at their hashes, with the corrections in `02` § The runs:
- `atol(` is 2 in 2;
- 25 path patterns over 27 registrations;
- 9 `HttpReq` constructions;
- the words 57 / 69 / 50, the brief having counted a comment;
- po L116 is the multi-line form, so its French is at L117.

Stage C adds three corrections:
- **3.32's second `atol` site does not wrap.** `secondsToString` folds the day back.
- **G-06's NO GAMES FIT is T31's PL-21 (#1254), not 3.16.** Corrected on #679 at 16:28 UTC.
- **L-16's `reloadCollection` then `reloadGameListView` is an either/or at `:461-464`.** The free-then-read is inside `reloadCollection`.

Of the six FAIL-at-pin leads, all six FAIL at the pin and pass their controls (`stage-c/runs.txt`). Three are stronger than the brief stated:
- 3.10 is a SEGV in the shipped build, not an assertion;
- 3.13 covers the spent 429 and the long Retry-After as well as the IO error;
- L-02 is a use-after-free.

The floor's other 27 are in `02` § The leads with their verdicts (`stage-c/floor.md`: 11 holds, 1 design, 15 findings; a read-only subagent's read, re-checked by the first reader where `floor.md` § Verification says). Two of the 15 change the picture: 3.15, a null dereference on SCRAPE NOW when the saved scraper is one this build does not register; and 3.19, which corrects G-05's 9 to ten games minus one thread.

## 3.4 Platform conformance

- **The image is M7's composition over the pin** (G-01: both literals). Every guest verdict is `image`.
- **The shipped theme has no grid view.** Grid falls back to the automatic view on the image, so L-14's per-tile read was not reached: 2.775 s against 2.786 s (G-02). 3.31's empty tile is therefore a theme-that-has-a-grid question, proved on the host only.
- **The build defines NDEBUG** (`config/functions`: the `ndebug` flag defaults on; ES's `PKG_BUILD_FLAGS` is `-gold`). This decides 3.10 and L-22: a crash, not an assertion.
- **The scrapers that ship:**
  - IGDB and ArcadeDB in every build.
  - ScreenScraper under the runtime developer login (#64, D-WORKFLOW-166).
  - TheGamesDB and HfsDB only with their macros.

  So 3.10 is reached only in a build with `GAMESDB_APIKEY`, while L-22's IGDB half and 3.16 are reached in every build by a player who set an IGDB client id.
- **The HTTP API is loopback-only by default.** WEB ACCESS opens it to the LAN, unauthenticated by upstream's design. L-24's unbounded body is reachable from the LAN then, and from any local process always (and ES runs as root).
- **A no-NIC guest reaches no scraper host.** G-07 and G-10 are `CANNOT`, with the reasons in `02` § The guest cycle; the success paths of the scrapers are therefore proved nowhere in this audit.

## 3.5 Cross-system interaction audit

### Interaction: `ScraperHttpRequest::update` x `ThreadedScraper`'s fatal list x T31's SCRAPING GAMES page

An IO error is DONE, so the reader counts no error and the page says COMPLETED (3.13, G-05). The fix must keep the 2020 intent that one game's failure does not stop a batch (a631e8c84). The reader already does that for a non-fatal code, so the fix is in the request, not the reader. Proved: `l313` (fixture), G-05 (image).

### Interaction: `stop()` x `run()`'s `delete this` x the page's `progress()`

The player's YES on CANCEL in the frame the last game ends gives two results (L-01, L-02):
- a write through a freed `ThreadedScraper`;
- `cancelled` over `finished`, so SKIPPED - YOU CANCELLED IT over a completed run.

Proved: `l02` (fixture, the window widened by a named hook).

### Interaction: a saved scraper name x a build's key set x SCRAPE NOW

The registry depends on the build's macros, while `Settings`' `Scraper` survives an upgrade. `GuiScraperStart` shows a fallback without saving it, and `ThreadedScraper::start` dereferences `getScraper()` (3.15). An image built with another key set, or an upgrade from one, crashes on SCRAPE NOW. `upgrade-and-install.md`'s case, tree; VM-provable by writing the setting on a guest.

### Interaction: IGDB's `ensureToken` x the interface thread x `generateRequests`' throw

The token fetch at a batch run's start runs on the interface thread, bounded by the connect timeout only (L-18). A later refetch on the scrape thread throws `INVALID CREDENTIALS` with no catch, and needs a 30-minute gap between searches (unproved). A malformed token body is a SEGV (L-22, `l316`).

### Interaction: the text filter x `CollectionSystemManager::reloadCollection` x `ViewController::reloadGameListView`

A grouped custom collection's root is cleared, then the bundle view's cursor is read (L-16). That is #246's shape, unproved here, and the holders are T33's.

### Interaction: `POST /launch` x the pool thread x a game-list reload

The walk over every system's files and a raw `FileData*` posted per match, with no `break`, against a reload on the interface thread (L-19). #774's sibling.

### Interaction: WEB ACCESS x httplib's unbounded body x ES as root

A LAN host can grow a request body until ES dies (L-24, tree).

## 3.6 Time to play

The slice is on the launch path at three points (01 § Read at stage C, item 10). What the window measured on the guest:
- **the populate on SCREENSHOTS:** 2.775 s from the press to a still screen in grid style (which the shipped theme draws as automatic), against 2.786 s automatic and 2.777 s for gb (G-02);
- **the list's press to `ViewController::launch`:** not timed (nothing was launched);
- **the carousel after UPDATE GAMELISTS:** framed, not timed (G-09).

The proposed fixes cost the launch path nothing: L-02's lock, 3.13's error status, the parses' shape checks, L-24's limit. L-18's fix moves a network wait **off** the interface thread at a scrape's start. No budget row exists for these numbers (`docs/vm-qa-log.md:9-18`).
