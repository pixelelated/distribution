# Device builds and build-storage assessment — October 7, 2026

The exact #491 cleanup is approved, completed and independently accepted:
22 files removed,42.05GiB recovered, seven protected identities, two held base
hashes and2,695 independent evidence hashes verified. The full execution and
acceptance are in ../2026-10-07-pixelelated-replacement-16/h700-qa-retirement-01/.
No other removal or filesystem-reserve change occurred.

## H700, then SM8550 — #492

Current04 runs fromf5f815faff4e18808d2c1c0298e4335cc0b20fe7 in
`/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01`, branch
build/m7-pixelelated-h700-01. Owner `/workspace/tmp/pixelelated-m7-h700-arm-04`,
run20261007T041821Z-41e78f9d; launcher2241024/watcher2241026. Actual pinned
container/mounts, seven sealed inputs and live processes are verified in
h700-arm04-start. Full compatibility completion is not yet claimed.

#495 fixes the exact [upstream GCC12 diagnostic](https://github.com/KhronosGroup/SPIRV-Tools/issues/6919)
by keeping that one warning nonfatal only for GCC12 host compilation. Current
SPIRV pins and all target flags remain unchanged. Original-failing/O0/loop/
warning-only controls and unrelated-warning rejection are in spirv-host-control01.
The actual installed host package now passes nine assembly/validation/roundtrip/
optimization checks, including invalid nested structure layout rejection; its
stamp/executables were independently hashed. Only this host recipe differs
from qualified16 product sources. Container988c0ba58626 and24/4 concurrency
remain pinned.

Arm01's compiler failure, full thread/stamp archive and five interrupted scopes
are retained; those scopes were moved aside without deletion before repair.
Arm02 correctly refused exhausted swap before compilation. The authorized
fixed helper restored8GiB free before03. Arm03's package succeeded, but its
final proof hashing used a Python3.11 API unavailable in pinned Python3.10;
#496 fixes only that receipt writer, and fresh04 reran the nine checks. All
three failed owners retain their original nonzero results and verified exits.

Next: finish/verify arm, complete#494 measured capacity review, build/verify
H700 aarch64 DDR3/DDR4, then capacity-check/build/verify SM8550. No physical
action or release publication is part of compilation approval.

## Further retention — #494

The completed read-only review verifies four old VM trees09/10/12/14 and
464,527,437,824allocated bytes (432.62GiB gross). Selected custody comprises
14,489unique objects;13,925have independently verified prior copies and only
15,371,743new content bytes were copied. The preservation/source-inventory
owner completed at 04:24 UTC with four zero result channels, nine unchanged
seals and verified process exits. The new independent store uses 59,297,792
allocated bytes (56.55 MiB), leaving 464,468,140,032 bytes (432.57 GiB) of
potential net recovery. All four 568-root source inventories have zero errors.
Primary acceptance independently hashed all 14,489 objects, checked the four
tree manifests and verified separate destination inodes and intact originals.
See `retention-preservation01` and `retention-acceptance01`.

This is not recovered space or removal approval. Full dependency review and a
fresh privileged process readback remain before a concrete removal proposal.
Current16/fallback15 and old device roots remain protected. The dependency
owner is `/workspace/tmp/pixelelated-m7-device-dependencies-01`, using the
standard watcher and read-only discovery across the build, source, image and
temporary stores.

## Current storage — #493

Read-only sizing02 finished03:57:20UTC. Allocated bytes are used, including
sparse-file allocation rather than apparent virtual sizes. Major areas:

| Area | Decimal TB | GiB |
| --- | ---: | ---: |
| Repositories and build trees | 1.689 | 1572.65 |
| Image and retained artifact stores | 1.013 | 943.33 |
| Temporary QA/build work | 0.762 | 709.68 |
| Shared downloads | 0.068 | 63.20 |

At completion the filesystem reports191.28GiB available and186.32GiB
reserved free space. The reserve was not changed. The sole unreadable path
was root-owned /workspace/lost+found; therefore this is explicitly not a fully
readable inventory. The du total and filesystem-used snapshot differ by about
3.23MiB; concurrent writes mean that difference does not measure that directory.
Raw host path inventory remains local, with its hash and location in
storage-sizing02/summary.json. Every major project area was measured.

The total is accumulated history. Most full VM build trees are about108–110GiB;
the old multi-device tree is464.79GiB. The rocknix-images area alone is864.44GiB,
and temporary QA data is709.67GiB. These totals are not all disposable: current,
fallback, baseline, source/licence and referenced failure evidence remain protected.

### Expansion recommendation so far

Hold off on a purchase until the next retention review establishes net usable
space. #494 is read-only review of replacement09/10/12/14, roughly432GiB gross.
It must first verify dependencies and independent preservation, subtract the
preservation cost, then obtain explicit removal approval. Gross historical
allocation is never counted as available space. The191.28GiB measured before checkout only establishes
the H700 arm stage; aarch64 and SM8550 are still measured at their stage gates.

A second4TB drive in RAID0 would provide about8TB decimal (7.28TiB) before
filesystem/metadata overhead. RAID0 stripes data and has no redundancy; it is
appropriate only for data whose loss can be recovered acceptably. A separate
build volume could add the same aggregate capacity without combining the two
volumes into one failure domain. No build-speed gain has been measured here.
See [Red Hat's RAID-level documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_storage_devices/managing-raid)
and [Linux MD documentation](https://docs.kernel.org/admin-guide/md.html).
The maintainer clarified RAID0; no RAID conversion or purchase was requested.

### Requested post-build review

The maintainer's latest request is quoted verbatim in #493. After this build
and its required qualification, review the large build, image and temporary
QA stores for maximum safe recovery. #494 is the bounded four-tree proposal
needed for upcoming firmware stages; it does not exhaust the broader review.

Use the existing D-INFRA-018 retention cadence: after qualification, and
before the next capacity-intensive build or QA copy. Keep the current useful
build tree, a qualified fallback per device/architecture, the actual ROCKNIX
upgrade baseline, exact source/licence inputs and independent failure/QA
evidence. Resolve transitive backing-file, custody-store and live-process
dependencies before proposing retirements. Each proposal records preservation
cost, net recovery and the next workload's full footprint. Execute only an
approved exact batch using the existing guarded helpers and watched owners.

Measured historical SM8550 roots occupy 175,974,195,200 bytes together. The
planning budget is 347,688,935,424 bytes, including 100 GiB operating allowance,
40 GiB growth, 18 GiB artifacts and the measured checkout. This is an estimate;
remeasure available space after H700 and any approved cleanup before starting
SM8550. See `device-capacity-measurements.json`. The broader report will use
these workload budgets to determine whether another drive is warranted.

The first H700 compiler failure was GCC12/SPIRV host compatibility (#495),
not evidence of a disk-full compiler failure. Disk availability separately
constrains later build stages. Host repair/proof issues #495/#496 are closed,
published on next `63ef759a`, with both hosted checks passing. Publication and
CI receipts are in `publication12` and `publication12-ci`; the refreshed live
M7 order is retained in `post-build-storage-order`.

The original sizing01 attempt was correctly refused by the one-job-per-worktree
watcher lock before running. Sizing02 used the idle primary checkout. That refusal
is retained; it is not a failed filesystem scan. Four zero wrapper channels on02
mean its observation was recorded, not that the unreadable lost+found was inspected.
