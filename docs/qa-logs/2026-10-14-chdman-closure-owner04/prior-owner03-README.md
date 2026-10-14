# #574 owner03 closure rebind — source only, UNRUN

This additive packet binds the fresh closure allocation to corrected CHD source
`2608923ba0ab80752e555adb393d7a029baeaf8c` and prospective build owner03.
The seven bridge Python files are **byte-identical** to `41684b51c3`; the
closure subpacket derives from `94ca020`. Both historical packets remain
unchanged. Owner02 failed configure, its original results remain failures, and
its retired work is not a usable input. Nothing here resumes that owner.

Read the corrected builder's `README.md` and `changes.json`: GENie's libretro
configuration block executed its Lua assignments unconditionally and replaced
the requested SDL OSD. The repair preserves all options and adds the exact
two-line guard around the three retro-only assignments. It does not drop the
XInput options. This source packet does not apply the patch or repeat the build.

## Exact source and input bindings

The coordinator copy at
`/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-14-chdman-configure-osd-source`
was compared against all **86 committed file blobs**, including both recursive
manifests. `source-review.json` records their SHA256 identities. The toolchain
object in input-bindings.json and common Docker/runner/telemetry files remain
byte-identical to their prior source. Actual runtime remains UNRUN here.

| Binding | Exact identity |
| --- | --- |
| Revised builder commit | `2608923ba0ab80752e555adb393d7a029baeaf8c` |
| Revised builder manifest | `349a57d0c81a03ef564bf2f9aec197a0fbf7e9b676106a8b00d375bea0b67c45` |
| Revised plan manifest | `1ff0f210cc3d88a4a761fff9dc1b81cc4e78c780f1367ed067d1abbaa0161ec0` |
| Revised plan input JSON | `b151b9218c6d91ef7148a14a7f0468c02c9ef299bce69c7cc7f556e9b6ce15ce` |
| Prospective successful build stage | `/workspace/tmp/pix574-chdman-build-20261014-03/stages/chdman-build` |
| Read-only source work | `/workspace/tmp/pix574-chdman-build-20261014-03/work` |

Both bridge and closure now bind the **revised plan**, not historical 1c0e93's
`d384...` input. The bridge mounts that coordinator plan read-only at `/plan`.
The revised closure requires that exact input hash. Its only executable-source
delta is a corrected refusal diagnostic and a narrow check of both scratch
adjustments: the source inventory and successful source-check receipt must name
each exact adjustment, and actual file bytes/size/mode must match the recorded
patched input. Both files' hashes join the final unchanged-input recheck.

- Existing `scripts/genie.lua` link-policy adjustment remains
  `60be68969448508ba3a130f64044ec196f6d52970337889474c85bcb075c40ba`.
- New `scripts/toolchain.lua` OSD adjustment must be
  `b45c6d1fa1d4d4a824d1f739ab749d2ae776dfb23b7a040b89bc4d2c67c2219b`.

Full pristine-source and exact two-file patch-scope verification remains the
corrected builder's contract, whose original PASS/consumed result is required.
The closure does not claim a new whole-tree audit. Build target path, size and
SHA256 still come **only from the eventual original `target-artifact.json`**,
verified against the actual file and generated inventory. No guessed binary
hash, loader wrapper, or failed-build recovery is accepted.

## Unchanged allocation contract

The bridge still requires original build child/attach/container/watchdog exits
0, consumed original admission, unchanged source-before/after, no OOM/forced
stop, exact CID absence and original host-process/cgroup quiescence. It freezes
and rechecks original receipts and target bytes at plan/run/finish boundaries.
The current fresh owner must be different from any completed or failed owner.

Fresh **180 seconds / 4 GiB RAM, no swap / 2 CPUs / 256 PIDs**, offline pinned
builder with read-only root, no capabilities, normal UID/GID. One new clock,
exclusive started/output files, no clock resets or implicit retries. The original
build clock is not reused. New scratch has a **1 GiB sampled ceiling** and
512 MiB host free-space floor; closure retains its 512 MiB bundle bound. Existing
bounded retirement waits are cleanup only, not more work time.

Archive, SDK at its required old prefix, revised plan, bridge, closure, completed
work and original build receipts are read-only container mounts. Only the fresh
stage's receipts/bundle plus 64 MiB `/tmp` tmpfs are writable. No host SDK aliases,
source export, compiler, target/loader execution or Sys assets. DockerOwner,
watchdog, exact host PID handshake, cgroup/telemetry and original result channels
are unchanged. The bridge's absolute closure path points to this new packet's
`closure/` in the assigned `m7-rvz-regressions-574` checkout; it must remain
available read-only. No historical branch merge is needed.

## Next coordinator command sequence — UNRUN

After owner03's actual build succeeds, consume all original results/admission.
Planning refuses before creating a new owner if that prerequisite is absent.
The proposed closure owner below is a fresh name, not an allocation made here.

```sh
cd /workspace/repos/rocknix.worktrees/m7-player-setup
PIX574_CHECKOUT=$PWD
PIX574_BRIDGE=/workspace/repos/rocknix.worktrees/m7-rvz-regressions-574/docs/qa-logs/2026-10-14-chdman-closure-owner03
PIX574_OWNER=/workspace/tmp/pix574-chdman-closure-20261014-03
PIX574_STAGE=$PIX574_OWNER/stages/chdman-closure
python3 -I -S -B "$PIX574_BRIDGE/plan.py" \
  --checkout "$PIX574_CHECKOUT" --owner "$PIX574_OWNER"
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$PIX574_STAGE/retention-plan.json" \
  --output "$PIX574_STAGE/retention-report.json"
# Consume original report/watcher results and review fresh capacity.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$PIX574_STAGE/admission-plan.json" \
  --output "$PIX574_STAGE/admission.json"
tools/watch-build-submit --owner "$PIX574_STAGE/submit" -- \
  --admission "$PIX574_STAGE/admission.json" \
  --activity-dir "$PIX574_STAGE/logs" -- \
  python3 -I -S -B "$PIX574_BRIDGE/run-stage.py" \
  --checkout "$PIX574_CHECKOUT" --owner "$PIX574_OWNER" --stage chdman-closure
```

The existing bridge invokes `/closure/closure.py` with `/plan/input-bindings.json`,
`/work/format-tools`, `/build-receipts`, and fresh output
`/receipts/chdman-closure-01`. Only pinned readelf subprocesses inspect the target.
Keep all original readelf/ELF/version-provider records, bundle manifest,
container/host/cleanup/watchdog records and submission/watcher/launcher exits.
Consume the new admission after actual host exit and exact cleanup proof.

Output remains `$PIX574_STAGE/chdman-closure-01/vm20-bundle`. No Sys assets.
Static closure is not loading/help/format acceptance: those remain distinct
coordinator-owned no-NIC VM gates, followed by the accepted CHD execution map.
No change to source-bound expected game hashes or previous format proof.

## Static validation and prepared controls

`static-validation.json` and `changes.json` record the exact changes, seven
unchanged bridge modules, unchanged ELF parsing/loader helpers, revised committed
source/recursive manifest identity, Python 3.10 AST and JSON checks. No module
import, helper/fixture run, compilation, readelf, container or VM occurred here.

Prepared runtime controls remain **UNRUN**: valid owner03 successful/consumed
build; old `d384` plan refusal; missing/mismatched OSD patch receipt or source
byte refusal before ELF inspection; target byte/path/size mismatch refusal;
failed/unconsumed build refusal; existing owner/replay refusal; unchanged
deadline/interruption/readelf-failure cleanup paths. Earlier owner02 failures and
all prior evidence stay unchanged. No product/shared-record edit, push or resource
allocation.
