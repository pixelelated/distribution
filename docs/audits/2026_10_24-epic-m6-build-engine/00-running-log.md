# Epic Audit Running Log — M6.P2 T5, the build engine

**Auditor:** Code Auditor skill (v1.13.0, identical to `next`'s copy: `diff -q` against `git show next:.claude/skills/code-auditor/SKILL.md`, no output), with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. Identity sources: the coordinator's dispatch on #652 (issuecomment-6379501933) and the session's own metadata
**Session:** herdr agent `m6-t5-build-engine`, session `c649553c-8086-4db7-ad9c-248c7e41ff95`, pane `wN:p7`
**Started:** 2026-10-24 03:51 UTC
**Scope:** slice `build-engine` (#652, `M6.P2 E800/T5`), area epic #800 (the build engine), renovation epic #339, milestone M6. The membership is the inventory's `k: 5` rules (brief § 2): 242 paths, re-derived below
**Spec:** `docs/reviews/briefs/build-engine.md` version 2 (`01ff4c0bcd`; its § 7 is #652's checklist); `docs/reviews/plan-for-the-plan.md`
**Depth:** Extended (two reviewers from two other labs: GPT-6 Astra `--member gpt` at `max`, Gemini 4 Argon `--member gemini-argon` at `high`; refutation pass alone each)
**Branch / worktree:** `feature/m6-build-engine-652` at `/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-652`
**Read hash:** the slice's bytes are `next`'s `8ebaf8daad`; **`reviewed-at` = `46f6c7d428`** (the branch `HEAD` at stage A; the commit that carries this log changes no slice path)

Every log line read in this audit goes through `readlog() { grep -v -i -E 'key|pass|token|user|psk|login' "$@"; }` or the masking `sed` of brief § 5; no build command line or `.env` content is reproduced here.

---

## Log Entries

### [Phase 0] 03:51 — The brief's first commands (`date -u` 03:51:34)

- `git fetch origin`, `git fetch upstream --no-tags`: both exit 0.
- Branch `feature/m6-build-engine-652`, `HEAD` `30b1bb38c069e841903f5ef3ce7c8ae5d58b3d2a`; `git merge-base --is-ancestor 2174265e9c HEAD` exit 0: stacked on the P1 tip.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md`: four files (37+/2-), `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `.claude/skills/council/IMPORTED-FROM.md`, exactly the dispatch's four. Nothing stale.
- `grep -c 'Renovation face' tools/lint-audit-artifacts` 4; `grep -c gemini-argon tools/lint-audit-artifacts` 4; `grep -c gemini-argon scripts/council-invoke.ts` 7 (the brief: 4, 4, 7).
- P1's and #644's files present: `tools/renovation-{inventory,status,drift}`, `docs/reviews/{inventory,slices}.json`, `docs/reviews/build-path-read.md`. The brief and the epic's futro `docs/futros/2026-10-24-m6-build-engine.md` present.
- `next` = `8ebaf8daad`. **`upstream/next` = `3421d7d178`** (committed 2026-10-23T21:22:36Z; Q4's upstream, fetched now). `git merge-base next upstream/next` = `c445081a59518f37d9776e5412dd7b14910696f7`. 323 upstream commits past the base.
- The stage-A byte check with the membership's exclusions (`git diff --quiet 8ebaf8daad HEAD -- <the brief's pathspec>`): exit 0, **the slice's bytes are `next`'s at `8ebaf8daad`**.
- `core.hooksPath` lists `commit-msg guard-lib hooks-test pre-commit pre-push secret-patterns`.
- `node` v24.21.0, `npm` 11.19.0; `tools/council/node_modules` absent (the § 1 install waits for the host's return and comes before Phase 4.6).
- The host file `/tmp/m7-m6-host-coordination-20261023.txt`, last block: `== M7 root — 2026-10-24T03:47:08 ... handoff read and accepted. Source preparation/review still active; no VM/compiler launched yet.` **A window is open (M7's from 03:47):** no guest, compiler or `npm install` from this lane until the coordinator relays the return on #652.

### [Phase 0] 03:52 — Start confirmed; lane start committed

- Start comment on #652: issuecomment-6379521847.
- Work-log entry in `2026_10_24-work_log.md`, `tools/work-log-index --write` rc 0; commit `46f6c7d428`, pushed (`git push -u`, rc 0). The entry's heading was first written `03:55 UTC`, an estimate; the commit's time is 03:52:38, so the heading is corrected to `03:52` in the next commit, and every time from here is read from `date -u`.
- `tools/register-check`: `660 IDs, each once` (rc 0).
- `tools/ceremony-check --gate` exits **1** on `weekly: 2026-W42 summary missing`; the push guard enforces the gate only on pushes of `next` (T3's log reads `.githooks/pre-push` 329), so the feature push went through without `--no-verify`. W42 predates this lane (brief § 9: the M7 lane's week); noted on #652 as owed elsewhere.

### [Stage A] 03:53 — The membership re-derived (brief § 2)

- The filter of brief § 2 over `docs/reviews/inventory.json` (python3 -I, rc 0; output `.qa-scratch/t5/stageA-filter.out`, the path list `.qa-scratch/t5/membership.txt`): **242 paths, 13,910 lines; 18 fork-own (3,266 lines), 224 upstream-carried, no vendor-carried; code-class lines 6,776, of which fork-own 2,419.** All six equal the recorded figures: no delta. `order()`'s own predicate (CODE, not vendor-carried, not `unreached`; `tools/renovation-inventory` 1274 to 1276) gives the same 6,776 and 2,419, since every row's `reach` is `n/a`. The tool's `CODE` set read at `tools/renovation-inventory` 674 to 676: as the brief quotes it, no `yaml`.
- The globs alone: 647 paths (`build-engine` 242, `tooling-and-guards` 52, `records` 353).
- `git ls-files scripts config distributions/ROCKNIX Makefile Dockerfile .gitignore .merge-head .github/workflows .github/ISSUE_TEMPLATE .github/pull_request_template.md .github/scripts`: 294; minus the membership, 52, every one `tooling-and-guards` (T10's): 46 under `scripts/` (the council toolchain, `scripts/lib/` 24, `scripts/__tests__/` 2 and the rest), the 4 `fork-*.yml` and the 2 `.github/scripts/*.sh`. No membership path is outside that listing; every membership path exists at `HEAD`.
- Fork commits on the membership `c445081a59..8ebaf8daad`: **31** (the brief's 31). Upstream's `c445081a59..upstream/next` on the membership: **3**, `c4d353449e` (2026-10-18, aethersx2 dropped), `76693a738d` (2026-10-13, ci: GitHub username in the release), `c200cc906d` (2026-10-07, the pull request template): the brief's three.
- **The M7 delta** (`git -C /workspace/repos/rocknix log next..069fc2704421 -- <the membership>`; the legacy `next` is `8ebaf8daad` too): 12 commits past `next`, **none on the membership**.
- **The branch scan** (predicate: `git log --oneline next..<branch> -- <the membership>` prints a line; over `refs/heads` and `refs/remotes/origin` of this clone): 17 branches, all old remote branches (`origin/feature/conflict-resolution` 8, `origin/x64-build-fix` 6, `origin/backup/generic-x64-pre-rebase-20260714` 5, `origin/rclone-bisync-beta` 3, `origin/pr/01-build` to `pr/10-es-pin` 1 to 2 each, `origin/pr/cairo-1.18` 1, two `verification-anchors/2026-09-30-*` 1 each); no local or M6 branch. The list is in `01-research-notes.md` § Scope; posted on #652 as a lead, not read.
- **The host:** still M7's (03:47 block the last at 03:53:48).

### [Phase 0] 03:56 — Reading (§ 3, the pre-flight)

- **Read whole:** the lane's pointer; the brief (version 2, 1,095 lines); `docs/reviews/build-path-read.md` (#644, 216 lines; the nine findings this slice carries: 1, 3, 4, 8, 9, 10, 11, 13, 22); the futro `docs/futros/2026-10-24-m6-build-engine.md` § 4 and § 5 (the simulation, the pre-mortem and the plan edits); the dispatch comment and the coordinator's stage-A reply (issuecomment-6379559529: carry on without waiting). T3's `02-forward-audit.md` structure and its § The host regeneration and F-06, at T3's tip `2481a04332`, read with `git -C`/by path, never written.
- **The rules this session read in full** (they are loaded in this session's context, `next`'s copies but the four files the stage-A diff names): `engineering-practices.md`, `device-builds.md`, `upgrade-and-install.md`, `fork-workflow.md`, `worktrees.md`, `issue-tracking.md`, `decision-register.md`, `learning-capture.md`, `ceremonies.md`, `milestone-phase-naming.md`, `adversarial-council.md`, `working-principles.md`, `instruction-files.md`, `release-candidates.md`, `bugs-are-agent-first.md`, `vm-first.md`, `time-to-play.md`, `least-surprise.md`, `player-language.md`, the four ES rules, `handheld-evidence.md`. **Not yet read this session:** `docs/reviews/plan-for-the-plan.md` beyond the brief's citations, `packages/README.md`, `packaging-and-patches.md`, `change-log.md`, `generic-x64-vm-testing.md`, `docs/blindspot-register.md` whole, the code-auditor skill's references; each is read before the stage it governs (Phase 3's interaction audit, Phase 4's analysis and the punch list).

### [Stage B] 03:57 — Phase 1

- Closed `bug` issues: `gh issue list --repo pixelelated/distribution --label bug --state closed --limit 500 --json number,title,body` (rc 0), 139 issues; pattern `(?<![\w/-])(scripts/build|scripts/image|get_env|calculate_stamp|mkimage|build_distro|Makefile|\.env|wrap-mode|build-identity)(?![\w-])` over title and body: **2** (#226, #413).
- Prior audits: `grep -c -E 'scripts/(build|image|install|mkimage|get_env|build_distro)|config/(functions|options|build-identity)|Makefile|\.env|wrap-mode'` per `05-punch-list.md`: 3 of 20 folders, 1, 6 and 9 lines (`2026_09_13-milestone-stable-before-upstream`, `2026_09_24-milestone-rc-round-since-186`, `2026_09_25-milestone-rc-round-since-258`). Compared after Phase 2 is written, never transcribed.
- The register: `grep -ciE 'scripts/(build|image)|get_env|Makefile|build-identity|calculate_stamp|watch-build|admission' docs/decision-register.md` 8 lines.
- Upstream's trackers (D-WORKFLOW-162), 03:57 UTC: `gh pr list --repo ROCKNIX/distribution --state all --limit 300 --search "updated:>=2026-09-01" --json number,title,state,mergedAt,files` (300 returned: **the limit, so the window is truncated**), intersected with the 242 paths; `gh pr list --repo LibreELEC/LibreELEC.tv --state all --limit 200 --search "updated:>=2026-08-01"` (200 returned, the limit), intersected with the engine's file prefixes. Hits in `01` § Phase 1.

### [Stage B] 03:58 — The mechanical checks

- `bash -n` 41 ok (26 scripts, 15 fragments); `py_compile` 5 ok (its `__pycache__/` removed); `tools/build-identity-test` rc 1, `21 passed, 2 failed` as #801 expects; `tools/host-maintenance/test-build-monitor` rc 0, `36 PASS; 0 FAIL` (read first: temporary directories, stub docker, no compiler); `tools/fork-package-freshness --list` rc 0, 47 recipes, none of the slice; `tools/pkgcheck rocknix` rc 0. Detail in `02` § Mechanical checks.
- 04:01 shellcheck v0.11.0, the release's digest checked (`sha256sum -c` OK); 5 errors, 271 warnings over 41 files; the errors read at their sites (`02` § shellcheck errors).

### [Stage B] 04:00 to 04:11 — The sandboxes, the manifests, the workflows

- One harness refusal, recorded as friction: a scratch-tree set-up that began with `rm -rf "$F"` over a variable path was stopped by the session's safety check (04:05); the trees were made with `mkdir` into new names instead, and no removal was run. The committed sandbox scripts take an explicit scratch directory (`${1:?}`) rather than writing beside themselves.
- 04:08 the two container manifests read without a pull, and the two config blobs through GHCR's anonymous token; the 19 workflows' states from `gh`.

PROOF: 04:00 P1 `scripts/get_env` over a constructed environment -- `tools/sb-get-env.sh`, trace `.qa-scratch/t5/sb-get-env/trace.txt` (F-01, F-02)
PROOF: 04:02 P2 `calculate_stamp` over a fixture override and its generic twin -- `tools/sb-calculate-stamp.sh` (F-05)
PROOF: 04:04 P3 the GENERIC_X64 launch table regenerated, byte-identical to `069fc2704421`'s install tree -- `tools/regen-es-systems.sh`
PROOF: 04:05 P4 case A, two default lines -- `tools/sb-es-cases.sh` (F-04)
PROOF: 04:05 P5 case B, a false core before the true one -- `tools/sb-es-cases.sh` (F-04)
PROOF: 04:05 P6 case C, a system after imageviewer -- `tools/sb-es-cases.sh` (F-03)
PROOF: 04:06 P7 `daphne` and `gp32` `<release>` in two install trees, read-only (F-03)
PROOF: 04:10 P8 `scripts/unpack` 90's test with one and two matches -- `tools/sb-unpack-glob.sh` (F-08)
PROOF: 03:58 P9 `tools/build-identity-test`, 21 identity checks passed (the 2 failures #801's)
