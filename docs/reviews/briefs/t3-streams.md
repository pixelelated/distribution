# T3's remediation streams (#650, audit issue #826)

Written by the coordinator at T3's stage-D pause (2026-10-24, D-WORKFLOW-189),
one stream per group of related items, each in the D-WORKFLOW-056 shape: the
files owned, the test first, the `Already written:` line, commits cut from
intermediates only after the checks are green. Streams are numbered in the
order they run; **S0 runs first and alone**, because it is a security defect
that every ROCKNIX image carries today. The lane's brief
(`docs/reviews/briefs/emulators-libretro.md`) § 5 and § 6 still govern what
runs where (`image-set`, `fix-host-regen`, `fix-guest-copy`,
`fix-pending-image`), and nothing here builds an image.

Common to every stream: the stream's commits land on the slice branch
`feature/m6-emulators-libretro-650`; a stream whose fix the M7 lane should be
able to take before the integration is cut on a `fix/*` branch from `next`
first and then merged `--no-ff` into the slice branch, so one commit serves
both (S0 is one). Every commit cites the punch item and its `bug` issue with
`Refs` (no closing keyword: the criteria close on an image or a guest); the
hook script and the patches keep their upstream headers; `tools/pkgcheck`
runs on every recipe touched; `git status --short` is empty after each
commit; the running log gets a `PROOF:` line per proof; the punch list's
Phase 7 table and `punch_index` are updated at the end of each stream, never
mid-way. A stream that cannot meet its test says so on #650 and stops; the
coordinator re-cuts the stream.

## S0. The achievements hook runs without a shell (PL-032, #825) -- security, first

- **Why first:** `0012-cheevos-cmd.patch` builds `<cmd> <id> "<title>" "<description>" > /dev/null 2>/dev/null`
  with `snprintf` and hands it to `system()`, on every unlock, as root,
  wherever RetroAchievements is on (`setsettings.sh:485` sets `cheevos_cmd`
  for the platform). The title and description are the achievement set's
  text -- RetroAchievements' server data or the offline proxy's copy -- and a
  `$( )`, a backtick or a `"` in either is executed. **Upstream ROCKNIX carries
  the identical patch** (`upstream/next`'s `0012-cheevos-cmd.patch` has the
  same `system(cmdargs)` line), so this is a contribution candidate on #585
  under D-WORKFLOW-164, held by D-WORKFLOW-165 and flagged to the maintainer
  for an earlier disclosure if they want one. The M7 lane's candidate images
  carry it; the packet below is cut so M7 can take it.
- **Files owned:** `projects/ROCKNIX/packages/emulators/libretro/retroarch/patches/0012-cheevos-cmd.patch`
  (the `cheevos/cheevos.c` hunk only; the `configuration.c` and
  `configuration.h` hunks stay) and
  `projects/ROCKNIX/packages/emulators/libretro/retroarch/scripts/call_achievements_hooks.sh`.
  Nothing else: not `setsettings.sh` (T1's, accepted), not the LED scripts
  under the quirks (T29's).
- **The branch:** `fix/m6-825-cheevos-hook-no-shell`, cut from `next` at
  `8ebaf8daad` in its own worktree `../m6-825-cheevos-hook-no-shell`, one
  commit; pushed; then `git merge --no-ff` of that commit into the slice
  branch in the slice worktree, so `fixed-at` carries it. The coordinator
  tells M7 the branch and hash.
- **The test first:**
  1. `grep -c 'system(cmdargs)' <the patch>` prints `1` before and `0` after;
     `grep -c 'execv' <the patch>` prints `0` before and `1` or more after;
     `grep -cE '\$\*' <the hook>` prints `2` before and `0` after, and
     `grep -c '"\$@"' <the hook>` prints `2` after.
  2. **The patch applies to the pin.** Take `cheevos/cheevos.c` from the M7
     GENERIC_X64 build root's RetroArch source (read only:
     `/workspace/repos/rocknix.worktrees/generic-x64/build.ROCKNIX-GENERIC_X64.x86_64/build/retroarch-<pin>/cheevos/cheevos.c`,
     copied to `.qa-scratch/t3/s0/`; that copy already carries 0012's hunk,
     so `patch -R` the old hunk first), then `patch --dry-run` the new hunk
     onto it: applies cleanly, no fuzz, no offset beyond the hunk's own.
     Record the pin and the path.
  3. **The compiler has seen it, if the command can be had.** The build
     root's RetroArch was built by make; if its `config.log` or a
     `compile_commands`-shaped record gives the exact command for
     `cheevos/cheevos.o`, replay it on the patched copy with
     `-fsyntax-only` from the toolchain in that root (reading the root,
     writing only under `.qa-scratch/`); if it cannot be reconstructed in
     twenty minutes, record *not runnable here* with what was tried, and
     the image proves it. A compile check that could not run is not a pass.
  4. **The hook's half on the guest now** (`fix-guest-copy`, the brief § 5's
     recipe; the host is M6's since 05:42 -- census first, the pidfile,
     stop the guest after): copy the fixed hook to
     `/usr/share/libretro/call_achievements_hooks.sh`'s place (the image's
     copy is read-only under the squashfs: bind-mount the fixed file over
     it, or run the fixed script from `/storage` directly), put a stub
     `achievements` at
     `/usr/lib/autostart/quirks/platforms/${HW_DEVICE}/bin/achievements`'s
     place the same way that writes `$#` and `$2` to `/tmp/t3-s0-args`, set
     `global.retroachievements.leds` to `1` for the run and back after, and
     call the hook with id `1`, title `a b $(touch /tmp/t3-s0-marker)` and
     description `c d`: the file records `3` and the whole title, and
     `/tmp/t3-s0-marker` is absent (#825 criterion 2, the synthetic input
     named in the tick). Before the fix the same call records `6` or more
     and a split title.
  5. **RetroArch's half is `fix-pending-image`**: #825 criterion 1 (the
     loopback provider of `tools/ra-ui-test` awards an achievement titled
     `$(touch /tmp/t3-hook)`; the marker is absent) runs on the first image
     built with the patch, by the coordinator's image proof; the row says so.
- **The change, in C** (the hunk in `rcheevos_award_achievement`, replacing
  the `snprintf`/`system` pair; keep the `cheevos_cmd[0]` guard):
  - build the id as a string (`char idbuf[16]; snprintf(idbuf, sizeof idbuf, "%u", cheevo->id);`);
  - `fork()`; in the child: open `/dev/null` and `dup2` it onto 1 and 2
    (what the old redirection did), then
    `execv(cheevos_cmd, (char *const[]){ (char*)cheevos_cmd, idbuf, (char*)(cheevo->title ? cheevo->title : ""), (char*)(cheevo->description ? cheevo->description : ""), NULL })`,
    and `_exit(127)` if it returns; in the parent, `waitpid` as `system()`
    waited (the hook backgrounds the LED script itself, so it returns at
    once); on `fork()` failure do nothing. Add the includes the file lacks
    (`<unistd.h>`, `<sys/wait.h>`, `<fcntl.h>`), guarded as the file's
    other POSIX includes are if it builds on non-POSIX targets (check
    `cheevos.c`'s existing `#ifdef`s; this patch is ours and builds on
    Linux only, so an `#if defined(__linux__)` around the block is
    acceptable if the file's style asks for it). No shell, no quoting: the
    title is one `argv` element however it is spelled.
  - **The hook:** `$*` becomes `"$@"` on both lines (the LED script receives
    three arguments: id, title, description).
- **Already written:** nothing stored. A crafted title would have run once
  per unlock; there is no state to migrate, and a device updated to an
  image with the fix needs nothing done (#825).
- **Commit:** `retroarch: run the achievements hook without a shell (patch 0012, #825)`,
  body with the mechanism in two sentences, the test lines, `Refs #825,
  #650, #826, #585`; `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`;
  `tools/pkgcheck retroarch` rc 0 (the recipe is untouched; the check is
  cheap).
- **Hand-back:** one comment on #825 and a one-line pointer to it on #650:
  the branch and hash, `git show --stat`, the five test results in order
  (with *not runnable here* where that is the truth), the guest's census
  and stop, and the `punch_index` entry for PL-032 moved to
  `fix-pending-image` with #825 as `tracked`. Then the lane proceeds to S1
  without waiting (the coordinator reviews S0 in parallel).
