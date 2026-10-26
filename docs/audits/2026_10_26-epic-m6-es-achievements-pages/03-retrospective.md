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
