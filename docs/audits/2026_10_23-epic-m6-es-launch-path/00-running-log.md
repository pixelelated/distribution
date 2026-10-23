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
