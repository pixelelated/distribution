# Research notes — M6.P2 T32, EmulationStation's game list views, scrapers and services (#679)

## Scope

The brief's § 2 block (`stage-a/membership.sh`), run from this worktree at `603b358a14` (stacked on the P1 branch at `2174265e9c`, the coordinator's `42cb00860c` merged at `121d0180f0`), with `W` the ES worktree at the pin:

```text
selects 1 paths 42 lines 17311 {'shipped': 42} {'upstream-carried': 36, 'fork-own': 6}
{'c++': 20, 'c-header': 22}
fork-own lines by inventory tier: 4005
42 .qa-scratch/t32/paths.txt
wc -l lines 17306
grep -c lines 17311
42
42
6 files 168 added 46 removed
6 files 168 added 46 removed
```

- **The two line counts** differ by 5, the five files without a trailing newline (§ 5's lines run). The inventory and the order count with `grep -c`.
- **The read's tiers.** The inventory's six `fork-own` files are all `fork-modified` by the read: none was added by the fork (0 fork-added against `bccd715707`). They are `Scraper.cpp`, `ThreadedScraper.cpp`, `ThreadedScraper.h`, `DetailedContainer.cpp`, `GridGameListView.cpp` and `ISimpleGameListView.cpp`. The 36 others are byte-identical to `rocknix/master` (the three directories' tree hashes are equal at `cada856d86` and `rocknix/master`).
- **The bases.** `cada856d86` is the merge base with `rocknix/master` (`f6c542872e`); `bccd715707`, its parent, is the base the inventory, `es-untranslated` and the per-file commit counts use. No upstream commit touches the slice since the merge base, so the merge debt is one line.
- **Excluded:** `views/ViewController.*` (T2's, #649) and `scrapers/ScreenScraper.*` (T21's, #668); every page under `guis/` is T31's. T21's `3ae9610b0` has changed `Scraper.cpp` and `Scraper.h` and added `ScraperReplies.{h,cpp}`: read there, recorded as inherited, never merged here.
- **The § 5 runs**, all as the brief expects but `atol(` (2 in 2 files, not 1: `DetailedContainer.cpp:1049` beside `GameNameFormatter.cpp:171`; `00` § Stage A).

## History

The fork's commits to the six files from `bccd715707` to the pin, no merges (`stage-a/history.out`): ten, and the merge `370ebe416` (2026-09-25, `rocknix/master` into `test/qa-integration`). They group by work (the files each commit touched in the slice, `git show --name-only`):

- **The scrape page and its run** (`acd7a6fee`, #241, D-UI-078; `ThreadedScraper.cpp`, `ThreadedScraper.h`): the `Progress` contract `GuiScraperRun` reads, and no background scrape.
- **The SCREENSHOTS list's aspect and turn** (#243, #245, D-UI-080/081): `3b7265f33`, `9f46264a8` and `05dc0a829` (`DetailedContainer.cpp`); `4e4ab0647` (`DetailedContainer.cpp`, `ISimpleGameListView.cpp`); `12de21757` (`DetailedContainer.cpp`, `GridGameListView.cpp`, `ISimpleGameListView.cpp`).
- **The help bar** (`7dc8bf373`, #210, D-UI-034; `ISimpleGameListView.cpp`).
- **The achievements hash the list passes** (`986f1749c`; `ISimpleGameListView.cpp`).
- **The developer pair at runtime** (`c0f6fb58f`, #64, `SCREENSCRAPER_RUNTIME_DEV_LOGIN`; `Scraper.cpp`), and **a credential's value kept out of the log** (`80f52e500`; `Scraper.cpp`).

## Callers

`stage-a/callers.out`: 47 include lines of the slice's 22 headers, from 23 files outside the 42 (es-app and es-core, at the pin). `UIModeController.h` 10, `IGameListView.h` 9, `ThreadedScraper.h` 9, `Scraper.h` 8, `SystemView.h` 3, `ISimpleGameListView.h` 2, and one each for the five view styles' headers, `GameNameFormatter.h` and `HttpServerThread.h`. The figure is the one § 5's stage-C include script is expected to print; that script, with its es-core edges, is stage C's.

## Context

Read this session, at the section § 3 names (`working-principles.md` § Pre-flight):

- **The rules.** `es-code-traps.md`, `es-native-ui.md`, `es-player-text.md`, `es-ui-style-guide.md`, `engineering-practices.md`, `bugs-are-agent-first.md`, `issue-tracking.md`, `device-builds.md` (§ Build credentials), `player-language.md`, `least-surprise.md` and `time-to-play.md` were loaded whole at the session's start and read at the sections § 3's table names. `generic-x64-vm-testing.md` is read at stage B, with the window's plan.
- **The register.** Every row § 3 names exists on this branch, D-UI-129 included (`grep -c "| <id> |"`: 1 each for D-QA-003, D-QA-005, D-WORKFLOW-166, D-CLOUD-038, D-UI-034, D-UI-078, D-UI-079, D-UI-080, D-UI-081, D-UI-113, D-QA-057, D-NET-017 and D-QA-050). `tools/archaeology 'scraper'` and `'carousel'` print 133 and 113 lines; they are read before anything is called pending, at stage B.
- **T21's routed items** (`origin/feature/m6-es-state-and-bridge-668`, `05`): PL-04 (a download removes its target before a byte arrives), PL-17 (the scraper's readers accept an empty or failed answer), PL-20 (`writeAllText` in place), PL-25 (#1154's peer verification); their lines are taken up in `02` § The leads.
- **The tests at the pin.** `es-app/tests/unit/README.md`: the pure-code rule ("functions that read nothing, ask nothing and draw nothing"); `CMakeLists.txt`'s targets are the build script's input at stage C. No test at the pin names a slice class (the sweep).
- **Read at stage B, said so:** the menu map's sections (§ 3 item 3), the blindspots (item 4), the walks and frames (item 6), the other audits' cited lines (item 8), the issues' states (item 9) and `docs/vm-qa-log.md:9-18` (item 10).
