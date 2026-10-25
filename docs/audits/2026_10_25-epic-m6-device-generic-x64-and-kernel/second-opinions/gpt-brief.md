# Second opinion (Phase 4.6), M6 T11: the GENERIC_X64 VM device, the kernel recipe and the boot files of pixelelated/distribution

You are the one independent reviewer for a read-only audit of 58 paths at commit `8ebaf8daad`. They are the fork's QEMU QA guest (`projects/ROCKNIX/devices/GENERIC_X64/`) and the project's shared kernel recipe, firmware recipes and boot scripts. The first reader (another lab's model) wrote `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md`, all included below. After them come three context sections, then the files, line-numbered: the 14 read paths, the four bootloader scripts, the kernel configuration's header with its diff against the Generic conf, and short excerpts of the code the audit cites.

The lens is cost against value: what each unit costs the images that carry it, and what reads it. **Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. Some figures come from a built tree the first reader read but you cannot: the built kernel `.config` and the installed firmware tree. Their outputs are quoted in `02` § The runs. Treat them as the first reader's measurements: check their consistency with the code you have, and say where the code makes one implausible.

Answer these first, in this order:

1. **The configuration (F-04, `02` § The configuration).**
   - Is the first reader right that the build copies the committed 6.15.6 file, forces four values, and then runs a silent `oldconfig` at 7.1.2 (`projects/ROCKNIX/packages/linux/package.mk`)?
   - Is the gap a provenance defect rather than a `bug`? The decisive question: does anything in the packet read the committed file as the guest's configuration and draw a wrong conclusion? The first reader found one reader, `docs/qa-logs/2026-10-11-usb-revision/guest02/run.py:15`, and says its claim holds.
   - Is the regeneration packet's check sound, including `CONFIG_IKCONFIG=m` and `modprobe configs`?
2. **The firmware (F-01, F-02).**
   - Does GENERIC_X64 really fall back to `firmwares/x86_64.dat` (`*`)? Trace `kernel-firmware/package.mk`'s `find_file_path config/kernel-firmware.dat` through `config/functions`' `find_path` order.
   - Does any of the guest's devices (`vm/profile.json`) need firmware the fallback supplies? Is Medium the right severity for a developers' QA guest (D-QA-053)?
   - Is F-02's x86 block (`package.mk:197-207`) keyed on the architecture alone, as claimed?
3. **The boot files (`02` § The boot files, F-03, F-05, F-06).**
   - Which `bootloader/install` branches does each shipped device (H700 `u-boot`, SM8550 `qcom-abl`, GENERIC_X64 `syslinux`) reach?
   - Is `release`'s `cp -a ${INSTALL}/usr/share/bootloader/*` safe on all three?
   - Is the syslinux copy into `/usr/share/bootloader` really unread on the guest?
   - Would the `grub` branch fail if reached?
4. **The launcher (`02` § The launcher).**
   - Is `tools/vm-pair` the only tool that runs `vm/generic-x64-vm`, by full path through `VM_TOOL`?
   - Does every flag `vm-pair:74` passes exist with the meaning `vm-pair` assumes?
   - Is the deferred design sentence (the launcher stays in the device directory; one `VM_TOOL` line; no basename on `PATH`) sound, or would you place it elsewhere?

Then:

5. **Refute or confirm each finding F-01 to F-10** in `02` § Findings: *confirmed*, *narrowed* (say how), or *refuted* (with the line). Weigh in particular:
   - F-09, the merge seam: upstream's version case at `651150fc88` has no GENERIC_X64 and no default branch. What does the override recipe then build for GENERIC_X64?
   - F-08: the inventory's reach for `rkhelper` and the overlay sources.
6. **What the first reader missed.** Look for:
   - a defect in the 14 files themselves: the sway wrapper's virgl bit test (`sway-generic-x64:21-35`), the serial shell's conditions, the launcher's socket and PID-file handling, `dtb_overlay`'s quoting and its refusals, the udev rules;
   - any boot or firmware path that fails silently under `scripts/image`'s lack of `set -e`;
   - anything in the 58 that behaves wrongly on a shipped device. That would be a `bug`, and the first reader proved none.

**Output:** numbered items `G-1`, `G-2`, ..., each with one line saying *confirmed / narrowed / refuted / new*, the `file:line` evidence, and two to five sentences. Group them under the six headings above. Do not restate the packet, and do not reproduce long code. Keep the whole reply under about 10,000 words.


## The first reader's 02-forward-audit.md (whole)

# Forward audit — M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

- **`reviewed-at`:** `2103f0271d`. The 58 are read at `8ebaf8daad`'s bytes (`git diff --stat 8ebaf8daad 2103f0271d -- <the 58>` is empty). Upstream is `651150fc88`, read locally.
- **Can this be done on the VM? Yes -- on the host, with no network.** Every read, diff, log and branch read runs on the build host at `8ebaf8daad`. The guest whose boot and harness T12 (#659) recorded is the device read here; no guest cycle was needed. No handheld.
- **Built artefacts read, not made.** Two facts came from the M7 lane's existing GENERIC_X64 build root (`/workspace/repos/rocknix.worktrees/m7-signin-generic-build-20261025-01`), read-only:
  - the built kernel configuration (`build/linux-7.1.2/.config`, sha256 `e769f2e5fe2ebe9d...`, byte-equal to the `m7-pixelelated-replacement20` root's and to the three `docs/qa-logs/2026-10-14-*/kernel-7.1.2.config`);
  - the installed firmware tree.

  The M7 head `bcc866f1f3` carries the committed configuration unchanged (`git diff --quiet 8ebaf8daad HEAD -- <conf>`, rc 0). Copies went to `/workspace/tmp/m6-t11/cfg/`; nothing was written in that tree.
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

So the committed file is the input to a configuration it does not record. **Stated from the recipe, the gap is every symbol 6.15.6 did not have** (`listnewconfig`'s list). Nothing was built. The M7 build root already holds the result of exactly this step on the same input, so the gap is also measured (r24; `diff` lines and option names):

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
| P5 | The built configuration's differences, and the fork's 10 settings kept | r24 on the M7 root's `.config` (sha256 `e769f2e5...`, two roots equal; the conf unchanged at the M7 head) | tool-run |
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



## The first reader's 03-retrospective.md (whole)

# Retrospective (Phase 3) — M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

## 3.1 What the slice is

Fifty-eight paths: the fork's QA guest and the project's shared kernel and boot plumbing.
- **The guest's own nine** (1,217 fork-own lines): its options, its kernel configuration, a compositor wrapper with a drop-in, a serial shell, the launcher, its profile and two guides.
- **The plumbing every image carries:** the override kernel recipe, the firmware recipes, four boot scripts, `config.xml`, the project options, two sysctl and three udev files, and `machine-info`.
- **The H700 overlay package**, and 20 firmware blobs.

Three facts organise it:
- **The guest is built from a configuration nobody built.** The committed file is a 6.15.6 configuration copied from the Generic conf on 2026-06-30. It became the input to a 7.1.2 build on 2026-08-21 (`dc948f59aa`). Since then the recipe's silent `oldconfig` has produced a different configuration every time, and the committed file records none of it.
- **The guest inherits a PC's payload.** Two upstream defaults written for real x86 hardware reach a QEMU guest whose four devices need none of it: `x86_64.dat`'s `*` and the x86 block that embeds GPU firmware in the kernel. Nobody chose this for the guest.
- **The boot files are mostly upstream's, run by an upstream mechanism.** The one fork file among them, `install`, does real work only on the guest. Elsewhere it echoes by design.

## 3.2 How it stays this way

- **Nothing compares the committed configuration with the built one.** The build prints `listnewconfig`'s list into its log and continues. The image carries `.config` in `.image/`, and the guest exposes it only after `modprobe configs`. A proof that wants the guest's configuration has to know which of the two files to read. The usb-revision proof read the committed one and happened to be right; the proxy proofs read the built one.
- **A device with no firmware list gets the arch's fallback silently.** `kernel-firmware`'s `makeinstall_target` reads `config/kernel-firmware.dat` if the device has one and otherwise the arch list; nothing says which it used. For x86_64 the fallback is everything. And until T5's E6 lands, adding the list would not even rebuild the package (F-17).
- **`scripts/image` sources the boot scripts without `set -e`.** A branch that fails prints and the image step goes on. That is why `install`'s unreached branches cost nothing, and why nobody would notice if one were reached and failed.
- **The inventory's reach is coarse for files read through `find_file_path` or by `${DEVICE}` subdirectory.** `rkhelper` and six Rockchip and Amlogic overlay sources read as reached by our devices. This is the opposite of the two unreached-but-live gaps T23 and T40 found (#1049, #1056).

## 3.3 What was hard

- **The brief's *by basename* did not match the tree.** Settled with the coordinator at 06:47 UTC: the resolution is `VM_TOOL`'s full path.
- **The built configuration was not supposed to be readable without a build.** It was: the M7 lane's GENERIC_X64 root holds it, and two roots agree byte for byte. Reading another lane's build root is a read, not a write. The provenance is stated in `02`: the M7 head carries the committed file unchanged, so that build's input is this tree's file.
- **Separating the firmware's share of the 47.5 MB bzImage from the initramfs's** needs a build. `02` says so rather than estimating.

## 3.5 The seams

**The recipe x the configuration x `oldconfig`.**
- The recipe owns four values (initramfs, hostname, swap, CIFS), the firmware list and the version.
- The configuration owns everything else, at 6.15.6.
- `oldconfig` silently fills the difference with 7.1's defaults: full preemption instead of voluntary, five-level page tables, and 137 set options the file never names.

A reader of the file sees `PREEMPT_VOLUNTARY=y` and `CONFIG_SWAP=y`; the guest runs neither. The fork's own settings survive because they are explicit lines (10 of 10). The defect is at the seam: no one of the three tells the whole truth. The regeneration packet (`02` § The configuration) closes it for one version. Only a check that compares the two after each build keeps it closed. That is a design for T27's configuration shape, not this slice's edit.

**`scripts/image` x `bootloader/install` x `options`.**
- `options` names the loader.
- The image package pulls the loader package through `${BOOTLOADER}`.
- `install` copies its files into `/usr/share/bootloader`.
- `release` copies that into the release directory.
- `scripts/mkimage` writes the boot partition, from the toolchain for syslinux and from the release directory for the others.

On GENERIC_X64 the middle two steps carry five files nobody reads (F-05). On H700 and SM8550, `install` correctly does nothing and their recipes stage the files. Four of `install`'s seven branches name loaders no device uses, and one of them would copy from a path the matching ROCKNIX package never writes (F-06). The upstream rewrite at `651150fc88` changes the SM side of this chain (bls/dtb), which T28 and T25 inherit (F-09).

**The device directory x `tools/`.**
- The device directory holds the guest's description: profile, launcher, guides.
- `tools/` holds what drives a running guest: `vm-pair`, `vm-serial`, `vm-qa`, the walks.

Exactly one line joins them, `vm-pair:36`. That is the right shape, and the design sentence keeps it: one `VM_TOOL` line, no basename on `PATH`. The prose that says `generic-x64-vm run --headless` names a command nobody can type as written.

## 3.6 Time to play

**Nothing, on either number.** The slice changed no file. Nothing it found is on the launch path: the firmware payload and the kernel's size touch the guest's boot and image size, not the interface-to-first-frame or exit-to-next-frame paths. No guest ran.



## The first reader's 04-analysis.md (whole)

# Analysis — M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

## Executive summary

**Nothing in the 58 behaves wrongly on a shipped device, and no `bug` is proven.**

The slice's weight is three findings about the QA guest:
- **It installs all of linux-firmware**, 6,158 files and 2.88 GB in the M7 build root, for a machine with four virtio and HDA devices (F-01, Medium).
- **Its kernel embeds 1,254 real-GPU firmware files** and builds three real-GPU drivers in, through an upstream block keyed on the architecture (F-02, Low).
- **Its committed configuration is a 6.15.6 file.** It differs from what the build makes of it in 18 values (among them the preemption model), 97 removed and 137 new set options (F-04, Low). The fork's 10 settings survive, and the one proof that read the file holds.

The rest:
- three standards and clarity findings: `install`'s header (F-03), the UTM text (F-07), and `options` silent on its choices (F-10);
- two dead ends in `install` (F-05, F-06);
- an inventory reach gap in the opposite direction to #1049 and #1056 (F-08);
- a merge seam with upstream's version case (F-09).

Removals none (D-WORKFLOW-209). The launcher design and every fork-own dead unit are deferred to the coordinator. The seat's grading is at stage C.

## Acceptance-criteria scorecard

#658's checkboxes, as at stage B. The coordinator ticks at acceptance.

| Criterion | State | Evidence |
| --- | --- | --- |
| Folder holds `00` to `05` | `05` at stage D | this folder |
| The lint `PASS` | at stage C (`--phase pre-issue`) and at close | — |
| `review-plan.json`, provenance, packet manifest | the plan written; the seat at stage C | `second-opinions/` |
| The punch-list issue at outcomes, `box-check` 0 | stage D onward | — |
| `reviewed-at` / `fixed-at`, the empty diffs | `reviewed-at` `2103f0271d`; r22 empty | `02` § The runs |
| `01` § Scope | complete | `01-research-notes.md` |
| `## Coverage`, 58 rows | 58 | `02` |
| § The configuration, three parts | complete, with the measured gap | `02` |
| § The boot files, one row per script | complete | `02` |
| § The launcher | complete; design deferred | `02` |
| § The runs | 28 runs | `02` |
| `00` clean of guests, builds, fetches, extra invokes | so far | `00` |
| `04` Q1, Q2, Q3, Q6, § Second opinion | Q1 to Q7 below; second opinion at C | this file |
| `proved:` cells; `question:` per item | 18 proofs; items at D | `02`, `05` |
| The retro | stage G | — |
| The checkers | stage H | — |

## Risk assessment

| Risk | Likelihood | Impact | Note |
| --- | --- | --- | --- |
| A proof reads the committed configuration as the guest's and is wrong | Medium: one proof already did (2026-10-11) | a false claim about the guest's kernel | F-04; the regeneration packet and the `modprobe configs` check |
| A GENERIC_X64 firmware list is added and nothing rebuilds | High until T5's E6 lands | the fix looks done and the image is unchanged | F-01 depends on E6 (`0c786d298e`) |
| A merge of `next` drops GENERIC_X64 from the version case | Medium at the next upstream merge | the guest builds another kernel under a 6.15.6 file | F-09, for T25 |
| An unreached `install` branch is reached | Low: no device sets those loaders | a warning and an empty `/usr/share/bootloader`; no `set -e` stops it | F-06 |
| The firmware payload grows with linux-firmware | High: `*` takes every new file | a larger guest image each bump | F-01 |

## Coverage boundary

- **Read:** all 58 at `8ebaf8daad`. The 14 code files are read whole; the 20 blobs by name, list membership and reach; the 7,754-line configuration by diff and option class, not line by line.
- **Read beyond the 58,** to answer the questions: `scripts/image`, `scripts/mkimage`, `config/functions:1179-1229`, `packages/virtual/image/package.mk`, the `syslinux`, `installer`, `grub`, `rocknix-abl` and `rocknix` recipes, every device's `options` and `config/kernel-firmware.dat`, `tools/vm-pair`, `tools/renovation-inventory`'s tier rule, and the 2026-10-11 usb-revision proof.
- **Read from the M7 lane's build root, read-only:** the built `.config`, the installed firmware tree, the bzImage's size.
- **Not done:**
  - no build, so the configuration's regeneration and the firmware's share of the bzImage are stated, not measured;
  - no guest, so no boot-time measurement of F-01's or F-02's cost;
  - no check of the 7.1.x kernel's current stable, which needs a fetch (Q4 records the pin and its date).
- **Not this slice's:** the kernel patches (T41), the dead patch set (T40, #1072's `cpugov.patch`), the harness tools themselves (T12), and the upstream merge's rewrite of the SM boot chain (T25, T28).

## Second opinion

At stage C: one seat, GPT-6 Astra at `max` through the installed Facilitator, a probe first, then one refutation pass over the packet (`second-opinions/`). Every item will be graded here as confirmed, narrowed, refuted or new, the decisive ones re-read at their lines.

## Finding Verification

Each finding re-read at its lines after `02` was written:

| Finding | Re-read | Verdict |
| --- | --- | --- |
| F-01 | r23 (no `devices/GENERIC_X64/config/`; `x86_64.dat` is `*`); `kernel-firmware/package.mk`'s `find_file_path config/kernel-firmware.dat` fallback; r25's tree; `profile.json`'s four devices | stands |
| F-02 | `package.mk:197-207` (keyed on `TARGET_ARCH`); r24's `EXTRA_FIRMWARE` count; r26 | stands; the size claim is limited to what is separable |
| F-03 | `install:2`; r12; `git log --diff-filter=A` (`73b20caf86`) | stands |
| F-04 | r03, r05, r24; `usb-revision/guest02/run.py:15-16` and its JSON | stands as provenance; **not a bug**: the one proof that read the file holds |
| F-05 | r28; no `devices/GENERIC_X64/bootloader/`; the shipped `init:432` | stands; it also keeps `release`'s glob filled, so not removable alone |
| F-06 | r11, r13; `projects/ROCKNIX/packages/tools/grub/package.mk:77-84` | stands |
| F-07 | `utm-bundle-readme.txt:9-23`; `README.md:4`, `:66-138`; D-QA-053, D-QA-054, D-CLOUD-175 | stands as a question for the coordinator |
| F-08 | r14; `device-tree-overlays/package.mk:8-11`; the inventory rows | stands |
| F-09 | `651150fc88:projects/ROCKNIX/packages/linux/package.mk:42` (`RK3326\|AMD64)`) and its `esac` at `:53`, no default branch | stands |
| F-10 | `options:26-27`; the conf's first lines (no provenance comment) | stands |

## Renovation face

### Q1 Modernize

**(a) The configuration, in three parts** (`02` § The configuration).
1. **The nearest candidate** is `projects/Generic/linux/linux.x86_64.conf`, 659 lines removed and 351 added. The AMD64 conf (7,671 / 2,980) is not a base.
2. **The fork's own edits since `73b20caf86`** are 13 lines: `1cd0093d67` (`FW_CFG_SYSFS`, for the advertised ssh port) and `cbf75c0b06` (watchdog and pstore).
3. **The built-versus-committed gap.** The recipe copies the 6.15.6 file and forces four values, then runs `listnewconfig` (`:306`) and `yes "" | kernel_make oldconfig` (`:315`) at 7.1.2. Measured on the M7 root's built file:
   - 335 / 641 `diff` lines;
   - 18 changed values: five forced by the recipe, six from the toolchain, seven from 7.1's defaults, including `PREEMPT_VOLUNTARY` -> `PREEMPT` and `PGTABLE_LEVELS` 4 -> 5;
   - 97 set options gone and 137 set options new;
   - **the fork's 10 settings kept.**

   **The regeneration is a packet, an open item.** Run `oldconfig` at 7.1.2 over the file with the recipe's forced values and commit it under its true header. A reviewer compares it with the built `.config` (equal but for paths and toolchain), with the fork's 10, and with a guest's `/proc/config.gz` after `modprobe configs`.

**(b) The launcher.**
- **The resolution:** `tools/vm-pair` runs it by full path through `VM_TOOL` (`:36`, `:74`), as the rule's two `VM_TOOL=` lines do. The basename appears only in comments and help strings, and nothing resolves it.
- **The flags `vm-pair` depends on:** `run`, `--headless`, `--daemonize`, `--gl`, `--monitor`, `--serial`, `--pidfile`, `--vnc`, `--ssh-port`, `--mac` and the disk.
- **The design, deferred to the coordinator:**
  - The launcher stays in the device directory, beside `profile.json`, as the guest's description of itself.
  - `tools/` keeps what drives a running guest, with `vm-pair` the one caller through one `VM_TOOL` line.
  - A second caller uses `vm-pair` or the same line, never a basename on `PATH`.
  - The prose naming `generic-x64-vm run --headless` should name `tools/vm-pair` or the full path.

### Q2 Standards

- **`bootloader/install:2`** (F-03): `# Copyright (C) 2024-present ROCKNIX`, on a file the fork created on 2026-06-30 (`73b20caf86`) that upstream has never carried. The reverse of `fork-workflow.md`'s credits rule: a fork-authored file should say it is the fork's. Not a `bug`; nothing behaves differently.
- **The configuration's header** (F-04): `Linux/x86 6.15.6` (`:3`) on the input to a 7.1.2 build. It is `scripts/kconfig`'s generated line, so it is true of the file and false of the guest.
- **The generic `packages/linux/package.mk` reads fork-own** because the inventory's tier is "differs from the merge base with `upstream/next`" (`tools/renovation-inventory:34-35`). One fork commit makes it differ: `3d7c075f63` (2026-10-02, blitterbot, the hostname line kept as `ROCKNIX`, D-WORKFLOW-123).

  ```text
  3d7c075f63 2026-10-02 blitterbot identity: prepare Rasteratops 0.0.1 source inputs (#337, #383)
  f6ab981bd8 2026-08-11 Matthias Reichl linux (RPi): update to 6.18.44-846462a
  aa0b259507 2026-08-05 Matthias Reichl linux (RPi): update to 6.18.42-8c0da7c
  ```

  That makes it an upstream file the fork touched, correctly marked; its reach is `unreached`, because the ROCKNIX override shadows it on every device. The override in the 58 is fork-own by the same commit and by `dc948f59aa` (GENERIC_X64's version line). Both marks are right.

### Q3 Bugs

- **The `oldconfig` gap is not a `bug`.** The file misleads a reader: the preemption model, swap and CIFS all read differently in the build. But no behaviour claim is wrong because of it. The one proof that read the committed file as the guest's (`usb-revision/guest02/run.py:15`, `CONFIG_USB_GADGET` unset) holds in the built file (`:6249`) and on its guest. The later proxy proofs read the built file. Swap and CIFS are off because `options` says so (`SWAP_SUPPORT="no"`, no `SAMBA_SUPPORT`), so the build is what was meant.

  `Already written:` the images built from the file since 2026-08-21 carry the built configuration in `.image/` and on the guest behind `modprobe configs`; nothing on a device; nothing inherited by a fix that regenerates the file. F-04 is an open item: the regeneration packet.
- **`install`'s echo branches are the design, not bugs.** H700 is `u-boot` and SM8550 `qcom-abl` (r13). Their loaders are staged by their recipes and written at image time (`install:51-58`; `rocknix-abl/package.mk:13-17`; `H700/packages/u-boot/package.mk:28-34`). `release`'s glob has sources on both (r27).
- **`systemd-boot` and `*)` are reached by no device**, and neither are `grub` and `""` (r13: every device is `syslinux`, `u-boot` or `qcom-abl`). They are dead ends (Q6), not bugs. Had `grub` been reached, its copy from `/usr/share/grub` would have warned, because ROCKNIX's grub package stages elsewhere (F-06). But it is not reached.
- **`cpugov.patch`** is #1072's (T40), cited, not re-read.

### Q4 Package currency

| Unit | Here (`8ebaf8daad`) | Upstream (`651150fc88`) | Note |
| --- | --- | --- | --- |
| Kernel, GENERIC_X64 | 7.1.2 (`:36-37`, `PKG_PATCH_DIRS+=" 7.0"`) | GENERIC_X64 absent; `RK3326\|AMD64` still 7.1.2 | No upstream bump moves it. The 7.1.x stable is not checked (no fetch); the pin dates from `dc948f59aa` (2026-08-21). F-09 is the merge seam. |
| Kernel, H700 and SM8550 | 7.2 | 7.2 | unchanged |
| Kernel, other devices | RK3566/RK3576 7.0.2; S922X/RK3399 6.18.49 | RK3566/RK3576/S922X 7.2.11 (`c803640655`, 2026-10-16); RK3399 6.18.54 | not ours; the next merge brings it |
| `rocknix-joypad` | `ROCKNIX/rocknix-joypad` `d02ed13aae` | `hackbar/rocknix-joypad` `005033d1dd` | H700's driver (GENERIC_X64 sets `ROCKNIX_JOYPAD="no"`); behind upstream, brought by the next merge (T25) |
| `extra-firmware` | `88b363e67d` | `925dfb5efb` | SM8550 copies `SM8550/*`; behind upstream (T25) |
| `kernel-firmware` | 20260309 | 20260309 | unchanged |

### Q5 Efficiency

- **The guest's firmware (F-01, Medium).** 6,158 files, 2,876,913,748 bytes installed, because GENERIC_X64 has no `config/kernel-firmware.dat` and `x86_64.dat` is `*`. Its four devices load none. A fork-own list would remove it. Any such list waits on T5's E6 for the stamp (F-17).
- **The guest's kernel (F-02, Low).** 1,254 firmware files embedded and `DRM_AMDGPU`, `DRM_RADEON`, `DRM_I915` built in (inherited from the Generic conf). The block is upstream's and keyed on the architecture. The fork's levers are a `DEVICE` guard or the device configuration: a design for the coordinator, with T27's configuration shape.
- **The configuration's size against the Generic conf's.** The comparison crosses versions (the Generic file is at 7.1.2, ours at 6.15.6), so part of the 659 / 351 is kernel drift, not a choice. By option (`/workspace/tmp/m6-t11/cfg/`, the same parser as r24):
  - **set in ours and not in the Generic conf: 107.** Version and arch symbols lead (`AS_` 7, `ARCH_` 6, `CRYPTO_LIB_` 6, `INLINE_` 5), then `IP`/`IP6` options and the fork's watchdog, pstore and fw_cfg lines;
  - **set in the Generic conf and not in ours: 217.** Netfilter leads (`NFT_` 32, `NF_` 17, `NETFILTER_` 9), then 20 `SND_HDA` codecs, `RTW89`, `MLX4`, SCSI and IOMMU options;
  - **8 values differ.**

  The four GPU drivers (`DRM_VIRTIO_GPU`, `DRM_AMDGPU`, `DRM_I915`, `DRM_RADEON`, all `=y`) are the Generic conf's too: ours inherits them, it does not add them. Nothing in the diff is an AMD64 handheld's (the AMD64 conf is 7,671 lines away). Which of the 217 are deliberate is not recorded anywhere (F-10).
- **The overlay package.** One recipe, eight sources; only H700's DDR3 source compiles on a shipped device (`package.mk:8-11`).
- **`machine-info`.** Nine lines on every image, one read by WebKitGTK and hostnamed, and wanted on the guest so its frames are the handheld's. No cost.
- **`install`'s syslinux copy (F-05).** Five files, unread on the guest.

### Q6 Dead ends

Every unit, removals none (D-WORKFLOW-209).

| Unit | Disposition |
| --- | --- |
| `bootloader/rkhelper` | Carried: read by seven ROCKNIX Rockchip u-boot recipes; no device of ours. The inventory's reach is F-08. |
| `install` `u-boot` branch | Design (H700), keep |
| `install` `qcom-abl\|arm-efi` branch | Design (SM8550), keep |
| `install` `grub` branch | Dead: no device; would read the wrong path (F-06). Fork-own; proposed for the coordinator's decision. |
| `install` `systemd-boot` branch | Dead: no device (F-06). Fork-own; proposed. |
| `install` `""` and `*)` branches | Dead: every device sets a named loader (F-06). Fork-own; proposed. |
| `install`'s syslinux copy into `/usr/share/bootloader` | Unread on the guest, but keeps `release`'s glob filled (F-05). Keep until the chain is redesigned (T28). |
| `vm/README.md` UTM sections, `vm/utm-bundle-readme.txt` | Live and tested (`last-good-scripts-test:3561-3571`); whether the macOS/UTM route stays a supported developer path after D-QA-053 is the coordinator's question (F-07). |
| `vm/profile.json` | Live: read by the launcher (`:26`, `:47-48`) |
| `device-tree-overlays` RK3566, RK3588 and S922X sources | Carried for ROCKNIX's devices; none of ours compiles them (F-08) |
| `kernel-firmware/extra-firmware` rtl_bt (8) and cirrus (4) | Carried for ROCKNIX's devices; on ours only the guest gets them, through `*` (F-01) |
| `kernel-firmware/extra-firmware` panels (10) | Live: H700's list and kernel |
| `firmwares/any.dat` | Carried: the aarch64 fallback; H700 and SM8550 have their own lists |
| `linux-drivers/rocknix-joypad` | Live on H700 |
| `linux-firmware/extra-firmware` | Live on SM8550 |

### Q7 Clarity and structure

- **What the guest is for.** The serial shell's unit says it (`serial-debug-shell.service:4-14`, D-QA-053), and so does a comment in `options` (`:13-14`). The README opens on *Linux/QEMU and macOS/UTM*, which reads like a product (F-07).
- **How it is booted.** `vm/README.md` and `profile.json` describe the launcher; T12's harness drives it through `vm-pair`. A reader of the device directory cannot tell that `vm-pair` is the way in; § The launcher's design sentence places that line.
- **`options`.** It does not say why `BOOTLOADER="syslinux"`: the profile boots UEFI, and `mkimage` writes syslinux's EFI loader from the toolchain (`:179-180`). It does not say why `UBOOT_SYSTEM` is absent, which is a u-boot device's knob (F-10).
- **The configuration.** Nothing says where it came from (the Generic conf at 6.15.6, `73b20caf86`) or that the build moves it to 7.1.2 (F-04, F-10).

## Instruction File Recommendations

Proposals for the coordinator, not edits:
1. **`generic-x64-vm-testing.md`:** the guest's kernel configuration is the built one. Read `.image/.config` in the build root, or `/proc/config.gz` on a guest after `modprobe configs`, never the committed `linux.x86_64.conf`, until the file is regenerated (F-04).
2. **`device-builds.md` or `packaging-and-patches.md`:** a device with no `config/kernel-firmware.dat` installs its arch's fallback, which on x86_64 is everything (`*`). A new device states its list (F-01).
3. **For reachability work:** a file read through `find_file_path` from a recipe, or a source compiled from a `${DEVICE}` subdirectory, is reached only by the devices that build that recipe or name that directory (F-08).

## Quality self-check

- Every figure in `02` comes from a run with its exit and wall time (r01 to r28), and every finding is re-read at its lines (§ Finding Verification).
- **Two claims rest on another lane's build root:** the built configuration and the firmware tree. Their provenance (the conf equal at the M7 head, two roots byte-equal) is in `02`'s header. Nothing was written there.
- **Three line ranges were wrong in the first draft of `02`** and were corrected before commit: `:197-207`, `scripts/image:272-289`, and the shipped `init:432`.
- **Q5's first draft said the configuration adds the four GPU drivers.** The option diff showed they are the Generic conf's (inherited, `=y` in both), and that the Generic file's 7.1.2 header makes part of the 659 / 351 version drift; corrected before commit.
- **What would change the verdicts:**
  - a built `.config` from a different input: the M7 head's conf differing;
  - a GENERIC_X64 firmware list somewhere `find_file_path` searches;
  - a device on `grub` or `systemd-boot`;
  - a proof that read the committed configuration and was wrong. One was looked for (`git grep` in `docs`, `.claude`, `tools`, the device) and the one found holds.



## Context 1: docs/reviews/order.md § T11

```text
### T11. devices: the GENERIC_X64 VM device, the kernel and drivers recipes, and the project's boot files

- **id**: `device-generic-x64-and-kernel`; **kind**: read; **lens**: cost against value
- **why here**: GENERIC_X64 is the fork's own (989 fork-own lines) and the VM every proof runs on; the kernel recipes and project bootloader serve every device; its fork-written kernel configuration (7,754 lines) is read here as a diff against its base (plan § 2); the test image (D-WORKFLOW-185), read with the harness that boots it under D-WORKFLOW-186, the maintainer's weight on the build process ahead of any device target ("test process")
- **paths** (58 paths, 10,418 lines, 1,820 read, of which 1,421 fork-own; 7,754 patch and config lines; reach shipped 49, test 9): areas `devices`; globs `projects/ROCKNIX/devices/GENERIC_X64/**`, `projects/ROCKNIX/packages/**`, `projects/ROCKNIX/{bootloader,filesystem}/**`, `projects/ROCKNIX/{options,config.xml}`, `packages/**`; reach `shipped`, `test`, `n/a` **plus** areas `patches-and-configs`; globs `projects/ROCKNIX/devices/GENERIC_X64/linux/*.conf`
- **read before**: none
- **depth**: Independent -- an ordinary code slice
- **interacting subsystems** (read-only context): the VM harness (tooling); every device
- **closing evidence**: audit folder, lint PASS, punch list through Phase 7

```


## Context 2: the brief's § 2 and § 4

```text
## 2. Scope

**58 paths, 10,418 lines; 14 of them read (code: shell, Python, recipe,
systemd, udev; 1,820 lines, 1,421 fork-own); fork-own 11 paths / 1,738
lines, upstream-carried 46 / 926, vendor-carried 1 / 7,754 (the kernel
configuration, `tier_note: fork-written`, area `patches-and-configs`);
reach shipped 49, test 9 (the nine are all `devices/GENERIC_X64`).** The
membership is `slices.json` k 11's rule on `inventory.json` at
`2174265e9c`: area `devices` with reach `shipped`, `test` or `n/a` under
the globs `projects/ROCKNIX/devices/GENERIC_X64/**`,
`projects/ROCKNIX/packages/**`, `projects/ROCKNIX/{bootloader,filesystem}/**`,
`projects/ROCKNIX/{options,config.xml}`, `packages/**`; **plus** area
`patches-and-configs` under `projects/ROCKNIX/devices/GENERIC_X64/linux/*.conf`.
`tools/renovation-inventory` has no single-slice selector (`--order` sizes
all 46), so the block reproduces the rule with the tool's glob semantics
(`**` crosses directories, `*` does not, `{a,b}` alternates):

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,re,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
def rx(g):
    g=re.sub(r"\{([^}]*)\}", lambda m: "(?:"+"|".join(m.group(1).split(","))+")", g)   # the loop below escapes each character once
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i] in "(|)?:": out+=g[i]; i+=1
        else: out+=re.escape(g[i]); i+=1
    return re.compile("^"+out+"$")
A=[rx(g) for g in ("projects/ROCKNIX/devices/GENERIC_X64/**","projects/ROCKNIX/packages/**","projects/ROCKNIX/{bootloader,filesystem}/**","projects/ROCKNIX/{options,config.xml}","packages/**")]
B=[rx("projects/ROCKNIX/devices/GENERIC_X64/linux/*.conf")]
t=[r for r in rows if (r["area"]=="devices" and r["reach"] in ("shipped","test","n/a") and any(p.match(r["path"]) for p in A)) or (r["area"]=="patches-and-configs" and any(p.match(r["path"]) for p in B))]
CODE={"assembly","c","c++","c++-header","c-header","cmake","css","docker","go","html","javascript","kconfig","lua","make","perl","python","recipe","rust","script","shader","shell","systemd","typescript","udev"}
read_=[r for r in t if r["tier"]!="vendor-carried" and r["reach"]!="unreached" and (r.get("language") or "") in CODE]
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t))
print("read",len(read_),sum(r["lines"] or 0 for r in read_),"fork-own read",sum(r["lines"] or 0 for r in read_ if r["tier"]=="fork-own"))
print("tier",dict(collections.Counter(r["tier"] for r in t)),"reach",dict(collections.Counter(r["reach"] for r in t)))
print("GENERIC_X64 fork-own lines",sum(r["lines"] or 0 for r in t if r["path"].startswith("projects/ROCKNIX/devices/GENERIC_X64/") and r["tier"]=="fork-own"))
import os; os.makedirs(".qa-scratch/t11", exist_ok=True)
open(".qa-scratch/t11/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))
print("written", len(t), ".qa-scratch/t11/paths.txt")'
# paths 58 lines 10418
# read 14 1820 fork-own read 1421
# tier {'fork-own': 11, 'upstream-carried': 46, 'vendor-carried': 1} reach {'shipped': 49, 'test': 9}
# GENERIC_X64 fork-own lines 1217
# written 58 .qa-scratch/t11/paths.txt
```

(Version 1's block printed 57 paths: its `{a,b}` alternation was escaped twice, so `config.xml` never matched, and it never wrote `paths.txt`; the stranger's proof caught both.)

A different count is a delta to record with the command, not a reason to
stop. **The order's "989 fork-own lines" is an erratum**: GENERIC_X64's
fork-own rows sum to 1,217 lines over 8 paths (`vm/generic-x64-vm` 817,
`vm/README.md` 138, `options` 91, `profile.json` 52,
`serial-debug-shell.service` 41, `sway-generic-x64` 40,
`utm-bundle-readme.txt` 35, `10-generic-x64-renderer.conf` 3), 175 without
`vm/*`; no subset gives 989.

**By directory group** (paths / lines): `devices/GENERIC_X64` 9 / 8,971
(the configuration 7,754; the eight above); `packages/linux` 6 / 460 (the
override recipe `package.mk` 432, **fork-own** in the inventory with `overlap:
true` -- it is upstream's file the fork touched once, `3d7c075f63`, and the
tier rule marks it so; 20 patches; 42 commits on the file since June, 2 of
them the fork's (`3d7c075f63`, `dc948f59aa`), 50 on the directory; `sysctl.d/qdisc.conf`;
`udev.d/10-bfq-sched.rules`; three more); `packages/kernel-drivers` 9 /
357; `packages/linux-firmware` 26 / 143 (lists; 22 of the 26 rows carry no
line count, `lines: null`, and the 143 are the other four's: 93, 25, 24, 1);
`packages/linux-drivers/rocknix-joypad/package.mk` 1 / 25;
`bootloader/install` 80 (fork-own), `mkimage` 113, `release` 5, `rkhelper`
60; `config.xml` 154 (26 upstream commits since June, 0 fork);
`options` 41; `filesystem/etc/machine-info` 9 (fork-own, `rasterabot`,
2026-10-01).

**The kernel configuration has no base in the tree.**
`devices/GENERIC_X64/linux/linux.x86_64.conf` line 3 reads `# Linux/x86
6.15.6 Kernel Configuration` (7,754 lines); the override recipe builds
**7.1.2** for `RK3326|AMD64|GENERIC_X64`
(`projects/ROCKNIX/packages/linux/package.mk:36-40`), copies the device's
conf, runs `kernel_make listnewconfig` and `yes "" | kernel_make oldconfig`
(the recipe's configure step, about lines 306-314), so every option new
between 6.15 and 7.1 takes its default at build time and **the committed
file is not the configuration the kernel is built from**. Measured
candidates (`diff` line counts, removed / added): the AMD64 conf
(`devices/AMD64/linux/linux.x86_64.conf`, 12,445 lines, 7.1.2, unchanged
since the adding commit's parent `cb50b45f6e`): 7,671 / 2,980, not a base;
LibreELEC's `projects/Generic/linux/linux.x86_64.conf` (8,062 lines,
7.1.2): 659 / 351, the nearest. The adding commit `73b20caf86` (2026-06-30,
"Re-derived from origin/x64-build-fix", Copilot co-authored) names none;
the fork's own edits since are 13 lines in two commits (`1cd0093d67`,
2026-07-26, `FW_CFG_SYSFS`, 2 lines; `cbf75c0b06`, 2026-09-10, `WATCHDOG`
x3, `I6300ESB_WDT`, `PSTORE` x5, 11 lines). The slice does not build: it states
the three parts (§ 4 Q1) and proposes the regeneration as a packet.

**The project's boot files are four scripts.** `bootloader/install` is
absent at `651150fc88` (added by `73b20caf86`, last `7178f1b1f3`
2026-09-02) yet opens `# Copyright (C) 2024-present ROCKNIX`; `scripts/image:280`
runs it through `find_file_path bootloader/install`; its `syslinux` branch
is the one GENERIC_X64 and AMD64 take (`BOOTLOADER="syslinux"`,
`devices/GENERIC_X64/options:27`), its `u-boot` and `qcom-abl|arm-efi`
branches echo **by design** -- H700 (`BOOTLOADER="u-boot"`) and SM8550
(`qcom-abl`) both land there, and `install:51-58` says the loader is written
at image time by `mkimage_abl` (`7178f1b1f3`), so the echo is not a missing
loader; its `grub` branch tracks a path upstream deletes (`e6da8dad2b`); it
also has a `systemd-boot` branch (line 35) and a default `*)` (line 68) that
attempts a copy, which no shipped device reaches. `mkimage` differs from upstream by 24 lines (7 added, 17 removed), is
sourced by `scripts/mkimage:225-263`, and T5's E1 changes 15 of its lines on
T5's branch (`feature/m6-build-engine-652`, tip `52e6794ba7`: every `mcopy`
gains `>"${SAVE_ERROR}" 2>&1 || show_error`; F-16; that branch merges
before this one). `release` (5 lines) is run by `scripts/image:285`. `rkhelper` (60 lines) is
`reach: shipped` by placement; whether any shipped device reads it is § 4
Q6's question.

**What `upstream/next` (`651150fc88`) already changes:** 7 of the 58 are
`M` (`bootloader/mkimage`, `config.xml`, `linux-drivers/rocknix-joypad/package.mk`,
`linux-firmware/extra-firmware/package.mk`, `linux/package.mk`,
`linux/sysctl.d/qdisc.conf`, `linux/udev.d/10-bfq-sched.rules`;
`c803640655` 2026-10-16 bumps the RK35x6/S922X kernel in the override);
the 11 `D` are fork-only files that never existed upstream (the GENERIC_X64
device, `bootloader/install`, `machine-info`), not deletions. The upstream
cleanups of 2026-10-22 (`e6da8dad2b` grub, `05fc864362` qualcomm u-boot in
mkimage, `cafbb1657d` Qualcomm to Boot Loader Spec) land after the merge
base `c445081a59`.

**History since 2026-06-01 at `8ebaf8daad`:** 110 non-merge commits on the
58; **40 fork-authored** (Max Engel 36: 34 on `devices/GENERIC_X64`,
`7178f1b1f3` on `install`, `dc948f59aa` on the override recipe; blitterbot
3: `3d7c075f63` on the override recipe, `d6e8390c93` 2026-10-05 and
`bed8e2bb1e` on the device; `rasterabot` 1: `98e1a30362`, `machine-info`)
and 70 upstream (by group, with overlap: `packages/linux` 40, `config.xml`
26, `linux-firmware` 7, `linux-drivers` 5, `bootloader` 4, `kernel-drivers`
2, `options` 1; 70 after de-duplication). **Three fork identities**: a count by author
that forgets `rasterabot` prints 39.

**What the slice's globs do not take, so it does not read them:** the
generic `packages/linux/package.mk` (358 lines, `tier=fork-own`,
`reach=unreached`, shadowed by the override, which is a full recipe and
does not source it -- why it is marked fork-own is § 4 Q2's question, by
`git log`, not by reading the file whole); the per-device aggregators
`virtual/linux-drivers` and `virtual/linux-firmware` (area
`generic-packages`); `graphics/gpudriver` (unshipped); every generic
`packages/linux-firmware/*` (unreached); the GENERIC_X64, AMD64 and QEMU
quirks under `hardware/quirks/platforms/` (T22, #669); T40's 277 dead
generic kernel patches (class (a)).


## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`design`):

- **Q1 Modernize -- the configuration and the launcher.** (a) The kernel
  configuration: state the three parts -- the nearest candidate and its
  removed/added counts (the Generic conf, 659 / 351; the AMD64 conf, 7,671
  / 2,980, named as not a base); the fork's own edits since the adding
  commit (`git log -p 73b20caf86..8ebaf8daad -- <conf>`, the 13 lines);
  the built-versus-committed gap (what `listnewconfig` would answer at
  7.1.2, stated from the recipe, **not built**: the slice names the
  regeneration as a packet, an open item, and says what a reviewer would
  compare after it). (b) `vm/generic-x64-vm` (817 lines) against the
  `tools/vm-*` that call it by basename (how the name resolves: `PATH`, a
  symlink, an install step -- read `generic-x64-vm-testing.md` and the
  callers' lines), what the callers assume of its flags, what the device
  directory should carry and what `tools/` should (a design, deferred to the
  coordinator; no edit).
- **Q2 Standards -- the headers and the marks.** `bootloader/install` is
  the fork's file under an upstream copyright header (`fork-workflow.md`:
  preserve upstream credits and add a ROCKNIX line -- here the reverse
  case: a fork-authored file must say so); the configuration's header
  names a kernel the recipe does not build; why the generic
  `packages/linux/package.mk` is marked fork-own (`git log --format='%h %an
  %s' 8ebaf8daad -- packages/linux/package.mk | head`: an upstream file
  the fork touched, or the inventory's tier rule) -- each a finding with
  its line, a `bug` only where behaviour is wrong.
- **Q3 Bugs -- what is wrong, read.** The `oldconfig` gap is a provenance
  defect, not a build failure: say whether any built image's configuration
  differs from the committed one in a way a reader of the file would be
  misled by (the 13 fork lines and the 6.15-to-7.1 options), and file it as
  a `bug` with its trace only if the file misleads a behaviour claim
  (`Already written:` the images built from it, nothing on a device).
  `install`'s echo branches are the design for H700 and SM8550 (the image
  step writes their loaders, `install:51-58`): not a bug. The questions are
  whether `install` says so where a reader lands (its header; Q2), and
  whether its `systemd-boot` and default `*)` branches are reached by any
  device at all (`grep -n BOOTLOADER projects/ROCKNIX/devices/*/options`
  for the shipped three and the rest): unreached ones are dead ends (Q6),
  a reached one whose copy would fail is a `bug` with its trace. T40's `cpugov.patch` is #1072's, cite.
- **Q4 Package currency.** The override recipe's kernel versions per device
  (`package.mk:36-40` at `8ebaf8daad` and at `651150fc88`, the
  `c803640655` bump), the GENERIC_X64 kernel 7.1.2 against the kernel's
  current stable (read from the recipe and `PKG_URL`, no fetch: the slice
  records the pin and the date, and the upstream bump that moves it);
  the firmware lists' upstream delta (`extra-firmware`); `rocknix-joypad`'s.
- **Q5 Efficiency.** The configuration's size against the Generic conf's
  for a QEMU guest (what the 351 added lines enable; whether the 659
  removed ones are the guest's or an AMD64 handheld's); the nine
  `kernel-drivers` recipes against the devices that reach them
  (`reachable_by`); `machine-info` on every image.
- **Q6 Dead ends -- what is carried and nobody reads.** `rkhelper` (who
  reads it: `grep -rn rkhelper scripts/ projects/ packages/ tools/`);
  `install`'s `u-boot`, `qcom-abl|arm-efi` and `grub` branches (upstream
  deleting grub); `README.md`'s and `utm-bundle-readme.txt`'s UTM/macOS
  instructions after D-QA-053 and D-QA-052; `profile.json`; any
  `kernel-drivers` or `linux-firmware` list no shipped device reaches.
  Dispositions per unit, removals none (D-WORKFLOW-209); fork-own dead
  units proposed on the punch list, deferred to the coordinator.
- **Q7 Clarity and structure.** Can a reader tell from the GENERIC_X64
  directory what the guest is for (D-QA-053) and how it is booted (T12's
  harness or the device's own `vm/generic-x64-vm`)? Does `options` say why
  `BOOTLOADER="syslinux"` and `UBOOT_SYSTEM`'s absence; does the
  configuration say where it came from?

```


## Context 3: register rows D-WORKFLOW-185, -186, -187 and D-QA-053

```text
| D-QA-053 | 2026-09-28 | **GENERIC_X64 is a developer's tool and is never published as a gameplay image.** Maintainer, 2026-09-28: *"With Generic x64, it is only ever intended to be a test harness and tool for developers, not for actual gameplay. At some point, someone could adapt it if they want, but my interest is strictly in making it a great tool to help with the development."* So the serial root shell (#307 PL-023) stays as the developer channel and says so in its unit; what does nothing on the guest (the quirk set's `/etc` writers, the orphan quirk tree, the updater that copies nothing) is removed or made honest because a tool that lies is a worse tool, not because anyone else boots it; GENERIC_X64 stays out of the PR series (D-WORKFLOW-034). Settles the open question of the same ID. | #307, D-WORKFLOW-034 |

| D-WORKFLOW-185 | 2026-10-23 | **The renovation order's shipped-device set is H700 and SM8550. GENERIC_X64 is the test image: built, read as the VM every proof runs on (T19), never shipped. Every other target the fork can build (RK3566, RK3326, RK3399, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750, AMD64) is a row in the unshipped tables, not a device slice; `device-builds.md` § Our devices is a hardware inventory, not the shipping list. RK3566 and RK3326 are the recorded first widening: on rocknix.org's device pages they are the two widest targets after the shipped pair (15 and 13 models against H700's 11 and SM8550's 10; SM8250 3, S922X 2, the other six 1 each, RK3576 none), the maintainer owns their test units (RG353M, RG351M), and upstream's release 20261001 publishes two image variants for each (RK3326 a and b, RK3566 Generic and Specific) as it does for H700 (DDR3 and DDR4). Opening either is a device build with its own issue (D-WORKFLOW-132), and the tables re-derive then.** Put by the coordinator lane (D-WORKFLOW-183) as P1's first pass-7 question, from the three-seat review's finding 12 (`device-builds.md`'s five against plan § 5's eight). Maintainer, 2026-10-22: *"Now we're focused on shipping the H700-based builds and the SM8550-based builds. We have not focused on any of the Rockchip builds or the RG353M or RG351M. The fork uses our VM image only for testing."* Then, the same exchange: *"You could check the ROCKNIX GitHub page for the devices they support and see what additional types might give us the most coverage in terms of chips being used by multiple devices."* The read (upstream's README names no device; rocknix.org's 53 device pages, each naming its image target; the 20261001 release's asset list) was put back as the table above with two options, and the maintainer, 2026-10-23: *"I think we should start with what we've done here with H700 and SM8550."* Consequence for the order (#641): T22 `device-rockchip-shipped` dissolves into T17's rows, its kernel patches and configurations move from T42 to T44 and the other patches only those two apply from T43 to T44, `reach` for RK3566 and RK3326 becomes `unshipped`, T23's run-time model derivation uses the shipped pair and the VM; plan § 5's Devices row is corrected in the same change. | #346; #641; D-WORKFLOW-184; D-WORKFLOW-132; D-WORKFLOW-183; `docs/reviews/plan-for-the-plan.md` § 5; `.claude/rules/device-builds.md` § Our devices; https://rocknix.org/devices/; https://github.com/ROCKNIX/distribution/releases/tag/20261001 |

| D-WORKFLOW-186 | 2026-10-23 | **The renovation's value is weighed on the build process and its tooling before any device target: the order reads the build engine, the package-currency table, the build and test harness (the VM and cloud harnesses, build supervision, the guards) ahead of the per-device slices and the non-gated interface slices, within D-WORKFLOW-102's gates (T1 and T2 stay first); the per-device slices are sized to what the shipped pair needs (D-WORKFLOW-185); and a slice that touches the build path compares it with ROCKNIX's own documented path, not only with the fork's rules. P1 re-sequences the order under this row before the maintainer's yes and argues the new sequence in `order.md`; the order's register row cites this one.** Maintainer, 2026-10-23, in the answer that settled D-WORKFLOW-185: *"In terms of a code audit, we're going to find more value in likely evaluating our build process itself and where there's room for improvement. We should focus on that more than any individual target chipset we're building for. That will always be shifting, and so we need to focus more on the tooling than on any individual chip we're optimized for. For example, we want to make sure package updates, our test harness updates, the actual build process, test process, and everything around that are fully up to date. There's documentation on how the builds are generated via the Docker image on ROCKNIX. It might be worth you going through everything on the website to see how they've structured it, because we may find there are better ways to generate builds, etc."* The read of rocknix.org's build documentation against the fork's build path is #644 (D-QA-012), owned by the coordinator lane; its findings are an input to the build-engine slice (T13) and the supervision slice (T38), and any decision the maintainer makes on a finding is its own row. | #346; #641; #644; D-WORKFLOW-181; D-WORKFLOW-102; D-WORKFLOW-183; D-WORKFLOW-185; `docs/reviews/plan-for-the-plan.md` § 5, § 6a |

| D-WORKFLOW-187 | 2026-10-23 | **The renovation gates no release. M6 is an audit, assessment and renovation of the codebase: it decides what is read, in what order and at what depth, never what ships or when. D-WORKFLOW-102's release clause is retired (`0.1` waiting on Tier 1's findings on the launch, control and state slice and on any known security, state-preservation or launch-path finding from any tier); its placed, progressive review stands. A finding that is a defect is filed as a bug the session it is found (D-WORKFLOW-132) and holds or clears a release the way every bug does (D-QA-051, `tools/rc-preflight`), owned by the release's milestone, never by a slice. The order carries no release-gate column; T1 and T2 keep their place on the order's own lenses, and the one prerequisite that stands is a reading order, not a gate: the launch-path slices are read before #336 Step 1 replaces what they read. The drift re-review runs at the renovation's own cadence (every slice close), not as a release step. D-WORKFLOW-186's "within D-WORKFLOW-102's gates" reads accordingly. P1's pass-7 question 2 (whether `backuptool`, T17, and the system services, T22, also gate `0.1`) is withdrawn as outside the program, not answered.** Maintainer, 2026-10-23, when the coordinator put question 2: *"Our codebase check shouldn't have anything to do with what we're actually shipping. This is meant to be an audit, assessment, and renovation, and not concerned with features proactively shipping. Now, why would your question 2 be part of what we're trying to accomplish here?"* Sweep in the same change: plan § 5 and § 6a, § 8's drift trigger, the M6 body's acceptance and dependencies, #339's gate checkbox; `order.md` § 1, the Gate column and T1's release-gate line are P1's (#641). | #346; #641; #339; D-WORKFLOW-102; D-WORKFLOW-186; D-WORKFLOW-132; D-QA-051; `docs/reviews/plan-for-the-plan.md` § 5, § 6a, § 8 |
```


## projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/sway/sway-generic-x64 @ 8ebaf8daad (whole, line-numbered)

```text
 1  #!/bin/sh
 2  # SPDX-License-Identifier: GPL-2.0-or-later
 3  # Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
 4  
 5  # Non-virgl virtio scanout can keep stale host frames with GLES2/llvmpipe.
 6  # Use Pixman only on that device, not on accelerated or unidentified GPUs.
 7  # This wrapper is installed only on GENERIC_X64 and makes no storage changes.
 8  select_software_renderer() {
 9    [ -z "${WLR_RENDERER:-}" ] || return
10    [ -z "${WLR_RENDER_DRM_DEVICE:-}" ] || return
11    case "${WLR_DRM_DEVICES:-}" in
12      /dev/dri/card*) card_number=${WLR_DRM_DEVICES#/dev/dri/card} ;;
13      *) return ;;
14    esac
15    case "$card_number" in
16      ''|*[!0-9]*) return ;; # Unknown paths or multiple GPUs: retain selection.
17    esac
18  
19    # Linux virtio_gpu registers DRM against the transport parent. Negotiated
20    # features belong to its virtio child, not the DRM card's device symlink.
21    set -- /sys/class/drm/card${card_number}/device/virtio[0-9]*
22    [ "$#" -eq 1 ] && [ -d "$1" ] || return
23    driver=$(readlink "$1/driver")
24    [ "${driver##*/}" = virtio_gpu ] || return
25  
26    # Virtio sysfs emits negotiated bits lowest-first; VIRTIO_GPU_F_VIRGL is0.
27    # A render node is not proof of virgl: DRIVER_RENDER is set in both modes.
28    features=$(cat "$1/features" 2>/dev/null) || return
29    case "$features" in
30      ''|*[!01]*) return ;;
31      0*)
32        [ "${#features}" -ge 64 ] || return
33        export WLR_RENDERER=pixman
34        logger -t Sway 'GENERIC_X64: Pixman for virtio GPU without virgl'
35        ;;
36    esac
37  }
38  
39  select_software_renderer
40  exec /usr/bin/sway.sh "$@"
```


## projects/ROCKNIX/devices/GENERIC_X64/filesystem/usr/lib/systemd/system/serial-debug-shell.service @ 8ebaf8daad (whole, line-numbered)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
 3  #
 4  # A root shell on the serial console, with no login: the developers' way into
 5  # a QA guest (tools/vm-serial; SSH is off on a fresh image). GENERIC_X64 is a
 6  # developer's tool and never a gameplay image (D-QA-053), and this unit is why
 7  # it must not become one unchanged. ROCKNIX strips every getty unit, so this is
 8  # systemd's debug-shell pattern -- a plain /bin/sh bound to the tty -- rather
 9  # than a getty and a login.
10  #
11  # It starts only on a virtual machine: ConditionVirtualization=vm has no |, so
12  # it must hold as well as one of the console conditions (both always met here,
13  # since EXTRA_CMDLINE puts console=ttyS0,115200 on every boot). GENERIC_X64
14  # installed on hardware with a serial header does not open the shell.
15  [Unit]
16  Description=Serial debug root shell on ttyS0 (GENERIC_X64 VM testing)
17  After=rocknix-automount.service
18  ConditionVirtualization=vm
19  ConditionKernelCommandLine=|console=ttyS0
20  ConditionKernelCommandLine=|console=ttyS0,115200
21  # A [Unit] key: the shell outlives an isolate (it sat under [Service] until
22  # 2026-09, where systemd ignores it).
23  IgnoreOnIsolate=yes
24  
25  [Service]
26  Environment=TERM=vt100
27  Environment=HOME=/storage
28  WorkingDirectory=/storage
29  ExecStart=/bin/sh
30  Restart=always
31  RestartSec=1
32  StandardInput=tty
33  StandardOutput=tty
34  StandardError=tty
35  TTYPath=/dev/ttyS0
36  TTYReset=yes
37  TTYVHangup=yes
38  KillMode=process
39  
40  [Install]
41  WantedBy=rocknix.target
```


## projects/ROCKNIX/devices/GENERIC_X64/options @ 8ebaf8daad (whole, line-numbered)

```text
 1  ################################################################################
 2  # setup device defaults
 3  ################################################################################
 4  
 5    # The TARGET_CPU variable controls which processor should be targeted for
 6    # generated code.
 7      case ${TARGET_ARCH} in
 8        x86_64)
 9          TARGET_KERNEL_ARCH="x86"
10          TARGET_KERNEL_PATCH_ARCH="x86_64"
11          # x86-64-v3 (Haswell/Excavator or newer: AVX2, BMI2, FMA). The VM
12          # profile's CPU model is Haswell-v4 for this reason; an older CPU
13          # stops with SIGILL at the first v3 instruction. GENERIC_X64 is a
14          # developers' QA device, not a PC image (D-QA-053).
15          TARGET_CPU="x86-64-v3"
16          TARGET_FEATURES="64bit"
17          ;;
18      esac
19  
20      PARTITION_TABLE="gpt"
21      HW_CPU="Generic x86_64"
22  
23    # Kernel target
24      KERNEL_TARGET="bzImage"
25  
26    # Additional bootloader settings
27      BOOTLOADER="syslinux"
28  
29    # Graphics drivers for x86_64.
30    # VM QA target: virtio (virgl) is the guest's GL -- generic-x64-vm --headless
31    # renders it on the host's GPU (D-QA-052) -- and vmware (svga) is kept for
32    # other hypervisors. llvmpipe (LLVM_SUPPORT below) is the software GL path
33    # (--gl none). iris (Intel HW GL/Vulkan) is intentionally omitted: it pulls in
34    # the intel_clc/SPIR-V toolchain cascade (issue #16). None of these is a
35    # Vulkan driver.
36      GRAPHIC_DRIVERS="virtio vmware"
37  
38    # OpenGL support
39      OPENGL_SUPPORT="yes"
40      OPENGL="mesa"
41  
42    # Vulkan: the loader and headers only. GRAPHIC_DRIVERS builds no Vulkan
43    # driver, so the image carries no ICD and a Vulkan renderer has no device on
44    # a guest; RetroArch's GENERIC_X64 profile draws with gl.
45      VULKAN_SUPPORT="yes"
46      VULKAN="vulkan-loader vulkan-headers"
47  
48    # VAAPI support
49      VAAPI_SUPPORT="yes"
50  
51    # Audio support
52      PULSEAUDIO_SUPPORT="yes"
53  
54    # Network support
55      NETWORK="yes"
56  
57    # Display server for x86_64 systems (wl = Wayland)
58      DISPLAYSERVER="wl"
59  
60    # Window manager/compositor selection (weston / swaywm-env / none)
61      WINDOWMANAGER="swaywm-env"
62  
63    # For x86_64 compatibility
64      PREFER_GLES="no"
65  
66    # Disable 32-bit support for x86_64 builds
67      ENABLE_32BIT="no"
68  
69    # Boot method
70      DISK_LABEL="ROCKNIX"
71      SYSTEM_SIZE="4096"
72      SYSTEM_PART_START="8192"
73  
74    # Keep kernel console redraws from erasing the framebuffer splash (#433).
75    # Serial QA access stays enabled; remove quiet and add debugging for verbosity.
76      EXTRA_CMDLINE="quiet console=ttyS0,115200 console=tty0"
77  
78    # Disable joypad driver for x86_64
79      ROCKNIX_JOYPAD="no"
80  
81    # LLVM for llvmpipe, the software GL path (config/graphic keeps this
82    # device's explicit yes; D-QA-052)
83      LLVM_SUPPORT="yes"
84  
85    # No swap: the QA guest has 8 GiB (vm/profile.json)
86      SWAP_SUPPORT="no"
87  
88    # Enable installer support for GENERIC_X64 (allows installation to disk; a
89    # developer's install -- the serial root shell stays off on hardware, see
90    # serial-debug-shell.service)
91      INSTALLER_SUPPORT="yes"
```


## projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm @ 8ebaf8daad (whole, line-numbered)

```text
  1  #!/usr/bin/env python3
  2  # SPDX-License-Identifier: GPL-2.0-or-later
  3  # Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
  4  
  5  import argparse
  6  import json
  7  import os
  8  import platform
  9  import plistlib
 10  import re
 11  import shlex
 12  import shutil
 13  import socket
 14  import stat
 15  import subprocess
 16  import sys
 17  import tempfile
 18  import time
 19  import uuid
 20  import zipfile
 21  from pathlib import Path
 22  
 23  
 24  VM_DIR = Path(__file__).resolve().parent
 25  
 26  PROFILE_PATH = VM_DIR / "profile.json"
 27  
 28  
 29  def pick_render_node(choice):
 30      """The host render node for --gl: None for the software path."""
 31      if choice in (None, "", "none", "off"):
 32          return None
 33      if choice != "auto":
 34          if not os.path.exists(choice):
 35              raise ValueError(f"--gl {choice}: no such render node")
 36          return choice
 37      for node in sorted(Path("/dev/dri").glob("renderD*")):
 38          driver = Path("/sys/class/drm") / node.name / "device" / "driver"
 39          name = os.path.basename(os.path.realpath(driver)) if driver.exists() else ""
 40          if name == "nvidia":
 41              continue
 42          if os.access(node, os.R_OK | os.W_OK):
 43              return str(node)
 44      return None
 45  
 46  
 47  def load_profile():
 48      with PROFILE_PATH.open(encoding="utf-8") as stream:
 49          profile = json.load(stream)
 50  
 51      if profile["architecture"] != "x86_64":
 52          raise ValueError("GENERIC_X64 profile architecture must be x86_64")
 53      if profile["disk"]["logical_block_size"] != 512:
 54          raise ValueError("GENERIC_X64 boot disk must expose 512-byte logical sectors")
 55      if profile["disk"]["virtual_size_bytes"] < 16 * 1024**3:
 56          raise ValueError("GENERIC_X64 VM disk must be at least 16 GiB")
 57      return profile
 58  
 59  
 60  def qemu_img_info(disk):
 61      qemu_img = shutil.which("qemu-img")
 62      if not qemu_img:
 63          raise RuntimeError("qemu-img is required")
 64      result = subprocess.run(
 65          [qemu_img, "info", "--output=json", str(disk)],
 66          check=True,
 67          capture_output=True,
 68          text=True,
 69      )
 70      return json.loads(result.stdout)
 71  
 72  
 73  def find_ovmf(explicit, candidates, label):
 74      if explicit:
 75          path = Path(explicit).resolve()
 76          if path.is_file():
 77              return path
 78          raise FileNotFoundError(f"{label} does not exist: {path}")
 79      for candidate in candidates:
 80          path = Path(candidate)
 81          if path.is_file():
 82              return path
 83      raise FileNotFoundError(f"could not locate {label}; pass its path explicitly")
 84  
 85  
 86  # OVMF code and its vars template come as a pair from one firmware build: a
 87  # 4 MiB code image with a 2 MiB vars store does not boot. Each entry is one
 88  # distribution's pair; the first whose two files both exist is taken.
 89  OVMF_PAIRS = (
 90      ("/usr/share/OVMF/OVMF_CODE_4M.fd", "/usr/share/OVMF/OVMF_VARS_4M.fd"),
 91      ("/usr/share/edk2/x64/OVMF_CODE.fd", "/usr/share/edk2/x64/OVMF_VARS.fd"),
 92      ("/usr/share/edk2/ovmf/OVMF_CODE.fd", "/usr/share/edk2/ovmf/OVMF_VARS.fd"),
 93  )
 94  
 95  
 96  def find_ovmf_pair(code_arg, vars_arg):
 97      """The OVMF code image and vars template, as one pair. Both given: taken as
 98      given. One given: its partner from the same pair, or the other flag is
 99      needed. Neither: the first pair whose two files exist."""
100      if code_arg and vars_arg:
101          return (
102              find_ovmf(code_arg, (), "OVMF code"),
103              find_ovmf(vars_arg, (), "OVMF vars template"),
104          )
105      if code_arg or vars_arg:
106          given = Path(code_arg or vars_arg).resolve()
107          side = 0 if code_arg else 1
108          for pair in OVMF_PAIRS:
109              if Path(pair[side]).resolve() == given:
110                  partner = find_ovmf(None, (pair[1 - side],), "OVMF vars template" if side == 0 else "OVMF code")
111                  found = find_ovmf(str(given), (), "OVMF code" if side == 0 else "OVMF vars template")
112                  return (found, partner) if side == 0 else (partner, found)
113          raise FileNotFoundError(
114              f"{given} is not a known OVMF pair's; pass --ovmf-code and --ovmf-vars-template together"
115          )
116      for code, vars_template in OVMF_PAIRS:
117          if Path(code).is_file() and Path(vars_template).is_file():
118              return Path(code), Path(vars_template)
119      raise FileNotFoundError(
120          "could not locate an OVMF code image and vars template from one firmware build; "
121          "pass --ovmf-code and --ovmf-vars-template"
122      )
123  
124  
125  def qemu_opt(value):
126      """A value inside one of QEMU's comma-separated option strings: a comma in
127      it is doubled, which is how QEMU reads a literal one (a path is otherwise
128      split at it into an option that does not exist)."""
129      return str(value).replace(",", ",,")
130  
131  
132  def auto_accel():
133      """KVM when this host can accelerate an x86_64 guest with it: the host is
134      x86_64 and /dev/kvm is open to us. /dev/kvm on an aarch64 host is ARM KVM,
135      which cannot run this guest; TCG emulates it instead."""
136      host = platform.machine().lower()
137      if host in ("x86_64", "amd64") and os.access("/dev/kvm", os.R_OK | os.W_OK):
138          return "kvm"
139      return "tcg,thread=multi"
140  
141  
142  def run_paths(args):
143      """The files a start makes or replaces: the OVMF vars store, the monitor
144      socket, and the serial socket with --headless (None otherwise). The
145      socket paths are made absolute but not resolved: a symlink there must
146      be seen as one (stale_socket), not followed to whatever it names."""
147      disk = Path(args.disk).resolve()
148      vars_path = (
149          Path(args.ovmf_vars).resolve()
150          if args.ovmf_vars
151          else disk.with_name(f"{disk.stem}.ovmf-vars.fd")
152      )
153      serial = Path(os.path.abspath(args.serial)) if args.headless else None
154      return vars_path, Path(os.path.abspath(args.monitor)), serial
155  
156  
157  # How long a socket that still answers may take to stop: a guest's QEMU sent
158  # SIGTERM a moment ago (vm-pair's down, then up) is let finish closing.
159  SOCKET_GRACE_SECONDS = 5.0
160  
161  
162  def socket_answers(path):
163      """Whether something still listens on the unix socket at path -- a running
164      QEMU's monitor or serial console. Only a refused connection says nobody
165      does; a connection, a timeout, a socket of another type or no permission
166      to ask all read as held, so a check that cannot tell refuses."""
167      probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
168      probe.settimeout(1.0)
169      try:
170          probe.connect(os.fspath(path))
171      except (ConnectionRefusedError, FileNotFoundError):
172          return False
173      except OSError:
174          return True
175      finally:
176          probe.close()
177      return True
178  
179  
180  def stale_socket(path):
181      """Whether a start may clear path for a socket QEMU binds: True for a
182      socket nobody listens on (a previous QEMU's), False for nothing there.
183      A symlink, a file that is not a socket -- a disk image given as
184      --monitor -- or a socket a running guest still listens on is refused
185      (ValueError) and left as it is."""
186      try:
187          mode = os.lstat(path).st_mode
188      except FileNotFoundError:
189          return False
190      if stat.S_ISLNK(mode):
191          raise ValueError(f"{path} is a symlink; refusing to remove what it points at")
192      if not stat.S_ISSOCK(mode):
193          raise ValueError(f"{path} exists and is not a socket; refusing to remove it")
194      deadline = time.monotonic() + SOCKET_GRACE_SECONDS
195      while socket_answers(path):
196          if time.monotonic() >= deadline:
197              raise ValueError(
198                  f"{path} is a socket a running guest still listens on; stop that "
199                  "guest, or give this one another --monitor/--serial"
200              )
201          time.sleep(0.25)
202      return True
203  
204  
205  def prepare_run(profile, args):
206      """What a start does before QEMU runs, and only a start: the vars store
207      made from its template if the guest has none yet, and the socket paths
208      cleared of a previous QEMU's sockets. Every socket path is checked before
209      any is cleared, so a start refused at one has removed nothing. qemu-args
210      never calls this -- it prints, and touches nothing."""
211      vars_path, monitor, serial = run_paths(args)
212      _, vars_template = find_ovmf_pair(args.ovmf_code, args.ovmf_vars_template)
213      stale = [sock for sock in (monitor, serial) if sock is not None and stale_socket(sock)]
214      for sock in stale:
215          sock.unlink(missing_ok=True)
216      if not vars_path.exists():
217          shutil.copyfile(vars_template, vars_path)
218  
219  
220  def qemu_command(profile, args):
221      """The QEMU command for this profile and these arguments. It reads and
222      checks; it creates, removes and changes nothing (prepare_run does that,
223      for a start)."""
224      disk = Path(args.disk).resolve()
225      if not disk.is_file():
226          raise FileNotFoundError(f"disk does not exist: {disk}")
227  
228      qemu = shutil.which(os.environ.get("QEMU_SYSTEM_X86_64", "qemu-system-x86_64"))
229      if not qemu:
230          raise RuntimeError("qemu-system-x86_64 is required")
231  
232      code, vars_template = find_ovmf_pair(args.ovmf_code, args.ovmf_vars_template)
233      vars_path, monitor, serial = run_paths(args)
234      # A vars store the guest already has is its UEFI settings and is kept --
235      # unless it was made from another firmware build's template (a 2 MiB
236      # store beside a 4 MiB code image, from before the code and template
237      # were chosen as a pair), which this firmware cannot use. Refused, named
238      # and left in place: moving it aside is the owner's call.
239      if vars_path.exists() and vars_path.stat().st_size != vars_template.stat().st_size:
240          raise ValueError(
241              f"{vars_path} is {vars_path.stat().st_size} bytes and this firmware's vars template "
242              f"({vars_template}) is {vars_template.stat().st_size}: it was made for another OVMF build. "
243              "Move it aside and the next start makes a new one from the template (the guest's UEFI "
244              "settings start over; the image boots from its default EFI path)"
245          )
246  
247      disk_info = qemu_img_info(disk)
248      # The canonical disk size is a floor for a Linux launch as for a UTM
249      # bundle: under it the first boot's copy of the interface's resources
250      # runs out of space and the menus come up broken (generic-x64-vm-testing).
251      if disk_info["virtual-size"] < profile["disk"]["virtual_size_bytes"]:
252          raise ValueError(
253              f"{disk} is {disk_info['virtual-size']} bytes, under the profile's 16 GiB "
254              f"({profile['disk']['virtual_size_bytes']} bytes); grow it before the first boot: "
255              f"qemu-img resize {disk} 16G"
256          )
257      disk_profile = profile["disk"]
258      display = profile["display"]
259      network = profile["network"]
260      sound = profile["sound"]
261      accel = args.accel
262      if accel == "auto":
263          accel = auto_accel()
264  
265      # Headless (a build host with no desktop): virtio-gpu-gl-pci refuses
266      # -display none, so the GL-less device stands in; a VNC display on
267      # loopback keeps a scanout committed, which is what makes the monitor's
268      # screendump return a frame rather than black; the serial console moves
269      # from stdio to a unix socket so a script can hold a root shell in the
270      # guest (SSH is off on a fresh image); and a pidfile makes stopping the
271      # VM a kill by PID rather than a pkill by pattern (which has killed the
272      # shell running it). Unix socket paths over 107 bytes fail to bind, and a
273      # session scratch directory is longer than that -- keep them under /tmp.
274      display_device = display["device"]
275      display_arg = args.display
276      vnc_args = []
277      serial_arg = "stdio"
278      pidfile_args = []
279      daemonize_args = []
280      if args.headless:
281          # Hardware GL for a headless guest (fork #291): virtio-gpu-gl-pci
282          # with egl-headless on a host render node, so the guest's Mesa
283          # renders through virgl on the host's GPU instead of softpipe --
284          # RetroArch dropped six frames in ten on the software path and
285          # one in two thousand on this one. --gl auto takes the first render
286          # node whose driver is not nvidia (virglrenderer wants Mesa's EGL);
287          # --gl none is the software path; --gl /dev/dri/renderDNNN names
288          # one. The monitor's screendump has no surface under a GL scanout;
289          # the VNC display stays and the harness takes its frames there.
290          gl_node = pick_render_node(args.gl)
291          if gl_node:
292              display_arg = f"egl-headless,rendernode={gl_node}"
293          else:
294              display_device = display_device.replace("-gl-", "-")
295              display_arg = "none"
296          vnc_args = ["-vnc", f"127.0.0.1:{args.vnc}"]
297          serial_arg = f"unix:{qemu_opt(serial)},server,nowait"
298          pidfile_args = ["-pidfile", str(Path(args.pidfile).resolve())]
299          for sock in (monitor, serial):
300              if len(str(sock).encode()) > 107:
301                  raise ValueError(f"unix socket path too long to bind (>107 bytes): {sock}")
302          if args.daemonize:
303              daemonize_args = ["-daemonize"]
304      elif args.daemonize:
305          raise ValueError("--daemonize needs --headless (a windowed QEMU has nowhere to go)")
306      # The guest's preferred mode. virtio-gpu-pci and virtio-gpu-gl-pci both
307      # take xres/yres, which set the EDID's preferred mode; the guest's DRM
308      # picks it and EmulationStation renders at it, so a handheld's 640x480
309      # is a VM check first (fork #97, D-QA-007). Without the flag QEMU's own
310      # default stands (1280x800), as before.
311      if args.res:
312          xres, yres = args.res
313          display_device = f"{display_device},xres={xres},yres={yres}"
314  
315      # SSH keeps a loopback bind unless --net lan is given (the image ships
316      # a well-known root password).
317      ssh_bind = "0.0.0.0" if args.net == "lan" else "127.0.0.1"
318      svc_bind = "0.0.0.0"
319  
320      # Running two guests at once needs a second forward: the profile pins one
321      # port, and a second VM would fail to bind it. The port the guest is told
322      # about has to move with it, or cloud_setup would print an SSH command
323      # pointing at the other machine.
324      if args.ssh_port or args.mac:
325          network = dict(network)
326      if args.ssh_port:
327          network["ssh_host_port"] = args.ssh_port
328          advertised = dict(network.get("advertised_ssh") or {})
329          advertised["host_port"] = args.ssh_port
330          network["advertised_ssh"] = advertised
331      # And its own MAC. NAT keeps two guests on the profile's address from
332      # colliding on any network, but cloud_device_id hashes the permanent MAC,
333      # so to the cloud they were one device (fork #91): the same folder, the
334      # same manifest, and two-device fixtures agreeing with themselves.
335      if args.mac:
336          network["mac_address"] = args.mac
337  
338      command = [
339          qemu,
340          "-name",
341          profile["name"],
342          "-machine",
343          profile["machine"],
344          "-accel",
345          accel,
346          "-cpu",
347          profile["cpu"],
348          "-smp",
349          str(profile["cpu_count"]),
350          "-m",
351          str(profile["memory_mib"]),
352          "-drive",
353          f"if=pflash,unit=0,readonly=on,format=raw,file={qemu_opt(code)}",
354          "-drive",
355          f"if=pflash,unit=1,format=raw,file={qemu_opt(vars_path)}",
356          "-drive",
357          (
358              f"if=none,id=rocknix,format={disk_info['format']},"
359              f"file={qemu_opt(disk)}"
360          ),
361          "-device",
362          (
363              f"{disk_profile['device']},drive=rocknix,"
364              f"logical_block_size={disk_profile['logical_block_size']},"
365              f"physical_block_size={disk_profile['physical_block_size']}"
366          ),
367          "-vga",
368          "none",
369          "-device",
370          display_device,
371          "-display",
372          display_arg,
373          *vnc_args,
374          "-netdev",
375          (
376              f"bridge,id=net0,br={args.bridge}"
377              if args.net == "bridged"
378              else (
379                  "user,id=net0,"
380                  f"hostfwd=tcp:{ssh_bind}:{network['ssh_host_port']}-:"
381                  f"{network['ssh_guest_port']}"
382                  + "".join(
383                      f",hostfwd=tcp:{svc_bind}:{fwd['host_port']}-:{fwd['guest_port']}"
384                      for fwd in network.get("extra_forwards", [])
385                  )
386              )
387          ),
388          "-device",
389          f"{network['device']},netdev=net0,mac={network['mac_address']}",
390          "-device",
391          "qemu-xhci",
392          "-device",
393          "usb-kbd",
394          "-device",
395          "usb-tablet",
396          "-device",
397          sound["device"],
398          "-device",
399          sound["codec"],
400          "-monitor",
401          f"unix:{qemu_opt(monitor)},server,nowait",
402          # Behind the NAT forward the guest's own address is unreachable, so
403          # the cloud-setup screen must show the loopback SSH command instead.
404          # Only the forwarded port is injected (a space-free token: UTM
405          # splits its argument list on whitespace, so a full command string
406          # would be broken apart); the guest quirk assembles the command.
407          *(
408              [
409                  "-fw_cfg",
410                  (
411                      f"name={network['advertised_ssh']['fwcfg_name']},"
412                      f"string={network['advertised_ssh']['host_port']}"
413                  ),
414              ]
415              if args.net != "bridged"
416              else []
417          ),
418          "-serial",
419          serial_arg,
420          *pidfile_args,
421          *daemonize_args,
422      ]
423      if profile["rng"]:
424          command += [
425              "-object",
426              "rng-random,id=rng0,filename=/dev/urandom",
427              "-device",
428              "virtio-rng-pci,rng=rng0",
429          ]
430      # A hardware watchdog, so the guest mirrors a handheld: systemd arms it
431      # (RuntimeWatchdogSec) and a kernel that stops scheduling is reset by it
432      # rather than left frozen (fork #104). i6300esb is QEMU's standard one and
433      # the kernel the image ships has its driver; "reset" is what the SoC's
434      # watchdog does on a device.
435      command += ["-device", "i6300esb", "-action", "watchdog=reset"]
436      return command
437  
438  
439  def utm_config(profile, image_name):
440      disk = profile["disk"]
441      display = profile["display"]
442      network = profile["network"]
443      sound = profile["sound"]
444      input_config = profile["input"]
445      notes = (
446          f"Canonical ROCKNIX GENERIC_X64 VM profile v{profile['profile_version']}: "
447          f"{profile['cpu']}, {profile['cpu_count']} vCPU, "
448          f"{profile['memory_mib']} MiB RAM, {profile['machine']} + UEFI, "
449          "VirtIO 512-byte disk, and virtio-gpu-gl."
450      )
451      return {
452          "Backend": "QEMU",
453          "ConfigurationVersion": 4,
454          "Display": [
455              {
456                  "DownscalingFilter": display["downscaling_filter"],
457                  "DynamicResolution": display["dynamic_resolution"],
458                  "Hardware": display["device"],
459                  "NativeResolution": display["native_resolution"],
460                  "UpscalingFilter": display["upscaling_filter"],
461              }
462          ],
463          "Drive": [
464              {
465                  "Identifier": "rocknix",
466                  "ImageName": image_name,
467                  "ImageType": "Disk",
468                  "Interface": disk["utm_interface"],
469                  "InterfaceVersion": 1,
470                  "ReadOnly": False,
471              }
472          ],
473          "Information": {
474              "IconCustom": False,
475              "Name": profile["name"],
476              "Notes": notes,
477              # Freshly generated per bundle: UTM identifies VMs by UUID, and
478              # identical UUIDs across downloaded revisions make UTM cross-wire
479              # library entries (manifesting as efi_vars.fd lock errors).
480              "UUID": str(uuid.uuid4()).upper(),
481          },
482          "Input": {
483              "MaximumUsbShare": input_config["maximum_usb_share"],
484              "UsbBusSupport": input_config["usb_bus_support"],
485              "UsbSharing": input_config["usb_sharing"],
486          },
487          "Network": [
488              {
489                  "Hardware": network["device"],
490                  "IsolateFromHost": False,
491                  # Random per bundle (QEMU OUI): bridged VMs join the LAN,
492                  # and duplicate MACs across copies would collide.
493                  "MacAddress": "52:54:00:%02X:%02X:%02X"
494                  % tuple(os.urandom(3)),
495                  # Bridged: the guest joins the LAN with its own address, like
496                  # real hardware (QR codes, phone access, SSH all work
497                  # verbatim). Port forwards only apply to emulated/shared NAT
498                  # modes, where services stay reachable through the host.
499                  "Mode": network["mode"],
500                  "PortForward": (
501                      []
502                      if network["mode"] == "Bridged"
503                      else [
504                          {
505                              "GuestPort": network["ssh_guest_port"],
506                              "HostAddress": "127.0.0.1",
507                              "HostPort": network["ssh_host_port"],
508                              "Protocol": "TCP",
509                          }
510                      ]
511                      + [
512                          {
513                              "GuestPort": fwd["guest_port"],
514                              "HostAddress": "0.0.0.0",
515                              "HostPort": fwd["host_port"],
516                              "Protocol": "TCP",
517                          }
518                          for fwd in network.get("extra_forwards", [])
519                      ]
520                  ),
521              }
522          ],
523          "QEMU": {
524              "AdditionalArguments": [
525                  "-global",
526                  f"virtio-blk-pci.logical_block_size={disk['logical_block_size']}",
527                  "-global",
528                  f"virtio-blk-pci.physical_block_size={disk['physical_block_size']}",
529              ]
530              # Behind the NAT forward the guest's own address is unreachable,
531              # so the cloud-setup screen must show the loopback SSH command
532              # instead. Only the forwarded port is injected (a space-free
533              # token: UTM splits its argument list on whitespace, so a full
534              # command string would be broken apart); the guest quirk
535              # assembles the command.
536              + (
537                  []
538                  if network["mode"] == "Bridged"
539                  else [
540                      "-fw_cfg",
541                      (
542                          f"name={network['advertised_ssh']['fwcfg_name']},"
543                          f"string={network['advertised_ssh']['host_port']}"
544                      ),
545                  ]
546              ),
547              "BalloonDevice": profile["balloon"],
548              # QA artifact: keep QEMU debug logging on so boot failures leave
549              # Data/debug.log inside the bundle for triage.
550              "DebugLog": True,
551              "Hypervisor": False,
552              "PS2Controller": False,
553              "RNGDevice": profile["rng"],
554              "RTCLocalTime": False,
555              "TPMDevice": profile["tpm"],
556              "TSO": False,
557              "UEFIBoot": True,
558          },
559          "Serial": [
560              {
561                  "Mode": "Terminal",
562                  "Target": "Auto",
563                  "Terminal": {
564                      "CursorBlink": True,
565                      "Font": "Menlo",
566                      "FontSize": 12,
567                      "Theme": "Default",
568                  },
569              }
570          ],
571          "Sharing": {
572              "ClipboardSharing": False,
573              "DirectoryShareMode": "None",
574              "DirectoryShareReadOnly": False,
575          },
576          "Sound": [{"Hardware": sound["device"]}],
577          "System": {
578              "Architecture": profile["architecture"],
579              "CPU": profile["cpu"],
580              "CPUCount": profile["cpu_count"],
581              "CPUFlagsAdd": [],
582              "CPUFlagsRemove": [],
583              "ForceMulticore": profile["force_multicore"],
584              "JITCacheSize": 0,
585              "MemorySize": profile["memory_mib"],
586              "Target": profile["machine"],
587          },
588      }
589  
590  
591  def build_utm(profile, args):
592      disk = Path(args.disk).resolve()
593      if not disk.is_file():
594          raise FileNotFoundError(f"disk does not exist: {disk}")
595      info = qemu_img_info(disk)
596      if info["format"] != "qcow2":
597          raise ValueError("UTM bundle input must be qcow2")
598      if info["virtual-size"] < profile["disk"]["virtual_size_bytes"]:
599          raise ValueError("qcow2 is smaller than the canonical 16 GiB VM disk")
600      # The bundle carries this one file, so a disk that needs another -- an
601      # overlay's backing image, an external data file -- would arrive on the
602      # other machine unable to open. Flatten it first (qemu-img convert).
603      backing = info.get("full-backing-filename") or info.get("backing-filename")
604      if backing:
605          raise ValueError(
606              f"qcow2 has a backing file ({backing}); a UTM bundle carries one file -- "
607              "flatten it first: qemu-img convert -O qcow2 <in> <out>"
608          )
609      data_file = ((info.get("format-specific") or {}).get("data") or {}).get("data-file")
610      if data_file:
611          raise ValueError(
612              f"qcow2 keeps its data in another file ({data_file}); a UTM bundle carries one file -- "
613              "convert it first: qemu-img convert -O qcow2 <in> <out>"
614          )
615  
616      output = Path(args.output).resolve()
617      output.parent.mkdir(parents=True, exist_ok=True)
618      bundle_name = output.name
619      for suffix in (".zip", ".utm"):
620          if bundle_name.endswith(suffix):
621              bundle_name = bundle_name[: -len(suffix)]
622      bundle_name += ".utm"
623      image_name = "ROCKNIX-GENERIC_X64.qcow2"
624      config = utm_config(profile, image_name)
625  
626      with tempfile.TemporaryDirectory(prefix="rocknix-utm-") as temp_dir:
627          config_path = Path(temp_dir) / "config.plist"
628          with config_path.open("wb") as stream:
629              plistlib.dump(config, stream, fmt=plistlib.FMT_XML, sort_keys=False)
630  
631          # The archive is written under a name only this build holds, beside
632          # the output (so the final rename stays on one filesystem), and
633          # renamed over the output once whole. A fixed name here let a second
634          # build for the same output remove the first one's unfinished file,
635          # or have its own published by the first.
636          handle, temporary_name = tempfile.mkstemp(
637              dir=output.parent, prefix=f".{output.name}.", suffix=".partial"
638          )
639          os.close(handle)
640          temporary_output = Path(temporary_name)
641          try:
642              with zipfile.ZipFile(
643                  temporary_output, "w", compression=zipfile.ZIP_STORED, allowZip64=True
644              ) as archive:
645                  archive.write(config_path, f"{bundle_name}/config.plist")
646                  archive.write(disk, f"{bundle_name}/Data/{image_name}")
647                  # Quick-start notes shipped next to the bundle (not inside it:
648                  # macOS treats .utm as an opaque document).
649                  archive.write(
650                      VM_DIR / "utm-bundle-readme.txt", "READ ME FIRST.txt"
651                  )
652              # mkstemp makes the file 0600; give it what a plain create would
653              # have had under the caller's umask, no more.
654              umask = os.umask(0)
655              os.umask(umask)
656              os.chmod(temporary_output, 0o666 & ~umask)
657              os.replace(temporary_output, output)
658          except BaseException:
659              temporary_output.unlink(missing_ok=True)
660              raise
661      print(output)
662  
663  
664  def add_qemu_options(parser):
665      parser.add_argument("disk", help="ROCKNIX qcow2 disk")
666      parser.add_argument("--accel", default="auto", help="QEMU accelerator (default: auto)")
667      parser.add_argument(
668          "--net",
669          choices=["user", "lan", "bridged"],
670          default="user",
671          help=(
672              "networking: 'user' (default; SSH forward on loopback only), "
673              "'lan' (exposes the SSH forward on the LAN), or 'bridged' (guest joins "
674              "the LAN directly; needs a host bridge + qemu-bridge-helper "
675              "allow rule)"
676          ),
677      )
678      parser.add_argument("--bridge", default="br0", help="bridge name for --net bridged (default: br0)")
679      parser.add_argument(
680          "--display",
681          default=os.environ.get("ROCKNIX_QEMU_DISPLAY", "gtk,gl=on"),
682          help="QEMU -display value (default: gtk,gl=on)",
683      )
684      parser.add_argument("--monitor", default="/tmp/rocknix-qemu-monitor.sock")
685      parser.add_argument(
686          "--headless",
687          action="store_true",
688          help=(
689              "no window: virtio-gpu-pci with -display none, a VNC scanout on "
690              "loopback (--vnc), the serial console on a unix socket (--serial) "
691              "and a --pidfile; for build hosts without a desktop"
692          ),
693      )
694      parser.add_argument("--serial", default="/tmp/rocknix-qemu-serial.sock", help="serial console socket with --headless")
695      parser.add_argument(
696          "--gl",
697          default=os.environ.get("ROCKNIX_QEMU_GL", "auto"),
698          help=(
699              "hardware GL for a --headless guest through virgl: auto (the first "
700              "host render node not driven by nvidia; the default, also "
701              "ROCKNIX_QEMU_GL), none (software rendering), or a /dev/dri/renderD* node"
702          ),
703      )
704      parser.add_argument("--vnc", type=int, default=9, help="VNC display number with --headless (default: 9, port 5909)")
705      parser.add_argument("--pidfile", default="/tmp/rocknix-qemu.pid", help="QEMU pidfile with --headless")
706      parser.add_argument(
707          "--daemonize",
708          action="store_true",
709          help="with --headless: return once the VM is up, leaving it running (stop it with kill $(cat pidfile))",
710      )
711      parser.add_argument(
712          "--ssh-port",
713          type=tcp_port,
714          default=None,
715          help=(
716              "host port to forward to the guest's SSH (default: the profile's). "
717              "Give a second VM its own port -- and its own --monitor -- to run "
718              "two at once for multi-device testing"
719          ),
720      )
721      parser.add_argument(
722          "--mac",
723          type=mac_address,
724          default=None,
725          help=(
726              "the guest NIC's MAC address (default: the profile's). Give a second "
727              "VM its own: cloud_device_id hashes the permanent MAC, so two guests "
728              "on the profile's address are one device to the cloud"
729          ),
730      )
731      parser.add_argument(
732          "--res",
733          type=resolution,
734          default=None,
735          metavar="WxH",
736          help=(
737              "the guest display's preferred mode, e.g. 640x480 -- appended to the "
738              "virtio-gpu device as xres/yres, for the desktop and headless variants "
739              "alike (default: QEMU's own, 1280x800). Check a handheld panel's look "
740              "on the VM first"
741          ),
742      )
743      parser.add_argument("--ovmf-code")
744      parser.add_argument("--ovmf-vars-template")
745      parser.add_argument("--ovmf-vars")
746  
747  
748  def resolution(value):
749      """WxH, both decimal and nonzero, as the (W, H) pair. QEMU would reject a
750      malformed xres= only once it starts; argparse says no before that."""
751      m = re.fullmatch(r"(\d+)x(\d+)", value)
752      if not m or "0" in (m.group(1).lstrip("0") or "0", m.group(2).lstrip("0") or "0"):
753          raise argparse.ArgumentTypeError(f"not a resolution (WxH, e.g. 640x480): {value!r}")
754      return int(m.group(1)), int(m.group(2))
755  
756  
757  def tcp_port(value):
758      """A TCP port, 1 to 65535. QEMU rejects anything else only once it starts,
759      after the sockets and pidfile have been claimed; argparse says no before
760      that."""
761      try:
762          port = int(value, 10)
763      except ValueError:
764          port = 0
765      if not 1 <= port <= 65535:
766          raise argparse.ArgumentTypeError(f"not a TCP port (1-65535): {value!r}")
767      return port
768  
769  
770  def mac_address(value):
771      """Six hex pairs joined by colons. QEMU rejects anything else only once it
772      starts, after the sockets and pidfile have been claimed; argparse says no
773      before that."""
774      if not re.fullmatch(r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", value):
775          raise argparse.ArgumentTypeError(f"not a MAC address (aa:bb:cc:dd:ee:ff): {value!r}")
776      return value
777  
778  
779  def main():
780      parser = argparse.ArgumentParser(
781          description="Run and package the canonical ROCKNIX GENERIC_X64 VM profile"
782      )
783      subparsers = parser.add_subparsers(dest="command", required=True)
784  
785      subparsers.add_parser("profile", help="print the canonical profile")
786  
787      args_parser = subparsers.add_parser("qemu-args", help="print the Linux QEMU command")
788      add_qemu_options(args_parser)
789  
790      run_parser = subparsers.add_parser("run", help="run the profile with QEMU")
791      add_qemu_options(run_parser)
792  
793      utm_parser = subparsers.add_parser("utm", help="build a macOS .utm.zip bundle")
794      utm_parser.add_argument("disk", help="pre-sized ROCKNIX qcow2 disk")
795      utm_parser.add_argument("--output", required=True)
796  
797      args = parser.parse_args()
798      profile = load_profile()
799      if args.command == "profile":
800          print(json.dumps(profile, indent=2))
801      elif args.command == "utm":
802          build_utm(profile, args)
803      else:
804          command = qemu_command(profile, args)
805          if args.command == "qemu-args":
806              print(shlex.join(command))
807          else:
808              prepare_run(profile, args)
809              os.execv(command[0], command)
810  
811  
812  if __name__ == "__main__":
813      try:
814          main()
815      except (FileNotFoundError, PermissionError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
816          print(f"error: {error}", file=sys.stderr)
817          sys.exit(1)
```


## projects/ROCKNIX/options @ 8ebaf8daad (whole, line-numbered)

```text
 1  ################################################################################
 2  # setup build defaults
 3  ################################################################################
 4  
 5    # Project FLAGS
 6      PROJECT_CFLAGS=""
 7  
 8    # SquashFS compression method (gzip / lzo / xz)
 9      SQUASHFS_COMPRESSION="zstd"
10  
11  ################################################################################
12  # setup project defaults
13  ################################################################################
14  
15    # OpenGL(X) implementation to use (no / mesa)
16      OPENGL="mesa"
17  
18    # OpenGL-ES implementation to use (no / mesa)
19      OPENGLES="mesa"
20  
21    # Displayserver to use (no / wl)
22      DISPLAYSERVER="no"
23  
24    # Windowmanager to use (none / weston)
25      WINDOWMANAGER="none"
26  
27    # Xorg Graphic drivers to use (all / i915,i965,r200,r300,r600,nvidia)
28    # Space separated list is supported,
29    # e.g. GRAPHIC_DRIVERS="i915 i965 r300 r600 radeonsi nvidia"
30      GRAPHIC_DRIVERS=""
31  
32    # Additional Firmware to use ( )
33    # Space separated list is supported,
34    # e.g. FIRMWARE=""
35      FIRMWARE=""
36  
37    # Additional packages to install
38      ADDITIONAL_PACKAGES=""
39  
40    # Satisfy legacy build dependencies
41      SWAP_SUPPORT="yes"
```


## projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/package.mk @ 8ebaf8daad (whole, line-numbered)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="device-tree-overlays"
 5  PKG_VERSION="1.0"
 6  PKG_LICENSE="GPL2"
 7  PKG_SITE="https://rocknix.org"
 8  PKG_LONGDESC="device-tree-overlays: ROCKNIX linux device tree overlays"
 9  PKG_TOOLCHAIN="manual"
10  PKG_IS_KERNEL_PKG="yes"
11  
12  make_target() {
13    for dts in ${PKG_BUILD}/${DEVICE}/*.dts; do
14      $(kernel_path)/scripts/dtc/dtc -@ -I dts -O dtb -o ${dts%.dts}.dtbo ${dts}
15    done
16  }
17  
18  makeinstall_target() {
19    mkdir -p ${INSTALL}/usr/share/bootloader/overlays
20      cp -a ${PKG_BUILD}/${DEVICE}/*.dtbo ${INSTALL}/usr/share/bootloader/overlays
21  
22    if [ ${DEVICE} != "RK3326" ]; then
23      mkdir -p ${INSTALL}/usr/bin
24        cp -a ${PKG_BUILD}/dtb_overlay ${INSTALL}/usr/bin
25    fi
26  }
```


## projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/dtb_overlay @ 8ebaf8daad (whole, line-numbered)

```text
  1  #!/bin/sh
  2  # SPDX-License-Identifier: GPL-2.0
  3  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
  4  . /etc/profile.d/001-functions
  5  SPECIALIZATIONS="undervolt-cpu undervolt-gpu driver-gpu"
  6  
  7  check_valid_specialization() {
  8      for spec in $SPECIALIZATIONS; do
  9          if [ "$spec" = "${1}" ]; then
 10              return
 11          fi
 12      done
 13      echo "Unknown specialization: ${1}"
 14      echo "Valid specializations are: ${SPECIALIZATIONS}"
 15      exit 1
 16  }
 17  
 18  get_current_custom_overlay() {
 19      fdtoverlaysline=$(grep FDTOVERLAYS /flash/extlinux/extlinux.conf)
 20      overlays=${fdtoverlaysline##  FDTOVERLAYS}
 21      for ol in $overlays; do
 22          match=0
 23          for spec in $SPECIALIZATIONS; do
 24              if [[ $ol == *"$spec"* ]]; then
 25                 match=1
 26                 break
 27              fi
 28          done
 29          if [ $match = 0 ]; then
 30              custom=$ol
 31              break
 32          fi
 33      done
 34      if [ $custom ]; then
 35          echo $custom | cut -d '/' -f 3
 36      else
 37          echo "None"
 38      fi
 39  }
 40  
 41  get_current_specialized_overlay() {
 42      fdtoverlaysline=$(grep FDTOVERLAYS /flash/extlinux/extlinux.conf)
 43      overlays=${fdtoverlaysline##  FDTOVERLAYS}
 44      for ol in $overlays; do
 45          if [[ $ol == *"$1"* ]]; then
 46              specialized="${ol} "
 47              break
 48          fi
 49      done
 50      if [ $specialized ]; then
 51          echo $specialized | cut -d '/' -f 3
 52      else
 53          echo "None"
 54      fi
 55  
 56  }
 57  
 58  list_custom_overlays() {
 59      for ol in /flash/overlays/*.dtbo; do
 60          for spec in $SPECIALIZATIONS; do
 61              if [[ $ol == *"$spec"* ]]; then
 62                  ol=""
 63          break
 64              fi
 65          done
 66          if [ $ol ]; then
 67              echo -n $ol | cut -d '/' -f 4 | tr -d '\n'
 68              echo -n " "
 69          fi
 70      done
 71      echo
 72  }
 73  
 74  list_specialized_overlays() {
 75      for ol in /flash/overlays/*.dtbo; do
 76          if [[ $ol == *"$1"* ]]; then
 77              echo -n $ol | cut -d '/' -f 4 | tr -d '\n'
 78              echo -n " "
 79          fi
 80      done
 81      echo
 82  }
 83  
 84  write_dtbo() {
 85      PRE=/overlays/
 86      for spec in $SPECIALIZATIONS custom_dtbo; do
 87  	ol=$(get_setting system.$spec)
 88          if [ "$ol" != "None" ] && [[ ! -z $ol ]]; then
 89              dtbos+="${PRE}${ol} "
 90          fi
 91      done
 92      mount -o remount,rw /flash
 93      if [ "$dtbos" ]; then
 94          if grep --quiet FDTOVERLAYS /flash/extlinux/extlinux.conf; then
 95              sed -i "/FDTOVERLAYS/c \ \ FDTOVERLAYS ${dtbos}" /flash/extlinux/extlinux.conf
 96          else
 97              sed -i "/FDT/a \ \ FDTOVERLAYS ${dtbos}" /flash/extlinux/extlinux.conf
 98          fi
 99      else
100          sed -i "/FDTOVERLAYS/d" /flash/extlinux/extlinux.conf
101      fi
102      mount -o remount,ro /flash
103  }
104  
105  case "$1" in
106      "ls")
107          case "$2" in
108              "custom")
109                  list_custom_overlays
110                  exit 0
111              ;;
112              *)
113                  check_valid_specialization $2
114                  list_specialized_overlays $2
115                  exit 0
116              ;;
117          esac
118      ;;
119      "get")
120          case "$2" in
121              "custom")
122                  get_current_custom_overlay
123                  exit 0
124              ;;
125              *)
126                  check_valid_specialization $2
127                  get_current_specialized_overlay $2
128                  exit 0
129              ;;
130          esac
131      ;;
132     "set")
133          case "$2" in
134              "custom")
135                  for ol in $(list_custom_overlays); do
136  		            if [ "$3" = "$ol" ] || [ $3 = None ]; then
137                          set_setting system.custom_dtbo $3
138                          write_dtbo
139                          exit 0
140  		            fi
141  		        done
142                  echo "dtbo doesn't exist: $3"
143                  exit 1
144              ;;
145              *)
146                  check_valid_specialization $2
147  	            for ol in $(list_specialized_overlays $2); do
148  		            if [ "$3" = "$ol" ] || [ $3 = None ]; then
149                          set_setting system.$2 $3
150                          write_dtbo
151                          exit 0
152  		            fi
153  		        done
154                  echo "dtbo doesn't exist: $3"
155                  exit 1
156              ;;
157          esac
158      ;;
159      *)
160          echo "Unknown operation: ${1}"
161          exit 1
162      ;;
163  esac
```


## projects/ROCKNIX/packages/linux-drivers/rocknix-joypad/package.mk @ 8ebaf8daad (whole, line-numbered)

```text
 1  # SPDX-License-Identifier: GPL-2.0-or-later
 2  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
 3  
 4  PKG_NAME="rocknix-joypad"
 5  PKG_VERSION="d02ed13aae08113f6f9e0e9d699cb29bb3450fa2"
 6  PKG_SHA256="89ade1769d6eb7b4f37265f26407a422cdbcf517487f80eb1c29964904ca138e"
 7  PKG_LICENSE="GPL"
 8  PKG_SITE="https://github.com/ROCKNIX/rocknix-joypad"
 9  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
10  PKG_LONGDESC="rocknix-joypad: ROCKNIX joypad driver"
11  PKG_TOOLCHAIN="manual"
12  PKG_IS_KERNEL_PKG="yes"
13  
14  pre_make_target() {
15    unset LDFLAGS
16  }
17  
18  make_target() {
19    kernel_make -C $(kernel_path) M=${PKG_BUILD}
20  }
21  
22  makeinstall_target() {
23    mkdir -p ${INSTALL}/$(get_full_module_dir)/${PKG_NAME}
24      cp *.ko ${INSTALL}/$(get_full_module_dir)/${PKG_NAME}
25  }
```


## projects/ROCKNIX/packages/linux-firmware/extra-firmware/package.mk @ 8ebaf8daad (whole, line-numbered)

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


## projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk @ 8ebaf8daad (whole, line-numbered)

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


## projects/ROCKNIX/packages/linux/package.mk @ 8ebaf8daad (whole, line-numbered)

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
121   : # reuse make_target()
122  }
123  
124  makeinstall_init() {
125    :
126  }
127  
128  make_host() {
129    :
130  }
131  
132  makeinstall_host() {
133    make \
134      ARCH=${HEADERS_ARCH:-${TARGET_KERNEL_ARCH}} \
135      HOSTCC="${TOOLCHAIN}/bin/host-gcc" \
136      HOSTCXX="${TOOLCHAIN}/bin/host-g++" \
137      HOSTCFLAGS="${HOST_CFLAGS}" \
138      HOSTCXXFLAGS="${HOST_CXXFLAGS}" \
139      HOSTLDFLAGS="${HOST_LDFLAGS}" \
140      INSTALL_HDR_PATH=dest \
141      headers_install
142    mkdir -p ${SYSROOT_PREFIX}/usr/include
143      cp -R dest/include/* ${SYSROOT_PREFIX}/usr/include
144  }
145  
146  pre_make_target() {
147    ( cd ${ROOT}
148      rm -rf ${BUILD}/initramfs
149      rm -f ${STAMPS_INSTALL}/initramfs/install_target ${STAMPS_INSTALL}/*/install_init
150      ${SCRIPTS}/install initramfs
151    )
152    pkg_lock_status "ACTIVE" "linux:target" "build"
153  
154    cp ${PKG_KERNEL_CFG_FILE} ${PKG_BUILD}/.config
155  
156    # set initramfs source
157    ${PKG_BUILD}/scripts/config --set-str CONFIG_INITRAMFS_SOURCE "$(kernel_initramfs_confs) ${BUILD}/initramfs"
158  
159    # Keep the RC2 network identity across the display rename (D-WORKFLOW-123).
160    ${PKG_BUILD}/scripts/config --set-str CONFIG_DEFAULT_HOSTNAME "ROCKNIX"
161  
162    # disable swap support if not enabled
163    if [ ! "${SWAP_SUPPORT}" = yes ]; then
164      ${PKG_BUILD}/scripts/config --disable CONFIG_SWAP
165    fi
166  
167    # disable nfs support if not enabled
168    if [ "${NFS_SUPPORT}" = no ]; then
169      ${PKG_BUILD}/scripts/config --disable CONFIG_NFS_FS
170    fi
171  
172    # disable cifs support if not enabled
173    if [ ! "${SAMBA_SUPPORT}" = yes ]; then
174      ${PKG_BUILD}/scripts/config --disable CONFIG_CIFS
175    fi
176  
177    # disable iscsi support if not enabled
178    if [ ! "${ISCSI_SUPPORT}" = yes ]; then
179      ${PKG_BUILD}/scripts/config --disable CONFIG_SCSI_ISCSI_ATTRS
180      ${PKG_BUILD}/scripts/config --disable CONFIG_ISCSI_TCP
181      ${PKG_BUILD}/scripts/config --disable CONFIG_ISCSI_BOOT_SYSFS
182      ${PKG_BUILD}/scripts/config --disable CONFIG_ISCSI_IBFT_FIND
183      ${PKG_BUILD}/scripts/config --disable CONFIG_ISCSI_IBFT
184    fi
185  
186    # disable lima/panfrost if libmali is configured
187    if [ "${OPENGLES}" = "libmali" ]; then
188      ${PKG_BUILD}/scripts/config --disable CONFIG_DRM_LIMA
189      ${PKG_BUILD}/scripts/config --disable CONFIG_DRM_PANFROST
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
291    # goes with it because CONFIG_CFG80211_REQUIRE_SIGNED_REGDB is set. Appends to
292    # whatever the per-device blocks above already listed (~7 KB in the image).
293    if grep -q '^CONFIG_CFG80211=y' ${PKG_BUILD}/.config; then
294      mkdir -p ${PKG_BUILD}/external-firmware
295        cp -Lv $(get_build_dir wireless-regdb)/regulatory.db ${PKG_BUILD}/external-firmware
296        cp -Lv $(get_build_dir wireless-regdb)/regulatory.db.p7s ${PKG_BUILD}/external-firmware
297  
298      FW_LIST="$(${PKG_BUILD}/scripts/config --state CONFIG_EXTRA_FIRMWARE)"
299      [ "${FW_LIST}" = "undef" ] && FW_LIST=""
300  
301      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE \
302        "$(echo ${FW_LIST} regulatory.db regulatory.db.p7s | xargs)"
303      ${PKG_BUILD}/scripts/config --set-str CONFIG_EXTRA_FIRMWARE_DIR "external-firmware"
304    fi
305  
306    kernel_make listnewconfig
307    if [ "${INTERACTIVE_CONFIG}" = "yes" ]; then
308      # manually answer .config changes
309      kernel_make oldconfig
310    elif [ "${INTERACTIVE_CONFIG}" = "menuconfig" ]; then
311      # manually answer .config changes
312      kernel_make menuconfig
313    else
314      # accept default answers for .config changes
315      yes "" | kernel_make oldconfig > /dev/null
316    fi
317  
318    if [ -f "${DISTRO_DIR}/${DISTRO}/kernel_options" ]; then
319      while read OPTION; do
320        [ -z "${OPTION}" -o -n "$(echo "${OPTION}" | grep '^#')" ] && continue
321  
322        if [ "${OPTION##*=}" == "n" -a "$(${PKG_BUILD}/scripts/config --state ${OPTION%%=*})" == "undef" ]; then
323          continue
324        fi
325  
326        if [ "$(${PKG_BUILD}/scripts/config --state ${OPTION%%=*})" != "$(echo ${OPTION##*=} | tr -d '"')" ]; then
327          MISSING_KERNEL_OPTIONS+="\t${OPTION}\n"
328        fi
329      done < ${DISTRO_DIR}/${DISTRO}/kernel_options
330  
331      if [ -n "${MISSING_KERNEL_OPTIONS}" ]; then
332        print_color CLR_WARNING "LINUX: kernel options not correct: \n${MISSING_KERNEL_OPTIONS%%}\nPlease run ./tools/check_kernel_config\n"
333      fi
334    fi
335  }
336  
337  make_target() {
338    DTC_FLAGS=-@ kernel_make ${KERNEL_TARGET} ${KERNEL_MAKE_EXTRACMD} modules
339  
340    if [ "${PKG_BUILD_PERF}" = "yes" ]; then
341      ( cd tools/perf
342  
343        # arch specific perf build args
344        case "${TARGET_ARCH}" in
345          x86_64|i*86)
346            PERF_BUILD_ARGS="ARCH=x86"
347            ;;
348          aarch64)
349            PERF_BUILD_ARGS="ARCH=arm64"
350            ;;
351          *)
352            PERF_BUILD_ARGS="ARCH=${TARGET_ARCH}"
353            ;;
354        esac
355  
356        [[ "${DEVICE}" != "RK3588" ]] && export BUILD_BPF_SKEL=0
357  
358        WERROR=0 \
359        NO_LIBPERL=1 \
360        NO_LIBPYTHON=1 \
361        NO_SLANG=1 \
362        NO_GTK2=1 \
363        NO_LIBNUMA=1 \
364        NO_LIBAUDIT=1 \
365        NO_LIBTRACEEVENT=1 \
366        NO_LZMA=1 \
367        NO_SDT=1 \
368        NO_LIBDEBUGINFOD=1 \
369        NO_JVMTI=1 \
370        NO_LIBLLVM=1 \
371        NO_LIBPFM4=1 \
372        NO_LIBBABELTRACE=1 \
373        NO_CAPSTONE=1 \
374        CROSS_COMPILE="${TARGET_PREFIX}" \
375        JOBS="${CONCURRENCY_MAKE_LEVEL}" \
376          make ${PERF_BUILD_ARGS}
377        mkdir -p ${INSTALL}/usr/bin
378          cp perf ${INSTALL}/usr/bin
379      )
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


## projects/ROCKNIX/packages/linux/udev.d/10-bfq-sched.rules @ 8ebaf8daad (whole, line-numbered)

```text
1  ACTION=="add|change", KERNEL=="mmcbl*", ATTR{queue/scheduler}="bfq"
```


## projects/ROCKNIX/packages/linux/udev.d/30-disable-wakeup.rules @ 8ebaf8daad (whole, line-numbered)

```text
 1  # SPDX-License-Identifier: GPL-2.0-or-later
 2  # Copyright (C) 2009-2014 Stephan Raue (stephan@openelec.tv)
 3  # Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)
 4  
 5  ACTION!="add|change", GOTO="end"
 6  
 7  DRIVER=="ehci-pci|xhci_hcd", RUN+="/usr/bin/sh -c 'echo disabled > /sys$devpath/power/wakeup'"
 8  
 9  LABEL="end"
```


## projects/ROCKNIX/packages/linux/udev.d/40-usb_modeswitch.rules @ 8ebaf8daad (whole, line-numbered)

```text
 1  # SPDX-License-Identifier: GPL-2.0-or-later
 2  # Copyright (C) 2009-2014 Stephan Raue (stephan@openelec.tv)
 3  
 4  ACTION!="add|change", GOTO="end_modeswitch"
 5  
 6  # Atheros Wireless / Netgear WNDA3200
 7  ATTRS{idVendor}=="0cf3", ATTRS{idProduct}=="20ff", RUN+="/usr/bin/eject '/dev/%k'"
 8  
 9  # Realtek RTL8821CU chipset 802.11ac NIC
10  #   initial cdrom mode 0bda:1a2b, wlan mode 0bda:c811
11  # Odroid WiFi Module 5B
12  #   initial cdrom mode 0bda:1a2b, wlan mode 0bda:c820
13  ATTR{idVendor}=="0bda", ATTR{idProduct}=="1a2b", RUN+="/usr/sbin/usb_modeswitch -K -v 0bda -p 1a2b"
14  ATTR{idVendor}=="0bda", ATTR{idProduct}=="c811", RUN+="/usr/sbin/usb_modeswitch -K -v 0bda -p c811"
15  
16  LABEL="end_modeswitch"
```


## projects/ROCKNIX/bootloader/install @ 8ebaf8daad (whole, line-numbered)

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
76      fi
77      ;;
78  esac
79  
80  echo "install: ROCKNIX bootloader installation completed for ${BOOTLOADER}"
```


## projects/ROCKNIX/bootloader/mkimage @ 8ebaf8daad (whole, line-numbered)

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


## projects/ROCKNIX/bootloader/release @ 8ebaf8daad (whole, line-numbered)

```text
1  # SPDX-License-Identifier: GPL-2.0
2  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
3  
4  mkdir -p ${RELEASE_DIR}/3rdparty/bootloader
5    cp -a ${INSTALL}/usr/share/bootloader/* ${RELEASE_DIR}/3rdparty/bootloader
```


## projects/ROCKNIX/bootloader/rkhelper @ 8ebaf8daad (whole, line-numbered)

```text
 1  # SPDX-License-Identifier: GPL-2.0
 2  # Copyright (C) 2024-present ROCKNIX (https://rocknix.org)
 3  
 4  PKG_SOC="${DEVICE/RK/rk}"
 5  
 6  # Make idbloader.img
 7  case "${DEVICE}" in
 8    RK3326)
 9      # mkimage does not support packing second level bootloader on rk3326
10      ${PKG_BUILD}/tools/mkimage -n px30 -T rksd -d "${PKG_DDR_BIN}" -C bzip2 idbloader.img
11      cat ${PKG_MINILOADER} >> idbloader.img
12      ;;
13    RK3399|RK3566|RK3576|RK3588)
14      [ "${PKG_SOC}" = "rk3566" ] && PKG_SOC="rk3568"
15      ${PKG_BUILD}/tools/mkimage -n "${PKG_SOC}" -T rksd -d "${PKG_DDR_BIN}":"${PKG_MINILOADER}" -C bzip2 idbloader.img
16      ;;
17  esac
18  
19  # Pack uboot.img
20  case "${DEVICE}" in
21    RK3326|RK3399)
22      ${PKG_RKBIN}/tools/loaderimage --pack --uboot u-boot-dtb.bin uboot.img 0x00200000
23      ;;
24  esac
25  
26  # Merge trust.img
27  case "${DEVICE}" in
28    RK3326)
29      cat >trust.ini <<EOF
30  [BL30_OPTION]
31  SEC=0
32  [BL31_OPTION]
33  SEC=1
34  PATH=${PKG_BL31}
35  ADDR=0x00010000
36  [BL32_OPTION]
37  SEC=0
38  [BL33_OPTION]
39  SEC=0
40  [OUTPUT]
41  PATH=trust.img
42  EOF
43      ${PKG_RKBIN}/tools/trust_merger --verbose trust.ini
44      ;;
45    RK3399)
46      ${PKG_RKBIN}/tools/trust_merger --ignore-bl32 --prepath "${PKG_RKBIN}"/ "${PKG_ATF_INI}"
47      ;;
48  esac
49  
50  # Build a unified uboot.bin image
51  dd if=idbloader.img of=uboot.bin bs=512 seek=0 conv=fsync,notrunc
52  for BOOT_IMAGE in uboot.img u-boot.itb; do
53    if [ -f "$BOOT_IMAGE" ]; then
54      dd if=$BOOT_IMAGE of=uboot.bin bs=512 seek=16320 conv=fsync,notrunc
55      break
56    fi
57  done
58  if [ -f "trust.img" ]; then
59    dd if=trust.img of=uboot.bin bs=512 seek=24512 conv=fsync,notrunc
60  fi
```


## projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf @ 8ebaf8daad: lines 1-8 (the header)

```text
1  #
2  # Automatically generated file; DO NOT EDIT.
3  # Linux/x86 6.15.6 Kernel Configuration
4  #
5  CONFIG_CC_VERSION_TEXT="x86_64-libreelec-linux-gnu-gcc-15.1.0 (GCC) 15.1.0"
6  CONFIG_CC_IS_GCC=y
7  CONFIG_GCC_VERSION=150100
8  CONFIG_CLANG_VERSION=0
```


## diff projects/Generic/linux/linux.x86_64.conf (<) ours (>) @ 8ebaf8daad (659 removed, 351 added)

```text
3c3
< # Linux/x86 7.1.2 Kernel Configuration
---
> # Linux/x86 6.15.6 Kernel Configuration
5c5
< CONFIG_CC_VERSION_TEXT="x86_64-libreelec-linux-gnu-gcc-16.1.0 (GCC) 16.1.0"
---
> CONFIG_CC_VERSION_TEXT="x86_64-libreelec-linux-gnu-gcc-15.1.0 (GCC) 15.1.0"
7c7
< CONFIG_GCC_VERSION=160100
---
> CONFIG_GCC_VERSION=150100
10c10
< CONFIG_AS_VERSION=24601
---
> CONFIG_AS_VERSION=24400
12c12
< CONFIG_LD_VERSION=24601
---
> CONFIG_LD_VERSION=24400
16d15
< CONFIG_RUSTC_LLVM_MAJOR_VERSION=0
22d20
< CONFIG_CC_HAS_ASSUME=y
25d22
< CONFIG_CC_HAS_COUNTED_BY_PTR=y
63a61
> # CONFIG_USELIB is not set
88d85
< CONFIG_ARCH_WANTS_CLOCKSOURCE_READ_INLINE=y
94,95d90
< CONFIG_GENERIC_CLOCKEVENTS_COUPLED=y
< CONFIG_GENERIC_CLOCKEVENTS_COUPLED_INLINE=y
97d91
< CONFIG_HRTIMER_REARM_DEFERRED=y
113c107
< # CONFIG_POSIX_AUX_CLOCKS is not set
---
> CONFIG_CLOCKSOURCE_WATCHDOG_MAX_SKEW_US=100
129c123
< CONFIG_PREEMPT_BUILD=y
---
> CONFIG_PREEMPT_VOLUNTARY_BUILD=y
131c125,127
< CONFIG_PREEMPT=y
---
> # CONFIG_PREEMPT_NONE is not set
> CONFIG_PREEMPT_VOLUNTARY=y
> # CONFIG_PREEMPT is not set
134,135d129
< CONFIG_PREEMPT_COUNT=y
< CONFIG_PREEMPTION=y
158d151
< CONFIG_PREEMPT_RCU=y
163d155
< CONFIG_TASKS_RCU=y
182d173
< # CONFIG_SCHED_PROXY_EXEC is not set
189d179
< CONFIG_CC_MS_EXTENSIONS="-fms-extensions"
207d196
< CONFIG_GROUP_SCHED_BANDWIDTH=y
228d216
< CONFIG_TIME_NS_VDSO=y
240,245c228,233
< # CONFIG_RD_GZIP is not set
< # CONFIG_RD_BZIP2 is not set
< # CONFIG_RD_LZMA is not set
< # CONFIG_RD_XZ is not set
< # CONFIG_RD_LZO is not set
< # CONFIG_RD_LZ4 is not set
---
> CONFIG_RD_GZIP=y
> CONFIG_RD_BZIP2=y
> CONFIG_RD_LZMA=y
> CONFIG_RD_XZ=y
> CONFIG_RD_LZO=y
> CONFIG_RD_LZ4=y
247c235
< # CONFIG_INITRAMFS_COMPRESSION_ZSTD is not set
---
> # CONFIG_INITRAMFS_COMPRESSION_GZIP is not set
252d239
< CONFIG_CMDLINE_LOG_WRAP_IDEAL_LEN=1021
274,275d260
< CONFIG_FUTEX_PRIVATE_HASH=y
< CONFIG_FUTEX_MPOL=y
283d267
< # CONFIG_IO_URING_MOCK_FILE is not set
288,290c272
< # CONFIG_RSEQ_SLICE_EXTENSION is not set
< # CONFIG_RSEQ_STATS is not set
< # CONFIG_RSEQ_DEBUG_DEFAULT_ENABLE is not set
---
> # CONFIG_DEBUG_RSEQ is not set
291a274
> # CONFIG_PC104 is not set
317,322d299
< 
< #
< # Live Update and Kexec HandOver
< #
< # CONFIG_KEXEC_HANDOVER is not set
< # end of Live Update and Kexec HandOver
346a324
> CONFIG_X86_64_SMP=y
349c327
< CONFIG_PGTABLE_LEVELS=5
---
> CONFIG_PGTABLE_LEVELS=4
367a346
> # CONFIG_PARAVIRT_DEBUG is not set
378d356
< # CONFIG_BHYVE_GUEST is not set
380,381d357
< CONFIG_CC_HAS_MARCH_NATIVE=y
< # CONFIG_X86_NATIVE_CPU is not set
408a385,387
> # CONFIG_SCHED_CLUSTER is not set
> CONFIG_SCHED_SMT=y
> CONFIG_SCHED_MC=y
433d411
< # CONFIG_MICROCODE_DBG is not set
435a414
> # CONFIG_X86_5LEVEL is not set
484d462
< CONFIG_ARCH_SUPPORTS_KEXEC_HANDOVER=y
492a471
> CONFIG_DYNAMIC_MEMORY_LAYOUT=y
499c478
< CONFIG_CMDLINE="root=/dev/ram0 rdinit=/init usbcore.autosuspend=-1"
---
> CONFIG_CMDLINE="root=/dev/sda1 init=/sbin/init usbcore.autosuspend=-1"
504d482
< CONFIG_HAVE_KLP_BUILD=y
559d536
< # CONFIG_PM_QOS_CPU_SYSTEM_WAKEUP is not set
624d600
< CONFIG_ACPI_MRRM=y
707d682
< CONFIG_X86_REQUIRED_FEATURE_SYSFAST32=y
721a697
> CONFIG_X86_DISABLED_FEATURE_LA57=y
728a705,711
> CONFIG_AS_AVX512=y
> CONFIG_AS_SHA1_NI=y
> CONFIG_AS_SHA256_NI=y
> CONFIG_AS_TPAUSE=y
> CONFIG_AS_GFNI=y
> CONFIG_AS_VAES=y
> CONFIG_AS_VPCLMULQDQ=y
737,742d719
< CONFIG_ARCH_SUPPORTS_SCHED_SMT=y
< CONFIG_ARCH_SUPPORTS_SCHED_CLUSTER=y
< CONFIG_ARCH_SUPPORTS_SCHED_MC=y
< CONFIG_SCHED_SMT=y
< # CONFIG_SCHED_CLUSTER is not set
< CONFIG_SCHED_MC=y
748,749d724
< CONFIG_GENERIC_IRQ_ENTRY=y
< CONFIG_GENERIC_SYSCALL=y
792,793d766
< CONFIG_UNWIND_USER=y
< CONFIG_HAVE_UNWIND_USER_FP=y
801d773
< CONFIG_ARCH_WANT_IRQS_OFF_ACTIVATE_MM=y
814c786
< CONFIG_HAVE_ARCH_KSTACK_ERASE=y
---
> CONFIG_HAVE_ARCH_STACKLEAK=y
823c795
< CONFIG_ARCH_SUPPORTS_CFI=y
---
> CONFIG_ARCH_SUPPORTS_CFI_CLANG=y
829d800
< CONFIG_HAVE_PV_STEAL_CLOCK_GEN=y
890d860
< CONFIG_HAVE_GENERIC_TIF_BITS=y
906,907d875
< CONFIG_ARCH_HAS_CPU_ATTACK_VECTORS=y
< CONFIG_HAVE_ARCH_GET_SECUREBOOT=y
969a938,939
> CONFIG_BLK_MQ_PCI=y
> CONFIG_BLK_MQ_VIRTIO=y
984c954,958
< CONFIG_UNINLINE_SPIN_UNLOCK=y
---
> CONFIG_INLINE_SPIN_UNLOCK_IRQ=y
> CONFIG_INLINE_READ_UNLOCK=y
> CONFIG_INLINE_READ_UNLOCK_IRQ=y
> CONFIG_INLINE_WRITE_UNLOCK=y
> CONFIG_INLINE_WRITE_UNLOCK_IRQ=y
1025a1000
> CONFIG_SLUB_CPU_PARTIAL=y
1047,1048c1022,1023
< CONFIG_BALLOON=y
< CONFIG_BALLOON_MIGRATION=y
---
> CONFIG_MEMORY_BALLOON=y
> CONFIG_BALLOON_COMPACTION=y
1052d1026
< CONFIG_NUMA_MIGRATION=y
1063d1036
< # CONFIG_PERSISTENT_HUGE_ZERO_FOLIO is not set
1069,1076d1041
< CONFIG_TRANSPARENT_HUGEPAGE_SHMEM_HUGE_NEVER=y
< # CONFIG_TRANSPARENT_HUGEPAGE_SHMEM_HUGE_ALWAYS is not set
< # CONFIG_TRANSPARENT_HUGEPAGE_SHMEM_HUGE_WITHIN_SIZE is not set
< # CONFIG_TRANSPARENT_HUGEPAGE_SHMEM_HUGE_ADVISE is not set
< CONFIG_TRANSPARENT_HUGEPAGE_TMPFS_HUGE_NEVER=y
< # CONFIG_TRANSPARENT_HUGEPAGE_TMPFS_HUGE_ALWAYS is not set
< # CONFIG_TRANSPARENT_HUGEPAGE_TMPFS_HUGE_WITHIN_SIZE is not set
< # CONFIG_TRANSPARENT_HUGEPAGE_TMPFS_HUGE_ADVISE is not set
1082d1046
< CONFIG_ASYNC_KERNEL_PGTABLE_FREE=y
1094d1057
< CONFIG_PAGE_BLOCK_MAX_ORDER=10
1099a1063
> CONFIG_ARCH_HAS_PTE_DEVMAP=y
1103a1068
> CONFIG_GET_FREE_REGION=y
1128a1094
> CONFIG_ARCH_SUPPORTS_PT_RECLAIM=y
1144d1109
< CONFIG_NET_CRC32C=y
1151d1115
< # CONFIG_INET_PSP is not set
1166d1129
< # CONFIG_DIBS is not set
1188c1151
< CONFIG_SYN_COOKIES=y
---
> # CONFIG_SYN_COOKIES is not set
1259d1221
< CONFIG_NETFILTER_FAMILY_ARP=y
1261d1222
< # CONFIG_NETFILTER_NETLINK_HOOK is not set
1265c1226
< CONFIG_NETFILTER_NETLINK_OSF=m
---
> # CONFIG_NETFILTER_NETLINK_OSF is not set
1268,1269c1229
< CONFIG_NETFILTER_CONNCOUNT=m
< CONFIG_NF_CONNTRACK_MARK=y
---
> # CONFIG_NF_CONNTRACK_MARK is not set
1275a1236
> # CONFIG_NF_CT_PROTO_DCCP is not set
1276a1238
> # CONFIG_NF_CT_PROTO_UDPLITE is not set
1297,1331c1259
< CONFIG_NETFILTER_SYNPROXY=m
< CONFIG_NF_TABLES=m
< CONFIG_NF_TABLES_INET=y
< CONFIG_NF_TABLES_NETDEV=y
< CONFIG_NFT_NUMGEN=m
< CONFIG_NFT_CT=m
< # CONFIG_NFT_EXTHDR_DCCP is not set
< # CONFIG_NFT_FLOW_OFFLOAD is not set
< CONFIG_NFT_CONNLIMIT=m
< CONFIG_NFT_LOG=m
< CONFIG_NFT_LIMIT=m
< CONFIG_NFT_MASQ=m
< CONFIG_NFT_REDIR=m
< CONFIG_NFT_NAT=m
< CONFIG_NFT_TUNNEL=m
< CONFIG_NFT_QUOTA=m
< CONFIG_NFT_REJECT=m
< CONFIG_NFT_REJECT_INET=m
< CONFIG_NFT_COMPAT=m
< CONFIG_NFT_HASH=m
< CONFIG_NFT_FIB=m
< # CONFIG_NFT_FIB_INET is not set
< CONFIG_NFT_XFRM=m
< CONFIG_NFT_SOCKET=m
< CONFIG_NFT_OSF=m
< CONFIG_NFT_TPROXY=m
< CONFIG_NFT_SYNPROXY=m
< CONFIG_NF_DUP_NETDEV=m
< CONFIG_NFT_DUP_NETDEV=m
< CONFIG_NFT_FWD_NETDEV=m
< # CONFIG_NFT_FIB_NETDEV is not set
< CONFIG_NFT_REJECT_NETDEV=m
< CONFIG_NF_FLOW_TABLE_INET=m
< CONFIG_NF_FLOW_TABLE=m
< # CONFIG_NF_FLOW_TABLE_PROCFS is not set
---
> # CONFIG_NF_TABLES is not set
1333d1260
< # CONFIG_NETFILTER_XTABLES_LEGACY is not set
1339c1266
< CONFIG_NETFILTER_XT_CONNMARK=m
---
> # CONFIG_NETFILTER_XT_CONNMARK is not set
1347c1274
< CONFIG_NETFILTER_XT_TARGET_CONNMARK=m
---
> # CONFIG_NETFILTER_XT_TARGET_CONNMARK is not set
1355c1282
< CONFIG_NETFILTER_XT_TARGET_MARK=m
---
> # CONFIG_NETFILTER_XT_TARGET_MARK is not set
1359a1287
> # CONFIG_NETFILTER_XT_TARGET_NOTRACK is not set
1364a1293
> # CONFIG_NETFILTER_XT_TARGET_TRACE is not set
1379c1308
< CONFIG_NETFILTER_XT_MATCH_CONNMARK=m
---
> # CONFIG_NETFILTER_XT_MATCH_CONNMARK is not set
1397c1326
< CONFIG_NETFILTER_XT_MATCH_MARK=m
---
> # CONFIG_NETFILTER_XT_MATCH_MARK is not set
1490,1497c1419,1422
< CONFIG_NF_SOCKET_IPV4=m
< CONFIG_NF_TPROXY_IPV4=m
< CONFIG_NF_TABLES_IPV4=y
< CONFIG_NFT_REJECT_IPV4=m
< CONFIG_NFT_DUP_IPV4=m
< CONFIG_NFT_FIB_IPV4=m
< CONFIG_NF_TABLES_ARP=y
< CONFIG_NF_DUP_IPV4=m
---
> CONFIG_IP_NF_IPTABLES_LEGACY=m
> # CONFIG_NF_SOCKET_IPV4 is not set
> # CONFIG_NF_TPROXY_IPV4 is not set
> # CONFIG_NF_DUP_IPV4 is not set
1505a1431
> CONFIG_IP_NF_FILTER=m
1507a1434,1438
> CONFIG_IP_NF_NAT=m
> CONFIG_IP_NF_TARGET_MASQUERADE=m
> # CONFIG_IP_NF_TARGET_NETMAP is not set
> CONFIG_IP_NF_TARGET_REDIRECT=m
> CONFIG_IP_NF_MANGLE=m
1509,1510c1440,1443
< CONFIG_NFT_COMPAT_ARP=m
< CONFIG_IP_NF_ARP_MANGLE=m
---
> # CONFIG_IP_NF_TARGET_TTL is not set
> CONFIG_IP_NF_RAW=m
> # CONFIG_IP_NF_ARPTABLES is not set
> # CONFIG_IP_NF_ARPFILTER is not set
1516,1522c1449,1452
< CONFIG_NF_SOCKET_IPV6=m
< CONFIG_NF_TPROXY_IPV6=m
< CONFIG_NF_TABLES_IPV6=y
< CONFIG_NFT_REJECT_IPV6=m
< CONFIG_NFT_DUP_IPV6=m
< CONFIG_NFT_FIB_IPV6=m
< CONFIG_NF_DUP_IPV6=m
---
> CONFIG_IP6_NF_IPTABLES_LEGACY=m
> # CONFIG_NF_SOCKET_IPV6 is not set
> # CONFIG_NF_TPROXY_IPV6 is not set
> # CONFIG_NF_DUP_IPV6 is not set
1535a1466,1467
> # CONFIG_IP6_NF_TARGET_HL is not set
> CONFIG_IP6_NF_FILTER=m
1537a1470,1473
> CONFIG_IP6_NF_MANGLE=m
> CONFIG_IP6_NF_RAW=m
> CONFIG_IP6_NF_NAT=m
> CONFIG_IP6_NF_TARGET_MASQUERADE=m
1542,1544d1477
< CONFIG_NF_TABLES_BRIDGE=m
< CONFIG_NFT_BRIDGE_META=m
< CONFIG_NFT_BRIDGE_REJECT=m
1545a1479
> # CONFIG_BRIDGE_NF_EBTABLES_LEGACY is not set
1546a1481
> # CONFIG_IP_DCCP is not set
1602d1536
< # CONFIG_NET_SCH_DUALPI2 is not set
1632,1634c1566
< CONFIG_QRTR=m
< # CONFIG_QRTR_TUN is not set
< CONFIG_QRTR_MHI=m
---
> # CONFIG_QRTR is not set
1656a1589
> # CONFIG_HAMRADIO is not set
1684a1618
> # CONFIG_BT_HCIBTUSB_AUTO_ISOC_ALT is not set
1721d1654
< CONFIG_STREAM_PARSER=y
1753a1687
> # CONFIG_CAIF is not set
1793d1726
< # CONFIG_PCI_TSM is not set
1851,1853c1784
< CONFIG_PCI_PWRCTRL=m
< CONFIG_PCI_PWRCTRL_GENERIC=m
< # CONFIG_PCI_PWRCTRL_TC9563 is not set
---
> # CONFIG_PCI_PWRCTL_SLOT is not set
1857d1787
< # CONFIG_PC104 is not set
1867d1796
< CONFIG_DRIVER_DEFERRED_PROBE_TIMEOUT=10
1894d1822
< CONFIG_REGMAP_IRQ=y
1903,1905c1831
< CONFIG_MHI_BUS=m
< # CONFIG_MHI_BUS_DEBUG is not set
< # CONFIG_MHI_BUS_PCI_GENERIC is not set
---
> # CONFIG_MHI_BUS is not set
1908a1835,1839
> #
> # Cache Drivers
> #
> # end of Cache Drivers
> 
1927c1858
< # CONFIG_FW_CFG_SYSFS is not set
---
> CONFIG_FW_CFG_SYSFS=y
1949,1950d1879
< # CONFIG_OVMF_DEBUG_LOG is not set
< CONFIG_EFI_SBAT_FILE=""
1989a1919
> # CONFIG_CDROM_PKTCDVD is not set
2017d1946
< # CONFIG_TI_FPC202 is not set
2047d1975
< # CONFIG_EEPROM_M24LR is not set
2057,2058d1984
< CONFIG_INTEL_MEI_CSC=m
< CONFIG_INTEL_MEI_LB=m
2063a1990
> # CONFIG_ECHO is not set
2264a2192
> # CONFIG_MD_BITMAP_FILE is not set
2316d2243
< CONFIG_OVPN=m
2319d2245
< # CONFIG_IFB is not set
2345d2270
< # CONFIG_MHI_NET is not set
2354a2280
> # CONFIG_NET_VENDOR_ALTEON is not set
2387d2312
< # CONFIG_BNGE is not set
2400a2326
> # CONFIG_DNET is not set
2420d2345
< CONFIG_LIBETH_XDP=y
2422,2423d2346
< CONFIG_LIBIE_ADMINQ=y
< CONFIG_LIBIE_FWLOG=y
2452,2459c2375
< CONFIG_NET_VENDOR_MELLANOX=y
< CONFIG_MLX4_EN=y
< CONFIG_MLX4_CORE=y
< # CONFIG_MLX4_DEBUG is not set
< CONFIG_MLX4_CORE_GEN2=y
< # CONFIG_MLX5_CORE is not set
< # CONFIG_MLXSW_CORE is not set
< # CONFIG_MLXFW is not set
---
> # CONFIG_NET_VENDOR_MELLANOX is not set
2467d2382
< # CONFIG_NET_VENDOR_MUCSE is not set
2471a2387
> # CONFIG_NET_VENDOR_NETERION is not set
2477a2394
> # CONFIG_NET_VENDOR_PACKET_ENGINES is not set
2512d2428
< # CONFIG_DWMAC_MOTORCOMM is not set
2527a2444
> # CONFIG_HIPPI is not set
2531d2447
< CONFIG_PHY_PACKAGE=y
2539d2454
< # CONFIG_AS21XXX_PHY is not set
2564d2478
< # CONFIG_MAXLINEAR_86110_PHY is not set
2598a2513,2514
> CONFIG_MDIO_DEVICE=y
> CONFIG_MDIO_BUS=y
2600a2517
> CONFIG_MDIO_DEVRES=y
2684a2602
> CONFIG_ATH9K_AHB=y
2717,2720c2635
< CONFIG_ATH12K=m
< # CONFIG_ATH12K_DEBUG is not set
< # CONFIG_ATH12K_TRACING is not set
< # CONFIG_ATH12K_COREDUMP is not set
---
> # CONFIG_ATH12K is not set
2914d2828
< CONFIG_RTW89_USB=m
2922d2835
< CONFIG_RTW89_8851BU=m
2924d2836
< CONFIG_RTW89_8852AU=m
2926d2837
< CONFIG_RTW89_8852BU=m
2929d2839
< CONFIG_RTW89_8852CU=m
2959a2870
> # CONFIG_ISDN is not set
2985a2897
> # CONFIG_KEYBOARD_ADP5589 is not set
2993a2906
> # CONFIG_KEYBOARD_TCA6416 is not set
2996d2908
< # CONFIG_KEYBOARD_CHARLIEPLEX is not set
3086d2997
< # CONFIG_TOUCHSCREEN_HIMAX_HX852X is not set
3089d2999
< # CONFIG_TOUCHSCREEN_HYNITRON_CST816X is not set
3154d3063
< # CONFIG_INPUT_AW86927 is not set
3192,3193d3100
< CONFIG_RMI4_F1A=y
< CONFIG_RMI4_F21=y
3205a3113
> # CONFIG_SERIO_CT82C710 is not set
3235a3144
> # CONFIG_SERIAL_8250_DEPRECATED_OPTIONS is not set
3239c3148
< # CONFIG_SERIAL_8250_CONSOLE is not set
---
> CONFIG_SERIAL_8250_CONSOLE=y
3246a3156,3157
> CONFIG_SERIAL_8250_MANY_PORTS=y
> # CONFIG_SERIAL_8250_PCI1XXXX is not set
3250,3251c3161
< CONFIG_SERIAL_8250_MANY_PORTS=y
< # CONFIG_SERIAL_8250_PCI1XXXX is not set
---
> CONFIG_SERIAL_8250_DWLIB=y
3258d3167
< CONFIG_SERIAL_8250_DWLIB=y
3297a3207
> # CONFIG_MWAVE is not set
3370a3281
> # CONFIG_I2C_DESIGNWARE_SLAVE is not set
3406d3316
< CONFIG_I3C_OR_I2C=y
3437d3346
< # CONFIG_PTP_NETC_V4_TIMER is not set
3440,3447d3348
< #
< # DPLL device support
< #
< CONFIG_DPLL=y
< # CONFIG_DPLL_REFCNT_TRACKER is not set
< # CONFIG_ZL3073X_I2C is not set
< # end of DPLL device support
< 
3456d3356
< # CONFIG_PINCTRL_STMFX is not set
3490d3389
< CONFIG_GPIOLIB_LEGACY=y
3497d3395
< CONFIG_GPIO_SYSFS_LEGACY=y
3506d3403
< # CONFIG_GPIO_BY_PINCTRL is not set
3524d3420
< # CONFIG_GPIO_NOVALAKE is not set
3545a3442
> # CONFIG_GPIO_ELKHARTLAKE is not set
3583c3480
< CONFIG_POWER_SEQUENCING=m
---
> # CONFIG_POWER_SEQUENCING is not set
3590d3486
< # CONFIG_BATTERY_CHAGALL is not set
3596d3491
< # CONFIG_BATTERY_S2MU005 is not set
3610d3504
< # CONFIG_CHARGER_MAX8971 is not set
3625d3518
< # CONFIG_CHARGER_RT9756 is not set
3678d3570
< # CONFIG_SENSORS_GPD is not set
3681d3572
< # CONFIG_SENSORS_GPIO_FAN is not set
3692d3582
< # CONFIG_SENSORS_LATTEPANDA_SIGMA_EC is not set
3723d3612
< # CONFIG_SENSORS_MCP9982 is not set
3753a3643
> # CONFIG_SENSORS_OXP is not set
3757a3648
> # CONFIG_SENSORS_SBRMI is not set
3790d3680
< # CONFIG_SENSORS_TSC1641 is not set
3806d3695
< # CONFIG_SENSORS_YOGAFAN is not set
3830d3718
< # CONFIG_DEVFREQ_THERMAL is not set
3847,3850c3735
< CONFIG_INT340X_THERMAL=m
< CONFIG_ACPI_THERMAL_REL=m
< CONFIG_INT3406_THERMAL=m
< CONFIG_PROC_THERMAL_MMIO_RAPL=m
---
> # CONFIG_INT340X_THERMAL is not set
3858c3743,3746
< # CONFIG_WATCHDOG is not set
---
> CONFIG_WATCHDOG=y
> CONFIG_WATCHDOG_CORE=y
> CONFIG_WATCHDOG_SYSFS=y
> CONFIG_I6300ESB_WDT=y
3891d3778
< # CONFIG_MFD_CS40L50_I2C is not set
3919d3805
< # CONFIG_MFD_MAX5970 is not set
3933d3818
< # CONFIG_MFD_NCT6694 is not set
3949d3833
< # CONFIG_MFD_BQ257XX is not set
3962a3847
> CONFIG_MFD_WL1273_CORE=m
3971a3857
> # CONFIG_MFD_CS40L50_I2C is not set
3975d3860
< # CONFIG_MFD_MAX7360 is not set
3987d3871
< # CONFIG_REGULATOR_ADP5055 is not set
3995d3878
< # CONFIG_REGULATOR_FP9931 is not set
4012d3894
< # CONFIG_REGULATOR_MAX77838 is not set
4017d3898
< # CONFIG_REGULATOR_PF0900 is not set
4030d3910
< # CONFIG_REGULATOR_RT8092 is not set
4041d3920
< # CONFIG_REGULATOR_TPS65185 is not set
4325a4205
> CONFIG_RADIO_WL1273=m
4356,4359d4235
< # ARM media platform drivers
< #
< 
< #
4499d4374
< # CONFIG_VIDEO_GC0310 is not set
4506d4380
< # CONFIG_VIDEO_IMX111 is not set
4522a4397
> # CONFIG_VIDEO_MT9V032 is not set
4525,4526d4399
< # CONFIG_VIDEO_OG0VE1B is not set
< # CONFIG_VIDEO_OS05B10 is not set
4529,4530d4401
< # CONFIG_VIDEO_OV02E10 is not set
< # CONFIG_VIDEO_OV02C10 is not set
4539d4409
< # CONFIG_VIDEO_OV2735 is not set
4548d4417
< # CONFIG_VIDEO_OV6211 is not set
4549a4419
> # CONFIG_VIDEO_OV6650 is not set
4564d4433
< # CONFIG_VIDEO_S5K3M5 is not set
4567,4570d4435
< # CONFIG_VIDEO_S5KJN1 is not set
< # CONFIG_VIDEO_T4KA3 is not set
< # CONFIG_VIDEO_VD55G1 is not set
< # CONFIG_VIDEO_VD56G3 is not set
4580c4445,4454
< # CONFIG_VIDEO_CAMERA_LENS is not set
---
> #
> # Lens drivers
> #
> # CONFIG_VIDEO_AD5820 is not set
> # CONFIG_VIDEO_AK7375 is not set
> # CONFIG_VIDEO_DW9714 is not set
> # CONFIG_VIDEO_DW9719 is not set
> # CONFIG_VIDEO_DW9768 is not set
> # CONFIG_VIDEO_DW9807_VCM is not set
> # end of Lens drivers
4696d4569
< # CONFIG_VIDEO_MAX96717 is not set
4926d4798
< CONFIG_GPU_BUDDY=y
4928,4935d4799
< 
< #
< # DRM debugging options
< #
< # CONFIG_DRM_WERROR is not set
< # CONFIG_DRM_DEBUG_MM is not set
< # end of DRM debugging options
< 
4936a4801
> # CONFIG_DRM_DEBUG_MM is not set
4939d4803
< # CONFIG_DRM_RAS is not set
4965d4828
< CONFIG_DRM_DISPLAY_HDMI_CEC_NOTIFIER_HELPER=y
4970d4832
< CONFIG_DRM_GPUSVM=m
4976c4838,4845
< CONFIG_DRM_PANEL_BACKLIGHT_QUIRKS=y
---
> 
> #
> # ARM devices
> #
> # end of ARM devices
> 
> CONFIG_DRM_RADEON=y
> # CONFIG_DRM_RADEON_USERPTR is not set
5000,5020c4869
< 
< #
< # ARM devices
< #
< # end of ARM devices
< 
< # CONFIG_DRM_AST is not set
< CONFIG_DRM_BRIDGE=y
< CONFIG_DRM_PANEL_BRIDGE=y
< 
< #
< # Display Interface Bridges
< #
< # CONFIG_DRM_I2C_NXP_TDA998X is not set
< # CONFIG_DRM_ANALOGIX_ANX78XX is not set
< # end of Display Interface Bridges
< 
< # CONFIG_DRM_ETNAVIV is not set
< # CONFIG_DRM_GMA500 is not set
< # CONFIG_DRM_GUD is not set
< # CONFIG_DRM_HISI_HIBMC is not set
---
> # CONFIG_DRM_NOUVEAU is not set
5059,5094d4907
< # CONFIG_DRM_MGAG200 is not set
< # CONFIG_DRM_NOUVEAU is not set
< CONFIG_DRM_PANEL=y
< 
< #
< # Display Panels
< #
< # CONFIG_DRM_PANEL_RASPBERRYPI_TOUCHSCREEN is not set
< # end of Display Panels
< 
< # CONFIG_DRM_QXL is not set
< CONFIG_DRM_RADEON=y
< # CONFIG_DRM_RADEON_USERPTR is not set
< # CONFIG_DRM_ST7571 is not set
< # CONFIG_DRM_SSD130X is not set
< 
< #
< # Drivers for system framebuffers
< #
< # CONFIG_DRM_EFIDRM is not set
< # CONFIG_DRM_SIMPLEDRM is not set
< # CONFIG_DRM_VESADRM is not set
< # end of Drivers for system framebuffers
< 
< # CONFIG_DRM_APPLETBDRM is not set
< # CONFIG_DRM_BOCHS is not set
< # CONFIG_DRM_CIRRUS_QEMU is not set
< # CONFIG_DRM_GM12U320 is not set
< # CONFIG_DRM_UDL is not set
< # CONFIG_DRM_VBOXVIDEO is not set
< # CONFIG_DRM_VGEM is not set
< CONFIG_DRM_VIRTIO_GPU=y
< CONFIG_DRM_VIRTIO_GPU_KMS=y
< # CONFIG_DRM_VKMS is not set
< CONFIG_DRM_VMWGFX=y
< # CONFIG_DRM_VMWGFX_MKSSTATS is not set
5096a4910
> CONFIG_DRM_XE_DEVMEM_MIRROR=y
5105d4918
< # CONFIG_DRM_XE_DEBUG_SRIOV is not set
5106a4920
> # CONFIG_DRM_XE_DEBUG_SRIOV is not set
5107a4922
> # CONFIG_DRM_XE_LARGE_GUC_BUFFER is not set
5123a4939,4979
> # CONFIG_DRM_VGEM is not set
> # CONFIG_DRM_VKMS is not set
> CONFIG_DRM_VMWGFX=y
> # CONFIG_DRM_VMWGFX_MKSSTATS is not set
> # CONFIG_DRM_GMA500 is not set
> # CONFIG_DRM_UDL is not set
> # CONFIG_DRM_AST is not set
> # CONFIG_DRM_MGAG200 is not set
> # CONFIG_DRM_QXL is not set
> CONFIG_DRM_VIRTIO_GPU=y
> CONFIG_DRM_VIRTIO_GPU_KMS=y
> CONFIG_DRM_PANEL=y
> 
> #
> # Display Panels
> #
> # CONFIG_DRM_PANEL_RASPBERRYPI_TOUCHSCREEN is not set
> # end of Display Panels
> 
> CONFIG_DRM_BRIDGE=y
> CONFIG_DRM_PANEL_BRIDGE=y
> 
> #
> # Display Interface Bridges
> #
> # CONFIG_DRM_I2C_NXP_TDA998X is not set
> # CONFIG_DRM_ANALOGIX_ANX78XX is not set
> # end of Display Interface Bridges
> 
> # CONFIG_DRM_ETNAVIV is not set
> # CONFIG_DRM_HISI_HIBMC is not set
> # CONFIG_DRM_APPLETBDRM is not set
> # CONFIG_DRM_BOCHS is not set
> # CONFIG_DRM_CIRRUS_QEMU is not set
> # CONFIG_DRM_GM12U320 is not set
> # CONFIG_DRM_SIMPLEDRM is not set
> CONFIG_DRM_VBOXVIDEO=y
> # CONFIG_DRM_GUD is not set
> # CONFIG_DRM_SSD130X is not set
> CONFIG_DRM_PANEL_BACKLIGHT_QUIRKS=y
> # CONFIG_DRM_WERROR is not set
5146a5003
> # CONFIG_FB_MATROX is not set
5149a5007
> # CONFIG_FB_S3 is not set
5156a5015
> # CONFIG_FB_VT8623 is not set
5157a5017
> # CONFIG_FB_ARK is not set
5170a5031
> # CONFIG_FIRMWARE_EDID is not set
5184a5046
> CONFIG_FB_MODE_HELPERS=y
5193d5054
< # CONFIG_BACKLIGHT_AW99706 is not set
5211d5071
< # CONFIG_FIRMWARE_EDID is not set
5228d5087
< # CONFIG_TRACE_GPU_MEM is not set
5235d5093
< # CONFIG_DRM_ACCEL_QAIC is not set
5343a5202,5203
> CONFIG_SND_HDA_GENERIC_LEDS=y
> CONFIG_SND_HDA_INTEL=m
5349,5354c5209,5213
< CONFIG_SND_HDA_POWER_SAVE_DEFAULT=0
< # CONFIG_SND_HDA_CTL_DEV_ID is not set
< CONFIG_SND_HDA_PREALLOC_SIZE=0
< CONFIG_SND_HDA_INTEL=m
< # CONFIG_SND_HDA_ACPI is not set
< CONFIG_SND_HDA_GENERIC_LEDS=y
---
> CONFIG_SND_HDA_SCODEC_COMPONENT=m
> # CONFIG_SND_HDA_SCODEC_CS35L41_I2C is not set
> # CONFIG_SND_HDA_SCODEC_CS35L56_I2C is not set
> # CONFIG_SND_HDA_SCODEC_TAS2781_I2C is not set
> CONFIG_SND_HDA_CODEC_REALTEK=m
5357a5217,5219
> CONFIG_SND_HDA_CODEC_HDMI=m
> CONFIG_SND_HDA_CODEC_CIRRUS=m
> # CONFIG_SND_HDA_CODEC_CS8409 is not set
5364d5225
< # CONFIG_SND_HDA_CODEC_CM9825 is not set
5367,5386c5228
< CONFIG_SND_HDA_CODEC_REALTEK=m
< CONFIG_SND_HDA_CODEC_REALTEK_LIB=m
< CONFIG_SND_HDA_CODEC_ALC260=m
< CONFIG_SND_HDA_CODEC_ALC262=m
< CONFIG_SND_HDA_CODEC_ALC268=m
< CONFIG_SND_HDA_CODEC_ALC269=m
< CONFIG_SND_HDA_CODEC_ALC662=m
< CONFIG_SND_HDA_CODEC_ALC680=m
< CONFIG_SND_HDA_CODEC_ALC861=m
< CONFIG_SND_HDA_CODEC_ALC861VD=m
< CONFIG_SND_HDA_CODEC_ALC880=m
< CONFIG_SND_HDA_CODEC_ALC882=m
< CONFIG_SND_HDA_CODEC_CIRRUS=m
< CONFIG_SND_HDA_CODEC_CS420X=m
< CONFIG_SND_HDA_CODEC_CS421X=m
< # CONFIG_SND_HDA_CODEC_CS8409 is not set
< CONFIG_SND_HDA_CODEC_HDMI=m
< CONFIG_SND_HDA_CODEC_HDMI_GENERIC=m
< CONFIG_SND_HDA_CODEC_HDMI_SIMPLE=m
< CONFIG_SND_HDA_CODEC_HDMI_INTEL=m
---
> CONFIG_SND_HDA_POWER_SAVE_DEFAULT=0
5388,5395c5230,5232
< CONFIG_SND_HDA_CODEC_HDMI_ATI=m
< CONFIG_SND_HDA_CODEC_HDMI_NVIDIA=m
< CONFIG_SND_HDA_CODEC_HDMI_NVIDIA_MCP=m
< CONFIG_SND_HDA_CODEC_HDMI_TEGRA=m
< CONFIG_SND_HDA_SCODEC_COMPONENT=m
< # CONFIG_SND_HDA_SCODEC_CS35L41_I2C is not set
< # CONFIG_SND_HDA_SCODEC_CS35L56_I2C is not set
< # CONFIG_SND_HDA_SCODEC_TAS2781_I2C is not set
---
> # CONFIG_SND_HDA_CTL_DEV_ID is not set
> # end of HD-Audio
> 
5400a5238
> CONFIG_SND_HDA_PREALLOC_SIZE=0
5404,5405d5241
< # end of HD-Audio
< 
5415d5250
< # CONFIG_SND_USB_US144MKII is not set
5438,5449c5273
< # CONFIG_SND_SOC_USB is not set
< 
< #
< # Analog Devices
< #
< # CONFIG_SND_SOC_ADI_AXI_I2S is not set
< # CONFIG_SND_SOC_ADI_AXI_SPDIF is not set
< # end of Analog Devices
< 
< #
< # AMD
< #
---
> # CONFIG_SND_SOC_ADI is not set
5460a5285
> # CONFIG_SND_SOC_AMD_RPL_ACP6x is not set
5463,5482c5288
< # end of AMD
< 
< #
< # Apple
< #
< # end of Apple
< 
< #
< # Atmel
< #
< # end of Atmel
< 
< #
< # Au1x
< #
< # end of Au1x
< 
< #
< # Broadcom
< #
---
> # CONFIG_SND_ATMEL_SOC is not set
5484,5493d5289
< # end of Broadcom
< 
< #
< # Cirrus Logic
< #
< # end of Cirrus Logic
< 
< #
< # DesignWare
< #
5495d5290
< # end of DesignWare
5498c5293
< # Freescale
---
> # SoC Audio for Freescale CPUs
5513c5308
< # end of Freescale
---
> # end of SoC Audio for Freescale CPUs
5515,5517d5309
< #
< # Google
< #
5519,5523d5310
< # end of Google
< 
< #
< # Hisilicon
< #
5525,5530d5311
< # end of Hisilicon
< 
< #
< # JZ4740
< #
< # end of JZ4740
5533c5314
< # Kirkwood
---
> # SoC Audio for Loongson CPUs
5535c5316
< # end of Kirkwood
---
> # end of SoC Audio for Loongson CPUs
5537,5544c5318
< #
< # Loongson
< #
< # end of Loongson
< 
< #
< # Intel
< #
---
> # CONFIG_SND_SOC_IMG is not set
5561d5334
< # CONFIG_SND_SOC_INTEL_AVS_CARDNAME_OBSOLETE is not set
5577d5349
< # CONFIG_SND_SOC_INTEL_AVS_MACH_RT5640 is not set
5595,5599d5366
< # end of Intel
< 
< #
< # Mediatek
< #
5601,5610d5367
< # end of Mediatek
< 
< #
< # PXA
< #
< # end of PXA
< 
< #
< # SoundWire (SDCA)
< #
5612,5614d5368
< CONFIG_SND_SOC_SDCA_HID=y
< CONFIG_SND_SOC_SDCA_IRQ=y
< CONFIG_SND_SOC_SDCA_FDL=y
5616,5631c5370
< # end of SoundWire (SDCA)
< 
< #
< # ST SPEAr
< #
< # end of ST SPEAr
< 
< #
< # Spreadtrum
< #
< # end of Spreadtrum
< 
< #
< # STMicroelectronics STM32
< #
< # end of STMicroelectronics STM32
---
> # CONFIG_SND_SOC_SOF_TOPLEVEL is not set
5634c5373
< # Tegra
---
> # STMicroelectronics STM32 SOC audio support
5636c5375
< # end of Tegra
---
> # end of STMicroelectronics STM32 SOC audio support
5638,5640d5376
< #
< # Xilinx
< #
5644,5648d5379
< # end of Xilinx
< 
< #
< # Xtensa
< #
5650,5652d5380
< # end of Xtensa
< 
< # CONFIG_SND_SOC_SOF_TOPLEVEL is not set
5723,5725d5450
< # CONFIG_SND_SOC_ES8375 is not set
< # CONFIG_SND_SOC_ES8389 is not set
< # CONFIG_SND_SOC_FS210X is not set
5743d5467
< # CONFIG_SND_SOC_PCM1754 is not set
5753d5476
< # CONFIG_SND_SOC_RT5575 is not set
5764,5766d5486
< # CONFIG_SND_SOC_RT9123 is not set
< # CONFIG_SND_SOC_RT9123P is not set
< # CONFIG_SND_SOC_RTQ9124 is not set
5807d5526
< # CONFIG_SND_SOC_UDA1380 is not set
5837d5555
< # CONFIG_SND_SOC_NAU8325 is not set
5852,5854d5569
< #
< # Generic drivers
< #
5857,5858d5571
< # end of Generic drivers
< 
5869d5581
< # CONFIG_HID_HAPTIC is not set
5929,5930d5640
< # CONFIG_HID_LENOVO_GO is not set
< # CONFIG_HID_LENOVO_GO_S is not set
5962d5671
< # CONFIG_HID_RAPOO is not set
5999d5707
< # CONFIG_HID_HUAWEI is not set
6073d5780
< # CONFIG_USB_XHCI_SIDEBAND is not set
6210d5916
< # CONFIG_USB_USBIO is not set
6297,6303c6003
< CONFIG_SCSI_UFSHCD=y
< CONFIG_SCSI_UFS_BSG=y
< CONFIG_SCSI_UFS_HWMON=y
< CONFIG_SCSI_UFSHCD_PCI=y
< CONFIG_SCSI_UFS_DWC_TC_PCI=y
< CONFIG_SCSI_UFSHCD_PLATFORM=y
< CONFIG_SCSI_UFS_CDNS_PLATFORM=y
---
> # CONFIG_SCSI_UFSHCD is not set
6315d6014
< # CONFIG_LEDS_OSRAM_AMS_AS3668 is not set
6359d6057
< # CONFIG_LEDS_LP5812 is not set
6428a6127
> # CONFIG_RTC_DRV_PCF85063 is not set
6457d6155
< # CONFIG_RTC_DRV_PCF85063 is not set
6482d6179
< # CONFIG_RTC_DRV_GOLDFISH is not set
6486a6184
> # CONFIG_RTC_DRV_GOLDFISH is not set
6502d6199
< # CONFIG_SWITCHTEC_DMA is not set
6529a6227
> # CONFIG_DMABUF_MOVE_NOTIFY is not set
6532a6231
> # CONFIG_DMABUF_SYSFS_STATS is not set
6547d6245
< # CONFIG_UIO_PCI_GENERIC_SVA is not set
6564d6261
< # CONFIG_VIRTIO_RTC is not set
6576d6272
< # CONFIG_GPIB is not set
6587c6283,6286
< # CONFIG_VIDEO_INTEL_IPU7 is not set
---
> 
> #
> # StarFive media platform drivers
> #
6593a6293
> # CONFIG_GPIB is not set
6603a6304
> CONFIG_ACPI_WMI=y
6606d6306
< # CONFIG_X86_PLATFORM_DRIVERS_UNIWILL is not set
6610d6309
< # CONFIG_REDMI_WMI is not set
6612c6311
< # CONFIG_BITLAND_MIFS_WMI is not set
---
> # CONFIG_YOGABOOK is not set
6625d6323
< # CONFIG_AMD_HFI is not set
6628d6325
< # CONFIG_AMD_ISP_PLATFORM is not set
6634d6330
< # CONFIG_AYANEO_EC is not set
6642a6339,6340
> # CONFIG_IDEAPAD_LAPTOP is not set
> # CONFIG_LENOVO_WMI_HOTKEY_UTILITIES is not set
6643a6342,6343
> # CONFIG_THINKPAD_ACPI is not set
> # CONFIG_THINKPAD_LMI is not set
6667d6366
< # CONFIG_INTEL_EHL_PSE_IO is not set
6675,6682d6373
< # CONFIG_IDEAPAD_LAPTOP is not set
< # CONFIG_LENOVO_WMI_HOTKEY_UTILITIES is not set
< # CONFIG_LENOVO_WMI_CAMERA is not set
< # CONFIG_THINKPAD_ACPI is not set
< # CONFIG_THINKPAD_LMI is not set
< # CONFIG_YOGABOOK is not set
< # CONFIG_LENOVO_WMI_GAMEZONE is not set
< # CONFIG_LENOVO_WMI_TUNING is not set
6706c6397
< # CONFIG_DASHARO_ACPI is not set
---
> # CONFIG_LENOVO_WMI_CAMERA is not set
6714,6715d6404
< # CONFIG_OXP_EC is not set
< # CONFIG_TUXEDO_NB04_WMI_AB is not set
6717,6718d6405
< CONFIG_ACPI_WMI=y
< # CONFIG_ACPI_WMI_LEGACY_DEVICE_NAMES is not set
6747a6435
> CONFIG_IOMMU_IO_PGTABLE=y
6761a6450
> CONFIG_INTEL_IOMMU_FLOPPY_WA=y
6767,6773d6455
< CONFIG_GENERIC_PT=y
< # CONFIG_DEBUG_GENERIC_PT is not set
< CONFIG_IOMMU_PT=y
< CONFIG_IOMMU_PT_AMDV1=y
< CONFIG_IOMMU_PT_VTDSS=y
< # CONFIG_IOMMU_PT_RISCV64 is not set
< CONFIG_IOMMU_PT_X86_64=y
6829d6510
< CONFIG_QCOM_QMI_HELPERS=m
6865,6879c6546
< CONFIG_PM_DEVFREQ=y
< 
< #
< # DEVFREQ Governors
< #
< CONFIG_DEVFREQ_GOV_SIMPLE_ONDEMAND=y
< # CONFIG_DEVFREQ_GOV_PERFORMANCE is not set
< # CONFIG_DEVFREQ_GOV_POWERSAVE is not set
< # CONFIG_DEVFREQ_GOV_USERSPACE is not set
< # CONFIG_DEVFREQ_GOV_PASSIVE is not set
< 
< #
< # DEVFREQ Drivers
< #
< # CONFIG_PM_DEVFREQ_EVENT is not set
---
> # CONFIG_PM_DEVFREQ is not set
6889d6555
< CONFIG_IRQ_MSI_LIB=y
6903,6904d6568
< # CONFIG_PHY_CAN_TRANSCEIVER is not set
< # CONFIG_PHY_GOOGLE_USB is not set
6905a6570
> # CONFIG_PHY_CAN_TRANSCEIVER is not set
6913d6577
< # CONFIG_PHY_INTEL_LGM_EMMC is not set
6915a6580
> # CONFIG_PHY_INTEL_LGM_EMMC is not set
6955,6956d6619
< # CONFIG_MUX_CORE is not set
< CONFIG_PM_OPP=y
6963a6627
> CONFIG_DPLL=y
6975a6640
> # CONFIG_EXT3_FS is not set
7005a6671
> # CONFIG_BTRFS_FS_REF_VERIFY is not set
7014a6681
> # CONFIG_BCACHEFS_FS is not set
7072,7075c6739,6743
< CONFIG_NTFS_FS=m
< # CONFIG_NTFS_DEBUG is not set
< # CONFIG_NTFS_FS_POSIX_ACL is not set
< # CONFIG_NTFS3_FS is not set
---
> CONFIG_NTFS3_FS=m
> # CONFIG_NTFS3_64BIT_CLUSTER is not set
> # CONFIG_NTFS3_LZX_XPRESS is not set
> # CONFIG_NTFS3_FS_POSIX_ACL is not set
> # CONFIG_NTFS_FS is not set
7094d6761
< CONFIG_ARCH_SUPPORTS_HUGETLBFS=y
7121d6787
< # CONFIG_SQUASHFS_COMP_CACHE_FULL is not set
7137c6803,6807
< # CONFIG_PSTORE is not set
---
> CONFIG_PSTORE=y
> CONFIG_PSTORE_COMPRESS=y
> CONFIG_PSTORE_CONSOLE=y
> CONFIG_PSTORE_RAM=y
> CONFIG_EFI_VARS_PSTORE=y
7147c6817
< CONFIG_NFS_V4_0=y
---
> CONFIG_NFS_V4_1=y
7269a6940
> CONFIG_LSM="yama,loadpin,safesetid,integrity,selinux,smack,tomoyo,apparmor"
7307a6979
> CONFIG_XOR_BLOCKS=y
7324a6997
> CONFIG_CRYPTO_RNG_DEFAULT=y
7328a7002
> CONFIG_CRYPTO_ACOMP2=y
7332c7006,7007
< # CONFIG_CRYPTO_SELFTESTS is not set
---
> # CONFIG_CRYPTO_MANAGER_DISABLE_TESTS is not set
> # CONFIG_CRYPTO_MANAGER_EXTRA_TESTS is not set
7333a7009
> CONFIG_CRYPTO_NULL2=y
7338c7014,7015
< # CONFIG_CRYPTO_BENCHMARK is not set
---
> # CONFIG_CRYPTO_TEST is not set
> CONFIG_CRYPTO_SIMD=y
7351c7028
< # CONFIG_CRYPTO_MLDSA is not set
---
> # CONFIG_CRYPTO_CURVE25519 is not set
7357a7035
> # CONFIG_CRYPTO_AES_TI is not set
7379c7057
< CONFIG_CRYPTO_CHACHA20=m
---
> # CONFIG_CRYPTO_CHACHA20 is not set
7394c7072
< CONFIG_CRYPTO_CHACHA20POLY1305=m
---
> # CONFIG_CRYPTO_CHACHA20POLY1305 is not set
7407a7086
> CONFIG_CRYPTO_GHASH=y
7410a7090,7091
> CONFIG_CRYPTO_MICHAEL_MIC=m
> # CONFIG_CRYPTO_POLY1305 is not set
7416c7097
< # CONFIG_CRYPTO_SM3 is not set
---
> # CONFIG_CRYPTO_SM3_GENERIC is not set
7443a7125
> # CONFIG_CRYPTO_ANSI_CPRNG is not set
7466a7149,7150
> CONFIG_CRYPTO_HASH_INFO=y
> 
7469a7154
> CONFIG_CRYPTO_CURVE25519_X86=m
7476a7162
> CONFIG_CRYPTO_DES3_EDE_X86_64=y
7487a7174
> CONFIG_CRYPTO_CHACHA20_X86_64=m
7488a7176,7185
> # CONFIG_CRYPTO_NHPOLY1305_SSE2 is not set
> # CONFIG_CRYPTO_NHPOLY1305_AVX2 is not set
> CONFIG_CRYPTO_BLAKE2S_X86=y
> # CONFIG_CRYPTO_POLYVAL_CLMUL_NI is not set
> CONFIG_CRYPTO_POLY1305_X86_64=m
> CONFIG_CRYPTO_SHA1_SSSE3=y
> CONFIG_CRYPTO_SHA256_SSSE3=y
> CONFIG_CRYPTO_SHA512_SSSE3=y
> # CONFIG_CRYPTO_SM3_AVX_X86_64 is not set
> # CONFIG_CRYPTO_GHASH_CLMUL_NI_INTEL is not set
7509d7205
< CONFIG_OPENSSL_SUPPORTS_ML_DSA=y
7533,7539c7229,7232
< CONFIG_CRC16=y
< CONFIG_CRC_CCITT=y
< CONFIG_CRC_ITU_T=m
< CONFIG_CRC32=y
< CONFIG_CRC32_ARCH=y
< CONFIG_CRC_OPTIMIZATIONS=y
< CONFIG_CRYPTO_HASH_INFO=y
---
> 
> #
> # Crypto library routines
> #
7542,7544c7235
< CONFIG_CRYPTO_LIB_AES_ARCH=y
< CONFIG_CRYPTO_LIB_AES_CBC_MACS=y
< CONFIG_CRYPTO_LIB_ARC4=y
---
> CONFIG_CRYPTO_LIB_ARC4=m
7546,7547c7237,7241
< CONFIG_CRYPTO_LIB_BLAKE2B=y
< CONFIG_CRYPTO_LIB_BLAKE2S_ARCH=y
---
> CONFIG_CRYPTO_ARCH_HAVE_LIB_BLAKE2S=y
> CONFIG_CRYPTO_LIB_BLAKE2S_GENERIC=y
> CONFIG_CRYPTO_ARCH_HAVE_LIB_CHACHA=y
> CONFIG_CRYPTO_LIB_CHACHA_GENERIC=m
> CONFIG_CRYPTO_LIB_CHACHA_INTERNAL=m
7549c7243,7245
< CONFIG_CRYPTO_LIB_CHACHA_ARCH=y
---
> CONFIG_CRYPTO_ARCH_HAVE_LIB_CURVE25519=y
> CONFIG_CRYPTO_LIB_CURVE25519_GENERIC=m
> CONFIG_CRYPTO_LIB_CURVE25519_INTERNAL=m
7551,7552d7246
< CONFIG_CRYPTO_LIB_CURVE25519_ARCH=y
< CONFIG_CRYPTO_LIB_CURVE25519_GENERIC=y
7554,7558d7247
< CONFIG_CRYPTO_LIB_GF128HASH=y
< CONFIG_CRYPTO_LIB_GF128HASH_ARCH=y
< CONFIG_CRYPTO_LIB_MD5=y
< CONFIG_CRYPTO_LIB_POLY1305=m
< CONFIG_CRYPTO_LIB_POLY1305_ARCH=y
7559a7249,7252
> CONFIG_CRYPTO_ARCH_HAVE_LIB_POLY1305=y
> CONFIG_CRYPTO_LIB_POLY1305_GENERIC=m
> CONFIG_CRYPTO_LIB_POLY1305_INTERNAL=m
> CONFIG_CRYPTO_LIB_POLY1305=m
7562d7254
< CONFIG_CRYPTO_LIB_SHA1_ARCH=y
7564,7569c7256,7266
< CONFIG_CRYPTO_LIB_SHA256_ARCH=y
< CONFIG_CRYPTO_LIB_SHA512=y
< CONFIG_CRYPTO_LIB_SHA512_ARCH=y
< CONFIG_CRYPTO_LIB_SHA3=y
< CONFIG_XOR_BLOCKS=y
< CONFIG_XOR_BLOCKS_ARCH=y
---
> # end of Crypto library routines
> 
> CONFIG_CRC_CCITT=y
> CONFIG_CRC16=y
> CONFIG_ARCH_HAS_CRC_T10DIF=y
> CONFIG_CRC_ITU_T=m
> CONFIG_CRC32=y
> CONFIG_ARCH_HAS_CRC32=y
> CONFIG_CRC32_ARCH=y
> CONFIG_ARCH_HAS_CRC64=y
> CONFIG_CRC_OPTIMIZATIONS=y
7620a7318
> CONFIG_SGL_ALLOC=y
7625a7324
> # CONFIG_GLOB_SELFTEST is not set
7634a7334
> CONFIG_GENERIC_VDSO_TIME_NS=y
7636a7337
> CONFIG_GENERIC_VDSO_DATA_STORE=y
7650d7350
< # CONFIG_FONT_TER10x18 is not set
7678d7377
< CONFIG_PRINTK_EXECUTION_CTX=y
7688d7386
< # CONFIG_DEBUG_BUGVERBOSE_DETAILED is not set
7726a7425
> # CONFIG_DEBUG_FS_DISALLOW_MOUNT is not set
7796a7496
> CONFIG_PANIC_ON_OOPS_VALUE=0
7800c7500
< CONFIG_BOOTPARAM_SOFTLOCKUP_PANIC=0
---
> # CONFIG_BOOTPARAM_SOFTLOCKUP_PANIC is not set
7812c7512
< CONFIG_BOOTPARAM_HUNG_TASK_PANIC=0
---
> # CONFIG_BOOTPARAM_HUNG_TASK_PANIC is not set
7825,7827d7524
< # CONFIG_DEBUG_PREEMPT is not set
< # CONFIG_DEBUG_ATOMIC is not set
< 
7852a7550
> # CONFIG_WARN_ALL_UNSEEDED_RANDOM is not set
7893d7590
< CONFIG_HAVE_SINGLE_FTRACE_DIRECT_OPS=y
7897c7594
< CONFIG_HAVE_DYNAMIC_FTRACE_WITH_JMP=y
---
> CONFIG_HAVE_FTRACE_MCOUNT_RECORD=y
7916d7612
< CONFIG_TRACEFS_AUTOMOUNT_DEPRECATED=y
7926,7927d7621
< CONFIG_DYNAMIC_FTRACE_WITH_JMP=y
< # CONFIG_FUNCTION_SELF_TRACING is not set
7932d7625
< # CONFIG_PREEMPT_TRACER is not set
7948d7640
< CONFIG_EPROBE_EVENTS=y
7952a7645
> CONFIG_FTRACE_MCOUNT_RECORD=y
7970d7662
< # CONFIG_TRACE_REMOTE_TEST is not set
7983c7675
< # CONFIG_EARLY_PRINTK is not set
---
> CONFIG_EARLY_PRINTK=y
8010a7703
> CONFIG_CC_HAS_SANCOV_TRACE_PC=y
8014a7708
> # CONFIG_TEST_MIN_HEAP is not set
8026a7721
> # CONFIG_TEST_UUID is not set
8034d7728
< # CONFIG_TEST_WORKQUEUE is not set
8039d7732
< # CONFIG_CONTEXT_ANALYSIS_TEST is not set
8062d7754
< CONFIG_IO_URING_BPF=y
```


## scripts/image @ 8ebaf8daad: lines 268-292 (excerpt)

```text
268  
269    # Remove any previously created release images
270    rm -rf ${TARGET_IMG}/${IMAGE_NAME}.img.gz
271  
272    if [ -n "${BOOTLOADER}" ]; then
273  
274      BOOTLOADER_DIR="$(get_pkg_directory "${BOOTLOADER}")"
275  
276      if [ -d ${BOOTLOADER_DIR}/files ]; then
277        cp -R ${BOOTLOADER_DIR}/files/* ${RELEASE_DIR}
278      fi
279  
280      if find_file_path bootloader/install ${BOOTLOADER_DIR}/install; then
281        echo "Running ${FOUND_PATH}"
282        . ${FOUND_PATH}
283      fi
284  
285      if find_file_path bootloader/release ${BOOTLOADER_DIR}/release; then
286        echo "Running ${FOUND_PATH}"
287        . ${FOUND_PATH}
288      fi
289    fi
290  
291    cp ${ROOT}/README* ${RELEASE_DIR}
292    echo "${TARGET_VERSION}" >${RELEASE_DIR}/RELEASE
```


## scripts/mkimage @ 8ebaf8daad: lines 137-182 (excerpt)

```text
137  if [ "${BOOTLOADER}" = "syslinux" -o "${BOOTLOADER}" = "bcm2835-bootloader" -o "${BOOTLOADER}" = "u-boot" -o "${BOOTLOADER}" = "arm-efi" -o "${BOOTLOADER}" = "qcom-abl" ]; then
138    mformat -i "${IMG_TMP}/part1.fat" -v "${DISTRO_BOOTLABEL}" -N "${UUID_SYSTEM//-/}" :: >"${SAVE_ERROR}" 2>&1 || show_error
139  fi
140  sync
141  
142  if [ "${BOOTLOADER}" = "syslinux" ]; then
143    # create bootloader configuration
144    echo "image: creating bootloader configuration... (syslinux)"
145    cat << EOF > "${IMG_TMP}/syslinux.cfg"
146  DEFAULT run
147  TIMEOUT 0
148  PROMPT 0
149  NOESCAPE 1
150  
151  LABEL run
152    KERNEL /${KERNEL_NAME}
153    APPEND boot=LABEL=${DISTRO_BOOTLABEL} disk=LABEL=${DISTRO_DISKLABEL} portable ${EXTRA_CMDLINE}
154  EOF
155  
156    cat << EOF > "${IMG_TMP}/grub.cfg"
157  set timeout="0"
158  set default="Run"
159  menuentry "Run" {
160          search --set -f /KERNEL
161          linux /KERNEL boot=LABEL=${DISTRO_BOOTLABEL} disk=LABEL=${DISTRO_DISKLABEL} grub_portable ${EXTRA_CMDLINE}
162  }
163  EOF
164  
165    mcopy "${IMG_TMP}/syslinux.cfg" :: >"${SAVE_ERROR}" 2>&1 || show_error
166  
167    # install syslinux
168    echo "image: installing syslinux to part1..."
169    syslinux.mtools -i "${IMG_TMP}/part1.fat" >"${SAVE_ERROR}" 2>&1 || show_error
170  
171    # copy files
172    echo "image: copying files to part1..."
173    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}" >"${SAVE_ERROR}" 2>&1 || show_error
174    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM >"${SAVE_ERROR}" 2>&1 || show_error
175    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5" >"${SAVE_ERROR}" 2>&1 || show_error
176    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5 >"${SAVE_ERROR}" 2>&1 || show_error
177  
178    mmd EFI EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
179    mcopy "${TOOLCHAIN}/share/syslinux/bootx64.efi" ::/EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
180    mcopy "${TOOLCHAIN}/share/syslinux/ldlinux.e64" ::/EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
181    mcopy "${IMG_TMP}/grub.cfg" ::/EFI/BOOT >"${SAVE_ERROR}" 2>&1 || show_error
```


## scripts/mkimage @ 8ebaf8daad: lines 222-275 (excerpt)

```text
222  elif [ "${BOOTLOADER}" = "u-boot" ]; then
223    # create bootloader configuration
224    echo "image: creating bootloader configuration... (u-boot)"
225    if [ -f "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage" ]; then
226      . "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage"
227    elif [ -f "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage" ]; then
228      . "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage"
229    else
230      echo "image: skipping u-boot. no mkimage script found"
231    fi
232  
233    echo "image: copying files to part1..."
234    mcopy "${TARGET_IMG}/${BUILD_NAME}.kernel" "::/${KERNEL_NAME}" >"${SAVE_ERROR}" 2>&1 || show_error
235    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM >"${SAVE_ERROR}" 2>&1 || show_error
236    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5" >"${SAVE_ERROR}" 2>&1 || show_error
237    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5 >"${SAVE_ERROR}" 2>&1 || show_error
238  
239  elif [ "${BOOTLOADER}" = "arm-efi" ]; then
240    # create bootloader configuration
241    echo "image: creating bootloader configuration... (arm-efi)"
242    if [ -f "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage" ]; then
243      . "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/bootloader/mkimage"
244    elif [ -f "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage" ]; then
245      . "${PROJECT_DIR}/${PROJECT}/bootloader/mkimage"
246    else
247      echo "image: skipping arm-efi. no mkimage script found"
248    fi
249  
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
271    mcopy "${TARGET_IMG}/${BUILD_NAME}.system" ::/SYSTEM
272    mcopy "${RELEASE_DIR}/target/KERNEL.md5" "::/${KERNEL_NAME}.md5"
273    mcopy "${RELEASE_DIR}/target/SYSTEM.md5" ::/SYSTEM.md5
274  
275  fi # bootloader
```


## config/functions @ 8ebaf8daad: lines 1179-1229 (excerpt)

```text
1179  find_path() {
1180    local test_func="$1" search="$2" default="$3"
1181    local dir match wildcard=0 ftype
1182  
1183    # support wildcard matches
1184    [[ $search =~ \* || $search =~ \? ]] && wildcard=1
1185  
1186    [ "$test_func" = "-f" ] && ftype="file" || ftype="dir"
1187  
1188    for dir in $PROJECT_DIR/$PROJECT/devices/$DEVICE/packages/$PKG_NAME \
1189               $PROJECT_DIR/$PROJECT/devices/$DEVICE \
1190               $PROJECT_DIR/$PROJECT/packages/$PKG_NAME \
1191               $PROJECT_DIR/$PROJECT \
1192               $DISTRO_DIR/$DISTRO/packages/$PKG_NAME \
1193               $DISTRO_DIR/$DISTRO \
1194               $PKG_DIR \
1195               ; do
1196      # ignore directories with missing DEVICE or PKG_NAME components
1197      [[ $dir =~ /packages/$ ]] && continue
1198      [[ $dir =~ /devices/$ ]] && continue
1199      [[ $dir =~ /devices//packages/$PKG_NAME$ ]] && continue
1200  
1201      if [ $wildcard -eq 1 ]; then
1202        ls $dir/$search 1>/dev/null 2>&1 && match="$dir/$search" && break
1203      else
1204        [ $test_func "$dir/$search" ] && match="$dir/$search" && break
1205      fi
1206    done
1207  
1208    if [ -z "$match" -a -n "$default" ]; then
1209      if [[ $default =~ \* || $default =~ \? ]]; then
1210        ls $default 1>/dev/null 2>&1 && match="$default"
1211      else
1212        [ $test_func "$default" ] && match="$default"
1213      fi
1214    fi
1215  
1216    if [ -n "$match" ]; then
1217      FOUND_PATH="$match"
1218      [ "${VERBOSE_FIND_PATH,,}" = "yes" ] && echo "find_path: Searching for $ftype: \"$search\", found: \"$FOUND_PATH\"" >&2
1219      return 0
1220    else
1221      unset FOUND_PATH
1222      [ "${VERBOSE_FIND_PATH,,}" = "yes" ] && echo "find_path: Searching for $ftype: \"$search\" - not found" >&2
1223      return 1
1224    fi
1225  }
1226  
1227  find_file_path() {
1228    find_path -f "$1" "$2"
1229  }
```


## packages/virtual/image/package.mk @ 8ebaf8daad: lines 1-12 (excerpt)

```text
 1  # SPDX-License-Identifier: GPL-2.0-only
 2  # Copyright (C) 2019-present Team LibreELEC (https://libreelec.tv)
 3  
 4  PKG_NAME="image"
 5  PKG_LICENSE="GPL-2.0-only"
 6  PKG_SITE="https://libreelec.tv"
 7  PKG_DEPENDS_TARGET="toolchain squashfs-tools:host pigz:host dosfstools:host fakeroot:host kmod:host mtools:host populatefs:host libc gcc linux linux-drivers linux-firmware ${BOOTLOADER} busybox util-linux corefonts network misc-packages debug hdparm parted dosfstools e2fsprogs exfatprogs usbutils procps-ng"
 8  PKG_SECTION="virtual"
 9  PKG_LONGDESC="Root package used to build and create complete image"
10  
11  # nano text editor
12  [ "${NANO_EDITOR}" = "yes" ] && PKG_DEPENDS_TARGET+=" nano"
```


## packages/tools/syslinux/package.mk @ 8ebaf8daad: lines 53-80 (excerpt)

```text
53  makeinstall_host() {
54    mkdir -p ${TOOLCHAIN}/bin
55      cp bios/linux/syslinux ${TOOLCHAIN}/bin
56      cp bios/mtools/syslinux ${TOOLCHAIN}/bin/syslinux.mtools
57  
58    mkdir -p ${TOOLCHAIN}/share/syslinux
59      cp bios/mbr/mbr.bin ${TOOLCHAIN}/share/syslinux
60      cp bios/mbr/gptmbr.bin ${TOOLCHAIN}/share/syslinux
61      cp efi64/efi/syslinux.efi ${TOOLCHAIN}/share/syslinux/bootx64.efi
62      cp efi64/com32/elflink/ldlinux/ldlinux.e64  ${TOOLCHAIN}/share/syslinux
63      # BIOS files (required for syslinux 6.x)
64      cp bios/com32/elflink/ldlinux/ldlinux.c32 ${TOOLCHAIN}/share/syslinux/
65  }
66  
67  makeinstall_target() {
68    mkdir -p ${INSTALL}/usr/bin
69      cp bios/linux/syslinux ${INSTALL}/usr/bin
70  
71    ${STRIP} ${INSTALL}/usr/bin/syslinux
72  
73    mkdir -p ${INSTALL}/usr/share/syslinux
74      cp bios/mbr/mbr.bin ${INSTALL}/usr/share/syslinux
75      cp bios/mbr/gptmbr.bin ${INSTALL}/usr/share/syslinux
76      cp efi64/efi/syslinux.efi ${INSTALL}/usr/share/syslinux/bootx64.efi
77      cp efi64/com32/elflink/ldlinux/ldlinux.e64  ${INSTALL}/usr/share/syslinux
78      # BIOS files (required for syslinux 6.x)
79      cp bios/com32/elflink/ldlinux/ldlinux.c32 ${INSTALL}/usr/share/syslinux/
80  }
```


## packages/tools/installer/scripts/installer @ 8ebaf8daad: lines 190-205 (excerpt)

```text
190      if [ "$GPT" = "1" ]; then
191        parted -s $INSTALL_DEVICE mklabel gpt >> $LOGFILE 2>&1
192      else
193        parted -s $INSTALL_DEVICE mklabel msdos >> $LOGFILE 2>&1
194      fi
195  
196      msg_progress_install "9" "Writing Master Boot Record on $INSTALL_DEVICE"
197      if [ "$GPT" = "1" ]; then
198        cat /usr/share/syslinux/gptmbr.bin > $INSTALL_DEVICE
199      else
200        cat /usr/share/syslinux/mbr.bin > $INSTALL_DEVICE
201      fi
202  
203      partsize_system_start=$PARTSIZE_SYSTEM_OFFSET
204      partsize_system_end=$(((PARTSIZE_SYSTEM * 1024 * 1024 / 512) + partsize_system_start - 1))
205      partsize_storage_start=$((partsize_system_end + 1))
```


## packages/tools/installer/scripts/installer @ 8ebaf8daad: lines 285-300 (excerpt)

```text
285  
286  menuentry "@DISTRONAME@" {
287  	search --set -f /KERNEL
288  	linux /KERNEL boot=UUID=$UUID_SYSTEM disk=UUID=$UUID_STORAGE quiet
289  }
290  EOF
291  
292      # uefi boot / hybrid mode
293      cp /usr/share/syslinux/bootx64.efi $TMPDIR/part1/EFI/BOOT
294      cp /usr/share/syslinux/ldlinux.e64 $TMPDIR/part1/EFI/BOOT
295      cp /usr/share/grub/bootia32.efi $TMPDIR/part1/EFI/BOOT
296      sync
297  
298      # umount system partition, remove mountpoint
299      msg_progress_install "85" "Unmount $TMPDIR/part1"
300      umount $TMPDIR/part1 >> $LOGFILE 2>&1
```


## projects/ROCKNIX/packages/tools/grub/package.mk @ 8ebaf8daad: lines 70-86 (excerpt)

```text
70  }
71  
72  makeinstall_target() {
73    ${PKG_BUILD}/.${HOST_NAME}/grub-mkimage -d grub-core -o bootaa64.efi -O arm64-efi -p /boot/grub \
74      boot linux ext2 fat squash4 part_msdos part_gpt normal search search_fs_file search_fs_uuid \
75      search_label chain reboot loadenv test gfxterm efi_gop
76  
77    mkdir -p ${INSTALL}/usr/share/bootloader/boot/grub
78      cp -av ${PKG_DIR}/config/* ${INSTALL}/usr/share/bootloader/boot/grub
79  
80    mkdir -p ${INSTALL}/usr/share/bootloader/EFI/BOOT
81      cp -av bootaa64.efi ${INSTALL}/usr/share/bootloader/EFI/BOOT
82  
83    # Create grub configuration
84    generate_grub_cfg_body > "${INSTALL}/usr/share/bootloader/boot/grub/grub.cfg"
85  
86  }
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


## projects/ROCKNIX/devices/H700/packages/u-boot/package.mk @ 8ebaf8daad: lines 20-36 (excerpt)

```text
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


## projects/ROCKNIX/packages/sysutils/busybox/scripts/init @ 8ebaf8daad: lines 425-440 (excerpt)

```text
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


## tools/vm-pair @ 8ebaf8daad: lines 30-80 (excerpt)

```text
30  # RUNTIME is VM_QEMU_RUNTIME_DIR (default /tmp). Keep both VM_PAIR_DIR and
31  # VM_QEMU_RUNTIME_DIR unchanged for up, info, SSH, serial, reimage and down;
32  # commands do not discover or take ownership of guests under another root.
33  set -euo pipefail
34  HERE=$(cd "$(dirname "$0")" && pwd)
35  ROOT=$(cd "$HERE/.." && pwd)
36  VM_TOOL="$ROOT/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm"
37  DIR="${VM_PAIR_DIR:-/tmp/rocknix-vm-pair}"
38  KEY="$DIR/qa-key"
39  # Keep short-lived socket/PID writes off a quota-limited /tmp when requested.
40  # vm-qa uses the same root; the default remains compatible with standalone tools.
41  RUNTIME="${VM_QEMU_RUNTIME_DIR:-/tmp}"
42  [[ "$RUNTIME" = /* && ! "$RUNTIME" =~ [[:space:]] ]] || {
43    echo 'vm-pair: VM_QEMU_RUNTIME_DIR needs an absolute path without whitespace' >&2; exit 2;
44  }
45  check_runtime() {
46    local probe
47    (umask 077; mkdir -p "$RUNTIME") || return 1
48    probe=$(mktemp "$RUNTIME/.pixelelated-vm-write-XXXXXX") || return 1
49    if ! printf 'pid-file-write-check\n' > "$probe"; then
50      rm -f "$probe"; echo 'vm-pair: runtime directory cannot accept PID writes' >&2; return 1
51    fi
52    rm -f "$probe"
53  }
54  
55  # VM_GL=none puts the guests on the software renderer; the launcher's default
56  # is hardware GL through virgl on the host's first Mesa render node (#291), and
57  # the harness takes its frames over the VNC display when the monitor has no surface.
58  # Per-guest settings: letter -> monitor serial pidfile vnc sshport mac
59  # (every `read` below names all six: the last variable takes the rest of the
60  # line, so a field added here without a slot there lands in the one before it)
61  settings() {
62    case "$1" in
63      a) echo "$RUNTIME/rocknix-qemu-monitor.sock $RUNTIME/rocknix-qemu-serial.sock $RUNTIME/rocknix-qemu.pid 9 10022 52:54:00:52:4E:58" ;;
64      b) echo "$RUNTIME/rocknix-qemu-monitor-b.sock $RUNTIME/rocknix-qemu-serial-b.sock $RUNTIME/rocknix-qemu-b.pid 10 10023 52:54:00:52:4E:59" ;;
65      *) echo "vm-pair: guest is a or b, not '$1'" >&2; exit 2 ;;
66    esac
67  }
68  
69  # One guest booted from its disk, with its own settings.
70  start_one() {
71    local mon ser pid vnc port mac
72    read -r mon ser pid vnc port mac <<<"$(settings "$1")"
73    local rc=0 started
74    "$VM_TOOL" run --headless --daemonize ${VM_GL:+--gl "$VM_GL"} --monitor "$mon" --serial "$ser" --pidfile "$pid" --vnc "$vnc" --ssh-port "$port" --mac "$mac" "$DIR/vm-$1.qcow2" 2>&1 | grep -v pw.conf || rc=${PIPESTATUS[0]}
75    if [ "$rc" != 0 ]; then
76      echo "vm-pair: guest $1 launch failed ($rc)" >&2; return "$rc"
77    fi
78    started=$(cat "$pid") || { echo "vm-pair: guest $1 has no PID file" >&2; return 1; }
79    # A successful launcher alone does not prove a guest. Refuse stale/wrong
80    # PID files before claiming up or waiting for an unrelated serial endpoint.
```


## projects/ROCKNIX/devices/AMD64/config/kernel-firmware.dat @ 8ebaf8daad: lines 1-40 (excerpt)

```text
 1  # MICROCODE_AMD (Van Gogh/Phoenix/Hawk Point APUs - Deck, Ally, Legion Go, Ayaneo)
 2  amd-ucode/*
 3  
 4  # DRM_AMDGPU (AMD APU graphics - most handhelds)
 5  amdgpu/*
 6  
 7  # DRM_I915 (Intel graphics - GPD Win, OneXPlayer Intel models, older Aya Neo Air)
 8  i915/*
 9  
10  # DRM_XE (Intel Meteor Lake/Lunar Lake handhelds - newer GPD/OneXPlayer)
11  xe/*
12  
13  # IWLWIFI (Intel WiFi)
14  iwlwifi-*
15  
16  # ATH10K (Qualcomm Atheros 802.11ac)
17  ath10k/*
18  
19  # ATH11K (Qualcomm Atheros WiFi 6)
20  ath11k/*
21  
22  # ATH12K (Qualcomm Atheros WiFi 7)
23  ath12k/*
24  
25  # MEDIATEK_MT76 WiFi (MT7921 chip uses MT7961-codenamed firmware; MT7922 uses its own; MT7925 has a subdir)
26  mediatek/WIFI_RAM_CODE_MT7961*.bin
27  mediatek/WIFI_MT7961_patch_mcu*.bin
28  mediatek/BT_RAM_CODE_MT7961*.bin
29  mediatek/WIFI_RAM_CODE_MT7922*.bin
30  mediatek/WIFI_MT7922_patch_mcu*.bin
31  mediatek/BT_RAM_CODE_MT7922*.bin
32  mediatek/mt7925/*
33  
34  # RTW89 (Realtek WiFi 6/6E - some Ayaneo/OneXPlayer variants)
35  rtw89/*
36  
37  # Realtek onboard NIC/misc
38  realtek/*
39  
40  # Bluetooth - Realtek (pairs with rtw89 combo cards)
```


## projects/ROCKNIX/devices/H700/config/kernel-firmware.dat @ 8ebaf8daad: lines 1-18 (excerpt)

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


## projects/ROCKNIX/devices/SM8550/config/kernel-firmware.dat @ 8ebaf8daad: lines 1-8 (excerpt)

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


## tools/renovation-inventory @ 2174265e9c: lines 30-40 (excerpt)

```text
30    stay inside a segment, `{a,b}` alternates globs (no nesting). A path must match
31    exactly one area: none counts as `unassigned`, two or more as `ambiguous`.
32    A bare `**` on the distribution is refused, since it would make
33    `unassigned` 0 whatever the tree held.
34  - Tiers: fork-own is `git diff --name-only <merge-base> HEAD` (the merge base
35    with upstream/next, or on ES with rocknix/master); a fork-own path that
36    upstream also changed since the base carries `overlap`. Every other path is
37    upstream-carried. Every `*.patch` and kernel `linux*.conf` under packages/
38    or projects/ is vendor-carried, `tier_note: fork-written` when fork-own.
39  - Reachability: `tools/viewplan` per device and arch the Makefile builds,
40    `image` for the 64-bit plans and `arm` (projects/ROCKNIX/packages/virtual/arm)
```


## docs/qa-logs/2026-10-11-usb-revision/guest02/run.py @ 8ebaf8daad: lines 1-25 (excerpt)

```text
 1  from pathlib import Path
 2  import subprocess,json,hashlib,time,os
 3  P=Path('/workspace/tmp/pixelelated-m7-usb-531-02')
 4  R=Path('/workspace/repos/rocknix.worktrees/m7-p5-usb-revision')
 5  opts=['-i',str(P/'qa-key'),'-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','BatchMode=yes','-o','ConnectTimeout=5']
 6  def ssh(s): return subprocess.run(['ssh',*opts,'-p','10331','root@127.0.0.1',s],capture_output=True,text=True,timeout=60)
 7  def copy(src,dst): subprocess.run(['scp','-q',*opts,'-P','10331',str(src),'root@127.0.0.1:'+dst],check=True,timeout=30)
 8  def dump(name,obj): (P/name).write_text(json.dumps(obj,indent=2)+'\n')
 9  try:
10   subprocess.run(['/usr/bin/python3','-I','-u',str(P/'create.py')],check=True,timeout=300)
11   protected='sha256sum /storage/.config/system/configs/system.cfg /storage/.config/emulationstation/es_settings.cfg /storage/.cache/systemd-machine-id'
12   before=ssh(protected);assert before.returncode==0; (P/'protected-before.txt').write_text(before.stdout)
13   kernel=ssh('zcat /proc/config.gz | grep CONFIG_USB_GADGET');dump('guest-kernel.json',{'returncode':kernel.returncode,'stdout':kernel.stdout,'stderr':kernel.stderr})
14   # /proc/config.gz is optional; the frozen input config is retained separately.
15   source_config=(P/'frozen-linux.config').read_text();assert '# CONFIG_USB_GADGET is not set' in source_config
16   gadget=ssh('test -d /sys/kernel/config/usb_gadget');dump('guest-gadget-presence.json',{'returncode':gadget.returncode,'configfs_gadget_directory_present':gadget.returncode==0,'frozen_config_sha256':hashlib.sha256((P/'frozen-linux.config').read_bytes()).hexdigest(),'kernel_config_exposed':kernel.returncode==0})
17   copy(R/'tools/usb-gadget-test','/tmp/pix531-test')
18   copy(R/'projects/ROCKNIX/packages/rocknix/sources/scripts/usbgadget','/tmp/pix531-usbgadget')
19   h=ssh('sha256sum /tmp/pix531-test /tmp/pix531-usbgadget');assert h.returncode==0;(P/'guest-source-hashes.txt').write_text(h.stdout)
20   assert h.stdout.splitlines()[0].split()[0]==hashlib.sha256((R/'tools/usb-gadget-test').read_bytes()).hexdigest()
21   assert h.stdout.splitlines()[1].split()[0]==hashlib.sha256((R/'projects/ROCKNIX/packages/rocknix/sources/scripts/usbgadget').read_bytes()).hexdigest()
22   results=[]
23   for name,source,expected in [('old','/usr/bin/usbgadget',1),('fixed','/tmp/pix531-usbgadget',0)]:
24    r=ssh('python3 -I /tmp/pix531-test --source '+source+' --shell /bin/sh --output /tmp/pix531-'+name+'.json')
25    results.append({'name':name,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});dump('test-results.json',results)
```


## projects/ROCKNIX/packages/linux/package.mk @ 651150fc88: lines 15-60 (excerpt)

```text
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
