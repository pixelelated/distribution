# T8's remediation streams (#655, audit issue #895)

Written by the coordinator at T8's stage-D pause (2026-10-24, 13:04 UTC post
at `c5a8c5c4a8`; D-WORKFLOW-189). Seventeen items (PL-18 and PL-19 added during stage E), four streams: the slice's
own first stream (#852, named in the brief's § 7) and the two Medium bugs the
second opinion found whose fix is contained (#893, #894). Everything else is a
disposition below. Plan § 6b E binds every stream: **a commit names its
paths**; **a time is produced, never typed**; **prose goes into a running
log through a quoted heredoc or the Write tool, never an unquoted one**.
Brief § 2's scope rule holds: no pin moves, no checksum changes except the
three S2 adds, nothing upstream-carried is deleted or renamed, and the only
files changed under `projects/` are the ones each stream names.

The lane's question of 13:04 (which of #893 and #894 are streams beside
#852): **both**. Each is Medium; each fix is contained
(`bugs-are-agent-first.md` rule 6: a defect in upstream's code is ours to
close when the fix is a guard or a line, not a redesign); each has a proof
the brief's bench gives -- the host for #893, the GENERIC_X64 guest for
#894 -- and neither moves a pin. Order S1, S2, S3: the guest cycle last,
since it needs the host, which M6 holds (census 0 at 13:20 UTC).

## S1. `virtual/image`'s Entware link moves into the install step (PL-02, #852; G-16 folded) -- `fix-tree`, then `fix-pending-image`

- **Why a stream:** the brief named it (§ 7); two lines in a recipe the
  fork carries from ROCKNIX; the load-time write is proved gone on the host
  with no compiler.
- **Files owned:** `projects/ROCKNIX/packages/virtual/image/package.mk`
  (`:109-110` at `8ebaf8daad`) and nothing else. `PKG_DEPENDS_TARGET+="
  entware"` stays at global scope.
- **The shape:** a `post_install()` hook. `scripts/install` runs
  `pre_install` and `post_install` (`:161`, `:189`) with `INSTALL` the image
  root, `$BUILD/image/system`, when nothing else has set it
  (`config/path:39-40`); the virtual package has no build step, so the hook
  is where the link is made once, by the install of `image`. Use `ln -sfn
  /storage/.opt ${INSTALL}/opt` (G-16: `ln -sf` onto an existing `opt`
  directory links *inside* it; `-n` treats an existing link as the file it
  is), with `mkdir -p ${INSTALL}` beside it inside the hook. Read
  `scripts/install:150-192` once before writing, so the hook named is the
  one that runs for a `virtual`-section package.
- **The test first**, each output pasted on #852 and in `02`: on a fresh
  export of the tree at `8ebaf8daad` (`git archive 8ebaf8daad | tar -x -C
  <dir>`), `PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64 bash -c '.
  config/options image >/dev/null 2>&1'` then `find . -path
  '*/image/system/opt' -printf '%p -> %l\n'` prints the link -- the failing
  control; the same two commands on an export of the fix's tip print
  nothing. `tools/pkgcheck image` exits 0 with the tree's copy and with
  T6's widened copy (`44f64842b6`, the one this worktree's baseline used).
  `grep -n 'INSTALL' projects/ROCKNIX/packages/virtual/image/package.mk`
  shows the references inside the function only.
- **Already written:** nothing on devices: the link is the intended result
  and stays through the install step. Build roots and worktrees that
  sourced the recipe carry `build.*/image/system/opt`, which the next image
  build overwrites with the same link. Say so in the commit.
- **Acceptance (PL-02; #852's first criterion):** the export test, both
  halves; `pkgcheck` with both copies; `git diff --stat 8ebaf8daad HEAD --
  projects` after S1 shows this one file. #852's second criterion
  (`unsquashfs -ll SYSTEM opt` on the first image) stays
  `fix-pending-image`, the coordinator's at the first build.
- **Commit:** `image: create the Entware link in post_install, not at
  recipe load` (or the lane's words in that shape), `Refs #852, #895,
  #655`, the attribution line; `git add -- <the one file>`; `git status
  --short` empty after.

## S2. `mangohud`'s three subprojects come through `get_archive` with a checksum (PL-13, #893) -- `fix-tree`, then `fix-pending-image`

- **Why a stream:** Medium; the recipe is ROCKNIX's, the fix is contained
  (rule 6), and the fork already has the shape for it in the same function
  (`:56-63`, `50f3eeb726`): a source package per subproject, hash-checked by
  `get_archive`, copied from `${SOURCES}` at configure. A #585 candidate
  afterwards; the coordinator posts it.
- **Files owned:** `projects/ROCKNIX/packages/apps/mangohud/package.mk`
  (`pre_configure_target`, `:66-91`; the dependency line that names the
  three new packages -- `PKG_DEPENDS_TARGET`, or `PKG_DEPENDS_UNPACK` as
  `spirv-tools` does for `spirv-headers`) and three new recipes beside the
  two that exist: `projects/ROCKNIX/packages/apps/mangohud-imgui/package.mk`,
  `.../mangohud-implot/package.mk`, `.../mangohud-spdlog/package.mk`, each
  in `mangohud-vulkan-headers/package.mk`'s shape (`PKG_TOOLCHAIN="manual"`,
  `PKG_DEPENDS_TARGET="toolchain"`, `PKG_SOURCE_NAME` the archive's own
  name, `PKG_VERSION` the tag, `PKG_URL` the archive the recipe fetches
  today -- `https://github.com/ocornut/imgui/archive/refs/tags/v1.91.6.tar.gz`,
  `https://github.com/epezent/implot/archive/refs/tags/v0.16.zip`,
  `https://github.com/gabime/spdlog/archive/refs/tags/v1.14.1.tar.gz` --
  and `PKG_SHA256` from a fetch into an empty directory, the command and the
  hash pasted on #893). The `meson-patches/*.zip` unzips and the `rm`
  lines stay; the `curl` and the archive they fetched go, replaced by an
  unpack of `${SOURCES}/<package>/<PKG_SOURCE_NAME>` into `subprojects/`
  that leaves the directory meson expects (today's `tar -xvf ... -C
  subprojects/` does; a `directory =` line in a shipped `.wrap`, if
  mangohud ships one for these three, says what that is -- read before the
  shape is chosen).
- **Hunt first** (#893's own line, output in `02`): `git grep -n -E 'curl
  -[A-Za-z]*L|wget ' 8ebaf8daad -- 'projects/ROCKNIX/packages/*package.mk'`;
  every hit outside `mangohud` is a verdict line, not a change.
- **The test first, on the host** (no compiler: M6 builds nothing,
  D-WORKFLOW-191): with `SOURCES_DIR=$PWD/.qa-scratch/t8/s2/sources` -- so
  the shared cache is not written; `config/path` reads
  `SOURCES=${SOURCES_DIR:-$ROOT/sources}` -- `PROJECT=ROCKNIX DEVICE=SM8550
  ARCH=aarch64 scripts/get mangohud-imgui` (and the other two) fetches each
  archive through `get_archive` and writes its `.sha256` stamp: the
  positive. A scratch copy of one recipe with its `PKG_SHA256` altered by
  one hex digit makes the same `scripts/get` fail: the guard seen to fire.
  `tools/pkgcheck` exits 0 on the four recipes. `grep -c 'curl '
  projects/ROCKNIX/packages/apps/mangohud/package.mk` prints 0.
  `PROJECT=ROCKNIX DEVICE=SM8550 ARCH=aarch64 bash -c '. config/options
  mangohud >/dev/null 2>&1; printf "%s\n" "$PKG_DEPENDS_TARGET
  $PKG_DEPENDS_UNPACK"'` names the three.
- **Two things to read before choosing:** `scripts/build` passes
  `--wrap-mode=nodownload` to every meson configure; the three subprojects
  are directories meson finds in place, so the mode is satisfied as it is
  today. GitHub tag archives are this tree's usual source, and the stamp
  guards the fetch; the mirror's second line in `get_archive` will miss
  these names until ROCKNIX carries them, which is the #585 row's point.
- **Already written:** nothing on devices; every SM8550 image built
  `mangohud` from whatever the three URLs served, unrecorded; the fix
  verifies the next build. A changed recipe restamps `mangohud`
  (`calculate_stamp`): say so.
- **Acceptance (PL-13; #893's first two criteria):** the grep prints 0; the
  three fetched at their recorded sha256 (commands and hashes on #893);
  `pkgcheck` on four; `git diff --stat 8ebaf8daad HEAD -- projects` shows
  S1's file and these four. #893's third criterion (the SM8550 build's
  `pre_configure_target` lines) is `fix-pending-image`, the coordinator's.
- **Commits:** one for the three recipes (`mangohud: add imgui, implot and
  spdlog as checksummed source packages`), one for the recipe (`mangohud:
  unpack the three subprojects from the source cache`), each `Refs #893,
  #895, #655`, the attribution line.

## S3. The installer stops at a failed step and says which, and no longer forks itself without a pad (PL-14, #894; #899 found on the guest; G-02 to G-06 read) -- `fix-guest`

- **Why a stream:** Medium; a person installing GENERIC_X64 on a PC is told
  the install completed after a wipe, format or mount failed. The script is
  LibreELEC's and ROCKNIX's with the fork's identity edits; a contained fix
  (rule 6), a #585 candidate afterwards.
- **Files owned:** `projects/ROCKNIX/packages/tools/installer/scripts/installer`
  only. No restructuring: the steps stay where they are; each destructive
  command gets a test.
- **#899, found by the lane on the first guest run (13:4x UTC) and added here
  by the coordinator:** with no game controller `control.ini` is empty,
  `GPTOKEYB` is unset, and line 45's `${GPTOKEYB} "installer" -c ... &` runs
  the installer itself in the background, without end; a copy whose dialog
  returns Close runs `poweroff -f`, which powered the guest off. Its fix is
  a guard on `:43-47` (the gptokeyb line runs only when `GPTOKEYB` is set),
  its own commit (`Refs #899, #895, #655`), **made first**, so that #894's two
  runs then happen on the fixed script with no `gptokeyb` or `poweroff`
  stub -- a real input (no controller, the guard), not a named substitute.
  The stub reproduction stands as #899's failing control in `02`, and a stub
  `gptokeyb` recording its argv is the fixture #899's third criterion names.
  Punch item PL-18 (Medium, Q3, `bug`, #899); a #585 row, the coordinator's.
- **The shape:** the steps run inside `{ ... } | whiptail --gauge`
  (`:200-372`), where stdout is the gauge, so a failure cannot show a dialog
  from inside. Inside the braces, `dd` (`:207`), the label and partition
  commands, `partprobe`, `mkfs.vfat` (`:280`), `dosfslabel`, `mount`
  (`:303`) and the copy of the system files each test their status; on
  failure the step's name is written to a marker under the script's own
  `$TMPDIR` and the braces are left (`exit 1` ends the subshell; the gauge
  closes). After the pipe (`:372`), the script reads the marker: present,
  a message box titled with the install's failure whose text says which
  step did not finish, that the disk may be partly written, and what to do
  (`player-language.md`: what did not happen, what is in place, the next
  step -- "Check the disk and the cable, then run the installer again." --
  no exit code; the log's path only if the script already shows it
  elsewhere, read `:1-60`); absent, the existing "Install Complete". No
  `set -e` (the gauge's subshell and the script's own tolerated failures
  make it wrong). The interpreter is busybox `ash`: `bash -n` is a syntax
  read; also run the image's busybox `sh -n` if one is on hand (the M7 x64
  root's `image/system/usr/bin/busybox` is read-only and may be run from our
  own directory), and quote both.
- **The leads** (G-02 to G-06) are read, each with a verdict line in `02`:
  fixed here only where it is a one-line guard inside this shape (G-03,
  `PARTID` reset before the device case, if the read agrees); G-02 (the
  mount-source text match), G-04 (512-byte sectors), G-05 (the boot-config
  order), G-06 (the helper's cleanup) are #585 rows unless the lane finds
  one is a one-liner and says so. Nothing else changes.
- **The bench:** a GENERIC_X64 guest. **M6 holds the host** (the host
  file's last M6 line; `pgrep -c -x qemu-system-x86` before the boot, 0
  expected; one guest at a time; `--pidfile`; `tools/vm-stop`; an M6 line in
  `/tmp/m7-m6-host-coordination-20261023.txt` before the boot and after the
  stop, with the census). The image: the M6 lanes' copy of the M7 build
  `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`
  with its `.sha256` sits in `/workspace/artifacts/m6-t1-20261023/` (T1's)
  and `/workspace/artifacts/m6-t2-20261023/`; copy it to
  `/workspace/artifacts/m6-t8-20261024/`, check the sha256 after the copy,
  make `t8.qcow2` from it as T1 and T2 did (their `docs/vm-qa-log.md`
  entries and the T30 hand-back carry the recipe). Nothing is written in
  the M7 tree. The target is a second virtual disk: a 2 GB raw file for the
  passing run; for the failing run a real failing target -- the same disk
  attached `readonly=on` (fails `dd`, the wipe), or an 8 MB raw file (too
  small: fails the partitioning or `mkfs.vfat`). `generic-x64-vm run` takes
  no second disk (its `--help`); `generic-x64-vm qemu-args` prints the QEMU
  command, so run that command with one `-drive
  file=<raw>,if=virtio,format=raw[,readonly=on]` added, `--pidfile` kept.
  A shadowed `mkfs.vfat` in `PATH` is a synthetic input (`vm-first.md`):
  used only if neither real target fails at the format or the mount, and
  named as such on #894.
- **Getting the fixed script in:** SSH is off on a fresh image; through
  `tools/vm-serial`, either start `sshd` for the session and `scp` the
  script to `/storage/installer`, or paste it in chunks; then `sh
  /storage/installer`. From the serial console the dialog is drawn on
  serial, and the transcript is the evidence (#894's first criterion as
  widened at 13:2x UTC); on the guest's own display it needs `essway`
  stopped and a VT the lane owns (`tools/vm-visual-qa` for the frame).
  Either is accepted; name which.
- **The fixture:** run 1, the blank target: the install runs through and
  ends on "Install Complete"; `blkid` on the target after shows the two
  labels. Run 2, the failing target: the dialog names the step that did not
  finish. Both transcripts (or frames) and the serial log's lines on #894
  and in `02`; the cycle in `docs/vm-qa-log.md` (image, qcow2, disks,
  commands, outcome, stop by pidfile).
- **Already written:** nothing the fix reads: an install that failed and
  said complete left a disk since reinstalled or noticed.
- **Acceptance (PL-14; #894's two criteria):** run 2's dialog names the
  step; run 1 ends on Install Complete; `bash -n` (and busybox `sh -n` if
  on hand) pass; `git diff --stat 8ebaf8daad HEAD -- projects` adds this
  one file; the five leads' verdict lines in `02`.
- **Commit:** `installer: stop at a failed step and say which`, `Refs #894,
  #895, #655`, the attribution line.

### S3 addendum (14:2x UTC): #899's guard reaches line 41 too

The lane narrowed #899's second criterion to its fix's first scope (`:43-47`),
because `:41`'s unconditional `get_controls` still prints `command not found`
once without a pad. The scope was the coordinator's and is widened instead:
`get_controls` runs only when it is defined (`command -v get_controls
>/dev/null 2>&1 && get_controls`, or the same test the gptokeyb line uses),
so the installer says nothing and goes on without pad input, and the
criterion's original clause stands (restored by the coordinator on #899). One
more commit on the same file, `Refs #899, #895, #655`; the guest run that
proves it is S4's (one quick install, its serial transcript read for the
line).

## S4. The installer writes its boot configuration after the copy (PL-19, #901; the seat's G-05, confirmed by S3) -- `fix-guest`

- **Why a stream:** S3 confirmed it from the installed bytes: the installer
  writes its `syslinux.cfg` (`:321-328`, `DEFAULT linux`, the two labels, no
  `portable`) and then `cp -r /flash/*` (`:339`) lands the media's
  `syslinux.cfg` over it (`scripts/mkimage:145-153`: `DEFAULT run`, the
  `portable` word, an `installer` label). Upstream's order is the same
  (`09810c3ece`); a contained fix is ours (rule 6) and a #585 row, the
  coordinator's. The brief excluded reorders from S3 to keep it bounded;
  this is the one reorder, in its own stream, now that it is a confirmed
  defect rather than a lead. `portable` at boot is `init:1245`'s branch
  (`SYSLINUX_DEFAULT="run"`): the installed disk boots the `run` label with
  the same two labels, so the file is wrong and the boot the same; the
  severity is the lane's call from that read, written in PL-19.
- **Files owned:** `projects/ROCKNIX/packages/tools/installer/scripts/installer`
  only, the `x86_64` arm of the `case` and the copy.
- **The shape:** the generated file must be the one on the disk. Either move
  the `x86_64` bootloader-configuration block (the `syslinux.cfg` heredoc and
  the two EFI copies) below the `cp -r /flash/*`, keeping `syslinux -i` where
  it is, or copy everything but `syslinux.cfg`. Read the `arm|aarch64` arm
  first (`update.sh` with `BOOT_ROOT=/flash`) so its order is untouched, and
  read whether the media's `EFI/BOOT/*` differ from the two files the
  installer copies at `:331-332` (the sibling S3 named); say which in `02`.
- **The test, on the same guest and disk recipe as S3:** a quick install onto
  a blank 6 GiB virtual disk; afterwards the target's system partition is
  mounted (over SSH or serial) and `syslinux.cfg` read: `DEFAULT linux`, the
  two labels, no `portable` (the passing run); S3's own read of the pre-fix
  install (`DEFAULT run`, `portable`) is the failing control and is quoted
  beside it. The media's `/flash/syslinux.cfg` first line before and after.
  The serial transcript of this run is also the proof of the S3 addendum (no
  `get_controls: command not found`). Census, pidfile, `tools/vm-stop`, the
  host-file lines and the `vm-qa-log` entry as before.
- **Already written:** every GENERIC_X64 disk installed so far carries the
  media's file; a reinstall rewrites it; nothing under `/storage` or a cloud.
- **Acceptance (PL-19; #901's two criteria):** the target's `syslinux.cfg`
  lines quoted; the media's unchanged; `bash -n` and busybox `sh -n`; `git
  diff --stat 8ebaf8daad HEAD -- projects` still six files.
- **Commit:** `installer: write the boot configuration after the system
  files are copied`, `Refs #901, #895, #655`, the attribution line.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-01 (#890):** resolved by the packet `fix/m6-890-shs-sha256`
  (`566b01448f`), reviewed, merging before T5's branch; `fix-tree`.
- **PL-03, PL-04 (#891, #892):** deferred to **#585**, as T7's four dead
  URLs were: the recipes are upstream's, the mirror serves the bytes, no
  new URL is known; each bug stays open, Low, with the mirror named, until
  a URL exists or a register row accepts mirror-only, with #844 the guard.
  For #892, `openabl` is read at the integration (conflict row 10) before
  any deletion. The coordinator posts both on #585.
- **PL-05 (`cairo`):** deferred to **#896** (filed at this pause, #839's
  shape; ROCKNIX's generic is 1.18.4 too, so the project is the mover); no
  pin moves in M6; read with the merge's conflict row 2.
- **PL-06, PL-08:** deferred to **#657** (the coordinator posts the two
  rows: the freshness tool's three blind shapes with the 17-of-19 count;
  `pkgcheck`'s if-arm duplicate with `moonlight` as the failing control).
- **PL-07, PL-10, PL-16, and PL-17's upstream shapes** (G-09
  `111-sway-init`'s `cut -b 5` and `head -n 1`; G-21 `glibc`'s `-O.`
  rewrite; G-23 `wlr-randr`'s parser; G-24 the `m8c` configs' doubled
  scancode): deferred to **#585**, one proposal the coordinator posts, with
  PL-07's six full hashes resolved today.
- **PL-17's three fork shapes**, the coordinator's call:
  - G-14 (`avahi-daemon.service`'s `After=network-base.service` without
    `Wants=`) is **withdrawn**: `network-base.service` is enabled by
    `projects/ROCKNIX/packages/sysutils/systemd/package.mk:328`
    (`enable_service`), so the target pulls it in and `After=` alone is the
    ordering the fork's own comment on the line asks for (fork #50). The
    lane records the verdict with that evidence.
  - G-17 (`tailscale`'s one cache name for two architectures): the shape is
    upstream's -- the fork's two lines in that recipe are its freshness
    comment (`63a2090a56`) -- so a #585 row; the one-line `PKG_SOURCE_NAME`
    fix may ride the integration as a `fix-tree` if upstream has not
    changed the recipe by then. Not a stream here.
  - G-24 (the GENERIC_X64 `m8c` config): the fork's copy (`cbdb91a517`) is
    H700's config, which upstream carries with the same two `=69` lines; a
    #585 row, and the fork's copy follows upstream's fix.
- **PL-09, PL-12:** the integration's pre-read, the coordinator's (`02` §
  The conflict set, 11 rows; `04`'s orphan table, 11 rows); nothing on this
  branch.
- **PL-11:** settled by D-WORKFLOW-198 and, for the third file,
  **D-WORKFLOW-199** (the triple: the `spirv-headers` override is kept at
  the base merge too; the lane's G-27 confirmed by the coordinator from
  history -- `b4fc2a28cf` modified it since the base, `6679670966` deleted
  it upstream in the same merge as `glslang`'s); the bump is **#897**. The
  inventory's `unreached` on it is a true reading of the plan: `tools/viewplan`
  for GENERIC_X64 lists `glslang` and `spirv-tools` and no `spirv-headers`,
  because `genbuildplan.py` does not follow `PKG_DEPENDS_UNPACK` while
  `config/functions:1331` unpacks it at build time; the coordinator files
  that as the inventory's lead.
- **PL-15:** deferred to **#844** (the coordinator posts the lead).

## Order and hand-back

S1, S2, S3 -- the guest last -- each committed and proved before the next
starts, with a checkpoint on #655 at the end of each; then stage F (`02`
appended, every proof's `proved:` cell one of `tree`, `history`,
`fixture`, `fix-tree`, `fix-guest`, `fix-pending-image`), stage G (the
retro: what the slice did to the two time-to-play numbers -- nothing, say
so), stage H (the hand-back on #655, `reviewed-at:`/`fixed-at:` in its
body; the Phase 7 table with every item's outcome as above, the Backlog
numbers in it). The coordinator accepts by brief § 10 (the membership
block, the (a) loop, the conflict set's derivation and the `pkgcheck`
baseline on an export; the (b) loop and the HEAD probe on seeded rows;
`register-check` on a simulated merge) and closes #895. **A stream that
would change a file outside the ones named, move a pin, change a checksum
the stream does not add, or delete anything, stops and asks on #655** --
and does not end its turn on the question: it posts it and continues with
what does not depend on the answer.
