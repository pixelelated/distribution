# Audit Analysis — M6.P2 T1, the OS scripts: launch, control and state

**Date:** 2026-10-23
**Spec:** `docs/reviews/briefs/os-launch-control-state.md` v2; `docs/reviews/plan-for-the-plan.md` § 4
**Issues:** #648, #695, #339
**Commits:** read at `reviewed-at` `efadfea08a` (slice bytes = `8ebaf8daad`); `upstream/next` for Q4 `8b70f693b8`; image `069fc270442134fe771258418adf4e666e0473fb`

---

## Executive Summary

T1 read the 83 paths of `projects/ROCKNIX/packages/rocknix/` (less `backuptool`) -- 13,327 lines, 29 fork-own and 54 upstream-carried -- at `8ebaf8daad`, under the code-auditor lifecycle with the renovation face, and proved every behaviour claim it could on a GENERIC_X64 guest booted from the M7 lane's newest image. It found **68 findings: 0 Critical, 0 High, 19 Medium, 49 Low**; 18 are proven on the guest, three are already fixed upstream (Q4), and the rest are traces with `file:line` or device-only leads named as such.

The fork's own state layer -- the settings writers and lock, `chksysconfig`, `rocknix-evidence`, `rocknix-corekeep` -- is sound under its tests and every refutation. The defects concentrate in the launch path's inherited middle and in upstream-carried scripts: `setsettings.sh` truncates the Gambatte and MAME 2003-Plus option files at every launch (F-16, F-17), reads `neogeo` as `neogeocd` (F-10), can lose its staged clears to a race (F-11) and ignores an explicit value (F-09); a typed netplay host reaches `runemu.sh`'s `eval` as root (F-14, #275's class through a second door); per-game settings are lost for any ROM whose name carries `[` (F-21); `runemu.sh` executes a governor name the H700 offers without a function (F-01). Guards that report success over a failure recur (F-29 `setrootpass`, F-40 `installtointernal`, F-67 `updateabl`). `post-update` resets a player's DPMS choice at every update (F-44) and is one of the last unguarded writers of `system.cfg` (F-32). On x86_64, `008-perfmode` stops at its third line at every boot (F-58). Ten scripts are unreached (Q6).

Two time-to-play numbers were measured (0.64 s and 1.01 s, against #336's stale 1.05 s and 2.03 s), `setsettings.sh` costs 127 ms a launch at the engineering image's verbose loglevel (99 ms at none), and all 43 upstream commits on the package are dispositioned. Phase 4.6 is incomplete: the Astra seat's result is recorded below, and the Gemini 4 Argon seat is pending because its route is not in this tree (the brief's named blocker).

## Acceptance-criteria scorecard

| ID | Criterion (#648 / brief § 7) | Verdict | Notes |
| --- | --- | --- | --- |
| AC-01 | the folder holds `00` to `05` | PARTIAL ⚠ | `05` at stage D |
| AC-02 | the lint PASS, renovation face included | FAIL ✗ | expected before stage D; re-run then |
| AC-03 | review plan: Extended, two labs, served models | UNTESTABLE ? | the Argon blocker |
| AC-04 | every punch item at a Phase 7 outcome | UNTESTABLE ? | stage F |
| AC-05 | `reviewed-at`/`fixed-at` on #648 | PARTIAL ⚠ | `efadfea08a` recorded; body at stage H |
| AC-06 | § Scope records hash, counts, BUILD_ID, M7 delta | PASS ✓ | |
| AC-07 | 83-row coverage table | PASS ✓ | `grep -c` = 83 |
| AC-08 | the ten mechanical checks recorded | PASS ✓ | |
| AC-09 | Q5: the two numbers and `setsettings.sh` timed | PASS ✓ | |
| AC-10 | Q6: one row per script, unreached rows with `Already written:` | PASS ✓ | 47 rows |
| AC-11 | Q4: 43 commits dispositioned | PASS ✓ | |
| AC-12 | every guest proof names its copy | PASS ✓ | |
| AC-13 | bug issues, removals with `Already written:`, `box-check` | UNTESTABLE ? | stage D |
| AC-14 | the retro | UNTESTABLE ? | stage G |
| AC-15 | the five checkers before the merge | UNTESTABLE ? | before the merge |

**Pass rate:** 7/15 criteria fully met (47%) at the end of stage B; the rest are later stages' (the Total is the column of the rows above, counted).

## Code Quality Assessment

### Strengths
- The settings writers and the lock: literal key matching through `index()`, values through the environment, one rename per write, `pipefail` in a subshell gating every rename, a torn last line dropped (`001-functions:360-612`); each decision dated in a comment.
- `rocknix-evidence`'s filter enforced at the boundary, and `rocknix-corekeep`'s bounds (cap before compression, floor, lock, ring by time).
- `factoryreset`'s and `wifictl`'s fork halves: every verb returns a status and checks what it removed or wrote.

### Concerns
- Success over a failure in inherited destructive or credential scripts (F-29, F-36, F-40, F-48, F-67).
- Values that cross into `eval` or `sed` unquoted (F-14, F-19, F-52, and § 3.6.5 (B)'s siblings).
- `#!/bin/sh` scripts that need bash, 14 sites (§ 3.6.5 (D)); `008-perfmode`'s fatal `.` is its consequence (F-58).

### Complexity Hotspots
- `setsettings.sh` (1,479 lines, 24 parallel functions sharing one staged sed file); `runemu.sh` (626 lines, the emulator dispatch, the performance modes and the exit mapping in one script); `rocknix-config` (Batocera's tool, half its verbs without their programs).

## Cornerstone Conformance

**Overall:** MEDIUM. The ⚠ and ✗ rows of `03-retrospective.md` § 3.2: dependencies undeclared (F-62); guards that fail open (F-29, F-36, F-40, F-48, F-67); what was already written on upgraded devices (F-33, F-44, F-63); least surprise (F-01, F-10, F-19, F-44); `upgrade.log` overwritten (F-28); blindspots 22, 43, 57 repeated in product code, 7/34 in the brief, 32 in this audit's own log.

## Spec Fidelity

### Aligned
The scope, the hash, the counts, the image, the M7 delta, the RetroArch-half rule, the tool arguments of § 5 (all ten ran as written).

### Diverged
Three brief claims were wrong and are recorded as deltas (`/bin/sh` is bash; `rocknix-memory-manager` is a oneshot; `vocabulary-check` reads none of this slice); `tools/vm-upgrade-rehearsal` cannot run under § 5's own bounds as written (asked on #648, not run). Impact: none on the verdicts; the Coverage Boundary names the rehearsal's absence.

## Missing Artifacts

From `03-retrospective.md` § 3.6 (with its search trail): tests for `setsettings.sh`'s option files, `match()`, `add_setting` and its parallel staging; any test for `rocknix-fake-suspend`, `paneladj`, `updateabl`, `installtointernal`; a launch-seam test with a per-game setting, a bracketed name, netplay or a governor; `vocabulary-check`'s scope over this package's scripts.

## Risk Assessment

Every finding, with its question, severity and evidence class (titles from `02-forward-audit.md`'s finding headings, generated):

| Finding | Question | Severity | Defect or item | Evidence |
| --- | --- | --- | --- | --- |
| F-01 | Q3 | Medium | a governor setting is run as a command, and names ES offers have no function | proven on the guest |
| F-02 | Q3 | Low | `onlinethreads` does not exist on x86_64, and the exit path calls it every time | proven on the guest |
| F-03 | Q3 | Medium | exit-time restores run in the background and race the next launch | trace / read |
| F-04 | Q3 | Low | the per-game fan profile is written into the global setting for the length of the game | trace / read |
| F-05 | Q6 | Low | dead variables | trace / read |
| F-06 | Q3 | Low | `rm ${ROMNAME}.nvmem*` unquoted | trace / read |
| F-07 | Q3 | Low | `CORE` and `EMULATOR` are still cut from the joined line | trace / read |
| F-08 | Q7 | Low | every `log $0 " | trace / read |
| F-09 | Q3 | Medium | `add_setting`'s condition is two commands, not one | proven on the guest |
| F-10 | Q3 | Medium | `match()` is a substring regex, so `neogeo` is read as `neogeocd` | proven on the guest |
| F-11 | Q3 | Medium | the parallel functions share one staged sed file through a check-then-create | proven on the guest |
| F-12 | Q2 | Low | `set_config_save` passes its arguments in the wrong positions | trace / read |
| F-13 | Q2 | Low | a joypad autoconfig is sourced as shell, as root | trace / read |
| F-14 | Q3/Q2 | Medium | the netplay host a player types reaches `runemu.sh`'s `eval` unquoted | proven on the guest |
| F-15 | Q3 | Low | two netplay `add_setting` calls are malformed | trace / read |
| F-16 | Q3 | Medium | tate mode wipes the MAME 2003-Plus core options | proven on the guest |
| F-17 | Q3 | Medium | every Game Boy launch truncates `Gambatte.opt` | proven on the guest |
| F-18 | Q3 | Low | Kronos's options file is written under a path RetroArch may not read | trace / read |
| F-19 | Q2/Q3 | Medium | option values are spliced into `sed` programs unquoted, and a default device never applies an overlay choice | proven on the guest |
| F-20 | Q2 | Low | the sway test prints into the caller's output | trace / read |
| F-21 | Q3 | Medium | a game's own settings are not found when its file name holds a regex character other than `'`, `(`, `)` or `&` | proven on the guest; fixed upstream (`25903bb59c`) |
| F-22 | Q7 | Low | `wait_lock` replaces its caller's traps | trace / read |
| F-23 | Q2 | Low | `sway_fullscreen` prints the sway test's match | trace / read |
| F-24 | Q5 | Low | the shared `log()` appends to `/var/log/messages` with no bound | trace / read |
| F-25 | Q3 | Low | `set_online_threads` counts CPUs by `find /sys/devices/system/cpu -name online / wc -l` | device-only: trace |
| F-26 | Q3 | Low | `create_controller_db` tests `[ ${INPUT_NAME} == "hotkeyenable" -a ${HOTKEYENABLE_BUTTON} == ${SELECT_BUTTON} ]` unquoted (`:132`), so a pad mapped wi | trace / read |
| F-27 | Q3 | Low | every launch on the default config asks for an empty shader | trace / read |
| F-28 | Q3/Q5 | Low | the update's own log is gone at the next boot | proven on the guest |
| F-29 | Q3/Q2 | Medium | a hash that failed to compute, or a shadow line of another shape, is reported as a password change | proven on the guest |
| F-30 | Q3 | Low | a bound (tens of seconds) costs nothing on a healthy card, where `cat` and `mv` of 5 KB take milliseconds | device-only: trace |
| F-31 | Q7/Q2 | Low | `Description=ROCKNIX user autostart script` names another unit's job, and `EnvironmentFile=/etc/profile` hands systemd a shell script as an environmen | trace / read |
| F-32 | Q3/Q2 | Medium | the two last writers of `system.cfg` that bypass the settings lock and the torn-file guard | proven on the guest |
| F-33 | Q3 | Low | the interface configs' `last_` copies are not idempotent | trace / read |
| F-34 | Q3 | Low | dev-image blocks overwrite the owner's files | trace / read |
| F-35 | Q3 | Low | `cd` without a check | trace / read |
| F-36 | Q7 | Low | `overlays` finds its folders with a greedy match that works by the option order | trace / read |
| F-37 | Q3 | Low | `rk817-fuelgauge` (`:220-238`) exits 0 having done nothing when no `rk817` is found (the loop's status), unlike every other verb | trace / read |
| F-38 | Q3 | Low | `audio` removes `/storage/.local/state` whole | trace / read |
| F-39 | Q3 | Medium | nothing refuses a target that holds the running system | device-only: trace |
| F-40 | Q3 | Medium | a failed copy of `/storage` ends on "successful" | proven on the guest |
| F-41 | Q6 | Low | `start_overlay` is dead | trace / read |
| F-42 | Q3 | Low | a mount that fails is neither checked nor said | trace / read |
| F-43 | Q7 | Low | `:251` writes `ISMOUNTED="$(grep "${DEV}" /proc/mounts) >/dev/null 2>&1"`, the redirection inside the quotes, so the test at `:252` works only because | trace / read |
| F-44 | Q3 | Medium | every update turns the player's DPMS choice back off | proven on the guest |
| F-45 | Q3/Q6 | Low | `ngpc.intergerscale=1` is misspelled | trace / read; fixed upstream (`4e3972d037`) |
| F-46 | Q6 | Low | `updates.enabled=1`, `updates.branch=auto`, `updates.force=0` | trace / read |
| F-47 | Q2 | Low | the credential filter misses three argv shapes the slice's scripts produce | trace / read |
| F-48 | Q3 | Low | the verbs outside the typed list report success with no adapter | trace / read |
| F-49 | Q6/Q3 | Low | `restart` cannot restart, and nothing calls it | trace / read; cause fixed upstream (`6aa745572b`) |
| F-50 | Q2 | Low | a `#!/bin/sh` script in bash | trace / read |
| F-51 | Q7 | Low | the service's `Description=Report anonymous ROCKNIX install statistics` describes what it no longer does | trace / read |
| F-52 | Q2 | Low | the setting flags write and `eval` their value unquoted | trace / read |
| F-53 | Q3 | Low | a swap-file resize writes over a file the kernel may still be swapping to | device-only: trace |
| F-54 | Q2 | Low | names from a remote list reach a file path, guarded by accident | trace / read |
| F-55 | Q6 | Low | nine scripts have no caller anywhere | trace / read |
| F-56 | Q3 | Low | `autostart/050-audio` runs a program that is not there, every boot | proven on the guest |
| F-57 | Q3 | Medium | `paneladj` clamps every stored panel value to its maximum and writes a stray file | proven on the guest |
| F-58 | Q3 | Medium | `autostart/008-perfmode` stops at its third line on every x86_64 boot | proven on the guest |
| F-59 | Q3 | Low | `055-hdmi-check` writes the 1080p mode to the wrong file | trace / read |
| F-60 | Q2 | Low | an unset `audio | trace / read |
| F-62 | Q2 | Low | the scripts' programs are present but undeclared | trace / read |
| F-63 | Q2 | Low | `system.cfg` is world-readable and world-executable | trace / read |
| F-64 | Q3/Q6 | Low | `rocknix-config` is carried with Batocera's dependencies, and the interface's calls reach verbs that do nothing or fail | trace / read |
| F-65 | Q3 | Low | `rocknix-settings` can write `system.cfg` outside the lock | trace / read |
| F-66 | Q6 | Low | `rocknix-scraper` (79, upstream-carried) is reached only through a page nothing opens, and runs a scraper the image does not have | trace / read |
| F-67 | Q3 | Medium | `updateabl` writes the bootloader on both slots without checking the writes | device-only: trace |
| F-68 | Q2 | Medium | the Bluetooth pairing keys are copied onto the games folder at every Bluetooth stop | trace / read |
| F-69 | Q1/Q6 | Low | drop the entry, or the file with the verb | trace / read |

**Totals:** 68 findings (19 Medium, 49 Low), counted from the rows above; F-61 is unused.

## Coverage Boundary

**Examined:** all 83 paths; 62 read whole and 21 in outline (named in `02-forward-audit.md` § Coverage Boundary and per row in the coverage table); 18 findings and a dozen image facts runtime-probed on the guest; ten mechanical checks run; shellcheck v0.11.0 over 63 shell files with all 16 errors dispositioned; the M7 delta read as context; the interface's call sites read at the pin.
**Deliberately not examined:** `backuptool` (T17), the interface's code beyond call sites (T2, T21), the sysutils runner and units (T22), the quirks (T29), the cloud scripts (T16, T17).
**Dimensions not exercised:** anything on a handheld (no device in M6): H700 governors (from the kernel config), backlight, LED, lid and power suspend, HDMI hotplug, USB gadget binding, Bluetooth, the Qualcomm ABL and internal storage; KSM on a 1 GiB device; `tools/vm-upgrade-rehearsal` (asked on #648); the outline-read files' remaining lines; the second reviewer seat (Argon, pending).

## Finding Verification (Phase 4.5)

No finding is Critical or High. The Medium findings, attacked the same way before they go to the seat:

| Finding | Severity | Survived refutation? | What was checked |
| --- | --- | --- | --- |
| F-01 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-03 | Medium | yes | code path re-read end to end; the device fact named |
| F-09 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-10 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-11 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-14 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-16 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-17 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-19 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-21 | Medium | yes | reproduced on the guest (§ Guest proofs); the fix exists upstream |
| F-29 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-32 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-39 | Medium | yes | code path re-read end to end; the device fact named |
| F-40 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-44 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-57 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-58 | Medium | yes | reproduced on the guest (§ Guest proofs) |
| F-67 | Medium | yes | code path re-read end to end; the device fact named |
| F-68 | Medium | yes | code path re-read end to end; the device fact named |

Refutations that **changed** a finding before this table: F-01 narrowed (the interface never writes `default`, `SystemConf.cpp:387`); F-32 corrected (busybox `sed` completes the half line rather than joining it); F-47 narrowed (the snapshot's `top` prints names only); F-67's skip-check suspicion cleared by the ELF's size; F-09's fix shape chosen to keep `:989`'s observed behaviour.

## Renovation face

### Q1 Modernize

Python 2 remnants in the two Python scripts the image runs under 3.14 (`rocknix-systems:1-3`, `rocknix-bluetooth-agent:1-5`: `#!/usr/bin/python`/`env python`, `from __future__`, `optparse`); `setsettings.sh`'s staged-sed mechanism, which writes and executes a shell program (`:310-325`, `deferred:#336`); hand parsing of `ps aux` in `vertical-check` and of `system.cfg` in `rocknix-settings` beside `get_setting`; a stale zone in the `tz` list (F-69); upstream's `get_setting` (`25903bb59c`) is the modern lookup (a quoted `=~`, no fork) and is taken in Q4. Backticks and `cat | grep` remain in the upstream-carried scripts (shellcheck notes, not itemised).

### Q2 Standards and best practices

`tools/pkgcheck rocknix` 0. shellcheck v0.11.0: 16 errors, all dispositioned (7 defects, 4 in unreached scripts, 4 benign, the rest folded into F-10); 319 warnings, 542 notes, summarised per file in the coverage table. The rules: `packaging-and-patches.md` (F-62), `engineering-practices.md` § Guards must fail closed (F-29, F-36, F-40, F-48, F-67), the credential filter's shapes (F-47), the `#!/bin/sh`-needs-bash pattern (14 sites, § 3.6.5 (D)), file modes (F-63). `installtointernal` is the only script with `set -euo pipefail`.

### Q3 Bugs

The defects among the findings (the Risk Assessment's Q3 rows): 18 proven on the guest, the rest traced. Two prevalent shapes: values spliced into `eval`/`sed` (§ 3.6.5 (B)) and success over a failure (§ 3.6.5 (C)). The RetroArch half's Q3 items (F-09, F-10, F-11, F-14, F-16, F-17, F-19) are fixed regardless of #336 (brief § 4).

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



### Q5 Efficiency: measured on the guest (`BUILD_ID 069fc270442134fe771258418adf4e666e0473fb`, 4 vCPUs, 8 GiB, virgl GL), `system.loglevel=verbose` (the engineering image's `DEVELOPMENT_DEFAULTS`)

**The two time-to-play numbers**, `tools/time-to-play --port 10032 --identity $A/qa-key --monitor $A/monitor.sock --out $A/ttp-q5 --no-configure-remote --vm --only launch,exit,g2g --repeat 3` (08:12:32-08:16:06 UTC; rc 1, `Not a pass: the exit sync had no cloud to reach`, the expected verdict without a remote):

| Measure | This slice's guest (n=3) | #336's baseline | Note |
| --- | --- | --- | --- |
| interface press to **the game's first frame** | **0.64 s** median (mean 0.67, max 0.76) | 1.05 s | the image's `runemu.sh` (the M7 copy, with its lifecycle prologue) |
| exit (`execute_kill`) to **the next game's first frame** | **1.01 s** median (mean 1.01, max 1.02) | 2.03 s | measured with no cloud: the exit sync skips at once, so this is not like for like with a configured device; #336's figure's conditions are not recorded in its body |
| exit to the last-sync-exit stamp | 0.55 s median | - | the skip |

Both numbers are well under #336's, which predates the hardware-GL guests (#291) and was taken at an unrecorded loglevel; this slice changed nothing yet, so the comparison says the baseline is stale, not that the slice improved anything. **What the slice's findings would do to the numbers**: F-09's backgrounded `[` costs a fork per `add_setting` (up to 104 a launch); upstream's `25903bb59c` drops a fork per `get_setting` (Q4); F-03's background restores race the next launch rather than delay it.

**`setsettings.sh` per launch**, with the arguments the last launch passed (`gb /storage/roms/gb/TTProbe.gb gambatte --state_file=/storage/roms/savestates/gb/TTProbe.state.auto --controllers= --autosave=1 --snapshot=`, read from `/var/log/exec.log`'s `Execute setsettings` line), five runs each, wall time from `date +%s%N` (08:16 UTC): **verbose 127 ms** median (141, 130, 127, 126, 127); **none 99 ms** median (92, 124, 99, 100, 99). So the verbose log costs about 28 ms a launch on this guest. An H700's four A53 cores will be several times slower; the guest number is the one this slice can stand behind.

**Boot** (`systemd-analyze`, the boot `time-to-play` itself made): startup 3.760 s (1.384 kernel + 2.376 userspace), `rocknix.target` at 1.942 s. This package's units: `rocknix-autostart.service` 1.177 s (T22's runner executing this package's fragments; `008-perfmode` stops at its third line here, F-58), `rocknix-automount.service` 417 ms, `rocknix-evidence.service` 271 ms, `rocknix-sysconfig.service` 16 ms, `rocknix-memory-manager.service` 15 ms.

**Standing costs**: `rocknix-evidence snapshot` 230 ms and 6,856 bytes a page, every five minutes; `/var/log/messages` (F-24) grew from 5,310 to 7,888 bytes across one reboot of the guest, about 2.5 KB a boot with no bound; KSM (on by default, `rocknix-memory-manager`) is not in the guest's kernel (`/sys/kernel/mm/ksm` absent), so its cost on a 1 GiB handheld is a device question, not measured here; `vertical-check` runs a `ps aux` per RetroArch window (not timed). **Not measured**: anything on an A53, KSM's background scan, the fake-suspend path.

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



### Q7 Clarity and structure

`setsettings.sh` carries nine cores' option files beside RetroArch's own settings (`deferred:#336`); `runemu.sh` logs every line with its own path as the first word (F-08) and carries dead variables (F-05); `rocknix-fake-suspend`'s `suspend()` shadows a bash builtin; `rocknix-config` is Batocera's tool with Batocera paths (F-64); two units describe what they no longer do (F-31, F-51); the fork's own files are documented decision by decision (`001-functions`, `chksysconfig`, `rocknix-corekeep`), sometimes at a length a newcomer must wade through, never misleadingly except `rocknix-evidence`'s process-list sentence (F-47) and `setsettings.sh`'s `-e` comment beside an unguarded host (F-14).

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

| Finding | Would have been caught by | Uncovered? |
| --- | --- | --- |
| F-29, F-36, F-40, F-48, F-67 | `.claude/rules/engineering-practices.md` § "Guards must fail closed" | — |
| F-62 | `.claude/rules/packaging-and-patches.md` § "A shipped script's tools are dependencies too" | — |
| F-32, F-65 | `.claude/rules/engineering-practices.md` § "Fail gracefully" (the last-good writers) | — |
| F-14 | `.claude/rules/engineering-practices.md` § "A failure you find is yours to fix" (#275's sibling search) | — |
| F-44, F-33 | `.claude/rules/upgrade-and-install.md` § "Every fix answers what was already written" | — |
| F-58, F-50 | (none: no rule says a `#!/bin/sh` script must not need bash) | **YES** |
| F-01, F-10, F-21 | (none: no rule covers a value from settings used as a pattern or a command) | **YES** |

### Codification Gaps (needs-new-rule)

| Pattern | Instances | Recommendation |
| --- | --- | --- |
| P-01: a `#!/bin/sh` script that needs bash | 14 sites (§ 3.6.5 (D)), F-50, F-58 | **Extend** `.claude/rules/packaging-and-patches.md` with "The interpreter line says what the code needs": a script using bash says `#!/bin/bash`; a fragment that sources `001-functions` is bash; prove a `#!/bin/sh` script under the image's `sh` on the guest |
| P-02: a setting's value used as a pattern, a command or program text | F-01, F-10, F-14, F-19, F-21, F-52 | **Extend** `.claude/rules/engineering-practices.md` § "Guards must fail closed" with "A value is data": match literally (`index()`, a quoted `=~`, `grep -F`), dispatch through a `case` of known names, pass values through the environment, never splice into `eval` or a `sed` program |
| P-03: success reported over a no-op in an inherited destructive script | F-29, F-36, F-40, F-48, F-67 | already covered by § "Guards must fail closed"; the gap is enforcement: a test per destructive script that plants the failure (the tool tier, `working-principles.md`) |

### Recommended Action Sequence

1. The coordinator decides whether P-01 and P-02 become rule edits (stage G's retro, Instruction-Recommendations mode).
2. The stream briefs carry P-03's tests as acceptance lines for the fail-open fixes.

## Second opinion (Phase 4.6)

_Pending: written after the Astra call below; the Gemini 4 Argon seat is pending on its route (`grep -c gemini-argon scripts/council-invoke.ts tools/lint-audit-artifacts`: `0`, `0`)._

## Quality Self-Check

| Item | Status |
| --- | --- |
| Acceptance Criteria Scorecard present, IDs match 02 | present (AC-01 to AC-15) |
| Cornerstone conformance tables present | present (`03` § 3.2, summarised above) |
| Coverage Boundary present (02 + 04) | present |
| Finding Verification recorded for all Crit/High | present (none Critical or High; the Mediums recorded) |
| Second opinion recorded (Phase 4.6) | absent: the Astra call follows; Argon pending on its route (the brief's blocker) |
| Instruction File Recommendations (epic) | present |
| Tier B visual-QA consolidation present | absent (no screen changed; no visual-QA process for scripts) |
| Verdicts use the defined vocabulary only | yes |
| Traceability / Evidence / Reproducible / Actionable / Complete | self-checked; the outline-read files are named as such |
