# Second opinion (Phase 4.6), M6 T28: the SM8550 device of pixelelated/distribution

You are the one independent reviewer for a read-only currency audit of 29 paths at commit `8ebaf8daad`: the SM8550 device directory (`projects/ROCKNIX/devices/SM8550/`), whose shipped unit is the Retroid Pocket Nova. The first reader is another lab's model. Its `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md` are included below, followed by the context sections and the files, line-numbered.

- **Upstream** is read at `651150fc88`, which replaces the SM8550 boot path.
- **Masking.** Every file was passed through a masking `sed` that replaces a value after `key=`, `token=`, `user=`, `pass...=` or `psk=` with `***`; treat `***` as an unknown value.
- **The lens** is currency, under cost against value.
- **Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong.
- **No one can run anything on the Nova.** A fact only the unit can show is a device-facts row, quoted in the context, and is otherwise an open item to test.

Answer these first, in this order:

1. **The pins and the superseded path (`02` § The pins, F-01, F-02).**
   - Are the eight pins as stated at both hashes: identical, differs, absent or deleted?
   - Is it right that every unit of the `qcom-abl` boot path changes upstream (`cafbb1657d` and its neighbours)?
   - Is the loader entry's name, `${DISTRONAME,,}.conf` from `virtual/arm-efi` (`pixelelated.conf` on the fork, with `boot=LABEL=ROCKNIX`), the identity seam the first reader says?
   - What else must the merge answer that the first reader did not name?
2. **The configuration (`02` § The configuration).** Is every one of the 14 diff lines attributed correctly, and is anything in them a behaviour change for the Nova rather than a toolchain stamp?
3. **The loader and the tree (`02` § The loader and the tree, F-04, F-05, F-08).**
   - Trace a build: are exactly the fourteen `config.xml` dtbs built (through `get_kernel_make_extracmd`) and appended to `kernel.gz` (`linux/package.mk:392-396`)?
   - Is `mkimage_abl` the only `mkimage_all` step for SM8550?
   - Are the two SM8550-naming branches of `bootloader/mkimage` really never run?
   - Trace an update: does `update.sh` hand `updateabl` anything that would make it write a loader it should not, as F-04 says it does not? Is the first reader right that the guard is inside `updateabl` (`:9-36`)?
   - Is the card's `/flash/rocknix_abl/` copy read by anything but the README's manual procedure?
4. **The firmware (F-03).** SM8550's six firmware entries are installed as files by `kernel-firmware/package.mk:39-70`, and the kernel embeds none (`linux/package.mk:83`, `:208-277`), unlike SM8250, SM8650 and SM8750, with `DRM_MSM=y` in all four.
   - Is "a divergence, observed working" right?
   - Is there a boot-order case where a built-in driver asks for its firmware before the root filesystem is mounted and does not retry? Name the driver and the line if so.
5. **The Nova's files (`02` § Deltas 2 and 3, F-07).** Is it right that `02-ayn-controller.yaml` and `ayn_mcu.yaml` serve the Nova, and that `rp6.dts` and `ayn-common.dtsi` are its include chain? Are any of the thirteen *carried by placement* trees or seven input files actually used by the Nova?

Then:

6. **Refute or confirm each finding F-01 to F-08** in `02` § Findings: *confirmed*, *narrowed* (say how), or *refuted* (with the line).
7. **What the first reader missed.** Look for:
   - a defect in `update.sh` (it runs as root on a person's handheld, writing to the boot partition) or in the hand-off to `updateabl`;
   - a tree that references a node or a label its include chain does not define;
   - anything in `options` that is inconsistent with the boot path or the configuration;
   - any reason the shipped image could pick a tree other than the Nova's from the fourteen.

**Output:** numbered items `G-1`, `G-2`, ..., each with one line saying *confirmed / narrowed / refuted / new*, the `file:line` evidence, and two to five sentences. Group them under the seven headings above. Do not restate the packet, and do not reproduce long code. Keep the whole reply under about 8,000 words.


## The first reader's 02-forward-audit.md (whole)

# Forward audit — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

## Running notes

- **What this is.** A currency slice over the 29 paths of `projects/ROCKNIX/devices/SM8550/` that are not T41's. Upstream carries every one, and no fork author has touched any of them since the base. The Nova (the Retroid Pocket Nova) is the shipped unit. The lens is currency, under cost against value: the eight pins, read from recipes outside the slice; the configuration's shape; the boot path by line; and upstream's October replacement of that path.
- **The read.** The bytes are `8ebaf8daad`'s; the branch differs from them on none of the 29 (r03). Upstream is read at `651150fc88` by name, from the repository's own store; no fetch. No file under `packages/`, `projects/` or `tools/` changes at stages A to D (r31).
- **The bench.** *Can this be done on the VM? Yes, on the host, with no network.* No guest is asked for: the guest cannot be an SM8550. **Nothing ran on the Nova.** The seven device-facts rows are its physical facts, cited by their Fact cells.
- **The runs.** Stage A's 31 runs are in `stage-a/`, with exits and wall times in `runs.tsv`. Stage B's 21 reads behind the sections below are in `stage-b/` (`reads.sh`, b01 to b20 and `g_check`, all rc 0). § The runs, § The pins, § The device trees and § Coverage are regenerated by `tools/t28-tables.py`, between marked blocks; `check` exits 1 when one differs from a fresh run.

## Deltas from the brief

1. **r08's pairs are reversed.** The brief's command prints `SM8650 41/36 SM8750 81/105 SM6115 228/133 SM4450 229/189 SM8250 371/204`; the brief's text gives each pair the other way round. The counts agree.
2. **Two of the nine filesystem files serve the Nova.** The brief says *"none the Nova's"*. But `filesystem/usr/share/inputplumber/devices/02-ayn-controller.yaml:44` matches `value: Retroid Pocket Nova`, the Nova's tree's `model` line exactly (`qcs8550-retroidpocket-rpnova.dts:11`). Its `capability_map_id: ayn_mcu` takes `capability_maps/ayn_mcu.yaml`. That fits device fact L28, where the physical *AYN Odin2 Gamepad* node is what InputPlumber hides. So those two are *shipped unit*, and seven are carried by placement.
3. **The Nova's include chain is part of the shipped unit.** `rpnova.dts:8` includes `qcs8550-retroidpocket-rp6.dts`, which includes `qcs8550-ayn-common.dtsi`. Those two trees build the Nova's dtb: *shipped unit (the Nova uses it)*. 13 trees are carried by placement.
4. **`gamepadcalibration`'s pin is identical, but the file is not.** Upstream's `48b98a02d7` (2026-09-27) changes the SM6115 branch of `makeinstall_target` only. SM8550's lines are unchanged.

## § The runs

Every § 5 command, from `stage-a/runs.sh` (10:32:32 to 10:32:33 UTC), with its exit, wall time, figure and what a FAIL would mean. **All exit 0.** The `grep -c` steps that could print 0 are wrapped (`|| true`, or a `wc -l` count), so no step exits 1 on the expected 0.

<!-- begin t28:runs -->
| Run (`stage-a/runs.sh`) | Exit | Seconds | Started (UTC) | Figure (first line of `stage-a/<run>.out`) | A FAIL would mean |
| --- | ---: | ---: | --- | --- | --- |
| `r01_block` | 0 | 0.51 | 10:32:32 | `paths 29 lines 28053 {'shipped': 29} {'upstream-carried': 29} (+33 lines)` | an inventory change, or a glob that picks up T41's rows |
| `r02_paths` | 0 | 0.00 | 10:32:32 | `29` | a membership other than the 29 |
| `r03_branch_vs_hash` | 0 | 0.01 | 10:32:32 | `[]` | an edit on this branch to one of the 29 |
| `r04_lines` | 0 | 0.06 | 10:32:32 | `28053` | an inventory line count that is not the tree's |
| `r05_disabled` | 0 | 0.01 | 10:32:32 | `20593` | a renamed, shortened or enabled patch |
| `r06_conf_head` | 0 | 0.01 | 10:32:32 | `# Linux/arm64 7.2.0 Kernel Configuration (+1 lines)` | a configuration for another kernel than the recipe's |
| `r07_conf_diff` | 0 | 0.01 | 10:32:32 | `removed=7 added=7 (+14 lines)` | a fork line in the configuration, or upstream regenerating it with new options |
| `r08_conf_distance` | 0 | 0.05 | 10:32:32 | `SM8650 41/36 SM8750 81/105 SM6115 228/133 SM4450 229/189 SM8250 371/204 ` | a different distance between the Qualcomm configurations |
| `r09_conf_fork` | 0 | 0.01 | 10:32:32 | `0` | a fork commit on the configuration since the base |
| `r10_conf_upstream` | 0 | 0.01 | 10:32:32 | `dcafa74090 2026-10-22 spycat88 linux: kernel config (+3 lines)` | an upstream commit other than the four |
| `r11_kernel_case` | 0 | 0.01 | 10:32:32 | `1:  H700\|SM4450\|SM6115\|SM8250\|SM8550\|SM8650\|SM8750) (+5 lines)` | SM8550 moved to another kernel branch, at either hash |
| `r12_pins` | 0 | 0.04 | 10:32:32 | `tools/qcom-abl 8ebaf8daad: PKG_VERSION="1.0" PKG_URL=""  (+13 lines)` | a pin other than the table's, at either hash |
| `r13_rocknix_abl_log` | 0 | 0.00 | 10:32:33 | `9aa7affee9 2026-10-15 blitterbot rocknix-abl: apply upstream v1.2 checksum fix (#600) (+2 lines)` | a setting commit other than the brief's |
| `r14_openabl` | 0 | 0.01 | 10:32:33 | `PKG_VERSION="1.2" (+4 lines)` | openabl at another version, or another history |
| `r15_update_sh` | 0 | 0.00 | 10:32:33 | `10:if [ -z "$BOOT_DISK" ]; then (+8 lines)` | a changed updater: another copy, no `updateabl`, no cleanup |
| `r16_scripts_mkimage` | 0 | 0.00 | 10:32:33 | `137:if [ "${BOOTLOADER}" = "syslinux" -o "${BOOTLOADER}" = "bcm2835-bootloader" -o "${BOOTLOADER}" = "u-boot"  (+3 lines)` | the `qcom-abl` branch moved or gone |
| `r17_bootloader_mkimage` | 0 | 0.00 | 10:32:33 | `22:  elif [ -f "${RELEASE_DIR}/3rdparty/bootloader/rocknix-u-boot.img" ]; then (+4 lines)` | a third SM8550 branch, or one of the two gone |
| `r18_kernel_abl_branch` | 0 | 0.00 | 10:32:33 | `5:    gzip -c "arch/${TARGET_KERNEL_ARCH}/boot/${KERNEL_TARGET}" > "${INSTALL}/.image/kernel.gz" (+5 lines)` | the boot image built another way (no dtb append, no mkbootimg) |
| `r19_embed_blocks` | 0 | 0.00 | 10:32:33 | `1:elif [ "${DEVICE}" = "SM8250" -o "${DEVICE}" = "H700" -o "${DEVICE}" = "SM8650" -o "${DEVICE}" = "SM8750" ]; (+11 lines)` | an SM8550 embed block in the kernel recipe |
| `r20_config_xml` | 0 | 0.00 | 10:32:33 | `14` | a tree list other than fourteen |
| `r21_updateabl` | 0 | 0.00 | 10:32:33 | `echo "Checksum abl_b: ${SUM_B:0:7}" (+11 lines)` | `updateabl` writing without the compare, or one slot only |
| `r22_dts_count` | 0 | 0.00 | 10:32:33 | `16` | a tree added or removed |
| `r23_nova_dts` | 0 | 0.00 | 10:32:33 | `8:#include "qcs8550-retroidpocket-rp6.dts" (+3 lines)` | another include, model or compatible for the Nova |
| `r24_dt_id` | 0 | 0.02 | 10:32:33 | `     16 0` | a tree carrying `rocknix-dt-id` |
| `r25_history` | 0 | 0.07 | 10:32:33 | `24 (+4 lines)` | a fork author on the 29, or a different upstream count |
| `r26_fork_since_base` | 0 | 0.02 | 10:32:33 | `0 (+2 lines)` | a fork non-merge commit on the directory since the base |
| `r27_delta_29` | 0 | 0.01 | 10:32:33 | `M	projects/ROCKNIX/devices/SM8550/bootloader/update.sh (+2 lines)` | an upstream delta over the 29 other than 2 M |
| `r28_delta_dir` | 0 | 0.01 | 10:32:33 | `M	projects/ROCKNIX/devices/SM8550/bootloader/update.sh (+6 lines)` | an upstream delta over the directory other than 4 M 2 A |
| `r29_boot_change` | 0 | 0.01 | 10:32:33 | `651150fc88 2026-10-24 Merge pull request #3547 from spycat88/qcom-bls (+17 lines)` | a different set of upstream boot-path commits |
| `r30_makefile` | 0 | 0.00 | 10:32:33 | `39:world AMD64 RK3588 RK3576 S922X RK3566 RK3326 RK3399 H700 SM4450 SM6115 SM8250 SM8550 SM8650 SM87 (+7 lines)` | SM8550 out of `world`, or another default device |
| `r31_removal_rule` | 0 | 0.00 | 10:32:33 | `[]` | a change under `packages/`, `projects/` or `tools/` since the dispatch tip |
<!-- end t28:runs -->

## § The pins

The eight pinned units, each read from its recipe outside the slice at both hashes. `CANNOT (no network)` for every author's current release. That check is `tools/fork-package-freshness`'s at the RC (D-WORKFLOW-024), named here, not run. *Set by* is `git log -1 -S` on the pin string. For the kernel, that is the last commit that changed the count of `PKG_VERSION="7.2"` in the recipe, which may be another branch's line.

<!-- begin t28:pins -->
| Unit | Recipe (outside the slice) and the reference | At `8ebaf8daad` | At `651150fc88` | Set by (`git log -1 -S`) | Author's current release |
| --- | --- | --- | --- | --- | --- |
| qcom-abl | `projects/ROCKNIX/packages/tools/qcom-abl/package.mk`; `options:34` `BOOTLOADER="qcom-abl"` | `1.0`, no sha | identical file | version 7a656ea09d 2026-01-29 | n/a (`PKG_URL=""`, a meta recipe) |
| rocknix-abl | `projects/ROCKNIX/packages/tools/rocknix-abl/package.mk`; `options:66` `ADDITIONAL_PACKAGES` | `1.2`, sha `64034fb076ea...` | **absent**: replaced by `openabl` `1.2` (71d8932b33 2026-10-14, a5d0dd4d57 2026-10-19, 73ffb8ee37 2026-10-24) | version b354bfe6d6 2026-09-30; sha 9aa7affee9 2026-10-15 blitterbot | CANNOT (no network) |
| the kernel | `projects/ROCKNIX/packages/linux/package.mk`; `linux/package.mk:29-35` (`H700\|SM4450\|SM6115\|SM8250\|SM8550\|SM8650\|SM8750)`) | `7.2`, sha `f9fef3d14c0d...` | the same pin; the file differs | version 00503e20c0 2026-08-22; sha e0a68c95bd 2026-08-25 spycat88 | CANNOT (no network) |
| mkbootimg | `projects/ROCKNIX/packages/tools/mkbootimg/package.mk`; `linux/package.mk:19` (`SM*` host tool) | `d2bb0af5ba6d...`, sha `418bb875c03d...` | **deleted** (`cafbb1657d`) | version 7a656ea09d 2026-01-29; sha e0a68c95bd 2026-08-25 spycat88 | CANNOT (no network) |
| extra-firmware | `projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk`; `options:63` `FIRMWARE` | `88b363e67d4f...`, sha `1b253d1a79ed...` | **differs**: `925dfb5efbe5...`, sha `b994fa1c4517...` | version 675c364c6d 2026-09-13 | CANNOT (no network) |
| kernel-firmware | `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk`; the ROCKNIX override; installs `config/kernel-firmware.dat` | `20260309`, sha `28fb1b57fa95...` | identical file | version 321ded3d39 2026-03-18; sha e0a68c95bd 2026-08-25 spycat88 | CANNOT (no network) |
| inputplumber | `projects/ROCKNIX/packages/tools/inputplumber/package.mk`; `options:66` | `v0.79.0`, sha `123c858139d3...` | **differs**: `0.82.0`, sha `aaee9b65b47a...` | version cbfb618679 2026-09-05 | CANNOT (no network) |
| gamepadcalibration | `projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk`; `options:66` | `2077e7af7e9a...`, sha `f14730170a41...` | the same pin; the file differs | version 959a9260de 2026-04-28; sha e0a68c95bd 2026-08-25 spycat88 | CANNOT (no network) |
<!-- end t28:pins -->

- **`rocknix-abl` carries a fork identity on its checksum.** The fork's `9aa7affee9` (blitterbot, 2026-10-15, #600) mirrors upstream's `15123b2951` (2026-10-01). The recipe is outside the slice, and the next base merge deletes it.
- **`kernel-firmware`'s ROCKNIX override is `20260309` at both hashes**, while the generic `packages/linux-firmware/kernel-firmware` is `20260622`. The override is three months behind its own generic recipe. That is outside the slice; cited.
- **`inputplumber` moves from a prebuilt `v0.79.0` tarball to `0.82.0` built from source.** **`extra-firmware`** moves to `925dfb5efbe5...`.

## § The configuration

T41's row, read here for the shape, as T27 read H700's (r06 to r10):
- **The file:** `projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf`, 8,608 lines. Line 3 is `# Linux/arm64 7.2.0 Kernel Configuration`, against the recipe's `7.2` (`linux/package.mk:29-35`, unchanged at `651150fc88:35`).
- **Against upstream's own copy at `651150fc88`: 7 removed, 7 added**, all upstream's. Every line is attributed:
  - the compiler stamps: `CC_VERSION_TEXT` and `GCC_VERSION` (gcc 16.2.0 upstream, 15.2.0 ours);
  - the Rust toolchain: `RUSTC_VERSION`, `RUSTC_LLVM_VERSION` and `RUSTC_LLVM_MAJOR_VERSION`;
  - `CC_HAS_COUNTED_BY_PTR=y` upstream, against our `# CONFIG_INPUT_POLLDEV is not set`, a compiler-capability line the new toolchain adds;
  - `RAID6_PQ_BENCHMARK`, off upstream (`5f56cd5150`, *skip the RAID6 algorithm benchmark at boot*) and on in ours.
- **History:** 0 fork non-merge commits since the base (r09). Upstream's four since: `dcafa74090` 10-22, `6fbefc45c6` 10-18, `5f56cd5150` 10-04, `c0980b2b71` 10-02, the same four as H700's.
- **Distance from the other Qualcomm configurations** at `8ebaf8daad` (r08, `^<` / `^>` against each): SM8650 41/36, SM8750 81/105, SM6115 228/133, SM4450 229/189, SM8250 371/204. That is a Q5 fact for the coordinator, not a proposal.

## § The loader and the tree

How the Nova gets its loader and its tree at `8ebaf8daad`. Nothing here ran on the unit; the observed boot is device fact L17.

**At build time.**
1. `options:34` sets `BOOTLOADER="qcom-abl"`. `qcom-abl` is a meta recipe (`1.0`, `PKG_URL=""`).
2. `options:28` sets `KERNEL_MAKE_EXTRACMD=" $(get_kernel_make_extracmd)"`. That function (`distributions/ROCKNIX/config/functions:226-231`) turns `config.xml`'s `<SM8550 ... dtb_prefix="qcom">` entries (`config.xml:130-145`) into make targets: `qcom/<file>.dtb` for each of **the fourteen `.dts`, the Nova's included** (r20).
3. The kernel recipe's `qcom-abl` branch (`projects/ROCKNIX/packages/linux/package.mk:387-404`):
   - gzips the Image into `.image/kernel.gz`;
   - then `for dtb in "arch/${TARGET_KERNEL_ARCH}/boot/dts/"**/*.dtb; do ... cat "$dtb" >> "${INSTALL}/.image/kernel.gz"` (`:392-396`), **appending every dtb in the build tree** (the fourteen the make targets built);
   - adds a dummy ramdisk, and runs `python3 "${TOOLCHAIN}/mkbootimg/mkbootimg.py"` into `.image/Image` (r18). `mkbootimg` is the host tool from `tools/mkbootimg`, `:19` for `SM*`.
4. `scripts/mkimage:257-266` is the `qcom-abl` branch. It sources `projects/ROCKNIX/bootloader/mkimage`, whose `mkimage_all` (`distributions/ROCKNIX/config/functions:384-400`) runs only the steps `mkimage_options` lists. For SM8550 that is `abl`, so only `mkimage_abl` runs (`bootloader/mkimage:108-111`, `mcopy "${RELEASE_DIR}/3rdparty/bootloader/rocknix_abl" ::`).
5. **Two SM8550-naming branches never run for SM8550.**
   - `bootloader/mkimage:22-26` copies `rocknix-u-boot.img` (*"SM8750, SM8650 & SM8550"*). No recipe or script produces that file: `git grep rocknix-u-boot` finds only these lines and five trees' inert `rocknix-u-boot-dt-id` properties. Upstream removed the branch, but the properties stay at `651150fc88`.
   - `bootloader/mkimage:81-83` is `mkimage_dtb()`'s `SM8550|SM8650|SM8750|SM8250|SM6115|SM4450)` case, copying `3rdparty/bootloader/boot`. `dtb` is not in SM8550's `mkimage_options`.
6. `projects/ROCKNIX/bootloader/install:50-61` is the designed echo branch: `qcom-abl|arm-efi)` *"is written into the boot partition at image time"* (the futro's `install:51-58`; the brief writes `install:50-60`, which is this file, not `scripts/install`).

**The ELF.**
- `rocknix-abl` (`options:66`) installs `usr/share/bootloader/rocknix_abl/abl_signed-${DEVICE}.elf`.
- On an update, `bootloader/update.sh` (37 lines) handles it:
  - `:17` remounts `/flash` rw (unchecked);
  - `:19-23` copies `rocknix_abl/*` to `/flash/rocknix_abl` (unchecked);
  - **`:25` runs `$SYSTEM_ROOT/usr/bin/updateabl` unconditionally**;
  - `:27-31` removes `/flash/boot` and `/flash/EFI` (*"REMOVE IN THE FUTURE"*);
  - `:37` writes `.boot.hint`;
  - `:10-14` compute `BOOT_DISK` for `mmcblk`, and nothing uses it.
- **`updateabl` is T1's file** (`projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl`), read here only for what `update.sh` hands it:
  - **the guard is inside `updateabl`, not in `update.sh`'s call.** It refuses a device outside `SM4450|SM6115|SM8250|SM8550|SM8650|SM8750` (`:9-16`), a missing ELF (`:24-27`) and missing `abl_a` / `abl_b` partitions (`:31-36`);
  - it reads the ELF from the new system's tree (`:19`, `$SYSTEM_ROOT/usr/share/bootloader/rocknix_abl/abl_signed-${HW_DEVICE}.elf`, `HW_DEVICE` from `$SYSTEM_ROOT/etc/os-release` at `:7`);
  - it compares sha256s and `dd`s the ELF into **both** slots only when either differs (`:60-73`, r21).
- **Observed:** device fact L17 (*SM8550 boot on the Retroid Pocket Nova*, `device-facts.md:17`) records both ABL slots written on the 2026-10-12 update, and L19 (*Nova shutdown and bootloader recovery*, `:19`) is a keep-an-eye-on.
- **The SD copy is a manual-flash input.** `/flash/rocknix_abl` is what `rocknix-abl/sources/README:1-6` tells a person to copy to Android storage and flash with `flash_abl.sh`. `updateabl` never reads it.

**The tree.** The Nova's tree is one of fourteen dtbs appended to one `kernel.gz`. **No tree carries a `rocknix-dt-id`** (r24), and nothing in the directory, `config.xml` or the recipes says how the ABL picks the Nova's dtb from the fourteen. Device fact L17 records only that it boots (F-05).

**Upstream's replacement, 2026-10-01 to 10-24** (r29, 18 commits):
- `0340192729` (10-01) adds ` gpt` to `EXTRA_CMDLINE`.
- `71d8932b33`, `a5d0dd4d57` and `73ffb8ee37` take `openabl` to `1.0`, `1.1` and `1.2` (10-14, 10-19, 10-24).
- **`cafbb1657d` (10-22, *Qualcomm: change from boot.img to Boot Loader Spec for booting*):**
  - `config.xml:134` reads `mkimage_options="abl,bls,dtb"`;
  - the kernel recipe drops `mkbootimg` (the tool's recipe is deleted);
  - `update.sh` copies `dtbs`, `loader` and `openabl` (43 lines after `7842b3b429`'s -6);
  - `updateabl` becomes a chroot hand-off.
- The loader entry is written by `projects/ROCKNIX/packages/virtual/arm-efi/package.mk`'s `post_install` (`:13-23` at `651150fc88`): `cat << EOF > "${BLS_PATH}/${DISTRONAME,,}.conf"` with `title ${DISTRONAME}` and `options boot=LABEL=${DISTRO_BOOTLABEL} ...`. On the fork, `DISTRONAME="pixelelated"` (`distributions/ROCKNIX/options:17`) and `DISTRO_BOOTLABEL="ROCKNIX"` (`:202`). So the entry would be `pixelelated.conf`, titled `pixelelated`, with `boot=LABEL=ROCKNIX`: the identity seam.
- **Every unit of the path above is *settled by the next base merge*.** What that merge must answer (both ABL slots' `Already written:`, the entry's name) is **Backlog #1099**, the coordinator's, cited here, not re-filed.

## § The device trees

16 sources (2 `.dtsi`, 14 `.dts`; 6,267 lines, 138,992 bytes) and the `.disabled` patch's row. The Nova and its include chain are the shipped unit; the other thirteen are AYANEO's and AYN's boards, built into every SM8550 boot image and carried by placement (D-WORKFLOW-185). The `model` lines are the at-hash files'. The Nova's `compatible` is `"retroidpocket,rpnova", "qcom,qcs8550", "qcom,sm8550"` (r23). Its panel, `il97680a,rpnova`, comes from patch 0105 (T41's row).

<!-- begin t28:trees -->
| Source | Lines | Includes (local and mainline) | `model` | `rocknix-dt-id` | Disposition |
| --- | ---: | --- | --- | --- | --- |
| `qcs8550-ayaneo-pocket-common.dtsi` | 1504 | `qcs8550.dtsi`, `pm8550.dtsi`, `pm8550b.dtsi`, `pm8550ve.dtsi`, `pm8550vs.dtsi`, `pmk8550.dtsi` | none (a `.dtsi`); included by `qcs8550-ayaneo-pocketace.dts`, `qcs8550-ayaneo-pocketdmg.dts`, `qcs8550-ayaneo-pocketds.dts`, `qcs8550-ayaneo-pocketevo.dts`, `qcs8550-ayaneo-pockets1k.dts`, `qcs8550-ayaneo-pockets2k.dts`, `qcs8550-ayaneo-pocketsmini.dts` | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayaneo-pocketace.dts` | 146 | `qcs8550-ayaneo-pocket-common.dtsi` | "AYANEO Pocket ACE" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayaneo-pocketdmg.dts` | 139 | `qcs8550-ayaneo-pocket-common.dtsi` | "AYANEO Pocket DMG" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayaneo-pocketds.dts` | 281 | `qcs8550-ayaneo-pocket-common.dtsi` | "AYANEO Pocket DS" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayaneo-pocketevo.dts` | 109 | `qcs8550-ayaneo-pocket-common.dtsi` | "AYANEO Pocket EVO" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayaneo-pockets1k.dts` | 174 | `qcs8550-ayaneo-pocket-common.dtsi` | "AYANEO Pocket S 1K" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayaneo-pockets2k.dts` | 196 | `qcs8550-ayaneo-pocket-common.dtsi` | "AYANEO Pocket S 2K" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayaneo-pocketsmini.dts` | 190 | `qcs8550-ayaneo-pocket-common.dtsi` | "AYANEO Pocket S Mini" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayn-common.dtsi` | 1767 | `qcs8550.dtsi`, `pm8550.dtsi`, `pm8550b.dtsi`, `pm8550ve.dtsi`, `pm8550vs.dtsi`, `pmk8550.dtsi` | none (a `.dtsi`); included by `qcs8550-ayn-odin2.dts`, `qcs8550-ayn-odin2mini.dts`, `qcs8550-ayn-odin2portal.dts`, `qcs8550-ayn-thor.dts`, `qcs8550-retroidpocket-rp6.dts` | none | shipped unit (the Nova uses it) |
| `qcs8550-ayn-odin2.dts` | 363 | `qcs8550-ayn-common.dtsi` | "AYN Odin 2" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayn-odin2mini.dts` | 192 | `qcs8550-ayn-common.dtsi` | "AYN Odin 2 Mini" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayn-odin2portal.dts` | 294 | `qcs8550-ayn-common.dtsi` | "AYN Odin 2 Portal" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-ayn-thor.dts` | 469 | `qcs8550-ayn-common.dtsi` | "AYN Thor" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-retroidpocket-rp6-top-dpad.dts` | 17 | `qcs8550-retroidpocket-rp6.dts` | "Retroid Pocket 6 TOP-DPAD" | none | carried by placement (D-WORKFLOW-185) |
| `qcs8550-retroidpocket-rp6.dts` | 391 | `qcs8550-ayn-common.dtsi` | "Retroid Pocket 6" | none | shipped unit (the Nova uses it) |
| `qcs8550-retroidpocket-rpnova.dts` | 35 | `qcs8550-retroidpocket-rp6.dts` | "Retroid Pocket Nova" | none | shipped unit |
| `0053-add-hynitron-touchscreen.patch.disabled` | 20593 | n/a (a patch) | n/a | n/a | disabled at birth, upstream's, never applied (`scripts/unpack:150-159`) |
<!-- end t28:trees -->

## Findings

### F-01 (Q4; Info; Renovation): the Nova's whole boot path is superseded upstream, settled by the next base merge (#1099)

- **What is superseded:** the `qcom-abl` branch of the kernel recipe; `mkbootimg`, now deleted; `rocknix-abl`, now absent, with `openabl` in its place; `update.sh` and `options` (the 2 M); and `config.xml`'s `mkimage_options`. All change between `0340192729` and `73ffb8ee37`, with `cafbb1657d` the core (§ The loader and the tree).
- **The merge brings all of it unchanged.** The fork has never edited the directory since the base, and has one checksum line in `rocknix-abl`, which the merge deletes.
- **What that merge must answer is #1099:**
  - both ABL slots' `Already written:` (L17 records both written with `rocknix-abl`'s ELF);
  - the loader entry `upstream's virtual/arm-efi` writes as `${DISTRONAME,,}.conf`, which becomes `pixelelated.conf` on the fork, against D-WORKFLOW-123's RC2 identifiers.
- **Disposition:** deferred to #1099. Nothing is changed here.

### F-02 (Q4; Info; Renovation): two pins differ, two are absent upstream, one override lags its generic recipe

- **Differ upstream:** `extra-firmware` (`88b363e67d...` to `925dfb5efb...`) and `inputplumber` (prebuilt `v0.79.0` to source-built `0.82.0`).
- **Absent upstream:** `rocknix-abl` (replaced by `openabl` 1.2) and `mkbootimg` (deleted by `cafbb1657d`).
- **Identical:** `qcom-abl`, the kernel `7.2` and `kernel-firmware` `20260309`. `gamepadcalibration`'s pin is identical, and its file differs only in SM6115's branch.
- **The fork identity on `rocknix-abl`'s checksum** (`9aa7affee9`) mirrors upstream's `15123b2951`.
- **The ROCKNIX `kernel-firmware` override is `20260309`** against the generic recipe's `20260622`: outside the slice, cited for its owner.
- **Disposition:** the merge settles the first four; the authors' releases are `CANNOT (no network)`.

### F-03 (Q3; Info): the SM8550 firmware list is installed as files, never embedded in the kernel, unlike its three Qualcomm siblings; observed working

- **The list.** `config/kernel-firmware.dat` lists six entries: `rtl_nic/rtl8153a-4.fw`, `qca/hmtbtfw20.tlv`, `qca/hmtnv20.*`, `qcom/sm8550/a740_zap.mbn`, `qcom/a740_sqe.fw` and `qcom/gmu_gen70200.bin`.
  - `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk:39-70` reads it with `find_file_path config/kernel-firmware.dat` and copies each entry into the image's firmware directory. It dies on a missing pattern (`:57`).
- **The kernel recipe embeds firmware for SM8250, H700, SM8650 and SM8750 only.**
  - `:83`: `elif [ "${DEVICE}" = "SM8250" -o "${DEVICE}" = "H700" -o "${DEVICE}" = "SM8650" -o "${DEVICE}" = "SM8750" ]; then` `PKG_DEPENDS_UNPACK+=" kernel-firmware"`.
  - `:208-277` holds the `TARGET_ARCH = aarch64 -a DEVICE = SM8250 / SM8650 / SM8750` blocks that fill `CONFIG_EXTRA_FIRMWARE`.
  - **No line names SM8550** except the version case, at both hashes.
- **All four Qualcomm confs build `CONFIG_DRM_MSM=y` with `CONFIG_EXTRA_FIRMWARE=""`.** The three siblings get theirs filled at build time; SM8550's GPU firmware (`a740_*`, `gmu_gen70200`) loads from the root filesystem at runtime.
- **Observed working:** device facts L17 and L18 (*Nova frontend readiness after #529*, `device-facts.md:18`) record an active frontend on the unit.
- **Not a bug: a divergence.** The coordinator may ask whether SM8550 should match its siblings; this slice proposes nothing. #836 (a device-level file that `find_file_path` reads is outside the package stamp) is the stamp issue for this `.dat`: cited, not re-filed.
- **Already written:** nothing, since no fix is proposed.

### F-04 (Q1; Low; Renovation): `update.sh` checks none of its steps, computes a disk it never uses, and keeps a cleanup marked for removal

- **The unchecked steps.** `:17`'s remount, `:22`'s copy and the two `rm -rf` are unchecked, and `:10-14`'s `BOOT_DISK` is unused. This is T27's #1095 shape: an updater that reports nothing when it fails.
- **Why it is not a bug here.** The loader write that matters is `updateabl`'s, which takes its ELF from `$SYSTEM_ROOT` and refuses a missing ELF, a foreign device and missing partitions. A failed copy can leave only a truncated `/flash/rocknix_abl/` on the card, the input to the README's manual flash procedure. `updateabl` and the boot never read it. **Q3: not a bug.** It is a latent hazard for a person following `rocknix-abl/sources/README`.
- **Upstream.** `update.sh` at `651150fc88` (43 lines) keeps the same unchecked shape for its `dtbs`, `loader` and `openabl` copies.
- **Disposition:** settled by the next base merge (#1099) for the path; the unchecked-copy shape is the coordinator's to weigh beside #1095.
- **Already written:** nothing, since no fix is proposed.

### F-05 (Q7; Low; Renovation): a reader cannot tell from the directory how the Nova boots, and no runbook section exists (#1100)

- **Which tree.** The Nova's dtb is one of fourteen appended to one `kernel.gz`. No tree declares a `rocknix-dt-id`, and nothing in the directory, `config.xml` or the recipes says how the ABL picks a dtb.
- **Which ELF and where it comes from.** `rocknix_abl` reaches `/flash` and both ABL slots through three recipes outside the directory and T1's `updateabl`.
- **The written procedure** is `rocknix-abl/sources/README:1-6`, an Android-side manual flash. **No runbook section exists for the SM8550** (Backlog #1100).
- **Upstream's BLS change** (F-01) makes the tree explicit, under `dtbs/`, and the entry readable.
- **Disposition:** deferred to #1100, beside #1099. No question is asked of the unit.

### F-06 (Q2, Q6; Info; Renovation): the `.disabled` patch is 73.4 % of the slice and never applied

- **The file:** `patches/linux/0053-add-hynitron-touchscreen.patch.disabled`, 20,593 lines and 1,402,545 bytes, born at that name (`aa458af6f9`, 2026-06-29).
- **Never applied.** `scripts/unpack:150-159` globs only `*.patch`.
- **Disposition:** disabled at birth, upstream's; still upstream at `651150fc88`. Its removal is #346's class decision. T27's `.disabled` disposition transfers.

### F-07 (Q2, Q6; Info; Renovation): thirteen trees and seven input files are other boards', carried by placement

- **What they are:** the trees for AYANEO's Pocket ACE, DMG, DS, EVO, S 1K, S 2K and S Mini; AYN's Odin 2, Odin 2 Mini, Odin 2 Portal and Thor; the Retroid Pocket 6 TOP-DPAD; and the AYANEO common `.dtsi`. Seven AYANEO and AYN input files sit beside them.
- **Shipped unit, by the brief's correction:** the Nova's chain (`rpnova.dts`, `rp6.dts`, `ayn-common.dtsi`) and the two InputPlumber files that match its model line.
- **Elsewhere:** `HW_CPU="Snapdragon 8 Gen2"` against upstream's `"Snapdragon 8 Gen 2"` (`471a2711ce`) is settled by the merge. `device-builds.md:25`'s Nova row mixes the two builds' CPU and FPU flags (#1094, cited).
- **Disposition:** carried by placement (D-WORKFLOW-185); no removal.

### F-08 (Q1, Q6; Info; Renovation): two SM8550-naming branches of `bootloader/mkimage` never run for SM8550

- **The branches:** `bootloader/mkimage:22-26` (`rocknix-u-boot.img`, which nothing produces) and `:81-83` (`mkimage_dtb`'s SM8550 case; `dtb` is not in SM8550's `mkimage_options`).
- **Their leftover:** five trees still carry an inert `rocknix-u-boot-dt-id` (the four AYANEO Pocket boards and `ayn-common.dtsi`).
- **Upstream:** it drops the first branch and adds `dtb` to the options (`config.xml:134`), so the second branch runs after the merge.
- **Disposition:** settled by the next base merge (#1099).

## Proofs

Every proof is a numbered proof line of `00-running-log.md`. Its cell reads `tree`, `history`, `tool-run`, `fixture` or `design`.

| # | Claim | Evidence | Cell |
| --- | --- | --- | --- |
| P1 | The 29 and their counts | r01, r02, r04 | proved: tool-run |
| P2 | History and the upstream delta: 24 non-merge, fork 0; 2 M over the 29; 4 M 2 A over the directory; 18 commits | r25 to r29 | proved: history |
| P3 | The branch carries the hash's bytes; nothing changed under `packages/`, `projects/` or `tools/` | r03, r31 | proved: tree |
| P4 | The configuration: 7 / 7, each line attributed, fork 0, upstream's four | r06 to r10 | proved: history |
| P5 | The eight pins at both hashes, and their setting commits | r11 to r14; § The pins | proved: history |
| P6 | The build side of the boot path: fourteen dtbs built and appended; `mkimage_abl` only | r16 to r18, r20; `functions:226-231`, `:384-400` | proved: tree |
| P7 | The update side: `update.sh`'s steps, `updateabl`'s guards and ELF source | r15, r21; `updateabl:7-36` | proved: tree |
| P8 | No SM8550 embed; the `.dat` installed as files; the four confs alike | r19; `kernel-firmware/package.mk:39-70`; the four confs' lines | proved: tree |
| P9 | 16 trees, their includes and models; no `rocknix-dt-id` | r22 to r24; § The device trees | proved: tree |
| P10 | Two input files serve the Nova | `02-ayn-controller.yaml:44`, its `capability_map_id` | proved: tree |
| P11 | Two SM8550 branches never run; no `rocknix-u-boot.img` producer | `git grep rocknix-u-boot`; `config.xml:130`; `functions:384-400` | proved: tree |
| P12 | Upstream's replacement and the loader entry's name | r29; `arm-efi/package.mk:13-23` and `update.sh` at `651150fc88`; `distributions/ROCKNIX/options:17,202` | proved: history |
| P13 | The Nova's physical facts | `device-facts.md:17-20,27,28,31` at `2174265e9c` (identical at `8ebaf8daad`), quoted by their Fact cells | proved: design |
| P14 | The tables regenerated | `tools/t28-tables.py`; `check` exits 0 | proved: tool-run |

## Positives

| Check | It would FAIL on ... |
| --- | --- |
| The block (r01) | an inventory change, or a glob that takes T41's rows |
| The branch and removal rule (r03, r31) | an edit to any of the 29, or under `packages/`, `projects/` or `tools/` |
| The configuration diff (r07) | a fork line, or a regenerated configuration |
| The pins (r12) | an upstream bump, or a recipe restored |
| The embed reading (r19) | an SM8550 block in the kernel recipe |
| The dt-id read (r24) | a tree carrying `rocknix-dt-id` |
| The history (r25, r26) | a fork author on the directory |
| The generator | a short table, an empty cell, a run without a FAIL meaning, or the shipped unit's count not 3 trees |

## Coverage

One row per path of the 29, in path order. *Reach* and *Tier* are the inventory's (all `shipped`, all `upstream-carried`).

<!-- begin t28:coverage -->
| Path | Tier | Reach | Lines | Bytes | What it is | At `651150fc88` | Disposition | proved |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| `projects/ROCKNIX/devices/SM8550/bootloader/update.sh` | upstream-carried | shipped | 37 | 1002 | the in-place updater: copies `rocknix_abl` to `/flash` (:19-23), runs `updateabl` (:25), removes `/flash/boot` and `/flash/EFI` (:27-31) | differs (M) | shipped; superseded upstream (#1099) | tree |
| `projects/ROCKNIX/devices/SM8550/config/kernel-firmware.dat` | upstream-carried | shipped | 8 | 133 | six firmware entries installed by `kernel-firmware`'s `makeinstall_target` (its `package.mk:39-70`); no kernel embed for SM8550 | identical | shipped; Q3 reading (F-03) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/lib/udev/hwdb.d/10-ayaneo.hwdb` | upstream-carried | shipped | 3 | 86 | AYANEO's or AYN's input file; no match names the Nova | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/capability_maps/ayaneo_mcu_japanese.yaml` | upstream-carried | shipped | 252 | 5313 | AYANEO's or AYN's input file; no match names the Nova | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/capability_maps/ayaneo_mcu_xbox.yaml` | upstream-carried | shipped | 252 | 5312 | AYANEO's or AYN's input file; no match names the Nova | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/capability_maps/ayaneo_pocketsmini_gpio.yaml` | upstream-carried | shipped | 28 | 694 | AYANEO's or AYN's input file; no match names the Nova | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/capability_maps/ayn_mcu.yaml` | upstream-carried | shipped | 257 | 5344 | InputPlumber: matches the Nova's model line (`02-ayn-controller.yaml:44`) and its map | identical | shipped unit (the Nova uses it) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/devices/01-ayaneo-controller-japanese.yaml` | upstream-carried | shipped | 71 | 2132 | AYANEO's or AYN's input file; no match names the Nova | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/devices/01-ayaneo-controller.yaml` | upstream-carried | shipped | 65 | 1965 | AYANEO's or AYN's input file; no match names the Nova | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/devices/02-ayn-controller.yaml` | upstream-carried | shipped | 89 | 2907 | InputPlumber: matches the Nova's model line (`02-ayn-controller.yaml:44`) and its map | identical | shipped unit (the Nova uses it) | tree |
| `projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/devices/02-ayn-thor-controller.yaml` | upstream-carried | shipped | 50 | 1555 | AYANEO's or AYN's input file; no match names the Nova | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocket-common.dtsi` | upstream-carried | shipped | 1504 | 36508 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketace.dts` | upstream-carried | shipped | 146 | 3058 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketdmg.dts` | upstream-carried | shipped | 139 | 2781 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketds.dts` | upstream-carried | shipped | 281 | 5942 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketevo.dts` | upstream-carried | shipped | 109 | 2094 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pockets1k.dts` | upstream-carried | shipped | 174 | 3723 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pockets2k.dts` | upstream-carried | shipped | 196 | 3814 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketsmini.dts` | upstream-carried | shipped | 190 | 3901 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-common.dtsi` | upstream-carried | shipped | 1767 | 42122 | in the Nova's include chain | identical | shipped unit (the Nova uses it) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-odin2.dts` | upstream-carried | shipped | 363 | 7287 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-odin2mini.dts` | upstream-carried | shipped | 192 | 3938 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-odin2portal.dts` | upstream-carried | shipped | 294 | 5872 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-thor.dts` | upstream-carried | shipped | 469 | 9334 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rp6-top-dpad.dts` | upstream-carried | shipped | 17 | 258 | another board's tree, built into every SM8550 boot image | identical | carried by placement (D-WORKFLOW-185) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rp6.dts` | upstream-carried | shipped | 391 | 7745 | in the Nova's include chain | identical | shipped unit (the Nova uses it) | tree |
| `projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rpnova.dts` | upstream-carried | shipped | 35 | 615 | the Nova's tree: `model = "Retroid Pocket Nova"`; includes `qcs8550-retroidpocket-rp6.dts` | identical | shipped unit | tree |
| `projects/ROCKNIX/devices/SM8550/options` | upstream-carried | shipped | 81 | 2306 | the device's build options (`BOOTLOADER="qcom-abl"` :34, `FIRMWARE="extra-firmware"` :63, `ADDITIONAL_PACKAGES` :66) | differs (M) | shipped; superseded upstream (#1099) | tree |
| `projects/ROCKNIX/devices/SM8550/patches/linux/0053-add-hynitron-touchscreen.patch.disabled` | upstream-carried | shipped | 20593 | 1402545 | disabled at birth (`aa458af6f9`); `scripts/unpack:150-159` globs `*.patch` only | identical | disabled at birth, upstream's; removal is #346's class decision | tree |
<!-- end t28:coverage -->



## The first reader's 03-retrospective.md (whole)

# Retrospective audit — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

Phase 3 over a currency slice. The 29 are upstream's, untouched by the fork since the base, and shipped on the Nova. The question is how current they are, and what meets them at the seams.

## 3.1 Architectural coherence

- **The directory is half the picture.** It holds the Nova's options, its updater, its firmware list and its trees, but none of the recipes that pin what boots it. `qcom-abl`, `rocknix-abl`, `mkbootimg`, the kernel, `extra-firmware`, `kernel-firmware`, `inputplumber` and `gamepadcalibration` all live under `projects/ROCKNIX/packages/`. The boot path runs through the kernel recipe's `qcom-abl` branch, `scripts/mkimage`, `projects/ROCKNIX/bootloader/mkimage`, `distributions/ROCKNIX/config/functions` and T1's `updateabl`. That is why the Q7 answer is *no* (`02` F-05): the directory does not say how its device boots.
- **One boot image carries fourteen boards.** `config.xml`'s list becomes make targets (`functions:226-231`), and the recipe's glob appends every built dtb to one `kernel.gz` (`:392-396`). The Nova is one board among AYANEO's and AYN's, and the selection is the ABL's, declared nowhere in the tree.
- **The guard sits where the write happens.** `update.sh` calls `updateabl` unconditionally. `updateabl` refuses a foreign device, a missing ELF and missing partitions, and writes only on a checksum difference. Read together they are safe for the ELF. The card's `/flash/rocknix_abl/` copy is unchecked, and is read only by a person following the README (`02` F-04).

## 3.2 Project conformance

- **`engineering-practices.md` § Nothing runs on a person's device without their yes.** Nothing ran on the Nova. The seven device-facts rows are quoted by Fact cell and line, never produced (D-QA-015, D-QA-027).
- **`device-builds.md` § After rebasing, item 3: every field as the build reads it.** The kernel version is read from the effective case branch (`:29-35`), not the generic recipe. The dtb set is read from what the make targets build (`functions:226-231`), not from the directory listing.
- **`upgrade-and-install.md`: `Already written:`.** No fix is proposed in this slice, so no trace owes one. The one live question of what is already written, both ABL slots after the BLS change, is #1099's by the coordinator's assignment.
- **`packaging-and-patches.md`.** The `.disabled` patch never matches `scripts/unpack`'s `*.patch` globs (`:150-159`), so it is not a patch to this build. Recorded under #346's class (`02` F-06).

## 3.3 Spec fidelity

The brief's figures were re-derived at stage A. Four deltas are recorded rather than corrected (`02` § Deltas):
- r08's pair order is reversed.
- Two filesystem files serve the Nova: the brief says none.
- The Nova's include chain is part of the shipped unit.
- `gamepadcalibration`'s file differs upstream in SM6115's branch, while its pin is identical.

Two of the brief's citations needed their files named:
- `install:50-60` is `projects/ROCKNIX/bootloader/install:50-61`.
- The kernel's embed blocks are as the brief says: `:83` and `:208-277`.

## 3.4 Platform conformance

As behaviour, this is the Nova's, and observed only through device facts L17 to L20, L27, L28 and L31. As record, the slice's firmware list installs files that the runtime loads, and the unit reaches an active frontend (L17, L18). The firmware path is observed working, though it differs from its siblings (`02` F-03).

## 3.5 Cross-system interaction audit

### Interaction: the next base merge x the boot path (#1099)

- **The shared state:** `/flash` and the two ABL partitions.
  - **Now:** `rocknix_abl` on the card, the ELF written into `abl_a` and `abl_b` by `updateabl`, and fourteen dtbs inside the Android boot image.
  - **After the merge:** `openabl` on the card, a BLS entry under `loader/entries/`, and dtbs under `dtbs/`. `updateabl` becomes a chroot hand-off.
- **The race.** The first boot after an in-place update runs the *new* `update.sh` from `$SYSTEM_ROOT` against the *old* `/flash` layout. Upstream's `update.sh` at `651150fc88` removes nothing (0 `rm` lines; the 37-line version's `:27-31` cleanup is gone), so `/flash/rocknix_abl` stays on the card beside `openabl`.
- **What decides which loader both slots hold** after that first update: whether the new `updateabl` takes openabl's ELF, and the entry's name (`pixelelated.conf` on the fork). These are #1099's questions, cited.

### Interaction: T41's patches and configuration x the trees

- **The shared state:** the Nova's dtb is built from three of the slice's sources and the patches that add its panel (`0105`, `il97680a,rpnova`) and the RP6 pieces.
- **The interaction.** A tree here that references a node a T41 patch adds compiles only with that patch. Upstream's new `0508` and `0509` (frame-length calibration, RP6 and Thor) arrive with the merge, beside the 2 M here. The configuration's 7 / 7 is the same merge.

### Interaction: T29's quirks x the Nova

- **The shared state:** the Nova's LEDs and battery indicator, `quirks/devices/Retroid Pocket Nova/bin/` (#332, device fact L31, an open item to test).
- **The interaction.** The quirks key on the board's `model` string, `"Retroid Pocket Nova"` (`rpnova.dts:11`), through `QUIRK_DEVICE` read from `/sys/firmware/devicetree/base/model` (`sysutils/autostart/profile.d/002-autostart:8`, `rocknix-info:8`). InputPlumber's `02-ayn-controller.yaml:44` keys on the same string. A model rename upstream would silently drop both. The string is unchanged at `651150fc88`.

### Interaction: T1's `updateabl` x `update.sh`

- **The shared state:** `$SYSTEM_ROOT`, `os-release`'s `HW_DEVICE`, and the two partitions.
- **The hand-off holds** (`02` § The loader and the tree): the ELF and the device come from the same new tree, and `updateabl` refuses the three missing cases.
- **One design note for T1, not a defect here:** both slots receive the same ELF in one run (`:72-73`), so a bad ELF reaches both, and the A/B pair gives no fallback. L19 (*Nova shutdown and bootloader recovery*) is the keep-an-eye-on that would show it.

### Interaction: T5's stamp (#836) x `config/kernel-firmware.dat`

- **The shared state:** the `kernel-firmware` package's stamp.
- **The interaction.** `find_file_path` reads this device-level file, which is outside the package's hashed directory. So an edit to SM8550's list does not rebuild `kernel-firmware` on a warm root. #836 owns it; this slice's list has not changed since the base.



## The first reader's 04-analysis.md (whole)

# Analysis — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

## Executive summary

- **What it read.** 29 paths, 28,053 lines and 1,570,286 bytes of `projects/ROCKNIX/devices/SM8550/`, at `8ebaf8daad`, all upstream's and all shipped on the Nova. No fork author has touched the directory since the base.
- **One file is 89 % of the bytes and 73.4 % of the lines:** a patch disabled at birth.
- **The lead answer (Q4): the Nova's whole boot path is superseded upstream.** Upstream replaced it between 2026-10-01 and 10-24, with `cafbb1657d`'s Boot Loader Spec at the core: `rocknix-abl` absent, `mkbootimg` deleted, `openabl` 1.2, dtbs under `dtbs/`, and a loader entry named from `DISTRONAME`. Every unit is *settled by the next base merge*, and what that merge must answer is #1099's.
- **The pins:** two differ (`extra-firmware`, `inputplumber`), two are absent (`rocknix-abl`, `mkbootimg`), and three are identical. The configuration is 7 / 7 against upstream's copy, all toolchain stamps and two flips, with 0 fork lines.
- **Q3 has one reading and no bug.** SM8550's six firmware entries are installed as files, never embedded in the kernel as SM8250, SM8650 and SM8750's are. The unit reaches an active frontend (device facts L17, L18), so this is a divergence, observed working.
- **Q7: the directory does not say how its device boots.** The tree is one of fourteen appended, the selection is undeclared, and no runbook section exists (#1100).
- **Four corrections to the brief:**
  - two InputPlumber files serve the Nova (`02-ayn-controller.yaml:44` matches its model line);
  - the Nova's include chain is part of the shipped unit;
  - r08's pairs are reversed;
  - `gamepadcalibration`'s file differs upstream in SM6115's branch.
- **Eight findings: 2 Low, 6 Info. No `bug`, and nothing proposes a removal.**
- **Nothing ran on the Nova; no guest, no build, no fetch.**

## Acceptance-criteria scorecard

#675's seventeen criteria (= brief § 7), at stage C before the punch-list issue. *Met* names its artifact; *waits* names the stage that ticks it.

| # | Criterion | State |
| --- | --- | --- |
| 1 | `00` and `01` to `05` | met at stage C |
| 2 | the lint `PASS` | pre-issue at stage C; resolution waits for stage H |
| 3 | `review-plan.json` independent, one reviewer; provenance on probe and refutation; the manifest with sha256s and 0 hits | stage C (`second-opinions/`) |
| 4 | every punch item at a Phase 7 outcome; `box-check` 0 fail | waits: stage D onward |
| 5 | `reviewed-at:` and `fixed-at:`; the 29 at `8ebaf8daad`'s bytes; nothing under `packages/`, `projects/` or `tools/` at A to D | the diffs are empty now (r03, r31); the header lines wait for stage H |
| 6 | `01` § Scope | met (`18f6d0b228`) |
| 7 | the coverage table, 29 rows under `## Coverage` | met: the brief's `awk` and `grep` print 29 |
| 8 | § The pins, 8 rows | met (generated) |
| 9 | § The configuration | met |
| 10 | § The loader and the tree, with the lines quoted, the device facts and upstream's commits with #1099 | met |
| 11 | § The device trees, 16 rows plus the `.disabled` row | met (generated) |
| 12 | § The runs, every § 5 command with exit, wall time, figure and *a FAIL would mean* | met (generated, 31 rows) |
| 13 | `00` shows no guest, build, handheld command, M7 read or extra keyed call | met through stage B; stage C adds the two keyed calls only |
| 14 | `04` § Q4, Q3, Q6, Q7 and § Second opinion | Q1 to Q7 met; § Second opinion at stage C |
| 15 | every proof's cell; every punch item's `question:`; every `bug` passes `box-check` | 14 proofs at stage B (15 with the seat's); `05` at stage C; no `bug` |
| 16 | the retro | waits: stage G |
| 17 | the five checkers | waits: stage H |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| The base merge brings BLS onto the Nova without both ABL slots' state and the entry's identity read first | Medium | High | #1099 owns it; the merge notes carry it (F-01) |
| A person flashes a truncated `/flash/rocknix_abl` ELF left by a failed update copy | Low | High | unchecked `update.sh:22`; `updateabl` does not read it; README's manual path only (F-04) |
| A bad ELF reaches both ABL slots at once | Low | High | T1's `updateabl:72-73`; L19 is the keep-an-eye-on; a design note for T1 |
| A model rename silently drops the Nova's quirks and InputPlumber layout | Low | Medium | both key on `"Retroid Pocket Nova"`; unchanged at `651150fc88` (`03` § 3.5) |
| SM8550's GPU firmware is absent from the root filesystem | Low | High | the list dies on a missing pattern at build (`kernel-firmware/package.mk:57`); observed working (F-03) |

## Coverage boundary

- **Read in full:** the 29 paths; `update.sh` line by line; the eight pin recipes at both hashes; the kernel recipe's `qcom-abl` branch and embed condition; `scripts/mkimage`'s branch; `projects/ROCKNIX/bootloader/mkimage`'s SM8550 branches; `bootloader/install`; `config.xml:130-145`; the two `distributions/ROCKNIX/config/functions` routines; `updateabl:1-77` (T1's, for the hand-off); upstream's `update.sh`, `arm-efi` and `config.xml` line; the seven device-facts rows.
- **Not read:**
  - the configuration's 8,608 lines beyond its diff, and the 55 live patches (T41's);
  - the quirks (T29's);
  - `updateabl` as a unit (T1's);
  - the M7 build cache, named and never opened.
- **Not checked:** an author's current release, the dtbs' built sizes and how the ABL selects a dtb, because they need a network, a build or the unit. They are `CANNOT` here.

## Second opinion

*Written at stage C (the seat's probe and refutation).*

## Finding Verification

Each finding re-derived from the tree after it was written (Phase 4.5):

| Finding | Re-derivation | Verdict |
| --- | --- | --- |
| F-01 | r29; `cafbb1657d`'s files at `651150fc88`: `config.xml:134`, `update.sh`, `arm-efi/package.mk:13-23`; `mkbootimg` and `rocknix-abl` absent (r12) | confirmed |
| F-02 | r12, r13, r14; `gamepadcalibration`'s diff (`48b98a02d7`, SM6115's branch); the generic `kernel-firmware` `20260622` | confirmed, with the delta |
| F-03 | r19; `kernel-firmware/package.mk:39-70`; the four confs' `DRM_MSM=y`, `EXTRA_FIRMWARE=""`; SM8550 named only in the version case at both hashes; L17, L18 | confirmed |
| F-04 | `update.sh` whole; `updateabl:7-36`; upstream's `update.sh` (0 `rm`, unchecked copies); README `:1-6` | confirmed |
| F-05 | `functions:226-231`; `:392-396`; r24; `config.xml:130-145`; no SM8550 runbook (#1100) | confirmed |
| F-06 | r05; `scripts/unpack:150-159` | confirmed |
| F-07 | `02-ayn-controller.yaml:44`; `rpnova.dts:8,11`; `rp6.dts`'s include; the 13 trees' models | confirmed, with the correction |
| F-08 | `git grep rocknix-u-boot` (one branch, five inert properties); `config.xml:130`; `functions:384-400`; upstream's `bootloader/mkimage` (0 mentions) and `config.xml:134` | confirmed |

Narrowings made while writing:
- The brief's `install:50-60` was first read as `scripts/install`. It is `projects/ROCKNIX/bootloader/install:50-61`.
- `kernel-firmware`'s die line is `:57` within `:39-70`, not `:58` within `:39-68`. Both corrections were made before commit.

## Renovation face

### Q1 Modernize

- **`update.sh`'s state:**
  - `:10-14` computes `BOOT_DISK` and nothing uses it;
  - `:17`'s remount and `:22`'s copy are unchecked;
  - `:27-31` is a cleanup marked *"REMOVE IN THE FUTURE"*.
- **The guard is `updateabl`'s, not the call's.** `:25` runs it unconditionally, and `updateabl:9-36` refuses a foreign device, a missing ELF and missing partitions; `:60-73` writes only on a difference (F-04).
- **`bootloader/mkimage:22-26`'s `rocknix-u-boot.img` branch** has no producer (F-08).
- **The fourteen-tree boot image** is a selection the trees do not declare (F-05).
- **Each is a design sentence, and the next base merge answers most of them.** Upstream's `update.sh` still leaves its copies unchecked.

### Q2 Standards

- **The `.disabled` patch:** 73.4 % of the slice, never matched by `scripts/unpack`'s globs (F-06).
- **The other boards:** 13 trees and 7 input files are AYANEO's and AYN's, carried by placement (D-WORKFLOW-185). The Nova's chain and its two InputPlumber files are the shipped unit (F-07).
- **Elsewhere:** `HW_CPU="Snapdragon 8 Gen2"` is settled by `471a2711ce`. `device-builds.md:25`'s mixed row is #1094's, cited.
- **No `pkgcheck` row:** the slice has no `package.mk`.

### Q3 Bugs

**None.** The one reading is F-03, quoted from both sides:
- **The list:** `config/kernel-firmware.dat` lists six entries, installed by `kernel-firmware/package.mk:39-70` into the image's firmware directory.
- **The embed:** the kernel recipe embeds firmware only for `"SM8250" -o "H700" -o "SM8650" -o "SM8750"` (`:83`), in the blocks at `:208-277`. No line names SM8550 outside the version case, at either hash.
- **Observed working:** all four confs build `DRM_MSM=y` with an empty `EXTRA_FIRMWARE`, and the unit reaches an active frontend (L17, L18).
- **#836** is the stamp issue for this `.dat`, cited.

`update.sh`'s hand-off makes `updateabl` write nothing it should not: the ELF and the device come from the same new tree, and the missing cases refuse (F-04). **Nothing ran on the Nova.**

### Q4 Package currency

- **The pins** (`02` § The pins, generated):
  - `qcom-abl` `1.0`, identical;
  - `rocknix-abl` `1.2`, **absent upstream** (openabl `1.0` `71d8932b33`, `1.1` `a5d0dd4d57`, `1.2` `73ffb8ee37`); its sha set by the fork's `9aa7affee9`;
  - the kernel `7.2`, the same pin;
  - `mkbootimg` **deleted** (`cafbb1657d`);
  - `extra-firmware` **differs**;
  - `kernel-firmware` `20260309`, identical (and three months behind the generic `20260622`);
  - `inputplumber` **differs** (`v0.79.0` prebuilt to `0.82.0` from source);
  - `gamepadcalibration`: the same pin, the file differing only for SM6115.
  - The authors' releases are `CANNOT (no network)`; `tools/fork-package-freshness` is the RC's check.
- **The configuration:** 7 / 7 against upstream's copy (toolchain stamps, `CC_HAS_COUNTED_BY_PTR` / `INPUT_POLLDEV`, `RAID6_PQ_BENCHMARK`), 0 fork lines, upstream's four commits. T41's row.
- **The trees:** the Nova's chain is unchanged at `651150fc88`. The panel and RP6 patches are T41's.
- **The path as a whole: *settled by the next base merge***, every unit of the `qcom-abl` boot path, with **#1099** cited for what the merge must answer (both ABL slots, `pixelelated.conf`).

### Q5 Efficiency

- **The slice: 1,570,286 bytes.**
  - The `.disabled` patch is 1,402,545 bytes (89.3 %), 20,593 lines.
  - The sixteen trees are 138,992 bytes, 6,267 lines.
  - The nine input files are 25,308 bytes, 1,067 lines.
  - `options`, `update.sh` and the `.dat` make up the rest.
- **The boot image** carries fourteen dtbs. Their built size needs a build (`CANNOT` here). The trees' source bytes, 138,992, are a proxy, not a bound, because a dtb also carries mainline's `qcs8550.dtsi` and the PMIC includes.
- **The configuration's distance** from the other Qualcomm configurations (r08): SM8650 41/36, SM8750 81/105, SM6115 228/133, SM4450 229/189, SM8250 371/204. A fact for the coordinator's parameterisation question, not a proposal.

### Q6 Dead ends

One disposition per unit (the coverage table carries each row's):

| Unit | Paths | Disposition |
| --- | ---: | --- |
| The Nova's tree and include chain (`rpnova.dts`, `rp6.dts`, `ayn-common.dtsi`) | 3 | shipped unit |
| The Nova's InputPlumber files (`02-ayn-controller.yaml`, `ayn_mcu.yaml`) | 2 | shipped unit |
| The other boards' trees | 13 | carried by placement (D-WORKFLOW-185) |
| The other boards' input files | 7 | carried by placement (D-WORKFLOW-185) |
| `options`, `bootloader/update.sh` | 2 | shipped; superseded upstream, *settled by the next base merge* (#1099) |
| `config/kernel-firmware.dat` | 1 | shipped; F-03's reading, no change |
| `patches/linux/0053-...patch.disabled` | 1 | disabled at birth, upstream's; its removal is #346's class decision |
| `bootloader/mkimage:22-26` and `:81-83` (outside the slice, read) | — | never run for SM8550; settled by the next base merge |

**Removals: none.**

### Q7 Clarity and structure

**No: a reader cannot tell from the directory how the Nova boots** (F-05).
- **Which ELF, and from where:** `rocknix_abl` reaches `/flash` and both ABL slots through `rocknix-abl`'s recipe, `update.sh` and T1's `updateabl`, outside the directory.
- **Which tree:** one of fourteen appended to one `kernel.gz` by the kernel recipe. No tree declares a dt-id, and the ABL's selection is written nowhere.
- **Where it is written down:** only `rocknix-abl/sources/README:1-6`, an Android-side manual flash. **#1100** owns the missing runbook section.
- Upstream's BLS change makes the tree explicit (`dtbs/`) and the entry readable, after the merge.
- **The `vm-first` answer for every device fact:** the seven rows named, nothing new asked of the unit.

## Instruction File Recommendations

### Coverage gaps (would have prevented)

- **None for a defect.**

### Codification gaps (proposals for the coordinator)

1. **Device briefs:** a file's ownership by device is read from its match rules, not its name. `02-ayn-controller.yaml` is the Nova's by its `model` match, though its name says AYN.
2. **Briefs that cite a short path name the file.** `install:50-60` meant `projects/ROCKNIX/bootloader/install`, while `scripts/install` exists too.

## Quality self-check

- **Blindspot 13 (assumed done):** each scorecard row names its artifact; nothing is ticked on a file's existence.
- **Blindspot 22 (a probe that cannot report absence):** each § The runs row says what a FAIL would mean, and the dt-id read's `|| true` keeps a 0 from reading as a failure.
- **Blindspot 31 (a harness that writes and reads through the same wrong path):** the update hand-off was read from both sides, `update.sh` and `updateabl`, not from either's comment.
- **Blindspot 46 (a name read as a behaviour):** F-07's correction is this blindspot caught. `02-ayn-controller.yaml` is the Nova's by its match rule, though its name says AYN.
- **Blindspot 51 (a checklist from open boxes):** the scorecard is #675's seventeen, read at dispatch.
- **Blindspot 75 (a corpus read on the wrong tree):** every figure is a command at `8ebaf8daad`. The device-facts rows were checked identical at `2174265e9c` and `8ebaf8daad`. Two citations were corrected after reading the file they named.
- **Rules read this session:** `engineering-practices.md`, `device-builds.md`, `packaging-and-patches.md`, `upgrade-and-install.md`, `release-candidates.md`, `bugs-are-agent-first.md`, `issue-tracking.md`, `vm-first.md`, `adversarial-council.md`, `decision-register.md`. Decisions: D-WORKFLOW-185, -195, -209, -123, D-QA-015, D-QA-027.



## Context 1: docs/reviews/order.md § T28

```text
### T28. devices: the SM8550 device (Retroid Pocket Nova)

- **id**: `device-sm8550`; **kind**: currency; **lens**: cost against value
- **why here**: a shipped test device
- **paths** (29 paths, 28,053 lines, 118 read, of which 0 fork-own; 0 patch and config lines; reach shipped 29): areas `devices`; globs `projects/ROCKNIX/devices/SM8550/**`
- **read before**: none
- **depth**: Independent -- an ordinary device slice
- **interacting subsystems** (read-only context): its quirks and kernel patches; the kernel recipe and project boot files (`device-generic-x64-and-kernel`)
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

```


## Context 2: the brief's § 2 and § 4

```text
## 2. Scope

**The membership block** (T25's shape; the slice's one rule is a glob and
the area):

```bash
python3 -I - <<'PY'
import json, collections, os
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
t28 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "devices"
       and r["path"].startswith("projects/ROCKNIX/devices/SM8550/")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t28), "lines", L(t28), dict(collections.Counter(r["reach"] for r in t28)), dict(collections.Counter(r["tier"] for r in t28)))
print(dict(collections.Counter(r["language"] for r in t28)))
CODE = {"shell", "recipe", "udev", "python", "c", "make"}
rd = [r for r in t28 if r["language"] in CODE and r["tier"] != "vendor-carried" and r["reach"] != "unreached"]
print("read", len(rd), L(rd), "fork-own", sum(1 for r in rd if r["tier"] == "fork-own"))
alld = [r for r in rows if r["tree"] == "distribution" and r["path"].startswith("projects/ROCKNIX/devices/SM8550/")]
print("whole directory in the inventory", len(alld), L(alld), dict(collections.Counter(r["area"] for r in alld)))
os.makedirs(".qa-scratch/t28", exist_ok=True)
open(".qa-scratch/t28/paths.txt", "w").write("".join(r["path"] + "\n" for r in sorted(t28, key=*** r: r["path"])))
for r in sorted(t28, key=*** r: r["path"]): print(r["reach"], r["tier"], r["lines"], r["path"])
PY
wc -l .qa-scratch/t28/paths.txt     # 29
```

Recorded (2026-10-25, at `2174265e9c`; the inventory there was generated at
`eb4763e3cc`): **29 paths, 28,053 lines; reach shipped 29; upstream-carried
29, fork-own 0; read 2 files / 118 lines / 0 fork-own** (`options` 81 and
`bootloader/update.sh` 37; the language rule reads no DTS); languages shell
2, other 3, yaml 8, devicetree 16. The whole directory holds 85 inventory
rows / 57,561 lines: the other 56 are `patches-and-configs` rows (the
8,608-line `linux/linux.aarch64.conf` and the 55 live patches, 20,899
lines), T41's -- which is why the order says *"0 patch and config lines"*
and this slice, unlike T27's, does **not** take the configuration into its
membership (the configuration shape is still read, one line and one diff,
under Q4, cited as T41's row).

**The 29, by weight.** `options` 81; `bootloader/update.sh` 37;
`config/kernel-firmware.dat` 8 (6 entries); `filesystem/` 9 files / 1,067
(`10-ayaneo.hwdb` 3; four inputplumber `capability_maps/*.yaml` 252 / 252 /
28 / 257; four `devices/*.yaml` 71 / 65 / 89 / 50 -- every one AYANEO's or
AYN's, none the Nova's); `linux/dts/qcom/` 16 files / 6,267 (two `.dtsi`:
`qcs8550-ayaneo-pocket-common.dtsi` 1,504 and `qcs8550-ayn-common.dtsi`
1,767; fourteen `.dts`, among them `qcs8550-retroidpocket-rpnova.dts` 35,
`qcs8550-retroidpocket-rp6.dts` 391 and `-rp6-top-dpad.dts` 17); and
**`patches/linux/0053-add-hynitron-touchscreen.patch.disabled`, 20,593
lines = 73.4 % of the slice**, born at that name (`aa458af6f9`,
2026-06-29, *"linux: bump SM8550 to 7.1.2"*), still upstream, never read by
`scripts/unpack` -- T27's `.disabled` disposition transfers. No
`package.mk`, no udev rule, no device `bootloader/mkimage` under the
directory: **every pin this slice reads lives in a recipe outside it**,
cited by path.

**The pins (8 rows, T27's shape; both hashes read locally):**

| Unit | Recipe (outside the slice) | At `8ebaf8daad` | At `651150fc88` | Set by |
| --- | --- | --- | --- | --- |
| `qcom-abl` (`options:34 BOOTLOADER="qcom-abl"`) | `projects/ROCKNIX/packages/tools/qcom-abl/package.mk` (11 lines, a meta recipe) | `PKG_VERSION="1.0"`, `PKG_URL=""`, no sha | identical | `7a656ea09d` 2026-01-29 |
| `rocknix-abl` (`options:66 ADDITIONAL_PACKAGES`) | `projects/ROCKNIX/packages/tools/rocknix-abl/package.mk` (18 lines) | `1.2`, sha `64034fb076ea...4cff7`, `github.com/ROCKNIX/abl/releases/download/v1.2/`; installs `usr/share/bootloader/rocknix_abl/abl_signed-${DEVICE}.elf` | **absent** -- replaced by `openabl` (`1.0` at `71d8932b33` 2026-10-14, `1.1` at `a5d0dd4d57`, `1.2` at `73ffb8ee37` 2026-10-24) | the version by `b354bfe6d6` 2026-09-30; **the sha by the fork's `9aa7affee9`** (blitterbot, 2026-10-15, #600, mirroring upstream's `15123b2951`) -- a fork identity on one pin recipe, outside the slice |
| the kernel | `projects/ROCKNIX/packages/linux/package.mk:29-35` (`H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)`) | `7.2`, sha `f9fef3d14c0d...402b3` | identical | the case line's commit |
| `mkbootimg` (the fork's host tool, `package.mk:19` for `SM*`) | `projects/ROCKNIX/packages/tools/mkbootimg/package.mk` | `d2bb0af5ba6d3198a3e99529c97eda1be0b5a093`, sha `418bb875...` | **deleted** (`cafbb1657d`) | `7a656ea09d` (the sha by `e0a68c95bd`) |
| `extra-firmware` (`options:63 FIRMWARE`) | `projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk` (`:20 "SM8550") cp -a SM8550/*`) | `88b363e67d4f730feb2c3124724d26dfaa88ce76` | `925dfb5efbe5d6c3ca654f81e3e1f367f8492777` (**differs**) | `675c364c6d` 2026-09-13 |
| `kernel-firmware` (the ROCKNIX override) | `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk` | `20260309` | identical (the generic `packages/linux-firmware/kernel-firmware` is `20260622` at both: the override is three months behind -- cite, outside the slice) | (the lane reads) |
| `inputplumber` (`options:66`) | `projects/ROCKNIX/packages/tools/inputplumber/package.mk` | `v0.79.0`, a prebuilt tarball | `0.82.0`, built from source (**differs**) | (the lane reads) |
| `gamepadcalibration` (`options:66`) | `projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk` | `2077e7af7e...` | identical | (the lane reads) |

`CANNOT (no network)` for every author's current release: that check is
`tools/fork-package-freshness`'s at the RC (D-WORKFLOW-024) and is named,
not run.

**The configuration** (T41's row, read here as T27 read H700's): 8,608
lines, line 3 `# Linux/arm64 7.2.0 Kernel Configuration` against the
recipe's `7.2`; against upstream's copy at `651150fc88` **7 removed / 7
added** (compiler stamps gcc 16.2.0 against 15.2.0, RUSTC and LLVM
versions, `CC_HAS_COUNTED_BY_PTR=y` against `# INPUT_POLLDEV is not set`,
`RAID6_PQ_BENCHMARK`); **fork non-merge commits since the base: 0**;
upstream's four since (`dcafa74090` 10-22, `6fbefc45c6` 10-18,
`5f56cd5150` 10-04, `c0980b2b71` 10-02 -- the same four as H700's); added
whole by `9f1fab30f6` (2025-07-13, +8,154); tier `vendor-carried`, no
*fork-written* note. Its distance from the other Qualcomm configurations at `8ebaf8daad` (`diff <(git show 8ebaf8daad:<this conf>) <(git show 8ebaf8daad:<other conf>) | grep -c '^<'` and `'^>'`: removed / added): SM8650 36 / 41, SM8750 105 / 81, SM6115 133 / 228, SM4450 189 / 229, SM8250 204 / 371 -- a Q5 fact, not a proposal. (The T41 rows' lines sum to 29,508 in the inventory against 29,507 by `wc -l`: one patch without a trailing newline.)

**The loader and the tree (the boot path at `8ebaf8daad`).** The kernel recipe's `qcom-abl` branch (`projects/ROCKNIX/packages/linux/package.mk:387-404`, the body `:389-403`) gzips the Image, **appends every built dtb into `kernel.gz`** (`:392-396`),
adds a dummy ramdisk and runs `mkbootimg.py` with the LABEL command line
into `.image/Image`; `scripts/mkimage:257-266` is the `qcom-abl` branch (T27's erratum: `:21-23` computes `DISK_SIZE`), sourcing
`projects/ROCKNIX/bootloader/mkimage`, whose `mkimage_all`
(`distributions/ROCKNIX/config/functions:384-400`) runs the `config.xml`
steps -- for SM8550 **only `mkimage_abl`** (`bootloader/mkimage:108-111`,
which mcopies `rocknix_abl`); the `mkimage_uboot` branch naming *"SM8750, SM8650 & SM8550"* (`bootloader/mkimage:22-26`, `rocknix-u-boot.img`) has no producer and is gone upstream; `mkimage_dtb()`'s `SM8550|...)` case (`bootloader/mkimage:81-83`, copying `3rdparty/bootloader/boot`) is a second SM8550-naming branch for Q1 and Q6 to read. `config.xml:130-145` (`<SM8550
mkimage_options="abl" dtb_prefix="qcom">`) lists **14 `<file>` entries =
all fourteen `.dts`, the Nova's included**; no tree carries a
`rocknix-dt-id`, and how the ABL selects the Nova's tree from the fourteen
appended is a Q7 design question (device fact L17: it boots). `install:50-60`
is the designed echo branch (T11's F-09; the futro at :208-213). On an
update, `bootloader/update.sh` (37 lines, last changed `18d890d349`
2026-06-06): `:12` computes `BOOT_DISK` for `mmcblk` and never uses it;
`:19-23` copies `rocknix_abl/*` to `/flash/rocknix_abl`; **`:25` runs
`updateabl` unconditionally** -- `rocknix/sources/scripts/updateabl` (77
lines, T1's) finds `abl_a` and `abl_b` by PARTLABEL, compares sha256 and
`dd`s the ELF into both slots when either differs (`:64-73`; device fact
L17 recorded both slots written on 2026-10-12); `:27-31` removes
`/flash/boot` and `/flash/EFI` (*"REMOVE IN THE FUTURE"*); `:37` writes
`.boot.hint`. **Upstream replaced this path between 2026-10-01 and 2026-10-24** (18 commits on the directory, `scripts/mkimage`, `rocknix-abl` and `openabl` in `8ebaf8daad..651150fc88`: `0340192729` 10-01 adds ` gpt` to the command line; `71d8932b33` 10-14 openabl `1.0`; `cafbb1657d` 10-22 Boot Loader Spec entries, `BOOTLOADER="arm-efi"`, `mkimage_options="abl,bls,dtb"`, dtbs under `usr/share/bootloader/dtbs`, the kernel recipe without mkbootimg, `update.sh` +12; `7842b3b429` `update.sh` -6, to 43 lines; `471a2711ce`; `73ffb8ee37` 10-24 openabl `1.2`; `scripts/mkimage` at `651150fc88` still carries one `qcom-abl` mention): every unit of the path above is *settled by the next base merge*, and that merge's `Already written:` and identity seam (the loader entry upstream's `virtual/arm-efi` recipe writes -- `packages/virtual/arm-efi/package.mk` at `651150fc88`, its post_install read and the entry's name quoted by the lane; it is in no file under `scripts/`, `projects/ROCKNIX/bootloader/` or the kernel recipe) are **Backlog #1099**, the coordinator's -- cited, not re-filed.

**The device trees (16).** The Nova: `model = "Retroid Pocket Nova"`,
`compatible = "retroidpocket,rpnova", "qcom,qcs8550", "qcom,sm8550"`,
`#include "qcs8550-retroidpocket-rp6.dts"` (which includes
`qcs8550-ayn-common.dtsi`, then mainline's `qcs8550.dtsi` and `pm8550*.dtsi`);
its panel `il97680a,rpnova` comes from patch 0105 (T41's); touchscreen
1280x960 (D-WORKFLOW-114); added `3c3ac4f4ee` 2026-07-26. The other
thirteen `.dts` and both `.dtsi` are AYANEO's and AYN's boards: *carried
by placement* (D-WORKFLOW-185), built into every SM8550 boot image.

**History and delta.** Over the 29, `git log --no-merges --format='%h %an'
--since='2026-06-01T00:00:00Z' 8ebaf8daad -- $(cat paths)`: **24
non-merge commits (27 with merges), fork 0, upstream 24**; over the whole
directory 54 / 63, fork 0 (a bare `--since=2026-06-01` printed 52: T27's
erratum, reproduced). `git log --no-merges 651150fc88..8ebaf8daad -- projects/ROCKNIX/devices/SM8550` is **empty** (without `--no-merges` it lists the fork's two upstream merges, `7bd7f31312` and `7650de7dd6`): no fork author has touched the directory since the base. The upstream delta over the 29: **2 M** (`update.sh` and `options`,
+20 / -14); over the directory 4 M + 2 A (the conf, patch 0104, and two
new panel-calibration patches 0508/0509, +451 / -22). `Makefile:39,42,98-101` (in `world`, `arm` then `aarch64`); `config/options:31` defaults `DEVICE="SM8550"` (`:28-30` are a blank, a comment and the `if`). **The fork's only SM8550 code is outside the slice**:
`quirks/devices/Retroid Pocket Nova/bin/{analog_sticks_ledcontrol,battery_led_status,ledcontrol}`
(45 / 135 / 83 lines, #332's), T29's rows.

**Device facts** (`docs/releases/device-facts.md` at `2174265e9c`, cited by the Fact cell and the line at that hash, never re-asked; D-QA-015; the table has no ID column, so a row is named by its Fact cell): line 17 (the Nova's boot after the 2026-10-12 update, both ABL slots written), 18 (frontend readiness after #529), 19 (shutdown and bootloader recovery, #558, keep an eye on), 20 (Tailscale after restart), 27 (the Nova), 28 (the sign-in window's pad, #331: InputPlumber hides the AYN Odin2 Gamepad node), 31 (the stick LEDs, #332, an open item to test). The lane quotes each Fact cell beside the line. No
runbook section exists for the SM8550 (**Backlog #1100**); the only
written flash procedure is `rocknix-abl/sources/README:1-6`.

**What is not here, and where it is:** the configuration and the 55 live
patches (T41, #688); the quirks (T29, #676: `platforms/SM8550/` 24 files,
`devices/Retroid Pocket Nova/` 4 files); `updateabl` (T1, #648); the pin
recipes (`tools/qcom-abl`, `tools/rocknix-abl`, `tools/mkbootimg`, the
kernel, `extra-firmware`, `kernel-firmware`, `inputplumber`,
`gamepadcalibration`: T11's, T8's and T23's rows, cited by path); the M7
lane's build cache `m7-signin-sm8550-build-20261025-01` (named, **never
read**: a pin is read from the tree, D-INFRA-025).


## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`design`); the lens is currency, so Q4 leads:

- **Q4 Package currency -- the lead question.** The eight pins of § 2: the
  pin at `8ebaf8daad`, at `651150fc88` (three differ, one is absent, one is
  deleted upstream), the setting commit, and `CANNOT (no network)` for the
  author's release. The configuration's currency: its 7 / 7 against
  upstream's copy, each line attributed (compiler stamps, two option
  flips), 0 fork lines. The DTS currency: the Nova's include chain against
  the 7.2 tree (the patches that add the boards are T41's, named). **And
  the path's currency as a whole:** every unit of the `qcom-abl` boot path
  is superseded by upstream's 2026-10-22 change; the disposition is
  *settled by the next base merge* with #1099 cited for what that merge
  must answer (both ABL slots, the loader entry's name).
- **Q1 Modernize.** `update.sh:12`'s `BOOT_DISK` computed and never used;
  `:25`'s unconditional `updateabl` run (the write is conditional inside
  `updateabl:64-73`: read both and say which is the guard); the dead
  `rocknix-u-boot.img` branch in `bootloader/mkimage:22-26`; the fourteen
  trees appended into one boot image (a byte cost and a selection the
  trees do not declare) -- each a design sentence for the coordinator, no
  edit; the next base merge answers most of them.
- **Q2 Standards.** The `.disabled` patch (73.4 % of the slice, never read
  by the build); the fourteen AYANEO/AYN trees and the nine AYANEO/AYN
  filesystem files under a directory whose shipped unit is the Nova (a
  placement reading, D-WORKFLOW-185, not a removal); the Nova's row in
  `device-builds.md:25` mixing the two builds' CPUs and the arm FPU (#1094,
  cited, not re-filed); `HW_CPU="Snapdragon 8 Gen2"` against upstream's
  *"Snapdragon 8 Gen 2"* (`471a2711ce`, settled by the merge).
- **Q3 Bugs.** `updateabl`'s compare-and-write of both slots is T1's file:
  read here only for what `update.sh` hands it; a `bug` with its trace
  only if `update.sh` makes it write a loader it should not (a missing
  ELF, a wrong `${DEVICE}`), and its `Already written:` names L17's two
  slots. The `kernel-firmware.dat` list (6 entries: `rtl_nic/rtl8153a-4.fw`,
  `qca/hmtbtfw20.tlv`, `qca/hmtnv20.*`, `qcom/sm8550/a740_zap.mbn`,
  `qcom/a740_sqe.fw`, `qcom/gmu_gen70200.bin`) against the kernel recipe's embed blocks (`:83` the condition naming SM8250, H700, SM8650 and SM8750; `:208-277` the blocks), which name **no SM8550**: a finding with both quoted; cite
  #836 for the stamp; nothing re-filed there. **Nothing runs on the Nova**
  (D-QA-015, D-QA-027).
- **Q5 Efficiency.** The slice's bytes and lines by unit (the one patch
  73.4 %; the sixteen trees 6,267; the nine AYANEO/AYN files 1,067); the
  boot image's size cost of fourteen appended dtbs (`git ls-tree -r -l`
  over the trees as the upper bound; no build); the configuration's
  distance from the other Qualcomm configurations (§ 2's table), a fact
  for the coordinator's parameterisation question, not a proposal.
- **Q6 Dead ends.** The `.disabled` patch (*disabled at birth, upstream's;
  its removal is #346's class decision*); the thirteen other boards' trees
  and the AYANEO/AYN filesystem files (*carried by placement*); the dead
  `rocknix-u-boot.img` branch, `update.sh:12` and `:27-31` (*settled by the
  next base merge*, #1099). Removals none.
- **Q7 Clarity and structure.** Can a reader tell from the directory how
  the Nova boots -- which ELF, which tree of the fourteen, where
  `/flash/rocknix_abl` comes from -- without reading three recipes outside
  it? Is there a written flash and update procedure (#1100: no)? The
  `vm-first` answer for every device fact: the seven rows named, nothing
  new asked of the unit.

A finding is one question with its evidence; `Renovation` is the category
for everything here that is not a defect. The seat (Phase 4.6) grades the
findings and the dispositions; its probe comes first.

```


## Context 3: the register rows

```text
| D-QA-015 | 2026-09-11 | **Every action that uses a handheld or the owner's cloud -- a game launch, pad input, a screenshot, a write under `/storage/roms`, a sync, an upload, a deletion in the cloud -- is asked for by name before it runs, with what it does on screen, what it writes, what it sends and what it leaves behind; a general offer of device testing is not a standing yes.** Extends D-QA-008/011 (reboot, staging) after the session ran the exit test and a Dropbox replacement proof on the RG35XX SP unannounced and the owner met the uploaded files in Dropbox first. Reads need no question. | maintainer, #130 |

| D-QA-023 | 2026-09-13 | **After the milestone audit's punch list closes (D-WORKFLOW-015), H700 builds first; SM8550 -- the Retroid Pocket Nova -- builds next, sequentially, from the same `next`, and is staged on the Nova only after the H700 round has been tested on the RG SP and the RG35XX SP.** Maintainer: "Once all the punch-list items are complete, we can go ahead and create the H700 build. If we want to create the build for the Pocket Nova, we can, or we can wait to test it first on the H700 before proceeding. It looks like the Pocket Nova uses an SM8550." Upstream release 20260901 lists the Pocket Nova under SM8550. Taken under the discretion offered: a build costs CPU hours and runs while H700 is tested; the staging waits so the first unit to meet a fresh build is one whose family has already been flashed. Every staging and reboot stays a per-device question (D-QA-015). | #150; `device-builds.md`; D-QA-015; D-WORKFLOW-015 |

| D-QA-027 | 2026-09-17 | **The RG35XX SP is the dedicated QA handheld from here on: it holds no personal saves or ROMs, signs in only to QA accounts, and may be left plugged in as a bench device, headless if that can be arranged; the RG SP stays the maintainer's own device under D-QA-015.** Settles D-QA-016 (#131). Maintainer: *"With 131, we'll make the RG35XX SP a dedicated QA handheld going forward, and I can plug that in. I can even look at how we might be able to leave it plugged in to make it a headless device, or at least something that's always running as a bench device."* Consequences: the deliberate-crash proof for ramoops (#104's last box) and any per-device proof that needs a real panel, a real Wi-Fi driver or a real provider runs there first; the QA cloud accounts (#131 box 2, #133) are created for it; the runner gains a device target beside the pair. It is flashed from the fork's images and seeded like `seed-device`, never restored from the maintainer's backups. | #131; #104; #133 |

| D-WORKFLOW-114 | 2026-10-01 | **0.0.1's support matrix is the Retroid Pocket Nova (SM8550) and the two H700 boards (the RG35XX SP, the migration device, and the RG SP), with the GENERIC_X64 guest for QA; the RG353M (RK3566) waits -- not built for 0.0.1, its row kept in the matrix as deferred -- and the next board after these is a 16:9 device the maintainer has yet to buy.** Refines D-WORKFLOW-092 (which named SM8550, H700 and RK3566). Read from the device tonight: the Nova's panel is 1280x960, so the matrix holds two panel sizes, 640x480 and 1280x960, both 4:3; the 16:9 board would be the first other shape. Maintainer, 2026-10-01: *"I think we can wait on the RG353M for now. That device isn't getting much use from me, and I'll probably be using the Retroid Pocket Nova more. I think focusing on that device and the H700 devices is a good place to start. Following that, we can look to expand [...] I'm more interested in moving on to a 16:9 device following that, which I'd have to get."* | #344 (owner question 5, P4's asset set), `docs/rasteratops/support-matrix.md`; refines D-WORKFLOW-092, D-WORKFLOW-100 |

| D-WORKFLOW-123 | 2026-10-01 | **Identity default for 0.0.1: every persisted path, partition label, hostname, share name, mount point, unit name and machine-readable identifier keeps its RC2 value, and only consumers the P0 sweep classified as display text change; `DISTRO=ROCKNIX` and `distributions/ROCKNIX/` are retained; relabelling belongs to a later clean-install-only release whose init accepts both labels. Two exceptions, each its own row: the cloud folder (D-CLOUD-158/159) and the chassis declaration (D-NET-016, a file added, no identifier changed).** #344's drafted row 12, approved as a batch. Maintainer, 2026-10-01: *"I think your plan for the 14 rows is good to start. We can always revise that as we go on, as long as we keep track."* | #344 row 12; `docs/rasteratops/p0-sweep.md` |

| D-WORKFLOW-150 | 2026-10-07 | **Build and verify H700 first, then SM8550, from the qualified pixelelated product inputs.** Maintainer explicitly authorizes both builds and names SM8550 as the next target after H700. Run H700 arm compatibility prerequisites, reassess capacity for aarch64 firmware, verify the H700 artifacts, then reassess capacity and build SM8550. Use frozen build worktrees and the standard actively supervised watcher. Compilation of the second target does not await physical testing of the first; D-WORKFLOW-100/120's artifact attachment, physical-action and publication gates remain. No additional cleanup, hardware purchase or RAID conversion is inferred. | #492; #491; #493; milestone7 ordered body |

| D-WORKFLOW-185 | 2026-10-23 | **The renovation order's shipped-device set is H700 and SM8550. GENERIC_X64 is the test image: built, read as the VM every proof runs on (T19), never shipped. Every other target the fork can build (RK3566, RK3326, RK3399, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750, AMD64) is a row in the unshipped tables, not a device slice; `device-builds.md` § Our devices is a hardware inventory, not the shipping list. RK3566 and RK3326 are the recorded first widening: on rocknix.org's device pages they are the two widest targets after the shipped pair (15 and 13 models against H700's 11 and SM8550's 10; SM8250 3, S922X 2, the other six 1 each, RK3576 none), the maintainer owns their test units (RG353M, RG351M), and upstream's release 20261001 publishes two image variants for each (RK3326 a and b, RK3566 Generic and Specific) as it does for H700 (DDR3 and DDR4). Opening either is a device build with its own issue (D-WORKFLOW-132), and the tables re-derive then.** Put by the coordinator lane (D-WORKFLOW-183) as P1's first pass-7 question, from the three-seat review's finding 12 (`device-builds.md`'s five against plan § 5's eight). Maintainer, 2026-10-22: *"Now we're focused on shipping the H700-based builds and the SM8550-based builds. We have not focused on any of the Rockchip builds or the RG353M or RG351M. The fork uses our VM image only for testing."* Then, the same exchange: *"You could check the ROCKNIX GitHub page for the devices they support and see what additional types might give us the most coverage in terms of chips being used by multiple devices."* The read (upstream's README names no device; rocknix.org's 53 device pages, each naming its image target; the 20261001 release's asset list) was put back as the table above with two options, and the maintainer, 2026-10-23: *"I think we should start with what we've done here with H700 and SM8550."* Consequence for the order (#641): T22 `device-rockchip-shipped` dissolves into T17's rows, its kernel patches and configurations move from T42 to T44 and the other patches only those two apply from T43 to T44, `reach` for RK3566 and RK3326 becomes `unshipped`, T23's run-time model derivation uses the shipped pair and the VM; plan § 5's Devices row is corrected in the same change. | #346; #641; D-WORKFLOW-184; D-WORKFLOW-132; D-WORKFLOW-183; `docs/reviews/plan-for-the-plan.md` § 5; `.claude/rules/device-builds.md` § Our devices; https://rocknix.org/devices/; https://github.com/ROCKNIX/distribution/releases/tag/20261001 |

| D-WORKFLOW-187 | 2026-10-23 | **The renovation gates no release. M6 is an audit, assessment and renovation of the codebase: it decides what is read, in what order and at what depth, never what ships or when. D-WORKFLOW-102's release clause is retired (`0.1` waiting on Tier 1's findings on the launch, control and state slice and on any known security, state-preservation or launch-path finding from any tier); its placed, progressive review stands. A finding that is a defect is filed as a bug the session it is found (D-WORKFLOW-132) and holds or clears a release the way every bug does (D-QA-051, `tools/rc-preflight`), owned by the release's milestone, never by a slice. The order carries no release-gate column; T1 and T2 keep their place on the order's own lenses, and the one prerequisite that stands is a reading order, not a gate: the launch-path slices are read before #336 Step 1 replaces what they read. The drift re-review runs at the renovation's own cadence (every slice close), not as a release step. D-WORKFLOW-186's "within D-WORKFLOW-102's gates" reads accordingly. P1's pass-7 question 2 (whether `backuptool`, T17, and the system services, T22, also gate `0.1`) is withdrawn as outside the program, not answered.** Maintainer, 2026-10-23, when the coordinator put question 2: *"Our codebase check shouldn't have anything to do with what we're actually shipping. This is meant to be an audit, assessment, and renovation, and not concerned with features proactively shipping. Now, why would your question 2 be part of what we're trying to accomplish here?"* Sweep in the same change: plan § 5 and § 6a, § 8's drift trigger, the M6 body's acceptance and dependencies, #339's gate checkbox; `order.md` § 1, the Gate column and T1's release-gate line are P1's (#641). | #346; #641; #339; D-WORKFLOW-102; D-WORKFLOW-186; D-WORKFLOW-132; D-QA-051; `docs/reviews/plan-for-the-plan.md` § 5, § 6a, § 8 |

| D-WORKFLOW-195 | 2026-10-24 | **An Extended seat whose answer the model's output ceiling cuts on the packet is run again on a trimmed packet for that seat -- the same model, effort and provider; the analyses and tables whole, the cited files as line-numbered excerpts with context, the ask bounded -- never a model or effort substitution and never the same packet again.** `04` § Second opinion says the seats saw different evidence; an item one seat saw only in excerpt carries `excerpt`, and a disagreement that could be the excerpt's doing is resolved from the artifact, not from either seat. A fork resolved during execution on T30 (#677): Argon at `high` spent about 57k of its 65.5k output tokens reasoning on a 438 KB packet three times (`finish=length`), where T3's 308 KB packet took 30k. The maintainer may reverse it by a new row. | #677, #798; `adversarial-council.md` § Council model floor; the T30 hold post of 10:04 UTC and the coordinator's answer the same hour |

| D-WORKFLOW-209 | 2026-10-25 | **A renovation dead-end table removes nothing and edits no recipe: T23 (and T40, T43 and T25 after it) record a disposition per unit -- dead upstream-carried, shadowed copy with its override live or dead, unshipped, fork-own dead with a proposed removal and its `Already written:` line, or reached after all -- and the removal of upstream-carried dead code is one class decision for the maintainer, put to them on #346 with the table's counts and the cost against the value; a fork-own dead unit's removal is proposed on the punch list and left for the coordinator.** The 1,604 rows are 1,601 upstream-carried: the fork tracks `upstream/next`, a deletion of upstream's file is a modify/delete at every merge (D-WORKFLOW-198's class), and the area futro already held T7 to *deletes nothing upstream carries*. The order's § T23 said *decides the removals*; this row narrows it to *decides the dispositions*. The three IDs before this one are the M7 lane's reservation; this row is the first M6 row after it. | #670, #848, #346; `docs/reviews/briefs/generic-packages-dead-ends.md` § 1 |
```


## Context 4: device-facts rows L17-L20, L27, L28, L31 (with the header)

```text
# Standing device facts

The things only a handheld can show (`vm-first.md`, D-QA-007/033), one row each,
with when each was last seen and on which cut -- so "have we checked this?" is a
| SM8550 boot on the Retroid Pocket Nova | Actual Nova boot chain, storage and compositor after an in-place update | 2026-10-12 04:28 UTC: approved8b511→bc9dfe update and one reboot; exact SYSTEM/kernel/ES/both RetroArch/5ABL files/both ABL slots; original mounts, empty queue and active frontend/zero restarts; credentials/paths/settings values preserved | `bc9dfe8141` | [Current deployment](../qa-logs/2026-10-12-owner-updates/README.md); original channels0/actual exits, owner use resumed, auto cloud sync off; no new frame/audio/gameplay claim | #557, #344; historical clock warning #328 |
| Nova frontend readiness after #529 | Actual SM8550 frontend service startup on the corrected image | 2026-10-12: first approved boot reaches active/idle frontend with NRestarts0; one observation, not a measured failure rate or rendering proof | `bc9dfe8141` | [Current deployment](../qa-logs/2026-10-12-owner-updates/README.md); original channels0/actual exits, owner use resumed, auto cloud sync off; no new frame/audio/gameplay claim | #529, #557 |
| Nova shutdown and bootloader recovery | Physical SM8550 power-off/restart and pre-Linux ABL behavior | 2026-10-12 read-only: three power-off intents, later reboot; empty pstore, no matching ES quit-mode entry; no reproduced failure or established cause | `bc9dfe8141` | [Incident timeline and evidence limits](../qa-logs/2026-10-12-nova-shutdown/README.md); owner reports one recovered Linux-load error; no agent mutation | #558; keep an eye on |
| Tailscale after a restart with the toggle on | Actual tailnet reconnection after boot | 2026-10-12 RG SP/Nova return on expected new build;2026-10-11 RG35XX SP return remains accepted | `bc9dfe8141` | [Current deployment](../qa-logs/2026-10-12-owner-updates/README.md); original channels0/actual exits, owner use resumed, auto cloud sync off; no new frame/audio/gameplay claim | #557, #556, #344, #174 (closed) |
| The Nova (SM8550) | Different physical board and update boot | 2026-10-12: detailed SM8550 row above; latest engineering firmware accepted on board | `bc9dfe8141` | [Current deployment](../qa-logs/2026-10-12-owner-updates/README.md); original channels0/actual exits, owner use resumed, auto cloud sync off; no new frame/audio/gameplay claim | #557, #344 |
| Retroid Pocket Nova: the sign-in window's pad | InputPlumber's virtual controller (the physical *AYN Odin2 Gamepad* node is hidden on the SM8550 image, so the bridge's next candidate and SELECT + START on it exist only on that device); the log's `gamepad bridge reading /dev/input/event7 (…)` and `player ended the sign-in from the handheld` | never (RC1 read `could not read the gamepad` on `event3`, 2026-09-29 17:17 of the device's clock) | -- | #331 | #331 |
| Retroid Pocket Nova: the stick LEDs | physical illumination and boot application of saved color/brightness on the Nova; VM proves eight sysfs writes, battery transitions and actual menu reselection | never for the corrected scripts; open item to test, not an unverified software criterion (D-QA-051) | -- | `docs/qa-logs/2026-10-03-led/` proves software behavior; no physical action performed | #332 |
```


## Context 5: .claude/rules/device-builds.md lines 16-26 (the device table)

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
25  | Retroid Pocket Nova | `SM8550` | aarch64 | cortex-a710 / cortex-x3 (`projects/ROCKNIX/devices/SM8550/options`), crypto-neon-fp-armv8; upstream release 20260901 lists it under SM8550 -- #150, D-QA-023. Check the current build inventory before deciding whether a cold build is needed. |
26  | VM / QA | `GENERIC_X64` | x86_64 | fork-only device; see `generic-x64-vm-testing` |
```


## projects/ROCKNIX/devices/SM8550/bootloader/update.sh @ 8ebaf8daad (whole, line-numbered, masked)

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
12      /dev/mmcblk*) BOOT_DISK=$(echo $BOOT_PART | sed -e "s,p[0-9]*,,g");;
13    esac
14  fi
15  
16  # mount $BOOT_ROOT rw
17  mount -o remount,rw $BOOT_ROOT
18  
19  if [ -d "$SYSTEM_ROOT/usr/share/bootloader/rocknix_abl" ]; then
20    mkdir -p $BOOT_ROOT/rocknix_abl
21    echo "Updating ROCKNIX ABL on SD..."
22    cp $SYSTEM_ROOT/usr/share/bootloader/rocknix_abl/* $BOOT_ROOT/rocknix_abl
23  fi
24  
25  $SYSTEM_ROOT/usr/bin/updateabl
26  
27  ### REMOVE IN THE FUTURE ###
28  # cleanup old boot files
29  [ -d "$BOOT_ROOT/boot" ] && rm -rf "$BOOT_ROOT/boot"
30  [ -d "$BOOT_ROOT/EFI" ] && rm -rf "$BOOT_ROOT/EFI"
31  # end
32  
33  # mount $BOOT_ROOT ro
34  sync
35  mount -o remount,ro $BOOT_ROOT
36  
37  echo "UPDATE" > /storage/.boot.hint
```


## projects/ROCKNIX/devices/SM8550/config/kernel-firmware.dat @ 8ebaf8daad (whole, line-numbered, masked)

```text
1  # USB_RTL8152
2  rtl_nic/rtl8153a-4.fw
3  
4  qca/hmtbtfw20.tlv
5  qca/hmtnv20.*
6  qcom/sm8550/a740_zap.mbn
7  qcom/a740_sqe.fw
8  qcom/gmu_gen70200.bin
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/lib/udev/hwdb.d/10-ayaneo.hwdb @ 8ebaf8daad (whole, line-numbered, masked)

```text
1  evdev:name:AYANEO DEVICE*
2   KEYBOARD_KEY_70068=volumeup
3   KEYBOARD_KEY_70069=volumedown
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/capability_maps/ayaneo_mcu_japanese.yaml @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  # yaml-language-server: $schema=https://raw.githubusercontent.com/ShadowBlip/InputPlumber/main/rootfs/usr/share/inputplumber/schema/capability_map_v2.json
  2  # Schema version number
  3  version: 2
  4  
  5  # The type of configuration schema
  6  kind: CapabilityMap
  7  
  8  # Name for the device event map
  9  name: AYANEO MCU Mapping Japanese
 10  
 11  # Unique identifier of the capability mapping
 12  id: ayaneo_mcu_japanese
 13  
 14  # List of mapped events
 15  mapping:
 16    - name: Guide Button
 17      source_events:
 18        - evdev:
 19            event_type: KEY
 20            event_code: BTN_MODE
 21            value_type: button
 22      target_event:
 23        gamepad:
 24          button: Guide
 25  
 26    - name: South Button
 27      source_events:
 28        - evdev:
 29            event_type: KEY
 30            event_code: BTN_EAST
 31            value_type: button
 32      target_event:
 33        gamepad:
 34          button: South
 35  
 36    - name: West Button
 37      source_events:
 38        - evdev:
 39            event_type: KEY
 40            event_code: BTN_NORTH
 41            value_type: button
 42      target_event:
 43        gamepad:
 44          button: West
 45  
 46    - name: North Button
 47      source_events:
 48        - evdev:
 49            event_type: KEY
 50            event_code: BTN_WEST
 51            value_type: button
 52      target_event:
 53        gamepad:
 54          button: North
 55  
 56    - name: East Button
 57      source_events:
 58        - evdev:
 59            event_type: KEY
 60            event_code: BTN_SOUTH
 61            value_type: button
 62      target_event:
 63        gamepad:
 64          button: East
 65  
 66    - name: Start Button
 67      source_events:
 68        - evdev:
 69            event_type: KEY
 70            event_code: BTN_START
 71            value_type: button
 72      target_event:
 73        gamepad:
 74          button: Start
 75  
 76    - name: Select Button
 77      source_events:
 78        - evdev:
 79            event_type: KEY
 80            event_code: BTN_SELECT
 81            value_type: button
 82      target_event:
 83        gamepad:
 84          button: Select
 85  
 86    - name: F1 Key
 87      source_events:
 88        - evdev:
 89            event_type: KEY
 90            event_code: BTN5
 91            value_type: button
 92      target_event:
 93        keyboard: KeyF1
 94  
 95    - name: Right Trigger
 96      source_events:
 97        - evdev:
 98            event_type: ABS
 99            event_code: ABS_GAS
100            value_type: trigger
101      target_event:
102        gamepad:
103          trigger:
104            name: RightTrigger
105  
106    - name: Left Trigger
107      source_events:
108        - evdev:
109            event_type: ABS
110            event_code: ABS_BRAKE
111            value_type: trigger
112      target_event:
113        gamepad:
114          trigger:
115            name: LeftTrigger
116  
117    - name: Right Bumper
118      source_events:
119        - evdev:
120            event_type: KEY
121            event_code: BTN_TR
122            value_type: button
123      target_event:
124        gamepad:
125          button: RightBumper
126  
127    - name: Left Bumper
128      source_events:
129        - evdev:
130            event_type: KEY
131            event_code: BTN_TL
132            value_type: button
133      target_event:
134        gamepad:
135          button: LeftBumper
136  
137    - name: Right Paddle
138      source_events:
139        - evdev:
140            event_type: KEY
141            event_code: BTN_C
142            value_type: button
143      target_event:
144        gamepad:
145          button: RightPaddle1
146  
147    - name: Left Paddle
148      source_events:
149        - evdev:
150            event_type: KEY
151            event_code: BTN_Z
152            value_type: button
153      target_event:
154        gamepad:
155          button: LeftPaddle1
156  
157    - name: Right Stick
158      source_events:
159        - evdev:
160            event_type: ABS
161            event_code: ABS_RX
162            value_type: joystick_x
163        - evdev:
164            event_type: ABS
165            event_code: ABS_RY
166            value_type: joystick_y
167      target_event:
168        gamepad:
169          axis:
170            name: RightStick
171  
172    - name: Left Stick
173      source_events:
174        - evdev:
175            event_type: ABS
176            event_code: ABS_X
177            value_type: joystick_x
178        - evdev:
179            event_type: ABS
180            event_code: ABS_Y
181            value_type: joystick_y
182      target_event:
183        gamepad:
184          axis:
185            name: LeftStick
186  
187    - name: Right Stick Click
188      source_events:
189        - evdev:
190            event_type: KEY
191            event_code: BTN_THUMBR
192            value_type: button
193      target_event:
194        gamepad:
195          button: RightStick
196  
197    - name: Left Stick Click
198      source_events:
199        - evdev:
200            event_type: KEY
201            event_code: BTN_THUMBL
202            value_type: button
203      target_event:
204        gamepad:
205          button: LeftStick
206  
207    - name: Dpad Left
208      source_events:
209        - evdev:
210            event_type: ABS
211            event_code: ABS_HAT0X
212            value_type: button
213            axis_direction: negative
214      target_event:
215        gamepad:
216          button: DPadLeft
217  
218    - name: Dpad Right
219      source_events:
220        - evdev:
221            event_type: ABS
222            event_code: ABS_HAT0X
223            value_type: button
224            axis_direction: positive
225      target_event:
226        gamepad:
227          button: DPadRight
228  
229    - name: Dpad Down
230      source_events:
231        - evdev:
232            event_type: ABS
233            event_code: ABS_HAT0Y
234            value_type: button
235            axis_direction: positive
236      target_event:
237        gamepad:
238          button: DPadDown
239  
240    - name: Dpad Up
241      source_events:
242        - evdev:
243            event_type: ABS
244            event_code: ABS_HAT0Y
245            value_type: button
246            axis_direction: negative
247      target_event:
248        gamepad:
249          button: DPadUp
250  
251  # List of events to filter from the source devices
252  filtered_events: []
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/capability_maps/ayaneo_mcu_xbox.yaml @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  # yaml-language-server: $schema=https://raw.githubusercontent.com/ShadowBlip/InputPlumber/main/rootfs/usr/share/inputplumber/schema/capability_map_v2.json
  2  # Schema version number
  3  version: 2
  4  
  5  # The type of configuration schema
  6  kind: CapabilityMap
  7  
  8  # Name for the device event map
  9  name: AYANEO MCU Mapping (Xbox mode)
 10  
 11  # Unique identifier of the capability mapping
 12  id: ayaneo_mcu_xbox
 13  
 14  # List of mapped events
 15  mapping:
 16    - name: Guide Button
 17      source_events:
 18        - evdev:
 19            event_type: KEY
 20            event_code: BTN_MODE
 21            value_type: button
 22      target_event:
 23        gamepad:
 24          button: Guide
 25  
 26    - name: South Button
 27      source_events:
 28        - evdev:
 29            event_type: KEY
 30            event_code: BTN_SOUTH
 31            value_type: button
 32      target_event:
 33        gamepad:
 34          button: South
 35  
 36    - name: West Button
 37      source_events:
 38        - evdev:
 39            event_type: KEY
 40            event_code: BTN_WEST
 41            value_type: button
 42      target_event:
 43        gamepad:
 44          button: West
 45  
 46    - name: North Button
 47      source_events:
 48        - evdev:
 49            event_type: KEY
 50            event_code: BTN_NORTH
 51            value_type: button
 52      target_event:
 53        gamepad:
 54          button: North
 55  
 56    - name: East Button
 57      source_events:
 58        - evdev:
 59            event_type: KEY
 60            event_code: BTN_EAST
 61            value_type: button
 62      target_event:
 63        gamepad:
 64          button: East
 65  
 66    - name: Start Button
 67      source_events:
 68        - evdev:
 69            event_type: KEY
 70            event_code: BTN_START
 71            value_type: button
 72      target_event:
 73        gamepad:
 74          button: Start
 75  
 76    - name: Select Button
 77      source_events:
 78        - evdev:
 79            event_type: KEY
 80            event_code: BTN_SELECT
 81            value_type: button
 82      target_event:
 83        gamepad:
 84          button: Select
 85  
 86    - name: F1 Key
 87      source_events:
 88        - evdev:
 89            event_type: KEY
 90            event_code: BTN5
 91            value_type: button
 92      target_event:
 93        keyboard: KeyF1
 94  
 95    - name: Right Trigger
 96      source_events:
 97        - evdev:
 98            event_type: ABS
 99            event_code: ABS_GAS
100            value_type: trigger
101      target_event:
102        gamepad:
103          trigger:
104            name: RightTrigger
105  
106    - name: Left Trigger
107      source_events:
108        - evdev:
109            event_type: ABS
110            event_code: ABS_BRAKE
111            value_type: trigger
112      target_event:
113        gamepad:
114          trigger:
115            name: LeftTrigger
116  
117    - name: Right Bumper
118      source_events:
119        - evdev:
120            event_type: KEY
121            event_code: BTN_TR
122            value_type: button
123      target_event:
124        gamepad:
125          button: RightBumper
126  
127    - name: Left Bumper
128      source_events:
129        - evdev:
130            event_type: KEY
131            event_code: BTN_TL
132            value_type: button
133      target_event:
134        gamepad:
135          button: LeftBumper
136  
137    - name: Right Paddle
138      source_events:
139        - evdev:
140            event_type: KEY
141            event_code: BTN_C
142            value_type: button
143      target_event:
144        gamepad:
145          button: RightPaddle1
146  
147    - name: Left Paddle
148      source_events:
149        - evdev:
150            event_type: KEY
151            event_code: BTN_Z
152            value_type: button
153      target_event:
154        gamepad:
155          button: LeftPaddle1
156  
157    - name: Right Stick
158      source_events:
159        - evdev:
160            event_type: ABS
161            event_code: ABS_RX
162            value_type: joystick_x
163        - evdev:
164            event_type: ABS
165            event_code: ABS_RY
166            value_type: joystick_y
167      target_event:
168        gamepad:
169          axis:
170            name: RightStick
171  
172    - name: Left Stick
173      source_events:
174        - evdev:
175            event_type: ABS
176            event_code: ABS_X
177            value_type: joystick_x
178        - evdev:
179            event_type: ABS
180            event_code: ABS_Y
181            value_type: joystick_y
182      target_event:
183        gamepad:
184          axis:
185            name: LeftStick
186  
187    - name: Right Stick Click
188      source_events:
189        - evdev:
190            event_type: KEY
191            event_code: BTN_THUMBR
192            value_type: button
193      target_event:
194        gamepad:
195          button: RightStick
196  
197    - name: Left Stick Click
198      source_events:
199        - evdev:
200            event_type: KEY
201            event_code: BTN_THUMBL
202            value_type: button
203      target_event:
204        gamepad:
205          button: LeftStick
206  
207    - name: Dpad Left
208      source_events:
209        - evdev:
210            event_type: ABS
211            event_code: ABS_HAT0X
212            value_type: button
213            axis_direction: negative
214      target_event:
215        gamepad:
216          button: DPadLeft
217  
218    - name: Dpad Right
219      source_events:
220        - evdev:
221            event_type: ABS
222            event_code: ABS_HAT0X
223            value_type: button
224            axis_direction: positive
225      target_event:
226        gamepad:
227          button: DPadRight
228  
229    - name: Dpad Down
230      source_events:
231        - evdev:
232            event_type: ABS
233            event_code: ABS_HAT0Y
234            value_type: button
235            axis_direction: positive
236      target_event:
237        gamepad:
238          button: DPadDown
239  
240    - name: Dpad Up
241      source_events:
242        - evdev:
243            event_type: ABS
244            event_code: ABS_HAT0Y
245            value_type: button
246            axis_direction: negative
247      target_event:
248        gamepad:
249          button: DPadUp
250  
251  # List of events to filter from the source devices
252  filtered_events: []
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/capability_maps/ayaneo_pocketsmini_gpio.yaml @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # yaml-language-server: $schema=https://raw.githubusercontent.com/ShadowBlip/InputPlumber/main/rootfs/usr/share/inputplumber/schema/capability_map_v2.json
 2  version: 2
 3  kind: CapabilityMap
 4  name: AYANEO Pocket S Mini GPIO Buttons
 5  id: ayaneo_pocketsmini_gpio
 6  
 7  mapping:
 8    - name: AYANEO Button
 9      source_events:
10        - evdev:
11            event_type: KEY
12            event_code: KEY_A
13            value_type: button
14      target_event:
15        gamepad:
16          button: Guide
17  
18    - name: Quick Access Button
19      source_events:
20        - evdev:
21            event_type: KEY
22            event_code: KEY_EQUAL
23            value_type: button
24      target_event:
25        gamepad:
26          button: QuickAccess
27  
28  filtered_events: []
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/capability_maps/ayn_mcu.yaml @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  # yaml-language-server: $schema=https://raw.githubusercontent.com/ShadowBlip/InputPlumber/main/rootfs/usr/share/inputplumber/schema/capability_map_v2.json
  2  # Schema version number
  3  version: 2
  4  
  5  # The type of configuration schema
  6  kind: CapabilityMap
  7  
  8  # Name for the device event map
  9  name: AYN MCU Mapping
 10  
 11  # Unique identifier of the capability mapping
 12  id: ayn_mcu
 13  
 14  # List of mapped events
 15  mapping:
 16    - name: Guide Button
 17      source_events:
 18        - evdev:
 19            event_type: KEY
 20            event_code: BTN_MODE
 21            value_type: button
 22      target_event:
 23        gamepad:
 24          button: Guide
 25  
 26    - name: South Button
 27      source_events:
 28        - evdev:
 29            event_type: KEY
 30            event_code: BTN_SOUTH
 31            value_type: button
 32      target_event:
 33        gamepad:
 34          button: South
 35  
 36    - name: West Button
 37      source_events:
 38        - evdev:
 39            event_type: KEY
 40            event_code: BTN_NORTH
 41            value_type: button
 42      target_event:
 43        gamepad:
 44          button: West
 45  
 46    - name: North Button
 47      source_events:
 48        - evdev:
 49            event_type: KEY
 50            event_code: BTN_WEST
 51            value_type: button
 52      target_event:
 53        gamepad:
 54          button: North
 55  
 56    - name: East Button
 57      source_events:
 58        - evdev:
 59            event_type: KEY
 60            event_code: BTN_EAST
 61            value_type: button
 62      target_event:
 63        gamepad:
 64          button: East
 65  
 66    - name: Start Button
 67      source_events:
 68        - evdev:
 69            event_type: KEY
 70            event_code: BTN_START
 71            value_type: button
 72      target_event:
 73        gamepad:
 74          button: Start
 75  
 76    - name: Select Button
 77      source_events:
 78        - evdev:
 79            event_type: KEY
 80            event_code: BTN_SELECT
 81            value_type: button
 82      target_event:
 83        gamepad:
 84          button: Select
 85  
 86    - name: F1 Key
 87      source_events:
 88        - evdev:
 89            event_type: KEY
 90            event_code: BTN_BACK
 91            value_type: button
 92      target_event:
 93        keyboard: KeyF1
 94  
 95    - name: Home Key
 96      source_events:
 97        - evdev:
 98            event_type: KEY
 99            event_code: KEY_F24
100            value_type: button
101      target_event:
102        keyboard: KeyHome
103  
104    - name: Right Trigger
105      source_events:
106        - evdev:
107            event_type: ABS
108            event_code: ABS_RZ
109            value_type: trigger
110      target_event:
111        gamepad:
112          trigger:
113            name: RightTrigger
114  
115    - name: Left Trigger
116      source_events:
117        - evdev:
118            event_type: ABS
119            event_code: ABS_Z
120            value_type: trigger
121      target_event:
122        gamepad:
123          trigger:
124            name: LeftTrigger
125  
126    - name: Right Bumper
127      source_events:
128        - evdev:
129            event_type: KEY
130            event_code: BTN_TR
131            value_type: button
132      target_event:
133        gamepad:
134          button: RightBumper
135  
136    - name: Left Bumper
137      source_events:
138        - evdev:
139            event_type: KEY
140            event_code: BTN_TL
141            value_type: button
142      target_event:
143        gamepad:
144          button: LeftBumper
145  
146    - name: Right Paddle
147      source_events:
148        - evdev:
149            event_type: KEY
150            event_code: BTN_C
151            value_type: button
152      target_event:
153        gamepad:
154          button: RightPaddle2
155  
156    - name: Left Paddle
157      source_events:
158        - evdev:
159            event_type: KEY
160            event_code: BTN_Z
161            value_type: button
162      target_event:
163        gamepad:
164          button: LeftPaddle2
165  
166    - name: Right Stick
167      source_events:
168        - evdev:
169            event_type: ABS
170            event_code: ABS_RX
171            value_type: joystick_x
172        - evdev:
173            event_type: ABS
174            event_code: ABS_RY
175            value_type: joystick_y
176      target_event:
177        gamepad:
178          axis:
179            name: RightStick
180  
181    - name: Left Stick
182      source_events:
183        - evdev:
184            event_type: ABS
185            event_code: ABS_X
186            value_type: joystick_x
187        - evdev:
188            event_type: ABS
189            event_code: ABS_Y
190            value_type: joystick_y
191      target_event:
192        gamepad:
193          axis:
194            name: LeftStick
195  
196    - name: Right Stick Click
197      source_events:
198        - evdev:
199            event_type: KEY
200            event_code: BTN_THUMBR
201            value_type: button
202      target_event:
203        gamepad:
204          button: RightStick
205  
206    - name: Left Stick Click
207      source_events:
208        - evdev:
209            event_type: KEY
210            event_code: BTN_THUMBL
211            value_type: button
212      target_event:
213        gamepad:
214          button: LeftStick
215  
216    - name: Dpad Left
217      source_events:
218        - evdev:
219            event_type: KEY
220            event_code: BTN_DPAD_LEFT
221            value_type: button
222      target_event:
223        gamepad:
224          button: DPadLeft
225  
226    - name: Dpad Right
227      source_events:
228        - evdev:
229            event_type: KEY
230            event_code: BTN_DPAD_RIGHT
231            value_type: button
232      target_event:
233        gamepad:
234          button: DPadRight
235  
236    - name: Dpad Down
237      source_events:
238        - evdev:
239            event_type: KEY
240            event_code: BTN_DPAD_DOWN
241            value_type: button
242      target_event:
243        gamepad:
244          button: DPadDown
245  
246    - name: Dpad Up
247      source_events:
248        - evdev:
249            event_type: KEY
250            event_code: BTN_DPAD_UP
251            value_type: button
252      target_event:
253        gamepad:
254          button: DPadUp
255  
256  # List of events to filter from the source devices
257  filtered_events: []
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/devices/01-ayaneo-controller-japanese.yaml @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # yaml-language-server: $schema=https://raw.githubusercontent.com/ShadowBlip/InputPlumber/main/rootfs/usr/share/inputplumber/schema/composite_device_v1.json
 2  # Schema version number
 3  version: 1
 4  
 5  # The type of configuration schema
 6  kind: CompositeDevice
 7  
 8  # Name of the composite device mapping
 9  name: AYANEO Japanese Layout
10  
11  # Only use this profile if *any* of the given matches matches. If this list is
12  # empty, then the source devices will *always* be checked.
13  # /sys/class/dmi/id/product_name
14  matches:
15    - udev:
16        sys_path: /sys/firmware/devicetree/base
17        attributes:
18          - name: model
19            value: AYANEO Pocket ACE
20    - udev:
21        sys_path: /sys/firmware/devicetree/base
22        attributes:
23          - name: model
24            value: AYANEO Pocket DMG
25    - udev:
26        sys_path: /sys/firmware/devicetree/base
27        attributes:
28          - name: model
29            value: AYANEO Pocket S Mini
30  
31  # Only allow a single source device per composite device of this type.
32  single_source: false
33  
34  # One or more source devices to combine into a single virtual device. The events
35  # from these devices will be watched and translated according to the key map.
36  source_devices:
37    - group: gamepad
38      evdev:
39        vendor_id: "1c4f"
40        product_id: "0002"
41        handler: event*
42      capability_map_id: ayaneo_mcu_japanese
43    - group: gamepad
44      evdev:
45        vendor_id: "045e"
46        product_id: "028e"
47        handler: event*
48      capability_map_id: ayaneo_mcu_japanese
49    - group: gamepad
50      evdev:
51        vendor_id: "4001"
52        product_id: "0428"
53        handler: event*
54      capability_map_id: ayaneo_mcu_japanese
55    - group: gamepad
56      evdev:
57        name: gpio-keys-pocket-s-mini
58        handler: event*
59      capability_map_id: ayaneo_pocketsmini_gpio
60  
61  # Optional configuration for the composite device
62  options:
63    # If true, InputPlumber will automatically try to manage the input device. If
64    # this is false, InputPlumber will not try to manage the device unless an
65    # external service enables management of the device. Defaults to 'false'
66    auto_manage: true
67  
68  # The target input device(s) to emulate by default
69  target_devices:
70    - ds5
71    - keyboard
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/devices/01-ayaneo-controller.yaml @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # yaml-language-server: $schema=https://raw.githubusercontent.com/ShadowBlip/InputPlumber/main/rootfs/usr/share/inputplumber/schema/composite_device_v1.json
 2  # Schema version number
 3  version: 1
 4  
 5  # The type of configuration schema
 6  kind: CompositeDevice
 7  
 8  # Name of the composite device mapping
 9  name: AYANEO Layout
10  
11  # Only use this profile if *any* of the given matches matches. If this list is
12  # empty, then the source devices will *always* be checked.
13  # /sys/class/dmi/id/product_name
14  matches:
15    - udev:
16        sys_path: /sys/firmware/devicetree/base
17        attributes:
18          - name: model
19            value: AYANEO Pocket EVO
20    - udev:
21        sys_path: /sys/firmware/devicetree/base
22        attributes:
23          - name: model
24            value: AYANEO Pocket DS
25    - udev:
26        sys_path: /sys/firmware/devicetree/base
27        attributes:
28          - name: model
29            value: AYANEO Pocket S 2K
30    - udev:
31        sys_path: /sys/firmware/devicetree/base
32        attributes:
33          - name: model
34            value: AYANEO Pocket S 1K
35  
36  # Only allow a single source device per composite device of this type.
37  single_source: false
38  
39  # One or more source devices to combine into a single virtual device. The events
40  # from these devices will be watched and translated according to the key map.
41  source_devices:
42    - group: gamepad
43      evdev:
44        vendor_id: "1c4f"
45        product_id: "0002"
46        handler: event*
47      capability_map_id: ayaneo_mcu_xbox
48    - group: gamepad
49      evdev:
50        vendor_id: "045e"
51        product_id: "028e"
52        handler: event*
53      capability_map_id: ayaneo_mcu_xbox
54  
55  # Optional configuration for the composite device
56  options:
57    # If true, InputPlumber will automatically try to manage the input device. If
58    # this is false, InputPlumber will not try to manage the device unless an
59    # external service enables management of the device. Defaults to 'false'
60    auto_manage: true
61  
62  # The target input device(s) to emulate by default
63  target_devices:
64    - ds5
65    - keyboard
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/devices/02-ayn-controller.yaml @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # yaml-language-server: $schema=https://raw.githubusercontent.com/ShadowBlip/InputPlumber/main/rootfs/usr/share/inputplumber/schema/composite_device_v1.json
 2  # Schema version number
 3  version: 1
 4  
 5  # The type of configuration schema
 6  kind: CompositeDevice
 7  
 8  # Name of the composite device mapping
 9  name: AYN Layout
10  
11  # Only use this profile if *any* of the given matches matches. If this list is
12  # empty, then the source devices will *always* be checked.
13  # /sys/class/dmi/id/product_name
14  matches:
15    - udev:
16        sys_path: /sys/firmware/devicetree/base
17        attributes:
18          - name: model
19            value: AYN Odin 2
20    - udev:
21        sys_path: /sys/firmware/devicetree/base
22        attributes:
23          - name: model
24            value: AYN Odin 2 Mini
25    - udev:
26        sys_path: /sys/firmware/devicetree/base
27        attributes:
28          - name: model
29            value: AYN Odin 2 Portal
30    - udev:
31        sys_path: /sys/firmware/devicetree/base
32        attributes:
33          - name: model
34            value: Retroid Pocket 6
35    - udev:
36        sys_path: /sys/firmware/devicetree/base
37        attributes:
38          - name: model
39            value: Retroid Pocket 6 TOP-DPAD
40    - udev:
41        sys_path: /sys/firmware/devicetree/base
42        attributes:
43          - name: model
44            value: Retroid Pocket Nova
45  
46  # Only allow a single source device per composite device of this type.
47  single_source: false
48  
49  # One or more source devices to combine into a single virtual device. The events
50  # from these devices will be watched and translated according to the key map.
51  source_devices:
52    - group: gamepad
53      evdev:
54        phys_path: rsinput-gamepad/input0
55        handler: event*
56      capability_map_id: ayn_mcu
57  
58    - group: gamepad
59      evdev:
60        name: gpio-keys
61        phys_path: gpio-keys/input0
62        handler: event*
63      capability_map_id: ayn_mcu
64  
65    # AYN Odin 2 back buttons (M1/M2): a separate gpio-keys device from the
66    # Odin 2 dts emitting BTN_Z (M1) / BTN_C (M2). Matched by name because
67    # its phys_path is shared with the other gpio-keys node. The ayn_mcu map
68    # turns them into Left/RightPaddle2, which the ds5-edge target emits as
69    # the Edge's real back-lever buttons.
70    - group: gamepad
71      evdev:
72        name: gpio-keys-paddles
73        handler: event*
74      capability_map_id: ayn_mcu
75  
76  # Optional configuration for the composite device
77  options:
78    # If true, InputPlumber will automatically try to manage the input device. If
79    # this is false, InputPlumber will not try to manage the device unless an
80    # external service enables management of the device. Defaults to 'false'
81    auto_manage: true
82  
83  # The target input device(s) to emulate by default. ds5-edge is the DualSense
84  # variant with back paddles, so the Odin 2's physical back buttons can be
85  # emitted as the Edge's real removable back-lever buttons (see ayn_mcu.yaml;
86  # decoded by the hid-playstation Edge support in patches/mainline/0006).
87  target_devices:
88    - ds5
89    - keyboard
```


## projects/ROCKNIX/devices/SM8550/filesystem/usr/share/inputplumber/devices/02-ayn-thor-controller.yaml @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  # yaml-language-server: $schema=https://raw.githubusercontent.com/ShadowBlip/InputPlumber/main/rootfs/usr/share/inputplumber/schema/composite_device_v1.json
 2  # Schema version number
 3  version: 1
 4  
 5  # The type of configuration schema
 6  kind: CompositeDevice
 7  
 8  # Name of the composite device mapping
 9  name: AYN Thor Layout
10  
11  # Only use this profile if *any* of the given matches matches. If this list is
12  # empty, then the source devices will *always* be checked.
13  # /sys/class/dmi/id/product_name
14  matches:
15    - udev:
16        sys_path: /sys/firmware/devicetree/base
17        attributes:
18          - name: model
19            value: AYN Thor
20  
21  # Only allow a single source device per composite device of this type.
22  single_source: false
23  
24  # One or more source devices to combine into a single virtual device. The events
25  # from these devices will be watched and translated according to the key map.
26  source_devices:
27    - group: gamepad
28      evdev:
29        phys_path: rsinput-gamepad/input0
30        handler: event*
31      capability_map_id: ayn_mcu
32  
33    - group: gamepad
34      evdev:
35        name: gpio-keys-ayn
36        phys_path: gpio-keys-ayn/input0
37        handler: event*
38      capability_map_id: ayn_mcu
39  
40  # Optional configuration for the composite device
41  options:
42    # If true, InputPlumber will automatically try to manage the input device. If
43    # this is false, InputPlumber will not try to manage the device unless an
44    # external service enables management of the device. Defaults to 'false'
45    auto_manage: true
46  
47  # The target input device(s) to emulate by default
48  target_devices:
49    - ds5
50    - keyboard
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocket-common.dtsi @ 8ebaf8daad (whole, line-numbered, masked)

```text
   1  // SPDX-License-Identifier: BSD-3-Clause
   2  /*
   3   * Copyright (c) 2025, Teguh Sobirin.
   4   */
   5  
   6  #include <dt-bindings/leds/common.h>
   7  #include <dt-bindings/regulator/qcom,rpmh-regulator.h>
   8  #include "qcs8550.dtsi"
   9  #include "pm8550.dtsi"
  10  #include "pm8550b.dtsi"
  11  #define PMK8550VE_SID 5
  12  #include "pm8550ve.dtsi"
  13  #include "pm8550vs.dtsi"
  14  #include "pmk8550.dtsi"
  15  
  16  /delete-node/ &aop_image_mem;
  17  /delete-node/ &aop_config_mem;
  18  /delete-node/ &camera_mem;
  19  /delete-node/ &ipa_fw_mem;
  20  /delete-node/ &ipa_gsi_mem;
  21  /delete-node/ &mpss_dsm_mem;
  22  /delete-node/ &mpss_mem;
  23  /delete-node/ &q6_mpss_dtb_mem;
  24  /delete-node/ &cdsp_mem;
  25  /delete-node/ &q6_cdsp_dtb_mem;
  26  
  27  /delete-node/ &remoteproc_mpss;
  28  /delete-node/ &remoteproc_cdsp;
  29  
  30  / {
  31  	chassis-type = "handset";
  32  
  33  	aliases {
  34  		serial0 = &uart7;
  35  		serial1 = &uart14;
  36  		hsuart0 = &uart11;
  37  	};
  38  
  39  	chosen {
  40  		stdout-path = "serial0:115200n8";
  41  	};
  42  
  43  	gpio-keys {
  44  		compatible = "gpio-keys";
  45  
  46  		pinctrl-0 = <&volume_up_n>;
  47  		pinctrl-names = "default";
  48  
  49  		key-volume-up {
  50  			label = "Volume Up";
  51  			debounce-interval = <15>;
  52  			gpios = <&pm8550_gpios 6 GPIO_ACTIVE_LOW>;
  53  			linux,code = <KEY_VOLUMEUP>;
  54  			linux,can-disable;
  55  			wakeup-source;
  56  		};
  57  	};
  58  
  59  	pmic-glink {
  60  		compatible = "qcom,sm8550-pmic-glink", "qcom,pmic-glink";
  61  		#address-cells = <1>;
  62  		#size-cells = <0>;
  63  		orientation-gpios = <&tlmm 11 GPIO_ACTIVE_HIGH>;
  64  
  65  		connector@0 {
  66  			compatible = "usb-c-connector";
  67  			reg = <0>;
  68  			power-role = "dual";
  69  			data-role = "dual";
  70  
  71  			ports {
  72  				#address-cells = <1>;
  73  				#size-cells = <0>;
  74  
  75  				port@0 {
  76  					reg = <0>;
  77  
  78  					pmic_glink_hs_in: endpoint {
  79  						remote-endpoint = <&usb_1_dwc3_hs>;
  80  					};
  81  				};
  82  
  83  				port@1 {
  84  					reg = <1>;
  85  
  86  					pmic_glink_ss_in: endpoint {
  87  						remote-endpoint = <&redriver_ss_out>;
  88  					};
  89  				};
  90  			};
  91  		};
  92  	};
  93  
  94  	reserved-memory {
  95  		hyp_mem: hyp-region@80000000 {
  96  			reg = <0 0x80000000 0 0xa00000>;
  97  			no-map;
  98  		};
  99  
 100  		cpusys_vm_mem: cpusys-vm-region@80a00000 {
 101  			reg = <0 0x80a00000 0 0x400000>;
 102  			no-map;
 103  		};
 104  
 105  		hyp_tags_mem: hyp-tags-region@80e00000 {
 106  			reg = <0 0x80e00000 0 0x3d0000>;
 107  			no-map;
 108  		};
 109  
 110  		xbl_sc_mem: xbl-sc-region@d8100000 {
 111  			reg = <0 0xd8100000 0 0x40000>;
 112  			no-map;
 113  		};
 114  
 115  		hyp_tags_reserved_mem: hyp-tags-reserved-region@811d0000 {
 116  			reg = <0 0x811d0000 0 0x30000>;
 117  			no-map;
 118  		};
 119  
 120  		xbl_dt_log_merged_mem: xbl-dt-log-merged-region@81a00000 {
 121  			reg = <0 0x81a00000 0 0x260000>;
 122  			no-map;
 123  		};
 124  
 125  		aop_config_merged_mem: aop-config-merged-region@81c80000 {
 126  			reg = <0 0x81c80000 0 0x74000>;
 127  			no-map;
 128  		};
 129  
 130  		chipinfo_mem: chipinfo-region@81cf4000 {
 131  			reg = <0 0x81cf4000 0 0x1000>;
 132  			no-map;
 133  		};
 134  
 135  		global_sync_mem: global-sync-region@82600000 {
 136  			reg = <0 0x82600000 0 0x100000>;
 137  			no-map;
 138  		};
 139  
 140  		tz_stat_mem: tz-stat-region@82700000 {
 141  			reg = <0 0x82700000 0 0x100000>;
 142  			no-map;
 143  		};
 144  
 145  		cpucp_fw_mem: cpucp-fw-region@d8140000 {
 146  			reg = <0 0xd8140000 0 0x1c0000>;
 147  			no-map;
 148  		};
 149  
 150  		qtee_mem: qtee-region@d8300000 {
 151  			reg = <0 0xd8300000 0 0x500000>;
 152  			no-map;
 153  		};
 154  
 155  		hwfence_shbuf: hwfence-shbuf-region@e6440000 {
 156  			reg = <0 0xe6440000 0 0x2dd000>;
 157  			no-map;
 158  		};
 159  
 160  		hyp_ext_reserved_mem: hyp-ext-reserved-region@ff700000 {
 161  			reg = <0 0xff700000 0 0x100000>;
 162  			no-map;
 163  		};
 164  
 165  		llcc_lpi_mem: llcc_lpi_region@ff800000 {
 166  			reg = <0 0xff800000 0 0x600000>;
 167  			no-map;
 168  		};
 169  
 170  		hyp_ext_tags_mem: hyp-ext-tags-region@fce00000 {
 171  			reg = <0 0xfce00000 0 0x2900000>;
 172  			no-map;
 173  		};
 174  
 175  		splash_region: splash_region@b8000000 {
 176  			reg = <0x0 0xb8000000 0x0 0x2b00000>;
 177  			label = "cont_splash_region";
 178  			no-map;
 179  		};
 180  	};
 181  
 182  	upd720201_avdd33_reg: upd720201-avdd33-regulator {
 183  		compatible = "regulator-fixed";
 184  
 185  		regulator-name = "upd720201_avdd33";
 186  		regulator-min-microvolt = <3300000>;
 187  		regulator-max-microvolt = <3300000>;
 188  
 189  		gpios = <&tlmm 18 GPIO_ACTIVE_HIGH>;
 190  		enable-active-high;
 191  
 192  		vin-supply = <&vph_pwr>;
 193  
 194  		pinctrl-0 = <&upd720201_avdd33>;
 195  		pinctrl-names = "default";
 196  	};
 197  
 198  	upd720201_vdd10_reg: upd720201-vdd10-regulator {
 199  		compatible = "regulator-fixed";
 200  
 201  		regulator-name = "upd720201_vdd10";
 202  		regulator-min-microvolt = <1050000>;
 203  		regulator-max-microvolt = <1050000>;
 204  
 205  		gpios = <&tlmm 13 GPIO_ACTIVE_HIGH>;
 206  		enable-active-high;
 207  
 208  		vin-supply = <&vph_pwr>;
 209  
 210  		pinctrl-0 = <&upd720201_vdd10>;
 211  		pinctrl-names = "default";
 212  	};
 213  
 214  	upd720201_vdd33_reg: upd720201-vdd33-regulator {
 215  		compatible = "regulator-fixed";
 216  
 217  		regulator-name = "upd720201_vdd33";
 218  		regulator-min-microvolt = <3300000>;
 219  		regulator-max-microvolt = <3300000>;
 220  
 221  		gpios = <&tlmm 10 GPIO_ACTIVE_HIGH>;
 222  		enable-active-high;
 223  
 224  		vin-supply = <&vph_pwr>;
 225  
 226  		pinctrl-0 = <&upd720201_vdd33>;
 227  		pinctrl-names = "default";
 228  	};
 229  
 230  	sound {
 231  		status = "okay";
 232  		compatible = "qcom,sm8550-sndcard", "qcom,sm8450-sndcard";
 233  		model = "SM8550-APS";
 234  		audio-routing = "SpkrLeft IN", "WSA_SPK1 OUT",
 235  				"SpkrRight IN", "WSA_SPK2 OUT",
 236  				"VA DMIC0", "vdd-micb",
 237  				"VA DMIC1", "vdd-micb";
 238  
 239  		wsa-dai-link {
 240  			link-name = "WSA Playback";
 241  
 242  			cpu {
 243  				sound-dai = <&q6apmbedai WSA_CODEC_DMA_RX_0>;
 244  			};
 245  
 246  			codec {
 247  				sound-dai = <&spk_amp_l>, <&spk_amp_r>, <&swr0 0>, <&lpass_wsamacro 0>;
 248  			};
 249  
 250  			platform {
 251  				sound-dai = <&q6apm>;
 252  			};
 253  		};
 254  
 255  		va-dai-link {
 256  			link-name = "VA Capture";
 257  
 258  			cpu {
 259  				sound-dai = <&q6apmbedai VA_CODEC_DMA_TX_0>;
 260  			};
 261  
 262  			codec {
 263  				sound-dai = <&lpass_vamacro 0>;
 264  			};
 265  
 266  			platform {
 267  				sound-dai = <&q6apm>;
 268  			};
 269  		};
 270  
 271  		dp0-dai-link {
 272  			link-name = "DP0 Playback";
 273  			cpu {
 274  				sound-dai = <&q6apmbedai DISPLAY_PORT_RX_0>;
 275  			};
 276  
 277  			platform {
 278  				sound-dai = <&q6apm>;
 279  			};
 280  
 281  			codec {
 282  				sound-dai = <&mdss_dp0>;
 283  			};
 284  		};
 285  	};
 286  
 287  	thermal-zones {
 288  		cpuss0-thermal {
 289  			polling-delay = <200>;
 290  			trips {
 291  				cpuss0_fan0: trip-point2 { temperature = <40000>; hysteresis = <3000>; type = "passive"; };
 292  				cpuss0_fan1: trip-point3 { temperature = <50000>; hysteresis = <3000>; type = "passive"; };
 293  				cpuss0_fan2: trip-point4 { temperature = <60000>; hysteresis = <3000>; type = "passive"; };
 294  				cpuss0_fan3: trip-point5 { temperature = <65000>; hysteresis = <3000>; type = "passive"; };
 295  				cpuss0_fan4: trip-point6 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 296  				cpuss0_fan5: trip-point7 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 297  				cpuss0_fan6: trip-point8 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 298  			};
 299  
 300  		};
 301  		cpuss1-thermal {
 302  			polling-delay = <200>;
 303  			trips {
 304  				cpuss1_fan0: trip-point2 { temperature = <40000>; hysteresis = <3000>; type = "passive"; };
 305  				cpuss1_fan1: trip-point3 { temperature = <50000>; hysteresis = <3000>; type = "passive"; };
 306  				cpuss1_fan2: trip-point4 { temperature = <60000>; hysteresis = <3000>; type = "passive"; };
 307  				cpuss1_fan3: trip-point5 { temperature = <65000>; hysteresis = <3000>; type = "passive"; };
 308  				cpuss1_fan4: trip-point6 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 309  				cpuss1_fan5: trip-point7 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 310  				cpuss1_fan6: trip-point8 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 311  			};
 312  
 313  		};
 314  		cpuss2-thermal {
 315  			polling-delay = <200>;
 316  			trips {
 317  				cpuss2_fan0: trip-point2 { temperature = <40000>; hysteresis = <3000>; type = "passive"; };
 318  				cpuss2_fan1: trip-point3 { temperature = <50000>; hysteresis = <3000>; type = "passive"; };
 319  				cpuss2_fan2: trip-point4 { temperature = <60000>; hysteresis = <3000>; type = "passive"; };
 320  				cpuss2_fan3: trip-point5 { temperature = <65000>; hysteresis = <3000>; type = "passive"; };
 321  				cpuss2_fan4: trip-point6 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 322  				cpuss2_fan5: trip-point7 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 323  				cpuss2_fan6: trip-point8 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 324  			};
 325  
 326  		};
 327  		cpuss3-thermal {
 328  			polling-delay = <200>;
 329  			trips {
 330  				cpuss3_fan0: trip-point2 { temperature = <40000>; hysteresis = <3000>; type = "passive"; };
 331  				cpuss3_fan1: trip-point3 { temperature = <50000>; hysteresis = <3000>; type = "passive"; };
 332  				cpuss3_fan2: trip-point4 { temperature = <60000>; hysteresis = <3000>; type = "passive"; };
 333  				cpuss3_fan3: trip-point5 { temperature = <65000>; hysteresis = <3000>; type = "passive"; };
 334  				cpuss3_fan4: trip-point6 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 335  				cpuss3_fan5: trip-point7 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 336  				cpuss3_fan6: trip-point8 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 337  			};
 338  
 339  		};
 340  		cpu7-top-thermal {
 341  			polling-delay = <200>;
 342  			trips {
 343  				cpu7_top_fan0: trip-point2 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 344  				cpu7_top_fan1: trip-point3 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 345  				cpu7_top_fan2: trip-point4 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 346  			};
 347  
 348  		};
 349  		gpuss-0-thermal {
 350  			polling-delay = <200>;
 351  			trips {
 352  				gpuss0_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 353  				gpuss0_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 354  				gpuss0_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 355  			};
 356  
 357  		};
 358  		gpuss-1-thermal {
 359  			polling-delay = <200>;
 360  			trips {
 361  				gpuss1_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 362  				gpuss1_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 363  				gpuss1_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 364  			};
 365  
 366  		};
 367  		gpuss-2-thermal {
 368  			polling-delay = <200>;
 369  			trips {
 370  				gpuss2_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 371  				gpuss2_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 372  				gpuss2_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 373  			};
 374  
 375  		};
 376  		gpuss-3-thermal {
 377  			polling-delay = <200>;
 378  			trips {
 379  				gpuss3_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 380  				gpuss3_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 381  				gpuss3_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 382  			};
 383  
 384  		};
 385  		gpuss-4-thermal {
 386  			polling-delay = <200>;
 387  			trips {
 388  				gpuss4_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 389  				gpuss4_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 390  				gpuss4_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 391  			};
 392  
 393  		};
 394  		gpuss-5-thermal {
 395  			polling-delay = <200>;
 396  			trips {
 397  				gpuss5_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 398  				gpuss5_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 399  				gpuss5_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 400  			};
 401  
 402  		};
 403  		gpuss-6-thermal {
 404  			polling-delay = <200>;
 405  			trips {
 406  				gpuss6_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 407  				gpuss6_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 408  				gpuss6_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 409  			};
 410  
 411  		};
 412  		gpuss-7-thermal {
 413  			polling-delay = <200>;
 414  			trips {
 415  				gpuss7_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 416  				gpuss7_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 417  				gpuss7_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 418  			};
 419  
 420  		};
 421  	};
 422  
 423  	vdd_fan_5v0: vdd-fan-5v0-regulator {
 424  		compatible = "regulator-fixed";
 425  		regulator-name = "vdd_fan_5v0";
 426  
 427  		regulator-min-microvolt = <5000000>;
 428  		regulator-max-microvolt = <5000000>;
 429  
 430  		gpio = <&tlmm 31 GPIO_ACTIVE_HIGH>;
 431  		enable-active-high;
 432  
 433  		pinctrl-names = "default";
 434  		pinctrl-0 = <&fan_pwr_active>;
 435  
 436  		regulator-state-mem {
 437  			regulator-off-in-suspend;
 438  		};
 439  	};
 440  
 441  	vph_pwr: regulator-vph-pwr {
 442  		compatible = "regulator-fixed";
 443  		regulator-name = "  vph_pwr";
 444  		regulator-min-microvolt = <3700000>;
 445  		regulator-max-microvolt = <3700000>;
 446  
 447  		regulator-always-on;
 448  		regulator-boot-on;
 449  	};
 450  
 451  	pwm_fan: pwm-fan {
 452  		compatible = "pwm-fan";
 453  
 454  		pinctrl-names = "default", "sleep";
 455  		pinctrl-0 = <&fan_pwm_active>, <&fan_int>;
 456  
 457  		fan-supply = <&vdd_fan_5v0>;
 458  		pwms = <&pm8550_pwm 3 40000>;
 459  		interrupt-parent = <&tlmm>;
 460  		interrupts = <64 IRQ_TYPE_EDGE_FALLING>;
 461  
 462  		#cooling-cells = <2>;
 463  		cooling-levels = <0 30 45 60 70 90 120 150>;
 464  	};
 465  
 466  	wcn7850-pmu {
 467  		compatible = "qcom,wcn7850-pmu";
 468  
 469  		pinctrl-names = "default";
 470  		pinctrl-0 = <&wlan_en>, <&bt_default>, <&pmk8550_sleep_clk>;
 471  
 472  		wlan-enable-gpios = <&tlmm 80 GPIO_ACTIVE_HIGH>;
 473  		bt-enable-gpios = <&tlmm 81 GPIO_ACTIVE_HIGH>;
 474  
 475  		vdd-supply = <&vreg_s5g_0p85>;
 476  		vddio-supply = <&vreg_l15b_1p8>;
 477  		vddaon-supply = <&vreg_s2g_0p85>;
 478  		vdddig-supply = <&vreg_s4e_0p95>;
 479  		vddrfa1p2-supply = <&vreg_s4g_1p25>;
 480  		vddrfa1p8-supply = <&vreg_s6g_1p86>;
 481  
 482  		regulators {
 483  			vreg_pmu_rfa_cmn: ldo0 {
 484  				regulator-name = "vreg_pmu_rfa_cmn";
 485  			};
 486  
 487  			vreg_pmu_aon_0p59: ldo1 {
 488  				regulator-name = "vreg_pmu_aon_0p59";
 489  			};
 490  
 491  			vreg_pmu_wlcx_0p8: ldo2 {
 492  				regulator-name = "vreg_pmu_wlcx_0p8";
 493  			};
 494  
 495  			vreg_pmu_wlmx_0p85: ldo3 {
 496  				regulator-name = "vreg_pmu_wlmx_0p85";
 497  			};
 498  
 499  			vreg_pmu_btcmx_0p85: ldo4 {
 500  				regulator-name = "vreg_pmu_btcmx_0p85";
 501  			};
 502  
 503  			vreg_pmu_rfa_0p8: ldo5 {
 504  				regulator-name = "vreg_pmu_rfa_0p8";
 505  			};
 506  
 507  			vreg_pmu_rfa_1p2: ldo6 {
 508  				regulator-name = "vreg_pmu_rfa_1p2";
 509  			};
 510  
 511  			vreg_pmu_rfa_1p8: ldo7 {
 512  				regulator-name = "vreg_pmu_rfa_1p8";
 513  			};
 514  
 515  			vreg_pmu_pcie_0p9: ldo8 {
 516  				regulator-name = "vreg_pmu_pcie_0p9";
 517  			};
 518  
 519  			vreg_pmu_pcie_1p8: ldo9 {
 520  				regulator-name = "vreg_pmu_pcie_1p8";
 521  			};
 522  		};
 523  	};
 524  };
 525  
 526  /* DMIC 01 23 */
 527  &lpass_vamacro {
 528  	pinctrl-0 = <&dmic01_default>, <&dmic23_default>;
 529  	pinctrl-names = "default";
 530  	vdd-micb-supply = <&vreg_l10b_1p8>;
 531  	qcom,dmic-sample-rate = <4800000>;
 532  };
 533  
 534  &apps_rsc {
 535  	regulators-0 {
 536  		compatible = "qcom,pm8550-rpmh-regulators";
 537  		qcom,pmic-id = "b";
 538  
 539  		vdd-bob1-supply = <&vph_pwr>;
 540  		vdd-bob2-supply = <&vph_pwr>;
 541  		vdd-l1-l4-l10-supply = <&vreg_s6g_1p86>;
 542  		vdd-l2-l13-l14-supply = <&vreg_bob1>;
 543  		vdd-l3-supply = <&vreg_s4g_1p25>;
 544  		vdd-l5-l16-supply = <&vreg_bob1>;
 545  		vdd-l6-l7-supply = <&vreg_bob1>;
 546  		vdd-l8-l9-supply = <&vreg_bob1>;
 547  		vdd-l11-supply = <&vreg_s4g_1p25>;
 548  		vdd-l12-supply = <&vreg_s6g_1p86>;
 549  		vdd-l15-supply = <&vreg_s6g_1p86>;
 550  		vdd-l17-supply = <&vreg_bob2>;
 551  
 552  		vreg_bob1: bob1 {
 553  			regulator-name = "vreg_bob1";
 554  			regulator-min-microvolt = <3296000>;
 555  			regulator-max-microvolt = <3960000>;
 556  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 557  		};
 558  
 559  		vreg_bob2: bob2 {
 560  			regulator-name = "vreg_bob2";
 561  			regulator-min-microvolt = <2720000>;
 562  			regulator-max-microvolt = <3960000>;
 563  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 564  		};
 565  
 566  		vreg_l2b_3p0: ldo2 {
 567  			regulator-name = "vreg_l2b_3p0";
 568  			regulator-min-microvolt = <3008000>;
 569  			regulator-max-microvolt = <3008000>;
 570  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 571  			regulator-allow-set-load;
 572  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 573  						   RPMH_REGULATOR_MODE_HPM>;
 574  		};
 575  
 576  		vreg_l5b_3p1: ldo5 {
 577  			regulator-name = "vreg_l5b_3p1";
 578  			regulator-min-microvolt = <3104000>;
 579  			regulator-max-microvolt = <3104000>;
 580  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 581  			regulator-allow-set-load;
 582  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 583  						   RPMH_REGULATOR_MODE_HPM>;
 584  		};
 585  
 586  		vreg_l6b_1p8: ldo6 {
 587  			regulator-name = "vreg_l6b_1p8";
 588  			regulator-min-microvolt = <1800000>;
 589  			regulator-max-microvolt = <3008000>;
 590  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 591  			regulator-allow-set-load;
 592  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 593  						   RPMH_REGULATOR_MODE_HPM>;
 594  		};
 595  
 596  		vreg_l7b_1p8: ldo7 {
 597  			regulator-name = "vreg_l7b_1p8";
 598  			regulator-min-microvolt = <1800000>;
 599  			regulator-max-microvolt = <3008000>;
 600  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 601  		};
 602  
 603  		vreg_l8b_1p8: ldo8 {
 604  			regulator-name = "vreg_l8b_1p8";
 605  			regulator-min-microvolt = <1800000>;
 606  			regulator-max-microvolt = <3008000>;
 607  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 608  			regulator-allow-set-load;
 609  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 610  						   RPMH_REGULATOR_MODE_HPM>;
 611  		};
 612  
 613  		vreg_l9b_2p9: ldo9 {
 614  			regulator-name = "vreg_l9b_2p9";
 615  			regulator-min-microvolt = <2960000>;
 616  			regulator-max-microvolt = <3008000>;
 617  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 618  			regulator-allow-set-load;
 619  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 620  						   RPMH_REGULATOR_MODE_HPM>;
 621  		};
 622  
 623  		vreg_l10b_1p8: ldo10 {
 624  			regulator-name = "vreg_l10b_1p8";
 625  			regulator-min-microvolt = <1800000>;
 626  			regulator-max-microvolt = <1800000>;
 627  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 628  			regulator-allow-set-load;
 629  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 630  						   RPMH_REGULATOR_MODE_HPM>;
 631  		};
 632  
 633  		vreg_l11b_1p2: ldo11 {
 634  			regulator-name = "vreg_l11b_1p2";
 635  			regulator-min-microvolt = <1200000>;
 636  			regulator-max-microvolt = <1504000>;
 637  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 638  			regulator-allow-set-load;
 639  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 640  						   RPMH_REGULATOR_MODE_HPM>;
 641  		};
 642  
 643  		vreg_l12b_1p8: ldo12 {
 644  			regulator-name = "vreg_l12b_1p8";
 645  			regulator-min-microvolt = <1800000>;
 646  			regulator-max-microvolt = <1800000>;
 647  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 648  			regulator-allow-set-load;
 649  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 650  						   RPMH_REGULATOR_MODE_HPM>;
 651  		};
 652  
 653  		vreg_l13b_3p0: ldo13 {
 654  			regulator-name = "vreg_l13b_3p0";
 655  			regulator-min-microvolt = <3000000>;
 656  			regulator-max-microvolt = <3000000>;
 657  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 658  			regulator-allow-set-load;
 659  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 660  						   RPMH_REGULATOR_MODE_HPM>;
 661  		};
 662  
 663  		vreg_l14b_3p2: ldo14 {
 664  			regulator-name = "vreg_l14b_3p2";
 665  			regulator-min-microvolt = <3200000>;
 666  			regulator-max-microvolt = <3200000>;
 667  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 668  			regulator-allow-set-load;
 669  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 670  						   RPMH_REGULATOR_MODE_HPM>;
 671  		};
 672  
 673  		vreg_l15b_1p8: ldo15 {
 674  			regulator-name = "vreg_l15b_1p8";
 675  			regulator-min-microvolt = <1800000>;
 676  			regulator-max-microvolt = <1800000>;
 677  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 678  			regulator-allow-set-load;
 679  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 680  						   RPMH_REGULATOR_MODE_HPM>;
 681  		};
 682  
 683  		vreg_l16b_2p8: ldo16 {
 684  			regulator-name = "vreg_l16b_2p8";
 685  			regulator-min-microvolt = <2800000>;
 686  			regulator-max-microvolt = <2800000>;
 687  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 688  			regulator-allow-set-load;
 689  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 690  						   RPMH_REGULATOR_MODE_HPM>;
 691  		};
 692  
 693  		vreg_l17b_2p5: ldo17 {
 694  			regulator-name = "vreg_l17b_2p5";
 695  			regulator-min-microvolt = <2504000>;
 696  			regulator-max-microvolt = <2504000>;
 697  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 698  		};
 699  	};
 700  
 701  	regulators-1 {
 702  		compatible = "qcom,pm8550vs-rpmh-regulators";
 703  		qcom,pmic-id = "c";
 704  
 705  		vdd-l1-supply = <&vreg_s4g_1p25>;
 706  		vdd-l2-supply = <&vreg_s4e_0p95>;
 707  		vdd-l3-supply = <&vreg_s4e_0p95>;
 708  
 709  		vreg_l3c_0p9: ldo3 {
 710  			regulator-name = "vreg_l3c_0p9";
 711  			regulator-min-microvolt = <880000>;
 712  			regulator-max-microvolt = <912000>;
 713  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 714  			regulator-allow-set-load;
 715  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 716  						   RPMH_REGULATOR_MODE_HPM>;
 717  		};
 718  	};
 719  
 720  	regulators-2 {
 721  		compatible = "qcom,pm8550vs-rpmh-regulators";
 722  		qcom,pmic-id = "d";
 723  
 724  		vdd-l1-supply = <&vreg_s4e_0p95>;
 725  		vdd-l2-supply = <&vreg_s4e_0p95>;
 726  		vdd-l3-supply = <&vreg_s4e_0p95>;
 727  
 728  		vreg_l1d_0p88: ldo1 {
 729  			regulator-name = "vreg_l1d_0p88";
 730  			regulator-min-microvolt = <880000>;
 731  			regulator-max-microvolt = <920000>;
 732  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 733  			regulator-allow-set-load;
 734  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 735  						   RPMH_REGULATOR_MODE_HPM>;
 736  		};
 737  	};
 738  
 739  	regulators-3 {
 740  		compatible = "qcom,pm8550vs-rpmh-regulators";
 741  		qcom,pmic-id = "e";
 742  
 743  		vdd-l1-supply = <&vreg_s4e_0p95>;
 744  		vdd-l2-supply = <&vreg_s4e_0p95>;
 745  		vdd-l3-supply = <&vreg_s4g_1p25>;
 746  		vdd-s4-supply = <&vph_pwr>;
 747  		vdd-s5-supply = <&vph_pwr>;
 748  
 749  		vreg_s4e_0p95: smps4 {
 750  			regulator-name = "vreg_s4e_0p95";
 751  			regulator-min-microvolt = <904000>;
 752  			regulator-max-microvolt = <984000>;
 753  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 754  		};
 755  
 756  		vreg_s5e_1p08: smps5 {
 757  			regulator-name = "vreg_s5e_1p08";
 758  			regulator-min-microvolt = <1010000>;
 759  			regulator-max-microvolt = <1120000>;
 760  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 761  		};
 762  
 763  		vreg_l1e_0p88: ldo1 {
 764  			regulator-name = "vreg_l1e_0p88";
 765  			regulator-min-microvolt = <880000>;
 766  			regulator-max-microvolt = <880000>;
 767  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 768  			regulator-allow-set-load;
 769  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 770  						   RPMH_REGULATOR_MODE_HPM>;
 771  		};
 772  
 773  		vreg_l2e_0p9: ldo2 {
 774  			regulator-name = "vreg_l2e_0p9";
 775  			regulator-min-microvolt = <904000>;
 776  			regulator-max-microvolt = <970000>;
 777  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 778  			regulator-allow-set-load;
 779  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 780  						   RPMH_REGULATOR_MODE_HPM>;
 781  		};
 782  
 783  		vreg_l3e_1p2: ldo3 {
 784  			regulator-name = "vreg_l3e_1p2";
 785  			regulator-min-microvolt = <1200000>;
 786  			regulator-max-microvolt = <1200000>;
 787  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 788  			regulator-allow-set-load;
 789  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 790  						   RPMH_REGULATOR_MODE_HPM>;
 791  		};
 792  	};
 793  
 794  	regulators-4 {
 795  		compatible = "qcom,pm8550ve-rpmh-regulators";
 796  		qcom,pmic-id = "f";
 797  
 798  		vdd-l1-supply = <&vreg_s4e_0p95>;
 799  		vdd-l2-supply = <&vreg_s4e_0p95>;
 800  		vdd-l3-supply = <&vreg_s4e_0p95>;
 801  		vdd-s4-supply = <&vph_pwr>;
 802  
 803  		vreg_s4f_0p5: smps4 {
 804  			regulator-name = "vreg_s4f_0p5";
 805  			regulator-min-microvolt = <500000>;
 806  			regulator-max-microvolt = <700000>;
 807  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 808  		};
 809  
 810  		vreg_l1f_0p9: ldo1 {
 811  			regulator-name = "vreg_l1f_0p9";
 812  			regulator-min-microvolt = <912000>;
 813  			regulator-max-microvolt = <912000>;
 814  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 815  			regulator-allow-set-load;
 816  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 817  						   RPMH_REGULATOR_MODE_HPM>;
 818  		};
 819  
 820  		vreg_l2f_0p88: ldo2 {
 821  			regulator-name = "vreg_l2f_0p88";
 822  			regulator-min-microvolt = <880000>;
 823  			regulator-max-microvolt = <912000>;
 824  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 825  			regulator-allow-set-load;
 826  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 827  						   RPMH_REGULATOR_MODE_HPM>;
 828  		};
 829  
 830  		vreg_l3f_0p88: ldo3 {
 831  			regulator-name = "vreg_l3f_0p88";
 832  			regulator-min-microvolt = <880000>;
 833  			regulator-max-microvolt = <912000>;
 834  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 835  			regulator-allow-set-load;
 836  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 837  						   RPMH_REGULATOR_MODE_HPM>;
 838  		};
 839  	};
 840  
 841  	regulators-5 {
 842  		compatible = "qcom,pm8550vs-rpmh-regulators";
 843  		qcom,pmic-id = "g";
 844  		vdd-l1-supply = <&vreg_s4g_1p25>;
 845  		vdd-l2-supply = <&vreg_s4g_1p25>;
 846  		vdd-l3-supply = <&vreg_s4g_1p25>;
 847  		vdd-s1-supply = <&vph_pwr>;
 848  		vdd-s2-supply = <&vph_pwr>;
 849  		vdd-s3-supply = <&vph_pwr>;
 850  		vdd-s4-supply = <&vph_pwr>;
 851  		vdd-s5-supply = <&vph_pwr>;
 852  		vdd-s6-supply = <&vph_pwr>;
 853  
 854  		vreg_s1g_1p25: smps1 {
 855  			regulator-name = "vreg_s1g_1p25";
 856  			regulator-min-microvolt = <1200000>;
 857  			regulator-max-microvolt = <1300000>;
 858  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 859  		};
 860  
 861  		vreg_s2g_0p85: smps2 {
 862  			regulator-name = "vreg_s2g_0p85";
 863  			regulator-min-microvolt = <800000>;
 864  			regulator-max-microvolt = <1000000>;
 865  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 866  		};
 867  
 868  		vreg_s3g_0p8: smps3 {
 869  			regulator-name = "vreg_s3g_0p8";
 870  			regulator-min-microvolt = <300000>;
 871  			regulator-max-microvolt = <1004000>;
 872  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 873  		};
 874  
 875  		vreg_s4g_1p25: smps4 {
 876  			regulator-name = "vreg_s4g_1p25";
 877  			regulator-min-microvolt = <1200000>;
 878  			regulator-max-microvolt = <1352000>;
 879  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 880  		};
 881  
 882  		vreg_s5g_0p85: smps5 {
 883  			regulator-name = "vreg_s5g_0p85";
 884  			regulator-min-microvolt = <500000>;
 885  			regulator-max-microvolt = <1004000>;
 886  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 887  		};
 888  
 889  		vreg_s6g_1p86: smps6 {
 890  			regulator-name = "vreg_s6g_1p86";
 891  			regulator-min-microvolt = <1800000>;
 892  			regulator-max-microvolt = <2000000>;
 893  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 894  		};
 895  
 896  		vreg_l1g_1p2: ldo1 {
 897  			regulator-name = "vreg_l1g_1p2";
 898  			regulator-min-microvolt = <1200000>;
 899  			regulator-max-microvolt = <1200000>;
 900  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 901  			regulator-allow-set-load;
 902  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 903  						   RPMH_REGULATOR_MODE_HPM>;
 904  		};
 905  
 906  		vreg_l3g_1p2: ldo3 {
 907  			regulator-name = "vreg_l3g_1p2";
 908  			regulator-min-microvolt = <1200000>;
 909  			regulator-max-microvolt = <1200000>;
 910  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 911  			regulator-allow-set-load;
 912  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 913  						   RPMH_REGULATOR_MODE_HPM>;
 914  		};
 915  	};
 916  };
 917  
 918  &pm8550_gpios {
 919  	sdc2_card_det_n: sdc2-card-det-n-state {
 920  		pins = "gpio12";
 921  		function = "normal";
 922  		input-enable;
 923  		output-disable;
 924  		bias-pull-up;
 925  		power-source = <1>;
 926  	};
 927  
 928  	volume_up_n: volume-up-n-state {
 929  		pins = "gpio6";
 930  		function = "normal";
 931  		power-source = <1>;
 932  		bias-pull-up;
 933  		input-enable;
 934  	};
 935  
 936  	fan_pwm_active: fan-pwm-active-state {
 937  		pins = "gpio9";
 938  		function = "func1";
 939  		output-low;
 940  		bias-disable;
 941  		power-source = <0>;
 942  		qcom,drive-strength = <3>; /* PMIC_GPIO_STRENGTH_LOW */
 943  	};
 944  };
 945  
 946  &pmk8550_gpios {
 947  	pmk8550_sleep_clk: sleep-clk-state {
 948  		pins = "gpio3";
 949  		function = "func1";
 950  		input-disable;
 951  		output-enable;
 952  		bias-disable;
 953  		power-source = <0>;
 954  	};
 955  };
 956  
 957  &pm8550b_eusb2_repeater {
 958  	vdd18-supply = <&vreg_l15b_1p8>;
 959  	vdd3-supply = <&vreg_l5b_3p1>;
 960  };
 961  
 962  &pon_pwrkey {
 963  	status = "okay";
 964  };
 965  
 966  &pon_resin {
 967  	linux,code = <KEY_VOLUMEDOWN>;
 968  
 969  	status = "okay";
 970  };
 971  
 972  &pmk8550_rtc {
 973  	nvmem-cells = <&rtc_offset>;
 974  	nvmem-cell-names = "offset";
 975  };
 976  
 977  &pmk8550_sdam_2 {
 978  	rtc_offset: rtc-offset@bc {
 979  		reg = <0xbc 0x4>;
 980  	};
 981  };
 982  
 983  &qupv3_id_0 {
 984  	status = "okay";
 985  };
 986  
 987  &qupv3_id_1 {
 988  	status = "okay";
 989  
 990  	/* AYANEO Controller serial interface */
 991  	uart11: uart@88c000 {
 992  		compatible = "qcom,geni-uart";
 993  		reg = <0 0x0088c000 0 0x4000>;
 994  		clock-names = "se";
 995  		clocks = <&gcc GCC_QUPV3_WRAP2_S3_CLK>;
 996  		pinctrl-names = "default";
 997  		pinctrl-0 = <&qup_uart11_default>;
 998  		interrupts = <GIC_SPI 585 IRQ_TYPE_LEVEL_HIGH 0>;
 999  		interconnects = <&clk_virt MASTER_QUP_CORE_2 QCOM_ICC_TAG_ALWAYS
1000  						 &clk_virt SLAVE_QUP_CORE_2 QCOM_ICC_TAG_ALWAYS>,
1001  						<&gem_noc MASTER_APPSS_PROC QCOM_ICC_TAG_ACTIVE_ONLY
1002  						&config_noc SLAVE_QUP_2 QCOM_ICC_TAG_ACTIVE_ONLY>;
1003  		interconnect-names = "qup-core", "qup-config";
1004  		operating-points-v2 = <&qup_opp_table_100mhz>;
1005  		power-domains = <&rpmhpd RPMHPD_CX>;
1006  		status = "okay";
1007  	};
1008  };
1009  
1010  &remoteproc_adsp {
1011  	firmware-name = "qcom/sm8550/ayaneo/adsp.mdt",
1012  			"qcom/sm8550/ayaneo/adsp_dtb.mdt";
1013  	status = "okay";
1014  };
1015  
1016  &sdhc_2 {
1017  	cd-gpios = <&pm8550_gpios 12 GPIO_ACTIVE_LOW>;
1018  	pinctrl-names = "default", "sleep";
1019  	pinctrl-0 = <&sdc2_default &sdc2_card_det_n>;
1020  	pinctrl-1 = <&sdc2_sleep &sdc2_card_det_n>;
1021  	vmmc-supply = <&vreg_l9b_2p9>;
1022  	vqmmc-supply = <&vreg_l8b_1p8>;
1023  	max-sd-hs-hz = <37500000>;
1024  	no-sdio;
1025  	no-mmc;
1026  
1027  	qcom,dll-config = <0x0007442c>;
1028  	sdhci-caps-mask = <0x3 0x0>;
1029  
1030  	status = "okay";
1031  };
1032  
1033  &sleep_clk {
1034  	clock-frequency = <32764>;
1035  };
1036  
1037  &swr0 {
1038  	status = "okay";
1039  
1040  	spk_amp_l: speaker@0,0 {
1041  		compatible = "sdw20217020400";
1042  		reg = <0 0>;
1043  
1044  		pinctrl-0 = <&spkr_1_sd_n_active>;
1045  		pinctrl-names = "default";
1046  
1047  		powerdown-gpios = <&tlmm 7 GPIO_ACTIVE_LOW>;
1048  
1049  		vdd-1p8-supply = <&vreg_l10b_1p8>;
1050  		vdd-io-supply = <&vreg_l10b_1p8>;
1051  
1052  		#sound-dai-cells = <0>;
1053  		sound-name-prefix = "SpkrLeft";
1054  		qcom,port-mapping = <1 2 3 7 10 13>;
1055  	};
1056  
1057  	spk_amp_r: speaker@0,1 {
1058  		compatible = "sdw20217020400";
1059  		reg = <0 1>;
1060  
1061  		pinctrl-0 = <&spkr_2_sd_n_active>;
1062  		pinctrl-names = "default";
1063  
1064  		powerdown-gpios = <&tlmm 12 GPIO_ACTIVE_LOW>;
1065  
1066  		vdd-1p8-supply = <&vreg_l10b_1p8>;
1067  		vdd-io-supply = <&vreg_l10b_1p8>;
1068  
1069  		#sound-dai-cells = <0>;
1070  		sound-name-prefix = "SpkrRight";
1071  		qcom,port-mapping = <4 5 6 7 11 13>;
1072  	};
1073  };
1074  
1075  &tlmm {
1076  	gpio-reserved-ranges = <32 8>;
1077  
1078  	bt_default: bt-default-state {
1079  		bt-en-pins {
1080  			pins = "gpio81";
1081  			function = "gpio";
1082  			drive-strength = <16>;
1083  			bias-disable;
1084  		};
1085  
1086  		sw-ctrl-pins {
1087  			pins = "gpio82";
1088  			function = "gpio";
1089  			bias-pull-down;
1090  		};
1091  	};
1092  
1093  	fan_pwr_active: fan-pwr-active-state {
1094  		pins = "gpio31";
1095  		function = "gpio";
1096  		drive-strength = <2>;
1097  		bias-disable;
1098  		output-low;
1099  	};
1100  
1101  	fan_int: fan-int-state {
1102  		pins = "gpio64";
1103  		function = "gpio";
1104  		drive-strength = <2>;
1105  		bias-pull-up;
1106  		input-enable;
1107  	};
1108  
1109  	upd720201_avdd33: upd720201-avdd33-state {
1110  		pins = "gpio18";
1111  		function = "gpio";
1112  		drive-strength = <2>;
1113  		bias-disable;
1114  	};
1115  
1116  	upd720201_vdd10: pd720201-vdd10-state {
1117  		pins = "gpio13";
1118  		function = "gpio";
1119  		drive-strength = <2>;
1120  		bias-disable;
1121  	};
1122  
1123  	upd720201_vdd33: upd720201-vdd33-state {
1124  		pins = "gpio10";
1125  		function = "gpio";
1126  		drive-strength = <2>;
1127  		bias-disable;
1128  	};
1129  
1130  	gamepad_pwr_en: gamepad-pwr-en-active-state {
1131  		pins = "gpio52";
1132  		function = "gpio";
1133  		drive-strength = <2>;
1134  		bias-disable;
1135  		output-high;
1136  	};
1137  
1138  	qup_uart11_default: qup-uart11-default-state {
1139  		/* TX, RX */
1140  		pins = "gpio70", "gpio71";
1141  		function = "qup2_se3";
1142  		drive-strength = <2>;
1143  		bias-disable;
1144  	};
1145  
1146  	sde_dsi_active: sde-dsi-active-state {
1147  		pins = "gpio133";
1148  		function = "gpio";
1149  		drive-strength = <8>;
1150  		bias-disable;
1151  		output-high;
1152  	};
1153  
1154  	sde_dsi_suspend: sde-dsi-suspend-state {
1155  		pins = "gpio133";
1156  		function = "gpio";
1157  		drive-strength = <2>;
1158  		bias-pull-down;
1159  	};
1160  
1161  	sde_te_active: sde-te-active-state {
1162  		pins = "gpio86";
1163  		function = "mdp_vsync";
1164  		drive-strength = <2>;
1165  		bias-pull-down;
1166  	};
1167  
1168  	sde_te_suspend: sde-te-suspend-state {
1169  		pins = "gpio86";
1170  		function = "mdp_vsync";
1171  		drive-strength = <2>;
1172  		bias-pull-down;
1173  	};
1174  
1175  	wlan_en: wlan-en-state {
1176  		pins = "gpio80";
1177  		function = "gpio";
1178  		drive-strength = <8>;
1179  		bias-pull-down;
1180  	};
1181  
1182  	spkr_1_sd_n_active: spkr-1-sd-n-active-state {
1183  		pins = "gpio7";
1184  		function = "gpio";
1185  		drive-strength = <16>;
1186  		bias-disable;
1187  		output-high;
1188  	};
1189  
1190  	spkr_2_sd_n_active: spkr-2-sd-n-active-state {
1191  		pins = "gpio12";
1192  		function = "gpio";
1193  		drive-strength = <16>;
1194  		bias-disable;
1195  		output-high;
1196  	};
1197  };
1198  
1199  &pm8550_pwm {
1200  	status = "okay";
1201  
1202  	power_led {
1203  		color = <LED_COLOR_ID_RGB>;
1204  		label = "power-led";
1205  
1206  		#address-cells = <1>;
1207  		#size-cells = <0>;
1208  
1209  		red@1 {
1210  			reg = <1>;
1211  			color = <LED_COLOR_ID_RED>;
1212  		};
1213  
1214  		green@2 {
1215  			reg = <2>;
1216  			color = <LED_COLOR_ID_GREEN>;
1217  		};
1218  
1219  		blue@3 {
1220  			reg = <3>;
1221  			color = <LED_COLOR_ID_BLUE>;
1222  		};
1223  	};
1224  };
1225  
1226  &xo_board {
1227  	clock-frequency = <76800000>;
1228  };
1229  
1230  &gpi_dma1 {
1231  	status = "okay";
1232  };
1233  
1234  &gpi_dma2 {
1235  	status = "okay";
1236  };
1237  
1238  &gpu {
1239  	status = "okay";
1240  
1241  	zap-shader {
1242  		firmware-name = "qcom/sm8550/a740_zap.mbn";
1243  	};
1244  };
1245  
1246  &gpu_opp_table {
1247  /* Additional speedbin for Adreno A32
1248  	719000000  RPMH_REGULATOR_LEVEL_SVS_L2
1249  	746000000 RPMH_REGULATOR_LEVEL_NOM
1250  	794000000 RPMH_REGULATOR_LEVEL_NOM_L1
1251  	827000000 RPMH_REGULATOR_LEVEL_TURBO
1252  	860000000 RPMH_REGULATOR_LEVEL_TURBO_L1
1253  	1000000000 RPMH_REGULATOR_LEVEL_TURBO_L2
1254  */
1255  	opp-719000000 {
1256  		opp-hz = /bits/ 64 <719000000>;
1257  		opp-level = <RPMH_REGULATOR_LEVEL_SVS_L2>;
1258  		opp-peak-kBps = <10687500>; // Level 7
1259  		qcom,opp-acd-level = <0x882e5ffd>;
1260  	};
1261  
1262  	opp-746000000 {
1263  		opp-hz = /bits/ 64 <746000000>;
1264  		opp-level = <RPMH_REGULATOR_LEVEL_NOM>;
1265  		opp-peak-kBps = <10687500>; // Level 7
1266  		qcom,opp-acd-level = <0x882e5ffd>;
1267  	};
1268  
1269  	opp-794000000 {
1270  		opp-hz = /bits/ 64 <794000000>;
1271  		opp-level = <RPMH_REGULATOR_LEVEL_NOM_L1>;
1272  		opp-peak-kBps = <14398438>; // Level 8
1273  		qcom,opp-acd-level = <0xa82d5ffd>;
1274  	};
1275  
1276  	opp-827000000 {
1277  		opp-hz = /bits/ 64 <827000000>;
1278  		opp-level = <RPMH_REGULATOR_LEVEL_TURBO>;
1279  		opp-peak-kBps = <16500000>; // Level 9
1280  		qcom,opp-acd-level = <0xa82d5ffd>;
1281  	};
1282  
1283  	opp-860000000 {
1284  		opp-hz = /bits/ 64 <860000000>;
1285  		opp-level = <RPMH_REGULATOR_LEVEL_TURBO_L1>;
1286  		opp-peak-kBps = <16500000>; // Level 9
1287  		qcom,opp-acd-level = <0x882d5ffd>;
1288  	};
1289  
1290  	opp-1000000000 {
1291  		opp-hz = /bits/ 64 <1000000000>;
1292  		opp-level = <RPMH_REGULATOR_LEVEL_TURBO_L2>;
1293  		opp-peak-kBps = <16500000>; // Level 9
1294  		qcom,opp-acd-level = <0x882d5ffd>;
1295  	};
1296  };
1297  
1298  &i2c_master_hub_0 {
1299  	status = "okay";
1300  };
1301  
1302  &i2c_hub_2 {
1303  	status = "okay";
1304  
1305  	typec-retimer@1c {
1306  		compatible = "onnn,nb7vpq904m";
1307  		reg = <0x1c>;
1308  		vcc-supply = <&vreg_l15b_1p8>;
1309  
1310  		retimer-switch;
1311  		orientation-switch;
1312  
1313  		ports {
1314  			#address-cells = <1>;
1315  			#size-cells = <0>;
1316  
1317  			port@0 {
1318  				reg = <0>;
1319  
1320  				redriver_ss_out: endpoint {
1321  					remote-endpoint = <&pmic_glink_ss_in>;
1322  				};
1323  			};
1324  
1325  			port@1 {
1326  				reg = <1>;
1327  
1328  				redriver_ss_in: endpoint {
1329  					remote-endpoint = <&usb_dp_qmpphy_out>;
1330  				};
1331  			};
1332  		};
1333  	};
1334  };
1335  
1336  &mdss {
1337  	status = "okay";
1338  };
1339  
1340  &mdss_dsi0 {
1341  	vdda-supply = <&vreg_l3e_1p2>;
1342  	status = "okay";
1343  
1344  	display_panel: panel@0 {
1345  		reg = <0>;
1346  
1347  		pinctrl-0 = <&sde_dsi_active>, <&sde_te_active>;
1348  		pinctrl-1 = <&sde_dsi_suspend>, <&sde_te_suspend>;
1349  		pinctrl-names = "default", "sleep";
1350  	};
1351  };
1352  
1353  &mdss_dsi0_phy {
1354  	vdds-supply = <&vreg_l1e_0p88>;
1355  	status = "okay";
1356  };
1357  
1358  &mdss_dp0 {
1359  	status = "okay";
1360  };
1361  
1362  &mdss_dp0_out {
1363  	sound-name-prefix = "Display Port0";
1364  };
1365  
1366  &pcie0 {
1367  	pinctrl-0 = <&pcie0_default_state>;
1368  	pinctrl-names = "default";
1369  
1370  	status = "okay";
1371  };
1372  
1373  &pcieport0 {
1374  	wake-gpios = <&tlmm 96 GPIO_ACTIVE_HIGH>;
1375  	reset-gpios = <&tlmm 94 GPIO_ACTIVE_LOW>;
1376  
1377  	wifi@0 {
1378  		compatible = "pci17cb,1107";
1379  		reg = <0x10000 0x0 0x0 0x0 0x0>;
1380  
1381  		vddrfacmn-supply = <&vreg_pmu_rfa_cmn>;
1382  		vddaon-supply = <&vreg_pmu_aon_0p59>;
1383  		vddwlcx-supply = <&vreg_pmu_wlcx_0p8>;
1384  		vddwlmx-supply = <&vreg_pmu_wlmx_0p85>;
1385  		vddrfa0p8-supply = <&vreg_pmu_rfa_0p8>;
1386  		vddrfa1p2-supply = <&vreg_pmu_rfa_1p2>;
1387  		vddrfa1p8-supply = <&vreg_pmu_rfa_1p8>;
1388  		vddpcie0p9-supply = <&vreg_pmu_pcie_0p9>;
1389  		vddpcie1p8-supply = <&vreg_pmu_pcie_1p8>;
1390  	};
1391  };
1392  
1393  &pcie0_phy {
1394  	vdda-phy-supply = <&vreg_l1e_0p88>;
1395  	vdda-pll-supply = <&vreg_l3e_1p2>;
1396  
1397  	status = "okay";
1398  };
1399  
1400  &pcie1 {
1401  	pinctrl-0 = <&pcie1_default_state>;
1402  	pinctrl-names = "default";
1403  
1404  	status = "okay";
1405  };
1406  
1407  &pcie1_port0 {
1408  	wake-gpios = <&tlmm 99 GPIO_ACTIVE_HIGH>;
1409  	reset-gpios = <&tlmm 97 GPIO_ACTIVE_LOW>;
1410  
1411  	/* Renesas μPD720201 PCIe USB3.0 HOST CONTROLLER */
1412  	usb-controller@0 {
1413  		compatible = "pci1912,0014";
1414  		reg = <0x10000 0x0 0x0 0x0 0x0>;
1415  
1416  		avdd33-supply = <&upd720201_avdd33_reg>;
1417  		vdd10-supply = <&upd720201_vdd10_reg>;
1418  		vdd33-supply = <&upd720201_vdd33_reg>;
1419  
1420  		pinctrl-0 = <&gamepad_pwr_en>;
1421  		pinctrl-names = "default";
1422  	};
1423  };
1424  
1425  &pcie1_phy {
1426  	vdda-phy-supply = <&vreg_l3c_0p9>;
1427  	vdda-pll-supply = <&vreg_l3e_1p2>;
1428  	vdda-qref-supply = <&vreg_l1e_0p88>;
1429  
1430  	status = "okay";
1431  };
1432  
1433  &ufs_mem_hc {
1434      reset-gpios = <&tlmm 210 GPIO_ACTIVE_LOW>;
1435  
1436      vcc-supply = <&vreg_l17b_2p5>;
1437      vcc-max-microamp = <1300000>;
1438      vccq-supply = <&vreg_l1g_1p2>;
1439      vccq-max-microamp = <1200000>;
1440      vdd-hba-supply = <&vreg_l3g_1p2>;
1441  
1442      status = "okay";
1443  };
1444  
1445  &ufs_mem_phy {
1446      vdda-phy-supply = <&vreg_l1d_0p88>;
1447      vdda-pll-supply = <&vreg_l3e_1p2>;
1448  
1449      status = "okay";
1450  };
1451  
1452  &usb_1 {
1453  	status = "okay";
1454  };
1455  
1456  &usb_1_dwc3_hs {
1457  	remote-endpoint = <&pmic_glink_hs_in>;
1458  };
1459  
1460  &usb_1_hsphy {
1461  	vdd-supply = <&vreg_l1e_0p88>;
1462  	vdda12-supply = <&vreg_l3e_1p2>;
1463  
1464  	phys = <&pm8550b_eusb2_repeater>;
1465  
1466  	status = "okay";
1467  };
1468  
1469  &usb_dp_qmpphy {
1470  	vdda-phy-supply = <&vreg_l3e_1p2>;
1471  	vdda-pll-supply = <&vreg_l3f_0p88>;
1472  
1473  	status = "okay";
1474  };
1475  
1476  &usb_dp_qmpphy_out {
1477  	remote-endpoint = <&redriver_ss_in>;
1478  };
1479  
1480  &uart7 {
1481  	status = "okay";
1482  };
1483  
1484  &uart14 {
1485  	status = "okay";
1486  
1487  	bluetooth {
1488  		compatible = "qcom,wcn7850-bt";
1489  
1490  		vddrfacmn-supply = <&vreg_pmu_rfa_cmn>;
1491  		vddaon-supply = <&vreg_pmu_aon_0p59>;
1492  		vddwlcx-supply = <&vreg_pmu_wlcx_0p8>;
1493  		vddwlmx-supply = <&vreg_pmu_wlmx_0p85>;
1494  		vddrfa0p8-supply = <&vreg_pmu_rfa_0p8>;
1495  		vddrfa1p2-supply = <&vreg_pmu_rfa_1p2>;
1496  		vddrfa1p8-supply = <&vreg_pmu_rfa_1p8>;
1497  
1498  		max-speed = <3200000>;
1499  	};
1500  };
1501  
1502  &iris {
1503  	status = "okay";
1504  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketace.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2025, Teguh Sobirin.
  4   * Copyright (c) 2025, ROCKNIX (https://github.com/ROCKNIX)
  5   */
  6  
  7  /dts-v1/;
  8  
  9  #include "qcs8550-ayaneo-pocket-common.dtsi"
 10  
 11  / {
 12  	model = "AYANEO Pocket ACE";
 13  	qcom,board-id = <0x1000b 0x01>;
 14  	qcom,msm-id = <0x258 0x20000>, <0x259 0x20000>;
 15  	compatible = "ayaneo,pocketace", "qcom,qcs8550", "qcom,sm8550";
 16  	rocknix-u-boot-dt-id = "u-boot-pocket-ace";
 17  };
 18  
 19  &tlmm {
 20  	panel_pwr_active: panel-pwr-active-state {
 21  		pins = "gpio72", "gpio42", "gpio152", "gpio153";
 22  		function = "gpio";
 23  		drive-strength = <8>;
 24  		bias-disable;
 25  		output-high;
 26  	};
 27  
 28  	panel_pwr_sleep: panel-pwr-sleep-state {
 29  		pins = "gpio72", "gpio42", "gpio152", "gpio153";
 30  		function = "gpio";
 31  		output-low;
 32  	};
 33  
 34  	backlight_pwr_active: backlight-pwr-active-state {
 35  		pins = "gpio41";
 36  		function = "gpio";
 37  		drive-strength = <8>;
 38  		bias-disable;
 39  		output-high;
 40  	};
 41  
 42  	backlight_pwr_sleep: backlight-pwr-sleep-state {
 43  		pins = "gpio41";
 44  		function = "gpio";
 45  		output-low;
 46  	};
 47  
 48  	ts_int_active: ts-int-default-state {
 49  		pins = "gpio25";
 50  		function = "gpio";
 51  		bias-pull-up;
 52  		input-enable;
 53  	};
 54  };
 55  
 56  &i2c0 {
 57     clock-frequency = <400000>;
 58  	status = "okay";
 59  
 60  	/* Screen power */
 61  	regulator@3e {
 62  		compatible = "sgmicro,sgm3804";
 63  		reg = <0x3e>;
 64  		pinctrl-0 = <&panel_pwr_active>;
 65  		pinctrl-1 = <&panel_pwr_sleep>;
 66  		pinctrl-names = "default", "sleep";
 67  
 68  		vin-supply = <&vph_pwr>;
 69  
 70  		sgm3804_pos: pos {
 71  			regulator-name = "panel-avdd";
 72  			regulator-min-microvolt = <5200000>;
 73  			regulator-max-microvolt = <5200000>;
 74  			regulator-active-discharge = <1>;
 75  			regulator-boot-on;
 76  			enable-gpios = <&tlmm 152 GPIO_ACTIVE_HIGH>;
 77  		};
 78  
 79  		sgm3804_neg: neg {
 80  			regulator-name = "panel-avee";
 81  			regulator-min-microvolt = <5200000>;
 82  			regulator-max-microvolt = <5200000>;
 83  			regulator-active-discharge = <1>;
 84  			regulator-boot-on;
 85  			enable-gpios = <&tlmm 153 GPIO_ACTIVE_HIGH>;
 86  		};
 87  	};
 88  
 89  	/* Backlight */
 90  	backlight: sy7758@2e {
 91  		compatible = "silergy,sy7758";
 92  		reg = <0x2e>;
 93  		pinctrl-0 = <&backlight_pwr_active>;
 94  		pinctrl-1 = <&backlight_pwr_sleep>;
 95  		pinctrl-names = "default", "sleep";
 96  		status = "okay";
 97  	};
 98  };
 99  
100  &i2c4 {
101  	clock-frequency = <400000>;
102  	status = "okay";
103  
104  	touchscreen@70 {
105  		compatible = "synaptics,dsx";
106  		reg = <0x70>;
107  
108  		pinctrl-names = "default";
109  		pinctrl-0 = <&ts_int_active>;
110  
111  		synaptics,irq-gpio = <&tlmm 25 0x2008>;
112  		synaptics,irq-flags = <0x2008>;
113  		synaptics,power-delay-ms = <200>;
114  		synaptics,ub-i2c-addr = <0x70>;
115  
116  		vdd-supply = <&vreg_l14b_3p2>;
117  		synaptics,pwr-reg-name = "vdd";
118  		synaptics,bus-reg-name = "vio";
119  		vio-supply = <&vreg_l12b_1p8>;
120  	};
121  };
122  
123  &mdss_dsi0_out {
124  	remote-endpoint = <&panel0_in>;
125  	data-lanes = <0 1 2 3>;
126  };
127  
128  &display_panel {
129  	compatible = "ayaneo,pocket-ace-panel";
130  
131  	avdd-supply = <&sgm3804_pos>;
132  	avee-supply = <&sgm3804_neg>;
133  	vci-supply = <&vreg_l13b_3p0>;
134  	vddio-supply = <&vreg_l12b_1p8>;
135  
136  	backlight = <&backlight>;
137  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
138  
139  	rotation = <90>;
140  
141  	port {
142  		panel0_in: endpoint {
143  			remote-endpoint = <&mdss_dsi0_out>;
144  		};
145  	};
146  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketdmg.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: GPL-2.0
  2  /*
  3   * Copyright (c) 2025, ROCKNIX (https://github.com/ROCKNIX)
  4   */
  5  
  6  /dts-v1/;
  7  
  8  #include "qcs8550-ayaneo-pocket-common.dtsi"
  9  
 10  / {
 11  	model = "AYANEO Pocket DMG";
 12  	qcom,board-id = <0x1000b 0x01>;
 13  	qcom,msm-id = <0x258 0x20000>, <0x259 0x20000>;
 14  	compatible = "ayaneo,pocketdmg", "qcom,qcs8550", "qcom,sm8550";
 15  	rocknix-u-boot-dt-id = "u-boot-pocket-dmg";
 16  };
 17  
 18  &tlmm {
 19  	panel_pwr_active: panel-pwr-active-state {
 20  		pins = "gpio152", "gpio153";
 21  		function = "gpio";
 22  		drive-strength = <8>;
 23  		bias-disable;
 24  		output-high;
 25  	};
 26  
 27  	ts_int_active: ts-int-active-state {
 28  		pins = "gpio25";
 29  		function = "gpio";
 30  		drive-strength = <8>;
 31  		bias-pull-up;
 32  	};
 33  
 34  	ts_reset_active: ts-reset-active-state {
 35  		pins = "gpio24";
 36  		function = "gpio";
 37  		drive-strength = <8>;
 38  		bias-pull-up;
 39  	};
 40  
 41  	ts_int_suspend: ts-int-suspend-state {
 42  		pins = "gpio25";
 43  		function = "gpio";
 44  		drive-strength = <2>;
 45  		bias-pull-down;
 46  	};
 47  
 48  	ts_reset_suspend: ts-reset-suspend-state {
 49  		pins = "gpio24";
 50  		function = "gpio";
 51  		drive-strength = <2>;
 52  		bias-pull-down;
 53  	};
 54  };
 55  
 56  &i2c0 {
 57     clock-frequency = <400000>;
 58  	status = "okay";
 59  
 60  	/* Screen power */
 61  	regulator@3e {
 62  		compatible = "sgmicro,sgm3804";
 63  		reg = <0x3e>;
 64  		pinctrl-names = "default";
 65  		pinctrl-0 = <&panel_pwr_active>;
 66  
 67  		vin-supply = <&vph_pwr>;
 68  
 69  		sgm3804_pos: pos {
 70  			regulator-name = "panel-avdd";
 71  			regulator-min-microvolt = <5200000>;
 72  			regulator-max-microvolt = <5200000>;
 73  			regulator-active-discharge = <1>;
 74  			regulator-boot-on;
 75  			enable-gpios = <&tlmm 152 GPIO_ACTIVE_HIGH>;
 76  		};
 77  
 78  		sgm3804_neg: neg {
 79  			regulator-name = "panel-avee";
 80  			regulator-min-microvolt = <5200000>;
 81  			regulator-max-microvolt = <5200000>;
 82  			regulator-active-discharge = <1>;
 83  			regulator-boot-on;
 84  			enable-gpios = <&tlmm 153 GPIO_ACTIVE_HIGH>;
 85  		};
 86  	};
 87  };
 88  
 89  &i2c4 {
 90  	status = "okay";
 91  	clock-frequency = <400000>;
 92  
 93  	hynitron@5a {
 94  		compatible = "hyn,66xx";
 95  		reg = <0x5a>;
 96  
 97  		vdd_ana;
 98  		vdd_ana-supply = <&vreg_l14b_3p2>;
 99  
100  		interrupt-parent = <&tlmm>;
101  		interrupts = <25 0x02>;
102  		reset-gpio = <&tlmm 24 0x01>;
103  		irq-gpio = <&tlmm 25 0x02>;
104  
105  		pinctrl-names = "ts_active","ts_suspend";
106  		pinctrl-0 = <&ts_int_active &ts_reset_active>;
107  		pinctrl-1 = <&ts_int_suspend &ts_reset_suspend>;
108  
109  		max-touch-number = <5>;
110  		display-coords = <0 0 1080 1240>;
111  		pos-swap = <1>;
112  		posx-reverse = <0>;
113  		posy-reverse = <0>;
114  	};
115  };
116  
117  &mdss_dsi0_out {
118  	remote-endpoint = <&panel0_in>;
119  	data-lanes = <0 1 2 3>;
120  };
121  
122  &display_panel {
123  	compatible = "ayaneo,pocket-dmg-panel";
124  
125  	avdd-supply = <&sgm3804_pos>;
126  	avee-supply = <&sgm3804_neg>;
127  	vci-supply = <&vreg_l13b_3p0>;
128  	vddio-supply = <&vreg_l12b_1p8>;
129  
130  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
131  
132  	rotation = <270>;
133  
134  	port {
135  		panel0_in: endpoint {
136  			remote-endpoint = <&mdss_dsi0_out>;
137  		};
138  	};
139  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketds.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2025, Teguh Sobirin.
  4   * Copyright (c) 2025, ROCKNIX (https://github.com/ROCKNIX)
  5   */
  6  
  7  /dts-v1/;
  8  
  9  #include "qcs8550-ayaneo-pocket-common.dtsi"
 10  
 11  / {
 12  	model = "AYANEO Pocket DS";
 13  	qcom,board-id = <0x1000b 0x01>;
 14  	qcom,msm-id = <0x258 0x20000>, <0x259 0x20000>;
 15  	compatible = "ayaneo,pocketds", "qcom,qcs8550", "qcom,sm8550";
 16  	rocknix-u-boot-dt-id = "u-boot-pocket-ds";
 17  
 18  	tca6424_vcc: regulator-tca6424-vcc {
 19  		compatible = "regulator-fixed";
 20  		regulator-name = "tca6424_vcc";
 21  
 22  		regulator-min-microvolt = <3300000>;
 23  		regulator-max-microvolt = <3300000>;
 24  
 25  		gpio = <&tlmm 168 GPIO_ACTIVE_HIGH>;
 26  		enable-active-high;
 27          regulator-boot-on;
 28  		regulator-state-mem {
 29  			regulator-off-in-suspend;
 30  		};
 31  	};
 32  
 33  	vdd_ts: vdd-ts {
 34  		compatible = "regulator-fixed";
 35  		regulator-name = "vdd_ts_en";
 36  		regulator-min-microvolt = <3300000>;
 37  		regulator-max-microvolt = <3300000>;
 38  		gpio = <&tca6408 1 GPIO_ACTIVE_HIGH>;
 39  		enable-active-high;
 40  	};
 41  
 42  	/*
 43  	 * The lower panel's ST7703 IOVCC rail is switched by an expander
 44  	 * GPIO; the mainline panel driver models it as a plain iovcc supply,
 45  	 * so wrap the enable line in a fixed regulator. Level is the ST7703
 46  	 * IOVCC nominal and wants confirming against the board.
 47  	 */
 48  	vreg_panel1_iovcc: regulator-panel1-iovcc {
 49  		compatible = "regulator-fixed";
 50  		regulator-name = "panel1-iovcc";
 51  		regulator-min-microvolt = <1800000>;
 52  		regulator-max-microvolt = <1800000>;
 53  		gpio = <&tca6408 0 GPIO_ACTIVE_HIGH>;
 54  		enable-active-high;
 55  	};
 56  
 57  };
 58  
 59  &tlmm {
 60  	gpio-reserved-ranges = <32 4>;
 61      panel_pwr_active: panel-pwr-active-state {
 62          pins = "gpio152", "gpio153";
 63          function = "gpio";
 64          drive-strength = <8>;
 65          bias-disable;
 66          output-high;
 67      };
 68  
 69      sde_dsi1_active: sde-dsi1-active-state {
 70          pins = "gpio137";
 71          function = "gpio";
 72          drive-strength = <8>;
 73          bias-disable;
 74          output-high;
 75      };
 76  
 77      sde_dsi1_suspend: sde-dsi1-suspend-state {
 78          pins = "gpio137";
 79          function = "gpio";
 80          drive-strength = <2>;
 81          bias-pull-down;
 82      };
 83  
 84  	ts_rst_default: ts-rst-default-state {
 85  		pins = "gpio24";
 86  		function = "gpio";
 87  		bias-pull-up;
 88  		drive-strength = <8>;
 89  	};
 90  
 91  	ts_rst_sleep: ts-rst-sleep-state {
 92  		pins = "gpio24";
 93  		function = "gpio";
 94  		bias-pull-down;
 95  		drive-strength = <2>;
 96  	};
 97  
 98  	ts_int_default: ts-int-default-state {
 99  		pins = "gpio25";
100  		function = "gpio";
101  		bias-pull-up;
102  		drive-strength = <8>;
103  	};
104  
105  	ts_int_sleep: ts-int-sleep-state {
106  		pins = "gpio25";
107  		function = "gpio";
108  		bias-pull-down;
109  		drive-strength = <2>;
110  	};
111  
112  	ts2_irq: ts2-irq-state {
113  		pins = "gpio39";
114  		function = "gpio";
115  		drive-strength = <8>;
116  		bias-disable;
117  		input-enable;
118  	};
119  
120  	ts2_reset: ts2-reset-state {
121  		pins = "gpio38";
122  		function = "gpio";
123  		drive-strength = <8>;
124  		input-enable;
125  		bias-pull-down;
126  	};
127  };
128  
129  &i2c0 {
130     clock-frequency = <400000>;
131  	status = "okay";
132  
133  	/* Screen power */
134  	regulator@3e {
135  		compatible = "sgmicro,sgm3804";
136  		reg = <0x3e>;
137  		pinctrl-names = "default";
138  		pinctrl-0 = <&panel_pwr_active>;
139  
140  		vin-supply = <&vph_pwr>;
141  
142  		sgm3804_pos: pos {
143  			regulator-name = "panel-avdd";
144  			regulator-min-microvolt = <5200000>;
145  			regulator-max-microvolt = <5200000>;
146  			regulator-active-discharge = <1>;
147  			regulator-boot-on;
148  			enable-gpios = <&tlmm 152 GPIO_ACTIVE_HIGH>;
149  		};
150  
151  		sgm3804_neg: neg {
152  			regulator-name = "panel-avee";
153  			regulator-min-microvolt = <5200000>;
154  			regulator-max-microvolt = <5200000>;
155  			regulator-active-discharge = <1>;
156  			regulator-boot-on;
157  			enable-gpios = <&tlmm 153 GPIO_ACTIVE_HIGH>;
158  		};
159  	};
160  
161  	/* Backlight */
162  	backlight: backlight@2e {
163  		compatible = "silergy,sy7758";
164  		reg = <0x2e>;
165  		status = "okay";
166  	};
167  
168  	tca6408: tca64_20@20 {
169  		gpio-controller;
170  		compatible = "ti,tca6408";
171  		status = "okay";
172  		reg = <0x20>;
173  		#gpio-cells = <0x02>;
174  		vcc-supply = <&tca6424_vcc>;
175  	};
176  };
177  
178  &i2c2 {
179  	clock-frequency = <400000>;
180  	status = "okay";
181  
182  	touchscreen@5d {
183  		reg = <0x5d>;
184  		compatible = "goodix,gt911";
185  
186  		interrupt-parent = <&tlmm>;
187  		interrupts = <39 IRQ_TYPE_EDGE_FALLING>;
188  
189  		reset-gpios = <&tlmm 38 GPIO_ACTIVE_HIGH>;
190  		irq-gpios = <&tlmm 39 GPIO_ACTIVE_HIGH>;
191  		VDDIO-supply = <&vdd_ts>;
192  
193  		touchscreen-size-x = <768>;
194  		touchscreen-size-y = <1024>;
195  
196  		pinctrl-names = "default";
197  		pinctrl-0 = <&ts2_reset>, <&ts2_irq>;
198  
199  	};
200  };
201  
202  &i2c4 {
203  	clock-frequency = <400000>;
204  	status = "okay";
205  	touchscreen: touchscreen@38 {
206  		compatible = "focaltech,ft5426";
207  		reg = <0x38>;
208  		#address-cells = <1>;
209  		#size-cells = <0>;
210  
211  		interrupt-parent = <&tlmm>;
212  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
213  
214  		reset-gpios = <&tlmm 24 GPIO_ACTIVE_LOW>;
215  
216  		vcc-supply = <&vreg_l14b_3p2>;
217  		iovcc-supply = <&vreg_l12b_1p8>;
218  
219  		pinctrl-0 = <&ts_int_default &ts_rst_default>;
220  		pinctrl-1 = <&ts_int_sleep &ts_rst_sleep>;
221  		pinctrl-names = "default", "sleep";
222  
223  		touchscreen-size-x = <1080>;
224  		touchscreen-size-y = <1920>;
225  	};
226  };
227  
228  &mdss_dsi0_out {
229  	remote-endpoint = <&panel0_in>;
230  	data-lanes = <0 1 2 3>;
231  };
232  
233  &display_panel {
234  	compatible = "chipone,icna3512";
235  
236  	vci-supply = <&vreg_l13b_3p0>;
237  	vddio-supply = <&vreg_l12b_1p8>;
238  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
239  	rotation = <270>;
240  
241  	port {
242  		panel0_in: endpoint {
243  			remote-endpoint = <&mdss_dsi0_out>;
244  		};
245  	};
246  };
247  
248  &mdss_dsi1 {
249  	vdda-supply = <&vreg_l3e_1p2>;
250  	status = "okay";
251  
252  	panel@0 {
253  		compatible = "ayaneo,pocket-ds-lower-panel";
254  		reg = <0>;
255  		pinctrl-0 = <&sde_dsi1_active>;
256  		pinctrl-1 = <&sde_dsi1_suspend>;
257  		pinctrl-names = "default", "sleep";
258  		vcc-supply = <&sgm3804_pos>;
259  		avee-supply = <&sgm3804_neg>;
260  		iovcc-supply = <&vreg_panel1_iovcc>;
261  		reset-gpios = <&tca6408 2 GPIO_ACTIVE_LOW>;
262  		rotation = <270>;
263  		backlight = <&backlight>;
264  
265  		port {
266  			panel1_in: endpoint {
267  				remote-endpoint = <&mdss_dsi1_out>;
268  			};
269  		};
270  	};
271  };
272  
273  &mdss_dsi1_out {
274  	remote-endpoint = <&panel1_in>;
275  	data-lanes = <0 1 2 3>;
276  };
277  
278  &mdss_dsi1_phy {
279  	vdds-supply = <&vreg_l1e_0p88>;
280  	status = "okay";
281  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketevo.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2025, Teguh Sobirin.
  4   * Copyright (c) 2025, ROCKNIX (https://github.com/ROCKNIX)
  5   */
  6  
  7  /dts-v1/;
  8  
  9  #include "qcs8550-ayaneo-pocket-common.dtsi"
 10  
 11  / {
 12  	model = "AYANEO Pocket EVO";
 13  	qcom,board-id = <0x1000b 0x01>;
 14  	qcom,msm-id = <0x258 0x20000>, <0x259 0x20000>;
 15  	compatible = "ayaneo,pocketevo", "qcom,qcs8550", "qcom,sm8550";
 16  	rocknix-u-boot-dt-id = "u-boot-pocket-evo";
 17  };
 18  
 19  &tlmm {
 20  	panel_pwr_active: panel-pwr-active-state {
 21  		pins = "gpio152", "gpio153";
 22  		function = "gpio";
 23  		drive-strength = <8>;
 24  		bias-disable;
 25  		output-high;
 26  	};
 27  
 28  	ts_reset_active: ts-reset-active-state {
 29  		pins = "gpio24";
 30  		function = "gpio";
 31  		drive-strength = <8>;
 32  		bias-pull-up;
 33  	};
 34  
 35  	ts_reset_suspend: ts-reset-suspend-state {
 36  		pins = "gpio24";
 37  		function = "gpio";
 38  		drive-strength = <2>;
 39  		bias-pull-down;
 40  	};
 41  
 42  	ts_int_active: ts-int-default-state {
 43  		pins = "gpio25";
 44  		function = "gpio";
 45  		bias-pull-up;
 46  		drive-strength = <8>;
 47  	};
 48  
 49  	ts_int_suspend: ts-int-sleep-state {
 50  		pins = "gpio25";
 51  		function = "gpio";
 52  		bias-pull-down;
 53  		drive-strength = <2>;
 54  	};
 55  };
 56  
 57  &i2c0 {
 58  	clock-frequency = <400000>;
 59  	status = "okay";
 60  
 61  };
 62  
 63  &i2c4 {
 64  	clock-frequency = <400000>;
 65  	status = "okay";
 66  	touchscreen: touchscreen@38 {
 67  		compatible = "focaltech,ft5426";
 68  		reg = <0x38>;
 69  		#address-cells = <1>;
 70  		#size-cells = <0>;
 71  
 72  		interrupt-parent = <&tlmm>;
 73  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
 74  
 75  		reset-gpios = <&tlmm 24 GPIO_ACTIVE_LOW>;
 76  
 77  		vcc-supply = <&vreg_l14b_3p2>;
 78  		iovcc-supply = <&vreg_l12b_1p8>;
 79  
 80  		pinctrl-0 = <&ts_int_active &ts_reset_active>;
 81  		pinctrl-1 = <&ts_int_suspend &ts_reset_suspend>;
 82  		pinctrl-names = "default", "sleep";
 83  
 84  		touchscreen-size-x = <1080>;
 85  		touchscreen-size-y = <1920>;
 86  	};
 87  };
 88  
 89  &mdss_dsi0_out {
 90  	remote-endpoint = <&panel0_in>;
 91  	data-lanes = <0 1 2 3>;
 92  };
 93  
 94  &display_panel {
 95  	compatible = "chipone,icna3512";
 96  
 97  	vci-supply = <&vreg_l13b_3p0>;
 98  	vddio-supply = <&vreg_l12b_1p8>;
 99  
100  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
101  
102  	rotation = <270>;
103  
104  	port {
105  		panel0_in: endpoint {
106  			remote-endpoint = <&mdss_dsi0_out>;
107  		};
108  	};
109  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pockets1k.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2024 Linaro Limited
  4   * Copyright (c) 2025, Kancy Joe <kancy2333@outlook.com>
  5   * Copyright (c) 2025, ROCKNIX (https://github.com/ROCKNIX)
  6   *
  7   * AYANEO Pocket S 1K - 1920x1080@60Hz WT0600 video mode panel
  8   * Derived from qcs8550-ayaneo-pockets2k.dts
  9   *
 10   * GPIO layout and power sequence validated from stock Android DTB dump:
 11   *   - Panel power: SGM3804 (i2c0, 0x3e) + GPIO 72/42/152/153
 12   *   - Backlight: SY7758 (i2c0, 0x2e) + GPIO 41
 13   *   - Touch: Goodix GT911 (i2c4, 0x5d) + GPIO 24/25
 14   *   - Panel reset: GPIO 133
 15   *
 16   * Panel timing extracted from stock DT overlay fragment:
 17   *   qcom,mdss_dsi_wt0600_1080p_60hz_video
 18   */
 19  
 20  /dts-v1/;
 21  
 22  #include "qcs8550-ayaneo-pocket-common.dtsi"
 23  
 24  / {
 25  	model = "AYANEO Pocket S 1K";
 26  	compatible = "ayaneo,pocket-s1", "qcom,sm8550";
 27  	chassis-type = "handset";
 28  };
 29  
 30  &tlmm {
 31  	panel_pwr_active: panel-pwr-active-state {
 32  		pins = "gpio72", "gpio42", "gpio152", "gpio153";
 33  		function = "gpio";
 34  		drive-strength = <8>;
 35  		bias-disable;
 36  		output-high;
 37  	};
 38  
 39  	panel_pwr_sleep: panel-pwr-sleep-state {
 40  		pins = "gpio72", "gpio42", "gpio152", "gpio153";
 41  		function = "gpio";
 42  		output-low;
 43  	};
 44  
 45  	backlight_pwr_active: backlight-pwr-active-state {
 46  		pins = "gpio41";
 47  		function = "gpio";
 48  		drive-strength = <8>;
 49  		bias-disable;
 50  		output-high;
 51  	};
 52  
 53  	backlight_pwr_sleep: backlight-pwr-sleep-state {
 54  		pins = "gpio41";
 55  		function = "gpio";
 56  		output-low;
 57  	};
 58  
 59  	ts_irq: ts-irq-state {
 60  		pins = "gpio25";
 61  		function = "gpio";
 62  		drive-strength = <8>;
 63  		bias-disable;
 64  		input-enable;
 65  	};
 66  
 67  	ts_reset: ts-reset-state {
 68  		pins = "gpio24";
 69  		function = "gpio";
 70  		drive-strength = <8>;
 71  		input-enable;
 72  		bias-pull-down;
 73  	};
 74  };
 75  
 76  &i2c0 {
 77  	clock-frequency = <400000>;
 78  	status = "okay";
 79  
 80  	/* Screen power */
 81  	regulator@3e {
 82  		compatible = "sgmicro,sgm3804";
 83  		reg = <0x3e>;
 84  		pinctrl-0 = <&panel_pwr_active>;
 85  		pinctrl-1 = <&panel_pwr_sleep>;
 86  		pinctrl-names = "default", "sleep";
 87  
 88  		vin-supply = <&vph_pwr>;
 89  
 90  		sgm3804_pos: pos {
 91  			regulator-name = "panel-avdd";
 92  			regulator-min-microvolt = <5200000>;
 93  			regulator-max-microvolt = <5200000>;
 94  			regulator-active-discharge = <1>;
 95  			regulator-boot-on;
 96  			enable-gpios = <&tlmm 152 GPIO_ACTIVE_HIGH>;
 97  		};
 98  
 99  		sgm3804_neg: neg {
100  			regulator-name = "panel-avee";
101  			regulator-min-microvolt = <5200000>;
102  			regulator-max-microvolt = <5200000>;
103  			regulator-active-discharge = <1>;
104  			regulator-boot-on;
105  			enable-gpios = <&tlmm 153 GPIO_ACTIVE_HIGH>;
106  		};
107  	};
108  
109  	/* Backlight */
110  	backlight: sy7758@2e {
111  		compatible = "silergy,sy7758";
112  		reg = <0x2e>;
113  		pinctrl-0 = <&backlight_pwr_active>;
114  		pinctrl-1 = <&backlight_pwr_sleep>;
115  		pinctrl-names = "default", "sleep";
116  		status = "okay";
117  	};
118  };
119  
120  &i2c4 {
121  	status = "okay";
122  	clock-frequency = <400000>;
123  
124  	touchscreen@5d {
125  		reg = <0x5d>;
126  		status = "okay";
127  		compatible = "goodix,gt911";
128  
129  		interrupt-parent = <&tlmm>;
130  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
131  
132  		reset-gpios = <&tlmm 24 GPIO_ACTIVE_LOW>;
133  		VDDIO-supply = <&vreg_l14b_3p2>;
134  		AVDD28-supply = <&vreg_l14b_3p2>;
135  
136  		touchscreen-size-x = <1080>;
137  		touchscreen-size-y = <1920>;
138  
139  		pinctrl-names = "default";
140  		pinctrl-0 = <&ts_reset>, <&ts_irq>;
141  	};
142  };
143  
144  /*
145   * WT0600 1080p 60Hz video mode panel
146   * Single DSI, 4-lane DPHY, video mode
147   */
148  &mdss_dsi0_out {
149  	remote-endpoint = <&panel0_in>;
150  	data-lanes = <0 1 2 3>;
151  };
152  
153  &mdss_dsi0_phy {
154  	vdds-supply = <&vreg_l1e_0p88>;
155  	status = "okay";
156  };
157  
158  &display_panel {
159  	status = "okay";
160  	compatible = "ayaneo,wt0600-1080p-60hz";
161  
162  	avdd-supply = <&sgm3804_pos>;
163  	avee-supply = <&sgm3804_neg>;
164  
165  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
166  	backlight = <&backlight>;
167  	rotation = <90>;
168  
169  	port {
170  		panel0_in: endpoint {
171  			remote-endpoint = <&mdss_dsi0_out>;
172  		};
173  	};
174  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pockets2k.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2024 Linaro Limited
  4   * Copyright (c) 2025, Kancy Joe <kancy2333@outlook.com>
  5   * Copyright (c) 2025, ROCKNIX (https://github.com/ROCKNIX)
  6   */
  7  
  8  /dts-v1/;
  9  
 10  #include "qcs8550-ayaneo-pocket-common.dtsi"
 11  
 12  / {
 13  	model = "AYANEO Pocket S 2K";
 14  	compatible = "ayaneo,pocket-s1", "qcom,sm8550";
 15  	chassis-type = "handset";
 16  };
 17  
 18  &tlmm {
 19  	panel_pwr_active: panel-pwr-active-state {
 20  		pins = "gpio72", "gpio42", "gpio152", "gpio153";
 21  		function = "gpio";
 22  		drive-strength = <8>;
 23  		bias-disable;
 24  		output-high;
 25  	};
 26  
 27  	panel_pwr_sleep: panel-pwr-sleep-state {
 28  		pins = "gpio72", "gpio42", "gpio152", "gpio153";
 29  		function = "gpio";
 30  		output-low;
 31  	};
 32  
 33  	backlight_pwr_active: backlight-pwr-active-state {
 34  		pins = "gpio41";
 35  		function = "gpio";
 36  		drive-strength = <8>;
 37  		bias-disable;
 38  		output-high;
 39  	};
 40  
 41  	backlight_pwr_sleep: backlight-pwr-sleep-state {
 42  		pins = "gpio41";
 43  		function = "gpio";
 44  		output-low;
 45  	};
 46  
 47  	ts_irq: ts-irq-state {
 48  		pins = "gpio25";
 49  		function = "gpio";
 50  		drive-strength = <8>;
 51  		bias-disable;
 52  		input-enable;
 53  	};
 54  
 55  	ts_reset: ts-reset-state {
 56  		pins = "gpio24";
 57  		function = "gpio";
 58  		drive-strength = <8>;
 59  		input-enable;
 60  		bias-pull-down;
 61  	};
 62  };
 63  
 64  &i2c0 {
 65     clock-frequency = <400000>;
 66  	status = "okay";
 67  
 68  	/* Screen power */
 69  	regulator@3e {
 70  		compatible = "sgmicro,sgm3804";
 71  		reg = <0x3e>;
 72  		pinctrl-0 = <&panel_pwr_active>;
 73  		pinctrl-1 = <&panel_pwr_sleep>;
 74  		pinctrl-names = "default", "sleep";
 75  
 76  		vin-supply = <&vph_pwr>;
 77  
 78  		sgm3804_pos: pos {
 79  			regulator-name = "panel-avdd";
 80  			regulator-min-microvolt = <5200000>;
 81  			regulator-max-microvolt = <5200000>;
 82  			regulator-active-discharge = <1>;
 83  			regulator-boot-on;
 84  			enable-gpios = <&tlmm 152 GPIO_ACTIVE_HIGH>;
 85  		};
 86  
 87  		sgm3804_neg: neg {
 88  			regulator-name = "panel-avee";
 89  			regulator-min-microvolt = <5200000>;
 90  			regulator-max-microvolt = <5200000>;
 91  			regulator-active-discharge = <1>;
 92  			regulator-boot-on;
 93  			enable-gpios = <&tlmm 153 GPIO_ACTIVE_HIGH>;
 94  		};
 95  	};
 96  
 97  	/* Backlight */
 98  	backlight: sy7758@2e {
 99  		compatible = "silergy,sy7758";
100  		reg = <0x2e>;
101  		pinctrl-0 = <&backlight_pwr_active>;
102  		pinctrl-1 = <&backlight_pwr_sleep>;
103  		pinctrl-names = "default", "sleep";
104  		status = "okay";
105  	};
106  };
107  
108  &i2c4 {
109  	status = "okay";
110  	clock-frequency = <400000>;
111  
112  	touchscreen@5d {
113  		reg = <0x5d>;
114  		status = "okay";
115  		compatible = "goodix,gt911";
116  
117  		interrupt-parent = <&tlmm>;
118  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
119  
120  		reset-gpios = <&tlmm 24 GPIO_ACTIVE_LOW>;
121  		VDDIO-supply = <&vreg_l14b_3p2>;
122  		AVDD28-supply = <&vreg_l14b_3p2>;
123  
124  		touchscreen-size-x = <1440>;
125  		touchscreen-size-y = <2560>;
126  
127  		pinctrl-names = "default";
128  		pinctrl-0 = <&ts_reset>, <&ts_irq>;
129  	};
130  };
131  
132  /* wt0600 60hz 2k dual dsi dphy panel */
133  &mdss_dsi0 {
134  	qcom,master-dsi;
135  	qcom,dual-dsi-mode;
136  	qcom,sync-dual-dsi;
137  };
138  
139  &mdss_dsi0_out {
140  	remote-endpoint = <&panel0_in_0>;
141  	data-lanes = <0 1 2 3>;
142  };
143  
144  &mdss_dsi0_phy {
145  	vdds-supply = <&vreg_l1e_0p88>;
146  	status = "okay";
147  };
148  
149  &mdss_dsi1 {
150  	vdda-supply = <&vreg_l3e_1p2>;
151  	qcom,dual-dsi-mode;
152  	qcom,sync-dual-dsi;
153  	assigned-clock-parents = <&mdss_dsi0_phy DSI_BYTE_PLL_CLK>, <&mdss_dsi0_phy DSI_PIXEL_PLL_CLK>;
154  	status = "okay";
155  };
156  
157  &mdss_dsi1_out {
158  	remote-endpoint = <&panel0_in_1>;
159  	data-lanes = <0 1 2 3>;
160  };
161  
162  &mdss_dsi1_phy {
163  	vdds-supply = <&vreg_l1e_0p88>;
164  	status = "okay";
165  };
166  
167  &display_panel {
168  	status = "okay";
169  	compatible = "ayaneo,wt0600-2k";
170  
171  	avdd-supply = <&sgm3804_pos>;
172  	avee-supply = <&sgm3804_neg>;
173  
174  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
175  	backlight = <&backlight>;
176  	rotation = <90>;
177  
178  	ports {
179  		#address-cells = <1>;
180  		#size-cells = <0>;
181  
182  		port@0 {
183  			reg = <0>;
184  			panel0_in_0: endpoint {
185  				remote-endpoint = <&mdss_dsi0_out>;
186  			};
187  		};
188  
189  		port@1{
190  			reg = <1>;
191  			panel0_in_1: endpoint {
192  				remote-endpoint = <&mdss_dsi1_out>;
193  			};
194  		};
195  	};
196  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayaneo-pocketsmini.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * AYANEO Pocket S Mini hardware description.
  4   *
  5   * Panel timing, GPIO assignments and touchscreen wiring are derived from a
  6   * live stock Android device-tree dump from the target hardware.
  7   */
  8  
  9  /dts-v1/;
 10  
 11  #include "qcs8550-ayaneo-pocket-common.dtsi"
 12  
 13  / {
 14  	model = "AYANEO Pocket S Mini";
 15  	qcom,board-id = <0x1000b 0x01>;
 16  	qcom,msm-id = <0x258 0x20000>, <0x259 0x20000>;
 17  	compatible = "ayaneo,pocket-s-mini", "qcom,qcs8550", "qcom,sm8550";
 18  	chassis-type = "handset";
 19  
 20  	gpio-keys-pocket-s-mini {
 21  		compatible = "gpio-keys";
 22  		label = "gpio-keys-pocket-s-mini";
 23  		pinctrl-names = "default";
 24  		pinctrl-0 = <&pocketsmini_buttons>;
 25  
 26  		key-ayaneo {
 27  			label = "AYANEO";
 28  			gpios = <&tlmm 85 GPIO_ACTIVE_LOW>;
 29  			linux,code = <KEY_A>;
 30  			debounce-interval = <15>;
 31  			linux,can-disable;
 32  		};
 33  
 34  		key-equal {
 35  			label = "EQUAL";
 36  			gpios = <&tlmm 169 GPIO_ACTIVE_LOW>;
 37  			linux,code = <KEY_EQUAL>;
 38  			debounce-interval = <15>;
 39  			linux,can-disable;
 40  		};
 41  	};
 42  };
 43  
 44  &tlmm {
 45  	pocketsmini_buttons: pocketsmini-buttons-state {
 46  		pins = "gpio85", "gpio169";
 47  		function = "gpio";
 48  		drive-strength = <2>;
 49  		bias-pull-up;
 50  		input-enable;
 51  	};
 52  
 53  	panel_pwr_active: panel-pwr-active-state {
 54  		pins = "gpio72", "gpio42", "gpio152", "gpio153";
 55  		function = "gpio";
 56  		drive-strength = <8>;
 57  		bias-disable;
 58  		output-high;
 59  	};
 60  
 61  	panel_pwr_sleep: panel-pwr-sleep-state {
 62  		pins = "gpio72", "gpio42", "gpio152", "gpio153";
 63  		function = "gpio";
 64  		output-low;
 65  	};
 66  
 67  	backlight_pwr_active: backlight-pwr-active-state {
 68  		pins = "gpio41";
 69  		function = "gpio";
 70  		drive-strength = <8>;
 71  		bias-disable;
 72  		output-high;
 73  	};
 74  
 75  	backlight_pwr_sleep: backlight-pwr-sleep-state {
 76  		pins = "gpio41";
 77  		function = "gpio";
 78  		output-low;
 79  	};
 80  
 81  	ts_irq: ts-irq-state {
 82  		pins = "gpio25";
 83  		function = "gpio";
 84  		drive-strength = <8>;
 85  		bias-disable;
 86  		input-enable;
 87  	};
 88  
 89  	ts_reset: ts-reset-state {
 90  		pins = "gpio24";
 91  		function = "gpio";
 92  		drive-strength = <8>;
 93  		bias-pull-up;
 94  		output-high;
 95  	};
 96  };
 97  
 98  &i2c0 {
 99  	clock-frequency = <400000>;
100  	status = "okay";
101  
102  	/* Screen power */
103  	regulator@3e {
104  		compatible = "sgmicro,sgm3804";
105  		reg = <0x3e>;
106  		pinctrl-0 = <&panel_pwr_active>;
107  		pinctrl-1 = <&panel_pwr_sleep>;
108  		pinctrl-names = "default", "sleep";
109  
110  		vin-supply = <&vph_pwr>;
111  
112  		sgm3804_pos: pos {
113  			regulator-name = "panel-avdd";
114  			regulator-min-microvolt = <5200000>;
115  			regulator-max-microvolt = <5200000>;
116  			regulator-active-discharge = <1>;
117  			regulator-boot-on;
118  			enable-gpios = <&tlmm 152 GPIO_ACTIVE_HIGH>;
119  		};
120  
121  		sgm3804_neg: neg {
122  			regulator-name = "panel-avee";
123  			regulator-min-microvolt = <5200000>;
124  			regulator-max-microvolt = <5200000>;
125  			regulator-active-discharge = <1>;
126  			regulator-boot-on;
127  			enable-gpios = <&tlmm 153 GPIO_ACTIVE_HIGH>;
128  		};
129  	};
130  
131  	backlight: sy7758@2e {
132  		compatible = "silergy,sy7758";
133  		reg = <0x2e>;
134  		pinctrl-0 = <&backlight_pwr_active>;
135  		pinctrl-1 = <&backlight_pwr_sleep>;
136  		pinctrl-names = "default", "sleep";
137  		status = "okay";
138  	};
139  };
140  
141  &i2c4 {
142  	clock-frequency = <400000>;
143  	status = "okay";
144  
145  	touchscreen@5a {
146  		compatible = "hynitron,cst66xx";
147  		reg = <0x5a>;
148  
149  		interrupt-parent = <&tlmm>;
150  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
151  		reset-gpios = <&tlmm 24 GPIO_ACTIVE_LOW>;
152  		vdd-supply = <&vreg_l14b_3p2>;
153  
154  		touchscreen-size-x = <1280>;
155  		touchscreen-size-y = <960>;
156  
157  		pinctrl-names = "default";
158  		pinctrl-0 = <&ts_reset>, <&ts_irq>;
159  	};
160  };
161  
162  &pcieport0 {
163  	wifi@0 {
164  		qcom,skip-11d-scan-offload;
165  	};
166  };
167  
168  &mdss_dsi0_out {
169  	remote-endpoint = <&panel0_in>;
170  	data-lanes = <0 1 2 3>;
171  };
172  
173  &display_panel {
174  	compatible = "ayaneo,ar16-4inch-panel";
175  
176  	avdd-supply = <&sgm3804_pos>;
177  	avee-supply = <&sgm3804_neg>;
178  	vci-supply = <&vreg_l13b_3p0>;
179  	vddio-supply = <&vreg_l12b_1p8>;
180  
181  	backlight = <&backlight>;
182  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
183  	rotation = <180>;
184  
185  	port {
186  		panel0_in: endpoint {
187  			remote-endpoint = <&mdss_dsi0_out>;
188  		};
189  	};
190  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-common.dtsi @ 8ebaf8daad (whole, line-numbered, masked)

```text
   1  // SPDX-License-Identifier: BSD-3-Clause
   2  /*
   3   * Copyright (c) 2025, Teguh Sobirin.
   4   */
   5  
   6  #include <dt-bindings/leds/common.h>
   7  #include <dt-bindings/regulator/qcom,rpmh-regulator.h>
   8  #include <dt-bindings/input/qcom,hv-haptics.h>
   9  #include "qcs8550.dtsi"
  10  #include "pm8550.dtsi"
  11  #include "pm8550b.dtsi"
  12  #define PMK8550VE_SID 5
  13  #include "pm8550ve.dtsi"
  14  #include "pm8550vs.dtsi"
  15  #include "pmk8550.dtsi"
  16  
  17  /delete-node/ &aop_image_mem;
  18  /delete-node/ &aop_config_mem;
  19  /delete-node/ &camera_mem;
  20  /delete-node/ &ipa_fw_mem;
  21  /delete-node/ &ipa_gsi_mem;
  22  /delete-node/ &mpss_dsm_mem;
  23  /delete-node/ &mpss_mem;
  24  /delete-node/ &q6_mpss_dtb_mem;
  25  
  26  /delete-node/ &remoteproc_mpss;
  27  
  28  / {
  29  	chassis-type = "handset";
  30  	rocknix-u-boot-dt-id = "u-boot-odin2";
  31  
  32  	aliases {
  33  		serial0 = &uart7;
  34  		serial1 = &uart14;
  35  		serial2 = &uart15;
  36  	};
  37  
  38  	chosen {
  39  		stdout-path = "serial0:115200n8";
  40  	};
  41  
  42  	gpio-keys {
  43  		compatible = "gpio-keys";
  44  
  45  		pinctrl-0 = <&volume_up_n>;
  46  		pinctrl-names = "default";
  47  
  48  		key-volume-up {
  49  			label = "Volume Up";
  50  			debounce-interval = <15>;
  51  			gpios = <&pm8550_gpios 6 GPIO_ACTIVE_LOW>;
  52  			linux,code = <KEY_VOLUMEUP>;
  53  			linux,can-disable;
  54  			wakeup-source;
  55  		};
  56  	};
  57  
  58  	pmic-glink {
  59  		compatible = "qcom,sm8550-pmic-glink", "qcom,pmic-glink";
  60  		#address-cells = <1>;
  61  		#size-cells = <0>;
  62  		orientation-gpios = <&tlmm 11 GPIO_ACTIVE_HIGH>;
  63  
  64  		connector@0 {
  65  			compatible = "usb-c-connector";
  66  			reg = <0>;
  67  			power-role = "dual";
  68  			data-role = "dual";
  69  
  70  			ports {
  71  				#address-cells = <1>;
  72  				#size-cells = <0>;
  73  
  74  				port@0 {
  75  					reg = <0>;
  76  
  77  					pmic_glink_hs_in: endpoint {
  78  						remote-endpoint = <&usb_1_dwc3_hs>;
  79  					};
  80  				};
  81  
  82  				port@1 {
  83  					reg = <1>;
  84  
  85  					pmic_glink_ss_in: endpoint {
  86  						remote-endpoint = <&usb_dp_qmpphy_out>;
  87  					};
  88  				};
  89  
  90  				port@2 {
  91  					reg = <2>;
  92  
  93  					pmic_glink_sbu: endpoint {
  94  						remote-endpoint = <&usb0_sbu_mux>;
  95  					};
  96  				};
  97  			};
  98  		};
  99  	};
 100  
 101  	pwm_fan: pwm-fan {
 102  		compatible = "pwm-fan";
 103  
 104  		fan-supply = <&vdd_fan_5v0>;
 105  		pwms = <&pm8550_pwm 3 40000>;
 106  
 107  		pinctrl-names = "default";
 108  		pinctrl-0 = <&fan_pwm_active>, <&fan_int>;
 109  
 110  		pulses-per-revolution = <4>;
 111  		interrupt-parent = <&tlmm>;
 112  		interrupts = <13 IRQ_TYPE_EDGE_FALLING>;
 113  
 114  		cooling-levels = <0 30 45 60 70 90 120 150>;
 115  		#cooling-cells = <2>;
 116  	};
 117  
 118  	reserved-memory {
 119  		hyp_mem: hyp-region@80000000 {
 120  			reg = <0 0x80000000 0 0xa00000>;
 121  			no-map;
 122  		};
 123  
 124  		cpusys_vm_mem: cpusys-vm-region@80a00000 {
 125  			reg = <0 0x80a00000 0 0x400000>;
 126  			no-map;
 127  		};
 128  
 129  		hyp_tags_mem: hyp-tags-region@80e00000 {
 130  			reg = <0 0x80e00000 0 0x3d0000>;
 131  			no-map;
 132  		};
 133  
 134  		xbl_sc_mem: xbl-sc-region@d8100000 {
 135  			reg = <0 0xd8100000 0 0x40000>;
 136  			no-map;
 137  		};
 138  
 139  		hyp_tags_reserved_mem: hyp-tags-reserved-region@811d0000 {
 140  			reg = <0 0x811d0000 0 0x30000>;
 141  			no-map;
 142  		};
 143  
 144  		xbl_dt_log_merged_mem: xbl-dt-log-merged-region@81a00000 {
 145  			reg = <0 0x81a00000 0 0x260000>;
 146  			no-map;
 147  		};
 148  
 149  		aop_config_merged_mem: aop-config-merged-region@81c80000 {
 150  			reg = <0 0x81c80000 0 0x74000>;
 151  			no-map;
 152  		};
 153  
 154  		chipinfo_mem: chipinfo-region@81cf4000 {
 155  			reg = <0 0x81cf4000 0 0x1000>;
 156  			no-map;
 157  		};
 158  
 159  		global_sync_mem: global-sync-region@82600000 {
 160  			reg = <0 0x82600000 0 0x100000>;
 161  			no-map;
 162  		};
 163  
 164  		tz_stat_mem: tz-stat-region@82700000 {
 165  			reg = <0 0x82700000 0 0x100000>;
 166  			no-map;
 167  		};
 168  
 169  		cpucp_fw_mem: cpucp-fw-region@d8140000 {
 170  			reg = <0 0xd8140000 0 0x1c0000>;
 171  			no-map;
 172  		};
 173  
 174  		qtee_mem: qtee-region@d8300000 {
 175  			reg = <0 0xd8300000 0 0x500000>;
 176  			no-map;
 177  		};
 178  
 179  		hwfence_shbuf: hwfence-shbuf-region@e6440000 {
 180  			reg = <0 0xe6440000 0 0x2dd000>;
 181  			no-map;
 182  		};
 183  
 184  		hyp_ext_reserved_mem: hyp-ext-reserved-region@ff700000 {
 185  			reg = <0 0xff700000 0 0x100000>;
 186  			no-map;
 187  		};
 188  
 189  		llcc_lpi_mem: llcc_lpi_region@ff800000 {
 190  			reg = <0 0xff800000 0 0x600000>;
 191  			no-map;
 192  		};
 193  
 194  		hyp_ext_tags_mem: hyp-ext-tags-region@fce00000 {
 195  			reg = <0 0xfce00000 0 0x2900000>;
 196  			no-map;
 197  		};
 198  
 199  		splash_region: splash_region@b8000000 {
 200  			reg = <0x0 0xb8000000 0x0 0x2b00000>;
 201  			label = "cont_splash_region";
 202  			no-map;
 203  		};
 204  	};
 205  
 206  	thermal-zones {
 207  		cpuss0-thermal {
 208  			polling-delay = <200>;
 209  			trips {
 210  				cpuss0_fan0: trip-point2 { temperature = <50000>; hysteresis = <3000>; type = "passive"; };
 211  				cpuss0_fan1: trip-point3 { temperature = <55000>; hysteresis = <3000>; type = "passive"; };
 212  				cpuss0_fan2: trip-point4 { temperature = <60000>; hysteresis = <3000>; type = "passive"; };
 213  				cpuss0_fan3: trip-point5 { temperature = <65000>; hysteresis = <3000>; type = "passive"; };
 214  				cpuss0_fan4: trip-point6 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 215  				cpuss0_fan5: trip-point7 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 216  				cpuss0_fan6: trip-point8 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 217  			};
 218  
 219  		};
 220  		cpuss1-thermal {
 221  			polling-delay = <200>;
 222  			trips {
 223  				cpuss1_fan0: trip-point2 { temperature = <50000>; hysteresis = <3000>; type = "passive"; };
 224  				cpuss1_fan1: trip-point3 { temperature = <55000>; hysteresis = <3000>; type = "passive"; };
 225  				cpuss1_fan2: trip-point4 { temperature = <60000>; hysteresis = <3000>; type = "passive"; };
 226  				cpuss1_fan3: trip-point5 { temperature = <65000>; hysteresis = <3000>; type = "passive"; };
 227  				cpuss1_fan4: trip-point6 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 228  				cpuss1_fan5: trip-point7 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 229  				cpuss1_fan6: trip-point8 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 230  			};
 231  
 232  		};
 233  		cpuss2-thermal {
 234  			polling-delay = <200>;
 235  			trips {
 236  				cpuss2_fan0: trip-point2 { temperature = <50000>; hysteresis = <3000>; type = "passive"; };
 237  				cpuss2_fan1: trip-point3 { temperature = <55000>; hysteresis = <3000>; type = "passive"; };
 238  				cpuss2_fan2: trip-point4 { temperature = <60000>; hysteresis = <3000>; type = "passive"; };
 239  				cpuss2_fan3: trip-point5 { temperature = <65000>; hysteresis = <3000>; type = "passive"; };
 240  				cpuss2_fan4: trip-point6 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 241  				cpuss2_fan5: trip-point7 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 242  				cpuss2_fan6: trip-point8 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 243  			};
 244  
 245  		};
 246  		cpuss3-thermal {
 247  			polling-delay = <200>;
 248  			trips {
 249  				cpuss3_fan0: trip-point2 { temperature = <50000>; hysteresis = <3000>; type = "passive"; };
 250  				cpuss3_fan1: trip-point3 { temperature = <55000>; hysteresis = <3000>; type = "passive"; };
 251  				cpuss3_fan2: trip-point4 { temperature = <60000>; hysteresis = <3000>; type = "passive"; };
 252  				cpuss3_fan3: trip-point5 { temperature = <65000>; hysteresis = <3000>; type = "passive"; };
 253  				cpuss3_fan4: trip-point6 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 254  				cpuss3_fan5: trip-point7 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 255  				cpuss3_fan6: trip-point8 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 256  			};
 257  
 258  		};
 259  		cpu7-top-thermal {
 260  			polling-delay = <200>;
 261  			trips {
 262  				cpu7_top_fan0: trip-point2 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 263  				cpu7_top_fan1: trip-point3 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 264  				cpu7_top_fan2: trip-point4 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 265  			};
 266  
 267  		};
 268  		gpuss-0-thermal {
 269  			polling-delay = <200>;
 270  			trips {
 271  				gpuss0_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 272  				gpuss0_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 273  				gpuss0_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 274  			};
 275  
 276  		};
 277  		gpuss-1-thermal {
 278  			polling-delay = <200>;
 279  			trips {
 280  				gpuss1_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 281  				gpuss1_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 282  				gpuss1_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 283  			};
 284  
 285  		};
 286  		gpuss-2-thermal {
 287  			polling-delay = <200>;
 288  			trips {
 289  				gpuss2_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 290  				gpuss2_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 291  				gpuss2_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 292  			};
 293  
 294  		};
 295  		gpuss-3-thermal {
 296  			polling-delay = <200>;
 297  			trips {
 298  				gpuss3_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 299  				gpuss3_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 300  				gpuss3_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 301  			};
 302  
 303  		};
 304  		gpuss-4-thermal {
 305  			polling-delay = <200>;
 306  			trips {
 307  				gpuss4_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 308  				gpuss4_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 309  				gpuss4_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 310  			};
 311  
 312  		};
 313  		gpuss-5-thermal {
 314  			polling-delay = <200>;
 315  			trips {
 316  				gpuss5_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 317  				gpuss5_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 318  				gpuss5_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 319  			};
 320  
 321  		};
 322  		gpuss-6-thermal {
 323  			polling-delay = <200>;
 324  			trips {
 325  				gpuss6_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 326  				gpuss6_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 327  				gpuss6_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 328  			};
 329  
 330  		};
 331  		gpuss-7-thermal {
 332  			polling-delay = <200>;
 333  			trips {
 334  				gpuss7_fan0: trip-point3 { temperature = <70000>; hysteresis = <3000>; type = "passive"; };
 335  				gpuss7_fan1: trip-point4 { temperature = <75000>; hysteresis = <3000>; type = "passive"; };
 336  				gpuss7_fan2: trip-point5 { temperature = <80000>; hysteresis = <3000>; type = "passive"; };
 337  			};
 338  
 339  		};
 340  	};
 341  
 342  	sound {
 343  		compatible = "qcom,sm8550-sndcard", "qcom,sm8450-sndcard";
 344  		pinctrl-0 = <&lpi_i2s3_active>;
 345  		pinctrl-names = "default";
 346  
 347  		clocks = <&q6prmcc LPASS_CLK_ID_SEN_MI2S_IBIT LPASS_CLK_ATTRIBUTE_COUPLE_NO>;
 348  		clock-names = "i2s_clk";
 349  
 350  		assigned-clocks = <&q6prmcc LPASS_CLK_ID_SEN_MI2S_IBIT LPASS_CLK_ATTRIBUTE_COUPLE_NO>;
 351  		assigned-clock-rates = <1536000>;
 352  
 353  		model = "AYN-Odin2";
 354  		audio-routing =
 355  				"IN1_HPHL", "HPHL_OUT",
 356  				"IN2_HPHR", "HPHR_OUT",
 357  				"AMIC2", "MIC BIAS2",
 358  				"TX SWR_INPUT1", "ADC2_OUTPUT";
 359  
 360  		speaker-i2s-dai-link {
 361  			link-name = "Primary MI2S Playback";
 362  
 363  			cpu {
 364  				sound-dai = <&q6apmbedai PRIMARY_MI2S_RX>;
 365  			};
 366  
 367  			codec {
 368  				sound-dai = <&spk_amp_l 0>, <&spk_amp_r 0>;
 369  			};
 370  
 371  			platform {
 372  				sound-dai = <&q6apm>;
 373  			};
 374  		};
 375  
 376  		wcd-playback-dai-link {
 377  			link-name = "WCD Playback";
 378  
 379  			cpu {
 380  				sound-dai = <&q6apmbedai RX_CODEC_DMA_RX_0>;
 381  			};
 382  
 383  			codec {
 384  				sound-dai = <&wcd938x 0>, <&swr1 0>, <&lpass_rxmacro 0>;
 385  			};
 386  
 387  			platform {
 388  				sound-dai = <&q6apm>;
 389  			};
 390  		};
 391  
 392  		wcd-capture-dai-link {
 393  			link-name = "WCD Capture";
 394  
 395  			cpu {
 396  				sound-dai = <&q6apmbedai TX_CODEC_DMA_TX_3>;
 397  			};
 398  
 399  			codec {
 400  				sound-dai = <&wcd938x 1>, <&swr2 0>, <&lpass_txmacro 0>;
 401  			};
 402  
 403  			platform {
 404  				sound-dai = <&q6apm>;
 405  			};
 406  		};
 407  
 408  		dp0-dai-link {
 409  			link-name = "DP0 Playback";
 410  			cpu {
 411  				sound-dai = <&q6apmbedai DISPLAY_PORT_RX_0>;
 412  			};
 413  
 414  			platform {
 415  				sound-dai = <&q6apm>;
 416  			};
 417  
 418  			codec {
 419  				sound-dai = <&mdss_dp0>;
 420  			};
 421  		};
 422  	};
 423  
 424  	usb0-sbu-mux {
 425  		compatible = "gpio-sbu-mux";
 426  
 427  		enable-gpios = <&tlmm 140 GPIO_ACTIVE_LOW>;
 428  		select-gpios = <&tlmm 141 GPIO_ACTIVE_HIGH>;
 429  
 430  		pinctrl-names = "default";
 431  		pinctrl-0 = <&usb0_sbu_default>;
 432  
 433  		mode-switch;
 434  		orientation-switch;
 435  
 436  		port {
 437  			usb0_sbu_mux: endpoint {
 438  				remote-endpoint = <&pmic_glink_sbu>;
 439  			};
 440  		};
 441  	};
 442  
 443  	vdd_fan_5v0: vdd-fan-5v0-regulator {
 444  		compatible = "regulator-fixed";
 445  		regulator-name = "vdd_fan_5v0";
 446  
 447  		regulator-min-microvolt = <5000000>;
 448  		regulator-max-microvolt = <5000000>;
 449  
 450  		gpio = <&tlmm 109 GPIO_ACTIVE_HIGH>;
 451  		enable-active-high;
 452  
 453  		pinctrl-names = "default";
 454  		pinctrl-0 = <&fan_pwr_active>;
 455  
 456  		regulator-state-mem {
 457  			regulator-off-in-suspend;
 458  		};
 459  	};
 460  
 461  	vdd_mcu_3v3: vdd-mcu-3v3-regulator {
 462  		compatible = "regulator-fixed";
 463  		regulator-name = "vdd_mcu_3v3";
 464  
 465  		regulator-min-microvolt = <3300000>;
 466  		regulator-max-microvolt = <3300000>;
 467  		startup-delay-us = <10000>;
 468  
 469  		gpio = <&tlmm 99 GPIO_ACTIVE_HIGH>;
 470  		regulator-always-on;
 471  		regulator-boot-on;
 472  		enable-active-high;
 473  	};
 474  
 475  	vph_pwr: regulator-vph-pwr {
 476  		compatible = "regulator-fixed";
 477  		regulator-name = "vph_pwr";
 478  		regulator-min-microvolt = <3700000>;
 479  		regulator-max-microvolt = <3700000>;
 480  
 481  		regulator-always-on;
 482  		regulator-boot-on;
 483  	};
 484  
 485  	wcd938x: audio-codec {
 486  		compatible = "qcom,wcd9385-codec";
 487  
 488  		pinctrl-names = "default";
 489  		pinctrl-0 = <&wcd_default>;
 490  
 491  		qcom,micbias1-microvolt = <1800000>;
 492  		qcom,micbias2-microvolt = <1800000>;
 493  		qcom,micbias3-microvolt = <1800000>;
 494  		qcom,micbias4-microvolt = <1800000>;
 495  		qcom,mbhc-buttons-vthreshold-microvolt = <75000 150000 237000 500000 500000 500000 500000 500000>;
 496  		qcom,mbhc-headset-vthreshold-microvolt = <1700000>;
 497  		qcom,mbhc-headphone-vthreshold-microvolt = <50000>;
 498  		qcom,rx-device = <&wcd_rx>;
 499  		qcom,tx-device = <&wcd_tx>;
 500  
 501  		reset-gpios = <&tlmm 108 GPIO_ACTIVE_LOW>;
 502  
 503  		vdd-buck-supply = <&vreg_l15b_1p8>;
 504  		vdd-rxtx-supply = <&vreg_l15b_1p8>;
 505  		vdd-io-supply = <&vreg_l15b_1p8>;
 506  		vdd-mic-bias-supply = <&vreg_bob1>;
 507  
 508  		#sound-dai-cells = <1>;
 509  	};
 510  
 511  	wcn7850-pmu {
 512  		compatible = "qcom,wcn7850-pmu";
 513  
 514  		pinctrl-names = "default";
 515  		pinctrl-0 = <&wlan_en>, <&bt_default>, <&pmk8550_sleep_clk>;
 516  
 517  		wlan-enable-gpios = <&tlmm 80 GPIO_ACTIVE_HIGH>;
 518          bt-enable-gpios = <&tlmm 81 GPIO_ACTIVE_HIGH>;
 519  
 520  		vdd-supply = <&vreg_s5g_0p8>;
 521  		vddio-supply = <&vreg_l15b_1p8>;
 522  		vddaon-supply = <&vreg_s2g_0p8>;
 523  		vdddig-supply = <&vreg_s4e_0p95>;
 524  		vddrfa1p2-supply = <&vreg_s4g_1p3>;
 525  		vddrfa1p8-supply = <&vreg_s6g_1p8>;
 526  
 527  		regulators {
 528  			vreg_pmu_rfa_cmn: ldo0 {
 529  				regulator-name = "vreg_pmu_rfa_cmn";
 530  			};
 531  
 532  			vreg_pmu_aon_0p59: ldo1 {
 533  				regulator-name = "vreg_pmu_aon_0p59";
 534  			};
 535  
 536  			vreg_pmu_wlcx_0p8: ldo2 {
 537  				regulator-name = "vreg_pmu_wlcx_0p8";
 538  			};
 539  
 540  			vreg_pmu_wlmx_0p85: ldo3 {
 541  				regulator-name = "vreg_pmu_wlmx_0p85";
 542  			};
 543  
 544  			vreg_pmu_btcmx_0p85: ldo4 {
 545  				regulator-name = "vreg_pmu_btcmx_0p85";
 546  			};
 547  
 548  			vreg_pmu_rfa_0p8: ldo5 {
 549  				regulator-name = "vreg_pmu_rfa_0p8";
 550  			};
 551  
 552  			vreg_pmu_rfa_1p2: ldo6 {
 553  				regulator-name = "vreg_pmu_rfa_1p2";
 554  			};
 555  
 556  			vreg_pmu_rfa_1p8: ldo7 {
 557  				regulator-name = "vreg_pmu_rfa_1p8";
 558  			};
 559  
 560  			vreg_pmu_pcie_0p9: ldo8 {
 561  				regulator-name = "vreg_pmu_pcie_0p9";
 562  			};
 563  
 564  			vreg_pmu_pcie_1p8: ldo9 {
 565  				regulator-name = "vreg_pmu_pcie_1p8";
 566  			};
 567  		};
 568  	};
 569  };
 570  
 571  &apps_rsc {
 572  	regulators-0 {
 573  		compatible = "qcom,pm8550-rpmh-regulators";
 574  		qcom,pmic-id = "b";
 575  
 576  		vdd-bob1-supply = <&vph_pwr>;
 577  		vdd-bob2-supply = <&vph_pwr>;
 578  		vdd-l1-l4-l10-supply = <&vreg_s6g_1p8>;
 579  		vdd-l2-l13-l14-supply = <&vreg_bob1>;
 580  		vdd-l3-supply = <&vreg_s4g_1p3>;
 581  		vdd-l5-l16-supply = <&vreg_bob1>;
 582  		vdd-l6-l7-supply = <&vreg_bob1>;
 583  		vdd-l8-l9-supply = <&vreg_bob1>;
 584  		vdd-l11-supply = <&vreg_s4g_1p3>;
 585  		vdd-l12-supply = <&vreg_s6g_1p8>;
 586  		vdd-l15-supply = <&vreg_s6g_1p8>;
 587  		vdd-l17-supply = <&vreg_bob2>;
 588  
 589  		vreg_bob1: bob1 {
 590  			regulator-name = "vreg_bob1";
 591  			regulator-min-microvolt = <3296000>;
 592  			regulator-max-microvolt = <3960000>;
 593  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 594  		};
 595  
 596  		vreg_bob2: bob2 {
 597  			regulator-name = "vreg_bob2";
 598  			regulator-min-microvolt = <2720000>;
 599  			regulator-max-microvolt = <3960000>;
 600  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 601  		};
 602  
 603  		vreg_l2b_3p0: ldo2 {
 604  			regulator-name = "vreg_l2b_3p0";
 605  			regulator-min-microvolt = <3008000>;
 606  			regulator-max-microvolt = <3008000>;
 607  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 608  			regulator-allow-set-load;
 609  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 610  						   RPMH_REGULATOR_MODE_HPM>;
 611  		};
 612  
 613  		vreg_l5b_3p1: ldo5 {
 614  			regulator-name = "vreg_l5b_3p1";
 615  			regulator-min-microvolt = <3104000>;
 616  			regulator-max-microvolt = <3104000>;
 617  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 618  			regulator-allow-set-load;
 619  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 620  						   RPMH_REGULATOR_MODE_HPM>;
 621  		};
 622  
 623  		vreg_l6b_1p8: ldo6 {
 624  			regulator-name = "vreg_l6b_1p8";
 625  			regulator-min-microvolt = <1800000>;
 626  			regulator-max-microvolt = <3008000>;
 627  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 628  			regulator-allow-set-load;
 629  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 630  						   RPMH_REGULATOR_MODE_HPM>;
 631  		};
 632  
 633  		vreg_l7b_1p8: ldo7 {
 634  			regulator-name = "vreg_l7b_1p8";
 635  			regulator-min-microvolt = <1800000>;
 636  			regulator-max-microvolt = <3008000>;
 637  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 638  		};
 639  
 640  		vreg_l8b_1p8: ldo8 {
 641  			regulator-name = "vreg_l8b_1p8";
 642  			regulator-min-microvolt = <1800000>;
 643  			regulator-max-microvolt = <3008000>;
 644  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 645  			regulator-allow-set-load;
 646  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 647  						   RPMH_REGULATOR_MODE_HPM>;
 648  		};
 649  
 650  		vreg_l9b_2p9: ldo9 {
 651  			regulator-name = "vreg_l9b_2p9";
 652  			regulator-min-microvolt = <2960000>;
 653  			regulator-max-microvolt = <3008000>;
 654  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 655  			regulator-allow-set-load;
 656  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 657  						   RPMH_REGULATOR_MODE_HPM>;
 658  		};
 659  
 660  		vreg_l11b_1p2: ldo11 {
 661  			regulator-name = "vreg_l11b_1p2";
 662  			regulator-min-microvolt = <1200000>;
 663  			regulator-max-microvolt = <1504000>;
 664  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 665  			regulator-allow-set-load;
 666  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 667  						   RPMH_REGULATOR_MODE_HPM>;
 668  		};
 669  
 670  		vreg_l12b_1p8: ldo12 {
 671  			regulator-name = "vreg_l12b_1p8";
 672  			regulator-min-microvolt = <1800000>;
 673  			regulator-max-microvolt = <1800000>;
 674  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 675  			regulator-allow-set-load;
 676  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 677  						   RPMH_REGULATOR_MODE_HPM>;
 678  		};
 679  
 680  		vreg_l13b_3p0: ldo13 {
 681  			regulator-name = "vreg_l13b_3p0";
 682  			regulator-min-microvolt = <3000000>;
 683  			regulator-max-microvolt = <3000000>;
 684  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 685  			regulator-allow-set-load;
 686  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 687  						   RPMH_REGULATOR_MODE_HPM>;
 688  		};
 689  
 690  		vreg_l14b_3p2: ldo14 {
 691  			regulator-name = "vreg_l14b_3p2";
 692  			regulator-min-microvolt = <3200000>;
 693  			regulator-max-microvolt = <3200000>;
 694  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 695  			regulator-allow-set-load;
 696  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 697  						   RPMH_REGULATOR_MODE_HPM>;
 698  		};
 699  
 700  		vreg_l15b_1p8: ldo15 {
 701  			regulator-name = "vreg_l15b_1p8";
 702  			regulator-min-microvolt = <1800000>;
 703  			regulator-max-microvolt = <1800000>;
 704  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 705  			regulator-allow-set-load;
 706  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 707  						   RPMH_REGULATOR_MODE_HPM>;
 708  		};
 709  
 710  		vreg_l16b_2p8: ldo16 {
 711  			regulator-name = "vreg_l16b_2p8";
 712  			regulator-min-microvolt = <2800000>;
 713  			regulator-max-microvolt = <2800000>;
 714  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 715  			regulator-allow-set-load;
 716  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 717  						   RPMH_REGULATOR_MODE_HPM>;
 718  		};
 719  
 720  		vreg_l17b_2p5: ldo17 {
 721  			regulator-name = "vreg_l17b_2p5";
 722  			regulator-min-microvolt = <2504000>;
 723  			regulator-max-microvolt = <2504000>;
 724  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 725  			regulator-allow-set-load;
 726  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 727  						   RPMH_REGULATOR_MODE_HPM>;
 728  		};
 729  	};
 730  
 731  	regulators-1 {
 732  		compatible = "qcom,pm8550vs-rpmh-regulators";
 733  		qcom,pmic-id = "c";
 734  
 735  		vdd-l1-supply = <&vreg_s4g_1p3>;
 736  		vdd-l2-supply = <&vreg_s4e_0p95>;
 737  		vdd-l3-supply = <&vreg_s4e_0p95>;
 738  
 739  		vreg_l3c_0p9: ldo3 {
 740  			regulator-name = "vreg_l3c_0p9";
 741  			regulator-min-microvolt = <880000>;
 742  			regulator-max-microvolt = <912000>;
 743  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 744  			regulator-allow-set-load;
 745  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 746  						   RPMH_REGULATOR_MODE_HPM>;
 747  		};
 748  	};
 749  
 750  	regulators-2 {
 751  		compatible = "qcom,pm8550vs-rpmh-regulators";
 752  		qcom,pmic-id = "d";
 753  
 754  		vdd-l1-supply = <&vreg_s4e_0p95>;
 755  		vdd-l2-supply = <&vreg_s4e_0p95>;
 756  		vdd-l3-supply = <&vreg_s4e_0p95>;
 757  
 758  		vreg_l1d_0p88: ldo1 {
 759  			regulator-name = "vreg_l1d_0p88";
 760  			regulator-min-microvolt = <880000>;
 761  			regulator-max-microvolt = <920000>;
 762  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 763  			regulator-allow-set-load;
 764  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 765  						   RPMH_REGULATOR_MODE_HPM>;
 766  		};
 767  	};
 768  
 769  	regulators-3 {
 770  		compatible = "qcom,pm8550vs-rpmh-regulators";
 771  		qcom,pmic-id = "e";
 772  
 773  		vdd-l1-supply = <&vreg_s4e_0p95>;
 774  		vdd-l2-supply = <&vreg_s4e_0p95>;
 775  		vdd-l3-supply = <&vreg_s4g_1p3>;
 776  		vdd-s4-supply = <&vph_pwr>;
 777  		vdd-s5-supply = <&vph_pwr>;
 778  
 779  		vreg_s4e_0p95: smps4 {
 780  			regulator-name = "vreg_s4e_0p95";
 781  			regulator-min-microvolt = <904000>;
 782  			regulator-max-microvolt = <984000>;
 783  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 784  		};
 785  
 786  		vreg_s5e_1p08: smps5 {
 787  			regulator-name = "vreg_s5e_1p08";
 788  			regulator-min-microvolt = <1010000>;
 789  			regulator-max-microvolt = <1120000>;
 790  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 791  		};
 792  
 793  		vreg_l1e_0p88: ldo1 {
 794  			regulator-name = "vreg_l1e_0p88";
 795  			regulator-min-microvolt = <880000>;
 796  			regulator-max-microvolt = <912000>;
 797  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 798  			regulator-allow-set-load;
 799  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 800  						   RPMH_REGULATOR_MODE_HPM>;
 801  		};
 802  
 803  		vreg_l2e_0p9: ldo2 {
 804  			regulator-name = "vreg_l2e_0p9";
 805  			regulator-min-microvolt = <870000>;
 806  			regulator-max-microvolt = <970000>;
 807  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 808  			regulator-allow-set-load;
 809  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 810  						   RPMH_REGULATOR_MODE_HPM>;
 811  		};
 812  
 813  		vreg_l3e_1p2: ldo3 {
 814  			regulator-name = "vreg_l3e_1p2";
 815  			regulator-min-microvolt = <1200000>;
 816  			regulator-max-microvolt = <1200000>;
 817  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 818  			regulator-allow-set-load;
 819  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 820  						   RPMH_REGULATOR_MODE_HPM>;
 821  		};
 822  	};
 823  
 824  	regulators-4 {
 825  		compatible = "qcom,pm8550ve-rpmh-regulators";
 826  		qcom,pmic-id = "f";
 827  
 828  		vdd-l1-supply = <&vreg_s4e_0p95>;
 829  		vdd-l2-supply = <&vreg_s4e_0p95>;
 830  		vdd-l3-supply = <&vreg_s4e_0p95>;
 831  		vdd-s4-supply = <&vph_pwr>;
 832  
 833  		vreg_s4f_0p5: smps4 {
 834  			regulator-name = "vreg_s4f_0p5";
 835  			regulator-min-microvolt = <300000>;
 836  			regulator-max-microvolt = <700000>;
 837  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 838  		};
 839  
 840  		vreg_l1f_0p9: ldo1 {
 841  			regulator-name = "vreg_l1f_0p9";
 842  			regulator-min-microvolt = <880000>;
 843  			regulator-max-microvolt = <912000>;
 844  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 845  			regulator-allow-set-load;
 846  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 847  						   RPMH_REGULATOR_MODE_HPM>;
 848  		};
 849  
 850  		vreg_l2f_0p88: ldo2 {
 851  			regulator-name = "vreg_l2f_0p88";
 852  			regulator-min-microvolt = <880000>;
 853  			regulator-max-microvolt = <912000>;
 854  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 855  			regulator-allow-set-load;
 856  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 857  						   RPMH_REGULATOR_MODE_HPM>;
 858  		};
 859  
 860  		vreg_l3f_0p88: ldo3 {
 861  			regulator-name = "vreg_l3f_0p88";
 862  			regulator-min-microvolt = <880000>;
 863  			regulator-max-microvolt = <912000>;
 864  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 865  			regulator-allow-set-load;
 866  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 867  						   RPMH_REGULATOR_MODE_HPM>;
 868  		};
 869  	};
 870  
 871  	regulators-5 {
 872  		compatible = "qcom,pm8550vs-rpmh-regulators";
 873  		qcom,pmic-id = "g";
 874  
 875  		vdd-l1-supply = <&vreg_s4g_1p3>;
 876  		vdd-l2-supply = <&vreg_s4g_1p3>;
 877  		vdd-l3-supply = <&vreg_s4g_1p3>;
 878  		vdd-s1-supply = <&vph_pwr>;
 879  		vdd-s2-supply = <&vph_pwr>;
 880  		vdd-s3-supply = <&vph_pwr>;
 881  		vdd-s4-supply = <&vph_pwr>;
 882  		vdd-s5-supply = <&vph_pwr>;
 883  		vdd-s6-supply = <&vph_pwr>;
 884  
 885  		vreg_s1g_1p2: smps1 {
 886  			regulator-name = "vreg_s1g_1p2";
 887  			regulator-min-microvolt = <1200000>;
 888  			regulator-max-microvolt = <1300000>;
 889  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 890  		};
 891  
 892  		vreg_s2g_0p8: smps2 {
 893  			regulator-name = "vreg_s2g_0p8";
 894  			regulator-min-microvolt = <800000>;
 895  			regulator-max-microvolt = <1000000>;
 896  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 897  		};
 898  
 899  		vreg_s3g_0p7: smps3 {
 900  			regulator-name = "vreg_s3g_0p7";
 901  			regulator-min-microvolt = <300000>;
 902  			regulator-max-microvolt = <1004000>;
 903  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 904  		};
 905  
 906  		vreg_s4g_1p3: smps4 {
 907  			regulator-name = "vreg_s4g_1p3";
 908  			regulator-min-microvolt = <1200000>;
 909  			regulator-max-microvolt = <1352000>;
 910  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 911  		};
 912  
 913  		vreg_s5g_0p8: smps5 {
 914  			regulator-name = "vreg_s5g_0p8";
 915  			regulator-min-microvolt = <500000>;
 916  			regulator-max-microvolt = <1004000>;
 917  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 918  		};
 919  
 920  		vreg_s6g_1p8: smps6 {
 921  			regulator-name = "vreg_s6g_1p8";
 922  			regulator-min-microvolt = <1800000>;
 923  			regulator-max-microvolt = <2000000>;
 924  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 925  		};
 926  
 927  		vreg_l1g_1p2: ldo1 {
 928  			regulator-name = "vreg_l1g_1p2";
 929  			regulator-min-microvolt = <1200000>;
 930  			regulator-max-microvolt = <1200000>;
 931  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 932  			regulator-allow-set-load;
 933  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 934  						   RPMH_REGULATOR_MODE_HPM>;
 935  		};
 936  
 937  		vreg_l3g_1p2: ldo3 {
 938  			regulator-name = "vreg_l3g_1p2";
 939  			regulator-min-microvolt = <1200000>;
 940  			regulator-max-microvolt = <1200000>;
 941  			regulator-initial-mode = <RPMH_REGULATOR_MODE_HPM>;
 942  			regulator-allow-set-load;
 943  			regulator-allowed-modes = <RPMH_REGULATOR_MODE_LPM
 944  						   RPMH_REGULATOR_MODE_HPM>;
 945  		};
 946  	};
 947  };
 948  
 949  &gpi_dma1 {
 950  	status = "okay";
 951  };
 952  
 953  &gpi_dma2 {
 954  	status = "okay";
 955  };
 956  
 957  &gpu {
 958  	status = "okay";
 959  
 960  	zap-shader {
 961  		firmware-name = "qcom/sm8550/a740_zap.mbn";
 962  	};
 963  };
 964  
 965  &i2c0 {
 966  	clock-frequency = <400000>;
 967  	status = "okay";
 968  };
 969  
 970  &i2c4 {
 971  	clock-frequency = <400000>;
 972  	status = "okay";
 973  };
 974  
 975  &i2c12 {
 976  	clock-frequency = <400000>;
 977  	status = "okay";
 978  };
 979  
 980  &i2c_master_hub_0 {
 981  	status = "okay";
 982  };
 983  
 984  &i2c_hub_2 {
 985  	clock-frequency = <400000>;
 986  	status = "okay";
 987  
 988  	spk_amp_l: spk_amp_l@34 {
 989  		compatible = "awinic,aw88166";
 990  		reg = <0x34>;
 991  		#sound-dai-cells = <1>;
 992  		reset-gpios = <&tlmm 103 GPIO_ACTIVE_LOW>;
 993  		awinic,audio-channel = <0>;
 994  		awinic,sync-flag;
 995  		sound-name-prefix = "SPK_L";
 996  	};
 997  
 998  	spk_amp_r: spk_amp_r@35 {
 999  		compatible = "awinic,aw88166";
1000  		reg = <0x35>;
1001  		#sound-dai-cells = <1>;
1002  		reset-gpios = <&tlmm 100 GPIO_ACTIVE_LOW>;
1003  		awinic,audio-channel = <1>;
1004  		awinic,sync-flag;
1005  		sound-name-prefix = "SPK_R";
1006  	};
1007  };
1008  
1009  &iris {
1010  	status = "okay";
1011  };
1012  
1013  &lpass_tlmm {
1014  	lpi_i2s3_active: lpi_i2s3-active-state {
1015  		sck-pins {
1016  			pins = "gpio12";
1017  			function = "i2s3_clk";
1018  			drive-strength = <8>;
1019  			bias-disable;
1020  			output-high;
1021  		};
1022  
1023  		ws-pins {
1024  			pins = "gpio13";
1025  			function = "i2s3_ws";
1026  			drive-strength = <8>;
1027  			bias-disable;
1028  			output-high;
1029  		};
1030  
1031  		data0-pins {
1032  			pins = "gpio17";
1033  			function = "i2s3_data";
1034  			drive-strength = <8>;
1035  			bias-disable;
1036  			output-high;
1037  		};
1038  
1039  		data1-pins {
1040  			pins = "gpio18";
1041  			function = "i2s3_data";
1042  			drive-strength = <8>;
1043  			bias-disable;
1044  			output-high;
1045  		};
1046  	};
1047  };
1048  
1049  &lpass_vamacro {
1050  	qcom,dmic-sample-rate = <4800000>;
1051  };
1052  
1053  &lpass_wsamacro {
1054  	status = "disabled";
1055  };
1056  
1057  &mdss {
1058  	status = "okay";
1059  };
1060  
1061  &mdss_dp0 {
1062  	status = "okay";
1063  	sound-name-prefix = "Display Port0";
1064  };
1065  
1066  &mdss_dsi1 {
1067  	vdda-supply = <&vreg_l3e_1p2>;
1068  	status = "okay";
1069  
1070  	display_panel: panel@0 {
1071  		reg = <0>;
1072  
1073  		port {
1074  			panel1_in: endpoint {
1075  				remote-endpoint = <&mdss_dsi1_out>;
1076  			};
1077  		};
1078  	};
1079  };
1080  
1081  &mdss_dsi1_out {
1082  	remote-endpoint = <&panel1_in>;
1083  	data-lanes = <0 1 2 3>;
1084  };
1085  
1086  &mdss_dsi1_phy {
1087  	vdds-supply = <&vreg_l1e_0p88>;
1088  	status = "okay";
1089  };
1090  
1091  &pcie0 {
1092  	pinctrl-0 = <&pcie0_default_state>;
1093  	pinctrl-names = "default";
1094  
1095  	status = "okay";
1096  };
1097  
1098  &pcieport0 {
1099  	wake-gpios = <&tlmm 96 GPIO_ACTIVE_HIGH>;
1100  	reset-gpios = <&tlmm 94 GPIO_ACTIVE_LOW>;
1101  
1102  	wifi@0 {
1103  		compatible = "pci17cb,1107";
1104  		reg = <0x10000 0x0 0x0 0x0 0x0>;
1105  
1106  		vddrfacmn-supply = <&vreg_pmu_rfa_cmn>;
1107  		vddaon-supply = <&vreg_pmu_aon_0p59>;
1108  		vddwlcx-supply = <&vreg_pmu_wlcx_0p8>;
1109  		vddwlmx-supply = <&vreg_pmu_wlmx_0p85>;
1110  		vddrfa0p8-supply = <&vreg_pmu_rfa_0p8>;
1111  		vddrfa1p2-supply = <&vreg_pmu_rfa_1p2>;
1112  		vddrfa1p8-supply = <&vreg_pmu_rfa_1p8>;
1113  		vddpcie0p9-supply = <&vreg_pmu_pcie_0p9>;
1114  		vddpcie1p8-supply = <&vreg_pmu_pcie_1p8>;
1115  	};
1116  };
1117  
1118  &pcie0_phy {
1119  	vdda-phy-supply = <&vreg_l1e_0p88>;
1120  	vdda-pll-supply = <&vreg_l3e_1p2>;
1121  
1122  	status = "okay";
1123  };
1124  
1125  &pm8550_gpios {
1126  	fan_pwm_active: fan-pwm-active-state {
1127  		pins = "gpio8";
1128  		function = "func1";
1129  		input-disable;
1130  		output-enable;
1131  		output-low;
1132  		bias-disable;
1133  		power-source = <1>;
1134  	};
1135  
1136  	sdc2_card_det_n: sdc2-card-det-n-state {
1137  		pins = "gpio12";
1138  		function = "normal";
1139  		input-enable;
1140  		output-disable;
1141  		bias-pull-up;
1142  		power-source = <1>;
1143  	};
1144  
1145  	volume_up_n: volume-up-n-state {
1146  		pins = "gpio6";
1147  		function = "normal";
1148  		power-source = <1>;
1149  		bias-pull-up;
1150  		input-enable;
1151  	};
1152  };
1153  
1154  &pm8550_pwm {
1155  	status = "okay";
1156  
1157  	power_led {
1158  		color = <LED_COLOR_ID_RGB>;
1159  		label = "power-led";
1160  
1161  		#address-cells = <1>;
1162  		#size-cells = <0>;
1163  
1164  		red@1 {
1165  			reg = <1>;
1166  			color = <LED_COLOR_ID_RED>;
1167  		};
1168  
1169  		green@2 {
1170  			reg = <2>;
1171  			color = <LED_COLOR_ID_GREEN>;
1172  		};
1173  
1174  		blue@3 {
1175  			reg = <3>;
1176  			color = <LED_COLOR_ID_BLUE>;
1177  		};
1178  	};
1179  };
1180  
1181  &pmk8550 {
1182  	pmk8550_sdam_9d00: nvram@9d00 {
1183  		compatible = "qcom,spmi-sdam";
1184  		reg = <0x9d00>;
1185  	};
1186  };
1187  
1188  &pm8550b {
1189  	pm8550b_hv_haptics: qcom,hv-haptics@f000 {
1190  		compatible = "qcom,hv-haptics";
1191  		reg = <0xf000>, <0xf100>, <0xf200>;
1192  		interrupts = <0x07 0xf0 0x1 IRQ_TYPE_EDGE_RISING>;
1193  		interrupt-names = "fifo-empty";
1194  		qcom,vmax-mv = <5000>;
1195  		qcom,brake-mode = <BRAKE_CLOSE_LOOP>;
1196  		qcom,brake-pattern = /bits/ 8 <0xff 0x3f 0x1f>;
1197  		qcom,lra-period-us = <5880>;
1198  		qcom,drv-sig-shape = <WF_SINE>;
1199  		qcom,brake-sig-shape = <WF_SINE>;
1200  		qcom,use-erm = <0x01>;
1201  		nvmem-names = "hap_cfg_sdam";
1202  		nvmem = <&pmk8550_sdam_9d00>;
1203  		status = "ok";
1204  
1205  		hap_swr_slave_reg: qcom,hap-swr-slave-reg {
1206  			regulator-name = "hap-swr-slave-reg";
1207  		};
1208  
1209  		effect_0 {
1210  			qcom,effect-id = <0x00>;
1211  			/* qcom,wf-auto-res-disable; */
1212  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1213  			qcom,wf-pattern-data =  <0x15f 0x00 0x00>,
1214  						<0x17f 0x00 0x00>,
1215  						<0x19f 0x00 0x00>,
1216  						<0x1df 0x00 0x00>,
1217  						<0x1df 0x00 0x00>,
1218  						<0x19f 0x00 0x00>,
1219  						<0x17f 0x00 0x00>,
1220  						<0x15f 0x00 0x00>;
1221  			qcom,wf-pattern-period-us = <5880>;
1222  			qcom,wf-vmax-mv = <5000>;
1223  		};
1224  
1225  		effect_1 {
1226  			qcom,effect-id = <0x01>;
1227  			/* qcom,wf-auto-res-disable; */
1228  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1229  			qcom,wf-pattern-data =  <0x01f 0x00 0x00>,
1230  						<0x03f 0x00 0x00>,
1231  						<0x05f 0x00 0x00>,
1232  						<0x07f 0x00 0x00>,
1233  						<0x17f 0x00 0x00>,
1234  						<0x15f 0x00 0x00>,
1235  						<0x13f 0x00 0x00>,
1236  						<0x11f 0x00 0x00>;
1237  			qcom,wf-pattern-period-us = <5880>;
1238  			qcom,wf-vmax-mv = <3200>;
1239  		};
1240  
1241  		effect_2 {
1242  			qcom,effect-id = <0x02>;
1243  			/* qcom,wf-auto-res-disable; */
1244  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1245  			qcom,wf-pattern-data =  <0x01f 0x00 0x00>,
1246  						<0x03f 0x00 0x00>,
1247  						<0x05f 0x00 0x00>,
1248  						<0x07f 0x00 0x00>,
1249  						<0x17f 0x00 0x00>,
1250  						<0x15f 0x00 0x00>,
1251  						<0x13f 0x00 0x00>,
1252  						<0x11f 0x00 0x00>;
1253  			qcom,wf-pattern-period-us = <5880>;
1254  			qcom,wf-vmax-mv = <3200>;
1255  		};
1256  
1257  		effect_3 {
1258  			qcom,effect-id = <0x03>;
1259  			/* qcom,wf-auto-res-disable; */
1260  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1261  			qcom,wf-pattern-data =  <0x01f 0x00 0x00>,
1262  						<0x03f 0x00 0x00>,
1263  						<0x05f 0x00 0x00>,
1264  						<0x07f 0x00 0x00>,
1265  						<0x17f 0x00 0x00>,
1266  						<0x15f 0x00 0x00>,
1267  						<0x13f 0x00 0x00>,
1268  						<0x11f 0x00 0x00>;
1269  			qcom,wf-pattern-period-us = <5880>;
1270  			qcom,wf-vmax-mv = <3200>;
1271  		};
1272  
1273  		effect_4 {
1274  			qcom,effect-id = <0x04>;
1275  			/* qcom,wf-auto-res-disable; */
1276  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1277  			qcom,wf-pattern-data =  <0x01f 0x00 0x00>,
1278  						<0x03f 0x00 0x00>,
1279  						<0x05f 0x00 0x00>,
1280  						<0x07f 0x00 0x00>,
1281  						<0x17f 0x00 0x00>,
1282  						<0x15f 0x00 0x00>,
1283  						<0x13f 0x00 0x00>,
1284  						<0x11f 0x00 0x00>;
1285  			qcom,wf-pattern-period-us = <5880>;
1286  			qcom,wf-vmax-mv = <3200>;
1287  		};
1288  
1289  		effect_5 {
1290  			qcom,effect-id = <0x05>;
1291  			/* qcom,wf-auto-res-disable; */
1292  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1293  			qcom,wf-pattern-data =  <0x11f 0x00 0x00>,
1294  						<0x13f 0x00 0x00>,
1295  						<0x15f 0x00 0x00>,
1296  						<0x17f 0x00 0x00>,
1297  						<0x17f 0x00 0x00>,
1298  						<0x15f 0x00 0x00>,
1299  						<0x13f 0x00 0x00>,
1300  						<0x11f 0x00 0x00>;
1301  			qcom,wf-pattern-period-us = <5880>;
1302  			qcom,wf-vmax-mv = <5000>;
1303  		};
1304  
1305  		primitive_0 {
1306  			qcom,primitive-id = <0x00>;
1307  			qcom,wf-auto-res-disable;
1308  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1309  			qcom,wf-pattern-data = <0x00 0x00 0x00 0x00 0x00 0x00>;
1310  			qcom,wf-pattern-period-us = <5880>;
1311  			qcom,wf-vmax-mv = <2400>;
1312  		};
1313  
1314  		primitive_1 {
1315  			qcom,primitive-id = <0x01>;
1316  			qcom,wf-auto-res-disable;
1317  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1318  			qcom,wf-pattern-data = <0xff 0x00 0x00 0x7f 0x00 0x00>;
1319  			qcom,wf-pattern-period-us = <5880>;
1320  			qcom,wf-vmax-mv = <2400>;
1321  		};
1322  
1323  		primitive_2 {
1324  			qcom,primitive-id = <0x02>;
1325  			qcom,wf-auto-res-disable;
1326  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1327  			qcom,wf-pattern-data = <0xff 0x00 0x00 0x7f 0x00 0x00>;
1328  			qcom,wf-pattern-period-us = <5880>;
1329  			qcom,wf-vmax-mv = <2400>;
1330  		};
1331  
1332  		primitive_3 {
1333  			qcom,primitive-id = <0x03>;
1334  			qcom,wf-auto-res-disable;
1335  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1336  			qcom,wf-pattern-data = <0xff 0x00 0x00 0x7f 0x00 0x00>;
1337  			qcom,wf-pattern-period-us = <5880>;
1338  			qcom,wf-vmax-mv = <2400>;
1339  		};
1340  
1341  		primitive_4 {
1342  			qcom,primitive-id = <0x04>;
1343  			qcom,wf-auto-res-disable;
1344  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1345  			qcom,wf-pattern-data = <0xff 0x00 0x00 0x7f 0x00 0x00>;
1346  			qcom,wf-pattern-period-us = <5880>;
1347  			qcom,wf-vmax-mv = <2400>;
1348  		};
1349  
1350  		primitive_5 {
1351  			qcom,primitive-id = <0x05>;
1352  			qcom,wf-auto-res-disable;
1353  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1354  			qcom,wf-pattern-data = <0xff 0x00 0x00 0x7f 0x00 0x00>;
1355  			qcom,wf-pattern-period-us = <5880>;
1356  			qcom,wf-vmax-mv = <2400>;
1357  		};
1358  
1359  		primitive_6 {
1360  			qcom,primitive-id = <0x06>;
1361  			qcom,wf-auto-res-disable;
1362  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1363  			qcom,wf-pattern-data = <0xff 0x00 0x00 0x7f 0x00 0x00>;
1364  			qcom,wf-pattern-period-us = <5880>;
1365  			qcom,wf-vmax-mv = <2400>;
1366  		};
1367  
1368  		primitive_7 {
1369  			qcom,primitive-id = <0x07>;
1370  			qcom,wf-auto-res-disable;
1371  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1372  			qcom,wf-pattern-data = <0xff 0x00 0x00 0x7f 0x00 0x00>;
1373  			qcom,wf-pattern-period-us = <5880>;
1374  			qcom,wf-vmax-mv = <2400>;
1375  		};
1376  
1377  		primitive_8 {
1378  			qcom,primitive-id = <0x08>;
1379  			qcom,wf-auto-res-disable;
1380  			qcom,wf-brake-pattern = /bits/ 8 <0x0 0x0 0x0>;
1381  			qcom,wf-pattern-data = <0xff 0x00 0x00 0x7f 0x00 0x00>;
1382  			qcom,wf-pattern-period-us = <5880>;
1383  			qcom,wf-vmax-mv = <2400>;
1384  		};
1385  	};
1386  };
1387  
1388  &pm8550b_eusb2_repeater {
1389  	qcom,tune-usb2-disc-thres = /bits/ 8 <0x6>;
1390  	qcom,tune-usb2-amplitude = /bits/ 8 <0xb>;
1391  	qcom,tune-usb2-preem = /bits/ 8 <0x3>;
1392  	vdd18-supply = <&vreg_l15b_1p8>;
1393  	vdd3-supply = <&vreg_l5b_3p1>;
1394  };
1395  
1396  &pmk8550_gpios {
1397  	pmk8550_sleep_clk: sleep-clk-state {
1398  		pins = "gpio3";
1399  		function = "func1";
1400  		input-disable;
1401  		output-enable;
1402  		bias-disable;
1403  		power-source = <0>;
1404  	};
1405  
1406  	pwm_backlight_default: pwm-backlight-default-state {
1407  		pins = "gpio5";
1408  		function = "func3";
1409  		input-disable;
1410  		output-low;
1411  		output-enable;
1412  		bias-disable;
1413  		power-source = <0>;
1414  		qcom,drive-strength = <2>;
1415  	};
1416  };
1417  
1418  &pmk8550_rtc {
1419  	nvmem-cells = <&rtc_offset>;
1420  	nvmem-cell-names = "offset";
1421  };
1422  
1423  &pmk8550_sdam_2 {
1424  	rtc_offset: rtc-offset@bc {
1425  		reg = <0xbc 0x4>;
1426  	};
1427  };
1428  
1429  &pon_pwrkey {
1430  	status = "okay";
1431  };
1432  
1433  &pon_resin {
1434  	linux,code = <KEY_VOLUMEDOWN>;
1435  
1436  	status = "okay";
1437  };
1438  
1439  &qupv3_id_0 {
1440  	status = "okay";
1441  };
1442  
1443  &qupv3_id_1 {
1444  	status = "okay";
1445  };
1446  
1447  &remoteproc_cdsp {
1448  	firmware-name = "qcom/sm8550/ayn/cdsp.mbn",
1449  			"qcom/sm8550/ayn/cdsp_dtb.mbn";
1450  	status = "okay";
1451  };
1452  
1453  &sdhc_2 {
1454  	cd-gpios = <&pm8550_gpios 12 GPIO_ACTIVE_LOW>;
1455  	pinctrl-names = "default", "sleep";
1456  	pinctrl-0 = <&sdc2_default &sdc2_card_det_n>;
1457  	pinctrl-1 = <&sdc2_sleep &sdc2_card_det_n>;
1458  	vmmc-supply = <&vreg_l9b_2p9>;
1459  	vqmmc-supply = <&vreg_l8b_1p8>;
1460  	max-sd-hs-hz = <37500000>;
1461  	no-sdio;
1462  	no-mmc;
1463  
1464  	qcom,dll-config = <0x0007442c>;
1465  	sdhci-caps-mask = <0x3 0x0>;
1466  
1467  	status = "okay";
1468  };
1469  
1470  &sleep_clk {
1471  	clock-frequency = <32764>;
1472  };
1473  
1474  &swr1 {
1475  	status = "okay";
1476  	wcd_rx: codec@0,4 {
1477  		compatible = "sdw20217010d00";
1478  		reg = <0 4>;
1479  		qcom,rx-port-mapping = <1 2 3 4 5>;
1480  	};
1481  };
1482  
1483  &swr2 {
1484  	status = "okay";
1485  	wcd_tx: codec@0,3 {
1486  		compatible = "sdw20217010d00";
1487  		reg = <0 3>;
1488  		qcom,tx-port-mapping = <2 2 3 4>;
1489  	};
1490  };
1491  
1492  &tlmm {
1493  	gpio-reserved-ranges = <32 8>;
1494  
1495  	dsi_p_rst_active: dsi-p-rst-active-state {
1496  		pins = "gpio133";
1497  		function = "gpio";
1498  		drive-strength = <8>;
1499  		bias-disable;
1500  	};
1501  
1502  	dsi_p_rst_suspend: dsi-p-rst-suspend-state {
1503  		pins = "gpio133";
1504  		function = "gpio";
1505  		drive-strength = <2>;
1506  		bias-pull-down;
1507  	};
1508  
1509  	dsi_p_te_active: dsi-p-te-active-state {
1510  		pins = "gpio86";
1511  		function = "mdp_vsync";
1512  		drive-strength = <2>;
1513  		bias-pull-down;
1514  	};
1515  
1516  	dsi_p_te_suspend: dsi-s-te-suspend-state {
1517  		pins = "gpio86";
1518  		function = "mdp_vsync";
1519  		drive-strength = <2>;
1520  		bias-pull-down;
1521  	};
1522  
1523  	dsi_s_rst_active: dsi-s-rst-active-state {
1524  		pins = "gpio137";
1525  		function = "gpio";
1526  		drive-strength = <8>;
1527  		bias-disable;
1528  	};
1529  
1530  	dsi_s_rst_suspend: dsi-s-rst-suspend-state {
1531  		pins = "gpio137";
1532  		function = "gpio";
1533  		drive-strength = <2>;
1534  		bias-pull-down;
1535  	};
1536  
1537  	dsi_s_te_active: dsi-s-te-active-state {
1538  		pins = "gpio87";
1539  		function = "mdp_vsync";
1540  		drive-strength = <2>;
1541  		bias-pull-down;
1542  	};
1543  
1544  	dsi_s_te_suspend: dsi-s-te-suspend-state {
1545  		pins = "gpio87";
1546  		function = "mdp_vsync";
1547  		drive-strength = <2>;
1548  		bias-pull-down;
1549  	};
1550  
1551  	bt_default: bt-default-state {
1552  		bt-en-pins {
1553  			pins = "gpio81";
1554  			function = "gpio";
1555  			drive-strength = <16>;
1556  			bias-disable;
1557  		};
1558  
1559  		sw-ctrl-pins {
1560  			pins = "gpio82";
1561  			function = "gpio";
1562  			bias-pull-down;
1563  		};
1564  	};
1565  
1566  	fan_pwr_active: fan-pwr-active-state {
1567  		pins = "gpio109";
1568  		function = "gpio";
1569  		drive-strength = <2>;
1570  		bias-disable;
1571  		output-low;
1572  	};
1573  
1574  	fan_int: fan-int-state {
1575  		pins = "gpio13";
1576  		function = "gpio";
1577  		drive-strength = <2>;
1578  		bias-disable;
1579  	};
1580  
1581  	mcu_en_active: mcu-en-active-state {
1582  		pins = "gpio12";
1583  		function = "gpio";
1584  		bias-pull-down;
1585  	};
1586  
1587  	ts_p_rst_default: ts-p-rst-default-state {
1588  		pins = "gpio24";
1589  		function = "gpio";
1590  		bias-pull-up;
1591  		drive-strength = <8>;
1592  	};
1593  
1594  	ts_p_rst_sleep: ts-p-rst-sleep-state {
1595  		pins = "gpio24";
1596  		function = "gpio";
1597  		bias-pull-down;
1598  		drive-strength = <2>;
1599  	};
1600  
1601  	ts_p_int_default: ts-p-int-default-state {
1602  		pins = "gpio25";
1603  		function = "gpio";
1604  		bias-pull-up;
1605  		drive-strength = <8>;
1606  	};
1607  
1608  	ts_p_int_sleep: ts-p-int-sleep-state {
1609  		pins = "gpio25";
1610  		function = "gpio";
1611  		bias-pull-down;
1612  		drive-strength = <2>;
1613  	};
1614  
1615  	ts_s_rst_default: ts-s-rst-default-state {
1616  		pins = "gpio14";
1617  		function = "gpio";
1618  		bias-pull-up;
1619  		drive-strength = <8>;
1620  	};
1621  
1622  	ts_s_rst_sleep: ts-s-rst-sleep-state {
1623  		pins = "gpio14";
1624  		function = "gpio";
1625  		bias-pull-down;
1626  		drive-strength = <2>;
1627  	};
1628  
1629  	ts_s_int_default: ts-s-int-default-state {
1630  		pins = "gpio15";
1631  		function = "gpio";
1632  		bias-pull-up;
1633  		drive-strength = <8>;
1634  	};
1635  
1636  	ts_s_int_sleep: ts-s-int-sleep-state {
1637  		pins = "gpio15";
1638  		function = "gpio";
1639  		bias-pull-down;
1640  		drive-strength = <2>;
1641  	};
1642  
1643  	usb0_sbu_default: usb0-sbu-state {
1644  		oe-n-pins {
1645  			pins = "gpio140";
1646  			function = "gpio";
1647  			bias-disable;
1648  			drive-strength = <16>;
1649  			output-high;
1650  		};
1651  
1652  		sel-pins {
1653  			pins = "gpio141";
1654  			function = "gpio";
1655  			bias-disable;
1656  			drive-strength = <16>;
1657  		};
1658  	};
1659  
1660  	wcd_default: wcd-reset-n-active-state {
1661  		pins = "gpio108";
1662  		function = "gpio";
1663  		drive-strength = <16>;
1664  		bias-disable;
1665  		output-low;
1666  	};
1667  
1668  	wlan_en: wlan-en-state {
1669  		pins = "gpio80";
1670  		function = "gpio";
1671  		drive-strength = <8>;
1672  		bias-pull-down;
1673  	};
1674  };
1675  
1676  &uart7 {
1677  	status = "okay";
1678  };
1679  
1680  &uart14 {
1681  	status = "okay";
1682  
1683  	bluetooth {
1684  		compatible = "qcom,wcn7850-bt";
1685  
1686  		vddrfacmn-supply = <&vreg_pmu_rfa_cmn>;
1687  		vddaon-supply = <&vreg_pmu_aon_0p59>;
1688  		vddwlcx-supply = <&vreg_pmu_wlcx_0p8>;
1689  		vddwlmx-supply = <&vreg_pmu_wlmx_0p85>;
1690  		vddrfa0p8-supply = <&vreg_pmu_rfa_0p8>;
1691  		vddrfa1p2-supply = <&vreg_pmu_rfa_1p2>;
1692  		vddrfa1p8-supply = <&vreg_pmu_rfa_1p8>;
1693  
1694  		max-speed = <3200000>;
1695  	};
1696  };
1697  
1698  &uart15 {
1699  	status = "okay";
1700  
1701  	gamepad: gamepad {
1702  		compatible = "gamepad,rsinput";
1703  
1704  		gamepad-name = "AYN Odin2 Gamepad";
1705  		gamepad-bus = <0x0003>;
1706  		gamepad-vid = <0x2020>;
1707  		gamepad-pid = <0x3001>;
1708  		gamepad-rev = <0x0001>;
1709  
1710  		vdd-supply = <&vreg_bob2>;
1711  		enable-gpios = <&tlmm 12 GPIO_ACTIVE_HIGH>;
1712  		pinctrl-0 = <&mcu_en_active>;
1713  		pinctrl-names = "default";
1714  	};
1715  };
1716  
1717  &ufs_mem_hc {
1718  	reset-gpios = <&tlmm 210 GPIO_ACTIVE_LOW>;
1719  	vcc-supply = <&vreg_l17b_2p5>;
1720  	vcc-max-microamp = <1300000>;
1721  	vccq-supply = <&vreg_l1g_1p2>;
1722  	vccq-max-microamp = <1200000>;
1723  	vdd-hba-supply = <&vreg_l3g_1p2>;
1724  
1725  	status = "okay";
1726  };
1727  
1728  &ufs_mem_phy {
1729  	vdda-phy-supply = <&vreg_l1d_0p88>;
1730  	vdda-pll-supply = <&vreg_l3e_1p2>;
1731  
1732  	status = "okay";
1733  };
1734  
1735  &usb_1 {
1736  	status = "okay";
1737  };
1738  
1739  &usb_1_dwc3_hs {
1740  	remote-endpoint = <&pmic_glink_hs_in>;
1741  };
1742  
1743  &usb_1_hsphy {
1744  	phys = <&pm8550b_eusb2_repeater>;
1745  
1746  	vdd-supply = <&vreg_l1e_0p88>;
1747  	vdda12-supply = <&vreg_l3e_1p2>;
1748  
1749  	status = "okay";
1750  };
1751  
1752  &usb_dp_qmpphy {
1753  	vdda-phy-supply = <&vreg_l3e_1p2>;
1754  	vdda-pll-supply = <&vreg_l3f_0p88>;
1755  
1756  	mode-switch;
1757  
1758  	status = "okay";
1759  };
1760  
1761  &usb_dp_qmpphy_out {
1762  	remote-endpoint = <&pmic_glink_ss_in>;
1763  };
1764  
1765  &xo_board {
1766  	clock-frequency = <76800000>;
1767  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-odin2.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2025, Teguh Sobirin.
  4   */
  5  
  6  /dts-v1/;
  7  
  8  #include "qcs8550-ayn-common.dtsi"
  9  
 10  / {
 11  	model = "AYN Odin 2";
 12  	compatible = "ayn,odin2", "qcom,qcs8550", "qcom,sm8550";
 13  	qcom,msm-id = <603 0x20000>;
 14  	qcom,board-id = <0x1001f 0>;
 15  
 16  	backlight: backlight {
 17  		compatible = "pwm-backlight";
 18  		pwms = <&pmk8550_pwm 0 860000>;
 19  		brightness-levels = <1023 0>;
 20  		num-interpolated-steps = <1023>;
 21  		default-brightness-level = <600>;
 22  		power-supply = <&vph_pwr>;
 23  		enable-gpios = <&pmk8550_gpios 5 GPIO_ACTIVE_HIGH>;
 24  		pinctrl-names = "default";
 25  		pinctrl-0 = <&pwm_backlight_default>;
 26  		status = "okay";
 27  	};
 28  
 29  	hdmi-out {
 30  		compatible = "hdmi-connector";
 31  		type = "d";
 32  		hpd-gpios = <&tlmm 9 GPIO_ACTIVE_HIGH>;
 33  		hdmi-pwr-supply = <&vdd_hdmi_1v8>;
 34  
 35  		port {
 36  			hdmi_con: endpoint {
 37  				remote-endpoint = <&lt8912_out>;
 38  			};
 39  		};
 40  	};
 41  
 42  	led_left_side: led-controller-1 {
 43  		compatible = "pwm-leds-multicolor";
 44  
 45  		multi-led {
 46  			label = "left-side";
 47  			color = <LED_COLOR_ID_RGB>;
 48  			max-brightness = <255>;
 49  
 50  			led-red {
 51  				color = <LED_COLOR_ID_RED>;
 52  				pwms = <&pwm_rgb_left 0>;
 53  			};
 54  
 55  			led-green {
 56  				color = <LED_COLOR_ID_GREEN>;
 57  				pwms = <&pwm_rgb_left 1>;
 58  			};
 59  
 60  			led-blue {
 61  				color = <LED_COLOR_ID_BLUE>;
 62  				pwms = <&pwm_rgb_left 2>;
 63  			};
 64  		};
 65  	};
 66  
 67  	led_left_joystick: led-controller-2 {
 68  		compatible = "pwm-leds-multicolor";
 69  
 70  		multi-led {
 71  			label = "left-joystick";
 72  			color = <LED_COLOR_ID_RGB>;
 73  			max-brightness = <255>;
 74  
 75  			led-red {
 76  				color = <LED_COLOR_ID_RED>;
 77  				pwms = <&pwm_rgb_left 6>;
 78  			};
 79  
 80  			led-green {
 81  				color = <LED_COLOR_ID_GREEN>;
 82  				pwms = <&pwm_rgb_left 7>;
 83  			};
 84  
 85  			led-blue {
 86  				color = <LED_COLOR_ID_BLUE>;
 87  				pwms = <&pwm_rgb_left 8>;
 88  			};
 89  		};
 90  	};
 91  
 92  	led_right_side: led-controller-3 {
 93  		compatible = "pwm-leds-multicolor";
 94  
 95  		multi-led {
 96  			label = "right-side";
 97  			color = <LED_COLOR_ID_RGB>;
 98  			max-brightness = <255>;
 99  
100  			led-red {
101  				color = <LED_COLOR_ID_RED>;
102  				pwms = <&pwm_rgb_right 0>;
103  			};
104  
105  			led-green {
106  				color = <LED_COLOR_ID_GREEN>;
107  				pwms = <&pwm_rgb_right 1>;
108  			};
109  
110  			led-blue {
111  				color = <LED_COLOR_ID_BLUE>;
112  				pwms = <&pwm_rgb_right 2>;
113  			};
114  		};
115  	};
116  
117  	led_right_joystick: led-controller-4 {
118  		compatible = "pwm-leds-multicolor";
119  
120  		multi-led {
121  			label = "right-joystick";
122  			color = <LED_COLOR_ID_RGB>;
123  			max-brightness = <255>;
124  
125  			led-red {
126  				color = <LED_COLOR_ID_RED>;
127  				pwms = <&pwm_rgb_right 6>;
128  			};
129  
130  			led-green {
131  				color = <LED_COLOR_ID_GREEN>;
132  				pwms = <&pwm_rgb_right 7>;
133  			};
134  
135  			led-blue {
136  				color = <LED_COLOR_ID_BLUE>;
137  				pwms = <&pwm_rgb_right 8>;
138  			};
139  		};
140  	};
141  
142  	vcc_hdmi_1v8: vcc-hdmi-1v8-regulator {
143  		compatible = "regulator-fixed";
144  		regulator-name = "vcc_hdmi_1v8";
145  
146  		regulator-min-microvolt = <1800000>;
147  		regulator-max-microvolt = <1800000>;
148  
149  		gpio = <&tlmm 10 GPIO_ACTIVE_HIGH>;
150  		enable-active-high;
151  	};
152  
153  	vdd_disp_2v8: vdd-disp-2v8-regulator {
154  		compatible = "regulator-fixed";
155  		regulator-name = "vdd_disp_2v8";
156  
157  		regulator-min-microvolt = <2800000>;
158  		regulator-max-microvolt = <2800000>;
159  
160  		gpio = <&tlmm 142 GPIO_ACTIVE_HIGH>;
161  		enable-active-high;
162  	};
163  
164  	vdd_hdmi_1v8: vdd-hdmi-1v8-regulator {
165  		compatible = "regulator-fixed";
166  		regulator-name = "vdd_hdmi_1v8";
167  
168  		regulator-min-microvolt = <1800000>;
169  		regulator-max-microvolt = <1800000>;
170  
171  		gpio = <&tlmm 6 GPIO_ACTIVE_HIGH>;
172  		enable-active-high;
173  	};
174  };
175  
176  &display_panel {
177  	compatible = "syna,td4328";
178  
179  	pinctrl-0 = <&dsi_p_rst_active>, <&dsi_p_te_active>;
180  	pinctrl-1 = <&dsi_p_rst_suspend>, <&dsi_p_te_suspend>;
181  	pinctrl-names = "default", "sleep";
182  
183  	vdd-supply = <&vdd_disp_2v8>;
184  	vddio-supply = <&vreg_l12b_1p8>;
185  
186  	backlight = <&backlight>;
187  
188  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
189  
190  	rotation = <90>;
191  };
192  
193  &i2c0 {
194  	pwm_rgb_left: sn3112@54 {
195  		compatible = "si-en,sn3112-pwm";
196  		reg = <0x54>;
197  		sdb-gpios = <&tlmm 55 GPIO_ACTIVE_LOW>;
198  		vdd-supply = <&vdd_mcu_3v3>;
199  		#pwm-cells = <1>;
200  	};
201  };
202  
203  &i2c4 {
204  	touchscreen@20 {
205  		compatible = "syna,rmi4-i2c";
206  		reg = <0x20>;
207  		#address-cells = <1>;
208  		#size-cells = <0>;
209  		interrupt-parent = <&tlmm>;
210  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
211  
212  		pinctrl-names = "default", "sleep";
213  		pinctrl-0 = <&ts_p_int_default>;
214  		pinctrl-1 = <&ts_p_int_sleep>;
215  
216  		vio-supply = <&vreg_l12b_1p8>;
217  
218  		syna,startup-delay-ms = <200>;
219  		syna,reset-delay-ms = <200>;
220  
221  		rmi4-f01@1 {
222  			syna,nosleep-mode = <0x1>;
223  			reg = <0x1>;
224  		};
225  
226  		rmi4-f12@12 {
227  			reg = <0x12>;
228  			syna,rezero-wait-ms = <20>;
229  			syna,clip-x-low = <0>;
230  			syna,clip-y-low = <0>;
231  			syna,clip-x-high = <1080>;
232  			syna,clip-y-high = <1920>;
233  			syna,sensor-type = <1>;
234  			touchscreen-inverted-x;
235  		};
236  	};
237  };
238  
239  &i2c12 {
240  	pwm_rgb_right: sn3112@54 {
241  		compatible = "si-en,sn3112-pwm";
242  		reg = <0x54>;
243  		sdb-gpios = <&tlmm 56 GPIO_ACTIVE_LOW>;
244  		vdd-supply = <&vdd_mcu_3v3>;
245  		#pwm-cells = <1>;
246  	};
247  };
248  
249  &i2c_hub_0 {
250  	clock-frequency = <100000>;
251  	status = "okay";
252  
253  	lt8912_codec: hdmi-bridge@48 {
254  		compatible = "lontium,lt8912b";
255  		reg = <0x48> ;
256  
257  		reset-gpios = <&tlmm 7 GPIO_ACTIVE_LOW>;
258  
259  		vdd-supply = <&vdd_hdmi_1v8>;
260  		vccmipirx-supply = <&vcc_hdmi_1v8>;
261  		vccsysclk-supply = <&vcc_hdmi_1v8>;
262  		vcclvdstx-supply = <&vcc_hdmi_1v8>;
263  		vcchdmitx-supply = <&vcc_hdmi_1v8>;
264  		vcclvdspll-supply = <&vcc_hdmi_1v8>;
265  		vcchdmipll-supply = <&vcc_hdmi_1v8>;
266  
267  		ports {
268  			#address-cells = <1>;
269  			#size-cells = <0>;
270  
271  			port@0 {
272  				reg = <0>;
273  
274  				hdmi_out_in: endpoint {
275  					data-lanes = <1 2 3 4>;
276  					remote-endpoint = <&mdss_dsi0_out>;
277  				};
278  			};
279  
280  			port@1 {
281  				reg = <1>;
282  
283  				lt8912_out: endpoint {
284  					remote-endpoint = <&hdmi_con>;
285  				};
286  			};
287  		};
288  	};
289  };
290  
291  &mdss_dsi0 {
292  	vdda-supply = <&vreg_l3e_1p2>;
293  	status = "okay";
294  };
295  
296  &mdss_dsi0_out {
297  	remote-endpoint = <&hdmi_out_in>;
298  	data-lanes = <0 1 2 3>;
299  };
300  
301  &mdss_dsi0_phy {
302  	vdds-supply = <&vreg_l1e_0p88>;
303  	status = "okay";
304  };
305  
306  &pmk8550_pwm {
307  	status = "okay";
308  };
309  
310  &remoteproc_adsp {
311  	firmware-name = "qcom/sm8550/ayn/odin2/adsp.mbn",
312  			"qcom/sm8550/ayn/odin2/adsp_dtb.mbn";
313  	status = "okay";
314  };
315  
316  &spk_amp_l {
317  	firmware-name = "qcom/sm8550/ayn/odin2/aw883xx_acf.bin";
318  };
319  
320  &spk_amp_r {
321  	firmware-name = "qcom/sm8550/ayn/odin2/aw883xx_acf.bin";
322  };
323  
324  &tlmm {
325  	paddle_keys_default: paddle-keys-default-state {
326  		pins = "gpio57", "gpio58";
327  		function = "gpio";
328  		bias-pull-up;
329  		drive-strength = <2>;
330  	};
331  };
332  
333  /*
334   * AYN Odin 2 has two extra back buttons (M1, M2) on the lower back of
335   * the device. They are plain active-low SoC TLMM GPIOs (M1 = GPIO_57,
336   * M2 = GPIO_58), not on the gamepad MCU UART and not ADC (despite AYN's
337   * Android "adckey"/keydetect.ko naming). Expose them as a gpio-keys
338   * device emitting BTN_Z (M1) / BTN_C (M2); ROCKNIX's InputPlumber map
339   * (ayn_mcu.yaml) routes BTN_Z -> LeftPaddle2 and BTN_C -> RightPaddle2.
340   * RE'd from the AYN Android keydetect driver (gpio_request 358/359 =
341   * TLMM base 301 + offsets 57/58), same scheme as the AYN Odin 3.
342   */
343  / {
344  	gpio-keys-paddles {
345  		compatible = "gpio-keys";
346  		pinctrl-names = "default";
347  		pinctrl-0 = <&paddle_keys_default>;
348  
349  		key-paddle-m1 {
350  			label = "Back Paddle M1";
351  			linux,code = <BTN_Z>;
352  			gpios = <&tlmm 57 GPIO_ACTIVE_LOW>;
353  			debounce-interval = <15>;
354  		};
355  
356  		key-paddle-m2 {
357  			label = "Back Paddle M2";
358  			linux,code = <BTN_C>;
359  			gpios = <&tlmm 58 GPIO_ACTIVE_LOW>;
360  			debounce-interval = <15>;
361  		};
362  	};
363  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-odin2mini.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2025, Teguh Sobirin.
  4   */
  5  
  6  /dts-v1/;
  7  
  8  #include "qcs8550-ayn-common.dtsi"
  9  
 10  / {
 11  	model = "AYN Odin 2 Mini";
 12  	compatible = "ayn,odin2mini", "qcom,qcs8550", "qcom,sm8550";
 13  	qcom,msm-id = <603 0x20000>;
 14  	qcom,board-id = <0x1001f 0>;
 15  
 16  	hdmi-out {
 17  		compatible = "hdmi-connector";
 18  		type = "d";
 19  		hpd-gpios = <&tlmm 9 GPIO_ACTIVE_HIGH>;
 20  		hdmi-pwr-supply = <&vdd_hdmi_1v8>;
 21  
 22  		port {
 23  			hdmi_con: endpoint {
 24  				remote-endpoint = <&lt8912_out>;
 25  			};
 26  		};
 27  	};
 28  
 29  	vcc_hdmi_1v8: vcc-hdmi-1v8-regulator {
 30  		compatible = "regulator-fixed";
 31  		regulator-name = "vcc_hdmi_1v8";
 32  
 33  		regulator-min-microvolt = <1800000>;
 34  		regulator-max-microvolt = <1800000>;
 35  
 36  		gpio = <&tlmm 10 GPIO_ACTIVE_HIGH>;
 37  		enable-active-high;
 38  	};
 39  
 40  	vdd_bl_5v0: vdd-bl-5v0-regulator {
 41  		compatible = "regulator-fixed";
 42  		regulator-name = "vdd_bl_5v0";
 43  
 44  		regulator-min-microvolt = <5000000>;
 45  		regulator-max-microvolt = <5000000>;
 46  
 47  		gpio = <&tlmm 55 GPIO_ACTIVE_HIGH>;
 48  		enable-active-high;
 49  	};
 50  
 51  	vdd_disp_2v8: vdd-disp-2v8-regulator {
 52  		compatible = "regulator-fixed";
 53  		regulator-name = "vdd_disp_2v8";
 54  
 55  		regulator-min-microvolt = <2800000>;
 56  		regulator-max-microvolt = <2800000>;
 57  
 58  		gpio = <&tlmm 142 GPIO_ACTIVE_HIGH>;
 59  		enable-active-high;
 60  	};
 61  
 62  	vdd_hdmi_1v8: vdd-hdmi-1v8-regulator {
 63  		compatible = "regulator-fixed";
 64  		regulator-name = "vdd_hdmi_1v8";
 65  
 66  		regulator-min-microvolt = <1800000>;
 67  		regulator-max-microvolt = <1800000>;
 68  
 69  		gpio = <&tlmm 6 GPIO_ACTIVE_HIGH>;
 70  		enable-active-high;
 71  	};
 72  };
 73  
 74  &display_panel {
 75  	compatible = "boe,xm91080g";
 76  
 77  	pinctrl-0 = <&dsi_p_rst_active>, <&dsi_p_te_active>;
 78  	pinctrl-1 = <&dsi_p_rst_suspend>, <&dsi_p_te_suspend>;
 79  	pinctrl-names = "default", "sleep";
 80  
 81  	vdd-supply = <&vreg_l11b_1p2>;
 82  	vddio-supply = <&vreg_l12b_1p8>;
 83  	vci-supply = <&vreg_l13b_3p0>;
 84  	disp-supply = <&vdd_disp_2v8>;
 85  	blvdd-supply = <&vdd_bl_5v0>;
 86  
 87  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
 88  
 89  	rotation = <90>;
 90  };
 91  
 92  &i2c0 {
 93  	backlight: backlight@46 {
 94  		compatible = "ayn,odin2miniled";
 95  		reg = <0x46>;
 96  		enable-gpios = <&tlmm 55 GPIO_ACTIVE_HIGH>;
 97  		vcc_1v2-supply = <&vreg_l11b_1p2>;
 98  		vcc_3v3-supply = <&vreg_bob2>;
 99  	};
100  };
101  
102  &i2c4 {
103  	touchscreen@1a {
104  		compatible = "hynitron,cst340";
105  		reg = <0x1a>;
106  		interrupt-parent = <&tlmm>;
107  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
108  		reset-gpios = <&tlmm 24 GPIO_ACTIVE_LOW>;
109  		vdd-supply = <&vreg_l2b_3p0>;
110  
111  		pinctrl-0 = <&ts_p_rst_default &ts_p_int_default>;
112  		pinctrl-1 = <&ts_p_rst_sleep &ts_p_int_sleep>;
113  		pinctrl-names = "default", "sleep";
114  
115  		touchscreen-size-x = <1920>;
116  		touchscreen-size-y = <1080>;
117  		touchscreen-swapped-x-y;
118  		touchscreen-inverted-y;
119  	};
120  };
121  
122  &i2c_hub_0 {
123  	clock-frequency = <100000>;
124  	status = "okay";
125  
126  	lt8912_codec: hdmi-bridge@48 {
127  		compatible = "lontium,lt8912b";
128  		reg = <0x48> ;
129  
130  		reset-gpios = <&tlmm 7 GPIO_ACTIVE_LOW>;
131  
132  		vdd-supply = <&vdd_hdmi_1v8>;
133  		vccmipirx-supply = <&vcc_hdmi_1v8>;
134  		vccsysclk-supply = <&vcc_hdmi_1v8>;
135  		vcclvdstx-supply = <&vcc_hdmi_1v8>;
136  		vcchdmitx-supply = <&vcc_hdmi_1v8>;
137  		vcclvdspll-supply = <&vcc_hdmi_1v8>;
138  		vcchdmipll-supply = <&vcc_hdmi_1v8>;
139  
140  		ports {
141  			#address-cells = <1>;
142  			#size-cells = <0>;
143  
144  			port@0 {
145  				reg = <0>;
146  
147  				hdmi_out_in: endpoint {
148  					data-lanes = <1 2 3 4>;
149  					remote-endpoint = <&mdss_dsi0_out>;
150  				};
151  			};
152  
153  			port@1 {
154  				reg = <1>;
155  
156  				lt8912_out: endpoint {
157  					remote-endpoint = <&hdmi_con>;
158  				};
159  			};
160  		};
161  	};
162  };
163  
164  &mdss_dsi0 {
165  	vdda-supply = <&vreg_l3e_1p2>;
166  	status = "okay";
167  };
168  
169  &mdss_dsi0_out {
170  	remote-endpoint = <&hdmi_out_in>;
171  	data-lanes = <0 1 2 3>;
172  };
173  
174  &mdss_dsi0_phy {
175  	vdds-supply = <&vreg_l1e_0p88>;
176  	status = "okay";
177  };
178  
179  &remoteproc_adsp {
180  	firmware-name = "qcom/sm8550/ayn/odin2mini/adsp.mbn",
181  			"qcom/sm8550/ayn/odin2mini/adsp_dtb.mbn";
182  	status = "okay";
183  };
184  
185  &spk_amp_l {
186  	firmware-name = "qcom/sm8550/ayn/odin2mini/aw883xx_acf.bin";
187  };
188  
189  &spk_amp_r {
190  	firmware-name = "qcom/sm8550/ayn/odin2mini/aw883xx_acf.bin";
191  };
192  
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-odin2portal.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2025, Teguh Sobirin.
  4   */
  5  
  6  /dts-v1/;
  7  
  8  #include "qcs8550-ayn-common.dtsi"
  9  
 10  / {
 11  	model = "AYN Odin 2 Portal";
 12  	compatible = "ayn,odin2portal", "qcom,qcs8550", "qcom,sm8550";
 13  	qcom,msm-id = <603 0x20000>;
 14  	qcom,board-id = <0x1001f 0>;
 15  
 16  	vdd_bl_5v0: vdd-bl-5v0-regulator {
 17  		compatible = "regulator-fixed";
 18  		regulator-name = "vdd_bl_5v0";
 19  
 20  		regulator-min-microvolt = <5000000>;
 21  		regulator-max-microvolt = <5000000>;
 22  
 23  		gpio = <&tlmm 52 GPIO_ACTIVE_HIGH>;
 24  		enable-active-high;
 25  	};
 26  
 27  	vdd_disp_2v8: vdd-disp-2v8-regulator {
 28  		compatible = "regulator-fixed";
 29  		regulator-name = "vdd_disp_2v8";
 30  
 31  		regulator-min-microvolt = <2800000>;
 32  		regulator-max-microvolt = <2800000>;
 33  
 34  		gpio = <&tlmm 142 GPIO_ACTIVE_HIGH>;
 35  		enable-active-high;
 36  	};
 37  
 38  	multi-ledr1 {
 39  		compatible = "leds-group-multicolor";
 40  		color = <LED_COLOR_ID_RGB>;
 41  		function = "r1";
 42  		leds = <&ledr_r4>, <&ledr_g4>, <&ledr_b4>;
 43  	};
 44  
 45  	multi-ledl1 {
 46  		compatible = "leds-group-multicolor";
 47  		color = <LED_COLOR_ID_RGB>;
 48  		function = "l1";
 49  		leds = <&ledl_r4>, <&ledl_g4>, <&ledl_b4>;
 50  	};
 51  
 52  	multi-ledr2 {
 53  		compatible = "leds-group-multicolor";
 54  		color = <LED_COLOR_ID_RGB>;
 55  		function = "r2";
 56  		leds = <&ledr_r1>, <&ledr_g1>, <&ledr_b1>;
 57  	};
 58  
 59  	multi-ledl2 {
 60  		compatible = "leds-group-multicolor";
 61  		color = <LED_COLOR_ID_RGB>;
 62  		function = "l2";
 63  		leds = <&ledl_r1>, <&ledl_g1>, <&ledl_b1>;
 64  	};
 65  
 66  	multi-ledr3 {
 67  		compatible = "leds-group-multicolor";
 68  		color = <LED_COLOR_ID_RGB>;
 69  		function = "r3";
 70  		leds = <&ledr_r2>, <&ledr_g2>, <&ledr_b2>;
 71  	};
 72  
 73  	multi-ledl3 {
 74  		compatible = "leds-group-multicolor";
 75  		color = <LED_COLOR_ID_RGB>;
 76  		function = "l3";
 77  		leds = <&ledl_r2>, <&ledl_g2>, <&ledl_b2>;
 78  	};
 79  
 80  	multi-ledr4 {
 81  		compatible = "leds-group-multicolor";
 82  		color = <LED_COLOR_ID_RGB>;
 83  		function = "r4";
 84  		leds = <&ledr_r3>, <&ledr_g3>, <&ledr_b3>;
 85  	};
 86  
 87  	multi-ledl4 {
 88  		compatible = "leds-group-multicolor";
 89  		color = <LED_COLOR_ID_RGB>;
 90  		function = "l4";
 91  		leds = <&ledl_r3>, <&ledl_g3>, <&ledl_b3>;
 92  	};
 93  };
 94  
 95  &display_panel {
 96  	compatible = "chipone,icna3512";
 97  
 98  	pinctrl-0 = <&dsi_p_rst_active>, <&dsi_p_te_active>;
 99  	pinctrl-1 = <&dsi_p_rst_suspend>, <&dsi_p_te_suspend>;
100  	pinctrl-names = "default", "sleep";
101  
102  	vdd-supply = <&vreg_l11b_1p2>;
103  	vddio-supply = <&vreg_l12b_1p8>;
104  	vci-supply = <&vreg_l13b_3p0>;
105  	disp-supply = <&vdd_disp_2v8>;
106  	blvdd-supply = <&vdd_bl_5v0>;
107  
108  	reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
109  
110  	rotation = <270>;
111  };
112  
113  &i2c0 {
114  	htr3212l: led-controller@3c {
115  		compatible = "heroic,htr3212";
116  		reg = <0x3c>;
117  		#address-cells = <1>;
118  		#size-cells = <0>;
119  		sdb-gpios = <&tlmm 55 GPIO_ACTIVE_HIGH>;
120  		vdd-supply = <&vdd_mcu_3v3>;
121  
122  		ledl_b1: led@1 {
123  			reg = <1>;
124  			label = "l:r1";
125  			color = <LED_COLOR_ID_RED>;
126  		};
127  		ledl_g1: led@2 {
128  			reg = <2>;
129  			label = "l:g1";
130  			color = <LED_COLOR_ID_GREEN>;
131  		};
132  		ledl_r1: led@3 {
133  			reg = <3>;
134  			label = "l:b1";
135  			color = <LED_COLOR_ID_BLUE>;
136  		};
137  		ledl_b2: led@4 {
138  			reg = <4>;
139  			label = "l:r2";
140  			color = <LED_COLOR_ID_RED>;
141  		};
142  		ledl_g2: led@5 {
143  			reg = <5>;
144  			label = "l:g2";
145  			color = <LED_COLOR_ID_GREEN>;
146  		};
147  		ledl_r2: led@6 {
148  			reg = <6>;
149  			label = "l:b2";
150  			color = <LED_COLOR_ID_BLUE>;
151  		};
152  		ledl_b3: led@7 {
153  			reg = <7>;
154  			label = "l:r3";
155  			color = <LED_COLOR_ID_RED>;
156  		};
157  		ledl_g3: led@8 {
158  			reg = <8>;
159  			label = "l:g3";
160  			color = <LED_COLOR_ID_GREEN>;
161  		};
162  		ledl_r3: led@9 {
163  			reg = <9>;
164  			label = "l:b3";
165  			color = <LED_COLOR_ID_BLUE>;
166  		};
167  		ledl_b4: led@10 {
168  			reg = <10>;
169  			label = "l:r4";
170  			color = <LED_COLOR_ID_RED>;
171  		};
172  		ledl_g4: led@11 {
173  			reg = <11>;
174  			label = "l:g4";
175  			color = <LED_COLOR_ID_GREEN>;
176  		};
177  		ledl_r4: led@12 {
178  			reg = <12>;
179  			label = "l:b4";
180  			color = <LED_COLOR_ID_BLUE>;
181  		};
182  	};
183  };
184  
185  &i2c4 {
186  	touchscreen@38 {
187  		compatible = "focaltech,ft5426";
188  		reg = <0x38>;
189  		#address-cells = <1>;
190  		#size-cells = <0>;
191  
192  		interrupt-parent = <&tlmm>;
193  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
194  
195  		reset-gpios = <&tlmm 24 GPIO_ACTIVE_LOW>;
196  
197  		vcc-supply = <&vreg_l14b_3p2>;
198  		iovcc-supply = <&vreg_l12b_1p8>;
199  
200  		pinctrl-0 = <&ts_p_rst_default &ts_p_int_default>;
201  		pinctrl-1 = <&ts_p_rst_sleep &ts_p_int_sleep>;
202  		pinctrl-names = "default", "sleep";
203  
204  		touchscreen-size-x = <1080>;
205  		touchscreen-size-y = <1920>;
206  	};
207  };
208  
209  &i2c12 {
210  	htr3212r: led-controller@3c {
211  		compatible = "heroic,htr3212";
212  		reg = <0x3c>;
213  		#address-cells = <1>;
214  		#size-cells = <0>;
215  		sdb-gpios = <&tlmm 56 GPIO_ACTIVE_HIGH>;
216  		vdd-supply = <&vdd_mcu_3v3>;
217  
218  		ledr_b1: led@1 {
219  			reg = <1>;
220  			label = "r:r1";
221  			color = <LED_COLOR_ID_RED>;
222  		};
223  		ledr_g1: led@2 {
224  			reg = <2>;
225  			label = "r:g1";
226  			color = <LED_COLOR_ID_GREEN>;
227  		};
228  		ledr_r1: led@3 {
229  			reg = <3>;
230  			label = "r:b1";
231  			color = <LED_COLOR_ID_BLUE>;
232  		};
233  		ledr_b2: led@4 {
234  			reg = <4>;
235  			label = "r:r2";
236  			color = <LED_COLOR_ID_RED>;
237  		};
238  		ledr_g2: led@5 {
239  			reg = <5>;
240  			label = "r:g2";
241  			color = <LED_COLOR_ID_GREEN>;
242  		};
243  		ledr_r2: led@6 {
244  			reg = <6>;
245  			label = "r:b2";
246   			color = <LED_COLOR_ID_BLUE>;
247  		};
248  		ledr_b3: led@7 {
249  			reg = <7>;
250  			label = "r:r3";
251  			color = <LED_COLOR_ID_RED>;
252  		};
253  		ledr_g3: led@8 {
254  			reg = <8>;
255  			label = "r:g3";
256  			color = <LED_COLOR_ID_GREEN>;
257  		};
258  		ledr_r3: led@9 {
259  			reg = <9>;
260  			label = "r:b3";
261  			color = <LED_COLOR_ID_BLUE>;
262  		};
263  		ledr_b4: led@10 {
264  			reg = <10>;
265  			label = "r:r4";
266  			color = <LED_COLOR_ID_RED>;
267  		};
268  		ledr_g4: led@11 {
269  			reg = <11>;
270  			label = "r:g4";
271  			color = <LED_COLOR_ID_GREEN>;
272  		};
273  		ledr_r4: led@12 {
274  			reg = <12>;
275  			label = "r:b4";
276  			color = <LED_COLOR_ID_BLUE>;
277  		};
278  	};
279  };
280  
281  &remoteproc_adsp {
282  	firmware-name = "qcom/sm8550/ayn/odin2portal/adsp.mbn",
283  			"qcom/sm8550/ayn/odin2portal/adsp_dtb.mbn";
284  	status = "okay";
285  };
286  
287  &spk_amp_l {
288  	firmware-name = "qcom/sm8550/ayn/odin2portal/aw883xx_acf.bin";
289  };
290  
291  &spk_amp_r {
292  	firmware-name = "qcom/sm8550/ayn/odin2portal/aw883xx_acf.bin";
293  };
294  
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-ayn-thor.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (c) 2025, Teguh Sobirin.
  4   */
  5  
  6  /dts-v1/;
  7  
  8  #include "qcs8550-ayn-common.dtsi"
  9  
 10  / {
 11  	model = "AYN Thor";
 12  	compatible = "ayn,thor", "qcom,qcs8550", "qcom,sm8550";
 13  	qcom,msm-id = <603 0x20000>;
 14  	qcom,board-id = <0x1001f 0>;
 15  
 16  	gpio-keys-ayn {
 17  		compatible = "gpio-keys";
 18  
 19  		pinctrl-0 = <&key_ayn_n>;
 20  		pinctrl-names = "default";
 21  
 22  		key-ayn {
 23  			label = "AYN Key";
 24  			debounce-interval = <15>;
 25  			gpios = <&tlmm 41 GPIO_ACTIVE_LOW>;
 26  			linux,code = <KEY_F24>;
 27  			linux,can-disable;
 28  		};
 29  	};
 30  
 31  	gpio-keys-lid {
 32  		compatible = "gpio-keys";
 33  
 34  		hall-lid-sensor {
 35  			label = "Hall Lid Sensor";
 36  			gpios = <&tlmm 17 GPIO_ACTIVE_LOW>;
 37  			linux,input-type = <EV_SW>;
 38  			linux,code = <SW_LID>;
 39  			linux,can-disable;
 40  			wakeup-source;
 41  		};
 42  	};
 43  
 44  	vdd_bl_5v0: vdd-bl-5v0-regulator {
 45  		compatible = "regulator-fixed";
 46  		regulator-name = "vdd_bl_5v0";
 47  
 48  		regulator-min-microvolt = <5000000>;
 49  		regulator-max-microvolt = <5000000>;
 50  
 51  		gpio = <&tlmm 52 GPIO_ACTIVE_HIGH>;
 52  		enable-active-high;
 53  	};
 54  
 55  	vdd_disp_1v8: vdd-disp-1v8-regulator {
 56  		compatible = "regulator-fixed";
 57  		regulator-name = "vdd_disp_1v8";
 58  
 59  		regulator-min-microvolt = <1800000>;
 60  		regulator-max-microvolt = <1800000>;
 61  
 62  		gpio = <&tlmm 70 GPIO_ACTIVE_HIGH>;
 63  		enable-active-high;
 64  	};
 65  
 66  	vdd_disp1_2v8: vdd-disp1-2v8-regulator {
 67  		compatible = "regulator-fixed";
 68  		regulator-name = "vdd_disp1_2v8";
 69  
 70  		regulator-min-microvolt = <2800000>;
 71  		regulator-max-microvolt = <2800000>;
 72  
 73  		gpio = <&tlmm 142 GPIO_ACTIVE_HIGH>;
 74  		enable-active-high;
 75  	};
 76  
 77  	vdd_disp2_2v8: vdd-disp2-2v8-regulator {
 78  		compatible = "regulator-fixed";
 79  		regulator-name = "vdd_disp2_2v8";
 80  
 81  		regulator-min-microvolt = <2800000>;
 82  		regulator-max-microvolt = <2800000>;
 83  
 84  		gpio = <&tlmm 143 GPIO_ACTIVE_HIGH>;
 85  		enable-active-high;
 86  	};
 87  
 88  	vdd_ts_3v0: vdd-ts-3v0-regulator {
 89  		compatible = "regulator-fixed";
 90  		regulator-name = "vdd_ts_3v0";
 91  
 92  		regulator-min-microvolt = <3000000>;
 93  		regulator-max-microvolt = <3000000>;
 94  
 95  		gpio = <&tlmm 144 GPIO_ACTIVE_HIGH>;
 96  		enable-active-high;
 97  	};
 98  
 99  	vdd_ts_1v8: vdd-ts-1v8-regulator {
100  		compatible = "regulator-fixed";
101  		regulator-name = "vdd_ts_1v8";
102  
103  		regulator-min-microvolt = <1800000>;
104  		regulator-max-microvolt = <1800000>;
105  
106  		gpio = <&tlmm 102 GPIO_ACTIVE_HIGH>;
107  		enable-active-high;
108  	};
109  
110  	multi-ledr1 {
111  		compatible = "leds-group-multicolor";
112  		color = <LED_COLOR_ID_RGB>;
113  		function = "r1";
114  		leds = <&ledr_r4>, <&ledr_g4>, <&ledr_b4>;
115  	};
116  
117  	multi-ledl1 {
118  		compatible = "leds-group-multicolor";
119  		color = <LED_COLOR_ID_RGB>;
120  		function = "l1";
121  		leds = <&ledl_r4>, <&ledl_g4>, <&ledl_b4>;
122  	};
123  
124  	multi-ledr2 {
125  		compatible = "leds-group-multicolor";
126  		color = <LED_COLOR_ID_RGB>;
127  		function = "r2";
128  		leds = <&ledr_r1>, <&ledr_g1>, <&ledr_b1>;
129  	};
130  
131  	multi-ledl2 {
132  		compatible = "leds-group-multicolor";
133  		color = <LED_COLOR_ID_RGB>;
134  		function = "l2";
135  		leds = <&ledl_r1>, <&ledl_g1>, <&ledl_b1>;
136  	};
137  
138  	multi-ledr3 {
139  		compatible = "leds-group-multicolor";
140  		color = <LED_COLOR_ID_RGB>;
141  		function = "r3";
142  		leds = <&ledr_r2>, <&ledr_g2>, <&ledr_b2>;
143  	};
144  
145  	multi-ledl3 {
146  		compatible = "leds-group-multicolor";
147  		color = <LED_COLOR_ID_RGB>;
148  		function = "l3";
149  		leds = <&ledl_r2>, <&ledl_g2>, <&ledl_b2>;
150  	};
151  
152  	multi-ledr4 {
153  		compatible = "leds-group-multicolor";
154  		color = <LED_COLOR_ID_RGB>;
155  		function = "r4";
156  		leds = <&ledr_r3>, <&ledr_g3>, <&ledr_b3>;
157  	};
158  
159  	multi-ledl4 {
160  		compatible = "leds-group-multicolor";
161  		color = <LED_COLOR_ID_RGB>;
162  		function = "l4";
163  		leds = <&ledl_r3>, <&ledl_g3>, <&ledl_b3>;
164  	};
165  };
166  
167  &display_panel {
168  	compatible = "chipone,icna3520";
169  
170  	pinctrl-0 = <&dsi_s_rst_active>, <&dsi_s_te_active>;
171  	pinctrl-1 = <&dsi_s_rst_suspend>, <&dsi_s_te_suspend>;
172  	pinctrl-names = "default", "sleep";
173  
174  	vdd-supply = <&vreg_l11b_1p2>;
175  	vddio-supply = <&vreg_l12b_1p8>;
176  	vci-supply = <&vreg_l14b_3p2>;
177  	disp-supply = <&vdd_disp1_2v8>;
178  	blvdd-supply = <&vdd_bl_5v0>;
179  
180  	reset-gpios = <&tlmm 137 GPIO_ACTIVE_LOW>;
181  
182  	rotation = <90>;
183  };
184  
185  &i2c0 {
186  	htr3212l: led-controller@3c {
187  		compatible = "heroic,htr3212";
188  		reg = <0x3c>;
189  		#address-cells = <1>;
190  		#size-cells = <0>;
191  		sdb-gpios = <&tlmm 55 GPIO_ACTIVE_HIGH>;
192  		vdd-supply = <&vdd_mcu_3v3>;
193  
194  		ledl_b1: led@1 {
195  			reg = <1>;
196  			label = "l:r1";
197  			color = <LED_COLOR_ID_RED>;
198  		};
199  		ledl_g1: led@2 {
200  			reg = <2>;
201  			label = "l:g1";
202  			color = <LED_COLOR_ID_GREEN>;
203  		};
204  		ledl_r1: led@3 {
205  			reg = <3>;
206  			label = "l:b1";
207  			color = <LED_COLOR_ID_BLUE>;
208  		};
209  		ledl_b2: led@4 {
210  			reg = <4>;
211  			label = "l:r2";
212  			color = <LED_COLOR_ID_RED>;
213  		};
214  		ledl_g2: led@5 {
215  			reg = <5>;
216  			label = "l:g2";
217  			color = <LED_COLOR_ID_GREEN>;
218  		};
219  		ledl_r2: led@6 {
220  			reg = <6>;
221  			label = "l:b2";
222  			color = <LED_COLOR_ID_BLUE>;
223  		};
224  		ledl_b3: led@7 {
225  			reg = <7>;
226  			label = "l:r3";
227  			color = <LED_COLOR_ID_RED>;
228  		};
229  		ledl_g3: led@8 {
230  			reg = <8>;
231  			label = "l:g3";
232  			color = <LED_COLOR_ID_GREEN>;
233  		};
234  		ledl_r3: led@9 {
235  			reg = <9>;
236  			label = "l:b3";
237  			color = <LED_COLOR_ID_BLUE>;
238  		};
239  		ledl_b4: led@10 {
240  			reg = <10>;
241  			label = "l:r4";
242  			color = <LED_COLOR_ID_RED>;
243  		};
244  		ledl_g4: led@11 {
245  			reg = <11>;
246  			label = "l:g4";
247  			color = <LED_COLOR_ID_GREEN>;
248  		};
249  		ledl_r4: led@12 {
250  			reg = <12>;
251  			label = "l:b4";
252  			color = <LED_COLOR_ID_BLUE>;
253  		};
254  	};
255  };
256  
257  &i2c4 {
258  	touchscreen@38 {
259  		compatible = "focaltech,ft5426";
260  		reg = <0x38>;
261  		#address-cells = <1>;
262  		#size-cells = <0>;
263  
264  		interrupt-parent = <&tlmm>;
265  		interrupts = <25 IRQ_TYPE_EDGE_FALLING>;
266  
267  		reset-gpios = <&tlmm 24 GPIO_ACTIVE_LOW>;
268  
269  		vcc-supply = <&vreg_l14b_3p2>;
270  		iovcc-supply = <&vreg_l12b_1p8>;
271  
272  		pinctrl-0 = <&ts_p_rst_default &ts_p_int_default>;
273  		pinctrl-1 = <&ts_p_rst_sleep &ts_p_int_sleep>;
274  		pinctrl-names = "default", "sleep";
275  
276  		touchscreen-size-x = <1080>;
277  		touchscreen-size-y = <1920>;
278  		touchscreen-swapped-x-y;
279  		touchscreen-inverted-x;
280  
281  		label = "top_touchscreen";
282  	};
283  };
284  
285  &i2c12 {
286  	htr3212r: led-controller@3c {
287  		compatible = "heroic,htr3212";
288  		reg = <0x3c>;
289  		#address-cells = <1>;
290  		#size-cells = <0>;
291  		sdb-gpios = <&tlmm 56 GPIO_ACTIVE_HIGH>;
292  		vdd-supply = <&vdd_mcu_3v3>;
293  
294  		ledr_b1: led@1 {
295  			reg = <1>;
296  			label = "r:r1";
297  			color = <LED_COLOR_ID_RED>;
298  		};
299  		ledr_g1: led@2 {
300  			reg = <2>;
301  			label = "r:g1";
302  			color = <LED_COLOR_ID_GREEN>;
303  		};
304  		ledr_r1: led@3 {
305  			reg = <3>;
306  			label = "r:b1";
307  			color = <LED_COLOR_ID_BLUE>;
308  		};
309  		ledr_b2: led@4 {
310  			reg = <4>;
311  			label = "r:r2";
312  			color = <LED_COLOR_ID_RED>;
313  		};
314  		ledr_g2: led@5 {
315  			reg = <5>;
316  			label = "r:g2";
317  			color = <LED_COLOR_ID_GREEN>;
318  		};
319  		ledr_r2: led@6 {
320  			reg = <6>;
321  			label = "r:b2";
322   			color = <LED_COLOR_ID_BLUE>;
323  		};
324  		ledr_b3: led@7 {
325  			reg = <7>;
326  			label = "r:r3";
327  			color = <LED_COLOR_ID_RED>;
328  		};
329  		ledr_g3: led@8 {
330  			reg = <8>;
331  			label = "r:g3";
332  			color = <LED_COLOR_ID_GREEN>;
333  		};
334  		ledr_r3: led@9 {
335  			reg = <9>;
336  			label = "r:b3";
337  			color = <LED_COLOR_ID_BLUE>;
338  		};
339  		ledr_b4: led@10 {
340  			reg = <10>;
341  			label = "r:r4";
342  			color = <LED_COLOR_ID_RED>;
343  		};
344  		ledr_g4: led@11 {
345  			reg = <11>;
346  			label = "r:g4";
347  			color = <LED_COLOR_ID_GREEN>;
348  		};
349  		ledr_r4: led@12 {
350  			reg = <12>;
351  			label = "r:b4";
352  			color = <LED_COLOR_ID_BLUE>;
353  		};
354  	};
355  };
356  
357  &{/sound} {
358  	model = "AYN-Thor";
359  	audio-routing =
360  			"IN1_HPHL", "HPHL_OUT",
361  			"IN2_HPHR", "HPHR_OUT",
362  			"AMIC2", "MIC BIAS2",
363  			"TX SWR_INPUT1", "ADC2_OUTPUT",
364  			"DMIC3", "MIC BIAS3",
365  			"TX SWR_INPUT7", "DMIC3_OUTPUT";
366  };
367  
368  &{/sound/wcd-capture-dai-link/codec} {
369  	sound-dai = <&wcd938x 1>, <&swr2 1>, <&lpass_txmacro 0>;
370  };
371  
372  &i2c_hub_3 {
373  	clock-frequency = <100000>;
374  	status = "okay";
375  
376  	touchscreen@38 {
377  		compatible = "focaltech,ft5452";
378  		reg = <0x38>;
379  		#address-cells = <1>;
380  		#size-cells = <0>;
381  
382  		interrupt-parent = <&tlmm>;
383  		interrupts = <15 IRQ_TYPE_EDGE_FALLING>;
384  
385  		reset-gpios = <&tlmm 14 GPIO_ACTIVE_LOW>;
386  
387  		vcc-supply = <&vdd_ts_3v0>;
388  		iovcc-supply = <&vdd_ts_1v8>;
389  
390  		pinctrl-0 = <&ts_s_rst_default &ts_s_int_default>;
391  		pinctrl-1 = <&ts_s_rst_sleep &ts_s_int_sleep>;
392  		pinctrl-names = "default", "sleep";
393  
394  		touchscreen-size-x = <1080>;
395  		touchscreen-size-y = <1240>;
396  		touchscreen-swapped-x-y;
397  		touchscreen-inverted-x;
398  
399  		label = "bottom_touchscreen";
400  
401  		no-regmap-bulk-read;
402  	};
403  };
404  
405  &mdss_dsi0 {
406  	vdda-supply = <&vreg_l3e_1p2>;
407  	status = "okay";
408  
409  	panel@0 {
410  		reg = <0>;
411  		compatible = "ch13726a,thor";
412  
413  		pinctrl-0 = <&dsi_p_rst_active>, <&dsi_p_te_active>;
414  		pinctrl-1 = <&dsi_p_rst_suspend>, <&dsi_p_te_suspend>;
415  		pinctrl-names = "default", "sleep";
416  
417  		vdd1v2-supply = <&vreg_l11b_1p2>;
418  		vddio-supply = <&vdd_disp_1v8>;
419  		vdd-supply = <&vreg_l13b_3p0>;
420  		avdd-supply = <&vdd_disp2_2v8>;
421  
422  		reset-gpios = <&tlmm 133 GPIO_ACTIVE_HIGH>;
423  
424  		rotation = <90>;
425  
426  		port {
427  			panel0_in: endpoint {
428  				remote-endpoint = <&mdss_dsi0_out>;
429  			};
430  		};
431  	};
432  };
433  
434  &mdss_dsi0_out {
435  	remote-endpoint = <&panel0_in>;
436  	data-lanes = <0 1 2 3>;
437  };
438  
439  &mdss_dsi0_phy {
440  	vdds-supply = <&vreg_l1e_0p88>;
441  	status = "okay";
442  };
443  
444  &mdss_dsi1_out {
445  	qcom,te-source = "mdp_vsync_s";
446  };
447  
448  &tlmm {
449  	key_ayn_n: key-ayn-n-state {
450  		pins = "gpio41";
451  		function = "gpio";
452  		bias-pull-up;
453  		output-disable;
454  	};
455  };
456  
457  &remoteproc_adsp {
458  	firmware-name = "qcom/sm8550/ayn/thor/adsp.mbn",
459  			"qcom/sm8550/ayn/thor/adsp_dtb.mbn";
460  	status = "okay";
461  };
462  
463  &spk_amp_l {
464  	firmware-name = "qcom/sm8550/ayn/thor/aw883xx_acf.bin";
465  };
466  
467  &spk_amp_r {
468  	firmware-name = "qcom/sm8550/ayn/thor/aw883xx_acf.bin";
469  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rp6-top-dpad.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: BSD-3-Clause
 2  /*
 3   * Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX).
 4   */
 5  
 6  /dts-v1/;
 7  
 8  #include "qcs8550-retroidpocket-rp6.dts"
 9  
10  / {
11  	model = "Retroid Pocket 6 TOP-DPAD";
12  };
13  
14  &gamepad {
15      invert-x;
16      invert-y;
17  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rp6.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
  1  // SPDX-License-Identifier: BSD-3-Clause
  2  /*
  3   * Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX).
  4   */
  5  
  6  /dts-v1/;
  7  
  8  #include "qcs8550-ayn-common.dtsi"
  9  
 10  / {
 11  	model = "Retroid Pocket 6";
 12  	compatible = "retroidpocket,rp6", "qcom,qcs8550", "qcom,sm8550";
 13  	qcom,board-id = <0x1001f 0x00>;
 14  	qcom,msm-id = <0x25b 0x20000>;
 15  
 16  	backlight: backlight {
 17  		compatible = "pwm-backlight";
 18  		pwms = <&pmk8550_pwm 0 860000>;
 19  		brightness-levels = <1023 0>;
 20  		num-interpolated-steps = <1023>;
 21  		default-brightness-level = <600>;
 22  		power-supply = <&vph_pwr>;
 23  		enable-gpios = <&pmk8550_gpios 5 GPIO_ACTIVE_HIGH>;
 24  		pinctrl-names = "default";
 25  		pinctrl-0 = <&pwm_backlight_default>;
 26  		status = "okay";
 27  	};
 28  
 29  	vdd_disp_1v8: vdd-disp-1v8-regulator {
 30  		compatible = "regulator-fixed";
 31  		regulator-name = "vdd_disp_1v8";
 32  
 33  		regulator-min-microvolt = <1800000>;
 34  		regulator-max-microvolt = <1800000>;
 35  
 36  		gpio = <&tlmm 70 GPIO_ACTIVE_HIGH>;
 37  		enable-active-high;
 38  	};
 39  
 40  	vdd_disp_2v8: vdd-disp-2v8-regulator {
 41  		compatible = "regulator-fixed";
 42  		regulator-name = "vdd_disp_2v8";
 43  
 44  		regulator-min-microvolt = <2800000>;
 45  		regulator-max-microvolt = <2800000>;
 46  
 47  		gpio = <&tlmm 142 GPIO_ACTIVE_HIGH>;
 48  		enable-active-high;
 49  	};
 50  
 51  	ts_avdd_3v0: regulator-ts-avdd-3v0 {
 52  		compatible = "regulator-fixed";
 53  		regulator-name = "ts_avdd_3v0";
 54  
 55  		regulator-min-microvolt = <3000000>;
 56  		regulator-max-microvolt = <3000000>;
 57  
 58  		gpio = <&tlmm 144 GPIO_ACTIVE_HIGH>;
 59  		enable-active-high;
 60  	};
 61  
 62  	ts_vddio_1v8: regulator-ts-vddio-1v8 {
 63  		compatible = "regulator-fixed";
 64  		regulator-name = "ts_vddio_1v8";
 65  
 66  		regulator-min-microvolt = <1800000>;
 67  		regulator-max-microvolt = <1800000>;
 68  
 69  		gpio = <&tlmm 102 GPIO_ACTIVE_HIGH>;
 70  		enable-active-high;
 71  	};
 72  
 73  	multi-ledr1 {
 74  		compatible = "leds-group-multicolor";
 75  		color = <LED_COLOR_ID_RGB>;
 76  		function = "r1";
 77  		leds = <&ledr_r4>, <&ledr_g4>, <&ledr_b4>;
 78  	};
 79  
 80  	multi-ledl1 {
 81  		compatible = "leds-group-multicolor";
 82  		color = <LED_COLOR_ID_RGB>;
 83  		function = "l1";
 84  		leds = <&ledl_r4>, <&ledl_g4>, <&ledl_b4>;
 85  	};
 86  
 87  	multi-ledr2 {
 88  		compatible = "leds-group-multicolor";
 89  		color = <LED_COLOR_ID_RGB>;
 90  		function = "r2";
 91  		leds = <&ledr_r1>, <&ledr_g1>, <&ledr_b1>;
 92  	};
 93  
 94  	multi-ledl2 {
 95  		compatible = "leds-group-multicolor";
 96  		color = <LED_COLOR_ID_RGB>;
 97  		function = "l2";
 98  		leds = <&ledl_r1>, <&ledl_g1>, <&ledl_b1>;
 99  	};
100  
101  	multi-ledr3 {
102  		compatible = "leds-group-multicolor";
103  		color = <LED_COLOR_ID_RGB>;
104  		function = "r3";
105  		leds = <&ledr_r2>, <&ledr_g2>, <&ledr_b2>;
106  	};
107  
108  	multi-ledl3 {
109  		compatible = "leds-group-multicolor";
110  		color = <LED_COLOR_ID_RGB>;
111  		function = "l3";
112  		leds = <&ledl_r2>, <&ledl_g2>, <&ledl_b2>;
113  	};
114  
115  	multi-ledr4 {
116  		compatible = "leds-group-multicolor";
117  		color = <LED_COLOR_ID_RGB>;
118  		function = "r4";
119  		leds = <&ledr_r3>, <&ledr_g3>, <&ledr_b3>;
120  	};
121  
122  	multi-ledl4 {
123  		compatible = "leds-group-multicolor";
124  		color = <LED_COLOR_ID_RGB>;
125  		function = "l4";
126  		leds = <&ledl_r3>, <&ledl_g3>, <&ledl_b3>;
127  	};
128  };
129  
130  &gamepad {
131  	axis-range = <1024>;
132  };
133  
134  &{/gpio-keys} {
135  	pinctrl-0 = <&volume_up_n>, <&paddle_keys_default>;
136  
137  	key-paddle-left {
138  		label = "Back Paddle Left";
139  		debounce-interval = <15>;
140  		gpios = <&tlmm 57 GPIO_ACTIVE_LOW>;
141  		linux,code = <BTN_Z>;
142  	};
143  
144  	key-paddle-right {
145  		label = "Back Paddle Right";
146  		debounce-interval = <15>;
147  		gpios = <&tlmm 58 GPIO_ACTIVE_LOW>;
148  		linux,code = <BTN_C>;
149  	};
150  };
151  
152  &tlmm {
153  	paddle_keys_default: paddle-keys-default-state {
154  		pins = "gpio57", "gpio58";
155  		function = "gpio";
156  		bias-pull-up;
157  		drive-strength = <2>;
158  		input-enable;
159  	};
160  };
161  
162  &mdss_dsi0 {
163  	vdda-supply = <&vreg_l3e_1p2>;
164  	status = "okay";
165  
166  	panel@0 {
167  		reg = <0>;
168  		compatible = "vtdr6130,rp6";
169  
170  		pinctrl-0 = <&dsi_p_rst_active>, <&dsi_p_te_active>;
171  		pinctrl-1 = <&dsi_p_rst_suspend>, <&dsi_p_te_suspend>;
172  		pinctrl-names = "default", "sleep";
173  
174  		vddio-supply = <&vdd_disp_1v8>;
175  		avdd-supply = <&vdd_disp_2v8>;
176  
177  		reset-gpios = <&tlmm 133 GPIO_ACTIVE_LOW>;
178  
179  		backlight = <&backlight>;
180  
181  		rotation = <270>;
182  
183  		port {
184  			panel0_in: endpoint {
185  				remote-endpoint = <&mdss_dsi0_out>;
186  			};
187  		};
188  	};
189  };
190  
191  &mdss_dsi0_out {
192  	remote-endpoint = <&panel0_in>;
193  	data-lanes = <0 1 2 3>;
194  };
195  
196  &mdss_dsi0_phy {
197  	vdds-supply = <&vreg_l1e_0p88>;
198  	status = "okay";
199  };
200  
201  &mdss_dsi1 {
202      status = "disabled";
203  };
204  
205  &i2c0 {
206  	htr3212l: led-controller@3c {
207  		compatible = "heroic,htr3212";
208  		reg = <0x3c>;
209  		#address-cells = <1>;
210  		#size-cells = <0>;
211  		sdb-gpios = <&tlmm 55 GPIO_ACTIVE_HIGH>;
212  		vdd-supply = <&vdd_mcu_3v3>;
213  
214  		ledl_b1: led@1 {
215  			reg = <1>;
216  			label = "l:r1";
217  			color = <LED_COLOR_ID_RED>;
218  		};
219  		ledl_g1: led@2 {
220  			reg = <2>;
221  			label = "l:g1";
222  			color = <LED_COLOR_ID_GREEN>;
223  		};
224  		ledl_r1: led@3 {
225  			reg = <3>;
226  			label = "l:b1";
227  			color = <LED_COLOR_ID_BLUE>;
228  		};
229  		ledl_b2: led@4 {
230  			reg = <4>;
231  			label = "l:r2";
232  			color = <LED_COLOR_ID_RED>;
233  		};
234  		ledl_g2: led@5 {
235  			reg = <5>;
236  			label = "l:g2";
237  			color = <LED_COLOR_ID_GREEN>;
238  		};
239  		ledl_r2: led@6 {
240  			reg = <6>;
241  			label = "l:b2";
242  			color = <LED_COLOR_ID_BLUE>;
243  		};
244  		ledl_b3: led@7 {
245  			reg = <7>;
246  			label = "l:r3";
247  			color = <LED_COLOR_ID_RED>;
248  		};
249  		ledl_g3: led@8 {
250  			reg = <8>;
251  			label = "l:g3";
252  			color = <LED_COLOR_ID_GREEN>;
253  		};
254  		ledl_r3: led@9 {
255  			reg = <9>;
256  			label = "l:b3";
257  			color = <LED_COLOR_ID_BLUE>;
258  		};
259  		ledl_b4: led@10 {
260  			reg = <10>;
261  			label = "l:r4";
262  			color = <LED_COLOR_ID_RED>;
263  		};
264  		ledl_g4: led@11 {
265  			reg = <11>;
266  			label = "l:g4";
267  			color = <LED_COLOR_ID_GREEN>;
268  		};
269  		ledl_r4: led@12 {
270  			reg = <12>;
271  			label = "l:b4";
272  			color = <LED_COLOR_ID_BLUE>;
273  		};
274  	};
275  };
276  
277  &i2c12 {
278  	htr3212r: led-controller@3c {
279  		compatible = "heroic,htr3212";
280  		reg = <0x3c>;
281  		#address-cells = <1>;
282  		#size-cells = <0>;
283  		sdb-gpios = <&tlmm 56 GPIO_ACTIVE_HIGH>;
284  		vdd-supply = <&vdd_mcu_3v3>;
285  
286  		ledr_b1: led@1 {
287  			reg = <1>;
288  			label = "r:r1";
289  			color = <LED_COLOR_ID_RED>;
290  		};
291  		ledr_g1: led@2 {
292  			reg = <2>;
293  			label = "r:g1";
294  			color = <LED_COLOR_ID_GREEN>;
295  		};
296  		ledr_r1: led@3 {
297  			reg = <3>;
298  			label = "r:b1";
299  			color = <LED_COLOR_ID_BLUE>;
300  		};
301  		ledr_b2: led@4 {
302  			reg = <4>;
303  			label = "r:r2";
304  			color = <LED_COLOR_ID_RED>;
305  		};
306  		ledr_g2: led@5 {
307  			reg = <5>;
308  			label = "r:g2";
309  			color = <LED_COLOR_ID_GREEN>;
310  		};
311  		ledr_r2: led@6 {
312  			reg = <6>;
313  			label = "r:b2";
314  			color = <LED_COLOR_ID_BLUE>;
315  		};
316  		ledr_b3: led@7 {
317  			reg = <7>;
318  			label = "r:r3";
319  			color = <LED_COLOR_ID_RED>;
320  		};
321  		ledr_g3: led@8 {
322  			reg = <8>;
323  			label = "r:g3";
324  			color = <LED_COLOR_ID_GREEN>;
325  		};
326  		ledr_r3: led@9 {
327  			reg = <9>;
328  			label = "r:b3";
329  			color = <LED_COLOR_ID_BLUE>;
330  		};
331  		ledr_b4: led@10 {
332  			reg = <10>;
333  			label = "r:r4";
334  			color = <LED_COLOR_ID_RED>;
335  		};
336  		ledr_g4: led@11 {
337  			reg = <11>;
338  			label = "r:g4";
339  			color = <LED_COLOR_ID_GREEN>;
340  		};
341  		ledr_r4: led@12 {
342  			reg = <12>;
343  			label = "r:b4";
344  			color = <LED_COLOR_ID_BLUE>;
345  		};
346  	};
347  };
348  
349  &i2c_hub_3 {
350  	clock-frequency = <400000>;
351  	status = "okay";
352  	touchscreen@38 {
353  		compatible = "focaltech,ft5426";
354  		reg = <0x38>;
355  		#address-cells = <1>;
356  		#size-cells = <0>;
357  
358  		interrupt-parent = <&tlmm>;
359  		interrupts = <15 IRQ_TYPE_EDGE_FALLING>;
360  		reset-gpios = <&tlmm 14 GPIO_ACTIVE_LOW>;
361  
362  		vcc-supply = <&ts_avdd_3v0>;
363  		iovcc-supply = <&ts_vddio_1v8>;
364  
365  		pinctrl-0 = <&ts_p_rst_default &ts_p_int_default>;
366  		pinctrl-1 = <&ts_p_rst_sleep &ts_p_int_sleep>;
367  		pinctrl-names = "default", "sleep";
368  
369  		touchscreen-size-x = <1080>;
370  		touchscreen-size-y = <1920>;
371  		touchscreen-inverted-y;
372          };
373  };
374  
375  &pmk8550_pwm {
376  	status = "okay";
377  };
378  
379  &remoteproc_adsp {
380  	firmware-name = "qcom/sm8550/ayn/odin2/adsp.mbn",
381  			"qcom/sm8550/ayn/odin2/adsp_dtb.mbn";
382  	status = "okay";
383  };
384  
385  &spk_amp_l {
386  	firmware-name = "qcom/sm8550/ayn/odin2/aw883xx_acf.bin";
387  };
388  
389  &spk_amp_r {
390  	firmware-name = "qcom/sm8550/ayn/odin2/aw883xx_acf.bin";
391  };
```


## projects/ROCKNIX/devices/SM8550/linux/dts/qcom/qcs8550-retroidpocket-rpnova.dts @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  // SPDX-License-Identifier: GPL-2.0
 2  /*
 3   * Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX).
 4   */
 5  
 6  /dts-v1/;
 7  
 8  #include "qcs8550-retroidpocket-rp6.dts"
 9  
10  / {
11  	model = "Retroid Pocket Nova";
12  	compatible = "retroidpocket,rpnova", "qcom,qcs8550", "qcom,sm8550";
13  };
14  
15  &mdss_dsi0 {
16  	panel@0 {
17  		compatible = "il97680a,rpnova";
18  		/delete-property/ rotation;
19  	};
20  };
21  
22  &i2c_hub_3 {
23  	touchscreen@38 {
24  		touchscreen-size-x = <1280>;
25  		touchscreen-size-y = <960>;
26  		/delete-property/ touchscreen-inverted-y;
27  	};
28  };
29  
30  &gamepad {
31  	invert-x;
32  	invert-y;
33  	trigger-left-deadzone = <100>;
34  	trigger-right-deadzone = <100>;
35  };
```


## projects/ROCKNIX/devices/SM8550/options @ 8ebaf8daad (whole, line-numbered, masked)

```text
 1  ################################################################################
 2  # setup device defaults
 3  ################################################################################
 4  
 5    # The TARGET_CPU variable controls which processor should be targeted for
 6    # generated code.
 7      case ${TARGET_ARCH} in
 8        aarch64)
 9          TARGET_CPU="cortex-x3"
10          TARGET_CPU_FLAGS="+fp16+crypto+i8mm+bf16+memtag+sm4+sha3+nosve+nosve2"
11          ;;
12        arm)
13          TARGET_KERNEL_ARCH="arm64"
14          TARGET_FLOAT="hard"
15          TARGET_CPU="cortex-a710"
16          TARGET_CPU_FLAGS="+fp16+crypto+i8mm+bf16"
17          TARGET_FPU="crypto-neon-fp-armv8"
18          ;;
19      esac
20  
21      PARTITION_TABLE="gpt"
22      HW_CPU="Snapdragon 8 Gen2"
23  
24    # Kernel target
25      KERNEL_TARGET="Image"
26  
27    # Additional kernel make parameters (for example to specify the u-boot loadaddress)
28      KERNEL_MAKE_EXTRACMD=" $(get_kernel_make_extracmd)"
29  
30    # Kernel cmdline
31      EXTRA_CMDLINE="quiet rootwait console=tty0 allow_mismatched_32bit_el0 fw_devlink.strict=1 pcie_ports=compat irqaffinity=0-2 cgroup.memory=nokmem,nosocket nosoftlockup usbcore.interrupt_interval_override=045e:028e:2"
32  
33    # Bootloader to use (syslinux / u-boot)
34      BOOTLOADER="qcom-abl"
35  
36    # Adreno GPU family
37      GRAPHIC_DRIVERS="freedreno"
38  
39    # For maximum cross compatbility
40      PREFER_GLES="no"
41  
42    # VULKAN_SUPPORT
43      VULKAN_SUPPORT="yes"
44  
45    # Vulkan implementation to use (vulkan-loader / no)
46      VULKAN="vulkan-loader"
47  
48    # Displayserver to use (wl / no)
49      DISPLAYSERVER="wl"
50  
51    # Windowmanager to use (weston / swaywm-env / no)
52      WINDOWMANAGER="swaywm-env"
53  
54    # Additional drivers to install:
55    # for a list of additional drivers see packages/linux-drivers
56    # Space separated list is supported,
57    # e.g. ADDITIONAL_DRIVERS="DRIVER1 DRIVER2"
58      ADDITIONAL_DRIVERS=""
59  
60    # Additional Firmware to use ( )
61    # Space separated list is supported,
62    # e.g. FIRMWARE=""
63      FIRMWARE="extra-firmware"
64  
65    # Additional packages to install
66      ADDITIONAL_PACKAGES="gamepadcalibration rocknix-abl inputplumber"
67  
68    # Debug tty path
69      DEBUG_TTY="/dev/ttyMSM0"
70  
71    # Build and install rocknix joypad driver (yes / no)
72      ROCKNIX_JOYPAD="no"
73  
74    # ZRAM Algorithm
75      ZRAM_COMPRESSION_ALGO="zstd"
76  
77    # ZRAM Size
78      ZRAM_SWAP_SIZE="Auto"
79  
80    # Disk Swap
81      SWAP_FILE_SIZE="0"
```


## projects/ROCKNIX/devices/SM8550/patches/linux/0053-add-hynitron-touchscreen.patch.disabled: lines 1-12 @ 8ebaf8daad (of 20,593)

```text
 1  From 01adf785d41c372fa044d38bd07c91e8bac7e626 Mon Sep 17 00:00:00 2001
 2  From: KancyJoe <kancy2333@outlook.com>
 3  Date: Tue, 1 Jul 2025 16:47:14 +0000
 4  Subject: [PATCH] input: touchscreen: porting downstream hynitron driver from
 5   lubancat bsp. Refernce Link:
 6   https://github.com/LubanCat/RV06_03_Linux_SDK/tree/main/sysdrv/source/kernel/drivers/input/touchscreen/hyn_driver
 7  
 8  ---
 9   drivers/input/touchscreen/Kconfig             |    6 +
10   drivers/input/touchscreen/Makefile            |    1 +
11   drivers/input/touchscreen/hynitron/Makefile   |   13 +
12   drivers/input/touchscreen/hynitron/hyn_cfg.h  |   44 +
```


## projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf: lines 1-6 @ 8ebaf8daad

```text
1  #
2  # Automatically generated file; DO NOT EDIT.
3  # Linux/arm64 7.2.0 Kernel Configuration
4  #
5  CONFIG_CC_VERSION_TEXT="aarch64-rocknix-linux-gnu-gcc-15.2.0 (GCC) 15.2.0"
6  CONFIG_CC_IS_GCC=y
```


## diff projects/ROCKNIX/devices/SM8550/linux/linux.aarch64.conf @ 651150fc88 (<) against @ 8ebaf8daad (>) (7 removed, 7 added)

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
2728a2728
> # CONFIG_INPUT_POLLDEV is not set
8219c8219
< # CONFIG_RAID6_PQ_BENCHMARK is not set
---
> CONFIG_RAID6_PQ_BENCHMARK=y
```


## CONFIG_DRM_MSM and CONFIG_EXTRA_FIRMWARE in the four Qualcomm configurations @ 8ebaf8daad

```text
SM8550: CONFIG_EXTRA_FIRMWARE="" CONFIG_DRM_MSM=y
SM8650: CONFIG_EXTRA_FIRMWARE="" CONFIG_DRM_MSM=y
SM8750: CONFIG_EXTRA_FIRMWARE="" CONFIG_DRM_MSM=y
SM8250: CONFIG_EXTRA_FIRMWARE="" CONFIG_DRM_MSM=y
```


## projects/ROCKNIX/packages/linux/package.mk @ 8ebaf8daad: lines 1-120 (excerpt)

```text
  1  # SPDX-License-Identifier: GPL-2.0-or-later
  2  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
  3  # Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)
  4  
  5  PKG_NAME="linux"
  6  PKG_LICENSE="GPL"
  7  PKG_SITE="http://www.kernel.org"
  8  PKG_DEPENDS_HOST="ccache:host openssl:host"
  9  PKG_DEPENDS_TARGET="linux:host kmod:host xz:host keyutils ncurses openssl:host ${KERNEL_EXTRA_DEPENDS_TARGET}"
 10  PKG_NEED_UNPACK="${LINUX_DEPENDS} $(get_pkg_directory initramfs) $(get_pkg_variable initramfs PKG_NEED_UNPACK)"
 11  PKG_NEED_UNPACK+=" ${PROJECT_DIR}/${PROJECT}/bootloader ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader"
 12  PKG_LONGDESC="This package contains a precompiled kernel image and the modules."
 13  PKG_IS_KERNEL_PKG="yes"
 14  PKG_STAMP="${KERNEL_TARGET} ${KERNEL_MAKE_EXTRACMD}"
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
 61    PKG_DEPENDS_TARGET+=" toolchain"
 62  fi
 63  
 64  if [ "${PKG_BUILD_PERF}" != "no" ] && grep -q ^CONFIG_PERF_EVENTS= ${PKG_KERNEL_CFG_FILE}; then
 65    PKG_BUILD_PERF="yes"
 66    PKG_DEPENDS_TARGET+=" binutils elfutils libunwind zlib openssl"
 67  fi
 68  
 69  if [[ "${TARGET_ARCH}" =~ i*86|x86_64 ]]; then
 70    PKG_DEPENDS_TARGET+=" elfutils:host pciutils"
 71    PKG_DEPENDS_UNPACK+=" intel-ucode kernel-firmware"
 72  fi
 73  
 74  # Ensure that the dependencies of initramfs:target are built correctly, but
 75  # we don't want to add initramfs:target as a direct dependency as we install
 76  # this "manually" from within linux:target
 77  for pkg in $(get_pkg_variable initramfs PKG_DEPENDS_TARGET); do
 78    ! listcontains "${PKG_DEPENDS_TARGET}" "${pkg}" && PKG_DEPENDS_TARGET+=" ${pkg}" || true
 79  done
 80  
 81  if [ "${DEVICE}" = "RK3326" -o "${DEVICE}" = "RK3566" ]; then
 82    PKG_DEPENDS_UNPACK+=" generic-dsi"
 83  elif [ "${DEVICE}" = "SM8250" -o "${DEVICE}" = "H700" -o "${DEVICE}" = "SM8650" -o "${DEVICE}" = "SM8750" ]; then
 84    PKG_DEPENDS_UNPACK+=" kernel-firmware"
 85  fi
 86  
 87  # SM8650/SM8750 build device-specific firmware blobs into the kernel, so the
 88  # extra-firmware package must be unpacked before the kernel is built.
 89  if [ "${DEVICE}" = "SM8650" -o "${DEVICE}" = "SM8750" ]; then
 90    PKG_DEPENDS_UNPACK+=" extra-firmware"
 91  fi
 92  
 93  # A built-in cfg80211 needs regulatory.db inside the kernel image (see
 94  # pre_make_target), so unpack wireless-regdb before the kernel is built.
 95  if grep -q '^CONFIG_CFG80211=y' ${PKG_KERNEL_CFG_FILE}; then
 96    PKG_DEPENDS_UNPACK+=" wireless-regdb"
 97  fi
 98  
 99  post_patch() {
100    # linux was already built and its build dir autoremoved - prepare it again for kernel packages
101    if [ -d ${PKG_INSTALL}/.image ]; then
102      cp -p ${PKG_INSTALL}/.image/.config ${PKG_BUILD}
103      kernel_make -C ${PKG_BUILD} prepare
104  
105      # restore the required Module.symvers from an earlier build
106      cp -p ${PKG_INSTALL}/.image/Module.symvers ${PKG_BUILD}
107    fi
108  
109    if [ "${DEVICE}" = "RK3326" -o "${DEVICE}" = "RK3566" -o "${DEVICE}" = "RK3576" ]; then
110      cp -v $(get_pkg_directory generic-dsi)/sources/panel-generic-dsi.c ${PKG_BUILD}/drivers/gpu/drm/panel/
111      echo "obj-y" += panel-generic-dsi.o >> ${PKG_BUILD}/drivers/gpu/drm/panel/Makefile
112    fi
113  
114    DTS_SOURCE_DIR="${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/linux/dts"
115    if [ -d "${DTS_SOURCE_DIR}" ]; then
116      rsync -av "${DTS_SOURCE_DIR}/" ${PKG_BUILD}/arch/arm64/boot/dts/
117    fi
118  }
119  
120  make_init() {
```


## projects/ROCKNIX/packages/linux/package.mk @ 8ebaf8daad: lines 190-290 (excerpt)

```text
190    fi
191  
192    # disable wireguard support if not enabled
193    if [ ! "${WIREGUARD_SUPPORT}" = yes ]; then
194      ${PKG_BUILD}/scripts/config --disable CONFIG_WIREGUARD
195    fi
196  
197    if [[ "${TARGET_ARCH}" =~ i*86|x86_64 ]]; then
198      # copy some extra firmware to linux tree
199      mkdir -p ${PKG_BUILD}/external-firmware
200        cp -a $(get_build_dir kernel-firmware)/.copied-firmware/{amdgpu,amd-ucode,i915,radeon,e100,rtl_nic} ${PKG_BUILD}/external-firmware
201  
202      cp -a $(get_build_dir intel-ucode)/intel-ucode ${PKG_BUILD}/external-firmware
203  
204      FW_LIST="$(find ${PKG_BUILD}/external-firmware \( -type f -o -type l \) \( -iname '*.bin' -o -iname '*.fw' -o -path '*/intel-ucode/*' \) | sed 's|.*external-firmware/||' | sort | xargs)"
205  
206      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
207      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
208    elif [ "${TARGET_ARCH}" = "aarch64" -a "${DEVICE}" = "SM8250" ]; then
209      mkdir -p ${PKG_BUILD}/external-firmware/qcom/sm8250
210      mkdir -p ${PKG_BUILD}/external-firmware/qcom/vpu-1.0
211        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/a650_gmu.bin ${PKG_BUILD}/external-firmware/qcom
212        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/a650_sqe.fw ${PKG_BUILD}/external-firmware/qcom
213        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/a650_zap.mbn ${PKG_BUILD}/external-firmware/qcom/sm8250
214        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/adsp.mbn ${PKG_BUILD}/external-firmware/qcom/sm8250
215        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/cdsp.mbn ${PKG_BUILD}/external-firmware/qcom/sm8250
216        cp $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/Thundercomm/RB5/* $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/
217        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8250/slpi.mbn ${PKG_BUILD}/external-firmware/qcom/sm8250
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
247        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen70900_aqe.fw ${PKG_BUILD}/external-firmware/qcom
248        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen70900_sqe.fw ${PKG_BUILD}/external-firmware/qcom
249        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gmu_gen70900.bin ${PKG_BUILD}/external-firmware/qcom
250      mkdir -p ${PKG_BUILD}/external-firmware/qcom/sm8650/ayaneo/ps2
251        cp -Lv $(get_build_dir extra-firmware)/SM8650/qcom/sm8650/ayaneo/ps2/gen70900_zap.mbn ${PKG_BUILD}/external-firmware/qcom/sm8650/ayaneo/ps2
252  
253      FW_LIST="$(find ${PKG_BUILD}/external-firmware -type f | sed 's|.*external-firmware/||' | sort | xargs)"
254  
255      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
256      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
257    elif [ "${TARGET_ARCH}" = "aarch64" -a "${DEVICE}" = "SM8750" ]; then
258      mkdir -p ${PKG_BUILD}/external-firmware/qcom
259        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen80000_aqe.fw ${PKG_BUILD}/external-firmware/qcom
260        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen80000_sqe.fw ${PKG_BUILD}/external-firmware/qcom
261        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/gen80000_gmu.bin ${PKG_BUILD}/external-firmware/qcom
262  
263      mkdir -p ${PKG_BUILD}/external-firmware/qcom/sm8750
264        cp -Lv $(get_build_dir kernel-firmware)/.copied-firmware/qcom/sm8750/gen80000_zap.mbn ${PKG_BUILD}/external-firmware/qcom/sm8750
265  
266      # KONKR Pocket FIT Elite: AW88261 speaker-amp ACF (vendor cal/profile blob,
267      # extracted from the stock Android image). The aw88261 driver requests the
268      # blob; the amp nodes point at it with firmware-name. Built-in so the codec
269      # probe never depends on the rootfs firmware overlay.
270      mkdir -p ${PKG_BUILD}/external-firmware/qcom/sm8750/konkr/pfe
271        cp -Lv $(get_build_dir extra-firmware)/SM8750/qcom/sm8750/konkr/pfe/aw88261_acf.bin ${PKG_BUILD}/external-firmware/qcom/sm8750/konkr/pfe
272  
273      # KONKR Pocket FIT Elite: QUAT-MI2S audio topology (the AYN tplg with its
274      # MI2S backend retargeted SECONDARY->QUATERNARY — the konkr's speaker amps
275      # are on QUATERNARY MI2S). Built-in firmware is searched before the rootfs,
276      # so this also overrides any stale copy in the SYSTEM overlay.
277        cp -Lv $(get_build_dir extra-firmware)/SM8750/qcom/sm8750/SM8750-KONKR-tplg.bin ${PKG_BUILD}/external-firmware/qcom/sm8750
278  
279      FW_LIST="$(find ${PKG_BUILD}/external-firmware -type f | sed 's|.*external-firmware/||' | sort | xargs)"
280  
281      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE "${FW_LIST}"
282      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
283    fi
284  
285    # cfg80211 requests regulatory.db as soon as it initialises. Built in (=y on
286    # every device but AMD64) that is during kernel init, while /usr/lib/firmware
287    # is still a dangling symlink to the kernel-overlay tmpfs that
288    # kernel-overlays-setup only populates later (scripts/image) - so the request
289    # fails with -ENOENT, the failure is cached, and the radio stays in domain 00
290    # with 5 GHz no-IR. Build the db into the kernel instead. The .p7s signature
```


## projects/ROCKNIX/packages/linux/package.mk @ 8ebaf8daad: lines 380-432 (excerpt)

```text
380    fi
381  }
382  
383  makeinstall_target() {
384    mkdir -p ${INSTALL}/.image
385    cp -p System.map .config Module.symvers ${INSTALL}/.image/
386  
387    if [ "${BOOTLOADER}" != "qcom-abl" ]; then
388    	cp -p arch/${TARGET_KERNEL_ARCH}/boot/${KERNEL_TARGET} ${INSTALL}/.image/
389    else
390  
391      gzip -c "arch/${TARGET_KERNEL_ARCH}/boot/${KERNEL_TARGET}" > "${INSTALL}/.image/kernel.gz"
392      for dtb in "arch/${TARGET_KERNEL_ARCH}/boot/dts/"**/*.dtb; do
393        if [ -f ${dtb} ]; then
394          cat "$dtb" >> "${INSTALL}/.image/kernel.gz"
395        fi
396      done
397      echo -n "dummy" > "${INSTALL}/.image/ramdisk"
398      python3 "${TOOLCHAIN}/mkbootimg/mkbootimg.py" \
399        --kernel "${INSTALL}/.image/kernel.gz" --ramdisk "${INSTALL}/.image/ramdisk" \
400  	  --kernel_offset 0x00000000 --ramdisk_offset 0x00000000 --tags_offset 0x00000000 \
401  	  --os_version 12.0.0 --os_patch_level "$(date '+%Y-%m')" --header_version 0 \
402  	  --cmdline "boot=LABEL=${DISTRO_BOOTLABEL} disk=LABEL=${DISTRO_DISKLABEL} ${EXTRA_CMDLINE}" \
403  	  -o "${INSTALL}/.image/${KERNEL_TARGET}" || { exit 1; }
404    fi
405  
406    kernel_make INSTALL_MOD_PATH=${INSTALL}/$(get_kernel_overlay_dir) modules_install
407    rm -f ${INSTALL}/$(get_kernel_overlay_dir)/lib/modules/*/build
408    rm -f ${INSTALL}/$(get_kernel_overlay_dir)/lib/modules/*/source
409  
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


## projects/ROCKNIX/packages/linux/package.mk @ 651150fc88: lines 1-60 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0-or-later
 2  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
 3  # Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)
 4  
 5  PKG_NAME="linux"
 6  PKG_LICENSE="GPL"
 7  PKG_SITE="http://www.kernel.org"
 8  PKG_DEPENDS_HOST="ccache:host openssl:host"
 9  PKG_DEPENDS_TARGET="linux:host kmod:host xz:host keyutils ncurses openssl:host ${KERNEL_EXTRA_DEPENDS_TARGET}"
10  PKG_NEED_UNPACK="${LINUX_DEPENDS} $(get_pkg_directory initramfs) $(get_pkg_variable initramfs PKG_NEED_UNPACK)"
11  PKG_NEED_UNPACK+=" ${PROJECT_DIR}/${PROJECT}/bootloader ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader"
12  PKG_LONGDESC="This package contains a precompiled kernel image and the modules."
13  PKG_IS_KERNEL_PKG="yes"
14  PKG_STAMP="${KERNEL_TARGET} ${KERNEL_MAKE_EXTRACMD}"
15  
16  PKG_PATCH_DIRS="${LINUX} mainline ${DEVICE} default"
17  
18  [[ "${DEVICE}" =~ "RK3326|RK3399|S922X|H700" ]] && PKG_PATCH_DIRS+=" rocknix-joypad"
19  [[ "${DEVICE}" == RK* ]] && PKG_PATCH_DIRS+=" mainline-rockchip"
20  
21  case ${DEVICE} in
22    RK3588)
23      PKG_VERSION="b8e62bed74766b6c8c423a767b35495e78b64caf"
24      PKG_SHA256="0e0fe5a2f108d525a044e190c3f23a4603cdbf8d54bc1cc488d6ee04b9fc5b3a"
25      PKG_URL="https://github.com/armbian/linux-rockchip/archive/${PKG_VERSION}.tar.gz"
26      PKG_GIT_CLONE_BRANCH="rk-6.1-rkr3"
27      PKG_PATCH_DIRS="${LINUX} ${DEVICE} default"
28      ;;
29    RK3566|RK3576|S922X)
30      PKG_VERSION="7.2.11"
31      PKG_SHA256="fd0fc479f983a8c05313f13e9c36330fe6651cf725396748c40d5cd93fa1e6a4"
32      PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
33      PKG_PATCH_DIRS+=" 7.2.6"
34      ;;
35    H700|SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)
36      PKG_VERSION="7.2"
37      PKG_SHA256="f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3"
38      PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
39      # Note that the patch dir 7.2 is automatically added as it matches the
40      # version. When we move past 7.2, remember to add 7.2 to patch dirs.
41      ;;
42    RK3326|AMD64)
43      PKG_VERSION="7.1.2"
44      PKG_SHA256="37198c93727be247c9fb5309bb86cd5e496c61e5322cd8c4eca9476bb0b5883f"
45      PKG_URL="https://www.kernel.org/pub/linux/kernel/v${PKG_VERSION/.*/}.x/${PKG_NAME}-${PKG_VERSION}.tar.xz"
46      PKG_PATCH_DIRS+=" 7.0"
47      ;;
48    RK3399)
49      PKG_VERSION="6.18.54"
50      PKG_SHA256="9df30b02dd8102bbd0be52556288ef6889ddbe7f1ddb96fbf847d0becf3eacac"
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


## scripts/mkimage @ 8ebaf8daad: lines 250-270 (excerpt)

```text
250    # copy files
251    echo "image: copying files to part1..."
252    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}"
253    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM
254    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5"
255    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5
256  
257  elif [ "${BOOTLOADER}" = "qcom-abl" ]; then
258    # create bootloader configuration
259    echo "image: creating bootloader configuration... (qcom-abl)"
260    if [ -f "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage" ]; then
261      . "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage"
262    elif [ -f "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage" ]; then
263      . "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage"
264    else
265      echo "image: skipping qcom-abl. no mkimage script found"
266    fi
267  
268    # copy files
269    echo "image: copying files to part1..."
270    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}"
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


## projects/ROCKNIX/bootloader/install @ 8ebaf8daad: lines 1-75 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  # Portable bootloader installer for ROCKNIX
 5  # Handles different bootloader types based on BOOTLOADER variable
 6  
 7  echo "install: building ROCKNIX bootloader for ${DEVICE} (${BOOTLOADER}) ..."
 8  
 9  # Ensure the bootloader directory exists
10  mkdir -p "${INSTALL}/usr/share/bootloader"
11  
12  # Handle different bootloader types
13  case "${BOOTLOADER}" in
14    syslinux)
15      echo "install: installing syslinux bootloader files"
16      if [ -d "${INSTALL}/usr/share/syslinux" ]; then
17        echo "install: copying syslinux files to bootloader location"
18        cp -av "${INSTALL}/usr/share/syslinux"/* "${INSTALL}/usr/share/bootloader/"
19      else
20        echo "install: warning - syslinux files not found in ${INSTALL}/usr/share/syslinux"
21        echo "install: this may indicate syslinux package was not built for this target"
22      fi
23      ;;
24      
25    grub)
26      echo "install: installing grub bootloader files"
27      if [ -d "${INSTALL}/usr/share/grub" ]; then
28        echo "install: copying grub files to bootloader location"
29        cp -av "${INSTALL}/usr/share/grub"/* "${INSTALL}/usr/share/bootloader/"
30      else
31        echo "install: warning - grub files not found"
32      fi
33      ;;
34      
35    systemd-boot)
36      echo "install: installing systemd-boot bootloader files"
37      if [ -d "${INSTALL}/usr/lib/systemd/boot/efi" ]; then
38        echo "install: copying systemd-boot files to bootloader location"
39        cp -av "${INSTALL}/usr/lib/systemd/boot/efi"/* "${INSTALL}/usr/share/bootloader/"
40      else
41        echo "install: warning - systemd-boot files not found"
42      fi
43      ;;
44      
45    u-boot)
46      echo "install: u-boot bootloader should be handled by device-specific bootloader scripts"
47      echo "install: skipping generic bootloader installation for u-boot"
48      ;;
49      
50    qcom-abl|arm-efi)
51      # Written into the boot partition at image time, not staged into the
52      # filesystem here: scripts/mkimage generates the config for both, and
53      # projects/ROCKNIX/bootloader/mkimage's mkimage_abl() mcopies the
54      # rocknix_abl binary in. There is nothing under /usr/share for this
55      # script to copy, which is why the generic fallback below reported
56      # every Qualcomm build as an unknown bootloader with missing files --
57      # two warnings, on five targets, for a step that had already been
58      # done correctly somewhere else.
59      echo "install: ${BOOTLOADER} is written into the boot partition at image time"
60      echo "install: skipping generic bootloader installation for ${BOOTLOADER}"
61      ;;
62      
63    "")
64      echo "install: no bootloader specified (BOOTLOADER variable empty)"
65      echo "install: skipping bootloader installation"
66      ;;
67      
68    *)
69      echo "install: unknown bootloader type: ${BOOTLOADER}"
70      echo "install: attempting to copy from ${INSTALL}/usr/share/${BOOTLOADER}"
71      if [ -d "${INSTALL}/usr/share/${BOOTLOADER}" ]; then
72        echo "install: copying ${BOOTLOADER} files to bootloader location"
73        cp -av "${INSTALL}/usr/share/${BOOTLOADER}"/* "${INSTALL}/usr/share/bootloader/"
74      else
75        echo "install: warning - ${BOOTLOADER} files not found in ${INSTALL}/usr/share/${BOOTLOADER}"
```


## distributions/ROCKNIX/config/functions @ 8ebaf8daad: lines 220-235 (excerpt)

```text
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
232  
233  get_fdt() {
234    local FDT_FILENAME=""
```


## distributions/ROCKNIX/config/functions @ 8ebaf8daad: lines 380-400 (excerpt)

```text
380  EOF
381    done
382  }
383  
384  mkimage_all() {
385    local OPTIONS_LIST=""
386  
387    if [[ -n "${SUBDEVICE}" ]]; then
388      OPTIONS_LIST=$(xmlstarlet sel -t -v "//rocknix/${DEVICE}/${SUBDEVICE}/@mkimage_options" "${CONFIGXML}" 2>/dev/null)
389    fi
390  
391    if [[ -z "${OPTIONS_LIST}" ]]; then
392      OPTIONS_LIST=$(xmlstarlet sel -t -v "//rocknix/${DEVICE}/@mkimage_options" "${CONFIGXML}" 2>/dev/null)
393    fi
394  
395    for step in $(echo "${OPTIONS_LIST}" | tr ',' ' '); do
396      local func_name="mkimage_${step}"
397  
398      "${func_name}"
399    done
400  }
```


## projects/ROCKNIX/config.xml @ 8ebaf8daad: lines 125-150 (excerpt)

```text
125      <file>sm8250-retroidpocket-rpminiv2</file>
126      <file>sm8250-ayn-thorlite</file>
127      <file>sm8250-mangmi-pocket-max</file>
128      <file>sm8250-mangmi-air-y-pro</file>
129    </SM8250>
130    <SM8550 mkimage_options="abl" dtb_prefix="qcom">
131      <file>qcs8550-ayn-odin2</file>
132      <file>qcs8550-ayn-odin2portal</file>
133      <file>qcs8550-ayn-odin2mini</file>
134      <file>qcs8550-ayn-thor</file>
135      <file>qcs8550-ayaneo-pocketace</file>
136      <file>qcs8550-ayaneo-pocketdmg</file>
137      <file>qcs8550-ayaneo-pocketevo</file>
138      <file>qcs8550-ayaneo-pocketds</file>
139      <file>qcs8550-ayaneo-pocketsmini</file>
140      <file>qcs8550-ayaneo-pockets2k</file>
141      <file>qcs8550-ayaneo-pockets1k</file>
142      <file>qcs8550-retroidpocket-rp6</file>
143      <file>qcs8550-retroidpocket-rp6-top-dpad</file>
144      <file>qcs8550-retroidpocket-rpnova</file>
145    </SM8550>
146    <SM8650 mkimage_options="abl" dtb_prefix="qcom">
147      <file>sm8650-ayaneo-ps2</file>
148      <file>sm8650-konkr-pf</file>
149    </SM8650>
150    <SM8750 mkimage_options="abl" dtb_prefix="qcom">
```


## projects/ROCKNIX/config.xml @ 651150fc88: lines 130-150 (excerpt)

```text
130      <file>sm8250-ayn-thorlite</file>
131      <file>sm8250-mangmi-pocket-max</file>
132      <file>sm8250-mangmi-air-y-pro</file>
133    </SM8250>
134    <SM8550 mkimage_options="abl,bls,dtb" dtb_prefix="qcom">
135      <file>qcs8550-ayn-odin2</file>
136      <file>qcs8550-ayn-odin2portal</file>
137      <file>qcs8550-ayn-odin2mini</file>
138      <file>qcs8550-ayn-thor</file>
139      <file>qcs8550-ayaneo-pocketace</file>
140      <file>qcs8550-ayaneo-pocketdmg</file>
141      <file>qcs8550-ayaneo-pocketevo</file>
142      <file>qcs8550-ayaneo-pocketds</file>
143      <file>qcs8550-ayaneo-pocketsmini</file>
144      <file>qcs8550-ayaneo-pockets2k</file>
145      <file>qcs8550-ayaneo-pockets1k</file>
146      <file>qcs8550-retroidpocket-rp6</file>
147      <file>qcs8550-retroidpocket-rp6-top-dpad</file>
148      <file>qcs8550-retroidpocket-rpnova</file>
149    </SM8550>
150    <SM8650 mkimage_options="abl,bls,dtb" dtb_prefix="qcom">
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


## projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl @ 8ebaf8daad: lines 1-77 (excerpt)

```text
 1  #!/bin/sh
 2  # SPDX-License-Identifier: GPL-2.0
 3  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 4  #
 5  # This script will update the ABL on the internal eMMC/UFS.
 6  
 7  . $SYSTEM_ROOT/etc/os-release
 8  
 9  case "$HW_DEVICE" in
10    SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)
11      ;;
12    *)
13      echo "This script is not compatible with this device!"
14      exit 1
15      ;;
16  esac
17  
18  # ---- Paths ----
19  ELF="$SYSTEM_ROOT/usr/share/bootloader/rocknix_abl/abl_signed-${HW_DEVICE}.elf"
20  TMP_ABL_A="/tmp/current_abl_a.bin"
21  TMP_ABL_B="/tmp/current_abl_b.bin"
22  
23  # ---- Sanity checks ----
24  if [ ! -f "${ELF}" ]; then
25    echo "Error: ABL update not found"
26    exit 1
27  fi
28  
29  $SYSTEM_ROOT/usr/sbin/partprobe
30  
31  ABL_A="$($SYSTEM_ROOT/usr/sbin/blkid -t PARTLABEL=abl_a -o device)"
32  ABL_B="$($SYSTEM_ROOT/usr/sbin/blkid -t PARTLABEL=abl_b -o device)"
33  if [ ! -b "${ABL_A}" ] || [ ! -b "${ABL_B}" ]; then
34    echo "Error: ABL partitions not found"
35    exit 1
36  fi
37  
38  # ---- Get sector size ----
39  SS="$($SYSTEM_ROOT/usr/sbin/blockdev --getss "${ABL_A}")"
40  [ -z "${SS}" ] && echo "Error: failed to get sector size" && exit 1
41  
42  
43  # ---- Determine how many sectors to read ----
44  ELF_SIZE=$($SYSTEM_ROOT/usr/bin/stat -c%s "${ELF}")
45  COUNT=$(( (ELF_SIZE + SS - 1) / SS ))
46  
47  # ---- Read current ABLs ----
48  echo "Reading ${COUNT} sectors from ABL_A..."
49  dd if="${ABL_A}" of="${TMP_ABL_A}" bs="${SS}" count="${COUNT}" status=none
50  
51  echo "Reading ${COUNT} sectors from ABL_B..."
52  dd if="${ABL_B}" of="${TMP_ABL_B}" bs="${SS}" count="${COUNT}" status=none
53  
54  # ---- Calculate checksums ----
55  SUM_A="$($SYSTEM_ROOT/usr/bin/sha256sum "${TMP_ABL_A}" | awk '{print $1}')"
56  SUM_B="$($SYSTEM_ROOT/usr/bin/sha256sum "${TMP_ABL_B}" | awk '{print $1}')"
57  SUM_UPDATE="$($SYSTEM_ROOT/usr/bin/sha256sum "${ELF}" | awk '{print $1}')"
58  
59  echo "Checksum abl_a: ${SUM_A:0:7}"
60  echo "Checksum abl_b: ${SUM_B:0:7}"
61  echo "Checksum update: ${SUM_UPDATE:0:7}"
62  
63  # ---- Compare ----
64  if [ "${SUM_A}" = "${SUM_UPDATE}" ] && [ "${SUM_B}" = "${SUM_UPDATE}" ]; then
65      echo "ABL_A and ABL_B match update version — skipping flash."
66      exit 0
67  fi
68  
69  echo "Checksums differ — flashing ABL partitions..."
70  
71  # ---- Flash ----
72  dd if="${ELF}" of="${ABL_A}" bs="${SS}" conv=fsync,notrunc status=none
73  dd if="${ELF}" of="${ABL_B}" bs="${SS}" conv=fsync,notrunc status=none
74  
75  sync
76  
77  echo "ABL update completed successfully..."
```


## projects/ROCKNIX/packages/rocknix/sources/scripts/updateabl @ 651150fc88: lines 1-89 (excerpt)

```text
 1  #!/bin/sh
 2  # SPDX-License-Identifier: GPL-2.0
 3  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 4  #
 5  # This script will update the ABL on the internal eMMC/UFS.
 6  
 7  if [ -n "$SYSTEM_ROOT" ]; then
 8    ROOT=$SYSTEM_ROOT
 9    mount --bind /dev $ROOT/dev
10    mount --bind /proc $ROOT/proc
11    mount --bind /sys $ROOT/sys
12    mount -t tmpfs tmpfs $ROOT/tmp
13    SYSTEM_ROOT="" chroot $ROOT /usr/bin/updateabl
14    RC=$?
15    umount $ROOT/tmp $ROOT/sys $ROOT/proc $ROOT/dev
16    exit $RC
17  fi
18  
19  . $SYSTEM_ROOT/etc/os-release
20  
21  case "$HW_DEVICE" in
22    SM4450|SM6115|SM8250|SM8550|SM8650|SM8750)
23      ;;
24    *)
25      echo "This script is not compatible with this device!"
26      exit 1
27      ;;
28  esac
29  
30  # ---- Paths ----
31  ELF="$SYSTEM_ROOT/usr/share/bootloader/openabl/abl_signed-${HW_DEVICE}.elf"
32  TMP_ABL_A="/tmp/current_abl_a.bin"
33  TMP_ABL_B="/tmp/current_abl_b.bin"
34  
35  # ---- Sanity checks ----
36  if [ ! -f "${ELF}" ]; then
37    echo "Error: ABL update not found"
38    exit 1
39  fi
40  
41  $SYSTEM_ROOT/usr/sbin/partprobe
42  
43  ABL_A="$($SYSTEM_ROOT/usr/sbin/blkid -t PARTLABEL=abl_a -o device)"
44  ABL_B="$($SYSTEM_ROOT/usr/sbin/blkid -t PARTLABEL=abl_b -o device)"
45  if [ ! -b "${ABL_A}" ] || [ ! -b "${ABL_B}" ]; then
46    echo "Error: ABL partitions not found"
47    exit 1
48  fi
49  
50  # ---- Get sector size ----
51  SS="$($SYSTEM_ROOT/usr/sbin/blockdev --getss "${ABL_A}")"
52  [ -z "${SS}" ] && echo "Error: failed to get sector size" && exit 1
53  
54  
55  # ---- Determine how many sectors to read ----
56  ELF_SIZE=$($SYSTEM_ROOT/usr/bin/stat -c%s "${ELF}")
57  COUNT=$(( (ELF_SIZE + SS - 1) / SS ))
58  
59  # ---- Read current ABLs ----
60  echo "Reading ${COUNT} sectors from ABL_A..."
61  dd if="${ABL_A}" of="${TMP_ABL_A}" bs="${SS}" count="${COUNT}" status=none
62  
63  echo "Reading ${COUNT} sectors from ABL_B..."
64  dd if="${ABL_B}" of="${TMP_ABL_B}" bs="${SS}" count="${COUNT}" status=none
65  
66  # ---- Calculate checksums ----
67  SUM_A="$($SYSTEM_ROOT/usr/bin/sha256sum "${TMP_ABL_A}" | awk '{print $1}')"
68  SUM_B="$($SYSTEM_ROOT/usr/bin/sha256sum "${TMP_ABL_B}" | awk '{print $1}')"
69  SUM_UPDATE="$($SYSTEM_ROOT/usr/bin/sha256sum "${ELF}" | awk '{print $1}')"
70  
71  echo "Checksum abl_a: ${SUM_A:0:7}"
72  echo "Checksum abl_b: ${SUM_B:0:7}"
73  echo "Checksum update: ${SUM_UPDATE:0:7}"
74  
75  # ---- Compare ----
76  if [ "${SUM_A}" = "${SUM_UPDATE}" ] && [ "${SUM_B}" = "${SUM_UPDATE}" ]; then
77      echo "ABL_A and ABL_B match update version — skipping flash."
78      exit 0
79  fi
80  
81  echo "Checksums differ — flashing ABL partitions..."
82  
83  # ---- Flash ----
84  dd if="${ELF}" of="${ABL_A}" bs="${SS}" conv=fsync,notrunc status=none
85  dd if="${ELF}" of="${ABL_B}" bs="${SS}" conv=fsync,notrunc status=none
86  
87  sync
88  
89  echo "ABL update completed successfully..."
```


## projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk @ 8ebaf8daad: lines 1-93 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
 3  
 4  PKG_NAME="kernel-firmware"
 5  PKG_VERSION="20260309"
 6  PKG_SHA256="28fb1b57fa9531edbd001a2462068267f10622e613abd40f952344b3f1fc5a16"
 7  PKG_LICENSE="other"
 8  PKG_SITE="https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/"
 9  PKG_URL="https://cdn.kernel.org/pub/linux/kernel/firmware/linux-firmware-${PKG_VERSION}.tar.gz"
10  PKG_NEED_UNPACK="${PROJECT_DIR}/${PROJECT}/packages/${PKG_NAME} ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/packages/${PKG_NAME}"
11  PKG_LONGDESC="kernel-firmware: kernel related firmware"
12  PKG_TOOLCHAIN="manual"
13  
14  configure_package() {
15    PKG_FW_SOURCE=${PKG_BUILD}/.copied-firmware
16  }
17  
18  post_patch() {
19    (
20      cd ${PKG_BUILD}
21  
22      # Do not run check_whence.py against the copied firmware
23      echo '#!/usr/bin/python3' > check_whence.py
24  
25      mkdir -p "${PKG_FW_SOURCE}"
26        ./copy-firmware.sh --verbose "${PKG_FW_SOURCE}"
27  
28      # copy extra firmware files (or overwrite upstream ones)
29      if [ -d ${PKG_DIR}/extra-firmware ]; then
30        cp -r ${PKG_DIR}/extra-firmware/* "${PKG_FW_SOURCE}"
31      fi
32    )
33  }
34  
35  # Install additional miscellaneous drivers
36  makeinstall_target() {
37    FW_TARGET_DIR=${INSTALL}/$(get_full_firmware_dir)
38  
39    if find_file_path config/kernel-firmware.dat; then
40      FW_LISTS="${FOUND_PATH}"
41    else
42      FW_LISTS="${PKG_DIR}/firmwares/any.dat ${PKG_DIR}/firmwares/${TARGET_ARCH}.dat"
43    fi
44  
45    FW_LISTS+=" ${PROJECT_DIR}/${PROJECT}/config/kernel-firmware-any.dat ${PROJECT_DIR}/${PROJECT}/config/kernel-firmware-${TARGET_ARCH}.dat"
46  
47    FW_LISTS+=" ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/config/kernel-firmware-any.dat ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/config/kernel-firmware-${TARGET_ARCH}.dat"
48  
49    for fwlist in ${FW_LISTS}; do
50      [ -f "${fwlist}" ] || continue
51  
52      while read -r fwline; do
53        [ -z "${fwline}" ] && continue
54        [[ ${fwline} =~ ^#.* ]] && continue
55        [[ ${fwline} =~ ^[[:space:]] ]] && continue
56  
57        eval "(cd ${PKG_FW_SOURCE} && find "${fwline}" >/dev/null)" || die "ERROR: Firmware pattern does not exist: ${fwline}"
58  
59        while read -r fwfile; do
60          [ -d "${PKG_FW_SOURCE}/${fwfile}" ] && continue
61  
62          if [ -f "${PKG_FW_SOURCE}/${fwfile}" ]; then
63            mkdir -p "$(dirname "${FW_TARGET_DIR}/${fwfile}")"
64              cp -Lv "${PKG_FW_SOURCE}/${fwfile}" "${FW_TARGET_DIR}/${fwfile}"
65          else
66            echo "ERROR: Firmware file ${fwfile} does not exist - aborting"
67            exit 1
68          fi
69        done <<<"$(cd ${PKG_FW_SOURCE} && eval "find "${fwline}"")"
70      done <"${fwlist}"
71    done
72  
73    PKG_KERNEL_CFG_FILE=$(kernel_config_path) || die
74  
75    # brcm pcie firmware is only needed by x86_64
76    [ "${TARGET_ARCH}" != "x86_64" ] && rm -fr ${FW_TARGET_DIR}/brcm/*-pcie.*
77  
78    # The BSP kernel for RK3588 reformats the vendor firmware path for Realtek BT devices,
79    # so symlink the firmware.
80    if [ ${DEVICE} = "RK3588" ]; then
81      for i in ${FW_TARGET_DIR}/rtl_bt/*.bin; do
82        ln -s "rtl_bt/$(basename ${i})" "${FW_TARGET_DIR}/$(basename ${i%.*})"
83      done
84    fi
85  
86    # Sm8250 devices need slpi firmware set to the correct dir
87    if [ ${DEVICE} = "SM8250" ]; then
88     mv ${FW_TARGET_DIR}/qcom/sm8250/Thundercomm/RB5/* ${FW_TARGET_DIR}/qcom/sm8250/
89    fi
90  
91    # Cleanup - which may be project or device specific
92    find_file_path scripts/cleanup.sh && ${FOUND_PATH} ${FW_TARGET_DIR} || true
93  }
```


## projects/ROCKNIX/packages/tools/qcom-abl/package.mk @ 8ebaf8daad: lines 1-11 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0-or-later
 2  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="qcom-abl"
 5  PKG_VERSION="1.0"
 6  PKG_LICENSE="GPL"
 7  PKG_SITE="https://rocknix.org/"
 8  PKG_URL=""
 9  PKG_DEPENDS_TARGET="toolchain"
10  PKG_SECTION="virtual"
11  PKG_LONGDESC="Meta package for installing qcom-abl kernel image"
```


## projects/ROCKNIX/packages/tools/rocknix-abl/package.mk @ 8ebaf8daad: lines 1-18 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2025 ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="rocknix-abl"
 5  PKG_VERSION="1.2"
 6  PKG_SHA256="64034fb076ea0bb858beaa2f29dbef635e97d29f3e3d32c13bce61bd4af4cff7"
 7  PKG_SITE="https://github.com/ROCKNIX/abl"
 8  PKG_URL="https://github.com/ROCKNIX/abl/releases/download/v${PKG_VERSION}/rocknix-abl-v${PKG_VERSION}.tar.gz"
 9  PKG_LONGDESC="ROCKNIX ABL."
10  PKG_TOOLCHAIN="manual"
11  
12  makeinstall_target() {
13    mkdir -p ${INSTALL}/usr/share/bootloader/rocknix_abl
14      cp -a ${PKG_BUILD}/abl_signed-${DEVICE}.elf ${INSTALL}/usr/share/bootloader/rocknix_abl/abl_signed-${DEVICE}.elf
15      cp -a ${PKG_DIR}/sources/* ${INSTALL}/usr/share/bootloader/rocknix_abl
16      mv ${INSTALL}/usr/share/bootloader/rocknix_abl/flash_abl.sh.template ${INSTALL}/usr/share/bootloader/rocknix_abl/flash_abl.sh
17      sed -i "s/%DEVICE%/${DEVICE}/g" ${INSTALL}/usr/share/bootloader/rocknix_abl/flash_abl.sh
18  }
```


## projects/ROCKNIX/packages/tools/rocknix-abl/sources/README @ 8ebaf8daad: lines 1-6 (excerpt)

```text
1  - Copy the rocknix_abl folder from the SD card to the root of Android Internal Storage
2  - Execute as root the backup_abl.sh script from the Internal Storage to backup your current ABL
3  - After backup, execute as root the flash_abl.sh script to flash the new ABL
4  - Reboot your device holding Vol - key to enter fastboot menu
5  - Select "Change boot mode" option using Vol -/+ key, and hit Power button
6  - Hit Power button to start
```


## projects/ROCKNIX/packages/tools/openabl/package.mk @ 651150fc88: lines 1-18 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="openabl"
 5  PKG_VERSION="1.2"
 6  PKG_SHA256="28cb97d1b387f28ddba28ed57fdc7d8b1c2ac2cdcd26af9c672620d41abddd4f"
 7  PKG_SITE="https://github.com/OpenHandheldCollective/OpenABL"
 8  PKG_URL="https://github.com/OpenHandheldCollective/OpenABL/releases/download/v${PKG_VERSION}/openabl-v${PKG_VERSION}.tar.gz"
 9  PKG_LONGDESC="OpenABL: an open-source alternative boot loader for Qualcomm devices"
10  PKG_TOOLCHAIN="manual"
11  
12  makeinstall_target() {
13    mkdir -p ${INSTALL}/usr/share/bootloader/openabl
14      cp -a ${PKG_BUILD}/${DEVICE}/abl_signed-${DEVICE}.elf ${INSTALL}/usr/share/bootloader/openabl/abl_signed-${DEVICE}.elf
15      cp -a ${PKG_DIR}/sources/{backup_abl.sh,flash_abl.sh.template,restore_backup_abl.sh} ${INSTALL}/usr/share/bootloader/openabl
16      mv ${INSTALL}/usr/share/bootloader/openabl/flash_abl.sh.template ${INSTALL}/usr/share/bootloader/openabl/flash_abl.sh
17      sed -i "s/%DEVICE%/${DEVICE}/g" ${INSTALL}/usr/share/bootloader/openabl/flash_abl.sh
18  }
```


## projects/ROCKNIX/packages/tools/mkbootimg/package.mk @ 8ebaf8daad: lines 1-18 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2025-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="mkbootimg"
 5  PKG_VERSION="d2bb0af5ba6d3198a3e99529c97eda1be0b5a093"
 6  PKG_SHA256="418bb875c03d5c5844d6d289956d8294ae6a2bd5be78c7d912d797e7826ca3d9"
 7  PKG_LICENSE="GPL"
 8  PKG_SITE="https://android.googlesource.com/platform/system/tools/mkbootimg"
 9  PKG_URL="https://github.com/jbeich/platform_system_tools_mkbootimg/archive/${PKG_VERSION}.tar.gz"
10  PKG_LONGDESC="mkbootimg: Creates kernel boot images for Android"
11  PKG_TOOLCHAIN="manual"
12  PKG_DEPENDS_HOST="toolchain Python3:host"
13  
14  makeinstall_host() {
15    mkdir -p ${TOOLCHAIN}/mkbootimg
16      cp -a gki/ mkbootimg.py $TOOLCHAIN/mkbootimg
17  }
```


## projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk @ 8ebaf8daad: lines 1-25 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="extra-firmware"
 5  PKG_VERSION="88b363e67d4f730feb2c3124724d26dfaa88ce76"
 6  PKG_SHA256="1b253d1a79ed9dc6fb6389be804197bb27f11097b0e7146065d0141ea99b2d25"
 7  PKG_LICENSE="proprietary"
 8  PKG_SITE="https://github.com/ROCKNIX/extra-firmware"
 9  PKG_URL="https://github.com/ROCKNIX/extra-firmware/archive/${PKG_VERSION}.tar.gz"
10  PKG_LONGDESC="extra-firmware: Extra kernel firmware needed for ROCKNIX devices"
11  PKG_TOOLCHAIN="manual"
12  
13  makeinstall_target() {
14    mkdir -p ${INSTALL}/$(get_full_firmware_dir)
15  
16    case "${DEVICE}" in
17      "SM4450") cp -a SM4450/* ${INSTALL}/$(get_full_firmware_dir) ;;
18      "SM6115") cp -a SM6115/* ${INSTALL}/$(get_full_firmware_dir) ;;
19      "SM8250") cp -a SM8250/* ${INSTALL}/$(get_full_firmware_dir) ;;
20      "SM8550") cp -a SM8550/* ${INSTALL}/$(get_full_firmware_dir) ;;
21      "SM8650") cp -a SM8650/* ${INSTALL}/$(get_full_firmware_dir) ;;
22      "SM8750") cp -a SM8750/* ${INSTALL}/$(get_full_firmware_dir) ;;
23      "RK3566") cp -a RK3566/* ${INSTALL}/$(get_full_firmware_dir) ;;
24    esac
25  }
```


## projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk @ 651150fc88: lines 1-25 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="extra-firmware"
 5  PKG_VERSION="925dfb5efbe5d6c3ca654f81e3e1f367f8492777"
 6  PKG_SHA256="b994fa1c451708bc7addd256e68e0a872559e54e4ddec27f73e6197d64aefc0c"
 7  PKG_LICENSE="proprietary"
 8  PKG_SITE="https://github.com/ROCKNIX/extra-firmware"
 9  PKG_URL="https://github.com/ROCKNIX/extra-firmware/archive/${PKG_VERSION}.tar.gz"
10  PKG_LONGDESC="extra-firmware: Extra kernel firmware needed for ROCKNIX devices"
11  PKG_TOOLCHAIN="manual"
12  
13  makeinstall_target() {
14    mkdir -p ${INSTALL}/$(get_full_firmware_dir)
15  
16    case "${DEVICE}" in
17      "SM4450") cp -a SM4450/* ${INSTALL}/$(get_full_firmware_dir) ;;
18      "SM6115") cp -a SM6115/* ${INSTALL}/$(get_full_firmware_dir) ;;
19      "SM8250") cp -a SM8250/* ${INSTALL}/$(get_full_firmware_dir) ;;
20      "SM8550") cp -a SM8550/* ${INSTALL}/$(get_full_firmware_dir) ;;
21      "SM8650") cp -a SM8650/* ${INSTALL}/$(get_full_firmware_dir) ;;
22      "SM8750") cp -a SM8750/* ${INSTALL}/$(get_full_firmware_dir) ;;
23      "RK3566") cp -a RK3566/* ${INSTALL}/$(get_full_firmware_dir) ;;
24    esac
25  }
```


## projects/ROCKNIX/packages/tools/inputplumber/package.mk @ 8ebaf8daad: lines 1-49 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2025 ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="inputplumber"
 5  PKG_VERSION="v0.79.0"
 6  PKG_SHA256="123c858139d3b78e3f075158ce16b8fdc8067a10e31a93cb1e7f2aea816106bd"
 7  PKG_LICENSE="GPLv3"
 8  PKG_SITE="https://github.com/ShadowBlip/InputPlumber"
 9  PKG_URL="https://github.com/ShadowBlip/InputPlumber/releases/download/${PKG_VERSION}/inputplumber-aarch64.tar.gz"
10  PKG_DEPENDS_TARGET="toolchain systemd libevdev libiio polkit"
11  PKG_LONGDESC="Open source input router and remapper daemon for Linux"
12  PKG_TOOLCHAIN="manual"
13  
14  # Upstream composite device configs for the handhelds we support ourselves.
15  # Our own configs (projects/ROCKNIX/devices/*/filesystem/usr/share/inputplumber)
16  # match the same hardware but map it to a DualSense target, so the upstream
17  # files would compete for the same source devices. Drop them.
18  PKG_DROP_DEVICE_CONFIGS="
19    50-ayaneo_pocket_s2.yaml
20    50-ayn_odin2.yaml
21    50-ayn_odin2_mini.yaml
22    50-ayn_odin3.yaml
23    50-ayn_thor.yaml
24    50-konkr_pocket_fit.yaml
25    50-konkr_pocket_fit_elite.yaml
26    50-retroid_pocket5.yaml
27    50-retroid_pocket6.yaml
28    50-retroid_pocket_flip2.yaml
29    50-retroid_pocket_mini.yaml
30    50-retroid_pocket_nova.yaml
31  "
32  
33  post_unpack() {
34    for config in ${PKG_DROP_DEVICE_CONFIGS}; do
35      rm -f ${PKG_BUILD}/usr/share/inputplumber/devices/${config}
36    done
37  }
38  
39  makeinstall_target() {
40    mkdir -p ${INSTALL}/usr
41    rsync -ar ${PKG_BUILD}/usr/ ${INSTALL}/usr/
42  
43    # sources/ is overlaid with cp, so pin the mode udev needs to run the shim.
44    chmod 0755 ${INSTALL}/usr/lib/inputplumber/setfacl-shim/setfacl
45  }
46  
47  post_install() {
48    enable_service inputplumber.service
49  }
```


## projects/ROCKNIX/packages/tools/inputplumber/package.mk @ 651150fc88: lines 1-60 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2025 ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="inputplumber"
 5  PKG_VERSION="0.82.0"
 6  PKG_SHA256="aaee9b65b47a21756169eb1c49eb258ecdd1896fb8dd4996c2b50d11af049d21"
 7  PKG_LICENSE="GPLv3"
 8  PKG_SITE="https://github.com/ShadowBlip/InputPlumber"
 9  PKG_URL="${PKG_SITE}/archive/refs/tags/v${PKG_VERSION}.tar.gz"
10  PKG_DEPENDS_TARGET="toolchain cargo:host cargo rust llvm:host systemd libevdev libiio polkit"
11  PKG_LONGDESC="Open source input router and remapper daemon for Linux"
12  PKG_TOOLCHAIN="manual"
13  
14  # Upstream composite device configs for the handhelds we support ourselves.
15  # Our own configs (projects/ROCKNIX/devices/*/filesystem/usr/share/inputplumber)
16  # match the same hardware but map it to a DualSense target, so the upstream
17  # files would compete for the same source devices. Drop them.
18  PKG_DROP_DEVICE_CONFIGS="
19    50-ayaneo_pocket_s2.yaml
20    50-ayaneo_pocket_ds.yaml
21    50-ayn_odin2.yaml
22    50-ayn_odin2_mini.yaml
23    50-ayn_odin3.yaml
24    50-ayn_thor.yaml
25    50-ayn_thor_lite.yaml
26    50-konkr_pocket_fit.yaml
27    50-konkr_pocket_fit_elite.yaml
28    50-retroid_pocket5.yaml
29    50-retroid_pocket6.yaml
30    50-retroid_pocket_flip2.yaml
31    50-retroid_pocket_mini.yaml
32    50-retroid_pocket_nova.yaml
33  "
34  
35  post_unpack() {
36    for config in ${PKG_DROP_DEVICE_CONFIGS}; do
37      rm -f ${PKG_BUILD}/rootfs/usr/share/inputplumber/devices/${config}
38    done
39  }
40  
41  make_target() {
42    export LIBCLANG_PATH=${TOOLCHAIN}/lib
43    export LD_LIBRARY_PATH=${TOOLCHAIN}/lib:${LD_LIBRARY_PATH}
44    export BINDGEN_EXTRA_CLANG_ARGS="--sysroot=${SYSROOT_PREFIX} -isystem ${SYSROOT_PREFIX}/usr/include"
45  
46    cargo build \
47      --target ${TARGET_NAME} \
48      --release
49  }
50  
51  makeinstall_target() {
52    mkdir -p ${INSTALL}/usr/bin
53    cp ${PKG_BUILD}/.${TARGET_NAME}/target/${TARGET_NAME}/release/inputplumber ${INSTALL}/usr/bin/
54  
55    mkdir -p ${INSTALL}/usr
56    rsync -ar ${PKG_BUILD}/rootfs/usr/ ${INSTALL}/usr/
57  
58    # sources/ is overlaid with cp, so pin the mode udev needs to run the shim.
59    chmod 0755 ${INSTALL}/usr/lib/inputplumber/setfacl-shim/setfacl
60  }
```


## projects/ROCKNIX/packages/tools/gamepadcalibration/package.mk @ 8ebaf8daad: lines 1-40 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0-or-later
 2  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="gamepadcalibration"
 5  PKG_VERSION="2077e7af7e9a8c1df54af6f1959cb92daea03207"
 6  PKG_SHA256="f14730170a41ec183a203bdad98e5acd089ab59cd580cd0235a5eda39759b677"
 7  PKG_LICENSE="MIT"
 8  PKG_SITE="https://github.com/cdeletre/GPcal"
 9  PKG_URL="https://github.com/cdeletre/GPcal/archive/${PKG_VERSION}.tar.gz"
10  PKG_DEPENDS_TARGET="Python3 SDL2 gamecontrollerdb pyxel"
11  PKG_LONGDESC="A gamepad calibration tool for the Retroid Pocket 5 and Mini"
12  PKG_TOOLCHAIN="manual"
13  
14  makeinstall_target() {
15    mkdir -p ${INSTALL}/usr/local/share
16      tar -xzf ${PKG_BUILD}/rocknix/gpcal-python-3.13.tgz -C ${INSTALL}/usr/local/share
17      rm -rf ${INSTALL}/usr/local/share/gpcal/pyxel
18  
19    case ${DEVICE} in
20      SM8250)
21        sed -i 's|^PARAMETERS_DIR_PATH=.*|import os\nPARAMETERS_DIR_PATH = "/sys/module/mangmi_pocket_max/parameters" if os.path.exists("/sys/module/mangmi_pocket_max/parameters") else "/sys/module/retroid/parameters"|' \
22          ${INSTALL}/usr/local/share/gpcal/Klib/RPocket.py
23        sed -i 's|^GAMEPAD_NAME=.*|from Klib.RPocket import PARAMETERS_DIR_PATH\nGAMEPAD_NAME = "MANGMI Pocket Max Joypad" if "mangmi" in PARAMETERS_DIR_PATH else "Retroid Pocket Gamepad"|' \
24          ${INSTALL}/usr/local/share/gpcal/Klib/PyxUI.py
25        ;;
26      SM8550|SM8750)
27        sed -i 's|/sys/module/retroid/parameters|/sys/module/rsinput/parameters|g' ${INSTALL}/usr/local/share/gpcal/Klib/RPocket.py
28        ;;
29      SM6115)
30        sed -i 's|/sys/module/retroid/parameters|/sys/module/mangmi/parameters|g' ${INSTALL}/usr/local/share/gpcal/Klib/RPocket.py
31        ;;
32    esac
33  
34    # restart inputplumber after the driver re-reads the calibration
35    sed -i '/echo 1 > .*update_params/a\
36              savefile.write("sleep 0.5\\n")\
37              savefile.write("# Restart InputPlumber\\n")\
38              savefile.write("systemctl restart inputplumber\\n")
39  ' ${INSTALL}/usr/local/share/gpcal/Klib/RPocket.py
```


## projects/ROCKNIX/devices/SM8550/bootloader/update.sh @ 651150fc88: lines 1-43 (excerpt)

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
12      /dev/mmcblk*) BOOT_DISK=$(echo $BOOT_PART | sed -e "s,p[0-9]*,,g");;
13    esac
14  fi
15  
16  # mount $BOOT_ROOT rw
17  mount -o remount,rw $BOOT_ROOT
18  
19  if [ -d $SYSTEM_ROOT/usr/share/bootloader/dtbs ]; then
20    echo "Updating device trees..."
21    mkdir -p $BOOT_ROOT/dtbs
22    cp -f $SYSTEM_ROOT/usr/share/bootloader/dtbs/* $BOOT_ROOT/dtbs
23  fi
24  
25  if [ -d "$SYSTEM_ROOT/usr/share/bootloader/loader" ]; then
26    echo "Updating BLS configuration..."
27    mkdir -p $BOOT_ROOT/loader
28    cp -r $SYSTEM_ROOT/usr/share/bootloader/loader/* $BOOT_ROOT/loader
29  fi
30  
31  if [ -d "$SYSTEM_ROOT/usr/share/bootloader/openabl" ]; then
32    mkdir -p $BOOT_ROOT/openabl
33    echo "Updating OpenABL on SD..."
34    cp $SYSTEM_ROOT/usr/share/bootloader/openabl/* $BOOT_ROOT/openabl
35  fi
36  
37  $SYSTEM_ROOT/usr/bin/updateabl
38  
39  # mount $BOOT_ROOT ro
40  sync
41  mount -o remount,ro $BOOT_ROOT
42  
43  echo "UPDATE" > /storage/.boot.hint
```


## projects/ROCKNIX/devices/SM8550/options @ 651150fc88: lines 1-81 (excerpt)

```text
 1  ################################################################################
 2  # setup device defaults
 3  ################################################################################
 4  
 5    # The TARGET_CPU variable controls which processor should be targeted for
 6    # generated code.
 7      case ${TARGET_ARCH} in
 8        aarch64)
 9          TARGET_CPU="cortex-x3"
10          TARGET_CPU_FLAGS="+fp16+crypto+i8mm+bf16+memtag+sm4+sha3+nosve+nosve2"
11          ;;
12        arm)
13          TARGET_KERNEL_ARCH="arm64"
14          TARGET_FLOAT="hard"
15          TARGET_CPU="cortex-a710"
16          TARGET_CPU_FLAGS="+fp16+crypto+i8mm+bf16"
17          TARGET_FPU="crypto-neon-fp-armv8"
18          ;;
19      esac
20  
21      PARTITION_TABLE="gpt"
22      HW_CPU="Snapdragon 8 Gen 2"
23  
24    # Kernel target
25      KERNEL_TARGET="Image"
26  
27    # Additional kernel make parameters (for example to specify the u-boot loadaddress)
28      KERNEL_MAKE_EXTRACMD=" $(get_kernel_make_extracmd)"
29  
30    # Kernel cmdline
31      EXTRA_CMDLINE="quiet rootwait console=tty0 allow_mismatched_32bit_el0 fw_devlink.strict=1 pcie_ports=compat irqaffinity=0-2 cgroup.memory=nokmem,nosocket nosoftlockup usbcore.interrupt_interval_override=045e:028e:2 gpt"
32  
33    # Bootloader to use (syslinux / u-boot)
34      BOOTLOADER="arm-efi"
35  
36    # Adreno GPU family
37      GRAPHIC_DRIVERS="freedreno"
38  
39    # For maximum cross compatbility
40      PREFER_GLES="no"
41  
42    # VULKAN_SUPPORT
43      VULKAN_SUPPORT="yes"
44  
45    # Vulkan implementation to use (vulkan-loader / no)
46      VULKAN="vulkan-loader"
47  
48    # Displayserver to use (wl / no)
49      DISPLAYSERVER="wl"
50  
51    # Windowmanager to use (weston / swaywm-env / no)
52      WINDOWMANAGER="swaywm-env"
53  
54    # Additional drivers to install:
55    # for a list of additional drivers see packages/linux-drivers
56    # Space separated list is supported,
57    # e.g. ADDITIONAL_DRIVERS="DRIVER1 DRIVER2"
58      ADDITIONAL_DRIVERS=""
59  
60    # Additional Firmware to use ( )
61    # Space separated list is supported,
62    # e.g. FIRMWARE=""
63      FIRMWARE="extra-firmware"
64  
65    # Additional packages to install
66      ADDITIONAL_PACKAGES="gamepadcalibration openabl inputplumber"
67  
68    # Debug tty path
69      DEBUG_TTY="/dev/ttyMSM0"
70  
71    # Build and install rocknix joypad driver (yes / no)
72      ROCKNIX_JOYPAD="no"
73  
74    # ZRAM Algorithm
75      ZRAM_COMPRESSION_ALGO="zstd"
76  
77    # ZRAM Size
78      ZRAM_SWAP_SIZE="Auto"
79  
80    # Disk Swap
81      SWAP_FILE_SIZE="0"
```


## projects/ROCKNIX/packages/virtual/arm-efi/package.mk @ 651150fc88: lines 1-23 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="arm-efi"
 5  PKG_VERSION="1.0"
 6  PKG_LICENSE="GPL"
 7  PKG_SITE="https://rocknix.org/"
 8  PKG_URL=""
 9  PKG_DEPENDS_TARGET="toolchain"
10  PKG_SECTION="virtual"
11  PKG_LONGDESC="Meta package for installing arm-efi bootloader"
12  
13  post_install() {
14    BLS_PATH="${INSTALL}/usr/share/bootloader/loader/entries"
15  
16    mkdir -p "${BLS_PATH}"
17    cat << EOF > "${BLS_PATH}/${DISTRONAME,,}.conf"
18  title      ${DISTRONAME}
19  version    ${OS_VERSION}
20  linux      /${KERNEL_NAME}
21  options    boot=LABEL=${DISTRO_BOOTLABEL} disk=LABEL=${DISTRO_DISKLABEL} ${EXTRA_CMDLINE}
22  EOF
23  }
```


## distributions/ROCKNIX/options @ 8ebaf8daad: lines 14-20 (excerpt)

```text
14    GIT_REPO="distribution"
15  
16  # Name of the Distro to build (full name, without special characters)
17    DISTRONAME="pixelelated"
18  
19  # Name of the OS to build (full name, lower case, without special characters)
20    OSNAME="rocknix"
```


## distributions/ROCKNIX/options @ 8ebaf8daad: lines 198-206 (excerpt)

```text
198  # Default supported get handlers (archive, git, file etc.)
199    GET_HANDLER_SUPPORT="${GET_HANDLER_SUPPORT:-archive git file}"
200  
201  # Partition labels for USB/SD installation media
202    DISTRO_BOOTLABEL="ROCKNIX"
203    DISTRO_DISKLABEL="STORAGE"
204  
205  # Settings package name - blank if not required
206    DISTRO_PKG_SETTINGS=""
```


## projects/ROCKNIX/packages/sysutils/autostart/profile.d/002-autostart @ 8ebaf8daad: lines 1-12 (excerpt)

```text
 1  #!/bin/bash
 2  # SPDX-License-Identifier: GPL-2.0
 3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
 4  
 5  ### Apply device quirks
 6  if [ -e "/sys/firmware/devicetree/base/model" ]
 7  then
 8    export QUIRK_DEVICE="$(strings /sys/firmware/devicetree/base/model)"
 9  else
10    export QUIRK_DEVICE="$(strings /sys/class/dmi/id/sys_vendor) $(strings /sys/class/dmi/id/product_name)"
11  fi
12  export QUIRK_DEVICE="$(echo ${QUIRK_DEVICE} | sed -e "s#[/]#-#g")"
```
