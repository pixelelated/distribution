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
