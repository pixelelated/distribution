# Analysis — M6.P2 T30, the standalone emulators (#677)

Written 2026-10-24 09:10 UTC (`date -u`), stage B, from `02` and `03`; § Second opinion follows Phase 4.6.

## Executive summary

The 35 standalone recipes (543 paths; 55 fork-own) are upstream's architecture, repeated by hand forty times, with the fork's own additions (Dolphin's save paths, DuckStation's screenshot default, the achievements sessions, the GENERIC_X64 repair) written to a higher standard. The defects cluster by **shape** on the launch path:

- **the exit hotkey does nothing** in four emulators (F-01 to F-04), DuckStation's among them, now the VM's default for PSX;
- **a ROM-library file or a device's name runs as shell** in two (F-07 as root from a `.scummvm` file; F-19's pad name), and a ROM's name stops a launch in a third (F-08's apostrophe, through `xargs`: not code);
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
| The player cannot leave a game with the hotkey | F-01, F-02 (every image), F-03, F-04 | every DuckStation and OpenBOR session | the global exit does nothing; least surprise |
| Root shell from a ROM-library file | F-07 | a crafted file in a ROM pack or a shared cloud library | code as root on the handheld |
| Awards sent to the wrong account | F-09 | after an offline account change or a refused sign-in | the previous account earns them |
| A save state, a memory card or a PS3 save deleted | F-12 | a real directory where the link belongs: DuckStation from the Tools launcher, then a game (G16); an old archive restored; the file manager | the player's saves |
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
- **F-12** needs a real directory to occur. Not rare: the Tools launcher's DuckStation creates one (G16, after Gemini's G-03); current backups carry no symlink content (`backuptool:813-822`). Re-graded High in § Second opinion.
- **F-18** is refuted by the image's busybox `sed`. Withdrawn.
- **The steam route's "no kill target"** is refuted by `start_steam.sh:262-281`. Not a finding.
- **`amiberry` and `yabasanshiro-sa` absent on GENERIC_X64** are by design (`PKG_ARCH`). Not a finding; their table rows are F-05.
- **The Python helpers' launch cost** measured negligible (G11). Not a finding.

## Renovation face

### Q1 Modernize

The fork's code is current: Python 3 stdlib, `renameat2`, `mktemp` with `umask 077`. The upstream-carried scripts write against busybox without knowing it: `unzip -Zl` (F-06), `grep -i .zip` regexes, and `echo -e` with unquoted arguments. One retired mechanism is still carried: `cheevos_duckstation.sh` ships though `start_duckstation.sh:130` no longer calls it (F-25), and `backuptool:705` still lists DuckStation's settings for blanking. DuckStation's own sign-in is switched off at every launch by `start_duckstation.sh:131` (F-38; corrected in Phase 4.6). The `testunofficial` fallback is read by `cheevos_dolphin.sh` and `cheevos_melonds.sh` as the pre-2026-09 spelling; upstream's `f8844ab04e` adds the same to `cheevos_armsx2.sh` (a q4a conflict row). The interface writes `.unofficial`, so the fallback is a compatibility read with no retirement condition (NAMING.md's shape), a Renovation note, not a defect.

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
| `amiberry` | start_amiberry.sh | amiberry | H700, SM8550 (GENERIC_X64 lists it, PKG_ARCH drops it) | amiberry: H700,SM8550 | not built for GENERIC_X64; the table's route exits 127 (G2) | matches |
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
| `yabasanshiro-sa` | start_yabasanshiro.sh | yabasanshiro | H700, SM8550 (GENERIC_X64 lists it, PKG_ARCH drops it) | yabasanshiro: H700,SM8550 | not built for GENERIC_X64; the default saturn route exits 127 (G2) | matches |

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
  - Measured: Dolphin's `check` phase, DuckStation's helper and one pk3 hash, each 0.02-0.07 s. Not measured: Dolphin's `prepare` phase, the `sed` passes, and Mupen64Plus's copy with a real ROM (narrowed in Phase 4.6).
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
- **`aethersx2-sa`:** every row is `deferred: base merge, class 1` (F-26). **Already written:** on SM8550, `/storage/.config/aethersx2/` (configs, and `inis/PCSX2.ini`'s `Token =`, which `backuptool:708` already blanks), `/storage/roms/bios/aethersx2/` (the player's BIOS) and the PS2 save states under `/storage/roms/savestates/ps2`, which ARMSX2 shares. After the deletion nothing launches AetherSX2, and nothing removes those files. The player's data stays where it was, and ARMSX2 (the remaining PS2 emulator) reads the same save-state folder. Nothing is removed by the deletion; whether ARMSX2 reads AetherSX2's save states is not shown (narrowed in Phase 4.6). The token in `PCSX2.ini` stays at rest, as for any emulator the player stops using.

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

Graded 2026-10-24 10:24 UTC (`date -u`), after both seats returned. **Depth: Extended** (D-WORKFLOW-184): `gpt` (`openai/gpt-6-astra`, max, provider OpenAI) and `gemini-argon` (`google/gemini-4-argon`, high, provider Google), each a probe and a refutation, all verified from the provider's own fields (`second-opinions/*.provenance.json`).

**The seats saw different evidence** (D-WORKFLOW-195). GPT read the full packet (`gpt-brief.md`, 438,502 B, sha256 `4c24f7cc03c94eec…`). Gemini's first attempt on the same bytes truncated at its 65,536-token ceiling; its provenance is kept as `gemini-argon-audit-run1-truncated.md.provenance.json`. Its second attempt read the trimmed packet (`gemini-argon-brief.md`, 237,403 B, sha256 `adfc1f750b629faa…`). That packet held `02`, `03`, `04` and q4a verbatim from GPT's, the guest outputs and the achievements scripts whole, the 41 start scripts as excerpts (2,240 of 5,752 lines), and no context excerpts. A Gemini item resting on a start-script line it saw only in excerpt carries **excerpt** below.

Every seat item was re-read at its artifact before it was graded. A verdict is **CONFIRMED** (the artifact shows it, with the command or the proof named), **PLAUSIBLE** (the reading shows the code path; the effect needs a run this slice could not make), **REFUTED** (the artifact contradicts it) or **NARROWED** (part of it holds). G16 (cycle 3) was run to decide one seat claim.

### The re-grades of the first reader's findings

| Finding | GPT | Gemini | Decision and the artifact |
| --- | --- | --- | --- |
| F-01 | agree; narrow "any image" (H1 is not an ARM runtime test) | agree | **Medium, stands.** "Every image" rests on H1 (both pinned AppImages' layout) for aarch64 and on G7 at run time for x86_64; the wording now says so |
| F-02 | agree; the `gptokeyb openbor` behaviour not supplied | agree | **Medium, stands.** The "own menu is the only exit" phrase is withdrawn; `gptokeyb` without `-k` is not shown to kill |
| F-03 | Medium | Medium | **Re-graded Medium** (both): the simple core is a supported per-game setting (`start_mupen64plus.sh:19,101-106`); same player impact as F-01 |
| F-04 | agree; the missing kill target is latent until the route works | agree | **Medium, stands**, worded as a broken route plus a latent kill target |
| F-05 | agree at the read hash; T3's tip not verifiable from the packet | agree | **Medium, stands**; T3's tip read by this lane at `3c47325fb2` (`02` F-05) |
| F-06 | agree | agree | **Medium, stands** |
| F-07 | **High** | **High** | **Re-graded High** (both): G3, root code from library content on a launch |
| F-08 | agree; not shell execution; the summary's grouping wrong | agree; adds globbing | **Medium, stands**; `04`'s summary no longer groups it with code execution; `echo ${params}` also globs against `/storage/roms/doom` (Gemini, **excerpt**: `start_gzdoom.sh:95-96`) |
| F-09 | agree; melonDS disables, does not clear | agree; melonDS refuted as "clears"; widen to "off" | **Medium, stands; wording corrected:** `cheevos_melonds.sh:28-54,98-104` sets `RA_Enabled=0` and keeps the username and password (it nulls only empty values), so melonDS does not reuse the session but does keep the credentials. Widened: on "off", ppsspp, armsx2, aethersx2 and flycast leave the token at rest (Gemini G-05, CONFIRMED by reading) |
| F-10 | Low | Medium | **Low, stands**: the image ships `global.retroachievements=0` (`/usr/config/system/configs/system.cfg:77`), so the empty case needs the key deleted |
| F-11 | Low; add `start_melonds.sh:140`; `:187` always false; `>` truncates | Medium; the same additions | **Low, stands; corrected to 11 sites** (`start_melonds.sh:140`, `if [ "$SROTATION" ] >"0"`, both seats, CONFIRMED by reading). `start_mednafen.sh:187` fails (`[: missing ']'`, always the else branch) rather than testing non-emptiness. A `>` redirection truncates an existing file of that name in `/storage` |
| F-12 | **High**; normal unlinking of a link is not deletion; cemu's globs miss hidden entries | agree; the trigger is not rare (G-03, G-04) | **Re-graded High.** G16 shows the Tools launcher's DuckStation creating `savestates` as a real directory, and the next game launch deleting it: a normal sequence, not only an old archive restored |
| F-13 | agree; "nowhere public" overstated | agree | **Medium, stands** (#849); worded "absent from the named locations" |
| F-14 | Medium | Medium | **Re-graded Medium** (both): the directory blocks the BIOS path every launch re-tests |
| F-15 | Low | Medium | **Low, stands**: amiberry is not on a shipped device's default route, and the effects are configuration, not saves |
| F-16 | Low; the parser not shown | Medium | **Low, stands**: class 1 (upstream's array form); the effect on Supermodel's start not shown |
| F-17 | Low; adds `right]` | Medium (as G-07) | **Low, stands; widened** with `pce[_fast]` (both seats; CONFIRMED with bash: `[[ pce =~ pce[_fast] ]]` is false), the stray `]` in `right]`, and the unquoted `$(get_setting …)` tests at 107, 131 and 137 (Gemini, **excerpt**) |
| F-19 | Medium; narrow the devices (SM8550 takes the fixed-name branch) | -- | **Low, stands; narrowed:** `start_yabasanshiro.sh:42-43` gives SM8550 a fixed name, so the device-name `eval` runs on H700 only, and needs a crafted device connected |
| F-20 | Medium | Medium; adds: an empty password shifts the arguments | **Re-graded Medium.** Gemini's G-02 is CONFIRMED by reading (`start_gopher64.sh:104,125`): with the password empty, `--ra-password` takes the ROM path |
| F-21 | Medium; the missing-key branch writes the escaped value | Medium | **Re-graded Medium**; both additions CONFIRMED (`cheevos_melonds.sh:94` writes `${password_esc}` with `escape_sed`'s backslashes) |
| F-22 | Low; broaden to SkyEmu | Low (in G-11) | **Low, widened** to `cheevos_skyemu.sh:30-33` |
| F-23 | Low; per-row not independently confirmed | -- | **Low, stands**; the per-row records are `.qa-scratch/t30/routes.json`, not in the packet |
| F-24 | Low; narrow: the ini sets the renderer | -- | **Low, stands**, worded as a dead construction |
| F-25 | Low; caller search for `psp_save_mover.sh` not shown | -- | **Low, stands**: `git grep -n psp_save_mover 8ebaf8daad -- projects packages` printed nothing (stage C) |
| F-26 | accept; "nothing to migrate" needs an inventory | -- | **Low, narrowed:** the deletion removes no data; whether ARMSX2 reads AetherSX2's save states is not shown, so "nothing to migrate" becomes "nothing removed; compatibility unproven" |
| F-27 | Low/informational | -- | stands |
| F-28 | narrow to provenance information | -- | **Low, narrowed** to "name the branch" |
| F-29 | Low | Medium | **Low, stands**: settings, not saves (`SaveSRAMPath` stays under `/storage/roms/n64`) |
| F-30 | Low; **wording wrong**: a quoted multi-PID kills none | Medium; the same correction | **Low, wording corrected:** `kill -9 "$(pidof gptokeyb)"` with two PIDs fails as one bad argument and kills none; the same quoted form at `start_melonds.sh:190` and `start_skyemu.sh:56`; the unquoted form at `start_azahar.sh:240` and `start_drastic.sh:93` kills every `gptokeyb` |
| F-18 | withdrawal accepted, but the empty-file and last-line cases stand | -- | **Withdrawn as filed; G-40 carried** (below) |

### Seat items: own findings

| Seat item | Verdict | New finding | Artifact |
| --- | --- | --- | --- |
| GPT G-01 / Gemini G-01 (Steam's `exit 0`) | **CONFIRMED** (both) | **F-31**, Medium | `start_steam.sh:253,264` exit inside `steam_launch_bigpicture`; the flavours' `steam_dual_screen_end` and `systemctl start/restart systemd-binfmt` (`start_steam_x86.sh:26-30`, `start_steam_arm64.sh:28-30`) never run |
| Gemini G-13 (x86 Steam's kill target names only `FEX`) | PLAUSIBLE | in **F-31** | `start_steam_x86.sh:10` against `start_steam.sh:259-260` |
| GPT G-21 (Steam URI and `-silent` as one argument) | CONFIRMED by reading; the effect PLAUSIBLE | **F-32**, Low | `start_steam.sh:205,240,260` |
| GPT G-16 (DraStic's binary never refreshed) | **CONFIRMED** by reading | **F-33**, Medium | `start_drastic.sh:28-31,92`: the copy only when `/storage/.config/drastic` is absent, the run from there; an OS update's DraStic never reaches an existing H700 (the default `nds` emulator there) |
| GPT G-13 (Dolphin's face swap re-applied to `Hotkeys.ini`) | **CONFIRMED** by reading | **F-34**, Medium | `start_dolphin_gc.sh:43-47,404-419`: `GCPadNew.ini` is recopied each launch, `Hotkeys.ini` is not, so its swap alternates launch to launch on an affected pad |
| GPT G-04 (melonDS's regenerated TOML holds the credentials) | PLAUSIBLE | **F-35**, Medium (to verify) | `start_melonds.sh:182`; patch `000:7519-7522`; `backuptool:707` blanks only the INI |
| GPT G-44 (`-9` with no orderly shutdown) | PLAUSIBLE | **F-36**, Medium (an open item to test) | every `set_kill` line; Dolphin's `start_dolphin_gc.sh:34-35` comment; #117's precedent for RetroArch |
| GPT G-02 (OpenBOR empties `Paks`) | CONFIRMED by reading | **F-37**, Low | `start_OpenBOR.sh:27`; the script's staging folder; loss only of files placed there by hand, or through a `Paks` link |
| Gemini G-04 / GPT G-19 (SkyEmu's link parent) | PLAUSIBLE (needs `/storage/.local/share/Sky` absent) | in **F-12** | `start_skyemu.sh:21,30-31` |
| Gemini G-03 (Tools-then-game) | **CONFIRMED** (G16) | in **F-12** (the High) | `p3-tools-then-game.out` |
| Gemini G-03's second half (DuckStation's achievements disabled every launch) / GPT G-42 | CONFIRMED by reading | **F-38**, Low | `start_duckstation.sh:131`, upstream's workaround ("not working"); `04` § Q1's "signs itself in" corrected |
| Gemini G-05 (tokens kept on "off") | CONFIRMED by reading | in **F-09** | the five scripts' "off" branches |
| Gemini G-06 / GPT G-14, G-15 (settings overwritten every launch) | CONFIRMED by reading | **F-39**, Low | `start_xemu.sh:19`; `start_melonds.sh:181-182`; `start_dolphin_gc.sh:72-76` |
| GPT G-08, G-09, G-10 / Gemini G-11 (sed escaping; section bounds; armsx2's first section) | CONFIRMED by reading | **F-40**, Low | the achievements scripts' `sed` lines; `cheevos_armsx2.sh:46-48` |
| GPT G-17, G-41 (ScummVM's seed unreachable; generated names unconfined) | CONFIRMED by reading | **F-41**, Low | `start_scummvm.sh:22-25,41-44,31-37` |
| GPT G-03, G-27 (hypseus device-name path; `.commands` word-split) | PLAUSIBLE | **F-42**, Low (hygiene) | `start_hypseus.sh:17-20,68,75-84` |
| GPT G-05, G-06, G-07 (publication failures not launch failures; temp files beside the configs; `.tmp.$$`) | PLAUSIBLE | **F-42** | `cheevos_armsx2.sh:106-131`; `cheevos_dolphin.sh:43-62` |
| GPT G-20 / Gemini G-12 (Daedalus's `rm` without `-r`) | CONFIRMED by reading | **F-42** | `start_daedalusx64.sh:20-25` |
| GPT G-23, G-24, G-25 (amiberry and Hatari floppies: `echo -e`, arbitrary entries, writes to a deleted temp tree) | CONFIRMED by reading; G-25's save loss PLAUSIBLE | **F-42** | `start_amiberry.sh:79-159`, `start_hatari.sh:40-74` |
| GPT G-26 (DS archives: unchecked extraction, top-level lowercase `.nds` only) | CONFIRMED by reading | **F-42** | `start_dsperate.sh:147-155`, `start_melonds.sh:157-165` |
| GPT G-29 (backslashes stripped from ROM paths) | CONFIRMED | **F-42** | `start_ppsspp.sh:105`, `start_vice.sh:15` |
| GPT G-31 (VSync read, not applied) | CONFIRMED by reading | **F-42** | `start_aethersx2.sh:35`, `start_armsx2.sh:45`, `start_cemu.sh:115,226-228` |
| GPT G-32 (cemu forwards the platform) | CONFIRMED by reading | **F-42** | `start_cemu.sh:335` |
| GPT G-33 (gzdoom's pk3 repair skipped when the copy is missing) | CONFIRMED by reading | **F-42** | `start_gzdoom.sh:28-33` |
| GPT G-34 (pico-8: "splore" anywhere in the path) | CONFIRMED by reading | **F-42** | `start_pico8.sh:20-27` |
| GPT G-35, G-36, G-37 (Vita3K's install paths) | CONFIRMED by reading | **F-42** | `start_vita3k.sh:14,32,187-190,210,227-244` |
| GPT G-38 (RPCS3's M3U prefix) | CONFIRMED by reading | **F-42** | `start_rpcs3.sh:182-186` |
| GPT G-39 (emulator status discarded) | CONFIRMED by reading | **F-42** | the eleven sites GPT lists |
| GPT G-40 (melonDS: a matching last line deleted, the append skipped) | PLAUSIBLE | **F-42** | `start_melonds.sh:112-113,130,133` |
| GPT G-22 (Steam's VDF index) | CONFIRMED by reading | **F-42** | `start_steam.sh:12-17` |
| GPT G-43 (the kill debounce across launches) | CONFIRMED as code | **F-42** | `input_sense:217-221` (T1's file; noted for its owner) |
| GPT G-12 (compositor replies evaluated) | CONFIRMED as code; a trust seam, not data a player supplies | **F-42** (a note) | `start_steam.sh:81-84`, `start_heroic_play_gamescope.sh:33-36` |
| GPT G-45 (gzdoom's provenance) | **REFUTED** as provenance; CONFIRMED as cosmetic | **F-42** (gzdoom's banner) | `git describe --tags b137d8c373` prints `rc1-20260929-185-gb137d8c373`: GZDoom stamps the enclosing checkout's describe |
| GPT G-18 (Hatari's config seed) | PLAUSIBLE, conditional on the first-boot seed (`post-update:38-49,118` names `system`, `game`, `modules` and a list) | **F-42** | `start_hatari.sh:8-34` |
| Gemini G-08 / GPT G-28 (yabasanshiro's unquoted `cp`) | **NARROWED**: latent | **F-42** | the only keymap seed is `keymapv2_rg_arc_joypad.json` (`git ls-tree`); no seed name has a space, so SM8550's DualSense name fails the `[ -e ]` test first |
| Gemini G-09 (ScummVM's `libretro` arm writes no kill target) | **REFUTED** | -- | `runemu.sh:263-264` sets `retroarch retroarch32` for every RetroArch launch before the `scummvm` platform case swaps `RUNTHIS`; the `add` arm is a scan, not a game |
| Gemini G-10 | CONFIRMED | in **F-11** | `start_melonds.sh:140` |
| Gemini G-07 | CONFIRMED | in **F-17** | above |

### The exit sweep and Q4, as the seats read them

- **Exit sweep.** Both seats accept it as an inventory, not as 35 live verdicts. The table's *Guest* column says which rows were seen live: G1, G7, G14, G15 and G16 cover ppsspp, x64sc, gzdoom, ScummVM, DuckStation and OpenBOR; G6 covers Dolphin's name length by substitute. Two device cells are corrected: GENERIC_X64 *lists* `amiberry` and `yabasanshiro-sa` but does not *build* them (`PKG_ARCH`). Steam's contract differs by flavour (F-31). ScummVM's row stands (G-09 refuted).
- **Q4.** Both seats accept the tally. Taken from them:
  - the five `conflicts` rows are flagged dispositions, not trial-merged conflicts;
  - `dsperate-sa` is behind upstream as well as its project;
  - q4a's merge rows are classed by their first-parent diff, which is why a merge touching `cheevos_armsx2.sh` reads differently from `f8844ab04e`.
- **Q5.** GPT is right that "nothing above 0.07 s" overstates: Dolphin's `prepare` phase and the `sed` passes were not timed. Q5 now says which helper runs were measured.

### Not judged by either seat, and said here

Real-game shutdown durability (F-36), melonDS's TOML (F-35), the 22 members the guest lacks, and the per-device configs.

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

