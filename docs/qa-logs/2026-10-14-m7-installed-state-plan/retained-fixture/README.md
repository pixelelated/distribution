# Executable retained-state and installed-backup fixture — #565 / #566

Additive subpacket of the installed-state plan at c912913fc81fddfae7b3d4a1760c8290f021a40f.
All eight original parent files and their seal remain unchanged. This packet is
source-only: no preparation reader, fixture, service, VM, update, reboot, device
operation, compiler, provider or test runtime was executed. AST and shell syntax
checks are not a behavioral PASS. Integrate only this new commit's files; do not
merge its older branch ancestry after the coordinator's citation metadata remap.

The scripts close the previously missing *executable fixture plumbing*. Root
still owns the actual one-guest allocation, clean-image gate, old→new update,
source/ELF custody, observed results and retirement. They do not replace #566's
separate actual compiled UI/error fixture or claim provider authentication.

## What executes

- `prepare.py`: host reader. Takes the actual frozen distribution and final
  SYSTEM plus its accepted SHA256. Verifies SYSTEM before/after, exact installed
  BUILD_ID, GENERIC_X64 identity and installed backuptool/source equality. Reads
  actual installed ES and hashes it. Resolves ES pin from the distribution's
  recipe, so the pending 3178b832… repair (or its final reviewed successor) is
  selected dynamically, with no stale a5c pin in execution. Emits four serial
  shell scripts and `bindings.json`; does not launch them.
- `guest-fixture.py`: only disposable QEMU/KVM GENERIC_X64. Four phases below.
  Imports the complete unchanged, hash-bound `pixelelated-state-check` as a
  module and calls its actual `first_boot_ready()` and parsers. No extracted or
  weakened readiness function and no obsolete `is-active autostart` shortcut.
- `run-phase.sh`: existing vm-serial transport, bounded and hash-bound to the
  prepared input. Saves serial output, original transport return and stderr.
- `collect.py`: requires transport 0, exactly one original guest exit marker 0,
  exactly one matching JSON PASS and every mandatory assertion. Transport
  completion alone never passes. Original watcher/runner/launcher exits and
  actual process exit still belong to root's ordinary watched lifecycle.

The predecessor is the accepted replacement20 image from the parent plan:
full distribution `1a026648442321609b2288c2c9c06803817f9df2`, ES c8dc72cf…,
installed ES SHA db136580f0a46442bb3fe7ac9e31606b38b816c78efc8f9b4e267284daca6502.
The current final image identity is read from SYSTEM, not supplied as a guessed
pin. Its BUILD_ID must equal the frozen checkout's full HEAD. The selected
state-checker, serial tool and backuptool source must still match the reviewed
hashes in source-bindings.json; changed contracts require a new reviewed packet.

## Four serialized phases

1. **seed**, on a fresh replacement20 guest: verify predecessor BUILD_ID and ES,
   actual QEMU vendor, full current-boot readiness and the actual clean first-boot
   state policy. Refuse populated account fields, existing fixture paths,
   existing activity stamps, custom backup configuration or an existing owner.
   Stop the one active frontend unit (`essway` or `emustation`), wait for ES exit,
   and write synthetic RA username/password/token/key, distinct ScreenScraper
   player and fallback developer fields, a harmless marker, explicit Recent
   collection choice, two valid historical operation stamps, an inert GB stub
   and gamelist, and a PPSSPP token-only file. Cloud startup/game-exit sync and
   achievements/proxy remain off. Restart the same frontend in `finally`, verify
   readiness, account/history equality and real ES API Recent membership. Never
   launch the stub. Record the positive seed receipt before any update.
2. **before**, on the same predecessor boot: reassert every selected field,
   exact stamp/stub/token bytes, loaded gamelist/Recent and retained-mode policy.
   Emit a before receipt bound to the seed and candidate identity. The checker
   only inspects, and its default payload is still held to clean policy.
3. **after**, only after root stages the exact accepted tar and completes the
   actual update/reboot: require changed boot ID, exact candidate BUILD_ID,
   installed and executing ES hash, real readiness and empty update queue.
   Reassert all selected synthetic accounts, history and activity, plus loaded
   Recent and the actual retained-mode policy. Existing config default additions
   are allowed; selected values and file bytes under test cannot change.
4. **backup**, on the accepted candidate boot: require the after receipt and
   exact installed backuptool source hash, default backup path, no custom list
   and no prior top-level backup archive. Stop ES for a stable comparison. Run
   actual `/usr/bin/backuptool backup` exactly once; record its original child
   return separately. Inspect the one new real archive without extraction.
   Restore frontend and readiness in the normal/failure cleanup path.

The ES XML writer deliberately emits one setting per line (ElementTree indent),
matching the real backuptool line-strip contract. A single-line synthetic config
would make password filtering remove unrelated fields and would be an invalid
fixture. System config edits preserve unrelated lines and mode, use an exclusive
sibling temporary then replace, and fsync before restart. Existing unrelated
account state is never borrowed. The owned private state directory is
`/storage/.cache/pixelelated-installed-state-<id>`; its reports/marker identify
which phase ran. Failed attempts remain there; no automatic retry or deletion.

## Exact backup assertions

Use the ordinary installed default LOCATIONS, not a rewritten backuptool or shim.
The new filename must follow the existing `…-ROCKNIX_SETTINGS.tar.gz` persisted
contract. All members must be unique regular files/directories under `storage/`,
without traversal or links; inspect at most 4096 members, 16 MiB per member and
256 MiB expanded data. Require both actual system.cfg and es_settings.cfg members.

- RA username, ScreenScraper username and fallback developer ID travel, as the
  existing export contract specifies. Passwords, RA key/token and ScreenScraper
  developer password do not. This does not misclassify retained usernames as
  secret leaks or demand a different export policy.
- The harmless marker and explicit Recent choice remain in the archived config.
- The actual PPSSPP token-only file is held back; every regular member is checked
  in memory for all planted secret sentinels, so another copy cannot pass.
- All selected runtime config/history/stamp/token bytes stay exactly unchanged
  by backup while ES is stopped. After restart, selected values and actual
  loaded Recent are rechecked. There is no cloud upload or restore in this phase.

Only booleans, counts, phase names and fixed error codes reach public stdout.
No account value or account-value digest is emitted. Code/ELF/artifact hashes
remain ordinary source custody. Child backup stdout/stderr are retained privately
inside the fixture directory and are not printed or copied into public evidence
by these tools. Never run against a real device or owner account.

## Commands for root after final artifacts exist

Preparation needs the host's existing unsquashfs. Final SYSTEM must already be
bound to the accepted actual update/install artifacts by the image verifier.
`--output` must not exist; preparation uses only bounded readers and small files.

```bash
TASK_PACKET=/workspace/repos/rocknix.worktrees/m7-candidate-compose/docs/qa-logs/2026-10-14-m7-installed-state-plan/retained-fixture
python3 -I "$TASK_PACKET/prepare.py" --checkout "$TASK_TREE" --system "$TASK_SYSTEM" --system-sha256 "$TASK_SYSTEM_SHA" --output "$TASK_PREPARED" --id m7-retained-20261014-01
```

Boot the accepted predecessor with one fresh owned disk, after retiring conflicting
guests. Use its serial console; no SSH key or provider login is needed by these
phases. For each phase allocate a different watched owner and submit:

```bash
tools/watch-build-submit --owner "$TASK_PHASE_OWNER" -- --record-only --activity-dir "$TASK_PHASE_OWNER" -- bash "$TASK_PACKET/run-phase.sh" "$TASK_TREE" "$TASK_PREPARED" "$TASK_PHASE_OWNER" "$TASK_SERIAL" seed
# Consume original results before the same command with phase `before`.
# Root then stages the accepted update tar and invokes actual sync/reboot.
# Reacquire the same guest's serial endpoint; run `after`, consume, then `backup`.
```

Do not run `after` on the fresh candidate VM or a bind-mounted overlay: exact
predecessor/candidate identities, seed/before receipts and changed boot are
mandatory. The scripts intentionally do not stage an update, choose a VM port,
reboot or own the guest. Those already belong to root's allocated update runner.
Root must verify the update tar hash before staging. No old owner or retired
rehearsal command is reused. Each phase is single-use because its receipts and
host outputs are exclusive. On failure consume the original result and inspect
its fixed stage/error; do not rerun over the partial state to manufacture PASS.

Guest outer bounds: seed 300 s, before/after 180 s, backup 420 s; kill grace 10 s.
Host transport bounds: 340/220/220/460 s plus 10 s grace. Readiness polls at most
70 s per call using real unit execution and mounts; ES API idle waits 30 s.
Service commands have 30 s limits. Backup child is a private process group with
180 s timeout, 5 s TERM grace then bounded KILL/wait. Its per-file write limit
is 256 MiB. Archive inspection has the caps above and lives inside the overall
phase deadline. Preparation readers have 120 s limits and output caps.

Use the existing standard 4-vCPU/8-GiB/16-GiB+ disposable guest. Allow 1 GiB
additional fixture/backup scratch and monitor actual free space with the existing
owner; this is an operating allowance, not an in-script global disk quota or a
measured peak. Root's outer timeout must still supervise the original VM process,
which a transport timeout does not stop. After compact phase/policy/identity
reports and original exits are accepted, retire the exact disk/UEFI/private
fixture and backup archive with that guest's owner. No physical device cleanup.
