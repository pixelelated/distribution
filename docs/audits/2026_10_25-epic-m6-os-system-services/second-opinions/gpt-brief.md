# Second opinion on a code audit -- M6.P2 T22, the OS's system services and platform quirks, epic tier

You are the second reader of a finished code audit. You cannot run
commands or open the repository; everything you may cite is in the packet
below, and every claim you make names the packet's `file:line` or the
command output it rests on. The first reader's verdicts are in the packet;
do not take them as given.

The scope: 422 paths under `projects/ROCKNIX/packages/sysutils/` and
`hardware/` (the per-device quirk directories excepted) of a handheld Linux
distribution -- busybox's configuration and its initramfs `/init`, the
systemd units, the boot-time autostart runner, the per-platform quirks, and
the small system packages -- read at one commit, with boot behaviour proven
on a QEMU guest of the distribution's x86_64 test image. Every unit runs as
root; the device has one user, who owns `/storage` and can reach a root
shell. The image's `/bin/sh` is bash; busybox provides the small utilities.
The first reader is Claude Opus 5.5 (Anthropic); you are a reviewer from
another lab. The lens is security first, then brittleness. The audit is a
renovation: besides defects, its findings answer seven questions (Q1
modernize, Q2 standards, Q3 bugs, Q4 package currency, Q5 efficiency, Q6
dead ends, Q7 clarity). The packet also compares the read tree with
upstream's newer tree (`651150fc88`): a finding upstream has already fixed
is *settled by the next base merge*, not a bug.

Answer in three parts, in this order:

1. **Your own findings first.** Read the packet's evidence -- the units,
   the scripts, the configuration excerpts, the guest's lines -- and list
   every defect, gap, or unsafe seam you find that is not already one of the
   first reader's findings. One line each: an id (G-01, G-02, ...), a
   severity (Critical / High / Medium / Low), the packet's `file:line`, what
   fails and when, and who can trigger it (a remote party, a medium the
   player inserts, the player's own files, nobody).
2. **Refute the first reader.** The Risk Assessment in 04 lists 16 findings,
   F-01 to F-16, all graded Low (eight as designs). For each: agree,
   disagree, re-grade, or narrow -- and say what would make the finding
   false and whether the packet shows it. Say plainly whether anything
   graded Low should be Medium or High under the threat model above, and
   whether any "design" is a defect the first reader excused.
3. **What you could not judge.** The claims the packet does not let you
   verify, so the orchestrator knows where its evidence was thin.

Everyday words, no hedging: a finding either survives your reading or it
does not, and you say which.

---


## The first reader's 02-forward-audit.md (whole)

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


## The first reader's 03-retrospective.md (whole)

# Retrospective — M6.P2 T22, the OS's system services and platform quirks

**Auditor:** Code Auditor skill, primary Claude Opus 5.5 (Anthropic) at high effort
**Date:** 2026-10-25
**Subject:** #669: the 422 paths of `projects/ROCKNIX/packages/sysutils/**` and `hardware/**` (`quirks/devices/**` excepted), read at `8ebaf8daad`
**Evidence:** `02-forward-audit.md` (the runs, the reachability table, the units, busybox, the upstream delta, the guest cycle, the proofs L-01 to L-15)

---

## Running Notes

Phase 3 reads what the area was for, what drifted, what nobody noticed, and
the seams. Every claim cites `02` or a `file:line` at `8ebaf8daad`.

### 3.1 Architectural coherence

The area is the OS's boot spine: `scripts/init` (PID 1 in the initramfs,
1,383 fork-own lines) selects a boot target from markers and the kernel
command line. systemd brings up 29 units from this slice. `rocknix-autostart`
then runs four layers of scripts in a fixed order: platform quirks, device
quirks, `common/*`, and the player's own hooks (`02` § The guest cycle, s5).
The design is coherent, and every layer runs as root: no unit names a user
(`02` § The units).

**Two selection mechanisms, and neither is written down where a reader
lands.** `system-utils` selects at install time (`package.mk:27-34`). The
quirks select at run time: every platform is copied into every image that
has a platform of its own (`quirks/package.mk:16-18`), and `HW_DEVICE` picks
one at boot (`autostart:16-28`). So 213 files, 108,294 bytes, ship on every
image and run on none (`02` § The reachability table). Neither `package.mk`
says so. A reader of the quirks recipe sees `cp -r platforms/*` after a test
on one platform's directory and could read it either way.

### 3.2 Project conformance

| Rule | Where it bites here | Verdict |
| --- | --- | --- |
| `engineering-practices.md` § Guards must fail closed | `autostart`'s `common` and custom loops have no `-f` and an unquoted `${script}` (L-01); its other three loops and `/etc/profile`'s have the `-f` (L-02) | PARTIAL: two loops of six unguarded |
| blindspot 16 (a unit naming a binary the image lacks) | `udevil-mount@.service`'s `samba-autoshare` (L-06); `video.service` cleared (L-09) | one instance, hidden by `-` |
| blindspot 34 (busybox is not the host's tools) | `/bin/sh` is bash; busybox supplies the applets | no new instance read |
| `upgrade-and-install.md` (what the units leave on devices) | `/storage/.ssh` as a file (#740 and `post-update:54-57`), `/storage/.cache/shadow` rewritten each boot (L-11) | read; reach named |
| `vm-first.md` | the units, tty1, the autostart order and `userconfig-setup` proven on one guest; H700 and SM8550 quirks read | PASS |

### 3.3 Spec fidelity

The brief's figures all reproduce (`01` § Scope). It has two errata, both
recorded: its unit loop's credential mask hides the `User=` count it is meant
to show (L-14), and `autostart:76` runs `${script}` rather than `exec`ing it.
The brief's leads land as follows:

- **`cron.service`**: no shipped image has it (L-08).
- **`video.service`** cannot meet a missing binary (L-09).
- **`shell.service`**: a `textmode`-only root shell, with no register row (L-03).
- **A writable path the brief did not name:** `/etc/profile:19-23` (L-02).

### 3.4 Platform architecture conformance

The units are the platform's: LibreELEC's shape (`/storage/.config/autostart`,
`/storage/.config/profile.d`, `/storage/.cache/services` markers), carried
by JELOS and ROCKNIX. The fork's own additions in this area are:
- `scripts/init`;
- `input_sense`;
- the GENERIC_X64 quirks (a developer's tool, D-QA-053);
- `var-log.mount` with `storage-log.service` (#104, the persistent journal);
- `hang-policy.conf`, `20-watchdog.conf` and the pstore drop-in;
- `network-base-setup`;
- `userconfig-setup`'s `es_savestates.cfg` link (#196).

Each sits inside the platform's shape, and none adds a root-reachable
writable path the platform did not already have.

### 3.5 Cross-system interaction audit

### Interaction: the player's hooks x every root service

`/storage/.config/autostart/*` runs once a boot, as root, after every other
layer (s5). `/storage/.config/profile.d/*` is sourced by `/etc/profile`. The
services that source it are `rocknix-autostart`, `powerstate` (as its
`EnvironmentFile` and again in `powerstate.sh:11`), `network-base-setup`,
`098-deviceutils` and the five sensing scripts, and the interactive shell.
A broken file there breaks all of them at once. Both directories are the
player's by design, so the seam is fragility, not exposure.

### Interaction: udev x udevil x samba

A USB-storage or optical medium triggers `udevil-mount@<dev>.service`
(`95-udevil-mount.rules`). It mounts under `udevil.conf`, with every type
`nosuid,noexec,nodev` except btrfs (L-05), and then calls a `samba-autoshare`
no shipped image has (L-06).

### Interaction: `userconfig-setup` and `post-update` x `/storage/.ssh`

Both copy a build's developer keys to the path `/storage/.ssh`. Where no
directory exists, the copy makes a file. This is reachable only on a build
with `LOCAL_SSH_KEYS_FILE` (L-07, #740).

### Interaction: this slice x the next base merge

Upstream changed 44 of the 422 in three and a half weeks. Only the busybox
pin's http URL is settled by the merge. The two collisions (C-1 crash
logging, C-2 the sysctls) need a decision before it (`02` § The upstream
delta).

### 3.6 What's missing?

- **A record of the boot layers' order and identity.** It is proven on the
  guest here and written nowhere a maintainer reads.
- **A test that a unit's `ExecStart*` names an installed binary.** The
  `samba-autoshare` line has been silent since the unit came in.
- **A note in `quirks/package.mk` that every platform ships everywhere.**

### 3.6.5 Audit-prescription verification: the shapes, every site

| Shape | Sites hunted | Found |
| --- | --- | --- |
| a loop running or sourcing each entry of a directory | `autostart:20-25,35-40,50-53,60-65,73-76`, `/etc/profile:6-10,19-23`, `sleep.sh:84-87` | the platform, device and `HW_DEVICE` loops test `-f` and quote; `sleep.sh` tests `-x` and quotes; **the `common` loop (`:50-53`, image files) and the custom loop (`:73-76`, the player's files) neither test nor quote**; `/etc/profile` tests `-f` and sources unquoted |
| a unit naming a path the image lacks | the 29 units' `Exec*` (`24`) against the guest | `samba-autoshare` |
| a marker under `/storage` changing root behaviour at boot | `scripts/init`, the units' `Condition*` | `.please_resize_me`, `.cache/volatile-log`, `.cache/debug.rocknix` (L-10) |
| a setuid binary or an applet enabled with no caller | busybox's configuration; `find -perm -4000` on the guest | busybox alone; four applets with no caller |

### 3.7 Retrospective Summary

The slice found no unauthenticated remote path. Every root-run, writable
input is one the platform hands the player deliberately: the hook
directories, the markers, an inserted medium. The defects are brittleness
and dead lines:
- the custom autostart loop's missing guard and quoting (L-01);
- `samba-autoshare` (L-06);
- the btrfs default that contradicts its own file's warning (L-05);
- four setuid-capable applets nothing calls (L-04).

All four are in upstream-carried files and stand at `651150fc88`, so the
class decision for each is the maintainer's on #346. The fork's own 24 files
read clean on this lens.


## The first reader's 04-analysis.md (whole)

# Audit Analysis — M6.P2 T22, the OS's system services and platform quirks

**Date:** 2026-10-25
**Spec:** `docs/reviews/briefs/os-system-services.md` v3 (`cc8b6cf2a3`); `docs/reviews/plan-for-the-plan.md` § 6b, § 6c
**Issues:** #669, #695, #339
**Commits:** read at `8ebaf8daad`; upstream `next` for the delta and Q4 `651150fc88` (merge base `c445081a59`); guest image `069fc270442134fe771258418adf4e666e0473fb`

---

## Executive Summary

T22 read the 422 paths of the OS's system services and platform quirks
(16,604 lines; 24 fork-own) at `8ebaf8daad` with the security lens first.
One GENERIC_X64 guest proved the boot behaviour (`02` § The guest cycle).

- **All 29 units run as root, and every root-run input a player can write is
  one the platform hands them on purpose:**
  - the hook directories `/storage/.config/autostart/` and `/storage/.config/profile.d/`;
  - three boot markers under `/storage`;
  - an inserted medium.
- **No unauthenticated remote path was found.** The tty1 root shell exists
  only on a `textmode` boot.
- **The defects are brittleness and dead lines, all in upstream-carried
  files that stand at `651150fc88`:**
  - the custom autostart loop runs entries without a `-f` test and with an
    unquoted name, so a hook with a space in its name runs a different file
    with an argument (F-01, shown on the guest);
  - udevil mounts a btrfs medium without the `nosuid,noexec,nodev` its own
    file says every type must carry (F-04);
  - `udevil-mount@.service` calls a `samba-autoshare` that no shipped image
    has (F-05);
  - busybox is setuid root with `su`, `login`, `passwd` and `httpd`+CGI
    enabled and nothing in the tree calling them (F-03).
- **Brief leads that landed differently:**
  - cron is on no shipped image (F-09);
  - `video.service` cannot meet a missing binary;
  - #740 is reachable only on a developer's build, with a second copy site
    in `post-update` (F-06).
- **The two selection mechanisms leave 213 platform files (108,294 bytes) on
  every image that never run there** (F-10), and neither recipe says so (F-14).
- **Upstream's next merge** settles the http busybox pin and brings two
  collisions (crash logging and the sysctls), which are deferred as designs
  (F-12, F-13).

## Acceptance-criteria scorecard

| ID | Criterion (#669) | Verdict | Notes |
| --- | --- | --- | --- |
| AC-01 | the folder holds `00` to `05` | PARTIAL ⚠ | `05` at stage D |
| AC-02 | the lint prints `PASS` | PARTIAL ⚠ | pre-issue at stage D; resolution at close |
| AC-03 | `review-plan.json`, two seats with provenance, the packet manifest | PARTIAL ⚠ | written before the first call; the seats at Phase 4.6 |
| AC-04 | the punch-list issue at Phase 7 outcomes | MISSING ✗ | stage D onward |
| AC-05 | `reviewed-at`, `fixed-at`; the 422 at `8ebaf8daad`; nothing under `packages/`, `projects/`, `tools/` | PASS ✓ | `git diff --stat 4a48d388c4 HEAD -- packages projects tools` empty (`02` § The runs, `18`); the header is written at hand-back |
| AC-06 | `01` § Scope with the block and the figures | PASS ✓ | `01` § Scope |
| AC-07 | the coverage table, 422 rows | PASS ✓ | `02` § Coverage, generated |
| AC-08 | the reachability table, 422 rows, 8 and 213 named | PASS ✓ | `02` § The reachability table; the generator asserts the figures |
| AC-09 | the units table, 29 rows, enablement, the named units' findings | PASS ✓ | `02` § The units; F-01 to F-09 below; `tools/archaeology shell.service tty1` quoted in `02` § Proofs L-03 |
| AC-10 | § busybox: the pin and each flagged applet's caller | PASS ✓ | `02` § busybox |
| AC-11 | § The upstream delta: 44 M with states, 20 D split, 42 A and 2 R, two collisions | PASS ✓ | `02` § The upstream delta |
| AC-12 | § The guest cycle | PASS ✓ | `02` § The guest cycle; `guest-cycle/` |
| AC-13 | § The runs: exit, wall, figure, *a FAIL would mean* | PASS ✓ | `02` § The runs |
| AC-14 | `00` shows what never ran, four seat calls, nothing written outside | PARTIAL ⚠ | so far, yes; the seats are pending |
| AC-15 | `04` § Q3, Q4, Q6, § Second opinion | PARTIAL ⚠ | Q1 to Q7 below; § Second opinion after the seats |
| AC-16 | `proved:` cells; `question:` per item; box-check per bug | PARTIAL ⚠ | `02` carries every cell; items and bugs at stage D |
| AC-17 | the retro posted | MISSING ✗ | stage G |
| AC-18 | the five checkers on the branch | MISSING ✗ | after the hand-back merge |

## Risk Assessment

Every finding, with its question, severity and evidence class. A finding on
an upstream-carried file names the file's state at `651150fc88`.

| Finding | Question | Severity | Defect or item | Evidence |
| --- | --- | --- | --- | --- |
| F-01 | Q3 | Low | `autostart`'s `common` and custom loops run each entry with no `-f` test and `${script}` unquoted: a non-executable file or a directory is an error in the journal, and a hook whose name has a space runs another hook with an argument (L-01). Stands at `651150fc88` | proven on the guest |
| F-02 | Q3 / Q2 | Low (design) | `/etc/profile:19-23` sources `/storage/.config/profile.d/*` into every root service that loads it; guarded by `-f`, `. ${CONFIG}` unquoted (L-02). Stands | trace / read |
| F-03 | Q3 / Q5 | Low | busybox is setuid root (`package.mk:177,209`; mode 4755 on the guest) with `su`, `login`, `passwd` and `httpd`+CGI enabled, linked and called by nothing in the tree (L-04). The flags stand at `651150fc88` | proven on the guest |
| F-04 | Q3 | Low | `udevil.conf:233` gives btrfs `compress=zstd:3` alone, against `:213`'s *FOR GOOD SECURITY ... SHOULD ALWAYS INCLUDE: nosuid,noexec,nodev* (L-05); upstream's (`c288a47e62`). Stands. The effective mount is not proven | trace / read |
| F-05 | Q3 / Q6 | Low | `udevil-mount@.service` runs `-/usr/lib/samba/samba-autoshare`, which no shipped image has (SAMBA_SUPPORT=no); the `-` hides the failure (L-06, blindspot 16) | proven on the guest |
| F-06 | Q3 | Low | #740's `cp ... /storage/.ssh` has a second site at `post-update:54-57`; both are reachable only on a build with `LOCAL_SSH_KEYS_FILE` (L-07). #740 is cited, not re-filed | trace / read |
| F-07 | Q3 | Low (design) | `shell.service`, an unauthenticated root shell on tty1, only on a `textmode` boot (L-03); no register row | proven on the guest |
| F-08 | Q3 | Low (design) | markers under `/storage` change root behaviour at boot: `.please_resize_me`, `.cache/volatile-log`, `.cache/debug.rocknix` (L-10) | trace / read |
| F-09 | Q6 | Low | cron's two units and `default.d/crond.conf` are on no shipped image (CRON_SUPPORT=no) (L-08) | proven on the guest |
| F-10 | Q6 / Q5 | Low | 213 platform files (108,294 bytes) ship on every image and run on none; 8 `system-utils` rows are installed by no shipped image | trace / read |
| F-11 | Q4 | Low | busybox 1.36.1 over http; systemd 255.8; util-linux 2.39.2: upstream has 1.38.0 over https, 261.2 and 2.42.4. The http pin is settled by the next base merge | trace / read |
| F-12 | Q1 | Low (design) | collision C-1: `8bce25b3b7` replaces core files with journal crash logging, against the fork's keeper (D-INFRA-011/012/013) | trace / read |
| F-13 | Q1 | Low (design) | collision C-2: `54acd9556f` moves the sysctls into the image (`60-rocknix.conf`) and deletes the fork-carried `sysctl.d/rocknix.conf` | trace / read |
| F-14 | Q7 | Low | neither `system-utils/package.mk` nor `quirks/package.mk` says which files each image carries or runs; the quirks recipe ships every platform with no comment | trace / read |
| F-15 | Q2 | Low (design) | no unit names a user (all 29 run as root) | proven on the guest |
| F-16 | Q2 | Low | `systemctl is-enabled` reads `disabled` for every vendor-linked unit, so no tool answers "enabled on which build" except the `.wants` links (L-15) | proven on the guest |

## Coverage Boundary

**Examined:** all 422 paths at `8ebaf8daad`; every shell, recipe, systemd, udev and C row read, the 30 config files read, busybox's three configurations at the flagged lines and the rest scanned; the 29 units and the GENERIC_X64 quirks run on one guest (`02` § The guest cycle).
**Deliberately not examined:** `quirks/devices/**` (T29's), the interface and launch scripts beyond their call sites (T1, T2), the cloud scripts (T16, T17).
**Dimensions not exercised:** anything on a handheld: the H700 and SM8550 platform quirks run (read only), `QUIRK_DEVICE`'s device-tree branch, `sleep.d/` on a real suspend, `volume-fixup` (RK3566), an inserted btrfs medium's effective mount options (F-04), a `textmode` boot (F-07).

## Finding Verification (Phase 4.5)

No finding is Critical or High. The four with a reachable consequence were
re-read at their lines after the guest window:
- **F-01:** `autostart:73-76`, and the guest's `40 uid=0 args=[split]`.
- **F-03:** `busybox/package.mk:177,209`, and `mode=4755` on the guest.
- **F-04:** `udevil.conf:209,213,233`.
- **F-05:** the unit's line, and the guest's `No such file or directory`.

## Renovation face

### Q1 Modernize

- **The two collisions (F-12, F-13)** are the modernization the next base merge forces. Each carries a design sentence in `02` § The upstream delta, deferred to the coordinator; no edit.
- **The hook directories** (`/storage/.config/autostart/`, `/storage/.config/profile.d/`) are LibreELEC's design, and T1 named the autostart shape as a design the coordinator holds. This slice adds that both run as root, last in the boot order, and that the custom loop is unguarded (F-01).

### Q2 Standards and best practices

- **F-15:** 29 units, no `User=`. On a single-user handheld this is the platform's choice, recorded as a design.
- **F-02:** `/etc/profile`'s loop is guarded but unquoted.
- **F-16:** `systemctl is-enabled` misleads on these images.
- **The inventory's `last_upstream_commit`** is upstream's tip, not the read tree's (brief § 2; T10's): it is cited here as the tip's.

### Q3 Bugs

The root-and-writable-path findings, each with its bug decision (proposed; stage D settles it) and its `Already written:` line:

| Finding | Writable input | Guard | Decision proposed | Already written |
| --- | --- | --- | --- | --- |
| F-01 | `/storage/.config/autostart/*` | none | `bug` (the guard and quotes are contained, `bugs-are-agent-first.md` rule 6); class decision #346 (upstream-carried) | nothing inherited: the loop reads the directory at each boot and writes nothing |
| F-02 | `/storage/.config/profile.d/*` | `-f` | design | nothing inherited |
| F-03 | none (an applet surface) | -- | `bug`-candidate for #346: disable the four applets in the configuration, or a design row | nothing inherited: a configuration choice |
| F-04 | an inserted btrfs medium | `udevil.conf` | `bug` (#346): the file's own warning; a VM proof of the effective mount is owed (a loop-backed btrfs on the guest) | mounts made under it are transient; nothing on `/storage` |
| F-05 | -- | `-` prefix | `bug` (#346): remove the post lines, or ship the script | nothing inherited |
| F-06 | `/usr/config/ssh` at build | `-e` test | cited on #740 with the second site | on a developer's device built with `LOCAL_SSH_KEYS_FILE`: a file `/storage/.ssh`; #740's own line |
| F-07 | tty1 on a `textmode` boot | the boot mode | design | -- |
| F-08 | three markers | -- | design | -- |

### Q4 Package currency: every pin at both hashes

| Package | Pin at `8ebaf8daad` | At `651150fc88` | Author's release | Note |
| --- | --- | --- | --- | --- |
| busybox | 1.36.1, http (`package.mk:7,11`) | 1.38.0, https | `CANNOT (no network)` | settled by the next base merge; the generic recipe already 1.38.0 (#997) |
| systemd | 255.8 (`systemd-stable`) | 261.2 | `CANNOT (no network)` | the generic recipe 261.2 at both; the override shadows it until the merge |
| util-linux | 2.39.2 | 2.42.4 | `CANNOT (no network)` | the generic recipe 2.42.2 at both |

`tools/fork-package-freshness` covers only the packages the fork introduces; none of these three is one (D-WORKFLOW-024).

### Q5 Efficiency

- **Bytes shipped and never run:** 213 platform files, 108,294 bytes, by directory:

  | Directory | Files | Bytes |
  | --- | ---: | ---: |
  | SM8250 | 30 | 23,075 |
  | SM6115 | 31 | 19,262 |
  | SM8750 | 26 | 12,944 |
  | SM8650 | 24 | 10,769 |
  | RK3566 | 16 | 6,921 |
  | SM4450 | 13 | 6,748 |
  | AMD64 | 18 | 6,723 |
  | RK3326 | 12 | 6,250 |
  | S922X | 10 | 4,286 |
  | RK3588 | 12 | 4,032 |
  | RK3576 | 13 | 3,845 |
  | RK3399 | 8 | 3,439 |

  Small against an image; the cost is the reader's, not the card's.
- **busybox's enabled applets against their callers:** `su`, `login`, `passwd` and `httpd` (with CGI, `/etc/httpd.conf` and a `/usr/www` webroot) have no caller (F-03); `nc` has 3 and `udhcpd` 1.

### Q6 Dead ends: a disposition per unit

- **The 8 `system-utils` rows no shipped image installs** (AMD64 3, RK3399 3, RK3566 1, S922X 1): *carried by placement* (D-WORKFLOW-185). They serve the devices upstream builds.
- **The 213 platform files, by directory** (AMD64, RK3326, RK3399, RK3566, RK3576, RK3588, S922X, SM4450, SM6115, SM8250, SM8650, SM8750): each directory is *carried by placement*. They serve upstream's devices, and the run-time selection is upstream's design.
- **The 9 files upstream deleted:** *settled by the next base merge*.
- **Cron's three files (F-09):** *carried, off by option* (`CRON_SUPPORT`).
- **`samba-autoshare`'s two lines (F-05):** the dead lines of F-05's decision.
- **`volume-fixup.service`:** RK3566's, carried by placement.
- **Removals:** none.

### Q7 Clarity and structure

A reader cannot tell from the tree which units run on which device, or which
quirks a boot selects. Three things would let them:
- the two `package.mk` files saying what they ship (F-14);
- `098-deviceutils` being the place the five sensing units start;
- the boot order (platform, device, common, custom) being written down.

The reachability and units tables in `02` are that record for this
reading, and T29 inherits their *runs on* column.

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- A check that every unit's `Exec*` path exists in the image would have caught F-05 (blindspot 16). The guest read here is a manual instance.

### Codification Gaps (needs-new-rule)

- `generic-x64-vm-testing.md` could say that `systemctl is-enabled` is not the enablement answer on these images, and that the `.wants` links are (F-16). Proposed to the coordinator; this lane edits no rule.

### Recommended Action Sequence

1. F-01, F-04 and F-05 to #346 with their traces.
2. F-06 as a comment on #740.
3. F-12 and F-13 to the coordinator before the next base merge.

## Second opinion (Phase 4.6)

Depth **extended**, with two seats: GPT-6 Astra at `max` and Gemini 4 Argon at `high`, each a probe and then one refutation, through the Facilitator. *Pending: the seats run after this section is written; their grades replace this line.*

## Quality Self-Check

| Item | Status |
| --- | --- |
| Acceptance Criteria Scorecard present, IDs match #669 | present (AC-01 to AC-18) |
| Coverage Boundary present (02 + 04) | present |
| Finding Verification recorded for all Crit/High | none at those grades; the four reachable findings re-read |
| Second opinion recorded (Phase 4.6) | pending |
| Instruction File Recommendations (epic) | present |
| Verdicts use the defined vocabulary only | yes |
| Traceability / Evidence / Reproducible / Actionable / Complete | self-checked against `02` |


## Context: docs/reviews/order.md § T22

### T22. os-scripts-and-launch: the OS's system services and platform quirks

- **id**: `os-system-services`; **kind**: read; **lens**: security, brittleness
- **why here**: busybox's configuration, the systemd units and the per-platform quirks run as root on every device; the inventory reads a whole package as reached, so `system-utils`' per-device sources (`sources/devices/` for AMD64, GENERIC_X64, RK3399, RK3566 and S922X, `sources/autostart/AMD64`) read `shipped` although `package.mk` installs only `${DEVICE}`'s: the slice first derives which the shipped pair (H700, SM8550, which have none) and the VM install, as T29 does for the quirks, reads those line by line, and records the rest as unshipped rows (the coordinator's read of the third version)
- **paths** (422 paths, 16,604 lines, 10,898 read, of which 3,002 fork-own; 0 patch and config lines; reach shipped 422): areas `os-scripts-and-launch`; globs `projects/ROCKNIX/packages/sysutils/**`, `projects/ROCKNIX/packages/hardware/**`, `!projects/ROCKNIX/packages/hardware/quirks/devices/**`
- **read before**: none
- **depth**: Extended -- the systemd units and services run as root on every device (security lens; plan § 6c)
- **interacting subsystems** (read-only context): `os-launch-control-state`'s scripts; `ApiSystem` (`es-state-and-bridge`); the devices' options; the game-end and autostart hooks (`sysutils/autostart`, read here)
- **closing evidence**: audit folder, lint PASS, VM proofs for boot behaviour, punch list through Phase 7


## Context: the brief § 2 Scope

## 2. Scope

**422 paths, 16,604 lines; 10,898 lines read by the survey's language rule
(shell, recipe, systemd, udev and one C file), 3,002 of them fork-own (24 paths);
0 patch and config lines; upstream-carried 398 paths; reach shipped 422.**
By group: the quirks 275 paths / 5,275 lines; systemd 41 / 1,732; busybox
36 / 6,507; `system-utils` 28 / 1,367; `autostart` 5 / 154; 23 other
`sysutils` packages. The membership is `slices.json` k 22's rule on
`inventory.json` at `2174265e9c`: area `os-scripts-and-launch`, reach
`shipped`, under `projects/ROCKNIX/packages/sysutils/**` and
`projects/ROCKNIX/packages/hardware/**`, **minus**
`projects/ROCKNIX/packages/hardware/quirks/devices/**` (T29's). The tool's
own `slice_of` (`tools/renovation-inventory:1237-1248`; `load_slices` at
`:1211-1236`) and the translator below agree on the set:

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,re,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
def rx(g):
    g=re.sub(r"\{([^}]*)\}", lambda m: "(?:"+"|".join(m.group(1).split(","))+")", g)
    out=""; i=0
    while i<len(g):
        if g.startswith("**/",i): out+="(?:.*/)?"; i+=3
        elif g.startswith("**",i): out+=".*"; i+=2
        elif g[i]=="*": out+="[^/]*"; i+=1
        elif g[i] in "(|)?:": out+=g[i]; i+=1
        else: out+=re.escape(g[i]); i+=1
    return re.compile("^"+out+"$")
INC=[rx("projects/ROCKNIX/packages/sysutils/**"), rx("projects/ROCKNIX/packages/hardware/**")]; EXC=rx("projects/ROCKNIX/packages/hardware/quirks/devices/**")
t=[r for r in rows if r["area"]=="os-scripts-and-launch" and r["reach"]=="shipped" and any(p.match(r["path"]) for p in INC) and not EXC.match(r["path"])]
READ={"shell","recipe","systemd","udev","c"}   # the survey counts these five as read; the dictionary below has no python or make
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t))
print("read",sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ),"fork-own read",sum(r["lines"] or 0 for r in t if (r.get("language") or "") in READ and r["tier"]=="fork-own"),"fork-own paths",sum(1 for r in t if r["tier"]=="fork-own"))
print("tier",dict(collections.Counter(r["tier"] for r in t)),"reach",dict(collections.Counter(r["reach"] for r in t)))
print("language",dict(collections.Counter((r.get("language") or "none") for r in t)))
g=collections.Counter("/".join(r["path"].split("/")[3:5]) for r in t); print("groups",dict(g.most_common(6)))
import os; os.makedirs(".qa-scratch/t22", exist_ok=True)
open(".qa-scratch/t22/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))
print("written", len(t), ".qa-scratch/t22/paths.txt")'
# (the sorted(..., key=...) above is Python's keyword, not a credential: a reader applying the read filter to this block drops that line and sees nothing written -- run the block raw)
# paths 422 lines 16604
# read 10898 fork-own read 3002 fork-own paths 24
# tier {'upstream-carried': 398, 'fork-own': 24} reach {'shipped': 422}
# language {'shell': 299, 'recipe': 28, 'other': 7, 'none': 21, 'symlink': 2, 'systemd': 29, 'config': 30, 'c': 1, 'udev': 5}
# written 422 .qa-scratch/t22/paths.txt
```

A different count is a delta to record with the command, not a reason to
stop. (The five read languages are shell, recipe, systemd, udev and the one C
file, `evtest.c`; the stranger's proof found that set and no other sums
to 10,898.) **The read count excludes every `config` file**: the
three busybox configurations (3,648 lines), the sysctls, the tmpfiles and
the systemd drop-ins are in the slice and in no count the depth was sized
on; the security lens reads them anyway, so the slice is 16,604 lines of
reading, not 10,898.

**Two selection mechanisms, and the `why` named only one.**
*Install-time:* `projects/ROCKNIX/packages/sysutils/system-utils/package.mk:27-34`
installs the generic scripts (`:14-15` also `sources/autostart/common/*`
on every build) and then only `sources/devices/${DEVICE}/*` and
`sources/autostart/${DEVICE}` -- so **8 rows / 317 lines marked
`shipped` are installed by no shipped image** (AMD64's, RK3399's,
RK3566's, S922X's), the VM installs `GENERIC_X64/video_sense` (fork-own),
and H700 and SM8550 have no device directory; the device files are copied
*after* the generic ones into `/usr/bin`, so `RK3399|RK3566|S922X/headphone_sense`
overwrite the generic one on those builds. *Run-time:* the quirks'
`package.mk:18` copies **every** `platforms/*` into every image that has a
platform directory of its own (`:16`, true for H700, SM8550 and
GENERIC_X64; `:15` copies every `devices/*`); selection happens at boot by `${HW_DEVICE}` (from
`/etc/os-release`, written by `scripts/image:156`) in `/usr/bin/autostart:16-28` (the file is
`sysutils/autostart/sources/autostart`, 97 lines) and by `${QUIRK_DEVICE}`
(the device-tree model, or DMI vendor and product, set in
`autostart/profile.d/002-autostart:6-12`) at `/usr/bin/autostart:31-43` -- so **213 of the
264 platform files are shipped bytes that never run on H700, SM8550 or the
VM**. The slice's reachability table carries a third column, **runs on**
(H700 / SM8550 / VM / none), beside *installed on*, with the line that
decides each.

**The units: 29 files, 397 lines, none with `User=` or `Group=` -- all
root.** The lines the security lens reads first: `shell.service` (an
unauthenticated root shell on tty1, `exec /bin/sh`); `/usr/bin/autostart:71-77`
running `/storage/.config/autostart/*` as root (the `exec` at `:76`), and
`:50-54` running `/usr/lib/autostart/common/*` -- neither loop carries an
`-f` test;
`cron.service` (crond over `/storage/.cache/cron/crontabs`);
`udevil-mount@.service` (any inserted medium mounted, then `samba-autoshare`
in `ExecStartPost`); `userconfig-setup` (#740: copies `authorized_keys` and
the Wi-Fi files at first boot, and makes a *file* named `/storage/.ssh`);
`video.service` -> `/usr/bin/video_sense`, which only the GENERIC_X64 and
RK3399 builds install (`git ls-tree` of `system-utils/sources/devices/*/video_sense`;
blindspot 16's shape). **`system-utils/package.mk` has no `post_install`**
(one function, `makeinstall_target`), `scripts/install` only copies
`system.d/*`, and no `enable_service` under `sysutils/` or the quirks names
`video`, `headphones`, `input`, `fancontrol`, `batteryledstatus` or
`rocknix-autostart.service`: which build enables those six is decided
elsewhere (a preset, another package) -- `git grep -n -E 'enable_service|preset'
8ebaf8daad -- projects packages config` answers it, quoted; `rocknix-autostart.service:9`
(T14's constant). **busybox:** the effective pin is the override's
**1.36.1** (`busybox/package.mk:7`; a plain-http `PKG_URL` at `:11`); the
generic LibreELEC recipe says 1.38.0 and is shadowed (#997, T14's);
`busybox-target.conf` (1,224 lines, `config`): `CONFIG_FEATURE_SUID=y`
`:30`, `LOGIN` `:549`, `PASSWD` `:554`, `SU` `:556`, `HTTPD` `:888` with
`CGI` `:894`, `NC` `:950`, `UDHCPD` `:1010`; `scripts/init` is 1,383
fork-own lines, PID 1. **The fork-own 24** (3,002 lines): `scripts/init`,
`input_sense` (539 lines, which upstream has since rewritten in four
commits), the
five GENERIC_X64 quirks (a developer's tool, D-QA-053, rewritten in eight
commits on 2026-09-28 -- a punch item there is a harness item, not a
product item), `99-coredump.conf`, `sysctl.d/rocknix.conf`,
`hang-policy.conf`, and the rest the block lists; the slice names each
with its last fork commit.

**The read tree is three and a half weeks behind upstream in exactly this
area.** Merge base `c445081a59` (2026-10-01); at `651150fc88` **44 of the
422 differ (M), 20 are gone (D: 9 files upstream never had, 2 the fork
carries that upstream has removed -- `99-coredump.conf` by `8bce25b3b7`,
`sysctl.d/rocknix.conf` by `54acd9556f` --, and 9 real deletions --
`80-clock.rules`, `99-rocknix-networking.conf`, the `file` and `i2c-tools`
recipes, the SM6115 and RK3576 sleep hooks), and 42 are new under the
globs, plus 2 renames (A: busybox 1.38.0's seven patches, 0001 to 0006
and 0010, renames of the override's own `busybox-0X-*.patch` -- the fork
already carries `06-prevent-root-weak-passwd`; `075-scanout-offload` for
SM8550, six files; `games-swap.oomrule`; `20-crash.conf`; `60-rocknix.conf`;
and the rest the lane lists)**; upstream moved busybox to 1.38.0, systemd
to 261.2, util-linux to 2.42.4 (the override; the generic recipe says
2.42.2 at both hashes), added `games.slice` and oomd, replaced core files
with journal crash logging (`8bce25b3b7`, which removes the fork's
`99-coredump.conf` -- D-INFRA-013's keeper), shipped the sysctls in the
image (`54acd9556f`: `qdisc.conf`, `post-update`, `cdrom.conf`,
`99-rocknix-networking.conf` and `sysctl.d/rocknix.conf` deleted,
`60-rocknix.conf` new; `hang-policy.conf` is the fork's own with no
upstream history), and rewrote `input_sense` in four commits (the fork's
539-line fork-own copy). **Every finding on one of
the 44 names the file's state at `651150fc88` beside it**, and a finding
upstream has already fixed is *settled by the next base merge*, not a
bug. **The inventory's `last_upstream_commit` is upstream's tip, not the
read tree's** (`busybox-target.conf` reads `be9a5e4a81 2026-10-04`,
`scripts/init` `03204074ef 2026-10-08`, neither an ancestor of
`8ebaf8daad`): the column is cited as the tip's, never as the tree's.
**History since 2026-06-01 over the 422:** 87 non-merge commits, 33 the
fork's (`Max Engel|blitterbot|rasterabot`) and 54 upstream's (the quirks
48 of which 13 fork's; systemd 17 of which 13 fork's; `system-utils` 9;
busybox 7).


## Context: the brief § 4 The questions

## 4. The questions

The renovation face's seven, each answered in `04-analysis.md` with a
proof in `02` (a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`,
`guest`, `design`); the lens is security first:

- **Q3 Bugs and security -- the lead question.** For every unit and script
  that runs as root (all 29, and the autostart chain): what path it reads
  or executes that the player or a medium can write (`/storage/.config/autostart/*`,
  `/storage/.cache/cron/crontabs`, an inserted medium, `authorized_keys`
  at first boot), what guards it (a `-f` test, a mode, a mount option, an
  allowlist), and what a missing guard lets happen -- read, with the lines.
  A defect with a reachable consequence is a `bug` with its trace, its
  `Already written:` line (what the units have already left on devices:
  a `/storage/.ssh` file, a crontab) and its VM line; `shell.service`'s
  tty1 root shell is a finding with the register searched first
  (`tools/archaeology shell.service tty1`) -- a design upstream chose for
  a handheld, recorded as such unless a row says otherwise. `video.service`
  on a build without `video_sense`: a `bug` only if the unit is enabled
  there. #740 is cited, not re-filed.
- **Q4 Package currency.** busybox 1.36.1 against upstream's 1.38.0 with
  its seven patches (renames of the override's own; `06-prevent-root-weak-passwd`
  already here); systemd 255.8
  in the image against 261.2 upstream; util-linux; the plain-http
  `PKG_URL`; each as the pin at `8ebaf8daad`, at `651150fc88`, and
  `CANNOT (no network)` for the author's release (`tools/fork-package-freshness`
  named, D-WORKFLOW-024).
- **Q6 Dead ends.** The 8 `system-utils` rows no shipped image installs;
  the 213 platform files no shipped unit runs (one disposition per
  platform directory, *carried by placement*, D-WORKFLOW-185); the 9 files
  upstream deleted (*settled by the next base merge*). Removals none.
- **Q5 Efficiency.** The bytes every image carries and never runs (the
  213, with their sizes); the busybox configuration's enabled applets
  against what the scripts call (`SU`, `LOGIN`, `PASSWD`, `HTTPD`, `NC`,
  `UDHCPD`: which script or unit calls each -- `git grep` -- and which
  none does).
- **Q2 Standards.** The units' missing `User=`; the `-f` test absent at
  `autostart:50-54`; the two selection mechanisms documented nowhere a
  reader of `package.mk` lands; the `last_upstream_commit` column read as
  the tree's (an inventory reading, cited, T10's).
- **Q1 Modernize.** The `/storage/.config/autostart/` hook shape (T1's
  lead, a design the coordinator holds); the collisions upstream's next
  merge brings (`99-coredump.conf`, which `8bce25b3b7` removes;
  `sysctl.d/rocknix.conf`, which `54acd9556f` removes for `60-rocknix.conf`): what the fork keeps, what it yields -- a design
  sentence each, deferred to the coordinator, no edit.
- **Q7 Clarity and structure.** Can a reader tell, from the tree, which
  units run on which device and which quirks a boot selects? Does
  `quirks/package.mk` say it ships every platform?


## Context: docs/decision-register.md: the rows the brief names (D-CLOUD-064, D-CLOUD-072, D-CLOUD-078, D-CLOUD-079, D-CLOUD-080, D-CLOUD-082, D-CLOUD-147, D-INFRA-011, D-INFRA-012, D-INFRA-013, D-NET-001, D-NET-002, D-NET-003, D-NET-004, D-NET-005, D-NET-006, D-NET-009, D-QA-042, D-QA-053, D-QA-063, D-SYS-002, D-SYS-003, D-SYS-006, D-SYS-008, D-SYS-009, D-UI-121, D-WORKFLOW-083, D-WORKFLOW-184, D-WORKFLOW-195, D-WORKFLOW-209)

| D-CLOUD-064 | 2026-09-08 | **The boot autostart runs `cloud_capture --full`, gated on a cloud-saves toggle and backgrounded.** Amends the judged design, which ran it above and outside the `cloudsaves.startup` gate: `102-cloud-saves` runs `--full` only when `cloudsaves.startup` or `cloudsaves.gameexit` is `1`, as `setsid nohup … >/dev/null 2>&1 &` under `nice`, so boot is never delayed and a device with cloud saves off never runs it (#84/D-CLOUD-057: boot time is not ours to spend). Consequence, accepted: on such a device an ES abort mid-game, a shell edit or an equal-size equal-mtime rewrite waits for the first boot after a toggle goes on; with cloud saves off nothing publishes, so nothing is lost meanwhile. Two further consequences of backgrounding, both accepted. **The pass can still be finishing when the first game exits**, so the two are concurrent writers of one manifest: capture takes no lock, the loser sees the file's inode or mtime change between its load and its rename, and an exit, `--rescan` or `--retire` that loses **re-runs itself once** against the winner's document (`CLOUD_CAPTURE_RETRY`), because a discarded first version is not self-healing — with no entry and an mtime below the next `--started` nothing would ever record it; `--full` never retries. **On a two-card device that has never synced** there is no saves-root record, `cloud_saves_root check --wait 10` returns at once, and the pass may hash the internal card's copies before the automount binds the second card — the next exit then records the real file with `replaces` pointing at that stale sha, a bogus lineage step; a flip *during* the pass is discarded, the pre-first-sync window is not (a device that has never synced has published nothing yet). #22's reconciler runs `--full` inside its own lock as the first step of every pass. | #21, #84; #21; `feature/capture` (hash at commit) |
| D-CLOUD-072 | 2026-09-09 | **EmulationStation owns the startup saves sync and shows it (refines D-CLOUD-038, D-CLOUD-064; delivers #94).** The autostart keeps only the `cloud_capture --full` pass; ES runs restore-then-backup (`--method=copy --update --saves-only`) through `ThreadedCloudSync` once the interface is up, with the same card and outcome the exit sync shows. Fork resolved during execution: the first cut held the launch gate for the whole network wait (up to two minutes offline), which fails the #84 standard for boot cost. Taken: **no route means no wait** (exit 4 within a second, `SKIPPED - NO NETWORK CONNECTION`); a link without internet is probed for at most 60 s under `WAITING FOR THE NETWORK...`; **a game launched during that wait cancels the sync** (`setsid` group killed, outcome `SKIPPED - A GAME WAS STARTED`, stamp rc 130) instead of being refused; the refusal (`YOUR SAVES ARE SYNCING...`) applies only once rclone is moving files. Every ES-started sync stamps `last-sync-<startup\|exit\|manual>` (`<epoch> <rc>`), and the two toggles on the CLOUD page read them as `LAST <date> <time> - SUCCEEDED\|STOPPED\|FAILED\|SKIPPED, ...`. Accepted residuals: the sync re-runs on an ES restart (once per process); a launch in the first probe's four seconds is refused, not cancelled; dates are absolute, matching the neighbouring rows. | #94; ES `296d326f5` on `feature/startup-sync`, merged `e521985f2`; `102-cloud-saves` `234cedd7dc` |
| D-CLOUD-078 | 2026-09-10 | **Always keep a record of the last known good state. A failure reverts to it; a success becomes it, and the previous record is then removed (refines D-CLOUD-077).** Maintainer: *"we should always keep a record of the last known good state, which hopefully is a fairly straightforward but powerful rule. That way, if something fails, it should always revert to the last known good state. This also means we should always know when something is successful, and therefore the successful state becomes the last known good state, and we can remove the previous one."* Three obligations follow for every writer: (1) it must *know* when it succeeded -- a positive check of the artifact, never the absence of an error (engineering-practices § guards fail closed); (2) the new state replaces the old only after that check -- temp-and-rename, a marker written after the bytes are confirmed, a copy kept until the replacement is verified; (3) the superseded record is removed once, after the new one is good, so there is exactly one last-known-good at rest. Where it already holds: rclone's per-file rename, the settings-upload marker, `backuptool`'s rotation, the capture stage (content-addressed copies of every save the manifest claims), the device id's `.previous`, the `last-*` stamps. Where it does not yet: `system.cfg` and `es_settings.cfg` are rewritten in place and `chksysconfig` overwrites its `.backup` every boot with whatever is there -- so the RG SP's truncated file replaced its own good copy and defaults won (#102); a saves restore that overwrites a newer local copy keeps no previous version (`--backup-dir` would). Work: #105 (messages and retries), #104 (config files kept last-good and restored from it at boot instead of defaults), #22 (the reconciler's kept losers are this rule for saves). | #105, #104, #22, #102 |
| D-CLOUD-079 | 2026-09-10 | **The config files' last-known-good record keeps its existing name and changes its meaning: `system.cfg.backup` (and, new, `es_settings.cfg.backup`) is written only from a file that has just been validated -- at boot after the check passes and at shutdown -- via temp-and-rename; a boot that finds the live file empty, truncated, or unparsable restores it from that record and logs the recovery, and reseeds defaults only when the record is missing or invalid too; the blanket `rsync -a /usr/config/ /storage/.config` is scoped to the files actually missing (implements D-CLOUD-078 for #102's loss).** Keeping the name means one record at rest and no migration; the scripts audit recommended it over a new `.last-good`. EmulationStation's own writers rename their temp into place (`SystemConf` already writes a `.tmp` and then copies it; `Settings` writes in place) and take the settings lock around the read-modify-write. Migration copies the helper keeps forever (`cloud_sync.conf.bak`, `cloud_sync-rules.txt.bak`, `.pre-copy-default`) are removed after the next successful run, per D-CLOUD-078(3). | #105, #104, #102; docs/audits/2026_09_10-graceful-degradation |
| D-CLOUD-080 | 2026-09-10 | **`system.cfg` is verified against its last-known-good record at sysinit, before anything reads it: `rocknix-sysconfig.service` runs `chksysconfig verify` after `userconfig.service` and before `network-base.service` (extends D-CLOUD-079).** `network-base-setup` applies `system.hostname` at about 1.7 s; the autostart chain that held the only verify runs seconds later, so a damaged file gave the device an empty hostname (`localhost`) for the whole boot even once the record had been put back, and a reseeded one gave it the image's name -- the RG SP's `H700` (#102). The record is the first source and the image defaults the last, in the same boot the damage is found; verify is idempotent and 001-setup keeps its call. `f907e7f526`. | #105, #102 |
| D-CLOUD-082 | 2026-09-10 | **The boot-time revert of a cut-off restore runs at whichever `chksysconfig verify` finds the copy's folder mounted (refines D-CLOUD-081).** The copy lives under the settings backups folder on `/storage/roms`, a bind mount `rocknix-automount` makes at about 2.5 s, after the sysinit verify (D-CLOUD-080) at 1.7 s. The sysinit run leaves the marker when the folder is not there yet and says so in the log; the autostart chain's verify (001-setup, after the mounts) puts the copy back. A folder present without the copy, or a copy that does not list, is the failure that is reported. Found on guest d: the first build said `COULDN'T BE UNDONE` with the copy sitting on the not-yet-bound folder. `61024a4d76`. | #105 |
| D-NET-001 | 2026-09-10 | **The device name is the player's and is stored as typed; the network name is derived and shown, never enforced (refines D-CLOUD-080).** Maintainer: *"let them enter whatever they want and then just have our own logic for stripping out and replacing invalid characters ... sanitize it behind the scenes ... we could add that below the IP address so we could show their IP address and then show their host name."* So no character rule at entry, `system.hostname` keeps what was typed, `network-base-setup` applies the cleaned form (letters, digits, hyphens) at boot without writing it back, and NETWORK SETTINGS shows `NETWORK NAME` under `IP ADDRESS` when the two differ. NetworkManager is told `hostname-mode=none` so there is one writer. ES `1593c299f`, `cba363e002`. | #106 |
| D-SYS-002 | 2026-09-10 | **systemd arms the hardware watchdog at 15 s and leaves the reboot watchdog off.** 15 s because the Allwinner watchdog counts to 16 at most and a longer figure is refused by the driver, which would leave systemd running with no watchdog; a kernel that has stopped scheduling is reset within 15 s instead of staying frozen until the power button. `RebootWatchdogSec=off` because the same ceiling would reset a device mid-way through a slow sync to the card at shutdown -- the corruption this is meant to prevent -- and systemd disarms the runtime watchdog when it hands over to shutdown, so a hung shutdown is as it was. Revisit when `WATCHDOG_SYSFS` reports a longer ceiling on other families. | #104 |
| D-SYS-003 | 2026-09-10 | **A soft lockup or a hung task panics, and a panic reboots after ten seconds; an oops does not.** `softlockup_panic=1`, `hung_task_panic=1`, `panic=10` in `/usr/lib/sysctl.d/hang-policy.conf` (image-level, so it applies on the first boot after an update and a device's own `/storage/.config/sysctl.d` still wins). `panic_on_oops` stays 0: with the journal persistent an oops is captured anyway, and the player keeps their session. | #104 |
| D-SYS-008 | 2026-09-11 | **`powerstate` skips its battery checks for a pass when there is no numeric reading, and never exits on a device without a battery.** The alternative -- leave the loop when `/sys/class/power_supply` has no battery -- would also leave it on a handheld whose battery driver probes late, and the loop's AC-status half still has work there. The first battery's reading is taken when there are several. | #121, `8d2f384d1c` |
| D-NET-002 | 2026-09-13 | **The shipped device name is the build family, and at boot it becomes this unit's own once -- `<FAMILY>-<four hex digits of the unit's id>` -- written back to `system.hostname`; a name equal to the family, or empty, is the shipped default and never something a player typed, and every other name is the player's and is never touched (extends D-NET-001).** Two units of one family on one network claimed the same DHCP name and the router's lease flipped between them; the failure read as EHOSTUNREACH and sent the maintainer to Wi-Fi and SSH rather than to a name collision (#50). The suffix comes from `cloud_device_id`, seeded from the permanent hardware address, so a reflash gives the same name; the setting is written once so it is stable and is what NETWORK SETTINGS shows. The upgrade path is the same rule: a device upgraded with its family name still set gets its own name at the first boot of the new image, and a device the player renamed keeps its name. Proven on three GENERIC_X64 guests (491f, 15ca, 0964) and by `last-good-scripts-test` case m. | #50, `d857ba04c9` |
| D-NET-003 | 2026-09-13 | **The device answers for its own `.local` name: `avahi-daemon.service` is enabled, ordered after `network-base.service` so it publishes the name D-NET-002 has just made this unit's own, and `network-base-setup` no longer calls `avahi-set-host-name` (the daemon was never running that early; the call failed on every boot). `/storage/.cache/services/avahi.disabled` still turns it off (settles the open D-NET-003).** Maintainer: "We should turn back on the mDNS responder." The responder had been commented out since the fork's first commit (`9f1fab30f6`) with no reason recorded; the device could resolve other `.local` names through nss-mdns and never be found by its own, so a handheld was reachable only through its DHCP lease -- the lease two same-family units flipped between them (#50). Nothing else answers on 5353: systemd-resolved runs with mDNS off. What the VM proves: the daemon up and publishing `<name>.local` in its journal; what only the LAN proves: a laptop resolving `RG-SP-xxxx.local`, since QEMU's user-mode network carries no multicast. | #50, `e76bafe860` |
| D-NET-004 | 2026-09-13 | **A stored device name of the generated shape -- the family as the network spells it, a hyphen, four hex digits -- whose digits are not this unit's is another unit's shipped default, carried here by a settings restore; `network-base-setup` re-derives it at boot and logs whose it was. A typed name (`Max Deck`) is kept, and another family's name, generated or not, is left alone as the bare family is (extends D-NET-002).** Unit A boots as `H700-9a3f`; the player restores A's settings on unit B -- the fresh-handheld journey, where `cloud_restore` offers another device's folder on purpose -- and B's `system.cfg` says `H700-9a3f`, neither the family nor empty, so the D-NET-002 branch read it as the player's and both units kept one name, permanently where before #50 it was per boot. Reproduced on the GENERIC_X64 pair: a's archive restored on b, b rebooted as `GENERIC-X64-15ca`, a's name (#151 PL-02). The alternative -- dropping `system.hostname` from the settings archive beside the passwords -- was not taken: D-NET-001 says the name is the player's, and a name they typed should follow their settings onto the next device. The cost accepted, as under D-NET-002: a player who typed exactly their family's generated shape with digits not their unit's loses it. Proven by `last-good-scripts-test` case m (`H700-15ca` becomes `H700-9a3f`, `GENERIC-X64-15ca` becomes `GENERIC-X64-9a3f`, `Max Deck` and `RK3566-15ca` stay) and by the fixed script run by hand on guest b; the boot-time proof on a rebuilt image is owed on #151. | #151 PL-02; D-NET-001; D-NET-002; #50 |
| D-NET-005 | 2026-09-13 | **The boot-time namer never seeds the device identity: `network-base-setup` asks `cloud_device_id --if-present`, which returns the stored id, or the adapter's hash computed and not stored, or nothing when there is no adapter yet -- and with nothing the shipped name stays for a later boot, logged as "adapter not present yet, keeping the shipped name" (refines D-NET-002's reflash clause).** `network-base.service` runs at ~2 s of the first boot (`DefaultDependencies=no`, after `local-fs.target`), before a handheld's SDIO wifi is an interface, and a plain `cloud_device_id` there falls back to machine-id and stores it; the stored value then wins, so a unit's id, its name suffix and its cloud folder would depend on whether the adapter beat the unit on the first boot, and a reflash whose first boot found the adapter would derive a different one (#151 PL-04). This is the audit's option (a); option (b), ordering the unit after the adapter, was device-specific (`sys-subsystem-net-devices-wlan0.device`) or a new oneshot after udev settle. Seeding stays with the callers that have the network up. Proven by `last-good-scripts-test` case m: the real tool against a fake `/sys/class/net` (nothing and no file without an adapter; the adapter's hash, unstored, with one; the stored id afterwards) and the namer keeping H700 without an adapter and naming the unit on the boot that finds one. The handheld proof -- two fresh flashes of an H700, the stored id equal to the MAC hash and the suffix its first four digits, or the first boot logging the kept name and the second renaming -- is still owed and stays on #151. | #151 PL-04; D-NET-002; #50 |
| D-NET-006 | 2026-09-13 | **D-NET-003 did not hold as shipped, and the off-switch it names is not one: every image since `e76bafe860` carries avahi's stock socket-activated `avahi-daemon.service`, not the fork's ordered copy.** The override recipe (`projects/ROCKNIX/packages/network/avahi/package.mk`) is upstream's minus `rm -rf ${INSTALL}/usr/lib/systemd`, so `scripts/install` copies the fork's `system.d/avahi-daemon.service` first and then extracts the package's own unit over it; the shipped unit has `Requires=avahi-daemon.socket`, `Type=dbus`, no `After=network-base.service` and no `ConditionPathExists`, and starts from `basic.target` at ~1.8 s, reading the kernel name whenever it comes up. On `519f40aa0c` the ordering held on guests a and d by timing (a: network-base done 1.83 s, avahi up 1.85 s; d: avahi up 2.04 s, name written 2.10 s and read during startup) and failed on guest b (avahi up 1.78 s, `Host name is ROCKNIX.local` at 2.76 s, `GENERIC-X64-0964` written at 2.79 s); nothing re-publishes -- `avahi-set-host-name` was removed as redundant and the unit has no reload. `avahi-defaults.service` has never run on any guest: the fork's file has no `[Install]` section, so `enable_service` made no symlink and only the fork's daemon unit's `Requires=` would pull it in; `/storage/.cache/services/` holds `sshd.conf` alone -- no `avahi.conf`, no `avahi.disabled`. **So on the shipped unit `avahi.disabled` does nothing** (only the never-run defaults unit reads it); the responder stops for a boot with `systemctl stop`, and durably only by a `/dev/null` link named `avahi-daemon.service` and `avahi-daemon.socket` under `/storage/.config/system.d/`, which no page offers. **On the fork's unit, once PL-01's recipe line ships it, the off-switch is two files, not one:** `rm /storage/.cache/services/avahi.conf && touch /storage/.cache/services/avahi.disabled` -- the daemon's condition is `avahi.conf`; once the first boot has copied it, `avahi.disabled` alone is inert (the defaults unit that reads it is the only thing it skips) and the `rm` alone is undone at the next boot. An interface toggle would write exactly that pair. The code half is #151 PL-01; the VM proof is `tools/vm-qa`'s pair-identity suite, which now asserts each guest's published `Host name is` line names its own kernel hostname (`d46f7fa227`). | #151 PL-01/PL-18; #50 box 6; `docs/audits/2026_09_13-milestone-stable-before-upstream/01-research-notes.md` § 1.3e-f; D-NET-003 |
| D-NET-009 | 2026-09-13 | **#154, option 1: `set_setting system.hostname default` (and the delete path) writes an empty `system.hostname=` line for this one key instead of removing it, so `chksysconfig`'s sentinel survives and `network-base-setup` re-derives the unit's own name on the next boot (empty is already the shipped-default branch, D-NET-002). The sentinel itself is not loosened (#102's failure shape stays guarded).** Maintainer: "With 154. It seems like option one is the more elegant path forward." The orchestrator's recommendation was the same. | #154; D-NET-002; D-NET-004; `chksysconfig`; #102 |
| D-INFRA-011 | 2026-09-14 | **A credential's value never reaches a log or a support bundle, and one helper decides what a credential looks like: `redact_credentials` in `001-functions`. Every launcher write to `exec.log` goes through it (setsettings' `log`, so the Added setting and Fetch lines; runemu's `log` and `loginit`), and `rocknix-evidence` passes every file it archives and every snapshot page through it and refuses to collect or snapshot without it. The key or flag stays and the value reads `<redacted>`; an empty value stays empty, since whether a credential is set may be shown (D-INFRA-010) and only what it is may not. The emulator's own stdout stays a direct redirect into `exec.log`, not a pipe through a filter: a running game's life must not depend on a second process reading its output, and the bundle pass is the layer that covers what an emulator prints itself.** #176: in verbose mode `exec.log` carried `cheevos_password` on setsettings' two lines and the bundle copied it; a process list carries gopher64's `--ra-password`; EmulationStation logs `runSystemCommand: setrootpass <password>` at LogInfo (`Platform.cpp:830`, off at the shipped `LogLevel=warning`) -- reported for the ES tree, covered on the bundle side by a `setrootpass` shape, not changed in ES during the release candidate. The launcher lines that name no credential (supermodel's and yabasanshiro's `Command:` echoes) are left as they are: a stamp-invalidating change to two emulator packages mid-RC for no credential path. | #176; D-INFRA-010; D-WORKFLOW-021; `tools/last-good-scripts-test` r, s |
| D-SYS-009 | 2026-09-24 | **EmulationStation's fault handler takes no lock and allocates nothing: the signal's name and the frames go to stderr with `write(2)`, installed with `SA_RESETHAND`; SIGINT sets a flag the main loop reads and quits through the loop's own end -- never `exit()` from a handler, which died of SIGSEGV in the teardown on guest d when tried.** Refines #246's handler (which LOGged under `Log`'s plain mutex, so a fault inside the logger became a hang that nothing on the device restarts; D-SYS-006 remains the watchdog question). Proven on guest d: `kill -SEGV` -> the name, the frames, `status=139`, essway back in 2 s. | #258 PL-003; ES `217872e32`, `4fd019f04` |
| D-QA-042 | 2026-09-24 | **RetroArch on a GENERIC_X64 guest draws at the panel's size: the image ships `video_fullscreen_x/y = 640/480` and a boot quirk follows the connected mode, and `tools/time-to-play` fails a run whose RetroArch log names a surface under the panel. Every RetroArch frame read off a guest before this (the #251 measurements among them) was a 240x256 surface scaled by sway and is not evidence about the device's rendering.** Found while doing #255 (D-UI-086); filed as #263. D-UI-084's 14 px floor stands on the maintainer's observation on the device and on `tools/font-stems`' table (10 px 11 % solid, 14 px 87 %), not on the void frames. | #263, #251, #255; blindspot 54 |
| D-QA-053 | 2026-09-28 | **GENERIC_X64 is a developer's tool and is never published as a gameplay image.** Maintainer, 2026-09-28: *"With Generic x64, it is only ever intended to be a test harness and tool for developers, not for actual gameplay. At some point, someone could adapt it if they want, but my interest is strictly in making it a great tool to help with the development."* So the serial root shell (#307 PL-023) stays as the developer channel and says so in its unit; what does nothing on the guest (the quirk set's `/etc` writers, the orphan quirk tree, the updater that copies nothing) is removed or made honest because a tool that lies is a worse tool, not because anyone else boots it; GENERIC_X64 stays out of the PR series (D-WORKFLOW-034). Settles the open question of the same ID. | #307, D-WORKFLOW-034 |
| D-CLOUD-147 | 2026-09-28 | **The last-good records beside a file the settings backup strips or holds back (`.backup`, `.bak`, `.tmp`, `.old`) are held back with it, not stripped**, and the sign-in scan reads `*.backup`, `*.bak`, `*.cfg.*`, `*.conf.*` and `*.ini.*` as config files. Archives already made are not rewritten; the next backup omits the records. Audit of the fixes, B-claude G-B-01. | `backuptool` (`97db4608d4`, stream B follow-up 2) |
| D-INFRA-012 | 2026-09-28 | **The settings lock (`/tmp/.system.cfg.lock`) stays pid-only, bounded by `kernel.pid_max` (4194304 on the image, systemd's `50-pid-max.conf`)**: a dead holder's pid comes round only after about four million processes in one boot. No start-time check: an RTC-less handheld steps its wall clock at first NTP, so a time-based staleness test could take a live holder's lock. B-claude G-B-05 and B-gpt G-B-12 withdrawn on this bound. | `001-functions` (`f3622d3a2d`) |
| D-INFRA-013 | 2026-09-28 | **A core dump is kept only under the cores-folder lock; without it the keeper's note reads "dump NOT KEPT" and no dump is written.** B-gpt G-B-14. | `rocknix-corekeep` (`9a90244e72`) |
| D-UI-121 | 2026-09-29 | **The Nova's stick LED behaviour (#332: the brightness row does nothing on that device, a colour applies only on a change, the default comes on and a first adjustment turns the sticks off) is tracked now and worked after RC2, not in it.** Maintainer: *"this might be deeper issues and LED behavior optimization can wait until this RC is finished, but I do want to track these items."* The rows are upstream's and the quirk script is the device's; the read of both is on the issue; its disposition for RC2's step 0 is this row. | #332; D-QA-012 |
| D-WORKFLOW-083 | 2026-09-30 | **The whole codebase is reviewed adversarially, in tiers, gradually over the fork's `0.0.x` releases: first the fork's own 121,000 lines, then the OS scripts, launcher, recipes and quirks the image runs (about 140,000), then the interface's 185,000; the patches and kernel configurations by provenance, one row each.** Maintainer: *"I'd be interested in running through a complete adversarial code review of the entire codebase"* and *"sounds good. it can happen gradually, but seems like a good thing to do over time with the new fork."* The `code-auditor` skill at milestone tier with both council seats (D-QA-048), each tier its own audit folder and punch list; every punch item resolved through Phase 7 or accepted by a row before `0.1`. Counted 2026-09-30: 1.3 million lines on the distribution's upstream-bound roots, of which half a million are patches and a quarter million configuration. | #339; #335; #338; D-WORKFLOW-081 |
| D-WORKFLOW-184 | 2026-10-22 | **The review-depth defaults of `docs/reviews/plan-for-the-plan.md` § 6c stand: Local (the executor alone; the lint and the counts are the check) for a dead-end table, a provenance table or a doctrine read; Independent (the executor plus one GPT-6 Astra review through the Facilitator) for an ordinary code slice; Extended (Astra plus Gemini 4 Argon) for a security, state-preservation or launch-path slice, the cloud sync and the updater. P1 records the depth on every slice issue before dispatch and may argue a per-slice downgrade in `order.md` with its reason; the executor's lab is never the reviewer's (D-WORKFLOW-181).** Put to the maintainer by the coordinator lane (D-WORKFLOW-183) as plan § 11's third open question: do the defaults stand, or should more of the upstream-carried slices run Local to hold the OpenRouter credit (D-WORKFLOW-049) for the fork-own ones? Maintainer, 2026-10-22: *"Yes, the default stand."* Recorded on #346 marked RELAYED; the order's own row (#641) takes the next free ID above this one. | #346; #641; D-WORKFLOW-137; D-WORKFLOW-181; D-WORKFLOW-183; D-WORKFLOW-049; `docs/reviews/plan-for-the-plan.md` § 6c, § 11 |
| D-WORKFLOW-195 | 2026-10-24 | **An Extended seat whose answer the model's output ceiling cuts on the packet is run again on a trimmed packet for that seat -- the same model, effort and provider; the analyses and tables whole, the cited files as line-numbered excerpts with context, the ask bounded -- never a model or effort substitution and never the same packet again.** `04` § Second opinion says the seats saw different evidence; an item one seat saw only in excerpt carries `excerpt`, and a disagreement that could be the excerpt's doing is resolved from the artifact, not from either seat. A fork resolved during execution on T30 (#677): Argon at `high` spent about 57k of its 65.5k output tokens reasoning on a 438 KB packet three times (`finish=length`), where T3's 308 KB packet took 30k. The maintainer may reverse it by a new row. | #677, #798; `adversarial-council.md` § Council model floor; the T30 hold post of 10:04 UTC and the coordinator's answer the same hour |
| D-QA-063 | 2026-10-25 | **Every fork suite shares one exit lattice: 1 when any case failed; else 3 when any case was skipped or was judged by something that is not device evidence (a host-tool run under `--host-diagnostic` or `--unverified-busybox`, a missing busybox); 2 on a usage error or an unknown selector; 0 only when every case ran as evidence and passed. The precedence is 1 over 3 over 0, so a failure is never hidden behind a skip and a skip is never read as a pass.** Generalizes D-QA-061 (`vm-qa`) to the state tests (T14's `--unverified-busybox`, ruled 1 on a failing case on #661) and `last-good-scripts-test`'s `--host-diagnostic` (T15 S1 asked on #662 whether to match T14; it does). The T15 stream brief's `exits 3` was written short and is corrected in the same change; a defect found under the host's applets is still a defect, and a caller reading 3 must be able to trust that nothing failed. | #662, #1018, #661, #940, D-QA-061; `docs/reviews/briefs/t15-streams.md` S1 |
| D-WORKFLOW-209 | 2026-10-25 | **A renovation dead-end table removes nothing and edits no recipe: T23 (and T40, T43 and T25 after it) record a disposition per unit -- dead upstream-carried, shadowed copy with its override live or dead, unshipped, fork-own dead with a proposed removal and its `Already written:` line, or reached after all -- and the removal of upstream-carried dead code is one class decision for the maintainer, put to them on #346 with the table's counts and the cost against the value; a fork-own dead unit's removal is proposed on the punch list and left for the coordinator.** The 1,604 rows are 1,601 upstream-carried: the fork tracks `upstream/next`, a deletion of upstream's file is a modify/delete at every merge (D-WORKFLOW-198's class), and the area futro already held T7 to *deletes nothing upstream carries*. The order's § T23 said *decides the removals*; this row narrows it to *decides the dispositions*. The three IDs before this one are the M7 lane's reservation; this row is the first M6 row after it. | #670, #848, #346; `docs/reviews/briefs/generic-packages-dead-ends.md` § 1 |
| D-SYS-006 | **Does a program that stops need a watchdog too?** D-SYS-002 catches a kernel that has stopped scheduling, not an EmulationStation that is alive and unresponsive or a sync that never ends -- which is what #102 may have been. A userspace watchdog (`WatchdogSec=` on `emustation.service` with `sd_notify`, or a poke from the input service when a hotkey goes unanswered) would restart the interface rather than the device. Wanted only if the state pages ever show a frozen device with a healthy kernel. | #104 |

## File: sysutils/autostart/sources/autostart (at 8ebaf8daad, 97 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  . /etc/os-release
    6  
    7  BOOTLOG="/var/log/boot.log"
    8  
    9  log() {
   10    echo "$(date): Autostart: $*" >>${BOOTLOG} 2>&1
   11  }
   12  
   13  performance 2>/dev/null
   14  
   15  ### Load platform specific quirks
   16  if [ -d "/usr/lib/autostart/quirks/platforms/${HW_DEVICE}" ]
   17  then
   18    log "Run ${HW_DEVICE} quirks."
   19    tocon "Applying ${HW_DEVICE} quirks..."
   20    for script in "/usr/lib/autostart/quirks/platforms/${HW_DEVICE}"/*
   21    do
   22      log "Run ${script}"
   23      if [ -f "${script}" ]
   24      then
   25        "${script}" 2>&1 >>${BOOTLOG}
   26      fi
   27    done
   28  fi
   29  
   30  ### Load device specific quirks
   31  if [ -d "/usr/lib/autostart/quirks/devices/${QUIRK_DEVICE}" ]
   32  then
   33    log "Run ${QUIRK_DEVICE} quirks."
   34    tocon "Applying ${QUIRK_DEVICE} quirks..."
   35    for script in "/usr/lib/autostart/quirks/devices/${QUIRK_DEVICE}"/*
   36    do
   37      log "Run ${script}"
   38      if [ -f "${script}" ]
   39      then
   40        "${script}" 2>&1 >>${BOOTLOG}
   41      fi
   42    done
   43  fi
   44  
   45  ### Start the automount service
   46  tocon "Starting storage services..."
   47  systemctl start rocknix-automount
   48  
   49  ### Run common start scripts
   50  for script in /usr/lib/autostart/common/*
   51  do
   52    log "Run ${script}"
   53    ${script} 2>&1 >>${BOOTLOG}
   54  done
   55  wait
   56  
   57  ### Run device start scripts
   58  if [ -d "/usr/lib/autostart/${HW_DEVICE}" ]
   59  then
   60    for script in "/usr/lib/autostart/${HW_DEVICE}"/*
   61    do
   62      log "Run ${script}"
   63      if [ -f "${script}" ]
   64      then
   65        "${script}" 2>&1 >>${BOOTLOG}
   66      fi
   67    done
   68  fi
   69  
   70  ### Run custom start scripts
   71  if [ -d "/storage/.config/autostart" ]
   72  then
   73    for script in /storage/.config/autostart/*
   74    do
   75      log "Run ${script}"
   76     ${script} 2>&1 >>${BOOTLOG}
   77    done
   78  fi
   79  wait
   80  
   81  tocon "Starting user interface..."
   82  log "Startup complete..."
   83  
   84  ### Re-source the profile so we fetch the correct UI_SERVICE variable.
   85  . /etc/profile
   86  
   87  ### Lock is a prerequisite for emustation
   88  rm /var/lock/start.games 2>&1 >>${BOOTLOG}
   89  touch /var/lock/start.games 2>&1 >>${BOOTLOG}
   90  log "Starting ${UI_SERVICE}..."
   91  systemctl start ${UI_SERVICE} 2>&1 >>${BOOTLOG} &
   92  
   93  DEVICE_CPU_GOVERNOR=$(get_setting system.cpugovernor)
   94  ${DEVICE_CPU_GOVERNOR} 2>&1 >>${BOOTLOG}
   95  log "Autostart complete..."
   96  
   97  clear >/dev/console
```

## File: sysutils/autostart/profile.d/002-autostart (at 8ebaf8daad, 12 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  ### Apply device quirks
    6  if [ -e "/sys/firmware/devicetree/base/model" ]
    7  then
    8    export QUIRK_DEVICE="$(strings /sys/firmware/devicetree/base/model)"
    9  else
   10    export QUIRK_DEVICE="$(strings /sys/class/dmi/id/sys_vendor) $(strings /sys/class/dmi/id/product_name)"
   11  fi
   12  export QUIRK_DEVICE="$(echo ${QUIRK_DEVICE} | sed -e "s#[/]#-#g")"
```

## File: sysutils/systemd/scripts/userconfig-setup (at 8ebaf8daad, 90 lines)

```text
    1  #!/bin/bash
    2  
    3  # SPDX-License-Identifier: GPL-2.0
    4  # Copyright (C) 2017-present Team LibreELEC (https://libreelec.tv)
    5  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    6  
    7  . /etc/profile.d/001-functions
    8  
    9  if [ ! -e "/storage/.configured" ]
   10  then
   11    tocon "Initializing configuration..."
   12    # Copy config files. The three es_*.cfg the OS manages are left out so the
   13    # ln -s below can be made: a copy here would stand where the link goes and
   14    # the link would fail without a word (2>/dev/null), leaving a fresh device
   15    # with a copy where an updated one has a link (post-update). es_savestates.cfg
   16    # was missing from this list for two weeks of builds (audit #258 PL-001).
   17    rsync -a --ignore-existing --exclude={es_features.cfg,es_systems.cfg,es_savestates.cfg} /usr/config/* /storage/.config/ >/var/log/configure.log 2>&1
   18  
   19    if [ -d "/usr/lib/autostart/quirks/platforms/${HW_DEVICE}/config" ]
   20    then
   21      rsync -a /usr/lib/autostart/quirks/platforms/"${HW_DEVICE}"/config/* /storage/.config/ >>/var/log/configure.log 2>&1
   22    fi
   23  
   24    if [ -d "/usr/lib/autostart/quirks/devices/${QUIRK_DEVICE}/config" ]
   25    then
   26      rsync -a /usr/lib/autostart/quirks/devices/"${QUIRK_DEVICE}"/config/* /storage/.config/ >>/var/log/configure.log 2>&1
   27    fi
   28  
   29    ### Apply developer ssh keys if they exist
   30    if [ -e /usr/config/ssh/authorized_keys ]
   31    then
   32      tocon "Update developer keys..."
   33      cp /usr/config/ssh/authorized_keys /storage/.ssh
   34    fi
   35    
   36    ### Apply developer wifi config if they exist
   37    if [ -d /usr/config/iwd ]
   38    then
   39      tocon "Update developer wifi config..."
   40      cp /usr/config/iwd/* /storage/.cache/iwd/
   41    fi
   42  
   43    if [ -e "/usr/bin/emulationstation" ]
   44    then
   45      tocon "Installing themes..."
   46      mkdir -p /storage/.config/emulationstation/themes  >/dev/null
   47      ln -s /usr/share/themes/es-theme-art-book-next /storage/.config/emulationstation/themes/system-theme  >/dev/null 2>&1
   48  
   49      ### Link the game controller database so it is managed with OS updates.
   50      tocon "Configuring controller database..."
   51      rm -f /storage/.config/SDL-GameControllerDB/gamecontrollerdb.txt  >/dev/null 2>&1
   52      ln -s /usr/config/SDL-GameControllerDB/gamecontrollerdb.txt /storage/.config/SDL-GameControllerDB/gamecontrollerdb.txt  >/dev/null 2>&1
   53  
   54      ### Link es configs so they are managed with OS updates: the rsync above
   55      ### excluded these three, so nothing stands where the link goes, and a
   56      ### fresh device ends in the same state as an updated one (post-update).
   57      ### es_savestates.cfg is the save state layout the interface reads first
   58      ### from here; runemu.sh/setsettings.sh carry its launcher contract (#196).
   59      for es_cfg in es_features.cfg es_systems.cfg es_savestates.cfg
   60      do
   61        ln -s /usr/config/emulationstation/${es_cfg} /storage/.config/emulationstation/${es_cfg}  >/dev/null 2>&1
   62      done
   63    fi
   64  
   65    mkdir -p /storage/.config/modprobe.d  >/dev/null 2>&1
   66    touch /storage/.configured  >/dev/null 2>&1
   67    sync
   68  fi
   69  
   70  # Update the library cache with new image or if missing. 
   71  LDSO_STAMP="/storage/.cache/ld.so.cache.osstamp"
   72  OS_STAMP="$(stat -c %Y /etc/os-release 2>/dev/null)"
   73  if [ ! -e "/storage/.cache/ld.so.cache" ] || [ "$(cat "${LDSO_STAMP}" 2>/dev/null)" != "${OS_STAMP}" ]
   74  then
   75    tocon "Initializing library cache..."
   76    ldconfig -X >/dev/null 2>&1
   77    echo "${OS_STAMP}" > "${LDSO_STAMP}"
   78  fi
   79  
   80  if [ ! -d "/storage/.config/locale" ]
   81  then
   82    tocon "Initializing language support..."
   83    rsync -a --delete /usr/config/locale/* /storage/.config/locale/ >/dev/null 2>&1
   84    if [ ! -L "/storage/.config/emulationstation/locale" ] &&
   85       [ -e "/usr/bin/emulationstation" ]
   86    then
   87      rm -rf /storage/.config/emulationstation/locale >/dev/null 2>&1 ||:
   88      ln -sf /usr/share/locale /storage/.config/emulationstation/locale
   89    fi
   90  fi
```

## File: sysutils/system-utils/package.mk (at 8ebaf8daad, 42 lines)

```text
    1  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    2  
    3  PKG_NAME="system-utils"
    4  PKG_VERSION=""
    5  PKG_LICENSE="mix"
    6  PKG_DEPENDS_TARGET="toolchain sleep"
    7  PKG_SITE=""
    8  PKG_URL=""
    9  PKG_LONGDESC="Hardware button support scripts."
   10  PKG_TOOLCHAIN="manual"
   11  
   12  makeinstall_target() {
   13  
   14    mkdir -p ${INSTALL}/usr/lib/autostart/common
   15    cp ${PKG_DIR}/sources/autostart/common/* ${INSTALL}/usr/lib/autostart/common
   16  
   17    mkdir -p ${INSTALL}/usr/bin
   18    cp ${PKG_DIR}/sources/scripts/fancontrol ${INSTALL}/usr/bin
   19    cp ${PKG_DIR}/sources/scripts/headphone_sense ${INSTALL}/usr/bin
   20    cp ${PKG_DIR}/sources/scripts/output_monitor ${INSTALL}/usr/bin
   21    cp ${PKG_DIR}/sources/scripts/hdmi_sense ${INSTALL}/usr/bin
   22    cp ${PKG_DIR}/sources/scripts/input_sense ${INSTALL}/usr/bin
   23    cp ${PKG_DIR}/sources/scripts/ledcontrol ${INSTALL}/usr/bin
   24    cp ${PKG_DIR}/sources/scripts/analog_sticks_ledcontrol ${INSTALL}/usr/bin
   25    cp ${PKG_DIR}/sources/scripts/battery_led_status ${INSTALL}/usr/bin
   26    cp ${PKG_DIR}/sources/scripts/turbomode ${INSTALL}/usr/bin
   27    if [ -d "${PKG_DIR}/sources/devices/${DEVICE}" ]
   28    then
   29      cp ${PKG_DIR}/sources/devices/${DEVICE}/* ${INSTALL}/usr/bin
   30      if [ -d "${PKG_DIR}/sources/autostart/${DEVICE}" ]
   31      then
   32        mkdir -p ${INSTALL}/usr/lib/autostart/${DEVICE}
   33        cp ${PKG_DIR}/sources/autostart/${DEVICE}/* ${INSTALL}/usr/lib/autostart/${DEVICE}
   34        chmod 0755 ${INSTALL}/usr/lib/autostart/${DEVICE}/*
   35      fi
   36    fi
   37    chmod 0755 ${INSTALL}/usr/bin/*
   38  
   39    mkdir -p ${INSTALL}/usr/config
   40    cp ${PKG_DIR}/sources/config/fancontrol.conf ${INSTALL}/usr/config/fancontrol.conf.sample
   41  }
   42  
```

## File: hardware/quirks/package.mk (at 8ebaf8daad, 29 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    3  
    4  PKG_NAME="quirks"
    5  PKG_VERSION=""
    6  PKG_LICENSE="GPLv2"
    7  PKG_SITE=""
    8  PKG_URL=""
    9  PKG_DEPENDS_TARGET="toolchain autostart"
   10  PKG_LONGDESC="Quirks is a simple package that provides device quirks."
   11  PKG_TOOLCHAIN="manual"
   12  
   13  makeinstall_target() {
   14    mkdir -p ${INSTALL}/usr/lib/autostart/quirks/{platforms,devices}
   15    cp -r ${PKG_DIR}/devices/* ${INSTALL}/usr/lib/autostart/quirks/devices
   16    if [ -d "${PKG_DIR}/platforms/${DEVICE}" ]
   17    then
   18      cp -r ${PKG_DIR}/platforms/* ${INSTALL}/usr/lib/autostart/quirks/platforms
   19    fi
   20    chmod -R 0755 ${INSTALL}/usr/lib/autostart/quirks
   21  }
   22  
   23  post_install() {
   24    enable_service led-poweroff.service
   25    if [ "${DEVICE}" = "RK3566" ]
   26    then
   27      enable_service volume-fixup.service
   28    fi
   29  }
```

## File: sysutils/busybox/package.mk (at 8ebaf8daad, 242 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    3  # Copyright (C) 2018 Team LibreELEC (https://libreelec.tv)
    4  # Copyright (C) 2018-present Team CoreELEC (https://coreelec.org)
    5  
    6  PKG_NAME="busybox"
    7  PKG_VERSION="1.36.1"
    8  PKG_SHA256="b8cc24c9574d809e7279c3be349795c5d5ceb6fdf19ca709f80cde50e47de314"
    9  PKG_LICENSE="GPL"
   10  PKG_SITE="http://www.busybox.net"
   11  PKG_URL="http://busybox.net/downloads/${PKG_NAME}-${PKG_VERSION}.tar.bz2"
   12  PKG_DEPENDS_HOST="gcc:host"
   13  PKG_DEPENDS_TARGET="toolchain busybox:host dosfstools e2fsprogs usbutils parted procps-ng gptfdisk libtirpc"
   14  PKG_DEPENDS_INIT="toolchain libc:init glibc:init libtirpc"
   15  PKG_LONGDESC="BusyBox combines tiny versions of many common UNIX utilities into a single small executable."
   16  # busybox fails to build with GOLD support enabled with binutils-2.25
   17  PKG_BUILD_FLAGS="-parallel -gold"
   18  PKG_NEED_UNPACK="${PROJECT_DIR}/${PROJECT}/initramfs"
   19  
   20  # nano text editor
   21  if [ "${NANO_EDITOR}" = "yes" ]; then
   22    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} nano"
   23  fi
   24  
   25  # nfs support
   26  if [ "${NFS_SUPPORT}" = yes ]; then
   27    PKG_DEPENDS_TARGET="${PKG_DEPENDS_TARGET} rpcbind"
   28  fi
   29  
   30  if [ "${TARGET_ARCH}" = "x86_64" ]; then
   31    PKG_DEPENDS_TARGET+=" pciutils"
   32  fi
   33  
   34  pre_build_target() {
   35    PKG_MAKE_OPTS_TARGET="ARCH=${TARGET_ARCH} \
   36                          HOSTCC=${HOST_CC} \
   37                          CROSS_COMPILE=${TARGET_PREFIX} \
   38                          KBUILD_VERBOSE=1 \
   39                          install"
   40  
   41    mkdir -p ${PKG_BUILD}/.${TARGET_NAME}
   42    cp -RP ${PKG_BUILD}/* ${PKG_BUILD}/.${TARGET_NAME}
   43  }
   44  
   45  pre_build_host() {
   46    PKG_MAKE_OPTS_HOST="ARCH=${TARGET_ARCH} CROSS_COMPILE= KBUILD_VERBOSE=1 install"
   47  
   48    mkdir -p ${PKG_BUILD}/.${HOST_NAME}
   49    cp -RP ${PKG_BUILD}/* ${PKG_BUILD}/.${HOST_NAME}
   50  }
   51  
   52  pre_build_init() {
   53    PKG_MAKE_OPTS_INIT="ARCH=${TARGET_ARCH} \
   54                        HOSTCC=${HOST_CC} \
   55                        CROSS_COMPILE=${TARGET_PREFIX} \
   56                        KBUILD_VERBOSE=1 \
   57                        install"
   58  
   59    mkdir -p ${PKG_BUILD}/.${TARGET_NAME}-init
   60    cp -RP ${PKG_BUILD}/* ${PKG_BUILD}/.${TARGET_NAME}-init
   61  }
   62  
   63  configure_host() {
   64    cd ${PKG_BUILD}/.${HOST_NAME}
   65      cp ${PKG_DIR}/config/busybox-host.conf .config
   66  
   67      # set install dir
   68      sed -i -e "s|^CONFIG_PREFIX=.*$|CONFIG_PREFIX=\"${PKG_BUILD}/.install_host\"|" .config
   69  
   70      make oldconfig
   71  }
   72  
   73  configure_target() {
   74    cd ${PKG_BUILD}/.${TARGET_NAME}
   75      find_file_path config/busybox-target.conf
   76      cp $FOUND_PATH .config
   77  
   78      # set install dir
   79      sed -i -e "s|^CONFIG_PREFIX=.*$|CONFIG_PREFIX=\"${INSTALL}/usr\"|" .config
   80  
   81      if [ ! "$CRON_SUPPORT" = "yes" ] ; then
   82        sed -i -e "s|^CONFIG_CROND=.*$|# CONFIG_CROND is not set|" .config
   83        sed -i -e "s|^CONFIG_FEATURE_CROND_D=.*$|# CONFIG_FEATURE_CROND_D is not set|" .config
   84        sed -i -e "s|^CONFIG_CRONTAB=.*$|# CONFIG_CRONTAB is not set|" .config
   85        sed -i -e "s|^CONFIG_FEATURE_CROND_SPECIAL_TIMES=.*$|# CONFIG_FEATURE_CROND_SPECIAL_TIMES is not set|" .config
   86      fi
   87  
   88      if [ ! "$SAMBA_SUPPORT" = yes ]; then
   89        sed -i -e "s|^CONFIG_FEATURE_MOUNT_CIFS=.*$|# CONFIG_FEATURE_MOUNT_CIFS is not set|" .config
   90      fi
   91  
   92      #CFLAGS="${CFLAGS} -I${SYSROOT_PREFIX}/usr/include/tirpc"
   93  
   94      LDFLAGS="${LDFLAGS} -fwhole-program"
   95  
   96      make oldconfig
   97  }
   98  
   99  configure_init() {
  100    cd ${PKG_BUILD}/.${TARGET_NAME}-init
  101    find_file_path config/busybox-init.conf
  102    cp $FOUND_PATH .config
  103  
  104    # set install dir
  105    sed -i -e "s|^CONFIG_PREFIX=.*$|CONFIG_PREFIX=\"${INSTALL}/usr\"|" .config
  106  
  107    #CFLAGS="${CFLAGS} -I${SYSROOT_PREFIX}/usr/include/tirpc"
  108  
  109    LDFLAGS="${LDFLAGS} -fwhole-program"
  110  
  111    make oldconfig
  112  }
  113  
  114  makeinstall_host() {
  115    mkdir -p ${TOOLCHAIN}/bin
  116    cp -R ${PKG_BUILD}/.install_host/bin/* ${TOOLCHAIN}/bin
  117  }
  118  
  119  makeinstall_target() {
  120    mkdir -p ${INSTALL}/usr/bin
  121      [ ${TARGET_ARCH} = x86_64 ] && cp ${PKG_DIR}/scripts/getedid ${INSTALL}/usr/bin
  122      cp ${PKG_DIR}/scripts/dthelper ${INSTALL}/usr/bin
  123        ln -sf dthelper ${INSTALL}/usr/bin/dtfile
  124        ln -sf dthelper ${INSTALL}/usr/bin/dtflag
  125        ln -sf dthelper ${INSTALL}/usr/bin/dtname
  126        ln -sf dthelper ${INSTALL}/usr/bin/dtsoc
  127      cp ${PKG_DIR}/scripts/lsb_release ${INSTALL}/usr/bin/
  128      cp ${PKG_DIR}/scripts/pastebinit ${INSTALL}/usr/bin/
  129      ln -sf pastebinit ${INSTALL}/usr/bin/paste
  130  
  131    mkdir -p ${INSTALL}/usr/sbin
  132      cp ${PKG_DIR}/scripts/kernel-overlays-setup ${INSTALL}/usr/sbin
  133  
  134    mkdir -p ${INSTALL}/usr/lib/rocknix/
  135      cp ${PKG_DIR}/scripts/functions ${INSTALL}/usr/lib/rocknix/
  136      cp ${PKG_DIR}/scripts/fs-resize ${INSTALL}/usr/lib/rocknix/
  137      sed -e "s/@DISTRONAME@/${DISTRONAME}/g" \
  138          -i ${INSTALL}/usr/lib/rocknix/fs-resize
  139  
  140    mkdir -p ${INSTALL}/etc
  141      cp ${PKG_DIR}/config/profile ${INSTALL}/etc
  142      cp ${PKG_DIR}/config/inputrc ${INSTALL}/etc
  143      cp ${PKG_DIR}/config/httpd.conf ${INSTALL}/etc
  144      cp ${PKG_DIR}/config/suspend-modules.conf ${INSTALL}/etc
  145  
  146    # /etc/fstab is needed by...
  147      touch ${INSTALL}/etc/fstab
  148  
  149    # /etc/machine-id, needed by systemd and dbus
  150      ln -sf /storage/.cache/systemd-machine-id ${INSTALL}/etc/machine-id
  151  
  152    # /etc/mtab is needed by udisks etc...
  153      ln -sf /proc/self/mounts ${INSTALL}/etc/mtab
  154  
  155    # create /etc/hostname
  156      ln -sf /proc/sys/kernel/hostname ${INSTALL}/etc/hostname
  157  
  158    # create folder for named tables support
  159      ln -sf /storage/.config/iproute2 ${INSTALL}/etc/iproute2
  160  
  161    # add webroot
  162      mkdir -p ${INSTALL}/usr/www
  163        echo "It works" > ${INSTALL}/usr/www/index.html
  164  
  165      mkdir -p ${INSTALL}/usr/www/error
  166        echo "404" > ${INSTALL}/usr/www/error/404.html
  167  }
  168  
  169  post_install() {
  170    ### This resolves a conflict with the bash package.
  171    if [ "$(readlink ${INSTALL}/usr/bin/sh)" = "busybox" ]
  172    then
  173      rm -f ${INSTALL}/usr/bin/sh
  174      ln -s bash ${INSTALL}/usr/bin/sh
  175    fi
  176  
  177    echo "chmod 4755 ${INSTALL}/usr/bin/busybox" >> ${FAKEROOT_SCRIPT}
  178    echo "chmod 000 ${INSTALL}/usr/cache/shadow" >> ${FAKEROOT_SCRIPT}
  179  
  180    add_user root "${ROOT_PASSWORD}" 0 0 "Root User" "/storage" "/bin/sh"
  181    add_group root 0
  182    add_group users 100
  183  
  184    add_user nobody x 65534 65534 "Nobody" "/" "/bin/sh"
  185    add_group nogroup 65534
  186  
  187    enable_service shell.service
  188    enable_service show-version.service
  189    enable_service var.mount
  190    enable_service proc-sys-fs-binfmt_misc.mount
  191  
  192    # cron support
  193    if [ "$CRON_SUPPORT" = "yes" ] ; then
  194      mkdir -p ${INSTALL}/usr/lib/systemd/system
  195        cp ${PKG_DIR}/system.d.opt/cron.service ${INSTALL}/usr/lib/systemd/system
  196        enable_service cron.service
  197      mkdir -p ${INSTALL}/usr/share/services
  198        cp -P ${PKG_DIR}/default.d/*.conf ${INSTALL}/usr/share/services
  199        cp ${PKG_DIR}/system.d.opt/cron-defaults.service ${INSTALL}/usr/lib/systemd/system
  200        enable_service cron-defaults.service
  201    fi
  202  }
  203  
  204  makeinstall_init() {
  205    mkdir -p ${INSTALL}/bin
  206      ln -sf busybox ${INSTALL}/usr/bin/sh
  207      ln -sf busybox ${INSTALL}/usr/bin/bash
  208      ln -sf busybox ${INSTALL}/usr/bin/bc
  209      chmod 4755 ${INSTALL}/usr/bin/busybox
  210  
  211    mkdir -p ${INSTALL}/usr/sbin
  212      ln -sf /usr/bin/busybox ${INSTALL}/usr/sbin/blockdev
  213  
  214    mkdir -p ${INSTALL}/etc
  215      touch ${INSTALL}/etc/fstab
  216      ln -sf /proc/self/mounts ${INSTALL}/etc/mtab
  217  
  218    if find_file_path initramfs/platform_init; then
  219      cp ${FOUND_PATH} ${INSTALL}
  220      sed -e "s/@BOOT_LABEL@/${DISTRO_BOOTLABEL}/g" \
  221          -e "s/@DISK_LABEL@/${DISTRO_DISKLABEL}/g" \
  222          -i ${INSTALL}/platform_init
  223      chmod 755 ${INSTALL}/platform_init
  224    fi
  225  
  226    cp ${PKG_DIR}/scripts/functions ${INSTALL}
  227    cp ${PKG_DIR}/scripts/init ${INSTALL}
  228  
  229    if [ -e "${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/device.init" ]
  230    then
  231      cp ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/device.init ${INSTALL}
  232    else
  233      touch ${INSTALL}/device.init
  234    fi
  235    chmod 755 ${INSTALL}/device.init
  236  
  237    sed -e "s/@DISTRONAME@/${DISTRONAME}/g" \
  238        -e "s/@DEVICENAME@/${DEVICE}/g" \
  239        -e "s/@KERNEL_NAME@/${KERNEL_NAME}/g" \
  240        -i ${INSTALL}/init
  241    chmod 755 ${INSTALL}/init
  242  }
```

## File: sysutils/busybox/scripts/init (at 8ebaf8daad, 1383 lines)

```text
    1  #!/bin/sh
    2  
    3  # SPDX-License-Identifier: GPL-2.0-or-later
    4  # Copyright (C) 2010-2011 Roman Weber (roman@openelec.tv)
    5  # Copyright (C) 2012 Yann Cézard (eesprit@free.fr)
    6  # Copyright (C) 2009-2014 Stephan Raue (stephan@openelec.tv)
    7  # Copyright (C) 2016-2018 Team LibreELEC (https://libreelec.tv)
    8  # Copyright (C) 2018-present Team CoreELEC (https://coreelec.org)
    9  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
   10  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
   11  
   12  # create directories
   13  /usr/bin/busybox mkdir -p /dev
   14  /usr/bin/busybox mkdir -p /proc
   15  /usr/bin/busybox mkdir -p /sys
   16  /usr/bin/busybox mkdir -p /tmp
   17  /usr/bin/busybox mkdir -p /flash
   18  /usr/bin/busybox mkdir -p /sysroot
   19  /usr/bin/busybox mkdir -p /storage
   20  /usr/bin/busybox mkdir -p /run
   21  
   22  # temp mountpoint for updates
   23  /usr/bin/busybox mkdir -p /update
   24  
   25  # mount all needed special filesystems
   26  /usr/bin/busybox mount -t devtmpfs devtmpfs /dev
   27  /usr/bin/busybox mount -t proc proc /proc
   28  /usr/bin/busybox mount -t sysfs sysfs /sys
   29  # /run options have to match what systemd uses by default
   30  /usr/bin/busybox mount -t tmpfs -o mode=755,size=20%,nr_inodes=800k,nosuid,nodev,strictatime tmpfs /run
   31  
   32  # set needed variables
   33  MODULE_DIR=/usr/lib/modules
   34  
   35  UPDATE_ROOT=/storage/.update
   36  UPDATE_DIR="${UPDATE_ROOT}"
   37  
   38  UPDATE_KERNEL="@KERNEL_NAME@"
   39  UPDATE_SYSTEM="SYSTEM"
   40  IMAGE_KERNEL="@KERNEL_NAME@"
   41  IMAGE_SYSTEM="SYSTEM"
   42  
   43  BOOT_STEP="start"
   44  MD5_FAILED="0"
   45  RUN_FSCK="yes"
   46  RUN_FSCK_DISKS=""
   47  SYSLINUX_DEFAULT=""
   48  GRUB_DEFAULT=""
   49  
   50  NBD_DEVS="0"
   51  FLASH_FREE_MIN="5"
   52  
   53  LIVE="no"
   54  FORCE_RECOVERY="no"
   55  
   56  BREAK_TRIPPED="no"
   57  
   58  BIGFONT="1080"
   59  
   60  TEE_PID=""
   61  
   62  exec 1>/dev/console
   63  exec 2>/dev/null
   64  
   65  # common functions
   66  . /functions 2>/dev/null
   67  . /device.init 2>/dev/null
   68  
   69  # Get a serial number if present (eg. RPi) otherwise use MAC address from eth0
   70  MACHINE_UID="$(awk '/^Serial/{s='0000000' $3; print substr(s, length(s) - 7)}' /proc/cpuinfo 2>/dev/null)"
   71  [ -z "${MACHINE_UID}" ] && MACHINE_UID="$(cat /sys/class/net/eth0/address 2>/dev/null | tr -d :)"
   72  
   73  clear >/dev/console
   74  
   75  # script functions
   76  progress() {
   77    if test "${PROGRESS}" = "yes"; then
   78      echo "### $1 ###" >&2
   79    fi
   80  }
   81  
   82  debug_msg() {
   83    echo "$1" >&${SILENT_OUT}
   84  }
   85  
   86  debug_shell() {
   87    echo "### Starting debugging shell for boot step: ${BOOT_STEP}... type  exit  to quit ###"
   88    showcursor
   89    setsid cttyhack sh
   90  }
   91  
   92  error() {
   93    # Display fatal error message
   94    # $1:action which caused error, $2:message
   95    # Send debug_shell output to stderr, in case caller is redirecting/consuming stdout
   96    # Return exitcode=1 so that called may detect when an error has occurred
   97    echo "*** Error in ${BOOT_STEP}: $1: $2 ***" >&2
   98    debug_shell >&2
   99    return 1
  100  }
  101  
  102  break_after() {
  103    # Start debug shell after boot step $1, and all subsequent steps
  104    if [ ${BREAK_TRIPPED} == yes ]; then
  105      debug_shell
  106    else
  107      case ${BREAK} in
  108        all|*$1*)
  109          BREAK_TRIPPED=yes
  110          debug_shell
  111          ;;
  112      esac
  113    fi
  114  }
  115  
  116  # Mount handlers
  117  # All handlers take the following parameters:
  118  # $1:target, $2:mountpoint, $3:mount options, [$4:fs type]
  119  mount_common() {
  120    # Common mount handler, handles block devices and filesystem images
  121    MOUNT_OPTIONS="-o $3"
  122    [ -n "$4" ] && MOUNT_OPTIONS="-t $4 ${MOUNT_OPTIONS}"
  123  
  124    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  125      ERR_ENV=1
  126  
  127      mount ${MOUNT_OPTIONS} $1 $2 >&${SILENT_OUT} 2>&1
  128      [ "$?" -eq "0" ] && ERR_ENV=0 && break
  129  
  130      usleep 1000000
  131    done
  132    [ "${ERR_ENV}" -eq "0" ] && return 0
  133    echo "Unable to find $1, powering off and on should correct it." >/dev/console
  134    StartProgress countdown "Power off in 3s... " 3 "NOW"
  135    poweroff
  136  }
  137  
  138  get_iscsistart_options() {
  139    # Convert kernel commandline ISCSI= options to iscsistart options
  140    IFS_SAVE="${IFS}"
  141    IFS=,
  142  
  143    for arg in $1; do
  144      val="${arg#*=}"
  145      case "$arg" in
  146        iscsi_initiator=*)
  147          option="-i"
  148          ;;
  149        iscsi_target_name=*)
  150          option="-t"
  151          ;;
  152        iscsi_target_ip=*)
  153          option="-a"
  154          ;;
  155        iscsi_target_port=*)
  156          option="-p"
  157          ;;
  158        iscsi_target_group=*)
  159          option="-g"
  160          ;;
  161        iscsi_username=*)
  162          option="-u"
  163          ;;
  164        iscsi_password=*)
  165          option="-w"
  166          ;;
  167        iscsi_in_username=*)
  168          option="-U"
  169          ;;
  170        iscsi_in_password=*)
  171          option="-W"
  172          ;;
  173      esac
  174      echo "$option $val"
  175    done
  176  
  177    IFS="${IFS_SAVE}"
  178  }
  179  
  180  mount_iscsi() {
  181    # Mount iSCSI target
  182    ISCSI_DEV="${1##*,}"
  183    ISCSI_OPTIONS="${1%,*}"
  184  
  185    if [ ! -f "/usr/sbin/iscsistart" ]; then
  186      error "iscsistart" "iSCSI support not available"
  187    fi
  188  
  189    if [ "${ISCSI_OPTIONS}" = "auto" ]; then
  190      progress "Network configuration based on iBFT"
  191      /usr/sbin/iscsistart -N >&${SILENT_OUT} 2>&1 || error "iscsistart" "Unable to configure network"
  192      progress "iSCSI auto connect based on iBFT"
  193      /usr/sbin/iscsistart -b >&${SILENT_OUT} 2>&1 || error "iscsistart" "Unable to auto connect"
  194    else
  195      /usr/sbin/iscsistart $(get_iscsistart_options "${ISCSI_OPTIONS}") >&${SILENT_OUT} 2>&1 || error "iscsistart" "Unable to connect to ISCSI target"
  196    fi
  197  
  198    mount_common "${ISCSI_DEV}" "$2" "$3" "$4"
  199  }
  200  
  201  mount_nbd() {
  202  # Mount NBD device
  203    NBD_SERVER="${1%%:*}"
  204    NBD_PORT="${1#*:}"
  205    NBD_DEV="/dev/nbd${NBD_DEV}S"
  206  
  207    nbd-client ${NBD_SERVER} ${NBD_PORT} ${NBD_DEV} >&${SILENT_OUT} 2>&1 || error "nbd-client" "Could not connect to NBD server $1"
  208  
  209    mount_common "${NBD_DEV}" "$2" "$3" "$4"
  210  
  211    NBD_DEVS=$(( NBD_DEVS + 1 ))
  212  }
  213  
  214  mount_nfs() {
  215    # Mount NFS export
  216    NFS_EXPORT="${1%%,*}"
  217    NFS_OPTIONS="${1#*,}"
  218  
  219    [ "${NFS_OPTIONS}" = "$1" ] && NFS_OPTIONS=
  220  
  221    mount_common "${NFS_EXPORT}" "$2" "$3,nolock,rsize=32768,wsize=32768,${NFS_OPTIONS}" "nfs"
  222  }
  223  
  224  mount_ubifs() {
  225    mount_common "$1" "$2" "$3" "ubifs"
  226  }
  227  
  228  #  mount_folder "$boot" "/flash" "ro,noatime"
  229  # $1:[TYPE=]target, $2:mountpoint, $3:mount options, [$4:fs type]
  230  mount_folder() {
  231    local target="${1#*=}"
  232  
  233    mkdir -p /dev/bind_tmp
  234    mount_common "$target" "/dev/bind_tmp" "rw,noatime"
  235    mount_common "/dev/bind_tmp/${OSNAME}_$(basename $2)" "$2" "bind"
  236    umount /dev/bind_tmp &>/dev/null
  237  
  238    [ "$2" = "/flash" ] && mount -o remount,ro /flash
  239    [ -z "$(ls -A /dev/bind_tmp)" ] && rm -rf /dev/bind_tmp
  240  }
  241  
  242  mount_part() {
  243    # Mount a local or network filesystem
  244    # $1:[TYPE=]target, $2:mountpoint, $3:mount options, [$4:fs type]
  245    progress "mount filesystem $1 ..."
  246  
  247    MOUNT_TARGET="${1#*=}"
  248    case $1 in
  249      /dev/ubi*)
  250        MOUNT_CMD="mount_ubifs"
  251        MOUNT_TARGET="$1"
  252        RUN_FSCK="no"
  253        ;;
  254      LABEL=*|UUID=*|/*)
  255        MOUNT_CMD="mount_common"
  256        MOUNT_TARGET="$1"
  257        ;;
  258      ISCSI=*)
  259        MOUNT_CMD="mount_iscsi"
  260        ;;
  261      NBD=*)
  262        MOUNT_CMD="mount_nbd"
  263        ;;
  264      NFS=*)
  265        MOUNT_CMD="mount_nfs"
  266        ;;
  267      FOLDER=*)
  268        MOUNT_CMD="mount_folder"
  269        MOUNT_TARGET="$1"
  270        ;;
  271      *)
  272        error "mount_part" "Unknown filesystem $1"
  273        ;;
  274    esac
  275  
  276    # Substitute unique identifier if available or remove placeholder
  277    MOUNT_TARGET="${MOUNT_TARGET//@UID@/${MACHINE_UID}}"
  278  
  279    ${MOUNT_CMD} "${MOUNT_TARGET}" "$2" "$3" "$4"
  280  }
  281  
  282  mount_sysroot() {
  283    if [ "${SYSTEM_TORAM}" = "yes" ]; then
  284      cp /flash/${IMAGE_SYSTEM} /dev/${IMAGE_SYSTEM}
  285      mount_part "/dev/${IMAGE_SYSTEM}" "/sysroot" "ro,loop"
  286    else
  287      mount_part "/flash/${IMAGE_SYSTEM}" "/sysroot" "ro,loop"
  288    fi
  289  
  290    if [ -f /flash/post-sysroot.sh ]; then
  291      . /flash/post-sysroot.sh
  292    fi
  293  
  294  }
  295  
  296  # mount the specified SYSTEM file and output arch from /etc/os-release
  297  get_project_arch() {
  298    if [ -f ${1}/etc/os-release ]; then
  299      . ${1}/etc/os-release
  300      echo "${OS_ARCH}"
  301    fi
  302  }
  303  
  304  # mount the specified SYSTEM file and output HW device from /etc/os-release
  305  get_project_device() {
  306    if [ -f ${1}/etc/os-release ]; then
  307      . ${1}/etc/os-release
  308      echo "${HW_DEVICE}"
  309    fi
  310  }
  311  
  312  # mount the specified SYSTEM file and output version from /etc/os-release
  313  get_project_version() {
  314    if [ -f ${1}/etc/os-release ]; then
  315      . ${1}/etc/os-release
  316      echo "${VERSION}"
  317    fi
  318  }
  319  
  320  # If the project/arch of current matches the update, then it is considered compatible.
  321  # Otherwise, mount the update SYSTEM partition and, if canupdate.sh is available,
  322  # call the script to determine if the current update file can be applied on to the
  323  # current system - 0 means it is compatible, non-zero that it is not compatible.
  324  is_compatible() {
  325    local result=1
  326  
  327    if [ "${1}" = "${2}" ]; then
  328      result=0
  329    else
  330      if [ -f /update/usr/share/bootloader/canupdate.sh ]; then
  331        sh /update/usr/share/bootloader/canupdate.sh "${1}" "${2}" && result=0
  332      fi
  333    fi
  334  
  335    return ${result}
  336  }
  337  
  338  # determine if the new SYSTEM file is compatible with the current SYSTEM file
  339  check_is_compatible() {
  340    local update_filename="${1}"
  341    local old_project_arch new_project_arch old_project_device new_project_device
  342  
  343    old_project_arch="$(get_project_arch "/sysroot")" || return
  344    new_project_arch="$(get_project_arch "/update")" || return
  345    old_project_device="$(get_project_device "/sysroot")" || return
  346    new_project_device="$(get_project_device "/update")" || return
  347  
  348    # If old or new project/arch isn't available then could be very old (pre-/etc/os-release) build - have to trust it
  349    if [ -n "${old_project_arch}" -a -n "${new_project_arch}" ]; then
  350      # If the old project/arch is not compatible with the new project/arch then abort...
  351      if ! is_compatible "${old_project_arch}" "${new_project_arch}"; then
  352        echo ""
  353        echo "ERROR: $(basename "${update_filename}") is not compatible with ${old_project_arch} hardware - update cancelled."
  354        echo ""
  355        echo "Current system: ${old_project_arch}"
  356        echo "Update  system: ${new_project_arch}"
  357        echo ""
  358        echo "Create ${UPDATE_ROOT}/.nocompat to disable compatibility checks and risk a non-booting system."
  359        echo ""
  360        return 1
  361      fi
  362      # If the old project/device is not compatible with the new project/device then abort...
  363      if ! is_compatible "${old_project_device}" "${new_project_device}"; then
  364        echo ""
  365        echo "ERROR: $(basename "${update_filename}") is not compatible with ${old_project_device} hardware - update cancelled."
  366        echo ""
  367        echo "Current system: ${old_project_device}"
  368        echo "Update  system: ${new_project_device}"
  369        echo ""
  370        echo "Create ${UPDATE_ROOT}/.nocompat to disable compatibility checks and risk a non-booting system."
  371        echo ""
  372        return 1
  373      fi
  374    fi
  375  
  376    return 0
  377  }
  378  
  379  display_versions() {
  380    local old_project_version new_project_version
  381  
  382    old_project_version="$(get_project_version "/sysroot")" || return
  383    new_project_version="$(get_project_version "/update")" || return
  384  
  385    if [ -n "${old_project_version}" -a -n "${new_project_version}" ]; then
  386      echo ""
  387      echo "Updating from ${old_project_version} to ${new_project_version}"
  388      echo ""
  389    fi
  390  
  391    return 0
  392  }
  393  
  394  update_file() {
  395    if [ -f "${UPDATE_DIR}/$2" -a -f "$3" ]; then
  396      mount -o remount,rw /flash
  397  
  398      StartProgress percent "Updating $1... " "$3" $(stat -Lt "${UPDATE_DIR}/$2" | awk '{print $2}')
  399        # use dd here with conv=fsync so that all writes are non-buffered
  400        # ensuring accurate progress - take the sync hit during the
  401        # transfer, rather than when flushing file buffers after the progress
  402        # meter declares the transfer already complete
  403        dd if=${UPDATE_DIR}/$2 of=$3 bs=1M conv=fsync 2>/dev/null
  404  
  405        StopProgress
  406  
  407      # loopback file needs writable /flash all the time
  408      if [ "${disk%%=*}" != "FILE" ]; then
  409        mount -o remount,ro /flash
  410      fi
  411      sync
  412    fi
  413  }
  414  
  415  update_partition() {
  416    local result
  417  
  418    if [ -f "${UPDATE_DIR}/$2" -a -b "$3" ]; then
  419      StartProgress spinner "Updating $1... "
  420        result="$(dd if="${UPDATE_DIR}/$2" of="$3" 2>&1)"
  421        StopProgress "done"
  422        sync
  423      echo "${result}"
  424    fi
  425  }
  426  
  427  update_bootloader() {
  428    local result
  429  
  430    export BOOT_ROOT="/flash"
  431    export SYSTEM_ROOT="/update"
  432    if [ -f ${SYSTEM_ROOT}/usr/share/bootloader/update.sh ]; then
  433      echo ""
  434      echo "Updating Boot Files... "
  435      sh ${SYSTEM_ROOT}/usr/share/bootloader/update.sh
  436      sync
  437      echo "Boot Files Updated."
  438      echo ""
  439    fi
  440  }
  441  
  442  load_modules() {
  443    progress "Loading kernel modules"
  444  
  445    [ ! -f "/etc/modules" ] && return
  446    for module in $(cat /etc/modules); do
  447      progress "Loading kernel module $module"
  448      insmod "${MODULE_DIR}/$module.ko" || progress "... Failed to load kernel module $module, skipping"
  449    done
  450  }
  451  
  452  set_consolefont() {
  453    local hres
  454  
  455    progress "Set console font"
  456    if [ -e /dev/fb0 ]; then
  457      hres="$(fbset 2>/dev/null | awk '/geometry/ { print $2 }')"
  458      if [ "${hres}" -gt "0" ] && [ "${hres}" -le "480" ]
  459      then
  460        setfont -C /dev/console spleen-5x8.psfu
  461      elif [ "${hres}" -gt "480" ] && [ "${hres}" -le "720" ]
  462      then
  463        setfont -C /dev/console spleen-6x12.psfu
  464      elif [ "${hres}" -gt "720" ] && [ "${hres}" -lt "1080" ]
  465      then
  466        setfont -C /dev/console spleen-8x16.psfu
  467      else
  468        setfont -C /dev/console spleen-12x24.psfu
  469      fi
  470    fi
  471  }
  472  
  473  hdmi_con() {
  474    if [ -f "/sys/class/extcon/hdmi/state" ]
  475    then
  476      HDMI="$(cat /sys/class/extcon/hdmi/state)"
  477      if [ "${HDMI}" = "HDMI=1" ]
  478      then
  479        if [ -f "/sys/devices/virtual/graphics/fbcon/rotate" ]
  480        then
  481          echo 0 >/sys/devices/virtual/graphics/fbcon/rotate
  482        fi
  483      fi
  484    fi
  485  }
  486  
  487  load_splash() {
  488    /usr/bin/rocknix-splash
  489  
  490    echo -en "\033[1000H\033[2K$(cat /sysroot/etc/issue)\n\n" >/dev/console
  491    if [ -f "/storage/.configured" ]
  492    then
  493      echo -ne "\033[1000H\033[2K==> Loading, please wait..." >/dev/console
  494    else
  495      echo -ne "\033[1000H\033[2K==> Initializing, please wait..." >/dev/console
  496    fi
  497  }
  498  
  499  do_reboot() {
  500    echo "System reboots now..."
  501  
  502    # stop output redirection
  503    [ -n "${TEE_PID}" ] && kill ${TEE_PID} &>/dev/null
  504    if [ -s /dev/init.log ]; then
  505      mv /dev/init.log /storage/init-previous.log
  506    fi
  507  
  508    # syncing filesystem
  509    sync
  510  
  511    # unmount filesystems
  512    if /usr/bin/busybox mountpoint -q /flash ; then
  513      /usr/bin/busybox umount /flash &>/dev/null
  514    fi
  515  
  516    if /usr/bin/busybox mountpoint -q /storage ; then
  517      /usr/bin/busybox umount /storage &>/dev/null
  518    fi
  519  
  520    usleep 2000000
  521    /usr/bin/busybox reboot
  522  }
  523  
  524  
  525  is_key_pressed() {
  526    # Here we do not have /dev/input/by-path/ yet, so iterate over all event devices
  527    for evdev in /dev/input/event*; do
  528      evtest --query "$evdev" EV_KEY $1
  529      if [ $? -eq 10 ]; then return 0; fi
  530    done
  531    return 1
  532  }
  533  
  534  KEY_VOLUMEDOWN=114
  535  KEY_VOLUMEUP=115
  536  
  537  recovery_mode() {
  538    # Silent keycode mode to read Vol buttons and not echo garbage
  539    stty -echo
  540  
  541    # Do recovery only if it is requested in cmdline or Vol- button is pressed
  542    if [ "${FORCE_RECOVERY}" != "yes" ] && ! is_key_pressed $KEY_VOLUMEDOWN; then
  543      # Return to normal boot, roll back tty changes
  544      stty echo
  545      return
  546    fi
  547  
  548    StartProgress spinner "Exporting storage as USB MSC... "
  549  
  550    sleep 1
  551    # If there is a role switch, switch to device mode (applies to RK3326 which has a single USB port)
  552    for sw in /sys/class/udc/*/device/usb_role/*/role; do
  553      echo device > $sw
  554    done
  555    # Let everything settle
  556    sleep 1
  557  
  558    # USB gadget boilerplate
  559    mount configfs -t configfs /sys/kernel/config
  560    g=/sys/kernel/config/usb_gadget/msc
  561    mkdir ${g}
  562    echo "0x0200" > ${g}/bcdUSB
  563    echo "8" > ${g}/bDeviceClass # mass storage device class
  564    echo "0x1d6b" > ${g}/idVendor
  565    echo "0x0104" > ${g}/idProduct
  566    mkdir ${g}/strings/0x409
  567    echo "00000000" > ${g}/strings/0x409/serialnumber
  568    echo "ROCKNIX" > ${g}/strings/0x409/manufacturer
  569    echo "RECOVERY" > ${g}/strings/0x409/product
  570    mkdir ${g}/configs/c.1
  571    echo 120 > ${g}/configs/c.1/MaxPower
  572  
  573    # Configure mass storage function
  574    msf=${g}/functions/mass_storage.0
  575    mkdir ${msf}
  576    # Every found mmcblk device gets its lun
  577    I=0
  578    for m in /dev/mmcblk?; do
  579      mkdir -p ${g}/functions/mass_storage.0/lun.${I}
  580      echo ${m} > ${g}/functions/mass_storage.0/lun.${I}/file
  581      ms=/sys/block/${m##*/}/device
  582      cat $ms/name $ms/serial $ms/date | tr '\n' ' ' > /tmp/msc_lun_string
  583      cat /tmp/msc_lun_string > ${g}/functions/mass_storage.0/lun.${I}/inquiry_string
  584      I=$((I+1))
  585    done
  586  
  587    # activate mass storage gadget
  588    ln -s ${g}/functions/mass_storage.0 ${g}/configs/c.1/
  589    ls /sys/class/udc/ | head -n 1 > ${g}/UDC
  590  
  591    StopProgress "done"
  592    echo "Exported devices:"
  593    cat ${g}/functions/mass_storage.0/lun.*/inquiry_string
  594    echo
  595    echo "Remember to properly eject partitions to prevent data corruption!"
  596    echo
  597  
  598    StartProgress spinner "Press VOLUMEUP to reboot "
  599    while ! is_key_pressed $KEY_VOLUMEUP; do
  600      read -t 0.1 discard # Faster polling than integer sleep
  601    done
  602  
  603    sync
  604    StopProgress "rebooting"
  605    sleep 1
  606    /usr/bin/busybox reboot
  607  }
  608  
  609  
  610  force_fsck() {
  611    echo "Filesystem corruption has been detected!"
  612    echo "To prevent an automatic repair attempt continuing,"
  613    echo "press any key or power off your system within the next 120 seconds"
  614    echo ""
  615    read -t120 -n1
  616    # The exit status is 0 if input is available
  617    # The exit status is greater than 128 if the timeout is exceeded
  618    if [ $? -ne 0 -o $? -gt 128 ]; then
  619      echo "Repairing filesystem..."
  620      echo ""
  621      /usr/sbin/fsck -T -M -y ${RUN_FSCK_DISKS}
  622      FSCK_RET=$?
  623      if [ $(( ${FSCK_RET} & 8 )) -eq 8 ]; then
  624        # fubar
  625        echo "Forced fsck failed. Your system is broken beyond repair"
  626        echo "Please re-install @DISTRONAME@"
  627        echo ""
  628        echo "Press enter to shutdown now"
  629        echo ""
  630        read fubar
  631        poweroff
  632      fi
  633      do_reboot
  634    else
  635      echo "Shutting down..."
  636      sleep 5
  637      sync
  638      poweroff
  639    fi
  640  }
  641  
  642  check_disks() {
  643    if [ "${RUN_FSCK}" = "yes" -a -n "${RUN_FSCK_DISKS}" ]; then
  644      progress "Checking disk(s): ${RUN_FSCK_DISKS}"
  645      echo "Checking disk(s): ${RUN_FSCK_DISKS}" >/dev/kmsg
  646      for i in 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0; do
  647        /usr/sbin/fsck -T -M -p -a ${RUN_FSCK_DISKS} >/dev/fsck.latest 2>&1
  648        FSCK_RET=$?
  649        cat /dev/fsck.latest >>/dev/fsck.log
  650  
  651        # FSCK_RET is the bit-wise OR of the exit codes for each filesystem that is checked.
  652        if [ ${FSCK_RET} -ge 16 ]; then
  653          progress "General error, continuing..."
  654          break
  655        elif [ $(( ${FSCK_RET} & 8 )) -eq 8 ]; then
  656          # device not found
  657          if [ $i -eq 0 ]; then
  658            progress "Device not found, continuing..."
  659          else
  660            usleep 500000
  661          fi
  662        elif [ $(( ${FSCK_RET} & 4 )) -eq 4 ]; then
  663          # errors left
  664          force_fsck
  665        elif [ $(( ${FSCK_RET} & 2 )) -eq 2 ]; then
  666          # reboot needed
  667          echo "Filesystem repaired, reboot needed..."
  668          do_reboot
  669        elif [ $(( ${FSCK_RET} & 1 )) -eq 1 ]; then
  670          # filesystem errors corrected
  671          progress "Filesystem errors corrected , continuing..."
  672          break
  673        elif [ ${FSCK_RET} -eq 0 ]; then
  674          # no errors found
  675          progress "No filesystem errors found, continuing..."
  676          break
  677        fi
  678      done
  679      while read line; do
  680        [ -n "$line" ] && echo "fsck: ${line::160}" >/dev/kmsg
  681      done </dev/fsck.latest
  682      rm -f /dev/fsck.latest
  683    fi
  684  }
  685  
  686  wakeonlan() {
  687    if [ "${STORAGE_NETBOOT}" = "yes" ]; then
  688      wol_ip=${disk%:*}
  689      wol_ip=${wol_ip#*=}
  690    elif [ "${FLASH_NETBOOT}" = "yes" ]; then
  691      wol_ip=${boot%:*}
  692      wol_ip=${wol_ip#*=}
  693    else
  694      return 0
  695    fi
  696  
  697    if [ -n "$wol_ip" -a -n "$wol_mac" -a -n "$wol_wait" ]; then
  698      progress "Sending Magic Packet (WOL) if needed"
  699  
  700      if ! ping -q -c 2 "$wol_ip" &>/dev/null; then
  701        ether-wake "$wol_mac"
  702        StartProgress countdown "WOL magic packet sent to $wol_ip, waiting $wol_wait seconds... " $wol_wait "done"
  703      fi
  704    fi
  705  }
  706  
  707  mount_flash() {
  708    progress "Mounting flash"
  709  
  710    wakeonlan
  711  
  712    mount_part "$boot" "/flash" "ro,noatime"
  713  
  714    if [ -f /flash/post-flash.sh ]; then
  715      . /flash/post-flash.sh
  716    fi
  717  }
  718  
  719  cleanup_flash() {
  720    progress "Cleaning up flash (if required)"
  721  
  722    if [ -f /flash/pieeprom.bin -o -f /flash/pieeprom.upd -o -f /flash/vl805.bin ]; then
  723      mount -o remount,rw /flash
  724  
  725      rm -f /flash/pieeprom.bin /flash/pieeprom.upd /flash/pieeprom.sig
  726      rm -f /flash/vl805.bin /flash/vl805.sig
  727      rm -f /flash/recovery.bin /flash/recovery.[0-9][0-9][0-9] /flash/RECOVERY.[0-9][0-9][0-9]
  728  
  729      mount -o remount,ro /flash
  730    fi
  731  }
  732  
  733  mount_storage() {
  734    progress "Mounting storage"
  735  
  736    if [ "${LIVE}" = "yes" ]; then
  737      # mount tmpfs and exit early. disk=xx is not allowed in live mode
  738      mount -t tmpfs none /storage
  739      return
  740    fi
  741  
  742    wakeonlan
  743  
  744    if [ -n "$disk" ]; then
  745      if [ -n "${OVERLAY}" ]; then
  746        OVERLAY_DIR=$(cat /sys/class/net/eth0/address | tr -d :)
  747  
  748        mount_part "$disk" "/storage" "rw,noatime"
  749        mkdir -p /storage/${OVERLAY_DIR}
  750        umount /storage &>/dev/null
  751  
  752        # split $disk into $target,$options so we can append ${OVERLAY_DIR}
  753        options="${disk#*,}"
  754        target="${disk%%,*}"
  755        if [ "$options" = "$disk" ]; then
  756          disk="$target/${OVERLAY_DIR}"
  757        else
  758          disk="$target/${OVERLAY_DIR},$options"
  759        fi
  760      fi
  761  
  762      if [ -f /flash/mount-storage.sh ]; then
  763        . /flash/mount-storage.sh
  764      else
  765        mount_part "$disk" "/storage" "rw,noatime"
  766      fi
  767    else
  768      # /storage should always be writable
  769      mount -t tmpfs none /storage
  770    fi
  771  }
  772  
  773  # Make last bootloader label (installer, live, run etc.) as the new default
  774  update_bootmenu() {
  775    local crnt_default
  776  
  777    if [ -n "${SYSLINUX_DEFAULT}" -a -f /flash/syslinux.cfg ]; then
  778      if grep -q "^LABEL ${SYSLINUX_DEFAULT}\$" /flash/syslinux.cfg 2>/dev/null; then
  779        crnt_default="$(awk '/^DEFAULT/ {print $2}' /flash/syslinux.cfg)"
  780        if [ ! "$crnt_default" = "${SYSLINUX_DEFAULT}" ]; then
  781          progress "Updating /flash/syslinux.cfg [$crnt_default -> ${SYSLINUX_DEFAULT}]"
  782  
  783          mount -o remount,rw /flash
  784          sed -e "s/^SAY Wait for .* mode/SAY Wait for ${SYSLINUX_DEFAULT} mode/" -i /flash/syslinux.cfg
  785          sed -e "s/^DEFAULT .*/DEFAULT ${SYSLINUX_DEFAULT}/" -i /flash/syslinux.cfg
  786          rm -f /flash/EFI/BOOT/syslinux.cfg
  787          mount -o remount,ro /flash
  788        fi
  789      fi
  790    fi
  791  
  792    if [ -n "${GRUB_DEFAULT}" -a -f /flash/EFI/BOOT/grub.cfg ]; then
  793      if grep -q "^menuentry \"${GRUB_DEFAULT}\"" /flash/EFI/BOOT/grub.cfg 2>/dev/null; then
  794        crnt_default="$(awk '/^set default/ {print substr($2,9,19)}' /flash/EFI/BOOT/grub.cfg)"
  795        if [ ! "$crnt_default" = "\"${GRUB_DEFAULT}\"" ]; then
  796          progress "Updating /flash/EFI/BOOT/grub.cfg [$crnt_default -> \"${GRUB_DEFAULT}\"]"
  797  
  798          mount -o remount,rw /flash
  799          sed -e "s/^set default=.*/set default=\"${GRUB_DEFAULT}\"/" -i /flash/EFI/BOOT/grub.cfg
  800          rm -f /flash/grub.cfg
  801          mount -o remount,ro /flash
  802        fi
  803      fi
  804    fi
  805  }
  806  
  807  check_out_of_space() {
  808    if [ "$(df /storage | awk '/[0-9]%/{print $4}')" -eq "0" ]; then
  809      echo ""
  810      echo "The $1 is corrupt, or there is not enough"
  811      echo "free space on /storage to complete the update!"
  812      echo ""
  813      echo "Please free up space on your /storage partition"
  814      echo "by deleting unecessary files, then try again."
  815      echo ""
  816      return 0
  817    else
  818      echo ""
  819      echo "The $1 is corrupt/invalid!"
  820      echo ""
  821      return 1
  822    fi
  823  }
  824  
  825  do_cleanup() {
  826    StartProgress spinner "Cleaning up... "
  827  
  828    # Busybox losetup doesn't have -D option
  829    for loop in $(losetup -a | cut -d: -f1); do
  830      losetup -d $loop
  831    done
  832  
  833    # update is mounted last on top of mnt and avfs, so it should be unmounted first
  834    if mountpoint -q /update; then
  835      umount /update &>/dev/null
  836    fi
  837  
  838    # mnt is a partition of .img loop, it uses avfs
  839    if [ -d ${UPDATE_ROOT}/.tmp/mnt ]; then
  840      if mountpoint -q ${UPDATE_ROOT}/.tmp/mnt ; then
  841        # busybox umount deletes loop device automatically
  842        umount ${UPDATE_ROOT}/.tmp/mnt &>/dev/null
  843      fi
  844    fi
  845  
  846    # among update stuff, avfs is mounted first, so, is unmounted last
  847    if [ -d ${UPDATE_ROOT}/.tmp/avfs ]; then
  848      if mountpoint -q ${UPDATE_ROOT}/.tmp/avfs ; then
  849        umount ${UPDATE_ROOT}/.tmp/avfs &>/dev/null
  850      fi
  851    fi
  852  
  853    rm -f "${UPDATE_TAR}" &>/dev/null
  854    rm -f "${UPDATE_IMG_GZ}" &>/dev/null
  855    rm -f "${UPDATE_IMG}" &>/dev/null
  856  
  857    rm -rf ${UPDATE_ROOT}/.[0-9a-zA-Z]* &>/dev/null
  858    rm -rf ${UPDATE_ROOT}/* &>/dev/null
  859  
  860    # All previous unmounts were needed to safely unmount storage partition
  861    if mountpoint -q /storage; then
  862      umount /storage &>/dev/null
  863    fi
  864  
  865    sync
  866  
  867    StopProgress "done"
  868  }
  869  
  870  check_update() {
  871    progress "Checking for updates"
  872    UPDATE_TAR=$(ls -1 "${UPDATE_DIR}"/*.tar 2>/dev/null | head -n 1)
  873    UPDATE_IMG_GZ=$(ls -1 "${UPDATE_DIR}"/*.img.gz 2>/dev/null | head -n 1)
  874    UPDATE_IMG=$(ls -1 "${UPDATE_DIR}"/*.img 2>/dev/null | head -n 1)
  875  
  876    if ! [ -f "${UPDATE_DIR}/${UPDATE_KERNEL}" -a -f "${UPDATE_DIR}/${UPDATE_SYSTEM}" ] &&
  877       ! [ -f "${UPDATE_TAR}" -o -f "${UPDATE_IMG_GZ}" -o -f "${UPDATE_IMG}" ]; then
  878      return 0
  879    fi
  880  
  881    hdmi_con
  882  
  883    echo "${UPDATE_TAR} ${UPDATE_IMG} ${UPDATE_IMG_GZ}" 2>&1 | grep @DISTRONAME@ 2>&1 >/dev/null
  884    if [ "$?" -ne "0" ]
  885    then
  886      echo "Unsupported operating system update.  Please only use @DISTRONAME@ update packages with this distribution."
  887      do_cleanup
  888      StartProgress countdown "Reboot in 5s... " 5 "now"
  889      reboot
  890    fi
  891  
  892    if [ "${UPDATE_DISABLED}" = "yes" ]; then
  893      echo "Updating is not supported on netboot"
  894      do_cleanup
  895      StartProgress countdown "Normal startup in 5s... " 5 "NOW"
  896      return 0
  897    fi
  898  
  899    if [ -d ${UPDATE_DIR}/.tmp ]; then
  900      # This isn't really a failed update, it's just a failure to clean up after updating.
  901      #echo "Failed update detected - performing recovery."
  902      #echo ""
  903      do_cleanup
  904      StartProgress countdown "Reboot in 5... " 5 "NOW"
  905      sync
  906      reboot
  907      #return 0
  908    fi
  909  
  910    mkdir -p ${UPDATE_DIR}/.tmp &>/dev/null
  911    mkdir -p ${UPDATE_DIR}/.tmp/avfs &>/dev/null
  912    sync
  913  
  914    clear >/dev/console
  915    echo "UPDATE IN PROGRESS"
  916    echo ""
  917    echo "Please do not reboot or turn off your device!"
  918    echo ""
  919  
  920    if [ -f "${UPDATE_TAR}" ]; then
  921      TARRESULT="0"
  922  
  923      echo "Found new .tar archive"
  924      UPDATE_FILENAME="${UPDATE_TAR}"
  925      StartProgress spinner "AVFS mounting archive... "
  926      /usr/bin/avfsd -o modules=subdir -o subdir="${UPDATE_TAR}#" ${UPDATE_DIR}/.tmp/avfs 2>/tmp/tarresult.txt
  927      # AVFS returns success (0) even when fuse kernel module is not available, so we need extra check
  928      if ls -d ${UPDATE_DIR}/.tmp/avfs/*/target 1>/dev/null 2>>/tmp/tarresult.txt; then
  929        # avfs mount succeeded
  930        UPDATE_DIR=$(ls -d -1 "${UPDATE_DIR}"/.tmp/avfs/*/target 2>/dev/null | head -n 1)
  931      else
  932        StopProgress "FAILED"
  933        cat /tmp/tarresult.txt
  934        # Fallback to extraction
  935        StartProgress spinner "Extracting contents of archive... "
  936        tar -xf "${UPDATE_TAR}" -C ${UPDATE_DIR}/.tmp 1>/dev/null 2>/tmp/tarresult.txt || TARRESULT="1"
  937        UPDATE_DIR=$(ls -d -1 "${UPDATE_DIR}"/.tmp/*/target 2>/dev/null | head -n 1)
  938      fi
  939  
  940      if [ "${TARRESULT}" -eq "0" ]; then
  941        StopProgress "done"
  942      else
  943        StopProgress "FAILED"
  944  
  945        echo "Failed to extract contents of archive file!"
  946        echo "tar result: '$(cat /tmp/tarresult.txt)'"
  947  
  948        check_out_of_space "archive"
  949  
  950        do_cleanup
  951        StartProgress countdown "Reboot in 5... " 5 "NOW"
  952        sync
  953        reboot
  954      fi
  955    elif [ -f "${UPDATE_IMG_GZ}" -o -f "${UPDATE_IMG}" ]; then
  956      LOOP=$(losetup -f)
  957  
  958      if [ -f "${UPDATE_IMG_GZ}" ]; then
  959        echo "Found new compressed image file"
  960        GZRESULT="0"
  961        UPDATE_FILENAME="${UPDATE_IMG_GZ}"
  962        StartProgress spinner "AVFS mounting image file... "
  963        GZ_BASENAME=$(basename "${UPDATE_IMG_GZ}")
  964        /usr/bin/avfsd -o modules=subdir -o subdir=${UPDATE_DIR} ${UPDATE_DIR}/.tmp/avfs 2>/tmp/gzresult.txt
  965        AVFS_IMG_FILE=${UPDATE_DIR}/.tmp/avfs/"${GZ_BASENAME}#"
  966        # AVFS returns success (0) even when fuse kernel module is not available, so we need extra check
  967        if losetup -P ${LOOP} ${AVFS_IMG_FILE}; then
  968          StopProgress "OK"
  969        else
  970          StopProgress "FAILED"
  971          cat /tmp/gzresult.txt
  972          # Fallback to decompressing the image
  973          IMG_FILE="${UPDATE_DIR}/.tmp/update.img"
  974          StartProgress spinner "Decompressing image file... "
  975          gunzip -d -c "${UPDATE_IMG_GZ}" 1>${IMG_FILE} 2>/tmp/gzresult.txt || GZRESULT="1"
  976          sync
  977          if [ "${GZRESULT}" -eq "0" ]; then
  978            StopProgress "OK"
  979            losetup -P ${LOOP} ${IMG_FILE}
  980          else
  981            StopProgress "FAILED"
  982          fi
  983        fi
  984  
  985        if [ "${GZRESULT}" -eq "1" ]; then
  986          echo "Failed to decompress image file!"
  987          echo "gunzip result: '$(cat /tmp/gzresult.txt)'"
  988  
  989          check_out_of_space "compressed image"
  990  
  991          do_cleanup
  992          StartProgress countdown "Reboot in 5... " 5 "NOW"
  993          sync
  994          reboot
  995        fi
  996      else
  997        echo "Found new image file"
  998        UPDATE_FILENAME="${UPDATE_IMG}"
  999        losetup -P ${LOOP} "${UPDATE_IMG}"
 1000      fi
 1001  
 1002      echo "Mounting system partition..."
 1003      mkdir -p ${UPDATE_DIR}/.tmp/mnt &>/dev/null
 1004      mount -o ro,loop ${LOOP}p1 ${UPDATE_DIR}/.tmp/mnt
 1005  
 1006      # don't make temporary files but instead copy
 1007      # directly from mountpoint to /flash
 1008      UPDATE_DIR=${UPDATE_ROOT}/.tmp/mnt
 1009      UPDATE_KERNEL="@KERNEL_NAME@"
 1010    else
 1011      UPDATE_FILENAME="${UPDATE_DIR}/${UPDATE_SYSTEM}"
 1012    fi
 1013  
 1014    sync
 1015  
 1016    if [ ! -b "/${IMAGE_KERNEL}" -a ! -f "/flash/${IMAGE_KERNEL}" ] || [ ! -f "/flash/${IMAGE_SYSTEM}" ]; then
 1017      echo "Missing (target) ${IMAGE_KERNEL} or ${IMAGE_SYSTEM}!"
 1018      do_cleanup
 1019      StartProgress countdown "Normal startup in 30s... " 30 "NOW"
 1020      return 0
 1021    fi
 1022  
 1023    # update parts may be symlinks, so check just for existence
 1024    if [ ! -e "${UPDATE_DIR}/${UPDATE_KERNEL}" -o ! -e "${UPDATE_DIR}/${UPDATE_SYSTEM}" ]; then
 1025      echo "Missing (source) ${UPDATE_KERNEL} or ${UPDATE_SYSTEM}!"
 1026      do_cleanup
 1027      StartProgress countdown "Normal startup in 30s... " 30 "NOW"
 1028      return 0
 1029    fi
 1030  
 1031    # check md5 sums if .nocheck doesn't exist
 1032    if [ ! -f "${UPDATE_ROOT}/.nocheck" ]; then
 1033      if [ -f "${UPDATE_DIR}/${UPDATE_KERNEL}.md5" -a -f "${UPDATE_DIR}/${UPDATE_SYSTEM}.md5" ]; then
 1034        # *.md5 size-check
 1035        if [ ! -s "${UPDATE_DIR}/${UPDATE_KERNEL}.md5" -o ! -s "${UPDATE_DIR}/${UPDATE_SYSTEM}.md5" ]; then
 1036          echo "Zero-sized .md5 file!"
 1037          MD5_FAILED="1"
 1038        else
 1039          sed "s#target/KERNEL#${UPDATE_DIR}/${UPDATE_KERNEL}#g" "${UPDATE_DIR}/${UPDATE_KERNEL}.md5" >"${UPDATE_ROOT}/${UPDATE_KERNEL}.check.md5"
 1040          sed "s#target#${UPDATE_DIR}#g" "${UPDATE_DIR}/${UPDATE_SYSTEM}.md5" >"${UPDATE_ROOT}/${UPDATE_SYSTEM}.check.md5"
 1041  
 1042          StartProgress spinner "Checking ${UPDATE_KERNEL}.md5... "
 1043            if md5sum -sc "${UPDATE_ROOT}/${UPDATE_KERNEL}.check.md5"; then
 1044              StopProgress "OK"
 1045            else
 1046              StopProgress "FAILED"
 1047              MD5_FAILED="1"
 1048            fi
 1049  
 1050          StartProgress spinner "Checking ${UPDATE_SYSTEM}.md5... "
 1051            if md5sum -sc "${UPDATE_ROOT}/${UPDATE_SYSTEM}.check.md5"; then
 1052              StopProgress "OK"
 1053            else
 1054              StopProgress "FAILED"
 1055              MD5_FAILED="1"
 1056            fi
 1057        fi
 1058      else
 1059        echo "Missing ${UPDATE_KERNEL}.md5 or ${UPDATE_SYSTEM}.md5!"
 1060        MD5_FAILED="1"
 1061      fi
 1062  
 1063      if [ "${MD5_FAILED}" -eq "1" ]; then
 1064        echo "md5 check failed!"
 1065        do_cleanup
 1066        StartProgress countdown "Normal startup in 30s... " 30 "NOW"
 1067        return 0
 1068      fi
 1069    fi
 1070  
 1071    mount_part "${UPDATE_DIR}/${UPDATE_SYSTEM}" "/update" "ro,loop"
 1072  
 1073    # Verify that the new update is compatible with the current system - this should avoid creating
 1074    # non-booting systems after (for example) an RPi tar is incorrectly applied to an RPi2 system.
 1075    if [ ! -f "${UPDATE_ROOT}/.nocompat" ]; then
 1076      if ! check_is_compatible "${UPDATE_FILENAME}"; then
 1077        do_cleanup
 1078        StartProgress countdown "Normal startup in 60s... " 60 "NOW"
 1079        return 0
 1080      fi
 1081    fi
 1082  
 1083    # get sizes
 1084    FLASH_FREE=$(df /flash/ | awk '/[0-9]%/{print $4}')
 1085    FLASH_FREE=$(( ${FLASH_FREE} * 1024 ))
 1086  
 1087    # Disregard kernel size if it's a a block device
 1088    if [ ! -b "/${IMAGE_KERNEL}" ]; then
 1089      OLD_KERNEL=$(stat -t "/flash/${IMAGE_KERNEL}" | awk '{print $2}')
 1090    else
 1091      OLD_KERNEL="0"
 1092    fi
 1093  
 1094    OLD_SYSTEM=$(stat -t "/flash/${IMAGE_SYSTEM}" | awk '{print $2}')
 1095    NEW_KERNEL=$(stat -Lt "${UPDATE_DIR}/${UPDATE_KERNEL}" | awk '{print $2}')
 1096    NEW_SYSTEM=$(stat -Lt "${UPDATE_DIR}/${UPDATE_SYSTEM}" | awk '{print $2}')
 1097  
 1098    # old KERNEL+SYSTEM+free space - new KERNEL+SYSTEM must be higher than 5MB
 1099    # at least 5MB free after update
 1100  
 1101    TMP_SIZE=$((OLD_KERNEL + OLD_SYSTEM + FLASH_FREE - NEW_KERNEL - NEW_SYSTEM))
 1102    FLASH_FREE_MIN=$((FLASH_FREE_MIN * 1024 * 1024))
 1103  
 1104    if [ ${TMP_SIZE} -ge ${FLASH_FREE_MIN} ]; then
 1105      echo "Checking size: OK"
 1106    else
 1107      echo "Checking size: FAILED"
 1108      echo ""
 1109      echo "Your System (FAT) partition is too small for this update,"
 1110      echo "and there is not enough space for the update to be installed!"
 1111      echo ""
 1112      echo "You must re-install your system using the disk image of a"
 1113      echo "current release, or you must re-size your existing partitions"
 1114      echo "so that the System (FAT) partition is at least 512MB in size."
 1115      echo ""
 1116      do_cleanup
 1117      StartProgress countdown "Normal startup in 60s... " 60 "NOW"
 1118      return 0
 1119    fi
 1120  
 1121    # all ok, update
 1122    display_versions
 1123    if [ -b "/${IMAGE_KERNEL}" ]; then
 1124      update_partition "Kernel" "${UPDATE_KERNEL}" "/${IMAGE_KERNEL}"
 1125    else
 1126      update_file "Kernel" "${UPDATE_KERNEL}" "/flash/${IMAGE_KERNEL}"
 1127    fi
 1128    umount /sysroot &>/dev/null
 1129    update_file "System" "${UPDATE_SYSTEM}" "/flash/${IMAGE_SYSTEM}"
 1130    update_bootloader
 1131    echo "UPDATE" >/storage/.boot.hint
 1132    sync
 1133    StartProgress countdown "Update complete. Reboot in 5s... " 5 "NOW"
 1134    do_cleanup
 1135    sync
 1136    do_reboot
 1137  }
 1138  
 1139  prepare_sysroot() {
 1140    progress "Preparing system"
 1141  
 1142    mount --move /flash /sysroot/flash
 1143    mount --move /storage /sysroot/storage
 1144  
 1145    if [ ! -d "/sysroot/usr/lib/kernel-overlays/base/lib/modules/$(uname -r)/" -a -f "/sysroot/usr/lib/systemd/systemd" ]; then
 1146      echo ""
 1147      echo "NEVER TOUCH boot= in syslinux.conf / cmdline.txt!"
 1148      echo "If you don't know what you are doing,"
 1149      echo "your installation is now broken."
 1150      echo ""
 1151      StartProgress countdown "Normal startup in 60s... " 60 "NOW"
 1152    fi
 1153  
 1154    [ -f "/sysroot/usr/lib/systemd/systemd" ] || error "final_check" "Could not find systemd!"
 1155  
 1156  }
 1157  
 1158  # Do init tasks to bring up system
 1159  
 1160  # run platform_init script if exists
 1161  if [ -f "./platform_init" ]; then
 1162    ./platform_init
 1163  fi
 1164  
 1165  # clear screen and hide cursor
 1166  clear >/dev/console
 1167  hidecursor
 1168  
 1169  # parse command line arguments
 1170  for arg in $(cat /proc/cmdline); do
 1171    case $arg in
 1172      BOOT_IMAGE=*)
 1173        IMAGE_KERNEL="${arg#*=}"
 1174        [ "${IMAGE_KERNEL:0:1}" = "/" ] && IMAGE_KERNEL="${IMAGE_KERNEL:1}"
 1175        ;;
 1176      SYSTEM_IMAGE=*)
 1177        IMAGE_SYSTEM="${arg#*=}"
 1178        [ "${IMAGE_SYSTEM:0:1}" = "/" ] && IMAGE_SYSTEM="${IMAGE_SYSTEM:1}"
 1179        ;;
 1180      boot=*)
 1181        boot="${arg#*=}"
 1182        case $boot in
 1183          ISCSI=*|NBD=*|NFS=*)
 1184            UPDATE_DISABLED=yes
 1185            FLASH_NETBOOT=yes
 1186            ;;
 1187          /dev/*|LABEL=*|UUID=*)
 1188            RUN_FSCK_DISKS="${RUN_FSCK_DISKS} $boot"
 1189            ;;
 1190          FOLDER=*)
 1191            RUN_FSCK_DISKS="${RUN_FSCK_DISKS} ${boot#*=}"
 1192            ;;
 1193        esac
 1194        ;;
 1195      disk=*)
 1196        disk="${arg#*=}"
 1197        case $disk in
 1198          ISCSI=*|NBD=*|NFS=*)
 1199            STORAGE_NETBOOT=yes
 1200            ;;
 1201          /dev/*|LABEL=*|UUID=*)
 1202            RUN_FSCK_DISKS="${RUN_FSCK_DISKS} $disk"
 1203            ;;
 1204          FOLDER=*)
 1205            RUN_FSCK_DISKS="${RUN_FSCK_DISKS} ${disk#*=}"
 1206            ;;
 1207        esac
 1208        ;;
 1209      wol_mac=*)
 1210        wol_mac="${arg#*=}"
 1211        ;;
 1212      wol_wait=*)
 1213        wol_wait="${arg#*=}"
 1214        ;;
 1215      textmode)
 1216        INIT_UNIT="--unit=textmode.target"
 1217        ;;
 1218      installer)
 1219        INIT_UNIT="--unit=installer.target"
 1220        SYSLINUX_DEFAULT="installer"
 1221        ;;
 1222      debugging)
 1223        DEBUG=yes
 1224        ;;
 1225      recovery)
 1226        FORCE_RECOVERY=yes
 1227        ;;
 1228      quiet)
 1229        QUIET=yes
 1230        ;;
 1231      progress)
 1232        PROGRESS=yes
 1233        INIT_ARGS="${INIT_ARGS} --show-status=1"
 1234        ;;
 1235      nofsck)
 1236        RUN_FSCK=no
 1237        ;;
 1238      toram)
 1239        SYSTEM_TORAM=yes
 1240        ;;
 1241      live)
 1242        LIVE=yes
 1243        SYSLINUX_DEFAULT="live"
 1244        ;;
 1245      portable)
 1246        SYSLINUX_DEFAULT="run"
 1247        ;;
 1248      grub_live)
 1249        LIVE=yes
 1250        GRUB_DEFAULT="Live"
 1251        ;;
 1252      grub_portable)
 1253        GRUB_DEFAULT="Run"
 1254        ;;
 1255      overlay)
 1256        OVERLAY=yes
 1257        ;;
 1258      setfbres=*)
 1259        SWITCH_FRAMEBUFFER="${arg#*=}"
 1260        SWITCH_FRAMEBUFFER="${SWITCH_FRAMEBUFFER//,/ }"
 1261        ;;
 1262      break=*)
 1263        BREAK="${arg#*=}"
 1264        ;;
 1265      bigfont=*)
 1266        BIGFONT="${arg#*=}"
 1267        ;;
 1268      ip=*)
 1269        KERNEL_IPCONFIG="yes"
 1270        ;;
 1271    esac
 1272  done
 1273  
 1274  # Existing GENERIC_X64 installs retain a boot config without quiet. Keep kernel
 1275  # console redraws off the splash there too; debugging without quiet opts out.
 1276  # This only changes console output, not the kernel log retained by journald.
 1277  if [ "${QUIET}" = "yes" ] || { [ "@DEVICENAME@" = "GENERIC_X64" ] && [ "${DEBUG}" != "yes" ]; }; then
 1278    echo '1 4 1 7' > /proc/sys/kernel/printk
 1279  fi
 1280  
 1281  if test "${DEBUG}" = "yes"; then
 1282    exec 3>&1
 1283  else
 1284    exec 3>/dev/null
 1285  fi
 1286  SILENT_OUT=3
 1287  
 1288  # If the network is up (due to the use of the "ip" kernel parameter) and a DNS
 1289  # server is known, allow the libc resolver to use it
 1290  grep '^\(nameserver\|domain\) ' /proc/net/pnp 2>/dev/null | grep -v '^nameserver 0\.0\.0\.0$' > /etc/resolv.conf
 1291  
 1292  if [ "${boot%%=*}" = "FILE" ]; then
 1293    error "check arguments" "boot argument can't be FILE type..."
 1294  fi
 1295  
 1296  debug_msg "Unique identifier for this client: ${MACHINE_UID:-NOT AVAILABLE}"
 1297  
 1298  # main boot sequence
 1299  for BOOT_STEP in \
 1300      load_modules \
 1301      recovery_mode \
 1302      check_disks \
 1303      mount_flash \
 1304      set_consolefont \
 1305      cleanup_flash \
 1306      update_bootmenu \
 1307      mount_sysroot \
 1308      mount_storage \
 1309      load_splash \
 1310      check_update \
 1311      prepare_sysroot 
 1312  do
 1313    ${BOOT_STEP}
 1314    [ -n "${DEBUG}" ] && break_after ${BOOT_STEP}
 1315  done
 1316  
 1317  BOOT_STEP=final
 1318  
 1319  # log if booting from usb / removable storage
 1320  STORAGE=$(cat /proc/mounts | grep " /sysroot/storage " 2>/dev/null | awk '{print $1}' | awk -F '/' '{print $3}')
 1321  FLASH=$(cat /proc/mounts | grep " /sysroot/flash " 2>/dev/null | awk '{print $1}' | awk -F '/' '{print $3}')
 1322  for i in ${STORAGE} ${FLASH} ; do
 1323    if [ -n "$i" ]; then
 1324      removable="/sys/class/block/*/$i/../removable"
 1325      if [ -e $removable ]; then
 1326        if [ "$(cat $removable 2>/dev/null)" = "1" ]; then
 1327          echo "### BIG FAT WARNING" > /dev/kmsg
 1328          echo "### $i is removable. suspend/resume may not work" > /dev/kmsg
 1329        fi
 1330      fi
 1331    fi
 1332  done
 1333  # move some special filesystems
 1334  /usr/bin/busybox mount --move /dev /sysroot/dev
 1335  /usr/bin/busybox mount --move /proc /sysroot/proc
 1336  /usr/bin/busybox mount --move /sys /sysroot/sys
 1337  /usr/bin/busybox mount --move /run /sysroot/run
 1338  /usr/bin/busybox rm -fr /tmp
 1339  
 1340  # setup kernel overlays
 1341  /usr/bin/busybox chroot /sysroot /usr/sbin/kernel-overlays-setup
 1342  
 1343  # tell OE settings addon to disable updates
 1344  if [ "${UPDATE_DISABLED}" = "yes" ]; then
 1345    echo "" > /sysroot/dev/.update_disabled
 1346  fi
 1347  
 1348  if [ "${FLASH_NETBOOT}" = "yes" ]; then
 1349    echo "" > /sysroot/dev/.flash_netboot
 1350  fi
 1351  
 1352  if [ "${KERNEL_IPCONFIG}" = "yes" ]; then
 1353    echo "" > /sysroot/dev/.kernel_ipconfig
 1354  fi
 1355  
 1356  # swap can not be used over nfs.(see scripts/mount-swap)
 1357  if [ "${STORAGE_NETBOOT}" = "yes" ]; then
 1358    echo "" > /sysroot/dev/.storage_netboot
 1359  fi
 1360  
 1361  BACKUP_FILE=$(ls -1 /sysroot/storage/.restore/??????????????.tar 2>/dev/null | head -n 1)
 1362  
 1363  if [ -f /sysroot/storage/.please_resize_me ]; then
 1364    INIT_UNIT="--unit=fs-resize.target"
 1365  elif [ -f /sysroot/storage/.cache/reset_oe -o -f /sysroot/storage/.cache/reset_xbmc ]; then
 1366    INIT_UNIT="--unit=factory-reset.target"
 1367  elif [ -f "${BACKUP_FILE}" ]; then
 1368    INIT_UNIT="--unit=backup-restore.target"
 1369  fi
 1370  
 1371  # stop output redirection
 1372  [ -n "${TEE_PID}" ] && kill ${TEE_PID} &>/dev/null
 1373  if [ -s /sysroot/dev/init.log ]; then
 1374    mv /sysroot/dev/init.log /sysroot/storage/init.log
 1375  else
 1376    rm -f /sysroot/dev/init.log
 1377    rm -f /sysroot/storage/init.log
 1378  fi
 1379  
 1380  # switch to new sysroot and start real init
 1381  exec /usr/bin/busybox switch_root /sysroot /usr/lib/systemd/systemd ${INIT_ARGS} ${INIT_UNIT}
 1382  
 1383  error "switch_root" "Error in initramfs. Could not switch to new root"
```

## File: sysutils/busybox/config/profile (at 8ebaf8daad, 23 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2014 Stephan Raue (stephan@openelec.tv)
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  # Read config files
    6  for CONFIG in /etc/profile.d/*; do
    7    if [ -f "${CONFIG}" ] ; then
    8      . ${CONFIG}
    9    fi
   10  done
   11  
   12  # Create user profile directory if it does not exist.
   13  if [ ! -d "/storage/.config/profile.d" ]
   14  then
   15    mkdir -p /storage/.config/profile.d
   16  fi
   17  
   18  # Read user config files
   19  for CONFIG in /storage/.config/profile.d/*; do
   20    if [ -f "${CONFIG}" ] ; then
   21      . ${CONFIG}
   22    fi
   23  done
```

## File: sysutils/system-utils/sources/autostart/common/098-deviceutils (at 8ebaf8daad, 40 lines)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  . /etc/profile
    6  
    7  if [ "${DEVICE_HAS_FAN}" == "true" ]
    8  then
    9    tocon "Enabling fan control..."
   10    nohup systemctl start fancontrol &
   11  else
   12    nohup systemctl stop fancontrol &
   13  fi
   14  
   15  if [ "${DEVICE_FAKE_JACKSENSE}" == "true" ]
   16  then
   17    tocon "Starting headphone service..."
   18    nohup systemctl start headphones &
   19  else
   20    nohup systemctl stop headphones &
   21  fi
   22  
   23  if [ "${DEVICE_HAS_HDMI}" == "true" ]
   24  then
   25    tocon "Starting hdmi service..."
   26    nohup systemctl start video &
   27  else
   28    nohup systemctl stop video &
   29  fi
   30  
   31  if [ "${DEVICE_BATTERY_LED_STATUS}" == "true" ]
   32  then
   33    tocon "Starting battery led status service..."
   34    nohup systemctl start batteryledstatus &
   35  else
   36    nohup systemctl stop batteryledstatus &
   37  fi
   38  
   39  tocon "Starting input service..."
   40  nohup systemctl start input &
```

## File: hardware/quirks/system.d/led-poweroff.service (at 8ebaf8daad, 12 lines)

```text
    1  [Unit]
    2  Description=Power LEDs off before shutting down.
    3  After=multi-user.target
    4  
    5  [Service]
    6  Type=oneshot
    7  RemainAfterExit=yes
    8  ExecStart=/bin/true
    9  ExecStop=/usr/bin/ledcontrol poweroff
   10  
   11  [Install]
   12  WantedBy=multi-user.target
```

## File: hardware/quirks/system.d/volume-fixup.service (at 8ebaf8daad, 12 lines)

```text
    1  [Unit]
    2  Description=Fix unset volumes on RK3566 devices 
    3  After=rocknix.target
    4  Before=essway.service
    5  
    6  [Service]
    7  Type=oneshot
    8  RemainAfterExit=yes
    9  ExecStart=/usr/lib/autostart/quirks/platforms/RK3566/bin/volumealign
   10  
   11  [Install]
   12  WantedBy=rocknix.target
```

## File: sysutils/autostart/system.d/rocknix-autostart.service (at 8ebaf8daad, 13 lines)

```text
    1  [Unit]
    2  Description=ROCKNIX user autostart script
    3  Before=emustation.service weston.service
    4  After=network.target graphical.target userconfig.service
    5  
    6  [Service]
    7  Type=oneshot
    8  Environment=HOME=/storage
    9  ExecStart=/bin/bash -a -c 'source /etc/profile && exec /usr/bin/autostart'
   10  RemainAfterExit=yes
   11  
   12  [Install]
   13  WantedBy=rocknix.target
```

## File: sysutils/busybox/system.d.opt/cron-defaults.service (at 8ebaf8daad, 11 lines)

```text
    1  [Unit]
    2  Description=Cron defaults
    3  After=local-fs.target
    4  
    5  ConditionPathExists=!/storage/.cache/services/crond.conf
    6  ConditionPathExists=!/storage/.cache/services/crond.disabled
    7  
    8  [Service]
    9  Type=oneshot
   10  ExecStart=/bin/sh -c 'cp /usr/share/services/crond.conf /storage/.cache/services/'
   11  RemainAfterExit=yes
```

## File: sysutils/busybox/system.d.opt/cron.service (at 8ebaf8daad, 16 lines)

```text
    1  [Unit]
    2  Description=Cron daemon
    3  After=cron-defaults.service
    4  Requires=cron-defaults.service
    5  
    6  ConditionPathExists=/storage/.cache/services/crond.conf
    7  
    8  [Service]
    9  ExecStartPre=/bin/mkdir -p /storage/.cache/cron/crontabs
   10  ExecStart=/sbin/crond -f -S
   11  KillMode=process
   12  TimeoutStopSec=1s
   13  
   14  [Install]
   15  WantedBy=multi-user.target
   16  
```

## File: sysutils/busybox/system.d/fs-resize.service (at 8ebaf8daad, 10 lines)

```text
    1  [Unit]
    2  Description=FS Resize
    3  DefaultDependencies=no
    4  
    5  [Service]
    6  Type=idle
    7  ExecStart=/usr/lib/rocknix/fs-resize
    8  StandardInput=tty-force
    9  StandardOutput=inherit
   10  StandardError=inherit
```

## File: sysutils/busybox/system.d/fs-resize.target (at 8ebaf8daad, 5 lines)

```text
    1  [Unit]
    2  Description=FS Resize target
    3  Requires=fs-resize.service
    4  After=fs-resize.service
    5  AllowIsolate=yes
```

## File: sysutils/busybox/system.d/proc-sys-fs-binfmt_misc.mount (at 8ebaf8daad, 24 lines)

```text
    1  
    2  #  SPDX-License-Identifier: LGPL-2.1-or-later
    3  #
    4  #  This file is part of systemd.
    5  #
    6  #  systemd is free software; you can redistribute it and/or modify it
    7  #  under the terms of the GNU Lesser General Public License as published by
    8  #  the Free Software Foundation; either version 2.1 of the License, or
    9  #  (at your option) any later version.
   10  
   11  [Unit]
   12  Description=Arbitrary Executable File Formats File System
   13  Documentation=https://docs.kernel.org/admin-guide/binfmt-misc.html
   14  Documentation=https://www.freedesktop.org/wiki/Software/systemd/APIFileSystems
   15  DefaultDependencies=no
   16  
   17  [Mount]
   18  What=binfmt_misc
   19  Where=/proc/sys/fs/binfmt_misc
   20  Type=binfmt_misc
   21  Options=nosuid,nodev,noexec
   22  
   23  [Install]
   24  WantedBy=local-fs.target
```

## File: sysutils/busybox/system.d/shell.service (at 8ebaf8daad, 23 lines)

```text
    1  [Unit]
    2  Description=Textmode Shell
    3  After=multi-user.target
    4  
    5  [Service]
    6  Environment=TTY=1
    7  WorkingDirectory=/storage
    8  ExecStartPre=/bin/sh -c 'echo -en "\033[?25h"'
    9  ExecStart=/bin/sh -c 'clear; lsb_release; . /etc/profile; exec /bin/sh'
   10  
   11  Restart=always
   12  RestartSec=0
   13  StandardInput=tty
   14  TTYPath=/dev/tty1
   15  TTYReset=yes
   16  TTYVHangup=yes
   17  KillMode=process
   18  IgnoreSIGPIPE=no
   19  # bash ignores SIGTERM
   20  KillSignal=SIGHUP
   21  
   22  [Install]
   23  WantedBy=textmode.target
```

## File: sysutils/busybox/system.d/show-version.service (at 8ebaf8daad, 13 lines)

```text
    1  [Unit]
    2  Description=Show Version
    3  DefaultDependencies=false
    4  ConditionKernelCommandLine=!morequiet
    5  
    6  [Service]
    7  Type=oneshot
    8  ExecStart=/usr/bin/lsb_release
    9  RemainAfterExit=yes
   10  StandardOutput=tty
   11  
   12  [Install]
   13  WantedBy=basic.target
```

## File: sysutils/busybox/system.d/storage-log.service (at 8ebaf8daad, 12 lines)

```text
    1  [Unit]
    2  Description=Create Persistent Log Directory on /storage
    3  DefaultDependencies=no
    4  RequiresMountsFor=/storage
    5  
    6  [Service]
    7  Type=oneshot
    8  RemainAfterExit=yes
    9  # journal/ is what turns journald's Storage=auto persistent; pstore/ is where
   10  # systemd-pstore archives a crash's kernel log (a symlink from
   11  # /var/lib/systemd/pstore points here, see tmpfiles z_01_rocknix.conf).
   12  ExecStart=/bin/mkdir -p /storage/.cache/log/journal /storage/.cache/log/pstore
```

## File: sysutils/busybox/system.d/textmode.target (at 8ebaf8daad, 6 lines)

```text
    1  [Unit]
    2  Description=Textmode
    3  Requires=multi-user.target
    4  After=multi-user.target
    5  Conflicts=rescue.target
    6  AllowIsolate=yes
```

## File: sysutils/busybox/system.d/var-log.mount (at 8ebaf8daad, 23 lines)

```text
    1  [Unit]
    2  Description=Persistent Log Storage
    3  # /var is a tmpfs, so without this mount every log on the device -- the
    4  # journal, EmulationStation's es_log.txt, cloud_sync.log, the kernel's own
    5  # messages -- is gone the moment the power is cut. That is precisely when it
    6  # is wanted: the RG SP froze during a startup sync and the forced power-off
    7  # that followed erased every line that could have said why (fork #102, #104).
    8  # Upstream ships this unit switched off, as a debugging aid; here it is on by
    9  # default (D-SYS-001). A device where card wear or space matters more than
   10  # evidence opts out by creating /storage/.cache/volatile-log.
   11  # systemd-journal-flush.service pulls this in through RequiresMountsFor, so
   12  # the journal lands on /storage before anything else writes to it.
   13  RequiresMountsFor=/var /storage
   14  Requires=storage-log.service
   15  After=storage-log.service
   16  ConditionKernelCommandLine=!installer
   17  ConditionPathExists=!/storage/.cache/volatile-log
   18  
   19  [Mount]
   20  What=/storage/.cache/log
   21  Where=/var/log
   22  Options=bind
   23  LazyUnmount=yes
```

## File: sysutils/busybox/system.d/var.mount (at 8ebaf8daad, 21 lines)

```text
    1  #  This file is part of systemd.
    2  #
    3  #  systemd is free software; you can redistribute it and/or modify it
    4  #  under the terms of the GNU Lesser General Public License as published by
    5  #  the Free Software Foundation; either version 2.1 of the License, or
    6  #  (at your option) any later version.
    7  
    8  [Unit]
    9  Description=Variable Directory
   10  Documentation=man:hier(7)
   11  Documentation=http://www.freedesktop.org/wiki/Software/systemd/APIFileSystems
   12  DefaultDependencies=no
   13  Before=local-fs.target umount.target
   14  
   15  [Mount]
   16  What=tmpfs
   17  Where=/var
   18  Type=tmpfs
   19  
   20  [Install]
   21  WantedBy=local-fs.target
```

## File: sysutils/powerstate/system.d/powerstate.service (at 8ebaf8daad, 21 lines)

```text
    1  [Unit]
    2  Description=AC/Battery Performance Service
    3  # The first thing the loop does is read led.color from system.cfg, and on a
    4  # first boot that file is still being seeded from /usr/config by
    5  # userconfig-setup: pulled in by sysinit.target, but with no Before= on it,
    6  # so this service started 0.1 s after it and 1.1 s before it finished (VM,
    7  # 2026-09-11). Two "awk: system.cfg: No such file" lines in the journal of
    8  # every fresh device's first boot (#121).
    9  After=userconfig.service
   10  Before=rocknix.target
   11  StartLimitIntervalSec=0
   12  
   13  [Service]
   14  Environment=HOME=/storage
   15  EnvironmentFile=/etc/profile
   16  ExecStart=/usr/bin/powerstate
   17  Restart=always
   18  RestartSec=1
   19  
   20  [Install]
   21  WantedBy=multi-user.target
```

## File: sysutils/system-utils/system.d/batteryledstatus.service (at 8ebaf8daad, 12 lines)

```text
    1  [Unit]
    2  Description=Battery LED Status
    3  Before=rocknix.target
    4  ConditionPathExists=/usr/bin/battery_led_status
    5  
    6  [Service]
    7  Environment=HOME=/storage
    8  ExecStart=/usr/bin/battery_led_status
    9  Restart=on-failure
   10  
   11  [Install]
   12  WantedBy=multi-user.target
```

## File: sysutils/system-utils/system.d/fancontrol.service (at 8ebaf8daad, 11 lines)

```text
    1  [Unit]
    2  Description=Simple Fan Control Service
    3  Before=rocknix.target
    4  
    5  [Service]
    6  Environment=HOME=/storage
    7  ExecStart=/usr/bin/fancontrol
    8  Restart=on-failure
    9  
   10  [Install]
   11  WantedBy=multi-user.target
```

## File: sysutils/system-utils/system.d/headphones.service (at 8ebaf8daad, 12 lines)

```text
    1  [Unit]
    2  Description=Headphone Sense
    3  Before=rocknix.target
    4  After=pipewire.service
    5  
    6  [Service]
    7  Environment=HOME=/storage
    8  ExecStart=/usr/bin/headphone_sense
    9  Restart=on-failure
   10  
   11  [Install]
   12  WantedBy=multi-user.target
```

## File: sysutils/system-utils/system.d/input.service (at 8ebaf8daad, 14 lines)

```text
    1  [Unit]
    2  Description=Volume button service
    3  After=headphones.service
    4  Before=rocknix.target
    5  StartLimitIntervalSec=0
    6  
    7  [Service]
    8  Environment=HOME=/storage
    9  ExecStart=/usr/bin/input_sense
   10  Restart=always
   11  RestartSec=1
   12  
   13  [Install]
   14  WantedBy=multi-user.target
```

## File: sysutils/system-utils/system.d/video.service (at 8ebaf8daad, 11 lines)

```text
    1  [Unit]
    2  Description=Video Sense
    3  Before=rocknix.target
    4  
    5  [Service]
    6  Environment=HOME=/storage
    7  ExecStart=/usr/bin/video_sense
    8  Restart=on-failure
    9  
   10  [Install]
   11  WantedBy=multi-user.target
```

## File: sysutils/systemd/system.d/debugconfig.service (at 8ebaf8daad, 14 lines)

```text
    1  [Unit]
    2  Description=Setup debug config
    3  DefaultDependencies=no
    4  After=systemd-tmpfiles-setup.service
    5  ConditionKernelCommandLine=|debugging
    6  ConditionPathExists=|/storage/.cache/debug.rocknix
    7  
    8  [Service]
    9  Type=oneshot
   10  ExecStart=/bin/sh -c 'cp /usr/share/debugconf/*.conf /run/rocknix/debug'
   11  RemainAfterExit=yes
   12  
   13  [Install]
   14  WantedBy=sysinit.target
```

## File: sysutils/systemd/system.d/machine-id.service (at 8ebaf8daad, 13 lines)

```text
    1  [Unit]
    2  Description=Setup machine-id
    3  DefaultDependencies=no
    4  Conflicts=shutdown.target
    5  Before=systemd-journald.service systemd-tmpfiles-setup-dev.service shutdown.target
    6  
    7  [Service]
    8  Type=oneshot
    9  ExecStart=/usr/bin/systemd-machine-id-setup
   10  RemainAfterExit=yes
   11  
   12  [Install]
   13  WantedBy=sysinit.target
```

## File: sysutils/systemd/system.d/network-base.service (at 8ebaf8daad, 21 lines)

```text
    1  [Unit]
    2  Description=Base Network Configuration
    3  DefaultDependencies=no
    4  After=local-fs.target systemd-tmpfiles-setup.service userconfig.service
    5  # Before hostnamed and NetworkManager (fork #50). /etc/hostname is a symlink
    6  # to /proc/sys/kernel/hostname, so systemd-hostnamed takes whatever the
    7  # kernel is called when it starts as the "static" name and re-applies it
    8  # on every later hostname1 call. NetworkManager activates hostnamed over
    9  # D-Bus at ~2.3 s; this unit wrote the name at ~3.2 s; the device then
   10  # spent the boot as ROCKNIX (GENERIC_X64 guest, 2026-09-13, one boot in
   11  # two). Ordered this way, hostnamed starts after the name is written and
   12  # reads the right one.
   13  Before=systemd-hostnamed.service NetworkManager.service
   14  
   15  [Service]
   16  Type=oneshot
   17  ExecStart=/usr/sbin/network-base-setup
   18  RemainAfterExit=yes
   19  
   20  [Install]
   21  WantedBy=network.target
```

## File: sysutils/systemd/system.d/systemd-timesyncd-setup.service (at 8ebaf8daad, 12 lines)

```text
    1  [Unit]
    2  Description=Setup NTP servers for timesyncd
    3  DefaultDependencies=no
    4  After=systemd-remount-fs.service systemd-sysusers.service
    5  
    6  [Service]
    7  Type=oneshot
    8  ExecStart=/usr/sbin/systemd-timesyncd-setup
    9  RemainAfterExit=yes
   10  
   11  [Install]
   12  WantedBy=sysinit.target
```

## File: sysutils/systemd/system.d/usercache.service (at 8ebaf8daad, 13 lines)

```text
    1  [Unit]
    2  Description=Setup User cache dir
    3  DefaultDependencies=no
    4  After=systemd-tmpfiles-setup.service
    5  Before=automount.service autostart.service
    6  
    7  [Service]
    8  Type=oneshot
    9  ExecStart=/usr/bin/usercache-setup
   10  RemainAfterExit=yes
   11  
   12  [Install]
   13  WantedBy=sysinit.target
```

## File: sysutils/systemd/system.d/userconfig.service (at 8ebaf8daad, 14 lines)

```text
    1  [Unit]
    2  Description=Setup User config dir
    3  DefaultDependencies=no
    4  After=systemd-tmpfiles-setup.service
    5  Before=rocknix-automount.service autostart.service
    6  
    7  [Service]
    8  Type=oneshot
    9  ExecStart=/usr/bin/userconfig-setup
   10  RemainAfterExit=yes
   11  StandardOutput=journal+console
   12  
   13  [Install]
   14  WantedBy=sysinit.target
```

## File: sysutils/udevil/system.d/udevil-mount@.service (at 8ebaf8daad, 11 lines)

```text
    1  [Unit]
    2  Description=Udevil mount service
    3  After=rocknix-automount.service
    4  
    5  [Service]
    6  Type=oneshot
    7  ExecStart=-/usr/bin/udevil --mount %I
    8  ExecStop=-/usr/bin/udevil --umount %I
    9  ExecStartPost=-/usr/lib/samba/samba-autoshare
   10  ExecStopPost=-/usr/lib/samba/samba-autoshare
   11  RemainAfterExit=yes
```

## File: sysutils/util-linux/system.d/fstrim.service (at 8ebaf8daad, 7 lines)

```text
    1  [Unit]
    2  Description=Discard unused blocks on all filesystems
    3  
    4  [Service]
    5  Type=oneshot
    6  ExecStart=-/usr/sbin/fstrim --all --verbose --quiet-unsupported
    7  ExecStart=-/usr/bin/touch /storage/.cache/fstrim.run
```

## File: sysutils/util-linux/system.d/fstrim.timer (at 8ebaf8daad, 10 lines)

```text
    1  [Unit]
    2  Description=Discard unused blocks once a week
    3  
    4  [Timer]
    5  OnCalendar=weekly
    6  AccuracySec=1h
    7  Persistent=true
    8  
    9  [Install]
   10  WantedBy=timers.target
```

## File: hardware/quirks/platforms/GENERIC_X64/090-ui_service (at 8ebaf8daad, 8 lines)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  ### Set the default device configuration
    6  cat <<EOF >/storage/.config/profile.d/090-ui_service
    7  UI_SERVICE="sway.service essway.service"
    8  EOF
```

## File: hardware/quirks/platforms/GENERIC_X64/091-ui_shader (at 8ebaf8daad, 8 lines)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2024 ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  ### Set the default device configuration
    6  cat <<EOF >/storage/.config/profile.d/091-ui_shader
    7  UI_SHADER="slangp"
    8  EOF
```

## File: hardware/quirks/platforms/GENERIC_X64/092-retroarch-surface (at 8ebaf8daad, 113 lines)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  ### RetroArch draws at the panel's size, on whatever mode the guest has.
    6  #
    7  # The image used to ship video_fullscreen_x/y = 0 here, and under wayland
    8  # that gave RetroArch a fullscreen surface the size of the game's picture
    9  # (240x256 for an NES core) that sway then scaled to the 640x480 output.
   10  # Every RetroArch frame ever read off a QA guest -- text, widgets, the
   11  # achievement banner -- was that small surface resampled up, and every
   12  # stem in every letter was two grey columns wide whatever the font size
   13  # (fork #263; #251's measurements described the scaling). The H700 ships
   14  # 640/480 and never drew this way.
   15  #
   16  # The shipped cfg says 640x480; a guest on another mode (the 1280x800 QA
   17  # guest) gets its own here, and keeps following it -- a guest kept and
   18  # re-run at another --res gets the new size -- for as long as the values
   19  # are this quirk's:
   20  #   - a size RECORD (beside the cfg, so a settings backup carries it with
   21  #     the values it describes) names as its own;
   22  #   - the shipped values, 640x480 or 0x0, with or without a record: that is
   23  #     the cfg after RESET RETROARCH CONFIG TO DEFAULT, which replaces
   24  #     retroarch.cfg and leaves RECORD, and either on another mode is the
   25  #     scaling this quirk exists to end -- so a hand-set 640x480 or 0x0
   26  #     follows the mode too. The pair, never one axis: the first version
   27  #     rewrote each axis into the mode's own size, so 640x0 and 0x480 are
   28  #     somebody's (short of a boot cut between its two writes on a
   29  #     640-wide mode);
   30  #   - with no RECORD yet, exactly the size this boot writes: an earlier
   31  #     build's write for this mode, or a hand-set pair equal to it, and
   32  #     taking it changes nothing now.
   33  # Anything else was set by somebody, or by an earlier build at a mode it
   34  # can no longer be told from, and is left alone; setting the two values to 0
   35  # hands them back. The cfg is only ever rewritten with RECORD already naming
   36  # both the old size and the new one, so a boot cut short between the two
   37  # writes still knows the cfg's size is its own. RetroArch does not write
   38  # these back (config_save_on_exit is off).
   39  CFG="/storage/.config/retroarch/retroarch.cfg"
   40  RECORD="/storage/.config/retroarch/.fullscreen-surface"
   41  [ -f "${CFG}" ] || exit 0
   42  
   43  # RetroArch's driver. This device's cfg named vulkan until 2026-09, and the
   44  # image carries no Vulkan driver, so RetroArch exited without drawing a
   45  # frame; gl is what a guest draws with (virgl, or llvmpipe with --gl none).
   46  # A cfg still naming vulkan moves to gl -- only while no Vulkan ICD exists
   47  # in the loader's system directories or in root's own (home is /storage).
   48  ICD=no
   49  for f in /usr/share/vulkan/icd.d/*.json /usr/local/share/vulkan/icd.d/*.json \
   50           /etc/vulkan/icd.d/*.json /storage/.local/share/vulkan/icd.d/*.json \
   51           /storage/.config/vulkan/icd.d/*.json; do
   52    [ -e "${f}" ] && ICD=yes
   53  done
   54  if [ "${ICD}" = no ] && grep -q '^video_driver = "vulkan"$' "${CFG}"; then
   55    sed -i 's/^video_driver = "vulkan"$/video_driver = "gl"/' "${CFG}"
   56  fi
   57  
   58  # The mode sway will take: the preferred (first) mode of the connected
   59  # output. The compositor has not started at this point of the boot, so
   60  # there is no current mode to read, and sway takes the preferred one. An
   61  # interlaced mode is named 1920x1080i; its height is still 1080.
   62  MODE=""
   63  for c in /sys/class/drm/card*-*; do
   64    [ "$(cat "${c}/status" 2>/dev/null)" = connected ] || continue
   65    MODE="$(head -n 1 "${c}/modes" 2>/dev/null)"
   66    [ -n "${MODE}" ] && break
   67  done
   68  MODE="${MODE%i}"
   69  case "${MODE}" in
   70    [1-9]*x[1-9]*) W="${MODE%%x*}"; H="${MODE#*x}" ;;
   71    *) exit 0 ;;
   72  esac
   73  case "${W}${H}" in *[!0-9]*) exit 0 ;; esac
   74  WANT="${W}x${H}"
   75  
   76  value() { sed -n "s/^$1 = \"\\([0-9]*\\)\"\$/\\1/p" "${CFG}" | head -n 1; }
   77  X="$(value video_fullscreen_x)"; Y="$(value video_fullscreen_y)"
   78  [ -n "${X}" ] && [ -n "${Y}" ] || exit 0
   79  SIZE="${X}x${Y}"
   80  
   81  # The sizes RECORD names: surface=WxH lines, or its first form (a5a03bd9fa),
   82  # one video_fullscreen_x= and one video_fullscreen_y= line.
   83  recorded() {
   84    [ -f "${RECORD}" ] || return 1
   85    grep -qx "surface=${1}" "${RECORD}" && return 0
   86    [ "$(sed -n 's/^video_fullscreen_x=\([0-9]*\)$/\1/p' "${RECORD}")x$(sed -n 's/^video_fullscreen_y=\([0-9]*\)$/\1/p' "${RECORD}")" = "${1}" ]
   87  }
   88  record() {
   89    { echo "# 092-retroarch-surface (GENERIC_X64): the fullscreen sizes of its own that retroarch.cfg may hold"
   90      for s in "$@"; do echo "surface=${s}"; done; } > "${RECORD}.new" && mv "${RECORD}.new" "${RECORD}"
   91  }
   92  
   93  OURS=no
   94  if recorded "${SIZE}"; then
   95    OURS=yes
   96  elif [ "${SIZE}" = 640x480 ] || [ "${SIZE}" = 0x0 ]; then
   97    OURS=yes
   98  elif [ ! -f "${RECORD}" ] && [ "${SIZE}" = "${WANT}" ]; then
   99    OURS=yes
  100  fi
  101  [ "${OURS}" = yes ] || exit 0
  102  
  103  if [ "${SIZE}" != "${WANT}" ]; then
  104    record "${SIZE}" "${WANT}" || exit 0
  105    sed -i -e "s/^video_fullscreen_x = .*/video_fullscreen_x = \"${W}\"/" \
  106           -e "s/^video_fullscreen_y = .*/video_fullscreen_y = \"${H}\"/" "${CFG}"
  107    [ "$(value video_fullscreen_x)x$(value video_fullscreen_y)" = "${WANT}" ] || exit 0
  108  fi
  109  # The cfg holds WANT: the record names it alone from here.
  110  if [ "$(grep -v '^#' "${RECORD}" 2>/dev/null)" != "surface=${WANT}" ]; then
  111    record "${WANT}"
  112  fi
  113  exit 0
```

## File: hardware/quirks/platforms/GENERIC_X64/095-cloud-ssh (at 8ebaf8daad, 76 lines)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # QEMU dev builds: when the guest is reached through a forward on the host
    6  # machine, the SSH command a tester must run targets the host's loopback
    7  # forward, not this guest's own (unreachable) address. The host side
    8  # supplies the forwarded port through fw_cfg (opt/org.rocknix.cloud_ssh_port
    9  # - only the port: UTM splits QEMU arguments on whitespace, so a full
   10  # command string cannot survive the trip). Assemble the command here and
   11  # publish it as the cloud-setup connection override; never leave a stale
   12  # one of ours behind.
   13  #
   14  # The same file is the manual fallback the VM README documents: a tester
   15  # whose guest is reached some other way (a bridged or host-network UTM mode,
   16  # a forward of their own) writes the command that works into it. That one
   17  # is theirs. This quirk replaces or removes only a command it wrote itself:
   18  # one RECORD names (RECORD names the old command and the new one before the
   19  # file changes, so a boot cut short between the two still knows it), or --
   20  # with no RECORD yet -- exactly the command this boot would write: an
   21  # earlier build wrote that very line, and taking it changes nothing now. A
   22  # loopback command on another port with no record could be a tester's own
   23  # forward and is left, as is anything else. Delete the file to go back to
   24  # the automatic command.
   25  
   26  FWCFG="/sys/firmware/qemu_fw_cfg/by_name/opt/org.rocknix.cloud_ssh_port/raw"
   27  TARGET="/storage/.config/cloud_setup_ssh"
   28  RECORD="/storage/.config/.cloud_setup_ssh.generated"
   29  
   30  # Retired override from the web-GUI era; clean up so no stale file lingers.
   31  rm -f /storage/.config/cloud_setup_url
   32  
   33  # A port is one to five digits, 1 to 65535; anything else on fw_cfg is no
   34  # port at all, never a shortened one.
   35  PORT=""
   36  if [ -r "${FWCFG}" ]; then
   37    RAW=$(tr -cd '0-9' < "${FWCFG}")
   38    case "${#RAW}" in
   39      1|2|3|4|5) [ "${RAW}" -ge 1 ] && [ "${RAW}" -le 65535 ] && PORT="${RAW}" ;;
   40    esac
   41  fi
   42  # The -L tunnel carries rclone's provider sign-in page (guest port 53682)
   43  # to the browser of the machine running SSH - see rclone.org/remote_setup.
   44  CMD=""
   45  [ -n "${PORT}" ] && CMD="ssh -L 53682:localhost:53682 -p ${PORT} root@127.0.0.1"
   46  
   47  ours() {
   48    [ -e "${TARGET}" ] || return 0
   49    [ "$(wc -l < "${TARGET}")" -le 1 ] || return 1
   50    LINE="$(cat "${TARGET}")"
   51    [ -n "${LINE}" ] || return 1
   52    if [ -f "${RECORD}" ]; then
   53      grep -qxF -- "${LINE}" "${RECORD}"
   54      return
   55    fi
   56    [ -n "${CMD}" ] && [ "${LINE}" = "${CMD}" ]
   57  }
   58  record() { printf '%s\n' "$@" > "${RECORD}.new" && mv "${RECORD}.new" "${RECORD}"; }
   59  
   60  if [ -n "${CMD}" ]; then
   61    ours || exit 0
   62    if [ "$(cat "${TARGET}" 2>/dev/null)" != "${CMD}" ]; then
   63      if [ -e "${TARGET}" ]; then
   64        record "$(cat "${TARGET}")" "${CMD}" || exit 0
   65      else
   66        record "${CMD}" || exit 0
   67      fi
   68      echo "${CMD}" > "${TARGET}.new" && mv "${TARGET}.new" "${TARGET}" || exit 0
   69    fi
   70    # The file holds CMD: the record names it alone from here.
   71    [ "$(cat "${TARGET}")" = "${CMD}" ] && [ "$(cat "${RECORD}" 2>/dev/null)" != "${CMD}" ] && record "${CMD}"
   72  elif ours; then
   73    rm -f "${TARGET}"
   74    [ -e "${TARGET}" ] || rm -f "${RECORD}"
   75  fi
   76  exit 0
```

## File: hardware/quirks/platforms/GENERIC_X64/097-retired-rescue-masks (at 8ebaf8daad, 40 lines)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  ### Takes back, once, the rescue and emergency masks an earlier quirk set.
    6  #
    7  # Until 2026-09, 097-disable-rescue-completely ran `systemctl mask` on
    8  # rescue.target, emergency.target, rescue.service and emergency.service at
    9  # every boot. systemctl writes a mask into this image's unit directory,
   10  # /storage/.config/system.d, so the masks outlived the quirk, and a boot whose
   11  # local filesystems fail stops with no emergency target to reach -- the
   12  # behaviour every other ROCKNIX device keeps. (Its stub targets under /lib
   13  # never existed: /lib is the read-only image.) Only a mask -- a link to
   14  # /dev/null -- is removed; a unit of somebody's own under one of these names
   15  # is theirs. It runs until the four are gone, says on the journal what it
   16  # unmasked, and then stops (STAMP): a mask somebody makes afterwards is
   17  # theirs. A guest that goes back to a build with the old quirk has them
   18  # masked again at every boot; on a QEMU guest, where that build's device
   19  # quirks ran too, 091-retired-vm-fixes knows it by their files coming back
   20  # and removes STAMP, so the four are taken back at the boot after. NOTE
   21  # tells it that STAMP was written this boot, and is not to be removed. (On
   22  # another hypervisor nothing tells: remove STAMP to take them back again.)
   23  STAMP=/storage/.cache/retired-rescue-masks
   24  NOTE=/run/retired-rescue-masks.stamped
   25  [ -e "${STAMP}" ] && exit 0
   26  D=/storage/.config/system.d
   27  masked() { [ -L "${D}/${1}" ] && [ "$(readlink "${D}/${1}")" = /dev/null ]; }
   28  GONE=""
   29  for unit in rescue.target emergency.target rescue.service emergency.service; do
   30    if masked "${unit}"; then
   31      rm -f "${D}/${unit}"
   32      masked "${unit}" || GONE="${GONE} ${unit}"
   33    fi
   34  done
   35  [ -n "${GONE}" ] && echo "097-retired-rescue-masks: unmasked what an earlier build masked:${GONE}" >&2
   36  for unit in rescue.target emergency.target rescue.service emergency.service; do
   37    masked "${unit}" && exit 0
   38  done
   39  mkdir -p "${STAMP%/*}" && echo "the rescue and emergency masks an earlier build set were taken back" > "${STAMP}" && : > "${NOTE}"
   40  exit 0
```

## File: hardware/quirks/profile.d/999-export (at 8ebaf8daad, 73 lines)

```text
    1  #!/bin/sh
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  ### If you add a variable that should persist across processes,
    6  ### remember to export it here.
    7  
    8  export  OS_NAME \
    9  	OS_VERSION \
   10  	OS_BUILD \
   11  	SLOW_CORES \
   12  	FAST_CORES \
   13  	CPU_FREQ \
   14  	DMC_FREQ \
   15  	GPU_FREQ \
   16  	HW_DEVICE\
   17  	DEVICE_ASPECT_RATIO \
   18  	DEVICE_AUDIO_MIXER \
   19  	DEVICE_BATTERY_LED_STATUS \
   20  	DEVICE_DTB_SWITCH \
   21  	DEVICE_FAKE_JACKSENSE \
   22  	DEVICE_FUNC_KEYA_MODIFIER \
   23  	DEVICE_FUNC_KEYB_MODIFIER \
   24  	DEVICE_HAS_FAN \
   25  	DEVICE_GPU_CUR_FREQ \
   26  	DEVICE_GPU_MAX_FREQ \
   27  	DEVICE_GPU_OVERCLOCK \
   28  	DEVICE_GPU_TEMP_SENSOR \
   29  	DEVICE_HAS_HDMI \
   30  	DEVICE_HAS_TOUCHSCREEN \
   31  	DEVICE_HDMI_GPIO \
   32  	DEVICE_HAS_DUAL_SCREEN \
   33  	DEVICE_HEADPHONE_DEV \
   34  	DEVICE_JACK \
   35  	DEVICE_KEY_VOLUMEDOWN \
   36  	DEVICE_KEY_VOLUMEUP \
   37  	DEVICE_LED_BRIGHTNESS \
   38  	DEVICE_LED_CHARGING \
   39  	DEVICE_LED_CONTROL \
   40  	DEVICE_ANALOG_STICKS_LED_CONTROL \
   41  	DEVICE_MANGOHUD_SUPPORT \
   42  	DEVICE_MMC_EJECT \
   43  	DEVICE_PIPEWIRE_PROFILE \
   44  	DEVICE_PWR_LED_CONTROL \
   45  	DEVICE_PWR_LED_GPIO \
   46  	DEVICE_PLAYBACK_PATH \
   47  	DEVICE_PLAYBACK_PATH_HP \
   48  	DEVICE_PLAYBACK_PATH_SPK \
   49  	DEVICE_PWM_FAN \
   50  	DEVICE_PWM_MOTOR \
   51  	DEVICE_PRODUCT_SERIAL \
   52  	DEVICE_RK817_FUEL_GAUGE \
   53  	DEVICE_SERIAL_NUMBER_PATH \
   54  	DEVICE_SW_HP_SWITCH \
   55  	DEVICE_TEMP_SENSOR \
   56  	DEVICE_TURBO_MODE \
   57  	DEVICE_VOLUME \
   58  	DEVICE_WIFI \
   59  	HDMI_STATE \
   60  	QUIRK_DEVICE \
   61  	UI_SERVICE \
   62  	PAN_MESA_DEBUG \
   63  	WLR_DRM_DEVICES \
   64  	WLR_BACKENDS \
   65  	WLR_CON \
   66  	MALI_WAYLAND_AFBC \
   67      MALI_DEFAULT_DISPLAY \
   68      PAN_I_WANT_A_BROKEN_VULKAN_DRIVER \
   69      DISABLE_WSI_LAYER \
   70  	ALSA_PRIMARY_CARD \
   71  	SDL_VIDEO_DISPLAY_PRIORITY \
   72  	TU_DEBUG \
   73  	MESA_LOADER_DRIVER_OVERRIDE
```

## File: sysutils/busybox/sysctl.d/99-coredump.conf (at 8ebaf8daad, 4 lines)

```text
    1  # Keep a bounded ring of core dumps under /storage/.cache/log/cores, so a
    2  # crash can be read rather than argued about (fork #79, #211). The handler
    3  # caps and prunes; see rocknix-corekeep for what it keeps and what it refuses.
    4  kernel.core_pattern=|/usr/bin/rocknix-corekeep %e %p %t %s %E
```

## File: sysutils/busybox/sysctl.d/hang-policy.conf (at 8ebaf8daad, 17 lines)

```text
    1  # A hang ends itself and leaves its trace (fork #104, D-SYS-003).
    2  #
    3  # A CPU that stops scheduling for 20 s, or a task stuck inside the kernel for
    4  # 120 s, is today a device that stays frozen until somebody holds the power
    5  # button -- which is what erased the evidence and truncated two config files
    6  # on the RG SP (#102). With these the kernel panics instead, ramoops keeps
    7  # the trace where the next boot can read it, and the device reboots itself
    8  # ten seconds later. panic_on_oops stays at its default of 0: an oops that
    9  # does not take the machine down is written to the persistent journal and the
   10  # player keeps their session.
   11  #
   12  # Here in /usr/lib/sysctl.d rather than under /usr/config, so it applies on
   13  # the first boot after an update and needs nothing copied to /storage first;
   14  # a device's own /storage/.config/sysctl.d still takes precedence.
   15  kernel.panic = 10
   16  kernel.softlockup_panic = 1
   17  kernel.hung_task_panic = 1
```

## File: sysutils/nvtop/package.mk (at 8ebaf8daad, 33 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0
    2  # Copyright (C) 2024-present JELOS (https://github.com/JustEnoughLinuxOS)
    3  
    4  PKG_NAME="nvtop"
    5  PKG_VERSION="76890233d759199f50ad3bdb57a0c0988e96fc44" #3.3.2
    6  PKG_SHA256="4391c5c9eecd09ed00a2c9f5fe6f36419acf52d0084d6e98213d36d657206a45"
    7  PKG_LICENSE="GPLv3"
    8  PKG_SITE="https://github.com/Syllo/nvtop"
    9  PKG_URL="${PKG_SITE}/archive/${PKG_VERSION}.tar.gz"
   10  PKG_DEPENDS_TARGET="libdrm mesa"
   11  PKG_LONGDESC="NVTOP stands for Neat Videocard TOP, a (h)top like task monitor for AMD, Intel and NVIDIA GPUs."
   12  PKG_TOOLCHAIN="cmake"
   13  
   14  case ${TARGET_ARCH} in
   15    x86_64)
   16      PKG_CMAKE_OPTS_TARGET+=" -DNVIDIA_SUPPORT=ON -DPANFROST_SUPPORT=OFF -DPANTHOR_SUPPORT=OFF -DMSM_SUPPORT=OFF"
   17  
   18      # The AMD and Intel backends include libdrm headers that libdrm itself
   19      # only installs when the matching Gallium driver is in GRAPHIC_DRIVERS -
   20      # amdgpu.h with radeonsi, xe_drm.h with the intel drivers. Mirror those
   21      # gates rather than assuming every x86_64 device is AMD64: a target
   22      # shipping only virtio has neither header, and no GPU those backends
   23      # could report on either.
   24      listcontains "${GRAPHIC_DRIVERS}" "radeonsi" &&
   25        PKG_CMAKE_OPTS_TARGET+=" -DAMDGPU_SUPPORT=ON" || PKG_CMAKE_OPTS_TARGET+=" -DAMDGPU_SUPPORT=OFF"
   26  
   27      listcontains "${GRAPHIC_DRIVERS}" "(crocus|i915|iris)" &&
   28        PKG_CMAKE_OPTS_TARGET+=" -DINTEL_SUPPORT=ON" || PKG_CMAKE_OPTS_TARGET+=" -DINTEL_SUPPORT=OFF"
   29      ;;
   30    aarch64)
   31      PKG_CMAKE_OPTS_TARGET+=" -DPANFROST_SUPPORT=ON -DPANTHOR_SUPPORT=ON -DMSM_SUPPORT=ON -DNVIDIA_SUPPORT=OFF -DAMDGPU_SUPPORT=OFF -DINTEL_SUPPORT=OFF"
   32      ;;
   33  esac
```

## File: sysutils/powerstate/sources/powerstate.sh (at 8ebaf8daad, 80 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
    4  
    5  ###
    6  ### Normally this would be a udev rule, but some devices like the AyaNeo Air
    7  ### do not properly report the applied power state to udev, and we can't use
    8  ### inotifyd to watch the status in /sys.
    9  ###
   10  
   11  . /etc/profile
   12  
   13  BATCNT=0
   14  unset CURRENT_MODE
   15  unset AC_STATUS
   16  ledcontrol $(get_setting led.color)
   17  
   18  while true; do
   19    AC_STATUS="$(cat /sys/class/power_supply/[bB][aA][tT]*/status 2>/dev/null)"
   20    if [[ ! "${CURRENT_MODE}" =~ ${AC_STATUS} ]]; then
   21      case ${AC_STATUS} in
   22        Disch*)
   23          log $0 "Switching to battery mode."
   24          if [ -e "/tmp/.gpu_performance_level" ]; then
   25            GPUPROFILE=$(cat /tmp/.gpu_performance_level)
   26          else
   27            GPUPROFILE=$(get_setting system.gpuperf)
   28          fi
   29          if [ -z "${GPUPROFILE}" ]; then
   30            GPUPROFILE="auto"
   31          fi
   32          gpu_performance_level ${GPUPROFILE}
   33          if [ "${DEVICE_LED_CHARGING}" = "true" ]; then
   34            ledcontrol discharging
   35          fi
   36        ;;
   37        *)
   38          log $0 "Switching to performance mode."
   39          gpu_performance_level auto
   40          if [ "${DEVICE_LED_CHARGING}" = "true" ]; then
   41            ledcontrol charging
   42          fi
   43        ;;
   44      esac
   45      CURRENT_MODE="${AC_STATUS}"
   46    fi
   47    ### Until we have an overlay. :rofl:
   48    # One reading, the first battery if there are several. No battery at all
   49    # (the GENERIC_X64 guest) or a driver that has not probed yet leaves this
   50    # empty, and an empty operand in (( )) is an arithmetic error -- logged
   51    # every two seconds for the life of the boot, so it was the last line of
   52    # every VM journal (#121). Nothing to compare means nothing to do this
   53    # pass; a battery that comes up late is read on the next one.
   54    BATLEFT=$(battery_percent | head -n1)
   55    if [[ "${BATLEFT}" =~ ^[0-9]+$ ]]; then
   56      if (( "${BATCNT}" >= "20" )) && [[ "${AC_STATUS}" =~ Disch ]]; then
   57        AUDIBLEALERT=$(get_setting system.battery.warning)
   58        AUDIBLEALERT_THRESHOLD=$(get_setting system.battery.warning_threshold)
   59        [[ -z $AUDIBLEALERT_THRESHOLD ]] && AUDIBLEALERT_THRESHOLD=25
   60  
   61        if [[ ${BATLEFT} -le ${AUDIBLEALERT_THRESHOLD} ]]; then
   62          if [ "${DEVICE_LED_CONTROL}" = "true" ] && [ ! "${DEVICE_BATTERY_LED_STATUS}" = "true" ]; then
   63            # Flash the RGB or power LED if available.
   64            led_flash
   65            BATCNT=0
   66          elif [ "${AUDIBLEALERT}" = "1" ]; then
   67            say "BATTERY AT ${BATLEFT}%"
   68            BATCNT=0
   69          fi
   70        fi
   71      elif (( "${BATLEFT}" > "97" )); then
   72        if [ "${DEVICE_LED_CHARGING}" = "true" ]; then
   73          # Reset the LED as if the battery was full.
   74          ledcontrol discharging
   75        fi
   76      fi
   77    fi
   78    BATCNT=$(( ${BATCNT} + 1 ))
   79    sleep 2
   80  done
```

## File: sysutils/system-utils/sources/devices/GENERIC_X64/video_sense (at 8ebaf8daad, 20 lines)

```text
    1  #!/bin/bash
    2  
    3  # SPDX-License-Identifier: GPL-2.0-or-later
    4  # Copyright (C) 2025 ROCKNIX
    5  
    6  # video_sense for GENERIC_X64 - No-op version for VMs/x86_64
    7  # HDMI detection via GPIO is not applicable to x86_64/VM environments
    8  
    9  . /etc/profile
   10  
   11  # For x86_64/VM environments, we don't need hardware HDMI detection
   12  # Just sleep indefinitely to satisfy systemd service requirements
   13  # Audio switching can be handled by desktop environment or manual configuration
   14  
   15  log $0 "video_sense: GENERIC_X64 no-op version running"
   16  
   17  # Keep the service alive but do nothing
   18  while true; do
   19      sleep 3600  # Sleep for 1 hour intervals
   20  done
```

## File: sysutils/system-utils/sources/scripts/input_sense (at 8ebaf8daad, 539 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2021-22 pkegg
    4  # Copyright (C) 2022-24 JELOS (https://github.com/JustEnoughLinuxOS)
    5  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    6  
    7  . /etc/profile
    8  
    9  # Remove or comment out 'set -e' so the script doesn't exit on a single error:
   10  # set -e
   11  set -o pipefail
   12  
   13  ### Summary
   14  #   This script listens to input events and takes actions.
   15  ###
   16  
   17  ### Enable logging
   18  case $(get_setting system.loglevel) in
   19    verbose)
   20      DEBUG=true
   21    ;;
   22    *)
   23      DEBUG=false
   24    ;;
   25  esac
   26  
   27  ### Define matching values from evtest, but allow them to be overridden in system.cfg.
   28  KEY_VOLUME_UP=$(get_setting key.volume.up)
   29  [ -z "${KEY_VOLUME_UP}" ] && KEY_VOLUME_UP='KEY_VOLUME*UP'
   30  
   31  KEY_VOLUME_DOWN=$(get_setting key.volume.down)
   32  [ -z "${KEY_VOLUME_DOWN}" ] && KEY_VOLUME_DOWN='KEY_VOLUME*DOWN'
   33  
   34  FUNCTION_VOLUME_UP_EVENT='*('${KEY_VOLUME_UP}'), value *'
   35  FUNCTION_VOLUME_DOWN_EVENT='*('${KEY_VOLUME_DOWN}'), value *'
   36  
   37  FUNCTION_POWER_RELEASED_EVENT='*(KEY_POWER), value 0'
   38  FUNCTION_POWER_PRESSED_EVENT='*(KEY_POWER), value 1'
   39  
   40  FUNCTION_LID_OPEN_EVENT='*(SW_LID), value 0'
   41  FUNCTION_LID_CLOSE_EVENT='*(SW_LID), value 1'
   42  
   43  ### Define matching function hotkeys from controller values, but allow them to be overridden in system.cfg.
   44  KEYA_MODIFIER=$(get_setting key.function.a)
   45  [ -z "${KEYA_MODIFIER}" ] && KEYA_MODIFIER="${DEVICE_FUNC_KEYA_MODIFIER}"
   46  
   47  KEYB_MODIFIER=$(get_setting key.function.b)
   48  [ -z "${KEYB_MODIFIER}" ] && KEYB_MODIFIER="${DEVICE_FUNC_KEYB_MODIFIER}"
   49  
   50  FUNCTION_MODIFIER_A_EVENT='*('${KEYA_MODIFIER}'), value *'
   51  FUNCTION_MODIFIER_B_EVENT='*('${KEYB_MODIFIER}'), value *'
   52  
   53  BTN_HOTKEY_A_MODIFIER=$(get_setting key.hotkey.a)
   54  [ -z "${BTN_HOTKEY_A_MODIFIER}" ] && BTN_HOTKEY_A_MODIFIER="BTN_TL"
   55  
   56  BTN_HOTKEY_B_MODIFIER=$(get_setting key.hotkey.b)
   57  [ -z "${BTN_HOTKEY_B_MODIFIER}" ] && BTN_HOTKEY_B_MODIFIER="BTN_SELECT"
   58  
   59  BTN_HOTKEY_C_MODIFIER=$(get_setting key.hotkey.c)
   60  [ -z "${BTN_HOTKEY_C_MODIFIER}" ] && BTN_HOTKEY_C_MODIFIER="BTN_START"
   61  
   62  HOTKEY_A_PRESSED=false
   63  HOTKEY_B_PRESSED=false
   64  HOTKEY_C_PRESSED=false
   65  
   66  FUNCTION_HOTKEY_A_EVENT='*('${BTN_HOTKEY_A_MODIFIER}'), value *'
   67  FUNCTION_HOTKEY_B_EVENT='*('${BTN_HOTKEY_B_MODIFIER}'), value *'
   68  FUNCTION_HOTKEY_C_EVENT='*('${BTN_HOTKEY_C_MODIFIER}'), value *'
   69  
   70  FUNCTION_HOTKEY_BTN_NORTH_EVENT="*(BTN_NORTH), value 1*"
   71  FUNCTION_HOTKEY_BTN_WEST_EVENT="*(BTN_WEST), value 1*"
   72  FUNCTION_HOTKEY_BTN_SOUTH_EVENT="*(BTN_SOUTH), value 1*"
   73  FUNCTION_HOTKEY_BTN_EAST_EVENT="*(BTN_EAST), value 1*"
   74  
   75  FUNCTION_HOTKEY_BTN_BACK_EVENT="*(BTN_BACK), value 1*"
   76  FUNCTION_HOTKEY_KEY_F1_EVENT="*(KEY_F1), value 1*"
   77  
   78  FUNCTION_HOTKEY_TOUCH_EVENT="*(BTN_TOUCH), value 1*"
   79  
   80  TOUCHSCREEN_EVENTS=$(get_setting key.touchscreen.events)
   81  if [ -z "${TOUCHSCREEN_EVENTS}" ] || [ "${TOUCHSCREEN_EVENTS}" = "0" ]; then
   82    TOUCHSCREEN_EVENTS=false
   83  else
   84    TOUCHSCREEN_EVENTS=true
   85  fi
   86  
   87  ### Define static values for dpad buttons and as a hat.
   88  FUNCTION_HOTKEY_DPAD_UP_EVENT="*(BTN_DPAD_UP), value 1*"
   89  FUNCTION_HOTKEY_DPAD_DOWN_EVENT="*(BTN_DPAD_DOWN), value 1*"
   90  FUNCTION_HOTKEY_DPAD_RIGHT_EVENT="*(BTN_DPAD_RIGHT), value 1*"
   91  FUNCTION_HOTKEY_DPAD_LEFT_EVENT="*(BTN_DPAD_LEFT), value 1*"
   92  
   93  FUNCTION_HOTKEY_HAT_UP_EVENT="*(ABS_HAT0Y), value -1*"
   94  FUNCTION_HOTKEY_HAT_DOWN_EVENT="*(ABS_HAT0Y), value 1*"
   95  FUNCTION_HOTKEY_HAT_RIGHT_EVENT="*(ABS_HAT0X), value 1*"
   96  FUNCTION_HOTKEY_HAT_LEFT_EVENT="*(ABS_HAT0X), value -1*"
   97  
   98  DPAD_EVENTS=$(get_setting key.dpad.events)
   99  if [ -z "${DPAD_EVENTS}" ] || [ "${DPAD_EVENTS}" = "0" ]; then
  100    DPAD_EVENTS=false
  101  else
  102    DPAD_EVENTS=true
  103  fi
  104  
  105  CONTROLLER_DISCONNECTED="*error reading: No such device"
  106  DEVICE_DISCONNECTED="*error reading: No such device"
  107  
  108  ### Matches if a button was pressed (1), released (0) or held down (2)
  109  PRESS='value 1'
  110  REPEAT='value 2'
  111  RELEASE='value 0'
  112  
  113  ### Function buttons should be defined as not pressed for later matching.
  114  FN_A_PRESSED=false
  115  FN_B_PRESSED=false
  116  
  117  ### Volume repeat variables
  118  VOLUME_REPEAT_DELAY=0.3  # Initial delay before repeating starts (seconds)
  119  VOLUME_REPEAT_INTERVAL=0.1  # Interval between repeats (seconds)
  120  VOLUME_UP_PRESSED=false
  121  VOLUME_DOWN_PRESSED=false
  122  VOLUME_REPEAT_PID=""
  123  
  124  ### Allow actions to be overridden in system.cfg
  125  FN_A_ACTION_UP="$(get_setting key.function.a.up)"
  126  FN_A_ACTION_DOWN="$(get_setting key.function.a.down)"
  127  FN_B_ACTION_UP="$(get_setting key.function.b.up)"
  128  FN_B_ACTION_DOWN="$(get_setting key.function.b.down)"
  129  FN_AB_ACTION_UP="$(get_setting key.function.ab.up)"
  130  FN_AB_ACTION_DOWN="$(get_setting key.function.ab.down)"
  131  
  132  ### Set sane defaults to manage volume, brightness, wireless on/off, and led on/off.
  133  [ -z "${FN_A_ACTION_UP}" ]    && FN_A_ACTION_UP="brightness up"
  134  [ -z "${FN_A_ACTION_DOWN}" ]  && FN_A_ACTION_DOWN="brightness down"
  135  [ -z "${FN_B_ACTION_UP}" ]    && FN_B_ACTION_UP="ledcontrol"
  136  [ -z "${FN_B_ACTION_DOWN}" ]  && FN_B_ACTION_DOWN="ledcontrol poweroff"
  137  [ -z "${FN_AB_ACTION_UP}" ]   && FN_AB_ACTION_UP="wifictl enable"
  138  [ -z "${FN_AB_ACTION_DOWN}" ] && FN_AB_ACTION_DOWN="wifictl disable"
  139  
  140  ### Volume repeat function
  141  start_volume_repeat() {
  142      local direction=$1
  143  
  144      # Stop any existing volume repeat
  145      stop_volume_repeat
  146  
  147      # Initial volume adjustment
  148      volume ${direction}
  149  
  150      # Start background process for repeating volume adjustments
  151      (
  152          sleep ${VOLUME_REPEAT_DELAY}
  153          while true; do
  154              # Check if button is still pressed before adjusting
  155              if { [ "${direction}" = "up" ] && [ "${VOLUME_UP_PRESSED}" = true ]; } || \
  156                 { [ "${direction}" = "down" ] && [ "${VOLUME_DOWN_PRESSED}" = true ]; }; then
  157                  volume ${direction}
  158                  sleep ${VOLUME_REPEAT_INTERVAL}
  159              else
  160                  break
  161              fi
  162          done
  163      ) &
  164  
  165      VOLUME_REPEAT_PID=$!
  166      ${DEBUG} && log $0 "Started volume repeat (${direction}) with PID: ${VOLUME_REPEAT_PID}"
  167  }
  168  
  169  stop_volume_repeat() {
  170      if [ -n "${VOLUME_REPEAT_PID}" ]; then
  171          kill ${VOLUME_REPEAT_PID} 2>/dev/null
  172          wait ${VOLUME_REPEAT_PID} 2>/dev/null
  173          ${DEBUG} && log $0 "Stopped volume repeat with PID: ${VOLUME_REPEAT_PID}"
  174      fi
  175      VOLUME_REPEAT_PID=""
  176  }
  177  
  178  ### Simple functions to execute button actions, including global kill.
  179  execute_kill() {
  180    if [ -e "/tmp/.process-kill-data" ]; then
  181      TO_KILL="$(cat /tmp/.process-kill-data)"
  182      ### Say that the player asked to leave, before the signal goes out. runemu.sh
  183      ### maps 137/143 to a clean exit already, which covers every emulator that
  184      ### dies on the signal -- but RetroArch catches SIGTERM and ends with its own
  185      ### exit(1), the same status as "Failed to load content", so the exit code
  186      ### alone cannot tell a forced quit from a failed launch (fork #92,
  187      ### D-LAUNCH-002). The marker sits beside the kill data this function already
  188      ### reads, in /tmp, because /tmp is a tmpfs: a power cut wipes it, and a
  189      ### marker that outlived the boot would make the next launch's failure read
  190      ### as clean. runemu.sh clears it on the way into the emulator and consumes
  191      ### it at exit; both it and this service run as root.
  192      touch "/tmp/.process-kill-requested" 2>/dev/null
  193  
  194      ### One press, one signal. The combo re-fires this on every further B or C
  195      ### press while A is held, and RetroArch takes about half a second to shut
  196      ### down -- so a player who holds the combo a moment too long, or presses
  197      ### again because the game has not vanished yet, delivers a second SIGTERM
  198      ### into that window. RetroArch answers the second one with exit(1) and
  199      ### WITHOUT flushing SRAM: measured on the VM with a battery-backed
  200      ### cartridge, one press wrote the .srm and two left none at all, losing
  201      ### everything since the last autosave (fork #117). The first press already
  202      ### ends it cleanly in ~0.5 s, so a repeat inside the window is the player
  203      ### waiting, not asking again -- it is dropped. A deliberate second attempt
  204      ### after the window still goes through, which is what a genuinely stuck
  205      ### emulator needs.
  206      ###
  207      ### date +%s, not a sub-second clock: busybox date has no %N on every
  208      ### build, and a whole second of granularity is plenty against a window
  209      ### measured in seconds.
  210      ###
  211      ### The state is a shell variable rather than a file because there is one
  212      ### reader to remember it: the several evtest processes started above all
  213      ### pipe into the single `while read line` loop below, and both callers of
  214      ### this function are inside that loop. A file would need the same
  215      ### power-cut reasoning as the marker above and buy nothing.
  216      now="$(date +%s)"
  217      if [ -n "${LAST_KILL_AT}" ] && [ "$((now - LAST_KILL_AT))" -lt 3 ]; then
  218        ${DEBUG} && log $0 "Ignoring a repeat kill $((now - LAST_KILL_AT))s after the last one; the emulator is still shutting down"
  219        return 0
  220      fi
  221      LAST_KILL_AT="${now}"
  222  
  223      ${DEBUG} && log $0 "Execute: killall ${TO_KILL}"
  224      killall ${TO_KILL} 2>/dev/null
  225    fi
  226  }
  227  
  228  execute_action() {
  229    ${DEBUG} && log $0 "${1}|${FN_A_PRESSED}|${FN_B_PRESSED}|${DPAD_UP_PRESSED}|${DPAD_DOWN_PRESSED}|${DPAD_RIGHT_PRESSED}|${DPAD_LEFT_PRESSED}"
  230    if [ "${FN_A_PRESSED}" = true ] && [ "${FN_B_PRESSED}" = true ]; then
  231      ${DEBUG} && log $0 "Executing FN_AB action"
  232      case ${1} in
  233        up)
  234          ${DEBUG} && log $0 "FN_AB (${FN_AB_ACTION_UP})"
  235          ${FN_AB_ACTION_UP}
  236          ;;
  237        down)
  238          ${DEBUG} && log $0 "FN_AB (${FN_AB_ACTION_DOWN})"
  239          ${FN_AB_ACTION_DOWN}
  240          ;;
  241      esac
  242    elif [ "${FN_A_PRESSED}" = true ] && [ "${FN_B_PRESSED}" = false ]; then
  243      ${DEBUG} && log $0 "Executing FN_A action"
  244      case ${1} in
  245        up)
  246          ${DEBUG} && log $0 "FN_A (${FN_A_ACTION_UP})"
  247          ${FN_A_ACTION_UP}
  248          if [ "${FN_A_ACTION_UP}" == "brightness up" ]; then
  249            CUR_BRIGHTNESS=$(get_setting "display.brightness")
  250            /usr/bin/mako-notify "Brightness: ${CUR_BRIGHTNESS}%" -no-es
  251          fi
  252          ;;
  253        down)
  254          ${DEBUG} && log $0 "FN_A (${FN_A_ACTION_DOWN})"
  255          ${FN_A_ACTION_DOWN}
  256          if [ "${FN_A_ACTION_DOWN}" == "brightness down" ]; then
  257            CUR_BRIGHTNESS=$(get_setting "display.brightness")
  258            /usr/bin/mako-notify "Brightness: ${CUR_BRIGHTNESS}%" -no-es
  259          fi
  260          ;;
  261      esac
  262    elif [ "${FN_A_PRESSED}" = false ] && [ "${FN_B_PRESSED}" = true ]; then
  263      ${DEBUG} && log $0 "Executing FN_B action"
  264      case ${1} in
  265        up)
  266          ${DEBUG} && log $0 "FN_B (${FN_B_ACTION_UP})"
  267          ${FN_B_ACTION_UP}
  268          ;;
  269        down)
  270          ${DEBUG} && log $0 "FN_B (${FN_B_ACTION_DOWN})"
  271          ${FN_B_ACTION_DOWN}
  272          ;;
  273      esac
  274    else
  275      # If neither FN_A nor FN_B is pressed, treat it as a volume control
  276      volume ${1}
  277    fi
  278  }
  279  
  280  ### Search the system for useful devices to monitor for inputs.
  281  INPUT_DEVICES=()
  282  
  283  get_devices() {
  284    local KJDEVS=false
  285    local FOUNDKEYS=false
  286    local FOUNDJOY=false
  287    local FOUNDTOUCH=false
  288    local RETRY=0
  289  
  290    ### Re-scanning must start from an empty list, otherwise every retry and
  291    ### every hotplug reload appends duplicates of what is already there.
  292    INPUT_DEVICES=()
  293  
  294    while [ ${KJDEVS} = false ]; do
  295      for DEV in /dev/input/ev*
  296      do
  297        unset SUPPORTS
  298        SUPPORTS=$(udevadm info ${DEV} | awk '/ID_INPUT_KEY=|ID_INPUT_JOYSTICK=|ID_INPUT_TOUCHSCREEN=/ {print $2}')
  299        if [ -n "${SUPPORTS}" ]; then
  300          DEVICE=$(udevadm info ${DEV} | awk 'BEGIN {FS="="} /DEVNAME=/ {print $2}')
  301          INPUT_DEVICES+=("${DEVICE}")
  302          if [[ "${SUPPORTS}" =~ ID_INPUT_KEY ]]; then
  303            ${DEBUG} && log $0 "Found Keyboard: ${DEVICE}"
  304            FOUNDKEYS=true
  305          elif [[ "${SUPPORTS}" =~ ID_INPUT_TOUCHSCREEN ]]; then
  306            ${DEBUG} && log $0 "Found Touchscreen: ${DEVICE}"
  307            FOUNDTOUCH=true
  308          elif [[ "${SUPPORTS}" =~ ID_INPUT_JOYSTICK ]]; then
  309            ${DEBUG} && log $0 "Found Joystick: ${DEVICE}"
  310            FOUNDJOY=true
  311          fi
  312        fi
  313      done
  314  
  315      if [ "${FOUNDKEYS}" = "true" ] && [ "${FOUNDJOY}" = "true" ]; then
  316        ${DEBUG} && log $0 "Found all needed devices."
  317        KJDEVS=true
  318        break
  319      fi
  320  
  321      if [ "${RETRY}" -ge 5 ]; then
  322        ${DEBUG} && log $0 "Did not find all needed devices, but continuing anyway."
  323        ${DEBUG} && log $0 "Did not find all of the needed devices, but that may be OK.  Breaking."
  324        break
  325      else
  326        RETRY=$(( RETRY + 1 ))
  327      fi
  328  
  329      sleep 1
  330    done
  331  }
  332  
  333  get_devices
  334  
  335  # If the input devices change, it may be a new controller
  336  # so handle it here.
  337  mkcontroller 2>/dev/null || :
  338  
  339  # ------------------------------------------------------------------
  340  # Turn OFF 'exit on error' *now* so a single evtest crash won't kill
  341  # the entire script. We still keep 'pipefail' for partial debugging.
  342  # ------------------------------------------------------------------
  343  set +e
  344  
  345  ### Start multiple evtest loops, each continuously restarted on failure. Take action when a known pattern of keys are pressed together.
  346  (
  347    for INPUT_DEVICE in "${INPUT_DEVICES[@]}"; do
  348      (
  349        while true
  350        do
  351          evtest "${INPUT_DEVICE}" 2>&1
  352          # If evtest exits, wait briefly and restart
  353          echo "evtest for ${INPUT_DEVICE} died; restarting in 1 second..." >&2
  354          sleep 1
  355        done
  356      ) &
  357    done
  358  
  359    wait  # Wait for all background loops (they never end unless forcibly stopped)
  360  ) | grep --line-buffered "EV_KEY\|EV_SW\|error reading" | while read line; do
  361  
  362      # Parse lines from any evtest instance:
  363      case ${line} in
  364        (${CONTROLLER_DISCONNECTED})
  365          ${DEBUG} && log $0 "Reloading due to ${CONTROLLER_DEVICE} reattach..."
  366          get_devices
  367        ;;
  368        (${DEVICE_DISCONNECTED})
  369          ${DEBUG} && log $0 "Reloading due to ${DEVICE} reattach..."
  370          get_devices
  371        ;;
  372        (${FUNCTION_MODIFIER_A_EVENT})
  373          if [[ "${line}" =~ ${PRESS} ]]; then
  374            ${DEBUG} && log $0 "${FUNCTION_MODIFIER_A_EVENT}: Pressed"
  375            FN_A_PRESSED=true
  376          elif [[ "${line}" =~ ${RELEASE} ]]; then
  377            ${DEBUG} && log $0 "${FUNCTION_MODIFIER_A_EVENT}: Released"
  378            FN_A_PRESSED=false
  379          fi
  380        ;;
  381        (${FUNCTION_MODIFIER_B_EVENT})
  382          if [[ "${line}" =~ ${PRESS} ]]; then
  383            ${DEBUG} && log $0 "${FUNCTION_MODIFIER_B_EVENT}: Pressed"
  384            FN_B_PRESSED=true
  385          elif [[ "${line}" =~ ${RELEASE} ]]; then
  386            ${DEBUG} && log $0 "${FUNCTION_MODIFIER_B_EVENT}: Released"
  387            FN_B_PRESSED=false
  388          fi
  389        ;;
  390        (${FUNCTION_VOLUME_UP_EVENT})
  391          if [[ "${line}" =~ ${PRESS} ]]; then
  392            ${DEBUG} && log $0 "Volume Up: Pressed"
  393            VOLUME_UP_PRESSED=true
  394            # Only start volume repeat if no function keys are pressed
  395            if [ "${FN_A_PRESSED}" = false ] && [ "${FN_B_PRESSED}" = false ]; then
  396              start_volume_repeat up
  397            else
  398              # If function keys are pressed, use the original behavior
  399              execute_action up
  400            fi
  401          elif [[ "${line}" =~ ${RELEASE} ]]; then
  402            ${DEBUG} && log $0 "Volume Up: Released"
  403            VOLUME_UP_PRESSED=false
  404            stop_volume_repeat
  405            if [ "${FN_A_PRESSED}" = false ] && [ "${FN_B_PRESSED}" = false ]; then
  406              CUR_VOLUME=$(get_setting "audio.volume")
  407              /usr/bin/mako-notify "Volume: ${CUR_VOLUME}%" -no-es
  408            fi
  409          fi
  410        ;;
  411        (${FUNCTION_VOLUME_DOWN_EVENT})
  412          if [[ "${line}" =~ ${PRESS} ]]; then
  413            ${DEBUG} && log $0 "Volume Down: Pressed"
  414            VOLUME_DOWN_PRESSED=true
  415            # Only start volume repeat if no function keys are pressed
  416            if [ "${FN_A_PRESSED}" = false ] && [ "${FN_B_PRESSED}" = false ]; then
  417              start_volume_repeat down
  418            else
  419              # If function keys are pressed, use the original behavior
  420              execute_action down
  421            fi
  422          elif [[ "${line}" =~ ${RELEASE} ]]; then
  423            ${DEBUG} && log $0 "Volume Down: Released"
  424            VOLUME_DOWN_PRESSED=false
  425            stop_volume_repeat
  426            if [ "${FN_A_PRESSED}" = false ] && [ "${FN_B_PRESSED}" = false ]; then
  427              CUR_VOLUME=$(get_setting "audio.volume")
  428              /usr/bin/mako-notify "Volume: ${CUR_VOLUME}%" -no-es
  429            fi
  430          fi
  431        ;;
  432        (${FUNCTION_POWER_PRESSED_EVENT})
  433          ${DEBUG} && log $0 "${FUNCTION_POWER_PRESSED_EVENT}: Pressed"
  434          /usr/bin/rocknix-fake-suspend power &
  435        ;;
  436        (${FUNCTION_LID_CLOSE_EVENT})
  437          ${DEBUG} && log $0 "${FUNCTION_LID_CLOSE_EVENT}: Close"
  438          /usr/bin/rocknix-fake-suspend lid close &
  439        ;;
  440        (${FUNCTION_LID_OPEN_EVENT})
  441          ${DEBUG} && log $0 "${FUNCTION_LID_OPEN_EVENT}: Open"
  442          /usr/bin/rocknix-fake-suspend lid open &
  443        ;;
  444      esac
  445  
  446      # Hotkey logic
  447      case ${line} in
  448        (${FUNCTION_HOTKEY_A_EVENT})
  449          if [[ "${line}" =~ ${PRESS} ]]; then
  450            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_A_EVENT}: Pressed"
  451            HOTKEY_A_PRESSED=true
  452          elif [[ "${line}" =~ ${RELEASE} ]]; then
  453            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_A_EVENT}: Released"
  454            HOTKEY_A_PRESSED=false
  455          fi
  456        ;;
  457        (${FUNCTION_HOTKEY_B_EVENT})
  458          if [[ "${line}" =~ ${PRESS} ]]; then
  459            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_B_EVENT}: Pressed"
  460            HOTKEY_B_PRESSED=true
  461            # Example: if A and C are also pressed => kill something
  462            if [ "${HOTKEY_A_PRESSED}" = true ] && [ "${HOTKEY_C_PRESSED}" = true ]; then
  463              execute_kill
  464            fi
  465          elif [[ "${line}" =~ ${RELEASE} ]]; then
  466            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_B_EVENT}: Released"
  467            HOTKEY_B_PRESSED=false
  468          fi
  469        ;;
  470        (${FUNCTION_HOTKEY_C_EVENT})
  471          if [[ "${line}" =~ ${PRESS} ]]; then
  472            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_C_EVENT}: Pressed"
  473            HOTKEY_C_PRESSED=true
  474            # Example: if A and B are also pressed => kill something
  475            if [ "${HOTKEY_A_PRESSED}" = true ] && [ "${HOTKEY_B_PRESSED}" = true ]; then
  476              execute_kill
  477            fi
  478          elif [[ "${line}" =~ ${RELEASE} ]]; then
  479            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_C_EVENT}: Released"
  480            HOTKEY_C_PRESSED=false
  481          fi
  482        ;;
  483        (${FUNCTION_HOTKEY_DPAD_UP_EVENT}|${FUNCTION_HOTKEY_HAT_UP_EVENT})
  484          if [ "${FN_A_PRESSED}" = true ] && [ "${DPAD_EVENTS}" = true ]; then
  485            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_DPAD_UP_EVENT}${FUNCTION_HOTKEY_HAT_UP_EVENT}: Volume Up"
  486            volume up
  487          fi
  488        ;;
  489        (${FUNCTION_HOTKEY_DPAD_DOWN_EVENT}|${FUNCTION_HOTKEY_HAT_DOWN_EVENT})
  490          if [ "${FN_A_PRESSED}" = true ] && [ "${DPAD_EVENTS}" = true ]; then
  491            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_DPAD_DOWN_EVENT}${FUNCTION_HOTKEY_HAT_DOWN_EVENT}: Volume Down"
  492            volume down
  493          fi
  494        ;;
  495        (${FUNCTION_HOTKEY_DPAD_RIGHT_EVENT}|${FUNCTION_HOTKEY_HAT_RIGHT_EVENT})
  496          if [ "${FN_A_PRESSED}" = true ] && [ "${DPAD_EVENTS}" = true ]; then
  497            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_DPAD_RIGHT_EVENT}${FUNCTION_HOTKEY_HAT_RIGHT_EVENT}: Brightness Up"
  498            brightness up
  499            CUR_BRIGHTNESS=$(get_setting "display.brightness")
  500            /usr/bin/mako-notify "Brightness: ${CUR_BRIGHTNESS}%" -no-es
  501          fi
  502        ;;
  503        (${FUNCTION_HOTKEY_DPAD_LEFT_EVENT}|${FUNCTION_HOTKEY_HAT_LEFT_EVENT})
  504          if [ "${FN_A_PRESSED}" = true ] && [ "${DPAD_EVENTS}" = true ]; then
  505            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_DPAD_LEFT_EVENT}${FUNCTION_HOTKEY_HAT_LEFT_EVENT}: Brightness Down"
  506            brightness down
  507            CUR_BRIGHTNESS=$(get_setting "display.brightness")
  508            /usr/bin/mako-notify "Brightness: ${CUR_BRIGHTNESS}%" -no-es
  509          fi
  510        ;;
  511        (${FUNCTION_HOTKEY_TOUCH_EVENT})
  512          if [ "${FN_A_PRESSED}" = true ] && [ "${TOUCHSCREEN_EVENTS}" = true ]; then
  513            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_TOUCH_EVENT}: Toggle Touchscreen Keyboard"
  514            kill -34 $(pidof wvkbd-mobintl)
  515          fi
  516        ;;
  517        (${FUNCTION_HOTKEY_BTN_EAST_EVENT})
  518          if [ "${HOTKEY_A_PRESSED}" = true ]; then
  519            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_BTN_EAST_EVENT}: Screenshot"
  520            /usr/bin/rocknix-screenshot
  521            # Display notification if 'success' exit code
  522            SCREENSHOT_SUCCESS=$?
  523            [ "$SCREENSHOT_SUCCESS" -eq 0 ] && /usr/bin/mako-notify "Screenshot Saved" -no-ra
  524          fi
  525        ;;
  526       (${FUNCTION_HOTKEY_BTN_WEST_EVENT})
  527          if [ "${HOTKEY_A_PRESSED}" = true ]; then
  528            ${DEBUG} && log $0 "${FUNCTION_HOTKEY_BTN_WEST_EVENT}: Config MangoHud"
  529            /usr/bin/mangohud_set toggle
  530          fi
  531        ;;
  532       (${FUNCTION_HOTKEY_BTN_NORTH_EVENT})
  533         if [ "${HOTKEY_A_PRESSED}" = true ]; then
  534           ${DEBUG} && log $0 "${FUNCTION_HOTKEY_BTN_NORTH_EVENT}: Opening Game Guide"
  535           /usr/bin/game-guides-tool
  536         fi
  537       ;;
  538    esac
  539  done
```

## File: sysutils/systemd/config/sysctl.d/rocknix.conf (at 8ebaf8daad, 3 lines)

```text
    1  vm.swappiness=1
    2  kernel.nmi_watchdog=0
    3  vm.dirty_writeback_centisecs=1500
```

## File: sysutils/systemd/config/system.conf.d/20-watchdog.conf (at 8ebaf8daad, 13 lines)

```text
    1  [Manager]
    2  # A kernel that has stopped scheduling is reset by the SoC's watchdog rather
    3  # than by somebody holding the power button -- which is what truncated two
    4  # config files on the RG SP (fork #102, #104; D-SYS-002). PID 1 pings it every
    5  # 7.5 s. 15 s because the Allwinner watchdog counts to 16 at most; a longer
    6  # figure is refused by the driver and systemd would then run with no watchdog
    7  # at all. A device without a watchdog device logs one line and carries on.
    8  RuntimeWatchdogSec=15s
    9  # Off on purpose. The same 16 s ceiling would have the shutdown watchdog
   10  # reset a device in the middle of a slow sync to the card, which is the very
   11  # corruption this is meant to prevent; systemd disarms the runtime watchdog
   12  # when it hands over to shutdown, so a hung shutdown behaves as it does today.
   13  RebootWatchdogSec=off
```

## File: sysutils/systemd/package.mk (at 8ebaf8daad, 333 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    3  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
    4  
    5  PKG_NAME="systemd"
    6  PKG_VERSION="255.8"
    7  PKG_SHA256="e770b9c4b5e36c1badf94444a27c9cd427931251009e4363f3239ad45ff75f3d"
    8  PKG_LICENSE="LGPL2.1+"
    9  PKG_SITE="http://www.freedesktop.org/wiki/Software/systemd"
   10  PKG_URL="https://github.com/systemd/systemd-stable/archive/v${PKG_VERSION}.tar.gz"
   11  PKG_DEPENDS_TARGET="toolchain libcap kmod util-linux libidn2 Python3:host Jinja2:host pcre2 zstd libgcrypt openssl"
   12  PKG_LONGDESC="A system and session manager for Linux, compatible with SysV and LSB init scripts."
   13  
   14  PKG_MESON_OPTS_TARGET="--libdir=/usr/lib \
   15                         -Drootprefix=/usr \
   16                         -Dsplit-usr=false \
   17                         -Dsplit-bin=true \
   18                         -Ddefault-hierarchy=hybrid \
   19                         -Dtty-gid=5 \
   20                         -Dtests=false \
   21                         -Dseccomp=false \
   22                         -Dselinux=false \
   23                         -Dapparmor=false \
   24                         -Dpolkit=false \
   25                         -Dacl=false \
   26                         -Daudit=false \
   27                         -Dblkid=true \
   28                         -Dfdisk=false \
   29                         -Dkmod=true \
   30                         -Dpam=false \
   31                         -Dpwquality=false \
   32                         -Dmicrohttpd=false \
   33                         -Dlibcryptsetup=false \
   34                         -Dlibcurl=false \
   35                         -Dlibidn=false \
   36                         -Dlibidn2=true \
   37                         -Dlibiptc=false \
   38                         -Dqrencode=false \
   39                         -Dgcrypt=true \
   40                         -Dgnutls=false \
   41                         -Dopenssl=true \
   42                         -Dp11kit=false \
   43                         -Delfutils=false \
   44                         -Dzlib=false \
   45                         -Dbzip2=false \
   46                         -Dxz=false \
   47                         -Dlz4=false \
   48                         -Dxkbcommon=false \
   49                         -Dpcre2=true \
   50                         -Dglib=false \
   51                         -Ddbus=false \
   52                         -Ddefault-dnssec=no \
   53                         -Dimportd=false \
   54                         -Dremote=false \
   55                         -Dutmp=true \
   56                         -Dhibernate=false \
   57                         -Denvironment-d=false \
   58                         -Dbinfmt=true \
   59                         -Drepart=false \
   60                         -Dcoredump=false \
   61                         -Dresolve=true \
   62                         -Dlogind=true \
   63                         -Dhostnamed=true \
   64                         -Dlocaled=false \
   65                         -Dmachined=false \
   66                         -Dportabled=false \
   67                         -Duserdb=false \
   68                         -Dhomed=false \
   69                         -Dnetworkd=false \
   70                         -Dtimedated=true \
   71                         -Dtimesyncd=true \
   72                         -Dfirstboot=false \
   73                         -Drandomseed=false \
   74                         -Dbacklight=false \
   75                         -Dvconsole=false \
   76                         -Dquotacheck=false \
   77                         -Dsysusers=false \
   78                         -Dtmpfiles=true \
   79                         -Dhwdb=true \
   80                         -Drfkill=true \
   81                         -Dldconfig=false \
   82                         -Defi=false \
   83                         -Dtpm=false \
   84                         -Dima=false \
   85                         -Dsmack=false \
   86                         -Dgshadow=false \
   87                         -Didn=false \
   88                         -Dnss-myhostname=false \
   89                         -Dnss-mymachines=false \
   90                         -Dnss-resolve=true \
   91                         -Dnss-systemd=false \
   92                         -Dman=false \
   93                         -Dhtml=false \
   94                         -Dlink-udev-shared=true \
   95                         -Dlink-systemctl-shared=true \
   96                         -Dlink-networkd-shared=false \
   97                         -Dbashcompletiondir=no \
   98                         -Dzshcompletiondir=no \
   99                         -Dkmod-path=/usr/bin/kmod \
  100                         -Dmount-path=/usr/bin/mount \
  101                         -Dumount-path=/usr/bin/umount \
  102                         -Dversion-tag=${PKG_VERSION} \
  103                         -Dc_args=-D__counted_by\(x\)\= \
  104                         -Dcpp_args=-D__counted_by\(x\)\="
  105  if [ -n "${BUILD_WITH_DEBUG}" ]
  106  then
  107    PKG_MESON_OPTS_TARGET+=" -Ddebug-tty=${DEBUG_TTY}"
  108  fi
  109  
  110  pre_configure_target() {
  111    export TARGET_CFLAGS=$(echo ${TARGET_CFLAGS} | sed -e "s|-O.|-O3|g")
  112  
  113    export TARGET_LDFLAGS=$(echo ${TARGET_LDFLAGS} | sed -e "s|-O.|-O3|g")
  114  
  115    export TARGET_CFLAGS="${TARGET_CFLAGS} -fno-schedule-insns -fno-schedule-insns2 -Wno-format-truncation"
  116    export LC_ALL=en_US.UTF-8
  117  }
  118  
  119  post_makeinstall_target() {
  120    # remove unneeded stuff
  121    safe_remove ${INSTALL}/etc/init.d
  122    safe_remove ${INSTALL}/etc/systemd/system
  123    safe_remove ${INSTALL}/etc/xdg
  124    safe_remove ${INSTALL}/etc/X11
  125    safe_remove ${INSTALL}/usr/bin/kernel-install
  126    safe_remove ${INSTALL}/usr/lib/kernel/install.d
  127    safe_remove ${INSTALL}/usr/lib/rpm
  128    safe_remove ${INSTALL}/usr/lib/systemd/user
  129    safe_remove ${INSTALL}/usr/lib/tmpfiles.d/etc.conf
  130    safe_remove ${INSTALL}/usr/lib/tmpfiles.d/home.conf
  131    safe_remove ${INSTALL}/usr/share/factory
  132  
  133    # remove Network adaper renaming rule, this is confusing
  134    safe_remove ${INSTALL}/usr/lib/udev/rules.d/80-net-setup-link.rules
  135  
  136    safe_remove ${INSTALL}/usr/lib/udev/rules.d/71-seat.rules
  137    safe_remove ${INSTALL}/usr/lib/udev/rules.d/73-seat-late.rules
  138  
  139    # remove getty units, we dont want a console
  140    safe_remove ${INSTALL}/usr/lib/systemd/system/autovt@.service
  141    safe_remove ${INSTALL}/usr/lib/systemd/system/console-getty.service
  142    safe_remove ${INSTALL}/usr/lib/systemd/system/container-getty@.service
  143    safe_remove ${INSTALL}/usr/lib/systemd/system/getty.target
  144    safe_remove ${INSTALL}/usr/lib/systemd/system/getty@.service
  145    safe_remove ${INSTALL}/usr/lib/systemd/system/serial-getty@.service
  146    safe_remove ${INSTALL}/usr/lib/systemd/system/*.target.wants/getty.target
  147  
  148    # remove other notused or nonsense stuff (our /etc is ro)
  149    safe_remove ${INSTALL}/usr/lib/systemd/systemd-update-done
  150    safe_remove ${INSTALL}/usr/lib/systemd/system/systemd-update-done.service
  151    safe_remove ${INSTALL}/usr/lib/systemd/system/*.target.wants/systemd-update-done.service
  152  
  153    safe_remove ${INSTALL}/usr/lib/systemd/system/dev-hugepages.mount
  154    safe_remove ${INSTALL}/usr/lib/systemd/system/*.target.wants/dev-hugepages.mount
  155  
  156    safe_remove ${INSTALL}/usr/lib/systemd/system/systemd-journald-audit.socket
  157  
  158    # adjust systemd-hwdb-update (we have read-only /etc).
  159    sed '/^ConditionNeedsUpdate=.*$/d' -i ${INSTALL}/usr/lib/systemd/system/systemd-hwdb-update.service
  160  
  161    # remove nspawn
  162    safe_remove ${INSTALL}/usr/bin/systemd-nspawn
  163    safe_remove ${INSTALL}/usr/lib/systemd/system/systemd-nspawn@.service
  164  
  165    # remove unneeded generators
  166    for gen in ${INSTALL}/usr/lib/systemd/system-generators/*; do
  167      case "${gen}" in
  168        */systemd-debug-generator)
  169          # keep it
  170          ;;
  171        *)
  172          safe_remove "${gen}"
  173          ;;
  174      esac
  175    done
  176  
  177    # remove catalog
  178    safe_remove ${INSTALL}/usr/lib/systemd/catalog
  179  
  180    # remove partition
  181    safe_remove ${INSTALL}/usr/lib/systemd/systemd-growfs
  182    safe_remove ${INSTALL}/usr/lib/systemd/systemd-makefs
  183  
  184    # distro preset policy
  185    safe_remove ${INSTALL}/usr/lib/systemd/system-preset/*
  186    echo "disable *" > ${INSTALL}/usr/lib/systemd/system-preset/99-default.preset
  187  
  188    safe_remove ${INSTALL}/usr/lib/systemd/user-preset/*
  189    echo "disable *" > ${INSTALL}/usr/lib/systemd/user-preset/90-systemd.preset
  190  
  191    # remove networkd
  192    safe_remove ${INSTALL}/usr/lib/systemd/network
  193  
  194    # remove systemd-time-wait-sync (not detecting slew time updates, using package wait-time-sync)
  195    safe_remove ${INSTALL}/usr/lib/systemd/system/systemd-time-wait-sync.service
  196    safe_remove ${INSTALL}/usr/lib/systemd/systemd-time-wait-sync
  197  
  198    # tune journald.conf
  199    sed -e "s,^.*Compress=.*$,Compress=no,g" -i ${INSTALL}/etc/systemd/journald.conf
  200    sed -e "s,^.*MaxFileSec=.*$,MaxFileSec=0,g" -i ${INSTALL}/etc/systemd/journald.conf
  201    sed -e "s,^.*MaxRetentionSec=.*$,MaxRetentionSec=0,g" -i ${INSTALL}/etc/systemd/journald.conf
  202    sed -e "s,^.*RuntimeMaxUse=.*$,RuntimeMaxUse=2M,g" -i ${INSTALL}/etc/systemd/journald.conf
  203    sed -e "s,^.*RuntimeMaxFileSize=.*$,RuntimeMaxFileSize=128K,g" -i ${INSTALL}/etc/systemd/journald.conf
  204    sed -e "s,^.*SplitMode=.*$,SplitMode=none,g" -i ${INSTALL}/etc/systemd/journald.conf
  205    # The journal is persistent since fork #104 (var-log.mount binds /var/log to
  206    # /storage/.cache/log), so these are limits on the card, not on RAM: 64M
  207    # holds days of an ordinary device's logging, and the journal is synced to
  208    # disk every minute rather than every five, so a freeze costs at most the
  209    # last minute of low-priority lines (crit and above are synced at once).
  210    sed -e "s,^.*SystemMaxUse=.*$,SystemMaxUse=64M,g" -i ${INSTALL}/etc/systemd/journald.conf
  211    sed -e "s,^.*SyncIntervalSec=.*$,SyncIntervalSec=1min,g" -i ${INSTALL}/etc/systemd/journald.conf
  212    if [ "${BUILD_WITH_DEBUG}" = "yes" ]; then
  213      sed -e "s,^.*ForwardToConsole=.*$,ForwardToConsole=yes,g" -i ${INSTALL}/etc/systemd/journald.conf
  214      sed -e "s,^.*TTYPath=.*$,TTYPath=${DEBUG_TTY},g" -i ${INSTALL}/etc/systemd/journald.conf
  215    fi
  216  
  217    # tune logind.conf
  218    sed -e "s,^.*HandleLidSwitch=.*$,HandleLidSwitch=suspend,g" -i ${INSTALL}/etc/systemd/logind.conf
  219    sed -e "s,^.*HandlePowerKey=.*$,HandlePowerKey=suspend,g" -i ${INSTALL}/etc/systemd/logind.conf
  220  
  221    # SYSTEMD-RESOLVED CONFIGURATION
  222    sed -i 's/^#MulticastDNS=yes/MulticastDNS=no/' ${INSTALL}/etc/systemd/resolved.conf || echo "MulticastDNS=no" >> ${INSTALL}/etc/systemd/resolved.conf
  223    # FALLBACK DNS (Mixed Google/Cloudflare Anycast)
  224    sed -i 's/^#FallbackDNS=.*/FallbackDNS=8.8.8.8 1.1.1.1 2001:4860:4860::8888 2606:4700:4700::1111/' ${INSTALL}/etc/systemd/resolved.conf || echo "FallbackDNS=8.8.8.8 1.1.1.1 2001:4860:4860::8888 2606:4700:4700::1111" >> ${INSTALL}/etc/systemd/resolved.conf
  225  
  226    # replace systemd-machine-id-setup with ours
  227    safe_remove ${INSTALL}/usr/lib/systemd/system/systemd-machine-id-commit.service
  228    safe_remove ${INSTALL}/usr/lib/systemd/system/*.target.wants/systemd-machine-id-commit.service
  229    safe_remove ${INSTALL}/usr/bin/systemd-machine-id-setup
  230    mkdir -p ${INSTALL}/usr/bin
  231    cp ${PKG_DIR}/scripts/systemd-machine-id-setup ${INSTALL}/usr/bin
  232    cp ${PKG_DIR}/scripts/userconfig-setup ${INSTALL}/usr/bin
  233    cp ${PKG_DIR}/scripts/usercache-setup ${INSTALL}/usr/bin
  234  
  235    mkdir -p ${INSTALL}/usr/sbin
  236    cp ${PKG_DIR}/scripts/network-base-setup ${INSTALL}/usr/sbin
  237    cp ${PKG_DIR}/scripts/systemd-timesyncd-setup ${INSTALL}/usr/sbin
  238  
  239    # /etc/resolv.conf and /etc/hosts must be writable
  240    ln -sf /run/rocknix/resolv.conf ${INSTALL}/etc/resolv.conf
  241    ln -sf /run/rocknix/hosts ${INSTALL}/etc/hosts
  242  
  243    # provide 'halt', 'shutdown', 'reboot' & co.
  244    ln -sf /usr/bin/systemctl ${INSTALL}/usr/sbin/halt
  245    ln -sf /usr/bin/systemctl ${INSTALL}/usr/sbin/poweroff
  246    ln -sf /usr/bin/systemctl ${INSTALL}/usr/sbin/reboot
  247    ln -sf /usr/bin/systemctl ${INSTALL}/usr/sbin/runlevel
  248    ln -sf /usr/bin/systemctl ${INSTALL}/usr/sbin/shutdown
  249    ln -sf /usr/bin/systemctl ${INSTALL}/usr/sbin/telinit
  250  
  251    # strip
  252    debug_strip ${INSTALL}/usr
  253  
  254    # defaults
  255    mkdir -p ${INSTALL}/usr/config
  256    cp -PR ${PKG_DIR}/config/* ${INSTALL}/usr/config
  257  
  258    safe_remove ${INSTALL}/etc/modules-load.d
  259    ln -sf /storage/.config/modules-load.d ${INSTALL}/etc/modules-load.d
  260    ln -sf /storage/.config/logind.conf.d ${INSTALL}/etc/systemd/logind.conf.d
  261    ln -sf /storage/.config/resolved.conf.d ${INSTALL}/etc/systemd/resolved.conf.d
  262    ln -sf /storage/.config/sleep.conf.d ${INSTALL}/etc/systemd/sleep.conf.d
  263    ln -sf /storage/.config/timesyncd.conf.d ${INSTALL}/etc/systemd/timesyncd.conf.d
  264    safe_remove ${INSTALL}/etc/sysctl.d
  265    ln -sf /storage/.config/sysctl.d ${INSTALL}/etc/sysctl.d
  266    safe_remove ${INSTALL}/etc/tmpfiles.d
  267    ln -sf /storage/.config/tmpfiles.d ${INSTALL}/etc/tmpfiles.d
  268    safe_remove ${INSTALL}/etc/udev/hwdb.d
  269    ln -sf /storage/.config/hwdb.d ${INSTALL}/etc/udev/hwdb.d
  270    safe_remove ${INSTALL}/etc/udev/rules.d
  271    ln -sf /storage/.config/udev.rules.d ${INSTALL}/etc/udev/rules.d
  272  
  273    # system manager timeout overrides
  274    mkdir -p ${INSTALL}/etc/systemd/system.conf.d
  275    cp -PR ${PKG_DIR}/config/system.conf.d/* ${INSTALL}/etc/systemd/system.conf.d/
  276  
  277    # journald
  278    ln -sf /storage/.cache/journald.conf.d ${INSTALL}/usr/lib/systemd/journald.conf.d
  279  
  280    # systemd-pstore's archive directory is a symlink into /storage (tmpfiles
  281    # z_01_rocknix.conf, fork #104). systemd's own tmpfiles line creates it as
  282    # a plain directory, sorts first, and tmpfiles ignores the later line for
  283    # the same path as a duplicate -- so the symlink was never made and the
  284    # dump was archived into tmpfs (VM, 2026-09-10). One line for the path.
  285    sed -e '/^d \/var\/lib\/systemd\/pstore/d' -i ${INSTALL}/usr/lib/tmpfiles.d/systemd-pstore.conf
  286  }
  287  
  288  post_install() {
  289    add_group systemd-journal 190
  290  
  291    add_group systemd-timesync 191
  292    add_user systemd-timesync x 191 191 "systemd-timesync" "/" "/bin/false"
  293  
  294    add_group systemd-network 193
  295    add_user systemd-network x 193 193 "systemd-network" "/" "/bin/sh"
  296  
  297    add_group systemd-oom 194
  298    add_user systemd-oom x 194 194 "systemd Userspace OOM Killer" "/" "/bin/false"
  299  
  300    add_group systemd-resolve 192
  301    add_user systemd-resolve x 192 192 "systemd-resolve" "/" "/bin/false"
  302  
  303    add_group adm 4
  304    add_group tty 5
  305    add_group disk 6
  306    add_group lp 7
  307    add_group kmem 9
  308    add_group wheel 10
  309    add_group cdrom 11
  310    add_group dialout 18
  311    add_group floppy 19
  312    add_group utmp 22
  313    add_group tape 33
  314    add_group kvm 36
  315    add_group video 39 pipewire
  316    add_group audio 63 pipewire
  317    add_group input 104
  318    add_group render 105
  319    add_group sgx 106
  320    add_group users 100
  321    add_group nogroup 65534
  322    add_user nobody x 65534 65534 "nobody" "/" "/bin/false"
  323  
  324    enable_service machine-id.service
  325    enable_service debugconfig.service
  326    enable_service userconfig.service
  327    enable_service usercache.service
  328    enable_service network-base.service
  329    enable_service systemd-timesyncd.service
  330    enable_service systemd-timesyncd-setup.service
  331    enable_service systemd-resolved.service
  332    enable_service debug-shell.service
  333  }
```

## File: sysutils/systemd/scripts/network-base-setup (at 8ebaf8daad, 129 lines)

```text
    1  #!/bin/sh
    2  . /etc/profile
    3  # The device name is the player's; the network's rules are ours to satisfy
    4  # quietly. system.hostname keeps whatever was typed -- spaces, punctuation,
    5  # anything -- and this applies the form the network accepts (clean_hostname:
    6  # letters, digits, hyphens). It is NOT written back: the name the player gave
    7  # the device stays theirs, and EmulationStation shows the applied form under
    8  # the IP address so somebody who sees RG-SP on their router can find out why
    9  # (maintainer, fork #106).
   10  #
   11  # NetworkManager is told not to touch the hostname (hostname-mode=none), so
   12  # this is the only writer. Quoted throughout: "RG SP" unquoted once reached
   13  # the setter as two arguments and failed, leaving a kernel name that
   14  # hostnamed later re-sanitised to RGSP.
   15  RAW_HOSTNAME=$(get_setting system.hostname)
   16  # A per-unit default (fork #50). The image ships system.hostname as the
   17  # build family -- H700, RK3566 -- so two units of one family on one network
   18  # claimed the same name and the router's lease flipped between them, and
   19  # the failure looked like a network fault (EHOSTUNREACH by name and by the
   20  # address the router showed). A name equal to the family is the shipped
   21  # default and never something a player typed, so it becomes
   22  # <FAMILY>-<four hex digits of this unit's id>, once, and is written back:
   23  # stable across boots, what NETWORK SETTINGS shows, and the same after a
   24  # reflash, because cloud_device_id seeds the id from the permanent hardware
   25  # address. Any other name is the player's and is never touched (D-NET-001).
   26  # An empty name gets the same default rather than the bare ROCKNIX below.
   27  FAMILY=$(sed -n 's/^HW_DEVICE="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' /etc/os-release 2>/dev/null | head -1)
   28  SHIPPED=""
   29  if [ -z "${RAW_HOSTNAME}" ] || { [ -n "${FAMILY}" ] && [ "${RAW_HOSTNAME}" = "${FAMILY}" ]; }; then
   30    SHIPPED="the shipped default (${FAMILY:-empty})"
   31  else
   32    # The generated shape with another unit's digits is another unit's shipped
   33    # default, carried here by a settings restore (#151 PL-02, D-NET-004):
   34    # unit A boots as H700-9a3f, the player restores A's settings on unit B --
   35    # the fresh-handheld journey -- and B's system.cfg says H700-9a3f, neither
   36    # the family nor empty, so it read as the player's and both units kept one
   37    # name, permanently where before it was per boot. The shape is the family
   38    # as the network spells it (GENERIC_X64 is GENERIC-X64), a hyphen and four
   39    # hex digits; whose digits they are is decided below, once this unit's own
   40    # are known. A name of another family's shape is left alone, as the bare
   41    # family is. A player who typed exactly this shape with digits not their
   42    # unit's loses it, as one who typed the bare family does (D-NET-002).
   43    case "${RAW_HOSTNAME}" in
   44      "$(clean_hostname "${FAMILY:-ROCKNIX}")"-[0-9a-f][0-9a-f][0-9a-f][0-9a-f]) SHIPPED="another unit's shipped default (${RAW_HOSTNAME}), carried here by a settings restore" ;;
   45    esac
   46  fi
   47  if [ -n "${SHIPPED}" ]; then
   48    # The stored id, or the adapter's, or nothing. This runs at ~2 s of the
   49    # first boot, before a handheld's SDIO wifi is an interface, and a plain
   50    # cloud_device_id there would seed the identity from machine-id and keep
   51    # it ("the stored value wins") -- a different id from the one a reflash
   52    # that finds the adapter derives, so the name and the cloud folder would
   53    # depend on boot timing (#151 PL-04, D-NET-005). --if-present never seeds:
   54    # with nothing to say, the shipped name stays for this boot, the log says
   55    # so, and the next boot asks again. An id with no hex in it is logged too
   56    # rather than passed over in silence.
   57    UNIT_ID=$(cloud_device_id --if-present 2>/dev/null)
   58    UNIT=$(printf '%s' "${UNIT_ID##*-}" | tr -cd 'a-f0-9' | cut -c1-4)
   59    if [ -n "${UNIT}" ]; then
   60      OWN=$(clean_hostname "${FAMILY:-ROCKNIX}-${UNIT}")
   61      if [ "${RAW_HOSTNAME}" != "${OWN}" ]; then
   62        RAW_HOSTNAME="${OWN}"
   63        set_setting system.hostname "${RAW_HOSTNAME}"
   64        logger -t network-base-setup "device name was ${SHIPPED}; it is now ${RAW_HOSTNAME}, this unit's own"
   65      fi
   66    elif [ -z "${UNIT_ID}" ]; then
   67      logger -t network-base-setup "adapter not present yet, keeping the shipped name (${RAW_HOSTNAME:-${FAMILY:-ROCKNIX}}) for a later boot"
   68    else
   69      logger -t network-base-setup "device id ${UNIT_ID} carries no hex digits; keeping the shipped name (${RAW_HOSTNAME:-${FAMILY:-ROCKNIX}})"
   70    fi
   71  fi
   72  HOSTNAME=$(clean_hostname "${RAW_HOSTNAME}")
   73  if [ -z "${HOSTNAME}" ]; then
   74    HOSTNAME="ROCKNIX"
   75  fi
   76  if [ "${HOSTNAME}" != "${RAW_HOSTNAME}" ]; then
   77    logger -t network-base-setup "device name '${RAW_HOSTNAME}' is '${HOSTNAME}' on the network (letters, digits and hyphens only)"
   78  fi
   79  echo "${HOSTNAME}" >/proc/sys/kernel/hostname
   80  # No hostnamectl here. /etc/hostname is a symlink to /proc/sys/kernel/hostname,
   81  # so systemd-hostnamed reads the kernel's name at ITS start as the static
   82  # name and refuses a transient one ("static hostname is already set") --
   83  # and answering that call is when it puts its cached name back over the
   84  # kernel's. When hostnamed had started first (NetworkManager activates it
   85  # over D-Bus) the call above undid the write above, and the device spent
   86  # the boot as ROCKNIX. The write is the whole job; the unit now orders
   87  # this before hostnamed and NetworkManager so they read the written name.
   88  #
   89  # The mDNS responder publishes the kernel's name as it finds it when it
   90  # starts, and its unit orders after this one, so on a boot in order it reads
   91  # the name just written and needs no telling. The boot that is not in order
   92  # -- the daemon already up when this runs, as on the image that shipped
   93  # avahi's stock unit with no ordering and published ROCKNIX.local for a
   94  # device named GENERIC-X64-0964 (#151 PL-01) -- is told the name. Only a
   95  # daemon that answers -c is told: calling avahi-set-host-name against one
   96  # that is not running failed on every boot ("Daemon not running"), which is
   97  # why the unguarded call was removed; a daemon that is not up yet is a log
   98  # line, and it publishes the written name itself when it starts.
   99  if ! command -v avahi-daemon >/dev/null 2>&1; then
  100    : # no responder in this image
  101  elif avahi-daemon -c 2>/dev/null; then
  102    if avahi-set-host-name "${HOSTNAME}" >/dev/null 2>&1; then
  103      logger -t network-base-setup "mDNS responder was already up; it now publishes ${HOSTNAME}.local"
  104    else
  105      logger -t network-base-setup "mDNS responder is up but could not be told ${HOSTNAME}; it publishes the name it read at its start"
  106    fi
  107  else
  108    logger -t network-base-setup "mDNS responder not up yet; it publishes ${HOSTNAME}.local when it starts"
  109  fi
  110  
  111  rm -f /run/rocknix/hosts
  112  if [ -f /storage/.config/hosts.conf ]; then
  113    cat /storage/.config/hosts.conf > /run/rocknix/hosts
  114  fi
  115  
  116  # RESOLUTION ORDER:
  117  # 1. USER OVERRIDE: /storage/.config/resolv.conf exists -> Use it directly.
  118  # 2. DYNAMIC/STUB:  No override -> Symlink to systemd-resolved stub.
  119  if [ -f /storage/.config/resolv.conf ]; then
  120    rm -f /run/rocknix/resolv.conf
  121    cat /storage/.config/resolv.conf > /run/rocknix/resolv.conf
  122  else
  123    TARGET="/run/systemd/resolve/stub-resolv.conf"
  124    LINK="/run/rocknix/resolv.conf"
  125    if [ ! -L "$LINK" ] || [ "$(readlink "$LINK")" != "$TARGET" ]; then
  126        rm -f "$LINK"
  127        ln -sf "$TARGET" "$LINK"
  128    fi
  129  fi
```

## File: sysutils/systemd/system.d/systemd-pstore.service.d/rocknix.conf (at 8ebaf8daad, 8 lines)

```text
    1  [Unit]
    2  # The archive directory is a symlink into /storage/.cache/log, made by
    3  # systemd-tmpfiles (z_01_rocknix.conf); the stock unit is ordered only after
    4  # the efi_pstore module and would race it, copying into a tmpfs directory
    5  # that the symlink then replaces -- the evidence copied and lost in one boot
    6  # (fork #104). storage-log.service creates the symlink's target.
    7  After=systemd-tmpfiles-setup.service storage-log.service
    8  Wants=storage-log.service
```

## File: sysutils/systemd/tmpfiles.d/z_01_rocknix.conf (at 8ebaf8daad, 12 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2009-2014 Stephan Raue (stephan@openelec.tv)
    3  
    4  d    /run/rocknix       0755 root root - -
    5  d    /run/rocknix/debug 0755 root root - -
    6  d    /storage/.cache/rfkill 0755 root root - -
    7  L+   /var/lib/systemd/rfkill  -  -    -    - /storage/.cache/rfkill
    8  # systemd-pstore copies a crash's kernel log out of /sys/fs/pstore into
    9  # /var/lib/systemd/pstore, which is tmpfs here -- so the copy would die with
   10  # the next power cycle exactly as the original would have. Point it into the
   11  # persistent log tree (fork #104). storage-log.service creates the target.
   12  L+   /var/lib/systemd/pstore  -  -    -    - /storage/.cache/log/pstore
```

## Excerpt: sysutils/busybox/config/busybox-target.conf (at 8ebaf8daad; the flagged lines (SUID, LOGIN, PASSWD, SU, HTTPD, CGI, NC, UDHCPD), not its 1,224 lines)

```text
   28  CONFIG_FEATURE_INSTALLER=y
   29  CONFIG_INSTALL_NO_USR=y
   30  CONFIG_FEATURE_SUID=y
   31  # CONFIG_FEATURE_SUID_CONFIG is not set
   32  # CONFIG_FEATURE_SUID_CONFIG_QUIET is not set
  ...
  547  # CONFIG_FEATURE_DEL_USER_FROM_GROUP is not set
  548  # CONFIG_GETTY is not set
  549  CONFIG_LOGIN=y
  550  # CONFIG_LOGIN_SESSION_AS_CHILD is not set
  551  CONFIG_LOGIN_SCRIPTS=y
  552  # CONFIG_FEATURE_NOLOGIN is not set
  553  # CONFIG_FEATURE_SECURETTY is not set
  554  CONFIG_PASSWD=y
  555  CONFIG_FEATURE_PASSWD_WEAK_CHECK=y
  556  CONFIG_SU=y
  557  CONFIG_FEATURE_SU_SYSLOG=y
  558  CONFIG_FEATURE_SU_CHECKS_SHELLS=y
  ...
  886  CONFIG_HOSTNAME=y
  887  CONFIG_DNSDOMAINNAME=y
  888  CONFIG_HTTPD=y
  889  CONFIG_FEATURE_HTTPD_PORT_DEFAULT=80
  890  CONFIG_FEATURE_HTTPD_RANGES=y
  891  CONFIG_FEATURE_HTTPD_SETUID=y
  892  CONFIG_FEATURE_HTTPD_BASIC_AUTH=y
  893  CONFIG_FEATURE_HTTPD_AUTH_MD5=y
  894  CONFIG_FEATURE_HTTPD_CGI=y
  895  CONFIG_FEATURE_HTTPD_CONFIG_WITH_SCRIPT_INTERPR=y
  896  CONFIG_FEATURE_HTTPD_SET_REMOTE_PORT_TO_ENV=y
  ...
  948  # CONFIG_FEATURE_NAMEIF_EXTENDED is not set
  949  CONFIG_NBDCLIENT=y
  950  CONFIG_NC=y
  951  # CONFIG_NETCAT is not set
  952  CONFIG_NC_SERVER=y
  ...
 1008  CONFIG_WHOIS=y
 1009  # CONFIG_ZCIP is not set
 1010  CONFIG_UDHCPD=y
 1011  # CONFIG_FEATURE_UDHCPD_BASE_IP_ON_MAC is not set
 1012  # CONFIG_FEATURE_UDHCPD_WRITE_LEASES_EARLY is not set
```

## Excerpt: sysutils/udevil/config/udevil.conf (at 8ebaf8daad; the default and allowed options (F-04))

```text
  200  # a link to a file will have no effect.
  201  forbidden_files =
  202  
  203  
  204  # default_options specifies what options are always included when performing
  205  # a mount, in addition to any options the user may specify.
  206  # Note:  When a device is present in /etc/fstab, and the user does not specify
  207  # a mount point, the device is mounted with normal user permissions using
  208  # the fstab entry, without these options.
  209  # default_options_FSTYPE, if present, is used to override default_options
  210  # when mounting a specific fstype (eg ext2, nfs).
  211  # The variables $USER, $UID, and $GID are changed to the user's username, UID,
  212  # and GID.
  213  # FOR GOOD SECURITY, default_options SHOULD ALWAYS INCLUDE: nosuid,noexec,nodev
  214  # WARNING:  OPTIONS PRESENT OR MISSING CAN CAUSE SERIOUS SECURITY PROBLEMS.
  215  default_options           = nosuid, noexec, nodev, noatime
  216  default_options_file      = nosuid, noexec, nodev, noatime, uid=$UID, gid=$GID, ro
  217  # mount iso9660 with 'ro' to prevent mount read-only warning
  218  default_options_iso9660   = nosuid, noexec, nodev, noatime, uid=$UID, gid=$GID, ro, utf8
  219  default_options_udf       = nosuid, noexec, nodev, noatime, uid=$UID, gid=$GID
  220  default_options_vfat      = nosuid, noexec, nodev, noatime, fmask=0133, dmask=0022, uid=$UID, gid=$GID, utf8
  221  default_options_exfat     = nosuid, noexec, nodev, noatime
  222  default_options_msdos     = nosuid, noexec, nodev, noatime, fmask=0133, dmask=0022, uid=$UID, gid=$GID
  223  default_options_umsdos    = nosuid, noexec, nodev, noatime, fmask=0133, dmask=0022, uid=$UID, gid=$GID
  224  default_options_ntfs      = nosuid, noexec, nodev, noatime, fmask=0133, uid=$UID, gid=$GID
  225  default_options_cifs      = nosuid, noexec, nodev, uid=$UID, gid=$GID
  226  default_options_smbfs     = nosuid, noexec, nodev, uid=$UID, gid=$GID
  227  default_options_sshfs     = nosuid, noexec, nodev, noatime, uid=$UID, gid=$GID, nonempty, allow_other
  228  default_options_curlftpfs = nosuid, noexec, nodev, noatime, uid=$UID, gid=$GID, nonempty, allow_other
  229  default_options_ftpfs     = nosuid, noexec, nodev, noatime, uid=$UID, gid=$GID
  230  default_options_davfs     = nosuid, noexec, nodev, uid=$UID, gid=$GID
  231  default_options_tmpfs     = nosuid, noexec, nodev, noatime, uid=$UID, gid=$GID
  232  default_options_ramfs     = nosuid, noexec, nodev, noatime, uid=$UID, gid=$GID
  233  default_options_btrfs     = compress=zstd:3
  234  
  235  # allowed_options determines all options that a user may specify when mounting.
  236  # All the options used in default_options above must be included here too, or
  237  # they will be rejected.  If the user attempts to use an option not included
  238  # here, an error will result.  Wildcards may be used.
  239  # allowed_options_FSTYPE, if present, is used to override allowed_options
  240  # when mounting a specific fstype (eg ext2, nfs).
  241  # The variables $USER, $UID, and $GID are changed to the user's username, UID,
  242  # and GID.
  243  # If you want to forbid remounts, remove 'remount' from here.
  244  # WARNING:  OPTIONS HERE CAN CAUSE SERIOUS SECURITY PROBLEMS - CHOOSE CAREFULLY
  245  allowed_options           = nosuid, noexec, nodev, noatime, big_writes, fmask=0133, dmask=0022, uid=$UID, gid=$GID, ro, rw, sync, flush, iocharset=*, utf8, remount
```