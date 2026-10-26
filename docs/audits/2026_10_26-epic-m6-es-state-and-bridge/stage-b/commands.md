| Line | Function | Executor | First literal | Joined from outside | Quoting | Output read | Exit read | Thread | Branch | Script | Ships at 8ebaf8daad |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 183 | `setOverscan` | `executeScript` | `rocknix-config overscan ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-config` | yes |
| 191 | `setOverclock` | `executeScript` | `batocera-overclock set ` | mode) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-overclock` | no |
| 197 | `areCpuMitigationsEnabled` | `executeScript` | `batocera-mitigations status` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-mitigations` | no |
| 207 | `setCpuMitigationsEnabled` | `executeScript` | `batocera-mitigations ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-mitigations` | no |
| 218 | `updateSystem` | `popen` | `rocknix-update` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-update` | yes |
| 250 | `backupSystem` | `popen` | `rocknix-sync sync ` | device | bare | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-sync` | no |
| 279 | `installSystem` | `popen` | `batocera-install install ` | architecture, device | bare | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-install` | no |
| 308 | `scrape` | `popen` | `rocknix-scraper` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-scraper` | yes |
| 344 | `ping` | `executeScript` | `timeout 5 sh -c 'ping -c 1 -W 2 -t 255 8.8.8.8 \|\| ping -c 1 -W 2 -t ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `ping` | base tool |
| 350 | `torrentIsReadyForUpdate` | `popen` | `batocera-upgrade-torrent --is-file-ready-to-update` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-upgrade-torrent` | no |
| 368 | `torrentStatus` | `executeEnumerationScript` | `batocera-upgrade-torrent --status` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-upgrade-torrent` | no |
| 381 | `torrentUpdateSystem` | `popen` | `batocera-upgrade-torrent --upgrade` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-upgrade-torrent` | no |
| 411 | `canLocalUpdate` | `popen` | `batocera-upgrade --check-media-upgrade` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-upgrade` | no |
| 429 | `canArchitectureUpdate` | `popen` | `batocera-architecture-compatibility` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `batocera-architecture-compatibility` | no |
| 458 | `canUpdate` | `popen` | `rocknix-update check` | - | none joined | fgets in the caller | WEXITSTATUS without WIFEXITED | the caller's |  | `rocknix-update` | yes |
| 511 | `launchControlcenter` | `system` | `batocera-controlcenter` | - | none joined | none (inherits stdout) | the caller's | the caller's |  | `batocera-controlcenter` | no |
| 524 | `launchKodi` | `system` | `batocera-kodi ` | commandline | bare | none (inherits stdout) | WIFEXITED then WEXITSTATUS | the caller's |  | `batocera-kodi` | no |
| 573 | `launchCloudSignIn` | `system` | `` | phoneKeyboard | a variable: the command built earlier | none (inherits stdout) | the caller's | the caller's |  | `-` | - |
| 584 | `launchCloudSignIn` | `system` | `/usr/bin/cloud_oauth wait` | - | none joined | none (inherits stdout) | WIFEXITED then WEXITSTATUS | the caller's |  | `/usr/bin/cloud_oauth` | yes |
| 593 | `launchCloudSignIn` | `system` | `/usr/bin/cloud_oauth close` | - | none joined | none (inherits stdout) | the caller's | the caller's |  | `/usr/bin/cloud_oauth` | yes |
| 606 | `launchFileManager` | `system` | `filemanagerlauncher` | - | none joined | none (inherits stdout) | WIFEXITED then WEXITSTATUS | the caller's |  | `filemanagerlauncher` | binary: the window's ls |
| 627 | `enableWifi` | `executeScript` | `timeout 30 wifictl enable` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 635 | `enableWifi` | `executeScript` | `timeout 150 wifictl connect ` | Utils::String::shellQuote(country)), Utils::String::shellQuo | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 642 | `enableWifi` | `executeScript` | `wifictl enable ` | Utils::String::shellQuote(key)), Utils::String::shellQuote(s | shellQuote | none (system) | system() == 0 (:2328) | the caller's | WIN32 only | `wifictl` | yes |
| 651 | `getWifiSecurity` | `executeScript` | `timeout 15 wifictl security ` | Utils::String::shellQuote(ssid) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 660 | `connectOpenWifi` | `executeScript` | `timeout 120 wifictl connect-open ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 665 | `disableWifi` | `executeScript` | `timeout 30 wifictl disable` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 677 | `getCurrentWifiSsid` | `executeScript` | `timeout 10 wifictl current` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 690 | `getSavedWifiNetworks` | `executeScript` | `timeout 15 wifictl saved --ssid` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 714 | `joinWifiNetwork` | `executeScript` | `timeout 120 wifictl join ` | Utils::String::shellQuote(name) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 728 | `forgetWifiNetwork` | `executeScript` | `timeout 30 wifictl forget ` | Utils::String::shellQuote(name) | shellQuote | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `wifictl` | yes |
| 763 | `isWifiAPModeSupported` | `executeScript` | `timeout 10 wifictl has_ap_mode` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 767 | `getSavedWifiNetworks` | `executeEnumerationScript` | `wifictl list_saved` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `wifictl` | yes |
| 771 | `forgetWifiNetwork` | `executeScript` | `wifictl forget_saved ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 775 | `connectSavedWifiNetwork` | `executeScript` | `wifictl connect_saved ` | Utils::String::shellQuote(ssid)) | shellQuote | none (system) | system() == 0 (:2328) | the caller's |  | `wifictl` | yes |
| 780 | `enableBluetooth` | `executeScript` | `rocknix-bluetooth enable 2>&1 >/dev/null` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 785 | `disableBluetooth` | `executeScript` | `rocknix-bluetooth disable` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 790 | `startBluetoothLiveDevices` | `executeScript` | `rocknix-bluetooth live_devices` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-bluetooth` | yes |
| 795 | `stopBluetoothLiveDevices` | `executeScript` | `rocknix-bluetooth stop_live_devices` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 800 | `pairBluetoothDevice` | `executeScript` | `rocknix-bluetooth trust ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 805 | `connectBluetoothDevice` | `executeScript` | `rocknix-bluetooth connect ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 810 | `disconnectBluetoothDevice` | `executeScript` | `rocknix-bluetooth disconnect ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 815 | `removeBluetoothDevice` | `executeScript` | `rocknix-bluetooth remove ` | deviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-bluetooth` | yes |
| 820 | `scanNewBluetooth` | `executeScript` | `rocknix-bluetooth trust input` | - | none joined | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-bluetooth` | yes |
| 825 | `getPairedBluetoothDeviceList` | `executeEnumerationScript` | `rocknix-bluetooth list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-bluetooth` | yes |
| 830 | `getAvailableStorageDevices` | `executeEnumerationScript` | `rocknix-config storage list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-config` | yes |
| 836 | `getVideoModes` | `executeEnumerationScript` | `batocera-resolution listModes` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-resolution` | no |
| 838 | `getVideoModes` | `executeEnumerationScript` | `batocera-resolution --screen \"` | output | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-resolution` | no |
| 844 | `getCustomRunners` | `executeEnumerationScript` | `batocera-wine-runners` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-wine-runners` | no |
| 849 | `getAvailableBackupDevices` | `executeEnumerationScript` | `rocknix-sync list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-sync` | no |
| 854 | `getAvailableInstallDevices` | `executeEnumerationScript` | `batocera-install listDisks` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-install` | no |
| 859 | `getAvailableInstallArchitectures` | `executeEnumerationScript` | `batocera-install listArchs` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-install` | no |
| 864 | `getAvailableOverclocking` | `executeEnumerationScript` | `echo no` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `echo` | base tool |
| 869 | `getSystemInformations` | `executeEnumerationScript` | `rocknix-info --full` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-info` | yes |
| 886 | `getBiosInformations` | `executeEnumerationScript` | `rocknix-systems` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-systems` | yes |
| 929 | `generateSupportFile` | `executeScript` | `batocera-support` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-support` | no |
| 942 | `getCurrentStorage` | `popen` | `rocknix-config storage current` | - | none joined | fgets in the caller | pclose, status unread | the caller's |  | `rocknix-config` | yes |
| 984 | `setStorage` | `executeScript` | `rocknix-config storage ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-config` | yes |
| 989 | `setButtonColorGameForce` | `executeScript` | `batocera-gameforce buttonColorLed ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-gameforce` | no |
| 994 | `setPowerLedGameForce` | `executeScript` | `batocera-gameforce powerLed ` | selected) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-gameforce` | no |
| 1026 | `forgetBluetoothControllers` | `executeScript` | `rocknix-config forgetBT` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `rocknix-config` | yes |
| 1041 | `getAvailableVideoOutputDevices` | `executeEnumerationScript` | `rocknix-config lsoutputs` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-config` | yes |
| 1052 | `getAvailableAudioOutputDevices` | `executeEnumerationScript` | `set-audio list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `set-audio` | no |
| 1059 | `getAvailableChannels` | `executeEnumerationScript` | `timeout 5 /usr/bin/sh -lc \"/usr/bin/wifictl channels\"` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `/usr/bin/wifictl` | yes |
| 1064 | `getAvailableCpuGovernors` | `executeEnumerationScript` | `/usr/bin/sh -lc \"echo \\\"default\\\"; tr \\\" \\\" \\\"\\n\\\" < /sy` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `echo` | base tool |
| 1069 | `getAvailableGpuGovernors` | `executeEnumerationScript` | `/usr/bin/sh -lc \". /etc/profile.d/099-freqfunctions; get_available_gp` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `.` | no |
| 1080 | `getAvailableDisplayModes` | `executeEnumerationScript` | `/usr/bin/sh -lc \"/usr/bin/wlr-randr \| awk '/Modes/{flag=1;next}/Posi` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `/usr/bin/wlr-randr` | binary: the window's ls |
| 1091 | `getAvailableColors` | `executeEnumerationScript` | `/usr/bin/sh -lc \"/usr/bin/ledcontrol list\"` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `/usr/bin/ledcontrol` | yes |
| 1096 | `getSleepModes` | `executeEnumerationScript` | `/usr/bin/sh -lc \"echo \\\"default\\\"; tr \\\" \\\" \\\"\\n\\\" </sys` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `echo` | base tool |
| 1109 | `getCurrentAudioOutputDevice` | `popen` | `set-audio get` | - | none joined | fgets in the caller | pclose, status unread | the caller's |  | `set-audio` | no |
| 1132 | `setAudioOutputDevice` | `system` | `set-audio set` | selected | single quotes | none (inherits stdout) | the caller's | the caller's |  | `set-audio` | no |
| 1147 | `getAvailableAudioOutputProfiles` | `executeEnumerationScript` | `set-audio list-profiles` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `set-audio` | no |
| 1160 | `getCurrentAudioOutputProfile` | `popen` | `set-audio get-profile` | - | none joined | fgets in the caller | pclose, status unread | the caller's |  | `set-audio` | no |
| 1183 | `setAudioOutputProfile` | `system` | `set-audio set-profile` | selected | single quotes | none (inherits stdout) | the caller's | the caller's |  | `set-audio` | no |
| 1459 | `getBatoceraBezelsList` | `executeEnumerationScript` | `rocknix-es-thebezelproject list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `rocknix-es-thebezelproject` | yes |
| 1484 | `installBatoceraBezel` | `executeScript` | `rocknix-es-thebezelproject install ` | bezelsystem | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-es-thebezelproject` | yes |
| 1489 | `uninstallBatoceraBezel` | `executeScript` | `rocknix-es-thebezelproject remove ` | bezelsystem | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `rocknix-es-thebezelproject` | yes |
| 1528 | `getMD5` | `executeEnumerationScript` | `7zr x -so \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `7zr` | binary: the window's ls |
| 1579 | `getCRC32` | `executeEnumerationScript` | `7zr l -slt \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `7zr` | binary: the window's ls |
| 1660 | `unzipFile` | `executeScript` | `7zr x \"` | Utils::FileSystem::getPreferredPath(destFolder), Utils::File | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `7zr` | binary: the window's ls |
| 1825 | `getLED` | `executeScript` | `batocera-led-handheld block_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 1831 | `getLED` | `executeScript` | `batocera-led-handheld block_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 1852 | `getLED` | `executeScript` | `batocera-led-handheld block_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 1861 | `getLED` | `executeScript` | `batocera-led-handheld block_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 1924 | `setLEDColours` | `executeScript` | `batocera-led-handheld set_color_force_dec ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2163 | `setLEDMode` | `executeScript` | `batocera-led-handheld unblock_color_changes` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2166 | `setLEDMode` | `executeScript` | `batocera-led-handheld rainbow` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2168 | `setLEDMode` | `executeScript` | `batocera-led-handheld chroma` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2170 | `setLEDMode` | `executeScript` | `batocera-led-handheld pulse` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-led-handheld` | no |
| 2230 | `getWifiNetworks` | `executeEnumerationScript` | `timeout 45 wifictl scanlist` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `wifictl` | yes |
| 2257 | `executeScriptLegacy` | `executeScriptLegacy` | `` | command | a variable: the command built earlier | every line to func | WEXITSTATUS without WIFEXITED (:2291) | the caller's |  | `-` | - |
| 2413 | `isScriptingSupported` | `executeScript` | `/usr/bin/pm-is-supported --suspend` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/pm-is-supported` | no |
| 2488 | `getFormatDiskList` | `executeEnumerationScript` | `batocera-format listDisks` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-format` | no |
| 2499 | `getFormatFileSystems` | `executeEnumerationScript` | `batocera-format listFstypes` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-format` | no |
| 2504 | `formatDisk` | `executeScript` | `batocera-format format ` | disk, format | bare | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-format` | no |
| 2509 | `getPdfPageCount` | `executeEnumerationScript` | `pdfinfo \"` | fileName | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `pdfinfo` | binary: the window's ls |
| 2591 | `extractPdfImages` | `executeEnumerationScript` | `pdftoppm -r ` | fileName, page, pdfFolder, prefix, squality | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's | WIN32 only | `pdftoppm` | binary: the window's ls |
| 2593 | `extractPdfImages` | `executeEnumerationScript` | `pdftoppm -jpeg -r ` | fileName, page, pdfFolder, prefix, squality | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `pdftoppm` | binary: the window's ls |
| 2622 | `getBatoceraStorePackages` | `executeEnumerationScript` | `batocera-store list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-store` | no |
| 2691 | `installBatoceraStorePackage` | `executeScript` | `batocera-store install \"` | name | double quotes | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-store` | no |
| 2696 | `uninstallBatoceraStorePackage` | `executeScript` | `batocera-store remove \"` | name | double quotes | the lines to func, the last as result | WEXITSTATUS without WIFEXITED (:2319) | the caller's |  | `batocera-store` | no |
| 2701 | `refreshBatoceraStorePackageList` | `executeScript` | `batocera-store refresh` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-store` | no |
| 2702 | `refreshBatoceraStorePackageList` | `executeScript` | `batocera-store clean-all` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-store` | no |
| 2707 | `callBatoceraPreGameListsHook` | `executeScript` | `batocera-preupdate-gamelists-hook` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-preupdate-gamelists-hook` | no |
| 2712 | `updateBatoceraStorePackageList` | `executeScript` | `batocera-store update` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-store` | no |
| 2823 | `getCurrentTimezone` | `executeEnumerationScript` | `batocera-timezone get` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-timezone` | no |
| 2827 | `getCurrentTimezone` | `executeEnumerationScript` | `batocera-timezone detect` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-timezone` | no |
| 2837 | `setTimezone` | `executeScript` | `batocera-timezone set \"` | tz | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-timezone` | no |
| 2846 | `getPadsInfo` | `executeEnumerationScript` | `batocera-padsinfo` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-padsinfo` | no |
| 2899 | `getRunningArchitecture` | `executeEnumerationScript` | `uname -m` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `uname` | base tool |
| 2908 | `getRunningBoard` | `executeEnumerationScript` | `cat /boot/boot/batocera.board` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `cat` | base tool |
| 2927 | `emuKill` | `executeScript` | `batocera-es-swissknife --emukill` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-es-swissknife` | no |
| 2933 | `suspend` | `executeScript` | `/usr/sbin/pm-suspend` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/sbin/pm-suspend` | no |
| 2939 | `replugControllers_sindenguns` | `executeScript` | `/usr/bin/virtual-sindenlightgun-remap` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/virtual-sindenlightgun-remap` | no |
| 2945 | `replugControllers_wiimotes` | `executeScript` | `/usr/bin/virtual-wii-mouse-bar-remap` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/virtual-wii-mouse-bar-remap` | no |
| 2951 | `replugControllers_steamdeckguns` | `executeScript` | `/usr/bin/steamdeckgun-remap` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/steamdeckgun-remap` | no |
| 2956 | `isPlaneMode` | `executeEnumerationScript` | `batocera-planemode status` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-planemode` | no |
| 2971 | `setPlaneMode` | `executeScript` | `batocera-planemode ` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-planemode` | no |
| 2980 | `getServices` | `executeEnumerationScript` | `batocera-services list` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-services` | no |
| 3001 | `getJoysticksHotkeys` | `executeEnumerationScript` | `batocera-joysticks-hotkeys` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-joysticks-hotkeys` | no |
| 3044 | `getJoysticksHotkeysValues` | `executeEnumerationScript` | `batocera-joysticks-hotkeys --values` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-joysticks-hotkeys` | no |
| 3052 | `getGlobalHotkeysValues` | `executeEnumerationScript` | `batocera-hotkeys --values` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3095 | `setJoysticksHotkeys` | `executeScript` | `batocera-joysticks-hotkeys ` | params) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-joysticks-hotkeys` | no |
| 3103 | `detectGlobalHotkeys` | `executeEnumerationScript` | `batocera-hotkeys --detect` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3147 | `getGlobalHotkeys` | `executeEnumerationScript` | `batocera-hotkeys` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3203 | `getKeyboardtopads` | `executeEnumerationScript` | `keyboardToPads --search` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `keyboardToPads` | no |
| 3251 | `getKeyboardtopadDevices` | `executeEnumerationScript` | `keyboardToPads --config \"` | config | double quotes | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `keyboardToPads` | no |
| 3306 | `setGlobalHotkey` | `executeScript` | `batocera-hotkeys --set --config ` | action), config, key | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-hotkeys` | no |
| 3311 | `removeGlobalHotkey` | `executeScript` | `batocera-hotkeys --remove --config ` | config, key) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-hotkeys` | no |
| 3319 | `getKeyboardtopadKeyValues` | `executeEnumerationScript` | `batocera-hotkeys --values` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3380 | `saveKeyboardtopads` | `executeScript` | `` | cmd_dev) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `-` | - |
| 3404 | `saveKeyboardtopads` | `executeScript` | `` | cmd_dev) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `-` | - |
| 3416 | `detectEvKey` | `executeEnumerationScript` | `batocera-hotkeys --detect --count 1 --nowait --evformat --device ` | device_path) | bare | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-hotkeys` | no |
| 3454 | `backglassThemes` | `executeEnumerationScript` | `batocera-backglass list-themes` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-backglass` | no |
| 3465 | `restartBackglass` | `executeScript` | `/usr/bin/batocera-backglass restart` | - | none joined | none (system) | system() == 0 (:2328) | the caller's |  | `/usr/bin/batocera-backglass` | no |
| 3476 | `enableService` | `executeScript` | `batocera-services ` | serviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-services` | no |
| 3478 | `enableService` | `executeScript` | `batocera-services ` | serviceName) | bare | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-services` | no |
| 3485 | `getEjectableDrives` | `executeEnumerationScript` | `batocera-storage-manager list_ejectable` | - | none joined | every line, 1023-byte pieces | discarded (:2251) | the caller's |  | `batocera-storage-manager` | no |
| 3491 | `ejectDrive` | `executeScript` | `batocera-storage-manager eject \"` | mountPath | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-storage-manager` | no |
| 3497 | `mergeDrive` | `executeScript` | `batocera-storage-manager merge \"` | mountPath | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-storage-manager` | no |
| 3503 | `prepareDrive` | `executeScript` | `batocera-storage-manager format \"` | device, fsType | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-storage-manager` | no |
| 3509 | `ignoreDevicePermanently` | `executeScript` | `batocera-storage-manager ignore \"` | deviceId | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-storage-manager` | no |
| 3518 | `nfc_write` | `executeScript` | `batocera-nfc --write \"` | game | double quotes | none (system) | system() == 0 (:2328) | the caller's |  | `batocera-nfc` | no |

143 rows. Quoting: none joined 93, bare 22, double quotes 16, shellQuote 8, a variable: the command built earlier 2, single quotes 2. Scripts not shipped at 8ebaf8daad: 82 rows.
