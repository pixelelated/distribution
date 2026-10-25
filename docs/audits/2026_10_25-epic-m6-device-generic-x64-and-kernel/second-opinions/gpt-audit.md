Packet-only review: I have not reproduced the M7 measurements. Citations below use unambiguous path suffixes; `linux/package.mk` means the ROCKNIX override unless another commit is specified.

## 1. The configuration

**G-1 — narrowed — `GENERIC_X64/linux/linux.x86_64.conf:3`; `linux/package.mk:36-40,154-207,293-316`.**  
The first reader is right about the essential pipeline: copy the 6.15.6 configuration, modify it, and normally run `yes "" | kernel_make oldconfig` for 7.1.2 with stdout suppressed. “Forces four values” is not a complete description of the recipe: it also conditionally disables NFS, iSCSI, WireGuard and graphics options, and constructs firmware settings, even where those operations produce no additional difference for this guest. `listnewconfig` still prints, and interactive modes are explicitly available. The resulting gap includes removed symbols and changed dependencies or defaults, not merely symbols newly introduced since 6.15.6.

**G-2 — confirmed — `docs/qa-logs/2026-10-11-usb-revision/guest02/run.py:13-16`; reported `build/linux-7.1.2/.config:6249`; `linux/package.mk:64-66,93-97`.**  
F-04 remains a provenance defect, not a demonstrated wrong-behaviour claim: the reported built configuration corroborates the frozen input’s `USB_GADGET` assertion. The test actually labels that file a “frozen input config,” so describing it simply as mistaking the input for the running configuration is too strong. Absence of `/sys/kernel/config/usb_gadget` alone would not prove the compile-time setting, but the reported built setting supplies the missing corroboration. “One reader” must also mean one identified proof, not the only code reader: the recipe itself consults the committed configuration for perf and regulatory-database dependencies.

**G-3 — narrowed — `linux/package.mk:146-316,383-406`; quoted `GENERIC_X64/linux/linux.x86_64.conf:162-163`; `guest02/run.py:13-16`.**  
The regeneration check is sound only if it reproduces the **whole configuration preparation**, using the same patched kernel, device/distro options, firmware inputs and toolchain—not just four assignments followed by `oldconfig`. Compare that result with the saved `.image/.config`, and separately assert preservation of the ten fork settings; “only paths and toolchain lines differ” is an expectation to verify, not a guaranteed property across different toolchains. Given the quoted `CONFIG_IKCONFIG=m` and `CONFIG_IKCONFIG_PROC=y`, **`modprobe configs && zcat /proc/config.gz` is correct**; the module is named `configs`, and the recipe installs kernel modules. Require successful loading and identification of the running kernel before comparison. The old probe’s failed `zcat | grep` is consistent with an unloaded module, but does not uniquely establish that explanation.

## 2. The firmware

**G-4 — narrowed — `kernel-firmware/package.mk:39-50,57-69,92`; `config/functions:1188-1228`; `kernel-firmware/firmwares/x86_64.dat:1`.**  
The fallback is consistent with the reported tree, but absence of a device-local list alone is insufficient proof. `find_file_path` searches, in order, the device/package directory, device directory, project/package directory, project directory, distro/package directory, distro directory and `PKG_DIR`; only after no match does this recipe select `any.dat` plus `${TARGET_ARCH}.dat`. Thus GENERIC_X64 cannot inherit AMD64’s restricted list, and the reported no-match case selects `*`, followed by additive project/device lists and any cleanup hook. The first reader is wrong to call `any.dat` exclusively “the aarch64 fallback”: this code includes it in the x86 fallback too.

**G-5 — confirmed — `vm/generic-x64-vm:89-121,338-435`; `GENERIC_X64/options:29-36,88-91`.**  
None of the canonical guest’s emulated devices requires the real GPU, radio, panel or physical-NIC firmware selected by that fallback. The “four devices” description is incomplete—the launcher also adds xHCI, keyboard/tablet, RNG and watchdog devices—but those additions do not supply a justification for the firmware collection. OVMF is separately located host-side firmware, not a consumer of the guest’s installed linux-firmware tree. This conclusion is limited to the canonical guest, not arbitrary passthrough devices or the optional developer installation onto physical hardware.

**G-6 — narrowed — `kernel-firmware/package.mk:25-30,49-69`; `projects/ROCKNIX/options:9`; `GENERIC_X64/options:11-15`.**  
The reported 6,158 files and 2,876,913,748 bytes are plausible for this code: it walks the selected trees and dereferences firmware symlinks with `cp -L`. I would retain **Medium as a developer build/image-efficiency finding**, not as a shipped-handheld correctness or gameplay finding. Those are raw staged bytes, not a measured 2.88 GB increase in the compressed image or a demonstrated boot-time penalty. A device list would reduce target staging and image contents, but would not eliminate the full `.copied-firmware` preparation or firmware download.

**G-7 — confirmed — `linux/package.mk:69-72,197-207`; `GENERIC_X64/options:29-36`.**  
F-02’s block really is keyed on architecture alone: neither `DEVICE`, selected Mesa drivers nor enabled DRM drivers guard it. It selects GPU firmware **and** AMD/Intel microcode and Ethernet firmware, so calling the entire collection “real-GPU firmware” is inaccurate. Disabling the inherited physical-GPU drivers does not itself change this list-construction code; firmware trimming needs its own verified change. The reported total bzImage size cannot isolate firmware cost from the kernel and initramfs.

**G-8 — narrowed — `linux/package.mk:197-207,285-315`.**  
The reported configuration totals are internally consistent—`6205 − 189 + 364 = 6380`—but the reported **1,254-entry final firmware list is suspect**. Its category counts already sum to 1,254, while this recipe appends `regulatory.db` and `regulatory.db.p7s` whenever the copied configuration has `CONFIG_CFG80211=y`, which its comment says applies to non-AMD64 devices. Under that premise, the final list would contain those two additional entries; either the premise is false for this configuration, the measurement counted only selected categories, or that build did not execute this exact recipe. The reported 1,255 external files do not resolve this, because the list generator includes symlinks and applies filename filters. Equality of the committed seed configuration is therefore **not sufficient provenance for “the result of exactly this step”** at this commit.

## 3. The boot files

**G-9 — confirmed — `bootloader/install:14-23,45-61`; `H700/packages/u-boot/package.mk:27-35`; `rocknix-abl/package.mk:12-17`; `scripts/mkimage:142-180,222-263`.**  
For the specified loader selections, H700 reaches the `u-boot` echo branch, SM8550 reaches `qcom-abl|arm-efi`, and GENERIC_X64 reaches the syslinux copy branch. The two echo branches are not missing installation steps: their package recipes already stage bootloader assets, and their image paths source the project’s `mkimage`. GENERIC_X64 instead uses the separate syslinux image path and toolchain loader files. The Qualcomm comment’s literal claim that there is “nothing under `/usr/share`” is misleading—`rocknix_abl` is staged there—but no second generic copy is required.

**G-10 — narrowed — `bootloader/release:4-5`; `H700/packages/u-boot/package.mk:28-34`; `rocknix-abl/package.mk:13-17`; `bootloader/install:16-18`; `scripts/image:280-292`.**  
`release` has a nonempty source glob on all three **after successful normal staging**; a directory such as `rocknix_abl` is a perfectly valid source for `cp -a`. That confirms the first reader’s narrow glob-presence argument, not an unconditional safety guarantee. Missing staging, copy errors or an empty directory still produce a failing `cp`, and the shown caller does not test the sourced script’s status before continuing.

**G-11 — confirmed — `bootloader/install:14-23`; `bootloader/release:5`; `installer:198-200,293-294`; `scripts/mkimage:179-180`; `busybox/scripts/init:427-435`.**  
F-05 is correct as a **guest-runtime** finding: the shown installer reads `/usr/share/syslinux`, image creation reads the toolchain copy, and the update hook requires an `update.sh` that the reported GENERIC_X64 tree lacks. The duplicate is not globally unread, because `release` consumes it during image assembly. Consequently, removing that copy alone would expose the unconditional release glob; its present justification is build-chain compatibility, not a guest boot-time reader.

**G-12 — narrowed — `bootloader/install:25-43,63-80`; `projects/ROCKNIX/packages/tools/grub/package.mk:72-84`; `scripts/image:272-287`.**  
The grub branch would **warn and return success**, not necessarily fail: its nonexistent-source check skips `cp`, and the script ends with a successful completion message. Moreover, the actual grub package already populates `/usr/share/bootloader/boot/grub` and `EFI/BOOT`, so the first reader’s associated “empty bootloader directory” failure model is wrong for that package. Its conclusion that this branch checks the wrong source location is nevertheless correct. The empty-loader branch is additionally unreachable through this caller’s outer nonempty-`BOOTLOADER` test, independently of the device inventory.

## 4. The launcher

**G-13 — narrowed — `tools/vm-pair:34-36,70-74`; reported `tools/last-good-scripts-test:3406-3571`; `vm/generic-x64-vm:793-802`.**  
`vm-pair` unquestionably invokes the canonical source file by absolute path through `VM_TOOL`, not by basename lookup. “The only tool” should mean the only identified operational launcher caller: the audit itself reports a test tool copying and executing the launcher’s UTM functionality. That fixture is not a second production invocation of the original path, but it is more than prose. Repository-wide uniqueness and absence of a symlink remain the first reader’s reported search results, not something these excerpts independently establish.

**G-14 — confirmed — `tools/vm-pair:55-80`; `vm/generic-x64-vm:280-305,324-336,374-421,664-745,790-809`.**  
Every argument passed at `vm-pair:74` exists with the intended operational meaning. VNC values 9 and 10 mean loopback displays on ports 5909 and 5910; monitor/serial are Unix sockets, and PID-file creation plus daemonization apply to the headless path. The SSH override updates both forwarding and the fw_cfg advertisement, while the MAC override changes the guest NIC identity. GL selection also matches `vm-pair`’s comments, although `--headless` help describes only the software branch rather than its current automatic-GL default. Daemonization is not guest-readiness proof, which `vm-pair:78-80` explicitly recognizes.

**G-15 — confirmed — `vm/generic-x64-vm:24-26,47-49,645-650`; `tools/vm-pair:36,70-74`.**  
Keeping this device-specific launcher beside its profile and bundled documentation is a sound design; those locations are explicit runtime dependencies. I would not move it into `tools/` merely to make a basename discoverable. Keep one authoritative integration path, and route another operational caller through `vm-pair` or a shared resolver rather than proliferating copied `VM_TOOL` assignments. Documentation should use the supported wrapper or full path, without implying an installation onto `PATH`.

## 5. Findings F-01 to F-10

**G-16 — narrowed — F-01 — `kernel-firmware/package.mk:10,25-30,39-69`; `vm/generic-x64-vm:338-435`.**  
Keep the finding for the canonical guest, with the cost and scope qualifications in G-5 and G-6. The recipe does not explicitly include the device firmware list in `PKG_NEED_UNPACK`, but the categorical assertion that adding one “rebuilds nothing” requires the stamp engine omitted from this packet; the recipe alone establishes an unrepresented input, not every possible invalidation route.

**G-17 — narrowed — F-02 — `linux/package.mk:197-207,293-304`.**  
Keep Low efficiency, but describe a mixed GPU/microcode/NIC payload rather than 1,254 GPU files. The architecture-only selection is confirmed; the exact final count needs reconciliation with the regulatory-database append, and disabling DRM drivers alone is not a demonstrated firmware fix.

**G-18 — confirmed — F-03 — `bootloader/install:1-5`.**  
Accepting the supplied addition history and attribution rule, this is a valid Low standards finding: the header does not identify the fork’s authorship. That is not, by itself, a legal conclusion that every existing copyright credit or its starting year is invalid. Preserve any justified prior credits while correcting the local provenance.

**G-19 — confirmed — F-04 — `GENERIC_X64/linux/linux.x86_64.conf:3`; `linux/package.mk:154-174,306-316`; `guest02/run.py:14-16`.**  
Keep Low provenance, not a demonstrated kernel-behaviour bug. The regeneration packet needs G-3’s complete-input qualification, and removed/new symbol counts must not be represented as equivalent counts of lost/new features: Kconfig renames and dependency changes also contribute.

**G-20 — confirmed — F-05 — `bootloader/install:18`; `bootloader/release:5`; `installer:198-200,293-294`.**  
The guest-runtime duplicate is a legitimate dead-end finding. Its build-time consumer is real, so “unread” must retain that scope and any removal must account for the release step.

**G-21 — narrowed — F-06 — `bootloader/install:25-43,63-80`; `scripts/image:272-287`; `grub/package.mk:77-84`.**  
The reported device selections leave these branches unused, but unused defensive cases are not automatically harmful or removable. The grub source check is wrong for this package, yet the claimed consequence must be narrowed to a warning/no-op rather than a failed copy or necessarily empty staging directory.

**G-22 — narrowed — F-07 — `serial-debug-shell.service:4-14`; `vm/generic-x64-vm:439-588,645-650,793-802`.**  
D-QA-053 does not make a macOS developer workflow obsolete: the launcher still implements and packages that route. Keep this as a support/documentation decision, not a dead-code finding inferred from the guest’s developer-only status. The reported fixture establishes exercised packaging, not successful boot or current cloud-linking behaviour on a Mac.

**G-23 — confirmed — F-08 — `device-tree-overlays/package.mk:12-24`; `bootloader/rkhelper:7-17,20-24,27-48`; `H700/packages/u-boot/package.mk:27-35`.**  
The reported inventory labels overstate file-level reach: compilation selects only `${DEVICE}/*.dts`, while the reported `rkhelper` callers and its device cases are Rockchip-specific. Thus the six RK3566/RK3588/S922X overlay sources impose no compiled-overlay payload on H700, and `rkhelper` is not an installed handheld helper. The first reader’s repeated citation to overlay-package lines 8–11 is wrong: those are metadata; **lines 13–20 are the decisive selectors**.

**G-24 — narrowed — F-09 — `651150fc88:projects/ROCKNIX/packages/linux/package.mk:21-55`; `8ebaf8daad:projects/ROCKNIX/packages/linux/package.mk:21-55`.**  
The merge risk is real, but the first reader is wrong that GENERIC_X64 would simply “take another version.” With the upstream case substituted, GENERIC_X64 matches **no branch**, so this override supplies no version, checksum or download URL for it; there is no default selection and no shown delegation to the generic recipe. The exact downstream failure depends on package-framework initialization, but a valid alternate kernel build is not established. Preserve an explicit GENERIC_X64 version case; this is potentially a broken-build merge regression, not merely configuration drift.

**G-25 — narrowed — F-10 — `GENERIC_X64/options:23-27,88-91`; `scripts/mkimage:178-180`; `GENERIC_X64/linux/linux.x86_64.conf:3`; `projects/Generic/linux/linux.x86_64.conf:3`.**  
Documenting syslinux’s EFI role and the configuration-generation contract would be useful; syslinux versus UEFI is not itself an inconsistency. Absence of a u-boot-specific knob does not require an exceptional explanation on a syslinux device. Also, the supplied nearest-candidate diff does **not** establish that the file was copied from a particular historical Generic configuration: the first reader should not turn similarity into proven ancestry.

## 6. What the first reader missed

**G-26 — new — `rocknix-abl/package.mk:13-17`; `bootloader/mkimage:108-113`; `bootloader/install:50-58`; `scripts/mkimage:257-263`.**  
The blanket “nothing behaves wrongly on a shipped device” conclusion misses a concrete SM8550 copy defect. `rocknix_abl` is staged as a **directory containing the ELF and flashing files**, but `mkimage_abl()` passes that directory to `mcopy` **without recursive `-s`**. That invocation does not transfer the intended directory contents onto the image, and its status is not checked locally. This proves a defective shipped-device asset-copy path, not that every already-provisioned SM8550 necessarily fails to boot. Adding error reporting alone would expose the failure, not correct the copy semantics.

**G-27 — new — `bootloader/install:16-22,80`; `bootloader/release:4-5`; `bootloader/mkimage:18-29,35,59,88-94`; `scripts/image:280-292`.**  
There are reached error-masking paths, not merely hypothetical failures in unused branches. A missing syslinux source becomes warnings followed by a successful “completed” message, and a failed release copy is not checked by the non-errexit image caller. Likewise, the H700-capable `mkimage_uboot` dispatch reports a missing loader with `echo`, returning success, while several project `mcopy` operations lack the surrounding script’s explicit error guards. These are failure-handling defects under missing assets or copy errors; they do not imply that normal staging always fails.

**G-28 — new — `kernel-firmware/package.mk:57-69,91-92`.**  
The firmware cleanup expression conflates “no cleanup script exists” with “the cleanup script ran and failed”: both become success through `|| true`. That suppression is explicit and would survive even an errexit-enabled caller. Conversely, bad firmware patterns and missing firmware files have explicit failure paths, so the image script’s lack of `set -e` should not be generalized into a claim that every firmware error is ignored. No supplied evidence establishes that a cleanup failure actually caused the measured tree size.

**G-29 — confirmed — `sway-generic-x64:9-35`.**  
I find no reversed virgl-bit test: virtio’s sysfs feature string is lowest-bit-first, so a validated string beginning with `0` correctly identifies absence of feature bit zero. The wrapper also requires one virtio child, the `virtio_gpu` driver, at least 64 binary characters and no explicit renderer override; unknown cases retain the existing selection. Narrow P17 to those prerequisites, especially the requirement that `WLR_DRM_DEVICES` already name one card, rather than claiming universal automatic detection.

**G-30 — confirmed — `serial-debug-shell.service:11-20,25-41`; `GENERIC_X64/options:74-76`; `scripts/mkimage:151-154`.**  
The serial conditions are correctly composed: virtualization is mandatory, and at least one of the two trigger-style console conditions must hold. The normal command line supplies the second console condition; it does not turn the three conditions into a permissive three-way OR. This is an intentional developer root-shell channel, not a demonstrated accidental shell on bare-metal installations.

**G-31 — new — `vm/generic-x64-vm:142-154,180-217,298,705,808-809`; `tools/vm-pair:41-52,63-64,78-80`.**  
The launcher’s careful socket protection does **not** extend to the PID file. It resolves `--pidfile`, thereby following a symlink, and hands the resulting path to QEMU without refusing unrelated existing files or aliases with other launch files. An existing symlink can consequently redirect QEMU’s PID-file write to another writable file; the predictable `/tmp` defaults make this more than a theoretical concern about a deliberately chosen output filename. Passing explicit paths from `vm-pair`, or checking the PID after launch, does not itself prevent that overwrite. This is a QA-host path-safety defect, not evidence of a guest kernel failure.

**G-32 — new — `vm/generic-x64-vm:180-217,233,298-301,400-401,808-809`.**  
The socket checks are conservative for a sequential launch, but checking and unlinking are not an atomic claim of the paths. Another launcher can replace a checked stale socket with a live socket before the first launcher reaches `unlink`, causing the live endpoint to be removed. The launcher also accepts identical monitor and serial paths without a distinctness check. These are concurrency/input-safety gaps requiring ownership or serialization, not proof that ordinary sequential `vm-pair` starts are broken.

**G-33 — new — `dtb_overlay:7-15,74-89,132-155`; `device-tree-overlays/package.mk:22-24`.**  
The helper does refuse unknown specializations and ordinary unmatched filenames, so it is not simply an unrestricted writer. However, acceptance of `None` is inside the candidate-file loop: an allowed specialization with no matching installed overlay cannot be cleared, because the loop never reaches that test. The unquoted `$3` in the second test and setter also loses argument boundaries and can interpret words such as `-o` as test operators, undermining the intended whitelist. Those are input-handling defects in the installed helper, not evidence that its normal space-free H700 filename fails. Its `[[...]]` and `+=` syntax additionally requires target-shell verification; this packet does not establish enough about `/bin/sh` to call that a proven interpreter failure.

**G-34 — new — `dtb_overlay:84-103,135-151`; `device-tree-overlays/package.mk:18-24`.**  
A valid selection can be reported successful even when the boot configuration was not updated. The script writes the setting first, ignores failure of the writable remount and `sed`, then the callers unconditionally `exit 0`. If the settings write succeeds but the flash update fails, requested state and boot state diverge while the command reports success. That is a concrete error-path bug in the H700-installed utility, independent of whether its normal overlay operation currently succeeds.

**G-35 — new — `linux/udev.d/10-bfq-sched.rules:1`.**  
`mmcbl*` is not a misspelling that misses MMC disks: it matches both `mmcblk0` **and partitions such as `mmcblk0p1`**. Partition devices lack their own `queue/scheduler`, so their add/change events cause this rule to attempt an invalid attribute write on a shipped MMC-based target. The whole-disk assignment can still succeed, making this a small reached rule defect rather than proof that BFQ is absent or storage is broken. The first reader’s observation that the VM uses virtio-blk does not dispose of the handheld-side error.

**G-36 — new — `linux/udev.d/40-usb_modeswitch.rules:4-14`; `linux/udev.d/30-disable-wakeup.rules:5-9`; `vm/generic-x64-vm:390-395`.**  
The Netgear rule’s `ATTRS` matching reaches descendant events, yet it always constructs `/dev/%k`; USB-device and interface kernel names are not the block-device paths that `eject` expects. Consequently, a matching dongle can generate spurious failing eject invocations before or alongside the relevant storage-node event; the rule needs an event/device-type scope, not merely VID/PID ancestry. The Realtek rules use current-device `ATTR` matching, so that particular fan-out criticism does not apply to them, and their normal-mode entry alone does not prove a switching regression. Nor does the wakeup rule establish a wrong wake policy on either handheld from the supplied evidence.