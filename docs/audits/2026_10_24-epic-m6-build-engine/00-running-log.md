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

### [Stage B] after 04:11:41 — The fork-own files, Q4 (a), Q6, the recorded runs

- Read with their fork commits: `scripts/get_env`, the `Makefile` (1 to 60, 120 to 208), `config/build-identity`, `distributions/ROCKNIX/version`, `scripts/image` (its diff against `upstream/next`), `scripts/build_compat`, and the diffs of `build_distro`, `install`, `extract`, `show_config`, `graphic`, `options`, `distributions/ROCKNIX/config/functions`, `.gitignore`, the two PR workflows. F-06, F-07, F-09, F-13, F-14 written.
- Q4 (a): `git diff --name-status upstream/next 8ebaf8daad -- <the 242 paths>`, 21 files, each with its fork and upstream commits since the base (`.qa-scratch/t5/q4a-table.tsv`); three differ only by upstream's (F-12).
- Q6: the caller search for the 30 scripts (fixed strings, the second pattern for each zero, then `scripts/get`'s dispatch); four device tables regenerated; `q6-tables.md` written (Tables 1 to 5).
- The subagent dispatched: one read-only research subagent (general-purpose) over the upstream core (`config/functions` and the 22 other core files), returning leads only; every lead is re-read before it is a finding (brief § 5 rule 5).
- The recorded runs (read-only, `readlog` filtered): `m7-signin-build-20261022-07/.build-runs/20261022T235954Z-4749157a` (GENERIC_X64, 23:59:54 to 00:05:01, `[654/654]`, rc 0), `m7-signin-h700-build-20261023-06/.build-runs/20261024T014932Z-8a1ff937` (H700, 01:49:32 to 02:00:04, `[671/671]`, rc 0; its predecessor `20261024T013624Z-826391e2` rc 1 after 2 minutes, `progress: none matched`), `m7-signin-sm8550-build-20261023-03/.build-runs/20261024T020912Z-68374394` (SM8550, 02:09:12 to 02:20:16, `[737/737]`, rc 0). No ccache statistics in any of them.
- The meson logs of the GENERIC_X64 root for the wrap mode.

PROOF: 04:11-04:31 P10 `-Dwrap_mode=nodownload` in all 85 meson logs of the GENERIC_X64 build root, read-only
PROOF: 04:11-04:31 P11 the H700 and SM8550 launch tables regenerated, byte-identical to their install trees -- `tools/regen-es-systems.sh`

### [Stage B] before 04:31:01 — Phase 3 written; F-15; the `.env` scan

- `03-retrospective.md` written (3.1 to 3.6.5: the instruction files and blindspots against the findings, six seams, the futro's predictions checked).
- `config/options` 86 to 152 read: `CONCURRENCY_MAKE_LEVEL=$(nproc)` (91), `CCACHE_CACHE_SIZE="15G"` (100), `CCACHE_COMPRESSLEVEL="0"` (109), `CCACHE_SLOPPINESS="pch_defines,time_macros"` (118); the options files at 132 to 140 led to F-15 (`~/.rocknix/options` against `~/.ROCKNIX/options`; both tested by `test -f` and mode only).
- `.env` at rest: none in 134 checkouts.

### [Stage B] before 04:31:01 — The subagent's leads re-read

- The research subagent returned (it ran 8 minutes 41 seconds by the harness's count) (28 leads, the sections of `config/functions`, the `set -e` status); a lead, never evidence (brief § 5 rule 5).
- Re-read at their sites: `scripts/mkimage` (F-16), `find_path`/`calculate_stamp`/`kernel-firmware` (F-17, P12), `get_git` 30 to 52, 193 to 218 (F-18, P13), `get_archive` and `update_packages` 46 to 64 (F-19; the subagent's line numbers for `update_packages` were wrong, 108 and 117 for 52 and 61), `checkdeps` 255 to 345 (F-20), and five small ones (F-21). Lead 11 found partly wrong (the failure path is caught). `config/functions` 948 to 962 and `5ce3dcc9d7`: the libtoolize guard, merged upstream as PR #3213 (`02c9dd740e`), widens F-05 (`device-builds.md` § After rebasing items 2 and 3 both describe fixed defects).
- Not re-read: 17 leads, listed in `02` as leads.

PROOF: 04:11-04:31 P12 `calculate_stamp` unchanged by a device-level file `find_file_path` reads -- `tools/sb-stamp-device-config.sh` (F-17)
PROOF: 04:11-04:31 P13 `get_git`'s cache check accepts `PKG_VERSION` matching a remote ref while `HEAD` differs -- `tools/sb-get-git-head.sh` (F-18)

### [Stage B] 04:31 — Clock correction

- `date -u` read **04:31:01** while the criterion entries were being written, and the entries since the previous reading (04:11:41) had been stamped by estimate as late as 04:50: the same shape as the 03:52 heading. Every stamp written between the two readings is corrected in place to the bracket the two readings support (`after 04:11:41`, `before 04:31:01`, `04:11-04:31`); the order of the entries is the order the work was done. From here, every stamp is a `date -u` reading taken at the moment it is written. A friction line records it (the second time in this lane).

### [Stage B to C] 04:34 — `04-analysis.md` written; the pre-issue lint

- `04-analysis.md` (Phase 4, 4.5 with one lead withdrawn, the renovation face Q1 to Q7 with Q4's two tables, Q5's runs and ccache table, Q6's summary of `q6-tables.md`; § Second opinion pending on the host).
- `tools/lint-audit-artifacts docs/audits/2026_10_24-epic-m6-build-engine --phase pre-issue`: 5 contract failures, all expected at this stage: the review plan's call evidence (no provenance file yet: Phase 4.6 waits for the host) and `05-punch-list.md` (not yet written: Phase 5 follows 4.6). Every `04` section, the renovation face's Q1 to Q7 included, reads `ok`.

### [Stage C] 04:34 — The reviewers' briefs, written and not sent

- `second-opinions/gpt-brief.md` and `gemini-argon-brief.md` (242,776 and 242,802 bytes): the same packet, a three-part instruction (own findings, refute the Mediums and Highs, what could not be judged), `02` to `04`, `q6-tables.md`, and the code at each finding's site from `8ebaf8daad` (16 excerpts). Neither carries the other's output. No credential-shaped value line (a pattern search, and the pre-commit scan on this commit). The two probe prompts (one line each).
- **Not sent:** the `npm install --prefix tools/council`, `verify-pins`, `test`, the probes and the two refutation calls wait for the host window's return line relayed on #652 (brief § 1, § 5). Until then Phase 5 is not final and no issue is filed.

### [Stage C] 04:37 — `05-punch-list.md` drafted (before Phase 4.6)

- 22 items from `tools/punch-items.py` (2 High, 7 Medium, 13 Low; a 23rd, F-22, added after the subagent's leads 21 and 22 were re-read), every one with its question, `Already written:`, the VM line and an acceptance an agent can check; nine marked for `bug` issues at stage D, seven deferred to a named issue (#651 T4, #657 T10, #652 the coordinator's), eight #585 candidates. **Draft:** the reviewers' grades come first, and nothing is filed before them.
- `tools/lint-audit-artifacts ... --phase pre-issue`: **1 contract failure**, the review plan's call evidence (no provenance file until Phase 4.6 runs). Everything else `ok`.

### [Stage C] 04:39 — Leads re-read while the host is held

- Re-read: leads 5, 21, 22, 25, 27 (`get_git` 13 to 18, `scripts/build` 598 to 612, `config/multithread` 60 to 66, `scripts/makefile_helper` 22 to 28, `config/arch.aarch64` 17 to 40 with the five devices' `TARGET_CPU`). 21 and 22 confirmed as F-22 (Low; PL-21); 5, 25, 27 left latent or by design, said so in `02`. `05` regenerated: 23 items.

### [Stage C] 05:48 — Phase 4.6 started on the host's return

- The coordinator relayed M7's `resource return` (05:42) on #652 at 05:43 (issuecomment-6380512709); the host file's 05:42 block read.
- The briefs rebuilt from the current `02` to `04` and `q6`, with two more excerpts for F-22's sites (`config/multithread` 40 to 70, `scripts/makefile_helper` 1 to 30); the builder, until now only a session command, kept as `tools/build-briefs.sh`. Committed before sending (`9c23bb5095`): `gpt-brief.md` 246,501 bytes sha256 `9fe85311…`, `gemini-argon-brief.md` 246,527 bytes sha256 `a88a9618…`. No credential-shaped value line; `tools/forbidden-terms-check` 0 hits.
- `npm install --prefix tools/council` 05:45, rc 0 (tsx v4.23.15, node v24.21.0; esbuild's install script not approved and not needed). `tools/council/run verify-pins`: `OK`, rc 0. `tools/council/run test`: rc 0, 39 + 127 + 19 tests, 0 failed.
- **Probe gpt** 05:47:07 to 05:47:16: rc 0, `council-facilitator@1.14.1-pixelelated.2`, outcome success, model `openai/gpt-6-astra`, provider OpenAI, effort max (281 reasoning tokens), identity source `provider_response`, 0 retries; the reply `READY unknown` (the identity rests on the provider's field, not the reply).
- **Probe gemini-argon** 05:47:16 to 05:47:21: rc 0, the same Facilitator, model `google/gemini-4-argon`, provider Google (route `google-vertex/global`), effort high, identity source `provider_response`, 0 retries; the reply `READY Gemini 4 Argon`.
- **Refutation passes in flight.** gpt since 05:47:31: `tools/watch-build --record-only -- tools/council/run invoke --member gpt --provider openrouter --prompt-file <abs>/gpt-brief.md --output <abs>/gpt-audit.md --per-attempt-timeout-ms 1800000 --total-timeout-ms 3600000`, recorded in `.build-runs/20261024T054731Z-0b725524/`, with a harness waiter (task `blyfq5xdl`). gemini-argon: the same command under `watch-build` was refused locally (`another monitored build owns this worktree`, rc 2; nothing sent), so it runs through the Facilitator directly since 05:48 (output and provenance written by the Facilitator; log `.qa-scratch/t5/argon-audit.run`), with a harness waiter (task `bk9n66x96`). If this session is killed, both waiters die silently; then the watcher's `build.rc` (gpt) and the Facilitator's provenance file (argon) are the records to read.

### [Stage C] 05:54 to 06:12 — Phase 4.6 graded; F-25 proved; `05` final

- **gemini-argon** returned at 05:54:26: rc 0, 392,700 ms, 0 retries, `google/gemini-4-argon` by Google, identity PASS (`provider_response`); `gemini-argon-audit.md` sha256 `c7ea46aa…`. **gpt** returned at 06:04:49: rc 0, 1,038,085 ms, 0 retries, `openai/gpt-6-astra` by OpenAI, effort max, identity PASS; `build.rc` 0; `gpt-audit.md` sha256 `b8d3f25c…`.
- Each seat item read at its site at `8ebaf8daad`, or by a sandbox or a read-only M7 artifact, and graded in `04` § Second opinion (Argon 17 items, Astra 19). Checks run for the grading: the cache keying (`config/functions` 1350, `scripts/get` 27); `CLEAN_OS_BASE` (`distributions/ROCKNIX/options` 45); `start_multithread_build`'s four callers; the shared bootloader hook; `DISTRO_MIRROR`; the 47 suffix values; the 139 `add_es_system` calls against their fragments; 1,347 archive recipes against `PKG_SHA256`; `chmod -R` over dangling symlinks (rc 0) and over an unmatched glob (rc 1); `config/options`'s stdout with a scratch `HOME` (one line); the SM8550 run's log for `GET (git)` through the filter; the M7 H700 root's initramfs and image stamp dates (read only).
- **F-25** (Astra G-01, High): P14 below. **F-23** (Argon G-01 = Astra G-10) and **F-24** (Argon G-03) Low. **F-18** High to Medium (the cache is keyed by the pin; Astra), **F-17** Medium to Low (`kernel-firmware` is cleaned at every device build; Astra). F-18's sentence on the fresh-clone path corrected in place in `02` (Argon G-06). The seats' re-grades of F-08, F-15, F-19 and F-22 declined, each on an artifact; Argon G-04 and Astra G-09 and G-17 declined.
- `05` regenerated from `tools/punch-items.py`: **26 items, 2 High (F-16, F-25), 7 Medium, 17 Low**; 10 for `bug` issues (drafts regenerated in `stage-d-bug-drafts/`, PL-01 to PL-10). The items are renumbered in severity order, so the PL-21 named at 04:39 (F-22) is now PL-22.
- `02`: F-23 to F-25 written, Phase 4.6 notes under F-16, F-17, F-18 and F-22, the coverage cells of `config/build-identity`, `config/functions`, `scripts/build_distro` and `scripts/get_git` updated (the table regenerated: 242 rows, 0 empty cells), AC-01, AC-03, AC-10 to AC-12 and AC-13 re-evaluated. `review-plan.json`: both seats completed.

PROOF: 06:07:52 P14 `get_git`'s cache check over a directory it cannot enter runs `git clean -fdx` in the caller's tree -- `tools/sb-get-git-pushd.sh` (F-25)

### [Stage D] 06:15 to 06:16 — The ten bug issues and the audit issue filed

- `tools/sb-get-git-pushd.sh` now lifts `_clean_repo` and `_repo_exists_and_valid` by name, so it still runs against a fix that moves lines; rerun at 06:14:45 with the same result (`after: .git`). F-25's criterion names the fix commit as its second argument.
- The ten drafts regenerated (with the folder's link) and pre-checked against `tools/box-check`'s patterns and `tools/forbidden-terms-check --stdin` (no hit). Filed 06:15 with the label `bug` and no milestone: PL-01 #827, PL-02 #828, PL-03 #829, PL-04 #830, PL-05 #831, PL-06 #832, PL-07 #833, PL-08 #834, PL-09 #835, PL-10 #836. `tools/box-check --issue N` on each: rc 0, 2 open checkboxes, 0 fail.
- The audit issue **#837**, "Audit: M6 T5 the build engine -- 25 findings (0 critical, 2 high)": labels `audit`, `punch-list`, milestone M6, a sub-issue of #652 (the parent read back as 652), one checkbox per item. `tools/box-check --issue 837`: 26 open checkboxes, 0 fail.
- `tools/punch-items.py` carries `tracked: "#N"` for the ten, and `05` shows each item's bug issue. `tools/lint-audit-artifacts ... --phase pre-issue`: **PASS**.
- The lane now pauses for the coordinator's stream briefs (plan § 6b stage E).

### [Stage E] 06:20 to 06:32 — E1, `scripts/mkimage` fails closed (PL-01, #827)

- The coordinator's streams E1 to E8 read from `feature/m6-renovation-plan-346:docs/reviews/briefs/t5-streams.md` (`7335583619`), with D-WORKFLOW-193 for E6.
- The test first: `tools/sb-mkimage.sh` runs the real `scripts/mkimage` and `projects/ROCKNIX/bootloader/mkimage`, at a commit or from the working tree, over fixture files. It uses mtools, populatefs and xmlstarlet copied read-only from the M7 SM8550 toolchain, because the host has no mtools. Before (`8ebaf8daad`): `overflow`, `nearfull` and `noabl` each exit 0 with an image and its checksum, `Disk full` or the missing ABL printed. The trace was read first.
- The change (`cfd5ee7324`): every part1 copy in the two branches and all fifteen in the hook, the seven `parted` calls, `mke2fs`, `pigz` and the checksum go through `show_error`. A size check compares the kernel and `SYSTEM` with `SYSTEM_SIZE` before any copy. `remove_partial` runs on an error and on `SIGINT` or `SIGTERM`, and the script ends `exit 0`. `bash -n` passes on both files.
- After: the same three modes exit 1 through the error path with no image; `fit` still builds. Two checks that no working build changes: the M7 SM8550 and H700 images need 75% and 61% of `SYSTEM_SIZE` (2,048 MiB), from their update tars read only; and their recorded image steps show no mtools refusal, so checking the hook's copies changes nothing that works today. RK3326's `stock` and `overlays` sources are in the tree but no RK3326 run is on record (`fix-pending-image`).
- Already written: of 26 recorded M7 image steps, none shows a copy refusal, so no image in the record shipped incomplete.
- Not changed: the `Generic` OVA block (`qemu-img`, `tar`, its checksum; unreached, `PROJECT=ROCKNIX` everywhere) and the hook's `exit 2` on a missing `boot.scr`, which already fails.

PROOF: 06:27-06:30 P15 `scripts/mkimage` exits 1 and leaves no image over a SYSTEM the FAT cannot hold or a missing ABL, where it exited 0 with an image -- `tools/sb-mkimage.sh` (F-16, #827)

### [Stage E] 06:31 to 06:34 — E2, `get_git`'s cache check (PL-02 #828, PL-03 #829)

- The coordinator accepted E1 on #652 (nothing owed).
- The test first: `tools/sb-get-git-head.sh` now lifts `_clean_repo` and `_repo_exists_and_valid` by name, from a commit or the working tree. It runs the check as `main` does, over a clone with `HEAD` at B behind its branch A, and then over the same clone with a tracked file edited. `tools/sb-get-git-pushd.sh` takes `WORKTREE` too.
- Before (`8ebaf8daad`): A accepted with `HEAD` at B; the edited file kept and accepted; P14's fixture left with `.git` alone.
- The change (`6712ae5ef3`): `pushd` and `_clean_repo` are checked on their own lines, and every return pops. `_clean_repo` is now `git clean -fdx && git reset --quiet --hard`. `HEAD` must equal `git rev-parse --verify "${PKG_VERSION}^{commit}"`, and the `ls-remote | grep` pipe is gone. `bash -n` passes.
- After: A refused; B accepted, full and abbreviated; the edit discarded and the cache accepted. P14's fixture comes back intact (`.git .gitignore build.fixture-1 sources untracked-file`), and the trace shows nothing after the refused `pushd`.
- Already written: the shared cache `/workspace/cache/rocknix-sources`, read only. All 311 git clones have `HEAD` equal to the pin in their directory name, so none is corrected by the next fetch. A tree already cleaned by #828 cannot be recovered, and none is known.

PROOF: 06:33 P16 `get_git`'s cache check refuses a clone whose `HEAD` is not the pin and discards tracked edits, where it accepted both -- `tools/sb-get-git-head.sh` (F-18, #829)
PROOF: 06:33 P17 `get_git`'s cache check over a directory it cannot enter leaves the build tree intact, where it ran `git clean -fdx` in it -- `tools/sb-get-git-pushd.sh` (F-25, #828)

### [Stage E] 06:34 to 06:37 — E3, `get_env`'s filter (PL-04, #830)

- The coordinator accepted E2 on #652 (nothing owed).
- The fixture: `tools/sb-get-env.sh` now takes a scratch directory and a commit or `WORKTREE`, and runs over `env -i` with 30 names built at run time. It prints names only, with a verdict of leaked and missing names. Besides the brief's set, it adds `WIFI_PSK`, `app_secret`, `ROCKNIX_GHTOKEN` (Argon G-08) and a carriage-return value. It also checks innocent names that must still pass: `KEYBOARD_LAYOUT`, `XDG_SESSION_TYPE`, `BYPASS_CACHE`, `BUILD_TIMESTAMP`, `OS_VERSION`, `DIRTY`, `SOURCES_DIR` and `TMPDIR`.
- Before: 12 names leaked; a failed write to `/dev/full` with the last name dropped exited 0 (Astra G-06).
- The change: `10f688e3cd`.
- After: none leaked; 15 kept; two notices naming `MULTILINE` and `CRLINE`; the failed write exits 1. `bash -n` passes.
- The `Makefile` recipe, read and unchanged: it removes a leftover `.env` before writing (205), writes 0600 under `set -C` (207), and removes it on exit by `trap` (206).
- Already written: none in the 134 checkouts at stage B.

PROOF: 06:35-06:36 P18 `get_env` forwards no secret-shaped or multi-line name and fails on a failed write, where 12 names leaked and the write failure exited 0 -- `tools/sb-get-env.sh` (F-01, F-02, #830)

### [Stage E] 06:37 to 06:43 — E4, the launch table (PL-05 #831, PL-06 #832)

- The coordinator accepted E3 on #652.
- The test first:
  - `tools/sb-es-cases.sh` runs cases A, B and C.
  - `tools/sb-es-regen5.sh` (new) regenerates the five devices' tables from a tree, with T3's parameters, for a diff between trees.
  - Before: run on an archive of `8ebaf8daad` and on the unchanged tree, whose copied paths had no diff from `8ebaf8daad`.
- Read before the change:
  - All 139 `add_es_system` calls have their fragment.
  - Nothing reads `SYSTEM_WIKI_PATH`, so `arcade` and `segamodel3` are left alone.
  - No caller sets a `SYSTEM_*` key before calling.
  - `SYSTEM_SIZE` and `SYSTEM_PART_START` are image options, kept out of the reset.
  - In today's tables, every system with cores has exactly one default, except GENERIC_X64's `psx`, which has none (T3's finding; its recipe line is #650's S2).
- The change (`cbb3e308b7`):
  - the reset, and a missing fragment refused by name;
  - `core[last()]`;
  - the defaults counted once per system: more than one fails by name, none is a WARNING (see below);
  - `mk_es_systems` failing loudly;
  - the two years.
  - `bash -n` passes.
- Not done as briefed: the brief asked for a count of anything but one to fail. A system with no default warns instead, because failing on it would stop GENERIC_X64's table until S2 gives `psx` a default. Put to the coordinator in the hand-back.
- After: A fails by name, B ships `b2` alone, C gets `runemu.sh`. The five tables differ in the two release lines only.

PROOF: 06:38-06:41 P19 the launch table's cases: two defaults fail by name, a false core first ships one default, an appended system gets the default command -- `tools/sb-es-cases.sh` (F-03, F-04, #831, #832)
PROOF: 06:38-06:41 P20 the five devices' tables after E4 differ from today's in `daphne`'s and `gp32`'s years only -- `tools/sb-es-regen5.sh` (F-03, #831)

### [Stage E] 06:43 to 06:48 — E5, the image path (PL-07 #833; PL-20, PL-24, PL-12, PL-13)

- The coordinator accepted E4. The zero-default case stays a warning here; the coordinator makes it fatal at the integration, after T3's S2, and has put that in the merge notes.
- The test first: `tools/sb-build-distro.sh` lifts `build_distro`'s prune, clean and closing blocks and `scripts/image`'s identity block by their marker lines. It does not run the real `build_distro`, because that enters `tools/watch-build` and its nesting marker is never pre-set. Before (`8ebaf8daad`): the three defects reproduced.
- The changes:
  - `cfb391e75d`, `build_distro`: the prune keeps the frozen identity's outputs, each step fails with its message, the initramfs clean falls back to `DEVICE`, and a failed clean is named.
  - `07b92ce5b7`, `image`: `ORIGIN_URL` and `BUILD_FILENAME` removed; `git grep` finds no reader in the tree, the workflows or the fork's tools.
  - `5f71b30310`, `build_compat`: 58 dead lines removed. The compat root names no file, and `do_mkimage` was never called. `CUSTOM_VERSION`'s export of `OS_VERSION` went with it, and the image step's identity already refuses `CUSTOM_VERSION`.
  - `bash -n` passes on all three.
- The history of `DEVICE_ROOT`: upstream's `Makefile` sets it for RK3566 only too (`f27f9088f6`, the 2025-07-13 import), and no reason is recorded. The fallback keeps RK3566's behaviour.
- After: the refusal fires with the files byte-identical; exit 1 with the message; the stamp removed.
- Already written: an identity already published is immutable (D-WORKFLOW-157). `${BUILD}/BUILD_FILENAME` files remain in old build roots, unread.
- Not in this stream: `.identity.json` is still written before `do_mkimage` (Argon G-02, folded into F-09's item). After E1 a failed `mkimage` removes its image, but the sidecar stays. The brief's files for `scripts/image` were 71 to 84, so it goes to the coordinator in the hand-back.

PROOF: 06:46 P21 `build_distro` keeps a frozen identity's outputs so the image refuses, fails a failed step by name, and cleans the initramfs without `DEVICE_ROOT` -- `tools/sb-build-distro.sh` (F-09, F-14, F-24, #833)

### [Stage E] 06:50 to 06:53 — E5b, the identity sidecar on failure (PL-07, #833)

- The coordinator accepted E5 and authorized E5b on #652: write `.identity.json` only after `do_mkimage` returns 0, or remove it on the failure path. Fixture first; one commit.
- Why not move the write: `tools/build-identity-test` (T14's) lifts the block from `# Record the identity` to `# Create legacy sym links`, so moving the write would break that test. The removal on failure was the option kept.
- Fixture: `tools/sb-image-sidecar.sh`. Before: a failing step leaves the sidecar.
- The change (`0a580b2d4d`): an `EXIT` handler removes the sidecar on a non-zero exit, then calls `onexitcleanup` with the same status; `NOONEXIT` is honoured. `bash -n` passes.
- A slip of mine, caught by the fixture: the first cut called `(exit ${rc}); onexitcleanup`, which under `set -e` exits before the call. Rewritten as `(exit ${rc}) || onexitcleanup`, then rerun.
- After: the sidecar is removed and `onexitcleanup` sees rc=1; success unchanged. `tools/build-identity-test`: 21 passed, 2 failed, the same two checks as stage B (#801).

PROOF: 06:52 P22 `scripts/image` removes its identity sidecar when a later step fails, where it left one naming no image -- `tools/sb-image-sidecar.sh` (F-09, #833)

### [Stage E] 06:53 to 06:58 — E6, fetch and unpack fail closed (PL-08 #834, PL-14, PL-10 #836)

- The coordinator accepted E5b on #652.
- **#834 under D-WORKFLOW-193.** `tools/sb-get-archive.sh` covers four cases with a `wget` shim (P23).
  - Check made before dropping `--no-check-certificate`: the container has a CA store, because every recorded `GET (git)` clones over verified `https`. The flag came with the 2025-07-13 import (`f6010e7b77`); LibreELEC's `curl --fail` verified.
  - `ca91e943fc`: an unhashed recipe is refused before the cache or the network is consulted, naming the package.
  - `b34868cb18`: `update_packages` keeps checksums and refreshes them from a verified fetch, and skips a package with no upstream version (G-12). Read and `bash -n` only; it has never run on the fork.
  - `430abc8f66`: the five archive versions without a checksum gain theirs. A per-branch scan of 1,347 recipes found five versions in four recipes, not the eight my stage-B count said; the correction is in `02` F-19. Each archive was fetched once into scratch over `curl --proto =https --tlsv1.2`. `atf` 2.12.0 and `rkbin` 74213af1 match the shared cache's earlier copies and stamps. `pkgcheck` passes on all four recipes.
  - Ordering: I edited `get_archive` before writing its fixture. The before/after evidence comes from `8ebaf8daad` and the working tree, so it is unaffected.
- **PL-14** (`64bca887c0`): `tools/sb-unpack-glob.sh` now lifts the real block (P24). Two matches die naming both. The zero-match `mkdir` stays, as the brief asks. In M7's three roots the empty build directories are all no-archive packages (`box86` on aarch64, `nspr`, `entware`, `quirks`, `installer`, `heroic`, `lib32`, H700's `u-boot`), so no recorded build meets the new die.
- **#836** (`0c786d298e`): the contained fix, in the recipe. The general one, teaching `calculate_stamp` what `find_file_path` resolves, is not taken: the recipe line covers the one shipped reader, and the broader fix changes stamp logic for every package. P25 runs P12's fixture against the recipe's own lines; `NOONEXIT=yes` was added to it, so sourcing `config/functions` sets no trap.
- **Already written:** archives in the shared cache are unaffected; a cached archive is checked against its new checksum at the next fetch, and two of the five match. The eight devices' roots rebuild `kernel-firmware` once.

PROOF: 06:54 P23 `get_archive` refuses an archive whose recipe has no checksum, cached or not, and no fetch skips TLS verification -- `tools/sb-get-archive.sh` (F-19, #834)
PROOF: 06:56 P24 `unpack` dies naming both entries when two match, where it emptied the package -- `tools/sb-unpack-glob.sh` (F-08)
PROOF: 06:57 P25 `kernel-firmware`'s stamp moves when the device's firmware list changes -- `tools/sb-stamp-device-config.sh` (F-17, #836)

### [Stage E] 06:59 to 07:03 — E7, the host side (PL-09 #835, PL-18)

- The coordinator accepted E6 and recorded the five-not-eight count as D-WORKFLOW-194. The close-out order is as given to T3 on #650.
- **#835** (`6b38804029`): `host_change` runs `sudo` only with `CHECKDEPS_ALLOW_HOST_CHANGES=1`; otherwise it prints the command, and `checkdeps` exits 1 at its end. Read first:
  - the `Dockerfile` already sets the gcc alternative (39, 43) and makes a 777 `/nix` (45), so container builds meet neither branch;
  - the `/nix` preparation came with FEX-emu and Steam (`214b17f900`);
  - this host has no `/nix` and no gcc alternative, so P26's fixture shows both branches with a recording shim and changes nothing.
- **PL-18** (`805b82a97d`):
  - the options mount gets `:ro`;
  - `LOCAL_SSH_KEYS_FILE` is tested with `-f` and `EMULATIONSTATION_SRC` with `-d`, under mount names of their own (Argon G-16, Astra G-07);
  - `docker-image-build` is kept, upstream-carried, with its use written down: nothing calls it, and the mirror is copied by `skopeo` in `fork-mirror-build-container.yml`. A `DOCKER_IMAGE` override is not documented, because the image would then record the pinned digest as its `BUILDER_VERSION`.
  - P27: `make -n` with a scratch `HOME`. No command line was pasted, and the real options file was not read.
- **Already written:**
  - A host `checkdeps` has already changed stays changed. The owner would undo it by hand with `sudo update-alternatives --remove gcc /usr/bin/gcc-12` and `sudo rm -rf /nix`, the latter only if nothing else uses it.
  - Inside the container, `LOCAL_SSH_KEYS_FILE` is still dropped by `get_env`'s `KEYS` word. That was so before E3, so `rocknix`'s `authorized_keys` copy has not run in a Docker build since that filter was written (`d704c9d563`, 2026-09-05). Named for the coordinator; not this stream's.

PROOF: 07:00 P26 `checkdeps` changes the build host only on `CHECKDEPS_ALLOW_HOST_CHANGES=1` and otherwise prints the commands and stops, where it ran four sudo changes unasked -- `tools/sb-checkdeps.sh` (F-20, #835)
PROOF: 07:02 P27 the options mount is read-only and a missing optional path is not mounted, every docker target still resolving -- `tools/sb-make-n.sh` (F-13)
