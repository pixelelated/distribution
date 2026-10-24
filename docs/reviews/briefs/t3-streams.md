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

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

| Item | Disposition |
| --- | --- |
| PL-001, PL-002 | `deferred:#802`: the packet exists, `fix/m6-802-pcsx-rearmed32` at `a0defbd527` (upstream `c9820d0e89` with `${DISTRONAME}`), reviewed, M7 has applied it; it reaches `next` with the integration, and the base merge takes `yabadabadoo-lr` the same way |
| PL-003 | `deferred:#806`: the recipe packet `fix/m6-806-grep-pcre2` at `ea0af11d07` (reviewed, applied by M7); the script's two `grep -oP` lines are `deferred:M7-merge` with `6101242e14` |
| PL-004 | class 1: upstream's `c4d353449e` with the base merge (the coordinator's ruling on #650; the maintainer told on #346) |
| PL-007 | routed to T5 (#652, its PL-06): the mechanism in `distributions/ROCKNIX/config/functions` |
| PL-008, PL-009, PL-021, PL-022 | `deferred:M7-merge`: `Install Steam.sh` is changed by the M7 hunk `6101242e14`; each gets its row on the follow-up the merge names (PL-022's Install-Steam lines included; its other sites, if any outside that file, go to S3) |
| PL-010 | class 1: upstream's `eeb33c5a37` with the base merge |
| PL-023 | routed to T5 (#652) as a lead: a shared rotation-table function belongs in `distributions/ROCKNIX/config/functions`; the five recipes call it after T5 lands (`deferred:#652`) |
| PL-025 | its own issue, **#839** (a bump is a re-cut and a build; after the M7 candidate) |
| PL-026 | the base merge (the coordinator's act; the eleven commits named in `q4a-dispositions.md`) |
| PL-029 | its own issue, **#838** (a fork tool; T9/T10's area) |

## S1. The recipes (PL-006, PL-012, PL-015, PL-017, PL-024, PL-005) -- `fix-pending-image`

- **Files owned:** `retroarch/package.mk` (PL-006 lines 106 to 114, PL-017 lines 94/96/98), `sameboy-lr/package.mk` (PL-012), `easyrpg-lr/wildmidi/package.mk` (PL-015), `flycast2021-lr/package.mk` (PL-024), `melonds-ds-lr/package.mk` and a new patch under `melonds-ds-lr/patches/` (PL-005). All under `projects/ROCKNIX/packages/emulators/libretro/`.
- **The test first:** `tools/pkgcheck <pkg>` on each before and after (PL-012's global-scope `PKG_BUILD` is what `pkgcheck` exists to catch: record whether it does, and if it does not, that is a lead on #657 for the tool); for PL-006 a shell fixture under `.qa-scratch/t3/s1/` that runs the recipe's install block with zero, one and two fake `install_pkg/retroarch-*` directories and asserts: zero or two **die** with a message naming the count, one copies; before the fix zero and two pass silently. For PL-017, `bash -n` and a reading that the three `make` lines now fail the build on error (`|| die`, or the dead arms removed with the reason in a comment). For PL-015, the full hash resolves (`git ls-remote <url> | grep <full>`). For PL-005, each of the eleven short hashes or tags resolved to a full commit with `git ls-remote` (the command and its line per dependency in the patch header).
- **The change:** PL-006 fail closed on any count but one and on a stale directory (`newer than the stamp`, or the file's own hash against the arm root's); PL-012 move the reference into a function or drop the option the build never reads (say which, from the core's Makefile); PL-015 the full hash; PL-024 the assignment to global scope; PL-017 the three checks made real or removed; PL-005 a patch to `cmake/FetchDependencies.cmake` pinning the eleven to full hashes (the fetch still happens at configure: the vendoring is the follow-up on its `bug`, named in the recipe comment with `device-builds.md` § A build that fetches its own dependency).
- **Already written:** nothing on a device: recipes write images. The next image is the proof (`fix-pending-image` for every item; the shell fixture is the host proof for PL-006).
- **Commit** per recipe, `<package>: <text>`, each `Refs` its bug and #826.

## S2. The launch table (PL-011, PL-030, PL-031, PL-019) -- `fix-host-regen`

- **Files owned:** `projects/ROCKNIX/packages/virtual/emulators/package.mk` (the device arms and the comment at 107 to 115), `projects/ROCKNIX/packages/virtual/emulators/sources/Scan id Tech Games.sh`'s install condition (not its content). **Not** the one-default mechanism (T5's PL-06) and not `add_es_system` (T5's PL-05).
- **The test first:** `tools/regen-es-systems.sh` for GENERIC_X64, H700 and SM8550 before the change (byte-identical to the three images, as stage B proved) and after: the diff is exactly the intended lines (`st-v` gone from the four device arms where no emulator builds it, or the emulator added where one exists for that device -- say which from the recipes; GENERIC_X64's `psx` with a default; the six skipped cores and the `ffmpeg` core no longer offered where no image installs them; the id Tech scanner installed only beside its binary). Then every core each regenerated table names exists in that device's install tree (`image/system/usr/lib/libretro`, read-only from the M7 roots): zero missing, the command and count per device recorded -- which is #838's check done by hand once.
- **Already written:** a device's own `es_systems.cfg` is the image's and is replaced whole; a player's per-game emulator choice (`gamelist.xml`'s `<emulator>`/`<core>`, in `/storage`) that named a removed offer falls back to the system's default at launch -- read `runemu.sh`'s fallback and name it in the row. Least surprise (D-UI-042): removing a choice that never worked surprises nobody; adding a default where none was makes a launch that failed work.
- **Commit:** `emulators: <text>` per item or one for the table, `Refs` the bugs and #826.

## S3. The scripts (PL-013; PL-022's sites outside Install Steam.sh, if any) -- `fix-pending-image`

- **Files owned:** `virtual/emulators/sources/Start Azahar.sh`, `Start MelonDS.sh` (the shebang to line 1; what was on line 1 goes to line 2 or is removed if it was blank or a stray header); any PL-022 site not in `Install Steam.sh`.
- **The test first:** `head -1` prints the shebang; `bash -n` rc 0; the image's `/bin/sh` is bash (the T1 erratum) so the interpreter line matters only when a launcher execs the script directly: read `runemu.sh`'s call and say whether line 2 ever bit.
- **Already written:** nothing. **Commit:** `emulators: <text>`.

## S4. The patches (PL-014, PL-018) -- `fix-pending-image`

- **Files owned:** `retroarch/patches/0004-drm-resolution.patch`, `retroarch/patches/0017-widgets-sharp-font-sizes.patch`.
- **The test first:** PL-014: `patch --dry-run` of 0004 against the pinned source read from the M7 GENERIC_X64 root applies with fuzz before and cleanly after the re-cut (the hunk re-based on the pin; no content change -- the diff of the two patches' `+` lines is empty). PL-018 is a **decision, not an edit**: the stream writes on #650 which shipped profile would engage 0017's size step and what the register says about the sharp-font work (`tools/font-stems`, the D-UI rows that chose the sizes); the default is **keep the patch and say in its header why it is dormant**; dropping it needs a register row from the coordinator. No edit to 0017 in this stream unless the header note.
- **Already written:** nothing. **Commit:** `retroarch: <text>`.

## S5. The configs (PL-016, PL-028, PL-033) -- `fix-pending-image`

- **Files owned:** `retroarch/sources/*/retroarch.cfg` (fifteen), `retroarch/udev.d/99-ninteno-wii-remote.rules` (deleted).
- **The test first:** PL-016: the list of keys the pinned RetroArch reads (`configuration.c`'s `SETTING_*` tables in the pinned source, read from the M7 root) against each profile's keys; the 24 or 25 unread keys named per file before, zero after; the `core_updater_buildbot_cores_url` line names the aarch64/x86_64 URL for its device after. PL-028: whether the recipe's install resolves symlinks (`retroarch/package.mk`'s install line: `cp -a` keeps a symlink, `install`/`cp -L` resolves) -- if it resolves, the four copies become symlinks to the one they copy and the regenerated install tree is byte-identical; if not, the four stay and the finding is recorded as *kept: the recipe copies files* with a one-line README in `sources/`. PL-033: `git ls-files retroarch/udev.d` lists one Wii remote rule, and the recipe installs the directory (not the misspelt name) -- read it.
- **Already written:** a device keeps its own `/storage/.config/retroarch/retroarch.cfg`; the shipped profile is the default for a fresh install and for keys a device's file lacks. Removing an unread key changes no behaviour anywhere (the pinned binary never read it); say so per key class in the row.
- **Commit:** `retroarch: <text>` per item.

## S6. Currency rows (PL-027, PL-020) -- `tree` and `tool-run`

- **Files owned:** the six recipes whose pins are off their project's default branch (a comment line `# pinned to <ref> because <reason>`, D-WORKFLOW-024, or the row says *bump proposed on #839's shape, its own issue*); the four recipes naming a moved, renamed or archived repository (`PKG_SITE`/`PKG_URL` to the current location with the same hash: `git ls-remote <new url>` lists the pinned hash, the line pasted); `tools/retroarch-wrapper-test` (PL-020: `--gated` asserts the gate's effect, seen to FAIL on a wrapper copy with the gate removed and PASS on the tree's).
- **Already written:** nothing. **Commit:** per recipe `<package>: <text>`; the tool `retroarch-wrapper-test: <text>`, `Refs #799` beside its bug.

## Order and hand-back

S0 (running), then S1, S2, S3, S4, S5, S6, each handed back with one comment on #650 (the stream, its commits, the test lines, the `punch_index` rows moved with their `proved:` class) and the lane going straight on. At the end: the Phase 7 table complete (every item resolved with its commit, deferred to a named issue, or withdrawn with its reason), `tools/lint-audit-artifacts` on the folder, `fixed-at` written into #650, the retro (stage G), the hand-back comment (stage H). The coordinator reviews each stream as it lands and accepts at hand-back per the brief § 10.
