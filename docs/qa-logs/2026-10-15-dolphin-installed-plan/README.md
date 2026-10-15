# Pending final-image installed Dolphin proof — #584 / #592

SOURCE ONLY, UNRUN. The new firmware has not been built or read back. This packet is ready for coordinator review; it is not an admission, prepared owner, build, installed-image result or test PASS. The parent owns product changes, final image custody, allocation, runtime, acceptance and issue updates.

Can this be done on the VM? Yes. Installed Sys resolution, local startup login, client initialization/shutdown and clean process exit need no physical device. Put this answer and the three rows below on the existing issues before allocation. This is a fresh no-NIC guest running the final installed executable. There is no real account, authentication success, award, network provider, gameplay, renderer or handheld claim. Root's separately owned clean/retained composition and native gameplay plans remain separate acceptance work.

## Exact scope and retained controls

Derived from `/tmp/m7-dolphin-ra-runtime-plan-20261015`, whose seven runtime/export scripts were byte-compared with the executed source in `docs/qa-logs/2026-10-15-dolphin-startup-result/startup/original-records.tar.gz`. `originals/original-runtime-sources.tar.gz` retains those seven exact sources losslessly; `originals/runtime-source-members.json` binds each decompressed member. The remaining preparation/provenance originals stay under `originals/`. The guest proof diff is losslessly compressed as `guest-proof.py.diff.gz`. The prior four-case result and known-bad baseline remain historical evidence; they are not rerun. The previous candidate's original three stderr files each contain all four badge-load failures, retained under `evidence/prior-stderr/`.

The runtime always launches `/usr/bin/dolphin-emu-nogui`; executable hash and actual `/proc/PID/exe` are checked for both live-core rows. No candidate binary or resource bytes are staged, copied or mounted into the guest. `inputs.json.staged` must be empty. The existing executable tmpfs still holds only private configuration, logs and a self-authored 0x104-byte GameCube branch-to-self DOL. This DOL establishes a CPU thread and advancing ticks for two seconds; it is not gameplay evidence.

| Case | Original exit | Required evidence |
| --- | --- | --- |
| `installed-enabled` | 0 after ordinary SIGTERM | Live CPU and advancing ticks; one initialization, one shutdown, exactly one synthetic POST `/dorequest.php` to loopback port 8080 |
| `installed-disabled` | 0 after ordinary SIGTERM | Live CPU and advancing ticks; no initialization, shutdown or HTTP request |
| `installed-failed-boot` | 1, no normal stop signal | Deliberately absent `.iso`, original BootCore error, one initialization/shutdown pair; zero or one synthetic request because early shutdown may cancel the queue |

The endpoint, HTTP request/form/destination checks, socket deadlines, pidfd signals, subreaper, child start identities, live CPU interval, native census and forced-cleanup failure rules are retained. All requests use the original synthetic invalid user/token and receive the original failed-login response. No service is installed. A case failure stops the family with no retry. Original result and stderr/stdout channels remain unmodified.

Every case independently rejects all four original stderr messages: default player, game, unlocked achievement and locked achievement badge failed to load. This yields twelve case/message observations, supported by positive startup evidence and actual resource hashes rather than error absence alone. `close.py` recounts the original retained stderr, preserving bytes including original NULs. Presence of ApprovedInis.json and GMSE01.ini proves installed path/byte availability only; no successful approved-settings application or game-specific behavior is claimed.

## Required new-image and source bindings

Preparation has no default commit or final hash. It requires full `--source-commit`, `--coordinator-commit`, `--es-commit`, `--image-sha256`, `--verification-sha256`, `--verification-inputs-sha256` and `--installed-executable-sha256`, plus the new frozen checkout and final readback directory. It rejects the old fac608ff source and known-bad installed executable. The supplied values must match the actual final readback, identity sidecar, source HEAD and installed executable. The admitted lifecycle rechecks the full compressed-image SHA and both source HEADs before boot; the guest's BUILD_ID and executable bytes must match.

The preparer binds the reviewed 84-file Dolphin package inventory, including package.mk SHA `cc4e7458e99329518b30b7f78aa38e149d083427f3c8b7e22d7f5e1090d2479b` and patch018. It requires the new build's MainNoGUI.cpp SHA `fcf6416ddeb39878e77ec8967e26e5805fedafec2b2c1c21d049d8054787ae8e`, the qualified lifecycle source. Any changed recipe/patch/default inventory requires reviewed source rebinding, not a weakened assertion. Build/source provenance is retained in `records/installed-source-basis.json`; this plan does not compile anything.

`resources.json` and `pinned-data/` retain six exact upstream Data/Sys blobs, 38,905 bytes, verified by `git show 6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4:<source-path>` against the former unpacked source. The final build must retain that exact pin and those bytes. The final artifact verifier must include these products rows:

- `usr/share/dolphin-emu/sys/Resources/achievements_player.png`
- `usr/share/dolphin-emu/sys/Resources/achievements_game.png`
- `usr/share/dolphin-emu/sys/Resources/achievements_unlocked.png`
- `usr/share/dolphin-emu/sys/Resources/achievements_locked.png`
- `usr/share/dolphin-emu/sys/ApprovedInis.json`
- `usr/share/dolphin-emu/sys/GameSettings/GMSE01.ini`

Use the existing final-image verifier's staged `image/system` versus extracted SYSTEM equality and link-chain comparison. No new image reader is supplied here. Each product row must have the pinned bytes/hash, mode `-rw-r--r--`, and exactly `links=[{"path":"/usr/share/dolphin-emu/sys","target":"../../config/dolphin-emu"}]`, resolving to `/usr/config/dolphin-emu/<suffix>`. Preparation additionally reads those actual staged paths and the final unpacked Data/Sys files. The guest reads both alias and resolved paths on the read-only filesystem before/after all cases and retains actual mountinfo. It rejects direct resource/executable overlays and resource-path/hash changes. Unrelated mount-table changes are recorded but do not turn this narrow product check into a global mount-stability test.

The known no-NIC helper is bound separately from firmware source: `/workspace/repos/rocknix.worktrees/m7-offline-vm-567/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm`, SHA `5b058ed8a8b11135cd5997e3d925939baff30726033125acf1244863a756318d`, adjacent profile SHA `26c420ecb0cc7aae29050554c55f522e62337cf6726619a59337c073f1c65406`. Its original generated and actual argv from the successful Dolphin startup owner are retained. Runtime requires `-nic none`, no netdev/host forwarding, exact generated/actual argv equality, 8192 MiB and four CPUs, and guest interfaces `['lo']`. Do not silently use an older frozen helper lacking `--no-network`.

## Coordinator launch sequence after final readback

The following is pending, not executed. Root supplies actually observed full identities from the completed build/readback, an unused fresh owner and a currently free VNC port. These environment variables must be set; there are no old-image fallback values.

```bash
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-player-setup
TASK_PACKET=/tmp/pix-m7-dolphin-installed-plan-20261015
: "${TASK_FROZEN:?new frozen checkout required}"
: "${TASK_VERIFY:?new completed final readback directory required}"
: "${TASK_VM:?fresh /workspace/tmp/pix... owner required}"
: "${TASK_FINAL_COMMIT:?full final source commit required}"
: "${TASK_COORDINATOR_COMMIT:?full coordinator HEAD required}"
: "${TASK_ES_COMMIT:?full final ES commit required}"
: "${TASK_IMAGE_SHA:?final compressed image SHA256 required}"
: "${TASK_VERIFY_SHA:?final result.json SHA256 required}"
: "${TASK_VERIFY_INPUTS_SHA:?final inputs.json SHA256 required}"
: "${TASK_DOLPHIN_SHA:?final installed executable SHA256 required}"
: "${TASK_VNC:?observed-free VNC number 100 through 199 required}"
python3 -I -S -B "$TASK_PACKET/prepare-vm.py" \
  --checkout "$TASK_TREE" --frozen-checkout "$TASK_FROZEN" \
  --verification "$TASK_VERIFY" --owner "$TASK_VM" --vnc "$TASK_VNC" \
  --source-commit "$TASK_FINAL_COMMIT" --coordinator-commit "$TASK_COORDINATOR_COMMIT" \
  --es-commit "$TASK_ES_COMMIT" --image-sha256 "$TASK_IMAGE_SHA" \
  --verification-sha256 "$TASK_VERIFY_SHA" --verification-inputs-sha256 "$TASK_VERIFY_INPUTS_SHA" \
  --installed-executable-sha256 "$TASK_DOLPHIN_SHA"
cd "$TASK_TREE"
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$TASK_VM/retention-plan.json" --output "$TASK_VM/retention-report.json"
# Review and consume original retention report/watcher channels and capacity.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$TASK_VM/admission-plan.json" --output "$TASK_VM/admission.json"
tools/watch-build-submit --owner "$TASK_VM/lifecycle-owner" -- \
  --activity-dir "$TASK_VM/logs" --admission "$TASK_VM/admission.json" -- \
  python3 -I -S -B "$TASK_VM/vm-lifecycle.py"
# Supervise actual original run, inspect within 60 seconds, then retain every final channel.
# Export only after every exact owner/process is absent; do not assume submission means success.
: "${TASK_RUN:?actual coordinator .build-runs path required}"
: "${TASK_EXPORT:?fresh /workspace/tmp/pix... export packet required}"
python3 -I -S -B "$TASK_VM/close.py" --owner "$TASK_VM" --run "$TASK_RUN" --packet "$TASK_EXPORT"
```

The final acceptance is coordinator review of originals: all launcher/wrapper/command/watcher/guest/export channels; per-case exit, exact request and process evidence; final image/source/resource bindings; exact QEMU and child absence; unmounted media and retained manifest equality. `close.py` never marks the run accepted, consumes admission or deletes media. Preserve any failure and its original channels. Do not rerun automatically.

## Bounds, custody and remaining dependency

Unchanged qualified allocation: one guest, 8 GiB RAM, four CPUs, no NIC, 16 GiB guest disk, two 256 MiB media files. Host work 1200 s, separate cleanup 120 s; serial guest command 240 s plus original 15 s transport envelope. Guest case family 180 s work, 10 s cleanup and 20 s export, 210 s owner. Each live case has 15 s startup, two seconds positive CPU observation and eight seconds ordinary shutdown; failed boot has eight seconds. Loopback connection timeout two seconds, endpoint close three seconds; exceptional process cleanup three seconds and always fails acceptance. Existing per-command output and compact export bounds remain. Capacity forecast is conservative 32 GiB raw/disk ceilings plus 512 MiB media and 64 MiB staging, not allocated usage. No compiler, old baseline or broad matrix is included.

Old-cache consumer closure: all six resource blobs and needed source snippets were copied before the parent's cache move. This agent has no live child/import/owner, no open old-cache file, and no remaining read dependency on `m7-p5-build-20261014-02/build.pixelelated-GENERIC_X64.x86_64`. Future preparation reads only the explicitly supplied NEW frozen checkout/readback and owns fresh output. Historical paths inside `originals/` or provenance are records, never active inputs. The old cache may move or be scoped-cleaned without racing this packet's preparation.

The final image, final installed executable hash, final source commit/readback and allocated owner are PENDING. Static parsing and source comparisons in `static-review.json` do not qualify runtime imports, resources, gameplay, a build, or a VM. The package's default-data symlink changes immutable SYSTEM only; it does not migrate or modify existing `/storage` configuration. This fresh-guest check leaves root's affected retained/clean-install composition proof outstanding.

## Source-only secret-pattern correction

The normal pre-commit guard refused the first uncommitted packet because its synthetic fixture had a credential-shaped literal assignment. No commit occurred. The only executable change constructs the same 20-byte synthetic token by joining three literal pieces. AST inspection proves the effective bytes equal the original and all remaining module structure is unchanged; endpoint credentials, assertions and bounds are preserved. No renaming, guard exemption or allowlist change was made. The seven exact original runtime scripts and the diff are retained in lossless compressed artifacts with decompressed member hashes. `history/` retains the previous uncommitted sealed source archive and manifest. No preparer, fixture, listener, VM or admission was executed during this correction.
