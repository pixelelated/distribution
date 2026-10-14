# Retained backup parser correction — parser03, UNRUN

The original retained owner ended with original exit 1 at the backup fixture's
prerequisite stage. Seed, before, actual update/reboot and after passed. Backup
transport exited 0 and its original guest marker was 1; no installed backuptool
child started. Those original results remain unchanged.

The cause is a fixture parser mismatch, not observed backup product failure.
The guest fixture passed raw cloud_sync.conf to the strict assignment parser.
The shipped RCLONEOPTS assignment spans three lines: its first physical line
starts a quote without ending it. The selected-state checker's existing cloud
branch joins backslash-newline continuations before parsing. Stopped-disk
readback original 0 established the retained config exactly equals shipped:
8,232 bytes, SHA256 a121977066ce805e791108258fe12d1ecbce5e71ce2f61f096394a9fca982305,
two continuations. Original backup-child/output/archive creation was absent.
No further disk-only evidence is needed for this diagnosis.

This derivative changes one guest expression to use precisely the checker's
text decoding, continuation removal and re-encoding. It evaluates no shell.
The strict assignment parser, backup destination requirement, after-receipt
same-boot guard, real installed command, original wait/timeout receipt,
selected-state comparison, archive sanitizer assertions and cleanup are retained.
Host changes only bind/copy that guest source into a separately sealed
`source/retained-parser-corrected` directory after preserving all prior source
stages. The prior parent packet and failed source, seals and selected original
receipts are retained byte-for-byte in `source-originals.tar.gz`.

`complete.diff` contains all executable and README differences against gate02
and its actual failed guest source. `derivation.json` records every original
archive member. `static-review.json` records Python 3.10 AST parsing and exact
source comparisons only. No packet script, fixture, service, image reader, VM,
container or build was run during preparation. Runtime acceptance remains open.

Source references: failed guest-fixture.py:372; corrected
retained-guest-fixture.py:373; bound pixelelated-state-check:128–163 (strict
parser), :525–529 (cloud normalization). Frozen installed backuptool:58–73
(destination), :145 (name), :699 (standalone token), :813–824 (regular files),
:1199–1232 (system and ScreenScraper stripping) match the retained assertions.
No additional deterministic archive-contract mismatch was found in this review;
actual installed backup and its archive remain untested.

## One fresh full lifecycle after root allocation

Root chose a fresh complete lifecycle, preserving the boot guard. The stopped
old disk cannot directly resume backup because after.json belongs to its prior
boot. Repeating before/after is necessary to complete the previously failed
composed proof; it neither replaces the original receipts nor invents a resume
protocol. Use fresh owner02, fresh storage and the same actual baseline/update.
The unchanged prepare reader derives final update/SYSTEM/ES/source identities
from the completed verifier. No product/source/native overlay is used.

Can this be done on the VM? Yes: the existing #565/#566 retained proof remains
one serial operator, normal 8 GiB/4 CPU/no-NIC QEMU. Root records the admitted
owner only after the current sole runtime owner has terminated and closed.

```bash
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
TASK_PACKET=/tmp/m7-retained-update-lifecycle-parser03-20261014
TASK_OWNER=/workspace/tmp/pix-m7-retained20-20261014-02
TASK_BASELINE=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261011T194522Z.g1a0266484423-from-ROCKNIX.img.gz
TASK_VERIFY=/workspace/tmp/pix-m7-image-readback-20261014-01/artifacts
# Root verifies display 129 is free before selecting it.
python3 -I -S -B "$TASK_PACKET/prepare.py" \
  --checkout "$TASK_TREE" --expected-commit d6a87f05c1935516115b2cca1af22151a0209224 \
  --gate-checker /workspace/repos/rocknix.worktrees/m7-player-setup/tools/pixelelated-state-check \
  --baseline "$TASK_BASELINE" --verification "$TASK_VERIFY" \
  --owner "$TASK_OWNER" --id m7-retained-20261014-02 --vnc 129
cd "$TASK_TREE"
tools/build-preflight
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$TASK_OWNER/retention-plan.json" --output "$TASK_OWNER/retention-report.json"
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$TASK_OWNER/admission-plan.json" --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --admission "$TASK_OWNER/admission.json" -- \
  python3 -I -S -B "$TASK_OWNER/vm-lifecycle.py"
```

Keep the unchanged 4200-second work and 180-second finalization bounds;
preparation450s, seed355s, before/after235s each, actual reboot620s,
backup475s (guest420s, child180s +5s TERM +5s KILL/wait). Output limits and
16GiB disk/raw ceilings, exact update tar +128MiB medium and 1GiB scratch
allowance are unchanged. Original owner/runner/watcher/launcher outcomes,
phase transport markers, cleanup and sole-operator custody remain required.

After all original channels close, using the actual returned run directory:

```bash
TASK_RUN="$TASK_TREE/.build-runs/ACTUAL_RETURNED_RUN_ID"
python3 -I -S -B "$TASK_OWNER/close.py" \
  --owner "$TASK_OWNER" --run "$TASK_RUN" \
  --packet /workspace/tmp/pix-m7-retained20-evidence-20261014-02
```

Expected success requires four original phase exits 0, changed update boot ID,
actual installed backup-child returncode 0 with timed_out false, archive and
runtime-state comparisons, ES restoration and original owner/runner/monitor
closure without forced cleanup. Root reviews originals, consumes the exact
allocation and retires only its owned media. The failed owner01 remains failed.
