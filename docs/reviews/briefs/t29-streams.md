# Stream brief: M6.P2 T29, stage E (#676)

**The coordinator's, 2026-10-26, at T29's stage-D pause** (the lane's comment of
05:25 UTC; #1121 the audit, #1120 the bug). Two streams, serial, in the lane's
worktree `/workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676`
on `feature/m6-os-device-quirks-676`, on top of its tip `ce2af0ca7c`. The
dispositions that are not streams are in the ruling on #676; this file is
only what changes code.

## The rules every stream keeps

- **Test first, then the fix, and the test's FAIL is recorded before the fix
  lands** (`engineering-practices.md` § Guards must fail closed: a guard with no
  observed positive is a guard with no evidence). The fixture runs on the host
  under the image's bash from M6's retained donor
  (`/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/bash`) or the
  build root's; which one is written beside every verdict.
- **The fork-own file only.** Upstream's copies of the same line (PL-04: twelve
  files, fifteen model names) are dispositions per unit (D-WORKFLOW-209) and a
  #585 line in the shape the lane writes; they do not change here.
- **Every stream answers `Already written:`** in its bug and in `02` § The
  streams (`upgrade-and-install.md`, D-WORKFLOW-050).
- **One commit per stream**, `Refs #676, #<bug>`; the paths named in the
  message; no closing keyword. `tools/pkgcheck` is not involved (no
  `package.mk` changes); `tools/register-check` before each commit.
- **Nothing runs on a unit; no guest; no build; no fetch; no keyed council
  call** (the slice's two were spent at stage C). The host is M7's under the
  04:47 handoff; these streams are reads and host fixtures.
- **`rm -rf` only as `"${VAR:?}"/...` or a literal path, in its own short
  command, never inside a `bash -c` script.**

## S1 -- #1120: the Nova's battery LED helper (F-01 and F-11)

File: `projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/battery_led_status`
(fork-own, 135 lines at `8ebaf8daad`; the fork's `a3d617ff54` added the loop).

1. **The positive, before the fix.** `docs/audits/2026_10_25-epic-m6-os-device-quirks/tools/t29-battery-unset.py --expect fixed`
   against the unfixed file exits 1 with `UNEXPECTED on fixed: unset,
   critical-recovery`, and `--expect unfixed` exits 0; both outputs into
   `stage-e/s1-before.txt`.
2. **The fix, two places in one file:**
   - `:73`: quote the test, modelled on `AYN Odin 2/bin/battery_led_status:62-63`
     (`[ "${BAT_LED_STATE}" != "battery" ]`, so an unset `led.color` breaks
     out of battery mode instead of running it);
   - the critical branch (`:85-94`): after the five-blink batch and
     `bat_led_off`, reset the cached bucket (`PREV_BATCAP`) so the next pass
     repaints when the charge returns to an earlier bucket; the smallest
     change that makes the fixture's `critical-recovery` case read `lit=yes`.
3. **The positive, after:** `--expect fixed` exits 0 on the fixed file and
   `--expect unfixed` exits 1; `bash -n` passes under the donor's bash; the
   outputs into `stage-e/s1-after.txt`.
4. **`Already written:`** nothing persisted -- the helper writes only sysfs
   and never calls `set_setting`; a Nova that booted the unfixed build holds
   no state the fix reads (the bug's line stands).
5. **Commit:** `Retroid Pocket Nova - quirks - battery_led_status: quote the
   led.color test and repaint after a critical blink (Refs #676, #1120)`.
6. **#1120's criteria** ticked from `stage-e/s1-after.txt` by the lane
   (the fixture's two exits, the `bash -n`), the trace's `fixed-at` the
   commit; the bug stays open until the fix is on `next`.

## S2 -- the VM take-back (F-12, PL-03): a `bug` the lane files first

File: `projects/ROCKNIX/packages/hardware/quirks/devices/QEMU Standard PC (Q35 + ICH9, 2009)/091-retired-vm-fixes`
(fork-own; the first pass `:61-75`).

0. **File the bug** (the lane's, D-WORKFLOW-187/189: a defect it proves),
   `bug` label, under #676: the first pass removes a file at any of the 17
   listed names before the stamp exists, whatever the file holds, and a
   dangling symlink at a listed name fails `-e` so the stamp is written with
   it still there. Severity Low (GENERIC_X64 only, a one-boot window on a
   developer's tool, D-QA-053), class `bug` (fork-own, a contained fix, a
   host-verifiable criterion; `bugs-are-agent-first.md` rule 1): the
   coordinator's ruling on #676. Criteria: the fixture's five cases below,
   each named; `Already written:` a guest that booted this build once holds
   its stamp and its first-pass removals are done, nothing to migrate;
   the VM line: yes, on the host.
1. **The positive, before.** A fixture under the audit folder's `tools/`
   (`t29-takeback.py`, the shape of `t29-battery-unset.py`) runs the script
   over a scratch root with the seat's G-12 cases: (a) unstamped edited
   content at a listed name, (b) content at each of the two known hashes,
   (c) stamped unknown content, (d) a dangling symlink at a listed name,
   (e) a missing stamp with nothing at the names. At `8ebaf8daad`: (a) is
   removed, (d) survives and the stamp is written. Recorded in
   `stage-e/s2-before.txt`.
2. **The fix, in the first pass only:** remove a listed name only when its
   content is one of the two known hashes (the check the second pass already
   makes, moved before the removal), and test the name with `-e || -L` so a
   dangling link is removed before the stamp is written. Nothing else in the
   file changes; the second pass and the stamp's format stay.
3. **The positive, after:** (a) kept, (b) removed, (c) kept, (d) removed,
   (e) the stamp written; `bash -n` under the donor's bash; `stage-e/s2-after.txt`.
4. **Commit:** `GENERIC_X64 - quirks - 091-retired-vm-fixes: remove only the
   known contents, and a dangling link, before stamping (Refs #676, #<bug>)`.

## The record

- `02` § The streams: one row per stream with the positive before, the
  commit, the positive after, the `Already written:` answer and
  `proved: fixture`; `05`'s PL-01, PL-02 and PL-03 rows point at it.
- `00`: the stage-E entry naming the donor's bash (its sha256 from
  RECORD.txt) and both fixtures' commands.
- The hand-back after stage E's record, as the brief's § 10: the tip, the
  artifacts by path, `reviewed-at:` and `fixed-at:` in #676's body.

## What never runs here

A build, a compiler, a guest, a fetch, a keyed council call, anything on a
unit, a change outside the two files and the audit folder, a change to any
upstream copy of either line.

## S3 -- #1125: the upgrade rehearsal seeds the retired quirks' real bytes (added at the hand-back, 2026-10-26 06:0x UTC)

Found by the lane while landing S2: `tools/vm-upgrade-rehearsal:99-115` seeds
four of `091-retired-vm-fixes`'s paths with its own line and `:156` expects
them taken back, which held only while the first pass removed by name. Against
#1124's fix the check reads `4`. The tool is fork-only and gates the next
candidate's step 3 (`release-candidates.md`), so it is this slice's third
stream, under this brief, in `tools/` -- stage E is past the stages A to D
rule.

File: `tools/vm-upgrade-rehearsal` (fork-only; `:99-115` the seed, `:156-157`
the checks).

1. **The positive, before.** On the host, the four seeded bodies as `:112`
   writes them, hashed, against `091`'s `WRITTEN` table at `8ebaf8daad`: none
   matches (`stage-e/s3-before.txt`). The fixed `091` over a scratch root
   seeded the rehearsal's way keeps all four (the fixture
   `t29-takeback.py`'s shape, or the fixture itself with the rehearsal's
   bytes as its input).
2. **The fix:**
   - `:112` seeds each of the four paths with **the bytes the retired quirk
     wrote there** -- the heredoc bodies of the `QEMU Standard PC (Q35 + ICH9,
     2009)/09x-*` scripts at `73b20caf86` or `8bb74015e6`, as
     `t29-takeback.py` rebuilds them -- embedded in the tool as heredocs,
     and **the seed asserts each body's sha256 is in `091`'s `WRITTEN`**
     (read from the new image's `091` on the guest, or from the tree at the
     rehearsal's start) so a later change to the table fails the seed, not
     the check;
   - **a fifth listed path with other bytes**, seeded beside them, with a
     `:156`-side check that it is kept (the owner's-edit case #1124 protects,
     on a real guest), and the existing `50-rehearsal-owner.conf` check kept;
   - `:102-105`'s comment says *bytes an old quirk wrote*, not *by name*.
3. **The positive, after:** the four bodies hash into `WRITTEN`; the fixed
   `091` over a scratch root seeded with them removes the four and keeps the
   fifth; `bash -n` on the tool (`stage-e/s3-after.txt`). The rehearsal's
   own run needs its guest pair and is the next candidate's step 3: #1125's
   criterion for it stays open until that run, stated in the bug.
4. **`Already written:`** nothing on a device; a rehearsal that ran the old
   seed left nothing behind (its guests are disposable).
5. **Commit:** `vm-upgrade-rehearsal: seed the retired quirks' real bytes, and
   a control that must be kept (Refs #676, #1125)`; `fixed-at` into #1125.

**The donor bash erratum.** This brief named
`/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/bash`; the
donor holds busybox and rclone only (its `RECORD.txt`). S1 ran under the
host's bash 5.3.9, named in its output, and the tree pins 5.3: accepted for
S1's verdict (a quoting and an assignment, the same in both); the image's
bash runs the fixture at the next granted window, not as a gate.
