# Retained20 → actual candidate update → installed backup — UNRUN

This is a small outer adapter for the existing #565/#566 retained fixture. It
adds no acceptance criterion and repeats no accepted UI/component proof. Source
preparation only: no packet program, fixture, product import, payload reader,
VM, service, compiler, container or allocation ran while this packet was made.
The current engineering build retains exclusive runtime ownership. Root reviews
and allocates this **after** final artifact/payload custody and clean588 closure.

The earlier focused source review of installed588 commit
`615bbece9789b71230af5acd45c75d1d106d15ad` found no actionable defect against
frozen d6a87 and the root image verifier. This records that accepted read-only
review; it does not turn that UNRUN fixture into runtime evidence.

The unchanged retained parent is frozen by manifest
`f57c6a11bcc6daa98a7d3b2249a7deeb366afb44df5c44bcb0c0ead086ab3100`.
The exact correction archive is
`5e1255cbf9d22d1b2f0ff7b128be9f657d82be2d6e38870fccc284d7bc4111dd`
and its inner seal is
`bc4a76241fc24c40a61be59821c15ce5d9eb9514e4e8a34f203a5306b6431b08`.
The existing correction materializer changes only the backup child's receipt:
actual wait returncode and separate `timed_out`, instead of inventing exit124.
Original parent and correction bytes are retained. Their preparation readers
run only inside the future watched allocation.

Host QEMU/serial/call/stop/export patterns come from installed588's reviewed
outer adapter and the accepted independent-format coordinator. `census.py` is
copied unchanged from the qualified #584/#588 numeric proc/pidfd helper. The
outer owner is a subreaper so a terminated `run-phase.sh` cannot leave an
unobserved `timeout`/serial grandchild reading the socket. Any forced host-child
cleanup fails the original lifecycle. QEMU is always stopped separately through
its exact pidfile/disk identity. This is one owner and one serial operator;
there is no visual/input lane or concurrent serial client in this allocation.

## Exact sequence and bounds

1. Read actual final verifier `result.json`/`inputs.json`, verify original hashes,
   materialize the corrected derivative, and invoke its existing SYSTEM reader
   to produce the four serial scripts. Candidate commit/ES/update/SYSTEM hashes
   come from actual completed receipts, not a predicted image filename.
2. Inflate the accepted replacement20 install image into a fresh owned 16GiB
   disk. Its compressed bytes are 2,073,682,425 and SHA256 is
   `1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490`.
   Boot normal 4-vCPU/8GiB/no-NIC QEMU with unchanged helper/profile. The parent
   fixture verifies predecessor commit `1a026648442321609b2288c2c9c06803817f9df2`
   and original executing ES before seeding. No old guest/storage owner is reused.
3. Run `seed`, then `before`, preserving each original transport rc, serial
   guest marker, collector result and outer call rc. The seed phase supplies its
   existing untouched baseline readiness/clean check. No fixture media is attached
   before seed/before complete.
4. Write the actual verified update tar to a private ext4 medium with host
   `debugfs`, attach it read-only, verify its whole SHA256 in the guest, copy it
   to the empty `/storage/.update`, verify the staged bytes, sync and unmount the
   medium. Free storage is checked against tar + SYSTEM + KERNEL +1GiB. The
   normal updater gets the exact tar; no compatibility/verification bypass,
   boot-file edit, bind overlay or forced kernel argument is used.
5. Request actual `systemctl reboot --no-block`, retaining its original request
   result. Poll the same QEMU for changed boot ID, exact final BUILD_ID and ES;
   the fixture's `after` then performs the complete actual readiness, executing
   identity, empty update queue and selected-state comparison. The enqueue result
   alone never establishes a reboot.
6. Run the actual installed `backuptool backup` through the unchanged corrected
   `backup` phase. Require its original child `returncode:0,timed_out:false` and
   the existing archive/member/runtime/Recent assertions. Export only original
   value-free JSON receipts, sync, stop the exact QEMU, and close original host
   channels. Failed phases stop the sequence; no automatic retry.

Prospective owner bound is **4200 seconds work +180 seconds cleanup**. This
includes preparation/hash I/O, baseline boot, four phases, media copy and actual
two-boot update path. It is separate from the UI900-second owner. The aggregate
source review raised the initial 60+2-minute proposal to **70+3 minutes** so
original reader/transport/update and finalizer bounds fit without resetting any
clock in flight.

| Operation | Existing/future bound |
| --- | --- |
| Retained preparation readers | Existing120s per reader; outer450s |
| Baseline serial readiness | 240s poll /260s outer |
| Seed | Existing300s guest /340s transport; outer355s |
| Before and after, each | Existing180s guest /220s transport; outer235s |
| Update medium write | 180s |
| Guest hash/copy/hash/sync | 240s serial /255s outer |
| Actual update/reboot return | 600s poll /620s outer |
| Backup | Existing420s guest /460s transport; outer475s |
| Backup child | Existing180s +5s TERM +5s KILL/wait |
| Final receipt export/sync/stop | 40s/20s/35s commands within180s finalizer |

Whole-work timeout or signals remain failures, with original child outcomes.
Host command output is checked each second at8MiB; existing phase collector caps
serial output at2MiB. Guest original JSON receipts are individually capped2MiB.
No real account/provider requests or emulator launch are involved. Synthetic
settings, archive and backup stdout/stderr remain private in the stopped disk;
the export contains phase booleans/counts/identity and original exit receipts.

Retention reserves a16GiB raw ceiling,16GiB guest virtual disk, update-media size
of actual tar +128MiB (rounded toMiB), and1GiB fixture/backup/reader allowance.
This is a conservative disk reservation, not a measured physical peak. Native
host readers use existing tools; no package/container/build cache is changed.

## Future commands after root allocation

Can this be done on the VM? Yes. Root records the existing #565/#566 retained
allocation and confirms clean588 original owners are closed before launch.
First supply the actual baseline path and final verifier directory. Preparation
reads only small source/receipt data and file metadata, leaving full artifact
hashing and SYSTEM reading under the admitted owner.

```bash
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
TASK_PACKET=/tmp/m7-retained-update-lifecycle-20261014
TASK_OWNER=/workspace/tmp/pix-m7-retained20-20261014-01
# Resolve TASK_BASELINE from the retained accepted20 artifact store.
# TASK_VERIFY is root's completed image-verification output containing
# result.json, inputs.json and extracted SYSTEM, not an unfinished build root.
# Root chooses an observed-free VNC display; 129 is proposed only.
python3 -I -S -B "$TASK_PACKET/prepare.py" \
  --checkout "$TASK_TREE" --expected-commit d6a87f05c1935516115b2cca1af22151a0209224 \
  --baseline "$TASK_BASELINE" --verification "$TASK_VERIFY" \
  --owner "$TASK_OWNER" --id m7-retained-20261014-01 --vnc 129
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

Root actively supervises the exact returned `.build-runs/<id>` and owner records.
No other agent operates serial, QMP/HMP, VNC or guest state during this owner.
After all original owner/runner/watcher/launcher channels close:

```bash
TASK_RUN="$TASK_TREE/.build-runs/ACTUAL_RETURNED_RUN_ID"
python3 -I -S -B "$TASK_OWNER/close.py" \
  --owner "$TASK_OWNER" --run "$TASK_RUN" \
  --packet /workspace/tmp/pix-m7-retained20-evidence-20261014-01
```

The close command checks original channel equality, actual PID absence, four
original phase receipts, changed boot IDs and the real backup-child receipt,
then archives and rehashes all small original records. It neither grants
acceptance nor consumes admission/deletes media. Root reviews those originals,
consumes the exact allocation, then retires only this owner's `vm/` disk/input
medium/UEFI; private synthetic state/archive retire with that disk. Failed runs
remain failed; compact available receipts can be exported without replaying a
phase. A missing owner/stop receipt requires diagnosis before retirement.
