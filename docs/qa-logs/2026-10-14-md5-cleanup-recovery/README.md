# #574 exact Docker cleanup recovery — source only

The original0962 compile at `/workspace/tmp/pix574-md5-target-20261014`
completed all four configure/build stages0, both include/instrumentation contracts
PASS, and nine artifacts. Cgroup peak410,615,808bytes; all OOM counters0.
Its outer result, launcher, wrapper, and watcher remain **FAIL1**. This packet
accepts those artifacts for the next runtime only after explicit cleanup recovery;
it does not relabel the old job or compile again. Runtime remains UNRUN.

The original `container-final-inspect.json` contains exit1, newline stdout, and
`error: no such object: <exact64-character CID>`. The original predicate required
capitalized `No such object`. Coordinator's later03:03:47UTC typed inspect returns
`Error response from daemon: No such container: <same CID>`; successful
`docker ps -a --no-trunc --format '{{.ID}}'` excludes that CID. The same immutable
readback records all five host PIDs absent and original wrapper1. The old terminal
watcher file's `alive=yes` was sampled before its process exited; it is not used
as current process proof. Worker only read these records; no Docker/process check
or other runtime was launched here.

`known-owner.json` pins original owner/CID, exact result/absence/wrapper/watcher
receipts, source binding and composition, both compile databases/contracts, nine
artifact hashes, and every original0962 packet member. The receipt bytes and
actual compile source are the evidence for this local fixture defect; no new
upstream-version assertion or remote research is needed.

## Narrow correction and adapter

`docker-absence.patch` is an UNAPPLIED proposal against the exact0962 `compile.py`
SHA256bc0b8f6a6a2e8e87826ea598fedf45c8415c8e771a34b0fba46d01a1ca64b1de.
It uses typed container inspect and accepts only original exit1, empty/newline
stdout, and a complete not-found diagnostic for the exact full CID. Diagnostic
words allow case differences; CID comparison stays exact. Daemon connection,
permission, extra diagnostics, truncated IDs, live state, and other exit codes
refuse. Existing forced-stop FAIL behavior remains. The predicate is identical
to `recovery.py:absent`; static checks bind the two. Do not apply it to0962 or
start another compile. It is a small prospective correction for review/adoption.

`prepare-recovery.py` performs no subprocess or container operations. It reads
only this owner, verifies all687 source snapshot files (candidate276, repaired
baseline271, sealed fixture140), preserves the old baseline's one-file repair
label, rehashes artifacts/receipts, and creates an exclusive NEW export outside
the original owner. Export ceiling40MiB; the nine existing artifacts total
32,009,440bytes. No build tree or cache is copied. Missing retired source snapshots
refuse rather than manufacturing a new source-verification receipt.

`recovery-acceptance.json` is created only after verification. It names the original
FAIL/exit1, container0, exact later absence evidence, source/contract/artifact
identities, and `runtime_status: UNRUN`. Runtime acceptance independently rechecks
all exported hashes and semantic guards: exact cleanup error only, four stages0,
no timeout, healthy sampler, no forced-stop field, no OOM/resource error, passing
contracts, and typed inspect plus successful complete-ID inventory. Another
owner, changed artifact, added failure, or generic failed build is ineligible.
The already captured post-failure readback is the fresh absence proof relative
to this compile; preparation does not query current Docker state or claim to.

`run-guest.py` is the original sealed runner with the exact diff in
`runtime-adapter.diff`: original packet location, recovery validator instead of
the PASS-only compile guard, and explicit recovery receipt/result metadata.
All target commands, digest264 oracles per build, wrapper comparisons, expected
negative exit2, sanitizers, no-NIC/read-only/tmpfs guards, limits, and process
cleanup are unchanged. Every target's original result remains independently
required. ASan/UBSan are not disabled. This recovery is not runtime qualification.

## Next coordinator commands — UNRUN by worker

Under a NEW watched record-only coordinator owner (no compiler admission needed
for copying32MiB), prepare the export once. Keep originals until its verification
completes; do not replay the completed compile owner.

```sh
REPO=/workspace/repos/rocknix.worktrees/m7-rvz-regressions-574
PACKET="$REPO/docs/qa-logs/2026-10-14-md5-cleanup-recovery"
# Coordinator creates a fresh record owner; its /input must not exist.
EXPORT=/workspace/tmp/REPLACE_WITH_NEW_RECOVERY_OWNER/input
python3 -I -S -B "$PACKET/prepare-recovery.py" \
  --owner /workspace/tmp/pix574-md5-target-20261014 \
  --packet "$REPO/docs/qa-logs/2026-10-14-md5-target-source" --output "$EXPORT"
python3 -I -S -B "$PACKET/controls.py" --input "$EXPORT"
```

Prepared controls cover16 Docker diagnostic shapes, exact known records,
23 independently mutated failure records, and matching/changed/missing file hashes
(**43 controls, UNRUN**). Save original exits/stdout/stderr for preparation and
controls. The export contains `packet/` (original0962), `recovery/` (this packet),
`artifacts/`, compact original receipts at unchanged relative paths, the watcher
exit under `evidence/`, and the new recovery receipt. Keep both sets of results.

Coordinator stages this public export read-only at `/tmp/pix-input/md5` in the
next admitted no-NIC GENERIC_X64 guest and provides the original empty512MiB
scratch tmpfs. Resource admission, serial ownership, staging hashes and retirement
remain coordinator-owned. Exact target entry:

```sh
/usr/bin/python3 -I -S -B /tmp/pix-input/md5/recovery/run-guest.py \
  --disposable-vm --input /tmp/pix-input/md5 --scratch /tmp/pix574-md5-NEW
```

Preserve original guest/serial/watcher exits and `receipts/compile-recovery.json`
alongside all ten target receipts/results. The runtime result embeds the compile
recovery label; never summarize this as an original clean compile PASS. Export
receipts before retiring scratch/artifacts. Original pristine-baseline MD5 UB
remains evidence; repaired-baseline comparisons do not erase it. Independent
format-tool packet1c0e93, full RVZ/Wii-image, frontend, ARM/big-endian, device and
release-image qualification remain separate. Static AST/diff/hash checks are
recorded in `static-result.json`; prepared code and controls were not imported
or executed by this source-only worker. No original packet/product/shared record
was edited.
