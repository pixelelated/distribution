# Analysis: M6.P2 T34, EmulationStation's core components (#681)

## Executive summary

The 80 paths of `es-core/src/components/**` at the pin `16dbac5211` were read whole: 21 modified by the fork (+591/-114 over 33 commits) and 59 carried byte-identical from ROCKNIX's master. There is no merge debt: 0 of the 14 upstream commits since the base touch the 80. `02-forward-audit.md` tables every layout read, house constant, input, lifetime, read and string, each table generated and asserted by a script under `tools/` that was seen to fail on a constructed drift. The guest window (19:28 to 19:39) confirmed on the image that the house constants hold: the button bar's gap at 14 px and 28 px, and the dim at 0x50.

**43 punch items: none Critical, 1 High, 15 Medium, 27 Low.**
- **The High item, PL-27,** is a security-sensitive finding the independent seat raised (G-3) and the first reader verified at the pin. Its details are held off the public tracker until the maintainer says where such findings go. The public record names its existence, severity and owner only.
- **The first reader's Medium items:** the progress card's closing race (PL-01); the card's lifetime against its holders (PL-02, T2 PC-1's component half); the text field's raw-`this` posts (PL-03); a two-line row's shares, which can trip an assertion (PL-07); and the VLC release path (PL-18).
- **The seat's verified Medium items:** three uninitialised members (PL-28); a 0-column help grid (PL-29); a web image's resize recursion (PL-30); a rebound web image's stale URL (PL-31); an image's stale pending load (PL-32); the image grid's `clear()`, which keeps its loop-copy tiles and corrects this audit's own stage-B contract (PL-33); stranded grid tiles (PL-34); a switch that can show a state other than the one it holds (PL-36); a subtitle's re-insert (PL-37); and right-to-left dispatch (PL-38).
- **The seat refuted two of the first reader's items,** and the proposals are to withdraw them: PL-05 as a component defect (the pin's chain keeps SWITCH TAB; the image's empty bar is named for T35 and M7), and PL-24 (`IList` clamps or wraps the carousel's negative count).

**What this analysis does not yet carry:**
- **The unit build:** `tools/t34-build-tests.sh` and the 34 seam cases, with the seven FAIL-at-pin pairs.
- **The sanitizer cases** for PL-01 and PL-03.
- **The stand-in syntax check** over the 37 sources.

Each proof below is `tree` or `guest` until those run. They are named as owed in § Coverage boundary and on #681. **Stage E ran them:** the unit build, the sanitizer cases (with a fourth, `asan-card-handle`) and the stand-in, each recorded in `stage-e/`.

## Acceptance-criteria scorecard

#681's 21 criteria, as they stand at the hand-back (`8adf428981`, amended at `d60c88966a` and after); the stage-D state is in this file's history:

| # | Criterion (short) | State at the hand-back | Evidence |
| --- | --- | --- | --- |
| 1 | the audit folder's files and directories | met: `stage-a/` to `stage-e/`, `second-opinions/`, `tools/`, `guest-cycle/` | `ls` at the hand-back |
| 2 | the lint at both phases and with `--issue` | pre-issue PASS at stage C; resolution PASS at the hand-back with the held reply copied in for the run and removed (the carry, #1308) | `tools/lint-audit-artifacts` |
| 3 | `review-plan.json` and the two provenance files | met: probe and refutation PASS, served `openai/gpt-6-astra` at `max`; the refutation's reply held off the tree (PL-27), its receipt committed and binding its sha256 | `second-opinions/` |
| 4 | the punch-list issue at Phase 7 | met: #1307 with 43 items; `05` at Phase 7, 26 Resolved, 14 Deferred, 3 Withdrawn | `05` |
| 5 | the four header fields | met: `d446c4c6c3`, `16dbac5211`, `8adf428981`, `52f0ff512` | #681's body |
| 6 | `01` § Scope with the block's lines | met | `01-research-notes.md` |
| 7 | the coverage table's 80 rows | met | `02` § Coverage |
| 8 | `02` § The runs with both counting rules | met | `02` § The runs |
| 9 | the generated sections, each drift-proven | met | `stage-b/generator-drifts.txt` |
| 10 | § The layouts' rows and the reproducer | met: the rows, and the reproducer 3.5 FAIL at the pin, PASS at `db12b1598` | `02` § The layouts |
| 11 | § The constants' rows and frames at both sizes | met for the bar (14 px, 28 px) and the dim (0.314); the card's frames `CANNOT` (G-02, a harness no), moved to the integration window | `02`, `guest-cycle/` |
| 12 | § The merge debt's one line | met | `02` § The merge debt |
| 13 | § The runs: every command, the unit build's `TOTAL:` | met: `TOTAL: 246 test cases in 6 binaries` at the pin, `TOTAL: 285 test cases in 6 binaries` at the ES tip | `02` § The runs |
| 14 | § The guest cycle | met: `02` § The guest cycle, G-01 to G-12 as run | `guest-cycle/`, #681 START and RETURN |
| 15 | `00` shows no build, fetch, device or account | met so far | `00-running-log.md` |
| 16 | `04` answers Q1 to Q7; bugs with their three lines | this file; bugs filed at stage D | this file |
| 17 | every proof's `proved:` cell; § What T35 to T37 inherit | met: every floor cell leads with `fix-unit-test` or `tool-run`; no `pending:` cell left | `02` |
| 18 | the retro | met: `docs/retros/2026-10-31-m6-es-core-components.md`, posted on #681 | the retro |
| 19 | the map rows | no row proposed; the checker's line quoted | `02` § The structure |
| 20 | the five checkers and the ES pre-push test | met: `stage-e/handback-checks.txt` | the checkers' exit lines |
| 21 | the unit build's `TOTAL:` line with 0 failed | met: `TOTAL: 285 test cases in 6 binaries`, 0 failed test cases in every binary; the 3 failed assertions are the two `may_fail` cases | `stage-e/handback-build.txt` |

## Risk assessment

- **PL-27** is the slice's one High item, security-sensitive and held. Its fix should land before the details do.
- **The card's closing race (PL-01)** sits under every automatic sync and every achievements card. Its likely symptom is a fade that starts late, not a crash, but it is undefined behaviour. The fix is small and the covering case is a host ThreadSanitizer run.
- **The holders' raw pointers (PL-02)** are the larger risk. A worker that outlives its card writes into freed memory. The component cannot refuse the call; only a handle the window keeps alive can. That is a design ruling across T34, T35, T18 and T20, so it waits for the pause.
- **The image is M7's composition, not the pin.** PL-04 did not reproduce there, and PL-05 appeared only there. Neither is a finding about the pin until the pin's code is read for it.
- **At the stage-D pause, no proof yet ran the components' own code** (stage E ran them all; this risk is closed). Every case was owed to the unit build. Until it runs, a `tree` proof is a reading, and the seven FAIL-at-pin leads are expectations.

## Coverage boundary

- **Read:** all 80 paths at the pin, whole; their neighbours (`Window.cpp`, `HttpReq.cpp`, `FileSystemUtil.cpp`, `Font.cpp`, `GuiTextEditPopupKeyboard.cpp`, `GuiMenu.cpp`) read only where a row cites them, never edited.
- **Run on the host:** the membership block, the brief's § 5 block, the nine generators, the packet's scan.
- **Run on the guest:** G-01, G-03, G-04, G-05, G-09 and G-11, at 640x480 and 1280x800.
- **Not run:**
  - the unit build, and with it every 3.x case;
  - the sanitizer cases (3.19, 3.20, PL-01's);
  - the stand-in syntax check over the 37;
  - G-02, G-06, G-07, G-08 and G-10 (`CANNOT`, each with its reason on #681).
- **Out of scope:** the neighbours' own defects, named for their owners in `05`.

## The questions

### Q1 Layout: computed from what it last produced, or from a moving number

The rule's shape survives in two places: L-03's shares (PL-07), and the font height every layout reads before the tallest glyph has drawn (PL-17, 13 layout reads in § The layouts, the brief's eight among them). #241's self-feeding row is fixed: `layoutRows` measures from the fonts. L-17 (PL-08) is a different shape, measured at one width and drawn at another, and 3.6 (PL-06) is a one-token slip in the same file. G-05's reopened page matched its first paint on the image because the menus had already drawn, so the moving number is not shown there.

### Q2 The house constants

On the image the bar's gap is 14 px at 640 and 28 px at 1280 (0.022 W), and the dim's ratio is 0.314 (0x50). The card's width and position are read in the tree (0.9 W, centred); its frame is `CANNOT` this window (G-02). The open items are L-04's overhang (PL-14), L-06's 20 px inset (PL-15), and L-05's second copy against the comment's "one place" (PL-16). L-19's floor is dead text, recorded.

### Q3 Input and the help bar

`canMoveCursor` decides the grid's prompts, so D-UI-034 holds in the tree. The strip is a focus stop on the image: four frames and the wrap. The open items:
- PL-04: the icon key through `_()`;
- PL-05: the tabbed page's empty bar, on the image;
- PL-11: BACK labelled SELECT;
- PL-12: the unstated cast;
- PL-19: directions offered by type.

PL-24, the carousel's negative count, is 3.8's to decide.

### Q4 Lifetime

The four `delete this` in the option list are sound by T31's invariant, which is kept (§ 1 d). The card's race (PL-01), its holders (PL-02, § 1 b) and the field's posts (PL-03) are the defects. The VLC release thread (PL-18) is recorded outside the lanes. The callback types (PL-22, § 1 c) and the grid's contract after `clear()` (§ 1 e) are written in § The lifetimes for the pause.

### Q5 Reads and the network

All ten `exists(` reads are cached. L-09's feared miss is sound at the pin: `HttpReq`'s `removeFile` and `renameFile` erase the cached key. L-20's media reads are recorded. L-08's never-again badge (PL-13) is by design and goes to the pause. § 1 (a)'s contract is written: a path is a cache key for a texture's lifetime, and the cache's half belongs to T36.

### Q6 The words

The 17 msgids each have French at the pin. Three strings sit outside `_()` or the vocabulary: `"Auto"` (PL-09), `"add star"` (PL-10) and the blank date (PL-25). The brand's guard is a reading, not a check (PL-23).

### Q7 The structure and the merge debt

There is no merge debt. Batocera's eight commits are a reconciliation list, with the one `updateGrid()` overlap. The es-app include (PL-21), the 13 gates and the one non-ASCII byte are recorded. The `setOpacity` guard is unreachable at the pin (§ 1 g). `UntintedImageComponent`'s lift is a question for the pause (PL-26). The tidy is PL-20.

## The take-up table (brief § 2), each row disposed

| Row | Disposition | Where |
| --- | --- | --- |
| T32 PL-07 / #1263 | the caller's half stated: one ask per `setImage`, a live texture reused | `02` § The reads, `ImageComponent.cpp:408` |
| T2 PC-1 | the component's half: PL-02 | `05` |
| T26 L-02 / #1221 | the contract stated beside #1263's row | `02` § The reads |
| T26 PL-27 | PL-22 | `05` |
| T31 L-03 / #1243 | the invariant kept | `02` § The lifetimes, `OptionListComponent.h:310`, `:323` |
| T31, #63, #65 | the component half of #65 shown on the image (G-05); the pages are T31's | `guest-cycle/g05-*` |
| T31 L-26 / #1245 | read; the checker proposal is the coordinator's | - |
| T31 retro, T26; `es-code-traps.md:22` | the rule restated beside `clearButtons` | `02` § The lifetimes |
| T32 S4 / #1266 | the grid's contract after `clear()` | `02` § The lifetimes |
| T32 PL-16, T31 PL-26 | not reached on the image (no grid theme, G-08) | `guest-cycle/g01-identity.txt` |
| T32 PL-10 / #1265 | read; the views' fix | - |
| #585 / #48 | PL-08: the reproducer written and run (3.5): FAIL at the pin, measured 28 against drawn 48; PASS at `db12b1598` (S3) | `05`; `stage-e/s3-before.txt`, `s3-after.txt` |
| #182 | the dim measured on the image | `guest-cycle/g04-1-cloud-hub-en.png` |
| #325 | the wrap shown (G-05) | `guest-cycle/g05-4-after-up-up.png` |
| #210 | the bar's fit; read | `02` § The layouts |
| #27 | read; no grid theme | - |
| #243 | 3.22, 3.23 (and 3.24) run in S5: PASS at the pin and after `568ef099d`, the turn's fit swapped and four turns the identity | `02` § The leads; `stage-e/s5-before.txt`, `s5-after.txt` |
| #157 | read | - |
| #1112 | read-only context | - |
| T21 L-11 / #1199 | read; `SystemConf`'s | - |
| T21 PL-26 / #1192 | the field's masking named for T35's pause | - |
| T18's double | a collision named at the hand-back | `02` § The structure |
| T20's SCAN GAMES row | 3.4 run in S3: FAIL at the pin (`0.986957`, `1.01304`), PASS at `db12b1598`; the row's refresh measured from its fonts (#241's fix) is unchanged | `02` § The leads; `stage-e/s3-after.txt` |
| T31's func-form rows | `CANNOT` with the harness's reason: the window's tools capture frames, not frame times, and the guest exposes no per-frame counter, so neither `ComponentList::render`'s re-tint nor the three func-form rows' per-frame updates could be priced there; the last figure on record is `docs/vm-qa-log.md:171` (2026-10-06, `7afa9efcfc0`: 0.603 s to the first pixels, 1.33 s exit with backup, 1.017 s rapid relaunch), from before this slice; the retro and `03` § 3.6 say what stage E did to the two numbers | the retro; `03` § 3.6 |
| `es-ui-style-guide.md:202` | read as it stands | - |
| #585 | the lines written out, one per item | `02` § The #585 lines owed |

## Renovation face

### Q1 Modernize

Nothing to modernize for its own sake. The fork's 21 files follow the house patterns, and the 59 are upstream's, kept as upstream has them (D-UI-079).

### Q2 Standards

The house constants hold on the image. The standards gaps are words outside `_()` (PL-09, PL-10), pixel constants where fractions belong (PL-15, and the table in `02`), and the brand's guard by reading (PL-23).

### Q3 Bugs

PL-01, PL-03 and PL-04 are the bug candidates. Each is filed at stage D with its trace, its `Already written:` line (nothing inherited: a component writes no file) and its VM line, once its case is seen to FAIL. PL-05 and PL-24 wait on a read and a case.

### Q4 Package currency

None: the slice carries no package. ROCKNIX's master is level for the 80, and batocera's eight are a reconciliation list.

### Q5 Efficiency

`ComponentList::render` re-tints every element every frame, and three func-form rows force per-frame updates. Their price on the guest is the retro's, and the window gave no frame time to read: `CANNOT` with the harness's reason.

### Q6 Dead ends

`VideoPlayerComponent` compiles to nothing on every image (`_RPI_`), the `WIN32` blocks are dead, and `ScrollableContainer.cpp:69` computes a value it never uses. Recorded only: a dead-end table removes nothing (D-WORKFLOW-209).

### Q7 Clarity and structure

The es-app include (PL-21), the misleading indentation (PL-20), the cast's unstated invariant (PL-12) and the "one place" claim (PL-16).

## Instruction File Recommendations

- `es-code-traps.md` could carry the card's rule: a component a worker holds by raw pointer must not be written from that worker without the card's lock (PL-01, PL-02). Proposed for the coordinator; not written by this lane.
- `generic-x64-vm-testing.md` could say that at 640x480 a menu page draws no help bar, so a help-bar proof belongs at 1280x800. This window spent G-04's French half learning that.

## Second opinion

Depth **independent**: one seat, `gpt` (`openai/gpt-6-astra`, effort `max`), over `second-opinions/gpt-brief.md` (547,488 bytes; `review-plan.json`).
- **The probe:** 19:59:53 to 20:00:06Z, PASS.
- **The refutation:** 20:00:16 to 20:17:16Z, attempt 1 of 4, `finish=stop`, 35,726 reasoning tokens; served by OpenAI at `max`; verification, effort and provider PASS (`gpt-audit.md.provenance.json`).
- **The reply** (24,818 bytes, sha256 `609c488c93cd7848dfb76d34587094eaf01313056262d4b301e9c9e2b7e02dcb`, the receipt's `output_file_sha256`) is held outside the tree, because one finding is security-sensitive (PL-27). It was scanned before it was read: 0 forbidden, 0 secret-shaped lines.
- **Its "Sections I need"** asked for whole neighbours (`Window.cpp`, `ThreadedCloudSync.cpp`, `HttpReq.cpp`, `Font.cpp` and more). This slice allows exactly two keyed invokes, so no second packet went, and its *cannot tell* grades stand as written.

**The seat's grades of PL-01 to PL-26.** Confirmed: PL-06, PL-09, PL-10, PL-19. Confirmed with narrowing: PL-01, PL-02, PL-03, PL-08, PL-11, PL-12, PL-13, PL-14, PL-15 (`rowInset()` is 10, not 20), PL-20, PL-21, PL-22, PL-25. Confirmed at a higher severity: PL-07 (Medium in assertion builds: a long description drives a share above 1) and PL-18 (Medium). Confirmed at a lower one: PL-04 (Low; the bar's delivery is not shown). **Refuted:** PL-05 as a component defect, and PL-24. Cannot tell from the packet: PL-16, PL-17, PL-23 (and the misnamed `:205`, `addWithLabel`, corrected in § The words), PL-26.

**On the seven FAIL-at-pin leads,** statically:
- 3.4 fails as the lead says;
- 3.6 is right;
- 3.7 is right for AUTO (the 1e-6 claim was too strong);
- 3.8's intermediate `-7` is real, but its out-of-range landing is not;
- 3.16 rejects `haut/bas`, subject to the bar's delivery;
- 3.21's first half is a citation-dependent PASS, its second half confirmed;
- 3.26: five buttons overhang, and at a windowed 480-px menu four do too.

**The seat's new findings, G-1 to G-16, each verified at the pin by the first reader before it was carried:**
- confirmed: G-1, G-2, G-3, G-5, G-6, G-7, G-9, G-12, G-14, G-15, G-16;
- confirmed with narrowing (callers' cells or reachability unread): G-4, G-8, G-10, G-11, G-13.

They are PL-27 to PL-42; PL-43 is the first reader's L-26, found while checking the seat's `:205` correction. **G-7 corrects this audit:** `02`'s stage-B statement of the grid's `clear()` contract was wrong and is rewritten.

## Quality self-check

- Every count in `02` is a generator's or a command's own line. None is summed by hand.
- Every `tree` proof cites its lines at the pin. Every guest reading names its frame and is labelled `image`.
- The owed proofs are named, not implied: the unit build, the sanitizer cases, and the syntax check.
- The scorecard above has no total row; its states are words, not sums.
