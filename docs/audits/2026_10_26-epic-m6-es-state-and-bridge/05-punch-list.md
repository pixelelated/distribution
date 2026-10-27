# Punch list — M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

Written by the M6 coordinator (Claude Fable 5.1) from the lane's committed inputs at 14cd564486, under D-WORKFLOW-212, because the lane's harness refused the artifact; the lane runs the lint, files the audit issue and posts the pause.

**Extended depth:** two seats, GPT-6 Astra at `max` (58 items: 54 accepted, 2 in part, 1 rejected in part, 1 plausible), then Gemini 4 Argon at `high` (45 items: 41 accepted, 3 in part, 1 plausible) -- `stage-c/astra-grades.md`, `stage-c/argon-grades.md`. The audit issue is filed by the lane at stage D as a sub-issue of #668; every item below is **Open** until the stage-D ruling.

- **The inputs:** `02` § The leads (L-01 to L-22; the four stage-B closures beneath them are unnumbered) and § Corrections and new leads from the seats (L-23 to L-36), `04` § Risk assessment and § The questions, the two grade tables, `stage-b/positives/` and `stage-c/positives/`, and the guest cycle's G1 to G5.
- **Not items:** the three brief corrections (25 `writeAllText` call sites, the four `wifictl` key lines, `:642` Windows-only); the stage-B closures (`file://`, the server's `format` as a path, the Bluetooth and storage arguments, `maskSecrets`' `--key`); the storage closure as Astra SO-3 re-reasoned it (no producer); #1154 itself, cited -- PL-25 carries its design question to the pause.
- **One item per defect or reusable improvement**, however many sources found it; a seat item the lane rejected is not here. Ordered by severity, L-23 and L-01 first.
- **Severities:** `04` § Risk assessment's for L-01 to L-22; the seats' where they gave one (L-23 High; L-29, L-30, L-33 Low); the coordinator's proposal, marked as such in the item, for L-24 and L-27, which no input graded.
- **Nothing in this list changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. Removals: none; every dead end is a proposal; a change to T1's files (`001-functions`, `wifictl`, `chksysconfig`) lands only by the coordinator's ruling (#648).
- **One guest window,** 22:43:36 to 22:49:29 UTC at 640x480, on an image whose EmulationStation is M7's composition over the pin (`02` § The guest cycle); G6(a) to G6(c) and G7 are `CANNOT` for the slice -- the executor's harness refused the step after G5 and the coordinator dropped the further window (the ruling of 2026-10-27 00:00 UTC); the two G6 walks are the coordinator's to write for the integration window. **Nothing ran on a person's device or cloud.**
- **Lines** are at the ES pin `16dbac5211` and, for the OS files, at `8ebaf8daad`.

---

## PL-01: clearing the HOSTNAME row loses every setting: the row saves an empty value unchecked, `applyChanges` drops the line from the file and the record, and the next boot's `chksysconfig verify` reseeds the image's defaults over both (a `bug` proposed)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q4
- **Family:** a state write that can lose the record
- **Source Finding:** L-23; Astra SO-23 (accepted, and proved further), SO-39 (per-key reset semantics first); Argon SO-14 (accepted, the same chain found independently) -- proved: fixture (`stage-c/positives/hostname-empty.out`, by `hostname-empty.py`: the pin's `SystemConf.cpp` and `AtomicFileUtil.cpp`, `8ebaf8daad`'s `chksysconfig` unrewritten, the host's `grep` standing in for the donor busybox's)
- **Owner area:** es-core/src/SystemConf.cpp `applyChanges`, `recordLastGood` (fork-modified); es-core/src/guis/GuiSettings.cpp `addInputTextConfigRow`'s `updateVal` (the row at `GuiMenu.cpp:9929` is T26's); `chksysconfig:57-62`, `:278-303` (T1's file, read, not changed)
- **What:**
  - **The cause:** the HOSTNAME row saves whatever the popup returns, an empty string included. `applyChanges` treats an empty value as a removal and the line leaves the file (`SystemConf.cpp:386-396`); `recordLastGood` then publishes that file as the record. At the next boot `chksysconfig verify` looks for its sentinel line in both copies (`chksysconfig:57-62`), which the hostname line is: the fixture removes only that line and the reseed follows (`:278-303`, the rsync at `:324`). The interface's next start records the seeded file over the record.
  - **The fixture, step by step:** before, 4 keys in both files; after the empty save, 3 keys and the hostname line ABSENT in both; after `chksysconfig`, the live file 221 keys with `qa.marker` ABSENT while the record still holds 3; after the next start, both files 221 keys and the marker gone from both. **Every setting is lost from both files.**
  - **On the image** the installed `chksysconfig` is byte-identical to `8ebaf8daad`'s (`guest-cycle/g01-image-vs-tree.txt`).
  - **The fix shape:** the row never saves an empty hostname (an empty entry restores the default name, written as `system.hostname=` the way `set_setting system.hostname default` does, or is refused); `applyChanges` keeps a key written with an empty value as `key=` rather than removing the line, with per-key reset semantics (Astra SO-39: a bare rule would delete the hostname default) -- coordinated with PL-10, the read side; and `recordLastGood` refuses to publish as the record a file that has lost a key the record holds, a guard the fork's own recorder can hold. `chksysconfig`'s sentinel is T1's file: a note to the coordinator, not a change here.
- **Can this be done on the VM?** Yes -- the host fixture is the positive: `hostname-empty.py` fails on the pin (step 3 prints `value=[]` and both files reach 221 keys) and passes once the line is kept and the record refuses the loss (`fix-unit-test`); the guest walk (NETWORK SETTINGS > HOSTNAME cleared, a reboot, the page read, a frame at 640x480) is `fix-walk-pending-image`.
- **Already written:** a device where this already happened holds the image's defaults as both its live file and its record; the player's keys are gone from both and the fix can read nothing back -- nothing inherited, argued (the loss is total). A device holding `system.hostname=` on purpose (D-NET-009's `set_setting ... default`) is read both ways: the fixed reader keeps the line and shows the default name (PL-10).
- **Acceptance:**
  - [ ] `stage-c/positives/hostname-empty.py` against the fixed `SystemConf`: after the empty save both files keep the `system.hostname` line, `chksysconfig verify` reseeds nothing (the live file's key count unchanged, `qa.marker` present in both), and the next start reads the player's keys -- the run's output posted beside the pin's, which prints the opposite.
  - [ ] a `SystemConfTests` case: `set("system.hostname", "")` then `saveSystemConf()` leaves `system.hostname=` in the live file and in the record (FAIL on the pin, PASS after, both summary lines posted).
  - [ ] the guest walk on the fixed image: the HOSTNAME row cleared, the guest rebooted, the frame at 640x480 shows the hostname row with the default name and a second row set before the clear unchanged; `system.cfg.backup`'s key count before and after the reboot equal (`fix-walk-pending-image`).
- **Disposition (proposed):** a `bug` (High) filed by the lane at the stage-D ruling; a fix stream on the ES branch (the row, `applyChanges`, the recorder's guard); `chksysconfig`'s sentinel to the coordinator as a note on T1's file (#648).

## PL-02: a ROM's file name reaches `sh` inside double quotes before `7zr` runs, as root, for every `.7z` the scraper hashes; the same shape for poppler over a manual's path (a `bug` proposed)

- **Severity:** High
- **Category:** Security
- **Question:** Q1
- **Family:** a command built from a player's string
- **Source Finding:** L-01; Astra SO-2 (accepted: the reach narrowed), SO-28; Argon SO-1 (accepted: `getMD5` falls through to `unzipFile` and runs `7zr` a second time), SO-2 (a `.m3u`'s first content file is what gets hashed), SO-19 (the `Already written:` line); L-31's `getMD5` half (Astra SO-54, Argon SO-43) -- proved: tree (`ApiSystem.cpp:1527-1528`, `:1578-1579`, `:1659-1660`; `:2509`, `:2593`; the file's own comment `:631-634`); guest (`guest-cycle/g01-identity.txt`: `7z`, `7za`, `7zr`, `pdfinfo` and `pdftoppm` in `/usr/bin`); the constructed positive G6(a) queued for the second window
- **Owner area:** es-app/src/ApiSystem.cpp `getMD5`, `getCRC32`, `unzipFile`, `getPdfPageCount`, `extractPdfImages` (upstream-carried lines; a contained fix, `bugs-are-agent-first.md` rule 6)
- **What:**
  - **The mechanism:** the command is a string, `7zr x -so "` + the file name + `"`, run through `executeEnumerationScript` -> `popen` -> `sh -c` (`:1528`; `:1579` is `7zr l -slt "`; `:1660` is `7zr x "` with the destination quoted the same way). Double quotes leave `$`, backticks and `\` live to the shell, as the comment at `:631-634` says. The file name is the ROM's path under `/storage/roms`: a string the player downloaded. EmulationStation runs as root.
  - **The reach (Astra SO-2):** `ScreenScraper.cpp:306-308` -> `getMD5` for a `.7z` up to 128 MB unless the game has a name override, an existing MD5 above 1 MiB or an empty file, or its system is one of the seven arcade-class platforms `SystemData.cpp:2315-2325` exempts. A `.7z` named in a `.m3u` is reached through the playlist's first content file (`ScreenScraper.cpp:295-303`, Argon SO-2). When the first pipeline's answer is not one line of 32 or more characters, `getMD5` runs `7zr` again through `unzipFile` (`:1538-1543`, Argon SO-1). `7zr` is on the image, so the rows are live code.
  - **The same shape** at `:2509` (`pdfinfo "`) and `:2593` (`pdftoppm -jpeg -r ... "`) over a manual's path.
  - **The companion (L-31's half):** a failed extraction hands `md5sum` empty input and its digest is stored as the game's (`:1527-1530`); `getCRC32`'s empty `CRC = ` entry and its `size_t` subtraction (`:1582-1586`).
  - **The fix shape:** the path reaches `7zr` and poppler without a shell -- an argv executor (`WifiScanProcess`'s `posix_spawnp` model, `GuiWifi.cpp:535-582`) or, where the pipeline stays, `Utils::String::shellQuote` (`StringUtil.cpp:426-444`), the rule `02` § What T26 and the OS slices inherit states; the exit checked; an empty extraction stored as no hash. Never double quotes.
- **Can this be done on the VM?** Yes -- the host: a unit over the command builder as a pure function (`CommandLineTests`' shape) is `fix-unit-test`; the guest: a ROM named with a command substitution in a scratch library and the marker file the substitution would write, G6(a) of the brief's § 5, `CANNOT` for this lane (its harness refuses the step), so the walk is the coordinator's for the integration window (on the pin's binary the marker appears; after the fix it does not) -- `fix-walk-pending-image`. No device.
- **Already written:** the digest of empty input already stored as a game's MD5 in gamelists on devices where an extraction failed (Argon SO-19) -- read both: the fix treats that digest on a non-empty archive as unhashed and hashes again; nothing else inherited (the command's path writes no file).
- **Acceptance:**
  - [ ] the builder's unit: a name carrying `"`, `$`, a backtick and `\` reaches the child as one argument byte for byte, and the pin's string form is shown to split it (FAIL on the pin, PASS after; both lines posted).
  - [ ] G6(a) on the guest: the scrape of the scratch ROM leaves no marker file after the fix, and the same walk on the pin's binary writes it (the coordinator's walk at the integration window, `fix-walk-pending-image`).
  - [ ] a unit: `getMD5` over an archive `7zr` cannot read stores no MD5 (FAIL on the pin, where the empty input's digest is stored).
  - [ ] at the fix's commit `tools/t21-commands.py` reports the double-quotes count down by the five live rows (`:1528`, `:1579`, `:1660`, `:2509`, `:2593`), its `--expect` asserted.
- **Disposition (proposed):** a `bug` (High) filed by the lane at the stage-D ruling; a fix stream on the ES branch; a #585 line (the lines are upstream's).

## PL-03: with `system.cfg` absent, `set_setting` copies the image's seed before the lock and without the record, and the interface's next load records the seed over the player's record (a `bug` proposed)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q4
- **Family:** a state write that can lose the record
- **Source Finding:** L-10; Astra SO-17 (accepted; `chksysconfig` can end with no file when restore, reseed and rsync all fail), SO-18 (the lock protects only cooperating writers); Argon SO-15 -- proved: fixture (`stage-b/positives/shell-writers.out` S1: `8ebaf8daad`'s `001-functions` in bubblewrap with `--clearenv`, the donor's busybox as `/usr/bin`, no path rewritten)
- **Owner area:** `001-functions:540-543`, `:595` (T1's file, #648); es-core/src/SystemConf.cpp:232-238 and es-core/src/utils/AtomicFileUtil.cpp:352-361 (the recorder's side, fork-own)
- **What:**
  - **The cause:** `set_setting` and `set_settings` `cp` the seed over a missing `system.cfg` (`:542`, `:595`) before `wait_lock` and without reading `.backup`. The interface's next load finds a usable live file, takes it, and `recordLastGood` writes it as the record: the player's keys go from both files (S1). D-CLOUD-078's three steps in the wrong order.
  - **Not read:** how often a live file is absent at a `set_setting` after boot (T22's order, #669); `chksysconfig` can leave no file (Astra SO-17).
  - **The fix shape:** the shell seeds under the lock and from the record when one exists (T1's file); and the recorder refuses to publish as the record a live file that is byte-identical to the shipped seed while a differing record exists (the ES half, the fork's own code).
- **Can this be done on the VM?** Yes -- S1 on the host is the positive (`shell-writers.py`, FAIL on `8ebaf8daad`'s `001-functions`); the recorder's half is a `SystemConfTests` case (a seed-identical live file beside a record: the record chosen, nothing recorded over it). `fix-unit-test` both; the boot order on the guest is T22's.
- **Already written:** a device where the seed has already replaced the live file and the record followed holds the image's defaults as both; nothing can bring the keys back -- nothing inherited, argued. The mixed case already on cards (the seed live, the player's record older) is what the recorder's half reads: the record wins and the seed is not recorded (read both).
- **Acceptance:**
  - [ ] `shell-writers.py` S1 against the fixed `001-functions`: with the live file absent and a record present, `set_setting` leaves a live file whose keys are the record's plus the set key (FAIL on `8ebaf8daad`, PASS after).
  - [ ] a `SystemConfTests` case: a live file equal to the seed beside a record with other keys loads the record and records nothing over it (FAIL on the pin, PASS after).
  - [ ] `tools/settings-modes-test` and `tools/last-good-scripts-test` PASS lines after the shell change.
- **Disposition (proposed):** a `bug` (High) filed by the lane; the shell half is T1's file, to the coordinator's ruling (#648); the recorder's half a fix stream on the ES branch.

## PL-04: a download removes the file it will replace before a byte arrives, and is called successful without a whole artifact (a `bug` proposed)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record (L-03); a check whose failure reads as success (L-28)
- **Source Finding:** L-03, L-28; Astra SO-6 (accepted, and narrower: not reached by default), SO-30, SO-51; Argon SO-6 (`ApiSystem::downloadFile` takes the same path), SO-21, SO-42 (`renameFile` removes its destination before the rename) -- proved: tree (`HttpReq.cpp:324-345`, `:361-368`, `:377-378`, `:477-506`; `FileSystemUtil.cpp:1448-1463`; `Scraper.cpp:400`, `:631-635`; `GuiScraperStart.cpp:99`; `Settings.cpp:198`, `:224`; `ApiSystem.cpp:2442-2460`); the guest's 404 positive G6(b) queued
- **Owner area:** es-core/src/HttpReq.cpp (the file-mode download), es-core/src/utils/FileSystemUtil.cpp `renameFile` (upstream-carried); es-app/src/scrapers/Scraper.cpp (the caller, T32's)
- **What:**
  - **The cause:** `:344` removes the target and `:328` opens `<path>.tmp`, one name shared by every request for that path; `closeStream` ignores `fflush`'s and `fclose`'s results; `renameFile` returns true for an absent source (`FileSystemUtil.cpp:1451-1452`) and removes the destination before `std::rename` (`:1454-1455`), so the rename is not atomic either. A download that fails (404 and I/O errors ignored at `Scraper.cpp:631-635`) leaves the game with no art where it had some.
  - **The reach:** with `ScrapeOverWrite` on (`Settings.cpp:198`) and the page's overwrite flag set, which the default filter GAMES MISSING ANY MEDIA clears (`Scraper.cpp:400`, `GuiScraperStart.cpp:99`, `Settings.cpp:224`): a re-scrape under ALL GAMES or MISSING ALL MEDIA; and `downloadFile`'s callers (Argon SO-6).
  - **The fix shape:** the bytes to a unique temporary, `fflush` and `fclose` checked, the artifact positive before the rename, the old file replaced only then (D-CLOUD-078: replace only after you know you succeeded); `renameFile` false for an absent source.
- **Can this be done on the VM?** Yes -- the host: a unit over the file-mode path with a transfer that fails after the open (the old file remains; `fix-unit-test`); the guest: the #1154 endpoint answering 404 under ALL GAMES, the art present before and after (G6(b) of the brief's § 5, `fix-walk-pending-image`).
- **Already written:** games whose art a failed re-scrape removed hold no art; a re-scrape restores it; nothing to migrate. A shared `<path>.tmp` left on a card is not read by the fix's unique names -- argued.
- **Acceptance:**
  - [ ] a unit: with the transfer failing after the open, the old file is byte-identical after the call and `status()` is not `REQ_SUCCESS` (FAIL on the pin: the file is gone).
  - [ ] a unit: `renameFile` of an absent source returns false (FAIL on the pin).
  - [ ] G6(b) on the guest: a 404 for one game's image under ALL GAMES leaves `<stem>-image.<ext>` unchanged by `cmp`, with the game's frame at 640x480 (`fix-walk-pending-image`).
- **Disposition (proposed):** a `bug` (Medium) filed by the lane; a fix stream on the ES branch; a #585 line for `renameFile`.

## PL-05: `system.cfg`, its record and the shipped seed are 0645 on the image with `wifi.key`, `root.password` and the RetroAchievements password inside; `es_settings.cfg` is 0644 with the scraper's pair and account; every writer keeps the mode (a `bug` proposed)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Family:** a credential's sink (a file's mode)
- **Source Finding:** L-21; Astra SO-16 (accepted; the universal claim withdrawn: 0645 survives under a umask of 022), SO-48; Argon SO-11 item 3 (`root.password` and the RetroAchievements password in the same file), SO-12 (both readers and the copies' modes), SO-39 (the existing files are chmodded, not only the seed) -- proved: guest (`guest-cycle/g02-modes.txt`, `g01-image-vs-tree.txt`); tree (`AtomicFileUtil.cpp:115`, `:127-147`; `Settings.cpp:533`, `:629`; `001-functions:385-404`)
- **Owner area:** es-core/src/utils/AtomicFileUtil.cpp, es-core/src/SystemConf.cpp, es-core/src/Settings.cpp (the modes they keep, fork-own); the seed's build step (untraced; a recipe under `projects/`, the coordinator's)
- **What:**
  - **On the image:** `system.cfg` and `.backup` 645; `es_settings.cfg` and `.backup` 644; the seed `/usr/config/system/configs/system.cfg` 645 though git records it `100644` and no recipe `chmod`s it -- the installed seed also differs in content, so a build step rewrites it, and that step's mode is the 0645 (which step is not traced). `AtomicFile::writeText` keeps a replaced file's mode; `prepare_settings_temp` keeps the shared bits less the umask. Only root runs on the image today; the exposure is the card read elsewhere and any unprivileged process to come.
  - **The fix shape:** a store that holds a credential is written 0600 (the fork's writers: `writeText` with an explicit mode for both stores and both records; the shell's #421 contract keeps the narrowed mode); the existing files on `/storage` chmodded once at the interface's start, the live file and the record of each store (Argon SO-12); the seed's build step found and its mode set, under `projects/` (the coordinator's).
- **Can this be done on the VM?** Yes -- the host: `AtomicFileTests` cases for the explicit mode and for the start-time narrowing, `tools/settings-modes-test` for the shell side (`fix-unit-test`); the guest: `stat -c %a` of the four files and the seed after a boot of the fixed image (`fix-walk-pending-image`).
- **Already written:** every upgraded device holds 0645 and 0644 files -- migrated: the fix narrows both copies of both stores once at start, idempotent, before any credential is written again; the seed stays the build's until its step is found.
- **Acceptance:**
  - [ ] a unit: `writeText` replacing a 0645 file with mode 0600 requested leaves 0600 (FAIL on the pin: 0645 kept).
  - [ ] on the guest after the fixed image's first boot, `stat -c %a` of `system.cfg`, `system.cfg.backup`, `es_settings.cfg` and `es_settings.cfg.backup` prints 600 four times (the pin's image prints 645 645 644 644, `g02-modes.txt`).
  - [ ] `tools/settings-modes-test` PASS (the shell keeps 0600 across its writers).
  - [ ] the build step that installs the seed at 0645 named by path and line on the audit issue, with the mode it will write.
- **Disposition (proposed):** a `bug` (Medium) filed by the lane; a fix stream on the ES branch for the writers and the start-time narrowing; the seed's step to the coordinator (a recipe under `projects/`, not this lane's to change).

## PL-06: `wifictl` exits 0 with no Wi-Fi device: a handheld whose driver did not load says CONNECTED and saves the network; `saved`, `disable`, `forget_saved` and `connect_saved` are empty successes; the Bluetooth bulk delete and `setStorage` ignore their results (a `bug` proposed)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q6
- **Family:** a check whose failure reads as success
- **Source Finding:** L-22, L-33; Astra SO-25 (the toast is `joined()`: CONNECTED), SO-26; Argon SO-18 (`disableWifi`, `forget_saved`, `connect_saved` exit 0 with no device; `setStorage`'s result ignored), SO-40 (the device guard for every verb that reports a state) -- proved: guest (`guest-cycle/g03-argv.txt`: the connect exited 0 with `eth0` and `lo` only); tree (`wifictl:55-56`; `ApiSystem.cpp:627-637`, `:687-705`; `GuiWifi.cpp:385-395`, `:403-413`, `:548-569`; `GuiBluetoothDevices.cpp:117-121`; `GuiMenu.cpp:3130-3151`)
- **Owner area:** `wifictl` (T1's file); es-app/src/ApiSystem.cpp `enableWifi`, `getSavedWifiNetworks`; es-app/src/guis/GuiWifi.cpp (fork-own)
- **What:**
  - **The cause:** `wifictl` returns 0 at `:55-56` when it finds no device. `enableWifi` reads `system() == 0` as joined (`:627-637`); the page saves `wifi.ssid` and `wifi.key` and toasts CONNECTED (`:385-395`, `:403-413`). `saved` with no device is an empty success to both readers (`:687-705`, `GuiWifi.cpp:548-569`). Outside the 14: the Bluetooth bulk delete ignores its result (`GuiBluetoothDevices.cpp:117-121`) and `setStorage`'s result is ignored before the reboot flag (`GuiMenu.cpp:3130-3151`, T26's).
  - **The fix shape:** `wifictl` exits non-zero with a reason on every verb that reports a state when it has no device (T1's file); the page asks `wifictl current` after a connect before it says CONNECTED and saves, and reads a no-device exit as its own sentence -- `WI-FI ISN'T AVAILABLE ON THIS DEVICE RIGHT NOW.` proposed, built with the proposed words (D-UI-112), with its French.
- **Can this be done on the VM?** Yes -- the guest has no Wi-Fi adapter, which is the case itself: the page's connect on the fixed image shows the refusal and saves nothing (`fix-walk-pending-image`, a frame at 640x480); the host: `tools/cloud-input-test` drives `wifictl connect` with no device and asserts the exit (`fix-unit-test`).
- **Already written:** a `wifi.ssid`/`wifi.key` pair saved for a network never joined is the same shape a real join saves; the fix reads it as before -- nothing inherited, argued.
- **Acceptance:**
  - [ ] on the guest (no adapter) the fixed page's connect shows the refusal sentence in a frame at 640x480 and `system.cfg` gains no `wifi.ssid` line (the pin's page says CONNECTED, `g03-argv.txt`).
  - [ ] `tools/cloud-input-test`'s case: `wifictl connect`, `saved` and `current` with no device exit non-zero (FAIL on `8ebaf8daad`, PASS after).
  - [ ] the new sentence in `fr.po` with a non-empty msgstr (`tools/es-untranslated --upstream bccd715707` names it in neither list).
- **Disposition (proposed):** a `bug` (Medium) filed by the lane; the script's half is T1's file, to the coordinator's ruling (#648); the page's half a fix stream on the ES branch; the Bluetooth and storage readers recorded for T26 (PL-26).

## PL-07: `header_callback` reads curl's header buffer as if it ended in a NUL; it does not (a `bug` proposed)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q2
- **Family:** a credential's sink (the client every credential travels through)
- **Source Finding:** L-02; Astra SO-5 (accepted: the over-read runs to the next NUL); Argon SO-5 (the trailing bytes are kept in `mResponseHeaders`) -- proved: fixture (`stage-b/positives/lifted.out`: ASan heap-buffer-overflow, READ of size 15 from a 14-byte buffer)
- **Owner area:** es-core/src/HttpReq.cpp:579-594 (upstream-carried; a contained fix, `bugs-are-agent-first.md` rule 6)
- **What:**
  - **The cause:** `:583` builds a `std::string` from the buffer pointer alone; curl passes `size * nitems` and no terminator. The read runs to the next NUL in curl's buffer and the bytes past the header land in `mResponseHeaders`. Every response header of every request.
  - **The fix:** `std::string(buffer, size * nitems)`.
- **Can this be done on the VM?** Yes -- the lifted fixture is the positive (`lifted header` under ASan: the report on the pin's lines, clean after), `fix-unit-test`.
- **Already written:** nothing inherited: memory only.
- **Acceptance:**
  - [ ] `lifted header` under ASan reports no error with the fixed lines (the pin's run reports `heap-buffer-overflow`; both outputs posted).
  - [ ] a header of 14 bytes without a NUL yields a 14-byte entry in `mResponseHeaders`.
- **Disposition (proposed):** a `bug` (Medium) filed by the lane; a one-line fix stream on the ES branch, shared with PL-08 and PL-19; a #585 line.

## PL-08: `CURLINFO_RESPONSE_CODE` is read into an `int`; curl writes a `long`, eight bytes into four, on every completed transfer (a `bug` proposed)

- **Severity:** Medium (the coordinator's proposal for the ruling: the same shape as PL-07, a write past an object's bounds on every transfer; neither seat nor `04` graded it)
- **Category:** Correctness
- **Question:** Q2
- **Family:** a check whose failure reads as success
- **Source Finding:** L-24; Astra SO-50 (accepted); Argon SO-41 (accepted, found independently) -- proved: tree (`HttpReq.cpp:432-433`)
- **Owner area:** es-core/src/HttpReq.cpp `status()` (upstream-carried; a contained fix)
- **What:**
  - **The cause:** `int http_status_code; curl_easy_getinfo(..., CURLINFO_RESPONSE_CODE, &http_status_code)`: curl stores a `long`, 8 bytes on the x86-64 guest and on aarch64 handhelds, through a pointer to 4. Undefined behaviour; what the other four bytes overwrite is the compiler's layout.
  - **The fix:** a `long`, narrowed where the status is used.
- **Can this be done on the VM?** Yes -- the host: the lines lifted with a stub `curl_easy_getinfo` that writes 8 bytes, under ASan (`fix-unit-test`); a `-Wall` compile shows nothing, so the fixture is the proof.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the lifted fixture under ASan reports no stack-buffer-overflow with the fixed lines (the pin's lines report one; both outputs posted).
  - [ ] a 200, a 404 and a 503 still reach their rows of `status()`'s table (a unit over the mapping).
- **Disposition (proposed):** a `bug` (severity to the ruling) filed by the lane; PL-07's stream; a #585 line.

## PL-09: a cut live file newer than its record is merged and saved whole without a record write, and the next load records it over the whole record, the cut keys gone (a `bug` proposed)

- **Severity:** Medium (the coordinator's proposal for the ruling: PL-03's loss on a narrower trigger; neither seat nor `04` graded it)
- **Category:** Correctness
- **Question:** Q4
- **Family:** a state write that can lose the record
- **Source Finding:** L-27; Astra SO-52 (accepted); Argon SO-15 (items 1 to 3) -- proved: tree (`AtomicFileUtil.cpp:343-361`, `:522-539`; `SystemConf.cpp:336-339`)
- **Owner area:** es-core/src/utils/AtomicFileUtil.cpp `chooseConfig`, `saveUnderLock`; es-core/src/SystemConf.cpp (fork-own)
- **What:**
  - **The cause:** `chooseConfig`'s cut-of-record case is mtime-bounded: a cut live file newer than its record that still parses as usable is Live. The save merges the pending changes into it and writes it whole (`SystemConf.cpp:336-339`) with no record write; the next load finds a usable live file and `recordLastGood` publishes it (`AtomicFileUtil.cpp:352-361`): the keys the cut removed are gone from both.
  - **The fix shape:** a live file whose text is a strict prefix of its record's is a recovery whatever its mtime; and a save onto a live file whose key set is a strict subset of the record's re-chooses under the lock before it records.
- **Can this be done on the VM?** Yes -- the host: a `SystemConfTests` case (the record; a cut copy of it touched newer; a `set` and a save; a reload: the record's keys present), FAIL on the pin, `fix-unit-test`; the guest: the G4 walk with the cut file touched newer than the record (`fix-walk-pending-image`).
- **Already written:** a device whose record was overwritten this way holds the cut set as its record -- nothing inherited, argued; a cut live file beside an older record, already on a card, is read by the fixed ladder as the recovery case (read both).
- **Acceptance:**
  - [ ] the unit case above FAILs on the pin and PASSes after, both summary lines posted.
  - [ ] `AtomicFileTests` 24 and `SystemConfTests` 10 + the new cases PASS in the generated build's summary line (`tools/t21-build-tests.sh`).
- **Disposition (proposed):** a `bug` (severity to the ruling) filed by the lane; a fix stream on the ES branch, shared with PL-01's recorder guard.

## PL-10: `SystemConf`'s readers: an empty value reads as the table's default (`system.hostname=` shows BATOCERA), and a reload keeps keys the file no longer holds (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q5
- **Family:** a check whose failure reads as success
- **Source Finding:** L-15, L-26; Astra SO-24 (accepted), SO-39 (per-key semantics with PL-01); Argon SO-11 item 4 -- proved: fixture (`stage-b/positives/state-units.out` U1: `BATOCERA`); guest (`guest-cycle/g05-hostname.txt`, `frames/g05-network-settings.png`); tree (`AtomicFileUtil.cpp:465`; `SystemConf.cpp:44`, `:428-434`, `:73-80`, `:148-179`)
- **Owner area:** es-core/src/utils/AtomicFileUtil.cpp `parseKeyValues`, es-core/src/SystemConf.cpp `loadSystemConf` (fork-own); the readers `GuiMenu.cpp:9909` (T26's) and `ApiSystem.cpp:2917`
- **What:**
  - **The empty value:** `parseKeyValues` drops a line whose value is empty (`:465`), so `get` answers the defaults table: D-NET-009's `set_setting system.hostname default` writes `system.hostname=` and NETWORK SETTINGS > HOSTNAME read **BATOCERA** on the guest.
  - **The reload:** `loadSystemConf` clears `mOnDisk` and the pending sets but not `confMap` (`:148-152`), and the parse only adds; after an open network's join writes `wifi.key=`, the previous network's key stays in the interface's memory. What reads it next is not traced.
  - **The fix shape:** a key present with an empty value is distinct from an absent key, and the hostname row shows the device's actual name for an empty one; `loadSystemConf` clears the map before the parse. Coordinated with PL-01 (the write side) and PL-11.
- **Can this be done on the VM?** Yes -- the host: U1 (`state-fixture parse`, FAIL on the pin) and a `SystemConfTests` case for the reload (`fix-unit-test`); the guest: the G5 frame after the fix shows the device's name (`fix-walk-pending-image`).
- **Already written:** `system.hostname=` on every device D-NET-009 touched -- read both: the fixed reader shows the device's name; no file is rewritten.
- **Acceptance:**
  - [ ] `state-fixture parse` prints an empty value for `system.hostname=` (the pin prints `BATOCERA`, `state-units.out` U1).
  - [ ] a unit: a reload after `wifi.key=` is written leaves `get("wifi.key")` empty (FAIL on the pin).
  - [ ] the G5 frame at 640x480 on the fixed image shows the HOSTNAME row with the device's name, not BATOCERA (`fix-walk-pending-image`).
- **Disposition (proposed):** a `bug` (Low) filed by the lane; PL-01's stream.

## PL-11: `applyChanges`: a value with a line end becomes a second key, the default check is dead, a commented `#k=` line is revived beside the real one, a first key behind a BOM is appended again, and a new key set to `default` is written literally (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a state write that can lose the record
- **Source Finding:** L-11, L-12, L-34; Argon SO-17 (accepted); Astra SO-22 -- proved: fixture (`state-units.out` U2: a second key; U3: the default written); tree (`SystemConf.cpp:366`, `:373-407`, `:414-419`; `TextEditComponent.cpp:176-185`, `HttpApi.cpp` for the absence of a line-end path)
- **Owner area:** es-core/src/SystemConf.cpp `applyChanges`, `set` (fork-modified)
- **What:**
  - **The cause:** `applyChanges` writes `key + val` (`:386-406`, `:414-419`), so a line end splits a value into two lines and a second key. `defaults.find(key)` with `key = it + "="` never matches (`:366`, `:389-391`), so a value equal to its table default is written, not removed. A `#k=` line is rewritten as a live `k=` beside the real one (no `break`, `:384-398`); a BOM hides the first key, which is appended again; a key not yet in the file set to `default` is written `key=default` (`:405`). No player or network path sets a line end at the pin.
  - **The fix shape:** a value is validated at `set` (no line end); the default comparison on the key, not `key=`; a comment line left alone; the BOM stripped at the parse (with PL-10); `default` is a removal, never a literal.
- **Can this be done on the VM?** Yes -- the host: U2 and U3, and new `SystemConfTests` cases for the three rewrites (`fix-unit-test`).
- **Already written:** files on cards may hold a revived `k=` beside the real one (the parser's last-nonempty rule makes the live line win today), a duplicated first key, or a literal `key=default` -- read both: the fixed reader treats a literal `default` as unset and the last duplicate as the value, writes neither shape again, and rewrites nothing until the next save.
- **Acceptance:**
  - [ ] U2: a value with a line end is refused or escaped (the pin writes two keys).
  - [ ] U3: a value equal to its table default removes the line (the pin writes it).
  - [ ] a unit: a file with `#k=1` and `k=2`, saved with `k=3`, holds one `k=` line and the comment intact (FAIL on the pin).
  - [ ] a unit: `set("new", "default")` then a save writes no `new=default` line (FAIL on the pin).
- **Disposition (proposed):** a `bug` (Low) filed by the lane; PL-01's stream.

## PL-12: `Settings` (`es_settings.cfg`): no lock and no mutex on its maps; a failed record write is not retried; any well-formed XML becomes the record; the recovery copy takes the record's mode and the recording the live file's; no unit test (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4, Q5
- **Family:** a state write that can lose the record
- **Source Finding:** L-13, L-30; Astra SO-20, SO-21, SO-53 (accepted); Argon SO-16 (`root = doc` when there is no `<config>`) -- proved: tree (`Settings.cpp:469-540`, `:533-534`, `:566-632`, `:590-592`, `:617`, `:629-631`; `Settings.h:147-157`; `001-functions:622-623`); the guest's G4b (the ladder recovered an emptied file, `g04b-es-settings.txt`)
- **Owner area:** es-core/src/Settings.cpp, es-core/src/Settings.h (upstream's file, fork-modified); es-app/tests/unit/ (no `SettingsTests.cpp`)
- **What:**
  - **The lock:** D-CLOUD-079's sentence says EmulationStation's writers "take the settings lock around the read-modify-write"; `SystemConf` does, `Settings` does not, and its maps have no mutex. Which setters run off the interface thread is not enumerated.
  - **The record:** a failed record write logs, clears the dirty flag and returns success (`:533-534`), so it is never retried. Any well-formed XML parses as settings (`:566-601`) and the record is re-read from the path after the parse. The recovery copy takes the record's mode and the recording the live file's (`:617`, `:629-631`), which can widen a private record.
  - **The fix shape:** a mutex on the maps and the same `PidLock` shape around `saveFile`; a failed record kept dirty; the parse requires `<config>`; the modes from PL-05; `SettingsTests.cpp` with the ladder's cases (`04` § Codification gaps).
- **Can this be done on the VM?** Yes -- the host: `SettingsTests.cpp` built by the generated `g++` line (`tools/t21-build-tests.sh`), `fix-unit-test`; the guest: the G4b walk on the fixed image (`fix-walk-pending-image`).
- **Already written:** a record on a card that is "any XML" was written by `Settings` itself -- nothing inherited, argued; the crossed modes are narrowed by PL-05's start-time chmod (migrated there). D-CLOUD-079's sentence is the coordinator's to refine by a new row citing it (PL-26).
- **Acceptance:**
  - [ ] `SettingsTests` exists in the unit set and its summary line PASSes with cases for an empty, a cut and a non-`<config>` live file (each recovers from the record), and for a record write that fails (the flag stays dirty and the next save retries).
  - [ ] a save from a worker thread during a `getString` on the interface thread runs clean under ThreadSanitizer in the host build (the pin's lines race by reading).
- **Disposition (proposed):** a `bug` (Low) filed by the lane; a fix stream on the ES branch; the register row to the coordinator.

## PL-13: the sweeps: a writer killed before its rename leaves `path.tmp.<pid>.<n>`, which nothing sweeps (42 of 99 kill points), and the interface's start removes `system.cfg.backup.tmp`, the name `chksysconfig backup` writes (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3, Q4
- **Family:** a credential's sink (the leftover takes the live file's mode with the scraper's account inside); a state write that can lose the record (L-29)
- **Source Finding:** L-09, L-29; Astra SO-19 (Low), SO-36 (a leftover can be empty or partial); Argon SO-27 (a leftover's own temporary starts 0600 and takes the live file's mode before the bytes) -- proved: fixture (`stage-b/positives/kill-writer.out`: 99 kill points, 42 leave a temporary); tree (`AtomicFileUtil.cpp:50-64`, `:115`; `Settings.cpp:557-558`; `SystemConf.cpp:203-210`; `chksysconfig:67-70`; `backuptool:283-292`)
- **Owner area:** es-core/src/utils/AtomicFileUtil.cpp, es-core/src/Settings.cpp, es-core/src/SystemConf.cpp (fork-own); `chksysconfig` (T1's file, read)
- **What:**
  - **The leftovers:** since PL-063 the sweeps remove only the old shared names. A leftover for `es_settings.cfg` can be empty or partial with the scraper's account inside at the live file's mode; the settings archive takes the stores by exact name, so leftovers stay on the card.
  - **The wrong sweep:** `SystemConf.cpp:210` removes `system.cfg.backup.tmp` at the interface's start, believing nothing else writes it; `chksysconfig backup` does (`:69-70`), so a start during a shutdown backup removes its temporary (unlikely; Low).
  - **The fix shape:** each store sweeps `<path>.tmp.*` whose pid is dead, at start and after every save; the start's sweep leaves `chksysconfig`'s name alone (or `chksysconfig` takes a name the interface never sweeps: T1's file, a note).
- **Can this be done on the VM?** Yes -- the host: `kill-writer.py` with a sweep assertion after a simulated next start (`fix-unit-test`); the guest: `ls` beside the stores after a kill of EmulationStation mid-save and a restart.
- **Already written:** leftovers already on cards, possibly holding an account -- migrated: the start's sweep removes every dead-pid temporary of both stores once.
- **Acceptance:**
  - [ ] `kill-writer.py` reports 0 temporaries left after the start's sweep (the pin: 42 of 99).
  - [ ] `tools/vm-upgrade-rehearsal`'s seed carries one leftover beside each store and the rehearsal reports both gone after the update's first start.
  - [ ] a unit: the start with a `system.cfg.backup.tmp` present leaves it (FAIL on the pin).
- **Disposition (proposed):** a `bug` (Low) filed by the lane; a fix stream on the ES branch; `chksysconfig`'s name to the coordinator as a T1 note.

## PL-14: the executors: `executeEnumerationScript` discards the exit, eleven `WEXITSTATUS` reads lack `WIFEXITED`, `cloud_oauth close`'s result is ignored, and the shared legacy reader loses a long line's head and a last line without a newline (T20's PL-08, inherited) (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Family:** a check whose failure reads as success
- **Source Finding:** L-17, L-18, L-19; T20's PL-08 (deferred to #668 with `stage-b/positives/reader.cpp` at distribution `ffb6b686cb`); Astra SO-27 (the decoder defect is the reaped shell's; `sh` is bash and forks), SO-45; Argon SO-3 (`getBiosInformations`' `--filter` joins a system's name bare), SO-36 -- proved: fixture (`lifted.out` enum and script; T20's `reader.out`); tree (`ApiSystem.cpp:2251`; `:234`, `:270`, `:293`, `:329`, `:354`, `:397`, `:415`, `:440`, `:469`, `:2291`, `:2319`; `:593`; `:714-718`; `Settings.cpp:207`; `ViewController.cpp:507-509`)
- **Owner area:** es-app/src/ApiSystem.cpp `executeEnumerationScript`, `executeScriptLegacy`, `executeScript` (upstream's shape, fork-modified)
- **What:**
  - **The discarded exit:** a script that fails or is killed returns the lines it printed, as success (`:2251`). That is `getBiosInformations` at launch with CHECK BIOS AT LAUNCH on: no BIOS problem reported when `rocknix-systems` fails.
  - **The signal:** eleven sites read `WEXITSTATUS` without `WIFEXITED`; `joinWifiNetwork` then reads `joined` from the lines (`:714-718`). On the image `sh` is bash and forks, so a killed script reads 128+N and only the wrapping shell's death reads 0 (T20's G02).
  - **The ignored result:** `cloud_oauth close` at `:593`.
  - **The reader (T20's):** `fgets` into 1,024 bytes drops a fragment without a newline; `WEXITSTATUS` without `WIFEXITED` at `:2278-2291`.
  - **The fix shape (Q1, modernize):** one bounded logical-line reader for the four executors, the exit returned and checked (`WIFEXITED` then `WEXITSTATUS`; a signal is a failure), an oversized record refused rather than cut, the last line kept; `executeEnumerationScript` returns the exit beside the lines and `getBiosInformations` says the check could not run. The Windows shims at `:45-46` recorded, not changed.
- **Can this be done on the VM?** Yes -- the host: `lifted enum|script` and T20's `reader.cpp` are the positives (`fix-unit-test` once the reader is a unit); the guest: CHECK BIOS AT LAUNCH on with `rocknix-systems` made to exit 1, the launch's sentence in a frame (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a unit: a script that exits 1 after printing two lines returns a failure from `executeEnumerationScript` (the pin returns the lines as success, `lifted.out` enum).
  - [ ] a unit: a child killed by a signal is a failure at every executor (the pin reads 0, `lifted.out` script).
  - [ ] T20's three: a 1,500-byte record is refused, not passed cut; a last line without a newline is kept; a waited process killed by a signal is a failure (`reader.cpp` FAIL on the pin, PASS after).
  - [ ] `cloud_oauth close`'s non-zero exit is logged at `:593`.
- **Disposition (proposed):** a `bug` (Low) filed by the lane; a fix stream on the ES branch (the reader as a unit).

## PL-15: `led.colour` is parsed with `std::stoi` and no catch: a word throws out of the LED page's build, `255,0,165` reads as white; `setLEDBrightness`'s `std::stoul` is the same shape (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q5
- **Family:** a check whose failure reads as success
- **Source Finding:** L-16 -- proved: fixture (`lifted.out` led: throws; white; `255 0 0`); tree (`ApiSystem.cpp:1868-1890`, `:2083-2087`; `GuiMenu.cpp:2989`, T26's page)
- **Owner area:** es-app/src/ApiSystem.cpp `getLEDColours`, `setLEDBrightness` (the parse; the page is T26's)
- **What:**
  - **The cause:** `getLEDColours` (`:1877-1887`) splits the setting on spaces and calls `stoi` on each field: a word throws `std::invalid_argument` out of the page's build; a comma list reads white; two numbers read as `255 0 0`. `setLEDBrightness`'s `stoul` has the same shape.
  - **The fix:** a parse that returns the default on anything but three numbers, in `CloudText`'s pure shape with a case (`es-code-traps.md` § Pure text has a home).
- **Can this be done on the VM?** Yes -- the host (`lifted led`, FAIL on the pin), `fix-unit-test`; the guest: `led.colour=blue` in `system.cfg` and the LED page opened (`fix-walk-pending-image`).
- **Already written:** a `led.colour` word already in a device's `system.cfg` -- read both: the fixed parse reads it as the default and the page opens.
- **Acceptance:**
  - [ ] `lifted led`: `blue` returns the default without throwing, and `255,0,165` returns either 255 0 165 or the default (the pin throws, then white).
  - [ ] a unit case in the pure parser's test file.
- **Disposition (proposed):** a `bug` (Low) filed by the lane; a fix stream on the ES branch (the parse); the page is T26's.

## PL-16: the Wi-Fi key on argv: of `sh`, `timeout` and `wifictl` for up to 150 s and of `nmcli` for up to 90 s, and of `env` during `set_settings`; the evidence page's `top` could carry it

- **Severity:** Low
- **Category:** Security
- **Question:** Q3
- **Family:** a credential's sink (argv)
- **Source Finding:** L-08, L-25; Astra SO-12 (accepted: the `env` sink), SO-35; Argon SO-11 item 1, SO-26 -- proved: guest (`guest-cycle/g03-argv.txt`: 3 processes carried the key in their command lines; `top -b -n 1 | head -25` carried it on 0 lines, with no adapter); tree (`ApiSystem.cpp:635-637`, `:2328`; `wifictl:177`, `:460`; `001-functions:600-602`; `rocknix-evidence:71`)
- **Owner area:** es-app/src/ApiSystem.cpp `enableWifi` (the command's shape); `wifictl` and `001-functions` (T1's files)
- **What:**
  - **The sinks:** `enableWifi` builds `timeout 150 wifictl connect '<ssid>' '<key>' '<country>'` for `system()` (the quoting closes injection, not the argv); `connect_wifi` hands it to `nmcli ... password "${PSK}"` (`wifictl:177`); `set_settings` passes `SV<n>=<value>` as `env`'s arguments while `awk` runs (`001-functions:600-602`). Readable in `/proc/*/cmdline` by any user; only root runs on the image. `:642` is Windows-only (a brief correction, not a finding).
  - **The fix shape:** the key leaves the command line -- the page writes it to `wifictl`'s stdin or a 0600 file it names, and `wifictl` hands `nmcli` a keyfile or `--ask` (T1's file); `set_settings` passes values through the environment it already uses for `K` and `V` (T1's file).
- **Can this be done on the VM?** Yes -- the guest's G3 count is the measure (the processes whose cmdline carries the key, the value never printed): 3 on the pin, 0 after (`fix-walk-pending-image`); the host: `tools/cloud-input-test` asserts `wifictl`'s argv after the change (`fix-unit-test`).
- **Already written:** nothing inherited: a process's lifetime.
- **Acceptance:**
  - [ ] G3 on the fixed image: 0 of `/proc/*/cmdline` carry the key during a connect (the pin: 3), the count written as `g03-argv.txt` writes it.
  - [ ] `tools/cloud-input-test`'s case: `wifictl connect` receives no key in argv (FAIL on `8ebaf8daad`, PASS after).
- **Disposition (proposed):** the page's half a fix stream on the ES branch; `wifictl` and `001-functions` are T1's files, to the coordinator's ruling (#648); the `bug` label at the ruling.

## PL-17: the scraper's readers accept an empty or failed answer: a failed `7zr` extraction's digest of empty input is stored as the game's, invalid user-info XML reads as one thread, `getCRC32`'s empty `CRC = ` entry, a `Retry-After` date read as 0 ms (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Family:** a check whose failure reads as success
- **Source Finding:** L-31; Astra SO-54 (accepted); Argon SO-43 (`getCRC32`'s empty entry and its `size_t` subtraction; the `Retry-After` HTTP-date), SO-19 -- proved: tree (`ApiSystem.cpp:1527-1530`, `:1582-1586`; `ScreenScraper.cpp:1075-1089`; `Scraper.cpp:618-623`)
- **Owner area:** es-app/src/ApiSystem.cpp `getMD5`, `getCRC32`; es-app/src/scrapers/ScreenScraper.cpp `getThreadCount`; es-app/src/scrapers/Scraper.cpp (T32's caller lines)
- **What:**
  - **The four:** a failed extraction's `md5sum` of empty input stored as the game's MD5 (with PL-02's stream: the exit checked, an empty extraction stored as no hash); an unparsable user-info body read as one thread (`ScreenScraper.cpp:1075-1089`); `getCRC32`'s empty entry (`:1582-1586`); a `Retry-After` HTTP-date read as 0 ms (`Scraper.cpp:618-623`).
  - **The fix shape:** validity beside the data (T20's PL-15 shape): a failed extraction stores nothing; an unparsable answer is a failure with its sentence; an HTTP-date parsed, or the default wait.
- **Can this be done on the VM?** Yes -- the host: units once the parses are pure (`fix-unit-test`).
- **Already written:** the empty input's digest already stored (PL-02's line: read both, re-hashed); nothing else inherited.
- **Acceptance:**
  - [ ] a unit: an archive `7zr` cannot read leaves the game's MD5 absent (with PL-02).
  - [ ] a unit: a non-XML user-info body yields a failure, not a thread count of 1.
  - [ ] a unit: `getCRC32` over an empty entry returns no CRC.
  - [ ] a unit: `Retry-After: <HTTP-date>` waits until that date or the default, never 0.
- **Disposition (proposed):** a `bug` (Low) filed by the lane; the `getMD5` and `getCRC32` halves in PL-02's stream; the scraper's two in a small stream of their own.

## PL-18: two sentences that are not true: RESTORED when the write-back failed or the lock was busy; YOU'RE NOT ONLINE for a 501 to 504 or redirects exhausted (a `bug` proposed)

- **Severity:** Low
- **Category:** Standards
- **Question:** Q5, Q6
- **Family:** a check whose failure reads as success
- **Source Finding:** L-32, L-36; Astra SO-55 (accepted), SO-10 (the certificate case, #1154's); Argon SO-45 item 2 -- proved: tree (`SystemConf.cpp:221-265`; `Settings.cpp:615-619`; `main.cpp:1041-1042`; `HttpReq.cpp:462-469`; `ScreenScraper.cpp:989-990`)
- **Owner area:** es-core/src/SystemConf.cpp, es-core/src/Settings.cpp, es-app/src/main.cpp (the recovery's sentence); es-core/src/HttpReq.cpp, es-app/src/scrapers/ScreenScraper.cpp (the status classes)
- **What:**
  - **RESTORED:** `sRecovered` is set when the write-back fails or the lock is busy, and the player reads `YOUR SETTINGS FILE WAS DAMAGED. THE LAST GOOD COPY WAS RESTORED.`; the words also stand for a file that was missing, not damaged.
  - **NOT ONLINE:** 501 to 503, 504 and redirect exhaustion read as `YOU'RE NOT ONLINE` to an online player.
  - **The fix shape:** three outcomes for the ladder, each a sentence in the player's words with its French (restored and written back; restored in memory with the write-back owed; the file was missing, the defaults used); the client's status classes mapped to their own sentence -- `THE SCRAPER'S SERVER ISN'T ANSWERING RIGHT NOW.` proposed, built with the proposed words (D-UI-112).
- **Can this be done on the VM?** Yes -- the host: the mapping as pure code with cases (`fix-unit-test`); the guest: the G4 walk with the lock held by a stub holder, and the #1154 endpoint answering 503, each a frame at 640x480 (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] with `/tmp/.system.cfg.lock` held, the recovery's frame says the copy is restored in memory and will be written next time, not RESTORED.
  - [ ] a 503 from the endpoint shows the server sentence, not YOU'RE NOT ONLINE, in a frame at 640x480.
  - [ ] each new sentence in `fr.po` with a non-empty msgstr.
- **Disposition (proposed):** a `bug` (Low) filed by the lane; a small stream on the ES branch.

## PL-19: `HttpReq`'s smaller ones: a data race on `mStatus`; the server's body for 400 to 503 logged verbatim into `es_log.txt`; `customHeaders`' `curl_slist` never freed (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a credential's sink (the log, L-05); a data race and a leak (no family, L-04 and L-07)
- **Source Finding:** L-04, L-05, L-07 -- proved: tree (`HttpReq.cpp:395`, `:416-521`, `:640-643`; `:439-473`, `:562`; `:174-179`); a ThreadSanitizer run needs curl, `CANNOT` on this host
- **Owner area:** es-core/src/HttpReq.cpp (upstream-carried; contained fixes)
- **What:**
  - **The race:** one caller's `status()` writes every request's `mStatus` under `mMutex` while each request's own thread reads its `mStatus` without it; no wrong outcome observed.
  - **The log:** for 400 to 503 the body goes verbatim to LogError; with #1154 that body is anyone's on the path.
  - **The leak:** the header list is never freed, per request.
  - **The fix shape:** `std::atomic` for `mStatus` or the read under the mutex; the body bounded and passed through `maskSecrets`, or at LogDebug; `curl_slist_free_all` in the destructor.
- **Can this be done on the VM?** Yes -- the host: the leak under ASan's leak check and the log line's shape as a unit (`fix-unit-test`); the race settled by reading until a curl-linked ThreadSanitizer build exists.
- **Already written:** bodies already in `es_log.txt` are on tmpfs and gone at reboot -- nothing inherited.
- **Acceptance:**
  - [ ] ASan's leak report for a request with a custom header is empty (the pin leaks the list).
  - [ ] a 503 body of 10 kB reaches the log as at most one bounded, masked line.
  - [ ] `mStatus` is atomic or read under `mMutex` at every read (`/usr/bin/grep -n mStatus es-core/src/HttpReq.cpp` posted with each line's guard named).
- **Disposition (proposed):** a `bug` (Low) filed by the lane; PL-07's stream.

## PL-20: eight `writeAllText` call sites write a state file on the card in place: truncate, unchecked `fwrite` and `fclose`, no `fsync`

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a state write that can lose the record
- **Source Finding:** L-14 (`02` § The writers, group 2); Astra SO-41 (in part), Argon SO-32 (in part) -- proved: tree, tool-run (`tools/t21-writers.py`: 25 sites, 16 sysfs, 8 on the card, 1 Windows-only)
- **Owner area:** es-app/src/CaptureRotation.cpp:175, FileData.cpp:2213, KeyboardMapping.cpp:426 and :429, guis/GuiMenu.cpp:11587, guis/GuiKeyboardLayout.cpp:164, services/HttpApi.cpp:258 (outside the 14); ThreadedCloudSync.cpp:944 (fixed on T18's branch, `f63ad4de4`)
- **What:**
  - **The cause:** `writeAllText` is `fopen "wb"`, `fwrite` and `fclose` unchecked, void (`FileSystemUtil.cpp:1429-1443`): a kill mid-write leaves an empty or cut file where the old one was. The sixteen sysfs writes are kernel attributes, not files on the card, and are not this item's.
  - **The fix shape:** each onto `Utils::AtomicFile::writeText` (T18's S2 shape), the write's result read. Seven of the eight are outside the slice's 14 files.
- **Can this be done on the VM?** Yes -- the host: the kill sweep (`kill-writer.py`) extended to each moved writer (`fix-unit-test`).
- **Already written:** an empty or cut file already on a card is read by its own reader as today, and the fixed writer replaces it whole at the next save -- read both, argued.
- **Acceptance:**
  - [ ] `tools/t21-writers.py --expect-writeall 17` passes at the fix's commit (the eight card files moved; the sixteen sysfs rows and the Windows row remain).
  - [ ] the kill sweep over each moved writer: 0 of its kill points leave a cut file.
- **Disposition (proposed):** a stream on the ES branch or a Backlog in #1143's family, to the coordinator's ruling: seven of the files are outside the slice's 14.

## PL-21: `GuiLoading` completions hold raw `this`; the Bluetooth page's worker writes `mWaitingLoad`, which the interface thread reads (plausible, not settled)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q7
- **Family:** none (a lifetime and a data race by reading)
- **Source Finding:** L-35; Astra SO-56 (plausible), Argon SO-44 (plausible) -- proved: tree (`GuiWifi.cpp:314`, `:350`, `:382`; `GuiBluetoothDevices.cpp:127`, `:150`); `tests/wifi-profile-lifetime.py` PASS at the pin (R18) covers the profile-choice callback, not these
- **Owner area:** es-app/src/guis/GuiWifi.cpp (fork-own); es-app/src/guis/GuiBluetoothDevices.cpp (outside the 14)
- **What:**
  - BACK is refused while `mWaitingLoad`, so the lifetime is plausible; whether anything else deletes the page meanwhile is not settled. The Bluetooth page's `mWaitingLoad` is written from the worker and read on the interface thread without a guard. Both seats graded it plausible; it is carried so the ruling can assign a reading or withdraw it.
- **Can this be done on the VM?** Yes -- the host: a case in `tests/wifi-profile-lifetime.py`'s shape that deletes the page under a `GuiLoading` and runs under ASan, if a path to the deletion exists; otherwise settled by reading and recorded.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] per the ruling: a `tests/` case that deletes the page under the load and runs clean under ASan, or a reading posted on the audit issue naming what keeps the page alive until the completion runs.
- **Disposition (proposed):** to the ruling: a reading in PL-06's stream (`GuiWifi.cpp` is its file), or withdrawn as recorded; `GuiBluetoothDevices.cpp` is outside the 14.

## PL-22: on the interface thread with no frame bound: the settings lock's 5 s budget up to twice per load or save, the setters and `cloud_oauth` calls with no bound, and every page close writing both stores with up to four `fsync`s

- **Severity:** Low
- **Category:** Performance
- **Question:** Q1, Q5
- **Family:** none (time to play)
- **Source Finding:** Astra SO-4 (a list, not a demonstrated freeze), SO-58 (a lock budget is not a frame bound); Argon SO-4 (up to 10 s); `04` § Q5 Efficiency; Q1's blocking calls -- proved: tree (`SystemConf.cpp:91-92`, `:218`, `:304`; `GuiSettings.cpp:94-95`; the setters' rows of `02` § The commands)
- **Owner area:** es-core/src/SystemConf.cpp, es-core/src/guis/GuiSettings.cpp; es-app/src/ApiSystem.cpp (the setters)
- **What:**
  - One load or one save can take the settings lock twice at up to 5 s each on the interface thread; a page close writes both stores and, for `SystemConf`, `fsync`s up to four times; the timezone, audio, storage, service, hotkey and LED setters, the `cloud_oauth` calls and `getBiosInformations` at launch (with its setting on) have no bound. The retro measures the two time-to-play numbers (`tools/time-to-play --vm`).
  - **The fix shape (Q1):** the save off the interface thread with the close not waiting on it, or one write per close; the lock's wait bounded by a frame budget with the change kept in memory, as `LockBusy` already does.
- **Can this be done on the VM?** Yes -- `tools/time-to-play --vm` with the backend up: the exit-sync median against D-CLOUD-119 and the launch number against the retro's line.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the retro's two numbers on the guest, cited from `docs/vm-qa-log.md`, with the save at a page's close and the BIOS enumeration named with what they cost.
  - [ ] a Backlog issue naming the lock budget and the close's writes, filed by the coordinator.
- **Disposition (proposed):** to the retro's time-to-play line and a Backlog the coordinator files.

## PL-23: the harness: no `SettingsTests.cpp`; the kill sweep, S1 and U1 to U3 are not standing cases; `tools/vm-upgrade-rehearsal` seeds neither `.backup`; `tools/cloud-input-test` drives `wifictl` on the host only; no Wi-Fi or scraper walk has a baseline; G6 and G7 owed

- **Severity:** Low
- **Category:** Harness
- **Question:** Q8
- **Family:** none
- **Source Finding:** Q8; `04` § Q8 and § Instruction File Recommendations; `02` § The guest cycle (G6 and G7 `CANNOT`: the harness refusal, no further window) -- proved: tool-run (R12, R13, R17, R21 to R24)
- **Owner area:** es-app/tests/unit/; tools/vm-upgrade-rehearsal, tools/cloud-input-test, tools/vm-walks/ (the distribution's, under a Backlog)
- **What:**
  - **What holds:** `AtomicFileTests` 24 and `SystemConfTests` 10 at the pin; `tools/settings-modes-test` (#421); `tools/last-good-scripts-test`'s `system.cfg` cases.
  - **What is missing:** nothing tests `Settings`; the kill sweep is the first and passes; the seed-against-the-record case is the first and fails; the rehearsal seeds neither `.backup`; `cloud-input-test` is host-only; no `claims.txt` baseline for a Wi-Fi or scraper walk.
  - **The new cases this slice would add:** the kill sweep, S1, U1 to U3 and the four lifted cases, each failing on the pin where it is a lead.
- **Can this be done on the VM?** Yes -- all on the host and the guest.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the Backlog issues the coordinator files, each naming its artifact (a test's PASS line; the rehearsal's seed and its report; a walk's `claims.txt`).
  - [ ] the two G6 walks exist as `.steps` under `tools/vm-walks/` for the integration window, written by the coordinator, each naming its marker and its frame (a Backlog under #903).
- **Disposition (proposed):** Backlogs the coordinator files (under #903's family); the two G6 walks for the integration window.

## PL-24: 82 of the 143 command rows name a script the distribution does not ship at `8ebaf8daad`; recorded as written

- **Severity:** Info
- **Category:** Dead code
- **Question:** Q7
- **Family:** none
- **Source Finding:** L-20 (`02` § The commands' last column); `04` § Q7 (the `isScriptingSupported` gates check absent executables too; `batocera-storage-manager` and `keyboardToPads` have no `ScriptId` gate, T26's to read) -- proved: tool-run (R4, R19)
- **Owner area:** es-app/src/ApiSystem.cpp (upstream's rows)
- **What:**
  - A table; D-WORKFLOW-209's shape removes nothing and edits no recipe. The Windows-only branches (`:639-645`, `Win32ApiSystem.cpp`) are recorded, not dead on Windows. Recorded as written.
- **Can this be done on the VM?** n/a.
- **Already written:** nothing inherited.
- **Acceptance:** none (a dead-end row).
- **Disposition (proposed):** recorded as written (D-WORKFLOW-209); the renovation's later pass, #1143's family.

## PL-25: #1154's design question for the pause: verify the peer by default with the image's CA bundle, the 2021 exception an explicit option the scrapers' media downloads set; three design notes

- **Severity:** Info
- **Category:** Security
- **Question:** Q2
- **Family:** a credential's sink (the unverified peer)
- **Source Finding:** L-06 (cited, not re-found); Astra SO-9 (the 429 retry rebuilds the request without its options), SO-10 (certificate failures read as `YOU'RE NOT ONLINE`; `VERIFYHOST` 0 rides with client certificates); Argon SO-9 -- proved: tree (`HttpReq.cpp:192`, `:200`; `Scraper.cpp:596`; `ScreenScraper.cpp:989-990`); guest (`g01-identity.txt`: `/etc/ssl/certs/ca-certificates.crt` present; curl 8.21.0)
- **Owner area:** es-core/src/HttpReq.cpp (#1154, one `bug` across T20's and T21's lines)
- **What:**
  - **The question:** verify the peer by default with the image's bundle, present on the image; keep the 2021 exception as an explicit `HttpReqOptions` field the scrapers' media downloads set. T20's S2 added `httpsRedirectsOnly` for a credential request.
  - **The notes for the fix:** a media-only exception must survive the 429 retry, which today rebuilds from URL and path; a certificate failure needs its own sentence (with PL-18); `VERIFYHOST` stays with the client-certificate path only if the ruling keeps it.
  - **Not read:** the scrapers' behaviour with verification on (G6(c), `CANNOT` for the slice).
- **Can this be done on the VM?** Yes -- the guest's self-signed listener for `api.screenscraper.fr` (the brief's § 5) is the scraper half's positive; the lane's window did not reach it.
- **Already written:** credentials already sent to an unverified peer cannot be recalled (T20's PL-02 line); nothing to migrate.
- **Acceptance:**
  - [ ] #1154's own criteria; the three design notes carried there in a comment by the coordinator.
- **Disposition (proposed):** to #1154 at the ruling (the fix is one `bug` across T20's and T21's lines).

## PL-26: notes for T26, T1, T22 and the register: the rows that read this slice's state, the shell writers' contract, the boot order, the WI-FI KEY popup with no masking mode, and D-CLOUD-079's sentence

- **Severity:** Info
- **Category:** Handoff
- **Question:** none
- **Family:** none
- **Source Finding:** `02` § What T26 and the OS slices inherit; `02` § The credentials' paths (the screen row); `04` § Instruction File Recommendations; Astra SO-11 (rejected in part: neither popup class takes a password parameter; the rest holds)
- **Owner area:** —
- **What:**
  - **T26 (#673):** `GuiMenu.cpp:9909` (the hostname row, PL-01 and PL-10), `:3209` (`getRootPassword`'s literal `linux` shown), `:2989` (the LED page, PL-15), `:3130-3151` (`setStorage`'s ignored result, PL-06); `batocera-storage-manager` and `keyboardToPads` with no `ScriptId` gate (PL-24).
  - **T1 (#648):** `set_setting`'s seed (PL-03), `wifictl`'s device guard (PL-06), `env`'s and `nmcli`'s argv (PL-16), `chksysconfig`'s sentinel and its `.backup.tmp` name (PL-01, PL-13).
  - **T22 (#669):** how often `system.cfg` is absent at a `set_setting` after boot (PL-03).
  - **The WI-FI KEY popup:** the key is typed in the clear (`GuiWifi.cpp:365`, `:367`) and neither popup class has a masking mode (`GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14`); the relink page's row is masked. A mode to add in es-core, for the coordinator to place; not a numbered lead, recorded here so it is not lost.
  - **The register and the rules:** D-CLOUD-079's sentence describes `SystemConf` only (PL-12); a rule beside D-CLOUD-078 that a writer seeding a file from defaults takes the writers' lock and consults the record first (PL-03); `es-code-traps.md`: curl's header buffer is not NUL-terminated (PL-07).
- **Can this be done on the VM?** n/a.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the notes posted on #673, #648 and #669, and the row and rule proposals on #668, by the coordinator.
- **Disposition (proposed):** routed at the stage-D ruling.

## Phase 7 resolution gate

Pre-issue, 2026-10-27: every item is **Open**; the stage-D ruling sets each outcome, and the table and the index are rewritten together when it does.

| Item | Outcome | Proposed disposition (the ruling's) |
| --- | --- | --- |
| PL-01 | Open | a `bug` (High); a fix stream on the ES branch; `chksysconfig`'s sentinel a note on #648 |
| PL-02 | Open | a `bug` (High); a fix stream on the ES branch; a #585 line |
| PL-03 | Open | a `bug` (High); the shell half to the ruling on #648; the recorder's half a fix stream on the ES branch |
| PL-04 | Open | a `bug` (Medium); a fix stream on the ES branch; a #585 line for `renameFile` |
| PL-05 | Open | a `bug` (Medium); a fix stream on the ES branch; the seed's build step to the coordinator |
| PL-06 | Open | a `bug` (Medium); `wifictl`'s half to the ruling on #648; the page's half a fix stream on the ES branch |
| PL-07 | Open | a `bug` (Medium); a fix stream on the ES branch; a #585 line |
| PL-08 | Open | a `bug`, severity to the ruling; PL-07's stream; a #585 line |
| PL-09 | Open | a `bug`, severity to the ruling; a fix stream on the ES branch |
| PL-10 | Open | a `bug` (Low); PL-01's stream |
| PL-11 | Open | a `bug` (Low); PL-01's stream |
| PL-12 | Open | a `bug` (Low); a fix stream on the ES branch; a register row to the coordinator |
| PL-13 | Open | a `bug` (Low); a fix stream on the ES branch; `chksysconfig`'s name a note on #648 |
| PL-14 | Open | a `bug` (Low); a fix stream on the ES branch (the reader as a unit) |
| PL-15 | Open | a `bug` (Low); a fix stream on the ES branch (the parse) |
| PL-16 | Open | the page's half a fix stream on the ES branch; the scripts' half to the ruling on #648 |
| PL-17 | Open | a `bug` (Low); PL-02's stream for the hashes; a small stream for the scraper's two |
| PL-18 | Open | a `bug` (Low); a small stream on the ES branch |
| PL-19 | Open | a `bug` (Low); PL-07's stream |
| PL-20 | Open | a stream on the ES branch or a Backlog in #1143's family, to the ruling |
| PL-21 | Open | a reading in PL-06's stream, or recorded as written, to the ruling |
| PL-22 | Open | the retro's time-to-play line and a Backlog the coordinator files |
| PL-23 | Open | Backlogs the coordinator files; the two G6 walks for the integration window |
| PL-24 | Open | recorded as written (D-WORKFLOW-209) |
| PL-25 | Open | to #1154 at the ruling |
| PL-26 | Open | routed at the ruling |

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: "High"
  category: Correctness
  question: Q4
  source_finding: "L-23"
  outcome: "open"
- id: PL-02
  severity: "High"
  category: Security
  question: Q1
  source_finding: "L-01, L-31 (the getMD5 half)"
  outcome: "open"
- id: PL-03
  severity: "High"
  category: Correctness
  question: Q4
  source_finding: "L-10"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-03, L-28"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: Security
  question: Q3
  source_finding: "L-21"
  outcome: "open"
- id: PL-06
  severity: "Medium"
  category: Correctness
  question: Q6
  source_finding: "L-22, L-33"
  outcome: "open"
- id: PL-07
  severity: "Medium"
  category: Security
  question: Q2
  source_finding: "L-02"
  outcome: "open"
- id: PL-08
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-24"
  outcome: "open"
- id: PL-09
  severity: "Medium"
  category: Correctness
  question: Q4
  source_finding: "L-27"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: Correctness
  question: Q5
  source_finding: "L-15, L-26"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-11, L-12, L-34"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-13, L-30"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-09, L-29"
  outcome: "open"
- id: PL-14
  severity: "Low"
  category: Correctness
  question: Q6
  source_finding: "L-17, L-18, L-19, T20's PL-08"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Correctness
  question: Q5
  source_finding: "L-16"
  outcome: "open"
- id: PL-16
  severity: "Low"
  category: Security
  question: Q3
  source_finding: "L-08, L-25"
  outcome: "open"
- id: PL-17
  severity: "Low"
  category: Correctness
  question: Q6
  source_finding: "L-31"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Standards
  question: Q5
  source_finding: "L-32, L-36"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-04, L-05, L-07"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-14"
  outcome: "open"
- id: PL-21
  severity: "Low"
  category: Correctness
  question: Q7
  source_finding: "L-35"
  outcome: "open"
- id: PL-22
  severity: "Low"
  category: Performance
  question: Q1
  source_finding: "Astra SO-4, SO-58; Argon SO-4; 04 § Q5"
  outcome: "open"
- id: PL-23
  severity: "Low"
  category: Harness
  question: none
  question_reason: "the brief's Q8 (the harness), not one of the renovation questions Q1 to Q7"
  source_finding: "Q8"
  outcome: "open"
- id: PL-24
  severity: "Info"
  category: Dead code
  question: Q7
  source_finding: "L-20"
  outcome: "open"
- id: PL-25
  severity: "Info"
  category: Security
  question: Q2
  source_finding: "L-06 (#1154, cited)"
  outcome: "open"
- id: PL-26
  severity: "Info"
  category: Handoff
  question: none
  question_reason: "an extraction note or a handoff, not a renovation question"
  source_finding: "02 § What T26 and the OS slices inherit"
  outcome: "open"
```
