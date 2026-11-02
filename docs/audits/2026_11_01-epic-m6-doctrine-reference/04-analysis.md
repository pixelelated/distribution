# Analysis -- M6.P2 T39, the reference documents (#686)

Phase 4 over the 254 at Local depth (plan § 6c, D-WORKFLOW-184). The executor works
alone. The lint and the counts are the check, and § 5's rule 4 (*what result would
have produced a FAIL?*) is asked of every PASS below, because no one else asks it at
this depth.

- **reviewed-at:** `86ebb6dffc`.
- **Written:** at the stage-B completion (#686, issuecomment-6565986529).
- **Pending:** Q4 to Q6's tables are `tools/t39-tables.py`'s and are written at stage C.

## Executive summary

**The slice.** The 254 reference documents are:
- 69 reference documents proper;
- 20 ledger rows;
- 31 binaries and 18 art text files, tabled and never edited;
- 117 read-only rows: 88 upstream-carried, 27 of #585's queue, `LICENSE.md` for #528,
  and the GENERIC_X64 table.

They were read once as a reader and again as an auditor, in § 2's order (`01` § The
reader's pass). **Every one of the brief's 46 leads printed its defect at the tip**
(`02` § The table). None was withdrawn.

**The findings, by disposition:**

| Disposition | Leads |
| --- | --- |
| fix candidates in the edit scope | L-02, L-03, L-04, L-05, L-06, L-07, L-08, L-09, L-10, L-11, L-12, L-13, L-15, L-16, L-18, plus L-17 and L-22 where the conditions hold |
| recorded as a ledger row or a `none` Coverage row | L-01, L-14, L-19, L-20, L-21, L-23, L-24, L-26 |
| inherited to the coordinator | L-03's rule half, L-15's catalog half, L-25, L-27, L-28, L-29, L-31, L-33, L-34, L-35, L-36, L-37, L-40, L-42 |
| inherited to an owner issue | #270 (L-15's tool half), #509 (L-30), #511 (L-22 where it is not fixed), #947 (L-38), #1013 (L-39), the interface lanes (L-17, L-32), the next upstream base merge (L-41) |
| #528 | L-43, L-44, L-45 |
| #585 | L-46, and L-11's `docs/upstream/README.md` share |

**Grades** (Phase 4.5 below; no Critical, no High):
- **6 Medium**, each a statement a reader acts on wrongly (§ 4 Q3), each a `bug` at
  stage D:

  | Lead | What the reader does wrong |
  | --- | --- |
  | L-02 | the front page sends a player to a release that does not exist |
  | L-03 | the policy calls a decided row open |
  | L-04 | a retired migration script is described as current |
  | L-05 | the flashing runbook names the OS wrongly throughout |
  | L-07 | the backup reference, the stated source of truth for the public docs, names labels the pin does not ship |
  | L-16 | the read mask a reader copies prints a credential flag |

- **11 Low:** L-06, L-08, L-09, L-10, L-11, L-12, L-13, L-15, L-18, plus L-17 and L-22
  where they hold.

**The shape.** The defects cluster where the rules send readers. Seven of the 11
documents the rules name most carry a fix candidate (`03` § 3.5). They also share one
family: a *record presenting itself as current*. In each, a status line was written
true and left in place when the state moved (`03` § 3.3: L-03, L-08, L-09 and L-15
were edited after the change that made them untrue, without the sentence being
touched).

**What did not drift.**

| Check | Result | What would have failed it |
| --- | --- | --- |
| relative links | 0 dead of 511 | the same scan resolved against the export alone read 417 dead, so the zero is not vacuous |
| decision IDs | 0 unresolved of 442 cited | a planted `D-CLOUD-9999` fails the stage-C `cites` step |
| capitalised `Pixelelated` | 0 | the identity step fails a planted heading |
| binaries and art bytes | unchanged | -- |
| removal check | empty | -- |

## Acceptance-criteria scorecard

The 27 checkboxes of #686's body (brief § 7) at the stage-B completion:

| # | Criterion (short) | State at stage B |
| --- | --- | --- |
| 1 | the folder holds `00`-`05`, `second-opinions/`, `stage-a/`-`stage-e/`, `tools/`, no `guest-cycle/` | partial: `00`-`04`, `stage-a/`, `stage-b/` now; `05` at D, `stage-c/`-`stage-e/` at C-E |
| 2 | the lint PASS (pre-issue before D, resolution at close), Q1-Q7 answered, every item with `question:` | pending C/D (Q1-Q7 subsections exist below) |
| 3 | `review-plan.json` Local, `ls second-opinions/` that file alone, the census | pending C (the model ruling is #686, 00:12 UTC) |
| 4 | the punch list's items at a Phase 7 outcome, `box-check` 0 fail | pending D-F |
| 5 | `reviewed-at`/`fixed-at`, the removal check, the registers' 0, only the lane's commits | pending H; the removal check is empty at every stage so far |
| 6 | `01` § Scope: the membership block's lines | **done** at A (`stage-a/block.out`) |
| 7 | `01` § Scope: the split block's lines, `CARVE`, the `--order` row | **done** at A (`stage-a/split-*.out`, `order.out`) |
| 8 | `00`: the lint's Local proof first, L-01's loop | **done** at A (`stage-a/lint-local-*.out`) |
| 9 | `02` § Coverage, 254 rows | pending C (`t39-tables.py`) |
| 10 | `02` § The table, 46 leads | **done** at B (`grep -o -w -E 'L-[0-9]{2}'` sorted unique: 46) |
| 11 | `02` § Binaries 31 and § Art bytes 18, the `fixed-at` column | tip column **done** at B; `fixed-at` at E |
| 12 | the ledger rows untouched | holding (removal check empty); proved at H |
| 13 | the read-only paths untouched | holding; proved at H |
| 14 | `02` § The runs, every checker's line | partial at B; stage C reruns each with its output kept |
| 15 | `es-menu-map-check` at the tip and at `fixed-at` | tip **done** (`0 missing`); `fixed-at` at E |
| 16 | `t39-checks.sh`'s four runs | pending C (three runs), E (the fourth) |
| 17 | the identity words and retired names at the tip and after E | tip **done** at B; after E at E |
| 18 | `04` Q4's tables, Q5's table, Q6's table, time to play untouched | pending C (`t39-tables.py`); time to play: below |
| 19 | § 4's two questions in `04` and on #686 | written below; posted at D |
| 20 | every fix's check lines in `02` § The streams | pending E |
| 21 | `02` § What the coordinator and the next slices inherit | **done** at B; the R3 C24 lead's six paths added at C (the coordinator's acceptance) |
| 22 | every bug's trace, punch items' ladder stage, take-up rows, rulings' rows | pending D |
| 23 | `proved:` cells equal `^PROOF:` lines | 0 against 8 at B; carried to F (the acceptance's carry 1) |
| 24 | the host file carries no line of this lane's | holding: 0 (the coordinator's own line 802 excluded, per its acceptance) |
| 25 | the retro | pending G |
| 26 | the five checkers pass before the hand-back merge and on the simulated merge | pending H |
| 27 | the hand-back: one comment, one tip, `box-check --issue 686` 0 fail | pending H |

## Risk assessment

| Risk | Likelihood | Effect | Hold |
| --- | --- | --- | --- |
| a stage-E edit moves a line an issue cites (L-15, L-32) | medium | the issue's citation silently points at another row | record the cited lines before and after (`03` § 3.5 table); never insert above `device-facts.md:17` without saying so on the issues |
| a "fix" reaches a historical record `NAMING.md` keeps | medium (the futro's prediction) | a dated record rewritten | the allowlists' `historical`, `character` and `provenance` classes; stage-E edits only under a stream brief |
| the catalog read as current because `--check` passes | high, already happened (L-15) | readers look for cuts the catalog lacks | L-15's pointer fix; the catalog's regeneration is the coordinator's; #270's tool |
| L-17's IA read against its four rows stays unread | -- | a contradiction stays in the wizard's IA | `[unverified]`, raised at D; the interface lanes own the screen half |
| the reader's pass over 223 text rows missed a guest claim | low | an unverified claim kept | brief § 5 rule 3: none found; any found later is `[unverified]` with its proof |
| the lane's own probe or checkpoint misreports | **happened twice** (417 dead; the four missing artifacts) | a wrong record accepted | every count by a tool's line; the checker is seen to fail on each planted defect before its pass counts |

## Coverage boundary

**Read:** the 254 at the dispatch tip, the 223 text rows whole, the 31 binaries by
size and sha256 (L-44's PDF by its upstream deletion). The rules and the register were
read at the sections § 3 item 1 names.

**Not read, with the reason:**

| Not read | Why | What would settle it |
| --- | --- | --- |
| the seven rocknix.org pages and the site branch | another repository, never fetched (L-13) | a read of a local site checkout by `git ls-tree` |
| the RAOfflineProxy repository's paths the design note names | another repository (`allow-legit` `external`) | -- |
| the EmulationStation source beyond L-07's labels | ruling (g) | -- |
| any handheld | no physical fact is asked of this slice (brief § 5) | -- |
| L-17's IA sentence by sentence against D-CLOUD-024/027/032/041 | `[unverified]`, carried to D | the reading |
| L-13's pages' existence | `[unverified]` | the site checkout |
| L-24's superseding row | `[unverified]`; `tools/archaeology --no-gh 'KEEP CLOUD'` not yet run | that run |

**Not this slice's at all:**
- the rules, `CLAUDE.md`, `AGENTS.md`, `NAMING.md` and the registers (T4's);
- the daily records (T46's);
- the skills (T38's);
- the screens behind the map (the interface lanes').

## Finding verification (Phase 4.5)

Local depth has no other reviewer, so every fix candidate is verified here, in full.
Each entry gives:
- the check line's result at the tip (re-run at `2d09ed5c4d`);
- the design-intent read (`git log -S`, `03` § 3.3);
- the verdict.

### L-02 (README.md:9)
`instructions attached` = 1. `gh release list` prints `rc1-20260929`, `dev-20260827`,
`dev-rk3326-20260819`, and no 0.0.1. #344 is OPEN. The sentence was written
`3d7c075f63` 2026-10-02 for a release that was never cut.
**Verdict:** **confirmed, Medium (bug).** A player follows the front page to
instructions that are not there.

### L-03 (docs/device-testing-policy.md:5)
`Open:.*D-QA-016` = 1. D-QA-016 was decided 2026-09-13 and D-QA-027 2026-09-17. #131
was CLOSED 2026-09-20. The file was last edited 2026-10-15 without this line.
**Verdict:** **confirmed, Medium (bug).** A tester treats the dedicated-handheld
question as open. `vm-first.md`'s sentence is the coordinator's.

### L-04 (docs/rasteratops/cloud-layout.md:16; docs/releases/pr/08-saves.md:5)
Both lines print. `D-CLOUD-175` occurs 0 times in each file. The shipped OS
(`projects`, `packages`, `scripts`) carries 0 `cloud_migrate_layout`.
**The other hits, read and classed:**
- `cloud-vocabulary-audit.md:189` is a 2026-09-06 audit naming what it read.
- `cloud-folder-state-table.md:46,61` are line-cited reads of the script at their date.
- `release-readiness.md:874` sits under a heading reading *review baseline*, about
  #356, which closed 2026-10-05.

All four are historical.
**Verdict:** **confirmed, Medium (bug)** for the two files.

### L-05 (docs/device-flashing-runbook.md)
`ROCKNIX` = 21, `pixelelated` = 0. The file was last edited 2026-09-20, before
D-WORKFLOW-144. `CLAUDE.md`, `AGENTS.md` and `device-builds.md:616` send every
fresh-card flasher here.
**Verdict:** **confirmed, Medium (bug)**, fixed only where `NAMING.md` decides the word.
The remaining `ROCKNIX` lines are classed as labels, paths or the upstream project.

### L-06 (docs/cloud-save-integrity.md:4)
`M7 order remains` = 1. The three issues closed 2026-10-08, the day the line was
written. The milestone body owns order.
**Verdict:** **confirmed, Low.**

### L-07 (docs/backup-contents.md:3-4)
**BACKUP CONFIGURATIONS**, **RESTORE FROM BACKUP** and **RESTORE EVERYTHING** each
read 0 at the pin `16dbac5211` (stage B, `git -C ~/Development/emulationstation-next
grep -F -c`, read-only). *configurations* and *everything* are banned (D-UI-022). The
file calls itself the source of truth for the rocknix.org docs.
**Verdict:** **confirmed, Medium (bug).** A docs writer copies labels the image does
not show.

### L-08 (docs/es-menu-map.md:758, 806, 817)
Three headings print. #570 was CLOSED 2026-10-14. The third heading's issue state is
unsaid. `es-menu-map-check` prints `0 missing` and cannot see headings.
**Verdict:** **confirmed, Low**, the headings only (ruling (b)). The journal's home is
§ 4 question 1.

### L-09 (docs/releases/next-candidate-work.md:4)
`baseline is` at `:4`, naming `0.0.1-dev+20261011T222153Z.gbc9dfe8141d9`.
`device-facts.md` records the 2026-10-16 transfer to `077197`. The file was last
edited 2026-10-17, after that transfer.
**Verdict:** **confirmed, Low.**

### L-10 (docs/pixelelated/cloud-folders.md:32)
`prepared release documentation` = 1. #508 closed 2026-10-08. `README.md:22` sends
players to this guide.
**Verdict:** **confirmed, Low.**

### L-11 (ten files)
The heuristic's counts (`02` § The table). This is a legibility defect, not a check.
**Verdict:** **confirmed, Low**, edit scope only. `docs/upstream/README.md` goes to
#585 and `rc-accept.txt` is a ledger row.

### L-12 (docs/council-mistral-counter.md)
`sealed|retired|scaffold#915` = 0. The note documents a counter for a seat outside
every run profile.
**Verdict:** **confirmed, Low** (a banner). `council-limits.md` belongs to § 4
question 2.

### L-13 (four files)
`docs/cloud-saves-native-wizard` is ABSENT from the tree. It is the site checkout's
branch (X02).
**Verdict:** **confirmed, Low**: the repository is named beside each page. The pages'
existence is `[unverified]`.

### L-15 (docs/releases/device-facts.md:7)
All four cut hashes are 0 in `catalog.md`. The catalog's newest row is 2026-10-02.
`release-catalog: current (99 cuts)`.
**Verdict:** **confirmed, Low**: the pointer fix, without moving a cited row. The tool
half is #270's, and the regeneration is the coordinator's (#964).

### L-16 (docs/device-testing-policy.md:94)
`--(token` = 0. `engineering-practices.md` added the flag form 2026-10-30.
**Verdict:** **confirmed, Medium (bug).** A reader masking a command line by the
policy's long form prints a flag's credential.

### L-17 (docs/conflict-wizard-ia.md)
Rev 6 is at `:19` and rev 5 at `:29`. The text has not been read against the four
rows.
**Verdict:** **`[unverified]`**, carried to D. Fix where a sentence contradicts a
decided row; otherwise the interface lanes'.

### L-18 (the low-inbound documents)
R2 C26's set of 17. `t39-tables.py` re-derives it at stage C (Q5).
**Verdict:** **confirmed in shape, Low.** A dated first line where a record presents
itself as current. Retirement is § 4 question 2.

### L-22 (docs/pixelelated/site-plan.md:72)
*"Remotes still name `maxengel/rocknix.org`"*. #511 is OPEN.
**Verdict:** **conditional, Low.** Fix where the sentence misstates the present (#511's
last comment read at D), otherwise #511's.

The ledger, inherited, #528 and #585 leads are not graded here. Each is a `02` row
with its owner, and § 8's list carries them.

## Renovation face

### Q1 Modernize

The documents still written against retired mechanisms:

| Retired mechanism | Leads | Retired by |
| --- | --- | --- |
| the cloud-folder migration | L-04, L-10 | D-CLOUD-175 |
| the closed upstream series | L-27, L-34 | D-WORKFLOW-084 |
| Rasteratops as the OS's name | L-21, L-25, L-30 | D-WORKFLOW-144, -151 |
| a package upstream dropped | L-44 | `c4d353449e` |
| upstream's tables, three regenerations behind | L-41 | -- |
| the July conflict plan | L-24 | the IA's KEEP BOTH/LEFT/RIGHT, no MERGE |

In the edit scope, only L-04 and L-10 change text. The rest are inherited, ledger or
read-only rows.

### Q2 Standards

**`NAMING.md`.**
- No capitalised brand anywhere.
- Every capitalised `Rasteratops` line is the character, a historical record,
  provenance, or one of four leads (L-21, L-22, L-23, L-25).
- The one current document that names the OS wrongly throughout is the runbook (L-05).

**`es-player-text.md`.** Two banned words, in the document that claims to be the
public docs' source (L-07).

**D-UI-039.** The map's tree is current. Its journal headings are not (L-08).

**Dated records** that do not say they are dated: L-06, L-09, L-18.

The stage-C `identity` and `retired` steps hold the standard line by line through the
allowlists' classes.

### Q3 Bugs

Six statements a reader acts on wrongly: L-02, L-03, L-04, L-05, L-07 and L-16. Each
is filed at stage D as a `bug` with:
- its trace (the statement at its `path:line`, the artifact it misdescribes, the
  artifact the corrected statement must match);
- its `Already written:` line;
- *"Can this be done on the VM? No -- the tree, the tool or the register shows it"*.

Everything else is a punch item, an inherited item or a ledger row.

### Q4 Currency

**Its tables are `tools/t39-tables.py`'s, written at stage C:**
- the decision IDs with their rows' state;
- the tools named with their existence;
- the issues cited with their states;
- the paths named with their class;
- the counts and baselines with their artifact;
- the line numbers issues cite, with the line.

Stage B's figures, which those tables re-derive:
- 442 distinct IDs, 0 unresolved, against 716 rows;
- the § 3 item 9 issues: 36 OPEN and 6 CLOSED (`stage-a/issue-states.txt`);
- the issue-cited lines in `03` § 3.5.

### Q5 Efficiency (the lens)

**Its table is `tools/t39-tables.py`'s, written at stage C.** It has one row per
reference document proper (69), with:
- lines and last commit;
- the R/O/D/W inbound counts;
- role, reader and verdict.

It also carries the low-inbound line re-derived against R2 C26's `files=17 lines=2135`.

**The heavy end** (lines at the tip):

| Document | Lines | Note |
| --- | ---: | --- |
| `docs/cloud-sync-changelog.md` | 3,581 | a ledger row |
| `docs/es-menu-map.md` | 989 | 279 of them the journal |
| `docs/rasteratops/release-readiness.md` | 990 | -- |
| `docs/releases/next-candidate-work.md` | 963 | -- |

`licenses/` (7,817 lines) and `documentation/` (2,160) are upstream's. They cost a
reader nothing except through L-41, L-43 and L-44.

### Q6 Dead ends

**Its table is `tools/t39-tables.py`'s, written at stage C**, from the `paths` and
`tools` steps and the inbound columns. Stage B's candidates:
- the dead paths: `packages/rocknix` (L-20);
- the external names: `tools/pixelelated-wordmark`, `tools/rasteratops-wordmark` and
  `docs/cloud-saves-native-wizard` (L-13, L-14, L-19);
- the two deleted map paths (L-27);
- the document two open issues cite (L-33);
- the generator-less GENERIC_X64 table (L-31);
- the documents nobody names (L-18).

### Q7 Clarity

A reader new to these documents cannot always tell in one pass what a document is for
and whether it is current:
- the map's journal inside the reference (L-08);
- a player's guide ending in internal status (L-10);
- words and numbers run together (L-11: 122 hits in `release-readiness.md`, 46 in
  `next-candidate-work.md`);
- records with no date in the first line (L-18);
- two counts of the documents that load nowhere (L-36, the coordinator's);
- a preliminary slice number in the order (L-29, a ledger row).

The reader's pass (`01`) is the evidence.

**Time to play: untouched.** No path of the 254 reaches an image, so neither number
moves.

### The two questions for the maintainer (brief § 4; posted on #686 at the stage-D pause)

1. **The menu map's dated journal: keep it in the map, marked historical, or move it
   into the qa-logs it already links?**

   Today an agent placing a row reads 279 lines under 16 headings of dated candidate
   narrative after `## Not mapped`. Two of those headings call closed work pending.
   T39 corrects those headings either way. Moving the journal is a restructuring this
   slice does not do. (Ruling (b), L-08.)

2. **The reference documents nobody reads: keep each with a dated first line, or
   retire it?**

   Today the documents with no inbound name from the rules, the root documents or the
   October work logs, and at most one from `docs/`, are R2 C26's 17 (2,135 lines). The
   stage-C Q5 table re-derives the set. Among them are the council limits note, two
   rocknix.org stubs and a 590-line design note whose paths are another repository's.
   Keeping them costs a reader a search result that looks current. Retiring them is a
   removal, which is the maintainer's call and never stage E's. (L-12, L-13, L-18.)

## Instruction file recommendations

These are proposals for the coordinator, never edits here:

1. **Promote `t39-checks.sh` to a fork tool** (`tools/docs-check`, R3 § 2.9) with its
   `links`, `paths`, `tools`, `identity`, `retired` and `cites` steps, and add it to CI.
   No CI step reads a reference document for whether it misleads (R3 § 1).
2. **Widen `register-check`'s `LIVE`** to every reference document (L-38, #947).
3. **#270's device-facts check** (L-15).
4. **A rule line:** a status sentence in a reference document carries its date, or the
   document's first line does. All four of `03` § 3.3's drifted sentences are status
   lines without dates.

## Second opinion (Phase 4.6)

**Not applicable at Local depth (plan § 6c).** There is no reviewer, no packet, no
Facilitator and no keyed call. `second-opinions/review-plan.json` (stage C) records
depth `local` and `tier_exception` `D-WORKFLOW-184`.

## Quality self-check

| Check | Result |
| --- | --- |
| every figure is a command's line | yes: each cites its command or the artifact that holds it |
| what would have failed each PASS | stated beside each one in the executive summary; the checker's mutations prove it at stage C |
| leads re-numbered or merged | none: the brief's L-01 to L-46 are used throughout |
| a fix landed at stage B | none: `git status --short` was empty for the 254 at each stage-B session's end |
| unverified items | marked (L-13, L-17, L-24), each with what would settle it |
| the lane's own errors | recorded: the 417-dead probe, the case-sensitive `errat`, and the four artifacts missing from the first stage-B checkpoint |
