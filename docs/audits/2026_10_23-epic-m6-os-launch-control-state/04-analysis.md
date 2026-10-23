# Audit Analysis — M6.P2 T1, the OS scripts: launch, control and state

**Date:** 2026-10-23
**Spec:** `docs/reviews/briefs/os-launch-control-state.md` v2; `docs/reviews/plan-for-the-plan.md` § 4
**Issues:** #648, #695, #339
**Commits:** read at `reviewed-at` `efadfea08a` (slice bytes = `8ebaf8daad`)

---

_Being written. § Renovation face Q6 was drafted during Phase 2 (08:02 UTC) so its search output is on disk before a compaction; the sections of the template follow after Phase 3._

## Renovation face

### Q6 Dead ends: one reachability row per script in `sources/scripts/` (47, `backuptool` excluded)

Search, per script name `<n>` (08:00 UTC, `.qa-scratch/t1/q6.tsv`): in the distribution, `grep -rlF --exclude-dir=.git "<n>" packages projects scripts tools config distributions`, less the script itself and the tools' own test fixtures; in the interface, `git -C /home/max/Development/emulationstation-next grep -lF "<n>" 16dbac5211eea7e70db7394372033be2be7df829 -- es-app es-core`. For the five names that are also ordinary words the raw count is noise, so the row cites a second search for the invocation. Units that `ExecStart` a script and the udev rule count as callers (they are in `projects/`). `unshipped` is not `unreached` (D-WORKFLOW-185).

| Script | Distribution hits | Interface hits | Callers (first few) | Verdict |
| --- | ---: | ---: | --- | --- |
| `amionline` | 0 | 0 | -  | **unreached** -- Already written: nothing (it writes nothing). Exposes: the command name `/usr/bin/amionline` only, for a person at a shell; it pings `www.google.com`, the reachability shape `rclone-cloud-sync.md` § Critical gotchas rejects. **Remove** (F-55). |
| `automount` | 24 | 1 | `distributions/LEIoT/options distributions/LibreELEC/options distributions/ROCKNIX/options packages/network/sam` ES: `es-app/src/guis/GuiMenu.cpp` | reached |
| `bezels.sh` | 0 | 0 | -  | **unreached** -- Already written: `/storage/.config/bezels_enabled` and `input_overlay` lines it wrote into `retroarch.cfg` on images from before the bezel project took over; nothing reads the marker (`grep -rlF bezels_enabled packages projects`: none). Exposes: the name only. **Remove**; the stale marker is inert (F-55). |
| `brightness` | 167 | 5 | `packages/addons/service/tvheadend43/source/defaults/comskip/comskip.ini packages/linux/patches/rockchip-old/ro` ES: `es-app/src/ApiSystem.cpp es-app/src/guis/GuiAnalogSticksLedControls.cpp es-app/src/guis/Gu` | reached: invoked by `autostart/006-display` and `sysutils/sleep/sources/sleep.sh` (`grep -rlE '/usr/bin/brightness|^\s*brightness |[;|&($] *brightness '`); the raw count (167) is the word in patches and docs |
| `chksysconfig` | 7 | 4 | `projects/ROCKNIX/packages/rocknix/autostart/001-setup projects/ROCKNIX/packages/rocknix/profile.d/001-function` ES: `es-app/src/main.cpp es-app/tests/unit/AtomicFileTests.cpp es-core/src/SystemConf.cpp` | reached |
| `controller-layout` | 0 | 1 | - ES: `es-app/src/guis/GuiMoonlight.cpp` | reached |
| `error.sh` | 0 | 0 | -  | **unreached** -- Already written: nothing. Exposes: the name; its `[ !-z ...]` (`:9`, SC1035) means it never shows the launch error it reads. **Remove** (F-55). |
| `factoryreset` | 2 | 1 | `projects/ROCKNIX/packages/hardware/quirks/devices/GameKiddy GKD Pixel2/bin/battery_led_status projects/ROCKNIX` ES: `es-app/src/guis/GuiMenu.cpp` | reached |
| `find.sh` | 0 | 0 | -  | **unreached** -- Already written: nothing. Exposes: the name; walks `/` with an unquoted glob. **Remove** (F-55). |
| `getfilters` | 0 | 1 | - ES: `es-app/src/guis/GuiMenu.cpp` | reached |
| `getoverlays` | 0 | 0 | -  | **unreached** -- Already written: nothing. Exposes: the name; the interface lists shaders and filters through `getshaders`/`getfilters` (`GuiMenu.cpp` at the pin) and not overlays through this. **Remove**, or wire it if the overlay list is meant to use it (F-55). |
| `getshaders` | 0 | 1 | - ES: `es-app/src/guis/GuiMenu.cpp` | reached |
| `handle-hdmi-hotplug` | 1 | 0 | `projects/ROCKNIX/packages/rocknix/system.d/hdmi-hotplug.service`  | reached |
| `installtointernal` | 0 | 0 | -  | **unreached** -- Typed at a shell by an owner of a Qualcomm device (F-39, F-40); **keep**, it is a tool, not a dead end. |
| `led_flash` | 1 | 0 | `projects/ROCKNIX/packages/sysutils/powerstate/sources/powerstate.sh`  | reached |
| `migrate_roms` | 0 | 0 | -  | **unreached** -- Already written: the pre-`games-*/roms` layout migration it performed by hand (`mv` + `rsync --remove-source-files`), on devices long since moved; its `1|>>${LOGFILE}` (`:13`, `:30`, SC2189) hands `mkdir` and `find` a stray `1` argument. **Remove** (F-55). |
| `paneladj` | 10 | 0 | `projects/ROCKNIX/packages/hardware/quirks/devices/Anbernic RG353P/040-display projects/ROCKNIX/packages/hardwa`  | reached |
| `rocknix-bluetooth` | 4 | 2 | `projects/ROCKNIX/packages/network/bluez/autostart/009-bluetooth projects/ROCKNIX/packages/network/bluez/system` ES: `es-app/src/ApiSystem.cpp es-app/tests/unit/MaskSecretsTests.cpp` | reached |
| `rocknix-bluetooth-agent` | 2 | 0 | `projects/ROCKNIX/packages/rocknix/sources/scripts/runemu.sh projects/ROCKNIX/packages/rocknix/system.d/bluetoo`  | reached |
| `rocknix-config` | 0 | 2 | - ES: `es-app/src/ApiSystem.cpp es-app/tests/unit/MaskSecretsTests.cpp` | reached |
| `rocknix-corekeep` | 2 | 0 | `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool projects/ROCKNIX/packages/sysutils/busybox/sysctl`  | reached |
| `rocknix-es-thebezelproject` | 0 | 1 | - ES: `es-app/src/ApiSystem.cpp` | reached |
| `rocknix-evidence` | 7 | 0 | `projects/ROCKNIX/packages/rocknix/package.mk projects/ROCKNIX/packages/rocknix/profile.d/001-functions project`  | reached |
| `rocknix-fake-suspend` | 2 | 0 | `projects/ROCKNIX/packages/rocknix/sources/post-update projects/ROCKNIX/packages/sysutils/system-utils/sources/`  | reached |
| `rocknix-info` | 1 | 1 | `projects/ROCKNIX/packages/emulators/libretro/retroarch/patches/batteryplus/0001-batteryplus-capacity.patch` ES: `es-app/src/ApiSystem.cpp` | reached |
| `rocknix-keyboard` | 0 | 1 | - ES: `es-app/src/guis/GuiMenu.cpp` | reached |
| `rocknix-memory-manager` | 2 | 0 | `projects/ROCKNIX/packages/rocknix/package.mk projects/ROCKNIX/packages/rocknix/system.d/rocknix-memory-manager`  | reached |
| `rocknix-report-stats` | 2 | 0 | `projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.service tools/rasteratops-identity-check`  | reached |
| `rocknix-retroachievements-info` | 0 | 0 | -  | **unreached** -- Already written: nothing. Exposes: the name; it scrapes retroachievements.org's HTML as of 2020 (`:6-13`) and reads `system.cfg` for the account, where the interface uses the RetroAchievements API. **Remove** (F-55). |
| `rocknix-scraper` | 0 | 1 | - ES: `es-app/src/ApiSystem.cpp` | reached |
| `rocknix-settings` | 2 | 0 | `projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-config projects/ROCKNIX/packages/rocknix/sources/scr`  | reached |
| `rocknix-systems` | 0 | 1 | - ES: `es-app/src/ApiSystem.cpp` | reached |
| `rocknix-update` | 1 | 1 | `tools/rasteratops-identity-check` ES: `es-app/src/ApiSystem.cpp` | reached |
| `run` | 864 | 126 | `config/arch.aarch64 config/docker/source/bin/docker config/functions config/options` ES: `es-app/src/ApiSystem.cpp es-app/src/CaptureRotation.cpp es-app/src/CheevosIndex.h` | reached: invoked by the interface (`GuiMenu.cpp:520`, the tools launch, F-20); the raw counts are the word |
| `runemu.sh` | 9 | 6 | `distributions/ROCKNIX/config/functions projects/ROCKNIX/packages/misc/modules/sources/Mount NFS.sh projects/RO` ES: `es-app/src/LaunchCommand.h es-app/src/main.cpp es-app/src/SaveState.cpp` | reached |
| `say` | 117 | 73 | `packages/addons/addon-depends/qt5/patches/0002-QSslSocket-make-it-work-with-OpenSSL-v4.patch packages/addons/f` ES: `es-app/src/ApiSystem.cpp es-app/src/ApiSystem.h es-app/src/CaptureRotation.cpp` | reached: invoked by `sysutils/powerstate/sources/powerstate.sh:67` (the audible battery alert; `espeak` is on the image); `chksysconfig` and `raofflineproxy-ctl` define their own `say()`; the raw counts are the word |
| `setemu.sh` | 0 | 0 | -  | **unreached** -- Already written: `/storage/.config/system/configs/emuoptions.conf` on old devices; nothing reads it (`grep -rlF emuoptions.conf`: none); its own comment says `This is no longer in use!` (`:3`). **Remove** (F-55). |
| `setrootpass` | 2 | 3 | `projects/ROCKNIX/packages/rocknix/autostart/007-rootpw projects/ROCKNIX/packages/rocknix/profile.d/001-functio` ES: `es-app/src/guis/GuiMenu.cpp es-app/tests/unit/MaskSecretsTests.cpp es-core/src/utils/Strin` | reached |
| `setsettings.sh` | 7 | 3 | `projects/ROCKNIX/packages/emulators/libretro/retroarch/patches/0013-cheevos-offline-proxy-toast.patch projects` ES: `es-app/src/guis/GuiMenu.cpp es-app/src/OfflineAchievementsText.h es-core/src/utils/Offline` | reached |
| `show_changelog` | 0 | 0 | -  | **unreached** -- Already written: nothing writes `/storage/.cache/changelog` (`grep -rlF .cache/changelog`: none), so it always exits at `:6-9`. Exposes: the name. **Remove** (F-55). |
| `suspendmode` | 14 | 1 | `projects/ROCKNIX/packages/hardware/quirks/devices/GameForce ACE/030-suspend_mode projects/ROCKNIX/packages/har` ES: `es-app/src/guis/GuiMenu.cpp` | reached |
| `timeinfo` | 1 | 2 | `projects/ROCKNIX/devices/RK3588/patches/linux/999-MALI-rockchip-upgrade-bifrost-DDK-to-g21p0-01eac0-fr.patch` ES: `es-app/src/guis/GuiMenu.cpp es-app/src/SystemScreenSaver.cpp` | reached: invoked by the interface, `GuiMenu.cpp:1859-1861` (`/usr/bin/timeinfo current_tim...`, `timezones`) |
| `updateabl` | 6 | 0 | `projects/ROCKNIX/devices/SM4450/bootloader/update.sh projects/ROCKNIX/devices/SM6115/bootloader/update.sh proj`  | reached |
| `usbgadget` | 4 | 1 | `projects/ROCKNIX/packages/rocknix/autostart/081-usbgadget projects/ROCKNIX/packages/rocknix/sources/scripts/ha` ES: `es-app/src/guis/GuiMenu.cpp` | reached |
| `vertical-check` | 1 | 0 | `projects/ROCKNIX/packages/wayland/compositor/sway/autostart/111-sway-init`  | reached |
| `volume` | 152 | 11 | `config/docker/source/resources/language/English/strings.po packages/addons/addon-depends/docker/moby/patches/0` ES: `es-app/src/guis/GuiControllersSettings.cpp es-app/src/guis/GuiKeyboardtopads.cpp es-app/sr` | reached: invoked by `autostart/050-audio` and `sysutils/system-utils` `input_sense`/`headphone_sense`; the raw count is the word |
| `wifictl` | 5 | 16 | `projects/ROCKNIX/packages/rocknix/autostart/080-network projects/ROCKNIX/packages/sysutils/sleep/sources/sleep` ES: `es-app/src/ApiSystem.cpp es-app/src/ApiSystem.h es-app/src/guis/GuiMenu.cpp` | reached |

Totals: 47 scripts; **9 unreached** by any caller (`amionline`, `bezels.sh`, `error.sh`, `find.sh`, `getoverlays`, `migrate_roms`, `rocknix-retroachievements-info`, `setemu.sh`, `show_changelog`), all present since the import `9f1fab30f6` (`git log --diff-filter=A`); 1 reached only by hand (`installtointernal`); 37 reached. Two further dead ends inside reached scripts: `automount`'s `start_overlay` (F-41) and `usbgadget`'s deprecated verbs (F-49). `engineering-practices.md` § Before deleting a duplicate applies before any removal: none of the nine is a duplicate of a survivor, and each row names what it wrote and exposed.

