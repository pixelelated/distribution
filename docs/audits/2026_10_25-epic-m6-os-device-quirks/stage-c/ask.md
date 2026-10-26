# Second opinion (Phase 4.6), M6 T29: the per-handheld quirks of pixelelated/distribution

You are the one independent reviewer for a read-only currency audit, under a brittleness lens, of the 333 files under `projects/ROCKNIX/packages/hardware/quirks/devices/` at commit `8ebaf8daad`: 88 entries (65 model directories, 23 alias symlinks), 328 upstream's and 5 the fork's.

- **What ships.** The shipped images are an H700 image (two owned units: `Anbernic RG35XX SP`, `Anbernic RG-SP`) and an SM8550 image (one owned unit, the Retroid Pocket Nova). A QEMU guest is the test image.
- **What you get.** The first reader is another lab's model. Its `02-forward-audit.md` (the 333-row coverage table trimmed to a note), `03-retrospective.md` and `04-analysis.md` are included below, followed by the context sections and the files, line-numbered.
- **Masking.** Every file was passed through a masking `sed` that replaces a value after `key=`, `token=`, `user=`, `pass...=` or `psk=` with `***`.
- **Your job is to refute, narrow or confirm, against the code: not to agree.** Cite `file:line` for every claim, and say plainly where the first reader is wrong.
- **No one can run anything on a handheld.** A fact only a unit can show is a device-facts row, quoted in the context, and is otherwise an open item to test.

Answer these first, in this order:

1. **The selection (`02` § The selection, § The entries, F-02).**
   - Is `QUIRK_DEVICE`'s derivation and the run rule read right (`002-autostart:6-12`, `autostart:31-43`, the wrappers' `exec ... $*`)?
   - Is it right that the two owned H700 units select no device entry, and that nothing they need sits in one (`platforms/H700/*` against the RG40XX H, RG40XX V and CubeXX entries)?
   - Is the board count (28 `model` lines, 26 distinct boards, 15 with an entry) right?
2. **F-01, the candidate bug in a fork-own file.**
   - With `led.color` unset, does `Retroid Pocket Nova/bin/battery_led_status:73`'s unquoted test keep the loop in battery mode under bash, as the fixture shows?
   - Does `batteryledstatus.service` start it at every boot?
   - Is "nothing seeds `led.color`" right?
   - Is quoting the variable the contained fix, and what else would the fix change?
3. **The fork-own five (`02` § The fork-own five).** Read each whole: the VM's `001-device_config` and `091-retired-vm-fixes`, and the Nova's `ledcontrol`, `analog_sticks_ledcontrol` and `battery_led_status`. Any defect the first reader missed? Pay particular attention to `091`'s take-back: can it remove a file a person wrote?
4. **Tier B's brittleness (F-03 to F-07).**
   - Are the every-boot `sed -i` rewrites of `retroarch.cfg`, the unset-colour shapes, the two `led.brightness` dialects and the unguarded device writes read right?
   - Is anything in tier B a defect on a board the shipped images boot, beyond what is named?
5. **Currency (F-08, F-09).** The 18 pending commits and the two panel-calibration files, and the two `QUIRK_DEVICE` derivations.

Then:

6. **Refute or confirm each finding F-01 to F-10** in `02` § Findings: *confirmed*, *narrowed* (say how), or *refuted* (with the line).
7. **What the first reader missed:** a defect in tier B or the fork-own five, a selection case it did not consider, or a disposition that should be different.

**Output:** numbered items `G-1`, `G-2`, ..., each with one line saying *confirmed / narrowed / refuted / new*, the `file:line` evidence, and two to five sentences. Group them under the seven headings above. Do not restate the packet, and do not reproduce long code. Keep the whole reply under about 8,000 words.
