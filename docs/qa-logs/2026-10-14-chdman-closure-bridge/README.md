# #574 fresh chdman closure allocation bridge — UNRUN

This additive packet supplies the missing executable bridge after the four-stage
CHD builder exits. It prepares **one new `chdman-closure` owner**, reusing the
reviewed Dolphin `DockerOwner`, watchdog, host PID handshake/cgroup observation,
resource sampling and original-result/cleanup machinery. It invokes unchanged
`94ca020acc65f9038f3a44a2f894be40868b1e1a` closure code. No build, export, target
execution, owner allocation or fixture import was performed in this source task.

The direct `/closure/closure.py` command in 94ca020 required an environment that
the completed four-stage owner cannot provide afterward. This bridge creates a
fresh admitted environment with the SDK's required old-prefix read-only mount.
It does not resume the original CHD family, rewrite its result or read/reset its
clock. Earlier packets and their evidence remain unchanged.

## Exact dependencies and acceptance

`bindings.json` fixes these source dependencies (all must remain available):

| Input | Identity/location |
| --- | --- |
| Original completed build | `/workspace/tmp/pix574-chdman-build-20261014-02/stages/chdman-build` |
| Original private work | `/workspace/tmp/pix574-chdman-build-20261014-02/work` |
| Build source | Coordinator `2026-10-14-chdman-export-alias-source`, commit `26a527f76527b1a4466404cbc8c07eee73524cd0`, manifest `2237c558dc1efb78fb889e803ab36a1be29d4715d119979167da04601b6fc96a` |
| Closure implementation | Assigned `m7-rvz-regressions-574/docs/qa-logs/2026-10-14-chdman-elf-closure-source`, manifest `602f03e41250396152b18da4b69d90697e53169bfafa0a2ee9a6d0e44d7175df` |
| Original sealed toolchain plan | Same assigned checkout, `docs/qa-logs/2026-10-13-rvz-regression-source/format-tool-build-plan`, commit `1c0e93`, manifest `f58655358feb6c0e75ee8f0ae5b9b02fdae985d075c5f6bcb66fcb0530604976` |

The exact absolute dependency roots are intentional: the coordinator checkout
does not currently carry both old source packets. This bridge can be invoked
from its assigned checkout while admission belongs to the coordinator checkout.
No package copy or broad historical branch merge is required. Their manifests
are verified before planning/execution and again afterward. Keep these small
source packets and original build inputs protected until closure/VM proof ends.

`prerequisites.snapshot()` refuses until the **actual future build** is PASS:
original selected child, attach, container and watchdog exits 0; no forced stop,
OOM or dead container; exact CID absence; empty recorded survivor/cgroup lists;
actual admitted host PID namespace and no matching recorded original container
process still alive. The original watched admission must be consumed with
runner/command/monitor exits 0 and unchanged admission identity. The parent
result's hash must bind the original inner result. Source-before/after and
generated target records must agree. Original archive/export failures cannot
be accepted through this gate.

The target's path, bytes and SHA256 come from that build's **original
`target-artifact.json`**, checked against the real file and generated inventory.
There is no guessed hash or generic failed-build recovery. Original receipt,
admission, source inventory and target hashes are frozen in `build-input.json`
at planning, rechecked at execution, and rechecked afterward. Full source
verification remains the successful build's contract; this bridge verifies its
receipts and mounts the completed work read-only, without rescanning every
source/object file. Closure independently rechecks every selected ELF/library.

## Allocation and containment

- Fresh **180-second clock** starts once at admitted `run-stage.py` execution
  after prerequisite/admission metadata verification. Exclusive `started`,
  `clock.json` and output creation refuse replay. Planning/review time is outside
  this new execution clock. The original family clock is neither used nor reset.
- Same pinned builder, `--pull=never`, `--network none`, read-only root, normal
  UID/GID, no-new-privileges, all capabilities dropped, **4 GiB/no swap, 2 CPUs,
  256 PIDs**. No compiler/loader/chdman execution.
- Read-only mounts: retained SDK checkout at its required old prefix, sealed
  plan `/plan`, this bridge `/runner`, unchanged closure packet `/closure`,
  original work `/work`, original build receipts `/build-receipts`, and original
  MAME archive `/mame-source.tar.gz`. Archive bytes are verified before/after;
  it is never extracted or used to build. No host old-prefix alias is created.
- Only the fresh stage is writable at `/receipts`; `/tmp` is a 64 MiB tmpfs.
  **1 GiB sampled ceiling** for new host owner / container receipts+tmp, with a
  512 MiB host free-space floor. Original read-only work/cache is protected and
  excluded from new scratch counting. The unchanged closure has its own 512 MiB
  bundle, 128-object and per-readelf bounds. Sampling is not a kernel disk quota.
- The actual host init PID is checked against container NSpid and PID namespace,
  then actual cgroup members/start ticks are retained. Original child/container
  exits, original logs, RAM/CPU/disk/deadline samples and cleanup channels remain
  distinct. Any watchdog intervention/forced stop leaves FAIL. The reused bounded
  retirement waits may exceed the work deadline solely to finish cleanup; they
  do not permit more closure work. No new clock allowance on timeout.

`docker_owner.py` and `watchdog.py` are byte-identical to the qualified Dolphin
loader-resolution packet. Selected common functions, inner telemetry/child
handling and host handshake/cleanup are reused. This includes exact typed Docker
inspection and case-insensitive exact-CID absence parsing plus complete ID
inventory, not broad text matching. Changed composition remains **UNRUN**.

## Next coordinator commands — prepared, not executed

Wait for original `chdman-build` PASS, all original delivery/host process channels
and admission consumption. `plan.py` refuses an unfinished/failed build before
creating the new owner. Choose a fresh owner if the proposed name already exists.
Do not loop/retry an existing owner. These commands allocate only after the
normal retention review/admission, not by this handoff itself.

```sh
cd /workspace/repos/rocknix.worktrees/m7-player-setup
PIX574_CHECKOUT=$PWD
PIX574_BRIDGE=/workspace/repos/rocknix.worktrees/m7-rvz-regressions-574/docs/qa-logs/2026-10-14-chdman-closure-bridge
PIX574_OWNER=/workspace/tmp/pix574-chdman-closure-20261014-01
PIX574_STAGE=$PIX574_OWNER/stages/chdman-closure
python3 -I -S -B "$PIX574_BRIDGE/plan.py" \
  --checkout "$PIX574_CHECKOUT" --owner "$PIX574_OWNER"
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$PIX574_STAGE/retention-plan.json" \
  --output "$PIX574_STAGE/retention-report.json"
# Consume the original report/watcher results and review current capacity.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$PIX574_STAGE/admission-plan.json" \
  --output "$PIX574_STAGE/admission.json"
tools/watch-build-submit --owner "$PIX574_STAGE/submit" -- \
  --admission "$PIX574_STAGE/admission.json" \
  --activity-dir "$PIX574_STAGE/logs" -- \
  python3 -I -S -B "$PIX574_BRIDGE/run-stage.py" \
  --checkout "$PIX574_CHECKOUT" --owner "$PIX574_OWNER" --stage chdman-closure
```

The container's sole task child is exactly:

```sh
python3 -I -S -B /closure/closure.py \
  --plan /plan/input-bindings.json --work /work/format-tools \
  --build-records /build-receipts --output /receipts/chdman-closure-01
```

It starts only the pinned readelf children. The bundle lands under
`$PIX574_STAGE/chdman-closure-01/vm20-bundle`; its original manifest and program
hash are the next VM inputs. Preserve `elf-N.*`, `elf-closure.json`,
`bundle-receipt.json`, `elf-inventory.json`, `container-result.json`, `result.json`,
watchdog/Docker cleanup evidence and original submission/watcher/launcher exits.
Check every original channel and actual host exit, then consume this new
admission with the existing `build-admission consume --run ... --evidence ...`
schema. No inner PASS alone is terminal acceptance.

Can this be done on the VM? **Yes** for actual loading/help and CHD/Saturn/CUE
execution; those remain the distinct fresh no-NIC VM gate using accepted 76f44e.
This admitted host step only reads ELF metadata and copies the required closure.
No target/loader execution, Sys assets, real game, account, provider or device.

## Static evidence / unrun refusal controls

`static-validation.json` records Python 3.10 AST/JSON parsing, exact source/file
and lifecycle-block comparisons, one child selection, readonly mount inspection,
fresh clock/bounds and manifest binding. No prepared module was imported and no
plan, owner, helper, fixture, Docker command or readelf was run by this worker.

Prepared acceptance/refusal cases for coordinator review, all **UNRUN** here:

1. Future original build PASS + consumed admission + unchanged target: one fresh
   closure owner, original closure/readelf exits 0, unchanged input snapshot,
   normal exact cleanup and no target execution.
2. Missing build, failure/forced cleanup/OOM, unconsumed or failed original
   admission: planning refuses before new owner creation.
3. Changed build source manifest, receipt, target byte/path/size or selection:
   refuse; no recovery/relabel of original failures.
4. Wrong host PID namespace or still-populated original cgroup: refuse.
5. Existing new owner/output/started/clock: refuse replay; never reset old clock.
6. Expiry, parent exit, interruption or readelf failure: original failure remains;
   exact owned container/process cleanup uses unchanged watchdog/DockerOwner.
7. Attempted writes to work/SDK/archive/old receipts: readonly mount; only new
   closure receipt/bundle output is writable.

No shared records, product edits, source pin promotion, push or upstream action.
