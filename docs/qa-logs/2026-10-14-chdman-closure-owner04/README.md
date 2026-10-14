# CHD runtime closure — prospective owner04

Coordinator-only binding update from c24a32c1d3e1a9977d3226a9baf17a677d3567e5. Every Python executable byte is unchanged. New bindings name build owner04, source1015ccf0 and its revised plan (shared libgcc/shared libstdc++). The two source-patch contracts and all target hashes are read from the actual sealed plan/successful consumed original build. Existing retained runtime hashes already include matching libgcc_s.so.1 and libstdc++; no loader/ELF/version acceptance checks are removed.

Original owner03 documentation/static evidence remain under prior-owner03 names; previous failure and worker packets are untouched. Hardcoded owner03 wording in two failure messages is historical wording, not the source of input identities. Runtime UNRUN. No target binary hash is guessed. Static review records unchanged executable bytes/ASTs, recursive manifests and explicit source/plan identities in rebind-review.json.

After actual build PASS and consumption, prepare once:

```sh
python3 -I -S -B docs/qa-logs/2026-10-14-chdman-closure-owner04/plan.py --checkout /workspace/repos/rocknix.worktrees/m7-player-setup --owner /workspace/tmp/pix574-chdman-closure-20261014-04
```

Then the unchanged report/admission/watch-build-submit protocol uses run-stage.py --checkout COORD --owner OWNER --stage chdman-closure. Fresh180s/4GiB/no swap/2CPU,1GiB sampled new scratch; readonly completed work/SDK/plan/receipts and readelf only. No compiler, target or loader execution. Consume original channels and exact cleanup before staging the bundle to a fresh no-NIC VM. Old original family clock is never reused.
