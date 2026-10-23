### 1. Your own findings first

- **A-01** | **Medium** | `profile.d/001-functions:547-550`, `sources/scripts/setrootpass:45`, `sources/scripts/wifictl:420-473` | `set_setting` turns any value equal to the literal word `default` into a key removal (`001-functions:547-550`, cited in F-01), so setting a free-text or credential key such as `root.password` (`setrootpass:45`) or `wifi.ssid` / `wifi.key` (`wifictl:420-473`) to `default` deletes the key from `system.cfg` instead of storing it.
- **A-02** | **Medium** | `profile.d/001-functions:129-166` | `get_setting` prints its result with an unquoted `echo ${OUTPUT}` (`001-functions:129-130`, cited in G-03), which glob-expands values containing `*`, `?`, or `[...]` against the current working directory, collapses multiple spaces in values such as SSIDs or passwords into one space, and swallows values like `-n` or `-e` as `echo` flags; its system and global awk regexes (`:137, :149, :158, :166`) also leave `.` unescaped in key names.
- **A-03** | **Medium** | `sources/scripts/setsettings.sh:334-335, 567` | F-09 dismisses the host netplay port call at `setsettings.sh:567` as "(the same setting either way: no effect)", but when the player has not set a custom netplay port in `system.cfg`, the backgrounded `[ -z "${RETROARCH_VALUE}" ]&` at `:334` discards the non-empty default `${NETPLAY_PORT}` (`55435`) passed as the third argument and overwrites `RETROARCH_VALUE` with the empty result of `get_setting`.
- **A-04** | **Medium** | `sources/scripts/setsettings.sh:577-582, 683, 688, 787, 1247-1252, 1427-1478`, `sources/scripts/runemu.sh:327` | `setsettings.sh:1427-1478` runs its 24 setting functions concurrently with `&`, so `set_netplay` (`:577-582`) and `set_gambatte` (`:1247-1252`) race on `Gambatte.opt` (`${GAMBATTECONF}`) within the same launch (even after F-17's `"GAMBATTECONF"` typo is fixed), and `set_netplay` (`:683, :688`) and `set_shader` (`:787`) write concurrently to stdout (`>/tmp/shader` at `runemu.sh:327`).
- **A-05** | **Medium** | `sources/scripts/runemu.sh:327, 349, 355, 500`, `sources/scripts/setsettings.sh:405-409` | `runemu.sh:327` captures the entire stdout of `setsettings.sh` into `/tmp/shader`, splices it into `RUNTHIS` (`:349, :355`), and executes `eval ${RUNTHIS}` as root (`:500`), turning any stdout emitted anywhere during `setsettings.sh` (including joypad `.cfg` files sourced as shell at `setsettings.sh:405-409` or any warning printed to fd 1 by a helper) into root command execution.
- **A-06** | **Low** | `sources/scripts/setsettings.sh:395, 397, 405-409` | `configure_hotkeys` runs `grep -b4` (byte offset plus 4 lines of context before and after, instead of `-B4` for 4 lines before) on `/proc/bus/input/devices`, which reads 4 lines past `Handlers=` into the next device stanza and concatenates multiple `Name` lines into the controller name so `/tmp/joypads/${CONTROLLER}.cfg` (`:405`) is not found when multiple pads or adjacent input devices are present (noted in F-13 as Q7 clarity, but it is a Q3 functional bug).
- **A-07** | **Low** | `sources/scripts/suspendmode:3, 51`, `autostart/009-sleepmode:1-17` | `suspendmode` compares the requested sleep mode against the setting already in `system.cfg` (`:3`) and only writes `sleep.conf` and restarts `systemd-logind` when they differ (before saving the setting at `:51`), so whenever `system.cfg` is updated first (by EmulationStation's `SystemConf`, `set_setting`, or a settings backup restore), `suspendmode` sees the stored setting already matches and never updates `sleep.conf`.
- **A-08** | **Low** | `sources/post-update:144-147` | F-35 states that when `cd /storage/.config/ppsspp/assets` at `:144` fails because the directory does not exist, "`cd -` restores it" (`:147`), which is false: a failed `cd` does not change `PWD` or `OLDPWD`, so `cd -` at `:147` either fails (`OLDPWD not set`) or moves `post-update` into an earlier working directory for lines `:148-251`.
- **A-09** | **Low** | `sources/scripts/runemu.sh:432-437, 537` | When no global `cooling.profile` was set prior to launch (`COOLINGPROFILE` empty) and a game sets a per-game `GAMEFAN` (`:432-437`), `quit()` at `:537` calls `set_setting cooling.profile ${COOLINGPROFILE}` unquoted with no value argument; the first reader left "`COOLINGPROFILE` empty -> `set_setting cooling.profile` with no value, behaviour to read in `001-functions`" unresolved in F-04.
- **A-10** | **Low** | `sources/scripts/vertical-check:12-17` | `vertical-check` recovers the active ROM path on every RetroArch window creation by grepping `ps aux` and cutting at the first unescaped space (`:12-17`), which truncates any ROM path with spaces whenever the unescaped `retroarch` argv line matches before the `sh -c` wrapper line (recorded as "lead only" in the Coverage table with no `F-xx` or `G-xx` finding ID).
- **A-11** | **Low** | `sources/scripts/rocknix-systems:1-3`, `sources/scripts/rocknix-bluetooth-agent:1-5`, `02-forward-audit.md` § Mechanical checks (`vocabulary-check`) | Three renovation/tooling items noted in `02-forward-audit.md` were dropped without `F-xx` IDs in `04-analysis.md`: the Python 2 remnants (`#!/usr/bin/env python`, `__future__`, `optparse`) in `rocknix-systems:1-3` and `rocknix-bluetooth-agent:1-5` (listed in the Coverage table's Q1 column), and the `vocabulary-check` scope gap where `02-forward-audit.md` § Mechanical checks says "See F-candidate below" but no finding was ever created (and F-61 was left unused).

---

### 2. Refute both readers

#### A. Every finding now at Medium or above (2 High, 22 Medium) and mis-graded Lows

**High findings (2):**

1. **F-14 (`setsettings.sh:620, 683, 688`, `runemu.sh:327, 349, 355, 500`) — High**: **Agree.**
   - *What would make it false:* `NETPLAY_HOST_IP` being validated or shell-quoted before `:683/:688` prints it, or `runemu.sh:500` not passing `RUNTHIS` containing `EXTRAOPTS` to `eval`.
   - *Does the packet show that?* No; the Group 1 guest proof (`02-forward-audit.md`) shows `global.netplay.host='127.0.0.1;touch /tmp/t1-f14-marker;'` created `/tmp/t1-f14-marker` as root and broke RetroArch's argv. The finding survives.
2. **F-67 (`sources/scripts/updateabl:62-65, 69-70, 72`) — High**: **Agree (device-only).**
   - *What would make it false:* `updateabl` checking `dd`'s exit status and verifying `abl_a`'s hash before writing `abl_b` at `:69-70`, or `updateabl` being unreached on shipped devices.
   - *Does the packet show that?* No; `updateabl` is called from SM8550's `bootloader/update.sh:25` (the shipped Retroid Pocket Nova) and writes `abl_a` then `abl_b` unconditionally with no status check or read-back. The finding survives.

**Medium findings (22):**

3. **F-01 (`runemu.sh:12, 130-131, 465-467, 505`, `099-freqfunctions:82-100`, `100-amd64-freqfunctions:120-142`) — Medium**: **Agree, narrowed to dispatch and H700 kernel config.**
   - *What would make it false:* `runemu.sh` mapping `CPU_GOVERNOR` through a `case` statement instead of executing `${CPU_GOVERNOR}` as a command, and `099-freqfunctions` defining functions for every governor in `scaling_available_governors` (`conservative`, `userspace`).
   - *Does the packet show that?* No; the Group 1 guest proof shows `runemu.sh: line 467: conservative: command not found`, and `projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf` builds `CONSERVATIVE` and `USERSPACE` while `099-freqfunctions:82-100` defines only four functions. The finding survives.
4. **F-03 (`runemu.sh:457-461, 538, 546, 549, 558, 560`) — Medium**: **Narrow to Low (unproven race).**
   - *What would make it false:* Either `runemu.sh` waiting for prior background restore jobs before applying a new launch's settings, or the minimum exit-to-next-launch time through EmulationStation exceeding the completion time of `systemctl restart fancontrol &`, `gpu_performance_level ... &`, and `onlinethreads ... &`.
   - *Does the packet show that?* The packet shows no synchronisation in `runemu.sh`, so the missing coordination is real, but it never measured the background jobs' completion time against the 1.01 s game-to-game time-to-play number (`02-forward-audit.md` promised "To measure: the time from exit to each background job's end against the measured exit-to-next-launch time; a trace on the guest" and never did). As an unmeasured theoretical race, it should be **Low**, not Medium.
5. **F-09 (`setsettings.sh:334-335, 557, 567, 989`) — Medium**: **Agree (with the two-call fix shape from Phase 4.6, plus `:567` in A-03).**
   - *What would make it false:* `:334` using `&&` instead of `&` AND callers distinguishing forced overrides (`:557`) from fallbacks (`:567`, `:989`).
   - *Does the packet show that?* No; shellcheck SC2265 and the Group 1 guest proof show `:334` backgrounds `[ -z "${RETROARCH_VALUE}" ]&` and writes `cheevos_hardcore_mode_enable = "1"` during netplay when `:557` passed `"false"`. The finding survives.
6. **F-10 (`setsettings.sh:133-155, 170-172, 344-356, 801, 840-852, 955-978, 983`) — Medium**: **Agree (with the `pcsx_rearmed` 32-bit check split out per Phase 4.6).**
   - *What would make it false:* `match()` testing whole-word equality instead of substring regex `[[ "${myarray[*]}" =~ ${seek} ]]`.
   - *Does the packet show that?* No; the Group 1 guest proof shows `neogeo` matches `neogeocd` in `NO_REWIND` and `NO_RUNAHEAD`, forcing `rewind_enable = "false"` and `run_ahead_enabled = "false"`. The finding survives.
7. **F-11 (`setsettings.sh:310-325, 1427-1478`) — Medium**: **Agree.**
   - *What would make it false:* `clear_setting` not using an unsynchronised `[ ! -f "${TMP_CONFIG}.sed" ]` check-then-truncate `>` across 24 background subshells.
   - *Does the packet show that?* No; the Group 1 guest proof lost keys in 9 of 200 iterations on the guest's bash. The finding survives.
8. **F-15 (`setsettings.sh:595, 621, 647, 671-675`) — Medium**: **Agree.**
   - *What would make it false:* `:621` passing `"netplay_ip_port"` as the second argument to `add_setting`, and `:675` appending `>>` to `TGB Dual.opt` instead of truncating it with `>`.
   - *Does the packet show that?* No; `:621` passes only two arguments (`"global.netplay.port" "${NETPLAY_PORT}"`) and `:675` truncates `TGB Dual.opt` with `>`. Upgrading F-15 to Medium in Phase 4.6 (matching F-16 and F-17) survives.
9. **F-16 (`setsettings.sh:1012, 1016`) — Medium**: **Agree.**
   - *What would make it false:* `:1012` not redirecting `grep`'s stdout to `/dev/null` inside `$(grep ... > /dev/null 2>&1)`, or `:1016` appending `>>` instead of truncating `MAME 2003-Plus.opt` with `>`.
   - *Does the packet show that?* No; shellcheck SC2328 and the Group 1 guest proof show a 3-line `MAME 2003-Plus.opt` is truncated to 1 line when `tatemode=1`. The finding survives.
10. **F-17 (`setsettings.sh:1247-1252`) — Medium**: **Agree.**
    - *What would make it false:* `:1247` testing `[ ! -f "${GAMBATTECONF}" ]` instead of the literal string `[ ! -f "GAMBATTECONF" ]`.
    - *Does the packet show that?* No; the Group 1 guest proof shows a 3-line `Gambatte.opt` is truncated to 1 line on a `gambatte` launch. The finding survives.
11. **F-21 (`profile.d/001-functions:129-134`) — Medium**: **Agree.**
    - *What would make it false:* `get_setting` matching the per-game key with literal string comparison (`index()`) or escaping all regex metacharacters (`[`, `]`, `*`, `+`, `?`, `.`, etc.) instead of only `'`, `(`, `)`, `&`.
    - *Does the packet show that?* No; the Group 1 guest proof shows `get_setting cpugovernor nes "T1 Test [!].nes"` returns empty while `"T1Test.nes"` returns `powersave`. The finding survives.
12. **F-29 (`sources/scripts/setrootpass:32-45`) — Medium**: **Agree.**
    - *What would make it false:* `setrootpass` checking that `cryptpw` succeeded and produced a non-empty `$6$...` hash at `:32`, and verifying that `:35` updated the root entry in `/storage/.cache/shadow` before updating Samba, Syncthing, and `system.cfg` and returning 0.
    - *Does the packet show that?* No; the Group 2 guest proof shows that when `cryptpw` fails, `setrootpass` writes an empty root hash field into `/storage/.cache/shadow`, updates `system.cfg` and Samba, and exits 0. The finding survives.
13. **F-32 (`sources/post-update:159-160, 202`) — Medium**: **Agree.**
    - *What would make it false:* `post-update:159-160` and `:202` using `set_setting` and `del_setting` (which acquire `wait_lock` and drop a torn final line via `settings_base`) instead of raw `sed -i` on `system.cfg`.
    - *Does the packet show that?* No; the Group 2 guest proof shows busybox `sed -i '$ a\system.batteryplus.enabled=1'` appends a newline to a torn final line (`wifi.country=G`), turning a detectable torn file into a syntactically complete corrupt one. The finding survives.
14. **F-33 (`sources/post-update:32-36`) — Medium**: **Agree.**
    - *What would make it false:* `post-update:32-36` skipping `mv <file> last_<file>` when `<file>` is already a symlink.
    - *Does the packet show that?* No; `:32-36` unconditionally moves `es_features.cfg`, `es_systems.cfg`, and `es_savestates.cfg` to `last_<name>` on every update, so the second update overwrites `last_<name>` with the symlink created by the first update. The finding survives.
15. **F-39 (`sources/scripts/installtointernal:89-108`) — Medium**: **Agree (device-only).**
    - *What would make it false:* `installtointernal` checking `/proc/mounts` and refusing to repartition/format `${DEVICE}` (`/dev/sda`) when `/flash` or `/storage` is already mounted from `${DEVICE}`.
    - *Does the packet show that?* No; `:89-108` detects existing partitions after `userdata`, runs `parted -s ... rm "$p" >/dev/null 2>&1 || true`, and proceeds to `mkfs` without checking if the running system is booted from `${DEVICE}`. The finding survives.
16. **F-40 (`sources/scripts/installtointernal:48, 200-205, 208-215, 255`) — Medium**: **Agree.**
    - *What would make it false:* `:208-215` propagating a `cp -a` failure to stop the script before `:255` prints `successful`, and `get_storage_size_kb` (`:48`) not subtracting `.cache/cores` when `:208-215` copies it.
    - *Does the packet show that?* No; the Group 2 guest proof shows busybox `find ... -exec cp -a {} ... \;` exits 0 when `cp` fails with `Permission denied`. The finding survives at Medium.
17. **F-42 (`sources/scripts/automount:57, 68, 167, 174`) — Medium**: **Agree.**
    - *What would make it false:* `start_ms` (`:57, :68`) and `mount_games` (`:167, :174`) checking the exit status of their `mount` commands and logging/handling failure.
    - *Does the packet show that?* No; neither checks `mount`'s status, leaving `/storage/roms` pointing at the internal card's directory on failure. The finding survives.
18. **F-43 (`sources/scripts/automount:234, 239, 251-252`) — Medium**: **Agree (provided `:239` stays in the Medium Q3 half).**
    - *What would make it false:* `:251` matching whole device tokens in `/proc/mounts` instead of substring `grep "${DEV}"`, `:239` not treating an empty `${SIZE}` (arithmetic syntax error in `(( ${SIZE} <= 8388608 ))`) as `> 8 GiB`, and `mount_games` restricting candidates to external storage devices.
    - *Does the packet show that?* No; all three flaws are present at `:239` and `:251-252`. The finding survives.
19. **F-44 (`sources/post-update:199-202`, `config/system/configs/system.cfg`) — Medium**: **Agree.**
    - *What would make it false:* `post-update:202` not deleting `system.suspend.dpms` on every update.
    - *Does the packet show that?* No; the Group 2 guest proof shows `post-update:202` (`sed -i "/system.suspend.dpms/d"`) deletes `system.suspend.dpms=1` unconditionally on every update, contradicting its own comment at `:199-201` that the setting is opt-in. The finding survives.
20. **F-57 (`sources/scripts/paneladj:20, 35, 37, 40`) — Medium**: **Agree.**
    - *What would make it false:* `:37` and `:40` using `-gt` and `-lt` instead of `>` and `<` inside `[ ... ]`.
    - *Does the packet show that?* No; shellcheck SC2071 and the guest proof show `[ "${MYVAL}" > "${MAX}" ]` at `:37` is a file redirection that creates/truncates a file named `100` in the working directory and clamps `MYVAL=30` to `100`. The finding survives.
21. **F-58 (`autostart/008-perfmode:8, 13-37`, `package.mk:119-126`) — Medium**: **Agree.**
    - *What would make it false:* `/etc/profile.d/099-freqfunctions` being installed on x86_64 or `008-perfmode:8` guarding the `. /etc/profile.d/099-freqfunctions` call by file existence / architecture.
    - *Does the packet show that?* No; `package.mk:119-126` installs `099-freqfunctions` on non-x86_64 only, and the guest's boot journal and `sh -x` proof show `008-perfmode` aborts at line 8 (`No such file or directory`) under POSIX-mode bash before lines `:13-37` can run. The finding survives.
22. **F-63 (`package.mk:29`, `config/system/configs/system.cfg`) — Medium**: **Agree.**
    - *What would make it false:* `package.mk:29` not running `chmod o+x` on `/usr/config/system/*` and `system.cfg` having private permissions (`0600`) rather than `0645`.
    - *Does the packet show that?* No; `stat` on the guest at 08:06 showed the seed, live `system.cfg`, and backup record are all mode `645` while holding `root.password`, `wifi.key`, and the RetroAchievements password. The finding survives.
23. **F-68 (`sources/scripts/rocknix-bluetooth:8-10, 73-98`, `network/bluez/system.d/bluetooth.service:10, 12`) — Medium**: **Agree.**
    - *What would make it false:* `rocknix-bluetooth` not archiving `/storage/.cache/bluetooth` (Bluetooth link keys) into `/storage/roms/backups/bluetooth.tar` on every service stop, or `/storage/roms` not being shared/backed up.
    - *Does the packet show that?* No; `:8-10` and `:73-82` write `/storage/roms/backups/bluetooth.tar` on every `bluetooth.service` stop, placing link keys inside the Samba-shared `/storage/roms` tree that `backuptool:277` explicitly excludes from settings backups. The finding survives.
24. **G-01 (`autostart/003-upgrade:11-15`) — Medium**: **Agree.**
    - *What would make it false:* `003-upgrade` removing `/storage/.boot.hint` at `:15` only when `/usr/share/post-update` at `:11` exits 0.
    - *Does the packet show that?* No; `rm /storage/.boot.hint` runs unconditionally after `post-update`, contradicting `02-forward-audit.md`'s initial claim under `003-upgrade` that "an interrupted `post-update` run[s] again at the next boot" when `post-update` fails with a non-zero exit code rather than a hard power cut. The finding survives.

**Mis-graded Low findings (3):**

25. **F-19 (`setsettings.sh:821-822, 1048-1056, 1077-1087, 1123, 1220-1222, 1270-1278, 1306-1331, 1405-1411`, `config/system/configs/system.cfg`) — Currently Low (downgraded from Medium in Phase 4.6)**: **Re-grade back to Medium.**
    - *What would make it false:* `set_overlay` (`:821-822`) falling through to apply the player's `overlayset` when `write_bezel_config` (`:1306-1331`) finds no bezel file on disk, or the shipped default not being `global.bezel=thebezelproject`.
    - *Does the packet show that?* No; the Group 2 guest proof (`02-forward-audit.md`) proves that with `global.overlayset=T1overlay.cfg` and the shipped default `global.bezel=thebezelproject`, the appendconfig gets **`0 input_overlay lines`** — neither a bezel nor an overlay — because no bezel files are installed by default, `write_bezel_config` fails, and `set_overlay` (`:821-822`) still exits early. Phase 4.6's downgrade to Low ("Nothing in the tree says whether bezels and overlays are exclusive") misread the proof: `0 input_overlay lines` means neither was applied.
26. **F-13 (`setsettings.sh:395, 397, 405-409`) — Currently Low**: **Re-grade to Medium.**
    - *What would make it false:* `configure_hotkeys` parsing `key = "value"` lines instead of running `source` as root on `/tmp/joypads/<controller>.cfg` (`:405-409`, where `/tmp/joypads` is backed by `/storage/joypads` per F-36), and `:395/:397` using `grep -B4` instead of `grep -b4`.
    - *Does the packet show that?* No; `:395/:397` uses `grep -b4` (which reads 4 lines after `Handlers=` and concatenates `Name` lines when multiple pads are present, breaking hotkey lookup, A-06) and `:405-409` `source`s the modified `.cfg` file as root on every launch.
27. **F-27 (`setsettings.sh:778-790`, `config/system/configs/system.cfg`) — Currently Low**: **Keep Low, but flag as incomplete in the audit.**
    - *What would make it false:* `set_shader` treating an empty `SHADER` the same as `none`/`false` instead of hitting `*)` and passing `--set-shader /tmp/shaders/` (a directory) and `video_shader_enable = "true"` on every default launch.
    - *Does the packet show that?* No; the Group 1 guest proof (`F-14` runs) recorded `--set-shader /tmp/shaders/` in the stub's argv on both runs, and the auditor never completed the promised check of `exec.log` to see whether passing a directory breaks or slows RetroArch shader initialisation.

---

#### B. Do the first reader's grades of the second reader's items in Phase 4.6 survive?

1. **The two refutations of the second reader:**
   - **F-40 kept at Medium (`installtointernal:208-215, 255`, refuting Astra's High)**: **Survives.** `:208-215` only runs `cp -a` from the SD card and never deletes or formats the source card; `installtointernal` is also manual-only (no UI caller). The script's bug is printing the false `successful` banner at `:255` after `find -exec cp` hides `cp`'s non-zero status.
   - **F-57's minimum branch (`paneladj:35, 37, 40`, refuting Astra's claim that a file named `1` selects the minimum)**: **Survives.** `getValue` reaches `:37` only when `MYVAL` is non-empty (`:35`). At `:37`, `[ "${MYVAL}" > "${MAX}" ]` runs `[ "${MYVAL}" ]` with stdout redirected to `${MAX}` (`100`). Because `MYVAL` is non-empty, `[ "${MYVAL}" ]` is always true (0) whenever opening `100` for writing succeeds, so the `if` branch at `:37` is always taken and the `elif [ "${MYVAL}" < "${MIN}" ]` at `:40` is never reached.
2. **The two corrections of the first reader:**
   - **F-54's traversal example (`rocknix-es-thebezelproject:401, 438, 454`)**: **Survives.** In bash, `${index_bezel_name##*.}` strips the longest prefix ending in `.` (through the last dot). For `./../x`, the last dot is the second dot of `..`, leaving `/x` (`$rom_no_ext./x`), not `../x`; in fact, `##*.` can never leave `..` in `$index_ext`. Narrowing F-54 to slash validation plus the empty `$system_name` check in `remove` (`:570-600`) is exact.
   - **F-57's `1`-file sentence (`paneladj:37, 40`)**: **Survives.** For the same reason `:40` is unreachable when `:37`'s redirection succeeds, `02-forward-audit.md`'s claim that "the first `<` reads its input from a file named `1`" was wrong and is properly retracted, while Astra's point that `> 100` truncates an existing file `100` in the working directory is right.
3. **The two re-grades to High:**
   - **F-14 (`setsettings.sh:620, 683, 688`, `runemu.sh:327, 349, 355, 500`) -> High**: **Survives.** Proven root command execution via `eval ${RUNTHIS}` from a `system.cfg` setting written by a free-text UI field (`GuiNetPlaySettings.cpp:33`, `GuiGameOptions.cpp:215`) and restorable via settings backups.
   - **F-67 (`updateabl:69-70, 72`) -> High**: **Survives.** Writing `abl_a` and immediately `abl_b` with `dd` and no status or read-back check on the shipped SM8550 can corrupt both bootloader slots.
4. **New findings G-01 to G-07:**
   - **G-01 (`003-upgrade:11-15`, confirmed Medium)**: **Survives.** `rm /storage/.boot.hint` at `:15` is unconditional after `post-update` at `:11`.
   - **G-02 (`post-update:38`, agree, narrowed to Low)**: **Survives.** `rsync -a --delete --exclude=configs /usr/config/system/ /storage/.config/system/` deletes anything placed beside `configs/`; narrowing to a Low intent/scope item is fair.
   - **G-03 (`001-functions:129-130`, confirmed Low)**: **Survives** (and exposes the unquoted `echo ${OUTPUT}` bug in A-02).
   - **G-04 (`installtointernal:63`, agree, narrowed to Low)**: **Survives.** Under `set -euo pipefail`, process substitution `< <(parted ... | grep ':userdata:')` does not propagate `parted`'s exit status to `mapfile`, whereas `MAX_PART_NUM=$(...)` at `:89` is a command substitution in an assignment and does fail under `-e` + `pipefail`.
   - **G-05 (`runemu.sh:378-379, 384-385`, agree, narrowed to Low)**: **Survives.** In a `sed` `c\` command, `/` and `&` are literal (not special as they are in `s///`), whereas `\` and newlines are interpreted by `sed` and `"` breaks `mapper.txt` quoting.
   - **G-06 (`rocknix-config:34, 39`, confirmed Low)**: **Survives.** Unanchored `grep "$key"` at `:34` and unescaped `sed -i "s/#\?$key=.*/$key=$value/g"` at `:39` fail on prefix keys and `/` or `&` in values.
   - **G-07 (`handle-hdmi-hotplug:19-21`, `081-usbgadget`, confirmed Low, device-only)**: **Grade Low survives, but the hardware scope in Phase 4.6 does not survive.** Phase 4.6 narrows G-07 to "USB-C DisplayPort on RK3588/SM8250", contradicting `02-forward-audit.md` (under `handle-hdmi-hotplug` and the Coverage table), which states that `hdmi-hotplug.path`/`.service` are enabled by `package.mk` on **H700** (a shipped device) and cites `handle-hdmi-hotplug:15-17, 28-30` calling the nonexistent `usbgadget` systemd unit.
5. **All other re-grades and narrowings in Phase 4.6:**
   - **F-19 (`setsettings.sh:821-822, 1306-1331`, downgraded from Medium to Low)**: **Does NOT survive.** As shown above, the Group 2 guest proof yielded `0 input_overlay lines` (neither bezel nor overlay) when `global.bezel=thebezelproject` has no bezel file on disk and `set_overlay` (`:821-822`) exits early after `write_bezel_config` fails.
   - **F-09 (`setsettings.sh:334-335, 557, 989`, fix shape rejected)**: **Survives.** "OS value when set, else caller's" would still let a player's `retroachievements.hardcore=1` override netplay's forced `"false"` at `:557`; forced values and fallbacks require separate shapes.
   - **F-10 (`setsettings.sh:170-172, 801`, `pcsx_rearmed` split out)**: **Survives.** Whole-word matching fixes `neogeo` vs `neogeocd`, but `pcsx_rearmed` is the exact core name for both 32-bit and 64-bit builds, so `IS_32BIT` cannot be decided by core name alone.
   - **F-43 (`automount:239, 251-252`, re-graded to Medium and split)**: **Survives only if `:239` stays in the Medium half.** The `:251` redirection-inside-quotes oddity is Q7, but `:239`'s `(( ${SIZE} <= 8388608 ))` arithmetic error on an empty `SIZE` (treating a device absent from `/proc/partitions` as `> 8 GiB`) is a Q3 storage-selection bug, not Q7.
   - **F-01, F-11, F-15 (to Medium), F-16, F-17, F-18 (to question/Low), F-21, F-29, F-32, F-33 (to Medium), F-39, F-42 (to Medium), F-44, F-55, F-58, F-63 (to Medium), F-68, F-06 (kept Low)**: **All survive** on the cited lines. (F-03's confirmation at Medium does not survive; see item 4 in section 2A above.)

---

### 3. What you could not judge

1. **The 43-row Q4 table (upstream commit dispositions) and 47-row Q6 table (reachability searches and `Already written:` lines) are not in the packet.** `02-forward-audit.md` (AC-10, AC-11) and Phase 4.6 reference both tables, and the Coverage table lists per-file upstream commit counts (`2` on `001-functions`, `5` on `post-update`, `4` on `factoryreset`, `5` on `runemu.sh`, `2` on `setsettings.sh`, etc.), but the tables themselves were omitted from the packet. I could not verify whether any of the 43 upstream commits in `c445081a59..8b70f693b8` were mis-dispositioned or whether the `Already written:` analyses for the unreached scripts hold.
2. **The M7 candidate delta (`next..069fc2704421`: `package.mk` +3, `runemu.sh` +63/-2) and `01-research-notes.md` § Scope are not in the packet.** I could not verify AC-06 directly, nor could I judge whether the 63-line M7 lifecycle prologue in the image's `/usr/bin/runemu.sh` affected the Q5 `time-to-play` measurements (0.64 s and 1.01 s) or `emulator-exit-test`, both of which ran against the image's copy rather than the tree's copy (`02-forward-audit.md` § Image versus tree).
3. **The unread bodies of the 21 "outline-read" files (`02-forward-audit.md` § Coverage Boundary).** For `rocknix-fake-suspend` (486 lines), `rocknix-bluetooth` (371), `rocknix-bluetooth-agent` (571), `rocknix-es-thebezelproject` (641), `brightness` (224), `vertical-check` (lines 41–182), `rocknix-info` (259), `rocknix-config` (296), `rocknix-settings` (267), `rocknix-systems` (250), and `rocknix-scraper` (79), the packet provides only high-level summaries and selected line citations. Any defects in the unquoted lines of those files cannot be judged from the packet.
4. **Six checks explicitly promised in `02-forward-audit.md` whose results were never recorded in the packet:**
   - **F-27 (`setsettings.sh:778-790`)**: What RetroArch logs in `exec.log` when passed `--set-shader /tmp/shaders/` (a directory) and `video_shader_enable = "true"` on every default launch.
   - **F-18 (`setsettings.sh:1065`)**: What `retroarch.cfg`'s `rgui_config_directory` and the Kronos core actually read (`${RETROARCH_PATH}/Kronos/config/Kronos` vs `${RETROARCH_PATH}/config/Kronos`).
   - **F-04 (`runemu.sh:432-437, 537`)**: Whether SM8550 defines `DEVICE_HAS_FAN`, and what `set_setting cooling.profile` (`001-functions:534-561`) does on disk when called at `:537` with an empty `${COOLINGPROFILE}`.
   - **F-08 (`runemu.sh:61-65`) and `vertical-check` (`02-forward-audit.md`)**: The promised Q5 guest timings for `game-guides-tool` at every launch and `vertical-check` (`ps aux` + `grep` of `arcaderoms.xml`) at every RetroArch window open.
   - **F-38 (`factoryreset:202`)**: What programs other than WirePlumber write to `/storage/.local/state` on the image before `factoryreset audio` deletes the whole directory.
   - **F-31 (`rocknix-automount.service` / `automount`)**: What environment files `automount` sources itself to make `EnvironmentFile=/etc/profile` redundant.
5. **The VM upgrade rehearsal (`tools/vm-upgrade-rehearsal`).** Noted in `02-forward-audit.md` § Coverage Boundary as not run this session; end-to-end upgrade boot behaviour of `003-upgrade` and `post-update` could not be judged.
6. **Hardware-only paths and timing races not reproduced on the x86_64 QEMU guest:**
   - Whether backgrounded exit jobs in `runemu.sh:538, 546, 549, 558, 560` (F-03) ever finish after the next launch's setup on a real handheld.
   - Whether `/sys/devices/system/cpu/cpu0/online` exists on the shipped ARM64 kernels (`099-freqfunctions:12, 18, 39-45`, F-25).
   - Live device behaviour for `installtointernal` on `/dev/sda` (F-39), `updateabl` on `abl_a`/`abl_b` (F-67), `rocknix-memory-manager` swap resize under load (F-53) and KSM scan cost on 1 GiB H700 devices, `save-sysconfig.service` on hung storage I/O (F-30), and `handle-hdmi-hotplug` / `rocknix-fake-suspend` on hardware events.