# Research notes — M6.P2 T20, EmulationStation's RetroAchievements and offline pages (#667)

## Scope

**The membership block** (brief § 2), run in the distribution worktree at `ae3c013cac`, with `W` the ES worktree at the pin `16dbac5211`:

```
selects 2 paths 25 lines 7485 {'shipped': 25} {'fork-own': 24, 'upstream-carried': 1}
{'c++': 10, 'c-header': 10, 'cmake': 1, 'other': 1, 'markdown': 1, 'c': 2}
read 23 7427 unread ['external/libcheevos/LICENSE.rvz-padding', 'external/libcheevos/RVZ-NOTICES.md']
fork-own 24 7474
libcheevos rows 9 2556
353 c++ fork-own es-app/src/OfflineAchievements.cpp
25 .qa-scratch/t20/paths.txt
wc -l lines 7485
15
```

**As the brief states:** 25 paths, 7,485 lines; read 23 / 7,427 (unread: the two notices); fork-own 24 / 7,474; libcheevos 9 / 2,556; 15 in the merge base. `.qa-scratch/t20/paths.txt` holds the 25.

**The 25, with each file's history since the merge base** (`git rev-list --count bccd715707..<pin> -- <path>`; the last commit at the pin):

| File | Lines at the pin | Language | Tier | In the merge base `bccd715707` | Commits since it | Last commit |
| --- | ---: | --- | --- | --- | ---: | --- |
| `es-app/src/OfflineAchievements.cpp` | 353 | c++ | fork-own | no | 17 | 747593f66 2026-09-28 OfflineAchievements: signal only the pid that holds the run lock |
| `es-app/src/OfflineAchievements.h` | 148 | c-header | fork-own | no | 9 | 19319821c 2026-09-28 RetroAchievements: offline, the summary does not ask for a web key |
| `es-app/src/OfflineScanJob.cpp` | 273 | c++ | fork-own | no | 8 | c0cb9925e 2026-09-29 offline achievements: no games completes, sign in before the offer, t |
| `es-app/src/OfflineScanJob.h` | 100 | c-header | fork-own | no | 5 | c0cb9925e 2026-09-29 offline achievements: no games completes, sign in before the offer, t |
| `es-app/src/RetroAchievements.cpp` | 1072 | c++ | fork-own | yes | 13 | 435a506b5 2026-09-28 OfflineAchievementsText: a null unlock count is unknown, not none |
| `es-app/src/RetroAchievements.h` | 286 | c-header | fork-own | yes | 5 | 435a506b5 2026-09-28 OfflineAchievementsText: a null unlock count is unknown, not none |
| `es-app/src/ThreadedHasher.cpp` | 415 | c++ | fork-own | yes | 8 | 5a86caea9 2026-10-13 ThreadedHasher: retry failed GameCube RVZ hashes without an id |
| `es-app/src/ThreadedHasher.h` | 76 | c-header | fork-own | yes | 3 | cce9ab12a 2026-09-14 SystemData.cpp, main.cpp, NetworkThread.cpp, ThreadedHasher.cpp: the  |
| `es-app/src/guis/GuiGameAchievements.cpp` | 352 | c++ | fork-own | yes | 5 | e2023b2f3 2026-09-15 GuiRetroAchievements.cpp, GuiGameAchievements.cpp, emulationstation2. |
| `es-app/src/guis/GuiGameAchievements.h` | 35 | c-header | fork-own | yes | 2 | 986f1749c 2026-09-14 RetroAchievements.cpp, GuiGameAchievements.cpp, GuiRetroAchievements. |
| `es-app/src/guis/GuiOfflineScan.cpp` | 382 | c++ | fork-own | no | 12 | c0cb9925e 2026-09-29 offline achievements: no games completes, sign in before the offer, t |
| `es-app/src/guis/GuiOfflineScan.h` | 93 | c-header | fork-own | no | 4 | acd7a6fee 2026-09-22 Scan, transfer and scrape pages: sat in, with CANCEL; nothing runs in |
| `es-app/src/guis/GuiRetroAchievements.cpp` | 471 | c++ | fork-own | yes | 4 | 435a506b5 2026-09-28 OfflineAchievementsText: a null unlock count is unknown, not none |
| `es-app/src/guis/GuiRetroAchievements.h` | 54 | c-header | fork-own | yes | 1 | e2023b2f3 2026-09-15 GuiRetroAchievements.cpp, GuiGameAchievements.cpp, emulationstation2. |
| `es-app/src/guis/GuiRetroAchievementsSettings.cpp` | 808 | c++ | fork-own | yes | 22 | c0cb9925e 2026-09-29 offline achievements: no games completes, sign in before the offer, t |
| `es-app/src/guis/GuiRetroAchievementsSettings.h` | 11 | c-header | upstream-carried | yes | 0 | 2c7c79bf2 2021-12-30 Scraper : Invert screens cinematic + split GuiSystemInformation, GuiS |
| `external/libcheevos/CMakeLists.txt` | 245 | cmake | fork-own | yes | 1 | 1a4a2f12c 2026-10-13 libcheevos: prepare bounded GameCube RVZ hash reader |
| `external/libcheevos/LICENSE.rvz-padding` | 29 | other | fork-own | no | 1 | 1a4a2f12c 2026-10-13 libcheevos: prepare bounded GameCube RVZ hash reader |
| `external/libcheevos/RVZ-NOTICES.md` | 29 | markdown | fork-own | no | 1 | 1a4a2f12c 2026-10-13 libcheevos: prepare bounded GameCube RVZ hash reader |
| `external/libcheevos/cheevos.cpp` | 193 | c++ | fork-own | yes | 2 | 5a86caea9 2026-10-13 ThreadedHasher: retry failed GameCube RVZ hashes without an id |
| `external/libcheevos/cheevos.h` | 8 | c-header | fork-own | yes | 1 | 5a86caea9 2026-10-13 ThreadedHasher: retry failed GameCube RVZ hashes without an id |
| `external/libcheevos/libretro-common/src/utils/md5.c` | 304 | c | fork-own | yes | 1 | 314da58d6 2026-10-14 libcheevos: read MD5 words without alignment assumptions |
| `external/libcheevos/rcheevos/src/rhash/hash_disc.c` | 1352 | c | fork-own | yes | 1 | 1a4a2f12c 2026-10-13 libcheevos: prepare bounded GameCube RVZ hash reader |
| `external/libcheevos/rvz_hash.cpp` | 389 | c++ | fork-own | no | 1 | 1a4a2f12c 2026-10-13 libcheevos: prepare bounded GameCube RVZ hash reader |
| `external/libcheevos/rvz_hash.h` | 7 | c-header | fork-own | no | 1 | 1a4a2f12c 2026-10-13 libcheevos: prepare bounded GameCube RVZ hash reader |

- The eight account files and the hasher are ROCKNIX's, rewritten. `GuiRetroAchievementsSettings.h` has had no commit since the base: it is the one upstream-carried row.
- The libcheevos rows came in three commits: `1a4a2f12c` (2026-10-13, the RVZ reader, the notices, `CMakeLists.txt`, `hash_disc.c`), `5a86caea9` (2026-10-13, `cheevos.cpp`/`.h` and the hasher's RVZ retry) and `314da58d6` (2026-10-14, `md5.c`).

## The runs at stage A

The brief's § 5 commands, each timed, with its exit on its own line: R0 rc 0 (0.00 s); R1 rc 0 (0.02 s); R2 rc 0 (0.01 s); R3 rc 0 (0.01 s); R4 rc 0 (0.01 s); R5 rc 0 (0.02 s); R6 rc 0 (0.01 s); R7 rc 0 (0.01 s); R8 rc 0 (0.01 s); R9 rc 0 (0.01 s); R10 rc 0 (0.28 s); R11 rc 1 (0.13 s); R12 rc 0 (0.04 s); R13 rc 0 (0.02 s); R14 rc 1 (0.02 s); R16 rc 0 (0.01 s); R17 rc 0 (0.13 s); R18 rc 0 (0.01 s). R11 exits 1 and R14 exits 1 only because the last `grep -c` in each counts 0 (the scan page's whole title in the map; the word regex). The figures and their *a FAIL would mean* go to `02` § The runs at stage B. The deltas from the brief are in `00` § Stage A: R5's 11 files, R14's 0 by word and 6 by subject, R17's headers.

## The callers of the 25's entry points (at the pin)

```
-- OfflineAchievements::: es-app/src/CloudText.cpp es-app/src/OfflineScanJob.cpp es-app/src/ProxyCards.cpp es-app/src/RetroAchievements.cpp es-app/src/RunLock.h es-app/src/ThreadedCloudSync.cpp es-app/src/ThreadedHasher.cpp es-app/src/guis/GuiMenu.cpp es-app/src/guis/GuiOfflineScan.cpp es-app/src/guis/GuiRetroAchievementsSettings.cpp es-app/tests/unit/CloudTextTests.cpp 
-- RetroAchievements::: es-app/src/FileData.cpp es-app/src/NetworkThread.cpp es-app/src/ThreadedHasher.cpp es-app/src/guis/GuiGameAchievements.cpp es-app/src/guis/GuiMenu.cpp es-app/src/guis/GuiRetroAchievementsSettings.cpp es-app/src/views/SystemView.cpp 
-- ThreadedHasher::start(: es-app/src/SystemData.cpp es-app/src/ThreadedHasher.cpp es-app/src/guis/GuiHashStart.cpp es-app/src/guis/GuiMenu.cpp es-app/src/guis/GuiNetPlaySettings.cpp es-app/src/guis/GuiRetroAchievementsSettings.cpp 
-- GuiOfflineScan(: es-app/src/guis/GuiRetroAchievementsSettings.cpp 
-- OfflineScanJob: es-app/CMakeLists.txt es-app/src/CloudTransferJob.cpp es-app/src/CloudTransferJob.h es-app/src/guis/GuiOfflineScan.cpp es-app/src/guis/GuiOfflineScan.h es-app/src/guis/GuiRetroAchievementsSettings.cpp es-app/tests/unit/CloudTextTests.cpp es-app/tests/unit/README.md 
-- GuiRetroAchievementsSettings: es-app/CMakeLists.txt es-app/src/guis/GuiMenu.cpp 
-- GuiRetroAchievements(: 
-- GuiGameAchievements(: 
-- generateHashFromFile: es-app/src/RetroAchievements.cpp 
-- gameCubeRvzHashEnabled: es-app/src/ThreadedHasher.cpp
```

- `GuiRetroAchievements::show` is entered from `GuiMenu.cpp:198` and `:5767` and from `SystemView.cpp:1621`.
- `GuiGameAchievements::show` is entered from `GuiGameOptions.cpp:128`, `:136` and `ISimpleGameListView.cpp:873`.
- `GuiOfflineScan` is entered only from `GuiRetroAchievementsSettings.cpp`.
- `ThreadedHasher::start(` has five direct call sites, plus `NetworkThread.cpp:251` through `postToUiThread` (R9).

## The issues the tree names (read on GitHub at stage A)

- #186 [CLOSED] Audit: Offline RetroAchievements (epic #163, the sixth candidate) — 33 findings (0 critical, 2 high)
- #241 [CLOSED] EmulationStation: long jobs run on a foreground page with CANCEL, never in the background (D-UI-078)
- #292 [OPEN] Show the send when it happens: a card on the link's return for the offline awards the proxy flushes and the saves sync the exit 
- #293 [OPEN] Every automatic process in the saves and achievements lanes is shown while it runs, and a launch over it asks the same question 
- #298 [CLOSED] Offline achievements' cards: 'ready' not 'added' on a refresh, the reconnect cards batched, and the exit card naming the achie
- #299 [CLOSED] The offline achievements' top-up at the link's return shows a card with nothing to add: silent unless it brings games in or fa
- #300 [CLOSED] An offline game list update holds the interface on a stalled hash-library fetch until the link returns (found by #299's proof)
- #305 [CLOSED] At a reconnection: saves first, then one RetroAchievements batch, and the send card reported once (maintainer, 2026-09-27)
- #306 [CLOSED] The wake check reads a history file RetroArch 1.22 does not write; the top-up at the link's return never runs on the device
- #465 [CLOSED] M7.P3: Prove installed RetroAchievements reconnect cards
- #986 [OPEN] Backlog: the VM harness's uncalled tools and uncaught suites -- what is kept, why, and the one retirement proposed (T12 PL-19)
- #1154 [OPEN] Bug: EmulationStation's HTTP client never verifies the TLS peer, so the RetroAchievements password and web API key travel unver
- #1141 [OPEN] Backlog: vm-pair cannot start a 640x480 guest, and the transfer walks fail at 640x480
- #1142 [OPEN] Backlog: the launch's stop wait over a running sync card spins on the interface thread for up to 2 s (T18 PL-15)
- #1143 [OPEN] Backlog: dead code in the cloud pages after the retired folder move, and one reader for both surfaces (T18 PL-11, PL-12, PL-23,
- #1144 [OPEN] Backlog: run T18's why-table generator in vm-qa, and the ES unit and app-unit tests as a suite (T18 PL-16)

## The context read at stage A

- **The brief** at `14852bd6ed` whole, and the dispatch comment on #667 (17:09 UTC).
- **T19's `02` § What T20 inherits** at `d8c02be1c9` (`feature/m6-offline-achievements-666`, lines 257-307): landed, and consumed in `02` § The contract at stage B. Its points that bear on these pages:
  - the ctl's `>>> ` protocol table;
  - the why tokens against `scanWhy`/`topUpWhy`, with the three new ones (`STAMP_UNWRITABLE`, `RESULT_UNREADABLE`, and `TOOK_TOO_LONG` absent from `topUpWhy`);
  - `ready=unknown` in the stamp and in the page's `>>> done` line;
  - `disable`'s new exits 2 and 1;
  - `account`'s exit 2;
  - the staleness contract (PL-13);
  - the refresh helper (PL-17);
  - `NO_GAMES_FOUND` (PL-18);
  - the page comment's `have_account` wording;
  - 022's refusal shape, and its upgrade path (D-RA-051).
- **The two kickoff notes** (the dispatch, read as errata at stage A, at their lines at stage B):
  1. `CloudText::scanWhy` keeps a `NO_GAMES_FOUND` row (the ctl's `>>> why NO GAMES FOUND` on an empty library, which the brief's why table omits). T19's PL-18 says no producer emits it at `8ebaf8daad`. Stage B reads both ends.
  2. `Settings.cpp:420`'s `.hardcore` default sits inside `#if WIN32` (`:417-433`) and serves `SystemConf`'s forward to `Settings` when its path is empty (`SystemConf.cpp:288` and siblings; the path from `Paths::getSystemConfFilePath()`). So it is a live second store only if that path can be empty on ROCKNIX, which is T21's Q4. `SystemConf`'s own defaults table carries the same key (`:46`).
- **Rules:** `es-native-ui.md`, `es-player-text.md`, `es-ui-style-guide.md` and `es-code-traps.md` are loaded this session. The brief's ranges in `generic-x64-vm-testing.md` are read before the window is asked for, at the end of stage B.
