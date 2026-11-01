# T11's remediation streams (#658, audit issue #1091)

Written by the coordinator on 2026-10-25 at T11's stage-D pause
(D-WORKFLOW-189), in the shape of `t13-streams.md`: four streams, each
with the files it owns, the test first, its `Already written:` line, its
acceptance and its commits; then the dispositions that are not streams;
then the order and the hand-back. The lane executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-device-generic-x64-658`,
branch `feature/m6-device-generic-x64-658`, stage-D tip `499628a049`).
**Review depth per stream: Local** (plan § 6c; the Independent seat sat at
stage C and does not sit again). Every file here is a script or a
configuration without a test of its own, so **a stream lands with a case
whose constructed input fails on the unfixed file and passes on the fixed
one, or it is not a stream** -- the positive run on the host against a
copy of the file at `499628a049` (from a clone or `git worktree add
--detach`, never `git archive`), quoted in `02` § The streams' positives
with the command, the exit and the line, and **the construction kept on
the branch** under the audit folder's `stage-e/` (one driver or fixture
script per positive, taking the file under test as its first argument,
writing only under `$TMPDIR`, printing one verdict line last; a README
table of the positives), as T13's `stage-e/` does, so the acceptance
re-run reproduces each from the branch. `TMPDIR` under
`/workspace/tmp/m6-t11/`.

**Nothing here boots a guest** (the launcher's positives stop before
QEMU: `qemu-args`, a refusal, a function called in isolation), runs a
build, a plan generation, a fetch, `tools/council/run invoke`, anything on
a handheld, an edit to any file but the four named below, to a rule, a
decided register row or `CLAUDE.md`, or a write under
`/workspace/repos/rocknix*` or `/tmp`. A fixture that must look like a
credential is assembled at run time. `rm -rf` only as `"${X:?}"/...` or a
literal path, in its own short command.

**The lane's question, answered first.** Yes: S1's acceptance includes
the `git grep` over every `projects/ROCKNIX/devices/*/options` for
`BOOTLOADER=`, run at the stream's tip and quoted, proving that every
device's value is one of the three kept branches -- r13 at `8ebaf8daad`
stands as stage A's record, and the stream proves it again as its own
guard, because the refusal is a behaviour change for any value outside
the three. The refusal's positive is a constructed `BOOTLOADER=grub`:
`install` copies and reports *completed* on the unfixed file, refuses with
exit non-zero naming the value on the fixed one.

## S1. `bootloader/install` and `bootloader/release`: a failure is a failure, an unknown loader is a refusal, the header tells the truth (#1090, PL-06, PL-03)

- **Why first:** the two Highs of the slice's own files are here (a
  masked failure in the image step; dead branches that would copy
  nothing and report success), and the header is a line in the same file.
- **Files owned:** `projects/ROCKNIX/bootloader/install` (the fork's own:
  `:2` the header, `:16-22` the syslinux copy, `:51-58` the qcom-abl
  comment, `:80` the completion line, the `grub`, `systemd-boot`, `""` and
  `*)` branches) and `projects/ROCKNIX/bootloader/release` (`:4-5`, the
  unchecked `cp`; upstream's file, a contained fix said in the commit).
- **The shape.** #1090: a missing syslinux source is an error (exit
  non-zero, the path named), never a warning followed by *completed*;
  `release`'s copy is checked (`cp ... || exit`) in a caller that runs
  without `set -e`. PL-06: the four unreached branches go -- `install`
  keeps `syslinux`, `u-boot` and `qcom-abl|arm-efi` (the design: the
  image step writes the u-boot and qcom loaders, `:51-58`) and refuses any
  other `BOOTLOADER` with exit non-zero naming it; the `grub` branch's
  path, which ROCKNIX's grub package never writes, goes with it. PL-03:
  the header names the fork and the year it was written; `:51-58` says
  truthfully why the step is skipped for u-boot and qcom-abl.
- **The test first** (`stage-e/s1/`): `install` run directly with a
  fixture environment (`INSTALL`/`BOOTLOADER`/the source paths the script
  reads, as `scripts/image:280` sets them -- read them there): (a)
  `BOOTLOADER=syslinux` with no syslinux source -- rc 0 and *completed*
  on the unfixed file, rc non-zero naming the path on the fixed; (b)
  `BOOTLOADER=grub` -- a copy attempt and *completed* on the unfixed,
  the refusal on the fixed; (c) `release` with a destination that cannot
  be written -- rc 0 on the unfixed, non-zero on the fixed; (d) the
  `git grep` over every device's `options` for `BOOTLOADER=`, quoted,
  every value in the kept three. Each quoted in `02` § The streams'
  positives.
- **Already written:** nothing on a device; an image built over a masked
  failure would have shown it in its build log; no device state reads
  these scripts.
- **Acceptance:** #1090's three checkboxes from (a) and (c); PL-06's row
  *resolved* at the commit with (b) and (d) quoted; PL-03's row *resolved*
  with `sed -n 2p` and `:51-58` quoted; `fixed-at` set.
- **Commits**, in this order: `bootloader: install and release fail
  closed on a missing source or a failed copy (#1090)`; `bootloader:
  install refuses an unknown BOOTLOADER instead of four dead branches
  (#658)`; `bootloader: install's header names the fork; the qcom-abl
  comment says why the step is skipped (#658)` -- each `Refs #1090, #658`
  or `Refs #658`, the attribution line.

## S2. The launcher: the PID-file path is not followed through a symlink, the stale socket is cleared atomically, the monitor and serial paths differ (#1089)

- **Files owned:** `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm`
  (`:142-154`, `:205-217`, `:298`, `:705`).
- **The shape.** A PID-file path that is a symlink is refused before QEMU
  starts (the default `/tmp/rocknix-qemu.pid` included); the stale-socket
  check and removal are one step that cannot race a live owner (check the
  owner by its pid, remove only what the check named); the monitor and
  serial socket paths are distinct by construction.
- **The test first** (`stage-e/s2/`): the fixture plants a symlink at the
  PID-file path and runs `generic-x64-vm qemu-args ... --pidfile <link>`
  (no QEMU) -- the resolved path printed on the unfixed file, the refusal
  on the fixed; the stale-socket function called in isolation (imported
  from the file, or the script run to the point before launch) over a
  socket a live fixture process owns -- removed on the unfixed, left on the
  fixed; the two paths compared from `qemu-args`'s output -- equal on the
  unfixed, distinct on the fixed. **No guest boots**: every case ends
  before QEMU, and `pgrep -x qemu-system-x86` is read before and after.
- **Already written:** nothing on a device; a QA host's PID files are
  rewritten at every start; T12's harness (`tools/vm-pair`) passes its
  own `--pidfile` and is read, not changed.
- **Acceptance:** #1089's two checkboxes from the cases; `tools/vm-pair`'s
  call line still matches the launcher's flags (`grep -n VM_TOOL tools/vm-pair`
  quoted); `fixed-at` set.
- **Commits:** `generic-x64-vm: refuse a symlinked PID-file path, clear a
  stale socket atomically, keep the monitor and serial paths apart (#1089)`
  -- `Refs #1089, #658`.

## S3. The udev rule and `options`: the modeswitch eject fires only on a block device; `options` says why syslinux (#1087, PL-10)

- **Files owned:** `projects/ROCKNIX/packages/linux/udev.d/40-usb_modeswitch.rules`
  (line 7, the `0cf3:20ff` match; upstream's file, a contained fix said
  in the commit) and `projects/ROCKNIX/devices/GENERIC_X64/options` (one
  comment line).
- **The shape.** The `eject` runs only for a block device (the match
  gains `SUBSYSTEM=="block"`, or the key the rule's own neighbours use);
  the bfq half is settled by the next base merge and is not touched.
  `options` carries one comment line above `BOOTLOADER="syslinux"`
  saying why (a BIOS guest; the image step's `install` copies it).
- **The test first** (`stage-e/s3/`): the positive the bug's VM line
  names -- `udevadm test` over a synthetic non-block child if the host's
  udev takes a rules-directory override (name the mechanism and the
  version), else the rule's effective match read back by `udevadm verify`
  plus a `grep` of the key on line 7 -- fires on the unfixed rule, not on
  the fixed; recorded with what was possible and why. The comment:
  `grep -n -B1 'BOOTLOADER=' options` quoted.
- **Already written:** nothing persistent: udev writes attributes at run
  time; a fixed rule needs no migration.
- **Acceptance:** #1087's two checkboxes; PL-10's row *resolved* with the
  comment quoted (the configuration's provenance line waits for #1084's
  regeneration, which rewrites the file); `fixed-at` set.
- **Commits:** `linux: the modeswitch eject rule matches a block device
  only (#1087)`; `GENERIC_X64: options says why syslinux (#658)`.

## S4. `dtb_overlay`: a failed boot-file update is reported, a specialization without an installed overlay can be cleared, the third argument is quoted (#1088)

- **Files owned:** the `dtb_overlay` script in T11's set (`:84-103`,
  `:132-156`; upstream's file, installed on H700, a contained fix said in
  the commit).
- **The shape.** `set` exits non-zero when the boot-file update fails
  (the remount, the write); `set <spec> None` with no installed overlay
  exits 0 and clears the setting; `$3` is quoted everywhere it is used.
- **The test first** (`stage-e/s4/`): the fixture the bug names -- a
  remount that fails (a stub `mount` on `PATH`, a read-only fixture
  directory) -- `set <spec> <overlay>` rc 0 on the unfixed file, non-zero
  on the fixed; `set <spec> None` with no installed overlay rc 1 unfixed,
  0 fixed; a spec with a space -- the unfixed splits it (the error quoted),
  the fixed does not. Nothing runs on a device: the script runs on the
  host against the fixture's paths.
- **Already written:** a device where the update failed carries the
  setting without the boot line; the fixed script re-writes the line on
  the next `set` -- read both, nothing migrated, said in the bug.
- **Acceptance:** #1088's three checkboxes; `fixed-at` set.
- **Commits:** `dtb_overlay: report a failed boot-file update, clear a
  specialization without an overlay, quote the third argument (#1088)` --
  `Refs #1088, #658`.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- #1086 (PL-08) is T10's tool (#657); the bug stays open for that lane.
- PL-01 #1083, PL-04 #1084, PL-07 #1085: Backlogs, deferred. PL-02, PL-05,
  PL-09: recorded (PL-09 in the coordinator's merge notes).
- The configuration's provenance line (PL-10's second half) waits for
  #1084; recorded.

## Order and hand-back

S1, S2, S3, S4; four files, so the streams are serial and each commit is
a working script: after each stream the file's own positives run once
more and go in `00`. Each commit cites its bug (`Refs #N, #658`, never a
closing keyword: a bug stays open until its fix reaches `next`) and
carries the attribution line; `git status --short` before every `git add
-A`; nothing under `packages/`, `projects/` or `tools/` but the four
files. After S4: the Phase 7 table and the `punch_index` at their outcomes
(`fixed` with its commit), `02` § The streams' positives, `stage-e/README.md`,
the lint on the folder (default phase), `fixed-at:` in #658's body, then
stages F to H as the brief has them (the re-verification, the retro
posted on #658, the hand-back naming the tip and each artifact by path).
The coordinator accepts by `AUDIT_ISSUE=1091 BUGS="1086 1087 1088 1089 1090"
DISPATCH_TIP=2103f0271d $S/t11-accept.sh <tip> <coordinator tip>` on a
clone of the lane's branch, extended with `stage-e/README.md`'s rows re-run
against the unfixed clone at `499628a049` and the fixed tree, reads every
stream's diff, ticks #658, #1091 and the bugs' host checkboxes from the
artifacts, closes #1091 when its checkboxes read back ticked by name, and
merges the branch in its turn (after T40's, before T9's).
