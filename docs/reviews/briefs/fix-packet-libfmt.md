# Fix packet: libfmt's empty PKG_SHA256 (#877), ahead of T5's merge

Written by the coordinator on 2026-10-24 at T7's stage B (D-WORKFLOW-189),
in the shape of `fix-packets-802-806.md`: one narrow stream, the files
owned, the test first, the `Already written:` line, one commit cut after the
checks are green. **Nothing here builds.** The packet is a branch on
`origin` that merges to `next` **before `feature/m6-build-engine-652`**
in the integration order, because T5's E6 (`scripts/get_archive` at
`52e6794ba7:7`, D-WORKFLOW-193) refuses an empty `PKG_SHA256` and
`projects/ROCKNIX/packages/devel/libfmt/package.mk:11` sets one for every
device but the six SM/AMD64 names (D-WORKFLOW-196). The M7 candidate does
not carry E6, so M7 needs nothing. **Review depth: Local** (plan § 6c: a
recipe of one line): the executor, `tools/pkgcheck`, and the coordinator
reading the diff on #877. No guest, no compiler, no `npm`, no process in an
M7 worktree.

## The stream (#877)

- **Branch and worktree:** cut **from `next` at `8ebaf8daad`**, in its own
  worktree beside the lane's, never in a slice worktree:
  `git -C /workspace/repos/pixelelated/distribution worktree add ../distribution.worktrees/m6-877-libfmt-sha256 -b fix/m6-877-libfmt-sha256 8ebaf8daad`.
  The coordinator removes the worktree with `tools/fork-worktree remove`
  after the merge.
- **Files owned:** `projects/ROCKNIX/packages/devel/libfmt/package.mk`, line
  11 and one comment line above it. Nothing else.
- **The test first**, in the new worktree, every output pasted on #877:
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-877-libfmt-sha256; cd "$D"
  git grep -n 'PKG_SHA256=""' HEAD -- packages projects                      # the one line, before
  mkdir -p .qa-scratch/libfmt && curl -sSL --max-time 300 -o .qa-scratch/libfmt/libfmt-9.1.0.tar.gz https://github.com/fmtlib/fmt/archive/9.1.0.tar.gz && sha256sum .qa-scratch/libfmt/libfmt-9.1.0.tar.gz   # witness 1: the fetch
  cat /workspace/cache/rocknix-sources/libfmt/libfmt-9.1.0.tar.gz.sha256      # witness 2: the cache's stamp (5dea48d1...), read only
  curl -sSL --max-time 300 https://github.com/ROCKNIX/distribution-sources/releases/download/sources-v2/libfmt-9.1.0.tar.gz | sha256sum   # witness 3: the mirror, streamed
  ```
  The value written is the fetch's. If the three agree, the comment says so;
  if the fetch differs from the cache (a regenerated tag archive), the
  comment names both and the packet says so on #877 before the commit -- that
  is a hold, not a choice to make alone.
- **The change:** `PKG_SHA256="<the fetch's sha256>"` in the `*)` branch, with
  one comment line above it: `# 9.1.0's archive, sha256 by trust on first use
  from the fetch of 2026-10-24, equal to the shared cache's 2026-08-26 stamp
  and ROCKNIX's mirror (D-WORKFLOW-193/196, #877)` -- adjusted to what the
  three witnesses said. Nothing else in the file moves.
- **The test after:** `git grep -n 'PKG_SHA256=""' -- packages projects` prints
  nothing; `PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 tools/pkgcheck libfmt`
  exits 0; `PROJECT=ROCKNIX DEVICE=H700 ARCH=aarch64 tools/pkgcheck libfmt`
  exits 0; `PROJECT=ROCKNIX DEVICE=SM8550 ARCH=aarch64 bash -c '. config/options libfmt >/dev/null; echo $PKG_VERSION $PKG_SHA256'`
  still prints 12.2.0 with the generic checksum (the SM branch untouched).
  `config/options` creates a gitignored `build.*/.cache_package_*` in the
  worktree; leave it, the worktree is removed after the merge.
- **Already written:** nothing on devices; a build-time checksum. The cache
  keeps its stamp; the recipe now names it.
- **Commit**, one, cut after the tests are green, by `git add -- projects/ROCKNIX/packages/devel/libfmt/package.mk`:
  `libfmt: give the 9.1.0 override its PKG_SHA256 (#877)`, body: the three
  witnesses' values, `Refs #877, #654, #652, #834` (no closing keyword: the
  last criterion closes on a build), the attribution line. `git status --short`
  empty after. Push `fix/m6-877-libfmt-sha256` to origin and post the tip,
  the diff and the four outputs on #877; then the session is idle.
- **Ceremonies:** a work-log entry headed `#877` (the time from `date -u` in
  the same command) is the coordinator's for a packet, as for #802 and #806;
  the lane posts on #877 only.

## After the packet

The coordinator reads the diff on #877, ticks the first two criteria from the
pasted outputs, names the branch in the pointer's merge notes **before T5's**,
and writes D-WORKFLOW-196 (an empty assignment is a missing checksum) with
this brief's commit. The third criterion closes on the first GENERIC_X64 build
after the integration.
