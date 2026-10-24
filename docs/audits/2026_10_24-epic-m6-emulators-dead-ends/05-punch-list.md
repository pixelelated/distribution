# Punch List — M6.P2 T24, emulator recipes and files no shipped image builds

**Local depth** (plan § 6c, D-WORKFLOW-184): no reviewer; Phase 4.5 is in `04`. Three items, all Low and all `Renovation`; no `bug`.
- **PL-01** is the #585 proposal for the 81 LibreELEC files: one item, whose outcome is the coordinator's post.
- **PL-02** is the five ROCKNIX recipes, said once with T3 cited.
- **PL-03** is the one finding outside the 86, in a fork-own line of T3's file.

Nothing in this list deletes, moves or edits a file under `packages/` or `projects/`. The outcomes are open until the coordinator's dispositions after the stage-D pause.

---

## PL-01: the 81 LibreELEC files under `packages/emulation/`, which nothing builds, come back with every merge of LibreELEC master (the #585 proposal)

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-01
- **Owner area:** upstream's: LibreELEC's recipe set, carried by ROCKNIX's merges of LibreELEC master and by our base merge
- **What:** Keep every file (brief § 2). The coordinator posts one proposal to ROCKNIX on #585, in this shape:
  - ROCKNIX carries LibreELEC's `packages/emulation/` (Kodi's RetroPlayer cores), which no ROCKNIX configuration builds:
    - **81 files, 2,258 lines, 86,663 bytes**: 77 `libretro-*` cores, `cyclone68000`, `libretro-common`, and `rcheevos` with its cmake file;
    - with the 16 patch files beside them, **97 files and 106,103 bytes**.
  - Their only build edges are 79 lines in the 78 Kodi `game.libretro*` addon recipes, which are unreached too.
  - LibreELEC master already differs from the carried copy in **67 of the 80 recipes** (61 version-stamp hunks, 6 moved pins), so each import re-touches them.
  - **67 of the 77 cores have a ROCKNIX `*-lr` twin** (52 by name and source, 5 by name, 10 by source; 12 at the same pin).
  - **10 have none**: `libretro-2048`, `-beetle-bsnes`, `-blastem`, `-bnes`, `-cannonball`, `-dinothawr`, `-dosbox`, `-mame2000`, `-mrboom`, `-nx`.
  - `pkgcheck` passes all 80, with 2 WARN lines (`libretro-beetle-pcfx:24`, `libretro-bsnes-hd:19`).
  - The fork removes nothing until ROCKNIX decides.
- **Where:** `04-analysis.md` § Q6 (the 81 rows), § Q7 (the twin map), § Q5 (the weight)
- **Evidence:** P1, P2, P4 to P9, P12 to P14, P16
- **Can this be done on the VM?** No: these are files no image carries; the tree, the record and the API show it (brief § 5)
- **Already written:** nothing: no ROCKNIX or fork configuration builds them, there is no build directory in the five roots, and Kodi ships in no image. Every row of `04` § Q6 says so.
- **Acceptance:** #585 carries the proposal with these counts and a link to `04` § Q6 and § Q7; `git diff --diff-filter=DR --name-only 8ebaf8daad <fixed-at> -- packages/emulation` is empty.
- **Disposition note:** deferred:#585 at Phase 7, the coordinator's post

## PL-02: the five ROCKNIX recipes no shipped device builds

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-02
- **Owner area:** upstream's: ROCKNIX's `projects/ROCKNIX/packages/emulators/libretro/`
- **What:** Keep all five (brief § 2), and say their standing once, citing T3's `04` § Q6 at `b3cb4ec8c5`.
  - **`boom3-lr` and `vitaquake3-lr`** are built only by `idtech-lr`'s `x86_64` arm (`idtech-lr/package.mk:20-22`), so only ROCKNIX's AMD64 image builds them.
  - **`mame2003-lr`, `panda3ds-lr` and `play-lr`** have no build edge from any file, so no ROCKNIX configuration builds them. `play-lr` left the metapackage in upstream's `20b7d7ea02` (2025-10-26), and the other two are named nowhere since the import `9f1fab30f6`.

  The three are a line for the #585 proposal: recipes dead in ROCKNIX itself.
- **Where:** `04-analysis.md` § Q6, the five `projects/` rows
- **Evidence:** P6 to P10, P17
- **Can this be done on the VM?** No: no shipped image holds them (P10)
- **Already written:** no fork image carries their `.so`. `core-info` ships their `.info` files, read only. Every image's `core-pins` names `boom3-lr` and `vitaquake3-lr` (PL-03). Nothing reaches `/storage` or a cloud. ROCKNIX's AMD64 image builds two of them, and pixelelated ships no AMD64 image (T3's `04` § Q6 at `b3cb4ec8c5`).
- **Acceptance:** the five rows of `04` § Q6 read `kept: upstream's; no shipped device builds it`; `git diff --name-only 8ebaf8daad <fixed-at> -- projects/ROCKNIX/packages/emulators/libretro` is empty; the three named in the #585 proposal, if the coordinator takes them there.
- **Disposition note:** the coordinator's: `deferred:#585` with PL-01, or `withdrawn` as said once and kept

## PL-03: every shipped image's `core-pins` names two cores the image does not hold

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-03
- **Owner area:** fork-own, outside this slice: `projects/ROCKNIX/packages/virtual/emulators/package.mk:1768` (T3's file, accepted; fork commit `3a56a04f8b`, #21)
- **What:** `IDTECH_CORES` lists `boom3-lr` and `vitaquake3-lr` on every device, while `idtech-lr` builds them on `x86_64` only. So the `core-pins` of GENERIC_X64, H700 and SM8550 each carry a row for both, and no image holds either `.so` (P10, P11). The one reader, `cloud_capture:121`, looks up the core that ran, so there is no failure, only a table that lists more than the image holds.
  - **The proposed fix**, if the coordinator routes one: add the two names under the same `TARGET_ARCH = x86_64` condition `idtech-lr` uses, and check that `idtech-lr` itself is built (GENERIC_X64 skips it).
  - **Its proof:** the three `core-pins` read from the next image, with the two rows gone where the `.so` is absent.
- **Where:** `virtual/emulators/package.mk:1768`; the three install trees' `/usr/share/rocknix/core-pins`
- **Evidence:** P7, P10, P11
- **Can this be done on the VM?** Yes, for a fix: the GENERIC_X64 image's `core-pins`, read on the guest or from its install tree. The finding itself is a read of three install trees.
- **Already written:** two rows in a read-only image file (`/usr/share/rocknix/core-pins`). No save manifest names either core, because `cloud_capture` writes the pin of the core that ran. Nothing under `/storage` or in a cloud. A fix changes only the next image's file.
- **Acceptance:** the coordinator's disposition, either a stream on T3's file with the three `core-pins` read back after the next image, or `withdrawn` as harmless with the reason.
- **Disposition note:** the coordinator's

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-01"
  owner_area: "upstream's: `packages/emulation/` (LibreELEC's, via the base merge)"
  tracked: "#585"
  outcome: "open"
- id: PL-02
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-02"
  owner_area: "upstream's: `projects/ROCKNIX/packages/emulators/libretro/` (five recipes)"
  outcome: "open"
- id: PL-03
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-03"
  owner_area: "fork-own, outside the slice: `virtual/emulators/package.mk:1768` (T3's file)"
  outcome: "open"
```

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | awaiting the coordinator's #585 post |
| PL-02 | Open | awaiting the coordinator's disposition |
| PL-03 | Open | awaiting the coordinator's disposition |
