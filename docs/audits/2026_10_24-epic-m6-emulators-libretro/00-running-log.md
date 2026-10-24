# Epic Audit Running Log — M6.P2 T3, RetroArch and the libretro cores

**Auditor:** Code Auditor skill (v1.13.0, identical to `next`'s copy: `diff -q` against `git show next:.claude/skills/code-auditor/SKILL.md`, no output), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #650 (issuecomment-6378830351, 2026-10-24T02:36:34Z) and the session's own metadata
**Session:** herdr agent `m6-t3-emulators`, session `a6d65411-5a44-4596-9a6c-337855905c17`, pane `wN:p6`
**Started:** 2026-10-24 02:38 UTC
**Scope:** slice `emulators-libretro` (#650, `M6.P2 E798/T3`), area epic #798 (the emulators and cores), renovation epic #339, milestone M6. The membership is the inventory's `k: 3` rules (brief § 2): 344 paths recorded
**Spec:** `docs/reviews/briefs/emulators-libretro.md` version 2 (`f650d65522`; its § 7 is #650's checklist); `docs/reviews/plan-for-the-plan.md`
**Depth:** Extended (two reviewers from two other labs: GPT-6 Astra `--member gpt` at `max`, Gemini 4 Argon `--member gemini-argon` at `high`; refutation pass alone each)
**Branch / worktree:** `feature/m6-emulators-libretro-650` at `/workspace/repos/pixelelated/distribution.worktrees/m6-emulators-libretro-650`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; `reviewed-at` is the branch `HEAD` at stage A, recorded below

---

## Log Entries

### [Phase 0] 02:38 — The brief's first commands (`date -u` 02:38:14)

- `git fetch origin`, `git fetch upstream --no-tags`: both exit 0.
- Branch `feature/m6-emulators-libretro-650`, `HEAD` `af35d54f87270ceafc351a08b38bc28a7f2c78ed`; `git merge-base --is-ancestor 2174265e9c HEAD` exit 0, so the branch is stacked on the P1 tip.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md` lists four files (37+/2-): `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `.claude/skills/council/IMPORTED-FROM.md`. These are exactly the four the dispatch and the pointer name, so nothing is stale.
- `grep -c 'Renovation face' tools/lint-audit-artifacts` 4; `grep -c gemini-argon tools/lint-audit-artifacts` 4; `grep -c gemini-argon scripts/council-invoke.ts` 7 (the brief: 7 and 4).
- P1's `tools/renovation-{inventory,status,drift}`, `docs/reviews/inventory.json` and `slices.json` are present.
- `next` = `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`. **`upstream/next` = `3421d7d178`** (Q4's upstream, fetched now). `git merge-base next upstream/next` = `c445081a59518f37d9776e5412dd7b14910696f7`.
- `git diff --quiet 8ebaf8daad HEAD -- projects/ROCKNIX/packages/emulators/libretro projects/ROCKNIX/packages/virtual/emulators`: exit 0, so **the slice's bytes are `next`'s at `8ebaf8daad`**.
- The brief and the futro (`docs/futros/2026-10-24-m6-emulators-and-cores.md`) are both in the tree. `core.hooksPath` lists `pre-push`.
- `git push -u origin feature/m6-emulators-libretro-650`: already up to date; tracking set.
- The host file `/tmp/m7-m6-host-coordination-20261023.txt`: its last two blocks are M7's `resource return` at 02:22:37 UTC and the coordinator's relay at 02:23. **No window is open.**
- `node` v24.21.0, `npm` 11.19.0; `tools/council/node_modules` is absent (the § 1 install comes before Phase 4.6).

### [Phase 0] 02:39 — Start confirmed; lane start committed

- Start comment on #650: issuecomment-6378851675.
- Work-log entry `T3 lane started` in `2026_10_24-work_log.md`, then `tools/work-log-index --write` (rc 0); commit `e1af3b2ba5`, pushed. The entry's heading was written as `02:45 UTC`, an estimate; `date -u` read 02:40:44 just after. It is corrected to `02:40` in the next commit, and every time from here is read from `date -u`.
- `tools/register-check`: 660 IDs, each once (rc 0).
- `tools/ceremony-check --gate` exits **1** on `weekly: 2026-W42 summary missing`. No branch carries a W42 summary (`origin/next`, the P0 and P1 branches: 0). The pre-push hook enforces the gate only on pushes of `next` (`.githooks/pre-push` 329, `refs/heads/next`), so the feature push went through without `--no-verify`. W42 (2026-10-12 to 18) predates this lane; it is noted on #650 as owed elsewhere, as T1 noted it on #648. The same report shows `box-check` red in CI (one failing checkbox across the tracker), which is not this lane's.

### [Phase 0] 02:42 — Reading (§ 3, the pre-flight)

- **Read whole:** the lane's pointer; `docs/reviews/plan-for-the-plan.md`; the brief (version 2, 1,191 lines); the futro `docs/futros/2026-10-24-m6-emulators-and-cores.md` with its erratum (the comment on #798 of 02:32 says the same as the file's § 1); the skill `SKILL.md`; `packages/README.md`; `packaging-and-patches.md`.
- **Issues read:** #650's body. Its fifteen criteria equal brief § 7, with two wording differences, both noted: criterion 9 asks `git apply --check` of the eight patches where the brief's § 4 says `patch -p1 --dry-run` (#650 wins, so both are run and `git apply --check` is the cell); criterion 12 lists four `proved:` classes where § 6 adds `fix-walk-pending-image`. Also read: the dispatch comment; #798's body and comments; #339's body (first 3.5 KB: the tiers and Tier 2's *"there is no longer anyone to send them to"*); #346's last three comments; the hand-back and stage-F comments on #648 (T1: `reviewed-at` `efadfea08a`, `fixed-at` `0f7558cff7`, tip `ba22eea867`, nine `fix-pending-image` rows) and on #649 (T2: 21 `fix-walk-pending-image` walks, ES tip `55158d2a6`, `time-to-play` 0.65 s and 1.01 s median at the pin).
- **Criterion 12's token, carried:** `grep -c 'proved:' 02-forward-audit.md` must equal `grep -c '^GUEST-PROOF:' 00-running-log.md`. So the string `proved:` appears in `02` only in guest-proof rows, and a running-log line begins with `GUEST-PROOF:` only to announce one. This entry names the token without starting a line with it.
- **Rules:** the every-session set was loaded this session from the worktree, which differs from `next` only in the four files above; `AGENTS.md` equals `next`'s and carries the same facts as `CLAUDE.md` (kept equal by `tools/rules-check`, D-WORKFLOW-045). Read in this session's context: `time-to-play.md`, `upgrade-and-install.md`, `engineering-practices.md`, `bugs-are-agent-first.md`, `vm-first.md`, `issue-tracking.md`, `decision-register.md`, `learning-capture.md`, `ceremonies.md`, `worktrees.md`, `fork-workflow.md`, `milestone-phase-naming.md`, `adversarial-council.md`, `working-principles.md`, `device-builds.md`, `release-candidates.md`, `instruction-files.md`, `handheld-evidence.md`, and the four ES rules (the interface's, not this slice's).
- **Blindspots read in full:** 38, 39, 47, 48, 50, 54, 55, 63, 65, 73, 74; the table rows of 1 to 28 by title. Carried into the read: 39 (no empty cell in a measuring table: the Q4 scan's assertion), 47 (the `FetchContent` grep), 48 (`git log -p` before judging any option), 50 and 55 (a log line is this run's only once tied to its launch), 54 and 63 (read `Using resolution` and `[GL] Renderer` before any RetroArch number), 65 and 74 (a fixture or a bind is part of the claim, and its hash is printed before the verdict).
- **Not yet read, opened when their phase needs them:** `generic-x64-vm-testing.md`'s sections (before the guest), `rclone-cloud-sync.md` § the save layout (Phase 3.5), `change-log.md` (stage E), the remaining phases of the skill (`phases.md`, `templates.md`, `review-levels.md`, `anti-patterns.md`, each before its phase), the decisions by ID (from the register as each is cited), the open issues of brief § 3 (Phase 1), and the prior audits' punch lists (counts only, after stage B's Phase 2).

### [Stage A] 02:41-02:49 — Scope re-derived; #799 filed and fixed

- **Counts** (brief § 2's filter, `python3 -I`, over `inventory.json` at `00ca350666`): 344 paths, 31,961 lines; 24 fork-own / 6,557 lines (1,038 of them GENERIC_X64 configuration); 299 upstream-carried; 21 vendor-carried / 1,670 lines, 8 fork-written / 1,244; 294 / 21 / 29 by area; 342 `shipped`, 2 `n/a`. **No delta.** `git ls-files` over the two directories gives 406 = 344 + 57 core patches (T42's) + 5 recipes (T24's). The patches' numstat sums to 1,670. All recorded in `01` § Scope.
- **Upstream:** `c445081a59..upstream/next` (`3421d7d178`) on the two directories is 14 commits, the brief's list exactly; 54 fork commits on the same paths since the base.
- **Branch scan:** 54 `origin` branches, 18 ahead, 44 differ (the brief's counts). **Correction:** `origin/feature/m7-player-setup` is ahead by `d9054efc46`, with `Install Steam.sh` blob-equal to `next`'s, and `6101242e14` is on no `origin` branch (only `legacy/m7-audit-integration-603`). It goes to #650 as a lead.
- **M7 delta:** `next..069fc2704421` touches one file, `Install Steam.sh` +605/-6, one commit `6101242e14`, eight hunks; tabled in `01`.
- **Image:** copied to `/workspace/artifacts/m6-t3-20261024/`, `sha256sum -c` OK; `.identity.json` `build_commit` `069fc270442134fe771258418adf4e666e0473fb`, `dirty` `no`. The guest's `/etc/os-release` is still to read. `df /workspace` 1.8 T free; `free -g` 45 G available, **swap 6 of 7 G used**; no QEMU and no `make docker-` running.
- **#336's body read; the line is drawn as the brief § 4 draws it** (`01` § Scope).
- **#799** (`Bug: retroarch-wrapper-test cannot run without a path ...`) filed at 02:45 before the fix. The fix is `d606301784`. Runs:
  - unfixed no-argument rc 2;
  - fixed no-argument PASS rc 0 (pin `bdba046fa6`, 12 byte-identical candidates, sha256 `b578746e…`);
  - explicit path PASS rc 0;
  - constructed pin failure rc 2;
  - 0015 reversed: 2011 calls of 2000, FAIL, rc 1.
- **Found alongside:** `--gated` is dead since `e5d14d4220` (parsed at line 57, never read; a `--gated` run printed the plain run's lines). Recorded for the punch list.
- **Another small delta:** the brief names `m7-signin-h700-build-20261023-05`; the host also has `-06`, and `-06` holds the live H700 aarch64 root.
- **`reviewed-at: d606301784`**: the slice's bytes there equal `8ebaf8daad` (`git diff --quiet`, exit 0).
