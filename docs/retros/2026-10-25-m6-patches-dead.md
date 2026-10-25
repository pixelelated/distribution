# Mini Retro: M6.P2 T40, the patches and kernel configurations no plan applies (#687)

**Completed:** 2026-10-25
**Scope of this retro:** the T40 lane at Local depth, covering:
- stage A, the slice's 778 rows, read at `8ebaf8daad` with T23's table from its branch;
- the provenance table (`docs/audits/2026_10_25-epic-m6-patches-dead/`);
- the three bugs (#1056, #1071, #1072) and the audit issue #1074;
- the close-out.

There was no stage E: the lane removes nothing and edits no patch, configuration, recipe or tool (D-WORKFLOW-209). Not retro'd here: the coordinator's acceptance, the class decision on #346, and the fixes behind the three bugs.

**Commits:** `reviewed-at` `b8cde6f305` (the dispatch tip), `fixed-at` `9c3fa25cfb`.

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** No row is applied to an image that runs, except the four reached after all, which already are. Nothing changed, and nothing ran on a device or a guest.

## What T41, T42 and T43 inherit

- **T42 (#689) inherits 50 leads** in 26 ROCKNIX overrides (glibc 7, ffmpeg 7, bluez 7, systemd 3, ...): LibreELEC changes the live override builds without, each with its subject in `02` § The shadowed 74, and a pointing comment on #689. Also the 18 the override carries in another form (12 re-offset, 6 with the context moved), recorded so T42 does not re-ask them.
- **T41 (#688) inherits no leads,** because no kernel override is among them (a pointing comment says why). It does inherit the rule that a kernel's `PATCH_ARCH` is `TARGET_KERNEL_PATCH_ARCH`, and that the 277 generic kernel patches are dead because `get_pkg_directory linux` resolves to the ROCKNIX override everywhere.
- **T43 inherits the classes as a method:** first match in order over `unpack`'s rules, with symlinks followed. The `patches/<arch>` shape also matters there: an arch directory `unpack` never names is never read.
- **All three inherit the generator** (`tools/t40-tables.py`): it classes rows by `unpack`'s rules, reads headers, compares a shadowed patch with its override's at three strictness levels, and asserts its counts.
- **All three inherit the inventory's two reach gaps:** #1049 (`PKG_DEPENDS_UNPACK`) and #1056 (symlinked `patches`). Until both are fixed, a row the column calls unreached can be live.

## What worked well

- **Reading T23's table, not re-deriving it.** Class (d) took T23's dispositions straight from its branch with `git show`, so the two tables cannot disagree about a unit.
- **No network, by construction.** No fetch and no plan generation. The one tool that touches the recipe set (`config/options`) ran under a logging `curl` shim, and it recorded 0 calls.
- **Naming the test behind a count.** "Duplicate" gave 2, 14 and 20 depending on the test. Stating all three turned a disagreement with the brief into a finding: 18 of its 68 are carried by the override in another form.
- **The code, read for the gap.** The symlink gap is `os.path.normpath` at `selected_patch_dirs:397`, read in the tool, not inferred from the output.

## What was harder than expected

- **My own slips, each caught before it landed:**
  - the generator's first symlink test compared the target with the unit, not `unit/patches`;
  - an ad-hoc changed-lines count (23) that the generator's tiers superseded;
  - one table label (*20 overrides* for 19);
  - a typed heading time.
- **Class (c) is two bugs, not a rename.** vitaquake2-lr's recipe passes `platform=` only on aarch64, and EmulationStation's patch carries a slip that would ship the day it applies.

## What we discovered

- **No recipe in the tree has a `patches/x86/` directory,** the name `unpack` gives x86_64. The only x86 directories are the five `patches/x86_64` that are never read.
- **gcc's and cmake's overrides apply the generic patches** through symlinked `patches`, every image, while the inventory reads them unreached (#1056).
- **The dead patch set churns with LibreELEC.** 99 of the 102 commits since June came through ROCKNIX's LibreELEC merges, and none is the fork's.

## Adjustments, Instruction-Recommendations mode

These are proposals for the coordinator.

1. **`packaging-and-patches.md`:** an x86_64 patch directory is `patches/x86`. A `patches/x86_64` directory is never read (`unpack:127-128`).
2. **For reachability work:** follow symlinked `patches` directories (#1056's shape).
3. **For any "duplicate" or "same patch" claim:** name the test and its count.

## Scoped audit (the close-out's own checks)

- **The lint:** `PASS` in the pre-issue and resolution phases and with `--issue 1074`.
- **The tables:** 778 coverage rows, 778 provenance rows and 74 shadowed rows; the dispositions sum to 778 rows and 317,908 lines.
- **The review plan** is local, `reviewers: []`, with no provenance file.
- **#1074:** 6 items, each at an outcome (#1071 and #1072, #1056, #689, #346, and two recorded at `b1c39c49d4`). `box-check` 0 fail on #1056, #1071, #1072 and #1074.
- **Nothing changed** under `packages/`, `projects/` or `tools/` from the dispatch tip, and `packages/` and `projects/` equal `8ebaf8daad`.
- **No network and no plan generation:** 0 `curl` calls in stage A and stage F.
