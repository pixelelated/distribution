# Forward audit — M6.P2 T9, build supervision and host maintenance (#656)

Read at `8ebaf8daad` (the export `.qa-scratch/t9/at-hash/`); every line number below is that tree's. `reviewed-at` is `cdc45513b0`, equal to the hash on all 18.

## Phase 2: #656's checklist at stage B

| # | Criterion (brief § 7, shortened) | State at stage B | Artifact |
| --- | --- | --- | --- |
| 1 | The audit folder holds `00` and `01` to `05` | `00` to `04` written; `05` at stage D | this folder |
| 2 | The lint passes, the renovation face included | run before stage D (`--phase pre-issue`) and at close | `04` § Renovation face |
| 3 | `review-plan.json` and the seat's provenance | stage C | `second-opinions/` |
| 4 | Every punch item at a Phase 7 outcome | stage D onward | `05`, the audit issue |
| 5 | `reviewed-at` and `fixed-at` on #656 | `reviewed-at` `cdc45513b0`; `fixed-at` at stage H | #656's body |
| 6 | `01` § Scope: hash, filter output, provenance, branch diff | done | `01` § Scope |
| 7 | One coverage row per path, 18 | done | § Coverage table |
| 8 | § The controls: all eight, exits, *a FAIL would mean*; the three failures as findings | done; the cause is two layers, not one | § The controls, F-01 |
| 9 | § The record: the `.build-runs/` listing, what the status files said, mtimes before and after | done; the after read is at stage F | § The record |
| 10 | `00` records the host line and census first; no forbidden command | done | `00` § Stage A |
| 11 | `04` Q6: the guard table, every `none` a punch item | done | `04` § Q6 |
| 12 | `04` Q1: the two legacy rows, deferred to #640 | done | `04` § Q1 |
| 13 | `04` Q7: the three guides read against the code; the sudoers policy quoted | done | `04` § Q7 |
| 14 | Every proof carries its class cell, equal in count to `00`'s `PROOF:` lines | kept equal at each commit | § Proofs |
| 15 | No file under `tools/` changed before a stream brief | `git diff --stat 8ebaf8daad HEAD -- tools`: empty | § Mechanical checks |
| 16 | The retro | stage G | `docs/retros/` |
| 17 | The six checkers' exits | stage H | the hand-back |

## Mechanical checks

| Check | Command | Exit | Summary |
| --- | --- | ---: | --- |
| Membership | brief § 2's Python block over `docs/reviews/inventory.json` | 0 | `paths 18 lines 3795 {'fork-own': 18} {'n/a': 18}`; python 12, shell 3, markdown 3 |
| Line and byte counts | `git show 8ebaf8daad:<path> \| wc -l` and `wc -c`, summed | 0 | 3,795 lines; 201,453 bytes |
| Provenance | `git cat-file -e upstream/next:<path>` for each; `git log c445081a59..8ebaf8daad -- <the 18>` | 0 | 0 of 18 upstream; 35 fork commits |
| Branch against hash | `xargs -0 git diff --stat 8ebaf8daad HEAD -- <the 18>` | 0 | empty |
| No tool changed | `git diff --stat 8ebaf8daad HEAD -- tools` | 0 | empty at stage B |
| The rules in the worktree | `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` | 0 | exactly the dispatch's eight paths |
| The checkers at stage A | `tools/rules-check`, `tools/register-check`, `tools/ceremony-check` | 0, 0, 1 | `ceremony-check`: the W42 summary only, M7's week |
| Version-sensitive Python | `grep -n -E 'file_digest\|removeprefix\|strict=\|match ...'` over the 12 Python files | 0 | `hashlib.file_digest` at `build-admission:34`, `retention-report:22`, `:69` (3.11 and later); nothing else past 3.9 |
| npm consumers | `git ls-files \| grep -E '(^\|/)package\.json$'` | 0 | `tools/council/package.json` alone |
| Controls named for each refusal | `grep -l -E '<refusal text>'` over the nine controls (`00`; § The controls) | 0 | the unmatched refusals are `04` § Q6's `none` rows |

## The controls

Run at stage A (15:42:48 to 15:44:28 UTC) in this worktree, after the host file and the census; logs under `.qa-scratch/t9/controls/`.

| Control | Exit | Summary | A FAIL would mean |
| --- | ---: | --- | --- |
| `python3 -I tools/host-maintenance/test-swap-reclaim` | 0 | `OK`, 37 tests | a swap guard (ownership, mode, priority, busy, memory, lock, reactivation), the preflight's opt-in path, or the installer's policy and rollback had regressed against its doubles |
| `python3 -I tools/host-maintenance/test-retention-report` | 0 | `"result": "PASS"`, 19 controls | a retention refusal (dependency, process, identity, evidence, fixture) no longer held a disk it should hold |
| `python3 -I tools/host-maintenance/test-build-admission` | 0 | `"result": "PASS"`, 68 checks | a payload could start without a current, unused, fitting admission, or a run could be consumed or recovered on the wrong evidence |
| `python3 -I tools/host-maintenance/test-build-monitor` | 0 | `36 PASS; 0 FAIL` | an entry line no longer enters the runner, a run's result could be green without a watcher, or two top-level builds could share a worktree |
| `python3 -I docs/qa-logs/2026-10-03-watch-job/test-watch-job.py tools/watch-job` | 0 | `32 PASS; 0 FAIL` | the status file could say `running` over a dead, stalled or zombie job, or accept a non-exit-code result |
| `python3 -I docs/qa-logs/2026-10-04-watch-progress/test-progress.py <worktree>` | **1** | `3 PASS; 10 FAIL` | overall progress could read a package's Ninja counter as the build's (blindspot 73); **failing at the hash, so this guard has no running control** (F-01) |
| `python3 -I docs/qa-logs/2026-10-04-watch-progress/test-watch-build.py` | **1** | `AssertionError: shared runner observes nested QA logs and retains terminal result` | the 2026-10-04 routing fixture; **failing at the hash** (F-01); `test-build-monitor` now carries the current routing checks |
| `python3 -I docs/qa-logs/2026-10-05-watch-submit/test-submit.py` | **1** | `AssertionError` at `:42`, from `:49` | the durable submission could lose its receipts or accept a reused owner; **failing at the hash, so the launcher's refusals have no running control** (F-01) |
| `.githooks/hooks-test` | 0 | `PASS` | the worktree's hooks would not refuse what they guard (T10's bench, run here as a control of the worktree) |

**The three failures' cause, in two layers.**
- **Layer 1:** the fixtures copy `watch-build` and `watch-job` only (`test-progress.py:39-40`, `test-watch-build.py:56-57`, `test-submit.py:17-18`). `watch-build:50-51` loads `host-maintenance/build-admission` beside itself. The receipt in `/tmp/pixelelated-watch-submit-ebkyj88c/success/` reads `[Errno 2] No such file or directory: '.../tools/host-maintenance/build-admission'`.
- **Layer 2:** diagnostic copies with the module added (`.qa-scratch/t9/diag/`, two lines each) still fail all three. The receipt in `/tmp/pixelelated-watch-submit-jvbeycz8/success/console.log` reads `watch-build: build admission required; prepare tools/host-maintenance/build-admission first`, with `runner_returncode: 2`.
- **The guard:** `watch-build:96-98` (`d7e2d6be41`, #493, 2026-10-13) refuses a run without an admission or `--record-only`. `test-build-monitor` passes because `admission-test-fixture.py` copies the module and prepares a receipt.
- **Not in the CI:** `fork-checks.yml:42-44` runs the other three, so nothing has said these stopped.

## The record

Read only, at 15:45:41 UTC; nothing written under any M7 path (`.qa-scratch/t9/record/`).

- **Directories:** 46 `.build-runs/`, 45 under `/workspace/repos/rocknix.worktrees/` and the legacy checkout's. They hold 1,902 run directories and 229 loose files (45 `active.lock`, 184 others), 2,131 entries in all; the brief's 2,022 is a delta.
- **What the watcher said:** all 1,885 `build.status` files read `state: finished`. None reads `died`, `error`, `stalled` or `running`, and no run directory holds a `runner-error`.
- **The 17 run directories without a `build.status`** are not watcher runs: hand-made folders of tracker readbacks, notes and a `__pycache__`, 16 in `conflict-resolution` and 1 in `m7-browser-memory-570`. Nothing reserves `.build-runs/` for the runner's `YYYYMMDDTHHMMSSZ-<hex>` runs; this is an observation, not a finding against these tools.
- **Admission timing:** `admission.json` exists in 663 runs, with `build.start` to `admitted` a median of 0.09 s (0.08 to 0.19 s).
- **Log sizes:** `build.log` sizes over 1,885 runs: median 590 bytes, p90 2,067, max 213,562,360. The largest is `m7-p5-build-20261014-01/.build-runs/20261014T191656Z-0cac274a` (13 min, `watcher.interval` 5, `progress: none matched`); the 45,743,868-byte `m7-pixelelated-sm8550-05/.build-runs/20261015T081827Z-07dceee9` read `progress: [737/737]`.
- **No-write check:** every directory's mtime is in `mtimes-before.txt`; the newest is 2026-10-24T05:40:27Z, before the slice. The after read is at stage F.

## Proofs

| # | Claim | Evidence | Class |
| --- | --- | --- | --- |
| P1 | The slice is the brief's 18 paths, 3,795 lines and 201,453 bytes; none upstream's; 35 fork commits; the branch equals the hash on all 18 | `.qa-scratch/t9/scope.txt` | proved: tree |
| P2 | Of the eight controls at the hash in this checkout, five pass and three fail, on a missing module and then on the admission guard | `.qa-scratch/t9/controls/`, `.qa-scratch/t9/diag/`, the two `/tmp` receipts | proved: tool-run |
| P3 | The record: 46 directories, 1,902 runs, every status file `finished`, 17 non-run folders, mtimes before | `.qa-scratch/t9/record/` | proved: tool-run |
| P4 | Supervision's cost: admission 0.09 s median over 663 runs; one `--build-progress` scan of the largest log 0.45 s, the SM8550 log 0.13 s, each per 5-second interval | the two commands in `00` § Stage B | proved: tool-run |
| P5 | `hashlib.file_digest` (3.11 and later) is in the admission and retention tools, and the pinned container's Python is 3.10 | `build-admission:34`, `retention-report:22`; `device-builds.md:379-380`; the 2026-10-07 work log `:793-794`; the pin unchanged since `2c349c6d51` | proved: history |
| P6 | `test-submit.py` leaves its `mkdtemp` directory under `/tmp`; the other controls clean up | the `/tmp` counts before and after (4, 5, 6); the other prefixes 0 | proved: tool-run |
| P7 | The refusals with no control: the text search over the nine controls and the 68, 36, 32, 37 and 19 named checks | `00` § Stage B; `04` § Q6 | proved: tree |
| P8 | `build-preflight --stop-vms` signals every PID `pgrep -f 'qemu-system-x86_64'` returns, by plain `kill`, without an ownership check or a wait, and can then print `READY` | `build-preflight:101-123`; `test-swap-reclaim:368-369` tests only the combination refusal | proved: tree |
| P9 | The README's memory-guard-removed negative control ran once and is not retained as an executable control | `README.md:99`; the 2026-10-04 work log `:241`; `test-swap-reclaim:199-206` is a boundary test | proved: history |

## Findings (stage B)

| F | Q | Finding | Where (at `8ebaf8daad`) |
| --- | --- | --- | --- |
| F-01 | Q3 | Three recorded watcher controls have failed at every hash since the admission guard landed (2026-10-13), on two layers: their fixtures copy no `build-admission`, and their payloads carry neither an admission nor `--record-only`. They are the progress (D-WORKFLOW-141, blindspot 73), routing and durable-submission (D-WORKFLOW-148) positives. None is in the fork CI. | `docs/qa-logs/2026-10-04-watch-progress/test-progress.py:39-40`, `test-watch-build.py:56-57`, `docs/qa-logs/2026-10-05-watch-submit/test-submit.py:17-18`; `tools/watch-build:96-98` |
| F-02 | Q3 | `test-submit.py` leaves its `mkdtemp` directory under `/tmp` on every run, 6 on 2026-10-24 | `docs/qa-logs/2026-10-05-watch-submit/test-submit.py:15` |
| F-03 | Q3 | `build-preflight --stop-vms` finds guests with `pgrep -f 'qemu-system-x86_64'` and stops each with a plain `kill`. It does no ownership or disk check and no wait, and can print `READY` while they exit. On this shared host it would stop the other lane's guests too. The rules require a stop by pidfile through `tools/vm-stop` and a wait for exit. The monitor-socket pattern `monitor-[a-z]\.sock` is an old naming. | `tools/build-preflight:101-123` |
| F-04 | Q1 | The admission and retention tools call `hashlib.file_digest` (Python 3.11 and later). The pinned container's Python is 3.10 (#492). An admitted build started inside `make docker-shell` (`build-admission.md:101-102`) would raise `AttributeError` in `admit()`, which neither of `watch-build`'s except lists (`:190`, `:221`) names: a traceback, not a refusal, with `finish` skipped. | `tools/host-maintenance/build-admission:34`, `retention-report:22`, `:69`; `tools/watch-build:190`, `:221` |
| F-05 | Q3 | `watch-job` reports `died` when `--pid` names a process whose identity it cannot read at start (`identity` empty at `:171`, so `alive=no` at `:220-222`). A PID hidden by a sandbox's PID namespace reads as a dead job. #506's rule says an invisible PID is unknown, not exited. The help names the constraint (`:68`); nothing checks it. | `tools/watch-job:163-171`, `:218-233` |
| F-06 | Q3 | If the watcher does not exit within `interval + 10 + 5` s after the result, `watch-build`'s `monitor.wait` raises `TimeoutExpired` out of `main`, `finish` is never called, and `runner-result.json` is never written. `consume` then cannot read it and the reservation is held; this fails closed, with no control. | `tools/watch-build:202-206`, `:212-214` |
| F-07 | Q3 | The worktree lock is held by the runner alone (`open()` makes non-inheritable descriptors). A runner killed outright releases it while its command group runs on, and a second admitted build can start in the same worktree. `device-builds.md` tells an operator to inspect `command.pid` first; the tool does not. | `tools/watch-build:102-106`, `:165-167` |
| F-08 | Q6 | Guards with no control that constructs their failure (`04` § Q6): `build-admission`'s wrong-checkout, tool or schema, Docker mount contract and nested-profile refusals; `watch-build`'s inherited-path, already-finished and not-active refusals and its `--record-only`-with-`--entry` error; the submit launcher's owner refusals (only F-01's failing control); `install`'s host and account checks; `fork-newdrive`'s system-disk refusal; `build-preflight`'s `--stop-vms` path. Also `watch-build`'s end-of-run timeout (F-06) and lock gap (F-07). | `04` § Q6 |
| F-09 | Q1 | The legacy layout: `fork-newdrive:20-21` (`/workspace/repos/rocknix.worktrees`, `/workspace/repos/rocknix`) and `watch-job:36` (`/workspace/tmp/rocknix-session/<job>.status`). #640's rows. | `tools/fork-newdrive:20-21`, `tools/watch-job:36` |
| F-10 | Q6 | `fork-newdrive` is a one-time migration (2026-09-04) carrying stale assumptions:<br>• it re-creates three named worktrees (`devices`, `generic-x64`, `rclone-cleanup`) and falls back to `--detach`, which `worktrees.md` forbids for a build worktree;<br>• it copies a per-worktree `sources/` from before the shared cache;<br>• it ends by advising `sudo rm -rf ${OLD}`, against the removal rule. | `tools/fork-newdrive:140-154` |
| F-11 | Q7 | `README.md:99` says "A memory-guard-removed negative control must fail", but the suite holds no such control. It ran once (2026-10-04 work log `:241`: "fails exactly 2"), and a reader cannot re-run it. | `tools/host-maintenance/README.md:95-101` |

## Coverage table

| Path | Lines | Role | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `tools/build-preflight` | 124 | the machine before a build | `/workspace` and the monitor-socket name hardcoded (F-03) | `set -u`, no `pipefail`; quoting sound | F-03 | bash, `free`, `pgrep`; current | a few `ps` and `free` reads | `--stop-vms` kill path: no control (F-08) | the header matches the code; thresholds read in `04` § Q7 |
| `tools/fork-newdrive` | 155 | move worktrees to a new disk | F-09 (`:20-21`) | `set -euo pipefail`; quoted | `:45`'s `tail -1 &&` returns 0 on empty output, harmless: the PV walk covers LVM | bash, `lsblk`, `blkid`, `rsync`; current | n/a: run once, by hand | F-10; system-disk refusal: no control (F-08) | F-10's advice against the rules |
| `tools/fork-publish-release` | 141 | prepare a release plan, never publish | none | except list names its errors; a 900 s state-check timeout | none found; `bundle_sha256` is the bundle's directory name (`:117`), a naming nit | Python 3 | the state check per asset, up to 900 s | plan checks controlled by `tools/build-identity-test:104-167` (outside the slice) | the docstring matches; prepare-only |
| `tools/host-maintenance/README.md` | 101 | the helper's guide | n/a: prose | n/a: prose | n/a: prose | n/a: prose | n/a: prose | n/a: prose | F-11; every other claim holds (`04` § Q7) |
| `tools/host-maintenance/admission-test-fixture.py` | 36 | synthetic admission inputs | none | dense one-line style | none | Python 3 | n/a: test | the fixture behind `test-build-monitor` | says it never authorizes production allocation (`:1`) |
| `tools/host-maintenance/build-admission` | 493 | the single-use admission | F-04 | fail-closed shape: `require` everywhere; one except list | F-04 | needs Python 3.11 | 0.09 s median before a payload | four refusals with no control (F-08) | `consume-reporting-failure` is one incident's path, documented as such |
| `tools/host-maintenance/build-admission.md` | 216 | its guide | n/a: prose | n/a: prose | n/a: prose | n/a: prose | n/a: prose | n/a: prose | claims read against the code (`04` § Q7); `:101-102` names the docker-shell path F-04 breaks |
| `tools/host-maintenance/install` | 184 | install the helper and policy | host-scoped by design (`serval`, `max` uid 1000) | `-I`; `assert` used as a check (`:120`), safe because `-O` is never passed | none found | Python 3 | n/a: run once, by an administrator | host and account checks: no control (F-08) | the policy line quoted in `04` § Q7, equal to the README's |
| `tools/host-maintenance/reclaim-swap` | 242 | the root-owned swap helper | none | `-I`; a fixed environment; signals deferred around the mutation | none found; every guard has a test | Python 3 | n/a: run before a build only | every guard controlled by `test-swap-reclaim` | the README matches |
| `tools/host-maintenance/retention-report` | 313 | the read-only retention report | F-04 | errors collected, never dropped | none found; `REPORT_COMPLETE` beside inventory errors is documented (`retention-report.md:13-15`) | needs Python 3.11 | scans the declared roots; run per build stage | 19 controls | the guide matches |
| `tools/host-maintenance/retention-report.md` | 94 | its guide | n/a: prose | n/a: prose | n/a: prose | n/a: prose | n/a: prose | n/a: prose | claims hold (`04` § Q7) |
| `tools/host-maintenance/test-build-admission` | 218 | admission controls | none | dense style | none | Python 3 | 17.9 s | 68 named checks | names its cases |
| `tools/host-maintenance/test-build-monitor` | 282 | entrypoint and Makefile controls | none | none | none | Python 3 | 63.9 s, the longest control | 36 named checks, in the CI | names its cases |
| `tools/host-maintenance/test-retention-report` | 95 | retention controls | none | none | none | Python 3, `qemu-img` | 6.9 s | 19 controls | names its controls |
| `tools/host-maintenance/test-swap-reclaim` | 507 | swap, preflight and installer controls | none | none | none | Python 3, the host `visudo` for one test | 0.1 s | 37 tests; no memory-guard-removed control (F-11) | test names describe each guard |
| `tools/watch-build` | 223 | the runner every build enters | none | one except tuple per level; `AttributeError` absent (F-04) | F-06, F-07 | Python 3 | admission plus arming; 0.09 s median for the check | inherited-run refusals and `--record-only`/`--entry` error: no control (F-08) | the docstring matches |
| `tools/watch-build-submit` | 101 | durable submission | none | exclusive writes (`'x'`) throughout | none found; its control is broken (F-01) | Python 3 | n/a: one fork | owner refusals: no running control (F-01, F-08) | the docstring says submission is not completion |
| `tools/watch-job` | 270 | the status file | F-09 (`:36`) | `set -u`; outputs checked against inputs; progress pipelines without `pipefail` give "none matched", not a pass | F-05 | bash 4 (`read -d ''`, `[[ =~ ]]`) | one whole-log scan per interval: 0.45 s on the largest log | 32 checks; `died` over an unreadable PID: no control | the header names every state and its meaning |
