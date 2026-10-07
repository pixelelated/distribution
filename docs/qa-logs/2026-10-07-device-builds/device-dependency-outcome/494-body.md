## Purpose

#492 authorizes H700 then SM8550. #491 recovered42.05GiB and establishes the H700 arm-stage budget, but later firmware stages need additional capacity review. #493 measures1.69TB in repositories/build worktrees,1.01TB artifacts and0.76TB temporary QA history. Assess retirement of superseded full VM build trees before recommending another drive.

Initial review candidates only: `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement09`, `replacement10`, `replacement12` and `replacement14` (the latter names share the same full prefix). Their measured gross total is about432GiB. No removal is authorized here, and gross size is not net recoverable space. Keep current16, fallback15, every device tree, actual ROCKNIX baseline and all referenced source/evidence dependencies.

Can this be done on the VM? No: exact host tree ownership, filesystem allocation and preservation dependencies are host facts. Inspection reads originals; bounded independent preservation copies are reversible preparation within the measured build budget. Deletion requires a separately approved concrete proposal. No physical-device action is involved.

## Acceptance criteria

- [ ] An exact-path report identifies each candidate tree/branch/head/dirty state, actual allocated bytes, live ownership and cross-store/backing/source dependencies.
- [x] Independent verified preservation retains required source/licence inputs, build/failed-run evidence and compact QA records; the report measures preservation cost and net reclaim without touching current/fallback/baseline stores.
- [ ] A concrete proposal shows H700 firmware and SM8550 budgets with protected identities and guarded execution commands, and records the explicit deletion decision separately from build authorization.
- [ ] If approved, the standard worktree helper removes only that exact batch; watched terminal records and post-action dependency/space readbacks establish actual recovery. Otherwise leave deletion undone with the reason recorded.

## Dependency review — 2026-10-07 04:39 UTC

Completed read-only discovery inspected 3,825,745 directories, 290 disk chains and 469 artifact manifests with zero scan errors. No matching current container mount or unprivileged process was found. All 52 artifact references are classified as retained historical provenance, with five immutable candidate bundles independently hash-verified. Their cache-copy receipts establish independent regular files.

**Keep replacement12 in this batch:** 14 symlinks from retained QA16/QA17 overlays still reference its source checkout. The remaining proposal candidates are replacement09, replacement10 and replacement14 only, with 348,357,001,216 gross allocated bytes and 348,297,703,424 potential net bytes (324.38 GiB) after charging the full 56.55 MiB preservation store. All four reviewed trees have accepted compact preservation; holding replacement12 does not discard that work.

**Pending administrator readback:** 196 processes had protected fields unreadable as the ordinary user. The read-only helper is prepared at /workspace/tmp/pixelelated-m7-device-root-readback-01 and has been requested; it reads process references only and deletes nothing. This is still a pre-proposal review, not an approved or executed removal.

At04:39, available space was177,227,026,432 bytes and the active H700 arm root22,361,726,976 bytes. Current availability does not fit the later H700 aarch64 budget287,480,930,304 bytes. The proposed three-tree cleanup would fit that stage after the remaining measured arm allowance. SM8550 retains its later347,688,935,424-byte stage budget; both devices with separate full40 GiB growth allowances do not yet fit the combined conservative forecast. Remeasure after H700 and carry out #493's broader retained-image/temporary-QA review before recommending hardware. No assumed cleanup is counted as actual free space.
