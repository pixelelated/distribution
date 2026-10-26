# Research notes — M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

## Scope

The brief's § 2 block, run from this worktree at `4844a773ca` (stacked on the P1 branch at `2174265e9c`), with `W` the ES worktree at the pin. Its output, verbatim (`stage-a/membership.txt`):

```text
selects 1 paths 14 lines 9249 {'shipped': 14} {'fork-own': 14}
{'c++': 7, 'c-header': 7}
3519 c++ fork-own es-app/src/ApiSystem.cpp
490 c-header fork-own es-app/src/ApiSystem.h
607 c++ fork-own es-app/src/guis/GuiWifi.cpp
93 c-header fork-own es-app/src/guis/GuiWifi.h
1092 c++ fork-own es-app/src/scrapers/ScreenScraper.cpp
104 c-header fork-own es-app/src/scrapers/ScreenScraper.h
644 c++ fork-own es-core/src/HttpReq.cpp
180 c-header fork-own es-core/src/HttpReq.h
723 c++ fork-own es-core/src/Settings.cpp
165 c-header fork-own es-core/src/Settings.h
494 c++ fork-own es-core/src/SystemConf.cpp
94 c-header fork-own es-core/src/SystemConf.h
829 c++ fork-own es-core/src/utils/AtomicFileUtil.cpp
215 c-header fork-own es-core/src/utils/AtomicFileUtil.h
14 .qa-scratch/t21/paths.txt
wc -l lines 9249
12
-- the 14 at the pin against the worktree (expect empty)
```

Every figure is the brief's: 14 paths and 9,249 lines, all shipped and fork-own; 7 C++ and 7 headers; 12 in the merge base `bccd715707` (`AtomicFileUtil.cpp` and `.h` are new); no difference between the worktree and the pin on the 14.

**The 14, with each file's history since the merge base** (`git -C W diff --numstat bccd715707 <pin>`, `git rev-list --count bccd715707..<pin>`, the last commit at the pin; `stage-a/history-callers.txt`). Every pair of insertions and deletions sums to the brief's: `ApiSystem.*` 251/34, `HttpReq.*` 25/0, `GuiWifi.*` 628/76, `ScreenScraper.*` 126/8, `Settings.*` 104/9, `SystemConf.*` 332/54, `AtomicFileUtil.*` 829/0 and 215/0.

| File | Lines at the pin | In the merge base | Insertions/deletions since it | Commits since it | Last commit |
| --- | ---: | --- | --- | ---: | --- |
| `es-app/src/ApiSystem.cpp` | 3519 | yes | 214/33 | 19 | f7b71db0a 2026-10-13 cloud: return freed renderer heap before sign-in wait |
| `es-app/src/ApiSystem.h` | 490 | yes | 37/1 | 11 | c8dc72cf9 2026-10-11 emulationstation: manage cloud connections and network recovery |
| `es-app/src/guis/GuiWifi.cpp` | 607 | yes | 552/62 | 14 | 16dbac521 2026-10-15 GuiWifi: cancel scan worker on normal frontend exit |
| `es-app/src/guis/GuiWifi.h` | 93 | yes | 76/14 | 9 | 16dbac521 2026-10-15 GuiWifi: cancel scan worker on normal frontend exit |
| `es-app/src/scrapers/ScreenScraper.cpp` | 1092 | yes | 120/7 | 8 | 3178b832b 2026-10-14 ScreenScraper: match rejected access guidance to credential source |
| `es-app/src/scrapers/ScreenScraper.h` | 104 | yes | 6/1 | 1 | c0f6fb58f 2026-09-05 scrapers: ScreenScraper developer pair entered on the device (SCREENS |
| `es-core/src/HttpReq.cpp` | 644 | yes | 9/0 | 2 | 9202ebed5 2026-09-27 hasher: the library fetch ends when it stalls; an offline index says  |
| `es-core/src/HttpReq.h` | 180 | yes | 16/0 | 2 | 9202ebed5 2026-09-27 hasher: the library fetch ends when it stalls; an offline index says  |
| `es-core/src/Settings.cpp` | 723 | yes | 97/9 | 7 | d242000a5 2026-10-13 GuiMenu: explain offline preparation before updating game lists |
| `es-core/src/Settings.h` | 165 | yes | 7/0 | 1 | b0e417df3 2026-09-10 Settings, SystemConf: write through a temporary and keep the last kno |
| `es-core/src/SystemConf.cpp` | 494 | yes | 275/52 | 15 | 39f888354 2026-10-03 settings: revalidate last-good records under the lock (#320) |
| `es-core/src/SystemConf.h` | 94 | yes | 57/2 | 8 | 812bc2f75 2026-09-29 SystemConf: a damaged reading keeps the pending changes |
| `es-core/src/utils/AtomicFileUtil.cpp` | 829 | no | 829/0 | 16 | ee6147aec 2026-09-28 AtomicFileUtil: a recovery is written back under the settings lock |
| `es-core/src/utils/AtomicFileUtil.h` | 215 | no | 215/0 | 15 | ee6147aec 2026-09-28 AtomicFileUtil: a recovery is written back under the settings lock |

## The runs at stage A

The brief's § 5 block verbatim (`stage-a/runs.sh`, the dispatch tip `4844a773ca` for its placeholder), its output in `stage-a/runs.txt` and its trace in `runs.trace`; rc 0, under one second. Each run with its exit, figure and *a FAIL would mean ...* is `02` § The runs at stage B. The figures, and the two deltas from the brief's comments (`00` § Stage A has them in full):

- **`wifictl`'s key lines:** the brief's pattern prints 177 and 460 of the four lines that carry the key; 195 and 209 (`802-11-wireless-security.psk "${PSK}"`) are real, and outside the pattern.
- **`writeAllText(`:** 27 lines, 25 call sites (sixteen sysfs in `ApiSystem.cpp`); the other two are the definition and the declaration.
- **The host `g++`:** `AtomicFileUtil.cpp` passes; the other six sources are CANNOT on `SDL_timer.h`, `SDL_joystick.h`, `pugixml.hpp` or `curl/curl.h` (`stage-a/runs-followup.txt`).
- **The unit tests at the pin:** 221 cases in four binaries, all passing; the eight named files 80 (`stage-a/unit-pin.txt`).
- **`tests/wifi-profile-lifetime.py`:** PASS (`stage-a/wifi-profile-lifetime.txt`).

## The callers of the 14's entry points (at the pin)

`git -C W grep -E <pattern> <pin> -- es-app/src es-core/src`, lines and files:

```text
-- callers at the pin (git grep -c, files and lines)
ApiSystem::getInstance\(\)->: 293 lines in 41 files
Settings::getInstance\(\)->: 882 lines in 77 files
SystemConf::getInstance\(\)->: 635 lines in 38 files
HttpReq\b: 167 lines in 27 files
AtomicFile::: 41 lines in 6 files
ScreenScraper: 65 lines in 9 files
GuiWifi: 32 lines in 4 files
```

## The issues the brief names

Read on GitHub at stage A, by title, state and closing date; the bodies are read at stage B where a question needs them. #536's title shows that the brief's caution was right: `tools/cloud-input-test` is #535's, and #536 is the phone browser's links.

| Issue | State | Closed | Title (as read) |
| --- | --- | --- | --- |
| #102 | closed, completed | 2026-09-17 | RG SP froze during the startup sync on its first d574edf975 boot; settings lost on the forced power-off; Wi-Fi absent on the next boot |
| #320 | closed, completed | 2026-10-04 | SystemConf -- the recovery record can be published from an older good state outside the settings lock (audit #319) |
| #421 | closed, completed | 2026-10-04 | Preserve private settings permissions in shell writers |
| #535 | closed, completed | 2026-10-11 | Skip the Wi-Fi password prompt for open networks |
| #536 | closed, completed | 2026-10-11 | Investigate phone-controlled browser links that will not click |
| #64 | open | | ES: ScreenScraper developer credentials entered on the device, not compiled in (fork build flag) |
| #566 | closed, completed | 2026-10-14 | Provision ScreenScraper credentials for pixelelated releases |
| #586 | open | | Backlog: Replace interim ScreenScraper developer credentials |
| #299 | closed, completed | 2026-09-27 | The offline achievements' top-up at the link's return shows a card with nothing to add |
| #300 | closed, completed | 2026-09-27 | An offline game list update holds the interface on a stalled hash-library fetch until the link returns |
| #1154 | open | | Bug: EmulationStation's HTTP client never verifies the TLS peer |
| #1143 | open | | Backlog: dead code in the cloud pages after the retired folder move, and one reader for both surfaces |
| #176 | closed, completed | 2026-09-15 | exec.log carries the RetroAchievements password in the clear |
| #1137 | open | | Backlog: M6 holds no GENERIC_X64 build root with a toolchain |
| #1138 | open | | Backlog: a brief's grep figures differ between ugrep and GNU grep |
| #1141 | open | | Backlog: vm-pair cannot start a 640x480 guest |

## The context read at stage A

- **Read whole:** the brief at `2f1d006461` and the dispatch comment on #668 with its errata and the 20:50 correction.
- **Read at their lines:** the register rows D-SYS-001 to 014, D-NET-001 to 016 (no D-NET-011 row), D-CLOUD-078, D-CLOUD-079 (its sentence that EmulationStation's writers "take the settings lock around the read-modify-write" is Q4's: `SystemConf` takes it, `Settings` does not) and D-WORKFLOW-166.
- **The lane's changed rules:** `device-builds.md`, `engineering-practices.md` and `es-code-traps.md`, against the copies this session loaded.
- **T20's inheritance** by `git show`: PL-08's reader fixture at distribution `ffb6b686cb`, and S2's `httpsRedirectsOnly` at ES `5c0ddaaee`.
- **For stage B, not yet read:** the 14 whole at the pin; § 3's remaining rules (`generic-x64-vm-testing.md`, `rclone-cloud-sync.md`, `handheld-evidence.md`), the menu map's lines, the blindspots, the audits it names (T1, T2, T12, T14, T15, T17, T18), the issues' bodies, and `Paths` for Q4.
