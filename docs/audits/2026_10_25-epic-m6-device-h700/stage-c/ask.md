# Second opinion (Phase 4.6), M6 T27: the H700 device of pixelelated/distribution

You are the one independent reviewer for a read-only currency audit of 28 paths at commit `8ebaf8daad`: the H700 device (`projects/ROCKNIX/devices/H700/`) the fork ships for two handhelds, an Anbernic RG35XX SP (LPDDR4) and an RG SP (LPDDR3). The first reader (another lab's model) wrote `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md`, all included below. After them come the context sections, then the files, line-numbered. Every file was passed through a masking `sed` that replaces a value after `key=`, `token=`, `user=`, `pass...=` or `psk=` with `***`; one recipe line (`h700-suspend-stub/package.mk:43`) is masked that way, so treat `***` as an unknown build flag.

The lens is currency, under cost against value. **Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong. No one can run anything on the handhelds. A fact only a board can show is a device-facts row, quoted in the context, and is otherwise an open item to test.

Answer these first, in this order:

1. **The pins and the atf seam (`02` § The pins, F-01, F-02).**
   - Are the pins the same at both hashes, as claimed?
   - Is it right that atf's H700 branch has no `PKG_SHA256` at `8ebaf8daad`?
   - Is it right that upstream's `651150fc88` sets a different checksum for both branches with a new URL?
   - Is the merge hazard real: a fetch that refuses a missing or mismatched checksum, a fork checksum computed from the old URL's archive?
   - Which combinations of URL and checksum would fail?
2. **The configuration (`02` § The configuration).** Is every one of the 25 diff lines attributed correctly? Is "upstream's file with a base" right, and the order's *fork-written* an erratum? Is anything in the fork's six lines (`cbf75c0b06`) inconsistent with the rest of the configuration?
3. **The loader and the tree (`02` § The loader and the tree, F-04, F-11).**
   - Trace a fresh card through `scripts/mkimage`, the project `bootloader/mkimage` and `config.xml`: is it right that nothing writes `/dtb.img`?
   - Trace an update through `update.sh`: is the voltage selection fail-safe, as claimed, for any other value, a missing regulator, a failed read, a non-`mmcblk` boot device, or a missing dt-id?
   - Is the first reader's correction of `mkimage:18-26` (F-11) right?
4. **The SIMD flags (F-03).** The rule's table says *crypto-neon-fp-armv8* for an aarch64 image; `options` says `+crc+fp+simd` on aarch64 and `crypto-neon-fp-armv8` on arm. Who is right, and what would settle it?

Then:

5. **Refute or confirm each finding F-01 to F-11** in `02` § Findings: *confirmed*, *narrowed* (say how), or *refuted* (with the line).
6. **What the first reader missed.** Look for:
   - a defect in `update.sh` (it runs as root on a person's handheld, writing to the boot disk);
   - in the u-boot and suspend-stub recipes;
   - in the udev rules;
   - in the trees: a dt-id that collides with another tree's or with a mainline file's, or an include that a 7.2 tree would not have;
   - any reason the firmware duplication (F-05) is not harmless.

**Output:** numbered items `G-1`, `G-2`, ..., each with one line saying *confirmed / narrowed / refuted / new*, the `file:line` evidence, and two to five sentences. Group them under the six headings above. Do not restate the packet, and do not reproduce long code. Keep the whole reply under about 8,000 words.
