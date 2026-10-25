# Retrospective (Phase 3) — M6.P2 T27, the H700 device (RG35XX SP, RG SP) (#674)

## 3.1 What the slice is

The maintainer's two test handhelds, as the tree describes them, in 28 paths:
- the device `options`;
- three u-boot recipes, the wrapper and one per memory type, with two defconfigs;
- an SRAM suspend stub;
- the in-place updater `update.sh`;
- two udev rules;
- a firmware list;
- 15 board trees;
- an 8,129-line kernel configuration;
- one 4,036-line patch nothing applies.

None of it is fork-own by the inventory's tier rule. The fork's own work here is six configuration lines in one commit (`cbf75c0b06`), and the device-facts rows that record the two units booting.

## 3.2 How it stays current

- **Currency comes from upstream.** Every pin is unchanged between `8ebaf8daad` and `651150fc88`. The configuration differs from upstream's copy by the fork's six lines and four upstream commits, a toolchain refresh and the RAID6 benchmark. A base merge carries all four.
- **One pin had no checksum** (atf 2.12.0). T5's E6 fixed that on its branch, and upstream fixed it differently, with a new URL. That is the slice's one merge seam (F-02).
- **The memory type is decided at update time, from the regulator's voltage,** not declared anywhere. A fresh card is activated by hand, because the image step names `/dtb.img` in `extlinux.conf` and never writes it.

## 3.3 What was hard

- **The brief's history count reproduced only at an explicit cutoff.** A bare `--since` date reads the current time of day, and a commit at 08:07 fell out of an 08:10 run. The coordinator ruled the explicit cutoff the slice's command.
- **The brief and T11's `02` read `mkimage:18-26` as H700's whole path.** The device-tree copy at `:26` is a Qualcomm branch.
- **One recipe line matches the credential read filter,** so every recipe read went through the masking `sed`.

## 3.5 The seams

**`config.xml` x the project `mkimage` x `update.sh`.**
- `config.xml` declares the SUBDEVICES (DDR3, DDR4), the trees and `fdt="dtb.img"`.
- `mkimage` writes one image per SUBDEVICE, with the loader at `seek=8`, `extlinux.conf` naming `/dtb.img`, and every tree.
- `update.sh` later writes `/dtb.img` from the running tree's dt-id, and the loader from `vdd-dram`.

The seam is a gap between the first boot and every later one. The first `/dtb.img` is a person's hand step; every later one is the updater's. #44 owns the related question of which image a unit takes.

**The kernel recipe x `kernel-firmware.dat` x the root filesystem.** The recipe builds the H700's 13 firmware files into the kernel (`package.mk:223-243`). The device's list installs the same 13 into the root filesystem. Neither knows of the other. T5's F-17 adds that the list is outside its package's stamp (#836).

**The atf recipe x T5's E6 x upstream.** Three versions of one branch: none (here), `ARM-software` with T5's checksum, and `TrustedFirmware-A` with upstream's. The merge must take one coherent pair.

## 3.6 Time to play

**Nothing, on either number.** No file changed. The loader, the trees and the configuration decide whether and how a unit boots, not how long a launch takes. The RAID6 benchmark upstream disables is boot time, which arrives with the next merge.
