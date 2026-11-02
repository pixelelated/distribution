# Retrospective audit -- M6.P2 T39, the reference documents (#686)

Phase 3 over the 254 (Local depth; brief § 6's `03` row): § 3.1 to § 3.4, then
§ 3.5's interaction audit for the seams § 2 names, then the doctrine futro's
predictions checked. **reviewed-at** `86ebb6dffc`. Every figure is a command's line at
that hash or at the lane's tip `2d09ed5c4d` (the 254's bytes are the same at both;
the removal check is empty). Counts are by `/usr/bin/grep` under `LC_ALL=C`.
Written at the stage-B completion (#686, issuecomment-6565986529).

## 3.1 Architectural coherence

The 254 are the doctrine area's `rest` (no glob of their own), and they fall into the
classes of ruling (a)'s carve (`stage-a/membership-block-2.txt`; `CARVE` lines in `01`
§ Scope):

- **69 reference documents proper:** `edit-scope` 68, plus `TRADEMARK.md` as
  `edit-under-naming` 1.
- **20 ledger rows:** 12 under `docs/reviews/`, 6 named ledgers and the plan.
- **31 binaries**, tabled.
- **18 art text files**, never edited.
- **117 read-only rows:** 88 upstream-carried, 27 of #585's, `LICENSE.md` for #528,
  and the GENERIC_X64 table.

The documents have no common structure, and need none, since each serves its own
reader. What they share is one convention, a dated record carrying its date, and it is
kept unevenly:

- Kept: `docs/rules-sweep-2026-09-12.md`, `docs/ra-offline/2026_09_13-phase-1-design-note.md`
  and `docs/save-manifest-alignment-review.md` carry the date in the name or the
  title.
- Not kept: `docs/cloud-save-integrity.md` and `docs/releases/next-candidate-work.md`
  carry dated status in their opening lines without saying they are dated (L-06, L-09).

The heavy documents mix two kinds of text:

- `docs/es-menu-map.md` holds a reference (the menu tree) and a journal (`:711` to the
  end, 279 lines under 16 headings; L-08).
- `docs/rasteratops/release-readiness.md` holds a current status table and dated review
  baselines (`:836`, `:857`, `:871`).

That mix is the structural cause of the *record presenting itself as current* family.

## 3.2 Project conformance

- **`NAMING.md`.** pixelelated is lowercase everywhere: `Pixelelated`/`PIXELELATED`
  is 0 over the 223. Every capitalised `Rasteratops` line (27) and every
  `maxengel/rocknix` line (28) is either:
  - the character;
  - a historical record (`docs/rasteratops/**`, the changelog, the P0 sweep);
  - provenance (the rename plan, the art system's origin, #585's identity draft);
  - one of four findings: L-21 is recorded as a ledger row; L-22 is a fix candidate;
    L-23 is a ledger row; L-25 is inherited.

  `t39-checks.sh`'s identity step (stage C) holds this line by line. The one document
  that names the OS wrongly throughout is the flashing runbook (L-05: `ROCKNIX` 21,
  `pixelelated` 0), which `CLAUDE.md`, `AGENTS.md` and `device-builds.md` all send a
  flasher to.
- **`es-player-text.md`.** `docs/backup-contents.md:3-4` names two labels in the banned
  words *configurations* and *everything*. It calls itself the source of truth for the
  user-facing docs (L-07).
- **D-UI-039.** The map's tree passes `es-menu-map-check` (`55 screen(s) at
  16dbac521, 31 in the map, 24 declared unmapped, 0 missing`). Its journal headings
  call closed work pending (L-08). The checker cannot see this: it reads titles only
  (`es-ui-style-guide.md:59`).
- **`decision-register.md`.**
  - Citations resolve: the 223 cite 442 distinct IDs, 0 unresolved, against 716 rows.
  - No cited ID is a reversed row read as live, with three exceptions. D-QA-016 is
    called open after it was decided (L-03). D-CLOUD-175 retired the migration script
    two documents still describe (L-04). D-WORKFLOW-084 ended the series that
    `map.txt` and seven rows describe (L-34).
- **`fork-workflow.md`.** `docs/` and `plans/` are personal paths, refused only on
  `pr/*`. No reference document is on a `pr/*` path. `docs/pr-series/map.txt` is a
  live input to `tools/pr-stack-check` (`:9`, `:40`) for a series D-WORKFLOW-084 closed
  (L-27, L-34).

## 3.3 Spec fidelity

The specification here is the brief's § 3 table (46 leads) and the rulings (a) to (q).

**Every lead's FAIL-first check printed its defect at the tip** (`02` § The table).
None was withdrawn at stage B.

**Each fix candidate's `git log -S` shows the sentence written before the change that
made it untrue, or the change not reaching it.** No guard keeps any of them on purpose:

| Lead | Written | Made untrue by | Last edit to the file |
| --- | --- | --- | --- |
| L-02 | `3d7c075f63` 2026-10-02 | no pixelelated release exists; #344 OPEN | `a9af618398` 2026-10-04 |
| L-03 | `e15ed2da63` 2026-09-11 | D-QA-016 decided 2026-09-13; #131 CLOSED 2026-09-20 | `3c31e2aa18` 2026-10-15 |
| L-04 | `f8816b4dc9` 2026-10-02 (`cloud-layout.md`), `826d52e395` 2026-09-29 (`08-saves.md`) | D-CLOUD-175 | `9bb2b42e5a` 2026-10-05; `826d52e395` |
| L-05 | `20303f67d7` 2026-09-06 | D-WORKFLOW-144 | `f7152d84a4` 2026-09-20 |
| L-06 | `1bd4554dc8` 2026-10-08 | #515, #507, #508 closed the same day | `1bd4554dc8` |
| L-07 | `aeb6ada34d` 2026-08-19 | the labels renamed at the pin `16dbac5211` | `5ca1427ab5` 2026-09-12 |
| L-08 | `7484a2b46d`, `0ea6eaf74a` 2026-10-13; `5176e20c6c` 2026-10-14 | #570 CLOSED 2026-10-14 23:41 | `060dbde841` 2026-10-16 |
| L-09 | `899857b591` 2026-10-14 | the 2026-10-16 transfer to `077197` | `8ebaf8daad` 2026-10-17 |
| L-10 | `a9af618398` 2026-10-04 | #508 CLOSED 2026-10-08 | `357d88010a` 2026-10-07 |
| L-12 | `5f1b343d25` 2026-09-30 | scaffold#915 (the Mistral seat outside every run profile) | `5f1b343d25` |
| L-15 | `83acc0921f` 2026-09-25 | the catalog's last regeneration `3d7c075f63` 2026-10-02 | `fb932eb1fe` 2026-10-16 |
| L-16 | `6075c64f2e` 2026-09-12 | `engineering-practices.md`'s widened mask (2026-10-30) | `3c31e2aa18` 2026-10-15 |
| L-22 | `90f9e0eafd` 2026-10-07 | #511 (open) | `62c382f467` 2026-10-15 |

Four of these were last edited after the change that made them untrue, without the
sentence being touched: L-03, L-08, L-09 and L-15. That is the brief's drift shape: a
second copy, or a status line, drifts from the first edit on (blindspot `:684-685`).

The R3 C24 parenthetical (`tools` 0) is wrong at the tip (`tools/` 127). The
coordinator ruled it the brief's erratum (#686, 00:12 UTC). L-04 stands.

## 3.4 Platform conformance

No path of the 254 reaches an image (reach `n/a` for all 254). **Neither time-to-play
number moves.** A document claiming a guest behaviour would be checked against the
tool's options and `docs/vm-qa-log.md`, and recorded `[unverified]` (brief § 5 rule 3).
The reader's pass found none whose truth needs a guest. A handheld fact a document
claims is read against `docs/releases/device-facts.md`, never tested; L-05 and L-15 are
the two places this matters.

## 3.5 Cross-system interaction audit

### Interaction: the documents x the rules that cite them

Rules, `CLAUDE.md` and `AGENTS.md` name 18 of the 254 (`git grep -l -F <path>
86ebb6dffc -- .claude/rules CLAUDE.md AGENTS.md`, per path).

| Document | Rule files naming it | Finding in it |
| --- | ---: | --- |
| `README.md` | 7 | L-02 |
| `docs/es-menu-map.md` | 6 | L-08, L-32 |
| `docs/vm-qa-log.md` | 5 | -- (ledger row) |
| `docs/device-testing-policy.md` | 5 | L-03, L-16; L-36's third document |
| `docs/conflict-wizard-ia.md` | 4 | L-17 |
| `docs/device-flashing-runbook.md` | 3 | L-05 |
| `docs/cloud-sync-changelog.md` | 3 | L-23 (ledger row) |
| `docs/releases/versioning.md` | 2 | L-39 |
| `docs/releases/device-facts.md` | 2 | L-15 |
| `docs/pixelelated/rename-plan.md` | 2 | -- |
| `docs/cloud-save-integrity.md` | 2 | L-06 |
| 7 more, one rule each | 1 | L-31 (GENERIC_X64 table), L-46 (`docs/upstream/README.md`), L-01, L-25/L-26, L-15's catalog, L-27 |

**The seam's finding.** The documents the rules send every session to carry the most
findings: 7 of the 11 most-cited documents have a fix candidate. A defect in
`README.md`, `device-testing-policy.md`, the map or the runbook is read by every agent
the rules route there. That is why L-02, L-03, L-05, L-08 and L-16 lead the punch list,
whatever their size.

The rule side of this seam is T4's (#651), and the brief keeps it so:
- L-35: `handheld-evidence.md`'s `docs/**` glob loads a device rule for every one of
  the 223 text rows under `docs/`.
- L-36: two documents, or three, that load nowhere.

Both are inherited by the coordinator.

### Interaction: the documents x the tools that read three of them

| Ledger row | Read by | What a hand edit would do |
| --- | --- | --- |
| `docs/pr-series/map.txt` | `tools/pr-stack-check:9`, `:40` | changes what the series builder stacks; two of its paths are deleted (L-27) |
| `docs/releases/rc-accept.txt` | `tools/rc-preflight:56` | changes which RC exceptions pass preflight (L-25, L-26) |
| `docs/releases/catalog.md` | `tools/release-catalog:9`, `:27`, `:98` (writer); `tools/rc-preflight:390` | breaks `--check`, which compares the page with the `RECORD.txt` files present (L-15's catalog half) |

All three are ledger rows under ruling (a), never edited here. `t39-checks.sh`'s
`untouched` and `generated` steps (stage C) hold them. The catalog's
`release-catalog: current (99 cuts)` is current against this host's `RECORD.txt`
files, and still holds none of the four cuts `device-facts.md` names (L-15, #964).
Being current against the records present is not being current against the cuts made.

### Interaction: the documents x the issues that cite their lines

| Issue | Cites | The line at the tip | Holds? |
| --- | --- | --- | --- |
| #1100 | `device-facts.md` L17-L19 | `:17` SM8550 boot on the Retroid Pocket Nova; `:18` Nova frontend readiness after #529; `:19` Nova shutdown and bootloader recovery | the three Nova rows are still there |
| #1126 | `device-facts.md` line 31 | `:31` Retroid Pocket Nova: the stick LEDs | still there |
| #682 | `es-menu-map.md:134` | `:134` the CONTROLLER & BLUETOOTH row | still there |
| #1216 | `es-menu-map.md:405`, *"reading FINISH RESTORE PROCESS"* | `:405` `### FINISH RESTORE SETUP (the checklist after a settings restore)` | **the line holds the page, the issue's quoted label does not**: the map says SETUP where #1216 reads PROCESS -- the interface lanes' (L-32) |
| #667 | `es-menu-map.md:595` | `:595` the SCAN GAMES FOR OFFLINE ACHIEVEMENTS node | still there |
| #576, #620 | `docs/graphics-memory-testing.md` | absent from every tree here (L-33) | no |

Any stage-E edit to `device-facts.md` (L-15) or `es-menu-map.md` (L-08) records these
lines before and after (brief § 5).

### Interaction: the reference set x upstream's copies

- **The 90 upstream-carried rows are byte-identical to the merge base `c445081a59`.** 76
  are identical to `upstream/next` `651150fc88`, 13 `documentation/` tables differ, and
  `licenses/AETHERSX2.pdf` is absent upstream (R1 C12; stage B's run: `15 files
  changed` over `documentation/` and `licenses/`).
- **Since the merge base, upstream:**
  - regenerated `SUPPORTED_EMULATORS_AND_CORES` three times (L-41);
  - deleted `licenses/AETHERSX2.pdf` for a licensing concern (L-44, `c4d353449e`).

  The fork has taken neither. Both belong to the next upstream base merge, or to #528
  for the PDF, never to this slice.
- **The fork's own GENERIC_X64 table has no generator** and has not changed since
  2026-08-21 (L-31, ruling (j)).

### The doctrine futro's predictions, checked

The T39 kickoff addendum (`docs/futros/2026-10-24-m6-doctrine.md:488`) lists what an
Opus lane with only the brief might do wrong:

| Prediction | What happened |
| --- | --- |
| edits `licenses/` text it finds stale | did not; read-only, `untouched` step |
| rewrites a `docs/reviews/` page | did not; ledger rows tabled (`02` § The ledgers) |
| regenerates the catalog with `--write` | did not; `--check` only |
| "fixes" every Rasteratops hit | did not; every hit classed (character, historical, provenance, interim-name, or a lead) |
| deletes `plans/` | did not; one historical-plan row (L-24) |
| treats a crude probe's dead paths as findings | **nearly**: stage B's first dead-link scan resolved against the 254-only export and read 417 dead; resolved against the worktree it read 0. Corrected in `00` before the checkpoint. The stage-C `paths` and `tools` steps class each dead path, line by line, in the allowlists |
| corrects `map.txt` | did not; inherited (L-27) |
| restructures the map's journal | did not; § 4 question 1 |
| edits an art SVG | did not; `binaries` step |
| runs the split under `LC_ALL=C` | did not; `en_US.UTF-8`, compared as a set (X01) |
| reads `UNRESOLVED D-WORKFLOW-188` as a defect | did not; it resolves at the tip (P1's row carried in) |
| writes a host-file START line | did not; 0 lines matching `T39\|#686` from this lane |
| posts the maintainer questions on #807 or #346 | not yet reached (stage D, on #686) |

**What the futro did not predict, and happened:**
- **A case-sensitive read of #807's body called a present erratum absent** (stage A,
  L-37). The coordinator settled it at 06:43 UTC.
- **The brief's own evidence line was wrong** (R3 C24's `tools` 0).
- **Stage B's checkpoint omitted four artifacts of its own list.** These are `03`,
  `04`, `stage-a/` and `stage-b/`. The lane named them on resume and the coordinator
  corrected the acceptance.

All three are the same lesson in different places. *Verify the artifact, not the
report* applies to the lane's own probes and the lane's own checkpoint, as much as to
the documents.
