# Build-cache directory permissions during cleanup — #460

The first approved replacement03 removal passed retention and live-dependency
checks but failed after Git reached owner-owned mode0555 Go module/toolchain
directories under Syncthing's `.gopath/pkg/mod`. Git had already removed some
files and unregistered the tree. The original run remains failed with all four
result channels1; the sequence stopped before attempting the next tree.

`tools/fork-worktree remove --force` now inspects every directory before Git
removal. Once the scan completes, it adds owner write/search bits only to
nonempty directories that need them and belong to the invoking user. It
does not follow directory symlinks or change regular-file bytes or modes.
Unreadable or unrepairable directories and filesystem boundaries refuse
before Git removal. Directory file descriptors bind permission changes to
the inspected inode; a changed inode/mode refuses. A nonzero Git exit remains
nonzero even if the directory is absent.

The first version also refused replacement05's empty root-owned `sources`
directory, before changing permissions or invoking Git. That directory is
the mountpoint left after the build container exits. Empty directories are
removed through their parent's permissions, so the final guard skips that
unnecessary write-permission requirement. The preflight refusal remains a
separate failed run; replacement05 was still registered and intact.

`test-removal.py` uses isolated temporary Git repositories. `controls/` retains
the original five-case run; `controls-02/` verifies the final helper with six
cases, all passing:

1. The old helper reproduces actual partial deletion/unregistration.
2. The corrected helper removes read-only directories, retains the branch,
   and leaves an external symlink target's bytes and mode unchanged.
3. Omitting `--force` refuses build-output deletion without chmod.
4. An empty read-only directory is removed without chmod.
5. An unreadable subtree refuses before chmod, deletion or unregistration.
6. A controlled nonzero Git result propagates even after directory removal.

The actual host's empty root-owned mountpoints are covered by the approved
cleanup; the isolated empty-directory fixture is owned by the test user.
Tests do not require or obtain root access. The old helper source and exact
stdout/stderr/results are retained. Current source SHA256 is recorded by
the final controls, not inferred from a version label.

Can this be done on the VM? No: this is a host Git/worktree and filesystem
permission issue. The regression controls use disposable host fixtures.
Actual cleanup is separately authorized and evidenced under #459:
`../2026-10-05-build-storage/approved-cleanup-20261006/`.
No build product or frozen candidate bytes change with this host-tool fix.
