# Analysis: M6.P2 T34, EmulationStation's core components (#681)

## Executive summary

The 80 paths of `es-core/src/components/**` at the pin `16dbac5211` were read whole: 21 modified by the fork (+591/-114 over 33 commits) and 59 carried byte-identical from ROCKNIX's master. There is no merge debt: 0 of the 14 upstream commits since the base touch the 80. `02-forward-audit.md` tables every layout read, house constant, input, lifetime, read and string, each table generated and asserted by a script under `tools/` that was seen to fail on a constructed drift. The guest window (19:28 to 19:39) confirmed on the image that the house constants hold: the button bar's gap at 14 px and 28 px, and the dim at 0x50.

**26 punch items, none Critical or High, 5 Medium.** The five Medium items:
- **PL-01:** a data race on the progress card's closing state, in a lane surface.
- **PL-02:** the card's lifetime against its holders once the window deletes it (T2 PC-1's component half).
- **PL-03:** the text field's two raw-`this` posts.
- **PL-04:** the `up/down` icon key through `_()`. It did not reproduce on the image.
- **PL-05:** a tabbed page's help bar that carried no component prompt on the image, unread at the pin.

The rest are Low: three contained upstream fixes under rule 6, four register-row rulings the brief expects, and recorded upstream surfaces.

**What this analysis does not yet carry:**
- **The unit build:** `tools/t34-build-tests.sh` and the 34 seam cases, with the seven FAIL-at-pin pairs.
- **The sanitizer cases** for PL-01 and PL-03.
- **The stand-in syntax check** over the 37 sources.

Each proof below is `tree` or `guest` until those run. They are named as owed in § Coverage boundary and on #681.

## Acceptance-criteria scorecard

#681's 21 criteria, as they stand at the stage-D pause:

| # | Criterion (short) | State at the pause | Evidence |
| --- | --- | --- | --- |
| 1 | the audit folder's files and directories | partial: `stage-d/`, `stage-e/` owed | `ls` at the hand-back |
| 2 | the lint at both phases and with `--issue` | pre-issue PASS owed this stage; resolution at close | `tools/lint-audit-artifacts` |
| 3 | `review-plan.json` and the two provenance files | after the seat this stage | `second-opinions/` |
| 4 | the punch-list issue at Phase 7 | the issue at stage D; outcomes at stage F | `05` |
| 5 | the four header fields | `reviewed-at:` at the hand-back | #681's body |
| 6 | `01` § Scope with the block's lines | met | `01-research-notes.md` |
| 7 | the coverage table's 80 rows | met | `02` § Coverage |
| 8 | `02` § The runs with both counting rules | met | `02` § The runs |
| 9 | the generated sections, each drift-proven | met | `stage-b/generator-drifts.txt` |
| 10 | § The layouts' rows and the reproducer | rows met; the #585 reproducer owed (3.5) | `02` § The layouts |
| 11 | § The constants' rows and frames at both sizes | met for the bar and the dim; the card's frame CANNOT (G-02) | `02`, `guest-cycle/` |
| 12 | § The merge debt's one line | met | `02` § The merge debt |
| 13 | § The runs: every command, the unit build's `TOTAL:` | the unit build owed | `02` § The runs |
| 14 | § The guest cycle | the window's record; `02` § The guest cycle filled at stage E's recompose | `guest-cycle/`, #681 START and RETURN |
| 15 | `00` shows no build, fetch, device or account | met so far | `00-running-log.md` |
| 16 | `04` answers Q1 to Q7; bugs with their three lines | this file; bugs filed at stage D | this file |
| 17 | every proof's `proved:` cell; § What T35 to T37 inherit | met in `02`; owed cells marked `pending:` | `02` |
| 18 | the retro | stage G | - |
| 19 | the map rows | no row proposed; the checker's line quoted | `02` § The structure |
| 20 | the five checkers and the ES pre-push test | at the hand-back | - |
| 21 | the unit build's `TOTAL:` line with 0 failed | owed | - |

## Risk assessment

- **The card's closing race (PL-01)** sits under every automatic sync and every achievements card. Its likely symptom is a fade that starts late, not a crash, but it is undefined behaviour. The fix is small and the covering case is a host ThreadSanitizer run.
- **The holders' raw pointers (PL-02)** are the larger risk. A worker that outlives its card writes into freed memory. The component cannot refuse the call; only a handle the window keeps alive can. That is a design ruling across T34, T35, T18 and T20, so it waits for the pause.
- **The image is M7's composition, not the pin.** PL-04 did not reproduce there, and PL-05 appeared only there. Neither is a finding about the pin until the pin's code is read for it.
- **No proof yet runs the components' own code.** Every case is owed to the unit build. Until it runs, a `tree` proof is a reading, and the seven FAIL-at-pin leads are expectations.

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
| #585 / #48 | PL-08, the reproducer owed | `05` |
| #182 | the dim measured on the image | `guest-cycle/g04-1-cloud-hub-en.png` |
| #325 | the wrap shown (G-05) | `guest-cycle/g05-4-after-up-up.png` |
| #210 | the bar's fit; read | `02` § The layouts |
| #27 | read; no grid theme | - |
| #243 | 3.22, 3.23 owed | `02` § The leads |
| #157 | read | - |
| #1112 | read-only context | - |
| T21 L-11 / #1199 | read; `SystemConf`'s | - |
| T21 PL-26 / #1192 | the field's masking named for T35's pause | - |
| T18's double | a collision named at the hand-back | `02` § The structure |
| T20's SCAN GAMES row | 3.4 owed | `02` § The leads |
| T31's func-form rows | the per-frame cost, priced in the retro | - |
| `es-ui-style-guide.md:202` | read as it stands | - |
| #585 | the lines owed | `02` § The #585 lines owed |

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

Depth **independent**: one seat, `gpt` (`openai/gpt-6-astra`, effort `max`), a probe and one refutation over `second-opinions/t34-packet.md` (`review-plan.json`). The outcome is recorded here after the refutation returns.

## Quality self-check

- Every count in `02` is a generator's or a command's own line. None is summed by hand.
- Every `tree` proof cites its lines at the pin. Every guest reading names its frame and is labelled `image`.
- The owed proofs are named, not implied: the unit build, the sanitizer cases, and the syntax check.
- The scorecard above has no total row; its states are words, not sums.
