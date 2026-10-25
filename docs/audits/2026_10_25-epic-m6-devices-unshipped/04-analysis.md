# Analysis — M6.P2 T25, the devices the fork does not ship and the other projects (#672)

## Executive summary

- **What it read.** 397 paths, 49,555 lines and 1,424,530 bytes, at `8ebaf8daad`. That covers:
  - the twelve targets the fork can build and does not ship;
  - the ROCKNIX driver and firmware recipes only they use;
  - the nine LibreELEC projects no target selects;
  - the three `packages/**` units nothing builds.
- **Provenance.** The fork changed one path since the base, in a dead copy. Upstream is 65 commits and 39 rows ahead.
- **Dispositions:**
  - **183 rows are unshipped:** the twelve targets' own rows, AMD64's `intel-ucode` pair and the ROCKNIX driver rows. 53 directory rows plus 6 driver rows touch the held first widening (RK3566, RK3326).
  - **9 are shadowed copies,** 8 with a live override and `iwlwifi-firmware` with an unshipped one.
  - **203 are dead upstream-carried,** the #346 class.
  - **2 are reached after all:** the generic `intel-ucode` copy, which the test image unpacks into its kernel.
- **One finding that changes the record (F-01, Low).** The kernel recipe takes `intel-ucode` and `generic-dsi` by unpack edges. The inventory's plan-derived reach cannot see these edges, so it calls four rows `unreached` that are reached, and lists one target where `generic-dsi` has three. A lead for the coordinator, in the direction opposite to #1086's.
- **Four recorded items, no defects:**
  - the class proposal for #346 (F-02);
  - the first widening, held (F-03);
  - the fork-own dead copy (F-04);
  - the drift the next base merge brings, with S922X's loader moving to mainline (F-05).
- **Nothing proposes a removal of an upstream-carried unit, and nothing under `packages/`, `projects/` or `tools/` changed.**
- **Depth:** Local (D-WORKFLOW-184); no `tools/council/run` call.

## Acceptance-criteria scorecard

#672's fourteen criteria (= brief § 7), at stage C before the punch-list issue. *Met* names its artifact; *waits* names the stage that ticks it.

| # | Criterion | State |
| --- | --- | --- |
| 1 | `00` and `01` to `05` | met at stage C: all six files |
| 2 | the lint `PASS` | pre-issue at stage C (`00`); resolution waits for stage H |
| 3 | the Local plan; no seat call | met: `second-opinions/review-plan.json`; `00` records no `tools/council/run` |
| 4 | every punch item at a Phase 7 outcome | waits: stage D onward |
| 5 | `reviewed-at:` and `fixed-at:` | waits: stage H |
| 6 | `01` § Scope | met (`8a13e45fa7`) |
| 7 | the coverage table, 397 rows, regenerated | met: `02` § Coverage; the grep prints 397; `check` exits 0 |
| 8 | targets 12, projects 9, pins 10 (+2 cited), trees 53 | met: `02`, asserted by the generator |
| 9 | § Mechanical checks | met: `02`, every brief § 5 check plus stage B's |
| 10 | Q6 the unit table, Q7 the duplicate map, Q5 the weight and drift | met: below |
| 11 | every proof's cell, the count equal to `00`'s | met: 14 and 14 |
| 12 | every punch item's `question:`; the class proposal one item; no change under `packages/` or `projects/` | met in `05` (pre-issue); the diff is empty |
| 13 | the retro | waits: stage G |
| 14 | the five checkers and the lint at hand-back | waits: stage H |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| A later decision reads the inventory's `unreached` as "safe to remove" for a reached row | Low | Medium | F-01's four `intel-ucode` rows; the class proposal (F-02) excludes them, and the lead goes to the coordinator |
| A base merge takes S922X's new u-boot without `amlogic-boot-fip`'s FIP tree | Low | Low | both recipes arrive together in one merge; an unshipped target's build, not a device (F-05) |
| The dead generic kernel copy's hostname hunk conflicts at the merge | Medium | None | the copy builds for no target; either side is harmless (F-04) |
| A target retired without moving its patch and generic rows | Low | Low | `03` § 3.5 names the pairings with T23 and T43; this table retires nothing |

## Coverage boundary

- **Read:** every one of the 397 paths' identities, reach, tier, drift and disposition. Read in full: the 52 recipes (`pkgcheck`, hosts, the edge sweep), the 10 loader pins, the 53 device trees (includes, `model`, `compatible`, dt-id), the twelve `options` files' cited lines and the kernel recipe's version case and edges.
- **Not read:**
  - the `*.patch` and `linux*.conf` rows (T43's under the targets, T40's under the projects), except each conf's header line;
  - `distributions/` (T6's);
  - the generic-packages area's unshipped rows (T23's);
  - the shipped pair and the test image (T27, T28, T11).
- **Not checked:** an author's current release, a host's status, a tarball's contents. All are `CANNOT (no network)`.
- **Not run:** a plan generation or a build. Reach rests on the inventory's plan runs at `eb4763e3cc` plus this slice's edge sweep; where the two disagree, F-01 says so.

## Second opinion

**Local, at epic tier, under D-WORKFLOW-184.** Plan § 6c's default for a dead-end table, `slices.json` `k: 25`. No reviewer was selected and no `tools/council/run` call was made, keyed or not. `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184` and the reason. The check is the lint, the counts and the generator's assertions.

## Finding Verification

Each finding re-derived from the tree after it was written (Phase 4.5):

| Finding | Re-derivation | Verdict |
| --- | --- | --- |
| F-01 | `edges` and b08: `:69-72`, `:202`, `:81-82`, `:108-111`; `config/functions:789-798` and `:1057-1079` for the resolution; T11's record at `ed8c48f3cd` for the payload (153 entries) | confirmed |
| F-02 | `dead`: 203 rows, 5,471 lines, 301,712 bytes; fork commits 0 per unit (`units`); 0 rows differing at `651150fc88` among the projects | confirmed |
| F-03 | `units`, `q6`: RK3566 16, RK3326 37; 6 driver rows touch them | confirmed |
| F-04 | c13, c14; `git diff 651150fc88 8ebaf8daad -- packages/linux/package.mk`: the fork's two-line hunk alone; the override resolves first | confirmed |
| F-05 | c08, b07, § The pins: 39 rows; 226 files; S922X's `0deba47fcb` and `amlogic-boot-fip` identical at both hashes | confirmed |

A narrowing found while writing: the first draft of `03` said upstream had edited the generic kernel copy. `git diff 651150fc88 8ebaf8daad` shows the fork's hunk alone, and the sentence was corrected before commit. The first draft of F-02's table was typed (4,960 lines, 140,469 bytes for the projects). The generator's `dead` section gives 4,966 and 145,992, and the table is now generated.

## Renovation face

### Q1 Modernize

The 52 recipes' resolved hosts (b05):
- `github.com` 38;
- `www.kernel.org` 2;
- one each: `cdn.kernel.org`, `linuxtv.org`, `developer.qualcomm.com`, `www.nxp.com`, `source.codeaurora.org`, `download.savannah.gnu.org`, `review.coreboot.org`, `gitlab.com`, `ftp.denx.de`, `source.denx.de`;
- `${DISTRO_SRC}` (`sources.libreelec.tv`) 2;
- RK3566's wrapper with no URL.

**None is shown retired: a host's status is `CANNOT (no network)`.** `source.codeaurora.org`, `developer.qualcomm.com` and `www.nxp.com` are named as the ones to check first, when a check is possible. All three recipes are dead or shadowed, so no build fetches them. No item: the class proposal (F-02) carries them.

### Q2 Standards

`tools/pkgcheck` over the 52 (the tree's copy, b02): **52 PASS, 0 FAIL, 1 WARN**. The WARN is RK3326's `u-boot` `:063`, *unknown function* `generate_custom_extlinux_conf_files()`: upstream's, recorded, not fixed. The control fails with rc 1 (b03). The whole tree's baseline is 1,607 recipes, 12 FAIL and 43 WARN, and none of the 12 is in the slice (b04). **None** as a finding.

### Q3 Bugs

**None.** The one fork-own row is a dead copy whose twin in the override is the live edit (F-04, `Already written:` nothing inherited). Every other row is upstream-carried and unchanged by the fork since the base. F-01 is a defect in no image: the edges do what they are written to do. Only the record misreads them.

### Q4 Package currency

- **(a) The drift per unit against `651150fc88`:** `02` § The units (rows differing; the newest upstream commit on the rows) and § The targets (files differing per directory, upstream commits since `2026-06-01T00:00:00Z` with the newest). 39 rows differ, all but one by upstream (F-05).
- **(b) The pins,** in T27's shape: the table below. Seven files are identical at both hashes. Two gain upstream's gcc 16 `KCFLAGS`, and S922X's `u-boot` moves to mainline `v2026.10` with a FIP built from `amlogic-boot-fip` (F-05). The oldest pins are `9f1fab30f6` (2025-07-13): RK3566's wrapper, RK3588's vendor u-boot and S922X's `amlogic-boot-fip`. The authors' releases are `CANNOT (no network)`; `tools/fork-package-freshness` is the RC's check (D-WORKFLOW-024).
- **(c) Each conf's header against the recipe's branch:** all twelve agree (`02` § The targets). RK3588's vendor `6.1.75` is set by a commit pin, `b8e62bed74...`, not a version.

<!-- begin t25:pins -->
| Unit | At `8ebaf8daad` | At `651150fc88` | Set by (`git log -1 -S`) | Author's current release |
| --- | --- | --- | --- | --- |
| `RK3326 u-boot` | `v2025.10`, sha256 `5414ee86562a...` | the same file | ad79cc1b50 2025-11-15 Danil Zagoskin | CANNOT (no network) |
| `RK3326 u-boot-legacy` | `2492a3e467e332e2350d987234ce6123700b3392`, sha256 `d8b358f20394...` | the same pin; the file differs | d2b00cd91a 2025-12-05 Danil Zagoskin | CANNOT (no network) |
| `RK3399 u-boot` | `2025.10`, sha256 `b4f032848e56...` | the same file | 799514729e 2025-11-11 rocknix | CANNOT (no network) |
| `RK3566 u-boot` | `1.0`, no `PKG_SHA256` | the same file | 9f1fab30f6 2025-07-13 ROCKNIX Team | n/a (no source: `PKG_URL=""`) |
| `RK3566 u-boot-Generic` | `v2026.01`, sha256 `03bb43c58d23...` | the same file | 95d1ec60d2 2026-01-08 sydarn | CANNOT (no network) |
| `RK3566 u-boot-Specific` | `v2026.01`, sha256 `03bb43c58d23...` | the same file | 95d1ec60d2 2026-01-08 sydarn | CANNOT (no network) |
| `RK3576 u-boot` | `88dc2788777babfd6322fa655df549a019aa1e69`, sha256 `c9858cd5fdc0...` | the same file | ed8ab09e5c 2026-04-19 sydarn | CANNOT (no network) |
| `RK3588 u-boot` | `e99376f7dd01e310a0874459a1fe7535be431f43`, sha256 `045519a0eb54...` | the same pin; the file differs | 9f1fab30f6 2025-07-13 ROCKNIX Team | CANNOT (no network) |
| `S922X amlogic-boot-fip` | `e96b6a694380ff07d5a9e4be644ffe254bd18512`, sha256 `2cc06bc7d564...` | the same file | 9f1fab30f6 2025-07-13 ROCKNIX Team | CANNOT (no network) |
| `S922X u-boot` | `b91540f886e8655a1547532eb0077e83a7b431d7`, sha256 `5cecb72e2392...` | `v2026.10`, sha256 `f943a88389c8...` | a01eb88a1e 2026-08-23 John Williams | CANNOT (no network) |
| `rkbin` (cited by path, outside the slice: `projects/ROCKNIX/packages/tools/rkbin/package.mk`) | `7c35e21a8529...`, `74213af1e952...` (2 branches of a device case) | the same file | not owned here | not owned here |
| `qcom-abl` (cited by path, outside the slice: `projects/ROCKNIX/packages/tools/qcom-abl/package.mk`) | `1.0` | the same file | not owned here | not owned here |
<!-- end t25:pins -->

### Q5 Efficiency

- **What the 397 cost: carriage, not build.** 397 files, 49,555 lines and 1,424,530 bytes at `8ebaf8daad` (c15). Device trees are 34,437 lines of it (69 %). No shipped image builds a row, except F-01's generic `intel-ucode` in the test image's kernel (T11's payload).
- **The dead class** is 203 rows, 5,471 lines and 301,712 bytes (21 % of the slice's bytes). 143,756 of those bytes are the DVB addons' 14 rows, and 137,432 of those are three addon icons (`icon/icon.png` under `crazycat`, `dvb-latest` and `digital_devices`).
- **What the drift costs the next merge:** over the twelve target directories with their patches, `226 files changed, 14839 insertions(+), 29156 deletions(-)` (b07), all upstream's.

### Q6 Dead ends

**The unit table:** 25 rows, each with its disposition in D-WORKFLOW-209's words, generated from the coverage rows (`tools/t25-tables.py q6`). Counts: dead 203, reached after all 2, shadowed 9, unshipped 183, total 397 (`counts`).
- **No row proposes a removal of an upstream-carried unit.** The generator asserts that no disposition says so.
- **`Already written:`** is answered where a fork edit exists, and one does: `packages/linux`.

<!-- begin t25:q6 -->
| Unit | Paths | Disposition (D-WORKFLOW-209's words; ×n where the unit's rows differ) | `Already written:` |
| --- | ---: | --- | --- |
| **`projects/ROCKNIX/devices/AMD64`** | 15 | unshipped: target AMD64, in world no ×13; unshipped: target AMD64, in world no (through the kernel's unpack edge, F-01) ×2 | no fork edit |
| **`projects/ROCKNIX/devices/RK3326`** | 37 | unshipped: first widening, held (D-WORKFLOW-185) | no fork edit |
| **`projects/ROCKNIX/devices/RK3399`** | 4 | unshipped: target RK3399, in world yes | no fork edit |
| **`projects/ROCKNIX/devices/RK3566`** | 16 | unshipped: first widening, held (D-WORKFLOW-185) | no fork edit |
| **`projects/ROCKNIX/devices/RK3576`** | 6 | unshipped: target RK3576, in world yes | no fork edit |
| **`projects/ROCKNIX/devices/RK3588`** | 3 | unshipped: target RK3588, in world yes | no fork edit |
| **`projects/ROCKNIX/devices/S922X`** | 4 | unshipped: target S922X, in world yes | no fork edit |
| **`projects/ROCKNIX/devices/SM4450`** | 18 | unshipped: target SM4450, in world no | no fork edit |
| **`projects/ROCKNIX/devices/SM6115`** | 16 | unshipped: target SM6115, in world no | no fork edit |
| **`projects/ROCKNIX/devices/SM8250`** | 28 | unshipped: target SM8250, in world yes | no fork edit |
| **`projects/ROCKNIX/devices/SM8650`** | 8 | unshipped: target SM8650, in world yes | no fork edit |
| **`projects/ROCKNIX/devices/SM8750`** | 14 | unshipped: target SM8750, in world yes | no fork edit |
| **`projects/ROCKNIX/packages/{linux-drivers,linux-firmware}`** | 15 | unshipped: target RK3588, in world yes ×5; unshipped: target RK3326, RK3566, RK3576, in world yes (RK3326, RK3566 the first widening, held) ×3; unshipped: target RK3326, RK3566, RK3576, S922X, in world yes (RK3326, RK3566 the first widening, held) ×2; unshipped: target S922X, in world yes ×1; unshipped: target SM8650, in world yes ×1; dead, upstream-carried (#346's class) ×1; unshipped: target RK3399, in world yes ×1; unshipped: first widening, held (D-WORKFLOW-185) ×1 | no fork edit |
| **`projects/ARM`** | 4 | dead, upstream-carried (#346's class) | no fork edit |
| **`projects/Allwinner`** | 24 | dead, upstream-carried (#346's class) | no fork edit |
| **`projects/Amlogic`** | 19 | dead, upstream-carried (#346's class) | no fork edit |
| **`projects/Generic`** | 19 | dead, upstream-carried (#346's class) | no fork edit |
| **`projects/NXP`** | 25 | dead, upstream-carried (#346's class) | no fork edit |
| **`projects/Qualcomm`** | 7 | dead, upstream-carried (#346's class) ×6; shadowed copy, override projects/ROCKNIX/packages/tools/mkbootimg, override reached ×1 | no fork edit |
| **`projects/RPi`** | 28 | dead, upstream-carried (#346's class) | no fork edit |
| **`projects/Rockchip`** | 35 | dead, upstream-carried (#346's class) | no fork edit |
| **`projects/Samsung`** | 12 | dead, upstream-carried (#346's class) | no fork edit |
| **`packages/linux`** | 4 | shadowed copy, override projects/ROCKNIX/packages/linux, override reached ×3; shadowed copy, override projects/ROCKNIX/packages/linux, override reached; fork-own edit in a shadowed dead copy; Already written: nothing inherited ×1 | Already written: nothing inherited (the generic recipe built for no target) |
| **`packages/linux-driver-addons`** | 14 | dead, upstream-carried (#346's class) | no fork edit |
| **`packages/linux-firmware`** | 22 | dead, upstream-carried (#346's class) ×16; shadowed copy, override projects/ROCKNIX/packages/linux-firmware/kernel-firmware, override reached ×3; reached after all: the test image (GENERIC_X64), through the kernel's unpack edge (F-01) ×2; shadowed copy, override projects/ROCKNIX/packages/linux-firmware/iwlwifi-firmware, override unshipped ×1 | no fork edit |
<!-- end t25:q6 -->

The brief's 172 + 32 + 3 dead rows are 172 + 30 + 1 here: F-01 moves the generic `intel-ucode` pair to *reached after all* and AMD64's pair to `unshipped`. `dtbocfg` stays dead: no edge reaches it (`edges`).

### Q7 Clarity and structure

**The duplicate map** (`tools/t25-tables.py q7`):
- the four Rockchip device names that duplicate ROCKNIX's (three exact, `RK356X` a near-name of `RK3566`);
- the 9 shadowed pairs with the override's reach;
- the `CONFIG_DEFAULT_HOSTNAME` strings across the two kernel recipes and the confs (named, not read: T40's and T43's).

<!-- begin t25:q7 -->
| Name or path | Its duplicate | Kind | Note |
| --- | --- | --- | --- |
| **`projects/Rockchip/devices/RK3399`** | `projects/ROCKNIX/devices/RK3399` | exact name | different trees, different `options` |
| **`projects/Rockchip/devices/RK356X`** | `projects/ROCKNIX/devices/RK3566` | near-name | different trees, different `options` |
| **`projects/Rockchip/devices/RK3576`** | `projects/ROCKNIX/devices/RK3576` | exact name | different trees, different `options` |
| **`projects/Rockchip/devices/RK3588`** | `projects/ROCKNIX/devices/RK3588` | exact name | different trees, different `options` |
| **`packages/linux-firmware/iwlwifi-firmware/package.mk`** | `projects/ROCKNIX/packages/linux-firmware/iwlwifi-firmware` | shadowed pair | override unshipped |
| **`packages/linux-firmware/kernel-firmware/firmwares/any.dat`** | `projects/ROCKNIX/packages/linux-firmware/kernel-firmware` | shadowed pair | override reached |
| **`packages/linux-firmware/kernel-firmware/firmwares/x86_64.dat`** | `projects/ROCKNIX/packages/linux-firmware/kernel-firmware` | shadowed pair | override reached |
| **`packages/linux-firmware/kernel-firmware/package.mk`** | `projects/ROCKNIX/packages/linux-firmware/kernel-firmware` | shadowed pair | override reached |
| **`packages/linux/package.mk`** | `projects/ROCKNIX/packages/linux` | shadowed pair | override reached |
| **`packages/linux/sysctl.d/network.conf`** | `projects/ROCKNIX/packages/linux` | shadowed pair | override reached |
| **`packages/linux/sysctl.d/qdisc.conf`** | `projects/ROCKNIX/packages/linux` | shadowed pair | override reached |
| **`packages/linux/udev.d/40-modeswitch.rules`** | `projects/ROCKNIX/packages/linux` | shadowed pair | override reached |
| **`projects/Qualcomm/devices/Dragonboard/packages/mkbootimg/package.mk`** | `projects/ROCKNIX/packages/tools/mkbootimg` | shadowed pair | override reached |
| `${PKG_BUILD}/scripts/config --set-str CONFIG_DEFAULT_HOSTNAME "ROCKNIX"` | 2 line(s) | hostname string | the generic copy and the override, both set by `3d7c075f63`: `packages/linux/package.mk:132`, `projects/ROCKNIX/packages/linux/package.mk:160` |
| `CONFIG_DEFAULT_HOSTNAME="@DEVICENAME@"` | 12 line(s) | hostname string | named, not read (T40's and T43's confs) |
| `CONFIG_DEFAULT_HOSTNAME="@DISTRONAME@"` | 18 line(s) | hostname string | named, not read (T40's and T43's confs) |
| `CONFIG_DEFAULT_HOSTNAME="ROCKNIX"` | 1 line(s) | hostname string | a conf's literal, named, not read (T43's): `projects/ROCKNIX/devices/SM8750/linux/linux.aarch64.conf:51` |
<!-- end t25:q7 -->

The structure a reader meets: `projects/` holds ten families and the build ever searches one. `projects/Rockchip/devices/RK3588` and `projects/ROCKNIX/devices/RK3588` are unrelated trees with one name. The second sentence is the one worth a line in the class proposal (F-02).

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **None for a defect.** F-01 is a record gap, and its guard is the inventory (`tools/renovation-inventory`). Per the brief's ladder, a shape the tool misses is a lead, not a rule.

### Codification gaps (proposals for the coordinator)

1. **Table briefs:** a reach verdict cites the plan-derived `buildable_by` *and* an edge sweep. That means every `PKG_DEPENDS_*` (including `_UNPACK`), `get_build_dir`, `get_install_dir` and `get_pkg_directory` naming the recipe, with the resolution order read from `config/functions:789-798`. T25's `edges` section is the shape.
2. **A generated table is generated whole.** Hand-typed counts beside a generator drift. F-02's first draft did; the fix is a generator section, not a corrected number.

### Recommended action sequence

The coordinator dispositions `05`. F-01 goes to #1086's class or a new issue for the inventory. F-02 is posted on #346 by the coordinator. Nothing else waits on this slice.

## Quality self-check

- **Blindspot 13 (assumed done):** no checkbox here is ticked on an artifact's existence. Each criterion's state names its check (§ Acceptance-criteria scorecard).
- **Blindspot 22 (a probe that cannot report absence):** each reachability read has its positive control (c16, c17). The edge sweep fails on an unnamed reached edge. The `pkgcheck` run has a failing control.
- **Blindspot 46 (a name read as a behaviour):** the reach verdicts rest on the resolution order and the edges, not on directory names. F-01 is what that found.
- **Blindspot 51 (a checklist from open boxes):** the scorecard is the brief's fourteen, read against #672's body at dispatch.
- **Blindspot 75 (a corpus read on the wrong tree):** every figure was produced by a command at `8ebaf8daad`. The tip-versus-hash check covers the `Makefile`, `config` and `scripts` reads (b01). Two typed figures were caught and replaced by generated ones (§ Finding Verification).
- **Rules read this session** (`working-principles.md` § Pre-flight): `engineering-practices.md`, `packaging-and-patches.md`, `device-builds.md`, `fork-workflow.md`, `release-candidates.md`, `upgrade-and-install.md`, `bugs-are-agent-first.md`, `issue-tracking.md`, `vm-first.md`, `decision-register.md`. Decisions read: D-WORKFLOW-184, -185 and -209, and -123 (the hostname's reason).
