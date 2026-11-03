# T3 → wN:p2: T46 current metadata binding

Bounded preparation under [#693 comment6602308433](https://github.com/pixelelated/distribution/issues/693#issuecomment-6602308433), read in full with the owning issue. T46 is next after verified T44 and remains the last source-reading slice. This report starts no audit or execution.

Actual executor: Codex / GPT-6-Astra / xhigh, T3 wN:p6, session01a19d12-29e3-7fe0-9f41-038dac0a5deb; actual harness label, not provider attestation. All shell/subprocess commands use CPUs8–23. Every Git invocation uses the absolute read-only root /workspace/repos/pixelelated/distribution.worktrees/m6-renovation-plan-346.

## New transition only

Old snapshot: 92e8d07b6163ec5ddd3e9b67f1c42a472b2911d1.
Current candidate: d707c82ab8c48b674acc1f95a9571f0cb24d226a.
Candidate root tree: b3ce6c6ea70d9d40ff2b74fff691a0a11f70e437.

**126,670 → 127,469 paths: 799 added, 0 deleted, 4 changed, 126,666 unchanged.** Raw Git diff and independent two-tree metadata agree on keys and old/new mode/object identities. All four changes are blob changes; there are no mode/type changes. Rename detection is disabled.

Logical bytes: **2,173,665,613 → 2,190,843,187**, +17,177,574. Additions contribute17,158,827; changed files rise from374,355 to393,102 bytes (+18,747). Unique blobs:37,761 →38,355. Unique-blob logical bytes:1,068,422,827 →1,084,128,032. The current selection references597 newly seen unique blobs and no longer references3 old unique blobs; that describes the selected paths, not deletion from the Git object store.

Current types:127,469 blobs. Modes:98,024×100644 and29,445×100755; zero symlinks/gitlinks. Logical bytes do not measure packed/disk storage, runtime cost or reclaimable savings.

| Canonical root | Old paths | Current paths | Added / deleted / changed | Logical-byte delta |
| --- | ---: | ---: | --- | ---: |
| .github/sessions | 356 | 356 | 0/0/1 | 1,907 |
| docs/audits | 59,693 | 59,693 | 0/0/0 | 0 |
| docs/futros | 17 | 17 | 0/0/1 | 3,488 |
| docs/qa-frames | 970 | 970 | 0/0/0 | 0 |
| docs/qa-logs | 64,815 | 65,613 | 798/0/0 | 17,152,553 |
| docs/retros | 8 | 8 | 0/0/0 | 0 |
| docs/retrospective | 1 | 1 | 0/0/0 | 0 |
| docs/reviews/inventory.json | 1 | 1 | 0/0/0 | 0 |
| docs/work-logs | 94 | 95 | 1/0/2 | 19,626 |
| research | 715 | 715 | 0/0/0 | 0 |

## Reused historical facts and source binding

The previously retained report.json at the current pin has SHA256713f999d552cdacce9e59bd062ac7b410b11ce26bf427860412b09de185a0b98; the old deriver has SHA2561eea99da03a27a158fc987677618b4b0de0ee55e27356cca233792b6b0583d94. Both were read; the deriver was not executed. Its prior coordinator counts, raw listing digest and canonical metadata digest match the old side of this new transition exactly.

Reuse, not recomputation: survey126,149 rows /22,984,582 inventory lines /15,392,661 generated “read” lines; P1 matching paths126,150. Those survey facts describe eb4763e3cc9bcd729830cd85f1719bbd4f28db10, generated2026-10-23T02:20:48Z, hosted at P1 2174265e9cc1b248c0fbe27fa101875984d46d6b. T46 remains a table; the generated CODE-language read tally is not an audit reading budget.

All canonical mode/type/blob/size identities match both old and current snapshots and the retained P1 report:

| Input | Full blob OID | Bytes |
| --- | --- | ---: |
| inventory.json | 9133125cd2d28180aafdfda79668241943bf9e3d | 33,229,468 |
| areas.json | ed033ea67c1ed0d147afbfcf1ab691aa46a5d8aa | 4,975 |
| slices.json | e64965a5493ebd1da3829069e98a845a96de5b26 | 52,223 |
| tools/renovation-inventory | af18e40cf8cb75496e7bb00b4059daed4792c94a | 85,435 |

The unchanged selectors therefore retain the original records roots and empty additional slice filter. Current canonical input bodies were not reread/recounted; their retained SHA256 values are reused by identical Git blob identity.

The inventory self-row is explicitly historical:134,637 stored lines, last_fork_commit a2cfa82233 2026-10-23. It is not a measurement of current inventory output. Already committed prior preparation files belong to the pinned input snapshot normally; this new report/comparator lives outside that tree and is not counted as its own input.

## Reproducible metadata-only comparator

The new compare-metadata.py reads the exact retained report, verifies canonical input identities, reads the two frozen path/mode/type/blob/size maps and raw diff, reconciles counts/digests and emits only grouped metadata. Complete path sets remain in memory. It never executes the old deriver, inventory generator, checker/test or any producer.

```sh
taskset -c 8-23 python3 -B /tmp/m6-t46-current-metadata-t3-20261103/compare-metadata.py --old 92e8d07b6163ec5ddd3e9b67f1c42a472b2911d1 --new d707c82ab8c48b674acc1f95a9571f0cb24d226a --prior-ref d707c82ab8c48b674acc1f95a9571f0cb24d226a --out /tmp/m6-t46-current-metadata-t3-20261103/result
```

Use a fresh private --out directory when reproducing; it refuses an existing output directory. Only the source pins, selector bindings and canonical result payload determine metadata values. created_at and the recorded invocation path/output directory naturally differ when rerun or relocated.

Exact Git argv, per-command output hashes and input mode/type/blob/size bindings are in result/report.json. Prior read commands, API body digests and this invocation's tool result are in provenance.json. Named source roots and group counts/digests are the only path population information exported; no credential-labelled individual paths or contents are printed or persisted.

- result/report.json SHA256: dec206e032e9ff00ac715bbc88410a66fe3e43be3bc6e779c30aa6d39a59f7be
- compare-metadata.py SHA256: d31413619e63fc1fe22cc30bf5996df8040aab77fa6509688f6cd58b1abae061
- Current raw ls-tree SHA256: b3f1be7ba504ab292928c1b9e5a15f3c24e587a0faa1cc3733cd9afef5481157
- Current canonical metadata SHA256: 83198fe7208e0e4e6b70b13b0ebc78a02f54b67d18a16bd0ecfc6193ab4c6eb0
- Current path-set SHA256: 8fdb11cc06194fb1937f27d5eb7fefb70cbd5a0da0a1c6839eb1dd9fea6bf99f
- Raw transition diff SHA256: 54e5167d19f12fbf66047560dcc4e05bb8d293f481bfc14607764fc27ecda969

## Boundaries and stop

No body sweep, own audit, membership recut, baseline selection, lane-branch union or integrated-next claim. No source/tree exports, live-tree scan, private/held/cache/process/host inspection, cleanup, repository/ledger/tracker/kit/shared-ref write, accepted producer/test/checker replay, build/guest/runtime/fetch/provider/device/cloud action or permission answer. T41 and historical trees are untouched.

P1's direct reader routes and T1's accepted-T39 bridge remain separately assigned work. Root writes the baseline, brief, criteria, source cutoff/branch context, epic/parent placement and dispatch. **Stop at this factual return.**
