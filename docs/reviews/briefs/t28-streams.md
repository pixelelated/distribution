# T28's remediation stream (#675)

Written by the coordinator on 2026-10-25 at T28's stage-D pause
(D-WORKFLOW-189): one stream, in the shape of `t27-streams.md` S1. The lane
executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-device-sm8550-675`,
branch `feature/m6-device-sm8550-675`). **Review depth: Independent**,
unchanged; the seat is not re-run for the fix. The stream lands with a case
whose constructed input fails on the unfixed file and passes on the fixed
one, run on the host against a copy of the file at the stage-D tip
`b13d5d8074`, kept on the branch under `stage-e/s1/` (a driver taking the
file as its first argument and `unfixed|fixed` as its second, one verdict
line, `UNEXPECTED` when crossed, a README row, `run-all.sh`), quoted in `02`
§ The streams' positives. **Nothing runs on the Nova** (D-QA-015,
D-QA-027): the fixture stands in for `/flash`, the ABL slots and
`updateabl`. `TMPDIR` under `/workspace/tmp/m6-t28/`.

## S1. `bootloader/update.sh`: `updateabl`'s failure is reported and the update is not marked done (PL-01, the bug the lane files)

- **File owned:** `projects/ROCKNIX/devices/SM8550/bootloader/update.sh`
  (upstream's file at `8ebaf8daad`; a contained fix, said in the commit;
  the next base merge replaces the file with upstream's 43-line version,
  which keeps the shape -- **#1099 carries the requirement forward** as a
  named line, so the merged script keeps the check). **Not** `updateabl`
  (T1's, #648: its own two-slot write is read, not changed) and **not**
  `init`'s *Boot Files Updated.* line (T22's, #669, pointed at from #1105's
  family).
- **The shape.** `:25` runs `updateabl` and ignores its exit; `:27-37`
  remove `/flash/boot` and `/flash/EFI`, write `UPDATE` and `.boot.hint`
  whatever happened. The fix: the copy to `/flash/rocknix_abl` (`:19-23`)
  and the `updateabl` run (`:25`) each capture their exit on its own line
  (`cmd; rc=$?`, `engineering-practices.md` § Guards must fail closed); a
  non-zero exit ends the script non-zero with the step named on the
  console, and neither the removals nor `UPDATE` nor `.boot.hint` are
  written after a failed step; the success path is byte-for-byte what it
  was. The `BOOT_DISK` computation (`:12`, never used) is left alone (a
  #585 line, not this stream).
- **The test first** (`stage-e/s1/`): the script's lines run under a fixture
  with a fake `/flash` and a fake `$SYSTEM_ROOT/usr/share/bootloader/rocknix_abl/`
  under `TMPDIR` (paths rewritten as T27's S1 did), a stub `updateabl` on
  `PATH` that exits 0, 1 or hangs-then-exits-1 by the case, and a stub `rm`
  that records: (a) `updateabl` exits 1 -- unfixed: exit 0, `UPDATE` and
  `.boot.hint` written, the removals done; fixed: exit non-zero naming
  `updateabl`, nothing written, nothing removed; (b) the copy fails (the
  source directory empty or unreadable) -- unfixed: exit 0 and `UPDATE`
  written; fixed: the step named, nothing written; (c) the success path --
  both files the same bytes, `UPDATE` and `.boot.hint` written.
- **Already written:** a unit whose `updateabl` failed carries the new OS
  with the ABL `updateabl` left (both slots unchanged when it failed before
  its `dd`s, or as `updateabl`'s own two-slot order left them -- T1's
  file); the fixed script reports on the next update and writes nothing
  new to the slots itself; nothing migrated; device fact line 17 (the
  2026-10-12 update, both slots written) is the observed case.
- **Acceptance:** the bug's checkboxes from the cases; `fixed-at` set.
- **Commits:** `SM8550: update.sh reports a failed copy or updateabl and
  does not mark the update done (#N)` -- `Refs #N, #675`.

## Order and hand-back

Stage D's outcomes and the lint first; then S1 with its case before its
fix; then stages F to H as the brief has them. The coordinator accepts by
`$S/t28-accept.sh` on a clone of the merged tip, plus `stage-e/run-all.sh`
against the stage-D clone and the fixed tree.
