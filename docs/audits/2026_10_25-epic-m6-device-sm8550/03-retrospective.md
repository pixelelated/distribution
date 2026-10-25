# Retrospective audit — M6.P2 T28, the SM8550 device (Retroid Pocket Nova) (#675)

Phase 3 over a currency slice. The 29 are upstream's, untouched by the fork since the base, and shipped on the Nova. The question is how current they are, and what meets them at the seams.

## 3.1 Architectural coherence

- **The directory is half the picture.** It holds the Nova's options, its updater, its firmware list and its trees, but none of the recipes that pin what boots it. `qcom-abl`, `rocknix-abl`, `mkbootimg`, the kernel, `extra-firmware`, `kernel-firmware`, `inputplumber` and `gamepadcalibration` all live under `projects/ROCKNIX/packages/`. The boot path runs through the kernel recipe's `qcom-abl` branch, `scripts/mkimage`, `projects/ROCKNIX/bootloader/mkimage`, `distributions/ROCKNIX/config/functions` and T1's `updateabl`. That is why the Q7 answer is *no* (`02` F-05): the directory does not say how its device boots.
- **One boot image carries fourteen boards.** `config.xml`'s list becomes make targets (`functions:226-231`), and the recipe's glob appends every built dtb to one `kernel.gz` (`:392-396`). The Nova is one board among AYANEO's and AYN's, and the selection is the ABL's, declared nowhere in the tree.
- **The guard sits where the write happens.** `update.sh` calls `updateabl` unconditionally. `updateabl` refuses a foreign device, a missing ELF and missing partitions, and writes only on a checksum difference. Read together, the payload is guarded: `init:341-368` refuses an incompatible update first, and the cached ELFs are sector-aligned. **The report is not guarded.** `updateabl`'s failure is ignored by `update.sh`, and `update.sh`'s by `init`, which says *"Boot Files Updated."* (`02` F-04, Medium, after the seat's G-21). The card's `/flash/rocknix_abl/` copy is unchecked, and is read only by a person following the README.

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

As behaviour, this is the Nova's, and observed only through device facts L17 to L20, L27, L28 and L31. As record, the slice's firmware list installs files for the runtime to load, and the unit reaches an active frontend (L17, L18). That is one observation on `bc9dfe8141`, which L18 says is not a rendering proof. So F-03 records a packaging divergence, not a proven firmware path (`02` F-03, narrowed by the seat's G-13). The touchscreen's pinctrl mismatch (F-09) is likewise a source fact with no observation either way.

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
- **Design notes for T1, not defects here:**
  - both slots receive the same ELF in one run (`:72-73`), so a bad ELF reaches both, and the A/B pair gives no fallback; L19 (*Nova shutdown and bootloader recovery*) is the keep-an-eye-on that would show it;
  - the compare hashes whole sectors against the ELF's own bytes (`:44-57`), so an unaligned ELF would never match. Every cached `abl_signed-SM8550.elf` is 258,048 bytes, aligned, so this is latent (the seat's G-28, `stage-c/rereads/rereads.sh` c06).

### Interaction: T5's stamp (#836) x `config/kernel-firmware.dat`

- **The shared state:** the `kernel-firmware` package's stamp.
- **The interaction.** `find_file_path` reads this device-level file, which is outside the package's hashed directory. So an edit to SM8550's list does not rebuild `kernel-firmware` on a warm root. #836 owns it; this slice's list has not changed since the base.
