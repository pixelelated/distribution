# T22's remediation streams (#669)

Written by the coordinator on 2026-10-25 at T22's stage-D ruling, for its
stage E (D-WORKFLOW-189): three streams and one conditional, in the shape
of `t27-streams.md`. The lane executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-os-system-services-669`,
branch `feature/m6-os-system-services-669`). **Review depth: Extended**,
unchanged -- the streams' positives are host fixtures, the seats are not
re-run for them. Each stream lands with a case whose constructed input
fails on the unfixed file and passes on the fixed one, run on the host
against a copy of the file at the stage-D tip `0f7ece71e8`, kept on the
branch under `stage-e/<stream>/` (a driver taking the file as its first
argument and `unfixed|fixed` as its second, printing one verdict line; a
crossed run prints `UNEXPECTED`; a README row per stream; `run-all.sh`),
quoted in `02` § The streams' positives. **The guest is not required for a
fix's positive**: the second window's record (cases 3 and 4) is the
*before*; the *after* on a guest is an open item to test unless a third
short window is asked for by name and granted. Nothing runs on a handheld
(D-QA-015). `TMPDIR` under `/workspace/tmp/m6-t22/`. The line numbers are
at `8ebaf8daad`, which the stage-D tip carries unchanged for these files.

## S1. `scripts/init`: an update's writes are checked and reported, and a rejected update leaves `/storage` mounted and the staged file named (PL-02, PL-03; the bugs the lane files)

- **File owned:** `projects/ROCKNIX/packages/sysutils/busybox/scripts/init`
  (upstream's file; a contained fix, said in the commits). Nothing else.
- **The shape, PL-02.** `update_file` discards `dd`'s status (`:403`) and
  `update_partition` captures and prints but never tests (`:420-423`);
  *Update complete* follows regardless (`:1133`). The fix: every write is
  checked (`cmd; rc=$?` on its own line, `engineering-practices.md` § Guards
  must fail closed) and compared where a checksum exists (the package's
  md5 the acceptance already read, `:1031-1069`); a file write goes to a
  temporary name beside the target and is renamed into place only after
  the write succeeded (`upgrade-and-install.md` § The last known good
  state), so a failed write leaves the previous kernel or SYSTEM whole; a
  partition write that fails is reported by name; the message on failure
  names the step and the file, never *Update complete*, and the boot
  continues on what is in place. `dd`'s operands are quoted (G-34's
  `:403`, the same lines).
- **The shape, PL-03.** Every rejection calls `do_cleanup` (`:1065`,
  `:1077`, `:1116`), which unmounts `/storage` (`:861-863`) and returns 0;
  the boot loop checks no step (`:1312-1314`) and `prepare_sysroot`'s
  `mount --move /storage` (`:1143`) finds nothing, behind `exec
  2>/dev/null`. The fix: a rejection leaves `/storage` mounted (the
  cleanup that follows a rejection unmounts only what the update mounted,
  or remounts `/storage` before returning), and the staged file is renamed
  to `<name>.rejected` with the reason written beside it rather than
  deleted, so the owner can read why; the rejection's reason reaches the
  console as it does today. The second window's case 4 is the *before*.
- **The test first** (`stage-e/s1/`): the update functions extracted from
  the file at the stage-D tip and at the fixed tip into a shell fixture
  with a fake `/flash` and `/storage` under `TMPDIR`, a stub `dd` that
  fails on the second call, a stub `mount`/`umount` that records calls:
  (a) a failed kernel write -- unfixed: *Update complete* printed and the
  target truncated or absent; fixed: the step named, rc non-zero, the
  previous file's bytes intact; (b) a failed SYSTEM write, the same; (c)
  the success path, both the same bytes; (d) a wrong-md5 staged update --
  unfixed: `do_cleanup` unmounts `/storage` and the file is gone; fixed:
  `/storage` stays mounted (the recorded calls show no `umount /storage`)
  and `<name>.rejected` exists with its reason.
- **Already written:** PL-02: a unit whose update write failed reboots
  into what was written, nothing on `/storage` -- read both, nothing
  migrated; the fixed script checks the next update. PL-03: a unit that
  met a rejection booted once without `/storage`; the next boot mounts
  it -- nothing inherited beyond the deleted staged file, which the fixed
  script keeps as `.rejected`.
- **Acceptance:** the two bugs' checkboxes from the cases; `fixed-at` set.
- **Commits:** `busybox: init reports a failed update write and keeps the
  previous kernel and SYSTEM (#N)` and `busybox: init leaves /storage
  mounted after a rejected update and keeps the staged file as .rejected
  (#M)` -- `Refs #N, #M, #669`.

## S2. `input_sense` -- does not run (PL-05 is the M7 line's `6101242e14`)

**Struck at the second window's RETURN (10:24 UTC).** The image's `input_sense` is not the read tree's: the M7 line's `6101242e14` (*m7: integrate reviewed frontend and installer repairs*) empties the list and the found-flags inside the loop, and the guest shows one reader per device. PL-05 stands as a defect of `8ebaf8daad`'s bytes and is *deferred to the M7 line's integration* (#344): recorded with that commit, no bug, no stream, checked when `next` carries it. What follows is the stream as written before the window, kept for the record.


- **File owned:** the `input_sense` script the analysis cites
  (`projects/ROCKNIX/packages/sysutils/system-utils/sources/...`: the lane
  names the path at `8ebaf8daad`; upstream's `dc5f51ad72`, *input_sense:
  make the device rescan retry actually run*, 2026-09-11).
- **The shape.** `:292` empties the list once before the retry loop
  (`:294-330`), so up to six passes append the same devices and the
  readers started at `:347-357` are duplicated; the comment at `:290-291`
  states the intent. The fix moves the reset inside the loop (each pass
  builds the list afresh) and starts one reader per device found on the
  last pass; the retry count and sleeps are unchanged. G-24 (`reload`
  restarts nothing, `:105-106`) is a #585 line, not this stream.
- **The test first** (`stage-e/s2/`): the function extracted into a host
  fixture with a fake `/dev/input` listing that is empty on the first
  pass and holds two devices from the second; the unfixed function
  returns a list with each device repeated for every remaining pass, the
  fixed one each device once; a stub `evtest` records how many readers
  start per device (unfixed > 1, fixed 1). The second window's case 3
  (six `input_sense` processes on the guest) is the *before*.
- **Already written:** nothing inherited (readers are processes; a reboot
  starts them afresh).
- **Acceptance:** the bug's checkboxes from the case; `fixed-at` set.
- **Commits:** `system-utils: input_sense rebuilds its device list on every
  retry pass (#N)` -- `Refs #N, #669`.

## S3. `095-cloud-ssh`: the port is a whole number or it is refused (PL-28; the fork's own bug)

- **File owned:** the GENERIC_X64 quirk `095-cloud-ssh` the analysis cites
  (`projects/ROCKNIX/packages/hardware/quirks/platforms/GENERIC_X64/...`;
  the fork's own, D-QA-053).
- **The shape.** `:38` does `tr -cd '0-9'`, so `12x34` is kept as `1234`,
  against the comment at `:33-34`. The fix: the value is accepted only
  when it is all digits and in 1 to 65535 (`case` on the whole string,
  then the range), else refused with one line to the journal naming the
  value's shape (never the value if it looks like a credential -- it is a
  port, print it) and the default kept.
- **The test first** (`stage-e/s3/`): the port block extracted and run
  over constructed values: `1234` accepted both; `12x34` -- unfixed
  accepted as `1234`, fixed refused; `70000` refused fixed; an empty
  value keeps the default.
- **Already written:** nothing inherited beyond the setting on the VM's
  own file; a guest that had `12x34` set listened on 1234 and keeps the
  default after the fix.
- **Acceptance:** the bug's checkboxes from the case; `fixed-at` set.
- **Commits:** `quirks: GENERIC_X64 095-cloud-ssh refuses a port that is
  not a whole number (#N)` -- `Refs #N, #669`.

## S4 -- does not run (the window's case 1 showed a refusal)

**Struck at the second window's RETURN (10:24 UTC).** `udevil` refuses the btrfs medium (`denied 90: option 'compress=zstd:3' is not an allowed option`, by the medium's unit and by `udevil --mount` alike), so no medium mounts without the three options; PL-01 is recorded as a Low on #585 (a filesystem the configuration cannot mount, and a unit that reads `active` after the refusal, G-30). The conditional stream as written before the window follows, for the record.


- **Runs only when** the second window's record shows `udevil --mount`
  mounting the loop-backed btrfs filesystem without the three options. If
  the record shows a refusal (`compress=zstd:3` absent from
  `allowed_options`, `:245`), PL-01 is recorded as a Low on #585 and this
  stream does not run.
- **File owned:** the udevil configuration the analysis cites
  (`udevil.conf:233`, upstream's `c288a47e62`).
- **The shape.** `default_options_btrfs` carries `nosuid,noexec,nodev`
  beside `compress=zstd:3`, as `:213`'s own rule says every type must; the
  option stays in `allowed_options` only if it is there today.
- **The test first** (`stage-e/s4/`): on the host, the file parsed the way
  udevil reads it (a grep of the effective line) at the unfixed and fixed
  tips; the guest's *after* is an open item to test unless a third window
  is granted.
- **Already written:** nothing inherited: mounts are transient.
- **Commits:** `udevil: btrfs media mount with nosuid,noexec,nodev like
  every other type (#N)` -- `Refs #N, #669`.

## Order and hand-back

Stage D's outcomes and the lint first; then S1 and S3 (S2 and S4 struck
at the window's RETURN), each with its case before its fix; then stages F to H as the brief
has them, the retro's scoped audit asking of each fix whether its positive
exercised the job the fix could break (check 7, step 5). The coordinator
accepts by `$S/t22-accept.sh` on a clone of the merged tip, plus
`stage-e/run-all.sh` against the stage-D clone and the fixed tree.
