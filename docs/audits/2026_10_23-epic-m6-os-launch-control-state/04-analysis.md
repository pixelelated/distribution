# Audit Analysis — M6.P2 T1, the OS scripts: launch, control and state

**Date:** 2026-10-23
**Spec:** `docs/reviews/briefs/os-launch-control-state.md` v2; `docs/reviews/plan-for-the-plan.md` § 4
**Issues:** #648, #695, #339
**Commits:** read at `reviewed-at` `efadfea08a` (slice bytes = `8ebaf8daad`); `upstream/next` for Q4 `8b70f693b8`; image `069fc270442134fe771258418adf4e666e0473fb`

---

## Executive Summary

T1 read the 83 paths of `projects/ROCKNIX/packages/rocknix/` (less `backuptool`) -- 13,327 lines, 29 fork-own and 54 upstream-carried -- at `8ebaf8daad`, under the code-auditor lifecycle with the renovation face, and proved every behaviour claim it could on a GENERIC_X64 guest booted from the M7 lane's newest image. It found **68 findings: 0 Critical, 0 High, 19 Medium, 49 Low**; 18 are proven on the guest, three are already fixed upstream (Q4), and the rest are traces with `file:line` or device-only leads named as such.

The fork's own state layer -- the settings writers and lock, `chksysconfig`, `rocknix-evidence`, `rocknix-corekeep` -- is sound under its tests and every refutation. The defects concentrate in the launch path's inherited middle and in upstream-carried scripts: `setsettings.sh` truncates the Gambatte and MAME 2003-Plus option files at every launch (F-16, F-17), reads `neogeo` as `neogeocd` (F-10), can lose its staged clears to a race (F-11) and ignores an explicit value (F-09); a typed netplay host reaches `runemu.sh`'s `eval` as root (F-14, #275's class through a second door); per-game settings are lost for any ROM whose name carries `[` (F-21); `runemu.sh` executes a governor name the H700 offers without a function (F-01). Guards that report success over a failure recur (F-29 `setrootpass`, F-40 `installtointernal`, F-67 `updateabl`). `post-update` resets a player's DPMS choice at every update (F-44) and is one of the last unguarded writers of `system.cfg` (F-32). On x86_64, `008-perfmode` stops at its third line at every boot (F-58). Ten scripts are unreached (Q6).

Two time-to-play numbers were measured (0.64 s and 1.01 s, against #336's stale 1.05 s and 2.03 s), `setsettings.sh` costs 127 ms a launch at the engineering image's verbose loglevel (99 ms at none), and all 43 upstream commits on the package are dispositioned. Phase 4.6 is complete: both reviewer seats (GPT-6 Astra and Gemini 4 Argon) ran and every item is graded in § Second opinion. Together they add 13 findings and move the severity of nine, which gives the final **81: 0 Critical, 2 High (F-14, F-67), 22 Medium, 57 Low**; the punch list carries 84 items (three findings split).

## Acceptance-criteria scorecard

| ID | Criterion (#648 / brief § 7) | Verdict | Notes |
| --- | --- | --- | --- |
| AC-01 | the folder holds `00` to `05` | PARTIAL ⚠ | `05` at stage D |
| AC-02 | the lint PASS, renovation face included | FAIL ✗ | expected before stage D; re-run then |
| AC-03 | review plan: Extended, two labs, served models | PASS ✓ | `openai/gpt-6-astra` by OpenAI and `google/gemini-4-argon` by Google, both from `provider_response` (§ Second opinion) |
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
Three brief claims were wrong and are recorded as deltas (`/bin/sh` is bash; `rocknix-memory-manager` is a oneshot; `vocabulary-check` reads none of this slice); `tools/vm-upgrade-rehearsal` cannot run under § 5's own bounds as written (asked on #648; answered (b), skip, issuecomment-6369533517). Impact: none on the verdicts; the Coverage Boundary names the rehearsal's absence.

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
**Dimensions not exercised:** anything on a handheld (no device in M6): H700 governors (from the kernel config), backlight, LED, lid and power suspend, HDMI hotplug, USB gadget binding, Bluetooth, the Qualcomm ABL and internal storage; KSM on a 1 GiB device; `tools/vm-upgrade-rehearsal` **not run, by the coordinator's answer (b) on #648 (issuecomment-6369533517, 2026-10-23 16:30 UTC)**: it is not in #648's checklist, it reaches the shared QA backend and `vm-pair`'s default guest and folder, which a slice lane stays off, and brief § 5's "give it its own instance paths too" was a brief error for a tool that takes none. The rehearsal belongs to the integration on the merged tree and to M7's qualification runs; an in-place proof a stage-D stream needs is the `.update` path on the lane's own guest, as that stream's brief will say; the outline-read files' remaining lines.

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

Depth **extended** (`second-opinions/review-plan.json`): the primary (Anthropic, Opus 5.5) and two reviewers from other labs. **Both seats ran, and both are graded below.** Each seat ran its probe first (`second-opinions/<member>-probe.md`), then the refutation pass alone (epic tier).

| Seat | Call | Provenance | Served | Outcome |
| --- | --- | --- | --- | --- |
| GPT-6 Astra, `max` | `tools/council/run invoke --member gpt --provider openrouter`, brief `second-opinions/gpt-brief.md` (151,087 bytes), under `tools/watch-build --record-only` (`.build-runs/20261023T082647Z-e7167ae6/`) | `second-opinions/gpt-audit.md.provenance.json`, output sha256 `df20875d97a70456...` | `model_field openai/gpt-6-astra`, `served_provider OpenAI`, identity from `provider_response` | success, 664,487 ms, prompt 43,304 / completion 30,329 (reasoning 25,332) tokens |
| Gemini 4 Argon, `high` | `tools/council/run invoke --member gemini-argon --provider openrouter`, brief `second-opinions/gemini-argon-brief.md` (163,754 bytes: the Astra packet unchanged, a third-reader preamble, and this section's Astra grades appended, as the coordinator directed on #648, issuecomment-6369533517), under `tools/watch-build --record-only` (`.build-runs/20261023T162530Z-c144c2c1/`); the route merged at `7dd89b86dc`, `verify-pins` OK, routing tests 127/127 | `second-opinions/gemini-argon-audit.md.provenance.json`, output sha256 `1f63422ddf79530f...` | `model_field google/gemini-4-argon`, `served_provider Google` (provider pin `google-vertex/global` PASS), identity from `provider_response`, effort `high` PASS | success, 527,419 ms, prompt 51,465 / completion 44,461 (reasoning 34,097) tokens, 0 retries |

### Astra's items, graded against the artifacts

Each grade below comes from re-reading the cited lines at `8ebaf8daad` (08:30-08:41 UTC), not from the seat's wording. The grades are: **confirmed**, **agree, re-graded**, **agree, narrowed**, **disagree** (with the artifact that refutes it), and **could not verify**.

**New findings (G-01 to G-07).** Each one is numbered here and gets its punch-list row in Phase 5.

| Item | Grade | Severity | Evidence from this audit's own read |
| --- | --- | --- | --- |
| G-01 `003-upgrade:11-15` | **confirmed** | Medium | `rm /storage/.boot.hint` runs unconditionally after `/usr/share/post-update >/var/log/upgrade.log`. A post-update that exits non-zero leaves no retry, and the only trace is the log. A sibling of F-28, which is the same fragment's log handling. |
| G-02 `post-update:38` | **agree, narrowed** | Low | `rsync -a --delete --exclude=configs /usr/config/system/ /storage/.config/system/` (`:26`, `:38`). It deletes anything an owner put beside `configs/`. The line dates from the fork's founding import (`9f1fab30f6`, `git log -S`), and the directory is the OS's own apart from `configs/`. So this is a documented-intent question (put the reason beside the line, or narrow the delete), not a proven loss. A fresh guest has nothing there to lose. |
| G-03 `001-functions:129-130` | **confirmed** | Low | The per-game pattern `^<sys>\["<game>"\]\.<key>` has no `=` boundary, while the system-level lookup beside it does (`/^sys.key=/`). Of the keys `setsettings.sh` reads, `integerscale` is a prefix of `integerscaleoverscale`. When a game carries both, `awk` prints both values and `echo ${OUTPUT}` joins them with a space. The fix lands with F-21, in the same function. |
| G-04 `installtointernal:63` | **agree, narrowed** | Low | `mapfile -t ud_line < <(parted ... | grep ':userdata:')`: under `set -euo pipefail` (`:8`), a process substitution's status is not checked, so a failed `parted` that still printed the userdata line passes the count test. The inventory the destructive loop uses, `MAX_PART_NUM=$(parted ... | awk | sort | tail -1)` (`:89`), is a command substitution in an assignment, and that does stop the script under `-e` and `pipefail`. So the gap is the userdata line's read, not the removal's inventory. |
| G-05 `runemu.sh:378-379,384-385` | **agree, narrowed** | Low | The ROM name is the text of a `sed` `c\` command. `/` and `&` are literal there, so the transformation is not changed by them as the seat says. A backslash or a newline in the name is interpreted, and a `"` in the name breaks the quoting in `mapper.txt`. It is reached only for PortMaster's `.sh`/`.appimage` and `windows` launches, which sits outside the RetroArch half, so Q3 applies. |
| G-06 `rocknix-config:39` | **confirmed** | Low | `sed -i "s/#\?$key=.*/$key=$value/g"`: a `/` or `&` in the value rewrites the edit, and `grep "$key"` (`:34`) is unanchored, so one key matches another. The interface does call `rocknix-config` (F-64), so this belongs in F-64's row. |
| G-07 `handle-hdmi-hotplug:19-21`, `081-usbgadget` | **confirmed** | Low, device-only | `git ls-files` lists no `usbgadget` unit, and the gadget is started by `/usr/bin/usbgadget --start` from the autostart fragment. `systemctl is-active --quiet usbgadget` is therefore false, and the stop never runs. The case is USB-C DisplayPort on RK3588/SM8250, which no VM can show, so it is a keep-an-eye-on lead. The logic can be checked with a fixture. |

**Severity and scope of the first reader's findings.**

| Item | Grade | Result | Evidence |
| --- | --- | --- | --- |
| F-01 | **confirmed** | Medium, narrowed to the dispatch | The H700 half is a kernel config, as `02` says. No governor transition was measured. |
| F-03 | **confirmed** | Medium, as missing coordination | No measured overtaking, as `02` says. |
| F-09 | **agree, narrowed** | Medium; **the fix shape is rejected** | The seat is right: "OS value when set, else the caller's" still writes `"1"` in the proven case. A forced value (netplay forbids hardcore, `:557`) and a fallback (`:989`) need different calls. Phase 5 carries two shapes. |
| F-10 | **agree, narrowed** | Medium for the list match; **the `pcsx_rearmed` half is split out** | Whole-entry matching still matches `pcsx_rearmed` in `IS_32BIT` (`:170-172`, `:801`). That half needs the installed core's architecture, and it becomes its own Low row in Phase 5. |
| F-11 | **confirmed** | Medium | 9 of 200 is the function's rate, not a launch's, as `02` says. |
| F-14 | **agree, re-graded** | **High** | The marker proof turns a stored setting into a root command. The value's source is `system.cfg`, which the interface writes from free text and which a settings restore also writes (backuptool's archive carries `/storage/.config/system/configs/system.cfg`). So the input is wider than one keyboard press. This is not a network exploit. |
| F-15 | **agree, re-graded** | Medium | `>` over the TGB Dual options file is the same loss as F-16/F-17, which are Medium. |
| F-16 | **confirmed** | Medium, scoped to `mame2003_plus` with tate on | -- |
| F-17 | **agree, narrowed** | Medium | Gambatte launches only, with the options directory present, not "every Game Boy launch". |
| F-18 | **agree, narrowed** | Low, as a question | A path the code writes but nothing in the packet reads is not proof that RetroArch never reads it. The Phase 5 row is a `question:`. |
| F-19 | **agree, re-graded** | **Low**; the precedence half becomes a `question:` | Nothing in the tree says whether bezels and overlays are exclusive. The splice and JSON escaping halves stay Low. |
| F-21 | **agree, narrowed** | Medium | Not every regex character stops the match: some match the original name or another game's name. The upstream repair `25903bb59c` was read in Q4's disposition (the get_setting half), not from its description alone. |
| F-29, F-44, F-58, F-68 | **confirmed** | Medium; each narrowed to what the guest showed | F-29 does not prove passwordless login, F-58 does not prove harmful CPU defaults, and F-68 does not prove the archive reaches a cloud. `02` already words all three that way. |
| F-32 | **agree, narrowed** | Medium | The guest proved the half line being completed, not a lost concurrent update. |
| F-39 | **confirmed** | Medium | -- |
| F-40 | **disagree** (keep Medium) | Medium | The source card is not touched (`:208-215` copy only, and the success line at `:255` says to remove the card). The harm is the false "successful" message. The data stays on the card until the owner reuses it, which is the owner's own later act. The fix (a failed copy reaches the failure status, and `:200-205` sizes what is copied) is unchanged. |
| F-67 | **agree, re-graded** | **High**, device-only | A failed `abl_a` write followed by the same write to `abl_b` (`:69-70`, no status read, no read-back) can leave the shipped Retroid Pocket Nova with no good bootloader. The control flow can be proven with loop-file fixtures, as `02` names. |

**Low findings the seat re-graded.**

| Item | Grade | Result | Evidence |
| --- | --- | --- | --- |
| F-06 | **disagree** (keep Low) | Low | `rm ${ROMNAME}.nvmem*` (`:309`) deletes another file only when a file's whole path equals a space-delimited prefix of the ROM path, such as `.../atomiswave/My` for `My Game.zip`. The common outcome is the NVRAM left in place, which `02` already states. |
| F-33 | **agree, re-graded** | Medium | `:33-34` move the link over `last_<name>` at the second update, so an owner's interface config is lost and stays lost. `02`'s `Already written:` line stands. |
| F-42 | **agree, re-graded** | Medium | A failed bind or overlay at `:57`/`:68` leaves saves written to the internal card's directory. That is #83/#84's state, and the cloud-side guard does not cover the local write. |
| F-43 | **agree, re-graded** | **Medium** for the storage selection; the assignment oddity stays Q7 | `grep "${DEV}" /proc/mounts` (`:251`) matches by substring, and `mount_games` takes the first large unmounted partition. Neither identifies the external card. Phase 5 splits the row. |
| F-54 | **agree, narrowed**: **the first reader's example is wrong** | Low | `${index_bezel_name##*.}` removes through the last dot, so an entry ending `./../x` gives `/x`, not `../x`. The traversal derivation in `02` is corrected here, and the finding becomes slash validation plus the empty-system removal. |
| F-55 | **agree, narrowed** | Low | "No in-tree caller found", not "dead": a manual user is possible, as `installtointernal` shows. |
| F-57 | **agree, narrowed**; **the seat's "a file named `1` selects the minimum" is refuted** | Medium | `getValue` reaches `:37` only with a non-empty `MYVAL` (`:35`), and `[ "${MYVAL}" ]` is then true, so the `elif` at `:40` never runs and no file `1` is read. `02`'s sentence "the first `<` reads its input from a file named `1`" is wrong on the same ground. The clamp always gives `MAX`. The seat is right that an existing file `100` in the working directory is truncated, not only created. |
| F-63 | **agree, re-graded** | Medium, bounded to the modes | Mode `645` on a file holding `root.password`, the RetroAchievements password and `wifi.key`. An effective read by another account was not tested. |

**Seat items not graded as findings.** These are § 3, what the seat could not judge. Each one restates a limit `02`/`04` already name: hardware outcomes; the background-restore race; installer and ABL failure paths; the upgrade rehearsal (asked on #648, issuecomment-6360655911; since answered (b), not run, § Coverage Boundary); the login policy; Bluetooth's trust boundary; emulator semantics; Q5 run against the image's copy of `runemu.sh`; and the lint's `13 CONTRACT FAILURE(S)`, which are expected before Phase 5 writes the punch list. One is answered by the artifacts: the 43 Q4 rows and the 47 Q6 rows are in this file (§ Q4, § Q6). The packet carried their counts, not the tables.

**The Astra seat's net effect.** The tally moved from 68 findings to **75: 0 Critical, 2 High (F-14, F-67), 22 Medium, 51 Low**:
- 7 new findings (G-01 Medium; G-02 to G-07 Low).
- F-14 and F-67 move up to High.
- F-19 moves down to Low.
- F-15, F-33, F-42, F-43 and F-63 move up to Medium.
- F-10 and F-43 split in Phase 5.
- F-09's fix shape is replaced.
- F-54's and F-57's derivations are corrected.

Two of the seat's claims were refuted by the code: F-40's High, and F-57's minimum branch. These were the Astra seat's counts alone; the Argon seat's grades below give the final tally.

### Argon's items, graded against the artifacts

Graded 16:34-16:50 UTC by re-reading the cited lines (the slice unchanged since `8ebaf8daad`: `git diff --quiet 8ebaf8daad HEAD -- projects/ROCKNIX/packages/rocknix/`), the interface at its pin `16dbac52`, and the proofs' own output (`.qa-scratch/t1/proofs/group2.out`). One read was made on the guest (its `sleep.conf.d`, through the credential filter) before it was stopped for the host handoff at 16:37:49.

**New findings (A-01 to A-11).**

| Item | Grade | Severity | Evidence from this audit's own read |
| --- | --- | --- | --- |
| A-01 `001-functions:547-550,581-585` | **confirmed, re-graded Medium → Low** | Low | `set_setting` turns the value `default` into `del_setting`, and `set_settings` does the same (`:581-585`), so a root password (`setrootpass:45`) or a Wi-Fi network name or key (`wifictl:460`) that is literally `default` is removed instead of stored. Low: the interface's own `SystemConf` drops a `default` value on save for every key (F-01's read of `SystemConf.cpp:387`), so the convention is the house's, and the collision needs that exact word. The fix is a sentinel no value can be, with `wifictl:383`'s deliberate clears moved to it. |
| A-02 `001-functions:129-166` | **confirmed** | Low | Every branch prints with an unquoted `echo ${OUTPUT}` / `${LOCAL}` / `${SYSTEM}`, so a value with a run of spaces is collapsed, one with `*` or `?` is globbed against the working directory, and `-n`/`-e` are taken as flags; the key's `.` is a regex wildcard in every `awk` pattern. Values pass back to writers (`wifictl:382`'s `key=$(get_setting wifi.key)` and the put-back at `:388`), so a key with two spaces would be put back changed. The fix is `printf '%s\n'`, with F-21 and G-03 in the same function. |
| A-03 `setsettings.sh:334-335,567` | **disagree** | -- | `NETPLAY_PORT` is `game_setting "global.netplay.port"` (`:562`), the same key `add_setting` reads as `OS_SETTING` (`:330`), so both sides hold the same value; and the shipped `system.cfg` sets `global.netplay.port=55435` (`:74`), so neither is empty on a default device. `02`'s "(the same setting either way: no effect)" stands. |
| A-04 `setsettings.sh:1427-1478` | **disagree** | -- | `set_gambatte` runs in the first parallel batch (`:1439`) and the batch's `wait` (`:1441`) ends before `set_netplay` starts in the second (`:1463`), so the two `Gambatte.opt` writers never overlap. The stdout half: `set_netplay` and `set_shader` each print one short `echo -n` to the one open file, so their order varies and their bytes do not interleave; RetroArch takes `--connect` and `--set-shader` in either order. |
| A-05 `runemu.sh:327,349,355,500` | **agree, folded into F-14** | (High, F-14) | The design is the defect: `setsettings.sh`'s whole stdout becomes part of a string `eval`ed as root, so any line any helper prints there is a command. F-14's fix already removes the `eval` (an argument array built from known flags); its acceptance gains "no text but the flags reaches the command". |
| A-06 `setsettings.sh:395,397` | **agree, narrowed** | Low | The image's `grep` is GNU (busybox has no `grep` applet here), so `-b4` is byte offsets plus four lines of context on each side. The `js0` branch reaches another stanza's `N:` line only when the matched device has fewer than three `B:` lines; the `joypad` branch joins the `Name` of every matching device, so a second pad breaks the `/tmp/joypads/<name>.cfg` lookup and the hotkeys are not set. A Q3 defect, beside F-13's Q2 item. |
| A-07 `suspendmode:8-10,51`, `autostart/009-sleepmode` | **agree, narrowed** | Low | The interface path works: `SystemConf::set` changes only its in-memory map (`SystemConf.cpp:439-460` at the pin), so `system.cfg` still holds the old mode when `GuiMenu.cpp:2491` runs `suspendmode`. First boot works too: the seed carries no `system.suspendmode`, so `009-sleepmode` asks for `mem`, the comparison differs and `sleep.conf` is written (the guest's file and key, 16:36). The broken path is a settings restore: `backuptool`'s list carries `system.cfg` and not `sleep.conf.d`, so a restored mode that differs from the device's `sleep.conf` is never applied -- at the next boot `009-sleepmode` asks for the stored mode, which matches, and nothing is written. The menu then shows one mode and the device suspends in another. |
| A-08 `post-update:144-147` | **agree, a correction of F-35's sentence** | (Low, F-35) | A failed `cd` changes neither `PWD` nor `OLDPWD`, so `02`'s "`cd -` restores it" is wrong: `cd -` errors or moves to whatever `OLDPWD` the environment carried. No later line in `post-update` uses a relative path (`:148-251` read again), so the effect is one error line. F-35's fix is unchanged. |
| A-09 `runemu.sh:432-437,537` | **agree, folded into F-04** | (Low, F-04) | With no stored profile, `quit` writes `cooling.profile=` (an empty value through `write_setting_line`, `001-functions:429-441`) where the key was absent. Readers see empty either way, so it answers F-04's open question rather than adding a defect; F-04's fix restores with `del_setting` when nothing was stored. |
| A-10 `vertical-check:9-18` | **could not verify** (carried as an item to verify) | Low | The ROM path is cut from the first `ps` line matching `runemu.sh` at its first unescaped space. Whether that line is the interface's `sh -c` wrapper (escaped or quoted by the interface's command builder) or the script's own argv (spaces unescaped) is the interface's launch shape and the process order, which a guest launch shows; the guest is down until `resource return`. |
| A-11 `rocknix-systems:1-3`, `rocknix-bluetooth-agent:1-5`, `02` § Mechanical checks | **confirmed** | Low | Two items the read noted and the punch list would have lost: the Python 2 remnants (answered in § Q1 with no item), and `02`'s "See F-candidate below" on `vocabulary-check`'s scope (it reads none of this slice's scripts), which no finding followed. Split in Phase 5 into A-11a (Q1) and A-11b (Q2). F-61 is accounted for (`02:482`). |

**The seat's re-grades, and its checks of the earlier grades.**

| Item | Grade | Result | Evidence |
| --- | --- | --- | --- |
| F-03 → Low | **agree, re-graded** | **Low** | No overtaking was measured: `02` promised a timing of the background jobs against the exit-to-next-launch time and did not run it, and the gap a person needs to pick the next game is seconds against jobs that are sysfs writes and one `systemctl restart`. The missing coordination is real; the acceptance measures it first. |
| F-19 → Medium | **agree, re-graded back** | **Medium** | The Astra grade misread the proof. With no bezel file, `write_bezel_config` returns 1 having written nothing (`setsettings.sh:1312-1331`), and `set_overlay` still exits (`:821-822`); the proof's `input_overlay lines: 0` under the shipped `thebezelproject` default (`group2.out:25`) is "neither applied". So on a default device a player's overlay choice is dropped and nothing replaces it. Whether a present bezel should win over an overlay stays the stream brief's question. |
| F-13 → Medium | **disagree** (keep Low) | Low | The sourced files are the image's and the player's own (`/tmp/joypads` over `/storage/joypads`), the player's own trust domain, as `02` says; the lookup half the seat adds is A-06, its own Low item. |
| F-27 | **agree** (keep Low, to verify) | Low | Already an item to verify: RetroArch's log for an empty shader is read before a fix. |
| F-43, `:239` | **agree** | Medium half | `(( ${SIZE} <= 8388608 ))` with no `/proc/partitions` row errors and the device is treated as large enough, which is part of choosing the wrong card: `:239` moves into F-43's Medium half; F-43b keeps only `:251`'s quoting oddity. |
| G-07's scope | **disagree** (keep the scope) | Low | The recipe enables `hdmi-hotplug.path` on the H700 only (`package.mk:115-119`), and the handler's gadget stop runs only when a DisplayPort connector reports connected (`handle-hdmi-hotplug:19-21`), which its own comment scopes to USB-C DisplayPort on RK3588/SM8250. On the one device that enables the handler, the branch needs a DP connector the comment says is not this SoC's case. |
| F-40 kept Medium; F-57's minimum branch; F-54's example; F-57's `1`-file sentence; F-14 and F-67 to High; G-01 to G-06; F-09's two shapes; F-10's split | **the seat agrees** | unchanged | Its § 2B confirms each against the same lines this section cites. |

**What the seat could not judge** (its § 3), against this audit's record: the Q4 and Q6 tables (in this file, not in the packet, as for Astra); the M7 delta and § Scope (`01-research-notes.md`); the outline-read files (named in § Coverage Boundary); six checks `02` promised and did not record -- F-27's and F-18's RetroArch reads (now items to verify), F-04's empty profile (answered above), F-08's and `vertical-check`'s timings (in their items' acceptance), F-38's list of `.local/state` writers (in its item's fix) and F-31's environment (in its item); the upgrade rehearsal (not run, by the coordinator's answer (b), § Coverage Boundary); and the hardware-only paths, already named there.

**Net effect, both seats.** The tally moves from the Astra seat's 75 to **81 findings: 0 Critical, 2 High (F-14, F-67), 22 Medium, 57 Low**:
- 6 new findings from the Argon seat, all Low (A-01, A-02, A-06, A-07, A-10, A-11).
- F-03 moves down to Low; F-19 moves back up to Medium.
- A-03 and A-04 are refuted by the code; A-05, A-08 and A-09 fold into F-14, F-35 and F-04; F-13 stays Low; G-07 keeps its scope.
- Phase 5 splits F-10, F-43 and A-11, so the punch list carries 84 items.

Both seats agreed with every High and with the refutations and corrections of the first reader's text. Neither raised a Critical.

## Quality Self-Check

| Item | Status |
| --- | --- |
| Acceptance Criteria Scorecard present, IDs match 02 | present (AC-01 to AC-15) |
| Cornerstone conformance tables present | present (`03` § 3.2, summarised above) |
| Coverage Boundary present (02 + 04) | present |
| Finding Verification recorded for all Crit/High | present: no Critical; the two Highs are F-14, proven on the guest (the marker), and F-67, a device-only trace whose skip check was cleared by the ELF's size (§ Finding Verification) |
| Second opinion recorded (Phase 4.6) | present: both seats ran, verified and graded (§ Second opinion) |
| Instruction File Recommendations (epic) | present |
| Tier B visual-QA consolidation present | absent (no screen changed; no visual-QA process for scripts) |
| Verdicts use the defined vocabulary only | yes |
| Traceability / Evidence / Reproducible / Actionable / Complete | self-checked; the outline-read files are named as such |
