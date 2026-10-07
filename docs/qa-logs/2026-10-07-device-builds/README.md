# Device builds and build-storage assessment — October 7, 2026

The exact #491 cleanup is approved, completed and independently accepted:
22 files removed,42.05GiB recovered, seven protected identities, two held base
hashes and2,695 independent evidence hashes verified. The full execution and
acceptance are in ../2026-10-07-pixelelated-replacement-16/h700-qa-retirement-01/.
No other removal or filesystem-reserve change occurred.

## H700, then SM8550 — #492

H700 arm compilation started03:59:39UTC under the standard watcher:
`/workspace/tmp/pixelelated-m7-h700-arm-01`, run20261007T035939Z-a3256af0,
launcher1635390/watcher1635395. The actual Docker image and mount readback is
retained in h700-arm01-start. Submission is not completion.

Frozen worktree: `/workspace/repos/rocknix.worktrees/m7-pixelelated-h700-01`,
branch build/m7-pixelelated-h700-01, distributionc7e3bcd6b5634fc4841488ac724d6f619c994d0f.
All product paths equal qualified16ee014909;6,550source files,207QA files and
180symlinks are sealed. The private input manifest hash is
`e8e6325baabbdd80c4da6ebf6b4995d07b19b12298dd1138ebe20a295f70beaf`.
Pinned container988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39;
24global jobs and WebKit4. This is a cold independent compatibility root,
using the shared downloads and preserving the old device tree.

The guarded swap helper restored8GiB free swap before any new build watcher
started; preflight reports35,215MiB available RAM and READY. Available disk
after the2.06GB checkout still exceeds the185.98GiB first-stage budget.
The initial1GiB checkout allowance was lower than actual checkout allocation;
the subsequent actual-space assertion passed before build submission.

Next: finish/verify arm, remeasure H700 aarch64 capacity and build/verify its
DDR3/DDR4 artifacts, then remeasure and build SM8550. #494 owns further retention
review; #493 owns this storage assessment. No physical action or release
publication is authorized by build approval.

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

The original sizing01 attempt was correctly refused by the one-job-per-worktree
watcher lock before running. Sizing02 used the idle primary checkout. That refusal
is retained; it is not a failed filesystem scan. Four zero wrapper channels on02
mean its observation was recorded, not that the unreadable lost+found was inspected.
