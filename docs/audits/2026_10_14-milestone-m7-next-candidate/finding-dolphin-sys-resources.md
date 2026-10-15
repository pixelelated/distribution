# Dolphin immutable Sys resources are absent from the compiled path

**Status:** confirmed source/package defect in frozen fac608; no fix integrated by auditor.
**Severity:** Medium. Four observed missing achievement badge assets; wider system-resource consumers also resolve the absent path, but their individual runtime effects have not been measured.
**Related criteria:** AC059/061/063/064/096/102/103; #575 and #584 integration. This is a separate defect from the NoGUI lifecycle omission.

## Primary evidence

The built Dolphin source root is `m7-p5-build-20261014-02/build.pixelelated-GENERIC_X64.x86_64/build/dolphin-sa-6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4`.

- Its `CMakeLists.txt:174–175` defines DATA_DIR from `${CMAKE_INSTALL_FULL_DATADIR}/dolphin-emu`; `:857` normally installs Data/Sys into `${datadir}/sys`. The original relink compile argv in `docs/qa-logs/2026-10-15-dolphin-startup-result/build/original-records.tar.gz`, member `stage/container-result.json`, contains `-DDATA_DIR="/usr/share/dolphin-emu/"`.
- `Source/Core/Common/FileUtil.cpp:762–790` resolves Linux `GetSysDirectory()` to DATA_DIR + `sys/`. LINUX_LOCAL_DEV is OFF in the recipe. The `-u` option affects user paths, not this immutable system path.
- Frozen `projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk:89–97` overrides installation and copies `Data/Sys/*` only to `/usr/config/dolphin-emu`, then adds device configuration and Triforce files. It never invokes upstream's Sys install rule.
- Auditor directly inspected frozen `build.pixelelated-GENERIC_X64.x86_64/image/system/usr`: `share/dolphin-emu` and `share/dolphin-emu/sys` do not exist and are not symlinks; `config/dolphin-emu/Resources/achievements_game.png` exists. Source Data/Sys contains all four named PNGs.
- Original `startup/guest-records.tar.gz`, members `native-owner/case/candidate-{enabled,disabled,failed-boot}/stderr`, logs failed default player/game/unlocked/locked badge loads at AchievementManager.cpp:892/902/912/922. `Init()` calls `LoadDefaultBadges()` before the enabled check, explaining disabled-case errors. The baseline NoGUI omits Init altogether, so its lack of those messages is not evidence the resource path works.

## Defect shape and other consumers

All immutable consumers use the same `File::GetSysDirectory()` root. Primary source reads establish:

| Site | Effect supported by source | Classification |
| --- | --- | --- |
| AchievementManager.cpp:885 | Four fallback achievement badges | FIX-NOW; original failed reads observed |
| AchievementManager.cpp:105 | Approved game-settings JSON; failure returns empty object | FIX-NOW through shared path; no hardcore qualification claim |
| ConfigLoaders/GameConfigLoader.cpp:191; ConfigManager.cpp:534/550 | Shipped global per-game INIs; local settings are loaded separately | FIX-NOW through shared path; specific game behavior not measured |
| VideoCommon/OnScreenUI.cpp:89 | Bundled OSD font | Same root; effect not separately exercised |
| DolphinQt/Resources.cpp:66; Common/FileUtil.cpp:1021/1026 | Qt resources and built-in themes | Same root; Qt startup not requalified here |
| InputCommon/InputConfig.cpp:158; Core/TitleDatabase.cpp:54/57; Core/WiiRoot.cpp:329 | Built-in profiles, title names, and Wii seed files | Same root; individual effects not asserted |
| DSP/font/graphics-mod/shader readers from `rg -n 'GetSysDirectory\(' Source/Core --glob '*.cpp'` | Other system resources | Same root; no duplicate per-consumer patches recommended |

## History, adoption, and ownership

`git log -S 'Data/Sys' -- projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk` locates the packaging layout at inherited `9f1fab30f6` (`projects: add modifications for ROCKNIX`). The latest observed upstream snapshot, fetched 2026-10-15T00:06:51Z and retained inside `docs/qa-logs/2026-10-15-dolphin-nogui-lifecycle/source-packet.tar.gz`, binds ROCKNIX next `c17558d2abadebec634100264523aaddc98b3b96`; its `source/upstream/rocknix-package.mk` has the same overridden copy into `/usr/config/dolphin-emu`. Upstream Dolphin already specifies the proper Sys install destination, so this repair belongs to distribution packaging, not a new Dolphin API or a per-resource loader fork. Current remote state beyond that dated snapshot was not queried by this auditor.

Literal negative search: `rg -n 'usr/share/dolphin|dolphin-emu/sys|dolphin-emu/Sys|Data/Sys|SYSDATA_DIR|DOLPHIN_EMU_USERPATH' projects/ROCKNIX packages distributions scripts` on frozen fac608 returned only the Dolphin recipe's Data/Sys copy (and unrelated azahar paths). `git ls-files '*dolphin*'` found no overlay that supplies the missing Sys link. Direct staged-tree reads independently confirm absence, so this is not inferred solely from a text search.

## Minimal correction and bounded check

Inside `makeinstall_target`, expose immutable `/usr/config/dolphin-emu` as `/usr/share/dolphin-emu/sys`, using a relative symlink if keeping the existing shared template layout. Alternatively install Data/Sys directly to the compiled destination; avoid duplicate writable state or redirecting Sys into retained `/storage`. Keep all player configuration and save-path logic unchanged. This should need package installation/image assembly, not a changed Dolphin compile input.

Run pkgcheck and a staged-tree assertion resolving the actual link within the candidate image root: all four badge hashes, the approved-settings JSON, and a representative shipped GameSettings INI must match the accepted source/template bytes. Then extend only the already-planned native startup receipt to assert the four prior badge failures are absent and enabled/disabled/failed-boot lifecycle behavior remains correct. No real account, award, extra gameplay matrix, or physical device is required for this defect. A complete native gameplay/save result remains a separate open criterion.
