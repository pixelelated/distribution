# Final-image standard/cloud continuation — SOURCE ONLY, UNRUN

This is the accepted qa19/20 sequence with completed final-image inputs and an
owned bounded lifecycle. Existing `tools/vm-pair`, `tools/vm-qa`, backend, round
trip, exit, time-to-play, walk and frame-diff implementations are unchanged.
No firmware, guest, backend, service, compiler, container or fixture was executed
while preparing this packet. No product or shared record was edited.

Can this be done on the VM? Yes. Root records the existing whole-image allocation
before launch. Run after completed image readback and the separately owned clean
and retained proofs. This sequence is the standard whole-image baseline; it does
not reopen #349's accepted checkboxes or repeat its archive/component controls.
#511 public documentation remains separate. It uses synthetic local QA data and
WebDAV/SFTP/local MinIO only: no real account, provider, handheld, optical game
ROM download or RetroAchievements opt-in. Existing walk stub ROMs are display
fixtures; their frames are not native gameplay/save qualification.

The ancestry is `2026-10-11-pixelelated-replacement-19/qa-plan/run.py` and the
replacement20 acceptance/report records. QA20's original aggregate remains 1
(seven host-script failures); its separate exact-input correction and
acceptance02 remain separate, and its other fourteen standard rows and each
108-check backend round remain accepted. This packet never relabels those exits.
The former fixed image19 payload checker is superseded here by the completed
final-artifact verifier and the separate untouched clean/retained owners; its
old identity literals are not copied into new assertions.

The sequence, once per same final image:

1. Verify completed image/source/ES receipts, exact selected installed BusyBox
   and rclone inputs, unchanged published ES checkout, exact built RetroArch
   wrapper source, and the existing walk baseline. Check fixed suite ports and
   absence of another QEMU; these standard tools use ports10022/10023, VNC9/10,
   WebDAV9010, SFTP9013, MinIO9012 and deliberately unbound9011. Root serializes
   this allocation with other guests/backends.
2. Use unchanged `vm-pair up IMAGE` to create two independent16GiB disks and
   default4CPU/8GiB guests. Record actual QEMU PID/start/argv and full guest
   BUILD_ID. No boot/controller/profile override is introduced. `vm-pair`
   provisions its normal QA SSH key; its existing `fresh` suite is not a claim
   of untouched pre-seeding clean evidence, which the earlier owner supplies.
3. Run unchanged default `vm-qa --skip-up IMAGE` on WebDAV. This covers all15
   required standard rows: scripts, lifetime, wrapper, vocabulary, French,
   quoting, menu map, register, pair identity, fresh, round trip, exit, time to
   play, walks, and frame diff. No `--link`, `--ra-offline` or extra case list.
   WebDAV/fresh/exit/TTP/pair/walks are not repeated as separate commands.
4. Run `vm-qa --skip-up --only round-trip --backend sftp IMAGE`, then the same
   one row for s3. Each backend has its own private state path and artifact root;
   the MinIO name is unique to this owner. Its immutable locally available image
   is `sha256:14cea493d9a34af32f524e538b8346cf79f3321eff8e708c1e2960462bd8936e`.
   The owner verifies `docker image inspect` before up; there is no pull step.
   Each actual process/container identity is recorded and checked after its row.
5. Close the exact pair's existing cloud-round-trip SSH masters normally. Stop
   each owned backend with the original helper, after checking PID/listener or
   container ownership; stop the exact pair by pidfile+disk. Any new anonymous
   MinIO volumes are removed only if attached to the recorded unique container
   and absent from the pre-run volume census. Retain original cleanup exits,
   actual port/container absence and subreaper/pidfd descendant census.

The outer command stops after the first failed stage; `vm-qa` itself retains its
existing behavior of completing its selected suite rows and returning aggregate
status. Original wait status and timeout indication are separate. A return0
alone is insufficient: `vm-qa` can return0 with SKIP, so the adapter reads the
original report and requires exactly the selected PASS rows and its unskipped
summary. It also preserves the original round-trip restoration line and refuses
its explicit incomplete-cleanup warning. This is correct interpretation of the
existing suite, not a new case. Failed reports/logs are retained unmodified.

Per-stage ceilings are pair-up900s; each explicit backend-up120s; standard3600s;
SFTP300s; S3300s; each backend-down25s; pair-down70s. The whole owner is5700s plus
an independent180s cleanup alarm. Accepted qa19/20 standard examples took roughly
29minutes (scripts~518s, walks~1010s, WebDAV~84s, exit~26s, TTP~69s); the bounds
allow existing work to finish without shortening product timers. Resource
sampling every5s records host memory/PSI, free disk and actual QEMU RSS. Both
canonical guests bound configured RAM to16GiB total; allow additional host
control/compiler/backend memory when admitting this existing standard suite.
No host or service cgroup cap is claimed. Records/frames are capped at512MiB,
4096files,16MiB per stage stream; retention reserves the actual raw image size,
32GiB disks,8GiB host/backend temporary allowance and512MiB originals. The8GiB
term is disk admission allowance, not a falsely claimed kernel quota. Qualified
`census.py` is copied unchanged; the owner is a verified subreaper, preserves
original waits and uses pidfd-only fallback. Any forced cleanup fails the owner.

`prepare.py` consumes `result.json`, sibling `inputs.json` and `candidate.img`
from the completed image verifier. It derives the full distribution and ES pins
from those receipts, requires the checkout/package pin/published ES HEAD to
match, and records the actual image path/hash/size. No predicted artifact name,
old image19 pin, whole SYSTEM extraction or manually asserted PASS is used.
`QA_SYSTEM_ROOT` is the completed build's verified `image/system`. Both
`usr/bin/busybox` and `usr/bin/rclone` must be present in the final verifier's
products with exact bytes/modes/root-local link chains. Root's verifier9e1ff0ef
added BusyBox for this input. Host-executed paths must resolve to those exact
root-local files, never follow an image absolute symlink into the host.

Concrete proposed commands (do not run before root allocates):

```bash
TASK_SOURCE=/tmp/pix-m7-baseline-continuation-20261014
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
TASK_VERIFY=/workspace/tmp/pix-m7-image-readback-20261014-01/artifacts
TASK_OWNER=/workspace/tmp/pix-m7-final-baseline-20261014-01
TASK_BUILD="$TASK_TREE/build.pixelelated-GENERIC_X64.x86_64"
TASK_ES=/home/max/Development/emulationstation-next.worktrees/qa-integration
TASK_RA="$TASK_BUILD/build/retroarch-bdba046fa6766380bc2457532f38e589df769aaf"

python3 -I -B "$TASK_SOURCE/prepare.py" \
  --checkout "$TASK_TREE" --verification "$TASK_VERIFY/result.json" \
  --system-root "$TASK_BUILD/image/system" --es-source "$TASK_ES" \
  --retroarch-source "$TASK_RA" \
  --baseline /workspace/artifacts/rocknix-images/walk-baseline \
  --owner "$TASK_OWNER"
cd "$TASK_TREE"
tools/host-maintenance/retention-report --plan "$TASK_OWNER/retention-plan.json" \
  --output "$TASK_OWNER/retention-report.json"
tools/host-maintenance/build-admission prepare --plan "$TASK_OWNER/admission-plan.json" \
  --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --admission "$TASK_OWNER/admission.json" --activity-dir "$TASK_OWNER" --recursive-activity -- \
  python3 -I -B "$TASK_OWNER/run.py"
```

The published ES checkout must remain at the verifier's pin; the preparer and
owner check tracked cleanliness and exact HEAD. No source overlay is used. The
shown RetroArch source is the actual current build source; its wrapper is bound
immutably and passed directly through `RETROARCH_SRC` so another worktree cannot
win the helper's fallback search. No baseline is regenerated or accepted.
Supervise `lifecycle-owner/console.log`, `records/resources.jsonl`, original
stage `.exit.json` files and each `artifacts/BACKEND/rocknix-images/qa-*/report.md`.
No current final-image standard rows exist to skip at preparation time. If an
original run later produces accepted same-image rows, retain them and use the
existing `vm-qa --only` follow-up mechanism for an actual failed remainder;
do not rerun already accepted rows or make this new adapter a repeat gate.

After actual completion and launcher/runner/monitor results exist:

```bash
TASK_RUN=$(cat "$TASK_OWNER/run.path")
TASK_EXPORT=/workspace/tmp/pix-m7-final-baseline-export-20261014-01
python3 -I -B "$TASK_OWNER/close.py" --owner "$TASK_OWNER" \
  --run "$TASK_RUN" --output "$TASK_EXPORT"
# Root reviews original reports/frames/TTP/restoration/status and actual cleanup.
# This never runs implicitly in close.py.
tools/host-maintenance/build-admission consume --run "$TASK_RUN" \
  --evidence "$TASK_EXPORT/consumption-draft.json"
```

`close.py` exports a verified lossless archive of compact originals, source/input
identities, all suite logs, report tables and frames. It excludes disks, private
SSH keys, cloud state and host fixture temporary data. It requires actual owner,
QEMU/backend/child closure; it neither claims acceptance nor consumes admission.
A failed aggregate remains failed even if some rows passed. After review and
consumption, retire only this owner's pair/runtime/tmp/cloud scratch with the
existing owner-scoped procedure; protect firmware, readback, build/system and
accepted baseline. This packet adds no RC acceptance criteria or provider gate.
