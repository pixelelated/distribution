# M7 ES syntax retry02 — header-root correction, UNRUN

This packet prepares only `es-syntax` for ES **c045d2ec1936c2dfc6c4777935fb2d4cd8b3bcfa**, tree **7a34dbe6ec6d5a5f153059153ba7d8b4a22e6451**. No owner, retention report, admission, container, compiler or VM was launched during preparation. The ES source tree and all existing packets/shared records remain unchanged.

It adapts the accepted `2026-10-14-proxy-current-native-py310` family runner. `docker_owner.py` and `watchdog.py` are byte-identical; shared command handling, original child/attach/container/monitor result channels, PID/CID identity, cgroup samples, fail-closed absence checks and owned cleanup remain. The native export/build payload is replaced by one source-bound invocation of the existing unchanged `tools/es-syntax-check`. No generic framework, downloads or cache copies are added. `derivation.json` binds the actual prior successful stage and source packet.

## Why run01 failed and what changes

Run01 remains original FAIL1. Its four other translation units passed; `ThreadedHasher.cpp:37` failed because the declared capability was missing from the header selected by the syntax fixture. The original tool captures compiler diagnostics in a shell variable and prints filtered errors on stdout; `selected-stage.stderr` is empty and the error is in `selected-stage.stdout`. Exact original selected-stage/container/owner/watchdog records are copied under `original-run01/` with source paths/hashes in `derivation.json`.

This is an include-path mismatch, not evidence that c045 lacks a declaration. The real caller uses `#include <libcheevos/cheevos.h>`. Existing `--with` is intentionally `-iquote`, so it cannot affect that angled include; existing `--tree` supplies `-I` only for es-core/es-app. The cached Ninja command then selects c8dc's external header (SHA52f8e0af…), which lacks the capability. The c045 external header (SHAc96241e0…) declares it unconditionally, and c045's cheevos.cpp defines it. `header-selection-static.json` binds both headers, caller, exact cached Ninja include order and static negative/positive selection. This is source reasoning; no compiler include trace has been collected by this worker.

The only execution-byte change in retry02 is the copied helper's `--tree` block: when the selected full tree has `external/`, prepend that real directory to its existing `PRE` include roots, ahead of cached `-I` roots. `--with` remains unchanged and quote-only. App/core header farms still use the same source inodes. No declaration stub, forced include, warning suppression, diagnostic removal, product change, changed feature define or weakened return-code expectation. The exact same five units,600s/4GiB/2CPU/no-network bounds, all wrapper files and original cleanup/status handling remain.

A durable repository tool repair is warranted: the helper promises to check selected-tree headers, yet an angle include from that tree's external root currently reaches stale cached source. The attached patch is minimal and independently reviewable. Root may apply it to `tools/es-syntax-check` after the admitted retry and scoped tool review; this packet does not modify that file or any shared record. `preprocessor-checks-proposal.md` describes optional targeted compiler-selection controls for that tool integration; these are UNRUN and not added RC gates. Original failure/accepted packets remain immutable.

## Exact inputs and writable scope

- New ES worktree `/home/max/Development/emulationstation-next.worktrees/m7-candidate-compose` is mounted read-only at its identical path. Host requires the exact commit/tree and clean state. Host and container recheck the1113 regular source-file identities/modes; the gitlink directory is recorded separately.
- Accepted SDK worktree `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20` is mounted read-only at `/workspace/repos/rocknix.worktrees/m7-pixelelated`. Existing Ninja rules embed that old prefix. No cache symlink is modified.
- `plan/es-syntax-check` is an additive fixture copy with the seven-line --tree external-root correction in `es-syntax-check-external.diff`; the shared repository tool is unchanged. `plan/syntax-command.sh` differs from the previous handoff only by selecting that sealed `/plan` copy. It checks ApiSystem.cpp, ThreadedHasher.cpp, GuiMenu.cpp, GuiWifi.cpp and Settings.cpp against the composed header tree. External libcheevos C/C++ is outside this helper's coverage; this run is not a full build or target test.
- Current g++, cc1plus and Ninja identities supplement the accepted compiler/header inventory. All26,095 SDK header/support rows and1,015 cached ES/Ninja input files are bound and rechecked. The source manifests are data; no product Python is imported.
- Container root, `/plan`, `/runner`, SDK and ES mounts are read-only. Only fresh owner `/work`, stage `/receipts` and64MiB private `/tmp` are writable. `TMPDIR`/`CCACHE_TEMPDIR` point to `/work/es-syntax/tmp`; the helper's symlink header farm and compiler temporaries stay there. CCACHE_DISABLE=1, one sequential compiler driver, no object build.

Pinned builder: `ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`. Original `--pull=never`, no network, read-only root, normal UID/GID, all capabilities dropped, no-new-privileges,4GiB memory/no swap,2CPUs,256PIDs. One fresh **600-second family work clock**, no retry/reset/extension. Existing bounded cleanup follows it; cleanup intervention makes FAIL. **1GiB sampled aggregate scratch ceiling**, not a hard filesystem quota;512MiB host free-space floor. Active coordinator supervision remains required; no off-session notifier is claimed.

## Exact coordinator commands — do not launch beside VM work

Keep this packet immutable in place, or copy it byte-exact to the coordinator's chosen source directory and change only `PIX_ES_PACKET` below. The following owner is reserved only in this proposed command; it has not been created. If already used when selected, choose a new owner and obtain a new report/admission. Do not reuse a failed/completed owner.

```sh
cd /workspace/repos/rocknix.worktrees/m7-player-setup
PIX_ES_REPO=$PWD
PIX_ES_PACKET=/tmp/m7-es-syntax-allocation-20261014-02
PIX_ES_OWNER=/workspace/tmp/pix-m7-es-syntax-20261014-02
PIX_ES_STAGE=es-syntax
python3 -I -S -B "$PIX_ES_PACKET/plan.py" \
  --checkout "$PIX_ES_REPO" --owner "$PIX_ES_OWNER" --stage "$PIX_ES_STAGE"
PIX_ES_STAGE_ROOT=$PIX_ES_OWNER/stages/$PIX_ES_STAGE
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$PIX_ES_STAGE_ROOT/retention-plan.json" \
  --output "$PIX_ES_STAGE_ROOT/retention-report.json"
# Inspect and consume the original report owner/results before admission.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$PIX_ES_STAGE_ROOT/admission-plan.json" \
  --output "$PIX_ES_STAGE_ROOT/admission.json"
tools/watch-build-submit --owner "$PIX_ES_STAGE_ROOT/submit" -- \
  --admission "$PIX_ES_STAGE_ROOT/admission.json" \
  --activity-dir "$PIX_ES_STAGE_ROOT/logs" -- \
  python3 -I -S -B "$PIX_ES_PACKET/run-stage.py" \
  --checkout "$PIX_ES_REPO" --owner "$PIX_ES_OWNER" --stage "$PIX_ES_STAGE"
```

Admission fingerprints the coordinator checkout at preparation. Do not change its tracked source during the admitted interval; later work needs fresh admission. The wrapper independently binds the ES commit/tree/bytes, so a coordinator fingerprint is not substituted for ES identity. The current issue allocation should state this exact source-only compiler stage and VM-first boundary: runtime/UI acceptance belongs to the disposable guest; this check uses the pinned cross-toolchain in its offline builder.

## Original result consumption

Consume `stages/es-syntax/result.json`, `container-result.json`, `syntax-result.json`, `selected-stage.json`, `logs/selected-stage.stdout`/stderr, `logs/container.stdout`/stderr, `compiler-inputs.json`, `watch-run.json`, watchdog/host Docker cleanup receipts and resource samples. `syntax-result.json` requires five exact ordered OK rows plus one PASS from the original tool; it never converts a missing command/error into success. The helper's original nonzero exit is retained. Original attach/container/child/watchdog must all succeed, no forced cleanup/OOM/resource fault, and actual recorded processes/CID must be absent.

Then consume the original watch runner/command/monitor and submit launcher/tool-wrapper channels using the existing admission workflow; inspect actual host exits before marking consumed. Retire only this fresh owner's private header-farm/compiler scratch after compact evidence export. Preserve failures as failures and use a fresh owner for any separately reviewed correction. No automatic retry, artifact promotion, distribution pin move or test-result relabelling occurs.

Preparation validation is static only: Python3.10 AST, exact unchanged ownership-helper comparison, binding/manifest hashes and command/mount inspection. All prepared entrypoints remain UNRUN. No shared docs or prior packet was modified.
