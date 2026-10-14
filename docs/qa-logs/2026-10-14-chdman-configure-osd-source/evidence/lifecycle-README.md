# #574 chdman lifecycle adaptation — source only, UNRUN

This packet adapts the qualified Dolphin Docker lifecycle to **four separate
chdman stages**. It does not launch, admit or allocate anything. `docker_owner.py`
and `watchdog.py` are byte-identical copies from Dolphin runner
`b65f782e20485fd7a499c108450ce1dd094ec0a3`; the retained common command/PID/cgroup
helpers, host handshake, resource monitoring and exact-container cleanup are reused.
No new generic harness or product change. Changed adaptation code is **UNRUN**,
not qualified merely because its lifecycle machinery was qualified previously.

`plan/` is a complete byte-identical copy of sealed
`1c0e93b4b34501928c79f9ade5b2b4c1442331a4` format-tool-build-plan, manifest
`f58655358feb6c0e75ee8f0ae5b9b02fdae985d075c5f6bcb66fcb0530604976`.
**`plan/build-stage.sh` and the shared-libstdc++ patch are unchanged.** The two
Dolphin selections remain in that immutable script but this adapter exposes only
chdman stages. `bindings.json` binds copied/adapted source provenance.

## Input and resource contract

- MAME/libretro pin `24cffe763621b164fc10be2ae3660f140be25182`, MAME 0.289.
  Retained archive: `/workspace/cache/rocknix-sources/mame-lr/mame-lr-24cffe763621b164fc10be2ae3660f140be25182.tar.gz`.
  Exact **213,471,628 bytes**, SHA256
  **`4867bee5dbd4129e6eea095fe8f8e9725563998710cc9620190e90529ef8931b`**.
  Its existing size was checked read-only here. Hash verification and extraction
  are prepared runtime actions, not newly claimed observations of this archive.
- Pinned offline builder image from sealed `plan/input-bindings.json`:
  `ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`.
  `--pull=never`, no network, read-only root, normal UID/GID, all capabilities
  dropped, no-new-privileges, 256 PIDs, **4 GiB RAM/no swap and 2 CPUs**.
- Accepted physical `m7-pixelelated-replacement20` is mounted **read-only** at
  `/workspace/repos/rocknix.worktrees/m7-pixelelated`. The unchanged script uses
  `build.pixelelated-GENERIC_X64.x86_64/toolchain` there. Absolute compiler wrapper
  and sysroot library links retain their original prefix. No cache copy, patch,
  host package install, download or accepted-cache mutation.
- One compile job (`-j1` in every unchanged make invocation). One **1800-second
  family clock**, starting at first export run and shared across export,
  bootstrap, configure, build **and inter-stage review/admission time**. No reset,
  extension, implicit retry or automatic next stage. An expired clock refuses.
  The existing bounded Docker retirement waits remain cleanup, not additional
  permitted compilation time; watchdog intervention always leaves FAIL.
- **6 GiB sampled scratch stop ceiling**, including source, generated outputs,
  receipts/logs and container temporary data; it is not a kernel disk quota.
  Original 512 MiB host free-space floor, cgroup memory/OOM/swap/CPU samples,
  disk samples, PID-namespace handshake and independent watchdog are retained.
  Actual host visibility/admission is coordinator-owned. Forecasts are stop and
  reassess bounds, not a promise that compilation fits or finishes in 30 minutes.

## Stage contracts

| Stage | Selected action | Evidence before advancing |
| --- | --- | --- |
| `chdman-export` | Hash archive, validate every header, privately extract regular files/directories, apply exact sealed patch | 33,835 members / 897,821,359 pristine regular bytes; original and patched inventories; patch child exit; source-after verification |
| `chdman-bootstrap` | Unchanged `build-stage.sh chdman-bootstrap` | Native `/usr/bin/gcc`, `g++`, `ar` only; original make exit; GENie artifact hash and generated-file inventory |
| `chdman-configure` | Unchanged `build-stage.sh chdman-configure` | Original make/GENie exit; generated 0.289/exact-pin version; release64 compiler, flags and selected library graph inspection |
| `chdman-build` | Unchanged `build-stage.sh chdman-build` | Exact configured files unchanged; original make/link exit; chdman path/size/SHA; pristine source comparison; cleanup original channels |

Each stage needs its own new admission and watched owner under the **same family
root**. Earlier stages must have PASS original container/client/guard/cleanup
results and successfully consumed watcher runner/command/monitor channels. No
failure-recovery adapter is provided; failures remain original failures and stop
this family. `started` and existing-output guards refuse replay.

The exporter validates the complete header inventory from the exact hash-bound
archive before writing source. Only canonical relative paths under the exact
archive root are accepted, with no duplicates, traversal, aliases, links, sparse
files, special nodes or privileged modes. Content is streamed with exclusive
creation and declared lengths; no `extractall` or blind tar command. Selected
source bytes are additionally checked against the sealed source hashes. All
other regular files, including licences, are retained; this is not an invented
hand-picked subset of MAME's generator inputs.

The sole allowed original-source difference is the exact existing
`chdman-shared-libstdcxx.patch`: `scripts/genie.lua` changes from
`b3dd93f153fa40fa69983f1cc24ee2119510a3459c22a378c6a4d80c4cef97d3` to
`60be68969448508ba3a130f64044ec196f6d52970337889474c85bcb075c40ba`.
Original chdman/CHD/codec sources remain unchanged. `-static-libgcc` remains;
the absent static libstdc++ is replaced by the sealed shared-runtime policy.
The actual target's dynamic library closure still requires later qualification.

Every stage rehashes original exported files and verifies their modes and
inventory. Generated files are kept separately under known build/GENie output
paths, plus the sole root `chdman` output. An original file remains protected even
if its path is inside a generated-output directory. Prior generated hashes are
checked between stages and across later stages; build may add outputs, not alter
configured makefiles, version or native bootstrap bytes. Changed original hashes
are recorded in failure diagnostics. `pristine-source-inventory.json`, patched
`source-inventory.json`, and per-stage `generated-before/after.json` retain the
separation; no placeholder is silently reclassified as an original source edit.

`template-evidence.json` records read-only member hashes and exact GENie/MAME
template excerpts inspected before sealing. The message-skip setting suppresses
the optional solution echo line, while empty LDDEPS is parsed without consuming
the next assignment. Native GENie's own release -Os is separate from target O1.
No templates were executed and no source tree was extracted during this review.

Configure inspection reads the emitted solution/selected project files without
running make again. The selected dependency graph must be chdman plus `utils`,
`expat`, `7z`, `ocore_sdl`, `zlib`, `zstd`, `flac`, and `utf8proc`. Its release64
compiler/archive tools must name the exact target prefix; C/C++ flags must select
O1 without LTO/OpenMP. Bundled static codec links, static libgcc, shared C++ policy,
private output location and generated version are required. Compiler-input hashes
are recorded separately for native bootstrap and target wrappers. Original
verbose make logs remain authoritative for actual compiler/link invocations.
An unexpected generator shape refuses rather than guessing. This contract's
first real generated-file inspection remains UNRUN.

## Coordinator-only next command — UNRUN

Can this be done on the VM? Conversion/loader/format proof must run later in the
coordinator's disposable VM. These four stages only prepare the tool in its
admitted offline builder; no target chdman execution on the host or builder.
Native GENie bootstrap and generator execution are the explicit host-tool part
of the existing sealed plan. pix-nova owns the CHD/cross-format guest packet;
pix-memory owns the actual proxy service fixture. This packet does neither.

Use a **fresh** family owner. Substitute a newly chosen owner basename before
running; the name below is a proposal, not an allocation or existing reservation.
Run only the selected stage, inspect/consume its original results, then prepare
the next stage explicitly. Never loop all four without consumption.

```sh
cd /workspace/repos/rocknix.worktrees/m7-steam-preservation-integration
PIX574_REPO=$PWD
PIX574_PACKET=$PIX574_REPO/docs/qa-logs/2026-10-14-chdman-build-runner
PIX574_OWNER=/workspace/tmp/pix574-chdman-build-20261014-01
PIX574_STAGE=chdman-export
python3 -I -S -B "$PIX574_PACKET/plan.py" \
  --checkout "$PIX574_REPO" --owner "$PIX574_OWNER" --stage "$PIX574_STAGE"
PIX574_STAGE_ROOT=$PIX574_OWNER/stages/$PIX574_STAGE
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$PIX574_STAGE_ROOT/retention-plan.json" \
  --output "$PIX574_STAGE_ROOT/retention-report.json"
# Coordinator consumes original report/watcher channels and reviews capacity.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$PIX574_STAGE_ROOT/admission-plan.json" \
  --output "$PIX574_STAGE_ROOT/admission.json"
tools/watch-build-submit --owner "$PIX574_STAGE_ROOT/submit" -- \
  --admission "$PIX574_STAGE_ROOT/admission.json" \
  --activity-dir "$PIX574_STAGE_ROOT/logs" -- \
  python3 -I -S -B "$PIX574_PACKET/run-stage.py" \
  --checkout "$PIX574_REPO" --owner "$PIX574_OWNER" --stage "$PIX574_STAGE"
```

Consume exact original stage/watcher/launcher receipts with the existing
`build-admission consume` schema before selecting `chdman-bootstrap`, then
`chdman-configure`, then `chdman-build`. The original family clock keeps running.
The packet can be copied byte-exact to the coordinator checkout for execution;
`--checkout` and the above repository variable must then identify that checkout.
No integration has been performed here.

All selected child exits, Docker attach/container exits, resource faults,
watchdog intervention, observed host PID identities, exact CID absence and cgroup
quiescence remain separate original receipts. Export compact manifests/logs and
failed results before retiring private scratch. Retain a successful target only
for immediate ELF/loader/CHD qualification; compilation alone is not format or
frontend acceptance. No historical cleanup, source pin, shared tracking or push.

## Static evidence and scope limits

`static-check.py` only parses source/AST, compares hashes and runs `bash -n` on the
unchanged entrypoint. It imports no prepared module and performs no export,
configure, make, compiler, Docker, VM, dependency install or target execution.
`static-result.json` records actual static checks; `SHA256SUMS` seals the packet.
No new generic lifecycle controls are introduced. Reused machinery retains its
prior provenance, while changed stage/export/configure contracts await coordinator
qualification. Any first-run failure keeps its original result.

Read current checkout AGENTS and canonical next checkpoint/rules (device-builds,
engineering-practices, handheld-evidence, vm-first, instruction-files and working
principles), plus coordinator's current 15:32 checkpoint, before preparation.
The canonical next checkpoint is historical and none of its commands were replayed.
Existing upstream/source/license research is retained byte-exact in sealed `plan/`;
this is a fork-specific QA adaptation, not a new upstream product fix or submission.
