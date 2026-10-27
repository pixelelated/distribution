# Punch list — M6.P2 T31, EmulationStation's other pages (#678)

Written by the first reader (Opus 5.5) at stage C, from `02` § Leads, `04` § Risk assessment, the guest cycle, the stage-C harnesses and `stage-c/astra-grades.md`.

- **reviewed-at:** `da7922a7bd` (distribution), **reviewed-at-es:** `16dbac5211` (the pin). **fixed-at** and **fixed-at-es:** at stage F.
- **Independent depth:** one seat, GPT-6 Astra at `max` (§ Second opinion in `04`).
- **One item per defect or reusable improvement**, however many leads found it, ordered by severity. Not an item: L-25 (a real seed, recorded).
- **Nothing here changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. A fix lands only under a stream brief on the ES branch, proven twice. A row added, moved or renamed updates `docs/es-menu-map.md` in the same commit (D-UI-039).
- **Lines** are the pin's. "Guest" means the M6 image (M7's composition over the pin); "fixture" means a stage-C harness that fails at the pin and passes its control.

---

## PL-01: START (CLOSE on every settings page) deletes the pages without `close()`, so every open page's unsaved choices are dropped (a `bug` proposed; upstream's base)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record
- **Source Finding:** L-01 -- proved: fixture (`stage-c/l01-start-drops.py`), guest (G02)
- **Owner area:** `GuiSettings.cpp:106-112` (`input`), `:133-139` (the bar's CLOSE); the same loop in `GuiScraperStart.cpp:542-548` and `GuiMetaDataEd.cpp:620-624`
- **What:** START runs `delete window->peekGui()` until the view, so no page's `save()` or `onFinalize` runs. A switch moved and then CLOSE is lost where BACK keeps it. Every `GuiSettings` page, the fork's cloud pages included, applies its rows on close. Identical in `batocera/master` (`b2ceb55a7`) and `rocknix/master`. **Fix shape:** close each page through its own `close()` in turn, or offer CLOSE only where it applies. An `onFinalize` that pushes a page or a toast must be read first. This is upstream behaviour reaching the fork's lanes, so the shape is put to the coordinator.
- **Can this be done on the VM?** Yes. The harness (`fix-unit-test`), and the guest step G02 again on the image (`fix-walk-pending-image`).
- **Already written:** nothing inherited. The lost choices were never written, and the fix changes when the stores are written, not what they hold.
- **Acceptance:**
  - [ ] `stage-c/l01-start-drops.py` against the fixed `GuiSettings.cpp` prints `2 cases` (rc 0); against the pin it fails (`stage-e/s1-before.txt`, `s1-after.txt`).
  - [ ] on the integration image, USER INTERFACE SETTINGS > SHOW RETROACHIEVEMENTS ICON moved and START pressed: `es_settings.cfg` carries the change (`fix-walk-pending-image`).
- **question:** Q2 -- the shape for the pause: close each page in turn, or change what CLOSE offers?

## PL-02: a `GuiSettings` page with no save function never writes the stores on close; the analog sticks' LED colour is lost at every restart (a `bug` proposed; the base and ROCKNIX's page)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record
- **Source Finding:** L-02 -- proved: fixture (`stage-c/l02-led-not-saved.py`); T26's PL-17 (deferred to #678: four GuiMenu sub-pages work around the same return with `onFinalize` saves)
- **Owner area:** `GuiSettings.cpp:83-96` (`save()` returns when `mSaveFuncs` is empty); `GuiAnalogSticksLedControls.cpp:62-87`
- **What:** the LED page sets `analogsticks.led` in memory at each slider step and registers no save function, so `save()` never calls `saveSystemConf`. Nothing saves `system.cfg` at exit, and the quirks' `ledcontrol` reads the key at boot. Each slider step also runs the script on the interface thread. **Fix shape:** `save()` writes the stores whenever they changed, whether or not the page has a save function; or the LED page adds its own. T26's four workarounds are then removable.
- **Can this be done on the VM?** Yes for the save, by the harness (`fix-unit-test`). The row appears only with `DEVICE_ANALOG_STICKS_LED_CONTROL=true` (`GuiMenu.cpp:2197`), so the guest walk needs that variable set for ES.
- **Already written:** a device whose `system.cfg` holds an old colour keeps it, and the page reads it at open (`:16-27`). The fix writes the next change; nothing to migrate.
- **Acceptance:**
  - [ ] `stage-c/l02-led-not-saved.py` against the fixed files: `analogsticks.led saved` (rc 0); against the pin it fails (`stage-e/s2-*.txt`).
  - [ ] the four `onFinalize` saves T26's PL-17 named either still work or are removed, by the fixture over `save()`.

## PL-03: Moonlight's SERVER IP reaches the shell unquoted in three commands (a `bug` proposed; ROCKNIX's page)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q6
- **Family:** a command built from a player's string
- **Source Finding:** L-05 -- proved: fixture (`stage-c/l05-l06-moonlight.py`: the canary made by all three)
- **Owner area:** `GuiMoonlight.cpp:282`, `:304`, `:306`; the pairing reader `:310-311`
- **What:** `snprintf(cmd, ..., "moonlight quit %s", server_ip)` and the two pair forms go to `executeScriptLegacy`, which is `popen` (`ApiSystem.cpp:2269`). `127.0.0.1;touch …` runs the second command as root. **Fix shape:** `Utils::String::shellQuote` on the IP (T26's one quoting function), or the argv executor `WifiScanProcess.h` models (#1192).
- **Can this be done on the VM?** Yes. The fixture (`fix-unit-test`); the guest with a canary in SERVER IP typed through the keyboard (`fix-walk-pending-image`).
- **Already written:** a `moonlight.host` already stored with shell metacharacters is quoted by the fix at its next use; nothing to migrate.
- **Acceptance:**
  - [ ] `stage-c/l05-l06-moonlight.py` against the fixed `GuiMoonlight.cpp` prints `moonlight: PASS`, and the argv log shows the whole IP as one argument (`stage-e/s3-*.txt`).

## PL-04: UNPAIR WITH SERVER removes nothing (`"~/..."` is not expanded) and says "Unpaired and settings cleared" (a `bug` proposed; ROCKNIX's page)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-06 -- proved: fixture, guest (G09)
- **Owner area:** `GuiMoonlight.cpp:328-338`
- **What:** a tilde inside double quotes is literal to the shell, so both `rm -r` exit 1 and the directories stay. The page does not read the result. **Fix shape:** the paths from `$HOME` (or `Paths`) quoted after expansion, the result checked, and a sentence for a failure.
- **Can this be done on the VM?** Yes. The fixture; guest G09 again (`fix-walk-pending-image`).
- **Already written:** a device whose player pressed UNPAIR still holds the pairing. The next UNPAIR after the fix removes it; nothing else inherited.
- **Acceptance:**
  - [ ] the fixture against the fixed file: `L-06 directories left: none`, and a removal that fails is reported (`stage-e/s3-*.txt`).

## PL-05: COPY TO FREE SLOT says nothing when it fails or when it works, and copies on the interface thread (a `bug` proposed; the fork's manager)

- **Severity:** Medium
- **Category:** UX
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-13; T2's PL-016 (#782: "the manager's message to the player is `GuiSaveState`'s, a lead for #678") -- proved: guest (G06)
- **Owner area:** `GuiSaveState.cpp:494-533`
- **What:**
  - With no free slot, the press does nothing (`:514`).
  - A failed copy, over a read-only directory, gives no message and no tile. At the pin `copyToSlot` returns `true` over an unchecked `copyFile` (SS-4); with T2's `f11e7528a` it returns `false` and the page says nothing.
  - A successful 64 MB copy rebuilds the grid with the cursor on START NEW GAME and the new tile off-screen: the same frame as the failure.
  - The copy runs on the interface thread (blindspot 45's sibling; D-UI-073 moved DELETE to a worker).

  **Fix shape:** the copy on `SaveStateBookkeeper`'s worker, with a sentence for a failure; the cursor put on the new tile after a success.
- **Can this be done on the VM?** Yes. A unit case over the page's copy path with a doubled `copyToSlot` (`fix-unit-test`); G06 again (`fix-walk-pending-image`).
- **Already written:** a copy recorded by the old page is a real file with its record; nothing inherited.
- **Acceptance:**
  - [ ] a fixture over `GuiSaveState::input`'s X path: `copyToSlot` false → a sentence; true → the cursor on the new slot; no free slot → a sentence (`stage-e/s5-*.txt`).
  - [ ] on the integration image, G06's read-only copy shows the failure sentence, and a copy that works leaves the cursor on SLOT 3 (`fix-walk-pending-image`).

## PL-06: changing USE RELAY SERVER replaces NETPLAY SETTINGS without `save()`, dropping ENABLE NETPLAY and every row applied on close (a `bug` proposed; upstream's)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a state write that can lose the record
- **Source Finding:** L-03 -- proved: guest (G08)
- **Owner area:** `GuiNetPlaySettings.cpp:155-187`
- **What:** the option list's callback runs `delete this` and pushes a new page; `save()` never runs. ENABLE NETPLAY switched on, then a relay change and BACK, leaves `global.netplay=0`. **Fix shape:** `save()` before the replacement (as `close()` would), or rebuild the rows in place.
- **Can this be done on the VM?** Yes. G08 again (`fix-walk-pending-image`); a unit case over the callback with doubled stores (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a fixture over the relay callback: a switch moved before it is saved (`stage-e/s6-*.txt`).
  - [ ] G08 on the integration image reads `global.netplay=1` (`fix-walk-pending-image`).

## PL-07: a failing `rocknix-systems` reads as THE BIOS CHECK RETURNED NOTHING, with no recovery (a `bug` proposed; the fork's page)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-12 -- proved: guest (G05)
- **Owner area:** `GuiBios.cpp:183-203`; `ApiSystem.cpp:872-886` (T21's executor, which returns lines only)
- **What:** a script that exits 1 and a check that knows no systems are one screen. **Fix shape:** the page tells an empty result from a failed run (the status the executor drops) and says what to do (REFRESH, or the log for us), in the house's words with French.
- **Can this be done on the VM?** Yes. A unit case over `loadList` with a doubled result; G05 again.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a fixture over the BIOS page: a failed run and an empty run show different sentences, both with French (`stage-e/s7-*.txt`; `es-untranslated` 0 without).

## PL-08: BIOS CHECK draws no help bar under full-screen menus, so DETAILS and REFRESH are never offered (a `bug` proposed; the fork's page)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a page with no help bar
- **Source Finding:** L-26 -- proved: guest (G05, G12)
- **Owner area:** `GuiBios.cpp:293-324`; the pattern at `GuiSaveState.cpp:397-398`
- **What:** a full-screen `GuiComponent` page must draw its own bar (`es-code-traps.md`, the window paragraph). BIOS CHECK defines `getHelpPrompts` and never calls `renderHelpPromptsEarly`. **Fix shape:** the manager's two lines in `render`.
- **Can this be done on the VM?** Yes: a 640x480 frame of BIOS CHECK on the integration image (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a 640x480 frame of BIOS CHECK shows DETAILS, BACK and REFRESH on the bar (`fix-walk-pending-image`).

## PL-09: the BIOS summary is built word by word (`7 SUR 7 MANQUANT`), and a system without games shows its short name (Nds, Psx, Gb) (a `bug` proposed; the fork's page)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-11, L-27 -- proved: guest (G05, G12)
- **Owner area:** `GuiBios.cpp:143-156`, `:220-230`
- **What:** `N + OF + M + MISSING` reads in English order in French, with no plural. A system with no games is named `Utils::String::proper(name)`. **Fix shape:** whole-sentence msgids with a count (`%i OF %i MISSING`) and their French; the full name from the system list where it exists.
- **Can this be done on the VM?** Yes: FR and EN frames (`fix-walk-pending-image`); `es-untranslated`.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `tools/es-untranslated` 0 without, the new msgids in the French catalog; a FR frame of BIOS CHECK reads a French sentence (`fix-walk-pending-image`).

## PL-10: an all-errored scrape says COULDN'T FINISH with no why and no next step; any input, an axis included, dismisses the outcome (a `bug` proposed; the fork's page)

- **Severity:** Low
- **Category:** UX
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-09, L-10 -- proved: fixture (`stage-c/l09-l10-scrape-page.py`)
- **Owner area:** `GuiScraperRun.cpp:90-103`, `:138-145`, `:217-236`
- **What:**
  - Line 4 (the why) is written only when `p.failed`, and line 5 (the next step) only when a game was scraped.
  - `input` deletes the finished page on any non-zero input, so stick drift can clear an outcome unread.

  **Fix shape:** a why and a next step for `p.errors > 0` (D-UI-028's shape: why, what is in place, how to recover), in words the coordinator approves with French. Dismissal on a button only.
- **Can this be done on the VM?** Yes. The fixture (`fix-unit-test`); the frames need a network scrape with failures (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `stage-c/l09-l10-scrape-page.py` against the fixed page prints `3 checks` (`stage-e/s8-*.txt`).

## PL-11: `SKIPPED - YOU CANCELLED IT` is a fourth SKIPPED reason (a design item, for the pause)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary
- **Source Finding:** L-08 -- proved: design
- **Owner area:** `GuiScraperRun.cpp:132-145`
- **What:** `es-player-text.md` § Outcome vocabulary and D-UI-028 reserve SKIPPED for rclone 69, 75 and the launch cancel. The page's comment argues that the player's own cancel is a skip (nothing went wrong; the games not reached are the next scrape's). No register row records it. **Options:** a register row admitting the reason; or the cancel worded under COULDN'T FINISH. The coordinator assigns the ID.
- **Can this be done on the VM?** Yes, if the words change: a frame of the cancelled page.
- **Already written:** nothing inherited (a word on a page).

## PL-12: Moonlight's page: the title is a raw English literal, four boxes are sentence case (one misspelt), and the page is neither mapped nor declared (a `bug` proposed; ROCKNIX's page)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a player sentence outside the vocabulary; a page the map does not describe and the checker cannot see
- **Source Finding:** L-07 -- proved: guest (G12)
- **Owner area:** `GuiMoonlight.cpp:268`, `:295-336`; `docs/es-menu-map.md`
- **What:** `GuiSettings(window, "MOONLIGHT GAME STREAMING")` is never translated and is invisible to `es-menu-map-check`. "Succesfully paired with server" and three more are sentence-case prose. **Fix shape:** the title through `_()`, the boxes in the house's upper case with French, and the page mapped (D-UI-039).
- **Can this be done on the VM?** Yes: FR frames; `es-menu-map-check`.
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] a FR frame of the page reads its title in French; `es-untranslated` 0 without; `es-menu-map-check` sees MOONLIGHT GAME STREAMING and reports it mapped (`fix-walk-pending-image`, `tool-run`).

## PL-13: the map: BIOS CHECK and SCRAPING GAMES (the fork's) are in neither the map nor `## Not mapped`, with ten upstream titles (D-UI-039)

- **Severity:** Low
- **Category:** Docs
- **Question:** Q7
- **Family:** a page the map does not describe and the checker cannot see
- **Source Finding:** L-24 -- proved: tool-run (`tools/t31-titles.py`)
- **Owner area:** `docs/es-menu-map.md`
- **What:** the twelve titles with their proposed dispositions are in `02` § The titles: BIOS CHECK and SCRAPING GAMES mapped, the ten upstream declared with reasons. The checker's blind spot is #951/#965's (this table is their evidence from the pages' side).
- **Can this be done on the VM?** Yes (`tool-run`).
- **Already written:** nothing inherited (a document).
- **Acceptance:**
  - [ ] `tools/t31-titles.py` reports 0 pages in neither place once the map changes, and `es-menu-map-check` prints `0 missing` (`tool-run`).

## PL-14: `GuiLoading`'s `mRunning` is a plain `bool` across its two threads (a `bug` proposed; batocera's header)

- **Severity:** Low
- **Category:** Reliability
- **Question:** Q3
- **Family:** work on the interface thread
- **Source Finding:** L-22 -- proved: fixture (`stage-c/l22-guiloading-race.py`: 2 ThreadSanitizer races)
- **Owner area:** `GuiLoading.h` (`threadLoading`, `update`, `mRunning`, `result`)
- **What:** the worker writes `result` and then `mRunning = false`; the interface thread reads `mRunning` and then `result`, with no ordering. The `std::thread` is never deleted. **Fix shape:** `std::atomic<bool>` (release/acquire), the thread object deleted after the join.
- **Can this be done on the VM?** Yes: the fixture under ThreadSanitizer (`fix-unit-test`).
- **Already written:** nothing inherited.
- **Acceptance:**
  - [ ] `stage-c/l22-guiloading-race.py` against the fixed header: no ThreadSanitizer warning, completion 42 (`stage-e/s9-*.txt`).

## PL-15: PLAYER PASSWORD is shown in clear on the row and in its editor (a `bug` proposed; upstream's row)

- **Severity:** Low
- **Category:** Security
- **Question:** Q2
- **Family:** a credential's sink
- **Source Finding:** L-04 -- proved: tree
- **Owner area:** `GuiGameOptions.cpp:204`
- **What:** `addInputTextConfigRow(_("PLAYER PASSWORD"), "global.netplay.password", false)`: `password = false`. batocera's is the same (`:198`). **Fix shape:** `true`.
- **Can this be done on the VM?** Yes: the rows table (`t31-rows.py`) and a frame of the row.
- **Already written:** nothing inherited (a display mode).
- **Acceptance:**
  - [ ] `tools/t31-rows.py` reads `password` for `GuiGameOptions.cpp:204` (`tool-run`).

## PL-16: SCRAPER stores its default systems on a first visit and cannot keep an empty selection; a first visit rewrites `es_settings.cfg` twice with nothing chosen (a `bug` proposed; the fork's remembered filters)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a row whose store is wrong
- **Source Finding:** L-15, L-16 -- proved: guest (G03)
- **Owner area:** `GuiScraperStart.cpp:34-37`, `:102-108`, `:166-210`; `Settings.cpp:646-654`
- **What:**
  - The first tab switch or close from the main menu stores the default set (`ScraperSystems="pico-8"`), so a system added later is not selected.
  - "None" saves `""`, which reads back as nothing remembered, and every system is selected.
  - `Settings` counts a value absent from its map as a change, so the OPTIONS page's save functions rewrite the file with no content changed.

  **Fix shape:** write `ScraperSystems` only when the selection moved; a distinct value for "none"; the save functions set only a value the player moved.
- **Can this be done on the VM?** Yes. A fixture over the save functions with doubled stores (`fix-unit-test`); G03 again.
- **Already written:** a device that visited SCRAPER holds a `ScraperSystems` list. The fix reads it as before; no migration.
- **Acceptance:**
  - [ ] a fixture over the SCRAPE tab's save functions: no write on an unchanged first visit; an empty selection kept (`stage-e/s10-*.txt`).

## PL-17: three back landings press the acting choice: CONTROLLER MAPPING's OK, the metadata editor's saving NO, the two SAVE CHANGES? boxes' discarding NO (recorded; D-UI-079, for the pause)

- **Severity:** Low
- **Category:** UX
- **Question:** Q1
- **Family:** a dialog whose back lands on the acting choice
- **Source Finding:** L-19, L-20, L-21 -- proved: tree
- **Owner area:** `GuiControllersSettings.cpp:74-83`, `GuiMetaDataEd.cpp:520-528`, `:626-632`, `GuiKeyMappingEditor.cpp:493-502`
- **What:** `GuiMsgBox`'s rule (`:116-134`) lands back on OK or NO, else the last button. These are upstream pages outside the fork's lanes, so a change of behaviour is the maintainer's to open (D-UI-079). **Options:** recorded as written; or CANCEL first, or a NO that keeps the editor open.
- **Can this be done on the VM?** Yes: the dialog table (`t31-dialogs.py`).
- **Already written:** nothing inherited.

## PL-18: `GuiAutoScrape` is not compiled and nothing opens it; the inventory records its two paths as shipped

- **Severity:** Low
- **Category:** Maintainability
- **Question:** Q7
- **Family:** --
- **Source Finding:** L-23 -- proved: tool-run (the CMake grep: 0)
- **Owner area:** `es-app/src/guis/GuiAutoScrape.*`; `docs/reviews/inventory.json` (the coordinator's)
- **What:** dead upstream code, counted in the slice's 76 and its lines. **Options:** the inventory's reach corrected (the coordinator's file); the files left as upstream has them, or removed with a #585 note.
- **Can this be done on the VM?** Yes (`tool-run`).
- **Already written:** nothing inherited.

## PL-19: interface-thread work recorded: the image viewer's first open walks the library; SCRAPER's worker reads the page's components

- **Severity:** Low
- **Category:** Reliability
- **Question:** Q3
- **Family:** work on the interface thread
- **Source Finding:** L-17, L-18 -- proved: tree
- **Owner area:** `GuiImageViewer.cpp:279-286` with `DisplayAspect.cpp:74-87` (another slice's); `GuiScraperStart.cpp:475-494`
- **What:** recorded with lines for the slices that own `DisplayAspect` and `GuiLoading`'s callers. G10 (the timing) could not run.
- **Can this be done on the VM?** Yes, with a seeded library: the viewer's first open timed.
- **Already written:** nothing inherited.

## PL-20: `isFlockHeld`'s non-ENOENT failure reads as A SYNC IS ALREADY RUNNING (keep an eye on)

- **Severity:** Low
- **Category:** UX
- **Question:** Q4
- **Family:** a check whose failure reads as success
- **Source Finding:** L-14 -- proved: tree
- **Owner area:** `GuiSaveState.cpp:26-36`; `AtomicFileUtil.cpp:440-442` (T21's)
- **What:** it fails closed, which is right, but with words that blame a sync. ES runs as root on the image (G01), so EACCES is hard to reach. Proposed as `keep an eye on` (`bugs-are-agent-first.md`), with what would make it a bug: a journal line of a refusal with no sync running.
- **Can this be done on the VM?** No reachable input on the image (root); a host fixture can show the words.
- **Already written:** nothing inherited.

## Phase 7 resolution gate

At stage D every item is open, awaiting the coordinator's dispositions. Stage F rewrites this table and the index together.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | -- |
| PL-02 | Open | -- |
| PL-03 | Open | -- |
| PL-04 | Open | -- |
| PL-05 | Open | -- |
| PL-06 | Open | -- |
| PL-07 | Open | -- |
| PL-08 | Open | -- |
| PL-09 | Open | -- |
| PL-10 | Open | -- |
| PL-11 | Open | -- |
| PL-12 | Open | -- |
| PL-13 | Open | -- |
| PL-14 | Open | -- |
| PL-15 | Open | -- |
| PL-16 | Open | -- |
| PL-17 | Open | -- |
| PL-18 | Open | -- |
| PL-19 | Open | -- |
| PL-20 | Open | -- |

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-01"
  outcome: "open"
- id: PL-02
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-02"
  outcome: "open"
- id: PL-03
  severity: "Medium"
  category: Security
  question: Q6
  source_finding: "L-05"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Correctness
  question: Q4
  source_finding: "L-06"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: UX
  question: Q4
  source_finding: "L-13"
  outcome: "open"
- id: PL-06
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-03"
  outcome: "open"
- id: PL-07
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-12"
  outcome: "open"
- id: PL-08
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-26"
  outcome: "open"
- id: PL-09
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-11, L-27"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: UX
  question: Q4
  source_finding: "L-09, L-10"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-08"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-07"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Docs
  question: Q7
  source_finding: "L-24"
  outcome: "open"
- id: PL-14
  severity: "Low"
  category: Reliability
  question: Q3
  source_finding: "L-22"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Security
  question: Q2
  source_finding: "L-04"
  outcome: "open"
- id: PL-16
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-15, L-16"
  outcome: "open"
- id: PL-17
  severity: "Low"
  category: UX
  question: Q1
  source_finding: "L-19, L-20, L-21"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Maintainability
  question: Q7
  source_finding: "L-23"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: Reliability
  question: Q3
  source_finding: "L-17, L-18"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: UX
  question: Q4
  source_finding: "L-14"
  outcome: "open"
```
