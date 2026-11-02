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

Written at stage C by `tools/t39-tables.py q4` (`stage-c/tables/q4.md`; its line: `Q4 ids 442 (decided 435, open 7, unresolved 0); tools 69 (absent 2); issues 617; path references 2060`) from the
checker's read of the 223 (`stage-c/probes/read-*.tsv`, cross-checked against the export: the export's
citations equal the checker's) and the issue-state snapshot `stage-c/issues-snapshot.tsv` (read
2026-11-02 00:25:51Z, 1398 rows). What they show: **no reference document proper cites an open-decision
row as settled** -- the seven open rows cited are in the dated rules sweep and three ledger rows; **every
tool named exists** but the splash repositories' two (L-14, L-19, `external`); every dead path is classed;
the leads' baselines and counts read as § 3 says; the issue-cited lines hold, #1216's quoted label aside
(`03` § 3.5). The issues table counts states only: a closed issue cited as open is found by the leads
(L-03, L-06, L-08), not by this table, which is the boundary (no tool reads a sentence's tense).

#### (a) The decision IDs the 223 cite, with their rows' state

| area | distinct IDs cited | decided | open | unresolved | citations |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLOUD | 137 | 135 | 2 | 0 | 357 |
| INFRA | 10 | 10 | 0 | 0 | 26 |
| LAUNCH | 6 | 6 | 0 | 0 | 10 |
| NET | 9 | 8 | 1 | 0 | 11 |
| QA | 33 | 33 | 0 | 0 | 94 |
| RA | 38 | 37 | 1 | 0 | 90 |
| SYS | 12 | 11 | 1 | 0 | 17 |
| UI | 94 | 93 | 1 | 0 | 271 |
| WORKFLOW | 103 | 102 | 1 | 0 | 396 |
| **Total** | 442 | 435 | 7 | 0 | 1272 |

The IDs cited whose rows sit under `## Open decisions` (a document citing one as settled would mislead):

| ID | cited by |
| --- | --- |
| D-CLOUD-051 | `docs/rules-sweep-2026-09-12.md`, `docs/vm-qa-log.md` |
| D-CLOUD-122 | `docs/rules-sweep-2026-09-12.md` |
| D-NET-012 | `docs/cloud-sync-changelog.md` |
| D-RA-006 | `docs/vm-qa-log.md` |
| D-SYS-006 | `docs/rules-sweep-2026-09-12.md` |
| D-UI-120 | `docs/cloud-sync-changelog.md` |
| D-WORKFLOW-191 | `docs/reviews/plan-for-the-plan.md` |

#### (b) Every `tools/<name>` the 223 name, with its existence at the tip

| tool | exists | named by (files) |
| --- | --- | ---: |
| `tools/box-check` | yes | 3 |
| `tools/build-identity-test` | yes | 2 |
| `tools/ceremony-check` | yes | 2 |
| `tools/cloud-capture-stamp-test` | yes | 2 |
| `tools/cloud-census` | yes | 1 |
| `tools/cloud-connections-test` | yes | 1 |
| `tools/cloud-input-test` | yes | 1 |
| `tools/cloud-pair-migration` | yes | 3 |
| `tools/cloud-round-trip` | yes | 9 |
| `tools/cloud-save-integrity` | yes | 2 |
| `tools/cloud-save-integrity-test` | yes | 2 |
| `tools/cloud-test-backend` | yes | 6 |
| `tools/council` | yes | 4 |
| `tools/device-act` | yes | 2 |
| `tools/distro-tool` | yes | 2 |
| `tools/emulator-exit-test` | yes | 3 |
| `tools/es-launch-memory` | yes | 1 |
| `tools/es-menu-map-check` | yes | 4 |
| `tools/es-syntax-check` | yes | 4 |
| `tools/es-untranslated` | yes | 2 |
| `tools/find_build_warnings.sh` | yes | 1 |
| `tools/fixlecode.py` | yes | 1 |
| `tools/font-stems` | yes | 1 |
| `tools/forbidden-terms-check` | yes | 3 |
| `tools/fork-package-freshness` | yes | 5 |
| `tools/fork-publish-release` | yes | 1 |
| `tools/fork-worktree` | yes | 3 |
| `tools/frame-diff` | yes | 2 |
| `tools/host-maintenance` | yes | 3 |
| `tools/last-good-scripts-test` | yes | 10 |
| `tools/lint-audit-artifacts` | yes | 6 |
| `tools/mkpkg` | yes | 3 |
| `tools/mtstats.py` | yes | 1 |
| `tools/pixelelated-state-check` | yes | 1 |
| `tools/pixelelated-state-check-test` | yes | 1 |
| `tools/pixelelated-vm-cloud-boundaries` | yes | 1 |
| `tools/pixelelated-wordmark` | **no** | 1 |
| `tools/pkgcheck` | yes | 7 |
| `tools/pr-stack-check` | yes | 2 |
| `tools/qa-accounts` | yes | 2 |
| `tools/ra-offline-test` | yes | 3 |
| `tools/ra-ui-test` | yes | 2 |
| `tools/rasteratops-cloud-layout-test` | yes | 3 |
| `tools/rasteratops-vm-cloud-epic` | yes | 1 |
| `tools/rasteratops-wordmark` | **no** | 1 |
| `tools/rc-preflight` | yes | 4 |
| `tools/register-check` | yes | 3 |
| `tools/release-catalog` | yes | 1 |
| `tools/renovation-drift` | yes | 4 |
| `tools/renovation-inventory` | yes | 9 |
| `tools/renovation-status` | yes | 4 |
| `tools/retroarch-wrapper-test` | yes | 3 |
| `tools/rules-check` | yes | 1 |
| `tools/signin-memory` | yes | 2 |
| `tools/test-fixtures` | yes | 4 |
| `tools/time-to-play` | yes | 4 |
| `tools/update-scan` | yes | 1 |
| `tools/viewplan` | yes | 5 |
| `tools/vm-pair` | yes | 3 |
| `tools/vm-qa` | yes | 11 |
| `tools/vm-serial` | yes | 1 |
| `tools/vm-upgrade-rehearsal` | yes | 3 |
| `tools/vm-visual-qa` | yes | 5 |
| `tools/vm-walks` | yes | 3 |
| `tools/vocabulary-check` | yes | 2 |
| `tools/wait-lock-test` | yes | 2 |
| `tools/watch-build` | yes | 4 |
| `tools/watch-job` | yes | 2 |
| `tools/work-log-index` | yes | 2 |

#### (c) The issues the reference documents cite, against their state (snapshot of 2026-11-02 00:25:51Z)

| state | distinct numbers |
| --- | ---: |
| absent absent | 3 |
| closed issue | 369 |
| closed pr | 1 |
| open issue | 244 |
| **Total** | 617 |

Open issues cited by a reference document proper: 94 (#7, #10, #11, #12, #14, #15, #18, #19, #21, #22, #23, #24, #26, #33, #34, #35, #37, #42, #51, #54, #55, #63, #64, #65, #88, #104, #120, #133, #134, #135, #163, #168, #191, #192, #196, #201, #236, #251, #255, #265, #268, #292, #293, #309, #322, #323, #324, #328, #330, #331, #333, #336, #337, #338, #341, #344, #345, #346, #347, #348, #355, #359, #378, #387, #395, #432, #463, #464, #493, #509, #511, #516, #518, #528, #555, #558, #559, #560, #561, #562, #563, #568, #576, #585, #586, #587, #605, #607, #609, #613, #615, #616, #617, #665).

#### (d) The backticked repository paths, resolved, in the `paths` step's classes

| class | references |
| --- | ---: |
| external | 33 |
| historical | 5 |
| pattern | 1 |
| resolves | 2021 |
| **Total** | 2060 |

#### (e) Every baseline, catalog row or count a lead names, against its artifact

| lead | the statement | the artifact, read now |
| --- | --- | --- |
| L-09 | `next-candidate-work.md:4-5`: `0.0.1-dev+20261011T222153Z.gbc9dfe8141d9` (#555–#557). This does not relabel it as | `device-facts.md` records the 2026-10-16 transfer to `077197` |
| L-15 | `device-facts.md:7`: the cuts are in `catalog.md` | `bc9dfe8141` 0, `077197` 0, `8b511` 0, `a0f60255ab` 0 occurrences in the catalog |
| L-26 | `rc-accept.txt`: the acceptances stay as the record | 9 non-comment lines |
| L-41 | the per-device tables | 13 of 15 upstream-carried tables differ from `upstream/next` `651150fc88` |

#### (f) Every line number an issue cites in a reference document, against the line

| issue | cites | the line at the tip |
| --- | --- | --- |
| #1100 | `docs/releases/device-facts.md:17` | \| SM8550 boot on the Retroid Pocket Nova \| Actual Nova boot chain, storage and compositor after an in-place up |
| #1100 | `docs/releases/device-facts.md:18` | \| Nova frontend readiness after #529 \| Actual SM8550 frontend service startup on the corrected image \| 2026-10 |
| #1100 | `docs/releases/device-facts.md:19` | \| Nova shutdown and bootloader recovery \| Physical SM8550 power-off/restart and pre-Linux ABL behavior \| 2026- |
| #1126 | `docs/releases/device-facts.md:31` | \| Retroid Pocket Nova: the stick LEDs \| physical illumination and boot application of saved color/brightness o |
| #682 | `docs/es-menu-map.md:134` | \| **CONTROLLER & BLUETOOTH** \| SETTINGS · BLUETOOTH · DISPLAY OPTIONS · BEHAVIOR · PLAYER ASSIGNMENTS \| |
| #1216 | `docs/es-menu-map.md:405` | ### FINISH RESTORE SETUP (the checklist after a settings restore) |
| #667 | `docs/es-menu-map.md:595` | PAGE --> SCAN[SCAN GAMES FOR OFFLINE ACHIEVEMENTS<br/><i>NOT SCANNED YET . N GAMES READY FOR OFFLINE PLAY</i>< |

### Q5 Efficiency (the lens)

Written at stage C by `tools/t39-tables.py q5` (`stage-c/tables/q5.md`; its line: `Q5 rows 69; LOW-INBOUND files=33 lines=2770; population 70`): one row
per reference document proper (69). **R/O/D/W** are the inbound names, in files: `.claude/**` (R), the
root documents (O), the 254's text rows outside the ledgers (D, by path, distinctive file name, a named
parent directory, or a relative link that resolves to it) and the October work logs (W). **The low-inbound
line differs from R2 C26's and is recorded beside it, not argued:** 33 files, 2,770 lines against
`files=17 lines=2135`. The 33 contain all 17 of R2's list (the plan, the backup reference, the save
reviews, the rules sweep, the appendix, the council limits, the rc1 note, the rocknix.org stubs, the review
guide, the candidate plan, the proxy design note and the cloud layout) plus 16 R2's method counted as
named: the eleven seven-line PR descriptions under `docs/releases/pr/`, the rc2 note, the vocabulary audit,
the 2026-09-30 provider note and the two P0 records. R2's population and matching rule are not in the
tree; this generator's are its docstring. The heavy end and the upstream-carried cost are as stage B wrote
(the changelog 3,581, the map 989, `release-readiness.md` 990, `next-candidate-work.md` 963; `licenses/`
7,817 and `documentation/` 2,160 by `grep -c`).

| document | lines | last commit | R | O | D | W | role | read by | verdict |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| `README.md` | 23 | a9af618398 2026-10-04 | 14 | 2 | 32 | 7 | the front page | the rules, the root documents, other documents, the October logs | keep; fix L-02 |
| `TRADEMARK.md` | 38 | a9af618398 2026-10-04 | 0 | 2 | 9 | 3 | a redistributor's notice | the root documents, other documents, the October logs | keep |
| `docs/backup-contents.md` | 100 | 5ca1427ab5 2026-09-12 | 0 | 0 | 0 | 0 | a reference document | nobody named | § 4 question 2: date its first line or retire |
| `docs/cloud-save-integrity.md` | 100 | 1bd4554dc8 2026-10-08 | 2 | 0 | 1 | 0 | a cloud reference | the rules, other documents | keep; fix L-06 |
| `docs/cloud-vocabulary-audit.md` | 240 | 5ca1427ab5 2026-09-12 | 0 | 0 | 1 | 0 | a cloud reference | other documents | § 4 question 2: date its first line or retire |
| `docs/conflict-wizard-ia.md` | 323 | 0f073485ff 2026-10-08 | 2 | 2 | 4 | 0 | an interface reference | the rules, the root documents, other documents | keep |
| `docs/council-limits.md` | 54 | d430818548 2026-09-28 | 0 | 0 | 0 | 0 | a council note | nobody named | § 4 question 2: date its first line or retire |
| `docs/council-mistral-counter.md` | 127 | 5f1b343d25 2026-09-30 | 1 | 0 | 2 | 0 | a council note | the rules, other documents | keep; fix L-12 |
| `docs/council-staged-attempts.md` | 144 | 5f1b343d25 2026-09-30 | 1 | 0 | 3 | 0 | a council note | the rules, other documents | keep |
| `docs/council-staged-controller.md` | 279 | 5f1b343d25 2026-09-30 | 1 | 0 | 3 | 0 | a council note | the rules, other documents | keep |
| `docs/council-staged-derived-packages.md` | 101 | 5f1b343d25 2026-09-30 | 1 | 0 | 2 | 0 | a council note | the rules, other documents | keep |
| `docs/council-staged-derived-runtime.md` | 298 | 5f1b343d25 2026-09-30 | 1 | 0 | 3 | 0 | a council note | the rules, other documents | keep |
| `docs/council-staged-readings.md` | 180 | 5f1b343d25 2026-09-30 | 1 | 0 | 1 | 0 | a council note | the rules, other documents | keep |
| `docs/council-staged-rereads.md` | 129 | 5f1b343d25 2026-09-30 | 1 | 0 | 1 | 0 | a council note | the rules, other documents | keep |
| `docs/council-staged-sources.md` | 151 | 5f1b343d25 2026-09-30 | 1 | 0 | 4 | 0 | a council note | the rules, other documents | keep |
| `docs/device-flashing-runbook.md` | 534 | f7152d84a4 2026-09-20 | 1 | 2 | 2 | 0 | a device procedure | the rules, the root documents, other documents | keep; fix L-05 |
| `docs/device-testing-policy.md` | 122 | 3c31e2aa18 2026-10-15 | 3 | 2 | 1 | 0 | a device procedure | the rules, the root documents, other documents | keep; fix L-03, L-16 |
| `docs/es-menu-map.md` | 989 | 060dbde841 2026-10-16 | 4 | 2 | 3 | 0 | an interface reference | the rules, the root documents, other documents | keep; fix L-08, L-11 |
| `docs/pixelelated/art/README.md` | 26 | b137d8c373 2026-10-04 | 0 | 2 | 2 | 0 | the art's reference | the root documents, other documents | keep |
| `docs/pixelelated/art/wordmark-system.md` | 334 | bd3fcfa228 2026-10-04 | 0 | 2 | 3 | 0 | the art's reference | the root documents, other documents | keep |
| `docs/pixelelated/cloud-folder-flow-review.md` | 632 | 3fcff2e1e2 2026-10-11 | 0 | 0 | 2 | 1 | identity and the site | other documents, the October logs | keep; fix L-11 |
| `docs/pixelelated/cloud-folders.md` | 35 | 357d88010a 2026-10-07 | 0 | 1 | 2 | 1 | identity and the site | the root documents, other documents, the October logs | keep; fix L-10 |
| `docs/pixelelated/rename-plan.md` | 77 | 90f9e0eafd 2026-10-07 | 0 | 2 | 0 | 0 | identity and the site | the root documents | keep |
| `docs/pixelelated/site-dns.md` | 62 | 0f073485ff 2026-10-08 | 0 | 0 | 1 | 1 | identity and the site | other documents, the October logs | keep |
| `docs/pixelelated/site-plan.md` | 147 | 62c382f467 2026-10-15 | 0 | 0 | 0 | 1 | identity and the site | the October logs | keep; fix L-13, L-22 |
| `docs/pr-series/es-review-guide.md` | 124 | f75d680769 2026-09-29 | 0 | 0 | 1 | 0 | a reference document | other documents | § 4 question 2: date its first line or retire |
| `docs/ra-offline/2026_09_13-phase-1-design-note.md` | 590 | d40897de80 2026-09-14 | 0 | 0 | 0 | 0 | offline achievements design | nobody named | § 4 question 2: date its first line or retire |
| `docs/ra-offline/rocknix-org-offline-achievements.md` | 59 | d52e3d81c7 2026-09-24 | 0 | 0 | 0 | 0 | offline achievements design | nobody named | § 4 question 2: date its first line or retire |
| `docs/rasteratops/art/README.md` | 16 | 3d7c075f63 2026-10-02 | 0 | 0 | 0 | 1 | a dated record under the retired folder | the October logs | keep |
| `docs/rasteratops/candidate-source-plan.md` | 80 | ca5d034488 2026-10-12 | 0 | 0 | 0 | 0 | a dated record under the retired folder | nobody named | § 4 question 2: date its first line or retire |
| `docs/rasteratops/cloud-folder-state-table.md` | 334 | 357d88010a 2026-10-07 | 0 | 0 | 1 | 1 | a dated record under the retired folder | other documents, the October logs | keep |
| `docs/rasteratops/cloud-layout.md` | 116 | 9bb2b42e5a 2026-10-05 | 0 | 0 | 1 | 0 | a dated record under the retired folder | other documents | § 4 question 2: date its first line or retire |
| `docs/rasteratops/cloud-provider-2026-09-30.md` | 68 | a63b01ce14 2026-10-02 | 0 | 0 | 0 | 0 | a dated record under the retired folder | nobody named | § 4 question 2: date its first line or retire |
| `docs/rasteratops/p0-read.md` | 70 | 224b73ea54 2026-09-30 | 0 | 0 | 1 | 0 | a dated record under the retired folder | other documents | § 4 question 2: date its first line or retire |
| `docs/rasteratops/p0-sweep.md` | 142 | 224b73ea54 2026-09-30 | 0 | 0 | 1 | 0 | a dated record under the retired folder | other documents | § 4 question 2: date its first line or retire |
| `docs/rasteratops/p0-updater.md` | 70 | 224b73ea54 2026-09-30 | 0 | 0 | 2 | 0 | a dated record under the retired folder | other documents | keep |
| `docs/rasteratops/raofflineproxy-refresh.md` | 195 | a0f60255ab 2026-10-11 | 0 | 0 | 2 | 0 | a dated record under the retired folder | other documents | keep |
| `docs/rasteratops/release-readiness.md` | 990 | fb932eb1fe 2026-10-16 | 0 | 0 | 2 | 2 | a dated record under the retired folder | other documents, the October logs | keep; fix L-11 |
| `docs/rasteratops/support-matrix.md` | 162 | fb932eb1fe 2026-10-16 | 0 | 0 | 5 | 0 | a dated record under the retired folder | other documents | keep; fix L-11 |
| `docs/releases/0.0.1-release-note-draft.md` | 43 | 3416cb4043 2026-10-15 | 0 | 0 | 3 | 0 | a release record | other documents | keep |
| `docs/releases/0.0.1-release-note-evidence.md` | 40 | 3416cb4043 2026-10-15 | 0 | 0 | 3 | 0 | a release record | other documents | keep |
| `docs/releases/0.0.1-release-preparation.md` | 115 | 3c31e2aa18 2026-10-15 | 0 | 0 | 4 | 0 | a release record | other documents | keep; fix L-11 |
| `docs/releases/device-facts.md` | 31 | fb932eb1fe 2026-10-16 | 2 | 0 | 3 | 0 | a release record | the rules, other documents | keep; fix L-11, L-15 |
| `docs/releases/next-candidate-scope.md` | 233 | cdd92f1060 2026-10-15 | 0 | 0 | 3 | 1 | a release record | other documents, the October logs | keep; fix L-11 |
| `docs/releases/next-candidate-work.md` | 963 | 8ebaf8daad 2026-10-17 | 0 | 0 | 3 | 1 | a release record | other documents, the October logs | keep; fix L-09, L-11 |
| `docs/releases/pr/01-build.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/02-generic-x64.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/03-evidence.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/04-settings.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/05-network.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/06-retroachievements.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/07-cloud-setup.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/08-saves.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/09-retroarch.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/10-es-pin.md` | 7 | 826d52e395 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/pr/11-interface.md` | 13 | a71a8f2d49 2026-09-29 | 0 | 0 | 0 | 0 | a dated PR description | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/rc1-20260929-release-note.md` | 38 | 1070d05378 2026-09-29 | 0 | 0 | 0 | 0 | a release record | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/rc2-20260929-release-note.md` | 32 | fcfe296258 2026-09-29 | 0 | 0 | 0 | 0 | a release record | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md` | 13 | fa935ed6ba 2026-09-29 | 0 | 0 | 0 | 0 | a release record | nobody named | § 4 question 2: date its first line or retire |
| `docs/releases/versioning.md` | 138 | 40bc5469b9 2026-10-11 | 2 | 1 | 0 | 0 | a release record | the rules, the root documents | keep; fix L-11 |
| `docs/rules-sweep-2026-09-12.md` | 277 | 438f14bfff 2026-09-12 | 0 | 0 | 0 | 0 | a reference document | nobody named | § 4 question 2: date its first line or retire |
| `docs/save-history-consensus-amendment.md` | 116 | 9d6afb83cd 2026-09-12 | 0 | 0 | 4 | 0 | a save-format reference | other documents | keep |
| `docs/save-history-gap-analysis.md` | 92 | 77e65722e9 2026-09-12 | 0 | 0 | 1 | 0 | a save-format reference | other documents | § 4 question 2: date its first line or retire |
| `docs/save-history-plan-delta.md` | 40 | 77e65722e9 2026-09-12 | 0 | 0 | 0 | 0 | a save-format reference | nobody named | § 4 question 2: date its first line or retire |
| `docs/save-history-serial-model-addendum.md` | 111 | edd06db408 2026-09-12 | 0 | 0 | 0 | 0 | a save-format reference | nobody named | § 4 question 2: date its first line or retire |
| `docs/save-manifest-alignment-review.md` | 98 | 24dce33f23 2026-09-06 | 0 | 0 | 1 | 0 | a save-format reference | other documents | § 4 question 2: date its first line or retire |
| `docs/save-manifest-schema.md` | 555 | d52e3d81c7 2026-09-24 | 1 | 0 | 1 | 0 | a save-format reference | the rules, other documents | keep |
| `docs/savestate-compat-test.md` | 117 | 0c03ae4d83 2026-08-24 | 0 | 0 | 0 | 0 | a save-format reference | nobody named | § 4 question 2: date its first line or retire |
| `docs/technical-appendix-cloud-sync-and-offline-achievements.md` | 3 | fa935ed6ba 2026-09-29 | 0 | 0 | 0 | 0 | a reference document | nobody named | § 4 question 2: date its first line or retire |

`LOW-INBOUND files=33 lines=2770` over R2's reference population (70 documents); R2 C26 printed `files=17 lines=2135`.

| low-inbound document | lines | class | R | O | D | W |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| `docs/backup-contents.md` | 100 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/cloud-vocabulary-audit.md` | 240 | edit-scope | 0 | 0 | 1 | 0 |
| `docs/council-limits.md` | 54 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/pr-series/es-review-guide.md` | 124 | edit-scope | 0 | 0 | 1 | 0 |
| `docs/ra-offline/2026_09_13-phase-1-design-note.md` | 590 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/ra-offline/rocknix-org-offline-achievements.md` | 59 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/rasteratops/candidate-source-plan.md` | 80 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/rasteratops/cloud-layout.md` | 116 | edit-scope | 0 | 0 | 1 | 0 |
| `docs/rasteratops/cloud-provider-2026-09-30.md` | 68 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/rasteratops/p0-read.md` | 70 | edit-scope | 0 | 0 | 1 | 0 |
| `docs/rasteratops/p0-sweep.md` | 142 | edit-scope | 0 | 0 | 1 | 0 |
| `docs/releases/pr/01-build.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/02-generic-x64.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/03-evidence.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/04-settings.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/05-network.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/06-retroachievements.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/07-cloud-setup.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/08-saves.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/09-retroarch.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/10-es-pin.md` | 7 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/pr/11-interface.md` | 13 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/rc1-20260929-release-note.md` | 38 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/rc2-20260929-release-note.md` | 32 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md` | 13 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/rules-sweep-2026-09-12.md` | 277 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/save-history-gap-analysis.md` | 92 | edit-scope | 0 | 0 | 1 | 0 |
| `docs/save-history-plan-delta.md` | 40 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/save-history-serial-model-addendum.md` | 111 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/save-manifest-alignment-review.md` | 98 | edit-scope | 0 | 0 | 1 | 0 |
| `docs/savestate-compat-test.md` | 117 | edit-scope | 0 | 0 | 0 | 0 |
| `docs/technical-appendix-cloud-sync-and-offline-achievements.md` | 3 | edit-scope | 0 | 0 | 0 | 0 |
| `plans/conflict-resolution/vita-style-conflict-resolution.md` | 223 | ledger-plan | 0 | 0 | 1 | 0 |

### Q6 Dead ends

Written at stage C by `tools/t39-tables.py q6` (`stage-c/tables/q6.md`; its line: `Q6 dead 41 (paths and tools) plus 3 inherited; rows 44`): every
backticked path and `tools/` name the 223 point at that the tip lacks, each re-checked absent at the tip
and found at its line in the export, with its allowlist class and reason (an unclassed one fails the
generator), then the three inherited absences (L-27's two map paths, L-33's document). None is an
unclassed finding: the real absent in-tree path `packages/rocknix` is L-20's dated record; the rest name
another repository (the splash tools, the site's pages and branch, RAOfflineProxy's paths, the bisync
branch) or are an install output. The documents nobody names are Q5's LOW-INBOUND set; the
generator-less GENERIC_X64 table is L-31's.

| what the document points at | where | resolves at the tip | class | reason |
| --- | --- | --- | --- | --- |
| `docs/cloud-saves-native-wizard` | `docs/pixelelated/site-plan.md:70` | no | external | L-13: docs/cloud-saves-native-wizard is a branch of the rocknix.org site checkout (X02) |
| `docs/linux-support/installation.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:62` | no | external | the RAOfflineProxy repository's documentation path (the design note reads that repository) |
| `scripts/install.sh` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:65` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/tool-launcher.sh` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:73` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/uninstall.sh` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:114` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/install.sh` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:132` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/uninstall.sh` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:132` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/launcher-raofflineproxy` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:133` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/launcher-raofflineproxy-uninstall` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:134` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/tool-launcher.sh` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:135` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/sdl-doctor.sh` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:136` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `scripts/sdl_probe.py` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:136` | no | external | the RAOfflineProxy repository's scripts/ (the design note reads that repository) |
| `docs/caveats.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:258` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/linux-support/cfg-patching.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:265` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/cfg-patching.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:265` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/linux-hash-chain.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:317` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/hash-chain.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:332` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/pending-awards.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:341` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/linux-hash-chain.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:350` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/hash-chain.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:351` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/privacy-policy.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:410` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/pending-awards.md` | `docs/ra-offline/2026_09_13-phase-1-design-note.md:489` | no | external | the RAOfflineProxy repository's docs/ (the design note reads that repository) |
| `docs/configure/offline-achievements.md` | `docs/ra-offline/rocknix-org-offline-achievements.md:3` | no | external | L-13: two pages of ROCKNIX/rocknix.org, the line names the site |
| `docs/configure/retroachievements.md` | `docs/ra-offline/rocknix-org-offline-achievements.md:3` | no | external | L-13: two pages of ROCKNIX/rocknix.org, the line names the site |
| `packages/rocknix` | `docs/rasteratops/p0-read.md:11` | no | historical | L-20: packages/rocknix in a dated P0 record, which does not present itself as current |
| `packages/rocknix` | `docs/rasteratops/p0-sweep.md:39` | no | historical | L-20: packages/rocknix in a dated P0 record, which does not present itself as current |
| `docs/configure/cloud-sync.md` | `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md:5` | no | external | L-13: five pages of ROCKNIX/rocknix.org, the PR this draft describes |
| `docs/configure/networking.md` | `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md:5` | no | external | L-13: five pages of ROCKNIX/rocknix.org, the PR this draft describes |
| `docs/play/retro-achievements.md` | `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md:5` | no | external | L-13: five pages of ROCKNIX/rocknix.org, the PR this draft describes |
| `docs/configure/scraper.md` | `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md:5` | no | external | L-13: five pages of ROCKNIX/rocknix.org, the PR this draft describes |
| `docs/contribute/cloud-sync-internals.md` | `docs/releases/rocknix-org-pr-cloud-sync-wifi-achievements.md:5` | no | external | L-13: five pages of ROCKNIX/rocknix.org, the PR this draft describes |
| `tools/council/node_modules/.bin/tsx` | `docs/reviews/briefs/p1-survey.md:53` | no | pattern | tools/council/node_modules/.bin/tsx is npm's install output, gitignored (.gitignore:66), named as what tools/council/run execs |
| `docs/es-ui-style-guide.md` | `docs/rules-sweep-2026-09-12.md:13` | no | historical | a dated sweep of the rules as they stood on 2026-09-12 (its paths, names and retired recipes are that day's) |
| `docs/es-ui-style-guide.md` | `docs/rules-sweep-2026-09-12.md:41` | no | historical | a dated sweep of the rules as they stood on 2026-09-12 (its paths, names and retired recipes are that day's) |
| `packages/readme.md` | `docs/rules-sweep-2026-09-12.md:218` | no | historical | a dated sweep of the rules as they stood on 2026-09-12 (its paths, names and retired recipes are that day's) |
| `plans/bisync/rclone-bisync-planning.md` | `docs/save-manifest-alignment-review.md:13` | no | external | a path on the branch rclone-bisync-beta, named with its branch on the line |
| `docs/contribute/cloud-sync-internals.md` | `docs/technical-appendix-cloud-sync-and-offline-achievements.md:3` | no | external | L-13: a rocknix.org page on the site checkout's branch, named so on the line |
| `docs/cloud-saves-native-wizard` | `docs/technical-appendix-cloud-sync-and-offline-achievements.md:3` | no | external | L-13: a rocknix.org page on the site checkout's branch, named so on the line |
| `.github/workflows/tests.yml` | `docs/upstream/raofflineproxy/contribution-map.md:59` | no | external | the RAOfflineProxy repository's CI workflow (#585's queue, read-only) |
| `tools/pixelelated-wordmark` | `docs/pixelelated/art/README.md:21` | no | external | L-14: pixelelated/splash's tools/pixelelated-wordmark, named with its repository (X02) |
| `tools/rasteratops-wordmark` | `docs/rasteratops/art/README.md:8` | no | external | L-19: rasteratops/splash's tools/rasteratops-wordmark, named with its repository (X02) |
| `projects/ROCKNIX/packages/network/rclone/sources/post-update` | docs/pr-series/map.txt:112 | no | L-27 | inherited:coordinator |
| `projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout` | docs/pr-series/map.txt:174 | no | L-27 | inherited:coordinator |
| `docs/graphics-memory-testing.md` | #576 :7, #620 :16 | no | L-33 | inherited:coordinator |

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
