# Corrected-image retained installed loader — UNRUN

This extends the exact sealed retained loader1ac31664 with the already-qualified
ordinary update/serial/USB input path. The protected retained02 base was really
updated from accepted20 to d6a and passed selected-state/default-backup checks.
Those accepted original proofs are retained; no fresh seed, backup, topup,
browser flow or memory matrix is repeated here.

Target currently frozen: fac608ff89940ce358ea9b8a95e9a08a6fe26568 at
`/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02`, ES3178b832… .
The source does not predict the new tar filename, hash or final installed
library hashes. Preparation requires the new completed verifier result and
inputs, matches its source to checkout HEAD and its ES to the literal package
pin, binds the one actual update tar by size/hash, and requires all13 selected
installed members. The new verifier prepared at
`/tmp/pix-m7-gstnet-image-verifier-20261014` supplies libgstnet and its four
installed plugin consumers in addition to the existing loader identities.
Do not hand-fill a missing receipt/member.

One normal8GiB/4CPU/640×480 no-NIC VM uses a new writable QCOW2 overlay over
`/workspace/tmp/pix-m7-retained20-20261014-02/vm/disk.qcow2`, with copied private
OVMF variables. The original base/OVMF/evidence stay protected; whole backing
hash/stat equality is verified before and after under the admitted owner.
No overlay is committed to the base.

Sequence:

1. Revalidate the original accepted retained02 receipts and normal owner exit.
   Boot the overlay on its inherited d6a image. Compare old installed identity,
   exact accepted synthetic selected-state predicates and original receipt hashes.
   Save a private byte/mode snapshot of the eight existing selected files in
   a uniquely owned overlay cache directory. No selected file is changed.
2. Hash the actual verified new tar. Use the existing bounded private ext4 USB
   input medium (host writable during creation, attached read-only), mounted
   ro,noload in the guest. Check SHA256 on the medium, copy to ordinary
   `/storage/.update/<actual filename>`, verify it again, sync and unmount.
   Reboot normally through the installed service. No SYSTEM/kernel overlay,
   boot option or product binary is replaced by the fixture.
3. Wait for changed boot ID, exact new BUILD_ID and normal ES readiness.
   Revalidate original receipt hashes/selected predicates, byte/mode equality
   across the actual update, empty update queue and the existing bound
   `retained-upgrade` checker policy. Remove only the private snapshot after
   successful comparison. Output names changed paths on mismatch without
   account values/hashes; mismatch stays failed and is investigated.
4. Run the unchanged installed loader fixture on that actual new boot:13
   installed byte/mode/rooted-link checks, three original RTLD_NOW loads,
   original two ldd calls, one fresh default `gst-inspect opengl` scan. The
   existing no-warning predicate remains strict. Original stdout/stderr/waits
   are emitted before assertions; the exact registry and failure envelope
   are exported. Existing selected state is also byte-compared across the probe.
5. Existing subreaper/pidfd census, normal vm-stop, original waits and backing
   equality finalize the owner. Any forced cleanup prevents success.

The checker is an explicit source path + expected SHA256 input, copied into
private host source and evaluated only by the future guest, as in accepted
retained qualification. Current qualified checker is6d061af89caba886bd3417ee96dc01e37675655aa1ed92f423b9db02164dff03.
No checker self-test or full backup is repeated. Its policy report is condensed
to the actual pass result, while original state command/stdout/exit remains.
Private snapshot contents remain inside disposable storage and are never in
compact export. Old seed/before/after/backup receipts remain byte-unchanged.

Resource envelope remains the accepted retained lifecycle4200s work plus180s
cleanup; this is a ceiling, not an inserted wait. Existing stage limits:
initial boot240s, input format60/write180, staging240, update readiness600,
state reader100 each, loader15/15/30 with130s guest transport, backing hash120
before/after, normal VM stop35. One guest only; no network or backend.
Private input media is actual tar bytes +128MiB rounded up to MiB. Retention
allows one16GiB overlay plus input media and128MiB records/UEFI margin.
Existing64MiB host record limit and resource sampling remain. No guest service
cgroup cap is claimed. This source packet has allocated or executed nothing.

After the coordinator's new build/readback completes:

```bash
TASK_SOURCE=/tmp/pix-m7-retained-loader-update-20261014
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-02
TASK_COORD=/workspace/repos/rocknix.worktrees/m7-player-setup
# Exact completed artifacts/result.json, with libgstnet and four plugins:
: "${TASK_VERIFY:?set newly completed verifier result.json}"
TASK_OWNER=/workspace/tmp/pix-m7-retained-loader-update-20261014-01

python3 -I -B "$TASK_SOURCE/prepare.py" \
  --checkout "$TASK_TREE" --verification "$TASK_VERIFY" \
  --retained-owner /workspace/tmp/pix-m7-retained20-20261014-02 \
  --retained-evidence /workspace/tmp/pix-m7-retained20-evidence-20261014-02 \
  --state-checker "$TASK_COORD/tools/pixelelated-state-check" \
  --state-checker-sha256 6d061af89caba886bd3417ee96dc01e37675655aa1ed92f423b9db02164dff03 \
  --owner "$TASK_OWNER" --vnc 130
cd "$TASK_TREE"
tools/host-maintenance/retention-report --plan "$TASK_OWNER/retention-plan.json" \
  --output "$TASK_OWNER/retention-report.json"
tools/host-maintenance/build-admission prepare --plan "$TASK_OWNER/admission-plan.json" \
  --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --admission "$TASK_OWNER/admission.json" --activity-dir "$TASK_OWNER" --recursive-activity -- \
  python3 -I -B "$TASK_OWNER/vm-lifecycle.py"
```

Port130 is proposed and checked before launch. Root alone allocates, supervises
and reviews originals. Inspect state-before/after, changed boot IDs, staged tar
hash results, per-command loader receipts, registry and base-before/after.
After actual completion and normal owner/process exit:

```bash
TASK_RUN=$(cat "$TASK_OWNER/run.path")
TASK_EXPORT=/workspace/tmp/pix-m7-retained-loader-update-evidence-20261014-01
python3 -I -B "$TASK_OWNER/close.py" \
  --owner "$TASK_OWNER" --run "$TASK_RUN" --output "$TASK_EXPORT"
# Coordinator reviews originals before this explicit existing consumption:
tools/host-maintenance/build-admission consume --run "$TASK_RUN" \
  --evidence "$TASK_EXPORT/consumption-draft.json"
```

Compact export contains original commands/statuses and value-free state/loader
receipts, never private snapshot values. After consumption, retire this overlay,
input medium and copied OVMF. Only the coordinator may then retire the separately
owned retained02 base after confirming no remaining dependent overlay/consumer.
The earlier failed diagnostic remains failed. This packet is entirely UNRUN.
