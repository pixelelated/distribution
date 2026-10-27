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

### Read at stage C (items 4, 8, 9 and 10)

- **Item 9, the issues, re-read 16:43 UTC.** Every state is as § 3 gives it. #1205 (T21 PL-17), #1191, #1154, #1206, #1186, #1187, #1192, #1193, #965, #1190, #156, #774, #780, #789, #791, #180, #64, #585, #951, #1137, #1138, #1141, #1183, #1135 and #700 are OPEN. #300, #299, #246, #243, #245, #241, #210, #177, #66, #67, #566 and #274 are CLOSED. #649, #665, #667, #668, #673 and #678 are OPEN until the integration merge. T31's PL-21 bug, #1254 (G-06's cause), is OPEN.
- **Item 8, the audits.**
  - T21's PL-17 (`05:332-351`, #1205) owns the `Retry-After` HTTP-date read as 0 ms at "T32's caller lines". At the pin that is `Scraper.cpp:354-356`, the search's 429, which 3.13's harness drives with a number; the HTTP-date half stays #1205's, not re-proposed here.
  - T2's PL-008 (`05:157`, #774) is a raw pointer held across a reload; L-19's `POST /launch` posting a raw `FileData*` is its sibling from the services side.
  - T2's `02:352` read `HttpServerThread.cpp:615-630` as context only; L-19 is this slice's reading of those lines.
  - PL-023 (#789) and PL-033 are not in this slice's lines.
- **Item 10, time to play.** `docs/vm-qa-log.md:9-18`: three headline columns, and "No budget row exists yet". The slice's three points on the launch path, as the window measured them:
  - the list's `launchSelectedGame`: not timed. The window launched nothing; G-08's `POST /launch` went to the API.
  - the populate on SCREENSHOTS in grid style: 2.775 s press to a still screen, against 2.786 s in automatic and 2.777 s for gb in grid (`guest-cycle/g02-l14-timings.txt`). L-14's per-tile cost was not reached, because the shipped theme has no grid view.
  - the carousel after UPDATE GAMELISTS: framed (G-09), not timed.
- **Item 4, the blindspots,** at their numbers. 22 is 3.13 (an unreachable scraper read as "nothing found": G-05, and `l313`'s FAIL). 44 is not in this slice's lines (T31's `MultiLineMenuEntry`). 62 is the `Already written:` line on every proposed bug (in 05). 64's sibling is L-06 and L-18 (the scrapers' unbounded requests). 75 holds: every count was taken at the hash, by `git -C <W> show 16dbac5211:`. 4 (`close()` inside a handler) has no new site here; its #246 cousin is L-16's shape, carried to T33. 3, 8 and 13 have no site in the 42.
