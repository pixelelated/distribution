# Research notes -- M6.P2 T33, EmulationStation's system layer (#680)

## Scope

The brief's § 2 block, run at stage A from this worktree (`stage-a/membership.sh`, `stage-a/membership.out`), printed the brief's expected lines byte for byte:

```
mine: 77 paths.txt: 77 equal: True
only-mine: []
only-paths.txt: []
lines: 16276 reach: {'shipped': 77} tier: {'fork-own': 31, 'upstream-carried': 46} lang: {'cmake': 1, 'other': 4, 'c-header': 41, 'c++': 31}
fork-own lines: 4522
read lines: 16210
```

- **The ES lines:** 75 text paths; `wc -l text 16272`; `grep -c text 16276`. Four files end without a newline: `EmulationStation.h.in`, `KeyboardMapping.cpp`, `LangParser.cpp` and `NetworkThread.cpp`.
- **The bases:** 50 of the 77 are present at the merge base `cada856d86` and 50 at `bccd715707`.
- **The fork's delta:** `31 files changed, 2689 insertions(+), 7 deletions(-)`, against `bccd715707`, `cada856d86` and `rocknix/master`. 27 files are added and 4 modified: `es-app/CMakeLists.txt` +44/-0, `NetworkThread.cpp` +105/-3, `NetworkThread.h` +29/-1, `Win32ApiSystem.cpp` +3/-3.
- **The read's tiers:** fork-added 27, fork-modified 4, upstream-carried 46. The last are identical to `rocknix/master`, with 0 upstream commits on the 77 since the merge base.
- **Inherited and read, not merged:**
  - T21's ES tip `3ae9610b0` carries `es-app/CMakeLists.txt` +10, `WifiText.cpp` +11 and `WifiText.h` +13;
  - T20's tip `5c0ddaaee` carries `OfflineAchievementsText.cpp` +99 and `.h` +52;
  - T26's, T31's, T2's and T18's tips carry nothing on the 77.
- **`CLAIMS`** (in `.qa-scratch/t33/block-2.txt`): `ApiSystem.*` are T21's by a non-rest glob, `FileData.*` and `SystemData.*` are T2's, and `CloudText.*` is T18's.

## History

`stage-a/history.out`: 72 fork commits on the 77 since `bccd715707`, 68 of them non-merge; the four merges are `da702d8b6`, `370ebe416`, `137309b7d` and `6c7a36d04`. They are read at stage B, grouped by the files each touched.

## Callers

`stage-a/callers.out`: 149 quoted `#include` lines of the slice's 41 headers, from 66 files outside the 77 (es-app/src and es-core/src, at the pin). The most included are `CollectionSystemManager.h` 17, `PlatformId.h` 11, `Gamelist.h` 10, `Genres.h` 9, `FileFilterIndex.h` 8, `ContentInstaller.h` 8, `EmulationStation.h` 7, `CloudExit.h` 7, `FileSorts.h` 7 and `DisplayAspect.h` 7. The include graph (stage C, `tools/t33-includes.py`) replaces these with the tool's own lines.

## Context

Read at stage A: the dispatch whole; the brief's § 1, § 2's block and its three hidden figures, and § 5's block with its expectations; the pointer. The rules were read at the session's start (`working-principles.md` § Pre-flight). The rest of § 3 (the rules at their sections, the register rows, the audits' cited lines, the issues' states, the blindspots and `docs/vm-qa-log.md`) is read at stage B, before `02`.
