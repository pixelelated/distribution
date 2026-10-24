# Second opinion on a code audit -- M6.P2 T9, build supervision and host maintenance, epic tier

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository; everything you may cite is in the packet below, and every claim you make names the packet's `file:line` or the output it rests on. The first reader's verdicts are in the packet; do not take them as given.

The scope: 18 fork-own files (12 Python, 3 bash, 3 Markdown; 3,795 lines) that supervise a Linux distribution's builds on one shared build host: the runner every build enters (`tools/watch-build`), the status file (`tools/watch-job`), a durable launcher (`tools/watch-build-submit`), a single-use capacity admission (`tools/host-maintenance/build-admission`) with a read-only retention report, a **root-owned swap helper run through a passwordless sudo rule** (`tools/host-maintenance/reclaim-swap`) and its **administrator installer** (`tools/host-maintenance/install`), a preflight, a release-plan preparer and a one-time disk-move script, with their tests and guides. Read at commit `8ebaf8daad`. The build container runs Python 3.10; the host runs 3.14. Nothing was built, reclaimed, installed or published by the first reader; the tests ran in a worktree.

The first reader's draft grades: **Medium** -- F-01 (three recorded controls broken since the admission guard), F-03 (`--stop-vms` kills by `pgrep -f`); **Low** -- F-02, F-04 (`file_digest` vs Python 3.10), F-05 (`died` for an unreadable PID), F-06 (late watcher skips `finish`), F-07 (the lock ends with the runner); F-08 (guards with no control), F-09 and F-10 (legacy layout, the disk-move tool), F-11 (a README control that is not retained).

Answer in three parts, in this order:

1. **Your own findings first, starting with `reclaim-swap`, `install` and `build-admission`** -- the sudo helper, the installer that grants it, and the guard that admits a compiler -- then the rest. List every defect, gap or unsafe seam you find that is not already one of the first reader's findings. One line each: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the packet's `file:line`, what fails and when. For the helper and installer, look especially at: what a caller who can run the sudo rule, or write the checkout the installer reads from, could make root do; time-of-check against time-of-use on every path and file; signal and timeout paths around `swapoff`/`swapon`; what the policy grants beyond its one command. For the admission: whether a receipt can be reused, replayed across checkouts or registries, or consumed on evidence that does not prove what it claims; and where a refusal can be bypassed.
2. **Refute the first reader.** For every finding F-01 to F-11: agree, disagree, re-grade or narrow, and say what would make it false and whether the packet shows it. Say also whether the guard table in `04` § Q6 lists every guard the code wires, and whether any row marked `yes` rests on a control that does not construct that failure.
3. **What you could not judge.** The claims the packet does not let you verify.

Keep each item to a few lines. At most 7,000 words.

# The packet

## 02-forward-audit.md (whole)

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

## 03-retrospective.md (whole)

# Retrospective — M6.P2 T9, build supervision and host maintenance (#656)

Phase 3 of the code-auditor lifecycle: how these tools came to be what they are, read from the 35 fork commits since `c445081a59` and the evidence folders. The renovation face is in `04`.

## 3.1 What the history shows

- **Five waves, each a response to a failure the record names:**
  - **The watcher** (#393 to #395, D-WORKFLOW-141 to 143, early October): two unnoticed build failures in one day (`watch-job:14-16`) and blindspot 73, a monitor that read package completion as build activity.
  - **The swap helper and its installer** (#410, D-INFRA-015, 2026-10-04): the 2026-09-19 OOM that killed a guest and a watcher (`build-preflight:13-16`).
  - **Durable submission** (#444, D-WORKFLOW-148, 2026-10-05).
  - **Retention and admission** (#461, #489, #493, D-INFRA-018 and 022, 2026-10-07 to 10-15).
  - **The release tool's prepare-only rewrite** (#265, #530, #532, #565).
- **Each wave brought its controls,** and the evidence folders under `docs/qa-logs/` record what each guard caught when it was wired (`engineering-practices.md` § Guards must fail closed, *the positive is recorded where the guard is wired*).
- **The later waves did not re-run the earlier waves' controls.** The admission guard (`d7e2d6be41`, 2026-10-13) made `watch-build` refuse an unadmitted run.
  - It updated `test-build-monitor` through `admission-test-fixture.py`.
  - It left the three earlier controls (progress, the 2026-10-04 routing fixture, submission) refusing at the guard's first line.
  - The fork CI runs three controls, none of them these, so their failure has gone unseen for eleven days (F-01).

## 3.2 What worked

- **A guard ships with its refusal tests.** `test-swap-reclaim` (37 tests), `test-build-admission` (68 checks) and `test-retention-report` (19 controls) each construct their guards' failures with doubles, and none touches the real swap, sudoers or Docker.
- **Results belong to their producer.** The exclusive (`'x'`) writes in `watch-build-submit` and `build-admission`, and the runner's `atomic()`, keep each receipt single-writer (#597).
- **The record agrees with the watcher's contract:** 1,885 recorded runs, every one `finished`, and no `runner-error`.

## 3.3 What was hard, as the code shows it

- **Process identity across namespaces.** Each tool answers it differently:
  - `reclaim-swap` refuses unless PID 1 is `systemd` (`:81-82`);
  - `build-admission` binds the PID namespace inode (`:208`, `:246`);
  - `watch-job` reads `/proc/<pid>/stat` and treats an unreadable PID as dead (F-05);
  - `build-preflight` matches command lines by pattern (F-03).
- **One-incident recovery.** `consume-reporting-failure` (`build-admission:285-473`, 189 lines) settles the custody of one #597 collision. It is pinned to the current launcher's hash, so any edit to `watch-build-submit` retires it for future collisions; the guide says so (`build-admission.md:124-125`).

## 3.4 What the slice inherits from earlier lanes

- **T5's *read what the recorded builds would meet before a guard fails closed*:** the record read here (1,885 runs, 663 admitted) is that reading for these guards.
- **T8's *run a fork script once at stage B when it can run*:** the eight controls ran at stage A, and the two-layer cause of F-01 came from running diagnostics, not from reading.

## 3.5 The seams

| Seam | What crosses it | Read | State |
| --- | --- | --- | --- |
| The runner and the Makefile and five scripts | `Makefile:40` wraps native targets without `--entry`. The five scripts `exec ./tools/watch-build --entry` (`build:9`, `build_distro:11`, `image:9`, `install:10`, `build_compat:7`). `docker-%` runs `--docker` on the host and passes `-e RASTERATOPS_BUILD_RUN` into the container (`Makefile:179`, `:208`), whose scripts then reuse the run through `nested()`. | `test-build-monitor`'s 36 checks cover every entry line, the native and Docker routes and the docker-shell exemption | Holds. Inside `make docker-shell` there is no outer run, so a build there needs its own admission and reaches `admit()` on the container's Python 3.10 (F-04). |
| The admission and the retention report | `build-admission:104-159` reads the report beside its own `retention-report` (tool hash), its plan hash, `REPORT_COMPLETE`, no deletion, no inventory errors, the stage budget equal term for term, and an age of 900 s or less | `test-build-admission`'s report and budget cases | Holds, and it is where the report's errors become a refusal. The 900 s window covers the report's scan and the admission's preparation together; no recorded scan time was read against it. |
| The submit launcher and the runner's receipts | The launcher writes `launcher-*.json` and `tool-wrapper.rc`; the runner writes `build.rc` and `runner-result.json`. `consume` requires the three return codes to agree (`build-admission:259-262`). | `test-submit.py` (failing, F-01); `test-build-admission`'s recovery cases | Holds in the code; its control is broken. `launcher-submission.json` records `watch-build`'s hash only, not those of `watch-job` and `build-admission`, which it loads (`watch-build-submit:76`). |
| The preflight and the helper | The preflight calls `sudo -n /usr/local/sbin/pixelelated-reclaim-swap --reclaim` only below 20% free swap (`build-preflight:67-75`), the helper's own threshold (`reclaim-swap:143`), and re-reads memory afterwards (`:77`). The two cannot be combined with `--stop-vms` (`:47-50`). | `test-swap-reclaim`'s `Preflight` class, six tests | Holds. The preflight's "LOW" floor is 16,000 MB available (`:84`), and the helper needs used swap plus 16 GiB (`reclaim-swap:18`, `:125`); they measure different things and neither claims the other's number. |
| The release tool and `docs/releases/versioning.md` | the version pattern (`dev` refused), the build identity `<version>+<stamp>.g<12>`, the image-name prefix, the `v<version>` tag and the `pixelelated <version>` title | `tools/build-identity-test:104-167` (outside the slice) | Holds; the tool matches `versioning.md:10-13`, `:28-30`, `:53-57`, `:74`. |

## 04-analysis.md (whole)

# Analysis — M6.P2 T9, build supervision and host maintenance (#656)

Phase 4. Every line number is `8ebaf8daad`'s (the export `.qa-scratch/t9/at-hash/`).

## Executive summary

The 18 files are the fork's own build supervision: the runner every build enters, the status file, the durable launcher, the admission guard with its retention report, the root-owned swap helper with its installer, the preflight, the release preparer and the old disk-move tool.

The guards are carefully built. Most of them construct their refusals in controls that pass today: 37 swap tests, 68 admission checks, 36 monitor checks, 32 watcher checks and 19 retention controls. The recorded runs agree with the watcher's contract: 1,885 runs, every status `finished`.

**The slice's lead finding is about the controls rather than the tools (F-01).** The admission guard of 2026-10-13 made the runner refuse unadmitted runs, and three recorded controls broke without notice: the progress control (blindspot 73's), the routing fixture and the submission control. Their fixtures lack the admission module, and past that their payloads carry no admission.

**Beside it:**
- **F-03:** `--stop-vms` stops guests by `pgrep -f` pattern and a plain `kill`, the shape the rules forbid, on a host two lanes share.
- **F-04:** the admission and retention tools need Python 3.11, and the docker-shell path runs on the container's 3.10.
- **F-05 to F-07:** three silent or misleading states in the watcher and runner.
- **F-08:** the guards with no control.
- **F-09, F-10:** the legacy disk-move tool.
- **F-11:** a README claim with no retained control.

## Acceptance-criteria scorecard

| Brief § 7 item | State |
| --- | --- |
| The folder's six files | `00` to `04` at stage B; `05` at D |
| The lint, renovation face included | this file answers Q1 to Q7; the lint runs before D |
| `review-plan.json` and provenance | stage C |
| Punch items at an outcome | stage D onward |
| `reviewed-at` and `fixed-at` | `cdc45513b0`; `fixed-at` at H |
| `01` § Scope | done |
| 18 coverage rows | done (`02`) |
| § The controls | done; F-01 with its two-layer cause |
| § The record | done; the after read at F |
| `00`'s host line, census and no forbidden command | done |
| The Q6 guard table | below |
| The Q1 legacy rows | below |
| The Q7 guides and the sudoers quote | below |
| Proof classes equal to `00`'s PROOF lines | 9 and 9 at stage B |
| No `tools/` change before a stream | `git diff --stat 8ebaf8daad HEAD -- tools` empty |
| The retro; the six exits | stages G, H |

## Code Quality Assessment

### Strengths

- **Fail-closed shapes throughout:**
  - `build-admission`'s `require()` on every input;
  - `reclaim-swap`'s `Refused` on every unparsed observation;
  - `watch-job`'s `error` state for an unreadable result;
  - exclusive (`'x'`) writes for every receipt in `watch-build-submit` and `build-admission`.
- **The root-owned helper takes no caller-controlled input:** fixed paths, a fixed environment, no shell, and a deferred-signal critical section that verifies reactivation before it reports (`reclaim-swap:138-189`).
- **The runner never starts a command it cannot watch** (`watch-build:136-148`), and it returns 125 for a green command whose watcher failed (`:209-213`).

### Concerns

- **The controls are not kept with the guards they test:** F-01, F-08, F-11.
- **Process identity is handled four different ways** (`03` § 3.3), and two of them contradict the rules (F-03, F-05).
- **One file serves two jobs at very different scales.** `build-admission` is 493 lines, of which `consume_reporting_failure` is 189 (`:285-473`), a recovery for one incident.

### Complexity Hotspots

- **`build-admission:324-473`:** a single 150-line function with about 40 `require` conditions.
- **`watch-job:172-270`:** the observation loop, where the order of the `if` chain decides every state.
- **`watch-build:61-215`:** `main()`, 155 lines, the runner's whole lifecycle.

## Risk Assessment

- **`--stop-vms` (F-03)** is the one mutating path here that reaches past its own run. It ends any guest on the host, not only the caller's.
- **The broken controls (F-01)** mean a regression in progress reporting, routing or submission would pass the fork CI.
- **The rest fail closed:** F-04's traceback (no payload starts), F-06's held reservation, F-07's lock gap that only an outright kill opens. They are clarity and recovery risks, not data risks.

## Coverage Boundary

- **Read:** the 18 files whole at the hash; the seven entry lines as context; the six evidence folders' controls; the record's status files.
- **Not run:** a build, a reclamation, an installation, a guest stop, a disk move, a release.
- **The container's Python** is from the record (F-04, P5), not a run in the pinned image.
- **F-05 to F-07 are traced, not reproduced:**
  - **F-05** needs a PID hidden by a namespace;
  - **F-06** needs a watcher that will not exit;
  - **F-07** needs an outright kill of a runner with a live command.
  - Each can be built under `.qa-scratch` as a control at stage E without touching the host.

## Finding Verification (Phase 4.5)

For each finding: what would make it false, and whether the evidence rules that out.

| F | What would make it false | Checked |
| --- | --- | --- |
| F-01 | The controls pass in some other checkout, or fail for a reason outside the tree | They fail in the lane's checkout at the hash. With the module added they still fail, with the runner's own refusal in the receipt. |
| F-02 | The directory is removed later by something else | Six directories, one per run, the oldest from before this slice; the script has no `shutil.rmtree` (`test-submit.py`, read whole) |
| F-03 | The preflight identifies guests by a pidfile or `tools/vm-stop` | `:101` is `pgrep -f 'qemu-system-x86_64'`, `:111` is `kill "$p"`, and there is no wait. The `rss < 64 MB` skip (`:106`) filters small processes, not unowned ones. |
| F-04 | The container has Python 3.11 or later, or no admitted build runs inside it | The pin is unchanged since 2026-10-01, and the record of 2026-10-07 and 2026-10-08 says 3.10. `build-admission.md:101-102` describes a docker-shell admitted run as supported. Not run (`Coverage Boundary`). |
| F-05 | `watch-job` is never given a PID it cannot see | The help makes `--detach`'s namespace the caller's duty (`:68`). #506 records a session whose `/proc` hid a healthy build's PIDs, and the rule exists because it happened. |
| F-06 | The watcher always exits within `interval + 15` s of the result | The watcher sleeps one interval and exits on `finished`; a hung `find` or `tail` on a stalled filesystem would hold it past that. Plausible, Low. |
| F-07 | The command inherits the lock, or the next runner checks the old `command.pid` | `open()` is non-inheritable and `Popen` closes descriptors. The runner reads no earlier run's files. |
| F-08 | A control constructs these refusals under another name | Searched by refusal text over the nine controls, and read against the 192 named checks. The install tests patch these checks out (`test-swap-reclaim:438-442`, `:460-462`, `:483-487`). |
| F-09 | The paths are not legacy | `/workspace/repos/rocknix*` is the M7 lane's layout, recorded by #640 and D-INFRA-025 |
| F-10 | `fork-newdrive` still has a current use | Its last run was the 2026-09-04 move. Its worktree list and `sources/` step predate the current layout (`device-builds.md` § Where things live). |
| F-11 | The negative control is retained somewhere | `git grep` finds it only in the 2026-10-04 work log, and the evidence folder holds none |

## Renovation face

### Q1 Modernize

**The two legacy-layout rows, quoted at the hash and unchanged on the branch** (deferred to #640; futro A5):

```
tools/fork-newdrive:20:WT_DIR="${WT_DIR:-/workspace/repos/rocknix.worktrees}"
tools/fork-newdrive:21:MAIN="${MAIN:-/workspace/repos/rocknix}"
tools/watch-job:36:#   cat /workspace/tmp/rocknix-session/<job>.status
```

Beside them:
- **F-04**, `hashlib.file_digest` against the container's 3.10.
- **F-03's** monitor-socket pattern `monitor-[a-z]\.sock` (`build-preflight:107`), from an older guest naming.
- **`build-preflight:81`**, which reports `/workspace` by a hardcoded path.

`install`'s `serval` and `max` (uid 1000) are deliberate host scoping (`README.md:29-30`), not drift.

### Q2 Standards and best practices

- **Python:**
  - every entry point has one except tuple at its top;
  - `watch-build:190` and `:221` omit `AttributeError` (F-04's path);
  - `install:120` uses `assert` as a check, safe under its fixed `-I` shebang.
- **Bash:**
  - `watch-job` and `build-preflight` run `set -u` without `pipefail`. Their pipelines produce display text (`progress: none matched`), never a pass, so nothing passes on a failed pipeline.
  - `fork-newdrive` runs `set -euo pipefail`.
  - Every expansion that becomes an argument is quoted.
- **Rules the code itself contradicts:**
  - `build-preflight:101-111` stops processes found by pattern (F-03), against `engineering-practices.md` § A promise is not a mechanism: *"Stop a watcher by the pid its status file records, never by pattern"*. The VM rule says guests stop by pidfile through `tools/vm-stop`.
  - `fork-newdrive:142` and `:154` contradict `worktrees.md` (F-10).

### Q3 Bugs

- **F-01** (Medium): three recorded controls broken since 2026-10-13.
- **F-03** (Medium): `--stop-vms` stops any guest by pattern.
- **F-04** (Low): `AttributeError` on the docker-shell admitted path.
- **F-05** (Low): an unreadable PID reported as `died`.
- **F-06** (Low): a late watcher skips `finish`.
- **F-07** (Low): the worktree lock does not cover an orphaned command.
- **F-02** (Low): `test-submit.py` leaks a directory under `/tmp`.

Each `bug` is filed at stage D with its code trace, `Already written:` and the VM line.

### Q4 Package currency

These tools pin nothing; the currency question is the interpreters they need:
- **Python 3.11 or later** for `build-admission` and `retention-report` (`hashlib.file_digest`). The host has 3.14; the container has 3.10 (F-04).
- **Python 3.6 or later** for everything else.
- **bash 4 or later** for `watch-job` (`read -d ''`, `[[ =~ ]]`).
- **`tools/council`** is the tree's only npm consumer (`git ls-files` finds one `package.json`).

### Q5 Efficiency

What a build pays for its supervision, from the record (P4):
- **The admission check** adds a median 0.09 s before the payload (663 runs, 0.08 to 0.19 s). The retention report it needs is prepared separately, and its scan time was not in the record read.
- **The watcher** wakes every 5 s, the interval `watch-build` passes. With `--build-progress` it re-reads the whole `build.log` each time (`watch-job:212-214`): 0.45 s on the largest recorded log (213,562,360 bytes), about 9% of one core, and 0.13 s on the 45,743,868-byte SM8550 log. The median log is 590 bytes.
- **No item:** the cost is small beside a 24-core build, and an offset-tracking reader would add a state the watcher does not have today.

### Q6 Dead ends

**The guard table.** Every guard the code wires, with the control that constructs its failure (file and test name) or `none`. "Running" means the control passes at the hash in this checkout.

| # | Tool | Guard (where) | Control | Running |
| --- | --- | --- | --- | --- |
| 1 | `watch-job` | quiet logs become `stalled` (`:236-237`) | `test-watch-job.py` "quiet logs stall; unrelated heartbeat files do not mask it" | yes |
| 2 | `watch-job` | a fresh package log prevents a false stall (`:183-208`) | "fresh package log prevents false stall; both progress counters retained" | yes |
| 3 | `watch-job` | `died`: no result and no process (`:232-233`) | "job death without result is detected" | yes |
| 4 | `watch-job` | a zombie is not alive (`:168`) | "unreaped zombie is not a live job" | yes |
| 5 | `watch-job` | `finished` keeps the exit code (`:225-228`) | "result code 0 preserved", "result code 23 preserved" | yes |
| 6 | `watch-job` | `error` on a result that is not 0 to 255 (`:229-230`) | "invalid result fails closed" ×3 | yes |
| 7 | `watch-job` | `error` on a lost activity directory (`:203`) | "lost activity directory is an observation error" | yes |
| 8 | `watch-job` | a job that writes no log stalls (`:208`) | "job that never writes a log eventually stalls" | yes |
| 9 | `watch-job` | setup refusals: interval, stall, PID, pattern, missing log, activity directory, overlapping status (`:100-127`) | "refuse invalid setup ..." ×9 | yes |
| 10 | `watch-job` | a detached watcher acknowledges its child and records later failure (`:129-156`) | "detach retains activity argument and acknowledges actual child", "detached watcher records subsequent failure" | yes |
| 11 | `watch-job` | a stopped watcher leaves a detectably stale heartbeat (`:242-269`) | "stopping watcher leaves detectably stale heartbeat" | yes |
| 12 | `watch-job` | overall progress only from structured pkgbuilder lines (`:209-214`; blindspot 73) | `docs/qa-logs/2026-10-04-watch-progress/test-progress.py` | **no** (F-01) |
| 13 | `watch-job` | a PID unreadable at start is reported `died`, where #506's rule says unknown (`:171`, `:220-222`) | none (F-05) | -- |
| 14 | `watch-build` | one top-level build per worktree (`:102-106`) | `test-build-monitor` "one top-level build per worktree" | yes |
| 15 | `watch-build` | an admission is required (`:96-98`) | `test-build-admission` "missing receipt blocks payload" | yes |
| 16 | `watch-build` | a stale inherited marker is refused (`:41-42`) | `test-build-monitor` "stale inherited marker cannot bypass monitoring" | yes |
| 17 | `watch-build` | inherited path, interval, state and finished refusals (`:33-46`) | none (F-08) | -- |
| 18 | `watch-build` | the record-only route; a record-only parent cannot admit nested compilation (`:84-98`) | `test-build-admission` "explicit recording-only job requires no build allocation", "recording-only parent cannot admit nested compilation" | yes |
| 19 | `watch-build` | `--record-only` with `--entry`, `--docker` or `--admission` is an error (`:84-85`) | none (F-08) | -- |
| 20 | `watch-build` | a watcher that cannot arm stops the launch (`:136-148`) | `test-build-monitor` "watcher startup failure refuses command launch" | yes |
| 21 | `watch-build` | a lost watcher cannot give a green run (`:208-213`) | "lost watcher cannot produce a green monitored run" | yes |
| 22 | `watch-build` | termination is forwarded to the child; 143 kept (`:153-160`, `:189`) | "termination forwards to child and retains143" | yes |
| 23 | `watch-build` | a killed runner is recorded without an invented result | "detached monitor records killed runner without inventing result" | yes |
| 24 | `watch-build` | every entry line enters the runner (the Makefile and five scripts) | "routing regression check fails when an entrypoint loses its hook" | yes |
| 25 | `watch-build` | a watcher still running past `interval + 15` s skips `finish` (`:202-206`) | none (F-06) | -- |
| 26 | `watch-build` | the lock ends with the runner, not its command (`:102`, `:165`) | none (F-07) | -- |
| 27 | `watch-build-submit` | owner reuse, inherited runs and receipt overwrites refused (`:65-71`, `:20-23`, `:44`) | `docs/qa-logs/2026-10-05-watch-submit/test-submit.py` | **no** (F-01) |
| 28 | `build-admission` | expired or future admission (`:181-182`) | "expired admission blocks payload", "future admission blocks payload" | yes |
| 29 | `build-admission` | single use (`:200`) | "consumed admission cannot launch twice" | yes |
| 30 | `build-admission` | capacity at preparation and at launch, less reservations (`:166-168`, `:202-204`) | "prepare refuses insufficient current capacity", "launch rechecks capacity after preparation", "existing unresolved reservations reduce new capacity" | yes |
| 31 | `build-admission` | changed plan, source, measurement, protected input, profile, report or registry (`:104-159`, `:183-201`) | the seven "changed ... blocks payload" cases and "refused report blocks payload" | yes |
| 32 | `build-admission` | an undeclared `BUILD_DIR` (`:192-194`) | "undeclared BUILD_DIR blocks payload" | yes |
| 33 | `build-admission` | a receipt for a different checkout (`:185`) | none (F-08) | -- |
| 34 | `build-admission` | a changed admission tool or schema (`:180`) | none (F-08) | -- |
| 35 | `build-admission` | the Docker mount contract (`:189-190`) | none (F-08) | -- |
| 36 | `build-admission` | nested source and profile (`nested()`, `:220-226`) | none (F-08); only its missing-`admission.json` path, through row 18 | -- |
| 37 | `build-admission` | `consume`: a live command, a foreign namespace, changed evidence, a failure called qualified; idempotent (`:242-282`) | "live original command prevents consumption", "foreign PID namespace cannot prove completion", "changed retained evidence prevents consumption", "failed job cannot be relabelled qualified", "same completion evidence reconciles idempotently" | yes |
| 38 | `build-admission` | `consume-reporting-failure`'s refusals (`:324-473`) | the 36 "report recovery refuses ..." cases and five more | yes |
| 39 | `reclaim-swap` | ownership, type, mode and hard links (`:32-41`) | `test-swap-reclaim` `test_unsafe_ownership_mode_links_and_type_refused` | yes |
| 40 | `reclaim-swap` | the lock (`:200-215`) | `test_lock_excludes_concurrent_reclamation`, `test_writable_lock_parent_refused_before_open` | yes |
| 41 | `reclaim-swap` | arguments, root, installed path (`:218-227`) | `test_args_nonroot_and_source_copy_cannot_mutate` | yes |
| 42 | `reclaim-swap` | `/proc/swaps` parse and target (`:44-63`) | `test_swap_exact_and_empty`, `test_swap_malformed_or_other_target_refused` | yes |
| 43 | `reclaim-swap` | `MemAvailable` (`:66-76`) | `test_available_ram_missing_or_invalid_refused` | yes |
| 44 | `reclaim-swap` | busy host and namespace (`:79-100`) | `test_active_jobs_and_container_namespace_refused`, `test_idle_process_exit_and_unreadable_process` | yes |
| 45 | `reclaim-swap` | the `fstab` activation (`:111-120`) | `test_activation_flags_are_not_silently_lost` | yes |
| 46 | `reclaim-swap` | priority (`:147-148`, `:174-179`) | `test_unrestorable_negative_priority_refuses`, `test_reclaims_only_one_file_and_restores_priority` | yes |
| 47 | `reclaim-swap` | memory headroom and its recheck (`:123-127`, `:150-155`) | `test_insufficient_memory_and_boundary`, `test_second_memory_read_refuses_new_pressure` | yes |
| 48 | `reclaim-swap` | a job started or the file changed during checks (`:149-158`) | `test_job_started_during_checks_refuses_before_mutation`, `test_active_job_and_changed_file_refuse_before_mutation` | yes |
| 49 | `reclaim-swap` | reactivation, failure and signals (`:162-188`) | `test_failed_swapoff_still_active_is_not_success`, `test_partial_swapoff_failure_and_interruption_reactivate`, `test_failed_swapon_never_reports_success`, `test_false_swapon_success_and_priority_drift_refused`, `test_signal_acknowledged_only_after_reactivation` | yes |
| 50 | `reclaim-swap` | healthy no-op; inactive swap refused (`:141-145`) | `test_healthy_noop_and_inactive_refusal` | yes |
| 51 | `reclaim-swap` | the memory guard itself, removed: a mutation control (`README.md:99`) | recorded once, the 2026-10-04 work log `:241` (F-11) | not retained |
| 52 | `install` | sudoers order and later files (`:67-79`) | `test_rule_order_refuses_later_files_or_main_directives` | yes |
| 53 | `install` | the include required (`:59-64`) | `test_policy_directory_must_be_included`, `test_real_visudo_rejects_unowned_include_directory` | yes |
| 54 | `install` | the exact policy line (`:20-26`) | `test_policy_is_exact_action_with_hash_receipt_and_valid_sudoers` | yes |
| 55 | `install` | non-root refused (`:83-84`) | `test_unprivileged_installation_cannot_write` | yes |
| 56 | `install` | validation rollback of both files (`:123-151`) | `test_policy_validation_failure_rolls_back_both_files`, `test_failed_policy_restore_still_restores_helper_and_cleans_temps` | yes |
| 57 | `install` | legacy migration only if unchanged (`:101-102`) | `test_migrate_only_unchanged_legacy_policy` | yes |
| 58 | `install` | host and account (`:85-88`) and `secure()` of paths (`:29-35`, `:89-94`) | none: patched to pass in every test (F-08) | -- |
| 59 | `retention-report` | its 18 refusals and one eligible case (`evaluate()`, `:207-265`) | `test-retention-report`'s 19 controls | yes |
| 60 | `build-preflight` | default read-only, opt-in helper, missing helper, inactive swap, bad observations and options (`:36-99`) | `test-swap-reclaim` `Preflight`'s six tests | yes |
| 61 | `build-preflight` | `--stop-vms` (`:101-119`) | none: only the combination refusal (`:368-369`) (F-03, F-08) | -- |
| 62 | `fork-publish-release` | the plan checks (`:21-125`) | `tools/build-identity-test:104-167` (outside the slice) | yes, by its own run |
| 63 | `fork-newdrive` | system-disk, mounted-disk and existing-`fstab` refusals (`:94-112`) | none (F-08); a one-time tool run by hand | -- |

**Rows with no running control:** 12 and 27 (F-01); 13, 17, 19, 25, 26, 33 to 36, 58, 61 and 63 (F-08); 51 (F-11).

**Dead ends:**
- `fork-newdrive` (F-10) is a one-time migration whose layout has gone (#640).
- `consume-reporting-failure` is live: it is pinned to the current launcher's hash (`3777c68f…` equals `watch-build-submit` at the hash), and it settles one incident's custody by design.

### Q7 Clarity and structure

**`README.md` against the code.** Every claim holds except F-11:

| Claim | Code |
| --- | --- |
| below 20% free | `reclaim-swap:143` |
| used swap plus 16 GiB | `:18`, `:125` |
| builders, compilers, watchers or QEMU refused | `:83-100` |
| the lock in root-owned `/run` | `:17`, `:202` |
| priority -1 kept; other negatives refused | `:147-148` |
| explicit priorities kept | `:174-175` |
| the 120 s timeout | `:133` |
| root:root 0755 and 0440 | `install:45-46`, `:107-108` |
| the include required | `:59-64` |
| later files refused | `:75-79` |
| unchanged legacy migrated | `:101-102` |

**The sudoers policy the installer writes** (`install:22-26`):

```python
    return ('# Managed by pixelelated tools/host-maintenance/install (#410).\n'
            '# Only this root-owned helper and literal argument; no environment grants.\n'
            f'# Installed helper SHA256 {digest} (receipt; sudo-rs has no digest matcher).\n'
            'max ALL=(root) NOPASSWD: NOSETENV: '
            '/usr/local/sbin/pixelelated-reclaim-swap --reclaim\n').encode()
```

and the README's sentence about it (`README.md:46-50`): *"The sole added permission is:"* `max ALL=(root) NOPASSWD: NOSETENV: /usr/local/sbin/pixelelated-reclaim-swap --reclaim`. **Equal byte for byte.** The README's *"does not modify fleet policy"* (`:42`) holds: `install` writes only `POLICY`, `HELPER` and the legacy file.

**`build-admission.md`:** each claim checked holds.

| Claim | Code |
| --- | --- |
| checked after the watcher arms, before the payload | `watch-build:136-148`, `:163-164` |
| nested reuse checks source and profile | `:220-226` |
| a record-only parent cannot admit nesting | `watch-build:92-93` and `nested()`'s read of `admission.json` |
| 15-minute expiry | `MAX_AGE = 900` |
| `f_bavail` less reservations | `:153-157`, `:202-204` |
| the registry in the common Git directory | `:77-80` |
| the consumer's checks | `:242-282` |
| the collision recovery | `:324-473` |
| "never contact Docker" for the controls | the recovery cases mock the census |

It describes an interactive docker-shell admitted run (`:101-102`) that F-04 breaks.

**`retention-report.md`:** each claim holds.

| Claim | Code |
| --- | --- |
| the output must be new | `:309`, `'x'` |
| a completed report can still reject everything; read errors and `fits_now` | `:13-15` |
| no directory symlinks followed | `:100-107` |
| hard-linked or differently owned files held | `:230-231` |
| a disk another disk references is held | `:223-225` |
| any live QEMU holds all candidates | `:181-182`, `:218` |

**The rules' descriptions of these tools** (`device-builds.md` § Before a build; `engineering-practices.md` § A promise is not a mechanism):
- **The descriptions match the code** for `watch-build`'s routing and markers, `watch-build-submit`'s receipts, the admission's single use, and `build-preflight`'s report and `--reclaim-swap`.
- **No drift for T4.** Where the code departs from a rule (F-03, F-05, F-10), the code is the defect and the rule is right.

**Smaller clarity points** (no items):
- `fork-publish-release:117` names the bundle's directory `bundle_sha256`.
- `launcher-submission.json` hashes only `watch-build` (`watch-build-submit:76`).
- The README's "less than20%" style lacks spaces before numbers throughout (a house style of #410's writer).

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- **A guard that changes a tool's contract re-runs every recorded control of that tool,** not only the ones in the CI. This would have caught F-01 on 2026-10-13. The rule's home is `engineering-practices.md` § Guards must fail closed; the coordinator's call (T4's lane).

### Codification Gaps (needs-new-rule)

- **A process found by pattern is never signalled** (F-03). This is already in `engineering-practices.md` for watchers and in the VM rule for guests. Its enforcement could be a grep in `tools/rules-check` or T10's guards for `pgrep -f` followed by `kill` in `tools/`. A lead for T10 (#657).

### Recommended Action Sequence

1. F-01: the three controls repaired and put in the fork CI (a stream).
2. F-03: `--stop-vms` through `tools/vm-stop` or removed (a stream; its contract is the coordinator's).
3. F-04 to F-07: each a bug with its control at stage E.
4. F-08: a control per `none` row, beside its stream or as one Renovation stream.
5. F-09, F-10: #640.
6. F-02, F-11: with F-01's stream and the README.

## Quality Self-Check

- Every finding cites a line at the hash and was re-read before it was written.
- Each `none` in the guard table came from a text search and the named checks, not from the absence of a match alone. Row 58's `none` was confirmed by reading the patches.
- No guard was run against the host; F-04's container fact is history.
- The counts in `02`, P1 to P9, and this file agree.

## file, whole, at 8ebaf8daad: tools/build-preflight

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # build-preflight -- what the machine has before a build takes it.
    6  #
    7  #   tools/build-preflight            # report only
    8  #   tools/build-preflight --stop-vms # also stop running QA guests
    9  #   tools/build-preflight --reclaim-swap # guarded host helper, before a build
   10  #
   11  # Builds here are memory-bound, not disk-bound, and the two are easy to
   12  # confuse: /workspace has terabytes free while the box runs out of RAM. On
   13  # 2026-09-19 a cold GENERIC_X64 build reached webkitgtk, compiled WebCore at
   14  # CONCURRENCY_MAKE_LEVEL=nproc=24, and the kernel killed cc1plus twice. It
   15  # also killed a running QA guest and a background watcher, so the first
   16  # symptom was silence rather than an error.
   17  #
   18  # What this checks, and why each one:
   19  #
   20  #   RAM        the constraint. A heavyweight C++ package wants 1.5-2.5 GB per
   21  #              parallel compiler.
   22  #   Swap       a full swap means there is no cushion left: the next spike goes
   23  #              to the OOM killer rather than degrading. Reclaiming it needs
   24  #              root. Default mode reports only; --reclaim-swap uses the installed guarded helper.
   25  #   QA guests  each QEMU guest holds ~2 GB and they are often left up for
   26  #              days. They are also what the build will kill first.
   27  #   Disk       reported for completeness; it has never been the limit here.
   28  #
   29  # It exits 0 when the machine looks ready, 1 when something is worth fixing
   30  # first. It never stops a guest without --stop-vms, because a guest may be
   31  # holding QA state someone is in the middle of.
   32  
   33  set -u
   34  STOP_VMS=0
   35  RECLAIM_SWAP=0
   36  for option in "$@"; do
   37      case "$option" in
   38          --stop-vms) STOP_VMS=1 ;;
   39          --reclaim-swap) RECLAIM_SWAP=1 ;;
   40          -h|--help)
   41              echo 'usage: tools/build-preflight [--stop-vms] [--reclaim-swap]'
   42              echo 'Default is read-only. Reclaim runs the installed fixed-action helper before a build.'
   43              exit 0 ;;
   44          *) echo "build-preflight: unknown option: $option" >&2; exit 2 ;;
   45      esac
   46  done
   47  if [ "$STOP_VMS" = 1 ] && [ "$RECLAIM_SWAP" = 1 ]; then
   48      echo 'Stop guests first, wait for them to exit, then run --reclaim-swap separately.' >&2
   49      exit 2
   50  fi
   51  
   52  verdict=0
   53  say() { printf '%s\n' "$*"; }
   54  
   55  read_memory() {
   56      local observation value
   57      observation=$(free -m) || return 1
   58      read -r _ mem_total mem_used _ _ _ mem_avail <<<"$(awk 'NR==2' <<<"$observation")"
   59      read -r _ swap_total swap_used swap_free <<<"$(awk 'NR==3' <<<"$observation")"
   60      for value in "$mem_total" "$mem_used" "$mem_avail" "$swap_total" "$swap_used" "$swap_free"; do
   61          [[ "$value" =~ ^[0-9]+$ ]] || return 1
   62      done
   63      [ "$mem_total" -gt 0 ] && [ "$mem_avail" -le "$mem_total" ] &&
   64          [ "$swap_free" -le "$swap_total" ] && [ "$swap_used" -le "$swap_total" ]
   65  }
   66  read_memory || { say 'ERROR: cannot read valid host memory counters'; exit 1; }
   67  if [ "$RECLAIM_SWAP" = 1 ] && [ "$swap_total" -gt 0 ] && [ "$swap_free" -lt $(( swap_total / 5 )) ]; then
   68      helper=/usr/local/sbin/pixelelated-reclaim-swap
   69      if [ ! -x "$helper" ]; then
   70          say '  RECLAIM UNAVAILABLE: install the reviewed tools/host-maintenance helper first.'
   71          verdict=1
   72      elif ! sudo -n -- "$helper" --reclaim; then
   73          say '  RECLAIM REFUSED: helper guards or administrator installation need attention.'
   74          verdict=1
   75      fi
   76      # The helper's exit status is not the memory observation; read the host again.
   77      read_memory || { say 'ERROR: cannot read valid host memory counters after reclaim'; exit 1; }
   78  fi
   79  say "RAM    ${mem_total}MB total, ${mem_used}MB used, ${mem_avail}MB available"
   80  say "Swap   ${swap_total}MB total, ${swap_used}MB used, ${swap_free}MB free"
   81  say "Disk   $(df -h /workspace | awk 'NR==2{print $4" free of "$2}')  (not the usual limit)"
   82  say ""
   83  
   84  if [ "$mem_avail" -lt 16000 ]; then
   85      say "  LOW: under 16GB available. A heavyweight package will not fit beside this."
   86      verdict=1
   87  fi
   88  if [ "$swap_total" -eq 0 ]; then
   89      say '  NO ACTIVE SWAP: inspect /proc/swaps and restore the configured swap as administrator.'
   90      say '    The guarded helper only recycles an already-active /swap.img; it cannot recover this state.'
   91      verdict=1
   92  fi
   93  if [ "$swap_total" -gt 0 ] && [ "$swap_free" -lt $(( swap_total / 5 )) ]; then
   94      say "  SWAP EXHAUSTED: ${swap_free}MB of ${swap_total}MB free. There is no cushion;"
   95      say "    the next spike is an OOM kill rather than a slowdown. To reclaim it:"
   96      say '      tools/build-preflight --reclaim-swap'
   97      say '    Uses the installed guarded /swap.img helper; see tools/host-maintenance/README.md.'
   98      verdict=1
   99  fi
  100  
  101  guests=$(pgrep -f 'qemu-system-x86_64' 2>/dev/null)
  102  if [ -n "$guests" ]; then
  103      say "  QA guests running:"
  104      for p in $guests; do
  105          rss=$(( $(ps -o rss= -p "$p" 2>/dev/null || echo 0) / 1024 ))
  106          [ "$rss" -lt 64 ] && continue
  107          mon=$(tr '\0' ' ' < "/proc/$p/cmdline" 2>/dev/null | grep -oE 'monitor-[a-z]\.sock' | head -1)
  108          up=$(ps -o etime= -p "$p" 2>/dev/null | tr -d ' ')
  109          say "      pid $p  ${mon:-unknown}  ${rss}MB  up ${up}"
  110          if [ "$STOP_VMS" = 1 ]; then
  111              kill "$p" 2>/dev/null && say "        stopped"
  112          fi
  113      done
  114      if [ "$STOP_VMS" = 0 ]; then
  115          say "    Each is ~2GB, and a build under pressure will kill them before it fails"
  116          say "    itself -- one was lost that way on 2026-09-19. Stop the idle ones with"
  117          say "    --stop-vms, or leave them knowingly."
  118          verdict=1
  119      fi
  120  fi
  121  
  122  say ""
  123  [ "$verdict" = 0 ] && say "READY" || say "Worth clearing the above first; a build that finishes beats one that is fast."
  124  exit "$verdict"
  125  
```

## file, whole, at 8ebaf8daad: tools/fork-newdrive

```
    1  #!/usr/bin/env bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  #
    4  # Move the build worktrees onto a freshly formatted disk.
    5  #
    6  # Deliberately does NOT migrate build roots. After an upstream merge with a
    7  # repo-wide metadata sweep every stamp is invalid anyway (see device-builds.md),
    8  # so copying hundreds of gigabytes of output only to delete it is waste. The
    9  # worktrees are re-created from git -- a checkout is ~100 MB -- and only
   10  # sources/, the content-addressed download cache, is carried across.
   11  #
   12  #   sudo parted /dev/nvme1n1 mklabel gpt
   13  #   sudo parted -a optimal /dev/nvme1n1 mkpart primary ext4 0% 100%
   14  #   sudo mkfs.ext4 -L rocknix-build /dev/nvme1n1p1
   15  #   ./tools/fork-newdrive /dev/nvme1n1p1
   16  set -euo pipefail
   17  
   18  PART="${1:-}"
   19  # Defaults follow the fleet /workspace convention (see device-builds.md).
   20  WT_DIR="${WT_DIR:-/workspace/repos/rocknix.worktrees}"
   21  MAIN="${MAIN:-/workspace/repos/rocknix}"
   22  OLD="${WT_DIR}.old"
   23  
   24  die() { echo "error: $*" >&2; exit 1; }
   25  
   26  usage() {
   27      cat <<USAGE
   28  usage: $0 --identify            list disks that look like a safe target
   29         $0 /dev/nvmeXn1p1        migrate onto an already-formatted partition
   30  
   31  Device names are not stable. A new drive can enumerate FIRST and push the OS
   32  disk down a number: fitting a 4 TB drive to this machine made the new disk
   33  nvme0n1 and moved the boot disk to nvme1n1, so instructions written in advance
   34  named the OS disk. --identify reads the machine rather than guessing.
   35  USAGE
   36      exit "${1:-1}"
   37  }
   38  
   39  # Which physical disk backs a mount, if any.
   40  disk_of_mount() {
   41      local src pk
   42      src=$(findmnt -no SOURCE "$1" 2>/dev/null) || return 0
   43      [ -n "${src}" ] || return 0
   44      # LVM and friends: walk to the physical parent.
   45      lsblk -nlo PKNAME "${src}" 2>/dev/null | grep -v '^$' | tail -1 && return 0
   46      lsblk -nlo NAME,TYPE -s "${src}" 2>/dev/null | awk '$2=="disk"{print $1; exit}'
   47  }
   48  
   49  system_disks() {
   50      { disk_of_mount /; disk_of_mount /boot; disk_of_mount /boot/efi
   51        # anything an LVM PV sits on counts too
   52        pvs --noheadings -o pv_name 2>/dev/null | while read -r pv; do
   53            lsblk -nlo PKNAME "${pv}" 2>/dev/null | tail -1
   54        done
   55      } | sed 's#^/dev/##' | grep -v '^$' | sort -u
   56  }
   57  
   58  identify() {
   59      local sys; sys=$(system_disks)
   60      echo "Disks holding the running system: ${sys//$'\n'/ }"
   61      echo
   62      printf '  %-14s %-10s %-6s %-28s %s\n' DEVICE SIZE PARTS MODEL VERDICT
   63      local d name parts model verdict
   64      for d in /dev/nvme?n? /dev/sd?; do
   65          [ -b "${d}" ] || continue
   66          name=$(basename "${d}")
   67          parts=$(lsblk -no NAME "${d}" 2>/dev/null | tail -n +2 | grep -c . || true)
   68          model=$(cat "/sys/block/${name}/device/model" 2>/dev/null | xargs)
   69          if printf '%s\n' "${sys}" | grep -qx "${name}"; then
   70              verdict="SYSTEM DISK - never touch"
   71          elif [ "${parts}" -gt 0 ]; then
   72              verdict="has ${parts} partition(s) - inspect first"
   73          else
   74              verdict="empty - candidate"
   75          fi
   76          printf '  %-14s %-10s %-6s %-28s %s\n' "${d}" "$(lsblk -dno SIZE "${d}")" "${parts}" "${model:0:28}" "${verdict}"
   77      done
   78      exit 0
   79  }
   80  
   81  [ "${PART}" = "--identify" ] && identify
   82  [ "${PART}" = "-h" ] || [ "${PART}" = "--help" ] && usage 0
   83  [ -n "${PART}" ] || usage
   84  [ -b "${PART}" ] || die "${PART} is not a block device"
   85  [ -d "${MAIN}/.git" ] || die "${MAIN} is not the primary checkout"
   86  
   87  # Refuse anything on a disk the running system lives on.
   88  #
   89  # The instructions for this migration were written before the drive was fitted
   90  # and named nvme1n1 for the new disk. The new disk enumerated first, so
   91  # nvme1n1 was the OS. Nothing in the original script would have stopped
   92  # `mkfs.ext4` on the boot drive -- it was a valid block device. A check that
   93  # only asks "is this a block device" cannot fail in the way that matters.
   94  PARENT=$(lsblk -nlo PKNAME "${PART}" 2>/dev/null | tail -1)
   95  [ -n "${PARENT}" ] || PARENT=$(basename "${PART}")
   96  if system_disks | grep -qx "${PARENT}"; then
   97      die "${PART} is on ${PARENT}, which holds the running system. Refusing.
   98       Run '$0 --identify' to see which disk is actually the new one."
   99  fi
  100  MOUNTED=$(lsblk -nlo MOUNTPOINT "/dev/${PARENT}" 2>/dev/null | grep -v '^$' | grep -v "^${WT_DIR}$" || true)
  101  if [ -n "${MOUNTED}" ]; then
  102      die "${PARENT} has mounted filesystems (${MOUNTED//$'\n'/, }). Refusing."
  103  fi
  104  
  105  UUID=$(blkid -s UUID -o value "${PART}") || die "cannot read a UUID from ${PART}"
  106  [ -n "${UUID}" ] || die "no filesystem on ${PART} -- format it first"
  107  
  108  echo "Partition : ${PART}"
  109  echo "UUID      : ${UUID}"
  110  echo "Target    : ${WT_DIR}"
  111  echo
  112  grep -q "${UUID}" /etc/fstab && die "already in /etc/fstab; nothing to do"
  113  
  114  # Everything below needs root, and asks once.
  115  echo "This will:"
  116  echo "  1. mount ${PART} at ${WT_DIR} (the current one moves to ${OLD})"
  117  echo "  2. add it to /etc/fstab by UUID"
  118  echo "  3. copy sources/ across  ($(du -sh "${OLD:-${WT_DIR}}"/*/sources 2>/dev/null | head -1 | cut -f1) if present)"
  119  echo "  4. re-create the build worktrees from git"
  120  echo
  121  echo "It does NOT delete the old build roots. Check the result, then remove"
  122  echo "${OLD} yourself -- that is the irreversible half and it is not automated."
  123  read -r -p "Continue? [y/N] " ans
  124  [ "${ans}" = "y" ] || die "aborted"
  125  
  126  SRC_CACHE=""
  127  for c in "${WT_DIR}"/*/sources; do [ -d "$c" ] && { SRC_CACHE="$c"; break; }; done
  128  
  129  sudo mv "${WT_DIR}" "${OLD}"
  130  sudo mkdir -p "${WT_DIR}"
  131  sudo chown "$(id -u):$(id -g)" "${WT_DIR}"
  132  echo "UUID=${UUID}  ${WT_DIR}  ext4  defaults,noatime  0  2" | sudo tee -a /etc/fstab >/dev/null
  133  sudo mount "${WT_DIR}"
  134  sudo chown "$(id -u):$(id -g)" "${WT_DIR}"
  135  echo "mounted, fstab updated"
  136  
  137  # git no longer knows where the worktrees went; drop the stale registrations.
  138  git -C "${MAIN}" worktree prune
  139  
  140  for b in devices generic-x64 rclone-cleanup; do
  141      git -C "${MAIN}" worktree add "${WT_DIR}/${b}" "build/${b}" 2>/dev/null \
  142          || git -C "${MAIN}" worktree add --detach "${WT_DIR}/${b}" next
  143      echo "  worktree: ${b}"
  144  done
  145  
  146  if [ -n "${SRC_CACHE}" ] && [ -d "${OLD}/$(basename "$(dirname "${SRC_CACHE}")")/sources" ]; then
  147      D="${WT_DIR}/devices/sources"
  148      echo "copying the download cache -- this is the only bulk copy"
  149      mkdir -p "${D}"
  150      rsync -aH --info=progress2 "${OLD}/$(basename "$(dirname "${SRC_CACHE}")")/sources/" "${D}/"
  151  fi
  152  
  153  echo
  154  echo "done. Old tree left at ${OLD} -- verify, then:  sudo rm -rf ${OLD}"
  155  df -h "${WT_DIR}" | tail -1
  156  
```

## file, whole, at 8ebaf8daad: tools/fork-publish-release

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present pixelelated
    4  """Prepare GitHub release identity from an explicit immutable candidate bundle.
    5  
    6  No upload, tag creation, asset replacement or publication occurs. The previous
    7  newest-file/date/undraft path is retired (#265, #530). Actual publication needs
    8  the independent qualification/source/credential gates and named approval.
    9  """
   10  import argparse
   11  import json
   12  import os
   13  from pathlib import Path
   14  import re
   15  import signal
   16  import subprocess
   17  import sys
   18  from datetime import datetime
   19  
   20  
   21  def prepare(bundle):
   22      store = Path(__file__).resolve().with_name("rasteratops-candidate-store")
   23      subprocess.run([str(store), "verify", str(bundle)], check=True,
   24                     stdout=sys.stderr)
   25      manifest = json.loads((bundle / "manifest.json").read_text())
   26      identities = [name for name in manifest["files"] if name.endswith(".identity.json")]
   27      if not identities:
   28          raise ValueError("bundle has no build identity; do not relabel historical firmware")
   29      common = None
   30      assets = {}
   31      for name in identities:
   32          item = json.loads((bundle / name).read_text())
   33          if item["schema"] != 1 or item["name"] != "pixelelated" or item["dirty"] != "no":
   34              raise ValueError("unsupported or dirty build identity")
   35          version = item["release_version"]
   36          num = r"(?:0|[1-9][0-9]*)"
   37          if not re.fullmatch(rf"{num}\.{num}\.{num}(?:-rc\.[1-9][0-9]*)?", version):
   38              raise ValueError("public release version must be MAJOR.MINOR.PATCH[-rc.N]; dev is engineering only")
   39          stamp, commit = item["build_timestamp"], item["build_commit"]
   40          if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z", stamp) or not re.fullmatch(r"[0-9a-f]{40}", commit):
   41              raise ValueError("invalid timestamp or source identity")
   42          datetime.strptime(stamp, "%Y%m%dT%H%M%SZ")
   43          build = f"{version}+{stamp}.g{commit[:12]}"
   44          if build != item["build_version"]:
   45              raise ValueError("build identity fields disagree")
   46          if manifest["inputs"].get("distribution_commit") != commit:
   47              raise ValueError("source commit differs from manifest inputs")
   48          key = (version, stamp, commit, build)
   49          if common is not None and common != key:
   50              raise ValueError("bundle mixes build identities")
   51          common = key
   52          base = item["image_name"]
   53          if not re.fullmatch(r"[A-Z0-9_]+", item["device"]) or not re.fullmatch(r"[a-z0-9_]+", item["arch"]):
   54              raise ValueError("invalid target identity")
   55          prefix = f"pixelelated-{item['device']}.{item['arch']}-{build}"
   56          if base != prefix and not base.startswith(prefix + "-"):
   57              raise ValueError("image name disagrees with build identity")
   58          if name != base + ".identity.json":
   59              raise ValueError("sidecar name disagrees with image identity")
   60          found = False
   61          for asset, record in manifest["files"].items():
   62              if not asset.startswith(base + ".") and not asset.startswith(base + "-"):
   63                  continue
   64              if not asset.endswith((".img.gz", ".tar")):
   65                  continue
   66              checksum = asset + ".sha256"
   67              if checksum not in manifest["files"]:
   68                  raise ValueError("missing artifact checksum: " + asset)
   69              line = (bundle / checksum).read_text().strip()
   70              if line not in (record["sha256"] + "  " + asset, record["sha256"] + " *" + asset):
   71                  raise ValueError("checksum file disagrees with manifest: " + asset)
   72              assets[asset] = record
   73              assets[checksum] = manifest["files"][checksum]
   74              found = True
   75          if not found:
   76              raise ValueError("identity has no firmware assets")
   77          assets[name] = manifest["files"][name]
   78      firmware = {n for n in manifest["files"] if n.endswith((".img.gz", ".tar"))}
   79      if firmware != {n for n in assets if n.endswith((".img.gz", ".tar"))}:
   80          raise ValueError("bundle contains firmware without matching identity")
   81      # Inspect the actual final assets on every preparation. A detached receipt or
   82      # selected default-file report cannot substitute for reading these bytes (#565).
   83      # The gate has no network, publication or repair path; unavailable readers and
   84      # unsupported layouts refuse preparation. Keep the prepare-only contract.
   85      gate = Path(__file__).resolve().with_name("pixelelated-state-check")
   86      state_checks = {}
   87      for asset in sorted(firmware):
   88          try:
   89              with subprocess.Popen([sys.executable, "-B", str(gate), "--payload", str(bundle / asset)],
   90                                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
   91                                    text=True, start_new_session=True) as checked:
   92                  try:
   93                      output, _ = checked.communicate(timeout=900)
   94                  finally:
   95                      if checked.poll() is None:
   96                          os.killpg(checked.pid, signal.SIGKILL)
   97                          checked.communicate()
   98          except (OSError, subprocess.SubprocessError):
   99              raise ValueError("selected-state inspection could not complete") from None
  100          try:
  101              report = json.loads(output)
  102          except (ValueError, TypeError):
  103              raise ValueError("selected-state inspection produced no valid report") from None
  104          if (checked.returncode != 0 or not isinstance(report, dict) or report.get("schema") != 1 or
  105                  report.get("policy") != "pixelelated-selected-state-v1" or
  106                  report.get("mode") != "clean-image" or report.get("status") != "pass" or
  107                  report.get("error_count") != 0 or report.get("blocked_count") != 0):
  108              # Do not forward child stderr or a failed artifact's values/diagnostics.
  109              raise ValueError("selected-state inspection refused a firmware asset")
  110          state_checks[asset] = report
  111      # Detect changed bundle bytes during inspection; no new credential-derived
  112      # digest is emitted by the gate. The existing candidate-store identity remains.
  113      subprocess.run([str(store), "verify", str(bundle)], check=True, stdout=sys.stderr)
  114      version, stamp, commit, build = common
  115      prerelease = "-" in version
  116      return {"schema": 1, "repository": "pixelelated/distribution",
  117              "bundle_sha256": bundle.name, "release_version": version,
  118              "build_version": build, "target_commitish": commit,
  119              "tag": "v" + version,
  120              "title": "pixelelated " + version,
  121              "prerelease": prerelease, "draft": True, "assets": assets,
  122              "publication_performed": False, "qualification": "not assessed",
  123              "selected_state_inspection": state_checks,
  124              "remaining_gates": ["unused immutable tag and recorded RC allocation", "candidate qualification", "source/licence custody",
  125                                  "credential surfaces outside selected-state policy", "named publication approval"]}
  126  
  127  
  128  def main():
  129      parser = argparse.ArgumentParser(description=__doc__)
  130      parser.add_argument("--prepare", type=Path, required=True, metavar="BUNDLE")
  131      args = parser.parse_args()
  132      try:
  133          print(json.dumps(prepare(args.prepare.resolve()), indent=2, sort_keys=True))
  134      except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
  135          print("release preparation: " + str(error), file=sys.stderr)
  136          return 1
  137      return 0
  138  
  139  
  140  if __name__ == "__main__":
  141      sys.exit(main())
  142  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/README.md

```
    1  # Guarded swap reclamation on serval
    2  
    3  Host maintenance for #410/D-INFRA-015. It is not included in a handheld image.
    4  The owner authorizes one fixed operation before a build: recycle the existing
    5  `/swap.img` when less than20% is free. Default preflight remains read-only.
    6  
    7  The helper requires root ownership and safe modes for itself, its directories,
    8  the swapfile and lock. It refuses extra arguments, other swap targets, multiple
    9  active swaps, non-default fstab activation options, an inactive swapfile,
   10  unknown observations and a changed file/configuration. It requires available
   11  RAM equal to used swap plus16GiB and refuses builders, compilers, watchers or
   12  QEMU guests. It takes an exclusive lock and repeats memory/job checks before
   13  mutation. Healthy swap is a no-op. It does not stop unrelated processes.
   14  The lock lives directly in root-owned `/run`, outside writable `/run/lock`.
   15  Serval's observed automatic priority is -1; other negative priorities are
   16  refused for administrator review, rather than assumed portable. Explicit
   17  nonnegative priorities are preserved using `swapon --priority`.
   18  
   19  Only absolute `/usr/sbin/swapoff -- /swap.img` and corresponding `swapon` are
   20  run, with a fixed environment. Active state, size and priority are read back.
   21  Normal command failures and handled SIGINT/SIGTERM/SIGHUP paths attempt
   22  reactivation before returning an error. Termination may wait for the current
   23  command's120second timeout. SIGKILL/power loss cannot run process cleanup.
   24  Memory observations are snapshots, not reservations against unrelated work.
   25  
   26  ## Installation
   27  
   28  Review `reclaim-swap`, `install`, the generated policy and the retained tests.
   29  The installer requires administrator authentication and is scoped to serval's
   30  `max` account (uid1000). It copies the standalone helper as root:root0755 to
   31  `/usr/local/sbin/pixelelated-reclaim-swap`, installs root:root0440 policy at
   32  `/etc/sudoers.d/zz-pixelelated-reclaim-swap`, and validates the complete sudoers
   33  configuration, and requires the normal direct `/etc/sudoers.d` include.
   34  Validation failure attempts to restore both prior files and
   35  reports any incomplete rollback with administrator recovery required. A
   36  failed restoration of one file does not skip the other or final validation. Concurrent
   37  installers/reclaimers share one lock. No swap operation occurs during install.
   38  
   39  The filename places the one-command exception after `zz-fleet-hardening`.
   40  Sudo-rs uses the last matching rule. The installer refuses later active
   41  include files or directives after the include, and migrates only an unchanged
   42  older `pixelelated-reclaim-swap` entry. It does not modify fleet policy.
   43  Successful parsing and installed checksums alone do not prove effective
   44  permission: verify the noninteractive busy refusal before calling setup ready.
   45  
   46  The sole added permission is:
   47  
   48  ```text
   49  max ALL=(root) NOPASSWD: NOSETENV: /usr/local/sbin/pixelelated-reclaim-swap --reclaim
   50  ```
   51  
   52  Serval's sudo-rs0.2.13 does not implement command-digest specifications; its
   53  real `visudo` rejected the first proposed policy. Root ownership and modes
   54  enforce the boundary. The installer records/verifies exact SHA256 values;
   55  the policy's hash comment is a receipt, not an enforced digest matcher.
   56  Python uses `-I` to ignore caller module paths and Python environment options.
   57  The installer itself is never granted passwordless access.
   58  
   59  From the reviewed folder, the administrator runs:
   60  
   61  ```bash
   62  sudo /usr/bin/python3 -I tools/host-maintenance/install
   63  ```
   64  
   65  Use the exact immutable staged path supplied with the release of this host
   66  tool when working from a frozen build checkout. Do not install from an old
   67  checkout. A later helper update requires another reviewed administrator
   68  installation. Re-running a completed installation is safe; an interrupted
   69  installation must be verified/reinstalled before claiming it succeeded.
   70  
   71  ## Before a future build
   72  
   73  Run from a checkout carrying the new preflight, **before** starting its watcher:
   74  
   75  ```bash
   76  tools/build-preflight --reclaim-swap
   77  ```
   78  
   79  Missing helper, missing authorization, refused guards or failed readback leave
   80  preflight nonzero. No password prompt is opened. If guests need stopping, use
   81  the separately authorized stop procedure and wait for exit before reclamation;
   82  `--stop-vms` and `--reclaim-swap` cannot be combined. Never recycle swap during
   83  an active build or VM run. A successful preflight does not prevent swap filling
   84  again; keep supervising actual RAM pressure and package activity.
   85  Zero active swap is also a failed preflight, including a later invocation
   86  after unsuccessful reactivation. The helper never silently activates it.
   87  
   88  ## Recovery and verification
   89  
   90  If reactivation cannot be verified, an administrator inspects `/proc/swaps`
   91  and restores this existing swapfile with `/usr/sbin/swapon /swap.img` if it is
   92  inactive. Never reformat it or run `swapoff -a` as a fallback. Retain the error
   93  and verify active state/priority before resuming. No timer retries failures.
   94  
   95  `python3 -I tools/host-maintenance/test-swap-reclaim` exercises the production
   96  guard/recovery functions with isolated observations and command doubles. The
   97  preflight integration tests replace only the installed helper path in a
   98  temporary script copy and use fake memory/sudo commands; actual host swap and
   99  sudoers are untouched. A memory-guard-removed negative control must fail.
  100  These tests are not a real kernel recycle or installation proof. Keep those
  101  later host readbacks separately scoped.
  102  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/admission-test-fixture.py

```
    1  """Synthetic host-only admission inputs. Never authorizes production allocation."""
    2  import importlib.machinery
    3  import importlib.util
    4  import json
    5  import subprocess
    6  from pathlib import Path
    7  
    8  
    9  def load(path, name='admission_fixture_module'):
   10      loader=importlib.machinery.SourceFileLoader(name,str(path))
   11      spec=importlib.util.spec_from_loader(loader.name,loader)
   12      mod=importlib.util.module_from_spec(spec);loader.exec_module(mod);return mod
   13  
   14  
   15  def prepare_fixture(root, source):
   16      folder=root/'tools/host-maintenance';folder.mkdir(exist_ok=True)
   17      for name in ['build-admission','retention-report']:
   18          (folder/name).write_bytes((source/'tools/host-maintenance'/name).read_bytes())
   19      kept=root/'kept';kept.mkdir();(kept/'measurement.json').write_text('{"synthetic_required_bytes":1048576}\n')
   20      for args in [['init','-q'],['add','tools','scripts','Makefile'],['-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic admission fixture']]:
   21          subprocess.run(['git',*args],cwd=root,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
   22      mod=load(folder/'build-admission')
   23      budget={'name':'fixture','terms_bytes':{'growth':1048576},'basis':'synthetic 1MiB test allowance; no compilation',
   24              'evidence':[{'path':str(kept/'measurement.json'),'sha256':mod.digest(kept/'measurement.json')}]}
   25      plan={'volume':str(root),'scan_roots':[str(root)],'reference_stores':[], 'protected':[str(kept)],'candidates':[],'builds':[budget]}
   26      rp=root/'retention-plan.json';rp.write_text(json.dumps(plan))
   27      report={'schema':1,'utc':mod.utc(),'result':'REPORT_COMPLETE','deletion_performed':False,'inventory':{'errors':[]},
   28              'plan_sha256':mod.digest(rp),'tool_sha256':mod.digest(folder/'retention-report'),
   29              'protected':[{'path':str(kept),'identity':mod.path_identity(kept)}],
   30              'builds':[dict(budget,required_bytes=1048576,fits_now=True)]}
   31      rr=root/'retention-report.json';rr.write_text(json.dumps(report))
   32      ap={'checkout':str(root),'retention_plan':str(rp),'retention_report':str(rr),'stage':'fixture',
   33          'profiles':[{'PROJECT':'ROCKNIX','DEVICE':'GENERIC_X64','ARCH':'x86_64'}],
   34          'outputs':[{'path':str(root/'build.fixture'),'issue':493,'kind':'build-cache','release_when':'synthetic fixture result accepted'}]}
   35      af=root/'admission-plan.json';af.write_text(json.dumps(ap));receipt=root/'admission.json';mod.prepare(af,receipt)
   36      return mod,af,receipt
   37  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/build-admission

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Require a current, single-use retention/capacity admission before compilation.
    5  
    6  This tool registers reservations and consumes completion evidence. It NEVER deletes
    7  build outputs, changes permissions, stops processes, or runs privileged commands.
    8  """
    9  import argparse
   10  import contextlib
   11  import datetime
   12  import fcntl
   13  import hashlib
   14  import json
   15  import os
   16  import re
   17  from pathlib import Path
   18  import stat
   19  import subprocess
   20  import sys
   21  import time
   22  import uuid
   23  
   24  MAX_AGE = 900
   25  
   26  
   27  def require(value, message):
   28      if not value:
   29          raise ValueError(message)
   30  
   31  
   32  def digest(path):
   33      with Path(path).open('rb') as f:
   34          return hashlib.file_digest(f, 'sha256').hexdigest()
   35  
   36  
   37  def read(path):
   38      return json.loads(Path(path).read_text())
   39  
   40  
   41  def write(path, data, exclusive=False):
   42      path = Path(path)
   43      text = json.dumps(data, indent=2, sort_keys=True) + '\n'
   44      if exclusive:
   45          with path.open('x') as f:
   46              f.write(text)
   47      else:
   48          temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
   49          with temp.open('x') as f:
   50              f.write(text)
   51              f.flush()
   52              os.fsync(f.fileno())
   53          temp.replace(path)
   54  
   55  
   56  def utc():
   57      return datetime.datetime.now(datetime.timezone.utc).isoformat()
   58  
   59  
   60  def path_identity(path):
   61      p = Path(path)
   62      require(p.is_absolute() and p.resolve() == p, 'path must be absolute without symlink ancestors')
   63      s = p.lstat()
   64      require(stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode), 'unsupported path type')
   65      return dict(device=s.st_dev, inode=s.st_ino, size=s.st_size,
   66                  mtime_ns=s.st_mtime_ns, allocated_bytes=s.st_blocks * 512,
   67                  uid=s.st_uid, links=s.st_nlink, mode=s.st_mode)
   68  
   69  
   70  def source_state(root):
   71      def git(*args):
   72          return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.PIPE)
   73      return {'head': git('rev-parse', 'HEAD').decode().strip(),
   74              'tracked_diff_sha256': hashlib.sha256(git('diff', '--binary', 'HEAD', '--')).hexdigest()}
   75  
   76  
   77  def registry_for(root):
   78      common = subprocess.check_output(['git', 'rev-parse', '--path-format=absolute', '--git-common-dir'],
   79                                       cwd=root, text=True, stderr=subprocess.PIPE).strip()
   80      return Path(common) / 'pixelelated-build-admission'
   81  
   82  
   83  @contextlib.contextmanager
   84  def registry(path):
   85      path = Path(path)
   86      path.mkdir(mode=0o700, exist_ok=True)
   87      require(not path.is_symlink() and path.stat().st_uid == os.getuid(), 'invalid registry owner/path')
   88      with (path / 'lock').open('a') as lock:
   89          fcntl.flock(lock, fcntl.LOCK_EX)
   90          file = path / 'jobs.json'
   91          data = read(file) if file.exists() else {'schema': 1, 'generation': 0, 'jobs': {}}
   92          require(data.get('schema') == 1 and isinstance(data.get('jobs'), dict), 'invalid registry')
   93          yield data
   94          write(file, data)
   95  
   96  
   97  def evidence(items):
   98      require(isinstance(items, list) and items, 'retained evidence is required')
   99      for item in items:
  100          path_identity(item['path'])
  101          require(digest(item['path']) == item['sha256'], 'retained evidence changed: ' + item['path'])
  102  
  103  
  104  def current(plan):
  105      root = Path(plan['checkout'])
  106      path_identity(root)
  107      require(root.is_dir(), 'checkout must exist')
  108      retention_plan = Path(plan['retention_plan'])
  109      report_path = Path(plan['retention_report'])
  110      path_identity(retention_plan); path_identity(report_path)
  111      rp, report = read(retention_plan), read(report_path)
  112      require(report['schema'] == 1 and report['result'] == 'REPORT_COMPLETE', 'retention report incomplete')
  113      require(not report['deletion_performed'] and not report['inventory']['errors'], 'retention report refused/unresolved')
  114      require(report['plan_sha256'] == digest(retention_plan), 'retention plan changed')
  115      tool = Path(__file__).with_name('retention-report')
  116      require(report['tool_sha256'] == digest(tool), 'retention report tool changed')
  117      age = time.time() - datetime.datetime.fromisoformat(report['utc']).timestamp()
  118      require(0 <= age <= MAX_AGE, 'retention report expired or from the future')
  119      volume = Path(rp['volume']); volume_id = path_identity(volume)
  120      require(root.stat().st_dev == volume_id['device'], 'checkout and budget volume differ')
  121      require(report['protected'] and len(report['protected']) == len(rp['protected']), 'protected identities missing')
  122      require({x['path'] for x in report['protected']} == set(rp['protected']), 'protected scope changed')
  123      for row in report['protected']:
  124          require(path_identity(row['path']) == row['identity'], 'protected identity changed: ' + row['path'])
  125      for item in rp['candidates']:
  126          require(path_identity(item['path']) == item['identity'], 'retirement candidate changed')
  127      matches = [b for b in rp['builds'] if b['name'] == plan['stage']]
  128      rows = [b for b in report['builds'] if b['name'] == plan['stage']]
  129      require(len(matches) == len(rows) == 1, 'exactly one matching build stage required')
  130      budget, observed = matches[0], rows[0]
  131      terms = budget['terms_bytes']
  132      require(terms and all(type(v) is int and v >= 0 for v in terms.values()), 'invalid budget')
  133      need = sum(terms.values())
  134      require(need > 0 and budget['basis'].strip(), 'positive measured budget and basis required')
  135      evidence(budget['evidence'])
  136      require(observed['fits_now'] is True and observed['terms_bytes'] == terms
  137              and observed['required_bytes'] == need, 'retention budget refused or changed')
  138      holds = plan['outputs']
  139      require(isinstance(holds, list) and holds, 'owned outputs and release conditions required')
  140      seen = set()
  141      for h in holds:
  142          p = Path(h['path'])
  143          require(p.is_absolute() and p.resolve() == p and str(p) not in seen, 'invalid/duplicate output path')
  144          seen.add(str(p))
  145          require(type(h['issue']) is int and h['issue'] > 0 and h['release_when'].strip(), 'output needs issue and release condition')
  146          parent = p if p.exists() else p.parent
  147          require(parent.is_dir() and parent.stat().st_dev == volume_id['device'], 'output is outside measured volume')
  148          require(h['kind'] in ['build-cache', 'firmware', 'qa-scratch'], 'invalid output classification')
  149      profiles = plan['profiles']
  150      require(isinstance(profiles, list) and profiles, 'explicit build profiles required')
  151      for profile in profiles:
  152          require(set(profile) == {'PROJECT', 'DEVICE', 'ARCH'} and all(isinstance(v, str) and v for v in profile.values()), 'invalid build profile')
  153      s = os.statvfs(volume)
  154      return {'checkout': str(root), 'source': source_state(root), 'profiles': profiles,
  155              'volume': str(volume), 'volume_device': volume_id['device'],
  156              'required_bytes': need, 'available_bytes': s.f_bavail * s.f_frsize,
  157              'retention_plan_sha256': digest(retention_plan), 'retention_report_sha256': digest(report_path),
  158              'outputs': holds, 'registry': str(registry_for(root)),
  159              'container_checkout': plan.get('container_checkout', str(root))}
  160  
  161  
  162  def prepare(plan_path, output):
  163      plan_path = Path(plan_path).resolve(strict=True)
  164      plan = read(plan_path); state = current(plan)
  165      with registry(state['registry']) as jobs:
  166          reserved = sum(j['required_bytes'] for j in jobs['jobs'].values()
  167                         if j['state'] != 'consumed' and j['volume_device'] == state['volume_device'])
  168          require(state['available_bytes'] >= state['required_bytes'] + reserved, 'insufficient space after existing reservations')
  169          row = {'schema': 1, 'id': uuid.uuid4().hex, 'utc': utc(), 'plan': str(plan_path),
  170                 'plan_sha256': digest(plan_path), 'state': state,
  171                 'registry_generation': jobs['generation'], 'reserved_bytes': reserved,
  172                 'tool_sha256': digest(__file__)}
  173          write(output, row, exclusive=True)
  174      return row
  175  
  176  
  177  def admit(receipt_path, root, run, environment, docker=False):
  178      receipt_path = Path(receipt_path).resolve(strict=True)
  179      receipt = read(receipt_path)
  180      require(receipt['schema'] == 1 and receipt['tool_sha256'] == digest(__file__), 'admission schema/tool changed')
  181      age = time.time() - datetime.datetime.fromisoformat(receipt['utc']).timestamp()
  182      require(0 <= age <= MAX_AGE, 'admission expired or from the future')
  183      require(digest(receipt['plan']) == receipt['plan_sha256'], 'admission plan changed')
  184      state = current(read(receipt['plan'])); expected = receipt['state']
  185      require(state['checkout'] == str(root.resolve()), 'admission belongs to a different checkout')
  186      require({k:v for k,v in state.items() if k != 'available_bytes'} ==
  187              {k:v for k,v in expected.items() if k != 'available_bytes'}, 'admission state changed')
  188      redirected = Path(environment.get('BUILD_DIR', str(root)))
  189      if docker:
  190          require(str(redirected) == state['container_checkout'], 'Docker checkout differs from measured mount contract')
  191      else:
  192          require(redirected.resolve() == root.resolve() or any(
  193              redirected.resolve() == Path(h['path']) for h in state['outputs']),
  194              'redirected BUILD_DIR is not a declared output')
  195      require(any(all(not environment.get(k) or environment[k] == v for k,v in p.items())
  196                  for p in state['profiles']), 'build profile is outside admission')
  197      if len(state['profiles']) == 1:
  198          environment.update(state['profiles'][0])
  199      with registry(state['registry']) as jobs:
  200          require(receipt['id'] not in jobs['jobs'], 'admission has already been used')
  201          require(jobs['generation'] == receipt['registry_generation'], 'registry changed; prepare a new admission')
  202          reserved = sum(j['required_bytes'] for j in jobs['jobs'].values()
  203                         if j['state'] != 'consumed' and j['volume_device'] == state['volume_device'])
  204          require(state['available_bytes'] >= state['required_bytes'] + reserved, 'current capacity no longer fits')
  205          row = dict(state, id=receipt['id'], state='running', run=str(run), admitted=utc(),
  206                     receipt_sha256=digest(receipt_path), runner_pid=os.getpid(),
  207                     submission_owner=environment.get('PIXELELATED_SUBMISSION_OWNER'),
  208                     pid_namespace=os.stat('/proc/self/ns/pid').st_ino,
  209                     runner_start=Path('/proc/self/stat').read_text().rsplit(')',1)[1].split()[19])
  210          write(run / 'admission.json', row, exclusive=True)
  211          write(run / 'admission-input.json', receipt, exclusive=True)
  212          plan = read(receipt['plan'])
  213          write(run / 'admission-plan.json', plan, exclusive=True)
  214          write(run / 'retention-plan.json', read(plan['retention_plan']), exclusive=True)
  215          write(run / 'retention-report.json', read(plan['retention_report']), exclusive=True)
  216          jobs['jobs'][row['id']] = row; jobs['generation'] += 1
  217      return row
  218  
  219  
  220  def nested(root, run, environment):
  221      row = read(run / 'admission.json')
  222      require(not (run / 'runner-result.json').exists(), 'admitted run has already ended')
  223      require(source_state(root) == row['source'], 'nested source differs from admission')
  224      require(any(all(environment.get(k) == v for k,v in p.items())
  225                  for p in row['profiles']), 'nested profile is outside admission')
  226      return row
  227  
  228  
  229  def finish(run, command_code, monitor_code, runner_code):
  230      write(run / 'runner-result.json', {'utc': utc(), 'command_rc': command_code,
  231                                        'monitor_rc': monitor_code, 'runner_rc': runner_code}, exclusive=True)
  232  
  233  
  234  def exited(pid):
  235      p = Path('/proc') / str(pid) / 'cmdline'
  236      try:
  237          require(not p.read_bytes(), 'recorded process is still live: ' + str(pid))
  238      except FileNotFoundError:
  239          pass
  240  
  241  
  242  def consume(run, evidence_path):
  243      # Run in the host namespace; inaccessible /proc state raises, never succeeds.
  244      run = Path(run).resolve(strict=True)
  245      row = read(run / 'admission.json'); proof = read(evidence_path)
  246      require(os.stat('/proc/self/ns/pid').st_ino == row['pid_namespace'], 'consume from the original host PID namespace')
  247      require(proof['run'] == str(run) and proof['disposition'] in ['qualified', 'failed-investigated'], 'wrong completion evidence')
  248      evidence(proof['evidence'])
  249      require(proof['outputs'] == row['outputs'], 'retained output dispositions changed')
  250      rc = read(run / 'runner-result.json')
  251      require(type(proof['expected_rc']) is int and rc['runner_rc'] == proof['expected_rc'], 'unexpected original result')
  252      require(int((run/'build.rc').read_text()) == rc['command_rc'], 'original command rc changed')
  253      require((run/'build.status').read_text().startswith('state:       finished\n'), 'watcher has no terminal status')
  254      require(rc['monitor_rc'] == 0, 'watcher failed; keep reservation for investigation')
  255      require((proof['disposition'] == 'qualified') == (rc['runner_rc'] == 0), 'failure cannot be called qualified')
  256      pids = [row['runner_pid']]
  257      for name in ['build.pid','command.pid','watcher.pid','build.status.pid']:
  258          if (run/name).exists():pids.append(int((run/name).read_text()))
  259      if row['submission_owner']:
  260          owner=Path(row['submission_owner']);launch=read(owner/'launcher-result.json')
  261          require(launch['runner_returncode'] == rc['runner_rc'] == int((owner/'tool-wrapper.rc').read_text()), 'launcher result mismatch')
  262          pids.append(launch['pid'])
  263      for pid in set(pids):exited(pid)
  264      if (run/'command.pid').exists():
  265          group = int((run/'command.pid').read_text())
  266          for p in Path('/proc').glob('[0-9]*/stat'):
  267              try:
  268                  fields = p.read_text().rsplit(')',1)[1].split()
  269                  require(int(fields[2]) != group or fields[0] == 'Z', 'command process group still has live children')
  270              except FileNotFoundError:
  271                  pass
  272      with registry(row['registry']) as jobs:
  273          job=jobs['jobs'][row['id']]
  274          require(job['run'] == str(run), 'registry run mismatch')
  275          if job['state'] == 'consumed':
  276              require(job['evidence_sha256'] == digest(evidence_path), 'different evidence for consumed run')
  277              return job
  278          job.update(state='consumed', consumed=utc(), evidence_sha256=digest(evidence_path),
  279                     original_result=rc, deleted_bytes=0, outputs_held=True)
  280          jobs['generation'] += 1
  281          write(run/'admission-consumed.json',job,exclusive=True)
  282      return job
  283  
  284  
  285  # Only this reviewed launcher's exclusive wrapper write ordering is recoverable.
  286  COLLISION_LAUNCHER_SHA256 = '3777c68fb2677775550183f8bacdb860d7e1e477ebac4e923beda63beba8e88e'
  287  COLLISION_STAGES = ['clean-dolphin-sa', 'build-dolphin-sa', 'build-emulationstation', 'image']
  288  
  289  
  290  def recovery_processes():
  291      """Error-aware PID/parent/group/session census; no privileged FD claim."""
  292      rows = []
  293      for directory in Path('/proc').iterdir():
  294          if not directory.name.isascii() or not directory.name.isdigit():
  295              continue
  296          try:
  297              raw = (directory / 'stat').read_text()
  298          except (FileNotFoundError, ProcessLookupError):
  299              try:
  300                  directory.stat()
  301              except (FileNotFoundError, ProcessLookupError):
  302                  continue
  303              raise ValueError('stat unavailable for present PID ' + directory.name)
  304          prefix, separator, tail = raw.rpartition(')')
  305          fields = tail.split()
  306          require(separator and prefix.split(' (', 1)[0] == directory.name and len(fields) >= 20,
  307                  'malformed process identity')
  308          rows.append(dict(pid=int(directory.name), ppid=int(fields[1]), pgid=int(fields[2]),
  309                           sid=int(fields[3]), start_ticks=int(fields[19]), state=fields[0]))
  310      return rows
  311  
  312  
  313  def recovery_containers():
  314      """A successful daemon census, never an arbitrary failed inspect as absence."""
  315      result = subprocess.run(['docker', 'container', 'ls', '--all', '--no-trunc', '--format', '{{.ID}}'],
  316                              capture_output=True, text=True, timeout=15, check=True)
  317      require(not result.stderr.strip(), 'container census diagnostic is ambiguous')
  318      ids = result.stdout.splitlines()
  319      require(all(re.fullmatch('[0-9a-f]{64}', item) for item in ids) and len(set(ids)) == len(ids),
  320              'invalid container census')
  321      return set(ids)
  322  
  323  
  324  def consume_reporting_failure(run, evidence_path, failure_path):
  325      """Settle custody for the exact #597 producer/report collision; never qualify it."""
  326      run, evidence_path, failure_path = map(lambda p: Path(p).resolve(strict=True),
  327                                           [run, evidence_path, failure_path])
  328      path_identity(run); path_identity(evidence_path); path_identity(failure_path)
  329      row, proof, failure = read(run / 'admission.json'), read(evidence_path), read(failure_path)
  330      root = Path(row['checkout']); owner = Path(row['submission_owner'])
  331      path_identity(root); path_identity(owner)
  332      require(run.parent == root / '.build-runs' and row['run'] == str(run), 'wrong original run path')
  333      require(row['registry'] == str(registry_for(root)), 'wrong original registry')
  334      require(os.stat('/proc/self/ns/pid').st_ino == row['pid_namespace'], 'recover from original host PID namespace')
  335      require(source_state(root) == row['source'], 'original source changed')
  336      require(proof['run'] == str(run) and proof['disposition'] == 'failed-investigated'
  337              and type(proof['expected_rc']) is int and proof['expected_rc'] == 0,
  338              'reporting failure requires investigated disposition with original runner0')
  339      require(proof['outputs'] == row['outputs'], 'retained output dispositions changed')
  340      evidence(proof['evidence'])
  341      require(any(x['path'] == str(failure_path) and x['sha256'] == digest(failure_path)
  342                  for x in proof['evidence']), 'acceptance must bind launcher failure evidence')
  343      require(failure['schema'] == 1 and failure['reason'] == 'exclusive-wrapper-receipt-collision'
  344              and failure['run'] == str(run) and failure['admission_id'] == row['id']
  345              and failure['owner'] == str(owner) and failure['source'] == row['source']
  346              and failure['pid_namespace'] == row['pid_namespace'], 'wrong launcher failure binding')
  347      require(failure['original_launcher_returncode'] is None and failure['qualification'] is False,
  348              'unknown launcher wait status must not be invented or qualified')
  349      provenance = failure['coordinator_provenance']
  350      require(provenance['action'] == 'premature-wrapper-receipt-write'
  351              and provenance['receipt_path'] == str(owner / 'tool-wrapper.rc')
  352              and provenance['receipt_is_launcher_result'] is False
  353              and isinstance(provenance['acknowledgment'], str) and provenance['acknowledgment'].strip(),
  354              'explicit coordinator collision provenance required')
  355      evidence(failure['originals'])
  356      indexed = {item['path']: item['sha256'] for item in failure['originals']}
  357      require(len(indexed) == len(failure['originals']), 'duplicate original evidence path')
  358      def original(path):
  359          require(str(path) in indexed and digest(path) == indexed[str(path)], 'missing/changed original: ' + str(path))
  360          return path
  361      def obj(path):
  362          return read(original(path))
  363      def number(path):
  364          text = original(path).read_text()
  365          require(re.fullmatch('[0-9]+\n?', text) is not None, 'invalid original number: ' + str(path))
  366          return int(text)
  367      original(run / 'admission.json')
  368      rc = obj(run / 'runner-result.json')
  369      require(all(type(rc[k]) is int and rc[k] == 0 for k in ['command_rc', 'monitor_rc', 'runner_rc'])
  370              and number(run / 'build.rc') == number(owner / 'inner.rc') == 0, 'producer did not complete successfully')
  371      status = original(run / 'build.status').read_text()
  372      require(status.startswith('state:       finished\n') and '\noutcome:     rc=0\n' in status,
  373              'watcher has no successful terminal status')
  374      runner = number(run / 'build.pid'); command = number(run / 'command.pid')
  375      watcher = number(run / 'watcher.pid')
  376      require(runner == row['runner_pid'] and int(row['runner_start']) > 0
  377              and watcher == number(run / 'build.status.pid'), 'recorded process bindings differ')
  378      require(re.search(r'^watcher_pid: '+str(watcher)+r'$', status, re.M)
  379              and re.search(r'^job_pid:     '+str(runner)+r'\s', status, re.M), 'terminal watcher identity differs')
  380      require(not os.path.lexists(owner / 'launcher-result.json'), 'launcher result exists; use ordinary consume')
  381      launcher_source = original(owner / 'watch-build-submit.py')
  382      require(digest(launcher_source) == COLLISION_LAUNCHER_SHA256, 'unsupported launcher source for collision recovery')
  383      collision = original(owner / 'tool-wrapper.rc')
  384      require(path_identity(collision) == failure['collision_identity'], 'conflicting receipt identity changed')
  385      # The collision bytes are retained but NEVER parsed as a launcher return code.
  386      console = original(owner / 'console.log').read_text()
  387      diagnostic = "watch-build-submit: [Errno 17] File exists: '" + str(collision) + "'"
  388      require(console.splitlines()[-1:] == [diagnostic] and console.splitlines().count(diagnostic) == 1,
  389              'missing exact terminal exclusive-wrapper collision diagnostic')
  390      launch, launch_pid = obj(owner / 'launcher-start.json'), obj(owner / 'launcher-pid.json')
  391      submission = obj(owner / 'launcher-submission.json')
  392      require(launch['pid'] == launch_pid['pid'] and int(launch['start_ticks']) > 0
  393              and launch['cwd'] == submission['cwd'] == str(root)
  394              and submission['runner'] == str(root / 'tools/watch-build')
  395              and submission['runner_sha256'] == digest(root / 'tools/watch-build')
  396              and submission['submission_is_not_completion'] is True, 'launcher producer identity differs')
  397      started, result = obj(owner / 'owner-start.json'), obj(owner / 'owner-result.json')
  398      inputs, resources = obj(owner / 'build-inputs.json'), obj(owner / 'resource-result.json')
  399      require(started['pid'] == command and int(started['start_ticks']) > 0
  400              and started['pid_namespace'] == inputs['host_pid_namespace'] == 'pid:['+str(row['pid_namespace'])+']'
  401              and started['source_commit'] == inputs['commit'] == row['source']['head']
  402              and inputs['checkout'] == str(root) and inputs['container_checkout'] == row['container_checkout']
  403              and started['input_sha256'] == digest(owner / 'build-inputs.json'), 'completed producer source/identity differs')
  404      require(set(inputs['helper_sha256']) == {'build-owner.py', 'host-resources.py', 'inner-build.py'}, 'producer helper scope differs')
  405      for name, expected in inputs['helper_sha256'].items():
  406          path_identity(owner / name)
  407          require(digest(owner / name) == expected, 'producer helper changed')
  408      require(result['status'] == resources['status'] == 'PASS' and not result['cleanup'] and not result['signals']
  409              and resources['all_threads_exited'] is True and not resources['errors'], 'producer cleanup/resources unresolved')
  410      require([x['stage'] for x in result['stages']] == COLLISION_STAGES, 'unsupported/incomplete producer stage sequence')
  411      pids = {runner, command, watcher, launch['pid']}; groups = {command, watcher, launch['pid']}; cids = set(); stage_groups = set()
  412      for expected in result['stages']:
  413          stage = expected['stage']; folder = owner / 'stages' / stage
  414          host, inner = obj(folder / 'host-result.json'), obj(folder / 'inner-result.json')
  415          ready, observed = obj(folder / 'inner-ready.json'), obj(folder / 'host-observed.json')
  416          container, host_command = obj(folder / 'container-observed.json'), obj(folder / 'host-command.json')
  417          codes = [host['original_host_make_rc'], inner['original_command_rc'], inner['wrapper_rc']]
  418          require(host == expected and all(type(code) is int and code == 0 for code in codes)
  419                  and host['container_observed'] is True and host['observation_handshake'] is True and not inner['signals'],
  420                  'stage did not complete successfully: ' + stage)
  421          require(inner['stage'] == ready['stage'] == observed['stage'] == host_command['stage'] == stage
  422                  and inner['host_observation_handshake'] == observed and ready['nonce'] == observed['nonce']
  423                  and re.fullmatch('[0-9a-f]{32}', ready['nonce']) is not None, 'stage handshake differs: ' + stage)
  424          cid = container['id']
  425          require(re.fullmatch('[0-9a-f]{64}', cid) is not None and cid == observed['container_id']
  426                  and original(folder / 'container.cid').read_text().strip() == cid and cid not in cids,
  427                  'container identity differs: ' + stage)
  428          require(container['image_id'] == started['builder_image_id']
  429                  and container['image_reference'] == inputs['builder_image'] and container['workdir'] == row['container_checkout']
  430                  and any(x['Source'] == str(root) and x['Destination'] == row['container_checkout'] and x['RW'] is True for x in container['mounts'])
  431                  and any(x['Source'] == str(owner) and x['Destination'] == '/build-owner' and x['RW'] is True for x in container['mounts']),
  432                  'container source/mount provenance differs: ' + stage)
  433          pid = host_command['pid']; require(type(pid) is int and pid > 0 and pid == host_command['process_group'], 'stage group identity differs')
  434          pids.add(pid); groups.add(pid); stage_groups.add(str(pid)); cids.add(cid)
  435      require(set(result['surviving_host_command_groups']) == stage_groups
  436              and all(value == [] for value in result['surviving_host_command_groups'].values()), 'producer groups unresolved')
  437      require(all(type(pid) is int and pid > 0 for pid in pids), 'invalid recorded PID')
  438      with registry(row['registry']) as jobs:
  439          job = jobs['jobs'][row['id']]
  440          require(all(job.get(k) == v for k, v in row.items() if k != 'state'), 'registry admission identity differs')
  441          # Recheck originals and current custody under the reservation lock. Unknown
  442          # or reused PIDs conservatively refuse; no broad root-FD visibility assumed.
  443          evidence(failure['originals']); evidence(proof['evidence'])
  444          require(path_identity(collision) == failure['collision_identity'] and not os.path.lexists(owner / 'launcher-result.json'),
  445                  'launcher reporting state changed')
  446          processes = recovery_processes()
  447          require(not any(x['pid'] in pids or x['ppid'] in pids or x['pgid'] in groups or x['sid'] in groups for x in processes),
  448                  'recorded process, child, group or session remains')
  449          require(not (cids & recovery_containers()), 'recorded container remains')
  450          if job['state'] == 'consumed':
  451              require(job['evidence_sha256'] == digest(evidence_path)
  452                      and job.get('completion_disposition') == 'failed-investigated/reporting-failure'
  453                      and job.get('qualification') is False and job.get('original_launcher_returncode') is None
  454                      and job.get('original_result') == rc
  455                      and job.get('recovery_tool_path') == str(Path(__file__).resolve())
  456                      and job.get('recovery_tool_sha256') == digest(__file__)
  457                      and job['launcher_reporting_failure']['evidence_sha256'] == digest(failure_path)
  458                      and read(run / 'admission-consumed.json') == job, 'different recovery for consumed run')
  459              return job
  460          require(job['state'] == 'running', 'admission is not a running reservation')
  461          job.update(state='consumed', consumed=utc(), evidence_sha256=digest(evidence_path), original_result=rc,
  462                     recovery_tool_path=str(Path(__file__).resolve()), recovery_tool_sha256=digest(__file__),
  463                     completion_disposition='failed-investigated/reporting-failure', qualification=False,
  464                     original_launcher_returncode=None, deleted_bytes=0, outputs_held=True,
  465                     launcher_reporting_failure={'reason':failure['reason'], 'evidence_path':str(failure_path),
  466                         'evidence_sha256':digest(failure_path), 'launcher_source_sha256':COLLISION_LAUNCHER_SHA256,
  467                         'conflicting_receipt_used_as_launcher_result':False},
  468                     recovery_absence={'utc':utc(), 'pid_namespace':row['pid_namespace'], 'pids':sorted(pids),
  469                         'groups_and_sessions':sorted(groups), 'container_ids':sorted(cids),
  470                         'scope':'recorded PID/parent/group/session and successful container-ID census; no root-FD claim'})
  471          jobs['generation'] += 1
  472          write(run / 'admission-consumed.json', job, exclusive=True)
  473      return job
  474  
  475  
  476  def main():
  477      os.umask(0o077)
  478      parser=argparse.ArgumentParser(description=__doc__);subs=parser.add_subparsers(dest='action',required=True)
  479      p=subs.add_parser('prepare');p.add_argument('--plan',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
  480      p=subs.add_parser('consume');p.add_argument('--run',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True)
  481      p=subs.add_parser('consume-reporting-failure');p.add_argument('--run',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);p.add_argument('--launcher-failure-evidence',type=Path,required=True)
  482      args=parser.parse_args()
  483      if args.action=='prepare':r=prepare(args.plan,args.output);print('prepared admission '+r['id'])
  484      elif args.action=='consume-reporting-failure':
  485          r=consume_reporting_failure(args.run,args.evidence,args.launcher_failure_evidence)
  486          print('consumed reporting failure; launcher wait unknown; outputs held; qualification false: '+r['id'])
  487      else:r=consume(args.run,args.evidence);print('consumed original results; retained outputs remain held: '+r['id'])
  488  
  489  
  490  if __name__=='__main__':
  491      try:main()
  492      except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as error:
  493          print('build-admission: '+str(error),file=sys.stderr);sys.exit(2)
  494  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/build-admission.md

```
    1  # Build admission and retained output ownership (#493)
    2  
    3  Native, Docker and ad-hoc compilation requires a fresh, single-use admission.
    4  `watch-build` checks it after the watcher arms and before starting the payload.
    5  Normal native device targets have one outer run covering all their ABI phases;
    6  Docker enters once on the host. Nested entrypoints reuse the admission and check
    7  source and profile. A non-compiling job uses `--record-only`; it cannot be a native
    8  or Docker build entrypoint, and a nested build cannot inherit it as an admission.
    9  This is an operational guard, not a security boundary against someone deliberately
   10  labelling a compiler command as a recording job or bypassing the build tools.
   11  
   12  ## Prepare from the existing report
   13  
   14  Use `retention-report` to create a current report from a measured stage budget,
   15  protected inputs and the explicit reviewed scan scope. Unknown historical trees
   16  still need their separate classification; the admission tool does not crawl or
   17  delete the volume. Use the recording mode for this read-only report job:
   18  
   19  ```sh
   20  tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
   21    --plan /absolute/owner/retention-plan.json --output /absolute/owner/retention-report.json
   22  ```
   23  
   24  Create an admission plan (private, outside tracked source):
   25  
   26  ```json
   27  {
   28    "checkout": "/absolute/frozen-checkout",
   29    "retention_plan": "/absolute/owner/retention-plan.json",
   30    "retention_report": "/absolute/owner/retention-report.json",
   31    "stage": "the exact measured stage name",
   32    "profiles": [
   33      {"PROJECT": "ROCKNIX", "DEVICE": "H700", "ARCH": "arm"},
   34      {"PROJECT": "ROCKNIX", "DEVICE": "H700", "ARCH": "aarch64"}
   35    ],
   36    "outputs": [
   37      {"path": "/absolute/frozen-checkout/build.pixelelated-H700.aarch64",
   38       "issue": 555, "kind": "build-cache",
   39       "release_when": "the immediately queued H700 qualification and required source custody are accepted"}
   40    ]
   41  }
   42  ```
   43  
   44  Enumerate **all** output roots and profiles in the real plan; the example only
   45  illustrates the schema, not a sufficient H700 budget. Supported output kinds are
   46  `build-cache`, `firmware`, and `qa-scratch`. Parent directories must exist on the
   47  measured filesystem. An existing output directory is allowed; protected input
   48  identity checks still apply. A redirected native `BUILD_DIR` must be a declared
   49  output root. Docker's `BUILD_DIR` names the container checkout; set
   50  `container_checkout` in the plan when it differs from the host path. The Docker
   51  mount contract must map the admitted host checkout there, as usual.
   52  
   53  ```sh
   54  python3 -I tools/host-maintenance/build-admission prepare \
   55    --plan /absolute/owner/admission-plan.json --output /absolute/owner/admission.json
   56  export PIXELELATED_BUILD_ADMISSION=/absolute/owner/admission.json
   57  make H700
   58  ```
   59  
   60  For an ad-hoc compile or cache copy, use
   61  `tools/watch-build --admission /absolute/owner/admission.json -- COMMAND`.
   62  For durable submission, pass those runner arguments after
   63  `tools/watch-build-submit --owner FRESH_OWNER --`. A fresh submission owner is
   64  always required. Do not label a compiler or cache copy `--record-only`.
   65  
   66  Both the report and admission expire after15minutes. The guard binds the report
   67  and its producing tool, plan, measurement evidence, protected identities, tracked
   68  source state, checkout, profiles, filesystem and current shared registry generation.
   69  It rechecks `f_bavail` at launch, excluding filesystem reserve, and subtracts
   70  unconsumed reservations on the same filesystem. No planned reclamation is counted
   71  as free space. A changed plan/source/input, unresolved inventory error, refused
   72  budget, changed registry or used admission requires fresh preparation. A report
   73  being written successfully does not make its budget acceptable.
   74  
   75  The registry is shared by Git worktrees in the common Git directory under
   76  `pixelelated-build-admission/`, with a file lock. Reservations are conservative
   77  future byte allowances; existing allocated files are already reflected in available
   78  space. Ordinary host processes outside these tools are not space-reserved. Existing
   79  memory/swap preflight and ongoing pressure monitoring remain required.
   80  
   81  ## Consume completion; retain outputs honestly
   82  
   83  Each admitted `.build-runs/<id>` retains admission/plan/report snapshots, original
   84  command/watcher/runner results and output ownership. A submitted run additionally
   85  requires the launcher's original result and wrapper rc. The reservation persists
   86  until evidence consumption succeeds; a completed compile is not qualification.
   87  
   88  An acceptance JSON names the exact `run`, `expected_rc`, `disposition` (`qualified`
   89  or `failed-investigated`), unchanged `outputs` from `admission.json`, and an
   90  `evidence` list of absolute paths and SHA256s covering the actual qualification
   91  or failure diagnosis. Then run from the **original host PID namespace**:
   92  
   93  ```sh
   94  python3 -I tools/host-maintenance/build-admission consume \
   95    --run /absolute/frozen-checkout/.build-runs/ID --evidence /absolute/owner/acceptance.json
   96  ```
   97  
   98  The consumer checks original results, terminal watcher state, retained evidence,
   99  recorded process exits and surviving command-group members. A lost watcher or
  100  unknown/active process keeps the reservation. Repeating the same accepted evidence
  101  is idempotent; different evidence for a consumed run is refused. An interactive
  102  Docker-shell run must be consumed in its original container namespace before that
  103  container is removed; ordinary host-wrapped Docker builds are preferred. A
  104  container namespace that has disappeared is not proof of individual host exits.
  105  
  106  **Consumption releases the reservation, not the outputs.** Output holds and release
  107  conditions remain recorded; this tool performs no deletion. #493's automatic
  108  qualified-artifact retirement, interrupted-removal reconciliation, complete
  109  historical classification and next-build resource telemetry remain separate open
  110  criteria. No root dependency visibility or automatic cleanup is claimed here.
  111  
  112  Run the synthetic controls with `test-build-admission` and `test-build-monitor` in
  113  this directory. They invoke actual launch wrappers and Makefile routes with small
  114  payloads, synthetic capacity/report inputs, and no compiler, VM or real container.
  115  The earlier historical routing fixture stays unchanged in its QA evidence folder.
  116  
  117  ## Recover the reviewed launcher receipt collision (#597)
  118  
  119  `consume-reporting-failure` is a separate, deliberately narrow custody operation.
  120  Ordinary `consume` is unchanged. It supports the reviewed four-stage engineering
  121  producer (`clean-dolphin-sa`, `build-dolphin-sa`, `build-emulationstation`, `image`)
  122  and exact launcher SHA256
  123  `3777c68fb2677775550183f8bacdb860d7e1e477ebac4e923beda63beba8e88e` only.
  124  It is not an ignore-missing-results option. A different producer or launcher
  125  requires its own reviewed recovery; neither a successful submission nor an
  126  operator-created zero establishes the original launcher's wait status.
  127  
  128  For this collision, preserve the copied launcher, complete console, conflicting
  129  `tool-wrapper.rc` bytes and identity, and all original producer receipts. Do not
  130  write `launcher-result.json` or replace the conflicting file. The terminal console
  131  must contain the exact exclusive-create Errno17 diagnostic for that owner's
  132  wrapper receipt. The final launcher wait status stays unknown; a source-derived
  133  exit2 may be documented separately but is never stored as an original result.
  134  
  135  Create a separate immutable failure JSON with these fields:
  136  
  137  ```json
  138  {
  139    "schema": 1,
  140    "reason": "exclusive-wrapper-receipt-collision",
  141    "run": "/absolute/frozen-checkout/.build-runs/ID",
  142    "admission_id": "the original admission id",
  143    "owner": "/absolute/submission-owner",
  144    "source": {"head": "original full commit", "tracked_diff_sha256": "original hash"},
  145    "pid_namespace": 123456789,
  146    "original_launcher_returncode": null,
  147    "qualification": false,
  148    "coordinator_provenance": {
  149      "action": "premature-wrapper-receipt-write",
  150      "receipt_path": "/absolute/submission-owner/tool-wrapper.rc",
  151      "receipt_is_launcher_result": false,
  152      "acknowledgment": "Explicit account of the operator's premature write."
  153    },
  154    "collision_identity": {"device": 0, "inode": 0, "size": 2, "mtime_ns": 0,
  155      "allocated_bytes": 4096, "uid": 1000, "links": 1, "mode": 33152},
  156    "originals": [{"path": "/absolute/original/file", "sha256": "actual SHA256"}]
  157  }
  158  ```
  159  
  160  The identity object uses `path_identity`'s complete actual values, including
  161  device, inode, mode and nanosecond mtime. The numbers above are illustrative.
  162  Required original hashes cover:
  163  
  164  - Run: `admission.json`, `runner-result.json`, `build.rc`, `build.status`,
  165    `build.pid`, `command.pid`, `watcher.pid`, `build.status.pid`.
  166  - Owner: `watch-build-submit.py`, `console.log`, `launcher-start.json`,
  167    `launcher-pid.json`, `launcher-submission.json`, `tool-wrapper.rc`,
  168    `owner-start.json`, `owner-result.json`, `resource-result.json`, `inner.rc`,
  169    `build-inputs.json`. The three producer helper files are additionally checked
  170    against the original `build-inputs.json` helper hashes.
  171  - Each of the four stage directories: `host-result.json`, `inner-result.json`,
  172    `inner-ready.json`, `host-observed.json`, `container-observed.json`,
  173    `host-command.json`, `container.cid`.
  174  
  175  Additional original submission and diagnosis evidence may be retained in the
  176  same list. Missing or changed originals, symlinked paths, a changed source,
  177  nonterminal watcher, nonzero/noninteger result, inconsistent nonce/container
  178  identity or unresolved resource/cleanup result refuse consumption. The new
  179  acceptance file uses the existing schema with `expected_rc: 0`, unchanged
  180  outputs, and `disposition: "failed-investigated"`; its evidence list must bind
  181  the failure JSON by absolute path and SHA256. This preserves runner0 separately
  182  from the reporting failure.
  183  
  184  ```sh
  185  python3 -I tools/host-maintenance/build-admission consume-reporting-failure \
  186    --run /absolute/frozen-checkout/.build-runs/ID \
  187    --evidence /absolute/recovery-owner/acceptance.json \
  188    --launcher-failure-evidence /absolute/recovery-owner/launcher-failure-evidence.json
  189  ```
  190  
  191  Run from the original host PID namespace, after the whole producer has ended.
  192  Under the existing registry lock, recovery rehashes the originals and requires
  193  all named PIDs, direct children, process groups and sessions to be absent. It
  194  conservatively refuses even reused PIDs or zombies. A successful bounded Docker
  195  container-ID census must exclude all four exact original CIDs. Unreadable process
  196  state, daemon errors or diagnostic output do not mean absence. This checks the
  197  recorded process/container custody; it makes no whole-host root-FD visibility
  198  claim and does not stop any process/container or delete any output.
  199  
  200  The consumed record retains the unchanged original runner result and records
  201  `completion_disposition: "failed-investigated/reporting-failure"`,
  202  `qualification: false`, `original_launcher_returncode: null`, the failure
  203  evidence path/hash and known launcher source hash. `recovery_tool_path` and
  204  `recovery_tool_sha256` identify the actual reviewed recovery implementation;
  205  `recovery_absence` records the namespace and exact PID/group/CID sets checked.
  206  Outputs remain held with zero deleted bytes. Identical evidence through the same
  207  tool is idempotent; altered evidence or recovery semantics refuses. A later
  208  artifact verifier must explicitly accept this nonqualified reporting-failure
  209  record while preserving every independent product/artifact check. Recovery
  210  alone is not firmware qualification, an RC gate or a reason to relabel the
  211  original submission successful.
  212  
  213  The added `test-build-admission` controls use temporary fake originals/registry,
  214  mocked process and container observations, and the real recovery logic. They
  215  never consume a production reservation or contact Docker. Existing ordinary
  216  admission/lifecycle controls remain in the same suite.
  217  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/install

```
    1  #!/usr/bin/python3 -I
    2  """One-time administrator installation of the reviewed fixed-action helper."""
    3  import hashlib
    4  import fcntl
    5  import os
    6  from pathlib import Path
    7  import pwd
    8  import stat
    9  import subprocess
   10  import sys
   11  import tempfile
   12  
   13  HELPER = Path('/usr/local/sbin/pixelelated-reclaim-swap')
   14  POLICY = Path('/etc/sudoers.d/zz-pixelelated-reclaim-swap')
   15  LEGACY_POLICY = Path('/etc/sudoers.d/pixelelated-reclaim-swap')
   16  ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'LC_ALL': 'C'}
   17  LOCK = Path('/run/pixelelated-reclaim-swap.lock')
   18  
   19  
   20  def policy(data):
   21      digest = hashlib.sha256(data).hexdigest()
   22      return ('# Managed by pixelelated tools/host-maintenance/install (#410).\n'
   23              '# Only this root-owned helper and literal argument; no environment grants.\n'
   24              f'# Installed helper SHA256 {digest} (receipt; sudo-rs has no digest matcher).\n'
   25              'max ALL=(root) NOPASSWD: NOSETENV: '
   26              '/usr/local/sbin/pixelelated-reclaim-swap --reclaim\n').encode()
   27  
   28  
   29  def secure(path, directory=False):
   30      info = path.lstat()
   31      expected = stat.S_ISDIR if directory else stat.S_ISREG
   32      if not expected(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
   33          raise RuntimeError(f'unsafe root installation path: {path}')
   34      if not directory and info.st_nlink != 1:
   35          raise RuntimeError(f'hard-linked installation target: {path}')
   36  
   37  
   38  def stage(target, data, mode):
   39      fd, name = tempfile.mkstemp(prefix='.' + target.name + '-', dir=target.parent)
   40      path = Path(name)
   41      try:
   42          with os.fdopen(fd, 'wb') as stream:
   43              stream.write(data)
   44              stream.flush()
   45              os.fchown(stream.fileno(), 0, 0)
   46              os.fchmod(stream.fileno(), mode)
   47              os.fsync(stream.fileno())
   48          return path
   49      except BaseException:
   50          path.unlink(missing_ok=True)
   51          raise
   52  
   53  
   54  def validate(path):
   55      subprocess.run(['/usr/sbin/visudo', '-c', '-f', str(path)], env=ENV,
   56                     stdin=subprocess.DEVNULL, check=True)
   57  
   58  
   59  def assert_policy_directory_included():
   60      # Installation is intentionally scoped to this host's normal direct include.
   61      # A valid file in an unreferenced directory would grant no permission.
   62      includes = {'@includedir /etc/sudoers.d', '#includedir /etc/sudoers.d'}
   63      if not any(line.strip() in includes for line in Path('/etc/sudoers').read_text().splitlines()):
   64          raise RuntimeError('expected direct /etc/sudoers.d include; administrator review required')
   65  
   66  
   67  def assert_policy_order():
   68      # sudo-rs uses the last matching rule, not the most specific. The normal
   69      # serval fleet policy must precede this one-command exception.
   70      lines = [line.strip() for line in Path('/etc/sudoers').read_text().splitlines()
   71               if line.strip() and (not line.lstrip().startswith('#')
   72                                    or line.lstrip().startswith(('#include ', '#includedir ')))]
   73      if not lines or lines[-1] not in ('@includedir /etc/sudoers.d', '#includedir /etc/sudoers.d'):
   74          raise RuntimeError('policy include must be the final directive; administrator review required')
   75      later = [path.name for path in POLICY.parent.iterdir()
   76               if '.' not in path.name and not path.name.endswith('~')
   77               and os.fsencode(path.name) > os.fsencode(POLICY.name)]
   78      if later:
   79          raise RuntimeError('later sudoers entries could override the fixed grant: ' + ', '.join(sorted(later)))
   80  
   81  
   82  def install(data):
   83      if os.geteuid() != 0:
   84          raise RuntimeError('administrator authentication is required for installation')
   85      if pwd.getpwnam('max').pw_uid != 1000:
   86          raise RuntimeError('expected serval account max with uid1000')
   87      if Path('/proc/sys/kernel/hostname').read_text().strip() != 'serval':
   88          raise RuntimeError('this reviewed installer is scoped to serval')
   89      for path in [Path('/'), Path('/usr'), Path('/usr/local'), HELPER.parent,
   90                   Path('/etc'), POLICY.parent]:
   91          secure(path, directory=True)
   92      for path in [HELPER, POLICY, LEGACY_POLICY]:
   93          if path.exists() or path.is_symlink():
   94              secure(path)
   95      validate(Path('/etc/sudoers'))
   96      assert_policy_directory_included()
   97      assert_policy_order()
   98      old_helper = HELPER.read_bytes() if HELPER.exists() else None
   99      old_policy = POLICY.read_bytes() if POLICY.exists() else None
  100      old_legacy = LEGACY_POLICY.read_bytes() if LEGACY_POLICY.exists() else None
  101      if old_legacy is not None and (old_helper is None or old_legacy != policy(old_helper)):
  102          raise RuntimeError('old helper policy was edited; administrator review required')
  103      new_helper = None
  104      new_policy = None
  105      changed = False
  106      try:
  107          new_helper = stage(HELPER, data, 0o755)
  108          new_policy = stage(POLICY, policy(data), 0o440)
  109          validate(new_policy)
  110          # Both versions permit only the same root-owned fixed action. Policy is
  111          # validated before replacement; a failed final check restores both files.
  112          new_helper.replace(HELPER)
  113          changed = True
  114          new_policy.replace(POLICY)
  115          if old_legacy is not None:
  116              LEGACY_POLICY.unlink()
  117          validate(Path('/etc/sudoers'))
  118          for path, expected, mode in [(HELPER, data, 0o755), (POLICY, policy(data), 0o440)]:
  119              secure(path)
  120              assert path.read_bytes() == expected and stat.S_IMODE(path.stat().st_mode) == mode
  121              print(f'VERIFIED {path} root:{path.stat().st_gid} mode{mode:o} '
  122                    f'sha256:{hashlib.sha256(expected).hexdigest()}')
  123      except BaseException as cause:
  124          if changed:
  125              failures = []
  126              for path, old, mode in [(POLICY, old_policy, 0o440), (HELPER, old_helper, 0o755),
  127                                      (LEGACY_POLICY, old_legacy, 0o440)]:
  128                  rollback = None
  129                  try:
  130                      if old is None:
  131                          path.unlink(missing_ok=True)
  132                      else:
  133                          rollback = stage(path, old, mode)
  134                          rollback.replace(path)
  135                  except BaseException as error:
  136                      failures.append(f'{path}: {error}')
  137                  finally:
  138                      if rollback:
  139                          try:
  140                              rollback.unlink(missing_ok=True)
  141                          except OSError as error:
  142                              failures.append(f'cleanup {rollback}: {error}')
  143              try:
  144                  validate(Path('/etc/sudoers'))
  145              except BaseException as error:
  146                  failures.append(f'final policy validation: {error}')
  147              if failures:
  148                  raise RuntimeError(f'installation failed ({cause}); rollback incomplete: '
  149                                     + '; '.join(failures)
  150                                     + '; administrator must inspect helper and policy') from cause
  151          raise
  152      finally:
  153          if new_helper:
  154              new_helper.unlink(missing_ok=True)
  155          if new_policy:
  156              new_policy.unlink(missing_ok=True)
  157      print('Installed fixed action only; no swap operation was run.')
  158  
  159  
  160  if __name__ == '__main__':
  161      try:
  162          if sys.argv[1:]:
  163              raise RuntimeError('installer accepts no arguments')
  164          source = Path(__file__).absolute().with_name('reclaim-swap')
  165          data = source.read_bytes()
  166          if not data.startswith(b'#!/usr/bin/python3 -I\n'):
  167              raise RuntimeError('helper must use isolated system Python')
  168          compile(data, str(source), 'exec')
  169          if os.geteuid() != 0:
  170              raise RuntimeError('administrator authentication is required for installation')
  171          secure(LOCK.parent, directory=True)
  172          os.umask(0o077)
  173          fd = os.open(LOCK, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
  174          try:
  175              info = os.fstat(fd)
  176              if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o077 or info.st_nlink != 1:
  177                  raise RuntimeError('unsafe lock file')
  178              fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
  179              install(data)
  180          finally:
  181              os.close(fd)
  182      except (OSError, RuntimeError, AssertionError, subprocess.SubprocessError) as error:
  183          print('INSTALL FAILED: ' + str(error), file=sys.stderr)
  184          sys.exit(1)
  185  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/reclaim-swap

```
    1  #!/usr/bin/python3 -I
    2  """Reclaim only serval's existing /swap.img before a build (#410).
    3  
    4  No caller-controlled paths, thresholds, subprocesses or environment settings.
    5  The installed, root-owned copy is the only privileged entry point.
    6  """
    7  import fcntl
    8  import os
    9  from pathlib import Path
   10  import signal
   11  import stat
   12  import subprocess
   13  import sys
   14  
   15  TARGET = Path('/swap.img')
   16  INSTALLED = Path('/usr/local/sbin/pixelelated-reclaim-swap')
   17  LOCK = Path('/run/pixelelated-reclaim-swap.lock')
   18  RESERVE_KIB = 16 * 1024 * 1024
   19  ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'LC_ALL': 'C'}
   20  SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
   21  PENDING_SIGNAL = None
   22  
   23  
   24  class Refused(RuntimeError):
   25      pass
   26  
   27  
   28  class Interrupted(RuntimeError):
   29      pass
   30  
   31  
   32  def trusted(path, directory=False, private=False):
   33      info = path.lstat()
   34      kind = stat.S_ISDIR if directory else stat.S_ISREG
   35      if not kind(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
   36          raise Refused(f'unsafe ownership, type or writable mode: {path}')
   37      if not directory and info.st_nlink != 1:
   38          raise Refused(f'hard-linked file refused: {path}')
   39      if private and info.st_mode & 0o077:
   40          raise Refused(f'private mode required: {path}')
   41      return info
   42  
   43  
   44  def swap_state():
   45      lines = Path('/proc/swaps').read_text().splitlines()
   46      if not lines or lines[0].split() != ['Filename', 'Type', 'Size', 'Used', 'Priority']:
   47          raise Refused('cannot parse /proc/swaps header')
   48      rows = []
   49      for line in lines[1:]:
   50          fields = line.split()
   51          if len(fields) != 5:
   52              raise Refused('cannot parse /proc/swaps row')
   53          name, kind = fields[:2]
   54          try:
   55              size, used, priority = map(int, fields[2:])
   56          except ValueError as error:
   57              raise Refused('invalid swap counters') from error
   58          if size <= 0 or not 0 <= used <= size or not -32768 <= priority <= 32767:
   59              raise Refused('invalid swap counters or priority')
   60          rows.append((name, kind, size, used, priority))
   61      if len(rows) > 1 or (rows and rows[0][:2] != (str(TARGET), 'file')):
   62          raise Refused('only one active swapfile, /swap.img, is supported')
   63      return rows[0] if rows else None
   64  
   65  
   66  def available_kib():
   67      values = []
   68      for line in Path('/proc/meminfo').read_text().splitlines():
   69          if line.startswith('MemAvailable:'):
   70              fields = line.split()
   71              if len(fields) != 3 or fields[2] != 'kB' or not fields[1].isdigit():
   72                  raise Refused('invalid MemAvailable observation')
   73              values.append(int(fields[1]))
   74      if len(values) != 1:
   75          raise Refused('missing or duplicate MemAvailable observation')
   76      return values[0]
   77  
   78  
   79  def assert_idle():
   80      # Require the host process view. Container/sandbox PID views miss other jobs.
   81      if Path('/proc/1/comm').read_text().strip() != 'systemd':
   82          raise Refused('host systemd process namespace required')
   83      builders = {'make', 'gmake', 'ninja', 'cc', 'c++', 'cc1', 'cc1plus', 'gcc', 'g++',
   84                  'clang', 'clang++', 'collect2', 'lto1', 'cargo', 'rustc', 'rust-lld',
   85                  'ld', 'ld.bfd', 'ld.gold', 'ld.lld', 'mold'}
   86      for proc in Path('/proc').glob('[0-9]*'):
   87          try:
   88              words = (proc / 'cmdline').read_bytes().split(b'\0')
   89          except (FileNotFoundError, ProcessLookupError):
   90              continue  # Process exited during the observation.
   91          except OSError as error:
   92              raise Refused(f'cannot inspect process {proc.name}') from error
   93          names = [os.fsdecode(word).rsplit('/', 1)[-1] for word in words[:3] if word]
   94          if not names:
   95              continue
   96          compiler = names[0] in builders or names[0].endswith(('-gcc', '-g++', '-clang', '-clang++'))
   97          guest = names[0].startswith('qemu-system-')
   98          watched = 'watch-build' in names or 'watch-job' in names
   99          if compiler or guest or watched:
  100              raise Refused(f'active build, compiler, watcher or VM: PID {proc.name}')
  101  
  102  
  103  def file_identity():
  104      trusted(Path('/'), directory=True)
  105      info = trusted(TARGET, private=True)
  106      if info.st_size < 4096:
  107          raise Refused('swapfile is unexpectedly small')
  108      return info.st_dev, info.st_ino, info.st_size
  109  
  110  
  111  def assert_default_activation():
  112      # /proc/swaps exposes priority but not discard/other activation flags.
  113      # Limit this helper to the reviewed default host configuration.
  114      rows = [line.split() for line in Path('/etc/fstab').read_text().splitlines()
  115              if line.strip() and not line.lstrip().startswith('#')]
  116      selected = [row for row in rows if row[0] == str(TARGET)]
  117      if (len(selected) != 1 or len(selected[0]) != 6 or
  118              selected[0][1:3] != ['none', 'swap'] or selected[0][3] not in ('sw', 'defaults') or
  119              selected[0][4:] != ['0', '0']):
  120          raise Refused('only the reviewed default /swap.img fstab activation is supported')
  121  
  122  
  123  def headroom(row):
  124      available = available_kib()
  125      required = row[3] + RESERVE_KIB
  126      if available < required:
  127          raise Refused(f'need {required} KiB available RAM; observed {available} KiB')
  128  
  129  
  130  def command(argv):
  131      result = subprocess.run(argv, env=ENV, stdin=subprocess.DEVNULL,
  132                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
  133                              text=True, timeout=120, check=False)
  134      if result.returncode:
  135          raise Refused(f'{Path(argv[0]).name} failed with exit {result.returncode}')
  136  
  137  
  138  def recycle():
  139      identity = file_identity()
  140      before = swap_state()
  141      if before is None:
  142          raise Refused('/swap.img must already be active; use administrator recovery if inactive')
  143      if (before[2] - before[3]) * 5 >= before[2]:
  144          print('READY: swap has at least 20% free; no change')
  145          return
  146      assert_default_activation()
  147      if before[4] < -1:
  148          raise Refused('negative swap priority differs from reviewed serval configuration')
  149      assert_idle()
  150      headroom(before)
  151      # Re-read immediately before mutation; headroom is a snapshot, not a reservation.
  152      current = swap_state()
  153      if current is None or current[:3] != before[:3] or current[4] != before[4]:
  154          raise Refused('swap configuration changed during checks')
  155      headroom(current)
  156      assert_idle()
  157      if file_identity() != identity:
  158          raise Refused('swapfile changed during checks')
  159      if PENDING_SIGNAL:
  160          raise Interrupted(f'interrupted by signal {PENDING_SIGNAL} before mutation')
  161      print('Reclaiming /swap.img with 16 GiB RAM reserve', flush=True)
  162      try:
  163          command(['/usr/sbin/swapoff', '--', str(TARGET)])
  164      finally:
  165          # Handled termination cannot interrupt our reactivation attempt. SIGKILL
  166          # and power loss remain outside a process's recovery guarantee.
  167          previous = signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
  168          try:
  169              if file_identity() != identity:
  170                  raise Refused('swapfile changed; administrator recovery required')
  171              active = swap_state()
  172              if active is None:
  173                  args = ['/usr/sbin/swapon']
  174                  if before[4] >= 0:
  175                      args += ['--priority', str(before[4])]
  176                  command(args + ['--', str(TARGET)])
  177              after = swap_state()
  178              if after is None or after[:3] != before[:3] or after[4] != before[4]:
  179                  raise Refused('swap activation/size/priority readback differs')
  180          except BaseException as error:
  181              raise Refused('reactivation could not be verified; administrator must inspect '
  182                            '/proc/swaps and recover with /usr/sbin/swapon /swap.img') from error
  183          finally:
  184              signal.pthread_sigmask(signal.SIG_SETMASK, previous)
  185      if (after[2] - after[3]) * 5 < after[2]:
  186          raise Refused('swap is active but still nearly full; not ready for a build')
  187      if PENDING_SIGNAL:
  188          raise Interrupted(f'interrupted by signal {PENDING_SIGNAL}; swap reactivation verified')
  189      print(f'READY: /swap.img active, priority {after[4]}, {after[2] - after[3]} KiB free')
  190  
  191  
  192  def interrupted(signum, _frame):
  193      # Defer termination until the critical section has restored swap. Raising
  194      # asynchronously here could interrupt subprocess cleanup or mask a failed
  195      # reactivation when the signal mask is restored.
  196      global PENDING_SIGNAL
  197      PENDING_SIGNAL = signum
  198  
  199  
  200  def acquire_lock():
  201      os.umask(0o077)
  202      trusted(LOCK.parent, directory=True)
  203      fd = os.open(LOCK, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
  204      try:
  205          info = os.fstat(fd)
  206          if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o077 or info.st_nlink != 1:
  207              raise Refused('unsafe lock file')
  208          try:
  209              fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
  210          except BlockingIOError as error:
  211              raise Refused('another swap reclamation owns the lock') from error
  212          return fd
  213      except BaseException:
  214          os.close(fd)
  215          raise
  216  
  217  
  218  def main(args):
  219      if args != ['--reclaim']:
  220          raise Refused('only --reclaim is supported; no paths or overrides accepted')
  221      if os.geteuid() != 0:
  222          raise Refused('use sudo -n /usr/local/sbin/pixelelated-reclaim-swap --reclaim')
  223      if Path(__file__).absolute() != INSTALLED:
  224          raise Refused('only the installed helper may run as root')
  225      for directory in (Path('/'), Path('/usr'), Path('/usr/local'), INSTALLED.parent):
  226          trusted(directory, directory=True)
  227      trusted(INSTALLED)
  228      fd = acquire_lock()
  229      try:
  230          for sig in SIGNALS:
  231              signal.signal(sig, interrupted)
  232          recycle()
  233      finally:
  234          os.close(fd)
  235  
  236  
  237  if __name__ == '__main__':
  238      try:
  239          main(sys.argv[1:])
  240      except (Refused, Interrupted, OSError, subprocess.SubprocessError) as error:
  241          print('REFUSED: ' + str(error), file=sys.stderr)
  242          sys.exit(1)
  243  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/retention-report

```
    1  #!/usr/bin/env python3
    2  """Read-only build capacity and completed-QA disk retention report (#461).
    3  
    4  Inputs are an explicit plan, not deletion authority. This tool never removes
    5  files, changes permissions, stops processes or invokes privileged commands.
    6  Only superseded QA disks are eligible; build trees use fork-worktree separately.
    7  """
    8  import argparse
    9  from datetime import datetime, timezone
   10  import hashlib
   11  import json
   12  import os
   13  from pathlib import Path
   14  import stat
   15  import subprocess
   16  import tarfile
   17  import time
   18  
   19  
   20  def digest(path):
   21      with Path(path).open('rb') as stream:
   22          return hashlib.file_digest(stream, 'sha256').hexdigest()
   23  
   24  
   25  def identity(path):
   26      s = Path(path).lstat()
   27      return dict(device=s.st_dev, inode=s.st_ino, size=s.st_size,
   28                  mtime_ns=s.st_mtime_ns, allocated_bytes=s.st_blocks * 512,
   29                  uid=s.st_uid, links=s.st_nlink, mode=s.st_mode)
   30  
   31  
   32  def within(path, root):
   33      return Path(path) == Path(root) or Path(root) in Path(path).parents
   34  
   35  
   36  def strings(value):
   37      if isinstance(value, str):
   38          yield value
   39      elif isinstance(value, list):
   40          for child in value:
   41              yield from strings(child)
   42      elif isinstance(value, dict):
   43          for key, child in value.items():
   44              yield key
   45              yield from strings(child)
   46  
   47  
   48  def source_fixtures(plan):
   49      """Only exact archive members in protected source trees are nonruntime."""
   50      accepted, errors, archives = {}, [], {}
   51      for item in plan.get('source_fixtures', []):
   52          try:
   53              path = Path(item['path'])
   54              if (not any(within(path, p) for p in plan['protected'])
   55                      or any(str(path) == c['path'] for c in plan['candidates'])
   56                      or identity(path) != item['identity'] or path.is_symlink()):
   57                  raise ValueError('fixture is changed, unprotected or a removal candidate')
   58              archive = Path(item['archive'])
   59              key = (str(archive), item['archive_sha256'])
   60              if key not in archives:
   61                  if digest(archive) != item['archive_sha256']:
   62                      raise ValueError('archive digest changed')
   63                  archives[key] = True
   64              with tarfile.open(archive) as source:
   65                  member = source.getmember(item['member'])
   66                  if not member.isfile():
   67                      raise ValueError('archive member is not a regular file')
   68                  stream = source.extractfile(member)
   69                  expected = hashlib.file_digest(stream, 'sha256').hexdigest()
   70              if expected != item['sha256'] or digest(path) != expected:
   71                  raise ValueError('fixture differs from exact archive member')
   72              accepted[str(path)] = item
   73          except (OSError, ValueError, KeyError, tarfile.TarError) as error:
   74              errors.append('source fixture ' + item.get('path', '?') + ': ' + str(error))
   75      return accepted, errors
   76  
   77  
   78  def inventory(plan):
   79      roots = [Path(p) for p in plan['scan_roots']]
   80      if not roots or any(not p.is_absolute() or not p.is_dir() or p.is_symlink() for p in roots):
   81          raise ValueError('scan roots must be explicit existing absolute directories')
   82      if any(not any(within(p, r) for r in roots) for p in plan['reference_stores']):
   83          raise ValueError('reference stores must be inside scanned roots')
   84      fixtures, errors = source_fixtures(plan)
   85      edges, disks, manifests = [], [], []
   86      count = 0
   87      tick = time.monotonic()
   88      targets = {str(Path(c['path'])) for c in plan['candidates']}
   89      if len(targets) != len(plan['candidates']):
   90          raise ValueError('duplicate candidate paths')
   91      for root in roots:
   92          pending = [root]
   93          while pending:
   94              base = pending.pop()
   95              count += 1
   96              try:
   97                  with os.scandir(base) as entries:
   98                      for entry in entries:
   99                          try:
  100                              if entry.is_symlink():
  101                                  target = str(Path(entry.path).resolve())
  102                                  if any(within(target, t) or within(t, target) for t in targets):
  103                                      edges.append(dict(source=entry.path, target=target, kind='symlink'))
  104                                  continue
  105                              if entry.is_dir(follow_symlinks=False):
  106                                  pending.append(entry.path)
  107                                  continue
  108                              name = entry.name
  109                              disk_name = name.endswith(('.qcow2', '.qcow', '.img', '.raw', '.vmdk', '.vdi', '.vhd', '.vhdx'))
  110                              if not disk_name and not name.endswith('.json'):
  111                                  continue
  112                              p = Path(entry.path)
  113                              if not entry.is_file(follow_symlinks=False):
  114                                  errors.append('unclassified special file: ' + str(p))
  115                                  continue
  116                              if str(p) in fixtures:
  117                                  item = fixtures[str(p)]
  118                                  if identity(p) != item['identity'] or digest(p) != item['sha256']:
  119                                      errors.append('source fixture changed during discovery: ' + str(p))
  120                                  continue
  121                              if disk_name:
  122                                  with p.open('rb') as stream:
  123                                      magic = stream.read(4)
  124                                  if magic == b'QFI\xfb' or name.endswith(('.qcow2', '.qcow', '.vmdk', '.vdi', '.vhd', '.vhdx')):
  125                                      disks.append(p)
  126                              if name.endswith('.json') and any(within(p, r) for r in plan['reference_stores']):
  127                                  manifests.append(p)
  128                          except (OSError, RuntimeError) as error:
  129                              errors.append(str(error))
  130              except OSError as error:
  131                  errors.append(str(error))
  132              if time.monotonic() - tick > 10:
  133                  print(f'Inspected {count} directories; {len(disks)} disk paths', flush=True)
  134                  tick = time.monotonic()
  135      disk_rows = []
  136      for n, p in enumerate(disks):
  137          try:
  138              before = identity(p)
  139              run = subprocess.run(['qemu-img', 'info', '--force-share', '--backing-chain',
  140                                    '--output=json', str(p)], capture_output=True, text=True, timeout=30)
  141              if run.returncode:
  142                  raise ValueError(str(p) + ': ' + run.stderr.strip())
  143              chain = json.loads(run.stdout)
  144              if identity(p) != before:
  145                  raise ValueError('disk changed during inspection: ' + str(p))
  146              for row in chain:
  147                  if row.get('format') not in ['qcow2', 'raw']:
  148                      raise ValueError('unclassified disk format: ' + str(p))
  149                  source = Path(row['filename'])
  150                  if not source.is_absolute():
  151                      source = p.parent / source
  152                  backing = row.get('full-backing-filename') or row.get('backing-filename')
  153                  if backing:
  154                      target = Path(backing)
  155                      if not target.is_absolute():
  156                          target = source.parent / target
  157                      edges.append(dict(source=str(source.resolve()), target=str(target.resolve()), kind='qcow-backing'))
  158              disk_rows.append(dict(path=str(p), identity=before, chain=chain))
  159          except (OSError, ValueError, subprocess.TimeoutExpired) as e:
  160              errors.append(str(e))
  161          if n % 25 == 0:
  162              print(f'Inspected {n + 1}/{len(disks)} backing chains', flush=True)
  163      for p in manifests:
  164          try:
  165              if p.stat().st_size > 32 * 1024 * 1024:
  166                  raise ValueError('unclassified oversized store manifest: ' + str(p))
  167              for value in strings(json.loads(p.read_text())):
  168                  if value in targets:
  169                      edges.append(dict(source=str(p), target=value, kind='cross-store-json'))
  170          except (OSError, ValueError) as e:
  171              errors.append(str(e))
  172      active, process_errors = [], []
  173      for entry in Path('/proc').glob('[0-9]*/cmdline'):
  174          try:
  175              argv = entry.read_bytes().split(b'\0')
  176              if not argv[0]:
  177                  continue
  178              pid = int(entry.parent.name)
  179              if pid == os.getpid():
  180                  continue
  181              if Path(os.fsdecode(argv[0])).name.startswith('qemu-system-'):
  182                  active.append(dict(pid=pid, kind='live-qemu', scope='all candidates held'))
  183              for c in plan['candidates']:
  184                  if any(os.fsencode(c['path']) in a or os.fsencode(c['owner']) in a for a in argv):
  185                      active.append(dict(pid=pid, kind='owner-argv', path=c['path']))
  186          except FileNotFoundError:
  187              pass  # Process exited between discovery and read.
  188          except OSError as e:
  189              process_errors.append(str(e))
  190      mounts = []
  191      try:
  192          ids = subprocess.check_output(['docker', 'ps', '-aq'], text=True, timeout=30).split()
  193          for cid in ids:
  194              data = json.loads(subprocess.check_output(['docker', 'inspect', cid], text=True, timeout=30))[0]
  195              for mount in data['Mounts']:
  196                  mounts.append(dict(container=cid, running=data['State']['Running'], source=mount['Source']))
  197      except (OSError, ValueError, subprocess.SubprocessError) as e:
  198          errors.append('container inspection: ' + str(e))
  199      return dict(directories=count, errors=errors + process_errors, disks=disk_rows,
  200                  source_fixtures=list(fixtures.values()),
  201                  references=edges, active=active, container_mounts=mounts,
  202                  scope='All directories under explicit roots; directory symlinks not followed. '
  203                        'QCOW magic in img/raw and named virtual disks; JSON references in explicit stores. '
  204                        'Actual process argv and all container mounts. No whole-host root FD census claimed.')
  205  
  206  
  207  def evaluate(candidate, plan, observed):
  208      path = Path(candidate['path'])
  209      reasons = []
  210      if candidate.get('classification') != 'superseded-qa-disk':
  211          reasons.append('unclassified candidate')
  212      if not any(within(path, r) for r in plan['scan_roots']):
  213          reasons.append('outside scanned roots')
  214      if any(within(path, p) or within(p, path) for p in plan['protected']):
  215          reasons.append('protected identity or ancestor')
  216      if observed['errors']:
  217          reasons.append('unreadable or unclassified dependency inventory')
  218      if any(a.get('path') == str(path) or a['kind'] == 'live-qemu' for a in observed['active']):
  219          reasons.append('active process')
  220      for m in observed['container_mounts']:
  221          if within(path, m['source']) or within(m['source'], path):
  222              reasons.append('container reference: ' + m['container'])
  223      for edge in observed['references']:
  224          if within(edge['target'], path) or within(path, edge['target']):
  225              reasons.append(edge['kind'] + ' reference: ' + edge['source'])
  226      try:
  227          actual = identity(path)
  228          if actual != candidate['identity']:
  229              reasons.append('identity changed')
  230          if not stat.S_ISREG(actual['mode']) or actual['links'] != 1 or actual['uid'] != os.getuid():
  231              reasons.append('not an exclusively owned regular file')
  232          if not any(d['path'] == str(path) and d['chain'][0]['format'] == 'qcow2' for d in observed['disks']):
  233              reasons.append('candidate not classified as QCOW2')
  234          evidence = candidate['evidence']
  235          if not evidence or not candidate.get('superseded_by'):
  236              reasons.append('missing preservation or replacement evidence')
  237          for item in evidence + [candidate['superseded_by']]:
  238              if within(item['path'], candidate['owner']):
  239                  reasons.append('evidence not independently retained')
  240              if digest(item['path']) != item['sha256']:
  241                  reasons.append('retained evidence hash mismatch: ' + item['path'])
  242          replacement = json.loads(Path(candidate['superseded_by']['path']).read_text())
  243          if replacement.get('result') != 'PASS':
  244              reasons.append('replacement qualification not accepted')
  245          cleanup = json.loads(Path(candidate['cleanup_receipt']).read_text())
  246          lifecycle = json.loads(Path(candidate['owner_receipt']).read_text())
  247          if (not cleanup.get('passed') or not lifecycle.get('pids_absent')
  248                  or set(lifecycle['channels']) != {'inner.rc', 'outer.rc', 'tool-wrapper.rc', 'build.rc'}
  249                  or len(set(lifecycle['channels'].values())) != 1):
  250              reasons.append('missing completed owner/cleanup proof')
  251          for pid in lifecycle['pids_absent']:
  252              if Path('/proc', str(pid)).exists():
  253                  reasons.append('recorded owner PID currently exists: ' + str(pid))
  254          # Bind the two authority-bearing receipts to the independently retained set.
  255          for receipt in [candidate['cleanup_receipt'], candidate['owner_receipt']]:
  256              if not any(e['sha256'] == digest(receipt) for e in evidence):
  257                  reasons.append('completion receipt not preserved independently')
  258          sha = digest(path)
  259          if identity(path) != actual:
  260              reasons.append('candidate changed while hashing')
  261      except (OSError, ValueError, KeyError, TypeError) as e:
  262          reasons.append('unreadable or malformed candidate evidence: ' + str(e))
  263          sha = None
  264      return dict(path=str(path), identity=candidate['identity'], sha256=sha,
  265                  eligible=not reasons, rejection_reasons=reasons)
  266  
  267  
  268  def report(plan):
  269      observed = inventory(plan)
  270      rows = [evaluate(c, plan, observed) for c in plan['candidates']]
  271      free = os.statvfs(plan['volume'])
  272      available = free.f_bavail * free.f_frsize
  273      preserved = []
  274      for p in plan['protected']:
  275          preserved.append(dict(path=p, identity=identity(p)))
  276      budgets = []
  277      for budget in plan['builds']:
  278          if not budget['evidence']:
  279              raise ValueError('capacity estimate requires retained measurements')
  280          for evidence in budget['evidence']:
  281              if digest(evidence['path']) != evidence['sha256']:
  282                  raise ValueError('capacity evidence changed')
  283          terms = budget['terms_bytes']
  284          if not terms or any(type(v) is not int or v < 0 for v in terms.values()):
  285              raise ValueError('invalid capacity terms')
  286          need = sum(terms.values())
  287          reclaim = sum(r['identity']['allocated_bytes'] for r in rows if r['eligible'])
  288          budgets.append(dict(name=budget['name'], terms_bytes=terms, required_bytes=need,
  289                              available_bytes=available, fits_now=available >= need,
  290                              eligible_reclaim_bytes=reclaim,
  291                              headroom_after_proposed_bytes=available + reclaim - need,
  292                              basis=budget['basis']))
  293      return dict(utc=datetime.now(timezone.utc).isoformat(), schema=1, deletion_performed=False,
  294                  result='REPORT_COMPLETE', protected=preserved, inventory=observed,
  295                  candidates=rows, builds=budgets, preservation_additional_bytes=0,
  296                  limitations='Evidence is already independently retained. Available bytes exclude filesystem reserve. '
  297                              'A report is not deletion authority; refresh identities, dependencies and active use before execution.')
  298  
  299  
  300  if __name__ == '__main__':
  301      parser = argparse.ArgumentParser(description=__doc__)
  302      parser.add_argument('--plan', type=Path, required=True)
  303      parser.add_argument('--output', type=Path, required=True)
  304      args = parser.parse_args()
  305      plan = json.loads(args.plan.read_text())
  306      result = report(plan)
  307      result['plan_sha256'] = digest(args.plan)
  308      result['tool_sha256'] = digest(__file__)
  309      with args.output.open('x') as stream:
  310          json.dump(result, stream, indent=2); stream.write('\n')
  311      print(json.dumps(dict(result=result['result'], candidates=len(result['candidates']),
  312                            eligible=sum(r['eligible'] for r in result['candidates']),
  313                            errors=len(result['inventory']['errors']), builds=result['builds'])), flush=True)
  314  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/retention-report.md

```
    1  # Read-only retention and capacity reports
    2  
    3  `retention-report` implements the first reporting portion of #461 and
    4  D-INFRA-018. Run it after required qualification and before the next build:
    5  
    6  ```sh
    7  tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
    8    --plan /absolute/review/plan.json --output /absolute/review/report.json
    9  ```
   10  
   11  The output must be new. The tool reads production storage and writes only the
   12  requested report. It has no deletion, permission-changing, process-stopping,
   13  swap or privileged mode. A successful command means the report was produced;
   14  inspect each candidate's `eligible` and `rejection_reasons`, inventory errors
   15  and each build's `fits_now`. A completed report can reject every removal.
   16  
   17  The initial scope is explicitly identified, superseded QA disks. Other object
   18  classes are rejected. Worktree removals still use `tools/fork-worktree` under
   19  their own reviewed scope. A report does not authorize any deletion, and cannot
   20  extend an earlier batch's approval.
   21  
   22  The JSON plan contains:
   23  
   24  - `scan_roots`: existing absolute project storage roots. No directory symlinks
   25    are followed. Read failures remain visible and prevent removal proposals.
   26  - `reference_stores`: preservation stores inside those roots. Any exact
   27    candidate path in their JSON files conservatively counts as a reference,
   28    including unfamiliar schemas. Oversized or unreadable JSON is unresolved.
   29  - `protected`: current and fallback candidate/build roots, upgrade baselines,
   30    sources, licensing inputs, shared cache and required evidence. Their identity
   31    observations are retained. Protection includes descendants and ancestors.
   32  - `volume`: the filesystem whose available bytes must accommodate the build.
   33    Availability uses `f_bavail`; filesystem reserve is excluded.
   34  - `candidates`: exact paths classified as `superseded-qa-disk`, each with its
   35    expected `identity`, owner path, original lifecycle and cleanup receipts,
   36    independent retained evidence paths and SHA256 values, and a hash-bound
   37    `superseded_by` acceptance receipt whose result is `PASS`.
   38  - `builds`: one explicit forecast per scheduled stage, with integer
   39    `terms_bytes`, a written `basis`, and hash-bound measurement `evidence`.
   40    Include independent build/copy, artifacts, QA and operating allowances.
   41    Distinguish measurements from future growth estimates. For sequential
   42    stages, later forecasts include earlier outputs that remain on disk.
   43  - Optional `source_fixtures`: exact protected source files that resemble disk
   44    images but are package test samples. Each names its identity, SHA256, source
   45    archive path and SHA256, and exact regular archive member. The tool compares
   46    the actual member bytes and rechecks the file during discovery. An altered,
   47    unprotected or proposed-for-removal fixture is held. This is an explicit
   48    per-file classification; no source directory or extension is skipped.
   49  
   50  `identity` contains device, inode, size, nanosecond modification time,
   51  allocated bytes, uid, hardlink count and mode, as emitted by the tool's
   52  `identity()` function. Every proposed file is hashed and its identity read
   53  again. Hardlinked, changed, nonregular or differently owned files are held.
   54  
   55  The retained evidence list should cover the complete independently preserved
   56  compact record: logs, source/input identities, reports, frames and failure
   57  evidence. Hashing a receipt alone does not establish that this set is complete;
   58  that selection remains part of the reviewed plan. The tool verifies all listed
   59  bytes and independently retained copies of both completion receipts. Existing
   60  preservation is assumed complete, so additional preservation cost is zero;
   61  perform and verify any additional preservation before forming this plan.
   62  
   63  Dependencies are read from actual QCOW backing chains, relevant symlinks,
   64  hardlink counts and JSON references across preservation stores. QCOW headers
   65  are recognized in `.img`/`.raw` files; explicitly named virtual disks are also
   66  inspected. Unknown formats and failed chain inspection prevent proposals.
   67  A disk that another disk references is held even when both are candidates.
   68  Directory-entry metadata avoids repeated stat calls while retaining traversal
   69  of every directory in the declared roots. The first production run identified
   70  64 small shared-mime-info 2.4 MIME samples; they are classified only against
   71  the override recipe's pinned archive and its exact four members (#490).
   72  
   73  Active-use checks inspect actual host process arguments, recorded owner PIDs,
   74  and all running/stopped container mounts. Any live QEMU holds all candidates.
   75  The report does not claim a root file-descriptor census or coverage of disks
   76  outside the declared project roots. Establish those scope boundaries before
   77  using it for a batch. The isolated controls do not require root:
   78  
   79  ```sh
   80  python3 -I tools/host-maintenance/test-retention-report
   81  ```
   82  
   83  They create actual temporary QCOW files, backing chains, cross-store links,
   84  an owned process, unreadable paths and altered evidence. They assert both
   85  eligible independent files and refusals, and check that no disk is removed.
   86  
   87  Before any later authorized action, refresh the report, retained evidence,
   88  exact file identities and active-use observations. Available space and process
   89  state are snapshots, not reservations. Preserve the approved plan digest and
   90  verify actual recovery and retained inputs after the separate guarded action.
   91  
   92  Native/Docker/ad-hoc build admission now consumes a current report and measured
   93  stage under #493; see [build-admission.md](build-admission.md). A report alone
   94  still cannot start a build or authorize removal.
   95  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/test-build-admission

```
    1  #!/usr/bin/env python3
    2  """Negative admission/lifecycle controls; synthetic host roots, no compiler/VM."""
    3  import copy,importlib.util,json,os,shutil,subprocess,tempfile,datetime,hashlib,types
    4  from pathlib import Path
    5  root=Path(__file__).resolve().parents[2]
    6  spec=importlib.util.spec_from_file_location('fixture',Path(__file__).with_name('admission-test-fixture.py'));helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    7  checks=[]
    8  def check(ok,label):
    9      assert ok,label;checks.append(label);print('PASS '+label,flush=True)
   10  with tempfile.TemporaryDirectory(prefix='pix493-admission-') as tmp:
   11      base=Path(tmp)
   12      def fixture(name):
   13          d=base/name;d.mkdir();(d/'tools').mkdir();(d/'scripts').mkdir()
   14          for x in ['watch-build','watch-job']:shutil.copy2(root/'tools'/x,d/'tools'/x)
   15          shutil.copy2(root/'Makefile',d/'Makefile')
   16          mod,plan,receipt=helper.prepare_fixture(d,root)
   17          env={'PATH':os.environ['PATH'],'HOME':str(d),'LC_ALL':'C','PIXELELATED_BUILD_ADMISSION':str(receipt)}
   18          return d,mod,plan,receipt,env
   19      def run(d,env,cmd=None):
   20          return subprocess.run([str(d/'tools/watch-build'),'--interval','1','--',*(cmd or ['touch','compiler-started'])],cwd=d,env=env,capture_output=True,text=True,timeout=15)
   21      mutations={
   22        'undeclared BUILD_DIR':lambda d,m,p,r,e:e.update(BUILD_DIR=str(d/'unbudgeted')),
   23        'missing receipt':lambda d,m,p,r,e:e.pop('PIXELELATED_BUILD_ADMISSION'),
   24        'expired admission':lambda d,m,p,r,e:m.write(r,dict(m.read(r),utc='2020-01-01T00:00:00+00:00')),
   25        'future admission':lambda d,m,p,r,e:m.write(r,dict(m.read(r),utc='2099-01-01T00:00:00+00:00')),
   26        'changed plan':lambda d,m,p,r,e:p.write_text(p.read_text()+' '),
   27        'changed tracked source':lambda d,m,p,r,e:(d/'Makefile').write_text((d/'Makefile').read_text()+'\n# mutation\n'),
   28        'changed measurement':lambda d,m,p,r,e:(d/'kept/measurement.json').write_text('{}'),
   29        'changed protected directory':lambda d,m,p,r,e:(d/'kept/unreviewed').touch(),
   30        'changed profile':lambda d,m,p,r,e:e.update(DEVICE='H700'),
   31        'refused report':lambda d,m,p,r,e:m.write(d/'retention-report.json',dict(m.read(d/'retention-report.json'),inventory={'errors':['unreadable dependency']})),
   32        'changed registry':lambda d,m,p,r,e:m.write(m.registry_for(d)/'jobs.json',{'schema':1,'generation':1,'jobs':{}}),
   33      }
   34      for name,mutate in mutations.items():
   35          d,m,p,r,e=fixture(name.replace(' ','-'));mutate(d,m,p,r,e);a=run(d,e)
   36          check(a.returncode!=0 and not (d/'compiler-started').exists(),name+' blocks payload')
   37      d,m,p,r,e=fixture('capacity')
   38      real = m.os.statvfs
   39      try:
   40          m.os.statvfs = lambda _:types.SimpleNamespace(f_bavail=0,f_frsize=4096)
   41          try:m.prepare(p,d/'no-space.json');ok=False
   42          except ValueError:ok=True
   43          check(ok and not (d/'no-space.json').exists(),'prepare refuses insufficient current capacity')
   44          active=d/'.build-runs/test-capacity';active.mkdir(parents=True)
   45          try:m.admit(r,d,active,e);ok=False
   46          except ValueError:ok=True
   47          check(ok and not (active/'admission.json').exists(),'launch rechecks capacity after preparation')
   48      finally:m.os.statvfs=real
   49      d,m,p,r,e=fixture('reservation')
   50      reg=m.registry_for(d)/'jobs.json';data=m.read(reg)
   51      data['jobs']['existing']={'state':'running','required_bytes':10**18,'volume_device':d.stat().st_dev}
   52      m.write(reg,data)
   53      try:m.prepare(p,d/'overcommitted.json');ok=False
   54      except ValueError:ok=True
   55      check(ok,'existing unresolved reservations reduce new capacity')
   56      d,m,p,r,e=fixture('positive');a=run(d,e);check(a.returncode==0 and (d/'compiler-started').exists(),'valid admission launches payload')
   57      runs=[x for x in (d/'.build-runs').iterdir() if x.is_dir()];runpath=runs[0];row=m.read(runpath/'admission.json')
   58      check(row['outputs']==m.read(p)['outputs'],'registered output release conditions match plan')
   59      (d/'compiler-started').unlink();a=run(d,e);check(a.returncode!=0 and not (d/'compiler-started').exists(),'consumed admission cannot launch twice')
   60      held=d/'build.fixture';held.mkdir();(held/'keep').write_text('retained cache')
   61      proof={'run':str(runpath),'disposition':'qualified','expected_rc':0,'outputs':row['outputs'],
   62        'evidence':[{'path':str(runpath/'build.log'),'sha256':m.digest(runpath/'build.log')}]}
   63      ep=d/'acceptance.json';m.write(ep,proof)
   64      original_pid=(runpath/'command.pid').read_text()
   65      (runpath/'command.pid').write_text(str(os.getpid()))
   66      try:
   67          try:m.consume(runpath,ep);ok=False
   68          except ValueError:ok=True
   69          check(ok,'live original command prevents consumption')
   70      finally:(runpath/'command.pid').write_text(original_pid)
   71      original_row=m.read(runpath/'admission.json');bad=copy.deepcopy(original_row);bad['pid_namespace']+=1;m.write(runpath/'admission.json',bad)
   72      try:
   73          try:m.consume(runpath,ep);ok=False
   74          except ValueError:ok=True
   75          check(ok,'foreign PID namespace cannot prove completion')
   76      finally:m.write(runpath/'admission.json',original_row)
   77      original_log=(runpath/'build.log').read_bytes();(runpath/'build.log').write_bytes(original_log+b'changed')
   78      try:
   79          try:m.consume(runpath,ep);ok=False
   80          except ValueError:ok=True
   81          check(ok,'changed retained evidence prevents consumption')
   82      finally:(runpath/'build.log').write_bytes(original_log)
   83      c=m.consume(runpath,ep);check(c['state']=='consumed' and (held/'keep').read_text()=='retained cache','consume releases reservation without deleting retained output')
   84      check(m.consume(runpath,ep)==c,'same completion evidence reconciles idempotently')
   85      d,m,p,r,e=fixture('failure');a=run(d,e,['sh','-c','exit 37']);check(a.returncode==37,'actual failure remains 37')
   86      runpath=next(x for x in (d/'.build-runs').iterdir() if x.is_dir());row=m.read(runpath/'admission.json')
   87      proof={'run':str(runpath),'disposition':'qualified','expected_rc':37,'outputs':row['outputs'],'evidence':[{'path':str(runpath/'build.log'),'sha256':m.digest(runpath/'build.log')}]};ep=d/'acceptance.json';m.write(ep,proof)
   88      try:m.consume(runpath,ep);ok=False
   89      except ValueError:ok=True
   90      check(ok,'failed job cannot be relabelled qualified')
   91      proof['disposition']='failed-investigated';m.write(ep,proof);check(m.consume(runpath,ep)['original_result']['command_rc']==37,'investigated failure preserves original result')
   92      d,m,p,r,e=fixture('record-only');e.pop('PIXELELATED_BUILD_ADMISSION')
   93      a=subprocess.run([str(d/'tools/watch-build'),'--record-only','--interval','1','--','true'],cwd=d,env=e,capture_output=True,text=True,timeout=10)
   94      check(a.returncode==0,'explicit recording-only job requires no build allocation')
   95      # An inherited recording parent is not a build admission.
   96      child=d/'nested.sh';child.write_text('#!/bin/sh\nexec ./tools/watch-build --entry -- touch nested-compiler\n');child.chmod(0o755)
   97      a=subprocess.run([str(d/'tools/watch-build'),'--record-only','--interval','1','--',str(child)],cwd=d,env=e,capture_output=True,text=True,timeout=10)
   98      check(a.returncode!=0 and not (d/'nested-compiler').exists(),'recording-only parent cannot admit nested compilation')
   99      # #597: all recovery inputs/processes/containers/registries below are isolated.
  100      # No production registry, container daemon, compiler or VM is accessed.
  101      def recovery_fixture(name):
  102          d,m,p,r,e=fixture('reporting-'+name)
  103          runpath=d/'.build-runs/completed';runpath.mkdir(parents=True)
  104          owner=d/'owner';owner.mkdir()
  105          row=dict(m.read(r)['state'],id='reporting-'+name,state='running',run=str(runpath),
  106                   runner_pid=4102,runner_start='100',submission_owner=str(owner),
  107                   pid_namespace=os.stat('/proc/self/ns/pid').st_ino)
  108          m.write(runpath/'admission.json',row)
  109          m.write(m.registry_for(d)/'jobs.json',{'schema':1,'generation':1,'jobs':{row['id']:copy.deepcopy(row)}})
  110          m.write(runpath/'runner-result.json',dict(command_rc=0,monitor_rc=0,runner_rc=0,utc=m.utc()))
  111          for name,value in [('build.rc',0),('build.pid',4102),('command.pid',4103),('watcher.pid',4104),('build.status.pid',4104)]:
  112              (runpath/name).write_text(str(value)+'\n')
  113          (runpath/'build.status').write_text('state:       finished\nwatcher_pid: 4104\njob_pid:     4102  alive=yes\noutcome:     rc=0\n')
  114          shutil.copy2(root/'tools/watch-build-submit',owner/'watch-build-submit.py')
  115          (owner/'tool-wrapper.rc').write_text('0\n');(owner/'inner.rc').write_text('0\n')
  116          (owner/'console.log').write_text("watch-build-submit: [Errno 17] File exists: '"+str(owner/'tool-wrapper.rc')+"'\n")
  117          m.write(owner/'launcher-start.json',dict(pid=4101,start_ticks='99',cwd=str(d)))
  118          m.write(owner/'launcher-pid.json',dict(pid=4101))
  119          m.write(owner/'launcher-submission.json',dict(cwd=str(d),runner=str(d/'tools/watch-build'),runner_sha256=m.digest(d/'tools/watch-build'),submission_is_not_completion=True))
  120          helpers={}
  121          for name in ['build-owner.py','host-resources.py','inner-build.py']:
  122              (owner/name).write_text('# synthetic producer bytes; never executed\n');helpers[name]=m.digest(owner/name)
  123          ns='pid:['+str(row['pid_namespace'])+']';image='sha256:'+'a'*64
  124          inputs=dict(host_pid_namespace=ns,commit=row['source']['head'],checkout=str(d),container_checkout=str(d),builder_image='fixture@'+image,helper_sha256=helpers)
  125          m.write(owner/'build-inputs.json',inputs)
  126          m.write(owner/'owner-start.json',dict(pid=4103,start_ticks='101',pid_namespace=ns,source_commit=inputs['commit'],input_sha256=m.digest(owner/'build-inputs.json'),builder_image_id=image))
  127          stages=[];groups={};cids=[]
  128          for n,stage in enumerate(m.COLLISION_STAGES):
  129              f=owner/'stages'/stage;f.mkdir(parents=True);cid=str(n+1)*64;cids.append(cid)
  130              host=dict(stage=stage,original_host_make_rc=0,container_observed=True,observation_handshake=True);stages.append(host)
  131              handshake=dict(stage=stage,nonce=str(n+1)*32,container_id=cid)
  132              m.write(f/'host-result.json',host)
  133              m.write(f/'inner-result.json',dict(stage=stage,original_command_rc=0,wrapper_rc=0,signals=[],host_observation_handshake=handshake))
  134              m.write(f/'inner-ready.json',dict(stage=stage,nonce=handshake['nonce'],pid=7))
  135              m.write(f/'host-observed.json',handshake)
  136              m.write(f/'container-observed.json',dict(id=cid,image_id=image,image_reference=inputs['builder_image'],workdir=str(d),mounts=[dict(Source=str(d),Destination=str(d),RW=True),dict(Source=str(owner),Destination='/build-owner',RW=True)]))
  137              m.write(f/'host-command.json',dict(stage=stage,pid=4200+n,process_group=4200+n));groups[str(4200+n)]=[]
  138              (f/'container.cid').write_text(cid+'\n')
  139          m.write(owner/'owner-result.json',dict(status='PASS',stages=stages,cleanup=[],signals=[],surviving_host_command_groups=groups))
  140          m.write(owner/'resource-result.json',dict(status='PASS',all_threads_exited=True,errors=[]))
  141          originals=[f for folder in [runpath,owner] for f in sorted(folder.rglob('*')) if f.is_file()]
  142          failure=dict(schema=1,reason='exclusive-wrapper-receipt-collision',run=str(runpath),admission_id=row['id'],owner=str(owner),source=row['source'],pid_namespace=row['pid_namespace'],original_launcher_returncode=None,qualification=False,coordinator_provenance=dict(action='premature-wrapper-receipt-write',receipt_path=str(owner/'tool-wrapper.rc'),receipt_is_launcher_result=False,acknowledgment='Synthetic operator owns the premature write; no launcher wait was observed.'),collision_identity=m.path_identity(owner/'tool-wrapper.rc'),originals=[])
  143          fp=d/'failure.json';ep=d/'acceptance.json'
  144          proof=dict(run=str(runpath),disposition='failed-investigated',expected_rc=0,outputs=row['outputs'],evidence=[])
  145          def refresh():
  146              failure['originals']=[dict(path=str(f),sha256=m.digest(f)) for f in originals if f.exists()]
  147              m.write(fp,failure);proof['evidence']=[dict(path=str(fp),sha256=m.digest(fp))];m.write(ep,proof)
  148          refresh();m.recovery_processes=lambda:[];m.recovery_containers=lambda:set()
  149          return types.SimpleNamespace(d=d,m=m,run=runpath,owner=owner,row=row,failure=failure,proof=proof,fp=fp,ep=ep,refresh=refresh,cids=cids)
  150      def change_json(f,path,**changes):
  151          f.m.write(path,dict(f.m.read(path),**changes));f.refresh()
  152      def fail_recovery(label,mutate):
  153          f=recovery_fixture(label);mutate(f)
  154          before=(f.m.registry_for(f.d)/'jobs.json').read_bytes()
  155          try:f.m.consume_reporting_failure(f.run,f.ep,f.fp);ok=False
  156          except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError):ok=True
  157          check(ok and (f.m.registry_for(f.d)/'jobs.json').read_bytes()==before and not (f.run/'admission-consumed.json').exists(),'report recovery refuses '+label+' without registry/receipt mutation')
  158      def failure_change(f,**changes):f.failure.update(changes);f.refresh()
  159      def proof_change(f,**changes):f.proof.update(changes);f.refresh()
  160      negatives={
  161        'unrelated-reason':lambda f:failure_change(f,reason='missing-receipt'),
  162        'wrong-run':lambda f:failure_change(f,run=str(f.d)),
  163        'wrong-owner':lambda f:failure_change(f,owner=str(f.d)),
  164        'wrong-source':lambda f:failure_change(f,source={}),
  165        'foreign-namespace':lambda f:failure_change(f,pid_namespace=f.row['pid_namespace']+1),
  166        'invented-launcher-zero':lambda f:failure_change(f,original_launcher_returncode=0),
  167        'qualified-reporting-failure':lambda f:proof_change(f,disposition='qualified'),
  168        'missing-coordinator-provenance':lambda f:failure_change(f,coordinator_provenance={}),
  169        'tampered-original':lambda f:(f.owner/'inner.rc').write_text('37\n'),
  170        'missing-terminal-result':lambda f:(f.run/'runner-result.json').unlink(),
  171        'missing-launcher-source':lambda f:(f.owner/'watch-build-submit.py').unlink(),
  172        'nonzero-runner':lambda f:change_json(f,f.run/'runner-result.json',runner_rc=37),
  173        'nonzero-watcher':lambda f:change_json(f,f.run/'runner-result.json',monitor_rc=1),
  174        'boolean-runner-status':lambda f:change_json(f,f.run/'runner-result.json',runner_rc=False),
  175        'nonterminal-watcher':lambda f:((f.run/'build.status').write_text('state:       running\n'),f.refresh()),
  176        'existing-launcher-result':lambda f:f.m.write(f.owner/'launcher-result.json',{'runner_returncode':0}),
  177        'unrelated-launcher-error':lambda f:((f.owner/'console.log').write_text('watch-build-submit: permission denied\n'),f.refresh()),
  178        'changed-launcher-source':lambda f:((f.owner/'watch-build-submit.py').write_text('# other launcher\n'),f.refresh()),
  179        'changed-collision-identity':lambda f:((f.owner/'tool-wrapper.rc').write_text('0\n'),f.refresh()),
  180        'nonzero-stage':lambda f:change_json(f,f.owner/'stages/image/inner-result.json',wrapper_rc=1),
  181        'boolean-stage-status':lambda f:change_json(f,f.owner/'stages/image/inner-result.json',original_command_rc=False),
  182        'wrong-stage-nonce':lambda f:change_json(f,f.owner/'stages/image/inner-ready.json',nonce='0'*32),
  183        'wrong-stage-cid':lambda f:((f.owner/'stages/image/container.cid').write_text('f'*64+'\n'),f.refresh()),
  184        'unresolved-cleanup':lambda f:change_json(f,f.owner/'owner-result.json',cleanup=['forced']),
  185        'resource-error':lambda f:change_json(f,f.owner/'resource-result.json',errors=['unknown']),
  186        'live-launcher':lambda f:setattr(f.m,'recovery_processes',lambda:[dict(pid=4101,ppid=1,pgid=4101,sid=4101,start_ticks=99)]),
  187        'reused-recorded-pid':lambda f:setattr(f.m,'recovery_processes',lambda:[dict(pid=4101,ppid=1,pgid=9000,sid=9000,start_ticks=999)]),
  188        'live-descendant':lambda f:setattr(f.m,'recovery_processes',lambda:[dict(pid=9000,ppid=4103,pgid=9000,sid=9000)]),
  189        'live-stage-group':lambda f:setattr(f.m,'recovery_processes',lambda:[dict(pid=9000,ppid=1,pgid=4200,sid=9000)]),
  190        'live-launcher-session':lambda f:setattr(f.m,'recovery_processes',lambda:[dict(pid=9000,ppid=1,pgid=9000,sid=4101)]),
  191        'live-container':lambda f:setattr(f.m,'recovery_containers',lambda:{f.cids[0]}),
  192        'unreadable-process-census':lambda f:setattr(f.m,'recovery_processes',lambda:(_ for _ in ()).throw(PermissionError('fixture proc unknown'))),
  193        'failed-daemon-census':lambda f:setattr(f.m,'recovery_containers',lambda:(_ for _ in ()).throw(subprocess.CalledProcessError(1,['docker']))),
  194      }
  195      # This mutation deliberately omits an otherwise unchanged required original.
  196      def missing_original(f):
  197          f.failure['originals']=[x for x in f.failure['originals'] if x['path']!=str(f.run/'build.rc')]
  198          f.m.write(f.fp,f.failure);f.proof['evidence']=[dict(path=str(f.fp),sha256=f.m.digest(f.fp))];f.m.write(f.ep,f.proof)
  199      negatives['missing-original-evidence']=missing_original
  200      def wrong_registry(f,field,value):
  201          path=f.m.registry_for(f.d)/'jobs.json';data=f.m.read(path);data['jobs'][f.row['id']][field]=value;f.m.write(path,data)
  202      negatives['wrong-registry-run']=lambda f:wrong_registry(f,'run',str(f.d))
  203      negatives['wrong-registry-source']=lambda f:wrong_registry(f,'source',{})
  204      for label,mutate in negatives.items():fail_recovery(label,mutate)
  205      f=recovery_fixture('positive')
  206      try:f.m.consume(f.run,f.ep);ok=False
  207      except ValueError:ok=True
  208      check(ok,'ordinary consume still refuses runner0 reporting failure')
  209      original_files={p:p.read_bytes() for folder in [f.run,f.owner] for p in folder.rglob('*') if p.is_file()}
  210      c=f.m.consume_reporting_failure(f.run,f.ep,f.fp)
  211      check(c['state']=='consumed' and c['completion_disposition']=='failed-investigated/reporting-failure' and c['qualification'] is False and c['original_launcher_returncode'] is None and c['original_result']==f.m.read(f.run/'runner-result.json'),'recovery retains original runner0 and unknown launcher separately')
  212      check(c['outputs_held'] is True and c['deleted_bytes']==0 and all(p.read_bytes()==raw for p,raw in original_files.items()),'recovery preserves every original and output hold')
  213      check(f.m.consume_reporting_failure(f.run,f.ep,f.fp)==c,'same reporting failure recovery is idempotent')
  214      old=f.ep.read_text();f.ep.write_text(old+' ')
  215      try:f.m.consume_reporting_failure(f.run,f.ep,f.fp);ok=False
  216      except ValueError:ok=True
  217      check(ok,'different recovery acceptance is refused after consumption')
  218  print(json.dumps({'result':'PASS','checks':len(checks),'cases':checks}))
  219  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/test-build-monitor

```
    1  #!/usr/bin/env python3
    2  """Execute real entrypoint prefixes and Makefile with isolated build payloads."""
    3  import argparse
    4  import importlib.util
    5  import json
    6  import os
    7  from pathlib import Path
    8  import re
    9  import shutil
   10  import signal
   11  import subprocess
   12  import tempfile
   13  import time
   14  
   15  parser = argparse.ArgumentParser()
   16  parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
   17  args = parser.parse_args()
   18  root = args.root.resolve()
   19  helper_spec = importlib.util.spec_from_file_location('admission_test_fixture', Path(__file__).with_name('admission-test-fixture.py'))
   20  helper = importlib.util.module_from_spec(helper_spec)
   21  helper_spec.loader.exec_module(helper)
   22  passed = 0
   23  entries = ('build_distro', 'image', 'build', 'build_compat', 'install')
   24  
   25  
   26  def check(value, label):
   27      global passed
   28      if not value:
   29          raise AssertionError(label)
   30      passed += 1
   31      print('PASS:', label, flush=True)
   32  
   33  
   34  def executable(path, body):
   35      path.write_text(body)
   36      path.chmod(0o755)
   37  
   38  
   39  def wait_for(predicate, seconds=10):
   40      until = time.monotonic() + seconds
   41      while time.monotonic() < until:
   42          result = predicate()
   43          if result:
   44              return result
   45          time.sleep(.025)
   46      raise AssertionError('timed out waiting for fixture state')
   47  
   48  
   49  with tempfile.TemporaryDirectory(prefix='watch-build-394-') as temporary:
   50      base = Path(temporary)
   51      count = 0
   52  
   53      def fixture():
   54          global count
   55          count += 1
   56          d = base / str(count)
   57          d.mkdir()
   58          (d / 'tools').mkdir()
   59          (d / 'scripts').mkdir()
   60          for name in ('watch-build', 'watch-job'):
   61              shutil.copy2(root / 'tools' / name, d / 'tools' / name)
   62          shutil.copy2(root / 'Makefile', d / 'Makefile')
   63          shutil.copy2(root / 'scripts/get_env', d / 'scripts/get_env')
   64          for name in entries:
   65              text = (root / 'scripts' / name).read_text()
   66              marker = 'unset RASTERATOPS_WATCH_EXEC\n'
   67              if marker not in text or 'exec ./tools/watch-build --entry -- "$0" "$@"' not in text:
   68                  raise AssertionError('unmonitored entrypoint: scripts/' + name)
   69              prefix = text[:text.index(marker) + len(marker)]
   70              body = '\nprintf "%s\\n" "fixture-' + name + ':$*:$TEST_ENV"\n'
   71              if name == 'build_distro':
   72                  body += 'make image\n'
   73              elif name == 'image':
   74                  body += './scripts/install fake\n'
   75              elif name == 'install':
   76                  body += './scripts/build fake\n'
   77              executable(d / 'scripts' / name, prefix + body)
   78          helper.prepare_fixture(d, root)
   79          return d
   80  
   81      def environment(d):
   82          # No personal account/environment values enter fixtures or receipts.
   83          return {'PATH': os.environ['PATH'], 'HOME': str(d), 'TEST_ENV': 'retained',
   84                  'LC_ALL': 'C', 'PIXELELATED_BUILD_ADMISSION': str(d/'admission.json')}
   85  
   86      def run(d, command, env=None):
   87          return subprocess.run(command, cwd=d, env=env or environment(d),
   88                                capture_output=True, text=True, timeout=35)
   89  
   90      def only_run(d):
   91          runs = [p for p in (d / '.build-runs').iterdir() if p.is_dir()]
   92          if len(runs) != 1:
   93              raise AssertionError(f'expected one outer run; got {len(runs)}')
   94          return runs[0]
   95  
   96      def finished(d, code):
   97          r = only_run(d)
   98          return ((r / 'build.rc').read_text().strip() == str(code)
   99                  and (r / 'build.status').read_text().startswith('state:       finished\n')
  100                  and (r / 'watch-job').exists())
  101  
  102      d = fixture()
  103      activity = d / 'qa artifacts'
  104      activity.mkdir()
  105      script = d / 'qa.py'
  106      script.write_text('import time\nfrom pathlib import Path\ntime.sleep(1.2)\n'
  107                        'p=Path("qa artifacts/suite")\np.mkdir()\n'
  108                        '(p/"proof.log").write_text("case advanced\\n")\n')
  109      result = run(d, ['./tools/watch-build', '--interval', '1', '--stall-min', '1',
  110                       '--activity-dir', str(activity), '--recursive-activity',
  111                       '--', 'python3', str(script)])
  112      check(result.returncode == 0 and finished(d, 0)
  113            and str(activity / 'suite/proof.log') in (only_run(d) / 'build.status').read_text(),
  114            'shared runner observes nested QA logs and retains terminal result')
  115  
  116      for name in entries:
  117          d = fixture()
  118          result = run(d, ['./scripts/' + name, 'an argument', 'literal;$value'])
  119          check(result.returncode == 0 and finished(d, 0), 'automatic direct entry: ' + name)
  120          check(f'fixture-{name}:an argument literal;$value:retained' in result.stdout,
  121                'arguments and environment preserved: ' + name)
  122          r = only_run(d)
  123          check(r.stat().st_mode & 0o777 == 0o700 and (r / 'build.log').stat().st_mode & 0o777 == 0o600,
  124                'private run and logs: ' + name)
  125  
  126      for target in ('GENERIC_X64', 'image', 'package'):
  127          d = fixture()
  128          result = run(d, ['make', target, 'PACKAGE=fake'])
  129          check(result.returncode == 0 and finished(d, 0), 'native make route: ' + target)
  130  
  131      d = fixture()
  132      mod = helper.load(d / 'tools/host-maintenance/build-admission')
  133      plan = mod.read(d / 'admission-plan.json')
  134      plan['profiles'] = [{'PROJECT':'ROCKNIX','DEVICE':'H700','ARCH':a} for a in ['arm','aarch64']]
  135      mod.write(d / 'admission-plan.json', plan)
  136      mod.prepare(d / 'admission-plan.json', d / 'admission-dual.json')
  137      env = environment(d); env['PIXELELATED_BUILD_ADMISSION'] = str(d / 'admission-dual.json')
  138      result = run(d, ['make', 'H700'], env)
  139      check(result.returncode == 0 and finished(d, 0) and result.stdout.count('fixture-build_distro:') == 2,
  140            'native dual-ABI target shares one admitted run')
  141  
  142      d = fixture()
  143      executable(d / 'scripts/build', '#!/bin/bash\necho unmonitored\n')
  144      negative = subprocess.run(['python3', str(Path(__file__).resolve()), '--root', str(d)],
  145                                capture_output=True, text=True, timeout=10)
  146      check(negative.returncode != 0 and 'unmonitored entrypoint: scripts/build' in negative.stderr,
  147            'routing regression check fails when an entrypoint loses its hook')
  148  
  149      d = fixture()
  150      (d / 'bin').mkdir()
  151      executable(d / 'bin/docker', '''#!/usr/bin/env python3
  152  import os,sys,subprocess,json
  153  from pathlib import Path
  154  if sys.argv[1:]==['--version']:
  155   print('Docker fixture'); sys.exit(0)
  156  a=sys.argv[1:]
  157  if a[0]!='run': raise SystemExit(2)
  158  assert '-e' in a and 'RASTERATOPS_BUILD_RUN' in a
  159  assert os.environ.get('RASTERATOPS_BUILD_RUN')
  160  Path('docker-run.json').write_text(json.dumps({'relative_run':os.environ['RASTERATOPS_BUILD_RUN']}))
  161  at=a.index(os.environ['TEST_DOCKER_IMAGE'])
  162  sys.exit(subprocess.call(a[at+1:]))
  163  ''')
  164      env = environment(d)
  165      env['PATH'] = str(d / 'bin') + ':' + env['PATH']
  166      # This fixture tests routing; the reviewed Makefile owns image identity.
  167      # Preserve the historical fixture and bind this copy to its actual pin.
  168      makefile = (d / 'Makefile').read_text()
  169      image = re.search(r'^docker-%: DOCKER_IMAGE = (\S+)@\$\(DOCKER_IMAGE_DIGEST\)$', makefile, re.M)
  170      digest = re.search(r'^docker-%: DOCKER_IMAGE_DIGEST := (sha256:[0-9a-f]{64})$', makefile, re.M)
  171      assert image and digest, 'fixture cannot resolve the pinned Docker image'
  172      env['TEST_DOCKER_IMAGE'] = image[1] + '@' + digest[1]
  173      result = run(d, ['make', 'docker-GENERIC_X64'], env)
  174      check(result.returncode == 0 and finished(d, 0), 'Docker host runner and inner scripts share one run')
  175      check(not (d / '.env').exists() and json.loads((d / 'docker-run.json').read_text())['relative_run'].startswith('.build-runs/'),
  176            'Docker gets relative mounted run; environment file is removed')
  177      dry = run(d, ['make', '-n', 'docker-shell'], env)
  178      check('./tools/watch-build --docker -- docker run' not in dry.stdout,
  179            'interactive docker-shell does not gain an outer monitor')
  180  
  181      for code in (0, 37):
  182          d = fixture()
  183          result = run(d, ['./tools/watch-build', '--interval', '1', '--',
  184                           'bash', '-c', f'echo out; echo err >&2; exit {code}'])
  185          r = only_run(d)
  186          check(result.returncode == code and finished(d, code), 'actual command exit preserved: ' + str(code))
  187          check('out\nerr\n' in result.stdout and (r / 'build.log').read_text() == 'out\nerr\n',
  188                'console and durable combined output preserved: ' + str(code))
  189  
  190      d = fixture()
  191      env = environment(d)
  192      env['RASTERATOPS_BUILD_RUN'] = '.build-runs/missing'
  193      result = run(d, ['./scripts/build', 'fake'], env)
  194      check(result.returncode != 0 and 'fixture-build' not in result.stdout,
  195            'stale inherited marker cannot bypass monitoring')
  196  
  197      d = fixture()
  198      result = subprocess.run(['./tools/watch-build', '--interval', '1', '--',
  199                               'bash', '-c', 'touch product-file; mkdir product-directory'],
  200                              cwd=d, env=environment(d), capture_output=True,
  201                              preexec_fn=lambda: os.umask(0o022), timeout=10)
  202      check(result.returncode == 0 and (d / 'product-file').stat().st_mode & 0o777 == 0o644
  203            and (d / 'product-directory').stat().st_mode & 0o777 == 0o755,
  204            'private monitor permissions do not change build artifact umask')
  205  
  206      d = fixture()
  207      executable(d / 'tools/watch-job', '#!/bin/sh\nexit 23\n')
  208      result = run(d, ['./tools/watch-build', '--', 'touch', 'should-not-exist'])
  209      check(result.returncode != 0 and not (d / 'should-not-exist').exists(),
  210            'watcher startup failure refuses command launch')
  211  
  212      d = fixture()
  213      result = run(d, ['./tools/watch-build', '--interval', '1', '--', 'bash', '-c',
  214                       'kill -TERM "$(cat "$RASTERATOPS_BUILD_RUN/watcher.pid")"; sleep 1; echo completed'])
  215      r = only_run(d)
  216      check(result.returncode == 125 and (r / 'build.rc').read_text().strip() == '0'
  217            and (r / 'runner-error').exists(), 'lost watcher cannot produce a green monitored run')
  218  
  219      d = fixture()
  220      p = subprocess.Popen(['./tools/watch-build', '--interval', '1', '--', 'sleep', '30'],
  221                           cwd=d, env=environment(d), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  222      try:
  223          wait_for(lambda: list((d / '.build-runs').glob('*/command.pid')) if (d / '.build-runs').exists() else [])
  224          blocked = run(d, ['./tools/watch-build', '--', 'touch', 'second-command'])
  225          check(blocked.returncode != 0 and not (d / 'second-command').exists(),
  226                'one top-level build per worktree')
  227          p.send_signal(signal.SIGTERM)
  228          check(p.wait(timeout=10) == 143 and finished(d, 143), 'termination forwards to child and retains143')
  229      finally:
  230          if p.poll() is None:
  231              p.terminate()
  232              p.wait(timeout=10)
  233  
  234      d = fixture()
  235      executable(d / 'activity.py', '''#!/usr/bin/env python3
  236  import os,time
  237  from pathlib import Path
  238  run=Path(os.environ['RASTERATOPS_BUILD_RUN'])
  239  p=Path(os.environ['BUILD_DIR'])/'build.fixture/.threads/logs'
  240  p.mkdir(parents=True)
  241  (p/'1.log').write_text('[7/10] compiling\\n')
  242  os.utime(run/'build.log',(time.time()-1200,time.time()-1200))
  243  time.sleep(2)
  244  s=(run/'build.status').read_text()
  245  assert 'state:       running' in s and 'activity_progress: [7/10]' in s,s
  246  print('new cold root observed')
  247  ''')
  248      env = environment(d)
  249      env['BUILD_DIR'] = str(d / 'new-external-build-root')
  250      mod = helper.load(d / 'tools/host-maintenance/build-admission')
  251      plan = mod.read(d / 'admission-plan.json')
  252      plan['outputs'][0]['path'] = env['BUILD_DIR']
  253      mod.write(d / 'admission-plan.json', plan)
  254      mod.prepare(d / 'admission-plan.json', d / 'admission-redirect.json')
  255      env['PIXELELATED_BUILD_ADMISSION'] = str(d / 'admission-redirect.json')
  256      result = run(d, ['./tools/watch-build', '--interval', '1', '--', './activity.py'], env)
  257      check(result.returncode == 0 and 'new cold root observed' in result.stdout,
  258            'cold build roots discovered after launch; buffered progress observed')
  259  
  260      d = fixture()
  261      p = subprocess.Popen(['./tools/watch-build', '--interval', '1', '--', 'sleep', '30'],
  262                           cwd=d, env=environment(d), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  263      child_pid = None
  264      try:
  265          paths = wait_for(lambda: list((d / '.build-runs').glob('*/command.pid')) if (d / '.build-runs').exists() else [])
  266          child_pid = int(paths[0].read_text())
  267          p.kill()
  268          p.wait(timeout=5)
  269          r = only_run(d)
  270          wait_for(lambda: 'state:       died\n' in (r / 'build.status').read_text())
  271          check(not (r / 'build.rc').exists(), 'detached monitor records killed runner without inventing result')
  272      finally:
  273          if child_pid is not None:
  274              try:
  275                  os.killpg(child_pid, signal.SIGTERM)
  276              except ProcessLookupError:
  277                  pass
  278          if p.poll() is None:
  279              p.kill()
  280              p.wait()
  281  
  282  print(f'{passed} PASS; 0 FAIL')
  283  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/test-retention-report

```
    1  #!/usr/bin/env python3
    2  """Exercise retention refusals with real temporary QCOW files and processes."""
    3  import copy
    4  import importlib.machinery
    5  import importlib.util
    6  import json
    7  import os
    8  from pathlib import Path
    9  import subprocess
   10  import tarfile
   11  import tempfile
   12  
   13  source = Path(__file__).with_name('retention-report')
   14  loader = importlib.machinery.SourceFileLoader('retention', str(source))
   15  spec = importlib.util.spec_from_loader(loader.name, loader)
   16  mod = importlib.util.module_from_spec(spec)
   17  loader.exec_module(mod)
   18  results = []
   19  with tempfile.TemporaryDirectory(prefix='pixelelated-retention-controls-') as tmp:
   20      root = Path(tmp); owner = root/'owner'; kept = root/'kept'; store = root/'store'
   21      for p in [owner, kept, store]: p.mkdir()
   22      disk = owner/'guest.qcow2'
   23      subprocess.run(['qemu-img','create','-f','qcow2',str(disk),'16M'], check=True, stdout=subprocess.DEVNULL)
   24      ended = subprocess.Popen(['true']); ended.wait()
   25      lifecycle = dict(pids_absent=[ended.pid], channels={n:'0' for n in ['inner.rc','outer.rc','tool-wrapper.rc','build.rc']})
   26      for name, data in [('owner.json',lifecycle),('cleanup.json',{'passed':True})]:
   27          text=json.dumps(data);(owner/name).write_text(text);(kept/name).write_text(text)
   28      (kept/'replacement.json').write_text(json.dumps({'result':'PASS'}))
   29      evidence=[dict(path=str(p),sha256=mod.digest(p)) for p in kept.iterdir()]
   30      candidate=dict(path=str(disk),owner=str(owner),classification='superseded-qa-disk',
   31                     identity=mod.identity(disk), evidence=evidence,
   32                     cleanup_receipt=str(owner/'cleanup.json'),owner_receipt=str(owner/'owner.json'),
   33                     superseded_by=dict(path=str(kept/'replacement.json'),sha256=mod.digest(kept/'replacement.json')))
   34      plan=dict(scan_roots=[str(root)],reference_stores=[str(store)],protected=[str(kept)],candidates=[candidate],
   35                volume=str(root),builds=[dict(name='fixture',terms_bytes={'required':1},
   36                                            evidence=[candidate['superseded_by']],basis='fixture')])
   37      def check(name, expected, changed=None):
   38          current=changed or plan
   39          result=mod.report(current);row=result['candidates'][0]
   40          assert row['eligible']==expected,(name,row)
   41          assert disk.exists() and result['deletion_performed'] is False
   42          results.append(dict(name=name,passed=True,eligible=row['eligible'],reasons=row['rejection_reasons']))
   43      check('eligible independent completed QA disk',True)
   44      other=copy.deepcopy(plan);other['candidates'][0]['classification']='unknown'
   45      check('unclassified candidate',False,other)
   46      disk.chmod(0)
   47      try: check('actual unreadable disk',False)
   48      finally: disk.chmod(0o644)
   49      # Permission changes altered identity; restore the expected observation.
   50      candidate['identity']=mod.identity(disk)
   51      hidden=root/'unreadable';hidden.mkdir();hidden.chmod(0)
   52      try: check('unreadable dependency tree',False)
   53      finally: hidden.chmod(0o755);hidden.rmdir()
   54      child=store/'dependent.qcow2'
   55      subprocess.run(['qemu-img','create','-f','qcow2','-F','qcow2','-b',str(disk),str(child)],check=True,stdout=subprocess.DEVNULL)
   56      check('actual cross-store QCOW backing dependency',False);child.unlink()
   57      link=store/'disk-link';link.symlink_to(disk)
   58      check('cross-store symlink',False);link.unlink()
   59      manifest=store/'objects.json';manifest.write_text(json.dumps({'object':str(disk)}))
   60      check('cross-store JSON reference',False);manifest.unlink()
   61      hard=store/'hardlink';os.link(disk,hard)
   62      check('hardlinked candidate',False);hard.unlink()
   63      sleeper=subprocess.Popen(['python3','-c','import time;time.sleep(60)',str(disk)])
   64      try: check('actual live owner process',False)
   65      finally: sleeper.terminate();sleeper.wait()
   66      other=copy.deepcopy(plan);other['protected'].append(str(owner))
   67      check('protected tree',False,other)
   68      other=copy.deepcopy(plan);other['candidates'][0]['identity']['inode']+=1
   69      check('changed identity',False,other)
   70      receipt=kept/'cleanup.json';before=receipt.read_bytes();receipt.write_text('{}')
   71      try: check('tampered retained evidence',False)
   72      finally: receipt.write_bytes(before)
   73      check('eligible after temporary controls removed',True)
   74      # A truncated real QCOW header forces an inspection error; arbitrary bytes
   75      # can legitimately be detected as a raw image by qemu-img.
   76      sample=kept/'source-sample.qcow2';sample.write_bytes(disk.read_bytes()[:32])
   77      archive=kept/'source.tar.gz'
   78      with tarfile.open(archive,'w:gz') as source_archive:
   79          source_archive.add(sample,arcname='tests/mime-detection/source-sample.qcow2')
   80      item=dict(path=str(sample),identity=mod.identity(sample),sha256=mod.digest(sample),
   81                archive=str(archive),archive_sha256=mod.digest(archive),
   82                member='tests/mime-detection/source-sample.qcow2')
   83      check('unclassified source disk is still held',False)
   84      plan['source_fixtures']=[item]
   85      check('exact protected archive fixture classified',True)
   86      before=sample.read_bytes();sample.write_bytes(before+b'changed')
   87      try: check('changed source fixture rejected',False)
   88      finally: sample.write_bytes(before);item['identity']=mod.identity(sample)
   89      before=archive.read_bytes();archive.write_bytes(before+b'changed')
   90      try: check('changed source archive rejected',False)
   91      finally: archive.write_bytes(before)
   92      other=copy.deepcopy(plan);other['protected']=[]
   93      check('unprotected fixture rejected',False,other)
   94      check('exact fixture remains valid after controls',True)
   95  print(json.dumps(dict(result='PASS',controls=results,tool_sha256=mod.digest(source)),indent=2))
   96  
```

## file, whole, at 8ebaf8daad: tools/host-maintenance/test-swap-reclaim

```
    1  #!/usr/bin/python3 -I
    2  """Isolated guard/recovery tests; never issue real swap commands or install policy."""
    3  import argparse
    4  from contextlib import ExitStack
    5  import importlib.machinery
    6  import importlib.util
    7  import os
    8  from pathlib import Path
    9  import signal
   10  import stat
   11  import subprocess
   12  import tempfile
   13  from types import SimpleNamespace
   14  import unittest
   15  from unittest.mock import patch
   16  
   17  parser = argparse.ArgumentParser()
   18  parser.add_argument('--helper', type=Path, default=Path(__file__).with_name('reclaim-swap'))
   19  args = parser.parse_args()
   20  if os.geteuid() == 0:
   21      parser.error('run the fixture suite unprivileged')
   22  
   23  
   24  def load(name, path):
   25      loader = importlib.machinery.SourceFileLoader(name, str(path))
   26      module = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader))
   27      loader.exec_module(module)
   28      return module
   29  
   30  
   31  helper = load('swap_helper', args.helper)
   32  installer = load('swap_installer', Path(__file__).with_name('install'))
   33  ROW = ('/swap.img', 'file', 8 * 1024 * 1024, 7 * 1024 * 1024, -1)
   34  HEADER = 'Filename Type Size Used Priority\n'
   35  
   36  
   37  class Observations(unittest.TestCase):
   38      def test_activation_flags_are_not_silently_lost(self):
   39          for text in ['/swap.img none swap sw 0 0', '/swap.img none swap defaults 0 0']:
   40              with patch.object(Path, 'read_text', return_value=text):
   41                  helper.assert_default_activation()
   42          for text in ['', '/swap.img none swap sw,discard 0 0', '/swap.img none swap sw 1 0',
   43                       '/swap.img none swap sw 0 0\n/swap.img none swap sw 0 0']:
   44              with self.subTest(text=text), patch.object(Path, 'read_text', return_value=text):
   45                  with self.assertRaises(helper.Refused):
   46                      helper.assert_default_activation()
   47  
   48      def test_lock_excludes_concurrent_reclamation(self):
   49          with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
   50              lock = Path(directory) / 'lock'
   51              stack.enter_context(patch.object(helper, 'LOCK', lock))
   52              stack.enter_context(patch.object(helper, 'trusted'))
   53              stack.enter_context(patch.object(Path, 'lstat', return_value=SimpleNamespace(st_mode=stat.S_IFDIR | 0o700, st_uid=0)))
   54              original = os.fstat
   55              def root_owned(fd):
   56                  info = original(fd)
   57                  return SimpleNamespace(st_mode=info.st_mode, st_uid=0, st_nlink=info.st_nlink)
   58              stack.enter_context(patch.object(helper.os, 'fstat', side_effect=root_owned))
   59              first = helper.acquire_lock()
   60              try:
   61                  with self.assertRaisesRegex(helper.Refused, 'another swap reclamation'):
   62                      helper.acquire_lock()
   63              finally:
   64                  os.close(first)
   65              second = helper.acquire_lock()
   66              os.close(second)
   67  
   68      def test_writable_lock_parent_refused_before_open(self):
   69          def info(path):
   70              mode = 0o755 if str(path) == '/run' else 0o1777
   71              return SimpleNamespace(st_mode=stat.S_IFDIR | mode, st_uid=0)
   72          with patch.object(helper, 'LOCK', Path('/run/writable/lock')), patch.object(Path, 'lstat', info), patch.object(helper.os, 'open', side_effect=AssertionError('unsafe directory reached open')):
   73              with self.assertRaises(helper.Refused):
   74                  helper.acquire_lock()
   75  
   76      def test_swap_exact_and_empty(self):
   77          for text, wanted in [(HEADER + '/swap.img file 8192 8100 -1\n', ('/swap.img', 'file', 8192, 8100, -1)), (HEADER, None)]:
   78              with self.subTest(text=text), patch.object(Path, 'read_text', return_value=text):
   79                  self.assertEqual(helper.swap_state(), wanted)
   80  
   81      def test_swap_malformed_or_other_target_refused(self):
   82          for text in ['', 'wrong header\n', HEADER + '/dev/sda partition 10 9 -1', HEADER + '/other file 10 9 -1',
   83                       HEADER + '/swap.img file 10 9 -1\n/swap.img file 10 9 -1', HEADER + '/swap.img file x 9 -1',
   84                       HEADER + '/swap.img file 0 0 -1', HEADER + '/swap.img file 10 11 -1',
   85                       HEADER + '/swap.img file 10 -1 -1', HEADER + '/swap.img file 10 9 32768']:
   86              with self.subTest(text=text), patch.object(Path, 'read_text', return_value=text):
   87                  with self.assertRaises(helper.Refused):
   88                      helper.swap_state()
   89  
   90      def test_available_ram_missing_or_invalid_refused(self):
   91          for text in ['', 'MemAvailable: -1 kB', 'MemAvailable: 2 MB', 'MemAvailable: 2 kB\nMemAvailable: 3 kB']:
   92              with self.subTest(text=text), patch.object(Path, 'read_text', return_value=text):
   93                  with self.assertRaises(helper.Refused):
   94                      helper.available_kib()
   95          with patch.object(Path, 'read_text', return_value='MemAvailable: 12345 kB\n'):
   96              self.assertEqual(helper.available_kib(), 12345)
   97  
   98      def test_unsafe_ownership_mode_links_and_type_refused(self):
   99          for uid, mode, links in [(1000, stat.S_IFREG | 0o600, 1), (0, stat.S_IFREG | 0o620, 1),
  100                                   (0, stat.S_IFREG | 0o604, 1), (0, stat.S_IFLNK | 0o777, 1),
  101                                   (0, stat.S_IFREG | 0o600, 2)]:
  102              with self.subTest(uid=uid, mode=mode, links=links), patch.object(Path, 'lstat', return_value=SimpleNamespace(st_uid=uid, st_mode=mode, st_nlink=links)):
  103                  with self.assertRaises(helper.Refused):
  104                      helper.trusted(Path('/swap.img'), private=True)
  105  
  106      def test_active_jobs_and_container_namespace_refused(self):
  107          for cmd in [b'/usr/bin/make\0all\0', b'/usr/bin/cc1plus\0', b'/toolchain/x86_64-linux-gnu-g++\0',
  108                      b'/usr/bin/qemu-system-x86_64\0', b'/usr/bin/python3\0/repo/tools/watch-build\0',
  109                      b'/bin/bash\0/repo/tools/watch-job\0']:
  110              with self.subTest(cmd=cmd), patch.object(Path, 'read_text', return_value='systemd\n'), patch.object(Path, 'glob', return_value=[Path('/proc/42')]), patch.object(Path, 'read_bytes', return_value=cmd):
  111                  with self.assertRaisesRegex(helper.Refused, 'PID 42'):
  112                      helper.assert_idle()
  113          with patch.object(Path, 'read_text', return_value='bash\n'):
  114              with self.assertRaisesRegex(helper.Refused, 'namespace'):
  115                  helper.assert_idle()
  116  
  117      def test_idle_process_exit_and_unreadable_process(self):
  118          with patch.object(Path, 'read_text', return_value='systemd\n'), patch.object(Path, 'glob', return_value=[Path('/proc/42')]):
  119              with patch.object(Path, 'read_bytes', return_value=b'/usr/bin/postgres\0'):
  120                  helper.assert_idle()
  121              for disappeared in (FileNotFoundError, ProcessLookupError):
  122                  with patch.object(Path, 'read_bytes', side_effect=disappeared):
  123                      helper.assert_idle()
  124              with patch.object(Path, 'read_bytes', side_effect=PermissionError):
  125                  with self.assertRaises(helper.Refused):
  126                      helper.assert_idle()
  127  
  128      def test_args_nonroot_and_source_copy_cannot_mutate(self):
  129          with patch.object(helper, 'recycle') as mutation:
  130              for argv in [[], ['--reclaim', '/other'], ['--check'], ['--reclaim', '--force']]:
  131                  with self.subTest(argv=argv), self.assertRaises(helper.Refused):
  132                      helper.main(argv)
  133              with patch.object(helper.os, 'geteuid', return_value=1000), self.assertRaises(helper.Refused):
  134                  helper.main(['--reclaim'])
  135              with patch.object(helper.os, 'geteuid', return_value=0), self.assertRaisesRegex(helper.Refused, 'installed'):
  136                  helper.main(['--reclaim'])
  137              mutation.assert_not_called()
  138  
  139      def test_command_uses_fixed_environment_no_shell_and_failure_propagates(self):
  140          with patch.object(helper.subprocess, 'run', return_value=SimpleNamespace(returncode=0)) as run:
  141              helper.command(['/usr/sbin/swapoff', '--', '/swap.img'])
  142              self.assertEqual(run.call_args.args[0], ['/usr/sbin/swapoff', '--', '/swap.img'])
  143              self.assertEqual(run.call_args.kwargs['env'], {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'LC_ALL': 'C'})
  144              self.assertNotIn('shell', run.call_args.kwargs)
  145          with patch.object(helper.subprocess, 'run', return_value=SimpleNamespace(returncode=2)):
  146              with self.assertRaises(helper.Refused):
  147                  helper.command(['/usr/sbin/swapoff', '--', '/swap.img'])
  148  
  149  
  150  class Reclamation(unittest.TestCase):
  151      def setUp(self):
  152          self.stack = ExitStack()
  153          self.addCleanup(self.stack.close)
  154          self.row = ROW
  155          self.calls = []
  156          self.identity = self.stack.enter_context(patch.object(helper, 'file_identity', return_value=(1, 2, 8589934592)))
  157          self.stack.enter_context(patch.object(helper, 'swap_state', side_effect=lambda: self.row))
  158          self.memory = self.stack.enter_context(patch.object(helper, 'available_kib', return_value=32 * 1024 * 1024))
  159          self.idle = self.stack.enter_context(patch.object(helper, 'assert_idle'))
  160          self.stack.enter_context(patch.object(helper, 'assert_default_activation'))
  161          self.stack.enter_context(patch.object(helper, 'PENDING_SIGNAL', None))
  162          self.action = self.stack.enter_context(patch.object(helper, 'command', side_effect=self.command))
  163  
  164      def command(self, argv):
  165          self.calls.append(argv)
  166          if argv[0] == '/usr/sbin/swapoff':
  167              self.row = None
  168          elif argv[0] == '/usr/sbin/swapon':
  169              priority = int(argv[2]) if '--priority' in argv else -1
  170              self.row = (*ROW[:3], 0, priority)
  171          else:
  172              raise AssertionError('unexpected command')
  173  
  174      def test_reclaims_only_one_file_and_restores_priority(self):
  175          helper.recycle()
  176          self.assertEqual(self.calls, [['/usr/sbin/swapoff', '--', '/swap.img'], ['/usr/sbin/swapon', '--', '/swap.img']])
  177          self.assertEqual(self.row, (*ROW[:3], 0, -1))
  178          self.calls.clear()
  179          self.row = (*ROW[:4], 17)
  180          helper.recycle()
  181          self.assertEqual(self.calls[-1], ['/usr/sbin/swapon', '--priority', '17', '--', '/swap.img'])
  182          self.assertEqual(self.row[4], 17)
  183  
  184      def test_healthy_noop_and_inactive_refusal(self):
  185          self.row = (*ROW[:3], 0, -1)
  186          helper.recycle()
  187          self.action.assert_not_called()
  188          self.row = None
  189          with self.assertRaises(helper.Refused):
  190              helper.recycle()
  191          self.action.assert_not_called()
  192  
  193      def test_unrestorable_negative_priority_refuses(self):
  194          self.row = (*ROW[:4], -2)
  195          with self.assertRaisesRegex(helper.Refused, 'negative swap priority'):
  196              helper.recycle()
  197          self.action.assert_not_called()
  198  
  199      def test_insufficient_memory_and_boundary(self):
  200          self.memory.return_value = ROW[3] + helper.RESERVE_KIB - 1
  201          with self.assertRaisesRegex(helper.Refused, 'available RAM'):
  202              helper.recycle()
  203          self.action.assert_not_called()
  204          self.memory.return_value += 1
  205          helper.recycle()
  206          self.assertEqual(len(self.calls), 2)
  207  
  208      def test_second_memory_read_refuses_new_pressure(self):
  209          self.memory.side_effect = [32 * 1024 * 1024, 1]
  210          with self.assertRaises(helper.Refused):
  211              helper.recycle()
  212          self.action.assert_not_called()
  213  
  214      def test_job_started_during_checks_refuses_before_mutation(self):
  215          self.idle.side_effect = [None, helper.Refused('new active build')]
  216          with self.assertRaisesRegex(helper.Refused, 'new active build'):
  217              helper.recycle()
  218          self.action.assert_not_called()
  219  
  220      def test_active_job_and_changed_file_refuse_before_mutation(self):
  221          self.idle.side_effect = helper.Refused('active job')
  222          with self.assertRaises(helper.Refused):
  223              helper.recycle()
  224          self.action.assert_not_called()
  225          self.idle.side_effect = None
  226          self.identity.side_effect = [(1, 2, 8589934592), (1, 3, 8589934592)]
  227          with self.assertRaises(helper.Refused):
  228              helper.recycle()
  229          self.action.assert_not_called()
  230  
  231      def test_failed_swapoff_still_active_is_not_success(self):
  232          self.action.side_effect = helper.Refused('swapoff failed')
  233          with self.assertRaisesRegex(helper.Refused, 'swapoff failed'):
  234              helper.recycle()
  235          self.assertEqual(self.row, ROW)
  236          self.assertEqual(self.action.call_count, 1)
  237  
  238      def test_partial_swapoff_failure_and_interruption_reactivate(self):
  239          for error in [helper.Refused('swapoff failed after deactivation'), helper.Interrupted('cancelled')]:
  240              with self.subTest(error=error):
  241                  self.row, self.calls = ROW, []
  242                  def command(argv):
  243                      self.command(argv)
  244                      if argv[0].endswith('swapoff'):
  245                          raise error
  246                  self.action.side_effect = command
  247                  with self.assertRaises(type(error)):
  248                      helper.recycle()
  249                  self.assertEqual(self.row[3], 0)
  250                  self.assertEqual(len(self.calls), 2)
  251  
  252      def test_failed_swapon_never_reports_success(self):
  253          def command(argv):
  254              if argv[0].endswith('swapon'):
  255                  raise helper.Refused('swapon failed')
  256              self.command(argv)
  257          self.action.side_effect = command
  258          with self.assertRaisesRegex(helper.Refused, 'administrator must inspect'):
  259              helper.recycle()
  260          self.assertIsNone(self.row)
  261  
  262      def test_false_swapon_success_and_priority_drift_refused(self):
  263          for wrong in [None, (*ROW[:3], 0, 9)]:
  264              self.row = ROW
  265              def command(argv):
  266                  self.command(argv)
  267                  if argv[0].endswith('swapon'):
  268                      self.row = wrong
  269              self.action.side_effect = command
  270              with self.assertRaisesRegex(helper.Refused, 'reactivation'):
  271                  helper.recycle()
  272  
  273      def test_signal_acknowledged_only_after_reactivation(self):
  274          def command(argv):
  275              self.command(argv)
  276              if argv[0].endswith('swapoff'):
  277                  helper.interrupted(signal.SIGTERM, None)
  278          self.action.side_effect = command
  279          with self.assertRaisesRegex(helper.Interrupted, 'reactivation verified'):
  280              helper.recycle()
  281          self.assertEqual(self.row[3], 0)
  282          self.assertEqual(len(self.calls), 2)
  283  
  284  
  285  class Preflight(unittest.TestCase):
  286      def setUp(self):
  287          self.directory = tempfile.TemporaryDirectory()
  288          self.addCleanup(self.directory.cleanup)
  289          root = Path(self.directory.name)
  290          self.state = root / 'reclaimed'
  291          self.calls = root / 'calls'
  292          self.helper_path = root / 'installed-helper'
  293          self.script = root / 'build-preflight'
  294          source = Path(__file__).resolve().parents[1] / 'build-preflight'
  295          self.script.write_text(source.read_text().replace('/usr/local/sbin/pixelelated-reclaim-swap', str(self.helper_path)))
  296          fixtures = {
  297              'pgrep': '#!/bin/sh\nexit 1\n',
  298              'free': '''#!/bin/sh
  299  [ "$TEST_MODE" = invalid ] && { echo malformed; exit 0; }
  300  total=8192; used=8191; remaining=1
  301  [ -f "$TEST_STATE" ] && { used=0; remaining=8192; }
  302  [ "$TEST_MODE" = inactive ] && { total=0; used=0; remaining=0; }
  303  printf 'total used free shared buff/cache available\nMem: 64000 16000 1000 0 47000 48000\nSwap: %s %s %s\n' "$total" "$used" "$remaining"
  304  ''',
  305              'sudo': '''#!/bin/sh
  306  printf '%s\n' "$@" > "$TEST_CALLS"
  307  [ "$#" = 4 ] && [ "$1" = -n ] && [ "$2" = -- ] && [ "$3" = "$TEST_HELPER" ] && [ "$4" = --reclaim ] || exit 96
  308  [ "$TEST_MODE" = denied ] && exit 1
  309  [ "$TEST_MODE" = stale ] || touch "$TEST_STATE"
  310  exit 0
  311  ''',
  312              'installed-helper': '#!/bin/sh\nexit 97\n',
  313          }
  314          for name, text in fixtures.items():
  315              path = root / name
  316              path.write_text(text)
  317              path.chmod(0o755)
  318          self.env = {'PATH': str(root) + ':/usr/bin:/bin', 'LC_ALL': 'C',
  319                      'TEST_MODE': 'success', 'TEST_STATE': str(self.state),
  320                      'TEST_CALLS': str(self.calls), 'TEST_HELPER': str(self.helper_path)}
  321  
  322      def run_preflight(self, *args):
  323          return subprocess.run(['/bin/bash', str(self.script), *args], env=self.env,
  324                                capture_output=True, text=True)
  325  
  326      def test_default_is_read_only(self):
  327          result = self.run_preflight()
  328          self.assertEqual(result.returncode, 1)
  329          self.assertFalse(self.calls.exists())
  330          self.assertFalse(self.state.exists())
  331  
  332      def test_opt_in_uses_only_fixed_sudo_action_and_fresh_readback(self):
  333          result = self.run_preflight('--reclaim-swap')
  334          self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
  335          self.assertEqual(self.calls.read_text().splitlines(), ['-n', '--', str(self.helper_path), '--reclaim'])
  336          self.assertIn('0MB used, 8192MB free', result.stdout)
  337  
  338      def test_missing_permission_or_false_success_does_not_pass(self):
  339          for mode in ['denied', 'stale']:
  340              with self.subTest(mode=mode):
  341                  self.env['TEST_MODE'] = mode
  342                  result = self.run_preflight('--reclaim-swap')
  343                  self.assertEqual(result.returncode, 1)
  344                  self.assertNotIn('\nREADY\n', result.stdout)
  345  
  346      def test_missing_helper_is_visible(self):
  347          self.helper_path.unlink()
  348          result = self.run_preflight('--reclaim-swap')
  349          self.assertEqual(result.returncode, 1)
  350          self.assertIn('RECLAIM UNAVAILABLE', result.stdout)
  351          self.assertFalse(self.calls.exists())
  352  
  353      def test_inactive_swap_never_reports_ready_or_auto_recovers(self):
  354          self.env['TEST_MODE'] = 'inactive'
  355          for argv in [(), ('--reclaim-swap',)]:
  356              with self.subTest(argv=argv):
  357                  result = self.run_preflight(*argv)
  358                  self.assertEqual(result.returncode, 1, result.stdout)
  359                  self.assertIn('NO ACTIVE SWAP', result.stdout)
  360                  self.assertNotIn('\nREADY\n', result.stdout)
  361                  self.assertFalse(self.calls.exists())
  362  
  363      def test_bad_observations_or_options_never_mutate(self):
  364          self.env['TEST_MODE'] = 'invalid'
  365          result = self.run_preflight('--reclaim-swap')
  366          self.assertEqual(result.returncode, 1)
  367          self.assertIn('cannot read valid', result.stdout)
  368          for argv in [('--force',), ('--stop-vms', '--reclaim-swap')]:
  369              self.assertEqual(self.run_preflight(*argv).returncode, 2)
  370          self.assertFalse(self.calls.exists())
  371  
  372  
  373  class Installation(unittest.TestCase):
  374      def test_rule_order_refuses_later_files_or_main_directives(self):
  375          good = '@includedir /etc/sudoers.d\n# trailing comment\n'
  376          entries = [Path('/etc/sudoers.d/zz-fleet-hardening'), Path('/etc/sudoers.d/README'),
  377                     Path('/etc/sudoers.d/zzz-ignored.tmp'), Path('/etc/sudoers.d/zzz-ignored~')]
  378          with patch.object(Path, 'read_text', return_value=good), patch.object(Path, 'iterdir', return_value=entries):
  379              installer.assert_policy_order()
  380          with patch.object(Path, 'read_text', return_value=good), patch.object(Path, 'iterdir', return_value=entries + [Path('/etc/sudoers.d/zzz-later')]):
  381              with self.assertRaisesRegex(RuntimeError, 'later sudoers'):
  382                  installer.assert_policy_order()
  383          with patch.object(Path, 'read_text', return_value=good + 'max ALL=(ALL) ALL\n'):
  384              with self.assertRaisesRegex(RuntimeError, 'final directive'):
  385                  installer.assert_policy_order()
  386  
  387      def test_policy_directory_must_be_included(self):
  388          for text in ['@includedir /etc/sudoers.d\n', '#includedir /etc/sudoers.d\n']:
  389              with patch.object(Path, 'read_text', return_value=text):
  390                  installer.assert_policy_directory_included()
  391          for text in ['', '# @includedir /etc/sudoers.d\n', '@includedir /different\n']:
  392              with patch.object(Path, 'read_text', return_value=text), self.assertRaisesRegex(RuntimeError, 'direct'):
  393                  installer.assert_policy_directory_included()
  394  
  395      def test_real_visudo_rejects_unowned_include_directory(self):
  396          with tempfile.TemporaryDirectory() as directory:
  397              root = Path(directory)
  398              included = root / 'included'
  399              included.mkdir()
  400              main = root / 'sudoers'
  401              main.write_text('@includedir ' + str(included) + '\n')
  402              entry = included / 'fixture'
  403              entry.write_bytes(installer.policy(args.helper.read_bytes()))
  404              result = subprocess.run(['/usr/sbin/visudo', '-c', '-f', str(main)], capture_output=True, text=True)
  405              self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
  406              self.assertIn('must be owned by root', result.stdout + result.stderr)
  407  
  408      def test_policy_is_exact_action_with_hash_receipt_and_valid_sudoers(self):
  409          data = args.helper.read_bytes()
  410          policy = installer.policy(data).decode()
  411          self.assertIn('max ALL=(root) NOPASSWD: NOSETENV: ', policy)
  412          self.assertIn(installer.hashlib.sha256(data).hexdigest(), policy)
  413          self.assertEqual(len([line for line in policy.splitlines() if not line.startswith('#')]), 1)
  414          self.assertTrue(policy.endswith(' /usr/local/sbin/pixelelated-reclaim-swap --reclaim\n'))
  415          self.assertNotIn('*', policy)
  416          with tempfile.TemporaryDirectory() as directory:
  417              target = Path(directory) / 'policy'
  418              target.write_text(policy)
  419              result = subprocess.run(['/usr/sbin/visudo', '-c', '-f', str(target)], capture_output=True, text=True)
  420              self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
  421  
  422      def test_unprivileged_installation_cannot_write(self):
  423          with patch.object(installer, 'stage') as stage, self.assertRaises(RuntimeError):
  424              installer.install(b'irrelevant')
  425          stage.assert_not_called()
  426  
  427      def test_policy_validation_failure_rolls_back_both_files(self):
  428          with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
  429              helper_path, policy_path = Path(directory) / 'helper', Path(directory) / 'policy'
  430              helper_path.write_bytes(b'old-helper'); helper_path.chmod(0o755)
  431              policy_path.write_bytes(b'old-policy'); policy_path.chmod(0o440)
  432              legacy_path = Path(directory) / 'legacy'
  433              legacy_path.write_bytes(installer.policy(b'old-helper'))
  434              stack.enter_context(patch.object(installer, 'HELPER', helper_path))
  435              stack.enter_context(patch.object(installer, 'POLICY', policy_path))
  436              stack.enter_context(patch.object(installer, 'LEGACY_POLICY', legacy_path))
  437              stack.enter_context(patch.object(installer.os, 'geteuid', return_value=0))
  438              stack.enter_context(patch.object(installer.pwd, 'getpwnam', return_value=SimpleNamespace(pw_uid=1000)))
  439              stack.enter_context(patch.object(Path, 'read_text', return_value='serval\n'))
  440              stack.enter_context(patch.object(installer, 'assert_policy_directory_included'))
  441              stack.enter_context(patch.object(installer, 'assert_policy_order'))
  442              stack.enter_context(patch.object(installer, 'secure'))
  443              stack.enter_context(patch.object(installer.os, 'fchown'))
  444              stack.enter_context(patch.object(installer, 'validate', side_effect=[None, None, RuntimeError('full policy rejected'), None]))
  445              with self.assertRaisesRegex(RuntimeError, 'full policy rejected'):
  446                  installer.install(b'new-helper')
  447              self.assertEqual(helper_path.read_bytes(), b'old-helper')
  448              self.assertEqual(policy_path.read_bytes(), b'old-policy')
  449              self.assertEqual(legacy_path.read_bytes(), installer.policy(b'old-helper'))
  450              self.assertEqual(sorted(p.name for p in Path(directory).iterdir()), ['helper', 'legacy', 'policy'])
  451  
  452      def test_migrate_only_unchanged_legacy_policy(self):
  453          with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
  454              helper_path, policy_path, legacy_path = [Path(directory) / name for name in ('helper', 'policy', 'legacy')]
  455              helper_path.write_bytes(b'old-helper')
  456              legacy_path.write_bytes(b'locally edited policy')
  457              for name, value in [('HELPER', helper_path), ('POLICY', policy_path), ('LEGACY_POLICY', legacy_path)]:
  458                  stack.enter_context(patch.object(installer, name, value))
  459              stack.enter_context(patch.object(installer.os, 'geteuid', return_value=0))
  460              stack.enter_context(patch.object(installer.pwd, 'getpwnam', return_value=SimpleNamespace(pw_uid=1000)))
  461              stack.enter_context(patch.object(Path, 'read_text', return_value='serval\n'))
  462              for name in ('secure', 'validate', 'assert_policy_directory_included', 'assert_policy_order'):
  463                  stack.enter_context(patch.object(installer, name))
  464              stack.enter_context(patch.object(installer.os, 'fchown'))
  465              with self.assertRaisesRegex(RuntimeError, 'old helper policy was edited'):
  466                  installer.install(b'new-helper')
  467              self.assertFalse(policy_path.exists())
  468              self.assertEqual(helper_path.read_bytes(), b'old-helper')
  469              legacy_path.write_bytes(installer.policy(b'old-helper'))
  470              installer.install(b'new-helper')
  471              self.assertEqual(helper_path.read_bytes(), b'new-helper')
  472              self.assertEqual(policy_path.read_bytes(), installer.policy(b'new-helper'))
  473              self.assertFalse(legacy_path.exists())
  474  
  475      def test_failed_policy_restore_still_restores_helper_and_cleans_temps(self):
  476          with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
  477              helper_path, policy_path = Path(directory) / 'helper', Path(directory) / 'policy'
  478              helper_path.write_bytes(b'old-helper'); policy_path.write_bytes(b'old-policy')
  479              stack.enter_context(patch.object(installer, 'HELPER', helper_path))
  480              stack.enter_context(patch.object(installer, 'POLICY', policy_path))
  481              stack.enter_context(patch.object(installer, 'LEGACY_POLICY', Path(directory) / 'legacy'))
  482              stack.enter_context(patch.object(installer.os, 'geteuid', return_value=0))
  483              stack.enter_context(patch.object(installer.pwd, 'getpwnam', return_value=SimpleNamespace(pw_uid=1000)))
  484              stack.enter_context(patch.object(Path, 'read_text', return_value='serval\n'))
  485              stack.enter_context(patch.object(installer, 'assert_policy_directory_included'))
  486              stack.enter_context(patch.object(installer, 'assert_policy_order'))
  487              stack.enter_context(patch.object(installer, 'secure'))
  488              stack.enter_context(patch.object(installer.os, 'fchown'))
  489              validate = stack.enter_context(patch.object(installer, 'validate', side_effect=[None, None, RuntimeError('full policy rejected'), None]))
  490              replace = Path.replace
  491              policy_replaces = []
  492              def fail_rollback(path, target):
  493                  if target == policy_path:
  494                      policy_replaces.append(path)
  495                      if len(policy_replaces) == 2:
  496                          raise OSError('injected policy restore failure')
  497                  return replace(path, target)
  498              stack.enter_context(patch.object(Path, 'replace', fail_rollback))
  499              with self.assertRaisesRegex(RuntimeError, 'rollback incomplete'):
  500                  installer.install(b'new-helper')
  501              self.assertEqual(helper_path.read_bytes(), b'old-helper')
  502              self.assertEqual(validate.call_count, 4)
  503              self.assertEqual(sorted(p.name for p in Path(directory).iterdir()), ['helper', 'policy'])
  504  
  505  
  506  if __name__ == '__main__':
  507      unittest.main(argv=['test-swap-reclaim'], verbosity=2)
  508  
```

## file, whole, at 8ebaf8daad: tools/watch-build

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """Run one build or QA command with durable logs and the shared watch-job monitor.
    5  
    6  Entrypoints use --entry; nested scripts reuse the outer run, including across
    7  the Docker mount. No command arguments or environment values are recorded.
    8  """
    9  import argparse
   10  import datetime
   11  import importlib.machinery
   12  import importlib.util
   13  import fcntl
   14  import os
   15  from pathlib import Path
   16  import selectors
   17  import shutil
   18  import signal
   19  import subprocess
   20  import sys
   21  import time
   22  import uuid
   23  
   24  
   25  def atomic(path, text):
   26      temporary = path.with_name(path.name + '.tmp')
   27      temporary.write_text(text)
   28      temporary.replace(path)
   29  
   30  
   31  def active_run(root, relative):
   32      run = root / relative
   33      if not relative.startswith('.build-runs/') or '..' in Path(relative).parts:
   34          raise RuntimeError('invalid inherited run path')
   35      status = run / 'build.status'
   36      text = status.read_text()
   37      try:
   38          interval = int((run / 'watcher.interval').read_text())
   39      except ValueError:
   40          raise RuntimeError('invalid inherited watcher interval')
   41      if interval < 1 or time.time() - status.stat().st_mtime > max(90, 2 * interval + 5):
   42          raise RuntimeError('inherited watcher heartbeat is stale')
   43      if not any(text.startswith('state:       ' + s + '\n') for s in ('running', 'stalled')):
   44          raise RuntimeError('inherited watcher is not active')
   45      if (run / 'build.rc').exists():
   46          raise RuntimeError('inherited build has already finished')
   47      return run
   48  
   49  
   50  def admission_tool():
   51      path = Path(__file__).resolve().parent / 'host-maintenance/build-admission'
   52      # Keep the frozen tool tree read-only; runtime records live in .build-runs.
   53      sys.dont_write_bytecode = True
   54      loader = importlib.machinery.SourceFileLoader('build_admission', str(path))
   55      spec = importlib.util.spec_from_loader(loader.name, loader)
   56      module = importlib.util.module_from_spec(spec)
   57      loader.exec_module(module)
   58      return module
   59  
   60  
   61  def main():
   62      parser = argparse.ArgumentParser(description=__doc__)
   63      parser.add_argument('--admission', type=Path, help='single-use build admission; otherwise PIXELELATED_BUILD_ADMISSION')
   64      parser.add_argument('--record-only', action='store_true', help='non-compiling QA/record job; nested build entrypoints remain forbidden')
   65      parser.add_argument('--entry', action='store_true')
   66      parser.add_argument('--docker', action='store_true', help='observe the host worktree, not its container path')
   67      parser.add_argument('--interval', type=int, default=5)
   68      parser.add_argument('--activity-dir', type=Path, help='observe this run\'s QA logs instead of build logs')
   69      parser.add_argument('--recursive-activity', action='store_true')
   70      parser.add_argument('--stall-min', type=int, default=15)
   71      parser.add_argument('command', nargs=argparse.REMAINDER)
   72      args = parser.parse_args()
   73      command = args.command
   74      if command and command[0] == '--':
   75          command = command[1:]
   76      if not command or args.interval < 1 or args.stall_min < 0:
   77          parser.error('a command, positive interval and nonnegative stall limit are required')
   78      if args.recursive_activity and args.activity_dir is None:
   79          parser.error('--recursive-activity needs --activity-dir')
   80      if args.activity_dir is not None and not args.activity_dir.is_dir():
   81          parser.error('--activity-dir must exist')
   82      root = Path.cwd().resolve()
   83      environment = os.environ.copy()
   84      if args.record_only and (args.entry or args.docker or args.admission):
   85          parser.error('--record-only cannot be a build entrypoint or carry an admission')
   86      guard = admission_tool()
   87      if args.entry:
   88          environment['RASTERATOPS_WATCH_EXEC'] = command[0]
   89      inherited = environment.get('RASTERATOPS_BUILD_RUN')
   90      if inherited:
   91          inherited_run = active_run(root, inherited)
   92          if args.entry or args.docker or not args.record_only:
   93              guard.nested(root, inherited_run, environment)
   94          os.execvpe(command[0], command, environment)
   95  
   96      receipt = args.admission or environment.get('PIXELELATED_BUILD_ADMISSION')
   97      if not args.record_only and not receipt:
   98          raise RuntimeError('build admission required; prepare tools/host-maintenance/build-admission first')
   99      build_umask = os.umask(0o077)
  100      runs = root / '.build-runs'
  101      runs.mkdir(exist_ok=True, mode=0o700)
  102      lock = (runs / 'active.lock').open('a')
  103      try:
  104          fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
  105      except BlockingIOError:
  106          raise RuntimeError('another monitored build owns this worktree')
  107      name = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:8]
  108      run = runs / name
  109      run.mkdir(mode=0o700)
  110      environment['RASTERATOPS_BUILD_RUN'] = str(run.relative_to(root))
  111      (run / 'build.pid').write_text(str(os.getpid()) + '\n')
  112      (run / 'watcher.interval').write_text(str(args.interval) + '\n')
  113      (run / 'build.start').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat() + '\n')
  114      source = Path(__file__).resolve().with_name('watch-job')
  115      shutil.copyfile(source, run / 'watch-job')
  116      (run / 'watch-job').chmod(0o500)
  117      print(f'watch-build: recording in {run}', file=sys.stderr, flush=True)
  118  
  119      # BUILD_DIR can move native build roots; Docker's host wrapper observes
  120      # the mounted worktree, even when its container path is different.
  121      activity_root = root if args.docker else Path(environment.get('BUILD_DIR', str(root)))
  122      log = (run / 'build.log').open('wb', buffering=0)
  123      errors = (run / 'watcher.err').open('wb', buffering=0)
  124      activity_args = ['--activity-root', str(activity_root), '--build-progress']
  125      if args.activity_dir is not None:
  126          activity_args = ['--activity-dir', str(args.activity_dir.resolve())]
  127          if args.recursive_activity:
  128              activity_args.append('--recursive-activity')
  129      monitor = subprocess.Popen([
  130          str(run / 'watch-job'), '--log', str(run / 'build.log'),
  131          '--rc', str(run / 'build.rc'), '--status', str(run / 'build.status'),
  132          '--pid', str(os.getpid()), *activity_args,
  133          '--stall-min', str(args.stall_min), '--interval', str(args.interval)], stdout=subprocess.DEVNULL,
  134          stderr=errors, start_new_session=True)
  135      (run / 'watcher.pid').write_text(str(monitor.pid) + '\n')
  136      deadline = time.monotonic() + 10
  137      while True:
  138          try:
  139              active_run(root, environment['RASTERATOPS_BUILD_RUN'])
  140              break
  141          except (OSError, RuntimeError):
  142              if monitor.poll() is not None or time.monotonic() > deadline:
  143                  if monitor.poll() is None:
  144                      monitor.terminate()
  145                      monitor.wait(timeout=5)
  146                  atomic(run / 'runner-error', 'watcher failed to arm; command was not started\n')
  147                  raise RuntimeError(f'watcher failed to arm; see {run}')
  148              time.sleep(.025)
  149  
  150      child = None
  151      interrupted = None
  152  
  153      def forward(signum, _frame):
  154          nonlocal interrupted
  155          interrupted = signum
  156          if child is not None and child.poll() is None:
  157              os.killpg(child.pid, signum)
  158  
  159      for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
  160          signal.signal(sig, forward)
  161      code = 125
  162      try:
  163          if not args.record_only:
  164              guard.admit(receipt, root, run, environment, docker=args.docker)
  165          child = subprocess.Popen(command, env=environment, stdout=subprocess.PIPE,
  166                                   stderr=subprocess.STDOUT, start_new_session=True,
  167                                   preexec_fn=lambda: os.umask(build_umask))
  168          (run / 'command.pid').write_text(str(child.pid) + '\n')
  169          if interrupted is not None:
  170              os.killpg(child.pid, interrupted)
  171          selector = selectors.DefaultSelector()
  172          selector.register(child.stdout, selectors.EVENT_READ)
  173          console = True
  174          while selector.get_map():
  175              for key, _ in selector.select(timeout=1):
  176                  data = os.read(key.fd, 65536)
  177                  if not data:
  178                      selector.unregister(key.fileobj)
  179                      break
  180                  log.write(data)
  181                  if console:
  182                      try:
  183                          sys.stdout.buffer.write(data)
  184                          sys.stdout.buffer.flush()
  185                      except BrokenPipeError:
  186                          # Losing a console reader must not lose the durable log.
  187                          console = False
  188          child.wait()
  189          code = child.returncode if child.returncode >= 0 else 128 - child.returncode
  190      except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as error:
  191          log.write(f'watch-build: command launch/output failed: {error}\n'.encode())
  192          if child is not None and child.poll() is None:
  193              os.killpg(child.pid, signal.SIGTERM)
  194              try:
  195                  child.wait(timeout=5)
  196              except subprocess.TimeoutExpired:
  197                  os.killpg(child.pid, signal.SIGKILL)
  198                  child.wait()
  199      finally:
  200          atomic(run / 'build.rc', str(code) + '\n')
  201          log.close()
  202      try:
  203          monitor_code = monitor.wait(timeout=args.interval + 10)
  204      except subprocess.TimeoutExpired:
  205          monitor.terminate()
  206          monitor_code = monitor.wait(timeout=5)
  207      errors.close()
  208      status = (run / 'build.status').read_text()
  209      if monitor_code != 0 or not status.startswith('state:       finished\n'):
  210          atomic(run / 'runner-error', 'build result retained, but watcher did not record completion\n')
  211          print(f'watch-build: monitoring failed; see {run}', file=sys.stderr)
  212          guard.finish(run, code, monitor_code, code or 125)
  213          return code or 125
  214      guard.finish(run, code, monitor_code, code)
  215      return code
  216  
  217  
  218  if __name__ == '__main__':
  219      try:
  220          sys.exit(main())
  221      except (OSError, RuntimeError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
  222          print(f'watch-build: {error}', file=sys.stderr)
  223          sys.exit(2)
  224  
```

## file, whole, at 8ebaf8daad: tools/watch-build-submit

```
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Submit a durable watch-build process. Submission success is NOT job success.
    5  
    6  Run from the frozen worktree. --owner must be a fresh QA/build owner. The
    7  standard runner retains build.rc/status; this launcher retains tool-wrapper.rc.
    8  Actively read both until completion. Disconnected notification is separate.
    9  """
   10  import argparse
   11  import datetime
   12  import hashlib
   13  import json
   14  import os
   15  from pathlib import Path
   16  import subprocess
   17  import sys
   18  
   19  
   20  def write_json(path, data):
   21      with path.open('x') as stream:
   22          json.dump(data, stream, indent=2)
   23          stream.write('\n')
   24  
   25  
   26  def now():
   27      return datetime.datetime.now(datetime.timezone.utc).isoformat()
   28  
   29  
   30  def worker(owner, command):
   31      owner = Path(owner)
   32      write_json(owner / 'launcher-start.json', {
   33          'utc': now(), 'pid': os.getpid(), 'cwd': str(Path.cwd()),
   34          'start_ticks': Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19],
   35      })
   36      try:
   37          environment = os.environ.copy()
   38          environment['PIXELELATED_SUBMISSION_OWNER'] = str(owner)
   39          result = subprocess.run(command, env=environment).returncode
   40          result = result if result >= 0 else 128 - result
   41      except OSError:
   42          result = 125
   43      # Never manufacture the runner's build.rc, or the job's own inner/outer rc.
   44      with (owner / 'tool-wrapper.rc').open('x') as stream:
   45          stream.write(str(result) + '\n')
   46      write_json(owner / 'launcher-result.json', {
   47          'utc': now(), 'pid': os.getpid(), 'runner_returncode': result,
   48          'submission_is_not_completion': True,
   49      })
   50      return result
   51  
   52  
   53  def main():
   54      if len(sys.argv) > 1 and sys.argv[1] == '--worker':
   55          return worker(sys.argv[2], sys.argv[3:])
   56      parser = argparse.ArgumentParser(description=__doc__)
   57      parser.add_argument('--owner', required=True, type=Path)
   58      parser.add_argument('runner_args', nargs=argparse.REMAINDER)
   59      args = parser.parse_args()
   60      runner_args = args.runner_args
   61      if runner_args and runner_args[0] == '--':
   62          runner_args = runner_args[1:]
   63      owner = args.owner.resolve(strict=True)
   64      runner = Path.cwd() / 'tools/watch-build'
   65      if not owner.is_dir() or not runner.is_file() or not os.access(runner, os.X_OK):
   66          parser.error('existing owner and executable cwd/tools/watch-build required')
   67      if not runner_args or os.environ.get('RASTERATOPS_BUILD_RUN'):
   68          parser.error('runner arguments required; inherited active runs cannot be submitted')
   69      for name in ['qa.start', 'start', 'inner.rc', 'outer.rc', 'tool-wrapper.rc', 'console.log']:
   70          if (owner / name).exists():
   71              parser.error('owner has already started: ' + name)
   72      os.umask(0o077)
   73      # Exclusive reservation is permanent even if launch fails. Use a fresh owner.
   74      write_json(owner / 'launcher-submission.json', {
   75          'utc': now(), 'cwd': str(Path.cwd()), 'runner': str(runner),
   76          'runner_sha256': hashlib.sha256(runner.read_bytes()).hexdigest(),
   77          'submission_is_not_completion': True,
   78      })
   79      copy = owner / 'watch-build-submit.py'
   80      with copy.open('xb') as output:
   81          output.write(Path(__file__).read_bytes())
   82      copy.chmod(0o500)
   83      with (owner / 'console.log').open('xb', buffering=0) as log:
   84          child = subprocess.Popen(
   85              [sys.executable, '-I', str(copy), '--worker', str(owner),
   86               str(runner), *runner_args], stdin=subprocess.DEVNULL,
   87              stdout=log, stderr=subprocess.STDOUT,
   88              start_new_session=True, close_fds=True)
   89      write_json(owner / 'launcher-pid.json', {'pid': child.pid, 'utc': now()})
   90      print(json.dumps({'state': 'submitted', 'pid': child.pid, 'owner': str(owner),
   91                        'completion': str(owner / 'launcher-result.json'),
   92                        'submission_is_not_completion': True}))
   93      return 0
   94  
   95  
   96  if __name__ == '__main__':
   97      try:
   98          sys.exit(main())
   99      except (OSError, ValueError) as error:
  100          print('watch-build-submit: ' + str(error), file=sys.stderr)
  101          sys.exit(2)
  102  
```

## file, whole, at 8ebaf8daad: tools/watch-job

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # watch-job -- keep one file that tells the truth about a long job.
    6  #
    7  #   tools/watch-job --log FILE --rc FILE [--pid N] [--pattern RE]
    8  #                   [--stall-min N] [--status FILE] [--detach]
    9  #   --pid is the job's process ID; --pattern matches progress in its log.
   10  #
   11  # Why a file and not a subscription. A session that says "I am watching this"
   12  # is relying on something that can stop without saying so: a harness can reap
   13  # a background task under memory pressure, a shell can be killed, a session
   14  # can end. All of those look exactly like a healthy job -- silence. That cost
   15  # this project two unnoticed build failures in one day, seven hours and five
   16  # (engineering-practices.md, "A promise is not a mechanism").
   17  #
   18  # So the artifact is a status file, rewritten every INTERVAL seconds, and the
   19  # file's own mtime is what makes an active watcher checkable: if a running
   20  # or stalled status is older than a couple of intervals, investigate the
   21  # watcher. Terminal results intentionally stop updating.
   22  #
   23  # It distinguishes activity, completion, death and observation errors:
   24  #
   25  #   running   a watched log advanced within --stall-min
   26  #   stalled   the process is alive but watched logs have not moved -- which is not
   27  #             always wrong (a long link step) but is always worth knowing
   28  #   finished  the rc file exists; its contents are the outcome
   29  #   died      no process and no rc file: killed outright, wrote no exit code.
   30  #             This is the case a plain "wait for the rc file" waits through
   31  #             forever.
   32  #   error     a required observation or result is invalid; never a green check.
   33  #
   34  # Reading it is one command; stale active status is a failed check:
   35  #
   36  #   cat /workspace/tmp/rocknix-session/<job>.status
   37  #
   38  # Fork-only.
   39  
   40  set -u
   41  LOG=""; RC=""; PID=""; PATTERN='\[[0-9]+/[0-9]+\]'; STALL=15; STATUS=""; DETACH=0; INTERVAL=30
   42  ACTIVITY_DIR=""; ACTIVITY_ROOT=""; RECURSIVE_ACTIVITY=0; BUILD_PROGRESS=0
   43  
   44  usage() {
   45    cat <<'EOF'
   46  usage: tools/watch-job --log FILE --rc FILE [--pid N] [--pattern RE]
   47                         [--stall-min N] [--status FILE] [--interval N] [--detach]
   48                         [--activity-dir DIR]
   49                         [--activity-root WORKTREE]
   50                         [--recursive-activity]
   51                         [--build-progress]
   52  
   53  --pid N       The running job's process ID, used to detect a job that died.
   54  --pattern RE  A regex matching progress lines in the LOG, never a process match.
   55  --build-progress Use only structured pkgbuilder DONE/FAIL lines for overall
   56                   progress; --pattern still applies to package activity.
   57  --log FILE    The job's output file.
   58  --activity-dir DIR  Also observe this job's direct *.log files for activity.
   59                     For parallel builds use the frozen build root's .threads/logs.
   60  --activity-root DIR Discover build.*/.threads/logs as roots appear during this run.
   61                     For the exclusive top-level build runner; not shared jobs.
   62  --recursive-activity Include nested *.log files under --activity-dir.
   63                       Use a fresh, exclusively owned QA artifact directory.
   64  --rc FILE     The result file the job writes when it finishes.
   65  --status FILE Heartbeat/result output (default: beside the result file).
   66  --interval N  Seconds between observations (default: 30).
   67  --stall-min N Minutes without any watched log writes before suspected stall (default: 15).
   68  --detach      Keep watching after the launching shell ends; use the job's PID namespace.
   69  
   70  Status is a local record, not a notification. A quiet linker can still be busy;
   71  stalled means inspect the job, never terminate or restart it automatically.
   72  The watcher PID is retained in FILE.pid beside the status; stop only that PID.
   73  EOF
   74  }
   75  
   76  die() { echo "watch-job: $*" >&2; exit 2; }
   77  
   78  while [ $# -gt 0 ]; do
   79    case "$1" in
   80      --log|--rc|--pid|--pattern|--stall-min|--status|--interval|--activity-dir|--activity-root)
   81        [ $# -ge 2 ] && [ -n "$2" ] || die "$1 needs a value" ;;
   82    esac
   83    case "$1" in
   84      -h|--help)    usage; exit 0 ;;
   85      --log)        LOG="$2"; shift 2 ;;
   86      --rc)         RC="$2"; shift 2 ;;
   87      --pid)        PID="$2"; shift 2 ;;
   88      --pattern)    PATTERN="$2"; shift 2 ;;
   89      --stall-min)  STALL="$2"; shift 2 ;;
   90      --status)     STATUS="$2"; shift 2 ;;
   91      --interval)   INTERVAL="$2"; shift 2 ;;
   92      --activity-dir) ACTIVITY_DIR="$2"; shift 2 ;;
   93      --activity-root) ACTIVITY_ROOT="$2"; shift 2 ;;
   94      --recursive-activity) RECURSIVE_ACTIVITY=1; shift ;;
   95      --build-progress) BUILD_PROGRESS=1; shift ;;
   96      --detach)     DETACH=1; shift ;;
   97      *) echo "watch-job: unknown argument $1" >&2; exit 2 ;;
   98    esac
   99  done
  100  [ -n "$LOG" ] && [ -n "$RC" ] || { echo "watch-job: --log and --rc are required" >&2; exit 2; }
  101  [ -n "$STATUS" ] || STATUS="${RC%.rc}.status"
  102  [[ "$STALL" =~ ^[0-9]{1,6}$ ]] || die "--stall-min needs a nonnegative integer"
  103  [[ "$INTERVAL" =~ ^[0-9]{1,6}$ ]] || die "--interval needs a positive integer"
  104  STALL=$((10#$STALL)); INTERVAL=$((10#$INTERVAL))
  105  [ "$INTERVAL" -gt 0 ] || die "--interval needs a positive integer"
  106  [[ -z "$PID" || "$PID" =~ ^[1-9][0-9]*$ ]] || die "--pid needs a positive integer"
  107  grep -E "$PATTERN" /dev/null >/dev/null 2>&1
  108  [ $? -le 1 ] || die "invalid --pattern regex"
  109  [ -z "$ACTIVITY_DIR" ] || [ -d "$ACTIVITY_DIR" ] || die "activity directory does not exist"
  110  [[ -z "$ACTIVITY_DIR" || -z "$ACTIVITY_ROOT" ]] || die "choose activity-dir or activity-root"
  111  [[ "$RECURSIVE_ACTIVITY" = 0 || -n "$ACTIVITY_DIR" ]] || die "recursive activity needs activity-dir"
  112  # Outputs must never overwrite inputs or create their own activity signal.
  113  status_path=$(readlink -m -- "$STATUS") || die "cannot resolve status path"
  114  for input in "$LOG" "$RC"; do
  115    input_path=$(readlink -m -- "$input") || die "cannot resolve input path"
  116    for output in "$status_path" "$status_path.tmp" "$status_path.pid" "$status_path.err"; do
  117      [ "$input_path" != "$output" ] || die "status outputs overlap a watched input"
  118    done
  119  done
  120  if [ -n "$ACTIVITY_DIR" ]; then
  121    activity_path=$(readlink -m -- "$ACTIVITY_DIR") || die "cannot resolve activity path"
  122    [[ "$status_path" != "$activity_path/"*.log ]] || die "status must be outside activity logs"
  123  fi
  124  if [ -n "$ACTIVITY_ROOT" ]; then
  125    activity_path=$(readlink -m -- "$ACTIVITY_ROOT") || die "cannot resolve activity root"
  126    [[ "$status_path" != "$activity_path/"build.*/.threads/logs/*.log ]] || die "status must be outside activity logs"
  127  fi
  128  
  129  if [ "$DETACH" = 1 ]; then
  130    # Detached, so a harness reaping its own background tasks does not take
  131    # this with them -- the reason the status file exists at all.
  132    DETACH=0
  133    # Its own stderr goes beside the status file, not to /dev/null: on
  134    # 2026-09-19 a watcher died ten minutes into a run and the only evidence
  135    # was a stale heartbeat, with nothing to say why.
  136    args=(--log "$LOG" --rc "$RC" --pattern "$PATTERN" --stall-min "$STALL"
  137          --status "$STATUS" --interval "$INTERVAL")
  138    [ -z "$PID" ] || args+=(--pid "$PID")
  139    [ -z "$ACTIVITY_DIR" ] || args+=(--activity-dir "$ACTIVITY_DIR")
  140    [ -z "$ACTIVITY_ROOT" ] || args+=(--activity-root "$ACTIVITY_ROOT")
  141    [ "$RECURSIVE_ACTIVITY" = 0 ] || args+=(--recursive-activity)
  142    [ "$BUILD_PROGRESS" = 0 ] || args+=(--build-progress)
  143    setsid nohup "$0" "${args[@]}" >/dev/null 2>"$STATUS.err" &
  144    watcher=$!
  145    for ((attempt=0; attempt<50; attempt++)); do
  146      if grep -qE "^watcher_pid: $watcher$" "$STATUS" 2>/dev/null; then
  147        grep -q '^state:       error$' "$STATUS" && die "detached observation failed; see $STATUS"
  148        echo "watch-job: detached pid $watcher, status at $STATUS"
  149        exit 0
  150      fi
  151      kill -0 "$watcher" 2>/dev/null || die "detached watcher exited before its first status; see $STATUS.err"
  152      sleep 0.1
  153    done
  154    kill "$watcher" 2>/dev/null || :
  155    die "detached watcher did not write its first status; see $STATUS.err"
  156  fi
  157  
  158  started=$(date -u '+%Y-%m-%d %H:%M:%S UTC')
  159  started_s=$(date +%s)
  160  printf '%s\n' "$$" > "$STATUS.pid" || die "cannot write watcher pidfile"
  161  
  162  # kill -0 alone considers an unreaped zombie alive and cannot notice PID reuse.
  163  job_identity() {
  164    local raw fields
  165    [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null || return 1
  166    raw=$(cat "/proc/$PID/stat" 2>/dev/null) || return 1
  167    read -ra fields <<< "${raw##*) }"
  168    [[ ${fields[0]:-Z} != Z && ${fields[0]:-X} != X ]] || return 1
  169    printf '%s\n' "${fields[19]:-}"
  170  }
  171  identity=$(job_identity) || identity=""
  172  while :; do
  173    now_s=$(date +%s)
  174    observation_error=""; outcome=""
  175    log_age=-1; newest=-1; activity=""
  176    if [ -f "$LOG" ]; then
  177      if newest=$(stat -c %Y -- "$LOG"); then
  178        activity="$LOG"; log_age=$((now_s - newest))
  179      else
  180        newest=-1; observation_error="cannot stat main log"
  181      fi
  182    fi
  183    activity_dirs=()
  184    if [ -n "$ACTIVITY_DIR" ]; then activity_dirs+=("$ACTIVITY_DIR"); fi
  185    if [ -n "$ACTIVITY_ROOT" ]; then
  186      for directory in "$ACTIVITY_ROOT"/build.*/.threads/logs; do
  187        [ ! -d "$directory" ] || activity_dirs+=("$directory")
  188      done
  189    fi
  190    for directory in "${activity_dirs[@]}"; do
  191      # Capture find's exit status rather than hiding it in process substitution.
  192      scan=$(mktemp "${STATUS}.scan.XXXXXX") || die "cannot create activity scan"
  193      depth=(-maxdepth 1)
  194      [ "$RECURSIVE_ACTIVITY" = 0 ] || depth=()
  195      if find "$directory" "${depth[@]}" -type f -name '*.log' -printf '%T@ %p\0' > "$scan"; then
  196        while IFS= read -r -d '' entry; do
  197          stamp=${entry%% *}; stamp=${stamp%%.*}
  198          if [ "$stamp" -gt "$newest" ]; then
  199            newest=$stamp; activity=${entry#* }
  200          fi
  201        done < "$scan"
  202      else
  203        observation_error="cannot scan activity logs"
  204      fi
  205      rm -f -- "$scan"
  206    done
  207    # A job that never creates output must not stay running forever.
  208    if [ "$newest" -ge 0 ]; then activity_age=$((now_s - newest)); else activity_age=$((now_s - started_s)); fi
  209    if [ "$BUILD_PROGRESS" = 1 ]; then
  210      # Completed package logs are copied into LOG and carry their own Ninja
  211      # counters. Only pkgbuilder's structured status identifies overall work.
  212      progress=$(sed 's/\x1b\[[0-9;]*m//g' "$LOG" 2>/dev/null |
  213        grep -E '^\[[0-9]+/[0-9]+\][[:space:]]+\[(DONE|FAIL)\][[:space:]]+(build|install|unpack)[[:space:]]' |
  214        grep -oE '^\[[0-9]+/[0-9]+\]' | tail -1)
  215    else
  216      progress=$(grep -oE "$PATTERN" "$LOG" 2>/dev/null | tail -1)
  217    fi
  218    alive=unknown
  219    if [ -n "$PID" ]; then
  220      alive=no
  221      current_identity=$(job_identity) || current_identity=""
  222      if [ -n "$identity" ] && [ "$identity" = "$current_identity" ]; then alive=yes; fi
  223    fi
  224  
  225    if [ -f "$RC" ]; then
  226      outcome=$(cat "$RC")
  227      if [[ "$outcome" =~ ^[0-9]{1,3}$ ]] && [ "$((10#$outcome))" -le 255 ]; then
  228        state=finished
  229      else
  230        state=error; observation_error="result file does not contain an exit code (0..255)"
  231      fi
  232    elif [ "$alive" = no ] && [ -n "$PID" ]; then
  233      state=died
  234    elif [ -n "$observation_error" ]; then
  235      state=error
  236    elif [ "$activity_age" -gt $(( STALL * 60 )) ]; then
  237      state=stalled
  238    else
  239      state=running
  240    fi
  241  
  242    {
  243      echo "state:       $state"
  244      case "$state" in
  245        finished|died|error) heartbeat_note='terminal result; heartbeat stops here' ;;
  246        *) heartbeat_note='if this is stale, investigate the watcher' ;;
  247      esac
  248      echo "written:     $(date -u '+%Y-%m-%d %H:%M:%S UTC')   <- $heartbeat_note"
  249      echo "watcher_pid: $$"
  250      echo "job_pid:     ${PID:-unknown}  alive=$alive"
  251      echo "started:     $started"
  252      echo "progress:    ${progress:-none matched}"
  253      echo "log:         $LOG  (last written ${log_age}s ago)"
  254      echo "activity:    ${activity:-no log yet}  (last written ${activity_age}s ago)"
  255      [ -z "$ACTIVITY_DIR" ] || echo "activity_dir: $ACTIVITY_DIR"
  256      [ -z "$ACTIVITY_ROOT" ] || echo "activity_root: $ACTIVITY_ROOT"
  257      [ "$state" = finished ] && echo "outcome:     rc=$outcome"
  258      [ "$state" = error ] && echo "outcome:     OBSERVATION ERROR -- $observation_error"
  259      [ "$state" = died ] && echo "outcome:     NO EXIT CODE WRITTEN -- job absent, exited or PID reused"
  260      [ "$state" = stalled ] && echo "note:        suspected stall: no watched log writes in over ${STALL} min; inspect process before acting"
  261      if [ -n "$activity" ] && [ "$activity" != "$LOG" ]; then
  262        echo "activity_progress: $(grep -oE "$PATTERN" "$activity" 2>/dev/null | tail -1)"
  263      fi
  264      echo "tail:"
  265      tail -2 "${activity:-$LOG}" 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-130 | sed 's/^/  /'
  266    } > "$STATUS.tmp" && mv "$STATUS.tmp" "$STATUS" || die "cannot publish status"
  267  
  268    case "$state" in finished|died) exit 0 ;; error) exit 2 ;; esac
  269    sleep "$INTERVAL"
  270  done
  271  
```

## entry-line context: Makefile:30-50

```
   30  kconfig-olddefconfig-%:
   31  	DEVICE=$* ./tools/adjust_kernel_config olddefconfig
   32  
   33  kconfig-menuconfig-%:
   34  	DEVICE=$* ./tools/adjust_kernel_config menuconfig
   35  
   36  # One admission covers the whole native device target, including both ABIs.
   37  # Docker already enters through the host watcher and takes the inner branch.
   38  ifeq ($(RASTERATOPS_BUILD_RUN),)
   39  world AMD64 RK3588 RK3576 S922X RK3566 RK3326 RK3399 H700 SM4450 SM6115 SM8250 SM8550 SM8650 SM8750 GENERIC_X64:
   40  	./tools/watch-build -- $(MAKE) $@
   41  else
   42  world: RK3588 RK3576 RK3566 RK3326 RK3399 S922X SM8250 SM8550 H700 SM8650 SM8750 GENERIC_X64
   43  
   44  AMD64:
   45  	unset DEVICE_ROOT
   46  	PROJECT=ROCKNIX DEVICE=AMD64 ARCH=x86_64 ./scripts/build_distro
   47  
   48  RK3588:
   49  	unset DEVICE_ROOT
   50  	PROJECT=ROCKNIX DEVICE=RK3588 ARCH=arm ./scripts/build_distro
```

## entry-line context: Makefile:170-212

```
  170  
  171  # Launch docker as interactive if this is an interactive shell (allows ctrl-c for manual and running non-interactive - aka: build server)
  172  docker-%: INTERACTIVE=$(shell [ -t 0 ] && echo "-it")
  173  
  174  # By default pass through anything after `docker-` back into `make`
  175  docker-%: COMMAND=make $*
  176  
  177  # Record from outside Docker so a container exit cannot erase its monitor.
  178  # Direct native scripts use the same runner; nested builds inherit its run.
  179  docker-%: BUILD_WATCH=$(if $(filter shell clean distclean package-clean update kconfig-%,$*),,./tools/watch-build --docker --)
  180  
  181  # If the user issues a `make docker-shell` just start up bash as the shell to run commands
  182  docker-shell: COMMAND=bash
  183  
  184  # Command: builds and saves a docker builder image locally.
  185  # The build user must also be a member of the "docker" group.
  186  docker-image-build:
  187  	$(DOCKER_CMD) buildx create --use
  188  	$(DOCKER_CMD) buildx build --tag $(DOCKER_IMAGE_LOCAL) --platform $(shell if [ "$$(uname -m)" = "aarch64" ]; then echo "linux/arm64"; else echo "linux/amd64"; fi) --load .
  189  
  190  # Command: pulls the pinned build container from the fork's mirror, by digest.
  191  docker-image-pull:
  192  	$(DOCKER_CMD) pull $(DOCKER_IMAGE)
  193  
  194  # Wire up docker to call equivalent make files using % to match and $* to pass the value matched by %
  195  # .env carries the forwarded environment into the container, credentials
  196  # included when a build has them (scripts/get_env drops the rest). It is
  197  # written here, in the recipe, and not as a prerequisite: a $(shell) there
  198  # ran whenever make read this file, for any target. rm first, so an older
  199  # copy's mode is never reused and umask 077 makes it owner-only -- and an
  200  # older copy that cannot be removed stops the recipe, since umask does not
  201  # tighten a file that already exists (set -C refuses to write into one); the
  202  # trap removes it when the container exits or the recipe is interrupted, and
  203  # a get_env that fails starts no container.
  204  docker-%:
  205  	rm -f .env && [ ! -e .env ] || { echo "an older .env cannot be removed: no container started" >&2; exit 1; }; \
  206  	trap 'rm -f .env' EXIT; trap 'exit 130' INT TERM HUP; \
  207  	( umask 077 && set -C && ./scripts/get_env > .env ) || { echo "scripts/get_env failed: no container started" >&2; exit 1; }; \
  208  	BUILD_DIR=$(DOCKER_WORK_DIR) $(BUILD_WATCH) $(DOCKER_CMD) run $(PODMAN_ARGS) $(INTERACTIVE) --init --env-file .env -e RASTERATOPS_BUILD_RUN -e PROJECT -e DEVICE -e ARCH -e BUILDER_NAME=pixelelated-build -e BUILDER_VERSION=$(DOCKER_IMAGE_DIGEST) --rm --user $(UID):$(GID) $(GLOBAL_SETTINGS) $(LOCAL_SSH_KEYS_FILE) $(EMULATIONSTATION_SRC) -v $(PWD):$(DOCKER_WORK_DIR) -w $(DOCKER_WORK_DIR) $(DOCKER_EXTRA_OPTS) $(DOCKER_IMAGE) $(COMMAND)
  209  
```

## entry-line context: scripts/build:1-12

```
    1  #!/bin/bash
    2  
    3  # SPDX-License-Identifier: GPL-2.0-or-later
    4  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    5  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
    6  
    7  # Fork build monitoring: nested calls reuse the outer run (#394).
    8  if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
    9    exec ./tools/watch-build --entry -- "$0" "$@"
   10  fi
   11  unset RASTERATOPS_WATCH_EXEC
   12  
```

## entry-line context: scripts/build_distro:1-14

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  ###
    6  ### Simple script to build ROCKNX
    7  ###
    8  
    9  # Fork build monitoring: nested calls reuse the outer run (#394).
   10  if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
   11    exec ./tools/watch-build --entry -- "$0" "$@"
   12  fi
   13  unset RASTERATOPS_WATCH_EXEC
   14  
```

## entry-line context: scripts/image:1-12

```
    1  #!/bin/bash
    2  
    3  # SPDX-License-Identifier: GPL-2.0-or-later
    4  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    5  # Copyright (C) 2016-present Team LibreELEC (https://libreelec.tv)
    6  
    7  # Fork build monitoring: nested calls reuse the outer run (#394).
    8  if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
    9    exec ./tools/watch-build --entry -- "$0" "$@"
   10  fi
   11  unset RASTERATOPS_WATCH_EXEC
   12  
```

## entry-line context: scripts/install:1-13

```
    1  #!/bin/bash
    2  
    3  # SPDX-License-Identifier: GPL-2.0-or-later
    4  # Copyright (C) 2010-2011 Roman Weber (roman@openelec.tv)
    5  # Copyright (C) 2009-2016 Stephan Raue (stephan@openelec.tv)
    6  # Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)
    7  
    8  # Fork build monitoring: nested calls reuse the outer run (#394).
    9  if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
   10    exec ./tools/watch-build --entry -- "$0" "$@"
   11  fi
   12  unset RASTERATOPS_WATCH_EXEC
   13  
```

## entry-line context: scripts/build_compat:1-10

```
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  # Fork build monitoring: nested calls reuse the outer run (#394).
    6  if [[ "${RASTERATOPS_WATCH_EXEC:-}" != "$0" ]]; then
    7    exec ./tools/watch-build --entry -- "$0" "$@"
    8  fi
    9  unset RASTERATOPS_WATCH_EXEC
   10  
```

## entry-line context: .github/workflows/fork-checks.yml:30-50

```
   30          with:
   31            fetch-depth: 0
   32        - name: identify upstream history for the fork issue-coverage check
   33          run: git fetch --no-tags https://github.com/ROCKNIX/distribution.git next:refs/remotes/upstream/next
   34        - name: work-log index is current
   35          run: ./tools/work-log-index --check
   36        - name: decision register is a lookup table
   37          run: ./tools/register-check
   38        - name: the instruction files are what their index says
   39          run: ./tools/rules-check
   40        - name: builds always enter the shared watcher and retain lifecycle evidence
   41          run: |
   42            python3 docs/qa-logs/2026-10-03-watch-job/test-watch-job.py tools/watch-job
   43            python3 tools/host-maintenance/test-build-monitor
   44            python3 tools/host-maintenance/test-build-admission
   45        - name: VM launch failures cannot report a guest as running
   46          run: |
   47            ./tools/vm-pair-test
   48            ./tools/vm-upgrade-readiness-test
   49        - name: optional hardware readings are valid or explicitly unavailable
   50          run: ./tools/rocknix-info-test
```

## output: the eight controls and hooks-test, in the lane's worktree at the hash

```
swap-reclaim               rc 0     0.1s  OK
retention-report           rc 0     6.9s  }
build-admission            rc 0    17.9s  {"result": "PASS", "checks": 68, "cases": ["undeclared BUILD_DIR blocks payload", "missing receipt blocks payl
build-monitor              rc 0    63.9s  36 PASS; 0 FAIL
watch-job                  rc 0     9.4s  32 PASS; 0 FAIL
progress                   rc 1     0.4s  3 PASS; 10 FAIL
watch-build-20261004       rc 1     0.1s  AssertionError: shared runner observes nested QA logs and retains terminal result
submit                     rc 1     0.2s  AssertionError
hooks-test                 rc 0     0.7s  PASS
```

## output: test-submit.py's receipt, unmodified control (layer 1)

```
[Errno 2] No such file or directory: '/tmp/pixelelated-watch-submit-ebkyj88c/tools/host-maintenance/build-admission'
```

## output: test-submit.py's receipt, diagnostic copy with build-admission added (layer 2)

```
runner_returncode: 2
tool-wrapper.rc: 2
console.log: watch-build: build admission required; prepare tools/host-maintenance/build-admission first
```

## output: the record: .build-runs directories and states

```
2026-10-24T15:45:41Z
46
run ids: 1902
build.status first lines over 1,885 runs: finished 1885; runner-error files: 0; 17 run directories without build.status are hand-made folders of tracker readbacks
```

## output: the cost figures

```
build.start -> admission.json admitted over 663 recorded runs: median 0.09 s (0.08..0.19)
watch-job --build-progress pipeline over the largest recorded build.log (213,562,360 bytes): 0.50, 0.45, 0.44 s; over a 45,743,868-byte log: 0.13 s; watcher.interval 5
```

## output: the container Python record

```
device-builds.md:379-380: On 2026-10-08, host Python3.14 accepted a helper using `hashlib.file_digest`, but the build container's Python3.10 lacked it.
Makefile:138 docker-%: DOCKER_IMAGE_DIGEST := sha256:988c0ba5... (unchanged since 2c349c6d51, 2026-10-01)
```
