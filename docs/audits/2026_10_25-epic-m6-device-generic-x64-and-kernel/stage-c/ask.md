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
