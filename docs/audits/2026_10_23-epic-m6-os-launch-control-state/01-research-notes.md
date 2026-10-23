# Research Notes — M6.P2 T1, the OS scripts: launch, control and state

**Auditor:** Code Auditor skill (v1.13.0), primary Claude Opus 5.5 (Anthropic) at high effort
**Date:** 2026-10-23
**Subject:** #648 (`M6.P2 E695/T1`), area epic #695, renovation epic #339, milestone M6
**Spec:** `docs/reviews/briefs/os-launch-control-state.md` version 2 (its § 7 is #648's checklist); `docs/reviews/plan-for-the-plan.md` § 4 (the seven questions), § 6b (the stages)

---

## Scope

### The read hash

- The slice's bytes are `next`'s at **`8ebaf8daad`** (`next` = `origin/next` = `8ebaf8daad` on 2026-10-23; `git diff --quiet 8ebaf8daad HEAD -- projects/ROCKNIX/packages/rocknix/` exit 0 at the branch's `HEAD` `4228561fd2` and again at `a0d9e39101`).
- **`reviewed-at`** is the branch commit that carries this § Scope (stage A's commit), named in `00-running-log.md` once it exists; every later read is made on a tree whose bytes under the package equal `8ebaf8daad`'s, re-checked before stage D.
- `upstream/next` for Q4: **`8b70f693b8`** (`8b70f693b87464efb2ad0febe570db8eb67b6563`), fetched 07:05 UTC; the merge base is `c445081a59`; `git log --oneline c445081a59..upstream/next -- projects/ROCKNIX/packages/rocknix/ | wc -l` = 43.

### The counts, re-derived (brief § 2; recorded by the survey at `eb4763e3cc`)

| Quantity | Command | Brief | Here | Delta |
| --- | --- | ---: | ---: | --- |
| paths | `git ls-files projects/ROCKNIX/packages/rocknix \| grep -v -F 'sources/scripts/backuptool' \| wc -l` | 83 | 83 | none |
| paths, lines, tiers | the brief's `python3 -I` filter over `docs/reviews/inventory.json` (rows with `tree=distribution`, `area=os-scripts-and-launch`, path under the package) | 83, 13327, 29, 54, 8369 | `paths 83 lines 13327 fork-own paths 29 upstream-carried paths 54 fork-own lines 8369` | none |
| lines | `git diff --numstat "$(git hash-object -t tree /dev/null)" 8ebaf8daad -- projects/ROCKNIX/packages/rocknix/ \| grep -v -F 'sources/scripts/backuptool' \| awk '{s+=$1} END {print s}'` | 13327 | 13327 | none |

Two commands for one quantity (lines: the inventory and numstat) agree. Every row's `reach` is `shipped` (package level).

### The image

- `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (2,122,289,964 bytes), copied with its `.tar`, `.identity.json` and the previous image `...20261022T145625Z.g6e3a2165d415...img.gz` to `ROCKNIX_ARTIFACTS=/workspace/artifacts/m6-t1-20261023`; `sha256sum -c` OK on all three.
- **BUILD_ID, read from the guest's `/etc/os-release`: `069fc270442134fe771258418adf4e666e0473fb`** (`BUILD_VERSION="0.0.1-dev+20261022T235948Z.g069fc2704421"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`).
- The guest: `generic-x64-vm run --headless --daemonize` with the lane's own `--pidfile`, `--serial`, `--monitor` under `$A`, `--vnc 19`, `--ssh-port 10032`; `system.loglevel=verbose`.
- **Delta against the brief: the image's `/bin/sh` is bash** (`/bin -> /usr/bin`, `/usr/bin/sh -> bash`, GNU bash 5.3.0; no dash on the image). The brief's "dash" was read through the build root's absolute `bin -> /usr/bin` symlink, which resolved on the host. Python is 3.14 as the brief says; busybox has 182 applets and no `grep` (GNU `grep` is `/usr/bin/grep`).

### Three groups, read in this order

From `.qa-scratch/t1/groups.tsv` (generated from the inventory; 8 + 13 + 62 = 83):

**Group 1-launch**:

- `profile.d/001-functions` (fork-own, none, 707 lines)
- `profile.d/099-freqfunctions` (upstream-carried, shell, 119 lines)
- `profile.d/100-amd64-freqfunctions` (upstream-carried, shell, 186 lines)
- `profile.d/100-gamecontroller-functions` (upstream-carried, none, 157 lines)
- `profile.d/101-gpu-functions` (upstream-carried, none, 23 lines)
- `sources/scripts/run` (fork-own, shell, 61 lines)
- `sources/scripts/runemu.sh` (fork-own, shell, 626 lines)
- `sources/scripts/setsettings.sh` (fork-own, shell, 1479 lines)

**Group 2-state**:

- `autostart/001-setup` (fork-own, shell, 44 lines)
- `autostart/003-upgrade` (upstream-carried, shell, 18 lines)
- `autostart/007-rootpw` (fork-own, shell, 26 lines)
- `config/system/configs/system.cfg` (fork-own, config, 221 lines)
- `sources/post-update` (fork-own, shell, 251 lines)
- `sources/scripts/automount` (fork-own, shell, 309 lines)
- `sources/scripts/chksysconfig` (fork-own, shell, 342 lines)
- `sources/scripts/factoryreset` (fork-own, shell, 268 lines)
- `sources/scripts/installtointernal` (fork-own, shell, 255 lines)
- `sources/scripts/setrootpass` (fork-own, shell, 65 lines)
- `system.d/rocknix-automount.service` (upstream-carried, systemd, 14 lines)
- `system.d/rocknix-sysconfig.service` (fork-own, systemd, 23 lines)
- `system.d/save-sysconfig.service` (upstream-carried, systemd, 12 lines)

**Group 3-control**:

- `autostart/006-display` (upstream-carried, shell, 29 lines)
- `autostart/008-perfmode` (upstream-carried, shell, 37 lines)
- `autostart/009-sleepmode` (upstream-carried, shell, 17 lines)
- `autostart/010-uimode` (upstream-carried, shell, 26 lines)
- `autostart/050-audio` (upstream-carried, shell, 51 lines)
- `autostart/055-hdmi-check` (upstream-carried, shell, 29 lines)
- `autostart/080-network` (upstream-carried, shell, 16 lines)
- `autostart/081-usbgadget` (upstream-carried, shell, 5 lines)
- `autostart/099-networkservices` (fork-own, shell, 45 lines)
- `config/system/configs/tz` (upstream-carried, none, 593 lines)
- `package.mk` (fork-own, recipe, 127 lines)
- `sources/motd` (upstream-carried, none, 6 lines)
- `sources/scripts/amionline` (upstream-carried, shell, 20 lines)
- `sources/scripts/bezels.sh` (upstream-carried, shell, 217 lines)
- `sources/scripts/brightness` (upstream-carried, shell, 224 lines)
- `sources/scripts/controller-layout` (upstream-carried, none, 60 lines)
- `sources/scripts/error.sh` (upstream-carried, shell, 19 lines)
- `sources/scripts/find.sh` (upstream-carried, shell, 6 lines)
- `sources/scripts/getfilters` (upstream-carried, shell, 11 lines)
- `sources/scripts/getoverlays` (upstream-carried, shell, 12 lines)
- `sources/scripts/getshaders` (upstream-carried, shell, 20 lines)
- `sources/scripts/handle-hdmi-hotplug` (upstream-carried, shell, 48 lines)
- `sources/scripts/led_flash` (upstream-carried, shell, 42 lines)
- `sources/scripts/migrate_roms` (upstream-carried, shell, 36 lines)
- `sources/scripts/paneladj` (upstream-carried, shell, 104 lines)
- `sources/scripts/rocknix-bluetooth` (upstream-carried, shell, 371 lines)
- `sources/scripts/rocknix-bluetooth-agent` (upstream-carried, python, 571 lines)
- `sources/scripts/rocknix-config` (upstream-carried, shell, 296 lines)
- `sources/scripts/rocknix-corekeep` (fork-own, shell, 250 lines)
- `sources/scripts/rocknix-es-thebezelproject` (fork-own, shell, 641 lines)
- `sources/scripts/rocknix-evidence` (fork-own, shell, 265 lines)
- `sources/scripts/rocknix-fake-suspend` (upstream-carried, shell, 486 lines)
- `sources/scripts/rocknix-info` (fork-own, shell, 259 lines)
- `sources/scripts/rocknix-keyboard` (upstream-carried, shell, 97 lines)
- `sources/scripts/rocknix-memory-manager` (fork-own, shell, 638 lines)
- `sources/scripts/rocknix-report-stats` (fork-own, shell, 7 lines)
- `sources/scripts/rocknix-retroachievements-info` (upstream-carried, shell, 104 lines)
- `sources/scripts/rocknix-scraper` (upstream-carried, shell, 79 lines)
- `sources/scripts/rocknix-settings` (upstream-carried, shell, 267 lines)
- `sources/scripts/rocknix-systems` (fork-own, python, 250 lines)
- `sources/scripts/rocknix-update` (fork-own, shell, 15 lines)
- `sources/scripts/say` (upstream-carried, shell, 22 lines)
- `sources/scripts/setemu.sh` (upstream-carried, shell, 30 lines)
- `sources/scripts/show_changelog` (upstream-carried, shell, 32 lines)
- `sources/scripts/suspendmode` (upstream-carried, shell, 55 lines)
- `sources/scripts/timeinfo` (upstream-carried, shell, 22 lines)
- `sources/scripts/updateabl` (upstream-carried, shell, 77 lines)
- `sources/scripts/usbgadget` (fork-own, shell, 615 lines)
- `sources/scripts/vertical-check` (upstream-carried, shell, 182 lines)
- `sources/scripts/volume` (upstream-carried, shell, 43 lines)
- `sources/scripts/wifictl` (fork-own, shell, 557 lines)
- `system.d/bluetooth-agent.service` (upstream-carried, systemd, 13 lines)
- `system.d/hdmi-hotplug.path` (upstream-carried, systemd, 8 lines)
- `system.d/hdmi-hotplug.service` (upstream-carried, systemd, 6 lines)
- `system.d/rocknix-evidence.service` (fork-own, systemd, 12 lines)
- `system.d/rocknix-evidence.timer` (fork-own, systemd, 10 lines)
- `system.d/rocknix-memory-manager.service` (upstream-carried, systemd, 17 lines)
- `system.d/rocknix-report-stats.service` (upstream-carried, systemd, 9 lines)
- `system.d/rocknix-report-stats.timer` (fork-own, systemd, 1 lines)
- `system.d/rocknix.target` (upstream-carried, systemd, 9 lines)
- `system.d/timers.target.wants/rocknix-report-stats.timer` (upstream-carried, systemd, 1 lines)
- `udev.d/80-usbgadget.rules` (upstream-carried, udev, 4 lines)

The state group's three units (`rocknix-sysconfig.service`, `save-sysconfig.service`, `rocknix-automount.service`) sit with the scripts they run. The control group is everything else, including the two interface-driven scripts (`rocknix-es-thebezelproject`, `rocknix-systems`, called by EmulationStation's `ApiSystem.cpp`) and Q6's first candidates (`setemu.sh`, `bezels.sh`).

### The RetroArch half (#336)

#336 Step 1 is a headless runner for the 2D cores, chosen per core in the launcher; RetroArch stays the runner for the GL cores and netplay. So the RetroArch half is a set of lines, not a file:

- **`runemu.sh` lines 238 to 357**: the `retroarch)` branch of `case ${EMULATOR}` (lines 233 to 395), from `del_setting netplay.mode` to the `RUNTHIS` rewrite with `EXTRAOPTS`; it calls `setsettings.sh` at line 327.
- **`setsettings.sh` whole** (1,479 lines): it writes RetroArch's configuration (`RETROARCH_CONFIG`, `/tmp/.retroarch.cfg`, line 13 to 22) and is called only from `runemu.sh:327` (to be confirmed by Q6's caller search).
- Not in the half: the rest of `runemu.sh` (argument parsing, logging, the mednafen and standalone branches, performance and GPU modes, the exit-hotkey marker, the exit-status mapping at 570 to 626, which governs every emulator).

Q1, Q5 and Q7 findings confined to those lines are carried `deferred:#336` at Phase 7 unless a stream brief says otherwise; Q2 and Q3 findings there are fixed.

### Interacting subsystems (read-only context, never changed here)

The interface's launch path (T2: `FileData::launchGame`, `ViewController`, `LaunchCommand.h`), `ApiSystem` (T21, calls this package's scripts by name), `es_systems.cfg` and `mk_es_systems` (`projects/ROCKNIX/packages/virtual/emulators`, T3), the autostart runner, units and sleep scripts of `projects/ROCKNIX/packages/sysutils/` (T22), the quirks (T29), the cloud scripts the exit path reaches and `backuptool` (T16, T17), the offline achievements proxy (T19), and `system.cfg`/`es_settings.cfg` as shared state. The EmulationStation checkout `/home/max/Development/emulationstation-next` is read only with `git -C $ES grep -F <name> 16dbac5211eea7e70db7394372033be2be7df829`.

### The incoming M7 delta, hunk by hunk

`git -C /workspace/repos/rocknix log --oneline next..069fc2704421 -- projects/ROCKNIX/packages/rocknix/` (the legacy checkout's `next` is `8ebaf8daad` too): `069fc27044` cloud: report failed achievements recovery after sign-in; `3b27b9a70d` cloud: repair browser audit lifecycle boundaries; `d535e026b2` m7: freeze shared achievements and sign-in engineering image. `diff --stat`: `package.mk` 3 (+2 -1), `runemu.sh` 63 (+62 -1).

1. **`package.mk` @@ -12,7 +12,8 @@**: a comment line `# Launch-refusal recovery guidance uses bounded Python observation (#642).` and `PKG_DEPENDS_TARGET` gains `Python3 coreutils` (`toolchain autostart zip busybox` -> `... busybox Python3 coreutils`).
2. **`runemu.sh` @@ -4,6 +4,67 @@** (before `. /etc/profile`): a function `ra_lifecycle_launch_refused` (reason, original rc; a bounded `timeout 4s python3 -I` read of `raofflineproxy.lifecycle_recovery.recovery_status()` when the reason is `transition-entry-present`; an English or French message; a `logger` line; the message published atomically to `/tmp/launch_error.log` with `mktemp` and `mv -fT`, then `exit 250`, else `exit 1`), then the admission sequence on `/run/raofflineproxy-lifecycle` (create `0700`, refuse a link or wrong custody, create and open `admission.lock` as fd 199, `flock -s -n 199`, check the fd's device and inode against the path, refuse while `transition.json` exists).
3. **`runemu.sh` @@ -335,7 +396,7 @@** (inside the RetroArch half): the proxy is started with `( exec 199>&-; python3 /usr/share/lowerdeck/ra_proxy.py ... ) &`, so the background proxy does not inherit the admission lock's fd.

The slice reads `next`'s copy. Findings on lines the M7 delta changes are recorded with that fact; a punch item that would touch those hunks is announced on #648 before any stream brief (brief § 2). Hunk 3 is inside the RetroArch half; hunk 2 is outside it.

### shellcheck

**`shellcheck: run`**: v0.11.0, the static `linux.x86_64` binary from the project's GitHub release, at `.qa-scratch/shellcheck-v0.11.0/shellcheck-v0.11.0/shellcheck` (gitignored, `.gitignore:63`); archive SHA-256 `8c3be12b05d5c177a04c29e3c78ce89ac86f1595681cab149b65b97c4e227198`, equal to the `digest` GitHub publishes for the asset; binary SHA-256 `4da528ddb3a4d1b7b24a59d4e16eb2f5fd960f4bd9a3708a15baddbdf1d5a55b`. No system package installed.

### Rules read (`working-principles.md` § Pre-flight)

From this worktree, whose rules differ from `next`'s only in `fork-workflow.md` and `instruction-files.md` (P1's tool-list additions); each scoped file below checked equal to `next`'s with `diff -q`:

- Read whole: `.claude/skills/code-auditor/SKILL.md` and `references/phases.md`, `review-levels.md`, `templates.md`, `anti-patterns.md`; `packaging-and-patches.md`; `change-log.md`; the every-session set, loaded this session (`engineering-practices.md`, `time-to-play.md`, `least-surprise.md`, `player-language.md`, `es-player-text.md`, `bugs-are-agent-first.md`, `vm-first.md`, `issue-tracking.md`, `decision-register.md`, `learning-capture.md`, `ceremonies.md`, `worktrees.md`, `fork-workflow.md`, `milestone-phase-naming.md`, `adversarial-council.md`, `working-principles.md`, `upgrade-and-install.md`, `handheld-evidence.md`, the other ES rules, `instruction-files.md`, `release-candidates.md`, `device-builds.md`).
- Read by the sections the brief names: `generic-x64-vm-testing.md` (§ Headless, § What the guest's busybox lacks, § Fixtures for the launch path, § After every VM cycle, § Crash and hang recipes, § Spin a guest down, § The interface runs under `essway.service`, § A settings change made from the shell is invisible, § Private settings modes); `rclone-cloud-sync.md` (§ Config conventions, § Critical gotchas, § Style, § What the audit's fixes changed, § What the audit of the fix round changed).
- `docs/blindspot-register.md`: entries 7, 13, 30, 32, 33, 34, 43, 51, 57, 64, 72, 73 in full; the titles of all 73.
- Not yet read, opened in the phase that needs them: `packages/README.md` (with `package.mk`), the decisions by ID (from the register as each is cited), the open issues of brief § 3, the prior punch lists (Phase 1.5, provenance only).

## Phase 1 — Research

### 1.1 The spec

The brief (version 2) and #648's body (its checklist identical to brief § 7) are the spec. The stage-D pause, the RetroArch-half rule and the reviewer route are stated in #648's body above the checklist. Ambiguity noted at stage A: the brief's `/bin/sh` claim (corrected; Q2 reads `#!/bin/sh` scripts under bash in POSIX mode). The coverage table's unit is one row per path (83), which the criterion counts with `grep -c`.

### 1.2 The issues (open, named by brief § 3), read for planned changes and leads, not as a work queue

Bodies saved under `.qa-scratch/t1/issue-<n>.md` (gitignored), grepped for this package's script names (`\b(runemu|setsettings|001-functions|get_setting|set_setting|chksysconfig|post-update|factoryreset|installtointernal|automount|usbgadget|wifictl|rocknix-evidence|corekeep|setrootpass|rocknix-update|system\.cfg|exec\.log|...)\b`). Leads, each to be re-derived from the tree before it bears on a verdict:

| Issue | State, label | What it says about this slice |
| --- | --- | --- |
| #336 | open | Step 1 keeps RetroArch for GL cores and netplay; the runner is per core. Baseline: first frame 1.05 s, next game 2.03 s on the VM. Draws the RetroArch half (§ Scope). |
| #10 | open, enhancement | RetroArch writes save states where `setsettings.sh` points `savestate_directory` (`${SNAPSHOTS}/${PLATFORM}`); a per-core layout would change it. Q7/Q3 context for `setsettings.sh`. |
| #79 | open, keep an eye on | `exec.log` is rewritten at every launch (D-LAUNCH-004); crash list. Q5/Q3 context for `runemu.sh`'s logging. |
| #104 | open, epic | `rocknix-evidence snapshot` from a timer at boot+60 s and every 5 min, ring of five; `chksysconfig` keeps the last good `system.cfg`; `set_setting` writes through a temp and a rename; the only shutdown writer of `system.cfg` is `save-sysconfig.service` -> `chksysconfig backup`. Claims to re-derive in Phase 2. |
| #120 | open, epic | `last-good-scripts-test` covers `chksysconfig`, `set_setting`, `backuptool`'s restore paths, "nothing else"; the exit cell drives `runemu.sh`. A test-gap lead for the rest of the package. |
| #159, #191, #201 | open | `wifictl connect|join|saved|forget`; `wifictl:87` drops only a stale profile of the same SSID; `pin_wifi` priorities `:144-160`; settings written by `wifictl join`, "never printed". Line numbers to re-derive. |
| #196 | open | `runemu.sh`/`setsettings.sh` honour `-state_file` (`.auto` -> `savestate_auto_load = true`, else `-e <N>`). The RetroArch half. |
| #256, #322 | open | The upstream PR series' map; `rocknix-evidence` and `rocknix-corekeep` are fork-own and named there. Context for Q4/upstream contribution. |
| #266 | open | Bucket B device checkboxes; `wifictl` is one. No slice work. |
| #292, #293 | open, enhancement | Cards for automatic jobs; `rocknix-evidence` named in passing. No slice work. |
| #309 | open, audit | PL-003: `WifiText::parseSavedLine` reads `wifictl saved --ssid`'s three columns and unescapes `\t` and `\\`. A seam lead (wifictl's output format x the interface). |
| #316 | open | **ROCKNIX merged spycat88's PR #3394 on 2026-09-28: `wifictl: refactor and add support for connecting to saved networks` (+185/-122) on the same lines the fork changed (+255).** The choice put to the maintainer there (keep the fork's whole, or adopt upstream's). **Q4 must disposition the upstream commit with that row's outcome**, read from the register before the disposition is written. |
| #561 | open, keep an eye on | RG SP LED preference across upgrades; `post-update` named. Context for `post-update` and `led_flash`; device-only. |
| #694 | open, backlog | `rocknix-update` "intentionally exits nonzero for `check`, performs no network request, and directs manual update users to the pixelelated release page. Preserve that isolation". Q6 for `rocknix-update`: a stub by design, not a dead end. |
| #585 | open, standing | The upstream contribution queue: a fix upstream would take is recorded there (D-WORKFLOW-164/165: submissions deferred). |
| #644, #645 | open | The build-path read; no findings ride this slice (brief § 3). No mentions. |
| #18 | open, epic | `backuptool` (out of scope, T17). |
| #323, #326 | open | Release notes; the series' shared files. No slice work. |

### Closed `bug` issues that name these scripts (brittleness evidence; leads for sibling sites, Phase 3.6.5)

`gh issue list --repo pixelelated/distribution --label bug --state closed --limit 500 --json number,title,body` returned **139** closed bugs; **28** name a script, unit or fragment of this package under a word-boundary pattern of 53 names (every `sources/scripts/` name and the fragments and units, less the bare English words `run` and `brightness`, which match prose; the exact pattern is in `00-running-log.md`'s 07:21 entry). Each is a lead for Phase 2's refutation step (does the fix still hold at `8ebaf8daad`, and did it cover every sibling site):

| Bug | Names | Title |
| --- | --- | --- |
| #80 | `setsettings` | Three RetroAchievements switches never reach RetroArch: ES and setsettings.sh spell the keys differently |
| #98 | `001-functions`, `get_setting`, `runemu`, `set_setting` | 001-functions: wait_lock spins forever on a stale settings lock |
| #102 | `chksysconfig`, `rocknix-evidence` | RG SP froze during the startup sync on its first d574edf975 boot; settings lost on the forced power-off; Wi-Fi absent on the next boot |
| #106 | `rocknix-info`, `rocknix-sysconfig` | network: NetworkManager/hostnamed rewrite a hostname carrying a space or underscore (GENERIC_X64 → GENERICX64) |
| #114 | `factoryreset` | The journey continuation and the settings restore still run in a fullscreen console |
| #116 | `get_setting` | cloud_setup --info prints the root password in clear text |
| #117 | `runemu` | The exit hotkey pressed twice loses battery saves: RetroArch's exit(1) path does not flush SRAM |
| #119 | `factoryreset` | /usr/bin/run exits 0 on failure and hides the error; remaining console callers get no outcome |
| #146 | `post-update` | cloud scripts: the RCLONE_NET_OPTS fallback still carries the two-retry bound #107 removed |
| #176 | `rocknix-evidence`, `runemu`, `setsettings` | exec.log carries the RetroAchievements password in the clear, and rocknix-evidence copies it into support files |
| #178 | `rocknix-evidence` | EmulationStation log: the file lags its lines by up to 8 batches, and WARNING lines have no second channel |
| #183 | `set_setting` | VIEW THIS GAME'S ACHIEVEMENTS never appears on the VM: the startup hasher does not run and a gamelist cheevosId is not enough (hasCheevos gate) |
| #198 | `setrootpass`, `wifictl` | Device password: the interface runs setrootpass with the password unquoted, so a password with a space or a shell character is cut or misread |
| #209 | `setsettings` | Save state hotkey: the save never lands in the launched slot, and DO NOT INCREMENT is ignored by setsettings.sh |
| #211 | `runemu` | RetroArch segfaults 8 ms after the badge image of a second offline award (Bubble Bobble, fbneo, RG SP) |
| #246 | `rocknix-corekeep` | EmulationStation SIGSEGV 2.4 s after a Dr. Mario exit, offline with awards queued (RG35XX SP, f2f23da875, the soak) |
| #247 | `rocknix-corekeep` | rocknix-corekeep: a dump cut at the cap is noted as whole, and the cap drops the stacks of a big interface core |
| #249 | `runemu`, `setsettings` | Launched from the manager's AUTO SAVE tile, RetroArch's slot stays 0, so the load-state hotkey does not reload the auto save |
| #275 | `runemu`, `setsettings` | netplay: NICKNAME and PORT reach the launch command unquoted (upstream code, outside the fork's lanes -- the maintainer's call) |
| #280 | `runemu` | Save state tiles turned by another game's rotation: the launch log accumulates every launch (runemu.sh truncates only under verbose) and the record reads its last SET_ROTATION line (Dr. Mario, F-Zero, Aladdin; RG35XX SP) |
| #288 | `rocknix-evidence` | Rotation records written under the accumulating launch log stay wrong until each game is replayed: Dr. Mario and F-Zero auto saves and Dr. Mario's achievement screenshots still turned 90 degrees clockwise on a8175c6193 |
| #320 | `001-functions`, `set_setting` | M7.P1: SystemConf — the recovery record can be published from an older good state outside the settings lock (audit #319, gpt G3-E-02) |
| #416 | `rocknix-memory-manager` | M7.P3: Remove stale player-facing names from Tools and status text |
| #420 | `chksysconfig`, `set_setting` | M7.P3: Make the installed settings-race probe observable and repeatable |
| #421 | `chksysconfig`, `set_setting` | M7.P3: Preserve private settings permissions in shell writers |
| #526 | `post-update` | M7.P5: Preserve melonDS settings during post-update |
| #531 | `usbgadget` | M7.P5: Decouple USB gadget revision from calendar OS versions |
| #548 | `rocknix-info` | M7.P5: Handle unavailable hardware readings in system information |

### 1.3 Git history

`git log --oneline --no-merges c445081a59..8ebaf8daad -- projects/ROCKNIX/packages/rocknix | wc -l` = **162** fork commits on the package. Per path (`--no-merges c445081a59..8ebaf8daad`, then `--since=2026-06-01`), the 29 paths with fork commits are exactly the inventory's 29 fork-own paths:

| Fork commits since the merge base | Since 2026-06-01 (all of `next`'s history) | Path |
| ---: | ---: | --- |
| 22 | 24 | `profile.d/001-functions` |
| 14 | 17 | `sources/scripts/wifictl` |
| 13 | 13 | `sources/scripts/chksysconfig` |
| 8 | 10 | `sources/scripts/setsettings.sh` |
| 8 | 8 | `sources/scripts/rocknix-corekeep` |
| 7 | 9 | `sources/scripts/runemu.sh` |
| 6 | 10 | `package.mk` |
| 6 | 6 | `sources/scripts/rocknix-evidence` |
| 4 | 15 | `sources/post-update` |
| 3 | 6 | `config/system/configs/system.cfg` |
| 3 | 3 | `sources/scripts/rocknix-update`, `sources/scripts/automount` |
| 2 | 2-9 | `rocknix-info` (9), `rocknix-memory-manager` (4), `installtointernal` (4), `factoryreset` (3), `setrootpass`, `run`, `rocknix-es-thebezelproject` (2) |
| 1 | 1-3 | `usbgadget` (3), `rocknix-systems` (2), `autostart/001-setup` (2), `rocknix-sysconfig.service`, `rocknix-report-stats.timer`, `rocknix-evidence.timer`, `rocknix-evidence.service`, `rocknix-report-stats`, `autostart/099-networkservices`, `autostart/007-rootpw` |

The upstream-carried 54 paths have no fork commit since the merge base; Q4 reads what upstream changed on them since (`c445081a59..8b70f693b8`).

### 1.5 Prior audits: the provenance map (verdicts sequestered until Phase 2.5)

`grep -c -i -E 'runemu|setsettings|post-update|chksysconfig|factoryreset|automount|installtointernal|001-functions|usbgadget|wifictl|rocknix-evidence|rocknix-info|corekeep' <audit>/05-punch-list.md` over every `docs/audits/*/05-punch-list.md`; the counts equal the brief's. Who audited what, at what tier, and the depth signal; no PASS/FAIL transcribed:

| Audit folder | Tier | Lines naming these scripts | Trust signal for allocating effort |
| --- | --- | ---: | --- |
| `2026_09_25-milestone-rc-round-since-258` | milestone | 28 | the densest; the fix round's streams (D-WORKFLOW-056) touched these scripts most: re-verify the fixes it lists hold at `8ebaf8daad` |
| `2026_09_24-milestone-rc-round-since-186` | milestone | 17 | the round with the one-call GPT seat; a third of its list from that seat |
| `2026_09_28-milestone-audit-of-the-fix-round` | milestone | 8 | an audit of fixes: the sibling-site question applies |
| `2026_09_14-epic-offline-retroachievements` | epic | 4 | the proxy's consumers (`runemu.sh`'s RetroArch half) |
| `2026_09_28-milestone-audit-of-the-fixes-307` | milestone | 3 | |
| `2026_10_14-milestone-m7-next-candidate` | milestone | 2 | the newest; closest to `8ebaf8daad` |
| `2026_09_06-issue-device-flashing-runbook` | issue | 2 | issue tier: thin by design |
| `2026_09_29-milestone-audit-of-the-313-fixes` | milestone | 1 | |
| `2026_09_12-milestone-cloud-saves-since-60` | milestone | 1 | |
| `2026_09_10-graceful-degradation/` | (no punch list) | README, `scripts-and-writers.md`, `kill-fixtures-design.md`, `emulationstation-flows.md` | read every writer of these scripts for D-CLOUD-077/078; its **method** (kill at every step, assert one record) is the model for Q3 on the state group |

No phase retro covers this slice (the renovation's first slice); there is no Tier B visual-QA process for scripts, so § Tier B coverage is not applicable (the scripts print text only through `/tmp/launch_error.log`, `say`, and the console flows; any player-visible string is read against `es-player-text.md` in Phase 2).

### 1.6 Research Summary

- **What was planned:** a Tier-1 renovation read of 83 paths (13,327 lines) under the seven questions, Extended depth, with VM proofs and the stage-D pause (brief, #648).
- **What issues exist:** 23 open issues name the package (leads above; #316's upstream `wifictl` refactor is Q4's largest item; #694 says `rocknix-update` is a stub by design); 28 closed bugs name its scripts.
- **What code changed:** 162 fork commits since the merge base, concentrated on `001-functions` (22), `wifictl` (14), `chksysconfig` (13), `setsettings.sh`, `rocknix-corekeep` (8 each), `runemu.sh` (7); 54 upstream-carried paths untouched by the fork; 43 upstream commits on the package since the merge base.
- **What constraints apply:** the rules named in § Scope; the decisions of brief § 3; the RetroArch-half rule; nothing on a device or a person's cloud; the stage-D pause.
- **Red flags from research:** (1) the brief's `/bin/sh` claim was wrong (stage A); (2) ROCKNIX's `wifictl` refactor conflicts with the fork's (#316); (3) #120 says the script tests cover `chksysconfig`, `set_setting` and `backuptool` "and nothing else", so most of the package has no executable check beyond the named tools; (4) the security list (`setrootpass`, `wifictl`, `usbgadget`, `rocknix-evidence`) has three entries with closed credential bugs (#198, #176, #116), so the sibling-site question (blindspot 57) is live there.
