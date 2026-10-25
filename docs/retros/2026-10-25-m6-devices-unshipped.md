# Mini Retro: M6.P2 T25, the devices the fork does not ship and the other projects (#672)

**Completed:** 2026-10-25
**Scope of this retro:** the T25 lane at Local depth: stages A to D (the reachability table over the 397 paths at `8ebaf8daad`), the audit issue #1102, the coordinator's dispositions, stage F's re-derivations, and the close-out to the hand-back. No stream ran.

Not retro'd here: #1101 (the inventory's unpack-edge shape, the coordinator's Backlog), the maintainer's class decision on #346, and the merge notes that carry PL-05.

**Commits:** `reviewed-at` `b27889bce2` (the dispatch tip); `fixed-at` the hand-back commit (no stream: nothing under `packages/`, `projects/` or `tools/` changed).

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** The slice is a table over files no shipped image builds, and it changed no file under `packages/`, `projects/` or `tools/`. F-01 finds one copy (`intel-ucode`) that the test image's kernel does carry, but the payload is T11's and unchanged.

## What T28 inherits

- **The drift cell read against a named upstream head:** every row states its bytes at `8ebaf8daad`, and its drift against `651150fc88` by name, never against "upstream". The newest upstream commit on the rows sits beside the drift.
- **The target-row shape:** target line, `world`, the arch pair, `BOOTLOADER` / `UBOOT_FIRMWARE` / `GRAPHIC_DRIVERS` with their `options` lines, the trees (`.dts` + `.dtsi`), the conf header beside the kernel recipe's branch version, the patch count as T43's, fork edits, files differing, and upstream commits since `--since='2026-06-01T00:00:00Z'` with the newest.
- **The dt-id erratum:** no unshipped `.dts` carries `rocknix-dt-id`. The coordinator says T28's trees carry none either, so T27's dt-id column records an absence outside H700.
- **The edge sweep:** a reach verdict cites `buildable_by` and the edges (`PKG_DEPENDS_*` including `_UNPACK`, `get_build_dir`, `get_install_dir`, `get_pkg_directory`, `get_pkg_variable`). Each edge is resolved with `config/functions:789-798`'s local-before-global order. `t25-tables.py edges` is the shape, and it fails on an unnamed reached edge.

## What worked well

- **A generator with asserted counts, writing into marked blocks.** Every table in `02` and `04` comes from `tools/t25-tables.py`, and `check` fails on a hand edit. Its own assertions caught two of my mistakes: RK3328 read as a near-name of RK3326, and the generic package count.
- **The edge sweep found what the inventory could not.** Asking *which copy does this edge resolve to?* for each edge turned up the kernel's unpack edges. `intel-ucode` is reached for the test image, and `generic-dsi` has three targets. T11's 153-entry count confirmed it from the record, with no build.
- **Recorded runners again.** Stages A, B and F each have a runner with exit codes and wall times in `runs.tsv`, so every check in `02` cites a file, not a memory.
- **T27's pointer, answered with this slice's data.** The `atf` seam was traced into RK3399's `u-boot`, and the compatible-case check was run over the 53 trees here, with H700's file as the control.

## What was harder than expected

- **Two typed figures.** I typed F-02's projects row and a sentence about the generic kernel copy beside the generator, and both were wrong. Both were caught before commit; the friction line names the guard.
- **Tool output that is not what it looks like.**
  - `pkgcheck`'s progress lines use `ESC[K`, not `ESC[2K`, so the first processed-file count read 0.
  - `\s` inside an ERE bracket is a literal `s`, so the first edge sweep matched `syslinux`.
  - Both were caught by a count that did not fit, and fixed in the committed runners.
- **The brief's disposition list did not cover the evidence.** F-01's rows needed D-WORKFLOW-209's *reached after all*, which the brief's list for this slice did not name. The register row had the words.

## What we discovered

- **The inventory's reach is plan-derived, and a plan does not list unpack-only edges** (F-01, #1101). This is the opposite direction to #1086.
- **No unshipped target carries a fork edit since the base.** The fork's one change in the 397 is a dead copy's hostname line, and its live twin is T11's.
- **Upstream is 65 commits and 39 rows ahead on the slice, 226 files across the targets.** S922X's loader moves to mainline, and T27's `atf` seam reaches RK3399.
- **The nine projects are dead by construction:** 27 `PROJECT=ROCKNIX` lines, and a search path that names one project.

## Adjustments, Instruction-Recommendations mode

These are proposals for the coordinator.

1. **Table briefs:** a reach verdict cites an edge sweep beside `buildable_by`, with the resolution order (`04` § Instruction File Recommendations).
2. **Generated tables are generated whole:** no figure typed beside the script that makes the table.
3. **Disposition lists in briefs** include D-WORKFLOW-209's *reached after all*, so a lane that finds one does not improvise the words.

## Scoped audit (the close-out's own checks)

- **AC conformance:** #672's fourteen. Twelve are met at stage F (`04` § Acceptance-criteria scorecard, updated by the artifacts since). The retro and the hand-back are this stage and the next. PASS.
- **Cornerstone spot-check:** the removal rule holds (`git diff --stat 8ebaf8daad HEAD -- packages projects` empty, f04). No upstream-carried removal is proposed (the generator asserts it). `Already written:` is answered for the one fork edit. PASS.
- **Interaction-defect scan:** `03` § 3.5's four seams, plus T27's `atf` seam through RK3399. PASS.
- **Futro prediction verification:** no futro ran. The brief's prediction of no fork-own defect held. SKIP (no futro).
- **Housekeeping:** `pkgcheck`'s whole-tree baseline is 12 FAIL and 43 WARN, all upstream's and none in the slice. Recorded, not fixed. PASS.
- **Harness self-coverage (check 7, step 5):** the generator is the slice's new harness. Its assertions covered two of the failure modes met while landing it (the near-name, the edge set). The typed-figure mode is covered by `check` once a figure is generated, which is why F-02's table moved into it. One mode stays uncovered: prose sentences in `03` and `04` are not generated, and a wrong one still needs a reader. PARTIAL, named.
- **Documentation freshness:** no new proper noun. T28's dt-id erratum is the coordinator's. PASS.
- **UI review:** no UI surface touched. SKIP.
- **Build-vs-adopt:** not applicable to a table. SKIP.
