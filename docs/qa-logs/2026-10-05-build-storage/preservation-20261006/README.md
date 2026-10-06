# Superseded-build preservation and removal proposal — #456, #458

No deletion or filesystem-reserve change is approved or executed. This report
prepares removal of replacement03/05/06/07/08 only. Run any eventual removal
from `/workspace/repos/rocknix.worktrees/conflict-resolution`, after the final
dependency readback and named approval. Product14 and its VM evidence remain
untouched.

## Completed preservation

Earlier `custody-followup-20261006/` records each branch, source commit,
generated tracked diff, immutable bundle and verified output hashes. The
five source heads remain unchanged. Independent cache-copy receipts record
distinct inodes; these old build roots are not the current build's hard links.

| Store under `/workspace/artifacts/pixelelated-build-custody/` | Retained content |
| --- | --- |
| `issue-456-es-logs-01` | All five complete ES source/build directories, `.threads`, `.stamps` and `.build-runs`; 3,585 unique objects, 1,633,877,538 content bytes. Modes, times, links and hashes in each tree manifest. |
| `issue-456-runtime-01` | Partial independent objects from the failed first runtime scan. Keep this store: accepted runtime02 independently reverified and references objects here. |
| `issue-456-runtime-02` | 91,496 executable ELF/library/module/debug or opaque malformed-fixture entries across five trees; 11,038 unique verified objects, 3,450,727,692 new content bytes plus verified reuse. |

Destination hashes were checked after copying; source device/inode/size/time
readbacks remained stable, and retained files have independent inodes. The
runtime scope excludes relocatable compiler intermediates and static archives.
It retains executable/library/kernel/module/debug outputs and complete ES
source/build data; it is not a byte-for-byte archive of every intermediate.

Each tree has a qualified source inventory:568source roots,547matching cached
inputs,0errors. The shared source cache **must remain**:
`/workspace/cache/rocknix-sources`. Also retain the recovered consumed archive:
`/workspace/artifacts/pixelelated-build-inputs/m7-cold-01-consumed/0d5570db7b689e96fb5e3d33293a5275e92d6df244acbcb8a1db1929bc3f491b/rclone-v1.75.1-linux-amd64.zip`,
SHA256`982b5aa772841168f8e380f139e9e787b2a105403e32b94da8676a0e1c0a13ab`.
`runtime-02/source-custody.json` names all qualified manifests and hashes.
This preserves cleanup inputs; it does not complete the P5 corresponding-source
and licence publication bundle or its14known metadata gaps.

## Malformed fixture failure and fix — #458

Runtime01 failed01:29:16UTC with four rc1channels. Its original logs and
completion remain here. Upstream's52byte
`pypackaging-26.3/tests/manylinux/hello-world-invalid-data` deliberately has
invalid ELF byte order. The old classifier asserted instead of preserving it.
SHA256`22e7fb680271534efb9f187ba7113e5f4ba93f4e9cda164891d88f1d958d02cf`.

Eight controls reproduce the old failure and check the corrected opaque
classification, valid ELF32/64 little/big endian, invalid class, truncated
and non-ELF headers. The copier retains malformed fixtures without executing
them. Runtime02 is a fresh sealed owner, completed01:36:51/allfour0;
actual cleanup01:37:39. It scanned12,707,750filenames and reverified all
destinations. Its completion helper's generic text says read-only inspection:
the exact operation was read-only on originals **plus independent copies into
new preservation stores**, as the retained source and summary show. Separately
owned QA18 guests were intentionally running then, not leaked by preservation.

## Dependency scope and remaining prerequisite

Expanded dependencies02 traversed4,221,564directories in `/workspace/tmp`,
`/workspace/artifacts`, `/workspace/repos/rocknix.worktrees` and
`/workspace/cache/rocknix-sources`, without pruning package/build directories.
It checked233qcow2-suffixed paths/backing chains, with0discovery errors,
0qemu errors,0backing references into proposed trees and0matching running
container mounts (ancestor and descendant matches checked). Five disks inside
proposed trees are identical131,072byte shared-mime-info test fixtures with
virtual size0 and no backing file. Exact fixture receipts are retained.

Directory symlinks are not followed; discovery is scoped to the four named
storage roots and `.qcow2` filenames. This is not a claim about arbitrary
unrelated host files. Full detailed path records remain local with their
hash published. Completed01:46:57/allfour0; actualcleanup01:48:00.

**Root-only live process references remain unverified.** The prior bounded
scan had537unreadable processes; classifying kernel threads or exited PIDs
does not establish absence of userspace references. Prepared read-only helper
SHA256`51a9b6c6026e94717505cc4376b1f5ce7b516261d7593b90b86d8955d9ad445e`
checks cwd/exe/root/arguments/fds/maps for exactly the five named trees.
Noninteractive sudo refused because interactive authentication is required;
this was not an automatic approval-review rejection. The maintainer has been
asked to run the helper and save its output. No answer/result yet.

Before removal, require that report's effective UID0, no unreadable fields and
no live references; refresh process/container checks immediately before each
operation. A new dependency excludes that tree until resolved. Reverify the
preservation hashes and current tracked diffs against the retained manifests.

## Concrete proposal, unexecuted

Run only after those checks and explicit named deletion approval:

```sh
tools/fork-worktree remove /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement03 --force
tools/fork-worktree remove /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement05 --force
tools/fork-worktree remove /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement06 --force
tools/fork-worktree remove /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement07 --force
tools/fork-worktree remove /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement08 --force
```

Execute separately, stop on failure, and verify both worktree registration
and directory removal after each. Do not add a wildcard or bypass this helper.
All retained branches, source objects, hashes and preservation stores remain.

Historical allocated gross579,103,657,984bytes (539.33GiB), less current
preservation allocation15,558,516,736bytes (14.49GiB), yields estimated net
563,545,141,248bytes (**524.84GiB**). This is a non-atomic estimate; actual
recovery must be measured after an approved removal. At01:48:00UTC available
space was39,878,275,072bytes (37.14GiB). No reserve change is proposed.

Protect replacement14, unbuilt13, retained12, qualified10, source09/cloud
evidence; every immutable bundle and original ROCKNIX RC2 image; all retained
QA disks/backing chains; shared source cache; all three preservation stores
and the recovered rclone archive. This report finishes the command/estimate
preparation; the dependency criterion and removal approval remain open.
