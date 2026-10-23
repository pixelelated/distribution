# Brief: M6.P2 T2, EmulationStation's launch path (#649)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #649 differ, #649 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-23):** written after T1's brief went through its futro and a
stranger's proof (`docs/reviews/briefs/os-launch-control-state.md` § 10),
so the shapes those found wrong are answered here from the start; this
version goes through the same two readings before dispatch, and version 2
records what they found.

## 1. Identity

- **Issue:** #649 `M6.P2 E700/T2: interface: EmulationStation's launch
  path`, slice `es-launch-path` in `docs/reviews/slices.json`, second in
  `docs/reviews/order.md` (the order's row is on the P1 branch). **Epic:**
  #700, the interface (T2, T18, T20, T21, T26, T31 to T37, T44), under the
  renovation epic #339; its futro is the comment on #700 and
  `docs/futros/2026-10-23-m6-interface.md`. **Milestone:** M6 (`M6:
  Codebase renovation`); its body holds the live order; read it first.
  **Predecessors:** #346 (the plan), #641 (the survey, the inventory and
  the order; closed 2026-10-23). **Beside it:** T1, #648, in its own lane
  (the maintainer's call of 2026-10-23, D-WORKFLOW-190: slices in different
  areas run in parallel; two slices never share a path). **The dispatch** is
  the coordinator's comment on #649 that names this brief's commit, the
  model and effort, and authorizes the two external reviewer calls and the
  `npm install` of § 1; the lane's first comment answers it.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, re-order anything, change a criterion, write a
  brief, move the M6 body, edit `slices.json`, `areas.json`, `order.md` or
  the plan, bump the EmulationStation pin in the distribution, or decide a
  question of scope: those are the coordinator's, reached through #649, one
  question at a time. What this lane does file: its own audit punch-list
  issue (stage D, the code-auditor skill's Phase 6) and a `bug` issue for
  every defect it finds (D-WORKFLOW-187: a defect found by the renovation
  is a bug like any other; `bugs-are-agent-first.md` gives the shape, with
  its VM-verifiable criterion). Nothing else.
- **Two worktrees, one session.** The slice's sources are in a separate
  repository, so the lane holds two worktrees and writes in both (plan § 11
  item 4: an ES slice runs in an ES worktree with the distribution
  checkout's rules, D-WORKFLOW-010):
  - **The distribution worktree**, where the audit artifacts, the work log,
    the pointer and every ceremony live: branch
    `feature/m6-es-launch-path-649` at
    `/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649`,
    created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
    `2174265e9c`** (which carries the P0 branch), with the coordinator's tip
    merged in and the lane's pointer seeded (the two hashes are in the
    dispatch comment on #649). The coordinator wrote there only before the
    lane started; from the dispatch on, one session per worktree
    (D-WORKFLOW-183) and the coordinator writes nothing there. **The rules
    in this worktree are `next`'s except three files:** P1's
    `fork-workflow.md` and `instruction-files.md` (the three renovation
    tools added to the fork-tool lists) and the council skill's
    `.claude/skills/council/IMPORTED-FROM.md` (M7's Argon route, cherry-picked
    onto the coordinator branch as `033eb7ed23`, `0ceb2994c5`,
    `6874394d49`); the first commands check it. The primary checkout is
    `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025).
    `worktrees.md`, `device-builds.md`, `CLAUDE.md` and `AGENTS.md` still
    name the legacy layout (`/workspace/repos/rocknix`,
    `rocknix.worktrees/`); #640 owns that drift, and this brief's paths are
    the ones to use. The legacy checkout and every worktree beside it are
    the M7 lane's: read from them (an image, a build root, a diff), never
    write.
  - **The EmulationStation worktree**, where the sources are read and the
    fixes are made:
    `/home/max/Development/emulationstation-next.worktrees/m6-es-launch-path-649`,
    branch `feature/m6-es-launch-path-649`, created by the coordinator on
    2026-10-23 from **the pin**
    `16dbac5211eea7e70db7394372033be2be7df829` (what
    `projects/ROCKNIX/packages/ui/emulationstation/package.mk` line 5 names;
    the tip of `test/qa-integration`, 2026-10-15). Its `build-tests/` is
    gitignored and holds the unit tests the coordinator built once as proof
    (§ 5). The repository's own `AGENTS.md` and `CLAUDE.md` are pointers to
    the distribution's rules (D-WORKFLOW-010), and its hooks path is the
    absolute `.githooks` of the `qa-integration` worktree, shared by every
    worktree there: the credential scan runs on every commit. **The primary
    checkout `/home/max/Development/emulationstation-next` is on somebody
    else's branch, and the `qa-integration` and `m7-*` worktrees beside it
    are the M7 lane's: never check anything out there, never write there;
    read an upstream ref with `git -C <primary> show <ref>:<path>`.** The ES
    remotes: `rocknix` and `upstream` are `ROCKNIX/emulationstation-next`
    (`rocknix/master` is the fresher fetch, `e282b0562` of 2026-10-22, the
    inventory's upstream); `batocera` is
    `batocera-linux/batocera-emulationstation` (`batocera/master`
    `b2ceb55a7` of 2026-10-21, the upstream's upstream); `origin` is
    `pixelelated/emulationstation`, where the branch is pushed.
- **Model and effort:** Opus 5.5 at high effort (the maintainer, 2026-10-22:
  *"the work will be Opus 5.5"*), unless the dispatch says otherwise.
  Record what actually ran in `00-running-log.md`'s header.
- **Review depth: Extended** (plan § 6c; `slices.json`: launch path). The
  primary auditor is this lane (Anthropic). The two reviewers come from two
  other labs, each through the Facilitator and nothing else (D-WORKFLOW-049,
  D-WORKFLOW-137; `adversarial-council.md` rule 4; the code-auditor skill's
  Phase 4.6):
  - **GPT-6 Astra**: `tools/council/run invoke --member gpt --provider
    openrouter --prompt-file <brief> --output <file>` at `max`, the installed
    recipe (`openai/gpt-6-astra`, provider pinned to OpenAI).
  - **Gemini 4 Argon** (Google): `--member gemini-argon --provider
    openrouter` at `high`. **Its route is in this tree**: the coordinator
    branch carries M7's three commits (`fac2129787`, `1c7d283ad5`,
    `a7a3bdda4e` cherry-picked, #636/#638), so `grep -c gemini-argon
    scripts/council-invoke.ts tools/lint-audit-artifacts` prints `7` and `4`,
    and T1 ran the seat on 2026-10-23 (served `google/gemini-4-argon` by
    `Google`, 527 s). The roster's `--member gemini` is never called in its
    place. A seat that fails identity verification is recorded as pending,
    never replaced, and at Extended depth that is the Phase 4.6 blocker
    (§ 8).
  - Both reviewers run the **refutation pass alone** (the audit is epic
    tier; phases.md § Phase 4.6: two calls at Milestone tier, one otherwise),
    each prepared independently. `second-opinions/review-plan.json` is
    written before the first call (`templates.md` § Second opinion: depth
    `extended`, primary `anthropic/claude-opus-5-5`, lab `anthropic`,
    identity source the dispatch comment and the session's own metadata,
    two reviewers). Every seat item is a lead; the orchestrator re-reads the
    artifact before a row is written.
  - The runner's dependencies are not in a fresh worktree: `tools/council/run`
    execs `tools/council/node_modules/.bin/tsx`, and `node_modules/` is
    gitignored. Install once, before Phase 4.6, with `npm install --prefix
    tools/council` in the distribution worktree (a gitignored write; the npm
    registry; `node` v24 and `npm` 11 are on the host; record the `tsx`
    version in `00-running-log.md`), then `tools/council/run verify-pins`
    must print its `OK` line and `tools/council/run test` must pass (T1 saw
    routing 127/127). The key is sourced from `~/.config/council/env`
    (present, never read into a transcript, never on a command line). The
    dispatch comment on #649 is the authorization for exactly these two
    external calls plus a probe of each seat first, its provenance naming
    the served model. **During the host handoff of § 5 the install waits
    too**: it is not a compiler, but the agreement with the M7 lane says no
    new runtime of any kind until the return line.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649
W=/home/max/Development/emulationstation-next.worktrees/m6-es-launch-path-649
PIN=16dbac5211eea7e70db7394372033be2be7df829
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-es-launch-path-649
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md   # exactly fork-workflow.md, instruction-files.md, .claude/skills/council/IMPORTED-FROM.md; any other file is STALE
grep -n 'PKG_VERSION=' projects/ROCKNIX/packages/ui/emulationstation/package.mk    # the pin above; record it
git -C "$W" branch --show-current                                   # feature/m6-es-launch-path-649
[ "$(git -C "$W" rev-parse HEAD)" = "$PIN" ] || echo "the ES worktree is not at the pin: stop"
git -C "$W" status --short                                          # nothing tracked modified; build-tests/ is ignored
git -C "$W" fetch rocknix --no-tags && git -C "$W" rev-parse --short rocknix/master   # record it: Q4's upstream for the ES side
git -C "$W" merge-base "$PIN" rocknix/master                        # cada856d8 on 2026-10-23; record it
test -f docs/reviews/briefs/es-launch-path.md || { echo "the brief is not in this tree: stop"; exit 1; }
test -f docs/futros/2026-10-23-m6-interface.md || echo "the epic's futro is not in this tree: ask the coordinator before the first audit commit"
cat .github/sessions/saved-session-state-feature-m6-es-launch-path-649.md   # the lane's seeded pointer
```

The order of the first session: § 3's reading first (it is the pre-flight,
`working-principles.md`; it fills the first hour), then stage A.

## 2. Scope

**Twenty files of the EmulationStation fork, read line by line.** The
membership is the inventory's: the rows whose `tree` is `es` and whose path
matches the four globs in `slices.json` (`es-app/src/{FileData,SystemData,LaunchCommand,ProxyCards}.*`,
`es-app/src/main.cpp`, `es-app/src/SaveState*`,
`es-app/src/views/ViewController.*`); #649 says the same set as
`tools/renovation-inventory --order`'s membership (the filter below is the
re-derivation, because `--order` writes files).

**The hash.** The slice's bytes are the pin's, `16dbac5211`, which is what
`next` builds (`package.mk` line 5) and what the ES worktree is at; the
first commands prove both. **`reviewed-at:` is the distribution branch's
`HEAD` at stage A** (the commit the read is made at), recorded with the pin
beside it in `00-running-log.md` and `01-research-notes.md` § Scope; the
ES worktree's `HEAD` at stage A is the pin itself. The stop (§ 8) is the ES
worktree not at the pin, or the distribution branch not on the P1 tip: then
the slice was re-based under the read and the coordinator re-baselines it.
`next` moving later is not a stop; it is drift, below.

**The counts, recorded by the survey at `eb4763e3cc` and re-derived here.**
A count that differs is a delta beside the recorded one, not a stop; the
stop is a count that cannot be produced, or two commands for one quantity
that disagree. The inventory's line count is git's numstat against the
empty tree (`docs/reviews/README.md`), which counts a file's last line
without a newline where `wc -l` does not:

```bash
python3 -I - <<'PY'
import json, re
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
pat = re.compile(r"^es-app/src/(FileData|SystemData|LaunchCommand|ProxyCards)\.[^/]+$|^es-app/src/main\.cpp$|^es-app/src/SaveState[^/]*$|^es-app/src/views/ViewController\.[^/]+$")
t2 = [r for r in rows if r["tree"] == "es" and pat.match(r["path"])]
print("paths", len(t2), "lines", sum(r["lines"] or 0 for r in t2),
      "fork-own", sum(1 for r in t2 if r["tier"] == "fork-own"),
      "upstream-carried", sum(1 for r in t2 if r["tier"] == "upstream-carried"),
      "fork-own lines", sum(r["lines"] or 0 for r in t2 if r["tier"] == "fork-own"))   # 20, 11287, 17, 3, 10804
for r in sorted(t2, key=lambda r: -(r["lines"] or 0)): print(r["lines"], r["tier"], r["reach"], r["path"])
PY
git -C "$W" ls-files 'es-app/src/FileData.*' 'es-app/src/SystemData.*' es-app/src/LaunchCommand.h 'es-app/src/ProxyCards.*' es-app/src/main.cpp 'es-app/src/SaveState*' 'es-app/src/views/ViewController.*' | wc -l    # 20
git -C "$W" diff --numstat "$(git -C "$W" hash-object -t tree /dev/null)" "$PIN" -- $(git -C "$W" ls-files 'es-app/src/FileData.*' 'es-app/src/SystemData.*' es-app/src/LaunchCommand.h 'es-app/src/ProxyCards.*' es-app/src/main.cpp 'es-app/src/SaveState*' 'es-app/src/views/ViewController.*') | awk '{s+=$1} END {print s}'   # 11287
```

Recorded: **20 paths, 11,287 lines, all read line by line** (11,284 by `wc
-l`); **17 fork-own paths, 10,804 lines; 3 upstream-carried** (`SaveState.h`,
`SaveStateConfigFile.cpp`, `SaveStateConfigFile.h`: byte-identical to
batocera's, 483 lines). Every path is `reach: shipped`: the binary
`/usr/bin/emulationstation` on every image, built with `-DROCKNIX=1`
(`package.mk` line 19), so every `#if ROCKNIX` branch is the one that ships
and every `#else` is upstream's. **Upstream's side of Q4:** zero commits on
`rocknix/master` touch these twenty files since the merge base `cada856d8`
(2026-09-23), and 115 fork commits do; the deeper upstream,
`batocera/master`, has seven commits on them since its merge base with the
pin, `1750dded8` (2026-09-13), with 865 fork commits on the other side (the
numbers of 2026-10-23; the first commands record the refs). The closed
`bug` issues that name these files are Phase 1's: `gh issue list --repo
pixelelated/distribution --label bug --state closed --limit 500 --json
number,title,body`, grepped with word boundaries for `launchGame`,
`FileData`, `SystemData`, `ViewController`, `SaveState`, `ProxyCards`,
`LaunchCommand`, `es_systems`, `main.cpp` (the count depends on the pattern,
so record the pattern with the count).

**Where the code runs on the image.** The one binary, started by
`essway.service` (`generic-x64-vm-testing.md` § The interface runs under
`essway.service`), reads `/etc/emulationstation/es_systems.cfg` (generated
at build time by `projects/ROCKNIX/packages/virtual/emulators`, T3's; the
user's `es_systems_custom.cfg` and `es_systems.cfg` under the config path
come first, `SystemData::getConfigPath`; #613 is open on the fallback
symlink), `es_settings.cfg` (`Settings`) and `system.cfg` (`SystemConf`,
the launch scripts' store), and runs the command the template gives it
through `system()` with a wrapper that captures stdout to
`es_launch_stdout.log` (first 300 lines) and stderr to
`es_launch_stderr.log` under the log path (`es-core/src/utils/Platform.cpp`
lines 160 to 168, out of scope, T35's; read for context). The game-start
and game-end hooks run scripts from `/usr/bin/scripts/<event>/` and the
user's (`Scripting::fireEvent`, T33's). The launch API the harness uses is
`POST /launch` on `127.0.0.1:1234` (`services/HttpServerThread.cpp` line
625 calls `ViewController::launch`; `/isIdle` gates it, D-QA-057).

**Five groups, read in this order** (the slice's reason to be second is the
launch path, read before #336 Step 1 replaces what sits under it; plan
§ 6a, `slices.json`'s `why`). Line numbers are the pin's, from a read-only
seam map the coordinator re-derived on 2026-10-23; each is a lead to
re-read, not a verdict:

1. **The launch chain** (on the order's launch-path list):
   `views/ViewController.cpp` (1,531) and `.h` (158): `launch` at line 533
   (`checkLaunchOptions`, the image viewer, the netplay downgrade, input
   locked, the splash, the transition animation whose end calls
   `doLaunchGame` at 476, which calls `game->launchGame(mWindow, options)`
   at 483); the return animation closes the splash and unlocks input.
   `FileData.cpp` (2,680) and `.h` (293): `getlaunchCommand` at 536
   **builds the command** from `system->getLaunchCommand(emulator, core)`
   (607) by sequential placeholder substitution (618 to 630: `%ROM%`
   through `getEscapedPath`, `%BASENAME%` and `%ROM_RAW%` raw, `%GAMENAME%`
   and `%SYSTEMNAME%` through `formatCommandLineArgument` at 528, then the
   controllers blob, `%NETPLAY%` under `#if ROCKNIX` with `shellQuote` at
   678, `-monitor`, and the save-state arguments from `SaveState.cpp`);
   `launchGame` at 928: the gates (a capture still recording, 876 to 926; a
   sync running, 993 to 1008, with the STOP IT AND PLAY / KEEP WAITING
   question of D-UI-096; a transfer running, 1010 to 1022; an achievements
   send, 1031 to 1043; a top-up, 1045 to 1057; `launchWhenGone` at 818 polls
   to 20 s), the audio and window teardown (1071 to 1080), `fireEvent
   ("game-start")` at 1086, the command through `ProcessStartInfo` at 1100
   to 1103, then the return: save states' `onGameEnded` (1117), the capture
   command built with `shellQuote` (1144 to 1154) and run on a detached
   thread (1268 to 1317) that starts the exit sync card
   (`ThreadedCloudSync::start`, 1308, D-UI-040/D-UI-095) unless another
   game launched since, `fireEvent("game-end")` at 1174, the window re-init
   (1176 to 1184), play count and time on exit 0 (1192 to 1209), the error
   box for exit codes 200 to 300 (1324). **`LaunchCommand.h` (57) builds
   nothing: `launchToken` (28) and `launchArgument` (51) read a finished
   command's `-P`, `--core=` and `--emulator=` tokens the way `runemu.sh`
   reads them** (its header says so; `es-app/tests/unit/LaunchCommandTests.cpp`
   checks both readings against each other), used at `FileData.cpp` 719 to
   720 and `main.cpp` 551 to 559. Callers from outside the slice:
   `SystemScreenSaver.cpp` line 546 calls `FileData::launchGame` directly,
   past `ViewController`'s checks; `ViewController::launch` is called from
   the five game-list views, `GuiGameOptions`, `GuiGameAchievements`,
   `GuiRetroAchievements`, `GuiNetPlay` and the HTTP API; `GuiMenu.cpp`
   line 11325 stores `getlaunchCommand(false)` as `global.bootgame.cmd`.
2. **The systems table**: `SystemData.cpp` (2,583) and `.h` (296):
   `loadConfig` at 1137 (a missing or unparseable file is the QUIT box in
   `main.cpp` at 860), the overlays `es_systems_*.cfg` merged tag by tag in
   `loadAdditionnalConfig` at 1024 (**an unparseable overlay `return`s at
   1042 and 1049, so every later overlay is skipped**, upstream's shape),
   `loadSystem` at 1377 (the `<command>`, `<emulator>` and `<core>` entries;
   a system without name, path, extensions or command is dropped), the
   precedence core `command=` over emulator `command=` over the system's
   (`getLaunchCommand`, 2219), the emulator and core chosen from `system.cfg`
   and validated against the table (2132 to 2217), and
   `rescanIfFolderChanged` at 382 (**deletes `FileData` for files gone from
   disk**, 456 to 473; skipped while the hasher, the scraper or a game
   runs; #246's lesson, `es-code-traps.md` § A rescan that deletes FileData
   drops the view first).
3. **The save-state five** (`SaveStateBookkeeper.*` and
   `SaveStateRepository.*` are on the order's state-preservation list):
   `SaveState.cpp` (240) and `.h` (60): `setupSaveState` renames the auto
   state and its screenshot to `.bak` and copies the chosen state over it
   (117 to 156), `onGameEnded` restores (164 to 190; the comment at
   `FileData.cpp` 1134 says it renumbers slots, and 192 to 198 say it does
   not); `-state_file "<name>"` is double-quoted (77, 97, 111).
   `SaveStateRepository.cpp` (342) and `.h` (53): the per-system map,
   `isEnabled` true only for the `retroarch` emulator (211 to 228),
   `renumberSlots` (251 to 277) with **no caller**. `SaveStateConfigFile.*`
   (337, 86): `es_savestates.cfg`, upstream-identical, a singleton behind a
   mutex with an unlocked static cache (271 to 336). `SaveStateJobQueue.*`
   (62, 72): pure, no I/O, used only by the bookkeeper.
   `SaveStateBookkeeper.cpp` (344) and `.h` (71): **the one background
   worker**, which runs `/usr/bin/cloud_capture --retire --unlink` and
   `--adopt` with every argument `shellQuote`d (182 to 229) under an
   exclusive `flock` on `/var/run/cloud_sync.lock` (124 to 129), joined at
   exit (`main.cpp` 352 and 1333). The bookkeeper and the queue are not on
   the launch path: `GuiSaveState.cpp` (T31's) calls them; the launch path
   calls the repository (`FileData.cpp` 703 to 710, 782, 804, 1120) and
   `SaveState` (713, 1118).
4. **The proxy cards**: `ProxyCards.cpp` (596) and `.h` (58): the link's
   return (`linkReturned` from `NetworkThread.cpp` 237), `afterSync` (from
   `ThreadedCloudSync.cpp` 755), the send card, the top-up and its watcher
   (D-UI-101, D-UI-109, D-RA-035), the launch gates `sendRunning`,
   `topUpRunning`, `stopTopUp` (553 to 586; `SIGTERM` to the pid in
   `/var/run/raofflineproxy-scan.lock`), `indexRanOffline` (from
   `ThreadedHasher.cpp`); every worker detached; the stamps read under
   `/storage/.cache/cloud_sync/` and `/storage/.config/raofflineproxy/`,
   the stamp written `last-sync-link`; `raofflineproxy-ctl` through
   `OfflineAchievements.cpp` (T20's).
5. **The process**: `main.cpp` (1,368): the fault handlers (710 to 728;
   `signalHandler` at 411 writes the backtrace to stderr only), `parseArgs`
   (82 to 260), `launchStartupGame` at 527 (**replays `global.bootgame.cmd`
   from `system.cfg` with no game-start or game-end event and no
   `mRunningGame`**, then `cloud_capture` with the tokens `launchToken` and
   `launchArgument` read), the startup order to the main loop at 1158, the
   startup sync card (622 to 693), the exit (1256, 1322 to 1360:
   `SaveStateBookkeeper::shutdown`, `ViewController::saveState`,
   `deleteSystems`, `processQuitMode` touching `/tmp/restart.please`,
   `reboot.please` or `shutdown.please` for a supervisor outside the slice).

The launch-path list names seven of these (`FileData.*`, `SystemData.*`,
`LaunchCommand.h`, `ProxyCards.*`, `main.cpp`, `ViewController.*`), the
state list four (`SaveStateBookkeeper.*`, `SaveStateRepository.*`);
`order.md` § The security, state-preservation and launch-path files. A
finding in one of them is Extended-depth material by definition.

**Interacting subsystems, read-only context** (never read line by line here,
never changed here; a defect found in one is a lead posted on #649 for its
own slice): `runemu.sh` and `setsettings.sh`, what the command runs and the
settings it writes per launch (T1, #648, beside this lane; the seam is the
argument line the template gives and `runemu.sh` parses, `${ARGUMENTS##*-P}`
and the `--core=`/`--emulator=` tokens, which `LaunchCommandTests.cpp`
checks from this side); `es_systems.cfg`'s generator
`projects/ROCKNIX/packages/virtual/emulators` (`mk_es_systems`, T3, #650);
`ThreadedCloudSync`, `CloudTransferJob` and `GuiCloudTransfer`, the cards
and page a launch asks over (T18, #665); `ApiSystem`, `Settings`,
`SystemConf`, `AtomicFileUtil`, `Scripting` (T21, #668; `ApiSystem.cpp`
line 2263's `executeScriptLegacy` is the popen every script call goes
through); `OfflineAchievements` and `raofflineproxy-ctl` (T20, #667; the
proxy itself T19, #666); `cloud_capture` and `cloud_backup`, the scripts
the exit path runs (T16, #663); `GuiSaveState` and `GuiNetPlay` (T31,
#678); `es-core`'s `Platform.cpp` wrapper, `Window`, `InputManager` and
`FileSystemUtil::getEscapedPath` (T35 and T36, #682 and #683); the
distribution's recipe `package.mk` (T37, #684). The two configuration
stores, `es_settings.cfg` and `system.cfg`, are the state this slice reads
and writes; where a key is written (the netplay nickname at `FileData.cpp`
653 to 657; `LastSystem` at `ViewController.cpp` 92 to 93), say so.

**Known incoming drift: none from M7.** The candidate image
`069fc2704421` carries the same pin (`package.mk` unchanged there,
read 2026-10-23), so the binary on the image is the slice's bytes, with
only the build-time flags and credentials on top (`device-builds.md` §
Build credentials). The ES fork's integration branch `test/qa-integration`
is at the pin; the M7 lane's `m7-*` ES worktrees are ahead of it on their
own branches and are not this slice's concern until a pin moves, which is
drift the tool reports (plan § 8). The swarm rule holds the other way: a
punch item that would touch a file an open M7 ES branch changes is
announced on #649 before any stream brief is written (`git -C <primary>
log --oneline $PIN..<branch> -- <file>` over the `m7-*` branches lists
them; read-only).

**Out of scope here:** every other ES file (`GuiSaveState.cpp`,
`ThreadedCloudSync.cpp`, `ApiSystem.cpp`, `Platform.cpp`, `Scripting.cpp`,
`InputManager.cpp`, the views), the launch scripts, the systems generator,
the cloud scripts, the proxy, the recipe. A reading of one of them for
context is noted as such in `01-research-notes.md`; a finding in one is a
lead for its slice, posted on #649 with the slice named.

## 3. Read first

From `next`, in this order, before any analysis (this is the first
session's first hour; stage A follows it):

- `.github/sessions/saved-session-state-next.md` (the M7 lane's canonical
  checkpoint; read for what runs on this host, not for a work queue) and
  this lane's own pointer. The ES repository's `AGENTS.md` and `CLAUDE.md`
  at the pin (pointers; they name the syntax check and the integration
  branch).
- The code-auditor skill whole: `.claude/skills/code-auditor/SKILL.md` and
  its `references/phases.md`, `review-levels.md`, `templates.md`,
  `anti-patterns.md`. The slice runs under its lifecycle with the renovation
  face added (plan § 6b); stage B's Phase 2 criteria are #649's checklist,
  and Phase 3 carries § 4 below as its renovation face beside the skill's
  own faces.
- The four EmulationStation rules whole, with the sections that bind this
  slice: `es-native-ui.md` (§ Core patterns: the OS event hooks, `exists
  (path, false)`, the gating; § The cards at the link's return; § Spacing's
  four surface tiers and the D-UI-078, D-UI-093 and D-UI-095 paragraphs;
  § Before the pin moves; § A layout must not be computed from what it last
  produced), `es-player-text.md` (§ Conventions: the question over a
  running job, D-CLOUD-130 and D-UI-096; the outcome vocabulary; every fork
  string in English and French, D-UI-051), `es-code-traps.md` (§ A rescan
  that deletes FileData drops the view first; § A file under three bytes;
  § Pure text has a home, and a test; § A pooled connection with the link
  gone; § Comments near a translatable string must be ASCII; § Three things
  a font is not, for `exists`'s cache), `es-ui-style-guide.md` (§ Keep the
  flow and its visual evidence together, D-WORKFLOW-155/156: a behaviour
  change on the launch path updates `docs/es-menu-map.md`'s flow and files
  its frames; § Confirmations: YES first, the back-button accelerator).
- Rules whose `paths:` match or whose subject is this slice:
  `generic-x64-vm-testing.md` (§ Headless; § A launch, a START or a walk
  waits for the interface to be idle, D-QA-057; § Driving EmulationStation
  from the monitor; § Fixtures for the launch path; § Crash and hang
  recipes; § The interface runs under `essway.service`; § A settings change
  made from the shell is invisible to the running interface; § A RetroArch
  frame is evidence only when its surface was the panel; § Spin a guest
  down; § After every VM cycle); `rclone-cloud-sync.md` (the exit sync and
  the capture the launch path starts: § Critical gotchas, § The bounded
  automatic sync, § What the audit's fixes changed); `time-to-play.md` whole
  (the two numbers are this slice's Q5); `least-surprise.md` and
  `player-language.md` (the gates' questions are strings a player reads);
  `handheld-evidence.md` (the crash handler's trace and where it lands);
  `upgrade-and-install.md` whole (every fix answers *Already written*,
  D-WORKFLOW-050; the save-state files and the stamps are what a device
  already has); `change-log.md`. Then the every-session set:
  `engineering-practices.md` (§ Change stays inside the fork's lanes,
  D-UI-079; § Verify design intent; § Verify the artifact; § A name is not
  a behaviour; § Guards must fail closed; § Before deleting a duplicate;
  § Stop after three fixes; § Fail gracefully; § Nothing runs on a person's
  device; § Never edit a shell tool in flight), `bugs-are-agent-first.md`,
  `vm-first.md`, `issue-tracking.md`, `decision-register.md`,
  `learning-capture.md`, `ceremonies.md`, `worktrees.md` (removal; its
  layout is superseded, § 1), `fork-workflow.md` (the ES work reaches
  upstream as the package bump in the distribution, D-WORKFLOW-012),
  `milestone-phase-naming.md`, `adversarial-council.md`,
  `working-principles.md` (§ Pre-flight: say which rules were read),
  `device-builds.md` § Iterating on EmulationStation and § Reading a crash
  (the unstripped binary and `llvm-addr2line` in the build root). Known
  stale facts so they do not cost an hour (#640): the legacy paths in
  `worktrees.md`, `device-builds.md`, `instruction-files.md`, `AGENTS.md`,
  the ES pointers' `/workspace/repos/rocknix`, and `tools/es-syntax-check`'s
  default root (#699, § 5).
- `docs/blindspot-register.md` whole, once (73 entries). The entries that
  touch these files: **35** (a remedy built on an audit's claim about a
  default nobody read), **44** (proven at a fixture's size, not the
  device's: a row refreshed hundreds of times), **49** (an edit made blind
  to the compiler: the syntax check before the pin moves), **54** and
  **63** (a measurement on a guest whose renderer was not the device's;
  `--vm` and the renderer read), **59** (a memory measurement that passed
  on a page that never loaded), **64** (a wait lengthened three times for
  an event the code had no path to produce: the gates' polls), **65** (a
  proof's substitute passed where the real input failed); and the general
  ones a reading repeats: 7 (host tools are not the device's), 13 (assumed
  done), 30 (a resumed session built on its own summary), 46 (a name read
  as a behaviour), 51 (an open checkbox is a claim), 73 (a monitor of
  completion, not activity).
- Prior audits of these files under `docs/audits/`, **as provenance only**:
  which files were audited, when, at what tier; verdicts are sequestered
  until Phase 2.5 and never transcribed into Phase 2. The punch lists that
  name them, counted with `grep -c -E
  'FileData|launchGame|ViewController|SaveState|ProxyCards|SystemData\.cpp|LaunchCommand|main\.cpp'
  05-punch-list.md`: `2026_09_25-milestone-rc-round-since-258` (24),
  `2026_09_24-milestone-rc-round-since-186` (21),
  `2026_09_28-milestone-audit-of-the-fix-round` (7),
  `2026_09_13-milestone-stable-before-upstream` (6),
  `2026_09_12-milestone-cloud-saves-since-60` (4),
  `2026_09_28-milestone-audit-of-the-fixes-307` (4),
  `2026_10_06-milestone-m7-p4-fixes-383` (2),
  `2026_10_14-milestone-m7-next-candidate` (2).
- Decisions by ID, cited and never re-argued. The launch path and its
  gates: D-CLOUD-038 and D-CLOUD-053 (a sync that can touch saves gates
  the launch; every writer of the saves tree inside ES under the transfer
  lock), D-CLOUD-072 (ES owns the startup sync), D-CLOUD-076 then
  D-CLOUD-109 (a launch cancelled an automatic sync; now it waits, bounded;
  `time-to-play.md` says both are true of different builds, so read the
  code for which ships), D-CLOUD-112 and D-CLOUD-119 (the offline benchmark
  and the budgets), D-CLOUD-113 (two contracts, never one budget),
  D-CLOUD-136 (the startup card's WAITING FOR A NETWORK line), D-CLOUD-098
  (time to play), D-UI-095 and D-UI-096 (anything automatic that moves
  data is shown; the question's three parts), D-UI-078 and D-UI-093 (long
  work on a foreground page; one floating surface at a time), D-UI-101,
  D-UI-109 and D-RA-035 (the cards at the link's return; the top-up is two
  things), D-UI-040 (the automatic cards say *sync*), D-LAUNCH-001 (an exit
  by the hotkey's signal reads as a clean exit; the exit-code contract
  `launchGame` reads), D-LAUNCH-004 (`/var/log/exec.log` is one launch's),
  D-CLOUD-062 (the frozen pair read from the finished command line:
  `launchedEmulator`/`launchedCore`), D-RA-018 (the startup index runs
  whether or not the splash is shown; `SystemData::loadConfig`), D-QA-057
  (`/isIdle`). State: D-CLOUD-077/078 (fail gracefully; the last known good
  state), D-UI-050 (the save state manager's sheet; the files these classes
  own), D-WORKFLOW-050 (*Already written*). The interface at large:
  D-UI-039 (the menu map), D-UI-051 (French), D-UI-042/045, D-UI-079
  (change stays inside the fork's lanes: it governs a player-visible
  behaviour change to an upstream surface, which is put to the maintainer
  first through the coordinator; a defect or cruft in upstream-carried
  code is this program's to find and fix, #339's Tier 2 words: *"there is
  no longer anyone to send them to"*), D-WORKFLOW-155/156 (flow and frame
  evidence with every ES change), D-WORKFLOW-010 and D-WORKFLOW-012 (one
  rule corpus; ES reaches upstream through the distribution). The program:
  D-WORKFLOW-181, 183, 184, 185, 186, 187, 189, 190; D-WORKFLOW-137 (depth
  and the reviewer's lab), D-WORKFLOW-049 (every seat through the
  Facilitator), D-WORKFLOW-162 (check upstream early: batocera's tracker
  and ROCKNIX's for these files) and D-WORKFLOW-164/165 (consider
  contributing a fix upstream; submissions deferred), D-WORKFLOW-132 and
  D-QA-012, D-WORKFLOW-149, D-QA-007/015, D-QA-021, D-QA-044/045/051.
- Open issues whose bodies name these files (read for the planned changes
  and the known leads, not as a work queue): #336 (the libretro runner;
  its Step 1 is why this slice is second, and § 4 draws its line), #613
  (the fallback systems-config symlink: `SystemData::getConfigPath`),
  #300 and #301 (the hash-library fetch on the interface thread; the
  startup index), #303 (the cards sweep), #310 (`es-launch-memory`), #135
  (time to play), #10 (save states across build families), #117 and #120
  (the exit hotkey), #198 (credential quoting), #246 and #245
  (`rescanIfFolderChanged`; a two-byte record), #299 (the pooled
  connection), #90 and #92 (exit codes), #585 (the upstream contribution
  queue, where a fix batocera or ROCKNIX would take is recorded), #699
  (`es-syntax-check` on this host), #644 and #645 (the build-path read:
  none of its findings ride this slice), #648 (T1, beside this lane: its
  findings on `runemu.sh`'s argument parsing are the other side of this
  slice's command). Every `gh` call carries `--repo pixelelated/distribution`.

## 4. The questions

All seven apply to this slice (plan § 4); none is struck. Provenance decides
the lens (plan § 3): the 17 fork-own paths get all seven in full; the 3
upstream-carried paths (`SaveState.h`, `SaveStateConfigFile.*`) get Q6 and
Q4 first, and the rest only where the file stays. Per file, the evidence
that answers each:

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | C++17 idioms the rest of the tree has reached and these files have not (raw owning pointers where the tree uses smart ones; `std::string` concatenation of shell commands where `shellQuote` and a vector exist; detached threads where the tree joins; `system()` through the `Platform.cpp` wrapper; static mutable state read across threads, `mRunningGame` at `FileData.cpp` 83 beside the atomic `sGamesStarted` at 90); `#if WIN32`/`#if ROCKNIX`/`#else` forks where one branch ships; duplicated parsing of the same tokens (`launchToken` here, `${ARGUMENTS##*-P}` in `runemu.sh`, the `-P` fixture in two unit test files) | the replacement named with where the tree already uses it; `git log -S` for when the old form stopped being written |
| Q2 Standards | The rules § 3 names, cited by section: every string a player reads on this path against `es-player-text.md` (the five gate questions and their buttons, the capture spinner's line, the 200-to-300 error box's text, the toast at `FileData.cpp` 1294; each with its French, D-UI-051, `tools/es-untranslated`); `_()` on every label; ASCII comments near `_()`; `exists(path, false)` for files other processes write (the stamps, the lock, `/tmp/emulationstation.ready`); the credential quoting of every typed value that reaches a shell (`tests/credential-quoting.py`, the `quoting` suite); `shellQuote` on every command built from a path or a name; the four surface tiers and D-UI-093 for the cards and the toast; the flow and frame evidence rule (D-WORKFLOW-155/156) for any player-visible change; `tools/es-menu-map-check` at the pin | the rule and section; the host checks of § 5 with their output lines |
| Q3 Bugs | Where each unit fails: the unhandled branch, the race, the wrong default, the path that works on the host and not on the device. The hot spots: the command's quoting of names and paths (`%BASENAME%` and `%ROM_RAW%` raw at 624 to 625; `formatCommandLineArgument` quoting only on a space, 528 to 534; `getEscapedPath`'s character list in `FileSystemUtil.cpp`, T36's, read for what it leaves; `-state_file` in double quotes); the ROCKNIX netplay client branch at 659 to 678, which computes a password and a session and uses neither; raw `FileData*` held across the gates' waits of up to 20 s while `rescanIfFolderChanged` may delete them (776 to 793, 818 to 849, the message-box lambdas); `mRunningGame` read from detached workers and the HTTP thread; the exit sync's generation check (1295); the boot-game replay with no events and no `mRunningGame`; `head -300` on the emulator's stdout (the wrapper's, T35's: a lead across); the overlay `return` at `SystemData.cpp` 1042 and 1049; the unlocked static cache in `SaveStateConfigFile`; `onGameEnded`'s `.bak` restore when the game was killed mid-write | a reproduction on the GENERIC_X64 guest or a trace with `file:line`; host reasoning about device behaviour is a lead (§ 5) |
| Q4 Package currency | The ES fork has two upstreams. ROCKNIX's `rocknix/master` has no commit on these twenty files since the merge base `cada856d8` (record the command and its zero: `git -C "$W" log --oneline cada856d8..rocknix/master -- <the 20 paths> | wc -l`); batocera's `batocera/master` has seven since `1750dded8` (`git -C "$W" log --oneline 1750dded8..batocera/master -- <the 20 paths>`), dispositioned one by one (merged already / not applicable to this fork / to merge, with the reason; the inventory's `overlap` column names the paths both sides changed). Both refs and their hashes recorded by the first commands. The pin itself is current with `test/qa-integration` (it is its tip) | the two lists with a disposition per line; the fetch's hashes recorded |
| Q5 Efficiency | What the launch path costs between the press and the command, itemised and timed on the guest: the transition animation and the splash, the gates' polls, the window and audio teardown and `malloc_trim`, the game-start hook, the command's wrapper; and between the exit and the next first frame: the window re-init, the capture thread, the exit sync card, `rescanChangedFolders`. The two time-to-play numbers on the guest at the image § 5 names, beside the baseline #336 records (a game's first frame 1.05 s from the press, the next game's 2.03 s from the exit, on the VM), with the guest's `system.loglevel` recorded beside them (the engineering image ships `verbose` under `DEVELOPMENT_DEFAULTS`; compare like with like); `tools/es-launch-memory`'s per-cycle memory (#310) for what a launch and an exit leave in the process; the startup order's cost in `main.cpp` where a player waits (the boot game, the index, the startup sync card) | `tools/time-to-play` output; `tools/es-launch-memory` output; a measurement in the guest with its command; or the named absence of one |
| Q6 Dead ends | Is each public entry point and branch reached: by a built image (`-DROCKNIX=1`: every `#else` of `#if ROCKNIX` and every `#if WIN32` branch is unreached on the image, a row each, not a removal, because the fork merges upstream through them, D-WORKFLOW-185's shape); by any caller (`git -C "$W" grep -n -E '<name>' "$PIN" -- es-app/src es-core/src`); by any player path. Candidates the seam map saw: `SaveStateRepository::renumberSlots` (no caller anywhere), `parseArgs` flags no unit or script passes on the image (`grep -r -- '--<flag>' projects/ROCKNIX/packages` in the distribution), `%GAMEINFOXML%`, `%ROM_RAW%` and `%BASENAME%` if no shipped template uses them (read the generated `es_systems.cfg` on the guest: `grep -c '%BASENAME%' /etc/emulationstation/es_systems.cfg`), the non-ROCKNIX `%NETPLAY%` branches, the stale comment at `FileData.cpp` 1134; the `SIGTERM` handler commented out at `main.cpp` 730 | the reachability search as a command and its output, one row per entry point in `04-analysis.md` § Renovation face Q6; `engineering-practices.md` § Before deleting a duplicate before any removal; every removal carries `Already written:` (what the retired code left on devices and in clouds: a stamp, a `.bak`, a settings key) and names what it guarded, stamped and exposed |
| Q7 Clarity | Can a reader new to it tell what each unit does and why in one pass: `FileData.cpp` at 2,680 lines with `launchGame` spanning the gates, the command, the exit path and the sync (one responsibility or five); `SystemData.cpp` at 2,583; the same tokens parsed in three places; comments that match the code (the renumbering comment; the `mitm_session` note at 667); a header that says where the file came from (batocera, ROCKNIX, this fork) and which `#if` is the one that ships | the unit named with what a reader stumbles on; a duplicate named with its original |

A finding is one question with its evidence; severity and category are the
code-auditor's, with `Renovation` as the category for Q1, Q5, Q6 and Q7
items that are not defects. A Q3 finding that is a defect is also a `bug`
issue (D-WORKFLOW-187, § 1), filed with the VM artifact that would close it.

**The #336 line.** #336 Step 1 puts a headless libretro runner under the
launcher in place of RetroArch, launched by EmulationStation through the
same launcher; Step 3, later, is the in-process bridge, where the core
renders into ES's own window and the process handover this slice reads
goes away. So Step 1 replaces little on this side: the RetroArch-specific
contract in these files is the save-state half (`isEnabled` only for the
`retroarch` emulator, the Auto slot and `-state_file` arguments, the
`.bak` dance) and the `--core=`/`--emulator=` tokens. Q1, Q5 and Q7
findings confined to those lines are recorded on the punch list like any
other and carried as `deferred:#336` at Phase 7 unless the coordinator's
stream brief says otherwise; Q2 and Q3 findings there are fixed regardless,
because a player has them today (D-WORKFLOW-187). Phase 1 reads #336's body
to draw the line, and `01-research-notes.md` § Scope records where it was
drawn.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict, as its `SKILL.md`
§ Evidence floor lists them (five rules under a heading that says three,
the last numbered 3 again; a lead for T38, posted on #685, not this slice's
to fix):

1. *Tracker state is never sole evidence.* Issue state, checked AC boxes,
   and retro summaries may corroborate but can never be the ONLY evidence
   for a PASS; every PASS cites at least one primary artifact (file:line,
   executed command output, or commit diff).
2. *Mechanical evidence outranks reading.* Where a check exists, RUN it and
   record the command, exit status and counts in the criterion entry (the
   skill's table names `tools/pkgcheck`, `tools/cloud-round-trip`,
   `tools/cloud-test-backend ls`, `tools/vm-visual-qa` and a device build;
   this slice's checks are listed below).
3. *Run it on a device, not on the host.* A verdict about runtime behaviour
   needs evidence from the target: a VM from `generic-x64-vm`, or hardware.
   Host-side reasoning about a device-side behaviour is a lead, never
   evidence.
4. *An assertion that cannot fail is not evidence.* Before recording a PASS,
   ask what result would have produced a FAIL.
5. *Subagent output is a LEAD, never EVIDENCE.* Every fact that supports a
   verdict is re-read from the primary artifact before the verdict is
   written. Fan-out inside this lane is read-only research subagents only
   (D-WORKFLOW-183).

**What runs on the VM, and how.** Can this be done on the VM? **Yes**, for
every behaviour claim about the binary: the GENERIC_X64 image runs the same
EmulationStation binary, scripts, systemd units and 640x480 panel as a
handheld (`vm-first.md`), and the image carries the pin. **Where the guest
cannot show it**, the claim is a lead, written as such: a real pad's hotkey
(the exit test drives `execute_kill` with a fixture of its own, blindspot
65 applies), a real panel's rotation, a cloud a player signed in to (the
shared QA backend is off-limits to this lane; a gate over a running sync is
proven by reading and by the unit-testable logic, and the walk for it is
written as a lead for the coordinator's integration run), a build family's
save states (#10). Nothing in this slice touches a handheld, a person's
cloud, a shared QA backend, or a QA guest another lane owns.

- **The host handoff comes first.** On 2026-10-23 the M7 lane asked for the
  host's swap and the T1 lane stopped its guest at 16:37 UTC; the agreement
  in `/tmp/m7-m6-host-coordination-20261023.txt` is that **M6 starts no
  runtime of any kind (no guest, no compiler, no `npm install`) until the
  M7 coordinator writes `resource return` there, which the coordinator
  relays as a comment on #649**. Stage A's reading and the host checks that
  run no compiler (`credential-quoting.py`, `es-menu-map-check`,
  `es-untranslated`, `vocabulary-check`, the counts) need nothing; the
  first guest, the unit tests' build and the syntax-only compiles wait for
  that comment, and the wait is written in `00-running-log.md`, not a stop.
- **The image.** Do not build one (D-WORKFLOW-183: lanes deliver branches;
  nothing in M6 builds). Use the newest GENERIC_X64 image on the host, which
  the M7 lane built on 2026-10-23 at
  `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`
  (2,122,289,964 bytes; source `069fc2704421`; its BUILD_ID is read from
  the guest's `/etc/os-release` and recorded in `00-running-log.md`; the T1
  lane keeps a copy under `/workspace/artifacts/m6-t1-20261023/`, read-only
  to this lane). Copy the `.img.gz` into this lane's own artifacts directory
  first (a fresh `ROCKNIX_ARTIFACTS=/workspace/artifacts/m6-t2-<date>`);
  never write in the M7 worktree. Then `generic-x64-vm-testing.md` §
  Headless: `gunzip`, `qemu-img convert` to qcow2, `qemu-img resize ... 16G`
  (not optional), `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
  run --headless --daemonize` **with the lane's own instance paths and
  ports**: `--pidfile $ROCKNIX_ARTIFACTS/qemu.pid --serial
  $ROCKNIX_ARTIFACTS/serial.sock --monitor $ROCKNIX_ARTIFACTS/monitor.sock
  --vnc 20 --ssh-port 10033` (T1's guest, when up, holds display 19 and
  port 10032; the defaults `/tmp/rocknix-qemu.pid`,
  `/tmp/rocknix-qemu-serial.sock`, `/tmp/rocknix-qemu-monitor.sock`,
  display 9 and port 10022 are shared with every other lane's guest;
  `pgrep -f 'qemu-system-x86_6[4]' | wc -l` before starting, and `ss -ltn`
  for the two ports). `tools/vm-serial --socket $ROCKNIX_ARTIFACTS/serial.sock
  wait`, then a root shell through `tools/vm-serial --socket ... sh`.
  Provision an SSH key over serial as § Headless shows (the key lives under
  `$ROCKNIX_ARTIFACTS`, never in a tree). Stop the guest by its pidfile
  with `tools/vm-stop $ROCKNIX_ARTIFACTS/qemu.pid <the qcow2>`, never by
  pattern (§ Spin a guest down), and bring it up for a job and down when
  the job ends: the host is shared. Every VM cycle writes its row in
  `docs/vm-qa-log.md` (§ After every VM cycle).
- **The image is the tree, for this slice.** The binary on the image was
  built from the pin, so a proof on the guest proves the slice's bytes;
  record the BUILD_ID and `strings /usr/bin/emulationstation | grep -c
  <a fork string from the slice>` once (`device-builds.md` § Iterating on
  EmulationStation: the mount does not build; the pin does). **A fix
  changes that**: an edited `.cpp` has no binary on any image until the
  coordinator's integration build (§ 6, stage F). Until then a fix's
  evidence is the unit tests, the syntax-only compile, the reading, and the
  walk written for the first image that carries it; the proof on the guest
  is the coordinator's at that image, and the hand-back says so per fix.
- **Stage A's tool trials.** Run `tools/time-to-play`,
  `tools/emulator-exit-test` and `tools/es-launch-memory` once each
  against this single guest, before the Q5 measurements, and record in
  `00-running-log.md` that they work without `tools/vm-pair`: all default
  to port 10022 and take `--port` and `--identity`; `time-to-play` also
  requires `--monitor <the guest's monitor socket>` and `--out <a directory
  under $ROCKNIX_ARTIFACTS>`, takes `--vm` (RetroArch to the gl driver for
  the run; the guest has no Vulkan) and `--no-configure-remote` (it would
  otherwise set up a QA cloud remote through `tools/cloud-test-backend`, a
  shared backend this slice has no business in; `generic-x64-vm-testing.md`
  § One writer per QA cloud folder); `emulator-exit-test --vm` builds its
  own cartridge; `es-launch-memory` requires `--identity`, `--cycles` and
  `--output` and takes `--monitor` and `--port` (its `--help`; omit the two
  memory limits for diagnosis).
- **The host-side checks that exist for these sources**, each run and its
  command, exit status and summary line recorded in `02-forward-audit.md`;
  a check that cannot run is recorded as such, never as a pass. Four were
  run by the coordinator on 2026-10-23 at the pin, in the lane's ES
  worktree, and their lines are the baseline a changed source is held to:
  - `python3 -I tests/credential-quoting.py "$W"` from `$W`
    (`credential-quoting: 9 credential call site(s), 9 quoted, 0 bare`;
    the `quoting` suite of `tools/vm-qa`, #198);
  - `tools/es-menu-map-check --es-src "$W" --ref "$PIN"` (`55 screen(s) at
    16dbac521, 31 in the map, 24 declared unmapped, 0 missing`; D-UI-039);
  - `tools/es-untranslated --es-src "$W"` (`703 fork string(s) in the
    source, 703 with French, 0 without`; D-UI-051);
  - `tools/vocabulary-check --es "$W"` (`163 string(s) ... judged, 0
    wrong`);
  - **the unit tests**, built with the toolchain's cmake from the M7 build
    root (read there, written only under `$W/build-tests`, gitignored;
    `es-code-traps.md` § Pure text has a home), proven by the coordinator
    the same day (`185 passed | 0 failed`, `4795 assertions`):
    ```bash
    B=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64
    cd "$W"
    $B/toolchain/bin/cmake -S es-app/tests/unit -B build-tests -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
      -DRAPIDJSON_INCLUDE_DIR=$B/toolchain/x86_64-rocknix-linux-gnu/sysroot/usr/include
    $B/toolchain/bin/cmake --build build-tests --target es-unit-tests -j8 && ./build-tests/es-unit-tests
    ```
    `LaunchCommandTests.cpp` and `SaveStateJobQueueTests.cpp` are this
    slice's; a fix to a pure function gets a case there first, and a new
    rule about a string or a token goes beside them (the two compiles are
    compiler runs: they wait for the host's return line);
  - **the syntax-only compile before any ES commit** (`es-native-ui.md` §
    Before the pin moves; blindspot 49). `tools/es-syntax-check` as shipped
    cannot run on this host (#699): its default root does not exist, and
    every GENERIC_X64 build root present carries a toolchain copied from a
    retired path, so the tool prints a bare `FAIL`. Until #699 lands, use
    its proven recipe for every edited `.cpp` (each about one second;
    the build root is read, never written, and its wrapper files are never
    edited):
    ```bash
    B=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64
    OLD=/workspace/repos/rocknix.worktrees/m7-pixelelated/build.pixelelated-GENERIC_X64.x86_64
    BD=$B/build/emulationstation-$PIN/.x86_64-rocknix-linux-gnu
    f=es-app/src/FileData.cpp            # the edited file, path relative to $W
    cmd=$(cd "$BD" && $B/toolchain/bin/ninja -t commands "es-app/CMakeFiles/emulationstation.dir/${f#es-app/}.o" | tail -1)
    (cd "$BD" && eval "$(echo "$cmd" | sed -E "s#$OLD#$B#g; s#^[^ ]*x86_64-rocknix-linux-gnu-g\+\+ #$B/toolchain/bin/x86_64-rocknix-linux-gnu-g++-15.2.0 #; s#-c [^ ]+\.(cpp|cc|cxx)( |\$)#-c $W/$f #; s# -o [^ ]+\.o# #; s# -MF [^ ]+# #; s# -MD # #; s# -MT [^ ]+# #") -fsyntax-only") && echo "PASS $f"
    ```
    A header edit needs every includer compiled (`git -C "$W" grep -l
    '"<header>"' -- es-app/src es-core/src`); the record names each. If
    #699's fix has landed on the branch by then, `tools/es-syntax-check
    --root $B <files>` replaces the recipe and the record says which ran;
  - the guest tools above: `tools/emulator-exit-test --port 10033 --identity
    <key> --vm` (the exit hotkey through `runemu.sh` and back into
    `launchGame`'s return path; § Fixtures for the launch path);
    `tools/time-to-play --port 10033 --identity <key> --monitor
    $ROCKNIX_ARTIFACTS/monitor.sock --out <dir> --no-configure-remote --vm`
    (the two numbers); `tools/es-launch-memory --port 10033 --identity
    <key> --monitor $ROCKNIX_ARTIFACTS/monitor.sock --cycles 5 --output
    <file>` (what a launch and exit leave in the process, #310);
    `tools/vm-visual-qa --monitor $ROCKNIX_ARTIFACTS/monitor.sock run
    <steps>` with a step file under `tools/vm-walks/` for every dialog on
    the launch path the guest can reach (the missing-BIOS box, the
    extension box, the capture spinner, the error box for an exit code in
    200 to 300, provoked with a fixture ROM and a template edit under
    `/storage`), frames at 640x480 filed with the audit and indexed as
    `es-ui-style-guide.md` § Keep the flow says;
  - of `tools/vm-qa`'s suites, `quoting`, `menumap`, `french` and
    `vocabulary` cover this slice and are the four host checks above;
    `exit` is `emulator-exit-test`; `lifetime` (the cloud pages' lifetimes)
    and `scripts` are other slices'. Run them directly, as above, rather
    than through the runner, which wants the pair up.
- **A read is free and goes through the filter.** Every line read back from
  the guest, from an image's config, from `rclone.conf`, `system.cfg`,
  `es_settings.cfg` or `get_setting`, passes `grep -v -i -E
  'key|pass|token|user|psk'`, or is masked with `sed -E
  's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'` where the line's
  presence is the evidence (D-QA-021; `engineering-practices.md` § Nothing
  runs on a person's device). The launch log `maskSecrets` writes
  (`FileData.cpp` 1090) is read the same way, and so is `global.bootgame.cmd`.

**What never runs in this slice:** a build of an image or a package; a
command on a handheld, a person's cloud, a shared QA cloud backend, or a QA
guest this lane did not start; a runtime of any kind before the host's
return line; an edit to any tool while a run of it is in flight; `pkill -f`
or `kill` by pattern; bare `git stash`; `git worktree remove --force` or
`rm -rf` of any worktree (`tools/fork-worktree remove` in the distribution;
`git worktree remove` without `--force` in the ES repository, and only of
this lane's own); a checkout, a branch switch or a write in the ES primary
checkout or in its `qa-integration` and `m7-*` worktrees; a push to
`test/qa-integration` or a pin bump in `package.mk` (the coordinator's at
integration); a model call outside `tools/council/run`; a credential or the
wordlist printed; a merge of another lane's feature branch to refresh rules
(read them from `next`); a write under `/workspace/repos/rocknix` or any
`rocknix.worktrees/*`, or in the P0, P1 or T1 worktrees; an edit to
`.github/sessions/saved-session-state-next.md` (the M7 lane's);
`--no-verify` on any push in either repository; a change to
`docs/reviews/order.md`, `slices.json`, `areas.json`, the plan, the brief,
#649's criteria or the M6 body (the coordinator's, D-WORKFLOW-189); a
GitHub issue other than the audit punch-list issue and `bug` issues (§ 1).

## 6. Outputs

All in the distribution worktree, committed on its branch with messages
that cite `#649` (`Refs #649` while any criterion is open, never a closing
keyword), except the source changes, which are commits on the ES branch in
the ES repository's own style (`<Area>: <what changed>`, as `GuiWifi:
cancel scan worker on normal frontend exit`; the body ends `Refs
pixelelated/distribution#649`, and a `bug` fix also `Refs` its bug); the
stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-es-launch-path/00-running-log.md` | the skill's append-only flight recorder, opened first: the model and effort that ran, `reviewed-at` (the distribution branch `HEAD`) with the pin beside it, the two upstream refs and hashes the first commands fetched, the image's BUILD_ID, the guest's instance paths, the host handoff's wait and the return line's time, the three tool trials' outcome, the `tsx` version, every checkpoint | A |
| Research notes | `.../01-research-notes.md` | § Scope: the 20 paths re-derived with the commands of § 2 and their deltas; the five groups; the interacting subsystems; the open M7 ES branches that touch a slice file, listed; the #336 line drawn; the rules read, by name (`working-principles.md` § Pre-flight) | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #649's checklist, plus a **coverage table with one row per path** (20 rows; the first cell the path in backticks, so ``grep -c '^| `es-app/src/' 02-forward-audit.md`` prints 20; then group, tier, Q1 to Q7 each answered or `n/a` with the reason); the host checks and the guest tools of § 5 with command, exit status and summary line; the proofs on the guest, each saying what it proved (the pin's binary; a fix's unit test; a walk written for the next image) | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5's interaction audit for the seams § 2 names (the command x `runemu.sh`'s parsing; the gates x the sync, the transfer and the proxy; `rescanIfFolderChanged` x the deferred launches; the exit path x `cloud_capture` and the exit sync; the boot game x the startup sync) | B |
| Analysis | `.../04-analysis.md` | Phase 4, then § Finding Verification (4.5), then **§ Renovation face** with one subsection per question Q1 to Q7 (the lint requires all seven), Q6 carrying the reachability table and Q5 the measurements beside the baseline with the guest's loglevel, then § Second opinion (4.6: the two seats, each with command, provenance path, served model, the grading table and the net-effect line) | B, C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (written before the first call), `<member>-brief.md`, the outputs, each call's `provenance.json`; the probe of each seat | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | prints `PASS pre-issue artifacts (does not certify resolution)`; recorded in the running log | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5, every item with `question: Q1..Q7` (or `none` with a reason), severity, category (`Renovation` where it is not a defect), where (file:line at the pin), acceptance; the YAML `punch_index` (`templates.md`); #336-line items marked for `deferred:#336`; a lead for another slice marked with its slice and posted on #649 | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #649 | `Audit: M6 T2 EmulationStation's launch path -- N findings (X critical, Y high)`; one checkbox per item, each agent-verifiable (D-QA-044); `tools/box-check --issue N` run on it and its line recorded | D |
| Bug issues | GitHub, label `bug`, milestone-less unless the coordinator places them | one per defect (D-WORKFLOW-187, D-QA-051): the code trace shape (`release-candidates.md` step 0), the `Can this be done on the VM?` line, the VM artifact that closes it (and, for a fix without a binary yet, the walk and the unit test that stand in until the integration image); `tools/box-check --issue N` on each | D |
| **The stage-D pause** | #649 | the punch list posted on #649 with the audit issue's number and the `bug` issues' numbers; **the lane waits** while the coordinator writes one remediation brief per stream of related items (plan § 6b stage E: the D-WORKFLOW-056 shape, the files owned, the test first, the `Already written:` line, the commit shape, which repository each file is in). The coordinator's brief names the branch each stream lands on; the default is this lane's two branches, one commit series per stream, headed by the stream's name | D to E |
| Remediation | the branches the stream briefs name | each stream as its brief specifies: a source change on the ES branch, the unit test first where the code is pure, the syntax-only compile recorded per edited `.cpp`, the French beside every new string; a `bug` issue's fix carries its `Already written:` line; a player-visible change updates `docs/es-menu-map.md`'s flow (D-UI-039) and the running change log the rule names (`change-log.md`) the same day; never a build, never a pin bump | E |
| Verification | `02-forward-audit.md` appended; `.../audit-completion.json` | every behaviour claim proven on the guest where the pin's binary can show it (§ 5), the VM cycle's row in `docs/vm-qa-log.md`; a fix's claim proven by its unit test and syntax compile now and by the coordinator at the integration image, each marked which; Phase 7 outcomes re-derived from commands (each outcome names the command or the diff that shows it: a resolved item its commit and the check that passes, a deferred item its issue, a withdrawn item the artifact that refutes it); `tools/lint-audit-artifacts <folder>` prints `PASS` before H | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-es-launch-path.md`, and the same text as a comment on #649 | the mini-retro skill's four answers with its scoped audit, in Instruction-Recommendations mode (plan § 6b G: the scope is epic tier); findings that recur become a rule edit, a tool, a blindspot entry with its guard, or a work-log entry (`learning-capture.md`); what the slice did to time to play (`time-to-play.md`) | G |
| Hand-back | #649 | `reviewed-at:` (the distribution branch `HEAD` at stage A), `fixed-at:` (that branch's tip when the fixes are complete) and `fixed-at-es:` (the ES branch's tip; the pin itself when no source changed) written into #649's body by the executor; one comment naming both branch tips and each artifact above by path; then the lane says it is idle. **The coordinator** accepts (§ 10), closes #649, writes `reviewed_at`, `fixed_at` and the `es` hash into `slices.json`, merges the ES branch into `test/qa-integration` and bumps the pin in `package.mk` in its turn, and after the distribution branch merges to `next` regenerates the inventory, `tools/renovation-status --write docs/reviews/status.md` and `tools/renovation-drift --write docs/reviews/drift.md`, and moves the M6 body (D-WORKFLOW-189) | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-es-launch-path-649.md` | seeded by the coordinator; the executor updates it at every checkpoint: start here, both worktrees, current focus, the stage reached, next commands, merge notes | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session, headed `#649` and the thing decided or learned | every session |

Neither `tools/renovation-status` nor `tools/renovation-drift` nor
`tools/renovation-inventory` is run to write ledgers or edited here; a
defect in one is a lead on #649 (they are P1's tools, documented in
`docs/reviews/README.md`).

## 7. Acceptance

The checklist on #649 is the contract. Its first five items are plan § 6b's
contract for every slice; the rest are this slice's, written by the
coordinator with this brief (D-WORKFLOW-189). Each names the artifact that
ticks it; the coordinator ticks them at hand-back from the artifacts, not
from this lane's word.

- [ ] `docs/audits/<date>-epic-m6-es-launch-path/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-es-launch-path/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
- [ ] `second-opinions/review-plan.json` records Extended depth and two reviewers from two other labs, and each reviewer's provenance names its served model (plan § 6c, D-WORKFLOW-137).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue, or withdrawn with its reason.
- [ ] `reviewed-at:`, `fixed-at:` and `fixed-at-es:` on #649 carry the lane's commits the read and the fixes were made at (the read made with the ES worktree at the pin `16dbac5211`, the distribution branch on the P1 tip; `fixed-at-es:` the ES branch's tip, or the pin when no source changed), and, after the coordinator closes #649 and the branches merge, `tools/renovation-status` lists this slice as `closed` (the coordinator's regeneration).
- [ ] `01-research-notes.md` § Scope records the pin, the two counting commands of brief § 2 with their output (20 paths, 11,287 lines, 17 fork-own, 3 upstream-carried, or the deltas beside them), the two upstream refs with their hashes and merge bases (`rocknix/master` and `cada856d8`; `batocera/master` and `1750dded8`), the image's BUILD_ID, the open M7 ES branches that touch a slice file, and the #336 line.
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c '^| `es-app/src/' 02-forward-audit.md`` prints 20; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` records, with command, exit status and summary line, each of: `tests/credential-quoting.py`, `tools/es-menu-map-check`, `tools/es-untranslated`, `tools/vocabulary-check`, the unit tests (`es-unit-tests` with its passed and assertion counts), the syntax-only compile per edited `.cpp` (the #699 recipe or the fixed tool, named), `tools/emulator-exit-test --vm`, `tools/time-to-play --vm`, `tools/es-launch-memory`; a check that could not run is recorded with the reason, never as a pass.
- [ ] `04-analysis.md` § Renovation face Q5 carries the two time-to-play numbers measured on the guest beside #336's baseline (1.05 s and 2.03 s), the guest's loglevel, and `es-launch-memory`'s per-cycle table.
- [ ] `04-analysis.md` § Renovation face Q6 carries one reachability row per public entry point of the twenty files and per `#if` branch (the search command and its output); every row marked unreached by any caller carries an `Already written:` line and what the code exposed.
- [ ] `04-analysis.md` § Renovation face Q4 records `rocknix/master`'s zero commits on these files since `cada856d8` with its command, and lists every commit of `1750dded8..batocera/master` touching them (7 on 2026-10-23) with a disposition each (merged / not applicable / to merge, with the reason).
- [ ] Every proof on the guest in `02-forward-audit.md` says what it proved: the pin's binary (the slice's bytes), or a fix whose binary does not exist yet, the latter with the unit test and the walk that stand in and the note that the coordinator proves it at the integration image.
- [ ] Every ES commit on the branch touches a `.cpp` only with a recorded syntax-only compile and a unit-test run before it (`00-running-log.md` names the commit and the two lines); every new or changed player string has its French in the same commit (`tools/es-untranslated` still prints `0 without`); `tools/es-menu-map-check` still prints `0 missing` at the branch tip.
- [ ] Every defect on the punch list has a `bug` issue carrying the `Can this be done on the VM?` line and a VM-verifiable criterion; every proposed removal carries `Already written:`; `tools/box-check --issue N` passes on the audit issue and on each `bug` issue this lane files.
- [ ] The retro exists at `docs/retros/<date>-m6-es-launch-path.md`, is posted on #649, and answers what the slice did to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the distribution branch, and the ES repository's `.githooks/pre-push-test` passes in the ES worktree, before the merges; the six exit codes pasted on #649.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and both
branches pushed (the hand-back, § 10); **the stage-D pause** (the punch
list and the audit issue posted on #649; the lane waits for the
coordinator's stream briefs and does no remediation before them,
D-WORKFLOW-189; #649's body says the same above its checklist); **the
Phase 4.6 blocker** (a reviewer seat failing identity verification, or the
route missing after all: the other pass done, the seat recorded pending,
the blocker named on #649, no Phase 5; § 1); an explicit maintainer pause
on #649; any other blocker, named on #649 with what is needed (a count that
cannot be produced or two commands that disagree; a rule that forbids a
step; a guest that will not boot after the recipes of
`generic-x64-vm-testing.md` § Debug order; the npm install failing; the
unit tests failing to build at the pin); **a hash mismatch at stage A**
(the ES worktree not at the pin, or the distribution branch not on the P1
tip: the coordinator re-baselines); or an execution limit, stated as such
with the running log current. **The host's return line is a wait, not a
stop**: the reading and the host checks go on, and the wait is in the
running log. A checkpoint is not a stop (D-WORKFLOW-149): write it and take
the next stage. A differing count is a delta, not a stop. `next` or the
integration branch moving under the slice is drift, not a stop. An idle
session says it is idle on #649.

## 9. Ceremonies owed

- A work-log entry per session, headed by `#649`; `tools/work-log-index
  --write` after it; the weekly summary if the lane's week falls due
  (`ceremonies.md`; the W42 summary is the M7 lane's and is not this
  lane's to write).
- A friction line in `docs/friction-log.md` the moment something slows,
  with `issue: #649` or the guard.
- The VM question written before every proof (§ 5 answers it for the slice,
  and names what the guest cannot show; a proof that needs something else
  the guest lacks writes its own line in `02-forward-audit.md`); a row in
  `docs/vm-qa-log.md` per VM cycle.
- The mini-retro skill at stage G, posted on #649, with its scoped audit, in
  Instruction-Recommendations mode.
- A register row the same session for any decision the slice forces (a fork
  resolved, an assumption invalidated). The ID: one above the highest
  `D-WORKFLOW` on every pushed branch (`git grep -ho 'D-WORKFLOW-[0-9]*'
  $(git branch -r --format='%(refname)') -- docs/decision-register.md | sort
  -t- -k3 -n | tail -1`) and in the M7 lane's worktree
  (`/workspace/repos/rocknix.worktrees/m7-player-setup/docs/decision-register.md`);
  on 2026-10-23 the highest is D-WORKFLOW-190 (the M7 lane holds 171 to 180
  unmerged; the T1 lane may add one beside this lane, so check both
  branches). A row goes at the end of the `## Decided` table, never after
  `## Open decisions` (`tools/register-check` refuses it there, #646).
- `tools/ceremony-check` before every push; what it reports as owed by this
  lane is paid first; what another lane owes is noted on #649. Never
  `--no-verify`, in either repository. A merge with conflicts is checked
  for leftover markers before it is committed (#696).
- Commit messages in each repository's style (§ 6): `docs: ...` in the
  distribution with `Refs #649`; `<Area>: ...` in the ES repository with
  `Refs pixelelated/distribution#649`.
- `docs/es-menu-map.md`'s flow and `change-log.md`'s running log the day a
  player-visible change lands (stage E).

## 10. Hand-back

The coordinator accepts the slice by reading, in this order, without
re-reviewing it: #649's checkboxes against their artifacts (§ 7); the lint's
`PASS` line on the audit folder; `second-opinions/` (two provenance files
naming two served models from two labs); the audit issue's checkboxes all
at an outcome; the coverage table's row count; `02-forward-audit.md`'s
check lines and the what-it-proved note on each guest proof; the ES branch's
log (every `.cpp` commit with its compile and test lines in the running
log); the retro's four answers; the six checker exit codes on #649. The
lane posts one hand-back comment on #649 naming both branch tips and each
of those artifacts by path, writes `reviewed-at:`, `fixed-at:` and
`fixed-at-es:` into #649's body, then says it is idle. After acceptance the
coordinator closes #649, writes the hashes into `slices.json`, merges the ES
branch into `test/qa-integration` and bumps the pin, merges the distribution
branch in its turn, proves each fix on the guest at the first image that
carries the new pin, and regenerates the ledgers (§ 6, Hand-back row). A
brief that needed the coordinator's help mid-slice, beyond the stage-D pause,
the Phase 4.6 blocker and the host's return line this brief already names,
is a defect in this brief: log the friction, and the coordinator fixes the
template in plan § 7 before the next brief.
