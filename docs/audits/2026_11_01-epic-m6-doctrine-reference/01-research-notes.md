# T39 (#686) research notes -- doctrine: the reference documents

## Scope

The membership is the brief's § 2 two blocks, extracted from the brief at `89fd4e2610` by their markers and never retyped, and run from the lane's worktree (stacked on P1 `2174265e9c`, which carries `docs/reviews/{slices,inventory,areas}.json` -- sha256 prefixes `49bc2745664e52f4`, `d17b9cac4b2c2245`, `985f742cfd4a2138`). The extracted blocks: `block.sh` sha256 `e81453b6732cdea8` (130 lines), `split.sh` sha256 `afb1909c5cdc6c88` (46 lines).

### `block.sh` (the membership), as it printed (rc 0)
- **254 paths** (`.qa-scratch/t39/paths.txt`), **223 text rows**; `mine: 254 paths.txt: 254 equal: True`, `only-mine: []`, `only-paths.txt: []`.
- Heads: distribution inventory `eb4763e3cc`, merge base `c445081a59`, `upstream/next c1f1746828`.
- **Tiers:** `fork-own 164, upstream-carried 90`; fork-own 28,749 lines, upstream-carried 9,849.
- **Lines, three ways (ruling (h)):** 38,598 by the inventory's column (`eb4763e3cc`); **38,674 by `wc -l`** and **38,675 by `grep -c ''`** over the 223 text rows at the P1 tip `2174265e9c`. The 31 binaries named and not counted.
- `GROUPS TOTAL 254 38598 groups 15`; both derived trees (inventory head, P1 hash) equal to `mine`, `only-*` empty.
- `MB..P1: 164 files changed, 28807 insertions(+), 75 deletions(-)`; `IH..P1: 9 files changed, 197 insertions(+), 120 deletions(-)`.

### `split.sh` (defaults, under `en_US.UTF-8`; X01: compare as a set, each once)
`L1-renovation-records same 12`, `L2-running-records same 3`, `R-fork-assets same 41`, `R-fork-reference same 108`, `R-upstream-carried same 90`; `the selector reaches: 254 paths; added since P1: 0; of the 254 absent: 0`; `added under docs/reviews/briefs/: 0`.

### `split.sh` at the dispatch tip (`TIP=86ebb6dffc`)
`tip: 86ebb6dffc`; `L1-renovation-records changed 2` (the two `docs/reviews/` rows the branch moved -- their `tip:` lines recorded here), `L1-renovation-records same 10`, `L2-running-records same 3`, `R-fork-assets same 41`, `R-fork-reference same 108`; `the selector reaches: 338 paths; added since P1: 84; of the 254 absent: 0` -- **no absent row among the 254 (ruling (p))**. The lines before `tip:` agree with the defaults run (`diff` clean).

### `renovation-inventory --order` (no `MISSING`, L-01 resolved)
`rc=0 lines=50`; `slices: 46`; `rows: 134634 (inventory: 134634)`; `unassigned: 0`; `ambiguous: 0`; the T39 row: `39 doctrine-reference  doctrine  254 paths  38,598 lines  190 read  190 fork-own  0 patch  table`.

### The carve (ruling (a)), printed by `block-2.txt`'s TSV, never typed
`art-bytes 18` · `edit-scope 68` · `edit-under-naming 1` · `ledger-binary 31` · `ledger-named 6` · `ledger-plan 1` · `ledger-reviews 12` · `read-only-528 1` · `read-only-585 27` · `read-only-upstream 88` · `tabled-generic-x64 1` · **total 254** -- the brief's § 2 classifier run unmodified against `block-2.txt`'s TSV, matching the brief's v2 expectation (`:1297`) byte for byte. The reference documents proper the lane may touch at stage E are `edit-scope` 68 and `edit-under-naming` 1 (`TRADEMARK.md`, where `NAMING.md` decides the word). The pointer's lens prose and `:188`/`:2316` record version 1's proof (K26) reading `edit-scope 69`/`ledger-named 5`; version 2 added `docs/rasteratops/p0-sweep-hits.txt` to the `NAMED` set, moving it from `edit-scope` to `ledger-named` (69->68, 5->6). The v2 figure is the live one; not an erratum -- a documented X-correction.

### The 31 binaries (named, not counted; never edited -- ruling (o))
28 png (the 3 art proofs, the 24 raster 1x/2x/4x of the eight themes, `docs/rasteratops/art/icon-interim-2026-10-01.png`), 2 pdf (`licenses/AETHERSX2.pdf`, `licenses/DRASTIC.pdf`), 1 gz (`docs/upstream/2026-10-15-queue-reconciliation/originals.tar.gz`).

### Information
- The `docs/reviews/briefs/` briefs are `ledger-reviews` (read-only, the other lanes'); read as information, never edited.
- `second-opinions/review-plan.json` is written in T4's Local shape (depth `local`, primary `anthropic/claude-opus-5-5`, lab `anthropic`, reviewers `[]`, `tier_exception D-WORKFLOW-184`), proved lintable at stage A (ruling (q)).

### The checkers at the dispatch tip (baseline)
`rules-check` rc 0 (30 rule files; **no evidence for the 254**); `register-check` rc 0 (**716 IDs** -- D-WORKFLOW-220, -219 and P1's -188 moved it from 713); `es-menu-map-check` rc 0 (`0 missing`); `release-catalog --check` rc 0 (99 cuts); `work-log-index --check` current; `prose-check --self-test` PASS. `ceremony-check` is `[unverified]` here (no research file for this brief runs it; what another lane owes is noted, never paid).

### The issues (§ 3 item 9), re-read at `COHASH`, states recorded
OPEN: #686, #807, #651, #685, #528, #585, #509, #511, #344, #42, #359, #360, #335, #334, #338, #947, #270, #964, #1094, #1100, #1126, #1013, #963, #273, #576, #620, #965, #682, #1216, #667, #11, #23, #134, #333, #256, #645.
CLOSED/COMPLETED: #570, #131, #507, #508, #515, #533.

## Read order

§ 2's table, the 15 groups in R5 § C stage B's order (top-level files, the
reference groups, then the read-only and ledger rows); the dispatch comment
moved nothing:

1 `README.md` (23) · 2 `TRADEMARK.md` (38) · 3 `LICENSE.md` (18) · 4 `docs/*`
(27, 9,222 lines: `council-*` 9, `save-*`/`savestate-*` 7, `cloud-*` 3,
`device-*` 2, other 6) · 5 `docs/pixelelated/` (50, 3,551) · 6
`docs/rasteratops/` (15, 4,906) · 7 `docs/releases/` (23, 1,858) · 8
`docs/ra-offline/` (2, 649) · 9 `docs/pr-series/` (2, 323) · 10 `plans/` (1,
223) · 11 `docs/upstream/` (28, 2,323) · 12 `documentation/` (16, 2,160) · 13
`licenses/` (75, 7,817) · 14 `docs/reviews/` (11, 5,101) · 15
`docs/reviews/briefs/` (1, 386). `GROUPS TOTAL 254 38598 groups 15`.

## The reader's pass

What a stranger would take from each group on its strength, before any
auditing -- read group by group from the export of the 254 at the dispatch
tip. (Depth: the lead-bearing documents were read closely; the rest at the
reader's-eye level the brief asks for -- opening sentences and structure.)

- **1-3 Top-level (`README`, `TRADEMARK`, `LICENSE`).** The front page tells a
  player this is pixelelated and sends them to a release for updates -- but to
  a release that is not published (L-02). `TRADEMARK.md` is about the name, and
  points at `LICENSE.md` for the code; `LICENSE.md` says GPL v2 in one place
  and "non-commercial use only" / "Copyright 2024 ROCKNIX" in others, and never
  states the fork's own terms (L-43). A reader cannot tell, from these three,
  what licence the fork's own work is under, nor find a working release.

- **4 `docs/*` (five families).** `council-*` (9) read as a durable record of
  the staged-council substrate and the retired Mistral counter -- a stranger
  meets a seat that is live on the page but retired in fact (L-12). `save-*`/
  `savestate-*` (7) announce their own supersession in their first lines ("Superseded
  2026-09-12 ... Kept as the record") -- honest dated records, the model to
  hold the rest to. `cloud-*`: `cloud-save-integrity.md` carries a stale M7
  order of closed issues (L-06); the changelog is a 3,581-line ledger with one
  redirecting link (L-23). `device-*`: the flashing runbook names the OS
  "ROCKNIX" throughout (L-05); the testing policy calls a decided QA-handheld
  row open (L-03) and its mask is short of the flag form (L-16). `es-menu-map.md`
  is the most-cited document (26 issues, by line) and carries three "pending"/
  "under qualification" headings for closed work (L-08, L-32); `conflict-wizard-ia.md`
  is at Rev 6 while #23 still says rev 5 (L-17).

- **5 `docs/pixelelated/`.** The rename plan is the current identity plan
  (D-WORKFLOW-144, lowercase throughout). The cloud-folder guide reads cleanly
  for `/pixelelated` but ends in internal release status (L-10); the folder-flow
  review and state table are dated contracts. The site plans name a retired
  remote in one place (L-22). The art tree (READMEs, SVGs, generator) names
  another repository's generator tool, correctly attributed (L-14) -- the 18
  art text files and 28/2/1 binaries are never edited (ruling (o)).

- **6 `docs/rasteratops/`.** Current release records -- `release-readiness.md`
  ("# pixelelated 0.0.1 release readiness") and `support-matrix.md` -- live
  under the retired-name folder (L-30, #509). The P0 sweep and its 2,419-line
  hits file are the identity baseline (`NAMING.md:30`); `cloud-layout.md`
  describes the retired `cloud_migrate_layout` in the present tense (L-04).
  Several carry the retired name as the OS's identity in dated prose (L-21).

- **7 `docs/releases/`.** `versioning.md` and `device-facts.md` are standing
  references; `device-facts.md` points at a catalog that holds none of its cuts
  (L-15). The candidate records (`next-candidate-work.md`, `-scope.md`) are
  dated readiness tables that name a superseded baseline (L-09) and run words
  into numbers (L-11). The PR stubs (`pr/01`..`pr/11`) read as finished
  PR descriptions; `rc-accept.txt` is the RC ledger (L-25, L-26). `catalog.md`
  and `rc-accept.txt` are ledger rows, never edited.

- **8 `docs/ra-offline/`.** A dated phase-1 design note (590 lines, read from
  upstream code) and a rocknix.org draft -- both present themselves as dated/
  draft, so a reader is not misled about currency.

- **9 `docs/pr-series/`.** The review guide and `map.txt` for the upstream
  series D-WORKFLOW-084 ended; `map.txt` names two deleted paths (L-27) and is
  a ledger row.

- **10 `plans/`.** The one plan, the July conflict-wizard design, superseded by
  the IA and unmarked (L-24) -- a ledger row with one historical-plan note owed.

- **11 `docs/upstream/` (read-only, #585).** The contribution queue and ten
  proxy patch drafts; `README.md` names #585 and D-WORKFLOW-165 and carries
  run-together hits (L-46, L-11's share). A reader takes these as drafts for a
  queue, which they are.

- **12 `documentation/` (read-only).** Upstream's per-device emulator tables;
  13 of 15 are behind upstream (L-41), and the one fork-own (GENERIC_X64) has
  drifted with no generator (L-31). A reader reads a table a little behind
  upstream's.

- **13 `licenses/` (read-only, #528).** 75 upstream licence texts, two PDFs;
  one (`AETHERSX2.pdf`) upstream dropped for a licensing concern (L-44). Legal
  reading is #528's.

- **14-15 `docs/reviews/` and its brief (ledger).** The renovation's own
  records -- the README/plan name files present only via the P1 stacking
  (L-01, resolved at dispatch), and carry a preliminary slice number and a
  "This file exists on next" line that `next` does not bear out (L-28, L-29).
  The coordinator's.
