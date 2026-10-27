# Retrospective audit — M6.P2 T31, EmulationStation's other pages (#678)

This was written by the first reader (Opus 5.5) after stages A and B and the guest window, before any seat saw the packet. Line numbers are the pin's (`16dbac5211`). The leads are `02`'s (L-01 to L-27).

## 3.1 Architectural coherence

- **One page, one file.** All 37 pages are each their own class in their own file. The fork's three new pages and nine changes sit where the pages already lived. Nothing here is a second copy of a GuiMenu page.
- **Two page shapes, and the help bar follows the shape.**
  - The `GuiSettings` pages get their bar from `MenuComponent`.
  - The full-screen `GuiComponent` pages must draw their own bar under full-screen menus. The fork's save state manager and scrape page do (`GuiSaveState.cpp:397-398`, `GuiScraperRun.cpp:173-174`); the fork-rebuilt BIOS CHECK does not (L-26, guest).
- **`GuiSettings` is the base every settings page stands on, and it has two exits.**
  - BACK goes through `close()`: the save functions, `saveFile`, `saveSystemConf`, then `onFinalize`.
  - START, CLOSE on the bar, deletes the pages without any of it (L-01).

  A page whose writes all happen in save functions loses them on START. A page that writes at once (`updateVal`, the LED page) keeps them in memory but writes the files only if some later `save()` runs (L-02). The base's contract is "apply on close", and one of its two closes does not apply.
- **The long jobs follow D-UI-078 where the fork works.** SCRAPING GAMES is a fourth-tier page with CANCEL; the hasher and the OS update keep upstream's cards (D-UI-079). The manager's DELETE runs on a worker (D-UI-073), and its COPY still runs on the interface thread (L-13).
- **`GuiLoading` is the async primitive of 18 call sites here and 41 lines in the tree.** It runs the work on a thread and the completion on the interface thread, and its done flag is a plain `bool` (L-22, ThreadSanitizer).

## 3.2 Project conformance

- **`least-surprise.md`:**
  - A COPY that worked and one that failed leave the same frame (L-13, guest).
  - START drops choices that B keeps (L-01, guest).
  - UNPAIR says it cleared what it did not (L-06, guest).
  - A relay change silently undoes ENABLE NETPLAY (L-03, guest).
- **`es-player-text.md` § Outcome vocabulary:**
  - SKIPPED is reserved for 69, 75 and the launch cancel, and the scrape page adds a fourth reason (L-08, for the pause).
  - An all-errored run says COULDN'T FINISH with no why and no recovery (L-09).
  - FAILED and HttpReq's own text reach the player on the netplay page (upstream's, recorded).
- **`es-player-text.md` § Every fork string ships in English and French:** the fork's strings all have French (706/706). The BIOS summary composes them in English order (L-11, guest). Moonlight's title is outside `_()` altogether (L-07, guest).
- **`es-ui-style-guide.md` § Confirmations:** YES / NO always lands on NO. OK / CANCEL lands on OK, the acting choice (L-19). Two SAVE CHANGES? boxes land on the discarding NO (L-21). One three-button box lands on a saving NO (L-20). All three are upstream's.
- **`es-native-ui.md` § Core patterns ("a file another process writes is read uncached"):** the twelve `exists` sites are all cached. Their writers are the scraper, RetroArch and the player (§ The reads), so a remembered miss can hide what a scrape just fetched. The guest positive was not reached within the bound (G11).
- **`es-code-traps.md` (the window paragraph):** BIOS CHECK is a full-screen page with no `renderHelpPromptsEarly` (L-26).
- **D-UI-039:** BIOS CHECK and SCRAPING GAMES are the fork's pages, and neither is in the map. Moonlight's page is in neither place either, and the checker cannot see it (L-24, L-07).
- **`engineering-practices.md` § Guards must fail closed:** `isFlockHeld` fails closed, with words that blame a sync (L-14).

## 3.3 Spec fidelity

The brief's figures held at their hashes (`01` § Scope, `02` § The runs), with seven corrections (`02` § Corrections to the brief), one of them the coordinator's own erratum (`:830`). Of the brief's leads:
- **Confirmed at their lines:** L-08 to L-15, L-17 and L-18.
- **Corrected:**
  - the LED parse is guarded;
  - `GuiKeyboardLayout.cpp:164` writes to `/tmp`;
  - the tab-switch writes happen for a reason other than the one the brief gave (L-16).
- **New:** L-01 to L-07, L-19 to L-23, L-26 and L-27.

## 3.4 Platform conformance

- **The image is M7's composition over the pin** (G01: both literals). Every guest verdict is the image's. The pages read here carry no M7 change that the frames contradict.
- **640x480 menus are full-screen:**
  - the manager draws its bar and shows its last tile (G06);
  - the scrape page's frames were not reached offline (G04);
  - BIOS CHECK draws no bar (G05).
- **ES runs as root** (`id -u` 0), so L-14's EACCES path is hard to reach on the image.
- **NETPLAY SETTINGS appears in GAME SETTINGS once a loaded system supports netplay** (`SystemData::isNetplayActivated`, `SystemData.cpp:2069-2072`). On the guest that was the Game Boy system G06 seeded: the row was absent at G05 and present at G12. That is the gate, not a defect.

## 3.5 Cross-system interaction audit

### Interaction: START x `GuiSettings::close` x every page's save functions

START's handler bypasses `close()`, and the pages built on `GuiSettings` depend on `close()` for their writes. That covers the fork's cloud pages (T26's) as much as SCRAPER's OPTIONS. A player who sets something and presses CLOSE loses it, while BACK keeps it (G02). The fix sits in this slice's base. Its effect reaches every page, and some `onFinalize` functions push a GUI (a reboot toast), so closing every page in turn needs reading before a stream is written (for the pause).

### Interaction: the LED page x `GuiSettings::save` x the quirks' `ledcontrol`

The page writes `system.cfg` through `SystemConf::set` (memory) and registers no save function, so `save()` returns early. The boot script reads the file. The colour survives a restart only if the player happens to close another settings page with something to save in the same session.

### Interaction: the relay option x `delete this` x `save()`

The option list's callback replaces its own page without `save()`. Every row on the page that applies on close is undone by a relay change, and ENABLE NETPLAY is the one a player notices (G08).

### Interaction: COPY TO FREE SLOT x `copyToSlot` x `loadGrid`

At the pin `copyToSlot` reports success over an unchecked copy (SS-4); T2's fix makes it truthful. The page then refreshes and rebuilds on success, which moves the cursor to the first tile. With T2's fix the page says nothing on `false`. Both paths need the page's own sentence (PL-016, #782's message).

### Interaction: Moonlight's SERVER IP x `popen` x `ParseServerIp`

The IP goes through a shell unquoted. The pairing reader writes a host it parsed back to `moonlight.host`, and the next command quotes it no better.

## 3.6 Time to play

From `docs/vm-qa-log.md`: interface to a game's first frame was 0.6 to 1.11 s in September's rows. It reads `Not measured` on 2026-10-14 and 2026-10-16, and nothing here built an image. This slice's pages sit on the launch path at two points:
- **The manager's PLAY from a slot** (`GuiSaveState::input`, `:418-428`) calls the run callback and deletes the page: no process, no file. The manager's opening (the constructor) builds the grid from the repository's list, which is the cost before the first frame of the page, not of the game. COPY's synchronous copy (L-13) is not on the launch path.
- **The game options menu** (X on a game) opens with five cached `exists` (`GuiGameOptions.cpp:41`, `:53-56`). On the guest it opened within the frame after the press (G06 g06-8); no figure was taken.

Neither number is measured for this slice; the integration image's `time-to-play` run is owed with the window of the fixes.
