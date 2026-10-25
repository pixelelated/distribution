# Research notes — M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

## Scope

- **The read hash:** `8ebaf8daad`; the 28 are byte-equal at the dispatch tip `ed7fd0ea50`. **`reviewed-at`:** `ed7fd0ea50`. **Upstream:** `651150fc88`, read locally.
- **The membership:** brief § 2's block, run at P1's `2174265e9c` (`stage-a/scope.sh`, r01):

  ```text
  paths 28 lines 12901
  read 8 327 fork-own 0
  tier {'upstream-carried': 27, 'vendor-carried': 1} reach {'shipped': 28}
  language {'shell': 2, 'other': 2, 'udev': 2, 'devicetree': 15, 'kernel-config': 1, 'recipe': 4, 'none': 2}
  written 28 .qa-scratch/t27/paths.txt
  ```

  - The 28 are in `stage-a/paths.txt`.
  - **The 15 device-tree sources (321 lines) are read here** though the survey's language rule does not count them as read.
- **The configuration has a base: upstream's own copy.** `projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf` is 8,129 lines, with the header `# Linux/arm64 7.2.0 Kernel Configuration`. Against `651150fc88`'s copy it is **12 lines removed and 13 added** (r03). The difference is two things:
  - the fork's one commit since the merge base `c445081a59`, `cbf75c0b06` (2026-09-10; D-SYS-002/003/004);
  - upstream's four since: `c0980b2b71`, `5f56cd5150`, `6fbefc45c6` and `dcafa74090` (r04, r05).

  The order's *fork-written* and the futro's guess that this configuration would meet T11's question are errata.
- **The history since 2026-06-01** (`--since='2026-06-01T00:00:00Z'`): **29** non-merge commits on the 28; **1 fork-authored** (`cbf75c0b06`, Max Engel), **28 upstream**. A bare `--since=2026-06-01` reads the date at the current time of day, and at 08:10 it printed 28 / 1 / 27, excluding `efae8a5653` (committed 2026-06-01T08:07:03Z) (`00`).
- **The upstream delta** at `651150fc88`: **1 D**, `filesystem/usr/lib/udev/rules.d/80-clock.rules`; **2 M**, `linux/linux.aarch64.conf` and `options` (r15).

## Phase 1

What each read file does, from its bytes at `8ebaf8daad`. The rest of the 28 are in `02` § Coverage.

| File | What it does |
| --- | --- |
| `options` | The device's knobs: cortex-a53 with `+crc+fp+simd` (aarch64) and a `crypto-neon-fp-armv8` FPU (arm); the `Image` kernel; u-boot with atf `sun50i_h616`; panfrost; Wayland with sway; out-of-tree trees and overlays; zram and swap 0. |
| `bootloader/update.sh` | On an update: copies the trees and overlays to `/flash`, writes `/dtb.img` from the running tree's dt-id, picks the DDR3 or DDR4 loader by `vdd-dram`'s voltage, and `dd`s it at 8 KiB. |
| `filesystem/.../80-clock.rules` | Sets the system clock from `rtc0` at boot. |
| `filesystem/.../wlan0.powersave.off.rules` | Turns off Wi-Fi power saving on the SDIO chip. |
| `packages/u-boot/package.mk` | The wrapper: depends on `u-boot-<SUBDEVICE>` for each SUBDEVICE and installs each loader as `H700_<sub>_u-boot-sunxi-with-spl.bin`. |
| `packages/u-boot-DDR3/package.mk`, `u-boot-DDR4/package.mk` | u-boot `v2026.01` built with atf's BL31 for the LPDDR3 and LPDDR4 defconfigs; the loader is staged in the sysroot. |
| `packages/h700-suspend-stub/package.mk` | Builds one SRAM suspend stub per memory type from each u-boot recipe's defconfig, refusing two with the same DRAM type and clock; atf embeds them. Line 43 is read masked. |
