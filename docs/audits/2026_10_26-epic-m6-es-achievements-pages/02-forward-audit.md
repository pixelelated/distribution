# Forward audit — M6.P2 T20, EmulationStation's RetroAchievements and offline pages (#667)

- **reviewed-at:** `ae3c013cac` (the distribution); **reviewed-at-es:** `16dbac5211eea7e70db7394372033be2be7df829` (the pin), the 25 read at the pin's bytes (R18 empty).
- **The ctl side:** `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl` at `8ebaf8daad` (2,455 lines, the same bytes at `ae3c013cac`), with T19's stage-E changes read from T19's `02` § What T20 inherits at `d8c02be1c9`.
- **Leads** are numbered L-01 to L-27. Each is read at its lines; it is a defect only where a `proved:` cell says so, and is put to the questions in `04`.
- **`proved:` values:** `tree` (read at the pin), `history`, `tool-run`, `fixture` (a host program built from the pin's own lines, under `stage-b/positives/`), `guest` (read in the window of 17:36 to 17:57 UTC, `guest-cycle/`), `design` (a stated trade, not a defect).

## Coverage

| Path | Lines | Read | Where in this file | Leads |
| --- | ---: | --- | --- | --- |
| `es-app/src/OfflineAchievements.cpp` | 353 | whole | § The contract, § The credentials' paths | L-05, L-06, L-11, L-12, L-13 |
| `es-app/src/OfflineAchievements.h` | 148 | whole | § The contract | — |
| `es-app/src/OfflineScanJob.cpp` | 273 | whole | § The reader | L-07, L-10 |
| `es-app/src/OfflineScanJob.h` | 100 | whole | § The reader | L-07 |
| `es-app/src/RetroAchievements.cpp` | 1072 | whole | § The credentials' paths, § The hasher | L-01 to L-04, L-20 |
| `es-app/src/RetroAchievements.h` | 286 | whole | § The credentials' paths | — |
| `es-app/src/ThreadedHasher.cpp` | 415 | whole | § The hasher | L-19 to L-23 |
| `es-app/src/ThreadedHasher.h` | 76 | whole | § The hasher | L-22 |
| `es-app/src/guis/GuiGameAchievements.cpp` | 352 | whole | § The pages | L-03 |
| `es-app/src/guis/GuiGameAchievements.h` | 35 | whole | § The pages | — |
| `es-app/src/guis/GuiOfflineScan.cpp` | 382 | whole | § The pages, § The reader | L-07, L-13 |
| `es-app/src/guis/GuiOfflineScan.h` | 93 | whole | § The pages | — |
| `es-app/src/guis/GuiRetroAchievements.cpp` | 471 | whole | § The pages | L-03 |
| `es-app/src/guis/GuiRetroAchievements.h` | 54 | whole | § The pages | — |
| `es-app/src/guis/GuiRetroAchievementsSettings.cpp` | 808 | whole | § The pages, § The credentials' paths, § The contract | L-02, L-03, L-09, L-14 to L-18 |
| `es-app/src/guis/GuiRetroAchievementsSettings.h` | 11 | whole (upstream-carried, no commit since the base) | § The pages | — |
| `external/libcheevos/CMakeLists.txt` | 245 | diff +17/-0 | § The library | L-24 |
| `external/libcheevos/LICENSE.rvz-padding` | 29 | notice, present and shipped (not read as code) | § The library | — |
| `external/libcheevos/RVZ-NOTICES.md` | 29 | notice, present and shipped (not read as code) | § The library | — |
| `external/libcheevos/cheevos.cpp` | 193 | diff +16/-0 | § The library | — |
| `external/libcheevos/cheevos.h` | 8 | diff +3/-0 | § The library | — |
| `external/libcheevos/libretro-common/src/utils/md5.c` | 304 | diff +10/-1 | § The library | L-24 |
| `external/libcheevos/rcheevos/src/rhash/hash_disc.c` | 1352 | diff +26/-14 | § The library | L-24 |
| `external/libcheevos/rvz_hash.cpp` | 389 | whole (new) | § The library | L-25 |
| `external/libcheevos/rvz_hash.h` | 7 | whole (new) | § The library | — |

## The credentials' paths

One row per credential kind per sink it can reach. "Mask" is what stands between the value and that sink.

| Credential | Sink | Line | Mask | proved: | Lead |
| --- | --- | --- | --- | --- | --- |
| username | setting store at rest (`system.cfg`, `global.retroachievements.username`) | `GuiRetroAchievementsSettings.cpp:610` | none (clear text; an account name, not a secret) | tree | — |
| username | query strings: login `u=` (`RetroAchievements.cpp:1037`); web API `z=` (`:149`) and `u=` (`:521`, `:634`, `:757`); the proxy's `u=` over loopback (`:301`, `:315`, `:338`) | as listed | `urlEncode` only | tree | L-04 |
| username | header: `User-Agent` `<user>/<version>` on every web API request | `RetroAchievements.cpp:181-183` | none | tree | L-04 |
| username | the screen: the page title `RETROACHIEVEMENTS - <user>` | `GuiRetroAchievements.cpp:334` | none (the player's own name, on purpose) | tree | — |
| username | a log | none found (R5: no `LOG(` carries it) | — | tool-run | — |
| password | setting store at rest (`system.cfg`, `global.retroachievements.password`) | `GuiRetroAchievementsSettings.cpp:611` (masked entry) | the row shows `*********`; the file is clear text, kept out of backups (`backuptool` strips it; read in T18 and not re-read here) | tree | — |
| password | query string of the login request, `dorequest.php?r=login&u=…&p=…` | `RetroAchievements.cpp:1037` | `urlEncode` only; over TLS with the peer unverified (#1154, cited, not re-found: `HttpReq.cpp:192`) and redirects followed to `http` or `https` (`HttpReq.cpp` `FOLLOWLOCATION 1`, `MAXREDIRS 2`, `REDIR_PROTOCOLS_STR "http,https"`) | tree | L-01 |
| password | the interface thread: the sign-in at page close | `GuiRetroAchievementsSettings.cpp:743-807`, `:776` | — (no value exposed; the freeze is the cost) | tree | L-02 |
| password | a shell command | none: the scan and toggle commands carry no credential (`:322`, `:479`); the ctl reads `system.cfg` itself | — | tree | — |
| password | a log | none: `HttpReq` logs no URL (`onError` logs the status and message, `HttpReq.cpp:559-563`) | — | tree | — |
| token | setting store at rest (`global.retroachievements.token`) | `GuiRetroAchievementsSettings.cpp:777`, cleared `:767`, `:780`, `:796` | none (clear text in `system.cfg`) | tree | — |
| token | the screen | none: `tokenOrError` is shown only on failure (`:784`), when it holds the error, never the token | — | tree | — |
| token | a log | two `LOG(` lines say the word *token* in prose (`:761`, `:792`), no value (R4) | — | tool-run | — |
| web API key | setting store at rest (`global.retroachievements.key`) | `GuiRetroAchievementsSettings.cpp:616` (masked entry, built only without `CHEEVOS_DEV_LOGIN`) | the row is masked; the file is clear text | tree | — |
| web API key | query string `y=` on every web API request | `RetroAchievements.cpp:149`, used at `:194` | `urlEncode` only; the same unverified peer (#1154) | tree | L-04 |
| web API key | a log | none | — | tool-run | — |
| all four | the packet | the stage-C scan's three-way pass is the guard; this file carries key names only, never a value | — | — | — |

- **What reaches the screen in a tool's words (L-03, Q1):**
  - curl's message as `tokenOrError` (`RetroAchievements.cpp:1040`, shown at `GuiRetroAchievementsSettings.cpp:784`);
  - the server's JSON `Error` (`:1063-1064`);
  - two English literals outside `_( )`: `Unable to parse response` (`:1048`) and `Unknown error` (`:1068`);
  - the user summary's `Status`, behind `AN ERROR OCCURRED` (`GuiRetroAchievements.cpp:44`, from `RetroAchievements.cpp:782`).
- **`maskSecrets`** is in 11 files at the pin (R5) and none of them is `RetroAchievements.cpp`. No line there needs it, because no URL is logged.

## The pages

| Page or dialog | Title | Rows (builder) | Gates | Store | Save | Strings (`_("` in file) | Buttons, safe last |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RETROACHIEVEMENTS SETTINGS | `RETROACHIEVEMENTS SETTINGS` (`GuiRetroAchievementsSettings.cpp:596`) | RETROACHIEVEMENTS (`addWithLabel` switch); USERNAME, PASSWORD, WEB API KEY (`addInputTextConfigRow`); HARDCORE MODE (`addSwitch`, `false`); OFFLINE ACHIEVEMENTS (BETA) (`addWithDescription`, arrow); LEADERBOARDS, VERBOSE, RICH PRESENCE, ENCORE, AUTOMATIC SCREENSHOT, CHALLENGE INDICATORS, UNOFFICIAL (`addSwitch`, `false`); PROGRESS TRACKER (by hand, default on); UNLOCK SOUND (option list); LED NOTIFICATIONS (env-gated); SHOW … IN MAIN MENU (`addSwitch`, `true`); INDEX NEW GAMES AT STARTUP (`addSwitch`, `true`); INDEX GAMES (entry) | the offline row on `exists(ctl)` (cached, right: an image file) `:633`; `#ifndef CHEEVOS_DEV_LOGIN` `:612` | `system.cfg` except the two `true` switches (`es_settings.cfg`) | `addSaveFunc` throughout; the sign-in in the save `:743-807`; PROGRESS TRACKER's own save `:658`; LEDs immediate `:688-691` | 93 (with the offline page) | — |
| OFFLINE ACHIEVEMENTS (BETA) | `OFFLINE ACHIEVEMENTS (BETA)` (`:411`) | the switch (`addWithLabel`, by hand); SCAN GAMES FOR OFFLINE ACHIEVEMENTS (`MultiLineMenuEntry` row, dimmed by gates); two info rows, two spacers; the hidden 1 s refresher (`:282-305`) | switch on, signed in (`:160-165`), an address (`:149-152`); a ctl run in flight overrides | `system.cfg` through the ctl (`enable`/`disable`, `:479`) | immediate, from a thread, mirrored into `SystemConf` (`:500-501`) and `CheevosCheckIndexesAtStart` saved at once (`:515-518`) | (counted above) | TURN ON / NOT NOW (`:587-589`) |
| the scan's confirmation | — | — | the three gates first, each an OK box (`:328-342`) | — | — | — | YES / NO (`:359-361`) |
| the offer after enable | — | — | signed in / online (`:530-551`) | — | — | — | SCAN NOW / LATER (`:542-544`) |
| SCANNING GAMES FOR OFFLINE ACHIEVEMENTS | `:32` of `GuiOfflineScan.cpp` | a full-screen page, eight lines, the spinner | fourth tier: back asks CANCEL (`:117-118`), others refused; finished: TRY AGAIN on OK when not completed (`:122-133`) | the ctl's stamp | — | 39 | CANCEL THE SCAN? YES / NO (`:147-151`) |
| RETROACHIEVEMENTS (account) | `RETROACHIEVEMENTS - <user>` (`GuiRetroAchievements.cpp:334`) | header text, recent games (rows to the game page) | `GuiLoading` with `PLEASE WAIT` | none (reads) | — | 19 | OK on the error box |
| the game's achievements | the game's title | the header, one row per achievement | `GuiLoading`; offline and not cached says so (`GuiGameAchievements.cpp:40`) | none (reads) | — | 27 | LAUNCH, BACK |
| GAME HASHING IS RUNNING… | — | — | `ThreadedHasher::checkCloseIfRunning` | — | — | (in the hasher's 9) | YES / NO (`ThreadedHasher.cpp:272`) |

- **The two `es_settings.cfg` switches (L-15):** what reads them is EmulationStation alone, so `storeInSettings = true` is right for both.
  - `RetroachievementsMenuitem` is read at `GuiMenu.cpp:190`, `:5760` and `SystemView.cpp:1616`.
  - `CheevosCheckIndexesAtStart` is read at `SystemData.cpp:1127`, `NetworkThread.cpp:248` and `GuiMenu.cpp:8533`.
  - **proved:** tree (`git grep` at the pin).
- **HARDCORE MODE (L-14), two writers:** the page's switch (`:621`) and the ctl's `enable` and `disable`. The page mirrors the ctl's answer afterwards (`:498-501`). Nothing holds HARDCORE MODE off while the proxy is on: the player can turn it back on at the page, and the proxy refuses hardcore awards (D-RA-001). **proved:** tree. The question for `04` is whether that is a defect or the player's choice.
- **Kickoff note 2, `Settings.cpp:420`:** read at its lines. The block `:417-433` is `#if WIN32`, and `SystemConf` forwards to `Settings` only when `mSystemConfFile` is empty (`SystemConf.cpp:288`). `Paths.cpp:94` sets `/storage/.config/system/configs/system.cfg`, so on ROCKNIX no second `.hardcore` store is live. `SystemConf`'s own default is `:46`. Whether `:94` is the branch every ROCKNIX build takes is T21's Q4 (`Paths`). **proved:** tree.
- **Dialogs (L-16):** each puts the safe choice last. Three are YES/NO, where the back-button accelerator binds `NO`. TURN ON / NOT NOW and SCAN NOW / LATER name no `NO`, so back falls through to the last button, which is the safe one. **proved:** tree.
- **The 1 s refresher** against the `layoutRows` trap: the row's words change only when they differ (`:265-267`), and the height holds by construction (`:366-370`). The trap is closed at the pin (ES `7c7ffab43`, `es-native-ui.md`). **proved:** tree.
- **The menu map (L-17):** `docs/es-menu-map.md:595` still names the PL-07 drift, and the scan page's title `SCANNING GAMES FOR OFFLINE ACHIEVEMENTS` is absent from the map (R11: 0). `es-menu-map-check` passes because it reads titles, not copy. **proved:** tool-run. The correction goes to a punch item under D-UI-039, since this slice changes no row.
- **The runtime msgid (L-18):** `_(Utils::String::toUpper(snd).c_str())` (`:671`) cannot be extracted by xgettext; it is a sound's file name. **proved:** tree.

## The contract

Both ends of every ctl verb EmulationStation runs. The ctl is read at `8ebaf8daad`; the reader is `ask()` (`OfflineAchievements.cpp:51-57`, the last stdout line and the exit) over `ApiSystem::executeScriptLegacy` (`ApiSystem.cpp:2262-2293`), unless the row says otherwise.

| Verb | The ctl prints, exits (`8ebaf8daad`) | EmulationStation keeps, at | Mismatch | Lead |
| --- | --- | --- | --- | --- |
| `enable` | `hardcore=0` last; 0; `fail` 1 on stderr | last line starts `hardcore=` and exit 0 (`GuiRetroAchievementsSettings.cpp:479-482`) | the reader's own (L-05, L-06) | — |
| `disable` | `hardcore=<0\|1>` last; 0; `fail` 1. **T19's S4/S5:** 2 (`cannot_tell`), 1 (did not stop within 10 s; the toggle put back), and 1 with everything done but the service | any non-0 → `COULDN'T BE TURNED OFF`, the switch reverts to on, `SystemConf` not mirrored (`:490-496`) | S5's exit 1 leaves `system.cfg` at off while the page shows on and in-memory `SystemConf` still reads on: `toggleOn()` then answers yes for a proxy that is off | L-09 |
| `scan` | `>>> ` lines (T19's table) and the stamp; 0, 1, 69, 75, 77, 78, 130, 143 | `OfflineScanJob` (§ The reader); outcome per exit at `GuiOfflineScan.cpp:185-201` | 77 and 78 are refused before the page by the page's own gates; 130 after CANCEL reads SKIPPED; 143 (from `disable`) reads COULDN'T FINISH, why `SOMETHING WENT WRONG`, no note | — |
| `topup [--after-index]` | nothing on stdout (T19); the stamp; the same exits | `ProxyCards::runTopUp` (`ProxyCards.cpp:226-385`): 143/130 stopped, 69 after the index, 0 ok, any other COULDN'T FINISH with the stamp's why | 75, 77 and 78 are not named. A refused top-up shows no card unless the poll saw *a* `running` file, and the scan's own counts: a top-up refused with 75 while a scan runs can say `COULDN'T FINISH - SOMETHING WENT WRONG` | L-08 |
| `pending` | the count; 0 with N > 0, 1 with 0; 2 `cannot_tell` | exit 0 or 1, then `parsePendingCount` (`OfflineAchievements.cpp:108-111`) | none | — |
| `pending-ids` | `<id> <epoch>` lines; 0 / 1; 2 | every line (`:275-279`) | none | — |
| `summary` | one JSON object per line; 1 off/no account/no store; 2 | every line, `parseStoreGame`, a bad line skipped with a warning (`:250-261`) | a line over 1,023 bytes loses its head and its tail is parsed as a line (L-05); `null` counts are read (`OfflineAchievementsText.h:130`) | L-05 |
| `account` | `score=N softcore=N`; 1 no row; 2 (and T19's S8 makes non-numeric 2) | exit 0 only, then `parseAccountTotals` (`:286-289`) | none | — |
| `flushed` | `<epoch> <n>`; 0; 1 none. The stamp is taken by `mv` (`:803-818`) | `takeFlushed` (`:119-122`); `flushStampPresent` reads `exists` only (`:125-128`) | two readers, one taker: the rename makes the take exclusive | L-11 |
| `index-offline` | its exit | logged only (`:323-328`) | none | — |
| `ready`, `status`, `listening`, `images`, `refresh` | — | not run by EmulationStation | — | — |

- **T19's `02` § What T20 inherits is consumed here.** These rows are T20's half:
  - **Why tokens.** `STAMP_UNWRITABLE` (S5) and `RESULT_UNREADABLE` (S7) have no row in `scanWhy` and fall to `SOMETHING WENT WRONG`. **A correction to T19's table:** `TOOK_TOO_LONG` is not missing from the top-up's words, because `topUpWhy` falls through to `scanWhy` (`CloudText.cpp:1057-1064`), which has its row (`:1036`). `NO_GAMES_FOUND` (`:1032-1033`) is a row no producer emits, which was kickoff note 1 (L-08).
  - **`unknown` (S8)** is read as 0 by both readers (L-07, below).
  - **`disable`'s exits (S4, S5)** are L-09.
  - **PL-13, staleness:** the page's half is § The reader.
  - **PL-17, the refresh helper:** no reader at the pin; the helper's protocol is written, not tested.
  - **PL-18:** `NO_GAMES_FOUND` and the `have_account` comment (`GuiRetroAchievementsSettings.cpp:154`, which names a ctl function as if it were a verb).
  - **S9:** a name holding non-UTF-8 bytes reaches the page as those bytes. `TextFit::fitOneLine` cuts on characters; the guest shows what the font draws.
- **L-06, `WEXITSTATUS` without `WIFEXITED` (`ApiSystem.cpp:2290`).** **proved: fixture** (`stage-b/positives/reader.out`). When the process `popen` waits on dies by `SIGKILL` after printing `hardcore=0`, the reader returns rc 0 with that last line. So a top-up killed by a signal reads as COMPLETED, and an `enable` killed after its last line reads as on.
  - A `sh -c` child killed inside the shell reads 137 instead, because the host's `/bin/sh` is `dash` and did not exec it.
  - **On the image the ctl is not that process** (`guest-cycle/g02`): bash forks for a command with a redirection, so a ctl killed by a signal reads 128+N, not 0. The gap is real in the reader and reaches a page only through a wrapping shell that itself dies by a signal.
  - `OfflineScanJob::run` checks `WIFEXITED` (`:156-157`) and leaves -1, so the scan page is not affected.
- **L-05, the 1,024-byte buffer and the last line (`ApiSystem.cpp:2278-2288`).** **proved: fixture.**
  - A 1,500-byte line yields 2 lines: its first 1,023 bytes are dropped (the fragment has no newline, so `getline(...).good()` is false), the 476-byte tail passes as a line, then the next line.
  - A last line with no newline is dropped (`first\nhardcore=1` gives `first`).
  - The ctl's `tell` and `echo` end in a newline, so the second case needs a ctl that prints without one. The first needs a summary line over 1,023 bytes: a game title of roughly 900 bytes, rare but not bounded by the ctl.
- **L-07, `unknown` read as 0.** **proved: fixture** (`num.out`, `stamp.out`). This is the seam with T19's S8, which lands when T19's branch is integrated; at `8ebaf8daad` the ctl never says `unknown`.
  - **The scan page:** `>>> done 3|0|unknown|0` sets `ready` from -1 to `num("unknown") = 0` (`OfflineScanJob.cpp:196-205`, `:256`). The page then says `NO GAMES READY FOR OFFLINE PLAY YET` (`GuiOfflineScan.cpp:299`, `:304`) where it would have counted the export.
  - **The stamp:** `parseScanStamp` passes over `ready=unknown`, so `ready` stays at its default 0 (`CloudText.cpp:1259-1266`, `CloudText.h:492`). The top-up card then says `EVERYTHING'S UP TO DATE.` (`ProxyCards.cpp:353-368`), a count nobody measured.

## The reader

- **The markers** (`OfflineScanJob.cpp:171-263`): `pid`, `doing`, `total`, `game i|n|name` (the name may hold `|`), `cached`, `note` (four tokens), `errors`, `why`, and `done c|s|ready|limit`. Anything else is ignored.
- **Caps and lifetime:**
  - A line is capped at 1,024 bytes; the rest of an over-long line is dropped, not split (`:145`).
  - `num()` takes at most nine digits and reads anything else as 0 (`:196-205`; L-07).
  - The job is a detached thread holding its own reference (`:46`). It outlives the page, and posts through `AppWindow::post`, so a refresh after the window is gone is dropped (`:99-116`).
- **The stop path:**
  - `cancel()` sends `SIGINT` to the process group (`:77-78`), or defers it until the `>>> pid` line arrives (`:213-218`).
  - `stopRun()` signals only a pid that holds the lock file open (`OfflineAchievements.cpp:59-92`, `:330-353`).
- **L-10, `>>> pid` from any line.** `handleLine` accepts `pid` from every line, not only the first one `run()` itself prints (`:209-219`), and `cancel()` signals `-pid` as root. A later line `>>> pid 1` would make a cancel signal every process. No producer at `8ebaf8daad` prints such a line (`tell` prints the run's own words, and S9 replaces control characters in names), so this is defence in depth. **proved:** tree.
- **PL-13, the page's half.**
  - The row reads the `running` line through `runningProgress` (`OfflineAchievements.cpp:141-150`) and treats a line past its bound as a dead run (`CloudText.cpp:1335-1342`).
  - The scan page does not read `running`: it reads its own job.
  - So a scan's image pass, which runs after `run_jobs` removes `running`, leaves the settings row reading the last finished run for up to 300 s. The page itself still shows its spinner. **proved:** tree.

## The hasher

- **What it hashes and where it runs:**
  - `start()` builds the queue on the caller's thread (`ThreadedHasher.cpp:268-388`).
  - The constructor fetches the hash library and the official games list on the same thread (`:63`, `RetroAchievements.cpp:860-930`), then starts `hardware_concurrency()/2` threads (`:132-139`).
  - The callers: `SystemData.cpp:1134` (startup), `GuiMenu.cpp:1214`, `GuiRetroAchievementsSettings.cpp:800` (the save), `GuiHashStart.cpp:85` and `GuiNetPlaySettings.cpp:59`, plus `NetworkThread.cpp:251` through `postToUiThread`. All of them are the interface thread.
- **L-19, the bound:**
  - each request: connect 10 s (`HttpReq.h:52`), stall 30 s (`RetroAchievements.cpp:863`), total unbounded on purpose (#190);
  - the two requests transfer together and are waited on in turn, so the freeze is up to about 40 s with the link gone;
  - moving the fetch off the thread is #300's follow-up.
  - **proved:** tree.
- **L-20, `throw e;`.** At `RetroAchievements.cpp:925` and `ThreadedHasher.cpp:117`, `throw e` slices the `std::domain_error` to `std::exception`. The caller logs `Game Hash failed : std::exception` and, when not silent, shows a dialog whose whole text is `std::exception` (`:396`, `:399`). **proved: fixture** (`slice.out`: `GuiMsgBox text: [std::exception]`).
  - The path is the fetch failing with a status other than success, which is the offline case. Pressing INDEX GAMES offline with games to hash shows the offline card and then that dialog.
  - **Guest:** INDEX GAMES with the link down.
- **L-21, `start()` against `run()`.** **proved:** tree. A host positive is `CANNOT` (the class needs `Window`, `FileData` and `SystemData`, and the host has no SDL).
  - The constructor starts the threads (`:138`). `start()` then reads `hasher->mCheevosHashes` and `hasher->mTotal` (`:385-391`) and writes `mInstance = hasher` (`:392`).
  - A short queue, such as lookups alone with one game, can finish first. The last thread then runs `delete this` and sets `mInstance` to null (`:258-265`).
  - So `start()` reads freed memory and leaves `mInstance` pointing at it. The next `checkCloseIfRunning` then offers to stop a hasher that is gone, and `stop()` writes into freed memory (`:403-411`).
- **L-22:** `mExit` and `mPaused` are plain `bool`s read across threads; `pause()`/`resume()` have no callers. **proved:** tree.
- **L-23, the after-index top-up offline (blindspot 64).** The destructor runs `topUpAfterIndex` only when the library came and a game was identified (`:156-157`). Offline, the constructor marks the waiting games through `ProxyCards::indexRanOffline` (`:74-75`, `:113-114`), and the link's return lists them. **proved:** design.
- **The zero sentinel:** an RVZ the reader rejects is retried while it has no id (`GameCubeRvzHashRetry`, `:35-48`), at every run, by design. **proved:** design.

## The library

| File | Diff against `bccd715707` | Upstream it came from | In rcheevos 12.5.0? | Licence notice | #585 line owed |
| --- | --- | --- | --- | --- | --- |
| `CMakeLists.txt` | +17: `ENABLE_RVZ_HASH` (default `${ROCKNIX}`), zstd and Boost SHA-1 found or a `FATAL_ERROR` | fork-own | n/a (this is ES's wrapper) | — | none |
| `LICENSE.rvz-padding` | new | bodgit/rvz BSD-3 | n/a | itself; installed to `/usr/share/licenses/emulationstation/` (`package.mk:58-64`) | none |
| `RVZ-NOTICES.md` | new | fork-own notice (bodgit/rvz BSD-3; Boost and zstd declared, not copied) | n/a | itself; installed beside the licence | none |
| `cheevos.cpp` | +16: `gameCubeRvzHashEnabled()`; GameCube `.rvz` routed to `generateGameCubeRvzHash` before the readers | fork-own | n/a | — | none |
| `cheevos.h` | +3: the declaration | fork-own | n/a | — | none |
| `md5.c` | +10/-1: `MD5_SET` through `memcpy` on x86 (no misaligned or type-punned load) | libretro-common | `CANNOT` here: no 12.5.0 or libretro-common source without a fetch | — | a libretro-common line, owed |
| `hash_disc.c` | +26/-14: every `rc_file_read` checked; a `uint64_t` header sum; the two `rc_file_close` before an early return removed (the caller closes, `:546`); the `(uint32_t)` casts | rcheevos | `CANNOT` here (as above); the digest's read says absent | — | three rcheevos lines, owed: the read checks, the sum, the double close |
| `rvz_hash.cpp` | new, 389 lines: a bounded RVZ reader (every size `require`d, zstd frames checked, SHA-1 of the headers checked) | fork-own; the padding adapted from bodgit/rvz | n/a | SPDX `MIT AND BSD-3-Clause` header, the notice files | none |
| `rvz_hash.h` | new | fork-own | n/a | — | none |

- **rcheevos 12.2.1 with a stale 10.7.0 beside it** (R13): named for T44, not changed here.
- **L-24:** the #585 lines owed are written above in the shape the lane writes. Whether upstream 12.5.0 already carries each change is `CANNOT` without a tarball; the distribution's download cache holds only `raofflineproxy-rcheevos`, the proxy's copy.
- **L-25, one hash and three hashers (Q7):**
  - `padding()` uses shifts `{24, 18, 8, 0}`. That is Dolphin's documented oddity (`dolphin-WiaAndRvz.md:242`, "NB: 18, not 16"), not a slip.
  - Dolphin and RetroArch's `cheevos_rvz.c` apply the tweak to every word before the four `Forward()`s; EmulationStation applies it at output. The two agree because the tweak is a bit-selection, which is linear over XOR, so it commutes with `Forward`.
  - **proved: fixture** (`lfg.out`): ES's `padding()` verbatim against Dolphin's generator transcribed from the retained source, on 4,000 random seeds, offsets and sizes (3,032 at `offset % 4 != 0`), gives 0 mismatches. The control with shift 16 gives 4,000 mismatches, so the fixture can fail.
  - What remains is end to end: one synthetic RVZ with a packed region at `offset % 4 != 0`, hashed by EmulationStation's index, by the proxy's `.so` on the guest and by RetroArch, against the raw ISO's MD5. That is `guest`, and only if the image carries a GameCube RVZ fixture. The `make-fixtures.py` under `docs/qa-logs/2026-10-13-rvz-source/` writes padding with the same `{24, 18, 8, 0}`, so its fixtures agree with the readers by construction; the fixture above is the non-circular one.

## The runs

Each of the brief's § 5 commands at stage A. The output is in `stage-b/runs.out`; every rc is on its own line there.

| Run | What it reads | Exit | Wall | Figure | A FAIL would mean |
| --- | --- | ---: | ---: | --- | --- |
| R0 | the worktree, the stack, the ES pin, the merge base | 0 | 0.00 s | clean; the pin; 0; `bccd715707` | the read is not on the pin's bytes |
| R1 | the credentials' sinks | 0 | 0.02 s | the four keys at `:610`, `:611`, `:616`; `z=`/`y=` at `:149`; `p=` at `:1037` | a sink outside § The credentials' paths |
| R2 | the settings keys on the page | 0 | 0.01 s | as the brief | a key read or written where the table does not say |
| R3 | `HttpReq`'s peer checks | 0 | 0.01 s | `VERIFYPEER 0` `:192`, `VERIFYHOST 0` `:200` (#1154) | the cited state changed |
| R4 | `LOG(` lines naming a credential | 0 | 0.01 s | 2, the word *token* in prose (`:761`, `:792`) | a value in a log |
| R5 | `maskSecrets` users | 0 | 0.02 s | **11 files** (the brief: 10), none `RetroAchievements.cpp` | — |
| R6 | the ctl calls and the reader | 0 | 0.01 s | as the brief (`:321`/`:322`, `:479`, `:51-57`, `:2278-2291`, `:156-157`, `:145`) | a call § The contract does not list |
| R7 | `exists(` and its cache | 0 | 0.01 s | two cached reads of the ctl's own path; every ctl-written file with `false` | a cached read of a file another process writes |
| R8 | the client's bounds | 0 | 0.01 s | login with no total; pages 15 s / 10 s; library stall 30 s | a request with no bound where § The hasher says one |
| R9 | `ThreadedHasher::start(` | 0 | 0.01 s | five call sites and `NetworkThread.cpp:251` | a caller off the list |
| R10 | the strings, `es-untranslated` | 0 | 0.28 s | 222 `_("` occurrences; 706 of 706 with French | an untranslated fork string |
| R11 | `es-menu-map-check`, the map's `:595`, the scan title | 1 | 0.13 s | 55 screens, 0 missing; `:595` names PL-07; the title 0 (the final `grep -c`'s exit) | — |
| R12 | the walk and the baseline | 0 | 0.04 s | one walk, 36 lines; 0 in `suite.txt`, `claims.txt`, `masks.txt`; `ra-ui-test --help` 0 | — |
| R13 | the library's delta | 0 | 0.02 s | 9 files, +526/-15; 12.2.1 and a stale 10.7.0 | a fork edit outside the nine |
| R14 | the tests at the pin | 1 | 0.02 s | 15, 6, 7, 4 cases; CloudText 70; **0** RA cases by the brief's word regex (6 by subject) | — |
| R15 | the generated test build | 0 | — | `es-unit-tests` 185/185, `es-file-tests` 24, `es-conf-tests` 10, `es-file-tests-win32` 2, `jobs-tests` 6, `proxycards-tests` 11 (`00` § Stage A) | a failing case at the pin |
| R16 | `tools/es-syntax-check` | 2 (its own line) | 0.01 s | `CANNOT`: no build root | — |
| R17 | host `g++ -fsyntax-only` on three files | 0 (the loop) | 0.13 s | `CANNOT`: `SDL_joystick.h` for `OfflineAchievements.cpp` and `GuiOfflineScan.cpp`, `curl/curl.h` for `RetroAchievements.cpp` | — |
| R18 | the removal check, the ES diff | 0 | 0.01 s | both empty | the slice changed what it may not |

## The guest cycle

- **The grant and the posts:** the coordinator's grant on #667 at 17:34 UTC. **START 17:36:17 UTC, RETURN 17:57:04 UTC**, both posted on #667 with the census as their first line (START: qemu 1, :8080 0, compilers 0; RETURN: qemu 0, :8080 0, compilers 0), and both mirrored in the host file. The bound was 18:36:17. The record is `guest-cycle/` (`g01` to `g09`, the frames under `frames/w1` to `frames/w7`, the steps and the probe under `scripts/`).
- **The image** (`g01`): `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, `.sha256` OK. It ran on a fresh 16 GB disk of the lane's own, at 640x480 (`fbset`: `640 480`). Read from the guest:
  - `VERSION="0.0.1-dev+20261022T235948Z.g069fc2704421"`, `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`.
  - **The identity literal** `wifi picker: stopping scan worker`, added by the pin's own commit `16dbac521` and absent from its parent, is in the installed `emulationstation` (1).
  - **But the installed ES is M7's composition on top of the pin, not the pin's bytes.** Its offline page carries `CHECK AGAIN`, `Current setting: on.` and "Pending achievements stay on this device…", none of which is in `16dbac5211`'s tree (`git grep`: 0). The installed ctl is M7's (`2fcd5f290ac2`, against `8ebaf8daad`'s `47391a3bbcaa`), as T19 found.
  - So every page frame below is of M7's pages. A row of the pin's that M7 left alone reads the same, and the rows below say which. proved: guest.
- **L-06, `/bin/sh`** (`g02`): `/bin/sh` is `bash`, and it **forks** for `sh -c "cmd 2>/dev/null"` (the `sh` is the parent of the `sleep`, not replaced by it). A ctl killed by a signal therefore reaches `pclose` as 128+N, read 137, as on the host. On this image the gap needs the wrapping shell itself to die by a signal. The last line of `g02` is void: my kill by pattern hit `video_sense`'s `sleep 3600` (`g02b`). proved: guest.
- **The modes** (`g03`, M7's `enable` and a scan through the installed ctl): every file under `/storage/.config/raofflineproxy/` is **`644 root`**, `proxy.sqlite3` (with the session's row) and its `-wal` and `-shm` included; the folder is `755`; `system.cfg` is **`600`**; the scan lock is `644`. These are T19's figures again. proved: guest.
- **The live sign-in** (`g04a`, `g04b`): the QA RetroAchievements account was carried in by `tools/qa-accounts` (never printed; never the owner's, D-QA-015/016). The token was empty before the reboot and set after, written by the network watcher's sign-in. The frames: the main menu with its RETROACHIEVEMENTS entry (`w3/01`); the account page online (`w4/01`, `RETROACHIEVEMENTS - <name>` with the name painted out by `tools/png-blackout`, `Softcore points: 3`); a game's page online (`w3/02`, `w3/03`, 28 achievements, one unlocked on 2026-10-06); and the settings page (`w5`, the USERNAME value painted out). proved: guest.
- **L-20 on the guest** (`g05`): with `CheevosCheckIndexesAtStart` on and the link cut on the monitor (`set_link net0 off`), ES's restart ran the startup hasher, and `es_log.txt` reads `HttpReq::onError (3) : Could not resolve hostname`, then **`Game Hash failed : std::exception`**. The domain error's sentence is gone; the non-silent dialog shows the same `what()` (`slice.out`). proved: guest.
- **L-13 on the guest** (`g06`, `w6`): with offline achievements on and the last scan `COMPLETED` with `note NO_GAMES`:
  - a ready file of `7\n` (2 bytes, one game ready) makes the SCAN row say `LAST 10/26/2026 13:48 - COMPLETED · NO GAMES TO SCAN YET`;
  - `7\n12\n` (5 bytes) makes it say `… · 2 GAMES READY FOR OFFLINE PLAY`, updated by the 1 s refresher;
  - the file was then removed, as it was before. proved: guest.
- **The scan's walk** (`w7`): the confirmation reads `SCAN GAMES FOR OFFLINE ACHIEVEMENTS?` with the paragraph of `GuiRetroAchievementsSettings.cpp:345`, YES / NO. The page reads `SCANNING GAMES FOR OFFLINE ACHIEVEMENTS`, `COMPLETED`, `NO GAMES TO SCAN YET`, `ADD GAMES, THEN SCAN AGAIN.`, `ELAPSED 0:00`, `PRESS ANY BUTTON TO CLOSE`, and its help bar `CLOSE`, every string as `GuiOfflineScan.cpp:304-352` writes it. proved: guest.
- **L-01, #1154's unfixed half** (`g07`, `scripts/tls-probe.py`): with **dummy** credentials (the QA values replaced first; token and key emptied), a self-signed certificate for `retroachievements.org`, and `/etc/hosts` pointing that name at the guest's loopback:
  - a CA-checking `curl` got no answer (http `000`);
  - ES's sign-in reached the listener **1 s after ES started**: `GET /dorequest.php?r=login&u=<masked>&p=<masked> host=retroachievements.org`, the values masked by the listener before it wrote anything;
  - the listener was stopped by its PID and `/etc/hosts` restored (through `/run/rocknix/hosts`; `cp` refuses the link).
  - proved: guest.
- **`tools/ra-ui-test`: `CANNOT in this window`** (`g08`): four EN attempts under fresh `watch-build-submit --record-only` owners.
  - The first three failed closed on the tool's own preconditions, two of them states I had made: a configured account; an output directory that existed; a store from step 3 it does not own.
  - The fourth failed at its installed-identity census, after three PASS lines.
  - FR was not attempted. The cards stay T2's and T18's proofs.
- **An observation for M7, not this slice:** M7's `disable` exited 75 twice, its lock naming pid 5719 with no such process alive (`g08-ra-ui-pre.txt`).
- **The close** (`g09`, `retired.txt`): the account's four keys read empty; `vm-stop` rc 0 (pid 1705349); `t20.qcow2`, 2,311,585,792 bytes, sha256 `9c6dcda1af98d912746ebd02220cca3fa232df418170891b89f016c3c1c17e37`, retired; the leftover check found qemu 0, :8080 0, compilers 0.

## Positives

| Lead | The constructed failure | Where | Result on the pin's bytes | proved: |
| --- | --- | --- | --- | --- |
| L-06 | the `popen` child killed by `SIGKILL` after `hardcore=0` | `stage-b/positives/reader.cpp` (the reader verbatim) | rc 0, last line `hardcore=0` | fixture |
| L-05 | a 1,500-byte line, then a short one; a last line with no newline | the same | 2 lines, the longest 476; `first` kept, `hardcore=1` dropped | fixture |
| L-20 | `domain_error` through the two `throw e;` shapes | `slice.cpp` | `[std::exception]` | fixture |
| L-07 | `>>> done 3\|0\|unknown\|0`; `ready=unknown` in a top-up stamp | `num.cpp` (verbatim `num`); `StampProbe.cpp` built with the generated unit build | `num("unknown") = 0`; `ready=0` | fixture |
| L-13 | `cached_game_ids.txt` holding `7\n` | `readall.cpp` (`readAllText` verbatim) | `[]`: no game ready where one is | fixture |
| L-25 | ES's padding against Dolphin's, unaligned | `lfg.cpp`, its control | 0 of 4,000 mismatched; the control 4,000 of 4,000 | fixture |
| L-01 | the self-signed endpoint for #1154's unfixed half | guest (`g07`) | the sign-in's `r=login&u=…&p=…` reached a certificate no CA signed; `curl` refused it | guest |
| L-06 | whether the image's `/bin/sh` execs the ctl | guest (`g02`) | bash forks: the signal reads 128+N, so L-06 needs the shell itself to be killed | guest |
| L-20 | the startup hasher with the link cut | guest (`g05`) | `Game Hash failed : std::exception` | guest |
| L-13 | the SCAN row with a one-id export | guest (`g06`, `w6`) | `NO GAMES TO SCAN YET`; with two ids, `2 GAMES READY` | guest |

## The streams

One row per stage-E stream (`docs/reviews/briefs/t20-streams.md` at `60c1dc2db3`), on the ES branch `feature/m6-es-achievements-pages-667` unless the row says otherwise. Each stream's checks are in `stage-e/sN-checks.txt` (`tools/t20-stream-checks.sh`): the four unit binaries, the app targets under the sanitizers, the non-ASCII comment grep, the host syntax check (`CANNOT` with the missing header), and `es-untranslated`.

| Stream | Bug | Positive before | Commit | Positive after | Already written | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | #1170 (PL-01, High) | `tests/app-unit/hasher-tests`, the shipped `ThreadedHasher.cpp` against doubles under ASan and UBSan: heap-use-after-free at `start()` (`:383`) on the short-queue schedule; 36 thread objects leaked by the other two cases (`stage-e/s1-before.txt`) | `698040b5c` | 3 of 3 cases, 0 sanitizer reports, no leak (`stage-e/s1-after.txt`); the silent startup run's walk `stage-e/walks/s1-startup-lookups.steps` | kept; the next run reconciles; nothing migrated | fix-unit-test; the startup run fix-walk-pending-image |
| S2 | #1171 (PL-02, Medium) | the vendored client's login read at `rc_api_user.c:27-39` (POST, `r=login2`, `u`/`p` in the body); the request lifted as the pin builds it fails 5 of 5 (`stage-e/s2-before.txt`) | `d3137f992` | 2 of 2 pass; one `HttpReqOptions` field, `httpsRedirectsOnly` (T21's file, the brief's one field); a 401/403 JSON refusal read as the answer (`stage-e/s2-after.txt`); the listener walk `stage-e/walks/s2-signin-listener.steps` | passwords already sent in a query cannot be recalled; `system.cfg` as before; nothing migrated | fix-unit-test; the listener fix-walk-pending-image |

## Corrections and new leads from the seats

The stage-B text above is left as it was read; each change here names the seat's item that made it, and was re-read at its lines (`stage-c/astra-grades.md`).

- **L-01** (A-2): `VERIFYHOST 0` is set only in the client-certificate branch (`HttpReq.cpp:194-201`). `VERIFYPEER 0` alone admits a self-signed certificate for the right name, which is what the guest showed (`g07`). The redirect to `http` is a downgrade path; whether it would carry the query depends on the redirect's target.
- **L-03 narrowed** (A-4): `tokenOrError` reaches the dialog at `GuiRetroAchievementsSettings.cpp:784` only when `refused` is true (`:782-786`): the server's JSON `Error`, or the empty-account sentence, which is translated. curl's message, `Unable to parse response` and `Unknown error` lead to the reconnect dialog. The account page's `ra.error` (`GuiRetroAchievements.cpp:44`) and the hasher's `e.what()` remain.
- **L-04 corrected** (A-1, A-27, A-49):
  - The `User-Agent` carries the URL-encoded `z=` user, and only when an API login exists (`RetroAchievements.cpp:178-185`). It rides the sign-in and the hash library requests as well as the API's.
  - Two sinks were missing: the username's own editable row (`:610`), and the ctl's Python argv (`raofflineproxy-ctl:616`, `:647`, `:788`), where the account name is an argument.
- **§ The contract, `scan`** (A-9): 77 and 78 are not always refused before the page. TRY AGAIN restarts the ctl without the gates (`GuiOfflineScan.cpp:122-127`), so they can reach the page, which reads COULDN'T FINISH with the ctl's why.
- **L-07 narrowed** (A-10): with `added=unknown` the card says no count (`ProxyCards.cpp:368`). The defect is `ready=unknown` beside a numeric `added`.
- **L-09 widened to the pin** (A-8): `do_disable` writes the toggle off first (`:523-524`), then can `fail` at the hardcore restore, the record's clearing or the marker (`:538-544`). That exits 1 with the toggle off on disk while the page reverts its switch to on: a pin-era path, before T19's S5.
- **L-10 raised to Medium** (A-11): at `8ebaf8daad` the `game` line carries the ROM's basename unreplaced (`:1723`, `:1778`), and the scan reader ends a line at `\r` (`OfflineScanJob.cpp:143`). A ROM whose name holds a CR followed by `>>> pid 1` plants a second pid line, and a later CANCEL sends `kill(-1, SIGINT)` as root. ext4 `/storage/roms` admits such a name. proved: tree.
- **L-14 reframed** (A-19): the defect is the silently contradictory state (hardcore on with a casual-only feature on), and `disable` restoring a preference made obsolete since (`:529-540`), not the second writer as such.
- **L-19** (A-42): there is no total bound for a transfer that keeps moving. Medium, and #300's.
- **L-20 lowered to Low** (A-43): the HTTP cause stays in the earlier `onError` lines (`g05`); the screen's and the summary line's `std::exception` remain.
- **L-21 widened** (A-12, A-13):
  - the race needs at least one recognized hash;
  - the constructor pushes each `std::thread*` after creating it (`ThreadedHasher.cpp:138-139`), so the last worker can `delete this` before the final `push_back`;
  - `stop()` writes through an unretained pointer (`:403-411`).
- **L-22** (A-45): the `mExit` race is active (`stop()` writes it, the workers read it).
- **L-23's wording** (A-46): `mCheevosIndexed` means a library came and the queue was not empty (`:107`), not that a game was identified.
- **New leads:**
  - **L-26** (A-50): the hasher's `std::thread*` are never joined, detached or deleted (`:138`, `:258-265`). The LED switch's callback captures its own `shared_ptr` (`GuiRetroAchievementsSettings.cpp:688`). The toggle's thread posts through a raw `Window*` (`:484`), where the scan job uses `AppWindow::post`. Low. proved: tree.
  - **L-27** (A-51): readers that turn incomplete into empty. `storeSummary` returns `ok` after skipping every malformed line (`OfflineAchievements.cpp:252-263`); a missing or unreadable ready file reads 0 (`:152-165`); an unreadable `pending-ids` answer reads "none" (`:271-279`). Low. proved: tree.
  - **L-28** (A-52): `Success: true` with no `Token` returns true with an empty token, and the caller stores it (`RetroAchievements.cpp:1052-1056`; `GuiRetroAchievementsSettings.cpp:776-777`). Members are read without type checks. Low; Medium beside #1154. proved: tree.
  - **L-29** (A-53): a stopped hasher still toasts `INDEXING COMPLETED` (`ThreadedHasher.cpp:146`). `cancel()` marks the job cancelled before the signal and ignores its failure, and refuses a second CANCEL (`OfflineScanJob.cpp:65-80`), so an undelivered cancel has no way out. Low. proved: tree.
- **PL-13's page half** (A-54): `topUpRunning()` trusts the progress file as liveness, and a top-up reads another run's stamp by its time alone.

- **From Argon** (`stage-c/argon-grades.md`):
  - **L-04** (R-1): the comment at `RetroAchievements.cpp:173`, "Use empty UserAgent with doRequest.php calls", is stale: `getHttpOptions()` also serves `dorequest.php` (`:855-866`, `:1035`).
  - **L-28 joined** (R-23): `response` and `mdlist` are used as objects without `IsObject()` (`:879-880`, `:904-905`).
  - **L-30** (R-22): an empty hash library without an exception (a 200 carrying a captive portal's HTML or bad JSON) posts the offline card and makes `mTotal` 0. A non-silent run then shows `NO GAMES FIT THAT CRITERIA.` (`ThreadedHasher.cpp:383-390`), false there. Low. proved: tree.
  - **L-31** (R-24): `offlineScanStart` saves `SystemConf` (`GuiRetroAchievementsSettings.cpp:321`) before the parent page's save has cleared or replaced the token (`:743-807`). An edited username reaches `system.cfg` beside the previous account's token, and the scan runs with that pair. Low. proved: tree.
  - **L-32** (R-25): the game page prefixes a message already in the player's words with `AN ERROR OCCURRED` (`GuiGameAchievements.cpp:41-42` over `RetroAchievements.cpp:507`, `:513`). Low. proved: tree.

## What T21 and T26 inherit

- **`ask()`'s reader.** `ApiSystem::executeScriptLegacy` (`ApiSystem.cpp:2262-2293`) and its siblings (`:234`, `:270`, `:293`, `:329`, `:354`, `:397`, `:415`, `:440`, `:469`, every one `WEXITSTATUS` without `WIFEXITED`) are T21's. The users this slice found are `OfflineAchievements.cpp:51-57`, `:250`, `:275` and `GuiRetroAchievementsSettings.cpp:479`.
- **`HttpReq`'s options** (`HttpReq.h:45-65`: connect 10 s, total 0, stall 0) and its TLS settings (`HttpReq.cpp:192`, `:200`; #1154) are T21's. This slice's users are `RetroAchievements.cpp:174-186`, `:520`, `:633`, `:755`, `:863`, `:1035`.
- **The gates:** `offlineScanOn`, `offlineScanSignedIn` and `offlineScanOnline` (`GuiRetroAchievementsSettings.cpp:140-165`), and `exists("/usr/bin/raofflineproxy-ctl")` (`:633`), are T26's for the main menu's rows.
- **The title's source:** `RetroachievementsMenuitem` (`GuiMenu.cpp:190`, `:5760`; `SystemView.cpp:1616`) is T26's.
