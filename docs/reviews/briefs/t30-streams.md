# T30's remediation streams (#677, audit issue #872)

Written by the coordinator at T30's stage-D pause (2026-10-24, 10:33 UTC
post at `8dad7513fc`; D-WORKFLOW-189), one stream per group of related
items, each in the D-WORKFLOW-056 shape: the files owned, the test first,
the `Already written:` line, commits cut from intermediates only after the
checks are green. Streams are numbered in the order they run; **S0 runs
first**, because its two eval sites run a ROM library's text as root. The
lane's brief (`docs/reviews/briefs/emulators-standalone.md`) § 5 and § 6
still govern what runs where, and nothing here builds an image. Plan § 6b E
binds every stream: **a commit names its paths** (`git add -- <files>`,
`git status --short` read before and after); **a time is produced, never
typed**; **a fixture runs the real script over fixture files with the
image's tools borrowed read-only** (the GENERIC_X64 M7 root's
`image/system/usr/bin/busybox`, `bash` and `sed`, never a process started in
that tree), **lifts by marker lines and takes a commit or `WORKTREE`
argument**, and **prints each stub's call count beside its verdict**; **a
tree export goes under `/workspace/tmp/m6-t30/` after `df -i`**.

Common to every stream: the commits land on the slice branch
`feature/m6-emulators-standalone-677` in the lane's own worktree; no `fix/*`
packet is cut from these (the M7 candidate carries the same scripts, but the
maintainer's M7 request named #802 and #806 only; the coordinator tells M7
on the host file which of these it may want, after the hand-back). Every
commit cites the punch item and its `bug` issue with `Refs` (no closing
keyword: the criteria close on a guest or an image); the scripts keep their
upstream headers and a ROCKNIX line; `bash -n` runs on every script
touched and `tools/pkgcheck` on every recipe touched (a recipe comment
restamps the package: say so); `git status --short` is empty after each
commit; the running log gets a `PROOF:` line per proof; the punch list's
Phase 7 table and `punch_index` are updated at the end of each stream,
never mid-way. **Guest cycles** are named on #677 before each boot with
what they leave (the T30 disk only; frames under
`/workspace/artifacts/m6-t30-20261024/`), run one at a time with census,
pidfile and `tools/vm-stop`, and the host file
(`/tmp/m7-m6-host-coordination-20261023.txt`) is read before each boot:
the host is M6's since 05:42, and a new M7 block ends the cycle at its next
stop. A stream that cannot meet its test says so on #677 and stops; the
coordinator re-cuts the stream. **An item fixed upstream already** (class 1
in q4a: PL-001's `4a6415c033`, PL-003's `eeb33c5a37`, PL-004's `2e7041d273`)
is fixed here with upstream's lines where they are right, named in the
commit, so the base merge meets no conflict and #585 records *already
upstream*.

## S0. Commands built from data (PL-007 #859, PL-018, PL-008 #860, PL-019 #865, PL-031) -- security, first

- **Why first:** `start_scummvm.sh:66-72` runs a `.scummvm` file's content
  through `eval` as root (G3 left a root-owned marker), and
  `start_yabasanshiro.sh:46-55` `eval`s a pad's self-reported name. The other
  three are the same shape without the shell: arguments built by
  `echo | xargs` (gzdoom: a WAD path with an apostrophe never launches) or by
  word-splitting a string (gopher64's password; Steam's URI and `-silent`).
- **Files owned:** `scummvm-sa/scripts/start_scummvm.sh` (66-72),
  `yabasanshiro-sa/scripts/start_yabasanshiro.sh` (46-55),
  `gzdoom-sa/scripts/start_gzdoom.sh` (49-96),
  `gopher64-sa/scripts/start_gopher64.sh` (97-125),
  `steam/scripts/start_steam.sh` (the argument lines 205, 240, 260 only; S2
  owns its control flow at 253 and 264 -- the same file, two streams, in
  order), all under `projects/ROCKNIX/packages/emulators/standalone/`.
- **The test first:** G3's crafted `.scummvm` (`; touch /tmp/t30-svm-injected`)
  and its plain control, on the guest; G14's Freedoom renamed
  `Free Doom's Gate.wad` beside the plain name; fixtures that print the
  argument vector for gopher64 (empty password; a password with a space) and
  Steam (URI and `-silent`), and a yabasanshiro fixture with a device name
  holding `'; touch /tmp/x; '`. Each run first against the unfixed script
  (the marker appears; `xargs: unmatched single quote`; the ROM path lands
  in the password's slot) so the fixture is seen to fail.
- **The change:** scummvm parses the file without a shell -- the path
  between the first pair of quotes and the target id after it
  (`runemu.sh:310`'s awk shape), passed as two quoted arguments; yabasanshiro
  builds the mapping file's name by stripping the quotes the script added,
  no `eval`; gzdoom builds `params` as a bash array and runs
  `"${EMUPERF[@]}" /usr/bin/gzdoom "${params[@]}"`; gopher64 builds its
  arguments as an array, passes the password only when it is not empty, and
  prefers gopher64's own token file once one exists; Steam keeps the URI and
  `-silent` as two array elements.
- **Already written:** nothing stored by any of the five; a crafted
  `.scummvm` in a library would have run once per launch.
- **Acceptance (PL-007, PL-008 on the guest; the rest by fixture):** the
  crafted `.scummvm` launches ScummVM or its error and leaves no marker, and
  Flight of the Amazon Queen's still launches (G15); the renamed Freedoom
  reaches its first frame and so does the plain name (G14's harness); the
  three fixtures print the expected vectors and create no `/tmp/x`.
- **Commit** per script, `<package>: <text>`, each `Refs` its bug (#871 for
  yabasanshiro and Steam's argument line) and #872.

## S1. The link step keeps what is there (PL-012 #863, PL-029, PL-036, PL-014 #864) -- state, High

- **Why here:** nine start scripts delete a real directory before linking
  it, with no copy (G8: a real `memcards` beside an existing target lost its
  card; G16: DuckStation started from the Tools launcher makes `savestates`
  a real directory and the next game launch deletes its contents). The three
  smaller items are the same family: flycast links over a path its own move
  may have made a directory, OpenBOR empties `/storage/openbor/Paks` every
  launch, NanoBoyAdvance makes a directory where the BIOS file belongs.
- **The helper, and where it lives:** one function, `link_storage_dir
  <source> <target>`: when `<source>` is a real directory, copy it into
  `<target>` without overwriting (`cp -n`), verify every file arrived
  (count and `cmp` per file), remove the source only then, and link; when
  it is already a link to `<target>`, do nothing; on any failure leave both
  in place, print one line, exit non-zero. **It is installed as
  `/usr/bin/link_storage_dir` from a new file
  `projects/ROCKNIX/packages/rocknix/sources/scripts/link_storage_dir`** --
  a path outside the 543 and inside T1's accepted area, which the
  coordinator authorises here because it is a new file (no merge conflict
  with T1's branch), the `rocknix` recipe installs every file under
  `sources/scripts/` (the lane reads the recipe's install loop and quotes
  the line; if it does not, the stream stops and says so), and the nine
  scripts have no other shared home. The fourth ladder item is this
  helper, so it is not filed separately.
- **Files owned:** the new helper; the link sites in `duckstation-sa/scripts/start_duckstation.sh`
  (28, 33, 37-47), `rpcs3-sa/scripts/start_rpcs3.sh` (14-29),
  `azahar-sa/scripts/start_azahar.sh` (28, 32, 37, 226), and the drastic,
  ares, skyemu, bigpemu, hatari and cemu sites `02` F-12 lists;
  `flycast-sa/scripts/start_flycast.sh` (25-35, and 149's kill by the PID
  it started); `openbor/scripts/start_OpenBOR.sh` (27: remove only the link
  the previous launch made); `nanoboyadvance-sa/scripts/start_nanoboyadvance.sh`
  (21-22: remove the copy -- the emulator runs its HLE BIOS when the file
  is absent -- and remove an empty `gba_bios.bin` directory the old script
  made, only when it is that copy).
- **The test first:** the helper's fixture with the image's busybox: a real
  source directory with two files and an existing target (expect: both
  files once under the target, the source replaced by a link); a source
  that is already the right link (expect: untouched); a copy made to fail
  (a read-only target; expect: both in place, rc non-zero, one line). Then
  G8 on the guest for DuckStation, and G16's Tools-launcher sequence (a
  synthetic state in the real directory survives the next game launch). A
  real file under `/storage/openbor/Paks` survives an OpenBOR launch on the
  guest. flycast: two launches leave `data` a link to `bios/dc` and kill
  only the launch's gptokeyb. NanoBoyAdvance by fixture (SM8550 only).
- **Already written:** saves already deleted are gone; saves sitting in a
  real directory today (an archive restored before a link existed, a Tools
  launcher's session) are kept and merged on their next launch; PAKs
  deleted from the staging folder are gone; a `gba_bios.bin` directory on
  SM8550 handhelds that launched NanoBoyAdvance without a BIOS is removed
  when it is the script's copy; a `dreamcast/data` directory moved by
  flycast's old script is kept.
- **Acceptance:** the G8 fixture keeps the synthetic card (found once under
  the target) and replaces the directory by the link, and a failed copy
  leaves the directory in place; G16's state survives; the OpenBOR file
  survives; flycast's two launches; the NanoBoyAdvance fixture leaves no
  `gba_bios.bin` and removes the old directory.
- **Commit:** the helper first (`rocknix: add link_storage_dir ...`, `Refs
  #863, #872`), then one per script (`Refs` #863, #871 or #864, and #872).

## S2. Exit: every kill target names a process (PL-001 #853, PL-002 #854, PL-003 #855, PL-004 #856, PL-030 #867)

- **Files owned:** `duckstation-sa/scripts/start_duckstation.sh:9` and
  `duckstation-sa/sources/Start Duckstation.sh:9` (`-9 duckstation-qt`,
  upstream's `4a6415c033`); `openbor/scripts/start_OpenBOR.sh` (source
  `/etc/profile`, `set_kill set "-9 OpenBOR"` before the run; gptokeyb by
  PID); `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh:9`
  (`set_kill set "-9 mupen64plus mupen64plus-simple"`, upstream's
  `eeb33c5a37`); `hatarisa/package.mk:38` and
  `hatarisa/scripts/start_hatari.sh` renamed `start_hatarisa.sh` with
  `set_kill set "-9 hatarisa"` (upstream's `2e7041d273`; the recipe's
  install line follows the rename; a recipe change restamps `hatarisa`);
  `steam/scripts/start_steam.sh:253,264` (return the session's status
  instead of `exit 0`, so `steam_dual_screen_end` and the binfmt restore
  run), `steam/scripts/start_steam_x86.sh:10,26-30` and
  `start_steam_arm64.sh:28-30` (gamescope and steam beside FEX in the x86
  kill target).
- **The test first:** on the guest, G7 (DuckStation: the written target ends
  the process), G1 (OpenBOR: `/tmp/.process-kill-data` names OpenBOR during
  the launch and `killall $(cat ...)` ends it), G6 (a renamed substitute
  named `mupen64plus-simple`, the substitute named in the tick), G2
  (`runemu.sh <st> -Patarist --core=hatarisa --emulator=hatarisa` reaches
  hatarisa, no exit 127, its kill data ends it; EmuTOS is the content); a
  fixture sourcing `start_steam.sh` with stub launch functions that record
  their calls (expect `steam_dual_screen_end` and the binfmt start recorded
  after `steam_launch_bigpicture` returns; counts printed).
- **Already written:** nothing for the kill data (tmpfs, one launch);
  `systemd-binfmt` stays stopped until the next boot on devices that ran an
  x86 Steam session -- the fix restores it at the session's end, and the
  reboot every update brings resets it for the rest.
- **Acceptance:** PL-001 to PL-004's guest lines; PL-030's fixture record.
- **Commit** per package; the three class-1 items name upstream's commit in
  the message.

## S3. Achievements: the session and the credentials (PL-009 and PL-010 #861, PL-021 and PL-039 #870, PL-020 #866, PL-034, PL-037)

- **Files owned:** `ppsspp-sa/scripts/cheevos_ppsspp.sh` (23-33, 35, 105),
  `flycast-sa/scripts/cheevos_flycast.sh` (19-30),
  `armsx2-sa/scripts/cheevos_armsx2.sh` (29-40, 46-48),
  `skyemu-sa/scripts/cheevos_skyemu.sh`, `duckstation-sa/scripts/cheevos_duckstation.sh:20`
  (the quote only; S5 may remove the file: if S5 does, this edit is moot
  and the Phase 7 row says so), `melonds-sa/scripts/cheevos_melonds.sh`
  (78-104), `duckstation-sa/scripts/start_duckstation.sh:128-131` (PL-037's
  comment). `aethersx2-sa`'s script is **not touched**: the recipe goes with
  the base merge (PL-025, class 1).
- **The test first:** the G9 fixture over each script with the image's
  busybox: switch 1 and token empty with a synthetic old token pre-seeded
  (expect 0 old-token lines and a disabled flag); the switch key unset
  (expect the disabled branch, rc 1); a token holding `/`, `&` and a
  backslash and a value holding `|` and `\` for melonDS's `set_key` (expect
  the bytes intact); the mode of `ppsspp_retroachievements.dat` after the
  run (expect 0600, written once). Each fixture first against the unfixed
  script.
- **The change:** on *off* and on *on, token empty*, publish a disabled
  session (`cheevos_dolphin.sh`'s `publish_disabled` shape: enabled false,
  token and user cleared) in ppsspp, flycast, armsx2 and skyemu; quote the
  four `[ "${enabled}" != "1" ]` tests; write the token files once with
  `umask 077`, `mktemp` and `mv`; write each emulator's achievements section
  whole by temp and rename with the values as data (armsx2's first section
  gains its three keys); melonDS's `set_key` escapes `|` and `\` -- **the
  password's presence in `melonDS.ini` stays #866's open half**: the token
  login the patch's library carries is a patch change and a build, deferred
  on #866 to after the renovation; PL-037: one comment above
  `start_duckstation.sh:131` naming upstream's workaround and the proof its
  retirement needs (DuckStation's own sign-in on a guest), nothing removed.
- **PL-034 (melonDS's TOML) is read, not assumed:** the stream reads the
  patch's config writer (`000-retro-achievements.patch:7519-7522` and the
  melonDS `Config` code it patches) and says whether `RetroAchievements.Password`
  or `.Token` reaches `melonDS.toml`. If yes: a `bug` for the cloud area
  (`backuptool`'s `RATOKENSETTINGS`, outside the 543) filed by the lane
  with the lines quoted, and PL-034 resolved as *confirmed, deferred to
  #N*; if no: withdrawn with the lines quoted; if the writer cannot be read
  to a verdict: *open item to test*, said so (`bugs-are-agent-first.md`).
- **Already written:** the old token sits in each emulator's config on
  devices that hit the state -- rewritten at the next launch (read both,
  overwrite on use); the password sits in `melonDS.ini` on SM8550
  handhelds (backups blank it; the open half of #866); token files keep
  their mode until the next write.
- **Acceptance:** the G9 fixture's lines per script; the mode line; the
  melonDS escape line; PL-034's verdict with its quoted lines; PL-037's
  comment present.
- **Commit** per script, `Refs` #861 / #870 / #866 and #872; PL-034's
  outcome in its own commit message or its own issue.

## S4. The launch scripts do what they say (PL-006 #858, PL-011 #862, PL-015, PL-017, PL-028, PL-032 #868, PL-033 #869, PL-038, PL-040, PL-041 #871)

- **Files owned:** `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh`
  (35, 70, 78, 81, 83, 211), `hatarisa/scripts/start_hatarisa.sh:37` (after
  S2's rename) and `amiberry/scripts/start_amiberry.sh:76` (the `.zip`
  test), the eleven redirection sites `02` F-11 lists (aethersx2's excluded:
  class 1), `amiberry/scripts/start_amiberry.sh` (34, 62, 70-71),
  `mednafen/scripts/start_mednafen.sh` (8, 175),
  `drastic-sa/scripts/start_drastic.sh` (28-31, 83-92),
  `dolphin-sa/scripts/start_dolphin_gc.sh` (43-47, 72-76, 404-419) and
  `start_dolphin_wii.sh` (373-387), `xemu-sa/scripts/start_xemu.sh:19`,
  `melonds-sa/scripts/start_melonds.sh:181-182`,
  `scummvm-sa/scripts/start_scummvm.sh` (22-25, 31-44), and the twenty-two
  F-42 sites `04` § Second opinion lists, each at its line.
- **The test first (guest where GENERIC_X64 ships the emulator, fixtures
  with the image's busybox for the rest, every substitute named):** a
  zipped synthetic `.z64` reaches mupen64plus with the member as its ROM
  argument and a ROM named `Zippy Race.z64` is not unzipped (`exec.log`);
  the redirection grep (`grep -E '\[ [^]]*[^-]( <>| >| <) [^]]*\]'` over the
  55 shell files) prints nothing after and the fixture over each fixed line
  creates no file; amiberry's fixture writes `gfx_width=<w>` and
  `gfx_height=<h>`; mednafen's line 175 passes `${DM}` and no `set -x`;
  mupen64plus leaves no copy of an unzipped ROM under `/tmp/mupen64plus`
  and a setting changed in the emulator survives the next launch; DraStic's
  fixture with a stale `/storage` copy and a newer image copy runs the newer
  and leaves `drastic.cfg` alone; two Dolphin launch preparations with
  `FACE_SWAP=yes` leave `Hotkeys.ini` byte-identical (a fixture pad row with
  a>b, named); a setting changed in `xemu.toml`, `melonDS.toml` and
  Dolphin's GameSettings survives the next preparation; ScummVM with
  `/storage/.config/scummvm` absent seeds it from `/usr/config/scummvm` on
  the guest; each F-42 site has its one-line check or is withdrawn with its
  reason in the stream's record.
- **The change:** `unzip -qql` (upstream's `195a8eba4b`) and
  `case "${1,,}" in *.zip)`; numeric tests and `!=`, and the removal of
  `/storage/0`, `/storage/1`, `/storage/2]` and the sha1-named file **only
  if present and empty**; amiberry writes its keys, uses `grep -E`, seeds
  only when absent; mednafen's `${DM}`, no `set -x`; mupen64plus passes the
  ROM in place and keeps its config in `/storage/.config`; DraStic runs the
  image's binary (or refreshes the `/storage` copy when it differs) and
  keeps the player's config; Dolphin applies the swap to a fresh copy each
  launch or marks the file swapped and swaps once -- and **normalises the
  file once** on devices that carry it in a swapped state (the `Already
  written:` of #869); xemu, melonDS and Dolphin seed only when absent;
  ScummVM tests the config directory before creating `games/` and strips `/`
  from generated names; the twenty-two sites each at their line.
- **Already written:** per item as `05` says -- empty junk files in
  `/storage` on handhelds (removed only when empty and of exactly those
  names); the player's overwritten configs are gone; DraStic's first-launch
  binary in `/storage/.config/drastic` is superseded by the image's;
  `Hotkeys.ini` in one of two swapped states (normalised once); a first-run
  device without a seeded `scummvm.ini` (seeded when absent).
- **Acceptance:** each item's line in `05`.
- **Commit** per script; `Refs` the bug (#858, #862, #868, #869, #871) and
  #872; a withdrawn F-42 site is a line in the Phase 7 table, not a commit.

## S5. Renovation: the shared Dolphin library, dead code, pin comments (PL-023, PL-024, PL-027)

- **Files owned:** `dolphin-sa/scripts/` (a new shared file both
  `start_dolphin_gc.sh` and `start_dolphin_wii.sh` source, installed by
  `dolphin-sa`'s recipe beside them; the dead `-v $GRENDERER` line dropped);
  the dead files `ppsspp-sa/scripts/psp_save_mover.sh` and
  `duckstation-sa/scripts/cheevos_duckstation.sh`, the six unused password
  reads in the cheevos scripts, touchHLE's echo of an unset variable;
  `supermodel-sa/package.mk` and `yabasanshiro-sa/package.mk` (one comment
  each naming the branch its `PKG_VERSION` is on and why; restamps both).
- **The test first:** `git grep` for every caller of a file about to be
  removed (none, quoted); `bash -n` on both Dolphin scripts after the
  split and a `diff` of each against the shared part showing only its
  system-specific half; `tools/pkgcheck` on the two recipes and on
  `dolphin-sa` (its install loop must carry the new file: quote the line).
- **The change:** `engineering-practices.md` § Before deleting a duplicate
  for each removal -- what the doomed copy guarded, stamped or exposed that
  nothing else does (none: the list is written out, empty where it is
  empty); the shared library; the two comments.
- **Already written:** nothing by any of them.
- **Acceptance:** no caller for any removed file; `pkgcheck` and `bash -n`
  pass; the Dolphin diff; the two comments present.
- **Commit** per package; `Refs #872` (and #871 where a site overlaps).

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-005 (#857) and PL-022 (#873):** T3's file. **Deferred to one packet
  at integration**, cut by a lane the coordinator dispatches after T3's
  branch merges (its S2 changed `add_es_system` in the same file): the
  standalone `add_emu_core` rows guarded by what the device builds,
  `PKG_ARCH` included, nds and saturn given a default the image carries,
  the AdvanceMame and moonlight rows removed or guarded, and the five
  tables regenerated under `env -i` in the C locale. `tools/t30-routes.py`
  is the check; the lane keeps it on its branch for that packet.
- **PL-013 (#849):** deferred, corrected -- ROCKNIX's mirror serves the
  archive with the recipe's sha256, so an empty-cache build succeeds through
  it; Low, *dead primary URL, mirror-covered*; no tree change.
- **PL-016 (`0c43a50420`) and PL-025 (`c4d353449e`):** deferred to the base
  merge, class 1; nothing on this branch.
- **PL-026:** deferred to **#878** (Backlog: the four bumps -- DuckStation
  `v0.1-11894`, ScummVM `v2026.4.0`, VICE `3.10`, BigPEmu `v1221` -- after
  the M7 candidate; D-WORKFLOW-187).
- **PL-035:** **open item to test**, #874 (Backlog: TERM first where an
  emulator writes at shutdown, the exit path's, T1's area); nothing on this
  branch; the Phase 7 row names it.
- **PL-034:** S3 decides it by reading (above); until then open.
- **The ladder:** #875 (standalone coverage in `tools/emulator-exit-test`),
  #876 (shellcheck in the fork CI), the kill-name resolution as a comment on
  #838; the shared helper is S1.
- **T30's brief, errata:** none owed by the proof so far; the lane records
  any it met in `01`.

## Order and hand-back

S0, S1, S2, S3, S4, S5, each handed back with one comment on #677 (the
stream, its commits, the fixture lines before and after, the guest cycle's
census and `vm-stop` line, the `punch_index` rows moved with their `proved:`
class) and the lane going straight on. Guest cycles: S0 (G3, G14, G15), S1
(G8, G16, OpenBOR, flycast), S2 (G7, G1, G6, G2), S4 (mupen64plus, Dolphin,
ScummVM); each named before its boot, one at a time. At the end: stage F
(`02` appended, every proof's `proved:` cell one of `tree`, `fixture`,
`fix-guest`, `fix-pending-image`), stage G (the retro, what the slice did to
the two time-to-play numbers), stage H (the hand-back on #677,
`reviewed-at:`/`fixed-at:` in its body); the coordinator accepts by brief
§ 10 and closes #872. **A stream that would change `runemu.sh`, the common
functions, `backuptool`, the launch table or any recipe outside the 543
other than `rocknix`'s new helper file stops and asks on #677**: those are
other areas' files.
