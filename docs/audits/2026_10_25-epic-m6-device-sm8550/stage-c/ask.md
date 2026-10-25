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
