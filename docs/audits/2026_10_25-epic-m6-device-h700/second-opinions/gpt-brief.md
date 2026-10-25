# Second opinion (Phase 4.6), M6 T27: the H700 device of pixelelated/distribution

You are the one independent reviewer for a read-only currency audit of 28 paths at commit `8ebaf8daad`: the H700 device (`projects/ROCKNIX/devices/H700/`) the fork ships for two handhelds, an Anbernic RG35XX SP (LPDDR4) and an RG SP (LPDDR3). The first reader (another lab's model) wrote `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md`, all included below. After them come the context sections, then the files, line-numbered. Every file was passed through a masking `sed` that replaces a value after `key=`, `token=`, `user=`, `pass...=` or `psk=` with `***`; one recipe line (`h700-suspend-stub/package.mk:43`) is masked that way, so treat `***` as an unknown build flag.

The lens is currency, under cost against value. **Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. No one can run anything on the handhelds. A fact only a board can show is a device-facts row, quoted in the context, and is otherwise an open item to test.

Answer these first, in this order:

1. **The pins and the atf seam (`02` § The pins, F-01, F-02).**
   - Are the pins the same at both hashes, as claimed?
   - Is it right that atf's H700 branch has no `PKG_SHA256` at `8ebaf8daad`?
   - Is it right that upstream's `651150fc88` sets a different checksum for both branches with a new URL?
   - Is the merge hazard real: a fetch that refuses a missing or mismatched checksum, a fork checksum computed from the old URL's archive?
   - Which combinations of URL and checksum would fail?
2. **The configuration (`02` § The configuration).** Is every one of the 25 diff lines attributed correctly? Is "upstream's file with a base" right, and the order's *fork-written* an erratum? Is anything in the fork's six lines (`cbf75c0b06`) inconsistent with the rest of the configuration?
3. **The loader and the tree (`02` § The loader and the tree, F-04, F-11).**
   - Trace a fresh card through `scripts/mkimage`, the project `bootloader/mkimage` and `config.xml`: is it right that nothing writes `/dtb.img`?
   - Trace an update through `update.sh`: is the voltage selection fail-safe, as claimed, for any other value, a missing regulator, a failed read, a non-`mmcblk` boot device, or a missing dt-id?
   - Is the first reader's correction of `mkimage:18-26` (F-11) right?
4. **The SIMD flags (F-03).** The rule's table says *crypto-neon-fp-armv8* for an aarch64 image; `options` says `+crc+fp+simd` on aarch64 and `crypto-neon-fp-armv8` on arm. Who is right, and what would settle it?

Then:

5. **Refute or confirm each finding F-01 to F-11** in `02` § Findings: *confirmed*, *narrowed* (say how), or *refuted* (with the line).
6. **What the first reader missed.** Look for:
   - a defect in `update.sh` (it runs as root on a person's handheld, writing to the boot disk);
   - in the u-boot and suspend-stub recipes;
   - in the udev rules;
   - in the trees: a dt-id that collides with another tree's or with a mainline file's, or an include that a 7.2 tree would not have;
   - any reason the firmware duplication (F-05) is not harmless.

**Output:** numbered items `G-1`, `G-2`, ..., each with one line saying *confirmed / narrowed / refuted / new*, the `file:line` evidence, and two to five sentences. Group them under the six headings above. Do not restate the packet, and do not reproduce long code. Keep the whole reply under about 8,000 words.


## The first reader's 02-forward-audit.md (whole)

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
| atf (H700 branch of `projects/ROCKNIX/packages/tools/atf/package.mk:16-21`) | `2.12.0`, **no `PKG_SHA256`**, URL `ARM-software/arm-trusted-firmware` | `2.12.0`, sha256 `d95aaf292792...`, URL `TrustedFirmware-A/trusted-firmware-a` (`6103571f67`, 2026-10-11) | `9f1fab30f6` (2025-07-13, the oldest pin here) | CANNOT (no network); the generic recipe is at 2.15.0 |
| kernel (`projects/ROCKNIX/packages/linux/package.mk:29-35`) | `7.2`, sha256 `f9fef3d14c0d...` | `7.2`, the same | `0c77a91dca` (2026-08-17, *linux: update H700 to kernel 7.2*) | CANNOT (no network) |

**The atf checksum is already known.** T8's sweep and D-WORKFLOW-194 list `atf` 2.12.0 among the five archive versions with no `PKG_SHA256`. T5's E6 gave it `30abf4da07418ad0...` from the `ARM-software` URL (`430abc8f66`, #834, on `feature/m6-build-engine-652`). **The seam:** upstream's fix moves the URL to `TrustedFirmware-A` and sets **different** checksums for both branches. The H700 branch becomes `d95aaf29...`, and the `*)` branch moves from `696b8e53...` to `6b1d5e89...`, because a GitHub archive's bytes carry the repository name. A merge of `next` takes upstream's URL with both of upstream's checksums, or the fetch T5 made fail closed refuses the download (F-02, for T25).

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
- **No line creates `dtb.img`** (r10): a fresh card does not boot until it is activated by hand, as `docs/device-flashing-runbook.md`'s H700 section says.
- *A correction to the brief and T11's `02`:* `mkimage:26`'s `device_trees` copy is the SM8550/8650/8750 branch (`:22-26`); H700's trees come from `mkimage_dtb` (`:88`).

**On an update** (`bootloader/update.sh`, run by the shipped `init` when `update.sh` exists):
- **The tree:** `:21-24` copies `device_trees` and `overlays` to `/flash`. `:26-32` reads `/proc/device-tree/rocknix-dt-id` and copies `device_trees/<dt-id>.dtb` to `/flash/dtb.img`, so the unit keeps the tree it booted, refreshed from the new build.
- **The loader:** `:35-37` finds the regulator named `vdd-dram`. `:40-48` maps `microvolts` 1,200,000 to the DDR3 loader and 1,100,000 to DDR4. `:52-56` `dd`s it at `bs=1K seek=8`.
- **Any other voltage, a missing regulator or a failed read leaves `UBOOT_BIN` empty, and no loader is written** (`:52`): the update keeps the loader already on the card. A missing dt-id skips the `dtb.img` copy (`:29`). Both fail safe.

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

**Currency of the trees:** whether each `#include` target exists in the 7.2 tree is a build fact. The mainline board files the 13 include are added by kernel patches (T41's), named, not re-read.

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
| F-03 | Q2 | Low | standards | `options:9-17`; `device-builds.md:22-23` | The rule's device table says *crypto-neon-fp-armv8* for both H700 units, which is the **arm** side's `TARGET_FPU` (`options:17`). The aarch64 side is `TARGET_CPU_FLAGS="+crc+fp+simd"` (`:10`), without `+crypto`. Whether the H700's cores carry the crypto extension is a device fact no row records (`/proc/cpuinfo`'s `Features`). A rule-edit lead (the table should name the arch), and an open item to test for the flag. |
| F-04 | Q1, Q7 | Low | design | `bootloader/mkimage:45-50`, `:88`; `update.sh:26-32` | `/dtb.img` is named by the fresh card's `extlinux.conf` and written only by `update.sh` on an update. A fresh card needs the runbook's hand step. A design question for the coordinator, with #44 (D-WORKFLOW-033) cited. |
| F-05 | Q5 | Low | efficiency | `config/kernel-firmware.dat:1-18`; `linux/package.mk:223-243` | The 13 files the list installs into the root filesystem are the same 13 the recipe builds into the kernel. Built-in firmware is searched first, so the installed copies are probably not loaded. Small (a few hundred KB); recorded. T5's F-17 (the list outside the stamp) is #836's. |
| F-06 | Q2, Q6 | Info | dead-end | `patches/linux/0203-...patch.disabled` | 4,036 lines (31 % of the slice) no build applies; upstream's, disabled at birth. Its removal is #346's class decision. The inventory reads it `shipped` (#1086's shape). |
| F-07 | Q5, Q6 | Info | placement | the 13 non-unit trees | Compiled for every H700 image; used by no unit the fork ships. Carried by placement (D-WORKFLOW-185); removals none. |
| F-08 | Q6 | Info | seam | `filesystem/usr/lib/udev/rules.d/80-clock.rules` | Deleted upstream by `899193e5af` (2026-10-05, *the kernel sets the clock*); settled by the next base merge. |
| F-09 | Q7 | Low | clarity | `options:77-84`; the device directory | `options` does not say why zram and swap are 0 (upstream's ZRAM menu changes the algorithm to `lz4` and adds `THP_DEFRAG`). Nothing in the device directory says which unit takes which loader and tree: `update.sh` decides by voltage and dt-id at update time. |
| F-10 | Q1, Q2 | Info | design | `packages/u-boot-DDR3/package.mk`, `u-boot-DDR4/package.mk` | Two 43-line recipes that differ only in `PKG_NAME` and `PKG_UBOOT_CONFIG`; the wrapper and the stub iterate over them. One parameterised recipe is a design sentence for the coordinator. |
| F-11 | Q7 | Info | erratum | the brief § 1; T11's `02` | `mkimage:18-26` read as H700's: `:22-26` is the SM8550/8650/8750 branch; H700's trees come from `mkimage_dtb:88`. The history count's bare date is the other erratum (the coordinator's ruling, 08:13). |

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



## The first reader's 03-retrospective.md (whole)

# Retrospective (Phase 3) — M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

## 3.1 What the slice is

The maintainer's two test handhelds, as the tree describes them, in 28 paths:
- the device `options`;
- three u-boot recipes, the wrapper and one per memory type, with two defconfigs;
- an SRAM suspend stub;
- the in-place updater `update.sh`;
- two udev rules;
- a firmware list;
- 15 board trees;
- an 8,129-line kernel configuration;
- one 4,036-line patch nothing applies.

None of it is fork-own by the inventory's tier rule. The fork's own work here is six configuration lines in one commit (`cbf75c0b06`), and the device-facts rows that record the two units booting.

## 3.2 How it stays current

- **Currency comes from upstream.** Every pin is unchanged between `8ebaf8daad` and `651150fc88`. The configuration differs from upstream's copy by the fork's six lines and four upstream commits, a toolchain refresh and the RAID6 benchmark. A base merge carries all four.
- **One pin had no checksum** (atf 2.12.0). T5's E6 fixed that on its branch, and upstream fixed it differently, with a new URL. That is the slice's one merge seam (F-02).
- **The memory type is decided at update time, from the regulator's voltage,** not declared anywhere. A fresh card is activated by hand, because the image step names `/dtb.img` in `extlinux.conf` and never writes it.

## 3.3 What was hard

- **The brief's history count reproduced only at an explicit cutoff.** A bare `--since` date reads the current time of day, and a commit at 08:07 fell out of an 08:10 run. The coordinator ruled the explicit cutoff the slice's command.
- **The brief and T11's `02` read `mkimage:18-26` as H700's whole path.** The device-tree copy at `:26` is a Qualcomm branch.
- **One recipe line matches the credential read filter,** so every recipe read went through the masking `sed`.

## 3.5 The seams

**`config.xml` x the project `mkimage` x `update.sh`.**
- `config.xml` declares the SUBDEVICES (DDR3, DDR4), the trees and `fdt="dtb.img"`.
- `mkimage` writes one image per SUBDEVICE, with the loader at `seek=8`, `extlinux.conf` naming `/dtb.img`, and every tree.
- `update.sh` later writes `/dtb.img` from the running tree's dt-id, and the loader from `vdd-dram`.

The seam is a gap between the first boot and every later one. The first `/dtb.img` is a person's hand step; every later one is the updater's. #44 owns the related question of which image a unit takes.

**The kernel recipe x `kernel-firmware.dat` x the root filesystem.** The recipe builds the H700's 13 firmware files into the kernel (`package.mk:223-243`). The device's list installs the same 13 into the root filesystem. Neither knows of the other. T5's F-17 adds that the list is outside its package's stamp (#836).

**The atf recipe x T5's E6 x upstream.** Three versions of one branch: none (here), `ARM-software` with T5's checksum, and `TrustedFirmware-A` with upstream's. The merge must take one coherent pair.

## 3.6 Time to play

**Nothing, on either number.** No file changed. The loader, the trees and the configuration decide whether and how a unit boots, not how long a launch takes. The RAID6 benchmark upstream disables is boot time, which arrives with the next merge.



## The first reader's 04-analysis.md (whole)

# Analysis — M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

## Executive summary

**The H700 device is current with upstream, and nothing in the 28 behaves wrongly.**
- **The pins:** u-boot `v2026.01`, the suspend stub `712653d11230`, atf 2.12.0 and the kernel 7.2 are all unchanged at `651150fc88`.
- **The configuration is upstream's, with a base:** 12 / 13 lines from upstream's copy. Those are the fork's six settings (D-SYS-002/003/004) and four upstream commits a base merge brings.
- **`update.sh`'s memory selection fails safe:** any voltage but the two known writes no loader.

The findings are:
- a merge seam on atf's checksum and URL (F-02, for T25);
- the rule's SIMD column, which describes the arm FPU for an aarch64 build (F-03);
- the fresh card's hand-activated `/dtb.img` (F-04, a design question with #44);
- firmware files both built in and installed (F-05);
- dispositions for the `.disabled` patch, 13 placement-carried trees and a rule deleted upstream (F-06 to F-08);
- two clarity notes and an erratum (F-09 to F-11).

No `bug`. Removals none (D-WORKFLOW-209). The seat's grading is at stage C.

## Acceptance-criteria scorecard

| Criterion (#674) | State | Evidence |
| --- | --- | --- |
| `00` to `05` | `05` at stage D | this folder |
| The lint | at stage C and at close | — |
| The seat | at stage C | `second-opinions/` |
| The punch-list issue | stage D | — |
| `reviewed-at` / `fixed-at`; the empty diffs | `ed7fd0ea50`; r16 empty | `02` § The runs |
| `01` § Scope | complete | `01` |
| `## Coverage` 28 | 28 | `02` |
| § The pins | six rows | `02` |
| § The configuration | 12 / 13 attributed | `02` |
| § The loader and the tree | written | `02` |
| § The device trees | 15 rows and the `.disabled` row | `02` |
| § The runs | 17 | `02` |
| `00` clean | so far | `00` |
| `04` Q4, Q2, Q3, Q6, § Second opinion | below; the second opinion at C | this file |
| `proved:`; `question:` | 14 proofs; the items at D | `02`, `05` |
| The retro; the checkers | stages G, H | — |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| A merge takes upstream's atf URL with T5's checksum, or the reverse | Medium at the next base merge | every H700 build refuses its atf fetch | F-02, for T25 |
| A fresh card is flashed without the hand step | Medium for anyone new | the card does not boot | F-04; the runbook covers it |
| A third memory type or a failed regulator read | Low | no loader update: the card keeps its old loader | `update.sh:52`; fails safe |
| A firmware change in the list is not rebuilt | High until #836 lands | the image keeps the old list | T5's F-17 |

## Coverage boundary

- **Read:** all 28 at `8ebaf8daad`, with the 15 trees whole and the configuration by diff against upstream's copy.
- **Read beyond the 28,** for the questions: the project `bootloader/mkimage`, `config.xml`'s H700 lists, `distributions/ROCKNIX/config/functions:224`, `scripts/unpack:143-159`, the ROCKNIX `atf` and `linux` recipes, `device-builds.md`'s device table, and device-facts L15, L16 and L29. T5's atf commit was read on `feature/m6-build-engine-652` with `git show`.
- **Not done:**
  - no network, so the authors' releases are `CANNOT`;
  - no build, so whether each tree's `#include` exists at 7.2 is a build fact;
  - nothing on a unit, so the RG35XX SP's tree name, the cores' crypto extension, and the watchdog and ramoops on a board are open items to test or rows (L29).
- **Not this slice's:** the 32 live kernel patches and the ramoops patch (T41, #688), the u-boot patches (T40's `patches-and-configs`), the H700 quirks (T29, #676), and the overlay source (T11).

## Second opinion

At stage C: one seat, GPT-6 Astra at `max`, a probe first, then one refutation pass. Every item is graded here.

## Finding Verification

| Finding | Re-read | Verdict |
| --- | --- | --- |
| F-01 | r07; `git log -S` for each pin | stands |
| F-02 | `atf/package.mk:16-28` at `8ebaf8daad`, at `651150fc88` and on T5's branch (`430abc8f66`); D-WORKFLOW-194 | stands; cited, not re-filed |
| F-03 | `options:9-17`; `device-builds.md:22-23` | stands |
| F-04 | `mkimage:45-50`, `:88`; r10; `update.sh:26-32` | stands |
| F-05 | `kernel-firmware.dat`; `package.mk:223-243` | stands |
| F-06 | `scripts/unpack:143-159`; `fad6d7d27a` | stands |
| F-07 | `config.xml`'s lists; r13 | stands |
| F-08 | r15; `899193e5af` | stands |
| F-09 | `options:77-84` | stands |
| F-10 | the two recipes' diff (two lines) | stands |
| F-11 | `mkimage:18-30` | stands |

## Renovation face

### Q1 Modernize

- **The three u-boot recipes against one parameterised recipe (F-10).** DDR3 and DDR4 differ only in `PKG_NAME` and `PKG_UBOOT_CONFIG`; the wrapper loops over `${SUBDEVICES}`; the stub reads each recipe's defconfig. *The design sentence, deferred to the coordinator:* a single recipe taking the memory type from the SUBDEVICE would remove the duplicate, but the wrapper, the stub and `config.xml` name the two packages, so it is upstream's to change, not a fork edit.
- **`update.sh`'s `vdd-dram` selection against a declared memory type.** The type is inferred at update time from the regulator (`:35-48`), and fails safe. A declared type would need a per-unit record the image does not have.
- **`/dtb.img` on a fresh card (F-04).** `mkimage` names it and never writes it; the runbook's hand step activates it. *The design sentence, for the coordinator:* the image step could write a default `/dtb.img` per SUBDEVICE, but which tree a unit needs is a fact about the unit, which is the question #44 (D-WORKFLOW-033) parks. Cited, not reopened.

### Q2 Standards

- **`TARGET_CPU_FLAGS` against the rule's table (F-03).** `.claude/rules/device-builds.md:22-23` says *cortex-a53, crypto-neon-fp-armv8* for both units. `options:10` reads `TARGET_CPU_FLAGS="+crc+fp+simd"` on aarch64, and `options:17` reads `TARGET_FPU="crypto-neon-fp-armv8"` on arm. **The table quotes the arm FPU for an aarch64 image, so the table is wrong in what it describes.** Whether the aarch64 flag should add `+crypto` depends on whether the cores carry the extension, which no row records. This is a rule-edit lead for the coordinator and an open item to test.
- **The `.disabled` patch (F-06):** a file the build never reads, 31 % of the slice.
- **The configuration's `tier_note: fork-written`:** the inventory's reading of a file the fork touched once (`cbf75c0b06`). Cited, not re-tiered (T10's).
- **The identical u-boot bodies (F-10)** and the identical patch pairs (T41's, outside the slice).

### Q3 Bugs

- **`update.sh`'s thresholds are not a bug.** At a voltage that is neither 1,200,000 nor 1,100,000 µV, or with no `vdd-dram` regulator or an unreadable `microvolts`, `UBOOT_BIN` stays empty and `:52` writes nothing. The unit keeps the loader already on its card. A missing dt-id skips the `dtb.img` copy (`:29`). No input makes it write a loader it should not. `Already written:` the two units' cards carry the loaders and trees L15 and L16 record; nothing written by this script is wrong, so nothing is inherited.
- **T5's F-17** (a `kernel-firmware.dat` change does not move the stamp): #836's, cited, not re-filed.
- **atf's missing checksum (F-02):** fixed on T5's branch (D-WORKFLOW-194); the merge seam is recorded.

### Q4 Package currency

The pin table (`02` § The pins), with its verdicts:

| Unit | Verdict |
| --- | --- |
| u-boot-DDR3, u-boot-DDR4 `v2026.01` | current with upstream; set 2026-06-08; the author's release `CANNOT (no network)` |
| the wrapper `1.0` | no source |
| h700-suspend-stub `712653d11230` | current with upstream; set 2026-09-17 |
| atf 2.12.0 (H700) | current with upstream's pin; the oldest here (2025-07-13); the generic recipe is at 2.15.0; the checksum seam is F-02 |
| kernel 7.2 | current with upstream; set 2026-08-17 |
| the configuration | 12 / 13 from upstream's copy: the fork's six (`cbf75c0b06`) and upstream's four (`c0980b2b71`, `5f56cd5150`, `6fbefc45c6`, `dcafa74090`) |
| the trees | the include targets are mainline board files; their presence at 7.2 is a build fact, and the patches that add them are T41's |

`tools/fork-package-freshness` is the RC's check for the authors' releases (D-WORKFLOW-024), named, not run.

### Q5 Efficiency

- **The configuration's size against upstream's copy:** equal but for 25 lines.
- **The 15 trees against the two units:** 2 are a shipped unit's; 13 are other H700 handhelds', compiled into every image and carried by placement (F-07). Removals none.
- **The firmware list against `CONFIG_EXTRA_FIRMWARE`:** the same 13 files both ways, no misses. The root-filesystem copies duplicate the built-in ones (F-05).

### Q6 Dead ends

| Unit | Disposition |
| --- | --- |
| `0203-...patch.disabled` | disabled at birth, upstream's; its removal is #346's class decision |
| the 13 non-unit trees | carried by placement (D-WORKFLOW-185) |
| `80-clock.rules` | gone upstream (`899193e5af`): settled by the next base merge |
| `kernel-firmware.dat`'s root-filesystem copies | recorded (F-05); the list is upstream's |
| everything else | live |

### Q7 Clarity and structure

- **Which unit boots which loader and tree:** a reader of the device directory cannot tell. `update.sh` decides by voltage and dt-id at update time; the rows and the rule's table say it for the two units (F-09).
- **Where `/dtb.img` comes from:** `update.sh` on an update, the runbook on a fresh card (F-04).
- **`options`** does not say why zram and swap are 0 (F-09).
- **The `vm-first` answer for every device fact:** L15, L16 and L29, read; nothing new asked of a unit.

## Instruction File Recommendations

Proposals for the coordinator:
1. **`device-builds.md`'s device table** names the arch its SIMD column describes. For H700 that means aarch64 `+crc+fp+simd`, with the arm build's `crypto-neon-fp-armv8` as a separate value (F-03).
2. **For briefs and acceptance scripts:** a history count uses an explicit cutoff (`--since='YYYY-MM-DDT00:00:00Z'`), never a bare date (the friction line of 08:11).

## Quality self-check

- **Every figure comes from a timed run** (r01 to r16, r14b), and every finding is re-read at its lines.
- **Every recipe read was masked;** `h700-suspend-stub/package.mk:43` appears nowhere unmasked.
- **What would change the verdicts:**
  - an upstream bump between the two hashes;
  - a writer of `dtb.img` in the image step;
  - a branch in `update.sh` that writes a loader for a third value;
  - a row naming the RG35XX SP's tree;
  - a second fork commit on the configuration.



## Context 1: docs/reviews/order.md § T27

```text
### T27. devices: the H700 device (RG35XX SP, RG SP)

- **id**: `device-h700`; **kind**: currency; **lens**: cost against value
- **why here**: the maintainer's test handhelds; options, device packages (u-boot DDR3/DDR4, the suspend stub), device trees and kernel configuration; its fork-written kernel configuration (8,129 lines) is read here as a diff against its base (plan § 2)
- **paths** (28 paths, 12,901 lines, 327 read, of which 0 fork-own; 8,129 patch and config lines; reach shipped 28): areas `devices`; globs `projects/ROCKNIX/devices/H700/**` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/devices/H700/linux/*.conf`
- **read before**: none
- **depth**: Independent -- an ordinary device slice
- **interacting subsystems** (read-only context): the H700 quirks (`os-device-quirks`); the kernel patches (patches slices); `docs/device-flashing-runbook.md`; the kernel recipe and project boot files (`device-generic-x64-and-kernel`); the fork-written H700 kernel patch (`patches-shipped-kernel`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

```


## Context 2: the brief's § 2 and § 4

```text
## 2. Scope

**28 paths, 12,901 lines; 8 read (shell 2 / 147, udev 2 / 3, recipe 4 /
177 -- 327 lines, 0 fork-own); the 15 device-tree sources (321 lines) are
not counted as read by the survey's language rule but are read here all
the same; upstream-carried 27 paths / 4,772 lines, vendor-carried 1 /
8,129 (the kernel configuration, `tier_note: fork-written`, area
`patches-and-configs`); reach shipped 28.** The membership is `slices.json`
k 27's rule on `inventory.json` at `2174265e9c`: area `devices` with reach
`shipped` under `projects/ROCKNIX/devices/H700/**`, **plus** area
`patches-and-configs` under `projects/ROCKNIX/devices/H700/linux/*.conf`.
The block (the same translator as T11's; its `{a,b}` is unused here):

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,re,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
def rx(g):
    g=re.sub(r"\{([^}]*)\}", lambda m: "(?:"+"|".join(m.group(1).split(","))+")", g)
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i] in "(|)?:": out+=g[i]; i+=1
        else: out+=re.escape(g[i]); i+=1
    return re.compile("^"+out+"$")
A=rx("projects/ROCKNIX/devices/H700/**"); B=rx("projects/ROCKNIX/devices/H700/linux/*.conf")
t=[r for r in rows if (r["area"]=="devices" and r["reach"]=="shipped" and A.match(r["path"])) or (r["area"]=="patches-and-configs" and B.match(r["path"]))]
READ={"shell","udev","recipe"}
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t))
print("read",sum(1 for r in t if (r.get("language") or "") in READ),sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ),"fork-own",sum(r["lines"] or 0 for r in t if r["tier"]=="fork-own"))
print("tier",dict(collections.Counter(r["tier"] for r in t)),"reach",dict(collections.Counter(r["reach"] for r in t)))
print("language",dict(collections.Counter((r.get("language") or "none") for r in t)))
import os; os.makedirs(".qa-scratch/t27", exist_ok=True)
open(".qa-scratch/t27/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=*** r:r["path"])))
print("written", len(t), ".qa-scratch/t27/paths.txt")'
# (the sorted(..., key=*** above is Python's keyword, not a credential: a reader applying the read filter to this block drops that line and sees nothing written -- run the block raw)
# paths 28 lines 12901
# read 8 327 fork-own 0
# tier {'upstream-carried': 27, 'vendor-carried': 1} reach {'shipped': 28}
# language {'shell': 2, 'other': 2, 'udev': 2, 'devicetree': 15, 'kernel-config': 1, 'recipe': 4, 'none': 2}
# written 28 .qa-scratch/t27/paths.txt
```

A different count is a delta to record with the command, not a reason to
stop. (The two `none` rows are the defconfigs, the two `other` rows
`kernel-firmware.dat` and the `.disabled` patch.)

**The device, at `8ebaf8daad`.** `options` (84 lines): aarch64
`TARGET_CPU=cortex-a53`, `TARGET_CPU_FLAGS="+crc+fp+simd"` (no `+crypto`;
the `arm` side carries `TARGET_FPU=crypto-neon-fp-armv8`, and
`device-builds.md`'s device table says *crypto-neon-fp-armv8* for H700 --
say which is read before any SIMD claim), `HW_CPU="Allwinner H700"`,
`KERNEL_TARGET=Image`, `BOOTLOADER="u-boot"` (`:34`), `UBOOT_FIRMWARE+=" atf"`,
`ATF_PLATFORM="sun50i_h616"`, `MALI_FAMILY=g31` / panfrost,
`BATTERYPLUS_SUPPORT=yes`, `DISPLAYSERVER=wl`, `ROCKNIX_DEVICE_TREE_OVERLAYS="yes"`,
`ZRAM_SWAP_SIZE=0`, `SWAP_FILE_SIZE=0`; **no `SUBDEVICES` line** -- the
SUBDEVICES are derived in `distributions/ROCKNIX/config/functions:224` from
`projects/ROCKNIX/config.xml` (`//rocknix/H700/*[@mkimage_options]`,
upstream `2e825afd0c` 2026-06-08 "h700: subdevices"), both outside the
slice, so the u-boot wrapper is not dead.

**u-boot, three recipes.** `packages/u-boot/package.mk` (36 lines,
`PKG_VERSION "1.0"`, no URL) depends on `u-boot-${SUBDEVICE}` and copies
each sysroot's `u-boot-sunxi-with-spl.bin` to
`usr/share/bootloader/H700_${SUBDEVICE}_u-boot-sunxi-with-spl.bin`;
`u-boot-DDR3` and `u-boot-DDR4` (43 lines each, `v2026.01`, the same
sha) differ only in `PKG_NAME` and `PKG_UBOOT_CONFIG`
(`anbernic_rg35xx_h700_lpddr3_defconfig` / `lpddr4`); the two defconfigs
(35 lines) differ in 10 lines a side (§ 5's count prints 20), `CONFIG_SUNXI_DRAM_H616_LPDDR3` /
`LPDDR4` and `CONFIG_AXP_DCDC3_VOLT` 1200 / 1100; the u-boot patch pairs
(0001 dram, 0002 axp717 charge-only boot) are byte-identical between the
two and **outside the slice** (patches-and-configs). The suspend stub
(`h700-suspend-stub/package.mk`, 55 lines, pin `712653d11230...`) builds
one stub per memory type from each defconfig; **its line 43 matches the
credential read filter** (`key=*** in a build flag), so a filtered read shows
54 lines -- read that line with the masking `sed`, never quote it raw.

**Device trees.** 15 fork-tree DTS under `linux/dts/allwinner/` (14 to 44
lines), 13 of them `#include`-ing a mainline board file and the two
`rg40xx-*-v2-panel` trees including their fork-tree siblings, each carrying
`rocknix-dt-id`: the RG SP is `sun50i-h700-anbernic-rg-sp` (model
"Anbernic RG-SP", `anbernic,rg34xx-sp-v2-panel`, added `fc89fab1a2`
2026-08-04); the RG35XX SP is mainline's `sun50i-h700-anbernic-rg35xx-sp`
(its dt-id from kernel patch 0154, T41's) or `-rg35xx-sp-v2-panel` here.
The kernel recipe copies every built dtb to `usr/share/bootloader/device_trees`
(`package.mk:419-431`); `bootloader/update.sh:21-32` copies them to
`/flash` and writes `/dtb.img` from `/proc/device-tree/rocknix-dt-id`;
`:34-49` reads the `vdd-dram` regulator (1,200,000 µV -> the DDR3
loader, 1,100,000 -> DDR4) and `:55` `dd`s it at `bs=1K seek=8`. The project
`mkimage` never creates `dtb.img`: a fresh card does not boot until it is
activated by hand (`docs/device-flashing-runbook.md`, the H700 section).

**The kernel configuration has a base, and it is upstream's own copy.**
`linux/linux.aarch64.conf`: 8,129 lines, header `# Linux/arm64 7.2.0
Kernel Configuration`, 2,104 `=` lines and 4,189 `is not set`; the override
recipe builds **`7.2`** for `H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750`
(`package.mk:29-35`), `listnewconfig` then `yes "" | kernel_make oldconfig`
at `:306-316`. Added by upstream (`9f1fab30f6` 2025-07-13, ROCKNIX Team,
"projects: add modifications for ROCKNIX", +7,773); 58 non-merge commits in all (64 with merges), 13
since 2026-06-01 (12 upstream's, 1 the fork's). **The fork's
edits are six lines in one commit**, `cbf75c0b06` (+6/-5: `WATCHDOG_SYSFS`,
`PSTORE_CONSOLE`, `PSTORE_RAM`, `SOFTLOCKUP_DETECTOR`, `DETECT_HUNG_TASK`
`=y`; `DEFAULT_HUNG_TASK_TIMEOUT=120` -- D-SYS-002/003/004). Against
`651150fc88`'s own copy the diff is **12 removed / 13 added** (the fork's
six and upstream's four commits since the merge base: `c0980b2b71`,
`5f56cd5150`, `6fbefc45c6`, `dcafa74090` 2026-10-22); against the other
confs in the tree it is far (RK3326 898 / 1,809; RK3566 1,518 / 1,908;
LibreELEC's Allwinner 1,871 / 1,953; SM8550 1,585 / 1,106). So plan § 2's
*one diff per kernel config against its base* is, here, the diff against
upstream's copy, with the fork's six lines named; T11's "no base" shape
does not apply, and the order's *fork-written* is an erratum (the
inventory's `tier_note` says it because the fork touched it).

**A third of the slice's lines is a patch nothing applies.**
`patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled`
(4,036 lines, 31 % of 12,901) is inside T27 only because `.disabled`
escapes the `*.patch` globs (`scripts/unpack:143-159` apply `*.patch`);
born disabled (`fad6d7d27a`). The 32 live H700 kernel patches (8,616 lines)
are T41's; the fork-written ramoops patch
`0950-arm64-dts-allwinner-h616-ramoops-reserved-memory.patch` (38 lines,
`From: ROCKNIX fork`, `cbf75c0b06`, absent upstream) is tiered
`vendor-carried` with `tier_note: fork-written` -- marked wrongly for anyone
counting fork-own, outside this slice, while the six configuration lines
that enable it are inside: cite it, do not re-tier it (the inventory is
T10's).

**What `upstream/next` (`651150fc88`) already changes:** `D
filesystem/usr/lib/udev/rules.d/80-clock.rules` (`899193e5af` 2026-10-05,
"systemd: drop the hwclock udev rules, the kernel sets the clock"), `M
options` (+4/-1 by two commits of 2026-10-03: `e1b7d1f82f`, the ES ZRAM
menu, and `dc14669f69`, the systemd THP policy), `M
linux.aarch64.conf` (the four commits above); the `.disabled` patch and the
rest unchanged; the kernel version 7.2, u-boot `v2026.01`, the suspend
stub's pin unchanged upstream. Upstream's linux recipe (18+/35-) adds
`rocknix-joypad` to `PKG_PATCH_DIRS` for `RK3326|RK3399|S922X|H700`.
**History since 2026-06-01 over the 28:** 29 non-merge commits, 1 the
fork's (`cbf75c0b06`), 28 upstream's (options 2, bootloader 1, config 1,
filesystem 1, dts 6, conf 13, suspend-stub 3, u-boot-DDR3/DDR4 5 each,
the wrapper 4, the `.disabled` patch 0).


## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`design`); the lens is currency, so Q4 leads:

- **Q4 Package currency -- the lead question.** For each pinned unit
  (u-boot `v2026.01` with its sha; the suspend stub's commit; atf, read
  from the recipe that pins it for H700; the kernel `7.2` and its sha at
  `package.mk:29-35`): the pin at `8ebaf8daad`, the pin at `651150fc88`
  (unchanged, by the research), the pin's date from the recipe or the
  upstream commit that set it, and **`CANNOT (no network)`** for the
  author's current release -- that check is `tools/fork-package-freshness`'s
  at the RC (D-WORKFLOW-024) and is named, not run. The configuration's
  currency is its 12 / 13 diff against upstream's copy, each line
  attributed to its commit. The DTS currency: which of the 15 boards has a
  mainline board file at the kernel the recipe builds (`#include` targets
  present in the 7.2 tree is a build fact; here, the include lines and
  the patches that add them, T41's, are named).
- **Q1 Modernize.** The three u-boot recipes against one parameterised
  recipe (a design sentence, deferred to the coordinator; no edit);
  `update.sh`'s `vdd-dram` selection against a declared memory type;
  `/dtb.img` written by `update.sh` on an update but never by `mkimage`
  on a fresh card (the runbook's hand step): a design question for the
  coordinator, with D-WORKFLOW-033 (#44) cited, not reopened.
- **Q2 Standards.** The `.disabled` patch (a file the build never reads,
  31 % of the slice); the `tier_note: fork-written` on a file the fork
  touched once (an inventory reading, cited, not re-tiered); the two
  identical u-boot patch pairs (T41's) and the identical recipe bodies;
  `TARGET_CPU_FLAGS` without `+crypto` against the rule's table (which is
  wrong, the table or the flag? -- a finding with both lines quoted, a
  rule-edit lead for the coordinator if the table).
- **Q3 Bugs.** T5's F-17 (a `kernel-firmware.dat` change does not move the
  stamp): cite #836's state, do not re-file. `update.sh`'s regulator
  thresholds (`:34-49`): what happens at a voltage that is neither
  (a third memory type, a regulator read that fails) -- read, and a `bug`
  with its trace only if the script writes a loader it should not; its
  `Already written:` names the two units' cards (device-facts rows L15,
  L16) and argues nothing inherited or names the migration. Nothing runs
  on a unit.
- **Q5 Efficiency.** The configuration's size against upstream's copy
  (equal but for 25 lines); the 15 DTS against the two shipped units (13
  are other H700 handhelds' -- shipped by placement, used by no unit the
  fork ships: a disposition each, not a removal, D-WORKFLOW-185); the
  firmware `kernel-firmware.dat` (18 lines) against `CONFIG_EXTRA_FIRMWARE`'s
  list in the recipe (duplicates, misses).
- **Q6 Dead ends.** The `.disabled` patch (disposition: *disabled at
  birth, upstream's; its removal is #346's class decision*); the 13 DTS of
  unshipped H700 boards (*carried by placement*); `80-clock.rules` (gone
  upstream: *settled by the next base merge*). Removals none.
- **Q7 Clarity and structure.** Can a reader tell from the device
  directory which unit boots which loader and which tree, and where
  `/dtb.img` comes from? Does `options` say why `ZRAM_SWAP_SIZE=0`
  (upstream's ZRAM menu change moves it)? The `vm-first` answer for every
  device fact: the three rows named, nothing new asked of a unit.

```


## Context 3: the register rows

```text
| D-SYS-002 | 2026-09-10 | **systemd arms the hardware watchdog at 15 s and leaves the reboot watchdog off.** 15 s because the Allwinner watchdog counts to 16 at most and a longer figure is refused by the driver, which would leave systemd running with no watchdog; a kernel that has stopped scheduling is reset within 15 s instead of staying frozen until the power button. `RebootWatchdogSec=off` because the same ceiling would reset a device mid-way through a slow sync to the card at shutdown -- the corruption this is meant to prevent -- and systemd disarms the runtime watchdog when it hands over to shutdown, so a hung shutdown is as it was. Revisit when `WATCHDOG_SYSFS` reports a longer ceiling on other families. | #104 |

| D-SYS-003 | 2026-09-10 | **A soft lockup or a hung task panics, and a panic reboots after ten seconds; an oops does not.** `softlockup_panic=1`, `hung_task_panic=1`, `panic=10` in `/usr/lib/sysctl.d/hang-policy.conf` (image-level, so it applies on the first boot after an update and a device's own `/storage/.config/sysctl.d` still wins). `panic_on_oops` stays 0: with the journal persistent an oops is captured anyway, and the player keeps their session. | #104 |

| D-SYS-004 | 2026-09-10 | **ramoops for every H700 board, from the SoC dtsi, at `0x4F000000`.** One kernel patch on `sun50i-h616.dtsi` rather than fifteen board files. The address is RAM on every H700 (all carry at least 1 GiB from `0x40000000`) and nothing in the U-Boot chain touches it: kernel at `0x40080000` (~32 MiB), U-Boot proper at `0x4A000000`, FDT at `0x4FA00000`, SPL stack at `0x4FE00000`, ramdisk at `0x4FF00000`; the top of RAM is avoided because U-Boot relocates itself there. 512 KiB console, four 128 KiB dumps, oopses and panics. Not something mainline would take in a SoC dtsi; the fork carries it. The VM cannot prove DRAM retention across the SoC's reset -- that is a device test, with a yes. | #104 |

| D-QA-027 | 2026-09-17 | **The RG35XX SP is the dedicated QA handheld from here on: it holds no personal saves or ROMs, signs in only to QA accounts, and may be left plugged in as a bench device, headless if that can be arranged; the RG SP stays the maintainer's own device under D-QA-015.** Settles D-QA-016 (#131). Maintainer: *"With 131, we'll make the RG35XX SP a dedicated QA handheld going forward, and I can plug that in. I can even look at how we might be able to leave it plugged in to make it a headless device, or at least something that's always running as a bench device."* Consequences: the deliberate-crash proof for ramoops (#104's last box) and any per-device proof that needs a real panel, a real Wi-Fi driver or a real provider runs there first; the QA cloud accounts (#131 box 2, #133) are created for it; the runner gains a device target beside the pair. It is flashed from the fork's images and seeded like `seed-device`, never restored from the maintainer's backups. | #131; #104; #133 |

| D-WORKFLOW-033 | 2026-09-24 | **#44 (which H700 image, DDR3 or DDR4) waits until after the release candidate.** Maintainer, 2026-09-24: *"Since this isn't directly related to saves, this might be an issue. We wait to tackle until after the release candidate."* Their questions go first when it is picked up: whether a single-image route adds complexity for other developers, whether it changes the fresh-install flow or the upgrade path, and what it does to the build; the documentation route (the regulator check in the release notes and on rocknix.org) changes none of those. | #44 |

| D-WORKFLOW-100 | 2026-09-30 | **The mandatory migration device for 0.0.1 is the RG35XX SP (H700), the fork's dedicated test device: #344's P2b builds its image first and P3's migration contract (RC2 to 0.0.1 with the player's state intact, by the RC2 client unaided or by the documented manual path) is rehearsed on it before any other target is attached.** Maintainer, 2026-09-30: *"I agree that the migration device is going to be the RG35XX SP. That's our dedicated testing device and a good place to start."* Settles the open half of D-WORKFLOW-092. | #344; D-WORKFLOW-092; D-WORKFLOW-047 |

| D-WORKFLOW-114 | 2026-10-01 | **0.0.1's support matrix is the Retroid Pocket Nova (SM8550) and the two H700 boards (the RG35XX SP, the migration device, and the RG SP), with the GENERIC_X64 guest for QA; the RG353M (RK3566) waits -- not built for 0.0.1, its row kept in the matrix as deferred -- and the next board after these is a 16:9 device the maintainer has yet to buy.** Refines D-WORKFLOW-092 (which named SM8550, H700 and RK3566). Read from the device tonight: the Nova's panel is 1280x960, so the matrix holds two panel sizes, 640x480 and 1280x960, both 4:3; the 16:9 board would be the first other shape. Maintainer, 2026-10-01: *"I think we can wait on the RG353M for now. That device isn't getting much use from me, and I'll probably be using the Retroid Pocket Nova more. I think focusing on that device and the H700 devices is a good place to start. Following that, we can look to expand [...] I'm more interested in moving on to a 16:9 device following that, which I'd have to get."* | #344 (owner question 5, P4's asset set), `docs/rasteratops/support-matrix.md`; refines D-WORKFLOW-092, D-WORKFLOW-100 |

| D-WORKFLOW-123 | 2026-10-01 | **Identity default for 0.0.1: every persisted path, partition label, hostname, share name, mount point, unit name and machine-readable identifier keeps its RC2 value, and only consumers the P0 sweep classified as display text change; `DISTRO=ROCKNIX` and `distributions/ROCKNIX/` are retained; relabelling belongs to a later clean-install-only release whose init accepts both labels. Two exceptions, each its own row: the cloud folder (D-CLOUD-158/159) and the chassis declaration (D-NET-016, a file added, no identifier changed).** #344's drafted row 12, approved as a batch. Maintainer, 2026-10-01: *"I think your plan for the 14 rows is good to start. We can always revise that as we go on, as long as we keep track."* | #344 row 12; `docs/rasteratops/p0-sweep.md` |

| D-WORKFLOW-150 | 2026-10-07 | **Build and verify H700 first, then SM8550, from the qualified pixelelated product inputs.** Maintainer explicitly authorizes both builds and names SM8550 as the next target after H700. Run H700 arm compatibility prerequisites, reassess capacity for aarch64 firmware, verify the H700 artifacts, then reassess capacity and build SM8550. Use frozen build worktrees and the standard actively supervised watcher. Compilation of the second target does not await physical testing of the first; D-WORKFLOW-100/120's artifact attachment, physical-action and publication gates remain. No additional cleanup, hardware purchase or RAID conversion is inferred. | #492; #491; #493; milestone7 ordered body |

| D-WORKFLOW-185 | 2026-10-23 | **The renovation order's shipped-device set is H700 and SM8550. GENERIC_X64 is the test image: built, read as the VM every proof runs on (T19), never shipped. Every other target the fork can build (RK3566, RK3326, RK3399, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750, AMD64) is a row in the unshipped tables, not a device slice; `device-builds.md` § Our devices is a hardware inventory, not the shipping list. RK3566 and RK3326 are the recorded first widening: on rocknix.org's device pages they are the two widest targets after the shipped pair (15 and 13 models against H700's 11 and SM8550's 10; SM8250 3, S922X 2, the other six 1 each, RK3576 none), the maintainer owns their test units (RG353M, RG351M), and upstream's release 20261001 publishes two image variants for each (RK3326 a and b, RK3566 Generic and Specific) as it does for H700 (DDR3 and DDR4). Opening either is a device build with its own issue (D-WORKFLOW-132), and the tables re-derive then.** Put by the coordinator lane (D-WORKFLOW-183) as P1's first pass-7 question, from the three-seat review's finding 12 (`device-builds.md`'s five against plan § 5's eight). Maintainer, 2026-10-22: *"Now we're focused on shipping the H700-based builds and the SM8550-based builds. We have not focused on any of the Rockchip builds or the RG353M or RG351M. The fork uses our VM image only for testing."* Then, the same exchange: *"You could check the ROCKNIX GitHub page for the devices they support and see what additional types might give us the most coverage in terms of chips being used by multiple devices."* The read (upstream's README names no device; rocknix.org's 53 device pages, each naming its image target; the 20261001 release's asset list) was put back as the table above with two options, and the maintainer, 2026-10-23: *"I think we should start with what we've done here with H700 and SM8550."* Consequence for the order (#641): T22 `device-rockchip-shipped` dissolves into T17's rows, its kernel patches and configurations move from T42 to T44 and the other patches only those two apply from T43 to T44, `reach` for RK3566 and RK3326 becomes `unshipped`, T23's run-time model derivation uses the shipped pair and the VM; plan § 5's Devices row is corrected in the same change. | #346; #641; D-WORKFLOW-184; D-WORKFLOW-132; D-WORKFLOW-183; `docs/reviews/plan-for-the-plan.md` § 5; `.claude/rules/device-builds.md` § Our devices; https://rocknix.org/devices/; https://github.com/ROCKNIX/distribution/releases/tag/20261001 |

| D-WORKFLOW-187 | 2026-10-23 | **The renovation gates no release. M6 is an audit, assessment and renovation of the codebase: it decides what is read, in what order and at what depth, never what ships or when. D-WORKFLOW-102's release clause is retired (`0.1` waiting on Tier 1's findings on the launch, control and state slice and on any known security, state-preservation or launch-path finding from any tier); its placed, progressive review stands. A finding that is a defect is filed as a bug the session it is found (D-WORKFLOW-132) and holds or clears a release the way every bug does (D-QA-051, `tools/rc-preflight`), owned by the release's milestone, never by a slice. The order carries no release-gate column; T1 and T2 keep their place on the order's own lenses, and the one prerequisite that stands is a reading order, not a gate: the launch-path slices are read before #336 Step 1 replaces what they read. The drift re-review runs at the renovation's own cadence (every slice close), not as a release step. D-WORKFLOW-186's "within D-WORKFLOW-102's gates" reads accordingly. P1's pass-7 question 2 (whether `backuptool`, T17, and the system services, T22, also gate `0.1`) is withdrawn as outside the program, not answered.** Maintainer, 2026-10-23, when the coordinator put question 2: *"Our codebase check shouldn't have anything to do with what we're actually shipping. This is meant to be an audit, assessment, and renovation, and not concerned with features proactively shipping. Now, why would your question 2 be part of what we're trying to accomplish here?"* Sweep in the same change: plan § 5 and § 6a, § 8's drift trigger, the M6 body's acceptance and dependencies, #339's gate checkbox; `order.md` § 1, the Gate column and T1's release-gate line are P1's (#641). | #346; #641; #339; D-WORKFLOW-102; D-WORKFLOW-186; D-WORKFLOW-132; D-QA-051; `docs/reviews/plan-for-the-plan.md` § 5, § 6a, § 8 |

| D-WORKFLOW-193 | 2026-10-24 | **An archive recipe without `PKG_SHA256` fails its fetch, and the fetch verifies TLS.** `scripts/get_archive` drops `--no-check-certificate` and dies when the recipe carries no checksum (`engineering-practices.md` § Guards must fail closed); the eight archive recipes of 1,347 that lack one gain theirs in the same stream, computed from the archive as fetched once and said to be so (trust on first use, as upstream's own `PKG_SHA256` sweep was). A fork resolved during execution under granted discretion, T5's PL-08; the maintainer may reverse it by a new row. | #834, #652, #837; T5's stream E6 (`docs/reviews/briefs/t5-streams.md`) |

| D-WORKFLOW-194 | 2026-10-24 | **Refines D-WORKFLOW-193's count, not its decision.** The archive versions without a `PKG_SHA256` were **five, in four recipes** (`atf` 2.12.0; `rkbin` 74213af1 and 7c35e21a; `libmali-vulkan` 11759f18; `sway` 1.9), not eight: the stage-B count tested for a top-level `PKG_SHA256=` line and missed the per-`case` branches, and three of its eight set one in every branch while three inherit one. T5's E6 gave the five theirs by trust on first use, said so, with two of them equal to the shared cache's files and stamps. | #834, #652, #837; T5's E6 hand-back on #652 (2026-10-24 06:58 UTC); `02-forward-audit.md` F-19 corrected |

| D-WORKFLOW-195 | 2026-10-24 | **An Extended seat whose answer the model's output ceiling cuts on the packet is run again on a trimmed packet for that seat -- the same model, effort and provider; the analyses and tables whole, the cited files as line-numbered excerpts with context, the ask bounded -- never a model or effort substitution and never the same packet again.** `04` § Second opinion says the seats saw different evidence; an item one seat saw only in excerpt carries `excerpt`, and a disagreement that could be the excerpt's doing is resolved from the artifact, not from either seat. A fork resolved during execution on T30 (#677): Argon at `high` spent about 57k of its 65.5k output tokens reasoning on a 438 KB packet three times (`finish=length`), where T3's 308 KB packet took 30k. The maintainer may reverse it by a new row. | #677, #798; `adversarial-council.md` § Council model floor; the T30 hold post of 10:04 UTC and the coordinator's answer the same hour |

| D-WORKFLOW-209 | 2026-10-25 | **A renovation dead-end table removes nothing and edits no recipe: T23 (and T40, T43 and T25 after it) record a disposition per unit -- dead upstream-carried, shadowed copy with its override live or dead, unshipped, fork-own dead with a proposed removal and its `Already written:` line, or reached after all -- and the removal of upstream-carried dead code is one class decision for the maintainer, put to them on #346 with the table's counts and the cost against the value; a fork-own dead unit's removal is proposed on the punch list and left for the coordinator.** The 1,604 rows are 1,601 upstream-carried: the fork tracks `upstream/next`, a deletion of upstream's file is a modify/delete at every merge (D-WORKFLOW-198's class), and the area futro already held T7 to *deletes nothing upstream carries*. The order's § T23 said *decides the removals*; this row narrows it to *decides the dispositions*. The three IDs before this one are the M7 lane's reservation; this row is the first M6 row after it. | #670, #848, #346; `docs/reviews/briefs/generic-packages-dead-ends.md` § 1 |
```


## Context 4: device-facts rows L15, L16, L29 (with the header)

```text
# Standing device facts

The things only a handheld can show (`vm-first.md`, D-QA-007/033), one row each,
with when each was last seen and on which cut -- so "have we checked this?" is a
| H700 boot on the RG35XX SP (LPDDR4 unit) | DDR4 bootloader/device tree and retained physical storage after an in-place update | 2026-10-16: approvedbc9d→077197 transfer and one reboot; exact SYSTEM/kernel/DTB/bootloader/ES/both RetroArch hashes, empty queue, original mounts and active frontend;163 protected files and settings/recovery preserved | `077197e6cd3e` | [Private deployment](../qa-logs/2026-10-16-rg35xxsp-private-update/README.md); original channels0/owners exited; automatic cloud sync off; no new frame/audio/gameplay claim | #344; prior alignment #519 |
| H700 boot on the RG SP (LPDDR3 unit) | DDR3 bootloader/RG SP tree and separate TF2 ROM mount after an in-place update | 2026-10-12 04:09 UTC: approved8b511→bc9dfe update and one reboot; exact installed hashes, original mounts, empty queue and active frontend/zero restarts;163 files plus credentials/settings/recovery preserved | `bc9dfe8141` | [Current deployment](../qa-logs/2026-10-12-owner-updates/README.md); original channels0/actual exits, owner use resumed, auto cloud sync off; no new frame/audio/gameplay claim | #557, #344 |
| The H700 watchdog, panic-on-hang and ramoops | the H700's DRAM kept across a warm reset -- the watchdog, the sysctls and the reserved-memory node are built (`cbf75c0b06`, D-SYS-002/003/004) and proven on the VM but for the DRAM | never | -- | a deliberate crash on the RG35XX SP with its yes by name (D-QA-008), read back with `rocknix-evidence collect`; corrected 2026-09-25 from "a change to make, not a check" | #104 |
```


## Context 5: .claude/rules/device-builds.md lines 16-24 (the device table)

```text
16  
17  ## Our devices
18  
19  | Hardware | Target | Arch | Notes |
20  |---|---|---|---|
21  | Anbernic RG353M | `RK3566` | aarch64 | cortex-a55, neon-fp-armv8 (no crypto ext) |
22  | Anbernic RG35XX SP | `H700` | aarch64 | cortex-a53, crypto-neon-fp-armv8; maintainer's unit is LPDDR4 and uses the DDR4 image (`vdd-dram` = 1.1 V, verified 2026-09-05) |
23  | Anbernic RG SP | `H700` | aarch64 | cortex-a53, crypto-neon-fp-armv8; maintainer's unit is LPDDR3 and uses the DDR3 image (stock boot0 `dram_type = 7`, then ROCKNIX `vdd-dram` = 1.2 V, verified 2026-09-05) |
24  | Anbernic RG351M | `RK3326` | aarch64 | |
```


## projects/ROCKNIX/devices/H700/bootloader/update.sh @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  #!/bin/sh
 2  # SPDX-License-Identifier: GPL-2.0
 3  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 4  
 5  [ -z "$SYSTEM_ROOT" ] && SYSTEM_ROOT=""
 6  [ -z "$BOOT_ROOT" ] && BOOT_ROOT="/flash"
 7  [ -z "$BOOT_PART" ] && BOOT_PART=$(df "$BOOT_ROOT" | tail -1 | awk {' print $1 '})
 8  
 9  # identify the boot device
10  if [ -z "$BOOT_DISK" ]; then
11    case $BOOT_PART in
12      /dev/mmcblk*)
13        BOOT_DISK=$(echo $BOOT_PART | sed -e "s,p[0-9]*,,g")
14        ;;
15    esac
16  fi
17  
18  # mount $BOOT_ROOT rw
19  mount -o remount,rw $BOOT_ROOT
20  
21  echo "Updating device trees..."
22  cp -f $SYSTEM_ROOT/usr/share/bootloader/device_trees/* $BOOT_ROOT/device_trees
23  mkdir -p $BOOT_ROOT/overlays
24  cp -f $SYSTEM_ROOT/usr/share/bootloader/overlays/* $BOOT_ROOT/overlays
25  
26  DT_ID=$(cat /proc/device-tree/rocknix-dt-id)
27  
28  UPDATE_DTB_SOURCE="$BOOT_ROOT/device_trees/$DT_ID.dtb"
29  if [ -f "$UPDATE_DTB_SOURCE" ]; then
30    echo "Updating dtb.img from $(basename $UPDATE_DTB_SOURCE)..."
31    cp -f "$UPDATE_DTB_SOURCE" "$BOOT_ROOT/dtb.img"
32  fi
33  
34  # detect DDR3/DDR4
35  for r in /sys/class/regulator/regulator.*/; do
36    [[ "$(cat "$r/name" 2>/dev/null)" == "vdd-dram" ]] && VDD_REG_PATH=$r
37  done
38  
39  if [ -n "${VDD_REG_PATH:-}" ]; then
40    DCDC3_MICROVOLTS=$(cat "$VDD_REG_PATH/microvolts")
41    case "$DCDC3_MICROVOLTS" in
42      1200000)
43        UBOOT_BIN="H700_DDR3_u-boot-sunxi-with-spl.bin"
44        ;;
45      1100000)
46        UBOOT_BIN="H700_DDR4_u-boot-sunxi-with-spl.bin"
47        ;;
48    esac
49  fi
50  
51  # update bootloader
52  if [ -n "${UBOOT_BIN:-}" ]; then
53    if [ -f $SYSTEM_ROOT/usr/share/bootloader/$UBOOT_BIN ]; then
54      echo "Updating u-boot on: $BOOT_DISK..."
55      dd if=$SYSTEM_ROOT/usr/share/bootloader/$UBOOT_BIN of=$BOOT_DISK bs=1K seek=8 conv=fsync,notrunc &>/dev/null
56    fi
57  fi
58  
59  # mount $BOOT_ROOT ro
60  sync
61  mount -o remount,ro $BOOT_ROOT
62  
63  echo "UPDATE" > /storage/.boot.hint
```


## projects/ROCKNIX/devices/H700/config/kernel-firmware.dat @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # RTW_88
 2  rtw88/rtw8821c_fw.bin
 3  
 4  # RTL_8821CS
 5  rtl_bt/rtl8821cs_config.bin
 6  rtl_bt/rtl8821cs_fw.bin
 7  
 8  # Panels
 9  panels/anbernic,rg28xx-panel.panel
10  panels/anbernic,rgcubexx-panel.panel
11  panels/anbernic,rg40xx-panel.panel
12  panels/anbernic,rg40xx-v2-panel.panel
13  panels/anbernic,rg35xx-plus-rev6-panel.panel
14  panels/anbernic,rg35xx-plus-panel.panel
15  panels/anbernic,rg35xx-sp-v2-panel.panel
16  panels/anbernic,rg34xx-panel.panel
17  panels/anbernic,rg34xx-sp-panel.panel
18  panels/anbernic,rg34xx-sp-v2-panel.panel
```


## projects/ROCKNIX/devices/H700/filesystem/usr/lib/udev/rules.d/80-clock.rules @ 8ebaf8daad (whole, line-numbered, masked)

```text
1  # Overrides the project default: only rtc0 (PCF8563) holds time across power off.
2  ACTION=="add", SUBSYSTEM=="rtc", KERNEL=="rtc0", RUN+="/sbin/hwclock --hctosys --utc --rtc=/dev/%k"
```


## projects/ROCKNIX/devices/H700/filesystem/usr/lib/udev/rules.d/wlan0.powersave.off.rules @ 8ebaf8daad (whole, line-numbered, masked)

```text
1  ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="sdio", KERNELS=="mmc2:0001:1", RUN+="/sbin/iw dev %k set power_save off"
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg-sp.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-sp.dts"
 8  
 9  / {
10  	model = "Anbernic RG-SP";
11  	compatible = "anbernic,rg-sp", "allwinner,sun50i-h700";
12  	rocknix-dt-id = "sun50i-h700-anbernic-rg-sp";
13  };
14  
15  &panel {
16  	compatible = "anbernic,rg34xx-sp-v2-panel", "panel-mipi-dpi-spi";
17  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg28xx.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-plus.dts"
 8  
 9  / {
10  	model = "Anbernic RG28XX";
11  	compatible = "anbernic,rg28xx", "allwinner,sun50i-h700";
12  	rocknix-dt-id = "sun50i-h700-anbernic-rg28xx";
13  };
14  
15  &panel {
16  	compatible = "anbernic,rg28xx-panel", "panel-mipi-dpi-spi";
17  	rotation = <270>;
18  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg34xx-sp-v2-panel.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-sp.dts"
 8  
 9  / {
10  	model = "Anbernic RG34XX-SP";
11  	compatible = "anbernic,rg34xx-sp", "allwinner,sun50i-h700";
12  	rocknix-dt-id = "sun50i-h700-anbernic-rg34xx-sp-v2-panel";
13  };
14  
15  &panel {
16  	compatible = "anbernic,rg34xx-sp-v2-panel", "panel-mipi-dpi-spi";
17  };
18  
19  &joypad {
20  	invert-absrx;
21  	invert-absry;
22  	amux-count = <4>;
23  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg34xx-sp.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-sp.dts"
 8  
 9  / {
10  	model = "Anbernic RG34XX-SP";
11  	compatible = "anbernic,rg34xx-sp", "allwinner,sun50i-h700";
12  	rocknix-dt-id = "sun50i-h700-anbernic-rg34xx-sp";
13  };
14  
15  &panel {
16  	compatible = "anbernic,rg34xx-sp-panel", "panel-mipi-dpi-spi";
17  };
18  
19  &joypad {
20  	invert-absrx;
21  	invert-absry;
22  	amux-count = <4>;
23  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg34xx.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-plus.dts"
 8  
 9  / {
10  	model = "Anbernic RG34XX";
11  	compatible = "anbernic,rg34xx", "allwinner,sun50i-h700";
12  	rocknix-dt-id = "sun50i-h700-anbernic-rg34xx";
13  };
14  
15  &panel {
16  	compatible = "anbernic,rg34xx-panel", "panel-mipi-dpi-spi";
17  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-2024-rev6-panel.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-2024.dts"
 8  
 9  / {
10  	rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-2024-rev6-panel";
11  };
12  
13  &panel {
14  	compatible = "anbernic,rg35xx-plus-rev6-panel", "panel-mipi-dpi-spi";
15  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-h-rev6-panel.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-h.dts"
 8  
 9  / {
10  	rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-h-rev6-panel";
11  };
12  
13  &panel {
14  	compatible = "anbernic,rg35xx-plus-rev6-panel", "panel-mipi-dpi-spi";
15  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-plus-rev6-panel.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-plus.dts"
 8  
 9  / {
10  	rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-plus-rev6-panel";
11  };
12  
13  &panel {
14  	compatible = "anbernic,rg35xx-plus-rev6-panel", "panel-mipi-dpi-spi";
15  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-pro.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-plus.dts"
 8  
 9  / {
10  	model = "Anbernic RG35XX Pro";
11  	compatible = "anbernic,rg35xx-pro", "allwinner,sun50i-h700";
12  	rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-pro";
13  };
14  
15  &joypad {
16  	amux-count = <4>;
17  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg35xx-sp-v2-panel.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-sp.dts"
 8  
 9  / {
10  	rocknix-dt-id = "sun50i-h700-anbernic-rg35xx-sp-v2-panel";
11  };
12  
13  &panel {
14  	compatible = "anbernic,rg35xx-sp-v2-panel", "panel-mipi-dpi-spi";
15  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-h-v2-panel.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Philippe Simons <simons.philippe@gmail.com>.
 4   */
 5  
 6  #include "sun50i-h700-anbernic-rg40xx-h.dts"
 7  
 8  / {
 9  	rocknix-dt-id = "sun50i-h700-anbernic-rg40xx-h-v2-panel";
10  };
11  
12  &panel {
13  	compatible = "anbernic,rg40xx-v2-panel", "panel-mipi-dpi-spi";
14  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-h.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Philippe Simons <simons.philippe@gmail.com>.
 4   */
 5  
 6  #include "sun50i-h700-anbernic-rg35xx-plus.dts"
 7  
 8  / {
 9  	model = "Anbernic RG40XX H";
10  	compatible = "anbernic,rg40xx-h", "allwinner,sun50i-h700";
11  	rocknix-dt-id = "sun50i-h700-anbernic-rg40xx-h";
12  };
13  
14  &joypad {
15  	invert-absrx;
16  	invert-absry;
17  	amux-count = <4>;
18  	pwms = <&pwm 3 1000000 0>;
19  	pinctrl-0 = <&joy_mux_pin>, <&pwm3_pin>;
20  };
21  
22  &uart5 {
23  	pinctrl-names = "default";
24  	pinctrl-0 = <&uart5_ph_pins>;
25  	status = "okay";
26  };
27  
28  &leds {
29  	led-rgb {
30  		function = LED_FUNCTION_KBD_BACKLIGHT;
31  		color = <LED_COLOR_ID_RGB>;
32  		gpios = <&pio 8 7 GPIO_ACTIVE_HIGH>; /* PI7 */
33  	};
34  };
35  
36  &panel {
37  	compatible = "anbernic,rg40xx-panel", "panel-mipi-dpi-spi";
38  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-v-v2-panel.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Philippe Simons <simons.philippe@gmail.com>.
 4   */
 5  
 6  #include "sun50i-h700-anbernic-rg40xx-v.dts"
 7  
 8  / {
 9  	rocknix-dt-id = "sun50i-h700-anbernic-rg40xx-v-v2-panel";
10  };
11  
12  &panel {
13  	compatible = "anbernic,rg40xx-v2-panel", "panel-mipi-dpi-spi";
14  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rg40xx-v.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Philippe Simons <simons.philippe@gmail.com>.
 4   */
 5  
 6  #include "sun50i-h700-anbernic-rg35xx-plus.dts"
 7  
 8  / {
 9  	model = "Anbernic RG40XX V";
10  	compatible = "anbernic,rg40xx-V", "allwinner,sun50i-h700";
11  	rocknix-dt-id = "sun50i-h700-anbernic-rg40xx-v";
12  };
13  
14  &joypad {
15  	amux-count = <4>;
16  	pwms = <&pwm 3 1000000 0>;
17  	pinctrl-0 = <&joy_mux_pin>, <&pwm3_pin>;
18  };
19  
20  &uart5 {
21  	pinctrl-names = "default";
22  	pinctrl-0 = <&uart5_ph_pins>;
23  	status = "okay";
24  };
25  
26  &leds {
27  	led-rgb {
28  		function = LED_FUNCTION_KBD_BACKLIGHT;
29  		color = <LED_COLOR_ID_RGB>;
30  		gpios = <&pio 8 7 GPIO_ACTIVE_HIGH>; /* PI7 */
31  	};
32  };
33  
34  &panel {
35  	compatible = "anbernic,rg40xx-panel", "panel-mipi-dpi-spi";
36  };
```


## projects/ROCKNIX/devices/H700/linux/dts/allwinner/sun50i-h700-anbernic-rgcubexx.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: (GPL-2.0-only OR BSD-2-Clause)
 2  /*
 3   * Copyright (C) 2024 Ryan Walklin <ryan@testtoast.com>.
 4   * Copyright (C) 2024 Chris Morgan <macroalpha82@gmail.com>.
 5   */
 6  
 7  #include "sun50i-h700-anbernic-rg35xx-plus.dts"
 8  
 9  / {
10  	model = "Anbernic RG CubeXX";
11  	compatible = "anbernic,rgcubexx", "allwinner,sun50i-h700";
12  	rocknix-dt-id = "sun50i-h700-anbernic-rgcubexx";
13  };
14  
15  &joypad {
16  	invert-absrx;
17  	invert-absry;
18  	amux-count = <4>;
19  	pwms = <&pwm 3 1000000 0>;
20  	pinctrl-0 = <&joy_mux_pin>, <&pwm3_pin>;
21  };
22  
23  &uart5 {
24  	pinctrl-names = "default";
25  	pinctrl-0 = <&uart5_ph_pins>;
26  	status = "okay";
27  };
28  
29  &leds {
30  	led-rgb {
31  		function = LED_FUNCTION_KBD_BACKLIGHT;
32  		color = <LED_COLOR_ID_RGB>;
33  		gpios = <&pio 8 7 GPIO_ACTIVE_HIGH>; /* PI7 */
34  	};
35  };
36  
37  &reg_lcd {
38  	regulator-min-microvolt = <2800000>;
39  	regulator-max-microvolt = <2800000>;
40  };
41  
42  &panel {
43  	compatible = "anbernic,rgcubexx-panel", "panel-mipi-dpi-spi";
44  };
```


## projects/ROCKNIX/devices/H700/options @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  ################################################################################
 2  # setup device defaults
 3  ################################################################################
 4  
 5    # The TARGET_CPU variable controls which processor should be targeted for
 6    # generated code.
 7      case ${TARGET_ARCH} in
 8        aarch64)
 9          TARGET_CPU="cortex-a53"
10          TARGET_CPU_FLAGS="+crc+fp+simd"
11          ;;
12        arm)
13          TARGET_KERNEL_ARCH="arm64"
14          TARGET_FLOAT="hard"
15          TARGET_CPU="cortex-a53"
16          TARGET_CPU_FLAGS="+crc"
17          TARGET_FPU="crypto-neon-fp-armv8"
18          ;;
19      esac
20  
21      PARTITION_TABLE="msdos"
22      HW_CPU="Allwinner H700"
23  
24    # Kernel target
25      KERNEL_TARGET="Image"
26  
27    # Kernel extra targets to build
28      KERNEL_MAKE_EXTRACMD=" $(get_kernel_make_extracmd)"
29  
30    # Kernel cmdline
31      EXTRA_CMDLINE="quiet console=ttyS0,115200 console=tty0 systemd.debug_shell=ttyS0"
32  
33    # Bootloader to use (syslinux / u-boot)
34      BOOTLOADER="u-boot"
35  
36    # U-Boot firmware package(s) to use
37      UBOOT_FIRMWARE+=" atf"
38      ATF_PLATFORM="sun50i_h616"
39      ATF_BL31_BINARY="bl31.bin"
40  
41    # Mali GPU family
42      MALI_FAMILY="g31"
43      GRAPHIC_DRIVERS="panfrost"
44  
45    # For maximum cross compatbility
46      PREFER_GLES="yes"
47  
48    # Batteryplus voltage-based battery percentage daemon (yes / no)
49      BATTERYPLUS_SUPPORT="yes"
50  
51    # Displayserver to use (wl / no)
52      DISPLAYSERVER="wl"
53  
54    # Windowmanager to use (weston / swaywm-env / no)
55      WINDOWMANAGER="swaywm-env"
56  
57    # Additional drivers to install:
58    # for a list of additional drivers see packages/linux-drivers
59    # Space separated list is supported,
60    # e.g. ADDITIONAL_DRIVERS="DRIVER1 DRIVER2"
61      ADDITIONAL_DRIVERS=""
62  
63    # Additional Firmware to use ( )
64    # Space separated list is supported,
65    # e.g. FIRMWARE=""
66      FIRMWARE=""
67  
68    # Additional packages to install
69      ADDITIONAL_PACKAGES=""
70  
71    # Debug tty path
72      DEBUG_TTY="/dev/ttyS0"
73  
74    # Build and install rocknix out-of-tree device trees and overlays (yes / no)
75      ROCKNIX_DEVICE_TREE_OVERLAYS="yes"
76  
77    # ZRAM Algorithm
78      ZRAM_COMPRESSION_ALGO="lzo-rle"
79  
80    # ZRAM Size
81      ZRAM_SWAP_SIZE="0"
82  
83    # Disk Swap
84      SWAP_FILE_SIZE="0"
```


## projects/ROCKNIX/devices/H700/packages/h700-suspend-stub/package.mk @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="h700-suspend-stub"
 5  PKG_VERSION="712653d11230b2450061ddb8e25f31e072da7a48"
 6  PKG_SHA256="3698da9aad40c26c10f6aa31f8366158914e0a351d31f1084c6b8032147f4616"
 7  PKG_LICENSE="GPL-2.0-or-later"
 8  PKG_SITE="https://github.com/Jacob-Matthew-Cook/h700-suspend-stub"
 9  PKG_URL="https://github.com/Jacob-Matthew-Cook/h700-suspend-stub/archive/${PKG_VERSION}.tar.gz"
10  PKG_DEPENDS_TARGET="toolchain"
11  PKG_LONGDESC="SRAM suspend stub for PSCI SYSTEM_SUSPEND on the H700, by kailashrs."
12  PKG_TOOLCHAIN="manual"
13  
14  # The DRAM sources are U-Boot's own, taken from the bootloader package's
15  # unpacked tree. Source only: a target dependency here would close the loop
16  # u-boot -> atf -> suspend-stub -> u-boot.
17  PKG_DEPENDS_UNPACK="u-boot-DDR4 u-boot-DDR3 atf"
18  PKG_NEED_UNPACK="$(get_pkg_directory u-boot-DDR4) $(get_pkg_directory u-boot-DDR3) $(get_pkg_directory atf)"
19  
20  # One stub per memory type; BL31 picks the match at boot. <bootloader package>:<output>
21  PKG_STUB_VARIANTS="u-boot-DDR4:suspend_stub_lpddr4.bin \
22                     u-boot-DDR3:suspend_stub_lpddr3.bin"
23  
24  make_target() {
25    local variant uboot out dir defconfig key
26  
27    : >${PKG_BUILD}/.stub-keys
28    for variant in ${PKG_STUB_VARIANTS}; do
29      uboot="${variant%:*}"; out="${variant##*:}"; dir="${PKG_BUILD}/${out%.bin}"
30  
31      # the defconfig comes from the bootloader package so the two can never disagree
32      defconfig="$(sed -n 's/^[[:space:]]*PKG_UBOOT_CONFIG="\([^"]*\)".*/\1/p' \
33                     "$(get_pkg_directory ${uboot})/package.mk" | head -1)"
34      [ -n "${defconfig}" ] || die "suspend-stub: no PKG_UBOOT_CONFIG in ${uboot}"
35      defconfig="$(get_build_dir ${uboot})/configs/${defconfig}"
36      [ -r "${defconfig}" ] || die "suspend-stub: ${defconfig} not found"
37  
38      mkdir -p ${dir}
39      make -C ${dir} -f ${PKG_BUILD}/Makefile SRC_DIR=${PKG_BUILD} UBOOT_DIR=$(get_build_dir ${uboot}) \
40        ATF_DIR=$(get_build_dir atf) DEFCONFIG=${defconfig} OUT=${out} CROSS_COMPILE=${TARGET_KERNEL_PREFIX}
41  
42      # TF-A matches on (type, clk); two stubs sharing both would be picked arbitrarily
43      key=*** '$2 == "STUB_DRAM_TYPE" || $2 == "CONFIG_DRAM_CLK" { printf "%s ", $3 }' ${dir}/boards/board.h)"
44      grep -qx "${key}" ${PKG_BUILD}/.stub-keys &&
45        die "suspend-stub: ${out} is DRAM type/clock ${key}, same as an earlier stub; TF-A could not tell them apart"
46      echo "${key}" >>${PKG_BUILD}/.stub-keys
47    done
48  }
49  
50  makeinstall_target() {
51    # atf reads the stubs from the sysroot rather than from this build directory,
52    # which neither survives AUTOREMOVE nor crosses a CI job boundary.
53    mkdir -p ${SYSROOT_PREFIX}/usr/share/${PKG_NAME}
54    cp -a *.bin ${SYSROOT_PREFIX}/usr/share/${PKG_NAME}
55  }
```


## projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/package.mk @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="u-boot-DDR3"
 5  PKG_VERSION="v2026.01"
 6  PKG_SHA256="03bb43c58d2343ee48dd191e0f181f0108425b179d84519add3a977071c3f654"
 7  PKG_LICENSE="GPL"
 8  PKG_SITE="https://www.denx.de/wiki/U-Boot"
 9  PKG_URL="https://github.com/u-boot/u-boot/archive/${PKG_VERSION}.tar.gz"
10  PKG_DEPENDS_TARGET="toolchain Python3 swig:host pyelftools:host"
11  PKG_LONGDESC="Das U-Boot is a cross-platform bootloader for embedded systems."
12  PKG_TOOLCHAIN="manual"
13  
14  PKG_NEED_UNPACK="${PROJECT_DIR}/${PROJECT}/bootloader ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader"
15  # the SPL embeds atf's BL31; rebuild when it changes
16  PKG_NEED_UNPACK+=" ${SYSROOT_PREFIX}/usr/share/atf/bl31.bin"
17  
18  if [ -n "${UBOOT_FIRMWARE}" ]; then
19    PKG_DEPENDS_TARGET+=" ${UBOOT_FIRMWARE}"
20    PKG_DEPENDS_UNPACK+=" ${UBOOT_FIRMWARE}"
21  fi
22  
23  pre_make_target() {
24    PKG_UBOOT_CONFIG="anbernic_rg35xx_h700_lpddr3_defconfig"
25    PKG_BL31="${SYSROOT_PREFIX}/usr/share/atf/bl31.bin"
26  }
27  
28  make_target() {
29    [ "${BUILD_WITH_DEBUG}" = "yes" ] && PKG_DEBUG=1 || PKG_DEBUG=0
30    setup_pkg_config_host
31  
32    DEBUG=${PKG_DEBUG} CROSS_COMPILE="${TARGET_KERNEL_PREFIX}" LDFLAGS="" ARCH=arm make mrproper
33    DEBUG=${PKG_DEBUG} CROSS_COMPILE="${TARGET_KERNEL_PREFIX}" LDFLAGS="" ARCH=arm make HOSTCC="${HOST_CC}" HOSTCFLAGS="-I${TOOLCHAIN}/include" HOSTLDFLAGS="${HOST_LDFLAGS}" ${PKG_UBOOT_CONFIG}
34    DEBUG=${PKG_DEBUG} CROSS_COMPILE="${TARGET_KERNEL_PREFIX}" LDFLAGS="" ARCH=arm _python_sysroot="${TOOLCHAIN}" _python_prefix=/ _python_exec_prefix=/ make BL31="${PKG_BL31}" HOSTCC="${HOST_CC}" HOSTCFLAGS="-I${TOOLCHAIN}/include" HOSTLDFLAGS="${HOST_LDFLAGS}" HOSTSTRIP="true" CONFIG_MKIMAGE_DTC_PATH="scripts/dtc/dtc"
35  }
36  
37  makeinstall_target() {
38    # The u-boot wrapper package picks these up. It read them from this build
39    # directory, which neither survives AUTOREMOVE nor crosses a CI job boundary;
40    # the sysroot lives inside toolchain and is carried between jobs.
41    mkdir -p ${SYSROOT_PREFIX}/usr/share/${PKG_NAME}
42    cp -a u-boot-sunxi-with-spl.bin ${SYSROOT_PREFIX}/usr/share/${PKG_NAME}
43  }
```


## projects/ROCKNIX/devices/H700/packages/u-boot-DDR3/sources/configs/anbernic_rg35xx_h700_lpddr3_defconfig @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  CONFIG_ARM=y
 2  CONFIG_ARCH_SUNXI=y
 3  CONFIG_DEFAULT_DEVICE_TREE="allwinner/sun50i-h700-anbernic-rg35xx-2024"
 4  CONFIG_SPL=y
 5  CONFIG_DRAM_SUNXI_DX_ODT=0x06060606
 6  CONFIG_DRAM_SUNXI_DX_DRI=0x0d0d0d0d
 7  CONFIG_DRAM_SUNXI_CA_DRI=0x1919
 8  CONFIG_DRAM_SUNXI_ODT_EN=0x9988eeee
 9  CONFIG_DRAM_SUNXI_TPR2=0x1
10  CONFIG_DRAM_SUNXI_TPR6=0x2fb08080
11  CONFIG_DRAM_SUNXI_TPR10=0x402f4489
12  CONFIG_DRAM_SUNXI_TPR11=0x10121013
13  CONFIG_DRAM_SUNXI_TPR12=0x0d0e0d0e
14  CONFIG_DRAM_SUNXI_PHY_ADDR_MAP_1=y
15  CONFIG_MACH_SUN50I_H616=y
16  CONFIG_SUNXI_DRAM_H616_LPDDR3=y
17  CONFIG_DRAM_CLK=672
18  CONFIG_R_I2C_ENABLE=y
19  CONFIG_SPL_I2C=y
20  CONFIG_SPL_SYS_I2C_LEGACY=y
21  CONFIG_SYS_I2C_MVTWSI=y
22  CONFIG_SYS_I2C_SLAVE=0x7f
23  CONFIG_SYS_I2C_SPEED=400000
24  CONFIG_REGULATOR_AXP=y
25  CONFIG_AXP717_POWER=y
26  CONFIG_AXP_DISABLE_BOOT_ON_POWERON=y
27  CONFIG_AXP_DCDC2_VOLT=940
28  CONFIG_AXP_DCDC3_VOLT=1200
29  CONFIG_EFI_LOADER=n
30  CONFIG_BOOTDELAY=0
31  CONFIG_LED_STATUS=y
32  CONFIG_LED_STATUS_GPIO=y
33  CONFIG_LED_STATUS0=y
34  CONFIG_LED_STATUS_BIT=267
35  CONFIG_LED_STATUS_STATE=2
```


## projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/package.mk @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="u-boot-DDR4"
 5  PKG_VERSION="v2026.01"
 6  PKG_SHA256="03bb43c58d2343ee48dd191e0f181f0108425b179d84519add3a977071c3f654"
 7  PKG_LICENSE="GPL"
 8  PKG_SITE="https://www.denx.de/wiki/U-Boot"
 9  PKG_URL="https://github.com/u-boot/u-boot/archive/${PKG_VERSION}.tar.gz"
10  PKG_DEPENDS_TARGET="toolchain Python3 swig:host pyelftools:host"
11  PKG_LONGDESC="Das U-Boot is a cross-platform bootloader for embedded systems."
12  PKG_TOOLCHAIN="manual"
13  
14  PKG_NEED_UNPACK="${PROJECT_DIR}/${PROJECT}/bootloader ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader"
15  # the SPL embeds atf's BL31; rebuild when it changes
16  PKG_NEED_UNPACK+=" ${SYSROOT_PREFIX}/usr/share/atf/bl31.bin"
17  
18  if [ -n "${UBOOT_FIRMWARE}" ]; then
19    PKG_DEPENDS_TARGET+=" ${UBOOT_FIRMWARE}"
20    PKG_DEPENDS_UNPACK+=" ${UBOOT_FIRMWARE}"
21  fi
22  
23  pre_make_target() {
24    PKG_UBOOT_CONFIG="anbernic_rg35xx_h700_lpddr4_defconfig"
25    PKG_BL31="${SYSROOT_PREFIX}/usr/share/atf/bl31.bin"
26  }
27  
28  make_target() {
29    [ "${BUILD_WITH_DEBUG}" = "yes" ] && PKG_DEBUG=1 || PKG_DEBUG=0
30    setup_pkg_config_host
31  
32    DEBUG=${PKG_DEBUG} CROSS_COMPILE="${TARGET_KERNEL_PREFIX}" LDFLAGS="" ARCH=arm make mrproper
33    DEBUG=${PKG_DEBUG} CROSS_COMPILE="${TARGET_KERNEL_PREFIX}" LDFLAGS="" ARCH=arm make HOSTCC="${HOST_CC}" HOSTCFLAGS="-I${TOOLCHAIN}/include" HOSTLDFLAGS="${HOST_LDFLAGS}" ${PKG_UBOOT_CONFIG}
34    DEBUG=${PKG_DEBUG} CROSS_COMPILE="${TARGET_KERNEL_PREFIX}" LDFLAGS="" ARCH=arm _python_sysroot="${TOOLCHAIN}" _python_prefix=/ _python_exec_prefix=/ make BL31="${PKG_BL31}" HOSTCC="${HOST_CC}" HOSTCFLAGS="-I${TOOLCHAIN}/include" HOSTLDFLAGS="${HOST_LDFLAGS}" HOSTSTRIP="true" CONFIG_MKIMAGE_DTC_PATH="scripts/dtc/dtc"
35  }
36  
37  makeinstall_target() {
38    # The u-boot wrapper package picks these up. It read them from this build
39    # directory, which neither survives AUTOREMOVE nor crosses a CI job boundary;
40    # the sysroot lives inside toolchain and is carried between jobs.
41    mkdir -p ${SYSROOT_PREFIX}/usr/share/${PKG_NAME}
42    cp -a u-boot-sunxi-with-spl.bin ${SYSROOT_PREFIX}/usr/share/${PKG_NAME}
43  }
```


## projects/ROCKNIX/devices/H700/packages/u-boot-DDR4/sources/configs/anbernic_rg35xx_h700_lpddr4_defconfig @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  CONFIG_ARM=y
 2  CONFIG_ARCH_SUNXI=y
 3  CONFIG_DEFAULT_DEVICE_TREE="allwinner/sun50i-h700-anbernic-rg35xx-2024"
 4  CONFIG_SPL=y
 5  CONFIG_DRAM_SUNXI_DX_ODT=0x08080808
 6  CONFIG_DRAM_SUNXI_DX_DRI=0x0e0e0e0e
 7  CONFIG_DRAM_SUNXI_CA_DRI=0x0e0e
 8  CONFIG_DRAM_SUNXI_ODT_EN=0x7887bbbb
 9  CONFIG_DRAM_SUNXI_TPR2=0x1
10  CONFIG_DRAM_SUNXI_TPR6=0x40808080
11  CONFIG_DRAM_SUNXI_TPR10=0x402f6633
12  CONFIG_DRAM_SUNXI_TPR11=0x1b1f1e1c
13  CONFIG_DRAM_SUNXI_TPR12=0x06060606
14  CONFIG_DRAM_SUNXI_PHY_ADDR_MAP_1=y
15  CONFIG_MACH_SUN50I_H616=y
16  CONFIG_SUNXI_DRAM_H616_LPDDR4=y
17  CONFIG_DRAM_CLK=672
18  CONFIG_R_I2C_ENABLE=y
19  CONFIG_SPL_I2C=y
20  CONFIG_SPL_SYS_I2C_LEGACY=y
21  CONFIG_SYS_I2C_MVTWSI=y
22  CONFIG_SYS_I2C_SLAVE=0x7f
23  CONFIG_SYS_I2C_SPEED=400000
24  CONFIG_REGULATOR_AXP=y
25  CONFIG_AXP717_POWER=y
26  CONFIG_AXP_DISABLE_BOOT_ON_POWERON=y
27  CONFIG_AXP_DCDC2_VOLT=940
28  CONFIG_AXP_DCDC3_VOLT=1100
29  CONFIG_EFI_LOADER=n
30  CONFIG_BOOTDELAY=0
31  CONFIG_LED_STATUS=y
32  CONFIG_LED_STATUS_GPIO=y
33  CONFIG_LED_STATUS0=y
34  CONFIG_LED_STATUS_BIT=267
35  CONFIG_LED_STATUS_STATE=2
```


## projects/ROCKNIX/devices/H700/packages/u-boot/package.mk @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="u-boot"
 5  PKG_VERSION="1.0"
 6  PKG_LICENSE="GPL"
 7  PKG_SITE="https://www.denx.de/wiki/U-Boot"
 8  PKG_URL=""
 9  PKG_DEPENDS_TARGET="toolchain"
10  PKG_LONGDESC="Das U-Boot is a cross-platform bootloader for embedded systems."
11  PKG_TOOLCHAIN="manual"
12  
13  PKG_NEED_UNPACK="${PROJECT_DIR}/${PROJECT}/bootloader ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader"
14  PKG_NEED_UNPACK+=" ${PROJECT_DIR}/${PROJECT}/options ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/options"
15  
16  for PKG_SUBDEVICE in ${SUBDEVICES}; do
17    PKG_DEPENDS_TARGET+=" u-boot-${PKG_SUBDEVICE}"
18    PKG_DEPENDS_UNPACK+=" u-boot-${PKG_SUBDEVICE}"
19    PKG_NEED_UNPACK+=" $(get_pkg_directory u-boot-${PKG_SUBDEVICE})"
20    PKG_NEED_UNPACK+=" ${SYSROOT_PREFIX}/usr/share/u-boot-${PKG_SUBDEVICE}/u-boot-sunxi-with-spl.bin"
21  done
22  
23  make_target() {
24    : # nothing
25  }
26  
27  makeinstall_target() {
28    mkdir -p $INSTALL/usr/share/bootloader
29  
30    for PKG_SUBDEVICE in ${SUBDEVICES}; do
31      # scripts/build redirects SYSROOT_PREFIX to a per-package staging dir for
32      # the duration of makeinstall; PKG_ORIG_SYSROOT_PREFIX is the shared one.
33      PKG_UBOOTBIN=${PKG_ORIG_SYSROOT_PREFIX}/usr/share/u-boot-${PKG_SUBDEVICE}/u-boot-sunxi-with-spl.bin
34      cp -av ${PKG_UBOOTBIN} $INSTALL/usr/share/bootloader/H700_${PKG_SUBDEVICE}_u-boot-sunxi-with-spl.bin
35    done
36  }
```


## projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf: lines 1-6 @ 8ebaf8daad

```text
1  #
2  # Automatically generated file; DO NOT EDIT.
3  # Linux/arm64 7.2.0 Kernel Configuration
4  #
5  CONFIG_CC_VERSION_TEXT="aarch64-rocknix-linux-gnu-gcc-15.2.0 (GCC) 15.2.0"
6  CONFIG_CC_IS_GCC=y
```


## diff projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf @ 651150fc88 (<) against @ 8ebaf8daad (>) (12 removed, 13 added)

```text
5c5
< CONFIG_CC_VERSION_TEXT="aarch64-rocknix-linux-gnu-gcc-16.2.0 (GCC) 16.2.0"
---
> CONFIG_CC_VERSION_TEXT="aarch64-rocknix-linux-gnu-gcc-15.2.0 (GCC) 15.2.0"
7c7
< CONFIG_GCC_VERSION=160200
---
> CONFIG_GCC_VERSION=150200
14,16c14,16
< CONFIG_RUSTC_VERSION=109901
< CONFIG_RUSTC_LLVM_VERSION=230101
< CONFIG_RUSTC_LLVM_MAJOR_VERSION=23
---
> CONFIG_RUSTC_VERSION=109801
> CONFIG_RUSTC_LLVM_VERSION=220108
> CONFIG_RUSTC_LLVM_MAJOR_VERSION=22
25d24
< CONFIG_CC_HAS_COUNTED_BY_PTR=y
2783a2783
> CONFIG_INPUT_POLLDEV=y
3656c3656
< # CONFIG_WATCHDOG_SYSFS is not set
---
> CONFIG_WATCHDOG_SYSFS=y
7290c7290
< # CONFIG_PSTORE_CONSOLE is not set
---
> CONFIG_PSTORE_CONSOLE=y
7292c7292
< # CONFIG_PSTORE_RAM is not set
---
> CONFIG_PSTORE_RAM=y
7744c7744
< # CONFIG_RAID6_PQ_BENCHMARK is not set
---
> CONFIG_RAID6_PQ_BENCHMARK=y
7975c7975
< # CONFIG_SOFTLOCKUP_DETECTOR is not set
---
> CONFIG_SOFTLOCKUP_DETECTOR=y
7978c7978,7979
< # CONFIG_DETECT_HUNG_TASK is not set
---
> CONFIG_DETECT_HUNG_TASK=y
> CONFIG_DEFAULT_HUNG_TASK_TIMEOUT=120
```


## projects/ROCKNIX/devices/H700/patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled: lines 1-12 @ 8ebaf8daad (of 4,036)

```text
 1  From 6ba0219c9da833fd27500bc72e3103ea8998ed47 Mon Sep 17 00:00:00 2001
 2  From: tiopex <tiopxyz@gmail.com>
 3  Date: Thu, 29 May 2025 12:51:30 +0200
 4  Subject: [PATCH] sound: soc: Add sunxi_v2 for h616 ahub
 5  
 6  ---
 7   sound/soc/Kconfig                         |    1 +
 8   sound/soc/Makefile                        |    1 +
 9   sound/soc/sunxi_v2/Kconfig                |   48 +
10   sound/soc/sunxi_v2/Makefile               |   11 +
11   sound/soc/sunxi_v2/drv_hdmi.h             |   63 +
12   sound/soc/sunxi_v2/snd_sunxi_ahub.c       | 1475 +++++++++++++++++++++
```


## projects/ROCKNIX/bootloader/mkimage @ 8ebaf8daad: lines 1-113 (excerpt)

```text
  1  # SPDX-License-Identifier: GPL-2.0
  2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
  3  
  4  . config/functions
  5  
  6  mkimage_uboot() {
  7    if [ -f "${RELEASE_DIR}/3rdparty/bootloader/${SUBDEVICE}_uboot.bin" ]; then
  8      # RK3566-Generic and RK3566-Powkiddy_x55
  9      echo "image: writing ${SUBDEVICE}_uboot.bin to $(basename "${DISK}")..."
 10      dd if="${RELEASE_DIR}/3rdparty/bootloader/${SUBDEVICE}_uboot.bin" of="${DISK}" bs=512 seek=64 conv=sync,noerror,notrunc >"${SAVE_ERROR}" 2>&1 || show_error
 11    elif [ -f "${RELEASE_DIR}/3rdparty/bootloader/uboot.bin" ]; then
 12      echo "image: writing uboot.bin to $(basename "${DISK}")..."
 13      dd if="${RELEASE_DIR}/3rdparty/bootloader/uboot.bin" of="${DISK}" bs=512 seek=64 conv=sync,noerror,notrunc >"${SAVE_ERROR}" 2>&1 || show_error
 14    elif [ -f "${RELEASE_DIR}/3rdparty/bootloader/u-boot.bin" ]; then
 15      # S922X
 16      echo "image: writing u-boot.bin to $(basename "${DISK}")..."
 17      dd if="${RELEASE_DIR}/3rdparty/bootloader/u-boot.bin" of="${DISK}" bs=512 seek=1 conv=sync,noerror,notrunc >"${SAVE_ERROR}" 2>&1 || show_error
 18    elif [ -f "${RELEASE_DIR}/3rdparty/bootloader/H700_${SUBDEVICE}_u-boot-sunxi-with-spl.bin" ]; then
 19      # H700
 20      echo "image: writing u-boot-sunxi-with-spl.bin to $(basename "${DISK}")..."
 21      dd if="${RELEASE_DIR}/3rdparty/bootloader/H700_${SUBDEVICE}_u-boot-sunxi-with-spl.bin" of="${DISK}" bs=1K seek=8 conv=fsync,notrunc >"${SAVE_ERROR}" 2>&1 || show_error
 22    elif [ -f "${RELEASE_DIR}/3rdparty/bootloader/rocknix-u-boot.img" ]; then
 23      # SM8750, SM8650 & SM8550
 24      echo "image: copying rocknix u-boot files..."
 25      mcopy -o "${RELEASE_DIR}/3rdparty/bootloader/rocknix-u-boot.img" ::
 26      mcopy -s -o "${RELEASE_DIR}/3rdparty/bootloader/device_trees" ::
 27    else
 28      echo "ERROR no u-boot file found for ${SUBDEVICE}"
 29    fi
 30  }
 31  
 32  mkimage_extlinux() {
 33    if [ -d "${RELEASE_DIR}/3rdparty/bootloader/extlinux" ]; then
 34      echo "image: copying custom extlinux.conf..."
 35      mcopy -s -o "${RELEASE_DIR}/3rdparty/bootloader/extlinux" ::
 36    else
 37      local fdt_type
 38      local fdt_overlays
 39      fdt_type=$(get_fdt_type)
 40      fdt_overlays=$(get_fdt_overlays)
 41  
 42      echo "image: set extlinux.conf to $fdt_type /$(get_fdt)..."
 43      mkdir -p "${IMG_TMP}/extlinux"
 44  
 45      cat << EOF > "${IMG_TMP}/extlinux/extlinux.conf"
 46  LABEL ${DISTRO}
 47    LINUX /${KERNEL_NAME}
 48    ${fdt_type} /$(get_fdt)
 49    APPEND boot=LABEL=${DISTRO_BOOTLABEL} disk=LABEL=${DISTRO_DISKLABEL} ${EXTRA_CMDLINE}
 50  EOF
 51  
 52      if [[ -n "${fdt_overlays}" ]]; then
 53        cat << EOF >> "${IMG_TMP}/extlinux/extlinux.conf"
 54    FDTOVERLAYS /overlays/${fdt_overlays}
 55  EOF
 56      fi
 57  
 58      echo "image: copying extlinux.conf..."
 59      mcopy -s -o "${IMG_TMP}/extlinux" ::
 60    fi
 61  }
 62  
 63  mkimage_bootscr() {
 64    if [ -f "${RELEASE_DIR}/3rdparty/bootloader/${SUBDEVICE}_boot.scr" ]; then
 65      echo "image: copying ${SUBDEVICE}_boot.scr..."
 66      mcopy "${RELEASE_DIR}/3rdparty/bootloader/${SUBDEVICE}_boot.scr" ::/boot.scr
 67    else
 68      echo "cannot find ${RELEASE_DIR}/3rdparty/bootloader/${SUBDEVICE}_boot.scr"
 69      exit 2
 70    fi
 71  }
 72  
 73  mkimage_dtb() {
 74    echo "image: copying device trees..."
 75    case "$DEVICE" in
 76      RK3326)
 77        mcopy "${RELEASE_DIR}/3rdparty/bootloader/device_trees/"*.dtb ::
 78        mcopy "${RELEASE_DIR}/3rdparty/bootloader/stock" ::
 79        mcopy "${RELEASE_DIR}/3rdparty/bootloader/overlays" ::
 80        ;;
 81      SM8550|SM8650|SM8750|SM8250|SM6115|SM4450)
 82        mcopy -s -o "${RELEASE_DIR}/3rdparty/bootloader/boot" ::
 83        ;;
 84      S922X)
 85        mcopy "${RELEASE_DIR}/3rdparty/bootloader/"*.dtb ::
 86        ;;
 87      *)
 88        mcopy -s "${RELEASE_DIR}/3rdparty/bootloader/device_trees" ::
 89        ;;
 90    esac
 91  
 92    if [ -d "${RELEASE_DIR}/3rdparty/bootloader/overlays" ]; then
 93      echo "image: copying device tree overlays..."
 94      mcopy -s "${RELEASE_DIR}/3rdparty/bootloader/overlays" ::
 95    fi
 96  }
 97  
 98  mkimage_gou_extras() {
 99    echo "image: copying res..."
100    mcopy "${RELEASE_DIR}/3rdparty/bootloader/res" ::
101  }
102  
103  mkimage_grub() {
104    echo "image: copying grub files and dtb..."
105    mcopy -s -o "${RELEASE_DIR}/3rdparty/bootloader/EFI" ::
106  }
107  
108  mkimage_abl() {
109    echo "image: copying ROCKNIX ABL..."
110    mcopy "${RELEASE_DIR}/3rdparty/bootloader/rocknix_abl" ::
111  }
112  
113  mkimage_all
```


## projects/ROCKNIX/config.xml @ 8ebaf8daad: lines 1-50 (excerpt)

```text
 1  <rocknix>
 2    <H700 dtb_prefix="allwinner">
 3      <DDR4 mkimage_options="dtb,extlinux,uboot" fdt="dtb.img" fdt_type="fdt">
 4          <file>sun50i-h700-anbernic-rg35xx-plus</file>
 5          <file>sun50i-h700-anbernic-rg35xx-plus-rev6-panel</file>
 6          <file>sun50i-h700-anbernic-rg35xx-pro</file>
 7          <file>sun50i-h700-anbernic-rg35xx-h</file>
 8          <file>sun50i-h700-anbernic-rg35xx-h-rev6-panel</file>
 9          <file>sun50i-h700-anbernic-rg35xx-sp</file>
10          <file>sun50i-h700-anbernic-rg35xx-sp-v2-panel</file>
11          <file>sun50i-h700-anbernic-rg35xx-2024</file>
12          <file>sun50i-h700-anbernic-rg35xx-2024-rev6-panel</file>
13          <file>sun50i-h700-anbernic-rg40xx-h</file>
14          <file>sun50i-h700-anbernic-rg40xx-h-v2-panel</file>
15          <file>sun50i-h700-anbernic-rg40xx-v</file>
16          <file>sun50i-h700-anbernic-rg40xx-v-v2-panel</file>
17          <file>sun50i-h700-anbernic-rgcubexx</file>
18          <file>sun50i-h700-anbernic-rg28xx</file>
19          <file>sun50i-h700-anbernic-rg34xx</file>
20          <file>sun50i-h700-anbernic-rg34xx-sp</file>
21          <file>sun50i-h700-anbernic-rg34xx-sp-v2-panel</file>
22          <file>sun50i-h700-anbernic-rg-sp</file>
23      </DDR4>
24      <DDR3 mkimage_options="dtb,extlinux,uboot" fdt="dtb.img" fdt_type="fdt" fdt_overlays="sun50i-h700-anbernic-rg35xx-2024-ddr3.dtbo">
25          <file>sun50i-h700-anbernic-rg35xx-plus</file>
26          <file>sun50i-h700-anbernic-rg35xx-plus-rev6-panel</file>
27          <file>sun50i-h700-anbernic-rg35xx-pro</file>
28          <file>sun50i-h700-anbernic-rg35xx-h</file>
29          <file>sun50i-h700-anbernic-rg35xx-h-rev6-panel</file>
30          <file>sun50i-h700-anbernic-rg35xx-sp</file>
31          <file>sun50i-h700-anbernic-rg35xx-sp-v2-panel</file>
32          <file>sun50i-h700-anbernic-rg35xx-2024</file>
33          <file>sun50i-h700-anbernic-rg35xx-2024-rev6-panel</file>
34          <file>sun50i-h700-anbernic-rg40xx-h</file>
35          <file>sun50i-h700-anbernic-rg40xx-h-v2-panel</file>
36          <file>sun50i-h700-anbernic-rg40xx-v</file>
37          <file>sun50i-h700-anbernic-rg40xx-v-v2-panel</file>
38          <file>sun50i-h700-anbernic-rgcubexx</file>
39          <file>sun50i-h700-anbernic-rg28xx</file>
40          <file>sun50i-h700-anbernic-rg34xx</file>
41          <file>sun50i-h700-anbernic-rg34xx-sp</file>
42          <file>sun50i-h700-anbernic-rg34xx-sp-v2-panel</file>
43          <file>sun50i-h700-anbernic-rg-sp</file>
44      </DDR3>
45    </H700>
46    <RK3326 dtb_prefix="rockchip">
47      <!-- NOTE: DO NOT ADD ANY NEW RK3326 IMAGES -->
48      <!-- see projects/ROCKNIX/devices/RK3326/packages/u-boot/package.mk, function generate_custom_extlinux_conf_files -->
49      <!-- By just adding a new dts, you get an extlinux.conf.<dev_name>.
50           Replace extlinux.conf with it, it's enough to boot your device. -->
```


## distributions/ROCKNIX/config/functions @ 8ebaf8daad: lines 215-232 (excerpt)

```text
215        fi
216      done <${ESTMP}/${SYSTEM_NAME}-emulators.tmp
217    fi
218    add_system_doc ${SYSTEM_NAME}
219  }
220  
221  # config.xml parsing
222  CONFIGXML="${PROJECT_DIR}/${PROJECT}/config.xml"
223  
224  SUBDEVICES=$(xmlstarlet sel -t -m "//rocknix/${DEVICE}/*[@mkimage_options]" -v "name()" -n "${CONFIGXML}" 2>/dev/null | tr '\n' ' ')
225  
226  get_kernel_make_extracmd() {
227    local DTB_PREFIX
228    DTB_PREFIX=$(xmlstarlet sel -t -v "//rocknix/${DEVICE}/@dtb_prefix" "${CONFIGXML}" 2>/dev/null)
229    DTB_PREFIX="${DTB_PREFIX}/"
230    xmlstarlet sel -t -m "//rocknix/${DEVICE}//file" -o "${DTB_PREFIX}" -v "." -o ".dtb " "${CONFIGXML}" 2>/dev/null
231  }
```


## scripts/unpack @ 8ebaf8daad: lines 140-162 (excerpt)

```text
140            [ -f ${patch_dir} ] && PATCH_DIRS_PKG+=" ${patch_dir}"
141            [ -d ${patch_dir} ] && PATCH_DIRS_PKG+=" ${patch_dir}/*.patch"
142          else
143            [ -d ${PKG_DIR}/patches/${patch_dir} ] && PATCH_DIRS_PKG+=" ${PKG_DIR}/patches/${patch_dir}/*.patch"
144            [ -d ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${patch_dir} ] && PATCH_DIRS_PRJ+=" ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${patch_dir}/*.patch"
145            [ -d ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/${patch_dir} ] && PATCH_DIRS_PRJ+=" ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/${patch_dir}/*.patch"
146          fi
147        done
148      fi
149  
150      for i in ${PKG_DIR}/patches/*.patch \
151        ${PKG_DIR}/patches/${PATCH_ARCH}/*.patch \
152        ${PATCH_DIRS_PKG} \
153        ${PKG_DIR}/patches/${PKG_VERSION}/*.patch \
154        ${PKG_DIR}/patches/${PKG_VERSION}/${PATCH_ARCH}/*.patch \
155        ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/*.patch \
156        ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PATCH_ARCH}/*.patch \
157        ${PATCH_DIRS_PRJ} \
158        ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PKG_VERSION}/*.patch \
159        ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/*.patch; do
160  
161        thisdir="${i%/*}"
```


## projects/ROCKNIX/packages/linux/package.mk @ 8ebaf8daad: lines 15-60 (excerpt)

```text
15  
16  PKG_PATCH_DIRS="${LINUX} mainline ${DEVICE} default"
17  
18  [[ "${DEVICE}" == RK* ]] && PKG_PATCH_DIRS+=" mainline-rockchip"
19  [[ "${DEVICE}" == SM* ]] && PKG_DEPENDS_TARGET+=" mkbootimg:host"
20  
21  case ${DEVICE} in
22    RK3588)
23      PKG_VERSION="b8e62bed74766b6c8c423a767b35495e78b64caf"
24      PKG_SHA256="0e0fe5a2f108d525a044e190c3f23a4603cdbf8d54bc1cc488d6ee04b9fc5b3a"
25      PKG_URL="https://github.com/armbian/linux-rockchip/archive/${PKG_VERSION}.tar.gz"
26      PKG_GIT_CLONE_BRANCH="rk-6.1-rkr3"
27      PKG_PATCH_DIRS="${LINUX} ${DEVICE} default"
28      ;;
29    H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)
30      PKG_VERSION="7.2"
31      PKG_SHA256="f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3"
32      PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
33      # Note that the patch dir 7.2 is automatically added as it matches the
34      # version. When we move past 7.2, remember to add 7.2 to patch dirs.
35      ;;
36    RK3326|AMD64|GENERIC_X64)
37      PKG_VERSION="7.1.2"
38      PKG_SHA256="37198c93727be247c9fb5309bb86cd5e496c61e5322cd8c4eca9476bb0b5883f"
39      PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
40      PKG_PATCH_DIRS+=" 7.0"
41      ;;
42    RK3576|RK3566)
43      PKG_VERSION="7.0.2"
44      PKG_SHA256="53591a03294527a48ccb0b9e559e922df8a38554745a1206827ca751d2ca7662"
45      PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
46      PKG_PATCH_DIRS+=" 7.0"
47      ;;
48    S922X|RK3399)
49      PKG_VERSION="6.18.49"
50      PKG_SHA256="ae826f33111fea6f1d279dde7299d7463c8dfd204aeb75a8fb5432bc60a28191"
51      PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
52      ;;
53  esac
54  
55  PKG_KERNEL_CFG_FILE=$(kernel_config_path) || die
56  
57  if [ -n "${KERNEL_TOOLCHAIN}" ]; then
58    PKG_DEPENDS_TARGET+=" gcc-${KERNEL_TOOLCHAIN}:host"
59    HEADERS_ARCH=${TARGET_ARCH}
60  else
```


## projects/ROCKNIX/packages/linux/package.mk @ 8ebaf8daad: lines 218-246 (excerpt)

```text
218  
219      FW_LIST="$(find ${PKG_BUILD}/external-firmware -type f | sed 's|.*external-firmware/||' | sort | xargs)"
220  
221      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
222      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
223    elif [ "${TARGET_ARCH}" = "aarch64" -a "${DEVICE}" = "H700" ]; then
224      mkdir -p ${PKG_BUILD}/external-firmware/rtl_bt
225      mkdir -p ${PKG_BUILD}/external-firmware/rtw88
226      mkdir -p ${PKG_BUILD}/external-firmware/panels
227        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/rtl_bt/rtl8821cs_config.bin ${PKG_BUILD}/external-firmware/rtl_bt
228        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/rtl_bt/rtl8821cs_fw.bin ${PKG_BUILD}/external-firmware/rtl_bt
229        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/rtw88/rtw8821c_fw.bin ${PKG_BUILD}/external-firmware/rtw88
230        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg28xx-panel.panel ${PKG_BUILD}/external-firmware/panels
231        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg34xx-panel.panel ${PKG_BUILD}/external-firmware/panels
232        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg34xx-sp-panel.panel ${PKG_BUILD}/external-firmware/panels
233        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg34xx-sp-v2-panel.panel ${PKG_BUILD}/external-firmware/panels
234        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg35xx-plus-panel.panel ${PKG_BUILD}/external-firmware/panels
235        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg35xx-plus-rev6-panel.panel ${PKG_BUILD}/external-firmware/panels
236        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg35xx-sp-v2-panel.panel ${PKG_BUILD}/external-firmware/panels
237        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg40xx-panel.panel ${PKG_BUILD}/external-firmware/panels
238        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rg40xx-v2-panel.panel ${PKG_BUILD}/external-firmware/panels
239        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/panels/anbernic,rgcubexx-panel.panel ${PKG_BUILD}/external-firmware/panels
240  
241      FW_LIST="$(find ${PKG_BUILD}/external-firmware -type f | sed 's|.*external-firmware/||' | sort | xargs)"
242  
243      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
244      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
245    elif [ "${TARGET_ARCH}" = "aarch64" -a "${DEVICE}" = "SM8650" ]; then
246      mkdir -p ${PKG_BUILD}/external-firmware/qcom
```


## projects/ROCKNIX/packages/linux/package.mk @ 8ebaf8daad: lines 410-432 (excerpt)

```text
410    if [ "${BOOTLOADER}" = "arm-efi" ]; then
411      mkdir -p ${INSTALL}/usr/share/bootloader/boot/grub
412      for dtb in arch/${TARGET_KERNEL_ARCH}/boot/dts/**/*.dtb; do
413        if [ -f ${dtb} ]; then
414            cp -v ${dtb} ${INSTALL}/usr/share/bootloader/boot/grub
415        fi
416      done
417    fi
418  
419    if [ "${BOOTLOADER}" = "u-boot" ]; then
420      mkdir -p ${INSTALL}/usr/share/bootloader
421      for dtb in arch/${TARGET_KERNEL_ARCH}/boot/dts/**/*.dtb; do
422        if [ -f ${dtb} ]; then
423          if [ "${DEVICE}" = "H700" -o "${DEVICE}" = "RK3326" -o "${DEVICE}" = "RK3399" -o "${DEVICE}" = "RK3566" -o "${DEVICE}" = "RK3576" -o "${DEVICE}" = "RK3588" ]; then
424            mkdir -p ${INSTALL}/usr/share/bootloader/device_trees
425            cp -v ${dtb} ${INSTALL}/usr/share/bootloader/device_trees
426          else
427            cp -v ${dtb} ${INSTALL}/usr/share/bootloader
428          fi
429        fi
430      done
431    fi
432  }
```


## projects/ROCKNIX/packages/tools/atf/package.mk @ 8ebaf8daad: lines 1-59 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2018-present Team LibreELEC
 3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 4  
 5  PKG_NAME="atf"
 6  
 7  PKG_ARCH="arm aarch64"
 8  PKG_LICENSE="BSD-3c"
 9  PKG_SITE="https://github.com/ARM-software/arm-trusted-firmware"
10  PKG_DEPENDS_TARGET="toolchain"
11  PKG_LONGDESC="ARM Trusted Firmware is a reference implementation of secure world software, including a Secure Monitor executing at Exception Level 3 and various Arm interface standards."
12  PKG_TOOLCHAIN="manual"
13  PKG_PATCH_DIRS+="${DEVICE}"
14  
15  case ${DEVICE} in
16    H700)
17      PKG_VERSION="2.12.0"
18      PKG_DEPENDS_TARGET+=" h700-suspend-stub"
19      # BL31 embeds the stubs; rebuild when they change
20      PKG_NEED_UNPACK+=" $(get_pkg_directory h700-suspend-stub) ${SYSROOT_PREFIX}/usr/share/h700-suspend-stub"
21    ;;
22    *)
23      PKG_VERSION="2.10.0"
24      PKG_SHA256="696b8e53923aac4474532da7dd681f0bd044b329732facd65aeabea3e61adca9"
25      ;;
26  esac
27  
28  PKG_URL="https://github.com/ARM-software/arm-trusted-firmware/archive/v${PKG_VERSION}.tar.gz"
29  
30  
31  [ -n "${KERNEL_TOOLCHAIN}" ] && PKG_DEPENDS_TARGET+=" gcc-${KERNEL_TOOLCHAIN}:host"
32  
33  if [ "${ATF_PLATFORM}" = "rk3399" ]; then
34    PKG_DEPENDS_TARGET+=" gcc-arm-none-eabi:host"
35    export M0_CROSS_COMPILE="${TOOLCHAIN}/bin/arm-none-eabi-"
36  fi
37  
38  make_target() {
39    if [ "${DEVICE}" = "H700" ]; then
40      STUB_DIR="${SYSROOT_PREFIX}/usr/share/h700-suspend-stub"
41      ATF_SUSPEND="SUNXI_SYSTEM_SUSPEND=1 SUNXI_SUSPEND_STUB=${STUB_DIR}/suspend_stub_lpddr4.bin"
42      ATF_SUSPEND+=" SUNXI_SUSPEND_STUB2=${STUB_DIR}/suspend_stub_lpddr3.bin"
43    fi
44  
45    CROSS_COMPILE="${TARGET_KERNEL_PREFIX}" LDFLAGS="" CFLAGS="" make PLAT=${ATF_PLATFORM} ${ATF_SUSPEND} bl31
46  }
47  
48  makeinstall_target() {
49    mkdir -p ${INSTALL}/usr/share/bootloader
50    cp -a build/${ATF_PLATFORM}/release/${ATF_BL31_BINARY} ${INSTALL}/usr/share/bootloader
51  
52    # u-boot embeds BL31 at build time. It read it straight out of this package's
53    # build directory, which neither survives AUTOREMOVE nor crosses a CI job
54    # boundary. Stage it in the sysroot, which is carried between jobs.
55    if [ -n "${ATF_BL31_BINARY}" ]; then
56      mkdir -p ${SYSROOT_PREFIX}/usr/share/${PKG_NAME}
57      cp -a build/${ATF_PLATFORM}/release/${ATF_BL31_BINARY} ${SYSROOT_PREFIX}/usr/share/${PKG_NAME}
58    fi
59  }
```


## projects/ROCKNIX/packages/tools/atf/package.mk @ 651150fc88: lines 1-35 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2018-present Team LibreELEC
 3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 4  
 5  PKG_NAME="atf"
 6  
 7  PKG_ARCH="arm aarch64"
 8  PKG_LICENSE="BSD-3c"
 9  PKG_SITE="https://github.com/ARM-software/arm-trusted-firmware"
10  PKG_DEPENDS_TARGET="toolchain"
11  PKG_LONGDESC="ARM Trusted Firmware is a reference implementation of secure world software, including a Secure Monitor executing at Exception Level 3 and various Arm interface standards."
12  PKG_TOOLCHAIN="manual"
13  PKG_PATCH_DIRS+="${DEVICE}"
14  
15  case ${DEVICE} in
16    H700)
17      PKG_VERSION="2.12.0"
18      PKG_SHA256="d95aaf292792c98035910d7e6c64ebfb297c897fef510415db1612f6d39f9223"
19      PKG_DEPENDS_TARGET+=" h700-suspend-stub"
20      # BL31 embeds the stubs; rebuild when they change
21      PKG_NEED_UNPACK+=" $(get_pkg_directory h700-suspend-stub) ${SYSROOT_PREFIX}/usr/share/h700-suspend-stub"
22    ;;
23    *)
24      PKG_VERSION="2.10.0"
25      PKG_SHA256="6b1d5e89c311c5e7eaeb062713953311464c0378ab3e4ebc7ede72a746964bb1"
26      ;;
27  esac
28  
29  PKG_URL="https://github.com/TrustedFirmware-A/trusted-firmware-a/archive/v${PKG_VERSION}.tar.gz"
30  
31  
32  [ -n "${KERNEL_TOOLCHAIN}" ] && PKG_DEPENDS_TARGET+=" gcc-${KERNEL_TOOLCHAIN}:host"
33  
34  if [ "${ATF_PLATFORM}" = "rk3399" ]; then
35    PKG_DEPENDS_TARGET+=" gcc-arm-none-eabi:host"
```


## projects/ROCKNIX/packages/tools/atf/package.mk @ feature/m6-build-engine-652: lines 1-35 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2018-present Team LibreELEC
 3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 4  
 5  PKG_NAME="atf"
 6  
 7  PKG_ARCH="arm aarch64"
 8  PKG_LICENSE="BSD-3c"
 9  PKG_SITE="https://github.com/ARM-software/arm-trusted-firmware"
10  PKG_DEPENDS_TARGET="toolchain"
11  PKG_LONGDESC="ARM Trusted Firmware is a reference implementation of secure world software, including a Secure Monitor executing at Exception Level 3 and various Arm interface standards."
12  PKG_TOOLCHAIN="manual"
13  PKG_PATCH_DIRS+="${DEVICE}"
14  
15  case ${DEVICE} in
16    H700)
17      PKG_VERSION="2.12.0"
18      PKG_SHA256="30abf4da07418ad0f840369c3e64dc6a0bc6a936d53a213ce10783f3d1a3430f"
19      PKG_DEPENDS_TARGET+=" h700-suspend-stub"
20      # BL31 embeds the stubs; rebuild when they change
21      PKG_NEED_UNPACK+=" $(get_pkg_directory h700-suspend-stub) ${SYSROOT_PREFIX}/usr/share/h700-suspend-stub"
22    ;;
23    *)
24      PKG_VERSION="2.10.0"
25      PKG_SHA256="696b8e53923aac4474532da7dd681f0bd044b329732facd65aeabea3e61adca9"
26      ;;
27  esac
28  
29  PKG_URL="https://github.com/ARM-software/arm-trusted-firmware/archive/v${PKG_VERSION}.tar.gz"
30  
31  
32  [ -n "${KERNEL_TOOLCHAIN}" ] && PKG_DEPENDS_TARGET+=" gcc-${KERNEL_TOOLCHAIN}:host"
33  
34  if [ "${ATF_PLATFORM}" = "rk3399" ]; then
35    PKG_DEPENDS_TARGET+=" gcc-arm-none-eabi:host"
```


## scripts/get_archive @ feature/m6-build-engine-652: lines 1-66 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0-only
 2  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
 3  
 4  # An archive is used only when its bytes match the recipe's PKG_SHA256, and it is
 5  # fetched over verified TLS: a recipe without a checksum fails here, before the
 6  # cache or the network is consulted (D-WORKFLOW-193, #834).
 7  if [ -z "${PKG_SHA256}" ]; then
 8    die "\nCannot get ${1} sources: its recipe has no PKG_SHA256, so the archive cannot be verified (D-WORKFLOW-193)"
 9  fi
10  
11  _get_file_already_downloaded() {
12    { [ ! -f "${PACKAGE}" ] || [ ! -f "${STAMP_URL}" ] || [ ! -f "${STAMP_SHA}" ]; } && return 1
13    [ "$(cat ${STAMP_SHA} 2>/dev/null)" != "${PKG_SHA256}" ] && return 1
14    return 0
15  }
16  
17  # Latest file already present, exit now...
18  _get_file_already_downloaded && exit 0
19  
20  lock_source_dir "${1}"
21  
22  # Check again in case of concurrent access - if nothing needs to be downloaded, exit now...
23  _get_file_already_downloaded && exit 0
24  
25  # At this point, we need to download something...
26  build_msg "CLR_GET" "GET" "${1} (archive)" "indent"
27  
28  pkg_lock_status "GETPKG" "${PKG_NAME}" "unpack" "downloading package..."
29  
30  PACKAGE_MIRROR="${DISTRO_MIRROR}/${PKG_SOURCE_NAME}"
31  [ "${VERBOSE}" != "yes" ] && WGET_OPT=-q
32  WGET_CMD="wget --secure-protocol=TLSv1_2 --output-file=- --timeout=30 --tries=3 --passive-ftp -c ${WGET_OPT} --progress=bar:force --retry-connrefused --waitretry=5 --retry-on-http-error=429,500,502,503,504 --show-progress -O ${PACKAGE}"
33  
34  # unset LD_LIBRARY_PATH to stop wget from using toolchain/lib and loading libssl.so/libcrypto.so instead of host libraries
35  unset LD_LIBRARY_PATH
36  
37  rm -f "${STAMP_URL}" "${STAMP_SHA}"
38  
39  PKG_URLS="${PKG_URL}"
40  if [ -n "${PACKAGE_MIRROR}" ]
41  then
42    PKG_URLS="${PKG_URL} ${PACKAGE_MIRROR}"
43  fi
44  
45  NBWGET=10
46  while [ ${NBWGET} -gt 0 ]; do
47    for url in ${PKG_URLS}; do
48      rm -f "${PACKAGE}"
49      if ${WGET_CMD} "${url}"; then
50        CALC_SHA256=$(sha256sum "${PACKAGE}" | cut -d" " -f1)
51  
52        [ "${PKG_SHA256}" = "${CALC_SHA256}" ] && break 2
53  
54        build_msg "CLR_WARNING" "WARNING" "Incorrect checksum calculated on downloaded file: got ${CALC_SHA256} wanted ${PKG_SHA256}"
55      fi
56    done
57    NBWGET=$((NBWGET - 1))
58  done
59  
60  if [ ${NBWGET} -eq 0 ]; then
61    die "\nCannot get ${1} sources : ${PKG_URL}\nTry later!"
62  else
63    build_msg "CLR_INFO" "INFO" "Calculated checksum: ${CALC_SHA256}"
64    echo "${PKG_URL}" > "${STAMP_URL}"
65    echo "${CALC_SHA256}" > "${STAMP_SHA}"
66  fi
```


## projects/ROCKNIX/packages/sysutils/busybox/scripts/init @ 8ebaf8daad: lines 420-440 (excerpt)

```text
420        result="$(dd if="${UPDATE_DIR}/$2" of="$3" 2>&1)"
421        StopProgress "done"
422        sync
423      echo "${result}"
424    fi
425  }
426  
427  update_bootloader() {
428    local result
429  
430    export BOOT_ROOT="/flash"
431    export SYSTEM_ROOT="/update"
432    if [ -f ${SYSTEM_ROOT}/usr/share/bootloader/update.sh ]; then
433      echo ""
434      echo "Updating Boot Files... "
435      sh ${SYSTEM_ROOT}/usr/share/bootloader/update.sh
436      sync
437      echo "Boot Files Updated."
438      echo ""
439    fi
440  }
```
