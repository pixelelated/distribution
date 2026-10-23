# Research Notes — M6.P2 T2, EmulationStation's launch path

**Auditor:** Code Auditor skill, with the renovation face (plan § 4)
**Date:** 2026-10-23
**Subject:** #649, slice `es-launch-path`, the twenty EmulationStation paths of brief § 2
**Spec:** `docs/reviews/briefs/es-launch-path.md` version 2; `docs/reviews/plan-for-the-plan.md`

---

## Scope

### The read hash

- **The slice's bytes:** the ES pin `16dbac5211eea7e70db7394372033be2be7df829`. `package.mk` line 5 names it, it is the tip of `test/qa-integration`, and the ES worktree's `HEAD` equals it (`git rev-parse HEAD`, 17:22 UTC).
- **reviewed-at:** distribution `f4e0f0a196`, the branch `HEAD` when stage A opened. It is stacked on the P1 tip `2174265e9c` (`merge-base --is-ancestor` exit 0).
- The candidate image `069fc2704421` carries the same pin (brief § 2), so a proof on its guest is a proof of these bytes. Its BUILD_ID is read from the guest's `/etc/os-release` when the guest runs, which is queued until the host's `resource return`; see `00-running-log.md`.

### The counts, re-derived (brief § 2; recorded by the survey at `eb4763e3cc`)

```
python3 -I - (the inventory filter of brief § 2)
paths 20 lines 11287 fork-own 17 upstream-carried 3 fork-own lines 10804
git -C $W ls-files <the seven globs> | wc -l                                  -> 20
git -C $W diff --numstat <empty tree> $PIN -- <20> | awk '{s+=$1} END{print s}' -> 11287
cat <20> | wc -l                                                              -> 11284
```

There are no deltas: 20 paths, 11,287 lines (11,284 by `wc -l`), 17 fork-own paths with 10,804 lines, and 3 upstream-carried paths. Every path is `reach: shipped`.

| Lines | Tier | Path | Group |
| ---: | --- | --- | --- |
| 2680 | fork-own | `es-app/src/FileData.cpp` | 1 launch chain |
| 293 | fork-own | `es-app/src/FileData.h` | 1 |
| 1531 | fork-own | `es-app/src/views/ViewController.cpp` | 1 |
| 158 | fork-own | `es-app/src/views/ViewController.h` | 1 |
| 57 | fork-own | `es-app/src/LaunchCommand.h` | 1 |
| 2583 | fork-own | `es-app/src/SystemData.cpp` | 2 systems table |
| 296 | fork-own | `es-app/src/SystemData.h` | 2 |
| 240 | fork-own | `es-app/src/SaveState.cpp` | 3 save states |
| 60 | upstream-carried | `es-app/src/SaveState.h` | 3 |
| 342 | fork-own | `es-app/src/SaveStateRepository.cpp` | 3 |
| 53 | fork-own | `es-app/src/SaveStateRepository.h` | 3 |
| 337 | upstream-carried | `es-app/src/SaveStateConfigFile.cpp` | 3 |
| 86 | upstream-carried | `es-app/src/SaveStateConfigFile.h` | 3 |
| 62 | fork-own | `es-app/src/SaveStateJobQueue.cpp` | 3 |
| 72 | fork-own | `es-app/src/SaveStateJobQueue.h` | 3 |
| 344 | fork-own | `es-app/src/SaveStateBookkeeper.cpp` | 3 |
| 71 | fork-own | `es-app/src/SaveStateBookkeeper.h` | 3 |
| 596 | fork-own | `es-app/src/ProxyCards.cpp` | 4 proxy cards |
| 58 | fork-own | `es-app/src/ProxyCards.h` | 4 |
| 1368 | fork-own | `es-app/src/main.cpp` | 5 the process |

### The two upstreams (Q4's refs)

| Ref | Hash (fetched 2026-10-23) | Merge base with the pin | Commits on the twenty since the base | Fork commits on the twenty, base..pin |
| --- | --- | --- | ---: | ---: |
| `rocknix/master` | `f6c542872` (2026-10-23T21:57:36+11:00; **delta**: the brief recorded `e282b0562`, and the 4 newer commits touch none of the twenty) | `cada856d8` | **0** (`git rev-list --count cada856d8..rocknix/master -- <20>`) | 115 |
| `batocera/master` | `b2ceb55a7` (2026-10-21T08:16:07+02:00) | `1750dded8` | **7** (`git rev-list --count 1750dded8..batocera/master -- <20>`) | 131 (865 repository-wide) |

The seven batocera commits are dispositioned one by one in `04-analysis.md` § Renovation face Q4.

### Five groups, read in this order

These are brief § 2's groups, with its line numbers taken as leads to re-read:

1. **The launch chain:** `ViewController.cpp`/`.h` (`launch` → `doLaunchGame` → `FileData::launchGame`), `FileData.cpp`/`.h` (`getlaunchCommand` builds the command; `launchGame` holds the gates, the teardown, `game-start`, the command, and the return path through capture, the exit sync, `game-end` and play time), and `LaunchCommand.h` (it reads `-P`, `--core=` and `--emulator=` from a finished command and builds nothing).
2. **The systems table:** `SystemData.cpp`/`.h`. It covers `loadConfig`, the overlays through `loadAdditionnalConfig`, `loadSystem`, the core-over-emulator-over-system command precedence, the emulator and core validated from `system.cfg`, and `rescanIfFolderChanged`.
3. **The save-state five:** `SaveState.*`, `SaveStateRepository.*`, `SaveStateConfigFile.*` (upstream-carried), `SaveStateJobQueue.*`, and `SaveStateBookkeeper.*`, the one background worker under the cloud-sync lock.
4. **The proxy cards:** `ProxyCards.*`. It covers the link's return, `afterSync`, the send card, the top-up and its watcher, the launch gates, and `indexRanOffline`.
5. **The process:** `main.cpp`. It covers the fault handlers, `parseArgs`, `launchStartupGame`, the startup order and startup sync card, and the exit.

### Interacting subsystems (read-only context, never changed here)

These are brief § 2's list. Each has its slice and is read only for the seam:

- `runemu.sh` and `setsettings.sh` (T1, #648): the argument line and `${ARGUMENTS##*-P}`.
- `mk_es_systems` in `projects/ROCKNIX/packages/virtual/emulators` (T3, #650).
- `ThreadedCloudSync`, `CloudTransferJob` and `GuiCloudTransfer` (T18, #665).
- `ApiSystem`, `Settings`, `SystemConf`, `AtomicFileUtil` and `Scripting` (T21, #668).
- `OfflineAchievements` and `raofflineproxy-ctl` (T20, #667), and the proxy (T19, #666).
- `cloud_capture` and `cloud_backup` (T16, #663).
- `GuiSaveState` and `GuiNetPlay` (T31, #678).
- `Platform.cpp`'s launch wrapper, `Window`, `InputManager` and `FileSystemUtil::getEscapedPath` (T35 and T36, #682 and #683).
- The recipe `package.mk` (T37, #684).

A context read of one of them is noted where it is made, and a finding in one is a lead posted on #649 with its slice named.

### The branch scan (brief § 2)

```
for b in $(git -C /home/max/Development/emulationstation-next for-each-ref --format='%(refname:short)' refs/heads/feature/ refs/heads/fix/); do
  n=$(git -C ... log --oneline "$PIN..$b" -- <the 20 paths> | wc -l); [ "$n" -gt 0 ] && echo "$b $n"; done
feature/backup-restore-dialogs 4
feature/cloud-epic 1
feature/restore-relink-wizard 5
```

The scan covered 104 branches, 18 of them `feature/m7-*`. **None of the `feature/m7-*` branches touches the twenty files.** The three branches that do are older and none is in flight, as the brief recorded. So there is no incoming M7 drift on these paths. `test/qa-integration` is at the pin.

### The shipped template's placeholders

From the distribution tree, `grep -rn -o -E '%[A-Z_]+%' projects/ROCKNIX/packages/virtual/emulators/` is re-derived in Phase 2. The guest's generated `/etc/emulationstation/es_systems.cfg` is read when the guest runs, which is queued.

### The #336 line

#336's body, Step 1: *"RetroArch stays the runner for the GL cores and for netplay; the choice is per core in the launcher, and ES does not know which ran."* The runner also gets *"a control channel (a Unix socket: pause, save, load, screenshot, quit) that ES's pages and the exit hotkey talk to instead of RetroArch's config and kill."* Step 3 is the in-process bridge.

So the line is drawn at the RetroArch-specific contract these files hold:

- the save-state half: `SaveStateRepository::isEnabled` (true for the `retroarch` emulator only), the Auto slot, the `-state_file` arguments `SaveState.cpp` builds, and the `.bak` rename-and-restore in `setupSaveState`/`onGameEnded`;
- the `--core=`/`--emulator=` tokens `LaunchCommand.h` reads from the finished command.

Q1, Q5 and Q7 findings confined to those lines are carried as `deferred:#336`. Q2 and Q3 findings on them are fixed regardless (brief § 4). Everything else on the launch path is untouched by Step 1: the gates, the command's quoting, the teardown, the hooks, the exit path and the systems table. ES does not know which runner ran.

### Rules read (`working-principles.md` § Pre-flight)

Read this session:

- **The every-session set**, loaded from the worktree (equal to `next`'s except P1's `fork-workflow.md` and `instruction-files.md`, and the council's `IMPORTED-FROM.md`): `least-surprise`, `player-language`, `time-to-play`, `vm-first`, `bugs-are-agent-first`, `es-native-ui`, `es-player-text`, `es-ui-style-guide`, `es-code-traps`, `engineering-practices`, `upgrade-and-install`, `documentation-accuracy`, `fork-workflow`, `worktrees`, `device-builds`, `release-candidates`, `issue-tracking`, `decision-register`, `learning-capture`, `instruction-files`, `ceremonies`, `working-principles`, `adversarial-council`, `milestone-phase-naming`, `handheld-evidence`.
- **The code-auditor skill:** `SKILL.md`; the references at their phases.

Opened at their phase (Phase 1 records them): `generic-x64-vm-testing.md`'s named sections, `rclone-cloud-sync.md`'s named sections, `change-log.md`, `docs/blindspot-register.md`, and the decisions by ID.
