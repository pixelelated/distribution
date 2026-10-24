# Q4a -- upstream's commits on the membership since the base

Generated 2026-10-24 08:49 UTC (`date -u`) from `git log --reverse 8ebaf8daad..upstream/next -- projects/ROCKNIX/packages/emulators/standalone` (`upstream/next` = `e0f9deb899`): 38 commits, all after the read hash (the base `c445081a59` gives the same 38). **Overlap** is each touched file that exists at `8ebaf8daad` and that the fork changed since the base (`git diff --quiet c445081a59 8ebaf8daad -- <file>` false). For a merge commit the files are its first-parent diff. Dispositions: `to merge` (no overlap, or a different hunk -- taken with the base merge, class 1), `conflicts` (the same lines; resolved at the base merge as noted), `superseded` (none: no upstream commit here is already in the fork's tree by other means). Every row is taken by the base merge; none is cherry-picked by this slice (D-WORKFLOW-187: the base merge is the coordinator's).

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

38 rows: 33 to merge, 5 conflicts, 0 superseded.

## The thirteen fork-own recipes against upstream's

| Recipe | Fork's pin | Upstream's pin | Pin | What the fork changed (none of it the pin) |
| --- | --- | --- | --- | --- |
| `aethersx2-sa` | `1.5-3606` | (absent upstream) | differs | `PKG_ARCH=aarch64` (audit #258 PL-010); upstream deletes the recipe |
| `amiberry` | `5c54536997c0` | `5c54536997c0` | same | not built for GENERIC_X64 |
| `bigpemu-sa` | `v119` | `v119` | same | `PKG_ARCH=aarch64` |
| `daedalusx64-sa` | `f17e9ed86f38` | `f17e9ed86f38` | same | `DISTRONAME` for `DISTRO` in the arm root path |
| `dolphin-sa` | `6094cfcf7b8f` | `6094cfcf7b8f` | same | Python3 dep (dolphin-save-paths), GENERIC_X64 GL backend, the `sys` link, patch 018's note |
| `drastic-sa` | `1.0` | `1.0` | same | `PKG_ARCH=aarch64` |
| `duckstation-sa` | `0.1-10998` | `0.1-10998` | same | Python3/libcom-err deps; `install -m 0755` |
| `mupen64plus-sa-audio-sdl` | `cec70e42b453` | `cec70e42b453` | same | speexdsp dependency |
| `mupen64plus-sa-video-gliden64` | `85bdd452d709` | `85bdd452d709` | same | GENERIC_X64 arms, `-DNOHQ=On` |
| `openbor` | `b8303cce992a` | `b8303cce992a` | same | `PKG_LICENSE` (#528) |
| `ppsspp-sa` | `afbc66a318b8` | `afbc66a318b8` | same | per-device sources guarded |
| `steam` | `1.0.0.85` | `1.0.0.85` | same | Python3 dependency |
| `yabasanshiro-sa` | `a40dace1ae0a` | `a40dace1ae0a` | same | not built for GENERIC_X64 |

No fork-own recipe's pin differs from upstream's except `aethersx2-sa`'s, which upstream no longer has. The one `behind-upstream` pin in the membership is `azahar-sa` (upstream-carried: `fbd3fb02f7` against upstream's `219d743a1e`, v2126.2 by `5675ab7b28`), taken with the base merge. `dsperate-sa` differs too (2.0.1 against upstream's 3.0.5, four bumps); the scan classes it by its tag shape.
