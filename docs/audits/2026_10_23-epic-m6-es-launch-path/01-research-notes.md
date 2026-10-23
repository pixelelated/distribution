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

## Phase 1 — Research

### 1.1 The spec

The spec is brief § 2 to § 7 and #649's checklist (sixteen criteria, identical to brief § 7). Phase 2's criteria are those sixteen, evaluated at the end of Phase 2. The substance is the seven questions per file (brief § 4) and the coverage table. Two ambiguities are recorded and need no question to the coordinator:

- (a) § 7 item 12 counts `proved:` cells against "the number of guest proofs the running log lists", so each guest proof gets one running-log line.
- (b) Q6's entry-point list includes the `.h` declarations of the three upstream-carried files, which get Q6 and Q4 first (brief § 4). So those rows are written, not skipped.

### 1.2 The issues (named by brief § 3), read for planned changes and leads, not as a work queue

| Issue | State | Bearing on this slice |
| --- | --- | --- |
| #336 | open | Step 1 puts a headless runner in place of RetroArch, chosen per core in the launcher; "ES does not know which ran". The line is drawn in § Scope. |
| #613 | open (M7.P5) | The `/etc/emulationstation/es_systems.cfg` fallback symlink points into a build directory (`package.mk` line 101). On the device the active config is `/storage/.config/emulationstation/es_systems.cfg`. The ES-side seam is `SystemData::getConfigPath`'s fallback order. The fix is the recipe's (T37), not this slice's. A lead to read in group 2. |
| #301 | open | The hash-library fetch is on the interface thread. `ThreadedHasher` is outside the slice; `ProxyCards::indexRanOffline` is its consumer here. |
| #303 | open | The sweep of every fork card and toast (icon, title, a body that does not repeat it). The launch path's toasts and the proxy cards are in its scope. A Q2 lead per card string. |
| #135 | open | Time to play: the Q5 numbers. |
| #10 | open | Save states across build families. The guest cannot show it, and it is not this slice's. |
| #585 | open | The upstream contribution queue, for a fix batocera or ROCKNIX would take. |
| #644, #645 | open | The build-path read and the upstream PR rules. None of their findings ride this slice. |
| #730 | open (T1's PL-030) | `runemu.sh:27-30` cuts `CORE`/`EMULATOR` from the joined line, and the last `--core=` wins. `LaunchCommand.h` reads whole words, also last wins. The seam is two readers of one argument line. |
| #300, #310, #117, #198, #246, #245, #299, #90, #92 | closed | History for these files (below). |
| #120 | **open** | Automated VM testing. **Delta:** brief § 3 lists #120 among the closed. It is open, which does not change the reading. |

### Closed `bug` issues that name these files (brittleness evidence; leads for sibling sites, Phase 3.6.5)

Pattern `\b(launchGame|FileData|SystemData|ViewController|SaveState\w*|ProxyCards|LaunchCommand|es_systems)\b|\bmain\.cpp\b` over title and body of the 139 closed `bug` issues: **14** match: #101 #114 #149 #183 #205 #206 #207 #209 #210 #246 #275 #300 #305 #520. Each is opened in Phase 3.6.5 where its shape recurs.

### 1.3 Git history (ES, `cada856d8..$PIN`, the fork's own)

Fork commits per path: `main.cpp` 42, `FileData.cpp` 40, `ProxyCards.cpp` 23, `SaveStateBookkeeper.cpp` 7, `ViewController.cpp` 6, `SystemData.cpp` 6, `SaveState.cpp` 5, `SaveStateBookkeeper.h` 4, `ProxyCards.h` 4, `FileData.h` 3, `SaveStateRepository.cpp` 2, `SystemData.h` 2, `ViewController.h` 2, `LaunchCommand.h` 2, `SaveStateRepository.h` 1, `SaveStateJobQueue.*` 1 each. The three upstream-carried files have 0 (last touched 2023-10).

The churn is in `main.cpp` and `FileData.cpp` (the cloud-folder boot work of 2026-10-01 to 2026-10-07, the identity rename, and the scan release of `e6e1e4d0f`), and in the fix rounds of 2026-09-28 (#307 and #313, streams E1 and E2: the capture gate's bound, the bookkeeper under the transfer lock, `LaunchCommand` whole words, the rotation record). The last commit on the pin, `16dbac521` (`GuiWifi: cancel scan worker on normal frontend exit`), touches `main.cpp`.

### 1.4 Documentation and constraints

These are the rules of § Scope § Rules read. The decisions cited by brief § 3 are read from `docs/decision-register.md` as each is cited in a finding, by ID, and never re-argued.

### 1.5 Prior audits: the provenance map (verdicts sequestered until after Phase 2)

| Audit | Tier | Lines in its punch list naming these files (`grep -c`, brief § 3's pattern) |
| --- | --- | ---: |
| `2026_09_25-milestone-rc-round-since-258` | milestone | 24 |
| `2026_09_24-milestone-rc-round-since-186` | milestone | 21 |
| `2026_09_28-milestone-audit-of-the-fix-round` | milestone | 7 |
| `2026_09_13-milestone-stable-before-upstream` | milestone | 6 |
| `2026_09_12-milestone-cloud-saves-since-60` | milestone | 4 |
| `2026_09_28-milestone-audit-of-the-fixes-307` | milestone | 4 |
| `2026_10_06-milestone-m7-p4-fixes-383` | milestone | 2 |
| `2026_10_14-milestone-m7-next-candidate` | milestone | 2 |

These are provenance only. Each was a milestone diff audit over a range, never a line-by-line read of these files whole, so the slice's own read is the first. Their verdicts are opened after Phase 2's own entries are written (plan § 7 item 3).

### 1.6 Research Summary

- **Planned:** a line-by-line read of 20 shipped ES files (11,287 lines) under the seven questions, at Extended depth.
- **What exists:** the slice issue #649, the area epic #700, and the seams with T1 (#648, #730) and T18, T20, T21, T31, T35 and T36 by name.
- **Code changed since the merge base:** 115 fork commits, concentrated in `main.cpp`, `FileData.cpp` and `ProxyCards.cpp`.
- **Constraints:** the host is held for M7, so every runtime proof is queued; nothing builds; ES fixes are stage E's, after the stream briefs.
- **Red flags carried into Phase 2** (leads, from the brief's seam map, each to be re-read):
  - raw `FileData*` across the gates' waits while `rescanIfFolderChanged` may delete them;
  - `mRunningGame` read off the interface thread;
  - `%BASENAME%`/`%ROM_RAW%` raw and `formatCommandLineArgument` quoting only on a space;
  - the ROCKNIX netplay client branch computing values it never uses;
  - the overlay `return` at `SystemData.cpp` 1042/1049;
  - the unlocked static cache in `SaveStateConfigFile`;
  - `renumberSlots` with no caller;
  - the boot-game replay with no events;
  - the `onGameEnded` comment that disagrees with its code.
