# Forward audit — M6.P2 T31, EmulationStation's other pages (#678)

Read at the pin `16dbac5211eea7e70db7394372033be2be7df829`, from the distribution worktree at `da7922a7bd` and later. Each figure below is a tool's line, kept with its output under `stage-a/` and `stage-b/`. Each lead was read at its lines before it was named. A lead is not yet a finding: stage C settles each one in `04`, with its proof.

## Coverage (76)

| Tier | Inventory's | The read's | Files | Lines (`grep -c`) | How read |
| --- | --- | --- | ---: | ---: | --- |
| fork-own | fork-own | **fork-own** | 3 (`GuiScraperRun.cpp`, `GuiScraperRun.h`, `WifiScanProcess.h`) | 527 | whole |
| fork-modified | fork-own | **fork-modified** | 9 | 3,703 | the fork's diff against `cada856d86` whole. Read whole: `GuiSaveState.cpp`, `GuiScraperStart.cpp`, `GuiBios.cpp`, `GuiSettings.cpp`/`.h`. Read at the leads' lines: `GuiImageViewer.cpp`, `GuiGameOptions.cpp`, `GuiSaveState.h`, `GuiBios.h` |
| upstream-carried | upstream-carried | **upstream-carried** | 64 | 11,307 | byte-identical to `cada856d86` and to `rocknix/master` (0 slice rows in upstream's delta, `stage-a/runs.txt`); read at the leads' lines, plus `GuiLoading.h` whole |

The twelve fork-touched files hold 4,230 lines by `grep -c ''` (`stage-a/membership.txt`). All 76 are counted by every census below: dialogs, rows, reads, titles and pages.

## The pages

`stage-b/pages.md` (`tools/t31-pages.py`) has one row per `.cpp`: class and base, what opens it, what it starts, its dialogs with where back lands, its title and the map's verdict. There are 37 pages plus 2 header-only units. Its totals match the brief's runs except one:

```text
pages 37, header-only units 2; runSystemCommand 6, executeScript 5, std::thread 18, GuiLoading< 18, postToUiThread 9, popen 1, system 0
```

`popen` reads 1 where the brief has 0: `GuiMoonlight.cpp:42` writes `popen ("moonlight -v", "r")` with a space, which the brief's `popen(` grep cannot see. Whether each start runs on the interface thread, and what bounds it, is in § Leads by site. The census is the list those readings hang on.

Who opens each class (`stage-a/callers.txt`, `tools/t31-callers.py`): 18 classes from `GuiMenu.cpp` (T26's), the game lists for the game options, the game-list options and the save state manager, and the pages for each other. **`GuiAutoScrape` has no caller, and `es-app/CMakeLists.txt` at the pin does not list it** (`git show <pin>:es-app/CMakeLists.txt | grep -c GuiAutoScrape`: 0). It is never compiled. The inventory still records its two paths as `reach: shipped`.

## The dialogs

`stage-b/dialogs.md` (`tools/t31-dialogs.py`): 50 sites in 18 files, each read whole by balanced brackets. The tool reads its landing rule from `GuiMsgBox.cpp:116-134` at the pin, where back presses the only button, else the first named OK or NO, else the last:

```text
sites 50 in 18 files; back lands on: OK 30, NO 18, CANCEL 1, CLOSE 1
```

- Every YES / NO box lands on NO: 17 sites: the fork's two (`GuiSaveState.cpp:449`, `GuiScraperRun.cpp:112`) and upstream's fifteen, `GuiScraperStart.cpp:449` and `:467` among them.
- WRITE / CANCEL (`GuiGameOptions.cpp:274`) lands on CANCEL. CLOSE (`:289`) is a single button.
- **Three landings press the choice that acts:**
  - `GuiControllersSettings.cpp:76` is OK / CANCEL, so back presses **OK** and starts the controller mapping (L-19).
  - `GuiMetaDataEd.cpp:524` is YES / NO / CANCEL, so back presses **NO**, which saves the edits without the copies (L-20).
  - The two SAVE CHANGES? boxes, `GuiMetaDataEd.cpp:629` and `GuiKeyMappingEditor.cpp:497`, land on **NO**, which discards the edits (L-21).
- The words: FAILED (`GuiNetPlay.cpp:336`, with HttpReq's error text after it); four sentence-case English boxes in `GuiMoonlight.cpp`, `Succesfully` misspelt; `<busy>` and `<busyNow>` are the manager's composed refusals. One message per family across pages: ARE YOU SURE YOU WANT TO DELETE THIS ITEM? (4 sites, identical), THIS WILL DELETE THE ACTUAL GAME FILE(S)! (2, identical), YOU ARE NOT CONNECTED TO A NETWORK (3, identical), FINISHED / OK (3, identical; `GuiAutoScrape`'s is not built).

## The rows

`stage-b/rows.md` (`tools/t31-rows.py`):

```text
calls 50: addInputTextConfigRow 15, addInputTextRow 1, addOptionList 3, addSwitch 23, addWithDescription 8
```

- **Switches:** all 23 are `storeInSettings = true` to ES-own keys in `es_settings.cfg`. They are the brief's 23: 20 by the three-argument form and 3 with a description at `GuiNetPlaySettings.cpp:38-40`.
- **Option lists:** 3 to SystemConf (`controllers.guns.*`).
- **The text rows:** 15. The scraper's six account rows go to `Settings` (`ScreenScraperUser`/`Pass`/`DevId`/`DevPass`, `IGDBClientID`/`IGDBSecret`); the three secrets are `password = true`. The netplay and Moonlight rows go to SystemConf. **PLAYER PASSWORD (`GuiGameOptions.cpp:204`) is `password = false`** (L-04).
- **`updateVal`** (`GuiSettings.cpp:218-238`) writes to the store when the editor's OK is pressed, empty or not (#1185, cited).
- **Two-line rows:** the `grep` finds 10 `addWithDescription(` lines in the `.cpp` files. Two are commented out (`GuiFavoriteMusicSelector.cpp:45-46`), leaving 8 calls: two through GuiSettings' comp form (`multiLine = true`, inside `addSwitch`/`addOptionList`), one explicit `multiLine = true` (`GuiGameOptions.cpp:126`), and five func forms at `false`.
- **Reboot flags:** none set or named in the slice (`stage-a/runs.txt`).

## The reads

`stage-b/reads.md` (`tools/t31-reads.py`):

```text
sites 26: exists 12, isFlockHeld 1, atoi 9, atof 4
```

| Site | The file | Its writer while ES runs | Cached | What a failure reads as |
| --- | --- | --- | --- | --- |
| `GuiGameOptions.cpp:41` | the game's marquee | the scraper | yes | no logo on the options menu until a restart, if the miss was remembered first |
| `GuiGameOptions.cpp:53-56` | manual, magazine, map, video | the scraper | yes | the four rows absent after a scrape until a restart (the guest's positive, § The window) |
| `GuiImageViewer.cpp:415` | a page extracted from an archive | this process (`zipFile.extract`) | yes | the extraction is reported failed if its path was asked before (to read on the guest) |
| `GuiImageViewer.cpp:629`, `:660`, `:723` | a screenshot, an image, a video | RetroArch (screenshots), the scraper | yes | a new capture not shown until a restart |
| `GuiNetPlay.cpp:679` | the game's image | the scraper | yes | the cartridge icon in place of a scraped image |
| `GuiNetPlaySettings.cpp:70` | `:/community_relay_servers.xml` | none (resources) | yes | harmless |
| `GuiFavoriteMusicSelector.cpp:19` | a music folder | the player (USB/network copy) | yes | a folder added while ES runs is not listed |
| `GuiSaveState.cpp:33` | `/var/run/cloud_sync.lock` | the cloud scripts | (flock) | an open failing for any reason but ENOENT reads as "a sync is running" (L-14) |
| `GuiAnalogSticksLedControls.cpp:20-26` | `analogsticks.led`'s seven tokens | the page itself | - | guarded by `tokens.size() == 7`; `atoi` of a non-number is 0, a dark LED -- a positive |
| `GuiKeyMappingEditor.cpp:156` | a tab's value, "0" to "3" | the page | - | positive |
| `GuiUpdate.cpp:213` | the updater's `>>> N%` line | `updateSystem`'s script | - | a non-number is 0% on the card; upstream's OS update card (D-UI-079) |
| `GuiGamelistOptions.cpp:389`, `GuiMetaDataEd.cpp:600-601` | ratings | the gamelist | - | positive |
| `GuiBios.cpp:183-187` with `ApiSystem.cpp:886` | `rocknix-systems --all`'s output | the script | - | a failed script and a check that knows nothing are one screen (L-12) |

## The titles

`stage-b/titles.md` (`tools/t31-titles.py`, which loads the checker's own patterns and `names_screen`):

```text
.cpp 37; with a title by the checker's shapes 12; by the wider sweep 27; with no _() literal title 10; pages whose every literal title is in neither the map's body nor ## Not mapped 12
```

All four of the brief's hand counts hold.
- **The twelve with a title in neither place:** BACKUP USER DATA, CONTENT DOWNLOADER, THE BEZEL PROJECT, **BIOS CHECK** (fork-modified), DEVICE OPTIONS, BLUETOOTH DEVICE LIST, the three game-list filter titles, INSTALL ON A NEW DISK, the key mapping editor's, EDIT METADATA, **SCRAPING GAMES** (fork-own) and THEMES DOWNLOADER.
- **The ten with no `_()` title:** among them `GuiMoonlight.cpp`, whose `GuiSettings(window, "MOONLIGHT GAME STREAMING")` is a raw literal. The checker cannot see it and the catalog never carries it. The map never names MOONLIGHT, although GAME SETTINGS opens the page unconditionally (`GuiMenu.cpp:5758`) and `moonlight` ships (`projects/ROCKNIX/packages/virtual/emulators/package.mk:12`) (L-07).
- **The four tab-strip pages** (#63, recorded and not moved): `GuiThemeInstaller`, `GuiBatoceraStore`, `GuiKeyMappingEditor` and `GuiKeyboardtopads` route left and right to their strips themselves.

## The merge debt

- **The bases:** `cada856d86` is the merge base with `rocknix/master` (`f6c542872e`). `bccd715707` is its parent and the base the earlier briefs used (`rev-list --count` 1). `upstream/master` is stale and was not read.
- **Upstream's side:** 14 commits past the base, 8 touching `guis/`, **0 touching a slice file**. The 64 upstream files are at `rocknix/master`'s bytes today.
- **The fork's side:** 12 files (9 M, 3 A), +1,207/-129 (`stage-a/runs.txt`), 58 commit lines (`stage-a/history.txt`).
- **What T32 to T37 read:** the provenance 3 / 9 / 64. And D-WORKFLOW-080's shape: the fork's pages here are already one file each, the shape GuiMenu's option (a) would reach.

## Leads

The questions are Q1 to Q7 as brief § 4 sets them, and the family is from the brief's list. "Fork" means the fork's lines; "upstream" means a contained fix under rule 6, with a #585 line. Severity is the lane's first reading, settled in `04`.

| Lead | Q | Lines | What the read shows | Family | Side | Proof |
| --- | --- | --- | --- | --- | --- | --- |
| **L-01** | Q2 | `GuiSettings.cpp:106-112`, `:133-139` (START, CLOSE on the bar); `GuiScraperStart.cpp:542-548`; `GuiMetaDataEd.cpp:620-624` | START deletes every page with `delete window->peekGui()`. That never calls `close()`, so no page's `save()` or `onFinalize` runs and every open page's unsaved choices are dropped. The settings pages, fork cloud pages included, apply on close. Identical in `batocera/master` (`b2ceb55a7`) and `rocknix/master` | a state write that can lose the record | upstream, reaching the fork's lanes | host: the extracted `input`/`close`/`save` over doubled stores; guest: a switch toggled, START, `es_settings.cfg` read |
| **L-02** | Q2, Q3 | `GuiAnalogSticksLedControls.cpp:62-87` | Each slider step runs `/usr/bin/analog_sticks_ledcontrol` on the interface thread and `SystemConf::set("analogsticks.led")` in memory. The page has no save function and `GuiSettings::save` returns at `:88-89`; nothing saves `system.cfg` at exit (`saveSystemConf` has no caller in `main.cpp` or `es-core`). The quirks' `ledcontrol` reads the key at boot. **The colour is lost at a restart** unless another page saves `system.cfg` first | a state write that can lose the record | upstream | host harness; the guest shows the row only with `DEVICE_ANALOG_STICKS_LED_CONTROL=true` (`GuiMenu.cpp:2197`) |
| **L-03** | Q2 | `GuiNetPlaySettings.cpp:155-187` | Changing USE RELAY SERVER runs `delete this` and opens a new page, without `save()`. **ENABLE NETPLAY, toggled before, is dropped.** The delete runs inside the option list's own callback; nothing is touched after it (`OptionListComponent.h:310`/`:323` return at once), recorded as blindspot 4's shape | a state write that can lose the record | upstream | host harness; guest: toggle, relay change, BACK, `system.cfg` read |
| **L-04** | Q2 | `GuiGameOptions.cpp:204` | PLAYER PASSWORD is `password = false`: the netplay password is shown on the row and in the editor | a credential's sink | upstream | rows table; guest frame |
| **L-05** | Q6 | `GuiMoonlight.cpp:282`, `:304`, `:306` | The SERVER IP the player typed goes unquoted into `popen` (`executeScriptLegacy`, `ApiSystem.cpp:2269`). The pairing callback writes a host parsed from moonlight's output back to `moonlight.host` (`:310-311`) | a command built from a player's string | upstream | host: the command run as `popen` does in bubblewrap, with a canary; guest: SERVER IP `x;touch /tmp/t31` and PAIR |
| **L-06** | Q4 | `GuiMoonlight.cpp:330-333` | `rm -r "~/.cache/Moonlight Game Streaming Project"`: a tilde inside double quotes is not expanded, so nothing is removed, and the box says UNPAIRED AND SETTINGS CLEARED | a check whose failure reads as success | upstream | host: both commands in bubblewrap over a fake HOME; guest: the conf seeded, UNPAIR, the directories listed |
| **L-07** | Q5, Q7 | `GuiMoonlight.cpp:268`, `:295-336` | The page title is a raw English literal (no `_()`, no French, invisible to the checker). Four boxes are in sentence case, one misspelt. The page is neither mapped nor declared | a player sentence outside the vocabulary; a page the map does not describe and the checker cannot see | upstream | titles table; guest frames EN/FR |
| **L-08** | Q5 | `GuiScraperRun.cpp:132-145` | `SKIPPED - YOU CANCELLED IT`, a fourth SKIPPED reason; the comment argues it; no register row | a player sentence outside the vocabulary | fork | **for the pause** (a decision; an ID the coordinator assigns) |
| **L-09** | Q4 | `GuiScraperRun.cpp:142`, `:225`, `:231` | A run where every game errored and the scraper did not fail reads COULDN'T FINISH and the counts. There is no why (line 4 needs `p.failed`) and no next step (line 5 needs `done - errors > 0`) | a check whose failure reads as success (half of it) | fork | host: `outcomeWord` and the finished rows over a `progress()` double; guest: SCRAPE NOW with the network down |
| **L-10** | Q1, Q4 | `GuiScraperRun.cpp:90-103` | Once finished, any non-zero input dismisses the outcome. That includes an axis past its deadzone, so stick drift can clear an outcome before it is read | (page) | fork | host: `input` over an axis event; the guest's QMP cannot send an axis -- **UNTESTABLE** there |
| **L-11** | Q5 | `GuiBios.cpp:220-230` | The row summary is built word by word (`N` + OF + `M` + MISSING), so the French reads `2 SUR 5 MANQUANT` | a player sentence outside the vocabulary | fork | guest FR frame; the catalog |
| **L-12** | Q4 | `GuiBios.cpp:183-187`, `ApiSystem.cpp:886` | A failing or absent `rocknix-systems` returns the same empty vector as a check that knows nothing: THE BIOS CHECK RETURNED NOTHING, with no recovery line | a check whose failure reads as success | fork | host: a doubled `getBiosInformations`; guest: the script shadowed by a failing one |
| **L-13** | Q3, Q4 | `GuiSaveState.cpp:507-529` | COPY TO FREE SLOT: `copyToSlot` runs on the interface thread (blindspot 45's sibling). `slot < 0` (no free slot) is silent. Once T2's `f11e7528a` lands, a `false` copy is silent too (PL-016, #782); at the pin `copyToSlot` returns `true` over an unchecked `copyFile` (SS-4) | a check whose failure reads as success; work on the interface thread | fork | guest: W-5's shape (a read-only save-state directory), the frame after; timed copy of a large state |
| **L-14** | Q4 | `GuiSaveState.cpp:26-36`, `AtomicFileUtil.cpp:440-442` | Any open failure but ENOENT is read as "a sync is running". It fails closed, with the wrong words. ES runs as root on the image, so EACCES is hard to reach: a keep-an-eye candidate | (page) | fork | host: `savesTreeBusy` over a lock it cannot open |
| **L-15** | Q2 | `GuiScraperStart.cpp:166-210` | An empty selection saved from the main menu reads back as "nothing remembered", so every system is selected: "none" cannot be kept. And the first close or tab switch from the main menu stores the default set, so a system added later is not selected | a row whose store is wrong | fork | host: the save functions over doubled stores |
| **L-16** | Q2, Q3 | `GuiScraperStart.cpp:34-37`, `GuiSettings.cpp:83-96`, `Settings.cpp:471` | `save()` on every tab switch writes `es_settings.cfg` only when a value changed (`mWasChanged`). The brief's "twice on every visit" holds only for a visit that changes something | (corrects the brief) | fork, upstream | guest: mtimes across tab switches with and without a change |
| **L-17** | Q3 | `GuiScraperStart.cpp:475-494`, `:97-100` | `getSearches` runs on `GuiLoading`'s worker, reading `mSystems`/`mFilters` (interface components), and its filters write `mOverwriteMedias` from that thread. Modal while it runs, so the shape is a data race by reading | work on the interface thread (its inverse) | fork, upstream lines | by reading |
| **L-18** | Q3 | `GuiImageViewer.cpp:279-286`, `DisplayAspect.cpp:74-87` | The first tile decorated walks every system's games (`buildStems`) on the interface thread | work on the interface thread | fork | guest: the viewer's first open timed over the seeded library |
| **L-19** | Q1 | `GuiControllersSettings.cpp:74-83` | OK / CANCEL: back presses OK and starts the mapping | a dialog whose back lands on the acting choice | upstream | dialogs table; guest frame after B |
| **L-20** | Q1 | `GuiMetaDataEd.cpp:520-528` | YES / NO / CANCEL: back presses NO, which saves without the copies | the same | upstream | the table |
| **L-21** | Q1 | `GuiMetaDataEd.cpp:626-632`, `GuiKeyMappingEditor.cpp:493-502` | SAVE CHANGES?: back presses NO, which discards the edits | a dialog whose back lands on the destructive choice | upstream | the table; guest frame |
| **L-22** | Q3 | `GuiLoading.h` | `mRunning` is a plain `bool`, written by the worker and read on the interface thread, and `result` is read on its strength: a data race in every `GuiLoading` (18 in the slice, 41 lines in the tree). The `std::thread` is never deleted | work on the interface thread | upstream | host: the header under `-fsanitize=thread` with doubles |
| **L-23** | Q7 | `GuiAutoScrape.*`, `es-app/CMakeLists.txt` | Not compiled, no caller; the inventory's `reach: shipped` is wrong for 2 paths | a page the map does not describe (the inventory's side) | upstream | the CMake grep |
| **L-24** | Q7 | the titles table | BIOS CHECK and SCRAPING GAMES (the fork's) are neither mapped nor declared (D-UI-039), with 10 upstream titles. #951/#965's evidence from the pages' side | a page the map does not describe and the checker cannot see | fork, upstream | the titles table |
| **L-25** | Q2 | `GuiNetPlaySettings.cpp:17-19` | The default port is written at page open: a real seed, saved on the next close | (record) | upstream | by reading |

**Cited, not re-found:** #776 (`GuiNetPlay.cpp:1021`, `:1058`), PL-016/#782, PL-031 (the nickname rows at `GuiNetPlaySettings.cpp:26`, `GuiGameOptions.cpp:203`), PL-005's sibling (`GuiGamelistOptions.cpp:148`: `>` where `>=` is meant, read at its line), FD-14 (`GuiGameOptions.cpp:253`), FD-21, T20's hasher constructions (#1170, #301), T21's L-23/#1185, L-33 (`GuiBluetoothDevices.cpp:117-121`: DELETED whatever `forgetBluetoothControllers` returned), L-35/#1212, #1193, L-03/#1191.

## Positives

- `WifiScanProcess.h`, read whole, is the argv model #1192 names:
  - `posix_spawnp` in its own process group;
  - a relocated low pipe end;
  - a 256 KiB cap and a deadline on the read;
  - a 2 s reap;
  - `-1` for every failure, and lines only on exit 0.
- Every YES / NO box lands on NO (17 of 17; the 18th NO landing is the three-button box of L-20); the fork's confirmations are YES first.
- The three `clearButtons(` sites rebuild from page methods, none from a button's own lambda.
- `GuiScraperRun`'s `delete this` at `:101` is the page deleting itself from its own input, after which nothing is touched. Its help bar is drawn under full-screen menus (`:173-174`), and the spinner is never a bar.
- The manager's placeholders are never null (`SaveStateRepository.cpp:280-294`), so the help bar's dereference at `:586` is safe.
- `GuiAnalogSticksLedControls`' parse is guarded by the token count.
- No `system(`; no reboot flag; 0 non-ASCII comments.
- The French: 706 of 706 against `bccd715707`, 703 of 703 against `cada856d86`.

## Corrections to the brief

1. `:830`: the non-ASCII adjacency grep is a basic-regex error (accepted by the coordinator, 12:09 UTC).
2. `popen(` 0 → **1** (`GuiMoonlight.cpp:42`, `popen (` with a space).
3. `GuiKeyboardLayout.cpp:164` writes `/tmp/kblayout-N.svg`, a scratch render on tmpfs, not a file on the card.
4. The LED page's `tokens[6]` lead is guarded (`tokens.size() == 7`).
5. "`save()` rewrites `es_settings.cfg` twice on every visit": only on a visit that changes a value (L-16).
6. `GuiAutoScrape` is not built (L-23).
7. The dialog count by landing replaces the three-line heuristic: OK 30, NO 18, CANCEL 1, CLOSE 1.

## The runs

| Run | Exit | Wall | The figure | A FAIL would mean |
| --- | ---: | ---: | --- | --- |
| membership block (§ 2) | 0 | <2 s | 76 paths, 15,537 / 15,526 lines, 73 in the base, 12 files +1207/-129 | the slice is not the brief's |
| § 5 runs (`tools/t31-run-runs.py`, `stage-a/runs.txt`) | 0 each but the grep counts on 0 (1, by design) | 0.0 to 0.7 s each | as `00` § Stage A lists | a figure drifted from the brief |
| `t31-callers.py` | 0 | <2 s | 39 classes, 1 without a caller | a basename count other than 39 (negative: 9 paths → 1) |
| `t31-dialogs.py` | 0 | <2 s | 50 sites; OK 30, NO 18, CANCEL 1, CLOSE 1 | a site count other than 50, or GuiMsgBox's rule changed (negative: `--expect 49` → 1) |
| `t31-titles.py` | 0 | <3 s | 12 / 27 / 10 / 12 | the brief's hand counts are wrong (negative: 9 paths → 1) |
| `t31-rows.py` | 0 | <2 s | 50 calls | a builder's total moved (negative: `addSwitch=26` → 1) |
| `t31-reads.py` | 0 | <2 s | exists 12, isFlockHeld 1, atoi 9, atof 4 | a read was added or lost (negative: `exists=11` → 1) |
| `t31-pages.py` | 0 | <3 s | 37 pages, the census totals | a total disagrees with the brief's runs (negative: 9 paths → 1) |
| `es-menu-map-check` | 0 | 0.7 s | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` | a mapped screen lost |
| `es-untranslated` (both bases) | 0, 0 | <1 s | 706/706/0; 703/703/0 | a fork string without French |
| `es-syntax-check` | 2 | 0.1 s | `no build root` (#1137) | -- (CANNOT) |
| `g++ -fsyntax-only` | 1 | <1 s | `InputConfig.h:6:10: fatal error: SDL_joystick.h` | -- (CANNOT; the host proofs are extraction harnesses) |

## The guest cycle

Planned in `stage-b/window-plan.md` and asked for on #678. Its record will be `guest-cycle/`.
