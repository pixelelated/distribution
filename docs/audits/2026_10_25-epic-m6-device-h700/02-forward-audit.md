# Forward audit — M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

- **`reviewed-at`:** `ed7fd0ea50`. The 28 are read at `8ebaf8daad`'s bytes (`git diff --stat 8ebaf8daad ed7fd0ea50 -- packages projects` is empty). Upstream is `651150fc88`, read locally.
- **Can this be done on the VM? Yes -- on the host, with no network.** Every read, diff and log runs on the build host at `8ebaf8daad`. The GENERIC_X64 guest cannot be an H700, so no guest is asked for.
- **A fact only a board can show is a `docs/releases/device-facts.md` row, read and cited:** L15 (the RG35XX SP's boot, 2026-10-16), L16 (the RG SP's, 2026-10-12) and L29 (the watchdog and ramoops, never observed). Nothing runs on a unit (D-QA-015, D-QA-027).
- **Recipe reads pass the masking `sed`;** `h700-suspend-stub/package.mk:43` is never quoted raw.
- **The runs** are `stage-a/runs.sh` (r01 to r16) and r14b, each with its exit and wall time in `stage-a/runs.tsv`.

## Phase 2 — #674's checklist at stage B

| Criterion (#674) | State at stage B | Artifact |
| --- | --- | --- |
| `00` and `01` to `05` | `00` to `04` written; `05` at stage D | this folder |
| The lint | `--phase pre-issue` at stage C | — |
| The seat's plan, provenance, manifest | the plan written; the seat at stage C | `second-opinions/review-plan.json` |
| The punch-list issue at outcomes | stage D onward | — |
| `reviewed-at`, `fixed-at`, the empty diffs | `reviewed-at` `ed7fd0ea50`; r16 empty | § The runs |
| `01` § Scope | complete | `01-research-notes.md` |
| `## Coverage`, 28 rows | 28 | below |
| § The pins, one row per unit | six rows | below |
| § The configuration | 12 / 13, every line attributed | below |
| § The loader and the tree | written; L15, L16 and #44 cited | below |
| § The device trees, 15 rows and the `.disabled` row | written | below |
| § The runs | 17 runs | below |
| `00`: no guest, build, fetch, handheld command or extra invoke | so far | `00-running-log.md` |
| `04` Q4, Q2, Q3, Q6, § Second opinion | Q1 to Q7 written; second opinion at C | `04-analysis.md` |
| `proved:` cells; `question:` per item | the proofs here; the items at D | § Proofs |
| The retro, the checkers | stages G, H | — |

## Coverage

One row per path of the 28, in path order. *Reach* is the inventory's column at `2174265e9c`.

| Path | Tier | Reach | Lines | What it is, and who reads it | Finding or disposition | proved |
| --- | --- | --- | ---: | --- | --- | --- |
| `projects/ROCKNIX/devices/H700/bootloader/update.sh` | upstream-carried | shipped | 63 | The in-place updater, run by the shipped `init` on an update: copies `device_trees` and `overlays` to `/flash` (`:21-24`), writes `/dtb.img` from `/proc/device-tree/rocknix-dt-id` (`:26-32`), picks the loader by `vdd-dram` (1,200,000 µV DDR3, 1,100,000 µV DDR4, `:34-49`) and `dd`s it at `bs=1K seek=8` (`:51-57`). Any other voltage, or a failed read, writes no loader. | § The loader and the tree; F-04; Q3 not a bug | tree |
| `projects/ROCKNIX/devices/H700/config/kernel-firmware.dat` | upstream-carried | shipped | 18 | The H700 firmware list (13 files: rtw88, rtl8821cs BT, ten panels). The recipe also builds the same 13 into the kernel (`linux/package.mk:223-243`). | F-05 (duplicates); T5's F-17, the stamp (#836) | tree |
| `projects/ROCKNIX/devices/H700/filesystem/usr/lib/udev/rules.d/80-clock.rules` | upstream-carried | shipped | 2 | Sets the clock from `rtc0` (PCF8563) at boot (`hwclock --hctosys`). | F-08: deleted upstream (`899193e5af`), settled by the next base merge | tree |
| `projects/ROCKNIX/devices/H700/filesystem/usr/lib/udev/rules.d/wlan0.powersave.off.rules` | upstream-carried | shipped | 1 | Turns off Wi-Fi power saving on the SDIO chip at `mmc2:0001:1`. | carried; no finding | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg-sp.dts` | upstream-carried | shipped | 17 | A fork-tree board file, compiled into `device_trees` on every H700 image: the RG SP's tree (its `rocknix-dt-id`; device-facts L16, *DDR3 bootloader/RG SP tree*). | shipped unit | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg28xx.dts` | upstream-carried | shipped | 18 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg34xx-sp-v2-panel.dts` | upstream-carried | shipped | 23 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg34xx-sp.dts` | upstream-carried | shipped | 23 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg34xx.dts` | upstream-carried | shipped | 17 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-2024-rev6-panel.dts` | upstream-carried | shipped | 15 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-h-rev6-panel.dts` | upstream-carried | shipped | 15 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-plus-rev6-panel.dts` | upstream-carried | shipped | 15 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-pro.dts` | upstream-carried | shipped | 17 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-sp-v2-panel.dts` | upstream-carried | shipped | 15 | A fork-tree board file, compiled into `device_trees` on every H700 image: an RG35XX SP tree (the v2 panel). The other is mainline's `rg35xx-sp`, whose dt-id comes from kernel patch 0154 (T41's). Device-facts L15 does not say which the LPDDR4 unit boots. | shipped unit | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-h-v2-panel.dts` | upstream-carried | shipped | 14 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-h.dts` | upstream-carried | shipped | 38 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-v-v2-panel.dts` | upstream-carried | shipped | 14 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-v.dts` | upstream-carried | shipped | 36 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rgcubexx.dts` | upstream-carried | shipped | 44 | A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image. | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf` | vendor-carried (fork-written) | shipped | 8129 | The kernel configuration, `Linux/arm64 7.2.0`, 8,129 lines; upstream's file with a base, its own copy at `651150fc88` (12 / 13 lines apart). | § The configuration; the order's *fork-written* an erratum | tool-run |
| `projects/ROCKNIX/devices/H700/options` | upstream-carried | shipped | 84 | Device knobs: cortex-a53 with `+crc+fp+simd` on aarch64, `crypto-neon-fp-armv8` FPU on arm (`:7-19`); `BOOTLOADER="u-boot"` (`:34`); atf `sun50i_h616` (`:37-39`); panfrost; zram and swap 0 (`:77-84`). Upstream changes the ZRAM algorithm and adds `THP_DEFRAG`. | F-03 (the SIMD flags against the rule's table); F-09 (Q7) | tree |
| `projects/ROCKNIX/devices/H700/packages/h700-suspend-stub/package.mk` | upstream-carried | shipped | 55 | Builds one SRAM suspend stub per memory type from each u-boot recipe's defconfig (`:20-47`), refusing two stubs with the same DRAM type and clock (`:42-45`). Pin `712653d11230`. Line 43 matches the credential read filter and is read masked. | § The pins | tree |
| `projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/package.mk` | upstream-carried | shipped | 43 | u-boot `v2026.01` for the LPDDR3 defconfig, its SPL embedding atf's BL31. | § The pins; F-10 | tree |
| `projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/sources/configs/anbernic_rg35xx_h700_lpddr3_defconfig` | upstream-carried | shipped | 35 | The LPDDR3 board defconfig; 20 lines from the LPDDR4 one (DRAM timing, `H616_LPDDR3`, `AXP_DCDC3_VOLT=1200`). | carried; no finding | tree |
| `projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/package.mk` | upstream-carried | shipped | 43 | u-boot `v2026.01` for the LPDDR4 defconfig; differs from DDR3's in `PKG_NAME` and `PKG_UBOOT_CONFIG` only. | § The pins; F-10 | tree |
| `projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/sources/configs/anbernic_rg35xx_h700_lpddr4_defconfig` | upstream-carried | shipped | 35 | The LPDDR4 board defconfig (`H616_LPDDR4`, `AXP_DCDC3_VOLT=1100`). | carried; no finding | tree |
| `projects/ROCKNIX/devices/H700/packages/u-boot/package.mk` | upstream-carried | shipped | 36 | The wrapper: depends on `u-boot-${SUBDEVICE}` for each SUBDEVICE from `config.xml` (DDR3, DDR4) and installs `H700_<sub>_u-boot-sunxi-with-spl.bin` (`:16-35`). | § The pins; F-10 | tree |
| `projects/ROCKNIX/devices/H700/patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled` | upstream-carried | shipped | 4036 | A 4,036-line patch (tiopex, 2025-05-29) no build applies: `scripts/unpack:143-159` globs `*.patch`. Added as `.disabled` by `fad6d7d27a`. The inventory reads it `shipped`. | F-06; the reach is #1086's shape | tree |

## The pins

`CANNOT (no network)` for every author's current release. That check is `tools/fork-package-freshness`'s at the RC (D-WORKFLOW-024), named here, not run (r07 for the recipes in the slice; the atf and kernel recipes read at their lines).

| Unit | At `8ebaf8daad` | At `651150fc88` | Set by | Author's current release |
| --- | --- | --- | --- | --- |
| u-boot-DDR3 | `v2026.01`, sha256 `03bb43c58d23...` | the same | `2e825afd0c` (2026-06-08, Philippe Simons, *h700: subdevices*) | CANNOT (no network) |
| u-boot-DDR4 | `v2026.01`, the same sha256 | the same | `2e825afd0c` | CANNOT (no network) |
| u-boot (the wrapper) | `1.0`, no URL: builds nothing, installs each SUBDEVICE's loader | the same | `2e825afd0c` | n/a (no source) |
| h700-suspend-stub | `712653d11230...`, sha256 `3698da9aad40...` (`Jacob-Matthew-Cook/h700-suspend-stub`) | the same | `fca6ac5140` (2026-09-17, Jacob Cook, *H700: firmware deep sleep*) | CANNOT (no network) |
| atf (H700 branch of `projects/ROCKNIX/packages/tools/atf/package.mk:16-21`) | `2.12.0`, **no `PKG_SHA256`**, URL `ARM-software/arm-trusted-firmware` | `2.12.0`, sha256 `d95aaf292792...`, URL `TrustedFirmware-A/trusted-firmware-a` (`6103571f67`, 2026-10-11) | `9f1fab30f6` (2025-07-13, the oldest pin here) | CANNOT (no network); the override's `*)` branch is 2.10.0, and the separate generic `packages/tools/atf` is at 2.15.0 |
| kernel (`projects/ROCKNIX/packages/linux/package.mk:29-35`) | `7.2`, sha256 `f9fef3d14c0d...` | `7.2`, the same | `0c77a91dca` (2026-08-17, *linux: update H700 to kernel 7.2*) | CANNOT (no network) |

**The atf checksum is already known.** T8's sweep and D-WORKFLOW-194 list `atf` 2.12.0 among the five archive versions with no `PKG_SHA256`. T5's E6 gave it `30abf4da07418ad0...` from the `ARM-software` URL (`430abc8f66`, #834, on `feature/m6-build-engine-652`). **The seam:** upstream's fix moves the URL to `TrustedFirmware-A` and sets **different** checksums for both branches. The H700 branch becomes `d95aaf29...`, and the `*)` branch moves from `696b8e53...` to `6b1d5e89...`, because a GitHub archive's bytes carry the repository name. A merge of `next` takes upstream's URL with both of upstream's checksums. For the recorded archive bytes, a crossed pair (old URL with upstream's checksum, or new URL with T5's) fails T5's checksum check (`scripts/get_archive` on T5's branch). As the seat narrowed it (G-4), a cached archive whose checksum stamp matches, or a mirror, can satisfy a recipe whatever its URL says, so the guarantee is about bytes, not URL spellings (F-02, for T25).

## The configuration

`linux/linux.aarch64.conf`: 8,129 lines, header `# Linux/arm64 7.2.0 Kernel Configuration` (r02). **It is upstream's file, and its base is upstream's own copy:** added by `9f1fab30f6` (2025-07-13, ROCKNIX Team). Against `651150fc88`'s copy it is **12 removed / 13 added** (r03). Every line, attributed:

| Lines (`<` upstream, `>` ours) | Commit |
| --- | --- |
| `> CONFIG_WATCHDOG_SYSFS=y`, `> CONFIG_PSTORE_CONSOLE=y`, `> CONFIG_PSTORE_RAM=y`, `> CONFIG_SOFTLOCKUP_DETECTOR=y`, `> CONFIG_DETECT_HUNG_TASK=y`, `> CONFIG_DEFAULT_HUNG_TASK_TIMEOUT=120`, against their five `is not set` lines | **the fork's `cbf75c0b06`** (2026-09-10; D-SYS-002/003/004: the watchdog, panic on hang, ramoops). The one fork commit since the merge base `c445081a59` (r04) |
| `CONFIG_CC_VERSION_TEXT` gcc 16.2.0 / 15.2.0; `CONFIG_GCC_VERSION` 160200 / 150200; `< CONFIG_CC_HAS_COUNTED_BY_PTR=y` | upstream's `c0980b2b71` (2026-10-02). Ours still records gcc 15.2.0, the fork's held-back gcc pin (`device-builds.md`) |
| `< # CONFIG_RAID6_PQ_BENCHMARK is not set` / `> CONFIG_RAID6_PQ_BENCHMARK=y` | upstream's `5f56cd5150` (2026-10-04, *skip the RAID6 algorithm benchmark at boot*) |
| `CONFIG_RUSTC_LLVM_VERSION` 230101 / 220108; `CONFIG_RUSTC_LLVM_MAJOR_VERSION` 23 / 22; `> CONFIG_INPUT_POLLDEV=y` | upstream's `6fbefc45c6` (2026-10-18) |
| `CONFIG_RUSTC_VERSION` 109901 / 109801 | upstream's `6fbefc45c6`, then `dcafa74090` (2026-10-22) |

Upstream's four are a toolchain refresh and one boot-time option. The RAID6 benchmark matters to boot time and comes with the next base merge. **The order's *fork-written* is an erratum:** the inventory's `tier_note` says it because the fork touched the file once. So is the futro's guess that this configuration *will meet the same question* as T11's: it has a base. Against every other configuration in the tree it is far (the brief's counts: RK3326 898 / 1,809, RK3566 1,518 / 1,908, LibreELEC's Allwinner 1,871 / 1,953, SM8550 1,585 / 1,106). The fork's six lines are explicit settings, so a rebase onto upstream's copy keeps them.

## The loader and the tree

**On a fresh card** (the image step):
- `scripts/mkimage` sources the project `bootloader/mkimage`. Its `mkimage_uboot` writes `H700_${SUBDEVICE}_u-boot-sunxi-with-spl.bin` at `bs=1K seek=8` (`:18-21`), one image per SUBDEVICE (DDR3, DDR4), from `config.xml`'s `mkimage_options="dtb,extlinux,uboot"`.
- `mkimage_extlinux` writes `extlinux.conf` with `FDT /dtb.img` (`:45-50`; `fdt="dtb.img"` in `config.xml`). The DDR3 image adds `FDTOVERLAYS /overlays/sun50i-h700-anbernic-rg35xx-2024-ddr3.dtbo` (`:52-55`).
- `mkimage_dtb`'s `*)` branch copies `device_trees` (`:88`).
- **No line creates `dtb.img`** (r10). `mkimage_all` (`distributions/ROCKNIX/config/functions:384-399`) only calls `mkimage_<step>` for each `config.xml` option (`dtb`, `extlinux`, `uboot`), and no H700 package stages a custom `extlinux` directory. So a fresh card does not boot until it is activated by hand, as `docs/device-flashing-runbook.md`'s H700 section says.
- *A correction to the brief and T11's `02`:* `mkimage:26`'s `device_trees` copy is the SM8550/8650/8750 branch (`:22-26`); H700's trees come from `mkimage_dtb` (`:88`).

**On an update** (`bootloader/update.sh`, run by the shipped `init` when `update.sh` exists):
- **The tree:** `:21-24` copies `device_trees` and `overlays` to `/flash`. `:26-32` reads `/proc/device-tree/rocknix-dt-id` and copies `device_trees/<dt-id>.dtb` to `/flash/dtb.img`, so the unit keeps the tree it booted, refreshed from the new build.
- **The loader:** `:35-37` finds the regulator named `vdd-dram`. `:40-48` maps `microvolts` 1,200,000 to the DDR3 loader and 1,100,000 to DDR4. `:52-56` `dd`s it at `bs=1K seek=8`.
- **Any other voltage, a missing regulator or a failed read leaves `UBOOT_BIN` empty, and no loader is written** (`:52`), as long as the caller does not export `UBOOT_BIN`. The script never initializes it or `VDD_REG_PATH` (the seat's G-9). No caller sets either: `init` exports only `BOOT_ROOT` and `SYSTEM_ROOT` (`init:430-431`), and the installer only `BOOT_DISK` and `BOOT_ROOT` (`installer:310`). So the inherited-value path is latent, a hardening note. A missing dt-id skips the `dtb.img` copy only because `device_trees/.dtb` does not exist (`:28-29`). **Failures are masked:** the remount, the copies and the `dd` are unchecked, `dtb.img` is overwritten in place, and `init` prints *Boot Files Updated.* whatever happened (`init:434-437`). That is F-12.

**The two units, from the rows** (read, never produced):

| Unit | Memory | Loader by `update.sh` | Tree | Observed |
| --- | --- | --- | --- | --- |
| RG35XX SP (the QA handheld, D-QA-027) | LPDDR4; `vdd-dram` 1.1 V (`device-builds.md`, verified 2026-09-05) | DDR4 (`:45-46`) | an `rg35xx-sp` tree: the row says *DDR4 bootloader/device tree* without naming which | L15: 2026-10-16, an in-place update and one reboot with exact hashes (`077197e6cd3e`) |
| RG SP (the maintainer's) | LPDDR3; stock boot0 `dram_type = 7`, then `vdd-dram` 1.2 V | DDR3 (`:42-43`) | `sun50i-h700-anbernic-rg-sp` | L16: 2026-10-12, an in-place update and one reboot |

Which image a unit takes on a fresh card (DDR3 or DDR4) is the parked question #44 (D-WORKFLOW-033), cited, not reopened. The watchdog and ramoops the fork's six configuration lines enable are L29, *never* observed on a board. A deliberate crash on the RG35XX SP is a run asked for by name (D-QA-008), not this slice's.

## The device trees

15 fork-tree sources under `linux/dts/allwinner/` (321 lines; r12, r13). All are compiled into `device_trees` on every H700 image, and `config.xml` lists them for both images.

| Tree | Lines | `#include` | dt-id | Shipped unit / carried by placement |
| --- | ---: | --- | --- | --- |
| `sun50i-h700-anbernic-rg-sp` | 17 | `sun50i-h700-anbernic-rg35xx-sp.dts` (mainline) | `sun50i-h700-anbernic-rg-sp` | **shipped unit**: the RG SP (L16) |
| `sun50i-h700-anbernic-rg35xx-sp-v2-panel` | 15 | `sun50i-h700-anbernic-rg35xx-sp.dts` | `...-rg35xx-sp-v2-panel` | **shipped unit**, one of the RG35XX SP's two trees (the other is mainline's `rg35xx-sp`, dt-id from patch 0154, T41's); L15 does not name which |
| `sun50i-h700-anbernic-rg28xx` | 18 | `...-rg35xx-plus.dts` | `...-rg28xx` | carried by placement |
| `sun50i-h700-anbernic-rg34xx-sp-v2-panel` | 23 | `...-rg35xx-sp.dts` | `...-rg34xx-sp-v2-panel` | carried by placement |
| `sun50i-h700-anbernic-rg34xx-sp` | 23 | `...-rg35xx-sp.dts` | `...-rg34xx-sp` | carried by placement |
| `sun50i-h700-anbernic-rg34xx` | 17 | `...-rg35xx-plus.dts` | `...-rg34xx` | carried by placement |
| `sun50i-h700-anbernic-rg35xx-2024-rev6-panel` | 15 | `...-rg35xx-2024.dts` | `...-rg35xx-2024-rev6-panel` | carried by placement |
| `sun50i-h700-anbernic-rg35xx-h-rev6-panel` | 15 | `...-rg35xx-h.dts` | `...-rg35xx-h-rev6-panel` | carried by placement |
| `sun50i-h700-anbernic-rg35xx-plus-rev6-panel` | 15 | `...-rg35xx-plus.dts` | `...-rg35xx-plus-rev6-panel` | carried by placement |
| `sun50i-h700-anbernic-rg35xx-pro` | 17 | `...-rg35xx-plus.dts` | `...-rg35xx-pro` | carried by placement |
| `sun50i-h700-anbernic-rg40xx-h` | 38 | `...-rg35xx-plus.dts` | `...-rg40xx-h` | carried by placement |
| `sun50i-h700-anbernic-rg40xx-h-v2-panel` | 14 | `sun50i-h700-anbernic-rg40xx-h.dts` (fork sibling) | `...-rg40xx-h-v2-panel` | carried by placement |
| `sun50i-h700-anbernic-rg40xx-v` | 36 | `...-rg35xx-plus.dts` | `...-rg40xx-v` | carried by placement |
| `sun50i-h700-anbernic-rg40xx-v-v2-panel` | 14 | `sun50i-h700-anbernic-rg40xx-v.dts` (fork sibling) | `...-rg40xx-v-v2-panel` | carried by placement |
| `sun50i-h700-anbernic-rgcubexx` | 44 | `...-rg35xx-plus.dts` | `...-rgcubexx` | carried by placement |
| `patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled` | 4,036 | — | — | **disabled at birth, upstream's, 4,036 lines, never applied.** `scripts/unpack:143-159` applies `*.patch` only; added as `.disabled` by `fad6d7d27a` (2026-03-27, *h700: extract dts from patches*). 31 % of the slice's lines |

**Currency of the trees:** read on the host from the M7 lane's patched 7.2 tree (read-only, provenance in § Stage C re-reads). The four mainline include targets (`rg35xx-sp`, `rg35xx-plus`, `rg35xx-2024`, `rg35xx-h`) all exist, and the tree's 19 H700 trees carry 19 distinct dt-ids, so none collides (the seat's G-32). One tree, `rg40xx-v`, declares `compatible = "anbernic,rg40xx-V"` with an uppercase `V` (`:10`), against its dt-id and file name (F-14).

## The runs

`stage-a/runs.sh`, started 08:10:10 UTC; r14b at 08:15:34. Outputs are in `stage-a/`. Every step is read-only.

| Run | Command (abridged) | Exit | Wall | Figure | A FAIL would mean ... |
| --- | --- | ---: | ---: | --- | --- |
| r01 | § 2's block at `2174265e9c` | 0 | 0.46 s | 28 / 12,901; read 8 / 327 / 0; tier 27 / 1; reach 28; written 28 | the membership moved |
| r02 | the conf's line 3 and length | 0 | 0.01 s | `Linux/arm64 7.2.0`; 8,129 | another version or file |
| r03 | `diff` against `651150fc88`'s copy | 0 | 0.01 s | removed 12, added 13 | the base claim is wrong |
| r04 | the fork's edits since `c445081a59` | 0 | 0.01 s | `cbf75c0b06` alone | another fork edit to attribute |
| r05 | upstream's commits since | 0 | 0.00 s | four | another upstream change |
| r06 | the kernel version (`:29-35`) | 0 | 0.00 s | `7.2` for H700 | another version |
| r07 | the pins at both hashes (masked) | 0 | 0.02 s | unchanged | an upstream bump to record |
| r08 | the defconfig diff | 0 | 0.00 s | 20 lines | another difference to read |
| r09 | `update.sh`'s lines | 0 | 0.00 s | `:30-31`, `:36`, `:40`, `:55` | another selection path |
| r10 | `mkimage`'s lines | 0 | 0.00 s | no `dtb.img` | a writer of `dtb.img`: F-04 falls |
| r11 | SUBDEVICES | 0 | 0.00 s | `config.xml` through `xmlstarlet` | the wrapper reads another source |
| r12 | the trees' count | 0 | 0.00 s | 15 | a tree added or dropped |
| r13 | each tree's include and dt-id | 0 | 0.08 s | 13 mainline, 2 sibling | a tree without a dt-id |
| r14 | the history, the brief's bare `--since=2026-06-01` | 0 | 0.03 s | 28 / 1 / 27 (run at 08:10) | — (the delta: a bare date reads the current time of day) |
| **r14b** | **the history, `--since='2026-06-01T00:00:00Z'` (the slice's command, the coordinator's ruling 08:13)** | 0 | 0.03 s | **29 / 1 / 28** | another fork commit, or the count moving |
| r15 | the upstream delta | 0 | 0.01 s | 1 D, 2 M | upstream changing another of the 28 |
| r16 | the removal rule | 0 | 0.01 s | both diffs empty | an edit under `packages/`, `projects/` or `tools/` |

## Findings

| ID | Q | Severity | Category | Where | What |
| --- | --- | --- | --- | --- | --- |
| F-01 | Q4 | Info | currency | § The pins | Every pin in the slice is unchanged at `651150fc88`; the authors' releases are `CANNOT (no network)`, left to `tools/fork-package-freshness` at the RC. atf 2.12.0 is the oldest pin (2025-07-13; the generic recipe is at 2.15.0). |
| F-02 | Q3, Q4 | Low | seam | `projects/ROCKNIX/packages/tools/atf/package.mk:16-21`, `:28` | H700's atf has no `PKG_SHA256` at `8ebaf8daad`, already fixed by T5's E6 (`430abc8f66`, D-WORKFLOW-194) from the `ARM-software` URL. Upstream's `6103571f67` moves the URL to `TrustedFirmware-A` with different checksums for both branches. A merge must take upstream's URL and both checksums together, or the fail-closed fetch refuses (for T25). |
| F-03 | Q2 | Low | standards | `options:9-17`; `device-builds.md:22-23` | The rule's device table (its Arch column says aarch64) gives *crypto-neon-fp-armv8* in its notes, which is the **arm** build's `TARGET_FPU` (`options:17`). The aarch64 build is `TARGET_CPU_FLAGS="+crc+fp+simd"` (`:10`), without `+crypto`. The notes mix the two builds' flag dialects. The hardware's crypto extension is a device fact no row records (`HWCAP` / `/proc/cpuinfo`'s `Features`), and the build policy is the toolchain's effective flags (G-14). A rule-edit lead (separate aarch64 flags, arm flags and observed capability), and an open item to test. |
| F-04 | Q1, Q7 | Low | design | `bootloader/mkimage:45-50`, `:88`; `update.sh:26-32` | `/dtb.img` is named by the fresh card's `extlinux.conf` and written only by `update.sh` on an update. A fresh card needs the runbook's hand step. A design question for the coordinator, with #44 (D-WORKFLOW-033) cited. |
| F-05 | Q5 | Low | coupling | `config/kernel-firmware.dat:1-18`; `linux/package.mk:223-243` | The 13 files the list installs into the root filesystem are the same 13 the recipe builds into the kernel. The kernel reads them from `kernel-firmware`'s build directory (`get_build_dir kernel-firmware`/`.copied-firmware`), so the two are coupled (the seat's G-34). Removing list entries could starve the embed, and a filesystem-only correction is shadowed by the built-in copy until the kernel rebuilds. The installed copies' size and their being unread are not established here. T5's F-17 (the list outside the stamp) is #836's. |
| F-06 | Q2, Q6 | Info | dead-end | `patches/linux/0203-...patch.disabled` | 4,036 lines (31 % of the slice) no build applies; upstream's, disabled at birth. Its removal is #346's class decision. The inventory reads it `shipped` (#1086's shape). |
| F-07 | Q5, Q6 | Info | placement | the 13 non-unit trees | Compiled for every H700 image; used by no unit the fork ships. Carried by placement (D-WORKFLOW-185); removals none. |
| F-08 | Q6 | Info | seam | `filesystem/usr/lib/udev/rules.d/80-clock.rules` | Deleted upstream by `899193e5af` (2026-10-05, *the kernel sets the clock*); settled by the next base merge. |
| F-09 | Q7 | Low | clarity | `options:77-84`; the device directory | `options` does not say why zram and swap are 0 (upstream's ZRAM menu changes the algorithm to `lz4` and adds `THP_DEFRAG`). Nothing in the device directory says which unit takes which loader and tree: `update.sh` decides by voltage and dt-id at update time. |
| F-10 | Q1, Q2 | Info | design | `packages/u-boot-DDR3/package.mk`, `u-boot-DDR4/package.mk` | Two 43-line recipes that differ only in `PKG_NAME` and `PKG_UBOOT_CONFIG`; the wrapper and the stub iterate over them. One parameterised recipe is a design sentence for the coordinator. |
| F-11 | Q7 | Info | erratum | the brief § 1; T11's `02` | `mkimage:18-26` read as H700's: `:22-26` is the SM8550/8650/8750 branch; H700's trees come from `mkimage_dtb:88`. The history count's bare date is the other erratum (the coordinator's ruling, 08:13). |
| F-12 | Q3 | Low | correctness | `bootloader/update.sh:19-31`, `:51-63`; `init:427-440` | From the seat (G-26, G-27), re-read. The remount, the tree and overlay copies, and the loader's `dd` are unchecked (`dd ... &>/dev/null`). `dtb.img` is overwritten in place with no temporary file and rename, so an interrupted copy can leave the card without a usable tree. `device_trees` on `/flash` is assumed to exist (only `overlays` gets `mkdir -p`). `init` prints *Boot Files Updated.* regardless. Upstream-carried; a contained fix (a checked copy to `dtb.img.new` and a rename, checked steps, a non-zero exit) is ours by `bugs-are-agent-first.md` rule 6, verifiable on the host with a fixture `/flash`. Bug or record is the coordinator's call. |
| F-13 | Q2, Q7 | Low | policy | `options:31` | From the seat (G-36). The kernel command line every H700 image boots with carries `systemd.debug_shell=ttyS0`, systemd's root shell on the serial port with no login. It is upstream's since `9f1fab30f6`, unchanged at `651150fc88`, and also on RK3326, RK3399, RK3566, RK3576, RK3588 and S922X. No register row decides it for handhelds (D-QA-053 is GENERIC_X64's guest). A shipping-policy question for the coordinator (#346's class). Whether the UART is reachable on either unit is a device fact. |
| F-14 | Q2 | Info | standards | `linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-v.dts:10` | From the seat (G-33). `compatible = "anbernic,rg40xx-V"`, uppercase, against the dt-id and the file name's `rg40xx-v`. A lead: an exact-match consumer would miss it. Not a unit of ours. |

## Stage C re-reads

The seat's decisive items, re-read by the lane (graded in `04` § Second opinion):
- **G-9 (the fail-safe claim):** `UBOOT_BIN` and `VDD_REG_PATH` are never initialized. No caller sets them (P16), so the inherited path is latent. The claim is narrowed in § The loader and the tree.
- **G-26, G-27:** re-read at `update.sh:19-63` and `init:427-440`. Confirmed as F-12.
- **G-28 (the shell dialect):** `init` runs `sh`, which is bash on the image (ROCKNIX's busybox package relinks `/usr/bin/sh` to `bash`, `projects/ROCKNIX/packages/sysutils/busybox/package.mk:171-174`), so `[[ ]]` and `&>` hold. Refuted.
- **G-8 (the whole fresh-card pipeline):** `mkimage_all` (`functions:384-399`), with no H700 `extlinux` staging. Closed (P15).
- **G-20:** `unpack:140` applies a file named explicitly in `PKG_PATCH_DIRS`, and no recipe names the `.disabled` patch. Narrowed.
- **G-29 and G-32,** read-only from the M7 lane's H700 root `/workspace/repos/rocknix.worktrees/m7-signin-h700-build-20261025-01/build.pixelelated-H700.aarch64`. Its worktree head is `bcc866f1f3`, where `git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/devices/H700 projects/ROCKNIX/packages/linux/package.mk projects/ROCKNIX/packages/tools/atf/package.mk` prints nothing. Read 08:33:52 to 08:34:23 UTC; nothing copied, written or started there.
  - The stub build directory holds both `.bin` files. The sysroot holds `suspend_stub_lpddr3.bin` (18,864 bytes) and `suspend_stub_lpddr4.bin` (18,880 bytes), and the stub `Makefile:34` writes `$(SRC_DIR)/$(OUT)`, so G-29 is refuted.
  - All four include targets exist in `build/linux-7.2/arch/arm64/boot/dts/allwinner/`, and the 19 H700 trees there carry 19 distinct dt-ids, so G-32 is confirmed with no collision.
- **G-33:** `rg40xx-v.dts:10` reads `anbernic,rg40xx-V`. Confirmed (F-14).
- **G-36:** `options:31`; upstream's since `9f1fab30f6`, on seven devices; no register row (F-13).

## Proofs

| Proof | Claim | Evidence | proved: |
| --- | --- | --- | --- |
| P1 | The 28 and their counts | r01; `01` § Scope | tool-run |
| P2 | The configuration's base is upstream's copy, 12 / 13 | r02, r03 | tool-run |
| P3 | Every diff line attributed; the fork's one commit | r04, r05; § The configuration | history |
| P4 | The pins unchanged upstream; their setting commits | r07; `git log -S` | history |
| P5 | atf's missing checksum and the URL seam | atf at both hashes and on T5's branch | tree |
| P6 | `mkimage` never writes `dtb.img`; `extlinux` names it | r10; `mkimage:45-50`, `:88` | tree |
| P7 | `update.sh` writes the loader only for the two voltages | `update.sh:35-57` | tree |
| P8 | The two units' loaders and trees | L15, L16; `device-builds.md:22-23`; `update.sh` | design |
| P9 | 15 trees, their includes and dt-ids | r12, r13 | tree |
| P10 | The `.disabled` patch is never applied | `scripts/unpack:143-159`; `fad6d7d27a` | tree |
| P11 | The firmware list duplicates the recipe's embed | `kernel-firmware.dat`; `package.mk:223-243` | tree |
| P12 | The history count, at an explicit cutoff | r14, r14b | tool-run |
| P13 | The upstream delta | r15 | tool-run |
| P14 | The removal rule held | r16 | tool-run |
| P15 | Nothing in the image step writes `dtb.img` | `functions:384-399` (`mkimage_all`); no H700 `extlinux` staging | tree |
| P16 | No caller sets `UBOOT_BIN` or `VDD_REG_PATH` | `git grep`; `init:430-431`; `installer:310` | tree |
| P17 | The suspend stubs reach the sysroot (G-29 refuted) | the stub `Makefile:34` writes `$(SRC_DIR)/$(OUT)`; both stubs in the M7 root's sysroot | tool-run |
| P18 | The include targets exist and the dt-ids are distinct in the patched 7.2 tree | the M7 root's `build/linux-7.2/arch/arm64/boot/dts/allwinner/` | tool-run |

## Positives

| Check | It would FAIL on ... |
| --- | --- |
| The block (r01) | an inventory change |
| The base diff (r03) | a fork edit beyond `cbf75c0b06`, or a regenerated file |
| The attribution (r04, r05) | a line no commit explains |
| The pins (r07) | an upstream bump |
| `dtb.img` never written by `mkimage` (r10) | a `dtb.img` writer in the image step |
| The fail-safe thresholds (P7) | a branch that writes a loader for a third value |
| The history (r14b) | a second fork commit |
| The removal rule (r16) | a non-empty diff |
