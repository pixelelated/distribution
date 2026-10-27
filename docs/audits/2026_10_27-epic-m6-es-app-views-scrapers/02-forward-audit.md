# Forward audit — M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

Composed by `tools/t32-02.py` from this template and the generators under `tools/`; each generated section ends with its generator's "generated, asserted" line. Read at the pin `16dbac5211` (the ES worktree `feature/m6-es-app-views-scrapers-679`, clean), from the distribution worktree at `603b358a14`. Lines are the pin's. `proved:` reads `tree` (read at the lines), `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`; a lead not yet proved says what will prove it.

## Coverage

| Path | Lines (`grep -c`) | Inventory tier | Read tier | Fork +/- (against `cada856d86`) | Leads naming it |
| --- | ---: | --- | --- | ---: | --- |
| `es-app/src/scrapers/ArcadeDBJSONScraper.cpp` | 243 | upstream-carried | upstream-carried | 0/0 | 3.1, 3.2, 3.3, 3.4, 3.5 |
| `es-app/src/scrapers/ArcadeDBJSONScraper.h` | 46 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/scrapers/GamesDBJSONScraper.cpp` | 633 | upstream-carried | upstream-carried | 0/0 | 3.10, 3.6, 3.7, 3.8, 3.9 |
| `es-app/src/scrapers/GamesDBJSONScraper.h` | 51 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/scrapers/GamesDBJSONScraperResources.cpp` | 201 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/scrapers/GamesDBJSONScraperResources.h` | 45 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/scrapers/HfsDBScraper.cpp` | 633 | upstream-carried | upstream-carried | 0/0 | 3.11, 3.12, L-18 |
| `es-app/src/scrapers/HfsDBScraper.h` | 66 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/scrapers/IGDBScraper.cpp` | 349 | upstream-carried | upstream-carried | 0/0 | 3.16, L-18 |
| `es-app/src/scrapers/IGDBScraper.h` | 62 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/scrapers/Scraper.cpp` | 813 | fork-own | fork-modified | 2/2 | 3.10, 3.13, 3.16, 3.1, 3.11, 3.12, 3.14, 3.15, 3.17, 3.18, 3.19, 3.2, 3.20, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, L-01, L-02, L-03, L-04, L-05, L-07, L-09, L-18 |
| `es-app/src/scrapers/Scraper.h` | 289 | upstream-carried | upstream-carried | 0/0 | L-01, L-03 |
| `es-app/src/scrapers/ThreadedScraper.cpp` | 339 | fork-own | fork-modified | 56/22 | 3.19, 3.20, L-01, L-02, L-03, L-04, L-05 |
| `es-app/src/scrapers/ThreadedScraper.h` | 119 | fork-own | fork-modified | 30/4 | L-01, L-03 |
| `es-app/src/services/HttpApi.cpp` | 344 | upstream-carried | upstream-carried | 0/0 | 3.17, 3.21, 3.22, 3.23, L-13 |
| `es-app/src/services/HttpApi.h` | 35 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/services/HttpServerThread.cpp` | 834 | upstream-carried | upstream-carried | 0/0 | 3.24, 3.25, 3.26, L-12, L-13, L-19, L-20, L-21 |
| `es-app/src/services/HttpServerThread.h` | 30 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/services/httplib.h` | 5713 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/SystemView.cpp` | 1638 | upstream-carried | upstream-carried | 0/0 | 3.27, 3.28, L-11, L-15 |
| `es-app/src/views/SystemView.h` | 142 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/SystemViewControlWrapper.h` | 184 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/UIModeController.cpp` | 197 | upstream-carried | upstream-carried | 0/0 | 3.33 |
| `es-app/src/views/UIModeController.h` | 63 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/BasicGameListView.cpp` | 227 | upstream-carried | upstream-carried | 0/0 | 3.30 |
| `es-app/src/views/gamelist/BasicGameListView.h` | 49 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/CarouselGameListView.cpp` | 207 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/CarouselGameListView.h` | 52 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/DetailedContainer.cpp` | 1450 | fork-own | fork-modified | 21/0 | 3.32, 3.35, L-08 |
| `es-app/src/views/gamelist/DetailedContainer.h` | 187 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/DetailedGameListView.cpp` | 66 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/DetailedGameListView.h` | 38 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/GameNameFormatter.cpp` | 269 | upstream-carried | upstream-carried | 0/0 | 3.32 |
| `es-app/src/views/gamelist/GameNameFormatter.h` | 36 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/GridGameListView.cpp` | 347 | fork-own | fork-modified | 14/0 | 3.31, L-14 |
| `es-app/src/views/gamelist/GridGameListView.h` | 65 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/IGameListView.cpp` | 49 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/IGameListView.h` | 57 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/ISimpleGameListView.cpp` | 937 | fork-own | fork-modified | 45/18 | 3.29, 3.34, L-16 |
| `es-app/src/views/gamelist/ISimpleGameListView.h` | 102 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/VideoGameListView.cpp` | 65 | upstream-carried | upstream-carried | 0/0 | - |
| `es-app/src/views/gamelist/VideoGameListView.h` | 39 | upstream-carried | upstream-carried | 0/0 | - |

generated, asserted: 42 paths; read tiers fork-modified 6, upstream-carried 36, fork-added 0; inventory fork-own 6, upstream-carried 36

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

| View | Base | Style (`getName()` default) | Draws | Populate | Help bar | Reads per item before the first frame |
| --- | --- | --- | --- | --- | --- | --- |
| `SystemView` | `GuiComponent` | - | the system carousel (`mCarousel`, `SystemView.cpp:196` `populate`, `TextureLoader::paused` while it runs) | `SystemView.cpp:196` | `SystemView::getHelpPrompts` | per visible system: its theme's view elements (`getViewElements`, when `mViewNeedsReload`) and its extras (`loadExtras`) -- after UPDATE GAMELISTS, every system's again (G-09) |
| `BasicGameListView` | `ISimpleGameListView` | `basic` (`BasicGameListView.h:31`) | `TextListComponent` (`mList`, theme element `gamelist`, `:44`) | `BasicGameListView.cpp:61` | `ISimpleGameListView::getHelpPrompts` (inherited) | per file: `GameNameFormatter::getDisplayName` (`:76`), metadata only; no file read |
| `DetailedGameListView` | `BasicGameListView` | `detailed` (`DetailedGameListView.h:24`) | Basic's list and the `DetailedContainer` panel (the `md_*` and the theme's extras) | `BasicGameListView.cpp:61` (`BasicGameListView`'s) | `ISimpleGameListView::getHelpPrompts` (inherited) | Basic's populate; on each cursor move the container's cached `exists(` reads (§ The reads, `:817-916`) |
| `VideoGameListView` | `BasicGameListView` | `video` (`VideoGameListView.h:26`) | Basic's list and the container's video | `BasicGameListView.cpp:61` (`BasicGameListView`'s) | `ISimpleGameListView::getHelpPrompts` (inherited) | as Detailed; the video on each cursor move |
| `GridGameListView` | `ISimpleGameListView` | `grid` (`GridGameListView.h:36`) | `ImageGridComponent` (`mGrid`, theme element `gamegrid`, `:229`) | `GridGameListView.cpp:156` | `ISimpleGameListView::getHelpPrompts` (inherited) | per file: `getImagePath` (`:131-153`, 3.31) and, for a folder, a cached `exists` (`:208`); **on SCREENSHOTS (IMAGEVIEWER), `DisplayAspect::forScreenshot(file)` per tile through `setTileDecorator` (`:42-47`) -- a capture record read per tile (`DisplayAspect.cpp:99-131`), L-14** |
| `CarouselGameListView` | `ISimpleGameListView` | `gamecarousel` (`CarouselGameListView.h:32`) | `CarouselComponent` (`mList`, theme element `gamecarousel`, `:37`) | `CarouselGameListView.cpp:68` | `ISimpleGameListView::getHelpPrompts` (inherited) | per file: `getDisplayName` (`:83`), metadata only |

generated, asserted: 6 views (the five styles and the carousel); getHelpPrompts defined by 2 classes: ISimpleGameListView, SystemView; 9 view classes under views/ in all

## The scrapers

| Scraper | Class | Compiled under | Hosts (scheme://host) | Options its requests carry | Success-reads |
| --- | --- | --- | --- | --- | --- |
| ScreenScraper | `ScreenScraperScraper` | `SCREENSCRAPER_DEV_LOGIN SCREENSCRAPER_RUNTIME_DEV_LOGIN` | T21's | T21's (`ScreenScraper.*`, #668): read there; its probe `getThreadCount` without bounds (T21 `02:23`), its media `Referer` at `Scraper.cpp:541-546` | T21's |
| TheGamesDB | `TheGamesDBScraper` | `GAMESDB_APIKEY` | https://api.thegamesdb.net (`:199`) | none on search (`ScraperHttpRequest`, `:267`); the resources fetch with no options (`GamesDBJSONScraperResources.cpp:153`) | `process` `:576` returns `true` on a parse error after `setError` (`:585-587`) and on every early exit; `:605-607` reads `HasMember` before `IsObject` (3.10); `getBoxartImage` `:293-309` throws on an array whose first element has no `filename` (3.7) |
| HfsDB | `HfsDBScraper` | `HFS_DEV_LOGIN` | https://db.hfsplay.fr (`:195`) | the Basic authorization header (`:179`, `:190`) and the bearer token (`:287`) | `process` `:584` returns `true` on a parse error after `setError` (`:592-594`); the token's failure throws `_("INVALID CREDENTIALS")` (`:217`), raised by `ThreadedScraper::start` as AN ERROR OCCURRED |
| IGDB | `IGDBScraper` | always | https://id.twitch.tv (`:150`), https://api.igdb.com (`:187`), https://images.igdb.com (`:266`), https://www.youtube.com (`:305`) | the Content-Type header and the POST body (`:146`, `:189`, `:205`, `:215`); the client id and its secret from `Settings` (D-QA-003, #274), never a build macro | `process` `:314` returns `false` on a parse error (`:322-324`) and on a non-array (`:331`) -- the one scraper that does (3.16's remainder); offered with no client id, `ensureToken` returns `false` at `:144` and `generateRequests` throws `_("INVALID CREDENTIALS")` at `:172` |
| ArcadeDB | `ArcadeDBScraper` | always | http://adb.arcadeitalia.net (`:29`) | none | `process` `:200` returns `true` on a parse error after `setError` (`:208-210`); its `:199` comment's contract (`false` only at the scrap-per-minute limit) is dead: `Scraper.cpp:337` discards the return (3.13) |

generated, asserted: 5 scrapers in the registry, 3 under a build macro (by name), 2 always

The routing, every scraper but ScreenScraper: `ScraperHttpRequest::update` (`Scraper.cpp:289`) ends `ASYNC_DONE` with no error on a 404 or an IO error (`:372-376`, 3.13), retries a 429 (`:343-361`, `Retry-After` at `:351`; T21's `44d3c7e25` reads it through `ScraperReplies`, inherited), and calls `setError` on any other failure (`:638-640`, the body's words: L-05); `process()`'s return is discarded at `:337`. An error becomes the handle's status, `ThreadedScraper::processError` (`:155-175`) counts it in `errors` or, for its seven whole-run statuses (`:157`), sets `failed`, and the page's line 4 (T31's `GuiScraperRun`) shows `removeHtmlTags(getErrorMsg())`.

## The services

| Line | Method | Path | On the pool thread | Posts to the interface thread | Writes |
| --- | --- | --- | --- | --- | --- |
| `:149` | GET | `/` | the web page (`/` serves index.html's body) | - | - |
| `:157` | GET | `/favicon.png` | the favicon from resources | - | - |
| `:167` | GET | `/index.html` | a page with Reload games and Quit buttons that call `/reloadgames` and `/quit` | - | - |
| `:219` | GET | `/quit` | `?confirm=switchscreen` / `menu`: a confirmation; else `Utils::Platform::quitES()` at `:241` on the pool thread | a YES/NO `GuiMsgBox` (`:229`) | - |
| `:244` | GET | `/shutdown` | `quitES(SHUTDOWN)` at `:249` on the pool thread | - | - |
| `:252` | GET | `/restart` | `quitES(REBOOT)` at `:257` on the pool thread | - | - |
| `:260` | GET | `/emukill` | `ApiSystem::emuKill()` (`:264`, T21's) | - | - |
| `:268` | GET | `/caps` | the capabilities JSON (`HttpApi`, `"Version"` `HttpApi.cpp:332`) | - | - |
| `:276` | GET | `/systems` | every system as JSON, read from `sSystemVector` on the pool thread | - | - |
| `:284` | GET | `/runningGame` | the running game's JSON, `201` with none | - | - |
| `:299` | GET | `/isIdle` | `[ true ]` 200 when no game runs and neither the scraper, the content installer, the hasher nor the updater is running (`:304-308`); else `[ false ]` 201. A cloud sync or the RetroAchievements proxy's work is not asked (D-QA-057's walks rely on it) | - | - |
| `:323` | GET | `R"(/systems/(/?.*)/logo)"` | a system's logo from its theme | - | - |
| `:353` | GET | `R"(/systems/(/?.*)/games)"` | a system's games as JSON, walked on the pool thread | - | - |
| `:370` | GET | `R"(/systems/(/?.*)/games/(/?.*)/media/(/?.*))"` | a game's media file by metadata name | - | - |
| `:407` | POST | `R"(/systems/(/?.*)/games/(/?.*)/media/(/?.*))"` | `HttpApi::ImportMedia` (`:440`): the media written on the pool thread (`HttpApi.cpp:258`, `writeAllText` in place, Backlog #1186), the game's metadata set there (L-13) | `onFileChanged(game, FILE_METADATA_CHANGED)` (`:443`) | the media file; the metadata in memory |
| `:456` | POST | `R"(/systems/(/?.*)/games/(/?.*))"` | `HttpApi::ImportFromJson` (`:476`): the game's metadata set on the pool thread (L-13) | `onFileChanged(game, FILE_METADATA_CHANGED)` (`:479`) | the metadata in memory |
| `:491` | GET | `R"(/systems/(/?.*)/games/(/?.*))"` | a game's JSON | - | - |
| `:514` | GET | `R"(/systems/(/?.*))"` | a system's JSON | - | - |
| `:533` | GET | `/reloadgames` | nothing on the pool thread; no idle check | `GuiMenu::updateGameLists(w, false)` (`:539`) | - |
| `:545` | POST | `/messagebox` | the body as a message box's text | a `GuiMsgBox` (`:559`) | - |
| `:562` | POST | `/notify` | **`mWindow->displayNotificationMessage(req.body)` at `:574`, on the pool thread, unbounded** (L-12) | - | the window's toast queue, from the pool thread |
| `:577` | POST | `/storage/event` | a storage event line | its handling (`:592`) | - |
| `:599` | POST | `/launch` | `getFilesRecursive(GAME)` over every game system on the pool thread, no `break` on a match (`:615-630`) | **a raw `FileData*` to `ViewController::launch` (`:623-626`), one post per match** | - |
| `:632` | POST | `R"(/addgames/(/?.*))"` | `loadGamelistFile` and `updateGamelist(system)` on the pool thread (`:659`, `:688`); a `new SystemData` for an unloaded system, deleted at `:676`/`:692` | `updateGameLists` (`:698`) or `onFileChanged(root, FILE_METADATA_CHANGED)` (`:702-704`) | gamelist.xml (`updateGamelist`) |
| `:711` | POST | `R"(/removegames/(/?.*))"` | `loadGamelistFile` against the system's own `fileMap`; each listed file's recovery entry removed and the file deleted on the pool thread (`:751-755`, a cached `exists` first); the `FileData` leaked on purpose (`:771`) (L-13) | `onFileChanged(root, FILE_REMOVED)` per system (`:776-779`) | the game files removed |
| `:786` | GET | `R"(/resources/(/?.*))"` | a resource file | - | - |
| `:803` | GET | `R"(/(/?.*))"` | any other path under the web root, else 404 | - | - |

generated, asserted: 27 registrations over 25 distinct path patterns (16 plain strings, 9 raw regex); isAllowed() in every handler (27 calls); 10 postToUiThread( calls; listen(ip, 1234) at :828

## The reads

| Line | Reads | Writer while ES runs | Cache | A remembered answer reads as | Disposition proposed |
| --- | --- | --- | --- | --- | --- |
| `DetailedContainer.cpp:667` | a folder's snapshot: its first game's titleshot / boxart / fanart / cartridge / mix | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss falls to the next source or the default picture until a launch | recorded with L-08 (the same rule) |
| `DetailedContainer.cpp:669` | a folder's snapshot: its first game's titleshot / boxart / fanart / cartridge / mix | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss falls to the next source or the default picture until a launch | recorded with L-08 (the same rule) |
| `DetailedContainer.cpp:677` | a folder's snapshot: its first game's titleshot / boxart / fanart / cartridge / mix | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss falls to the next source or the default picture until a launch | recorded with L-08 (the same rule) |
| `DetailedContainer.cpp:679` | a folder's snapshot: its first game's titleshot / boxart / fanart / cartridge / mix | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss falls to the next source or the default picture until a launch | recorded with L-08 (the same rule) |
| `DetailedContainer.cpp:681` | a folder's snapshot: its first game's titleshot / boxart / fanart / cartridge / mix | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss falls to the next source or the default picture until a launch | recorded with L-08 (the same rule) |
| `DetailedContainer.cpp:756` | the per-game theme extras' xml (by stem, by CRC32, then theme.xml) | the player or a theme installer | cached | a remembered miss shows no per-game extras until a launch | left cached: theme files, not game content |
| `DetailedContainer.cpp:762` | the per-game theme extras' xml (by stem, by CRC32, then theme.xml) | the player or a theme installer | cached | a remembered miss shows no per-game extras until a launch | left cached: theme files, not game content |
| `DetailedContainer.cpp:765` | the per-game theme extras' xml (by stem, by CRC32, then theme.xml) | the player or a theme installer | cached | a remembered miss shows no per-game extras until a launch | left cached: theme files, not game content |
| `DetailedContainer.cpp:768` | the per-game theme extras' xml (by stem, by CRC32, then theme.xml) | the player or a theme installer | cached | a remembered miss shows no per-game extras until a launch | left cached: theme files, not game content |
| `DetailedContainer.cpp:771` | the per-game theme extras' xml (by stem, by CRC32, then theme.xml) | the player or a theme installer | cached | a remembered miss shows no per-game extras until a launch | left cached: theme files, not game content |
| `DetailedContainer.cpp:817` | the selected game's picture source (titleshot / boxart / fanart / cartridge / mix) | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss shows the fallback picture until a launch | L-08: the stream with :903 and :916 |
| `DetailedContainer.cpp:819` | the selected game's picture source (titleshot / boxart / fanart / cartridge / mix) | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss shows the fallback picture until a launch | L-08: the stream with :903 and :916 |
| `DetailedContainer.cpp:827` | the selected game's picture source (titleshot / boxart / fanart / cartridge / mix) | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss shows the fallback picture until a launch | L-08: the stream with :903 and :916 |
| `DetailedContainer.cpp:829` | the selected game's picture source (titleshot / boxart / fanart / cartridge / mix) | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss shows the fallback picture until a launch | L-08: the stream with :903 and :916 |
| `DetailedContainer.cpp:831` | the selected game's picture source (titleshot / boxart / fanart / cartridge / mix) | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss shows the fallback picture until a launch | L-08: the stream with :903 and :916 |
| `DetailedContainer.cpp:863` | the marquee (getMarqueePath) | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves the marquee blank until a launch | L-08 |
| `DetailedContainer.cpp:873` | each md_* image's metadata path | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss leaves the image blank until a launch | L-08 |
| `DetailedContainer.cpp:903` | the manual or the magazine (two calls), PreloadMedias off (2 calls) | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss hides MANUAL (or shows NO MANUAL) until a launch | L-08: the guest's G-09 positive; a stream question |
| `DetailedContainer.cpp:916` | the map, PreloadMedias off | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss hides MAP until a launch | L-08: as :903 |
| `GamesDBJSONScraperResources.cpp:37` | the scrapers' resource directory | ES itself (createDirectory, :38) | cached | a remembered miss calls createDirectory on a directory that exists: harmless | left cached: nothing changes on screen |
| `GridGameListView.cpp:208` | a folder tile's image (getImagePath) | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss names the folder without its picture flag at populate | recorded |
| `HttpServerThread.cpp:754` | the delete route: the game's own file before removeFile | the player, a cloud restore of ROMs | cached | a remembered miss skips the delete: the safe direction | left cached (the brief's reading confirmed) |
| `ISimpleGameListView.cpp:619` | the theme's logo element path | a theme installer | cached | a remembered miss leaves the header without its logo | left cached: theme files |
| `ISimpleGameListView.cpp:910` | the system's logo property, for the parent folder's row | a theme installer | cached | a remembered miss gives the .. row no picture | left cached: theme files |
| `Scraper.cpp:88` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:92` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:96` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:100` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:104` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:108` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:112` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:116` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:120` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:124` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:128` | hasAnyMedia: each media path a game's metadata names | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered hit for a file removed since counts the game as having media: GAMES MISSING ALL MEDIA skips it | L-09: a stream question (uncached, or the scrape's run resetting the cache first) |
| `Scraper.cpp:137` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:141` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:145` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:149` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:153` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:157` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:161` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:165` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:169` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:173` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:177` | hasMissingMedia: the same paths | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | a remembered miss for a file restored since counts it missing: the game is fetched again | L-09: as above |
| `Scraper.cpp:407` | MDResolveHandle: the media path already in the game's metadata | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | with ScrapeOverWrite off, a remembered miss downloads over a file the player kept | L-09: a stream question |
| `Scraper.cpp:440` | MDResolveHandle: the save-as path the download would write | outside ES only (cloud_content_restore's game content, the player over SSH); the scraper and the API write through Utils::FileSystem and drop the entry | cached | as :407: a remembered miss overwrites; a remembered hit keeps a file removed since and records its path | L-09: a stream question |
| `Scraper.cpp:808` | getSaveAsPath: the media folder under the system's root | ES itself (createDirectory, :809); the player | cached | a remembered hit for a folder removed since leaves the download nowhere to land (the write fails) | recorded |

generated, asserted: 49 lines, 50 calls, 0 uncached, in 6 files

## The bounds

| Site | Function | Options | Connect | Total | Stall | Requests |
| --- | --- | --- | --- | --- | --- | --- |
| `GamesDBJSONScraperResources.cpp:153` | TheGamesDBJSONRequestResources::fetchResource | none (`new HttpReq(path)`) | 10 s | none | none | the platform, genre and developer lists from api.thegamesdb.net (under GAMESDB_APIKEY) |
| `HfsDBScraper.cpp:195` | HfsDBScraper::ensureToken, on the stack, then `request.wait()` (`:196`) | `options` (`:179`): the Basic authorization header only | 10 s | none | none | the token, from `generateRequests` (`:214`) -- the batch scrape's thread, or `ScraperSearchComponent::search` (`components/ScraperSearchComponent.cpp:261`, outside the 42) for one game |
| `IGDBScraper.cpp:150` | IGDBScraper::ensureToken, on the stack, then `request.wait()` (`:151`) | `options` (`:146`): the Content-Type header and the POST body only | 10 s | none | none | the token, from `generateRequests` (`:169`), as HfsDB's; not made without a client id (`:143-144`) |
| `Scraper.cpp:267` | ScraperHttpRequest's constructor | the scraper's own, copied into `mOptions` (`:265-266`): headers and the POST body only -- HfsDB `:179`, `:287`; IGDB `:146`, `:189`, `:205`, `:215`; none for ArcadeDB and TheGamesDB | 10 s | none | none | every search request of the four upstream scrapers |
| `Scraper.cpp:302` | ScraperHttpRequest::update, the 429 retry | `mOptions`, as `:267` | 10 s | none | none | the same request again after `Retry-After` |
| `Scraper.cpp:332` | ScraperHttpRequest::update, the dependency queue | `mOptions`, as `:267` | 10 s | none | none | TheGamesDB's dependent requests (`preProcess`) |
| `Scraper.cpp:564` | ImageDownloadHandle's constructor (ScreenScraper media, resized) | `options` (`:539`): `outputFilename`, the ScreenScraper `Referer` header (`:541-546`) | 10 s | none | none | a media download from ScreenScraper with maxwidth/maxheight |
| `Scraper.cpp:567` | ImageDownloadHandle's constructor (every other media) | `options` (`:539`): `outputFilename`, and the `Referer` for a ScreenScraper media path | 10 s | none | none | every scraper's media download |
| `Scraper.cpp:596` | ImageDownloadHandle::update, the 429 retry | none: `new HttpReq(url, mSavePath)`, the two-string constructor -- the first request's `Referer` header is not carried | 10 s | none | none | the media download again after `Retry-After` |

generated, asserted: 9 constructions in 4 files (7 `new HttpReq(`, 2 on the stack); 0 set a total or stall bound

## The words

| msgid | Sites | French (po line) |
| --- | --- | --- |
| `AN ERROR OCCURRED` | `ThreadedScraper.cpp:299`, `ThreadedScraper.cpp:314` | UNE ERREUR EST SURVENUE (L40) |
| `BACK` | `ISimpleGameListView.cpp:709` | RETOUR (L215) |
| `Back to %s` | `ISimpleGameListView.cpp:904` | Retourner vers %s (L240) |
| `Basic` | `UIModeController.cpp:11` | Basique (L70) |
| `CHOOSE` | `ISimpleGameListView.cpp:690` | CHOISIR (L212) |
| `COLLECTIONS` | `SystemView.cpp:524` | COLLECTIONS (L131) |
| `CONFIGURATION` | `SystemView.cpp:708` | CONFIGURATION (L146) |
| `DO YOU WANT TO SWITCH THE SCREEN ?` | `HttpServerThread.cpp:229` | VOULEZ-VOUS CHANGER D’ÉCRAN ? (L3497) |
| `Developer` | `DetailedContainer.cpp:118` | Développeur (L22) |
| `ERROR: EVERY SYSTEM IS HIDDEN, RE-DISPLAYING ALL OF THEM NOW` | `SystemView.cpp:243` | ERREUR : TOUS LES SYSTÈMES SONT CACHÉS, TOUS LES RÉAFFICHER IMMÉDIATEMENT (L115) |
| `FAVORITE` | `ISimpleGameListView.cpp:727`, `ISimpleGameListView.cpp:734`, `ISimpleGameListView.cpp:737` | FAVORIS (L230) |
| `FILES` | `SystemView.cpp:915` | FICHIERS (L182) |
| `FILTER GAMES BY TEXT` | `ISimpleGameListView.cpp:468`, `ISimpleGameListView.cpp:470` | FILTRER LES JEUX PAR TEXTE (L203) |
| `Favorite` | `DetailedContainer.cpp:140` | Favori (L194) |
| `Full` | `UIModeController.cpp:8` | Complet (L61) |
| `GAME OPTIONS` | `ISimpleGameListView.cpp:725`, `ISimpleGameListView.cpp:727` | OPTIONS DU JEU (L227) |
| `GAME OPTIONS (HOLD)` | `ISimpleGameListView.cpp:717` | OPTIONS DU JEU (MAINTENU) (L221) |
| `GO TO DECADE` | `SystemView.cpp:539` | ALLER À LA DÉCENNIE (L140) |
| `GO TO HARDWARE` | `SystemView.cpp:534` | ALLER AU MATÉRIEL (L137) |
| `GO TO LETTER` | `SystemView.cpp:524` | ALLER À LA LETTRE (L128) |
| `GO TO MANUFACTURER` | `SystemView.cpp:529` | ALLER AU CONSTRUCTEUR (L134) |
| `Game time` | `DetailedContainer.cpp:137` | Temps de jeu (L191) |
| `Games similar to` | `ISimpleGameListView.cpp:659` | Jeux similaires à (L206) |
| `Genre` | `DetailedContainer.cpp:124` | Genre (L25) |
| `INVALID CREDENTIALS` | `HfsDBScraper.cpp:217`, `IGDBScraper.cpp:172` | IDENTIFIANTS INVALIDES (L3236) |
| `Kid` | `UIModeController.cpp:10` | Enfant (L67) |
| `Kiosk` | `UIModeController.cpp:9` | Kiosque (L64) |
| `Last played` | `DetailedContainer.cpp:130` | Dernier jeu (L185) |
| `NAVIGATION BAR` | `SystemView.cpp:911` | VOLET NAVIGATION (L179) |
| `NETPLAY` | `SystemView.cpp:900` | PARTIES EN RÉSEAU (L170) |
| `NO` | `HttpServerThread.cpp:229`, `DetailedContainer.cpp:1043` | NON (L85) |
| `No Entries Found` | `ISimpleGameListView.cpp:929` | Aucune entrée trouvée (L243) |
| `OK` | `SystemView.cpp:243`, `SystemView.cpp:365`, `SystemView.cpp:1619` | OK (L119) |
| `OPTIONS` | `ISimpleGameListView.cpp:720` | OPTIONS (L224) |
| `Players` | `DetailedContainer.cpp:127` | Joueurs (L28) |
| `Publisher` | `DetailedContainer.cpp:121` | Éditeur (L19) |
| `QUICK SEARCH` | `SystemView.cpp:353`, `SystemView.cpp:355` | RECHERCHE RAPIDE (L122) |
| `RANDOM` | `SystemView.cpp:901`, `SystemView.cpp:905`, `ISimpleGameListView.cpp:739` | ALÉATOIRE (L176) |
| `Rating` | `DetailedContainer.cpp:112` | Notation (L34) |
| `Released` | `DetailedContainer.cpp:115` | Date de sortie (L31) |
| `SAVE STATES` | `ISimpleGameListView.cpp:732`, `ISimpleGameListView.cpp:734` | SAUVEGARDES D’ÉTAT (L233) |
| `SAVE STATES (HOLD)` | `ISimpleGameListView.cpp:714` | SAUVEGARDES (MAINTENU) (L218) |
| `SEARCH` | `SystemView.cpp:901`, `SystemView.cpp:907`, `ISimpleGameListView.cpp:739` | RECHERCHER (L173) |
| `SELECT` | `SystemView.cpp:894` | SELECT (L3809) |
| `SYSTEM` | `ISimpleGameListView.cpp:688` | SYSTÈME (L209) |
| `SYSTEM INFO` | `SystemView.cpp:34` | INFO SYSTÈME (L112) |
| `Times played` | `DetailedContainer.cpp:134` | Nombre de parties (L188) |
| `Unknown` | `SystemView.cpp:539`, `DetailedContainer.cpp:1010`, `GameNameFormatter.cpp:113` | Inconnu (L143) |
| `YES` | `HttpServerThread.cpp:229`, `DetailedContainer.cpp:1043` | OUI (L82) |
| `YOU ARE NOT CONNECTED TO A NETWORK` | `SystemView.cpp:365`, `SystemView.cpp:1619` | VOUS N’ÊTES CONNECTÉ À AUCUN RÉSEAU (L125) |

generated, asserted: 57 lines, 69 calls, 50 distinct msgids in 9 files; 0 with an empty French msgstr, 0 with no msgid

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

**Granted** on #679 at 16:07 UTC (comment 6447015977), under T13's conditions; the host free (qemu 0, compilers 0; swap 1,402 of 8,191 MiB, no reclaim needed).
- **START 16:08 UTC** (comment 6447041699; the first line `START 16:08:36 UTC`; census qemu 0, compilers 0) and its line in the shared host file.
- **RETURN** (comment 6447364690; the first line `RETURN 16:22:34 UTC`; census qemu 0, compilers 0) and its line. The guest was stopped by `tools/vm-stop` on its pidfile at 16:22:12 (rc 0), 14 minutes into the 35.

**The image:** `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (sha256 compared by hand with its bare `.sha256`: match), on a fresh 16 GiB qcow2 (`guest-cycle/g01-identity.txt`): `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`, `geometry 640 480`. The installed ES carries M7's composition (`Pending achievements stay`: 1) beside the pin's slice strings, so **every frame is `image` evidence**. Fixtures (`guest-cycle/scripts/seed.sh`, `g09-seed.sh`): ten gb games A to J, 100 screenshots, a `gamelist.xml` naming Alpha's manual and Bravo's picture, both absent.

| G | What ran | What was read back | Verdict (side) |
| --- | --- | --- | --- |
| G-01 | the identity script | the four os-release lines, 640x480, seven literals, the ES digest `25155163fd7970f7` | `image` |
| G-02 | the five styles by `GamelistViewStyle` with ES stopped (`guest-cycle/scripts/style.sh`), the gb list in each; SCREENSHOTS (`imageviewer`) timed | basic, detailed and video drawn; **grid and gamecarousel draw the basic list** (the shipped theme has neither view); one list bar in every style (OPTIONS, MENU, BACK, SEARCH, GAME OPTIONS, SAVE STATES); **L-14 not reached**: SCREENSHOTS draws the detailed style under `grid`, and the press to a still screen read 2.775 s (SCREENSHOTS, grid), 2.786 s (automatic), 2.777 s (gb, 10 games) -- the settle tool's floor (`guest-cycle/g02-l14-timings.txt`) | `image` |
| G-03 | VIEW OPTIONS' JUMP TO GAME BEGINNING WITH THE LETTER moved to D, then BACK | the row reads D; **the list's cursor stays on Alpha** -- read at stage C before it is called anything (T31's `GuiGamelistOptions` applies it through this slice's `moveToLetter`); the l2/r2 keys `CANNOT` (no trigger in the guest's keyboard map) | `image` |
| G-04 | the fast move backward (`q`, left shoulder) then forward (`w`) on the carousel | FAVORITES, then PICO-8 again; ES's pid unchanged, no backtrace in the journal | `image` |
| G-05 | `ip link set eth0 down`; SCRAPER, ArcadeDB, SCRAPE NOW | **COMPLETED, GAMES SCRAPED: 9, UPDATE GAMELISTS TO APPLY CHANGES.**, no COULDN'T SCRAPE, `ELAPSED 0:00`; no `images` folder written, the gamelist unchanged; no scraper line in the journal at the image's log level (`guest-cycle/g05-journal.txt`) -- **3.13's and L-07's positive** | `image` |
| G-06 | SCRAPER, IGDB with no client id, SCRAPE NOW; then `fr_FR` | SYSTEMS INCLUDED empty; **NO GAMES FIT THAT CRITERIA.** / **AUCUN JEU NE CORRESPOND.** (one OK) -- not INVALID CREDENTIALS: 3.16's remainder as the player meets it, `isSupportedPlatform` read at C | `image` |
| G-07 | -- | `CANNOT`: host port 80 is privileged (`ip_unprivileged_port_start` 1024) | -- |
| G-08 | `guest-cycle/scripts/g08-api.sh` from inside the guest | `"Version": "0.0.1-dev"`; `[ true ]`; `/notify`'s long body one line cut with an ellipsis (`frames/g08-notify-toast.png`; L-12 holds the one-line rule, its thread shows nothing); `/removegames/gb` outside the system `204 No game removed`, the 10 games kept (`guest-cycle/g08-api.txt`); the `403` `CANNOT` (no forward of 1234) | `image` |
| G-09 | Bravo's picture written from outside ES with its detailed list open, the list re-entered; then ES restarted | **no picture after the write in the same session; the picture after the restart** -- L-08's positive with its control (the theme has no MANUAL element, so the picture's read `:817-831` stands in for `:903`) | `image` |
| G-10 | -- | `CANNOT`: the https hosts refuse a stub | -- |
| G-11 | `tools/vm-stop` on the pidfile | `retired.txt`: `t32.qcow2`, 2,312,372,224 bytes, sha256 `a3a152ce5b6df4d848caa8446654a622c746db0f1ea2ee7cdc8b13694bd0627d`, removed; qemu 0, compilers 0 | -- |

- **French** (`frames/g02-fr-gb-list.png`, `g06-fr-1-box.png`): the list's bar reads OPTIONS, MENU, RETOUR, RECHERCHER, OPTIONS DU JEU -- five, where English showed six with SAVE STATES. Read at stage C (#210's bar) before it is called anything.
- **Not driven:** L-11's dialog (hiding every system), L-10's `SAVE STATES (HOLD)` (no game with states).
- **Void passes, mine, each redone with a frame:** a SCREENSHOTS timing under `StartupSystem=screenshots` (the system is `imageviewer`); a `ret` that went to the list after the outcome page; a French switch run without `/etc/profile` (`set_setting` absent).

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
