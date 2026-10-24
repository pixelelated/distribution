# Mini Retro: M6.P2 T8, the image's own packages (#655)

**Completed:** 2026-10-24
**Scope of this retro:** the T8 lane, covering:
- the slice's 485 paths (260 recipes and 225 scripts, units and configs under `projects/ROCKNIX/packages`), read at `8ebaf8daad`;
- the Independent-depth currency audit, stages A to D (`docs/audits/2026_10_24-epic-m6-image-packages/`, #895, now nineteen items), with one GPT-6 Astra seat;
- the four fix streams of the coordinator's `t8-streams.md`: S1 #852, S2 #893, S3 #894 with #899 found on its guest, and S4 #901 with S3's addendum;
- verification.

Not retro'd here, because they are not this lane's:
- #890's packet (the T1 session's);
- the #585, #657 and #844 posts and the Backlogs #896 and #897 (the coordinator's);
- the merge to `next`.

**Commits:** `reviewed-at` `caf1de3727`; `fixed-at` `b58489297c` (S4's, the last fix). From 12:09 to the hand-back, about two and a half hours.

## What the slice did to the two time-to-play numbers

**Nothing measurable, and nothing on either path.** Interface to a game's first frame and game to game are untouched.
- **S1** moves where `virtual/image` makes `/opt -> /storage/.opt` (at install, not at recipe load). The image's link is the same.
- **S2** builds `mangohud`'s three subprojects from checksummed source recipes instead of `curl`. They are the same bytes its wraps name, so the binary is unchanged in intent; no build ran to compare.
- **S3, the addendum and S4** change the GENERIC_X64 installer, which runs only from installation media.
- **S4 changes an installed disk's kernel command line,** from the media's (`portable quiet console=…`) to the generated one (`quiet console=…`). `portable` only keeps `DEFAULT run` in `syslinux.cfg` (`busybox/scripts/init:1245-1246`, `:777-785`), so nothing on the launch path moves. Boot to the carousel was not timed.

## What worked well

- **Simulating the base merge with `git merge-tree --write-tree`** gave the conflict list as data (9 of this slice's paths, `02` § The conflict set), without touching a branch.
- **One bounded packet for the seat** (398,152 bytes, one probe and one refutation; the refutation call cost 3.91 USD and ran 920 s).
  - It brought five findings the lane's read had not graded: G-01 the installer, G-15 `mangohud`'s `curl`, G-20, G-22 and G-27, the third `spirv` file.
  - It was refuted once (G-07), and its G-05 turned into #901 when the guest read the bytes.
- **The coordinator's fix-first order in S3.** #899 was fixed before #894's runs, so both bugs rest on a real input (no pad, the guard) rather than on stubs. The only stubs left are #899's failing control and its third criterion's fixture.
- **Failing controls without stubs.**
  - #894: the #899-only file on the same 8 MB disk.
  - #901: S3's own installed disk.
  - In both cases a control from the fix's own predecessor was cheaper and more honest than a synthetic one.
- **SSH beside the serial console.** The serial console carried the dialogs; SSH carried every read, process count and stop by PID.
- **Booting the installed disk itself.** Through a qcow2 overlay grown to the launcher's 16 GiB floor, the raw disks stayed evidence.
  - It settled that syslinux's EFI loader reads the root `/syslinux.cfg` (the control's `/proc/cmdline`).
  - It settled that the image's `ldlinux.e64` boots beside the toolchain's `bootx64.efi`. A file read alone could not have shown either.
- **Reading installed bytes with `7z`** from the raw target confirmed G-05 without a second boot.

## What was harder than expected

- **The guest powered itself off,** three minutes into S3's first run: #899's background copies of the installer. Neither the lane's read nor the seat's had seen it, although the seat's G-06 sits on the same lines. Three monitor resets followed, one of them only because whiptail holds the console raw, so Ctrl-\ is a key. Two friction lines.
- **The brief's bench assumed things the script refutes:**
  - a virtio target never reaches the menu (`get_device_unmount` lists only `sd`, `mmcblk` and `nvme`);
  - a 2 GB target cannot pass (`PARTSIZE_SYSTEM="4096"`).
  - Both were found at the bench, not at the brief.
- **Measurement traps, each of which read as a result before it was understood:**
  - the driver's first screen mark was taken after the output it waited for, which looked like an installer failure;
  - busybox `ps -o comm` does not show a script's name, which gave a count of 0;
  - a renamed copy (`installer-899`) missed an exact-name count, which gave 0 again;
  - a pipeline subshell keeps the script's name, which gave a second "installer" during the gauge.
- **S4's reorder was not a pure reorder.** It exposed a dead `@EXTRA_CMDLINE@` substitution (the recipe's `sed` and the script's `${EXTRA_CMDLINE}` came apart in upstream's `09810c3ece`). Without a second token, every installed disk would have lost `quiet` and its serial console. The boot test found it; the brief's file-only proof would not have.
- **The lane's own slips:**
  - the host-file line at 13:40 went through an unquoted heredoc (variables only, no command substitution, but against the brief);
  - a #895 comment claimed parity with T7's #884 without checking, and was edited out within a minute;
  - two line numbers in the running log and two in 02 were one off and were corrected before commit;
  - #899's second criterion was narrowed to the fix at verification, which the coordinator reversed: a criterion is edited at authoring, not refined to the fix.

## What we discovered

- **#899:** the installer started copies of itself without end on any machine without a game controller.
  - The sibling hunt found seven launch scripts with the same unguarded `$GPTOKEYB "<name>" -c … &` (melonDS, drastic, flycast, SkyEmu, azahar twice, fexconfig), filed as **#902**: read, not run, outside T8's files.
- **#901, with S4:**
  - the installed disk carried the media's `syslinux.cfg`;
  - the media's `ldlinux.e64` is the toolchain's build and differs from the image's;
  - the recipe's `@EXTRA_CMDLINE@` substitution matches nothing.
- **The unfixed installer reported Install Complete after copying 2.0 G into `/tmp`** (RAM) when its mount failed.
- **The leads:** G-02, G-04 and G-06 are #585 rows. G-04 can be run on the VM with QEMU's `nvme` at `logical_block_size=4096`, since the installer lists `/dev/nvme*`.

## Adjustments for the next lane (proposals for the coordinator, D-WORKFLOW-189)

- **Run a fork script once on the VM at stage B when it can run there,** not only read it. #899 hid from two readers on the same lines and showed itself in a minute. The brief's evidence floor could name "a VM-runnable script in scope is run once".
- **Before a TUI owns a guest's serial console, provision the QA key and keep SSH for reads and stops,** and stop the TUI by PID. A rule edit for `generic-x64-vm-testing.md` (the second friction line); the procedure is `tools/t8-installer-drive.py`.
- **A bench in a brief is read against the script first:** its device filter and its sizes.
- **A fix whose proof is a file also boots, where the file is a boot input.** S4's file-only criterion would have passed a change that dropped `quiet` and the serial console.
- **Count processes by `/proc/*/comm` with a prefix, and expect a pipeline's subshell** under the parent's name.

## Scoped audit (the close-out's own checks)

- `tools/lint-audit-artifacts docs/audits/2026_10_24-epic-m6-image-packages`: `PASS` at stage F's second pass, nineteen items.
- `PROOF:` lines 21, `proved:` cells 21.
- The coverage table has 485 rows; `q4-table.md` has 260.
- `tools/box-check`: 0 fail on #895, #894, #899, #852 and #893 at 14:15, and on #895's nineteen at 14:37.
- `git diff --stat 8ebaf8daad b58489297c -- projects packages`: six files (S1's one, S2's four, the installer), 136 insertions and 37 deletions. In modified files no `PKG_VERSION` or `PKG_SHA256` line changed; nothing was deleted or renamed.
- The checkers' exit codes: in the stage-H hand-back on #655.
