# #519 old-helper synthetic proof

**13 distinct controls qualify** against distribution
`43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa`, with real rclone1.75.1 and
an alias to a disposable local filesystem. Network namespaces have no network.
Inputs use only public old-default constants and invented QA payloads.

The exact held `flock` inode is probed from inside each sandbox before and
after the helper; its release is also witnessed. Every fixture first executes
real rclone and reads a known synthetic sentinel. Production input hashes match
the old commit; the existing fixture's device-id stub is explicitly recorded.

- Unguarded join and follow rewrite local pointers despite the transfer lease.
- Matching historical-path keep guards preserve pointers for join, follow,
  settle and folder scan. The local-only `--needs-step` returns1 without rclone.
- A mismatching guard permits follow. Even a matching keep on the current
  default does not suppress direct join: this guard is not a universal stop.
- Backup, restore, content backup, content restore and migration apply return75
  under the lease. The content scripts do read-only discovery first, including
  old restore's account-root fallback; the lease is not a network barrier.
- All synthetic local saves, recovery, credentials, auto0 settings and remote
  bytes retain their exact hashes. No transfers or deletions were observed.

`helper01` retained11PASS/2FAIL. Those failures were an overstrict assertion
that a locked content writer must not start rclone at all. Source and argv
show read-only discovery before lock refusal. Only those two controls were
rerun with the corrected assertion in `helper02`, both PASS. The two harness
versions, raw transcripts, comparison hashes and watched terminal receipts
remain intact. Heavy fixture copies were retired after their terminal runs.

`qualification.json` maps each accepted result to its run;
`pinned-source-verification.json` independently verifies all15executed fixture
input sets against the source pin and confirms protected-byte equality even
in the initial rejected controls. `source-evidence.json` binds cached
SystemConf, ES startup/game-exit commands and the independent boot folder
predicate to ES72494bc72e3d64d4dcfeb4e6478052bbdf166c5b. **These are source
claims, not ES runtime execution.** No fabricated frontend or systemd model
was used. No device, external provider or shared UI guest was contacted.

Transaction/fault/rollback/restart/systemd proof and bounded state readback
remain outside this artifact. The private operational plan and values are
not included. The transfer/reboot gate is not satisfied by this host proof.

Run the finite proof with the explicit source root, existing fixture tool,
pinned rclone and a fresh output directory:

```sh
python3 old-helper-proof.py --source-root /path/to/distribution \
  --fixture-tool /path/to/tools/rasteratops-cloud-layout-test \
  --rclone /path/to/rclone-1.75.1 --output /fresh/synthetic/output
```

The frozen file index is `freeze.json`; changing a listed byte invalidates it.
