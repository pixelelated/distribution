# Punch list — M6.P2 T31, EmulationStation's other pages (#678)

Written by the first reader (Opus 5.5) at stage C, from:
- `02` § Leads and § Corrections and new leads from the seat;
- `04` § Risk assessment;
- the guest cycle and the stage-C harnesses;
- `stage-c/astra-grades.md`.

- **reviewed-at:** `da7922a7bd` (distribution), **reviewed-at-es:** `16dbac5211` (the pin). **fixed-at:** `ada47cfe46` (distribution, `feature/m6-es-pages-678`), **fixed-at-es:** `95852f873` (`feature/m6-es-pages-678` on pixelelated/emulationstation).
- **Independent depth:** one seat, GPT-6 Astra at `max` (43 items: 41 accepted, 1 in part, 1 not kept).
- **One item per defect or reusable improvement**, however many leads found it, ordered by severity. Not an item: L-25 (a real seed, recorded).
- **Nothing here changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. A fix lands only under a stream brief on the ES branch, proven twice. A row added, moved or renamed updates `docs/es-menu-map.md` in the same commit (D-UI-039).
- **Lines** are the pin's. "Guest" means the M6 image (M7's composition over the pin); "fixture" means a stage-C harness that fails at the pin and passes its control.

---

## PL-01: START (CLOSE) and a click outside the menu delete settings pages without `close()`, dropping their deferred choices (a `bug` proposed; upstream's base)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record
- **Source Finding:** L-01 (EP-1, narrowed), L-34 (EP-34) -- proved: fixture (`stage-c/l01-start-drops.py`), guest (G02)
- **Owner area:** `GuiSettings.cpp:106-112`, `:133-139`, `:456-464`; the same loop in `GuiScraperStart.cpp:542-548` and `GuiMetaDataEd.cpp:620-624`
- **What:**
  - START runs `delete window->peekGui()` down to the view, and an outside click runs `delete this`. Neither calls `close()`, so a `GuiSettings` page's deferred choices and its `onFinalize` are dropped. G02 shows it: B keeps a moved switch, START drops it.
  - Immediate setters keep theirs in memory, and `GuiGameOptions` saves in its destructor.
  - A stack can mix `GuiSettings` and plain pages (BIOS DETAILS over `GuiBios`), and `close()` is not virtual.
  - This is upstream behaviour reaching the fork's lanes (every cloud page is a `GuiSettings`).

  **Fix shape:** one close contract for the three exits, designed for a mixed stack and for pages an `onFinalize` pushes. This is not a loop of `close()`. Put to the coordinator.
- **Can this be done on the VM?** Yes. The harness, extended to a mixed stack (`fix-unit-test`); G02 again on the integration image (`fix-walk-pending-image`).
- **Already written:** nothing inherited. The lost choices were never written, and the fix changes when the stores are written, not what they hold.
- **Acceptance:**
  - [ ] `stage-c/l01-start-drops.py` against the fixed `GuiSettings.cpp` prints its cases (rc 0), with a mixed-stack case and an outside-click case added; against the pin it fails (`stage-e/s1-before.txt`, `s1-after.txt`).
  - [ ] on the integration image, USER INTERFACE SETTINGS > SHOW RETROACHIEVEMENTS ICON moved and START pressed: `es_settings.cfg` carries the change (`fix-walk-pending-image`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; fixed in this shape under **D-UI-128** (`acb7ead172`): each `GuiSettings` page closed from the top through `close()`, a plain page deleted as today, the loop stopped if an `onFinalize` pushes a page. Rule 6 applies (every cloud page is a `GuiSettings`; the save was the page's own promise). The reach is every settings page in the app, named in the stream's record and in a #585 line to ROCKNIX (the lines are identical in batocera's master). Proof: the lifetime harness over a mixed stack (a plain page between two settings pages; an `onFinalize` that pushes), FAIL first against the pin, then G02 with its control. **Already written:** nothing inherited -- the dropped values were never written.
- **Bug:** #1236 (filed 2026-10-27, with its code trace).

## PL-02: a settings page that registers no save function does not write the stores on its own close: the LED colour, and every page of only text rows (a `bug` proposed; the base, with T26's PL-17)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record
- **Source Finding:** L-02 (EP-2, narrowed), L-36 (EP-36); T26's PL-17, deferred to #678 (four GuiMenu sub-pages work around the same return with `onFinalize` saves) -- proved: fixture (`stage-c/l02-led-not-saved.py`)
- **Owner area:** `GuiSettings.cpp:83-96`; `GuiAnalogSticksLedControls.cpp:62-87`; `GuiMoonlight.cpp:278-343`; `GuiGameOptions.cpp:203-216`
- **What:**
  - `save()` returns when `mSaveFuncs` is empty, so a page that writes through `SystemConf::set` or a text row never calls `saveSystemConf`.
  - The change stays pending and persists only if a later page flushes `system.cfg` in the same session. The quirks' `ledcontrol` reads `analogsticks.led` from the file at boot.
  - Each LED slider step also runs the script on the interface thread.

  **Fix shape:** `save()` writes the stores whenever they changed, with or without a save function. T26's four workarounds then come out.
- **Can this be done on the VM?** Yes, by the harness (`fix-unit-test`). The LED row needs `DEVICE_ANALOG_STICKS_LED_CONTROL=true` for ES on a guest.
- **Already written:** a device whose `system.cfg` holds an old colour keeps it, and the page reads it at open (`:16-27`). The fix writes the next change; nothing to migrate.
- **Acceptance:**
  - [ ] `stage-c/l02-led-not-saved.py` against the fixed files: `analogsticks.led saved` (rc 0), with a text-row-only page case; against the pin it fails (`stage-e/s2-*.txt`).
  - [ ] the four `onFinalize` saves T26's PL-17 named either still work or are removed, by the fixture over `save()`.
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1237 (filed 2026-10-27, with its code trace).

## PL-03: Moonlight builds shell commands from the player's SERVER IP and the server's game titles, unquoted (a `bug` proposed; ROCKNIX's page)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q6
- **Family:** a command built from a player's string
- **Source Finding:** L-05 (EP-16), L-28 (EP-28) -- proved: fixture (`stage-c/l05-l06-moonlight.py`: the canary made by all three immediate commands); tree (the launchers)
- **Owner area:** `GuiMoonlight.cpp:282`, `:304`, `:306`, `:223-239`
- **What:**
  - The SERVER IP goes bare into `popen` (`executeScriptLegacy`, `ApiSystem.cpp:2269`).
  - UPDATE MOONLIGHT GAMES writes one `.sh` per game, with the server's `AppTitle` inside double quotes (`$(...)` and backticks stay live) and the host bare.

  **Fix shape:** `Utils::String::shellQuote` on every inserted argument, or the argv executor `WifiScanProcess.h` models (#1192).
- **Can this be done on the VM?** Yes. The fixture, extended with a generated launcher run under bubblewrap against a crafted title (`fix-unit-test`).
- **Already written:** launchers already generated from a crafted title stay on the card until the next UPDATE, which rewrites them all; a stored `moonlight.host` is quoted at its next use.
- **Acceptance:**
  - [ ] the fixture against the fixed file: no canary from the three commands or a generated launcher; the whole IP and the whole title each one argument (`stage-e/s3-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; one Moonlight stream with PL-03 to PL-06, PL-15 and PL-16 under rule 6 (D-QA-051), the #585 lines to ROCKNIX, whose page it is.
- **Bug:** #1238 (filed 2026-10-27, with its code trace).

## PL-04: UPDATE MOONLIGHT GAMES deletes the library before fetching its replacement, and reports success over unchecked writes (a `bug` proposed; ROCKNIX's page)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record
- **Source Finding:** L-29 (EP-29), L-30 (EP-30) -- proved: tree
- **Owner area:** `GuiMoonlight.cpp:167-184`, `:230-257`, `:287-295`
- **What:**
  - `rm .../images/*` and `rm .../*` run before the app list is fetched. A fetch or parse failure leaves the library empty, and the page says "Unable to connect to server".
  - The launchers' streams, `gamelist.xml`'s save and the box art are not checked, and `true` quits ES to reload.

  **Fix shape:** fetch and validate first, build the new set beside the old, replace it only on success, and check every write.
- **Can this be done on the VM?** Yes. A fixture over `UpdateMoonlightGames` with a doubled fetch (empty, malformed) and a read-only target (`fix-unit-test`).
- **Already written:** a device whose library was emptied by a failed update stays empty until a successful UPDATE rebuilds it. Nothing to migrate.
- **Acceptance:**
  - [ ] the fixture: an empty or malformed fetch leaves the seeded library untouched; a failed write returns false (`stage-e/s4-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; one Moonlight stream with PL-03 to PL-06, PL-15 and PL-16 under rule 6 (D-QA-051), the #585 lines to ROCKNIX, whose page it is.
- **Bug:** #1239 (filed 2026-10-27, with its code trace).

## PL-05: UNPAIR WITH SERVER removes nothing (`"~/..."` is not expanded) and says "Unpaired and settings cleared"; neither branch checks its removal (a `bug` proposed; ROCKNIX's page)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-06 (EP-17, extended to the embedded branch) -- proved: fixture, guest (G09)
- **Owner area:** `GuiMoonlight.cpp:328-338`
- **What:** a tilde inside double quotes is literal to the shell, so both `rm -r` exit 1 and the directories stay. The embedded branch's `rm` is not checked either. **Fix shape:** expanded, quoted paths, the results checked, and a sentence for a failure. The cleanup is local; no server-side revocation is claimed.
- **Can this be done on the VM?** Yes. The fixture; G09 again (`fix-walk-pending-image`).
- **Already written:** a device whose player pressed UNPAIR still holds the pairing. The next UNPAIR after the fix removes it.
- **Acceptance:**
  - [ ] the fixture against the fixed file: `L-06 directories left: none`, and a removal that fails is reported (`stage-e/s5-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; one Moonlight stream with PL-03 to PL-06, PL-15 and PL-16 under rule 6 (D-QA-051), the #585 lines to ROCKNIX, whose page it is.
- **Bug:** #1240 (filed 2026-10-27, with its code trace).

## PL-06: Moonlight's certificate parser can loop forever or throw inside the pairing callback, on the interface thread (a `bug` proposed; ROCKNIX's page)

- **Severity:** Medium
- **Category:** Reliability
- **Question:** Q3
- **Family:** work on the interface thread
- **Source Finding:** L-32 (EP-32) -- proved: tree
- **Owner area:** `GuiMoonlight.cpp:54-100`, `:308-325`
- **What:** `extractClient`/`extractKey` loop on `getline` with no EOF test, so a conf without the marker never ends. `replace(npos, ...)` throws on a value with no escaped newline. Both run in `executeScriptLegacy`'s line callback, synchronously. **Fix shape:** stop at EOF, check `find`, and fail the pairing with a sentence.
- **Can this be done on the VM?** Yes. A fixture over the two functions with an empty and a malformed conf, under a watchdog (`fix-unit-test`).
- **Already written:** nothing inherited (a parser).
- **Acceptance:**
  - [ ] the fixture: both inputs return within the watchdog, with no exception (`stage-e/s6-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; one Moonlight stream with PL-03 to PL-06, PL-15 and PL-16 under rule 6 (D-QA-051), the #585 lines to ROCKNIX, whose page it is.
- **Bug:** #1241 (filed 2026-10-27, with its code trace).

## PL-07: COPY TO FREE SLOT is silent when it fails and when it works, copies on the interface thread, and releases the transfer lock before it writes (a `bug` proposed; the fork's manager)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q4
- **Family:** a check whose failure reads as success; a state write that can lose the record
- **Source Finding:** L-13 (EP-11, narrowed), L-38 (EP-38); T2's PL-016 (#782: "the manager's message to the player is `GuiSaveState`'s, a lead for #678") -- proved: guest (G06), tree (L-38)
- **Owner area:** `GuiSaveState.cpp:494-533`; `AtomicFileUtil.cpp:440-449` (T21's)
- **What:**
  - No free slot is silent. A `false` copy is silent. A `true` one rebuilds the grid with the cursor on START NEW GAME and no success word (on G06 the new tile was off-screen).
  - At the pin a failed `copyFile` takes the `true` branch (SS-4).
  - The copy runs on the interface thread.
  - The lock is probed and released before the copy, so a sync can start between them (D-CLOUD-053).

  **Fix shape:** the copy on `SaveStateBookkeeper`'s worker under the transfer lock, as DELETE is; a sentence for a failure; the cursor on the new tile.
- **Can this be done on the VM?** Yes. A fixture over the X path with a doubled `copyToSlot` and lock (`fix-unit-test`); G06 again (`fix-walk-pending-image`).
- **Already written:** a copy made by the old page is a real file with its record; nothing inherited.
- **Acceptance:**
  - [ ] the fixture: `false` → a sentence; `true` → the cursor on the new slot; no free slot → a sentence; the lock held across the copy (`stage-e/s7-*.txt`).
  - [ ] on the integration image, G06's read-only copy shows the failure sentence, and a copy that works leaves the cursor on SLOT 3 (`fix-walk-pending-image`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1242 (filed 2026-10-27, with its code trace).

## PL-08: USE RELAY SERVER and SHOW CONTROLLER ACTIVITY replace their pages without `save()`, dropping the deferred switches changed before (a `bug` proposed; upstream's)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record
- **Source Finding:** L-03 (EP-3, extended), L-35 (EP-35) -- proved: guest (G08), tree (L-35)
- **Owner area:** `GuiNetPlaySettings.cpp:155-187`; `GuiControllersSettings.cpp:200-211`
- **What:** each callback runs `delete this` and pushes a fresh page. ENABLE NETPLAY, the lobby switches and INDEX NEW GAMES AT STARTUP are dropped on one page; AUTOCONFIGURE RETROARCH HOTKEYS and the notification switches on the other. G08: `global.netplay=0` after it was switched on. **Fix shape:** `save()` before the replacement, or a rebuild in place.
- **Can this be done on the VM?** Yes. G08 again (`fix-walk-pending-image`); a fixture over each callback with doubled stores (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a fixture over both callbacks: a switch moved before each is saved (`stage-e/s8-*.txt`).
  - [ ] G08 on the integration image reads `global.netplay=1` (`fix-walk-pending-image`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1243 (filed 2026-10-27, with its code trace).

## PL-09: a failing or partial `rocknix-systems` reads as THE BIOS CHECK RETURNED NOTHING, or as ALL PRESENT (a `bug` proposed; the fork's page)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-12 (EP-10), L-39 (EP-39) -- proved: guest (G05, the empty case); tree (the partial case)
- **Owner area:** `GuiBios.cpp:158-203`, `:220-223`; `ApiSystem.cpp:872-924`, `:2233-2252` (T21's executor drops the status)
- **What:** a script that exits 1 shows the empty screen. One that prints a header and dies shows ALL PRESENT (0), and one that dies after PRESENT rows reads clean. **Fix shape:** the run's status reaches the page; a failed or partial check says so, with REFRESH and French.
- **Can this be done on the VM?** Yes. A fixture over `loadList` with a doubled result and status; G05 again with a header-then-exit-1 script.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the fixture: a failed run, a partial run and an empty run each show their own sentence, with French (`stage-e/s9-*.txt`; `es-untranslated` 0 without).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1244 (filed 2026-10-27, with its code trace).

## PL-10: BIOS CHECK draws no help bar under full-screen menus; DETAILS and START (REFRESH) are never shown (a `bug` proposed; the fork's page)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a page with no help bar
- **Source Finding:** L-26 (EP-14, narrowed) -- proved: guest (G05, G12)
- **Owner area:** `GuiBios.cpp:293-324`; the pattern at `GuiSaveState.cpp:397-398`
- **What:** the page never calls `renderHelpPromptsEarly`. REFRESH is a visible button, but DETAILS and the START shortcut are on no bar. DETAILS is offered whenever `mBios` is non-empty, wherever the focus is. **Fix shape:** the manager's two lines in `render`, and DETAILS only while a row is focused.
- **Can this be done on the VM?** Yes: a 640x480 frame on the integration image (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a 640x480 frame of BIOS CHECK shows DETAILS, BACK and REFRESH on the bar with a row focused, and no DETAILS on the buttons (`fix-walk-pending-image`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1245 (filed 2026-10-27, with its code trace).

## PL-11: the BIOS summary is assembled from fragments (`7 SUR 7 MANQUANT`), and a system not loaded shows its short name (a `bug` proposed; the fork's page)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-11 (EP-25), L-27 (EP-15) -- proved: guest (G05, G12)
- **Owner area:** `GuiBios.cpp:143-156`, `:220-230`
- **What:** separately translated fragments cannot be reordered or agreed with the count. A system missing from `sSystemVector` is named `proper(shortName)`. **Fix shape:** whole-sentence msgids with a count, plural forms and French; the full name from the system definitions.
- **Can this be done on the VM?** Yes: FR and EN frames (`fix-walk-pending-image`); `es-untranslated`.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `tools/es-untranslated` 0 without, with the new msgids in the French catalog; a FR frame of BIOS CHECK reads an agreed sentence (`fix-walk-pending-image`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1246 (filed 2026-10-27, with its code trace).

## PL-12: the scrape page's outcome: an all-errored run has no why and no next step; any input, an axis included, dismisses it, even before it is drawn (a `bug` proposed; the fork's page)

- **Severity:** Low
- **Category:** UX
- **Question:** Q4
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-09 (EP-8), L-10 (EP-9, extended) -- proved: fixture (`stage-c/l09-l10-scrape-page.py`)
- **Owner area:** `GuiScraperRun.cpp:84-103`, `:138-145`, `:201-236`
- **What:**
  - Line 4 is written only when `p.failed`, and line 5 only when a game was scraped: an incomplete failure outcome, also met by partly successful runs.
  - `input` deletes on `p.finished` before `update` has drawn it, for any non-zero input.
  - The comment at `:87-89` says SCRAPER is behind; it was closed at the run's start.

  **Fix shape:** a truthful why and retry guidance for `p.errors > 0`, in words the coordinator approves, with French. Dismissal on a button, once `mShownFinished` is set.
- **Can this be done on the VM?** Yes. The fixture (`fix-unit-test`); the frames need a network scrape with failures (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the fixture against the fixed page passes, with a case for input arriving before the finished frame (`stage-e/s10-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1247 (filed 2026-10-27, with its code trace).

## PL-13: `SKIPPED - YOU CANCELLED IT` is a fourth SKIPPED reason (a design item, for the pause)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-08 (EP-7) -- proved: design
- **Owner area:** `GuiScraperRun.cpp:132-145`
- **What:** `es-player-text.md` § Outcome vocabulary and D-UI-028 reserve SKIPPED for rclone 69, 75 and the launch cancel. The page's comment argues that the player's own cancel is a skip; no register row records it. **Options:** a register row admitting the reason, or the cancel worded another way. The coordinator assigns the ID.
- **Can this be done on the VM?** Yes, if the words change: a frame of the cancelled page.
- **Already written:** nothing inherited (a word on a page).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** **D-UI-129** (`acb7ead172`): `SKIPPED - <reason>` admits a player's own cancel of a run they started on a fourth-tier page; `es-player-text.md` § Outcome vocabulary carries the fourth entry (the coordinator's commit). The word stays; no bug. A completed run reported as cancelled (`stop()` after `run()` finished, in `ThreadedScraper`) is T32's lead L-02 and T32's file: recorded in `02` as inherited by T32.

## PL-14: Moonlight's page title is a raw English literal, four boxes are sentence case (one misspelt), and the page is neither mapped nor declared (a `bug` proposed; ROCKNIX's page)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary; a page the map does not describe and the checker cannot see
- **Source Finding:** L-07 (EP-24) -- proved: guest (G12)
- **Owner area:** `GuiMoonlight.cpp:268`, `:295-336`; `docs/es-menu-map.md`
- **What:** `GuiSettings(window, "MOONLIGHT GAME STREAMING")` is never translated and is invisible to `es-menu-map-check`. "Succesfully paired with server" and three more are sentence-case prose. The PIN is regenerated at each opening. **Fix shape:** the title through `_()`, the boxes in the house's upper case with French, and the page mapped (D-UI-039).
- **Can this be done on the VM?** Yes: FR frames; `es-menu-map-check`.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a FR frame of the page reads its title in French; `es-untranslated` 0 without; `es-menu-map-check` sees MOONLIGHT GAME STREAMING as mapped (`fix-walk-pending-image`, `tool-run`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed, for the title: it goes through `_()` (an untranslatable string is a defect, not a word choice) and the page is mapped in the same commit (D-UI-039); the sentence-case box wording stays as ROCKNIX wrote it (D-UI-079), recorded.
- **Bug:** #1248 (filed 2026-10-27, with its code trace).

## PL-15: Moonlight's `isEmbedded()` reads a pointer, not the output, and leaks a `popen` per call (a `bug` proposed; ROCKNIX's page)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-31 (EP-31) -- proved: tree
- **Owner area:** `GuiMoonlight.cpp:40-50`, `:301-306`
- **What:** `ss << mlver` streams the `FILE*`'s address, so the function is always false, and the stream is never `pclose`d. **Fix shape:** a bounded, checked read of the output and a `pclose`.
- **Can this be done on the VM?** Yes. A fixture with a stub `moonlight -v` printing "Embedded" (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the fixture: "Embedded" from the stub makes `isEmbedded()` true; a second call leaves no open descriptor (`stage-e/s11-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; one Moonlight stream with PL-03 to PL-06, PL-15 and PL-16 under rule 6 (D-QA-051), the #585 lines to ROCKNIX, whose page it is.
- **Bug:** #1249 (filed 2026-10-27, with its code trace).

## PL-16: Moonlight writes the client's private key with no explicit mode (a `bug` proposed if the image's mode reads open; ROCKNIX's page)

- **Severity:** Low
- **Category:** Security
- **Question:** Q2
- **Family:** a credential's sink
- **Source Finding:** L-33 (EP-33, accepted in part) -- proved: tree (the writer); the mode on the image unread
- **Owner area:** `GuiMoonlight.cpp:79-100`, `:145-147`
- **What:** a plain `ofstream` creates `key.pem`, so its mode is the umask's and the directory's. **Fix shape:** create it 0600 (`Utils::AtomicFile::writeText` with a mode, or `open` with 0600).
- **Can this be done on the VM?** Yes: on a guest, a seeded conf and a pairing callback, then `stat` the key (`fix-walk-pending-image`); or a fixture under umask 022.
- **Already written:** a key already extracted keeps its mode; the fix's writer should also tighten an existing file.
- **Acceptance:**
  - [ ] a fixture under umask 022: `key.pem` created and replaced at 0600 (`stage-e/s12-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; one Moonlight stream with PL-03 to PL-06, PL-15 and PL-16 under rule 6 (D-QA-051), the #585 lines to ROCKNIX, whose page it is; a bug whether or not the image reads the file open (an explicit mode on a key is the fix); the VM line reads the mode on the guest at the stream's proof, labelled by side.
- **Bug:** #1250 (filed 2026-10-27, with its code trace).

## PL-17: the map: BIOS CHECK and SCRAPING GAMES (the fork's) are in neither the map nor `## Not mapped`, with ten upstream titles (D-UI-039)

- **Severity:** Low
- **Category:** Docs
- **Question:** Q7
- **Family:** a page the map does not describe and the checker cannot see
- **Source Finding:** L-24 (EP-27) -- proved: tool-run (`tools/t31-titles.py`)
- **Owner area:** `docs/es-menu-map.md`
- **What:** the twelve titles with their proposed dispositions are in `02` § The titles: BIOS CHECK and SCRAPING GAMES mapped, the ten upstream declared with reasons. The checker's blind spot is #951's and #965's; this table is their evidence from the pages' side.
- **Can this be done on the VM?** Yes (`tool-run`).
- **Already written:** nothing inherited (a document).
- **Acceptance:**
  - [ ] `tools/t31-titles.py` reports 0 pages in neither place once the map changes, and `es-menu-map-check` prints `0 missing` (`tool-run`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** the map commit (D-UI-039), in a stream's commit; no bug.

## PL-18: `GuiLoading`'s `mRunning` is a plain `bool` across its two threads, and its thread object leaks (a `bug` proposed; batocera's header)

- **Severity:** Low
- **Category:** Reliability
- **Question:** Q3
- **Family:** work on the interface thread
- **Source Finding:** L-22 (EP-21, extended) -- proved: fixture (`stage-c/l22-guiloading-race.py`: 2 ThreadSanitizer races)
- **Owner area:** `GuiLoading.h`
- **What:** the worker publishes `result` and `mRunning` with no ordering, and `update` copies `result` before the join. The `std::thread` object is never deleted. **Fix shape:** `std::atomic<bool>` with release/acquire, and the thread owned by value (or deleted after the join).
- **Can this be done on the VM?** Yes: the fixture under ThreadSanitizer, with a leak check (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `stage-c/l22-guiloading-race.py` against the fixed header: no ThreadSanitizer warning, completion 42, no leak under LeakSanitizer (`stage-e/s13-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1251 (filed 2026-10-27, with its code trace).

## PL-19: the image viewer guards its pool jobs with a plain global rather than the instance, and abandons an unpushed viewer whose first extraction is empty (a `bug` proposed; upstream's)

- **Severity:** Low
- **Category:** Reliability
- **Question:** Q3
- **Family:** work on the interface thread
- **Source Finding:** L-40 (EP-40), L-41 (EP-41) -- proved: tree
- **Owner area:** `GuiImageViewer.cpp:272-277`, `:362-399`, `:501-545`, `:692-712`
- **What:**
  - `g_isGuiImageViewerRunning` is read from pool jobs, which is a race. A later viewer sets it true for an old viewer's posted callbacks.
  - An empty first extraction returns with the viewer neither pushed nor deleted, its pool started.

  **Fix shape:** an instance life token (`GuiSettings::lifeToken`'s shape), and the unpushed viewer deleted on failure, with a sentence.
- **Can this be done on the VM?** Yes. Fixtures under ThreadSanitizer and AddressSanitizer with a delayed callback (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the fixtures: no race on the guard; viewer A's callback after B's construction touches nothing of A; an empty extraction leaves no live viewer (`stage-e/s14-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1252 (filed 2026-10-27, with its code trace).

## PL-20: PLAYER PASSWORD is shown in clear on the row and in its editor (a `bug` proposed; upstream's row)

- **Severity:** Low
- **Category:** Security
- **Question:** Q2
- **Family:** a credential's sink
- **Source Finding:** L-04 (EP-6) -- proved: tree
- **Owner area:** `GuiGameOptions.cpp:204`
- **What:** `addInputTextConfigRow(_("PLAYER PASSWORD"), "global.netplay.password", false)`. batocera's is the same (`:198`). **Fix shape:** `password = true`.
- **Can this be done on the VM?** Yes: the rows table and a frame of the row.
- **Already written:** nothing inherited (a display mode).
- **Acceptance:**
  - [ ] `tools/t31-rows.py` reads `password` for `GuiGameOptions.cpp:204` (`tool-run`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1253 (filed 2026-10-27, with its code trace).

## PL-21: SCRAPER's remembered filters: the default set stored on a first visit, an empty selection unkeepable, and a change of SCRAPE FROM leaving the filters bound to the old scraper (a `bug` proposed; the fork's remembered filters)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a row whose store is wrong; a check whose failure reads as success
- **Source Finding:** L-15 (EP-13), L-16 (EP-4: the cause withdrawn, the observation kept), L-42 (EP-42) -- proved: guest (G03), tree (L-42)
- **Owner area:** `GuiScraperStart.cpp:34-37`, `:83-133`, `:166-215`
- **What:**
  - With `currentSystem` empty, the first tab switch or close stores the default set (`ScraperSystems="pico-8"`), so a system added later is not selected. "None" saves `""`, which reads back as nothing remembered.
  - A first visit rewrote `es_settings.cfg` twice; which save function set `mWasChanged` is not recorded.
  - SCRAPE FROM only updates the setting, so the filters and systems keep the old scraper until the tab is rebuilt.

  **Fix shape:** write `ScraperSystems` only when the selection moved, with a distinct value for "none"; rebuild the SCRAPE tab when the source changes.
- **Can this be done on the VM?** Yes. A fixture over the SCRAPE tab with two scraper doubles and doubled stores (`fix-unit-test`); G03 again.
- **Already written:** a device that visited SCRAPER holds a `ScraperSystems` list. The fix reads it as before; no migration.
- **Acceptance:**
  - [ ] the fixture: no write on an unchanged first visit; an empty selection kept; the queue after a source change uses the new scraper (`stage-e/s15-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1254 (filed 2026-10-27, with its code trace).

## PL-22: `addInputTextRow`'s editor reopens from the value captured at build, so an unchanged OK writes the old value back (a `bug` proposed; upstream's base)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record
- **Source Finding:** L-37 (EP-37) -- proved: tree
- **Owner area:** `GuiSettings.cpp:260-337`; `GuiKeyboardtopads.cpp:168`
- **What:** the accept handler captures `value`, and `updateVal` changes the display and calls `onsave` but not the captured value. **Fix shape:** keep the current value beside the row (not the masked text).
- **Can this be done on the VM?** Yes. A fixture over the builder (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the fixture: A → B, reopen, OK without editing → B stays (`stage-e/s16-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1255 (filed 2026-10-27, with its code trace).

## PL-23: the save state manager's incremental sort uses `>=` in a `std::sort` comparator (a `bug` proposed; upstream's lines in the fork's file)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Family:** work on the interface thread
- **Source Finding:** L-43 (EP-43) -- proved: tree
- **Owner area:** `GuiSaveState.cpp:268-278`
- **What:** equal creation dates make the comparator true both ways, which breaks strict weak ordering (undefined behaviour). **Fix shape:** `>` with a stable tie-break (the slot).
- **Can this be done on the VM?** Yes. A fixture over the comparator: irreflexivity, and the sort under `_GLIBCXX_DEBUG` (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] the fixture: the comparator irreflexive and asymmetric on equal dates; the debug sort clean (`stage-e/s17-*.txt`).
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** a `bug`, filed; its stream in `docs/reviews/briefs/t31-streams.md` (the coordinator's).
- **Bug:** #1256 (filed 2026-10-27, with its code trace).

## PL-24: four back landings act: CONTROLLER MAPPING's OK, the metadata editor's saving NO, the two SAVE CHANGES? boxes' discarding NO (recorded; D-UI-079, for the pause)

- **Severity:** Low
- **Category:** UX
- **Question:** Q1
- **Family:** a dialog whose back lands on the acting choice
- **Source Finding:** L-19, L-20, L-21 (EP-18 to EP-20) -- proved: tree
- **Owner area:** `GuiControllersSettings.cpp:74-83`, `GuiMetaDataEd.cpp:520-528`, `:626-632`, `GuiKeyMappingEditor.cpp:489-502`
- **What:** `GuiMsgBox`'s rule (`:116-134`) lands back on OK or NO, else the last button, so reordering does not change it. These are upstream pages outside the fork's lanes, so a change of behaviour is the maintainer's to open (D-UI-079). DELETE COLLECTION's NO only navigates. **Options:** recorded as written; or an explicit accelerator on each (CANCEL, keep editing).
- **Can this be done on the VM?** Yes: the dialog table (`t31-dialogs.py`).
- **Already written:** nothing inherited.
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** recorded as written, with #585 lines (D-UI-079: CONTROLLER MAPPING and the metadata editor are upstream pages outside the lanes), one line per landing in `02` § The #585 lines owed.

## PL-25: `GuiAutoScrape` is not compiled and nothing opens it; the inventory records its two paths as shipped

- **Severity:** Low
- **Category:** Maintainability
- **Question:** Q7
- **Family:** --
- **Source Finding:** L-23 (EP-26 not kept: `es-app/CMakeLists.txt:315` lists `ES_SOURCES`, without it) -- proved: tool-run
- **Owner area:** `es-app/src/guis/GuiAutoScrape.*`; `docs/reviews/inventory.json` (the coordinator's)
- **What:** dead upstream code, counted in the slice's 76. **Options:** correct the inventory's reach (the coordinator's file); leave the files as upstream has them, or remove them with a #585 note.
- **Can this be done on the VM?** Yes (`tool-run`).
- **Already written:** nothing inherited.
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** Backlog **#1235** (the coordinator's): the inventory's `reach` derives from the CMake source lists, so a source compiled nowhere reads `unbuilt`; the two files stay as upstream has them.

## PL-26: interface-thread work recorded: the image viewer's library walk on an uncached lookup; SCRAPER's worker reading the page's components

- **Severity:** Low
- **Category:** Reliability
- **Question:** Q3
- **Family:** work on the interface thread
- **Source Finding:** L-17 (EP-22), L-18 (EP-23) -- proved: tree
- **Owner area:** `GuiImageViewer.cpp:279-286`, `:675-681` with `DisplayAspect.cpp:66-119` (another slice's); `GuiScraperStart.cpp:475-518`
- **What:** recorded with lines for the slices that own `DisplayAspect` and `GuiLoading`'s callers. Moving the walk needs a safe snapshot of `SystemData`. G10 (the timing) could not run.
- **Can this be done on the VM?** Yes, with a seeded library: the viewer's first open timed.
- **Already written:** nothing inherited.
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** recorded as written; no bug.

## PL-27: `isFlockHeld`'s failures read as A SYNC IS ALREADY RUNNING (keep an eye on)

- **Severity:** Low
- **Category:** UX
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-14 (EP-12, extended) -- proved: tree
- **Owner area:** `GuiSaveState.cpp:26-36`; `AtomicFileUtil.cpp:440-449` (T21's)
- **What:** an open failure other than ENOENT, or a failed `flock` other than EINTR, is read as held. That fails closed, which is right, but with words that blame a sync. ES runs as root on the image (G01). Proposed as `keep an eye on` (`bugs-are-agent-first.md`). It becomes a bug on a journal line of a refusal with no sync running.
- **Can this be done on the VM?** No reachable input on the image (root); a host fixture can show the words.
- **Already written:** nothing inherited.
- **Disposition (ruled 13:27 UTC, #678 comment 6443081619):** keep an eye on (`bugs-are-agent-first.md`); no bug.

## Phase 7 resolution gate

Stage F, 2026-10-27: every item at its outcome, the table and the index rewritten together. The ES commits are on `feature/m6-es-pages-678` (pixelelated/emulationstation), fixed-at-es `95852f873`; each stream's before, after and checks are under `stage-e/`, and `02` § The streams carries one row per stream.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Resolved | Resolved in `9cb0e5c9a` (ES, S1) under #1236 and D-UI-128: START, CLOSE and an outside click close each settings page through `close()` from the top (`GuiSettings::closeAllFromTop`), stopping at a page an `onFinalize` pushed (`stage-e/s1-*.txt`); a #585 line |
| PL-02 | Resolved | Resolved in `1ca322f75` (ES, S2) under #1237: `save()` writes the stores on every close, with or without a save function (`stage-e/s2-*.txt`); GuiMenu's four workaround saves are merge debt in `02`; a #585 line |
| PL-03 | Resolved | Resolved in `70db6535b` (ES, S3) under #1238: every value handed to the shell quoted, the launcher's file name kept to what a shell reads as itself; `credential-quoting.py` 9 to 11 sites (`stage-e/s3-*.txt`); a #585 line |
| PL-04 | Resolved | Resolved in `70db6535b` (ES, S3) under #1239: fetch and parse first, the new set swapped in whole, every write checked, the library as it was on a failure (`stage-e/s3-*.txt`); a #585 line |
| PL-05 | Resolved | Resolved in `70db6535b` (ES, S3) under #1240: the literal `/storage` paths removed and checked, the box true only when both are gone (`stage-e/s3-*.txt`); a #585 line |
| PL-06 | Resolved | Resolved in `70db6535b` (ES, S3) under #1241: one bounded conf reader, nothing written on a missing or malformed value, its failure said (`stage-e/s3-*.txt`); a #585 line |
| PL-07 | Resolved | Resolved in `f9b97b3ea` (ES, S4) under #1242: the copy made on the worker under the transfer lock, checked by its size, and said both ways (`stage-e/s4-*.txt`); `SaveState.cpp`'s half is T2's under #782 |
| PL-08 | Resolved | Resolved in `82f80693d` (ES, S5) under #1243: `save()` before each page is replaced (`stage-e/s5-*.txt`); two #585 lines |
| PL-09 | Deferred | Deferred: #1244 -- S6b is the patch `stage-e/s6b.patch` with `s6b-fr.po`, proven on a scratch tree of T21's `a73ed9efc` (`stage-e/s6b-*`), for the integration to apply after T21's merge (the coordinator's ruling of 15:12 UTC); T21's `a73ed9efc` carries the failed case |
| PL-10 | Resolved | Resolved in `95852f873` (ES, S6a) under #1245: the help bar drawn under full-screen menus, DETAILS only on a system's row (`stage-e/s6a-*.txt`) |
| PL-11 | Resolved | Resolved in `95852f873` (ES, S6a) under #1246: the summary one sentence per count through the catalog's plural forms, an unloaded system's full name from the definitions (`stage-e/s6a-*.txt`) |
| PL-12 | Resolved | Resolved in `2fa6b5f73` (ES, S7) under #1247: the why and the next step on the finished page, a button dismissing it once drawn (`stage-e/s7-*.txt`) |
| PL-13 | Resolved | Resolved by D-UI-129 as ruled on #678 (13:27 UTC, comment 6443081619): the word stays; the completed run reported as cancelled is T32's L-02, inherited in `02` |
| PL-14 | Resolved | Resolved in `70db6535b` (ES, S3) under #1248, the title through `_()`, and the map in `babec2f359` (distribution), MOONLIGHT GAME STREAMING under GAME SETTINGS > TOOLS (`stage-e/s3-*.txt`); a #585 line |
| PL-15 | Resolved | Resolved in `70db6535b` (ES, S3) under #1249: the probe read and closed (`stage-e/s3-*.txt`); a #585 line |
| PL-16 | Resolved | Resolved in `70db6535b` (ES, S3) under #1250: the key written 0600, an existing one narrowed at the page's open (`stage-e/s3-*.txt`); a #585 line |
| PL-17 | Resolved | Resolved in `50f5d08ccd` (distribution, S8) and `ee8ac47dd6`'s record, under #1234: BIOS CHECK and SCRAPING GAMES mapped; the ten upstream declarations wait as comments on #951/#965 (the ruling of 14:27 UTC; `stage-e/s8-*.txt`) |
| PL-18 | Resolved | Resolved in `1f06113e0` (ES, S9) under #1251: an atomic flag, the result read after the join, the thread owned (`stage-e/s9-*.txt`); a #585 line |
| PL-19 | Resolved | Resolved in `b71d656d9` (ES, S10) under #1252: a life token per viewer, an unfilled viewer deleted with a toast (`stage-e/s10-*.txt`); a #585 line |
| PL-20 | Resolved | Resolved in `a8dcc23ea` (ES, S11) under #1253: PLAYER PASSWORD masked (`stage-e/s11-*.txt`); a #585 line |
| PL-21 | Resolved | Resolved in `a8beab553` (ES, S12) under #1254: only a moved selection written, an empty one kept as `none`, the filters rebuilt on SCRAPE FROM (`stage-e/s12-*.txt`) |
| PL-22 | Resolved | Resolved in `03a929e02` (ES, S13) under #1255: the editor reopens from the value last saved (`stage-e/s13-*.txt`); a #585 line |
| PL-23 | Resolved | Resolved in `bc3959c69` (ES, S14) under #1256: a strict ordering, the slot breaking a tie (`stage-e/s14-*.txt`) |
| PL-24 | Deferred | Deferred: #585 -- recorded as written, four lines in `02` § The #585 lines owed, as ruled on #678 (13:27 UTC; D-UI-079) |
| PL-25 | Deferred | Deferred: #1235 (a Backlog, the coordinator's), as ruled on #678 (13:27 UTC): the inventory's reach from the CMake source lists; the files stay as upstream has them |
| PL-26 | Deferred | Deferred: #678's inheritance -- recorded as written in `02` § What T32 to T37 inherit, for the slices that own `DisplayAspect.cpp` and SCRAPER's worker, as ruled on #678 (13:27 UTC); no bug |
| PL-27 | Withdrawn | Withdrawn as a bug: keep an eye on (`bugs-are-agent-first.md`), as ruled on #678 (13:27 UTC, comment 6443081619); a journal line naming an open failure turns it into one |

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-01, L-34"
  outcome: "resolved"
- id: PL-02
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-02, L-36"
  outcome: "resolved"
- id: PL-03
  severity: "Medium"
  category: Security
  question: Q6
  source_finding: "L-05, L-28"
  outcome: "resolved"
- id: PL-04
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-29, L-30"
  outcome: "resolved"
- id: PL-05
  severity: "Medium"
  category: Correctness
  question: Q4
  source_finding: "L-06"
  outcome: "resolved"
- id: PL-06
  severity: "Medium"
  category: Reliability
  question: Q3
  source_finding: "L-32"
  outcome: "resolved"
- id: PL-07
  severity: "Medium"
  category: Correctness
  question: Q4
  source_finding: "L-13, L-38"
  outcome: "resolved"
- id: PL-08
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-03, L-35"
  outcome: "resolved"
- id: PL-09
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-12, L-39"
  outcome: "deferred"
- id: PL-10
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-26"
  outcome: "resolved"
- id: PL-11
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-11, L-27"
  outcome: "resolved"
- id: PL-12
  severity: "Low"
  category: UX
  question: Q4
  source_finding: "L-09, L-10"
  outcome: "resolved"
- id: PL-13
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-08"
  outcome: "resolved"
- id: PL-14
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-07"
  outcome: "resolved"
- id: PL-15
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-31"
  outcome: "resolved"
- id: PL-16
  severity: "Low"
  category: Security
  question: Q2
  source_finding: "L-33"
  outcome: "resolved"
- id: PL-17
  severity: "Low"
  category: Docs
  question: Q7
  source_finding: "L-24"
  outcome: "resolved"
- id: PL-18
  severity: "Low"
  category: Reliability
  question: Q3
  source_finding: "L-22"
  outcome: "resolved"
- id: PL-19
  severity: "Low"
  category: Reliability
  question: Q3
  source_finding: "L-40, L-41"
  outcome: "resolved"
- id: PL-20
  severity: "Low"
  category: Security
  question: Q2
  source_finding: "L-04"
  outcome: "resolved"
- id: PL-21
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-15, L-16, L-42"
  outcome: "resolved"
- id: PL-22
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-37"
  outcome: "resolved"
- id: PL-23
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-43"
  outcome: "resolved"
- id: PL-24
  severity: "Low"
  category: UX
  question: Q1
  source_finding: "L-19, L-20, L-21"
  outcome: "deferred"
- id: PL-25
  severity: "Low"
  category: Maintainability
  question: Q7
  source_finding: "L-23"
  outcome: "deferred"
- id: PL-26
  severity: "Low"
  category: Reliability
  question: Q3
  source_finding: "L-17, L-18"
  outcome: "deferred"
- id: PL-27
  severity: "Low"
  category: UX
  question: Q4
  source_finding: "L-14"
  outcome: "withdrawn"
```
