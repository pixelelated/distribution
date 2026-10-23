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
