# Punch List — M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

**Independent depth:** one seat, GPT-6 Astra at `max`, its 36 items graded in `04` § Second opinion. Every `where` is at `8ebaf8daad`, unchanged at the dispatch tip `2103f0271d`. The lane removes nothing and edits no file under `packages/`, `projects/` or `tools/` (D-WORKFLOW-209). No defect behaves wrongly on a shipped device's normal path. The coordinator's dispositions (07:34 UTC, #658) made five items `bug`s, filed by the lane: #1086, #1087, #1088, #1089 and #1090.

The VM line, common to every item: **Can this be done on the VM? Yes, on the host:** reads at `8ebaf8daad`, local diffs, the M7 root's artefacts read-only (accepted 07:10 UTC, #658), and one `mtools` fixture under `/workspace/tmp/m6-t11/`. No guest, no device, no build, no plan, no network. Where an item's acceptance needs an image, that is said.

## PL-01: The QA guest installs all of linux-firmware (6,158 files, 2,876,913,748 bytes staged) because GENERIC_X64 has no `config/kernel-firmware.dat` and `x86_64.dat` is `*`

- **Severity:** Medium
- **Category:** Renovation
- **Question:** Q5
- **Source:** F-01 (G-5, G-6, G-16)
- **Owner area:** `projects/ROCKNIX/devices/GENERIC_X64/` (a new `config/kernel-firmware.dat`); `projects/ROCKNIX/packages/linux-firmware/kernel-firmware/package.mk`'s stamp (T5's E6)
- **What:** Give GENERIC_X64 its own firmware list, empty or minimal, since none of the guest's devices loads firmware. It lands after T5's E6 (`0c786d298e`) puts the list in the stamp, or the change rebuilds nothing (T5's P25). A fork-own change, for a stage-E stream or a Backlog the coordinator files.
- **Where:** `kernel-firmware/package.mk` (`find_file_path config/kernel-firmware.dat`, the `any.dat` plus `${TARGET_ARCH}.dat` fallback); `firmwares/x86_64.dat:1`; `vm/profile.json`; `generic-x64-vm:361-435`
- **Evidence:** `02` r23, r25; P13, P15
- **Already written:** the GENERIC_X64 images built so far carry the whole tree in their SYSTEM; nothing on a handheld; a QA guest updated in place takes the smaller image, and no state reads the firmware.
- **Acceptance:** after the change and E6, a GENERIC_X64 build's `install_pkg/kernel-firmware-*/.../firmware` holds what the list names (an open item for that image); on the host, `git ls-tree` shows `projects/ROCKNIX/devices/GENERIC_X64/config/kernel-firmware.dat`.

## PL-02: The upstream x86 block builds 1,254 firmware files (GPU, CPU microcode, NIC) into the guest's kernel, and the configuration builds amdgpu, radeon and i915 in, inherited from the Generic conf

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q5
- **Source:** F-02 (G-7, G-8, G-17)
- **Owner area:** `projects/ROCKNIX/packages/linux/package.mk:197-207` (upstream-carried, keyed on `TARGET_ARCH`); the guest's configuration
- **What:** A design for the coordinator, with T27's configuration shape: a `DEVICE` guard on the block, or the guest's configuration without the real-GPU drivers. Disabling the drivers alone does not change the list. The class question for the upstream block is #346's.
- **Where:** `package.mk:197-207`; the conf's `DRM_AMDGPU`, `DRM_RADEON`, `DRM_I915` `=y`
- **Evidence:** `02` r24, r26; P14, P20
- **Already written:** the built bzImages carry the payload; nothing on a handheld; nothing inherited by a change.
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table.

## PL-03: `bootloader/install` is the fork's file under a ROCKNIX copyright line dated before it existed, and its `qcom-abl` comment misstates why the step is skipped

- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source:** F-03 (G-9, G-18)
- **Owner area:** `projects/ROCKNIX/bootloader/install`
- **What:** Name the fork's authorship (keeping any justified prior credit), and correct `:51-58`'s reason: `rocknix-abl` does stage files under `/usr/share/bootloader/rocknix_abl`; the boot partition gets them at image time. A header and comment edit for a stream.
- **Where:** `install:2`, `:51-58`; `rocknix-abl/package.mk:13-17`
- **Evidence:** `02` r12; `git log --diff-filter=A` (`73b20caf86`)
- **Already written:** nothing on a device: a header and a comment.
- **Acceptance:** `sed -n 2p` of the file names the fork; `:51-58` describes the staging truthfully.

## PL-04: The guest's kernel configuration is a 6.15.6 file that the 7.1.2 build changes silently: the regeneration packet

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q1
- **Source:** F-04 (G-1, G-2, G-3, G-19)
- **Owner area:** `projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf`; the regeneration needs a GENERIC_X64 build root, so its owner is the coordinator's to place; T27 (#674) inherits the configuration shape (the brief's hand-on)
- **What:** Regenerate by reproducing the whole configuration preparation at 7.1.2 and commit the result under its true header. Then compare it with the saved `.image/.config`, check the fork's 10 settings, and compare an identified guest's `/proc/config.gz` after `modprobe configs` (`02` § The configuration). Provenance, not a bug: the one proof that read the file holds.
- **Where:** `linux.x86_64.conf:3`, `:126`, `:162-163`; `package.mk:146-316`
- **Evidence:** `02` § The configuration (the primary statement, the corroboration, the provenance table and transfer argument); P4, P5, P6
- **Already written:** the images built since 2026-08-21 carry the built configuration (`.image/.config`, and on the guest behind `modprobe configs`); nothing on a handheld; a regenerated file changes no built image whose input it reproduces.
- **Acceptance:** the regenerated file's line 3 reads `Linux/x86 7.1.2`, and its comparison with the built `.config` shows only the build path and toolchain lines (an open item for the image that builds it).

## PL-05: On the guest, `install`'s syslinux copy into `/usr/share/bootloader` has no runtime reader; `release` consumes it at image time

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source:** F-05 (G-11, G-20)
- **Owner area:** `projects/ROCKNIX/bootloader/install`, `release`
- **What:** Recorded: keep it until the boot chain is redesigned (T28), because removing it alone would leave `release`'s glob empty on GENERIC_X64.
- **Where:** `install:14-23`; `release:5`; `installer:198-200`, `:293-294`; `scripts/mkimage:179-180`
- **Evidence:** `02` r27, r28; P9, P10
- **Already written:** five small files in the guest's SYSTEM and release directory; nothing on a handheld.
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table.

## PL-06: Four of `install`'s seven branches are reached by no device (`grub`, `systemd-boot`, `""`, `*)`), and `grub` reads a path ROCKNIX's grub package never writes

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q6
- **Source:** F-06 (G-12, G-21)
- **Owner area:** `projects/ROCKNIX/bootloader/install` (fork-own)
- **What:** **The coordinator's decision (07:34 UTC, #658): they go.** The fork-own dead code is not under D-WORKFLOW-209's class decision. The stage-E stream S1 replaces the four with one refusal naming an unknown `BOOTLOADER`, in the same commit as PL-14's fix. `""` is unreachable by construction (`scripts/image:272`). If reached, `grub` would warn and report success, and the grub package's own staging would stay.
- **Where:** `install:25-43`, `:63-77`; `projects/ROCKNIX/packages/tools/grub/package.mk:77-84`
- **Evidence:** `02` r11, r13; P8
- **Already written:** nothing: unreached code writes nothing.
- **Acceptance:** the coordinator's decision recorded (a removal is a stream).

## PL-07: The macOS/UTM route and its ssh + `rclone config` steps: is it still a supported developer path after D-QA-053 and D-CLOUD-175?

- **Severity:** Low
- **Category:** Documentation
- **Question:** Q7
- **Source:** F-07 (G-22)
- **Owner area:** `projects/ROCKNIX/devices/GENERIC_X64/vm/README.md`, `utm-bundle-readme.txt`, the launcher's `utm`
- **What:** A support decision for the coordinator, not dead code. The route is packaged and tested in a fixture (`last-good-scripts-test:3561-3571`), and `095-cloud-ssh` still prints the loopback command (D-QA-054).
- **Where:** `utm-bundle-readme.txt:9-23`; `README.md:4`, `:66-138`
- **Evidence:** `04` § Q6, § Q7
- **Already written:** nothing on a device: text.
- **Acceptance:** the coordinator's decision recorded.

## PL-08: `tools/renovation-inventory` reads `bootloader/rkhelper` and six overlay sources as reached by shipped devices that never read or compile them

- **Severity:** Low
- **Category:** Bug
- **Question:** Q6
- **Source:** F-08 (G-23)
- **Owner area:** `tools/renovation-inventory`'s reach (T10's set, beside #1049 and #1056)
- **What:** The opposite direction to #1049 and #1056: files read through `find_file_path` from a recipe, or compiled from a `${DEVICE}` directory, are reached only by the devices that build that recipe or name that directory. Whether this is a `bug` (as #1056 was) is the coordinator's call.
- **Where:** the inventory rows at `2174265e9c`; `device-tree-overlays/package.mk:13`, `:20`; r14
- **Evidence:** `02` r14; P11
- **Already written:** `inventory.json` at `2174265e9c` marks them `shipped`; the fixed tool regenerates it.
- **Acceptance:** a constructed tree with a `find_file_path`-read file used by one device's recipe reads reached only by that device (shipped by all today).
- **Bug issue:** #1086

## PL-09: A merge of `next` must keep GENERIC_X64 in the override's version case: upstream's case has none and no default, and the override sources no generic recipe

- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source:** F-09 (G-24)
- **Owner area:** T25 (#672) and T28 (#675); the merge of `next`
- **What:** Recorded for the merge: taking upstream's case leaves GENERIC_X64 with no `PKG_VERSION`, checksum or URL, a broken build. The SM bls/dtb rewrite of `bootloader/mkimage` and `config.xml` comes with it.
- **Where:** `packages/linux/package.mk:1-20`, `:36`; `651150fc88:...:42`, `:53`
- **Evidence:** `02` r09; P16
- **Already written:** nothing: a merge hazard.
- **Acceptance:** a design: recorded with its sentence in the Phase 7 table, and carried into T25's and T28's briefs.

## PL-10: `options` does not say why `syslinux`, and the configuration says nowhere where it came from

- **Severity:** Low
- **Category:** Documentation
- **Question:** Q7
- **Source:** F-10 (G-25)
- **Owner area:** `projects/ROCKNIX/devices/GENERIC_X64/options`; the configuration
- **What:** A comment beside `BOOTLOADER="syslinux"` (the profile boots UEFI; `mkimage` writes syslinux's EFI loader); the regenerated configuration (PL-04) carries its own provenance. Ancestry from the Generic conf is not claimed (G-25).
- **Where:** `options:26-27`; `scripts/mkimage:179-180`; `73b20caf86`
- **Evidence:** `04` § Q7
- **Already written:** nothing on a device: comments.
- **Acceptance:** `options` names the reason beside the line; the regenerated configuration's provenance comment exists.

## PL-11: The bfq udev rule writes a scheduler on partitions, fixed upstream; the modeswitch `eject` fires on non-block children

- **Severity:** Low
- **Category:** Bug
- **Question:** Q3
- **Source:** F-11 (G-35, G-36)
- **Owner area:** `projects/ROCKNIX/packages/linux/udev.d/` (upstream-carried)
- **What:** The bfq half comes with the next merge (`651150fc88`'s `SUBSYSTEM=="block", ENV{DEVTYPE}=="disk"`), for T25. The modeswitch half is upstream's and unfixed; no device of ours is known to carry the dongle.
- **Where:** `10-bfq-sched.rules:1`; `40-usb_modeswitch.rules` (the `0cf3:20ff` line)
- **Evidence:** `04` § Second opinion G-35, G-36; r09 (upstream modified the bfq rule)
- **Already written:** nothing persistent: udev writes attributes at runtime; a fixed rule needs no migration.
- **Acceptance:** after the merge, `git show HEAD:projects/ROCKNIX/packages/linux/udev.d/10-bfq-sched.rules` carries the disk-only match.
- **Bug issue:** #1087

## PL-12: `dtb_overlay` reports success over a failed boot-file update, cannot clear a specialization with no installed overlay, and leaves `$3` unquoted

- **Severity:** Low
- **Category:** Bug
- **Question:** Q3
- **Source:** F-12 (G-33, G-34)
- **Owner area:** `projects/ROCKNIX/packages/kernel-drivers/device-tree-overlays/sources/dtb_overlay` (upstream-carried; installed on H700)
- **What:** Upstream-carried and outside the fork's lanes (D-UI-079), but a contained fix (`bugs-are-agent-first.md` rule 6): check the remount and `sed`, accept `None` before the loop, and quote `$3`. Bug or Backlog is the coordinator's call. A host fixture with a fake `/flash` and `get_setting`/`set_setting` shims can verify it.
- **Where:** `dtb_overlay:84-103`, `:132-156`
- **Evidence:** `02` § Stage C re-reads; `04` § Second opinion
- **Already written:** a device where the update failed carries the setting without the boot line; the fix re-writes the line on the next `set`.
- **Acceptance:** under a fixture whose remount fails, `dtb_overlay set <spec> <overlay>` exits non-zero (0 today), and `set <spec> None` with no installed overlay exits 0 (1 today).
- **Bug issue:** #1088

## PL-13: The launcher follows a symlink at its PID-file path (default `/tmp/rocknix-qemu.pid`), and its stale-socket clearing is not atomic

- **Severity:** Low
- **Category:** Bug
- **Question:** Q3
- **Source:** F-13 (G-31, G-32)
- **Owner area:** `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm` (fork-own)
- **What:** Treat the PID file as the sockets are treated: refuse a symlink or an existing non-PID file, refuse identical monitor and serial paths, and serialise the check and the unlink. A stream or Backlog for the coordinator.
- **Where:** `generic-x64-vm:142-154`, `:205-217`, `:298`, `:705`
- **Evidence:** `02` § Stage C re-reads
- **Already written:** nothing on a device; a QA host's PID files, rewritten every start.
- **Acceptance:** with a symlink at the PID-file path, `generic-x64-vm run --headless ... --pidfile <link>` refuses before QEMU starts (`qemu-args` prints the resolved path today).
- **Bug issue:** #1089

## PL-14: `install` and `release` mask a failure: a missing syslinux source warns then reports *completed*, and `release`'s `cp` is unchecked by a caller without `set -e`

- **Severity:** Low
- **Category:** Bug
- **Question:** Q3
- **Source:** F-14 (G-27, G-10)
- **Owner area:** `projects/ROCKNIX/bootloader/install`, `release`; `scripts/image:272-289`
- **What:** Fail the step when its files are missing or its copy fails, as T5's E1 (`cfd5ee7324`, #827) did for the `mkimage` copies. A stream for the coordinator, beside #827.
- **Where:** `install:16-22`, `:80`; `release:4-5`
- **Evidence:** `04` § Second opinion G-27
- **Already written:** nothing: an image built over a failure would show it in the build log; no device state.
- **Acceptance:** a fixture with no `/usr/share/syslinux` makes the image step exit non-zero (0 today).
- **Bug issue:** #1090

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Medium
  category: Renovation
  question: Q5
  source_finding: "F-01"
  owner_area: "`projects/ROCKNIX/devices/GENERIC_X64/` (a new `config/kernel-firmware.dat`); `kernel-firmware`'s stamp (T5's E6)"
  tracked: "#1083"
  outcome: "deferred"
- id: PL-02
  severity: Low
  category: Renovation
  question: Q5
  source_finding: "F-02"
  owner_area: "`projects/ROCKNIX/packages/linux/package.mk:197-207`; the guest's configuration"
  tracked: "`b501bdad67`"
  outcome: "resolved"
- id: PL-03
  severity: Low
  category: Standards
  question: Q2
  source_finding: "F-03"
  owner_area: "`projects/ROCKNIX/bootloader/install`"
  tracked: "`f56cbd1c69`"
  outcome: "resolved"
- id: PL-04
  severity: Low
  category: Renovation
  question: Q1
  source_finding: "F-04"
  owner_area: "`projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf`; a GENERIC_X64 build root (the coordinator places it); T27 (#674) inherits the shape"
  tracked: "#1084"
  outcome: "deferred"
- id: PL-05
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-05"
  owner_area: "`projects/ROCKNIX/bootloader/install`, `release`"
  tracked: "`b501bdad67`"
  outcome: "resolved"
- id: PL-06
  severity: Low
  category: Renovation
  question: Q6
  source_finding: "F-06"
  owner_area: "`projects/ROCKNIX/bootloader/install`"
  tracked: "`6e63150105`"
  outcome: "resolved"
- id: PL-07
  severity: Low
  category: Documentation
  question: Q7
  source_finding: "F-07"
  owner_area: "`projects/ROCKNIX/devices/GENERIC_X64/vm/` README, UTM text, `utm`"
  tracked: "#1085"
  outcome: "deferred"
- id: PL-08
  severity: Low
  category: Bug
  question: Q6
  source_finding: "F-08"
  owner_area: "`tools/renovation-inventory`'s reach"
  tracked: "#1086"
  outcome: "deferred"
- id: PL-09
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "F-09"
  owner_area: "T25 (#672), T28 (#675); the merge of `next`"
  tracked: "`b501bdad67`"
  outcome: "resolved"
- id: PL-10
  severity: Low
  category: Documentation
  question: Q7
  source_finding: "F-10"
  owner_area: "`projects/ROCKNIX/devices/GENERIC_X64/options`; the configuration"
  tracked: "`22c227d41c`"
  outcome: "resolved"
- id: PL-11
  severity: Low
  category: Bug
  question: Q3
  source_finding: "F-11"
  owner_area: "`projects/ROCKNIX/packages/linux/udev.d/`"
  tracked: "#1087"
  outcome: "deferred"
- id: PL-12
  severity: Low
  category: Bug
  question: Q3
  source_finding: "F-12"
  owner_area: "`device-tree-overlays/sources/dtb_overlay`"
  tracked: "#1088"
  outcome: "deferred"
- id: PL-13
  severity: Low
  category: Bug
  question: Q3
  source_finding: "F-13"
  owner_area: "`projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm`"
  tracked: "#1089"
  outcome: "deferred"
- id: PL-14
  severity: Low
  category: Bug
  question: Q3
  source_finding: "F-14"
  owner_area: "`projects/ROCKNIX/bootloader/install`, `release`; `scripts/image`"
  tracked: "#1090"
  outcome: "deferred"
```

## Phase 7 resolution gate

The coordinator's dispositions, 07:34 UTC on #658.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | **Deferred** | #1083, a Backlog the coordinator filed: the guest's `kernel-firmware.dat`, written once T5's E6 is on `next`; its proof needs a build |
| PL-02 | **Resolved** | recorded at `b501bdad67` (`02` F-02, `04` § Q5): the upstream x86 block and the Generic conf's built-in drivers are inputs to #1084's regeneration |
| PL-03 | **Resolved** | `f56cbd1c69` (stream S1): `install`'s line 2 now reads `# Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)`, and the `qcom-abl\|arm-efi` comment says what stages the loaders (`02` § The streams' positives) |
| PL-04 | **Deferred** | #1084, a Backlog the coordinator filed: the regeneration packet, from a build root; T27 (#674) inherits the configuration shape |
| PL-05 | **Resolved** | recorded at `b501bdad67` (`02` F-05, `04` § Q6); the coordinator carries it into T28's brief (#675) |
| PL-06 | **Resolved** | `6e63150105` (stream S1): the four branches replaced by one refusal; `grub` refused (rc 1, the value named), the 15 devices' values kept (`bootloaders.sh`), the kept branches still completing (`kept-loaders.sh`) |
| PL-07 | **Deferred** | #1085, a Backlog the coordinator filed: the README's `rclone config` steps are documentation drift against the native wizard (as #42 for the site); D-QA-053 and D-QA-054 already settle the guest's purpose |
| PL-08 | **Deferred** | bug #1086, filed by the lane (box-check 0 fail); the fix is T10's set (#657), beside #1049 and #1056 |
| PL-09 | **Resolved** | recorded at `b501bdad67` (`02` F-09); the coordinator carries it into T25's brief (#672) and the merge notes |
| PL-10 | **Resolved** | `22c227d41c` (stream S3): `options:26` reads `# syslinux: scripts/mkimage writes its BIOS and UEFI loaders, and vm/profile.json boots UEFI`; the configuration's provenance line waits for #1084's regeneration, which rewrites that file |
| PL-11 | **Deferred** | bug #1087 (the modeswitch half), filed by the lane (box-check 0 fail); fixed in stream S3 at `5934e9616c`, its block-child firing open (no USB block device on the host); the bfq half is settled by the next base merge (`651150fc88` carries the fix) |
| PL-12 | **Deferred** | bug #1088, filed by the lane (box-check 0 fail), stream S4 |
| PL-13 | **Deferred** | bug #1089, filed by the lane (box-check 0 fail); fixed in stream S2 at `594acf48bc`, positives in `02` § The streams' positives; the bug stays open until the fix reaches `next` |
| PL-14 | **Deferred** | bug #1090, filed by the lane (box-check 0 fail); fixed in stream S1 at `7b8608e7a3`, positives in `02` § The streams' positives; the bug stays open until the fix reaches `next` |
