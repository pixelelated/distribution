# Forward audit — M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

Composed by `tools/t32-02.py` from this template and the generators under `tools/`; each generated section ends with its generator's "generated, asserted" line. Read at the pin `16dbac5211` (the ES worktree `feature/m6-es-app-views-scrapers-679`, clean), from the distribution worktree at `603b358a14`. Lines are the pin's. `proved:` reads `tree` (read at the lines), `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; a lead not yet proved says what will prove it.

## Coverage

{{COVERAGE}}

## The leads

§ 2's L-01 to L-17, read at their lines, and the leads this read added (L-18 to L-21). The disposition is proposed for the stage-D pause; the six that FAIL at the pin are proved at stage C by unit cases seen to fail against the unfixed extract first.

| Lead | Lines at the pin | Shape | Family | Owner | Disposition proposed | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| L-01 | `ThreadedScraper.cpp:325`, `:335` against `:241-242`; `ThreadedScraper.h:77` | `stop()` and `isRunning()` read `mInstance` and write `thread->mExitCode` under no lock while `run()` may be at `delete this` on its own thread | a lifetime or a thread | the fork (`acd7a6fee`) | a read trace; a contained fix (atomics, the null-check under the mutex) | tree |
| L-02 | `ThreadedScraper.cpp:331` with T31's `GuiScraperRun.cpp:140-141` | a `stop()` after `:235` freezes `finished` marks a finished run cancelled: SKIPPED - YOU CANCELLED IT over a completed run (T31's inherited L-02) | a check whose failure reads as success | the fork | a unit case on `progress()`'s shape (stage C) | tree; fixture at C |
| L-03 | `ThreadedScraper.cpp:53`; `ThreadedScraper.h:100`, `:111`, `:113` | the scrape thread is never joined, detached or deleted; `mExitCode` and `mPaused` cross threads as plain variables | a lifetime or a thread | the fork | with L-01 | tree |
| L-04 | `ThreadedScraper.cpp:299`, `:314` | `_("AN ERROR OCCURRED") + " :\r\n" +` the probe's or the scraper's text, one button each; B lands on the only button | a player sentence outside the vocabulary | the fork's start path, upstream's words | G-06 frames it EN and FR | tree; guest at the window |
| L-05 | T31's `GuiScraperRun.cpp:225` <- `ThreadedScraper.cpp:166` <- `Scraper.cpp:640` | the page's line 4 carries `removeHtmlTags(getErrorMsg())`, curl's or the server's words, for every scraper but ScreenScraper | a player sentence outside the vocabulary | upstream (`Scraper.cpp`), shown on the fork's page | G-05 reads line 4 | tree; guest at the window |
| L-06 | § The bounds: 9 constructions, none with a total or stall bound | `HttpReq.cpp:204`'s 10 s connect and nothing else, under a page whose only exit is CANCEL (#299's quarter of an hour); the media retry's lost `Referer` (`:596`) is fixed on T21's tip (`mOptions` reused at its `:611`), inherited | a call with no bound | upstream (rule 6) | a `stallTimeout` on the scrapers' options, as #299 did for the hasher | tree; tool-run (`t32-bounds.py`) |
| L-07 | `Scraper.cpp:607-614`, `:631-635` | a 429 whose retries are spent, a 404 and an IO error on a media download read as done: no file, the result accepted, the page COMPLETED (#1191's caller half) | a check whose failure reads as success | upstream (rule 6) | a unit case on `ImageDownloadHandle` with a doubled `HttpReq` (stage C) | tree; fixture at C |
| L-08 | `DetailedContainer.cpp:903`, `:916` (and `:817-831`, `:863`, `:873`) | a row decided from a cached read of a file written outside ES while the list is open; a remembered miss hides MANUAL or MAP until a launch. ES's own writers drop their cache entry (§ The reads' preamble), so the stale case is a writer outside the process | a read of a file another process writes | upstream (rule 6) | G-09's positive; uncached (`, false`) a stream question | tree; guest at the window |
| L-09 | `Scraper.cpp:88-177`, `:407`, `:440` | what to fetch and what to overwrite decided from the same cache, against files changed outside ES since it answered | a read of a file another process writes | upstream (rule 6) | a stream question | tree; tool-run (`t32-reads.py`) |
| L-10 | po L218 against L233 | `SAVE STATES (HOLD)` is `SAUVEGARDES (MAINTENU)`, the game-save word; L233's `SAVE STATES` is `SAUVEGARDES D’ÉTAT` | a player sentence outside the vocabulary | the fork's French (#210's string) | one catalog line | tree |
| L-11 | `SystemView.cpp:233-234` | an English sentence-case dialog, not through `_()`, with a bare `"OK"`, after `:233` writes `UIMode` without `saveFile()`. **Corrected:** the brief's second half, an empty French `msgstr` at po L116, is gettext's multi-line form: the French continues at L117 (`ERREUR : TOUS LES SYSTÈMES SONT CACHÉS, ...`) | a player sentence outside the vocabulary | upstream (rule 6) | `_()` with French; the `UIMode` write saved | tree |
| L-12 | `HttpServerThread.cpp:574` | the request body as a toast from the pool thread, unbounded, where every other route posts to the interface thread | a lifetime or a thread; a player sentence | upstream (rule 6) | G-08's `POST /notify` with a long body | tree; guest at the window |
| L-13 | `HttpServerThread.cpp:738`, `:751-755`; `HttpApi.cpp:258-260` | files removed and media written on the pool thread while the interface thread reads the same `FileData` | a lifetime or a thread | upstream (rule 6) | G-08's out-of-system `POST` (`204 No game removed`) | tree; guest at the window |
| L-14 | `GridGameListView.cpp:42-47` with `DisplayAspect.cpp:99-131` | one capture record read per tile on the interface thread at populate, on SCREENSHOTS | work on the interface thread | the fork (`12de21757`) | G-02's press-to-first-frame with N seeded captures | tree; guest at the window |
| L-15 | `docs/es-menu-map.md:135` | no row for the view styles, the row that picks them, or the SCREENSHOTS list; the views carry no screen title, so the checker cannot see them; `SystemView.cpp:552`'s computed title is #965's | a page the map does not describe | the map (D-UI-039) | a map section at stage E | tree; tool-run |
| L-16 | `ISimpleGameListView.cpp:462-464` | `reloadCollection` then `reloadGameListView`: #246's shape if the collection reload frees the view's cursor first | a lifetime or a thread | upstream; the holders `CollectionSystemManager` (T33's) | the holders listed at stage C | tree |
| L-17 | § 5's two delta commands | merge debt none | -- | -- | § The merge debt | tool-run |
| L-18 | `HfsDBScraper.cpp:195-196`, `IGDBScraper.cpp:150-151` | the token requests are built on the stack and ended by `request.wait()` (`HttpReq.cpp:638-644`, a 20 ms sleep loop) with the 10 s connect as their only bound; `ensureToken` runs from `generateRequests` (`:214`, `:169`), reached by the batch scrape's thread and by `ScraperSearchComponent::search` (`components/ScraperSearchComponent.cpp:261`, outside the 42: its thread read at stage C) | a call with no bound | upstream (rule 6) | with L-06 | tree |
| L-19 | `HttpServerThread.cpp:615-630` | `POST /launch` walks every game system's files on the pool thread while the interface thread may rebuild them, and posts a raw `FileData*` to `ViewController::launch` once per match, with no `break`: #246's shape, and two launches for a path matched twice | a lifetime or a thread | upstream (rule 6) | a read trace; G-08 reads one `/launch` | tree |
| L-20 | `HttpServerThread.cpp:299-320`, `:533-543` | `/isIdle` answers `[ true ]` while a cloud sync or the RetroAchievements proxy's work runs (it asks the scraper, the content installer, the hasher and the updater only); `/reloadgames` posts `updateGameLists` with no idle check. D-QA-057's walks wait on `/isIdle` | a check whose failure reads as success | upstream (rule 6), the fork's walks | a read trace; the stream question whether the fork's work belongs in `/isIdle` | tree |
| L-21 | `HttpServerThread.cpp:241`, `:249`, `:257` | `/quit`, `/shutdown` and `/restart` call `Utils::Platform::quitES` on the pool thread, where `/quit?confirm=` posts its dialog to the interface thread | a lifetime or a thread | upstream (rule 6) | recorded | tree |

The floor's 35, carried from the brief's § 4 table (the six that FAIL at the pin in bold); each is a unit case in `ScraperReplies`'s shape at stage C unless marked guest-only.

| # | At the pin | What a case would catch | proved: |
| --- | --- | --- | --- |
| 3.1 | `ArcadeDBJSONScraper.cpp:26` (`:34-37`) | the name cleaning in the URL | at C |
| 3.2 | `ArcadeDBJSONScraper.cpp:76`, `:85`, `:94` | a silently defaulted field | at C |
| 3.3 | `ArcadeDBJSONScraper.cpp:103` | a renamed image source yielding no media | at C |
| 3.4 | `ArcadeDBJSONScraper.cpp:121` | tag precedence; a non-string skipped | at C |
| 3.5 | `ArcadeDBJSONScraper.cpp:200` | the `:199` contract (see 3.13) | at C |
| 3.6 | `GamesDBJSONScraper.cpp:195` | the platform map drifting | at C |
| 3.7 | `GamesDBJSONScraper.cpp:293` (`:309`) | an array whose first element has no `filename` throws | at C |
| 3.8 | `GamesDBJSONScraper.cpp:402` | the resource JSON's shape | at C |
| 3.9 | `GamesDBJSONScraper.cpp:553` | the dependency queue's shape | at C |
| **3.10** | `GamesDBJSONScraper.cpp:575`; `:605`, `:607` | `HasMember` before `IsObject`: `"boxart": []` is a rapidjson assertion | at C (FAIL at the pin) |
| 3.11 | `HfsDBScraper.cpp:308`, `:343` | the `name == tagName + "type"` convention | at C |
| 3.12 | `HfsDBScraper.cpp:407`, `:584` | the arcade filter; the first-result rule | at C |
| **3.13** | `Scraper.cpp:289` (`:337`, `:372-376`) | 404 and IO error end `ASYNC_DONE` with no error: an unreachable scraper reads as "no results"; `:337` discards `process()`'s return | at C (FAIL at the pin) |
| 3.14 | `Scraper.cpp:212` | the multi-URL fallback | at C |
| 3.15 | `Scraper.cpp:41-78` | the registry lookups over an injected vector | at C |
| **3.16** | `IGDBScraper.cpp:143-144`, `:167-172`, `:314` | `process` returns `false` where the three others return `true`; IGDB offered with no client id | at C (FAIL at the pin); G-06 |
| 3.17 | `Scraper.cpp:583`; `HttpApi.cpp:210` | the Content-Type rule written twice; a non-image body kept | at C |
| 3.18 | `Scraper.cpp:779` | an id outside `getSaveAsPath`'s switch | at C |
| 3.19 | `ThreadedScraper.cpp:15`, `:155`, `:248` (fork-own) | a status landing in the wrong column of `Progress` | at C |
| 3.20 | `ThreadedScraper.cpp:103` | the state machine | at C |
| 3.21 | `HttpApi.cpp:102`, `:110` | the id scheme a web client caches | at C |
| 3.22 | `HttpApi.cpp:170` | `ImportFromJson`'s string-only rule | at C |
| 3.23 | `HttpApi.cpp:210` (`:240-253`) | `image/svg+xml` refused with no reason | at C |
| 3.24 | `HttpServerThread.cpp:93`, `:114` | the MIME table | at C |
| 3.25 | `HttpServerThread.cpp:127` | `::1` refused unless public | at C |
| 3.26 | `HttpServerThread.cpp:149-803` | the routes (§ The services: 27 registrations over 25 patterns) | guest (G-08) |
| **3.27** | `SystemView.cpp:272` (`:331`) | `_moveCursorInRange(2, -10, 5)` leaves `-3` | at C (FAIL at the pin); G-04 |
| 3.28 | `SystemView.cpp:282` | the manufacturer grouping | at C |
| 3.29 | `ISimpleGameListView.cpp:486`, `:529`, `:580` (fork-own file) | a UTF-8 lead byte as a letter; the `break` assuming name order | at C; G-03 |
| 3.30 | `BasicGameListView.cpp:101` (`:123-124`) | not found with an empty stack -> the root, silently | at C |
| **3.31** | `GridGameListView.cpp:131` (`:135-136`) (fork-own file) | `src == IMAGE` returns `getImagePath()` even when empty | at C (FAIL at the pin) |
| **3.32** | `GameNameFormatter.cpp:84-85`, `:171-185`; **and `DetailedContainer.cpp:1049`** | no year under a descending sort; `(seconds / 3600) % 24` wraps a 25-hour game -- at both `atol` sites (§ The runs' correction) | at C (FAIL at the pin) |
| 3.33 | `UIModeController.cpp:55-97` (`:72`) | a wrong press resets the unlock counter (settled) | design |
| 3.34 | `ISimpleGameListView.cpp:681` (fork-own, #210) | the #210 rule regressing | at C; G-02 |
| 3.35 | `DetailedContainer.cpp:112-140`, `:1010`, `:1043` (fork-own file) | a label without French | tool-run (`t32-words.py`: 0 without) |

## The views

{{VIEWS}}

## The scrapers

{{SCRAPERS}}

## The services

{{SERVICES}}

## The reads

{{READS}}

## The bounds

{{BOUNDS}}

## The words

{{WORDS}}

- **Two counting rules, and a comment.** `git grep -c -F '_("'` prints 58 lines and `git grep -o` 70 occurrences; both count `ISimpleGameListView.cpp:905`'s `// _("Parent folder")`, a comment `xgettext` does not extract. The calls are 57 lines and 69 calls with 50 distinct msgids; with the comment's, 51 (its French at po L4924, `Dossier parent`).
- **L115/L116, corrected:** the msgid `ERROR: EVERY SYSTEM IS HIDDEN, RE-DISPLAYING ALL OF THEM NOW` (`SystemView.cpp:243`) has French: `msgstr ""` at L116 is the multi-line form's first line and the text is at L117. Every one of the 50 has French at the pin (0 empty, 0 missing).
- **L218 against L233** (L-10): `SAVE STATES (HOLD)` reads `SAUVEGARDES (MAINTENU)`; `SAVE STATES` reads `SAUVEGARDES D’ÉTAT`.
- **The dialog words:** `ThreadedScraper.cpp:299` and `:314` (`AN ERROR OCCURRED` + the text, one button: L-04); `SystemView.cpp:233-234` (English, not through `_()`, `"OK"`: L-11); `SystemView.cpp:243` (`_()` with `_("OK")`); the toast `HttpServerThread.cpp:574` (the request body as sent: L-12).

## The structure

- **The modes** (`UIModeController.{cpp,h}`): Full, Basic, Kid, Kiosk; the unlock sequence `listen()` `:55-97`, a wrong press resetting the counter at `:72` (3.33, settled); `UIMode = Full` and `saveFile()` at `:102-103` -- the right store for an ES-only mode. `SystemView.cpp:233`'s `UIMode` write has no `saveFile()` (L-11).
- **The registry and the build macros** (§ The scrapers): ScreenScraper under `SCREENSCRAPER_DEV_LOGIN` or `SCREENSCRAPER_RUNTIME_DEV_LOGIN` (#64), TheGamesDB under `GAMESDB_APIKEY`, HfsDB under `HFS_DEV_LOGIN`, IGDB and ArcadeDB always (D-QA-003; `device-builds.md` § Build credentials). The macro names only; no value is read.
- **The include cycle:** every `.cpp` under `views/` and `services/` includes `views/ViewController.h`, and `ViewController.cpp` includes the slice's headers back; taken as given (the brief, § 2). 47 include lines of the slice's 22 headers come from 23 files outside the 42 (`stage-a/callers.out`).
- **`httplib.h`'s currency:** to be judged at stage C by content against cpp-httplib's 2020 series (no version line; `CPPHTTPLIB_OPENSSL_SUPPORT` defined nowhere, so the server is plain HTTP on `127.0.0.1:1234`, `:821-828`).

## The merge debt

`cada856d86` is the merge base with `rocknix/master` (`f6c542872e`), one commit after `bccd715707` (the base the stale `upstream/master` ref still names); 0 of the 14 upstream commits since the base touch the 42 paths and the numstat prints nothing; the fork's six files carry `Scraper.cpp` 2/2, `ThreadedScraper.cpp` 56/22, `ThreadedScraper.h` 30/4, `DetailedContainer.cpp` 21/0, `GridGameListView.cpp` 14/0 and `ISimpleGameListView.cpp` 45/18 (168/46 against both bases); T21's ES tip carries, inherited and not merged here, `Scraper.cpp` 28/8 and `Scraper.h` 5/0 and adds `ScraperReplies.cpp` 51 and `ScraperReplies.h` 22 (`3ae9610b0`, `44d3c7e25`, `e38dcdefd`).

## The runs

Every § 5 run of stage A (`stage-a/runs.sh`, its output `stage-a/runs.out`, rc 0, 2 s wall for the whole block), with what a FAIL would mean. The stage-C runs (the include graph, the unit build) are stage C's.

| Run | Figure | rc | A FAIL would mean |
| --- | --- | ---: | --- |
| the scope | 46 all, 4 excluded, 42; scrapers 14, services 5, views 23 (gamelist 18); 20 `.cpp`, 22 `.h` | 0 | the slice is not the brief's |
| the worktree and the bases | the pin; 0 changes; `cada856d86`; `bccd715707`; 14; 725; 1; `f6c542872e`; `3ae9610b0` | 0 | a read of the wrong tree (blindspot 75) |
| the lines two ways | `wc -l` 17,306; `grep -c` 17,311; 5 without a trailing newline | 0 | a file changed |
| the fork's delta | 6 `M`; 168 46 against both bases; 0 fork-added (rc 1 of the count) | 0 | a fork file the brief missed |
| upstream's delta | 0 commits, 0 numstat rows (rc 1 each); 42 at both refs; the tree hashes as the brief gives | 0 | merge debt |
| T21's deltas | the six rows; `3ae9610b0 44d3c7e25 e38dcdefd` | 0 | T21's branch moved |
| the fork's commits | 2 / 1 / 1 / 5 / 1 / 4; 10; 11 | 0 | history the brief did not read |
| the strings | 58 lines in 9 files; 70 occurrences (the comment at `ISimpleGameListView.cpp:905` among them: § The words) | 0 | a string added or lost |
| the dialogs | `new Gui` 19 in 5 files; `GuiMsgBox` 8 | 0 | a dialog the table misses |
| the threads | `std::thread` 13 in 5; `new std::thread` `ThreadedScraper.cpp:53`, `HttpServerThread.cpp:74`; `delete this` `:241`; `mInstance` 9; `.detach(` 0; `postToUiThread(` 13 in 3 | 0 | a thread unaccounted for |
| the bounds | `HttpReq` 83 lines in 14 files, 95 occurrences; `new HttpReq(` at the seven lines; 0 bounds set (rc 1) | 0 | a bound the table misses -- and the two stack constructions this grep cannot see (§ The bounds) |
| the success-reads | `214 ... 688`; `448 607`; `144 164 230 324 331` | 0 | a line moved |
| the reads | `exists(` 49 lines in 6 files, 50 occurrences, 0 uncached; DetailedContainer's 19 lines | 0 | a read unaccounted for |
| the process starts and parses | 0 process starts; `std::stoi(` 3 in 1; `std::stoul(` 0; `atoi(` 0; `toInteger(` 6 in 5; **`atol(` 2 in 2** | 0 | **the brief expects 1 in 1: the second site is `DetailedContainer.cpp:1049`, 3.32's play time, a count the brief missed** |
| the help bars and the views | `SystemView.cpp`, `ISimpleGameListView.cpp`; the five `getName()` defaults; `_moveCursorInRange` at the ten lines | 0 | a view with its own bar |
| the T21-class uses | 51 lines in 14 files; the macro names at the lines § 1 gives | 0 | a credential surface the scan must disposition |
| the non-ASCII comments | 0 files; 0 adjacent (by `-F`; rc 1) | 0 | an xgettext stop |
| the harness sweep | no basename; 15 `.py`; 19 `*Tests.cpp` | 0 | a test already covers the slice |
| the French | L218/219, L233/234; L115/L116; `706 ... 706 with French, 0 without` (`bccd715707`) and `703 ... 703 with French, 0 without` (`cada856d86`) | 0 | a string without French |
| the menu map | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`; `:135`; 989 lines | 0 | a screen the map lost |
| the compile | `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2; `g++` on `ThreadedScraper.cpp`: `es-core/src/HttpReq.h:5:10: fatal error: curl/curl.h: No such file or directory` rc 1 | 2 / 1 | -- (`CANNOT` on the host, as § 5 names) |
| the stand-in syntax check (`stage-a/syntax-check.out`) | rc 0 on the seven scrapers' `.cpp` files and `GameNameFormatter.cpp` (T21's script and 13 fakes) | 0 | a scraper that does not compile against the stand-ins |
| the removal check | empty against `603b358a14` and `121d0180f0`; `TIPHASH` refused; the ES diff against the pin empty | 0 | a change under `packages`, `projects` or `tools` |

**The generators, each seen to exit 1 on a constructed drift before it was trusted** (`stage-b/generators.txt`): `t32-reads.py` (a count of 48; `ISimpleGameListView.cpp` dropped from the paths: its two groups name lines with no site), `t32-bounds.py` (6, and 7 against its 9; `GamesDBJSONScraperResources.cpp` dropped), `t32-services.py` (the brief's 16 as the pattern count), `t32-scrapers.py` (2 gated), `t32-views.py` (6 help bars), `t32-words.py` (the brief's 58 / 70 / 51 / 1 empty). Two defects in my own generators were found by their first runs and fixed before use: `t32-views.py`'s precedence slip (it flagged `SystemView` despite its note) and its count of `ViewController`'s help bar (T2's file, outside the 42).

**Corrections to the brief, each a count and none a finding:** `atol(` is 2 in 2 files (above); the services are 25 distinct path patterns over 27 registrations, 16 of them plain strings (the brief's "16 distinct paths" counts the plain strings only); the `HttpReq` constructions are 9, the seven `new HttpReq(` and two on the stack (L-18); the strings are 57 code lines, 69 calls and 50 msgids, the brief's 58 / 70 / 51 counting a comment; L116's `msgstr ""` continues at L117 (L-11 corrected).

## The guest cycle

To be written when the window is granted and run (stage B's request on #679; `stage-b/window-plan.md`).

## The streams

Written by the coordinator after stage D (as for T21 and T26); the lane leaves this heading and the pause's dispositions.

## Positives

Stage C's: each unit case's FAIL against the unfixed extract, then its PASS.

## The #585 lines owed

Stage D's: one per upstream-carried defect closed under rule 6, in the shape the lane writes, never sent.

## What T33 to T37 inherit

§ 5 item 3's seven, with their lines:

1. **The views' provenance table** (6 fork-modified / 36 upstream-carried; both bases named): § Coverage.
2. **The cached-read table with its writers** (49 lines, 50 calls; ES's own writers drop their entry, a writer outside the process does not): § The reads.
3. **The thread-and-lifetime table**: the scrape thread (`ThreadedScraper.cpp:53`, never joined, L-01, L-03), the server thread (`HttpServerThread.cpp:74`) and httplib's pool (`:145`) with every route's work and posts (§ The services), L-12, L-13, L-19, L-21.
4. **The bounds table** (every `HttpReq` construction with its options; none bounded but the 10 s connect): § The bounds, L-06, L-18.
5. **The scrapers' outcome routing** (status -> `processError` -> `Progress` -> the page's line 4): § The scrapers' last paragraph.
6. **`httplib.h`'s currency note**: § The structure (stage C completes it).
7. **The map section for the views**: L-15, at stage E.
