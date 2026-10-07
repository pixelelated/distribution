# Device builds and build-storage assessment — October 7, 2026

The exact #491 cleanup is approved, completed and independently accepted:
22 files removed,42.05GiB recovered, seven protected identities, two held base
hashes and2,695 independent evidence hashes verified. The full execution and
acceptance are in ../2026-10-07-pixelelated-replacement-16/h700-qa-retirement-01/.
No other removal or filesystem-reserve change occurred.

## H700, then SM8550 — #492

**H700 arm compatibility is accepted.** Owner
`/workspace/tmp/pixelelated-m7-h700-arm-05` completed at 04:50:21 UTC from
frozen `43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa`, branch
`build/m7-pixelelated-h700-01`. All 244 tasks completed, all four result
channels are zero, seven sealed inputs match and the actual container/owner
exited. Independent acceptance verified 7,866 files, 797 symlinks, 938 ARM
ELF objects and 244 build stamps, including RetroArch and libretro cores.
The acceptance owner also has four zero results, two seals and verified
exits. See `h700-arm05` and `h700-arm05-acceptance`.

This is the compatibility output needed by the later H700 aarch64 firmware
build. No bootable H700 firmware, physical smoke or release claim is made.
At 04:50:50, 173,770,547,200 bytes (161.83 GiB) were available, below the
287,480,930,304-byte (267.74 GiB) firmware-stage budget. #494's proposed
three-tree retirement would fit that stage, pending the read-only root
process check and exact deletion approval. See `h700-post-arm-capacity.json`.

### Repairs and preserved failures

#495/#496 are completed: the exact upstream GCC12 SPIRV diagnostic is kept
nonfatal only for host compilation, with the source pins and target flags
unchanged. The installed host tools pass nine shader controls. Failed01
retains its compiler evidence and interrupted scopes; failed02 retains its
swap preflight refusal; failed03 retains the incompatible Python receipt
writer. Original failed results are never replaced by later success.

Failed04 reached 228/244 and successfully linked box86, then tried to copy
from `build.ROCKNIX-H700.arm`. The canonical root uses DISTRONAME=pixelelated,
while DISTRO remains the ROCKNIX configuration namespace. #497 fixes the
same mismatch in box86, lib32, RetroArch, gpSP, DeSmuME, Daedalus and
build_distro cleanup/device-root paths. Forty-two original/fixed hook and
lifecycle controls pass, including unchanged ROCKNIX and missing-payload
cases; all six package lints pass. Initial control01's JSON-spacing assertion
remains failed; fresh02 checks document contents without weakening payload
assertions. See `build-root-controls02` and `h700-arm04-failed`.

Recovery01 archived thread/stamp evidence and preserved all six interrupted
package scopes and changed recipe outputs by same-filesystem rename, with
zero payload deletion. Only then was the stopped build checkout advanced.
The source repair is feature `dba99f4b57` / next `43d0bc3bf4`; the full
qualified16 product delta is these seven generated-path files plus the
earlier SPIRV host-only hook. No source pin or stored data format changed.
#497 stays open for the real aarch64 handoff/image evidence.

Next: finish the scoped process dependency check and exact #494 capacity
proposal, then build and verify H700 aarch64 DDR3/DDR4. After H700 artifacts
verify, remeasure capacity and build SM8550. The broader post-build retention
review remains #493; physical operations and release publication stay separate.

## Further retention — #494

The original read-only review covered replacement09/10/12/14, totaling
432.62 GiB. Independent preservation is accepted: all 14,489 objects verify,
all four 568-root source inventories have zero errors, and originals remain
intact. The new store costs 56.55 MiB. See `retention-preservation01` and
`retention-acceptance01`.

Full dependency discovery completed at 04:36 UTC: 3,825,745 directories,
290 disk chains and 469 artifact manifests, with zero scan errors. All 52
artifact references are classified as historical provenance; five referenced
immutable bundles independently pass their manifest/byte checks. Their cache
receipts record checksum-equal, independent files. The accepted custody
retains referenced owner logs and results. See `retention-dependencies01`
and `retention-classification01`; the full private discovery report's hash
and location are retained in the summary.

**Keep replacement12 in this batch.** Fourteen symlinks from retained QA16
and QA17 overlays still use its source checkout. Replacement09/10/14 remain
the proposal candidates: 348,357,001,216 gross allocated bytes, or
348,297,703,424 potential net bytes (324.38 GiB) after the full preservation
cost. No data has been removed. Current16/fallback15, replacement12, every
device root, ROCKNIX baseline and independent source/custody stores stay
protected.

Ordinary-user discovery found no matching active process or container mount,
but 196 processes had protected details unreadable. The scoped read-only
administrator check has been requested from
`/workspace/tmp/pixelelated-m7-device-root-readback-01`; its source/checksum
and scope are retained in `root-readback-request`. It installs/deletes
nothing. A readable process check still precedes the concrete exact removal
proposal and separate deletion approval.

At 04:39, current availability did not fit H700 aarch64's 267.74 GiB stage
budget. The three proposed removals would fit that stage after the remaining
arm allowance. SM8550 retains a later 323.81 GiB stage budget. Both devices
with separate full 40 GiB growth allowances do not yet fit the combined
conservative forecast; remeasure after H700 and use the broader #493 review
if necessary. See `device-capacity-after-dependencies.json`. Proposed
recovery is never counted as actual free space.

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
space. #494 narrowed its original four-tree review to replacement09/10/14, with replacement12 held for retained QA source links. The three-tree potential net recovery is324.38GiB.
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
QA stores for maximum safe recovery. #494 is the bounded three-tree proposal after dependency review
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

The dated image-store inventory includes 104 x64-prefixed directories using
417,036,288,000 allocated bytes and 117 H700-prefixed directories using
440,225,484,800 bytes, together about 798 GiB. Prefixes define review groups,
not deletion eligibility or verified contents. `post-build-image-groups.json`
binds these totals to the original sizing report; refresh after qualification.

Publication13 and both hosted checks are accepted on next `70e41ca3`.
The later dependency findings and administrator-check request are recorded
in the live milestone/issue readbacks under `device-dependency-outcome`.
