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
