# Analysis — M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

Written by the first reader (Opus 5.5) at stage C, before the seat. Line numbers are the pin's (`16dbac5211`). The leads are `02` § The leads.

## Executive summary

The slice is 42 files and 17,311 lines. Six files carry the fork's changes and 36 are upstream's, byte for byte. It has three parts: the views, the scrapers and the local HTTP API. Each fails in the same way: **a failure that the next layer reads as success, or as nothing at all.**
- **The scrapers.**
  - A request that never reached its server ends as "done" (3.13). So an offline scrape says COMPLETED, GAMES SCRAPED: 9 (G-05, the image).
  - A response of the wrong shape is read before it is checked. In the shipped build, which has NDEBUG, that is a wild read: TheGamesDB's `"boxart": "x"` and IGDB's or HfsDB's numeric token are SEGVs (3.10, L-22).
- **The batch scrape's thread** frees itself while the player's CANCEL can still write through it. A CANCEL in the frame the run finishes is a use-after-free, and it marks the finished run cancelled (L-02).
- **The token fetches and media downloads** have no bound but the 10 s connect (L-06, L-18). The token fetch at a scrape's start runs on the interface thread.
- **The HTTP API** runs handlers that touch `FileData` on httplib's pool (L-12, L-13, L-19, L-21). Its 2020 httplib accepts an unbounded request body (L-24).
- **A saved scraper name the build does not register** crashes SCRAPE NOW (3.15). The page's count is short by the thread count (3.19).
- **The views are mostly sound.** Their defects are small and upstream's: a missing year (3.32), a wrapped play time (3.32), an empty tile in a grid theme (3.31), and a fast move whose wrong index a wrapping carousel hides (3.27).

All seven host harnesses FAIL at the pin and pass their controls. The window proved 3.13 and L-08 on the image. Proposed: **N bugs** (counted in `05`) and the rest Deferred or recorded, each named in `05`.

## Acceptance-criteria scorecard

#679's body, at stage C (before the seat):

| # | Checkbox (short) | State at stage C |
| --- | --- | --- |
| 1 | the folder's files | `00`-`04`, `stage-a`, `stage-b`, `stage-c`, `tools`, `guest-cycle` present; `05`, `second-opinions`, `stage-d`, `stage-e` to come |
| 2 | `lint-audit-artifacts` PASS | pre-issue lint at the end of stage C; resolution at close |
| 3 | `review-plan.json`, one reviewer, provenance | stage C, after this file |
| 4 | the punch list at Phase 7 outcomes | stage E onward |
| 5 | the header's four hashes | `reviewed-at` `603b358a14` and `reviewed-at-es` the pin in `00`; the fixed pair at stage E |
| 6 | 01 § Scope | done (stage A) |
| 7 | 02's coverage table, one row per path | done: 42 rows (`t32-02.py` asserts) |
| 8 | 02 § The runs, both rules | done, with the corrections |
| 9 | the five generated sections | done; each seen to exit 1 on a drift (`stage-b/generators.txt`) |
| 10 | § The reads, one row per line | done: 49 |
| 11 | § The merge debt | done |
| 12 | every § 5 command recorded | done (stage A/B); stage C's runs added |
| 13 | § The guest cycle | done, with G-06 corrected |
| 14 | `00` shows no build, fetch, handheld or owner account | holds so far; the council runtime is `npm install --offline` at the seat call |
| 15 | 04 Q1-Q7 answered; each `bug` traced | this file; the bugs at stage D |
| 16 | `proved:` cells, `question:` on punch items | 02 done; 05 at stage D |
| 17 | the retro | stage G |
| 18 | `es-menu-map-check` 0 missing after the views section | stage E (L-15) |
| 19 | the five checks and the hooks tests | before the hand-back |
| 20 | the unit build's TOTAL line, after the fixes | the pin's is recorded (`TOTAL: 221 test cases in 4 binaries`); after the fixes at stage E |

## Risk assessment

- **High, data or process safety:**
  - L-02, a use-after-free on the fork's own CANCEL path;
  - 3.10 and L-22, SEGVs on a malformed response. Each needs a server, a proxy or a captive portal to send the shape.
  - 3.15, a null dereference on SCRAPE NOW after an upgrade or a build change (tree; VM-provable).
- **Medium, a lie the player reads:**
  - 3.13, COMPLETED for a scrape that reached nothing;
  - L-02's SKIPPED over a completed run;
  - 3.19's count, short by the thread count;
  - L-05, curl's words on line 4;
  - L-08, a manual that appears only after a restart.
- **Medium, a freeze or a bound:**
  - L-18, the token fetch on the interface thread, bounded by the connect timeout;
  - L-06, a media download with no bound under a page whose only exit is CANCEL.
- **Low:**
  - L-24 (WEB ACCESS off by default);
  - 3.31 (no shipped theme has a grid view);
  - 3.32 (the year and the play time beside a name);
  - 3.27 (hidden by the wrap);
  - L-23 (a leak per run);
  - L-10 and L-11 (words).
- **Carried, not proved here:** L-16, #246's shape in `CollectionSystemManager` (T33's); L-19 (#774's sibling).

## Coverage boundary

**Read line by line:** the 42 paths at the pin, except `httplib.h`.
- `httplib.h` was read by fingerprint and at the request path's lines: `:72`, `:615-633`, `:2475`, `:2540-2575`, `:2735`, `:2796`, `:3782`. 02 § The structure gives the reason: a vendored library is checked for currency, not read whole.

**Read outside the 42, as context:**
- `ScraperSearchComponent.cpp:195-330` and `:636-670` (L-18);
- `CollectionSystemManager.cpp:1103-1140` and `:1541-1600` (L-16);
- `ViewController.cpp:1119-1150`;
- `FileData.cpp:2321-2327`;
- `TimeUtil.cpp:514-583` (3.32);
- `HttpReq.h`, `HttpReq.cpp:630-646`, `AsyncHandle.h`;
- `GuiMenu.cpp:1088-1097` and `Settings.cpp:190` (WEB ACCESS);
- the distribution's `config/functions:384-388` (NDEBUG) and `backuptool:1209-1218` (#274's strip).

**Not run:**
- any scraper's success path (G-07, G-10: `CANNOT`);
- L-14's per-tile cost (no grid view in the shipped theme);
- L-16's and L-19's reloads on a guest;
- a TSan run of L-01's unlocked reads.

## The questions

### Q1 Lifetimes and threads

- **L-01 and L-02.** `ThreadedScraper::stop()` (`:323-337`) reads `mInstance` and writes `thread->mExitCode` under no lock, while `run()` frees itself at `:238`. `l02` shows both halves at the pin:
  - a heap-use-after-free at `:333`;
  - `cancelled` over `finished` under `--plain`.

  The window was widened by a hook in the finishing block's `LOG`, and the harness says so. The fix shape (the control): `stop()` takes `sProgressMutex`, returns when `finished`, and `run()` clears `mInstance` under the same lock before `delete this`. `isRunning()` reads the same static and is with it. History: `stop()`'s CANCEL comment is the fork's (D-UI-078); the unlocked read is upstream's.
- **L-23.** `run()` erases each `ScraperThread` without a `delete` (`:218`, 717e7d8c3), and `mHandle` is never joined or freed (`:53`): a leak per run, upstream's.
- **L-12, L-13, L-19, L-21: the pool thread.**
  - `/notify` builds a toast off the interface thread (`HttpServerThread.cpp:574`).
  - `/removegames` and the media writes touch `FileData` there (`:738`, `:751-755`; `HttpApi.cpp:258-260`).
  - `/launch` walks every system's files there and posts one raw `FileData*` per match with no `break` (`:615-630`; #774's sibling, T2 PL-008).
  - `/quit`, `/shutdown` and `/restart` call `quitES` there (`:241`, `:249`, `:257`).

  Each is upstream's and contained. G-08 drove `/notify` and `/removegames` on the image without a crash, which proves no race either way.
- **L-16.** `ISimpleGameListView.cpp:461-464` is an either/or. The free-then-read is inside `CollectionSystemManager::reloadCollection` (`:1574-1589`): the root is cleared at `:1117`, then the bundle view's cursor is read (`ViewController.cpp:1140-1142`). #246's shape, carried to T33 with its lines.
- **The rescan callers that delete nothing** (`BasicGameListView.cpp:54`, `:182`, `CarouselGameListView.cpp:61`, `:171`) call `reloadGameListView(this)` with nothing freed first. Recorded sound.

### Q2 Bounded calls

- **L-06.** Nine `HttpReq` constructions; none sets `timeout` or `stallTimeout` (`t32-bounds.py`: `bounded=0`). Each ends at `HttpReq.cpp:204`'s 10 s connect and nothing else, so a link that goes after the connect is silent for `tcp_retries2` (#299's quarter of an hour). The scrape page's only exit is CANCEL, and CANCEL ends the loop, not the request in flight. The fix is #299's: a `stallTimeout` on the scrapers' options (`Scraper.cpp`'s `mOptions`, the media handle's, the two token requests').
- **L-18.**
  - The token requests are stack `HttpReq`s ended by `wait()`, a 20 ms sleep loop (`HttpReq.cpp:638-644`).
  - The batch run's first games are searched on the **interface thread** (`ThreadedScraper::start` -> `Process()` -> `ProcessNextGame` -> `ScraperThread::run` -> `search`, `:100`).
  - The manual scrape is on the interface thread where the player typed a name (`ScraperSearchComponent.cpp:303`), where no scraper takes the system (`:321`), and in `update()`'s retry (`:652`, `:658`).
  - The default manual path uses its own thread and catches the throw (`:206`, `:211-217`).
  - **Unproved:** on the scrape thread, `generateRequests`' `throw` (`IGDBScraper.cpp:172`, `HfsDBScraper.cpp:217`) has no catch. It needs a token older than 30 minutes, which needs a 30-minute gap between searches, and L-06 can make one.
- **L-24.** httplib's body limit is `SIZE_MAX` (`:72`), and chunked reads take no limit (`:2475`, `:2558-2559`). The fix is a contained `set_payload_max_length` where the server is built. The vendored copy's age is a #585 line (02 § The structure).
- **The cost the lens prices:** a token fetch on the interface thread is a freeze bounded only by the connect, at the moment the player presses SCRAPE NOW.

### Q3 Reads that read as success

- **3.13** (`l313`). `Scraper.cpp:372-376` makes `REQ_IO_ERROR` an "ignored error". `:350-352` makes a spent 429 DONE, and `:357-361` does the same for a Retry-After over 5 s where `retryOn249()` is false (IGDB and HfsDB in a manual scrape). The reader (`ThreadedScraper.cpp:155-173`) stops a run only on its fatal list, so `setError(status, ...)` for these keeps a631e8c84's intent (a batch survives one game) and gives the page a count. G-05 is the image's positive.
- **`:337` drops `process()`'s return.** The three scrapers' contract comment is therefore dead (3.5, 3.16). IGDB returns false for "no match" and on a parse error (`IGDBScraper.cpp:318-329`). A fix to 3.13 that honours the return would retry an empty answer as rate-limited, so 3.16's change lands with 3.13's or before it.
- **3.10, L-22.** The shape is read before it is checked, at `GamesDBJSONScraper.cpp:590`, `:598`, `:605-607`, `IGDBScraper.cpp:155-157` and `HfsDBScraper.cpp:202-204`. NDEBUG makes each a wild read. `l310` and `l316` show two SEGVs (rc -11 without the sanitizers). The fix is `IsObject` or `IsString` first (the controls). **The floor's parse items** (`stage-c/floor.md`): 3.2 and 3.4 hold; 3.7 drops a whole game on one bad boxart entry; 3.8 extends 3.10 to the images JSON (`:462-491`) and `GamesDBJSONScraperResources.cpp:180`.
- **ScreenScraper's rate limit** (`ScreenScraper.cpp:383-384`, outside the 42): "maximum threads per minute reached" returns `false`, which `:337` drops, so the game reads as no match. **So 3.13's fix should honour the return with a bounded retry, and 3.16 must be corrected with it.**
- **3.19.** `done` is set only as a game is handed out (`ThreadedScraper.cpp:250-256`, `:66`), so a finished run counts total minus threads: G-05's ten games read 9. A no-match is counted as scraped, against `ThreadedScraper.h:67`.
- **3.15.** `getScraper()` is dereferenced unchecked at `ThreadedScraper.cpp:296` and `:100`, and at `ScraperSearchComponent.cpp:321`. `GuiScraperStart.cpp:74-78` shows a fallback but saves only on change (`:215`).
- **L-07.** A media download's 404, IO error and spent 429 read as done (`Scraper.cpp:607-614`, `:631-635`): the caller half of #1191. #1205 (T21 PL-17) owns the HTTP-date `Retry-After` read as 0 ms.
- **L-02's cancel** is also this family: a CANCEL that did nothing reads as one that did.

### Q4 Uncached reads

- All 49 `exists`-family lines in the 42 are cached (`t32-reads.py`: `uncached=0`).
- ES's own writers drop their entry: `FileSystemUtil.cpp` `:1051`, `:1067`, `:1097`, `:1445`, `:1457-1458`, `:1506-1507`. So a stale answer needs a writer outside the process: the cloud content restore, a player over SSH, a scraper run by another tool.
- **L-08:** `DetailedContainer.cpp:903`, `:916` decide the MANUAL and MAP rows from such a read. G-09 is its positive with a control: the manual written from outside was absent in the session and present after a restart.
- **L-09:** the scrape decides what to fetch and what to overwrite from the same cache. A stream question: pass `false` for the reads whose writer is outside ES, as #179's rclone.conf gate did.

### Q5 The words, the French and the help bars

- **The strings** (`t32-words.py`): 57 code lines, 69 calls, 50 msgids, 0 with an empty French, 0 missing. The brief's 58 / 70 / 51 counted `ISimpleGameListView.cpp:905`'s comment.
- **L-10.** #210's `SAVE STATES (HOLD)` is `SAUVEGARDES (MAINTENU)` (po L218), the game-save word, where L233's `SAVE STATES` is `SAUVEGARDES D’ÉTAT`. One catalog line closes it.
- **L-11.** `SystemView.cpp:233-234`: an English sentence-case dialog outside `_()`, with a bare `"OK"`, after a `UIMode` write with no `saveFile()`. L116's empty `msgstr` is the multi-line form (its French at L117), so that half is withdrawn.
- **L-05.** Line 4 carries `removeHtmlTags(getErrorMsg())` (`Scraper.cpp:640`, `:638`'s `if`). G-05 reached no error, so line 4 stayed empty on the image, which is 3.13 seen from the page.
- **L-12.** G-08's long `/notify` body was clipped to one line at 640x480, against the one-line toast rule, which holds. The words are the caller's, unbounded, from the pool thread.
- **The help bars.** `getHelpPrompts()` is defined twice in the slice, and the five styles inherit `ISimpleGameListView`'s. **3.34** (#210's rule, `stage-c/floor.md`): SAVE STATES (HOLD) needs GameOptionsAtNorth and a `retroarch` game with a save-state config outside IMAGEVIEWER. The bar refreshes on a cursor change only in collections (`BasicGameListView.cpp:31`, `DetailedGameListView.cpp:39`). The French frame's five entries against six are consistent with a stale bar, not proved by it: an open question for a frame.
- **3.35** holds (`t32-words.py`; `stage-c/floor.md`). Only `": "` and `"- "` are concatenated outside `_()`, so French loses its ` : `.

### Q6 The views and their cost

| View | What draws it | What it reads per item on the interface thread | What the first frame waits for (guest) |
| --- | --- | --- | --- |
| Carousel (`SystemView`) | the systems' logos, `populate` (`:196`) | each system's game count and theme | framed after UPDATE GAMELISTS (G-09), not timed |
| Basic | a text list | the name (`GameNameFormatter`) | (G-02 frames) |
| Detailed | the list plus `DetailedContainer` | the image and extras' paths; MANUAL/MAP `exists` (L-08); the play time (3.32) | (G-02) |
| Video | Detailed plus a video | the video path | (G-02) |
| Grid | tiles | `DisplayAspect::forScreenshot` per tile (L-14, `GridGameListView.cpp:42-47`) | not reached: the shipped theme has no grid; 2.775 s press to still in grid style (drawn as automatic) |
| Carousel list | a game carousel | the image per item | (G-02) |

- **3.27** (`l327`): 25 of 312 cases out of range, all congruent modulo the size, so `moveSelectionBy`'s delta (`:407`, `:413`) on a wrapping carousel hides them. G-04 wrapped cleanly. The other 37 cases that are not congruent are the forward fast move on 3 to 9 systems: a no-op, by the `count >= sz` guard. Recorded, with a one-line contained fix.
- **3.31** (`l331`): IMAGE with no image draws an empty tile. The intent read is ambiguous (8f30c244c, 4371e3b7d), so it is a stream question.
- **3.32** (`l332`): no year under RELEASEDATE_DESCENDING, and `[01:00:00]` for 25 hours. The detailed row does not wrap.
- **3.29** (`floor.md`): a UTF-8 lead byte is taken as the letter, and the `break` at `:514` assumes name order. Neither explains G-03's cursor on Alpha under a name sort, so **G-03 is left open** for a frame in a stream.
- **3.30** is design (9be91629e). `BasicGameListView.cpp:101`'s `recurseFind` is a dead copy.
- **The #243 extras:** `DetailedContainer.cpp:1057-1072` and `ISimpleGameListView.cpp:755-765` reach both `mImage` and the theme's extras (`es-code-traps.md` § The picture beside a game list). Read, sound.
- **The cost.** The press to a still screen is 2.78 s in each style the theme draws (G-02), and no per-item read dominates it on the guest. L-14 remains a grid-theme question.

### Q7 The structure, the map and the merge debt

- **L-15.** `docs/es-menu-map.md` has no section for the five view styles, the rows that pick them (GAMELIST VIEW STYLE, T26's; VIEW OPTIONS, T31's) or the SCREENSHOTS list. The views carry no screen title, so `es-menu-map-check` cannot see them. `SystemView.cpp:552`'s computed title is #965's. The map section lands at stage E (checkbox 18).
- **The modes.** `UIModeController` has four modes. A wrong press resets the unlock counter (3.33, settled at `:72`), and `UIMode = Full` saves at `:102-103`. `SystemView.cpp:233`'s write does not save (L-11).
- **The registry** (`Scraper.cpp:24-39`): ScreenScraper under the runtime login, ArcadeDB and IGDB always, TheGamesDB and HfsDB with their macros. Names only. `IGDBSecret` is stripped from a settings backup by name (`backuptool:1218`; #274, D-QA-050). `IGDBClientID` is kept, an identifier not a secret.
- **`httplib.h`.** The 2020 v0.7 series (02 § The structure; L-24). A #585 line: the vendored copy is behind upstream's chunked-body limit (0.20.1). CVE-2026-45372's mechanism is absent.
- **The merge debt.** 0 of the 14 upstream commits since `cada856d86` touch the 42. The fork's six files carry 168/46. T21's ES tip carries `Scraper.cpp` 28/8 and `Scraper.h` 5/0, and adds `ScraperReplies.{cpp,h}`, inherited. The #585 candidates: #210's bar, the `Progress` contract, the aspect and the turn, `maskSecrets`, the `CheevosHash` argument. D-WORKFLOW-080's shape is recorded, not decided.

## Renovation face

### Q1 Modernize
The scrapers' parses want a shape-first helper, one function per response. The thread wants one owner of its lifetime. The services want every handler that touches `FileData` posted to the interface thread, as `/reloadgames` already does.

### Q2 Standards
rapidjson's preconditions are the standard here, and four sites break them (3.10, L-22, and the floor's). #299's stall bound is the standard for a request, and nine constructions lack it.

### Q3 Bugs
3.13, L-02, 3.10, L-22, L-06 with L-18, 3.32, 3.31, L-24. The proposed set and its owners are in `05`.

### Q4 Package currency
The vendored httplib (2020) is behind upstream (a #585 line). rapidjson is the recipe's 1.1.0, as everywhere in the tree.

### Q5 Efficiency
The token fetch on the interface thread. Nothing else measured on the guest dominates the 2.78 s.

### Q6 Dead ends
`process()`'s return (`:337`). The `count >= sz` guard's forward no-op (3.27). IMAGE's unreachable fallback (3.31).

### Q7 Clarity and structure
The contract comment repeated in three scrapers and read by no caller. `HttpServerThread.cpp`'s 27 registrations in one 650-line function (`:149-803`).

## Instruction File Recommendations

### Coverage gaps (would have prevented)
- `es-code-traps.md` has no line on rapidjson under NDEBUG: an unchecked `HasMember` or `GetString` is a wild read in the shipped build, not an assertion. 3.10 and L-22 are two instances.

### Codification gaps (proposals for the coordinator)
- **A shape-first parse rule.** "`IsObject`, `IsArray` or `IsString` before any member access on a body a network sent." A `grep` could audit it: `HasMember` or `GetString` with no `Is*` on the same value within N lines.

## Second opinion

(After the seat: the packet, the plan, the probe and the refutation, and the grades.)
