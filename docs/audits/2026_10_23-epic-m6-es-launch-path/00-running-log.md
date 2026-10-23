# Epic Audit Running Log — M6.P2 T2, EmulationStation's launch path

**Auditor:** Code Auditor skill (`SKILL.md` and its four references identical to `next`'s: `git diff --quiet next -- .claude/skills/code-auditor/<file>` exit 0 for each), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #649 (2026-10-23T17:21:03Z) and the session's own metadata
**Session:** herdr agent `m6-t2-es-launch`, session `9adce27f-9c22-4065-af78-e6c9a2a1f6ff`, pane `wN:p5`
**Started:** 2026-10-23 17:22 UTC
**Scope:** slice `es-launch-path` (#649, `M6.P2 E700/T2`), area epic #700, renovation epic #339, milestone M6. The twenty EmulationStation paths of brief § 2
**Spec:** `docs/reviews/briefs/es-launch-path.md` version 2 (`6de32b24b0`; its § 7 is #649's checklist); `docs/reviews/plan-for-the-plan.md`
**Depth:** Extended (two reviewers from two other labs: GPT-6 Astra and Gemini 4 Argon)
**reviewed-at:** distribution `f4e0f0a196` (the branch `HEAD` when stage A opened), ES pin `16dbac5211eea7e70db7394372033be2be7df829` (the ES worktree's `HEAD`)
**Branches / worktrees:** distribution `feature/m6-es-launch-path-649` at `/workspace/repos/pixelelated/distribution.worktrees/m6-es-launch-path-649`; ES `feature/m6-es-launch-path-649` at `/home/max/Development/emulationstation-next.worktrees/m6-es-launch-path-649`

---

## Queued until the host's `resource return` (brief § 5)

Nothing on this list runs before the coordinator relays M7's `resource return` on #649. They run in this order when it comes:

1. `npm install --prefix tools/council` in the distribution worktree. Record the `tsx` version, then run `tools/council/run verify-pins` (expect its `OK` line) and `tools/council/run test`.
2. #699's compile proofs: criterion 1, `tools/es-syntax-check --root $B <the pinned FileData.cpp>` should print `PASS` and name the compiler. Criterion 3, a broken copy of `LaunchCommand.h`'s includer should give the compiler's `error:` line and `FAIL`.
3. The unit tests (`es-unit-tests`, built into `$W/build-tests` with the toolchain's cmake). Baseline: `185 passed | 0 failed`, `4795 assertions`.
4. `tests/app-unit`: `proxycards-tests`, `bookkeeper-tests` and `jobs-tests`, built into `$W/build-app-unit`. This is the first run; the coordinator has not proven it.
5. `tests/launch-capture-gate.py`, `tests/launch-deferred-state.py` and `tests/hasher-offline-index.py`, each with `--help` first.
6. The guest. Copy the image, its `.sha256` and `.identity.json` into `/workspace/artifacts/m6-t2-20261023/` and check the copy with `sha256sum -c`. Then `qcow2`, resize to 16G, and boot headless with `--pidfile/--serial/--monitor` under that directory, `--vnc 20` and `--ssh-port 10033`. Then the SSH key, the BUILD_ID and the `strings` count.
7. The tool trials: `tools/time-to-play --vm --no-configure-remote --only launch,exit,g2g --repeat 3` and `tools/es-launch-memory --cycles 5 --rom /storage/roms/gb/TTProbe.gb`.
8. The Q5 measurements, the Q6 template read (`grep -c '%BASENAME%' /etc/emulationstation/es_systems.cfg`), and the launch-path dialogs' walks.

## Log Entries

### [Phase 0] 17:22 — The brief's first commands

- Distribution `HEAD` `46f3a19b2f`, on `feature/m6-es-launch-path-649`. `git merge-base --is-ancestor 2174265e9c HEAD` exit 0: the branch is stacked on the P1 tip.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md` lists exactly `fork-workflow.md` (2 +-), `instruction-files.md` (5 ++++-) and `.claude/skills/council/IMPORTED-FROM.md` (25 +). Nothing else, as expected. `origin/next` gives the same.
- `package.mk` line 5: `PKG_VERSION="16dbac5211eea7e70db7394372033be2be7df829"`.
- ES worktree: on `feature/m6-es-launch-path-649`, `HEAD` equals the pin, `git status --short` empty. Hooks path `/home/max/Development/emulationstation-next.worktrees/qa-integration/.githooks` lists `commit-msg guard-lib pre-commit pre-push pre-push-test secret-patterns`.
- `git fetch rocknix --no-tags` moved `rocknix/master` from `e282b0562` to **`f6c542872`** (2026-10-23T21:57:36+11:00). **Delta** from the brief's `e282b0562`. `e282b0562..f6c542872` is 4 commits, and none touches the twenty files. `merge-base $PIN rocknix/master` = `cada856d8`, as recorded.
- `batocera/master` = **`b2ceb55a7`** (2026-10-21T08:16:07+02:00); `merge-base $PIN batocera/master` = `1750dded8`, as recorded.
- `git push -u origin feature/m6-es-launch-path-649` (ES): a new branch at the pin.
- The brief and the epic's futro are in the tree.
- Start comment on #649: issuecomment-6370692523.

### [Phase 0] 17:23 — Lane start committed

- Work-log entry `17:25 UTC — #649 T2 lane start`, then `tools/work-log-index --write` and `--check` (current); commit `f4e0f0a196`, pushed.
- `tools/ceremony-check --gate` exits 1 with `BLOCK weekly: 2026-W42 summary missing`. Brief § 9 makes W42 the M7 lane's. The pre-push hook applies the gate only to pushes of `next` (`.githooks/pre-push` line 334 onwards), so the feature push needed no `--no-verify`. This goes on #649 as owed by another lane.

### [Phase 0] 17:24 — Reading (brief § 3, the pre-flight) begun

- Read: `docs/reviews/plan-for-the-plan.md` § 1 to § 7, item 3, and the remaining headings (§ 8 to § 11); the brief whole; the lane's pointer; #649's dispatch comment; `/tmp/m7-m6-host-coordination-20261023.txt` (no `resource return` line).
- Read: the code-auditor `SKILL.md` sections on the serial discipline, checkpoints, depth, the evidence floor, document-as-you-go, the lifecycle, Phase 0, the verdict vocabulary, project conformance and the interaction audit. Each reference is opened at its phase.
- Every-session rules and the four ES rules were loaded this session from the worktree. They equal `next`'s except P1's two files and the council `IMPORTED-FROM.md`.
- The host at 17:25:04: `pgrep -f 'qemu-system-x86_6[4]' | wc -l` = 0; RAM 42 GiB available; swap 2 of 7 GiB used. `node` v24.21.0, `npm` 11.19.0; `tools/council/node_modules` absent.

### [Stage A] 17:25 — Scope re-derived (brief § 2)

- The inventory filter gives `paths 20 lines 11287 fork-own 17 upstream-carried 3 fork-own lines 10804`, as recorded. `git ls-files` = 20; numstat against the empty tree = 11287; `wc -l` = 11284. Every row is `reach: shipped`.
- `rev-list --count cada856d8..rocknix/master -- <20>` = **0**; `cada856d8..$PIN -- <20>` = 115.
- `1750dded8..batocera/master -- <20>` = **7**; `1750dded8..$PIN -- <20>` = 131; repository-wide 865. All as recorded.
- Branch scan of the ES primary (read-only): 104 `feature/`+`fix/` branches, 18 of them `feature/m7-*`. Three touch a slice file ahead of the pin: `feature/backup-restore-dialogs` 4, `feature/restore-relink-wizard` 5 and `feature/cloud-epic` 1, none in flight. **No `m7-*` branch touches the twenty.** `test/qa-integration` = `16dbac521`, the pin.
- Closed `bug` issues: 139. 14 match the pattern `\b(launchGame|FileData|SystemData|ViewController|SaveState\w*|ProxyCards|LaunchCommand|es_systems)\b|\bmain\.cpp\b` over title and body: #101 #114 #149 #183 #205 #206 #207 #209 #210 #246 #275 #300 #305 #520.
- Prior punch lists, `grep -c` with the brief's pattern: 24, 21, 7, 6, 4, 4, 2 and 2, as recorded.

### [Stage A] 17:26 — The four host checks that run no compiler (baseline at the pin)

- `(cd $W && python3 -I tests/credential-quoting.py $W)`: rc 0, `credential-quoting: 9 credential call site(s), 9 quoted, 0 bare`.
- `tools/es-menu-map-check --es-src $W --ref $PIN`: rc 0, `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`.
- `tools/es-untranslated --es-src $W`: rc 0, `703 fork string(s) in the source, 703 with French, 0 without`. Two upstream strings (`GuiMenu.cpp` 517 and 518, the fuel gauge) are not counted, and they are outside the slice.
- `tools/vocabulary-check --es $W`: rc 0, `163 string(s) with back up / backup, save state or Wi-Fi judged, 0 wrong`.
- All four equal the coordinator's baseline in brief § 5.

### [Stage A] 17:26 — #699: the fix written, the constructed failure seen

- `tools/es-syntax-check`: the recorded root (the compiler's path above `toolchain/bin`) is rewritten to `--root` wherever the command names it. The real compiler beside the wrapper (`<wrapper>-<version>`) runs in the wrapper's place, and the tool prints `compiler <path>` once. With no real compiler, a wrapper that names a missing path gives `NO-COMPILER <path>` and exit 2. The stderr filter now keeps `No such file` and `not found`. `bash -n` passes.
- `.claude/rules/es-native-ui.md` § Before the pin moves now has one sentence on `--root` and the moved root (#699 criterion 4). The worktree's rules now differ from `next` in a fourth file, and this lane wrote it.
- Criterion 2 (no compiler ran; ninja listed commands only): a fake root under the scratchpad holds symlinks to the M7 root's ES build directory and ninja, plus a copy of the two-line wrapper and no `g++-15.2.0`. `tools/es-syntax-check --root <fake> $W/es-app/src/FileData.cpp` printed `(moved) recorded root .../m7-pixelelated/..., rewritten to <fake>` and `NO-COMPILER .../m7-pixelelated/.../toolchain/bin/ccache: named by <fake>/toolchain/bin/x86_64-rocknix-linux-gnu-g++, and no real compiler beside it`, rc 2. `LaunchCommand.h` gave the same (it borrows `FileData.cpp`'s command).
- Criteria 1 and 3 compile: queued, item 2 above.

### [Phase 1] 17:29 — Research written

- `01-research-notes.md` § Phase 1: the issues of brief § 3 (#120 is **open**, a delta from the brief's closed list); 14 closed bugs naming the files; the history (115 fork commits, concentrated in `main.cpp`, `FileData.cpp` and `ProxyCards.cpp`); the prior audits as provenance only.

### [Phase 2] 17:31-18:0x — Group 1 read (`LaunchCommand.h`, `FileData.*`, `ViewController.*`)

- Provenance per region: `git diff -U0 1750dded8 $PIN` puts the fork's hunks in `FileData.cpp` at about 1-130, 677-723 and 763-1318, and in `ViewController.cpp` at 39-80, 1059-1118 and 1468-1496. The rest is batocera's, byte for byte.
- Findings FD-1 to FD-21 and VC-1 to VC-6 are in `02-forward-audit.md`. Leads to grade in Phase 4.5:
  - FD-8: a raw `FileData*` held across the gates' waits; severity depends on group 2's rescan triggers.
  - FD-14: DELETE GAME removes files outside the game's directory through `.m3u`/`.cue`/`.gdi`.
  - VC-1: the gates ask after the launch transition and the splash.
  - FD-1, corrected by a caller search: `netplayClientPassword` is never assigned, and a `SPECTATOR` join becomes a plain client on the image.
- Seam leads for other slices: FD-7 (the controllers blob, T36), FD-9/FD-19 (`Scripting` quoting, T33/T21), FD-1's `mitm_session` (T31).

### [Phase 2] 17:3x-17:43 — Groups 2 to 5 read; the Q6 list and the Q4 dispositions

- Groups 2 (SD-1 to SD-7), 3 (SS-1 to SS-4, SR-1 to SR-3, SC-1, SB-1 to SB-3), 4 (FD-18 confirmed, PC-1, PC-2) and 5 (MN-1 to MN-7) are in `02-forward-audit.md`. FD-8 was graded down to Low after the rescan's two posts were traced (`FileData.cpp:1223`, `GuiCloudTransfer.cpp:335`).
- Q6 list: `q6-reachability.py` (in the audit folder) on the pin gives **370 entry points**: 295 header declarations (one-line, multi-line and inline), 13 file-static functions and 62 preprocessor conditionals (`#if`/`#ifdef`/`#ifndef`/`#else`/`#elif`, indented ones included).
  - The brief's three commands count 154 declarations, 32 statics and 60 conditionals. The brief recorded 36 conditionals, a **delta**: its pattern also matches `#ifdef`/`#ifndef`.
  - The 32 "statics" include static data (19 are data, `^static ` with no parenthesis), which are not entry points.
  - The hand reading added `recordCopy` (its call spans two lines, `GuiSaveState.cpp:524`) as reached.
  - Five functions are unreached: `renumberSlots`, `isVirtualFolderDisplayEnabled`, `hasGamelist`, `setIndex` and `isDefaultConfig`. Each was confirmed with `git grep -n -w <name> $PIN -- es-app/src es-core/src es-app/tests`.
  - The table is generated into `q6-table.md`, 370 rows.
- Preprocessor facts: `-DROCKNIX=1 -DDISABLE_KODI=1` (`package.mk:19-25`); CMake defines `BATOCERA` only under `if(BATOCERA)` and `_RPI_` only under BCMHOST/RPI. No CMake file defines `DEBUG` or `FREEIMAGE_LIB`.
- Q4, batocera's seven commits (`1750dded8..batocera/master -- <20>`), each tested against the pin with `git show <c> -- <20> | git apply --check [--reverse]`, which writes nothing:
  - `13e21d420`, `d17cf003e` and `308221458` apply forward.
  - `b69fb143c` conflicts with the fork's constructor hunk.
  - `5f106acce` and `0806a0c5c` stack on `308221458`.
  - `195a517ef` is the merge carrying `13e21d420`.
  - None is already in the pin.
- `CheckBiosesAtLaunch` defaults to `false` (`es-core/src/Settings.cpp:207`).
- Host: no `resource return` line yet.

### [Phase 3-4] 17:47-18:0x — Retrospective, analysis, verification; stage C prepared

- `03-retrospective.md`: 3.1 to 3.7, with the five seams of brief § 2 as interaction entries. The 3.6.5 sibling table comes from `git grep -n -E <shape> $PIN -- es-app/src es-core/src`, one row per shape. Siblings were found for SS-1, FD-2, FD-15, MN-4 and MN-5, in this slice and in neighbouring slices.
- **Doctrine drift found:** `time-to-play.md` says D-CLOUD-076 ships and D-CLOUD-109 replaces it. The code ships D-CLOUD-130 (`FileData.cpp:993-1008`). This is a lead for the doctrine slice.
- `04-analysis.md`: the lint's five sections, § Finding Verification, and § Renovation face Q1 to Q7 (Q6 with the 370-row table; Q4 with the seven dispositions; Q5 the named absence of a measurement until the host returns). § Second opinion is pending.
- Phase 4.5: the graded findings' lines re-read from `git show $PIN:<path>`, and `isAbsolute` read (`FileSystemUtil.cpp`). FD-1, FD-8 and VC-2 are corrected as recorded.
- Prior punch lists (provenance), grepped for this audit's shapes: `grep -c -E '\.m3u|state_file|rfind\("ports"\)|UKNOWN|formatCommandLineArgument|renumberSlots|getContentFiles|deleteGameFiles|loadAdditionnalConfig'` over the eight is **0** each, and the same over every audit's `05-punch-list.md` is 0. The findings are new to the record.
- Stage C prepared, with no runtime: `second-opinions/review-plan.json` (status pending), the probe prompts, and `gpt-brief.md` and `gemini-argon-brief.md` (178 KB each: preamble, the audit's 02/03/04 without the Q6 table, and sixteen source excerpts at the pin; `grep -c -i -E 'DEV_LOGIN|devpassword|password='` = 0). Phase 4.6's calls wait for `npm install`, and the install waits for the host's return.
- **The lane waits** on the host's `resource return` for the queue at the top, then runs Phase 4.6, then Phase 5.

### [Wait] 17:54 — The coordinator read the checkpoint (#649, 17:53:44Z); the hold stands

- No `resource return` yet. Carried to Phase 5: FD-14's `bug` issue carries an `Already written:` line for what such a delete has already removed on devices, and its guest proof uses a fixture `.m3u` under `/storage` (the coordinator's words on #649).
- Waiter re-armed on #649's comment count above 4 and on a new `resource return` line in the coordination file.

### [Resume] 18:34 — `resource return` (the M7 line 18:34:04Z; the coordinator's relay on #649 18:34:33Z)

- The host at 18:34:51: 41 GiB available, swap 0 of 7 GiB used, `pgrep -f 'qemu-system-x86_6[4]' | wc -l` = 0.
- Queue item 1: `npm install --prefix tools/council` rc 0, **tsx v4.23.15** (node v24.21.0). npm warned that esbuild's postinstall is not in its allowScripts list. `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.` rc 0. `tools/council/run test`: rc 0, with suites of 39/39, **127/127** (routing) and 19/19.
- Queue item 2, #699's proofs (18:36:51-18:36:55). These are compiler runs, syntax-only; the command text is never recorded.
  - Criterion 1: `tools/es-syntax-check --root <m7-signin-build-20261022-07 root> $W/es-app/src/FileData.cpp $W/es-app/src/views/ViewController.cpp` printed the moved line, `compiler .../toolchain/bin/x86_64-rocknix-linux-gnu-g++-15.2.0`, `OK` for each, then `PASS`. rc 0.
  - Criterion 3: a copy of `LaunchCommand.h`'s includer `FileData.cpp`, with the `;` at `:719` removed, under the scratchpad, run with `--tree $W`: `error: expected ';' before 'options'` at `:719:83`, then `FAIL`. rc 1.
  - With criterion 2 (17:26) and criterion 4 (the rule sentence), all four of #699's criteria are now observed.
- Queue item 3: `es-unit-tests` (`build-tests`, toolchain cmake, host g++). It reported `185 passed | 0 failed`, `4795 assertions`, rc 0, equal to the baseline. The coordinator's build was already current, so nothing was recompiled; the run is the pin's.
- Queue item 4: `tests/app-unit`, built **out of the tree** into the scratchpad, because `build-app-unit/` is not gitignored in the ES worktree (`git check-ignore` found no rule) and building in place would leave untracked files. Built with `-fsanitize=address,undefined`, 18:37:26-18:40:01, rc 0. `app-unit-tests` 18/18 (119 assertions), `proxycards-tests` 11/11 (67), `jobs-tests` 6/6 (28), `bookkeeper-tests` 5/5 (20); each rc 0. This is the first recorded run of the three named targets, plus `app-unit-tests`.
- Queue item 5: the python harnesses. None has `--help`: each takes the source path as `argv[1]` and defaults to the tree's file, so `--help` was read as a path and failed (FileNotFoundError). That is a usage note, not a failure of the code under test. Run with no argument and `TMPDIR` set to the scratchpad: `launch-capture-gate: PASS`, `launch-deferred-state: PASS`, `hasher-offline-index: PASS`, each rc 0 (18:40:19-18:40:33). `git -C $W status --short` stays empty.

### [Guest] 18:41-18:45 — The lane's guest up; the image read

- **The image.** `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/target/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` was copied with its `.sha256` and `.identity.json` into `/workspace/artifacts/m6-t2-20261023/` (the lane's `ROCKNIX_ARTIFACTS`). `sha256sum -c` printed `OK`. The identity file names build commit `069fc270442134fe771258418adf4e666e0473fb`, `dirty: no`.
- Then `gunzip -c` → `qemu-img convert -f raw -O qcow2` → `qemu-img resize t2.qcow2 16G` (virtual 16 GiB).
- **Instance:** `generic-x64-vm run --headless --daemonize --pidfile $R/qemu.pid --serial $R/serial.sock --monitor $R/monitor.sock --vnc 20 --ssh-port 10033 $R/t2.qcow2` at 18:42:07 (`$R` = the artifacts directory), rc 0, **pid 3314372**. Before the start, `pgrep -f 'qemu-system-x86_6[4]'` counted 1 (T1's guest) and `ss -ltn` showed 10033 and 5920 free.
- `tools/vm-serial --socket $R/serial.sock wait`: ready after about 32 s. An ed25519 key under `$R` (`key`, `key.pub`; never in a tree) was provisioned over serial.
- **BUILD_ID `069fc270442134fe771258418adf4e666e0473fb`**, `VERSION="0.0.1-dev+20261022T235948Z.g069fc2704421"`, `BUILD_BRANCH="build/m7-signin-20261022-07"` (`/etc/os-release`). `strings /usr/bin/emulationstation | grep -c` finds 1 each for the slice's `STOPPING IT SO YOU CAN PLAY` and `RECORDING YOUR LAST GAME`, the pin's strings.
- `get_setting system.loglevel` is **`verbose`** (the engineering image's `DEVELOPMENT_DEFAULTS`).
- **The shipped template on the guest:** `grep -o '%[A-Z_]*%' /usr/config/emulationstation/es_systems.cfg | sort | uniq -c` counts `%CONTROLLERSCONFIG%` 125, `%CORE%` 125, `%EMULATOR%` 125, `%ROM%` 127 and `%SYSTEM%` 125, across 128 `<command>`s. `grep -c` for `%BASENAME%|%ROM_RAW%|%GAMENAME%|%SYSTEMNAME%|%GAMEINFOXML%` = **0**, and `grep -c ' -system '` = 0. That confirms Phase 2's Q6 rows (FD-2, FD-3 and FD-5 are unreached on the image) as `pin-binary` facts read from the guest.
- `/etc/emulationstation/es_systems.cfg` → `/usr/config/emulationstation/es_systems.cfg` on this x86_64 image, so #613's broken link (an H700 image) is not reproduced on GENERIC_X64. `/storage/.config/emulationstation/es_savestates.cfg` → `/usr/config/...`, so `racommands` is false on the image (SS-2's premise).
- 18:45: `tools/time-to-play --port 10033 --identity $R/key --monitor $R/monitor.sock --out $R/ttp-q5 --no-configure-remote --vm --only launch,exit,g2g --repeat 3` started in the background (harness task `bpfof0o74`; its log is `$R/ttp-q5.log`).

### [Guest] 18:43-19:0x — The stage-A tool trials and the guest proofs (each is one row in `02-forward-audit.md` § Guest proofs)

- **G-1** 18:43:14-18:46:49 `tools/time-to-play --port 10033 --identity $R/key --monitor $R/monitor.sock --out $R/ttp-q5 --no-configure-remote --vm --only launch,exit,g2g --repeat 3` exited 1 (`Not a pass`, no cloud remote, by design). A game's first frame: **0.65** s median. The next game's: **1.01** s. It works without `tools/vm-pair` (stage A trial: yes). It removed its probe ROM and `/storage/roms/gb/` at the end and left `savestates/gb/TTProbe.state.auto(.png)`, a residue noted for the tooling slice. The image ships `video_driver = "gl"` (`/usr/config/retroarch/retroarch.cfg`), so `--vm` changes nothing here.
- **G-2** 18:48:34-18:49:13 `tools/es-launch-memory --port 10033 --identity $R/key --cycles 5 --rom /storage/roms/gb/TTProbe.gb --output $R/launch-memory-1` rc 0. One pid, 1567; growth VmSize −4,992 KiB, RSS −26,300 KiB. The probe ROM was rebuilt with `time-to-play`'s own `build_gb_probe` (sha256 `085a0105...5e8e59` on host and guest) and a reboot (boot_id changed, uptime 36 s). It works without `vm-pair` (stage A trial: yes). `exit-helper return=1` is `killall`'s status, which the tool keeps by design (`tools/es-launch-memory:137-141`).
- **G-3** 18:44 the template census (`/usr/config/emulationstation/es_systems.cfg`).
- Cycle 2 fixtures: `$R/fixtures-cycle2.sh`. BusyBox `ls` has no `-f`, so `set -e` stopped it after the overlays and the rest was run by hand. Then a reboot, a new boot_id `cec36bc1-...`, uptime 24.6 s, and `/isIdle` true.
- **G-4** SD-2: reproduced. **G-5** SD-3: reproduced. **G-6** SS-1: reproduced (`exec.log:20`).
- **G-7** FD-14: walked through GAME OPTIONS > DELETE GAME > YES (frames `$R/fd14/`, the confirmation box with YES focused). Only the `.m3u` was removed; the two sentinels and the disc remain. **The finding is corrected** from a Medium outside-folder delete to a Low "never deletes the listed files", with the containment kept as latent. Re-read: `FileData.cpp:1503` (remove) precedes `:1505` (read).
- **G-8** VC-1: the synthetic `running` file (a named substitute) and a 16 Hz VNC sampler (`vc1-sample.py`). The question appeared at 0.11-0.24 s over black. **The finding is corrected** to Low: `GameTransitionStyle` defaults to `instant` (`Settings.cpp:250`) and `HideWindow` to true on ROCKNIX (`:372-376`). My reading had not read the default, which is blindspot 35 repeated by the auditor and caught by the guest. Question closed with B (KEEP WAITING) and `running` removed.
- **G-9** SD-4: reproduced with sort 28 (status 134, pid changed); the control with 27 holds. The first attempt was void because `time-to-play` had removed `/storage/roms/gb`; the probe was put back and the run repeated.
- **G-10** SR-2: 500 states, no measurable exit cost; withdrawn at this size.
- 19:04:30 the guest stopped: `tools/vm-stop $R/qemu.pid $R/t2.qcow2` printed `down: owned QEMU exited (pid 3314372)`, rc 0. No QEMU on the host after; 10033 and 5920 free. The guest's settings were restored from the copy taken before G-9, and every fixture was removed. `docs/vm-qa-log.md` has its row.
- **Ten guest proofs** (G-1 to G-10); `grep -c 'proved:' 02-forward-audit.md` = 10.

### [Phase 4.6] 19:05-19:07 — Briefs rebuilt; both seats probed; both refutation passes in flight

- Pre-issue lint before 4.6 (19:05): `tools/lint-audit-artifacts <folder> --phase pre-issue` reported 5 contract failures, all expected at this point: no reviewer provenance yet, and no `05-punch-list.md` items, index or Phase 7 gate. The five 04 sections and the renovation face Q1-Q7 were `ok`.
- The briefs were rebuilt from the guest-updated 02/03/04 with eighteen excerpts, adding `FileData.cpp:1655-1663` and `Settings.cpp:248-251`, `:368-376`: `gpt-brief.md` 187,860 bytes (sha256 `d1224767ab9021c7...`) and `gemini-argon-brief.md` 187,979 bytes (`f74ef056b1283bfa...`). `grep -c -i -E 'DEV_LOGIN|devpassword|password='` = 0. The runner sources `~/.config/council/env` itself (`tools/council/run:21-27`), so no key is on a command line.
- **Probe gpt** 19:06:24 (`tools/council/run invoke --member gpt --provider openrouter --prompt-file <abs>/gpt-probe-prompt.md --output <abs>/gpt-probe.md`): rc 0, `council-facilitator@1.14.1-pixelelated.2`, outcome success. Observed model **`openai/gpt-6-astra`**, provider **OpenAI** (PASS), identity source `provider_response`, effort `max` PASS (358 reasoning tokens). The reply was `READY unknown`; the identity check rests on the provider's field, not the reply.
- **Probe gemini-argon** 19:06:37: rc 0. Observed **`google/gemini-4-argon`**, provider **Google** (PASS), `provider_response`, effort `high` PASS (186 tokens). Reply `READY Gemini 4 Argon`.
- **Refutation passes in flight** since 19:07: `tools/watch-build --record-only -- tools/council/run invoke --member <m> --provider openrouter --prompt-file <abs>/<m>-brief.md --output <abs>/<m>-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`, one per seat. What watches them: the watched runner's record (`.build-runs/<id>/`), plus a harness background waiter per call (tasks `beqefbent` and `bl0p0w30z`) that delivers the result to this session when each command exits. If the session is reaped, the waiters say nothing, and the run's `build.rc` is the record to read.
- 19:07:05 the Argon call was **refused before any provider call**: `watch-build: another monitored build owns this worktree` (rc 2; `second-opinions/gemini-argon-audit.refused-19-07.run.log`). One monitored run per worktree, so the two refutation passes run one after the other: Argon starts when Astra's `build.rc` exists. Nothing was spent.

### [Phase 4.6] 19:26-19:4x — Both refutation passes complete and graded

- gpt: 19:07:00-19:26:32, rc 0, `openai/gpt-6-astra` by OpenAI, effort max PASS, 0 retries, output sha256 `4929f876...3bad5`.
- gemini-argon: rc 0, `google/gemini-4-argon` by Google, effort high PASS, 1 retry, 825,007 ms, output sha256 `9c89f7c6...d812`.
- Each item was graded against the pin and the guest artifacts in `04-analysis.md` § Second opinion. Re-graded: SS-1 to High; FD-14, SD-3, SD-4, MN-3 and FD-2/FD-3 to Medium. Two seat items withdrawn with their artifacts (Astra G-04 by D-CLOUD-133; Argon G-09 by design). Two disagreements recorded (FD-8 kept Low; SS-1 kept High).
- FD-12 withdrawn as an item: the tree is split, 14 toasts with two spaces after the glyph and 12 with one (`git grep -h 'displayNotificationMessage(_U(' $PIN -- es-app/src`). That is the style guide's inconsistency to settle, not this site's.
- Phase 5 (the punch list and the issues) is next.
- 20:1x Phase 5: `05-punch-list.md` written in four committed chunks in the defensive register (the coordinator's direction (c), #649 19:59Z); 35 items (High 1, Medium 6, Low 28), 35 index entries; no item went in by reference. `tools/lint-audit-artifacts <folder> --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`.
- 20:1x The 23 `bug` issues **#767 to #789** (PL-001 to PL-023), filed by reference: the body names the item, `file:line` and owner area, and points to `05-punch-list.md` § PL-nnn for the description, code trace, `Already written:` and acceptance; plus the VM line and two criteria. The classifier stopped the generator for full restated bodies once, so all 23 went in the reference shape (the coordinator's point 3). `tools/box-check --issue N` on each: rc 0, 2 open checkboxes, 0 fail.
- The audit issue **#790**, `Audit: M6 T2 EmulationStation's launch path -- 35 findings (0 critical, 1 high)`, labels `audit` and `punch-list`, milestone M6, a sub-issue of #649 (`gh api .../issues/649/sub_issues` lists it). 35 checkboxes; `tools/box-check --issue 790` rc 0, 0 fail.
- `05-punch-list.md`: every defect carries `tracked:` in the index and **Tracked work** in its item (23 each). The tracker line names #790. `tools/lint-audit-artifacts <folder> --phase pre-issue --issue 790`: `PASS pre-issue artifacts (does not certify resolution)`.
- **The stage-D pause:** posted on #649. The lane waits for the coordinator's stream briefs.

### [Stage E, S1] 20:14-20:19 — The stream briefs merged; S1 begun on the ES branch

- The coordinator tip `6f7381315f` was merged into the distribution branch (`31f0ec2a70`). The work log, friction log and index were united by whole entries, with 0 conflict markers; `register-check` passed.
- ES head commit `dd638965f` (`emulationstation: stream S1, the command and the state file`, empty, listing PL-001, PL-007, PL-021, PL-034 and PL-031).
- **PL-001 / PL-007, the test first.** New `es-app/src/LaunchTemplate.h` and `es-app/tests/unit/LaunchTemplateTests.cpp`, plus the file added to the unit tests' `CMakeLists.txt`.
  - 20:18:05, the header holding the **pin's** behaviour (the double-quoted state file, sequential replaces, a substring option test): `./build-tests/es-unit-tests -tc='state file*,template*'` gave `6 | 3 passed | 3 failed`. The failures were the state-file argument (`:95`), the re-expansion (`:120`) and the substring option (`:135`).
  - 20:18:22, the fix's behaviour: `6 | 6 passed | 0 failed`. The whole suite: **`191 passed | 0 failed`, `4809 assertions`**.
- 20:18:41 the syntax-only compile with the fixed `tools/es-syntax-check --root <m7-signin-build-20261022-07 root> --tree $W`, compiler `x86_64-rocknix-linux-gnu-g++-15.2.0`: **`PASS es-app/src/SaveState.cpp`** (rc 0). The ASCII-comment check on the three files is empty.
- **PL-007 / PL-034, the call site.** `FileData::getlaunchCommand`:
  - `formatCommandLineArgument` is retired. `%GAMENAME%`, `%SYSTEMNAME%`, `%BASENAME%` and `%ROM_RAW%` go through `Utils::String::shellQuote`, and `%ROM%` keeps `getEscapedPath`.
  - Every placeholder is replaced by one `LaunchTemplate::expand` over the finished template; the netplay branches now assign a value instead of replacing.
  - The forced `-emulator`/`-core` options are found with `LaunchTemplate::hasOption`.
  - `configureEmulators()` now runs only when `includeControllers` is true and the template names `%CONTROLLERSCONFIG%`; otherwise that placeholder is left as it is, as before, for the boot game's stored command.
  - The shipped template still names it (`functions:128`, 125 of 127 commands on the guest), so the controllers blob is still built on every shipped launch.
  - The test-first evidence is LaunchTemplateTests' 20:18:05 failure (expand, hasOption). The call site has no unit seam; its guest proof is PL-007's walk, recorded as `fix-walk-pending-image`.
- 20:21:17 `tools/es-syntax-check --root <m7 root> --tree $W es-app/src/FileData.cpp`, compiler `x86_64-rocknix-linux-gnu-g++-15.2.0`: **`PASS`** (rc 0). The ASCII-comment check on the two files is empty.
- 20:21:24 `es-unit-tests`: **`191 passed | 0 failed`, `4809 assertions`**.
- A lead, not a change: on WIN32, the `retroarch.exe` test in the netplay branches now reads the template before expansion, not the expanded line. That is upstream's Windows path, outside ROCKNIX's build.
- ES `2f26f410f` (PL-007, PL-034) committed after the lines above.
- **PL-021, the test first.**
  - `LaunchCommandTests.cpp` gained three cases: a quoted value, an explicitly empty value, and a nick that is itself an option word.
  - The `runemu` stand-in was brought to runemu.sh's reading at distribution `fe3e832e4a` (#730): whole unquoted arguments, the first `-P` after the ROM, the last `--core=`/`--emulator=`. The nick case that recorded the two readings parting company now records that they agree.
  - 20:23:45, against the unfixed header: `-tc='launch command*'` gave `11 | 9 passed | 2 failed`. The 6 failed assertions are all the header's PL-021 lines (`:190`, `:191`, `:196`, `:197`, `:205`, `:209`); every `runemu` check passed.
  - 20:24:01, fixed (`findLaunchToken`; the prefix matched on the word as written, the value read as the shell hands it on; `launchArgument` keeps the fallback for an absent word only): `11 | 11 passed`. The whole suite: **`194 passed | 0 failed`, `4829 assertions`**.
- 20:24:44 `tools/es-syntax-check --root <m7 root> --tree $W`, run from the ES worktree: **`PASS es-app/src/FileData.cpp`** and **`PASS es-app/src/main.cpp`** (the two includers of `LaunchCommand.h`), rc 0 each. The ASCII-comment check on both files is empty. Committed as ES `3872afe5a`.
- **#699, a gap in my own fix, found and closed.** At 20:24:08, run from the distribution worktree, `es-syntax-check --tree $W es-app/src/FileData.cpp` printed `MISSING es-app/src/FileData.cpp` (rc 1). The cause: the relative path was resolved against the current directory, not against the tree.
  - With `--tree`, a relative path is now the tree's.
  - 20:25:13, from the same directory: FileData.cpp and main.cpp give `PASS` (rc 0). A file the tree lacks still gives `MISSING`, `FAIL` and rc 1. `bash -n` is clean.
- **A lead for T1 (#648)**, from the new case: runemu.sh reads every whole argument, so a netplay nick that is itself a `--core=` word, one quoted argument after the real option, is read as the core. The header keeps the core ES built. `LaunchCommandTests.cpp`'s last case records the difference.
- **PL-031 deferred to #678 (T31).** Stopping the builder's write alone would empty the NICKNAME rows (`GuiNetPlaySettings.cpp:26`, `GuiGameOptions.cpp:203`) and `SystemData.cpp:1854`'s export on a fresh device. The row with the proposed move is in `04-analysis.md` § Q7.
- The fix walks W-1 (PL-001), W-2 (PL-007) and W-3 (PL-034) are written in `02-forward-audit.md` § Fix walks, each `proved: fix-walk-pending-image`.
- 20:27:37 `tests/credential-quoting.py` at the ES tip `3872afe5a`: `9 credential call site(s), 9 quoted, 0 bare`, rc 0.
- The Phase 7 outcomes are in `05-punch-list.md`: PL-001, PL-007, PL-021 and PL-034 `Resolved` with their commits, and PL-031 `Deferred` to #678. `tools/lint-audit-artifacts --phase pre-issue --issue 790`: `PASS`.
- **S1 ends at ES `3872afe5a`.**
