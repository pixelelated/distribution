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
| 15 | No file under `tools/` changed before a stream brief | none by this lane: `git diff --stat cdc45513b0 HEAD -- tools` empty; the hash-based command lists P1's and the coordinator's 15 inherited files | § Mechanical checks |
| 16 | The retro | stage G | `docs/retros/` |
| 17 | The six checkers' exits | stage H | the hand-back |

## Mechanical checks

| Check | Command | Exit | Summary |
| --- | --- | ---: | --- |
| Membership | brief § 2's Python block over `docs/reviews/inventory.json` | 0 | `paths 18 lines 3795 {'fork-own': 18} {'n/a': 18}`; python 12, shell 3, markdown 3 |
| Line and byte counts | `git show 8ebaf8daad:<path> \| wc -l` and `wc -c`, summed | 0 | 3,795 lines; 201,453 bytes |
| Provenance | `git cat-file -e upstream/next:<path>` for each; `git log c445081a59..8ebaf8daad -- <the 18>` | 0 | 0 of 18 upstream; 35 fork commits |
| Branch against hash | `xargs -0 git diff --stat 8ebaf8daad HEAD -- <the 18>` | 0 | empty |
| No tool changed | `git diff --stat cdc45513b0 HEAD -- tools`; the 18 against the hash | 0 | empty. `git diff --stat 8ebaf8daad HEAD -- tools` lists 15 files inherited before stage A (P1's three renovation tools, the coordinator's lint and `register-check`, the lint's fixtures), none of the 18 |
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
- **What the watcher said:** all 1,885 `build.status` files read `state: finished`. None reads `died`, `error`, `stalled` or `running`, and no run directory holds a `runner-error`. `finished` is the watcher's state, not success: the outcomes are rc 0 1,470; rc 1 397; rc 2 10; rc 125 4; rc 143 3; and rc 137, 130 and 127 one each (P11).
- **The 17 run directories without a `build.status`** are not watcher runs: hand-made folders of tracker readbacks, notes and a `__pycache__`, 16 in `conflict-resolution` and 1 in `m7-browser-memory-570`. Nothing reserves `.build-runs/` for the runner's `YYYYMMDDTHHMMSSZ-<hex>` runs; this is an observation, not a finding against these tools.
- **Admission timing:** `admission.json` exists in 664 runs, every one in the host's PID namespace (`4026531836`). Over the 663 that also have a readable `build.start`, `build.start` to `admitted` is a median of 0.09 s (0.08 to 0.19 s).
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
| P9 | The README's memory-guard-removed control ran once as a mutation (and F-11 is withdrawn at stage C because the boundary test is that control in effect) | `README.md:99`; the 2026-10-04 work log `:241`; `test-swap-reclaim:199-206` | proved: history |
| P10 | The three controls pass at `e198f0fc3b` (`d7e2d6be41^`) and fail at `d7e2d6be41`: F-01 began with the admission guard | exports under `/workspace/tmp/m6-t9/hist-*`, each control's rc and last line | proved: tool-run |
| P11 | The record's 1,885 terminal outcomes: rc 0 1,470; rc 1 397; rc 2 10; rc 125 4; rc 143 3; rc 137, 130 and 127 one each | the outcome lines read from every `build.status` | proved: tool-run |
| P12 | Two clones' admission registries on one volume: both `.git` on device 66304; `rocknix`'s holds `pixelelated-build-admission/`, `pixelelated/distribution`'s holds none | `stat -c %d` and `test -d` of both | proved: tool-run |
| P13 | S1 (#913): the three watcher controls pass at the fix (13/0, 35/0, rc 0) and each removed-admission copy fails (rc 1); the retention control passes beside a live process named `qemu-system-x86_64` where the unchanged control fails | `.qa-scratch/t9/s1-*.log`, `.qa-scratch/t9/positives/`; `9b071c5d12`, `a9bd346d54` | proved: fix-control |
| P14 | S2 (#914): `test-build-preflight` passes at the fix (8/0) and fails against the unfixed tool, which stopped the control's own sleeper, read `READY` over a failed census and missed the helper's swap boundary | `.qa-scratch/t9/s2-control-fixed.log`, `.qa-scratch/t9/positives/preflight-unfixed/`; `c9e38e2939` | proved: fix-control |
| P15 | S4 (#916): `test-watch-job.py` passes at the fix (36/0) with four new cases, each of which fails alone against the unfixed tool | `.qa-scratch/t9/s4-watch-job-fixed.log`, `.qa-scratch/t9/positives/watch-job-unfixed/`; `4a22ed0b41` | proved: fix-control |

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
| F-11 | Q7 | **Withdrawn at stage C.** `README.md:99`'s memory-guard-removed control *is* retained in effect: `test_insufficient_memory_and_boundary` (`test-swap-reclaim:199-206`) fails when the refusal is removed, which the 2026-10-04 mutation run (work log `:241`) proved once. | `tools/host-maintenance/README.md:95-101` |
| F-12 | Q3 | Admission reservations live in each clone's Git common directory, so two clones on one volume never see each other's reservations. On this host `/workspace/repos/rocknix/.git` (with a registry) and `/workspace/repos/pixelelated/distribution/.git` (without) are both on device 66304 (the seat's G-12). | `tools/host-maintenance/build-admission:77-80`, `:165-168`, `:202-204` |
| F-13 | Q3 | `install` installs, as root, whatever helper bytes sit beside it in a user-writable checkout, with no expected digest. A process running as `max` could plant a helper that later runs passwordless as root (G-08, narrowed to Medium). The installer is not crash-atomic (G-10), and its final check is an `assert` that `-O` removes (G-11). A contract change: a lead for the coordinator (D-INFRA-015). | `tools/host-maintenance/install:160-168`, `:106-157`, `:120` |
| F-14 | Q3 | `retention-report` parses its plan before the scan and hashes it after (G-40). It stamps `utc` at completion, so admission's 900 s window starts after the scan (G-41). Its reclaim figure sums candidates on any filesystem (G-45). | `tools/host-maintenance/retention-report:305-308`, `:293`, `:287` |
| F-15 | Q3 | `test-retention-report` is not host-isolated. It runs the real `report()`, which reads the real `/proc` and `docker ps`, so a live QEMU anywhere on the host flips its four positive cases (G-46). | `tools/host-maintenance/test-retention-report:37-43`; `retention-report:172-198` |
| F-16 | Q3 | `consume` compares the registry row by `run` only, where recovery compares it whole, so an edited `admission.json` drops checks (G-22). It writes `admission-consumed.json` before the registry commits, so a failed commit blocks every retry (G-26). | `tools/host-maintenance/build-admission:245-282`, `:440` |
| F-17 | Q3 | `reclaim-swap` defers only SIGINT, SIGTERM and SIGHUP: a SIGQUIT during `swapoff` leaves swap off, which the next preflight then reports (G-06). Its flushed `print` sits between the last check and `swapoff` (G-03). | `tools/host-maintenance/reclaim-swap:20`, `:157-184` |
| F-18 | Q2 | `watch-job` passes the caller's pattern to `grep` without `--`, so `--help` passes validation as grep's help (G-34). It writes `"$STATUS.pid"` and `.tmp` by name after resolving only `STATUS` (G-33). `mv` takes a dash-leading name as an option. | `tools/watch-job:107-108`, `:160`, `:216`, `:262`, `:266` |
| F-19 | Q3 | `watch-build-submit`'s fresh-owner check omits three of its own receipts (G-36). It starts the worker before writing `launcher-pid.json` exclusively (G-37). The worker forwards no signal to the runner (G-38). | `tools/watch-build-submit:69-71`, `:83-89`, `:30-50` |
| F-20 | Q3 | `fork-publish-release`: its byte binding is only as strong as the candidate store's immutability (G-54, outside the slice). A SIGTERM orphans the state-check group (G-55). | `tools/fork-publish-release:22-24`, `:89-97`, `:113` |
| F-21 | Q6 | The operational-guard boundaries the seat named: registry history and files inside `.git` (G-13, G-14); the inherited marker as a bearer token (G-15, G-16); `nested()`'s missing `BUILD_DIR` and mount checks (G-17); output overlap across worktrees (G-18); metadata-only protected identity (G-19); read-then-hash (G-21); escaped sessions (G-25); lexical containment, the PID view and receipt binding in the report (G-42 to G-44). Each is a contract question: a lead for the coordinator. | `04` § Second opinion |

**Re-grades at stage C** (`04` § Second opinion): F-04 and F-07 to Medium; F-08 to Medium, expanded; F-10 to Medium (G-49 to G-53); F-05 broadened to every failed identity read; F-06 joined by G-27 to G-30; F-03 joined by G-47 and G-48.

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
| `tools/host-maintenance/install` | 184 | install the helper and policy | host-scoped by design (`serval`, `max` uid 1000) | `-I`; `assert` used as a check (`:120`), which `python3 -O` would remove (G-11, F-13) | none found | Python 3 | n/a: run once, by an administrator | host and account checks: no control (F-08) | the policy line quoted in `04` § Q7, equal to the README's |
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

## Stage E

The streams of `t9-streams.md` (`4c842e2485`), each with its test first and its positive.

### S1 (#913; PL-01, PL-02, PL-15)

| Control | Before (the stage-D tip) | After (`9b071c5d12`, `a9bd346d54`) | Positive (`.qa-scratch/t9/positives/`) |
| --- | --- | --- | --- |
| `test-progress.py` | rc 1, `3 PASS; 10 FAIL`; the diagnostic copy with the module added: rc 1 | rc 0, `13 PASS; 0 FAIL` | admission removed: rc 1, `5 PASS; 8 FAIL` |
| `test-watch-build.py` (2026-10-04) | rc 1, `AssertionError: shared runner observes nested QA logs ...`; the diagnostic: rc 1 | rc 0, `35 PASS; 0 FAIL` | admission removed: rc 1 |
| `test-submit.py` | rc 1, `AssertionError`; the diagnostic's receipt `watch-build: build admission required` | rc 0, four rows; `/tmp` 10 → 10 | admission removed: rc 1; `/tmp` 10 → 10 |
| `test-retention-report` | rc 0 at a census of 0; beside a sleeper renamed `qemu-system-x86_64`: rc 1, the eligible case refused | rc 0, 20 controls (one new: an injected QEMU holds every candidate); beside the sleeper: rc 0 | the unchanged control beside the sleeper |

**`/tmp`:** this lane's six leftovers were removed by literal path; the four made before its runs stay (2026-10-05T07:42:06Z; 2026-10-24T14:58:26Z, 14:59:15Z, 15:22:36Z).


### S2 (#914; PL-03)

| Control | Before (unfixed tool, PATH doubles) | After (`c9e38e2939`) | Positive |
| --- | --- | --- | --- |
| `test-build-preflight` (new) | rc 1: `--stop-vms` stopped the control's own sleeper; `pgrep` exit 3 read `READY`; 200 MB free of 1001 MB was not exhausted | rc 0, `8 PASS; 0 FAIL` | the unfixed tool, `.qa-scratch/t9/positives/preflight-unfixed/` |

P14 in the table above.

### S4 (#916; PL-05, PL-18)

| Control | Before (unfixed tool) | After (`4a22ed0b41`) | Positive |
| --- | --- | --- | --- |
| `test-watch-job.py` (+4 cases) | rc 1; alone: `expected running: state: died` for PID 1; a dash pattern, a dash status and a linked `.pid`, each failing on its own label | rc 0, `36 PASS; 0 FAIL` | the unfixed copy, `.qa-scratch/t9/positives/watch-job-unfixed/` |

The EPERM input is PID 1, because `unshare` is refused here. A PID hidden by another namespace still reads as exited (#506); that limit is named, not fixed.

P15 in the table above.
