# Punch list — M6.P2 T25, the devices the fork does not ship and the other projects (#672)

**Local depth** (plan § 6c, D-WORKFLOW-184): no reviewer; Phase 4.5 is in `04`. Five items, no `bug`:
- **PL-01** (Low) is the one finding that changes the record: the inventory's reach misses the kernel's unpack edges. A lead for the coordinator.
- **PL-02** is the #346 class proposal, one `Renovation` item whose outcome names the coordinator's post.
- **PL-03** is the first widening, held.
- **PL-04** is the fork-own dead-copy row.
- **PL-05** is the drift the next base merge brings.

Nothing in this list deletes, moves or edits a file under `packages/` or `projects/`, and no item proposes a removal of an upstream-carried unit (D-WORKFLOW-209). No stream is expected: nothing here changes.

---

## PL-01: the inventory's plan-derived reach cannot see the kernel's unpack edges (`intel-ucode`, `generic-dsi`)

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-01
- **Owner area:** fork-own tool, outside the slice: `tools/renovation-inventory` (P1's), whose `buildable_by` comes from plan steps
- **What:** `projects/ROCKNIX/packages/linux/package.mk` takes two of the slice's recipes by edges a build plan does not list.
  - `:69-72` puts `intel-ucode` in `PKG_DEPENDS_UNPACK` on any x86 `TARGET_ARCH`, and `:202` copies its build dir into the kernel's `CONFIG_EXTRA_FIRMWARE`. `config/functions:789-798` resolves AMD64's device copy and, for GENERIC_X64, the generic `packages/linux-firmware/intel-ucode`. T11 counted 153 `intel-ucode` entries in the guest kernel (`ed8c48f3cd`, its `02:142`).
  - `:81-82` unpacks `generic-dsi` for RK3326 and RK3566, and `:108-111` compiles its source for RK3326, RK3566 and RK3576.
  - The inventory reads all four `intel-ucode` rows as `unreached` (`buildable_by []`) and lists `generic-dsi` for RK3326 alone.
  - This table corrects its own dispositions: the generic pair *reached after all*, AMD64's pair `unshipped`, `generic-dsi`'s three targets. That leaves the dead class at 203. The tool is not changed here (brief § 4, the ladder).
  - The shape runs the opposite direction to #1086's (#1086 reads reached where nothing reads).
- **Where:** `02` F-01, § The edges; `04` § Q6
- **Evidence:** P13, P14
- **Can this be done on the VM?** Yes, for the payload: T11's guest kernel already shows the 153 entries. The reach verdict itself is a tree read.
- **Already written:** nothing: the inventory is regenerated, not migrated, and no image changes.
- **Acceptance:** the coordinator files or names the issue that owns the shape (#1086 or a new one), and that issue cites `02` F-01's four rows and `generic-dsi`'s two missing targets; this table's dispositions read `reached after all` and `unshipped: target AMD64` for the four (`tools/t25-tables.py counts` prints `dead 203 reached after all 2 shadowed 9 unshipped 183 total 397`).
- **Disposition note:** open

## PL-02: 203 dead upstream-carried rows, put to the maintainer as one class (the #346 proposal)

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-02
- **Owner area:** upstream's: LibreELEC's other hardware families and DVB addons, carried by our base merge
- **What:** Keep every file (D-WORKFLOW-209). The text the lane proposes, for the coordinator to post on #346:
  - The fork carries 203 files that no image we build, ship or test can reach: **5,471 lines, 301,712 bytes**.
    - **172** are the nine LibreELEC hardware projects (ARM, Allwinner, Amlogic, Generic, NXP, Qualcomm, RPi, Rockchip, Samsung). No `Makefile` target selects them: all 27 `PROJECT=` lines say ROCKNIX, and the build searches only `projects/ROCKNIX`.
    - **14** are Kodi-era DVB addons, 143,756 bytes, of which 137,432 are three icons.
    - **16** are firmware recipes for boards we do not build.
    - **1** is a device-tree overlay driver, `dtbocfg`, that nothing references.
  - The fork has never edited any of them, and none differs from upstream's current `next`.
  - **What they cost:** reading time, not build time. A reader of `projects/` meets ten hardware families when one is used, and three Rockchip folders share names with ROCKNIX's own devices (`RK3399`, `RK3576`, `RK3588`) but hold unrelated files.
  - **What removing them would cost:** every future merge from ROCKNIX would carry the deletions as conflicts, because ROCKNIX keeps the files.
  - **The question for the maintainer:** keep the class as upstream carries it, or remove it as a fork-only deletion and accept the merge cost. The table recommends keeping it while ROCKNIX does.
  - Excluded from the class:
    - the 4 `intel-ucode` rows (PL-01: reached);
    - the 9 shadowed copies, kept beside their overrides, which ROCKNIX also carries;
    - every unshipped target's rows (PL-03, D-WORKFLOW-185).
- **Where:** `02` F-02 (the generated group table), `04` § Q6, § Q5, § Q7
- **Evidence:** P1, P2, P5, P8, P13, P14
- **Can this be done on the VM?** No: these are files no image carries; the tree and the record show it (brief § 5).
- **Already written:** nothing: no configuration builds them and no image carries them.
- **Acceptance:** #346 carries the coordinator's post with these counts (203 rows; 5,471 lines; 301,712 bytes; 172 / 14 / 16 / 1) and a link to `04` § Q6; `git diff --diff-filter=DR --name-only 8ebaf8daad <fixed-at> -- projects packages` is empty.
- **Disposition note:** open

## PL-03: RK3566 and RK3326, the first widening, held

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-03
- **Owner area:** the shipped-device set (D-WORKFLOW-185)
- **What:** Record the two targets as held, with nothing proposed.
  - 53 rows under their directories: 16 + 37 = 13,833 lines.
  - 6 of the ROCKNIX driver and firmware rows touch them: `generic-dsi` 3, `mali-bifrost` 2, `esp8089-firmware` 1.
  - 4 of T23's generic rows are built only by them.
  - No fork edit; drift 4 rows (RK3566) and 7 (RK3326) of the slice.
  - A widening decision moves these rows, T23's and T43's patch rows together (`03` § 3.5).
- **Where:** `04` § Q6 (the two unit rows), `02` § The targets
- **Evidence:** P4, P6, P14
- **Can this be done on the VM?** No: a disposition of a target, read from the tree and the decision register.
- **Already written:** nothing: no fork edit in either directory.
- **Acceptance:** `04` § Q6's RK3566 and RK3326 rows read `unshipped: first widening, held (D-WORKFLOW-185)`; `git diff --stat 8ebaf8daad <fixed-at> -- projects/ROCKNIX/devices/RK3566 projects/ROCKNIX/devices/RK3326` is empty.
- **Disposition note:** open

## PL-04: `packages/linux/package.mk`, a fork edit in a shadowed dead copy

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q6
- **Source Finding:** F-04
- **Owner area:** fork-own line in a dead upstream copy; the live twin is T11's override
- **What:** `3d7c075f63` (2026-10-02, D-WORKFLOW-123) set `CONFIG_DEFAULT_HOSTNAME "ROCKNIX"` at `packages/linux/package.mk:132` and at `projects/ROCKNIX/packages/linux/package.mk:160`.
  - The override resolves first for every target and sources no generic recipe. So the generic copy never builds, and its edit changes no image.
  - Upstream's head still reads `"${DISTRONAME}"` at both lines, so the base merge meets this hunk; either side is harmless here.
  - Recorded, not reverted: the edit keeps the two copies saying the same thing, and the decision behind it is D-WORKFLOW-123's.
- **Where:** `02` F-04, `04` § Q3, § Q6
- **Evidence:** P2, P7
- **Can this be done on the VM?** No: a recipe no target resolves; the tree shows it.
- **Already written:** nothing inherited: the generic recipe built for no target.
- **Acceptance:** `04` § Q6's `packages/linux` row carries `fork-own edit in a shadowed dead copy; Already written: nothing inherited`; `git diff 8ebaf8daad <fixed-at> -- packages/linux/package.mk` is empty.
- **Disposition note:** open

## PL-05: 39 rows drifted and 226 files across the targets; S922X's loader moves to mainline upstream

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** F-05
- **Owner area:** upstream's, arriving with the next base merge of `next`
- **What:** Against `651150fc88`, 39 of the 397 rows differ: 38 by upstream, 1 the fork's (PL-04).
  - Over the twelve target directories with their patches, the merge brings `226 files changed, 14839 insertions(+), 29156 deletions(-)`.
  - **The seam to keep whole:** upstream's `0deba47fcb` moves `S922X u-boot` from the ROCKNIX vendor fork to mainline `v2026.10` and builds its FIP from `amlogic-boot-fip`'s tree. The merge takes both recipes together.
  - **T27's PL-02 reaches RK3399:** its `u-boot` builds `atf`'s `*)` branch (`u-boot/package.mk:26`; `atf/package.mk:22-25`, outside the slice). Upstream's `6103571f67` moves that branch's URL to `TrustedFirmware-A` and its checksum from `696b8e53...` to `6b1d5e89...`. The merge takes upstream's URL with both checksums, never a crossed pair.
  - Upstream's `6679670966` adds gcc 16 `KCFLAGS` to `RK3326 u-boot-legacy` and `RK3588 u-boot`.
  - Nothing is re-derived here.
- **Where:** `02` § The pins, § The units, § The targets; `03` § 3.5
- **Evidence:** P2, P6, P11
- **Can this be done on the VM?** No: an unshipped target's recipes, read from the tree; no image carries them.
- **Already written:** nothing: no image builds these targets.
- **Acceptance:** the coordinator names the merge that carries `651150fc88` (or later) into `next`; after it, `git diff --stat 651150fc88 next -- projects/ROCKNIX/devices/S922X/packages projects/ROCKNIX/packages/tools/atf/package.mk` is empty.
- **Disposition note:** open

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-01"
  owner_area: "fork-own tool, outside the slice: `tools/renovation-inventory` (P1's)"
  outcome: "open"
- id: PL-02
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-02"
  owner_area: "upstream's: the nine LibreELEC projects, the DVB addons, the unbuilt firmware, `dtbocfg`"
  outcome: "open"
- id: PL-03
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-03"
  owner_area: "the shipped-device set (D-WORKFLOW-185)"
  outcome: "open"
- id: PL-04
  severity: Info
  category: Renovation
  question: Q6
  source_finding: "F-04"
  owner_area: "fork-own line in a dead upstream copy (`packages/linux/package.mk:132`)"
  outcome: "open"
- id: PL-05
  severity: Info
  category: Renovation
  question: Q4
  source_finding: "F-05"
  owner_area: "upstream's, via the next base merge"
  outcome: "open"
```

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | the coordinator's disposition at the stage-D pause |
| PL-02 | Open | the coordinator's disposition at the stage-D pause |
| PL-03 | Open | the coordinator's disposition at the stage-D pause |
| PL-04 | Open | the coordinator's disposition at the stage-D pause |
| PL-05 | Open | the coordinator's disposition at the stage-D pause |
