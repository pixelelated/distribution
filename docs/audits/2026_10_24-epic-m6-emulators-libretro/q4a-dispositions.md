# Q4 (a): the 14 upstream commits on the slice's two directories, dispositioned (2026-10-24)

`git log --oneline c445081a59..upstream/next -- projects/ROCKNIX/packages/emulators/libretro projects/ROCKNIX/packages/virtual/emulators`, with `upstream/next` at `3421d7d178`.

**What was established for every row:**

- **None of the 14 is on `next`.** The merge base precedes all of them, and none of their diffs (`git diff <c>^1 <c> -- <dirs>`) reverse-applies to the worktree, whose slice bytes are `next`'s.
- **Seven forward-apply on their own** (`git apply --check`): `075a7c303b`, `a1ea79474b`, `eeb33c5a37`, `c9820d0e89`, `096c0d4e96`, `142df62157`, `6679670966`.
- **Applied in date order onto an export of `next`'s two directories**, `af70bd435b`, `6103571f67`, `aca36dbad7`, `8704addb6b`, `bb8d0aab8e` and `c4d353449e` conflict.
- **The real three-way merge** (`git merge-tree --write-tree next upstream/next`, tree `d2df30a92a`) conflicts on the slice only in the five rotation-table recipes, and leaves two `build.${DISTRO}-` copies the fork's roots cannot satisfy (F-09).

The base merge is the coordinator's act. **Nothing here is applied on this branch** (brief § 5).

| # | Commit | What it changes on the slice | Disposition | Reason |
| ---: | --- | --- | --- | --- |
| 1 | `c4d353449e` (2026-10-18) aethersx2: drop package due to licensing concern | `virtual/emulators/package.mk` (27 lines), `Start AetherSX2.sh` removed | **to merge** (class 1, with the base merge; the coordinator's ruling on #650, maintainer told on #346) | F-07: a licensing removal; the fork's SM8550 carries the package. `Already written:` AetherSX2's settings and memory cards under `/storage` on devices that had it |
| 2 | `075a7c303b` (2026-10-17) the multimedia merge #3513 | adds `retroarch/patches/retroarch-0100-ffmpeg9-lavc63.patch` (189 lines) | **to merge**, with the rest of #3513 | the patch adapts RetroArch to the FFmpeg the same merge brings; one without the other breaks one build or the other. Applies cleanly alone |
| 3 | `bb8d0aab8e` (2026-10-16) s922x: remove 32bit yabadabadoo | `virtual/emulators/package.mk` (1 line) | **to merge**, after row 4 | S922X only (not a fork device) |
| 4 | `8704addb6b` (2026-10-15) yabadabadoo: new Saturn emulator | the `yabadabadoo-lr` recipe and patch; `EMUS_32BIT` and the `saturn` table lines | **to merge**, **adapted**: `yabadabadoo-lr/package.mk:46` copies from `build.${DISTRO}-${DEVICE}.arm`, which must become `${DISTRONAME}` (F-09) | a new core (player-visible: a new Saturn emulator on 32-bit-capable devices, H700 among them) arriving with ROCKNIX's merge; its `Already written:` is nothing (new). A core's save and state format is new, so #10 has nothing to compare |
| 5 | `a1ea79474b` (2026-10-11) rk3566: port to inputplumber | `retroarch/sources/RK3566/retroarch.cfg`: `input_enable_hotkey_btn`, `input_exit_emulator_btn`, `input_hold_fast_forward` to `nul` | **to merge**, only together with the rest of `a1ea79474b` (outside the slice) | RK3566 is a fork-built device: the hotkeys move from RetroArch's binds to InputPlumber, so the RetroArch half alone would leave RK3566 with no exit hotkey. `Already written:` the profile is copied to `/storage/.config/retroarch/retroarch.cfg` once (9fd73da845's note), so devices keep their old binds until the setsettings layer or a profile refresh writes them, which is to be read at the merge (T1's `setsettings.sh` writes hotkeys per launch) |
| 6 | `aca36dbad7` (2026-10-11) mame-lr: don't depend on retroarch | `mame-lr/package.mk` (1 line) | **to merge**, after row 8 | follows `af70bd435b` |
| 7 | `6103571f67` (2026-10-11) the core-updates merge #3470 | `doublecherrygb-lr/patches/001-*`, `flycast2021-lr/patches/02-*`, `np2kai-lr/patches/001-*` added; `emuscv-lr`, `mame-lr`, `same_cdi-lr`, `uae4arm-lr`, `vircon32-lr` recipes | **to merge** | core updates. Each changed core's save and state format is read against #10 by the stream that takes the bump (Q4 (b)'s `behind-upstream` row is `np2kai-lr`, row 14) |
| 8 | `af70bd435b` (2026-10-10) libretro-cores: add retroarch as PKG_DEPENDS_TARGET | 136 recipes, one line each | **to merge**, resolving five conflicts: the rotation-table recipes keep both, `toolchain Python3:host retroarch` (F-09) | a build-order dependency; no runtime change |
| 9 | `eeb33c5a37` (2026-10-05) fix quit hotkey targets for RPCS3, AetherSX2 and mupen64plus | `Start AetherSX2.sh` (`set_kill set "aethersx2"`), `Start RPCS3.sh` (`set_kill set "-9 rpcs3-sa"`) | **to merge** (`Start RPCS3.sh`; the AetherSX2 half goes with row 1) | **a defect on `next`**: the exit hotkey's kill target names a process that is not running for RPCS3 on SM8550 (`rpcs3` against the binary `rpcs3-sa`). Applies cleanly. The exit hotkey is T1's seam (`set_kill`), noted for the coordinator |
| 10 | `c9820d0e89` (2026-10-04) pcsx_rearmed-lr: install the 32-bit core where runemu loads it | `pcsx_rearmed-lr/package.mk` +3 | **to merge, adapted** to `${DISTRONAME}` (F-08, F-09; **#802**, the coordinator's) | the default `psx` core on H700, RK3326, RK3566 and SM8550 is absent where the launcher loads it |
| 11 | `dc781c0c75` (2026-10-04) udev-rules: non-blocking systemctl | `virtual/emulators/udev.d/99-automount.rules` | **to merge** | a hang avoided at card insertion (T1's automount seam) |
| 12 | `096c0d4e96` (2026-10-04) the mmc-resume merge #3304 | the same 3 lines as row 13 | **to merge** (with row 13; already present once row 13 is applied) | merge commit of row 13 |
| 13 | `142df62157` (2026-10-02) mmc: retry a failed SD card resume after a power cycle | `99-automount.rules` +3 | **to merge** | a fix for the card a handheld boots from |
| 14 | `6679670966` (2026-10-01) the gcc-glibc merge #3415 | `np2kai-lr` pin `d1a40352e2` to `5939e0c6d5` with its `PKG_SHA256` | **to merge** | Q4 (b)'s one `behind-upstream` row. A core bump: np2kai's commit range `d1a40352e2..5939e0c6d5` is read for save and state changes by the stream that takes it, citing #10. Not applied here |

**So all 14 are `to merge`, and two need adapting.** None is "not applicable".

- **Adapt rows 4 and 10:** `${DISTRO}` becomes `${DISTRONAME}`.
- **Resolve row 8:** keep both dependency lines in the five rotation-table recipes.
- **Order:** row 5 lands only with its out-of-slice half; rows 3 and 6 follow rows 4 and 8.
- **Row 9's RPCS3 half is a live defect on SM8550**, punch-listed as such.
