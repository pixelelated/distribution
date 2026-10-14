Canonical sealed source is stored byte-for-byte in `source-originals.tar.gz` to preserve unified-diff context whitespace. Extract into a fresh private directory and verify SHA256SUMS before using that directory as TASK_CORRECTION. `source-storage.json` binds both archive and original manifest. The following is the original source guide.

# Installed-state execution correction — source-only, UNRUN

The existing parent and retained child are compatible with final ES
3178b832b8d134198b2b4eede4f725d4ed283f8c. Their seven-file seals match, as do the
execution-bound state checker, serial tool, backuptool and existing SDK mcopy.
The ES change touches error guidance/catalogs, not settings persistence or the
local API used here. `prepare.py` reads the final distribution package pin; it
does not execute its historical a5c observation. Default boot uses the unchanged
state checker's real successful autostart execution, mounts and live ES, with
no cgroup requirement or private boot flag. Compilation is independent of this
post-image work.

One deterministic failure-receipt defect was found: retained
`guest-fixture.py:319` replaces the actual backup child exit after TERM/KILL with
124. The supplied patch saves each actual wait result and records `timed_out`
separately. A timeout remains FAIL even if the child subsequently exits zero.
The 180-second wait, 5-second TERM/KILL waits, process-group signaling, file cap,
archive checks and success path are otherwise unchanged. No claim is made about
an unobserved exit if signaling/wait itself raises. Original parent/child files
and seals are untouched; materialize a fresh derivative and retain their seals.
No preparer, post-check, fixture, backup or VM has run in this lane. Validation
was source reading, hashes and AST only; do not treat this as behavioral PASS.

`check-shared-identity.py` implements the parent's already documented #566
postcondition. Generic `payload-check.sh` verifies clean policy but intentionally
does not require a positive approved compiled pair. The new reader checks both
original payload reports: actual ES has a positive approved shared identity count
and zero unapproved developer identities. It prints counts only. This adds no new
product gate and does not replace the actual compiled UI/URL evidence.

## Exact sequence after final image, under root's allocations

Use the coordinator packet location and the actual clean, frozen final build
checkout. The old README's m7-candidate-compose path is historical. Define
TASK_CORRECTION as this content-carried correction directory. All owner/output
paths are fresh; shell variables below come from the real build custody record.

```bash
TASK_PLAN=/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-14-m7-installed-state-plan
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
# Root supplies TASK_CORRECTION, final artifact paths/hashes and fresh owners.
cd "$TASK_TREE"
tools/watch-build-submit --owner "$TASK_PAYLOAD_OWNER" -- --record-only --activity-dir "$TASK_PAYLOAD_OWNER" -- bash "$TASK_PLAN/payload-check.sh" "$TASK_TREE" "$TASK_PAYLOAD_OWNER" "$TASK_UPDATE" "$TASK_UPDATE_SHA" "$TASK_IMAGE" "$TASK_IMAGE_SHA"
# Wait for and consume original payload/runner/launcher exits, then:
python3 -I -S -B "$TASK_CORRECTION/check-shared-identity.py" --update "$TASK_PAYLOAD_OWNER/update.json" --install "$TASK_PAYLOAD_OWNER/install.json"
```

Retain that reader's original exit and JSON under the same reviewed execution
receipt. Payload deadline remains two sequential 600-second readers plus grace
and artifact hashing. Its passing report is not a new guest's clean boot proof.

Boot a fresh candidate with the ordinary guest profile. Before keys, accounts,
ROM metadata or other intentional state, run:

```bash
"$TASK_TREE/docs/qa-logs/2026-10-13-clean-state-565/run-first-boot.sh" "$TASK_CLEAN_OWNER" "$TASK_SERIAL"
```

Require original transport/runner exits, exactly one PIX_STATE_565_RC=0, JSON pass
and present/clear ready row. Retain the actual final install/SYSTEM/guest identity
chain separately. Then retire or separately own that fresh guest; retained upgrade
uses a fresh replacement20 disk, not this candidate disk or a retired owner disk.

Prepare the corrected source derivative and four serial scripts:

```bash
python3 -I -S -B "$TASK_CORRECTION/materialize.py" --original "$TASK_PLAN/retained-fixture" --output "$TASK_DERIVATIVE"
python3 -I "$TASK_DERIVATIVE/prepare.py" --checkout "$TASK_TREE" --system "$TASK_SYSTEM" --system-sha256 "$TASK_SYSTEM_SHA" --output "$TASK_PREPARED" --id m7-retained-20261014-01
```

`TASK_DERIVATIVE` must be fresh under /tmp or /workspace/tmp. The materializer
requires the exact old seal/source, applies only the bound patch with zero fuzz,
checks the exact resulting source hash, and keeps original seal, patch rc/stdout/
stderr plus a new derivative seal. Its source preparation does not start a guest.
The next preparer requires clean frozen checkout, SYSTEM BUILD_ID equal to its
full HEAD, installed backuptool equal to source, and dynamic ES pin/hash.

Root boots the accepted replacement20 image (SHA
1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490), fresh disk,
ordinary boot. After readiness, run one phase per new watched owner:

```bash
# TASK_PHASE is seed, then before; later after, then backup. Consume each original
# result before advancing, never loop blindly over this list.
tools/watch-build-submit --owner "$TASK_PHASE_OWNER" -- --record-only --activity-dir "$TASK_PHASE_OWNER" -- bash "$TASK_DERIVATIVE/run-phase.sh" "$TASK_TREE" "$TASK_PREPARED" "$TASK_PHASE_OWNER" "$TASK_SERIAL" "$TASK_PHASE"
```

The seed phase itself requires clean predecessor state before any seed. It stops
and restarts the actual frontend; RA and cloud automation stay off. `before`
rechecks accounts, exact token/history/stamp bytes and real loaded GB/Recent API
membership. Root then stages the independently hash-verified actual update tar
through its allocated media/transport, verifies staged SHA, syncs/reboots, and
records the real updater outcome. The fixture intentionally performs no update
or reboot. `after` requires prior receipts, changed boot ID, exact new BUILD_ID,
installed/executing ES hash, actual readiness, empty update queue and preserved
selected state. A filesystem overlay is not a substitute for this custody chain.

The backup phase runs installed backuptool once and inspects the real archive:
RA password/token/key, both ScreenScraper passwords and PPSSPP token are absent;
user identifiers, fallback developer ID, harmless setting and Recent selection
remain. It scans every bounded regular member for planted secret sentinels,
rejects links/traversal, preserves selected runtime bytes while ES is stopped,
then restores frontend/readiness/loaded Recent. This exercises default LOCATIONS;
custom-list Dolphin/proxy exclusions and cloud restore remain their existing
separate evidence. No provider or real account is needed.

Phase guest ceilings stay 300/180/180/420 seconds; host transport ceilings
340/220/220/460 plus 10-second grace. The separate full-VM owner must cover actual
boot/update plus all serialized phases, not reuse a 900-second UI allocation.
Transport timeout cannot retire the VM or guarantee cleanup of a child process
that made its own session; root's existing bounded VM lifecycle remains required.
No new guest/helper is supplied by this small correction. Use current admitted
transport and staging; the e483 in-tree generic launcher has no --no-network flag.

Remaining facts are actual final build/SYSTEM/custody, fresh clean and retained
runtime receipts, backup archive result and owner retirement. No further
source-level blocker to those commands was found. Source compatibility is not
image acceptance or an RC designation.
