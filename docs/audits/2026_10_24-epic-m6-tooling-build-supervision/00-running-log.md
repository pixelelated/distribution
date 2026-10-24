# Running log — M6.P2 T9, build supervision and host maintenance (#656)

- **Executor:** Opus 5.5 (`claude-opus-5-5`) at high effort, Claude Code, the T5 session (`m6-t5-build-engine`, pane `wN:p7`), session `c649553c-8086-4db7-ad9c-248c7e41ff95`.
- **Brief:** `docs/reviews/briefs/tooling-build-supervision.md` version 2 (`8826d2968d`), dispatched on #656 by the coordinator at 15:41 UTC. Depth Independent: one GPT-6 Astra seat at `max` through the Facilitator at Phase 4.6.
- **Branch:** `feature/m6-tooling-build-supervision-656`, at `cdc45513b0` at stage A, stacked on P1's `2174265e9c`. The coordinator's tip `8826d2968d` was merged in at `2a24aa2063`.
- **The read:** `8ebaf8daad`'s bytes, in the at-hash export `.qa-scratch/t9/at-hash/`. `reviewed-at:` is the branch's `HEAD` at stage A; the branch equals the hash on all 18 paths.
- **Never run here** (brief § 8): a build; `--reclaim-swap`; `--stop-vms`; `host-maintenance/install` or `reclaim-swap` directly; `fork-newdrive`; `fork-publish-release` without `--prepare`; `watch-build` around a real command; a write under `/workspace/repos/rocknix*`.

## [Stage A] 15:42 to 15:46 UTC — scope, the host, the eight controls

**The first commands** (15:42:04; `.qa-scratch/t9/first-commands*.txt`):
- `git fetch origin` and `git fetch upstream --no-tags`: rc 0.
- The branch is `feature/m6-tooling-build-supervision-656` at `cdc45513b0`, `stacked-on-P1`, and `docs/reviews/inventory.json` is present.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` lists exactly the dispatch's eight paths (`device-builds.md`, `engineering-practices.md`, `fork-workflow.md`, `generic-x64-vm-testing.md`, `instruction-files.md`, `code-auditor/references/templates.md`, `council/IMPORTED-FROM.md`, `tools/lint-audit-artifacts`): 127 insertions, 11 deletions.
- `df -i /tmp`: 40% used. `.gitignore`: `:63` `/.qa-scratch/` and `:84` `/.build-runs/`.
- The at-hash export: rc 0, 115 files.
- `tools/rules-check` rc 0 (30 rule files). `tools/register-check` rc 0 (667 IDs). `tools/ceremony-check` rc 1, the W42 weekly summary only: M7's week, not this lane's to pay (brief § 1).

**The host, read before the first test** (15:42:48):
- The host file's last line is the coordinator's 15:04 UTC observation: `swapon --show` reads /swap.img 8G with 8G used, `free -g` 60 total and 46 available, and M6 runs no build and no reclamation.
- The census, `pgrep -c -x qemu-system-x86`: **0**.
- `/tmp/pixelelated-watch-submit-*`: 4 before the controls. `git status --short`: empty.

**Scope** (15:45; § 2's block; `.qa-scratch/t9/scope.txt`):
- 18 paths, 3,795 lines, 201,453 bytes; 18 fork-own; reach `n/a` 18; python 12, shell 3, markdown 3. Equal to the brief.
- None of the 18 is on `upstream/next`. 35 fork commits since `c445081a59`.
- The branch-vs-hash diff over the 18 is empty.

**The eight controls and `hooks-test`**, in this worktree, 15:42:48 to 15:44:28 (`.qa-scratch/t9/controls/`):

| Control | rc | Time | Last line |
| --- | ---: | ---: | --- |
| `tools/host-maintenance/test-swap-reclaim` | 0 | 0.1 s | `OK` |
| `tools/host-maintenance/test-retention-report` | 0 | 6.9 s | `}` (its JSON) |
| `tools/host-maintenance/test-build-admission` | 0 | 17.9 s | `"result": "PASS", "checks": 68` |
| `tools/host-maintenance/test-build-monitor` | 0 | 63.9 s | `36 PASS; 0 FAIL` |
| `docs/qa-logs/2026-10-03-watch-job/test-watch-job.py tools/watch-job` | 0 | 9.4 s | `32 PASS; 0 FAIL` |
| `docs/qa-logs/2026-10-04-watch-progress/test-progress.py <worktree>` | **1** | 0.4 s | `3 PASS; 10 FAIL` |
| `docs/qa-logs/2026-10-04-watch-progress/test-watch-build.py` | **1** | 0.1 s | `AssertionError: shared runner observes nested QA logs and retains terminal result` |
| `docs/qa-logs/2026-10-05-watch-submit/test-submit.py` | **1** | 0.2 s | `AssertionError` (`:42`, from `:49`'s `submit(base / 'success', 0)`) |
| `.githooks/hooks-test` | 0 | 0.7 s | `PASS` |

- After the controls, `git status --short` is still empty. `test-submit.py` left one more `/tmp/pixelelated-watch-submit-*` (4 → 5).

**The three failures, read to their cause.** The brief's cause is the first of two layers.
- **Layer 1, as the brief says.** The three fixtures copy `watch-build` and `watch-job` only (`test-progress.py:39-40`, `test-watch-build.py:56-57`, `test-submit.py:17-18`). `watch-build:50-51` loads `host-maintenance/build-admission` beside itself. The receipts `test-submit.py` left in `/tmp/pixelelated-watch-submit-ebkyj88c/success/` say `[Errno 2] No such file or directory: '.../tools/host-maintenance/build-admission'`.
- **Layer 2, found here.** A diagnostic copy of each control puts the module in its fixture (`.qa-scratch/t9/diag/`, two added lines each, the recorded files untouched). All three still fail: `test-progress` rc 1 (`3 PASS; 10 FAIL`), `test-watch-build` rc 1 (the same assertion), `test-submit` rc 1. The receipts of the diagnostic `test-submit` (`/tmp/pixelelated-watch-submit-jvbeycz8/success/`) show `runner_returncode: 2`, `tool-wrapper.rc` 2, and the console line `watch-build: build admission required; prepare tools/host-maintenance/build-admission first`.
- **The guard behind layer 2.** `watch-build:96-98` (`d7e2d6be41`, 2026-10-13, #493: *build: require current capacity admission before compilation*) refuses any run that carries neither an admission receipt nor `--record-only`. All three controls (2026-10-04 and 2026-10-05) predate it and pass neither. `test-build-monitor` passes because `admission-test-fixture.py` copies the module and `prepare`s a receipt (`test-build-monitor:84`, `PIXELELATED_BUILD_ADMISSION`).
- **So:** three recorded controls stopped running when the admission guard landed, on both its parts. None is in the fork CI (`fork-checks.yml:42-44` runs the other three), so nothing said so. Each diagnostic run left one more `/tmp` directory (5 → 6).

**The record, read only** (15:45:41; `.qa-scratch/t9/record/`):
- 46 `.build-runs/` directories: 45 under `/workspace/repos/rocknix.worktrees/` and the legacy checkout's. Equal to the brief.
- **A delta in what was counted:** 1,902 run directories and 229 loose files (45 `active.lock`, 184 others), 2,131 entries in all, against the brief's 2,022 run ids.
- The largest are `m7-p5-build-20261015-03` (435 entries), `conflict-resolution` (362) and `m7-player-setup` (276).
- Every directory's mtime was recorded in `mtimes-before.txt`. The newest is 2026-10-24T05:40:27Z, before this slice began.

**The at-hash `watch-build`** is sha256 `44a6d87505fd…`. `docs/qa-logs/2026-10-04-watch-progress/source-hashes.json` records `9c15e068…` as its corrected copy, so the recorded control was bound to an older `watch-build`, as the brief says.

PROOF: 15:45 P1 the slice is the brief's 18 paths, 3,795 lines and 201,453 bytes; none upstream's; 35 fork commits; the branch equals the hash on all 18 -- `.qa-scratch/t9/scope.txt`
PROOF: 15:44 P2 the eight controls at the hash in this checkout: five pass, three fail; the three fail on a missing module and then on the admission guard -- `.qa-scratch/t9/controls/`, `.qa-scratch/t9/diag/`, the two `/tmp` receipts

## [Stage B] 15:47 to 15:58 UTC — the reading

- **The 18, read whole at the hash** (`.qa-scratch/t9/at-hash/`): the six tools, `build-admission`, `reclaim-swap`, `install` and `retention-report` line by line; the three guides against the code; the five controls by their test and case names (37 swap tests, 68 admission checks, 36 monitor checks, 32 watcher checks, 19 retention controls).
- **Each refusal matched to a control:** a `grep -l -E` of each refusal's text over the nine controls (`test-build-admission`, `test-build-monitor`, `test-swap-reclaim`, `test-retention-report`, `admission-test-fixture.py`, the four qa-logs controls), read beside the named checks. The unmatched refusals are `04` § Q6's `none` rows.
- **Outside the slice:** the release tool's control is `tools/build-identity-test:104-167`. `--stop-vms` is tested only for refusing to combine with `--reclaim-swap` (`test-swap-reclaim:368-369`).
- **The README's memory-guard-removed control** is in `git grep` only as the 2026-10-04 work log `:241` ("runs the same35 tests and fails exactly2"). The evidence folder `2026-10-04-host-swap-rollout/` holds none.
- **The container's Python:**
  - The pin `sha256:988c0ba5…` is unchanged since `2c349c6d51` (2026-10-01).
  - `device-builds.md:379-380` and the 2026-10-07 work log `:793-794` record that this container runs Python 3.10 without `hashlib.file_digest`.
  - The host has no 3.10 interpreter (`/usr/bin/python3.14` only), and the brief names no container start, so this rests on the record.
- **The record's states:** across all 1,885 `build.status` files, `head -1` gives `finished` 1,885. There are no `runner-error` files. The 17 directories without a status are hand-made folders (16 in `conflict-resolution`, 1 in `m7-browser-memory-570`).
- **Q5 costs:**
  - `build.start` to `admission.json`'s `admitted` over 663 recorded runs: median 0.09 s (0.08 to 0.19).
  - `watch-job`'s `--build-progress` pipeline, run read-only over the largest recorded `build.log` (213,562,360 bytes): 0.50, 0.45 and 0.44 s. Over the SM8550 log (45,743,868 bytes): 0.13 s. Both runs' `watcher.interval` is 5.
- **`/tmp` after the controls and diagnostics:** `pixelelated-watch-submit-*` 6 (4 at the start; one per `test-submit` run). `watch-job-393-*`, `pixelelated-retention-controls-*`, `pixelelated-build-admission*` and `pixelelated-build-monitor*` 0.
- **Written:** `02-forward-audit.md` (F-01 to F-11, P1 to P9, the 18 coverage rows), then `03` and `04`.

PROOF: 15:45 P3 the record: 46 directories, 1,902 runs, every status file `finished`, 17 non-run folders, mtimes recorded before -- `.qa-scratch/t9/record/`
PROOF: 15:52 P4 supervision's cost: admission 0.09 s median over 663 runs; a whole-log progress scan 0.45 s on the largest log and 0.13 s on the SM8550 log, per 5-second interval -- the two commands above
PROOF: 15:53 P5 `hashlib.file_digest` in the admission and retention tools against the pinned container's Python 3.10 -- `build-admission:34`, `retention-report:22`, `device-builds.md:379-380`, the 2026-10-07 work log, `2c349c6d51`
PROOF: 15:50 P6 `test-submit.py` leaves its `mkdtemp` under `/tmp`; the other controls clean up -- the `/tmp` counts
PROOF: 15:51 P7 the refusals with no control, by text search and the named checks -- the grep in this entry
PROOF: 15:54 P8 `build-preflight --stop-vms` stops every `pgrep -f` match by plain `kill`, unowned and unwaited, and can print READY -- `build-preflight:101-123`, `test-swap-reclaim:368-369`
PROOF: 15:52 P9 the memory-guard-removed control ran once and is not retained -- `README.md:99`, the 2026-10-04 work log `:241`

## [Stage C] 16:00 UTC onward — Phase 4.6: the Facilitator, the probe, the packet, the refutation

- **Setup (16:00:11 to 16:00:41):** `npm install --prefix tools/council` rc 0. `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.` `tools/council/run test`: 39/39, 127/127 and 19/19 pass, 0 fail. `run` sources `~/.config/council/env` itself; the env was not read.
- **The probe** (16:01:25 to 16:01:35): `tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-probe-prompt.md --output second-opinions/gpt-probe.md`, rc 0. The provenance reads:
  - declared `openai/gpt-6-astra (OpenRouter, via openai, effort=max)`;
  - observed `openai/gpt-6-astra`, PASS, `model_identity_source: provider_response`;
  - provider OpenAI, PASS;
  - effort `max`, PASS, 302 reasoning tokens.
  - The seat's own line reads `READY unknown`; the provider's field is the authority.
- **The packet** (`tools/t9-packet.py`): `second-opinions/gpt-brief.md`, **295,270 bytes, sha256 `4e15670d1c7b8b46f23ee5e8f64d2cd9a7c6959de368f9ef540a936077bc7967`**, 41 parts. `second-opinions/packet-manifest.json` names each part with its sha256, and the 18 files and the six entry-line files with their own `file_sha256`.
  - **What it carries:** the ask, with `reclaim-swap`, `install` and `build-admission` first; `02`, `03` and `04` whole; the 18 files whole and line-numbered; the context of the seven entry lines (`Makefile:30-50` and `:170-212`, the five scripts' heads, `fork-checks.yml:30-50`); the controls' summary, the two-layer receipts, and the record and cost figures.
  - **Checks before sending:** the hook's secret patterns 0 hits; `forbidden-terms-check --stdin` rc 0; under the 440,000-byte cap.
- **The refutation** started at 16:02:33 (the log's `start` line): `timeout 5400 tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-brief.md --output second-opinions/gpt-audit.md`, in the background.
  - **Watching it:** the harness task `bgsvjury2` delivers its end.
  - **Its silent mode:** a hung call is ended only by the Facilitator's own per-attempt and total timeouts and by the `timeout 5400` around it.
- **`review-plan.json`** is written in T8's shape: depth `independent`, scope `epic`, one reviewer `gpt` (`openai/gpt-6-astra`, lab `openai`, effort `max`, OpenRouter pinned to OpenAI). Its status reads `running` until the seat ends.
- **The refutation ended at 16:22:33, rc 0.**
  - One attempt, http 200, `model=openai/gpt-6-astra`, `providers=["OpenAI"]`, effort `max`.
  - 44,956 reasoning tokens, 51,800 completion tokens, 1,200 s, USD 3.59458, `outcome=success`.
  - `final.verification`: PASS (observed `openai/gpt-6-astra`, `provider_response`); provider PASS; effort PASS.
  - The provenance's `user_prompt_sha256` equals the packet's `4e15670d…`. The output is `second-opinions/gpt-audit.md`, 30,928 bytes.

## [Stage C] 16:23 to 16:40 UTC — the second opinion graded

- **Read at their sites before grading:**
  - Rows 14, 16, 29 and 31's controls (`test-build-monitor:188-196`, `:215-228`; `test-build-admission:28-32`, `:55-60`, `:80-84`).
  - `test-retention-report:35-44` (G-46) and `scripts/build:5-10` (G-16).
  - Both clones' `.git` devices (G-12): 66304 and 66304. The `rocknix` registry is present and the `distribution` one absent.
- **F-01's history** (the seat asked): exports of `d7e2d6be41^` (`e198f0fc3b`) and `d7e2d6be41` under `/workspace/tmp/m6-t9/hist-*` (`df -i` 21%).
  - At `e198f0fc3b`: `test-progress.py` rc 0 `13 PASS; 0 FAIL`; `test-watch-build.py` rc 0 `35 PASS; 0 FAIL`; `test-submit.py` rc 0.
  - At `d7e2d6be41`: all three rc 1.
  - A first pass printed `rc 0` for all six because `$?` was read after a command substitution inside `printf`'s arguments. The second pass captured each exit first, and those are the exits recorded.
  - `/tmp/pixelelated-watch-submit-*` went 6 → 10: passing runs leak too.
- **The record's outcomes:** rc 0 1,470; rc 1 397; rc 2 10; rc 125 4; rc 143 3; rc 137, 130 and 127 one each.
- **Graded in `04` § Second opinion,** all 55 items:
  - **Confirmed, into findings:** G-03, G-06, G-08 (narrowed to Medium), G-10, G-11, G-12, G-17, G-22, G-26, G-27, G-28, G-29, G-30, G-33, G-34, G-36, G-37, G-38, G-40, G-41, G-45, G-46, G-47, G-48, G-49 to G-53, G-55.
  - **Narrowed to F-21's leads:** G-13 to G-19, G-21, G-25, G-42 to G-44. G-54 is a lead in F-20.
  - **Withdrawn or no item, each with its reason:** G-01, G-02, G-04, G-05, G-07, G-09, G-20, G-23, G-24, G-31, G-32, G-35, G-39.
- **The refutations accepted:**
  - F-04, F-07, F-08 and F-10 re-graded Medium; F-05 broadened; F-06's escape made precise.
  - F-11 withdrawn: the boundary test is the retained control.
  - F-01's history proved (P10).
  - Five guard-table rows corrected (14, 16, 29, 31, 59), ten rows added (64 to 73), and row 51 corrected.
- **My statements corrected:**
  - `03` § 3.2 said no control touches real Docker; `test-retention-report` does (G-46).
  - `03` § 3.5 said the 900 s window covers the scan; it starts after it (G-41).
  - `02`'s install row said the `assert` is safe because `-O` is never passed; an administrator can pass it (G-11).
- **New findings:** F-12 to F-21.

PROOF: 16:30 P10 the three controls pass at `d7e2d6be41^` and fail at `d7e2d6be41` -- `/workspace/tmp/m6-t9/hist-*`
PROOF: 16:28 P11 the record's 1,885 outcomes: rc 0 1,470, rc 1 397, and the rest -- the outcome lines of every `build.status`
PROOF: 16:28 P12 two clones' admission registries on one volume (device 66304) -- `stat` and `test -d` of both `.git`
- **Written:** `05` from `tools/punch-items.py` (21 items: 8 Medium, 13 Low, PL-11 withdrawn). `review-plan.json` complete. `tools/lint-audit-artifacts --phase pre-issue`: `PASS pre-issue artifacts`, with `review plan: independent, 2 model perspectives, 1 verified external calls`.

## [Stage D] 16:33 to 16:36 UTC — the bugs, the audit issue, the pause

- **Eleven `bug`s, milestone M6** (16:34:03), each with its trace, its VM line, criteria an agent can tick and `Already written:`:
  - #913: F-01, with F-02 and F-15;
  - #914: F-03, with G-47 and G-48;
  - #915: F-04;
  - #916: F-05, with F-18;
  - #917: F-06;
  - #918: F-07;
  - #919: F-12;
  - #920: F-14;
  - #921: F-16;
  - #922: F-17;
  - #923: F-19.
  - `tools/box-check --issue N`: 0 fail on each.
- **The audit issue #924**, `Audit: M6 T9 build supervision and host maintenance -- 21 findings (0 critical, 0 high, 8 medium, 13 low)`, labels `audit` and `punch-list`, milestone M6, attached as a sub-issue of #656. One checkbox per item; `box-check` 0 fail.
- **For the coordinator at this pause:**
  - the stream briefs;
  - the leads PL-13 (the installer, D-INFRA-015), PL-20, PL-21, and PL-03's, PL-10's and PL-12's contract choices;
  - #640's row PL-09.
- **The lane pauses here** for the coordinator's stream briefs (brief § 8). No file under `tools/` has changed on this lane: `git diff --stat cdc45513b0 HEAD -- tools` is empty, and the 18 equal the hash.
- **A correction to the line above as first committed** (`bb1478835c`). It said `git diff --stat 8ebaf8daad HEAD -- tools` is empty. That command prints **15 files changed, 2130 insertions, 8 deletions**, all inherited before stage A in `8ebaf8daad..cdc45513b0`: P1's `renovation-inventory`, `renovation-drift` and `renovation-status`, the coordinator's `lint-audit-artifacts` and `register-check`, and the lint's two fixtures. None is one of the 18. Criterion 15's command therefore cannot read empty on a branch stacked on P1; the delta is put to the coordinator.

## [Stage E] 16:48 UTC onward — the streams (`t9-streams.md` at `4c842e2485`)

- **Read first:** the coordinator's 16:48 dispatch on #656 and `t9-streams.md` whole (`/workspace/tmp/m6-t9/t9-streams.md`). The host file's last lines: the coordinator's 16:40 grant to M7 of a bounded VM window. Census 0 at 16:49:17.
- **Moved:** the lane's 28 stage-D drafts, messages and logs, from `/workspace/tmp/m6-t8/` to `/workspace/tmp/m6-t9/`.

### S1 (#913; PL-01, PL-02, PL-15), 16:50 to 16:57

- **Test first:**
  - The progress control at the stage-D tip: rc 1, `3 PASS; 10 FAIL`, its first run at 16:51 being an Edit refused for want of a Read, so the file was unchanged.
  - The stage-A exits of all three, and the stage-A diagnostic copies (module added, no receipt): rc 1, the receipt `watch-build: build admission required`.
- **The fix**, test files only (`9b071c5d12`):
  - **`test-progress.py`:** each case's root gains `scripts/README` and a `Makefile`, and `prepare_fixture` gives it a receipt. The four build-shaped cases carry it; `generic-qa` runs `--record-only`.
  - **The 2026-10-04 `test-watch-build.py`:** the helper is loaded from its own repository (`parents[3]`), and each fixture prepares a receipt. The cold-root case declares its redirected `BUILD_DIR` as an output, with a fresh receipt, as `test-build-monitor:249-255` does. The untouched historical original is `docs/qa-logs/2026-10-03-watch-job/test-watch-build.py`.
  - **`test-submit.py`:** an admitted fixture root, a receipt prepared just before each launch (an admission binds the registry generation), and `atexit` removing the root.
- **At the fix:**
  - `test-progress.py`: rc 0, `13 PASS; 0 FAIL`, 5.9 s.
  - `test-watch-build.py`: rc 0, `35 PASS; 0 FAIL`, 58.8 s. The first fixed run stopped at 33 on the cold-root case, until its `BUILD_DIR` was declared.
  - `test-submit.py`: rc 0, its four rows; `/tmp/pixelelated-watch-submit-*` 10 before and 10 after.
- **The positives** (`.qa-scratch/t9/positives/`, each fixed control with its admission step removed): `test-progress.py` rc 1 `5 PASS; 8 FAIL`, `test-watch-build.py` rc 1, `test-submit.py` rc 1. `/tmp` was still 10 after.
- **The retention control** (`a9bd346d54`):
  - Its `/proc` root and `docker` are injected; the live-owner case copies its real process's `cmdline` once the child has exec'd. A new case, "a live QEMU holds every candidate", was added.
  - The first sleeper run found that race in my own edit: "actual live owner process" read eligible, because `/proc/<pid>/cmdline` was read before the child exec'd. The wait was added.
  - After the fix: three runs rc 0 (20 controls, 4 eligible). Beside a sleeper renamed `qemu-system-x86_64` (`comm` `sleep`; `pgrep -c -x qemu-system-x86` 0), the unchanged control gives rc 1 (`AssertionError: ('eligible independent completed QA disk', ...)`) and the fixed one rc 0. The sleeper was killed by its PID (`.qa-scratch/t9/s1-retention-sleeper.sh`).
- **A slip in my first sleeper command:** `a && b && bash -c '...' &` backgrounded the whole chain, so the following commands ran with `P` empty. They wrote nothing (`/with-sleeper.log: Permission denied`; `/test-retention-report` absent). The orphaned renamed `sleep` (pid 3312321, ppid 1) was found by its exact `cmdline` and killed by PID after its `comm` and `argv` were checked. The proof was rerun from a script.
- **`/tmp`:** the six directories this lane's runs left (15:44:27, 15:45:10, 16:26:18, 16:26:22, 16:27:41, 16:27:44) were removed by literal path. The other four stay: 2026-10-05T07:42:06Z, 2026-10-24T14:58:26Z, 14:59:15Z and 15:22:36Z, each made before this lane ran a control.
- **Guard-table rows closed:** 12 (progress) and 27, 65 (the launcher's owner refusals) now have running controls. Row 59 is host-isolated, with the new QEMU case beside it. The CI clause is #657's.

PROOF: 16:57 P13 S1: the three controls pass at the fix and their removed-admission copies fail; the retention control passes beside a live process named qemu-system-x86_64 where the unchanged one fails -- `.qa-scratch/t9/s1-*.log`, `.qa-scratch/t9/positives/`

### S2 (#914; PL-03, D-INFRA-028), 16:57 to 17:00

- **Test first:** a new control, `tools/host-maintenance/test-build-preflight` (8 cases). It uses PATH doubles for `pgrep`, `ps` and `free`; the only guest it can see is its own sleeper, whose argv[0] is `qemu-system-x86_64`. No real guest, swap or sudo is touched, and the unfixed tool's `--stop-vms` was run only against that double, never on the host.
- **Against the unfixed tool** (`.qa-scratch/t9/positives/preflight-unfixed/`):
  - the control gives rc 1, `AssertionError: --stop-vms leaves a listed guest running`, because the unfixed tool stopped the control's own sleeper;
  - with `pgrep` exiting 3 it gives rc 0 and `READY`;
  - at 200 MB free of 1001 MB of swap it gives rc 0 and no exhaustion.
- **The fix** (`c9e38e2939`): `tools/build-preflight` stops nothing.
  - Each guest is listed with `its owner stops it with: tools/vm-stop <pidfile> <disk>`, read from the guest's own command line.
  - `--stop-vms` says it stops nothing, and the verdict stays nonzero.
  - A `pgrep` exit of 2 or more is `ERROR: cannot census guests`, with exit 1.
  - Exhaustion is `free * 5 < total`, as `reclaim-swap` counts it.
- **The rules** (`c4d4c147d0`): `device-builds.md` and `generic-x64-vm-testing.md`, the two sentences S2 names.
- **At the fix:** rc 0, `8 PASS; 0 FAIL` (`.qa-scratch/t9/s2-control-fixed.log`). `test-swap-reclaim` 37 OK; `tools/rules-check` rc 0.

PROOF: 17:00 P14 S2: test-build-preflight passes at the fix and fails against the unfixed tool, which stopped the control's own sleeper, said READY over a failed census and missed the helper's boundary -- `.qa-scratch/t9/s2-control-fixed.log`, `.qa-scratch/t9/positives/preflight-unfixed/`

### S4 (#916; PL-05, PL-18), 17:00 to 17:05

- **Test first:** four cases added to `docs/qa-logs/2026-10-03-watch-job/test-watch-job.py`, before the help case:
  - `--pid 1`, a live process this user cannot signal, must read `alive=yes` in `running`;
  - `--pattern --help` must give the progress `--help`;
  - a status named `-status`, with relative paths, must be published;
  - a `build.status.pid` symlinked to `build.log` must be refused with rc 2, leaving the log intact.
- **The EPERM input is PID 1**, because `unshare -Upf --mount-proc` is refused on this host (`Permission denied`). A PID that another namespace hides still reads as exited after the fix (#506); the fix's comment names that limit.
- **Against the unfixed tool** (`.qa-scratch/t9/positives/watch-job-unfixed/`), each case alone:
  - case 1: `AssertionError: expected running: state: died`;
  - cases 2 to 4: each fails on its own label.
  - The full control gives rc 1.
- **The fix** (`4a22ed0b41`):
  - `job_identity` reads `/proc` only. It returns alive with the start time; exited, for absent, zombie or dead; or unreadable, which is an observation error rather than a death.
  - The pattern reaches `grep` after `-e`, and every path comes after `--`.
  - The derived outputs `.tmp`, `.pid` and `.err` are resolved and checked against the inputs, beside the status itself.
- **At the fix:** rc 0, `36 PASS; 0 FAIL`, 9.7 s (`.qa-scratch/t9/s4-watch-job-fixed.log`).

PROOF: 17:05 P15 S4: test-watch-job passes at the fix with four new cases, each of which fails alone against the unfixed tool -- `.qa-scratch/t9/s4-watch-job-fixed.log`, `.qa-scratch/t9/positives/watch-job-unfixed/`

### S3 (#915; PL-04), 17:07 to 17:13

- **The probe first** (`.qa-scratch/t9/s3/probe-before.log`), on the host:
  - **A changed plan:** rc 125, no payload, and the run's `build.log` says `watch-build: command launch/output failed: admission plan changed`.
  - **An unreadable plan:** rc 125, `[Errno 13] Permission denied`.
  - **The host interpreter with `hashlib.file_digest` deleted** (3.10's hashlib on 3.14): rc 1, and a traceback ending `AttributeError: module 'hashlib' has no attribute 'file_digest'`, raised from `admit` at `build-admission:180`.
- **Test first:** two cases in `test-build-admission`.
  - **"A registry that is not an object is a refusal, not a traceback":** `jobs.json` holds `[]`, `data.get` raises `AttributeError`, and the unfixed `watch-build`'s tuples let it out.
  - **"A hashlib without file_digest (3.10) admits and hashes":** the same deletion as the probe, through `runpy`.
  - Against the unfixed tools, each fails on its own label (`control-unfixed.log`; `control-unfixed-case2.log`, run from a copy with case 1 removed and deleted after).
- **The fix** (`6a25254359`):
  - `digest` in both tools streams 1 MiB blocks into `hashlib.sha256()`, as #492 did. `retention-report`'s archive member uses the same `stream_digest`.
  - `watch-build`'s two except tuples add `LookupError` and `AttributeError`. No other line of `watch-build` changed (S5's file).
- **At the fix:**
  - `test-build-admission`: rc 0, 70 checks.
  - `test-retention-report`: rc 0, 20 controls.
  - `test-build-monitor`: rc 0, `36 PASS; 0 FAIL`.
  - `test-progress.py`: rc 0, `13 PASS; 0 FAIL`.
  - The 2026-10-04 `test-watch-build.py`: rc 0, `35 PASS; 0 FAIL`.
- **The 3.10 proof.** The pinned image is local, as `ghcr.io/rocknix/rocknix-build:latest` with the repo digest `sha256:988c0ba5…` (`Makefile:138`).
  - The census was qemu 0, and the start was posted on the host file at 17:12:32Z.
  - **The one start:** `docker run --rm --network none --pull never -v /workspace/tmp/m6-t9/s3/container-fixture:/f:ro ghcr.io/rocknix/rocknix-build@sha256:988c0ba5… python3 -I /f/probe.py`, rc 0, Python 3.10.12 with no `file_digest`.
  - **The fixture:** a 3,145,731-byte random payload and a 6-byte file.
  - **What it shows:** the fixed `build-admission` and `retention-report` give `63603ed4…a2a9f5` and `4c47b3e8…28e8f`, equal to `sha256sum` and to the host 3.14.4. The unfixed copies raise `AttributeError` there. The completion is on the host file; no container of that image is left.
- **Two departures from the stream's shape, for the coordinator:**
  - **The refusal is rc 125, not rc 2.** A refusal inside `admit` is caught by the run's own tuple (`watch-build:164` → `:190`): rc 125, the payload not started, the reason recorded in the run's `build.log` as `watch-build: command launch/output failed: <reason>`, and nothing on stderr but the recording line. rc 2 with `watch-build: <reason>` on stderr belongs to failures before the run directory exists (`:221`). Calling an admission refusal "command launch/output failed", without saying it on stderr, is in S5's region of `watch-build`; it is left to S5 or the coordinator.
  - **`grep -rn 'file_digest(' tools/` prints one line: `tools/ceremony-check:113`.** It is outside S3's files, and it runs on the host only (the pre-push guard and the fork CI). It is left and named. The two comments and the test's deletion name `file_digest` without a call.

PROOF: 17:13 P16 S3: under the pinned 3.10.12 the fixed tools' hashes equal sha256sum's and 3.14's while the unfixed raise AttributeError; test-build-admission's two new cases pass at the fix and fail against the unfixed tools -- `.qa-scratch/t9/s3/`

### S5 (#917, #918; PL-06, PL-07), 17:14 to 17:34

- **Test first:** six cases in `tools/host-maintenance/test-build-monitor`.
  - **Lock control, rewritten:** its second launch carries a fresh admission (`fresh()`), so the refusal it sees is the lock's. It also asserts the stderr `another monitored build owns this worktree`.
  - **A runner killed with its command alive:** a second admitted launch in the same worktree must be refused (#918).
  - **A watcher that ignores SIGTERM:** the runner must still record `runner-error` and `runner-result.json`, rc 125, and the watcher must be gone.
  - **A log the runner cannot write:** `RLIMIT_FSIZE` of 200,000 bytes, with a payload writing 400 KB and then sleeping. The payload must not outlive the runner.
  - **A SIGTERM while admission runs:** a `git` double on PATH marks entry and then sleeps 2 s. The run must end rc 143, with no `command.pid` and no payload.
  - **A console pipe that is never read,** against a 1 MiB payload: rc 0, and the log holds all 1,048,576 bytes.
- **Against the unfixed runner** (an export of `6779d487f0` at `/workspace/tmp/m6-t9/s5-unfixed-root`, through a copy of the control whose `check` prints FAIL and goes on; `.qa-scratch/t9/positives/s5/unfixed.log`):
  - the lock control passes there, as it should with the lock intact;
  - the five new cases fail: four `FAIL:` lines, and the console case by `TimeoutExpired` after 30 s, the runner stuck on the console.
  - The stubborn-watcher case's first unfixed result was invalid. Its fixture replaced the tracked `watch-job` after the admission was measured, so `admit` refused (`command_rc` 125). The case now prepares its admission after the double is written. Standalone against the unfixed runner (`unfixed-stubborn-standalone.log`): rc 2 with `timed out after 5 seconds`, no `runner-error`, no `runner-result.json`, and the double left running. It exited by itself once its directory was removed (pid 3546549, gone when checked).
- **The signal case, standalone** (`signal-standalone.log`): the unfixed runner gives `rc 143 command.pid True payload-started False` (the command was started, then signalled); the fixed one gives `rc 143 command.pid False`.
- **The lock's positive:** the fixed runner with its `flock` removed (`/workspace/tmp/m6-t9/s5-nolock-root`) fails the lock control, `FAIL: one top-level build per worktree` and then `expected one outer run; got 2` (`nolock.log`).
- **The fixes:**
  - **`dce53bf0ba` (#917):**
    - the second `monitor.wait` timeout kills the watcher and records the finish;
    - the output loop's failure handler stops the payload before it writes its note, and that write is guarded;
    - `interrupted` is checked between `admit` and `Popen`;
    - `console_write` selects for 2 s and writes 4 KiB at a time; a stalled or closed console is dropped, with a `console-dropped` note in the run.
  - **`d1a1495bc5` (#918):** the command inherits the lock descriptor (`pass_fds`).
- **The lock mechanism, and why:** the kernel holds an flock while any process holds its open file description, so exclusion lasts as long as the command, with no PID to reuse. The other choice, a refusal while an earlier run's `command.pid` group is alive, would need a start-identity check against PID reuse, and it would be a second code path. The detached watcher is not given the descriptor. Nested `--entry` runs take the inherited-run path, which never locks.
- **At the fix:**
  - `test-build-monitor`: rc 0, `41 PASS; 0 FAIL`; at `dce53bf0ba` alone, 40 PASS.
  - `test-build-admission`: rc 0, 70 checks.
  - `test-progress.py`: 13 PASS.
  - The 2026-10-04 `test-watch-build.py`: 35 PASS.
  - `test-submit.py`: rc 0, with `/tmp/pixelelated-watch-submit-*` at 1 before and 1 after.
- **Left for the coordinator (S3's note):** an admission refusal is still logged as `command launch/output failed: <reason>`, rc 125, and says nothing on stderr but the recording line. This stream's brief did not name it, and it is unchanged.

PROOF: 17:34 P17 S5: test-build-monitor passes at the fix (41/0); its five new cases fail against the unfixed runner and its lock control fails against a runner without its lock -- `.qa-scratch/t9/s5-monitor-fixed.log`, `.qa-scratch/t9/positives/s5/`

### S6 (#919, #921, #920; PL-12, PL-16, PL-14; D-INFRA-029), 17:35 to 17:50

- **The registry's place, chosen:** `${XDG_STATE_HOME:-~/.local/state}/pixelelated/build-admission/<dev>-<fsid>/`, keyed by the measured volume's `st_dev` and `f_fsid`.
  - **Why the state directory and not the volume:** a registry on the volume would have to sit at the filesystem's mount root, or two plans naming two paths on one filesystem would get two registries again. The user may not be able to write a mount root, and a fixture under `/tmp` would point at `/tmp` or `/`.
  - **What the state directory gives:** it is the user's own, at mode 0700, as `registry()` already demands (owner == uid). It is in no clone's `.git`, and it takes no write on the volume.
  - **What it costs:** another user on the same volume keeps a separate registry, and a device renumbered by a reboot starts a new one. Both are written in `build-admission.md`.
- **Test isolation.** The registry moving out of each fixture's `.git` would have put every control's in-process `prepare` into the real `~/.local/state`, and its subprocesses' registries under their `HOME`.
  - `admission-test-fixture.py` binds each loaded module's `state_home` to `<fixture root>/.admission-state`.
  - The five controls pass that directory to their subprocesses as `XDG_STATE_HOME`: `test-build-admission`, `test-build-monitor`, `test-progress.py`, the 2026-10-04 `test-watch-build.py`, and `test-submit.py`. The last three are S1's files, changed by one line each.
  - `~/.local/state/pixelelated` does not exist after every run.
  - A shared per-run registry was rejected: `test-build-admission`'s injected 10^18 reservation would refuse every later fixture.
- **The cases and their unfixed runs** (`.qa-scratch/t9/positives/s6/`):
  - **#919, two clones in one state directory, `statvfs` faked to 1.5 MiB free:** at the fix, clone B's `prepare` is refused `insufficient space after existing reservations` by clone A's unconsumed 1 MiB, and the same `prepare` in another state directory succeeds. Against the unfixed tools it fails on its own label (`919-unfixed.log`), because each clone's registry is its own `.git`'s.
  - **#921, an `admission.json` whose `runner_pid` is a different exited PID:** refused `registry admission identity differs`, with no receipt written.
  - **#921, a registry commit that fails once (an injected `OSError` on `jobs.json`):** the retry reaches `consumed`, and the receipt equals the registry row. Against the unfixed `consume` (an export of `e03fc7982d`), both #921 cases fail (`921-unfixed.log`).
  - **#920, three cases, each run alone against the unfixed report** (`920-case1..3-unfixed.log`):
    - no `observation_start` (`AssertionError: None`);
    - a plan whose `volume` is `/dev/shm` counts 200,704 bytes of a candidate on `/tmp`;
    - a plan edited during the scan (a shim edits the plan on the first `statvfs`, with `docker` stubbed to empty): the unfixed report binds the edited file's hash, `903c045c…`.
- **The fixes:**
  - **`e03fc7982d` (#919):** `registry_for(volume)`; recovery checks the registry against the row's `volume`.
  - **`e8828c13ad` (#921):** the whole row is compared, and the registry is committed before the receipt, with a retry reconciling the receipt.
  - **`82840dbc42` (#920):** the plan's bytes are read once and hashed; `observation_start` is stamped, and the admission window runs from it; reclaim counts only candidates on the volume. The fixture report carries `observation_start`.
- **At the fix** (`82840dbc42`):
  - `test-build-admission`: rc 0, 73 checks.
  - `test-retention-report`: rc 0, 23 controls.
  - `test-build-monitor`: 41 PASS.
  - `test-progress.py`: 13 PASS.
  - `test-watch-build.py`: 35 PASS.
  - `test-submit.py`: rc 0.
- **Already written, read from the record** (read only; counts printed only; `.qa-scratch/t9/s6-record-rows.txt`): the 46 stage-B run directories hold 665 `admission.json` rows, one more than stage B's 664, in one registry, M7's `/workspace/repos/rocknix/.git/pixelelated-build-admission/`.
  - All 665 equal their registry row (state aside), and all 665 have a consumed receipt equal to that row.
  - So the fixed `consume` reads every recorded run unchanged: it opens `row['registry']`, the stored path, which is the old registry for those runs.
  - New admissions use the new registry. M7's stays the record of its reservations, as D-INFRA-029 says.
- **A departure:** the stream says earlier retention reports "stay valid for their 900 s". They do not: a report without `observation_start` is refused by the fixed admission. It is refused in any case, because a report binds `retention-report`'s hash, and that changed in `82840dbc42`. A report prepared before this commit must be remade.
- **A slip of mine:** to stop my slow record glob, I ran `kill $(pgrep -f 's6-record-rows.py')`. The pattern also matched the shell issuing it, which died (exit 144). This broke the rule to kill by PID, never by pattern (`engineering-practices.md`, blindspot: self-matching pattern). The glob's task ended, `failed`. Afterwards, nothing with that name was running (`ps` read by a fixed string), and the background control run was unaffected; it completed rc 0. The count was rerun from the stage-B list.
- **Q7, the docs against the diff:** `build-admission.md` (where the registry lives and why; consume's whole-row check and commit order; the window from `observation_start`) and `retention-report.md` (plan bytes, `observation_start`, reclaim on the volume), each re-read against `e03fc7982d..82840dbc42`. `git grep` for the old location outside `docs/audits` and `docs/work-logs` finds only historical QA records and my own sentence naming the earlier registry.

PROOF: 17:50 P18 S6: the six cases pass at the fix and each fails against the unfixed tools; the record's 665 rows equal their registry rows and receipts -- `.qa-scratch/t9/positives/s6/`, `.qa-scratch/t9/s6-*.log`, `.qa-scratch/t9/s6-record-rows.txt`
