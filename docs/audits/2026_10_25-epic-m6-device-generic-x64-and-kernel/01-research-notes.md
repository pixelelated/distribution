# Research notes — M6.P2 T11, the GENERIC_X64 VM device, the kernel recipe and the boot files (#658)

## Scope

- **The read hash:** `8ebaf8daad`; the 58 are byte-equal at the dispatch tip `2103f0271d`. **`reviewed-at`:** `2103f0271d`. **Upstream:** `651150fc88`, read locally.
- **The membership:** brief § 2's block, run at P1's `2174265e9c`:

  ```text
  paths 58 lines 10418
  read 14 1820 fork-own read 1421
  tier {'fork-own': 11, 'upstream-carried': 46, 'vendor-carried': 1} reach {'shipped': 49, 'test': 9}
  GENERIC_X64 fork-own lines 1217
  written 58 .qa-scratch/t11/paths.txt
  ```

  - The 58 are in `stage-a/paths.txt` and the 14 read in `stage-a/read.txt`.
  - **Erratum:** the order's *989 fork-own lines* does not reproduce. GENERIC_X64's fork-own rows sum to **1,217** over 8 paths, and no subset gives 989.
- **The configuration's two candidates** (`diff` line counts, removed / added):

  | Candidate | Lines | Its header | Removed | Added |
  | --- | ---: | --- | ---: | ---: |
  | `projects/Generic/linux/linux.x86_64.conf` | 8,062 | `Linux/x86 7.1.2` | 659 | 351 |
  | `projects/ROCKNIX/devices/AMD64/linux/linux.x86_64.conf` | 12,445 | `Linux/x86 7.1.2` | 7,671 | 2,980 |

  - Ours is 7,754 lines, with the header `Linux/x86 6.15.6`. The recipe builds `7.1.2` for GENERIC_X64 (`projects/ROCKNIX/packages/linux/package.mk:36-37`).
  - The Generic conf is the nearest. The AMD64 conf is not a base.
- **The history since 2026-06-01:** 110 non-merge commits on the 58. **40 fork-authored** across three identities (Max Engel 36, blitterbot 3, rasterabot 1); **70 upstream**.
- **The upstream delta** at `651150fc88`: **7 M** and **11 D**. The 11 are fork-only files that never existed upstream: the GENERIC_X64 device's nine, `bootloader/install` and `filesystem/etc/machine-info`.
- **A delta from the brief:** the `tools/vm-*` callers do not reach the launcher by basename. The one that runs it, `tools/vm-pair:36/74`, uses its full path through `$VM_TOOL`; the basename appears only in comments and help text (`00`).

## Phase 1

What each read file does, from its bytes at `8ebaf8daad`. The rest of the 58 are in `02` § Coverage.

| File | What it does |
| --- | --- |
| `devices/GENERIC_X64/options` | The device's knobs: `x86-64-v3` for the profile's Haswell CPU (`:15`), `BOOTLOADER="syslinux"` (`:27`), virtio and vmware GL with llvmpipe for `--gl none` (`:36`, `:83`), the Vulkan loader without a driver (`:45-46`), `quiet console=ttyS0,115200 console=tty0` (`:76`), `ROCKNIX_JOYPAD="no"` (`:79`), no swap for an 8 GiB guest (`:86`), the installer on (`:91`). |
| `devices/GENERIC_X64/vm/generic-x64-vm` | The launcher, 817 lines of Python: `profile` prints `profile.json`; `qemu-args` prints the QEMU command; `run` starts QEMU (headless with a monitor, serial and VNC socket and a PID file, or with a display); `utm` writes a macOS bundle. |
| `devices/GENERIC_X64/filesystem/usr/lib/sway/sway-generic-x64` | Starts sway with Pixman only when the one DRM card is virtio without virgl; otherwise leaves the renderer alone. |
| `devices/GENERIC_X64/filesystem/usr/lib/systemd/system/serial-debug-shell.service` | A root `/bin/sh` on ttyS0, only on a virtual machine with a serial console argument. |
| `projects/ROCKNIX/options` | Project defaults every device overrides: zstd squashfs, mesa, no display server or window manager, swap on. |
| `packages/linux/package.mk` (the override) | Picks the kernel per device (GENERIC_X64 7.1.2), copies the device configuration, forces four values, embeds firmware per arch or device, runs `listnewconfig` and a silent `oldconfig`, checks the distro's kernel options, builds, and installs the kernel, `.config`, modules and device trees. |
| `packages/linux/udev.d/*.rules` (3) | bfq on `mmcbl*`; USB host controllers' wakeup off; three modeswitch rules. |
| `kernel-drivers/device-tree-overlays/package.mk` | Compiles the device's `.dts` overlays to `.dtbo` and installs them with `dtb_overlay`. |
| `kernel-drivers/device-tree-overlays/sources/dtb_overlay` | The shell tool installed with them: lists the custom and specialized overlays, reports the current one, and writes a chosen `.dtbo` (`write_dtbo`, `:84`), refusing an unknown specialization or a missing file (`:13-14`, `:142`, `:154`). |
| `linux-drivers/rocknix-joypad/package.mk` | Builds the joypad module out of tree. |
| `linux-firmware/extra-firmware/package.mk` | Copies the device's directory of ROCKNIX's extra firmware (SM8550's for us). |
| `linux-firmware/kernel-firmware/package.mk` | Copies linux-firmware and the project's extra blobs, then installs what the device's list, or the arch's fallback, names. |
