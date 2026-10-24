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
- **The refutation** started at 16:03: `timeout 5400 tools/council/run invoke --member gpt --provider openrouter --prompt-file second-opinions/gpt-brief.md --output second-opinions/gpt-audit.md`, in the background.
  - **Watching it:** the harness task `bgsvjury2` delivers its end.
  - **Its silent mode:** a hung call is ended only by the Facilitator's own per-attempt and total timeouts and by the `timeout 5400` around it.
- **`review-plan.json`** is written in T8's shape: depth `independent`, scope `epic`, one reviewer `gpt` (`openai/gpt-6-astra`, lab `openai`, effort `max`, OpenRouter pinned to OpenAI). Its status reads `running` until the seat ends.
