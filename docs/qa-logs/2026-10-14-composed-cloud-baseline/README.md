# Final-image cloud baseline continuation — source only, UNRUN

No new #349 gate or adapter is needed. Its installed same-model/newest and
foreign-only proof is already accepted on replacement19, with complete19→20
installed byte applicability. The only unchecked #349 item is the public
explanation tracked by #511. Keep those original results and checkboxes intact.

At final distribution d6a87f05c1935516115b2cca1af22151a0209224 and ES
3178b832b8d134198b2b4eede4f725d4ed283f8c, the cloud package differs from
replacement19 only in cloud_oauth's phone/sign-in presentation. The package
recipe, cloud backup/restore/scan/archive selection, rules/defaults, backuptool,
cloud-round-trip and cloud-test-backend are unchanged. ES's cloud scan/options/
restore region and CloudText/GuiCloudTransfer sources are unchanged; GuiMenu's
cloud changes are in OAuth presentation. This is source applicability, not a
claim that the future SYSTEM or ES ELF is identical. Final artifact verification
must retain actual installed identities. No new #349 archive/frame replay follows
from these unrelated deltas. Phone/sign-in qualification remains in its own lane.

The already planned whole-image baseline can reuse the installed single-device
round-trip suite. Run it once each for WebDAV, SFTP and local MinIO/S3 on the
clean-image QA guest, and once for WebDAV on the genuinely updated retained guest
if that retained baseline has not already run. Do not repeat an accepted same-image
row. Do not add pair, LINK, KILL, real accounts, providers, game launches, or another
same-model/archive fixture campaign. These four rows are the existing image
qualification sequence, not reopened #349 criteria.

Accepted command/evidence ancestry:

- docs/qa-logs/2026-10-11-pixelelated-replacement-19/qa-plan/run.py:
  standard WebDAV plus --only round-trip for SFTP and S3. Each round trip has108
  PASS assertions. Original WebDAV84s, SFTP68s, MinIO/S3 115s. The original full
  standard aggregate is1 for separately resolved suites; retain that outcome.
- The same packet's retained/artifacts/rocknix-images/
  qa-a0f60255ab-webdav-a-20261011-1841/report.md: retained round-trip83s, PASS.
- docs/qa-logs/2026-10-11-installed-ui/ui19e/settings-proof.py and its artifacts:
  installed writer/upload, same-model selection/download SHA, foreign-only
  disabled presentation/preservation. No rerun proposed.
- docs/qa-logs/2026-10-11-pixelelated-replacement-20/
  pixelelated-m7-image20-compare/review.json:61,309 installed entries; only six
  identity/rocknix-info/factory-shadow paths changed, modes unchanged.

Commands below are for the coordinator's existing admitted watched owner, after
clean-before-seeding and retained update checks. They are not a VM launch script.
The coordinator binds IMAGE to the verified final img.gz, OWNER to a fresh private
run directory, VM_PAIR_DIR to this guest's existing qa-key directory, and
VM_QEMU_RUNTIME_DIR to its actual runtime directory. Guest a uses SSH10022. Its
user-mode NIC must reach host loopback at10.0.2.2; QA SSH is injected only after
clean-state evidence as already planned. The no-NIC installed588 lifecycle is
incompatible as-is; do not call vm-qa without --skip-up and accidentally boot a pair.
A later admitted one-guest networked continuation suffices.

```bash
TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
SYSTEM="$TREE/build.pixelelated-GENERIC_X64.x86_64/image/system"
cd "$TREE"
export CLOUD_QA_STATE="$OWNER/cloud"
export CLOUD_QA_BIND=127.0.0.1 CLOUD_QA_GUEST_HOST=10.0.2.2
export CLOUD_QA_USER=qauser CLOUD_QA_PASS=qa-password
export CLOUD_QA_NAME="pix-m7-cloud-$(basename "$OWNER")"
export ROCKNIX_ARTIFACTS="$OWNER/artifacts" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$OWNER/bin"
ln -s "$SYSTEM/usr/bin/rclone" "$OWNER/bin/rclone"
export PATH="$OWNER/bin:$PATH"
# The host rclone selection above follows qa19. It is not a guest PATH overlay.
# Bind a reviewed cached MinIO image ID/digest before the S3 command:
: "${CLOUD_QA_IMAGE:?set to the exact cached MinIO image ID or digest}"
export CLOUD_QA_IMAGE

# Clean image: submit each as a separate observed stage, stop on first failure.
tools/vm-qa --skip-up --only round-trip --backend webdav "$IMAGE"
tools/cloud-test-backend --backend webdav down
tools/vm-qa --skip-up --only round-trip --backend sftp "$IMAGE"
tools/cloud-test-backend --backend sftp down
tools/vm-qa --skip-up --only round-trip --backend s3 "$IMAGE"
tools/cloud-test-backend --backend s3 down

# Retained owner only, on its genuinely updated guest and fresh own backend state:
tools/vm-qa --skip-up --only round-trip --backend webdav "$IMAGE"
tools/cloud-test-backend --backend webdav down
```

Run each vm-qa stage under the existing owner's300-second work bound, with an
additional30-second bounded cleanup allowance, original child wait status and a
separate timed_out field. The accepted rows took68–115seconds;300 is a proposed
fixture ceiling, not a measured new result. Keep the already allocated VM RAM/
CPU/disk bounds, output guard and actual process cleanup; no new product cap or
controller requirement. Four rows fit a20-minute work reservation excluding
VM preparation/real update. Preserve the original rc and any timeout/cleanup
failure independently. Do not use `timeout`'s124 as an invented child exit.

vm-qa starts the chosen backend itself and does not stop it. Always issue the
matching down in the owner's finally path, including failures. The existing
cloud-round-trip SSH ControlMaster persists120seconds; explicitly close that
run's connection before final owner census:

```bash
ssh -o ControlMaster=auto -o "ControlPath=/tmp/crt-$(id -u)-%C" \
  -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  -i "$VM_PAIR_DIR/qa-key" -p10022 -O exit root@127.0.0.1
```

An already absent master is a cleanup observation, not a suite failure. Backend
down alone is not proof of process exit: retain exact owned PID birth identities
or container identity and verify gone. Stop the VM through its existing owner
and pidfile. No broad process-name kill, shared default backend state or reused
container name. The driver restores prior remote/active selection/path settings
in finally and removes its scratch fixture; cleanup errors print WARN without
necessarily changing its final rc. Preserve/check those messages and actual
cleanup before accepting the owner, rather than promoting PASSED alone.

Data are synthetic: /storage/cloud-qa saves/states, excluded ROM stubs, tiny
settings tar and temporary /storage/roms/vectrex{,-unselected} content. The suite
also exercises actual installed settings restore against its qa-suite member.
Its backend paths come from cloud-test-backend, not hand-coded root assumptions:
SFTP uses an absolute owner data path and S3 uses a bucket prefix. No --real-roms,
--keep, --path-prefix, --second-port, --only fixture IDs, --link or --kill. Note:
cloud-round-trip --only skips this baseline; vm-qa --only round-trip selects it.

Retain compact originals: each owner's image/boot identity and installed binding,
argv/environment with synthetic values, backend identity/capabilities, original
stage/launcher/cleanup statuses, vm-qa report.md and round-trip.log, backend logs,
final process/container census. Paths are
$ROCKNIX_ARTIFACTS/rocknix-images/qa-<BUILD_ID first10>-<backend>-a-<UTCminute>/.
Count108 PASS lines and final PASSED without FAIL/WARN cleanup, while retaining
original output. Use separate owner artifact roots for clean versus retained to
avoid minute-based report collisions. No new screenshots are needed for this
nonvisual baseline.

Remaining launch facts, not product failures:

1. Final image/SYSTEM/build acceptance receipt is still pending. Bind the cloud
   installed members in installed-bindings.json to verified final SYSTEM bytes,
   plus actual rclone version/hash and final ES source/native identity. This
   source packet does not assert final installed equality.
2. The accepted local S3 is the existing MinIO implementation, not a new rclone
   S3 or substitute service. Historical retained reports do not pin its image
   digest. cloud-test-backend defaults to quay.io/minio/minio:latest; before
   allocation, read the cached image identity and pass CLOUD_QA_IMAGE explicitly.
   No pull or provider change is proposed. Cached image existence was not tested
   during this source-only handoff.
3. Reuse/provision the admitted networked guest's QA SSH channel and verify only
   these owned loopback ports are free:9010 WebDAV,9012 S3,9013 SFTP. Keep9011
   deliberately unbound for the suite's failure path. Host sshd and rclone paths
   exist; no service was launched or dependencies executed for this packet.

No runtime, VM, backend, service, container, compiler, external account or product
change occurred. The packet is source-only and UNRUN.
