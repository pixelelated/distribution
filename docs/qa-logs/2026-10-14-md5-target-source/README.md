# #574 MD5 target compilation and repaired-wrapper packet

**Source-only preparation. Nothing here has been configured, compiled, imported
as a fixture, run in a guest, or allocated by this worker.** No product edit, pin,
shared record or publication. Independent format-tool plan **1c0e93b4b34501928c79f9ade5b2b4c1442331a4**
remains separate and UNRUN.

## Source and historical boundary

Candidate ES **314da58d68820a79b26f99a5b6c12f9bb37054d5** changes only
`external/libcheevos/libretro-common/src/utils/md5.c` within the compiled library
closure, relative to bb9e. Its added `tests/md5-alignment.c` supplies8 offsets ×
11 lengths ×3 update splits =264 output rows. The fix reads each little-endian
word through `memcpy`; it does not change the other architecture branch.

The original full-library sanitizer03 build qualified compilation, not execution.
The subsequent pristine a7 wrapper run returned1 with UBSan's misaligned
`MD5_u32plus` load at md5.c:110, reached through `MD5_Update` → Nintendo partition
hash → public GameCube hash → `generateHashFromFile`. Only fixture generation had
passed before that run stopped. Those stderr/return/result bytes remain intact;
`input-bindings.json` binds them and the actual successful compiler methodology.
No old run becomes a pass and no sanitizer is disabled.

For the new comparison, an exclusive source snapshot of pristine
**a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20** receives exactly the candidate's
`md5.c`, after verifying its original hash. It is labeled **baseline-repaired**
everywhere. It is neither pristine a7 nor a new ES commit. Every other baseline
file remains byte-identical. Candidate source stays exactly314da58d; neither ES
worktree is edited. Git-object exports are small public source copies: candidate
275 files/4,395,349bytes; pristine baseline271/4,374,568; sealed fixture140/2,758,521,
plus the1,364-byte MD5 driver. No build-cache copying or firmware extraction.

The actual MD5 owner is **libretro/libretro-common**, path `utils/md5.c`, as the
coordinator's dated upstream snapshot at
[39eae6ac1c4e4dd809f27cec210ace8d62a5c0a5](https://github.com/libretro/libretro-common/blob/39eae6ac1c4e4dd809f27cec210ace8d62a5c0a5/utils/md5.c)
records. rcheevos calls it; it is not the owner of this implementation. The other
`libFLAC/md5.c` in the same archive is distinct. Compiler-contract matching uses
the full `libretro-common/src/utils/md5.c` suffix, never a basename-only lookup.
This packet reuses that upstream evidence; it makes no newer-upstream-status claim.

## Small target set, exact compiler/include contract

`CMakeLists.txt` composes the sealed **7180edfedf39a34322fc209c8727567bffaf2501**
`cmake-all-direct-contracts` entrypoint, not the failed earlier include fixes.
It forces whole-library ASan/UBSan on. The MD5 driver links the real static
`libcheevos` archive with ordinary archive extraction; no duplicate MD5, alternate
implementation, whole-archive link or sanitizer exclusion. It inherits the
library's private includes and definitions and the sealed direct consumer's
compile options, including the ten legacy feature flags. The candidate retains
RVZ enabled; repaired baseline retains it disabled.

Configure produces a fresh compile database. Before any build command,
`build-target.py` checks MD5-driver and Wii direct-source includes/definitions
against their actual product TUs, checks RVZ feature agreement, requires
`-fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -g`
in every TU, and rejects `-fno-sanitize=`. Any missing/ambiguous contract refuses.
It saves the evaluated database and contract reports. As in sealed7180, only the
official synthetic generator's signed PRNG has `-fwrapv`; product UBSan remains on.

Compile just these targets, sequentially with one compiler job:

| Composition | Targets |
| --- | --- |
| baseline-repaired | `pix574-md5-alignment`, `pix574-regression-hash`, `pix574-wii-partition-probe` |
| candidate314 | those three plus `pix574-fixture-writer` |

The reviewed reader/concurrency and padding tests are not recompiled or replayed.
No frontend or French catalog build. Nine artifacts total: seven executables and
exact target `libasan.so.8`/`libubsan.so.1`. CMake's unbuilt graph can still contain
other sealed targets; those are not requested or counted as compiled artifacts.
Actual configure/link success and evaluated option inheritance remain UNRUN.

`compile.py` verifies source/tool/packet hashes, exports exclusive snapshots,
records the repaired composition, and launches the same pinned builder and
accepted read-only target toolchain prefix as sanitizer03. The toolchain files
are selected executable/config identities, not a checksum of the entire cache.
`--pull=never`, no network, read-only container root/cache, private writable owner,
4GiB memory with equal swap limit,2CPU,256PIDs, one compile job,900seconds for the
container and finite cleanup. GCC target is x86_64 ROCKNIX. It never runs target
binaries on the host. It records original stage/container exits and resource
samples; an interrupted or forced-stop job cannot pass.

## Admission and exact next command — coordinator only, UNRUN

Can the behavior be checked on the VM? **Yes.** Cross-compilation uses the admitted
host builder; target digest and sanitizer checks use a fresh disposable no-NIC
GENERIC_X64 VM. The prior VM and compiler owners are retired, not reusable.
No current capacity or allocation is asserted here.

Choose a NEW simple `/workspace/tmp/<name>` owner. From this frozen distribution
checkout, set `REPO`, `PACKET` and `ES` to these paths:

```sh
REPO=/workspace/repos/rocknix.worktrees/m7-rvz-regressions-574
PACKET="$REPO/docs/qa-logs/2026-10-14-md5-target-source"
ES=/home/max/Development/emulationstation-next.worktrees/m7-md5-alignment
OWNER=/workspace/tmp/REPLACE_WITH_NEW_MD5_OWNER
cd "$REPO"
python3 -I -S -B "$PACKET/plan.py" --owner "$OWNER" --checkout "$REPO"
```

This only creates a plan and fresh empty scan/log/record/submission directories.
The plan reserves1GiB for two sanitized builds,512MiB scratch,256MiB artifacts/logs
and32MiB public snapshots. This retains the previous conservative disk allowance;
actual03 peak was435,642,368 cgroup bytes, zero OOM, two compile stages about21.2s.
Those measurements are historical estimates, not fresh capacity/admission.
Protected cache and source roots are never removal candidates; no reclamation is
assumed. Plans/report/admission remain coordinator-owned outside tracked source.

```sh
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$OWNER/retention-plan.json" --output "$OWNER/retention-report.json"
# After reviewing the fresh report and original report-job exits:
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$OWNER/admission-plan.json" --output "$OWNER/admission.json"
```

The **exact next admitted compile submission** is:

```sh
tools/watch-build-submit --owner "$OWNER/submit" -- \
  --admission "$OWNER/admission.json" --activity-dir "$OWNER/logs" -- \
  python3 -I -S -B "$PACKET/compile.py" \
    --owner "$OWNER" --repo "$REPO" --es-repo "$ES"
```

Do not use `--record-only` for that command. The admission expires and is single
use; re-evaluate current memory/disk/concurrent jobs rather than replaying03.
Actively consume launcher/wrapper/watcher/runner results within60seconds; there
is no off-session notification. Review `result.json`, `compile-result.json`,
`records/stages.json`, the actual configure/build logs and contract databases,
CID/host process exits and cgroup OOM counters. Zero exit alone is insufficient.
Preserve original failure results before investigating. Consume the admission
with new evidence; it does not delete outputs. Retire new objects/tmp/snapshots
once their evidence is retained. Keep only targets/libs for the next admitted
runtime, then retire them after its result consumption. No old owner is touched.

## Fresh target runtime — prepared, UNRUN

After a successful newly bound compile, the coordinator prepares a NEW public
read-only input root `/tmp/pix-input/md5` containing this packet under `packet/`,
`artifacts/`, `compile-result.json`, `result.json`, and both
`records/contract-*.json`. Preserve executable modes on all seven binaries.
No source tree, build cache, account, real ROM or independent format tool is
needed in the VM. Record the export/installed byte hashes and source commit.

Use the next admitted no-NIC GENERIC_X64 guest (only `lo`), standard8GiB/4CPU
profile or a separately reviewed adequate profile, and a new empty512MiB tmpfs
at `/tmp/pix574-md5-NEW`. Guest root, Python3, target runtime loader/libs and the
matching image are prerequisites. Coordinator mounts/owns scratch; the runner
will not mount, start services, boot an engine or grant itself a VM. It checks
scratch is a distinct tmpfs with256–512MiB available and input is read-only.

The exact first target command, within the coordinator's watched serial job:

```sh
/usr/bin/python3 -I -S -B /tmp/pix-input/md5/packet/run-guest.py \
  --disposable-vm --input /tmp/pix-input/md5 --scratch /tmp/pix574-md5-NEW
```

Save its original exit/stdout/stderr and serial wrapper exit separately. On
success or failure, export `scratch/receipts/` to a fresh `/tmp/pix-output` owner
before unmounting scratch; never export synthetic fixtures as owner library data.
The runner has a300s whole-run alarm,30s per normal control/60s per repeated
wrapper,64MiB per-file cap and no core dumps. It kills/waits only its own current
process group on timeout/interruption and records original signals/exits. ASan's
large virtual shadow is preserved; no incompatible address-space ceiling or
sanitizer suppression. The tmpfs provides the finite aggregate storage ceiling.

## Acceptance mapping and limits

| Criterion | New evidence required |
| --- | --- |
| Correct target source and instrumentation | before/after source hashes; evaluated `contract-*.json` PASS; original configure/compile/container0; compile database/logs and exact binary/runtime hashes |
| MD5 bytes preserved | Each build emits the exact264 offset/length/split rows, compared to independent Python `hashlib.md5` on generated `(i*13+7)&255` bytes;528 comparisons across the pair, original0 and empty sanitizer stderr |
| Blocked public wrapper regression repaired | Both actual wrappers hash official synthetic GameCube ISO and Saturn ISO/CUE against the immutable known answers, once and16 repeats in one process; four exact-output receipts, original0/empty stderr |
| Shared Wii helper semantics preserved | Both positive helper digests match independently selected byte ranges; candidate truncated-section control returns original2 with `FAIL`, empty sanitizer stderr |
| Negative evidence stays honest | Old pristine-baseline exit1/MD5 UB remains bound separately; repaired-baseline labels retained; any new stderr, wrong row, duplicate/reordered/missing row, timeout, nonzero unexpected exit or identity mismatch fails |
| Bounded retirement | ten runtime command receipts and final result, all child groups exited; original outer exits; scratch/export/VM retired by coordinator |

No fresh original-baseline UB rerun is needed. This is a repair comparison, not a
new claim that pristine baseline was sanitizer-clean. Successful rows do not
qualify big-endian/ARM behavior, handhelds, an installed frontend, a release image,
CHD, independent DolphinTool/RVZ format compatibility or a public Wii ISO/catalog
hash. Those remaining criteria and independent plan1c0e93 remain separate. No
matching library/ABI blocker was found by source inspection; actual new CMake
configuration and target linking are the next executable checks. Static checks
are in `static-result.json`; all prepared scripts remain UNRUN.
