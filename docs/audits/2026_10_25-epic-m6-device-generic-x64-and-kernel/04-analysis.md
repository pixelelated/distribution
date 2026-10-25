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
3. **The built-versus-committed gap.** **Stated from the recipe (primary):** the recipe copies the 6.15.6 file and forces four values, then runs `listnewconfig` (`:306`) and `yes "" | kernel_make oldconfig` (`:315`) at 7.1.2. So every symbol 7.1 added takes its default unseen, every dropped one vanishes, and the forced values override the file. **Corroborated** on an M7 root's built file (provenance and transfer argument in `02` § The configuration; accepted by the coordinator, 07:10 UTC):
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
- **Three facts rest on another lane's build roots:** the built configuration, the firmware tree and the bzImage's size. The coordinator accepted them as evidence at 07:10 UTC, with the recipe-only statement primary. Their provenance is in `02` § The configuration: both roots' identity and head, each read's time, each copy's sha256, and the transfer argument with its `git diff`. Nothing was written there.
- **Three line ranges were wrong in the first draft of `02`** and were corrected before commit: `:197-207`, `scripts/image:272-289`, and the shipped `init:432`.
- **Q5's first draft said the configuration adds the four GPU drivers.** The option diff showed they are the Generic conf's (inherited, `=y` in both), and that the Generic file's 7.1.2 header makes part of the 659 / 351 version drift; corrected before commit.
- **What would change the verdicts:**
  - a built `.config` from a different input: the M7 head's conf differing;
  - a GENERIC_X64 firmware list somewhere `find_file_path` searches;
  - a device on `grub` or `systemd-boot`;
  - a proof that read the committed configuration and was wrong. One was looked for (`git grep` in `docs`, `.claude`, `tools`, the device) and the one found holds.
