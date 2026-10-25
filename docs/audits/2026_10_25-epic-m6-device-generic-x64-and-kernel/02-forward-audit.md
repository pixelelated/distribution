# Forward audit — M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

- **`reviewed-at`:** `2103f0271d`. The 58 are read at `8ebaf8daad`'s bytes (`git diff --stat 8ebaf8daad 2103f0271d -- <the 58>` is empty). Upstream is `651150fc88`, read locally.
- **Can this be done on the VM? Yes -- on the host, with no network.** Every read, diff, log and branch read runs on the build host at `8ebaf8daad`. The guest whose boot and harness T12 (#659) recorded is the device read here; no guest cycle was needed. No handheld.
- **Built artefacts read, not made** (accepted as evidence by the coordinator, 07:10 UTC on #658: the recipe-only statement is primary, and the measurement is its corroboration). Three facts were read, read-only, from the M7 lane's existing GENERIC_X64 build roots: the built kernel configuration, the installed firmware tree, and the bzImage's size. Their provenance is § The configuration's *Provenance of the corroboration*. Nothing was written in those trees and no process was started there.
- **The runs** are `/workspace/tmp/m6-t11/runner/runs.sh`, 28 steps with exit and wall time (§ The runs). Their outputs are copied to `stage-b/`.

## Phase 2 — #658's checklist at stage B

| Criterion (#658 § Acceptance) | State at stage B | Artifact |
| --- | --- | --- |
| `00` and `01` to `05` | `00`, `01`, `02`, `03`, `04` written; `05` at stage D | this folder |
| The lint | `--phase pre-issue` at stage C | — |
| `review-plan.json`, provenance, packet manifest | the plan written; the seat at stage C | `second-opinions/review-plan.json` |
| The punch-list issue at outcomes | stage D onward | — |
| `reviewed-at`, `fixed-at`, the empty diffs | `reviewed-at` `2103f0271d`; r22 empty under `packages/`, `projects/`, `tools/` | § The runs r22 |
| `01` § Scope | written at stage A | `01-research-notes.md` |
| `## Coverage`, 58 rows | 58 | below |
| § The configuration, three parts | written | below |
| § The boot files, one row per script | written | below |
| § The launcher | written, the resolution as the coordinator accepted it (06:47 UTC, #658) | below |
| § The runs | 28 runs with exit, wall time and the FAIL each guards | below |
| `00` shows no guest, build, fetch or extra invoke | so far | `00-running-log.md` |
| `04` Q1, Q2, Q3, Q6, § Second opinion | Q1 to Q7 written; the second opinion at stage C | `04-analysis.md` |
| `proved:` cells; `question:` per punch item | the proofs here; punch items at stage D | § Proofs |
| The retro | stage G | — |
| The checkers | stage H | — |

## Coverage

One row per path of the 58, in the inventory's order. *Reach* is the inventory's column at `2174265e9c`; *Read* marks the 14 read files with their lines.

| Path | Tier | Reach | Read | What it is, and who reads it | Finding or disposition | proved |
| --- | --- | --- | --- | --- | --- | --- |
| `projects/ROCKNIX/bootloader/install` | fork-own | shipped | 80 | `scripts/image:280` sources it for every device (`find_file_path`; no package carries its own, so nothing is shadowed). Branches: `syslinux` does work for GENERIC_X64; `u-boot` (H700) and `qcom-abl` (SM8550) echo by design (`:45-61`); `grub`, `systemd-boot`, `""` and `*)` are reached by no device. Fork-only (`73b20caf86`, `7178f1b1f3`). | F-03 (header), F-05 (unread copy), F-06 (unreached branches) | tree |
| `projects/ROCKNIX/bootloader/mkimage` | upstream-carried | shipped | 113 | Sourced by `scripts/mkimage:225-263` for `u-boot`, `arm-efi` and `qcom-abl` when the device has no own `bootloader/mkimage`: H700 and SM8550 reach it; GENERIC_X64's syslinux path does not (`scripts/mkimage:142-180`). Upstream rewrote its SM branches at `651150fc88` (bls/dtb). | carried; the upstream rewrite is T25's and T28's (F-09) | tree |
| `projects/ROCKNIX/bootloader/release` | upstream-carried | shipped | 5 | `scripts/image:285`, every device: `cp -a ${INSTALL}/usr/share/bootloader/*` into `3rdparty/bootloader`. The glob has sources on all three shipped devices (H700 u-boot and dtbs; SM8550 `rocknix-abl` and the `rocknix` package; GENERIC_X64 `install`'s syslinux copy). | carried; no finding | tree |
| `projects/ROCKNIX/bootloader/rkhelper` | upstream-carried | shipped | 60 | Read by seven Rockchip u-boot recipes (RK3326 x2, RK3399, RK3566 x2, RK3576, RK3588) through `find_file_path bootloader/rkhelper`; no shipped device. The inventory's `shipped` is directory-level. | F-08 (inventory reach); carried for ROCKNIX's Rockchip devices | tree |
| `projects/ROCKNIX/config.xml` | upstream-carried | shipped | 154 | Read by the image step's `mkimage` for u-boot/abl devices: H700 (`:2`) and SM8550 (`:130`); GENERIC_X64 has no entry and its syslinux path reads none. Upstream changed the SM entries at `651150fc88`. | carried; the upstream change is T28's (F-09) | tree |
| `projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/sway/sway-generic-x64` | fork-own | test | read (40) | The compositor wrapper the drop-in below starts: Pixman only for a virtio GPU without virgl (`:26-35`), then `exec /usr/bin/sway.sh`. Fork-own, GENERIC_X64 only. | positive (P17); no finding | tree |
| `projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/systemd/system/serial-debug-shell.service` | fork-own | test | read (41) | The developers' root shell on ttyS0, gated `ConditionVirtualization=vm` and the console argument (`:18-20`); D-QA-053 keeps it and the unit says so (`:4-14`). | positive; no finding | tree |
| `projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf` | fork-own | test | 3 | Replaces sway's `ExecStart` with the wrapper above (`:2-3`). | no finding | tree |
| `projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf` | vendor-carried | test | 7754 | The guest's kernel configuration: header `Linux/x86 6.15.6` (`:3`); the recipe builds 7.1.2 and runs `oldconfig` over it (`package.mk:306`, `:315`). Nearest base the Generic conf (659 / 351). The fork's 13 lines survive the build; 18 values, 97 set and 137 new options differ in the built file. | F-04 (provenance; the regeneration packet), F-02 (embedded firmware and the GPU drivers it carries) | tool-run |
| `projects/ROCKNIX/devices/GENERIC_X64/options` | fork-own | test | read (91) | Device knobs: `x86-64-v3` (`:15`), `BOOTLOADER="syslinux"` (`:27`), virtio/vmware GL (`:36`), `SWAP_SUPPORT="no"` (`:86`), serial console (`:76`), `INSTALLER_SUPPORT="yes"` (`:91`). No line says why syslinux or where the kernel configuration came from. | Q7 (F-10) | tree |
| `projects/ROCKNIX/devices/GENERIC_X64/vm/README.md` | fork-own | test | 138 | The profile's guide for Linux/QEMU and macOS/UTM: the UTM bundle, networking, the loopback ssh cloud route (`:92-121`), a UTM bridged-mode workaround (`:123-138`). | F-07 (the UTM text after D-QA-053) | tree |
| `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm` | fork-own | test | read (817) | The launcher (817 lines, 19 functions): `profile`, `qemu-args`, `run`, `utm` (`:785-795`). Run by `tools/vm-pair:74` through `VM_TOOL` (`:36`); no other tool runs it. | § The launcher; design sentence deferred | tree |
| `projects/ROCKNIX/devices/GENERIC_X64/vm/profile.json` | fork-own | test | 52 | The canonical guest: q35, Haswell-v4, 4 CPUs, 8 GiB, UEFI, 16 GiB virtio-blk, virtio-gpu-gl, virtio-net with the fw_cfg ssh port, intel-hda. Read by the launcher (`:26`, `:47-48`). | positive; no finding | tree |
| `projects/ROCKNIX/devices/GENERIC_X64/vm/utm-bundle-readme.txt` | fork-own | test | 35 | Packed into the `utm` bundle; teaches the ssh + `rclone config` cloud route on a Mac. | F-07 | tree |
| `projects/ROCKNIX/filesystem/etc/machine-info` | fork-own | shipped | 9 | `CHASSIS=handset` on every image (`98e1a30362`); WebKitGTK and hostnamed read it, the guest included so its frames are the handheld's (`:1-8`). | positive; nine lines, no cost (Q5) | tree |
| `projects/ROCKNIX/options` | upstream-carried | shipped | read (41) | Project defaults (`SQUASHFS_COMPRESSION="zstd"`, `SWAP_SUPPORT="yes"`, ...); every device's options override. | carried; no finding | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/package.mk` | upstream-carried | shipped | read (26) | Compiles `${PKG_BUILD}/${DEVICE}/*.dts` and installs the `.dtbo`s and `dtb_overlay` (`:8-19`): on our devices only H700's source compiles. | carried; no finding | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/H700/sun50i-h700-anbernic-rg35xx-2024-ddr3.dts` | upstream-carried | shipped | 12 | H700's DDR3 overlay; the only source that compiles on a shipped device. | carried; no finding | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/RK3566/rk3566-undervolt-cpu-l1.dts` | upstream-carried | shipped | 35 | Compiled only when `DEVICE` names its directory; no shipped device does. The inventory lists it under H700 (package-level reach). | F-08 (inventory reach); carried for ROCKNIX's devices | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/RK3566/rk3566-undervolt-cpu-l2.dts` | upstream-carried | shipped | 35 | Compiled only when `DEVICE` names its directory; no shipped device does. The inventory lists it under H700 (package-level reach). | F-08 (inventory reach); carried for ROCKNIX's devices | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/RK3566/rk3566-undervolt-cpu-l3.dts` | upstream-carried | shipped | 35 | Compiled only when `DEVICE` names its directory; no shipped device does. The inventory lists it under H700 (package-level reach). | F-08 (inventory reach); carried for ROCKNIX's devices | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/RK3588/driver-gpu-panthor.dts` | upstream-carried | shipped | 19 | Compiled only when `DEVICE` names its directory; no shipped device does. The inventory lists it under H700 (package-level reach). | F-08 (inventory reach); carried for ROCKNIX's devices | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/S922X/driver-gpu-panfrost.dts` | upstream-carried | shipped | 18 | Compiled only when `DEVICE` names its directory; no shipped device does. The inventory lists it under H700 (package-level reach). | F-08 (inventory reach); carried for ROCKNIX's devices | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/S922X/gpu-underclock.dts` | upstream-carried | shipped | 14 | Compiled only when `DEVICE` names its directory; no shipped device does. The inventory lists it under H700 (package-level reach). | F-08 (inventory reach); carried for ROCKNIX's devices | tree |
| `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/dtb_overlay` | upstream-carried | shipped | read (163) | The overlay helper installed on every device but RK3326 that builds the package (H700 here). | carried; no finding | tree |
| `projects/ROCKNIX/packages/linux-drivers/rocknix-joypad/package.mk` | upstream-carried | shipped | read (25) | The joypad module; H700 builds it, GENERIC_X64 sets `ROCKNIX_JOYPAD="no"` (`options:79`). Upstream moved it to `hackbar/rocknix-joypad` `005033d1dd` at `651150fc88`. | Q4: behind upstream; the next merge brings it (T25) | tree |
| `projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk` | upstream-carried | shipped | read (25) | Copies `SM8550/*` for SM8550 (`:13-21`); nothing for H700 or GENERIC_X64. Upstream at `925dfb5efb`. | Q4: behind upstream; the next merge brings it (T25) | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/cirrus/cs35l41-dsp1-spk-cali.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/cirrus/cs35l41-dsp1-spk-cali.wmfw` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/cirrus/cs35l41-dsp1-spk-prot.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/cirrus/cs35l41-dsp1-spk-prot.wmfw` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg28xx-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg34xx-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg34xx-sp-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg34xx-sp-v2-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg35xx-plus-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg35xx-plus-rev6-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg35xx-sp-v2-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg40xx-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rg40xx-v2-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/panels/anbernic,rgcubexx-panel.panel` | upstream-carried | shipped | binary | An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`. | carried; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/rtl_bt/rtl8723ds_config.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/rtl_bt/rtl8723ds_fw.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/rtl_bt/rtl8723fu_config.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/rtl_bt/rtl8723fu_fw.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/rtl_bt/rtl8761b_config.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/rtl_bt/rtl8761b_fw.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/rtl_bt/rtl8852bs_config.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/extra-firmware/rtl_bt/rtl8852bs_fw.bin` | upstream-carried | shipped | binary | Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device). | carried for ROCKNIX's devices; the guest copy is F-01's | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/firmwares/any.dat` | upstream-carried | shipped | 24 | The aarch64 fallback list; H700 and SM8550 carry their own `config/kernel-firmware.dat`, so it reaches neither. | carried; no finding | tree |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/firmwares/x86_64.dat` | upstream-carried | shipped | 1 | One line, `*`: the x86_64 fallback. GENERIC_X64 has no own list, so it installs all of linux-firmware: 6,158 files, 2,876,913,748 bytes in the M7 build root. | F-01 | tool-run |
| `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk` | upstream-carried | shipped | read (93) | Copies linux-firmware 20260309 plus `extra-firmware/` into `.copied-firmware`, then installs what the device's list (or the arch fallback) names (`makeinstall_target`). | F-01 (GENERIC_X64's fallback); F-17's stamp gap (T5 E6) bears on any new list | tree |
| `projects/ROCKNIX/packages/linux/package.mk` | fork-own | shipped | read (432) | The override kernel recipe: GENERIC_X64 7.1.2 (`:36-40`), the x86 firmware block (`:197-207`), `listnewconfig`/`oldconfig` (`:306-316`), the `.config` copied into `.image` (`:385`). Fork-own by `dc948f59aa` and `3d7c075f63`. | F-02, F-04; Q4 | tree |
| `projects/ROCKNIX/packages/linux/sysctl.d/network.conf` | upstream-carried | shipped | 1 | `net.ipv4.tcp_no_metrics_save=1`, every device. | carried; no finding | tree |
| `projects/ROCKNIX/packages/linux/sysctl.d/qdisc.conf` | upstream-carried | shipped | 1 | `net.core.default_qdisc = fq_codel`, every device; upstream drops the line at `651150fc88`. | carried; the upstream change is T25's | tree |
| `projects/ROCKNIX/packages/linux/udev.d/10-bfq-sched.rules` | upstream-carried | shipped | read (1) | bfq on `mmcbl*`; upstream narrows it to whole disks at `651150fc88`. The guest's virtio-blk is not `mmcbl*`. | carried; the upstream change is T25's | tree |
| `projects/ROCKNIX/packages/linux/udev.d/30-disable-wakeup.rules` | upstream-carried | shipped | read (9) | Disables USB host controllers' wakeup (`ehci-pci|xhci_hcd`). | carried; no finding | tree |
| `projects/ROCKNIX/packages/linux/udev.d/40-usb_modeswitch.rules` | upstream-carried | shipped | read (16) | Three modeswitch rules for USB Wi-Fi/NIC sticks. | carried; no finding | tree |

## The configuration

**1. The nearest candidate.** `projects/Generic/linux/linux.x86_64.conf` (8,062 lines, header `Linux/x86 7.1.2`): **659 lines removed, 351 added** against ours. `projects/ROCKNIX/devices/AMD64/linux/linux.x86_64.conf` (12,445 lines, `7.1.2`): 7,671 / 2,980, **not a base**. Ours is 7,754 lines with the header `# Linux/x86 6.15.6 Kernel Configuration` (`:3`). (r02, r03.)

**2. The fork's own edits since the adding commit `73b20caf86` (2026-06-30)** -- 13 lines in two commits (r06, r07):

```text
=== cbf75c0b06 2026-09-10 Handhelds keep their evidence across a power cycle: persistent logs, a watchdog, a crash store
-# CONFIG_WATCHDOG is not set
+CONFIG_WATCHDOG=y
+CONFIG_WATCHDOG_CORE=y
+CONFIG_WATCHDOG_SYSFS=y
+CONFIG_I6300ESB_WDT=y
-# CONFIG_PSTORE is not set
+CONFIG_PSTORE=y
+CONFIG_PSTORE_COMPRESS=y
+CONFIG_PSTORE_CONSOLE=y
+CONFIG_PSTORE_RAM=y
+CONFIG_EFI_VARS_PSTORE=y
=== 1cd0093d67 2026-07-26 GENERIC_X64 - advertise the host's address in the cloud setup QR
-# CONFIG_FW_CFG_SYSFS is not set
+CONFIG_FW_CFG_SYSFS=y
```

**3. The built-versus-committed gap.** The recipe builds `PKG_VERSION="7.1.2"` for `RK3326|AMD64|GENERIC_X64` (`projects/ROCKNIX/packages/linux/package.mk:36-37`). It copies the committed file in (`:154`), sets four values with `scripts/config` (`:157-174`: the initramfs, the hostname, `CONFIG_SWAP` off without `SWAP_SUPPORT=yes`, `CONFIG_CIFS` off without `SAMBA_SUPPORT=yes`), adds the x86 firmware list (`:197-207`), and then:

```text
306:  kernel_make listnewconfig
309:    kernel_make oldconfig            # INTERACTIVE_CONFIG=yes
315:    yes "" | kernel_make oldconfig > /dev/null   # the default: every new 7.1 symbol takes its default
```

So the committed file is the input to a configuration it does not record.

**The gap, stated from the recipe (the primary statement).** Every Kconfig symbol 7.1.2 has and 6.15.6 did not is answered with its default, unseen (`listnewconfig`'s list, `:306`, then `yes "" | ... oldconfig`, `:315`). Every symbol 6.15.6 had and 7.1.2 dropped disappears from the result. The four forced values and the firmware list replace whatever the file says. So the file cannot be read as the guest's configuration for any option 7.1 added, renamed or re-defaulted, nor for `CONFIG_SWAP`, `CONFIG_CIFS`, `CONFIG_DEFAULT_HOSTNAME`, `CONFIG_INITRAMFS_SOURCE` or `CONFIG_EXTRA_FIRMWARE`. Nothing was built for this statement.

**The corroboration, measured.** An existing M7 build root holds the output of exactly this step on the same input (provenance below), so the statement's prediction can be checked (r24; `diff` lines and option names):

| Built (7.1.2) against committed (6.15.6) | Count |
| --- | ---: |
| `diff` lines removed / added | 335 / 641 |
| Options in ours / in the built file | 6,205 / 6,380 |
| Same option, different value | 18 |
| In ours, absent from the built file (gone in 7.1) | 189, of them 97 set |
| In the built file only (new in 7.1, defaulted) | 364, of them 137 set |
| **The fork's 10 settings above, kept in the built file** | **10 of 10** |

The 18 changed values, by cause:
- **The recipe forces them:** `CONFIG_SWAP y -> n` (`SWAP_SUPPORT="no"`, `options:86`); `CONFIG_CIFS y -> n` (no `SAMBA_SUPPORT`); `CONFIG_DEFAULT_HOSTNAME`; `CONFIG_INITRAMFS_SOURCE`; `CONFIG_EXTRA_FIRMWARE` (1,254 entries: amdgpu 675, radeon 247, intel-ucode 153, i915 130, rtl_nic 40, amd-ucode 6, e100 3).
- **The toolchain:** `CC_VERSION_TEXT`, `GCC_VERSION`, `AS_VERSION`, `LD_VERSION`, `RUSTC_VERSION`, `RUSTC_LLVM_VERSION`.
- **7.1's `oldconfig` defaults:** `PREEMPT n -> y` (the committed file says `CONFIG_PREEMPT_VOLUNTARY=y` at `:126`; the built file has `CONFIG_PREEMPT=y` at `:134` and no voluntary option), `PGTABLE_LEVELS 4 -> 5`, `INT340X_THERMAL n -> m`, `NLS_UCS2_UTILS y -> m`, `CRYPTO_LIB_CURVE25519_GENERIC m -> y`, and `BOOTPARAM_HUNG_TASK_PANIC` / `BOOTPARAM_SOFTLOCKUP_PANIC` from a boolean to an integer `0`.

**Provenance of the corroboration** (copies under `/workspace/tmp/m6-t11/cfg/`; a copy's time is its file's mtime, a run's time is its start in `runs.tsv`):

| Item | Source (read-only) | Its time | Read at (UTC) | Copy and sha256 |
| --- | --- | --- | --- | --- |
| Root A | `/workspace/repos/rocknix.worktrees/m7-signin-generic-build-20261025-01`, branch `build/m7-signin-generic-20261025-01`, head `bcc866f1f3143b3040947777f5e9098cecdaf8b4`; root `build.pixelelated-GENERIC_X64.x86_64` | — | ad-hoc reads between 06:48 and 06:56:11 (not timed one by one) | — |
| Root B | `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20`, branch `build/m7-pixelelated-replacement20`, head `1a026648442321609b2288c2c9c06803817f9df2`; the same root name | — | ad-hoc reads between 06:48 and 06:56:11 (not timed one by one) | — |
| A's built `.config` | `A/build/linux-7.1.2/.config` | mtime 2026-10-14 21:52:32 | 06:52:01 (copy); 06:56:12 (r24) | `built-a.config`, `e769f2e5fe2ebe9d489d04c77fc4a397071df06ef77f19c5ecaf68dad6e1be82` |
| B's built `.config` | `B/build/linux-7.1.2/.config` | mtime 2026-10-05 03:37:29 | 06:52:01 (copy); 07:10:54 (sha256 re-read) | `built-b.config`, the same sha256 |
| The committed file | `git show 8ebaf8daad:<conf>` | — | 06:52:01 | `ours.conf`, `7ec3d2b40528370d110ab133122a877f5a9a9f53e18e84d103afe8a4aad72ef7` |
| The Generic conf | `git show 8ebaf8daad:projects/Generic/linux/linux.x86_64.conf` | — | 07:02:47 | `generic.conf`, `d31df3f1d3cd47d9ad167619a08d9a07fd148c6312afce2e85619e9f09b6748f` |
| The class output | `cfgclass.py` over the two copies | — | 06:52:12 | `classes.out`, `600521bf1e13cbec1d8406d0ab5b0dc8ec69d5333585c57f2870f0c98b6540c7` |
| A's installed firmware | `A/install_pkg/kernel-firmware-20260309/usr/lib/kernel-overlays/base/lib/firmware` | dir mtime 2026-10-25 05:58:48 | ad-hoc reads between 06:48 and 06:56:11 (not timed one by one); 06:56:12 (r25) | not copied: counted in place (6,158 files, 2,876,913,748 bytes) |
| A's bzImage and embedded firmware | `A/build/linux-7.1.2/arch/x86/boot/bzImage`; `A/build/linux-7.1.2/external-firmware` | 2026-10-14 21:53:56; 21:52:29 | ad-hoc reads between 06:48 and 06:56:11 (not timed one by one); 06:56:12 (r26); 07:10:54 (stat) | not copied: `stat` and `du` in place |

**The transfer argument** (why a root built elsewhere measures this tree's file):
1. Each root's head carries the committed configuration byte for byte: `git -C <root's worktree> diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf` prints nothing, and `--quiet` exits 0, for both A and B (07:10).
2. The file's last commit in both heads' history is `cbf75c0b06` (2026-09-10), before either `.config` was written (2026-10-05 and 2026-10-14).
3. Two roots built nine days apart from different heads produced byte-equal configurations.
4. The recipe lines that shape the output (`:36-37`, `:154-207`, `:306-316`) are the ones read at `8ebaf8daad`. The toolchain values that differ are the build's, and are named as such.

What the argument does not cover: a root's `.config` reflects that build's recipe, so a later recipe change would make the measurement stale. The primary statement does not depend on it.

**Does the file mislead a behaviour claim?** One proof read it as the guest's configuration: `docs/qa-logs/2026-10-11-usb-revision/guest02/run.py:15` asserts `# CONFIG_USB_GADGET is not set` in `frozen-linux.config`, which is byte-equal to the committed file (sha256 `7ec3d2b40528370d...`). The claim holds: the built file says the same (`:6249`), and the run's own guest probe found no `/sys/kernel/config/usb_gadget`. The 2026-10-14 proxy proofs used the built file. No other claim reads the file (r24; the `git grep` for the preemption model in `docs`, `.claude`, `tools` and the device). **So the gap is a provenance defect, not a bug** (F-04).

**The regeneration, named as a packet, not done here.** Run `oldconfig` at 7.1.2 over the committed file with the recipe's four forced values, and commit the result under its true header. A reviewer then compares three things: the regenerated file against the built `.config` (expected: equal but for the build path and the toolchain lines); the fork's 10 settings (expected: kept); and, on a guest, `modprobe configs; zcat /proc/config.gz` against the file (`CONFIG_IKCONFIG=m`, `CONFIG_IKCONFIG_PROC=y` at `:162-163`, which is why the usb-revision run recorded `kernel_config_exposed: false`). It needs a build root, so it belongs to the lane that owns the next GENERIC_X64 build.

## The boot files

`scripts/image:272-289` (r10): when `BOOTLOADER` is set, `find_file_path bootloader/install ${BOOTLOADER_DIR}/install` sources the first match. The search runs the device directory, then `projects/ROCKNIX`, then the package (`config/functions:1188-1195`). **No bootloader package in the tree carries its own `install` or `release`**, so the project files shadow nothing. `scripts/image` has no `set -e`: a failing `cp` inside these sourced files prints and the step goes on.

| Script | Who runs it | The branch that works, per shipped device | Upstream at `651150fc88` | Disposition |
| --- | --- | --- | --- | --- |
| `bootloader/install` (80) | `scripts/image:280`, every device | GENERIC_X64 `syslinux` (`:14-23`): copies `${INSTALL}/usr/share/syslinux/*` (staged by `syslinux:target`, which the image package pulls through `${BOOTLOADER}`) into `/usr/share/bootloader`. H700 `u-boot` (`:45-48`) and SM8550 `qcom-abl` (`:50-61`) echo and skip: their files are staged by their recipes and written at image time (`install:51-58`; `rocknix-abl/package.mk:13-17`, `H700/packages/u-boot/package.mk:28-34`). `grub` (`:25`), `systemd-boot` (`:35`), `""` (`:63`) and `*)` (`:68`) are reached by **no** device (r13: every `BOOTLOADER=` is `syslinux`, `u-boot` or `qcom-abl`). | **Fork-only** (r12; added `73b20caf86`, edited `7178f1b1f3`) | Keep: syslinux does work and keeps `release`'s glob filled on GENERIC_X64. F-03 (header), F-05 (an unread copy), F-06 (four unreached branches). |
| `bootloader/mkimage` (113) | `scripts/mkimage:225-263`, sourced for `u-boot`, `arm-efi` and `qcom-abl` when the device has no own `bootloader/mkimage` | H700 (u-boot) and SM8550 (qcom-abl). GENERIC_X64's syslinux path never sources it: it writes `syslinux.cfg` and copies the loader from `${TOOLCHAIN}/share/syslinux` (`scripts/mkimage:142-180`). | **Modified**: the SM branches move to bls/dtb, `gou_extras` goes (r09) | Carried; the upstream rewrite is T25's and T28's (F-09). |
| `bootloader/release` (5) | `scripts/image:285`, every device | All three: `cp -a ${INSTALL}/usr/share/bootloader/* ${RELEASE_DIR}/3rdparty/bootloader`. The glob has sources on each (r27): H700 u-boot and dtbs; SM8550 `rocknix-abl` and the `rocknix` package; GENERIC_X64 `install`'s syslinux copy. | Unchanged | Carried; no finding. |
| `bootloader/rkhelper` (60) | Nobody on a shipped device. `grep` (r14): read by `RK3326/packages/u-boot-legacy:39`, `RK3326/packages/u-boot:35`, `RK3399/packages/u-boot:39`, `RK3566/packages/u-boot-Generic:37`, `RK3566/packages/u-boot-Specific:37`, `RK3576/packages/u-boot:37`, `RK3588/packages/u-boot:38` | None of ours. | Unchanged | Carried for ROCKNIX's Rockchip devices. The inventory's `shipped` reach is directory-level (F-08). |

**`install`'s header** (F-03): line 2 reads `# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)`. The file was created by the fork on 2026-06-30 (`73b20caf86`, Max Engel), upstream has never carried it (r12), and nothing in it says it is the fork's.

## The launcher

**How the tools reach it** (the resolution accepted by the coordinator, 06:47 UTC on #658, in place of the brief's *by basename*):
- **The one tool that runs `vm/generic-x64-vm` is `tools/vm-pair`, by full path through `VM_TOOL`.** `:36` sets `VM_TOOL="$ROOT/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm"`, and `:74` runs it.
- The rule's `VM_TOOL=` lines (`generic-x64-vm-testing.md:83`, `:107`) do the same, and `tools/last-good-scripts-test:3406-3571` copies it into a fixture by path.
- The basename appears only in comments and help text: `tools/vm-serial:8`, `tools/cloud-test-backend:8`, `tools/cloud-round-trip:4`, `:504`, `:513`, `:607`.
- **Nothing resolves the basename**: there is no `tools/generic-x64-vm` (r21), no `PATH` entry, no symlink and no install step (r18).

**The flags `vm-pair` depends on** (`:74`; r19, r20): the `run` subcommand; `--headless` (`:686`), `--daemonize` (`:707`), `--gl` (`:696`, only when `VM_GL` is set), `--monitor` (`:684`), `--serial` (`:694`), `--pidfile` (`:705`), `--vnc` (`:704`), `--ssh-port` (`:712`), `--mac` (`:722`); the positional disk (`:665`). `vm-pair` passes an explicit path for each socket and the PID file, so the launcher's `/tmp` defaults (`:684`, `:694`, `:705`) do not reach it. Not used by any tool: `profile`, `qemu-args`, `--net`, `--bridge`, `--display`, `--res`, `--accel` and the `--ovmf-*` trio. `utm` is used only by `last-good-scripts-test`'s fixture (`:3564`, `:3571`) and the README.

**The design, deferred to the coordinator:** the launcher is the device's own description of its machine, read beside `profile.json`, so it stays in the device directory. `tools/` keeps what drives a guest that runs: `vm-pair` owns starting one, through the single `VM_TOOL` line. A second caller should reach the launcher through `vm-pair` or through the same `VM_TOOL` line, not through a basename on `PATH`. The comments and help strings that say *`generic-x64-vm run --headless`* name a command a reader cannot run as written; they should name `tools/vm-pair` or the full path. No edit here.

## The runs

`/workspace/tmp/m6-t11/runner/runs.sh`, started 06:56:11 UTC, from the worktree, `TMPDIR=/workspace/tmp/m6-t11/tmp`. Outputs are in `stage-b/runs/`. Every step is read-only.

| Run | Command (abridged) | Exit | Wall | Figure | A FAIL would mean ... |
| --- | --- | ---: | ---: | --- | --- |
| r01 | § 2's block at `2174265e9c` | 0 | 0.47 s | paths 58, lines 10,418; read 14 / 1,820 / 1,421; tier 11 / 46 / 1; reach 49 / 9; GENERIC_X64 fork-own 1,217 | a different count: the slice's membership moved |
| r02 | `diff` ours against the Generic and AMD64 confs | 0 | 0.03 s | 659 / 351; 7,671 / 2,980; ours 7,754 | the base claim is wrong |
| r03 | the conf's line 3 | 0 | 0.01 s | `Linux/x86 6.15.6` | a header that matches the built version: no Q2 finding |
| r04 | the recipe's versions (`:30-45`) | 0 | 0.00 s | `7.1.2` for `RK3326\|AMD64\|GENERIC_X64` | GENERIC_X64 on another version |
| r05 | `listnewconfig` / `oldconfig` lines | 0 | 0.00 s | `:306`, `:309`, `:315` | no silent `oldconfig`: the gap would not exist |
| r06 | the conf's fork commits since `73b20caf86` | 0 | 0.01 s | `cbf75c0b06`, `1cd0093d67` | another edit to read |
| r07 | their lines | 0 | 0.02 s | 13 lines | a count other than 13 |
| r08 | the history with three identities | 0 | 0.06 s | 110; fork 40; upstream 70 | the history figures move |
| r09 | the upstream delta | 0 | 0.01 s | 7 M, 11 D | a fork-only file upstream has, or a new change |
| r10 | who runs the boot files | 0 | 0.01 s | `scripts/image:280`, `:285`; `scripts/mkimage:225-263` | a boot file run from elsewhere |
| r11 | `install`'s branches | 0 | 0.00 s | 7 branches at `:14`, `:25`, `:35`, `:45`, `:50`, `:63`, `:68` | a branch not read |
| r12 | `install` upstream? | 0 | 0.00 s | `fork-only-install` | upstream carries it: F-03 falls |
| r13 | `BOOTLOADER=` per device | 0 | 0.01 s | 15 devices: syslinux 2, u-boot 7, qcom-abl 6 | a device on `grub` or `systemd-boot`: F-06 falls |
| r14 | `rkhelper`'s readers | 0 | 0.12 s | 7 Rockchip u-boot recipes | a shipped device reads it: F-08 falls |
| r15 | the generic recipe's last commits | 0 | 0.01 s | `3d7c075f63` (fork), then four upstream | — |
| r16 | the override's fork commits | 0 | 0.02 s | `3d7c075f63`, `dc948f59aa` | — |
| r17 | the launcher's functions | 0 | 0.02 s | 19 | — |
| r18 | callers of `generic-x64-vm` | 0 | 0.02 s | `vm-pair:36` the only runner; the rest prose | a basename caller: the resolution falls |
| r19 | the launcher's flags | 0 | 0.01 s | 4 subcommands, 18 flags | a flag `vm-pair` passes that does not exist |
| r20 | `vm-pair`'s call | 0 | 0.00 s | `:36`, `:74` | — |
| r21 | `tools/generic-x64-vm`? | 0 | 0.00 s | absent | present: a second copy |
| r22 | the removal rule | 0 | 0.01 s | both diffs empty | an edit under `packages/`, `projects/` or `tools/` |
| r23 | the firmware lists | 0 | 0.01 s | 8 device lists, none for GENERIC_X64; `x86_64.dat` is `*` | a GENERIC_X64 list: F-01 falls |
| r24 | the built `.config` against ours | 0 | 0.04 s | the table in § The configuration | the fork's settings lost: a bug |
| r25 | the installed firmware (M7 root) | 0 | 0.03 s | 6,158 files, 2,876,913,748 bytes | a small tree: F-01 falls |
| r26 | the built bzImage and the embedded firmware | 0 | 0.01 s | 47,531,008 bytes; 1,255 files, 166,022,540 bytes before compression | no embedded list: F-02 falls |
| r27 | `release`'s glob sources | 0 | 0.01 s | H700, SM8550 and GENERIC_X64 each stage files | a shipped device with none: `release`'s `cp` fails there |
| r28 | readers of the syslinux files | 1 | 0.01 s | the installer reads `/usr/share/syslinux`; `mkimage` the toolchain's; GENERIC_X64 has 0 `bootloader/` files | (rc 1 is `grep -c` printing 0, the expected answer) a reader of `/usr/share/bootloader` on the guest: F-05 falls |

## Findings

| ID | Q | Severity | Category | Where | What |
| --- | --- | --- | --- | --- | --- |
| F-01 | Q5 | Medium | efficiency | `devices/GENERIC_X64/` (no `config/kernel-firmware.dat`); `kernel-firmware/firmwares/x86_64.dat:1` | The guest installs all of linux-firmware, **6,158 files, 2,876,913,748 bytes** in the M7 build root's install tree, for a machine whose four devices (`virtio-blk-pci`, `virtio-gpu-gl-pci`, `virtio-net-pci`, `intel-hda`) load none. Eight devices carry their own list; GENERIC_X64 falls back to `*`. A list of its own is a fork-own fix, but the list sits outside the stamp until T5's E6 (`0c786d298e`) lands, so a new list rebuilds nothing before that (F-17). |
| F-02 | Q5 | Low | efficiency | `packages/linux/package.mk:197-207`; the conf's `DRM_AMDGPU`, `DRM_RADEON`, `DRM_I915` `=y` | The upstream x86 block, keyed on `TARGET_ARCH` alone, builds 1,254 GPU, microcode and NIC firmware files into the guest's kernel. The configuration builds three real-GPU drivers in, inherited from the Generic conf. The bzImage is 47,531,008 bytes with the initramfs; the firmware's share is not separable without a build. |
| F-03 | Q2 | Low | standards | `bootloader/install:2` | A fork-authored, fork-only file under an upstream copyright line dated before it existed; nothing says it is the fork's. |
| F-04 | Q1, Q2, Q3 | Low | provenance | `linux.x86_64.conf:3`; `package.mk:306-316` | The committed configuration names 6.15.6 and differs from what the build makes of it: 18 values (among them `PREEMPT_VOLUNTARY` -> `PREEMPT`), 97 set options gone, 137 set options new. The fork's 10 settings survive, and the one proof that read the file holds. Not a bug: the regeneration packet above, an open item. |
| F-05 | Q5, Q6 | Info | dead-end | `bootloader/install:14-23` | On the guest the syslinux copy into `/usr/share/bootloader` has no reader: the installer reads `/usr/share/syslinux` (`installer:198-200`, `:293-294`), `mkimage` the toolchain's copy, and the device has no `bootloader/update.sh`. It does keep `release`'s glob from failing. |
| F-06 | Q6 | Low | dead-end | `bootloader/install:25-43`, `:63-77` | `grub`, `systemd-boot`, `""` and `*)` are reached by no device. `grub` copies from `/usr/share/grub`, while ROCKNIX's grub package stages into `/usr/share/bootloader/boot/grub` and `EFI/BOOT` directly (`projects/ROCKNIX/packages/tools/grub/package.mk:77-84`), so the branch would warn even if reached. Proposed for the coordinator's decision; removals none. |
| F-07 | Q6, Q7 | Low | clarity | `vm/utm-bundle-readme.txt`; `vm/README.md:4`, `:66-138` | The macOS/UTM route and its ssh + `rclone config` cloud steps, written before D-QA-053 made GENERIC_X64 a developers' tool and D-CLOUD-175 made cloud setup normal linking. The route is still tested (`last-good-scripts-test:3561-3571`), and `095-cloud-ssh` still prints the loopback command (D-QA-054). Whether the UTM route is a supported developer path is the coordinator's question. |
| F-08 | Q6 | Low | tooling | `tools/renovation-inventory`'s reach for `bootloader/rkhelper` and six `device-tree-overlays/sources/{RK3566,RK3588,S922X}` | The inventory reads them `shipped` / H700 by directory or package. No shipped device reads `rkhelper`, and those sources compile only for the device their directory names. The opposite direction to #1049 and #1056 (unreached read as live). |
| F-09 | Q4 | Info | seam | `packages/linux/package.mk:36` against `651150fc88:...:42` | Upstream's case reads `RK3326\|AMD64)`: it never had GENERIC_X64. A merge of `next` must keep the fork's `GENERIC_X64` in a version case, or the device takes another version under a 6.15.6 file. For T25 and T28, with the SM bls/dtb rewrite of `bootloader/mkimage` and `config.xml`. |
| F-10 | Q7 | Low | clarity | `devices/GENERIC_X64/options:26-27`; the conf | `options` does not say why `syslinux` (the profile boots UEFI, and `mkimage` writes the EFI loader, `:179-180`), and the configuration says nowhere where it came from (the Generic conf at 6.15.6, `73b20caf86`). |

## Proofs

| Proof | Claim | Evidence | proved: |
| --- | --- | --- | --- |
| P1 | The 58 and their counts | r01; `01` § Scope | tool-run |
| P2 | The Generic conf is the nearest base | r02 | tool-run |
| P3 | The fork's 13 lines | r06, r07 | history |
| P4 | The build runs a silent `oldconfig` over a 6.15.6 file at 7.1.2 | r03, r04, r05; `package.mk:154-174`, `:306-316` | tree |
| P5 | The built configuration's differences, and the fork's 10 settings kept (corroboration of P4) | r24 on root A's `.config`; § The configuration's provenance table and transfer argument | tool-run |
| P6 | The one proof that read the committed file holds | `usb-revision/guest02/run.py:15-16`; `guest-gadget-presence.json`; both configs' `USB_GADGET` | tree |
| P7 | `install` is fork-only and shadows nothing | r12; the `git ls-tree` of every `install`/`release`; `config/functions:1188-1195` | tree |
| P8 | `install`'s branches per device | r11, r13 | tree |
| P9 | `release`'s glob has a source on each shipped device | r27 | tree |
| P10 | Nothing on the guest reads `/usr/share/bootloader` | r28; the shipped `init`'s `update.sh` hook (`projects/ROCKNIX/packages/sysutils/busybox/scripts/init:432`) finds no `update.sh` on GENERIC_X64 | tree |
| P11 | `rkhelper` reaches no shipped device | r14 | tree |
| P12 | The launcher's resolution and the flags `vm-pair` uses | r18 to r21 | tree |
| P13 | GENERIC_X64 installs all of linux-firmware | r23 (`*`, no device list); r25 (6,158 files) | tool-run |
| P14 | The guest's kernel embeds 1,254 firmware files | r24, r26; `package.mk:197-207` | tool-run |
| P15 | The guest's devices load no firmware | `vm/profile.json`'s four devices | design |
| P16 | Upstream never carried GENERIC_X64 in its version case | r09; `651150fc88:projects/ROCKNIX/packages/linux/package.mk:42` | tree |
| P17 | The sway wrapper chooses Pixman only for virtio without virgl | `sway-generic-x64:21-35` | tree |
| P18 | The removal rule held at stage B | r22 | tool-run |

## Positives

Every check the slice ran, with the input that would have failed it.

| Check | It would FAIL on ... |
| --- | --- |
| The membership block (r01) | an inventory change or a glob error (version 1's `{a,b}` printed 57) |
| The conf diffs (r02) | a base other than the Generic conf, or a regenerated file |
| The fork-lines count (r07) | a third fork commit or a lost line |
| The history split (r08) | a fourth fork identity, or a fork commit under another name |
| The upstream delta (r09) | upstream adding one of the 11 or changing another file |
| `install` fork-only (r12) | upstream carrying `projects/ROCKNIX/bootloader/install` |
| No device on `grub`/`systemd-boot` (r13) | a device options file setting either |
| `rkhelper` unread by ours (r14) | an H700, SM8550 or GENERIC_X64 recipe reading it |
| The launcher resolution (r18, r21) | a `tools/generic-x64-vm`, a symlink, or a caller by basename |
| The fork's settings survive (r24) | any of the 10 differing in the built file -- that would have been a bug |
| The proof that read the file holds (P6) | the built file setting `CONFIG_USB_GADGET` |
| F-01 (r23, r25) | a GENERIC_X64 `config/kernel-firmware.dat`, or a small installed tree |
| F-05 (r28) | an `update.sh` for GENERIC_X64, or the installer reading `/usr/share/bootloader` |
| The removal rule (r22) | a non-empty diff under `packages/`, `projects/` or `tools/` |
| The built-root provenance (r24) | the M7 head's conf differing from `8ebaf8daad`'s, or the two roots' configs differing |
