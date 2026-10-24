# Research notes — M6.P2 T30, the standalone emulators (#677)

## Scope

**Read hash:** `8ebaf8daad8eaac6331dff6fc048fb4411d7decb` (`next`). The branch at stage A is `c7e3dfcc87` (the dispatch's hash); `git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/standalone` is **empty**, so the membership's bytes are the hash's and every line number in these artifacts is the hash's (the export `.qa-scratch/t30/at-hash/`, `git archive 8ebaf8daad projects/ROCKNIX/packages/emulators/standalone`, 623 files) unless marked *branch*. `upstream/next` at the read: `e0f9deb899`; the merge base `c445081a59`.

**The filter** (brief § 2, run with `python3 -I` over `docs/reviews/inventory.json`, generated `2026-10-23T02:20:48Z` at P1's `eb4763e3cc`; the rows of `tree == distribution`, `area == emulators-and-cores`, path under `projects/ROCKNIX/packages/emulators/standalone/`, reach in `shipped`, `test`, `n/a`). Output, 08:19 UTC:

```
paths 543 lines 157365 {'fork-own': 55, 'upstream-carried': 488} {'shipped': 543}
fork-own lines 7421
read 105 lines 10695 fork-own read lines 3104
read by lang {'c': (1, 926), 'python': (2, 483), 'recipe': (47, 2651), 'shell': (55, 6635)}
languages {'symlink': 80, 'config': 277, 'recipe': 47, 'shell': 55, 'yaml': 9, 'other': 52, 'xml': 13, 'python': 2, 'c': 1, 'json': 2, 'image': 1, 'font': 1, 'none': 2, 'text': 1}
recipes 35
```

Every figure equals the brief's and #677's: **543 paths, 157,365 lines; 55 fork-own (7,421 lines), 488 upstream-carried; all `shipped`; 10,695 code-class lines in 105 files, 3,104 fork-own; 35 recipes; 47 `package.mk`; thirteen fork-own `package.mk`.** No delta.

**The tree against the membership.** `git ls-tree -r --name-only 8ebaf8daad -- projects/ROCKNIX/packages/emulators/standalone` lists 623 paths, of which 80 end in `.patch` (the `patches-and-configs` area's T42/T43 rows, read here only as their recipe's context). The other 543 equal the membership: `comm -3` of the two sorted lists, in the C locale, prints nothing (in an `en_US` shell `comm` refused the inputs as unsorted: Python sorts by codepoint, the same trap as T3's S2). 35 recipe directories at the top level.

**The 35 recipes:** `aethersx2-sa amiberry ares-sa armsx2-sa azahar-sa bigpemu-sa cemu-sa daedalusx64-sa dolphin-sa drastic-sa dsperate-sa duckstation-sa flycast-sa gopher64-sa gzdoom-sa hatarisa heroic hypseus-singe mednafen melonds-sa mupen64plus-sa nanoboyadvance-sa openbor pico-8 ppsspp-sa rpcs3-sa scummvm-sa skyemu-sa steam supermodel-sa touchhle-sa vice-sa vita3k-sa xemu-sa yabasanshiro-sa`. The 47 `package.mk` are these, `mupen64plus-sa`'s ten sub-recipes, `gzdoom-sa/zmusic` and `hatarisa/portaudio`.

**The thirteen fork-own `package.mk`** (the filter's output): `aethersx2-sa`, `amiberry`, `bigpemu-sa`, `daedalusx64-sa`, `dolphin-sa`, `drastic-sa`, `duckstation-sa`, `mupen64plus-sa/mupen64plus-sa-audio-sdl`, `mupen64plus-sa/mupen64plus-sa-video-gliden64`, `openbor`, `ppsspp-sa`, `steam`, `yabasanshiro-sa`.

**The start scripts.** 40 `start_*.sh` at the hash (the brief's list, by `git ls-tree`). `order.md:787` (its review table, not § T30) says "the 41 standalone `start_*.sh`". The 41st is `duckstation-sa/sources/Start Duckstation.sh`: a case-insensitive `start[_ ]*.sh` pattern counts 41. Both counts are recorded; they measure different patterns and do not disagree (#809's class, resolved).

**Upstream on the membership.** `git log c445081a59..upstream/next -- <standalone>`: 38 commits, all after `8ebaf8daad` (`git log 8ebaf8daad..upstream/next` lists the same 38). `git diff --stat upstream/next 8ebaf8daad -- <standalone>`: 144 files changed, 71,085 insertions, 1,034 deletions; most of that is `aethersx2-sa` (upstream's `c4d353449e` deletes it, and `GameIndex.yaml` is 62,331 lines). The fork's own commits on the membership since the base: 41. The 38 are tabled in `q4a-dispositions.md` (Phase 4). Two are exit-sweep leads before a line is read: `eeb33c5a37` (*fix quit hotkey targets for RPCS3, AetherSX2 and mupen64plus*) and `4a6415c033` (*duckstation-sa: point the quit hotkey at duckstation-qt*).

**Interacting subsystems (read-only context):** `runemu.sh` and `001-functions` (T1's: the standalone arms and the kill-name writer); `input_sense` (T1's: the `killall`); the `emulators` metapackage (T3's: the device arms and `mk_es_systems`); the quirks (T29's); the save layout (`cloud-sync-core`, #520); `tools/emulator-exit-test`.

### The device × recipe table

From the metapackage's arms (`projects/ROCKNIX/packages/virtual/emulators/package.mk:12-105` at the hash, T3's file), evaluated per device rather than transcribed: `env -i PATH=/usr/bin:/bin DEVICE=<d> ARCH=<a> ENABLE_32BIT=true bash -c '. <copy>; echo "$PKG_EMUS | 32: $EMUS_32BIT"'`, over a copy in `.qa-scratch/t30/meta/`. Cross-checked against the inventory's `reachable_by` for each `package.mk` (P1's dependency plans, transitive dependencies included): **the two agree for every recipe.** `daedalusx64-sa` reaches SM8550 only through `EMUS_32BIT` (the arm root). Non-member names in `PKG_EMUS` (`moonlight`, `wine`, `box64`, `portmaster`) are left out.

| Recipe | H700 | SM8550 | GENERIC_X64 (arm) |
| --- | :-: | :-: | :-: |
| `aethersx2-sa` | - | yes | - |
| `amiberry` | yes | yes | yes |
| `ares-sa` | - | yes | - |
| `armsx2-sa` | - | yes | - |
| `azahar-sa` | - | yes | - |
| `bigpemu-sa` | - | yes | - |
| `cemu-sa` | - | yes | - |
| `daedalusx64-sa` (32-bit) | - | yes | - |
| `dolphin-sa` | - | yes | yes |
| `drastic-sa` | yes | yes | - |
| `dsperate-sa` | yes | yes | - |
| `duckstation-sa` | yes | yes | yes |
| `flycast-sa` | yes | yes | yes |
| `gopher64-sa` | - | yes | - |
| `gzdoom-sa` | yes | yes | yes |
| `hatarisa` | yes | yes | yes |
| `heroic` | - | yes | - |
| `hypseus-singe` | yes | yes | yes |
| `mednafen` | yes | yes | - |
| `melonds-sa` | - | yes | - |
| `mupen64plus-sa` | yes | yes | yes |
| `nanoboyadvance-sa` | - | yes | - |
| `openbor` | yes | yes | yes |
| `pico-8` | yes | yes | yes |
| `ppsspp-sa` | yes | yes | yes |
| `rpcs3-sa` | - | yes | - |
| `scummvm-sa` | yes | yes | yes |
| `skyemu-sa` | - | yes | - |
| `steam` | - | yes | - |
| `supermodel-sa` | - | yes | - |
| `touchhle-sa` | yes | yes | yes |
| `vice-sa` | yes | yes | yes |
| `vita3k-sa` | - | yes | - |
| `xemu-sa` | - | yes | - |
| `yabasanshiro-sa` | yes | yes | yes |
| **35** | **17** | **35** | **15** |

The sub-recipes follow their parents (`mupen64plus-sa-simplecore` reaches GENERIC_X64 and SM8550, not H700). **GENERIC_X64's arms name fifteen recipes; the brief says the image carries thirteen** (twelve binaries and `pico-8`'s script). `amiberry` and `yabasanshiro-sa` are named by the arm and not on the brief's list: a Q6 lead for the image-set check (stage B), not a finding yet.

### The fork-own paths

| Path | Language | Lines | Last fork commit |
| --- | --- | ---: | --- |
| `aethersx2-sa/config/GENERIC_X64` | symlink | 1 | `cbdb91a517` |
| `aethersx2-sa/package.mk` | recipe | 55 | `efb8aec861` |
| `amiberry/package.mk` | recipe | 46 | `43227905ea` |
| `armsx2-sa/scripts/cheevos_armsx2.sh` | shell | 131 | `a78a72269f` |
| `azahar-sa/config/GENERIC_X64` | symlink | 1 | `cbdb91a517` |
| `bigpemu-sa/package.mk` | recipe | 34 | `efb8aec861` |
| `cemu-sa/config/GENERIC_X64/controllerProfiles` | symlink | 1 | `cbdb91a517` |
| `cemu-sa/config/GENERIC_X64/settings.xml` | xml | 110 | `cbdb91a517` |
| `daedalusx64-sa/package.mk` | recipe | 43 | `43d0bc3bf4` |
| `dolphin-sa/config/GENERIC_X64/Dolphin.ini` | config | 154 | `811573dd4e` |
| `dolphin-sa/config/GENERIC_X64/GFX.ini` | config | 62 | `cbdb91a517` |
| `dolphin-sa/config/GENERIC_X64/GamecubeControllerProfiles` | symlink | 1 | `811573dd4e` |
| `dolphin-sa/config/GENERIC_X64/Hotkeys.ini` | config | 1 | `811573dd4e` |
| `dolphin-sa/config/GENERIC_X64/WiiControllerProfiles` | symlink | 1 | `811573dd4e` |
| `dolphin-sa/package.mk` | recipe | 120 | `6616cc36cb` |
| `dolphin-sa/scripts/cheevos_dolphin.sh` | shell | 148 | `f8636de1d1` |
| `dolphin-sa/scripts/dolphin-save-paths` | python | 346 | `-` |
| `dolphin-sa/scripts/start_dolphin_gc.sh` | shell | 478 | `f8636de1d1` |
| `dolphin-sa/scripts/start_dolphin_wii.sh` | shell | 442 | `f8636de1d1` |
| `drastic-sa/config/GENERIC_X64/drastic.cfg` | config | 111 | `cbdb91a517` |
| `drastic-sa/package.mk` | recipe | 48 | `efb8aec861` |
| `duckstation-sa/config/AMD64/settings.ini` | config | 316 | `e6645cb5ea` |
| `duckstation-sa/config/GENERIC_X64` | symlink | 1 | `cbdb91a517` |
| `duckstation-sa/config/H700/settings.ini` | config | 200 | `e6645cb5ea` |
| `duckstation-sa/config/InputPlumber/settings.ini` | config | 273 | `e6645cb5ea` |
| `duckstation-sa/config/RK3326/settings.ini` | config | 269 | `e6645cb5ea` |
| `duckstation-sa/config/RK3399/settings.ini` | config | 248 | `e6645cb5ea` |
| `duckstation-sa/config/RK3566/settings.ini` | config | 246 | `e6645cb5ea` |
| `duckstation-sa/config/RK3588/settings.ini` | config | 248 | `e6645cb5ea` |
| `duckstation-sa/config/S922X/settings.ini` | config | 323 | `e6645cb5ea` |
| `duckstation-sa/config/SM4450/settings.ini` | config | 273 | `e6645cb5ea` |
| `duckstation-sa/package.mk` | recipe | 36 | `e6645cb5ea` |
| `duckstation-sa/scripts/duckstation_screenshot_path` | python | 137 | `e6645cb5ea` |
| `duckstation-sa/scripts/start_duckstation.sh` | shell | 135 | `e6645cb5ea` |
| `duckstation-sa/sources/Start Duckstation.sh` | shell | 36 | `e6645cb5ea` |
| `flycast-sa/config/GENERIC_X64/emu.cfg` | config | 21 | `7c8ba04368` |
| `flycast-sa/config/GENERIC_X64/mappings` | symlink | 1 | `cbdb91a517` |
| `melonds-sa/config/GENERIC_X64` | symlink | 1 | `cbdb91a517` |
| `melonds-sa/scripts/cheevos_melonds.sh` | shell | 104 | `5f00ab7c26` |
| `mupen64plus-sa/mupen64plus-sa-audio-sdl/package.mk` | recipe | 77 | `c474af4c05` |
| `mupen64plus-sa/mupen64plus-sa-core/config/GENERIC_X64/mupen64plus.cfg` | config | 664 | `7c8ba04368` |
| `mupen64plus-sa/mupen64plus-sa-core/scripts/start_mupen64plus.sh` | shell | 211 | `9f1d126d24` |
| `mupen64plus-sa/mupen64plus-sa-input-sdl/config/GENERIC_X64` | symlink | 1 | `cbdb91a517` |
| `mupen64plus-sa/mupen64plus-sa-video-gliden64/package.mk` | recipe | 84 | `e7166ee63d` |
| `nanoboyadvance-sa/config/GENERIC_X64/keymap.toml` | config | 18 | `cbdb91a517` |
| `openbor/package.mk` | recipe | 33 | `63a2090a56` |
| `ppsspp-sa/package.mk` | recipe | 108 | `e424886341` |
| `ppsspp-sa/scripts/cheevos_ppsspp.sh` | shell | 131 | `759b65b5c5` |
| `rpcs3-sa/config/GENERIC_X64/GuiConfigs/CurrentSettings.ini` | config | 17 | `cbdb91a517` |
| `rpcs3-sa/config/GENERIC_X64/config.yml` | yaml | 244 | `cbdb91a517` |
| `rpcs3-sa/config/GENERIC_X64/input_configs` | symlink | 1 | `cbdb91a517` |
| `steam/package.mk` | recipe | 38 | `-` |
| `supermodel-sa/config/GENERIC_X64/Supermodel.ini` | config | 472 | `cbdb91a517` |
| `xemu-sa/config/GENERIC_X64/xemu.toml` | config | 37 | `cbdb91a517` |
| `yabasanshiro-sa/package.mk` | recipe | 83 | `43227905ea` |

55 rows, 7421 lines.
