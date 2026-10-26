# Fix packet: simple-http-server's per-arch checksums (#890), ahead of T5's merge

Written by the coordinator on 2026-10-24 at T8's stage B (D-WORKFLOW-189),
in the shape of `fix-packets-802-806.md`: one narrow stream, the files
owned, the test first, the `Already written:` line, one commit cut after the
checks are green. **Nothing here builds.** The packet is a branch on
`origin` that merges to `next` **before `feature/m6-build-engine-652`**
in the integration order, because T5's E6 (`scripts/get_archive` at
`52e6794ba7:7`, D-WORKFLOW-193) refuses an empty `PKG_SHA256` and
`projects/ROCKNIX/packages/network/simple-http-server/package.mk:12-23` sets
one only in its `aarch64` branch (D-WORKFLOW-197), so every GENERIC_X64 build
would stop at it. The M7 candidate does
not carry E6, so M7 needs nothing. **Review depth: Local** (plan § 6c: two
recipe lines): the executor, `tools/pkgcheck`, and the coordinator
reading the diff on #890. No guest, no compiler, no `npm`, no process in an
M7 worktree.

## The stream (#890)

- **Branch and worktree:** cut **from `next` at `8ebaf8daad`**, in its own
  worktree beside the lane's, never in a slice worktree:
  `git -C /workspace/repos/pixelelated/distribution worktree add ../distribution.worktrees/m6-890-shs-sha256 -b fix/m6-890-shs-sha256 8ebaf8daad`.
  The coordinator removes the worktree with `tools/fork-worktree remove`
  after the merge.
- **Files owned:** `projects/ROCKNIX/packages/network/simple-http-server/package.mk`,
  the `x86_64` and `arm` branches of its `case ${ARCH}` (lines 13-18): one
  `PKG_SHA256` line and one comment line in each. Nothing else; the
  `aarch64` branch keeps `88a523d3…`.
- **The test first**, in the new worktree, every output pasted on #890:
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-890-shs-sha256; cd "$D"
  for a in x86_64:GENERIC_X64 arm:H700 aarch64:H700; do PROJECT=ROCKNIX DEVICE=${a#*:} ARCH=${a%:*} bash -c '. config/options simple-http-server >/dev/null 2>&1; printf "%s sha=[%s] url=%s\n" "$1" "$PKG_SHA256" "$PKG_URL"' _ "${a%:*}"; done   # before: x86_64 and arm empty
  mkdir -p .qa-scratch/shs && for a in x86_64 arm; do url=$(PROJECT=ROCKNIX DEVICE=$([ $a = x86_64 ] && echo GENERIC_X64 || echo H700) ARCH=$a bash -c '. config/options simple-http-server >/dev/null 2>&1; printf "%s" "$PKG_URL"'); curl -sSL --max-time 300 -o ".qa-scratch/shs/$a" "$url" && sha256sum ".qa-scratch/shs/$a"; done   # witness 1: the fetch, per arch
  cat /workspace/cache/rocknix-sources/simple-http-server/*x86_64*.sha256 2>/dev/null   # witness 2: the cache's stamp for x86_64 (a16d73db...), read only; arm has none on this host: say so
  ```
  The `x86_64` value written is the fetch's, which must equal the cache's
  stamp (`a16d73db4b33edc6aada0bb54088773dba8cb4d02eaa13364559552072d628cd`);
  the `arm` value is the fetch's alone, and its comment says *one witness*.
  If the `x86_64` fetch differs from the stamp, post both on #890 and stop:
  that is a hold.
- **The change:** in the `x86_64` branch, after its `PKG_URL` line,
  `PKG_SHA256="<fetch>"` with the comment `# the release binary's sha256 by
  trust on first use from the fetch of 2026-10-24, equal to the shared
  cache's 2026-08-26 stamp; the mirror has no copy (D-WORKFLOW-193/197,
  #890)`; in the `arm` branch the same with `one witness: the fetch`.
  Nothing else in the file moves.
- **The test after:** the three expansions print a 64-hex value for every
  arch; `PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 tools/pkgcheck
  simple-http-server` exits 0, and so with `DEVICE=H700 ARCH=arm` and
  `DEVICE=H700 ARCH=aarch64`; `git grep -c 'PKG_SHA256' -- <the recipe>`
  prints 3. `config/options` creates a gitignored `build.*/.cache_package_*`
  in the worktree; leave it, the worktree is removed after the merge.
- **Already written:** nothing on devices; a build-time checksum. The cache
  keeps its stamp; the recipe now names it.
- **Commit**, one, cut after the tests are green, by `git add -- projects/ROCKNIX/packages/network/simple-http-server/package.mk`:
  `simple-http-server: give the x86_64 and arm branches their PKG_SHA256 (#890)`,
  body: the witnesses' values per arch, `Refs #890, #655, #877, #652, #834`
  (no closing keyword: the last criterion closes on a build), the attribution
  line. `git status --short` empty after. Push `fix/m6-890-shs-sha256` to
  origin and post the tip, the diff and the outputs on #890; then the session
  is idle.
- **Ceremonies:** the work-log entry headed `#890` is the coordinator's, as
  for #877; the lane posts on #890 only.

## After the packet

The coordinator reads the diff on #890, ticks the first two criteria from the
pasted outputs, names the branch in the pointer's merge notes **before T5's**,
and writes D-WORKFLOW-196 (an empty assignment is a missing checksum) with
this brief's commit. The third criterion closes on the first GENERIC_X64 build
after the integration.
