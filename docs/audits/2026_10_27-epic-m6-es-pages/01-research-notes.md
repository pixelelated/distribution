# Research notes — M6.P2 T31, EmulationStation's other pages (#678)

## Scope

The brief's § 2 block (`stage-a/membership.sh`), run from this worktree at `da7922a7bd` (stacked on the P1 branch at `2174265e9c`, the coordinator's `266a14163e` merged at `3d591f7e30`), with `W` the ES worktree at the pin. Its figures, from the output (`stage-a/membership.txt`, which also lists all 76 rows with their lines, language and tier):

```text
selects 1 paths 76 lines 15537 {'shipped': 76} {'upstream-carried': 64, 'fork-own': 12}
{'c++': 37, 'c-header': 39}
fork-own lines by inventory tier: 4230
76 .qa-scratch/t31/paths.txt
wc -l lines 15526
grep -c lines 15537
73
12 files 1207 added 129 removed
```

- **The two line counts** differ by 11, the eleven files without a trailing newline (§ 5's lines run). The inventory and the order count with `grep -c`.
- **The three read tiers.** The inventory has two (12 `fork-own`, 64 `upstream-carried`); the brief splits the twelve into three files the fork added (`GuiScraperRun.cpp`, `GuiScraperRun.h`, `WifiScanProcess.h`; absent at the merge base, hence 73) and nine it modified. The 64 are byte-identical to `rocknix/master`: no slice file is among upstream's 14 commits past the base (`stage-a/runs.txt` § upstream's delta: 0 slice rows).
- **The bases.** `cada856d86` is the merge base with `rocknix/master` (`f6c542872e`). `bccd715707`, its parent, is the base the inventory, `es-untranslated` and the brief's per-file commit counts use. `upstream/master` in the ES repository is stale and is not read. The French counts at both bases: 706 against `bccd715707`, 703 against `cada856d86`, 0 without at either.
- **The § 5 runs**, all as the brief expects except one malformed grep (`00` § Stage A; `stage-a/runs.txt`, `stage-a/reruns.txt`). The title shapes are stage B's.

## History

The fork's commits to the twelve files from `cada856d86` to the pin, no merges (`stage-a/history.txt`): 58 lines across the twelve files. They group by work:

- **`GuiSaveState.cpp`** has 25 of them, 2026-09-08 to 2026-09-28: the same 25 from either base, since the one commit between them (`cada856d8`, upstream's Wi-Fi profiles) does not touch it (`git log --no-merges --format=%h <base>..<pin> -- GuiSaveState.cpp | wc -l`, 25 and 25). They cover:
  - the retired record (`00df7eca6`, #21) and the gate on the transfer lock (`62888f967`, D-CLOUD-053; `6e58988f8`, `9b89369dc`);
  - the label fit and the help bar (#27, #93, #149: `2088eadb9`, `c7838165b`, `d8e95118c`, `7c935a39d`, `772d70035`);
  - the worker deletion (`a11cde632`, #205, D-UI-073) and the rebuild only on disagreement (`ee4786940`, #207, D-UI-074);
  - the aspect and the turn (#243, #245, #250: D-UI-080/081);
  - the dates (#195: D-UI-087/089).
- **`GuiScraperRun.{cpp,h}`** were added by `acd7a6fee` (#241, D-UI-078: the scrape page sat in, with CANCEL). The later commits are the note's fit (`46111b1e3`), the comments audit (`217872e32`) and the player's own buttons (`4a87044e7`).
- **`GuiScraperStart.cpp`:** the developer pair on the device (`c0f6fb58f`, `ee53ecd65`), the remembered filters (`3e7195eb9`), the page (`acd7a6fee`), and two comments back to ASCII (`6ae936577`).
- **`GuiBios.{cpp,h}`:** the empty list explained, the tabs named, one ordered list (2026-09-04/05), and the paths as the system expects them (`72ef97b54`).
- **`GuiSettings.{cpp,h}`:** the network calls off the interface thread (`75e97ab0f`, #103) and the WI-FI rows (`6915d80f7`, `daafb69f1`, `404d3a9a3`).
- **`WifiScanProcess.h`** was added by `a6dbc33bb` (2026-10-13, the stable picker) and cancelled at exit by `16dbac521`, which is the pin itself.
- **`GuiGameOptions.cpp`** (`986f1749c`, the achievements page) and **`GuiImageViewer.cpp`** (`12de21757`, the turn) have one commit each.

## Callers

Who constructs each of the 39 classes, or calls a static of it, outside its own two files (`tools/t31-callers.py`; `stage-a/callers.txt`; a short paths file is its constructed negative, and it exits 1):

- **From `GuiMenu.cpp` (T26's):** 18 classes, among them `GuiScraperStart` (`:542`), `GuiBios` (`:6196`), `GuiNetPlaySettings` (`:3524`), `GuiMoonlight` (`:5758`), `GuiKeyMappingEditor` (`:11654`), `GuiUpdate` (`:1570`) and the three store pages (`:1485`, `:1497`, `:1509`).
- **From the game lists:** `GuiGameOptions` (`ISimpleGameListView.cpp:358`); `GuiGamelistOptions` (`GridGameListView.cpp:119`, `ISimpleGameListView.cpp:347`); `GuiSaveState` (`GuiGameOptions.cpp:152`, `ISimpleGameListView.cpp:380`, `:421`); `GuiNetPlay` (`SystemView.cpp:367`).
- **From each other:**
  - `GuiScraperRun` from `GuiScraperStart.cpp:491`;
  - `GuiBluetoothDevices` and `GuiBluetoothPair` from `GuiControllersSettings.cpp:188`/`:184`;
  - `GuiKeyboardLayout` from `GuiKeyMappingEditor.cpp` (4 lines);
  - `GuiHashStart` from `GuiNetPlaySettings.cpp:49` and `GuiRetroAchievementsSettings.cpp:721` (T20's lead: the hasher on the interface thread);
  - `GuiMetaDataEd` from `GuiGameOptions.cpp:572` and `GuiGamelistOptions.cpp:500`.
- **`WifiScanProcess`** from `GuiWifi.cpp` alone (3 lines; GuiWifi is T18's).
- **The base classes:** `GuiSettings` (84 lines in 16 files) and `GuiLoading` (41 lines in 18 files) are built everywhere.
- **No caller: `GuiAutoScrape`.** At the pin nothing includes `GuiAutoScrape.h` or constructs the class; its last commits are upstream's (`77cb954fa`, `d8229b6f4`, `97fb8b6da`). A Q7 lead for stage B: dead upstream code, read for whether it is built at all.

## Context

Read in this session at stage A, in the brief's § 3 order:

1. **The rules.** The four ES rules, `engineering-practices.md`, `bugs-are-agent-first.md`, `player-language.md` and `least-surprise.md` were loaded at session start. The worktree's differences from `next` are the coordinator's nine files, the same T26 read (`00`). The sections at the brief's line numbers are read as stage B reaches each page.
2. **The register.** All 24 rows the brief names in bold or plainly were read, and each is present:
   - D-UI-021, D-UI-022, D-UI-023, D-UI-028, D-UI-030, D-UI-034, D-UI-035;
   - D-UI-069, D-UI-073, D-UI-074, D-UI-078, D-UI-079, D-UI-080, D-UI-081, D-UI-087, D-UI-089;
   - D-CLOUD-053, D-UI-118, D-RA-009, D-RA-011, D-NET-009, D-WORKFLOW-166, D-WORKFLOW-195;
   - the open D-WORKFLOW-080.

   `tools/archaeology 'save state manager'` and `'scrape'` run at stage B, before anything is called pending.
3. **The menu map** (989 lines, as the brief says): its headings; `## Save state manager` at `:150`; D-UI-039's paragraph at `:666-668`; `## Not mapped` at `:677` with the rule at `:683`.
4. **The blindspots** 4, 8, 13, 44, 45, 49, 62 and 75, by their headings.
5. **The tests.** The § 5 sweep: three classes with harnesses at the pin. The pattern harnesses are read whole before a case is written in their shape (stage E).
6. **The audits.** T2's punch list at the routed lines: PL-005's sibling at `GuiGamelistOptions.cpp:148` (`:109`); PL-016's callers in `GuiSaveState` (`:295`, and the resolution row, *"The manager's message to the player is `GuiSaveState`'s, a lead for #678; #782 stays open"*); the relay session and the spectator mode (`:614`); PL-031 deferred to #678, the nickname default moving to where `GuiNetPlaySettings` and `GuiGameOptions` load. Also T26's `02` § What T31 to T37 inherit, and T26's retro. T21's and T20's sections are read at stage B with the pages they bear on.
7. **The issues.** The 37 the brief names, by title and state at 12:1x UTC:
   - **Closed (11):** #149, #205, #241, #243, #245, #250, #307, #308, #540, #566, #577.
   - **Open (26):** #18, #36, #37, #63, #65, #196, #222, #301, #768, #776, #782, #791, #951, #965, #1137, #1141, #1170, #1182, #1185, #1188, #1190, #1191, #1192, #1193, #1202, #1212.

   #678's own body: 21 checkboxes.
