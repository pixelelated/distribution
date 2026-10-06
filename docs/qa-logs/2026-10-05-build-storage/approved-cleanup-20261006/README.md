# Approved five-tree cleanup complete — #459

Removed only replacement03/05/06/07/08 under D-INFRA-017. Each successful run
has four zero result channels, actual helper/owner process exits, directory
and worktree-registration absence, and retained branch/head verification.
All protected paths and preserved artifacts remain. No reserve setting changed.

The live filesystem sample increased from **37.11 GiB available to
576.45 GiB**, recovering **539.34 GiB** (579,115,601,920 bytes).
The earlier 524.84 GiB net estimate subtracted preservation storage; those
stores already existed in this execution's before sample. Do not subtract
their cost twice. Small concurrent host allocations can affect this measured
delta; it is not an atomic per-directory accounting claim.

| Tree | Successful owner suffix | Terminal UTC, October 6 | Result |
| --- | --- | --- | --- |
| replacement03 | `03-v2` | 03:28:09 | Removed; branch retained |
| replacement05 | `05-v3` | 03:30:24 | Removed; branch retained |
| replacement06 | `06-v3` | 03:31:17 | Removed; branch retained |
| replacement07 | `07-v3` | 03:32:06 | Removed; branch retained |
| replacement08 | `08-v3` | 03:33:23 | Removed; branch retained |

Owners are under `/tmp/pixelelated-approved-cleanup-`; their complete receipts
are retained in this directory. Never replay any completed or failed owner.
The original unsubmitted owners and v2 owners06/07/08 are obsolete preparations,
not outstanding work. The root watcher stopped automatically after its
03:33:14 UID0 snapshot saw all five directories absent, with zero matching
references and unreadable fields. Actual PID2780340 absence is verified.

## Final retention verification

Final read-only owner `final-01` finished03:34:03 with all four results0;
actual runner/watcher/command process absence verified03:34:30.

- Rehashed all **15,206 retained files**, plus the current candidate's
  **19 bundle files**: 15,225 files / 47,029,011,798 bytes total, no mismatch.
- Verified all15retention manifests,27git source inputs/submodules and12
  protected path identities, including current/protected worktree heads.
- The original frozen14 verifier passes: product/QA source files and symlinks,
  host-options hash, container identity and build concurrency are unchanged.
- Re-read all230surviving disk backing chains; no dependency points into a
  removed tree. The only five missing disks are the removed internal test
  fixtures. Discovery scope remains the four project roots and qcow2 suffix;
  directory symlinks were not followed during the preflight inventory.
- Reserved bytes remain200,056,127,488. Current14, unbuilt13, retained12,
  qualified10, source09, all bundles, RC2/backing chains, shared source cache,
  recovered rclone input and all three preservation stores remain protected.

`final-verification.json` records exact byte counts, branches, source hashes,
per-removal space samples and the final verification. Full initial retention
and disk-discovery reports remain at their recorded local paths with published
digests. The failed runtime-01 preservation store remains because accepted
runtime-02 references its reverified objects.

## Failures retained and corrected — #460

Original03 failed03:22:47/allfour1 after Git encountered owner-owned0555 Go
module directories and partially deleted/unregistered the tree. Watched
repair03 restored registration at02163b4 and its exact saved branch/diff;
allfour0 and actual exits verified before fresh03-v2. Already-removed build
intermediates were not reconstructed. The original failure remains failed.

The first permission-preflight version refused05's empty root-owned Docker
mountpoint before mutation or Git removal;05-v2 remains failed/allfour1.
The final helper permits empty-directory removal through the writable parent,
and repairs only necessary owner-write/search bits on owned nonempty
directories after a complete scan. It leaves files and symlink targets alone.
Six isolated regression controls pass; see
`../../2026-10-06-worktree-permissions/README.md`.

This host-tool fix is now the normal forced-removal path. No running tool was
edited. The two original failures, their source versions, repair and every
fresh owner are retained rather than rewritten as successful attempts.

## Release status

Frozen replacement14 remains7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2,
bundleb77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1.
No product or VM qualification result changed. Nothing is running and no
disconnected alert is armed. Remaining P3 dedicated RA/Dropbox account proofs
and upstream preparation precede P4, H700 and separately gated physical/P5
work. Cleanup success is not an RC/device-ready claim.

Can this be done on the VM? No: these are host filesystem/worktree operations.
All five removals were already explicitly approved. No wider cleanup,
filesystem reserve change, physical device or personal-cloud action occurred.
