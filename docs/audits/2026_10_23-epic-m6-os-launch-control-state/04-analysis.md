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
| `rocknix-scraper` | 0 | 1 | - ES: `es-app/src/ApiSystem.cpp` | **unreached in effect** -- its one caller is `ApiSystem::scrape` (`ApiSystem.cpp:308`), whose one caller is `GuiAutoScrape.cpp:93`, a page nothing opens (`git -C $ES grep -n GuiAutoScrape $PIN -- es-app/src`, outside its own files: none); it runs `sselph-scraper`, absent from the image and shipped by no package. Already written: nothing. Exposes: the name. **Remove** with the dead page's call, or leave both as upstream's (F-66). |
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

Totals: 47 scripts; **9 unreached** by any caller, **1 unreached in effect** (`rocknix-scraper`, through a page nothing opens) (`amionline`, `bezels.sh`, `error.sh`, `find.sh`, `getoverlays`, `migrate_roms`, `rocknix-retroachievements-info`, `setemu.sh`, `show_changelog`), all present since the import `9f1fab30f6` (`git log --diff-filter=A`); 1 reached only by hand (`installtointernal`); 36 reached. Two further dead ends inside reached scripts: `automount`'s `start_overlay` (F-41) and `usbgadget`'s deprecated verbs (F-49). `engineering-practices.md` § Before deleting a duplicate applies before any removal: none of the nine is a duplicate of a survivor, and each row names what it wrote and exposed.


### Q4 Package currency: every upstream commit on the package since the merge base

The package has no upstream tarball (`PKG_VERSION=""`), so currency is ROCKNIX's own copies of these files. `git log --format='%h|%ad|%p|%s' --name-only c445081a59..8b70f693b8 -- projects/ROCKNIX/packages/rocknix/` (`upstream/next` = `8b70f693b8`, fetched 07:05 UTC): **43 commits, 11 of them merges** (dispositioned `merge`: their content is the commits listed beside them). "To merge" means `next` should take it when it next levels with `upstream/next` (`release-candidates.md` step 0, the M7 lane's); "with care" names a conflict or a launch-path change. ROCKNIX's `wifictl` refactor (PR #3394, #316) is inside the merge base, not in this range: the fork's `wifictl` is the merged design D-UI-118 decided.

| Commit | Date | Subject | Files | Disposition |
| --- | --- | --- | --- | --- |
| `a94a2e0bde` | 2026-10-23 | emulationstation: batteryplus calibration reset | `sources/scripts/factoryreset` | **to merge** (adds a verb; `factoryreset` is fork-changed (#119/#307), so a conflict to resolve by hand) |
| `b011b5144f` | 2026-10-22 | emulationstation: hide cursor setting | `sources/post-update`, `sources/scripts/runemu.sh` | **to merge with care**: both files fork-changed, and `runemu.sh` carries the M7 delta |
| `09ce29c548` | 2026-10-19 | Merge pull request #3534 from sunshineinabox/PR_ASX2 | - | merge (its content is the commits it brings) |
| `c4d353449e` | 2026-10-18 | aethersx2: drop package due to licensing concern | `sources/scripts/factoryreset`, `sources/scripts/rocknix-systems` | **to merge** (licensing; also makes `post-update:153-156`'s aethersx2 BIOS copy moot) |
| `38cc9c7e7d` | 2026-10-17 | rk3566: fix some inputplumber issues | `sources/post-update`, `sources/scripts/factoryreset` | **to merge** (RK3566; shared files) |
| `68bff3f07a` | 2026-10-15 | Merge pull request #3510 from sydarn/yabadabadoo | - | merge (its content is the commits it brings) |
| `8704addb6b` | 2026-10-15 | yabadabadoo: add new Saturn emulator for low end platforms | `sources/scripts/runemu.sh` | **to merge** (a new emulator branch in `runemu.sh`'s dispatch) |
| `2707ea7e27` | 2026-10-15 | Merge pull request #3503 from beebono/sm4450-install | - | merge (its content is the commits it brings) |
| `71d8932b33` | 2026-10-14 | openabl: introduce package | `sources/scripts/updateabl` | **to merge**, read against F-67 (does it change the ABL write?) |
| `2d3f874ecd` | 2026-10-14 | installtointernal: allow RG55G1 in SM4450 | `sources/scripts/installtointernal` | **to merge** (SM4450) |
| `a1ea79474b` | 2026-10-10 | rk3566: port to inputplumber | `sources/post-update`, `sources/scripts/factoryreset` | **to merge** (RK3566; shared files) |
| `cb4b9e8e11` | 2026-10-11 | rocknix: set default wifi country | `config/system/configs/system.cfg` | **to merge** (`wifi.country` default; the fork's Wi-Fi work reads it, `wifictl:61`) |
| `2898e4947a` | 2026-10-11 | Merge pull request #3434 from Jacob-Matthew-Cook/zram-memory-management | - | merge (its content is the commits it brings) |
| `115a89be2b` | 2026-10-10 | Merge pull request #3468 from qzydustin/setting-keys | - | merge (its content is the commits it brings) |
| `abfdcfb57f` | 2026-10-10 | SM8550/SM8750: add RP6 and Odin 3 display refresh rate calibration | `sources/scripts/rocknix-panel-calibration` | **to merge** (SM8550 panel calibration, a shipped device; a new script) |
| `ce8f17d48b` | 2026-10-10 | Merge pull request #3454 from qzydustin/usbgadget-stop-shell | - | merge (its content is the commits it brings) |
| `f7d9c1f540` | 2026-10-10 | Merge pull request #3446 from qzydustin/usbgadget-boot-settle | - | merge (its content is the commits it brings) |
| `03204074ef` | 2026-10-08 | Merge pull request #3475 from sunshineinabox/PR_ToolCompat | `sources/scripts/handle-hdmi-hotplug`, `sources/scripts/rocknix-config`, `sources/scripts/rocknix-retroachievements-info`, `sources/scripts/updateabl` | **to merge** (tool compatibility across four scripts the slice read; compare with F-64's `rocknix-config` gaps) |
| `2d34256719` | 2026-10-08 | Merge pull request #3464 from sunshineinabox/PR_QuitHotkey | - | merge (its content is the commits it brings) |
| `72a96e2d8b` | 2026-10-07 | script: address feedback | `sources/scripts/rocknix-fake-suspend` | **to merge** |
| `cdbf28938a` | 2026-10-07 | rocknix: pass the auto frame delay and VRR options to RetroArch | `sources/scripts/setsettings.sh` | **to merge** (RetroArch half; adds keys, no conflict with F-09/F-10's lines expected but to check) |
| `0ebba6b301` | 2026-10-07 | rocknix: pass the AI service pause option to RetroArch | `sources/scripts/setsettings.sh` | **to merge** (RetroArch half) |
| `4e3972d037` | 2026-10-07 | rocknix: fix two keys in the default system.cfg | `config/system/configs/system.cfg` | **to merge: resolves F-45** (`ngpc.intergerscale` to `integerscale`) **and a key this audit missed** (`global.retroachievements.soundenable=0` to `global.retroachievements.sound=none`; `setsettings.sh:498` reads `.sound`) |
| `6aa745572b` | 2026-10-06 | usbgadget: fix usb_stop running in a subshell | `sources/scripts/usbgadget` | **to merge: resolves F-49's cause** (`usb_stop`'s `( )` to `{ }`) |
| `ee8cda0090` | 2026-10-05 | usbgadget: fix the gadget network not coming up at boot | `sources/scripts/usbgadget` | **to merge** |
| `e1b7d1f82f` | 2026-10-03 | rocknix-memory-manager: support the ES ZRAM menu | `sources/scripts/rocknix-memory-manager`, `system.d/rocknix-memory-recompress.service`, `system.d/rocknix-memory-recompress.timer`, `system.d/timers.target.wants/rocknix-memory-recompress.timer` | **to merge** (adds `rocknix-memory-recompress` service and timer; the interface's ZRAM menu calls the manager after it, so F-52's `eval` gains a caller: re-read F-52 then) |
| `48b98a02d7` | 2026-09-27 | sm6115: initial Retroid Pocket Duo Lite support | `sources/scripts/vertical-check` | **to merge** (SM6115) |
| `82000b31d3` | 2026-10-06 | installtointernal: handle qcom-spec partition tables | `sources/scripts/installtointernal` | **to merge**, read against F-39/F-40 |
| `54d72565ce` | 2026-10-05 | rocknix-fake-suspend: stop a pending suspend before resuming | `sources/scripts/rocknix-fake-suspend` | **to merge** |
| `18aded5898` | 2026-10-05 | Merge pull request #3449 from sunshineinabox/PR_FixMelonDSPostUpdate | `sources/post-update` | **not applicable as written**: the fork fixed the same melonDS post-update reset its own way (#526, `post-update:204-251`, `tools/melonds-upgrade-test` 15 PASS); compare before taking either |
| `32ebcdbf1b` | 2026-10-05 | rocknix: keep Steam alive when one of its processes is OOM-killed | `sources/scripts/runemu.sh` | **to merge with care** (`runemu.sh`, the launch path; Steam only) |
| `c1ee20e954` | 2026-10-05 | rocknix: set up zram swap before oomd starts | `system.d/rocknix-memory-manager.service` | **to merge** (unit ordering) |
| `54acd9556f` | 2026-10-05 | systemd: ship the distro sysctls in the image, drop dead keys | `sources/post-update` | **to merge**, compared with D-SYS-007's one-line `vm.laptop_mode` removal (`post-update:89-104`) so the two do not fight |
| `9234c39496` | 2026-10-05 | Merge pull request #3432 from sunshineinabox/PR_FastSettings | - | merge (its content is the commits it brings) |
| `25903bb59c` | 2026-10-04 | rocknix: look up settings without fork and use flock | `profile.d/001-functions` | **split**: the `get_setting` half **to merge** (a literal match through a quoted `=~`, so it **resolves F-21**, and no fork per lookup, Q5); the lock half (`flock` on `/tmp/.system.cfg.lock`) **not applicable**: the fork's lock is pid-only and shared with the interface's `PidLock`, which reads the pid (D-INFRA-012, `001-functions:188-232`) |
| `dc14669f69` | 2026-10-03 | systemd: set THP policy with tmpfiles and MemoryTHP | `sources/scripts/rocknix-memory-manager` | **to merge** (THP by tmpfiles; `rocknix-memory-manager` then stops writing it) |
| `bb9e42e2a0` | 2026-10-03 | rocknix: run games in games.slice with oomd and freeze on suspend | `sources/scripts/rocknix-fake-suspend`, `sources/scripts/rocknix-games-freeze`, `sources/scripts/runemu.sh`, `system.d/rocknix-report-stats.service` | **to merge with care**: games in `games.slice` with oomd and a freeze on suspend changes the launch path (`runemu.sh`) -- measure time to play before and after (`time-to-play.md`) |
| `a98a3066f5` | 2026-10-03 | systemd: persist timesyncd clock and reboot on PID1 crash | `sources/scripts/rocknix-memory-manager` | **to merge** |
| `4840b3e2a2` | 2026-10-03 | Merge pull request #3303 from Jacob-Matthew-Cook/dwc2-usb-fixes | - | merge (its content is the commits it brings) |
| `8628890fec` | 2026-09-11 | dwc2: fix resume crash, suspend hang, and vbus leak on role switch | `sources/scripts/usbgadget` | **to merge** (dwc2 role-switch fixes; F-50's file) |
| `e181700da7` | 2026-10-02 | Merge pull request #3393 from porschemad911/input-sense-touchscreen | - | merge (its content is the commits it brings) |
| `0c43a50420` | 2026-10-01 | Merge pull request #3377 from sunshineinabox/PR_RotScaling | `profile.d/001-functions`, `sources/scripts/runemu.sh` | **to merge with care**: rotation scaling in `001-functions` and `runemu.sh`, where the fork's rotation records live (#280, #288) |
| `f4fc3dc419` | 2026-10-01 | system-utils: input_sense: add touchscreen toggle | `sources/scripts/rocknix-touchscreen` | **to merge** (a new `rocknix-touchscreen` script) |

Totals: 11 merges; 32 commits: 26 to merge (`abfdcfb57f` among them, a new script for the shipped SM8550), 4 to merge with care (`b011b5144f`, `32ebcdbf1b`, `bb9e42e2a0`, `0c43a50420`), 1 split (`25903bb59c`), 1 not applicable as written (`18aded5898`); 26 + 4 + 1 + 1 = 32, counted from the table's rows. **Three of this audit's findings are already fixed upstream** (F-21 by `25903bb59c`'s lookup, F-45 by `4e3972d037`, F-49's cause by `6aa745572b`); their stream is a merge, not a fork patch (D-WORKFLOW-164's queue, #585, the other way round).

