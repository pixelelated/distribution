# Forward audit — M6.P2 T31, EmulationStation's other pages (#678)

Read at the pin `16dbac5211eea7e70db7394372033be2be7df829`, from the distribution worktree at `da7922a7bd` and later. Each figure below is a tool's line; this file is composed by `tools/t31-02.py` from `stage-b/02-template.md` and the generators' tables, and the composer asserts every count. Each lead was read at its lines before it was named. A lead is not yet a finding: `04` settles each one, with its proof.

## Coverage

One row per path (76). `Lines` is `grep -c ''`, the inventory's count. The read's tier: fork-own (3 files the fork added), fork-modified (9), upstream-carried (64, byte-identical to `cada856d86` and to `rocknix/master`). Every path is counted by every census in this file. A lead named in the last column was read at its lines.

{{COVERAGE}}

## The pages

`tools/t31-pages.py`: one row per `.cpp`. Each row gives the class and its base, what opens it, what it starts (the census; the thread and the bound of each start are in § Leads by site), its dialogs with where back lands, its title and the map's verdict.

{{PAGES}}

What each page runs, and on which thread, beyond the census:
- The process starts are all on the interface thread with no bound: `GuiMoonlight`'s 5 `executeScriptLegacy` and 3 `runSystemCommand`, the LED page's one per slider step (L-02), and `GuiControllersSettings`' 2. Moonlight's `popen ("moonlight -v")` at `:42` is the version probe of its client.
- The 18 `GuiLoading<` run their work on a worker and their completion on the interface thread, holding the page's raw `this` (#1212's shape, T21's grading), over L-22's race.
- The 18 `std::thread` mentions are `GuiLoading.h`'s 2, `GuiUpdate`'s 6 (the OS update, D-UI-079's named card), `GuiBluetoothPair`'s 2, `GuiNetPlay`'s 2, `GuiBackup`'s, `GuiInstall`'s and `GuiAutoScrape`'s (not built).

## The dialogs

`tools/t31-dialogs.py`: 50 sites, each read whole by balanced brackets. Where back lands is read from `GuiMsgBox.cpp:116-134` at the pin: the only button; else the first named OK or NO; else the last.

{{DIALOGS}}

- Every YES / NO box lands on NO: 17 sites. The fork's two (`GuiSaveState.cpp:449`, `GuiScraperRun.cpp:112`) and upstream's fifteen, `GuiScraperStart.cpp:449` and `:467` among them. The two THIS WILL DELETE boxes (`GuiGameOptions.cpp:253`, `GuiMetaDataEd.cpp:365`) land on NO; on the guest, B on DELETE GAME and on the manager's DELETE left the files (G07). proved: guest.
- WRITE / CANCEL (`GuiGameOptions.cpp:274`) lands on CANCEL. CLOSE (`:289`) is a single button.
- **Three landings press the choice that acts** (proved: tree):
  - `GuiControllersSettings.cpp:76` is OK / CANCEL: back presses **OK** and starts the controller mapping (L-19);
  - `GuiMetaDataEd.cpp:524` is YES / NO / CANCEL: back presses **NO**, which saves the edits without the copies (L-20);
  - the two SAVE CHANGES? boxes (`GuiMetaDataEd.cpp:629`, `GuiKeyMappingEditor.cpp:497`) land on **NO**, which discards the edits (L-21).
- **The words:**
  - FAILED (`GuiNetPlay.cpp:336`, with HttpReq's error text after it);
  - four sentence-case English boxes in `GuiMoonlight.cpp`, `Succesfully` misspelt;
  - the manager's `<busy>` and `<busyNow>` are its composed refusals;
  - one message per family across pages, identical at every site: ARE YOU SURE YOU WANT TO DELETE THIS ITEM? (4), THIS WILL DELETE THE ACTUAL GAME FILE(S)! (2), YOU ARE NOT CONNECTED TO A NETWORK (3), FINISHED (3; `GuiAutoScrape`'s is not built).

## The rows

`tools/t31-rows.py`: every value-binding builder call in the slice's `.cpp` files, with its store and the overload it hits.

{{ROWS}}

- **Switches:** all 23 are `storeInSettings = true` to ES-own keys in `es_settings.cfg`: 20 by the three-argument form, 3 with a description at `GuiNetPlaySettings.cpp:38-40`. None is the PROGRESS TRACKER shape.
- **Text rows:**
  - The scraper's six account rows go to `Settings`, the three secrets with `password = true`.
  - The netplay and Moonlight rows go to SystemConf. **PLAYER PASSWORD (`GuiGameOptions.cpp:204`) is `password = false`** (L-04).
  - `updateVal` (`GuiSettings.cpp:218-238`) writes to the store when the editor's OK is pressed, empty or not (#1185, cited). No row here guards an untouched editor; the account rows' mode is #1193's (cited).
- **Two-line rows:** the 8 `addWithDescription` calls. The `grep`'s 10 lines include two commented out (`GuiFavoriteMusicSelector.cpp:45-46`).
- **Reboot flags:** none set or named in the slice.
- **The metadata editor's popups** (`GuiMetaDataEd.cpp:333-341`) are upstream's own rows and bind no store; it saves through its own `save()`.

## The reads

`tools/t31-reads.py`: one row per site, 26. These are the brief's 12 + 1 + 9, and the 4 `atof` its runs did not count. The writer, and what a failure reads as, were read at each line.

{{READS}}

The BIOS page's empty vector is not a read site but belongs with them. `GuiBios.cpp:183-187` over `ApiSystem.cpp:886`: `executeEnumerationScript` returns lines only, so a failed `rocknix-systems` and a check that knows nothing are one screen, THE BIOS CHECK RETURNED NOTHING (L-12, proved: guest).

## The titles

`tools/t31-titles.py`, which loads the checker's own three patterns and its `names_screen`: one row per `.cpp`.

{{TITLES}}

**The twelve in neither place, each with a disposition for the pause** (BIOS CHECK and SCRAPING GAMES first, and neither deferred):

| Title | Page | Disposition proposed |
| --- | --- | --- |
| BIOS CHECK | `GuiBios` (fork-modified) | **map it**: a section beside the save state manager's, its one list and DETAILS (D-UI-039; the fork wrote the page) |
| SCRAPING GAMES | `GuiScraperRun` (fork-own) | **map it**: under SCRAPER, the fourth-tier page with CANCEL (D-UI-078) |
| BACKUP USER DATA | `GuiBackupStart` | declare: hidden on ROCKNIX (no `ApiSystem::BACKUP` backend; `es-native-ui.md` § Reusable precedents) |
| CONTENT DOWNLOADER | `GuiBatoceraStore` | declare: upstream store page, unchanged here |
| THE BEZEL PROJECT | `GuiBezelInstaller` | declare: upstream installer behind DECORATIONS, which is declared |
| DEVICE OPTIONS | `GuiBluetoothDeviceOptions` | declare: upstream Bluetooth page, unchanged here |
| BLUETOOTH DEVICE LIST | `GuiBluetoothDevices` | declare: upstream, unchanged here |
| FILTER GAMELIST BY / EDIT DYNAMIC COLLECTION FILTERS / FIND GAMES | `GuiGamelistFilter` | declare: upstream game-list filter pages |
| INSTALL ON A NEW DISK | `GuiInstallStart` | declare: upstream installer, not a handheld flow |
| the key mapping editor's | `GuiKeyMappingEditor` | declare: upstream pad-to-keyboard editor (one of #63's four strips) |
| EDIT METADATA | `GuiMetaDataEd` | declare: upstream metadata editor, unchanged here |
| THEMES DOWNLOADER | `GuiThemeInstaller` | declare: upstream, one of #63's four strips |

A thirteenth page has no `_()` title at all: **MOONLIGHT GAME STREAMING** (`GuiMoonlight`, a raw literal). The map never names it, and the checker cannot see it (L-07): map or declare it, at the pause. **The four tab-strip pages** (#63, recorded and not moved): `GuiThemeInstaller`, `GuiBatoceraStore`, `GuiKeyMappingEditor` and `GuiKeyboardtopads` route left and right to their strips themselves.

## The merge debt

- **The bases:** `cada856d86` is the merge base with `rocknix/master` (`f6c542872e`). `bccd715707` is its parent and the base the earlier briefs used (`rev-list --count` 1). `upstream/master` in the ES repository is a stale copy and was not read.
- **Upstream's side:** 14 commits past the base, 8 of them touching `guis/`, **0 touching a slice file** (GuiMenu's 152/2 and 1/0 are T26's). The 64 upstream files are at `rocknix/master`'s bytes today.
- **The fork's 12 files**, `git diff --numstat cada856d86 <pin>` (added, removed):

{{NUMSTAT}}

- **What T32 to T37 read:** the provenance 3 / 9 / 64. D-WORKFLOW-080's shape: the fork's pages here are already one file each, the shape GuiMenu's option (a) would reach.

## Leads

The questions are Q1 to Q7 as brief § 4 sets them, the family is from the brief's list, and `proved:` is how the lead was shown. "Upstream" means a contained fix under `bugs-are-agent-first.md` rule 6 with a #585 line; severity is settled in `04`.

| Lead | Q | Lines | What the read shows | Family | Side | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| **L-01** | Q2 | `GuiSettings.cpp:106-112`, `:133-139`; `GuiScraperStart.cpp:542-548`; `GuiMetaDataEd.cpp:620-624` | START, offered as CLOSE on every settings page, deletes every page with `delete window->peekGui()`. No `close()`, `save()` or `onFinalize` runs, so every open page's unsaved choices are dropped, the fork's cloud pages included. Identical in `batocera/master` (`b2ceb55a7`) and `rocknix/master` | a state write that can lose the record | upstream, reaching the fork's lanes | fixture (`stage-c/l01-start-drops.py`: FAIL at the pin, control PASS); guest (G02: START left `es_settings.cfg` untouched, the B control wrote `ShowCheevosIcon=false`) |
| **L-02** | Q2, Q3 | `GuiAnalogSticksLedControls.cpp:62-87` | Each slider step runs `/usr/bin/analog_sticks_ledcontrol` on the interface thread and sets `analogsticks.led` in memory. The page has no save function, so `GuiSettings::save` returns at `:88-89`, and nothing saves `system.cfg` at exit. The quirks' `ledcontrol` reads the key at boot, **so the colour is lost at a restart** | a state write that can lose the record | upstream (ROCKNIX's own page) | fixture (`stage-c/l02-led-not-saved.py`: FAIL, control PASS); the guest shows the row only with `DEVICE_ANALOG_STICKS_LED_CONTROL=true` (`GuiMenu.cpp:2197`) |
| **L-03** | Q2 | `GuiNetPlaySettings.cpp:155-187` | Changing USE RELAY SERVER runs `delete this` without `save()` and opens a new page, **so ENABLE NETPLAY, toggled before, is dropped**. The delete runs inside the option list's own callback; nothing is touched after it (`OptionListComponent.h:310`, `:323`) | a state write that can lose the record | upstream | guest (G08: switched on, relay moved, BACK: `global.netplay=0`, `global.netplay.relay=nyc`) |
| **L-04** | Q2 | `GuiGameOptions.cpp:204` | PLAYER PASSWORD is `password = false`: the netplay password is shown on the row and in the editor. batocera's is the same | a credential's sink | upstream | tree |
| **L-05** | Q6 | `GuiMoonlight.cpp:282`, `:304`, `:306` | The SERVER IP the player typed goes unquoted into `popen` (`executeScriptLegacy`, `ApiSystem.cpp:2269`). The pairing callback writes a host parsed from moonlight's output back to `moonlight.host` (`:310-311`) | a command built from a player's string | upstream (ROCKNIX's own page) | fixture (`stage-c/l05-l06-moonlight.py`: the canary made by all three commands; control PASS) |
| **L-06** | Q4 | `GuiMoonlight.cpp:330-333` | `rm -r "~/.cache/Moonlight Game Streaming Project"`: a tilde inside double quotes is not expanded, so nothing is removed, and the box says "Unpaired and settings cleared" | a check whose failure reads as success | upstream (ROCKNIX's own) | fixture (both `rm` rc 1, the directories left; control PASS); guest (G09) |
| **L-07** | Q5, Q7 | `GuiMoonlight.cpp:268`, `:295-336` | The page title is a raw English literal, with no `_()`, no French and invisible to the checker. Four boxes are in sentence case, one misspelt. The page is neither mapped nor declared; GAME SETTINGS opens it unconditionally (`GuiMenu.cpp:5758`). The pairing PIN is new at each opening | a player sentence outside the vocabulary; a page the map does not describe and the checker cannot see | upstream (ROCKNIX's own) | guest (G12: the rows French, the title English; PIN 4269, then 4282) |
| **L-08** | Q5 | `GuiScraperRun.cpp:132-145` | `SKIPPED - YOU CANCELLED IT`, a fourth SKIPPED reason. The comment argues it; no register row | a player sentence outside the vocabulary | fork | design -- **for the pause** (a decision; an ID the coordinator assigns) |
| **L-09** | Q4 | `GuiScraperRun.cpp:142`, `:225`, `:231` | A run where every game errored and the scraper did not fail reads COULDN'T FINISH and the counts. There is no why (line 4 needs `p.failed`) and no next step (line 5 needs `done - errors > 0`) | a check whose failure reads as success (half) | fork | fixture (`stage-c/l09-l10-scrape-page.py`: lines 4 and 5 empty; control PASS); the guest's offline run never reaches the page (G04) |
| **L-10** | Q1, Q4 | `GuiScraperRun.cpp:90-103` | Once finished, any non-zero input dismisses the outcome, an axis past its deadzone included | (page) | fork | fixture (an axis dismissed it; control PASS) |
| **L-11** | Q5 | `GuiBios.cpp:220-230` | The row summary is built word by word, so the French reads `7 SUR 7 MANQUANT` | a player sentence outside the vocabulary | fork | guest (G12) |
| **L-12** | Q4 | `GuiBios.cpp:183-187`, `ApiSystem.cpp:886` | A failing or absent `rocknix-systems` gives the same screen as a check that knows nothing, with no recovery line | a check whose failure reads as success | fork | guest (G05: the script shadowed by one that exits 1) |
| **L-13** | Q3, Q4 | `GuiSaveState.cpp:507-529` | COPY TO FREE SLOT runs `copyToSlot` on the interface thread. No free slot is silent. A failed copy is silent, and so is a successful one: `loadGrid` puts the cursor back on START NEW GAME, the new tile off-screen. At the pin `copyToSlot` returns `true` over an unchecked `copyFile` (SS-4, T2's `f11e7528a` not in the pin) | a check whose failure reads as success; work on the interface thread | fork | guest (G06: read-only directory, no message, no tile; a 64 MB copy leaves the identical frame) |
| **L-14** | Q4 | `GuiSaveState.cpp:26-36`, `AtomicFileUtil.cpp:440-442` | Any open failure but ENOENT is read as "a sync is running". It fails closed, with the wrong words. ES runs as root on the image (G01 `id -u` 0), so EACCES is hard to reach: a keep-an-eye candidate | (page) | fork | tree |
| **L-15** | Q2 | `GuiScraperStart.cpp:166-210` | An empty selection saved from the main menu reads back as "nothing remembered", so every system is selected: "none" cannot be kept. The first tab switch or close from the main menu stores the default set, so a system added later is not selected | a row whose store is wrong | fork | guest (G03: `ScraperSystems="pico-8"` written at the first SCRAPE → OPTIONS) |
| **L-16** | Q2, Q3 | `GuiScraperStart.cpp:34-37`, `GuiSettings.cpp:83-96`, `Settings.cpp:471` | `save()` on every tab switch. `Settings` counts a value equal to its default as a change and `saveMap` omits it, so a first visit rewrote `es_settings.cfg` twice with nothing chosen: the second write changed no content | a state write with nothing to write | fork, upstream | guest (G03: two mtimes moved; the second with no key changed) |
| **L-17** | Q3 | `GuiScraperStart.cpp:475-494`, `:97-100` | `getSearches` runs on `GuiLoading`'s worker reading `mSystems`/`mFilters` (interface components), and its filters write `mOverwriteMedias` from that thread. Modal while it runs | work on the interface thread (its inverse) | fork, upstream lines | tree |
| **L-18** | Q3 | `GuiImageViewer.cpp:279-286`, `DisplayAspect.cpp:74-87` | The first tile decorated walks every system's games (`buildStems`) on the interface thread | work on the interface thread | fork | tree (G10 CANNOT: no library to time) |
| **L-19** | Q1 | `GuiControllersSettings.cpp:74-83` | OK / CANCEL: back presses OK and starts the mapping | a dialog whose back lands on the acting choice | upstream | tree (not pressed on the guest) |
| **L-20** | Q1 | `GuiMetaDataEd.cpp:520-528` | YES / NO / CANCEL: back presses NO, which saves without the copies | the same | upstream | tree |
| **L-21** | Q1 | `GuiMetaDataEd.cpp:626-632`, `GuiKeyMappingEditor.cpp:493-502` | SAVE CHANGES?: back presses NO, which discards the edits | a dialog whose back lands on the destructive choice | upstream | tree |
| **L-22** | Q3 | `GuiLoading.h` | `mRunning` is a plain `bool` written by the worker and read on the interface thread, and `result` is read on its strength: a data race in every `GuiLoading`. The `std::thread` is never deleted | work on the interface thread | upstream (batocera's bytes) | fixture (`stage-c/l22-guiloading-race.py`: 2 ThreadSanitizer races; control with an atomic: none) |
| **L-23** | Q7 | `GuiAutoScrape.*`, `es-app/CMakeLists.txt` | Not compiled, no caller; the inventory's `reach: shipped` is wrong for 2 paths | the inventory's side | upstream | tool-run (`git show <pin>:es-app/CMakeLists.txt \| grep -c GuiAutoScrape`: 0) |
| **L-24** | Q7 | § The titles | BIOS CHECK and SCRAPING GAMES (the fork's) neither mapped nor declared (D-UI-039), with 10 upstream titles and MOONLIGHT; #951/#965's evidence from the pages' side | a page the map does not describe and the checker cannot see | fork, upstream | tool-run (`t31-titles.py`) |
| **L-25** | Q2 | `GuiNetPlaySettings.cpp:17-19` | The default port is written at page open: a real seed, saved on the next close | (record) | upstream | tree |
| **L-26** | Q5 | `GuiBios.cpp:293-324` | BIOS CHECK is a `GuiComponent` and does not call `renderHelpPromptsEarly`, so with full-screen menus its help bar is never drawn. DETAILS and START (REFRESH) are offered by `getHelpPrompts` and shown nowhere; START refreshes unannounced (`es-code-traps.md` § Three things a font is not, the window paragraph) | a page with no help bar | fork | guest (G05, G12: no bar in any frame; START refreshed) |
| **L-27** | Q5 | `GuiBios.cpp:143-156` | A system without games is named `proper()` of its short name (Nds, Psx, Gb), where a system with games has its full name (Game Boy) | a player sentence outside the vocabulary | fork | guest (G05, G12) |

**Cited, not re-found (their dispositions at their lines):**
- T2's four routed leads:
  - #776, the relay session and spectator (`GuiNetPlay.cpp:1021`, `:1058`): this slice's lines read; the fix is #776's;
  - PL-016/#782, the manager's sentence for a failed copy: here as L-13;
  - PL-031, the nickname default at `GuiNetPlaySettings.cpp:26` and `GuiGameOptions.cpp:203`: both rows read at their lines and relying on `FileData.cpp:653-657`'s seed; the move is PL-031's;
  - PL-005's sibling (`GuiGamelistOptions.cpp:148`: `>` where `>=` is meant), read at its line.
- FD-14 (`GuiGameOptions.cpp:253`, read: names no path) and FD-21.
- T20's hasher constructions (#1170, #301).
- T21's rows in this slice's files:
  - L-23/#1185 (`GuiSettings.cpp:218-238`, read);
  - L-33 (`GuiBluetoothDevices.cpp:117-121`: DELETED whatever `forgetBluetoothControllers` returned, read);
  - L-35/#1212 (`:127`, `:150`, read);
  - #1193 (`GuiScraperStart.cpp:413-420`);
  - L-03/#1191 (`:99`);
  - `GuiKeyboardLayout.cpp:164` (Backlog #1186: the write is `/tmp/kblayout-N.svg`, a scratch render).

## Positives

- `WifiScanProcess.h`, read whole, is the argv model #1192 names:
  - `posix_spawnp` in its own process group, with a relocated low pipe end;
  - a 256 KiB cap and a deadline on the read, and a 2 s reap;
  - `-1` for every failure, and lines only on exit 0.
- Every YES / NO box lands on NO (17 of 17), and the fork's confirmations are YES first (proved: guest, G07, for DELETE GAME and the manager).
- The three `clearButtons(` sites rebuild from page methods, none from a button's own lambda.
- `GuiScraperRun`'s `delete this` at `:101` is the page deleting itself from its own input. Its help bar is drawn under full-screen menus (`:173-174`), and the spinner is never a bar.
- The manager's placeholders are never null (`SaveStateRepository.cpp:280-294`). Its help bar is drawn at 640x480 and follows the cursor (G06: BACK / LAUNCH on START NEW GAME; BACK / DELETE / COPY TO FREE SLOT / LAUNCH on a slot).
- `GuiAnalogSticksLedControls`' parse is guarded by the token count.
- No `system(`; no reboot flag; 0 non-ASCII comments.
- The French: 706 of 706 against `bccd715707`, 703 of 703 against `cada856d86`.

## Corrections to the brief

1. `:830`'s non-ASCII adjacency grep is a basic-regex error (accepted by the coordinator, 12:09 UTC).
2. `popen(` 0 → **1** (`GuiMoonlight.cpp:42`, `popen (` with a space).
3. `GuiKeyboardLayout.cpp:164` writes `/tmp/kblayout-N.svg`, a scratch render on tmpfs, not a file on the card.
4. The LED page's `tokens[6]` lead is guarded (`tokens.size() == 7`).
5. "`save()` rewrites `es_settings.cfg` twice on every visit" holds on a first visit, but not for the reason given: `Settings` counts a default as a change. Stage B's own first correction ("only on a change") was wrong in effect, and the guest corrected it (L-16).
6. `GuiAutoScrape` is not built (L-23).
7. The dialogs counted by landing replace the three-line heuristic: OK 30, NO 18, CANCEL 1, CLOSE 1.

## The runs

| Run | Exit | Wall | The figure | A FAIL would mean |
| --- | ---: | ---: | --- | --- |
| membership block (§ 2) | 0 | <2 s | 76 paths, 15,537 / 15,526 lines, 73 in the base, 12 files +1207/-129 | the slice is not the brief's |
| the scope | 1 (grep -c on 0) | 0.1 s | 90 / 14 / 76 / 0 subdirectories | the exclusion moved |
| the bases | 0 | 0.1 s | the pin; 0; `cada856d86`; `bccd715707`; 14; 724; 1; `f6c542872e` | the merge base is not the one named |
| the lines | 0 | 0.4 s | 15,526 / 15,537 / 11 | a file changed under the slice |
| the fork's delta | 0 | 0.1 s | 12 rows, 9 M 3 A, 1207/129 | the fork touched more |
| upstream's delta | 1 (grep -c on 0) | 0.1 s | 0 slice rows; 8 `guis/` commits; 73 / 73 | upstream changed a slice file since the base |
| commits per file | 0 | 0.2 s | GuiSaveState.cpp 25 … GuiGameOptions.cpp 1 | the history is not the brief's |
| the strings | 0 | 0.1 s | 891 in 37 | strings added or lost |
| the dialogs | 0 | 0.1 s | 50 in 18 | a dialog added or lost |
| the switches | 0 | 0.1 s | 26 in 6; 3 in the 4th slot; 20 in the 3rd | a store changed |
| the reads | 0 | 0.1 s | 12 in 5, 0 uncached | a read added or lost |
| the process starts | 0 / 1 | 0.1 s | system 0, popen 0 (the grep's; the census 1), runSystemCommand 6, executeScript 5 | a command added |
| the button bars | 0 | 0.1 s | clearButtons 3 in 2 | a rebuild moved into a lambda |
| the async surfaces | 0 | 0.1 s | 18 / 18 / 9 / 3 | a worker added |
| the help bars | 0 | 0.1 s | 79; 8 `.cpp` without | a bar lost |
| the parses | 0 / 1 | 0.1 s | stoi 0, stoul 0, atoi 9 in 3 | a throwing parse added |
| the two-line rows | 0 | 0.1 s | multiLine 8, addWithDescription 14 | an overload changed |
| the reboot flags | 1 / 1 | 0.1 s | 0 and 0 | a page asks for a reboot |
| the non-ASCII comments | 1 | 0.5 s | **0** files; the adjacency grep is malformed (rerun with `-F`: 0) | a non-ASCII comment near a `_(` |
| the harness sweep | 0 | 0.2 s | `GuiLoading: tests/launch-capture-gate.py`; `GuiSaveState: es-app/tests/unit/TimeTextTests.cpp`; `GuiSettings: tests/cloud-content-selection.py tests/cloud-gated-row.py tests/cloud-oauth-lifetime.py tests/wifi-profile-lifetime.py`; 15 `.py` | a harness reads a slice file |
| `es-menu-map-check` | 0 | 0.7 s | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` | a mapped screen lost |
| `es-untranslated` (both bases) | 0, 0 | <1 s | `706 fork string(s) in the source, 706 with French, 0 without`; 703/703/0 against `cada856d86` | a fork string without French |
| `es-syntax-check` | 2 | 0.1 s | `no build root` (#1137): CANNOT | -- |
| `g++ -fsyntax-only` | 1 | <1 s | `InputConfig.h:6:10: fatal error: SDL_joystick.h`: CANNOT, the missing header named | -- |
| the removal check | 0 | 0.0 s | empty against `3d591f7e30` and against the pin | a path outside the lane changed |
| `t31-callers.py` | 0 | <2 s | 39 classes, 1 without a caller | negative: 9 paths → exit 1 |
| `t31-dialogs.py` | 0 | <2 s | 50 sites; OK 30, NO 18, CANCEL 1, CLOSE 1 | negative: `--expect 49` → exit 1 |
| `t31-titles.py` | 0 | <3 s | 12 / 27 / 10 / 12 | negative: 9 paths → exit 1 |
| `t31-rows.py` | 0 | <2 s | 50 calls | negative: `addSwitch=26` → exit 1 |
| `t31-reads.py` | 0 | <2 s | 26 sites | negative: `exists=11` → exit 1 |
| `t31-pages.py` | 0 | <3 s | 37 pages, 2 header-only units | negative: 9 paths → exit 1 |
| `stage-c/l01-start-drops.py` | 1, then 0 | <5 s | FAIL at the pin; the control (START closes each page) PASS | -- (the lead) |
| `stage-c/l02-led-not-saved.py` | 1, then 0 | <5 s | FAIL at the pin; the control (one save function) PASS | -- |
| `stage-c/l05-l06-moonlight.py` | 1, then 0 | <2 s | FAIL: 3 canaries, 2 directories left; the control (quoted IP, `$HOME`) PASS | -- |
| `stage-c/l09-l10-scrape-page.py` | 1, then 0 | <5 s | FAIL: lines 4 and 5 empty, an axis dismissed; the control PASS | -- |
| `stage-c/l22-guiloading-race.py` | 1, then 0 | <5 s | FAIL: 2 ThreadSanitizer races; the control (atomic) PASS | -- |

Every harness was run against the unfixed extract first. Each FAIL-then-PASS pair is in `stage-c/runs.txt`.

## The guest cycle

**Granted** on #678 at 12:25 UTC (comment 6441815522), under T13's conditions. The guarded swap reclaim ran once before it (`READY`, swap to 0).
- **START 12:26:47 UTC** (comment 6441849481; the first line `START 12:26:47 UTC`; census qemu 1, compilers 0).
- **RETURN** (comment 6442212756; the first line `RETURN 12:45:31 UTC`; census qemu 0, compilers 0). The stop was by `tools/vm-stop` on the pidfile at 12:45:00, rc 0. Each post has its line in the shared host file.

**The image:** `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (sha256 checked OK), on a fresh 16 GiB qcow2.
- Read from the guest: `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`, `geometry 640 480`.
- Both literals were found: M7's composition's `Pending achievements stay` and the pin's `SKIPPED - YOU CANCELLED IT`. **Every frame is `image` evidence.**

| Step | What ran | Read back | Verdict |
| --- | --- | --- | --- |
| G01 | identity | above; `moonlight`, `rocknix-systems`, `analog_sticks_ledcontrol` present; ES runs as uid 0, `HOME=/storage` | -- |
| G02 | USER INTERFACE SETTINGS: a switch moved, START; then the same move, B | `es_settings.cfg`'s mtime unmoved after START, `ShowCheevosIcon=false` after B (`g02-*.txt`, frames g02-2, g02-3) | L-01 on the image |
| G03 | SCRAPER from the main menu, SCRAPE → OPTIONS → ACCOUNTS, no change | `ScraperSystems="pico-8"` written at the first switch; a second write at the next with no key changed (`g03-tabs.txt`, two passes recorded VOID first) | L-15, L-16 on the image |
| G04 | SCRAPE NOW with `eth0` down | no SCRAPING GAMES page: the main menu, AN ERROR OCCURRED : YOU'RE NOT ONLINE. TRY AGAIN WHEN YOU ARE. (g04-3) | L-09 CANNOT offline |
| G05 | BIOS CHECK (EN), REFRESH with `rocknix-systems` shadowed by an exit-1 script, one system's DETAILS | the list `7 OF 7 MISSING` (g05-1); THE BIOS CHECK RETURNED NOTHING (g05-2); DETAILS rows with their MD5 (g05-3); no help bar in any frame | L-12, L-26, L-27 |
| G06 | the manager over `TTProbe.gb` with two states; COPY on SLOT 1 over a read-only directory; COPY on a 64 MB SLOT 2 | no message, no tile, the cursor back on START NEW GAME (g06-14); the 64 MB copy written within the second, the same frame (g06-16), SLOT 3 four presses right (g06-17); the help bar and the last tile on screen at 640x480 | L-13 |
| G07 | B on DELETE GAME's and the manager's DELETE | both land on NO, the files remain (g07-*) | positive |
| G08 | NETPLAY SETTINGS (FR): ENABLE NETPLAY on, relay moved, BACK | `global.netplay=0`, `global.netplay.relay=nyc` | L-03 |
| G09 | MOONLIGHT: UNPAIR over seeded directories | "Unpaired and settings cleared", both directories intact | L-06 |
| G10 | the viewer's first open, timed | CANNOT: no library large enough to time | -- |
| G11 | the stale-read positive | CANNOT within the bound: a metadata path set while ES runs needs the on-screen keyboard | -- |
| G12 | French, after ES's restart with `system.language=fr_FR` | MENU PRINCIPAL; `7 SUR 7 MANQUANT`; MOONLIGHT's title in English with its rows in French; the PIN new | L-07, L-11 |
| G13 | the stop, the disk retired | `t31.qcow2`, 2,510,749,696 bytes, sha256 `8aee68ee915fbbc6c93eb13bd562a6728ef780a6610c4a4ea877ecb901b2a596`, removed with its firmware-variables file; the leftover check clean (`retired.txt`) | -- |

The stores' mtimes after a SCRAPER tab switch and close are in `g03-tabs.txt`. The QA accounts were not needed: no step signed in.

## The #585 lines owed

Per D-WORKFLOW-164, each upstream-side lead is weighed for upstream (none sent, D-WORKFLOW-165; rechecked against upstream's head when ready). "Present at" names local refs, which are not refreshed here.

| Upstream | File | The change | Evidence | Present at |
| --- | --- | --- | --- | --- |
| batocera-emulationstation, then ROCKNIX | `es-app/src/guis/GuiSettings.cpp` `input` / `getHelpPrompts` (START, CLOSE) | close each page through `close()` so its save functions and `onFinalize` run, or say on the bar that CLOSE discards | `stage-c/l01-start-drops.py`; G02 | `batocera/master` `b2ceb55a7`, `rocknix/master` `f6c542872` |
| ROCKNIX/emulationstation-next | `es-app/src/guis/GuiAnalogSticksLedControls.cpp` | a save function so `GuiSettings::save` writes `system.cfg` | `stage-c/l02-led-not-saved.py` | `rocknix/master` (the page is ROCKNIX's own) |
| batocera-emulationstation, then ROCKNIX | `es-app/src/guis/GuiNetPlaySettings.cpp` relay callback | `save()` before the page is replaced | G08 | `batocera/master` (the same `delete this`), `rocknix/master` |
| ROCKNIX/emulationstation-next | `es-app/src/guis/GuiMoonlight.cpp` | `Utils::String::shellQuote` on the SERVER IP; `$HOME` in the removals; the title through `_()` | `stage-c/l05-l06-moonlight.py`; G09, G12 | `rocknix/master` (the page is ROCKNIX's own) |
| batocera-emulationstation, then ROCKNIX | `es-app/src/guis/GuiLoading.h` | `std::atomic<bool> mRunning` | `stage-c/l22-guiloading-race.py` | `batocera/master` (identical bytes), `rocknix/master` |
| batocera-emulationstation | `es-app/src/guis/GuiGameOptions.cpp:204` | PLAYER PASSWORD with `password = true` | tree | `batocera/master:198` |

The rest are the fork's own and stay here.

## What T32 to T37 inherit

- **The provenance table** (§ Coverage): 3 / 9 / 64 against `cada856d86`, the 64 at `rocknix/master`'s bytes.
- **The dialog method:** the first button is read whole, never by a three-line window. The landing comes from `GuiMsgBox.cpp:116-134`'s rule, which `t31-dialogs.py` asserts from the source.
- **The title-shape table** (§ The titles). The checker's three regexes see 12 of 37 pages; a raw literal (MOONLIGHT) and a computed title (`GuiBios`' DETAILS, `GuiSettings(window, displayName)`) are invisible to it.
- **The cached-read table** (§ The reads): the scraper, RetroArch and the player are the writers of what these pages ask `exists` about.
- **The four tab-strip pages**, with their lines: `GuiThemeInstaller`, `GuiBatoceraStore`, `GuiKeyMappingEditor` (`:150-156`), `GuiKeyboardtopads` (`:78`).
- **The base's two traps:**
  - START drops what a page did not save (L-01);
  - a page with no save function never writes `system.cfg`, whatever it `set` (L-02).
