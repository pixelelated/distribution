# Analysis — M6.P2 T31, EmulationStation's other pages (#678)

The first reader's analysis (Opus 5.5), written after stages A and B, the guest window and the stage-C proofs, before the seat saw the packet. § Second opinion follows the seat. The leads are `02`'s (L-01 to L-27); every line is the pin's (`16dbac5211`).

## Executive summary

The fork's three pages are built to the house rules. The scrape page is a fourth-tier page with CANCEL and its own help bar. The save state manager draws its bar at 640x480, deletes on a worker, and refuses a write while the saves tree is busy. The Wi-Fi scan's executor is the argv model #1192 names. Every YES / NO box lands on NO. The French is complete.

What does not hold:
- **The base's second exit.** START (CLOSE on every settings page's bar) deletes the pages without `close()`, so no save function runs. A choice B keeps, START drops (L-01, guest and fixture). This is upstream's, in batocera's and ROCKNIX's masters alike, and it reaches the fork's cloud pages, which are all `GuiSettings`.
- **Pages that set without saving.** The LED colour never reaches `system.cfg` (L-02, fixture). A relay-server change replaces NETPLAY SETTINGS without `save()` and drops ENABLE NETPLAY (L-03, guest).
- **Moonlight**, ROCKNIX's own page:
  - the player's SERVER IP is run by the shell (L-05, fixture);
  - UNPAIR says the settings were cleared while removing nothing (L-06, guest and fixture);
  - its title is English in every language, and no map entry or check sees it (L-07, guest).
- **Silence where the fork works.** COPY TO FREE SLOT says nothing when it fails. A copy that worked leaves the same frame, the cursor back on START NEW GAME and the new tile off-screen (L-13, guest). A failing BIOS script reads as an empty check (L-12, guest). An all-errored scrape gives no why and no next step (L-09, fixture).
- **The BIOS page's bar.** BIOS CHECK draws no help bar under full-screen menus, so DETAILS and REFRESH are never offered (L-26, guest). Its French summary is English word order (L-11, guest).
- **The map.** BIOS CHECK and SCRAPING GAMES, the fork's pages, are in neither the map nor `## Not mapped` (L-24).
- **`GuiLoading`'s done flag** races its worker (L-22, ThreadSanitizer).

One brief lead is closed without a change: the LED parse is guarded by the token count. One is narrowed: `GuiKeyboardLayout.cpp:164` writes a scratch render under `/tmp`.

## Acceptance-criteria scorecard

#678's body, at this point (stage C, before the seat):

| # | Criterion | State | Artifact |
| ---: | --- | --- | --- |
| 1 | `00`, `01` to `05` | 00 to 04 written; 05 at stage C's end | the folder |
| 2 | lint `PASS` (pre-issue before D, resolution at close) | pending: the pre-issue run ends stage C | `tools/lint-audit-artifacts` |
| 3 | `review-plan.json` independent, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`), provenance, manifest scan, two keyed invokes | pending: stage C | `second-opinions/` |
| 4 | every punch item at a Phase 7 outcome; box-check 0 fail | pending: stage D onward | the audit issue |
| 5 | reviewed-at / fixed-at headers; the ES read on the pin's bytes; no `packages`/`projects`/`tools` change | reviewed-at `da7922a7bd` and the pin; the removal check empty | `00`, `stage-a/runs.txt` |
| 6 | `01` § Scope with § 2's block | met | `01-research-notes.md` |
| 7 | `02` § Coverage, 76 rows | met: the checkbox's `awk` prints `76` | `02` |
| 8 | `02` § The pages, 37 rows, by a script that names its count | met (`t31-pages.py`) | `02` § The pages |
| 9 | `02` § The dialogs, 50 sites with landings | met (`t31-dialogs.py`) | `02` § The dialogs |
| 10 | `02` § The rows, generated, asserted | met (`t31-rows.py`, 50 calls) | `02` § The rows |
| 11 | `02` § The reads, 12 + 1 + 9 with writers | met: 25 rows, 26 calls with the 4 `atof` | `02` § The reads |
| 12 | `02` § The titles, 37 rows, the twelve with dispositions | met; the dispositions are proposals for the pause | `02` § The titles |
| 13 | `02` § The merge debt | met | `02` |
| 14 | `02` § The runs, the harnesses FAIL-then-PASS | met | `02` § The runs, `stage-c/runs.txt` |
| 15 | `02` § The guest cycle | met for the steps run; G10 and G11 `CANNOT` with reasons | `02`, `guest-cycle/` |
| 16 | `00`'s closing census | at the hand-back | `00` |
| 17 | `04` § Q1 to Q7; bugs with trace, `Already written:`, VM line; T2's and T21's routed leads dispositioned | Q1 to Q7 below; the routed leads in `02` § Leads; the bugs at stage D | this file |
| 18 | `proved:` cells; `question:` per item; § What T32 to T37 inherit | proved met; question at 05; inherit met | `02` |
| 19 | the retro | at stage G | -- |
| 20 | `es-menu-map-check` `0 missing`; the twelve dispositioned | the check passes at the pin; the dispositions at the pause | `02` |
| 21 | the ceremony tools and hooks' tests | at the hand-back | -- |

## Risk assessment

| Risk | Leads | Likelihood | Impact | Severity |
| --- | --- | --- | --- | --- |
| A choice made on any settings page lost on CLOSE | L-01 | certain on START (guest) | settings the player set are silently gone, the fork's cloud pages included | Medium |
| The LED colour reset at every restart | L-02 | certain on devices with the row (fixture) | a setting that never sticks | Medium |
| ENABLE NETPLAY undone by a relay change | L-03 | certain on that path (guest) | netplay stays off after the player turned it on | Low |
| A typed SERVER IP run by the shell | L-05 | needs a crafted string; the player's own | a command run as root from a settings row | Medium |
| UNPAIR says it cleared what it did not | L-06 | certain (guest) | a pairing the player believes gone is still there | Medium |
| COPY TO FREE SLOT silent both ways | L-13 | certain (guest) | a player cannot tell whether the copy happened; a failed one is invisible | Medium |
| A failed BIOS check reads as an empty one | L-12 | when `rocknix-systems` fails (guest) | no recovery offered for a broken check | Low |
| BIOS CHECK's keys never shown | L-26 | certain at 640x480 (guest) | DETAILS and REFRESH undiscoverable | Low |
| `GuiLoading`'s race | L-22 | every use; benign so far | undefined behaviour in the async primitive | Low |
| Moonlight's English title; the BIOS French order | L-07, L-11 | certain (guest) | a French player reads English or broken French | Low |
| An all-errored scrape with no why; an axis dismisses an outcome | L-09, L-10 | uncommon | an outcome the player cannot act on, or never reads | Low |
| Three back landings that act | L-19, L-20, L-21 | certain on those dialogs | B saves, discards or starts a flow | Low |

## Coverage boundary

- **Read whole:** the three fork-own files, `GuiSaveState.cpp`, `GuiScraperStart.cpp`, `GuiBios.cpp`, `GuiSettings.cpp`/`.h` and `GuiLoading.h`. **The fork's diff whole:** the other four fork-modified files. **At the leads' lines:** the upstream pages (§ Coverage names which).
- **Every site of every census:** the six generators read all 76 paths.
- **On the guest:** the image is M7's composition over the pin, so every guest verdict is the image's, with the steps in `02` § The guest cycle, at 640x480, in English and French. Not run: G10 (the viewer's timing), G11 (the stale read), the scrape page's finished frames (offline only), L-19's press.
- **Not this slice's:** `SaveState.cpp`'s `copyToSlot` (T2's), `AtomicFileUtil.cpp` (T21's), `ApiSystem.cpp`'s executors (T21's), `DisplayAspect.cpp` (T32-T37's), `OptionListComponent.h` and `GuiMsgBox` (es-core): read where a lead turns on them, not graded.
- **Not compiled here:** the host has no toolchain (`es-syntax-check` exit 2; `g++` stops at SDL). The five stage-C harnesses compile extracted functions and pass their controls.

## The questions

### Q1 The dialogs and where back lands

All 50 sites read whole (`02` § The dialogs). YES / NO lands on NO at 17 of 17, proved on the guest for DELETE GAME and the manager. Three landings act: CONTROLLER MAPPING's OK (L-19), the metadata editor's saving NO (L-20), and the two SAVE CHANGES? boxes' discarding NO (L-21). All are upstream's and recorded with #585 lines owed. A change of behaviour on an upstream surface outside the lanes is the maintainer's to open (D-UI-079), so they go to the pause. The NFC writer's WRITE / CANCEL lands on CANCEL. The manager's `busyNow` box, re-asked inside YES (`:457`), is the gate's second ask, correct. The scrape page's finished state is dismissed by any input (L-10).

### Q2 The rows, their stores, and the writes that can lose the record

- **The 23 switches** are ES-own keys in `es_settings.cfg`, the store their readers read.
- **The credential rows:**
  - the scraper's three secrets are masked;
  - PLAYER PASSWORD is not (L-04);
  - an untouched editor writes on OK (#1185, cited);
  - the mode is #1193's (cited).
- **Writes that lose the record:**
  - START drops every page's choices (L-01);
  - the LED page never saves (L-02);
  - a relay change drops ENABLE NETPLAY (L-03);
  - SCRAPER stores its default set on the first visit and cannot keep "none" (L-15);
  - a first visit rewrites `es_settings.cfg` twice with nothing chosen (L-16).
- **PL-031's nickname rows** read the builder's seed (`FileData.cpp:653-657`); the move is PL-031's.
- **No reboot flag** is set by any page.

### Q3 The interface thread

- **The process starts** are all on the interface thread with no bound:
  - Moonlight's 5 `executeScriptLegacy`, 3 `runSystemCommand` and its version `popen`;
  - the LED page's command at every slider step (L-02);
  - `GuiControllersSettings`' two.
- **COPY TO FREE SLOT** runs `copyToSlot` synchronously (L-13). On the guest's disk 64 MB took under a second; a card is not measured here.
- **The image viewer's first tile** walks the library (L-18).
- **The 18 `GuiLoading`** completions run on the interface thread over a raced flag (L-22), holding raw `this` (#1212's shape, T21's).
- **SCRAPER's `getSearches`** reads the page's components from the worker (L-17).
- **The hasher constructions** are #1170's and #301's (cited).
- **Time to play** (`03` § 3.6): the manager's PLAY and the options menu start nothing at the press.

### Q4 The reads, and the checks whose failure reads as success

- **The 12 cached `exists`:** their writers are the scraper, RetroArch and the player (`02` § The reads). The stale-read positive was not reached on the guest (G11 `CANNOT`).
- **Failures that read as something else:**
  - the BIOS page's empty vector (L-12, guest);
  - `isFlockHeld`'s non-ENOENT failure as a running sync (L-14, keep an eye: ES is root);
  - COPY's silence both ways (L-13, guest);
  - UNPAIR's false success (L-06);
  - the all-errored scrape (L-09);
  - the Bluetooth bulk delete's ignored result (L-33, cited).
- **The 9 `atoi`:** the LED page's seven are guarded; the key mapping editor's tab value and the update card's percent are benign.

### Q5 The words, the French and the help bars

- **The fourth SKIPPED** is for the pause (L-08): `SKIPPED - YOU CANCELLED IT` against D-UI-028's reserved reasons. The comment argues it, and no row exists.
- **The French:**
  - 706 of 706 strings have their French (`es-untranslated`);
  - the BIOS summary is English word order (L-11);
  - Moonlight's title is no msgid at all (L-07).
- **Upstream's words:** FAILED and HttpReq's text on the netplay page; Moonlight's sentence-case boxes.
- **The bar-less pages:** of the 8 `.cpp` files with no `getHelpPrompts`, all are `GuiSettings` pages or opened from one and inherit the menu's bar. The fork's BIOS CHECK defines `getHelpPrompts` and never draws it (L-26). The manager draws its own (#149), as does the scrape page.
- **Sizing:** no page here calls `getMenu().setSize(` (#540's shape absent).

### Q6 The commands and their readers

- **The SERVER IP** reaches `popen` unquoted, in three commands (L-05). The fix is `Utils::String::shellQuote`, T26's single quoting function, or the argv executor `WifiScanProcess.h` already models (#1192).
- **The LED values** are numbers formatted by `%u` (safe by shape). The Bluetooth and storage arguments are joined bare (T21's `:66`, safe by shape).
- **`GuiUpdate.cpp:213`'s percent reader** takes the text after `>>>`.
- **The spectator and relay session** are #776's.
- No `system(`.

### Q7 The map, the structure and the merge debt

- **The checker** sees 12 of 37 pages' titles. Twelve titles are in neither the map nor `## Not mapped`; dispositions are proposed in `02` § The titles, with BIOS CHECK and SCRAPING GAMES to be mapped. MOONLIGHT is invisible (L-07, L-24).
- **`GuiAutoScrape`** is not built, though the inventory lists it as shipped (L-23).
- **The four tab-strip pages** are recorded (#63).
- **The duplicate dialogs** are identical per family.
- **Merge debt:** 0 upstream changes to any slice file since `cada856d86`. The fork's 12 files are all one-file pages, so D-WORKFLOW-080's option (a) holds here.

## Renovation face

### Q1 Modernize

`GuiLoading`'s done flag wants `std::atomic<bool>` (L-22). The manager's COPY wants the worker DELETE already has (L-13), and the image viewer's index wants to be built off the interface thread (L-18).

### Q2 Standards

- **Confirmations:** three landings act (L-19 to L-21).
- **Help bars:** a full-screen page must draw its own bar (L-26).
- **French:** every `_()` string has its French, but the composition (L-11) and the raw title (L-07) break the standard.
- **Outcome words:** L-08 (the fourth SKIPPED) and L-09 (no why).

### Q3 Bugs

L-01, L-02, L-03, L-05, L-06, L-12, L-13 and L-26 are proved defects (guest or fixture). L-09, L-10, L-11 and L-22 are proved with lower stakes. L-14 is a keep-an-eye item.

### Q4 Package currency

The 64 upstream files are at `rocknix/master`'s bytes. Of the leads' upstream sides, batocera's master is the same at `GuiLoading.h` and the START handler (L-22, L-01); Moonlight's and the LED page are ROCKNIX's own. Nothing in the slice is behind its upstream.

### Q5 Efficiency

Moonlight's and the LED page's commands block the interface thread per press or per slider step. The image viewer's first open walks the library. COPY copies on the interface thread. None of these is on the launch path.

### Q6 Dead ends

- `GuiAutoScrape.*`: compiled by nothing, opened by nothing (L-23).
- The commented `addWithDescription` lines (`GuiFavoriteMusicSelector.cpp:45-46`) and the commented-out help prompts (`GuiKeyMappingEditor.cpp:476`) are dead text.

### Q7 Clarity and structure

`GuiSettings`' two exits should be one contract (L-01). BIOS CHECK and SCRAPING GAMES should be in the map (L-24). The pages' titles should be visible to the checker (#951/#965's evidence, `02` § The titles).

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **`es-native-ui.md` § Core patterns** ("Settings page ... `addSaveFunc` (apply-on-close)") does not say that START closes without applying. A line there would have kept L-01 from being a surprise.
- **`es-code-traps.md`, the window paragraph,** names the manager as the example of a page that draws its own bar. A checker of `renderHelpPromptsEarly` against full-screen `GuiComponent` pages would have caught L-26.

### Codification gaps (proposals for the coordinator)

- **A walk's key is sent once the screen is settled, and the focus is read in a frame before an action press.** Three passes of this window were void without it (the friction line).
- **The brief's runs use `grep -F` for literal C++ calls.** `popen (` and `_\("` both slipped past a basic-regex `grep`.

## Second opinion

Pending: the seat runs at stage C's end (GPT-6 Astra at `max`, one refutation call after its probe). This section records the plan, the call and the grading.

## Quality self-check

- Every figure in `02` is a tool's line; the composer asserts the counts, and every generator has a constructed negative.
- Every proved lead names its artifact: a guest step's file and frame, or a stage-C harness's FAIL-then-PASS pair.
- Void guest passes are recorded as void. No void pass is cited as evidence.
- Corrections to the brief and to this lane's own earlier statements are listed (`02` § Corrections; `00` § Window).
- Not done: G10, G11, the scrape page's finished frames on the guest.
