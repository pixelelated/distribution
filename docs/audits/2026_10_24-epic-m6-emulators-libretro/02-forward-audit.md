# Forward Audit — M6.P2 T3, RetroArch and the libretro cores

**Auditor:** Code Auditor skill (v1.13.0), primary Claude Opus 5.5 at high effort
**Date:** 2026-10-24
**Subject:** #650 (`M6.P2 E798/T3`), slice `emulators-libretro`; read at `reviewed-at: d606301784`, the slice's bytes equal to `next`'s `8ebaf8daad`
**Spec:** `docs/reviews/briefs/emulators-libretro.md` version 2; #650's checklist (= brief § 7)

---

## Running Notes

Findings are numbered `F-NN` in the order they are written. Each names its question (Q1 to Q7), its unit and its evidence. Severity and category are set in `04` and `05`. A guest proof is written under § Guest proofs, with its cell; the cell's token appears in this file only there (criterion 12).

## Mechanical checks (brief § 5)

### `tools/retroarch-wrapper-test` (02:47 UTC, host `gcc` with ASan, the M7 roots read-only)

All runs are from the T3 worktree at `d606301784` (the #799 fix):

| Run | Command | rc | Summary line |
| --- | --- | ---: | --- |
| unfixed, no argument | `python3 -I <HEAD^'s copy>` | 2 | `no video_thread_wrapper.c given and none under .../devices/build.ROCKNIX-H700.aarch64, .../generic-x64/build.ROCKNIX-GENERIC_X64.x86_64` |
| fixed, no argument | `python3 -I tools/retroarch-wrapper-test` | 0 | `pin bdba046fa6766380bc2457532f38e589df769aaf, 12 candidate source(s)`; source `m7-pixelelated-h700-03/build.pixelelated-H700.aarch64/...`; `posted 2000 command(s); the method ran 2000 time(s)`, `PASS` |
| plain, the M7 GENERIC_X64 root | `python3 -I tools/retroarch-wrapper-test $B/build/retroarch-bdba046fa6766380bc2457532f38e589df769aaf/gfx/video_thread_wrapper.c` | 0 | 2000 of 2000, `PASS` |
| `--gated`, the same file | the same, with `--gated` | 0 | 2000 of 2000, `PASS`: identical to the plain run (F-01) |
| constructed failure: a pin no root carries | a copy of the tool in `.qa-scratch/t3-wrapper/fakecheckout/` with `PKG_VERSION="000...0"` | 2 | `none for the pin 0000000000000000000000000000000000000000 in the build.* roots of 132 checkout(s)` |
| constructed failure: the pin's source with 0015 reversed | `patch -R -p1` of `0015-video-thread-wrapper-run-a-command-once.patch` onto a copy, then the tool on it | 1 | `posted 2000 command(s); the method ran 2011 time(s)`, `FAIL: a posted command was executed more than once` |

`$B` is `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64`. The twelve candidate copies of the pinned `gfx/video_thread_wrapper.c` (H700, SM8550 and GENERIC_X64 roots, arm and aarch64) all have sha256 `b578746ee1b053b5211961f6f56f08cd0b2568fef8bb8bfc84b374b307c76952`. **What the check proves:** patch 0015's dequeue runs each posted command once against the pinned source, and the same harness catches the doubled run when 0015 is removed. **What it does not prove:** patch 0011's poster lock (the harness posts from one thread), and anything at run time on a device.

### `tools/pkgcheck` over every recipe (finished before 02:55:29 UTC, the next `date -u`)

The loop of brief § 5: the 151 `package.mk` under `emulators/libretro/` as the two globs list them (the five recipes outside the membership included, recorded as T24's), plus `emulators`. **152 runs: 151 rc 0, 1 rc 1.** Each run's output is kept under `.qa-scratch/t3-pkgcheck/<name>.out` (gitignored). Every run printed exactly one recipe path, and the three `easyrpg-lr` sub-recipes printed only their own path. The non-clean lines (ANSI stripped):

| rc | Recipe | Line |
| ---: | --- | --- |
| 1 | `sameboy-lr` | `[FAIL] 013: .../sameboy-lr/package.mk: late binding violation : ref PKG_BUILD` (F-02) |
| 0 | `flycast2021-lr` | `[WARN] 032: .../flycast2021-lr/package.mk: intertwined vars & funcs : PKG_MAKE_OPTS_TARGET+=" ARCH=${TARGET_ARCH} ..."` (F-03) |
| 0 | `emulators` | `[WARN] 132: .../virtual/emulators/package.mk: unknown function : install_script()` (read at its site: the recipe's own helper, called from `makeinstall_target`; the warning is about the name, not a defect. Recorded, no finding) |

## Findings, written as each unit is read

### F-01 (Q6, Q3): `tools/retroarch-wrapper-test --gated` asserts nothing

`tools/retroarch-wrapper-test:57` (after #799, line numbers at `d606301784`) sets `gated = "--gated" in sys.argv`, and no other line reads `gated` (`grep -n gated` prints the usage line 7 and line 57 only). `git log -S gated` shows the flag arrived with the tool's first commit, `e5d14d4220` (2026-09-19), already unread. A `--gated` run prints exactly the plain run's lines (above). The docstring does not say what it was meant to assert. The brief told the lane to read the docstring before trusting either line, and the docstring is silent. **So the usage line advertises a mode that does not exist, and a reader who runs `--gated` believes something extra was checked.** Fix shape for the punch list: remove the flag and its usage mention, or implement what the author meant (the history does not say, so it is a question for the coordinator). Outside the membership, in the slice's group 5.

### F-02 (Q2, Q6): `sameboy-lr`'s `BOOTROMS_DIR` is a late-binding violation and a dead option

`projects/ROCKNIX/packages/emulators/libretro/sameboy-lr/package.mk:13` reads `PKG_MAKE_OPTS_TARGET="-C libretro BOOTROMS_DIR=${PKG_BUILD}/BootROMs/prebuilt"` at global scope. `PKG_BUILD` is empty there (`packages/README.md` § Late binding), so the option is `BOOTROMS_DIR=/BootROMs/prebuilt`. It is also read by nothing on this build path:

- the recipe builds with `-C libretro`;
- SameBoy's `libretro/Makefile` (the M7 GENERIC_X64 root's unpack of `aa158a889a`, read-only) takes its boot ROMs from `$(CORE_DIR)/BootROMs/prebuilt/%_boot.bin` (its lines 368 and 381);
- only the top-level `Makefile` reads `BOOTROMS_DIR` (line 56), for the SDL, tester and app targets.

The core is built and installed regardless (`image/system/usr/lib/libretro/sameboy_libretro.so`, 355,104 bytes). **So it is the `ppsspp-lr` shape of `device-builds.md` § Late binding bites hardest in a merge, with no effect today: a variable that is empty, passed to a make that ignores it.** `pkgcheck` fails the recipe on it. History: the line came with the ROCKNIX recipe (`9f1fab30f6`, 2025-07-13), unchanged since. `upstream/next` carries the same line (its only diff is the dependency line of `af70bd435b`). Fix shape: drop `BOOTROMS_DIR=...`, keep `-C libretro`. Proof: `pkgcheck sameboy-lr` rc 0; the core's build has no image until the coordinator's integration build, so its row is `fix-pending-image`. An upstream contribution candidate for #585 (D-WORKFLOW-164).

### F-03 (Q2, Q7): `flycast2021-lr` assigns `PKG_MAKE_OPTS_TARGET` between two functions

`flycast2021-lr/package.mk:32` (`PKG_MAKE_OPTS_TARGET+=" ARCH=${TARGET_ARCH} HAVE_OPENMP=0 GIT_VERSION=${PKG_VERSION:0:7} HAVE_LTCG=0"`) sits between `post_unpack()` and `pre_make_target()`. `pkgcheck` warns that this is cosmetic. It is also a late-binding reference: `TARGET_ARCH` is set by the build system before recipes load (`config/options` reads `config/arch.${TARGET_ARCH}`), so it is not on the README's late-binding list, and `pkgcheck` does not fail it. The recipe is upstream-carried and in `X64_SKIP_CORES`. Cosmetic Q2 only: the fix is to move the line above the functions. It is a Q7 row, not a defect.

### shellcheck v0.11.0 (03:00 UTC; the binary downloaded into `.qa-scratch/t3-shellcheck-dl/`, `sha256sum -c` against the release's published digest `8c3be12b05d5c177…` OK; run by path from `.qa-scratch/t3-shellcheck/`)

**30 files**, the brief § 5 set: `virtual/emulators/package.mk` (`-s bash`), `functions` lifted, the 24 `sources/*.sh` (each with its own shebang), `scripts/mkcontroller`, `autostart/001-controller`, RetroArch's `autostart/003-logging` and `scripts/call_achievements_hooks.sh`. Totals: **6 errors, 46 warnings, 70 notes**. By code: SC2086 37, SC1091 29, SC2154 26, SC2034 11, SC2166 2, SC2048 2, SC2046 2, SC1128 2, one each of SC3014, SC2295, SC2231, SC2164, SC2001, SC1090. **Each error read at its site:**

- **4 errors in the `functions` lift (SC1046, SC1073, SC1047, SC1072) are artifacts of the lift**: lines 99 to 140, as the brief gives them, end inside `add_es_system`'s `if`. Re-lifted on whole-function boundaries, `add_emu_core` (88) to the end of `add_es_system` (219), plus the config.xml lines to 225: **0 errors**, 9 warnings (six SC2069 at 177, 187, 193, 201, 207, 214: `2>&1 >/dev/null` sends `xmlstarlet`'s stderr to the build log and discards stdout, which is what the code wants, so not a defect; SC2048 at 96, `add_emu_doc $*`; SC1090 at 131; SC2034 at 224). These are T5's lines, read as the table's machinery.
- **2 errors, SC1128, in `Start Azahar.sh` and `Start MelonDS.sh`: the shebang is on line 2** (F-04).

The warnings, read by group:

- **SC2154 ×26 in `scripts/mkcontroller`:** 56 to 101 reference the pad's mapping variables, which come from a non-constant `source` at 56 (SC1090). Not a defect; read again when the script is read.
- **SC2034 in `package.mk` 5 to 10:** `PKG_*` read by the build engine. False positives.
- **SC2034 in `Install Steam.sh` 2723 to 2729 and `Scan Heroic Games.sh` 18:** variables assigned and never read. Q6 leads for the reading; the Steam ones are on the file M7's `6101242e14` changes.
- **SC2046 in `Start Azahar.sh` 32 and `Start BigPEmu.sh` 11; SC2164 in `Start DaedalusX64.sh` 12; SC2166 ×2 in `Start Vita3K.sh` 17; SC2154 `param_device` in `Start Dolphin.sh` 28:** Q2 leads, read at their sites with the scripts (group 2).
- **`call_achievements_hooks.sh`, a `#!/bin/sh` script:** SC3014 at 13 (`==` in a POSIX `[`) and SC2048 at 15 and 17 (unquoted `$*`). Read with RetroArch's group.

### The launch table on the image, parsed (03:03 UTC)

`usr/config/emulationstation/es_systems.cfg` from the M7 GENERIC_X64 build root's install tree (83,206 bytes), parsed with `python3 -I` and `xml.etree.ElementTree`:

- **128 `<system>`, 152 `<emulator>`, 348 `<core>`.** The brief's recorded "500 `<core` elements" is a text count that also matches the 152 `<cores>` wrappers: 348 + 152 = 500. **This is a delta, recorded beside the brief's figure.**
- **Commands:** 125 systems carry `RUNCMD` (`/usr/bin/runemu.sh %ROM% -P%SYSTEM% --core=%CORE% --emulator=%EMULATOR% --controllers="%CONTROLLERSCONFIG%"`). Three carry their own: `imageviewer` `/usr/bin/true`, `moonlight` `/bin/sh %ROM%`, `tools` `/usr/bin/foot %ROM%`.
- **Defaults:** every system has exactly one `default="true"` core except four. `imageviewer` and `tools` have no emulator, by design. **`psx` and `st-v` have none** (F-05).

### F-04 (Q2): `Start Azahar.sh` and `Start MelonDS.sh` carry their shebang on line 2

Both files begin with an empty line and put `#!/bin/bash` on line 2 (`head -4 | cat -A`). Both are upstream-carried (`1a30c6a368` 2026-03-23; `02fe535ab1` 2026-03-20), and `upstream/next` has the same bytes. Installed as `/usr/config/modules/<name>.sh` on the devices whose arms call `install_script` (`package.mk` 194, 998 to 1035), they run from the `tools` system as `/usr/bin/foot %ROM%`. `foot` calls `execvp` (`strings usr/bin/foot`). With no shebang on line 1 the kernel refuses the file (ENOEXEC), and glibc's `execvp` falls back to running it with `/bin/sh`. On the image `/bin` is a symlink to `/usr/bin` and `usr/bin/sh` points at `bash` (read in the install tree), so the scripts still run under bash, and `Start MelonDS.sh`'s `[[` works. **So today it is a standards defect with no visible effect, resting on two facts outside the file:** glibc's fallback and the image's `sh`. Neither module is installed on GENERIC_X64 (`usr/config/modules/` lists 19 others), so the guest cannot run the shipped file. Fix shape: delete the blank first line in both. Can this be done on the VM? The fallback interpreter can be shown on the guest with a fixture of the same shape (a blank line, a line-2 shebang, a `[[` test) run through `env`, which also calls `execvp`; that is a lead to prove if the fix is taken.

### F-05 (Q3, Q6): on GENERIC_X64 `psx` has no default core, and `st-v` has no emulator on the fork's handheld images either

`virtual/emulators/package.mk` 1165 to 1209: the `psx` `case ${DEVICE}` has arms for every device except **GENERIC_X64**. After it come two lines for every device: `add_emu_core psx duckstation duckstation-sa false` and `add_emu_core psx retroarch swanstation false`. So on the VM image `psx` carries two emulators and no `default="true"`, as the parsed table shows: `duckstation` (`duckstation-sa`) and `retroarch` (`swanstation`), both unmarked. Which one EmulationStation then launches is the interface's choice (T2's `SystemData` rows). Read there, not assumed here.

`st-v` (1395 to 1401) gets `add_emu_core st-v mednafen ss true` only on RK3588, SM4450, SM6115, SM8250, SM8550, SM8650, SM8750 and AMD64. **So on H700, RK3326, RK3566 and GENERIC_X64, four of the fork's five built devices, the table carries an `st-v` system with no emulator at all** (the image's `st-v` entry has an empty `emulators` list). A player with ST-V games on an H700 sees a system that cannot launch them.

To prove per device, by the host regeneration of the table (the next check), and to read against `upstream/next` (whether the same lines are upstream's) before a fix shape is written. The VM claim is the image's table, read above: `image-set` evidence, read on the host, not a guest proof.

### The host regeneration of the table (03:01 to 03:04 UTC): the tree's own shell, proven byte-exact against three images

`docs/audits/2026_10_24-epic-m6-emulators-libretro/tools/regen-es-systems.sh` (committed with this file) sources `distributions/ROCKNIX/config/functions` and `virtual/emulators/package.mk` from the worktree. It runs `makeinstall_target` under `bash -e`, matching the real build (`config/path:4` sets `set -e`), inside `env -i`. Every write goes under `.qa-scratch/t3-regen/<DEVICE>/`: `ROOT`, `ESTMP`, `INSTALL` and `SYSDOC`, with `ROOT/config` a read-only symlink to the tree's `config/`.

**A gap in the brief's recipe, found and closed:** brief § 5 says only the formatted file needs `xmlstarlet`. But `add_es_system` calls `xmlstarlet sel` and `xmlstarlet ed` for every core (`functions` 171 to 214), so without it every system would come out with no emulators. **The run therefore uses the build's own host `xmlstarlet`**, copied from the M7 GENERIC_X64 root's `toolchain/bin/xml` (`xmlstarlet` is a symlink to it) into `.qa-scratch/t3-regen/xs/xml`. The copy and the original both have sha256 `3ee557da6cbdefa8…`; version 1.6.1, libxml2 2.15.3.

`get_pkg_version` (the build engine's) is a stub that reads `PKG_VERSION` from the recipe, the `projects/ROCKNIX` override first. It logs every call and every miss.

| `DEVICE` (`ARCH`, `ENABLE_32BIT`, `WINDOWMANAGER`, `PREFER_GLES`) | rc | Systems | Against the image built from it | The stub |
| --- | ---: | ---: | --- | --- |
| GENERIC_X64 (`x86_64`, `no`, `swaywm-env`, `no`) | 0 | 128 | **byte-identical**: `es_systems.cfg` (sha256 `95b1a9b6b166a47d…`, 83,206 bytes), `system-dirs.conf`, `core-pins` (128 lines); the 8 modules it installs are among the image's 19 (the 11 others come from other packages) | 129 calls, 0 misses |
| H700 (`aarch64`, `true`, `swaywm-env`, `yes`) | 0 | 126 | **byte-identical** to `m7-signin-h700-build-20261023-06`'s install tree: `es_systems.cfg`, `system-dirs.conf`, `core-pins`; its modules all present | 0 misses |
| RK3326 (the same knobs as H700) | 0 | 126 | no image on the host | 0 misses |
| RK3566 (`aarch64`, `true`, `swaywm-env`, `yes`) | 0 | 132 | no image on the host | 0 misses |
| SM8550 (`aarch64`, `true`, `swaywm-env`, `no`) | 0 | 139 | **byte-identical** to `m7-signin-sm8550-build-20261023-03`'s: `es_systems.cfg`, `system-dirs.conf`, `core-pins` | 0 misses |

The device knobs are each device's `options` (`WINDOWMANAGER`, `PREFER_GLES`; GENERIC_X64's `ENABLE_32BIT=no`), and `ENABLE_32BIT` defaults to `true` (`distributions/ROCKNIX/options:69`). The H700 and SM8550 images were built from `08cc7ff6cd`. On the two slice directories, `functions` and `config/emulators`, that source differs from `next` only in `Install Steam.sh` (`git -C /workspace/repos/rocknix diff --stat next 08cc7ff6cd -- ...`), which the table does not read.

**So the regeneration is the build's own table for any tree.** A fix to the recipe or the table can be proven on the host by this script (`fix-host-regen`), and the five devices' tables are the Q6 input. A FAIL it can produce: any edit to an `add_emu_core` line changes the bytes; the constructed case is below.

**The five tables, analysed** (`python3 -I`, `ElementTree`, over each regenerated `es_systems.cfg`; per system: the count of `default="true"` cores and whether it has an emulator):

| Device | Systems | Emulators | Cores | No default | More than one default | No emulator (besides `tools`, `imageviewer`) |
| --- | ---: | ---: | ---: | --- | --- | --- |
| H700 | 126 | 184 | 395 | none | none | `st-v` |
| RK3326 | 126 | 184 | 395 | none | none | `st-v` |
| RK3566 | 132 | 196 | 410 | none | none | `st-v` |
| SM8550 | 139 | 256 | 481 | none | none | none |
| GENERIC_X64 | 128 | 152 | 348 | `psx` | none | `st-v` |

**F-05 confirmed per device.** `st-v` has no emulator on H700, RK3326, RK3566 and GENERIC_X64, and `psx` has no default on GENERIC_X64 alone. `git diff upstream/next 8ebaf8daad -- virtual/emulators/package.mk` does not touch the `psx` or `st-v` blocks, so both are upstream's lines, carried into a fork-own file. The `psx` gap is the fork's because GENERIC_X64 is the fork's device. The `st-v` gap is a defect upstream ships too (#585 candidate, D-WORKFLOW-164).

### F-06 (Q3, Q7): the table's "only one default" rule is enforced by accident on one shape, silently, and not at all on the other

The README comment in `makeinstall_target` (`virtual/emulators/package.mk` 150 to 151) says: *"Only ONE core per system can be set as the default, setting multiple cores will result in a build failure."* No line checks this. What happens is decided by `add_es_system`'s default step (`functions` 212 to 214), `xmlstarlet ed --inplace -i "//system/emulators/emulator[@name=X]/cores/core" -t attr -n default -v true`. It adds the attribute to **every** core of that emulator added so far, not to the one just added. Two constructed cases, by the regeneration over a scratch copy of the recipe (`.qa-scratch/t3-regen/fake/`, GENERIC_X64):

- **Case A, two `true` lines in one emulator** (`3do`: `opera true`, then `opera_two true`): the first core gets the attribute twice (`<core default="true" default="true">opera</core>`), the pre-format file is malformed, and `mk_es_systems`'s `xmlstarlet fo` (`functions:113`) exits **2**. `set -e` ends the recipe there. **The build does fail, with no message**: `fo`'s stderr goes to `/dev/null`, and its reason (`Attribute default redefined`, read by running the same `fo` by hand) is never printed. The regeneration's log was empty; `bash -x` found the line.
- **Case B, a `false` core listed before the `true` one in the same emulator** (`bbcmicro`: `first_false false`, then `b2 true`): **both cores carry `default="true"`**, the file is well-formed, and the build succeeds. The table then holds two defaults, against the comment's rule, and which one the interface launches is the interface's choice.

**Today:** no device's table has two defaults (above), because every list puts its `true` line first in its emulator. So case B is latent, a trap for the next edit. Both cases sit in T5's `functions` (the slice reads it as context and the fix is T5's path), but the comment that misleads is this slice's recipe. Fix shape for the punch list: in `functions`, mark the core just added (`.../cores/core[last()]`) and make `mk_es_systems` print `fo`'s error. That is T5's, filed as a lead on #650 for the coordinator to route. On this slice's side, the comment should say what is checked (Q7).

### F-07 (Q4): upstream dropped `aethersx2-sa` on 2026-10-18 for a licensing concern; `next` still builds and ships it

`c4d353449e` (`upstream/next`, sunshineinabox, 2026-10-18, *"aethersx2: drop package due to licensing concern"*) removes the recipe, `licenses/AETHERSX2.pdf`, its per-device inis, `Start AetherSX2.sh`, its `es_features.cfg` block, its `rocknix-systems` and `factoryreset` lines, and 27 lines of `virtual/emulators/package.mk`. `next` still carries `aethersx2-sa` in `PKG_EMUS` for RK3399, RK3566/RK3576, RK3588, SM6115, SM4450, SM8250, **SM8550**, SM8650/SM8750 and S922X (`package.mk` 49 to 94), and the `ps2` arm installs `Start AetherSX2.sh`. **SM8550 is a device the fork builds**, so the fork's SM8550 image carries a package its upstream dropped over licensing. This is the first of Q4 (a)'s 14 dispositions, and its decision is not this lane's. The recipe is T30's (`emulators/standalone/aethersx2-sa`). The table lines and `Start AetherSX2.sh` are this slice's. The licence question belongs to #528's gates. **Posted on #650 for the coordinator, with D-UI-079 in view: it removes a player-visible emulator.** Disposition on the punch list: `to merge` pending that word, `Already written:` the PS2 settings and memory cards AetherSX2 left under `/storage` on SM8550 and RK3566 devices.

### F-08 (Q3, Q4): the default PlayStation core on H700, RK3326, RK3566 and SM8550 is not where the launcher loads it

**What the table says:** `virtual/emulators/package.mk` 1165 to 1189 makes `retroarch` / **`pcsx_rearmed32` the `default="true"` `psx` core** on H700|RK3326, RK3576|RK3566 and SM4450|SM8250|SM8550. That is four of the fork's five built devices, and the H700 and SM8550 images' tables carry it (`<core default="true">pcsx_rearmed32</core>`).

**What the launcher loads:** `runemu.sh` (T1's, read-only) switches `RABIN` to `retroarch32` for `pcsx_rearmed32`, `gpsp` and `desmume` on aarch64 (lines 268 to 279). It starts `/usr/bin/${RABIN} -L /tmp/cores/${CORE}_libretro.so` (302). `/tmp/cores` is RetroArch's `tmp-cores.mount`, an overlay whose only lower directory is **`/usr/lib/libretro`**, with `/storage/cores` above it (`emulators/libretro/retroarch/system.d/tmp-cores.mount`). `retroarch32bit-append.cfg`'s `libretro_directory = /usr/lib32/libretro` does not apply, because `-L` names an absolute path.

**What the images carry** (the M7 roots' install trees, built from `08cc7ff6cd`, whose slice bytes are `next`'s except `Install Steam.sh`):

| Image | `usr/lib/libretro/pcsx_rearmed32_libretro.so` | `usr/lib32/libretro/pcsx_rearmed32_libretro.so` | `gpsp`, `desmume` in `usr/lib/libretro` |
| --- | --- | --- | --- |
| H700 (`m7-signin-h700-build-20261023-06`) | **absent** | present | present |
| SM8550 (`m7-signin-sm8550-build-20261023-03`) | **absent** | present | present |

`gpsp-lr` (24) and `desmume-lr` (34) each copy their 32-bit `.so` from `${ROOT}/build.${DISTRONAME}-${DEVICE}.arm/install_pkg/...` into `usr/lib/libretro`. **`pcsx_rearmed-lr` has no such copy**: its `makeinstall_target` installs `pcsx_rearmed32_libretro.so` only in the arm build, which `compat/lib32` then carries into `/usr/lib32`. No other writer puts a core under `/usr/lib/libretro` or `/storage/cores`: `git grep -E '/storage/cores|/tmp/cores'` finds only the mount and the `retroarch.cfg` keys.

**So, as the code and the images read, a PlayStation game launched with the default core on the fork's H700 and SM8550 images asks `retroarch32` to load a file that does not exist**, unless the player has put one in `/storage/cores` (the core updater's upper layer).

**Upstream found and fixed the same defect:** `c9820d0e89` (`upstream/next`, Jacob Cook, 2026-10-04, *"pcsx_rearmed-lr: install the 32-bit core where runemu loads it"*) adds exactly the missing copy. It is one of Q4 (a)'s 14, not on `next`.

**Can this be done on the VM?** No. The guest is x86_64, has no 32-bit RetroArch and no `pcsx_rearmed32` (`psx` there is F-05's). The load failure itself is a device fact. What an agent can verify on the host is the artifact: the file's presence in an arm-enabled image's `usr/lib/libretro`, read from the install tree or the `SYSTEM` squashfs. That is the criterion the bug carries. The verdict here rests on that artifact plus the code path, and the load failure is a lead until a device shows it. **Severity: High** (the default core of a common system on the fork's main handheld). It goes to a `bug` issue at stage D, and to #650 now because the M7 lane is testing an H700 image. **Tracked as #802**, filed by the coordinator on 2026-10-24 after verifying F-08 and F-09; the maintainer and the M7 lane were told, and no device run was asked. The fix comes with the base merge as `c9820d0e89` adapted to `${DISTRONAME}`; nothing on this branch. The punch item references #802 rather than filing a second bug.

`Already written:` nothing is written by the defect; a player who fetched `pcsx_rearmed32` into `/storage/cores` keeps that copy, which the overlay puts above the image's once the image carries one. That is read both ways, nothing to migrate.

### F-09 (Q4, interaction): the next base merge brings two copies that fail on the fork's build roots, and git merges them cleanly

`git merge-tree --write-tree --name-only next upstream/next` (read-only; result tree `d2df30a92a`): on the slice, exactly **five content conflicts**, all in the fork-own arcade recipes that carry the rotation-table hook (`fbalpha2012-lr`, `fbalpha2019-lr`, `fbneo-lr`, `mame2003-plus-lr`, `mame2010-lr`). Each is the fork's `PKG_DEPENDS_TARGET="toolchain Python3:host"` plus `PKG_NEED_UNPACK` against upstream's `af70bd435b` `PKG_DEPENDS_TARGET="toolchain retroarch"`; the resolution keeps both, `toolchain Python3:host retroarch`. The rest of the slice merges cleanly, including `virtual/emulators/package.mk` (the 29 conflicts tree-wide are outside this slice).

**But the clean part carries a trap.** The fork's ARM compatibility roots are `build.${DISTRONAME}-${DEVICE}.arm` (`43d0bc3bf4`, 2026-10-07; `DISTRONAME="pixelelated"`, `distributions/ROCKNIX/options:17`). Upstream's copies say `build.${DISTRO}-...`, and `DISTRO` is `ROCKNIX` here (`config/options:24`). `next` carries none (`git grep -F 'build.${DISTRO}-' next`: empty). The merged tree carries **two**, both new from upstream:

- `pcsx_rearmed-lr/package.mk:27`, the F-08 fix (`c9820d0e89`);
- `yabadabadoo-lr/package.mk:46`, the new core (`8704addb6b`).

On a fork build with `ENABLE_32BIT=true` both resolve to `build.ROCKNIX-<DEVICE>.arm`, which does not exist. Their `cp -a` fails, and `set -e` stops the build at that package. **So the fix for F-08 cannot be taken verbatim: the base merge must rewrite those two lines to `${DISTRONAME}`**, as `43d0bc3bf4` did for the other five. A check that would have caught it: `git grep -F 'build.${DISTRO}-'` empty on the merged tree.

### Q4 (c): the 21 RetroArch patches against master (03:18 UTC), `tools/q4c-patches.sh`

`q4c-patches.sh` fetches, from `libretro/RetroArch` through `gh api` (raw), the 25 files the series touches: 24 sources plus `retroarch/`-prefixed duplicates that `-p1` strips. It then applies the series in `scripts/unpack`'s order (`patches/*.patch` sorted, then `batteryplus/`, which the recipe adds through `PKG_PATCH_DIRS`). For each patch it records `git apply --check -p1` (#650 criterion 9's form) and `patch -p1 --fuzz=0 --dry-run`, then advances with `patch -p1` as `scripts/unpack:197` runs it (default fuzz). Outputs: `q4c-at-pin.txt`, `q4c-at-master-4fe09508d4.txt`. Master was **`4fe09508d4b9a2a1732e4249e7ee53af03ac68ed`** at 03:18:31; it had been `deebdf6a4c` at 02:58, and it moves by the hour.

| Patch | Author | At the pin (control): `git apply` / fuzz 0 / applied | At master: `git apply` / fuzz 0 / applied |
| --- | --- | --- | --- |
| `0001-Increase-glui-size` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (2 of 2 hunks) |
| `0001-Increase-ozone-size` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (2 of 2) |
| `0001-Increase-ozone-widget_size` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 1) |
| `0002-quit-not-restart` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 1) |
| `0003-fix-oga-no-preferred` | upstream | ok / ok / clean | ok / ok / offset |
| `0004-drm-resolution` | upstream | **FAIL / FAIL / fuzz** | FAIL / FAIL / fuzz |
| `0006-no-screen-brightness` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 2) |
| `0008-disable_search` | upstream | ok / ok / offset | ok / ok / offset |
| `0009-hide-wayland-checkerboard` | upstream | ok / ok / offset | ok / ok / offset |
| `0010-paths` | upstream | ok / ok / clean | FAIL / FAIL / **FAILED** (1 of 4) |
| `0011-cheevos-sounds` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 2) |
| `0011-video-thread-wrapper-serialise-posters` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (4 of 4); **upstream's own form of it is on master** (#19518, merged 2026-09-08) |
| `0012-cheevos-cmd` | upstream | ok / ok / offset | FAIL / FAIL / **FAILED** (1 of 1) |
| `0013-cheevos-offline-proxy-toast` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (`intl/msg_hash_fr.h`, `msg_hash.h`) |
| `0014-widgets-backdrop-follows-the-font` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (3 of 6) |
| `0015-video-thread-wrapper-run-a-command-once` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (2 of 2); **its defect is already fixed on master** (#19577, its author: *"master already fixes this"*) |
| `0016-widgets-message-queue-floor` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (2 of 4) |
| `0017-widgets-sharp-font-sizes` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (3 of 5) |
| `0018-auto-slot-survives-content-load` | **fork** | ok / ok / clean | FAIL / FAIL / **FAILED** (`runtime_file.c`, 1 of 2; #19223 changed `state_slot` there after the pin) |
| `0019-widgets-message-queue-keeps-its-place` | **fork** | ok / ok / clean | FAIL / FAIL / fuzz |
| `batteryplus/0001-batteryplus-capacity` | upstream | **FAIL** / ok / clean | FAIL / ok / offset |

**What it shows:**

- **The control holds.** The build's `patch -p1` applies all 21 at the pin, so the method reproduces the build.
- **One finding inside the control (F-10):** `0004-drm-resolution` applies to the pin only with fuzz, and `git apply` refuses it there.
- **Against master, a bump is a re-cut of the series, not a pin edit.** Fifteen patches fail outright, and two of the fork's (0011, 0015) are superseded by master's own fixes, so they are dropped, not rebased. Brief § 5 says the bump itself is a stream brief's decision; the punch list records it as `deferred:` with this table.
- A failure later in the series can be partly a consequence of an earlier one: several patches touch `gfx/gfx_widgets.c` and `configuration.c`. So each fork patch's master row is "does not apply to master as the build would meet it", not a hunk-exact rebase estimate.
- `git apply --check` refuses `batteryplus` at both refs while `patch` at fuzz 0 accepts it. The cause is not read here; the build uses `patch`, so it does not affect the build.

### F-10 (Q2): `0004-drm-resolution.patch` applies to the pin only with fuzz

At the pin, `patch -p1 --fuzz=0 --dry-run` refuses `0004-drm-resolution.patch` and `git apply --check` refuses it. The build's `patch -p1` (default fuzz 2) applies it, logging `with fuzz`. A patch that holds only by fuzz is the shape `150a4e1402` (2026-09-28, *"widget patches follow the drawn face and apply at fuzz 0"*) cured for the fork's widget patches: fuzz lets a patch land on the wrong lines when the context moves. Upstream-carried (ROCKNIX's patch); fix shape: refresh its context against the pin so it applies at fuzz 0, the same content. Proof: `q4c-patches.sh` at the pin reads `fuzz0=ok` for it. The build's own proof is an image, so `fix-pending-image`.

### `emulators/libretro/retroarch/package.mk` (153 lines, fork-own through `43d0bc3bf4`; read whole at `d606301784`)

History on the slice since the base: `43d0bc3bf4` (2026-10-07, the ARM compatibility roots renamed to `build.${DISTRONAME}`), plus two upstream merges. `upstream/next`'s copy differs only by that rename (F-09). Read line by line:

- **1 to 2, the header:** one line, `Copyright (C) 2024-present ROCKNIX`, the same as upstream's. No JELOS or LibreELEC line, and none is owed unless the recipe came from one. `git log --follow` reaches `9f1fab30f6` (2025-07-13, *"projects: add modifications for ROCKNIX"*, 14 commits in all) and no earlier. Q2 n/a.
- **10:** `libass` appears twice in `PKG_DEPENDS_TARGET`. Q7, cosmetic (upstream's).
- **17 to 24:** `arm) true` / `*) PKG_DEPENDS_TARGET+=" empty"`. `empty` is `projects/ROCKNIX/packages/tools/empty`, a placeholder dependency (upstream's idiom). Q7: a reader cannot tell why from the recipe.
- **26:** `batteryplus` only when `BATTERYPLUS_SUPPORT=yes` (Q4 (c) applies it last, as the build does).
- **66 to 76:** GLES only when both `OPENGLES_SUPPORT` and `PREFER_GLES` are `yes`, else full GL. GENERIC_X64 and SM8550 set `PREFER_GLES=no`, H700, RK3326 and RK3566 `yes` (their `options`).
- **92 to 98, Q1 (the brief's own lead):** three `make ...` followed by `[ $? -eq 0 ] && echo "(... ok)" || { echo "(... failed)" ; exit 1 ; }`. The build runs under `set -e` (`config/path:4`), so a failing `make` has already ended the function before the test: the test is dead in both branches. Fix shape: drop the three status lines (F-13).
- **106 to 114, F-11 below.**
- **117:** upstream's own `retroarch.cfg` goes to `/etc/retroarch.cfg`. `git grep -n -F '/etc/retroarch.cfg' -- projects packages distributions` (patches excluded) prints nothing, so no script of the tree reads it. RetroArch's own fallback reads it when started with no `--config`, and `runemu.sh` always passes one (302). So it is not reached on the launch path, and its one reader is a hand-started `retroarch`. Q6: kept as RetroArch's default reference; a row, no fix.
- **129 to 134:** a device with no `sources/<DEVICE>/` fails the build with `Configure retroarch for ${DEVICE}`, which is a guard that fails closed and says why. Q2 PASS.
- **137 to 138:** `.overlay` markers so the `tmp-*.mount` overlays have a lower directory. **147 to 153:** five mounts enabled (Q5: boot cost read with the units, group 1).

### F-11 (Q3): `retroarch32` is skipped silently whenever the ARM root's install directory is not exactly one

`package.mk` 106 to 112: on aarch64 the recipe installs `/usr/bin/retroarch32` only `if [ -f ${ROOT}/build.${DISTRONAME}-${DEVICE}.arm/install_pkg/retroarch-*/usr/bin/retroarch ]`. Two cases make that test false or an error (`[: too many arguments`), and the build then goes on without the 32-bit RetroArch and without saying so: no arm root at all (an aarch64 build run without its arm half), and two `retroarch-<pin>` install directories left in one root after a pin bump. Every 32-bit core (`pcsx_rearmed32`, `gpsp`, `desmume`, `runemu.sh` 268 to 279) then fails at launch, the same shape as F-08. **Today:** the glob also matches `retroarch-assets-*`, but the full path matches only the real binary. All four live arm roots on the host hold one `retroarch-bdba046fa6` install directory, and the H700 and SM8550 images carry `usr/bin/retroarch32` (14,159,572 and 14,683,872 bytes). So it is latent. Fix shape: on aarch64 with `ENABLE_32BIT=true`, require exactly one match and `exit 1` naming the path otherwise (the 129 to 134 guard's shape). Proof: a constructed arm root with zero and with two install directories, through the recipe's function in a sandbox (`fix-host-regen`'s method). Severity Medium (latent; its failure is silent and costs every 32-bit core).

### The per-device `retroarch.cfg` (fifteen sets; GENERIC_X64's fork-own, read whole for Q2, Q5, Q6, Q7)

**Keys the pinned RetroArch does not read (Q6, Q1).** The test, over every `.c`/`.h` of the pin's unpack in the M7 GENERIC_X64 root (`build/retroarch-bdba046fa6/`): a key is not read when it does not occur as a word anywhere in that source. Generated families are excluded (`input_*_btn|_axis|_mbtn`, `input_device_pN`, `input_libretro_device_pN`, `network_remote_enable_user_pN`, `input_playerN_*`), and a hotkey `input_<bind>` counts as read when `<bind>` occurs (RetroArch stringifies the bind names). The output is `q6-retroarch-cfg-keys-not-read.txt`. **GENERIC_X64: 24 of 855 keys; H700, RK3326, RK3566: 24 each; SM8550: 25; AMD64: 25.** GENERIC_X64's list:

- `check_firmware_before_loading`, `content_history_dir`, `content_show_add`, `cursor_directory`
- `emuelec_exit_to_kodi`, `video_oga_vertical_enable`: keys of the forks this tree descends from, never upstream RetroArch's
- `frame_time_counter_reset_after_fastforwarding`, `_after_load_state`, `_after_save_state`
- `input_duty_cycle`, `input_turbo_default_button`: the turbo keys, renamed
- `input_movie_record_toggle`, `input_send_debug_info`
- `menu_show_video_layout`, `video_layout_enable`, `video_layout_path`, `video_layout_selected_view`: the video-layout feature, retired
- `netplay_stateless_mode`, `playlist_cores`, `playlist_entry_remove`, `resampler_directory`
- `video_hdr_display_contrast`, `video_hdr_max_nits`, `video_scale_integer_overscale`

**This is a lower bound, not a list of every dead key.** `core_updater_buildbot_url` occurs as a word in the source and is still not read as a setting. `9fd73da845` (#307 PL-076) established that on 2026-09-28 by reading `configuration.c` 1683 to 1684 and dropped it from GENERIC_X64 alone. **The other fourteen profiles still carry it pointing at `.../linux/armhf/latest/`**, including the aarch64 H700, RK3326, RK3566 and SM8550 files (`grep core_updater_buildbot_url sources/*/retroarch.cfg`), which F-12 carries.

### F-12 (Q6, Q1): every shipped `retroarch.cfg` carries 24 or 25 keys the pinned RetroArch never reads, and the armhf core-updater URL on fourteen

The list above. RetroArch ignores an unknown key, so nothing breaks. What it costs:

- **A reader is misled about what is configured.** `content_history_dir` is blindspot 65's case: RetroArch 1.22 writes its history under `playlists/builtin/` (#306), and this key reads as if it set the place.
- **The renamed keys' values reach nothing.** The turbo pair and `video_hdr_*` probably have successor keys that sit at their defaults; whether the profiles' intent needs carrying to them is read key by key at fix time, from the pin's `configuration.c`.

**`content_history_dir` and `core_updater_buildbot_url` on GENERIC_X64 are the fork's lines**, and the rest are upstream's in all fifteen. Fix shape, the class #307 PL-076 set:

- remove the not-read keys from the GENERIC_X64 profile now;
- for the fourteen upstream profiles, remove them too, the same lines in every file, which D-UI-079 allows because nothing a player sees changes (RetroArch ignores them today);
- name each renamed key's successor and its current value in the commit.

Proof: the key test above reads 0 on the edited files, and a guest launch reads the same `retroarch.cfg` behaviour (`fix-guest-copy`). `Already written:` each device copies the profile to `/storage/.config/retroarch/retroarch.cfg` once (9fd73da845's own note), so existing devices keep the dead lines, harmlessly. Read both, nothing to migrate. Q1 / Q6, Low (`Renovation`).

**Q7, the fifteen files as copies:** compared by key and value (`python3 -I`, a dict per file), GENERIC_X64 against H700 differs in 89 keys (55 only in GENERIC_X64, 17 only in H700, 17 with different values). Against RK3326 and RK3566 it differs in 87; against SM8550 in 246. H700 against the other RK families differs in 20 to 33 lines; SM4450 equals SM8250 and SM8550 (0 changed lines) and differs from SM8650/SM8750 by 2. **So at least four of the fifteen are byte-for-byte copies of another** (SM4450, SM8250, SM8550, and SM8650 = SM8750 up to 2 lines), with no base file they derive from: a "diff against a base in disguise", the brief's Q7 question. Not changed here; a Q7 row for the coordinator (the files are upstream's, and folding them is a recipe change across devices the fork does not build).

### F-13 (Q1): RetroArch's `make_target` carries three status checks that `set -e` has made dead

`emulators/libretro/retroarch/package.mk` 92 to 98: each of the three `make` calls (RetroArch, `gfx/video_filters`, `libretro-common/audio/dsp_filters`) is followed by `[ $? -eq 0 ] && echo "(... ok)" || { echo "(... failed)" ; exit 1 ; }`. The recipe's functions run under `set -e` (`config/path:4`). A failing `make` therefore ends `make_target` before the next line, and a succeeding one prints a status the build log already carries. Fix shape: drop the three lines, behaviour unchanged. Proof: `pkgcheck retroarch` rc 0; the build log of the next image shows the three makes; `fix-pending-image`. Q1, Low (`Renovation`). Upstream's lines (#585 candidate).
