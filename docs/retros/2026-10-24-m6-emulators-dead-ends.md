# Mini Retro: M6.P2 T24, the emulator recipes and files no shipped image builds (#671)

**Completed:** 2026-10-24

**Scope of this retro:** the T24 lane, from stage A (13:38 UTC) to stage G:
- the dispatch on #671 (issuecomment-6384884754);
- the audit in `docs/audits/2026_10_24-epic-m6-emulators-dead-ends/`;
- the punch-list issue #900;
- the coordinator's stage-E dispositions (issuecomment-6385217441: no streams).

Not retro'd here, because they are not this lane's: the #585 proposal (the coordinator's post), the #857/#873 integration packet that carries PL-03's fix, and the merge.

**Branch:** `feature/m6-emulators-dead-ends-671`. `reviewed-at` and `fixed-at` are both `81331b499e`: the slice changed nothing under `packages/` or `projects/`.

**Delta:**
- **Code:** none. `git diff --stat 8ebaf8daad 81331b499e -- packages projects` and the same from `8ebaf8daad` to the tip are empty, as are `--diff-filter=DR`.
- **Records:** the audit folder holds `00` to `05`, a Local `review-plan.json`, and three tools: `t24-tables.py`, `t24-twin.py`, and `tick-checkboxes.py` (copied from T30's `a020b3d375`).
- **The table:** 86 rows, all unreached by any shipped image, all `kept: upstream's`, each with an `Already written:` line. The twin map has 77 rows. There are 22 proofs.
- **The punch list:** 3 items, all Low and `Renovation`, all deferred:
  - PL-01 and PL-02 to #585;
  - PL-03 to the #857/#873 packet, as `fix-pending-image`.
- **Bugs:** none filed; none found.
- **Network:** 90 LibreELEC contents-API reads (80 at stage B, 10 at stage F), and 85 HEAD probes plus 3 controls. No archive was downloaded, no remote added, no process started in an M7 worktree.

## What the slice did to the two time-to-play numbers

**The slice did nothing to the two time-to-play numbers.** Interface to first frame and game to game are untouched. Nothing under `packages/` or `projects/` changed, and none of the 86 paths is built into any image, so none is on a launch or exit path. Nothing was measured, because there was nothing to measure.

## What worked well

- **Every zero had a control beside it, read four ways.** `snes9x-lr` was the control for each read: it appeared in the plans (3 narrow, 6 wide), in the metapackage (2 lines), in the build edges, and as a build directory in three roots. So each `0` for the 85 recipes is a read that could have said "reached". T6's adjustment ("read a reachability zero a second way") was applied twice over: a wider plan column, and a bare-prefix second match on the record.
- **Generated tables, asserted.** `t24-tables.py` writes the 86-row coverage table, the 86-row Q6 table and the 77-row twin map from the § 5 outputs. It asserts each count and refuses an empty cell. Moving `twin.py` into `tools/` and fixing its duplicates was checked by regenerating all three tables byte-identical (`cmp`). The coordinator's acceptance re-runs one script, not a hand edit.
- **The controls found the method's limits before a row claimed too much.** Two examples:
  - A HEAD probe of an archive at a nonexistent commit answers 302, so Q3 says "the repository answers", not "the pin exists" (P15).
  - `pkgcheck`'s PASS was shown able to fail (a late-binding fixture fails both copies), and each name was shown to match exactly one recipe (T6's F-02).
- **Citing T3, not re-deriving it.** The five ROCKNIX recipes' project pins came from T3's `04-analysis.md` rows at `b3cb4ec8c5` (P17), which saved 15 API reads and kept one answer in one place.

## What was harder than expected

- **A brief block run line by line lost its `mkdir`.** I ran § 5's commands one at a time and left out the block's first line. The LibreELEC loop's `2>.qa-scratch/t24/le/err` then failed on every row, and bash ran no `gh`. The loop failed closed: 80 rows of `not-read`, none `identical`. It cost one minute (friction line 13:57). This is the second time in the area that a redirect into a scratch path that did not exist broke a run: T6's fixture failed on its own stderr file under a relative path.
- **I wrote a table from memory and had to replace it.** `03`'s first table of "the futro's A1 to A6" was filled from what brief version 2 carries, as if A1 to A6 were the errata. The addendum's A1 to A6 are adjustments. I caught it before commit by reading the futro (`docs/futros/2026-10-24-m6-emulators-and-cores.md:489-582`), and `04` § Quality Self-Check records it. This is the same shape as the typed times of T3, T6 and T30: a claim produced from recall, not from the artifact.
- **Several sentences said more than their read.** All were narrowed before commit:
  - "79 Kodi recipes" was 79 edges from 78 recipes;
  - "a substring search finds none" was false: it finds other cores;
  - "every core vendors its own `libretro-common`" was a generalisation that P8 does not show.
- **`upstream/next` moved during the first fetch** (to `481c9d0d75`, heroic). It cost nothing, because the (a) loop ran at both heads. It is still the moving-base class plan § 8 names.

## What we discovered

- **The 81 come back changed with every import.** LibreELEC master differs from our copy in 67 of the 80 recipes:
  - 61 by version-stamp hunks that only add lines;
  - 6 by moved pins, including `rcheevos` from 9.2.0 to 12.5.0.

  ROCKNIX's next import of LibreELEC master rewrites them, and our base merge after that carries the diff. That is now on #585.
- **Three ROCKNIX recipes are dead in ROCKNIX itself:** `mame2003-lr`, `panda3ds-lr` and `play-lr` have no build edge from any file. `play-lr` left the metapackage in upstream's `20b7d7ea02`.
- **`core-pins` lists two cores no image holds.** The fork's `IDTECH_CORES` (`virtual/emulators/package.mk:1768`, `3a56a04f8b`) names `boom3-lr` and `vitaquake3-lr` on every device, so every shipped image's `/usr/share/rocknix/core-pins` carries rows for cores whose `.so` is absent. It is harmless, but it is a record that overstates (PL-03, to the #857 packet). T3's `Already written:` for the five said "only the `.info` files"; this is the second trace.
- **10 of LibreELEC's 77 cores have no ROCKNIX twin at all**, and 12 twins sit at LibreELEC's exact pin. The #585 post names both as worth a second look.

## Adjustments for the next lane

These are proposals for the coordinator. This lane edits no rule, brief template or skill (D-WORKFLOW-189).
1. **A loop makes the folder it writes into.** This is the second instance (T6, T24) of a redirect into a scratch path that does not exist. Proposed for the brief template's § 5 shape: every loop that writes under `.qa-scratch/<lane>/<dir>/` starts with its own `mkdir -p`, or the block is marked "run whole". On the rule of three, the next instance moves it to a tool.
2. **A HEAD probe of a GitHub archive does not prove the pin.** Proposed for plan § 6b's stage-E list, after T7's mirror line: a probe without `-L` answers 302 for a nonexistent commit. A pin is settled by `commits/<pin>` through the API (T3's `q4-pins.py`) or a HEAD on the redirect target.
3. **A table about another document is filled from that document.** The futro table slip is the recall shape again. Proposed: a criterion entry that cites a document names its line range, as `03` now does, so the table cannot be written before the read.
4. **`tick-checkboxes.py` to `tools/`.** T30's adjustment 2 stands, and the tool has now been copied a second time.

## Scoped audit (Step 2.5)

- **AC conformance:** PASS for this stage. #671's criteria 1, 3 and 6 to 12 are met with their artifacts (`04` § Acceptance-criteria scorecard; criterion 11 at 22 = 22). Criterion 4 is met by `05` § Phase 7 (three Deferred rows with links). Criteria 2, 5, 13 and 14 are met at stage H (this retro is 13). `renovation-status` reading `closed` follows the coordinator's close and merge.
- **Cornerstone spot-check:** PASS.
  - No upstream-carried file is changed (brief § 2; D-UI-079).
  - Every row answers *Already written* (`upgrade-and-install.md`).
  - Nothing is deleted, though the duplicate test was asked of each row (`engineering-practices.md`).
  - Nothing went outward from the lane (D-WORKFLOW-165).
  - Every `gh` call carried `--repo pixelelated/distribution` or a repository path.
- **Interaction-defect scan:** PASS. `03` § 3.5 reads four seams: the base merge × the 81, the twins × the 77, T40's patches × the 12, and `core-pins` × `idtech-lr`'s arm. The last is PL-03.
- **Futro prediction verification:**
  - The addendum's four unknowns were all answered (U-1 to U-4).
  - Its seven simulated mistakes (S-1 to S-7) did not happen.
  - Its six adjustments were all done.
  - Its figures, after the errata, held with no delta.
  - It missed three things: the `core-pins` rows, the probe's blindness to a dead commit, and the 61 identical-pin files master has rewritten.
- **Housekeeping (the checkers):** PASS: `register-check`, `work-log-index --check`, `rules-check --quiet`, `forbidden-terms-check`, `.githooks/hooks-test` and the full lint, with their exit codes in the hand-back. `ceremony-check` rc 1 is the W42 summary only, which is M7's.
- **UI review:** SKIP: no UI surface touched.
- **Harness self-coverage:** PASS. `t24-tables.py` refuses a wrong row count and an empty cell. `tick-checkboxes.py` refuses an empty body or a change beyond the named lines, and read #900's body back equal.
- **Documentation and glossary freshness:** SKIP. No new proper noun, and no document made stale.
- **Build-vs-adopt:** SKIP. No build-vs-adopt answer was recorded for a table slice.

## Practice adjustments

- The skill's Step 1 harvest ("read the prior 3–5 retros") is what found adjustment 1's second instance in T6's retro. Without it, the `mkdir` slip reads as a one-off.

## Code-verifiable state

| Artifact | Path | Check |
| --- | --- | --- |
| the reachability table | `04-analysis.md` § Q6 | 86 rows, 86 `Already written:` |
| the twin map | `04-analysis.md` § Q7 | 77 rows |
| the coverage table | `02-forward-audit.md` | `grep -c -E '^\| `(packages\|projects)/'` = 86 |
| the proofs | `02` and `00` | 22 = 22 |
| the punch list | `05-punch-list.md`, #900 | 3 Deferred; #900's 3 checkboxes ticked |
| no change | `git diff --stat 8ebaf8daad 81331b499e -- packages projects` | empty |

---

**T24 code-complete, with no code. Next is the hand-back on #671 (stage H). The coordinator accepts by brief § 10 on an export of the tip.**
