# T27's remediation stream (#674)

Written by the coordinator on 2026-10-25 at T27's stage-C checkpoint, ahead
of its stage-D pause (D-WORKFLOW-189): one stream, in the shape of
`t11-streams.md`. The lane executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-device-h700-674`,
branch `feature/m6-device-h700-674`). **Review depth: Local.** The stream
lands with a case whose constructed input fails on the unfixed file and
passes on the fixed one, run on the host against a copy of the file at the
stage-D tip, kept on the branch under `stage-e/` (a driver taking the file
as its first argument, a README row), quoted in `02` § The streams'
positives. **Nothing runs on a unit**: the fixture stands in for the card
and the flash partition (D-QA-015, D-QA-027). `TMPDIR` under
`/workspace/tmp/m6-t27/`.

## S1. `bootloader/update.sh`: a failed step is reported, `dtb.img` is replaced whole or not at all (PL-12, the bug the lane files)

- **Files owned:** `projects/ROCKNIX/devices/H700/bootloader/update.sh`
  (upstream's file; a contained fix, said in the commit). **Not** `init`'s
  *Boot Files Updated.* line (`busybox/scripts/init`, T22's file, #669): the
  lane points it there with one comment naming this stream and the bug.
- **The shape.** Every step that can fail -- the remount, each copy to
  `/flash`, the `dd` of the loader -- is checked and ends the script with a
  non-zero exit naming the step; `dtb.img` is written to a temporary name
  beside it and renamed into place only after the write succeeded
  (`upgrade-and-install.md` § The last known good state: temp-and-rename,
  never in place), so a failed update leaves the previous `dtb.img` whole;
  the loader's `dd` happens after the tree is in place, and a failed `dd`
  is reported. The `vdd-dram` thresholds and the dt-id read are unchanged.
- **The test first** (`stage-e/s1/`): a fixture directory standing for
  `/flash`, a stub `mount` that fails the remount, a `cp` that fails on the
  tree, a `dd` that fails; `update.sh` run with its paths pointed at the
  fixture -- exit 0 and a truncated `dtb.img` on the unfixed file, exit
  non-zero naming the step with `dtb.img` as it was on the fixed, for each
  of the three failures; and the success case, both files the same bytes.
- **Already written:** a card whose update failed keeps what the failed copy
  left (a truncated `dtb.img` is possible today); the fixed script re-writes
  the tree and the loader on the next update, and a card already truncated
  is the runbook's hand step -- read both, nothing migrated, said in the bug.
- **Acceptance:** the bug's checkboxes from the cases; `fixed-at` set.
- **Commits:** `H700: update.sh reports a failed step and replaces dtb.img
  whole or not at all (#N)` -- `Refs #N, #674`.

## Order and hand-back

Stage D first (the bug, the audit issue, the Phase 7 outcomes), then S1,
then stages F to H as the brief has them. The coordinator accepts by
`$S/t27-accept.sh` on a clone of the merged tip, plus `stage-e/`'s row
re-run against the stage-D clone and the fixed tree.
