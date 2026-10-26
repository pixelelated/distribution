# Second opinion (Phase 4.6), M6 T20: EmulationStation's RetroAchievements and offline pages, in pixelelated's EmulationStation fork

You are one of two independent reviewers for a read-only renovation audit of 25 files, read under a **security and new-functionality lens**. They total 7,485 lines at the EmulationStation commit `16dbac5211` (the distribution pins that commit).

- **The account client:** `RetroAchievements.{h,cpp}`. It signs in, and calls the web API and the local offline proxy.
- **The pages:** `GuiRetroAchievementsSettings`, `GuiRetroAchievements` (the account) and `GuiGameAchievements` (one game).
- **The offline half,** which drives a control script, `raofflineproxy-ctl`, and reads its files: `OfflineAchievements.{h,cpp}`, `OfflineScanJob.{h,cpp}`, and the scan page `GuiOfflineScan.{h,cpp}`.
- **The game hasher:** `ThreadedHasher.{h,cpp}`.
- **Nine files of the vendored libcheevos:** a bounded GameCube RVZ reader (`rvz_hash.cpp`), its notices, and five small edits to imported files.

**What ships.** The product is an immutable handheld OS; a person updates it in place and keeps `/storage`.

- EmulationStation is its interface, at 640x480 on the smallest panel.
- RetroAchievements is a third-party service the player signs in to. The "offline proxy" is a local service on `127.0.0.1:8080` that holds awards earned offline and sends them later; `raofflineproxy-ctl` is its shell control script, run as root.
- The rules the code answers to are named in `03` § 3.2.

**What you get.**

- The first reader is another lab's model. You get its `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md` whole.
- Then context: the order's entry, the brief's questions, the register rows the code cites, and the proxy audit's (T19's) list of what it hands this slice.
- Then the host fixtures' outputs and three guest records.
- Then four files whole and line-numbered: `OfflineAchievements.cpp`, `OfflineScanJob.cpp`, `GuiOfflineScan.cpp`, `ThreadedHasher.cpp`. Then `rvz_hash.cpp` whole, and the library's diff against its import.
- Then **line-numbered excerpts** covering every line the analyses cite, with eight lines of context:
  - `RetroAchievements.cpp`, `GuiRetroAchievementsSettings.cpp`, the two account pages, `ApiSystem.cpp`, `HttpReq.{h,cpp}`, `CloudText.{h,cpp}`, `ProxyCards.cpp`, `FileSystemUtil.cpp`;
  - the control script at the distribution commit `8ebaf8daad`.
- **When a claim needs lines outside the packet, say `outside the packet` and do not guess.**

**Masking.** Every section was passed through a mask that replaces a value after `key=`, `key:`, `token=`, `user=`, `pass...=` or `psk=` with `***`; a `***` is the mask, not the code. The packet was scanned for credential shapes before it left, and no hit was a value.

**Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. Its line numbers are the pin's.

**What was run.** Nothing can be run for you.

- The unit tests were built on the host and pass at the pin.
- Six fixtures were built from the pin's own lines; their outputs are in the packet.
- A guest window ran on an image whose EmulationStation is a **later composition over the pin**: its offline settings page differs from the pin's. So a page frame there is not the pin's page, and the first reader says which code path each guest proof exercised.

Answer these first, in this order:

1. **Credentials (`02` § The credentials' paths; Q1; L-01 to L-04).**
   - Is every sink of the username, password, token and web API key listed, at its line?
   - Is the password in a query string over an unverified peer, with redirects followed to `http`, a defect of this slice's code or only #1154's (`HttpReq.cpp`)?
   - Is the sign-in on the interface thread with no total and no stall bound (L-02) reached as `02` says?
   - What reaches the screen in a tool's words?
2. **The contract with the control script (`02` § The contract; Q2; L-05 to L-11).**
   - Are both readers' behaviours right? The 1,024-byte reader, the dropped last line, `WEXITSTATUS` without `WIFEXITED`, `>>> pid` from any line.
   - Is the guest's finding on `/bin/sh` (bash forks for a redirected command) enough to downgrade L-06?
   - Is each verb's row right against the ctl's lines?
   - Are L-07 (`unknown` read as 0) and L-09 (`disable`'s exit 1 with the toggle already off) real at the integration seam as described?
3. **Lifetimes and threads (§ The hasher, § The reader; L-19 to L-23).**
   - Is L-21 real? Can `ThreadedHasher::start` (`:383-392`) read `hasher->…` or store `mInstance` after the last `run()` thread has executed `delete this` (`:258-265`)? Is the silent lookups-alone run the short-queue case it says?
   - Does anything else hold a page, a job or a hasher across its own deletion?
   - Is the scan page's job ownership sound against CANCEL and TRY AGAIN?
4. **Files and pages (Q3, Q4; L-12 to L-18).**
   - Are the `exists(` cache readings right? Is the under-three-bytes read (L-13) right?
   - Is each dialog's button order safe, and is each row's store and save as `02` § The pages says?
   - Is HARDCORE MODE's second writer (L-14) a defect or the player's right?
5. **The library (Q6, Q7; L-24, L-25).**
   - Is each of the five edits bounded and correct (`hash_disc.c`, `md5.c`, `cheevos.cpp`, `cheevos.h`, `CMakeLists.txt`)?
   - Is `rvz_hash.cpp` safe against a hostile RVZ: integer overflow, a size taken from the file before it is bounded, a decompression bomb, a read past a buffer?
   - Is the padding argument (the bit-selection commutes with XOR) right?

Then:

6. **Refute or confirm each lead L-01 to L-25** in `02`: *confirmed*, *narrowed* (say how), or *refuted* (with the line). For the High and Medium ones in `04` § Risk assessment, also judge the severity, the fix a stream would make, and its `Already written:` line: what the code before a fix has already left on devices and in their clouds.
7. **What the first reader missed:**
   - a credential reaching a log, a command line, a file or the screen;
   - a reader that turns a failure into a success or a number;
   - a pointer used after its owner goes;
   - a string that promises what the code does not do;
   - a file read cached when another process writes it;
   - a bound missing on the interface thread.

**Output:**

- Numbered items `{PREFIX}-1`, `{PREFIX}-2`, ..., grouped under the seven headings above.
- Each item gets one line saying *confirmed / narrowed / refuted / new*, then the `file:line` evidence, then two to five sentences.
- Do not restate the packet, and do not reproduce long code.
- Keep the whole reply under about 8,000 words.


## The first reader's 02-forward-audit.md (whole)

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

## What T21 and T26 inherit

- **`ask()`'s reader.** `ApiSystem::executeScriptLegacy` (`ApiSystem.cpp:2262-2293`) and its siblings (`:234`, `:270`, `:293`, `:329`, `:354`, `:397`, `:415`, `:440`, `:469`, every one `WEXITSTATUS` without `WIFEXITED`) are T21's. The users this slice found are `OfflineAchievements.cpp:51-57`, `:250`, `:275` and `GuiRetroAchievementsSettings.cpp:479`.
- **`HttpReq`'s options** (`HttpReq.h:45-65`: connect 10 s, total 0, stall 0) and its TLS settings (`HttpReq.cpp:192`, `:200`; #1154) are T21's. This slice's users are `RetroAchievements.cpp:174-186`, `:520`, `:633`, `:755`, `:863`, `:1035`.
- **The gates:** `offlineScanOn`, `offlineScanSignedIn` and `offlineScanOnline` (`GuiRetroAchievementsSettings.cpp:140-165`), and `exists("/usr/bin/raofflineproxy-ctl")` (`:633`), are T26's for the main menu's rows.
- **The title's source:** `RetroachievementsMenuitem` (`GuiMenu.cpp:190`, `:5760`; `SystemView.cpp:1616`) is T26's.



## The first reader's 03-retrospective.md (whole)

# Retrospective audit — M6.P2 T20, EmulationStation's RetroAchievements and offline pages (#667)

The first reader's read of how the 25 sit in the system, at the pin `16dbac5211`, with the ctl at `8ebaf8daad`. The leads are `02`'s L-numbers.

## 3.1 Architectural coherence

- **Three layers, one direction.**
  - The pages (`GuiRetroAchievementsSettings`, `GuiOfflineScan`, `GuiRetroAchievements`, `GuiGameAchievements`) call two facades: `RetroAchievements` (the web and the proxy's HTTP) and `OfflineAchievements` (the ctl and its files).
  - The facades call `HttpReq` and `ApiSystem::executeScriptLegacy`.
  - The pure text is in `CloudText` and `OfflineAchievementsText`, with unit tests.
  - Nothing in the pages builds a command line beyond a fixed verb.
- **Two process readers with different contracts.**
  - `OfflineScanJob::run` reads byte by byte, caps each line at 1,024, and checks `WIFEXITED` (`:136-157`).
  - `ask()` and every other ctl verb go through `executeScriptLegacy`, which reads 1,024-byte chunks, loses a line's head past that, drops a last line without a newline, and reads a signal as exit 0 (L-05, L-06).
  - So the same ctl is read to two standards. The scan, the long job, got the careful reader; the short verbs, which decide the toggle and the top-up's card, got the shared one.
- **The hasher** fetches on the interface thread and hashes on its own threads. Its object's lifetime is owned by its last thread (`delete this`), while `start()` still holds the pointer (L-21). That is the one place where the ownership is not single.

## 3.2 Project conformance

| Rule | Where it holds | Where it does not |
| --- | --- | --- |
| `es-native-ui.md` § A file another process writes is read uncached | every ctl-written file is read with `exists(path, false)` (`OfflineAchievements.cpp:127`, `:136`, `:147`, `:156`, `:192`); the two cached reads are of the image's own `/usr/bin/raofflineproxy-ctl` (`:98`, `GuiRetroAchievementsSettings.cpp:633`) | — |
| `es-code-traps.md` § A file under three bytes | — | `readAllText` is unchanged at the pin (`FileSystemUtil.cpp:1369-1379`); `cached_game_ids.txt` with one one-digit id reads empty (L-13, fixture) |
| `es-code-traps.md` § A pooled connection | the hash library carries `stallTimeout` 30 s (`RetroAchievements.cpp:863`) | the sign-in at page close carries none, with total 0 (L-02) |
| `es-native-ui.md` § the fourth tier | the scan page is sat in, with CANCEL (`GuiOfflineScan.cpp:110-152`) | — |
| `es-ui-style-guide.md` § Confirmations | every dialog puts the safe choice last (L-16) | — |
| `player-language.md`: a tool's words never reach a player | the scan page's why goes through `scanWhy` | curl's message, the server's `Error`, two English literals and `std::exception` reach the screen (L-03, L-20) |
| `engineering-practices.md` § Guards must fail closed | `pending` and `pending-ids` accept only 0 and 1 (`OfflineAchievements.cpp:109`, `:277`) | a signal read as 0 (L-06); `unknown` read as 0 (L-07) |
| D-UI-039: a row changed updates the menu map | — | `:595` and the scan page's title are stale already (L-17) |

## 3.3 Spec fidelity

- **D-RA-010, D-RA-012 and D-RA-013** (the scan, the offer after enable, the index feeding the cache) are implemented as the rows say. The offer is suppressed until a sign-in exists (`GuiRetroAchievementsSettings.cpp:530-537`, fork #329).
- **D-UI-078** (the scan page is sat in) holds: back asks CANCEL while the run is up.
- **D-UI-095 and D-UI-107** (the cards and their words) are T2's and T18's; this slice reads only the top-up card's outcome mapping. Its words for an unmeasured count would be wrong after T19's S8 (L-07).
- **D-RA-001** (casual only: hardcore off while the proxy is on) is enforced once, by `enable`. The page lets the player turn HARDCORE MODE back on afterwards with no word (L-14). Whether that is a defect or the player's right is a question for the coordinator, not a finding.

## 3.4 Platform conformance

- **On the device:** GENERIC_X64 and the handhelds run the same scripts and binary. The two facts the host cannot answer are both guest steps:
  - whether `/bin/sh` on the image execs the ctl, so that a signal reaches `pclose`'s status (L-06);
  - the runtime files' modes.
- **The library** builds the RVZ reader only with `ENABLE_RVZ_HASH`, default `${ROCKNIX}`. It fails the configure without zstd and Boost's SHA-1 header, rather than building a hasher that silently skips RVZ (`CMakeLists.txt:230-244`).
- **`md5.c`'s x86 path** no longer dereferences a misaligned `uint32_t*`. That path matters to GENERIC_X64 only; ARM builds take the byte path.

## 3.5 Cross-system interaction audit

### Interaction: the ctl (T19) x the two readers

- **Who writes:** the ctl, at `8ebaf8daad` and after T19's stage E.
- **Who reads:** `OfflineScanJob::handleLine`, `ask()`, `ProxyCards::runTopUp`, `CloudText::parseScanStamp` and `parseRunningProgress`.
- **What fails at the seam:**
  - T19's S8 `unknown` is read as 0 by both readers (L-07, fixture).
  - T19's S5 `disable` exit 1 with the toggle already off leaves the page showing on, with in-memory `SystemConf` still on (L-09).
  - T19's S5 and S7 tokens `STAMP_UNWRITABLE` and `RESULT_UNREADABLE` have no row (L-08).
  - The ctl's 75, 77 and 78 for `topup` are not named by the card (L-08).
- **What holds:** `pending`, `pending-ids` and `account` read their exits fail-closed.
- **Owner:** T20's half; the ctl's half is T19's, already landed.

### Interaction: the hasher x the startup and the settings page

- **Who:** `SystemData.cpp:1134` (the silent startup run, lookups alone once a day), `GuiRetroAchievementsSettings.cpp:800` (the page's save), `GuiHashStart.cpp:85` (INDEX GAMES), and `NetworkThread.cpp:251`.
- **What fails:**
  - **The silent startup's lookups-alone run is the short-queue case.** Its threads read no file and can finish while `start()` is still writing `CheevosLookupOnlyLast` to `es_settings.cfg` (`ThreadedHasher.cpp:383-391`). `start()` then reads `hasher->mTotal` from freed memory and stores a dangling `mInstance` (L-21, tree).
  - **The non-silent run offline** shows `std::exception` (L-20, fixture).
- **Owner:** this slice, for the defect. The fetch on the interface thread is #300's (L-19).

### Interaction: the sign-in x the network watcher

- **Who:** the page's save (`:743-807`), `CheevosRetry::saveSignIn`, and `NetworkThread::checkCheevosTokenSoon`.
- **What holds:** offline and unchanged defers to the watcher's thread (`:758-761`).
- **What fails:** a change with an address signs in on the interface thread with no total bound. The freeze is as long as the server takes on a bad link (L-02).
- **Owner:** this slice. `HttpReq`'s defaults are T21's.

### Interaction: the toggle x the parent page's save

- **Who:** the offline page's thread writes through the ctl and mirrors `SystemConf` on success (`:500-501`). The parent page saves `HARDCORE MODE` and `CheevosCheckIndexesAtStart` at close.
- **What holds:** on success the mirror makes the parent's save write what the ctl wrote, and `CheevosCheckIndexesAtStart` is saved at once with the row updated (`:515-523`).
- **What fails:** on a failure that left the file changed (T19's S5), nothing is mirrored (L-09).

### Interaction: the three RVZ hashers

- **Who:** EmulationStation's index (`rvz_hash.cpp`), the proxy's `.so` (its rcheevos), and RetroArch (`cheevos_rvz.c`).
- **What holds:** the padding generator agrees with Dolphin's on 4,000 cases, 3,032 unaligned (L-25, fixture). Dolphin's generator is the one RetroArch's code follows by its own comment.
- **What is not proved:** one RVZ hashed end to end by all three. That needs a GameCube RVZ fixture on the guest.

### Interaction: M7's open work on these files

M7's October commits on the 25 are cited by number in `01`. This slice changes nothing before a stream brief, and the pin is the coordinator's to move.



## The first reader's 04-analysis.md (whole)

# Analysis — M6.P2 T20, EmulationStation's RetroAchievements and offline pages (#667)

The first reader's analysis, at the pin `16dbac5211` with the ctl at `8ebaf8daad`. Leads are `02`'s L-numbers; the evidence is `02`'s, at the lines it names. § Second opinion is written after stage C's two seats.

## Executive summary

- **The 25 paths read, 23 of them as code.** The account client and its pages, the offline half, the hasher, and the nine libcheevos files as diffs.
- **Seven leads are proved,** six on the host by fixtures built from the pin's own lines and four on the guest (three of them on both):
  - **the password over an unverified peer** (L-01, guest: the sign-in reached a self-signed listener that `curl` refused);
  - **`std::exception` as the player's and the log's whole message** (L-20, fixture and guest);
  - **`unknown` read as 0** at both readers of T19's S8 (L-07, fixture; the seam lands at integration);
  - **a one-id ready file read as no games** (L-13, fixture and guest);
  - **the shared process reader's** lost line heads and last lines (L-05, fixture);
  - **its signal read as exit 0** (L-06, fixture). The guest shows the ctl is not the process it waits on, so on the image this needs the wrapping shell itself to be killed.
- **One lead is read, not proved,** and is the most severe here: the hasher's `start()` reads and keeps a pointer its own threads may already have freed (L-21). The daily silent lookups-alone run at startup is exactly its short-queue case.
- **The library is clean.** The nine diffs are bounded and licensed, and the RVZ padding generator agrees with Dolphin's on 4,000 cases (L-25). Three rcheevos lines and one libretro-common line are owed to #585 (L-24).
- **The guest's ES is M7's composition over the pin.** So the window's page frames are M7's pages; the shared code paths still bear on the leads.

## Acceptance-criteria scorecard

| #667 criterion | State at stage C | Evidence |
| --- | --- | --- |
| the folder holds `00` to `05` | `00` to `04` written; `05` at stage D | this folder |
| `--phase pre-issue` lint PASS before stage D | at stage C's end | — |
| `review-plan.json`, two seats, provenance | stage C | `second-opinions/` |
| the punch list at Phase 7 outcomes; `box-check` 0 fail | after the stage-D rulings | — |
| `reviewed-at` and `reviewed-at-es`; the ES diff empty; no `packages/`/`projects/`/`tools/` change | held | `00`; R18 |
| `01` § Scope with the block and the table | done | `01` |
| `02` § Coverage 25 rows | done (the brief's command prints 25) | `02` |
| `02` § The credentials' paths | done | `02` |
| `02` § The pages | done; the two `es_settings.cfg` switches and their readers | `02` |
| `02` § The contract, T19's inheritance consumed | done | `02` |
| `02` § The reader and § The hasher | done | `02` |
| `02` § The library (9 rows; the three hashers) | done; 12.5.0's content `CANNOT` without a tarball | `02` |
| `02` § The runs | done | `02`, `stage-b/runs.out` |
| `02` § The guest cycle | done; `ra-ui-test` CANNOT in this window | `02`, `guest-cycle/` |
| `00` shows the never-run list kept | held so far; the keyed-invoke count at stage C | `00` |
| `04` § Q1 to Q8 | this file, § The questions | below |
| every proof has `proved:`; § What T21 and T26 inherit | done | `02` |
| the retro, posted | at close | — |
| the checkers on both branches | at hand-back | — |

## Risk assessment

| Lead | What | Severity | Likelihood | proved: |
| --- | --- | --- | --- | --- |
| L-21 | `ThreadedHasher::start` reads and stores a hasher its threads may have deleted (`:385-392` against `:258-265`) | High: use after free on the interface thread, a dangling `mInstance` that `stop()` then writes through | plausible daily: the silent lookups-alone run writes `es_settings.cfg` (file I/O) between the threads' start and the read | tree |
| L-01 | the password in the login's query string to a peer nobody verified, redirects followed to `http` | Medium; #1154 owns the peer | every sign-in with a changed account, and the watcher's at boot | guest |
| L-20 | `throw e;` slices to `std::exception`: a dialog whose whole text is that, and a log line with no cause | Medium (the player's words, and a diagnosis lost) | every non-silent index with the library unreachable | fixture, guest |
| L-07 | `unknown` (T19 S8) read as 0: NO GAMES READY…, EVERYTHING'S UP TO DATE. | Medium (a count nobody measured, said as fact) | once T19 merges, whenever the store cannot be read | fixture |
| L-09 | `disable`'s exit 1 with the toggle already off (T19 S5): the page shows on and `SystemConf` keeps on | Medium | once T19 merges, a service that will not stop | tree |
| L-02 | the sign-in on the interface thread with no total and no stall bound | Medium (a frozen screen of unknown length) | a changed account on a bad link | tree |
| L-13 | `readAllText` reads a file under three bytes as empty: one one-digit id reads as no games | Low (narrow) | a store holding exactly one game whose id is 1 to 9 | fixture, guest |
| L-05 | the shared reader drops a line's first 1,023 bytes, and a last line with no newline | Low | a summary line over 1,023 bytes; a ctl that ends without one | fixture |
| L-06 | `WEXITSTATUS` without `WIFEXITED` | Low on the image (bash forks) | the wrapping shell itself killed by a signal | fixture, guest |
| L-03 | curl's words, the server's `Error`, two English literals on screen | Low | sign-in failures | tree |
| L-08 | `STAMP_UNWRITABLE` and `RESULT_UNREADABLE` without rows; `NO_GAMES_FOUND` a dead row; 75/77/78 unnamed for a top-up | Low | once T19 merges | tree |
| L-10 | `>>> pid` accepted from any line; `kill(-1)` as root if one said 1 | Low (no producer prints it) | none at `8ebaf8daad` | tree |
| L-14 | HARDCORE MODE can be turned back on with the proxy on | question | — | tree |
| L-17 | the menu map's `:595` and the scan page's missing title | Low (D-UI-039) | — | tool-run |
| L-18 | a runtime msgid from a sound's name | Low | — | tree |
| L-19 | the hash library fetched on the interface thread, about 40 s bound offline | known: #300 | — | tree |
| L-22 | `mExit`/`mPaused` plain `bool`s across threads; `pause()`/`resume()` uncalled | Low | — | tree |
| L-24 | four #585 lines owed (rcheevos ×3, libretro-common ×1) | Info | — | tree |

## Coverage boundary

- **Read:** the 23 code paths at the pin whole or as diffs, and the two notices as present and shipped. Read where a contract crosses: `ApiSystem.cpp:2262-2293` and its siblings, `HttpReq.{h,cpp}`, `ProxyCards.cpp:196-385`, `CloudText.cpp` (the why tables, the stamp), `FileSystemUtil.cpp` (`readAllText`), and the ctl at `8ebaf8daad`.
- **Not read, owned elsewhere:**
  - `GuiMenu.cpp`'s rows and `SystemView` (T26);
  - `ApiSystem`'s command assembly and `HttpReq` beyond the options (T21);
  - `ProxyCards` beyond the top-up's outcome (T2 and T18);
  - the proxy's service and client (T19);
  - `GuiHashStart` (upstream, called only).
- **The guest's limit:** the window's ES was M7's composition over the pin, so a page frame is evidence about M7's page. Each proof on the guest says which shared path it exercised: the startup hasher, `readAllText` under the row, the sign-in's `HttpReq`.
- **CANNOT:**
  - `tools/es-syntax-check` (no build root here);
  - rcheevos 12.5.0's content (no tarball);
  - L-21's positive on the host (the class needs `Window`, `FileData` and `SDL`);
  - `ra-ui-test` in this window;
  - the three hashers end to end (no GameCube RVZ fixture on the image).

## The questions

### Q1 The credential's paths

- **Every sink, at its line:** `02` § The credentials' paths.
- **The peer:**
  - The password travels in the login's query string (`RetroAchievements.cpp:1037`), over TLS with the peer unverified. #1154 is cited, not re-found; its unfixed half is proved on the guest (`guest-cycle/g07`).
  - Redirects are followed to `http` or `https` (`HttpReq.cpp`, `REDIR_PROTOCOLS_STR "http,https"`).
  - The username rides the `User-Agent` and every query (L-04).
  - The web API key rides `y=` on every web request (`:149`).
- **At rest:** the four keys are clear text in `system.cfg` (`600` on the image). The rows mask the password and key.
- **The sign-in on the interface thread:** inside `addSaveFunc` (`GuiRetroAchievementsSettings.cpp:772-794`), when `CheevosRetry::saveSignIn` answers `Now`, with `HttpReq`'s defaults (connect 10 s, total 0, stall 0; `HttpReq.h:52-54`). The screen is frozen for as long as the server takes (L-02).
- **A tool's words on screen:** curl's message and the server's JSON `Error` (`:1040`, `:1063-1064`), shown at `GuiRetroAchievementsSettings.cpp:784`. Also `Unable to parse response` (`:1048`), `Unknown error` (`:1068`) and `std::exception` (L-20).
- **The runtime msgid** at `:671` (L-18).
- **`maskSecrets`** is unused here because nothing here logs a URL (R5, `HttpReq.cpp:559-563`).

### Q2 The contract, both ends

- **`ask()`'s reader:**
  - `WEXITSTATUS` without `WIFEXITED` is proved on the host (L-06). On the image the ctl's own signal reaches `pclose` as 128+N, because bash forks for a redirected command (`g02`). So "a top-up killed by a signal → COMPLETED" needs the wrapping shell itself to be killed.
  - The 1,023-byte split and the dropped last line are proved (L-05).
  - The last-line rule holds for every verb at `8ebaf8daad`: `hardcore=` last for `enable` and `disable`; the counts printed last.
- **`>>> pid`** is accepted from any line (L-10).
- **The outcomes per exit:**
  - the scan: 75 reads `SKIPPED - A SCAN IS ALREADY RUNNING`; 143 from `disable` reads `COULDN'T FINISH` with the generic why and no note;
  - the top-up: 75, 77 and 78 unnamed (L-08).
- **T19's inheritance** is consumed in `02` § The contract: L-07, L-08, L-09, PL-13's page half, PL-17 written, PL-18.

### Q3 The stamps and the files

- **`last-flush`:** two readers, one taker by `mv` (L-11, design).
- **`online_state.json` absent** reads as online, a recorded trade (PL-028; L-12, design).
- **`cached_game_ids.txt`:**
  - read every frame by the scan page only after a run that ended before its `done` line (`GuiOfflineScan.cpp:299`, when `s.ready < 0`);
  - read once a second by the row's refresher while the settings page is open;
  - **a two-byte file reads empty** (L-13, fixture and guest).
- **The modes on the image:** every proxy file `644 root`, `proxy.sqlite3` included; `system.cfg` `600` (`g03`). These are T19's figures, and the store's mode is T19's finding.
- **`exists(`:** every ctl-written file is read with `false`; the two cached reads are of the image's own ctl path, which is right (R7).

### Q4 The pages

- **Each page and dialog,** with its builder, store, save and button order: `02` § The pages.
- **The two `es_settings.cfg` switches** are read only by EmulationStation (`GuiMenu.cpp:190`, `:5760`, `:8533`; `SystemView.cpp:1616`; `SystemData.cpp:1127`; `NetworkThread.cpp:248`), so their store is right.
- **HARDCORE MODE** has two writers and nothing holding it off (L-14; a question).
- **`Settings.cpp:420`** is `#if WIN32` and not live on ROCKNIX (`Paths.cpp:94`).
- **The dialogs** all put the safe choice last (L-16).
- **The scan page** keeps the fourth tier's contract (guest `w7`).
- **The 1 s refresher** keeps its height, and the `layoutRows` trap is closed at the pin.
- **The menu map's** `:595` and the scan page's missing title (L-17).

### Q5 The hasher

- **The library fetch** runs on the interface thread for all its callers. Its bound is about 40 s offline: two requests waited in turn, each with connect 10 s and stall 30 s (L-19; #300 owns moving it).
- **The after-index top-up** never runs offline. The waiting games are marked instead and the link's return lists them (L-23, design; blindspot 64).
- **The `start()`/`run()` race** (L-21, High, tree).
- **`throw e;`** at `:117` and at `RetroAchievements.cpp:925` (L-20).
- **`e.what()`** shown outside `_( )` at `:399`.
- **`pause()`/`resume()`** have no callers (L-22).
- **The zero sentinel** re-hashes a rejected RVZ at every run while it has no id (design).

### Q6 The library

- **The nine diffs:** `02` § The library. Each is bounded, and the two notices are installed (`package.mk:58-64`).
- **#585 lines owed:** three for rcheevos (the read checks, the 64-bit header sum, the double close) and one for libretro-common (`md5.c`'s `memcpy`). Whether 12.5.0 has them is `CANNOT` without a tarball.
- **The stale 10.7.0 beside 12.2.1** is named for T44.

### Q7 One hash, three hashers

- **The generator agrees.** ES's `padding()` and Dolphin's generator agree on 4,000 random cases, 3,032 of them at unaligned offsets, and the control with shift 16 disagrees on all 4,000 (`stage-b/positives/lfg.out`). Dolphin's own specification says "18, not 16", and RetroArch's comment says it follows Dolphin.
- **What remains** is one synthetic RVZ hashed by all three against its raw ISO. That is `CANNOT` here: no GameCube RVZ fixture on the image, and `docs/qa-logs/2026-10-13-rvz-source/make-fixtures.py` writes padding with the same constants as the readers, so its fixtures agree by construction. **The harness work the question asks for** (`bugs-are-agent-first.md` rule 3) is a fixture built from Dolphin's own generator, not the readers'.

### Q8 The harness

- **`tools/ra-ui-test`** proves the reconnect cards with a synthetic award. It cannot prove these pages, and it fails closed on any state a lane has left. Three of four attempts in the window refused on the tool's own preconditions, two of them states I had made.
- **The one walk** (`tools/vm-walks/m7-retro-achievements.steps`) has no baseline, no claim and no mask (R12). So `frame-diff` catches no change to these pages: a harness gap for #1144's family.
- **`tools/es-menu-map-check`** reads titles, not copy (L-17).
- **`tools/es-untranslated`** reads 706 of 706 with French.
- **Positives:** host fixtures for L-05, L-06, L-07, L-13, L-20 and L-25; guest runs for L-01, L-06, L-13 and L-20.
- **What would prove L-21:** an AddressSanitizer build of ES running the silent lookups-alone path, which needs a toolchain and is a stream's `fix-unit-test` if the hasher's lifetime is moved into a testable unit.

## Renovation face

### Q1 Modernize

- **The two process readers become one.** `OfflineScanJob::run`'s byte reader, with its cap and `WIFEXITED`, is the better one; `executeScriptLegacy` serves every other verb. Moving `ask()` onto a reader with the same contract (a cap that keeps the line's head, a last line kept, a signal read as a signal) answers L-05 and L-06 together. The function itself is T21's.

### Q2 Standards

- **`player-language.md`:** no tool's words on screen (L-03, L-20).
- **`es-code-traps.md`:**
  - § A file under three bytes is live at the pin (L-13);
  - § A pooled connection: the sign-in has no stall bound (L-02).
- **D-UI-039:** the map's drift (L-17).

### Q3 Bugs

- **High:** L-21.
- **Medium:** L-01 (with #1154), L-02, L-07, L-09, L-20.
- **Low:** L-03, L-05, L-06, L-08, L-10, L-13, L-18, L-22.
- **A question:** L-14.

### Q4 Package currency

- rcheevos 12.2.1 is vendored, with a stale 10.7.0 tree beside it (T44's).
- The fork's own reader is new. Nothing here is a package with a release to follow.

### Q5 Efficiency

- The row's refresher reads three files a second while the settings page is open.
- The scan page reads `cached_game_ids.txt` every frame only in the no-`done` case.
- The library fetch is the one cost the player waits on (L-19, #300).

### Q6 Dead ends

- `NO_GAMES_FOUND`'s row has no producer (L-08).
- `pause()`/`resume()` have no callers (L-22).
- `GuiRetroAchievementsSettings.cpp:154` names a ctl function as if it were a verb.

### Q7 Clarity and structure

- The hasher's lifetime has two owners (L-21).
- The settings page's `openOfflineAchievements` is 185 lines of lambdas over weak pointers. It is careful, and its comments carry the reasons, but a unit for the toggle's thread and outcome would make L-09's case testable.

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **A guest identity check uses two literals:** one the pin added, and one the pin lacks (from the image's build branch), so "contains the pin" and "is the pin" are told apart (friction log 17:45 UTC). This belongs in `generic-x64-vm-testing.md` beside the window's identity step.
- **A process probe on a guest kills by `$!`, never by `pgrep … | head`** (friction log 17:37 UTC). `engineering-practices.md` already says it; a guest probe is where it was broken.

### Codification gaps (proposals for the coordinator)

- `es-code-traps.md` § A file under three bytes could name the readers this slice found (`readyIds`) so a later slice greps for the rest.

## Quality self-check

- **Re-read at its lines before writing:** every lead. Four line citations in `02` were corrected after a re-read (`:1048`, `:272`, `:403-411`, `:546`).
- **One lead was withdrawn** before it was written, the RVZ shift. **One correction** was made to T19's table (`TOOK_TOO_LONG` reaches `topUpWhy`).
- **Each guest proof names the exact code path it exercised,** and every page frame is marked as M7's composition.
- **The QA account's name** is painted out in three frames and written nowhere. The #1154 probe used dummy values, masked before logging.
- **Not checked:** L-21 at runtime; 12.5.0's content; the three hashers end to end.



## Context 1: docs/reviews/order.md § T20

```text
### T20. interface: EmulationStation's RetroAchievements and offline pages

- **id**: `es-achievements-pages`; **kind**: read; **lens**: security, new functionality
- **why here**: the account pages and the offline scan, which drive the proxy (16 interface files name it); with the fork-touched files of ES's vendored libcheevos (rcheevos and libretro-common), read as a diff against their imported version, since a local delta in the protocol library is invisible to a version row
- **paths** (25 paths, 7,485 lines, 7,427 read, of which 7,416 fork-own; 0 patch and config lines; reach shipped 25): areas `interface`; globs `es:es-app/src/{RetroAchievements,OfflineAchievements,ThreadedHasher,OfflineScanJob}.*`, `es:es-app/src/guis/Gui{RetroAchievements,OfflineScan,GameAchievements}*` **plus** areas `interface`; globs `es:external/libcheevos/**`
- **read before**: none
- **depth**: Extended -- `RetroAchievements.*` is on the security list: the account's credentials (plan § 6c)
- **interacting subsystems** (read-only context): the proxy (`offline-achievements`) and its own rcheevos; `ProxyCards` (`es-launch-path`); `ApiSystem` (`es-state-and-bridge`)
- **closing evidence**: audit folder, lint PASS, `tools/ra-ui-test`, punch list through Phase 7

```


## Context 2: the brief's § 4

```text
## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of four families: **where a credential
travels** (a query string, a header, an unverified peer, a log, a command
line, the screen), **a contract read one-sidedly** (an exit or a line one
end prints and the other does not expect), **a check whose failure reads as
success**, **a library edit without its upstream**. The leads below are
the digests' by shape; each is read at its lines before it is called
anything.

- **Q1 The credential's paths.** Every sink of the four keys at its line;
  #1154 cited, not re-found (the peer); the username in the `User-Agent`
  and in every query; the clear text at rest in `system.cfg` against what
  `backuptool` strips; the sign-in with timeout 0 and stall 0 **on the
  interface thread** inside `addSaveFunc` (`CheevosRetry::saveSignIn`'s
  `Now`) -- the screen frozen for as long as the server takes on a bad
  link (`es-code-traps.md` § A pooled connection); curl's `getErrorMsg()`
  and the server's JSON `Error` shown to a player verbatim
  (`player-language.md`: a tool's words never reach a player); the
  runtime msgid at `:671`; `maskSecrets` unused here.
- **Q2 The contract, both ends.** `ask()`'s `WEXITSTATUS` without
  `WIFEXITED` and what each caller then shows (a top-up killed by a
  signal → COMPLETED); the unmapped 75/77/78 for `topup`; the 1,023-byte
  `summary` line; the last-line rule against a ctl that prints two; the
  `>>> pid` accepted from any line and `kill(-n)` as root (`>>> pid 1`);
  the outcome per exit for the scan (75 as A SCAN IS ALREADY RUNNING, 143
  from `disable` as COULDN'T FINISH with no note); T19's inheritance table
  consumed when it lands, and this slice's half written as § The contract.
- **Q3 The stamps and the files.** The two takers of `last-flush`;
  `online_state.json` absent read as online; `cached_game_ids.txt` read
  every frame by the scan page and possibly two bytes; the runtime paths'
  modes as the ctl writes them (T19's finding: no `umask` anywhere -- read
  from the guest); `exists(` second arguments (all `false` for the ctl's
  files; the one cached read right).
- **Q4 The pages.** Every row's builder, store and save mechanism against `es-ui-style-guide.md` (two switches on `es_settings.cfg`: the proof's grep finds no file under `projects/` or `packages/` reading `RetroachievementsMenuitem` or `CheevosCheckIndexesAtStart` at `fbdcbde7d9`, so the store is right for both and the lane confirms it at its lines); HARDCORE
  MODE with two writers (the page and the ctl's `enable` line) and nothing
  holding it while the proxy is on; `Settings.cpp:420`'s same-named
  `.hardcore` default and who reads it; the dialogs' button order (all
  safe by the digest's read: NOT NOW / LATER / NO last -- verified at their
  lines); the scan page's fourth-tier contract and its every-frame reads;
  the settings page's 1 s refresher against the `layoutRows` trap (closed
  at the pin, ES `7c7ffab43`); the menu map's `:595` drift and the two
  missing entries.
- **Q5 The hasher.** The library fetch on the interface thread in four
  callers with its 10 s connect + 30 s stall bound (the freeze is the
  bound; moving it off the thread is #300's follow-up, not this slice's
  change unless ruled); the after-index top-up that offline never runs
  (blindspot 64); the `start()`/`run()` race for a short queue; `throw e;`
  slicing at `:117`; `e.what()` outside `_( )` at `:399`; `pause()`/`resume()`
  with no caller; the zero sentinel re-hashing permanently unsupported
  RVZs (a design fact, named).
- **Q6 The library.** Each of the nine as a diff: what the fork changed,
  the upstream it came from, whether upstream has it (the `hash_disc.c`
  read checks, the `uint64_t` sum and the double close absent from 12.5.0:
  three #585 lines for rcheevos; `md5.c`'s x86-only `memcpy`), the licence
  notices present and shipped (bodgit/rvz BSD-3; Boost and zstd declared,
  not copied); the stale 10.7.0 generation compiled beside 12.2.1 named for
  T44, not changed here.
- **Q7 One hash, three hashers.** The paper agreement of the three RVZ
  readers on the padding generator and on the partial-word case; what
  would prove it (one synthetic RVZ with a packed region at `offset % 4 !=
  0`, hashed by EmulationStation's index, by the proxy's `.so` on the
  guest, by RetroArch where it has the reader, against the raw ISO's MD5)
  -- `CANNOT` with the fixture named if no RVZ can be made without a
  fetch, and the coordinator's harness Backlog follows at the stage-D
  pause (`bugs-are-agent-first.md` rule 3).
- **Q8 The harness.** `tools/ra-ui-test` (what it proves: the reconnect
  cards with a synthetic award; what it cannot: the pages themselves),
  the one walk with no baseline and no claim (a `frame-diff` gap: every
  change to these pages is uncaught -- a harness finding for #1144's
  family), `tools/es-untranslated`, `tools/es-menu-map-check`'s blindness
  to copy; for each lead this slice confirms, the constructed positive
  that fails on the pin's bytes (the self-signed endpoint for #1154's
  unfixed half; a ctl stub killed by a signal under `ask()`; a `summary`
  line over 1,023 bytes; a two-byte `cached_game_ids.txt`), on the host
  where the pure parts allow (the generated `g++` build) and on the guest
  where they do not.

```


## Context 3: the register rows

```text
| D-UI-028 | 2026-09-10 | **Four outcome words for every cloud surface, then a why, what is in place, and how to recover.** `COMPLETED`; `COMPLETED WITH GAPS - <what>` (some of the run succeeded and some did not -- never reported as FAILED and never as COMPLETED, D-CLOUD-077); `COULDN'T FINISH - <why>` (nothing succeeded and it is not a sentinel); `SKIPPED - <reason>` only for the two sentinels (`NO NETWORK CONNECTION`, `ANOTHER CLOUD SYNC IS RUNNING`) and the launch cancel (`A GAME WAS STARTED`). The why comes from a `>>> why <sentence>` protocol line the scripts print at the failure point (rclone's taxonomy stays in the log), else from a small rc table; the in-place clause is one per verb (`WHAT WAS SENT IS IN YOUR CLOUD. THE REST IS STILL ON THIS DEVICE.`, `NOTHING ARRIVED. THIS DEVICE IS AS IT WAS.`); the recovery clause names the surface that retries (`TRY AGAIN`, or the row). `COMPLETED SUCCESSFULLY`, `SUCCEEDED`, bare `FAILED`, `STOPPED`, every log path and exit code retire from the screen. The card uses its action line for in-place + recovery; the transfer page keeps its seven fitted lines (D-UI-024) and gains `A TRY AGAIN  B CLOSE` on line 7 when the run did not complete. The row line under a toggle reads the same words with commas. Stamps gain a third field, the why token, additively. Register-of-record: the vocabulary table in `es-native-ui.md`. Fork resolved from the EmulationStation audit's proposal (docs/audits/2026_09_10-graceful-degradation). | #105 |

| D-UI-030 | 2026-09-10 | **A cloud run passes or fails; `COMPLETED WITH GAPS` is removed from the vocabulary (reverses that part of D-UI-028).** Maintainer, on getting it from a manual sync: *"if you don't know what the gaps are, it's not very helpful for you and it just makes you more anxious and trust the system less because it's working kind of. You'd rather just know it couldn't connect or it could connect."* A run whose parts disagree reads `COULDN'T FINISH - <why>` with the failing part's why, on card, page and rows alike. What did move is still said truthfully -- the card's in-place clause, the page's line 4 -- so nobody is told nothing happened when something did. The stamps keep the `gaps` token so a log can still tell a partial run from a total one. ES `cdbe284a5`. | #111 |

| D-UI-035 | 2026-09-10 | **A row that reports an outcome is composed from candidates, longest first, and the last candidate must fit any panel.** The card's action line already did this; the reason line was one string that clipped at ~70 characters on 640x480. Now `COULDN'T FINISH - <why> - <clause>` degrades to `COULDN'T FINISH - <why>` and then `COULDN'T FINISH`, measured in the row's own font on the interface thread. `460102b91`. | #115 |

| D-QA-015 | 2026-09-11 | **Every action that uses a handheld or the owner's cloud -- a game launch, pad input, a screenshot, a write under `/storage/roms`, a sync, an upload, a deletion in the cloud -- is asked for by name before it runs, with what it does on screen, what it writes, what it sends and what it leaves behind; a general offer of device testing is not a standing yes.** Extends D-QA-008/011 (reboot, staging) after the session ran the exit test and a Dropbox replacement proof on the RG35XX SP unannounced and the owner met the uploaded files in Dropbox first. Reads need no question. | maintainer, #130 |

| D-QA-021 | 2026-09-12 | **Every read of a device's or a QA guest's config goes through a secrets filter wider than the word *password*: `grep -v -i -E 'key\|pass\|token\|user\|psk'`.** A read needs no permission (D-QA-015) but lands in a transcript, and `system.cfg`, `rclone.conf`, `get_setting` output and anything piped back over SSH can carry a sign-in; rclone writes `pass =`, `user =`, `token =`, `key =`, and the network writes `psk`. The QA guests are in scope: their credentials are throwaway, their files are the same shape, and the transcript is the same transcript. A filter written as `password` let a `pass =` line through on a guest on 2026-09-12. Practice text moved into `engineering-practices.md` by the #147 sweep; long form in `docs/device-testing-policy.md` § Reading a device's output. (source: work log 2026-09-12 05:57 UTC, `6075c64f2e`; no maintainer quote on record) | #147, `6075c64f2e` |

| D-QA-016 | 2026-09-13 | **No new device is bought for QA now. Once the H700 round of testing is done and the work moves on to conflict resolution, the RG35XX SP becomes the testing-only handheld -- the maintainer plays on the RG353, the RG351 and the Retroid Pocket Nova -- and a more powerful Rockchip device is on offer if the tests need one (settles the open D-QA-016).** Maintainer: "Once we're done testing the H700 builds and move on to conflict resolution, we could turn the RG35XX SP into our testing-only handheld because I have the RG353, RG351, and the Retroid Pocket Nova. If we'd like a more powerful test device, I could get a Rockchip-powered one as well." Until that handover D-QA-015 governs (nothing on a person's device without a per-action yes). Still to choose: the QA device's own cloud accounts, so no test reads or writes the maintainer's data (#131's remaining box). | #131 |

| D-RA-001 | 2026-09-13 | **Offline RetroAchievements is a milestone of its own ("Offline RetroAchievements", #4), built on RAOfflineProxy packaged natively, offered to the player as a toggle whose line says it is a beta feature and casual-only, run in its own worktree (`feature/ra-offline`) in parallel with conflict resolution, and contributed back to misantronic/RAOfflineProxy where the fork improves it.** Maintainer: "I think offering a toggle for the proxy and explaining it is a beta feature and casual only would still add tremendous value. If we can contribute to the project, all the better. Supporting RAOfflineProxy seems like the right long-term solution. Let's definitely create a milestone, and this could be something we work on in parallel with conflict resolution in a different worktree and branch. With our new QA RA account and the VMs, we should be in a good position to build and test this." The project's Linux side is per emulator by construction (it patches `retroarch.cfg`, RetroArch and PPSSPP on ROCKNIX), so "system-wide" means the fork's toggle covers every emulator the proxy supports, not a network-level redirect. Settled from the open row of the same ID. | #163 (epic), #162, milestone 4; D-QA-016 |

| D-RA-010 | 2026-09-14 | **The OFFLINE ACHIEVEMENTS page offers a scan of every game on the console that caches each one's achievement data, so a game the player never started while connected still earns offline; the verb is "scan", never "sync"; and the issues found around offline play (#179 the scan, #180 viewing achievements offline) are built now, not parked.** Maintainer: *"we also need to have some sort of initial scan to cache every game on the console. [...] in the enable offline achievements screen, we need a way to allow someone to sync, which isn't the right word, but scan games to enable offline achievements so we cache everything. We should take care of any of the issues we identified related to that."* Settles #179's options: a page action on the fourth-tier surface for the scan, an automatic recently-played top-up on connect, one line of outcome under the row. | #179 comment of 2026-09-14; D-RA-008; D-RA-009; D-UI-022 |

| D-RA-012 | 2026-09-14 | **Turning OFFLINE ACHIEVEMENTS on offers the scan at once: a dialog `SCAN GAMES FOR OFFLINE ACHIEVEMENTS NOW?` with what the scan does, SCAN NOW / LATER; when the device is offline, one line saying to scan when connected.** Maintainer, on the RG SP with RC-5: *"When enabling offline achievements, it would be good to have a pop-up message asking the user if they want to scan, because otherwise, they may skip the scan process and be brought into a broken process."* | #184 note 3a; ES `feature/round-notes-rc5`; D-RA-010 |

| D-RA-013 | 2026-09-14 | **The offline cache follows the interface's own game index. The scan and the top-up read the index where it exists (games with a `cheevosId`, their hashes reused, no re-hashing) and hash everything only when there is none; the top-up on connect caches every game not yet cached, not only recently played ones; the OFFLINE ACHIEVEMENTS page says `NEW GAMES ARE ADDED THE NEXT TIME YOU'RE CONNECTED.`; and the GAME INDEXES option's text says, while offline achievements are on, that indexing also saves the new games' achievement data for offline play.** Maintainer: *"the idea of joining the existing scan and using that index might be helpful. And so your recommendation seems on point, including that new games are added the next time you're connected. And I just think we need to be clear that [...] scanning for retro achievements, or whatever this setting is called, [...] will cache new games discovered as well if we're piggybacking on that. Or perhaps even changing the text of that option when offline achievements are enabled."* Was open from notes 3b and 5b. | #184 notes 3b/5b; #179; D-RA-010 |

| D-UI-078 | 2026-09-21 | **Long work runs on a foreground page that owns the screen until it ends; the only way out while it runs is CANCEL, which says what cancelling means for that job (start over, or resume where the job supports it); backgrounding is for fast work only.** Reverses the fourth-tier shape of D-UI-060 and D-UI-070 (#186 PL-07, #187, rule commit `0462cf0141`) for the offline-achievements scan, the cloud transfer page and the scraper; the other background cards (index, content installer, OS update, Bluetooth) are classified per surface in #241. Maintainer, on the RG35XX SP at the scan page's PRESS B TO KEEP SCANNING IN THE BACKGROUND: *"we should only allow things to run in the background when they're fast. If it's something that's going to take longer time, like scraping or doing the RetroAchievements offline work, we should force that to be on a foreground page."* And on the way out: *"We could add a cancel button if we want to give them the option of backing out. That way, they would know explicitly that they would have to start over or resume if we can support that. Backgrounding is tricky because there are more edge cases we're introducing for what has to happen in order for them to then finish it, surfacing an alert when it finishes, etc."* The background shape had no end signal: a scan left with B reported only on the row that launched it, which the player had to go and find. | #241, #236, #187, D-UI-060, D-UI-070, D-UI-028, D-CLOUD-129 |

| D-UI-095 | 2026-09-26 | **Any automatic activity in the saves or achievements lanes that moves data over the network, or changes what the player will find earned or saved, is shown while it runs, and a launch over it asks the same question a sync gets; bookkeeping that only reads the device stays silent, and its failure is said once.** Maintainer: *"if there's activity happening in the background around RetroAchievements or save management, etc., we want to make sure we're showing the user what's going on. We want to enact the right gates to keep the user from proceeding without knowing what's going on"*; and *"if RetroAchievements were being sent and the user immediately tried to launch a game, we probably would want to show the same modal we show for save."* The inventory (#293): the startup and exit syncs and the transfer pages already have both; the proxy's send and the two top-ups have neither (D-RA-010's "nothing on screen" is superseded); the captures and the proxy's hourly re-read stay silent as bookkeeping, a failed capture to be said. The proxy's send is not ours to stop, so its question is wait or go; a top-up is stoppable, so its question is stop or wait. | #293, #292 |

| D-UI-107 | 2026-09-27 | **Every fork card's title names the thing and its line says what happened; no word is said twice across them, and the words are crisp, clear and warm. The send card: `RETROACHIEVEMENTS` over `SENDING N EARNED OFFLINE...`, then `WHAT YOU EARNED OFFLINE IS NOW ON YOUR ACCOUNT.` (short `NOW ON YOUR ACCOUNT.`), whys `IT STOPPED ANSWERING` / `THIS DEVICE'S OFFLINE SERVICE DIDN'T ANSWER`. The top-up card: `RETROACHIEVEMENTS (OFFLINE)` over `GETTING GAME I OF N READY...`, then `N MORE GAMES ARE READY.` / `N GAMES ARE READY.` / `EVERYTHING'S UP TO DATE.`. The sync cards keep their titles (D-UI-040) and their offline lines read `THEY'LL GO UP NEXT TIME YOU'RE CONNECTED(, WITH YOUR ACHIEVEMENTS).`, short `THEY GO UP WITH YOUR ACHIEVEMENTS WHEN YOU'RE BACK.`, and `THEY GO UP WHEN YOU EXIT THE GAME.`** Maintainer, 2026-09-27: *"We should do this in general and make sure it's not duplicative in terms of what the title says and what the body text is across the board."* and *"once we've done the redundancy sweep and made sure the language in toasts and our screens is crisp, clear, and not too cold, you're good to both transfer and reboot the device."* Rewords D-UI-096's sentence, D-UI-101's lines and D-UI-103's title; the outcome words (D-UI-028/030) and the sync titles (D-UI-040) stand. `RETROACHIEVEMENTS STOPPED ANSWERING` stays in `scanWhy`, read by the settings row without a title. The one-sentence toast of D-UI-093 stays a toast (it fits, and has nothing a title would add). The transfer and scan pages already passed the plain-language pass (#108) and are unchanged. | #303, ES `2178c9e6d`; swept: `es-player-text.md`, `es-native-ui.md`, `docs/es-menu-map.md` |

| D-WORKFLOW-195 | 2026-10-24 | **An Extended seat whose answer the model's output ceiling cuts on the packet is run again on a trimmed packet for that seat -- the same model, effort and provider; the analyses and tables whole, the cited files as line-numbered excerpts with context, the ask bounded -- never a model or effort substitution and never the same packet again.** `04` § Second opinion says the seats saw different evidence; an item one seat saw only in excerpt carries `excerpt`, and a disagreement that could be the excerpt's doing is resolved from the artifact, not from either seat. A fork resolved during execution on T30 (#677): Argon at `high` spent about 57k of its 65.5k output tokens reasoning on a 438 KB packet three times (`finish=length`), where T3's 308 KB packet took 30k. The maintainer may reverse it by a new row. | #677, #798; `adversarial-council.md` § Council model floor; the T30 hold post of 10:04 UTC and the coordinator's answer the same hour |

| D-RA-050 | 2026-10-26 | **The proxy's offline login answers only a request that presents the configured account's credential: the cached session token, or the password whose salted hash the proxy recorded at the last successful online `login2` that carried it; a request with no credential, a wrong one, another account, a `Host` that is not a loopback name, or any `Origin` gets the API's failed-login shape and no token.** At the pin `handle_offline_login` (`proxy_service.py:491-505`) returned the cached body and its token to any `login2` naming the account while upstream was unreachable (PL-01, F-01/F-02; fell on the guest, `b1-07`). The fix is a fork patch on upstream's handler and one storage column (rule 6 of `bugs-are-agent-first.md`) and a #585 line; a row with no recorded hash answers only the token until the next online login records one (read both). The password must be accepted because the client logs in with it on every start and holds the token only in memory. | #666 PL-01; `docs/reviews/briefs/t19-streams.md` S1; #585 |

| D-RA-051 | 2026-10-26 | **While the proxy's store holds no recorded password hash for the configured account, its offline login answers that account's password unverified, as the code before D-RA-050 did, until the first successful online login records a hash; thereafter the hash is compared.** RetroArch holds the session token only in memory and signs in with the password on every start, so the token-only reading of D-RA-050 refused every offline login on a device that updated and played offline before an online launch (T19's retro, 16:41). The exposure kept is the old one, loopback-only, bounded to one online launch; a foreign `Host`, an `Origin`, another account or no credential stays refused. This is `upgrade-and-install.md`'s *read both, write the new one*, which D-RA-050 claimed and 022 as first landed did not deliver. Refines D-RA-050. | #666 (the ruling of 16:42 UTC, `t19-streams.md` § S1b); #1157; D-RA-050 |
```


## Context 4: T19's 02 § What T20 inherits (at d8c02be1c9)

```text
## What T20 inherits

Written, not tested here.

**The protocol** (`>>> ` lines; the producers at `8ebaf8daad`, the readers at `16dbac5211`):

| Producer | Tokens (line) | Reader |
| --- | --- | --- |
| ctl `scan` | `doing listing` :1986; `total` :2018; `game i\|n\|name` :1723, :1778; `cached c\|s` :1776; `note NO_GAMES` :2012, `NOTHING_NEW` :2020, `LIMIT_REACHED` :2096, `TRUNCATED` :2100; `errors n` :2101; `why <TOKEN>` :1167, :1172, :1817, :1989, :2029, :2102; `done c\|s\|ready\|limit` :2015, :2106 | `OfflineScanJob` (the scan page), `CloudText::classifyProtocolLine` |
| ctl `topup` | none on stdout (`refuse_unless_ready topup >/dev/null`); the stamp only | `CloudText::parseScanStamp` (`CloudText.cpp:1186`) |
| ctl `images`, `refresh` | `why NO_NETWORK` :1897 and the helpers' own | **no reader at the pin** (no interface caller of either verb) |
| `raofflineproxy-refresh` | `doing refresh` :122; `total` :157; `refresh i\|n` :215; `note NOTHING_DUE` :152, `LEFT n` :169; `why STORE_UNREADABLE` :127, `NO_ACCOUNT` :133, `REPEATED_FAILURES` :222; `done a\|b` :153, :170, :223, :227 -- **b is `failed` at :227 and `left` at :170 and :223**; `note()` lines on the same stdout :50-51 | none at the pin (#224's row would be) |
| `raofflineproxy-cache-images` | `doing images` :284; `total` :379; `image i\|n` :433; `verified c\|n` :347, :356; `note VERIFY_COMPLETE` :358, `VERIFY_LEFT n` :362, `ABSENT n` :376, `NOTHING_MISSING` :381; `why STORE_UNREADABLE` :289, `NO_ACCOUNT` :296, `SOME_IMAGES_NOT_SAVED` :460, `CANCELLED` :495; `done f\|left` :382, :461 | the ctl sends it to `scan.log` under `run_image_pass`; none on screen |
| `raofflineproxy-cache-indexed` | none: `OK i/n`, `FAIL i/n label: why`, `DONE cached= failed= indexed=` (:162-216) | the ctl's `run_jobs` |

**The ctl's why tokens against `CloudText::scanWhy`** (`CloudText.cpp:1022-1055`) and `topUpWhy` (`:1057-1064`): the ctl emits TOGGLE_OFF, NO_ACCOUNT, SIGN_IN_REFUSED, RETROACHIEVEMENTS_STOPPED_ANSWERING, LIBRARY_UNREADABLE, TOOK_TOO_LONG, SOME_GAMES_NOT_SAVED, SOME_IMAGES_NOT_SAVED, CANCELLED, SOMETHING_WENT_WRONG, NO_NETWORK. `scanWhy` has a row for each but SOMETHING_WENT_WRONG and NO_NETWORK, which fall to its last line, `SOMETHING WENT WRONG` (the same words for the first; NO_NETWORK reaches no page). **`scanWhy` has a row for `NO_GAMES_FOUND`, which no producer emits** (the ctl says `note NO_GAMES`, fork #329): a reader row for a token gone.

**The stamps' shapes:** `last-scan` -- `<epoch> <rc> <scan|topup> cached= skipped= ready= limit= indexed= errors= added=[ truncated=1][ why=][ note=]` (ctl `write_stamp`; read by `parseScanStamp`, `CloudText.cpp:1186-1270`, which passes over unknown keys and a non-numeric `added`); `last-flush` -- `<epoch> <flushed>` (patch 003; taken by the ctl's `flushed`, `OfflineAchievements.cpp:119`); `running` -- `route=<scan|topup|images|refresh> at=<epoch>[ index= total= name=]` (ctl `mark_running`; read at `CloudText.cpp:1312-1330`); `index-pending` -- `<epoch> <pid> <random>` (the ctl's alone). The exit codes the pages act on: 0, 1, 2 (usage at `:2453` and every `cannot_tell`; `listening` and `refresh` use 64 for usage), 69, 75, 77, 78, 130, 143.

**The page comment's wording:** `GuiRetroAchievementsSettings.cpp:154` names `raofflineproxy-ctl have_account` as if a verb; it is the ctl's function (:1119, called :1170), not in the dispatch (:2434-2450).

**The consent setting's name:** `usage_stats_consent` (with `usage_stats_consent_version`) in the client's `config.json` (patch 019; `usage_report.py:180`); `upload_logs` (JSON `true` only) for the automatic log upload (patch 008).

**Handed to T20 (#667) at the stage-D ruling** (#666, 13:48 UTC):

- **PL-13, the staleness contract.** The scan has no deadline, by design: it is a foreground page with CANCEL (D-UI-078). The interface treats a `running` line older than its bound as a dead run "because the ctl bounds its runs" (`CloudText.cpp:1335-1342` at `16dbac5211`). `run_jobs` removes `running` before the image pass, so the interface sees no run for up to 300 s while one is going (A-19, A-54, R-17). The two must agree on one contract: what a scan's `running` line promises about its age, and what the page does past it. T20 owns the page's half.
- **PL-17, the refresh helper.** `raofflineproxy-refresh` puts `note()` lines on the protocol's stdout, and its `done a|b` reads as failed, left, or every one unfinished, by path (`refresh:170`, `:223`, `:227`). `row_ages` reads three whole prefixes per game (F-40). No interface caller exists at the pin. The row #224 would add, and the helper's protocol it would read, are T20's.
- **PL-18, the reader's rows.** `scanWhy` keeps `NO_GAMES_FOUND` (`CloudText.cpp:1032-1033`), which no producer emits; since fork #329 the ctl says `note NO_GAMES` with rc 0. The page comment at `GuiRetroAchievementsSettings.cpp:154` names `have_account` as a verb (above). Both are T20's.

**From stage E** (each stream adds its line here as it lands):

- **S1, the offline login's refusal (#1157, D-RA-050).** An offline `login` or `login2` that does not present the configured account's credential is now answered 401 `invalid_credentials`, `Success: false`, no token, no `X-RA-Offline`. No interface reader parses it: EmulationStation signs in to retroarchievements.org directly (`RetroAchievements.cpp:1037` at `16dbac5211`), not through the proxy. The emulator meets the refusal; what RetroArch shows for a 401 is not read here and is `fix-walk-pending-image` (its `(offline)` toast, patch 0013 in the retroarch package, keys on `X-RA-Offline`, which a refusal does not carry). No `>>> why` token is added.
- **S1 and S1b, for the integration: the upgrade path (D-RA-051).** RetroArch logs in with the password (D-RA-050). As S1 first landed, a device that updated and then played offline before any online launch had no recorded hash, and its offline login was refused until an online launch recorded one. S1b (#1157, ruled 16:42 UTC) amends 022: while no hash is recorded for the configured account, its password is answered unverified, as before, and the service's log says so once. The first successful online `login2` records the hash, and from then on it is compared. The player meets no change on the upgrade path; the exposure kept is the old one, loopback-only and bounded to that first online launch. The integration's upgrade rehearsal seeded with a store from before the column, followed by an offline launch, should see the login answered (`fix-walk-pending-image`).

- **S2, for the integration (#1158, D-RA-049).** The unit runs `private-modes` as `ExecStartPre=-`: a file it cannot change is logged and the start goes on, as before the pass existed (the dash is the lane's reading; a failure that stopped the service would take offline achievements down over a mode). `enable` says such a failure and keeps the toggle on. Two owed items: the upgrade rehearsal seeded with a 644 proxy folder, and the service's effective umask read on the image. **Observed, not changed:** under the ctl's `umask 077`, a `system.cfg` the ctl rewrites through `set_setting` becomes 0600, because #421's `prepare_settings_temp` never relaxes the caller's umask (`stage-e/s2-after.txt`, case 4). The marker becomes 0600 too. Every reader of either on the image runs as root; reading cannot prove there is no other.

- **S4, for T20 (#1160).** `disable` can now exit 2 (`cannot_tell`: the lock could not be opened, nothing changed) or 1 (a scan or top-up did not stop within 10 s; the toggle is put back and the device stays on). Before, it carried on and exited 0 in both cases. How the interface's toggle reads those two exits is T20's. A helper the ctl started under `timeout(1)` that ignores TERM and the watchdog's KILL can outlive its wrapper (the KILL reaches the wrapper, not the helper), but it no longer holds the lock.

- **S5, for T20 (#1161).** A run that otherwise completed but could not write its stamp now ends 1 with `>>> why STAMP_UNWRITABLE`. That token is new to the interface's table and falls to the generic sentence (`CloudText::scanWhy`); its row and French are T20's. A run already ending non-zero keeps its own code and why. `disable` ends 1 when the service would not stop, with everything else done. The `stop` verb now exits 1 when `systemctl stop` fails, where it exited 0.

- **S7, for T20 (#1163).** S7 emits three why tokens, read against the interface's table at the ES pin `16dbac5211`:
  - `RESULT_UNREADABLE` (a recently played pass that exited 0 with no result line that could be read): **no row**. It falls to the generic sentence until T20 gives it a row and French.
  - `TOOK_TOO_LONG` (a top-up with too little time for the recently played pass, which ended 0 with nothing said before): a row in `CloudText::scanWhy` (`:1036`), **none in `topUpWhy`** (`:1057-1064`).
  - `SOME_IMAGES_NOT_SAVED` (a missing image helper; a damaged image `--verify` could not remove): rows in both (`:1047`, `:1061`).
  - S5's `STAMP_UNWRITABLE` has no row either.

- **S8, for T20 (#1164).** A count the ctl could not read is now `unknown`, never a number. It appears in the stamp's `ready=` (beside the existing `added=unknown`) and in the page's `>>> done <cached>|<skipped>|unknown|<limit>` line. `ready` exits 2 with nothing on stdout, as `pending` does. `account` exits 2 (`cannot_tell`) for a `login2` row that is not a JSON object or a score that is not a number, where it exited 1 (no points) or printed a boolean as 1. Whether `CloudText::parseScanStamp` and the page's `done` reader accept `unknown` for `ready` is T20's to read.

- **S9, for T20 (#1165).** Only the ctl reads the job file and the helper's lines, and both change: entries are NUL-separated, and the helper prints `<KIND> <i>/<n><TAB><reason><TAB><label>`. Two things reach the interface. The game name in `>>> game i|n|name` has its control characters replaced by `_`. A name holding a byte that is not UTF-8 reaches the page as that byte. How the page shows such a name is T20's.

```


## Evidence: stage-b/positives/reader.out

```text
RESULT popen-child-killed rc=0 lines=1 longest=10 last=[hardcore=0]
RESULT killed-by-signal rc=137 lines=1 longest=10 last=[hardcore=0]
RESULT exit-143 rc=143 lines=1 longest=10 last=[hardcore=0]
RESULT line-1500-bytes rc=0 lines=2 longest=476 last=[{"id":2}]
RESULT last-line-no-newline rc=0 lines=1 longest=5 last=[first]
```


## Evidence: stage-b/positives/slice.out

```text
GuiMsgBox text: [std::exception]
```


## Evidence: stage-b/positives/num.out

```text
num("3") = 3
num("unknown") = 0
num("") = 0
State.ready initial -1 (OfflineScanJob.h:40); after ">>> done 3|0|unknown|0": 0
```


## Evidence: stage-b/positives/stamp.out

```text
PROBE ran=1 code=0 topup=1 ready=0 added=0
[doctest] test cases: 1 | 1 passed | 0 failed | 185 skipped
```


## Evidence: stage-b/positives/readall.out

```text
/workspace/tmp/m6-t20/pos/ids-one -> [] /workspace/tmp/m6-t20/pos/ids-two -> [7 12 ] 
```


## Evidence: stage-b/positives/lfg.out

```text
Q7 padding: cases=4000 unaligned=3032 mismatches=0
control (shift 16): Q7 padding: cases=4000 unaligned=3032 mismatches=4000
```


## Evidence: guest-cycle/g02-sh-exec.txt

```text
== step 2, /bin/sh and exec (17:37:11Z)
/usr/bin/bash
lrwxrwxrwx    1 root     root             4 Oct 22 20:02 [1;36m/bin/sh[m -> [1;32mbash[m
[1] 2003
popen-like child pid 2003 comm: sh args: sh -c sleep 7 2>/dev/null 
    358       1 sh
   2003     358 sh
   2005    2003 sleep
--- a killed child read through the shell: 
rc of sh -c killing itself: 137
[2] 2042
rc when the exec-ed command is KILLed: 0
```


## Evidence: guest-cycle/g05-l20-startup-offline.txt

```text
== step 5, L-20 on the startup hasher, the link cut (17:47:25Z)
set_link net0 off
0
168:2026-10-26 13:47:30	[3261]	ERROR	HttpReq::onError (3) : Could not connect to server
169:2026-10-26 13:47:30	[3251]	ERROR	HttpReq::onError (3) : Could not resolve hostname
170:2026-10-26 13:47:30	[3251]	ERROR	HttpReq::onError (3) : Could not resolve hostname
171:2026-10-26 13:47:30	[3251]	ERROR	Game Hash failed : std::exception
172:2026-10-26 13:47:31	[3260]	ERROR	HttpReq::onError (3) : Could not resolve hostname
```


## Evidence: guest-cycle/g06-l13.txt

```text
== step 6, L-13 (17:48:45Z)
ls: /storage/.config/raofflineproxy/cached_game_ids.txt: No such file or directory
2
control bytes: 5
ready file removed (it did not exist before step 6)
```


## Evidence: guest-cycle/g07-l01-tls.txt

```text
== step 7, L-01 / #1154's unfixed half, dummy credentials only (17:52:44Z); the first attempt stopped at openssl req: no /etc/ssl/openssl.cnf on the image, nothing changed
openssl rc 0; cert: issuer=CN=retroachievements.org subject=CN=retroachievements.org 
the QA values replaced by dummies (username t20probe, password t20dummy; token and key emptied)
listener on :443: 1
a CA-checking client (curl) against it: http 000 rc 0
essway started 13:52:46
-- requests that reached the self-signed listener:
13:52:47 GET /dorequest.php?r=login&u=<masked>&p=<masked> host=retroachievements.org
  File "/usr/lib/python3.14/ssl.py", line 1138, in read
BrokenPipeError: [Errno 32] Broken pipe
----------------------------------------
168:2026-10-26 13:52:46	[5664]	ERROR	HttpReq::onError (3) : Could not connect to server
listener pid 5527: python3 /storage/t20-tls-probe.py /storage/t20tls/c.pem /storage/t20tls/k.pem /storage/t20tls/requests.log 
listener on :443 after: 0
hosts entries for retroachievements.org: 1
hosts restored through its target: retroachievements.org entries 0
```


## es-app/src/OfflineAchievements.cpp @ 16dbac5211 (whole, 353 lines)

```text
    1  #include "ProxyCards.h"
    2  #include <csignal>
    3  #include <cstdlib>
    4  #include "OfflineAchievements.h"
    5  #include "RunLock.h"
    6  #include "ApiSystem.h"
    7  #include "CloudText.h"
    8  #include "HttpReq.h"
    9  #include "LocaleES.h"
   10  #include "Log.h"
   11  #include "SystemConf.h"
   12  #include "Window.h"
   13  #include "utils/FileSystemUtil.h"
   14  #include "utils/OfflineProxyUrl.h"
   15  #include "utils/Platform.h"
   16  #include "utils/StringUtil.h"
   17  #include <chrono>
   18  #include <ctime>
   19  #include <dirent.h>
   20  #include <string>
   21  #include <sys/stat.h>
   22  #include <thread>
   23  
   24  namespace
   25  {
   26  	const char* CTL = "/usr/bin/raofflineproxy-ctl";
   27  	// Where the proxy keeps everything it writes (the unit's
   28  	// RAOFFLINEPROXY_CONFIG_DIR), and the two files the scan reads back.
   29  	const char* SCAN_STAMP = "/storage/.config/raofflineproxy/last-scan";
   30  	// The one line the ctl keeps while a scan or top-up runs its jobs,
   31  	// rewritten as each game finishes and removed when the run ends (fork
   32  	// #189); CloudText::parseRunningProgress reads it.
   33  	const char* RUNNING_FILE = "/storage/.config/raofflineproxy/running";
   34  	const char* READY_FILE = "/storage/.config/raofflineproxy/cached_game_ids.txt";
   35  	// The proxy's own answer to "can RetroAchievements be reached", written
   36  	// by its connectivity monitor (state.py save_online_state).
   37  	const char* ONLINE_STATE = "/storage/.config/raofflineproxy/online_state.json";
   38  	// The proxy's flush stamp (the ctl's FLUSH_STAMP): present until a
   39  	// reader takes it. And the ctl's lock, holding the running pid.
   40  	const char* FLUSH_STAMP = "/storage/.config/raofflineproxy/last-flush";
   41  	const char* SCAN_LOCK = "/var/run/raofflineproxy-scan.lock";
   42  
   43  	// How long one question to the proxy may take, in all. It answers from
   44  	// its store on the same device in milliseconds; anything longer is a
   45  	// proxy that is not answering, and the page must not wait on it.
   46  	const long PROXY_CONNECT_MS = 2000L;
   47  	const long PROXY_TOTAL_MS = 15000L;
   48  
   49  	// The ctl's last stdout line and its exit status. executeScriptLegacy is
   50  	// the public route that hands back both, as the toggle's page uses it.
   51  	std::pair<std::string, int> ask(const char* verb)
   52  	{
   53  		std::string last;
   54  		auto result = ApiSystem::executeScriptLegacy(std::string(CTL) + " " + verb + " 2>/dev/null",
   55  			[&last](const std::string line) { last = line; });
   56  		return std::make_pair(last, result.second);
   57  	}
   58  
   59  	// Whether process `pid` has `path` open (audit of the fix round,
   60  	// G2-E-app-05 gpt / G2-E-app-06 claude). RunLock::holder names the pid
   61  	// in the lock file when the lock is held and that pid's command line
   62  	// mentions the ctl -- a mention, not an identity. The ctl writes its pid
   63  	// just after it takes the lock, so for that moment, and after a run
   64  	// killed -9, the file names an earlier run's pid, which may by now be
   65  	// anything whose arguments say raofflineproxy-ctl: a tail of its log, a
   66  	// grep. The run that holds an flock holds the file open, so a pid is
   67  	// signalled only when one of its descriptors is that file (the same
   68  	// device and inode).
   69  	bool holdsOpen(long pid, const std::string& path)
   70  	{
   71  		struct stat want;
   72  		if (::stat(path.c_str(), &want) != 0)
   73  			return false;
   74  		const std::string fds = "/proc/" + std::to_string(pid) + "/fd";
   75  		DIR* dir = ::opendir(fds.c_str());
   76  		if (dir == nullptr)
   77  			return false;
   78  		bool found = false;
   79  		while (struct dirent* entry = ::readdir(dir))
   80  		{
   81  			if (entry->d_name[0] == '.')
   82  				continue;
   83  			struct stat got;
   84  			if (::stat((fds + "/" + entry->d_name).c_str(), &got) == 0 && got.st_dev == want.st_dev && got.st_ino == want.st_ino)
   85  			{
   86  				found = true;
   87  				break;
   88  			}
   89  		}
   90  		::closedir(dir);
   91  		return found;
   92  	}
   93  }
   94  
   95  bool OfflineAchievements::available()
   96  {
   97  	// The image's own file: static for the session, so the cache is right.
   98  	return Utils::FileSystem::exists(CTL);
   99  }
  100  
  101  int OfflineAchievements::pendingAwards()
  102  {
  103  	if (!available())
  104  		return -1;
  105  
  106  	// 0 with the count, 1 with 0; anything else is the ctl saying it could
  107  	// not tell, and prints no number to be mistaken for one.
  108  	const auto answer = ask("pending");
  109  	if (answer.second != 0 && answer.second != 1)
  110  		return -1;
  111  	return CloudText::parsePendingCount(answer.first);
  112  }
  113  
  114  bool OfflineAchievements::takeFlushed()
  115  {
  116  	if (!available())
  117  		return false;
  118  
  119  	const auto answer = ask("flushed");
  120  	if (answer.second != 0)
  121  		return false;
  122  	return CloudText::parseFlushStamp(answer.first).ok;
  123  }
  124  
  125  bool OfflineAchievements::flushStampPresent()
  126  {
  127  	return available() && Utils::FileSystem::exists(FLUSH_STAMP, false);
  128  }
  129  
  130  CloudText::ScanStamp OfflineAchievements::lastScan()
  131  {
  132  	// Uncached: the ctl writes this while EmulationStation runs, and
  133  	// Utils::FileSystem::exists remembers a miss for the session otherwise
  134  	// (es-native-ui.md; the cloud rows read NOT DONE ON THIS DEVICE YET
  135  	// after a run had stamped, 2026-09-10).
  136  	if (!Utils::FileSystem::exists(SCAN_STAMP, false))
  137  		return CloudText::ScanStamp();
  138  	return CloudText::parseScanStamp(Utils::FileSystem::readAllText(SCAN_STAMP));
  139  }
  140  
  141  CloudText::RunningProgress OfflineAchievements::runningProgress()
  142  {
  143  	// Uncached, as the stamp is. The ctl writes the file whole (a temporary
  144  	// name, then a rename) and removes it as the run ends, so a read finds
  145  	// either a whole line or nothing -- and nothing, should the file go
  146  	// between the two calls here, parses as no run.
  147  	if (!Utils::FileSystem::exists(RUNNING_FILE, false))
  148  		return CloudText::RunningProgress();
  149  	return CloudText::parseRunningProgress(Utils::FileSystem::readAllText(RUNNING_FILE), (long long) time(nullptr));
  150  }
  151  
  152  std::vector<int> OfflineAchievements::readyIds()
  153  {
  154  	// Uncached, like the scan stamp: the client rewrites this file while
  155  	// EmulationStation runs.
  156  	if (!Utils::FileSystem::exists(READY_FILE, false))
  157  		return std::vector<int>();
  158  	// One game id per line (es_export.py). Lines that are not a number are
  159  	// not games: a count is never made of what was not read as one.
  160  	return OfflineAchievementsText::parseReadyIds(Utils::FileSystem::readAllText(READY_FILE));
  161  }
  162  
  163  int OfflineAchievements::readyCount()
  164  {
  165  	return (int)readyIds().size();
  166  }
  167  
  168  bool OfflineAchievements::toggleOn()
  169  {
  170  	return SystemConf::getInstance()->getBool("global.retroachievements.offlineproxy");
  171  }
  172  
  173  bool OfflineAchievements::proxyOffline()
  174  {
  175  	if (!available() || !toggleOn())
  176  		return false;
  177  	// The device's own link first (fork #190). The proxy's monitor rewrites
  178  	// its state only when its next probe fails, some time after the link
  179  	// drops, and a player who has just switched Wi-Fi off opens a page
  180  	// before that; asking the web then is a PLEASE WAIT with no route
  181  	// under it. No address on any wired or wireless interface (the same
  182  	// question the network watcher and the scan row ask; a VPN's tunnel
  183  	// does not count) is offline, whatever the file says.
  184  	if (Utils::Platform::queryIPAddress().empty())
  185  		return true;
  186  	// An address and no state file yet: the toggle has just gone on and the
  187  	// proxy's monitor has not probed. That reads as online, on purpose -- a
  188  	// player with a link who has just enabled the feature expects the page
  189  	// they had a minute ago, and the web request is bounded; reading it as
  190  	// offline would show an empty device copy for a store that has cached
  191  	// nothing yet (audit #258 PL-028 asked which; this is the trade).
  192  	if (!Utils::FileSystem::exists(ONLINE_STATE, false))
  193  		return false;
  194  	bool online = true;
  195  	if (!OfflineAchievementsText::parseOnlineState(Utils::FileSystem::readAllText(ONLINE_STATE), online))
  196  		return false;
  197  	return !online;
  198  }
  199  
  200  std::string OfflineAchievements::username()
  201  {
  202  	return SystemConf::getInstance()->get("global.retroachievements.username");
  203  }
  204  
  205  bool OfflineAchievements::askProxy(const std::string& query, std::string& body, std::string& error)
  206  {
  207  	body.clear();
  208  	error.clear();
  209  
  210  	HttpReqOptions options;
  211  	options.connectTimeout = PROXY_CONNECT_MS;
  212  	options.timeout = PROXY_TOTAL_MS;
  213  	// No cookie jar for a local process, and the interface's own name: the
  214  	// proxy remembers the last client's User-Agent but never uses it for
  215  	// its own requests (utils.py self_user_agent), so this changes nothing
  216  	// about how it speaks to RetroAchievements.
  217  	options.useCookieManager = false;
  218  	// The store and nothing else (fork #190): the fork's proxy answers a
  219  	// request carrying this from its store whatever it believes about the
  220  	// link. Without it, a proxy that still believes it is online -- up to its
  221  	// monitor's next probe after the link drops -- tries upstream first, with a
  222  	// fifteen-second timeout, for every one of these; the pages show the
  223  	// device's copy, which is exactly the store. The same line rides every
  224  	// image WebImageComponent asks of the proxy (fork #199).
  225  	options.customHeaders.push_back(Utils::OfflineProxy::StoreOnlyHeader);
  226  
  227  	HttpReq req(OfflineAchievementsText::requestUrl(query), &options);
  228  	if (req.wait())
  229  	{
  230  		body = req.getContent();
  231  		return true;
  232  	}
  233  	// For a 4xx or 503 HttpReq keeps the proxy's body as the message, so a
  234  	// miss reads as the proxy's own words and not as a status code.
  235  	error = req.getErrorMsg();
  236  	return false;
  237  }
  238  
  239  std::vector<OfflineAchievementsText::StoreGame> OfflineAchievements::storeSummary(bool& ok)
  240  {
  241  	std::vector<OfflineAchievementsText::StoreGame> games;
  242  	ok = false;
  243  	if (!available())
  244  		return games;
  245  	// One process over the store, one line a game -- in place of two
  246  	// requests a game to the proxy (fork #190). The ctl exits 1 with the
  247  	// toggle off, no account or no store, and says a store it could not
  248  	// read; either way the caller has no summary from the device.
  249  	std::vector<std::string> lines;
  250  	auto result = ApiSystem::executeScriptLegacy(std::string(CTL) + " summary 2>/dev/null",
  251  		[&lines](const std::string line) { lines.push_back(line); });
  252  	if (result.second != 0)
  253  		return games;
  254  	for (const auto& line : lines)
  255  	{
  256  		auto game = OfflineAchievementsText::parseStoreGame(line);
  257  		if (game.ok)
  258  			games.push_back(game);
  259  		else if (!line.empty())
  260  			LOG(LogWarning) << "OfflineAchievements: a line of the store's summary was not a game; skipped";
  261  	}
  262  	ok = true;
  263  	return games;
  264  }
  265  
  266  std::vector<OfflineAchievementsText::PendingAward> OfflineAchievements::pendingAwardIds()
  267  {
  268  	if (!available() || !toggleOn())
  269  		return std::vector<OfflineAchievementsText::PendingAward>();
  270  
  271  	// Every line, not the last: one award per line. Exit 0 with rows, 1 with
  272  	// none; anything else is the ctl saying it could not tell, and the page
  273  	// then marks nothing as waiting rather than guessing.
  274  	std::string all;
  275  	auto result = ApiSystem::executeScriptLegacy(std::string(CTL) + " pending-ids 2>/dev/null",
  276  		[&all](const std::string line) { all += line + "\n"; });
  277  	if (result.second != 0 && result.second != 1)
  278  		return std::vector<OfflineAchievementsText::PendingAward>();
  279  	return OfflineAchievementsText::parsePendingIds(all);
  280  }
  281  
  282  OfflineAchievementsText::AccountTotals OfflineAchievements::accountTotals()
  283  {
  284  	if (!available() || !toggleOn())
  285  		return OfflineAchievementsText::AccountTotals();
  286  	const auto answer = ask("account");
  287  	if (answer.second != 0)
  288  		return OfflineAchievementsText::AccountTotals();
  289  	return OfflineAchievementsText::parseAccountTotals(answer.first);
  290  }
  291  
  292  // The table is CloudText's, where it has a case (CloudText::scanWhy).
  293  std::string OfflineAchievements::scanWhy(const std::string& token)
  294  {
  295  	return CloudText::scanWhy(token);
  296  }
  297  
  298  void OfflineAchievements::topUpWhenOnline(Window* window)
  299  {
  300  	if (!available())
  301  		return;
  302  	// The toggle is read here as well as in the ctl so a device with the
  303  	// feature off never starts a process for it on every link.
  304  	if (!SystemConf::getInstance()->getBool("global.retroachievements.offlineproxy"))
  305  		return;
  306  	ProxyCards::topUp(window, false);
  307  }
  308  
  309  void OfflineAchievements::topUpAfterIndex(Window* window)
  310  {
  311  	if (!available() || !toggleOn())
  312  		return;
  313  	ProxyCards::topUp(window, true);
  314  }
  315  
  316  int OfflineAchievements::runTopUp(bool afterIndex)
  317  {
  318  	const auto answer = ask(afterIndex ? "topup --after-index" : "topup");
  319  	LOG(LogInfo) << "OfflineAchievements: topup" << (afterIndex ? " --after-index" : "") << " exited " << answer.second;
  320  	return answer.second;
  321  }
  322  
  323  int OfflineAchievements::markIndexOffline()
  324  {
  325  	const auto answer = ask("index-offline");
  326  	LOG(LogInfo) << "OfflineAchievements: index-offline exited " << answer.second;
  327  	return answer.second;
  328  }
  329  
  330  bool OfflineAchievements::stopRun()
  331  {
  332  	// The pid in the lock file names a run only while the lock is held, and
  333  	// only as the ctl (RunLock): a file a finished or killed run left names a
  334  	// pid that may belong to anything by now. And only a pid that holds the
  335  	// file open is the run (holdsOpen); while the lock is held by a run that
  336  	// has not yet written its pid, the file is asked again for half a
  337  	// second, then nothing is signalled and the launch waits for the run to
  338  	// end on its own (FileData's launchWhenGone).
  339  	for (int attempt = 0; ; attempt++)
  340  	{
  341  		const long pid = RunLock::holder(SCAN_LOCK, "raofflineproxy-ctl");
  342  		if (pid > 1 && holdsOpen(pid, SCAN_LOCK))
  343  			return ::kill((pid_t) pid, SIGTERM) == 0;
  344  		if (!RunLock::held(SCAN_LOCK))
  345  			return false;
  346  		if (attempt >= 10)
  347  		{
  348  			LOG(LogWarning) << "OfflineAchievements: the run lock is held, and the pid it names (" << pid << ") does not hold it; nothing was signalled";
  349  			return false;
  350  		}
  351  		std::this_thread::sleep_for(std::chrono::milliseconds(50));
  352  	}
  353  }
```


## es-app/src/OfflineScanJob.cpp @ 16dbac5211 (whole, 273 lines)

```text
    1  #include "OfflineScanJob.h"
    2  #include "AppWindow.h"
    3  #include "CloudText.h"
    4  
    5  #include "Window.h"
    6  #include "Log.h"
    7  #include "utils/StringUtil.h"
    8  
    9  #include <cctype>
   10  #include <cstdio>
   11  #include <thread>
   12  #include <signal.h>
   13  #include <sys/wait.h>
   14  
   15  std::mutex OfflineScanJob::sMutex;
   16  std::shared_ptr<OfflineScanJob> OfflineScanJob::sCurrent;
   17  
   18  OfflineScanJob::OfflineScanJob(Window* window, const std::string& command)
   19  	: mWindow(window), mCommand(command), mStarted(std::chrono::steady_clock::now())
   20  {
   21  }
   22  
   23  std::shared_ptr<OfflineScanJob> OfflineScanJob::current()
   24  {
   25  	std::unique_lock<std::mutex> lock(sMutex);
   26  	return sCurrent;
   27  }
   28  
   29  bool OfflineScanJob::running()
   30  {
   31  	auto job = current();
   32  	return job != nullptr && !job->state().finished;
   33  }
   34  
   35  std::shared_ptr<OfflineScanJob> OfflineScanJob::start(Window* window, const std::string& command)
   36  {
   37  	std::unique_lock<std::mutex> lock(sMutex);
   38  	if (sCurrent != nullptr && !sCurrent->state().finished)
   39  		return sCurrent;
   40  
   41  	std::shared_ptr<OfflineScanJob> job(new OfflineScanJob(window, command));
   42  	sCurrent = job;
   43  	// Detached, and holding its own reference: the run ends when the ctl
   44  	// does, not when a page closes -- the same shape as the top-up's thread
   45  	// (OfflineAchievements::topUpWhenOnline).
   46  	std::thread([job] { job->run(); }).detach();
   47  	return job;
   48  }
   49  
   50  OfflineScanJob::State OfflineScanJob::state() const
   51  {
   52  	std::unique_lock<std::mutex> lock(mMutex);
   53  	State s = mState;
   54  	if (!s.finished)
   55  		s.elapsedMs = (int) std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - mStarted).count();
   56  	return s;
   57  }
   58  
   59  void OfflineScanJob::setOnChanged(const std::function<void()>& onChanged)
   60  {
   61  	std::unique_lock<std::mutex> lock(mMutex);
   62  	mOnChanged = onChanged;
   63  }
   64  
   65  void OfflineScanJob::cancel()
   66  {
   67  	pid_t pid = 0;
   68  	{
   69  		std::unique_lock<std::mutex> lock(mMutex);
   70  		if (mState.finished || mState.cancelled)
   71  			return;
   72  		mState.cancelled = true;
   73  		pid = mPid;
   74  		if (pid <= 0)
   75  			mCancelWanted = true;   // the pid line has not arrived: handleLine delivers it
   76  	}
   77  	if (pid > 0)
   78  		::kill(-pid, SIGINT);
   79  	LOG(LogInfo) << "OfflineScanJob: cancelled by the player (SIGINT, group " << pid << ")";
   80  	changed();
   81  }
   82  
   83  // One refresh waiting on the interface thread at a time: a game in
   84  // progress pauses the interface's loop, and a thousand queued refreshes
   85  // running back to back when it returns would be a thousand for nothing.
   86  void OfflineScanJob::changed()
   87  {
   88  	std::function<void()> onChanged;
   89  	{
   90  		std::unique_lock<std::mutex> lock(mMutex);
   91  		if (mPostPending || !mOnChanged)
   92  			return;
   93  		mPostPending = true;
   94  		onChanged = mOnChanged;
   95  	}
   96  	// This run, not current(): a TRY AGAIN may have started the next one
   97  	// between the last line and here.
   98  	//
   99  	// Through AppWindow (#308 8-es claude F-ES-26's rule): this thread is
  100  	// detached and a scan runs for minutes, so its end can come after main()
  101  	// has let the window go. A refresh nobody can draw is dropped, and with
  102  	// it the pending mark, so nothing waits on a post that was not made.
  103  	std::shared_ptr<OfflineScanJob> self = shared_from_this();
  104  	const bool posted = AppWindow::post(mWindow, [self, onChanged]
  105  	{
  106  		{
  107  			std::unique_lock<std::mutex> lock(self->mMutex);
  108  			self->mPostPending = false;
  109  		}
  110  		onChanged();
  111  	});
  112  	if (!posted)
  113  	{
  114  		std::unique_lock<std::mutex> lock(mMutex);
  115  		mPostPending = false;
  116  	}
  117  }
  118  
  119  void OfflineScanJob::run()
  120  {
  121  	int ret = -1;
  122  	// Braces around the whole command: a trailing redirection binds to the
  123  	// last element of a sequence only (GuiCloudTransfer learnt it). SIGPIPE
  124  	// ignored inside them, and so in the ctl, which inherits the disposition:
  125  	// should this process end while the ctl is mid-scan, its ">>> " lines
  126  	// meet a closed pipe and fail without killing it, so the scan runs to
  127  	// its end and writes its stamp rather than dying at the next line.
  128  	//
  129  	// In a session of its own, saying so on its first line: setsid makes the
  130  	// shell a process group leader and ">>> pid N" tells cancel() which group
  131  	// to signal, so the shell, the ctl and its helper go together -- the
  132  	// shape CloudTransferJob gives its commands (D-CLOUD-129). shellQuote, so
  133  	// a command with a quote in it survives the trip.
  134  	const std::string wrapped = "setsid sh -c "
  135  		+ Utils::String::shellQuote("echo \">>> pid $$\"; { trap '' PIPE; " + mCommand + " ; }") + " 2>&1";
  136  	FILE* pipe = popen(wrapped.c_str(), "r");
  137  	if (pipe != nullptr)
  138  	{
  139  		std::string buf;
  140  		int c;
  141  		while ((c = fgetc(pipe)) != EOF)
  142  		{
  143  			if (c != '\n' && c != '\r')
  144  			{
  145  				if (buf.size() < 1024)
  146  					buf += (char) c;
  147  				continue;
  148  			}
  149  			handleLine(cleanLine(buf));
  150  			buf.clear();
  151  		}
  152  		if (!buf.empty())
  153  			handleLine(cleanLine(buf));
  154  
  155  		int status = pclose(pipe);
  156  		if (WIFEXITED(status))
  157  			ret = WEXITSTATUS(status);
  158  	}
  159  
  160  	{
  161  		std::unique_lock<std::mutex> lock(mMutex);
  162  		mState.exit = ret;
  163  		mState.elapsedMs = (int) std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - mStarted).count();
  164  		mState.finished = true;
  165  		LOG(LogInfo) << "OfflineScanJob: " << Utils::String::maskSecrets(mCommand) << " exited " << ret
  166  			<< " (cached " << mState.cached << ", skipped " << mState.skipped << ", ready " << mState.ready << ")";
  167  	}
  168  	changed();
  169  }
  170  
  171  // The ctl talks to the page through ">>> " lines (raofflineproxy-ctl's
  172  // header is the contract), after run()'s own first line:
  173  //   ">>> pid <n>"              the run's process group, from the shell run() starts
  174  //   ">>> doing listing"        the library is being walked
  175  //   ">>> total <n>"            how many ROMs will be looked at
  176  //   ">>> game <i>|<n>|<name>"  the one it is on now
  177  //   ">>> cached <c>|<s>"       added so far, and passed over so far
  178  //   ">>> note <TOKEN>"         LIMIT_REACHED, NOTHING_NEW, TRUNCATED, NO_GAMES
  179  //   ">>> errors <n>"           games a fetch failed for (audit #186 PL-24; the
  180  //                              ctl says it as the run ends, before why)
  181  //   ">>> why <TOKEN>"          why it stopped, in the ctl's token (CANCELLED
  182  //                              after cancel(): the ctl's INT trap says it)
  183  //   ">>> done <c>|<s>|<ready>|<limit>"
  184  // Everything else on stdout is the client's own and is not shown. TRUNCATED
  185  // is read should the ctl ever say it; at ad25fdeb22 it logs the fact and
  186  // tells the page nothing.
  187  void OfflineScanJob::handleLine(const std::string& line)
  188  {
  189  	if (line.rfind(">>> ", 0) != 0)
  190  		return;
  191  	const std::string body = line.substr(4);
  192  	const size_t space = body.find(' ');
  193  	const std::string word = body.substr(0, space);
  194  	const std::string rest = space == std::string::npos ? "" : Utils::String::trim(body.substr(space + 1));
  195  	const std::vector<std::string> fields = Utils::String::split(rest, '|', false);
  196  	auto num = [](const std::string& s) -> int
  197  	{
  198  		const std::string t = Utils::String::trim(s);
  199  		if (t.empty() || t.size() > 9)
  200  			return 0;
  201  		for (char c : t)
  202  			if (c < '0' || c > '9')
  203  				return 0;
  204  		return std::stoi(t);
  205  	};
  206  
  207  	{
  208  		std::unique_lock<std::mutex> lock(mMutex);
  209  		if (word == "pid")
  210  		{
  211  			// run()'s own first line: the group cancel() signals. A cancel
  212  			// that came first is delivered now.
  213  			mPid = num(rest);
  214  			if (mCancelWanted && mPid > 0)
  215  			{
  216  				mCancelWanted = false;
  217  				::kill(-mPid, SIGINT);
  218  			}
  219  			return;
  220  		}
  221  		if (word == "doing")
  222  			mState.listing = rest == "listing";
  223  		else if (word == "total")
  224  			mState.total = num(rest);
  225  		else if (word == "game" && fields.size() >= 3)
  226  		{
  227  			mState.listing = false;
  228  			mState.index = num(fields[0]);
  229  			mState.total = num(fields[1]);
  230  			// The name may itself contain '|', so everything past the second is it.
  231  			std::string name = fields[2];
  232  			for (size_t i = 3; i < fields.size(); i++)
  233  				name += "|" + fields[i];
  234  			mState.game = name;
  235  		}
  236  		else if (word == "cached" && fields.size() >= 2)
  237  		{
  238  			mState.cached = num(fields[0]);
  239  			mState.skipped = num(fields[1]);
  240  		}
  241  		else if (word == "note")
  242  		{
  243  			if (rest == "LIMIT_REACHED") mState.limit = true;
  244  			else if (rest == "NOTHING_NEW") mState.nothingNew = true;
  245  			else if (rest == "TRUNCATED") mState.truncated = true;
  246  			else if (rest == "NO_GAMES") mState.noGames = true;
  247  		}
  248  		else if (word == "errors")
  249  			mState.errors = num(rest);
  250  		else if (word == "why")
  251  			mState.why = rest;
  252  		else if (word == "done" && fields.size() >= 4)
  253  		{
  254  			mState.cached = num(fields[0]);
  255  			mState.skipped = num(fields[1]);
  256  			mState.ready = num(fields[2]);
  257  			mState.limit = num(fields[3]) != 0;
  258  		}
  259  		else
  260  			return;
  261  	}
  262  	changed();
  263  }
  264  
  265  // One line of a script's output: ANSI escapes, C0 controls and DEL dropped,
  266  // every UTF-8 byte kept, then trimmed -- CloudText::cleanLine, the rule the
  267  // sync card reads by since #308 F-CS-19. This page carried a copy of its
  268  // own; the two gave the same line for every input, and one copy is one
  269  // rule to change.
  270  std::string OfflineScanJob::cleanLine(const std::string& raw)
  271  {
  272  	return CloudText::cleanLine(raw);
  273  }
```


## es-app/src/guis/GuiOfflineScan.cpp @ 16dbac5211 (whole, 382 lines)

```text
    1  #include "guis/GuiOfflineScan.h"
    2  #include "TextFit.h"
    3  
    4  #include "CloudExit.h"
    5  #include "guis/GuiMsgBox.h"
    6  #include "CloudText.h"
    7  #include "OfflineAchievements.h"
    8  #include "Window.h"
    9  #include "ThemeData.h"
   10  #include "LocaleES.h"
   11  #include "utils/StringUtil.h"
   12  #include "Log.h"
   13  
   14  #include <cstdio>
   15  
   16  GuiOfflineScan::GuiOfflineScan(Window* window, const std::string& command, const std::function<void()>& onChanged)
   17  	: GuiComponent(window), mBusyAnim(window, ""), mBackground(window, ":/frame.png"),
   18  	  mCommand(command), mOnChanged(onChanged), mShownFinished(false)
   19  {
   20  	auto theme = ThemeData::getMenuTheme();
   21  	mBackground.setImagePath(theme->Background.path);
   22  	mBackground.setEdgeColor(theme->Background.color);
   23  	mBackground.setCenterColor(theme->Background.centerColor);
   24  	mBackground.setCornerSize(theme->Background.cornerSize);
   25  
   26  	const float SW = Renderer::getScreenWidth();
   27  	const float SH = Renderer::getScreenHeight();
   28  	setSize(SW, SH);
   29  
   30  	mTextFont  = theme->Text.font;
   31  	mSmallFont = theme->TextSmall.font;
   32  	mTitle    = std::make_shared<TextComponent>(window, _("SCANNING GAMES FOR OFFLINE ACHIEVEMENTS"), theme->Title.font, theme->Title.color, ALIGN_CENTER);
   33  	mStatus   = std::make_shared<TextComponent>(window, _("PREPARING..."), mTextFont,  theme->Text.color,      ALIGN_CENTER);
   34  	mCounter  = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   35  	mActivity = std::make_shared<TextComponent>(window, "",                mTextFont,  theme->Text.color,      ALIGN_CENTER);
   36  	mDetail   = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   37  	mNote     = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   38  	mElapsed  = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   39  	mFooter   = std::make_shared<TextComponent>(window, "",                mSmallFont, theme->TextSmall.color, ALIGN_CENTER);
   40  
   41  	// One column, 0.78 of the width, every line fitted to it, and the rows
   42  	// stacked from the fonts' own heights -- GuiCloudTransfer's geometry,
   43  	// so the two long-job pages of this app sit the same way on every panel
   44  	// (its constructor carries the derivation and the numbers per panel).
   45  	const float w  = SW * 0.78f;
   46  	const float cx = SW * 0.5f;
   47  	const float x  = cx - w / 2.0f;
   48  	mLineWidth = w;
   49  	for (auto& t : { mTitle, mStatus, mCounter, mActivity, mDetail, mNote, mElapsed, mFooter })
   50  		t->setSize(w, 0);
   51  
   52  	const float hT = theme->Title.font->getHeight();
   53  	const float hM = mTextFont->getHeight();
   54  	const float hS = mSmallFont->getHeight();
   55  	const float natural = 2 * SH * 0.05f + hT + 3 * hM + 4 * hS + 5.5f * SH * 0.02f;
   56  	const float fit = natural > SH * 0.9f ? (SH * 0.9f) / natural : 1.0f;
   57  	const float pad = SH * 0.05f * fit;
   58  	const float gap = SH * 0.02f * fit;
   59  	const float rT = hT * fit, rM = hM * fit, rS = hS * fit;
   60  	const float H = 2 * pad + rT + 3 * rM + 4 * rS + 5.5f * gap;
   61  	const float top = (SH - H) / 2.0f;
   62  
   63  	float y = top + pad;
   64  	mTitle   ->setPosition(x, y);
   65  	y += rT + 1.5f * gap;
   66  	mStatus  ->setPosition(x, y);
   67  	mCounter ->setPosition(x, y + rM);
   68  	y += rM + rS + gap;
   69  	mActivity->setPosition(x, y);
   70  	mDetail  ->setPosition(x, y + rM);
   71  	y += rM + rS + 0.5f * gap;
   72  	// 5. The spinner while it runs, the note once done, one row. No caption
   73  	// on the spinner: line 1 says what is happening, and BusyComponent's
   74  	// setText("") is a no-op against its empty start (es-code-traps.md).
   75  	mBusyAnim.setBackgroundVisible(false);
   76  	mBusyAnim.setSize(w, rM);
   77  	mBusyAnim.setPosition(x, y);
   78  	mNote    ->setPosition(x, y + (rM - hS) / 2.0f);
   79  	y += rM + 1.5f * gap;
   80  	mElapsed ->setPosition(x, y);
   81  	y += rS + gap;
   82  	mFooter  ->setPosition(x, y);
   83  
   84  	mPanelSize = Vector2f(w + SW * 0.06f, H);
   85  	mPanelPos  = Vector2f(cx - mPanelSize.x() / 2.0f, top);
   86  	mBackground.fitTo(mPanelSize, Vector3f(mPanelPos.x(), mPanelPos.y(), 0), Vector2f(-32, -32));
   87  
   88  	// The run in flight, when there is one, else a new one. Either way the
   89  	// row follows it from here.
   90  	mJob = OfflineScanJob::start(window, mCommand);
   91  	mJob->setOnChanged(mOnChanged);
   92  }
   93  
   94  // Nothing to join: the run is the job's (OfflineScanJob). The page is sat
   95  // in since D-UI-078 -- CANCEL ends the run before the page goes -- so the
   96  // job outliving the page is the seam's guard, not the design.
   97  GuiOfflineScan::~GuiOfflineScan()
   98  {
   99  }
  100  
  101  // While the scan runs, back asks whether to cancel it (D-UI-078: the page is
  102  // sat in, and CANCEL is the one way out); every other press is refused,
  103  // since there is nothing to choose and a stray press should not dismiss a
  104  // page somebody is waiting on. Once it has finished, any button dismisses
  105  // it, and when the run did not complete, OK runs it again from here: the
  106  // surface that reported the failure carries the retry (D-UI-028). OK and
  107  // back are the player's mapping, which may be swapped; the literal "a" the
  108  // retry was bound to was back's own button then (#308 1-raoffline claude
  109  // F-RA-14, gpt F-RA-22).
  110  bool GuiOfflineScan::input(InputConfig* config, Input input)
  111  {
  112  	if (!input.value)
  113  		return true;
  114  	const OfflineScanJob::State s = mJob->state();
  115  	if (!s.finished)
  116  	{
  117  		if (config->isMappedTo(BUTTON_BACK, input))
  118  			askCancel();
  119  		return true;
  120  	}
  121  	const Outcome o = outcome(s);
  122  	if (!o.completed && config->isMappedTo(BUTTON_OK, input))
  123  	{
  124  		// A new run; the finished one is let go. The page shows the run
  125  		// from its first line again.
  126  		mJob = OfflineScanJob::start(mWindow, mCommand);
  127  		mJob->setOnChanged(mOnChanged);
  128  		mShownFinished = false;
  129  		mStatus->setText(_("PREPARING..."));
  130  		for (auto& t : { mCounter, mActivity, mDetail, mNote })
  131  			t->setText("");
  132  		updateHelpPrompts();
  133  		return true;
  134  	}
  135  	close();
  136  	return true;
  137  }
  138  
  139  // What cancelling means, read at the moment of deciding (D-UI-023): the
  140  // games already saved stay saved, and a scan passes over games already
  141  // cached, so the next one carries on from here. YES first, NO last so B
  142  // answers NO. The run is captured, not the page: the page outlives the
  143  // dialog either way, but nothing here needs it.
  144  void GuiOfflineScan::askCancel()
  145  {
  146  	std::shared_ptr<OfflineScanJob> job = mJob;
  147  	mWindow->pushGui(new GuiMsgBox(mWindow,
  148  		_("CANCEL THE SCAN?") + std::string("\n\n")
  149  			+ _("GAMES ALREADY SAVED STAY SAVED. THE NEXT SCAN CARRIES ON FROM THERE."),
  150  		_("YES"), [job] { job->cancel(); },
  151  		_("NO"), nullptr));
  152  }
  153  
  154  void GuiOfflineScan::close()
  155  {
  156  	// Copied out first: the page is gone by the time it runs.
  157  	std::function<void()> onChanged = mOnChanged;
  158  	delete this;
  159  	if (onChanged)
  160  		onChanged();
  161  }
  162  
  163  std::vector<HelpPrompt> GuiOfflineScan::getHelpPrompts()
  164  {
  165  	std::vector<HelpPrompt> prompts;
  166  	const OfflineScanJob::State s = mJob->state();
  167  	if (!s.finished)
  168  	{
  169  		prompts.push_back(HelpPrompt(BUTTON_BACK, _("CANCEL")));
  170  		return prompts;
  171  	}
  172  	const Outcome o = outcome(s);
  173  	if (!o.completed)
  174  		prompts.push_back(HelpPrompt(BUTTON_OK, _("TRY AGAIN")));
  175  	prompts.push_back(HelpPrompt(BUTTON_BACK, _("CLOSE")));
  176  	return prompts;
  177  }
  178  
  179  // The word for the run (D-UI-028): COMPLETED, SKIPPED for the two sentinels
  180  // the ctl exits with before touching anything -- not online, another scan
  181  // or top-up holding the lock -- and for the player's own cancel (the word
  182  // the transfer page gives a run stopped for a game, D-CLOUD-129: nothing
  183  // went wrong, and the next run carries on), and COULDN'T FINISH for
  184  // everything else, the refusals included: the why on line 4 says which.
  185  GuiOfflineScan::Outcome GuiOfflineScan::outcome(const OfflineScanJob::State& s)
  186  {
  187  	Outcome o;
  188  	o.completed = !s.cancelled && s.exit == 0;
  189  	o.skipped = s.cancelled || s.exit == CloudExit::NoNetwork || s.exit == CloudExit::LockHeld;
  190  	if (s.cancelled)
  191  		o.word = _("SKIPPED - YOU CANCELLED IT");
  192  	else if (o.completed)
  193  		o.word = _("COMPLETED");
  194  	else if (s.exit == CloudExit::NoNetwork)
  195  		o.word = _("SKIPPED - YOU'RE NOT ONLINE");
  196  	else if (s.exit == CloudExit::LockHeld)
  197  		o.word = _("SKIPPED - A SCAN IS ALREADY RUNNING");
  198  	else
  199  		o.word = _("COULDN'T FINISH");
  200  	return o;
  201  }
  202  
  203  void GuiOfflineScan::render(const Transform4x4f& parentTrans)
  204  {
  205  	Transform4x4f trans = parentTrans * getTransform();
  206  	Renderer::setMatrix(trans);
  207  	// Dim the whole screen: this is a takeover, and the carousel showing
  208  	// through would say the app is idle while a scan is in flight.
  209  	Renderer::drawRect(0.f, 0.f, mSize.x(), mSize.y(), 0x000000D0);
  210  
  211  	mBackground.render(trans);
  212  
  213  	for (auto& t : { mTitle, mStatus, mCounter, mActivity, mDetail, mNote, mElapsed, mFooter })
  214  		t->render(trans);
  215  
  216  	// A spinner and never a bar: the client reports each game as it
  217  	// finishes it and nothing in between, and hashing a disc image can take
  218  	// as long as ten cartridges, so a bar at i/n would be an invented
  219  	// position (es-native-ui.md: a bar only where a real percentage exists).
  220  	if (!mShownFinished)
  221  		mBusyAnim.render(trans);
  222  
  223  	// The keys are the help bar's, drawn here: with full-screen menus on
  224  	// (every handheld) Window draws no help while a second page is open, so
  225  	// the footer spelled them out as A and B -- the wrong buttons on a
  226  	// swapped mapping (es-ui-style-guide.md, Interaction rules; the save
  227  	// state manager draws its bar the same way).
  228  	if (mWindow->peekGui() == this && Renderer::ScreenSettings::fullScreenMenus())
  229  		mWindow->renderHelpPromptsEarly(parentTrans);
  230  }
  231  
  232  // Clip to one line: a long game name gets an ellipsis, never a second line.
  233  std::string GuiOfflineScan::fitOneLine(const std::shared_ptr<Font>& font, std::string text, float width)
  234  {
  235  	if (!font)
  236  		return text;
  237  	// On characters, not bytes (TextFit; #308 gpt F-RA-23).
  238  	return TextFit::fitOneLine(text, width, [&font](const std::string& t) { return font->sizeText(t).x(); });
  239  }
  240  
  241  // "N GAMES READY FOR OFFLINE PLAY": the one sentence the row under SCAN
  242  // GAMES and this page's line 3 both end on, so they never disagree.
  243  std::string GuiOfflineScan::readyPhrase(int ready)
  244  {
  245  	if (ready <= 0)
  246  		return _("NO GAMES READY FOR OFFLINE PLAY YET");
  247  	if (ready == 1)
  248  		return std::string("1 ") + _("GAME READY FOR OFFLINE PLAY");
  249  	return std::to_string(ready) + " " + std::string(_("GAMES READY FOR OFFLINE PLAY"));
  250  }
  251  
  252  // "GAMES WITH ACHIEVEMENTS ADDED: 3" -- what this run did, and "NOT SAVED: 1"
  253  // beside it when a fetch failed for any game (the ctl's errors count, audit
  254  // #186 PL-24: such a run is COULDN'T FINISH, and the next scan tries those
  255  // games again). The games without a set are not counted here: the
  256  // maintainer, on the RG SP with RC-5 (2026-09-14), "I'm not that concerned
  257  // about the games that don't have achievements [...] I just want to know
  258  // that it's scanning through the games with achievements." That count still
  259  // travels in the stamp for the log (skipped), unused here.
  260  std::string GuiOfflineScan::countsLine(int cached, int skipped, int errors)
  261  {
  262  	(void) skipped;
  263  	std::string line = std::string(_("GAMES WITH ACHIEVEMENTS ADDED:")) + " " + std::to_string(cached);
  264  	if (errors > 0)
  265  		line += "  ·  " + std::string(_("NOT SAVED:")) + " " + std::to_string(errors);
  266  	return line;
  267  }
  268  
  269  void GuiOfflineScan::update(int deltaTime)
  270  {
  271  	GuiComponent::update(deltaTime);
  272  	mBusyAnim.update(deltaTime);
  273  	const OfflineScanJob::State s = mJob->state();
  274  	if (s.finished && !mShownFinished)
  275  	{
  276  		mShownFinished = true;
  277  		// The help bar changes with the page: TRY AGAIN and CLOSE now.
  278  		updateHelpPrompts();
  279  	}
  280  	const int mins = s.elapsedMs / 60000;
  281  	const int secs = (s.elapsedMs / 1000) % 60;
  282  	char elapsed[32];
  283  	snprintf(elapsed, sizeof(elapsed), "%d:%02d", mins, secs);
  284  
  285  	if (s.finished)
  286  	{
  287  		// The same seven rows, now carrying the outcome (D-UI-028): 1 the
  288  		// word; 2 what this run added and passed over; 3 how many games
  289  		// earn offline now -- the answer the page exists to give; 4 why it
  290  		// stopped, when it did; 5 what to do next; 6 elapsed; 7 the buttons.
  291  		const Outcome o = outcome(s);
  292  		mStatus->setText(fitOneLine(mTextFont, o.word, mLineWidth));
  293  
  294  		const bool ran = s.total > 0 || s.cached > 0 || s.skipped > 0 || s.nothingNew;
  295  		mCounter->setText(ran && !s.nothingNew ? fitOneLine(mSmallFont, countsLine(s.cached, s.skipped, s.errors), mLineWidth) : "");
  296  
  297  		// The ctl's done line carries the count; a run that ended before it
  298  		// said one reads the client's export directly.
  299  		const int ready = s.ready >= 0 ? s.ready : OfflineAchievements::readyCount();
  300  		// A scan with no game to look at completed (fork #329): line 3 says
  301  		// so while the store is empty too, and line 4 says what to do next;
  302  		// with games still ready from before, line 3 keeps its count and
  303  		// line 4 carries both sentences.
  304  		mActivity->setText(fitOneLine(mTextFont, s.noGames && ready <= 0 ? _("NO GAMES TO SCAN YET") : readyPhrase(ready), mLineWidth));
  305  
  306  		std::string detail;
  307  		if (o.completed && s.noGames)
  308  			detail = ready <= 0 ? _("ADD GAMES, THEN SCAN AGAIN.")
  309  				: _("NO GAMES TO SCAN YET") + std::string(". ") + _("ADD GAMES, THEN SCAN AGAIN.");
  310  		else if (!o.completed && !o.skipped && !s.why.empty())
  311  		{
  312  			// The why whole, else its first sentence: a trailing instruction
  313  			// is the part that can go (D-UI-035), never a word cut short.
  314  			// SOME ACHIEVEMENT IMAGES COULDN'T BE SAVED. TRY THE SCAN AGAIN.
  315  			// is 516 px of the theme's bold at 15 px against this line's 499
  316  			// at 640x480, and the French of SOME GAMES... 521.
  317  			const std::string why = OfflineAchievements::scanWhy(s.why);
  318  			std::vector<std::string> forms = { why };
  319  			const std::string first = CloudText::shortenWhy(why);
  320  			if (!first.empty())
  321  				forms.push_back(first);
  322  			const auto font = mSmallFont;
  323  			detail = CloudText::chooseThatFits(forms, mLineWidth, [font](const std::string& t) { return font->sizeText(t).x(); });
  324  		}
  325  		else if (!o.completed && !o.skipped)
  326  			detail = _("SOMETHING WENT WRONG");
  327  		mDetail->setText(fitOneLine(mSmallFont, detail, mLineWidth));
  328  
  329  		// The client's cap on cached games is out of reach on ROCKNIX (patch
  330  		// 004, D-RA-014), but the ctl still forwards the client's word when it
  331  		// says it, so the branch stays -- with a sentence that names no
  332  		// number, since the number is not this product's to promise
  333  		// (audit #186 PL-15).
  334  		std::string note;
  335  		if (s.limit)
  336  			note = _("THAT'S AS MANY GAMES AS CAN BE SAVED FOR OFFLINE PLAY.");
  337  		else if (s.truncated)
  338  			// The walk stopped at the client's cap of files per run (#186
  339  			// PL-17): the games past it are the next run's.
  340  			note = _("NOT EVERY FOLDER WAS LOOKED AT. SCAN AGAIN TO CONTINUE.");
  341  		else if (s.nothingNew)
  342  			note = _("NOTHING NEW - EVERY GAME WAS ALREADY READY.");
  343  		else if (s.cancelled)
  344  			note = _("THE NEXT SCAN CARRIES ON FROM HERE.");
  345  		else if (s.exit == CloudExit::NoNetwork)
  346  			note = _("TRY AGAIN WHEN YOU'RE ONLINE.");
  347  		mNote->setText(fitOneLine(mSmallFont, note, mLineWidth));
  348  
  349  		mElapsed->setText(std::string(_("ELAPSED")) + " " + elapsed);
  350  		// A run that did not complete: TRY AGAIN and CLOSE are the help bar's,
  351  		// on the player's own buttons.
  352  		mFooter ->setText(!o.completed ? std::string() : _("PRESS ANY BUTTON TO CLOSE"));
  353  	}
  354  	else
  355  	{
  356  		// 1 what it is doing; 2 GAME i OF n; 3 the game it is on -- the line
  357  		// that says it is alive, because a disc image can take a while and
  358  		// a frozen count is indistinguishable from a hang; 4 the counts.
  359  		if (s.index > 0)
  360  			mStatus->setText(_("SCANNING..."));
  361  		else if (s.listing)
  362  			mStatus->setText(_("LOOKING THROUGH YOUR GAMES..."));
  363  		else
  364  			mStatus->setText(_("PREPARING..."));
  365  
  366  		std::string counter;
  367  		if (s.index > 0)
  368  		{
  369  			counter = std::string(_("GAME")) + " " + std::to_string(s.index);
  370  			if (s.total > 0)
  371  				counter += " " + std::string(_("OF")) + " " + std::to_string(s.total);
  372  		}
  373  		mCounter ->setText(counter);
  374  		mActivity->setText(fitOneLine(mTextFont, s.game, mLineWidth));
  375  		mDetail  ->setText(s.index > 0 ? fitOneLine(mSmallFont, countsLine(s.cached, s.skipped, s.errors), mLineWidth) : "");
  376  		mNote    ->setText("");
  377  		mElapsed ->setText(std::string(_("ELAPSED")) + " " + elapsed);
  378  		// 7. That it takes a while; how to cancel is the help bar's, on the
  379  		// player's own back button.
  380  		mFooter  ->setText(fitOneLine(mSmallFont, _("THIS CAN TAKE A WHILE."), mLineWidth));
  381  	}
  382  }
```


## es-app/src/ThreadedHasher.cpp @ 16dbac5211 (whole, 415 lines)

```text
    1  #include "ThreadedHasher.h"
    2  #include "Window.h"
    3  #include "FileData.h"
    4  #include "components/AsyncNotificationComponent.h"
    5  #include "guis/GuiMsgBox.h"
    6  #include "Gamelist.h"
    7  #include "RetroAchievements.h"
    8  #include "SystemConf.h"
    9  #include "SystemData.h"
   10  #include "FileData.h"
   11  #include "ApiSystem.h"
   12  #include "OfflineAchievements.h"
   13  #include "ProxyCards.h"
   14  #include "CheevosIndex.h"
   15  #include "GameCubeRvzHashRetry.h"
   16  #include "PlatformId.h"
   17  #include <libcheevos/cheevos.h>
   18  #include "utils/StringUtil.h"
   19  #include "Log.h"
   20  #include "Settings.h"
   21  #include <ctime>
   22  #include <unordered_set>
   23  #include <queue>
   24  
   25  #include "LocaleES.h"
   26  
   27  #define ICONINDEX _U("\uF002 ")
   28  
   29  ThreadedHasher* ThreadedHasher::mInstance = nullptr;
   30  bool ThreadedHasher::mPaused = false;
   31  bool ThreadedHasher::sCheevosLibraryCame = false;
   32  
   33  static std::mutex mLoaderLock;
   34  
   35  static bool retryGameCubeRvzHash(FileData* game)
   36  {
   37      if (!gameCubeRvzHashEnabled() || game->getSystem() == nullptr)
   38          return false;
   39      const auto& platforms = game->getSystem()->getPlatformIds();
   40      // A mixed-platform system can select another console in getCheevosHash.
   41      // Keep the repair confined to the unambiguous GameCube mapping.
   42      const bool gameCubeOnly = platforms.size() == 1 &&
   43          platforms.count(PlatformIds::NINTENDO_GAMECUBE) != 0;
   44      return GameCubeRvzHashRetry::needed(true, gameCubeOnly,
   45          Utils::FileSystem::getExtension(game->getPath()),
   46          game->getMetadata(MetaDataId::CheevosHash), game->getMetadata(MetaDataId::CheevosId));
   47  }
   48  
   49  ThreadedHasher::ThreadedHasher(Window* window, HasherType type, std::queue<FileData*> searchQueue, const std::vector<FileData*>& lookupOnly, bool forceAllGames)
   50  	: mWindow(window), mWndNotification(nullptr)
   51  {
   52  	mForce = forceAllGames;
   53  	mExit = false;
   54  	mType = type;
   55  	mCheevosIndexed = false;
   56  	mThreadCount = 0;
   57  
   58  	mSearchQueue = searchQueue;
   59  	mTotal = mSearchQueue.size();
   60  
   61  	if ((mType & HASH_CHEEVOS_MD5) == HASH_CHEEVOS_MD5)
   62  	{
   63  		try
   64  		{
   65  			mCheevosHashes = RetroAchievements::getCheevosHashes();
   66  			if (mCheevosHashes.size() == 0)
   67  			{
   68  				// Offline, or not yet: nothing can be identified without it. Said
   69  				// once, so a boot that indexed nothing can be told apart from one
   70  				// that never tried (fork #183); the link-up run tries again.
   71  				LOG(LogWarning) << "ThreadedHasher: RetroAchievements' hash library did not come; nothing is indexed this run";
   72  				// The games that waited for it are said to be waiting (fork
   73  				// #299, D-UI-104): the toast, and the control script's marker
   74  				// so the link's return looks them up.
   75  				if (!mSearchQueue.empty())
   76  					ProxyCards::indexRanOffline(mWindow, (int) mSearchQueue.size());
   77  				while (!mSearchQueue.empty())
   78  					mSearchQueue.pop();
   79  				// And nothing is counted: mTotal was taken from the queue
   80  				// above, so it stayed at the games that were waiting. A card
   81  				// and threads were made for an empty queue, the destructor
   82  				// toasted INDEXING COMPLETED beside the offline card, and the
   83  				// threads -- ending at once -- could delete this before
   84  				// start() read it back (#308 1-raoffline claude F-RA-05).
   85  				// With 0, the check below returns before any of that.
   86  				mTotal = 0;
   87  			}
   88  			else
   89  				sCheevosLibraryCame = true;
   90  
   91  			// The games with a hash and no id (audit #186 PL-08): the ones
   92  			// the library knows join the queue for a lookup and a save, and
   93  			// nothing else -- their ROM is never read again. RC-5 left every
   94  			// game indexed in a session that ended with a reboot in this
   95  			// state (fork #183): the hash in its recovery file, the id
   96  			// decided afterwards in memory and lost. The ones the library
   97  			// does not know stay as they are, so a library of games without
   98  			// a set costs no card and no toast at every startup.
   99  			for (FileData* game : lookupOnly)
  100  			{
  101  				const std::string hash = Utils::String::toUpper(game->getMetadata(MetaDataId::CheevosHash));
  102  				if (mCheevosHashes.find(hash) == mCheevosHashes.cend())
  103  					continue;
  104  				mSearchQueue.push(game);
  105  				mLookupOnly.insert(game);
  106  				mTotal++;
  107  			}
  108  			mCheevosIndexed = !mCheevosHashes.empty() && !mSearchQueue.empty();
  109  		}
  110  		catch (const std::exception& e)
  111  		{
  112  			// The fetch failed outright -- offline, nearly always -- with the
  113  			// same games waiting: the same word to the player (fork #299).
  114  			if (!mSearchQueue.empty())
  115  				ProxyCards::indexRanOffline(mWindow, (int) mSearchQueue.size());
  116  			mType = (HasherType)0;
  117  			throw e;
  118  		}
  119  	}
  120  
  121  	// A run with nothing to do -- lookups alone, and the library knew none
  122  	// of them -- shows no card and starts no thread; start() deletes it.
  123  	if (mTotal == 0)
  124  		return;
  125  
  126  	mWndNotification = mWindow->createAsyncNotificationComponent();
  127  
  128  	if (mType == HASH_CHEEVOS_MD5)
  129  		mWndNotification->updateTitle(ICONINDEX + _("SEARCHING RETROACHIEVEMENTS"));
  130  	else 
  131  		mWndNotification->updateTitle(ICONINDEX + _("SEARCHING NETPLAY GAMES"));
  132  
  133  	int num_threads = std::thread::hardware_concurrency() / 2;
  134  	if (num_threads == 0)
  135  		num_threads = 1;
  136  
  137  	mThreadCount = num_threads;
  138  	for (size_t i = 0; i < num_threads; i++)
  139  		mThreads.push_back(new std::thread(&ThreadedHasher::run, this));
  140  }
  141  
  142  ThreadedHasher::~ThreadedHasher()
  143  {
  144  	if ((mType & HASH_CHEEVOS_MD5) == HASH_CHEEVOS_MD5 && mTotal > 0)
  145  	{
  146  		mWindow->displayNotificationMessage(ICONINDEX + _("INDEXING COMPLETED") + std::string(". ") + _("UPDATE GAMELISTS TO APPLY CHANGES."));
  147  
  148  		// The offline cache follows this index (fork #184, D-RA-013): once
  149  		// the games are identified, and while the device is still connected
  150  		// (the hash library just came from RetroAchievements), the games not
  151  		// yet cached for offline play are cached from the ids and hashes
  152  		// written above -- raofflineproxy-ctl topup --after-index, from a
  153  		// thread of its own, with a card once it has work (fork #293). Not
  154  		// after a run the player stopped, and not after one that identified
  155  		// nothing.
  156  		if (!mExit && mCheevosIndexed)
  157  			OfflineAchievements::topUpAfterIndex(mWindow);
  158  	}
  159  
  160  	if (mWndNotification != nullptr)
  161  		mWndNotification->close();
  162  	mWndNotification = nullptr;
  163  
  164  	ThreadedHasher::mInstance = nullptr;
  165  }
  166  
  167  std::string ThreadedHasher::formatGameName(FileData* game)
  168  {
  169  	return "[" + game->getSystemName() + "] " + game->getName();
  170  }
  171  
  172  void ThreadedHasher::updateUI(const std::string label)
  173  {
  174  	std::string idx = std::to_string(mTotal + 1 - mSearchQueue.size()) + "/" + std::to_string(mTotal);
  175  	int percent = 100 - (mSearchQueue.size() * 100 / mTotal);
  176  		
  177  	mWndNotification->updateText(label);
  178  	mWndNotification->updatePercent(percent);	
  179  }
  180  
  181  void ThreadedHasher::run()
  182  {
  183  	std::unique_lock<std::mutex> lock(mLoaderLock);
  184  
  185  	bool cheevos = ((mType & HASH_CHEEVOS_MD5) == HASH_CHEEVOS_MD5);
  186  	bool netplay = ((mType & HASH_NETPLAY_CRC) == HASH_NETPLAY_CRC);
  187  
  188  	while (!mExit && !mSearchQueue.empty())
  189  	{
  190  		FileData* game = mSearchQueue.front();
  191  
  192  		auto label = formatGameName(game);
  193  
  194  		LOG(LogDebug) << "Hashing " << formatGameName(game);
  195  		updateUI(label);
  196  
  197  		mSearchQueue.pop();
  198  
  199  		lock.unlock();
  200  
  201  		if (mPaused)
  202  		{
  203  			while (!mExit && mPaused)
  204  			{
  205  				std::this_thread::yield();
  206  				std::this_thread::sleep_for(std::chrono::milliseconds(500));
  207  			}
  208  		}		
  209  
  210  		// A game here for a lookup alone is not read: not its CRC, not its
  211  		// hash (checkCheevosHash returns on the hash it has; checkCrc32 would
  212  		// not, in a system netplay never asked for).
  213  		const bool lookupOnly = mLookupOnly.count(game) > 0;
  214  
  215  		if (netplay && !lookupOnly)
  216  		{
  217  			LOG(LogDebug) << "CheckCrc32 : " << label;
  218  			game->checkCrc32(mForce);
  219  		}
  220  
  221  		if (cheevos)
  222  		{
  223  			LOG(LogDebug) << "CheckCheevosHash : " << label;
  224  			if (!lookupOnly)
  225  				// Queue eligibility alone is insufficient: FileData skips every
  226  				// stored hash unless forced. Force only this failed RVZ entry.
  227  				game->checkCheevosHash(mForce || retryGameCubeRvzHash(game));
  228  
  229  			auto hash = Utils::String::toUpper(game->getMetadata(MetaDataId::CheevosHash));
  230  			if (!hash.empty())
  231  			{
  232  				// The id reaches the disk with the hash. checkCheevosHash
  233  				// saved the game to the recovery folder with the hash and no
  234  				// id, because the id is decided here, afterwards, and until
  235  				// now it lived in memory until the gamelist was written at
  236  				// exit. The offline cache's scan reads that folder for the
  237  				// index (fork #184, D-RA-013), so a changed id is saved the
  238  				// same way.
  239  				const std::string before = game->getMetadata(MetaDataId::CheevosId);
  240  				auto cheevos = mCheevosHashes.find(hash);
  241  				const std::string id = cheevos != mCheevosHashes.cend() ? cheevos->second : std::string();
  242  				game->setMetadata(MetaDataId::CheevosId, id);
  243  				if (id != before)
  244  				{
  245  					saveToGamelistRecovery(game);
  246  					if (lookupOnly)
  247  						LOG(LogInfo) << "ThreadedHasher: id " << id << " for " << label << " from the hash library, no file read (audit #186 PL-08)";
  248  				}
  249  			}
  250  
  251  			LOG(LogDebug) << "CheckCheevosHash OK : " << label;;
  252  		}		
  253  
  254  		lock.lock();
  255  	}
  256  
  257  	mThreadCount--;
  258  
  259  	if (mThreadCount == 0)
  260  	{
  261  		lock.unlock();
  262  		delete this;
  263  		ThreadedHasher::mInstance = nullptr;
  264  
  265  	}
  266  }
  267  
  268  bool ThreadedHasher::checkCloseIfRunning(Window* window)
  269  {
  270  	if (ThreadedHasher::mInstance != nullptr)
  271  	{
  272  		window->pushGui(new GuiMsgBox(window, _("GAME HASHING IS RUNNING. DO YOU WANT TO STOP IT?"), _("YES"), []
  273  		{
  274  			ThreadedHasher::stop();
  275  		}, _("NO"), nullptr));
  276  
  277  		return false;
  278  	}
  279  
  280  	return true;
  281  }
  282  
  283  void ThreadedHasher::start(Window* window, HasherType type, bool forceAllGames, bool silent, std::set<std::string>* systems)
  284  {
  285  	if (ThreadedHasher::mInstance != nullptr)
  286  	{
  287  		if (silent)
  288  			return;
  289  
  290  		if (!checkCloseIfRunning(window))
  291  			return;
  292  	}
  293  	
  294  	std::queue<FileData*> searchQueue;
  295  	// The games with a hash and no id: a lookup against the library once it
  296  	// has come, no read (CheevosIndex, audit #186 PL-08).
  297  	std::vector<FileData*> lookupOnly;
  298  	
  299  	for (auto sys : SystemData::sSystemVector)
  300  	{
  301  		if (sys->isGroupSystem() || sys->isCollection())
  302  			continue;
  303  
  304  		bool takeNetplay = ((type & HASH_NETPLAY_CRC) == HASH_NETPLAY_CRC) && sys->isNetplaySupported();
  305  		bool takeCheevos = ((type & HASH_CHEEVOS_MD5) == HASH_CHEEVOS_MD5) && sys->isCheevosSupported();
  306  
  307  		if (!takeNetplay && !takeCheevos)
  308  			continue;
  309  
  310  		if (systems != nullptr && systems->find(sys->getName()) == systems->cend())
  311  			continue;
  312  		
  313  		if (!sys->isGameSystem() || sys->getRootFolder() == nullptr)
  314  			continue;
  315  
  316  		if (sys->isGroupChildSystem() ? sys->isHidden() : !sys->isVisible())
  317  			continue;
  318  
  319  		for (auto file : sys->getRootFolder()->getFilesRecursive(GAME))
  320  		{
  321  			bool netPlay = takeNetplay && (forceAllGames || file->getMetadata(MetaDataId::Crc32).empty());
  322  			CheevosIndex::Take take = CheevosIndex::Take::None;
  323  			if (takeCheevos)
  324  			{
  325  				take = CheevosIndex::take(forceAllGames, file->getMetadata(MetaDataId::CheevosHash), file->getMetadata(MetaDataId::CheevosId));
  326  				if (retryGameCubeRvzHash(file))
  327  					take = CheevosIndex::Take::Hash;
  328  			}
  329  			bool cheevos = take == CheevosIndex::Take::Hash;
  330  
  331  			if (cheevos)
  332  			{
  333  				std::string ext = Utils::String::toLower(Utils::FileSystem::getExtension(file->getPath()));
  334  				
  335  				if (ext == ".pbp" || ext == ".cso") // Currently unsupported formats
  336  					cheevos = false;
  337  			}
  338  
  339  			if (netPlay || cheevos)
  340  				searchQueue.push(file);
  341  			else if (take == CheevosIndex::Take::Lookup)
  342  				lookupOnly.push_back(file);
  343  		}
  344  	}
  345  
  346  	if (searchQueue.size() == 0 && lookupOnly.empty())
  347  	{
  348  		if (!silent)
  349  			window->pushGui(new GuiMsgBox(window, _("NO GAMES FIT THAT CRITERIA.")));
  350  
  351  		return;
  352  	}
  353  
  354  	// Lookups alone, from the silent startup run: once a day at most
  355  	// (CheevosIndex::lookupDue) -- the pass costs the hash library, and
  356  	// nearly every library has a game RetroAchievements does not know whose
  357  	// hash would ask for it at every boot. A run the player asked for, or
  358  	// one with games to hash (the library comes anyway), is not held back.
  359  	// The stamp is written once the library has come, so an offline boot
  360  	// does not spend the day's pass on a fetch that failed.
  361  	const bool lookupsAlone = searchQueue.empty() && silent && ((type & HASH_CHEEVOS_MD5) == HASH_CHEEVOS_MD5);
  362  	const long long now = (long long) time(nullptr);
  363  	if (lookupsAlone)
  364  	{
  365  		const long long last = strtoll(Settings::getInstance()->getString("CheevosLookupOnlyLast").c_str(), nullptr, 10);
  366  		if (!CheevosIndex::lookupDue(last, now))
  367  		{
  368  			LOG(LogInfo) << "ThreadedHasher: " << lookupOnly.size() << " game(s) with a hash and no id; the lookup pass ran within the day, next one later";
  369  			return;
  370  		}
  371  	}
  372  
  373  	try
  374  	{
  375  		ThreadedHasher* hasher = new ThreadedHasher(window, type, searchQueue, lookupOnly, forceAllGames);
  376  		// Stamped only when the library came: a boot without it has not spent
  377  		// the day's pass (the comment above promised as much; the code did not).
  378  		if (lookupsAlone && !hasher->mCheevosHashes.empty())
  379  		{
  380  			Settings::getInstance()->setString("CheevosLookupOnlyLast", std::to_string(now));
  381  			Settings::getInstance()->saveFile();
  382  		}
  383  		if (hasher->mTotal == 0)
  384  		{
  385  			// Lookups alone and the library knew none of them: nothing was
  386  			// started, nothing is shown -- as a run with nothing to hash.
  387  			delete hasher;
  388  			if (!silent)
  389  				window->pushGui(new GuiMsgBox(window, _("NO GAMES FIT THAT CRITERIA.")));
  390  			return;
  391  		}
  392  		ThreadedHasher::mInstance = hasher;
  393  	}
  394  	catch (const std::exception& e)
  395  	{
  396  		LOG(LogError) << "Game Hash failed : " << e.what();
  397  
  398  		if (!silent)
  399  			window->pushGui(new GuiMsgBox(window, e.what()));
  400  	}	
  401  }
  402  
  403  void ThreadedHasher::stop()
  404  {
  405  	auto thread = ThreadedHasher::mInstance;
  406  	if (thread == nullptr)
  407  		return;
  408  
  409  	try
  410  	{
  411  		thread->mExit = true;
  412  	}
  413  	catch (...) {}
  414  }
  415  
```


## external/libcheevos/rvz_hash.cpp @ 16dbac5211 (whole, 389 lines)

```text
    1  // SPDX-License-Identifier: MIT AND BSD-3-Clause
    2  // Copyright (c) 2026 pixelelated contributors
    3  // Padding recurrence/serialization adapted from bodgit/rvz (BSD-3-Clause).
    4  // See RVZ-NOTICES.md and LICENSE.rvz-padding. Container code follows Dolphin's
    5  // published WiaAndRvz format; no RetroArch or Dolphin implementation is copied.
    6  #include "rvz_hash.h"
    7  #include "rcheevos/include/rc_hash.h"
    8  #include "libretro-common/include/streams/interface_stream.h"
    9  #include "libretro-common/include/libretro.h"
   10  #include <boost/uuid/detail/sha1.hpp>
   11  #include <zstd.h>
   12  #include <algorithm>
   13  #include <array>
   14  #include <cstdint>
   15  #include <cstdlib>
   16  #include <cstring>
   17  #include <memory>
   18  #include <stdexcept>
   19  #include <vector>
   20  #include <utility>
   21  
   22  namespace
   23  {
   24  constexpr uint64_t Sector = 0x8000;
   25  constexpr uint32_t MaxChunk = 2 * 1024 * 1024;
   26  constexpr uint32_t MaxWork = MaxChunk + 1024 * 1024;
   27  constexpr uint64_t MaxDisc = uint64_t(2) * 1024 * 1024 * 1024;
   28  constexpr uint64_t MaxFile = uint64_t(4) * 1024 * 1024 * 1024;
   29  constexpr uint32_t MaxGroups = 65536;
   30  constexpr uint32_t MaxRaw = 4096;
   31  using Bytes = std::vector<uint8_t>;
   32  
   33  void require(bool condition)
   34  {
   35      if (!condition)
   36          throw std::runtime_error("Invalid or unsupported GameCube RVZ");
   37  }
   38  uint32_t be32(const uint8_t* p)
   39  {
   40      return (uint32_t(p[0]) << 24) | (uint32_t(p[1]) << 16) |
   41          (uint32_t(p[2]) << 8) | p[3];
   42  }
   43  uint64_t be64(const uint8_t* p)
   44  {
   45      return (uint64_t(be32(p)) << 32) | be32(p + 4);
   46  }
   47  bool sha1Matches(const uint8_t* data, size_t size, const uint8_t* expected)
   48  {
   49      boost::uuids::detail::sha1 state;
   50      boost::uuids::detail::sha1::digest_type digest;
   51      state.process_bytes(data, size);
   52      state.get_digest(digest);
   53      // Boost changed digest_type from host words to bytes. Accept both APIs.
   54      for (size_t i = 0; i < 20; ++i)
   55      {
   56          const auto byte = sizeof(digest[0]) == 1 ? digest[i] :
   57              ((digest[i / 4] >> (24 - 8 * (i % 4))) & 0xff);
   58          if (byte != expected[i])
   59              return false;
   60      }
   61      return true;
   62  }
   63  
   64  // BSD-3-Clause adaptation of bodgit/rvz/internal/padding/reader.go.
   65  // State is local, and output uses explicit bytes on both endian families.
   66  void padding(const uint8_t* seed, uint64_t offset, uint8_t* out, size_t size)
   67  {
   68      std::array<uint32_t, 521> words{};
   69      for (size_t i = 0; i < 17; ++i)
   70          words[i] = be32(seed + 4 * i);
   71      for (size_t i = 17; i < words.size(); ++i)
   72          words[i] = (words[i - 17] << 23) ^ (words[i - 16] >> 9) ^ words[i - 1];
   73      const auto advance = [&]() {
   74          for (size_t i = 0; i < 32; ++i)
   75              words[i] ^= words[i + words.size() - 32];
   76          for (size_t i = 32; i < words.size(); ++i)
   77              words[i] ^= words[i - 32];
   78      };
   79      for (unsigned i = 0; i < 4; ++i)
   80          advance();
   81      size_t byteIndex = static_cast<size_t>(offset % Sector);
   82      while (byteIndex >= words.size() * 4)
   83      {
   84          advance();
   85          byteIndex -= words.size() * 4;
   86      }
   87      const unsigned shifts[] = {24, 18, 8, 0};
   88      for (size_t i = 0; i < size; ++i)
   89      {
   90          if (byteIndex == words.size() * 4)
   91          {
   92              advance();
   93              byteIndex = 0;
   94          }
   95          out[i] = static_cast<uint8_t>(words[byteIndex / 4] >> shifts[byteIndex % 4]);
   96          ++byteIndex;
   97      }
   98  }
   99  
  100  Bytes unpack(const Bytes& packed, size_t expected, uint64_t discOffset)
  101  {
  102      Bytes result(expected);
  103      size_t input = 0, output = 0, records = 0;
  104      while (input < packed.size())
  105      {
  106          require(++records <= 4096 && packed.size() - input >= 4);
  107          const uint32_t tag = be32(packed.data() + input);
  108          input += 4;
  109          const uint32_t length = tag & 0x7fffffff;
  110          require(length <= result.size() - output);
  111          if (tag & 0x80000000)
  112          {
  113              require(packed.size() - input >= 68);
  114              if (length)
  115                  padding(packed.data() + input, discOffset + output, result.data() + output, length);
  116              input += 68;
  117          }
  118          else
  119          {
  120              require(length <= packed.size() - input);
  121              if (length)
  122                  std::memcpy(result.data() + output, packed.data() + input, length);
  123              input += length;
  124          }
  125          output += length;
  126      }
  127      require(output == expected);
  128      return result;
  129  }
  130  
  131  struct StreamCloser
  132  {
  133      void operator()(intfstream_t* stream) const
  134      {
  135          if (stream)
  136          {
  137              intfstream_close(stream);
  138              std::free(stream);
  139          }
  140      }
  141  };
  142  struct Raw
  143  {
  144      uint64_t offset, end, aligned;
  145      uint32_t first, count;
  146  };
  147  struct Group
  148  {
  149      uint64_t offset;
  150      uint32_t size, packed;
  151      bool compressed;
  152  };
  153  class Reader
  154  {
  155  public:
  156      explicit Reader(const char* path) : stream(intfstream_open_file(path,
  157          RETRO_VFS_FILE_ACCESS_READ, RETRO_VFS_FILE_ACCESS_HINT_NONE))
  158      {
  159          require(stream != nullptr);
  160          const int64_t size = intfstream_get_size(stream.get());
  161          require(size >= 0x48 + 0xd5 && uint64_t(size) <= MaxFile);
  162          fileSize = static_cast<uint64_t>(size);
  163          const Bytes header = physical(0, 0x48);
  164          require(be32(header.data()) == 0x52565a01);
  165          const uint32_t version = be32(header.data() + 4);
  166          const uint32_t compatible = be32(header.data() + 8);
  167          require(version >= 0x00030000 && version <= 0x01000000 &&
  168              compatible >= 0x00030000 && compatible <= version);
  169          require(sha1Matches(header.data(), 0x34, header.data() + 0x34));
  170          discSize = be64(header.data() + 0x24);
  171          require(discSize >= 0x2460 && discSize <= MaxDisc &&
  172              be64(header.data() + 0x2c) == fileSize);
  173          const uint32_t secondSize = be32(header.data() + 0xc);
  174          require(secondSize >= 0xd5 && secondSize <= 4096);
  175          const Bytes second = physical(0x48, secondSize);
  176          require(sha1Matches(second.data(), second.size(), header.data() + 0x10));
  177          require(be32(second.data()) == 1 && be32(second.data() + 0x90) == 0);
  178          compression = be32(second.data() + 4);
  179          require((compression == 0 || compression == 5) && second[0xd4] == 0);
  180          chunk = be32(second.data() + 0xc);
  181          require(chunk >= Sector && chunk <= MaxChunk && (chunk & (chunk - 1)) == 0);
  182          std::copy_n(second.data() + 0x10, head.size(), head.begin());
  183          require(be32(head.data() + 0x1c) == 0xc2339f3d);
  184          const uint32_t rawCount = be32(second.data() + 0xb4);
  185          const uint32_t groupCount = be32(second.data() + 0xc4);
  186          require(rawCount && rawCount <= MaxRaw && groupCount && groupCount <= MaxGroups);
  187          Bytes table = decode(be64(second.data() + 0xc8), be32(second.data() + 0xd0),
  188              groupCount * 12, compression == 5);
  189          groups.reserve(groupCount);
  190          for (uint32_t i = 0; i < groupCount; ++i)
  191          {
  192              const uint8_t* p = table.data() + size_t(i) * 12;
  193              const uint32_t flags = be32(p + 4);
  194              Group group{uint64_t(be32(p)) * 4, flags & 0x7fffffff, be32(p + 8),
  195                  (flags & 0x80000000) != 0};
  196              require(group.size <= MaxWork && group.packed <= MaxWork);
  197              require(group.offset <= fileSize && group.size <= fileSize - group.offset);
  198              groups.push_back(group);
  199          }
  200          table = decode(be64(second.data() + 0xb8), be32(second.data() + 0xc0),
  201              rawCount * 24, compression == 5);
  202          raw.reserve(rawCount);
  203          for (uint32_t i = 0; i < rawCount; ++i)
  204          {
  205              const uint8_t* p = table.data() + size_t(i) * 24;
  206              const uint64_t offset = be64(p), length = be64(p + 8);
  207              require(offset < discSize && length && length <= discSize - offset);
  208              Raw entry{offset, offset + length, offset - offset % Sector,
  209                  be32(p + 16), be32(p + 20)};
  210              require(entry.first < groups.size() && entry.count <= groups.size() - entry.first);
  211              require(entry.count == (entry.end - entry.aligned + chunk - 1) / chunk);
  212              raw.push_back(entry);
  213          }
  214          std::sort(raw.begin(), raw.end(), [](const Raw& a, const Raw& b) { return a.offset < b.offset; });
  215          uint64_t end = raw.front().offset;
  216          require(end == 0 || end == head.size());
  217          for (const Raw& entry : raw)
  218          {
  219              require(entry.offset == end);
  220              end = entry.end;
  221          }
  222          require(end == discSize);
  223      }
  224  
  225      void seek(int64_t offset, int origin)
  226      {
  227          uint64_t base;
  228          if (origin == SEEK_SET) base = 0;
  229          else if (origin == SEEK_CUR) base = position;
  230          else if (origin == SEEK_END) base = discSize;
  231          else { failed = true; return; }
  232          if (offset < 0)
  233          {
  234              if (offset < -static_cast<int64_t>(base)) { failed = true; return; }
  235              position = base - static_cast<uint64_t>(-offset);
  236          }
  237          else
  238          {
  239              if (static_cast<uint64_t>(offset) > discSize - base) { failed = true; return; }
  240              position = base + static_cast<uint64_t>(offset);
  241          }
  242      }
  243      int64_t tell() const { return static_cast<int64_t>(position); }
  244      size_t read(void* destination, size_t requested)
  245      {
  246          if (failed || requested > discSize - position || requested > 128 * 1024 * 1024 - totalRead)
  247          {
  248              failed = true;
  249              return 0;
  250          }
  251          totalRead += requested;
  252          auto* out = static_cast<uint8_t*>(destination);
  253          size_t done = 0;
  254          while (done < requested)
  255          {
  256              if (position < head.size())
  257              {
  258                  const size_t take = std::min(requested - done, head.size() - size_t(position));
  259                  std::memcpy(out + done, head.data() + position, take);
  260                  position += take;
  261                  done += take;
  262                  continue;
  263              }
  264              const auto found = std::upper_bound(raw.begin(), raw.end(), position,
  265                  [](uint64_t value, const Raw& entry) { return value < entry.offset; });
  266              require(found != raw.begin());
  267              const Raw& entry = *(found - 1);
  268              require(position < entry.end);
  269              const uint64_t groupBase = entry.aligned + (position - entry.aligned) / chunk * chunk;
  270              const uint32_t index = entry.first + uint32_t((position - entry.aligned) / chunk);
  271              const size_t length = static_cast<size_t>(std::min(uint64_t(chunk), entry.end - groupBase));
  272              if (cachedIndex != index || cachedBase != groupBase || cache.size() != length)
  273              {
  274                  const Group& group = groups[index];
  275                  Bytes decoded;
  276                  if (!group.size)
  277                  {
  278                      accountDecoded(length);
  279                      decoded.assign(length, 0);
  280                  }
  281                  else
  282                  {
  283                      decoded = decode(group.offset, group.size,
  284                          group.packed ? group.packed : length, group.compressed && compression == 5);
  285                      if (group.packed)
  286                      {
  287                          accountDecoded(length);
  288                          decoded = unpack(decoded, length, groupBase);
  289                      }
  290                  }
  291                  cache = std::move(decoded);
  292                  cachedIndex = index;
  293                  cachedBase = groupBase;
  294              }
  295              const size_t into = static_cast<size_t>(position - groupBase);
  296              const size_t take = std::min(requested - done, cache.size() - into);
  297              require(take != 0);
  298              std::memcpy(out + done, cache.data() + into, take);
  299              done += take;
  300              position += take;
  301          }
  302          return done;
  303      }
  304      bool failed = false;
  305  
  306  private:
  307      Bytes physical(uint64_t offset, size_t bytes)
  308      {
  309          require(bytes <= MaxWork && offset <= fileSize && bytes <= fileSize - offset);
  310          require(intfstream_seek(stream.get(), static_cast<int64_t>(offset), SEEK_SET) >= 0);
  311          Bytes result(bytes);
  312          require(intfstream_read(stream.get(), result.data(), bytes) == static_cast<int64_t>(bytes));
  313          return result;
  314      }
  315      void accountDecoded(size_t bytes)
  316      {
  317          require(bytes <= MaxWork && bytes <= 512 * 1024 * 1024 - totalDecoded);
  318          totalDecoded += bytes;
  319      }
  320      Bytes decode(uint64_t offset, uint32_t bytes, size_t expected, bool compressed)
  321      {
  322          accountDecoded(expected);
  323          Bytes input = physical(offset, bytes);
  324          if (!compressed)
  325          {
  326              require(input.size() == expected);
  327              return input;
  328          }
  329          require(!input.empty());
  330          const size_t frameSize = ZSTD_findFrameCompressedSize(input.data(), input.size());
  331          require(!ZSTD_isError(frameSize) && frameSize == input.size());
  332          Bytes output(expected);
  333          const size_t actual = ZSTD_decompress(output.data(), output.size(), input.data(), input.size());
  334          require(!ZSTD_isError(actual) && actual == expected);
  335          return output;
  336      }
  337      std::unique_ptr<intfstream_t, StreamCloser> stream;
  338      uint64_t fileSize = 0, discSize = 0, position = 0;
  339      uint32_t chunk = 0, compression = 0;
  340      std::array<uint8_t, 128> head{};
  341      std::vector<Raw> raw;
  342      std::vector<Group> groups;
  343      Bytes cache;
  344      uint32_t cachedIndex = UINT32_MAX;
  345      uint64_t cachedBase = 0;
  346      size_t totalRead = 0, totalDecoded = 0;
  347  };
  348  
  349  void* openRvz(const char* path)
  350  {
  351      try { return new Reader(path); }
  352      catch (...) { return nullptr; }
  353  }
  354  void closeRvz(void* opaque) { delete static_cast<Reader*>(opaque); }
  355  void seekRvz(void* opaque, int64_t offset, int origin)
  356  {
  357      static_cast<Reader*>(opaque)->seek(offset, origin);
  358  }
  359  int64_t tellRvz(void* opaque) { return static_cast<Reader*>(opaque)->tell(); }
  360  size_t readRvz(void* opaque, void* data, size_t bytes)
  361  {
  362      Reader& reader = *static_cast<Reader*>(opaque);
  363      try { return reader.read(data, bytes); }
  364      catch (...) { reader.failed = true; return 0; }
  365  }
  366  struct Iterator
  367  {
  368      explicit Iterator(const char* path) { rc_hash_initialize_iterator(&value, path, nullptr, 0); }
  369      ~Iterator() { rc_hash_destroy_iterator(&value); }
  370      rc_hash_iterator_t value;
  371  };
  372  } // namespace
  373  
  374  bool generateGameCubeRvzHash(char hash[33], const char* path)
  375  {
  376      hash[0] = '\0';
  377      try
  378      {
  379          Iterator iterator(path);
  380          if (!iterator.value.path)
  381              return false;
  382          iterator.value.callbacks.filereader = {openRvz, seekRvz, tellRvz, readRvz, closeRvz};
  383          if (rc_hash_generate(hash, RC_CONSOLE_GAMECUBE, &iterator.value))
  384              return true;
  385      }
  386      catch (...) {}
  387      hash[0] = '\0';
  388      return false;
  389  }
```


## The library's five edits: git diff bccd715707..16dbac5211

```text
diff --git a/external/libcheevos/CMakeLists.txt b/external/libcheevos/CMakeLists.txt
index 39574ad05..952b33efc 100644
--- a/external/libcheevos/CMakeLists.txt
+++ b/external/libcheevos/CMakeLists.txt
@@ -226,3 +226,20 @@ include_directories(${COMMON_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR}/libretro-
 include_directories(${COMMON_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR}/libretro-common/src/7zip)
 
 add_library(libcheevos STATIC ${CHEEVOS_SOURCES} ${CHEEVOS_HEADERS} ${LIBRETRO_COMMON_HEADERS} ${LIBRETRO_COMMON_SOURCES})
+
+# The distro enables this bounded GameCube reader; other builds may opt in.
+# No global file-reader override, extracted ISO, or emulator invocation.
+option(ENABLE_RVZ_HASH "Hash supported GameCube RVZ files" ${ROCKNIX})
+if(ENABLE_RVZ_HASH)
+    find_path(LIBCHEEVOS_ZSTD_INCLUDE_DIR zstd.h)
+    find_library(LIBCHEEVOS_ZSTD_LIBRARY NAMES zstd libzstd)
+    find_path(LIBCHEEVOS_SHA1_INCLUDE_DIR boost/uuid/detail/sha1.hpp
+        HINTS ${Boost_INCLUDE_DIRS} ${COMMON_INCLUDE_DIRS})
+    if(NOT LIBCHEEVOS_ZSTD_INCLUDE_DIR OR NOT LIBCHEEVOS_ZSTD_LIBRARY OR NOT LIBCHEEVOS_SHA1_INCLUDE_DIR)
+        message(FATAL_ERROR "ENABLE_RVZ_HASH requires target Zstandard and Boost SHA-1 headers")
+    endif()
+    target_sources(libcheevos PRIVATE rvz_hash.cpp rvz_hash.h)
+    target_compile_definitions(libcheevos PRIVATE HAVE_RVZ_HASH)
+    target_include_directories(libcheevos PRIVATE ${LIBCHEEVOS_ZSTD_INCLUDE_DIR} ${LIBCHEEVOS_SHA1_INCLUDE_DIR})
+    target_link_libraries(libcheevos PUBLIC ${LIBCHEEVOS_ZSTD_LIBRARY})
+endif()
diff --git a/external/libcheevos/cheevos.cpp b/external/libcheevos/cheevos.cpp
index 554504b88..e21bea792 100644
--- a/external/libcheevos/cheevos.cpp
+++ b/external/libcheevos/cheevos.cpp
@@ -1,4 +1,7 @@
 #include "cheevos.h"
+#ifdef HAVE_RVZ_HASH
+#include "rvz_hash.h"
+#endif
 #include "rcheevos/include/rc_hash.h"
 #include "rcheevos/include/rc_consoles.h"
 #include "libretro-common/include/formats/cdfs.h"
@@ -153,8 +156,21 @@ static void* rc_hash_handle_cd_open_track(
     }
 }
 
+bool gameCubeRvzHashEnabled()
+{
+#ifdef HAVE_RVZ_HASH
+    return true;
+#else
+    return false;
+#endif
+}
+
 bool generateHashFromFile(char hash[33], int console_id, const char* path)
 {
+#ifdef HAVE_RVZ_HASH
+    if (console_id == RC_CONSOLE_GAMECUBE && string_is_equal_noncase(path_get_extension(path), "rvz"))
+        return generateGameCubeRvzHash(hash, path);
+#endif
 	try
 	{
 		if (!readersinit)
diff --git a/external/libcheevos/cheevos.h b/external/libcheevos/cheevos.h
index a18ccb71a..ca6f3785c 100644
--- a/external/libcheevos/cheevos.h
+++ b/external/libcheevos/cheevos.h
@@ -3,3 +3,6 @@
 #include "rcheevos/include/rc_consoles.h"
 
 bool generateHashFromFile(char hash[33], int console_id, const char* path);
+
+// Build capability only: individual RVZ modes/inputs may still be rejected.
+bool gameCubeRvzHashEnabled();
diff --git a/external/libcheevos/libretro-common/src/utils/md5.c b/external/libcheevos/libretro-common/src/utils/md5.c
index 5deb03ce5..132486f06 100644
--- a/external/libcheevos/libretro-common/src/utils/md5.c
+++ b/external/libcheevos/libretro-common/src/utils/md5.c
@@ -68,8 +68,17 @@
  * doesn't work.
  */
 #if defined(__i386__) || defined(__x86_64__) || defined(__vax__)
+/* These hosts are little-endian, but input need not satisfy C alignment or
+ * effective-type requirements. memcpy preserves the unaligned fast path
+ * without dereferencing an incompatible or misaligned word pointer. */
+static MD5_u32plus MD5_load_word(const unsigned char *input)
+{
+	MD5_u32plus word;
+	memcpy(&word, input, sizeof(word));
+	return word;
+}
 #define MD5_SET(n) \
-	(*(MD5_u32plus *)&ptr[(n) * 4])
+	MD5_load_word(&ptr[(n) * 4])
 #define MD5_GET(n) \
 	MD5_SET(n)
 #else
diff --git a/external/libcheevos/rcheevos/src/rhash/hash_disc.c b/external/libcheevos/rcheevos/src/rhash/hash_disc.c
index 83c93545e..e74ac4208 100644
--- a/external/libcheevos/rcheevos/src/rhash/hash_disc.c
+++ b/external/libcheevos/rcheevos/src/rhash/hash_disc.c
@@ -425,6 +425,7 @@ static int rc_hash_nintendo_disc_partition(md5_state_t* md5, const rc_hash_itera
   uint8_t* buffer;
 
   uint64_t dol_offset;
+  uint64_t full_header_size;
   uint64_t dol_offsets[18];
   uint64_t dol_sizes[18];
 
@@ -435,23 +436,27 @@ static int rc_hash_nintendo_disc_partition(md5_state_t* md5, const rc_hash_itera
   /* GetApploaderSize */
   rc_file_seek(iterator, file_handle, part_offset + BASE_HEADER_SIZE + 0x14, SEEK_SET);
   apploader_header_size = 0x20;
-  rc_file_read(iterator, file_handle, quad_buffer, 4);
+  if (rc_file_read(iterator, file_handle, quad_buffer, 4) != 4)
+    return rc_hash_iterator_error(iterator, "Truncated Nintendo disc header");
   apploader_body_size =
-    (quad_buffer[0] << 24) | (quad_buffer[1] << 16) | (quad_buffer[2] << 8) | quad_buffer[3];
-  rc_file_read(iterator, file_handle, quad_buffer, 4);
+    ((uint32_t)quad_buffer[0] << 24) | (quad_buffer[1] << 16) | (quad_buffer[2] << 8) | quad_buffer[3];
+  if (rc_file_read(iterator, file_handle, quad_buffer, 4) != 4)
+    return rc_hash_iterator_error(iterator, "Truncated Nintendo disc header");
   apploader_trailer_size =
-    (quad_buffer[0] << 24) | (quad_buffer[1] << 16) | (quad_buffer[2] << 8) | quad_buffer[3];
-  header_size = BASE_HEADER_SIZE + apploader_header_size + apploader_body_size + apploader_trailer_size;
-  if (header_size > MAX_HEADER_SIZE) header_size = MAX_HEADER_SIZE;
+    ((uint32_t)quad_buffer[0] << 24) | (quad_buffer[1] << 16) | (quad_buffer[2] << 8) | quad_buffer[3];
+  full_header_size = (uint64_t)BASE_HEADER_SIZE + apploader_header_size + apploader_body_size + apploader_trailer_size;
+  header_size = (full_header_size > MAX_HEADER_SIZE) ? MAX_HEADER_SIZE : (uint32_t)full_header_size;
 
   /* Hash headers */
   buffer = (uint8_t*)malloc(header_size);
   if (!buffer) {
-    rc_file_close(iterator, file_handle);
     return rc_hash_iterator_error(iterator, "Could not allocate temporary buffer");
   }
   rc_file_seek(iterator, file_handle, part_offset, SEEK_SET);
-  rc_file_read(iterator, file_handle, buffer, header_size);
+  if (rc_file_read(iterator, file_handle, buffer, header_size) != header_size) {
+    free(buffer);
+    return rc_hash_iterator_error(iterator, "Truncated Nintendo disc header");
+  }
   rc_hash_iterator_verbose_formatted(iterator, "Hashing %u byte partition header", header_size);
   md5_append(md5, buffer, header_size);
 
@@ -466,7 +471,8 @@ static int rc_hash_nintendo_disc_partition(md5_state_t* md5, const rc_hash_itera
 
   /* Find offsets and sizes for the 7 main.dol code segments and 11 main.dol data segments */
   rc_file_seek(iterator, file_handle, part_offset + dol_offset, SEEK_SET);
-  rc_file_read(iterator, file_handle, addr_buffer, 0xD8);
+  if (rc_file_read(iterator, file_handle, addr_buffer, sizeof(addr_buffer)) != sizeof(addr_buffer))
+    return rc_hash_iterator_error(iterator, "Truncated Nintendo disc executable table");
   for (ix = 0; ix < 18; ix++) {
     dol_offsets[ix] = (((uint64_t)addr_buffer[0x0 + ix * 4] << 24) |
       ((uint64_t)addr_buffer[0x1 + ix * 4] << 16) |
@@ -481,7 +487,6 @@ static int rc_hash_nintendo_disc_partition(md5_state_t* md5, const rc_hash_itera
   /* Iterate through the 18 main.dol segments and hash each */
   buffer = (uint8_t*)malloc(MAX_CHUNK_SIZE);
   if (!buffer) {
-    rc_file_close(iterator, file_handle);
     return rc_hash_iterator_error(iterator, "Could not allocate temporary buffer");
   }
 
@@ -497,11 +502,17 @@ static int rc_hash_nintendo_disc_partition(md5_state_t* md5, const rc_hash_itera
 
     remaining_size = dol_sizes[ix];
     while (remaining_size > MAX_CHUNK_SIZE) {
-      rc_file_read(iterator, file_handle, buffer, MAX_CHUNK_SIZE);
+      if (rc_file_read(iterator, file_handle, buffer, MAX_CHUNK_SIZE) != MAX_CHUNK_SIZE) {
+        free(buffer);
+        return rc_hash_iterator_error(iterator, "Truncated Nintendo disc executable");
+      }
       md5_append(md5, buffer, MAX_CHUNK_SIZE);
       remaining_size -= MAX_CHUNK_SIZE;
     }
-    rc_file_read(iterator, file_handle, buffer, (int32_t)remaining_size);
+    if (rc_file_read(iterator, file_handle, buffer, (size_t)remaining_size) != remaining_size) {
+      free(buffer);
+      return rc_hash_iterator_error(iterator, "Truncated Nintendo disc executable");
+    }
     md5_append(md5, buffer, (int32_t)remaining_size);
   }
 
@@ -524,8 +535,9 @@ int rc_hash_gamecube(char hash[33], const rc_hash_iterator_t* iterator)
   md5_init(&md5);
   /* Check Magic Word */
   rc_file_seek(iterator, file_handle, 0x1c, SEEK_SET);
-  rc_file_read(iterator, file_handle, quad_buffer, 4);
-  if (quad_buffer[0] == 0xC2 && quad_buffer[1] == 0x33 && quad_buffer[2] == 0x9F && quad_buffer[3] == 0x3D)
+  if (rc_file_read(iterator, file_handle, quad_buffer, 4) != 4)
+    success = rc_hash_iterator_error(iterator, "Truncated GameCube disc magic");
+  else if (quad_buffer[0] == 0xC2 && quad_buffer[1] == 0x33 && quad_buffer[2] == 0x9F && quad_buffer[3] == 0x3D)
     success = rc_hash_nintendo_disc_partition(&md5, iterator, file_handle, 0, 0);
   else
     success = rc_hash_iterator_error(iterator, "Not a Gamecube disc");
```


## es-app/src/RetroAchievements.cpp @ 16dbac5211: lines 126-203 (excerpt of 1072)

```text
  126  	RC_CONSOLE_SEGA_32X,
  127  	RC_CONSOLE_SG1000,
  128  	RC_CONSOLE_VECTREX,
  129  	RC_CONSOLE_VIRTUAL_BOY,
  130  	RC_CONSOLE_WONDERSWAN,
  131  	RC_CONSOLE_SUPERVISION
  132  };
  133  
  134  // The web API authenticates with a user and that user's web API key
  135  // ("z=<user>&y=<key>"). Upstream compiles a pair in (CHEEVOS_DEV_LOGIN). A
  136  // fork build compiles none in, so the player's own key -- from the account's
  137  // settings page on retroachievements.org, entered under RETROACHIEVEMENTS
  138  // SETTINGS -- goes with their username (#68). Empty means the API cannot be
  139  // asked, and callers say so instead of letting it answer 401.
  140  std::string RetroAchievements::getApiLogin()
  141  {
  142  #ifdef CHEEVOS_DEV_LOGIN
  143  	return CHEEVOS_DEV_LOGIN;
  144  #else
  145  	const std::string user = SystemConf::getInstance()->get("global.retroachievements.username");
  146  	const std::string key = SystemConf::getInstance()->get("global.retroachievements.key");
  147  	if (user.empty() || key.empty())
  148  		return "";
  149  	return "z=" + HttpReq::urlEncode(user) + "&y=" + HttpReq::urlEncode(key);
  150  #endif
  151  }
  152  
  153  std::string RetroAchievements::getMissingLoginMessage()
  154  {
  155  	return _("RETROACHIEVEMENTS NEEDS YOUR WEB API KEY.\nENTER IT UNDER RETROACHIEVEMENTS SETTINGS, NEXT TO YOUR PASSWORD.");
  156  }
  157  
  158  // A 401 from the API is the key being wrong; say that in English rather than
  159  // showing the API's JSON.
  160  std::string RetroAchievements::getLoginErrorMessage(HttpReq& req)
  161  {
  162  	if (req.status() == HttpReq::REQ_401_FORBIDDEN || req.status() == HttpReq::REQ_403_BADLOGIN)
  163  		return _("RETROACHIEVEMENTS REJECTED YOUR WEB API KEY.\nCHECK IT AND YOUR USERNAME UNDER RETROACHIEVEMENTS SETTINGS.");
  164  
  165  	return req.getErrorMsg();
  166  }
  167  
  168  // How long a page waits on the web in all before the device's copy is shown
  169  // instead (fork #190): the connect limit alone (10 s) left a summary on a
  170  // dead link on PLEASE WAIT with no end on the RG SP.
  171  static const long PAGE_REQUEST_MS = 15000L;
  172  
  173  // Use empty UserAgent with doRequest.php calls
  174  static HttpReqOptions getHttpOptions()
  175  {
  176  	HttpReqOptions options;
  177  
  178  	std::string login = RetroAchievements::getApiLogin();
  179  	if (!login.empty())
  180  	{
  181  		std::string ret = Utils::String::extractString(login, "z=", "&");
  182  		ret =  ret + "/" + Utils::String::replace(RESOURCE_VERSION_STRING, ",", ".");		 
  183  		options.userAgent = ret;
  184  	}
  185  
  186  	return options;
  187  }
  188  
  189  std::string RetroAchievements::getApiUrl(const std::string& method, const std::string& parameters)
  190  {
  191  	std::string login = getApiLogin();
  192  	if (login.empty())
  193  		return "https://retroachievements.org/API/" + method + ".php?" + parameters;
  194  
  195  	return "https://retroachievements.org/API/" + method + ".php?" + login + "&" + parameters;
  196  }
  197  
  198  std::string GameInfoAndUserProgress::getImageUrl(const std::string& image)
  199  {
  200  	const std::string& icon = image.empty() ? ImageIcon : image;
  201  	// The proxy hands the icon back as a whole address on itself; the web
  202  	// API hands back a path on the media host.
  203  	if (Utils::String::startsWith(icon, "http://") || Utils::String::startsWith(icon, "https://"))
```


## es-app/src/RetroAchievements.cpp @ 16dbac5211: lines 282-353 (excerpt of 1072)

```text
  282  	ret.ID = 0;
  283  	ret.ConsoleID = 0;
  284  	ret.ForumTopicID = 0;
  285  	ret.Flags = 0;
  286  	ret.IsFinal = false;
  287  	ret.NumAchievements = 0;
  288  	ret.NumAwardedToUser = 0;
  289  	ret.NumAwardedToUserHardcore = 0;
  290  
  291  	const std::string user = OfflineAchievements::username();
  292  	if (user.empty())
  293  		return ret;
  294  
  295  	std::string body, error;
  296  	OfflineAchievementsText::Game game;
  297  	bool notCached = false;
  298  
  299  	if (gameId > 0)
  300  	{
  301  		if (OfflineAchievements::askProxy("r=patch&g=" + std::to_string(gameId) + "&u=" + HttpReq::urlEncode(user), body, error))
  302  			game = OfflineAchievementsText::parsePatch(body);
  303  		else if (OfflineAchievementsText::isNotCached(error))
  304  			notCached = true;
  305  		else
  306  		{
  307  			LOG(LogWarning) << "RetroAchievements: the offline proxy did not answer patch for game " << gameId << ": " << error;
  308  			ret.ProxyDidNotAnswer = true;
  309  			return ret;
  310  		}
  311  	}
  312  
  313  	if (!game.ok && !cheevosHash.empty())
  314  	{
  315  		if (OfflineAchievements::askProxy("r=achievementsets&m=" + HttpReq::urlEncode(Utils::String::toLower(cheevosHash)) + "&u=" + HttpReq::urlEncode(user), body, error))
  316  			game = OfflineAchievementsText::parseAchievementSets(body);
  317  		else if (OfflineAchievementsText::isNotCached(error))
  318  			notCached = true;
  319  		else
  320  		{
  321  			LOG(LogWarning) << "RetroAchievements: the offline proxy did not answer achievementsets: " << error;
  322  			ret.ProxyDidNotAnswer = true;
  323  			return ret;
  324  		}
  325  	}
  326  
  327  	if (!game.ok)
  328  	{
  329  		ret.NotOnDevice = notCached;
  330  		return ret;
  331  	}
  332  
  333  	// The unlocks are half the page; without them every badge would read
  334  	// locked, which is a page that lies. No answer, no page: the caller
  335  	// asks the web and says what it says. A 200 whose body is not the
  336  	// unlocks shape is no answer either (audit #186 PL-26): it is not read
  337  	// as "nothing unlocked".
  338  	if (!OfflineAchievements::askProxy("r=unlocks&g=" + std::to_string(game.id) + "&u=" + HttpReq::urlEncode(user), body, error))
  339  	{
  340  		LOG(LogWarning) << "RetroAchievements: the offline proxy did not answer unlocks for game " << game.id << ": " << error;
  341  		ret.ProxyDidNotAnswer = true;
  342  		return ret;
  343  	}
  344  	const OfflineAchievementsText::Unlocks unlocks = OfflineAchievementsText::parseUnlocks(body);
  345  	if (!unlocks.ok)
  346  	{
  347  		LOG(LogWarning) << "RetroAchievements: the offline proxy's unlocks for game " << game.id << " were not the shape expected; no page from the device";
  348  		return ret;
  349  	}
  350  	std::set<int> unlocked;
  351  	for (int id : unlocks.ids)
  352  		unlocked.insert(id);
  353  
```


## es-app/src/RetroAchievements.cpp @ 16dbac5211: lines 492-533 (excerpt of 1072)

```text
  492  	// will say in its own words that there is no connection. Online, the
  493  	// web stays the source -- it has the unlock dates, the hardcore counts
  494  	// and the rank the cache does not -- with the device's copy as the
  495  	// fallback when the web could not be reached.
  496  	const bool offline = OfflineAchievements::proxyOffline();
  497  	if (offline)
  498  	{
  499  		auto device = getGameInfoFromDevice(gameId, cheevosHash);
  500  		if (device.ID != 0 || device.NotOnDevice)
  501  			return device;
  502  		// The proxy did not answer, and there is no link to ask the web on:
  503  		// the web's answer would be its timeout, ten seconds later, in
  504  		// libcurl's words (fork #242: "Timeout was reached" on the RG35XX
  505  		// SP). Say what happened instead, in the player's.
  506  		LOG(LogWarning) << "RetroAchievements: offline, and the proxy did not answer for game " << gameId << "; not asking the web";
  507  		ret.Title = _("THE OFFLINE ACHIEVEMENTS SERVICE DIDN'T ANSWER. TRY AGAIN IN A MOMENT.");
  508  		return ret;
  509  	}
  510  
  511  	if (getApiLogin().empty())
  512  	{
  513  		ret.Title = getMissingLoginMessage();
  514  		return ret;
  515  	}
  516  
  517  	auto options = getHttpOptions();
  518  	// A page's request ends: the device's copy follows a web that did not
  519  	// answer in time (fork #190; the hash library keeps its unbounded fetch).
  520  	options.timeout = PAGE_REQUEST_MS;
  521  	HttpReq httpreq(getApiUrl("API_GetGameInfoAndUserProgress", "u=" + HttpReq::urlEncode(usrName) + "&g=" + std::to_string(gameId)), &options);
  522  	if (httpreq.wait())
  523  	{
  524  		rapidjson::Document doc;
  525  		doc.Parse(httpreq.getContent().c_str());
  526  		if (doc.HasParseError())
  527  			return ret;
  528  
  529  		ret.ID = jsonInt(doc, "ID");
  530  		ret.Title = jsonString(doc, "Title");
  531  		ret.ConsoleID = jsonInt(doc, "ConsoleID");
  532  		ret.ForumTopicID = jsonInt(doc, "ForumTopicID");
  533  		ret.Flags = jsonInt(doc, "Flags");
```


## es-app/src/RetroAchievements.cpp @ 16dbac5211: lines 732-808 (excerpt of 1072)

```text
  732  		{
  733  			auto device = getUserSummaryFromDevice();
  734  			if (!device.Username.empty())
  735  				return device;
  736  		}
  737  		ret.Status = getLoginErrorMessage(httpreq);
  738  	}
  739  
  740  	return ret;
  741  }
  742  
  743  UserRankAndScore RetroAchievements::getUserRankAndScore(const std::string& userName)
  744  {
  745  	auto usrName = userName;
  746  	if (usrName.empty())
  747  		usrName = SystemConf::getInstance()->get("global.retroachievements.username");
  748  
  749  	UserRankAndScore ret;
  750  
  751  	if (getApiLogin().empty())
  752  		return ret;
  753  
  754  	auto options = getHttpOptions();
  755  	options.timeout = PAGE_REQUEST_MS;   // fork #190
  756  
  757  	HttpReq request(getApiUrl("API_GetUserRankAndScore", "u=" + HttpReq::urlEncode(usrName)), &options);
  758  	if (request.wait())
  759  	{
  760  		rapidjson::Document doc;
  761  		doc.Parse(request.getContent().c_str());
  762  		if (doc.HasParseError())
  763  			throw std::domain_error("Error while parsing API GetUserRankAndScore response");
  764  
  765  		ret.Score = jsonInt(doc, "Score");
  766  		ret.SoftcoreScore = jsonInt(doc, "SoftcoreScore");
  767  		ret.Rank = jsonString(doc, "Rank");
  768  		ret.TotalRanked = jsonInt(doc, "TotalRanked");
  769  	}
  770  	else
  771  		throw std::domain_error("Error while accessing API GetUserRankAndScore :\n" + request.getErrorMsg());
  772  
  773  	return ret;
  774  }
  775  
  776  RetroAchievementInfo RetroAchievements::toRetroAchivementInfo(UserSummary& ret)
  777  {
  778  	RetroAchievementInfo info;
  779  
  780  	if (ret.Username.empty() && !ret.Status.empty())
  781  	{
  782  		info.error = ret.Status;
  783  		return info;
  784  	}
  785  
  786  	info.fromDevice = ret.FromDevice;
  787  	// The proxy caches no picture of the player; a request for one would
  788  	// only fail offline.
  789  	info.userpic = ret.FromDevice ? "" : "https://retroachievements.org" + ret.UserPic;
  790  	info.rank = ret.Rank;
  791  
  792  	if (!ret.TotalRanked.empty() && !ret.Rank.empty())
  793  		info.rank = ret.Rank + " / " + ret.TotalRanked;
  794  
  795  	info.points = ret.TotalPoints;
  796  	info.totalpoints = ret.TotalTruePoints;
  797  
  798  	if (!ret.TotalSoftcorePoints.empty())
  799  		info.softpoints = std::to_string(Utils::String::toInteger(ret.TotalSoftcorePoints));
  800  	else
  801  		info.softpoints = std::to_string(Utils::String::toInteger(info.totalpoints) - Utils::String::toInteger(info.points));
  802  
  803  	info.username = ret.Username;
  804  	info.registered = ret.MemberSince;
  805  
  806  	for (auto played : ret.RecentlyPlayed)
  807  	{
  808  		RetroAchievementGame rg;
```


## es-app/src/RetroAchievements.cpp @ 16dbac5211: lines 842-938 (excerpt of 1072)

```text
  842  	}
  843  
  844  	return info;
  845  }
  846  
  847  std::map<std::string, std::string> RetroAchievements::getCheevosHashes()
  848  {
  849  	std::map<std::string, std::string> ret;
  850  
  851  	try
  852  	{
  853  		std::map<int, std::string> officialGames;
  854  
  855  		auto options = getHttpOptions();
  856  		// Long is allowed (the library is megabytes, and #190 keeps its total
  857  		// unbounded); silent is not. With the link gone, a pooled connection
  858  		// to RetroAchievements sends nothing and TCP retries it for a quarter
  859  		// of an hour, and this fetch runs on the interface thread: the game
  860  		// list update with the Wi-Fi down held the screen for twelve minutes
  861  		// on the VM before the link's return failed it (ROCKNIX fork #299).
  862  		// Thirty seconds without a byte ends it, and the hasher then says so.
  863  		options.stallTimeout = 30L;
  864  
  865  		HttpReq hashLibrary("https://retroachievements.org/dorequest.php?r=hashlibrary", &options);
  866  		HttpReq officialGamesList("https://retroachievements.org/dorequest.php?r=officialgameslist", &options);
  867  
  868  		// Official games
  869  		if (officialGamesList.wait())
  870  		{
  871  			rapidjson::Document ogdoc;
  872  			ogdoc.Parse(officialGamesList.getContent().c_str());
  873  			if (ogdoc.HasParseError())
  874  				return ret;
  875  
  876  			if (!ogdoc.HasMember("Response"))
  877  				return ret;
  878  
  879  			const rapidjson::Value& response = ogdoc["Response"];
  880  			for (auto it = response.MemberBegin(); it != response.MemberEnd(); ++it)
  881  			{
  882  				int gameId = Utils::String::toInteger(it->name.GetString());
  883  
  884  				if (it->value.GetType() == rapidjson::Type::kStringType)
  885  					officialGames[gameId] = it->value.GetString();
  886  				else if (it->value.GetType() == rapidjson::Type::kNumberType)
  887  					officialGames[gameId] = std::to_string(it->value.GetInt());
  888  			}
  889  		}
  890  		else if (officialGamesList.status() != HttpReq::REQ_SUCCESS)
  891  			throw std::domain_error("Error while accessing retroachievements official games list :\n" + officialGamesList.getErrorMsg());
  892  
  893  		// Hash library
  894  		if (hashLibrary.wait())
  895  		{
  896  			rapidjson::Document doc;
  897  			doc.Parse(hashLibrary.getContent().c_str());
  898  			if (doc.HasParseError())
  899  				return ret;
  900  
  901  			if (!doc.HasMember("MD5List"))
  902  				return ret;
  903  
  904  			const rapidjson::Value& mdlist = doc["MD5List"];
  905  			for (auto it = mdlist.MemberBegin(); it != mdlist.MemberEnd(); ++it)
  906  			{
  907  				std::string name = Utils::String::toUpper(it->name.GetString());
  908  
  909  				if (!it->value.IsInt())
  910  					continue;
  911  
  912  				int gameId = it->value.GetInt();
  913  
  914  				if (officialGames.find(gameId) == officialGames.cend())
  915  					continue;
  916  
  917  				ret[name] = std::to_string(gameId);
  918  			}
  919  		}
  920  		else if (hashLibrary.status() != HttpReq::REQ_SUCCESS)
  921  			throw std::domain_error("Error while accessing retroachievements hashlibrary :\n" + hashLibrary.getErrorMsg());
  922  	}
  923  	catch (const std::exception& e)
  924  	{
  925  		throw e;
  926  	}
  927  	catch (...)
  928  	{
  929  
  930  	}
  931  
  932  	return ret;
  933  }
  934  
  935  std::string RetroAchievements::getCheevosHashFromFile(int consoleId, const std::string& fileName)
  936  {
  937  	LOG(LogDebug) << "getCheevosHashFromFile : " << fileName;
  938  
```


## es-app/src/RetroAchievements.cpp @ 16dbac5211: lines 1002-1072 (excerpt of 1072)

```text
 1002  	else
 1003  		ret = ApiSystem::getInstance()->getMD5(contentFile, false);
 1004  
 1005  	if (!tmpZipDirectory.empty())
 1006  		Utils::FileSystem::deleteDirectoryFiles(tmpZipDirectory, true);
 1007  
 1008  	return ret;
 1009  }
 1010  
 1011  // refused, when asked for, says whether RetroAchievements itself turned the
 1012  // account down -- it answered, and the answer was no, which is a wrong
 1013  // username or password -- as against a server that could not be reached or
 1014  // answered in a shape this does not read (#175). A caller keeping a switch
 1015  // on the player's word needs the difference: a refusal is the account's to
 1016  // fix, and anything else is tried again when the network is there.
 1017  bool RetroAchievements::testAccount(const std::string& username, const std::string& password, std::string& tokenOrError, bool* refused)
 1018  {
 1019  	if (refused != nullptr)
 1020  		*refused = false;
 1021  
 1022  	if (username.empty() || password.empty())
 1023  	{
 1024  		// Nothing to sign in with: the account is what is missing, not the network.
 1025  		if (refused != nullptr)
 1026  			*refused = true;
 1027  		tokenOrError = _("A valid account is required. Please register an account on https://retroachievements.org");
 1028  		return false;
 1029  	}
 1030  
 1031  	std::map<std::string, std::string> ret;
 1032  
 1033  	try
 1034  	{
 1035  		auto options = getHttpOptions();
 1036  
 1037  		HttpReq request("https://retroachievements.org/dorequest.php?r=login&u=" + HttpReq::urlEncode(username) + "&p=" + HttpReq::urlEncode(password), &options);
 1038  		if (!request.wait())
 1039  		{						
 1040  			tokenOrError = request.getErrorMsg();
 1041  			return false;
 1042  		}
 1043  
 1044  		rapidjson::Document ogdoc;
 1045  		ogdoc.Parse(request.getContent().c_str());
 1046  		if (ogdoc.HasParseError() || !ogdoc.HasMember("Success"))
 1047  		{
 1048  			tokenOrError = "Unable to parse response";
 1049  			return false;
 1050  		}
 1051  
 1052  		if (ogdoc["Success"].IsTrue())
 1053  		{
 1054  			if (ogdoc.HasMember("Token"))
 1055  				tokenOrError = ogdoc["Token"].GetString();
 1056  
 1057  			return true;
 1058  		}
 1059  
 1060  		// The server answered, and the answer is no.
 1061  		if (refused != nullptr)
 1062  			*refused = true;
 1063  		if (ogdoc.HasMember("Error"))
 1064  			tokenOrError = ogdoc["Error"].GetString();
 1065  	}
 1066  	catch (...)
 1067  	{
 1068  		tokenOrError = "Unknown error";
 1069  	}
 1070  
 1071  	return false;
 1072  }
```


## es-app/src/guis/GuiRetroAchievementsSettings.cpp @ 16dbac5211: lines 132-183 (excerpt of 808)

```text
  132  // once at construction is gone by the first frame (the same reason a QR
  133  // code in a row needs UntintedImageComponent, es-native-ui.md). That is
  134  // MultiLineMenuEntry::setDimmed, and for the OFFLINE ACHIEVEMENTS switch
  135  // -- dimmed while raofflineproxy-ctl is enabling or disabling on its
  136  // behalf (audit #186 PL-27) -- SwitchComponent::setDimmed: the rule first
  137  // lived in two classes here and moved into es-core so the cloud rows
  138  // share it (fork #182).
  139  
  140  static bool offlineScanOn()
  141  {
  142  	return SystemConf::getInstance()->getBool("global.retroachievements.offlineproxy");
  143  }
  144  
  145  // The cheap question, for a row built at page open: an address on any
  146  // interface. Whether RetroAchievements itself answers is the ctl's to ask
  147  // when the row is pressed -- a network round trip never runs at page build
  148  // (es-ui-style-guide.md, Gating).
  149  static bool offlineScanOnline()
  150  {
  151  	return !Utils::Platform::queryIPAddress().empty();
  152  }
  153  
  154  // The ctl's own test (raofflineproxy-ctl have_account): a user name, and
  155  // either the token the sign-in wrote or the password it will sign in with.
  156  // The scan refuses without one, and the first scan on the Retroid Pocket
  157  // Nova was pressed from the offer four seconds after the switch went on,
  158  // before any sign-in, and read COULDN'T FINISH (fork #329). So the page
  159  // asks first, in the row's words, everywhere the scan can be started.
  160  static bool offlineScanSignedIn()
  161  {
  162  	SystemConf* conf = SystemConf::getInstance();
  163  	return !conf->get("global.retroachievements.username").empty()
  164  		&& (!conf->get("global.retroachievements.token").empty() || !conf->get("global.retroachievements.password").empty());
  165  }
  166  
  167  // Whether the row is showing a run the ctl runs on its own (fork #189),
  168  // which keeps the row undimmed whatever the gates say now. A scan from this
  169  // page has its page over it for its whole length (D-UI-078), so the row
  170  // never reports one.
  171  static bool offlineScanShowsRun()
  172  {
  173  	return OfflineAchievements::runningProgress().running;
  174  }
  175  
  176  // The line under the row. A run the ctl started on its own first (fork
  177  // #189, below); else why it cannot run now, else how the last run went and
  178  // the count that is the point of the row -- longest form first, and the
  179  // row's own small font decides which fits (D-UI-035). An automatic top-up
  180  // says so in place of the date (D-UI-032).
  181  static std::string offlineScanDetail(bool on, bool online)
  182  {
  183  	const int readyNow = OfflineAchievements::readyCount();
```


## es-app/src/guis/GuiRetroAchievementsSettings.cpp @ 16dbac5211: lines 302-373 (excerpt of 808)

```text
  302  private:
  303  	std::weak_ptr<MultiLineMenuEntry> mRow;
  304  	int mElapsedMs;
  305  };
  306  
  307  // A press on the row: the reason when it cannot run, else the confirmation
  308  // (D-UI-023: what the scan does and costs is read at the moment of
  309  // deciding, with why the last one could not finish as its second paragraph,
  310  // D-UI-029), then the page. YES first, NO last so B answers NO.
  311  // The scan page itself, from the row's confirmation and from the prompt
  312  // that follows turning the switch on (D-RA-012). The refresh it is handed
  313  // runs as the scan reports, when it ends and when the page closes, so the
  314  // row's line is right the moment the page is gone.
  315  static void offlineScanStart(Window* window, std::weak_ptr<MultiLineMenuEntry> weak)
  316  {
  317  	// The ctl reads the account from system.cfg, and a name typed on the
  318  	// page below is in memory until that page closes (GuiSettings saves at
  319  	// close): written now, so a sign-in followed by a scan is not refused
  320  	// for the account the player can see on the screen (fork #329).
  321  	SystemConf::getInstance()->saveSystemConf();
  322  	window->pushGui(new GuiOfflineScan(window, "/usr/bin/raofflineproxy-ctl scan",
  323  		[weak] { offlineScanRefresh(weak); }));
  324  }
  325  
  326  static void offlineScanPressed(Window* window, std::weak_ptr<MultiLineMenuEntry> weak)
  327  {
  328  	if (!offlineScanOn())
  329  	{
  330  		window->pushGui(new GuiMsgBox(window, _("TURN ON OFFLINE ACHIEVEMENTS FIRST."), _("OK")));
  331  		return;
  332  	}
  333  	if (!offlineScanSignedIn())
  334  	{
  335  		window->pushGui(new GuiMsgBox(window, _("SIGN IN TO RETROACHIEVEMENTS FIRST."), _("OK")));
  336  		return;
  337  	}
  338  	if (!offlineScanOnline())
  339  	{
  340  		window->pushGui(new GuiMsgBox(window, _("YOU'RE NOT ONLINE. TRY AGAIN WHEN YOU'RE ONLINE."), _("OK")));
  341  		return;
  342  	}
  343  
  344  	std::string text = _("SCAN GAMES FOR OFFLINE ACHIEVEMENTS?") + std::string("\n\n")
  345  		+ _("THIS LOOKS AT EVERY GAME ON THIS CONSOLE AND SAVES ITS ACHIEVEMENT DATA SO ACHIEVEMENTS CAN BE EARNED WHILE OFFLINE. THIS CAN TAKE A WHILE FOR A LARGE LIBRARY.");
  346  	const CloudText::ScanStamp last = OfflineAchievements::lastScan();
  347  	// A cancelled run is not one that could not finish (D-UI-078): nothing
  348  	// to explain, the next scan carries on.
  349  	if (last.ran && last.code != 0 && !last.why.empty() && last.why != "CANCELLED")
  350  	{
  351  		// The why as a clause, then a full stop -- unless the why is a
  352  		// sentence already (SOME GAMES COULDN'T BE SAVED. TRY THE SCAN
  353  		// AGAIN.), which brings its own.
  354  		const std::string why = OfflineAchievements::scanWhy(last.why);
  355  		text += "\n\n" + _("LAST TIME IT COULDN'T FINISH:") + " " + why
  356  			+ (Utils::String::endsWith(why, ".") ? "" : ".");
  357  	}
  358  
  359  	window->pushGui(new GuiMsgBox(window, text,
  360  		_("YES"), [window, weak] { offlineScanStart(window, weak); },
  361  		_("NO"), nullptr));
  362  }
  363  
  364  static std::shared_ptr<MultiLineMenuEntry> addOfflineScanRow(GuiSettings* s, Window* window)
  365  {
  366  	// The line goes in at construction: ComponentList sizes the row from the
  367  	// entry as it is added, and an entry made with no substring is one line
  368  	// tall for good -- a description set afterwards hangs below the row's
  369  	// slot, under the selector bar (frame 02 of the first 640x480 run).
  370  	// Later refreshes only change the words, so the height holds.
  371  	const bool on = offlineScanOn();
  372  	const bool online = offlineScanOnline();
  373  	auto entry = std::make_shared<MultiLineMenuEntry>(window, _("SCAN GAMES FOR OFFLINE ACHIEVEMENTS"),
```


## es-app/src/guis/GuiRetroAchievementsSettings.cpp @ 16dbac5211: lines 432-568 (excerpt of 808)

```text
  432  	addSpacerRow(s, window, 1.0f);
  433  	addInfoRow(s, window, offlineInfoFirst(), offlineInfoFirst());
  434  	addSpacerRow(s, window, 0.5f);
  435  	std::weak_ptr<TextComponent> infoRow = addInfoRow(s, window,
  436  		offlineInfoSecond(Settings::CheevosCheckIndexesAtStart()), offlineInfoSecond(true));
  437  
  438  	// Weak on purpose: the callback lives inside the switch it names, so a
  439  	// shared_ptr here would be a cycle that keeps the page alive forever --
  440  	// and the ctl's answer arrives from a thread after the page may have
  441  	// been closed. setState fires the change callback too, so a revert made
  442  	// from inside it would re-enter it: quiet while the code, not the
  443  	// player, sets the state.
  444  	std::weak_ptr<SwitchComponent> offlineWeak = offline;
  445  	auto quiet = std::make_shared<bool>(false);
  446  	auto setQuietly = [offlineWeak, quiet](bool state)
  447  	{
  448  		if (auto sw = offlineWeak.lock())
  449  		{
  450  			*quiet = true;
  451  			sw->setState(state);
  452  			*quiet = false;
  453  		}
  454  	};
  455  
  456  	// The ctl runs from a thread of its own (audit #186 PL-27): disable
  457  	// waits on systemctl stop, up to the unit's fifteen seconds, and the
  458  	// interface thread never blocks on a process (es-native-ui.md). While it
  459  	// runs the switch is dimmed and refuses a second press; the rows are set
  460  	// from the ctl's answer on the interface thread (postToUiThread), the
  461  	// pattern sayAfterGame uses. Every row is held weakly: the player may
  462  	// have left the page, or the page below it, before the answer comes,
  463  	// and each row that is gone is simply not set -- system.cfg already
  464  	// holds what the ctl wrote, and the page below saves only what changed.
  465  	auto pending = std::make_shared<bool>(false);
  466  	auto apply = [window, offlineWeak, hardcoreRow, indexRow, infoRow, setQuietly, scanRow, pending](bool on)
  467  	{
  468  		if (*pending)
  469  			return;
  470  		*pending = true;
  471  		if (auto sw = offlineWeak.lock())
  472  			sw->setDimmed(true);
  473  
  474  		std::thread([window, on, offlineWeak, hardcoreRow, indexRow, infoRow, setQuietly, scanRow, pending]
  475  		{
  476  			std::string last;
  477  			// executeScriptLegacy: the public route that hands back the real
  478  			// exit status and every line, as the cloud pages use it.
  479  			auto result = ApiSystem::executeScriptLegacy(std::string("/usr/bin/raofflineproxy-ctl ") + (on ? "enable" : "disable") + " 2>/dev/null",
  480  				[&last](const std::string line) { last = line; });
  481  			const bool ok = result.second == 0 && Utils::String::startsWith(last, "hardcore=");
  482  			const bool hardcoreNow = (last == "hardcore=1");
  483  
  484  			window->postToUiThread([window, on, ok, hardcoreNow, offlineWeak, hardcoreRow, indexRow, infoRow, setQuietly, scanRow, pending]
  485  			{
  486  				*pending = false;
  487  				if (auto sw = offlineWeak.lock())
  488  					sw->setDimmed(false);
  489  
  490  				if (!ok)
  491  				{
  492  					setQuietly(!on);
  493  					window->pushGui(new GuiMsgBox(window,
  494  						on ? _("OFFLINE ACHIEVEMENTS COULDN'T BE TURNED ON.") : _("OFFLINE ACHIEVEMENTS COULDN'T BE TURNED OFF."),
  495  						_("OK"), nullptr, GuiMsgBoxIcon::ICON_ERROR));
  496  					return;
  497  				}
  498  				if (auto row = hardcoreRow.lock())
  499  					row->setState(hardcoreNow);
  500  				SystemConf::getInstance()->set("global.retroachievements.offlineproxy", on ? "1" : "0");
  501  				SystemConf::getInstance()->set("global.retroachievements.hardcore", hardcoreNow ? "1" : "0");
  502  				// The scan row reads the switch: on, it offers the scan; off, it
  503  				// says to turn the switch on first.
  504  				offlineScanRefresh(scanRow);
  505  
  506  				// The cache follows the index (D-RA-013), and the index is off
  507  				// by default: turning the switch on turns INDEX NEW GAMES AT
  508  				// STARTUP on as well, said in the confirmation above (audit
  509  				// #186 PL-06). Saved here, not left to the page below: its save
  510  				// writes the row's state, so the row is set too where it is
  511  				// still there, and a page already closed has already saved.
  512  				// The block of text gains its last sentence now that it is
  513  				// true. Turning the switch off leaves the setting as it is --
  514  				// an index is the player's, and costs nothing offline.
  515  				if (on && !Settings::CheevosCheckIndexesAtStart())
  516  				{
  517  					Settings::getInstance()->setBool("CheevosCheckIndexesAtStart", true);
  518  					Settings::getInstance()->saveFile();
  519  					if (auto row = indexRow->lock())
  520  						row->setState(true);
  521  					if (auto info = infoRow.lock())
  522  						info->setText(offlineInfoSecond(true));
  523  				}
  524  
  525  				// Turning it on offers the scan at once (D-RA-012): without it a
  526  				// player who skips the row plays offline with nothing cached.
  527  				// Offline, one line says when to come back to it.
  528  				if (on)
  529  				{
  530  					if (!offlineScanSignedIn())
  531  					{
  532  						// No account yet: the scan would be refused (fork #329),
  533  						// so say the order of things instead of offering it.
  534  						window->pushGui(new GuiMsgBox(window,
  535  							_("SIGN IN TO RETROACHIEVEMENTS FIRST.") + std::string(" ") + _("THEN SCAN GAMES FOR OFFLINE ACHIEVEMENTS, SO ACHIEVEMENTS CAN BE EARNED WHILE OFFLINE."),
  536  							_("OK")));
  537  					}
  538  					else if (offlineScanOnline())
  539  					{
  540  						std::string text = _("SCAN GAMES FOR OFFLINE ACHIEVEMENTS NOW?") + std::string("\n\n")
  541  							+ _("THIS LOOKS AT EVERY GAME ON THIS CONSOLE AND SAVES ITS ACHIEVEMENT DATA SO ACHIEVEMENTS CAN BE EARNED WHILE OFFLINE. THIS CAN TAKE A WHILE FOR A LARGE LIBRARY.");
  542  						window->pushGui(new GuiMsgBox(window, text,
  543  							_("SCAN NOW"), [window, scanRow] { offlineScanStart(window, scanRow); },
  544  							_("LATER"), nullptr));
  545  					}
  546  					else
  547  					{
  548  						window->pushGui(new GuiMsgBox(window,
  549  							_("YOU'RE NOT ONLINE. SCAN GAMES FOR OFFLINE ACHIEVEMENTS WHEN YOU'RE CONNECTED, SO ACHIEVEMENTS CAN BE EARNED WHILE OFFLINE."),
  550  							_("OK")));
  551  					}
  552  				}
  553  			});
  554  		}).detach();
  555  	};
  556  
  557  	offline->setOnChangedCallback([window, offlineWeak, quiet, setQuietly, apply, pending]
  558  	{
  559  		if (*quiet)
  560  			return;
  561  		auto sw = offlineWeak.lock();
  562  		if (!sw)
  563  			return;
  564  
  565  		// A press while the ctl is still at work on the last one: the switch
  566  		// goes back to the state the ctl is making, and nothing else happens.
  567  		if (*pending)
  568  		{
```


## es-app/src/guis/GuiRetroAchievementsSettings.cpp @ 16dbac5211: lines 588-648 (excerpt of 808)

```text
  588  			_("TURN ON"), [apply] { apply(true); },
  589  			_("NOT NOW"), [setQuietly] { setQuietly(false); }));
  590  	});
  591  
  592  	window->pushGui(s);
  593  }
  594  #endif
  595  
  596  GuiRetroAchievementsSettings::GuiRetroAchievementsSettings(Window* window) : GuiSettings(window, _("RETROACHIEVEMENTS SETTINGS").c_str())
  597  {
  598  	addGroup(_("SETTINGS"));
  599  
  600  	bool retroachievementsEnabled = SystemConf::getInstance()->getBool("global.retroachievements");
  601  	std::string username = SystemConf::getInstance()->get("global.retroachievements.username");
  602  	std::string password = SystemConf::getInstance()->get("global.retroachievements.password");
  603  
  604  	// retroachievements_enable
  605  	auto retroachievements_enabled = std::make_shared<SwitchComponent>(mWindow);
  606  	retroachievements_enabled->setState(retroachievementsEnabled);
  607  	addWithLabel(_("RETROACHIEVEMENTS"), retroachievements_enabled);
  608  	
  609  	// retroachievements, username, password
  610  	addInputTextConfigRow(_("USERNAME"), "global.retroachievements.username", false);
  611  	addInputTextConfigRow(_("PASSWORD"), "global.retroachievements.password", true);
  612  #ifndef CHEEVOS_DEV_LOGIN
  613  	// A fork build compiles no developer pair in, so the menu pages authenticate
  614  	// with the player's own web API key, from the account's settings page on
  615  	// retroachievements.org (#68). Held back from backups like the password.
  616  	addInputTextConfigRow(_("WEB API KEY"), "global.retroachievements.key", true);
  617  #endif
  618  
  619  	addGroup(_("OPTIONS"));
  620  
  621  	auto hardcore = addSwitch(_("HARDCORE MODE"), _("Disable loading states, rewind and cheats for more points."), "global.retroachievements.hardcore", false, nullptr);
  622  
  623  #if defined(ROCKNIX)
  624  	// OFFLINE ACHIEVEMENTS: a row that opens a page (D-RA-003; es-player-text
  625  	// "A row that leads somewhere is a label"). The switch and what it means
  626  	// need more room than one line under a row gives them on a 3.5" panel,
  627  	// so the row carries the label and one short line -- sentence case like
  628  	// every description on this page (#166) -- and the page carries the
  629  	// switch with the explanation beside it. Shown only where the backend
  630  	// is: an image without the package has no toggle to offer.
  631  	// indexRow is filled once the GAME INDEXES rows exist, below.
  632  	auto indexRow = std::make_shared<std::weak_ptr<SwitchComponent>>();
  633  	if (Utils::FileSystem::exists("/usr/bin/raofflineproxy-ctl"))
  634  	{
  635  		std::weak_ptr<SwitchComponent> hardcoreRow = hardcore;
  636  		addWithDescription(_("OFFLINE ACHIEVEMENTS (BETA)"), _("Casual achievements only."), makeArrow(mWindow),
  637  			[window, hardcoreRow, indexRow] { openOfflineAchievements(window, hardcoreRow, indexRow); }, "", false, true);
  638  	}
  639  #endif
  640  	addSwitch(_("LEADERBOARDS"), _("Compete in high-score and best time leaderboards (requires hardcore)."), "global.retroachievements.leaderboards", false, nullptr);
  641  	addSwitch(_("VERBOSE MODE"), _("Show achievement progression on game launch and other notifications."), "global.retroachievements.verbose", false, nullptr);
  642  	addSwitch(_("RICH PRESENCE"), "global.retroachievements.richpresence", false);
  643  	addSwitch(_("ENCORE MODE"), _("Unlocked achievements can be earned again."), "global.retroachievements.encore", false, nullptr);
  644  	addSwitch(_("AUTOMATIC SCREENSHOT"), _("Automatically take a screenshot when an achievement is earned."), "global.retroachievements.screenshot", false, nullptr);
  645  	addSwitch(_("CHALLENGE INDICATORS"), _("Shows icons in the bottom right corner when eligible achievements can be earned."), "global.retroachievements.challenge_indicators", false, nullptr);
  646  	// RetroArch's progress tracker is a separate widget from the challenge
  647  	// indicators -- it counts measured progress (34/99 rings) while an
  648  	// indicator marks a live "do X without Y" achievement -- and it had no
```


## es-app/src/guis/GuiRetroAchievementsSettings.cpp @ 16dbac5211: lines 682-808 (excerpt of 808)

```text
  682                  // Enable LED Notifications
  683                  auto cheevos_led_enabled = std::make_shared<SwitchComponent>(mWindow);
  684                  bool cheevosledenabled = SystemConf::getInstance()->get("global.retroachievements.leds") == "1";
  685                  cheevos_led_enabled->setState(SystemConf::getInstance()->getBool("global.retroachievements.leds"));
  686                  //s->addWithLabel(_("LED NOTIFICATIONS"), cheevos_led_enabled);
  687                  addWithLabel(_("LED NOTIFICATIONS"), cheevos_led_enabled);
  688                  cheevos_led_enabled->setOnChangedCallback([cheevos_led_enabled] {
  689                          bool cheevosledenabled = cheevos_led_enabled->getState();
  690                                  SystemConf::getInstance()->set("global.retroachievements.leds", cheevosledenabled ? "1" : "0");
  691                  });
  692          }
  693  #endif
  694  	// retroachievements_hardcore_mode
  695  	addSwitch(_("SHOW RETROACHIEVEMENTS ENTRY IN MAIN MENU"), _("View your RetroAchievements stats right from the main menu!"), "RetroachievementsMenuitem", true, nullptr);
  696  
  697  	addGroup(_("GAME INDEXES"));
  698  	// With OFFLINE ACHIEVEMENTS on, the index feeds the offline cache (fork
  699  	// #184, D-RA-013): as the hasher finishes, the games it identified are
  700  	// cached for offline play from their id and hash, and a game the index
  701  	// does not know is not cached at all. Maintainer: "we need to be clear
  702  	// that scanning for retro achievements [...] will cache new games
  703  	// discovered as well [...] perhaps even changing the text of that option
  704  	// when offline achievements are enabled." So each row says so in one
  705  	// line while the switch is on (D-UI-023), and reads as upstream's when
  706  	// it is off. Read at page build: the switch lives on the page below,
  707  	// and this page is built again on the way back to it.
  708  	bool indexFeedsOffline = false;
  709  #if defined(ROCKNIX)
  710  	indexFeedsOffline = OfflineAchievements::available() && OfflineAchievements::toggleOn();
  711  #endif
  712  	auto indexAtStartup = addSwitch(_("INDEX NEW GAMES AT STARTUP"),
  713  		indexFeedsOffline ? _("Also saves new games' achievement data for offline play.") : std::string(),
  714  		"CheevosCheckIndexesAtStart", true, nullptr);
  715  #if defined(ROCKNIX)
  716  	*indexRow = indexAtStartup;
  717  #endif
  718  	auto indexGames = [this]
  719  	{
  720  		if (ThreadedHasher::checkCloseIfRunning(mWindow))
  721  			mWindow->pushGui(new GuiHashStart(mWindow, ThreadedHasher::HASH_CHEEVOS_MD5));
  722  	};
  723  	if (indexFeedsOffline)
  724  		addWithDescription(_("INDEX GAMES"), _("Also saves their achievement data for offline play."), makeArrow(mWindow), indexGames, "", false, true);
  725  	else
  726  		addEntry(_("INDEX GAMES"), true, indexGames);
  727  
  728  	// The switch is the player's choice, and this save writes that choice
  729  	// and nothing else (#175). The sign-in below decides the token only. It
  730  	// used to decide the switch as well: a sign-in that failed because the
  731  	// device was offline -- this page closed on a boot whose first attempt
  732  	// had run before the network was up, so no token was there to skip it
  733  	// -- wrote the switch off, and the RETROACHIEVEMENTS entry left the
  734  	// main menu with nothing on screen to say why.
  735  	//
  736  	// What the player is told depends on why it failed and on what they
  737  	// did. RetroAchievements turned the account down: said every time, the
  738  	// credentials are wrong and no retry changes that. RetroAchievements
  739  	// could not be reached after the switch was turned on or the account
  740  	// changed: said once, with what happens next. Could not be reached and
  741  	// nothing was changed: nothing to say -- the sign-in that runs when the
  742  	// network comes up (NetworkThread) finishes this on its own.
  743  	addSaveFunc([retroachievementsEnabled, retroachievements_enabled, username, password, window]
  744  	{
  745  		bool newState = retroachievements_enabled->getState();
  746  		std::string newUsername = SystemConf::getInstance()->get("global.retroachievements.username");
  747  		std::string newPassword = SystemConf::getInstance()->get("global.retroachievements.password");
  748  		std::string token = SystemConf::getInstance()->get("global.retroachievements.token");
  749  
  750  		bool accountChanged = !retroachievementsEnabled || username != newUsername || password != newPassword;
  751  		// On the interface thread only for a change the player made and an
  752  		// address to send it from (#308 1-raoffline claude F-RA-19): nothing
  753  		// changed and no token was a sign-in at every close while offline,
  754  		// the screen waiting on the request -- its connect timeout on a
  755  		// hotspot with a route and no DNS (#242). That case is the token
  756  		// check's, on the watchers' thread, which retries when the network
  757  		// comes up; CheevosRetry::saveSignIn decides.
  758  		const CheevosRetry::SaveSignIn signIn = CheevosRetry::saveSignIn(newState, accountChanged, token.empty(),
  759  			!Utils::Platform::queryIPAddress().empty());
  760  		if (signIn == CheevosRetry::SaveSignIn::InBackground)
  761  			LOG(LogInfo) << "retroachievements: no token; the token check is asked to sign in, off the interface thread";
  762  		else if (signIn == CheevosRetry::SaveSignIn::Offline)
  763  		{
  764  			// The account changed and there is nowhere to send it from: the
  765  			// old token is not this account's, and the answer is the one a
  766  			// request would have come back with, without the wait.
  767  			SystemConf::getInstance()->set("global.retroachievements.token", "");
  768  			window->pushGui(new GuiMsgBox(window,
  769  				_("COULDN'T REACH RETROACHIEVEMENTS TO SIGN YOU IN.\n\nRETROACHIEVEMENTS STAYS ON. IT'LL SIGN IN WHEN YOU'RE ONLINE."),
  770  				_("OK")));
  771  		}
  772  		else if (signIn == CheevosRetry::SaveSignIn::Now)
  773  		{
  774  			std::string tokenOrError;
  775  			bool refused = false;
  776  			if (RetroAchievements::testAccount(newUsername, newPassword, tokenOrError, &refused))
  777  				SystemConf::getInstance()->set("global.retroachievements.token", tokenOrError);
  778  			else
  779  			{
  780  				SystemConf::getInstance()->set("global.retroachievements.token", "");
  781  
  782  				if (refused)
  783  					window->pushGui(new GuiMsgBox(window,
  784  						_("RETROACHIEVEMENTS DIDN'T ACCEPT YOUR SIGN-IN:") + "\n" + tokenOrError + "\n\n"
  785  						+ _("RETROACHIEVEMENTS STAYS ON. CHECK YOUR USERNAME AND PASSWORD, THEN TRY AGAIN."),
  786  						_("OK"), nullptr, GuiMsgBoxIcon::ICON_ERROR));
  787  				else if (accountChanged)
  788  					window->pushGui(new GuiMsgBox(window,
  789  						_("COULDN'T REACH RETROACHIEVEMENTS TO SIGN YOU IN.\n\nRETROACHIEVEMENTS STAYS ON. IT'LL SIGN IN WHEN YOU'RE ONLINE."),
  790  						_("OK")));
  791  				else
  792  					LOG(LogWarning) << "retroachievements: could not reach RetroAchievements for a token (" << tokenOrError << "); the switch stays as set, and the sign-in runs when the network is up";
  793  			}
  794  		}
  795  		else if (!newState)
  796  			SystemConf::getInstance()->set("global.retroachievements.token", "");
  797  
  798  		if (SystemConf::getInstance()->setBool("global.retroachievements", newState))
  799  			if (!ThreadedHasher::isRunning() && newState)
  800  				ThreadedHasher::start(window, ThreadedHasher::HASH_CHEEVOS_MD5, false, true);
  801  
  802  		// After the switch is written: the check reads it, and one that ran
  803  		// before a switch just turned on would find it off and do nothing
  804  		// -- nor retry when the network comes up.
  805  		if (signIn == CheevosRetry::SaveSignIn::InBackground || signIn == CheevosRetry::SaveSignIn::Offline)
  806  			NetworkThread::checkCheevosTokenSoon();
  807  	});
  808  }
```


## es-app/src/guis/GuiRetroAchievements.cpp @ 16dbac5211: lines 36-52 (excerpt of 471)

```text
   36  		[window](auto gui)
   37  		{
   38  			auto summary = RetroAchievements::getUserSummary();
   39  			return RetroAchievements::toRetroAchivementInfo(summary);
   40  		}, 
   41  		[window](RetroAchievementInfo ra)
   42  		{
   43  			if (ra.username.empty() && !ra.error.empty())
   44  				window->pushGui(new GuiMsgBox(window, _("AN ERROR OCCURRED") + "\r\n" + ra.error, _("OK")));
   45  			else if (ra.username.empty())
   46  				window->pushGui(new GuiMsgBox(window, _("AN ERROR OCCURRED"), _("OK")));
   47  			else
   48  				window->pushGui(new GuiRetroAchievements(window, ra));
   49  		}));
   50  }
   51  
   52  RetroAchievementProgress::RetroAchievementProgress(Window* window, int valueSoftcore, int valueHardcore, int max, const std::string& label) : GuiComponent(window),
```


## es-app/src/guis/GuiRetroAchievements.cpp @ 16dbac5211: lines 326-342 (excerpt of 471)

```text
  326  
  327  	std::shared_ptr<WebImageComponent> mImage;
  328  	std::shared_ptr<CarouselItemTemplate> mItemTemplate;
  329  		
  330  	RetroAchievementGame mGameInfo;
  331  };
  332  
  333  GuiRetroAchievements::GuiRetroAchievements(Window* window, RetroAchievementInfo ra) : 
  334  	GuiSettings(window, _("RETROACHIEVEMENTS") + " - " + ra.username, "", nullptr)
  335  {
  336  	// Required for WebImageComponent
  337  	setUpdateType(ComponentListFlags::UPDATE_ALWAYS);
  338  
  339  	if (!ra.error.empty())
  340  	{
  341  		setSubTitle(ra.error);
  342  		return;
```


## es-app/src/guis/GuiGameAchievements.cpp @ 16dbac5211: lines 32-48 (excerpt of 352)

```text
   32  	},
   33  		[window](GameInfoAndUserProgress ra)
   34  	{
   35  		// Offline, and the proxy has never cached this game: not an error,
   36  		// and not an empty page -- the one line that says what makes it
   37  		// viewable (#180). The row that does it is named as the cards name
   38  		// theirs (es-player-text.md, Recover).
   39  		if (ra.NotOnDevice)
   40  			window->pushGui(new GuiMsgBox(window, _("YOU'RE NOT ONLINE, AND THIS GAME'S ACHIEVEMENTS AREN'T SAVED ON THIS DEVICE YET. SCAN GAMES FOR OFFLINE ACHIEVEMENTS, OR START THE GAME ONCE WHILE YOU'RE CONNECTED."), _("OK")));
   41  		else if (ra.ID == 0 && !ra.Title.empty())
   42  			window->pushGui(new GuiMsgBox(window, _("AN ERROR OCCURRED") + "\r\n" + ra.Title, _("OK")));
   43  		else if (ra.ID == 0)
   44  			window->pushGui(new GuiMsgBox(window, _("AN ERROR OCCURRED"), _("OK")));
   45  		else
   46  			window->pushGui(new GuiGameAchievements(window, ra));
   47  	}));
   48  }
```


## es-app/src/OfflineScanJob.h @ 16dbac5211: lines 1-100 (excerpt of 100)

```text
    1  #pragma once
    2  #ifndef ES_APP_OFFLINE_SCAN_JOB_H
    3  #define ES_APP_OFFLINE_SCAN_JOB_H
    4  
    5  #include <atomic>
    6  #include <chrono>
    7  #include <functional>
    8  #include <memory>
    9  #include <mutex>
   10  #include <string>
   11  #include <sys/types.h>
   12  
   13  class Window;
   14  
   15  // One run of raofflineproxy-ctl scan (fork #179, D-RA-010), apart from the
   16  // page that shows it (GuiOfflineScan). The run is a thread of its own
   17  // reading the ctl's stdout -- ">>> " lines, the header of raofflineproxy-ctl
   18  // is the contract -- into the state below, and it keeps itself alive (the
   19  // thread holds the shared_ptr) until the ctl exits. One run at a time:
   20  // start() hands back the run in flight when there is one, as the ctl itself
   21  // would refuse a second (exit 75).
   22  //
   23  // The page sits on the run for its length (D-UI-078, #241): the one way out
   24  // while it runs is CANCEL, which is cancel() here -- the ctl gets SIGINT,
   25  // traps it as the player's cancel, stamps the run and exits 130; what it
   26  // saved stays saved, and the next scan passes over those games. For a week
   27  // (audit #186 PL-07) the page could be left and the run went on in the
   28  // background, reported only on the row that launched it; the maintainer met
   29  // that prompt on the device and asked what would happen, and the honest
   30  // answer was "nothing tells you".
   31  class OfflineScanJob : public std::enable_shared_from_this<OfflineScanJob>
   32  {
   33  public:
   34  	struct State
   35  	{
   36  		bool listing = false;     // ">>> doing listing": the library is being walked
   37  		int total = 0;            // ">>> total n" / the n of ">>> game i|n|name"
   38  		int index = 0;            // the i
   39  		std::string game;         // the name
   40  		int cached = 0, skipped = 0, ready = -1;
   41  		int errors = 0;           // ">>> errors n": games a fetch failed for (audit #186 PL-24)
   42  		bool limit = false, nothingNew = false;
   43  		bool truncated = false;   // ">>> note TRUNCATED": the walk stopped at the client's cap of files
   44  		bool noGames = false;     // ">>> note NO_GAMES": nothing under the ROM folders to look at (fork #329)
   45  		std::string why;          // the ctl's token
   46  		bool cancelled = false;   // cancel(): the player's word for the outcome, whatever the exit
   47  		bool finished = false;
   48  		int exit = -1;
   49  		int elapsedMs = 0;        // since the run began; frozen once finished
   50  	};
   51  
   52  	// The run in flight or the last one this session; null when none has run.
   53  	static std::shared_ptr<OfflineScanJob> current();
   54  	// Whether a run is in flight.
   55  	static bool running();
   56  	// Start a run of command, or hand back the one in flight.
   57  	static std::shared_ptr<OfflineScanJob> start(Window* window, const std::string& command);
   58  
   59  	State state() const;
   60  	const std::string& command() const { return mCommand; }
   61  
   62  	// The player's CANCEL (D-UI-078): SIGINT to the run's process group --
   63  	// the shell, the ctl and its helper together -- and the state marked
   64  	// cancelled, so the page words the outcome as the player's choice and
   65  	// not as a failure. The ctl's INT trap writes the stamp. Nothing to do
   66  	// once the run has ended.
   67  	void cancel();
   68  
   69  	// Run on the interface thread whenever the run's state changes and once
   70  	// when it ends -- at most one waiting at a time -- so the row that
   71  	// offered the scan can follow it with no page open. The page sets it on
   72  	// attach; the last setter wins.
   73  	void setOnChanged(const std::function<void()>& onChanged);
   74  
   75  private:
   76  	OfflineScanJob(Window* window, const std::string& command);
   77  	// The thread that runs it holds the job (start()), so nothing here does.
   78  	void run();
   79  	void handleLine(const std::string& line);
   80  	void changed();
   81  	static std::string cleanLine(const std::string& raw);
   82  
   83  	Window* mWindow;
   84  	std::string mCommand;
   85  	mutable std::mutex mMutex;
   86  	State mState;
   87  	// The command's process group (run() starts it under setsid and reads
   88  	// its ">>> pid N" first line), for cancel(). A cancel that arrives before
   89  	// the line has (mCancelWanted) is delivered when it does.
   90  	std::atomic<pid_t> mPid{0};
   91  	bool mCancelWanted = false;
   92  	std::chrono::steady_clock::time_point mStarted;
   93  	std::function<void()> mOnChanged;
   94  	bool mPostPending = false;   // a changed() already waits on the interface thread
   95  
   96  	static std::mutex sMutex;
   97  	static std::shared_ptr<OfflineScanJob> sCurrent;
   98  };
   99  
  100  #endif // ES_APP_OFFLINE_SCAN_JOB_H
```


## es-app/src/ThreadedHasher.h @ 16dbac5211: lines 1-76 (excerpt of 76)

```text
    1  #pragma once
    2  
    3  #include <thread>
    4  #include <queue>
    5  #include <set>
    6  #include <unordered_set>
    7  #include <vector>
    8  #include "components/AsyncNotificationComponent.h"
    9  
   10  class FileData;
   11  
   12  class ThreadedHasher
   13  {
   14  public:
   15  	enum HasherType : unsigned int
   16  	{
   17  		HASH_NETPLAY_CRC = 1,
   18  		HASH_CHEEVOS_MD5 = 2,
   19  		HASH_ALL = HASH_NETPLAY_CRC | HASH_CHEEVOS_MD5,
   20  	};
   21  
   22  	static void start(Window* window, HasherType type, bool forceAllGames=false, bool silent=false, std::set<std::string>* systems = nullptr);
   23  	static void stop();
   24  	static bool isRunning() { return mInstance != nullptr; }
   25  	// Whether a run this session got RetroAchievements' hash library. The
   26  	// network watcher starts the startup index again at link-up until one has
   27  	// (fork #183); a run without the library indexes nothing.
   28  	static bool cheevosLibraryCameThisSession() { return sCheevosLibraryCame; }
   29  	static bool checkCloseIfRunning(Window* window);
   30  
   31  	static void pause() { mPaused = true; }
   32  	static void resume() { mPaused = false; }
   33  
   34  private:
   35  	// lookupOnly: the games with a cheevosHash and no cheevosId (CheevosIndex::Take::Lookup).
   36  	// Those whose hash the library knows join the queue once it has come; none is read.
   37  	ThreadedHasher(Window* window, HasherType type, std::queue<FileData*> searchQueue, const std::vector<FileData*>& lookupOnly, bool forceAllGames = false);
   38  	~ThreadedHasher();
   39  
   40  	void updateUI(const std::string label);
   41  	static std::string formatGameName(FileData* game);
   42  
   43  	std::queue<FileData*> mSearchQueue;
   44  	// The queued games that are here for a lookup alone: no hash, no CRC is
   45  	// read for them. Filled in the constructor, read by the threads, never
   46  	// written again, so it needs no lock.
   47  	std::unordered_set<FileData*> mLookupOnly;
   48  
   49  	Window* mWindow;
   50  	AsyncNotificationComponent* mWndNotification;
   51  	std::string		mCurrentAction;
   52  
   53  	std::vector<std::string> mErrors;
   54  	std::map<std::string, std::string>    mCheevosHashes;
   55  
   56  	HasherType mType;
   57  
   58  	void run();
   59  
   60  	//std::thread* mHandle;
   61  	std::vector<std::thread*>	mThreads;
   62  	int							mThreadCount;
   63  
   64  	int mTotal;
   65  	bool mExit;
   66  	bool mForce;
   67  	// Whether this run identified games at all: RetroAchievements' hash
   68  	// library came and there was something to hash. Only then does the
   69  	// offline cache have a reason to follow it (fork #184, D-RA-013).
   70  	bool mCheevosIndexed;
   71  
   72  	static bool mPaused;
   73  	static ThreadedHasher* mInstance;
   74  	static bool sCheevosLibraryCame;
   75  };
   76  
```


## es-app/src/ApiSystem.cpp @ 16dbac5211: lines 2254-2301 (excerpt of 3519)

```text
 2254  
 2255  std::vector<std::string> ApiSystem::executeScriptLegacy(const std::string& command) {
 2256  	std::vector<std::string> vec;
 2257  	executeScriptLegacy(command, [&vec](const std::string& line) {
 2258  		vec.push_back(line);
 2259  	});
 2260  	return vec;
 2261  }
 2262  
 2263  std::pair<std::string, int> ApiSystem::executeScriptLegacy(const std::string& command, const std::function<void(const std::string)>& func)
 2264  {
 2265  	const std::string shown = Utils::String::maskSecrets(command);
 2266  	std::cout << "ApiSystem::executeScriptLegacy -> " << shown << std::endl;
 2267  	LOG(LogInfo) << "ApiSystem::executeScriptLegacy -> " << shown;
 2268  
 2269  	FILE *pipe = popen(command.c_str(), "r");
 2270  	if (pipe == NULL)
 2271  	{
 2272  		LOG(LogError) << "Error executing " << shown;
 2273  		return std::pair<std::string, int>("Error starting command : " + shown, -1);
 2274  	}
 2275  
 2276  	std::stringstream output_stream;
 2277  	char buff[1024];
 2278  	while (fgets(buff, 1024, pipe))
 2279  	{
 2280  		std::stringstream output_stream(buff);
 2281  		std::string line;
 2282  		while (getline(output_stream, line).good()) {
 2283  			if (line.empty()) continue;
 2284  			std::cout << line << std::endl;
 2285  			if (func != nullptr) {
 2286  				func(std::string(line));
 2287  			}
 2288  		}
 2289  	}
 2290  
 2291  	int exitCode = WEXITSTATUS(pclose(pipe));
 2292  	return std::pair<std::string, int>("", exitCode);
 2293  }
 2294  
 2295  std::pair<std::string, int> ApiSystem::executeScript(const std::string command, const std::function<void(const std::string)>& func)
 2296  {
 2297  	const std::string shown = Utils::String::maskSecrets(command);
 2298  	LOG(LogInfo) << "ApiSystem::executeScript -> " << shown;
 2299  
 2300  	FILE *pipe = popen(command.c_str(), "r");
 2301  	if (pipe == NULL)
```


## es-core/src/HttpReq.cpp @ 16dbac5211: lines 162-248 (excerpt of 644)

```text
  162  	}
  163  #endif
  164  
  165  	if (options != nullptr && !options->dataToPost.empty())
  166  	{
  167  		curl_easy_setopt(mHandle, CURLOPT_POST, 1L);
  168  		curl_easy_setopt(mHandle, CURLOPT_POSTFIELDSIZE, options->dataToPost.length());
  169  		curl_easy_setopt(mHandle, CURLOPT_COPYPOSTFIELDS, options->dataToPost.c_str());
  170  	}
  171  
  172  	if (options != nullptr && options->customHeaders.size() > 0)
  173  	{
  174  		struct curl_slist *hs = nullptr;
  175  
  176  		for (auto header : options->customHeaders)
  177  			hs = curl_slist_append(hs, header.c_str());
  178  
  179  		curl_easy_setopt(mHandle, CURLOPT_HTTPHEADER, hs);
  180  	}
  181  
  182  	//set curl to handle redirects
  183  	err = curl_easy_setopt(mHandle, CURLOPT_FOLLOWLOCATION, 1L);
  184  	if(err != CURLE_OK)
  185  	{
  186  		mStatus = REQ_IO_ERROR;
  187  		onError(curl_easy_strerror(err));
  188  		return;
  189  	}
  190  
  191  	// Ignore expired SSL certificates
  192  	curl_easy_setopt(mHandle, CURLOPT_SSL_VERIFYPEER, 0L);
  193  
  194  	// Add client cert support
  195  	if (options != nullptr && !options->clientCert.empty() && !options->clientKey.empty()) {
  196  		// curl_easy_setopt(mHandle, CURLOPT_VERBOSE, 1L);
  197  		curl_easy_setopt(mHandle, CURLOPT_SSLCERT, options->clientCert.c_str());
  198  		curl_easy_setopt(mHandle, CURLOPT_SSLCERTTYPE, "PEM");
  199  		curl_easy_setopt(mHandle, CURLOPT_SSLKEY, options->clientKey.c_str());
  200  		curl_easy_setopt(mHandle, CURLOPT_SSL_VERIFYHOST, 0L);
  201  	}
  202  
  203  	//set curl to connection timeout
  204  	err = curl_easy_setopt(mHandle, CURLOPT_CONNECTTIMEOUT_MS, options != nullptr ? options->connectTimeout : 10000L);
  205  	if (err == CURLE_OK && options != nullptr && options->timeout > 0)
  206  		err = curl_easy_setopt(mHandle, CURLOPT_TIMEOUT_MS, options->timeout);
  207  	// A transfer under one byte a second for stallTimeout seconds ends with
  208  	// CURLE_OPERATION_TIMEDOUT: the bound for a request that may be long but
  209  	// never silent (ROCKNIX fork #299).
  210  	if (err == CURLE_OK && options != nullptr && options->stallTimeout > 0)
  211  		err = curl_easy_setopt(mHandle, CURLOPT_LOW_SPEED_LIMIT, 1L);
  212  	if (err == CURLE_OK && options != nullptr && options->stallTimeout > 0)
  213  		err = curl_easy_setopt(mHandle, CURLOPT_LOW_SPEED_TIME, options->stallTimeout);
  214  	if (err != CURLE_OK)
  215  	{
  216  		mStatus = REQ_IO_ERROR;
  217  		onError(curl_easy_strerror(err));
  218  		return;
  219  	}
  220  		
  221  	//set curl max redirects
  222  	err = curl_easy_setopt(mHandle, CURLOPT_MAXREDIRS, 2L);
  223  	if(err != CURLE_OK)
  224  	{
  225  		mStatus = REQ_IO_ERROR;
  226  		onError(curl_easy_strerror(err));
  227  		return;
  228  	}
  229  
  230  	// set curl restrict redirect protocols
  231  #if WIN32
  232  	curl_version_info_data* version_info = curl_version_info(CURLVERSION_NOW);
  233  
  234  	unsigned int major, minor, patch;
  235  	if (version_info && sscanf(version_info->version, "%u.%u.%u", &major, &minor, &patch) == 3)
  236  		err = curl_easy_setopt(mHandle, CURLOPT_REDIR_PROTOCOLS_STR, "http,https");
  237  	else 
  238  		err = curl_easy_setopt(mHandle, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS);
  239  #elif CURL_AT_LEAST_VERSION(7,85,0)
  240  	err = curl_easy_setopt(mHandle, CURLOPT_REDIR_PROTOCOLS_STR, "http,https");	
  241  #else
  242  	err = curl_easy_setopt(mHandle, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS);
  243  #endif
  244  
  245  	if(err != CURLE_OK)
  246  	{
  247  		mStatus = REQ_IO_ERROR;
  248  		onError(curl_easy_strerror(err));
```


## es-core/src/HttpReq.cpp @ 16dbac5211: lines 547-578 (excerpt of 644)

```text
  547  		ifs.close();
  548  
  549  		return ofs.str();
  550  	}
  551  	catch (...)
  552  	{
  553  		LOG(LogError) << "Error getting Http request content";
  554  	}
  555  
  556  	return "";
  557  }
  558  
  559  void HttpReq::onError(const char* msg)
  560  {
  561  	mErrorMsg = msg;
  562  	LOG(LogError) << "HttpReq::onError (" + std::to_string(mStatus) << ") : " + mErrorMsg;
  563  }
  564  
  565  std::string HttpReq::getErrorMsg()
  566  {
  567  	return mErrorMsg;
  568  }
  569  
  570  std::string HttpReq::getResponseHeader(const std::string& header)
  571  {
  572  	auto it = mResponseHeaders.find(header);
  573  	if (it != mResponseHeaders.cend())
  574  		return it->second;
  575  		
  576  	return "";
  577  }
  578  
```


## es-core/src/HttpReq.h @ 16dbac5211: lines 32-88 (excerpt of 180)

```text
   32  class HttpCookie
   33  {
   34  public:
   35  	std::string name;
   36  	std::string value;
   37  };
   38  
   39  class HttpCookieContainer
   40  {
   41  public:
   42  	std::vector<HttpCookie> cookies;
   43  };
   44  
   45  class HttpReqOptions
   46  {
   47  public:
   48  	HttpReqOptions() 
   49  	{
   50  		userAgent = HTTP_REQ_USERAGENT;
   51  		useCookieManager = true;
   52  		connectTimeout = 10000L;
   53  		timeout = 0L;
   54  		stallTimeout = 0L;
   55  	}
   56  
   57  	HttpReqOptions(const std::string& filename)
   58  	{
   59  		outputFilename = filename;
   60  		userAgent = HTTP_REQ_USERAGENT;
   61  		useCookieManager = true;
   62  		connectTimeout = 10000L;
   63  		timeout = 0L;
   64  		stallTimeout = 0L;
   65  	}
   66  
   67  	std::string outputFilename;
   68  	std::vector<std::string> customHeaders;
   69  	std::string dataToPost;
   70  	std::string userAgent;
   71  	// Client certificate files in .pem format
   72  	std::string clientCert, clientKey;
   73  
   74  	long connectTimeout;
   75  	// The whole request, connect included, in milliseconds; 0 (the default)
   76  	// leaves it unbounded, as every request was before. A caller asking a
   77  	// local service sets it, so a service that hangs cannot hold a page.
   78  	long timeout;
   79  	// Seconds a transfer may move no byte before it ends with an error; 0
   80  	// (the default) leaves a silent connection to TCP, which retries a
   81  	// dead peer for a quarter of an hour. For a request that may be long
   82  	// but must never be silent: the hash library's fetch on a pooled
   83  	// connection whose link had gone held the interface thread for twelve
   84  	// minutes on the VM (ROCKNIX fork #299), while a total bound would cut
   85  	// a slow but moving download.
   86  	long stallTimeout;
   87  	bool useCookieManager;
   88  };
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 1010-1074 (excerpt of 1409)

```text
 1010  	const int flushed = fields[1].size() > 9 ? 0 : std::stoi(fields[1]);
 1011  	if (when <= 0 || flushed <= 0)
 1012  		return stamp;
 1013  
 1014  	stamp.ok = true;
 1015  	stamp.when = (time_t) when;
 1016  	stamp.flushed = flushed;
 1017  	return stamp;
 1018  }
 1019  
 1020  // Moved from OfflineAchievements::scanWhy and ProxyCards' topUpWhy, so the
 1021  // table has a case (#308 follow-up): those two now ask here.
 1022  std::string CloudText::scanWhy(const std::string& token)
 1023  {
 1024  	if (token == "TOGGLE_OFF")
 1025  		return _("TURN ON OFFLINE ACHIEVEMENTS FIRST.");
 1026  	if (token == "NO_ACCOUNT")
 1027  		return _("SIGN IN TO RETROACHIEVEMENTS FIRST.");
 1028  	if (token == "SIGN_IN_REFUSED")
 1029  		return _("RETROACHIEVEMENTS DIDN'T ACCEPT YOUR SIGN-IN");
 1030  	if (token == "RETROACHIEVEMENTS_STOPPED_ANSWERING")
 1031  		return _("RETROACHIEVEMENTS STOPPED ANSWERING");
 1032  	if (token == "NO_GAMES_FOUND")
 1033  		return _("NO GAMES WERE FOUND ON THIS CONSOLE");
 1034  	if (token == "LIBRARY_UNREADABLE")
 1035  		return _("YOUR GAMES COULDN'T BE READ");
 1036  	if (token == "TOOK_TOO_LONG")
 1037  		return _("IT TOOK TOO LONG");
 1038  	// A fetch failed for some game, even among many that went through
 1039  	// (audit #186 PL-24): the run could not finish, and the next scan tries
 1040  	// those games again, since nothing marks them cached.
 1041  	if (token == "SOME_GAMES_NOT_SAVED")
 1042  		return _("SOME GAMES COULDN'T BE SAVED. TRY THE SCAN AGAIN.");
 1043  	// The image pass left achievement images behind (#307 PL-060; the ctl
 1044  	// stamps it only for a failure that may pass, so a scan can fetch them):
 1045  	// the games are cached, and the next scan tries the images again.
 1046  	// Proposed words, for the maintainer to approve.
 1047  	if (token == "SOME_IMAGES_NOT_SAVED")
 1048  		return _("SOME ACHIEVEMENT IMAGES COULDN'T BE SAVED. TRY THE SCAN AGAIN.");
 1049  	// The player's CANCEL on the scan page (D-UI-078): the ctl's INT trap
 1050  	// stamps it so the row says so; not a failure, and the next scan
 1051  	// carries on from what was saved.
 1052  	if (token == "CANCELLED")
 1053  		return _("YOU CANCELLED IT");
 1054  	return _("SOMETHING WENT WRONG");
 1055  }
 1056  
 1057  std::string CloudText::topUpWhy(const std::string& token)
 1058  {
 1059  	if (token == "SOME_GAMES_NOT_SAVED")
 1060  		return _("SOME GAMES COULDN'T BE SAVED");
 1061  	if (token == "SOME_IMAGES_NOT_SAVED")
 1062  		return _("SOME ACHIEVEMENT IMAGES COULDN'T BE SAVED");
 1063  	return scanWhy(token);
 1064  }
 1065  
 1066  // What a match that did not complete removed. The count is the one
 1067  // cloud_content_restore's ">>> removed" reports from rclone's own Deleted
 1068  // lines (stream A's 258b5eca38), no longer its plan. Nothing about the
 1069  // cloud: a match removes only what the cloud does not have (D-CLOUD-023),
 1070  // and the clause that followed -- YOUR CLOUD STILL HAS THEM -- said the
 1071  // opposite of what had happened.
 1072  std::string CloudText::matchRemovedNote(int removedFiles)
 1073  {
 1074  	if (removedFiles <= 0)
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 1178-1283 (excerpt of 1409)

```text
 1178  bool CloudText::isKnownUnitLabel(const std::string& label)
 1179  {
 1180  	for (auto& l : unitLabels())
 1181  		if (l.first == label)
 1182  			return true;
 1183  	return false;
 1184  }
 1185  
 1186  CloudText::ScanStamp CloudText::parseScanStamp(const std::string& text)
 1187  {
 1188  	ScanStamp stamp;
 1189  
 1190  	// One line: the time, the exit code and the route, then key=***
 1191  	// fields in any order. A whole number is at most twelve digits, as the
 1192  	// flush stamp's are.
 1193  	std::string line = text;
 1194  	const size_t newline = line.find('\n');
 1195  	if (newline != std::string::npos)
 1196  		line = line.substr(0, newline);
 1197  	const std::vector<std::string> fields = Utils::String::split(Utils::String::trim(line), ' ', true);
 1198  	if (fields.size() < 3)
 1199  		return stamp;
 1200  
 1201  	auto number = [](const std::string& f, long long& out) -> bool
 1202  	{
 1203  		if (f.empty() || f.size() > 12)
 1204  			return false;
 1205  		for (char c : f)
 1206  			if (c < '0' || c > '9')
 1207  				return false;
 1208  		out = std::stoll(f);
 1209  		return true;
 1210  	};
 1211  
 1212  	long long when = 0, code = 0;
 1213  	if (!number(fields[0], when) || when <= 0 || !number(fields[1], code))
 1214  		return stamp;
 1215  	if (fields[2] == "scan")
 1216  		stamp.topup = false;
 1217  	else if (fields[2] == "topup")
 1218  		stamp.topup = true;
 1219  	else
 1220  		return stamp;
 1221  
 1222  	for (size_t i = 3; i < fields.size(); i++)
 1223  	{
 1224  		const size_t eq = fields[i].find('=');
 1225  		if (eq == std::string::npos)
 1226  			continue;
 1227  		const std::string key = fields[i].substr(0, eq);
 1228  		const std::string value = fields[i].substr(eq + 1);
 1229  		if (key == "why")
 1230  		{
 1231  			// A token and nothing else: the caller maps it to a sentence,
 1232  			// and anything it does not know reads as SOMETHING WENT WRONG.
 1233  			bool token = !value.empty();
 1234  			for (char c : value)
 1235  				if (!((c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_'))
 1236  					token = false;
 1237  			if (token)
 1238  				stamp.why = value;
 1239  			continue;
 1240  		}
 1241  		if (key == "note")
 1242  		{
 1243  			// The ctl's token for a run that completed with nothing to do
 1244  			// (NO_GAMES, fork #329): a token, as why= is, or nothing.
 1245  			bool token = !value.empty();
 1246  			for (char c : value)
 1247  				if (!((c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_'))
 1248  					token = false;
 1249  			if (token)
 1250  				stamp.note = value;
 1251  			continue;
 1252  		}
 1253  		// The ctl's word for a count it could not measure (PL-031): an
 1254  		// answer of its own, where any other non-number says nothing.
 1255  		if (key == "added" && value == "unknown")
 1256  		{
 1257  			stamp.added = ScanStamp::AddedUnknown;
 1258  			continue;
 1259  		}
 1260  		long long n = 0;
 1261  		if (!number(value, n) || n > 1000000)
 1262  			continue;
 1263  		if (key == "cached")       stamp.cached = (int) n;
 1264  		else if (key == "added")   stamp.added = (int) n;
 1265  		else if (key == "skipped") stamp.skipped = (int) n;
 1266  		else if (key == "ready")   stamp.ready = (int) n;
 1267  		else if (key == "limit")   stamp.limit = n != 0;
 1268  		else if (key == "indexed") stamp.indexed = (int) n;
 1269  		else if (key == "errors")  stamp.errors = (int) n;
 1270  		else if (key == "truncated") stamp.truncated = n != 0;
 1271  	}
 1272  
 1273  	stamp.ran = true;
 1274  	stamp.when = (time_t) when;
 1275  	stamp.code = (int) code;
 1276  	return stamp;
 1277  }
 1278  
 1279  CloudText::RunningProgress CloudText::parseRunningProgress(const std::string& text, long long nowEpoch)
 1280  {
 1281  	RunningProgress run;
 1282  
 1283  	// One line of key=*** fields, in any order. A whole number is at most
```


## es-app/src/CloudText.cpp @ 16dbac5211: lines 1292-1353 (excerpt of 1409)

```text
 1292  	auto number = [](const std::string& f, long long& out) -> bool
 1293  	{
 1294  		if (f.empty() || f.size() > 12)
 1295  			return false;
 1296  		for (char c : f)
 1297  			if (c < '0' || c > '9')
 1298  				return false;
 1299  		out = std::stoll(f);
 1300  		return true;
 1301  	};
 1302  
 1303  	bool hasAt = false;
 1304  	for (const std::string& field : fields)
 1305  	{
 1306  		// The name may carry '=' of its own: the first one splits.
 1307  		const size_t eq = field.find('=');
 1308  		if (eq == std::string::npos)
 1309  			continue;
 1310  		const std::string key = field.substr(0, eq);
 1311  		const std::string value = field.substr(eq + 1);
 1312  		if (key == "route")
 1313  			run.route = value;
 1314  		else if (key == "at")
 1315  		{
 1316  			long long at = 0;
 1317  			if (number(value, at) && at > 0)
 1318  			{
 1319  				run.at = at;
 1320  				hasAt = true;
 1321  			}
 1322  		}
 1323  		else if (key == "index" || key == "total")
 1324  		{
 1325  			long long n = 0;
 1326  			if (!number(value, n) || n > 1000000)
 1327  				continue;
 1328  			if (key == "index")
 1329  				run.index = (int) n;
 1330  			else
 1331  				run.total = (int) n;
 1332  		}
 1333  	}
 1334  
 1335  	// A file is never a run on its own: it says when the ctl last wrote it,
 1336  	// and the ctl bounds its runs, so a line older than that bound was left
 1337  	// by a run that died. A line from the future by more than a day is a
 1338  	// clock that jumped, not a run.
 1339  	if (!hasAt)
 1340  		return run;
 1341  	if (nowEpoch - run.at > RUNNING_STALE_AFTER_S || run.at - nowEpoch > RUNNING_AHEAD_LIMIT_S)
 1342  		return run;
 1343  	run.running = true;
 1344  	return run;
 1345  }
 1346  
 1347  CloudText::NextTime CloudText::nextTime(bool awardsPending, bool savesPending)
 1348  {
 1349  	if (awardsPending && savesPending)
 1350  		return NextTime::AwardsAndSaves;
 1351  	if (awardsPending)
 1352  		return NextTime::Awards;
 1353  	if (savesPending)
```


## es-app/src/CloudText.h @ 16dbac5211: lines 472-518 (excerpt of 589)

```text
  472  	// limit=<0|1> indexed=<i> errors=<e>[ why=<TOKEN>]" from
  473  	// raofflineproxy-ctl's last-scan (indexed= and errors= since audit #186
  474  	// PL-24; a ctl before them writes neither, and both read 0): how
  475  	// the last scan of the console's games for offline achievements went,
  476  	// or the last automatic top-up when the device came online (fork #179,
  477  	// D-RA-010). ran is false for a line of any other shape, and the row
  478  	// then reads NOT SCANNED YET rather than inventing a date. The why is
  479  	// the ctl's token -- upper case, underscores, nothing else -- and the
  480  	// caller says it in words; a field that is not a count reads as zero.
  481  	struct ScanStamp
  482  	{
  483  		bool ran = false;
  484  		time_t when = 0;
  485  		int code = 0;
  486  		bool topup = false;   // the automatic run, not one the player pressed
  487  		int cached = 0;       // games this run cached, new and re-read alike
  488  		int added = -1;       // games new to the store this run (the ctl's added=, fork #298); -1 when the
  489  		                      // stamp does not say -- an older ctl's, where cached stood for it;
  490  		                      // AddedUnknown when the ctl said added=unknown (PL-031, below)
  491  		int skipped = 0;      // ROMs RetroAchievements does not know
  492  		int ready = 0;        // games cached in all, after the run
  493  		bool limit = false;   // the proxy's cap was reached
  494  		int indexed = 0;      // of cached, how many came from the interface's index (no hash)
  495  		int errors = 0;       // games a fetch failed for: what makes rc 1 with why=SOME_GAMES_NOT_SAVED
  496  		bool truncated = false; // the walk stopped at the client's cap of files; a second run reaches the rest
  497  		std::string why;
  498  		std::string note;       // the ctl's token for a run that completed with nothing to do: NO_GAMES (fork #329)
  499  		// added=unknown (audit of the fix round PL-031): the ctl could not
  500  		// read the store before or after a run that cached games, so how
  501  		// many were new was never counted. Not -1: that is an older ctl's
  502  		// stamp, where cached stood for the count; this one has no count
  503  		// to stand in, and the card says how many are ready instead.
  504  		static constexpr int AddedUnknown = -2;   // constexpr: inline, so a use by reference links
  505  	};
  506  	ScanStamp parseScanStamp(const std::string& text);
  507  
  508  	// The ctl's why tokens (raofflineproxy-ctl's scan and top-up), in the
  509  	// player's words (es-player-text.md: everyday, not formal): scanWhy for
  510  	// the scan page and the row under SCAN GAMES, topUpWhy for the top-up's
  511  	// card -- the same, except where the scan's sentence sends the player to
  512  	// the scan page, since that card's action line already says it tries
  513  	// again by itself (#308 1-raoffline F-RA-09). A token neither knows is
  514  	// SOMETHING WENT WRONG.
  515  	std::string scanWhy(const std::string& token);
  516  	std::string topUpWhy(const std::string& token);
  517  
  518  	// A match that did not complete, on the transfer page's done lines
```


## es-app/src/ProxyCards.cpp @ 16dbac5211: lines 182-408 (excerpt of 596)

```text
  182  		ThreadedCloudSync::writeStamp(LINK_STAMP, done ? 0 : 5, token, why);
  183  		LOG(LogInfo) << "ProxyCards: the send card ended " << token << " (pending " << pending << ")";
  184  
  185  		// The gate lets go as the outcome shows, as the sync card's does;
  186  		// the card holds the outcome long enough to read, then goes.
  187  		sSendRunning = false;
  188  		std::this_thread::sleep_for(std::chrono::milliseconds(5000));
  189  		card->close();
  190  	}
  191  
  192  	// The top-up card's why: the scan's words, except where the scan's
  193  	// sentence sends the player to the scan page -- this card's action line
  194  	// already says it tries again by itself, and two instructions on one
  195  	// card is one too many (#308 1-raoffline F-RA-09).
  196  	std::string topUpWhy(const std::string& token)
  197  	{
  198  		return CloudText::topUpWhy(token);
  199  	}
  200  
  201  	// One run of the top-up: the ctl on a thread of its own, this one
  202  	// attaching a card once the ctl's progress file says it has work and no
  203  	// other card holds the screen, and ending it with the ctl's stamp.
  204  	// topUpWatcher runs these one after another.
  205  	// One card for both ways an index can end offline (D-UI-104): the ctl's
  206  	// probe refused, or the hash library never came. The maintainer's shape
  207  	// and words (D-UI-106, 2026-09-27): the trophy and a title, the sentence
  208  	// under it, as the other RetroAchievements cards are drawn -- a one-line
  209  	// toast clipped the first sentence at 640x480 and had no room for a
  210  	// second (D-UI-105). Five seconds, as those cards' outcomes stand.
  211  	static void offlineIndexCard(Window* window)
  212  	{
  213  		AppWindow::post(window, [window]
  214  		{
  215  			AsyncNotificationComponent* card = window->createAsyncNotificationComponent();
  216  			card->updateTitle(TROPHY + _("RETROACHIEVEMENTS (OFFLINE)"));
  217  			card->updateText(_("NEWLY ADDED GAMES WILL BE ENABLED ONCE YOU RECONNECT."));
  218  			std::thread([card]
  219  			{
  220  				std::this_thread::sleep_for(std::chrono::milliseconds(5000));
  221  				card->close();
  222  			}).detach();
  223  		});
  224  	}
  225  
  226  	void runTopUp(Window* window, bool afterIndex)
  227  	{
  228  		sTopUpStoppedForGame = false;   // a stop that missed an earlier run is not this run's
  229  		std::atomic<bool> finished{ false };
  230  		int rc = -1;
  231  		const time_t startedAt = time(nullptr);
  232  		std::thread ctl([&rc, &finished, afterIndex]
  233  		{
  234  			rc = OfflineAchievements::runTopUp(afterIndex);
  235  			finished = true;
  236  		});
  237  
  238  		AsyncNotificationComponent* card = nullptr;
  239  		bool sawWork = false;
  240  		// A card is made on the interface thread and handed back here. When
  241  		// the loop that runs posted tasks is not turning -- a game has the
  242  		// screen -- the run goes on without a card, and the lambda, run
  243  		// later, makes none.
  244  		auto attach = [window]() -> AsyncNotificationComponent*
  245  		{
  246  			// `wanted` is flipped once, by whichever side gets there
  247  			// first: the lambda, which then makes the card and hands it
  248  			// over; or this thread on giving up, after which the lambda
  249  			// makes nothing. A card is never made for nobody.
  250  			auto made = std::make_shared<std::promise<AsyncNotificationComponent*>>();
  251  			auto wanted = std::make_shared<std::atomic<bool>>(true);
  252  			auto got = made->get_future();
  253  			AppWindow::post(window, [window, made, wanted]
  254  			{
  255  				if (!wanted->exchange(false))
  256  					return;
  257  				AsyncNotificationComponent* c = window->createAsyncNotificationComponent(true);
  258  				c->updateTitle(TROPHY + _("RETROACHIEVEMENTS (OFFLINE)"));
  259  				c->updateText(_("STARTING..."));
  260  				c->updatePercent(-1);
  261  				made->set_value(c);
  262  			});
  263  			if (got.wait_for(std::chrono::seconds(3)) == std::future_status::ready || !wanted->exchange(false))
  264  				return got.get();
  265  			return nullptr;
  266  		};
  267  		auto screenFree = []
  268  		{
  269  			return !sSendRunning && !ThreadedCloudSync::isRunning() && FileData::GetRunningGame() == nullptr;
  270  		};
  271  		while (!finished)
  272  		{
  273  			std::this_thread::sleep_for(std::chrono::milliseconds(500));
  274  			const CloudText::RunningProgress p = OfflineAchievements::runningProgress();
  275  			if (!p.running)
  276  				continue;
  277  			// Every run the ctl makes is worth its card (fork #299, D-UI-103): the
  278  			// link's return runs only when a game was played since the last
  279  			// attempt, and the index's run only when it found new games, so a run
  280  			// that shows is a run with something to look for -- and the card's
  281  			// words say what it is doing.
  282  			sawWork = true;
  283  			if (card == nullptr && screenFree())
  284  				card = attach();
  285  			if (card != nullptr && p.total > 0)
  286  				card->updateText(Utils::String::format(_("GETTING GAME %d OF %d READY...").c_str(), p.index, p.total));
  287  		}
  288  		ctl.join();
  289  		// 143 (TERM) or 130 (INT) is a run that was stopped. The launch's STOP
  290  		// IT AND PLAY is said below; any other stop -- the toggle turned off,
  291  		// whose disable stops the run -- is the player's own doing on another
  292  		// page, and there is nothing to report.
  293  		const bool stopped = rc == 143 || rc == 130;
  294  		const bool stoppedForGame = stopped && sTopUpStoppedForGame.exchange(false);
  295  		if (stopped && !stoppedForGame)
  296  		{
  297  			LOG(LogInfo) << "ProxyCards: the top-up was stopped (rc " << rc << ") and not for a game; no outcome is said";
  298  			if (card != nullptr)
  299  				card->close();
  300  			return;
  301  		}
  302  		// A game list updated offline (fork #299, D-UI-104): the index found
  303  		// games and the ctl could not reach RetroAchievements (69). It left
  304  		// its marker, and the link's return lists the library once for it,
  305  		// so the toast's promise is the ctl's to keep.
  306  		if (afterIndex && rc == 69)
  307  		{
  308  			LOG(LogInfo) << "ProxyCards: the index's top-up was refused offline; the card says the new games are enabled once reconnected";
  309  			offlineIndexCard(window);
  310  		}
  311  		// A run too quick for the poll to have seen its progress file still
  312  		// left its stamp: work was done when the stamp is this run's and
  313  		// counts a game added or a fetch failed.
  314  		const CloudText::ScanStamp s = OfflineAchievements::lastScan();
  315  		// The stamp speaks for this run only when this run wrote it: a run
  316  		// stopped by a signal, or cut off, writes none, and the one there is
  317  		// the last run's (F-RA-09: its why was said of this one).
  318  		const bool stamped = s.ran && s.when >= startedAt;
  319  		if (!sawWork && stamped && (s.cached > 0 || s.errors > 0))
  320  			sawWork = true;
  321  		if (!sawWork)
  322  			return;   // a run with no work: nothing to show
  323  		// A run that had work and ended before a card could be attached --
  324  		// quick, or behind the send card -- still gets its outcome said,
  325  		// once the screen is free (bounded: a game may have it).
  326  		const auto waited = std::chrono::steady_clock::now();
  327  		while (card == nullptr && std::chrono::steady_clock::now() - waited < std::chrono::seconds(90))
  328  		{
  329  			if (screenFree())
  330  				card = attach();
  331  			else
  332  				std::this_thread::sleep_for(std::chrono::seconds(1));
  333  		}
  334  		if (card == nullptr)
  335  			return;   // the screen stayed taken: the ctl's stamp keeps the outcome for the achievements page
  336  		std::vector<std::string> action;
  337  		std::string outcome;
  338  		const bool ok = rc == 0;
  339  		// Added is said only of games new to the store; a run that re-read
  340  		// what was there says how many are ready (#298, the maintainer:
  341  		// "if it's just doing an update, it can say X number of games
  342  		// ready for offline play"). A stamp an older ctl wrote has no
  343  		// added=, and cached stood for it. added=unknown is a count nobody
  344  		// measured (the store could not be read, PL-031): no count of new
  345  		// games is said, only how many are ready -- and with no ready total
  346  		// either, COMPLETED alone, since EVERYTHING'S UP TO DATE would claim
  347  		// what nobody counted.
  348  		// A run with nothing new writes no stamp (the row's line keeps the
  349  		// last scan that said something), so its count is the ready file's;
  350  		// a stamp from before this run says nothing about it.
  351  		const bool addedUnknown = stamped && s.added == CloudText::ScanStamp::AddedUnknown;
  352  		const int added = !stamped || addedUnknown ? 0 : s.added >= 0 ? s.added : s.cached;
  353  		const int ready = stamped ? s.ready : OfflineAchievements::readyCount();
  354  		if (ok)
  355  		{
  356  			outcome = _("COMPLETED");
  357  			// The title says RETROACHIEVEMENTS (OFFLINE); the line says only
  358  			// what changed (D-UI-107, the maintainer's rule for every card).
  359  			if (added == 1)
  360  				action.push_back(_("1 MORE GAME IS READY."));
  361  			else if (added > 1)
  362  				action.push_back(Utils::String::format(_("%d MORE GAMES ARE READY.").c_str(), added));
  363  			else if (ready == 1)
  364  				action.push_back(_("1 GAME IS READY."));
  365  			else if (ready > 1)
  366  				action.push_back(Utils::String::format(_("%d GAMES ARE READY.").c_str(), ready));
  367  			else if (!addedUnknown)
  368  				action.push_back(_("EVERYTHING'S UP TO DATE."));
  369  		}
  370  		else if (stoppedForGame)
  371  		{
  372  			// The launch's question promised this line (FileData::launchGame).
  373  			outcome = _("SKIPPED - YOU STARTED A GAME");
  374  			action.push_back(_("IT'LL TRY AGAIN NEXT TIME YOU'RE CONNECTED."));
  375  		}
  376  		else
  377  		{
  378  			outcome = std::string(_("COULDN'T FINISH")) + " - " + topUpWhy(stamped ? s.why : "");
  379  			action.push_back(_("IT'LL TRY AGAIN NEXT TIME YOU'RE CONNECTED."));
  380  		}
  381  		card->updateTitle(TROPHY + _("RETROACHIEVEMENTS (OFFLINE)"));
  382  		card->updateText(CloudText::outcomeCandidates(outcome), action);
  383  		card->updatePercent(ok ? 100 : -1);
  384  		LOG(LogInfo) << "ProxyCards: the top-up card ended rc " << rc << " cached " << s.cached << " added " << s.added << " ready " << s.ready
  385  			<< " says added " << (!ok ? 0 : added) << (addedUnknown ? " (the ctl could not count them)" : "")
  386  			<< " ready " << (!ok ? 0 : ready)
  387  			<< (stoppedForGame ? " (stopped for a game)" : "");
  388  		std::this_thread::sleep_for(std::chrono::milliseconds(5000));
  389  		card->close();
  390  	}
  391  
  392  	// The one watcher (PL-056): runs what was asked for, and what is asked
  393  	// for while it runs, then lets go. The index's run goes first when both
  394  	// are waiting. A run asked for while a game has the screen waits for the
  395  	// game to end rather than start under it: the ctl reads the network and
  396  	// the store, and a player who chose STOP IT AND PLAY was told it would
  397  	// try again later, not the moment the game started.
  398  	// Before every run, the first included: a stop for a game holds the
  399  	// queue until that game has started (or LaunchStartSeconds from the stop
  400  	// passed without it), and no run starts while a game has the screen.
  401  	// The first run skipped this (PL-056 kept its old at-once start), so a
  402  	// request made under a game -- the index ending as one launched --
  403  	// started the ctl under it (audit of the fix round, G2-E-app-05).
  404  	void waitForTheGame()
  405  	{
  406  		long long until = sTopUpHeldUntilMs.load();
  407  		if (until != 0)
  408  		{
```


## es-app/src/ProxyCards.cpp @ 16dbac5211: lines 552-596 (excerpt of 596)

```text
  552  
  553  	bool sendRunning()
  554  	{
  555  		return sSendRunning;
  556  	}
  557  
  558  	void topUp(Window* window, bool afterIndex)
  559  	{
  560  		if (!OfflineAchievements::available() || !OfflineAchievements::toggleOn())
  561  			return;
  562  		sTopUpWanted |= afterIndex ? 2 : 1;
  563  		if (sTopUpRunning.exchange(true))
  564  			return;   // the watcher that holds the flag runs this request when its run ends
  565  		std::thread(topUpWatcher, window).detach();
  566  	}
  567  
  568  	bool topUpRunning()
  569  	{
  570  		return OfflineAchievements::available() && OfflineAchievements::runningProgress().running;
  571  	}
  572  
  573  	bool stopTopUp()
  574  	{
  575  		// Before the signal: the watcher reads both the moment the ctl exits.
  576  		sTopUpStoppedForGame = true;
  577  		// The game the stop is for starts after it -- the launch waits for
  578  		// the ctl to be gone -- so one already on the screen is that game.
  579  		sTopUpHeldGames = FileData::GetGamesStarted() - (FileData::GetRunningGame() != nullptr ? 1 : 0);
  580  		sTopUpHeldUntilMs = steadyMs() + LaunchStartSeconds * 1000LL;
  581  		if (OfflineAchievements::stopRun())
  582  			return true;
  583  		sTopUpStoppedForGame = false;
  584  		sTopUpHeldUntilMs = 0;
  585  		return false;
  586  	}
  587  
  588  	void indexRanOffline(Window* window, int games)
  589  	{
  590  		if (!OfflineAchievements::available() || !OfflineAchievements::toggleOn())
  591  			return;
  592  		LOG(LogInfo) << "ProxyCards: the index ran offline with " << games << " game(s) to identify; the card says the new games are enabled once reconnected, and the ctl is told (index-offline)";
  593  		offlineIndexCard(window);
  594  		std::thread([] { OfflineAchievements::markIndexOffline(); }).detach();
  595  	}
  596  }
```


## es-core/src/utils/FileSystemUtil.cpp @ 16dbac5211: lines 1357-1438 (excerpt of 1805)

```text
 1357  
 1358  			// check if stat64 succeeded
 1359  #if defined(_WIN32)
 1360  			if ((_wstat64(Utils::String::convertToWideString(path).c_str(), &info) == 0))
 1361  				return Utils::Time::DateTime(info.st_mtime);
 1362  #else
 1363  			if ((stat64(path.c_str(), &info) == 0))
 1364  				return Utils::Time::DateTime(info.st_mtime);
 1365  #endif
 1366  			return Utils::Time::DateTime();
 1367  		}
 1368  
 1369  		static void skipUtf8Bom(std::ifstream& file) 
 1370  		{
 1371  			if (!file.is_open())
 1372  				return;
 1373  
 1374  			char bom[3];
 1375  			if (file.read(bom, 3) && bom[0] == '\xEF' && bom[1] == '\xBB' && bom[2] == '\xBF')			
 1376  				return;
 1377  			
 1378  			file.seekg(0);
 1379  		}
 1380  
 1381  		std::vector<char> readAllBytes(const std::string& fileName)
 1382  		{
 1383  			std::ifstream file(WINSTRINGW(fileName), std::ios::binary | std::ios::ate);
 1384  			if (!file.is_open())
 1385  				return {};
 1386  
 1387  			std::streampos size = file.tellg();			
 1388  			if (size <= 0 || size == LLONG_MAX)
 1389  				return {};
 1390  
 1391  			file.seekg(0, std::ios::beg);
 1392  			
 1393  			std::vector<char> buffer(size);			
 1394  			if (!file.read(buffer.data(), size))
 1395  				return {};
 1396  
 1397  			return buffer;
 1398  		}
 1399  
 1400  		std::list<std::string> readAllLines(const std::string& fileName)
 1401  		{
 1402  			std::list<std::string> lines;
 1403  
 1404  			std::ifstream file(WINSTRINGW(fileName));
 1405  			if (!file.is_open()) 
 1406  				return lines;
 1407  
 1408  			skipUtf8Bom(file);
 1409  
 1410  			std::string line;
 1411  			while (std::getline(file, line))
 1412  				lines.push_back(line);
 1413  
 1414  			file.close();
 1415  			return lines;
 1416  		}
 1417  
 1418  		std::string	readAllText(const std::string& fileName)
 1419  		{
 1420  			std::ifstream t(WINSTRINGW(fileName));
 1421  
 1422  			skipUtf8Bom(t);
 1423  
 1424  			std::stringstream buffer;
 1425  			buffer << t.rdbuf();
 1426  			return buffer.str();
 1427  		}
 1428  
 1429  		void writeAllText(const std::string& fileName, const std::string& text)
 1430  		{
 1431  #if defined(_WIN32)
 1432  			FILE* file = _wfopen(Utils::String::convertToWideString(fileName).c_str(), L"wb");
 1433  #else
 1434  			FILE* file = fopen(fileName.c_str(), "wb");
 1435  #endif
 1436  			if (file == nullptr)
 1437  				return;		
 1438  
```


## es-core/src/Settings.cpp @ 16dbac5211: lines 51-67 (excerpt of 723)

```text
   51  	UPDATE_STATIC_BOOL_SETTING(DebugImage)
   52  	UPDATE_STATIC_BOOL_SETTING(DebugGrid)
   53  	UPDATE_STATIC_BOOL_SETTING(DebugMouse)
   54  	UPDATE_STATIC_BOOL_SETTING(ShowControllerActivity)
   55  	UPDATE_STATIC_BOOL_SETTING(ShowControllerBattery)
   56  	UPDATE_STATIC_BOOL_SETTING(ShowNetworkIndicator)
   57  	UPDATE_STATIC_BOOL_SETTING(DrawClock)
   58  	UPDATE_STATIC_BOOL_SETTING(ClockMode12)
   59  	UPDATE_STATIC_BOOL_SETTING(DrawFramerate)
   60  	UPDATE_STATIC_BOOL_SETTING(UseFileCache)
   61  	UPDATE_STATIC_BOOL_SETTING(ScrollLoadMedias)
   62  	UPDATE_STATIC_BOOL_SETTING(VolumePopup)
   63  	UPDATE_STATIC_BOOL_SETTING(VSync)
   64  	UPDATE_STATIC_BOOL_SETTING(PreloadMedias)
   65  	UPDATE_STATIC_BOOL_SETTING(IgnoreLeadingArticles)		
   66  	UPDATE_STATIC_BOOL_SETTING(ShowVideoPreviews)
   67  	UPDATE_STATIC_BOOL_SETTING(ShowFoldersFirst)
```


## es-core/src/Settings.cpp @ 16dbac5211: lines 412-428 (excerpt of 723)

```text
  412  	
  413  	mBoolMap["CheevosCheckIndexesAtStart"] = false;	
  414  
  415  	mBoolMap["AllImagesAsync"] = true;
  416  
  417  #if WIN32
  418  	mBoolMap["updates.enabled"] = true;
  419  	mBoolMap["global.retroachievements"] = false;
  420  	mBoolMap["global.retroachievements.hardcore"] = false;
  421  	mBoolMap["global.retroachievements.leaderboards"] = false;
  422  	mBoolMap["global.retroachievements.verbose"] = false;
  423  	mBoolMap["global.retroachievements.screenshot"] = false;
  424  	mBoolMap["global.retroachievements.encore"] = false;
  425  	mBoolMap["global.retroachievements.richpresence"] = false;
  426  
  427  	mBoolMap["global.netplay_public_announce"] = true;
  428  	mBoolMap["global.netplay"] = false;
```


## es-core/src/SystemConf.cpp @ 16dbac5211: lines 280-296 (excerpt of 494)

```text
  280  
  281  	LOG(LogError) << "Unable to open " << mSystemConfFile;
  282  	return false;
  283  }
  284  
  285  bool SystemConf::saveSystemConf()
  286  {
  287  	if (mSystemConfFile.empty())
  288  		return Settings::getInstance()->saveFile();	
  289  
  290  	if (changedConf.empty())
  291  		return false;
  292  
  293  	// The shell's settings lock (wait_lock in profile.d/001-functions), held
  294  	// across the read-modify-write: set_setting reads the file, writes a
  295  	// temporary and renames it under the same lock, and a save that read or
  296  	// renamed beside it put one writer's snapshot over the other's. Five
```


## es-core/src/Paths.cpp @ 16dbac5211: lines 86-102 (excerpt of 363)

```text
   86  	mThemesPath = mUserEmulationStationPath + "/themes";
   87  	mUserThemesPath = "/storage/roms/themes";
   88  	mDecorationsPath = "/storage/roms/bezels";
   89  	mUserDecorationsPath = "/tmp/overlays/bezels";
   90  	mTimeZonesPath = "/usr/share/zoneinfo";
   91  	mRetroachivementSounds = "/usr/share/libretro/sounds";
   92  	mUserRetroachivementSounds = "/storage/roms/music/retroachievements";
   93  
   94  	mSystemConfFilePath = "/storage/.config/system/configs/system.cfg";
   95  #endif
   96  
   97  /* EmuElec sample locations.
   98  #ifdef _ENABLEEMUELEC
   99  	mRootPath = "/storage/roms"; // ?
  100  	mEmulationStationPath = Utils::FileSystem::getExePath();
  101  	mUserEmulationStationPath = Utils::FileSystem::getCanonicalPath(Utils::FileSystem::getHomePath() + "/.emulationstation");
  102  	mLogPath = "/storage/.config/emuelec/logs";
```


## raofflineproxy-ctl @ 8ebaf8daad: lines 292-408 (excerpt of 2455)

```text
  292  RUNNING="${PROXY_DIR}/running"
  293  TOPUP_MARK="${PROXY_DIR}/last-topup-attempt"
  294  # An index run that could not reach RetroAchievements (a game list updated
  295  # offline) leaves this, and the next link-return run lists the library
  296  # once for it, so the games an index identified while the device was
  297  # offline are cached when it is next online (fork #299; the games an index
  298  # could not identify are the interface's next index's, #308 F-RA-22). It is
  299  # removed only by a run whose listing and indexed pass both went through, so
  300  # a run that fails or is stopped part-way leaves it for the next (#307
  301  # PL-055).
  302  INDEX_PENDING="${PROXY_DIR}/index-pending"
  303  READY_FILE="${PROXY_DIR}/cached_game_ids.txt"
  304  SCAN_LOCK="/var/run/raofflineproxy-scan.lock"
  305  ROMS_ROOT="/storage/roms"
  306  # The interface's own folder: es_systems.cfg, and the two places its game
  307  # index is kept on disk (gamelists/<system>/ and recovery/<system>/).
  308  ES_DIR="/storage/.config/emulationstation"
  309  # The account keys EmulationStation writes (the token after a sign-in). Read
  310  # for presence only, never printed.
  311  USER_KEY=***
  312  TOKEN_KEY=***
  313  PASSWORD_KEY=***
  314  
  315  # sysexits.h, as CloudExit.h names them: a run that did nothing, and why.
  316  EX_USAGE=64         # a bad argument; the usage line was printed (refresh, audit #258 PL-012)
  317  EX_UNAVAILABLE=69   # offline by the proxy's probe
  318  EX_TEMPFAIL=75      # another scan or top-up holds the lock
  319  EX_NOPERM=77        # no RetroAchievements account signed in
  320  EX_CONFIG=78        # the toggle is off
  321  
  322  # The top-up's probe schedule: the token check's (#175, CheevosRetry.h --
  323  # nine tries ten seconds apart), for the same reason: the hook fires when
  324  # the address arrives, and a hotspot's resolver answers 20-45 s later.
  325  PROBE_TRIES=9
  326  PROBE_INTERVAL=10
  327  # How long disable waits for a scan or top-up it has asked to stop.
  328  STOP_WAIT=10
  329  # Lookups RetroAchievements did not answer, in a row, before the scan stops
  330  # asking: every one is a request spent on a link or a sign-in that is not
  331  # working, and the page can say so sooner.
  332  ERRORS_IN_A_ROW=3
  333  # One automatic top-up attempt per this many seconds, and no single run
  334  # longer than TOPUP_TIMEOUT: a link that flaps must not turn into a request
  335  # storm, and a hook that never returns is a hook nobody can reason about.
  336  TOPUP_INTERVAL=1800
  337  TOPUP_TIMEOUT=900
  338  
  339  # The client resolves its folder the way the unit sets it, and RetroArch's
  340  # `~` in content_history_path and playlist_directory is /storage on ROCKNIX
  341  # (the proxy expands it with HOME, and EmulationStation's may differ).
  342  export RAOFFLINEPROXY_CONFIG_DIR="${PROXY_DIR}"
  343  export HOME=/storage
  344  export XDG_CONFIG_HOME=/storage/.config
  345  PROXY_PY="python3 -m raofflineproxy.main"
  346  
  347  # The ROCKNIX ROM folders of the systems RetroAchievements has sets for, by
  348  # RetroAchievements' console list (2026-09) mapped onto the folder names
  349  # es_systems.cfg uses on this image, both spellings where two images differ
  350  # (coleco/colecovision, odyssey/odyssey2, pc88/pc-8800, fbneo/fbn,
  351  # sgfx/supergrafx). A folder that is not here is never walked: the proxy
  352  # would only hash it and be told no, one request per file, and a computer
  353  # or Windows library can be tens of gigabytes. Arcade folders hash by file
  354  # name (rc_hash's arcade rule), so they cost no reading. The hack folders
  355  # (nesh, snesh, ...) stay: RetroAchievements has sets for many hacks, and
  356  # the ones it does not know are skipped like any other ROM.
  357  SCAN_SYSTEMS="
  358    nes famicom fds nesh snes sfc snesh snesmsu1 satellaview sufami
  359    gb gbh gbc gbch gba gbah n64 n64dd nds ndsiware gamecube wii
  360    pokemini virtualboy megaduck supervision arduboy wasm4 uzebox
  361    channelf odyssey odyssey2 videopac intellivision coleco colecovision vectrex
  362    mastersystem megadrive genesis megadrive-japan megadriveh genh sega32x
  363    segacd megacd saturn dreamcast gamegear gamegearh ggh sg-1000
  364    psx ps2 psp pspminis
  365    atari2600 atari7800 atarijaguar atarijaguarcd atarilynx
  366    pcengine tg16 pcenginecd tg16cd sgfx supergrafx pcfx pc88 pc-8800
  367    ngp ngpc neocd wonderswan wonderswancolor msx msx2 amstradcpc apple2 3do
  368    arcade mame fbneo fbn neogeo cps1 cps2 cps3
  369  "
  370  
  371  say() {
  372      logger -t raofflineproxy-ctl "$*"
  373  }
  374  
  375  fail() {
  376      say "$*"
  377      echo "raofflineproxy-ctl: $*" >&2
  378      exit 1
  379  }
  380  
  381  # A setting as system.cfg holds it; empty when absent.
  382  setting() {
  383      get_setting "${1}"
  384  }
  385  
  386  # 0 or 1, from a value that may be empty or anything else.
  387  as_flag() {
  388      if [ "${1:-}" = "1" ]; then echo 1; else echo 0; fi
  389  }
  390  
  391  have_systemctl() {
  392      command -v systemctl >/dev/null 2>&1
  393  }
  394  
  395  service_state() {
  396      if have_systemctl; then
  397          systemctl is-active "${UNIT}" 2>/dev/null || true
  398      else
  399          echo unknown
  400      fi
  401  }
  402  
  403  do_start() {
  404      have_systemctl || fail "no systemctl to start ${UNIT} with"
  405      systemctl start "${UNIT}" || fail "${UNIT} did not start"
  406  }
  407  
  408  do_stop() {
```


## raofflineproxy-ctl @ 8ebaf8daad: lines 432-668 (excerpt of 2455)

```text
  432      [ "${E_KEY_CHANGED}" -eq 1 ] && put_back "${KEY}" "${E_KEY_BEFORE}"
  433      [ "${E_HARDCORE_CHANGED}" -eq 1 ] && put_back "${HARDCORE_KEY}" "${E_HARDCORE_BEFORE}"
  434      [ "${E_RECORD_WROTE}" -eq 1 ] && set_setting "${HARDCORE_WAS_KEY}" default
  435      [ "${E_STARTED}" -eq 1 ] && [ "${E_SERVICE_WAS}" -eq 0 ] && do_stop
  436      [ "${E_MARKER_WAS}" -eq 0 ] && rm -f "${MARKER}"
  437      fail "$*"
  438  }
  439  
  440  do_enable() {
  441      E_KEY_BEFORE="$(setting "${KEY}")"
  442      E_HARDCORE_BEFORE="$(setting "${HARDCORE_KEY}")"
  443      [ -e "${MARKER}" ] && E_MARKER_WAS=1
  444      [ "$(service_state)" = "active" ] && E_SERVICE_WAS=1
  445  
  446      # The marker first, the service second: if the service cannot start,
  447      # nothing about the player's settings has changed yet, and the marker
  448      # goes again so the next boot does not start what could not run now.
  449      mkdir -p "${MARKER_DIR}" || fail "cannot create ${MARKER_DIR}"
  450      touch "${MARKER}" || fail "cannot write ${MARKER}"
  451      if have_systemctl; then
  452          if ! systemctl start "${UNIT}"; then
  453              [ "${E_MARKER_WAS}" -eq 0 ] && rm -f "${MARKER}"
  454              fail "${UNIT} did not start; the toggle stays off"
  455          fi
  456          E_STARTED=1
  457      fi
  458  
  459      # Then the settings, each read back before the next is written, the
  460      # toggle last of all: until it reads 1 nothing routes through the proxy,
  461      # so a failure anywhere before it leaves the device as it was once
  462      # enable_undo has run, and a failure after it cannot happen -- it is
  463      # the last write.
  464      #
  465      # Record hardcore as it was, once. A second enable finds the record and
  466      # keeps it, so the value disable puts back is the player's and not the 0
  467      # the first enable wrote.
  468      if [ -z "$(setting "${HARDCORE_WAS_KEY}")" ]; then
  469          set_setting "${HARDCORE_WAS_KEY}" "$(as_flag "${E_HARDCORE_BEFORE}")"
  470          E_RECORD_WROTE=1
  471          [ -n "$(setting "${HARDCORE_WAS_KEY}")" ] || enable_undo "${HARDCORE_WAS_KEY} did not take"
  472      fi
  473      set_setting "${HARDCORE_KEY}" 0
  474      E_HARDCORE_CHANGED=1
  475      [ "$(setting "${HARDCORE_KEY}")" = "0" ] || enable_undo "${HARDCORE_KEY} did not take"
  476      set_setting "${KEY}" 1
  477      E_KEY_CHANGED=1
  478      [ "$(setting "${KEY}")" = "1" ] || enable_undo "${KEY} did not take"
  479      [ -e "${MARKER}" ] || enable_undo "${MARKER} is gone"
  480  
  481      say "offline RetroAchievements on: hardcore was $(setting "${HARDCORE_WAS_KEY}"), now 0; ${UNIT} $(service_state)"
  482      echo "hardcore=0"
  483  }
  484  
  485  # A scan or top-up the interface started is no child of this process; its
  486  # lock file carries its pid (take_lock writes it), so it is asked to stop
  487  # (SIGTERM: its trap ends the helper and cleans up) and given STOP_WAIT
  488  # seconds to let go of the lock. Nothing else is matched by name or pattern.
  489  # Exit 0 when nothing was running or it stopped, 1 when it did not.
  490  stop_running_run() {
  491      [ -e "${SCAN_LOCK}" ] || return 0
  492      exec 7<>"${SCAN_LOCK}" || return 0
  493      if flock -n 7; then exec 7>&-; return 0; fi
  494      local PID WAITED=0
  495      PID="$(head -n 1 "${SCAN_LOCK}" 2>/dev/null)"
  496      case "${PID}" in ''|*[!0-9]*) PID="" ;; esac
  497      if [ -n "${PID}" ]; then
  498          say "disable: a scan or top-up is running (pid ${PID}); asking it to stop"
  499          kill -TERM "${PID}" 2>/dev/null
  500      else
  501          say "disable: a scan or top-up holds the lock and left no pid; waiting for it"
  502      fi
  503      until flock -n 7; do
  504          if [ "${WAITED}" -ge "${STOP_WAIT}" ]; then
  505              say "disable: the running scan or top-up did not stop within ${STOP_WAIT}s; carrying on"
  506              exec 7>&-
  507              return 1
  508          fi
  509          sleep 1
  510          WAITED=$((WAITED + 1))
  511      done
  512      exec 7>&-
  513      say "disable: the running scan or top-up stopped"
  514      return 0
  515  }
  516  
  517  do_disable() {
  518      # The toggle first: a scan or top-up starting from now on is refused by
  519      # its own check, and the launchers route direct from the next launch.
  520      # Each step is read back before the next one uses it up (#308 F-RA-18):
  521      # a toggle that did not clear stops nothing, so the device stays on --
  522      # service, marker and record together -- rather than half off.
  523      set_setting "${KEY}" 0
  524      [ "$(setting "${KEY}")" = "0" ] || fail "${KEY} did not clear; the service, the marker and the hardcore record are left as they were"
  525      stop_running_run
  526      do_stop
  527      rm -f "${MARKER}"
  528  
  529      # Put hardcore back as the record says, and remove the record only once
  530      # hardcore reads back as it says: a write that did not hold keeps the
  531      # record, so the next disable can still put the player's setting back
  532      # (#308 F-RA-18). No record -- a device that never had the toggle on, or
  533      # a second disable -- leaves it alone.
  534      local WAS
  535      WAS="$(setting "${HARDCORE_WAS_KEY}")"
  536      if [ -n "${WAS}" ]; then
  537          set_setting "${HARDCORE_KEY}" "$(as_flag "${WAS}")"
  538          [ "$(setting "${HARDCORE_KEY}")" = "$(as_flag "${WAS}")" ] || fail "${HARDCORE_KEY} was not put back; the record is kept for the next disable"
  539          set_setting "${HARDCORE_WAS_KEY}" default
  540          [ -z "$(setting "${HARDCORE_WAS_KEY}")" ] || fail "${HARDCORE_WAS_KEY} was not cleared"
  541      fi
  542  
  543      [ ! -e "${MARKER}" ] || fail "${MARKER} could not be removed"
  544  
  545      say "offline RetroAchievements off: hardcore ${WAS:+put back to }${WAS:-left as it was}; ${UNIT} $(service_state)"
  546      echo "hardcore=$(as_flag "$(setting "${HARDCORE_KEY}")")"
  547  }
  548  
  549  do_status() {
  550      local ON
  551      ON="$(as_flag "$(setting "${KEY}")")"
  552      echo "enabled=${ON}"
  553      if [ -e "${MARKER}" ]; then echo "marker=1"; else echo "marker=0"; fi
  554      echo "service=$(service_state)"
  555      echo "hardcore=$(as_flag "$(setting "${HARDCORE_KEY}")")"
  556      [ "${ON}" = "1" ]
  557  }
  558  
  559  # The count could not be read: nothing on stdout, the reason on stderr and in
  560  # the log, exit 2. A guard that cannot run has not passed -- and a number
  561  # that is not known is not printed as one.
  562  cannot_tell() {
  563      say "$*"
  564      echo "raofflineproxy-ctl: $*" >&2
  565      exit 2
  566  }
  567  
  568  do_pending() {
  569      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ] || [ ! -e "${QUEUE}" ]; then
  570          echo 0
  571          return 1
  572      fi
  573      # The same interpreter and sqlite3 module the service writes the store
  574      # with (the package depends on Python3 for the service itself), opened
  575      # read-only, with a second's patience for a write in flight. The image
  576      # also carries a sqlite3 binary, but not by this package's asking.
  577      local N
  578      N="$(python3 -c '
  579  import sqlite3, sys
  580  db = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True, timeout=1.0)
  581  print(db.execute("SELECT COUNT(*) FROM pending_awards WHERE status = ?", ("pending",)).fetchone()[0])
  582  ' "${QUEUE}" 2>/dev/null)" || cannot_tell "the award queue at ${QUEUE} could not be read"
  583      case "${N}" in
  584          ''|*[!0-9]*) cannot_tell "the award queue answered '${N}', not a count" ;;
  585      esac
  586      echo "${N}"
  587      [ "${N}" -gt 0 ]
  588  }
  589  
  590  # The pending awards by id, oldest first, each with the second it was earned
  591  # (the store keeps milliseconds). Read the way pending reads: read-only, the
  592  # service's own sqlite3 module, a second's patience.
  593  do_pending_ids() {
  594      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ] || [ ! -e "${QUEUE}" ]; then
  595          return 1
  596      fi
  597      # The signed-in account's awards, and those that name no account: the
  598      # page marks these as this player's, so another account's award on this
  599      # device is not among them (#308 gpt F-RA-09). No account set: all, as
  600      # before.
  601      local ROWS
  602      ROWS="$(python3 -c '
  603  import sqlite3, sys
  604  from urllib.parse import parse_qs
  605  user = sys.argv[2].strip().lower()
  606  def owner(query, body):
  607      for text in ((query or "").split("?", 1)[-1], body or ""):
  608          values = parse_qs(text, keep_blank_values=True).get("u")
  609          if values and values[0].strip():
  610              return values[0].strip().lower()
  611      return ""
  612  db = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True, timeout=1.0)
  613  for aid, queued, query, body in db.execute("SELECT achievementId, queuedAt, queryString, requestBody FROM pending_awards WHERE status = ? ORDER BY queuedAt ASC, id ASC", ("pending",)):
  614      if not user or owner(query, body) in ("", user):
  615          print(int(aid), int(queued) // 1000)
  616  ' "${QUEUE}" "$(setting "${USER_KEY}")" 2>/dev/null)" || cannot_tell "the award queue at ${QUEUE} could not be read"
  617      [ -n "${ROWS}" ] || return 1
  618      printf '%s\n' "${ROWS}"
  619      return 0
  620  }
  621  
  622  # summary: the page's whole offline summary in one read of the store (fork
  623  # #190: 247 saved games were 494 requests to the service, each tried
  624  # upstream first while the service still believed it was online -- hours on
  625  # a link that had just gone). One JSON object a line, sorted by id:
  626  #   {"id":4902,"title":"Bobl","icon":"http://127.0.0.1:8080/Images/x.png",
  627  #    "achievements":12,"points":110,"unlocked":1,"unlockedPoints":5,"pending":1}
  628  # A game is the account's patch row, or -- for a game a launch cached and
  629  # nothing else did -- its achievementsets row (RetroArch asks achievementsets,
  630  # not patch; #307 PL-057), read as the interface's game page reads one: the
  631  # set of Type core, else the first. The core set (Flags 3, positive ids) as
  632  # the interface reads a patch; a game whose set is empty is not a cached game
  633  # (audit #186 PL-26); unlocked counts the store's unlocks and the casual
  634  # awards still waiting, as the service's own offline unlocks answer does --
  635  # and when the store's unlock row for the game is missing or cannot be read,
  636  # unlocked and unlockedPoints are null: unknown, never 0 (#307 PL-057). The
  637  # icon carries the service's address as the service would rewrite it. Exit
  638  # 1 with the toggle off, no account set or no store; the store that cannot
  639  # be read is a cannot_tell (exit 2).
  640  do_summary() {
  641      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ] || [ ! -e "${QUEUE}" ]; then
  642          return 1
  643      fi
  644      local USER
  645      USER=*** "${USER_KEY}")"
  646      [ -n "${USER}" ] || return 1
  647      python3 - "${QUEUE}" "${USER}" <<'PY_SUMMARY'
  648  import json, sqlite3, sys
  649  from urllib.parse import parse_qs, urlsplit
  650  store, user = sys.argv[1], sys.argv[2].strip().lower()
  651  base = "http://127.0.0.1:8080"
  652  def icon_url(text):
  653      text = (text or "").strip()
  654      if not text:
  655          return ""
  656      if text.startswith("/"):
  657          return base + text
  658      if "://" in text:
  659          path = urlsplit(text).path
  660          return base + path if path else ""
  661      return base + "/" + text
  662  def core_of(achievements):
  663      return [a for a in (achievements or []) if isinstance(a, dict) and int(a.get("Flags") or 3) == 3 and int(a.get("ID") or 0) > 0]
  664  def set_achievements(data):
  665      # OfflineAchievementsText::parseAchievementSets: the set of Type core, else the first.
  666      if isinstance(data.get("Achievements"), list):
  667          return data["Achievements"]
  668      chosen = None
```


## raofflineproxy-ctl @ 8ebaf8daad: lines 692-878 (excerpt of 2455)

```text
  692              return values[0].strip().lower()
  693      return ""
  694  # Awards waiting for this account, or naming none: another account's award
  695  # on this device is that account's, not whoever is signed in now (#308 gpt
  696  # F-RA-09).
  697  pending = {int(aid) for aid, query, body in awards if owner(query, body) in ("", user)}
  698  found = {}   # id -> (title, icon, core set)
  699  for key, body in patches:
  700      parts = key.split(":")
  701      if len(parts) != 3 or parts[2] != user:***
  702          continue
  703      try:
  704          gid = int(parts[1])
  705          patch = (json.loads(body) or {}).get("PatchData") or {}
  706          core = core_of(patch.get("Achievements"))
  707      except Exception:
  708          continue
  709      found[gid] = (str(patch.get("Title") or ""), patch.get("ImageIcon"), core)
  710  for key, body in sets:
  711      parts = key.split(":")
  712      if len(parts) != 3 or parts[2] != user:***
  713          continue
  714      try:
  715          data = json.loads(body) or {}
  716          gid = int(data.get("GameId") or 0)
  717          core = core_of(set_achievements(data))
  718      except Exception:
  719          continue
  720      if gid > 0 and core and not (gid in found and found[gid][2]):
  721          found[gid] = (str(data.get("Title") or ""), data.get("ImageIconUrl") or data.get("ImageIcon"), core)
  722  games = []
  723  for gid, (title, icon, core) in found.items():
  724      if gid <= 0 or not core:
  725          continue
  726      points = {int(a["ID"]): int(a.get("Points") or 0) for a in core}
  727      queued = pending & set(points)
  728      unlocked = None   # unknown until the store's unlock row is read
  729      row = unlock_rows.get("unlocks:%d:%s:0" % (gid, user))   # the casual row (cache_keys.unlocks: a trailing 0)
  730      if row is not None:
  731          try:
  732              data = json.loads(row)
  733              values = data.get("UserUnlocks") if isinstance(data, dict) and data.get("Success") is not False else None
  734              if isinstance(values, list):
  735                  unlocked = ({int(u) for u in values} | queued) & set(points)
  736          except Exception:
  737              unlocked = None
  738      games.append({"id": gid, "title": title, "icon": icon_url(icon),
  739                    "achievements": len(points), "points": sum(points.values()),
  740                    "unlocked": None if unlocked is None else len(unlocked),
  741                    "unlockedPoints": None if unlocked is None else sum(points[i] for i in unlocked),
  742                    "pending": len(queued)})
  743  for game in sorted(games, key=*** g: g["id"]):
  744      print(json.dumps(game, separators=(",", ":"), ensure_ascii=False))
  745  PY_SUMMARY
  746      local RC=$?
  747      [ "${RC}" -eq 0 ] || cannot_tell "the proxy's store at ${QUEUE} could not be read"
  748  }
  749  
  750  # The account's points from the proxy's cached sign-in (the login2 row of the
  751  # signed-in user, keyed by the user name in lower case as cache_keys.py
  752  # normalises it). The row carries the session token; the two numbers are
  753  # all that leaves this function.
  754  do_account() {
  755      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ] || [ ! -e "${QUEUE}" ]; then
  756          return 1
  757      fi
  758      local USER LINE
  759      USER=*** "${USER_KEY}")"
  760      [ -n "${USER}" ] || return 1
  761      # Exit 1 is "no such row", said apart from a store that cannot be read
  762      # (exit 3): an account nobody signed in is not the same as a store the
  763      # page should not trust, and only the second is a cannot_tell.
  764      LINE="$(python3 -c '
  765  import json, sqlite3, sys
  766  try:
  767      db = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True, timeout=1.0)
  768      row = db.execute("SELECT responseBody FROM api_cache WHERE cacheKey = ?", ("login2::" + sys.argv[2].strip().lower(),)).fetchone()
  769  except Exception:
  770      sys.exit(3)
  771  if row is None:
  772      sys.exit(1)
  773  try:
  774      body = json.loads(row[0])
  775  except Exception:
  776      sys.exit(3)
  777  # The row the proxy writes from a token (auth.cache_token_credentials) has no
  778  # Score: nothing is cached about the points, and an absent number is never
  779  # printed as 0.
  780  if not isinstance(body, dict) or body.get("Score") is None or body.get("SoftcoreScore") is None:
  781      sys.exit(1)
  782  try:
  783      score = int(body["Score"])
  784      softcore = int(body["SoftcoreScore"])
  785  except Exception:
  786      sys.exit(3)
  787  print("score=%d softcore=%d" % (score, softcore))
  788  ' "${QUEUE}" "${USER}" 2>/dev/null)"
  789      local RC=$?
  790      if [ "${RC}" -eq 1 ]; then
  791          return 1
  792      elif [ "${RC}" -ne 0 ]; then
  793          cannot_tell "the proxy's store at ${QUEUE} could not be read"
  794      fi
  795      case "${LINE}" in
  796          score=*\ softcore=*) ;;
  797          *) cannot_tell "the proxy's store answered '${LINE}', not the account's points" ;;
  798      esac
  799      echo "${LINE}"
  800      return 0
  801  }
  802  
  803  do_flushed() {
  804      [ -e "${FLUSH_STAMP}" ] || return 1
  805      # Taken before it is read: the rename is one step, so a stamp the
  806      # service replaces after this moment is a new file this call never
  807      # touches (it is the next caller's), and of two callers only the one
  808      # whose rename succeeded has anything to report. Whatever was taken is
  809      # removed before it is judged, so a stamp that says nothing went, or
  810      # nothing readable, is gone too and never read twice.
  811      local MINE="${FLUSH_STAMP}.$$" LINE
  812      mv -f "${FLUSH_STAMP}" "${MINE}" 2>/dev/null || return 1
  813      LINE="$(head -n 1 "${MINE}" 2>/dev/null)"
  814      rm -f "${MINE}"
  815      if [[ "${LINE}" =~ ^[0-9]+\ [1-9][0-9]*$ ]]; then
  816          echo "${LINE}"
  817          return 0
  818      fi
  819      return 1
  820  }
  821  
  822  # ---- the scan -------------------------------------------------------------
  823  
  824  # The progress file (fork #189): whole or not at all (temp + rename), so a
  825  # reader never sees half a line; RUN_ROUTE is set by the route before its
  826  # first mark. $1 is the rest of the line (" index=<i> total=<n> name=<g>").
  827  mark_running() {
  828      printf 'route=%s at=%s%s\n' "${RUN_ROUTE:-run}" "$(date +%s)" "${1:-}" > "${RUNNING}.tmp" 2>/dev/null \
  829          && mv -f "${RUNNING}.tmp" "${RUNNING}" 2>/dev/null
  830  }
  831  unmark_running() { rm -f "${RUNNING}" "${RUNNING}.tmp"; }
  832  
  833  # A line for the page: ">>> <word> <fields>". Everything else on stdout is
  834  # the client's own output, which the page shows nothing of.
  835  tell() {
  836      printf '>>> %s\n' "$*"
  837  }
  838  
  839  # The scan's own log, rotated once past a megabyte. The client's lines are
  840  # file names and reasons; nothing from system.cfg is ever written here.
  841  slog() {
  842      mkdir -p "${PROXY_DIR}" 2>/dev/null
  843      if [ -e "${SCAN_LOG}" ] && [ "$(stat -c %s "${SCAN_LOG}" 2>/dev/null || echo 0)" -gt 1048576 ]; then
  844          mv -f "${SCAN_LOG}" "${SCAN_LOG}.1"
  845      fi
  846      printf '%s %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" "$*" >> "${SCAN_LOG}"
  847  }
  848  
  849  # How many games are cached, from the client's export. One id per line, so
  850  # the count is the line count; absent means none yet. Falls back to asking
  851  # the client when the export is missing but a store exists, and to 0 when
  852  # even that cannot be read -- a number that is not known is never invented.
  853  # RetroArch's play history (fork #299): the link's return looks for games
  854  # played since the last attempt and nothing else, so a wake with no game
  855  # played costs nothing and shows nothing. RetroArch 1.22 with
  856  # content_history_directory = "default" writes it under playlist_directory
  857  # as builtin/content_history.lpl, beside the video, music and image
  858  # histories -- not at content_history_path, which the config still names
  859  # and which the RG35XX SP never had (fork #306: the check read "no game
  860  # played" at every link for a day). Both are read from retroarch.cfg (~ is
  861  # /storage) and the newest file wins; a missing file loses to one that
  862  # exists. PPSSPP's ppsspp.ini is read beside them: it is the toggle's other
  863  # emulator (D-RA-002), the recently played pass reads its [Recent] list as
  864  # well as RetroArch's history (the client's load_content_history_paths), and
  865  # the file is written at every PPSSPP launch (cheevos_ppsspp.sh) and exit, so
  866  # a game played in PPSSPP alone is a game played (#308 F-RA-13).
  867  # RAOFFLINEPROXY_HISTORY overrides them all (the scripts suite's fixture).
  868  PPSSPP_INI=/storage/.config/ppsspp/PSP/SYSTEM/ppsspp.ini
  869  history_path() {
  870      local CFG=/storage/.config/retroarch/retroarch.cfg P D BUILTIN NEWEST=""
  871      if [ -n "${RAOFFLINEPROXY_HISTORY:-}" ]; then
  872          printf '%s\n' "${RAOFFLINEPROXY_HISTORY}"
  873          return 0
  874      fi
  875      P="$(sed -n 's/^content_history_path = "\(.*\)"$/\1/p' "${CFG}" 2>/dev/null | head -n 1)"
  876      case "${P}" in "~/"*) P="/storage/${P#\~/}" ;; esac
  877      P="${P:-/storage/.config/retroarch/content_history.lpl}"
  878      D="$(sed -n 's/^playlist_directory = "\(.*\)"$/\1/p' "${CFG}" 2>/dev/null | head -n 1)"
```


## raofflineproxy-ctl @ 8ebaf8daad: lines 1111-1208 (excerpt of 2455)

```text
 1111      fi
 1112      [ ! -d "${SCAN_CURSOR}" ] && mv -f "${SCAN_CURSOR}.next" "${SCAN_CURSOR}" 2>/dev/null \
 1113          && [ "$(cat "${SCAN_CURSOR}" 2>/dev/null)" = "${WANT}" ]
 1114  }
 1115  
 1116  # The account EmulationStation signed in with: a user name and either the
 1117  # token it wrote after the sign-in or the password it will sign in with.
 1118  # Presence only; the values stay in system.cfg.
 1119  have_account() {
 1120      [ -n "$(setting "${USER_KEY}")" ] || return 1
 1121      [ -n "$(setting "${TOKEN_KEY}")" ] || [ -n "$(setting "${PASSWORD_KEY}")" ]
 1122  }
 1123  
 1124  # The proxy's own answer to "is RetroAchievements reachable": probe-online
 1125  # sends one HEAD to retroachievements.org (a fresh process asks every time;
 1126  # its thirty-second memory is per process) and writes the answer to
 1127  # online_state.json in its config folder, printing nothing. It is pointed
 1128  # at a folder of its own for the call: the service's online_state.json is
 1129  # the service's (its monitor writes it at start and on a change, and the
 1130  # interface reads it as the proxy's own view, D-RA-011), and a probe from
 1131  # here that lands in a resolver lag would otherwise write "false" over it
 1132  # with nothing to correct it until the service's next transition (#186
 1133  # PL-03). Anything but a readable "online": true reads as offline -- a
 1134  # check that cannot run has not passed.
 1135  is_online() {
 1136      local SCRATCH ANSWER=1
 1137      SCRATCH="$(mktemp -d /tmp/raofflineproxy-probe.XXXXXX)" || return 1
 1138      if RAOFFLINEPROXY_CONFIG_DIR="${SCRATCH}" ${PROXY_PY} probe-online >/dev/null 2>&1; then
 1139          grep -q -E '"online": *true' "${SCRATCH}/online_state.json" 2>/dev/null && ANSWER=0
 1140      fi
 1141      rm -rf "${SCRATCH}"
 1142      return ${ANSWER}
 1143  }
 1144  
 1145  # Seconds left of a run's deadline, from its START; never negative.
 1146  time_left() {
 1147      local L=$(( TOPUP_TIMEOUT - ($(date +%s) - ${1}) ))
 1148      [ "${L}" -gt 0 ] || L=0
 1149      echo "${L}"
 1150  }
 1151  
 1152  # A sleep that a SIGTERM interrupts: the shell waits on a background sleep,
 1153  # and wait returns the moment a trapped signal arrives, so disable is not
 1154  # kept waiting for a probe interval to run out.
 1155  pause() {
 1156      sleep "${1}" &
 1157      wait $! 2>/dev/null
 1158  }
 1159  
 1160  # What both verbs refuse before they touch anything, in the order a player
 1161  # would fix them: the toggle, then the account. Exit codes only; the page
 1162  # says them.
 1163  refuse_unless_ready() {
 1164      local VERB="$1"
 1165      if [ "$(as_flag "$(setting "${KEY}")")" != "1" ]; then
 1166          say "${VERB}: refused, offline RetroAchievements is off"
 1167          tell "why TOGGLE_OFF"
 1168          exit ${EX_CONFIG}
 1169      fi
 1170      if ! have_account; then
 1171          say "${VERB}: refused, no RetroAchievements account is signed in"
 1172          tell "why NO_ACCOUNT"
 1173          exit ${EX_NOPERM}
 1174      fi
 1175  }
 1176  
 1177  # One scan or top-up at a time (the lock is held for the rest of the run;
 1178  # the fd closes with the process). Exit 75 when another holds it -- except
 1179  # for the top-up that follows the interface's index (topup --after-index),
 1180  # which waits its turn for what is left of its deadline ($3, the run's
 1181  # START; the wait spends from the same fifteen minutes as the rest, #186
 1182  # PL-28): it is the one run that knows the index has just grown, and the
 1183  # top-up ahead of it read the index before that. Busybox flock has no -w,
 1184  # so the wait is a loop. The file is opened without truncating it, and the
 1185  # holder writes its pid on the first line once it has the lock, which is
 1186  # how disable finds a run to stop (#186 PL-30) -- a run that finds the lock
 1187  # taken has not wiped the holder's pid by opening the file.
 1188  take_lock() {
 1189      local VERB="$1" WAIT="${2:-0}" START="${3:-0}"
 1190      exec 9<>"${SCAN_LOCK}" || fail "cannot open ${SCAN_LOCK}"
 1191      until flock -n 9; do
 1192          if [ "${WAIT}" -eq 0 ] || [ "$(time_left "${START}")" -le 10 ]; then
 1193              say "${VERB}: another scan or top-up is running"
 1194              exit ${EX_TEMPFAIL}
 1195          fi
 1196          pause 10
 1197      done
 1198      printf '%s\n' "$$" >&9
 1199      # The lock is held, so no run is live: a progress file still here was a
 1200      # run that died without its EXIT trap (a kill -9, a power cut), and the
 1201      # interface has been ignoring it since its 900 s bound. Removed here, at
 1202      # the one point every verb passes (#189 box 3's "and removed"; the
 1203      # seat's G-08 under audit #258).
 1204      rm -f "${RUNNING}" "${RUNNING}.tmp"
 1205  }
 1206  
 1207  # The games to cache, one job per line into $1, in the client's own terms
 1208  # where it has any, and in the interface's where it has the better ones
```


## raofflineproxy-ctl @ 8ebaf8daad: lines 1692-1838 (excerpt of 2455)

```text
 1692      *)   HELPER="/usr/bin/raofflineproxy-cache-indexed"; IMAGE_HELPER="/usr/bin/raofflineproxy-cache-images"; REFRESH_HELPER="/usr/bin/raofflineproxy-refresh" ;;
 1693  esac
 1694  
 1695  # Run the job list $2 of $3 games through the helper and read its lines as
 1696  # they come -- "OK i/n <file>", "FAIL i/n <file>: <reason>", "DONE cached=
 1697  # failed= indexed=" -- stopping it after three lookups in a row that
 1698  # RetroAchievements did not answer, or on a refused sign-in, or when the
 1699  # client reports its cap. $1 is page (the >>> lines for GuiOfflineScan) or
 1700  # quiet (nothing on stdout, for the top-up); $4 a bound in seconds, 0 for
 1701  # none. Leaves R_CACHED R_SKIPPED R_ERRORS R_LIMIT R_WHY R_STOPPED R_INDEXED
 1702  # R_CLIENT_RC for the caller, and the helper's stderr in the scan log. The
 1703  # helper's stdout goes through a fifo so it can be stopped between two lines.
 1704  run_jobs() {
 1705      local MODE="$1" LIST="$2" TOTAL="$3" BUDGET="${4:-0}"
 1706      local -a PATHS
 1707      mapfile -t PATHS < "${LIST}"
 1708      JOBS_FIFO="$(mktemp -u /tmp/raofflineproxy-scan-out.XXXXXX)"
 1709      mkfifo "${JOBS_FIFO}" || fail "cannot create ${JOBS_FIFO}"
 1710      if [ "${BUDGET}" -gt 0 ]; then
 1711          timeout "${BUDGET}" python3 "${HELPER}" "${LIST}" > "${JOBS_FIFO}" 2>>"${SCAN_LOG}" &
 1712      else
 1713          python3 "${HELPER}" "${LIST}" > "${JOBS_FIFO}" 2>>"${SCAN_LOG}" &
 1714      fi
 1715      CLIENT=$!
 1716      exec 8< "${JOBS_FIFO}"
 1717  
 1718      R_CACHED=0; R_SKIPPED=0; R_ERRORS=0; R_LIMIT=0; R_WHY=""; R_STOPPED=0; R_INDEXED=0; R_DONE=0
 1719      local IN_A_ROW=0 line index name
 1720      if [ "${TOTAL}" -gt 0 ]; then
 1721          name="${PATHS[0]##*/}"
 1722          mark_running " index=1 total=${TOTAL} name=${name//[[:space:]]/_}"
 1723          [ "${MODE}" = page ] && tell "game 1|${TOTAL}|${name%.*}"
 1724      fi
 1725      while IFS= read -r line <&8; do
 1726          slog "client: ${line}"
 1727          case "${line}" in
 1728              OK\ *)
 1729                  R_CACHED=$((R_CACHED + 1)); IN_A_ROW=0 ;;
 1730              DONE\ *)
 1731                  # The helper's verdict on the games: whatever the process does
 1732                  # afterwards (badge downloads outliving the bound, fork #188) is
 1733                  # not the run's outcome.
 1734                  R_INDEXED="$(count_of "${line}" indexed)"; R_DONE=1
 1735                  continue ;;
 1736              *"Cache limit reached"*)
 1737                  # The client says it will cache no more (no ROCKNIX client
 1738                  # does since patch 004; kept for one that says so): every
 1739                  # further ROM would be hashed and looked up only to be
 1740                  # refused.
 1741                  R_LIMIT=1; R_STOPPED=1
 1742                  slog "run: the client reports its cache limit; stopping"
 1743                  kill "${CLIENT}" 2>/dev/null
 1744                  break ;;
 1745              *"No RetroAchievements match"*|*"Hash failed"*|*": not found")
 1746                  # Not a game RetroAchievements knows, or not a file it can
 1747                  # read: the proxy's docs skip these silently, and so does
 1748                  # the page -- counted here for the log and the stamp.
 1749                  R_SKIPPED=$((R_SKIPPED + 1)); IN_A_ROW=0 ;;
 1750              *"login required"*|*"HTTP Error 401"*|*"HTTP Error 403"*)
 1751                  # The account, not the link: no retry changes it.
 1752                  R_WHY=SIGN_IN_REFUSED; R_STOPPED=1
 1753                  kill "${CLIENT}" 2>/dev/null
 1754                  break ;;
 1755              FAIL\ *)
 1756                  # A lookup or a fetch that did not come back: the link, the
 1757                  # server, a 429. A run of them is the scan asking a question
 1758                  # nobody is answering.
 1759                  R_ERRORS=$((R_ERRORS + 1)); IN_A_ROW=$((IN_A_ROW + 1))
 1760                  if [ "${IN_A_ROW}" -ge "${ERRORS_IN_A_ROW}" ]; then
 1761                      R_WHY=RETROACHIEVEMENTS_STOPPED_ANSWERING; R_STOPPED=1
 1762                      kill "${CLIENT}" 2>/dev/null
 1763                      break
 1764                  fi ;;
 1765              *)
 1766                  continue ;;
 1767          esac
 1768          # The helper finished game i (1-based); what it is on now is i+1.
 1769          index="${line#* }"; index="${index%%/*}"
 1770          case "${index}" in ''|*[!0-9]*) index=0 ;; esac
 1771          if [ "${index}" -gt 0 ] && [ "${index}" -lt "${TOTAL}" ]; then
 1772              name="${PATHS[${index}]##*/}"
 1773              mark_running " index=$((index + 1)) total=${TOTAL} name=${name//[[:space:]]/_}"
 1774          fi
 1775          [ "${MODE}" = page ] || continue
 1776          tell "cached ${R_CACHED}|${R_SKIPPED}"
 1777          if [ "${index}" -gt 0 ] && [ "${index}" -lt "${TOTAL}" ]; then
 1778              tell "game $((index + 1))|${TOTAL}|${name%.*}"
 1779          fi
 1780      done
 1781      exec 8<&-
 1782      wait "${CLIENT}" 2>/dev/null
 1783      R_CLIENT_RC=$?
 1784      unset CLIENT
 1785      rm -f "${JOBS_FIFO}"; JOBS_FIFO=""
 1786      unmark_running
 1787      if [ "${R_DONE}" -eq 1 ] && [ "${R_CLIENT_RC}" -ne 0 ]; then
 1788          slog "run: the helper had reported DONE and ended with rc ${R_CLIENT_RC} afterwards (badge downloads cut short) -- not the run's verdict (#188)"
 1789      fi
 1790  }
 1791  
 1792  # A run asked to stop (disable's SIGTERM, #186 PL-30) exits through its
 1793  # EXIT trap: the helper is ended, the run's files go, no stamp is written --
 1794  # the line under the row keeps the last run that finished.
 1795  stopped() {
 1796      say "${1}: stopped; offline RetroAchievements was turned off"
 1797      exit 143
 1798  }
 1799  
 1800  # A scan the player cancelled from its page (SIGINT from the interface,
 1801  # fork #241, D-UI-078). Not a failure: what the run saved stays saved, and
 1802  # the next scan passes over those games. So the stamp is written with the
 1803  # counts the run had reached -- the line under the row says SKIPPED and the
 1804  # ready count is right -- the page is told why, and the run exits 130
 1805  # through its EXIT trap (the helper ended, the run's files gone). R_CACHED
 1806  # and the rest are the run's so far; before run_jobs they are unset, and
 1807  # read as 0. added= is measured as the run's own end measures it -- the
 1808  # ready set the run took before its jobs against the store now -- and is
 1809  # unknown when either cannot be read, never the games cached so far
 1810  # (PL-031).
 1811  cancelled() {
 1812      local READY MADE=""
 1813      READY="$(count_ready)"
 1814      if [ -n "${READY_BEFORE:-}" ] && READY_AFTER="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && ready_games_into "${READY_AFTER}"; then
 1815          MADE="$(games_made_ready "${READY_BEFORE}" "${READY_AFTER}")"
 1816      fi
 1817      tell "why CANCELLED"
 1818      write_stamp 130 "${1}" "${R_CACHED:-0}" "${R_SKIPPED:-0}" "${READY}" 0 "${R_INDEXED:-0}" "${R_ERRORS:-0}" CANCELLED "${MADE}"
 1819      slog "${1} cancelled by the player: cached=${R_CACHED:-0} skipped=${R_SKIPPED:-0} errors=${R_ERRORS:-0} ready=${READY}"
 1820      say "${1}: cancelled"
 1821      exit 130
 1822  }
 1823  
 1824  # The images of what is cached, fetched until none is missing (#212). A
 1825  # game's achievements and its images are one action to a player -- the
 1826  # maintainer, 2026-09-18: "whenever we cache the achievements, we cache the
 1827  # images for the achievements" -- so this runs at the end of a scan and of a
 1828  # top-up that cached anything, and on its own as the `images` verb.
 1829  #
 1830  # The helper walks the store, not the library: every cached set row, every
 1831  # image path in it, and the ones with no file get fetched. Idempotent (the
 1832  # check is the file's existence and the client's own download no-ops on one)
 1833  # and resumable (nothing marks a game done but its files), so a run that
 1834  # stops at its ceiling costs the next one nothing. Bounded by what is left of
 1835  # the caller's deadline, or IMAGE_PASS_SECONDS on its own.
 1836  #
 1837  # Its verdict is part of the run's (#307 PL-060). A game whose badges are
 1838  # missing offline reads as half working (D-RA-027), and a run whose parts
```


## raofflineproxy-ctl @ 8ebaf8daad: lines 1957-2118 (excerpt of 2455)

```text
 1957      timeout "$(( TOPUP_TIMEOUT + 60 ))" "${REFRESH_HELPER}" --seconds "${TOPUP_TIMEOUT}" "${WHICH[@]}" &
 1958      CLIENT=$!
 1959      wait "${CLIENT}" || RC=$?
 1960      CLIENT=""
 1961      slog "refresh: rc=${RC} ${WHICH[*]}"
 1962      exit "${RC}"
 1963  }
 1964  
 1965  do_scan() {
 1966      trap 'stopped scan' TERM
 1967      trap 'cancelled scan' INT
 1968      RUN_ROUTE=scan
 1969      take_lock scan
 1970      refuse_unless_ready scan
 1971      mkdir -p "${PROXY_DIR}" || fail "cannot create ${PROXY_DIR}"
 1972      if ! is_online; then
 1973          say "scan: refused, RetroAchievements is not reachable"
 1974          slog "scan refused: offline by the proxy's probe"
 1975          exit ${EX_UNAVAILABLE}
 1976      fi
 1977  
 1978      local LIST
 1979      LIST="$(mktemp /tmp/raofflineproxy-scan.XXXXXX)" || fail "cannot create the list"
 1980      # Everything of the run's goes when the run does, however it ends.
 1981      trap 'rm -f "${LIST}" "${JOBS_FIFO:-}" "${READY_BEFORE:-}" "${READY_AFTER:-}" "${SCAN_CURSOR}.next" "${RUNNING}" "${RUNNING}.tmp"; [ -n "${CLIENT:-}" ] && kill "${CLIENT}" 2>/dev/null' EXIT
 1982  
 1983      local COUNTS
 1984      R_IMAGES_WHY=""
 1985      mark_running
 1986      tell "doing listing"
 1987      if ! COUNTS="$(list_jobs "${LIST}" all 0 2>>"${SCAN_LOG}")"; then
 1988          slog "scan: the library could not be listed"
 1989          tell "why LIBRARY_UNREADABLE"
 1990          write_stamp 1 scan 0 0 "$(count_ready)" 0 0 0 LIBRARY_UNREADABLE
 1991          exit 1
 1992      fi
 1993      local FOUND NEW TRUNC
 1994      FOUND="$(count_of "${COUNTS}" found)"
 1995      NEW="$(count_of "${COUNTS}" new)"
 1996      TRUNC="$(count_of "${COUNTS}" truncated)"
 1997      slog "scan start: ${COUNTS}"
 1998      if [ "${TRUNC}" -eq 1 ]; then
 1999          slog "scan: the walk stopped at the client's cap of files per run; the next scan walks on from ${SCAN_CURSOR}"
 2000      fi
 2001  
 2002      local READY
 2003      if [ "${FOUND}" -eq 0 ]; then
 2004          # Nothing under the ROM folders to look at is a run that completed
 2005          # with nothing to do, not one that could not finish (fork #329: the
 2006          # page read COULDN'T FINISH on a device with no game yet, and the
 2007          # maintainer's reading was that "there was just nothing to scan").
 2008          # rc 0 and no why; the note tells the page and the stamp what there
 2009          # was to say, and the row reads NO GAMES TO SCAN YET.
 2010          READY="$(count_ready)"
 2011          slog "scan done: no games found under ${ROMS_ROOT}, ready=${READY}"
 2012          tell "note NO_GAMES"
 2013          commit_cursor || slog "scan: an old cursor could not be removed; the next walk starts from the top all the same"
 2014          write_stamp 0 scan 0 0 "${READY}" 0 0 0 "" "" 0 NO_GAMES
 2015          tell "done 0|0|${READY}|0"
 2016          exit 0
 2017      fi
 2018      tell "total ${NEW}"
 2019      if [ "${NEW}" -eq 0 ]; then
 2020          tell "note NOTHING_NEW"
 2021          commit_cursor || slog "scan: an old cursor could not be removed; the next walk starts from the top all the same"
 2022          # No game to cache, but the images of what is cached may still be
 2023          # missing -- a pass the last run cut, a badge that did not come --
 2024          # and pressing SCAN again is how a player asks for them (#307
 2025          # PL-060). The same pass, the same verdict.
 2026          run_image_pass scan "${IMAGE_PASS_SECONDS}"
 2027          READY="$(count_ready)"
 2028          local RC0=0 WHY0="${R_IMAGES_WHY}"
 2029          [ -n "${WHY0}" ] && { RC0=1; tell "why ${WHY0}"; }
 2030          slog "scan done: nothing new, ready=${READY}${WHY0:+ why=${WHY0}}"
 2031          write_stamp "${RC0}" scan 0 0 "${READY}" 0 0 0 "${WHY0}"
 2032          tell "done 0|0|${READY}|0"
 2033          exit "${RC0}"
 2034      fi
 2035  
 2036      READY_BEFORE="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && { ready_games_into "${READY_BEFORE}" || { rm -f "${READY_BEFORE}"; READY_BEFORE=""; }; }
 2037      run_jobs page "${LIST}" "${NEW}" 0
 2038  
 2039      READY="$(count_ready)"
 2040      local ADDED=""
 2041      READY_AFTER="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && ready_games_into "${READY_AFTER}" && ADDED="$(games_made_ready "${READY_BEFORE}" "${READY_AFTER}")"
 2042      rm -f "${READY_BEFORE}" "${READY_AFTER}"; READY_BEFORE=""; READY_AFTER=""
 2043      # A measurement that failed is said as one (added_count, PL-031).
 2044      ADDED="$(added_count "${ADDED}" "${R_CACHED}")"
 2045      [ "${ADDED}" = "unknown" ] && slog "scan: the store could not be read before or after the jobs; how many games they made ready is not known (added=unknown)"
 2046      local RC=0 WHY="${R_WHY}"
 2047      if [ -n "${WHY}" ]; then
 2048          RC=1
 2049      elif [ "${R_STOPPED}" -eq 0 ] && [ "${R_CLIENT_RC}" -ne 0 ] && [ "${R_DONE}" -eq 0 ]; then
 2050          # The helper died on its own, before its DONE, without a reason the
 2051          # lines above named: the log has its traceback. (After DONE the games
 2052          # are cached and the exit is the badge downloads', fork #188.)
 2053          RC=1; WHY=SOMETHING_WENT_WRONG
 2054      elif [ "${R_ERRORS}" -gt 0 ]; then
 2055          # A fetch that failed for any game, even between games that went
 2056          # through, is a run that did not finish (D-UI-030: a run whose
 2057          # parts disagree is COULDN'T FINISH); the next run tries them again.
 2058          RC=1; WHY=SOME_GAMES_NOT_SAVED
 2059      fi
 2060      # The images of what this run cached, and of anything cached before it
 2061      # that is still missing one (#212): the same action, finished.
 2062      # The scan has no deadline of its own (the top-up's TOPUP_TIMEOUT is the
 2063      # one clock here), so the pass gets its own ceiling.
 2064      # Whenever the run worked through its jobs -- cached one or not: a
 2065      # library with a ROM RetroAchievements does not know lists a job at
 2066      # every scan, and gating the pass on a cached game left such a scan
 2067      # COMPLETED over badges it never looked at (audit of the fixes, claude
 2068      # G-D-02 = gpt G-D-01). Not after a stop on a refused sign-in or a
 2069      # server that stopped answering.
 2070      [ "${R_STOPPED}" -eq 0 ] && run_image_pass scan "${IMAGE_PASS_SECONDS}"
 2071      # The games' own why comes first; a pass that left images behind is the
 2072      # run's why when the games went through (#307 PL-060).
 2073      if [ -z "${WHY}" ] && [ -n "${R_IMAGES_WHY}" ]; then
 2074          RC=1; WHY="${R_IMAGES_WHY}"
 2075      fi
 2076  
 2077      # The walk's cursor is kept once the run has worked through its jobs; a
 2078      # run stopped short leaves it where it was (claude G-D-06). A cut walk
 2079      # whose cursor could not be kept promises no continuation: the run could
 2080      # not finish, and neither the page nor the stamp says TRUNCATED (gpt
 2081      # G-D-06).
 2082      if [ "${R_DONE}" -eq 1 ] && [ "${R_STOPPED}" -eq 0 ]; then
 2083          if [ "${TRUNC}" -eq 1 ]; then
 2084              if [ "$(count_of "${COUNTS}" cursor_saved)" -ne 1 ] || ! commit_cursor; then
 2085                  slog "scan: the walk's cursor could not be saved; the next scan would take the same slice"
 2086                  TRUNC=0
 2087                  [ -z "${WHY}" ] && { RC=1; WHY=SOMETHING_WENT_WRONG; }
 2088              fi
 2089          else
 2090              commit_cursor || slog "scan: an old cursor could not be removed; the next walk starts from the top all the same"
 2091          fi
 2092      elif [ "${TRUNC}" -eq 1 ]; then
 2093          slog "scan: the run stopped short of its jobs; the cursor stays where it was"
 2094      fi
 2095      rm -f "${SCAN_CURSOR}.next"
 2096      [ "${R_LIMIT}" -eq 1 ] && tell "note LIMIT_REACHED"
 2097      # Not every folder was walked: the page says so (GuiOfflineScan's
 2098      # NOT EVERY FOLDER WAS LOOKED AT. SCAN AGAIN TO CONTINUE.) and the stamp
 2099      # carries it -- the log alone said it before (#307 PL-059).
 2100      [ "${TRUNC}" -eq 1 ] && tell "note TRUNCATED"
 2101      [ "${R_ERRORS}" -gt 0 ] && tell "errors ${R_ERRORS}"
 2102      [ -n "${WHY}" ] && tell "why ${WHY}"
 2103      write_stamp "${RC}" scan "${R_CACHED}" "${R_SKIPPED}" "${READY}" "${R_LIMIT}" "${R_INDEXED}" "${R_ERRORS}" "${WHY}" "${ADDED}" "${TRUNC}"
 2104      slog "scan done: rc=${RC} cached=${R_CACHED} indexed=${R_INDEXED} skipped=${R_SKIPPED} errors=${R_ERRORS} ready=${READY} limit=${R_LIMIT}${WHY:+ why=${WHY}}"
 2105      say "scan: cached ${R_CACHED} (${R_INDEXED} from the index), skipped ${R_SKIPPED}, ${READY} ready${WHY:+; ${WHY}}"
 2106      tell "done ${R_CACHED}|${R_SKIPPED}|${READY}|${R_LIMIT}"
 2107      exit "${RC}"
 2108  }
 2109  
 2110  # index-offline: the interface's index had games to identify and
 2111  # RetroAchievements' hash library did not come -- offline, nearly always
 2112  # (fork #299, D-UI-104). The marker the after-index run leaves when its
 2113  # probe fails is written here without a probe, since the interface already
 2114  # knows the library did not come: the next link-return topup lists the
 2115  # library once, inside the half hour or not, and clears it once that
 2116  # listing's games are handled. The games this index could not identify are
 2117  # not among them -- they have no cheevosId until an index with the library
 2118  # gives them one; the interface runs that index when the link comes up, and
```


## raofflineproxy-ctl @ 8ebaf8daad: lines 2129-2273 (excerpt of 2455)

```text
 2129  # (ack_index_pending), and a write takes it too, so an index's newer marker
 2130  # cannot land between that check and that removal and go with the older
 2131  # one. It is held for a read, a rename or an unlink, never across anything
 2132  # that waits. Busybox flock has no -w: five tries a second apart. A lock
 2133  # that cannot be had leaves the safe side -- the write goes ahead, since a
 2134  # notification lost leaves the player's games uncached, and the removal
 2135  # does not, since a marker kept costs one more listing.
 2136  PENDING_LOCK="/var/run/raofflineproxy-index-pending.lock"
 2137  pending_lock() {
 2138      local TRY=0
 2139      exec 6<>"${PENDING_LOCK}" 2>/dev/null || return 1
 2140      until flock -n 6; do
 2141          TRY=$((TRY + 1))
 2142          if [ "${TRY}" -ge 5 ]; then exec 6>&-; return 1; fi
 2143          sleep 1
 2144      done
 2145  }
 2146  
 2147  pending_unlock() {
 2148      exec 6>&-
 2149  }
 2150  
 2151  write_index_pending() {
 2152      local LOCKED=0 RC=0
 2153      if pending_lock; then LOCKED=1; else say "index-pending: its lock could not be had; written without it"; fi
 2154      printf '%s %s %s\n' "$(date +%s)" "$$" "${RANDOM}" > "${INDEX_PENDING}.tmp" 2>/dev/null \
 2155          && mv -f "${INDEX_PENDING}.tmp" "${INDEX_PENDING}" || RC=1
 2156      [ "${LOCKED}" -eq 1 ] && pending_unlock
 2157      return "${RC}"
 2158  }
 2159  
 2160  # ack_index_pending <token>: remove index-pending if it is still the marker
 2161  # the caller's listing was made for. 0 removed, 1 kept (a newer marker), 2
 2162  # kept because the lock could not be had.
 2163  ack_index_pending() {
 2164      # Taken aside by rename before it is read: a writer that could not have
 2165      # the lock renames a newer marker into place (write_index_pending's
 2166      # fallback), and a compare-then-rm on the shared path removed that newer
 2167      # one (the audit of the fixes, gpt G3-D-03). Whatever lands on the path
 2168      # after the rename is somebody else's and stays; a moved marker that is
 2169      # not the caller's token goes back.
 2170      local RC=1 mine="${INDEX_PENDING}.ack.$$"
 2171      pending_lock || return 2
 2172      if mv -f "${INDEX_PENDING}" "${mine}" 2>/dev/null; then
 2173          if [ "$(cat "${mine}" 2>/dev/null)" = "${1}" ]; then
 2174              rm -f "${mine}" && [ ! -e "${mine}" ] && RC=0
 2175          else
 2176              [ -e "${INDEX_PENDING}" ] || mv -f "${mine}" "${INDEX_PENDING}" 2>/dev/null
 2177              rm -f "${mine}" 2>/dev/null
 2178          fi
 2179      fi
 2180      pending_unlock
 2181      return "${RC}"
 2182  }
 2183  
 2184  do_index_offline() {
 2185      mkdir -p "${PROXY_DIR}" || fail "cannot create ${PROXY_DIR}"
 2186      write_index_pending || fail "cannot write ${INDEX_PENDING}"
 2187      slog "index ran offline: the hash library did not come (index-pending); the library is listed once at the link's return"
 2188  }
 2189  
 2190  # topup [--after-index]. --after-index is the run the interface starts as
 2191  # its hasher finishes (ThreadedHasher, with the toggle on): it waits for a
 2192  # top-up already running instead of giving way to it, and it does not count
 2193  # the half-hour since the last attempt against itself -- the index has just
 2194  # grown, and that is the one moment a top-up is sure to have something to
 2195  # do. It marks the attempt like any other, once its probe has answered.
 2196  do_topup() {
 2197      local AFTER_INDEX=0 AI_NOTE=""
 2198      RUN_ROUTE=topup
 2199      if [ "${1:-}" = "--after-index" ]; then AFTER_INDEX=1; AI_NOTE=" (after the index)"; fi
 2200      trap 'stopped topup' TERM
 2201      # One deadline, taken before anything can wait: the lock, the probes,
 2202      # the listing and both passes all spend from it, so the run ends within
 2203      # TOPUP_TIMEOUT of this moment whatever each part costs (#186 PL-28).
 2204      local START
 2205      START="$(date +%s)"
 2206      take_lock topup "${AFTER_INDEX}" "${START}"
 2207      refuse_unless_ready topup >/dev/null
 2208      mkdir -p "${PROXY_DIR}" || fail "cannot create ${PROXY_DIR}"
 2209  
 2210      # Bounded: one attempt per interval, whatever the link does. The mark
 2211      # is read here and set only below, once a probe has reached the server.
 2212      # An index that ran offline (index-pending, below) is the one reason to
 2213      # run inside the interval: the player added games and the toast said
 2214      # they are looked up next time the device is connected (fork #299,
 2215      # D-UI-104), and "next time" is this link, not the one after the half
 2216      # hour. Only a marker written since the last attempt: one a failed
 2217      # attempt left behind (#307 PL-055, below) waits out the half hour like
 2218      # any other run, so a link that flaps does not turn it into a request
 2219      # storm.
 2220      local PENDING_DUE=0
 2221      if [ -e "${INDEX_PENDING}" ] && { [ ! -e "${TOPUP_MARK}" ] || [ "${INDEX_PENDING}" -nt "${TOPUP_MARK}" ]; }; then
 2222          PENDING_DUE=1
 2223      fi
 2224      if [ "${AFTER_INDEX}" -eq 0 ] && [ -e "${TOPUP_MARK}" ] && [ "${PENDING_DUE}" -eq 0 ]; then
 2225          local AGE=$(( $(date +%s) - $(stat -c %Y "${TOPUP_MARK}" 2>/dev/null || echo 0) ))
 2226          if [ "${AGE}" -ge 0 ] && [ "${AGE}" -lt "${TOPUP_INTERVAL}" ]; then
 2227              exit 0
 2228          fi
 2229          # The link's return has one question -- was a game played since the
 2230          # last attempt? -- and no game means nothing to look for: out before
 2231          # the probe, the mark untouched (fork #299, D-RA-035: the maintainer,
 2232          # a nine-second check at wake with nothing to add).
 2233          local HIST
 2234          HIST="$(history_path)"
 2235          if [ ! -e "${INDEX_PENDING}" ] && { [ ! -e "${HIST}" ] || [ ! "${HIST}" -nt "${TOPUP_MARK}" ]; }; then
 2236              slog "topup: no game played since the last attempt (${HIST} is not newer than the mark); nothing to look for, skipped"
 2237              exit 0
 2238          fi
 2239      fi
 2240  
 2241      # The hook fires when the address arrives, which can be well before the
 2242      # resolver answers (fork #175: 20-45 s behind on that boot shape), so
 2243      # the probe gets the token check's patience -- PROBE_TRIES tries,
 2244      # PROBE_INTERVAL apart, inside the deadline. A probe that never reached
 2245      # RetroAchievements is not an attempt: no mark, so the next link event
 2246      # (or the after-index run) tries again rather than waiting out the half
 2247      # hour on a connect that was never tested (#186 PL-04).
 2248      local TRY=0 ONLINE=0
 2249      while [ "${TRY}" -lt "${PROBE_TRIES}" ]; do
 2250          TRY=$((TRY + 1))
 2251          if is_online; then ONLINE=1; break; fi
 2252          [ "${TRY}" -lt "${PROBE_TRIES}" ] || break
 2253          [ "$(time_left "${START}")" -gt "${PROBE_INTERVAL}" ] || break
 2254          pause "${PROBE_INTERVAL}"
 2255      done
 2256      if [ "${ONLINE}" -eq 0 ]; then
 2257          slog "topup refused: offline by the proxy's probe (${TRY} probes); not counted as an attempt"
 2258          if [ "${AFTER_INDEX}" -eq 1 ]; then
 2259              write_index_pending
 2260              slog "topup: the index's games wait for the link (index-pending)"
 2261          fi
 2262          exit ${EX_UNAVAILABLE}
 2263      fi
 2264      touch "${TOPUP_MARK}"
 2265  
 2266      local LIST
 2267      LIST="$(mktemp /tmp/raofflineproxy-topup.XXXXXX)" || fail "cannot create the list"
 2268      trap 'rm -f "${LIST}" "${JOBS_FIFO:-}" "${SC_OUT:-}" "${READY_BEFORE:-}" "${READY_AFTER:-}" "${RUNNING}" "${RUNNING}.tmp"; [ -n "${CLIENT:-}" ] && kill "${CLIENT}" 2>/dev/null' EXIT
 2269      mark_running
 2270      # The games ready for this account before either pass, for added=.
 2271      READY_BEFORE="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && { ready_games_into "${READY_BEFORE}" || { rm -f "${READY_BEFORE}"; READY_BEFORE=""; }; }
 2272  
 2273      # First, every game the interface's index knows and the client has not
```


## raofflineproxy-ctl @ 8ebaf8daad: lines 2392-2455 (excerpt of 2455)

```text
 2392      # A listing that could not be read is the run's why when nothing later
 2393      # had one of its own.
 2394      [ -z "${WHY}" ] && [ -n "${LIST_WHY}" ] && WHY="${LIST_WHY}"
 2395      local READY MADE
 2396      READY="$(count_ready)"
 2397      # added=: the games the two passes made ready for this account, from the
 2398      # store before and after (#308 F-RA-10, F-RA-15); unknown when the store
 2399      # could not be read, never the passes' cache operations in its place
 2400      # (added_count, PL-031).
 2401      READY_AFTER="$(mktemp /tmp/raofflineproxy-ready.XXXXXX 2>/dev/null)" && ready_games_into "${READY_AFTER}" && MADE="$(games_made_ready "${READY_BEFORE}" "${READY_AFTER}")" && ADDED="${MADE}"
 2402      rm -f "${READY_BEFORE}" "${READY_AFTER}"; READY_BEFORE=""; READY_AFTER=""
 2403      ADDED="$(added_count "${ADDED}" "${CACHED}")"
 2404      [ "${ADDED}" = "unknown" ] && slog "topup${AI_NOTE}: the store could not be read before or after the passes; how many games they made ready is not known (added=unknown)"
 2405      slog "topup done: cached=${CACHED} added=${ADDED} indexed=${INDEXED} skipped=${SKIPPED} errors=${ERRORS} ready=${READY} limit=${LIMIT} took=$(( $(date +%s) - START ))s${WHY:+ why=${WHY}}"
 2406  
 2407      # The line under the row changes only when the top-up has something to
 2408      # say: games it added, or a run that could not finish. Nothing new
 2409      # leaves the last scan's line as it was.
 2410      if [ -n "${WHY}" ]; then
 2411          write_stamp 1 topup "${CACHED}" "${SKIPPED}" "${READY}" "${LIMIT}" "${INDEXED}" "${ERRORS}" "${WHY}" "${ADDED}"
 2412          say "topup could not finish (${WHY}); cached ${CACHED}, ${READY} ready"
 2413          exit 1
 2414      fi
 2415      if [ "${CACHED}" -gt 0 ]; then
 2416          # The top-up is the background run, so it is where the store is
 2417          # verified as well as filled: a slice per run from the cursor, so
 2418          # the whole store comes round without any one run being long (#213).
 2419          run_image_pass topup "$(time_left "${START}")" --verify
 2420          if [ -n "${R_IMAGES_WHY}" ]; then
 2421              # The games are cached; their images are not all there (#307
 2422              # PL-060): a run whose parts disagree could not finish.
 2423              write_stamp 1 topup "${CACHED}" "${SKIPPED}" "${READY}" "${LIMIT}" "${INDEXED}" "${ERRORS}" "${R_IMAGES_WHY}" "${ADDED}"
 2424              say "topup could not finish (${R_IMAGES_WHY}); cached ${CACHED}, ${READY} ready"
 2425              exit 1
 2426          fi
 2427          write_stamp 0 topup "${CACHED}" "${SKIPPED}" "${READY}" "${LIMIT}" "${INDEXED}" "${ERRORS}" "" "${ADDED}"
 2428          say "topup: cached ${CACHED} game(s), ${INDEXED} from the index; ${READY} ready"
 2429      fi
 2430      exit 0
 2431  }
 2432  
 2433  case "${1:-}" in
 2434      enable)  do_enable ;;
 2435      disable) do_disable ;;
 2436      start)   do_start ;;
 2437      stop)    do_stop ;;
 2438      status)  do_status ;;
 2439      pending) do_pending ;;
 2440      pending-ids) do_pending_ids ;;
 2441      account) do_account ;;
 2442      summary) do_summary ;;
 2443      flushed) do_flushed ;;
 2444      scan)    do_scan ;;
 2445      topup)   do_topup "${2:-}" ;;
 2446      index-offline) do_index_offline ;;
 2447      ready)   do_ready ;;
 2448      listening) do_listening "${2:-}" "${3:-}" ;;
 2449      images)  do_images "${2:-}" ;;
 2450      refresh) do_refresh "${2:-}" "${3:-}" ;;
 2451      *)
 2452          echo "Usage: raofflineproxy-ctl {enable|disable|start|stop|status|pending|pending-ids|account|summary|flushed|scan|topup [--after-index]|index-offline|images [--verify]|refresh [--all|--game <id>]|listening [--wait <seconds>]|ready}" >&2
 2453          exit 2
 2454      ;;
 2455  esac
```
