## Purpose

#492 authorizes H700 then SM8550. #491 recovered42.05GiB and establishes the H700 arm-stage budget, but later firmware stages need additional capacity review. #493 measures1.69TB in repositories/build worktrees,1.01TB artifacts and0.76TB temporary QA history. Assess retirement of superseded full VM build trees before recommending another drive.

Initial review candidates only: `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09`, `replacement10`, `replacement12` and `replacement14` (the latter names share the same full prefix). Their measured gross total is about432GiB. No removal is authorized here, and gross size is not net recoverable space. Keep current16, fallback15, every device tree, actual ROCKNIX baseline and all referenced source/evidence dependencies.

Can this be done on the VM? No: exact host tree ownership, filesystem allocation and preservation dependencies are host facts. Inspection reads originals; bounded independent preservation copies are reversible preparation within the measured build budget. Deletion requires a separately approved concrete proposal. No physical-device action is involved.

## Acceptance criteria

- [ ] An exact-path report identifies each candidate tree/branch/head/dirty state, actual allocated bytes, live ownership and cross-store/backing/source dependencies.
- [ ] Independent verified preservation retains required source/licence inputs, build/failed-run evidence and compact QA records; the report measures preservation cost and net reclaim without touching current/fallback/baseline stores.
- [ ] A concrete proposal shows H700 firmware and SM8550 budgets with protected identities and guarded execution commands, and records the explicit deletion decision separately from build authorization.
- [ ] If approved, the standard worktree helper removes only that exact batch; watched terminal records and post-action dependency/space readbacks establish actual recovery. Otherwise leave deletion undone with the reason recorded.


Current04:25UTC: the watched preservation/source-inventory owner completed with four0/nine unchanged seals and actual exits. All four568-root source inventories have zero errors; selected custody uses independently verified existing objects plus15,371,743new content bytes (59,297,792allocated bytes including manifests). Originals remain unchanged. The fresh full dependency scan is running; the broader post-build storage request is quoted and tracked in #493. No further removal has been approved.
