# Second opinion on a code audit -- M6.P2 T2, EmulationStation's launch path, epic tier

You are the second reader of a code audit, and the reviewer from Google (Gemini 4 Argon); a second reviewer from a third lab reads the same packet independently, and neither of you sees the other's answer. You cannot run commands or open the repository. Everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the command output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope is twenty C++ files of an EmulationStation fork, the front end of a handheld Linux distribution. The files cover the launch chain (`ViewController::launch` → `FileData::launchGame`, its gates, the command it builds and the return path), the systems table (`SystemData`), the save-state classes, the offline-achievements cards (`ProxyCards`) and `main.cpp`. They were read at one commit, the pin `16dbac5211`, which every image carries. The binary is built with `-DROCKNIX=1`, and the shipped launch template is `/usr/bin/runemu.sh %ROM% -P%SYSTEM% --core=%CORE% --emulator=%EMULATOR% --controllers="%CONTROLLERSCONFIG%"`. Commands run through `system()` (`/bin/sh`). Most of the three large files is the fork's upstream (batocera) code, byte for byte; the fork's lines are named in the packet.

The first reader is Claude Opus 5.5 (Anthropic). The audit is a renovation: besides defects, its findings answer seven questions (Q1 modernize, Q2 standards, Q3 bugs, Q4 package currency, Q5 efficiency, Q6 dead ends, Q7 clarity). No runtime proof has run yet (the test host was held for another lane); every behaviour claim is a reading.

Answer in three parts, in this order:

1. **Your own findings first.** List every defect, gap or unsafe seam in the excerpts that is not already one of the first reader's findings. One line each: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the packet's `file:line`, and what fails and when.
2. **Refute the first reader.** For every finding at Medium (FD-14, SS-1, SD-2, VC-1), and for any Low you think mis-graded (FD-8, SD-3, SD-4/FD-15, MN-3, SB-2 and FD-18 especially), say one of: agree, disagree, re-grade, or narrow. In each case say what would make the finding false and whether the packet shows it. Say also whether anything graded Medium should be High (the first reader graded nothing above Medium).
3. **What you could not judge.** The claims the packet does not let you verify, so the orchestrator knows where its evidence was thin.

Everyday words, no hedging: a finding either survives your reading or it does not, and you say which.

---
# Forward Audit — M6.P2 T2, EmulationStation's launch path

**Auditor:** Code Auditor skill, with the renovation face (plan § 4)
**Date:** 2026-10-23
**Subject:** #649, the twenty EmulationStation paths at the pin `16dbac5211`
**Spec:** `docs/reviews/briefs/es-launch-path.md` version 2 (§ 7 = #649's checklist)

---

## Running Notes

Findings are written as each unit is read (`READ → WRITE → REPEAT`). Line numbers are the pin's (`git -C $W show $PIN:<path>`). Every finding is a lead until Phase 4.5. A runtime claim stays a lead until the guest proves it, and the guest is queued for the host's return (brief § 5).

## Mechanical checks (brief § 5)

| Check | Command | Exit | Summary line | When |
| --- | --- | ---: | --- | --- |
| credential quoting (`quoting` suite) | `(cd $W && python3 -I tests/credential-quoting.py $W)` | 0 | `credential-quoting: 9 credential call site(s), 9 quoted, 0 bare` | 17:26, at the pin |
| menu map (`menumap`) | `tools/es-menu-map-check --es-src $W --ref $PIN` | 0 | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` | 17:26, at the pin |
| French (`french`) | `tools/es-untranslated --es-src $W` | 0 | `703 fork string(s) in the source, 703 with French, 0 without` | 17:26, at the pin |
| vocabulary | `tools/vocabulary-check --es $W` | 0 | `163 string(s) with back up / backup, save state or Wi-Fi judged, 0 wrong` | 17:26, at the pin |
| unit tests `es-unit-tests` | brief § 5 recipe | — | queued (host held for M7) | — |
| `tests/app-unit`: `proxycards-tests`, `bookkeeper-tests`, `jobs-tests` | brief § 5 | — | queued | — |
| `tests/launch-capture-gate.py`, `tests/launch-deferred-state.py`, `tests/hasher-offline-index.py` | brief § 5 | — | queued (they compile) | — |
| syntax-only compile per edited `.cpp` | #699 recipe or the fixed tool | — | no `.cpp` edited yet | — |
| `tools/time-to-play --vm --only launch,exit,g2g` | brief § 5 | — | queued (guest) | — |
| `tools/es-launch-memory` | brief § 5 | — | queued (guest) | — |

## Findings, written as each unit is read

### Group 1. `es-app/src/LaunchCommand.h` (57 lines, fork-own; read whole)

- **Reading.** `launchToken` walks whole shell words (`Utils::CommandLine::wordEnd`, `es-core/src/utils/CommandLineUtil.h`, T36's) and keeps the value of the **last** word beginning with `prefix`. `launchArgument` falls back when the token is empty. The header states the divergence from `runemu.sh`'s `${ARGUMENTS##*-P}` (the last occurrence anywhere) and assigns the launcher side to the launcher. That is T1's F-07 (#730) for `--core=`/`--emulator=`, and `-P` is the same shape there.
- **LC-1 (Q7, Low, lead).** A token's value keeps any quoting inside its word. `--core='a b'` would give `'a b'` with the quotes, since `substr` copies the word's bytes. It is unreached: core and emulator names come from the systems table (group 2 checks the charset). It is recorded for Q7: the header does not say that values are raw words.
- **Q1/Q6.** The two readers of one argument line (`launchToken` here, `runemu.sh` there) are the duplicated parsing Q1 names. The seam row is in `03-retrospective.md` § 3.5. There is nothing to remove here, and both callers are live (`FileData.cpp:719-720`, `main.cpp`).

### Group 1. `es-app/src/FileData.cpp`, the command builder (`formatCommandLineArgument` :528-534, `getlaunchCommand` :536-723; read whole)

The shipped template (the distribution's `distributions/ROCKNIX/config/functions:128`, `add_es_system`) is `/usr/bin/runemu.sh %ROM% -P%SYSTEM% --core=%CORE% --emulator=%EMULATOR% --controllers="%CONTROLLERSCONFIG%"`. Per-system overrides come from `config/emulators/<system>.conf` (`SYSTEM_COMMAND`), and the `tools` systems use `%RUNCOMMAND%` (rewritten by `virtual/emulators/package.mk:1735-1739` to `weston-terminal`/`foot`/`run %ROM%`). In the tree, `grep -rn -o -E '%[A-Z_]+%' projects/ROCKNIX/packages/virtual/emulators/` counts `%ROM%` 3 and `%RUNCOMMAND%` 3, and `functions:128` adds `%SYSTEM% %CORE% %EMULATOR% %CONTROLLERSCONFIG%`. So `%BASENAME%`, `%ROM_RAW%`, `%GAMENAME%`, `%SYSTEMNAME%`, `%GAMEINFOXML%`, `%HOME%` and `%NETPLAY%` are not in the shipped command. The guest's generated file is read when the guest runs (queued).

- **FD-1 (Q3, Low; Q6), corrected 17:4x from a Medium lead: the netplay client branch computes three values the image never uses, one of them for a field nothing sets, and a spectator joins as a player.** `:659-681`: for `CLIENT`/`SPECTATOR`, `pass` (`-netplaypass`), `session` (`-netplaysession`) and `mode` are computed. Then the `#if ROCKNIX` branch (`:677-678`) writes `--connect <ip> --port <port> --nick <nick>` and uses none of them. Only the `#else` (`:680`, upstream's, unreached with `-DROCKNIX=1`) uses them. The caller search corrects the first reading:
  - `git grep -n netplayClientPassword $PIN -- es-app/src es-core/src` finds the field only at `FileData.h:69` (declared) and `FileData.cpp:664-665` (read). **Nothing assigns it**, so there is no password to drop on any build. That makes it a Q6 row, a dead field, not a Q3 defect.
  - `session` is filled (`GuiNetPlay.cpp:1021`, `entry.mitm_session`) and unused on the image. The comment at `:667` says it should reach RetroArch as `--mitm-session`. A relay-only host (one reachable only through the lobby's MITM relay) is then joined at its own IP and port, which is a Q3 lead for T31 (`GuiNetPlay`) to grade.
  - **`SPECTATOR` is set** (`GuiNetPlay.cpp:1058`, `opts.netPlayMode = NetPlayMode::SPECTATOR`) and on the image becomes the same `--connect` as a client. A player who chose to watch takes a player's seat. This is Q3, Low: the ROCKNIX branch ignores the mode it is given. Whether `runemu.sh` can express spectating (`--spectate`?) is the launcher's question (T1).
  - The guest cannot show a netplay join without a host, so this is a lead for the integration run.
- **FD-2 (Q3, Low; a precondition: a player's own systems template): `formatCommandLineArgument` (:528-534) double-quotes only a name containing a space and escapes only `"`.** Inside double quotes the shell still expands `$`, backtick and `\`. A scraped game name such as `$(...)` or one with a backtick runs as a command when a template uses `%GAMENAME%` or `%SYSTEMNAME%`. Without a space it is not even quoted, so `;`, `&` and `*` act too. The shipped template does not use either placeholder (above), so this is reachable only under `es_systems_custom.cfg`. `Utils::String::shellQuote` already exists and is used at `:678` and `:691`. The guest proof (queued) is a template under `/storage` using `%GAMENAME%` with a game named `a;touch${IFS}/tmp/x`.
- **FD-3 (Q3, Low; the same precondition): `%BASENAME%` (:619, :624) and `%ROM_RAW%` (:620, :625) are substituted raw.** A ROM file name with a space or a shell character splits or expands. Only `%ROM%` goes through `getEscapedPath` (:618; T36's character list, read below for what it leaves).
- **FD-4 (Q7/Q5, Low): building the command writes `system.cfg`.** `:653-657` sets `global.netplay.nickname` and **saves `system.cfg`** when the nickname is empty, on every call. Callers include `GuiMenu.cpp:11325`, which only stores `global.bootgame.cmd`. A function named `get...` that persists a setting is the "name is not a behaviour" shape. The write goes through `SystemConf::saveSystemConf` (T21's last-known-good path). The `Settings`/`SystemConf` store written is named, as brief § 2 asks: `system.cfg`, key `global.netplay.nickname`.
- **FD-5 (Q6): branches unreached on the image.** `-monitor` (:699-701) needs ` -system ` in the command, and the shipped command has none. The `forceCore` appends (:609-616) are no-ops on the shipped command, because `find("-emulator")` matches inside `--emulator=` (reached, inert). `#ifdef WIN32` (:633-637, :672-676, :685-689) and the `#else` netplay forms (:680, :693) are unreached. The commented-out extension block (:586-605) is dead text. All are Q6 rows; none is a removal, because the fork merges upstream through them (brief § 4, D-WORKFLOW-185's shape).
- **FD-6 (Q5, Low): `InputManager::configureEmulators()` runs on every command build (:547)**, including `includeControllers == false` (the boot-game store), where its result is discarded. The cost is to be measured, and it is small beside the launch.
- **FD-7 (Q3 seam lead, T36): the controllers blob is spliced inside the template's double quotes (`--controllers="%CONTROLLERSCONFIG%"`, :647-648).** `configureEmulators()` builds it from device names the kernel reports. A pad whose name contains `"`, `$` or a backtick would break or expand the line. This is posted as a lead for T36 (`InputManager`); the quoting is the template's (T3, `functions:128`) and the blob's.
- **Reached and correct:** `%ROM%` through `getEscapedPath`, and the ROCKNIX `%NETPLAY%` forms with `shellQuote` on the IP, port and nick (#275's fix, `:678`, `:691`). `options.launchedEmulator/Core` come from the finished command (D-CLOUD-062, `:716-720`).

### Group 1. `es-app/src/FileData.cpp`, the gates, the launch and the return (`getMessageFromExitCode` :725-761, `launchNow` :774-794, `rememberSaveState` :800-810, `launchWhenGone` :818-850, `captureGate` :876-926, `launchGame` :928-1328; read whole)

- **FD-8 (Q3, Low, latent; graded down from Medium after group 2's trigger search): a deferred launch holds a raw `FileData*` across a wait.** The gates' answers capture `this` (`:997`, `:1014`, `:1035`, `:1050`). `launchWhenGone` (`:818-849`, up to 20 s) and `captureGate`'s spinner (`:898-924`, up to 10 s) carry `game`, and `launchNow` posts it to the next frame (`:776`). `options.saveStateFile` (#308 F-ES-11) protects the save state against the repository's refresh, but nothing protects the game.
  - **What can delete it during the wait.** `git grep -n -E 'rescanChangedFolders|rescanIfFolderChanged' $PIN -- es-app/src es-core/src` finds exactly two posts: one at a game's exit (`FileData.cpp:1223`) and one when the transfer page is dismissed after a restore (`GuiCloudTransfer.cpp:335`). The first runs on the frame after the exit, before the next press. The second runs after the page, which owns the screen (D-UI-078), is closed. Neither lands inside a gate's wait.
  - The remaining path is `ViewController::reloadAllGames` (it deletes every system and every page), wired to `Window::setReloadGamelistsCallback` (`main.cpp:818`), which the HTTP API's game-list reload calls. A reload requested during a gate's wait deletes the box or spinner and the files. A `launchNow` already posted (`FileData.cpp:776`) then calls `ViewController::launch` with freed memory.
  - So: Low, latent, reachable through the API on the loopback only. A fix that finds the game again by path in `launchNow`, as it already does for the save state, closes it. The guest proof (queued): `POST /launch` over a held gate, then the reload endpoint, then the answer; the journal is checked for a crash backtrace (`device-builds.md` § Reading a crash).
- **FD-9 (Q3 seam lead, T33/T21 `Scripting`): the `game-start` event passes the ROM's stem raw and the scraped name (`:1083-1086`).** `Scripting::executeScript` (`es-core/src/Scripting.cpp:88-148`, context read) builds a shell string, quoting an argument only when it contains a space and stripping `"`. A ROM named `a$(id)b.zip` or a scraped name with a backtick and no space reaches `sh` unquoted when any script sits in `/usr/bin/scripts/game-start/`, the user's `scripts/game-start/` or `/var/run/emulationstation/scripts/`. The distribution ships none (`grep -rn 'scripts/game-start' projects/ROCKNIX/packages --include=package.mk`: none; the old `game-end` hook was retired, `:1227-1237`). So the precondition is a player's own script. The call site is in the slice and the quoting is `Scripting`'s, so this is posted as a lead for its slice. (The brief names `Scripting` T33's in § 2 and T21's in the interacting list; **delta** recorded, the coordinator's to place.)
- **FD-10 (Q2, Low): the fallback error text is misspelled and reaches the player.** `:760` reads `_("UKNOWN ERROR") + " : " + <code>`. The French catalogue has `msgid "UKNOWN ERROR"` → `ERREUR INCONNUE` (`locale/lang/fr/.../emulationstation2.po:3612`). batocera's `FileData.cpp` carries the same misspelling (`git show batocera/master:es-app/src/FileData.cpp | grep -c 'UKNOWN ERROR'` = 1), so a fix changes an upstream string and its catalogue key together. `es-player-text.md`'s register also marks `AN ERROR OCCURRED:\r\n...` and the bare exit code as the developer's words (`:1325`; § Outcome words). It is reached by an exit code 200 to 300 without the cases 200 to 205/250/299.
- **FD-11 (Q2, Low): the 250/299 box shows a file's text verbatim to the player.** `:741-757` reads `/tmp/launch_error.log` and returns it as the message. `cheevos_dolphin.sh:39` writes `DOLPHIN DID NOT START\n<title>\n\n<message>` there, and `runemu.sh:498` removes it. Whether every writer uses player words is the writers' slices' (the Dolphin wrapper, T4/T5). Two details are this slice's. `exists()` is the cached form: the file is written by another process during the run, and the cache was reset at `:1113` after the run, so this read is fresh. That is correct by order, not by `exists(path, false)`, and recorded for Q7. And the text is unbounded in length on a 640x480 box.
- **FD-12 (Q2, Low): the capture-failure toast prefixes its glyph with two spaces.** `:1294` has `_U("  ")`. `es-ui-style-guide.md` § Glyphs: a row label takes two trailing spaces, a notification one. The other fork toasts are to be counted in Phase 3.6.5 before this is a finding rather than a house exception.
- **FD-13 (Q7, Low): a comment says what the code does not.** `:1134-1135` says `onGameEnded` "renumbers slot files and restores .state.auto". Group 3 reads `SaveState::onGameEnded` (the brief's lead: 192 to 198 there say it does not renumber).
- **Reached and correct (read):**
  - The capture command quotes every argument (`:1147-1153`, `shellQuote`).
  - The exit sync is skipped when another game launched since (generation, `:1295`) or a launch waited on the capture (`:1303`); `sExitGeneration`, `sCaptureInFlight` and `sCaptureWaitedOn` are read with `.load()` and declared atomic (to confirm at their declarations, `:83-95`).
  - The detached worker posts through `AppWindow::post` (`5443b5301`, workers stop posting once `main()` lets the window go).
  - Play count and time only on exit 0 (`:1192-1209`; D-LAUNCH-001: the hotkey's signal reads as a clean exit).
  - The four gates ask with the safe verb last and `KEEP WAITING` as the `nullptr` choice (D-UI-096). The back-button accelerator binds to `NO`/`OK` only, so on these boxes it falls to the last button, `KEEP WAITING`, which is the safe one (`es-ui-style-guide.md` § Confirmations).
- **Q5 (to measure):**
  - Between the press and the command: `captureGate`'s up to 300 ms on the interface thread (`:888`, by design, no spinner flash); `getlaunchCommand` (`configureEmulators`, FD-6); `AudioManager`/`VolumeControl` deinit; `window->deinit`; `malloc_trim(0)` (`:1080`); `fireEvent("game-start")` (directory scans of three paths even when empty, `Scripting.cpp:158-207`); `convertP2kFile`; `WatchersManager::pause`.
  - After the exit: `FileSystemCache::reset`; the save-state `refresh` (a directory scan, `:1120`); `CaptureRotation::recordAfterSession`; `fireEvent("game-end")`; `window->init`; `refreshCollectionSystems` and `saveToGamelistRecovery` on exit 0 (`:1207-1208`); a second `malloc_trim`; then the posted rescan and the detached capture and sync.
  - Each is itemised against the guest's time-to-play numbers when they run.

### Group 1. `es-app/src/FileData.cpp`, the rest (:1-523, :1331-2680)

**Provenance inside the file:** `git diff -U0 1750dded8 $PIN -- es-app/src/FileData.cpp` has hunks only at 2, 36-48, 52, 85-126, 677-683, 690-696, 716-721, 763-927, 932-1058, 1076-1081, 1090, 1095, 1123-1170 and 1213-1318 (526 lines added, 1 removed). **Lines 1331-2680 and the property, path and art code before 523 are byte-identical to batocera's.** So this fork-own path is about a fifth fork code by line, and the rest is upstream code the fork carries. That calls for Q6 and Q4 first on those lines (brief § 4's lens by provenance), plus Q3 where a defect reaches the image. The inventory's tier is per file, so this is recorded for Q7: nothing in the file says which part is whose.

- **FD-14 (Q3, Medium, upstream-carried code; lead → bug candidate): DELETE GAME removes every absolute path an `.m3u` lists, and any `..` path a `.cue` names.** `getContentFiles` (`:1386-1476`) inserts an `.m3u` line that `isAbsolute` as is (`:1446-1447`). `.cue` `FILE` tokens go in as `path + "/" + token` with no containment (`:1416-1418`), and so do `.gdi` tracks (`:1465-1467`). `deleteGameFiles` (`:1478-1507`) then `removeFile`s each one (`:1505-1506`). It is reached from GAME OPTIONS > DELETE (`GuiGameOptions.cpp:533`) and the game-list options' delete (`GuiGamelistOptions.cpp:485`), each behind a confirmation that names the game, not the files. A playlist that names `/storage/.config/system.cfg`, or a cue with `FILE "../../bios/scph1001.bin"`, takes those files with it. The `else if (trim[0] == '/') continue;` at `:1448` reads as a guard against exactly this, and it is unreachable, because `isAbsolute` is true for every `/` path on Linux. The other consumers read the list for hashing and scraping (`SystemData.cpp:243`, `ScreenScraper.cpp:297`), which is harmless. The fix keeps `getContentFiles` and makes `deleteGameFiles` refuse any file not under the game's own directory. `Already written:` nothing; the defect is in a delete. Guest proof (queued): a fixture `.m3u` naming a sentinel file under `/storage/` outside `roms/`, DELETE through the API or a walk, and the sentinel's presence checked.
- **FD-15 (Q3, Low, upstream-carried): the sort id's bound is off by one.** `:1658-1662`: `if (currentSortId > getSortTypes().size()) currentSortId = 0;`, then `.at(currentSortId)`. An id equal to the size passes the check and throws `std::out_of_range`, which ends the interface. The id comes from `setSortId` (`SystemData.cpp:1937`, group 2 reads its bound) and from a system's stored sort (`es_settings.cfg`). Reachable only with a stored id equal to the count. `CollectionSystemManager.cpp:540` uses `.at()` on a set value too. To be confirmed at `setSortId`.
- **FD-16 (Q6/Q7, Low, upstream-carried):**
  - `getThumbnailPath` (`:276-279`) and `getImagePath`/`getVideoPath` test `getType() == FOLDER` inside a branch that requires `getType() == GAME`, so the folder arm never runs.
  - `resetSettings` (`:377-380`) is empty.
  - `getBreadCrumbPath` assigns `parent` twice (`:151-152`).
  - `getTokens`' quote case falls through to the separator case without a marker (`:1356-1361`); it is intentional, and a reader stumbles.
  - Several getters persist found art into metadata (`setMetadata` in `getThumbnailPath`, `getVideoPath`, `getMarqueePath`, `getImagePath`), which marks the game list dirty from a read.
  - Each is a Q6/Q7 row, not a removal, because the fork merges batocera through these lines.
- **FD-17 (Q1, Renovation, upstream-carried):** `mDisplayName` is a raw owning `std::string*` (`:207-219`, `:197-198`) where `std::optional<std::string>` would do. The C-style `(FolderData*)this` casts (`:278`, `:404`, `:456`) and `ifstream(WINSTRINGW(...))` with manual `close()` (`:1407-1421`) are the same shape. Changing upstream lines costs merge friction and buys little, so these are recorded, not proposed.
- **FD-18 (Q3/Q1, Low): `mRunningGame` is a plain static `FileData*` (`:83`, `FileData.h:217`) read off the interface thread.** `git grep -n -E 'mRunningGame|GetRunningGame' $PIN -- es-app/src es-core/src` finds the readers `FileData.cpp:1295` (on the interface thread, in a posted task) and **`ProxyCards.cpp:410` and `:579`**. The thread of the latter two is read in group 4. A non-atomic pointer shared across threads is a data race, though only its null-ness is read. The atomic beside it (`sGamesStarted`, `:90`) is the tree's own pattern. **Delta:** the brief names the HTTP thread as a reader, and the grep finds none there.
- **Read, nothing further (upstream-carried, :1700-2680):**
  - the folder and child lists, `FindByPath`, the filename map;
  - `getCore`/`getEmulator`, which validate the `system.cfg` value against the systems table (`:1954-2031`), so `%CORE%`/`%EMULATOR%` in the command are table names or empty;
  - `isNetplaySupported`, the CRC/MD5/cheevos hashes, the P2K mapping (`convertP2kFile` writes `<rom>.keys` beside the ROM for the session and `launchGame` removes it, `:1092`, `:1171-1172`);
  - `getCurrentGameSetting`, the bindable properties, `parsePlayersRange`, `getBindableParent`.
- **FD-19 (Q3 seam lead, the same as FD-9):** `setSelectedGame` (`:2364-2373`) fires `game-selected` on every cursor move with the system name, the raw path and the scraped name, through the same `Scripting::executeScript`. It runs only when a script is in a `game-selected` directory. Recorded with FD-9.
- **FD-20 (Q6, Low, upstream-carried):** `FolderData::removeChild` asserts `false` after a successful removal under `DEBUG` (`:1888-1891`), so a debug build aborts on every removal. It is unreached in the shipped build, which is not `DEBUG`. It is a row.

### Group 1. `es-app/src/FileData.h` (293 lines)

- **FD-21 (Q6): `LaunchGameOptions` carries two fields nothing uses.** `isSaveStateInfoTemporary` (`FileData.h:58`, `:72`) is set in the constructor and read nowhere (`git grep -n isSaveStateInfoTemporary $PIN -- es-app/src es-core/src`: 2 hits, both the header). `netplayClientPassword` is read and never set (FD-1). `FileData::resetSettings` is static, empty, and called from `GuiCollectionSystemsOptions.cpp:346,358` and `GuiMenu.cpp:9144`. `netPlayMode` is an `int`, not the `NetPlayMode` enum (`:63`).

### Group 1. `es-app/src/views/ViewController.cpp` (1,531 lines) and `.h` (158)

**Provenance inside the file:** against `1750dded8` the fork's hunks are 2, 20, 39-44 (`configurationReplaced`), 72-79 (the `saveState` guard), 1059-1118 (`dropGameListView`/`remakeGameListView`, #246) and 1468-1496 (`forgetScreenshots`, the #300 note). That is 89 lines added and 0 removed; the rest is batocera's.

- **VC-1 (Q5/Q2, Medium, lead; least surprise): a launch the gates will refuse plays the whole launch transition and the game's splash first, then asks.** `launch` (`:533-671`) runs `checkLaunchOptions`, locks input, puts up the game's splash (`:586-587`) and starts the transition: `fast slide` 750 ms by default (`auto` → `fast slide`, `:596-597`), `slide` 1500, `fade` 800, `fast fade` 400. **Only at the animation's end** does `doLaunchGame` (`:476-488`) call `FileData::launchGame`, whose first act is the four gates (FD-8). A launch held by the capture, a sync, a transfer, the send or the top-up therefore shows the zoom into the game and its splash, then the question. The return animation then plays (`:626`, `:647`, 600 to 800 ms) under the box, with input locked until it ends. A STOP IT AND PLAY goes through `launchNow` → `ViewController::launch` again (FileData `:792`), so the full transition plays a second time. `time-to-play.md` (nothing on the launch path unless it must) and `least-surprise.md` (no screen implies what is not happening) are the rules. The question is asked after the screen has said the game is starting. The fix is to ask the gates' question before the transition, from `checkLaunchOptions`' position. Proof on the guest (queued): a frame series of a launch over a running transfer or a fixture sync, and the time from the press to the question.
- **VC-2 (Q5, Low, lead): every launch asks `ApiSystem::getIpAddress()` (`:571`)** to decide whether netplay is possible, and compares the result with the literal `"NOT CONNECTED"`. Its cost on the image is T21's to read (`ApiSystem.cpp`). It sits on the press-to-frame path even when netplay is off: the `||` checks `global.netplay` first, so with netplay off it short-circuits. **Correction while writing:** the call is skipped when `global.netplay` is off. It is a Q5 row only for a player with netplay on.
- **VC-3 (Q7, Low, upstream-carried):** `PowerSaverMode() == "instant"` is tested twice (`:593-594`, `:599-600`). The fade, slide and instant arms repeat the same end-callback body three times (`:615-629`, `:635-650`, `:654-669`).
- **VC-4 (fork hunk, read, correct):** `saveState` skips its write after `configurationReplaced()` (a factory reset or a settings restore), so a stale `Settings` map is not written back with `LastSystem` (`:72-79`; #308 F-ES-10). It writes `es_settings.cfg`, key `LastSystem` (`:92-93`), only when `StartupSystem` is `lastsystem`. `dropGameListView` and `remakeGameListView` (`:1059-1117`) are es-code-traps § A rescan that deletes FileData drops the view first, implemented: the cursor's path is read while the file is alive, and the view is dropped before the delete. Their callers are read in group 2.
- **VC-5 (Q3, Low, upstream-carried):** `reloadAll`'s theme pool increments a plain `int processedSystem` from every worker (`:1248-1267`), a data race that only feeds the splash's progress bar. `reloadAllGames` dereferences `getSelectedSystem()` without a null check (`:1437`). `getSelectedSystem` falls back to `mState.getSystem()`, which is null before any view has been chosen. With `deleteCurrentGui == false` the top GUI is removed and not deleted (`:1442-1447`), by upstream's design for the caller's own page.
- **VC-6 (Q2, Low, upstream-carried):** the splash strings `_("Preloading UI")`, `_("Loading theme")`, `_("Loading gamelists")` and `_("Loading...")` (`:1023`, `:1276`, `:1290`, `:1313`, `:1319`, `:1440`) are in sentence case where the fork writes capitals. They are upstream's and outside the fork's lanes (D-UI-079), so this is a row, not a change.
- **Read, nothing further (upstream-carried, :97-475, :673-1050, :1119-1460):** start, system and game-list navigation (`Scripting::fireEvent("system-selected", ...)` at `:212` with a system name, safe), view-type selection (`:700-846`; `getFilesRecursive` walks the whole system once to choose a view, upstream's cost), input (`mLockInput` during the launch, `:876`), render, preload, and `reloadGameListView` (`:1119-1184`; its callers are read in group 2 for es-code-traps § A rescan).

### Group 2. `es-app/src/SystemData.cpp` (2,583 lines) and `.h` (296)

**Provenance inside the file:** against `1750dded8` the fork's hunks are at 22-30 (includes), 111, 304-519 (`dropCollectionEntries`, `rescanIfFolderChanged`, `rescanChangedFolders`), 540-560, 626-633, 1098-1136 and 1301-1304 (280 lines added, 13 removed). The rest is batocera's.

- **SD-1 (fork code, read; correct by design): `rescanIfFolderChanged` (:378-512).** It runs only for game systems with **no gamelist** (`:382`, cached `exists`; the gamelist is written by ES itself, so the cache is right). It is one `stat` per system (`:385-387`). It is skipped while the hasher, the scraper or a game holds files, and leaves the time unrecorded so the next trigger retries (`:393-397`). It drops this system's view and its group's view before the delete (`:406-417`), merges a fresh tree so a kept file keeps its object (`:431-486`, `FolderMerge`), and drops collection entries before a vanished file is deleted (`dropCollectionEntries`, `:312-342`). The index is set aside while the fresh twins are deleted, so a twin's destructor does not take its kept file's count out (`:491-494`). Then the views are remade by path (`:506-511`). es-code-traps § A rescan that deletes FileData drops the view first is met. **Gap (FD-8):** pending launches hold a `FileData*` the merge's `vanished` can delete. No current trigger lands inside a wait; recorded at FD-8.
- **SD-2 (Q3, Low, lead): `populateFolder`'s two path filters match a substring anywhere in the path, not the folder's name.** `fileInfo.path.rfind("ports") != npos` (`:627`) and `rfind("windows")` (`:631`) are upstream's. On the image, a sub-folder of **any** system whose path contains `ports` or `windows` is skipped: `/storage/roms/snes/Sports/`, `.../Supports/`, `.../Imports/`, `/storage/roms/psx/Windows 95 era/`. Its games never appear. The comment says "Skip ports folders", meaning the `ports` system. The fix compares the system name (`mMetadata.name == "ports"`), as `:619` and `:623` do. Guest proof (queued): a fixture `/storage/roms/gb/Sports/<rom>.gb`, UPDATE GAMELISTS, then the game list read through the API (`/systems/gb/games`).
- **SD-3 (Q3, Low, upstream-carried; confirmed from the brief's lead): one unparseable `es_systems_*.cfg` overlay skips every later overlay.** `loadAdditionnalConfig` (`:1024-1095`) `return`s from the whole function on a parse failure (`:1039-1043`) or a missing `<systemList>` (`:1046-1050`). Every overlay later in the directory listing, and every overlay in the second root (`getEmulationStationPath()`), is then never read. The only report is an error log line. The player sees systems silently lose their per-emulator overrides. The distribution ships no overlay (`git ls-files | grep -E 'es_systems_[^/]*\.cfg$'` lists only a QA fixture), so this is reachable with a player's own or an add-on's overlay. The fix is `continue`. The function also re-runs, and re-reads every overlay, for each `loadSystem(name)` and `getKnownSystemNames()` call (`:1327`, `:1357`), which is Q5 at startup (`createGroupedSystems` calls `loadSystem` once per group, `:752`, and each re-parses `es_systems.cfg` from disk, `:1318`). Guest proof (queued): two overlays under `/storage/.config/emulationstation/`, the first malformed, the second changing a system's `<fullname>`, then the system list read through the API after a reload.
- **SD-4 (Q3, Low; FD-15 confirmed): `setSortId` stores any value, and `mSortId` is read from `es_settings.cfg` unbounded (`:86`, `:1937-1941`).** `getChildrenListToDisplay` then checks `> size()` where it needs `>= size()` (FileData `:1659`). A stored `<system>.sort` equal to the number of sort types throws `std::out_of_range` from `.at()` when that system's list is shown. On an upgrade, a build with more sort types than the next one leaves such a value behind. Under `upgrade-and-install.md`, that is what is already written: settings carried from a different build.
- **SD-5 (Q3, Low, upstream-carried): data races on progress counters.** `loadConfig`'s `processedSystem` (`:1217`, `:1223-1227`, `:1250-1254`) and `ViewController::reloadAll`'s (VC-5) are plain `int`s incremented from `ThreadPool` workers and read by the splash. Only the splash's progress is affected.
- **SD-6 (Q6/Q7, Low):** `getConfigPath` (`:1579-1594`) takes `es_systems_custom.cfg` as **the** configuration, a replacement, and `loadAdditionnalConfig` also merges every `es_systems_*.cfg`, the custom file included, so a custom configuration is merged onto itself. That is harmless, and a reader stumbles. The last fallback is `/etc/emulationstation/es_systems.cfg` ("Backward compatibility with Retropie"). On the image it is the link #613 is about, reached only when both user-path files are absent. The ES side is upstream's order; the link is the recipe's (T37). The commented-out symlink check (`:526-538`), the commented-out `loadFeatures()` (`:1285-1286`) and the old count code (`:1814-1820`) are dead text.
- **SD-7 (fork code, read, correct):** `startIndexesAtStart` (`:1098-1135`) retries the cheevos-only index at most once in ten minutes, with function-local statics read and written only on the interface thread (its callers: `loadConfig`, `main`, the network watcher's post; to confirm in group 5). The `#300` note in `ViewController.cpp:1487-1495` and the single start in `loadConfig` (`:1303-1304`) agree.
- **Read, nothing further (upstream-carried):** the constructor and destructor, `removeMultiDiskContent` (the multidisk cache in metadata), `createGroupedSystems`, the features, the emulator and core choice (`getEmulator`/`getCore` validate `system.cfg` against the table, `:2132-2176`), `getLaunchCommand`'s precedence of core over emulator over system (`:2219-2235`, as the brief says), the counts, the theme variables (`loadTheme` puts the RetroAchievements username and netplay nick in theme variables, `:1851`, `:1854`, for themes that show them, by upstream's design), the bindable properties and the header. **Q1 (Renovation, upstream-carried):** raw owning pointers (`mEnvData`, `mRootFolder`, `mGameCountInfo`, `mSaveRepository`, `mFilterIndex`, `mBindableRandom`) with manual `delete` in the destructor (`:158-177`), and `new SystemDataPtr[systemCount]` (`:1210`). They are recorded and not proposed: merge friction against batocera.

### Group 3. `es-app/src/SaveState.cpp` (240 lines, fork-own; 82 lines changed against `1750dded8`) and `SaveState.h` (60, upstream-carried: `git diff --quiet 1750dded8 $PIN -- es-app/src/SaveState.h` exit 0)

The shipped path: `es_savestates.cfg` is linked into `/storage/.config/emulationstation/` on first boot and after every update (the distribution's `ui/emulationstation/config/common/es_savestates.cfg`, its header comment), so `config != nullptr` and **`racommands == false`**. The interface hands the launcher `-state_slot N -state_file <file>` and parks nothing.

- **SS-1 (Q3/Q2, Low, lead → bug candidate; on the shipped path): the state file's path is spliced into the command inside double quotes, unescaped.** `-autosave 1 -state_file "<fileName>"` (`:77`) and `-state_slot N -state_file "<fileName>"` (`:97`, `:111`). The file name is built from `{{romfilename}}` (the shipped `es_savestates.cfg`: `file="{{romfilename}}.state{{slot}}"`), so a ROM whose name holds `"`, `$`, a backtick or `\` breaks the command or expands inside it. On the image the shell runs this line through `Platform.cpp`'s `system()` wrapper (T35's). `%ROM%` beside it goes through `getEscapedPath` (FileData `:618`). `Utils::String::shellQuote` is the tree's form (`FileData.cpp:1148-1151`, `:678`). `es-player-text`/`es-ui-style-guide` do not govern this; the rule is brief § 4 Q2's: `shellQuote` on every command built from a path or a name. Reach: a RetroArch game launched from a save state, or with AUTO SAVE on (the Auto slot, `:72-77`), whose ROM name carries one of those characters. `$` is the plausible one in a real library. What happens on the launcher's side once the shell has split it is T1's (`runemu.sh`'s `parse_savestate_arguments`, #730's seam). Guest proof (queued): a fixture ROM `Test $HOME.gb` under `/storage/roms/gb/`, one save state made, then a launch from it. Read the argv `runemu.sh` received from `/var/log/exec.log` (D-LAUNCH-004: one launch's log) and look for `$HOME` expanded.
- **SS-2 (Q6): the `racommands` arms are reached only without `es_savestates.cfg`** (`:74-75`, `:87-93`, `:101-107`, `:114-158`, `:166-190`): the built-in layout's park-and-restore of `.state.auto` and the next-slot copy. On the image the file is linked on first boot and after every update, so these arms run only on a device whose link is missing. The header comment of `es_savestates.cfg` says without it "the pre-launch auto save at exit [is restored] and loses the quit state". That makes the fallback a lossy path, kept for the merge with batocera (D-UI-057's patch is in it). Q6 row: unreached on a healthy image, reachable after a lost link. `Already written:` a `.bak` beside an auto state is what this arm leaves if a session is killed between `:121` and `:182`. Group 3's repository read checks whether anything reads or cleans a stale `.bak`.
- **SS-3 (Q7, Low): duplicated arms.** For `racommands == false` the `incrementalSaveStates` and non-incremental branches emit the same text (`:95-97` and `:109-111`). The fork's comment at `:42-46` names `runemu.sh:23-26` for `--core=`. That is T1's file, where #730 is open on those lines.
- **SS-4 (Q3, Low, upstream-carried): `copyToSlot` returns `true` without checking its rename or copy** (`:213-239`). A failed move reports success to its caller (`GuiSaveState`, T31's). `remove()` ignores `removeFile`'s result too (`:201-211`). The callers are T31's to grade. Recorded as `engineering-practices.md` § Verify the artifact.
- **FD-13 confirmed:** `onGameEnded` says, and does, **no renumbering** (`:192-198`, D-UI-069). `FileData.cpp:1134-1135`'s "renumbers slot files" is wrong. Q7, Low: a comment fix.
- **SaveState.h (upstream-carried, Q6/Q4 first):** byte-identical to batocera's merge base. It declares a `virtual` member in a struct with no virtual destructor, and nothing derives from `SaveState` (`git grep -n ': public SaveState\|: SaveState' $PIN -- es-app/src` is to be run in Phase 3.6). Reached: every declared member is used by the repository or `FileData`.

### Group 3. `es-app/src/SaveStateRepository.cpp` (342) and `.h` (53), fork-own (34 lines changed against `1750dded8`)

- **SR-1 (Q6): `SaveStateRepository::renumberSlots` (`:251-277`, declared `.h:21`) has no caller.** `git grep -n renumberSlots $PIN -- es-app/src es-core/src` finds the definition and the declaration only. batocera's `SaveState.cpp` at `1750dded8` calls it (`git show 1750dded8:es-app/src/SaveState.cpp | grep -c renumberSlots` = 1). The fork removed the call under D-UI-069 (no renumbering after a session; `SaveState.cpp:192-198` says why). So it is a retired mechanism still carried, and the brief's Q6 candidate is confirmed. `Already written:` nothing. The function renames slot files when called, and it has not been called since D-UI-069, so no device holds anything it left that this code reads. A removal guards and stamps nothing. **What it exposed:** a call would rename every slot above a gap, which the save sync reads as a deletion plus a new file. That is exactly what D-UI-069 stopped. Removal or a comment naming D-UI-069 is the stream brief's to decide (merge cost against batocera, D-WORKFLOW-185's shape).
- **SR-2 (Q5, Low, to measure): every game exit re-reads the system's whole save-state directory on the interface thread.** `FileData.cpp:1120` calls `refresh()` (`:62-129`): `clear()` deletes every state object, then one `getDirectoryFiles` per config directory, then per file a `std::regex_match` against the slot and the auto patterns, one or two `exists()` for its screenshot, and one `stat` for its time. This sits between the emulator's exit and the interface's next frame (time to play's second number). For a system with hundreds of states it is a measurable cost. The guest measurement (queued) is a fixture of N states under `/storage/roms/savestates/gb/`, with `time-to-play`'s exit cell at N = 0 and N = 500. It is on the RetroArch half of #336's line, so a Q5 finding confined here is `deferred:#336` unless the stream brief says otherwise.
- **SR-3 (Q3, Low): the shared state objects are allocated once and never freed.** `_empty` (`:19`, static), `_autosave` and `_newGame` (`:280-294`, per repository; the destructor's `clear()` does not delete them, `:30-42`). There is one leak per system per process, a few bytes each, and nothing reads freed memory. This is a Q1/Q3 row. `isEnabled` (`:211-228`) is true only for the `retroarch` emulator name, which is the #336 line (§ Scope).
- **Read, correct:** `onDisk`/`anyOnDisk` stat uncached (`exists(path, false)`, `:142-150`; fork #205). That is es-native-ui § Core patterns' rule for files another thread writes, and it is met. `getGameAutoSave` (`:301-342`) hands back a live repository object, which `rememberSaveState` records by file before a gate can wait (FD-8's context).

### Group 3. `es-app/src/SaveStateConfigFile.cpp` (337) and `.h` (86), upstream-carried (byte-identical to `1750dded8`)

Q6 and Q4 first (brief § 4): every function is reached. `getSaveStateConfigs` is called from the repository, `SaveState` and `GuiSaveState`, and `isEnabled` from `getSaveStateConfigs`. Q4: batocera has no commit on either file since the merge base (`04-analysis.md` § Q4 lists the seven batocera commits on the twenty, and none is on these two; to confirm there).

- **SC-1 (Q3, Low, upstream-carried): the configs cache is a static map read and written without a lock, and it outlives the systems it describes.** `_cache` (`:271-337`) is keyed by system name and filled on first use. `Instance()` is behind `mLock` (`:133-141`), and `_cache` and `SaveStateConfig::Default()`'s `_default` (`:27-49`) are not. Every caller found runs on the interface thread: the repository's `refresh` from `launchGame` and the manager. The bookkeeper's worker never calls in (it holds paths only, `SaveStateBookkeeper.h:33-35`). So there is no race today, and the hazard is latent. The cache is never cleared, so after `ViewController::reloadAllGames` (new `SystemData`, possibly a changed `es_systems` overlay with other emulators) a system keeps the configs computed for its old emulator list. That is reachable after UPDATE GAMELISTS with a changed systems file, without a restart. It is a Q3 row, not proved; the guest proof would be an overlay that removes `retroarch` from a system, a reload, and the manager's tiles.
- **Read, nothing further:** the regex built from the file pattern (`:63-89`, `.` and `\` escaped; the pattern is the shipped config's, so other metacharacters in it would be the config's own), `matchSlotFile`/`matchAutoFile`, `isDefaultConfig`/`isActiveConfig`, and the XML reader. `es_savestates.cfg` is read from the user path, then the ES path (`:188-191`), with `exists()` cached once at first use; the link is made by first boot and post-update (distribution side).

### Group 3. `es-app/src/SaveStateJobQueue.cpp` (62) and `.h` (72), fork-own, pure

- **Read, correct; the four rules the header states hold in the code:** one job at a time (`take` refuses while `mRunning`, `:37-38`); a pending deletion is never queued twice (`:7-8`); a copy hides nothing (no `mPending` insert for a copy, `:19-33`); `finish` counts either kind (`:47-57`). Tested by `es-app/tests/unit/SaveStateJobQueueTests.cpp` (to run, queued). No findings.

### Group 3. `es-app/src/SaveStateBookkeeper.cpp` (344) and `.h` (71), fork-own

- **SB-1 (fork code, read; correct on the order of act and lock):** `runDelete` asks `isFlockHeld` (it fails closed), waits for the transfer, then takes the lock **exclusive and non-blocking** with `O_CLOEXEC` (`:116-151`, `:153-173`), so the question and the act are one (E2's fix). The retire runs with every argument `shellQuote`d (`:182-186`), and the unlink falls back when the script is absent or failed (`:194-197`). The log line reports what is on disk (`:199-205`, `engineering-practices.md` § Verify the artifact). `shutdown` drains, then joins (`:332-344`; it is called from `main.cpp`, read in group 5).
- **SB-2 (Q3, Low): a lock file that cannot be opened makes the worker spin at five hertz for the session, and the tile stays hidden.** If `open(CLOUD_SYNC_LOCK_PATH, O_RDWR|O_CREAT)` fails (`:124-126`: `/var/run` read-only, out of descriptors), `take()` is false every time. `transferGone` answers true (`isFlockHeld` finds no holder), so the loop at `:159-173` sleeps 200 ms and retries until `stop`. The deletion the player confirmed never happens, and its tile stays hidden (`isPending`) until exit. Nothing on the screen says so, which is `engineering-practices.md` § Fail gracefully's "silence is the worst failure". It fails closed (no unlink under a possible transfer), which is right. The gap is the missing bound and the missing word. Guest proof: not without making `/var/run` unwritable on the guest, which is possible under a mount namespace. A lead.
- **SB-3 (Q3, Low, lead for T16): `shutdown()` joins a worker that may sit in `executeScriptLegacy` on an unbounded `cloud_capture`** (`:186`, `:229`). The exit's five-second bound applies to waiting for the transfer lock (`:92-101`), not to the script. `cloud_capture --retire` ignores SIGTERM while it runs, by design (`.h:13-17`, D-CLOUD-133). A hung script would hold the interface's exit, and then the supervisor's stop. That bound is the script's (T16, #663), and it is posted as a seam lead.
- **Q1 (the tree's own pattern):** the worker is a leaked `new Worker` by design, so no static `std::thread` is destroyed at teardown (`:31-45`). The comment says why. No finding.

### Group 4. `es-app/src/ProxyCards.cpp` (596) and `.h` (58), fork-own (23 fork commits; read whole)

- **FD-18 confirmed (Q3/Q1, Low): `FileData::mRunningGame` is read on worker threads.** The top-up watcher's thread reads it in `screenFree` (`:269`), `waitForTheGame` (`:410`, `:416`), and the probe's detached thread (`:479`, `:500`, `:503`). The interface thread writes it at `FileData.cpp:1094` and `:1111`. A plain static pointer read and written concurrently is a data race (undefined behaviour), even though only its null-ness is compared. The fix is `std::atomic<FileData*>` behind the same `GetRunningGame()` (the tree's pattern: `sGamesStarted` beside it, `FileData.cpp:90`). No player-visible failure is known, so this is a Q3 row with a Q1 fix. A guest proof is not meaningful (a race in the abstract machine); the evidence is the reading plus ThreadSanitizer, if the unit build can host it (a lead).
- **PC-1 (Q3, Low, lead for T35 `Window`): the send and top-up workers touch their card directly after sleeps of up to 45 + 10 + 5 s and 90 + 5 s** (`runSend` `:125-190`; `runTopUp` `:381-389`; `offlineIndexCard`'s detached closer `:218-222`). They are detached threads holding raw `AsyncNotificationComponent*`, and `card->close()` is their last act. `AppWindow::post` stops posting once `main()` lets the window go (`5443b5301`), but these calls are not posts. If the interface exits (QUIT, the supervisor's stop) while a card's worker sleeps, the worker calls into a card the window may already have freed. That depends on `Window`'s teardown of its async notifications (T35's) and on `main.cpp`'s exit order (group 5). Recorded here and checked against `main.cpp`'s shutdown. The existing pattern (`ThreadedBluetooth`, the sync card) shares the shape, so a finding would be the tree's.
- **PC-2 (Q3, Low): `SystemConf` is read on worker threads** (`savesOwed`, `:102-109`, from the probe's thread `:472`; `OfflineAchievements::toggleOn` and friends, T20's). Whether `SystemConf::get` is safe off the interface thread is T21's (`SystemConf.cpp`). A seam lead.
- **Read, correct (fork logic):**
  - One top-up watcher at a time, with requests kept as bits (`:48-49`, `:420-456`, `:558-566`; PL-056). The exchange-then-store race at the watcher's exit is handled (`:437-443`).
  - The stop's hold is a deadline plus a games-started count, so a game that came and went releases it (`:73-74`, `:404-418`, `:573-586`).
  - Saves first, then the batch (`:465-521`, `:529-551`; #305, D-UI-101/D-UI-109).
  - The send card takes the proxy's flush stamp, waiting up to 10 s (`:139-147`).
  - The outcome words match the vocabulary: COMPLETED, COULDN'T FINISH - <why>, SKIPPED - YOU STARTED A GAME (D-UI-028/D-UI-030, `es-player-text.md` § Outcome vocabulary). The line does not repeat the title (D-UI-107).
  - One floating surface: the send card waits for a sync card and a game (`:499-504`, `:509-513`; D-UI-093).
  - The French for every string is counted by `es-untranslated` (0 without, at the pin).
- **Q5:** the probe and watcher poll at 1 Hz and 2 Hz while they wait (`:129-134`, `:271-287`, `:479-481`, `:500-502`), off the interface thread and bounded (45 s, 10 s, 90 s, 120 s). They are not on the launch path: the gates ask `sendRunning`/`topUpRunning`, which are atomics and a stat.
- **Q7 (Low):** the comments carry the audit trail (`PL-056`, `G2-E-app-05`, `G-E2-04`, `F-RA-09`...) as much as the intent. A reader new to the file meets five audit identifiers before the rule they produced. The rules are there and right; the history could live in the commits. A Q7 row, not a defect.

### Group 5. `es-app/src/main.cpp` (1,368 lines, fork-own; 42 fork commits; read whole)

**Provenance inside the file:** against `1750dded8` the fork's hunks are 6-10, 37-63, 349-353, 378-447 (the fault and interrupt handlers), 523-693 (the boot game's capture, the startup sync), 707-730, 862-870, 917-1118 (the boot prompts, the startup sync's start), 1162-1172 and 1319-1333 (498 lines added, 18 removed). The rest is batocera's.

How the image starts it: `emulationstation --log-path /var/log --no-splash` (the distribution's `ui/emulationstation/sources/start_es.sh:8`, under `essway.service`).

- **MN-1 (Q6, Low): the image passes a flag the binary does not read.** `--log-path /var/log` is not in `parseArgs` (`:75-298`). `git -C $W grep -n -i 'log-path' $PIN` finds nothing, and the log goes where `Paths::getLogPath()` says (`es-core/src/Log.cpp:258`), which on the image is `/var/log` as well (`handheld-evidence.md`: `/var/log/es_log.txt`). `parseArgs` ignores an unknown argument silently, so the flag and its value pass as nothing. It is harmless today, because the default agrees, and a reader of the start script believes the flag decides the path. The fix is the start script's (T37's recipe, `package.mk:89` copies it) or a parsed flag here. `--no-splash` is read (`:192-194`) and is why `startIndexesAtStart` runs from `main` (`:862-870`, fork #183).
- **MN-2 (Q3, Low, upstream-carried): four flags read `argv[i + 1]` without a bound check.** `--videoduration` (`:98-101`), `--video` (`:103-106`) and `--vsync` (`:220-224`; `strcmp` on `NULL`) do this, and `--max-vram` (`:225-229`) also never skips its value. Each, given as the last argument, reads `argv[argc]` (`NULL`): `atoi(NULL)` and `strcmp(NULL, ...)` crash at start. The image passes none of them (MN-1). Reachable only by hand, so it is a Q3 row; the fix is `if (i >= argc - 1)` as the neighbouring flags do.
- **MN-3 (Q3, Low): the boot game replays a frozen command.** `launchStartupGame` (`:527-572`) runs `global.bootgame.cmd` from `system.cfg` (stored by `GuiMenu.cpp:11325` as `getlaunchCommand(false)` when the player chose the game), with only `%CONTROLLERSCONFIG%` re-substituted. It has no gates (none can apply: nothing else runs yet), no `game-start`/`game-end` events, no `mRunningGame`, no save-state refresh, no play count and no exit sync. The capture runs, with `launchToken`/`launchArgument` reading the stored line. The stored command also carries what `getlaunchCommand` baked in when it was stored: the emulator and core of that day, a `-state_file` path when a save state or AUTO SAVE was on (SS-1's shape), and the netplay arguments. A player who later changes that game's core still boots the old one, and a stored `-state_file` that has since been deleted is passed as it was. The brief's lead is confirmed by reading. Guest proof (queued): set a boot game, change its core in `system.cfg`, reboot, and read the core that ran from `/var/log/exec.log`. `Already written:` every device with a boot game holds a stored command in `system.cfg` (`global.bootgame.cmd`), and any fix must read the old shape or rebuild it at boot.
- **MN-4 (Q7, Low): two comments describe superseded behaviour (`decision-register.md` § A reversal sweeps its old words).** First, `:615-621` says "A game launched while this sync runs cancels it in whatever phase it is in ... and goes ahead (#101 ...)". D-CLOUD-130 replaced that with a question (`FileData.cpp:947-950` says so, "since 2026-09-16 (D-CLOUD-130) it asks first"). Second, `:592-596` names the card's line `SKIPPED - NO NETWORK CONNECTION`, which D-UI-031 reworded to `SKIPPED - YOU'RE NOT ONLINE` (`es-player-text.md` § Outcome vocabulary). There is also `:1110-1114`, "would turn the player's YES into 'Another cloud sync is already running. Skipped.' in a console": the continuation has been the transfer page since #114 (`:999-1002`). `tools/archaeology --reversal` is the sweep the rule names, and it is run in Phase 3.6.
- **MN-5 (Q2, Low): three player-visible boxes bypass `_()`, so they have no French and are not counted by `es-untranslated`.** The serial-number warning `"pixelelated IS FREE SOFTWARE.\n\n IF YOU PAID ..."` (`:929`; mis-indented under its `if`, with leading spaces after each `\n\n`). The two systems-configuration errors (`:328-329`, `:336-339`), shown through `GuiMsgBox` at `:860`, which point the player to `EMULATIONSTATION.ORG` and say "YOU'LL NEED TO DO THIS BY HAND, UNFORTUNATELY". D-UI-051 says every fork string ships in English and French. The serial box is a fork string (the rename, D-WORKFLOW-144); the two config errors are upstream's, on a box the image shows when `es_systems.cfg` is broken (D-UI-079 decides whether their words are this fork's to change; recorded for the coordinator). `tools/es-untranslated` cannot see a string outside `_()`, which is a gap in the checker. That is a lead for the tooling slice: `es-untranslated` counts only `_()`.
- **MN-6 (Q2, Low): the legacy journey prompt uses a verb outside the vocabulary.** `:980` reads `"YOUR SETTINGS WERE RESTORED.\n\nDOWNLOAD YOUR GAMES, BIOS FILES, AND SAVES FROM THE CLOUD NOW?"` (an earlier build's marker with no tier record). D-UI-022 allows only *back up* and *restore*, and the tiers are *ROMs and BIOS*, not *games*. Its seven siblings (`:982-994`) say RESTORE ... and are right. `tools/vocabulary-check` judges only back up/backup, save state and Wi-Fi, so it passes this. Reach: a device updated from a build that wrote the marker without the record, mid-restore.
- **MN-7 (fork code, read, correct):**
  - The fault handler (`:380-428`) uses only `write(2)` and `backtrace_symbols_fd`, then re-raises with the default action. It is installed with `SA_RESETHAND | SA_NODEFER` (`:710-719`), and the unwinder is warmed (`:721-729`).
  - SIGINT sets a flag the loop reads (`:442-447`, `:1166-1171`).
  - SIGTERM keeps its default action on purpose (`:730` commented, `:1323-1324`, D-CLOUD-133). On the image `essway` stops the unit with SIGTERM, so a stop skips `main`'s tail: the bookkeeper's join, `ViewController::saveState` (`LastSystem`) and `deleteSystems`' gamelist save on exit. Recorded as the consequence of a decided row, not re-argued. The SIGTERM handler commented out at `:730` is the brief's Q6 candidate: a row, decided.
  - The boot prompts are ordered with the marker consumed on the choice, not on display (`:934-1031`).
  - The recovered-settings box, the interrupted-restore box (uncached `exists`, consumed on OK), the RetroAchievements re-entry offer and the READY flag follow (`:1041-1100`).
  - The startup sync starts after READY and not after a one-touch restore (`:1117-1118`).
  - The exit: `AppWindow::closing()` before any teardown, then the scan worker, the watchers, the hasher, the scraper, the bookkeeper's join, `saveState`, `deleteSystems`, `window.deinit`, and `processQuitMode` (`:1319-1366`).
- **PC-1, re-read against the exit:** `AppWindow::closing()` stops posts (`:1322`), and `window.deinit()` runs at `:1358`. The ProxyCards and `ThreadedCloudSync` workers are detached and are not stopped or joined anywhere in the exit. A card worker in its 5-second outcome sleep then calls `card->close()` on a card the deinit has taken down, or the process returns from `main` with the thread still running. That is exit-time only and the tree's shape (the sync card too). Q3 Low, a lead for T35/T18.
- **Q5 (startup, to measure):** `launchStartupGame` runs before the window (`:799-802`). `serial_number_check` runs through `runSystemCommand` with a splash at every boot (`:918`). Then `preload` and the index start. The startup card's network wait is bounded at 60 s by `cloud_net_ready --wait 60` (`:666-667`; D-CLOUD-112's offline benchmark is the exit sync's, not this one).

## Coverage table: one row per path (20)

Every path was read line by line at the pin. The cells name the findings above, and `04-analysis.md` § Renovation face carries each question across the slice. "Clean" means read with the question in hand and nothing found.

| Path | Group | Tier | Q1 Modernize | Q2 Standards | Q3 Bugs | Q4 Currency | Q5 Efficiency | Q6 Dead ends | Q7 Clarity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `es-app/src/FileData.cpp` | 1 | fork-own (~1/5 fork lines) | FD-17 raw owning `mDisplayName`, C casts (upstream lines; recorded) | FD-10, FD-11, FD-12 | FD-1, FD-2, FD-3, FD-8, FD-14, FD-15, FD-18 | `d17cf003e` (batocera, to merge) | FD-6; the launch and exit costs itemised (Phase 2 Q5 list) | FD-1, FD-5, FD-16, FD-20, FD-21; Q6 table | FD-4, FD-13, FD-16; no provenance header |
| `es-app/src/FileData.h` | 1 | fork-own | `netPlayMode` an `int` (FD-21); raw `mParent`/`mSystem` pointers by design (non-owning) | clean | FD-18 (`mRunningGame`) | no batocera commit | n/a: declarations | FD-21 (`isSaveStateInfoTemporary`, `netplayClientPassword`); `isVirtualFolderDisplayEnabled` unreached | clean (the fork's `LaunchGameOptions` comments say why) |
| `es-app/src/views/ViewController.cpp` | 1 | fork-own (89 fork lines) | upstream's callbacks repeated three times (VC-3) | VC-6 | VC-5 | `308221458`, `5f106acce`, `0806a0c5c` (to merge) | VC-1, VC-2 | `#ifdef _RPI_` and WIN32 arms (Q6 table) | VC-3 |
| `es-app/src/views/ViewController.h` | 1 | fork-own | clean | clean | clean | `308221458` changes `launch`'s signature (to merge) | n/a: declarations | `hasInstance` reached; Q6 table | clean (`dropGameListView` is documented in place) |
| `es-app/src/LaunchCommand.h` | 1 | fork-own | the duplicated reader beside `runemu.sh` (seam, § 3.5) | clean | LC-1 (raw words, unreached) | no batocera commit (fork file) | n/a: a word scan per launch | both functions reached (`FileData.cpp:719-720`, `main.cpp:551-559`) | clean (its header states the divergence) |
| `es-app/src/SystemData.cpp` | 2 | fork-own (280 fork lines) | raw owning members (recorded) | clean | SD-2, SD-3, SD-4 (FD-15), SD-5 | `13e21d420`/`195a517ef`, `b69fb143c` (to merge) | SD-3 (config re-parsed per `loadSystem(name)`) | SD-6 (dead text); `hasGamelist` unreached | SD-6 |
| `es-app/src/SystemData.h` | 2 | fork-own | clean | clean | clean | `b69fb143c` touches it | n/a | `setIndex` unreached | clean |
| `es-app/src/SaveState.cpp` | 3 | fork-own | the `racommands` fallback (SS-2) | SS-1 (`shellQuote`) | SS-1, SS-4 | no batocera commit | n/a: string building | SS-2 | SS-3, FD-13 |
| `es-app/src/SaveState.h` | 3 | upstream-carried (identical to `1750dded8`) | `virtual` in a struct, no virtual destructor, nothing derives (recorded) | n/a: upstream-identical declarations | clean | Q4 first: no batocera commit since the base | n/a | Q6 first: every member reached (Q6 table) | n/a: upstream's, unchanged |
| `es-app/src/SaveStateRepository.cpp` | 3 | fork-own | clean | clean | SR-3 | no batocera commit | SR-2 (refresh on every exit) | SR-1 (`renumberSlots`) | clean |
| `es-app/src/SaveStateRepository.h` | 3 | fork-own | clean | clean | clean | no batocera commit | n/a | SR-1 | clean |
| `es-app/src/SaveStateConfigFile.cpp` | 3 | upstream-carried | n/a: upstream's; kept for the merge | n/a: upstream's | SC-1 (unlocked static cache, never cleared) | Q4 first: no batocera commit since the base | n/a: one parse per process | Q6 first: `isDefaultConfig` unreached; the rest reached | n/a: upstream's |
| `es-app/src/SaveStateConfigFile.h` | 3 | upstream-carried | n/a | n/a | clean | Q4 first: none | n/a | Q6 first: `isDefaultConfig` declared, unreached | n/a |
| `es-app/src/SaveStateJobQueue.cpp` | 3 | fork-own (pure) | clean | clean | clean | n/a: fork file | n/a | all reached (the bookkeeper) | clean |
| `es-app/src/SaveStateJobQueue.h` | 3 | fork-own | clean | clean | clean | n/a: fork file | n/a | all reached | clean (its rules in the header) |
| `es-app/src/SaveStateBookkeeper.cpp` | 3 | fork-own | clean (the leaked worker is deliberate, commented) | clean (`shellQuote` on every argument) | SB-2, SB-3 | n/a: fork file | n/a: off the interface thread | all reached | clean |
| `es-app/src/SaveStateBookkeeper.h` | 3 | fork-own | clean | clean | clean | n/a | n/a | all reached (`recordCopy` by hand) | clean |
| `es-app/src/ProxyCards.cpp` | 4 | fork-own | FD-18's fix (`std::atomic<FileData*>`) | clean (words, French counted) | PC-1, PC-2 | n/a: fork file | bounded polls off-thread (Q5 note) | all reached | Q7 note (audit IDs over intent) |
| `es-app/src/ProxyCards.h` | 4 | fork-own | clean | clean | clean | n/a | n/a | all reached | clean |
| `es-app/src/main.cpp` | 5 | fork-own (498 fork lines) | clean | MN-5, MN-6 | MN-2, MN-3, PC-1 (the exit) | no batocera commit on it | startup items (Q5 note) | MN-1; WIN32/BATOCERA/KODI/FREEIMAGE arms (Q6 table) | MN-4 |

## Guest proofs

None has run yet: the host is handed to M7 until its `resource return` (brief § 5). Each proof below is queued, in `00-running-log.md`'s queue and in the finding it would prove. A proof's row gets its `proved:` cell (`pin-binary`, `fix-unit-test` or `fix-walk-pending-image`) when it runs, and none is counted before then.

Can this be done on the VM? **Yes** for every behaviour claim above about the binary: the image carries the pin. **No** for: a netplay join (FD-1, it needs a host), a real pad's name in the controllers blob (FD-7), and anything only a race shows (FD-18). Those stay leads.

## Criterion entries: #649's checklist (= brief § 7), evaluated at the end of Phase 2 (17:47 UTC)

### AC-01: the audit folder holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`
**Verdict:** PARTIAL ⚠. Evidence: `ls docs/audits/2026_10_23-epic-m6-es-launch-path/` lists `00`, `01` and `02` at this entry. `03` to `05` follow in Phases 3 to 5. Refutation: n/a while in progress.

### AC-02: `tools/lint-audit-artifacts` prints PASS (pre-issue before stage D; resolution at close), the renovation face included
**Verdict:** UNTESTABLE ?. The lint runs once `04-analysis.md` exists (stage C to D).

### AC-03: `review-plan.json` records Extended depth and two reviewers from two other labs, each provenance naming its served model
**Verdict:** UNTESTABLE ?. Phase 4.6 waits for the `npm install`, which waits for the host's return line (brief § 1).

### AC-04: every punch item at a Phase 7 outcome
**Verdict:** UNTESTABLE ?. That is stage F.

### AC-05: `reviewed-at:`, `fixed-at:`, `fixed-at-es:` on #649
**Verdict:** PARTIAL ⚠. `reviewed-at` is recorded (`00-running-log.md` header: distribution `f4e0f0a196`, ES pin `16dbac5211`). It is written into #649's body at the hand-back.

### AC-06: § Scope records the pin, the two counting commands with output, both upstream refs with hashes and merge bases, the BUILD_ID, the M7 ES branches touching a slice file, and the #336 line
**Verdict:** PARTIAL ⚠. Evidence: `01-research-notes.md` § Scope holds the pin, both counting commands with their output (20, 11,287, 17, 3; no delta), `rocknix/master` `f6c542872` (delta noted) with merge base `cada856d8`, `batocera/master` `b2ceb55a7` with merge base `1750dded8`, the branch scan (no `m7-*` branch touches the twenty), and the #336 line. **Gap:** the image's BUILD_ID is read from the guest, which is queued.

### AC-07: a coverage table with exactly one row per path, `grep -c` printing 20, every Q1-Q7 cell answered or `n/a` with a reason
**Verdict:** PASS ✓. Evidence: ``grep -c '^| `es-app/src/' 02-forward-audit.md`` prints 20 (run 17:46). Refutation: every cell was read for an empty or bare `n/a`, and none is bare; each `n/a` gives its reason (declarations, upstream-identical, a fork file with no upstream).

### AC-08: each named check recorded with command, exit status and summary line; a check that could not run recorded with its reason
**Verdict:** PARTIAL ⚠. Four of fourteen ran (the table at the top). The unit tests, `tests/app-unit`'s three targets, the three python harnesses, `time-to-play` and `es-launch-memory` are recorded as queued for the host's return. No `.cpp` has been edited yet, so no syntax compile is owed yet.

### AC-09: Q5 carries the two time-to-play numbers beside #336's baseline (1.05 s, 2.03 s), the guest's loglevel, and `es-launch-memory`'s per-cycle table
**Verdict:** UNTESTABLE ?. These are guest measurements, queued.

### AC-10: Q6 carries one reachability row per entry point and per `#if`/`#else`/`#elif` line, with the commands' counts and the final count; every unreached row carries `Already written:` and what it exposed
**Verdict:** PASS ✓ for the table; it lands in `04-analysis.md` § Q6 in Phase 4. Evidence: `q6-reachability.py` → `q6-table.md`, 370 rows (295 + 13 + 62). The brief's commands' counts (154, 32, 60) are recorded beside it with the reasons they differ. Each of the five unreached rows carries `Already written:` and what it exposed (generator in `q6-table.md`). Refutation: each zero was checked by hand with `git grep -w` over `es-app/src es-core/src es-app/tests`; one zero (`recordCopy`) was wrong and corrected.

### AC-11: Q4 records `rocknix/master`'s zero commits since `cada856d8` with its command, and lists every commit of `1750dded8..batocera/master` (7) with a disposition each
**Verdict:** PASS ✓, carried into `04-analysis.md` § Q4. Evidence: `git rev-list --count cada856d8..rocknix/master -- <20>` = 0; seven commits, each with an `apply --check` result (`00-running-log.md` 17:43).

### AC-12: every guest proof carries a `proved:` cell; their count equals the running log's guest proofs
**Verdict:** UNTESTABLE ?. No guest proof has run; both counts are 0 now.

### AC-13: syntax compile and unit-test lines precede every ES `.cpp` commit; the coordinator re-runs; French beside every new string; `es-menu-map-check` still `0 missing`
**Verdict:** UNTESTABLE ?. There are no ES commits yet (stage E).

### AC-14: every `tracked:` punch item has its bug issue with the VM line and a VM-verifiable criterion; every `removal: yes` item has `Already written:`; `box-check` passes on each issue
**Verdict:** UNTESTABLE ?. That is stage D.

### AC-15: the retro exists, is posted on #649, and answers what the slice did to the two numbers
**Verdict:** UNTESTABLE ?. That is stage G.

### AC-16: the five distribution checkers and the ES `pre-push-test` pass before the merges, exit codes on #649
**Verdict:** UNTESTABLE ?. They run at the hand-back.

## Forward Audit Summary

| Verdict | Count | Criteria |
| --- | ---: | --- |
| PASS ✓ | 3 | AC-07, AC-10, AC-11 |
| PARTIAL ⚠ | 4 | AC-01, AC-05, AC-06, AC-08 |
| FAIL ✗ | 0 | |
| SKIP ○ | 0 | |
| UNTESTABLE ? | 9 | AC-02, AC-03, AC-04, AC-09, AC-12 to AC-16 (later stages, or the host's return) |

**Overall Assessment:** PASS WITH FINDINGS for the read (Phase 2's substance): 20 of 20 paths read, with the findings above. The checklist's runtime and later-stage criteria are open by construction at this point.

## Coverage Boundary

**Examined:** all 20 paths, line by line, at the pin, by reading (`git show $PIN:<path>` through `awk`). Context reads outside the slice, each named where used: `es-core/src/Scripting.cpp` (FD-9), `GuiCloudTransfer.cpp:315-345` (FD-8), `HttpServerThread.cpp:615-630`, `CMakeLists.txt` (the defines), the distribution's `config/functions:128`, `virtual/emulators/package.mk:1735-1739`, `start_es.sh`, `es_savestates.cfg`, and `ApiSystem.cpp`'s support switch.
**Deliberately not examined:** the files of the interacting slices beyond those reads (brief § 2, out of scope).
**Dimensions not exercised:** runtime behaviour (no guest yet), timing (Q5), memory (`es-launch-memory`), the compiled tests, and thread interleavings (no sanitizer run).

# Retrospective — M6.P2 T2, EmulationStation's launch path

**Auditor:** Code Auditor skill, with the renovation face (plan § 4)
**Date:** 2026-10-23
**Subject:** #649, the twenty EmulationStation paths at the pin `16dbac5211`
**Spec:** `docs/reviews/briefs/es-launch-path.md` version 2

---

## Running Notes

Written after Phase 2's entries, from them and from the tree. The prior audits' verdicts (provenance in `01-research-notes.md` § 1.5) were not opened before Phase 2 was written. They are compared in `04-analysis.md` § Finding Verification.

### 3.1 Architectural coherence

The launch path is coherent in its order: the view's transition, then `FileData::launchGame`'s gates, the command, the hooks, the run, and the return. It carries two structural costs.

- **The gates sit after the transition (VC-1).** The question is asked once the screen has said the game is starting. The gates are `FileData`'s, and the transition is `ViewController`'s, which knows nothing of them. That is the seam that misplaced them.
- **`FileData.cpp` is five responsibilities in one unit (Q7).** It holds the node model, the art lookup, the command builder, the gates and their deferred launch, and the return path (capture, rotation, play time, exit sync). Of its 2,680 lines about a fifth are the fork's, and all the fork's are in the last three. `launchGame` alone is 400 lines (`:928-1328`). A reader meets the gates' 60-line rationale comment (`:941-989`) before the first gate.

No orphaned file. Five unreached functions (Q6) are upstream API kept for the merge, plus `renumberSlots`, which is retired.

### 3.2 Project conformance

**Instruction files** (read this session; equal to `next`'s except P1's two files, the council's `IMPORTED-FROM.md` and this lane's own `es-native-ui.md` sentence):

| Rule | Relevance | Finding |
| --- | --- | --- |
| `es-player-text.md` § Conventions, § Outcome vocabulary, § Every fork string in English and French | ✓ | ⚠ FD-10 (`UKNOWN ERROR`), MN-5 (three boxes outside `_()`), MN-6 (`DOWNLOAD ... GAMES`). The four gate questions follow D-CLOUD-130/D-UI-096 (statement, consequence, two verbs, safe last). The proxy cards follow D-UI-107. |
| `es-ui-style-guide.md` § Confirmations, § Glyphs | ✓ | ⚠ FD-12 (two spaces before a toast's glyph). The gate boxes have no `NO`/`OK` button, so the back button falls to the last one, `KEEP WAITING`, which is safe. |
| `es-native-ui.md` § Core patterns (`exists(path, false)`), § Spacing's tiers, D-UI-093/095 | ✓ | ✓ The stamps and markers are read uncached (`ProxyCards.cpp:97`, `main.cpp:960`, `:1051`, `SaveStateRepository.cpp:144`). FD-11's `/tmp/launch_error.log` is fresh by order (cache reset at `FileData.cpp:1113`), not by the rule; recorded. One floating surface at a time (`ProxyCards.cpp:499-513`). |
| `es-code-traps.md` § A rescan that deletes FileData drops the view first | ✓ | ✓ for the view and collections (SD-1); ⚠ FD-8 for a deferred launch's pointer (latent). |
| `es-code-traps.md` § Comments near a translatable string must be ASCII | ✓ | Not re-checked by `grep -nP '^\s*//.*[^\x00-\x7F]'` yet; owed before any ES commit (stage E). |
| `time-to-play.md` | ✓ | ⚠ VC-1, SR-2 to measure. **Doctrine drift (lead for the doctrine slice):** the rule says "what ships today still cancels an automatic sync at launch (D-CLOUD-076) ... D-CLOUD-109 replaces that". The code ships D-CLOUD-130: every sync a launch would interrupt asks STOP IT AND PLAY / KEEP WAITING, nothing is cancelled until the answer (`FileData.cpp:993-1008`, `:947-950`). |
| `least-surprise.md` | ✓ | ⚠ VC-1 (the screen says starting, then asks); FD-1 (a spectator joins as a player). |
| `upgrade-and-install.md` | ✓ | ⚠ SD-4 (a stored sort id from another build), MN-3 (a stored boot command), SS-2 (a `.bak` left by the fallback). Each finding's fix carries its `Already written:` line in the punch list. |
| `engineering-practices.md` § Guards must fail closed, § Fail gracefully, § A name is not a behaviour | ✓ | ⚠ SB-2 (fails closed, silently); FD-4 (`get...` writes `system.cfg`); SS-4 (a copy that reports success unchecked). |
| `decision-register.md` § A reversal sweeps its old words | ✓ | ⚠ MN-4 (three comments describe superseded behaviour). |
| `vm-first.md`, `bugs-are-agent-first.md` | ✓ | Every runtime claim is held as a lead until the guest proof runs (queued). Each defect's bug issue gets its VM line at stage D. |

**Blindspot register** (the entries brief § 3 names):

| Entry | Does this work repeat it? |
| --- | --- |
| 7 host tools are not the device's | Not repeated: no device verdict was made from a host tool. `git apply --check` is a host operation on host data (Q4). |
| 13 assumed done | Not repeated: no criterion was ticked from an artifact's existence. AC-07/10/11 cite commands. |
| 30 a resumed session built on its own summary | Guarded: every finding cites `file:line` read this session. Phase 4.5 re-reads each. |
| 35 a remedy built on an audit's claim about a default | Avoided: `CheckBiosesAtLaunch`'s default was read (`Settings.cpp:207`, false) before VC/308221458's Q5 claim was graded. |
| 44 proven at a fixture's size | **Applies to SR-2**: the exit's state refresh must be measured at hundreds of states, not a handful. The queued proof says N = 500. |
| 46 a name read as a behaviour | **Found in the code**: FD-4 (`getlaunchCommand` persists `system.cfg`). Avoided in this audit: FD-1 was corrected by the caller search, not by the field's name. |
| 49 an edit made blind to the compiler | No ES edit yet. #699's fix restores the tool that guards it (stage A). |
| 51 a checklist built from open boxes | Applies at stage D: each punch item is written from the reading, not from a prior audit's box. |
| 54, 63 a measurement on a guest whose renderer was not the device's | Applies to Q5: `time-to-play --vm` sets gl, and the renderer is read and recorded beside the numbers. |
| 59 a memory measurement on a page that never loaded | Applies to `es-launch-memory`: the frame of the loaded game is checked, not only the process. |
| 64 a wait lengthened for an event the code cannot produce | Read: `launchWhenGone`'s 20 s, `captureGate`'s 10 s, the proxy's 45/10/90/120 s each wait for an event their callers produce. No repeat found. |
| 65 a proof's substitute | Applies to the queued proofs: a fixture ROM with `$` in its name (SS-1) and a fixture `.m3u` (FD-14) are named substitutes. Each checkbox stays partial until the real input is seen. |
| 73 a monitor of completion, not activity | Applies to the queued tool runs (watched by their own output). |

**Project invariants:**
- Progress over recency: the `racommands` fallback's `.bak` dance can restore an older auto state over a newer one after a killed session (SS-2), on the fallback path only.
- No secrets in what is written: `global.bootgame.cmd` stores a launch command in `system.cfg`, including a netplay nick but no password (`netplayClientPassword` is never set, FD-1). The launch log goes through `maskSecrets` (`FileData.cpp:1090`).
- The allowlist invariant: not this slice's.
- Every change lands on a device with state: SD-4, MN-3, SS-2 above.

### 3.3 Spec fidelity

The code agrees with the decisions brief § 3 names, with three exceptions:

- **D-CLOUD-130 ships, not D-CLOUD-109's bounded wait.** `time-to-play.md` says otherwise (above). The code is right, and the rule's paragraph is stale.
- **D-UI-069** (no renumbering) holds in `SaveState::onGameEnded`. `FileData.cpp:1134` says the opposite (FD-13), and `renumberSlots` survives unreached (SR-1).
- **D-UI-031** reworded `SKIPPED - NO NETWORK CONNECTION`, and `main.cpp:595` keeps the old words (MN-4).

### 3.4 Platform architecture conformance

| Check | Relevance | Finding |
| --- | --- | --- |
| Reference Implementation | · | not this repository's model |
| Schema-Before-Code | · | not applicable |
| Dogfooding Gate | · | not applicable |
| API-First | · | the HTTP API's `POST /launch` reaches `ViewController::launch` (FD-8's context) |

### 3.5 Cross-system interaction audit

### Interaction: the command × `runemu.sh`'s parsing (T1, #648, #730)
**State shared:** the argument line: `-P<system>`, `--core=`, `--emulator=`, `--controllers="..."`, `-state_slot N -state_file "<file>"`, and the netplay words.
**Wipe risk:** a word in one reading that the other reads differently: a nick such as `'Bob -Pro'` (LaunchCommand.h's header), a state file path holding `--core=` (#730), a ROM name with `"`/`$` inside `-state_file "..."` (SS-1).
**Test coverage:** PARTIAL. `LaunchCommandTests.cpp` covers this side with a `runemu` stand-in; T1's #730 holds the launcher's side.
**Finding:** risky at SS-1 (this side), with #730 on the other side. The two halves are one fix series across lanes, which is the coordinator's to sequence.

### Interaction: the gates × the sync, the transfer and the proxy (T18, T20)
**State shared:** `ThreadedCloudSync::isRunning`, `CloudTransferJob::current`, `ProxyCards::sendRunning/topUpRunning`, and the capture generation.
**Wipe risk:** a gate answered while its job ends. The answer lambdas re-check (`cancelForLaunch(...) || !isRunning()`, `FileData.cpp:1001`).
**Test coverage:** PARTIAL. `tests/launch-capture-gate.py` and `tests/launch-deferred-state.py` (queued) compile `captureGate` and `launchNow`. The question boxes need a running sync on the guest, which is a lead for the integration run (brief § 5: the shared QA backend is not this lane's).
**Finding:** safe in logic. VC-1 is the placement cost.

### Interaction: `rescanIfFolderChanged` × the deferred launches
**State shared:** `FileData*` of the system's files.
**Wipe risk:** the merge's `vanished` deletes a file a pending launch holds (FD-8). No current trigger lands in a wait; the API's reload does.
**Test coverage:** UNTESTED (the guest proof is queued).
**Finding:** risky, latent.

### Interaction: the exit path × `cloud_capture` and the exit sync (T16, T18)
**State shared:** `sCaptureInFlight`, `sExitGeneration` and `sCaptureWaitedOn`; the capture manifest; the sync lock.
**Wipe risk:** a launch on the next frame under a running capture, which `captureGate` prevents. A second exit's capture: the generation check (`FileData.cpp:1281`, `:1295`).
**Test coverage:** PARTIAL (`launch-capture-gate.py`, queued).
**Finding:** safe.

### Interaction: the boot game × the startup sync (MN-3)
**State shared:** the saves the boot game writes; the capture.
**Wipe risk:** the boot game runs before the window and before the startup sync. The sync's `copy --update` then carries what it wrote; the capture records it (`main.cpp:551-570`).
**Test coverage:** UNTESTED.
**Finding:** safe for the saves. The stored command's staleness is MN-3.

### 3.6 What's missing?

Searches:
- `git -C $W grep -n -E 'formatCommandLineArgument|getContentFiles|deleteGameFiles|launchToken' $PIN -- es-app/tests` finds `launchToken` (LaunchCommandTests) and none of the other three. **No unit case** covers `formatCommandLineArgument` (FD-2) or `getContentFiles`/`deleteGameFiles` (FD-14). Both are pure enough to test (es-code-traps § Pure text has a home).
- `ls $W/es-app/tests/unit/` (queued with the unit build) was not read further here. The punch list's test-first items name the files.
- No flow or frame evidence is owed yet: no player-visible change has been made.
- `git -C $W log --oneline -5 $PIN -- es-app/tests` (proximate work) is run at stage E with the stream briefs.

### 3.6.5 Audit-prescription verification: the shapes, every site

Searches: `git -C $W grep -n -E <shape> $PIN -- es-app/src es-core/src` per row (`00-running-log.md` 17:5x).

| Shape | Site | Sibling (this slice) | Adjacent (another slice) | Verdict |
| --- | --- | --- | --- | --- |
| a path or name double-quoted into a shell line, unescaped (SS-1) | `SaveState.cpp:97` | `:77`, `:111` | `ApiSystem.cpp:1527`, `:1659` (7z on a ROM path, reached from `FileData::checkMd5`/the hasher), `:838`, `:2591-2593`, `:3502` (T21); `GuiMenu.cpp:1842` (`rocknix-keyboard`, the GuiMenu slice) | FIX-NOW in the slice; FILE-FOLLOWUP as leads for T21 and the GuiMenu slice |
| quoted only when it holds a space (FD-2, FD-9) | `FileData.cpp:530` | none | `Scripting.cpp:92`, `:109` (T33/T21); `ApiSystem.cpp:2076`, `:3471` (T21) | FIX-NOW (the site); leads for the others |
| a path filter by substring (SD-2) | `SystemData.cpp:627` | `:631` | none found | FIX-NOW |
| `> size()` before `.at()` (FD-15) | `FileData.cpp:1659` | none | `GuiGamelistOptions.cpp:148` (the game-list options slice) | FIX-NOW; lead |
| a list's entries deleted with no containment (FD-14) | `FileData.cpp:1505-1506` | `:1487-1495` (every `MD_PATH` metadata file removed, wherever it points, including art a second game's entry names) | none found | FIX-NOW |
| superseded words in a comment (MN-4) | `main.cpp:617` | `:595`, `:1110-1114` | `GuiMenu.cpp:6665`, `:8167` are current player strings (`NO NETWORK CONNECTION DETECTED ...`) on another surface, the GuiMenu slice's to judge against D-UI-031 | FIX-NOW (comments); lead |
| a player string outside `_()` (MN-5) | `main.cpp:929` | `:328-329`, `:336-339` | `GuiMenu.cpp:11714`, `:11727`, `:11738` (eject drive), `SystemView.cpp:234` (upstream) | FIX-NOW for the fork string; D-UI-079 for the upstream ones; leads |
| an unknown argument ignored silently (MN-1) | `main.cpp` `parseArgs` | `:98-106`, `:220-229` (MN-2, unbounded `argv[i+1]`) | none | FIX-NOW or BY-DESIGN, the stream brief's call |
| a plain static read across threads (FD-18) | `FileData.h:217` | `ViewController.cpp:39` `sConfigurationReplaced` (interface thread only: SAFE-AS-TESTED by reading) | `SaveStateConfigFile.cpp:271` `_cache` (interface thread only today, SC-1) | FIX-NOW (FD-18); recorded |

### 3.7 Retrospective Summary

#### Architectural Assessment
The order is right except for the gates' placement (VC-1). `FileData.cpp` carries five responsibilities, and the fork's part of it is the launch.

#### Cornerstone Alignment
The ES rules are met with the exceptions above. The doctrine has one stale paragraph (`time-to-play.md`, D-CLOUD-130).

#### Cross-System Interactions
The command × `runemu.sh` is the riskiest seam (SS-1 with #730). The rescan × deferred launches is latent (FD-8).

#### Spec Drift
Three comments and one rule describe superseded behaviour (MN-4, FD-13, `time-to-play.md`).

#### Missing Artifacts
Unit cases for `formatCommandLineArgument` and for `getContentFiles`/`deleteGameFiles`.

# Audit Analysis — M6.P2 T2, EmulationStation's launch path

**Auditor:** Code Auditor skill, with the renovation face (plan § 4)
**Date:** 2026-10-23
**Subject:** #649, the twenty EmulationStation paths at the pin `16dbac5211` (distribution `reviewed-at` `f4e0f0a196`)
**Spec:** `docs/reviews/briefs/es-launch-path.md` version 2

---

## Executive Summary

All twenty paths were read line by line: 11,287 lines, 17 fork-own and 3 upstream-carried. The fork's part of the three big files is the launch: about a fifth of `FileData.cpp`, 280 lines of `SystemData.cpp` and 498 of `main.cpp`. The rest is batocera's, byte for byte.

Leads before the second opinion: no Critical and no High. **Four Medium:**

- **FD-14:** DELETE GAME removes every absolute path an `.m3u` lists and any `..` path a `.cue` or `.gdi` names, with no containment. It is upstream code on a fork-own path.
- **SS-1:** the shipped save-state path double-quotes the state file into the command, so a ROM name with `$`, a backtick or `"` expands or breaks.
- **SD-2:** a sub-folder of any system is skipped when its path contains `ports` or `windows` (`Sports/`, `Imports/`). Its games never show.
- **VC-1:** a launch the gates will refuse plays the whole transition and the game's splash before it asks.

The rest are Low and Renovation rows. Q4: `rocknix/master` has 0 commits on the twenty since `cada856d8`; batocera has seven, none merged yet, three applying cleanly. Q6: 370 entry points, five unreached functions (one fork-retired, `renumberSlots`) and the expected unshipped `#if` arms. Q5 and every guest proof are queued for the host's return. So is Phase 4.6: its `npm install` is a runtime under the hold.

## Acceptance-criteria scorecard

| AC | Verdict (end of Phase 2) | Note |
| --- | --- | --- |
| AC-01 | PARTIAL | `00` to `04` now; `05` is stage D |
| AC-02 | UNTESTABLE | the lint runs after 4.6 |
| AC-03 | UNTESTABLE | 4.6 waits for the host |
| AC-04 | UNTESTABLE | stage F |
| AC-05 | PARTIAL | `reviewed-at` recorded; the body is written at the hand-back |
| AC-06 | PARTIAL | all but the BUILD_ID (guest) |
| AC-07 | PASS | 20 rows |
| AC-08 | PARTIAL | 4 of 14 checks ran; 10 queued (host) |
| AC-09 | UNTESTABLE | guest |
| AC-10 | PASS | 370 rows, below |
| AC-11 | PASS | below |
| AC-12 | UNTESTABLE | 0 guest proofs yet |
| AC-13 to AC-16 | UNTESTABLE | stages E to H |

## Code Quality Assessment

### Strengths
- The fork's launch code states its reasons beside the code: each gate, the capture generation, and the bookkeeper's lock order. It is quoted consistently (`shellQuote` on every capture, retire and adopt argument; `FileData.cpp:1147-1153`, `SaveStateBookkeeper.cpp:182-228`, `main.cpp:555-561`).
- `rescanIfFolderChanged` merges rather than rebuilds, dropping views and collection entries before deleting (SD-1).
- The fault handler is async-signal-careful and re-raises (MN-7).
- The pure parts have homes and tests: `LaunchCommand.h` (LaunchCommandTests), `SaveStateJobQueue` (SaveStateJobQueueTests).

### Concerns
- Command lines are built by string concatenation in several dialects: `shellQuote`, `getEscapedPath`, quote-on-space, and raw double quotes (SS-1, FD-2, FD-3).
- Upstream's list-driven deletes have no containment (FD-14).
- Plain statics are read across threads (FD-18).

### Complexity Hotspots
- `FileData::launchGame` (`:928-1328`, 400 lines, five responsibilities).
- `FileData.cpp` overall, which mixes the node model, the art lookup, the command, the gates and the return.
- `SystemData.cpp` (`loadConfig`'s two loading modes; `populateFolder`'s hard-coded exclusions).
- `main.cpp`'s `main` (`:697-1367`).

## Cornerstone Conformance

### Findings
See `03-retrospective.md` § 3.2. The ES rules are met except FD-10, FD-12, MN-5 and MN-6 (words), FD-8 (latent) and MN-4 (comments). One doctrine paragraph is stale (`time-to-play.md` on D-CLOUD-076/109, where the code ships D-CLOUD-130).

## Spec Fidelity

### Aligned
D-CLOUD-130 (every sync a launch interrupts asks), D-UI-096 (the question's shape), D-UI-093/095 (one surface at a time; automatic network work shown), D-UI-101/109 (saves first, then the batch), D-RA-035, D-CLOUD-062 (the frozen pair read from the finished command), D-LAUNCH-001 (play time on exit 0), D-UI-069 in `onGameEnded`, D-CLOUD-133 (SIGTERM kept immediate), D-UI-073 (the bookkeeper's rules).

### Diverged
FD-13 (a comment says renumbering), MN-4 (three comments), and `time-to-play.md` (the rule, not the code).

## Missing Artifacts

Unit cases for `formatCommandLineArgument` (FD-2) and `getContentFiles`/`deleteGameFiles` (FD-14). Search: `git -C $W grep -n -E 'formatCommandLineArgument|getContentFiles|deleteGameFiles' $PIN -- es-app/tests` → none.

## Risk Assessment

| Risk | Likelihood | Impact | Finding |
| --- | --- | --- | --- |
| A player's files outside the game's folder deleted by DELETE GAME | low (needs such a playlist) | high (data loss) | FD-14 |
| A state launch's command broken or expanded by a ROM name | low-medium (`$` in names) | medium (wrong file, or a command) | SS-1 |
| Games in a folder named `...ports`/`...windows` invisible | medium (genre folders) | medium (games missing) | SD-2 |
| A refused launch looks like a started one, then asks | high (every gated launch) | low (time, surprise) | VC-1 |
| A freed `FileData` used by a deferred launch | very low (API reload during a wait) | high (crash) | FD-8 |
| A stored sort id crashes a list after a cross-build update | low | medium (crash on open) | SD-4 / FD-15 |

## Coverage Boundary

**Examined:** the twenty paths by reading, and the context reads named in `02-forward-audit.md` § Coverage Boundary.
**Not exercised:** runtime (queued), compiled tests (queued), timing and memory (queued), thread interleavings (no sanitizer).

## Finding Verification (Phase 4.5)

Each graded finding's primary lines were re-read at 17:5x from `git show $PIN:<path>`, not from the notes. **Confirmed:**
- **FD-14:** `FileData.cpp:1446-1451` (`isAbsolute` → insert; the `trim[0] == '/'` arm unreachable because `FileSystemUtil.cpp`'s `isAbsolute` is `path[0] == '/'` off WIN32), `:1503-1506` (the removes). The confirmation is `GuiGameOptions.cpp:253` `THIS WILL DELETE THE ACTUAL GAME FILE(S)!`, which names no path.
- **SS-1:** `SaveState.cpp:77`, `:97`, `:111`.
- **SD-2:** `SystemData.cpp:626-632`.
- **SD-3:** `SystemData.cpp:1039-1043`, `:1046-1050`.
- **VC-1:** `ViewController.cpp:584-587` (the splash before the animation), `:615-618` (`doLaunchGame` at its end).
- **FD-15:** `FileData.cpp:1658-1662`.
- **MN-3:** `main.cpp:533-540`.

**Withdrawn or graded down while writing** (recorded where they changed):
- **FD-1** Medium → Low and Q6: `netplayClientPassword` is never assigned.
- **FD-8** Medium → Low and latent: the rescan's two posts cannot land in a wait.
- **VC-2**: netplay off short-circuits the IP check.
- **FD-18**'s HTTP-thread reader: none exists.

**Prior audits (provenance only, read now that Phase 2 is written):** the eight punch lists of § 1.5 were grepped for this phase's finding shapes (`.m3u`, `state_file`, `rfind("ports")`, `UKNOWN`, `formatCommandLineArgument`, `renumberSlots`). The command and its result are in the running log. A prior item that already names a finding is cited at Phase 5, and nothing is transcribed.

## Renovation face

### Q1 Modernize
- **FD-18:** `FileData::mRunningGame` → `std::atomic<FileData*>` behind `GetRunningGame()`. The tree's form is `sGamesStarted` (`FileData.cpp:90`).
- **One quoting dialect for command lines:** SS-1, FD-2 and FD-3 should use `Utils::String::shellQuote`, which the fork already uses in the same file (`:678`, `:1148-1153`).
- **Recorded, not proposed (upstream lines; merge cost against batocera, D-WORKFLOW-185's shape):** raw owning pointers (`mDisplayName`, `SystemData`'s members, `new SystemDataPtr[]`), C-style casts, and `ifstream` with manual `close()`.
- **The duplicated readers of one argument line** (`launchToken` here, `${ARGUMENTS##*-P}` in `runemu.sh`, and the `-P` fixtures in two test files) are the seam of § 3.5. The coordinator sequences the two lanes' fixes.
- The `racommands` save-state arms (SS-2) and the `--core=`/`--emulator=` tokens are #336's line: Q1 items there are `deferred:#336`.

### Q2 Standards and best practices
- **FD-10:** `UKNOWN ERROR` (`FileData.cpp:760`; the msgid in the French catalogue, and batocera's).
- **FD-11:** a log file's text shown to the player, unbounded.
- **FD-12:** two spaces before a toast's glyph (`es-ui-style-guide.md` § Glyphs).
- **MN-5:** three boxes outside `_()` (`main.cpp:929`, `:328-339`), so no French (D-UI-051). `es-untranslated` cannot see them.
- **MN-6:** `DOWNLOAD YOUR GAMES, ...` (`main.cpp:980`; D-UI-022's verbs and tiers).
- **SS-1:** the `shellQuote` rule (brief § 4 Q2).
- Checks run at the pin: credential quoting 9/9/0, menu map 0 missing, French 703/703/0, vocabulary 163 judged, 0 wrong (`02-forward-audit.md` § Mechanical checks).

### Q3 Bugs
Defects, each a `bug` issue at stage D with its VM criterion:
- **Medium:** FD-14, SS-1, SD-2.
- **Low:** SD-3, SD-4/FD-15, FD-8 (latent), MN-2, MN-3, SB-2, FD-1 (spectator), FD-2/FD-3 (reachable under a custom template), FD-18.

Seam leads posted for other slices: FD-7 (T36), FD-9/FD-19 (T33/T21), PC-1/SB-3 (T35/T16/T18), PC-2 (T21), the 7z hash quoting (`ApiSystem.cpp:1527`, `:1659`; T21), `GuiGamelistOptions.cpp:148` (FD-15's sibling), and `GuiMenu.cpp:11714-11738` (MN-5's sibling).

### Q4 Package currency: both upstreams
- **`rocknix/master`** (`f6c542872`, fetched 2026-10-23): `git -C $W rev-list --count cada856d8..rocknix/master -- <the 20 paths>` = **0**. Nothing to take.
- **`batocera/master`** (`b2ceb55a7`): `git -C $W log --oneline 1750dded8..batocera/master -- <the 20 paths>` = **7**. Each was tested with `git show <c> -- <20> | git apply --check` (forward) and `--reverse`, which writes nothing:

| Commit | Date | Subject | Files | Forward / reverse at the pin | Disposition |
| --- | --- | --- | --- | --- | --- |
| `13e21d420` | 2026-09-12 | Fix for quicksearch/random system | `SystemData.cpp` (`getRandomSystem`) | applies / no | **to merge**: a fix (random picks only visible systems), upstream lines, no fork overlap |
| `195a517ef` | 2026-10-01 | Merge pull request #2213 from Tartifless/master | (the merge carrying `13e21d420`) | no diff of its own | **merged with `13e21d420`**: the same change |
| `b69fb143c` | 2026-09-30 | Add a "max depth" to limit the number of rom subfolders to parse | `SystemData.cpp`, `.h` | conflicts (`SystemData.cpp:100`, `.h:119`, the fork's `mFolderScannedAt` hunk) / no | **to merge, by hand**: `populateFolder`'s new depth must also reach the fork's `rescanIfFolderChanged` (`:434`), or a rescan reads deeper than startup did and its merge reports files as new |
| `d17cf003e` | 2026-10-05 | [Pico8] Only show .p8 carts as images when they are PNG files | `FileData.cpp` (`getImagePath`) | applies / no | **to merge**: a fix on upstream lines (`:442`) |
| `308221458` | 2026-10-16 | fix zoom into the game art at launch; fix bios check threading | `ViewController.cpp`, `.h` | applies / no | **to merge**: the BIOS check leaves the interface thread and runs during the transition (`CheckBiosesAtLaunch`, default false, `Settings.cpp:207`). It changes `launch`'s signature for every caller in other slices, and it touches VC-1's ground (where the gates sit) |
| `5f106acce` | 2026-10-19 | fix game launch zoom timings | `ViewController.cpp` | stacks on `308221458` | **to merge after `308221458`** |
| `0806a0c5c` | 2026-10-20 | launch zoom centres on the selected game art from every launch path, fade to the game splash when there is no art | `ViewController.cpp` | stacks on `308221458` | **to merge after `308221458`** |

None is merged, none is not applicable, and six are to merge, one by hand. Upstream merges are the coordinator's to schedule (D-WORKFLOW-189). The three `ViewController` commits are best taken before VC-1's fix, so the fix is written once against the new `launch`. The inventory's `overlap` column is false for all twenty, measured against `rocknix/master` only, so these seven come from the log, as the brief says.

### Q5 Efficiency
The measurements are **queued** until the host's `resource return` (brief § 5). No number is claimed here. What will be measured, against #336's baseline (a game's first frame 1.05 s from the press, the next game's 2.03 s from the exit), with the guest's `system.loglevel` recorded:
- `tools/time-to-play --vm --no-configure-remote --only launch,exit,g2g --repeat 3`;
- `tools/es-launch-memory --cycles 5`'s per-cycle table.

Items to itemise:
- **Press → command:** the transition, 750 ms by default (VC-1); `captureGate`'s ≤ 300 ms (`FileData.cpp:888`); `configureEmulators` (FD-6); `window->deinit` and `malloc_trim`; `fireEvent("game-start")`'s three directory scans.
- **Exit → next frame:** `FileSystemCache::reset`; the state repository's `refresh` (SR-2, at N = 0 and N = 500 states); `recordAfterSession`; `fireEvent("game-end")`; `window->init`; `refreshCollectionSystems` and `saveToGamelistRecovery`.
- **Startup:** the boot game, `serial_number_check`, `preload`, and `loadSystem(name)`'s re-parse per group (SD-3).

Until then this subsection is the named absence of a measurement, which brief § 4 allows, and #649's AC-09 stays open.

### Q6 Dead ends: one reachability row per entry point of the twenty files, and per preprocessor conditional

(The 370-row reachability table is omitted from this packet; its summary is above and below.)

**The commands and their counts** (at the pin):
- brief § 4's header regex → **154** declarations;
- `grep -n '^static '` over the ten `.cpp` → **32** lines (13 functions, 19 data);
- `git grep -n -E '^#(if|else|elif)'` → **60** (the brief recorded 36; the pattern also matches `#ifdef`/`#ifndef`).

A regex misses multi-line, inline and indented forms, so the list was rebuilt by `q6-reachability.py` (this folder; `python3 -I q6-reachability.py $W $PIN`) to **295** declarations, **13** static functions and **62** conditionals: **370 rows**, read by eye against the headers. The hand corrections: `recordCopy`, whose call spans two lines and is reached (`GuiSaveState.cpp:524`), and the 19 static data lines, which are not entry points.

**Unreached:** five functions, each confirmed with `git grep -n -w <name> $PIN -- es-app/src es-core/src es-app/tests`: `renumberSlots` (SR-1, fork-retired by D-UI-069), `isVirtualFolderDisplayEnabled`, `hasGamelist`, `setIndex` and `isDefaultConfig` (upstream API). Of the conditionals, every WIN32, `_RPI_`, `BATOCERA`, `_ENABLE_KODI_`, `FREEIMAGE_LIB` and `DEBUG` arm and the `#else` of each `#if ROCKNIX` are unshipped. Each is a row, not a removal (D-WORKFLOW-185's shape). Beyond functions:
- the template placeholders `%BASENAME%`, `%ROM_RAW%`, `%GAMENAME%`, `%SYSTEMNAME%`, `%GAMEINFOXML%`, `%HOME%` and `%NETPLAY%` are not in the shipped command (FD-5; `distributions/ROCKNIX/config/functions:128`);
- `-monitor` needs ` -system `, which the command lacks;
- the `racommands` save-state arms run only without `es_savestates.cfg` (SS-2);
- `LaunchGameOptions::isSaveStateInfoTemporary` and `netplayClientPassword` (FD-21);
- the commented-out SIGTERM handler (`main.cpp:730`, decided by D-CLOUD-133);
- `--log-path` is passed by `start_es.sh` and read by nobody (MN-1).

Final count: **370 rows** (295 + 13 + 62), command counts 154/32/60, and **5 unreached functions** carrying `Already written:`.

### Q7 Clarity and structure
- `FileData.cpp` holds five responsibilities in 2,680 lines, and `launchGame` alone is 400 lines (§ 3.1).
- Nothing in the three big files says which lines are batocera's and which the fork's (the hunk maps above). A header line naming the provenance would save a reader the `git diff`.
- **FD-4:** `getlaunchCommand` writes `system.cfg`.
- **FD-13:** the renumbering comment.
- **MN-4:** three stale comments.
- **SS-3:** duplicated arms.
- **VC-3:** three copies of the end callback.
- **ProxyCards:** the comments carry audit identifiers as much as rules.
- **SD-6:** dead commented code.
- The three readers of one argument line (Q1).

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)
- `tools/es-untranslated` counts only `_()` strings, so a player string outside `_()` has no French and no checker sees it (MN-5). This is a tool change for the tooling slice, not a rule.
- `tools/vocabulary-check` judges three word pairs. A verb outside the two (MN-6, `DOWNLOAD`) passes. Same owner.

### Codification Gaps (needs-new-rule)
- `time-to-play.md`'s paragraph on what ships (D-CLOUD-076/109) is stale against D-CLOUD-130. That is a doctrine edit for the doctrine slice, found here and not this lane's to make (D-WORKFLOW-189).

### Recommended Action Sequence
At stage D, the punch list and the bug issues. Then the coordinator's stream briefs (stage E). The leads are posted on #649 for their slices.

### Handoff to Phase Z.6
None; the retro is at stage G.

## Second opinion (Phase 4.6)

**Pending: the host's return.** Depth Extended: GPT-6 Astra (`--member gpt`, `max`) and Gemini 4 Argon (`--member gemini-argon`, `high`), a refutation pass each, through `tools/council/run` only. The runner needs `npm install --prefix tools/council`, a runtime the M7 handoff holds (brief § 1, § 5). The briefs and `review-plan.json` are prepared before the call. Probes, calls, grading and the net-effect line are written here when they run. Phase 5 follows them.

## Quality Self-Check

- Every finding cites `file:line` at the pin, read this session. Phase 4.5 re-read the graded ones.
- No verdict rests on tracker state.
- Every runtime claim is a lead, held for the guest.
- Two findings were corrected by caller searches (FD-1, FD-8), and the corrections are recorded where they happened.
- The counts that differ from the brief are written as deltas (`rocknix/master`'s hash, #120's state, the conditional count, the reader on the HTTP thread, Scripting's slice).

## Source excerpts at the pin (`git show 16dbac5211:<path>`, line-numbered)

### `es-app/src/FileData.cpp:528-534`

```cpp
528	static std::string formatCommandLineArgument(const std::string& name)
529	{
530		if (name.find(" ") != std::string::npos)
531			return "\"" + Utils::String::replace(name, "\"", "\\\"") + "\"";
532	
533		return Utils::String::replace(name, "\"", "\\\"");
534	};
```

### `es-app/src/FileData.cpp:607-723`

```cpp
607		std::string command = system->getLaunchCommand(emulator, core);
608	
609		if (forceCore)
610		{
611			if (command.find("%EMULATOR%") == std::string::npos && command.find("-emulator") == std::string::npos)
612				command = command + " -emulator %EMULATOR%";
613	
614			if (command.find("%CORE%") == std::string::npos && command.find("-core") == std::string::npos)
615				command = command + " -core %CORE%";
616		}
617	
618		const std::string rom = Utils::FileSystem::getEscapedPath(getPath());
619		const std::string basename = Utils::FileSystem::getStem(getPath());
620		const std::string rom_raw = Utils::FileSystem::getPreferredPath(getPath());
621		
622		command = Utils::String::replace(command, "%SYSTEM%", systemName);
623		command = Utils::String::replace(command, "%ROM%", rom);
624		command = Utils::String::replace(command, "%BASENAME%", basename);
625		command = Utils::String::replace(command, "%ROM_RAW%", rom_raw);
626		command = Utils::String::replace(command, "%EMULATOR%", emulator);
627		command = Utils::String::replace(command, "%CORE%", core);
628		command = Utils::String::replace(command, "%HOME%", Paths::getHomePath());
629		command = Utils::String::replace(command, "%GAMENAME%", formatCommandLineArgument(gameToUpdate->getName()));
630		command = Utils::String::replace(command, "%SYSTEMNAME%", formatCommandLineArgument(system->getFullName()));
631	
632		// Export Game info XML is requested
633	#ifdef WIN32
634		std::string fileInfo = Utils::FileSystem::combine(Utils::FileSystem::getTempPath(), "game.xml");
635	#else
636		std::string fileInfo = "/tmp/game.xml";
637	#endif
638	
639		if (command.find("%GAMEINFOXML%") != std::string::npos && saveToXml(gameToUpdate, fileInfo, true))
640			command = Utils::String::replace(command, "%GAMEINFOXML%", Utils::FileSystem::getEscapedPath(fileInfo));
641		else
642		{
643			command = Utils::String::replace(command, "%GAMEINFOXML%", "");
644			Utils::FileSystem::removeFile(fileInfo);
645		}
646		
647		if (includeControllers)
648			command = Utils::String::replace(command, "%CONTROLLERSCONFIG%", controllersConfig);
649	
650		if (options.netPlayMode != DISABLED && (forceCore || gameToUpdate->isNetplaySupported()) && command.find("%NETPLAY%") == std::string::npos)
651			command = command + " %NETPLAY%"; // Add command line parameter if the netplay option is defined at <core netplay="true"> level
652	
653		if (SystemConf::getInstance()->get("global.netplay.nickname").empty())
654		{
655			SystemConf::getInstance()->set("global.netplay.nickname", ApiSystem::getInstance()->getApplicationName() + " Player");
656			SystemConf::getInstance()->saveSystemConf();
657		}
658	
659		if (options.netPlayMode == CLIENT || options.netPlayMode == SPECTATOR)
660		{
661			std::string mode = (options.netPlayMode == SPECTATOR ? "spectator" : "client");
662			std::string pass;
663	
664			if (!options.netplayClientPassword.empty())
665				pass = " -netplaypass " + options.netplayClientPassword;
666	
667			// mitm_session: Should inject this into retroarch -> --mitm-session=ID
668			std::string session;
669			if (!options.session.empty())
670				session = " -netplaysession " + options.session;
671	
672	#if WIN32
673			if (Utils::String::toLower(command).find("retroarch.exe") != std::string::npos)
674				command = Utils::String::replace(command, "%NETPLAY%", "--connect " + options.ip + " --port " + std::to_string(options.port) + " --nick " + SystemConf::getInstance()->get("global.netplay.nickname"));
675			else
676	#endif
677	#if ROCKNIX
678				command = Utils::String::replace(command, "%NETPLAY%", "--connect " + Utils::String::shellQuote(options.ip) + " --port " + std::to_string(options.port) + " --nick " + Utils::String::shellQuote(SystemConf::getInstance()->get("global.netplay.nickname"))); // fork #275
679	#else
680				command = Utils::String::replace(command, "%NETPLAY%", "-netplaymode " + mode + " -netplayport " + std::to_string(options.port) + " -netplayip " + options.ip + session + pass);
681	#endif
682		}
683		else if (options.netPlayMode == SERVER)
684		{
685	#if WIN32
686			if (Utils::String::toLower(command).find("retroarch.exe") != std::string::npos)
687				command = Utils::String::replace(command, "%NETPLAY%", "--host --port " + SystemConf::getInstance()->get("global.netplay.port") + " --nick " + SystemConf::getInstance()->get("global.netplay.nickname"));
688			else
689	#endif
690	#if ROCKNIX
691				command = Utils::String::replace(command, "%NETPLAY%", "--host --port " + Utils::String::shellQuote(SystemConf::getInstance()->get("global.netplay.port")) + " --nick " + Utils::String::shellQuote(SystemConf::getInstance()->get("global.netplay.nickname"))); // fork #275
692	#else
693				command = Utils::String::replace(command, "%NETPLAY%", "-netplaymode host");
694	#endif
695		}
696		else
697			command = Utils::String::replace(command, "%NETPLAY%", "");
698	
699		int monitorId = Settings::getInstance()->getInt("MonitorID");
700		if (monitorId >= 0 && command.find(" -system ") != std::string::npos)
701			command = command + " -monitor " + std::to_string(monitorId);
702	
703		if (SaveStateRepository::isEnabled(this))
704		{
705			if (options.saveStateInfo == nullptr)
706			{
707				if (getCurrentGameSetting("autosave") == "1")
708					options.saveStateInfo = system->getSaveStateRepository()->getGameAutoSave(this);
709				else
710					options.saveStateInfo = SaveStateRepository::getEmptySaveState();
711			}
712	
713			command = options.saveStateInfo->setupSaveState(this, command);		
714		}
715	
716		// The pair the emulator will actually be handed, read from the finished
717		// command (fork #21 R5): a savestate config's rewrite above and the netplay
718		// client override both diverge from getEmulator()/getCore().
719		options.launchedEmulator = launchArgument(command, "--emulator", emulator);
720		options.launchedCore = launchArgument(command, "--core", core);
721	
722		return command;
723	}
```

### `es-app/src/FileData.cpp:763-1328`

```cpp
763	// The launch a STOP IT AND PLAY leads to, on the next frame: the dialog or
764	// spinner that asked is off the stack first, and the launch effect and the
765	// emulator take the screen from the view, as a press on the game would.
766	//
767	// A save state chosen in the manager is carried by its file (options.
768	// saveStateFile, rememberSaveState) and found again here, when the launch
769	// runs: the repository's refresh -- the manager's jobs call it as they land
770	// -- deletes every state object, and a launch deferred behind a gate held a
771	// copy of the pointer for as long as the gate took (#308 8-es-menus-and-
772	// core claude F-ES-11). A state gone by then is not handed over: the game
773	// starts as it would with none chosen, and the log says so.
774	static void launchNow(Window* window, FileData* game, const LaunchGameOptions& options)
775	{
776		window->postToUiThread([game, options]
777		{
778			LaunchGameOptions now = options;
779			if (!now.saveStateFile.empty())
780			{
781				now.saveStateInfo = nullptr;
782				if (SaveStateRepository::isEnabled(game))
783					for (auto* state : game->getSourceFileData()->getSystem()->getSaveStateRepository()->getSaveStates(game))
784						if (state->fileName == now.saveStateFile)
785						{
786							now.saveStateInfo = state;
787							break;
788						}
789				if (now.saveStateInfo == nullptr)
790					LOG(LogWarning) << "launch: the save state chosen before the wait is gone (" << now.saveStateFile << "); the game starts without it";
791			}
792			ViewController::get()->launch(game, now);
793		});
794	}
795	
796	// The save state the launch was handed, by its file, while the pointer is
797	// the repository's live object (launchNow finds it again by it). The three
798	// shared states -- none, the auto-save, a new game -- are never deleted and
799	// need no name.
800	static void rememberSaveState(FileData* game, LaunchGameOptions& options)
801	{
802		options.saveStateFile.clear();
803		SaveState* state = options.saveStateInfo;
804		if (state == nullptr || !SaveStateRepository::isEnabled(game))
805			return;
806		SaveStateRepository* repo = game->getSourceFileData()->getSystem()->getSaveStateRepository();
807		if (state == SaveStateRepository::getEmptySaveState() || state == repo->getDefaultAutoSaveSaveState() || state == repo->getDefaultNewGameSaveState())
808			return;
809		options.saveStateFile = state->fileName;
810	}
811	
812	// Wait behind a spinner for a sync or transfer that has been told to stop,
813	// then launch (D-CLOUD-129). stillRunning is asked every 50 ms; hardStop,
814	// when given, is sent once at five seconds for an rclone slow to act on
815	// SIGTERM; at twenty the wait gives up and says so -- a run that will not
816	// die is not one to start a game over (cancelForLaunch's rule, on a longer
817	// leash and behind a spinner rather than a frozen menu).
818	static void launchWhenGone(Window* window, FileData* game, const LaunchGameOptions& options,
819		const std::function<bool()>& stillRunning, const std::function<void()>& hardStop)
820	{
821		window->pushGui(new GuiLoading<bool>(window, _("STOPPING IT SO YOU CAN PLAY..."),
822			[stillRunning, hardStop](IGuiLoadingHandler*)
823			{
824				const auto started = std::chrono::steady_clock::now();
825				bool hard = false;
826				while (stillRunning())
827				{
828					const long ms = (long) std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - started).count();
829					if (ms >= 20000)
830						return false;
831					if (!hard && ms >= 5000 && hardStop != nullptr)
832					{
833						hardStop();
834						hard = true;
835					}
836					std::this_thread::sleep_for(std::chrono::milliseconds(50));
837				}
838				return true;
839			},
840			[window, game, options](bool gone)
841			{
842				if (!gone)
843				{
844					LOG(LogWarning) << "launch: the sync or transfer did not stop within 20 s; the game was not started";
845					window->pushGui(new GuiMsgBox(window, _("IT DIDN'T STOP IN TIME. TRY AGAIN IN A MOMENT.")));
846					return;
847				}
848				launchNow(window, game, options);
849			}));
850	}
851	
852	// The last game's saves still being recorded (the capture in launchGame, on
853	// a thread of its own since fork #290; audit #307 PL-061): true when the
854	// launch may go on now. Bookkeeping with no network, so no question
855	// (D-UI-095): the launch waits for it. Most captures are done within a
856	// moment, and a moment is waited for here, on this thread, so a spinner
857	// does not flash (es-ui-style-guide.md, Waiting). A longer one is waited
858	// for behind the spinner, bounded.
859	//
860	// At the bound the launch is refused and says why (audit of the fixes, E2
861	// gpt G-E2-03): it used to start anyway, under the capture it was waiting
862	// on, and every later launch skipped the same capture -- the overlap the
863	// gate exists to prevent, only later. A capture is local hashing of one
864	// game's saves and ends in a second or two; one still running after ten
865	// is stalled, and the next press waits for it again. Only a capture so old
866	// it is hung (CaptureHungSeconds) stops holding the device, with a warning:
867	// a player kept from every game for bookkeeping is the worse failure.
868	//
869	// The exit sync is the gate's to decide while a launch waits (claude
870	// G-E2-06): a launch that goes owns it -- the generation moves at the
871	// moment it goes, so the capture's post leaves the sync to that game's
872	// exit and the player is not asked about a sync that started while they
873	// waited -- and a launch refused at the bound leaves it to the capture,
874	// whose post runs it when the capture ends. The generation used to move as
875	// the spinner went up, before the launch was certain.
876	static bool captureGate(Window* window, FileData* game, const LaunchGameOptions& options)
877	{
878		const unsigned capturing = sCaptureInFlight.load();
879		if (capturing == 0)
880			return true;
881		if (captureAgeSeconds() >= CaptureHungSeconds)
882		{
883			LOG(LogWarning) << "launch: the last game's capture has run " << captureAgeSeconds() << " s and is taken as hung; the game starts";
884			return true;
885		}
886	
887		const auto started = std::chrono::steady_clock::now();
888		while (sCaptureInFlight.load() == capturing && std::chrono::steady_clock::now() - started < std::chrono::milliseconds(300))
889			std::this_thread::sleep_for(std::chrono::milliseconds(20));
890		if (sCaptureInFlight.load() != capturing)
891		{
892			LOG(LogInfo) << "launch: the last game's saves were recorded first";
893			return true;
894		}
895	
896		LOG(LogInfo) << "launch: waiting for the last game's saves to be recorded";
897		sCaptureWaitedOn = capturing;
898		window->pushGui(new GuiLoading<bool>(window, _("RECORDING YOUR LAST GAME'S SAVES..."),
899			[capturing](IGuiLoadingHandler*)
900			{
901				const auto waited = std::chrono::steady_clock::now();
902				while (sCaptureInFlight.load() == capturing)
903				{
904					if (std::chrono::steady_clock::now() - waited >= std::chrono::seconds(10))
905						return false;
906					std::this_thread::sleep_for(std::chrono::milliseconds(50));
907				}
908				return true;
909			},
910			[window, game, options, capturing](bool)
911			{
912				// Decided by the capture itself, not the wait's answer: one that
913				// ended as the bound came has ended.
914				if (sCaptureInFlight.load() == capturing)
915				{
916					sCaptureWaitedOn = 0;
917					LOG(LogWarning) << "launch: the last game's capture did not finish within 10 s; the game was not started";
918					window->pushGui(new GuiMsgBox(window, _("YOUR LAST GAME'S SAVES ARE STILL BEING RECORDED. TRY AGAIN IN A MOMENT.")));
919					return;
920				}
921				++sExitGeneration;
922				sCaptureWaitedOn = 0;
923				launchNow(window, game, options);
924			}));
925		return false;
926	}
927	
928	bool FileData::launchGame(Window* window, LaunchGameOptions options)
929	{
930		LOG(LogInfo) << "Attempting to launch game...";
931	
932		// PLAY NOW's answer is for the launch it leads to and no other (#308
933		// 8-es-menus-and-core claude F-ES-07): taken here, on the way in,
934		// whether or not the send is still running. It was taken only where the
935		// send was, so a send that ended between the press and the relaunch left
936		// it set, and a later launch over a later send asked nothing. A relaunch
937		// that meets another question first asks the send's again after it.
938		const bool playThroughSend = sPlayThroughSend.exchange(false);
939		rememberSaveState(this, options);
940	
941		// Not while saves are moving -- unless the sync is one EmulationStation
942		// started on its own. A cloud sync reads and writes the same save files
943		// the emulator is about to open, and the archive step tars up /storage
944		// while it runs: starting a game in the middle of that can upload a
945		// half-written save or restore over one the game has already loaded.
946		//
947		// The startup sync and the after-a-game sync run without a press. From
948		// #101 (maintainer, 2026-09-09) a launch cancelled them on its own --
949		// picking a game was the choice -- and since 2026-09-16 (D-CLOUD-130)
950		// it asks first, like every other sync: the maintainer met the exit
951		// sync's stop as "it told me it was stopping so I couldn't play" and
952		// wants one behaviour for every sync or transfer a launch would
953		// interrupt. Stopping is safe because the scripts are rclone copy --
954		// each file written under a temporary name and renamed when complete,
955		// nothing deleted -- so a copy cut short leaves no partial file and the
956		// next run finishes it; the wait for the process to be gone is what
957		// keeps a rename from landing after the emulator has the save open.
958		// Before #101 only the network wait could be cancelled (fork #94), and a
959		// transfer that had lost its link was refused for as long as rclone's
960		// own timeouts let it run (#103).
961		//
962		// A sync the player asked for, and a back up, restore or match they
963		// started on the transfer page (fork #187, D-CLOUD-113; while that page
964		// could be left with the run going, before D-UI-078), used to refuse
965		// the launch outright: theirs to wait for.
966		// Maintainer, 2026-09-15, having met the refusal on the RG SP: "We
967		// should say for the user, would you like to cancel and play, or would
968		// you like to stop the sync or continue ... If it shows a modal anyways
969		// when the sync is in progress and someone tries to start the new game,
970		// we might as well give them the option as to whether they'd like to
971		// cancel or keep waiting." So each is a question with two answers
972		// (D-CLOUD-129), and since D-CLOUD-130 the automatic syncs ask the same
973		// question: "If we want consistent behavior on how user-started syncs or
974		// transfers deal with a potential interruption by a game launch, we
975		// should have a consistent behavior."
976		// STOP IT AND PLAY sends the run's process group SIGTERM,
977		// waits behind a spinner for it to be gone -- the automatic sync's wait,
978		// for the same reason: a rename must not land under a game that has the
979		// save open -- and then launches through ViewController, launch effect
980		// and all; KEEP WAITING (B as well) leaves it running. Stopping is safe
981		// for the reason the automatic cancel is: the scripts are rclone copy,
982		// each file renamed into place whole, so the next run finishes what this
983		// one did not, and a match's deletions stop where they are. The run's
984		// outcome reads SKIPPED - YOU STARTED A GAME, as the card's does.
985		//
986		// One question for any sync on the card, whoever started it. STOP IT AND
987		// PLAY cancels it (cancelForLaunch with the player's answer, which sends
988		// the group SIGTERM and waits its two seconds) and launches; a sync slow
989		// to die is waited for behind the spinner rather than refused.
990		if (!captureGate(window, this, options))
991			return false;
992	
993		if (ThreadedCloudSync::isRunning())
994		{
995			window->pushGui(new GuiMsgBox(window,
996				_("YOUR SAVES ARE SYNCING WITH THE CLOUD.") + "\n\n" + _("IF YOU STOP IT, THE NEXT SYNC FINISHES WHAT THIS ONE DID NOT."),
997				_("STOP IT AND PLAY"), [this, window, options]
998				{
999					LOG(LogInfo) << "launch: the player chose to stop the sync for a game";
1000					ThreadedCloudSync::CancelRefusal again = ThreadedCloudSync::CancelRefusal::Stopping;
1001					if (ThreadedCloudSync::cancelForLaunch(&again, true) || !ThreadedCloudSync::isRunning())
1002						launchNow(window, this, options);
1003					else
1004						launchWhenGone(window, this, options, [] { return ThreadedCloudSync::isRunning(); }, nullptr);
1005				},
1006				_("KEEP WAITING"), nullptr));
1007			return false;
1008		}
1009	
1010		if (const std::shared_ptr<CloudTransferJob> transfer = CloudTransferJob::current(); transfer != nullptr && !transfer->finished())
1011		{
1012			window->pushGui(new GuiMsgBox(window,
1013				GuiCloudTransfer::stillRunningSentence(transfer) + "\n\n" + _("IF YOU STOP IT, WHAT IT HAS NOT MOVED YET WAITS FOR THE NEXT RUN."),
1014				_("STOP IT AND PLAY"), [this, window, options]
1015				{
1016					LOG(LogInfo) << "launch: the player chose to stop the transfer for a game";
1017					CloudTransferJob::stopForLaunch(false);
1018					launchWhenGone(window, this, options, [] { return CloudTransferJob::running(); }, [] { CloudTransferJob::stopForLaunch(true); });
1019				},
1020				_("KEEP WAITING"), nullptr));
1021			return false;
1022		}
1023	
1024		// The offline achievements' two jobs ask the same question (fork #293,
1025		// D-UI-095). The send is the proxy's and cannot be stopped from here,
1026		// so its question offers to play through it: PLAY NOW launches at once
1027		// and the proxy goes on sending behind the game. The top-up can be
1028		// stopped: STOP IT AND PLAY signals the ctl and waits for it to be
1029		// gone, and the ctl runs again next time the device is connected. The
1030		// safe verb is last in both (D-UI-096).
1031		if (ProxyCards::sendRunning() && !playThroughSend)
1032		{
1033			window->pushGui(new GuiMsgBox(window,
1034				_("OFFLINE ACHIEVEMENTS ARE BEING SENT.") + "\n\n" + _("IT'LL BE A MOMENT."),
1035				_("PLAY NOW"), [this, window, options]
1036				{
1037					LOG(LogInfo) << "launch: the player chose to play through the send";
1038					sPlayThroughSend = true;
1039					launchNow(window, this, options);
1040				},
1041				_("KEEP WAITING"), nullptr));
1042			return false;
1043		}
1044	
1045		if (ProxyCards::topUpRunning())
1046		{
1047			window->pushGui(new GuiMsgBox(window,
1048				_("YOUR OFFLINE ACHIEVEMENTS ARE BEING UPDATED.") + "\n\n" + _("IF YOU STOP IT, IT'LL TRY AGAIN NEXT TIME YOU'RE CONNECTED."),
1049				_("STOP IT AND PLAY"), [this, window, options]
1050				{
1051					LOG(LogInfo) << "launch: the player chose to stop the top-up for a game";
1052					ProxyCards::stopTopUp();
1053					launchWhenGone(window, this, options, [] { return ProxyCards::topUpRunning(); }, nullptr);
1054				},
1055				_("KEEP WAITING"), nullptr));
1056			return false;
1057		}
1058	
1059		FileData* gameToUpdate = getSourceFileData();
1060		if (gameToUpdate == nullptr)
1061			return false;
1062	
1063		SystemData* system = gameToUpdate->getSystem();
1064		if (system == nullptr)
1065			return false;
1066	
1067		std::string command = getlaunchCommand(options);
1068		if (command.empty())
1069			return false;
1070	
1071		AudioManager::getInstance()->deinit();
1072		VolumeControl::getInstance()->deinit();
1073	
1074		bool hideWindow = Settings::getInstance()->getBool("HideWindow");
1075		window->deinit(hideWindow);
1076	
1077	#if defined(__GLIBC__)
1078		// Renderer teardown frees large heaps which glibc may keep mapped.
1079		// Return those pages before the emulator needs memory (distro #310).
1080		malloc_trim(0);
1081	#endif
1082		
1083		const std::string rom = Utils::FileSystem::getEscapedPath(getPath());
1084		const std::string basename = Utils::FileSystem::getStem(getPath());
1085	
1086		Scripting::fireEvent("game-start", rom, basename, getName());
1087	
1088		time_t tstart = time(NULL);
1089	
1090		LOG(LogInfo) << "	" << Utils::String::maskSecrets(command);
1091	
1092		auto p2kConv = convertP2kFile();
1093	
1094		mRunningGame = gameToUpdate;
1095		sGamesStarted++;
1096	
1097		// Pause watchers before game launch
1098		WatchersManager::pause();
1099	
1100		ProcessStartInfo process(command);
1101		process.window = hideWindow ? NULL : window;
1102		
1103		int exitCode = process.run();
1104		
1105		// Resume watchers when returning to ES
1106		WatchersManager::resume();
1107		
1108		if (exitCode != 0)
1109			LOG(LogWarning) << "...launch terminated with nonzero exit code " << exitCode << "!";
1110	
1111		mRunningGame = nullptr;
1112	
1113		Utils::FileSystem::FileSystemCache::reset();
1114	
1115		if (SaveStateRepository::isEnabled(this))
1116		{
1117			if (options.saveStateInfo != nullptr)
1118				options.saveStateInfo->onGameEnded(this);
1119	
1120			getSourceFileData()->getSystem()->getSaveStateRepository()->refresh();
1121		}
1122	
1123		// Record what this session wrote (fork #21 R5). On every exit: whatever
1124		// the exit code, whatever the cloud toggle says, whether or not another
1125		// sync holds the lock -- a save written and not recorded is exactly what
1126		// the reconciler cannot explain later. Network-free, takes no lock and
1127		// spawns no rclone: a handful of stats and at most a few hundred KB of
1128		// hashing. It ran here, synchronously, while the window was still down,
1129		// and on the RG35XX SP that was three seconds of nothing on screen
1130		// between the emulator's exit and the interface's first frame (fork
1131		// #290); the command is built here and run below, on the worker that
1132		// then starts the exit sync, so it still finishes before the sync
1133		// starts and the manifest the push carries is current. The paths are
1134		// read here, after onGameEnded above, which renumbers slot files
1135		// and restores .state.auto -- the paths only settle there. The emulator
1136		// and core are the ones the command carried (launchedEmulator/
1137		// launchedCore), never getEmulator()/getCore() re-read now. --started is
1138		// tstart: a member with no entry is recorded only if this session wrote
1139		// it, so nothing stamps a file it did not write. A system with no
1140		// <emulators> element (tools, imageviewer) reaches here with an empty
1141		// pair; nothing there writes a save, so there is nothing to record and
1142		// no failure to stamp -- an empty --emulator would otherwise be a usage
1143		// row in capture-failures on every run of such a system.
1144		std::string capture;
1145		if (Utils::FileSystem::exists("/usr/bin/cloud_capture") && !options.launchedEmulator.empty())
1146		{
1147			capture = std::string("/usr/bin/cloud_capture")
1148				+ " --system "   + Utils::String::shellQuote(system->getName())
1149				+ " --rom "      + Utils::String::shellQuote(gameToUpdate->getPath())
1150				+ " --emulator " + Utils::String::shellQuote(options.launchedEmulator)
1151				+ " --core "     + Utils::String::shellQuote(options.launchedCore)
1152				+ " --started "  + std::to_string(static_cast<long long>(tstart))
1153				+ " --exit "     + std::to_string(exitCode);
1154		}
1155	
1156		// What the display did with this game's frame, for its captures (fork
1157		// #245, D-UI-081): the core's rotation request is in the launch log
1158		// only while the log is this session's, so it is read here. Only after a
1159		// session that ran: a launch that failed before RetroArch's banner (a
1160		// missing core, a bad ROM) exits non-zero, and its log is the previous
1161		// game's section or no banner at all -- recordAfterSession then wrote
1162		// that game's turn, or 0, as this game's own, from=own-launch (#308
1163		// 8-es claude F-ES-08). A crash after a real session keeps the record it
1164		// had. CaptureRotation checks the rest: the log's age against the
1165		// launch, and no record from a log with no launch in it.
1166		if (exitCode == 0)
1167			CaptureRotation::recordAfterSession(gameToUpdate, options.launchedEmulator, tstart);
1168		else
1169			LOG(LogInfo) << "capture rotation: not recorded, the launch exited " << exitCode;
1170	
1171		if (!p2kConv.empty()) // delete .keys file if it has been converted from p2k
1172			Utils::FileSystem::removeFile(p2kConv);
1173	
1174		Scripting::fireEvent("game-end");
1175	
1176		if (!hideWindow && Settings::getInstance()->getBool("HideWindowFullReinit"))
1177		{
1178			ResourceManager::getInstance()->reloadAll();
1179			window->deinit();
1180			window->init();
1181			window->setCustomSplashScreen(gameToUpdate->getImagePath(), gameToUpdate->getName(), gameToUpdate);
1182		}
1183		else
1184			window->init(hideWindow);
1185		
1186		VolumeControl::getInstance()->init();
1187		AudioManager::getInstance()->init();
1188	
1189		window->normalizeNextUpdate();
1190	
1191		//update number of times the game has been launched
1192		if (exitCode == 0)
1193		{
1194			int timesPlayed = gameToUpdate->getMetadata().getInt(MetaDataId::PlayCount) + 1;
1195			gameToUpdate->setMetadata(MetaDataId::PlayCount, std::to_string(static_cast<long long>(timesPlayed)));
1196	
1197			// How long have you played that game? (more than 10 seconds, otherwise
1198			// you might have experienced a loading problem)
1199			time_t tend = time(NULL);
1200			long elapsedSeconds = difftime(tend, tstart);
1201			long gameTime = gameToUpdate->getMetadata().getInt(MetaDataId::GameTime) + elapsedSeconds;
1202			if (elapsedSeconds >= 10)
1203				gameToUpdate->setMetadata(MetaDataId::GameTime, std::to_string(static_cast<long>(gameTime)));
1204	
1205			//update last played time
1206			gameToUpdate->setMetadata(MetaDataId::LastPlayed, Utils::Time::DateTime(Utils::Time::now()));
1207			CollectionSystemManager::get()->refreshCollectionSystems(gameToUpdate);
1208			saveToGamelistRecovery(gameToUpdate);
1209		}
1210	
1211		window->reactivateGui();
1212	
1213	#if defined(__GLIBC__)
1214		// Resource reload also leaves temporary heap pages behind. Release
1215		// them once the interface is ready, rather than accumulating them.
1216		malloc_trim(0);
1217	#endif
1218	
1219		// A screenshot taken in this session is in a folder the viewer scanned
1220		// at boot. Re-read the folders that changed, once the launch has fully
1221		// unwound (#82; the rescan may delete this very FileData when the game
1222		// was an image in the viewer).
1223		window->postToUiThread([] { SystemData::rescanChangedFolders(); });
1224	
1225		// Sync saves to the cloud, visibly.
1226		//
1227		// This was an OS event hook -- /usr/bin/scripts/game-end/, run by the
1228		// fireEvent above -- which backgrounded cloud_backup with its output sent
1229		// to /dev/null. It worked, and no player could ever tell: a silent
1230		// background job that a reboot kills looks exactly like one that never
1231		// started, and the first question after exiting a game is whether the save
1232		// is safe. Running it here puts the answer on the progress card and leaves
1233		// the outcome on it, which is what every other cloud operation does.
1234		//
1235		// It replaces the hook rather than joining it. The hook had no caller but
1236		// this line, so there is nothing else to keep working -- and two paths to
1237		// one operation is what the cloud menu was just collapsed to avoid.
1238		//
1239		// Not gated on exitCode: an emulator that crashed may still have written a
1240		// save, and that is the copy most worth having.
1241		//
1242		// --saves-only --recent: the after-every-game job is the saves this
1243		// session touched, pushed now. The system-settings archive is the
1244		// occasional job and has its own row. Comparing every save on the device
1245		// against the cloud was 18 seconds of somebody's time to move nothing,
1246		// most of it remote round trips that had nothing to do with the game
1247		// just played. With no network, cloud_backup answers
1248		// CloudExit::NoNetwork at once rather than waiting for a probe to time
1249		// out.
1250		//
1251		// The capture first, then the sync, both off the interface thread (fork
1252		// #290): the window is back and drawing before either starts, where the
1253		// capture used to run before the window came back and the RG35XX SP
1254		// showed nothing for its three seconds. The sync card is created on the
1255		// interface thread, so the worker posts it there once the capture is
1256		// done. A game launched and left in between owns the outcome: the loop
1257		// that runs posted tasks does not turn while a game runs, so this task
1258		// runs only after that game's exit, when that exit's own task is the
1259		// one to act -- its --recent run carries this session's saves as well.
1260		const bool exitSync = SystemConf::getInstance()->get("cloudsaves.gameexit") == "1"
1261			&& Utils::FileSystem::exists("/usr/bin/cloud_backup");
1262		const unsigned generation = ++sExitGeneration;
1263		if (!capture.empty())
1264		{
1265			sCaptureStartedMs = steadyMs();
1266			sCaptureInFlight = generation;   // before the thread, so a launch on the next frame sees it
1267		}
1268		std::thread([window, capture, exitSync, generation]
1269		{
1270			bool captureFailed = false;
1271			if (!capture.empty())
1272			{
1273				const int captureCode = ApiSystem::executeScriptLegacy(capture, nullptr).second;
1274				if (captureCode != 0)
1275				{
1276					LOG(LogWarning) << "cloud_capture exited " << captureCode << " -- see /var/log/cloud_sync.log and /storage/.cache/cloud_sync/capture-failures";
1277					captureFailed = true;
1278				}
1279				// Only this exit's: a later exit's capture owns the slot now.
1280				unsigned mine = generation;
1281				sCaptureInFlight.compare_exchange_strong(mine, 0);
1282			}
1283			AppWindow::post(window, [window, exitSync, generation, captureFailed]
1284			{
1285				// A capture that could not record says so once, as a toast, in
1286				// the player's words (fork #293 item 3, D-UI-095): what did not
1287				// happen and what is in place. Said before the sync card starts,
1288				// so it shows after the card (D-UI-093 puts a toast's words back
1289				// on the queue when a card takes the screen). And said whether or
1290				// not another game has been launched since: a later game makes
1291				// this exit's sync its own, not this capture's failure (#308
1292				// 8a-es-app gpt F-ES-05; the check below returned before it).
1293				if (captureFailed)
1294					window->displayNotificationMessage(_U("\uF0C2  ") + _("COULDN'T RECORD THIS SESSION'S SAVES. THEY'RE STILL ON THIS DEVICE."));
1295				if (generation != sExitGeneration.load() || mRunningGame != nullptr)
1296				{
1297					LOG(LogInfo) << "exit: another game was launched since; its exit syncs";
1298					return;
1299				}
1300				// A launch is waiting on this capture behind the spinner: if it
1301				// goes it owns the sync, as above; it can only be refused while
1302				// the capture runs, and this capture has ended (captureGate).
1303				if (sCaptureWaitedOn.load() == generation)
1304				{
1305					LOG(LogInfo) << "exit: a launch waited for this capture; its game's exit syncs";
1306					return;
1307				}
1308				if (exitSync && !ThreadedCloudSync::isRunning())
1309				{
1310					ThreadedCloudSync::start(window, "/usr/bin/cloud_backup --yes --saves-only --recent --automatic",
1311						_("SYNC SAVES"), _("SYNCING SAVES TO THE CLOUD"), ThreadedCloudSync::Origin::Exit);
1312				}
1313				// Nothing else is said at exit (fork #292, D-RA-030): the offline
1314				// achievements go up when RetroAchievements answers, with a card
1315				// of their own on the link's return (ProxyCards).
1316			});
1317		}).detach();
1318	
1319		if (system != nullptr && system->getTheme() != nullptr)
1320			AudioManager::getInstance()->changePlaylist(system->getTheme(), true);
1321		else
1322			AudioManager::getInstance()->playRandomMusic();
1323	
1324		if (exitCode >= 200 && exitCode <= 300)
1325			window->pushGui(new GuiMsgBox(window, _("AN ERROR OCCURRED") + ":\r\n" + getMessageFromExitCode(exitCode), _("OK"), nullptr, GuiMsgBoxIcon::ICON_ERROR));
1326	
1327		return exitCode == 0;
1328	}
```

### `es-app/src/FileData.cpp:1386-1507`

```cpp
1386	std::set<std::string> FileData::getContentFiles()
1387	{
1388		std::set<std::string> files;
1389	
1390		if (mPath.empty())
1391			return files;
1392	
1393		if (Utils::FileSystem::isDirectory(mPath))
1394		{
1395			for (auto file : Utils::FileSystem::getDirContent(mPath, true, true))
1396				files.insert(file);
1397		}
1398		else if (hasContentFiles())
1399		{
1400			auto path = Utils::FileSystem::getParent(mPath);
1401			auto ext = Utils::String::toLower(Utils::FileSystem::getExtension(mPath));
1402	
1403			if (ext == ".cue")
1404			{
1405				std::string start = "FILE";
1406	
1407				std::ifstream cue(WINSTRINGW(mPath));
1408				if (cue && cue.is_open())
1409				{
1410					std::string line;
1411					while (std::getline(cue, line))
1412					{
1413						if (!Utils::String::startsWith(line, start))
1414							continue;
1415	
1416						auto tokens = getTokens(line);
1417						if (tokens.size() > 1)
1418							files.insert(path + "/" + tokens[1]);
1419					}
1420	
1421					cue.close();
1422				}
1423			}
1424			else if (ext == ".ccd")
1425			{
1426				std::string stem = Utils::FileSystem::getStem(mPath);
1427				files.insert(path + "/" + stem + ".cue");
1428				files.insert(path + "/" + stem + ".img");
1429				files.insert(path + "/" + stem + ".bin");
1430				files.insert(path + "/" + stem + ".sub");
1431			}
1432			else if (ext == ".m3u" || ext == ".xbox360")
1433			{
1434				std::ifstream m3u(WINSTRINGW(mPath));
1435				if (m3u && m3u.is_open())
1436				{
1437					std::string line;
1438					while (std::getline(m3u, line))
1439					{
1440						auto trim = Utils::String::trim(line);
1441						if (trim.empty() || trim[0] == '#')
1442							continue;
1443	
1444						trim = Utils::String::replace(trim, "\\", "/");
1445	
1446						if (Utils::FileSystem::isAbsolute(trim))
1447							files.insert(Utils::FileSystem::getGenericPath(trim));
1448						else if (trim[0] == '/')
1449							continue;
1450						else
1451							files.insert(Utils::FileSystem::getCanonicalPath(path + "/" + trim));
1452					}
1453	
1454					m3u.close();
1455				}
1456			}
1457			else if (ext == ".gdi")
1458			{
1459				std::ifstream gdi(WINSTRINGW(mPath));
1460				if (gdi && gdi.is_open())
1461				{
1462					std::string line;
1463					while (std::getline(gdi, line))
1464					{
1465						auto tokens = getTokens(line);
1466						if (tokens.size() > 5 && tokens[4].find(".") != std::string::npos)
1467							files.insert(path + "/" + tokens[4]);
1468					}
1469	
1470					gdi.close();
1471				}			
1472			}
1473		}
1474	
1475		return files;
1476	}
1477	
1478	void FileData::deleteGameFiles()
1479	{
1480		if (mType != FileType::GAME)
1481			return;
1482	
1483		std::string path = getPath();
1484		if (path.empty() || getSystemEnvData()->mStartPath == path)
1485			return;
1486	
1487		for (auto mdd : mMetadata.getMDD())
1488		{
1489			if (mMetadata.getType(mdd.id) != MetaDataType::MD_PATH)
1490				continue;
1491	
1492			std::string path = mMetadata.get(mdd.id);
1493			if (Utils::FileSystem::exists(path) && !Utils::FileSystem::isDirectory(path))
1494				Utils::FileSystem::removeFile(mMetadata.get(mdd.id));
1495		}
1496	
1497		if (Utils::FileSystem::isDirectory(path))
1498		{
1499			Utils::FileSystem::deleteDirectoryFiles(path, true);
1500			return;
1501		}
1502	
1503		Utils::FileSystem::removeFile(path);
1504	
1505		for (auto contentFile : getContentFiles())
1506			Utils::FileSystem::removeFile(contentFile);
1507	}
```

### `es-app/src/views/ViewController.cpp:476-671`

```cpp
476	bool ViewController::doLaunchGame(FileData* game, LaunchGameOptions options)
477	{
478		if (mCurrentView) mCurrentView->onHide();
479	
480		// Silence TTS when launching a game
481		TextToSpeech::getInstance()->say(" ");
482	
483		if (game->launchGame(mWindow, options))
484			if (game->getSourceFileData()->getSystemName() == "windows_installers")
485				return true;
486	
487		return false;
488	}
489	
490	bool ViewController::checkLaunchOptions(FileData* game, LaunchGameOptions options, Vector3f center)
491	{
492	#ifdef _RPI_
493		if (Settings::getInstance()->getBool("VideoOmxPlayer") && mCurrentView)
494			mCurrentView->onHide();
495	#endif
496	
497		if (!game->isExtensionCompatible())
498		{
499			auto gui = new GuiMsgBox(mWindow, _("WARNING: THE EMULATOR/CORE CURRENTLY SET DOES NOT SUPPORT THIS GAME'S FILE FORMAT.\nDO YOU WANT TO LAUNCH IT ANYWAY?"),
500				_("YES"), [this, game, options, center] { launch(game, options, center, false); },
501				_("NO"), nullptr, ICON_ERROR);
502	
503			mWindow->pushGui(gui);
504			return false;
505		}
506	
507		if (Settings::getInstance()->getBool("CheckBiosesAtLaunch") && ApiSystem::getInstance()->isScriptingSupported(ApiSystem::ScriptId::BIOSINFORMATION))
508		{
509			auto bios = ApiSystem::getInstance()->getBiosInformations(game->getSourceFileData()->getSystem()->getName());
510			if (bios.size() != 0)
511			{
512				auto systemName = game->getSystem()->getName();
513				auto it = std::find_if(bios.cbegin(), bios.cend(), [&systemName](const BiosSystem& x) { return x.name == systemName; });
514				if (it != bios.cend() && it->bios.size() > 0)
515				{
516					bool hasMissing = std::find_if(it->bios.cbegin(), it->bios.cend(), [&systemName](const BiosFile& x) { return x.status == "MISSING"; }) != it->bios.cend();
517					if (hasMissing)
518					{
519						auto gui = new GuiMsgBox(mWindow, _("WARNING: THE SYSTEM HAS MISSING BIOS FILE(S) AND THE GAME MAY NOT WORK CORRECTLY.\nDO YOU WANT TO LAUNCH IT ANYWAY?"),
520							_("YES"), [this, game, options, center] { launch(game, options, center, false); },
521							_("NO"), nullptr, ICON_ERROR);
522	
523						mWindow->pushGui(gui);
524						return false;
525					}
526				}
527			}
528		}
529	
530		return true;
531	}
532	
533	void ViewController::launch(FileData* game, LaunchGameOptions options, Vector3f center, bool allowCheckLaunchOptions)
534	{
535		if (allowCheckLaunchOptions && !checkLaunchOptions(game, options, center))
536			return;
537	
538		if(game->getType() != GAME)
539		{
540			LOG(LogError) << "tried to launch something that isn't a game";
541			return;
542		}
543	
544		if (game->getSourceFileData()->getSystem()->hasPlatformId(PlatformIds::IMAGEVIEWER))
545		{
546			auto ext = Utils::String::toLower(Utils::FileSystem::getExtension(game->getPath()));
547	
548			if (Utils::FileSystem::isVideo(game->getPath()))
549				GuiVideoViewer::playVideo(mWindow, game->getPath());
550			else if (ext == ".pdf")
551				GuiImageViewer::showPdf(mWindow, game->getPath());
552			else if (ext == ".cbz")
553				GuiImageViewer::showCbz(mWindow, game->getPath());
554			else if (!Utils::FileSystem::isAudio(game->getPath()))
555			{
556				auto gameImage = game->getImagePath();
557				if (Utils::FileSystem::exists(gameImage))
558				{
559					auto imgViewer = new GuiImageViewer(mWindow);
560	
561					for (auto sibling : game->getParent()->getChildrenListToDisplay())
562						imgViewer->add(sibling->getImagePath());
563	
564					imgViewer->setCursor(gameImage);
565					mWindow->pushGui(imgViewer);
566				}
567			}
568			return;
569		}
570	
571		if (!SystemConf::getInstance()->getBool("global.netplay") || ApiSystem::getInstance()->getIpAddress() == "NOT CONNECTED" || !game->isNetplaySupported())
572			options.netPlayMode = DISABLED;
573		else if (options.netPlayMode == DISABLED && Settings::getInstance()->getBool("NetPlayAutomaticallyCreateLobby"))
574			options.netPlayMode = SERVER;
575		
576		Transform4x4f origCamera = mCamera;
577		origCamera.translation() = -mCurrentView->getPosition();
578	
579		center += mCurrentView->getPosition();
580		stopAnimation(1); // make sure the fade in isn't still playing
581		mWindow->stopNotificationPopups(); // make sure we disable any existing info popup
582		mLockInput = true;
583	
584		GuiComponent::isLaunchTransitionRunning = true;
585			
586		if (!Settings::getInstance()->getBool("HideWindow"))
587			mWindow->setCustomSplashScreen(game->getImagePath(), game->getName(), game);
588	
589		std::string transition_style = Settings::GameTransitionStyle();
590		if (transition_style.empty() || transition_style == "auto")
591			transition_style = Settings::TransitionStyle();
592		
593		if (Settings::PowerSaverMode() == "instant")
594			transition_style = "instant";
595	
596		if(transition_style == "auto")
597			transition_style = "fast slide";
598	
599		if (Settings::PowerSaverMode() == "instant")
600			transition_style = "instant";
601	
602		if (transition_style == "fade & slide")
603			transition_style = "slide";
604	
605		// Workaround, the grid scale has problems when sliding giving bad effects
606		//if (transition_style == "slide" && mCurrentView->isKindOf<GridGameListView>())
607			//transition_style = "fade";
608	
609		if (transition_style == "fade" || transition_style == "fast fade")
610		{
611			int fadeDuration = (transition_style == "fast fade") ? 400 : 800; // Halve the duration for fast fade
612			// fade out, launch game, fade back in
613			auto fadeFunc = [this](float t) { mFadeOpacity = Math::lerp(0.0f, 1.0f, t); };
614	
615			setAnimation(new LambdaAnimation(fadeFunc, fadeDuration), 0, [this, game, fadeFunc, options]
616			{
617				if (doLaunchGame(game, options))
618				{
619					GuiComponent::isLaunchTransitionRunning = false;
620	
621					Window* w = mWindow;
622					mWindow->postToUiThread([w]() { reloadAllGames(w, false); });
623				}
624				else
625				{
626					setAnimation(new LambdaAnimation(fadeFunc, 800), 0, [this] { GuiComponent::isLaunchTransitionRunning = false; mLockInput = false; mWindow->closeSplashScreen(); }, true, 3);
627					this->onFileChanged(game, FILE_METADATA_CHANGED);
628				}
629			});
630		} 
631		else if (transition_style == "slide" || transition_style == "fast slide")
632		{
633			int slideDuration = (transition_style == "fast slide") ? 750 : 1500; // Halve the duration for fast slide
634			// move camera to zoom in on center + fade out, launch game, come back in
635			setAnimation(new LaunchAnimation(mCamera, mFadeOpacity, center, slideDuration), 0, [this, origCamera, center, game, options]
636			{			
637				if (doLaunchGame(game, options))
638				{
639					GuiComponent::isLaunchTransitionRunning = false;
640	
641					Window* w = mWindow;
642					mWindow->postToUiThread([w]() { reloadAllGames(w, false); });
643				}
644				else
645				{
646					mCamera = origCamera;
647					setAnimation(new LaunchAnimation(mCamera, mFadeOpacity, center, 600), 0, [this] { GuiComponent::isLaunchTransitionRunning = false; mLockInput = false; mWindow->closeSplashScreen(); }, true, 3);
648					this->onFileChanged(game, FILE_METADATA_CHANGED);
649				}
650			});
651		} 
652		else // instant
653		{			
654			setAnimation(new LaunchAnimation(mCamera, mFadeOpacity, center, 10), 0, [this, origCamera, center, game, options]
655			{			
656				if (doLaunchGame(game, options))
657				{
658					GuiComponent::isLaunchTransitionRunning = false;
659	
660					Window* w = mWindow;
661					mWindow->postToUiThread([w]() { reloadAllGames(w, false); });
662				}
663				else
664				{
665					mCamera = origCamera;
666					setAnimation(new LaunchAnimation(mCamera, mFadeOpacity, center, 10), 0, [this] { GuiComponent::isLaunchTransitionRunning = false; mLockInput = false; mWindow->closeSplashScreen(); }, true, 3);
667					this->onFileChanged(game, FILE_METADATA_CHANGED);
668				}
669			});
670		}
671	}
```

### `es-app/src/SaveState.cpp:52-199`

```cpp
52	std::string SaveState::setupSaveState(FileData* game, const std::string& command)
53	{
54		if (game == nullptr)
55			return command;
56	
57		std::string cmd = command;
58	
59		// Savestate has core information ? Setup correct emulator/core
60		if (slot >= -1 && this->config != nullptr && !config->isActiveConfig(game) && !racommands)
61		{
62			cmd = _changeCommandlineArgument(cmd, "-emulator", config->emulator);
63			cmd = _changeCommandlineArgument(cmd, "-core", config->core);
64		}	
65	
66		bool supportsIncremental = config != nullptr ? config->incremental : game->getSourceFileData()->getSystem()->getSaveStateRepository()->supportsIncrementalSaveStates();
67	
68		bool incrementalSaveStates = SystemConf::getIncrementalSaveStates() && /*hasAutosave && */supportsIncremental;
69	
70		std::string path = Utils::FileSystem::getParent(fileName);
71	
72		if (slot == -1) // Run current AutoSave
73		{
74			if (racommands || fileName.empty())
75				cmd = cmd + " -autosave 1 -state_slot " + std::to_string(slot);
76			else
77				cmd = cmd + " -autosave 1 -state_file \"" + fileName + "\"";
78		}
79		else
80		{
81			if (slot == -2) // Run new game without AutoSave
82			{
83				cmd = cmd + " -autosave 0";
84			}
85			else if (incrementalSaveStates)
86			{
87				if (racommands)
88				{
89					cmd = cmd + " -state_slot " + std::to_string(slot); // slot
90	
91					// Run game, and activate AutoSave to load it
92					if (!fileName.empty())
93						cmd = cmd + " -autosave 1";
94				}
95				else
96				  if (!fileName.empty())
97				    cmd = cmd + " -state_slot " + std::to_string(slot) + " -state_file \"" + fileName + "\"";
98			}
99			else
100			{
101				if (racommands)
102				{
103					cmd = cmd + " -state_slot " + std::to_string(slot);
104	
105					// Run game, and activate AutoSave to load it
106					if (!fileName.empty())
107						cmd = cmd + " -autosave 1";
108				}
109				else
110				  if (!fileName.empty())
111				    cmd = cmd + " -state_slot " + std::to_string(slot) + " -state_file \"" + fileName + "\"";
112			}
113	
114			if (racommands) 
115			{
116				// Copy to state.auto file
117				auto autoFilename = makeStateFilename(-1);
118				if (Utils::FileSystem::exists(autoFilename))
119				{
120					Utils::FileSystem::removeFile(autoFilename + ".bak");
121					Utils::FileSystem::renameFile(autoFilename, autoFilename + ".bak");
122				}
123	
124				// Copy to state.auto.png file
125				auto autoImage = autoFilename + ".png";
126				if (Utils::FileSystem::exists(autoImage))
127				{
128					Utils::FileSystem::removeFile(autoImage + ".bak");
129					Utils::FileSystem::renameFile(autoImage, autoImage + ".bak");
130				}
131	
132				mAutoImageBackup = autoImage;
133				mAutoFileBackup = autoFilename;
134	
135				if (!fileName.empty())
136				{
137					Utils::FileSystem::copyFile(fileName, autoFilename);
138	
139					// Copy file to new slot, if the users want to reload the saved game in the slot directly from retroach
140					//
141					// Only when that slot is another file. Batocera's no-next-slot
142					// patch (D-UI-057) changed the target from the next free slot
143					// to the launched one, so this named the launched state
144					// itself: removeFile deleted it and the copy from it then
145					// failed -- the player's state was gone, with only the .auto
146					// copy above left (#308 F-CS-14). With no free-slot target
147					// left there is nothing for it to copy, and onGameEnded's
148					// check below finds no mNewSlotFile.
149					const std::string newSlotFile = makeStateFilename(slot);
150					if (incrementalSaveStates && Utils::FileSystem::getGenericPath(newSlotFile) != Utils::FileSystem::getGenericPath(fileName))
151					{
152						mNewSlotFile = newSlotFile;
153						Utils::FileSystem::removeFile(mNewSlotFile);
154						if (Utils::FileSystem::copyFile(fileName, mNewSlotFile))
155							mNewSlotCheckSum = ApiSystem::getInstance()->getMD5(fileName, false);
156					}
157				}
158			}
159		}
160	
161		return cmd;
162	}
163	
164	void SaveState::onGameEnded(FileData* game)
165	{
166		if (racommands)
167		{
168			if (slot < 0)
169				return;
170	
171			if (!mNewSlotCheckSum.empty() && Utils::FileSystem::exists(mNewSlotFile))
172			{
173				// Check if the file in the slot has changed. If it's the same, then delete it & clear the slot
174				auto fileChecksum = ApiSystem::getInstance()->getMD5(mNewSlotFile, false);
175				if (fileChecksum == mNewSlotCheckSum)
176					Utils::FileSystem::removeFile(mNewSlotFile);
177			}
178	
179			if (!mAutoFileBackup.empty())
180			{
181				Utils::FileSystem::removeFile(mAutoFileBackup);
182				Utils::FileSystem::renameFile(mAutoFileBackup + ".bak", mAutoFileBackup);
183			}
184	
185			if (!mAutoImageBackup.empty())
186			{
187				Utils::FileSystem::removeFile(mAutoImageBackup);
188				Utils::FileSystem::renameFile(mAutoImageBackup + ".bak", mAutoImageBackup);
189			}
190		}
191	
192		// No renumbering after a session (D-UI-069, maintainer 2026-09-16): a
193		// slot's number never changes once written. Upstream closes the gaps a
194		// deletion leaves by renaming every slot above it, which the save sync
195		// reads as a deletion plus a new file -- a re-upload, a delete the
196		// player never made, and on a second device a conflict out of nothing.
197		// Gaps stay; the tiles show dates, and RetroArch's auto-increment saves
198		// to the highest slot plus one whatever lies below.
199	}
```

### `es-app/src/SystemData.cpp:378-512`

```cpp
378	void SystemData::rescanIfFolderChanged()
379	{
380		if (mRootFolder == nullptr || mIsCollectionSystem || !mIsGameSystem || Settings::ParseGamelistOnly())
381			return;
382		if (Utils::FileSystem::exists(getGamelistPath(false)))
383			return;
384	
385		const time_t mtime = Utils::FileSystem::getFileModificationDate(mEnvData->mStartPath).getTime();
386		if (mtime == mFolderScannedAt)
387			return;
388	
389		// Not while something else walks these files from a thread of its own
390		// (the index's and the scraper's queues hold FileData*, and a file that
391		// left the folder is deleted here), nor under a running game. The
392		// folder's time is not recorded, so the next exit or restore re-reads it.
393		if (ThreadedHasher::isRunning() || ThreadedScraper::isRunning() || FileData::GetRunningGame() != nullptr)
394		{
395			LOG(LogInfo) << "SystemData::rescanIfFolderChanged: " << getName() << " changed on disk; not re-read while the index, the scraper or a game holds its files";
396			return;
397		}
398	
399		LOG(LogInfo) << "SystemData::rescanIfFolderChanged: " << getName() << " changed on disk, re-reading " << mEnvData->mStartPath;
400		mFolderScannedAt = mtime;
401	
402		// The views that show these files first, while their cursors are files
403		// that exist: this system's, and its group's when it is grouped, which
404		// shows the same pointers (fork #246). Each is made again below, found by
405		// path. The group's only if it had one: the player may never have opened it.
406		SystemData* group = isGroupChildSystem() ? getParentGroupSystem() : nullptr;
407		std::string cursorPath, groupCursorPath;
408		bool wasCurrent = false, groupWasCurrent = false, groupHadView = false;
409		if (ViewController::get() != nullptr)
410		{
411			cursorPath = ViewController::get()->dropGameListView(this, &wasCurrent);
412			if (group != nullptr && ViewController::get()->getGameListView(group, false) != nullptr)
413			{
414				groupHadView = true;
415				groupCursorPath = ViewController::get()->dropGameListView(group, &groupWasCurrent);
416			}
417		}
418	
419		// A group system shows its grouped child's top level through a folder of
420		// its own (createGroupedSystems) holding the same pointers without owning
421		// them; deeper entries are reached through folders both share.
422		FolderData* groupFolder = nullptr;
423		if (group != nullptr && group->getRootFolder() != nullptr)
424			for (auto* child : group->getRootFolder()->getChildren())
425				if (child->getType() == FOLDER && child->getSystem() == this && ((FolderData*)child)->isVirtualStorage())
426				{
427					groupFolder = (FolderData*)child;
428					break;
429				}
430	
431		FolderData* fresh = new FolderData(mEnvData->mStartPath, this);
432		std::unordered_map<std::string, FileData*> fileMap;
433		fileMap[mEnvData->mStartPath] = fresh;
434		populateFolder(fresh, fileMap);
435	
436		// The merge's view of FileData (FolderMerge). A class local to this
437		// member, so it reaches FolderData's children the way SystemData does.
438		struct Tree
439		{
440			SystemData* system;
441			FolderData* root;
442			FolderData* groupFolder;
443			int vanishedCount;
444			int arrivedCount;
445	
446			std::vector<FileData*> children(FileData* folder) { return ((FolderData*)folder)->getChildren(); }
447			std::string key(FileData* n) { return n->getPath(); }
448			bool isFolder(FileData* n) { return n->getType() == FOLDER; }
449			void detach(FileData* folder, FileData* n) { ((FolderData*)folder)->removeChild(n); }
450			void attach(FileData* folder, FileData* n)
451			{
452				((FolderData*)folder)->addChild(n);
453				if (folder == root && groupFolder != nullptr)
454					groupFolder->mChildren.push_back(n);
455			}
456			void vanished(FileData* n)
457			{
458				vanishedCount++;
459				std::vector<FileData*> games;
460				if (n->getType() == GAME)
461					games.push_back(n);
462				else
463					games = ((FolderData*)n)->getFilesRecursive(GAME);
464				for (auto* game : games)
465					dropCollectionEntries(game);
466				if (groupFolder != nullptr && n->getParent() == root)
467				{
468					auto& held = groupFolder->mChildren;
469					held.erase(std::remove(held.begin(), held.end(), n), held.end());
470				}
471				// Out of its folder and the index (~FileData), and a folder's own
472				// files with it (~FolderData).
473				delete n;
474			}
475			void arrived(FileData* n)
476			{
477				arrivedCount++;
478				if (n->getType() == GAME)
479					system->addToIndex(n);
480				else
481					for (auto* game : ((FolderData*)n)->getFilesRecursive(GAME))
482						system->addToIndex(game);
483			}
484		};
485		Tree tree{ this, mRootFolder, groupFolder, 0, 0 };
486		FolderMerge::merge<FileData>(mRootFolder, fresh, tree);
487	
488		// What is left in the fresh tree is the twin of a kept file, never
489		// indexed and never shown. The index is set aside while they go, or each
490		// one's destructor would take its twin's count out of it.
491		FileFilterIndex* index = mFilterIndex;
492		mFilterIndex = nullptr;
493		delete fresh;
494		mFilterIndex = index;
495	
496		LOG(LogInfo) << "SystemData::rescanIfFolderChanged: " << getName() << " " << tree.vanishedCount << " gone, " << tree.arrivedCount << " new";
497	
498		// Which game a screenshot belongs to is cached by content name, misses
499		// included, and built from the library once (DisplayAspect): a library
500		// that changed makes both wrong -- a screenshot looked at before its ROM
501		// arrived kept its file's proportions (#308 8-es claude F-ES-15, 8a gpt
502		// F-ES-09).
503		if (tree.vanishedCount > 0 || tree.arrivedCount > 0)
504			DisplayAspect::forgetScreenshots();
505	
506		if (ViewController::get() != nullptr)
507		{
508			ViewController::get()->remakeGameListView(this, cursorPath, wasCurrent);
509			if (groupHadView)
510				ViewController::get()->remakeGameListView(group, groupCursorPath, groupWasCurrent);
511		}
512	}
```

### `es-app/src/SystemData.cpp:620-650`

```cpp
620					continue;
621	
622				// Hardcoded optimisation : vpinball 'roms' subfolder must be excluded
623				if (mMetadata.name == "vpinball" && fn == "roms")
624					continue;			
625	
626				// Skip ports folders, as many folders in ports causes slow down at startup
627				if (fileInfo.path.rfind("ports") != std::string::npos)
628					continue;
629	
630				// Skip windows folder for the same reason as ports folder
631				if (fileInfo.path.rfind("windows") != std::string::npos)
632					continue;
633	
634				FolderData* newFolder = new FolderData(filePath, this);
635				populateFolder(newFolder, fileMap);
636	
637				//ignore folders that do not contain games
638				if(newFolder->getChildren().size() == 0)
639					delete newFolder;
640				else 
641				{
642					const std::string& key = newFolder->getPath();
643					if (fileMap.find(key) == fileMap.end())
644					{
645						folder->addChild(newFolder);
646						fileMap[key] = newFolder;
647					}
648				}
649			}
650		}
```

### `es-app/src/SystemData.cpp:1024-1095`

```cpp
1024	void SystemData::loadAdditionnalConfig(pugi::xml_node& srcSystems)
1025	{	
1026		std::vector<std::string> rootPaths = { Paths::getUserEmulationStationPath(), Paths::getEmulationStationPath() };
1027		for (auto rootPath : VectorHelper::distinct(rootPaths, [](auto x) { return x; }))
1028		{
1029			for (auto customPath : Utils::FileSystem::getDirContent(rootPath, false, false))
1030			{
1031				if (Utils::FileSystem::getExtension(customPath) != ".cfg")
1032					continue;
1033	
1034				if (!Utils::String::startsWith(Utils::FileSystem::getFileName(customPath), "es_systems_"))
1035					continue;
1036	
1037				pugi::xml_document doc;
1038				pugi::xml_parse_result res = doc.load_file(WINSTRINGW(customPath).c_str());
1039				if (!res)
1040				{
1041					LOG(LogError) << "Could not parse " << Utils::FileSystem::getFileName(customPath) << " file!";
1042					return;
1043				}
1044	
1045				pugi::xml_node systemList = doc.child("systemList");
1046				if (!systemList)
1047				{
1048					LOG(LogError) << Utils::FileSystem::getFileName(customPath) << " is missing the <systemList> tag !";
1049					return;
1050				}
1051	
1052				for (pugi::xml_node system = systemList.child("system"); system; system = system.next_sibling("system"))
1053				{
1054					if (!system.child("name"))
1055						continue;
1056	
1057					std::string name = system.child("name").text().get();
1058					if (name.empty())
1059						continue;
1060	
1061					bool found = false;
1062	
1063					// Remove existing one
1064					for (pugi::xml_node& srcSystem : srcSystems.children())
1065					{
1066						if (std::string(srcSystem.name()) != "system")
1067							continue;
1068	
1069						std::string srcName = srcSystem.child("name").text().get();
1070						if (srcName != name)
1071							continue;
1072	
1073						found = true;
1074	
1075						for (pugi::xml_node& child : system.children())
1076						{
1077							std::string tag = child.name();
1078							if (tag == "name")
1079								continue;
1080	
1081							srcSystem.remove_child(tag.c_str());
1082	
1083							if (tag == "emulators" || !std::string(child.text().get()).empty())
1084								srcSystem.append_copy(child);
1085						}
1086	
1087						break;
1088					}
1089	
1090					if (!found)
1091						srcSystems.append_copy(system);
1092				}
1093			}
1094		}
1095	}
```

### `es-app/src/SystemData.cpp:1937-1941`

```cpp
1937	void SystemData::setSortId(const unsigned int sortId)
1938	{
1939		mSortId = sortId;
1940		Settings::getInstance()->setInt(getName() + ".sort", mSortId);
1941	}
```

### `es-app/src/LaunchCommand.h:1-57`

```cpp
1	#pragma once
2	#ifndef ES_APP_LAUNCH_COMMAND_H
3	#define ES_APP_LAUNCH_COMMAND_H
4	
5	#include <string>
6	
7	#include "utils/CommandLineUtil.h"
8	
9	// Readers for a finished launch command (fork #21 R5). The save manifest
10	// records exactly what the emulator was handed, so these never re-resolve
11	// anything from SystemConf. Shared by FileData::getlaunchCommand (the
12	// ordinary launch) and launchStartupGame in main.cpp (the boot game, whose
13	// command is stored and replayed before any system is loaded, so the
14	// stored string is the only source).
15	//
16	// A token is a whole shell word of the command -- the words
17	// Utils::CommandLine::replaceOptionValue reads when a save state swaps the
18	// core, so the two agree -- and the last such word wins, as it does there.
19	// It was the last occurrence of the letters anywhere in the line, and a
20	// netplay nick is the player's own text, one quoted word: 'Bob -Pro'
21	// recorded the system as ro (#308 8-es-menus-and-core claude F-ES-20).
22	// runemu.sh still reads ${ARGUMENTS##*-P}, which does find it there; that
23	// is the launcher's to change (es-app/tests/unit/LaunchCommandTests.cpp).
24	
25	// The value of the last word that begins with `prefix` ("-P" ->
26	// the system name), to the end of that word; "" when the command carries
27	// none.
28	inline std::string launchToken(const std::string& command, const std::string& prefix)
29	{
30		std::string value;
31		size_t i = 0;
32		while (i < command.size())
33		{
34			if (command[i] == ' ' || command[i] == '\t')
35			{
36				i++;
37				continue;
38			}
39			const size_t end = Utils::CommandLine::wordEnd(command, i);
40			if (command.compare(i, prefix.size(), prefix) == 0)
41				value = command.substr(i + prefix.size(), end - i - prefix.size());
42			i = end;
43		}
44		return value;
45	}
46	
47	// The value of a "--key=" word: a ROM path or a --controllers= blob holding
48	// the literal is part of another word and cannot win.
49	// `fallback` covers a per-system customCommandLine with no such token
50	// (config/emulators/tools.conf is "%RUNCOMMAND%").
51	inline std::string launchArgument(const std::string& command, const std::string& key, const std::string& fallback)
52	{
53		std::string value = launchToken(command, key + "=");
54		return value.empty() ? fallback : value;
55	}
56	
57	#endif // ES_APP_LAUNCH_COMMAND_H
```

### `es-app/src/main.cpp:527-572`

```cpp
527	void launchStartupGame()
528	{
529		auto gamePath = SystemConf::getInstance()->get("global.bootgame.path");
530		if (gamePath.empty() || !Utils::FileSystem::exists(gamePath))
531			return;
532		
533		auto command = SystemConf::getInstance()->get("global.bootgame.cmd");
534		if (!command.empty())
535		{
536			InputManager::getInstance()->init();
537			command = Utils::String::replace(command, "%CONTROLLERSCONFIG%", InputManager::getInstance()->configureEmulators());
538	
539			time_t tstart = time(NULL);
540			int exitCode = Utils::Platform::ProcessStartInfo(command).run();
541	
542			// A boot-launched session is a game exit too (fork #21 R5), and the
543			// one FileData::launchGame never sees: a save it wrote has no entry
544			// and an mtime below every later session's --started, so unless it is
545			// recorded here nothing ever records it. No system is loaded yet
546			// (loadSystemConfigFile runs later in main), so the stored command is
547			// the only source -- the -P token is the system, --emulator=/--core=
548			// the frozen pair, read the way runemu.sh reads them. A command with
549			// no emulator token has nothing that writes a save (tools), so there
550			// is nothing to record.
551			std::string system = launchToken(command, "-P");
552			std::string emulator = launchArgument(command, "--emulator", "");
553			if (Utils::FileSystem::exists("/usr/bin/cloud_capture") && !system.empty() && !emulator.empty())
554			{
555				std::string capture = std::string("/usr/bin/cloud_capture")
556					+ " --system "   + Utils::String::shellQuote(system)
557					+ " --rom "      + Utils::String::shellQuote(gamePath)
558					+ " --emulator " + Utils::String::shellQuote(emulator)
559					+ " --core "     + Utils::String::shellQuote(launchArgument(command, "--core", ""))
560					+ " --started "  + std::to_string(static_cast<long long>(tstart))
561					+ " --exit "     + std::to_string(exitCode);
562				int captureCode = ApiSystem::executeScriptLegacy(capture, nullptr).second;
563				if (captureCode != 0)
564				{
565					LOG(LogWarning) << "cloud_capture exited " << captureCode << " after the startup game -- see /var/log/cloud_sync.log and /storage/.cache/cloud_sync/capture-failures";
566					// Said once the window exists (fork #293 item 3): this runs
567					// before the window is created.
568					sStartupCaptureFailed = true;
569				}
570			}
571		}
572	}
```

### `es-app/src/SaveStateBookkeeper.cpp:106-206`

```cpp
106		// The transfer lock, taken for the deletion (gpt's coverage note on
107		// PL-068, audit of the fixes, E2): transferGone asks whether the lock
108		// is held and the deletion followed, so a transfer that started between
109		// the answer and the deletion ran beside it. Held, the lock turns the
110		// question and the act into one: a transfer that starts meanwhile finds
111		// it taken, and the scripts give a busy lock a second -- longer than a
112		// retire and an unlink. Exclusive and non-blocking, as the scripts take
113		// it; created when no transfer has made it yet. Released when this goes.
114		std::atomic<bool> gHoldsTransferLock{ false };
115	
116		struct TransferLock
117		{
118			int fd = -1;
119			bool take()
120			{
121	#if defined(_WIN32)
122				return true;   // no transfer scripts, no lock (isFlockHeld's own answer there)
123	#else
124				fd = ::open(CLOUD_SYNC_LOCK_PATH, O_RDWR | O_CREAT | O_CLOEXEC, 0644);
125				if (fd < 0)
126					return false;
127				int r;
128				do
129					r = ::flock(fd, LOCK_EX | LOCK_NB);
130				while (r != 0 && errno == EINTR);
131				if (r == 0)
132				{
133					gHoldsTransferLock = true;
134					return true;
135				}
136				::close(fd);
137				fd = -1;
138				return false;
139	#endif
140			}
141			~TransferLock()
142			{
143	#if !defined(_WIN32)
144				if (fd >= 0)
145				{
146					gHoldsTransferLock = false;
147					::close(fd);   // and the lock with it
148				}
149	#endif
150			}
151		};
152	
153		void runDelete(Worker* w, const SaveStateJob& job)
154		{
155			// Asked, then taken: a transfer that took the lock between the two
156			// sends the deletion back to waiting for it; a lock that cannot be
157			// taken at all fails closed, as isFlockHeld does -- it waits.
158			TransferLock held;
159			for (;;)
160			{
161				if (!transferGone(w, job))
162					return;
163				if (held.take())
164					break;
165				LOG(LogInfo) << "save state deletion waits: the transfer lock was taken as the deletion began (" << job.stateFile << ")";
166				std::this_thread::sleep_for(std::chrono::milliseconds(200));
167				std::unique_lock<std::mutex> lock(w->mutex);
168				if (w->stop)
169				{
170					LOG(LogWarning) << "save state deletion not made at exit: the transfer lock could not be taken; " << job.stateFile << " stays";
171					return;
172				}
173			}
174	
175			// Record the deletion before the file goes (#21 R3, D-CLOUD-053): the
176			// next pass then propagates a decided deletion instead of asking about
177			// an absence it cannot explain (D-CLOUD-037). With --unlink the script
178			// takes the files too, once the row is on disk, and it ignores SIGTERM
179			// while it runs, so the two cannot be split by a stop (D-CLOUD-133).
180			if (Utils::FileSystem::exists(CAPTURE))
181			{
182				std::string retire = std::string(CAPTURE) + " --retire --unlink " + Utils::String::shellQuote(job.stateFile);
183				if (!job.screenshot.empty())
184					retire += " " + Utils::String::shellQuote(job.screenshot);
185	
186				int code = ApiSystem::executeScriptLegacy(retire, nullptr).second;
187				if (code != 0)
188					LOG(LogWarning) << "cloud_capture --retire --unlink exited " << code << " -- see /var/log/cloud_sync.log and /storage/.cache/cloud_sync/capture-failures";
189			}
190	
191			// Whatever the script did or did not do -- absent on an image without
192			// it, a usage error, a card gone -- the deletion the player asked for
193			// proceeds: anything still there goes now.
194			if (Utils::FileSystem::exists(job.stateFile, false))
195				Utils::FileSystem::removeFile(job.stateFile);
196			if (!job.screenshot.empty() && Utils::FileSystem::exists(job.screenshot, false))
197				Utils::FileSystem::removeFile(job.screenshot);
198	
199			// The line says what is on disk, not what was asked: a file the
200			// unlink was refused (immutable, a card gone read-only) is still
201			// there, and the manager's compare (#207) puts its tile back.
202			if (Utils::FileSystem::exists(job.stateFile, false))
203				LOG(LogWarning) << "save state deletion did not take: " << job.stateFile << " is still present; the manager shows it again";
204			else
205				LOG(LogInfo) << "save state deleted: " << job.stateFile;
206		}
```

### `es-app/src/ProxyCards.cpp:226-290`

```cpp
226		void runTopUp(Window* window, bool afterIndex)
227		{
228			sTopUpStoppedForGame = false;   // a stop that missed an earlier run is not this run's
229			std::atomic<bool> finished{ false };
230			int rc = -1;
231			const time_t startedAt = time(nullptr);
232			std::thread ctl([&rc, &finished, afterIndex]
233			{
234				rc = OfflineAchievements::runTopUp(afterIndex);
235				finished = true;
236			});
237	
238			AsyncNotificationComponent* card = nullptr;
239			bool sawWork = false;
240			// A card is made on the interface thread and handed back here. When
241			// the loop that runs posted tasks is not turning -- a game has the
242			// screen -- the run goes on without a card, and the lambda, run
243			// later, makes none.
244			auto attach = [window]() -> AsyncNotificationComponent*
245			{
246				// `wanted` is flipped once, by whichever side gets there
247				// first: the lambda, which then makes the card and hands it
248				// over; or this thread on giving up, after which the lambda
249				// makes nothing. A card is never made for nobody.
250				auto made = std::make_shared<std::promise<AsyncNotificationComponent*>>();
251				auto wanted = std::make_shared<std::atomic<bool>>(true);
252				auto got = made->get_future();
253				AppWindow::post(window, [window, made, wanted]
254				{
255					if (!wanted->exchange(false))
256						return;
257					AsyncNotificationComponent* c = window->createAsyncNotificationComponent(true);
258					c->updateTitle(TROPHY + _("RETROACHIEVEMENTS (OFFLINE)"));
259					c->updateText(_("STARTING..."));
260					c->updatePercent(-1);
261					made->set_value(c);
262				});
263				if (got.wait_for(std::chrono::seconds(3)) == std::future_status::ready || !wanted->exchange(false))
264					return got.get();
265				return nullptr;
266			};
267			auto screenFree = []
268			{
269				return !sSendRunning && !ThreadedCloudSync::isRunning() && FileData::GetRunningGame() == nullptr;
270			};
271			while (!finished)
272			{
273				std::this_thread::sleep_for(std::chrono::milliseconds(500));
274				const CloudText::RunningProgress p = OfflineAchievements::runningProgress();
275				if (!p.running)
276					continue;
277				// Every run the ctl makes is worth its card (fork #299, D-UI-103): the
278				// link's return runs only when a game was played since the last
279				// attempt, and the index's run only when it found new games, so a run
280				// that shows is a run with something to look for -- and the card's
281				// words say what it is doing.
282				sawWork = true;
283				if (card == nullptr && screenFree())
284					card = attach();
285				if (card != nullptr && p.total > 0)
286					card->updateText(Utils::String::format(_("GETTING GAME %d OF %d READY...").c_str(), p.index, p.total));
287			}
288			ctl.join();
289			// 143 (TERM) or 130 (INT) is a run that was stopped. The launch's STOP
290			// IT AND PLAY is said below; any other stop -- the toggle turned off,
```

### `es-app/src/ProxyCards.cpp:404-418`

```cpp
404		void waitForTheGame()
405		{
406			long long until = sTopUpHeldUntilMs.load();
407			if (until != 0)
408			{
409				LOG(LogInfo) << "ProxyCards: the top-up was stopped for a game; the next run waits for that game";
410				while (steadyMs() < until && FileData::GetRunningGame() == nullptr && FileData::GetGamesStarted() == sTopUpHeldGames.load())
411					std::this_thread::sleep_for(std::chrono::milliseconds(100));
412				// Started, or it never did in time: spent either way -- unless a
413				// later stop has set a hold of its own meanwhile.
414				sTopUpHeldUntilMs.compare_exchange_strong(until, 0);
415			}
416			while (FileData::GetRunningGame() != nullptr)
417				std::this_thread::sleep_for(std::chrono::seconds(1));
418		}
```

### `es-core/src/Scripting.cpp:88-113`

```cpp
88	    static void executeScript(const std::string& script, const std::string& eventName, const std::string& arg1, const std::string& arg2, const std::string& arg3, bool allowAsync = true)
89	    {
90	        std::string command = script;
91	
92	        if (script.find(" ") != std::string::npos)
93	            command = "\"" + script + "\"";
94	
95	        if (!eventName.empty())
96	            command += " " + eventName;
97	
98	        for (auto arg : { arg1, arg2, arg3 })
99	        {
100	            if (arg.empty())
101	                break;
102	
103	            std::string data = arg;
104	            if (Utils::String::startsWith(data, "\"") && Utils::String::startsWith(data, "\""))
105	                data = Utils::String::replace(data.substr(1, data.size() - 2), "\"", "");
106	
107	            data = Utils::String::replace(data, "\"", "");
108	
109	            if (data.find(" ") != std::string::npos)
110	                command += " \"" + data + "\"";
111	            else
112	                command += " " + data;
113	        }
```
