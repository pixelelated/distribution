# #508 broad script harness

Owner: `/root/handoff_review`. These are host-side synthetic fixture checks,
using candidate16 BusyBox/rclone. They do not qualify final firmware or exercise
personal devices or cloud data.

The selected product source is clean commit
`e484380a3426626d84afa0c5109abeff4512dd0c` in
`/workspace/repos/rocknix.worktrees/m7-manual-cloud-folders`.
`broad01-inputs.json` records exact harness, helper, source and binary hashes;
`broad01-harness.patch` records the harness delta. `broad01-owner.json` records
host PIDs/start ticks and the durable watcher directory. The sandbox's `/proc`
need not expose those host PIDs.

## Focused results

- `focused02.log`: current C1/C2 setup/seeding and SC scan checks, 80 PASS.
- `focused03-historical.log`: the same extracted sections against
  pre-retirement commit `7cfdf9f73ae2a064ee4f281461e661301cb2dd65`, 83 PASS.
  Historical join/follow assertions execute against actual historical bytes.
- `selection-results.json`: three source-availability controls PASS. A missing
  engine still installed by the selected recipe exits 2. Retired engines are
  explicitly not applicable and contribute no PASS checks.
- `reader-results.json`: current setup and historical migration pointer-reader
  checks both exit 0.
- `historical-ref-dispatch.log`: `--cloud-layout --ref ... --case T24 --list`
  is forwarded to the dedicated helper. This is CLI routing evidence only;
  T24 substring selection also includes migration cases. Current broad coverage
  therefore uses the helper's explicit `--archives-only` allowlist.

Original unsuccessful focused runs are retained. `focused01.log` has one new
assertion failure: a failed scan's state file holds diagnostic text, so the
correct assertion is absence of usable `STATE=` facts. `focused02-historical.log`
has one inherited comparison failure: the selected historical config was
compared with today's source config. The check now compares selected source
bytes. Each corresponding extracted script is retained, along with the final
successful historical extract. `focused-summary.json` gives the counts.

## Broad run

`broad01-supervisor.log` is the complete console output. The durable watcher
owns exit status and terminal state; an in-progress tail is not acceptance.
The shell, helper and product source are frozen until this run terminates.
No historical migration case is counted as passed when its engine is retired.
Ordinary archive writer, reader and selection checks remain enabled.

Broad01 uses direct `tools/watch-build` in exec session58141. It has durable
watcher files but no separate `watch-build-submit` launcher. The named owner
actively supervises through terminal delivery; automatic off-session delivery
is not established. Future long checks use the D-WORKFLOW-148 submit launcher.

Broad01 completed at 18:44 UTC: build.rc=0, watcher `finished`, 1,303 main
PASS lines, no FAIL/SKIP lines, and all thirteen archive-only cases. Exact
controller, shell and watcher exits were confirmed in the host namespace before
source or harness edits resumed. This is pre-delta evidence for e484/67c6; two
separately reproduced folder edge cases were not covered by that run.

## Final affected delta

The later source review found an empty relative folder was misclassified and a
final seeding readback accepted partial output from a failed provider call.
The source owner retains the comprehensive path/provider controls. This harness
adds one targeted C2 guard: after README writes, the synthetic provider prints a
name but exits 5. Setup must fail and must not report the saves folder OK.

`focused04-pre/` runs immutable e484: 80 PASS, one expected regression FAIL.
`focused04-post/` runs frozen cloud_setup SHA256
a7eea3879848ec4879f279f3b7e2a2c08f3531c970ec4dd9858b09290975265c:
81/81 C1/C2/SC checks PASS. Each uses a fresh durable submit owner with both
runner and wrapper exit codes, terminal watcher state, and confirmed process
exits. No archive implementation changed, so the ordinary archive subset was
not repeated. Original full and focused failures remain available.

`final-result.json` and `final-harness.patch` seal the completed harness work.
The product source remains an unintegrated draft pending the requested flow
review. No new firmware build or personal device/cloud action is part of this
packet.
