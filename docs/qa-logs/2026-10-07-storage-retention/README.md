# Storage retention review — #493/#494

## Completed cleanup — October 7, 06:38 UTC

The authorized batch removed all 850 selected VM/firmware files, the 30 paths
holding ten extracted copies, and four old worktrees. The filesystem readback
measured **2,117,325,385,728 bytes recovered** and **2,290,757,619,712 bytes
available** after final verification. All 51,070 retained records, 14,489 source
custody objects and five test-required firmware files still match their hashes.
There are 415 retirement markers beside retained records. The standard
`tools/fork-worktree remove` helper removed all four trees; none remains
registered. Four terminal results are zero, eight sealed inputs match and the
actual cleanup processes have exited. See `completed/`.

**Administrator-check limitation, #498:** the supplied UID0 snapshot read every
process without access errors, but its directory-only scope omitted 14 loose
firmware files directly in the image-store root. These files were explicitly
authorized and passed hash, ordinary-user live-reference, container and external
reference checks. Do not claim the administrator snapshot covered them. This
was discovered after deletion while adding retirement markers; the original
sealed receipts remain unchanged, with a separate scope-gap record. The current
executor now refuses any target outside the administrator roots; eight isolated
controls include this omission and covering-parent cases. These later controls
do not retroactively validate the old root scope.

The marker writer's first attempt assumed every inventory group was a directory
and failed before writing markers. Its corrected run uses the containing
directory for loose files. No additional payload was removed by that correction.

H700 aarch64 firmware started at 06:38:36 after a passing capacity check and
guarded swap reclamation. The actual pinned container, frozen checkout and
watcher are verified. SM8550 follows verified H700 artifacts. No firmware
completion, physical boot or RC designation is claimed. #493 remains open for
classification of remaining historical stores and the continuing retention
cadence; the majority-scale batch is complete. Older preparation below remains
the record of how that batch was selected, not a request to execute it again.

## Historical preparation

The maintainer moved broader cleanup ahead of the next firmware stage and
made large testing artifacts temporary (D-INFRA-021, D-INFRA-022). Keep one
only for a named active or immediately queued test, with an owning issue and
release condition. Remove it when that testing finishes and its compact record
is accepted. Generic fallback or historical interest is insufficient.
H700 arm is accepted; firmware compilation is waiting on capacity.

The fresh read-only census covers temporary QA data and the retained firmware
store: 712.43 GiB and 864.44 GiB respectively, about 1.54 TiB combined.
VM disks account for about 560.21 GiB within temporary data; screenshots and
logs are separate. This is allocation, not virtual disk capacity.

The revised selection contains all 263 completed QA disks (560.21 GiB) and
587 superseded firmware payloads (854.86 GiB): 1,415.07 GiB potential recovery.
No VM test is running or immediately queued; the earlier nine-disk hold is
superseded. Both hash passes completed without errors, covering all 850 exact
payloads. The prepared plan orders disk children before backing files and
retains 50,983 distinct independent compact records beside the retired payloads.
The full private selection and plan are bound by the hashes in
`review-selection.json` and `review-plan.json`. No historical payload has been
removed; only the regeneration benchmark's own new scratch files were deleted.

Five firmware files have an explicit temporary hold under #492: the known-booted
H700 DDR3/DDR4 image and update files, and the known-booted SM8550 image and update.
They serve the recovery steps of the immediately queued device adoption/smoke
tests. Release each device's hold when those tests and recovery needs finish.
Their hashes and identities are in the plan. Current candidate16 is the release
input; older immutable candidate-store bundles need separate retirement
classification that preserves source records and the store's verification
semantics. This is unfinished cleanup work, not a permanent retention exception.

The external reference scan completed without errors: 4,158,437 directories,
469 artifact manifests, 51 historical/source references classified, no external
symlinks into the reviewed stores and no current container mounts. Keep the
rclone source archive referenced by source custody; only its owner's QA disk
is selected. No selected payload is directly referenced by those manifests.

Four build trees (replacement09/10/12/14) add 432.57 GiB potential net recovery,
after charging the full 56.55 MiB independent preservation store. Its 14,489
content objects were independently verified. QA16 failed and QA17 passed; both
ended with verified guest/process cleanup. Their 14 source links to replacement12
are now classified as historical inputs with exact commit/path, preserved diff,
source inventories and terminal receipts. They do not keep the compiled tree
alive. Whole worktrees must still use `tools/fork-worktree remove`.

## Regeneration cost

One actual measurement on this host, using the qualified candidate16 firmware:
6.60 s to decompress into a sparse raw disk, 1.05 s to create a standalone
QCOW2, 0.32 s to resize to the supported 16 GiB, and 0.02 s for a disposable
copy-on-write overlay. A separate 0.73 s comparison verified guest contents
against the raw firmware; the size difference is the intentional zero extension.
All three newly created scratch files were removed and the watcher completed.

This measures disk creation, not booting, fixture setup or rerunning tests.
A guest can be recreated cheaply while its firmware is retained. Retiring the
only older firmware copy can require a source rebuild to revisit that version;
rebuilding or rerunning does not recreate the original experiment's state.
Keep logs, results, commands, environment, inputs, frames and diagnosis for that
historical record. Keep a large state artifact only for the specific immediate
test that requires it. Required source/licence inputs remain independent records.

## Prerequisites recorded before execution

Consume the requested administrator process readback, classify any matches and
complete fresh active-use checks before guarded deletion. The ordinary user
cannot read protected processes' cwd, descriptors and mappings; the exact
noninteractive sudo attempt also required authentication. This is a Linux
permission prerequisite, not a new request for cleanup authorization.

The prepared read-only helper is
`/workspace/tmp/pixelelated-m7-broad-root-readback-01/readonly-process-dependencies.py`;
it covers 1,079 exact directories. Its SHA256 is
`b0f5cf96836788bb71da9c418260e4e264157d907fd8bf38f4b3801ae7c44c39`.
Inspect the actual UID0, timestamp, exact roots, matches and unreadable fields
when its JSON arrives. The older four-tree readback request is superseded.

Ten redundant extracted OS copies passed their separate review, adding
124.21 GiB. The combined potential recovery is 2,117,252,173,824 bytes
(1,971.84 GiB), 53.78% of the filesystem's capacity. That review
checks raw/SYSTEM bytes against retained immutable firmware and inventories
extracted-tree entries; it does not claim to freshly compare every extracted
file's bytes. Its first run failed because older owners05/06/07 never had the
assumed owner console.log. The corrected run checks their actual required
scripts, terminal results and equality receipts and records console presence.
The failure is preserved separately; it deleted nothing.

Use a watched, exact-scope execution with current identities, kept inputs and
records verified before and after. Retire backing children first; use the
standard helper for whole worktrees. Record actual recovery and retirement
markers, then capacity-check H700 aarch64 and SM8550 in that order. The preparer
in this directory does not delete files or implement the final execution guard.
No automatic post-test cleanup is claimed: the owning work stream must finish it.
