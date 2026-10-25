# T22 forward audit: the OS's system services and platform quirks (#669)

The 422 paths are read at `8ebaf8daad` and compared with upstream `next` at
`651150fc88`. One guest window ran (granted 09:12 on #669). Every
`proved:` cell reads `tree`, `history`, `tool-run`, `fixture`, `guest` or
`design`. The tables marked *generated* come from
`tools/t22-reach.py` (run as `python3 -I -B tools/t22-reach.py .qa-scratch/t22/rows.json <dir>`),
never typed.

## The runs

The brief's § 5 commands and the stage-B reads. Each output is in
`.qa-scratch/t22/runs/<#>.out` (gitignored; re-made by the commands in `01`).

| # | Run | rc | Wall | Figure | A FAIL would mean | proved |
| --- | --- | --- | --- | --- | --- | --- |
| `01-membership` | the § 2 membership block (at `2174265e9c`) | 0 | 0.51 s | 422 paths / 16,604 lines; read 10,898; fork-own 3,002 over 24; tier 398/24; reach 422; written 422 | a different set: a path gained or lost, a glob that no longer matches the inventory, or a stale `inventory.json`; recorded as a delta, not a stop | tool-run |
| `02-sysutils-pkg` | `system-utils/package.mk` lines 10-36 | 0 | 0.01 s | `:14-15` common autostart; `:27-36` only `${DEVICE}`'s files | a package that installs every device's files, so the 8 rows would be shipped | tool-run |
| `03-quirks-pkg` | `quirks/package.mk`: the copies | 0 | 0.00 s | `:15` every `devices/*`; `:16-18` every `platforms/*` when `platforms/${DEVICE}` exists | a platform-scoped copy, so the 213 would not be on the image | tool-run |
| `04-sysutils-devices` | `system-utils` device and autostart directories | 0 | 0.01 s | AMD64 3, common 1, GENERIC_X64 1, RK3399 3, RK3566 1, S922X 1 | a shipped device with a directory, changing the 8 | tool-run |
| `05-platforms` | platform files by directory | 0 | 0.01 s | 264; H700 22, SM8550 24, GENERIC_X64 5 | a different shipped share than 51 | tool-run |
| `06-video_sense` | `video_sense` files | 0 | 0.00 s | GENERIC_X64 and RK3399 | a shipped image starting `video.service` without the binary (blindspot 16) | tool-run |
| `07-autostart` | `/usr/bin/autostart`: the selectors and loops | 0 | 0.01 s | 97 lines; `:16-28` HW_DEVICE, `:31-43` QUIRK_DEVICE, `:71` the custom loop | a guarded or quoted custom loop | tool-run |
| `08-quirk_device` | who sets and reads `QUIRK_DEVICE` | 0 | 0.01 s | set at `002-autostart:8-12` (device tree, else DMI); read by autostart, sleep.sh, four system-utils scripts, userconfig-setup | another setter, a second selection rule | tool-run |
| `09-units` | the units under the globs | 0 | 0.01 s | 29 | a unit added or lost | tool-run |
| `10-units-user` | the brief's `User=` loop, as written | 0 | 0.14 s | every row `User=***`: **its mask hides the count** (a delta) | not a FAIL of the product: the run cannot show its figure; rerun as 10b | tool-run |
| `10b-units-user-unmasked` | the same loop, mask on the ExecStart text only | 0 | 0.24 s | 0 of 29 name `User=`, `Group=` or `DynamicUser=` | a unit that drops privileges | tool-run |
| `11-busybox-pkg` | busybox's pin | 0 | 0.01 s | 1.36.1 `:7`, http `PKG_URL` `:11` | another pin; an https URL | tool-run |
| `12-busybox-flags` | busybox's flagged applets | 0 | 0.00 s | SUID `:30`, LOGIN `:549`, PASSWD `:554`, SU `:556`, HTTPD `:888`, CGI `:894`, NC `:950`, UDHCPD `:1010` | a flag off, narrowing the setuid surface | tool-run |
| `13-history` | history since `2026-06-01T00:00:00Z` | 0 | 0.27 s | 87; 33 fork; 54 upstream | a count off by the hour of a bare `--since` date | tool-run |
| `14-delta` | the 422 against `651150fc88` | 0 | 0.01 s | 44 M, 20 D | a different drift | tool-run |
| `15-added` | A and R under the globs | 0 | 0.01 s | 42 A, 2 R | a new file under the globs unlisted | tool-run |
| `16-bb-systemd-log` | upstream's busybox and systemd commits since the read tree | 0 | 0.01 s | 12 listed, `03204074ef` .. `ed5aeaa34a` | -- (a listing) | tool-run |
| `17-routes` | the two seats' routes | 0 | 0.00 s | `council-invoke.ts` 7, `lint-audit-artifacts` 4 | 0: a named blocker at Phase 4.6 | tool-run |
| `18-removal-rule` | `git diff --stat 4a48d388c4 HEAD -- packages projects tools` | 0 | 0.00 s | empty | a line: a change outside the lane's rule | tool-run |
| `19-deleted` | the 20 D, with the merge base and the deleting commit | 0 | 0.09 s | 9 never upstream's / 2 upstream removed / 9 deleted | a different split | tool-run |
| `20-enable` | `enable_service|preset` naming the 29 | 0 | 0.13 s | 7 units named; none of video, headphones, input, fancontrol, batteryledstatus | an enablement for the five | tool-run |
| `21-fork-own-and-config` | the fork-own 24 and the 30 config files | ? | ? | 24 with last fork commits; 30 config, 4,487 lines (busybox 3,648) | -- (a listing) | tool-run |
| `22-applet-callers` | callers of the flagged applets | 0 | 0.67 s | su 0, login 0 (prose only), passwd 0 (smb.conf setting only), httpd 0, nc 3, udhcpd 1 (`usbgadget:238`); setuid at `busybox/package.mk:177`, `:209` | a caller that needs an applet this slice calls unused | tool-run |
| `23-modified` | the 44 M with diff size and commits | 0 | 0.65 s | 44; the two touching the lead findings: `autostart` (`a98a3066f5`, the lock path only), `95-udevil-mount.rules` (`dc781c0c75`, `--no-block`) | -- (a listing) | tool-run |
| `24-unit-exec` | every unit's Exec, Where, Condition lines | ? | ? | 29 read | -- (a listing) | tool-run |

## The reachability table

*Generated.* One row per path: **installed on** (which shipped image carries
the file; the package's `reachable_by` from the inventory, then the file's
own selector), **runs on** (where it is executed, sourced or read at run
time) and the line that decides it. Summary, as the generator printed it:

```
{"rows": 422, "platform files": 264, "platform files run on no shipped device": 213, "install-time rows no shipped image installs": 8, "installed on none": 12, "recipes (build only)": 28, "runs on none": 225, "deltas": []}
```

- **422 rows**; **8 install-time rows** installed by no shipped image (`system-utils/sources/devices/` AMD64 3, RK3399 3, RK3566 1, S922X 1, by `system-utils/package.mk:27-29`); **213 platform files** installed on every shipped image and run on none (`quirks/package.mk:16-18` copies every platform; `autostart:16-28`, `sleep.sh:44,84` and the `bin/` callers select by `HW_DEVICE`).
- **Installed on none: 12** = those 8, the host busybox configuration, cron's two units and its default (CRON_SUPPORT=no).
- **Runs on none: 225** = the 213 platform files, the 8 install-time rows, cron's three files (two units and `default.d/crond.conf`) and `volume-fixup.service` (installed everywhere, enabled only for RK3566).
- The 28 recipes are build-time (`runs on: build`).

| Path | Installed on | Runs on | Deciding line (at `8ebaf8daad`) | proved |
| --- | --- | --- | --- | --- |
| `hardware/quirks/autostart/002-device-switch` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:96-100 -> /usr/lib/autostart/common; autostart:50-54 | tree |
| `hardware/quirks/autostart/020-configs` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:96-100 -> /usr/lib/autostart/common; autostart:50-54 | tree |
| `hardware/quirks/autostart/020-rumble` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:96-100 -> /usr/lib/autostart/common; autostart:50-54 | tree |
| `hardware/quirks/autostart/020-set_audio_latency` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:96-100 -> /usr/lib/autostart/common; autostart:50-54 | tree |
| `hardware/quirks/autostart/080-dual_screen_mode` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:96-100 -> /usr/lib/autostart/common; autostart:50-54 | tree |
| `hardware/quirks/autostart/095-turbo-mode` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:96-100 -> /usr/lib/autostart/common; autostart:50-54 | tree |
| `hardware/quirks/autostart/999-export` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:96-100 -> /usr/lib/autostart/common; autostart:50-54 | tree |
| `hardware/quirks/package.mk` | — (recipe) | build | hardware/quirks/package.mk | tree |
| `hardware/quirks/platforms/AMD64/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/005-thermal_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/006-gpu-freq-path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/010-default_tdp` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/010-dpms` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/010-led_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/020-fan_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/030-suspend_mode` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/050-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/050-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/post/001-dpms` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/post/002-ledcontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/post/003-wifi` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/post/004-log` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/pre/001-dpms` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/pre/002-ledcontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/GENERIC_X64/090-ui_service` | H700, SM8550, VM | VM | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/GENERIC_X64/091-ui_shader` | H700, SM8550, VM | VM | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/GENERIC_X64/092-retroarch-surface` | H700, SM8550, VM | VM | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/GENERIC_X64/095-cloud-ssh` | H700, SM8550, VM | VM | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/GENERIC_X64/097-retired-rescue-masks` | H700, SM8550, VM | VM | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/001-device_config` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/002-turbo-mode_config` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/006-panfrost` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/010-governors` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/010-led_control` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/020-fan_control` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/020-set_audio_latency` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/030-analog_leds` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/030-suspend_mode` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/040-wifi_probe_retry` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/050-modifiers` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/090-ui_service` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/091-ui_shader` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/400-set_gpu_overclock` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/bin/analog_sticks_ledcontrol` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/H700/bin/gpu_overclock` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/H700/bin/ledcontrol` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/H700/sleep.d/post/003-codec` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/sleep.d/post/004-led` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/sleep.d/post/005-usbgadget` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/sleep.d/pre/003-codec` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/H700/sleep.d/pre/004-led` | H700, SM8550, VM | H700 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/002-turbo-mode_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/015-rk817_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/050-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/050-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/060-game_settings` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/075-mangohud-supported` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/bin/battery_led_status` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/RK3326/sleep.d/post/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3326/sleep.d/pre/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3399/002-turbo-mode_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3399/005-thermal_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3399/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3399/050-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3399/065-Touchscreen-events` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3399/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3399/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3399/bin/battery_led_status` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/RK3566/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/002-turbo-mode_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/010-led_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/015-rk817_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/030-suspend_mode` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/050-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/050-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/055-thermal-trips` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/060-game_settings` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/065-Touchscreen-events` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3566/bin/ledcontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/RK3566/bin/volumealign` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); volume-fixup.service, enabled on RK3566 only (quirks/package.mk:25-28) | tree |
| `hardware/quirks/platforms/RK3566/modules.keep` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:44 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/002-turbo-mode_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/010-led_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/020-suspend_mode` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/050-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/050-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/055-thermal-trips` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/065-Touchscreen-events` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3576/sleep.d/pre/99-idle-only` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/009-commander-cfg` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/010-led_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/041-panfrost` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/050-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/050-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/065-Touchscreen-events` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/RK3588/bin/ledcontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/S922X/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/030-suspend_mode` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/041-panfrost` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/050-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/075-mangohud-supported` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/S922X/bin/battery_led_status` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM4450/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/004-usb-autosuspend` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/005-thermal_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/007-usb-input-current` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/015-turnip-debug` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/020-fan_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/070-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/075-mangohud-supported` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM4450/bin/fancontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM4450/bin/usb-input-current` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM6115/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/002-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/004-usb-autosuspend` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/005-thermal_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/009-commander-cfg` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/009-serial-number-path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/015-turnip-debug` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/020-set_audio_latency` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/030-led-control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/030-suspend_mode` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/031-analog_leds` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/045-irq-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/060-game_settings` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/065-Touchscreen-events` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/070-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/075-mangohud-supported` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/400-set_gpu_max_clock` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/500-enable-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/bin/achievements` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM6115/bin/analog_sticks_ledcontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM6115/bin/battery_led_status` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM6115/bin/gpu_max_clock` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM6115/bin/ledcontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM6115/sleep.d/post/001-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/sleep.d/post/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/sleep.d/pre/001-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM6115/sleep.d/pre/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/002-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/005-thermal_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/009-commander-cfg` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/009-serial-number-path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/020-fan_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/020-set_audio_latency` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/030-led-control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/031-analog_leds` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/061-yabasanshiro_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/065-Touchscreen-events` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/070-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/075-mangohud-supported` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/400-set_gpu_overclock` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/500-enable-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/bin/achievements` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8250/bin/analog_sticks_ledcontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8250/bin/battery_led_status` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8250/bin/fancontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8250/bin/gpu_overclock` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8250/bin/ledcontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/post/001-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/post/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/post/003-audio` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/pre/001-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/pre/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/001-device_config` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/002-audio_path` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/005-thermal_path` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/009-serial-number-path` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/010-governors` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/020-fan_control` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/030-analog_leds` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/030-led-control` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/030-suspend_mode` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/040-affinity` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/065-Touchscreen-events` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/070-modifiers` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/075-mangohud-supported` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/090-ui_service` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/091-ui_shader` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/095-force_zink` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/096-cpuidle` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/500-enable-led` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/bin/fancontrol` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8550/bin/gpu_overclock` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8550/sleep.d/post/001-led` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/sleep.d/post/002-freq` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/sleep.d/pre/001-led` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8550/sleep.d/pre/002-freq` | H700, SM8550, VM | SM8550 | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/002-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/005-thermal_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/020-fan_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/030-analog_leds` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/030-led-control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/030-suspend_mode` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/050-retroarch-configs` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/061-yabasanshiro_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/065-Touchscreen-events` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/070-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/075-mangohud-supported` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/095-force_zink` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/500-enable-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/bin/fancontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8650/bin/gpu_overclock` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8650/sleep.d/post/001-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/sleep.d/post/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/sleep.d/pre/001-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8650/sleep.d/pre/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/001-device_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/002-audio_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/002-turbo-mode_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/005-thermal_path` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/010-governors` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/020-fan_control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/030-analog_leds` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/030-led-control` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/030-suspend_mode` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/040-affinity` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/050-retroarch-configs` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/060-game_settings` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/061-yabasanshiro_config` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/065-Touchscreen-events` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/070-modifiers` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/075-mangohud-supported` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/090-ui_service` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/091-ui_shader` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/095-force_zink` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/500-enable-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); autostart:16-28 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/bin/fancontrol` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8750/bin/gpu_overclock` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); its caller's platforms/${HW_DEVICE}/bin path | tree |
| `hardware/quirks/platforms/SM8750/sleep.d/post/001-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/sleep.d/post/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/sleep.d/pre/001-led` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/platforms/SM8750/sleep.d/pre/002-freq` | H700, SM8550, VM | none | quirks/package.mk:16-18 (copies every platform); sleep.sh:84 (HW_DEVICE) | tree |
| `hardware/quirks/profile.d/999-export` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:86-89; sourced by /etc/profile | tree |
| `hardware/quirks/system.d/led-poweroff.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; quirks/package.mk:24 (enable_service); multi-user.target.wants (quirks/package.mk:24) | tree |
| `hardware/quirks/system.d/volume-fixup.service` | H700, SM8550, VM | none | scripts/install:107-110; enabled only when DEVICE=RK3566 (quirks/package.mk:25-28) | tree |
| `sysutils/autostart/package.mk` | — (recipe) | build | sysutils/autostart/package.mk | tree |
| `sysutils/autostart/profile.d/002-autostart` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:86-89 | tree |
| `sysutils/autostart/sources/autostart` | H700, SM8550, VM | H700, SM8550, VM | sysutils/autostart/package.mk | tree |
| `sysutils/autostart/sources/daemons/005-fstrim` | H700, SM8550, VM | H700, SM8550, VM | sysutils/autostart/package.mk | tree |
| `sysutils/autostart/system.d/rocknix-autostart.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; rocknix.target.wants, the default target (rocknix/package.mk:85) | tree |
| `sysutils/avfs/package.mk` | — (recipe) | build | sysutils/avfs/package.mk | tree |
| `sysutils/bash/package.mk` | — (recipe) | build | sysutils/bash/package.mk | tree |
| `sysutils/btop/package.mk` | — (recipe) | build | sysutils/btop/package.mk | tree |
| `sysutils/btrfs-progs/package.mk` | — (recipe) | build | sysutils/btrfs-progs/package.mk | tree |
| `sysutils/busybox/config/busybox-host.conf` | none (the host tool) | build | busybox/package.mk:65 (configure_host) | tree |
| `sysutils/busybox/config/busybox-init.conf` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:101-102 (the initramfs busybox) | tree |
| `sysutils/busybox/config/busybox-target.conf` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:75-76 (compiled into /usr/bin/busybox) | tree |
| `sysutils/busybox/config/httpd.conf` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:141-144 | tree |
| `sysutils/busybox/config/inputrc` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:141-144 | tree |
| `sysutils/busybox/config/profile` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:141-144 | tree |
| `sysutils/busybox/config/suspend-modules.conf` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:141-144 | tree |
| `sysutils/busybox/default.d/crond.conf` | none | none | busybox/package.mk:193-201 (CRON_SUPPORT, "no" at distributions/ROCKNIX/options:177) | tree |
| `sysutils/busybox/package.mk` | — (recipe) | build | sysutils/busybox/package.mk | tree |
| `sysutils/busybox/profile.d/098-busybox` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:86-89 | tree |
| `sysutils/busybox/scripts/dthelper` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:122-136 | tree |
| `sysutils/busybox/scripts/fs-resize` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:122-136 | tree |
| `sysutils/busybox/scripts/functions` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:135 and :226 | tree |
| `sysutils/busybox/scripts/getedid` | VM | VM | busybox/package.mk:121 (x86_64 only) | tree |
| `sysutils/busybox/scripts/init` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:227 (initramfs /init, PID 1) | tree |
| `sysutils/busybox/scripts/kernel-overlays-setup` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:122-136 | tree |
| `sysutils/busybox/scripts/lsb_release` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:122-136 | tree |
| `sysutils/busybox/scripts/pastebinit` | H700, SM8550, VM | H700, SM8550, VM | busybox/package.mk:122-136 | tree |
| `sysutils/busybox/sleep.d.serial/99-suspend-modules.sh` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:127-130 | tree |
| `sysutils/busybox/sources/console-tools/evtest.c` | H700, SM8550, VM | H700, SM8550, VM | the evtest applet (IF_EVTEST) in /usr/bin/busybox; scripts/init:528 calls it | tree |
| `sysutils/busybox/sysctl.d/99-coredump.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:132-135 | tree |
| `sysutils/busybox/sysctl.d/cdrom.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:132-135 | tree |
| `sysutils/busybox/sysctl.d/hang-policy.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:132-135 | tree |
| `sysutils/busybox/sysctl.d/memory.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:132-135 | tree |
| `sysutils/busybox/system.d.opt/cron-defaults.service` | none | none | busybox/package.mk:193-201 (CRON_SUPPORT, "no" at distributions/ROCKNIX/options:177) | tree |
| `sysutils/busybox/system.d.opt/cron.service` | none | none | busybox/package.mk:193-201 (CRON_SUPPORT, "no" at distributions/ROCKNIX/options:177) | tree |
| `sysutils/busybox/system.d/fs-resize.service` | H700, SM8550, VM | first boot after a resize request | scripts/install:107-110; fs-resize.target; scripts/init:1363-1364 (/storage/.please_resize_me) | tree |
| `sysutils/busybox/system.d/fs-resize.target` | H700, SM8550, VM | first boot after a resize request | scripts/install:107-110; scripts/init:1363-1364 | tree |
| `sysutils/busybox/system.d/proc-sys-fs-binfmt_misc.mount` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; local-fs.target.wants (busybox/package.mk:190) | tree |
| `sysutils/busybox/system.d/shell.service` | H700, SM8550, VM | only when booted with `textmode` on the kernel command line | scripts/install:107-110; textmode.target.wants (busybox/package.mk:187); the target is selected by scripts/init:1215-1216 | tree |
| `sysutils/busybox/system.d/show-version.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; basic.target.wants (busybox/package.mk:188) | tree |
| `sysutils/busybox/system.d/storage-log.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; var-log.mount's Requires= (var-log.mount:14) | tree |
| `sysutils/busybox/system.d/textmode.target` | H700, SM8550, VM | only when booted with `textmode` | scripts/install:107-110; scripts/init:1215-1216 | tree |
| `sysutils/busybox/system.d/var-log.mount` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; no link; active on the guest (journald's mount dependency on /var/log); ConditionPathExists=!/storage/.cache/volatile-log | tree |
| `sysutils/busybox/system.d/var.mount` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; local-fs.target.wants (busybox/package.mk:189) | tree |
| `sysutils/busybox/tmpfiles.d/z_01_busybox.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:91-94 | tree |
| `sysutils/drm_tool/package.mk` | — (recipe) | build | sysutils/drm_tool/package.mk | tree |
| `sysutils/file/package.mk` | — (recipe) | build | sysutils/file/package.mk | tree |
| `sysutils/fuse2/package.mk` | — (recipe) | build | sysutils/fuse2/package.mk | tree |
| `sysutils/gptfdisk/package.mk` | — (recipe) | build | sysutils/gptfdisk/package.mk | tree |
| `sysutils/grep/package.mk` | — (recipe) | build | sysutils/grep/package.mk | tree |
| `sysutils/i2c-tools/package.mk` | — (recipe) | build | sysutils/i2c-tools/package.mk | tree |
| `sysutils/kmod/modprobe.d/aliases.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:152-155 | tree |
| `sysutils/kmod/modprobe.d/i2c.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:152-155 | tree |
| `sysutils/kmod/package.mk` | — (recipe) | build | sysutils/kmod/package.mk | tree |
| `sysutils/libevdev/package.mk` | — (recipe) | build | sysutils/libevdev/package.mk | tree |
| `sysutils/libiio/package.mk` | — (recipe) | build | sysutils/libiio/package.mk | tree |
| `sysutils/lsof/package.mk` | — (recipe) | build | sysutils/lsof/package.mk | tree |
| `sysutils/nvtop/package.mk` | — (recipe) | build | sysutils/nvtop/package.mk | tree |
| `sysutils/powerstate/package.mk` | — (recipe) | build | sysutils/powerstate/package.mk | tree |
| `sysutils/powerstate/sources/powerstate.sh` | H700, SM8550, VM | H700, SM8550, VM | sysutils/powerstate/package.mk | tree |
| `sysutils/powerstate/system.d/powerstate.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; multi-user.target.wants (powerstate/package.mk:20) | tree |
| `sysutils/sleep/package.mk` | — (recipe) | build | sysutils/sleep/package.mk | tree |
| `sysutils/sleep/sources/modules.bad` | H700, SM8550, VM | H700, SM8550, VM | sysutils/sleep/package.mk | tree |
| `sysutils/sleep/sources/sleep.conf` | H700, SM8550, VM | H700, SM8550, VM | sysutils/sleep/package.mk | tree |
| `sysutils/sleep/sources/sleep.sh` | H700, SM8550, VM | H700, SM8550, VM | sysutils/sleep/package.mk | tree |
| `sysutils/squashfs-tools/package.mk` | — (recipe) | build | sysutils/squashfs-tools/package.mk | tree |
| `sysutils/squashfuse/package.mk` | — (recipe) | build | sysutils/squashfuse/package.mk | tree |
| `sysutils/system-utils/package.mk` | — (recipe) | build | sysutils/system-utils/package.mk | tree |
| `sysutils/system-utils/sources/autostart/AMD64/002-overclock` | none | none | system-utils/package.mk:30-34 (only sources/autostart/${DEVICE}) | tree |
| `sysutils/system-utils/sources/autostart/common/098-deviceutils` | H700, SM8550, VM | H700, SM8550, VM | system-utils/package.mk:14-15; autostart:50-54 | tree |
| `sysutils/system-utils/sources/config/fancontrol.conf` | H700, SM8550, VM | read by fancontrol where it runs (SM8550) | system-utils/package.mk:39-40 (as /usr/config/fancontrol.conf.sample) | tree |
| `sysutils/system-utils/sources/devices/AMD64/overclock` | none | none | system-utils/package.mk:27-29 (only sources/devices/${DEVICE}) | tree |
| `sysutils/system-utils/sources/devices/AMD64/set_epp` | none | none | system-utils/package.mk:27-29 (only sources/devices/${DEVICE}) | tree |
| `sysutils/system-utils/sources/devices/GENERIC_X64/video_sense` | VM | VM | system-utils/package.mk:27-29 (only sources/devices/${DEVICE}) | tree |
| `sysutils/system-utils/sources/devices/RK3399/headphone_sense` | none | none | system-utils/package.mk:27-29 (only sources/devices/${DEVICE}) | tree |
| `sysutils/system-utils/sources/devices/RK3399/internalwifi` | none | none | system-utils/package.mk:27-29 (only sources/devices/${DEVICE}) | tree |
| `sysutils/system-utils/sources/devices/RK3399/video_sense` | none | none | system-utils/package.mk:27-29 (only sources/devices/${DEVICE}) | tree |
| `sysutils/system-utils/sources/devices/RK3566/headphone_sense` | none | none | system-utils/package.mk:27-29 (only sources/devices/${DEVICE}) | tree |
| `sysutils/system-utils/sources/devices/S922X/headphone_sense` | none | none | system-utils/package.mk:27-29 (only sources/devices/${DEVICE}) | tree |
| `sysutils/system-utils/sources/scripts/analog_sticks_ledcontrol` | H700, SM8550, VM | H700, SM8550, VM | system-utils/package.mk:17-26 | tree |
| `sysutils/system-utils/sources/scripts/battery_led_status` | H700, SM8550, VM | SM8550 (platforms/SM8550/030-led-control:7) | system-utils/package.mk:17-26; started by 098-deviceutils:31-37 (DEVICE_BATTERY_LED_STATUS) | tree |
| `sysutils/system-utils/sources/scripts/fancontrol` | H700, SM8550, VM | SM8550 (platforms/SM8550/020-fan_control:9) | system-utils/package.mk:17-26; started by 098-deviceutils:7-13 (DEVICE_HAS_FAN) | tree |
| `sysutils/system-utils/sources/scripts/hdmi_sense` | H700, SM8550, VM | H700, SM8550, VM | system-utils/package.mk:17-26 | tree |
| `sysutils/system-utils/sources/scripts/headphone_sense` | H700, SM8550, VM | none of the three sets it true (VM false; H700, SM8550 per device, T29's) | system-utils/package.mk:17-26; started by 098-deviceutils:15-21 (DEVICE_FAKE_JACKSENSE) | tree |
| `sysutils/system-utils/sources/scripts/input_sense` | H700, SM8550, VM | H700, SM8550, VM | system-utils/package.mk:17-26 | tree |
| `sysutils/system-utils/sources/scripts/ledcontrol` | H700, SM8550, VM | H700, SM8550, VM | system-utils/package.mk:17-26 | tree |
| `sysutils/system-utils/sources/scripts/output_monitor` | H700, SM8550, VM | H700, SM8550, VM | system-utils/package.mk:17-26 | tree |
| `sysutils/system-utils/sources/scripts/turbomode` | H700, SM8550, VM | H700, SM8550, VM | system-utils/package.mk:17-26 | tree |
| `sysutils/system-utils/system.d/batteryledstatus.service` | H700, SM8550, VM | SM8550 | scripts/install:107-110; no .wants link (guest s2c); started by 098-deviceutils:31-37 (SM8550) | tree |
| `sysutils/system-utils/system.d/fancontrol.service` | H700, SM8550, VM | SM8550 | scripts/install:107-110; no .wants link (guest s2c); started by 098-deviceutils:7-13 (SM8550) | tree |
| `sysutils/system-utils/system.d/headphones.service` | H700, SM8550, VM | per device (T29's); VM no | scripts/install:107-110; no .wants link (guest s2c); started by 098-deviceutils:15-21 (DEVICE_FAKE_JACKSENSE) | tree |
| `sysutils/system-utils/system.d/input.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; no .wants link (guest s2c); started by 098-deviceutils:39-40 (always) | tree |
| `sysutils/system-utils/system.d/video.service` | H700, SM8550, VM | VM (H700, SM8550 per device: T29's) | scripts/install:107-110; no .wants link (guest s2c); started by 098-deviceutils:23-29 (DEVICE_HAS_HDMI; VM true) | tree |
| `sysutils/system-utils/udev.d/99-hdmi.rules` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:112-115 | tree |
| `sysutils/system-utils/udev.d/99-input.rules` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:112-115 | tree |
| `sysutils/systemd/config/hosts.conf` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/hwdb.d/99-osmcrf.hwdb` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/hwdb.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/logind.conf.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/modules-load.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/resolved.conf.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/sleep.conf.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/sysctl.d/99-rocknix-networking.conf` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/sysctl.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/sysctl.d/rocknix.conf` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/system.conf.d/10-shutdown-timeout.conf` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 and :275 (/etc/systemd/system.conf.d) | tree |
| `sysutils/systemd/config/system.conf.d/20-watchdog.conf` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 and :275 (/etc/systemd/system.conf.d) | tree |
| `sysutils/systemd/config/system.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/timesyncd.conf.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/tmpfiles.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/config/udev.rules.d/README` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot) | tree |
| `sysutils/systemd/hwdb.d/10-adc-keys.hwdb` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:117-120 | tree |
| `sysutils/systemd/hwdb.d/20-joypad.hwdb` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:117-120 | tree |
| `sysutils/systemd/hwdb.d/61-thor-ft5x06.hwdb` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:117-120 | tree |
| `sysutils/systemd/hwdb.d/70-local-keyboard.hwdb` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:117-120 | tree |
| `sysutils/systemd/package.mk` | — (recipe) | build | sysutils/systemd/package.mk | tree |
| `sysutils/systemd/profile.d/090-systemd.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:86-89 | tree |
| `sysutils/systemd/scripts/network-base-setup` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:231-237 | tree |
| `sysutils/systemd/scripts/systemd-machine-id-setup` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:231-237 | tree |
| `sysutils/systemd/scripts/systemd-timesyncd-setup` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:231-237 | tree |
| `sysutils/systemd/scripts/usercache-setup` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:231-237 | tree |
| `sysutils/systemd/scripts/userconfig-setup` | H700, SM8550, VM | H700, SM8550, VM | systemd/package.mk:231-237 | tree |
| `sysutils/systemd/system.d/debugconfig.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; sysinit.target.wants (guest s2c) | tree |
| `sysutils/systemd/system.d/flash.mount.d/dependencies.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110 | tree |
| `sysutils/systemd/system.d/machine-id.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; sysinit.target.wants (guest s2c) | tree |
| `sysutils/systemd/system.d/network-base.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; network.target.wants (guest s2c) | tree |
| `sysutils/systemd/system.d/storage.mount.d/dependencies.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110 | tree |
| `sysutils/systemd/system.d/systemd-pstore.service.d/rocknix.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110 | tree |
| `sysutils/systemd/system.d/systemd-resolved.service.d/override.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110 | tree |
| `sysutils/systemd/system.d/systemd-timesyncd-setup.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; sysinit.target.wants (guest s2c) | tree |
| `sysutils/systemd/system.d/usercache.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; sysinit.target.wants (guest s2c) | tree |
| `sysutils/systemd/system.d/userconfig.service` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:107-110; sysinit.target.wants (systemd/package.mk:326) | tree |
| `sysutils/systemd/tmpfiles.d/connectivity.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:91-94 | tree |
| `sysutils/systemd/tmpfiles.d/z_01_rocknix.conf` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:91-94 | tree |
| `sysutils/systemd/udev.d/60-not-joysticks.rules` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:112-115 | tree |
| `sysutils/systemd/udev.d/80-clock.rules` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:112-115 | tree |
| `sysutils/udevil/config/udevil.conf` | H700, SM8550, VM | H700, SM8550, VM | sysutils/udevil/package.mk | tree |
| `sysutils/udevil/package.mk` | — (recipe) | build | sysutils/udevil/package.mk | tree |
| `sysutils/udevil/system.d/udevil-mount@.service` | H700, SM8550, VM | when a USB-storage sd* or sr* medium appears | scripts/install:107-110; 95-udevil-mount.rules (udevil/package.mk:40) | tree |
| `sysutils/udevil/udev.d/95-udevil-mount.rules` | H700, SM8550, VM | H700, SM8550, VM | scripts/install:112-115 | tree |
| `sysutils/umtprd/etc/umtprd.conf` | H700, SM8550, VM | H700, SM8550, VM | sysutils/umtprd/package.mk | tree |
| `sysutils/umtprd/package.mk` | — (recipe) | build | sysutils/umtprd/package.mk | tree |
| `sysutils/usb-modeswitch/package.mk` | — (recipe) | build | sysutils/usb-modeswitch/package.mk | tree |
| `sysutils/util-linux/config/swap.conf` | H700, SM8550, VM | H700, SM8550, VM | sysutils/util-linux/package.mk | tree |
| `sysutils/util-linux/package.mk` | — (recipe) | build | sysutils/util-linux/package.mk | tree |
| `sysutils/util-linux/system.d/fstrim.service` | H700, SM8550, VM | only when fstrim.enabled=1 (0 by default) | scripts/install:107-110; fstrim.timer; autostart/sources/daemons/005-fstrim; rocknix system.cfg:55 | tree |
| `sysutils/util-linux/system.d/fstrim.timer` | H700, SM8550, VM | only when fstrim.enabled=1 (0 by default) | scripts/install:107-110; autostart/sources/daemons/005-fstrim; rocknix system.cfg:55 | tree |

## The units

29 units, **none with `User=`, `Group=` or `DynamicUser=`** (`10b`; the guest's `systemctl show -P User` read `runs-as=root` for all 25 installed there). *Pulled in by* is what makes a unit run: `systemctl is-enabled` reads `disabled` for units linked under `/usr/lib/systemd/system/*.wants` (guest s2), so the links are the evidence (guest s2c). `enable_service` (`config/functions:1700-1720`) makes those links from `WantedBy=`.

| Unit | ExecStart (masked) | `User=` | Writable path it reads or runs | Guard | Pulled in by (enabled on) | proved |
| --- | --- | --- | --- | --- | --- | --- |
| `led-poweroff.service` | `/bin/true`; stop `ledcontrol poweroff` | root | none | -- | multi-user.wants (quirks/package.mk:24) | guest |
| `volume-fixup.service` | `platforms/RK3566/bin/volumealign` | root | none | -- | not on a shipped image (enabled only for RK3566, quirks/package.mk:25-28) | tree |
| `rocknix-autostart.service` | `bash -a -c 'source /etc/profile && exec /usr/bin/autostart'` | root | **`/storage/.config/autostart/*` executed** (`autostart:71-77`); **`/storage/.config/profile.d/*` sourced** (`/etc/profile:19-23`) | autostart: none (no `-f`, `${script}` unquoted, guest s5b); profile: `-f` (`:20`), unquoted `. ${CONFIG}` | rocknix.target.wants, the default target (rocknix/package.mk:85) | guest |
| `cron-defaults.service` | `cp /usr/share/services/crond.conf /storage/.cache/services/` | root | `/storage/.cache/services/` | `ConditionPathExists=!` twice | **not installed on any shipped image** (CRON_SUPPORT=no, distributions/ROCKNIX/options:177; busybox/package.mk:193-201) | guest |
| `cron.service` | `crond -f -S` over `/storage/.cache/cron/crontabs` | root | `/storage/.cache/cron/crontabs` (would be) | `ConditionPathExists=` | not installed on any shipped image (as above) | guest |
| `fs-resize.service` | `/usr/lib/rocknix/fs-resize` | root | `/storage/.please_resize_me` (a marker selects the target) | the marker; `scripts/init:1363-1364` | fs-resize.target, by init when the marker exists | tree |
| `fs-resize.target` | -- | root | -- | -- | scripts/init:1363-1364 | tree |
| `proc-sys-fs-binfmt_misc.mount` | `binfmt_misc` on `/proc/sys/fs/binfmt_misc` | root | none | `nosuid,nodev,noexec` | local-fs.wants (busybox/package.mk:190) | guest |
| `shell.service` | `sh -c '... . /etc/profile; exec /bin/sh'` on tty1 | root | `/etc/profile` -> `/storage/.config/profile.d/*`; a root shell, no login | **only a `textmode` boot** (scripts/init:1215-1216, the kernel command line) | textmode.target.wants (busybox/package.mk:187); inactive on the guest | guest |
| `show-version.service` | `lsb_release` | root | none | `ConditionKernelCommandLine=!morequiet` | basic.wants (busybox/package.mk:188) | guest |
| `storage-log.service` | `mkdir -p /storage/.cache/log/journal /storage/.cache/log/pstore` | root | `/storage/.cache/log` (created) | -- | var-log.mount's `Requires=` | guest |
| `textmode.target` | -- | root | -- | -- | scripts/init:1215-1216 | tree |
| `var-log.mount` | bind `/storage/.cache/log` on `/var/log` | root | `/storage/.cache/log`; **`/storage/.cache/volatile-log` turns it off** | `ConditionKernelCommandLine=!installer` | active on the guest; no `.wants` link | guest |
| `var.mount` | tmpfs on `/var` | root | none | -- | local-fs.wants (busybox/package.mk:189) | guest |
| `powerstate.service` | `/usr/bin/powerstate`, `EnvironmentFile=/etc/profile` | root | `/etc/profile` sourced by the script (`powerstate.sh:11`) -> `/storage/.config/profile.d/*` | `-f`, unquoted | multi-user.wants (powerstate/package.mk:20) | guest |
| `batteryledstatus.service` | `/usr/bin/battery_led_status` | root | `/etc/profile` via the script | `ConditionPathExists=/usr/bin/battery_led_status` | no link; `098-deviceutils:31-37` (DEVICE_BATTERY_LED_STATUS: SM8550) | guest |
| `fancontrol.service` | `/usr/bin/fancontrol` -> `quirks/devices/${QUIRK_DEVICE}/bin/fancontrol` | root | `/etc/profile` | -- | no link; `098-deviceutils:7-13` (DEVICE_HAS_FAN: SM8550) | guest |
| `headphones.service` | `/usr/bin/headphone_sense` | root | `/etc/profile` | -- | no link; `098-deviceutils:15-21` (DEVICE_FAKE_JACKSENSE) | guest |
| `input.service` | `/usr/bin/input_sense` (539 fork-own lines) | root | `/etc/profile`; the settings it reads | -- | no link; `098-deviceutils:39-40`, always; running as uid 0 on the guest | guest |
| `video.service` | `/usr/bin/video_sense` | root | `/etc/profile` | -- | no link; `098-deviceutils:23-29` (DEVICE_HAS_HDMI: the RG552 and the QEMU machine, both with `video_sense`); running as uid 0 on the guest | guest |
| `debugconfig.service` | `cp /usr/share/debugconf/*.conf /run/rocknix/debug` | root | **`/storage/.cache/debug.rocknix` turns it on** | `ConditionKernelCommandLine=\|debugging`, `ConditionPathExists=\|...` | sysinit.wants | guest |
| `machine-id.service` | `systemd-machine-id-setup` | root | `/storage/.cache/machine-id`, `/storage/.cache/systemd-machine-id` | -- | sysinit.wants | guest |
| `network-base.service` | `network-base-setup` (fork-own) | root | `/storage/.config/hosts.conf`, `/storage/.config/resolv.conf`; `/etc/profile` | -- | network.wants | guest |
| `systemd-timesyncd-setup.service` | `systemd-timesyncd-setup` | root | none named | -- | sysinit.wants | guest |
| `usercache.service` | `usercache-setup` | root | `/storage/.cache/`, `services`, **`shadow`** | replaces a file without a root entry (`usercache-setup:18`) | sysinit.wants | guest |
| `userconfig.service` | `userconfig-setup` (fork-own) | root | `/storage/.config/` (rsync from `/usr/config`); **`/storage/.ssh` written as a file when `/usr/config/ssh/authorized_keys` exists** (#740) | `/storage/.configured` (first boot only); `/usr/config/ssh` exists only on a build with `LOCAL_SSH_KEYS_FILE` (rocknix/package.mk:36-40), absent on the guest | sysinit.wants (systemd/package.mk:326) | guest |
| `udevil-mount@.service` | `udevil --mount %I`; post `samba-autoshare` | root | **an inserted USB-storage or optical medium** | `udevil.conf`: `nosuid,noexec,nodev` for every type **but btrfs** (`default_options_btrfs = compress=zstd:3`); `allowed_users = *` | 95-udevil-mount.rules (udevil/package.mk:40); `samba-autoshare` absent on the image (SAMBA_SUPPORT=no) | guest |
| `fstrim.service` | `fstrim --all`; `touch /storage/.cache/fstrim.run` | root | `/storage/.cache/fstrim.run` | -- | fstrim.timer, only when `fstrim.enabled=1` (`system.cfg:55`: 0) | tree |
| `fstrim.timer` | weekly | root | -- | -- | `autostart/sources/daemons/005-fstrim` | guest |

## busybox

- **The pin:** 1.36.1 (`busybox/package.mk:7`), fetched over **plain http** (`:11`). Upstream at `651150fc88`: **1.38.0 over https**, with seven patches: six A (`0001`-`0006`, `0006-prevent-root-weak-passwd` among them) and one R (`busybox-10-...MS_BIND` -> `0010`, R056), renames of the override's own `busybox-0X-*.patch`. The generic LibreELEC recipe's 1.38.0 is shadowed (#997, T14's).
- **On the image:** `/usr/bin/busybox`, **mode 4755, owner root**, the only setuid file in `/bin /usr/bin /sbin /usr/sbin` (guest s4). The mode is set at `busybox/package.mk:177` (the fakeroot script) and `:209`. `CONFIG_FEATURE_SUID=y` (`:30`) makes busybox drop or keep privilege per applet.

| Applet | Config line | On the image (guest s4) | Caller in the tree (`22`) | proved |
| --- | --- | --- | --- | --- |
| `su` | `CONFIG_SU=y` `:556` | applet, `/usr/bin/su` | **none** | guest (s4); tree (`22`) |
| `login` | `CONFIG_LOGIN=y` `:549` | applet, `/usr/bin/login` | **none** (six prose hits) | guest (s4); tree (`22`) |
| `passwd` | `CONFIG_PASSWD=y` `:554` | applet, `/usr/bin/passwd` | **none** (one `smb.conf` setting) | guest (s4); tree (`22`) |
| `httpd` + CGI | `:888`, `:894` | applet, `/usr/sbin/httpd`; `/etc/httpd.conf` and `/usr/www` installed (`package.mk:143`, `:162-166`) | **none** | guest (s4); tree (`22`) |
| `nc` | `:950` | applet | 3: `easyrpg.sh:53`, `freej2me.sh:24` (connectivity probes), `rocknix-fake-suspend:53` | guest (s4); tree (`22`) |
| `udhcpd` | `:1010` | applet | 1: `usbgadget:238` | guest (s4); tree (`22`) |
| `evtest` | (the fork's applet, `sources/console-tools/evtest.c`) | in the initramfs busybox | `scripts/init:528` | tree |

## The upstream delta

**44 M** (`23`, each with its upstream commits and a stage-B note where a
finding lies on it):

| File | Diff | Upstream commits | Fork commits since the base | A finding on it, and its state at `651150fc88` |
| --- | --- | --- | --- | --- |
| `hardware/quirks/package.mk` | +4 -0 | 48b98a02d7 | 0 | no finding at stage B |
| `hardware/quirks/platforms/RK3326/090-ui_service` | +10 -4 | 075a7c303b | 0 | no finding at stage B |
| `hardware/quirks/platforms/RK3326/sleep.d/post/002-freq` | +6 -1 | a7b7677202 | 0 | no finding at stage B |
| `hardware/quirks/platforms/RK3326/sleep.d/pre/002-freq` | +3 -1 | a7b7677202 | 0 | no finding at stage B |
| `hardware/quirks/platforms/RK3566/090-ui_service` | +14 -4 | e48ea0f5b5 075a7c303b | 0 | no finding at stage B |
| `hardware/quirks/platforms/RK3576/090-ui_service` | +15 -4 | a67cd08feb 075a7c303b | 0 | no finding at stage B |
| `hardware/quirks/platforms/RK3588/090-ui_service` | +1 -0 | 075a7c303b | 0 | no finding at stage B |
| `hardware/quirks/platforms/S922X/030-suspend_mode` | +6 -7 | b48d63c445 | 0 | no finding at stage B |
| `hardware/quirks/platforms/S922X/090-ui_service` | +7 -0 | e80b64f531 075a7c303b | 0 | no finding at stage B |
| `hardware/quirks/platforms/SM6115/004-usb-autosuspend` | +3 -0 | 94d6314624 | 0 | no finding at stage B |
| `hardware/quirks/platforms/SM6115/bin/analog_sticks_ledcontrol` | +6 -8 | 6ac52e0c04 | 0 | no finding at stage B |
| `hardware/quirks/platforms/SM6115/bin/battery_led_status` | +10 -51 | 6ac52e0c04 | 0 | no finding at stage B |
| `hardware/quirks/platforms/SM6115/bin/ledcontrol` | +4 -7 | 6ac52e0c04 | 0 | no finding at stage B |
| `hardware/quirks/profile.d/999-export` | +9 -3 | 075a7c303b abfdcfb57f 0c43a50420 | 1 | no finding at stage B |
| `sysutils/autostart/sources/autostart` | +2 -2 | a98a3066f5 | 0 | F-AUTOSTART (the custom loop: no `-f`, unquoted) **stands**: upstream changed only the lock path (`:85-86`) |
| `sysutils/busybox/config/busybox-host.conf` | +20 -3 | be9a5e4a81 | 0 | no finding at stage B |
| `sysutils/busybox/config/busybox-init.conf` | +28 -11 | c92afac014 be9a5e4a81 | 0 | no finding at stage B |
| `sysutils/busybox/config/busybox-target.conf` | +27 -6 | be9a5e4a81 | 0 | the flagged applets: none of the eight flags changes upstream: **stands** |
| `sysutils/busybox/package.mk` | +4 -7 | 033f0ea96d be9a5e4a81 | 0 | the plain-http `PKG_URL` and the 1.36.1 pin: **settled by the next base merge** (1.38.0, https) |
| `sysutils/busybox/profile.d/098-busybox` | +1 -1 | 033f0ea96d | 0 | no finding at stage B |
| `sysutils/busybox/scripts/init` | +5 -14 | 03204074ef a98a3066f5 | 1 | no finding at stage B |
| `sysutils/busybox/sysctl.d/cdrom.conf` | +2 -2 | 54acd9556f | 0 | no finding at stage B |
| `sysutils/busybox/system.d/storage-log.service` | +1 -4 | none | 1 | no finding at stage B |
| `sysutils/busybox/system.d/var-log.mount` | +2 -11 | none | 1 | no finding at stage B |
| `sysutils/busybox/tmpfiles.d/z_01_busybox.conf` | +0 -1 | 8bce25b3b7 | 0 | part of `8bce25b3b7` (crash logging): collision C-1 |
| `sysutils/nvtop/package.mk` | +1 -13 | none | 1 | no finding at stage B |
| `sysutils/powerstate/sources/powerstate.sh` | +18 -26 | none | 1 | no finding at stage B |
| `sysutils/powerstate/system.d/powerstate.service` | +0 -7 | none | 1 | no finding at stage B |
| `sysutils/sleep/sources/sleep.sh` | +3 -0 | bb9e42e2a0 | 0 | no finding at stage B |
| `sysutils/squashfs-tools/package.mk` | +3 -28 | 6103571f67 | 0 | no finding at stage B |
| `sysutils/systemd/config/system.conf.d/10-shutdown-timeout.conf` | +1 -0 | c92afac014 | 0 | no finding at stage B |
| `sysutils/systemd/hwdb.d/70-local-keyboard.hwdb` | +1 -0 | 03204074ef | 0 | no finding at stage B |
| `sysutils/systemd/package.mk` | +98 -42 | 03204074ef 9883f84793 75e2468cef 8bce25b3b7 401028b691 83c72c6a47 ed5aeaa34a 687fce45ff f33f412916 dc14669f69 bb9e42e2a0 3b4f80dfe3 adb5cbfea4 a98a3066f5 c22cda5f06 c92afac014 033f0ea96d | 2 | collision C-2 (the sysctls, `54acd9556f`) and C-1 (`8bce25b3b7`) land here; see below |
| `sysutils/systemd/scripts/network-base-setup` | +4 -107 | none | 8 | no finding at stage B |
| `sysutils/systemd/scripts/userconfig-setup` | +4 -12 | none | 2 | #740's `cp ... /storage/.ssh` is the same at both: **stands** (the diff is the fork's `es_savestates.cfg`) |
| `sysutils/systemd/system.d/network-base.service` | +0 -9 | none | 1 | no finding at stage B |
| `sysutils/systemd/tmpfiles.d/z_01_rocknix.conf` | +0 -5 | none | 1 | no finding at stage B |
| `sysutils/system-utils/sources/devices/RK3399/video_sense` | +2 -2 | 03204074ef | 0 | no finding at stage B |
| `sysutils/system-utils/sources/scripts/input_sense` | +54 -42 | 72a96e2d8b 0bf9356953 367ee23654 f4fc3dc419 | 2 | no finding at stage B |
| `sysutils/system-utils/system.d/input.service` | +2 -0 | bb9e42e2a0 | 0 | no finding at stage B |
| `sysutils/udevil/udev.d/95-udevil-mount.rules` | +3 -3 | dc781c0c75 | 0 | the btrfs default lives in `udevil.conf`, unchanged upstream: **stands**; the rule gains `--no-block` |
| `sysutils/util-linux/config/swap.conf` | +0 -1 | dc14669f69 | 0 | no finding at stage B |
| `sysutils/util-linux/package.mk` | +5 -4 | dc14669f69 c92afac014 dc19c754a2 | 0 | no finding at stage B |
| `sysutils/util-linux/system.d/fstrim.service` | +1 -0 | bb9e42e2a0 | 0 | no finding at stage B |

**20 D** (`19`): **9** upstream never had (absent at `c445081a59`), **2** the fork carries and upstream removed, and **9** upstream deleted:

- `hardware/quirks/platforms/GENERIC_X64/090-ui_service`: base-lacks; none
- `hardware/quirks/platforms/GENERIC_X64/091-ui_shader`: base-lacks; none
- `hardware/quirks/platforms/GENERIC_X64/092-retroarch-surface`: base-lacks; none
- `hardware/quirks/platforms/GENERIC_X64/095-cloud-ssh`: base-lacks; none
- `hardware/quirks/platforms/GENERIC_X64/097-retired-rescue-masks`: base-lacks; none
- `hardware/quirks/platforms/RK3576/sleep.d/pre/99-idle-only`: base-has; a98a3066f5 systemd: persist timesyncd clock and reboot on PI
- `hardware/quirks/platforms/SM6115/sleep.d/post/001-led`: base-has; 6ac52e0c04 sm6115: add mangmi air y
- `hardware/quirks/platforms/SM6115/sleep.d/post/002-freq`: base-has; 6ac52e0c04 sm6115: add mangmi air y
- `hardware/quirks/platforms/SM6115/sleep.d/pre/001-led`: base-has; 6ac52e0c04 sm6115: add mangmi air y
- `hardware/quirks/platforms/SM6115/sleep.d/pre/002-freq`: base-has; 6ac52e0c04 sm6115: add mangmi air y
- `sysutils/busybox/sysctl.d/99-coredump.conf`: base-has; 8bce25b3b7 systemd: log crashes in the journal without writi
- `sysutils/busybox/sysctl.d/hang-policy.conf`: base-lacks; none
- `sysutils/file/package.mk`: base-has; 6103571f67 Merge pull request #3470 from sunshineinabox/WIP_
- `sysutils/i2c-tools/package.mk`: base-has; 6103571f67 Merge pull request #3470 from sunshineinabox/WIP_
- `sysutils/system-utils/sources/devices/GENERIC_X64/video_sense`: base-lacks; none
- `sysutils/systemd/config/sysctl.d/99-rocknix-networking.conf`: base-has; 54acd9556f systemd: ship the distro sysctls in the image, dr
- `sysutils/systemd/config/sysctl.d/rocknix.conf`: base-has; 54acd9556f systemd: ship the distro sysctls in the image, dr
- `sysutils/systemd/config/system.conf.d/20-watchdog.conf`: base-lacks; none
- `sysutils/systemd/system.d/systemd-pstore.service.d/rocknix.conf`: base-lacks; none
- `sysutils/systemd/udev.d/80-clock.rules`: base-has; 899193e5af systemd: drop the hwclock udev rules, the kernel 

**42 A and 2 R** (`15`; the gptfdisk patch's name is written as a placeholder, its line matching the commit scanner's key shape):

- A `hardware/quirks/autostart/045-background-cpus`
- A `hardware/quirks/platforms/RK3576/021-sleep_mode`
- A `hardware/quirks/platforms/S922X/031-sleep_mode`
- A `hardware/quirks/platforms/SM4450/075-scanout-offload`
- A `hardware/quirks/platforms/SM6115/075-scanout-offload`
- A `hardware/quirks/platforms/SM8250/075-scanout-offload`
- A `hardware/quirks/platforms/SM8550/075-scanout-offload`
- A `hardware/quirks/platforms/SM8650/075-scanout-offload`
- A `hardware/quirks/platforms/SM8750/075-scanout-offload`
- A `hardware/quirks/system.d/duolite-bottom-screen.service`
- A `sysutils/busybox/patches/0001-halt-no-init.patch`
- A `sysutils/busybox/patches/0002-silence-crond-startup-logging.patch`
- A `sysutils/busybox/patches/0003-make-unicode-printable.patch`
- A `sysutils/busybox/patches/0004-revert-dd-fsync-change.patch`
- A `sysutils/busybox/patches/0005-update-shadow-or-passwd-not-both.patch`
- A `sysutils/busybox/patches/0006-prevent-root-weak-passwd.patch`
- R056 `sysutils/busybox/patches/busybox-10-add-MS_BIND-option-when-remouting-bind-mount.patch	projects/ROC`
- A `sysutils/gptfdisk/patches/<patch 0001>`
- A `sysutils/ntfs-3g_ntfsprogs/package.mk`
- A `sysutils/systemd/config/system.conf.d/20-crash.conf`
- A `sysutils/systemd/oomd/rules.d/games-swap.oomrule`
- A `sysutils/systemd/scripts/hwdb-update-cached`
- A `sysutils/systemd/scripts/low-memory-tunables`
- A `sysutils/systemd/scripts/rtc-offset`
- A `sysutils/systemd/sysctl.d/60-rocknix.conf`
- A `sysutils/systemd/system.d/background.slice`
- A `sysutils/systemd/system.d/debug-shell.service.d/rocknix.conf`
- A `sysutils/systemd/system.d/games.slice`
- A `sysutils/systemd/system.d/rtc-offset-sync.path`
- A `sysutils/systemd/system.d/rtc-offset-sync.service`
- A `sysutils/systemd/system.d/rtc-offset.service`
- A `sysutils/systemd/system.d/service.d/10-rocknix-thp.conf`
- A `sysutils/systemd/system.d/storage-timesync.service`
- A `sysutils/systemd/system.d/system.slice.d/10-rocknix.conf`
- A `sysutils/systemd/system.d/systemd-hwdb-update.service.d/rocknix.conf`
- A `sysutils/systemd/system.d/systemd-rfkill.service.d/rocknix.conf`
- A `sysutils/systemd/system.d/systemd-timesyncd.service.d/rocknix.conf`
- A `sysutils/systemd/system.d/systemd-udev-trigger.service.d/rocknix.conf`
- A `sysutils/systemd/system.d/udev-trigger-late.service`
- A `sysutils/systemd/system.d/udev-trigger-late.timer`
- A `sysutils/systemd/system.d/var-lib-systemd-timesync.mount`
- A `sysutils/systemd/udev.d/61-rocknix-internal-emmc.rules`
- A `sysutils/util-linux/patches/0001-fix-pkgconf.patch`
- R073 `sysutils/util-linux/patches/util-linux-02-enable-blkdiscard.patch `sysutil`

**The two collisions**, each a design sentence deferred to the coordinator, no edit:
- **C-1, crash logging:** `8bce25b3b7` (*log crashes in the journal without writing core files*) deletes the fork's `busybox/sysctl.d/99-coredump.conf` and changes `z_01_busybox.conf` and `systemd/package.mk`. The fork's core keeper (D-INFRA-011/012/013) reads core files. *Design:* when the next base merge lands, the fork either keeps its core pattern and keeper against upstream's journal-only crash logging, or yields and retires the keeper. That is a decision for the coordinator under the D-INFRA rows, not this lane's.
- **C-2, the sysctls:** `54acd9556f` (*ship the distro sysctls in the image, drop dead keys*) deletes `sysctl.d/rocknix.conf`, `99-rocknix-networking.conf`, `qdisc.conf`, `post-update` and `cdrom.conf`'s old form, and adds `60-rocknix.conf`. `hang-policy.conf` is the fork's own and has no upstream history. *Design:* the fork's `hang-policy.conf` and its `sysctl.d/rocknix.conf` keys are re-read against `60-rocknix.conf` at the merge, keeping a key only where upstream's file lacks it; deferred to the coordinator.

## The guest cycle

The window was granted on #669 at **09:12 UTC** (the coordinator's comment; one guest, 30 minutes). Image: `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, BUILD_ID `069fc270442134fe771258418adf4e666e0473fb` (`guest-cycle/s1`). **START 09:13:41** (posted on #669), **stopped 09:16:25** by `tools/vm-pair down` (`owned QEMU exited (pid 3339623)`). Leftover check: 0 on every line (`guest-cycle/leftover.txt`). Every output is in `guest-cycle/`.

| Step | What it read | The line | proved |
| --- | --- | --- | --- |
| s1 userconfig's first boot | `/usr/config/ssh`, `/usr/config/iwd`, `configure.log`, the journal | `ls: /usr/config/ssh: No such file or directory`; `configure.log lines: 0`; `Finished userconfig.service.`. #740's copy cannot run on this image | guest |
| s2 the units | `systemctl show -P User`, `is-enabled`, `is-active` for 25 installed | every `runs-as=root group=root`; `is-enabled` `disabled` for linked units; no `cron*.service` file | guest |
| s2b processes | uid from `/proc/<pid>/status` | `input_sense` and `video_sense` at uid 0; `powerstate` uid 0 | guest |
| s2c `.wants` | every link naming the 29 | 14 links; none for the five sensing units; `textmode.target.wants -> shell.service`; default `rocknix.target` | guest |
| s3 tty1 | `shell.service` | `active: inactive enabled: disabled`; no process on tty1 | guest |
| s4 busybox | the binary and the applets | `/usr/bin/busybox mode=4755 owner_uid=0`; su, login, passwd, httpd, nc, udhcpd each `applet=1` and linked | guest |
| s5 autostart | five plants in `/storage/.config/autostart/`, one reboot | marker `10-marker uid=0`, `40 uid=0 args=[]`, `40 uid=0 args=[split]`; journal `line 76: .../20-noexec: Permission denied`, `.../30-dir: Is a directory`; order: platform quirks, device quirks (`QEMU Standard PC (Q35 + ICH9, 2009)`), `common/*`, then the custom hooks | guest |
| s6 cron, udevil | cron files; `udevil.conf`, the unit, the rule | no cron unit, no crontab directory; `default_options_btrfs = compress=zstd:3`; `/usr/lib/samba/samba-autoshare: No such file or directory`; the rule acts on USB-storage `sd*` and `sr*` | guest |

## The second window

The coordinator granted it on #669 at **10:13 UTC** (one guest, 15 minutes from START, four cases). The image is the same, BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`. **START 10:14:56** (posted on #669). **Stopped 10:23:46** by `tools/vm-pair down` (`owned QEMU exited (pid 992351)`). The leftover check reads 0 on every line. Every output is in `guest-cycle-2/`.

| Case | What ran | The lines | Verdict | proved |
| --- | --- | --- | --- | --- |
| 1, PL-01 | A btrfs image made on the host (the guest has no `mkfs.btrfs` and no `truncate`) and a vfat image made on the guest, each on a loop device. Each was mounted through the medium's own unit, `systemctl start udevil-mount@<dev>.service`, then btrfs again by `udevil --mount` | btrfs: `udevil: denied 90: option 'compress=zstd:3' is not an allowed option`, not mounted, **the unit `active`**. vfat: `/var/media/loop2-... vfat rw,nosuid,nodev,noexec,noatime,fmask=0133,dmask=0022,...` | **udevil refuses every btrfs medium** (G-44): F-04's missing `nosuid,noexec,nodev` never applies. A btrfs medium cannot be mounted. The unit reading `active` after the refusal is G-30, shown | guest |
| 2, PL-04 | `debug-shell.service`'s state | `is-active: active`; `TTYPath=/dev/tty9`; `sysinit.target.wants/debug-shell.service -> ../debug-shell.service`; `pid=223 uid=0 comm=sh` on tty9; no `systemd.debug_shell` on the command line | **G-13 is proven:** an unauthenticated root shell on tty9 on every boot | guest |
| 3, PL-05 | the `evtest` readers by device; then the installed `get_devices` run alone, under the script's options | one reader each for `event0`, `event1` and `event2` (the three key devices); `entries=3 after 5s` (six passes) | **Not reproduced on the image.** The image's `input_sense` differs from the read tree's (`c3c-input_sense.diff`): it empties the list and the found-flags on each attempt, inside the loop. That is the M7 line's `6101242e14` (*m7: integrate reviewed frontend and installer repairs*, 2026-10-18), not in `8ebaf8daad` or upstream. G-23 stands at the read tree and is fixed on the M7 line | guest |
| 4, PL-03 | A `.tar` staged in `/storage/.update` with a 1 KB `KERNEL` and `SYSTEM` and wrong md5 files, named so the branding test passes. One reboot, then a read over serial (SSH's key is on `/storage`) | `/proc/mounts`: `/flash` only, **no `/storage`**; `/storage` empty; `systemctl is-system-running`: `degraded`; `storage-log.service: Failed`, with iwd, Avahi defaults and six `tmp-*.mount` failed; `sshd` inactive. The next boot (`systemctl reboot` over serial): `/dev/vda2 /storage ext4 rw,noatime`, `.update: []`, `running` | **G-04 is proven:** a rejected update boots once without `/storage`, every service that needs it failing, and deletes the staged update. The next boot is whole | guest |

**What the window changes:**
- **PL-01** is decided: udevil refuses the mount, so it is recorded as a Low on #585 (a filesystem the configuration cannot mount), with G-30's unit state.
- **PL-04's** state is recorded until the next base merge.
- **PL-03** is proven, and its `Already written:` line is now shown rather than argued.
- **PL-05** turns out to be fixed on the M7 line (`6101242e14`).
- **PL-02** was not exercised, and the M7 line changes nothing in `scripts/init` (`git show --stat 6101242e14`: `input_sense` only).

## Proofs

The leads stage B carries to the analysis (`04`). Each has the line that shows it, its state at `651150fc88` and its `proved:` cell. The bug decisions are stage D's, after the seats.

| # | Lead | The line(s) | At `651150fc88` | proved |
| --- | --- | --- | --- | --- |
| L-01 | The custom autostart loop runs `/storage/.config/autostart/*` as root with no `-f` test and `${script}` unquoted: a non-executable file or a directory errors into the journal, and a name with a space runs a different file with an argument. The `common` loop (`:50-53`) has the same shape over the image's own files; the platform, device and `HW_DEVICE` loops test `-f` and quote | `autostart:71-77` (`:76`); guest s5 | stands | guest |
| L-02 | `/etc/profile` sources `/storage/.config/profile.d/*` into every root service that loads it (`rocknix-autostart`, `powerstate`, `network-base-setup`, the five sensing scripts); guarded by `-f`, `. ${CONFIG}` unquoted | `busybox/config/profile:13-23` | stands | tree |
| L-03 | `shell.service`: an unauthenticated root shell on tty1, only when booted with `textmode` on the kernel command line; no register row (`tools/archaeology shell.service tty1`: nothing in the register, blindspots, logs or rules) | `shell.service`; `scripts/init:1215-1216`; guest s3 | same | guest |
| L-04 | busybox is setuid root with `su`, `login`, `passwd` and `httpd`+CGI enabled and linked, and nothing in the tree calls them | `busybox/package.mk:177,209`; `busybox-target.conf:30,549,554,556,888,894`; `22`; guest s4 | the flags are unchanged; the pin moves to 1.38.0 | guest |
| L-05 | `udevil.conf` mounts an inserted btrfs medium with `compress=zstd:3` only: no `nosuid`, `noexec` or `nodev`, while every other type has all three. The effective mount is **not proven** (a write the window did not cover) | `udevil.conf:233`; guest s6 | stands | tree |
| L-06 | `udevil-mount@.service`'s `ExecStartPost=-/usr/lib/samba/samba-autoshare` names a file no shipped image has (SAMBA_SUPPORT=no); the `-` hides it (blindspot 16) | the unit; `distributions/ROCKNIX/options:81`; guest s6 | same | guest |
| L-07 | #740: `userconfig-setup:30-34` and `post-update:54-57` copy `authorized_keys` to `/storage/.ssh`, making it a file when no directory exists; reachable only on a build with `LOCAL_SSH_KEYS_FILE` (`rocknix/package.mk:36-40`), which nothing in the tree sets | as named; guest s1 | stands | guest |
| L-08 | cron (`cron.service`, `cron-defaults`, crond) is on no shipped image: the brief's crontab lead has nothing to run | `distributions/ROCKNIX/options:177`; `busybox/package.mk:193-201`; guest s6 | same | guest |
| L-09 | `video.service` on a build without `video_sense`: does not arise; the two `DEVICE_HAS_HDMI=true` devices both install it | `098-deviceutils:23-29`; the RG552 and QEMU `001-device_config` | same | tree |
| L-10 | Markers under `/storage` switch root behaviour at boot: `.please_resize_me` (a partition resize), `.cache/volatile-log` (the journal's persistence), `.cache/debug.rocknix` (debug configs) | `scripts/init:1363-1364`; `var-log.mount`; `debugconfig.service` | same | tree |
| L-11 | `usercache-setup` writes `/storage/.cache/shadow` when the current one lacks a root entry | `usercache-setup:18` | not read at stage B | tree |
| L-12 | busybox fetched over plain http | `busybox/package.mk:11` | **settled by the next base merge** (https) | history |
| L-13 | Upstream's crash logging and sysctl moves collide with the fork's keeper and sysctls (C-1, C-2) | as above | the collisions | history |
| L-14 | The brief's unit loop masks `User=` with its credential `sed` and hides its own count | the brief § 5; `10` | -- | tool-run |
| L-15 | `systemctl is-enabled` reads `disabled` for every vendor-linked unit, so it cannot answer "enabled on which build" on these images | guest s2 / s2c | -- | guest |

## Coverage

*Generated.* One row per path (422), with what was read.

| Path | Lines | Tier | Language | Read | proved |
| --- | ---: | --- | --- | --- | --- |
| `hardware/quirks/autostart/002-device-switch` | 5 | upstream-carried | shell | counted | tree |
| `hardware/quirks/autostart/020-configs` | 25 | upstream-carried | shell | counted | tree |
| `hardware/quirks/autostart/020-rumble` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/autostart/020-set_audio_latency` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/autostart/080-dual_screen_mode` | 15 | upstream-carried | shell | counted | tree |
| `hardware/quirks/autostart/095-turbo-mode` | 16 | upstream-carried | shell | counted | tree |
| `hardware/quirks/autostart/999-export` | 5 | upstream-carried | shell | counted | tree |
| `hardware/quirks/package.mk` | 29 | upstream-carried | recipe | counted | tree |
| `hardware/quirks/platforms/AMD64/001-device_config` | 43 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/005-thermal_path` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/006-gpu-freq-path` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/010-default_tdp` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/010-dpms` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/010-led_control` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/020-fan_control` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/030-suspend_mode` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/050-audio_path` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/050-modifiers` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/090-ui_service` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/post/001-dpms` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/post/002-ledcontrol` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/post/003-wifi` | 55 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/post/004-log` | 26 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/pre/001-dpms` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/AMD64/sleep.d/pre/002-ledcontrol` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/GENERIC_X64/090-ui_service` | 8 | fork-own | shell | counted | tree |
| `hardware/quirks/platforms/GENERIC_X64/091-ui_shader` | 8 | fork-own | shell | counted | tree |
| `hardware/quirks/platforms/GENERIC_X64/092-retroarch-surface` | 113 | fork-own | shell | counted | tree |
| `hardware/quirks/platforms/GENERIC_X64/095-cloud-ssh` | 76 | fork-own | shell | counted | tree |
| `hardware/quirks/platforms/GENERIC_X64/097-retired-rescue-masks` | 40 | fork-own | shell | counted | tree |
| `hardware/quirks/platforms/H700/001-device_config` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/002-turbo-mode_config` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/006-panfrost` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/010-governors` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/010-led_control` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/020-fan_control` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/020-set_audio_latency` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/030-analog_leds` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/030-suspend_mode` | 24 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/040-wifi_probe_retry` | 28 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/050-modifiers` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/090-ui_service` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/400-set_gpu_overclock` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/bin/analog_sticks_ledcontrol` | 73 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/bin/gpu_overclock` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/bin/ledcontrol` | 68 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/sleep.d/post/003-codec` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/sleep.d/post/004-led` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/sleep.d/post/005-usbgadget` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/sleep.d/pre/003-codec` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/H700/sleep.d/pre/004-led` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/002-turbo-mode_config` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/010-governors` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/015-rk817_config` | 14 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/050-audio_path` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/050-modifiers` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/060-game_settings` | 6 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/075-mangohud-supported` | 25 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/090-ui_service` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/bin/battery_led_status` | 70 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/sleep.d/post/002-freq` | 23 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3326/sleep.d/pre/002-freq` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3399/002-turbo-mode_config` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3399/005-thermal_path` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3399/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3399/050-modifiers` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3399/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3399/090-ui_service` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3399/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3399/bin/battery_led_status` | 70 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/001-device_config` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/002-turbo-mode_config` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/010-governors` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/010-led_control` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/015-rk817_config` | 14 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/030-suspend_mode` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/050-audio_path` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/050-modifiers` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/055-thermal-trips` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/060-game_settings` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/090-ui_service` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/bin/ledcontrol` | 96 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/bin/volumealign` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3566/modules.keep` | 1 | upstream-carried | other | read | tree |
| `hardware/quirks/platforms/RK3576/001-device_config` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/002-turbo-mode_config` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/010-governors` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/010-led_control` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/020-suspend_mode` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/050-audio_path` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/050-modifiers` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/055-thermal-trips` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/090-ui_service` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3576/sleep.d/pre/99-idle-only` | 5 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/001-device_config` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/009-commander-cfg` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/010-governors` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/010-led_control` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/041-panfrost` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/050-audio_path` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/050-modifiers` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/090-ui_service` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/RK3588/bin/ledcontrol` | 70 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/001-device_config` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/010-governors` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/030-suspend_mode` | 14 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/041-panfrost` | 5 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/050-modifiers` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/075-mangohud-supported` | 25 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/090-ui_service` | 14 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/S922X/bin/battery_led_status` | 53 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/001-device_config` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/004-usb-autosuspend` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/005-thermal_path` | 16 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/007-usb-input-current` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/010-governors` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/015-turnip-debug` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/020-fan_control` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/070-modifiers` | 7 | upstream-carried | none | listed (no text) | tree |
| `hardware/quirks/platforms/SM4450/075-mangohud-supported` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/090-ui_service` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/bin/fancontrol` | 96 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM4450/bin/usb-input-current` | 24 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/001-device_config` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/002-audio_path` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/004-usb-autosuspend` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/005-thermal_path` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/009-commander-cfg` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/009-serial-number-path` | 15 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/010-governors` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/015-turnip-debug` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/020-set_audio_latency` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/030-led-control` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/030-suspend_mode` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/031-analog_leds` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/045-irq-affinity` | 25 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/060-game_settings` | 25 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/070-modifiers` | 7 | upstream-carried | none | listed (no text) | tree |
| `hardware/quirks/platforms/SM6115/075-mangohud-supported` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/090-ui_service` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/400-set_gpu_max_clock` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/500-enable-led` | 16 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/bin/achievements` | 5 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/bin/analog_sticks_ledcontrol` | 45 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/bin/battery_led_status` | 129 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/bin/gpu_max_clock` | 51 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/bin/ledcontrol` | 156 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/sleep.d/post/001-led` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/sleep.d/post/002-freq` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/sleep.d/pre/001-led` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM6115/sleep.d/pre/002-freq` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/001-device_config` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/002-audio_path` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/005-thermal_path` | 25 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/009-commander-cfg` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/009-serial-number-path` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/010-governors` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/020-fan_control` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/020-set_audio_latency` | 11 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/030-led-control` | 9 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/031-analog_leds` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/061-yabasanshiro_config` | 26 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/070-modifiers` | 7 | upstream-carried | none | listed (no text) | tree |
| `hardware/quirks/platforms/SM8250/075-mangohud-supported` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/090-ui_service` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/400-set_gpu_overclock` | 16 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/500-enable-led` | 16 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/bin/achievements` | 5 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/bin/analog_sticks_ledcontrol` | 45 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/bin/battery_led_status` | 129 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/bin/fancontrol` | 196 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/bin/gpu_overclock` | 51 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/bin/ledcontrol` | 153 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/post/001-led` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/post/002-freq` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/post/003-audio` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/pre/001-led` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8250/sleep.d/pre/002-freq` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/001-device_config` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/002-audio_path` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/005-thermal_path` | 16 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/009-serial-number-path` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/010-governors` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/020-fan_control` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/030-analog_leds` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/030-led-control` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/030-suspend_mode` | 14 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/070-modifiers` | 7 | upstream-carried | none | listed (no text) | tree |
| `hardware/quirks/platforms/SM8550/075-mangohud-supported` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/090-ui_service` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/095-force_zink` | 1 | upstream-carried | symlink | listed (no text) | tree |
| `hardware/quirks/platforms/SM8550/096-cpuidle` | 6 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/500-enable-led` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/bin/fancontrol` | 96 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/bin/gpu_overclock` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/sleep.d/post/001-led` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/sleep.d/post/002-freq` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/sleep.d/pre/001-led` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8550/sleep.d/pre/002-freq` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/001-device_config` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/002-audio_path` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/005-thermal_path` | 16 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/010-governors` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/020-fan_control` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/030-analog_leds` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/030-led-control` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/030-suspend_mode` | 14 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/050-retroarch-configs` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/061-yabasanshiro_config` | 26 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/070-modifiers` | 7 | upstream-carried | none | listed (no text) | tree |
| `hardware/quirks/platforms/SM8650/075-mangohud-supported` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/090-ui_service` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/095-force_zink` | 1 | upstream-carried | symlink | listed (no text) | tree |
| `hardware/quirks/platforms/SM8650/500-enable-led` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/bin/fancontrol` | 96 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/bin/gpu_overclock` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/sleep.d/post/001-led` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/sleep.d/post/002-freq` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/sleep.d/pre/001-led` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8650/sleep.d/pre/002-freq` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/001-device_config` | 10 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/002-audio_path` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/002-turbo-mode_config` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/005-thermal_path` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/010-governors` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/020-fan_control` | 24 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/030-analog_leds` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/030-led-control` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/030-suspend_mode` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/040-affinity` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/050-retroarch-configs` | 7 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/060-game_settings` | 43 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/061-yabasanshiro_config` | 26 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/065-Touchscreen-events` | 12 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/070-modifiers` | 7 | upstream-carried | none | listed (no text) | tree |
| `hardware/quirks/platforms/SM8750/075-mangohud-supported` | 13 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/090-ui_service` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/091-ui_shader` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/095-force_zink` | 8 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/500-enable-led` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/bin/fancontrol` | 97 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/bin/gpu_overclock` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/sleep.d/post/001-led` | 17 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/sleep.d/post/002-freq` | 22 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/sleep.d/pre/001-led` | 19 | upstream-carried | shell | counted | tree |
| `hardware/quirks/platforms/SM8750/sleep.d/pre/002-freq` | 18 | upstream-carried | shell | counted | tree |
| `hardware/quirks/profile.d/999-export` | 73 | fork-own | shell | counted | tree |
| `hardware/quirks/system.d/led-poweroff.service` | 12 | upstream-carried | systemd | counted | tree |
| `hardware/quirks/system.d/volume-fixup.service` | 12 | upstream-carried | systemd | counted | tree |
| `sysutils/autostart/package.mk` | 29 | upstream-carried | recipe | counted | tree |
| `sysutils/autostart/profile.d/002-autostart` | 12 | upstream-carried | shell | counted | tree |
| `sysutils/autostart/sources/autostart` | 97 | upstream-carried | shell | counted | tree |
| `sysutils/autostart/sources/daemons/005-fstrim` | 3 | upstream-carried | none | listed (no text) | tree |
| `sysutils/autostart/system.d/rocknix-autostart.service` | 13 | upstream-carried | systemd | counted | tree |
| `sysutils/avfs/package.mk` | 22 | upstream-carried | recipe | counted | tree |
| `sysutils/bash/package.mk` | 32 | upstream-carried | recipe | counted | tree |
| `sysutils/btop/package.mk` | 22 | upstream-carried | recipe | counted | tree |
| `sysutils/btrfs-progs/package.mk` | 12 | upstream-carried | recipe | counted | tree |
| `sysutils/busybox/config/busybox-host.conf` | 1200 | upstream-carried | config | read, not counted | tree |
| `sysutils/busybox/config/busybox-init.conf` | 1224 | upstream-carried | config | read, not counted | tree |
| `sysutils/busybox/config/busybox-target.conf` | 1224 | upstream-carried | config | read, not counted | tree |
| `sysutils/busybox/config/httpd.conf` | 46 | upstream-carried | config | read, not counted | tree |
| `sysutils/busybox/config/inputrc` | 66 | upstream-carried | none | listed (no text) | tree |
| `sysutils/busybox/config/profile` | 23 | upstream-carried | none | listed (no text) | tree |
| `sysutils/busybox/config/suspend-modules.conf` | 1 | upstream-carried | config | read, not counted | tree |
| `sysutils/busybox/default.d/crond.conf` | 0 | upstream-carried | config | read, not counted | tree |
| `sysutils/busybox/package.mk` | 242 | upstream-carried | recipe | counted | tree |
| `sysutils/busybox/profile.d/098-busybox` | 32 | upstream-carried | none | listed (no text) | tree |
| `sysutils/busybox/scripts/dthelper` | 93 | upstream-carried | shell | counted | tree |
| `sysutils/busybox/scripts/fs-resize` | 74 | upstream-carried | shell | counted | tree |
| `sysutils/busybox/scripts/functions` | 156 | upstream-carried | none | listed (no text) | tree |
| `sysutils/busybox/scripts/getedid` | 256 | upstream-carried | shell | counted | tree |
| `sysutils/busybox/scripts/init` | 1383 | fork-own | shell | counted | tree |
| `sysutils/busybox/scripts/kernel-overlays-setup` | 85 | upstream-carried | shell | counted | tree |
| `sysutils/busybox/scripts/lsb_release` | 7 | upstream-carried | shell | counted | tree |
| `sysutils/busybox/scripts/pastebinit` | 8 | upstream-carried | shell | counted | tree |
| `sysutils/busybox/sleep.d.serial/99-suspend-modules.sh` | 93 | upstream-carried | shell | counted | tree |
| `sysutils/busybox/sources/console-tools/evtest.c` | 94 | upstream-carried | c | counted | tree |
| `sysutils/busybox/sysctl.d/99-coredump.conf` | 4 | fork-own | config | read, not counted | tree |
| `sysutils/busybox/sysctl.d/cdrom.conf` | 2 | upstream-carried | config | read, not counted | tree |
| `sysutils/busybox/sysctl.d/hang-policy.conf` | 17 | fork-own | config | read, not counted | tree |
| `sysutils/busybox/sysctl.d/memory.conf` | 1 | upstream-carried | config | read, not counted | tree |
| `sysutils/busybox/system.d.opt/cron-defaults.service` | 11 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/system.d.opt/cron.service` | 16 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/system.d/fs-resize.service` | 10 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/system.d/fs-resize.target` | 5 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/system.d/proc-sys-fs-binfmt_misc.mount` | 24 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/system.d/shell.service` | 23 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/system.d/show-version.service` | 13 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/system.d/storage-log.service` | 12 | fork-own | systemd | counted | tree |
| `sysutils/busybox/system.d/textmode.target` | 6 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/system.d/var-log.mount` | 23 | fork-own | systemd | counted | tree |
| `sysutils/busybox/system.d/var.mount` | 21 | upstream-carried | systemd | counted | tree |
| `sysutils/busybox/tmpfiles.d/z_01_busybox.conf` | 12 | upstream-carried | config | read, not counted | tree |
| `sysutils/drm_tool/package.mk` | 21 | upstream-carried | recipe | counted | tree |
| `sysutils/file/package.mk` | 17 | upstream-carried | recipe | counted | tree |
| `sysutils/fuse2/package.mk` | 51 | upstream-carried | recipe | counted | tree |
| `sysutils/gptfdisk/package.mk` | 20 | upstream-carried | recipe | counted | tree |
| `sysutils/grep/package.mk` | 15 | upstream-carried | recipe | counted | tree |
| `sysutils/i2c-tools/package.mk` | 43 | upstream-carried | recipe | counted | tree |
| `sysutils/kmod/modprobe.d/aliases.conf` | 172 | upstream-carried | config | read, not counted | tree |
| `sysutils/kmod/modprobe.d/i2c.conf` | 1 | upstream-carried | config | read, not counted | tree |
| `sysutils/kmod/package.mk` | 54 | upstream-carried | recipe | counted | tree |
| `sysutils/libevdev/package.mk` | 6 | upstream-carried | recipe | counted | tree |
| `sysutils/libiio/package.mk` | 27 | upstream-carried | recipe | counted | tree |
| `sysutils/lsof/package.mk` | 20 | upstream-carried | recipe | counted | tree |
| `sysutils/nvtop/package.mk` | 33 | fork-own | recipe | counted | tree |
| `sysutils/powerstate/package.mk` | 21 | upstream-carried | recipe | counted | tree |
| `sysutils/powerstate/sources/powerstate.sh` | 80 | fork-own | shell | counted | tree |
| `sysutils/powerstate/system.d/powerstate.service` | 21 | fork-own | systemd | counted | tree |
| `sysutils/sleep/package.mk` | 21 | upstream-carried | recipe | counted | tree |
| `sysutils/sleep/sources/modules.bad` | 4 | upstream-carried | other | read | tree |
| `sysutils/sleep/sources/sleep.conf` | 25 | upstream-carried | config | read, not counted | tree |
| `sysutils/sleep/sources/sleep.sh` | 140 | upstream-carried | shell | counted | tree |
| `sysutils/squashfs-tools/package.mk` | 43 | upstream-carried | recipe | counted | tree |
| `sysutils/squashfuse/package.mk` | 12 | upstream-carried | recipe | counted | tree |
| `sysutils/system-utils/package.mk` | 42 | upstream-carried | recipe | counted | tree |
| `sysutils/system-utils/sources/autostart/AMD64/002-overclock` | 19 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/autostart/common/098-deviceutils` | 40 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/config/fancontrol.conf` | 34 | upstream-carried | config | read, not counted | tree |
| `sysutils/system-utils/sources/devices/AMD64/overclock` | 47 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/devices/AMD64/set_epp` | 52 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/devices/GENERIC_X64/video_sense` | 20 | fork-own | shell | counted | tree |
| `sysutils/system-utils/sources/devices/RK3399/headphone_sense` | 46 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/devices/RK3399/internalwifi` | 23 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/devices/RK3399/video_sense` | 38 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/devices/RK3566/headphone_sense` | 53 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/devices/S922X/headphone_sense` | 39 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/analog_sticks_ledcontrol` | 18 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/battery_led_status` | 18 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/fancontrol` | 18 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/hdmi_sense` | 58 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/headphone_sense` | 53 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/input_sense` | 539 | fork-own | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/ledcontrol` | 18 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/output_monitor` | 109 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/sources/scripts/turbomode` | 15 | upstream-carried | shell | counted | tree |
| `sysutils/system-utils/system.d/batteryledstatus.service` | 12 | upstream-carried | systemd | counted | tree |
| `sysutils/system-utils/system.d/fancontrol.service` | 11 | upstream-carried | systemd | counted | tree |
| `sysutils/system-utils/system.d/headphones.service` | 12 | upstream-carried | systemd | counted | tree |
| `sysutils/system-utils/system.d/input.service` | 14 | upstream-carried | systemd | counted | tree |
| `sysutils/system-utils/system.d/video.service` | 11 | upstream-carried | systemd | counted | tree |
| `sysutils/system-utils/udev.d/99-hdmi.rules` | 1 | upstream-carried | udev | counted | tree |
| `sysutils/system-utils/udev.d/99-input.rules` | 7 | upstream-carried | udev | counted | tree |
| `sysutils/systemd/config/hosts.conf` | 12 | upstream-carried | config | read, not counted | tree |
| `sysutils/systemd/config/hwdb.d/99-osmcrf.hwdb` | 17 | upstream-carried | other | read | tree |
| `sysutils/systemd/config/hwdb.d/README` | 10 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/logind.conf.d/README` | 233 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/modules-load.d/README` | 33 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/resolved.conf.d/README` | 1 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/sleep.conf.d/README` | 59 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/sysctl.d/99-rocknix-networking.conf` | 9 | upstream-carried | config | read, not counted | tree |
| `sysutils/systemd/config/sysctl.d/README` | 35 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/sysctl.d/rocknix.conf` | 3 | fork-own | config | read, not counted | tree |
| `sysutils/systemd/config/system.conf.d/10-shutdown-timeout.conf` | 7 | upstream-carried | config | read, not counted | tree |
| `sysutils/systemd/config/system.conf.d/20-watchdog.conf` | 13 | fork-own | config | read, not counted | tree |
| `sysutils/systemd/config/system.d/README` | 232 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/timesyncd.conf.d/README` | 86 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/tmpfiles.d/README` | 109 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/config/udev.rules.d/README` | 25 | upstream-carried | none | listed (no text) | tree |
| `sysutils/systemd/hwdb.d/10-adc-keys.hwdb` | 6 | upstream-carried | other | read | tree |
| `sysutils/systemd/hwdb.d/20-joypad.hwdb` | 23 | upstream-carried | other | read | tree |
| `sysutils/systemd/hwdb.d/61-thor-ft5x06.hwdb` | 7 | upstream-carried | other | read | tree |
| `sysutils/systemd/hwdb.d/70-local-keyboard.hwdb` | 14 | upstream-carried | other | read | tree |
| `sysutils/systemd/package.mk` | 333 | fork-own | recipe | counted | tree |
| `sysutils/systemd/profile.d/090-systemd.conf` | 4 | upstream-carried | config | read, not counted | tree |
| `sysutils/systemd/scripts/network-base-setup` | 129 | fork-own | shell | counted | tree |
| `sysutils/systemd/scripts/systemd-machine-id-setup` | 69 | upstream-carried | shell | counted | tree |
| `sysutils/systemd/scripts/systemd-timesyncd-setup` | 22 | upstream-carried | shell | counted | tree |
| `sysutils/systemd/scripts/usercache-setup` | 27 | upstream-carried | shell | counted | tree |
| `sysutils/systemd/scripts/userconfig-setup` | 90 | fork-own | shell | counted | tree |
| `sysutils/systemd/system.d/debugconfig.service` | 14 | upstream-carried | systemd | counted | tree |
| `sysutils/systemd/system.d/flash.mount.d/dependencies.conf` | 2 | upstream-carried | config | read, not counted | tree |
| `sysutils/systemd/system.d/machine-id.service` | 13 | upstream-carried | systemd | counted | tree |
| `sysutils/systemd/system.d/network-base.service` | 21 | fork-own | systemd | counted | tree |
| `sysutils/systemd/system.d/storage.mount.d/dependencies.conf` | 2 | upstream-carried | config | read, not counted | tree |
| `sysutils/systemd/system.d/systemd-pstore.service.d/rocknix.conf` | 8 | fork-own | config | read, not counted | tree |
| `sysutils/systemd/system.d/systemd-resolved.service.d/override.conf` | 6 | upstream-carried | config | read, not counted | tree |
| `sysutils/systemd/system.d/systemd-timesyncd-setup.service` | 12 | upstream-carried | systemd | counted | tree |
| `sysutils/systemd/system.d/usercache.service` | 13 | upstream-carried | systemd | counted | tree |
| `sysutils/systemd/system.d/userconfig.service` | 14 | upstream-carried | systemd | counted | tree |
| `sysutils/systemd/tmpfiles.d/connectivity.conf` | 3 | upstream-carried | config | read, not counted | tree |
| `sysutils/systemd/tmpfiles.d/z_01_rocknix.conf` | 12 | fork-own | config | read, not counted | tree |
| `sysutils/systemd/udev.d/60-not-joysticks.rules` | 2 | upstream-carried | udev | counted | tree |
| `sysutils/systemd/udev.d/80-clock.rules` | 2 | upstream-carried | udev | counted | tree |
| `sysutils/udevil/config/udevil.conf` | 331 | upstream-carried | config | read, not counted | tree |
| `sysutils/udevil/package.mk` | 4 | upstream-carried | recipe | counted | tree |
| `sysutils/udevil/system.d/udevil-mount@.service` | 11 | upstream-carried | systemd | counted | tree |
| `sysutils/udevil/udev.d/95-udevil-mount.rules` | 32 | upstream-carried | udev | counted | tree |
| `sysutils/umtprd/etc/umtprd.conf` | 100 | upstream-carried | config | read, not counted | tree |
| `sysutils/umtprd/package.mk` | 19 | upstream-carried | recipe | counted | tree |
| `sysutils/usb-modeswitch/package.mk` | 5 | upstream-carried | recipe | counted | tree |
| `sysutils/util-linux/config/swap.conf` | 12 | upstream-carried | config | read, not counted | tree |
| `sysutils/util-linux/package.mk` | 103 | upstream-carried | recipe | counted | tree |
| `sysutils/util-linux/system.d/fstrim.service` | 7 | upstream-carried | systemd | counted | tree |
| `sysutils/util-linux/system.d/fstrim.timer` | 10 | upstream-carried | systemd | counted | tree |
