"""Write T27's coverage table: one row per path in stage-a/rows.json."""
import json
import sys

rows = json.load(open(sys.argv[1]))
H = "projects/ROCKNIX/devices/H700/"
SHIPPED_TREES = {
    "sun50i-h700-anbernic-rg-sp.dts": "the RG SP's tree (its `rocknix-dt-id`; device-facts L16, *DDR3 bootloader/RG SP tree*)",
    "sun50i-h700-anbernic-rg35xx-sp-v2-panel.dts": "an RG35XX SP tree (the v2 panel). The other is mainline's `rg35xx-sp`, whose dt-id comes from kernel patch 0154 (T41's). Device-facts L15 does not say which the LPDDR4 unit boots",
}
NOTES = {
    H + "bootloader/update.sh": ("The in-place updater, run by the shipped `init` on an update: copies `device_trees` and `overlays` to `/flash` (`:21-24`), writes `/dtb.img` from `/proc/device-tree/rocknix-dt-id` (`:26-32`), picks the loader by `vdd-dram` (1,200,000 µV DDR3, 1,100,000 µV DDR4, `:34-49`) and `dd`s it at `bs=1K seek=8` (`:51-57`). Any other voltage, or a failed read, writes no loader.", "§ The loader and the tree; F-04; Q3 not a bug", "tree"),
    H + "config/kernel-firmware.dat": ("The H700 firmware list (13 files: rtw88, rtl8821cs BT, ten panels). The recipe also builds the same 13 into the kernel (`linux/package.mk:223-243`).", "F-05 (duplicates); T5's F-17, the stamp (#836)", "tree"),
    H + "filesystem/usr/lib/udev/rules.d/80-clock.rules": ("Sets the clock from `rtc0` (PCF8563) at boot (`hwclock --hctosys`).", "F-08: deleted upstream (`899193e5af`), settled by the next base merge", "tree"),
    H + "filesystem/usr/lib/udev/rules.d/wlan0.powersave.off.rules": ("Turns off Wi-Fi power saving on the SDIO chip at `mmc2:0001:1`.", "carried; no finding", "tree"),
    H + "linux/linux.aarch64.conf": ("The kernel configuration, `Linux/arm64 7.2.0`, 8,129 lines; upstream's file with a base, its own copy at `651150fc88` (12 / 13 lines apart).", "§ The configuration; the order's *fork-written* an erratum", "tool-run"),
    H + "options": ("Device knobs: cortex-a53 with `+crc+fp+simd` on aarch64, `crypto-neon-fp-armv8` FPU on arm (`:7-19`); `BOOTLOADER=\"u-boot\"` (`:34`); atf `sun50i_h616` (`:37-39`); panfrost; zram and swap 0 (`:77-84`). Upstream changes the ZRAM algorithm and adds `THP_DEFRAG`.", "F-03 (the SIMD flags against the rule's table); F-09 (Q7)", "tree"),
    H + "packages/h700-suspend-stub/package.mk": ("Builds one SRAM suspend stub per memory type from each u-boot recipe's defconfig (`:20-47`), refusing two stubs with the same DRAM type and clock (`:42-45`). Pin `712653d11230`. Line 43 matches the credential read filter and is read masked.", "§ The pins", "tree"),
    H + "packages/u-boot-DDR3/package.mk": ("u-boot `v2026.01` for the LPDDR3 defconfig, its SPL embedding atf's BL31.", "§ The pins; F-10", "tree"),
    H + "packages/u-boot-DDR3/sources/configs/anbernic_rg35xx_h700_lpddr3_defconfig": ("The LPDDR3 board defconfig; 20 lines from the LPDDR4 one (DRAM timing, `H616_LPDDR3`, `AXP_DCDC3_VOLT=1200`).", "carried; no finding", "tree"),
    H + "packages/u-boot-DDR4/package.mk": ("u-boot `v2026.01` for the LPDDR4 defconfig; differs from DDR3's in `PKG_NAME` and `PKG_UBOOT_CONFIG` only.", "§ The pins; F-10", "tree"),
    H + "packages/u-boot-DDR4/sources/configs/anbernic_rg35xx_h700_lpddr4_defconfig": ("The LPDDR4 board defconfig (`H616_LPDDR4`, `AXP_DCDC3_VOLT=1100`).", "carried; no finding", "tree"),
    H + "packages/u-boot/package.mk": ("The wrapper: depends on `u-boot-${SUBDEVICE}` for each SUBDEVICE from `config.xml` (DDR3, DDR4) and installs `H700_<sub>_u-boot-sunxi-with-spl.bin` (`:16-35`).", "§ The pins; F-10", "tree"),
    H + "patches/linux/0203-sound-soc-Add-sunxi_v2-for-h616-ahub.patch.disabled": ("A 4,036-line patch (tiopex, 2025-05-29) no build applies: `scripts/unpack:143-159` globs `*.patch`. Added as `.disabled` by `fad6d7d27a`. The inventory reads it `shipped`.", "F-06; the reach is #1086's shape", "tree"),
}


def note(path):
    if path in NOTES:
        return NOTES[path]
    base = path.rsplit("/", 1)[1]
    if base in SHIPPED_TREES:
        return ("A fork-tree board file, compiled into `device_trees` on every H700 image: " + SHIPPED_TREES[base] + ".", "shipped unit", "tree")
    return ("A fork-tree board file for an H700 handheld the fork does not ship, compiled into `device_trees` on every H700 image.", "carried by placement (D-WORKFLOW-185)", "tree")


print("| Path | Tier | Reach | Lines | What it is, and who reads it | Finding or disposition | proved |")
print("| --- | --- | --- | ---: | --- | --- | --- |")
for r in rows:
    what, disp, proved = note(r["path"])
    tier = r["tier"] + (f" ({r['tier_note']})" if r["tier_note"] else "")
    print("| `%s` | %s | %s | %s | %s | %s | %s |" % (r["path"], tier, r["reach"], r["lines"], what, disp, proved))
