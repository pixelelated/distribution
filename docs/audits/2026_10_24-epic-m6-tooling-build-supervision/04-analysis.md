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
