# Analysis — M6.P2 T30, the standalone emulators (#677)

Written 2026-10-24 09:10 UTC (`date -u`), stage B, from `02` and `03`; § Second opinion follows Phase 4.6.

## Executive summary

The 35 standalone recipes (543 paths; 55 fork-own) are upstream's architecture, repeated by hand forty times, with the fork's own additions (Dolphin's save paths, DuckStation's screenshot default, the achievements sessions, the GENERIC_X64 repair) written to a higher standard. The defects cluster by **shape** on the launch path:

- **the exit hotkey does nothing** in four emulators (F-01 to F-04), DuckStation's among them, now the VM's default for PSX;
- **a ROM-library file or a name runs as shell** in three (F-07 as root from a `.scummvm` file, F-08's apostrophe, F-19's pad name);
- **the previous RetroAchievements account stays signed in** in five achievements scripts (F-09) on a state the interface creates;
- **a real directory is deleted before it is linked** in nine (F-12), memory cards included;
- **comparisons written as redirections** in five (F-11).

Six of these are fixed upstream after our base and arrive with the base merge (class 1). One currency finding is not code: `portaudio`'s source exists nowhere public (F-13, #849). 30 leads, 1 withdrawn (F-18), 15 guest proofs in two cycles and 5 host proofs. Nothing in the membership was edited.

## Acceptance-criteria scorecard

Criteria 6, 7, 8, 12 and 14 are met at stage B (`02` § Phase 2); 9, 10 and 11 are met by this file's § Renovation face; 2, 3 and 13 at stages C and D; 1, 4, 5, 15 and 16 at F to H.

## Code Quality Assessment

### Strengths

- The fork's own scripts fail closed with a reason a player can read (`dolphin-save-paths`, `cheevos_dolphin.sh`'s `settings_failed`), write by temp and rename, and say in a comment why each line is there.
- `runemu.sh` and `input_sense` (T1's) are sound; the defects are in what each start script hands them.

### Concerns

- One unwritten contract (the kill name) broken four ways; one shape (`rm -rf` then `ln -sf`) copied nine times.
- `eval` and `xargs` over data the player supplies.
- Five achievements scripts that never learned what dolphin's knows.

### Complexity Hotspots

`start_dolphin_gc.sh`/`_wii.sh` (478/442 lines, 282 shared), `start_cemu.sh` (335), `start_steam.sh` (281), `start_vita3k.sh` (255).

## Cornerstone Conformance

`engineering-practices.md` § Guards must fail closed (F-10, F-11), `upgrade-and-install.md` § Migrating data (F-12), `least-surprise.md` (F-01 to F-04), `time-to-play.md` (G11, G12: nothing measured on the path above 0.07 s).

## Spec Fidelity

### Aligned

The brief's counts, the membership, the five pin shapes, and its leads (all six pursued, `02` § The leads).

### Diverged

The install trees' `os-release` path; the 41 start scripts; the table's reach (F-05) widens the brief's GENERIC_X64 picture.

## Missing Artifacts

A standalone exit test in `tools/emulator-exit-test`; free guest content for flycast, Dolphin, Mupen64Plus and touchHLE; shellcheck.

## Risk Assessment

| Risk | Where | Likelihood | Consequence |
| --- | --- | --- | --- |
| The player cannot leave a game with the hotkey | F-01, F-02 (every image), F-03, F-04 | every DuckStation and OpenBOR session | the emulator's own menu is the only exit; least surprise |
| Root shell from a ROM-library file | F-07 | a crafted file in a ROM pack or a shared cloud library | code as root on the handheld |
| Awards sent to the wrong account | F-09 | after an offline account change or a refused sign-in | the previous account earns them |
| A memory card or a PS3 save deleted | F-12 | a real directory where the link belongs (an old archive restored, the file manager) | the player's saves |
| A fresh build fails | F-13 (#849) | any host without this cache | no image |

## Coverage Boundary

Read at `8ebaf8daad`; the guest is the M7 image `069fc27044`, whose start scripts are the hash's (H4). Not covered: the 22 members the GENERIC_X64 image lacks, beyond reading and the image-set; first frames (no real content); the live kill of four emulators that exited on synthetic inputs (flycast, Dolphin, Mupen64Plus, touchHLE; gzdoom and ScummVM were proven with free content, G14, G15); the 80 patches (T42/T43); the data files' contents (provenance only); `libdrastouch.c` beyond a skim.

## Finding Verification (Phase 4.5)

Each lead was re-read at its artifact before grading, and refuted where it could be:

- **F-01** could have been a stale name from an older AppImage layout. Refuted by the pinned bytes (H1) and by the live process (G7). Stands.
- **F-05** could have been the image predating T3's S2. At T3's tip, `core_built` still passes `amiberry` (the device's lists name it), and the `nds` and `saturn` defaults are unguarded. Stands, as T3's file.
- **F-07**: does `runemu.sh` reach `start_scummvm.sh`'s `eval` arm? Yes: the generic arm, then `*)` (G3). Stands.
- **F-09**: does the interface ever leave switch on, token empty? Yes (`GuiRetroAchievementsSettings.cpp:767,780`). Stands.
- **F-11** depends on the cwd. It is `/storage`, writable (G13). Stands.
- **F-12** needs a real directory to occur. Rare: current backups carry no symlink content (`backuptool:813-822`). Stands, graded by trigger.
- **F-18** is refuted by the image's busybox `sed`. Withdrawn.
- **The steam route's "no kill target"** is refuted by `start_steam.sh:262-281`. Not a finding.
- **`amiberry` and `yabasanshiro-sa` absent on GENERIC_X64** are by design (`PKG_ARCH`). Not a finding; their table rows are F-05.
- **The Python helpers' launch cost** measured negligible (G11). Not a finding.

## Renovation face

### Q1 Modernize

The fork's code is current: Python 3 stdlib, `renameat2`, `mktemp` with `umask 077`. The upstream-carried scripts write against busybox without knowing it: `unzip -Zl` (F-06), `grep -i .zip` regexes, and `echo -e` with unquoted arguments. One retired mechanism is still carried: `cheevos_duckstation.sh` ships though `start_duckstation.sh:130` no longer calls it (F-25), and `backuptool:705` still lists DuckStation's settings for blanking, correctly, because DuckStation signs itself in. The `testunofficial` fallback is read by `cheevos_dolphin.sh` and `cheevos_melonds.sh` as the pre-2026-09 spelling; upstream's `f8844ab04e` adds the same to `cheevos_armsx2.sh` (a q4a conflict row). The interface writes `.unofficial`, so the fallback is a compatibility read with no retirement condition (NAMING.md's shape), a Renovation note, not a defect.

### Q2 Standards and best practices

- `tools/pkgcheck`: 47/47 rc 0.
- `bash -n`: 55/55.
- shellcheck: not runnable (recorded).
- `PKG_SHA256` per branch: complete.
- The fork's header is kept on the thirteen changed recipes. Each change carries a comment with its reason.

Standards defects:

- F-10, the unquoted test, in four scripts.
- F-22, the PPSSPP token written with the default umask, twice.
- F-21's `sed` escaping.
- `start_OpenBOR.sh` sources no `/etc/profile`.
- The heroic, dsperate and steam scripts use arrays; most others build strings.

### Q3 Bugs

#### The exit sweep (35 recipes)

The name each start script writes to `/tmp/.process-kill-data` (`set_kill set`), against the executables of that name in the three install trees, and the guest's process for those it carries. *Row* reads `matches`, **differs** (a bug) or `not shipped on any built image`.

| Recipe | Start script(s) | Kill names written | Devices that build it | Executable of that name in the trees | Guest (GENERIC_X64) | Row |
| --- | --- | --- | --- | --- | --- | --- |
| `aethersx2-sa` | start_aethersx2.sh | aethersx2 | SM8550 | aethersx2: SM8550 | not on the guest | matches; class 1 (deleted upstream, F-26) |
| `amiberry` | start_amiberry.sh | amiberry | GENERIC_X64, H700, SM8550 | amiberry: H700,SM8550 | not built for GENERIC_X64; the table's route exits 127 (G2) | matches |
| `ares-sa` | start_ares.sh | ares | SM8550 | ares: SM8550 | not on the guest | matches |
| `armsx2-sa` | start_armsx2.sh | armsx2-qt | SM8550 | armsx2-qt: SM8550 | not on the guest | matches |
| `azahar-sa` | start_azahar.sh | azahar | SM8550 | azahar: SM8550 | not on the guest | matches |
| `bigpemu-sa` | start_bigpemu.sh | bigpemu | SM8550 | bigpemu: SM8550 | not on the guest | matches |
| `cemu-sa` | start_cemu.sh | cemu | SM8550 | cemu: SM8550 | not on the guest | matches |
| `daedalusx64-sa` | start_daedalusx64.sh | daedalus | SM8550 | daedalus: SM8550 | not on the guest | matches |
| `dolphin-sa` | start_dolphin_gc.sh, start_dolphin_wii.sh | ${DOLPHIN_CORE} | GENERIC_X64, SM8550 | ${DOLPHIN_CORE}: runtime/variable | exited on the synthetic input (G1); dolphin-emu-nogui's 17-char name matched by busybox killall (G6, substitute) | matches |
| `drastic-sa` | start_drastic.sh | drastic | H700, SM8550 | drastic: H700,SM8550 | not on the guest | matches |
| `dsperate-sa` | start_dsperate.sh | dsperate | H700, SM8550 | dsperate: H700,SM8550 | not on the guest | matches |
| `duckstation-sa` | Start Duckstation.sh, start_duckstation.sh | AppRun.wrapped | GENERIC_X64, H700, SM8550 | AppRun.wrapped: runtime/variable | comm AppRun, exe duckstation-qt: SURVIVED (G1, G7) | **differs** (F-01) |
| `flycast-sa` | start_flycast.sh | flycast | GENERIC_X64, H700, SM8550 | flycast: GENERIC_X64,H700,SM8550 | exited on the synthetic input before the kill (G1): not tested | matches |
| `gopher64-sa` | start_gopher64.sh | gopher64 | SM8550 | gopher64: SM8550 | not on the guest | matches |
| `gzdoom-sa` | start_gzdoom.sh | gzdoom | GENERIC_X64, H700, SM8550 | gzdoom: GENERIC_X64,H700,SM8550 | comm gzdoom: ended by its kill (G14, Freedoom) | matches |
| `hatarisa` | start_hatari.sh | **none** | GENERIC_X64, H700, SM8550 | - | the route's script absent: exit 127 (G2) | **differs**: no target, and the route's script is absent (F-04) |
| `heroic` | start_heroic_authenticate.sh, start_heroic_play.sh, start_heroic_play_gamescope.sh | Heroic heroic | SM8550 | Heroic: runtime/variable; heroic: runtime/variable | not on the guest | matches (runtime binaries: the player's or downloaded) |
| `hypseus-singe` | start_hypseus.sh | hypseus | GENERIC_X64, H700, SM8550 | hypseus: GENERIC_X64,H700,SM8550 | not run (no laserdisc content) | matches |
| `mednafen` | start_mednafen.sh | mednafen | H700, SM8550 | mednafen: H700,SM8550 | not on the guest | matches |
| `melonds-sa` | start_melonds.sh | melonDS | SM8550 | melonDS: SM8550 | not on the guest | matches |
| `mupen64plus-sa` | start_mupen64plus.sh | mupen64plus | GENERIC_X64, H700, SM8550 | mupen64plus: GENERIC_X64,H700,SM8550 | simple: the substitute SURVIVED (G6); the binary exited on its input | **differs** for the simple core (F-03) |
| `nanoboyadvance-sa` | start_nanoboyadvance.sh | NanoBoyAdvance | SM8550 | NanoBoyAdvance: SM8550 | not on the guest | matches |
| `openbor` | start_OpenBOR.sh | **none** | GENERIC_X64, H700, SM8550 | - | no kill data: SURVIVED (G1) | **differs**: no target (F-02) |
| `pico-8` | start_pico8.sh | ${STATIC_BIN} start_pico8.sh | GENERIC_X64, H700, SM8550 | ${STATIC_BIN}: runtime/variable; start_pico8.sh: GENERIC_X64,H700,SM8550 | not run (the player's binary) | matches (runtime binaries: the player's or downloaded) |
| `ppsspp-sa` | start_ppsspp.sh | ppsspp | GENERIC_X64, H700, SM8550 | ppsspp: GENERIC_X64,H700,SM8550 | comm ppsspp: ended (G1) | matches |
| `rpcs3-sa` | start_rpcs3.sh | rpcs3-sa | SM8550 | rpcs3-sa: SM8550 | not on the guest | matches |
| `scummvm-sa` | start_scummvm.sh | scummvm | GENERIC_X64, H700, SM8550 | scummvm: GENERIC_X64,H700,SM8550 | comm scummvm: ended by its kill (G15, FOTAQ) | matches |
| `skyemu-sa` | start_skyemu.sh | SkyEmu | SM8550 | SkyEmu: SM8550 | not on the guest | matches |
| `steam` | start_steam.sh, start_steam_arm64.sh, start_steam_x86.sh | FEX gamescope steam | SM8550 | FEX: SM8550; gamescope: SM8550; steam: SM8550 | not on the guest | matches (runtime binaries: the player's or downloaded) |
| `supermodel-sa` | start_supermodel.sh | supermodel | SM8550 | supermodel: SM8550 | not on the guest | matches |
| `touchhle-sa` | start_touchhle.sh | touchHLE | GENERIC_X64, H700, SM8550 | touchHLE: GENERIC_X64,H700,SM8550 | exited on the synthetic input (G1): not tested | matches |
| `vice-sa` | start_vice.sh | @EMU@ | GENERIC_X64, H700, SM8550 | @EMU@: runtime/variable | comm x64sc: ended (G1) | matches |
| `vita3k-sa` | start_vita3k.sh | vita3k-sa | SM8550 | vita3k-sa: SM8550 | not on the guest | matches |
| `xemu-sa` | start_xemu.sh | xemu | SM8550 | xemu: SM8550 | not on the guest | matches |
| `yabasanshiro-sa` | start_yabasanshiro.sh | yabasanshiro | GENERIC_X64, H700, SM8550 | yabasanshiro: H700,SM8550 | not built for GENERIC_X64; the default saturn route exits 127 (G2) | matches |

35 rows.


Every written name resolves to an executable in each tree that builds the recipe, or is a run-time name (the AppImage's, the player's binary, Steam's and Heroic's own), except DuckStation's, which names no process at all (H1, G7). Three of the four **differs** rows are fixed upstream after the base (`4a6415c033`, `eeb33c5a37`, `2e7041d273`); OpenBOR's is not.

#### The shell-line sweep (#825's class): every start and achievements script

| Script | Built from | Verdict |
| --- | --- | --- |
| `aethersx2-sa/cheevos_aethersx2.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `aethersx2-sa/start_aethersx2.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `amiberry/start_amiberry.sh` | the ROM path | floppy names into the temp config through echo -e ${ARGS} unquoted; the zip test unquoted (F-06); a pad name into sed's replacement |
| `ares-sa/start_ares.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `armsx2-sa/cheevos_armsx2.sh` | the sign-in settings | the token passed to awk through ENVIRON (no interpolation); the username into sed's replacement |
| `armsx2-sa/start_armsx2.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `azahar-sa/start_azahar.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `bigpemu-sa/start_bigpemu.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `cemu-sa/start_cemu.sh` | the ROM path | "$@" passed whole (the platform argument too); controller names through xmlstarlet -v (no shell) |
| `daedalusx64-sa/start_daedalusx64.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `dolphin-sa/cheevos_dolphin.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `dolphin-sa/start_dolphin_gc.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `dolphin-sa/start_dolphin_wii.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `drastic-sa/start_drastic.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `dsperate-sa/start_dsperate.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `duckstation-sa/cheevos_duckstation.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `duckstation-sa/start_duckstation.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `duckstation-sa/Start Duckstation.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `flycast-sa/cheevos_flycast.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `flycast-sa/start_flycast.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `gopher64-sa/start_gopher64.sh` | the ROM path | the ROM quoted; the RetroAchievements password on argv, unquoted (F-20) |
| `gzdoom-sa/start_gzdoom.sh` | the ROM path | **unsafe**: the WAD path through echo and xargs, split and quote-parsed (F-08; G4) |
| `hatarisa/start_hatari.sh` | the ROM path | the floppy names through echo -e ${ARGS} unquoted (spaces collapse, globs expand); the zip test unquoted (F-06) |
| `heroic/start_heroic_authenticate.sh` | the ROM path | arguments as an array |
| `heroic/start_heroic_play.sh` | the ROM path | arguments as an array |
| `heroic/start_heroic_play_gamescope.sh` | the ROM path | the compositor's numeric geometry through eval (:33); arguments as an array |
| `hypseus-singe/start_hypseus.sh` | the ROM path | the .commands file word-split into $params without eval (globs expand; no command) |
| `mednafen/start_mednafen.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `melonds-sa/cheevos_melonds.sh` | the sign-in settings | credentials into an INI through sed with an incomplete escape (F-21); no command built |
| `melonds-sa/start_melonds.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `mupen64plus-sa/start_mupen64plus.sh` | the ROM path | the ROM quoted to the emulator; the zip test reads $1 unquoted through echo and grep (F-06); unzip's name list reaches the path (F-06) |
| `nanoboyadvance-sa/start_nanoboyadvance.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `openbor/start_OpenBOR.sh` | the ROM path | the pak quoted |
| `pico-8/start_pico8.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `ppsspp-sa/cheevos_ppsspp.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `ppsspp-sa/start_ppsspp.sh` | the ROM path | the ROM quoted, backslashes stripped (:105) |
| `rpcs3-sa/start_rpcs3.sh` | the ROM path | the .psn/.m3u first line into a quoted path |
| `scummvm-sa/start_scummvm.sh` | the ROM path | **unsafe**: the .scummvm file's content through eval, as root (F-07; G3) |
| `skyemu-sa/cheevos_skyemu.sh` | the sign-in settings | values into the emulator's config by heredoc or sed; no command built from a value |
| `skyemu-sa/start_skyemu.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `steam/start_steam.sh` | the ROM path | the compositor's numeric geometry through eval (:81); the game URI quoted |
| `steam/start_steam_arm64.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `steam/start_steam_x86.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `supermodel-sa/start_supermodel.sh` | the ROM path | the ROM quoted; the options as one argument (F-16) |
| `touchhle-sa/start_touchhle.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `vice-sa/start_vice.sh` | the ROM path | the ROM quoted, backslashes stripped (:15) |
| `vita3k-sa/start_vita3k.sh` | the ROM path | the zRIF from "$(cat ...)" quoted; .psvita content quoted |
| `xemu-sa/start_xemu.sh` | the ROM path | the ROM quoted to the emulator; GAME and PLATFORM used only as get_setting keys |
| `yabasanshiro-sa/start_yabasanshiro.sh` | the ROM path | **unsafe** (Low): a pad's self-reported name through eval (F-19); the ROM quoted |

49 scripts: three **unsafe** (F-07, F-08, F-19), the rest quoted or word-split without a shell.

#### The defects (each a `bug` at stage D unless noted)

F-01 to F-04 (the exit), F-05 (T3's file: the coordinator routes it), F-06, F-07, F-08, F-09 with F-10, F-11, F-12, F-13 (filed as #849 by the coordinator; a Medium row, no tree change), F-14, F-15, F-16 (class 1), F-17, F-19, F-20, F-21, F-29, F-30. F-22 is a standards item; F-24 and F-25 Renovation; F-26 to F-28 currency.

### Q4 Package currency

#### Q4 (a) behind-upstream: the fork against ROCKNIX

The thirteen fork-own recipes' pins equal upstream's (`q4a-dispositions.md` § The thirteen). What the fork changed in each is a dependency, an architecture guard or a comment, never the pin. Upstream's 38 commits on the membership since the base:

| Commit | Kind | Files | Overlap with fork changes | Subject | Disposition |
| --- | --- | ---: | --- | --- | --- |
| `0c43a50420` | commit | 20 | `dolphin-sa/scripts/start_dolphin_gc.sh`, `dolphin-sa/scripts/start_dolphin_wii.sh`, `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3377 from sunshineinabox/PR_RotScaling | conflicts: rotation/scaling across the two Dolphin scripts, DuckStation's and Mupen64Plus's, all fork-changed (save paths, #521, the repair block); carries supermodel's array fix (`b6fcd2ca4f`'s base). Resolve hunk by hunk at the base merge. |
| `6679670966` | commit | 2 | `dolphin-sa/package.mk` | Merge pull request #3415 from sunshineinabox/WIP_gcc-glibc | conflicts: read at the base merge |
| `ca67c5f1dd` | commit | 1 | none | dolphin-sa: read wayland events in the nogui loop | to merge (no overlap) |
| `c92afac014` | commit | 1 | none | systemd: restore 255 parity for 261 | to merge (no overlap) |
| `bb9e42e2a0` | commit | 1 | none | rocknix: run games in games.slice with oomd and freeze on suspend | to merge (no overlap) |
| `b6fcd2ca4f` | commit | 1 | none | supermodel-sa: use the screen size for full resolution | to merge (no overlap) |
| `74c46ddbb9` | merge | 2 | none | Merge pull request #3435 from sunshineinabox/WIP_SystemD261 | merge: its content is its parents' rows |
| `32ebcdbf1b` | commit | 1 | none | rocknix: keep Steam alive when one of its processes is OOM-killed | to merge (no overlap) |
| `4a6415c033` | commit | 2 | `duckstation-sa/scripts/start_duckstation.sh` | duckstation-sa: point the quit hotkey at duckstation-qt | to merge, class 1: DuckStation's kill target `duckstation-qt` (this slice's exit sweep, confirmed by the AppImages' listing). The overlap is the fork's `duckstation_screenshot_path` call (#521), a different hunk: merges. |
| `eeb33c5a37` | commit | 1 | `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | emulators: fix quit hotkey targets for RPCS3, AetherSX2 and mupen64plus | to merge, class 1: the kill targets (`mupen64plus-simple`; `Start RPCS3.sh` and `Start AetherSX2.sh` are T3's files, T3's PL-010). The overlap is the fork's GENERIC_X64 repair block (47-67), a different hunk: merges. |
| `2e7041d273` | commit | 3 | none | hatarisa: rename the start script to match the core name | to merge, class 1: `start_hatari.sh` -> `start_hatarisa.sh` and its kill target; the table's `hatarisa` route needs it. |
| `48b98a02d7` | commit | 5 | none | sm6115: initial Retroid Pocket Duo Lite support | to merge (no overlap) |
| `f610969ba1` | commit | 18 | none | dsperate-sa: bump to v3.0.1, refresh configs + es opts | to merge (no overlap) |
| `bc4db4f0e7` | commit | 1 | none | dsperate-sa: bump to v3.0.2 | to merge (no overlap) |
| `f8844ab04e` | commit | 1 | `armsx2-sa/scripts/cheevos_armsx2.sh` | armsx2-sa: read the testunofficial key like the other launchers | conflicts: upstream adds the `testunofficial` fallback to `cheevos_armsx2.sh`, whose token block the fork rewrote (#170, #308); keep the fork's block and take the one line. |
| `d74fde77e0` | commit | 1 | none | flycast-sa: read the auto frame skipping key ES writes | to merge (no overlap) |
| `2d34256719` | merge | 30 | `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3464 from sunshineinabox/PR_QuitHotkey | to merge: overlap in a different hunk; read at the base merge |
| `195a8eba4b` | commit | 3 | `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | mupen64plus-sa: fix zipped ROMs and DualSense controls | to merge, class 1: `unzip -Zl` -> `unzip -qql` (zipped N64 ROMs under busybox). Overlap: the fork's repair block, a different hunk. |
| `99870f0449` | commit | 8 | none | azahar-sa: async_shader_compilation feature | to merge (no overlap) |
| `5675ab7b28` | commit | 8 | none | azahar-sa: bump to v2126.2 | to merge (no overlap) |
| `e0bf3a55b0` | commit | 1 | none | azahar-sa: SM4450: symlink to InputPlumber config | to merge (no overlap) |
| `115a89be2b` | merge | 18 | `armsx2-sa/scripts/cheevos_armsx2.sh`, `duckstation-sa/scripts/start_duckstation.sh`, `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | Merge pull request #3468 from qzydustin/setting-keys | to merge: overlap in a different hunk; read at the base merge |
| `7af4b5bcf3` | merge | 11 | `armsx2-sa/scripts/cheevos_armsx2.sh` | Merge pull request #3478 from porschemad911/azahar-v2126.2 | to merge: overlap in a different hunk; read at the base merge |
| `6103571f67` | commit | 1 | none | Merge pull request #3470 from sunshineinabox/WIP_core-updates | to merge (no overlap) |
| `a1ea79474b` | commit | 20 | `duckstation-sa/config/RK3566`, `duckstation-sa/config/RK3566/settings.ini` | rk3566: port to inputplumber | conflicts: RK3566's InputPlumber port touches `duckstation-sa/config/RK3566/settings.ini`, a fork-own file (#521's screenshot key). RK3566 is not a shipped device (D-WORKFLOW-185): take upstream's and re-apply the one key. |
| `2e85dcde25` | commit | 1 | none | melonds-sa: fix broken launch script (libmali) | to merge (no overlap) |
| `8c8800dc01` | commit | 1 | none | sm4450: add Retroid Pocket Classic 6 Rev Q | to merge (no overlap) |
| `ac844389f4` | commit | 1 | none | dsperate-sa: bump to v3.0.4 | to merge (no overlap) |
| `693632077e` | merge | 2 | none | Merge pull request #3498 from Jacob-Matthew-Cook/sm4450-rpclassic-sgb | merge: its content is its parents' rows |
| `075a7c303b` | commit | 2 | `dolphin-sa/package.mk` | Merge pull request #3513 from sunshineinabox/WIP_multimedia | conflicts: read at the base merge |
| `38cc9c7e7d` | commit | 3 | none | rk3566: fix some inputplumber issues | to merge (no overlap) |
| `c4d353449e` | commit | 17 | `aethersx2-sa/package.mk` | aethersx2: drop package due to licensing concern | to merge, class 1: deletes `aethersx2-sa` (licensing). The fork's 4 commits on the recipe (`PKG_ARCH`) go with it; `Already written:` in `04` § Q6. |
| `09ce29c548` | merge | 20 | `aethersx2-sa/package.mk` | Merge pull request #3534 from sunshineinabox/PR_ASX2 | merge of `c4d353449e`'s branch: as `c4d353449e`. |
| `abcb61ec9b` | commit | 1 | none | armsx2-sa: add patch to fix Vulkan backend on mali | to merge (no overlap) |
| `d91679afb8` | commit | 1 | none | dsperate-sa: bump to v3.0.5 | to merge (no overlap) |
| `62da3f7e23` | commit | 1 | none | dsperate-sa: S922X: use 'renderer' sink | to merge (no overlap) |
| `861c9ce4ea` | commit | 3 | none | ppsspp: change menu button combo | to merge (no overlap) |
| `3df05945a7` | commit | 5 | none | ppsspp-sa: remove the guide and misc swap patch | to merge (no overlap) |


38 rows: 33 to merge, 5 conflicts, 0 superseded. Every row is taken by the base merge (the coordinator's); this branch cherry-picks none.

#### Q4 (b) behind-project: the 47 pins against their projects, by shape

| Recipe | Shape | Pin | Against its project | q4-pins class | Disposition |
| --- | --- | --- | --- | --- | --- |
| `aethersx2-sa` | moving tarball | `1.5-3606` | matches PKG_SHA256 today | pin-not-on-project | deferred: base merge, class 1 (F-26) |
| `amiberry` | hash | `5c54536997c0` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `ares-sa` | hash | `0aafd8578921` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `armsx2-sa` | hash | `19c83bf065ed` | behind-project; default branch head 2026-10-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `azahar-sa` | hash (tag 2126.0) | `fbd3fb02f71e` | behind-upstream: ROCKNIX pins 219d743a1e (v2126.2) | behind-upstream | to merge with the base (q4a), class 1 |
| `bigpemu-sa` | release asset | `v119` | v119 against v1221 on the download page | by-hand | bump proposed (F-27) |
| `cemu-sa` | hash | `6f6c1299e29f` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `daedalusx64-sa` | hash | `f17e9ed86f38` | behind-project; default branch head 2026-10-10 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `dolphin-sa` | hash | `6094cfcf7b8f` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `drastic-sa` | moving tarball | `1.0` | matches PKG_SHA256 today | pin-not-on-project | kept: the checksum is the pin; #844's check is the guard |
| `dsperate-sa` | release asset | `2.0.1` | 2.0.1 against v3.0.5; ROCKNIX already at 3.0.5 | pin-not-on-project | to merge with the base (q4a), class 1 |
| `duckstation-sa` | release asset | `0.1-10998` | v0.1-10998 against v0.1-11894 (latest 2026-10-13) | pin-not-on-project | bump proposed (F-27), F-01's target re-checked with it |
| `flycast-sa` | hash | `5aa091fde632` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `gopher64-sa` | hash | `ca4a20f52403` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `gzdoom-sa` | tag | `g4.14.2` | g4.14.2 = the latest release (2025-05-03) | pin-not-on-project | current |
| `zmusic` | tag | `1.1.14` | 1.1.14 | behind-project | informational (upstream-carried) |
| `hatarisa` | hash | `6da06056d89b` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `portaudio` | hash | `64d1bf913433` | repository 404; the commit is not in PortAudio/portaudio | repo-missing | deferred: #849 (F-13); the hosting choice via #346 |
| `heroic` | no project | `1.0` | metapackage; Heroic is installed by the player | by-hand | n/a |
| `hypseus-singe` | hash | `b353e1728bf5` | behind-project; default branch head 2026-08-30 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mednafen` | tag (a fork's) | `1.32.1` | 1.32.1-chd, the fork's only tag | pin-not-on-project | current |
| `melonds-sa` | hash | `906e9ebb27da` | behind-project; default branch head 2026-10-21 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-audio-sdl` | hash | `cec70e42b453` | behind-project; default branch head 2026-10-20 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-core` | hash | `5340dafcc0f5` | behind-project; default branch head 2026-10-20 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-input-sdl` | hash | `3698a2b12b1d` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-rsp-cxd4` | hash | `f6ff3719cb68` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-rsp-hle` | hash | `9d13986f764b` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-simplecore` | hash | `5340dafcc0f5` | behind-project; default branch head 2024-11-03 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-ui-console` | hash | `1340c4bdfc9e` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-video-glide64mk2` | hash | `992b5942078f` | behind-project; default branch head 2026-06-23 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-video-gliden64` | hash | `85bdd452d709` | behind-project; default branch head 2026-10-11 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa-video-rice` | hash | `470865c6c64b` | behind-project; default branch head 2026-09-15 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `mupen64plus-sa` | no project | `1.0` | metapackage over its ten sub-recipes | by-hand | n/a |
| `nanoboyadvance-sa` | hash | `3bb6f478f977` | behind-project; default branch head 2026-06-21 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `openbor` | hash | `b8303cce992a` | behind-project; default branch head 2026-10-18 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `pico-8` | no project | `95cb4d4f28e1` | the player's own binary | by-hand | n/a |
| `ppsspp-sa` | hash | `afbc66a318b8` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `rpcs3-sa` | hash | `2f4034590f26` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `scummvm-sa` | tag | `2026.1.0` | 2026.1.0 against v2026.4.0 (2026-10-11) | pin-not-on-project | bump proposed (F-27) |
| `skyemu-sa` | hash | `46efbcbdb3b9` | behind-project; default branch head 2026-10-13 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `steam` | release .deb | `1.0.0.85` | 1.0.0.85 against 1.0.0.87 in the pool (not the recipe's stable path: approximate) | by-hand | informational; Steam updates itself |
| `supermodel-sa` | hash | `b13fdd5029a2` | the pin is on no default branch | pin-not-on-project | F-28: the pin's branch named in the recipe |
| `touchhle-sa` | hash | `3c5850585ba5` | behind-project; default branch head 2026-10-13 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `vice-sa` | tag | `3.8` | 3.8 against 3.10 (SourceForge) | by-hand | bump proposed (F-27) |
| `vita3k-sa` | hash | `ba5c2029c96a` | behind-project; default branch head 2026-10-24 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `xemu-sa` | hash | `cbffb57d084c` | behind-project; default branch head 2026-10-22 | behind-project | informational (upstream-carried; ROCKNIX's to take) |
| `yabasanshiro-sa` | hash | `a40dace1ae0a` | the pin is on no default branch (master pushed 2024-12-28) | pin-not-on-project | F-28 |

47 rows: hash 33, tag 5, release 4, moving tarball 2, no project 3. No empty cell.

### Q5 Efficiency

- **Time to play, standalone.** `runemu.sh` start to the emulator's process (G12, n=3 each, synthetic inputs): ppsspp 0.61/0.63/0.63 s, x64sc 0.62/0.67/0.56 s, DuckStation 0.62/0.53/0.52 s. **With real free content (G14, G15, n=3):** gzdoom, from the launch call to Freedoom's title, 3.13 / 1.03 / 1.11 s (the first run cold); ScummVM, to its own splash, 0.64-1.08 s. These start at `runemu.sh`, not at the interface's press, because an SSH launch skips the interface's own launch path. A launch driven from the interface is the measurement still owed. T3's RetroArch numbers on the same image are interface to first frame 0.62 s and game to game 1.01 s; T1's are in its retro. A first frame needs real content, which is the second guest cycle's job.
- **Before `exec`:**
  - Dolphin runs two Python helpers (0.03-0.05 s each) and some forty `sed -i` passes.
  - DuckStation runs one helper (0.04-0.07 s) and five `sed` passes.
  - gzdoom hashes its 3 MB pk3 twice (0.02 s each).
  - Mupen64Plus copies the whole ROM into tmpfs (F-29: up to 64 MB of RAM, plus the copy's time).
  - DaedalusX64 copies its binary on every launch (F-11's `<>`).
  - amiberry copies its configs on every launch (F-15).
  - Measured: none above 0.07 s on the VM. Mupen64Plus's copy grows with the ROM and was not measured with a real one.
- **Configs:** read once at launch; not measured.

### Q6 Dead ends

#### Q6: the reachability table (35 recipes)

| Recipe | Devices that build it | Start scripts | Per-device config directories | Of those, for a device not shipped | On the guest |
| --- | --- | --- | ---: | ---: | --- |
| `aethersx2-sa` | SM8550 | start_aethersx2.sh | 12 | 10 (RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `amiberry` | GENERIC_X64, H700, SM8550 | start_amiberry.sh | 0 | 0 (-) | no: not built for GENERIC_X64 (PKG_ARCH) |
| `ares-sa` | SM8550 | start_ares.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `armsx2-sa` | SM8550 | start_armsx2.sh | 1 | 1 (S922X) | no: not in GENERIC_X64's arms |
| `azahar-sa` | SM8550 | start_azahar.sh | 12 | 10 (AMD64, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `bigpemu-sa` | SM8550 | start_bigpemu.sh | 1 | 1 (S922X) | no: not in GENERIC_X64's arms |
| `cemu-sa` | SM8550 | start_cemu.sh | 7 | 5 (AMD64, SM4450, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `daedalusx64-sa` | SM8550 | start_daedalusx64.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `dolphin-sa` | GENERIC_X64, SM8550 | start_dolphin_gc.sh, start_dolphin_wii.sh | 13 | 11 (AMD64, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `drastic-sa` | H700, SM8550 | start_drastic.sh | 12 | 9 (RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250) | no: not in GENERIC_X64's arms |
| `dsperate-sa` | H700, SM8550 | start_dsperate.sh | 6 | 5 (RK3326, RK3399, RK3566, RK3588, S922X) | no: not in GENERIC_X64's arms |
| `duckstation-sa` | GENERIC_X64, H700, SM8550 | Start Duckstation.sh, start_duckstation.sh | 15 | 12 (AMD64, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `flycast-sa` | GENERIC_X64, H700, SM8550 | start_flycast.sh | 15 | 12 (AMD64, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `gopher64-sa` | SM8550 | start_gopher64.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `gzdoom-sa` | GENERIC_X64, H700, SM8550 | start_gzdoom.sh | 0 | 0 (-) | yes |
| `hatarisa` | GENERIC_X64, H700, SM8550 | start_hatari.sh | 0 | 0 (-) | yes |
| `heroic` | SM8550 | start_heroic_authenticate.sh, start_heroic_play.sh, start_heroic_play_gamescope.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `hypseus-singe` | GENERIC_X64, H700, SM8550 | start_hypseus.sh | 0 | 0 (-) | yes |
| `mednafen` | H700, SM8550 | start_mednafen.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `melonds-sa` | SM8550 | start_melonds.sh | 13 | 11 (AMD64, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `mupen64plus-sa` | GENERIC_X64, H700, SM8550 | start_mupen64plus.sh | 15 | 12 (AMD64, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `nanoboyadvance-sa` | SM8550 | start_nanoboyadvance.sh | 10 | 8 (AMD64, RK3326, RK3399, RK3588, SM4450, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `openbor` | GENERIC_X64, H700, SM8550 | start_OpenBOR.sh | 0 | 0 (-) | yes |
| `pico-8` | GENERIC_X64, H700, SM8550 | start_pico8.sh | 0 | 0 (-) | yes |
| `ppsspp-sa` | GENERIC_X64, H700, SM8550 | start_ppsspp.sh | 15 | 13 (AMD64, PSP, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750) | yes |
| `rpcs3-sa` | SM8550 | start_rpcs3.sh | 5 | 3 (SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `scummvm-sa` | GENERIC_X64, H700, SM8550 | start_scummvm.sh | 0 | 0 (-) | yes |
| `skyemu-sa` | SM8550 | start_skyemu.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `steam` | SM8550 | start_steam.sh, start_steam_arm64.sh, start_steam_x86.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `supermodel-sa` | SM8550 | start_supermodel.sh | 8 | 6 (RK3588, SM4450, SM6115, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `touchhle-sa` | GENERIC_X64, H700, SM8550 | start_touchhle.sh | 0 | 0 (-) | yes |
| `vice-sa` | GENERIC_X64, H700, SM8550 | start_vice.sh | 0 | 0 (-) | yes |
| `vita3k-sa` | SM8550 | start_vita3k.sh | 0 | 0 (-) | no: not in GENERIC_X64's arms |
| `xemu-sa` | SM8550 | start_xemu.sh | 7 | 5 (AMD64, SM4450, SM8250, SM8650, SM8750) | no: not in GENERIC_X64's arms |
| `yabasanshiro-sa` | GENERIC_X64, H700, SM8550 | start_yabasanshiro.sh | 0 | 0 (-) | no: not built for GENERIC_X64 (PKG_ARCH) |

Per-file rows where a file's reach differs from its recipe's are the coverage table's Q6 cells (`per-device file for <DEVICE>, a device the fork does not ship`). They are T25's unshipped table, named and not removed (plan § 5). Other dead ends:

- `psp_save_mover.sh` has no caller (F-25).
- `cheevos_duckstation.sh` is not called (F-25).
- Six achievements scripts read the password and never use it (F-25).
- `start_steam_x86.sh` is reached only through `start_steam.sh`'s `steam_version` setting.
- **`aethersx2-sa`:** every row is `deferred: base merge, class 1` (F-26). **Already written:** on SM8550, `/storage/.config/aethersx2/` (configs, and `inis/PCSX2.ini`'s `Token =`, which `backuptool:708` already blanks), `/storage/roms/bios/aethersx2/` (the player's BIOS) and the PS2 save states under `/storage/roms/savestates/ps2`, which ARMSX2 shares. After the deletion nothing launches AetherSX2, and nothing removes those files. The player's data stays where it was, and ARMSX2 (the remaining PS2 emulator) reads the same save-state folder. Nothing is to be migrated; the token in `PCSX2.ini` stays at rest, as for any emulator the player stops using.

### Q7 Clarity and structure

- **The Dolphin pair:** `start_dolphin_gc.sh` and `_wii.sh` share 282 of their unique lines; 128 lines differ. A shared library would hold the common part (F-24).
- **The eight achievements scripts:** one shape, three generations. `cheevos_dolphin.sh`'s publish-whole-file is the model the other seven should share (F-09, F-25).
- **The forty start scripts:** the five steps (seed, link, settings, kill target, run) are written by hand each time. Two helpers would remove F-12 and F-01's class: `link_storage_dir` and a kill target derived from the binary run.
- **DuckStation's nine per-device `settings.ini`** (200-323 lines) are per-device seeds; the fork changed one key in each (#521).
- **Comments against code:** `start_touchhle.sh:71` echoes a variable it never sets (F-25); `start_daedalusx64.sh:44`'s "Always grab the latest daedalus bin" is literally true, every launch, because of F-11.

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- *A kill target names a process the image runs* is a contract in no rule and no test. `tools/emulator-exit-test` drives RetroArch only. The ladder's tool (`05`): every name a start script writes resolves to an executable the image carries, or is a declared run-time name.
- shellcheck's absence leaves SC2071 and SC2086 to readers (F-10, F-11).

### Codification Gaps (needs-new-rule)

- `upgrade-and-install.md`'s "copy, verify, then delete" is written for cloud migrations. A local link step is the same act, and F-12 shows nine scripts that skip it. The rule could say so; the coordinator's call.

### Recommended Action Sequence

Proposals for the coordinator: the exit fixes first (F-01 to F-04, three of them class 1), then F-07 and F-09 (security, accounts), then F-12 and F-11, then the rest.

## Second opinion (Phase 4.6)

**Pending:** the two seats (GPT-6 Astra `max`, Gemini 4 Argon `high`) run next, probes first. This section is filled from their outputs and graded item by item.

## Quality Self-Check

- **Every verdict names its artifact:** a line at the hash, a proof (G1-G13, H1-H5), or a command's output in `00`.
- **Every substitute input is named** (blindspot 65): G1-G12's inputs are synthetic and G6's binaries are renamed copies. No verdict about a real game is drawn from them.
- **What was not checked is said:**
  - four live kills (flycast, Dolphin, Mupen64Plus, touchHLE);
  - first frames;
  - the 22 members the guest lacks, beyond reading;
  - `libdrastouch.c`, skimmed only;
  - the Steam launcher's version, read from the pool listing, not the recipe's path.
- **No value from an achievements log or config was printed;** G9 counted synthetic strings.
- **Times are from the clock or from artifacts' mtimes.** Two typed times were corrected (`00`; the friction line of 08:46).

