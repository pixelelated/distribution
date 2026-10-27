# Analysis — M6.P2 T26, EmulationStation's main menu, GuiMenu (#673)

The first reader's analysis (Opus 5.5), written after stages A and B and the guest window, before the seat saw the packet. § Second opinion follows the seat. The leads are `02`'s (L-01 to L-30); every line is the pin's (`16dbac5211`) unless it names a script (`8ebaf8daad`'s).

## Executive summary

The fork's own pages are built carefully where they were built to be. The wizard's page changes all hand the new page on (fifteen of sixteen `cloudSetupPresent` calls are their scope's last statement, the sixteenth deliberately so). Every dialog callback runs on its own copy. The long cloud calls run behind a spinner. The retired folder migration's replacement asks before it creates anything.

What does not hold is at the joins:
- **A row and its reader:** two upstream rows write a key nothing reads. The global VIDEO FILTER writes `global.videofilters`, where the launch script reads `videofilter` (L-09). The fast-scrolling switch saves to `system.cfg`, where its reader reads `es_settings.cfg` (L-10). Both proved on the guest.
- **A rename and its sentences:** after a failed check, the relink page sends the player to CONNECT OR REPAIR CLOUD STORAGE, a row renamed on 2026-10-11 (L-18, guest in English and French).
- **The interface and the cache:** the sign-in's QR read is cached, so one failed attempt leaves the session text-only (L-01, guest with a control).
- **The interface thread:** 116 process starts with no bound, the cloud pages' among them (L-04).
- **The French surface:** the match's refusal and two provider labels reach a French player in English (L-19, L-20).
- **A credential row:** the ROCKNIX SECURITY page runs `setrootpass` on every close (L-08).

Two leads of the brief are closed without a change here: T21's S1 already guards the six relink rows (L-07), and `led.colour` is in code no ROCKNIX image builds (L-14).

## Acceptance-criteria scorecard

The brief's § 7, as #673's body carries it, at this point (stage C, before the seat):

| # | Criterion | State | Artifact |
| ---: | --- | --- | --- |
| 1 | `00` and `01` to `05` | 00 to 04 written; 05 at stage C's end | the folder |
| 2 | lint `PASS` (pre-issue before D, resolution at close) | pending: the pre-issue run ends stage C | `tools/lint-audit-artifacts` |
| 3 | `review-plan.json` independent, one reviewer, provenance, manifest scan, two keyed invokes | pending: stage C | `second-opinions/` |
| 4 | the punch list's items at Phase 7 outcomes; box-check 0 fail | pending: stage D onward | the audit issue |
| 5 | reviewed-at / fixed-at headers; ES read on the pin's bytes; no `packages`/`projects`/`tools` change | reviewed-at `db7be4b104` and the pin; the removal check empty at every stage so far | `00`, `stage-a/runs.txt` |
| 6 | `01` § Scope with § 2's block and the parser's line | met | `01-research-notes.md` |
| 7 | `02` § Coverage, exactly 2 rows | met: the check prints `2` | `02-forward-audit.md` |
| 8 | `02` § The pages, one row per page, by a script that names its count | met: 60 pages, 65 titles (`t26-pages.py`) | `02` § The pages |
| 9 | `02` § The rows, generated, asserted, exit 1 on drift, both-sides keys marked | met: 275 rows; the OS column | `02` § The rows |
| 10 | `02` § The transitions | met: 16 + 10 rows | `02` § The transitions |
| 11 | `02` § The reads | met: 37 rows, 12 uncached | `02` § The reads |
| 12 | `02` § The duplicates and § The merge debt, D-WORKFLOW-080's option (a) | met | `02` |
| 13 | `02` § The runs | met | `02` § The runs |
| 14 | `02` § The guest cycle | met for the steps run; L-22's landing `CANNOT in this window` | `02` § The guest cycle, `guest-cycle/` |
| 15 | `00`'s closing census | at the hand-back | `00` |
| 16 | `04` § Q1 to Q7 answered; bugs with trace, `Already written:`, VM line | Q1 to Q7 below; the bugs are filed at stage D | this file |
| 17 | `proved:` cells; `question:` per punch item; § What T31 to T37 inherit | proved cells met; question at 05; inherit met | `02` |
| 18 | the retro at `docs/retros/` | at stage G | -- |
| 19 | `es-menu-map-check` `0 missing`; D-UI-046 settled at its lines | the check passes at the pin; D-UI-046 is L-23, for the pause | `02` § The runs |
| 20 | the ceremony tools and the hooks' tests | at the hand-back | -- |

## Risk assessment

| Risk | Leads | Likelihood | Impact | Severity |
| --- | --- | --- | --- | --- |
| A player follows a dead path after a failed cloud check | L-18 | certain on that path (guest) | a player told to use a row that is not there, at the moment of a failure | Medium |
| A setting the player changes does nothing | L-09, L-10 | certain (guest) | the VIDEO FILTER default and the fast-scrolling choice are silently ignored | Medium |
| The interface freezes on a wedged helper | L-04 | low (each call is local) | a frozen menu with nothing on screen, for as long as the helper hangs | Medium |
| A sign-in without a code after one failed attempt | L-01 | low (needs a first failure) | a text-only page for the rest of the session; the address still shows | Low |
| The device password re-applied on every SECURITY close | L-08 | certain (tree) | seconds of frozen interface and service restarts; after S1, `root.password` reads empty while the device keeps it | Medium |
| A French player reads English | L-19, L-20 | certain where reached (guest for L-20) | a refusal they must read to act on, in a language not theirs | Low |
| A long error line loses a byte and the wrong sentence shows | L-05 | low | the generic sentence instead of the specific one | Low |
| The next upstream merge conflicts in `openNetworkSettings` | L-28 | certain at the next merge | a manual resolution against a competing saved-networks design | Low (planning) |

## Coverage boundary

- **Read whole:** the 97 added definitions and the fork's three classes; the header. **At their lines:** the 12 changed definitions (fork hunks and every lead) and the 47 unchanged (every lead). **Every line:** the five generators.
- **On the guest:** the image is M7's composition over the pin, so every guest verdict is the image's; the steps listed in `02` § The guest cycle, at 640x480, in English and French. Not run: L-22's landing, L-16 at 1280x800.
- **Not this slice's:** `GuiSettings.cpp` (L-12's systemic fix), `Platform.cpp`'s `GetShOutput` (L-05's reader), `TextureResource` (L-02's cache), the cloud scripts (T17's), `setrootpass` (T1's): read and cited, not graded.
- **Not compiled here:** the host has no toolchain (`es-syntax-check` exit 2; `g++` stops at SDL); the ten harnesses compile extracted functions and passed.

## The questions

### Q1 The pages' lifetimes

**Sound, with one shape recorded.** The sixteen `cloudSetupPresent` calls hand the new page on; fifteen are their scope's last statement and `:7862` opens the blocking window after the push on purpose (`02` § The transitions; the ten harnesses rc 0). The posted rebuilds are weakly held (`:4529-4584`) or owned by the page (`:5202-5206`); `CloudConnectionsPage`'s posted refresh is guarded (`:5580-5594`); the three detached threads post through the gated `AppWindow::post` with weak rows (`:9769-9847`; `queryInterfaceAddresses` unbounded). The recorded shape: three callbacks delete the page whose row holds them, from inside that row's callback (`:10149-10153` the fork's; `:1616`, `:10855-10856` upstream's) -- safe by a self-capture cycle that leaks the switch, and by the input path returning at once at the two levels read (L-17). `cloud-oauth-lifetime.py` and `cloud-gated-row.py` cover five wizard transitions and `cloud-folder-reopen.py` the folder page's rebuild; the relink page's and the connections pages' transitions have no harness. L-16 (the 0.75 page unpositioned) is not reached at 640x480.

### Q2 The rows and their stores

275 value-binding rows (`t26-rows.py`), 267 store writes. **Two rows write where nothing reads** (L-09, L-10: guest). Eleven built rows write keys nothing reads once `get_setting`'s global fallback is counted; on the image two are hidden by runtime gates and PAUSE ON TRANSLATED SCREEN is reachable (L-13). The six `addInputTextConfigRow`-only pages persist through their `onFinalize` saves (L-12, the systemic fix `GuiSettings.cpp`'s). The six unguarded credential rows are fixed by T21's S1 (L-07). ROOT PASSWORD is unmasked and applied on every close (L-08). `led.colour` and the first SECURITY page are never built (L-14). `exitreboot` has no consumer on its page (L-15). Writes at open: two pages' (L-11), the image's seed making one moot. **The folder step** builds no join, follow or move: CHECK and CREATE, the latter confirmed (D-CLOUD-175/178/179).

### Q3 The interface thread's bounds

159 runs, 131 on the interface thread, 116 of those with no bound (`t26-pages.py`; L-04). The player sees nothing while each runs. The bounded ones are `cloudSetupInfo()` (10 s), `cloudScanStamped` (5 s), `cloudFolderContext()` (5 s) and the path editor (30 s, on a worker). None sits between a launch press and a frame (`03` § 3.6).

### Q4 The reads that can be stale

37 reads (`02` § The reads): 12 uncached. The cached ones that read a file another process writes are the QR (L-01, guest with a control) and the scan and selection files through `isRegularFile` (L-03, narrow). L-02 (a texture by path) is a second stale read on the same page, not reached on this image.

### Q5 The words and the dialogs

108 dialogs: 41 YES/NO landing on NO, 56 single OK. Off the house rules: L-18 (a dead row named, guest), L-19 and L-20 (English in French), L-21 (MANUAL UPDATES' case and URL, the fork's), L-22 (back lands on CANCEL SIGN-IN: a style call), L-23 (the map's stale heading), L-24 (upstream's strings, recorded), L-25 (HOSTNAME's blank). French: 978 of 980 one-line literals (the two are upstream's fuel gauge); 706 of 706 fork strings; 0 non-ASCII comments. The menu map: `0 missing`.

### Q6 The commands and their readers

`GetShOutput` drops a byte per read (fixture); the create and change paths read through it and match sentences by substring (L-05), with two parsers of one success line (L-06). One quoting algorithm in two functions (L-27). T18's PL-21 composers (`:5006`, `:6140`) and PL-17's discarded `backuptool backup` output (`:5125`) are cited. `credential-quoting.py`: 9 of 9 sites quoted.

### Q7 The structure and the merge debt

The ten longest functions are as the brief lists them; `openSystemSettings` is 1,604 lines. 74 labels are built in two or more functions; the FINISH RESTORE PROCESS row is built identically in two menus. 86 conditional regions, 869 lines no ROCKNIX image compiles, 13 regions whose first arm's braces do not balance (L-29). The Wi-Fi verdict is composed three ways (L-26). The merge debt: `cada856d8` meets the fork in all four of its hunks (L-28). D-WORKFLOW-080's option (a) is the shape the definitions table argues for.

## Renovation face

### Q1 Modernize

- Every short cloud call off the interface thread, or bounded, with a spinner where it can take longer than a frame (L-04).
- One output reader (`GetShOutputLines`) and one success parse for `cloud_remote` (L-05, L-06).
- The cloud and network pages out of `GuiMenu.cpp` into their own files (D-WORKFLOW-080's option (a)).

### Q2 Standards

- **`es-player-text.md` § French:** L-19, L-20. **`upgrade-and-install.md` (old paths in strings):** L-18. **`es-ui-style-guide.md` § Saving:** L-08. **§ Text:** L-21. **D-UI-039:** L-23. **`engineering-practices.md` § Guards must fail closed:** L-05's generic fallback hides the real refusal.

### Q3 Bugs

- **Medium:** L-08, L-09, L-10, L-18.
- **Low:** L-01, L-03, L-04 (Medium where a helper hangs), L-05, L-19, L-20, L-21, L-26.
- **Latent or not reached here:** L-02, L-16, L-17.

### Q4 Package currency

Nothing in these two files vendors a package. `qrencode` and the sign-in window ship on the image.

### Q5 Efficiency

The ROCKNIX SECURITY page's close re-applies the password and restarts services every time (L-08). A settings page's close rewrites `es_settings.cfg` even with no change (G05). CLOUD CONNECTIONS starts `cloud_remote list` twice at build.

### Q6 Dead ends

869 lines no ROCKNIX image compiles (L-29): the BATOCERA pages (the RGB LED page, the first SECURITY page, the torrent updates), the `!ROCKNIX` first arms and the WIN32 lambda copies. Recorded, not removed (D-UI-079). `:7422`'s `\r\n` search can never match (L-05).

### Q7 Clarity and structure

- `GuiMenu.cpp` is 11,747 lines of the main menu and every fork page; `openSystemSettings` alone is 1,604.
- The wizard's own comment calls `--check` "the only slow call" (`:6627-6630`), and `cloudSelectionRead`'s neighbour calls an `isRegularFile` read uncached (`:4154-4156`): two comments that state what the code does not do.

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **A rename's sweep greps the old name in `_()` strings and the French catalog** (L-18): `tools/archaeology --reversal` covers the tree, but `c8dc72cf9` updated one of two sentences. A `tools/vocabulary-check`-style check of row names cited in dialog text against the labels the pin builds would catch it mechanically.
- **A row's store matches its reader's** (L-10): `es-native-ui.md` already says `addSwitch`'s bool is `storeInSettings`; a generator like `t26-rows.py`'s OS column, run in CI, would catch a key no reader names.

### Codification gaps (proposals for the coordinator)

- `es-code-traps.md`: "`exists()` on a file a helper writes for this page" -- the QR's case (L-01) is the third of its kind after the stamps and the restore marker.
- `generic-x64-vm-testing.md`: `vm-serial script` takes no arguments; a `sh` call that reads stdin blocks the guest's shell; `system.language` takes `fr_FR`.

## Second opinion

Pending the seat (stage C).

## Quality self-check

Pending stage C's end.
