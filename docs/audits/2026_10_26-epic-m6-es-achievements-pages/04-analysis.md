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
