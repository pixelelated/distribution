# Build-host storage inventory — #453

The maintainer asked: “With the 4 TB drive, shouldn't we have more than 246 GB
available, or is it because we have multiple builds on disk already?”

Yes: retained build trees, image history and isolated QA data account for the
space. This was a read-only inventory; nothing was deleted or resized.

The main scan ran from 22:39:09 to no later than 22:48:03 UTC on 2026-10-05,
returned zero, and produced no permission/errors. Sizes below are allocated
blocks, not apparent sparse-file sizes. The filesystem was live: candidate12
finished and new image/VM proof started during the scan, so these directory
sizes are not an atomic reconciliation of a single `df` sample.

| Storage group | Allocated GiB |
| --- | ---: |
| Build worktrees | 1776.06 |
| Saved images and artifacts | 917.24 |
| Temporary QA owners and extracted images | 496.55 |
| Shared downloaded source cache | 63.03 |

The primary checkout plus other small repositories add about 2 GiB. Empty
`builds/` and `containers/` directories are not substantial consumers. The
root-owned `lost+found` directory was not traversed; it is not included in
these per-directory totals. All requested accessible scans completed without
errors. Do not infer that filesystem metadata or open-deleted files were
individually inventoried.

The formatted filesystem provides 3.5805 TiB (3.9368 TB). At the first sample,
245.35 GiB was available and 186.32 GiB was free but reserved. At 22:48:16,
after new outputs/extraction/VM allocation, available space was 221.01 GiB;
the reserved amount remained 186.32 GiB. The exact later byte counts are in
`disk-capacity-after.json`. Decimal drive capacity, binary reporting and the
filesystem reserve explain part of the difference; retained data explains
most of it. No reserve setting was changed.

## Largest consumers and what they retain

- `rocknix.worktrees/devices`: 464.79 GiB across six device/architecture roots.
- Individual GENERIC_X64 roots: roughly 104–117 GiB each, including toolchains,
  unpacked source, intermediate objects, installed payload and outputs.
- `artifacts/rocknix-images`: 864.44 GiB across 490 immediate directories.
  Some are image sets of roughly 3.86–4.14 GiB; others are smaller evidence
  directories. Directory count is not a count of released builds.
- `artifacts/pixelelated-candidates`: 38.86 GiB of immutable candidate bundles
  at scan time. These bind inputs, image/update artifacts and build evidence.
- Temporary QA owners include sparse guest disks, extracted system trees,
  diagnostic captures and process receipts. Several extracted owners consume
  12.42 GiB each; completed opt-in QA owners use about 14.16 GiB each.
- The shared source cache is 63.03 GiB and avoids downloading inputs again.

## Concrete reclaim proposal — not authorization to delete

First review the superseded build trees below. Their aggregate footprint is
**539.33 GiB gross**; preservation archives, hard-link relationships and live
allocation changes may reduce the eventual net recovery. The exact measured
bytes are recorded in `inventory-receipt.json`.

- `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement03`: 107.79 GiB.
- `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement05`: 107.80 GiB.
- `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement06`: 107.82 GiB.
- `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement07`: 107.89 GiB.
- `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement08`: 108.04 GiB.

For each proposed tree, before requesting removal: verify clean tracked state,
no running owner/container, recorded source/recipe/archive and output hashes,
retained candidate bundle and logs, and every downstream QA/backing dependency.
Preserve any unique consumed source, unstripped diagnostic binary, source/licence
input or failed-run evidence still needed. A directory being old or reproducible
in principle is insufficient evidence that it is safe to delete. Then present
the exact preservation destination, named deletion and revised net estimate
for approval; approved worktree removal uses `tools/fork-worktree remove`.

Exclude current replacement12 and its build/image/QA owners; qualified10 and
its consumed proxy source/host qualification; source09 and its cloud evidence;
all immutable candidate bundles; the original September29 ROCKNIX RC2 image;
all retained upgraded COW disks and their full backing chains; source cache;
and active source/licence inventory. Preserve failed attempts and their logs.
No generic age-based or wildcard cleanup is proposed. Work on #453 is inventory
and proposal only; an approved cleanup should receive its own named execution
record. The ongoing VM qualification remains the critical path.
