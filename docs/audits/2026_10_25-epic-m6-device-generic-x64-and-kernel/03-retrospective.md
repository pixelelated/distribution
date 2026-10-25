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
