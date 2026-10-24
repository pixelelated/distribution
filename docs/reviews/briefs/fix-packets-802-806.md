# Fix packets for the M7 candidate: #802 and #806

Two narrow remediation streams, written by the coordinator on 2026-10-24
(D-WORKFLOW-189) at the M7 lane's request, relayed through the maintainer's
channel at about 04:30 UTC: *"#802 and #806 are now in our next-candidate
list; please retain your existing source ownership and tell me if a narrow
reviewed fix packet is ready for M7 consumption before our next images. No
additional runtime requested from M6."* Each stream is the D-WORKFLOW-056
shape: the files owned, the test first, the `Already written:` line, one
commit cut after the checks are green. **Neither builds anything**: the
packet is a branch on `origin` that M7 fetches and applies to its candidate
tree; the proof is M7's image, read against the issue's acceptance criteria.
**Review depth: Local** (plan § 6c, a recipe of three lines): the executor,
`tools/pkgcheck`, and the coordinator reading the diff on the issue before
telling M7 the packet is ready. Nothing here runs a guest, a compiler or
`npm`; the host hold is M7's and stays so.

Common to both streams:

- The branch is cut **from `next` at `8ebaf8daad`**, in its own worktree
  beside the lane's (`worktrees.md`: one worktree per branch, the directory
  named after the branch leaf), never in the lane's slice worktree and never
  on the slice branch: `git worktree add ../<leaf> -b fix/<leaf> next`.
  The coordinator removes the worktree with `tools/fork-worktree remove`
  once M7 has consumed the packet and the branch has merged.
- Commit message in the fork's style, `<package>: <text>`, body naming the
  issue with `Refs #N` (no closing keyword: the criteria close on M7's
  image), ending `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`;
  committed as `git -c user.name=blitterbot`.
- `tools/pkgcheck <package>` run from the fix worktree and its output
  pasted; `git status --short` empty after the commit; `git push -u origin
  fix/<leaf>`.
- The hand-back is **one comment on the issue**: the branch, the commit
  hash, `git show --stat`, the pkgcheck line, `git apply --check` of
  `git format-patch -1 --stdout <hash>` against `8ebaf8daad` (trivially
  clean; M7 repeats it against its own tree), the criterion lines M7's
  image must show, and what the stream could not prove (no build here).
  Then the lane's pointer is updated and the lane says what state it is in.
- The coordinator reads the diff on the issue, comments *reviewed*, and
  tells M7 on the host file and the maintainer's channel that the packet is
  ready, with the branch and hash. M7's `git apply --check` against its
  candidate tree, the build and the install-tree readback are M7's; a
  failure there comes back to the issue, not to the lane's chat.

## Stream 802: `pcsx_rearmed-lr` installs the 32-bit core where `runemu` loads it

**Lane:** T3 (`m6-t3-emulators`, #650) -- the finding is its F-08/F-09 and
the recipe is its slice's. **Before anything: update the lane's pointer and
push**, because the session's context is nearly spent and a compaction
mid-stream must find the state on disk.

- **Files owned:** `projects/ROCKNIX/packages/emulators/libretro/pcsx_rearmed-lr/package.mk`
  only. `yabadabadoo-lr` is not on `next` and is **not** in this packet (it
  arrives with the base merge, #802's note).
- **The test first:** on `next`, `grep -c 'pcsx_rearmed32_libretro.so ${INSTALL}/usr/lib/libretro' projects/ROCKNIX/packages/emulators/libretro/pcsx_rearmed-lr/package.mk`
  prints `0` (the 32-bit core is installed only into the arm build root's
  `usr/lib/libretro/`, which the aarch64 image's `runemu` never reads); after
  the fix it prints `1`, and `git grep -F 'build.${DISTRO}-' -- projects
  packages` prints nothing (the fork's roots are `build.${DISTRONAME}-`
  since `43d0bc3bf4`; `box86`'s recipe at `projects/ROCKNIX/packages/compat/box86/package.mk:72`
  is the model).
- **The change:** `git cherry-pick -x c9820d0e89` (upstream's *"pcsx_rearmed-lr:
  install the 32-bit core where runemu loads it"*, 2026-10-04; `git apply
  --check` of its patch against `next` is clean), then the one-word
  adaptation `${DISTRO}` to `${DISTRONAME}` in the added `cp -a` line,
  folded into the same commit (`git commit --amend`), the message saying
  the cherry-pick's origin and the adaptation. Nothing else in the file
  moves.
- **Already written:** nothing inherited that this changes -- the squashfs
  is replaced whole on update; PlayStation saves and states written through
  the 64-bit core or an earlier image's 32-bit core are untouched (#802).
- **What M7's image must show** (#802 criterion 1): on the first H700 and
  SM8550 images built with the packet, `image/system/usr/lib/libretro/pcsx_rearmed32_libretro.so`
  exists in both install trees, and the build log shows the `cp -a` ran
  in `pcsx_rearmed-lr`'s install for the aarch64 build (the arm root's file
  must exist first: `ENABLE_32BIT=true` on both devices, as it is today).
- **Commit subject:** `pcsx_rearmed-lr: install the 32-bit core where runemu loads it (upstream c9820d0e89, DISTRONAME)`.

## Stream 806: `grep` declares PCRE2 and fails closed without it

**Lane:** T1's (`m6-t1-os-launch`, #648, accepted and idle) -- the recipe is
T22's slice under the same area epic #695, and no lane holds T22; T1's
session knows the OS-scripts area and its rules.

- **Files owned:** `projects/ROCKNIX/packages/sysutils/grep/package.mk`
  only (the fork's override, byte-identical to upstream's today; the
  generic `packages/sysutils/grep/package.mk` is not touched). `Install
  Steam.sh`'s two `grep -oP` lines are the script layer, `deferred:M7-merge`
  with the M7 hunk `6101242e14`, and are **not** in this packet.
- **The test first:** on `next`, `grep -c 'pcre2\|perl-regexp' projects/ROCKNIX/packages/sysutils/grep/package.mk`
  prints `0`; after the fix it prints `2` or more, and
  `grep -n '^PKG_DEPENDS_TARGET=' projects/ROCKNIX/packages/sysutils/grep/package.mk`
  shows `pcre2` in the list.
- **The change:** `PKG_DEPENDS_TARGET="toolchain pcre2"` and a new
  `PKG_CONFIGURE_OPTS_TARGET="--enable-perl-regexp"` (grep 3.9's configure
  has the switch; the fallback binary's own message, *"Perl matching not
  supported in a --disable-perl-regexp build"*, is what the SM8550 image's
  `usr/bin/grep` carries today). Check `packages/devel/pcre2/package.mk`
  (10.47) builds for the target as a plain dependency (`PKG_DEPENDS_TARGET`
  and no host-only marker), and say in the comment what the image gains
  (`libpcre2-8.so`, its size from the recipe's install or from another
  build root's `image/system/usr/lib/` -- read, never built). Keep the
  host side as it is (`PKG_CONFIGURE_OPTS_HOST` unchanged).
- **Already written:** nothing inherited that the recipe fix changes; a
  Steam install that stopped at the Proton step left the client and runtime
  installed and no Proton, and completes on the next run with a PCRE grep
  (#806).
- **What M7's image must show** (#806 criterion 2): on the first SM8550 and
  H700 images built with the packet, `strings image/system/usr/bin/grep |
  grep -c pcre2` is non-zero and `| grep -c 'disable-perl-regexp build'` is
  zero, in both install trees.
- **Commit subject:** `grep: declare pcre2 and enable perl regexps so a build without PCRE fails closed`.
- **The sweep is not this stream's:** the list of every `grep -P` on the
  image (`git grep -n -E 'grep +-[a-zA-Z]*P' -- projects packages`) is
  T22's row on #669; mention the command in the comment and leave the list.
